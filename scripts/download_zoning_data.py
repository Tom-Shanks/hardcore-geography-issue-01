#!/usr/bin/env python3
"""
Denver Zoning Data Download and Processing Script
Downloads Denver zoning data and creates spatial joins with venue locations.
"""

import json
import csv
import os
from urllib.request import urlopen
from urllib.error import URLError
import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance between two points on the earth in kilometers."""
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r

def fetch_denver_zoning_data():
    """Fetch Denver zoning data from the ArcGIS REST API."""
    # Denver zoning districts API endpoint
    base_url = "https://services6.arcgis.com/DZHaqZm9cxOD4CWM/arcgis/rest/services/ZONING_DISTRICTS/FeatureServer/0/query"
    
    params = {
        'where': '1=1',
        'outFields': 'OBJECTID,ZONE_DISTRICTS,ZONE_DESCRIPTION',
        'returnGeometry': 'true',
        'geometryType': 'esriGeometryPolygon',
        'spatialRel': 'esriSpatialRelIntersects',
        'outSR': '4326',  # WGS84 coordinate system
        'f': 'json'
    }
    
    # Build URL with parameters
    url = base_url + "?" + "&".join([f"{k}={v}" for k, v in params.items()])
    
    try:
        print(f"Fetching zoning data from: {url}")
        with urlopen(url) as response:
            data = json.loads(response.read().decode())
            
        if 'features' in data:
            print(f"Successfully fetched {len(data['features'])} zoning districts")
            return data['features']
        else:
            print("No zoning features found in response")
            return []
            
    except URLError as e:
        print(f"Error fetching zoning data: {e}")
        return []

def point_in_polygon(point, polygon):
    """Check if a point is inside a polygon using ray casting algorithm."""
    x, y = point
    n = len(polygon)
    inside = False
    
    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    
    return inside

def assign_zoning_to_venues(venues, zoning_features):
    """Assign zoning classifications to venues based on their coordinates."""
    results = []
    
    for venue in venues:
        # Skip venues without coordinates
        if not venue.get('lat') or not venue.get('lng'):
            results.append({
                **venue,
                'zoning_type': 'Unknown',
                'zoning_description': 'No coordinates available',
                'zoning_method': 'N/A'
            })
            continue
            
        venue_point = (float(venue['lng']), float(venue['lat']))
        assigned_zoning = None
        closest_distance = float('inf')
        
        # Check each zoning district
        for feature in zoning_features:
            geometry = feature.get('geometry', {})
            attributes = feature.get('attributes', {})
            
            if geometry.get('type') == 'Polygon':
                # Handle single polygon
                rings = geometry.get('rings', [])
                if rings:
                    exterior_ring = rings[0]  # First ring is exterior
                    
                    # Check if point is inside polygon
                    if point_in_polygon(venue_point, exterior_ring):
                        assigned_zoning = {
                            'zoning_type': attributes.get('ZONE_DISTRICTS', 'Unknown'),
                            'zoning_description': attributes.get('ZONE_DESCRIPTION', 'No description'),
                            'zoning_method': 'Point-in-polygon'
                        }
                        break
                    
                    # Calculate distance to polygon centroid as fallback
                    if rings:
                        centroid_x = sum(p[0] for p in exterior_ring) / len(exterior_ring)
                        centroid_y = sum(p[1] for p in exterior_ring) / len(exterior_ring)
                        
                        distance = haversine_distance(
                            venue_point[1], venue_point[0],
                            centroid_y, centroid_x
                        )
                        
                        if distance < closest_distance:
                            closest_distance = distance
                            assigned_zoning = {
                                'zoning_type': attributes.get('ZONE_DISTRICTS', 'Unknown'),
                                'zoning_description': attributes.get('ZONE_DESCRIPTION', 'No description'),
                                'zoning_method': f'Nearest (distance: {distance:.2f}km)'
                            }
        
        # If no zoning found, use unknown
        if not assigned_zoning:
            assigned_zoning = {
                'zoning_type': 'Unknown',
                'zoning_description': 'No zoning district found',
                'zoning_method': 'No match'
            }
        
        results.append({
            **venue,
            **assigned_zoning
        })
    
    return results

def load_venue_data(filename):
    """Load venue data from CSV file."""
    venues = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                venues.append(row)
        print(f"Loaded {len(venues)} venues from {filename}")
        return venues
    except FileNotFoundError:
        print(f"Error: Could not find file {filename}")
        return []

def save_venues_zoning(venues_with_zoning, filename):
    """Save venues with zoning data to CSV file."""
    if not venues_with_zoning:
        print("No data to save")
        return
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Get all field names
    fieldnames = list(venues_with_zoning[0].keys())
    
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(venues_with_zoning)
    
    print(f"Saved {len(venues_with_zoning)} venues with zoning data to {filename}")

def main():
    """Main function to orchestrate the data processing."""
    print("Denver Zoning Data Integration Script")
    print("=" * 50)
    
    # File paths
    input_file = "data/raw/hg-01-venues-raw.csv"
    output_file = "data/processed/hg-01-venues-zoning.csv"
    
    # Load venue data
    venues = load_venue_data(input_file)
    if not venues:
        print("No venue data loaded. Exiting.")
        return
    
    # Fetch zoning data
    zoning_features = fetch_denver_zoning_data()
    if not zoning_features:
        print("No zoning data fetched. Exiting.")
        return
    
    # Process spatial joins
    print("\nProcessing spatial joins...")
    venues_with_zoning = assign_zoning_to_venues(venues, zoning_features)
    
    # Save results
    save_venues_zoning(venues_with_zoning, output_file)
    
    # Print summary
    print("\nProcessing Summary:")
    print(f"Total venues processed: {len(venues_with_zoning)}")
    
    zoning_counts = {}
    for venue in venues_with_zoning:
        zoning_type = venue.get('zoning_type', 'Unknown')
        zoning_counts[zoning_type] = zoning_counts.get(zoning_type, 0) + 1
    
    print("Zoning distribution:")
    for zoning_type, count in sorted(zoning_counts.items()):
        print(f"  {zoning_type}: {count} venues")

if __name__ == "__main__":
    main()