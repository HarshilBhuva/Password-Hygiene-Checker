#!/bin/bash

if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please run ./setup.sh first to create the virtual environment."
    exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "Error: Failed to activate virtual environment."
    exit 1
fi

echo ""
echo "Starting Password Hygiene Checker..."
echo "Server will be available at: http://localhost:5000"
echo "Press Ctrl+C to stop the server."
echo ""
python app.py

