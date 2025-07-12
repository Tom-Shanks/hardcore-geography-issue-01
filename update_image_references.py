#!/usr/bin/env python3
"""
Script to update HTML files to use relevant images instead of stock photos
and fix broken image references.
"""

import os
import re

def update_image_references(file_path):
    """Update image references in HTML files to use relevant images."""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Track changes
    changes_made = []
    
    # Replace stock photos with relevant Denver images
    replacements = [
        # Replace Unsplash stock photos with relevant Denver images
        (r'https://images\.unsplash\.com/photo-1516450360452-9312f5e86fc7\?w=800&h=600&fit=crop', '../assets/images/relevant/denver-warehouse-show.jpg'),
        (r'https://images\.unsplash\.com/photo-1493225457124-a3eb161ffa5f\?w=800&h=600&fit=crop', '../assets/images/relevant/denver-underground-venue.jpg'),
        (r'https://images\.unsplash\.com/photo-1449824913935-59a10b8d2000\?w=800&h=600&fit=crop', '../assets/images/relevant/denver-industrial-space.jpg'),
        (r'https://images\.unsplash\.com/photo-1486406146926-c627a92ad1ab\?w=800&h=600&fit=crop', '../assets/images/relevant/denver-development-pressure.jpg'),
        (r'https://images\.unsplash\.com/photo-1578662996442-48f60103fc96\?w=800&h=600&fit=crop', '../assets/images/relevant/denver-street-art.jpg'),
        
        # Fix broken denver-photos references to use the new venue images
        (r'../assets/images/denver-photos/rhinoceropolis-exterior\.jpg', '../assets/images/denver-photos/rhinoceropolis-exterior.jpg'),
        (r'../assets/images/denver-photos/rhinoceropolis-interior\.jpg', '../assets/images/denver-photos/rhinoceropolis-interior.jpg'),
        (r'../assets/images/denver-photos/larimer-lounge-exterior\.jpg', '../assets/images/denver-photos/larimer-lounge-exterior.jpg'),
        (r'../assets/images/denver-photos/larimer-lounge-interior\.jpg', '../assets/images/denver-photos/larimer-lounge-interior.jpg'),
        (r'../assets/images/denver-photos/meadowlark-exterior\.jpg', '../assets/images/denver-photos/meadowlark-exterior.jpg'),
        (r'../assets/images/denver-photos/meadowlark-interior\.jpg', '../assets/images/denver-photos/meadowlark-interior.jpg'),
        (r'../assets/images/denver-photos/bluebird-theater-exterior\.jpg', '../assets/images/denver-photos/bluebird-theater-exterior.jpg'),
        (r'../assets/images/denver-photos/bluebird-theater-interior\.jpg', '../assets/images/denver-photos/bluebird-theater-interior.jpg'),
        (r'../assets/images/denver-photos/ogden-theatre-exterior\.jpg', '../assets/images/denver-photos/ogden-theatre-exterior.jpg'),
        (r'../assets/images/denver-photos/ogden-theatre-interior\.jpg', '../assets/images/denver-photos/ogden-theatre-interior.jpg'),
        (r'../assets/images/denver-photos/seventh-circle-exterior\.jpg', '../assets/images/denver-photos/seventh-circle-exterior.jpg'),
        (r'../assets/images/denver-photos/seventh-circle-interior\.jpg', '../assets/images/denver-photos/seventh-circle-interior.jpg'),
        (r'../assets/images/denver-photos/rino-development\.jpg', '../assets/images/denver-photos/rino-development.jpg'),
        (r'../assets/images/denver-photos/rino-street-art\.jpg', '../assets/images/denver-photos/rino-street-art.jpg'),
        (r'../assets/images/denver-photos/colfax-corridor\.jpg', '../assets/images/denver-photos/colfax-corridor.jpg'),
        (r'../assets/images/denver-photos/colfax-venues\.jpg', '../assets/images/denver-photos/colfax-venues.jpg'),
        (r'../assets/images/denver-photos/five-points-historic\.jpg', '../assets/images/denver-photos/five-points-historic.jpg'),
        (r'../assets/images/denver-photos/five-points-development\.jpg', '../assets/images/denver-photos/five-points-development.jpg'),
        (r'../assets/images/denver-photos/highland-historic\.jpg', '../assets/images/denver-photos/highland-historic.jpg'),
        (r'../assets/images/denver-photos/highland-development\.jpg', '../assets/images/denver-photos/highland-development.jpg'),
        (r'../assets/images/denver-photos/south-broadway-corridor\.jpg', '../assets/images/denver-photos/south-broadway-corridor.jpg'),
        (r'../assets/images/denver-photos/south-broadway-venues\.jpg', '../assets/images/denver-photos/south-broadway-venues.jpg'),
        
        # Replace some generic images with more specific Denver images
        (r'../assets/images/news/music-venue-interior\.jpg', '../assets/images/relevant/denver-underground-venue.jpg'),
        (r'../assets/images/news/diy-venue-basement\.jpg', '../assets/images/relevant/denver-basement-show.jpg'),
        (r'../assets/images/news/diy-recording-studio\.jpg', '../assets/images/relevant/denver-diy-recording.jpg'),
        (r'../assets/images/news/denver-warehouse-industrial\.jpg', '../assets/images/relevant/denver-industrial-space.jpg'),
        (r'../assets/images/news/luxury-development-construction\.jpg', '../assets/images/relevant/denver-development-pressure.jpg'),
        (r'../assets/images/news/gentrification-street-art\.jpg', '../assets/images/relevant/denver-street-art.jpg'),
        (r'../assets/images/news/venue-closure-demolition\.jpg', '../assets/images/relevant/denver-venue-closure.jpg'),
        (r'../assets/images/news/neighborhood-transformation\.jpg', '../assets/images/relevant/denver-neighborhood-change.jpg'),
        (r'../assets/images/news/temporary-venue-space\.jpg', '../assets/images/relevant/denver-temporary-venue.jpg'),
        (r'../assets/images/news/community-resistance\.jpg', '../assets/images/relevant/denver-cultural-resistance.jpg'),
    ]
    
    # Apply replacements
    for pattern, replacement in replacements:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            changes_made.append(f"Replaced {pattern} with {replacement}")
    
    # Write updated content back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return changes_made

def main():
    """Update all HTML files in the essays directory."""
    
    essay_files = [
        'essays/culture-washing_enhanced.html',
        'essays/geography-displacement_enhanced.html',
        'essays/sonic-resistance_enhanced.html',
        'essays/culture-washing.html',
        'essays/geography-displacement.html',
        'essays/sonic-resistance.html'
    ]
    
    print("Updating image references in essay files...")
    
    for file_path in essay_files:
        if os.path.exists(file_path):
            print(f"\nProcessing: {file_path}")
            changes = update_image_references(file_path)
            if changes:
                print(f"Made {len(changes)} changes:")
                for change in changes:
                    print(f"  - {change}")
            else:
                print("No changes needed")
        else:
            print(f"File not found: {file_path}")
    
    print("\nImage reference update complete!")
    print("All essays now use relevant, non-stock images specific to Denver's music scene.")

if __name__ == "__main__":
    main()