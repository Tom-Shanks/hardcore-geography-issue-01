#!/usr/bin/env python3
"""
Script to replace corrupted placeholder files in denver-photos directory
with proper images relevant to Denver music venues and cultural spaces.
"""

import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_venue_image(filename, venue_name, description, width=800, height=600):
    """Create a venue-specific image with relevant content."""
    
    # Create a new image with a gradient background
    img = Image.new('RGB', (width, height), color='#2c3e50')
    draw = ImageDraw.Draw(img)
    
    # Create gradient effect
    for y in range(height):
        r = int(44 + (y / height) * 20)
        g = int(62 + (y / height) * 30)
        b = int(80 + (y / height) * 40)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Add accent color bar
    draw.rectangle([0, 0, width, 80], fill='#ff6b35')
    
    # Try to use a default font
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
        desc_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    except:
        try:
            title_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 36)
            desc_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 20)
        except:
            title_font = ImageFont.load_default()
            desc_font = ImageFont.load_default()
    
    # Draw venue name
    title_bbox = draw.textbbox((0, 0), venue_name, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, 20), venue_name, fill='white', font=title_font)
    
    # Draw description (wrapped)
    margin = 40
    max_width = width - 2 * margin
    wrapped_text = textwrap.fill(description, width=60)
    
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
    """Create venue-specific images for Denver music venues."""
    
    # Ensure the denver-photos directory exists
    os.makedirs('assets/images/denver-photos', exist_ok=True)
    
    # Define the venue images to create
    venues = [
        {
            'filename': 'assets/images/denver-photos/rhinoceropolis-exterior.jpg',
            'venue_name': 'Rhinoceropolis',
            'description': 'DIY venue in Denver that operated from 2005-2017. A cornerstone of the underground music scene before its closure due to gentrification.'
        },
        {
            'filename': 'assets/images/denver-photos/rhinoceropolis-interior.jpg',
            'venue_name': 'Rhinoceropolis Interior',
            'description': 'Interior of the DIY venue showing the warehouse space that housed underground music performances and community events.'
        },
        {
            'filename': 'assets/images/denver-photos/larimer-lounge-exterior.jpg',
            'venue_name': 'Larimer Lounge',
            'description': 'Music venue in RiNo district that has managed to persist despite surrounding gentrification and development pressure.'
        },
        {
            'filename': 'assets/images/denver-photos/larimer-lounge-interior.jpg',
            'venue_name': 'Larimer Lounge Interior',
            'description': 'Interior of Larimer Lounge showing the intimate performance space that has hosted countless underground bands.'
        },
        {
            'filename': 'assets/images/denver-photos/meadowlark-exterior.jpg',
            'venue_name': 'The Meadowlark',
            'description': 'Underground venue in RiNo that has adapted to survive in a rapidly gentrifying neighborhood.'
        },
        {
            'filename': 'assets/images/denver-photos/meadowlark-interior.jpg',
            'venue_name': 'The Meadowlark Interior',
            'description': 'Interior of The Meadowlark showing the basement performance space and DIY aesthetic.'
        },
        {
            'filename': 'assets/images/denver-photos/bluebird-theater-exterior.jpg',
            'venue_name': 'Bluebird Theater',
            'description': 'Historic theater on Colfax Avenue that has hosted music performances since 1913.'
        },
        {
            'filename': 'assets/images/denver-photos/bluebird-theater-interior.jpg',
            'venue_name': 'Bluebird Theater Interior',
            'description': 'Interior of the Bluebird Theater showing the historic venue space and stage area.'
        },
        {
            'filename': 'assets/images/denver-photos/ogden-theatre-exterior.jpg',
            'venue_name': 'Ogden Theatre',
            'description': 'Historic theater on Colfax Avenue that has been a music venue since 1919.'
        },
        {
            'filename': 'assets/images/denver-photos/ogden-theatre-interior.jpg',
            'venue_name': 'Ogden Theatre Interior',
            'description': 'Interior of the Ogden Theatre showing the historic venue space and balcony seating.'
        },
        {
            'filename': 'assets/images/denver-photos/seventh-circle-exterior.jpg',
            'venue_name': 'Seventh Circle Music Collective',
            'description': 'DIY venue and community space that has provided a home for underground music since 2012.'
        },
        {
            'filename': 'assets/images/denver-photos/seventh-circle-interior.jpg',
            'venue_name': 'Seventh Circle Interior',
            'description': 'Interior of Seventh Circle showing the DIY performance space and community gathering area.'
        },
        {
            'filename': 'assets/images/denver-photos/rino-development.jpg',
            'venue_name': 'RiNo Development',
            'description': 'River North Art District showing the transformation from industrial area to luxury development.'
        },
        {
            'filename': 'assets/images/denver-photos/rino-street-art.jpg',
            'venue_name': 'RiNo Street Art',
            'description': 'Street art and murals in the RiNo district showing the cultural appropriation of creative expression.'
        },
        {
            'filename': 'assets/images/denver-photos/colfax-corridor.jpg',
            'venue_name': 'Colfax Corridor',
            'description': 'Colfax Avenue corridor showing the historic music venues and cultural spaces along Denver\'s main east-west artery.'
        },
        {
            'filename': 'assets/images/denver-photos/colfax-venues.jpg',
            'venue_name': 'Colfax Venues',
            'description': 'Music venues along Colfax Avenue showing the concentration of cultural spaces that have resisted gentrification.'
        },
        {
            'filename': 'assets/images/denver-photos/five-points-historic.jpg',
            'venue_name': 'Five Points Historic',
            'description': 'Historic Five Points neighborhood showing the cultural heritage and community spaces before development pressure.'
        },
        {
            'filename': 'assets/images/denver-photos/five-points-development.jpg',
            'venue_name': 'Five Points Development',
            'description': 'Five Points neighborhood showing the transformation and gentrification of the historic African American cultural district.'
        },
        {
            'filename': 'assets/images/denver-photos/highland-historic.jpg',
            'venue_name': 'Highland Historic',
            'description': 'Historic Highland neighborhood showing the community spaces and cultural heritage before luxury development.'
        },
        {
            'filename': 'assets/images/denver-photos/highland-development.jpg',
            'venue_name': 'Highland Development',
            'description': 'Highland neighborhood showing the luxury development and gentrification that has transformed the area.'
        },
        {
            'filename': 'assets/images/denver-photos/south-broadway-corridor.jpg',
            'venue_name': 'South Broadway Corridor',
            'description': 'South Broadway corridor showing the concentration of music venues and cultural spaces in this area.'
        },
        {
            'filename': 'assets/images/denver-photos/south-broadway-venues.jpg',
            'venue_name': 'South Broadway Venues',
            'description': 'Music venues along South Broadway showing the underground scene and DIY spaces in this corridor.'
        }
    ]
    
    # Create each venue image
    for venue_info in venues:
        create_venue_image(
            venue_info['filename'],
            venue_info['venue_name'],
            venue_info['description']
        )
    
    print("\nAll Denver venue images have been created!")
    print("These images will now display properly in your HTML files.")
    print("\nThe images are relevant to the Denver music scene and cultural spaces discussed in your essays.")

if __name__ == "__main__":
    main()