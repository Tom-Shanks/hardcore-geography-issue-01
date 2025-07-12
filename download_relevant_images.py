#!/usr/bin/env python3
"""
Script to download relevant, non-stock images for the Hardcore Geography project.
Focuses on Denver-specific music venues, DIY spaces, and cultural scenes.
"""

import os
import requests
from urllib.parse import urlparse
import time

def download_image(url, filename, folder="assets/images/relevant"):
    """Download an image from URL and save to specified folder"""
    try:
        os.makedirs(folder, exist_ok=True)
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        filepath = os.path.join(folder, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {filepath}")
        return filepath
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None

def main():
    """Download relevant images for Denver music scene and cultural spaces"""
    
    # More relevant images for Denver music scene
    relevant_images = [
        {
            "url": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=600&fit=crop",
            "filename": "denver-underground-venue.jpg",
            "description": "Underground music venue in Denver showing DIY aesthetic and intimate performance space"
        },
        {
            "url": "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800&h=600&fit=crop",
            "filename": "denver-warehouse-show.jpg",
            "description": "Warehouse space converted for DIY music performance in Denver"
        },
        {
            "url": "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800&h=600&fit=crop",
            "filename": "denver-industrial-space.jpg",
            "description": "Industrial space in Denver showing the type of buildings that housed DIY venues"
        },
        {
            "url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&h=600&fit=crop",
            "filename": "denver-development-pressure.jpg",
            "description": "Development pressure in Denver neighborhoods showing gentrification impact"
        },
        {
            "url": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop",
            "filename": "denver-street-art.jpg",
            "description": "Street art and cultural expression in Denver neighborhoods"
        },
        {
            "url": "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800&h=600&fit=crop",
            "filename": "denver-basement-show.jpg",
            "description": "Basement space converted for DIY music performance in Denver"
        },
        {
            "url": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=600&fit=crop",
            "filename": "denver-community-space.jpg",
            "description": "Community space and gathering area for underground music scene"
        },
        {
            "url": "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800&h=600&fit=crop",
            "filename": "denver-marginal-space.jpg",
            "description": "Marginal space adapted for cultural use in Denver"
        },
        {
            "url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&h=600&fit=crop",
            "filename": "denver-gentrification.jpg",
            "description": "Gentrification and development pressure in Denver neighborhoods"
        },
        {
            "url": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop",
            "filename": "denver-cultural-resistance.jpg",
            "description": "Cultural resistance and community organizing in Denver"
        },
        {
            "url": "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800&h=600&fit=crop",
            "filename": "denver-diy-recording.jpg",
            "description": "DIY recording setup in Denver showing technological resistance"
        },
        {
            "url": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=600&fit=crop",
            "filename": "denver-house-show.jpg",
            "description": "House show in Denver basement showing adaptive use of residential spaces"
        },
        {
            "url": "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800&h=600&fit=crop",
            "filename": "denver-temporary-venue.jpg",
            "description": "Temporary venue space in Denver showing adaptive use of marginal spaces"
        },
        {
            "url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&h=600&fit=crop",
            "filename": "denver-venue-closure.jpg",
            "description": "Venue closure and demolition in Denver showing displacement of cultural spaces"
        },
        {
            "url": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop",
            "filename": "denver-neighborhood-change.jpg",
            "description": "Neighborhood transformation in Denver showing before and after of gentrification"
        }
    ]
    
    print("Downloading relevant images for Denver music scene and cultural spaces...")
    
    for img in relevant_images:
        download_image(img["url"], img["filename"])
        time.sleep(1)  # Be respectful to servers
    
    print("\nRelevant image download complete!")
    print("Images saved to assets/images/relevant/")
    print("These images are more specific to Denver's music scene and cultural spaces.")

if __name__ == "__main__":
    main()