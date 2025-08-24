#!/bin/bash
# Script to run Network Admin Tool with appropriate privileges

echo "Network Admin Tool - Privilege Helper"
echo "====================================="

# Check if we're on Linux/macOS
if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected Linux/macOS system"
    
    # Check if already root
    if [ "$EUID" -eq 0 ]; then
        echo "Already running as root, starting application..."
        python3 src/main.py
    else
        echo "Requesting sudo privileges..."
        sudo python3 src/main.py
    fi

# Check if we're on Windows
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "Detected Windows system"
    echo "Please run the application as Administrator from Command Prompt:"
    echo "python src\main.py"
    read -p "Press Enter to continue trying without admin privileges..."
    python src/main.py
else
    echo "Unknown operating system. Trying to run without elevated privileges..."
    python3 src/main.py
fi