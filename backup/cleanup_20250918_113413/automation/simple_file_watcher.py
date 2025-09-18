#!/usr/bin/env python3
"""
Simple File Watcher for Gantt Chart Auto-Regeneration
Uses built-in Python features to watch for file changes
"""

import os
import sys
import time
import subprocess
import hashlib
from pathlib import Path
from datetime import datetime
import json
import threading

class SimpleFileWatcher:
    def __init__(self, data_dir="data", output_dir="output/reports", deploy_dir="deploy/gantt-chart"):
        self.data_dir = data_dir
        self.output_dir = output_dir
        self.deploy_dir = deploy_dir
        self.file_checksums = {}
        self.last_regeneration = 0
        self.regeneration_cooldown = 15  # seconds
        self.running = True
        
        # Ensure directories exist
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        Path(self.deploy_dir).mkdir(parents=True, exist_ok=True)
        
        print(f"🔍 Watching: {self.data_dir}")
        print(f"📊 Output: {self.output_dir}")
        print(f"🌐 Deploy: {self.deploy_dir}")
        
    def get_file_checksum(self, filepath):
        """Get MD5 checksum of file for change detection"""
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
                return hashlib.md5(content).hexdigest()
        except:
            return None
    
    def scan_for_markdown_files(self):
        """Find all markdown files in data directory"""
        markdown_files = []
        
        for root, dirs, files in os.walk(self.data_dir):
            # Skip hidden directories and common excluded ones
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'backup']]
            
            for file in files:
                if file.endswith('.md') and not file.startswith('.'):
                    file_path = os.path.join(root, file)
                    markdown_files.append(file_path)
        
        return markdown_files
    
    def check_for_changes(self):
        """Check if any markdown files have changed"""
        current_files = self.scan_for_markdown_files()
        changes_detected = []
        
        # Check for new files and modified files
        for filepath in current_files:
            current_checksum = self.get_file_checksum(filepath)
            if current_checksum is None:
                continue
                
            if filepath not in self.file_checksums:
                # New file
                changes_detected.append(('new', filepath))
                self.file_checksums[filepath] = current_checksum
            elif self.file_checksums[filepath] != current_checksum:
                # Modified file
                changes_detected.append(('modified', filepath))
                self.file_checksums[filepath] = current_checksum
        
        # Check for deleted files
        for filepath in list(self.file_checksums.keys()):
            if filepath not in current_files:
                changes_detected.append(('deleted', filepath))
                del self.file_checksums[filepath]
        
        return changes_detected
    
    def regenerate_charts(self, changes):
        """Regenerate Gantt charts when changes are detected"""
        current_time = time.time()
        
        if current_time - self.last_regeneration < self.regeneration_cooldown:
            return
            
        self.last_regeneration = current_time
        
        print(f"\\n🔄 Changes detected - Regenerating charts...")
        print(f"⏰ {datetime.now().strftime('%H:%M:%S')}")
        
        for change_type, filepath in changes:
            rel_path = os.path.relpath(filepath, self.data_dir)
            print(f"  {change_type}: {rel_path}")
        
        success_count = 0
        total_charts = 2
        
        try:
            # 1. Regenerate Advanced Gantt Chart
            print("  📊 Regenerating advanced Gantt chart...")
            result = subprocess.run([
                sys.executable, 
                "scripts/visualization/advanced_gantt_generator.py"
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                print("    ✅ Advanced Gantt chart updated")
                success_count += 1
                
                # Deploy to web server
                self.deploy_file(
                    f"{self.output_dir}/dclt_advanced_gantt_chart.html",
                    f"{self.deploy_dir}/index.html"
                )
            else:
                print(f"    ❌ Advanced Gantt failed: {result.stderr[:200]}...")
            
            # 2. Regenerate FigJam-style Chart
            print("  🎨 Regenerating FigJam-style chart...")
            result = subprocess.run([
                sys.executable,
                "scripts/visualization/figjam_style_generator.py"
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                print("    ✅ FigJam-style chart updated")
                success_count += 1
                
                # Deploy to web server
                self.deploy_file(
                    f"{self.output_dir}/dclt_figjam_style_timeline.html",
                    f"{self.deploy_dir}/figjam-style.html"
                )
            else:
                print(f"    ❌ FigJam-style failed: {result.stderr[:200]}...")
            
            # Update status
            self.update_deployment_status(changes, success_count, total_charts)
            
            if success_count == total_charts:
                print(f"  🌐 All charts updated! View at http://localhost:8081/")
            elif success_count > 0:
                print(f"  ⚠️ {success_count}/{total_charts} charts updated successfully")
            else:
                print(f"  ❌ All chart regeneration failed")
                
        except subprocess.TimeoutExpired:
            print("  ⏰ Chart regeneration timed out")
        except Exception as e:
            print(f"  ❌ Regeneration error: {e}")
    
    def deploy_file(self, source, destination):
        """Deploy file to web server directory"""
        try:
            if os.path.exists(source):
                import shutil
                shutil.copy2(source, destination)
                return True
        except Exception as e:
            print(f"    ⚠️ Deploy failed: {e}")
        return False
    
    def update_deployment_status(self, changes, success_count, total_charts):
        """Update deployment status file"""
        status = {
            'last_update': datetime.now().isoformat(),
            'changes': [(change_type, os.path.relpath(path, self.data_dir)) for change_type, path in changes],
            'charts_updated': success_count,
            'total_charts': total_charts,
            'success_rate': f"{success_count}/{total_charts}",
            'status': 'success' if success_count == total_charts else 'partial' if success_count > 0 else 'failed'
        }
        
        status_file = f"{self.deploy_dir}/watcher_status.json"
        try:
            with open(status_file, 'w') as f:
                json.dump(status, f, indent=2)
        except:
            pass  # Non-critical
    
    def start_watching(self, check_interval=5):
        """Start watching for file changes"""
        print("🚀 Starting simple file watcher...")
        print(f"   Checking for changes every {check_interval} seconds")
        print("   Press Ctrl+C to stop")
        print("=" * 60)
        
        # Initial scan
        print("📋 Performing initial file scan...")
        initial_files = self.scan_for_markdown_files()
        for filepath in initial_files:
            self.file_checksums[filepath] = self.get_file_checksum(filepath)
        
        print(f"✅ Monitoring {len(initial_files)} markdown files")
        
        # Initial chart generation
        print("🔄 Performing initial chart generation...")
        self.regenerate_charts([('initial', 'startup')])
        
        # Main watching loop
        try:
            while self.running:
                time.sleep(check_interval)
                
                changes = self.check_for_changes()
                if changes:
                    self.regenerate_charts(changes)
                    
        except KeyboardInterrupt:
            print("\\n⏹️ Stopping file watcher...")
            self.running = False
        
        print("✅ File watcher stopped")
    
    def stop_watching(self):
        """Stop the file watcher"""
        self.running = False

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Simple File Watcher for Gantt Charts")
    parser.add_argument('--data-dir', default='data', help='Directory to watch for changes')
    parser.add_argument('--interval', type=int, default=5, help='Check interval in seconds')
    parser.add_argument('--cooldown', type=int, default=15, help='Regeneration cooldown in seconds')
    
    args = parser.parse_args()
    
    # Verify required scripts exist
    required_scripts = [
        "scripts/visualization/advanced_gantt_generator.py",
        "scripts/visualization/figjam_style_generator.py"
    ]
    
    missing_scripts = []
    for script in required_scripts:
        if not os.path.exists(script):
            missing_scripts.append(script)
    
    if missing_scripts:
        print("❌ Missing required generator scripts:")
        for script in missing_scripts:
            print(f"   {script}")
        return 1
    
    # Start file watcher
    watcher = SimpleFileWatcher(args.data_dir)
    watcher.regeneration_cooldown = args.cooldown
    
    try:
        watcher.start_watching(args.interval)
        return 0
    except Exception as e:
        print(f"❌ Watcher failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())