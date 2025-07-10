#!/usr/bin/env python3
"""
Create Mock Denver Zoning Data for Demonstration
This script creates realistic mock zoning data for the Denver area to demonstrate 
the spatial join functionality when real API access is not available.
"""

import csv
import json
import os
import random
from datetime import datetime

# Denver zoning classifications based on actual Denver Zoning Code
DENVER_ZONING_TYPES = {
    'M-I': 'Mixed Use - Industrial',
    'M-C': 'Mixed Use - Commercial', 
    'I-B': 'Industrial - Business',
    'I-M': 'Industrial - Manufacturing',
    'C-G': 'Commercial - General',
    'C-H': 'Commercial - Heavy',
    'C-L': 'Commercial - Light',
    'U-MS': 'Urban - Mixed Use',
    'D-C': 'Downtown - Commercial',
    'D-CV': 'Downtown - Central Core',
    'R-1': 'Residential - Single Family',
    'R-2': 'Residential - Two Family',
    'R-3': 'Residential - Multi-Family',
    'R-4': 'Residential - High Density',
    'R-X': 'Residential - Mixed Use',
    'OS-A': 'Open Space - Parks',
    'OS-B': 'Open Space - Recreation'
}

# Neighborhood-based zoning assignments (typical patterns)
NEIGHBORHOOD_ZONING = {
    'Five Points': ['M-I', 'M-C', 'I-B', 'R-3', 'R-4'],
    'RiNo': ['M-I', 'M-C', 'I-B', 'U-MS', 'R-X'],
    'Baker': ['M-C', 'C-L', 'R-2', 'R-3', 'R-X'],
    'Capitol Hill': ['M-C', 'C-L', 'R-3', 'R-4', 'U-MS'],
    'South Broadway': ['C-G', 'C-L', 'M-C', 'R-2', 'R-3'],
    'Colfax': ['C-G', 'C-L', 'M-C', 'R-3', 'R-4'],
    'Downtown': ['D-C', 'D-CV', 'C-G', 'C-H', 'M-C'],
    'Highlands': ['R-1', 'R-2', 'R-3', 'C-L', 'M-C'],
    'Stapleton': ['R-1', 'R-2', 'R-3', 'C-L', 'OS-A'],
    'Lowry': ['R-1', 'R-2', 'R-3', 'C-L', 'OS-A'],
    'Westwood': ['R-1', 'R-2', 'I-B', 'M-I', 'C-L'],
    'Globeville': ['I-B', 'I-M', 'M-I', 'R-2', 'R-3'],
    'Elyria-Swansea': ['I-B', 'I-M', 'M-I', 'R-2', 'R-3'],
    'Montbello': ['R-1', 'R-2', 'R-3', 'C-L', 'I-B'],
    'Green Valley Ranch': ['R-1', 'R-2', 'R-3', 'C-L', 'OS-A']
}

def estimate_neighborhood_from_address(address):
    """Estimate neighborhood from address for zoning assignment."""
    address_lower = address.lower()
    
    # Common street/area indicators
    if 'welton' in address_lower or '5 point' in address_lower or 'five point' in address_lower:
        return 'Five Points'
    elif 'larimer' in address_lower or 'rino' in address_lower or 'river north' in address_lower:
        return 'RiNo'
    elif 'broadway' in address_lower and ('s ' in address_lower or 'south' in address_lower):
        return 'South Broadway'
    elif 'colfax' in address_lower:
        return 'Colfax'
    elif 'lincoln' in address_lower or 'glenarm' in address_lower or 'market' in address_lower:
        return 'Downtown'
    elif 'baker' in address_lower or 'santa fe' in address_lower:
        return 'Baker'
    elif 'capitol hill' in address_lower or 'cap hill' in address_lower:
        return 'Capitol Hill'
    elif 'highlands' in address_lower or 'highland' in address_lower:
        return 'Highlands'
    elif 'stapleton' in address_lower:
        return 'Stapleton'
    elif 'lowry' in address_lower:
        return 'Lowry'
    elif 'westwood' in address_lower:
        return 'Westwood'
    elif 'globeville' in address_lower:
        return 'Globeville'
    elif 'elyria' in address_lower or 'swansea' in address_lower:
        return 'Elyria-Swansea'
    elif 'montbello' in address_lower:
        return 'Montbello'
    elif 'green valley' in address_lower:
        return 'Green Valley Ranch'
    else:
        return 'Central Denver'  # Default

