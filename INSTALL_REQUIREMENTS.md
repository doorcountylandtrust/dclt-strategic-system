# Screenshot Optimization Script - Installation Requirements

## Python Dependencies

The screenshot optimization script requires the Pillow library for image processing.

### Install Pillow

**Option 1: Using pip (recommended)**
```bash
pip3 install Pillow
```

**Option 2: Using pipx (if you prefer isolated environments)**
```bash
pipx install Pillow
```

**Option 3: Using homebrew (macOS)**
```bash
brew install python-pillow
```

**Option 4: Using conda**
```bash
conda install pillow
```

### Verify Installation

Test that Pillow is properly installed:
```bash
python3 -c "from PIL import Image; print('Pillow is ready!')"
```

## Running the Script

Once Pillow is installed, you can run the screenshot optimization:

```bash
python3 scripts/screenshot_optimization/optimize_screenshots.py
```

## What the Script Does

1. **Creates Backups**: All modified files are backed up to `screenshot_backups/`
2. **Deletes Error Files**: Removes 5 confirmed error/blocked pages
3. **Crops Large Files**: Intelligently crops 88 oversized screenshots to focus on strategic content
4. **Compresses Huge Files**: Reduces file size of 13 very large screenshots
5. **Generates Report**: Creates detailed optimization report with statistics

## Safety Features

- **Automatic Backups**: Every modified file is backed up before changes
- **Detailed Logging**: Complete log of all operations
- **User Confirmation**: Prompts before starting destructive operations
- **Error Handling**: Continues processing even if individual files fail

## Expected Results

- **46.7% of files remain untouched** (already excellent quality)
- **~30-40% storage reduction** through cropping and compression
- **Focus on strategic content**: Hero sections, navigation, key CTAs preserved
- **Improved browsing speed** for competitive analysis

Run with confidence - all changes are reversible via the backup system!