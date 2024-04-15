#!/bin/bash

if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed."
    exit 1
else
    echo "Python is installed."
fi

# Make python virtual environment
echo "Creating python virtual environment"
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment"
source venv/bin/activate

# Install required packages
echo "Installing required python packages"
pip install -r requirements.txt

# Run app
echo "Starting SmartSpend"
python app.py