def assign_zoning_based_on_venue_type(venue_name, address, active_years):
    """Assign realistic zoning based on venue characteristics."""
    venue_lower = venue_name.lower()
    neighborhood = estimate_neighborhood_from_address(address)
    
    # Get neighborhood-specific zoning options
    if neighborhood in NEIGHBORHOOD_ZONING:
        zoning_options = NEIGHBORHOOD_ZONING[neighborhood]
    else:
        # Default urban mixed zoning
        zoning_options = ['M-C', 'C-L', 'R-3', 'R-4', 'U-MS']
    
    # Industrial/warehouse venues typically in industrial zones
    if any(word in venue_lower for word in ['warehouse', 'industrial', 'factory', 'collective']):
        preferred_zones = ['M-I', 'I-B', 'I-M']
        zoning_options = [z for z in zoning_options if z in preferred_zones] or preferred_zones
    
    # Commercial venues in commercial zones
    elif any(word in venue_lower for word in ['bar', 'club', 'lounge', 'restaurant', 'theatre', 'theater']):
        preferred_zones = ['C-G', 'C-L', 'M-C', 'D-C']
        zoning_options = [z for z in zoning_options if z in preferred_zones] or preferred_zones
    
    # Mixed use venues
    elif any(word in venue_lower for word in ['art', 'gallery', 'studio', 'space', 'center']):
        preferred_zones = ['M-C', 'U-MS', 'R-X']
        zoning_options = [z for z in zoning_options if z in preferred_zones] or preferred_zones
    
    # Select zoning type
    zoning_type = random.choice(zoning_options)
    
    # Assign historical context based on active years
    start_year = 2000  # Default
    if active_years:
        # Extract year from various formats
        import re
        year_match = re.search(r'(\d{4})', active_years)
        if year_match:
            start_year = int(year_match.group(1))
        elif 's-' in active_years.lower():  # Handle "1990s-present" etc
            decade_match = re.search(r'(\d{3})0s', active_years)
            if decade_match:
                start_year = int(decade_match.group(1) + '0')
    
    if start_year < 2000:
        # Pre-2000: More industrial zoning
        if zoning_type not in ['M-I', 'I-B', 'I-M']:
            zoning_type = random.choice(['M-I', 'I-B', 'C-G'])
        zoning_year = random.randint(1975, 1999)
        land_use_change = 'Pre-gentrification industrial'
    elif start_year < 2010:
        # 2000-2010: Mixed use transition
        zoning_year = random.randint(2000, 2009)
        land_use_change = 'Early mixed-use rezoning'
    else:
        # 2010+: Modern mixed use
        zoning_year = random.randint(2010, 2020)
        land_use_change = 'Post-recession development'
    
    return {
        'zoning_type': zoning_type,
        'zoning_description': DENVER_ZONING_TYPES[zoning_type],
        'zoning_year': zoning_year,
        'land_use_change': land_use_change,
        'neighborhood': neighborhood
    }

def calculate_venue_density(venues_with_zoning):
    """Calculate venue density by zoning district."""
    zoning_counts = {}
    neighborhood_counts = {}
    
    for venue in venues_with_zoning:
        zoning_type = venue['zoning_type']
        neighborhood = venue['neighborhood']
        
        zoning_counts[zoning_type] = zoning_counts.get(zoning_type, 0) + 1
        neighborhood_counts[neighborhood] = neighborhood_counts.get(neighborhood, 0) + 1
    
    # Add density calculations
    for venue in venues_with_zoning:
        venue['zoning_density'] = zoning_counts[venue['zoning_type']]
        venue['neighborhood_density'] = neighborhood_counts[venue['neighborhood']]
    
    return venues_with_zoning

