#!/bin/bash

echo "========================================"
echo "نظام إدارة المخزون المتكامل"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt
echo ""

# Check if database exists
if [ ! -f "erp_system.db" ]; then
    echo "Initializing database..."
    flask init-db
    echo ""
fi

# Start the application
echo "Starting the application..."
echo ""
echo "========================================"
echo "Application is running on http://localhost:5000"
echo "Username: admin"
echo "Password: admin123"
echo "========================================"
echo ""
python run.py

