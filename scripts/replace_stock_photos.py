#!/usr/bin/env python3
"""
Replace Stock Photos with Actual Denver Photographs
Scrapes local news sources and venue websites for authentic images of Denver venues and locations
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import re
import time
import random
from urllib.parse import urljoin, urlparse
import logging
from pathlib import Path
import csv
from datetime import datetime
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DenverPhotoReplacer:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Denver-specific news sources
        self.news_sources = {
            'westword': {
                'base_url': 'https://www.westword.com',
                'search_url': 'https://www.westword.com/search/',
                'image_selectors': ['img.article-image', 'img.photo', '.gallery-image img', '.article-content img']
            },
            'denver_post': {
                'base_url': 'https://www.denverpost.com',
                'search_url': 'https://www.denverpost.com/search/',
                'image_selectors': ['img.article-image', 'img.photo', '.gallery-image img', '.article-content img']
            },
            'denverite': {
                'base_url': 'https://denverite.com',
                'search_url': 'https://denverite.com/search/',
                'image_selectors': ['img.article-image', 'img.photo', '.gallery-image img', '.article-content img']
            }
        }
        
        # Venue-specific search terms
        self.venue_searches = {
            'Rhinoceropolis': [
                'Rhinoceropolis Denver', 'Rhino Denver venue', 'DIY venue Denver',
                'underground music Denver', 'warehouse venue Denver'
            ],
            'Larimer Lounge': [
                'Larimer Lounge Denver', 'Larimer Lounge venue', 'RiNo music venue',
                'Larimer Street venue Denver'
            ],
            'The Meadowlark': [
                'Meadowlark Denver', 'Meadowlark venue', 'RiNo venue Denver',
                'Larimer Street music venue'
            ],
            'Seventh Circle Music Collective': [
                'Seventh Circle Music Collective', 'Seventh Circle Denver',
                'DIY music collective Denver', 'all-ages venue Denver'
            ],
            'The Bluebird Theater': [
                'Bluebird Theater Denver', 'Bluebird Theater Colfax',
                'historic venue Denver', 'Colfax Avenue venue'
            ],
            'The Ogden Theatre': [
                'Ogden Theatre Denver', 'Ogden Theatre Colfax',
                'historic venue Denver', 'Colfax Avenue venue'
            ]
        }
        
        # Neighborhood-specific search terms
        self.neighborhood_searches = {
            'RiNo': [
                'RiNo Denver', 'River North Art District', 'RiNo development',
                'RiNo gentrification', 'RiNo art district Denver'
            ],
            'Highland': [
                'Highland Denver', 'LoHi Denver', 'Highland neighborhood',
                'Highland Bridge Denver', 'Highland development'
            ],
            'Colfax': [
                'Colfax Avenue Denver', 'Colfax corridor', 'Colfax venues',
                'East Colfax Denver', 'Colfax development'
            ],
            'Five Points': [
                'Five Points Denver', 'Five Points neighborhood',
                'Five Points development', 'Five Points gentrification'
            ],
            'South Broadway': [
                'South Broadway Denver', 'Broadway corridor',
                'South Broadway development', 'Broadway venues'
            ]
        }
        
        # Load venue data
        self.venues_data = self.load_venue_data()
        
    def load_venue_data(self):
        """Load venue data from CSV"""
        venues = {}
        try:
            with open('data/venues_zoning.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    venues[row['name']] = row
        except FileNotFoundError:
            logger.warning("Venues CSV not found, using default data")
        return venues
    
    def search_venue_images(self, venue_name, max_results=5):
        """Search for images of specific venues"""
        images = []
        
        if venue_name in self.venue_searches:
            search_terms = self.venue_searches[venue_name]
        else:
            search_terms = [f"{venue_name} Denver", f"{venue_name} venue"]
        
        for source_name, source_config in self.news_sources.items():
            for term in search_terms:
                try:
                    search_url = f"{source_config['search_url']}{term.replace(' ', '+')}"
                    response = self.session.get(search_url, timeout=10)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    for selector in source_config['image_selectors']:
                        img_elements = soup.select(selector)
                        
                        for img in img_elements:
                            img_url = img.get('src') or img.get('data-src')
                            if img_url and isinstance(img_url, str):
                                img_url = urljoin(source_config['base_url'], img_url)
                                
                                # Get context
                                alt_text = img.get('alt', '')
                                caption = img.get('title', '') or alt_text
                                
                                # Check if image is relevant
                                if self.is_relevant_image(alt_text, caption, venue_name):
                                    images.append({
                                        'url': img_url,
                                        'alt_text': alt_text,
                                        'caption': caption,
                                        'venue_name': venue_name,
                                        'source': source_name,
                                        'search_term': term
                                    })
                                    
                                    if len(images) >= max_results:
                                        break
                    
                    time.sleep(random.uniform(1, 2))
                    
                except Exception as e:
                    logger.warning(f"Error searching for {venue_name} in {source_name}: {e}")
                    continue
        
        return images
    
    def search_neighborhood_images(self, neighborhood, max_results=5):
        """Search for images of specific neighborhoods"""
        images = []
        
        if neighborhood in self.neighborhood_searches:
            search_terms = self.neighborhood_searches[neighborhood]
        else:
            search_terms = [f"{neighborhood} Denver", f"{neighborhood} neighborhood"]
        
        for source_name, source_config in self.news_sources.items():
            for term in search_terms:
                try:
                    search_url = f"{source_config['search_url']}{term.replace(' ', '+')}"
                    response = self.session.get(search_url, timeout=10)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    for selector in source_config['image_selectors']:
                        img_elements = soup.select(selector)
                        
                        for img in img_elements:
                            img_url = img.get('src') or img.get('data-src')
                            if img_url and isinstance(img_url, str):
                                img_url = urljoin(source_config['base_url'], img_url)
                                
                                alt_text = img.get('alt', '')
                                caption = img.get('title', '') or alt_text
                                
                                if self.is_relevant_image(alt_text, caption, neighborhood):
                                    images.append({
                                        'url': img_url,
                                        'alt_text': alt_text,
                                        'caption': caption,
                                        'neighborhood': neighborhood,
                                        'source': source_name,
                                        'search_term': term
                                    })
                                    
                                    if len(images) >= max_results:
                                        break
                    
                    time.sleep(random.uniform(1, 2))
                    
                except Exception as e:
                    logger.warning(f"Error searching for {neighborhood} in {source_name}: {e}")
                    continue
        
        return images
    
    def is_relevant_image(self, alt_text, caption, search_term):
        """Check if image is relevant to the search term"""
        text = f"{alt_text} {caption}".lower()
        search_lower = search_term.lower()
        
        # Check for venue/neighborhood name
        if search_term.lower() in text:
            return True
        
        # Check for related terms
        related_terms = {
            'venue': ['venue', 'club', 'theater', 'theatre', 'music', 'concert'],
            'neighborhood': ['neighborhood', 'district', 'area', 'development', 'gentrification'],
            'RiNo': ['rino', 'river north', 'art district', 'creative district'],
            'Highland': ['highland', 'lohi', 'lower highland'],
            'Colfax': ['colfax', 'avenue', 'corridor'],
            'Five Points': ['five points', 'welton', 'historic'],
            'South Broadway': ['broadway', 'south broadway', 'corridor']
        }
        
        for category, terms in related_terms.items():
            if any(term in text for term in terms):
                return True
        
        return False
    
    def download_image(self, image_data, output_dir):
        """Download and save image"""
        try:
            response = self.session.get(image_data['url'], timeout=15)
            response.raise_for_status()
            
            # Check if it's actually an image
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                return None
            
            # Generate filename
            if 'venue_name' in image_data:
                filename = f"{image_data['venue_name'].replace(' ', '-').lower()}-{self.generate_hash(image_data['url'])}.jpg"
            else:
                filename = f"{image_data['neighborhood'].replace(' ', '-').lower()}-{self.generate_hash(image_data['url'])}.jpg"
            
            filepath = os.path.join(output_dir, filename)
            
            # Save image
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            return {
                'filepath': filepath,
                'filename': filename,
                'alt_text': image_data['alt_text'],
                'caption': image_data['caption'],
                'source': image_data['source'],
                'original_url': image_data['url']
            }
            
        except Exception as e:
            logger.warning(f"Error downloading image {image_data['url']}: {e}")
            return None
    
    def generate_hash(self, url):
        """Generate a short hash for filename"""
        return hashlib.md5(url.encode()).hexdigest()[:8]
    
    def update_essay_images(self, essay_file, new_images):
        """Update essay HTML with new images"""
        try:
            with open(essay_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace stock photos with actual Denver photos
            replacements = []
            
            for image_data in new_images:
                if 'venue_name' in image_data:
                    # Replace venue-related stock photos
                    old_patterns = [
                        r'<img[^>]*src="[^"]*rino-district-gentrification\.jpg"[^>]*>',
                        r'<img[^>]*src="[^"]*luxury-development\.jpg"[^>]*>',
                        r'<img[^>]*src="[^"]*warehouse-industrial-space\.jpg"[^>]*>'
                    ]
                    
                    for pattern in old_patterns:
                        if re.search(pattern, content):
                            new_img_tag = f'<img src="../assets/images/denver-photos/{image_data["filename"]}" alt="{image_data["alt_text"]}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">'
                            content = re.sub(pattern, new_img_tag, content)
                            replacements.append(f"Replaced stock photo with {image_data['venue_name']} photo")
                            break
                
                elif 'neighborhood' in image_data:
                    # Replace neighborhood-related stock photos
                    old_patterns = [
                        r'<img[^>]*src="[^"]*denver-neighborhoods\.jpg"[^>]*>',
                        r'<img[^>]*src="[^"]*community-resistance\.jpg"[^>]*>'
                    ]
                    
                    for pattern in old_patterns:
                        if re.search(pattern, content):
                            new_img_tag = f'<img src="../assets/images/denver-photos/{image_data["filename"]}" alt="{image_data["alt_text"]}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">'
                            content = re.sub(pattern, new_img_tag, content)
                            replacements.append(f"Replaced stock photo with {image_data['neighborhood']} photo")
                            break
            
            # Write updated content
            with open(essay_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return replacements
            
        except Exception as e:
            logger.error(f"Error updating essay {essay_file}: {e}")
            return []
    
    def process_all_essays(self):
        """Process all essays to replace stock photos"""
        essays_dir = Path('essays')
        output_dir = Path('assets/images/denver-photos')
        output_dir.mkdir(exist_ok=True)
        
        all_replacements = []
        
        # Get all venue names from data
        venue_names = list(self.venues_data.keys())
        
        # Get all neighborhood names
        neighborhoods = ['RiNo', 'Highland', 'Colfax', 'Five Points', 'South Broadway']
        
        # Search for venue images
        venue_images = []
        for venue_name in venue_names:
            logger.info(f"Searching for images of {venue_name}")
            images = self.search_venue_images(venue_name)
            venue_images.extend(images)
        
        # Search for neighborhood images
        neighborhood_images = []
        for neighborhood in neighborhoods:
            logger.info(f"Searching for images of {neighborhood}")
            images = self.search_neighborhood_images(neighborhood)
            neighborhood_images.extend(images)
        
        # Download images
        downloaded_images = []
        for image_data in venue_images + neighborhood_images:
            downloaded = self.download_image(image_data, output_dir)
            if downloaded:
                downloaded_images.append(downloaded)
        
        # Update essays
        for essay_file in essays_dir.glob('*.html'):
            if not essay_file.name.endswith('_enhanced.html'):
                logger.info(f"Updating {essay_file}")
                replacements = self.update_essay_images(essay_file, downloaded_images)
                all_replacements.extend(replacements)
        
        # Create summary report
        self.create_replacement_report(all_replacements, downloaded_images)
        
        return downloaded_images
    
    def create_replacement_report(self, replacements, downloaded_images):
        """Create a report of all replacements made"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_images_downloaded': len(downloaded_images),
            'total_replacements': len(replacements),
            'downloaded_images': downloaded_images,
            'replacements': replacements
        }
        
        with open('photo_replacement_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Replacement report saved to photo_replacement_report.json")
        logger.info(f"Downloaded {len(downloaded_images)} images")
        logger.info(f"Made {len(replacements)} replacements")

def main():
    """Main function"""
    replacer = DenverPhotoReplacer()
    downloaded_images = replacer.process_all_essays()
    
    print(f"\nPhoto replacement complete!")
    print(f"Downloaded {len(downloaded_images)} authentic Denver photographs")
    print("Check photo_replacement_report.json for detailed results")

if __name__ == "__main__":
    main()