def identify_displacement_patterns(venues_with_zoning):
    """Identify displacement patterns based on closure patterns."""
    # Count closures by neighborhood and zoning type
    closure_patterns = {}
    
    for venue in venues_with_zoning:
        active_years = venue.get('active_years', '')
        closure_reason = venue.get('closure_reason', '')
        neighborhood = venue.get('neighborhood', 'Unknown')
        
        # Check if venue closed due to development/displacement
        is_displacement = any(word in closure_reason.lower() for word in [
            'development', 'rent', 'eviction', 'gentrification', 'demolition', 
            'redevelopment', 'displacement', 'lease'
        ])
        
        if is_displacement:
            if neighborhood not in closure_patterns:
                closure_patterns[neighborhood] = []
            closure_patterns[neighborhood].append(venue)
    
    # Add displacement pattern indicators
    for venue in venues_with_zoning:
        neighborhood = venue.get('neighborhood', 'Unknown')
        if neighborhood in closure_patterns:
            venue['displacement_pattern'] = f"High risk: {len(closure_patterns[neighborhood])} closures"
        else:
            venue['displacement_pattern'] = "Low risk"
    
    return venues_with_zoning

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
    """Main function to create mock zoning data."""
    print("Creating Mock Denver Zoning Data")
    print("=" * 50)
    
    # File paths
    input_file = "data/raw/hg-01-venues-raw.csv"
    output_file = "data/processed/hg-01-venues-zoning.csv"
    
    # Load venue data
    venues = load_venue_data(input_file)
    if not venues:
        print("No venue data loaded. Exiting.")
        return
    
    # Process venues with mock zoning data
    venues_with_zoning = []
    
    for venue in venues:
        # Assign zoning based on venue characteristics
        zoning_info = assign_zoning_based_on_venue_type(
            venue.get('name', ''),
            venue.get('address', ''),
            venue.get('active_years', '')
        )
        
        # Combine original venue data with zoning info
        venue_with_zoning = {**venue, **zoning_info}
        venues_with_zoning.append(venue_with_zoning)
    
    # Calculate density and displacement patterns
    venues_with_zoning = calculate_venue_density(venues_with_zoning)
    venues_with_zoning = identify_displacement_patterns(venues_with_zoning)
    
    # Save results
    save_venues_zoning(venues_with_zoning, output_file)
    
    # Print summary
    print("\nProcessing Summary:")
    print(f"Total venues processed: {len(venues_with_zoning)}")
    
    # Zoning distribution
    zoning_counts = {}
    for venue in venues_with_zoning:
        zoning_type = venue.get('zoning_type', 'Unknown')
        zoning_counts[zoning_type] = zoning_counts.get(zoning_type, 0) + 1
    
    print("\nZoning distribution:")
    for zoning_type, count in sorted(zoning_counts.items()):
        print(f"  {zoning_type}: {count} venues")
    
    # Neighborhood distribution
    neighborhood_counts = {}
    for venue in venues_with_zoning:
        neighborhood = venue.get('neighborhood', 'Unknown')
        neighborhood_counts[neighborhood] = neighborhood_counts.get(neighborhood, 0) + 1
    
    print("\nNeighborhood distribution:")
    for neighborhood, count in sorted(neighborhood_counts.items()):
        print(f"  {neighborhood}: {count} venues")
    
    # Displacement patterns
    displacement_venues = [v for v in venues_with_zoning if "High risk" in v.get('displacement_pattern', '')]
    print(f"\nDisplacement analysis:")
    print(f"  High-risk venues: {len(displacement_venues)}")
    print(f"  Low-risk venues: {len(venues_with_zoning) - len(displacement_venues)}")

if __name__ == "__main__":
    main()