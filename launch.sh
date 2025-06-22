#!/bin/bash

# E.L.E.S. Launch Script
echo "🌍 Welcome to E.L.E.S. - Extinction-Level Event Simulator"
echo "=================================================="

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check Python version
python_version=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "🐍 Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
else
    echo "❌ Failed to install dependencies. Please check the error messages above."
    exit 1
fi

# Ask user what they want to run
echo ""
echo "What would you like to run?"
echo "1. 🌐 Web Interface (Streamlit)"
echo "2. 💻 Command Line Interface"
echo "3. 🧪 Run Tests"
echo "4. 📖 Show Help"

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo "🚀 Starting Streamlit web interface..."
        streamlit run ui/streamlit_app.py
        ;;
    2)
        echo "💻 Starting CLI interface..."
        echo "Example: python cli/main.py asteroid --diameter 2 --density 8000 --velocity 20"
        echo "For help: python cli/main.py --help"
        ;;
    3)
        echo "🧪 Running tests..."
        python -m pytest tests/ -v
        ;;
    4)
        echo "📖 E.L.E.S. Help"
        echo ""
        echo "Web Interface:"
        echo "  streamlit run ui/streamlit_app.py"
        echo ""
        echo "CLI Examples:"
        echo "  python cli/main.py asteroid --diameter 2 --density 8000 --velocity 20"
        echo "  python cli/main.py pandemic --r0 3.5 --mortality 0.05"
        echo "  python cli/main.py supervolcano --name Yellowstone --vei 8"
        echo ""
        echo "For more help: python cli/main.py --help"
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac
