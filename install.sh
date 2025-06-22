#!/bin/bash

# Installation script for E.L.E.S. (Extinction-Level Event Simulator)

echo "🌍 Installing E.L.E.S. - Extinction-Level Event Simulator"
echo "=================================================="

# Check Python version
python_version=$(python --version 2>&1)
echo "Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Install package in development mode
echo "Installing E.L.E.S. package..."
pip install -e .

# Run tests
echo "Running installation tests..."
python test_installation.py

echo ""
echo "🎉 Installation complete!"
echo ""
echo "To run E.L.E.S.:"
echo "1. Activate the virtual environment:"
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "   source .venv/Scripts/activate"
else
    echo "   source .venv/bin/activate"
fi
echo "2. Run the CLI: python run_cli.py asteroid --diameter 2"
echo "3. Run the web app: python run_app.py"
echo ""
echo "Example commands:"
echo "  python run_cli.py asteroid --diameter 10 --density 3000 --velocity 20"
echo "  python run_cli.py pandemic --r0 3.5 --mortality 0.05"
echo "  python run_cli.py supervolcano --name Yellowstone --vei 8"
