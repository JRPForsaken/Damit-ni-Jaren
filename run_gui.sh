#!/bin/bash

echo "========================================"
echo " AI Clothing Photo Sorter - GUI"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "Starting GUI application..."
echo ""

python3 gui.py

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Failed to start the application"
    echo ""
    echo "Please make sure all dependencies are installed:"
    echo "  pip3 install -r requirements.txt"
    echo ""
    read -p "Press Enter to continue..."
fi
