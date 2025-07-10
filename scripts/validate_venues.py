#!/usr/bin/env python3
"""
Venue Data Validation and Processing Script
Part of Hardcore Geography Issue 01

This script validates venue data, checks geocoding accuracy,
and processes the raw CSV for quality control.
"""

import csv
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

def validate_coordinates(lat: str, lng: str) -> bool:
    """Validate latitude and longitude coordinates for Denver area."""
    try:
        lat_float = float(lat) if lat else 0
        lng_float = float(lng) if lng else 0
        
        # Denver approximate bounds
        # Latitude: 39.6 to 39.8 (roughly)
        # Longitude: -105.1 to -104.8 (roughly)
        if 39.5 <= lat_float <= 39.9 and -105.2 <= lng_float <= -104.7:
            return True
        return False
    except ValueError:
        return False

def validate_year_range(year_range: str) -> bool:
    """Validate year range format (YYYY-YYYY or YYYY-present)."""
    if not year_range:
        return False
    
    patterns = [
        r'^\d{4}-\d{4}$',      # 1998-2005
        r'^\d{4}-present$',     # 2016-present
        r'^\d{4}$',            # 1998 (single year)
        r'^\d{4}s-\d{4}s$',    # 1980s-1990s
        r'^\d{4}s-present$',   # 1980s-present
    ]
    
    return any(re.match(pattern, year_range) for pattern in patterns)

def validate_venue_data(row: Dict[str, str]) -> List[str]:
    """Validate a single venue record and return list of issues."""
    issues = []
    
    # Required fields check
    required_fields = ['name', 'active_years']
    for field in required_fields:
        if not row.get(field, '').strip():
            issues.append(f"Missing required field: {field}")
    
    # Coordinate validation
    lat = row.get('lat', '')
    lng = row.get('lng', '')
    if lat and lng:
        if not validate_coordinates(lat, lng):
            issues.append(f"Invalid coordinates: {lat}, {lng}")
    elif lat or lng:
        issues.append("Incomplete coordinates (missing lat or lng)")
    
    # Year range validation
    year_range = row.get('active_years', '')
    if year_range and not validate_year_range(year_range):
        issues.append(f"Invalid year range format: {year_range}")
    
    # Address validation (basic)
    address = row.get('address', '')
    if address and address.lower() == 'address tbd':
        issues.append("Address needs research")
    
    return issues

def process_venue_csv(input_file: str, output_file: Optional[str] = None) -> None:
    """Process venue CSV file and generate validation report."""
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"Error: File {input_file} not found")
        sys.exit(1)
    
    venues = []
    all_issues = []
    
    with open(input_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row_num, row in enumerate(reader, start=2):  # Start at 2 for header
            venues.append(row)
            issues = validate_venue_data(row)
            if issues:
                all_issues.extend([f"Row {row_num} ({row.get('name', 'Unknown')}): {issue}" 
                                 for issue in issues])
    
    # Print validation report
    print(f"Venue Database Validation Report")
    print(f"=" * 40)
    print(f"Total venues: {len(venues)}")
    print(f"Total issues found: {len(all_issues)}")
    print()
    
    if all_issues:
        print("Issues Found:")
        for issue in all_issues:
            print(f"  - {issue}")
    else:
        print("✅ All venue records passed validation!")
    
    # Summary statistics
    venues_with_coords = sum(1 for v in venues if v.get('lat') and v.get('lng'))
    venues_need_research = sum(1 for v in venues if 'research needed' in v.get('documentation_status', '').lower())
    active_venues = sum(1 for v in venues if 'present' in v.get('active_years', '').lower())
    
    print(f"\nStatistics:")
    print(f"  - Venues with coordinates: {venues_with_coords}/{len(venues)}")
    print(f"  - Venues needing research: {venues_need_research}")
    print(f"  - Currently active venues: {active_venues}")
    
    # Generate clean output if requested
    if output_file:
        output_path = Path(output_file)
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            if venues:
                writer = csv.DictWriter(csvfile, fieldnames=venues[0].keys())
                writer.writeheader()
                writer.writerows(venues)
        print(f"\nClean data written to: {output_file}")

def main():
    """Main function to run venue validation."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Validate venue database')
    parser.add_argument('input_file', help='Input CSV file path')
    parser.add_argument('--output', '-o', help='Output processed CSV file')
    
    args = parser.parse_args()
    
    process_venue_csv(args.input_file, args.output)

if __name__ == "__main__":
    main()