#!/bin/bash
echo "Installing Your Software on Linux..."

# Step 1: Install Python (if not already installed)
if ! command -v python3 &>/dev/null; then
    echo "Installing Python..."
    sudo apt-get update
    sudo apt-get install -y python3
fi

# Step 2: Install pip (if not already installed)
if ! command -v pip3 &>/dev/null; then
    echo "Installing pip..."
    sudo apt-get install -y python3-pip
fi

# Step 3: Install required packages
echo "Installing required Python packages..."
pip3 install -r requirements.txt

# Step 4: Create desktop shortcut (if using a GUI)
# Note: Linux desktop environments vary; this is a general example
if [ -n "$XDG_CURRENT_DESKTOP" ]; then
    echo "Creating desktop shortcut..."
    cp your_shortcut.desktop ~/Desktop/
fi

echo "Installation complete!"
