#!/usr/bin/env python3
"""
DCLT Legacy Content Archiver
==============================
Zips the legacy_site_content directory and stray zip files,
then removes them from the working tree.

Usage:
    cd /path/to/your/workspace
    python scripts/archive_legacy.py

Or with an explicit path:
    python scripts/archive_legacy.py /path/to/workspace
"""

import os
import sys
import shutil
import zipfile
from pathlib import Path
from datetime import datetime


def count_md_files(directory):
    return sum(1 for _ in Path(directory).rglob('*.md'))


def main():
    workspace = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
    date_str = datetime.now().strftime('%Y%m%d')

    legacy_dir = workspace / '01_STRATEGY' / 'legacy_site_content'
    archive_dir = workspace / '_archive'
    archive_path = archive_dir / f'legacy_site_content_{date_str}.zip'

    print("=" * 50)
    print("DCLT Legacy Content Archiver")
    print("=" * 50)
    print(f"\nWorkspace: {workspace}")

    if not legacy_dir.exists():
        print("\nNo legacy_site_content directory found. Nothing to archive.")
        return

    total_before = count_md_files(workspace)
    legacy_count = count_md_files(legacy_dir)

    print(f"\nTotal .md files in workspace: {total_before}")
    print(f"Files in legacy_site_content: {legacy_count}")
    print()

    response = input("Archive and remove legacy content? (y/N) ").strip().lower()
    if response != 'y':
        print("Cancelled.")
        return

    # Create archive directory
    archive_dir.mkdir(exist_ok=True)

    # Create zip
    print("\nCreating archive...")
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in legacy_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(workspace)
                zf.write(file_path, arcname)

    size_mb = archive_path.stat().st_size / (1024 * 1024)
    print(f"Archive created: {archive_path} ({size_mb:.1f} MB)")

    # Remove legacy directory
    print("\nRemoving legacy_site_content...")
    shutil.rmtree(legacy_dir)
    print("  Removed: 01_STRATEGY/legacy_site_content/")

    # Move stray zip files
    stray_zips = [
        '02_EXECUTION.zip',
        '03_REFERENCE_AND_TOOLS.zip',
        'Strategy_NoImages.zip'
    ]
    for zname in stray_zips:
        zpath = workspace / zname
        if zpath.exists():
            shutil.move(str(zpath), str(archive_dir / zname))
            print(f"  Moved to archive: {zname}")

    total_after = count_md_files(workspace)

    print(f"\n{'=' * 50}")
    print("Done!")
    print(f"{'=' * 50}")
    print(f"Files before: {total_before}")
    print(f"Files after:  {total_after}")
    print(f"Removed:      {total_before - total_after} files")
    print(f"\nRestore anytime with:")
    print(f"  cd {workspace} && unzip {archive_path}")


if __name__ == '__main__':
    main()