#!/bin/bash
set -e

echo "🚀 Starting Outreach Scraping Toolkit..."

# Install backend dependencies
if [ -d "backend" ]; then
    echo "📦 Installing backend dependencies..."
    cd backend
    pip install -r requirements.txt 2>/dev/null || pip3 install -r requirements.txt 2>/dev/null
    cd ..
fi

# Install frontend dependencies
if [ -d "frontend" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

# Start backend
if [ -d "backend" ]; then
    echo "🔧 Starting backend server..."
    cd backend
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
    BACKEND_PID=$!
    cd ..
    echo "✅ Backend running on http://localhost:8000"
fi

# Start frontend
if [ -d "frontend" ]; then
    echo "🎨 Starting frontend dev server..."
    cd frontend
    npm run dev &
    FRONTEND_PID=$!
    cd ..
    echo "✅ Frontend running on http://localhost:5173"
fi

echo ""
echo "🎉 All services started!"
echo "   Backend:  http://localhost:8000"
echo "   Frontend: http://localhost:5173"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for background processes
wait
