# Screenshot Quality Optimizer

A Python script that implements the findings from the land trust screenshot quality assessment to automatically optimize your competitive intelligence collection.

## What It Does

Based on the comprehensive quality analysis, this script:

### 🗑️ **Deletes Poor Quality Files (5 files)**
- Removes confirmed error pages and security blocks
- Includes the CloudFlare block page from Black Canyon Regional Land Trust
- Eliminates files under 30KB that contain no useful content

### ✂️ **Crops Oversized Screenshots (88 files)**
- Intelligently crops large 2-5MB files to focus on strategic content
- Preserves: Hero sections, navigation, key CTAs, impact metrics
- Removes: Lengthy footers, repetitive content, excessive white space
- Uses smart cropping that keeps top 70% of page content

### 🗜️ **Compresses Very Large Files (13 files)**
- Reduces file sizes from 5MB+ to ~2MB range
- Maintains visual quality using progressive compression
- Tries multiple quality levels to hit target file size

## Key Features

- **🔒 Safe Operation**: Creates backups of ALL modified files
- **📊 Detailed Logging**: Complete audit trail of all operations
- **📈 Storage Analytics**: Reports exact savings achieved
- **⚡ Batch Processing**: Handles all 210+ screenshots automatically
- **🛡️ Error Handling**: Continues processing even if individual files fail

## Installation & Setup

### 1. Install Dependencies
```bash
pip3 install Pillow
```

### 2. Verify Installation
```bash
python3 scripts/screenshot_optimization/test_script_logic.py
```

### 3. Run Optimization
```bash
python3 scripts/screenshot_optimization/optimize_screenshots.py
```

## Expected Results

- **46.7% of files remain untouched** (already excellent quality)
- **30-40% storage reduction** through smart cropping and compression
- **Improved browsing speed** for competitive analysis
- **Focus on strategic content** while preserving visual quality

## File Processing Categories

| Category | Count | Action | Result |
|----------|-------|--------|---------|
| Excellent | 76 | Keep unchanged | Ready for analysis |
| Good | 22 | Keep unchanged | Ready for analysis |
| Crop | 88 | Smart crop to strategic content | Focused competitive intel |
| Compress | 13 | Reduce file size | Manageable storage |
| Delete | 5 | Remove error pages | Clean collection |
| Review | 6 | Manual inspection needed | Flagged for attention |

## Safety & Backup System

### Automatic Backups
- **Location**: `screenshot_backups/` directory
- **Coverage**: Every file that gets modified or deleted
- **Naming**: Handles conflicts with automatic numbering
- **Restoration**: Simple copy back to restore any file

### Detailed Logging
- **File**: `output/reports/screenshot_optimization_YYYYMMDD_HHMMSS.log`
- **Content**: Every operation with timestamps and file sizes
- **Errors**: Complete error reporting with details
- **Summary**: Final statistics and savings report

## Smart Cropping Logic

The script uses intelligent cropping that:

1. **Analyzes file size** to determine crop necessity
2. **Preserves strategic content** in the top 70% of the page
3. **Maintains minimum height** of 800px for readability
4. **Skips minimal crops** (less than 10% reduction)
5. **Focuses on key elements**:
   - Header navigation and branding
   - Hero section with primary messaging
   - Main content blocks and CTAs
   - Impact metrics and key statistics

## Compression Strategy

For very large files (5MB+), the script:

1. **Targets 2MB file size** for optimal balance
2. **Uses progressive quality reduction** (85% → 75% → 65% → 55%)
3. **Maintains visual fidelity** while reducing storage
4. **Applies optimization** for web-friendly loading

## Usage Example

```bash
$ python3 scripts/screenshot_optimization/optimize_screenshots.py

Screenshot Optimization Script
========================================
This script will:
1. DELETE 5 poor-quality/error screenshots
2. CROP 88 oversized screenshots to focus on strategic content
3. COMPRESS 13 very large screenshots
4. CREATE BACKUPS of all modified files

Proceed? (y/N): y

2025-09-11 14:30:15 - INFO - Screenshot optimization started
2025-09-11 14:30:15 - INFO - Loaded analysis for 210 files
2025-09-11 14:30:15 - INFO - Deleting 5 poor-quality screenshots
2025-09-11 14:30:15 - INFO - DELETED: Black_Canyon_Regional_Land_Trust_homepage.png (26.8 KB) - Reason: Very small file size
...
```

## Advanced Usage

### Selective Processing
You can modify the script to run only specific operations:

```python
# Only delete poor quality files
optimizer.run_optimization(delete_files=True, crop_files=False, compress_files=False)

# Only crop and compress, don't delete
optimizer.run_optimization(delete_files=False, crop_files=True, compress_files=True)
```

### Custom Parameters
Adjust cropping and compression settings:

```python
# Keep top 80% instead of 70%
optimizer.smart_crop_screenshot(image_path, target_height_ratio=0.8)

# Target 1.5MB instead of 2MB
optimizer.compress_large_file(image_path, target_size_mb=1.5)
```

## Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'PIL'"**
- Solution: Install Pillow with `pip3 install Pillow`

**"Permission denied" errors**
- Solution: Ensure you have write access to the screenshots directory
- Try running with `sudo` if necessary

**"File not found" warnings**
- Normal: Some files may have been moved or renamed since analysis
- Script continues processing remaining files

### Recovery

If something goes wrong:
1. **Stop the script** with Ctrl+C
2. **Check the backup directory** `screenshot_backups/`
3. **Restore files** by copying from backup to original location
4. **Review the log file** for specific error details

## Performance

- **Processing time**: ~2-5 minutes for 210 files
- **Memory usage**: Minimal (processes one image at a time)
- **Storage**: Creates temporary backup copies during processing
- **CPU**: Moderate during image processing operations

## Integration

This script integrates with your competitive intelligence workflow:

1. **Automated optimization** of screenshot collections
2. **Standardized file sizes** for consistent analysis
3. **Focused content** for strategic comparison
4. **Clean datasets** for further processing

Perfect for preparing land trust competitive intelligence assets for strategic analysis and comparison studies.