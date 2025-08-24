#!/bin/bash
# Build script for Network Admin Tool

echo "Building Network Admin Tool..."

# Create distribution directory if it doesn't exist
mkdir -p ../dist

# Create executable with PyInstaller if available
if command -v pyinstaller &> /dev/null; then
    echo "Creating executable with PyInstaller..."
    pyinstaller --onefile --windowed ../src/main.py -n NetworkAdminTool
    echo "Executable created in dist/ directory"
else
    echo "PyInstaller not found. Creating simple package..."
    cp -r ../src ../dist/NetworkAdminTool
    cp ../requirements.txt ../dist/NetworkAdminTool/
    echo "Package created in dist/NetworkAdminTool directory"
fi

echo "Build complete."