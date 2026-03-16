#!/bin/bash

# Comic Generator Startup Script

echo "================================"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ Error: uv not found, please install uv first"
    echo "💡 Mac/Linux installation: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Sync dependencies
echo "📦 Checking and installing dependencies..."
cd backend
uv sync
if [ $? -ne 0 ]; then
    echo "❌ Dependency installation failed"
    exit 1
fi
cd ..

# Start backend server
echo "🚀 Starting backend service..."
cd backend
uv run app.py &
BACKEND_PID=$!
cd ..

echo "✅ Backend service started (PID: $BACKEND_PID)"
echo "📍 Backend address: http://localhost:5003"

# Wait for backend to start
sleep 2

# Start frontend server
echo "🚀 Starting frontend service..."
python3 -m http.server 8000 &
FRONTEND_PID=$!

echo "✅ Frontend service started (PID: $FRONTEND_PID)"
echo "📍 Frontend address: http://localhost:8000"
echo ""
echo "================================"
echo "✨ All services started!"
echo "🌐 Please open in browser: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop all services"
echo "================================"

# Trap Ctrl+C to kill both processes
trap "echo ''; echo '🛑 Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; echo '✅ Services stopped'; exit 0" INT

# Wait for processes
wait
