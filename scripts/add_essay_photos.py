#!/usr/bin/env python3
"""
Script to add context-appropriate photos to essays using Unsplash API.
Analyzes essay content and adds relevant images for venues, locations, and topics.
"""

import os
import re
import requests
import json
from pathlib import Path
from typing import List, Dict, Tuple
import time

class EssayPhotoEnhancer:
    def __init__(self):
        self.unsplash_access_key = "YOUR_UNSPLASH_ACCESS_KEY"  # Replace with actual key
        self.base_url = "https://api.unsplash.com"
        self.headers = {
            "Authorization": f"Client-ID {self.unsplash_access_key}"
        }
        
        # Context-specific image mappings
        self.venue_images = {
            "Rhinoceropolis": [
                "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800&h=600&fit=crop"
            ],
            "Larimer Lounge": [
                "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=600&fit=crop"
            ],
            "The Meadowlark": [
                "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800&h=600&fit=crop"
            ],
            "Monkey Mania": [
                "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=600&fit=crop"
            ],
            "Streets of London": [
                "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800&h=600&fit=crop"
            ],
            "Kingdom of Doom": [
                "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=600&fit=crop"
            ],
            "The Church": [
                "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800&h=600&fit=crop"
            ],
            "The Skylark Lounge": [
                "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=600&fit=crop"
            ],
            "3 Kings Tavern": [
                "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800&h=600&fit=crop"
            ],
            "Seventh Circle Music Collective": [
                "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=600&fit=crop"
            ]
        }
        
        self.location_images = {
            "RiNo": [
                "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800&h=600&fit=crop"
            ],
            "Five Points": [
                "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop"
            ],
            "Central Denver": [
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
            "Highland": [
                "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop"
            ],
            "LoHi": [
                "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop"
            ],
            "Park Hill": [
                "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop"
            ],
            "Lakewood": [
                "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop"
            ]
        }
        
        self.topic_images = {
            "warehouse": [
                "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800&h=600&fit=crop"
            ],
            "industrial": [
                "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=600&fit=crop"
            ],
            "music venue": [
                "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800&h=600&fit=crop"
            ],
            "DIY": [
                "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=600&fit=crop"
            ],
            "gentrification": [
                "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop"
            ],
            "development": [
                "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop"
            ],
            "street art": [
                "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop"
            ],
            "creative district": [
                "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop"
            ]
        }

    def search_unsplash(self, query: str, count: int = 1) -> List[str]:
        """Search Unsplash for relevant images."""
        try:
            url = f"{self.base_url}/search/photos"
            params = {
                "query": query,
                "per_page": count,
                "orientation": "landscape"
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                data = response.json()
                return [photo["urls"]["regular"] for photo in data["results"]]
            else:
                print(f"Unsplash API error: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error searching Unsplash: {e}")
            return []

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract venues, locations, and topics from text."""
        entities = {
            "venues": [],
            "locations": [],
            "topics": []
        }
        
        # Extract venue names
        venue_patterns = [
            r"Rhinoceropolis",
            r"Larimer Lounge",
            r"The Meadowlark",
            r"Monkey Mania",
            r"Streets of London",
            r"Kingdom of Doom",
            r"The Church",
            r"The Skylark Lounge",
            r"3 Kings Tavern",
            r"Seventh Circle Music Collective"
        ]
        
        for pattern in venue_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                venue_name = match.group()
                if venue_name not in entities["venues"]:
                    entities["venues"].append(venue_name)
        
        # Extract location names
        location_patterns = [
            r"RiNo",
            r"Five Points",
            r"Central Denver",
            r"South Broadway",
            r"Colfax",
            r"Downtown",
            r"Highland",
            r"LoHi",
            r"Park Hill",
            r"Lakewood"
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                location_name = match.group()
                if location_name not in entities["locations"]:
                    entities["locations"].append(location_name)
        
        # Extract topics
        topic_patterns = [
            r"warehouse",
            r"industrial",
            r"music venue",
            r"DIY",
            r"gentrification",
            r"development",
            r"street art",
            r"creative district"
        ]
        
        for pattern in topic_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                topic_name = match.group()
                if topic_name not in entities["topics"]:
                    entities["topics"].append(topic_name)
        
        return entities

    def add_inline_photos(self, content: str, entities: Dict[str, List[str]]) -> str:
        """Add inline photos to content based on extracted entities."""
        lines = content.split('\n')
        enhanced_lines = []
        
        for i, line in enumerate(lines):
            enhanced_lines.append(line)
            
            # Add photos after paragraphs that mention entities
            if line.strip() and not line.startswith('#'):
                # Check for venues
                for venue in entities["venues"]:
                    if venue in line and f"<img" not in line:
                        if venue in self.venue_images:
                            img_url = self.venue_images[venue][0]
                            img_tag = f'<img src="{img_url}" alt="{venue} photo" class="inline-photo">'
                            enhanced_lines.append(img_tag)
                
                # Check for locations
                for location in entities["locations"]:
                    if location in line and f"<img" not in line:
                        if location in self.location_images:
                            img_url = self.location_images[location][0]
                            img_tag = f'<img src="{img_url}" alt="{location} photo" class="inline-photo">'
                            enhanced_lines.append(img_tag)
                
                # Check for topics
                for topic in entities["topics"]:
                    if topic in line and f"<img" not in line:
                        if topic in self.topic_images:
                            img_url = self.topic_images[topic][0]
                            img_tag = f'<img src="{img_url}" alt="{topic} photo" class="inline-photo">'
                            enhanced_lines.append(img_tag)
        
        return '\n'.join(enhanced_lines)

    def create_photo_galleries(self, entities: Dict[str, List[str]]) -> str:
        """Create photo galleries for extracted entities."""
        galleries = []
        
        # Create venue galleries
        for venue in entities["venues"]:
            if venue in self.venue_images:
                gallery_html = f"""
<div class="photo-gallery venue-gallery">
<h3>{venue} - Photo Gallery</h3>
<div class="gallery-grid">"""
                
                for img_url in self.venue_images[venue]:
                    gallery_html += f"""
<div class="gallery-item">
<img src="{img_url}" alt="{venue} photo" class="gallery-photo">
</div>"""
                
                gallery_html += """
</div>
</div>"""
                galleries.append(gallery_html)
        
        # Create location galleries
        for location in entities["locations"]:
            if location in self.location_images:
                gallery_html = f"""
<div class="photo-gallery area-gallery">
<h3>{location} - Photo Gallery</h3>
<div class="gallery-grid">"""
                
                for img_url in self.location_images[location]:
                    gallery_html += f"""
<div class="gallery-item">
<img src="{img_url}" alt="{location} photo" class="gallery-photo">
</div>"""
                
                gallery_html += """
</div>
</div>"""
                galleries.append(gallery_html)
        
        return '\n'.join(galleries)

    def enhance_essay(self, file_path: str) -> str:
        """Enhance an essay with context-appropriate photos."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract entities from content
        entities = self.extract_entities(content)
        
        # Add inline photos
        enhanced_content = self.add_inline_photos(content, entities)
        
        # Create photo galleries
        galleries = self.create_photo_galleries(entities)
        
        # Add galleries to the end
        if galleries:
            enhanced_content += f"\n\n<!-- Photo Galleries -->\n<div class=\"photo-galleries\">\n{galleries}\n</div>"
        
        return enhanced_content

    def process_all_essays(self):
        """Process all essay files."""
        content_dir = Path("../content")
        essays_dir = Path("../essays")
        
        # Process markdown files
        for md_file in content_dir.glob("essay-*.md"):
            print(f"Processing {md_file}...")
            enhanced_content = self.enhance_essay(str(md_file))
            
            # Save enhanced markdown
            output_path = md_file.with_suffix('_enhanced.md')
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(enhanced_content)
            
            print(f"Enhanced {md_file} -> {output_path}")
        
        # Process HTML files
        for html_file in essays_dir.glob("*_enhanced.html"):
            print(f"Processing {html_file}...")
            enhanced_content = self.enhance_essay(str(html_file))
            
            # Save enhanced HTML
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(enhanced_content)
            
            print(f"Enhanced {html_file}")

def main():
    enhancer = EssayPhotoEnhancer()
    enhancer.process_all_essays()

if __name__ == "__main__":
    main()