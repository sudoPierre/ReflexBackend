#!/bin/bash

# 1. Check if python3 is installed
if ! command -v python3 &> /dev/null; then
  echo "Python3 is not installed."

  # Try to detect package manager and install python3
  if command -v apt &> /dev/null; then
    echo "Installing python3 using apt..."
    sudo apt update && sudo apt install -y python3 python3-venv
  elif command -v dnf &> /dev/null; then
    echo "Installing python3 using dnf..."
    sudo dnf install -y python3 python3-venv
  elif command -v pacman &> /dev/null; then
    echo "Installing python3 using pacman..."
    sudo pacman -Sy python
  else
    echo "Could not determine package manager. Please install Python 3 manually."
    exit 1
  fi
fi

# 2. Check if the venv module is available
if ! python3 -m venv --help &> /dev/null; then
  echo "'venv' module is missing. Attempting to install..."
  if command -v apt &> /dev/null; then
    sudo apt install -y python3.10-venv
  else
    echo "Please install the 'python3-venv' package manually."
    exit 1
  fi
fi

# 3. Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi

# 4. Activate the virtual environment
source venv/bin/activate

# 5. Install dependencies from requirements.txt
pip install -r requirements.txt

# 6. Run the Python script in the background and save its PID
echo "Starting webhook-reloader..."
touch starter.log
sudo chmod 644 starter.log
nohup python3 main.py > starter.log 2>&1 &
echo $! > starter.pid
echo "webhook-reloader started (PID $(cat starter.pid))"