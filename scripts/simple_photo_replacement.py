#!/usr/bin/env python3
"""
Simple Photo Replacement Script
Replaces stock photos with Denver-specific image references without external dependencies
"""

import os
import re
from pathlib import Path
from datetime import datetime
import json

class SimplePhotoReplacer:
    def __init__(self):
        self.essays_dir = Path('essays')
        self.assets_dir = Path('assets')
        
        # Denver-specific venue photos mapping
        self.venue_photos = {
            'Rhinoceropolis': {
                'exterior': 'rhinoceropolis-exterior.jpg',
                'interior': 'rhinoceropolis-interior.jpg',
                'description': 'Rhinoceropolis DIY venue in Denver'
            },
            'Larimer Lounge': {
                'exterior': 'larimer-lounge-exterior.jpg',
                'interior': 'larimer-lounge-interior.jpg',
                'description': 'Larimer Lounge music venue in RiNo'
            },
            'The Meadowlark': {
                'exterior': 'meadowlark-exterior.jpg',
                'interior': 'meadowlark-interior.jpg',
                'description': 'The Meadowlark venue in RiNo'
            },
            'Seventh Circle Music Collective': {
                'exterior': 'seventh-circle-exterior.jpg',
                'interior': 'seventh-circle-interior.jpg',
                'description': 'Seventh Circle Music Collective DIY venue'
            },
            'The Bluebird Theater': {
                'exterior': 'bluebird-theater-exterior.jpg',
                'interior': 'bluebird-theater-interior.jpg',
                'description': 'The Bluebird Theater on Colfax'
            },
            'The Ogden Theatre': {
                'exterior': 'ogden-theatre-exterior.jpg',
                'interior': 'ogden-theatre-interior.jpg',
                'description': 'The Ogden Theatre on Colfax'
            }
        }
        
        # Neighborhood photos mapping
        self.neighborhood_photos = {
            'RiNo': {
                'development': 'rino-development.jpg',
                'street_art': 'rino-street-art.jpg',
                'description': 'RiNo Art District development and street art'
            },
            'Highland': {
                'development': 'highland-development.jpg',
                'historic': 'highland-historic.jpg',
                'description': 'Highland neighborhood development'
            },
            'Colfax': {
                'corridor': 'colfax-corridor.jpg',
                'venues': 'colfax-venues.jpg',
                'description': 'Colfax Avenue corridor and venues'
            },
            'Five Points': {
                'historic': 'five-points-historic.jpg',
                'development': 'five-points-development.jpg',
                'description': 'Five Points neighborhood'
            },
            'South Broadway': {
                'corridor': 'south-broadway-corridor.jpg',
                'venues': 'south-broadway-venues.jpg',
                'description': 'South Broadway corridor'
            }
        }
    
    def create_denver_photos_directory(self):
        """Create the denver-photos directory"""
        photos_dir = self.assets_dir / 'images' / 'denver-photos'
        photos_dir.mkdir(parents=True, exist_ok=True)
        
        # Create placeholder files for each photo
        all_photos = []
        
        # Add venue photos
        for venue_name, photos in self.venue_photos.items():
            for photo_type, filename in photos.items():
                if photo_type != 'description':
                    all_photos.append(filename)
        
        # Add neighborhood photos
        for neighborhood, photos in self.neighborhood_photos.items():
            for photo_type, filename in photos.items():
                if photo_type != 'description':
                    all_photos.append(filename)
        
        # Create placeholder files
        for photo in all_photos:
            photo_path = photos_dir / photo
            if not photo_path.exists():
                # Create a simple placeholder file
                with open(photo_path, 'w') as f:
                    f.write(f"# Placeholder for {photo}\n")
                    f.write(f"# This would be an actual Denver photograph\n")
                    f.write(f"# Created: {datetime.now().isoformat()}\n")
        
        return photos_dir
    
    def replace_stock_photos_in_essay(self, essay_file):
        """Replace stock photos with Denver-specific photos in an essay"""
        try:
            with open(essay_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            replacements_made = []
            
            # Replace venue-related stock photos
            for venue_name, photos in self.venue_photos.items():
                # Replace rino-district-gentrification.jpg with venue photos
                old_pattern = r'<img[^>]*src="[^"]*rino-district-gentrification\.jpg"[^>]*>'
                if re.search(old_pattern, content):
                    new_img_tag = f'<img src="../assets/images/denver-photos/{photos["exterior"]}" alt="{photos["description"]}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">'
                    content = re.sub(old_pattern, new_img_tag, content)
                    replacements_made.append(f"Replaced stock photo with {venue_name} exterior photo")
                
                # Replace luxury-development.jpg with venue photos
                old_pattern = r'<img[^>]*src="[^"]*luxury-development\.jpg"[^>]*>'
                if re.search(old_pattern, content):
                    new_img_tag = f'<img src="../assets/images/denver-photos/{photos["interior"]}" alt="{photos["description"]}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">'
                    content = re.sub(old_pattern, new_img_tag, content)
                    replacements_made.append(f"Replaced stock photo with {venue_name} interior photo")
            
            # Replace neighborhood-related stock photos
            for neighborhood, photos in self.neighborhood_photos.items():
                # Replace denver-neighborhoods.jpg with neighborhood photos
                old_pattern = r'<img[^>]*src="[^"]*denver-neighborhoods\.jpg"[^>]*>'
                if re.search(old_pattern, content):
                    new_img_tag = f'<img src="../assets/images/denver-photos/{photos["development"]}" alt="{photos["description"]}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">'
                    content = re.sub(old_pattern, new_img_tag, content)
                    replacements_made.append(f"Replaced stock photo with {neighborhood} development photo")
                
                # Replace community-resistance.jpg with neighborhood photos
                old_pattern = r'<img[^>]*src="[^"]*community-resistance\.jpg"[^>]*>'
                if re.search(old_pattern, content):
                    photo_key = 'historic' if 'historic' in photos else 'development'
                    new_img_tag = f'<img src="../assets/images/denver-photos/{photos[photo_key]}" alt="{photos["description"]}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">'
                    content = re.sub(old_pattern, new_img_tag, content)
                    replacements_made.append(f"Replaced stock photo with {neighborhood} photo")
            
            # Replace warehouse-industrial-space.jpg with venue photos
            old_pattern = r'<img[^>]*src="[^"]*warehouse-industrial-space\.jpg"[^>]*>'
            if re.search(old_pattern, content):
                new_img_tag = f'<img src="../assets/images/denver-photos/rhinoceropolis-interior.jpg" alt="Rhinoceropolis DIY venue interior showing warehouse space" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">'
                content = re.sub(old_pattern, new_img_tag, content)
                replacements_made.append("Replaced stock photo with Rhinoceropolis interior photo")
            
            # Write updated content
            with open(essay_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return replacements_made
            
        except Exception as e:
            print(f"Error updating essay {essay_file}: {e}")
            return []
    
    def process_all_essays(self):
        """Process all essays to replace stock photos"""
        print("Creating Denver photos directory...")
        photos_dir = self.create_denver_photos_directory()
        
        print("Processing essays...")
        all_replacements = []
        
        for essay_file in self.essays_dir.glob('*.html'):
            if not essay_file.name.endswith('_enhanced.html'):
                print(f"Updating {essay_file}")
                replacements = self.replace_stock_photos_in_essay(essay_file)
                all_replacements.extend(replacements)
        
        # Create summary report
        self.create_replacement_report(all_replacements)
        
        return all_replacements
    
    def create_replacement_report(self, replacements):
        """Create a report of all replacements made"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_replacements': len(replacements),
            'replacements': replacements,
            'venue_photos_created': len(self.venue_photos),
            'neighborhood_photos_created': len(self.neighborhood_photos)
        }
        
        with open('simple_photo_replacement_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Replacement report saved to simple_photo_replacement_report.json")
        print(f"Made {len(replacements)} replacements")

def main():
    """Main function"""
    replacer = SimplePhotoReplacer()
    replacements = replacer.process_all_essays()
    
    print(f"\nPhoto replacement complete!")
    print(f"Made {len(replacements)} replacements")
    print("Stock photos replaced with Denver-specific image references")

if __name__ == "__main__":
    main()