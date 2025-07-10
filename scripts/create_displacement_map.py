#!/usr/bin/env python3
"""
Denver DIY Displacement Map Generator
Creates a static choropleth map showing venue displacement patterns by neighborhood
with print-ready specifications for the Hardcore Geography zine.
"""

import csv
import json
import os
from datetime import datetime

def create_svg_map():
    """Create an SVG-based displacement overview map."""
    # Map dimensions for half-letter format (5.5" x 8.5") at 300 DPI
    width = 1650  # 5.5" * 300 DPI
    height = 2550  # 8.5" * 300 DPI
    map_area_height = 1800  # Leave space for legend and title
    
    # Color scheme: Grayscale + red spot color
    colors = {
        'background': '#ffffff',
        'water': '#f0f0f0',
        'low_risk': '#d0d0d0',
        'medium_risk': '#999999', 
        'high_risk': '#ff0000',  # Red spot color for closures
        'venue_active': '#333333',
        'venue_closed': '#ff0000',
        'text': '#000000',
        'grid': '#cccccc'
    }
    
    # Create SVG header
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" 
     xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Define patterns for QR block-style legend icons -->
    <pattern id="highRiskPattern" patternUnits="userSpaceOnUse" width="8" height="8">
      <rect width="8" height="8" fill="{colors['high_risk']}"/>
      <rect x="2" y="2" width="2" height="2" fill="white"/>
      <rect x="6" y="2" width="2" height="2" fill="white"/>
      <rect x="2" y="6" width="2" height="2" fill="white"/>
    </pattern>
    <pattern id="mediumRiskPattern" patternUnits="userSpaceOnUse" width="8" height="8">
      <rect width="8" height="8" fill="{colors['medium_risk']}"/>
      <rect x="1" y="1" width="2" height="2" fill="white"/>
      <rect x="5" y="1" width="2" height="2" fill="white"/>
      <rect x="3" y="5" width="2" height="2" fill="white"/>
    </pattern>
    <pattern id="lowRiskPattern" patternUnits="userSpaceOnUse" width="8" height="8">
      <rect width="8" height="8" fill="{colors['low_risk']}"/>
      <rect x="3" y="1" width="2" height="2" fill="white"/>
      <rect x="1" y="5" width="2" height="2" fill="white"/>
      <rect x="5" y="5" width="2" height="2" fill="white"/>
    </pattern>
  </defs>
  
  <!-- Background -->
  <rect width="{width}" height="{height}" fill="{colors['background']}"/>
  
  <!-- Title Area -->
  <rect x="50" y="50" width="{width-100}" height="200" fill="none" stroke="{colors['text']}" stroke-width="2"/>
  <text x="{width//2}" y="120" text-anchor="middle" font-family="monospace" font-size="36" font-weight="bold" fill="{colors['text']}">
    DENVER DIY DISPLACEMENT OVERVIEW
  </text>
  <text x="{width//2}" y="160" text-anchor="middle" font-family="monospace" font-size="24" fill="{colors['text']}">
    Venue Closures by Neighborhood Risk Pattern
  </text>
  <text x="{width//2}" y="200" text-anchor="middle" font-family="monospace" font-size="18" fill="{colors['text']}">
    1995 → 2025
  </text>'''
    
    # Map area coordinates (simplified Denver neighborhoods)
    map_y_start = 300
    neighborhoods = [
        # (name, x, y, width, height, risk_level, venue_count, closure_count)
        ("Five Points", 400, map_y_start + 200, 200, 150, "medium", 1, 0),
        ("RiNo", 620, map_y_start + 200, 250, 180, "low", 2, 0),
        ("Downtown", 300, map_y_start + 400, 300, 200, "high", 3, 1),
        ("Capitol Hill", 650, map_y_start + 450, 280, 220, "medium", 0, 0),
        ("Baker", 200, map_y_start + 650, 200, 150, "medium", 0, 0),
        ("Colfax Corridor", 450, map_y_start + 600, 400, 100, "low", 6, 0),
        ("South Broadway", 150, map_y_start + 850, 180, 300, "high", 5, 1),
        ("Central Denver", 400, map_y_start + 900, 350, 250, "high", 13, 4)
    ]
    
    # Draw neighborhoods
    for name, x, y, w, h, risk, venues, closures in neighborhoods:
        # Determine fill pattern based on risk
        if risk == "high":
            fill = f"url(#highRiskPattern)"
        elif risk == "medium":
            fill = f"url(#mediumRiskPattern)"
        else:
            fill = f"url(#lowRiskPattern)"
        
        # Draw neighborhood boundary
        svg_content += f'''
  <!-- {name} -->
  <rect x="{x}" y="{y}" width="{w}" height="{h}" 
        fill="{fill}" stroke="{colors['text']}" stroke-width="1.5" opacity="0.8"/>
  <text x="{x + w//2}" y="{y + h//2 - 20}" text-anchor="middle" 
        font-family="monospace" font-size="14" font-weight="bold" fill="{colors['text']}">
    {name.upper()}
  </text>
  <text x="{x + w//2}" y="{y + h//2}" text-anchor="middle" 
        font-family="monospace" font-size="12" fill="{colors['text']}">
    {venues} venues
  </text>
  <text x="{x + w//2}" y="{y + h//2 + 20}" text-anchor="middle" 
        font-family="monospace" font-size="12" fill="{colors['high_risk']}">
    {closures} closures
  </text>'''
    
    # Add venue markers (simplified positioning)
    venue_markers = [
        # High-closure neighborhoods get red closure markers
        (450, map_y_start + 500, "closed", "Downtown venues"),
        (250, map_y_start + 950, "closed", "South Broadway"),
        (575, map_y_start + 1000, "closed", "Central Denver cluster"),
        (650, map_y_start + 1050, "closed", "Central Denver cluster"),
        
        # Active venues in various locations
        (720, map_y_start + 280, "active", "RiNo active"),
        (800, map_y_start + 320, "active", "RiNo active"),
        (500, map_y_start + 680, "active", "Colfax active"),
        (600, map_y_start + 680, "active", "Colfax active"),
        (700, map_y_start + 680, "active", "Colfax active"),
    ]
    
    # Draw venue markers
    for x, y, status, label in venue_markers:
        if status == "closed":
            color = colors['venue_closed']
            marker = "✕"
            size = "16"
        else:
            color = colors['venue_active']
            marker = "●"
            size = "12"
        
        svg_content += f'''
  <text x="{x}" y="{y}" text-anchor="middle" font-family="monospace" 
        font-size="{size}" fill="{color}" font-weight="bold">{marker}</text>'''
    
    # Legend area
    legend_y = map_y_start + 1300
    svg_content += f'''
  
  <!-- Legend -->
  <rect x="100" y="{legend_y}" width="{width-200}" height="350" 
        fill="none" stroke="{colors['text']}" stroke-width="2"/>
  <text x="150" y="{legend_y + 40}" font-family="monospace" font-size="20" 
        font-weight="bold" fill="{colors['text']}">LEGEND</text>
  
  <!-- QR-style legend icons -->
  <rect x="150" y="{legend_y + 70}" width="40" height="40" fill="url(#highRiskPattern)"/>
  <text x="210" y="{legend_y + 95}" font-family="monospace" font-size="14" fill="{colors['text']}">
    HIGH DISPLACEMENT RISK (4+ closures)
  </text>
  
  <rect x="150" y="{legend_y + 130}" width="40" height="40" fill="url(#mediumRiskPattern)"/>
  <text x="210" y="{legend_y + 155}" font-family="monospace" font-size="14" fill="{colors['text']}">
    MEDIUM DISPLACEMENT RISK (1-3 closures)
  </text>
  
  <rect x="150" y="{legend_y + 190}" width="40" height="40" fill="url(#lowRiskPattern)"/>
  <text x="210" y="{legend_y + 215}" font-family="monospace" font-size="14" fill="{colors['text']}">
    LOW DISPLACEMENT RISK (0 closures)
  </text>
  
  <!-- Venue markers legend -->
  <text x="800" y="{legend_y + 95}" text-anchor="middle" font-family="monospace" 
        font-size="16" fill="{colors['venue_closed']}" font-weight="bold">✕</text>
  <text x="850" y="{legend_y + 95}" font-family="monospace" font-size="14" fill="{colors['text']}">
    CLOSED VENUE
  </text>
  
  <text x="800" y="{legend_y + 135}" text-anchor="middle" font-family="monospace" 
        font-size="12" fill="{colors['venue_active']}" font-weight="bold">●</text>
  <text x="850" y="{legend_y + 135}" font-family="monospace" font-size="14" fill="{colors['text']}">
    ACTIVE VENUE
  </text>
  
  <!-- Data source -->
  <text x="150" y="{legend_y + 280}" font-family="monospace" font-size="10" fill="{colors['text']}">
    Data: Hardcore Geography Venue Database, 2024
  </text>
  <text x="150" y="{legend_y + 300}" font-family="monospace" font-size="10" fill="{colors['text']}">
    Sources: Denver Open Data, venue documentation, field research
  </text>
  <text x="150" y="{legend_y + 320}" font-family="monospace" font-size="10" fill="{colors['text']}">
    Analysis: Zoning classifications and closure patterns (1995-2025)
  </text>
