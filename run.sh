#!/usr/bin/env bash
# run.sh - Linux launcher for the Grocery POS (same as run.bat on Windows)
cd "$(dirname "$0")"

# Find Python 3
PY=python3
if ! command -v python3 >/dev/null 2>&1; then
    echo "Python 3 was not found. Install it with:"
    echo "  sudo apt install python3 python3-venv python3-pip"
    read -r -p "Press Enter to close..."
    exit 1
fi

# Create the private environment on first run
if [ ! -f "venv/bin/python" ]; then
    echo "First run: creating a private Python environment..."
    "$PY" -m venv venv
fi

# Activate it
source venv/bin/activate

echo "Checking packages (fast when already installed)..."
python -m pip install --quiet --disable-pip-version-check -r requirements.txt
if [ $? -ne 0 ]; then
    echo ""
    echo "Could not install required packages."
    echo "On Kali/Debian, first run:  sudo apt install python3-venv python3-pip"
    echo "Then connect to the internet once and start again."
    read -r -p "Press Enter to close..."
    exit 1
fi

if [ ! -f "database/grocery.db" ]; then
    echo "Creating the local database with sample data..."
    python init_db.py
fi

echo ""
echo " Starting Disodi Stores POS at http://127.0.0.1:5000"
echo " Keep this window OPEN while using the system. Press Ctrl+C to stop."
echo ""
python app.py