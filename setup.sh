#!/bin/bash

echo "========================================"
echo "Password Hygiene Checker - Setup"
echo "========================================"
echo ""

if [ -d "venv" ]; then
    echo "Virtual environment already exists."
    echo "Skipping venv creation..."
else
    echo "Creating virtual environment..."
    python3 -m venv venv
    
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment."
        echo "Please make sure Python is installed and in your PATH."
        exit 1
    fi
fi

echo ""
echo "Activating virtual environment..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "Error: Failed to activate virtual environment."
    exit 1
fi

echo ""
echo "Upgrading pip..."
python -m pip install --upgrade pip

echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies."
    exit 1
fi

echo ""
echo "========================================"
echo "Setup complete!"
echo "========================================"
echo ""
echo "To run the application, use:"
echo "  ./run.sh"
echo ""
echo "Or manually activate and run:"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""