</svg>'''
    
    return svg_content

def load_venue_data(filename):
    """Load processed venue data with zoning information."""
    venues = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                venues.append(row)
        print(f"Loaded {len(venues)} venues with zoning data")
        return venues
    except FileNotFoundError:
        print(f"Error: Could not find file {filename}")
        return []

def analyze_displacement_data(venues):
    """Analyze venue data for displacement patterns."""
    analysis = {
        'total_venues': len(venues),
        'closed_venues': 0,
        'active_venues': 0,
        'high_risk_neighborhoods': set(),
        'displacement_closures': 0,
        'by_neighborhood': {},
        'by_zoning': {}
    }
    
    for venue in venues:
        # Count active vs closed
        if 'present' in venue.get('active_years', '').lower():
            analysis['active_venues'] += 1
        else:
            analysis['closed_venues'] += 1
        
        # Count displacement-related closures
        closure_reason = venue.get('closure_reason', '').lower()
        if any(word in closure_reason for word in ['development', 'closure', 'eviction']):
            analysis['displacement_closures'] += 1
        
        # Neighborhood analysis
        neighborhood = venue.get('neighborhood', 'Unknown')
        if neighborhood not in analysis['by_neighborhood']:
            analysis['by_neighborhood'][neighborhood] = {'total': 0, 'closed': 0, 'risk': 'Low'}
        
        analysis['by_neighborhood'][neighborhood]['total'] += 1
        
        if 'High risk' in venue.get('displacement_pattern', ''):
            analysis['by_neighborhood'][neighborhood]['risk'] = 'High'
            analysis['high_risk_neighborhoods'].add(neighborhood)
        
        # Zoning analysis
        zoning = venue.get('zoning_type', 'Unknown')
        if zoning not in analysis['by_zoning']:
            analysis['by_zoning'][zoning] = 0
        analysis['by_zoning'][zoning] += 1
    
    return analysis

def create_data_summary(venues, analysis):
    """Create a data summary for inclusion in the map or separate documentation."""
    summary = f"""
DENVER DIY DISPLACEMENT DATA SUMMARY

OVERVIEW:
Total venues documented: {analysis['total_venues']}
Active venues: {analysis['active_venues']}
Closed venues: {analysis['closed_venues']}
Displacement-related closures: {analysis['displacement_closures']}

HIGH-RISK NEIGHBORHOODS:
{', '.join(sorted(analysis['high_risk_neighborhoods']))}

VENUE DISTRIBUTION BY ZONING:
"""
    
    for zoning, count in sorted(analysis['by_zoning'].items()):
        summary += f"  {zoning}: {count} venues\n"
    
    summary += f"""
NEIGHBORHOOD ANALYSIS:
"""
    
    for neighborhood, data in sorted(analysis['by_neighborhood'].items()):
        summary += f"  {neighborhood}: {data['total']} venues ({data['risk']} risk)\n"
    
    return summary

def main():
    """Main function to create the displacement map."""
    print("Creating Denver DIY Displacement Overview Map")
    print("=" * 60)
    
    # Load venue data
    input_file = "data/processed/hg-01-venues-zoning.csv"
    venues = load_venue_data(input_file)
    
    if not venues:
        print("No venue data available. Cannot create map.")
        return
    
    # Analyze displacement patterns
    analysis = analyze_displacement_data(venues)
    print(f"Analyzed {analysis['total_venues']} venues:")
    print(f"  Active: {analysis['active_venues']}")
    print(f"  Closed: {analysis['closed_venues']}")
    print(f"  High-risk neighborhoods: {len(analysis['high_risk_neighborhoods'])}")
    
    # Create output directory
    output_dir = "assets/maps"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate SVG map
    print("\nGenerating displacement overview map...")
    svg_content = create_svg_map()
    
    # Save SVG file
    svg_filename = f"{output_dir}/hg-01-displacement-overview.svg"
    with open(svg_filename, 'w', encoding='utf-8') as file:
        file.write(svg_content)
    
    print(f"Saved SVG map: {svg_filename}")
    
    # Create data summary
    summary = create_data_summary(venues, analysis)
    summary_filename = f"{output_dir}/hg-01-displacement-data-summary.txt"
    with open(summary_filename, 'w', encoding='utf-8') as file:
        file.write(summary)
    
    print(f"Saved data summary: {summary_filename}")
    
    # Print next steps
    print("\nNext steps for map production:")
    print("1. Convert SVG to PNG at 300 DPI using:")
    print(f"   inkscape --export-png={output_dir}/hg-01-displacement-overview_300dpi.png --export-dpi=300 {svg_filename}")
    print("2. Export PDF version:")
    print(f"   inkscape --export-pdf={output_dir}/hg-01-displacement-overview.pdf {svg_filename}")
    print("3. Verify half-letter format compatibility (5.5\" x 8.5\")")
    print("4. Test print reproduction quality")

if __name__ == "__main__":
    main()