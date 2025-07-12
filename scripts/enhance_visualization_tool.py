#!/usr/bin/env python3
"""
Enhance Visualization Tool with Comprehensive Venue Data
Scrapes additional venue information and enriches the interactive map with more data
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
# import pandas as pd  # Not used in this script

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VisualizationEnhancer:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Additional data sources
        self.data_sources = {
            'yelp': {
                'base_url': 'https://www.yelp.com',
                'search_url': 'https://www.yelp.com/search',
                'selectors': ['.photo-box img', '.photo-slider img', '.business-photo']
            },
            'google_maps': {
                'base_url': 'https://www.google.com/maps',
                'search_url': 'https://www.google.com/maps/search',
                'selectors': ['.section-result-image', '.section-result-thumbnail']
            },
            'instagram': {
                'base_url': 'https://www.instagram.com',
                'search_url': 'https://www.instagram.com/explore/tags',
                'selectors': ['img._aagt', '.photo-box img']
            }
        }
        
        # Venue information sources
        self.venue_info_sources = {
            'westword': {
                'base_url': 'https://www.westword.com',
                'search_url': 'https://www.westword.com/search/',
                'article_selectors': ['.article-title', '.headline', '.article-content']
            },
            'denver_post': {
                'base_url': 'https://www.denverpost.com',
                'search_url': 'https://www.denverpost.com/search/',
                'article_selectors': ['.article-title', '.headline', '.article-content']
            },
            'denverite': {
                'base_url': 'https://denverite.com',
                'search_url': 'https://denverite.com/search/',
                'article_selectors': ['.article-title', '.headline', '.article-content']
            }
        }
        
        # Load existing venue data
        self.venues_data = self.load_venue_data()
        
    def load_venue_data(self):
        """Load existing venue data"""
        venues = {}
        try:
            with open('data/venues_zoning.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    venues[row['name']] = row
        except FileNotFoundError:
            logger.warning("Venues CSV not found")
        return venues
    
    def scrape_venue_information(self, venue_name):
        """Scrape additional information about a venue"""
        venue_info = {
            'name': venue_name,
            'description': '',
            'history': '',
            'events': [],
            'photos': [],
            'reviews': [],
            'social_media': {},
            'last_updated': datetime.now().isoformat()
        }
        
        # Search for venue information across sources
        for source_name, source_config in self.venue_info_sources.items():
            try:
                search_url = f"{source_config['search_url']}{venue_name.replace(' ', '+')}"
                response = self.session.get(search_url, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract articles about the venue
                for selector in source_config['article_selectors']:
                    articles = soup.select(selector)
                    
                    for article in articles:
                        title = article.get_text(strip=True)
                        if venue_name.lower() in title.lower():
                            # Extract article content
                            content = article.find_parent('article')
                            if content:
                                venue_info['description'] += f" {content.get_text(strip=True)[:500]}"
                
                time.sleep(random.uniform(1, 2))
                
            except Exception as e:
                logger.warning(f"Error scraping {venue_name} from {source_name}: {e}")
                continue
        
        return venue_info
    
    def scrape_venue_photos(self, venue_name):
        """Scrape photos of venues from various sources"""
        photos = []
        
        # Search for venue photos
        search_terms = [
            f"{venue_name} Denver",
            f"{venue_name} venue",
            f"{venue_name} music",
            f"{venue_name} concert"
        ]
        
        for source_name, source_config in self.data_sources.items():
            for term in search_terms:
                try:
                    search_url = f"{source_config['search_url']}/{term.replace(' ', '+')}"
                    response = self.session.get(search_url, timeout=10)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    for selector in source_config['selectors']:
                        img_elements = soup.select(selector)
                        
                        for img in img_elements:
                            img_url = img.get('src') or img.get('data-src')
                            if img_url and isinstance(img_url, str):
                                img_url = urljoin(source_config['base_url'], img_url)
                                
                                alt_text = img.get('alt', '')
                                if venue_name.lower() in alt_text.lower() if isinstance(alt_text, str) else False:
                                    photos.append({
                                        'url': img_url,
                                        'alt_text': alt_text,
                                        'source': source_name,
                                        'venue_name': venue_name
                                    })
                    
                    time.sleep(random.uniform(1, 2))
                    
                except Exception as e:
                    logger.warning(f"Error searching photos for {venue_name} in {source_name}: {e}")
                    continue
        
        return photos
    
    def enrich_venue_data(self):
        """Enrich venue data with additional information"""
        enriched_venues = []
        
        for venue_name, venue_data in self.venues_data.items():
            logger.info(f"Enriching data for {venue_name}")
            
            # Scrape additional information
            venue_info = self.scrape_venue_information(venue_name)
            venue_photos = self.scrape_venue_photos(venue_name)
            
            # Combine with existing data
            enriched_venue = {
                **venue_data,
                'enriched_info': venue_info,
                'photos': venue_photos,
                'last_enriched': datetime.now().isoformat()
            }
            
            enriched_venues.append(enriched_venue)
        
        return enriched_venues
    
    def create_enhanced_venue_csv(self, enriched_venues):
        """Create enhanced CSV with all venue data"""
        enhanced_data = []
        
        for venue in enriched_venues:
            enhanced_row = {
                'name': venue['name'],
                'address': venue.get('address', ''),
                'active_years': venue.get('active_years', ''),
                'closure_reason': venue.get('closure_reason', ''),
                'lat': venue.get('lat', ''),
                'lng': venue.get('lng', ''),
                'notes': venue.get('notes', ''),
                'documentation_status': venue.get('documentation_status', ''),
                'zoning_type': venue.get('zoning_type', ''),
                'zoning_description': venue.get('zoning_description', ''),
                'zoning_year': venue.get('zoning_year', ''),
                'land_use_change': venue.get('land_use_change', ''),
                'neighborhood': venue.get('neighborhood', ''),
                'zoning_density': venue.get('zoning_density', ''),
                'neighborhood_density': venue.get('neighborhood_density', ''),
                'displacement_pattern': venue.get('displacement_pattern', ''),
                'description': venue.get('enriched_info', {}).get('description', ''),
                'history': venue.get('enriched_info', {}).get('history', ''),
                'photo_count': len(venue.get('photos', [])),
                'last_enriched': venue.get('last_enriched', '')
            }
            enhanced_data.append(enhanced_row)
        
        # Save enhanced CSV
        with open('data/enhanced_venues.csv', 'w', newline='', encoding='utf-8') as f:
            if enhanced_data:
                writer = csv.DictWriter(f, fieldnames=enhanced_data[0].keys())
                writer.writeheader()
                writer.writerows(enhanced_data)
        
        return enhanced_data
    
    def create_venue_photos_json(self, enriched_venues):
        """Create JSON file with venue photos"""
        photos_data = {}
        
        for venue in enriched_venues:
            venue_name = venue['name']
            photos_data[venue_name] = {
                'venue_info': venue.get('enriched_info', {}),
                'photos': venue.get('photos', []),
                'total_photos': len(venue.get('photos', []))
            }
        
        with open('data/venue_photos.json', 'w') as f:
            json.dump(photos_data, f, indent=2)
        
        return photos_data
    
    def update_visualization_tool(self, enriched_venues):
        """Update the interactive map with enriched data"""
        map_file = 'assets/interactive-map.html'
        
        try:
            with open(map_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Create enhanced venue data for JavaScript
            venue_data_js = []
            for venue in enriched_venues:
                venue_js = {
                    'name': venue['name'],
                    'lat': float(venue.get('lat', 0)) if venue.get('lat') else 0,
                    'lng': float(venue.get('lng', 0)) if venue.get('lng') else 0,
                    'active_years': venue.get('active_years', ''),
                    'closure_reason': venue.get('closure_reason', ''),
                    'neighborhood': venue.get('neighborhood', ''),
                    'zoning_type': venue.get('zoning_type', ''),
                    'description': venue.get('enriched_info', {}).get('description', ''),
                    'photo_count': len(venue.get('photos', [])),
                    'photos': venue.get('photos', [])
                }
                venue_data_js.append(venue_js)
            
            # Find the venue data section and replace it
            venue_data_pattern = r'const venueData = \[.*?\];'
            venue_data_replacement = f'const venueData = {json.dumps(venue_data_js, indent=2)};'
            
            if re.search(venue_data_pattern, content, re.DOTALL):
                content = re.sub(venue_data_pattern, venue_data_replacement, content, flags=re.DOTALL)
            else:
                # Add venue data if it doesn't exist
                script_pattern = r'(<script[^>]*>)'
                content = re.sub(script_pattern, f'\\1\n{venue_data_replacement}\n', content)
            
            # Add enhanced features
            enhanced_features = """
            // Enhanced venue information display
            function showEnhancedVenueInfo(venue) {
                let info = `
                    <div class="venue-info-enhanced">
                        <h3>${venue.name}</h3>
                        <p><strong>Active Years:</strong> ${venue.active_years}</p>
                        <p><strong>Neighborhood:</strong> ${venue.neighborhood}</p>
                        <p><strong>Zoning:</strong> ${venue.zoning_type}</p>
                        <p><strong>Status:</strong> ${venue.closure_reason || 'Active'}</p>
                        ${venue.description ? `<p><strong>Description:</strong> ${venue.description.substring(0, 200)}...</p>` : ''}
                        ${venue.photo_count > 0 ? `<p><strong>Photos Available:</strong> ${venue.photo_count}</p>` : ''}
                    </div>
                `;
                return info;
            }
            
            // Enhanced filtering
            function filterVenuesByNeighborhood(neighborhood) {
                return venueData.filter(venue => venue.neighborhood === neighborhood);
            }
            
            function filterVenuesByZoning(zoningType) {
                return venueData.filter(venue => venue.zoning_type === zoningType);
            }
            """
            
            # Add enhanced features to the map
            if 'function showEnhancedVenueInfo' not in content:
                content = content.replace('</script>', f'{enhanced_features}\n</script>')
            
            # Write updated content
            with open(map_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Updated visualization tool with enriched data")
            
        except Exception as e:
            logger.error(f"Error updating visualization tool: {e}")
    
    def create_enhancement_report(self, enriched_venues):
        """Create a report of the enhancement process"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_venues_processed': len(enriched_venues),
            'venues_with_photos': len([v for v in enriched_venues if v.get('photos')]),
            'total_photos_found': sum(len(v.get('photos', [])) for v in enriched_venues),
            'venues_with_descriptions': len([v for v in enriched_venues if v.get('enriched_info', {}).get('description')]),
            'enhancement_summary': {
                'active_venues': len([v for v in enriched_venues if 'Active' in v.get('closure_reason', '')]),
                'closed_venues': len([v for v in enriched_venues if 'Closure' in v.get('closure_reason', '')]),
                'venues_by_neighborhood': {},
                'venues_by_zoning': {}
            }
        }
        
        # Calculate statistics
        for venue in enriched_venues:
            neighborhood = venue.get('neighborhood', 'Unknown')
            zoning = venue.get('zoning_type', 'Unknown')
            
            report['enhancement_summary']['venues_by_neighborhood'][neighborhood] = \
                report['enhancement_summary']['venues_by_neighborhood'].get(neighborhood, 0) + 1
            
            report['enhancement_summary']['venues_by_zoning'][zoning] = \
                report['enhancement_summary']['venues_by_zoning'].get(zoning, 0) + 1
        
        with open('visualization_enhancement_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def process_enhancement(self):
        """Main enhancement process"""
        logger.info("Starting visualization enhancement process...")
        
        # Enrich venue data
        enriched_venues = self.enrich_venue_data()
        
        # Create enhanced CSV
        enhanced_data = self.create_enhanced_venue_csv(enriched_venues)
        
        # Create photos JSON
        photos_data = self.create_venue_photos_json(enriched_venues)
        
        # Update visualization tool
        self.update_visualization_tool(enriched_venues)
        
        # Create enhancement report
        report = self.create_enhancement_report(enriched_venues)
        
        logger.info("Visualization enhancement complete!")
        logger.info(f"Processed {len(enriched_venues)} venues")
        logger.info(f"Found {report['total_photos_found']} photos")
        logger.info(f"Enhanced {report['venues_with_descriptions']} venues with descriptions")
        
        return enriched_venues, report

def main():
    """Main function"""
    enhancer = VisualizationEnhancer()
    enriched_venues, report = enhancer.process_enhancement()
    
    print(f"\nVisualization enhancement complete!")
    print(f"Enhanced {len(enriched_venues)} venues")
    print(f"Found {report['total_photos_found']} photos")
    print(f"Updated interactive map with enriched data")
    print("Check visualization_enhancement_report.json for detailed results")

if __name__ == "__main__":
    main()