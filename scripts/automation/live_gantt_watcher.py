#!/usr/bin/env python3
"""
Live Gantt Chart Watcher
Automatically regenerates Gantt charts when markdown files change
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
import threading
import json

class GanttChartRegenerator(FileSystemEventHandler):
    def __init__(self, data_dir="data", output_dir="output/reports", deploy_dir="deploy/gantt-chart"):
        self.data_dir = data_dir
        self.output_dir = output_dir
        self.deploy_dir = deploy_dir
        self.last_regeneration = 0
        self.regeneration_cooldown = 10  # seconds
        self.pending_changes = set()
        self.lock = threading.Lock()
        
        # Ensure output directories exist
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        Path(self.deploy_dir).mkdir(parents=True, exist_ok=True)
        
        print(f"🔍 Watching: {self.data_dir}")
        print(f"📊 Output: {self.output_dir}")
        print(f"🌐 Deploy: {self.deploy_dir}")
    
    def on_modified(self, event):
        if event.is_directory:
            return
            
        if self.should_trigger_regeneration(event.src_path):
            with self.lock:
                self.pending_changes.add(event.src_path)
            self.schedule_regeneration()
    
    def on_created(self, event):
        if event.is_directory:
            return
            
        if self.should_trigger_regeneration(event.src_path):
            with self.lock:
                self.pending_changes.add(event.src_path)
            self.schedule_regeneration()
    
    def on_deleted(self, event):
        if event.is_directory:
            return
            
        if self.should_trigger_regeneration(event.src_path):
            with self.lock:
                self.pending_changes.add(event.src_path)
            self.schedule_regeneration()
    
    def should_trigger_regeneration(self, filepath):
        """Check if file change should trigger Gantt chart regeneration"""
        # Only watch markdown files
        if not filepath.endswith('.md'):
            return False
            
        # Skip temporary files and system files
        filename = os.path.basename(filepath)
        if filename.startswith('.') or filename.startswith('~') or filename.endswith('.tmp'):
            return False
            
        # Skip files in certain directories
        excluded_dirs = ['node_modules', '.git', '__pycache__', 'backup']
        for excluded in excluded_dirs:
            if excluded in filepath:
                return False
                
        return True
    
    def schedule_regeneration(self):
        """Schedule regeneration with cooldown to avoid excessive rebuilds"""
        current_time = time.time()
        
        if current_time - self.last_regeneration < self.regeneration_cooldown:
            # Start timer for delayed regeneration
            threading.Timer(self.regeneration_cooldown, self.execute_regeneration).start()
        else:
            self.execute_regeneration()
    
    def execute_regeneration(self):
        """Execute the actual Gantt chart regeneration"""
        current_time = time.time()
        
        # Check if we're still in cooldown (multiple timers might be running)
        if current_time - self.last_regeneration < self.regeneration_cooldown:
            return
            
        self.last_regeneration = current_time
        
        with self.lock:
            changed_files = list(self.pending_changes)
            self.pending_changes.clear()
        
        if not changed_files:
            return
            
        print(f"\\n🔄 Regenerating Gantt charts... ({len(changed_files)} files changed)")
        print(f"⏰ {datetime.now().strftime('%H:%M:%S')}")
        
        try:
            # Regenerate both chart types
            success = True
            
            # 1. Advanced DHTMLX Gantt Chart
            print("  📊 Regenerating advanced Gantt chart...")
            result = subprocess.run([
                sys.executable, 
                "scripts/visualization/advanced_gantt_generator.py"
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode != 0:
                print(f"  ❌ Advanced Gantt generation failed: {result.stderr}")
                success = False
            else:
                print("  ✅ Advanced Gantt chart updated")
                
                # Deploy to web server
                self.deploy_file(
                    f"{self.output_dir}/dclt_advanced_gantt_chart.html",
                    f"{self.deploy_dir}/index.html"
                )
            
            # 2. FigJam-style Chart
            print("  🎨 Regenerating FigJam-style chart...")
            result = subprocess.run([
                sys.executable,
                "scripts/visualization/figjam_style_generator.py"
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode != 0:
                print(f"  ❌ FigJam-style generation failed: {result.stderr}")
                success = False
            else:
                print("  ✅ FigJam-style chart updated")
                
                # Deploy to web server
                self.deploy_file(
                    f"{self.output_dir}/dclt_figjam_style_timeline.html",
                    f"{self.deploy_dir}/figjam-style.html"
                )
            
            # Update metadata
            self.update_deployment_metadata(changed_files, success)
            
            if success:
                print(f"  🌐 Charts deployed and ready at http://localhost:8081/")
            else:
                print(f"  ⚠️ Some charts failed to regenerate")
                
        except subprocess.TimeoutExpired:
            print("  ⏰ Regeneration timed out")
        except Exception as e:
            print(f"  ❌ Regeneration failed: {e}")
    
    def deploy_file(self, source, destination):
        """Deploy generated file to web server"""
        try:
            if os.path.exists(source):
                import shutil
                shutil.copy2(source, destination)
                return True
        except Exception as e:
            print(f"  ⚠️ Deploy failed for {destination}: {e}")
        return False
    
    def update_deployment_metadata(self, changed_files, success):
        """Update deployment metadata for tracking"""
        metadata = {
            'last_update': datetime.now().isoformat(),
            'changed_files': changed_files,
            'success': success,
            'charts': ['advanced_gantt', 'figjam_style']
        }
        
        metadata_file = f"{self.deploy_dir}/update_metadata.json"
        try:
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
        except:
            pass  # Non-critical

class LiveGanttWatcher:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.observer = Observer()
        self.event_handler = GanttChartRegenerator(data_dir)
        
    def start_watching(self):
        """Start the file system watcher"""
        print("🚀 Starting live Gantt chart watcher...")
        print("   Changes to markdown files will automatically regenerate charts")
        print("   Press Ctrl+C to stop")
        print("=" * 60)
        
        # Set up file system watcher
        self.observer.schedule(
            self.event_handler,
            self.data_dir,
            recursive=True
        )
        
        self.observer.start()
        
        # Initial regeneration
        print("🔄 Performing initial chart generation...")
        self.event_handler.pending_changes.add("initial_run")
        self.event_handler.execute_regeneration()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\\n⏹️ Stopping watcher...")
            self.observer.stop()
        
        self.observer.join()
        print("✅ Watcher stopped")
    
    def stop_watching(self):
        """Stop the file system watcher"""
        if self.observer.is_alive():
            self.observer.stop()
            self.observer.join()

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Live Gantt Chart Watcher")
    parser.add_argument('--data-dir', default='data', help='Data directory to watch')
    parser.add_argument('--cooldown', type=int, default=10, help='Regeneration cooldown in seconds')
    
    args = parser.parse_args()
    
    # Check dependencies
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except ImportError:
        print("❌ Missing required dependency: watchdog")
        print("   Install with: pip install watchdog")
        return 1
    
    # Check if generator scripts exist
    required_scripts = [
        "scripts/visualization/advanced_gantt_generator.py",
        "scripts/visualization/figjam_style_generator.py"
    ]
    
    for script in required_scripts:
        if not os.path.exists(script):
            print(f"❌ Missing required script: {script}")
            return 1
    
    # Start watcher
    watcher = LiveGanttWatcher(args.data_dir)
    watcher.event_handler.regeneration_cooldown = args.cooldown
    
    try:
        watcher.start_watching()
        return 0
    except Exception as e:
        print(f"❌ Watcher failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())