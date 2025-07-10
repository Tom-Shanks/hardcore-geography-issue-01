#!/usr/bin/env python3
"""
Hardcore Geography - Simple Essay Photo Enhancement
Enhance essays with relevant photos without external dependencies
"""

import os
import re
from pathlib import Path

class SimpleEssayEnhancer:
    def __init__(self):
        self.venue_photos = {
            "Rhinoceropolis": [
                "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800&h=600&fit=crop"
            ],
            "Larimer Lounge": [
                "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=600&fit=crop"
            ],
            "Hi-Dive": [
                "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800&h=600&fit=crop"
            ],
            "The Bluebird Theater": [
                "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=600&fit=crop"
            ],
            "The Ogden Theatre": [
                "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800&h=600&fit=crop"
            ],
            "The Lion's Lair": [
                "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=600&fit=crop"
            ],
            "The Meadowlark": [
                "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800&h=600&fit=crop"
            ],
            "Lost Lake Lounge": [
                "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=600&fit=crop"
            ]
        }
        
        self.area_photos = {
            "RiNo": [
                "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop"
            ],
            "South Broadway": [
                "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop"
            ],
            "Colfax": [
                "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop"
            ],
            "Downtown": [
                "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop"
            ],
            "Central Denver": [
                "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop"
            ]
        }
    
    def enhance_essay(self, essay_file, output_file):
        """Enhance an essay with relevant photos"""
        print(f"Enhancing essay: {essay_file}")
        
        # Read the essay
        with open(essay_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find venues mentioned in the essay
        mentioned_venues = self._find_mentioned_venues(content)
        print(f"Found venues: {[v['name'] for v in mentioned_venues]}")
        
        # Find areas mentioned
        mentioned_areas = self._find_mentioned_areas(content)
        print(f"Found areas: {mentioned_areas}")
        
        # Enhance the content with photos
        enhanced_content = self._insert_photos_into_essay(content, mentioned_venues, mentioned_areas)
        
        # Write enhanced essay
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(enhanced_content)
        
        print(f"Enhanced essay saved to: {output_file}")
    
    def _find_mentioned_venues(self, content):
        """Find venues mentioned in the essay content"""
        mentioned = []
        for venue_name in self.venue_photos.keys():
            if venue_name.lower() in content.lower():
                mentioned.append({"name": venue_name})
        return mentioned
    
    def _find_mentioned_areas(self, content):
        """Find areas/neighborhoods mentioned in the essay content"""
        mentioned = []
        for area in self.area_photos.keys():
            if area.lower() in content.lower():
                mentioned.append(area)
        return mentioned
    
    def _insert_photos_into_essay(self, content, mentioned_venues, mentioned_areas):
        """Insert photo galleries into the essay content"""
        enhanced_content = content
        
        # Add CSS for photo galleries
        css_style = """
        <style>
        .photo-gallery {
            margin: 2rem 0;
            padding: 1rem;
            background: var(--light-gray);
            border-radius: 4px;
        }
        .gallery-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }
        .gallery-item {
            text-align: center;
        }
        .gallery-photo {
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-radius: 4px;
            border: 1px solid var(--accent-gray);
        }
        .inline-photo {
            width: 200px;
            height: 150px;
            object-fit: cover;
            margin: 10px;
            border-radius: 4px;
            float: right;
            border: 1px solid var(--accent-gray);
        }
        @media (max-width: 768px) {
            .gallery-grid {
                grid-template-columns: 1fr;
            }
            .inline-photo {
                float: none;
                width: 100%;
                height: 200px;
                margin: 10px 0;
            }
        }
        </style>
        """
        
        # Insert CSS into head
        enhanced_content = enhanced_content.replace('</head>', f'{css_style}\n</head>')
        
        # Insert venue photo galleries
        for venue in mentioned_venues:
            venue_name = venue['name']
            photos = self.venue_photos.get(venue_name, [])
            if photos:
                # Insert inline photo after first mention
                venue_pattern = re.compile(f"({re.escape(venue_name)})", re.IGNORECASE)
                inline_photo = self._create_inline_photo(photos[0], venue_name)
                enhanced_content = venue_pattern.sub(f"\\1{inline_photo}", enhanced_content, count=1)
        
        # Insert area photo galleries
        for area in mentioned_areas:
            photos = self.area_photos.get(area, [])
            if photos:
                # Insert inline photo after first mention
                area_pattern = re.compile(f"({re.escape(area)})", re.IGNORECASE)
                inline_photo = self._create_inline_photo(photos[0], area)
                enhanced_content = area_pattern.sub(f"\\1{inline_photo}", enhanced_content, count=1)
        
        # Add photo galleries at the end
        if mentioned_venues or mentioned_areas:
            enhanced_content += "\n\n<!-- Photo Galleries -->\n"
            enhanced_content += '<div class="photo-galleries">\n'
            
            for venue in mentioned_venues:
                venue_name = venue['name']
                photos = self.venue_photos.get(venue_name, [])
                if photos:
                    enhanced_content += self._create_photo_gallery(venue_name, photos, "venue")
            
            for area in mentioned_areas:
                photos = self.area_photos.get(area, [])
                if photos:
                    enhanced_content += self._create_photo_gallery(area, photos, "area")
            
            enhanced_content += '</div>\n'
        
        return enhanced_content
    
    def _create_inline_photo(self, photo_url, name):
        """Create inline photo element"""
        return f'<img src="{photo_url}" alt="{name} photo" class="inline-photo">'
    
    def _create_photo_gallery(self, name, photos, type_):
        """Create a photo gallery HTML"""
        gallery_html = f'<div class="photo-gallery {type_}-gallery">\n'
        gallery_html += f'<h3>{name} - Photo Gallery</h3>\n'
        gallery_html += '<div class="gallery-grid">\n'
        
        for i, photo_url in enumerate(photos):
            gallery_html += f'<div class="gallery-item">\n'
            gallery_html += f'<img src="{photo_url}" alt="{name} photo {i+1}" class="gallery-photo">\n'
            gallery_html += '</div>\n'
        
        gallery_html += '</div>\n'
        gallery_html += '</div>\n'
        
        return gallery_html

def main():
    """Main function to enhance all essays with photos"""
    enhancer = SimpleEssayEnhancer()
    
    # List of essays to enhance
    essays = [
        "essays/geography-displacement.html",
        "essays/culture-washing.html", 
        "essays/sonic-resistance.html"
    ]
    
    for essay in essays:
        if os.path.exists(essay):
            output_file = essay.replace('.html', '_enhanced.html')
            try:
                enhancer.enhance_essay(essay, output_file)
                print(f"Enhanced {essay}")
            except Exception as e:
                print(f"Error enhancing {essay}: {e}")
        else:
            print(f"Essay file not found: {essay}")
    
    print("Essay enhancement complete!")

if __name__ == "__main__":
    main()