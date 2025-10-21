#!/bin/bash

echo "==================================="
echo "PCA Backend Server Startup Script"
echo "==================================="
echo

# Get the directory where the script is located
cd "$(dirname "$0")"
echo "Current directory: $(pwd)"
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment."
        echo "Make sure Python 3 is installed and in your PATH."
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment."
    exit 1
fi

# Install required packages
echo "Installing required packages..."
pip install -r Requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install packages from Requirements.txt"
    echo "Installing packages directly..."
    pip install Flask Flask-CORS PyJWT python-dotenv Werkzeug numpy pandas scikit-learn matplotlib Pillow openpyxl plotly
fi

echo
echo "Starting Flask server..."
python app.py
