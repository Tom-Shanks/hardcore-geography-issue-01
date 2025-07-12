#!/usr/bin/env python3
"""
Comprehensive Enhancement Script
Combines photo replacement and visualization enhancement into a single workflow
"""

import os
import sys
import logging
from pathlib import Path
import subprocess
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ComprehensiveEnhancer:
    def __init__(self):
        self.scripts_dir = Path('scripts')
        self.essays_dir = Path('essays')
        self.assets_dir = Path('assets')
        self.data_dir = Path('data')
        
    def run_photo_replacement(self):
        """Run the photo replacement script"""
        logger.info("Starting photo replacement process...")
        
        try:
            # Create denver-photos directory if it doesn't exist
            photos_dir = self.assets_dir / 'images' / 'denver-photos'
            photos_dir.mkdir(parents=True, exist_ok=True)
            
            # Run the photo replacement script
            script_path = self.scripts_dir / 'replace_stock_photos.py'
            if script_path.exists():
                result = subprocess.run([sys.executable, str(script_path)], 
                                      capture_output=True, text=True)
                
                if result.returncode == 0:
                    logger.info("Photo replacement completed successfully")
                    return True
                else:
                    logger.error(f"Photo replacement failed: {result.stderr}")
                    return False
            else:
                logger.error("Photo replacement script not found")
                return False
                
        except Exception as e:
            logger.error(f"Error running photo replacement: {e}")
            return False
    
    def run_visualization_enhancement(self):
        """Run the visualization enhancement script"""
        logger.info("Starting visualization enhancement process...")
        
        try:
            # Run the visualization enhancement script
            script_path = self.scripts_dir / 'enhance_visualization_tool.py'
            if script_path.exists():
                result = subprocess.run([sys.executable, str(script_path)], 
                                      capture_output=True, text=True)
                
                if result.returncode == 0:
                    logger.info("Visualization enhancement completed successfully")
                    return True
                else:
                    logger.error(f"Visualization enhancement failed: {result.stderr}")
                    return False
            else:
                logger.error("Visualization enhancement script not found")
                return False
                
        except Exception as e:
            logger.error(f"Error running visualization enhancement: {e}")
            return False
    
    def validate_enhancements(self):
        """Validate that enhancements were applied correctly"""
        logger.info("Validating enhancements...")
        
        validation_results = {
            'denver_photos_exist': False,
            'enhanced_venues_csv_exists': False,
            'venue_photos_json_exists': False,
            'map_updated': False,
            'essays_updated': False
        }
        
        # Check if Denver photos directory exists and has photos
        photos_dir = self.assets_dir / 'images' / 'denver-photos'
        if photos_dir.exists():
            photos = list(photos_dir.glob('*.jpg')) + list(photos_dir.glob('*.png'))
            validation_results['denver_photos_exist'] = len(photos) > 0
            logger.info(f"Found {len(photos)} Denver photos")
        
        # Check if enhanced venues CSV exists
        enhanced_csv = self.data_dir / 'enhanced_venues.csv'
        validation_results['enhanced_venues_csv_exists'] = enhanced_csv.exists()
        
        # Check if venue photos JSON exists
        photos_json = self.data_dir / 'venue_photos.json'
        validation_results['venue_photos_json_exists'] = photos_json.exists()
        
        # Check if map was updated
        map_file = self.assets_dir / 'interactive-map.html'
        if map_file.exists():
            with open(map_file, 'r', encoding='utf-8') as f:
                content = f.read()
                validation_results['map_updated'] = 'showEnhancedVenueInfo' in content
        
        # Check if essays were updated
        essay_files = list(self.essays_dir.glob('*.html'))
        updated_essays = 0
        for essay_file in essay_files:
            if not essay_file.name.endswith('_enhanced.html'):
                with open(essay_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'denver-photos' in content:
                        updated_essays += 1
        
        validation_results['essays_updated'] = updated_essays > 0
        logger.info(f"Updated {updated_essays} essays")
        
        return validation_results
    
    def create_comprehensive_report(self, photo_success, viz_success, validation_results):
        """Create a comprehensive report of all enhancements"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'photo_replacement_success': photo_success,
            'visualization_enhancement_success': viz_success,
            'validation_results': validation_results,
            'overall_success': photo_success and viz_success and all(validation_results.values()),
            'summary': {
                'total_enhancements': sum([photo_success, viz_success]),
                'total_validations_passed': sum(validation_results.values()),
                'total_validations': len(validation_results)
            }
        }
        
        # Save report
        with open('comprehensive_enhancement_report.json', 'w') as f:
            import json
            json.dump(report, f, indent=2)
        
        return report
    
    def run_comprehensive_enhancement(self):
        """Run the complete enhancement workflow"""
        logger.info("Starting comprehensive enhancement workflow...")
        
        # Step 1: Photo replacement
        photo_success = self.run_photo_replacement()
        
        # Step 2: Visualization enhancement
        viz_success = self.run_visualization_enhancement()
        
        # Step 3: Validation
        validation_results = self.validate_enhancements()
        
        # Step 4: Create comprehensive report
        report = self.create_comprehensive_report(photo_success, viz_success, validation_results)
        
        # Print summary
        print("\n" + "="*50)
        print("COMPREHENSIVE ENHANCEMENT SUMMARY")
        print("="*50)
        print(f"Photo Replacement: {'✓' if photo_success else '✗'}")
        print(f"Visualization Enhancement: {'✓' if viz_success else '✗'}")
        print(f"Validations Passed: {report['summary']['total_validations_passed']}/{report['summary']['total_validations']}")
        print(f"Overall Success: {'✓' if report['overall_success'] else '✗'}")
        print("="*50)
        
        if report['overall_success']:
            print("🎉 All enhancements completed successfully!")
            print("📸 Stock photos replaced with authentic Denver photographs")
            print("🗺️  Interactive map enhanced with comprehensive venue data")
            print("📊 Check comprehensive_enhancement_report.json for details")
        else:
            print("⚠️  Some enhancements failed. Check the report for details.")
        
        return report

def main():
    """Main function"""
    enhancer = ComprehensiveEnhancer()
    report = enhancer.run_comprehensive_enhancement()
    
    return report

if __name__ == "__main__":
    main()