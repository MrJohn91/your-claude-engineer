#!/bin/bash

# Outreach Scraping Preparation Toolkit - Development Server Startup Script
# This script helps start the backend and/or frontend development servers

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print header
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Outreach Scraping Toolkit - Dev Setup${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Function to check if a directory exists
check_dir() {
    if [ ! -d "$1" ]; then
        echo -e "${YELLOW}Warning: $1 directory not found${NC}"
        return 1
    fi
    return 0
}

# Function to check Python
check_python() {
    if ! command -v python3 &> /dev/null; then
        echo -e "${YELLOW}Python3 is not installed${NC}"
        return 1
    fi
    echo -e "${GREEN}✓ Python3 found: $(python3 --version)${NC}"
    return 0
}

# Function to check Node.js
check_node() {
    if ! command -v node &> /dev/null; then
        echo -e "${YELLOW}Node.js is not installed${NC}"
        return 1
    fi
    echo -e "${GREEN}✓ Node.js found: $(node --version)${NC}"
    return 0
}

# Function to start backend
start_backend() {
    echo ""
    echo -e "${BLUE}Starting Backend (FastAPI)...${NC}"
    echo -e "${YELLOW}Backend will run on: http://localhost:8000${NC}"
    echo ""

    if [ ! -d "backend" ]; then
        echo -e "${YELLOW}Backend directory not found. Skipping backend startup.${NC}"
        return 1
    fi

    cd backend

    # Check if requirements.txt exists and install dependencies
    if [ -f "requirements.txt" ]; then
        echo -e "${YELLOW}Installing Python dependencies...${NC}"
        pip install -r requirements.txt
    fi

    echo -e "${GREEN}Launching backend server...${NC}"
    python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
}

# Function to start frontend
start_frontend() {
    echo ""
    echo -e "${BLUE}Starting Frontend (React + Vite)...${NC}"
    echo -e "${YELLOW}Frontend will run on: http://localhost:3000${NC}"
    echo ""

    if [ ! -d "frontend" ]; then
        echo -e "${YELLOW}Frontend directory not found. Skipping frontend startup.${NC}"
        return 1
    fi

    cd frontend

    # Check if node_modules exists, if not install dependencies
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}Installing Node.js dependencies...${NC}"
        npm install
    fi

    echo -e "${GREEN}Launching frontend dev server...${NC}"
    npm run dev
}

# Main menu
show_menu() {
    echo ""
    echo -e "${BLUE}What would you like to do?${NC}"
    echo "1) Run both backend and frontend (in separate terminals)"
    echo "2) Run backend only"
    echo "3) Run frontend only"
    echo "4) Just install dependencies (no server startup)"
    echo "5) Exit"
    echo ""
}

# Check environment
echo -e "${BLUE}Checking environment...${NC}"
check_python
check_node
echo ""

# Verify directory structure
if [ ! -d "backend" ] && [ ! -d "frontend" ]; then
    echo -e "${YELLOW}Warning: Neither backend nor frontend directory found${NC}"
    echo "Make sure you're in the project root directory"
    exit 1
fi

# Menu loop
while true; do
    show_menu
    read -p "Select an option (1-5): " choice

    case $choice in
        1)
            echo -e "${GREEN}Starting both services...${NC}"
            echo -e "${YELLOW}Note: Starting backend in background, frontend in foreground${NC}"
            echo "To stop services, press Ctrl+C and then kill background processes"
            echo ""

            # Start backend in background
            (start_backend) &
            BACKEND_PID=$!
            echo -e "${GREEN}Backend started with PID: $BACKEND_PID${NC}"

            # Give backend time to start
            sleep 3

            # Start frontend in foreground
            start_frontend

            # If we reach here, frontend stopped
            kill $BACKEND_PID 2>/dev/null || true
            echo -e "${GREEN}Both services stopped${NC}"
            ;;
        2)
            start_backend
            ;;
        3)
            start_frontend
            ;;
        4)
            echo -e "${BLUE}Installing dependencies...${NC}"

            if check_dir "backend" && [ -f "backend/requirements.txt" ]; then
                echo -e "${YELLOW}Installing Python dependencies...${NC}"
                cd backend
                pip install -r requirements.txt
                cd ..
                echo -e "${GREEN}✓ Python dependencies installed${NC}"
            fi

            if check_dir "frontend" && [ -f "frontend/package.json" ]; then
                echo -e "${YELLOW}Installing Node.js dependencies...${NC}"
                cd frontend
                npm install
                cd ..
                echo -e "${GREEN}✓ Node.js dependencies installed${NC}"
            fi

            echo -e "${GREEN}All dependencies installed!${NC}"
            echo -e "${YELLOW}Run this script again and select option 1, 2, or 3 to start servers${NC}"
            ;;
        5)
            echo -e "${GREEN}Goodbye!${NC}"
            exit 0
            ;;
        *)
            echo -e "${YELLOW}Invalid option. Please select 1-5${NC}"
            ;;
    esac
done
