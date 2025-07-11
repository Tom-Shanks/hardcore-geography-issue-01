#!/usr/bin/env python3
"""
Update Image Captions Script
Updates existing article images with better captions that connect to the main stories
"""

import re
import os
import json
from pathlib import Path

class ImageCaptionUpdater:
    def __init__(self):
        # Venue-specific captions
        self.venue_captions = {
            'Rhinoceropolis': [
                'Rhinoceropolis venue exterior in the Elyria-Swansea neighborhood, showing the warehouse space that housed Denver\'s experimental music scene from 2005-2017',
                'The former Rhinoceropolis building at 5070 North Washington Street, where DIY shows and art installations were hosted before demolition in 2017',
                'Rhinoceropolis interior during a performance, showcasing the industrial space that became a cornerstone of Denver\'s underground music community'
            ],
            'Larimer Lounge': [
                'Larimer Lounge venue in RiNo, one of the few remaining DIY spaces that has survived gentrification pressure',
                'Exterior of Larimer Lounge showing the venue\'s location in the rapidly developing River North Art District',
                'Larimer Lounge during a show, demonstrating how some venues have adapted to changing neighborhood conditions'
            ],
            'The Meadowlark': [
                'The Meadowlark bar in RiNo, another venue that has maintained its presence despite surrounding development',
                'Exterior view of The Meadowlark, showing the venue\'s industrial aesthetic in the gentrifying RiNo district',
                'The Meadowlark interior, preserving the warehouse atmosphere that attracted Denver\'s creative community'
            ],
            'Monkey Mania': [
                'Former location of Monkey Mania (1998-2005), one of Denver\'s early warehouse venues that closed due to development pressure',
                'The building that housed Monkey Mania, showing the type of industrial space that supported early DIY music scenes',
                'Monkey Mania venue space, representing the affordable warehouse venues that existed before systematic displacement'
            ],
            'Streets of London': [
                'Former Streets of London venue (1980s-1990s), an early Denver DIY space that operated in industrial zoning',
                'The building that housed Streets of London, showing the industrial spaces that supported early underground music',
                'Streets of London venue exterior, representing Denver\'s pre-gentrification DIY music infrastructure'
            ],
            'Kingdom of Doom': [
                'Former Kingdom of Doom venue (2005-2009), which closed amid development pressure in the Arapahoe Street area',
                'The site of Kingdom of Doom, showing how venue displacement preceded luxury residential development',
                'Kingdom of Doom building, representing venues that were eliminated through mixed-use rezoning'
            ],
            'The Church': [
                'Former The Church venue (1900s-2000s), a downtown venue lost to office development expansion',
                'The Church venue location, showing how downtown revitalization eliminated cultural spaces',
                'Former The Church building, representing venues displaced by central business district expansion'
            ],
            'The Skylark Lounge': [
                'Former The Skylark Lounge in South Broadway, a working-class venue closed for mixed-income housing development',
                'The Skylark Lounge building, showing how venue displacement accompanied residential gentrification',
                'Former Skylark Lounge location, representing the systematic elimination of working-class cultural infrastructure'
            ],
            '3 Kings Tavern': [
                'Former 3 Kings Tavern in South Broadway, another venue lost to development in the historically working-class corridor',
                'The 3 Kings Tavern building, showing how venue closures accompanied neighborhood transformation',
                'Former 3 Kings location, representing the displacement of cultural spaces in gentrifying neighborhoods'
            ],
            'Seventh Circle Music Collective': [
                'Seventh Circle Music Collective, a worker cooperative venue that has maintained community control despite gentrification',
                'Seventh Circle Music Collective exterior, showing how cooperative ownership can preserve cultural space',
                'Seventh Circle Music Collective during a show, demonstrating alternative organizational models for DIY venues'
            ]
        }
        
        # Neighborhood-specific captions
        self.neighborhood_captions = {
            'RiNo': [
                'River North Art District (RiNo) development, showing the transformation from industrial wasteland to luxury creative district',
                'RiNo neighborhood view, demonstrating how culture-washing has commodified artistic authenticity',
                'RiNo area development, showing the systematic replacement of affordable cultural spaces with luxury housing',
                'RiNo street scene, illustrating the aesthetic appropriation of displaced creative communities'
            ],
            'Highland': [
                'Highland (LoHi) neighborhood development, showing heritage washing through aesthetic preservation and economic displacement',
                'Highland area view, demonstrating how working-class authenticity is preserved visually while being eliminated economically',
                'Highland street scene, showing the transformation from working-class Latino community to luxury residential area',
                'Highland development, illustrating the strategic preservation of historic aesthetics for marketing purposes'
            ],
            'Five Points': [
                'Five Points neighborhood, showing the displacement of early DIY venues through systematic rezoning',
                'Five Points area development, demonstrating how industrial zoning changes eliminated affordable cultural spaces',
                'Five Points street scene, representing the geographic concentration of venue displacement in formerly industrial areas',
                'Five Points neighborhood view, showing the transformation from affordable warehouse spaces to luxury development'
            ],
            'Central Denver': [
                'Central Denver development, showing the concentration of venue closures in areas targeted for mixed-use rezoning',
                'Central Denver area view, demonstrating the systematic elimination of cultural infrastructure through planning policy',
                'Central Denver street scene, representing the geographic pattern of displacement that transformed Denver\'s cultural landscape',
                'Central Denver neighborhood, showing how venue displacement followed predictable geographic patterns'
            ],
            'Colfax': [
                'Colfax corridor, one of the few areas that has maintained protective zoning for cultural spaces',
                'Colfax area view, showing how commercial zoning has preserved DIY venues despite development pressure',
                'Colfax street scene, demonstrating the importance of zoning protection for cultural infrastructure',
                'Colfax corridor development, representing an area that has resisted comprehensive culture-washing'
            ],
            'Park Hill': [
                'Park Hill neighborhood, showing the dispersion of DIY music to residential areas through house shows',
                'Park Hill area view, demonstrating how underground music has adapted to displacement through tactical spatial practice',
                'Park Hill residential area, showing how house shows create temporary cultural space in residential neighborhoods',
                'Park Hill neighborhood, representing the adaptation of DIY scenes to changing urban conditions'
            ],
            'Lakewood': [
                'Lakewood area, showing the geographic expansion of DIY music beyond Denver\'s core neighborhoods',
                'Lakewood development, demonstrating how underground scenes have dispersed to suburban areas',
                'Lakewood residential area, showing how house shows operate in legal gray areas to maintain cultural production',
                'Lakewood neighborhood, representing the tactical adaptation of DIY communities to displacement'
            ],
            'South Broadway': [
                'South Broadway corridor, a historically working-class area that has lost multiple venues to development',
                'South Broadway development, showing how venue displacement accompanied residential gentrification',
                'South Broadway street scene, demonstrating the systematic elimination of working-class cultural infrastructure',
                'South Broadway area view, representing the transformation from affordable cultural spaces to luxury housing'
            ]
        }
        
        # Topic-specific captions
        self.topic_captions = {
            'warehouse': [
                'Industrial warehouse space, showing the type of affordable venue that supported Denver\'s DIY music scene',
                'Warehouse interior, demonstrating the spatial conditions that made DIY venues economically viable',
                'Industrial building exterior, representing the affordable spaces that housed underground music before displacement',
                'Warehouse district view, showing the industrial zones that inadvertently created conditions for cultural production'
            ],
            'industrial': [
                'Industrial neighborhood development, showing the systematic rezoning that eliminated affordable cultural spaces',
                'Industrial area transformation, demonstrating how mixed-use rezoning facilitated venue displacement',
                'Industrial building demolition, representing the physical elimination of cultural infrastructure',
                'Industrial zone development, showing how planning policy collaborated with real estate speculation'
            ],
            'music venue': [
                'Music venue exterior, showing the type of cultural space that has been systematically displaced',
                'Venue interior during performance, demonstrating the community spaces lost to development pressure',
                'Music venue building, representing the cultural infrastructure eliminated through gentrification',
                'Venue space, showing how DIY music scenes have adapted to changing urban conditions'
            ],
            'DIY': [
                'DIY music scene, showing the community-driven cultural production that persists despite displacement',
                'DIY venue space, demonstrating the grassroots cultural infrastructure that operates outside commercial markets',
                'DIY performance, representing the authentic cultural expression that resists commodification',
                'DIY community, showing how underground music adapts to changing spatial and economic conditions'
            ],
            'gentrification': [
                'Gentrification development, showing the systematic replacement of affordable cultural spaces with luxury housing',
                'Gentrification transformation, demonstrating how cultural displacement accompanies neighborhood change',
                'Gentrification street scene, representing the aesthetic appropriation of displaced communities',
                'Gentrification area view, showing how development pressure eliminates cultural infrastructure'
            ],
            'development': [
                'Luxury development project, showing how real estate speculation drives venue displacement',
                'Development construction, demonstrating the physical transformation that eliminates cultural spaces',
                'Development site, representing the systematic replacement of cultural infrastructure with residential projects',
                'Development area view, showing how planning policy facilitates cultural displacement'
            ]
        }

    def update_essay_images(self, essay_file):
        """Update essay markdown with better image captions"""
        with open(essay_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all image tags
        img_pattern = r'<img[^>]+src="[^"]+"[^>]*>'
        img_matches = re.findall(img_pattern, content)
        
        if not img_matches:
            print(f"No image tags found in {essay_file}")
            return content
        
        # Update images with better captions
        updated_content = content
        image_index = 0
        
        for match in img_matches:
            # Extract current alt text
            alt_match = re.search(r'alt="([^"]*)"', match)
            current_alt = alt_match.group(1) if alt_match else ''
            
            # Generate better caption based on context
            better_caption = self.generate_contextual_caption(current_alt, essay_file, image_index)
            
            # Create new image tag with better caption
            new_img_tag = self.create_updated_img_tag(match, better_caption)
            updated_content = updated_content.replace(match, new_img_tag, 1)
            image_index += 1
        
        return updated_content

    def generate_contextual_caption(self, current_alt, essay_file, image_index):
        """Generate a contextual caption based on the essay content and image context"""
        essay_name = os.path.basename(essay_file)
        
        # Determine essay topic
        if 'geography-displacement' in essay_name:
            return self.generate_displacement_caption(current_alt, image_index)
        elif 'culture-washing' in essay_name:
            return self.generate_culture_washing_caption(current_alt, image_index)
        elif 'sonic-resistance' in essay_name:
            return self.generate_resistance_caption(current_alt, image_index)
        else:
            return self.generate_general_caption(current_alt, image_index)

    def generate_displacement_caption(self, current_alt, image_index):
        """Generate captions for geography of displacement essay"""
        if 'Rhinoceropolis' in current_alt:
            return self.venue_captions['Rhinoceropolis'][image_index % len(self.venue_captions['Rhinoceropolis'])]
        elif 'warehouse' in current_alt.lower():
            return self.topic_captions['warehouse'][image_index % len(self.topic_captions['warehouse'])]
        elif 'gentrification' in current_alt.lower():
            return self.topic_captions['gentrification'][image_index % len(self.topic_captions['gentrification'])]
        else:
            return self.topic_captions['industrial'][image_index % len(self.topic_captions['industrial'])]

    def generate_culture_washing_caption(self, current_alt, image_index):
        """Generate captions for culture-washing essay"""
        if 'RiNo' in current_alt:
            return self.neighborhood_captions['RiNo'][image_index % len(self.neighborhood_captions['RiNo'])]
        elif 'Highland' in current_alt or 'LoHi' in current_alt:
            return self.neighborhood_captions['Highland'][image_index % len(self.neighborhood_captions['Highland'])]
        elif 'Colfax' in current_alt:
            return self.neighborhood_captions['Colfax'][image_index % len(self.neighborhood_captions['Colfax'])]
        else:
            return self.topic_captions['development'][image_index % len(self.topic_captions['development'])]

    def generate_resistance_caption(self, current_alt, image_index):
        """Generate captions for sonic resistance essay"""
        if 'Seventh Circle' in current_alt:
            return self.venue_captions['Seventh Circle Music Collective'][image_index % len(self.venue_captions['Seventh Circle Music Collective'])]
        elif 'warehouse' in current_alt.lower():
            return self.topic_captions['warehouse'][image_index % len(self.topic_captions['warehouse'])]
        elif 'DIY' in current_alt:
            return self.topic_captions['DIY'][image_index % len(self.topic_captions['DIY'])]
        else:
            return self.topic_captions['music venue'][image_index % len(self.topic_captions['music venue'])]

    def generate_general_caption(self, current_alt, image_index):
        """Generate general captions for other essays"""
        if 'venue' in current_alt.lower():
            return self.topic_captions['music venue'][image_index % len(self.topic_captions['music venue'])]
        elif 'industrial' in current_alt.lower():
            return self.topic_captions['industrial'][image_index % len(self.topic_captions['industrial'])]
        else:
            return self.topic_captions['development'][image_index % len(self.topic_captions['development'])]

    def create_updated_img_tag(self, original_tag, new_caption):
        """Create an updated image tag with better caption"""
        # Remove existing alt and title attributes
        tag_without_alt = re.sub(r'\s+alt="[^"]*"', '', original_tag)
        tag_without_title = re.sub(r'\s+title="[^"]*"', '', tag_without_alt)
        
        # Add new alt and title attributes
        return f'{tag_without_title} alt="{new_caption}" title="{new_caption}"'

    def update_gallery_captions(self, content):
        """Update photo gallery captions to be more contextual"""
        # Find photo gallery sections
        gallery_pattern = r'<div class="photo-gallery[^"]*">\s*<h3>([^<]+)</h3>'
        galleries = re.findall(gallery_pattern, content)
        
        updated_content = content
        
        for gallery_title in galleries:
            # Generate better gallery title
            better_title = self.generate_gallery_title(gallery_title)
            
            # Replace gallery title
            old_title = f'<h3>{gallery_title}</h3>'
            new_title = f'<h3>{better_title}</h3>'
            updated_content = updated_content.replace(old_title, new_title)
        
        return updated_content

    def generate_gallery_title(self, original_title):
        """Generate better gallery titles"""
        if 'Rhinoceropolis' in original_title:
            return 'Rhinoceropolis - The Lost DIY Venue (2005-2017)'
        elif 'Larimer Lounge' in original_title:
            return 'Larimer Lounge - Surviving Gentrification'
        elif 'The Meadowlark' in original_title:
            return 'The Meadowlark - Preserving Industrial Aesthetic'
        elif 'RiNo' in original_title:
            return 'RiNo - From Industrial to Luxury Creative District'
        elif 'Highland' in original_title:
            return 'Highland - Heritage Washing in Action'
        elif 'Five Points' in original_title:
            return 'Five Points - Systematic Venue Displacement'
        elif 'Colfax' in original_title:
            return 'Colfax - Protected Cultural Corridor'
        elif 'warehouse' in original_title.lower():
            return 'Warehouse Venues - The Displaced Cultural Infrastructure'
        elif 'industrial' in original_title.lower():
            return 'Industrial Spaces - From Cultural Production to Luxury Development'
        elif 'DIY' in original_title:
            return 'DIY Music - Community Resistance and Adaptation'
        elif 'gentrification' in original_title.lower():
            return 'Gentrification - The Systematic Elimination of Cultural Space'
        elif 'development' in original_title.lower():
            return 'Development - Real Estate Speculation and Cultural Displacement'
        else:
            return original_title

def main():
    """Main function to update all essay images"""
    updater = ImageCaptionUpdater()
    
    # Essay files to process
    essays = [
        'content/essay-01-geography-displacement_enhanced.md',
        'content/essay-02-culture-washing_enhanced.md',
        'content/essay-03-sonic-resistance_enhanced.md'
    ]
    
    for essay_file in essays:
        if os.path.exists(essay_file):
            try:
                # Update inline images
                updated_content = updater.update_essay_images(essay_file)
                
                # Update gallery captions
                updated_content = updater.update_gallery_captions(updated_content)
                
                # Write updated content
                with open(essay_file, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                print(f"Successfully updated image captions for {essay_file}")
                
            except Exception as e:
                print(f"Error processing {essay_file}: {e}")
        else:
            print(f"Essay file not found: {essay_file}")

if __name__ == "__main__":
    main()