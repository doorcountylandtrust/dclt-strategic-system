#!/usr/bin/env python3
"""
Analyze land trust homepage screenshots for quality assessment
"""
import os
from pathlib import Path
import json

def analyze_screenshot_quality(image_path):
    """Analyze a single screenshot for quality indicators"""
    try:
        file_size = os.path.getsize(image_path)
        
        # Quality assessment based on file characteristics
        quality_issues = []
        recommendations = []
        
        # Check file size indicators
        if file_size < 30000:  # 30KB - likely error page
            quality_issues.append("Very small file size")
            recommendations.append("Likely error/blocked/incomplete page - DELETE")
        elif file_size < 100000:  # 100KB - possibly incomplete
            quality_issues.append("Small file size")
            recommendations.append("May be incomplete page - REVIEW")
        elif file_size > 8000000:  # 8MB - very large
            quality_issues.append("Very large file size")
            recommendations.append("Consider compression or cropping")
        
        # Check filename for clues
        filename_lower = image_path.name.lower()
        
        # Problematic indicators in filename or size
        problematic_terms = ['error', 'blocked', '404', 'forbidden', 'unavailable']
        if any(term in filename_lower for term in problematic_terms):
            quality_issues.append("Filename suggests error page")
            recommendations.append("DELETE - error page")
        
        # Determine quality based on file size ranges and characteristics
        if file_size < 30000:
            quality = "delete"  # Too small, likely error
        elif file_size < 100000:
            quality = "review"  # Small, needs manual check
        elif file_size < 500000:
            quality = "good"    # Reasonable size
        elif file_size < 2000000:
            quality = "excellent"  # Good full page
        elif file_size < 5000000:
            quality = "crop"    # Large, might benefit from cropping
        else:
            quality = "compress"  # Very large, needs compression
        
        # Special handling for very small files
        if file_size < 50000:
            quality = "delete"
            recommendations = ["DELETE - File too small, likely error page"]
        
        return {
            'filename': image_path.name,
            'file_size_kb': round(file_size / 1024, 1),
            'file_size_mb': round(file_size / (1024*1024), 2),
            'quality': quality,
            'issues': quality_issues,
            'recommendations': recommendations
        }
        
    except Exception as e:
        return {
            'filename': image_path.name,
            'error': str(e),
            'quality': 'error',
            'issues': ['File cannot be accessed'],
            'recommendations': ['DELETE - corrupted file']
        }

def main():
    """Analyze all screenshots"""
    screenshots_dir = Path('data/landtrusts/datasets/screens/screenshots')
    
    if not screenshots_dir.exists():
        print(f"Directory not found: {screenshots_dir}")
        return
    
    # Get all image files
    image_files = []
    for ext in ['*.png', '*.jpg', '*.jpeg']:
        image_files.extend(screenshots_dir.glob(ext))
    
    print(f"Found {len(image_files)} screenshot files")
    
    # Analyze each image
    results = []
    for img_path in sorted(image_files):
        print(f"Analyzing: {img_path.name}")
        analysis = analyze_screenshot_quality(img_path)
        results.append(analysis)
    
    # Categorize results
    excellent = [r for r in results if r.get('quality') == 'excellent']
    good = [r for r in results if r.get('quality') == 'good']
    crop = [r for r in results if r.get('quality') == 'crop']
    compress = [r for r in results if r.get('quality') == 'compress']
    review = [r for r in results if r.get('quality') == 'review']
    delete = [r for r in results if r.get('quality') == 'delete']
    errors = [r for r in results if r.get('quality') == 'error']
    
    # Save detailed results
    os.makedirs('output/reports', exist_ok=True)
    with open('output/reports/screenshot_analysis.json', 'w') as f:
        json.dump({
            'summary': {
                'total_files': len(results),
                'excellent': len(excellent),
                'good': len(good),
                'crop': len(crop),
                'compress': len(compress),
                'review': len(review),
                'delete': len(delete),
                'errors': len(errors)
            },
            'categories': {
                'excellent': excellent,
                'good': good,
                'crop': crop,
                'compress': compress,
                'review': review,
                'delete': delete,
                'errors': errors
            },
            'detailed_results': results
        }, f, indent=2)
    
    print(f"\nQuality Distribution:")
    print(f"Excellent (keep): {len(excellent)}")
    print(f"Good (keep): {len(good)}")
    print(f"Crop (edit): {len(crop)}")
    print(f"Compress (edit): {len(compress)}")
    print(f"Review (manual check): {len(review)}")
    print(f"Delete: {len(delete)}")
    print(f"Errors: {len(errors)}")
    
    return results, excellent, good, crop, compress, review, delete, errors

if __name__ == '__main__':
    main()