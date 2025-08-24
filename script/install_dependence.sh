#!/bin/bash
# Install dependencies for Network Admin Tool

echo "Installing Python dependencies..."
pip install -r ../requirements.txt

# Check if nmap is installed
if ! command -v nmap &> /dev/null; then
    echo "nmap is not installed. Please install nmap:"
    echo "  Ubuntu/Debian: sudo apt-get install nmap"
    echo "  CentOS/RHEL: sudo yum install nmap"
    echo "  macOS: brew install nmap"
    echo "  Windows: Download from https://nmap.org/download.html"
fi

# Check if Scapy dependencies are installed
if python -c "import scapy" 2>/dev/null; then
    echo "Scapy is installed correctly."
else
    echo "Scapy may require additional dependencies:"
    echo "  Ubuntu/Debian: sudo apt-get install tcpdump"
    echo "  CentOS/RHEL: sudo yum install tcpdump"
    echo "  macOS: brew install libdnet"
fi

echo "Installation complete."