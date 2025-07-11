#!/usr/bin/env python3
"""
Script to download newsworthy images for the Hardcore Geography essays.
Downloads images from public sources and saves them to assets/images/news/
"""

import os
import requests
from urllib.parse import urlparse
import time

def download_image(url, filename, folder="assets/images/news"):
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
    """Download relevant images for each essay topic"""
    
    # Images for Culture-Washing Essay
    culture_washing_images = [
        {
            "url": "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800&h=600&fit=crop",
            "filename": "denver-warehouse-industrial.jpg",
            "description": "Industrial warehouse space in Denver showing the type of buildings that housed DIY venues"
        },
        {
            "url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&h=600&fit=crop",
            "filename": "luxury-development-construction.jpg",
            "description": "Luxury development construction showing the transformation of industrial areas"
        },
        {
            "url": "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800&h=600&fit=crop",
            "filename": "music-venue-interior.jpg",
            "description": "Interior of a music venue showing the cultural spaces being displaced"
        },
        {
            "url": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=600&fit=crop",
            "filename": "gentrification-street-art.jpg",
            "description": "Street art and cultural markers being appropriated in gentrifying neighborhoods"
        }
    ]
    
    # Images for Geography of Displacement Essay
    displacement_images = [
        {
            "url": "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800&h=600&fit=crop",
            "filename": "denver-industrial-zoning.jpg",
            "description": "Industrial zoning areas in Denver showing the spaces where DIY venues emerged"
        },
        {
            "url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&h=600&fit=crop",
            "filename": "venue-closure-demolition.jpg",
            "description": "Demolition of venues showing the physical displacement of cultural spaces"
        },
        {
            "url": "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800&h=600&fit=crop",
            "filename": "underground-music-scene.jpg",
            "description": "Underground music scene showing the communities being displaced"
        },
        {
            "url": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=600&fit=crop",
            "filename": "neighborhood-transformation.jpg",
            "description": "Neighborhood transformation showing the before and after of gentrification"
        }
    ]
    
    # Images for Sonic Resistance Essay
    resistance_images = [
        {
            "url": "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800&h=600&fit=crop",
            "filename": "diy-venue-basement.jpg",
            "description": "DIY venue in basement showing house show culture"
        },
        {
            "url": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=600&fit=crop",
            "filename": "community-resistance.jpg",
            "description": "Community resistance and activism against displacement"
        },
        {
            "url": "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800&h=600&fit=crop",
            "filename": "temporary-venue-space.jpg",
            "description": "Temporary venue space showing adaptive use of marginal spaces"
        },
        {
            "url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&h=600&fit=crop",
            "filename": "diy-recording-studio.jpg",
            "description": "DIY recording studio showing technological resistance"
        }
    ]
    
    # Download all images
    all_images = culture_washing_images + displacement_images + resistance_images
    
    print("Downloading newsworthy images for Hardcore Geography essays...")
    
    for img in all_images:
        download_image(img["url"], img["filename"])
        time.sleep(1)  # Be respectful to servers
    
    print("\nImage download complete!")
    print("Images saved to assets/images/news/")

if __name__ == "__main__":
    main()