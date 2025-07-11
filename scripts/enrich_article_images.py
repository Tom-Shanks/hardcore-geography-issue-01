#!/usr/bin/env python3
"""
Article Image Enrichment Script
Scrapes relevant images from newspaper websites and updates article images with proper captions
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
import markdown
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
import io

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImageEnricher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Newspaper sources to scrape
        self.newspaper_sources = {
            'denver_post': {
                'base_url': 'https://www.denverpost.com',
                'search_url': 'https://www.denverpost.com/search/',
                'image_selectors': ['img.article-image', 'img.photo', '.gallery-image img']
            },
            'westword': {
                'base_url': 'https://www.westword.com',
                'search_url': 'https://www.westword.com/search/',
                'image_selectors': ['img.article-image', 'img.photo', '.gallery-image img']
            },
            'denver_westword': {
                'base_url': 'https://www.westword.com',
                'search_url': 'https://www.westword.com/search/',
                'image_selectors': ['img.article-image', 'img.photo', '.gallery-image img']
            }
        }
        
        # Topic keywords for each essay
        self.essay_topics = {
            'essay-01-geography-displacement': [
                'Rhinoceropolis', 'Denver music venues', 'gentrification Denver',
                'warehouse venues', 'DIY music scene', 'RiNo development',
                'Five Points Denver', 'Central Denver venues', 'venue displacement'
            ],
            'essay-02-culture-washing': [
                'RiNo art district', 'culture washing', 'creative district Denver',
                'Highland Denver', 'LoHi development', 'art district gentrification',
                'creative economy Denver', 'artist displacement', 'cultural appropriation'
            ],
            'essay-03-sonic-resistance': [
                'DIY music scene', 'underground music', 'house shows Denver',
                'Seventh Circle Music Collective', 'warehouse shows', 'temporary venues',
                'music resistance', 'underground venues', 'community music'
            ]
        }
        
        # Image caption templates
        self.caption_templates = {
            'venue': {
                'template': 'Photo of {venue_name} in {neighborhood}, showing {description}',
                'variations': [
                    'Exterior view of {venue_name} in {neighborhood}',
                    'Interior of {venue_name} during a performance',
                    '{venue_name} venue space in {neighborhood}',
                    'The {venue_name} building in {neighborhood}'
                ]
            },
            'neighborhood': {
                'template': 'View of {neighborhood} neighborhood showing {description}',
                'variations': [
                    'Aerial view of {neighborhood} development',
                    'Street scene in {neighborhood}',
                    'Industrial buildings in {neighborhood}',
                    'Development in {neighborhood} area'
                ]
            },
            'topic': {
                'template': 'Image showing {topic} in Denver',
                'variations': [
                    'Photograph of {topic}',
                    'Scene depicting {topic}',
                    'Visual representation of {topic}',
                    'Image related to {topic}'
                ]
            }
        }

    def search_newspaper_images(self, keywords, source='denver_post', max_results=10):
        """Search newspaper websites for relevant images based on keywords"""
        images = []
        
        for keyword in keywords:
            try:
                # Search the newspaper website
                search_url = f"{self.newspaper_sources[source]['search_url']}{keyword.replace(' ', '+')}"
                response = self.session.get(search_url, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find images using selectors
                for selector in self.newspaper_sources[source]['image_selectors']:
                    img_elements = soup.select(selector)
                    
                    for img in img_elements:
                        img_url = img.get('src') or img.get('data-src')
                        if img_url and isinstance(img_url, str):
                            img_url = urljoin(self.newspaper_sources[source]['base_url'], img_url)
                            
                            # Get alt text and caption
                            alt_text = img.get('alt', '')
                            caption = img.get('title', '') or alt_text
                            
                            # Get article context
                            article = img.find_parent('article') or img.find_parent('.article')
                            article_title = ''
                            if article:
                                title_elem = article.find('h1') or article.find('h2') or article.find('.headline')
                                if title_elem:
                                    article_title = title_elem.get_text(strip=True)
                            
                            images.append({
                                'url': img_url,
                                'alt_text': alt_text,
                                'caption': caption,
                                'article_title': article_title,
                                'keyword': keyword,
                                'source': source
                            })
                            
                            if len(images) >= max_results:
                                break
                
                time.sleep(random.uniform(1, 3))  # Be respectful
                
            except Exception as e:
                logger.warning(f"Error searching for keyword '{keyword}': {e}")
                continue
        
        return images

    def download_and_process_image(self, image_data, output_dir):
        """Download and process an image"""
        try:
            response = self.session.get(image_data['url'], timeout=15)
            response.raise_for_status()
            
            # Check if it's actually an image
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                return None
            
            # Process image
            if PIL_AVAILABLE:
                img = Image.open(io.BytesIO(response.content))
                
                # Generate filename
                filename = self.generate_filename(image_data)
                filepath = os.path.join(output_dir, filename)
                
                # Save image
                img.save(filepath, 'JPEG', quality=85)
            else:
                # Fallback: save raw image data
                filename = self.generate_filename(image_data)
                filepath = os.path.join(output_dir, filename)
                with open(filepath, 'wb') as f:
                    f.write(response.content)
            
            return {
                'filepath': filepath,
                'filename': filename,
                'alt_text': image_data['alt_text'],
                'caption': image_data['caption'],
                'article_title': image_data['article_title'],
                'keyword': image_data['keyword'],
                'source': image_data['source']
            }
            
        except Exception as e:
            logger.warning(f"Error downloading image {image_data['url']}: {e}")
            return None

    def generate_filename(self, image_data):
        """Generate a descriptive filename for the image"""
        keyword = image_data['keyword'].replace(' ', '_').lower()
        source = image_data['source']
        
        # Extract a meaningful name from alt text or caption
        text = image_data['alt_text'] or image_data['caption'] or keyword
        words = re.findall(r'\b\w+\b', text.lower())[:3]
        name_part = '_'.join(words) if words else keyword
        
        return f"{source}_{name_part}_{int(time.time())}.jpg"

    def generate_caption(self, image_data, essay_topic):
        """Generate a contextual caption for the image"""
        if 'venue' in image_data['keyword'].lower():
            # Extract venue name from keyword or alt text
            venue_name = self.extract_venue_name(image_data)
            neighborhood = self.extract_neighborhood(image_data)
            template = random.choice(self.caption_templates['venue']['variations'])
            return template.format(venue_name=venue_name, neighborhood=neighborhood, description=image_data['alt_text'])
        
        elif any(area in image_data['keyword'].lower() for area in ['rino', 'highland', 'five points', 'colfax']):
            neighborhood = self.extract_neighborhood(image_data)
            template = random.choice(self.caption_templates['neighborhood']['variations'])
            return template.format(neighborhood=neighborhood, description=image_data['alt_text'])
        
        else:
            topic = image_data['keyword']
            template = random.choice(self.caption_templates['topic']['variations'])
            return template.format(topic=topic)

    def extract_venue_name(self, image_data):
        """Extract venue name from image data"""
        text = image_data['alt_text'] or image_data['caption'] or image_data['keyword']
        
        # Common venue names
        venue_names = [
            'Rhinoceropolis', 'Larimer Lounge', 'The Meadowlark', 'Monkey Mania',
            'Streets of London', 'Kingdom of Doom', 'The Church', 'The Skylark Lounge',
            '3 Kings Tavern', 'Seventh Circle Music Collective'
        ]
        
        for venue in venue_names:
            if venue.lower() in text.lower():
                return venue
        
        return 'music venue'

    def extract_neighborhood(self, image_data):
        """Extract neighborhood name from image data"""
        text = image_data['alt_text'] or image_data['caption'] or image_data['keyword']
        
        neighborhoods = [
            'RiNo', 'Highland', 'LoHi', 'Five Points', 'Central Denver',
            'Colfax', 'Park Hill', 'Lakewood', 'South Broadway'
        ]
        
        for neighborhood in neighborhoods:
            if neighborhood.lower() in text.lower():
                return neighborhood
        
        return 'Denver'

    def update_essay_images(self, essay_file, enriched_images):
        """Update essay markdown with enriched images"""
        with open(essay_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all image tags
        img_pattern = r'<img[^>]+src="[^"]+"[^>]*>'
        img_matches = re.findall(img_pattern, content)
        
        if not img_matches:
            logger.warning(f"No image tags found in {essay_file}")
            return content
        
        # Replace images with enriched versions
        updated_content = content
        image_index = 0
        
        for match in img_matches:
            if image_index < len(enriched_images):
                new_img_tag = self.create_enriched_img_tag(enriched_images[image_index])
                updated_content = updated_content.replace(match, new_img_tag, 1)
                image_index += 1
        
        return updated_content

    def create_enriched_img_tag(self, image_data):
        """Create an enriched image tag with proper caption"""
        caption = image_data.get('caption', '')
        if not caption:
            caption = image_data.get('alt_text', '')
        
        return f'<img src="{image_data["filepath"]}" alt="{caption}" class="inline-photo" title="{caption}">'

    def enrich_essay_images(self, essay_file, essay_topic):
        """Main function to enrich images for a specific essay"""
        logger.info(f"Enriching images for {essay_file}")
        
        # Get topics for this essay
        topics = self.essay_topics.get(essay_topic, [])
        
        # Create output directory
        output_dir = Path('assets/images/enriched')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Search for images
        all_images = []
        for source in self.newspaper_sources:
            images = self.search_newspaper_images(topics, source, max_results=5)
            all_images.extend(images)
        
        # Download and process images
        enriched_images = []
        for image_data in all_images[:10]:  # Limit to 10 images per essay
            processed_image = self.download_and_process_image(image_data, output_dir)
            if processed_image:
                processed_image['caption'] = self.generate_caption(image_data, essay_topic)
                enriched_images.append(processed_image)
        
        # Update essay content
        updated_content = self.update_essay_images(essay_file, enriched_images)
        
        # Write updated content
        with open(essay_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        logger.info(f"Enriched {len(enriched_images)} images for {essay_file}")
        return enriched_images

def main():
    """Main function to enrich all essay images"""
    enricher = ImageEnricher()
    
    # Essay files to process
    essays = [
        ('content/essay-01-geography-displacement_enhanced.md', 'essay-01-geography-displacement'),
        ('content/essay-02-culture-washing_enhanced.md', 'essay-02-culture-washing'),
        ('content/essay-03-sonic-resistance_enhanced.md', 'essay-03-sonic-resistance')
    ]
    
    for essay_file, essay_topic in essays:
        if os.path.exists(essay_file):
            try:
                enriched_images = enricher.enrich_essay_images(essay_file, essay_topic)
                print(f"Successfully enriched {len(enriched_images)} images for {essay_file}")
            except Exception as e:
                logger.error(f"Error processing {essay_file}: {e}")
        else:
            logger.warning(f"Essay file not found: {essay_file}")

if __name__ == "__main__":
    main()