#!/usr/bin/env python3
"""
Screenshot Quality Optimizer for Land Trust Competitive Intelligence
Implements recommendations from screenshot quality assessment to:
- Delete poor-quality/error screenshots
- Crop oversized screenshots to focus on strategic content
- Compress very large files while maintaining quality
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageOps
import logging

class ScreenshotOptimizer:
    def __init__(self, screenshots_dir='data/landtrusts/datasets/screens/screenshots'):
        self.screenshots_dir = Path(screenshots_dir)
        self.backup_dir = Path('screenshot_backups')
        self.reports_dir = Path('output/reports')
        
        # Setup logging first
        self.setup_logging()
        
        # Load quality assessment results
        self.analysis_file = self.reports_dir / 'screenshot_analysis.json'
        self.load_analysis()
        
        # Optimization statistics
        self.stats = {
            'deleted': 0,
            'cropped': 0,
            'compressed': 0,
            'errors': 0,
            'total_size_before': 0,
            'total_size_after': 0
        }
    
    def setup_logging(self):
        """Setup logging for optimization operations"""
        log_file = self.reports_dir / f'screenshot_optimization_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("Screenshot optimization started")
    
    def load_analysis(self):
        """Load the quality assessment analysis results"""
        try:
            with open(self.analysis_file, 'r') as f:
                self.analysis = json.load(f)
            self.logger.info(f"Loaded analysis for {self.analysis['summary']['total_files']} files")
        except FileNotFoundError:
            self.logger.error(f"Analysis file not found: {self.analysis_file}")
            raise
        except Exception as e:
            self.logger.error(f"Error loading analysis: {e}")
            raise
    
    def create_backup(self, file_path):
        """Create backup of file before modification"""
        if not self.backup_dir.exists():
            self.backup_dir.mkdir(parents=True)
            
        backup_path = self.backup_dir / file_path.name
        
        # Handle name conflicts in backup
        counter = 1
        original_backup_path = backup_path
        while backup_path.exists():
            name_parts = original_backup_path.stem, original_backup_path.suffix
            backup_path = self.backup_dir / f"{name_parts[0]}_backup_{counter}{name_parts[1]}"
            counter += 1
        
        shutil.copy2(file_path, backup_path)
        self.logger.debug(f"Created backup: {backup_path}")
        return backup_path
    
    def delete_poor_quality_files(self):
        """Delete files marked for deletion in quality assessment"""
        delete_list = self.analysis['categories']['delete']
        
        self.logger.info(f"Deleting {len(delete_list)} poor-quality screenshots")
        
        for file_info in delete_list:
            file_path = self.screenshots_dir / file_info['filename']
            
            if file_path.exists():
                try:
                    # Record original size
                    original_size = file_path.stat().st_size
                    self.stats['total_size_before'] += original_size
                    
                    # Create backup before deletion
                    backup_path = self.create_backup(file_path)
                    
                    # Delete the file
                    file_path.unlink()
                    
                    self.stats['deleted'] += 1
                    self.logger.info(f"DELETED: {file_info['filename']} ({file_info['file_size_kb']} KB) - Reason: {', '.join(file_info['issues'])}")
                    
                except Exception as e:
                    self.stats['errors'] += 1
                    self.logger.error(f"Error deleting {file_info['filename']}: {e}")
            else:
                self.logger.warning(f"File not found for deletion: {file_info['filename']}")
    
    def smart_crop_screenshot(self, image_path, target_height_ratio=0.7):
        """
        Intelligently crop screenshot to focus on strategic content
        
        Args:
            image_path: Path to image file
            target_height_ratio: Ratio of original height to keep (0.7 = keep top 70%)
        """
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                
                # Calculate crop dimensions
                # Keep full width, crop from top to remove excessive footer content
                crop_height = int(height * target_height_ratio)
                
                # Ensure minimum reasonable height
                min_height = 800
                crop_height = max(crop_height, min_height)
                
                # Don't crop if the reduction is minimal
                if crop_height >= height * 0.9:
                    self.logger.debug(f"Skipping crop for {image_path.name} - minimal reduction")
                    return False
                
                # Define crop box (left, top, right, bottom)
                crop_box = (0, 0, width, crop_height)
                
                # Crop the image
                cropped_img = img.crop(crop_box)
                
                # Save the cropped image (overwrites original)
                cropped_img.save(image_path, optimize=True, quality=85)
                
                self.logger.info(f"CROPPED: {image_path.name} from {width}x{height} to {width}x{crop_height}")
                return True
                
        except Exception as e:
            self.logger.error(f"Error cropping {image_path.name}: {e}")
            return False
    
    def compress_large_file(self, image_path, target_size_mb=2.0):
        """
        Compress very large image files while maintaining visual quality
        
        Args:
            image_path: Path to image file
            target_size_mb: Target file size in MB
        """
        try:
            original_size = image_path.stat().st_size
            original_size_mb = original_size / (1024 * 1024)
            
            if original_size_mb <= target_size_mb:
                return False
            
            with Image.open(image_path) as img:
                # Try different quality levels to reach target size
                for quality in [85, 75, 65, 55]:
                    # Save to temporary file to check size
                    temp_path = image_path.with_suffix('.tmp.png')
                    img.save(temp_path, optimize=True, quality=quality)
                    
                    temp_size = temp_path.stat().st_size
                    temp_size_mb = temp_size / (1024 * 1024)
                    
                    if temp_size_mb <= target_size_mb:
                        # Replace original with compressed version
                        shutil.move(temp_path, image_path)
                        
                        self.logger.info(f"COMPRESSED: {image_path.name} from {original_size_mb:.1f}MB to {temp_size_mb:.1f}MB (quality={quality})")
                        return True
                    else:
                        # Remove temp file and try lower quality
                        temp_path.unlink()
                
                # If we can't reach target size, use the last attempt
                img.save(image_path, optimize=True, quality=55)
                final_size = image_path.stat().st_size
                final_size_mb = final_size / (1024 * 1024)
                
                self.logger.info(f"COMPRESSED: {image_path.name} from {original_size_mb:.1f}MB to {final_size_mb:.1f}MB (best effort)")
                return True
                
        except Exception as e:
            self.logger.error(f"Error compressing {image_path.name}: {e}")
            return False
    
    def process_crop_candidates(self):
        """Process files marked for cropping"""
        crop_list = self.analysis['categories']['crop']
        
        self.logger.info(f"Processing {len(crop_list)} files for cropping")
        
        for file_info in crop_list:
            file_path = self.screenshots_dir / file_info['filename']
            
            if file_path.exists():
                try:
                    # Record original size
                    original_size = file_path.stat().st_size
                    self.stats['total_size_before'] += original_size
                    
                    # Create backup
                    backup_path = self.create_backup(file_path)
                    
                    # Attempt cropping
                    if self.smart_crop_screenshot(file_path):
                        self.stats['cropped'] += 1
                        
                        # Record new size
                        new_size = file_path.stat().st_size
                        self.stats['total_size_after'] += new_size
                    else:
                        # No crop applied, record original size
                        self.stats['total_size_after'] += original_size
                    
                except Exception as e:
                    self.stats['errors'] += 1
                    self.logger.error(f"Error processing crop for {file_info['filename']}: {e}")
            else:
                self.logger.warning(f"File not found for cropping: {file_info['filename']}")
    
    def process_compression_candidates(self):
        """Process files marked for compression"""
        compress_list = self.analysis['categories']['compress']
        
        self.logger.info(f"Processing {len(compress_list)} files for compression")
        
        for file_info in compress_list:
            file_path = self.screenshots_dir / file_info['filename']
            
            if file_path.exists():
                try:
                    # Record original size
                    original_size = file_path.stat().st_size
                    self.stats['total_size_before'] += original_size
                    
                    # Create backup
                    backup_path = self.create_backup(file_path)
                    
                    # Attempt compression
                    if self.compress_large_file(file_path):
                        self.stats['compressed'] += 1
                        
                        # Record new size
                        new_size = file_path.stat().st_size
                        self.stats['total_size_after'] += new_size
                    else:
                        # No compression applied, record original size
                        self.stats['total_size_after'] += original_size
                    
                except Exception as e:
                    self.stats['errors'] += 1
                    self.logger.error(f"Error compressing {file_info['filename']}: {e}")
            else:
                self.logger.warning(f"File not found for compression: {file_info['filename']}")
    
    def calculate_size_for_unchanged_files(self):
        """Calculate total size for files that weren't modified"""
        excellent_list = self.analysis['categories']['excellent']
        good_list = self.analysis['categories']['good']
        
        for file_list in [excellent_list, good_list]:
            for file_info in file_list:
                file_path = self.screenshots_dir / file_info['filename']
                if file_path.exists():
                    size = file_path.stat().st_size
                    self.stats['total_size_before'] += size
                    self.stats['total_size_after'] += size
    
    def generate_optimization_report(self):
        """Generate detailed report of optimization results"""
        
        # Calculate savings
        size_saved = self.stats['total_size_before'] - self.stats['total_size_after']
        size_saved_mb = size_saved / (1024 * 1024)
        size_saved_percent = (size_saved / self.stats['total_size_before']) * 100 if self.stats['total_size_before'] > 0 else 0
        
        report = f"""
# Screenshot Optimization Report
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

## Summary
- **Files Deleted**: {self.stats['deleted']}
- **Files Cropped**: {self.stats['cropped']}
- **Files Compressed**: {self.stats['compressed']}
- **Errors Encountered**: {self.stats['errors']}

## Storage Impact
- **Before Optimization**: {self.stats['total_size_before'] / (1024*1024):.1f} MB
- **After Optimization**: {self.stats['total_size_after'] / (1024*1024):.1f} MB
- **Space Saved**: {size_saved_mb:.1f} MB ({size_saved_percent:.1f}% reduction)

## Files Affected
Total files processed: {self.stats['deleted'] + self.stats['cropped'] + self.stats['compressed']}

## Backup Location
All modified/deleted files backed up to: {self.backup_dir}

## Next Steps
1. Review cropped files to ensure strategic content is preserved
2. Check compressed files for acceptable quality
3. Consider re-capturing any problematic sites identified in manual review list
"""
        
        report_path = self.reports_dir / f'screenshot_optimization_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        with open(report_path, 'w') as f:
            f.write(report)
        
        self.logger.info(f"Optimization report saved to: {report_path}")
        return report
    
    def run_optimization(self, delete_files=True, crop_files=True, compress_files=True):
        """
        Run complete screenshot optimization process
        
        Args:
            delete_files: Whether to delete poor-quality files
            crop_files: Whether to crop oversized files
            compress_files: Whether to compress very large files
        """
        
        self.logger.info("=== Starting Screenshot Optimization ===")
        
        # Ensure directories exist
        self.reports_dir.mkdir(exist_ok=True)
        
        if not self.screenshots_dir.exists():
            self.logger.error(f"Screenshots directory not found: {self.screenshots_dir}")
            return
        
        try:
            # Step 1: Delete poor-quality files
            if delete_files:
                self.delete_poor_quality_files()
            
            # Step 2: Crop oversized files
            if crop_files:
                self.process_crop_candidates()
            
            # Step 3: Compress very large files
            if compress_files:
                self.process_compression_candidates()
            
            # Step 4: Account for unchanged files
            self.calculate_size_for_unchanged_files()
            
            # Step 5: Generate report
            report = self.generate_optimization_report()
            
            self.logger.info("=== Screenshot Optimization Complete ===")
            print("\n" + "="*50)
            print(report)
            print("="*50)
            
        except Exception as e:
            self.logger.error(f"Optimization failed: {e}")
            raise

def main():
    """Main execution function"""
    try:
        optimizer = ScreenshotOptimizer()
        
        # Ask user for confirmation before proceeding
        print("\nScreenshot Optimization Script")
        print("="*40)
        print("This script will:")
        print("1. DELETE 5 poor-quality/error screenshots")
        print("2. CROP 88 oversized screenshots to focus on strategic content")
        print("3. COMPRESS 13 very large screenshots")
        print("4. CREATE BACKUPS of all modified files")
        print("\nProceed? (y/N): ", end="")
        
        response = input().strip().lower()
        if response != 'y':
            print("Operation cancelled.")
            return
        
        # Run optimization
        optimizer.run_optimization()
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()