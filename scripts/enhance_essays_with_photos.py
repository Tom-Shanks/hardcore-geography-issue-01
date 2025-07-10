#!/usr/bin/env python3
"""
Comprehensive essay photo enhancement script.
Adds context-appropriate photos to all essays using curated image database.
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict, Tuple
from curated_photo_database import CURATED_IMAGES, SPECIFIC_IMAGES, get_image_for_entity, get_images_for_entity

class EssayPhotoEnhancer:
    def __init__(self):
        self.used_images = set()  # Track used images to avoid repetition
        
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract venues, locations, and topics from text."""
        entities = {
            "venues": [],
            "locations": [],
            "topics": []
        }
        
        # Extract venue names with better pattern matching
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
        
        # Extract topics with better context
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

    def get_best_image(self, entity_type: str, entity_name: str) -> str:
        """Get the best available image for an entity, avoiding repetition."""
        images = get_images_for_entity(entity_type, entity_name)
        
        for img_url in images:
            if img_url not in self.used_images:
                self.used_images.add(img_url)
                return img_url
        
        # If all images are used, return the first one
        return images[0] if images else ""

    def add_inline_photos(self, content: str, entities: Dict[str, List[str]]) -> str:
        """Add inline photos to content based on extracted entities."""
        lines = content.split('\n')
        enhanced_lines = []
        added_images = set()  # Track images added to this content
        
        for i, line in enumerate(lines):
            enhanced_lines.append(line)
            
            # Add photos after paragraphs that mention entities
            if line.strip() and not line.startswith('#'):
                # Check for venues
                for venue in entities["venues"]:
                    if venue in line and f"<img" not in line:
                        img_url = self.get_best_image("venues", venue)
                        if img_url and img_url not in added_images:
                            img_tag = f'<img src="{img_url}" alt="{venue} photo" class="inline-photo">'
                            enhanced_lines.append(img_tag)
                            added_images.add(img_url)
                
                # Check for locations
                for location in entities["locations"]:
                    if location in line and f"<img" not in line:
                        img_url = self.get_best_image("locations", location)
                        if img_url and img_url not in added_images:
                            img_tag = f'<img src="{img_url}" alt="{location} photo" class="inline-photo">'
                            enhanced_lines.append(img_tag)
                            added_images.add(img_url)
                
                # Check for topics
                for topic in entities["topics"]:
                    if topic in line and f"<img" not in line:
                        img_url = self.get_best_image("topics", topic)
                        if img_url and img_url not in added_images:
                            img_tag = f'<img src="{img_url}" alt="{topic} photo" class="inline-photo">'
                            enhanced_lines.append(img_tag)
                            added_images.add(img_url)
        
        return '\n'.join(enhanced_lines)

    def create_photo_galleries(self, entities: Dict[str, List[str]]) -> str:
        """Create comprehensive photo galleries for extracted entities."""
        galleries = []
        
        # Create venue galleries
        for venue in entities["venues"]:
            images = get_images_for_entity("venues", venue)
            if images:
                gallery_html = f"""
<div class="photo-gallery venue-gallery">
<h3>{venue} - Photo Gallery</h3>
<div class="gallery-grid">"""
                
                for img_url in images:
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
            images = get_images_for_entity("locations", location)
            if images:
                gallery_html = f"""
<div class="photo-gallery area-gallery">
<h3>{location} - Photo Gallery</h3>
<div class="gallery-grid">"""
                
                for img_url in images:
                    gallery_html += f"""
<div class="gallery-item">
<img src="{img_url}" alt="{location} photo" class="gallery-photo">
</div>"""
                
                gallery_html += """
</div>
</div>"""
                galleries.append(gallery_html)
        
        # Create topic galleries
        for topic in entities["topics"]:
            images = get_images_for_entity("topics", topic)
            if images:
                gallery_html = f"""
<div class="photo-gallery topic-gallery">
<h3>{topic.title()} - Photo Gallery</h3>
<div class="gallery-grid">"""
                
                for img_url in images:
                    gallery_html += f"""
<div class="gallery-item">
<img src="{img_url}" alt="{topic} photo" class="gallery-photo">
</div>"""
                
                gallery_html += """
</div>
</div>"""
                galleries.append(gallery_html)
        
        return '\n'.join(galleries)

    def enhance_markdown_essay(self, file_path: str) -> str:
        """Enhance a markdown essay with context-appropriate photos."""
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

    def enhance_html_essay(self, file_path: str) -> str:
        """Enhance an HTML essay with context-appropriate photos."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract entities from content
        entities = self.extract_entities(content)
        
        # Add inline photos to HTML content
        enhanced_content = self.add_inline_photos(content, entities)
        
        # Create photo galleries
        galleries = self.create_photo_galleries(entities)
        
        # Add galleries before the closing body tag
        if galleries:
            # Find the closing body tag
            body_end = enhanced_content.find('</body>')
            if body_end != -1:
                gallery_section = f"\n\n<!-- Photo Galleries -->\n<div class=\"photo-galleries\">\n{galleries}\n</div>\n"
                enhanced_content = enhanced_content[:body_end] + gallery_section + enhanced_content[body_end:]
        
        return enhanced_content

    def process_all_essays(self):
        """Process all essay files."""
        content_dir = Path("../content")
        essays_dir = Path("../essays")
        
        print("Starting essay photo enhancement...")
        
        # Process markdown files
        for md_file in content_dir.glob("essay-*.md"):
            print(f"Processing {md_file}...")
            enhanced_content = self.enhance_markdown_essay(str(md_file))
            
            # Save enhanced markdown
            output_path = md_file.with_name(md_file.stem + '_enhanced.md')
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(enhanced_content)
            
            print(f"Enhanced {md_file} -> {output_path}")
        
        # Process HTML files
        for html_file in essays_dir.glob("*_enhanced.html"):
            print(f"Processing {html_file}...")
            enhanced_content = self.enhance_html_essay(str(html_file))
            
            # Save enhanced HTML
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(enhanced_content)
            
            print(f"Enhanced {html_file}")
        
        print("Essay photo enhancement completed!")

def main():
    enhancer = EssayPhotoEnhancer()
    enhancer.process_all_essays()

if __name__ == "__main__":
    main()