#!/usr/bin/env python3
"""
Hardcore Geography - Essay Photo Enhancement Script
Web scraping script to gather photos of Denver venues and areas discussed in essays
"""

import requests
import os
import json
import time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import re
from pathlib import Path

class DenverVenuePhotoScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.venue_photos = {}
        self.area_photos = {}
        
    def search_venue_photos(self, venue_name, address=None):
        """Search for photos of specific venues"""
        search_terms = [venue_name]
        if address:
            search_terms.append(f"{venue_name} {address}")
        
        photos = []
        
        # Search Google Images (simulated - would need API key for real implementation)
        for term in search_terms:
            try:
                # This is a placeholder - in real implementation you'd use Google Custom Search API
                print(f"Searching for photos of: {term}")
                # Simulate finding photos
                photos.extend(self._simulate_photo_search(term))
            except Exception as e:
                print(f"Error searching for {term}: {e}")
        
        return photos
    
    def _simulate_photo_search(self, search_term):
        """Simulate finding photos for venues"""
        # This would normally use Google Custom Search API or similar
        # For now, we'll create placeholder photo URLs based on venue names
        
        venue_photos = {
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
            ]
        }
        
        # Find matching venue
        for venue, photos in venue_photos.items():
            if venue.lower() in search_term.lower():
                return photos
        
        # Default venue photo
        return ["https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=600&fit=crop"]
    
    def search_area_photos(self, area_name):
        """Search for photos of Denver areas/neighborhoods"""
        area_photos = {
            "RiNo": [
                "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop"
            ],
            "South Broadway": [
                "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop"
            ],
            "Colfax": [
                "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop"
            ],
            "Downtown Denver": [
                "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop"
            ],
            "Central Denver": [
                "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop"
            ]
        }
        
        for area, photos in area_photos.items():
            if area.lower() in area_name.lower():
                return photos
        
        return ["https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop"]
    
    def download_photo(self, url, filename):
        """Download a photo from URL"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Create assets directory if it doesn't exist
            os.makedirs("assets/photos", exist_ok=True)
            
            filepath = f"assets/photos/{filename}"
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"Downloaded: {filename}")
            return filepath
        except Exception as e:
            print(f"Error downloading {url}: {e}")
            return None

class EssayEnhancer:
    def __init__(self):
        self.scraper = DenverVenuePhotoScraper()
        self.venue_data = self._load_venue_data()
        
    def _load_venue_data(self):
        """Load venue data from CSV"""
        venues = [
            {"name": "Rhinoceropolis", "address": "5070 N Washington St", "neighborhood": "Central Denver"},
            {"name": "Larimer Lounge", "address": "2721 Larimer Street", "neighborhood": "RiNo"},
            {"name": "Hi-Dive", "address": "7 S Broadway", "neighborhood": "South Broadway"},
            {"name": "The Bluebird Theater", "address": "3317 E Colfax Ave", "neighborhood": "Colfax"},
            {"name": "The Ogden Theatre", "address": "935 E Colfax Ave", "neighborhood": "Colfax"},
            {"name": "The Lion's Lair", "address": "2022 E Colfax Ave", "neighborhood": "Colfax"},
            {"name": "The Meadowlark", "address": "2701 Larimer Street", "neighborhood": "RiNo"},
            {"name": "Lost Lake Lounge", "address": "3602 E Colfax Ave", "neighborhood": "Colfax"}
        ]
        return venues
    
    def enhance_essay_with_photos(self, essay_file, output_file):
        """Enhance an essay with relevant photos"""
        print(f"Enhancing essay: {essay_file}")
        
        # Read the essay
        with open(essay_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find venues mentioned in the essay
        mentioned_venues = self._find_mentioned_venues(content)
        print(f"Found venues: {mentioned_venues}")
        
        # Get photos for mentioned venues
        venue_photos = {}
        for venue in mentioned_venues:
            photos = self.scraper.search_venue_photos(venue['name'], venue.get('address'))
            if photos:
                venue_photos[venue['name']] = photos[:2]  # Limit to 2 photos per venue
        
        # Find areas mentioned
        mentioned_areas = self._find_mentioned_areas(content)
        print(f"Found areas: {mentioned_areas}")
        
        # Get photos for mentioned areas
        area_photos = {}
        for area in mentioned_areas:
            photos = self.scraper.search_area_photos(area)
            if photos:
                area_photos[area] = photos[:1]  # Limit to 1 photo per area
        
        # Enhance the content with photos
        enhanced_content = self._insert_photos_into_essay(content, venue_photos, area_photos)
        
        # Write enhanced essay
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(enhanced_content)
        
        print(f"Enhanced essay saved to: {output_file}")
        
        return venue_photos, area_photos
    
    def _find_mentioned_venues(self, content):
        """Find venues mentioned in the essay content"""
        mentioned = []
        for venue in self.venue_data:
            if venue['name'].lower() in content.lower():
                mentioned.append(venue)
        return mentioned
    
    def _find_mentioned_areas(self, content):
        """Find areas/neighborhoods mentioned in the essay content"""
        areas = ["RiNo", "South Broadway", "Colfax", "Downtown Denver", "Central Denver", "Highland"]
        mentioned = []
        for area in areas:
            if area.lower() in content.lower():
                mentioned.append(area)
        return mentioned
    
    def _insert_photos_into_essay(self, content, venue_photos, area_photos):
        """Insert photo galleries into the essay content"""
        enhanced_content = content
        
        # Insert venue photo galleries
        for venue_name, photos in venue_photos.items():
            gallery_html = self._create_photo_gallery(venue_name, photos, "venue")
            # Insert after first mention of venue
            venue_pattern = re.compile(f"({re.escape(venue_name)})", re.IGNORECASE)
            enhanced_content = venue_pattern.sub(f"\\1{self._create_inline_photo(photos[0])}", enhanced_content, count=1)
        
        # Insert area photo galleries
        for area_name, photos in area_photos.items():
            gallery_html = self._create_photo_gallery(area_name, photos, "area")
            # Insert after first mention of area
            area_pattern = re.compile(f"({re.escape(area_name)})", re.IGNORECASE)
            enhanced_content = area_pattern.sub(f"\\1{self._create_inline_photo(photos[0])}", enhanced_content, count=1)
        
        # Add photo galleries at the end
        if venue_photos or area_photos:
            enhanced_content += "\n\n<!-- Photo Galleries -->\n"
            enhanced_content += '<div class="photo-galleries">\n'
            
            for venue_name, photos in venue_photos.items():
                enhanced_content += self._create_photo_gallery(venue_name, photos, "venue")
            
            for area_name, photos in area_photos.items():
                enhanced_content += self._create_photo_gallery(area_name, photos, "area")
            
            enhanced_content += '</div>\n'
        
        return enhanced_content
    
    def _create_inline_photo(self, photo_url):
        """Create inline photo element"""
        return f'<img src="{photo_url}" alt="Venue photo" class="inline-photo" style="width: 200px; height: 150px; object-fit: cover; margin: 10px; border-radius: 4px; float: right;">'
    
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
    enhancer = EssayEnhancer()
    
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
                venue_photos, area_photos = enhancer.enhance_essay_with_photos(essay, output_file)
                print(f"Enhanced {essay} with {len(venue_photos)} venue photos and {len(area_photos)} area photos")
            except Exception as e:
                print(f"Error enhancing {essay}: {e}")
        else:
            print(f"Essay file not found: {essay}")
    
    print("Essay enhancement complete!")

if __name__ == "__main__":
    main()