#!/bin/bash
# DCLT Live Gantt Chart System Startup Script

echo "🚀 Starting DCLT Live Gantt Chart System"
echo "========================================"

# Check if we're in the right directory
if [ ! -f "scripts/automation/simple_file_watcher.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Kill any existing servers on ports 8080 and 8081
echo "🧹 Cleaning up existing servers..."
lsof -ti :8080 | xargs kill -9 2>/dev/null || true
lsof -ti :8081 | xargs kill -9 2>/dev/null || true

# Start web server in background
echo "🌐 Starting web server on port 8081..."
cd deploy/gantt-chart
python3 -m http.server 8081 > server.log 2>&1 &
SERVER_PID=$!
cd ../..

# Wait for server to start
sleep 2

# Test server
if curl -s -I http://localhost:8081/ | grep -q "200 OK"; then
    echo "✅ Web server running at http://localhost:8081/"
else
    echo "❌ Web server failed to start"
    exit 1
fi

echo ""
echo "📊 Available Charts:"
echo "  • Advanced Gantt: http://localhost:8081/"
echo "  • FigJam Style:   http://localhost:8081/figjam-style.html"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down..."
    kill $SERVER_PID 2>/dev/null || true
    kill $WATCHER_PID 2>/dev/null || true
    echo "✅ Cleanup complete"
    exit 0
}

# Set trap for cleanup
trap cleanup INT TERM EXIT

# Start file watcher
echo "👁️ Starting file watcher (live updates enabled)..."
echo "   Any changes to markdown files will automatically regenerate charts"
echo "   Press Ctrl+C to stop everything"
echo ""

python3 scripts/automation/simple_file_watcher.py --interval 3 --cooldown 10 &
WATCHER_PID=$!

# Keep script running
wait $WATCHER_PID