#!/usr/bin/env python3
"""
Script to create proper placeholder images for the Hardcore Geography project.
This will replace the corrupted/placeholder images with actual visible images.
"""

import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_placeholder_image(filename, title, description, width=800, height=600):
    """Create a placeholder image with text content."""
    
    # Create a new image with a gradient background
    img = Image.new('RGB', (width, height), color='#2c3e50')
    draw = ImageDraw.Draw(img)
    
    # Create gradient effect
    for y in range(height):
        r = int(44 + (y / height) * 20)  # Dark blue to lighter blue
        g = int(62 + (y / height) * 30)
        b = int(80 + (y / height) * 40)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Add accent color bar
    draw.rectangle([0, 0, width, 80], fill='#ff6b35')
    
    # Try to use a default font, fall back to basic if not available
    try:
        # Try to use a larger font for the title
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        desc_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    except:
        try:
            title_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 48)
            desc_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
        except:
            # Fall back to default font
            title_font = ImageFont.load_default()
            desc_font = ImageFont.load_default()
    
    # Draw title
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, 20), title, fill='white', font=title_font)
    
    # Draw description (wrapped)
    margin = 40
    max_width = width - 2 * margin
    wrapped_text = textwrap.fill(description, width=50)
    
    # Calculate text position
    desc_bbox = draw.textbbox((0, 0), wrapped_text, font=desc_font)
    desc_height = desc_bbox[3] - desc_bbox[1]
    desc_y = 120 + (height - 200 - desc_height) // 2
    
    # Draw description
    draw.text((margin, desc_y), wrapped_text, fill='white', font=desc_font)
    
    # Add a decorative element
    draw.rectangle([width-100, height-100, width-20, height-20], 
                   outline='#ff6b35', width=3)
    draw.ellipse([width-90, height-90, width-30, height-30], 
                 fill='#ff6b35')
    
    # Save the image
    img.save(filename, 'JPEG', quality=85)
    print(f"Created: {filename}")

def main():
    """Create placeholder images for all the missing/corrupted images."""
    
    # Ensure the images directory exists
    os.makedirs('assets/images', exist_ok=True)
    
    # Define the images to create
    images = [
        {
            'filename': 'assets/images/rhinoceropolis-venue.jpg',
            'title': 'Rhinoceropolis',
            'description': 'DIY music venue in Denver that operated from 2005-2017. A cornerstone of the underground music scene before its closure due to gentrification.'
        },
        {
            'filename': 'assets/images/house-show-basement.jpg',
            'title': 'House Show Basement',
            'description': 'Residential basement space converted for DIY music performances. These temporary venues represent the adaptive nature of underground culture.'
        },
        {
            'filename': 'assets/images/diy-recording-studio.jpg',
            'title': 'DIY Recording Studio',
            'description': 'Bedroom recording setup with basic equipment. The democratization of recording technology has enabled independent music production.'
        },
        {
            'filename': 'assets/images/underground-music-scene.jpg',
            'title': 'Underground Music Scene',
            'description': 'Intimate performance space showing the raw, authentic nature of DIY music culture. These spaces prioritize community over commercial success.'
        },
        {
            'filename': 'assets/images/warehouse-industrial-space.jpg',
            'title': 'Warehouse Industrial Space',
            'description': 'Industrial warehouse converted for cultural use. These marginal spaces provide affordable venues for experimental music and art.'
        },
        {
            'filename': 'assets/images/luxury-development.jpg',
            'title': 'Luxury Development',
            'description': 'High-end residential development replacing cultural spaces. This represents the displacement pressure facing DIY venues and communities.'
        },
        {
            'filename': 'assets/images/rino-district-gentrification.jpg',
            'title': 'RiNo District Gentrification',
            'description': 'The River North (RiNo) district showing rapid development and gentrification. Former industrial areas are being transformed into luxury housing.'
        },
        {
            'filename': 'assets/images/denver-neighborhoods.jpg',
            'title': 'Denver Neighborhoods',
            'description': 'Aerial view of Denver neighborhoods showing the geographic patterns of development and displacement affecting cultural communities.'
        },
        {
            'filename': 'assets/images/community-resistance.jpg',
            'title': 'Community Resistance',
            'description': 'Community organizing and activism against displacement. These efforts demonstrate resistance to the erasure of cultural spaces.'
        }
    ]
    
    # Create each image
    for image_info in images:
        create_placeholder_image(
            image_info['filename'],
            image_info['title'],
            image_info['description']
        )
    
    print("\nAll placeholder images have been created!")
    print("These images will now display properly in your HTML files.")
    print("\nYou can now view your website and the images should appear correctly.")

if __name__ == "__main__":
    main()