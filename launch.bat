@echo off
REM E.L.E.S. Launch Script for Windows

echo 🌍 Welcome to E.L.E.S. - Extinction-Level Event Simulator
echo ==================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Show Python version
for /f "tokens=2" %%i in ('python --version') do echo 🐍 Python version: %%i

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo 📦 Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Failed to install dependencies. Please check the error messages above.
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully!

REM Ask user what they want to run
echo.
echo What would you like to run?
echo 1. 🌐 Web Interface (Streamlit)
echo 2. 💻 Command Line Interface
echo 3. 🧪 Run Tests
echo 4. 📖 Show Help

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo 🚀 Starting Streamlit web interface...
    streamlit run ui/streamlit_app.py
) else if "%choice%"=="2" (
    echo 💻 Starting CLI interface...
    echo Example: python cli/main.py asteroid --diameter 2 --density 8000 --velocity 20
    echo For help: python cli/main.py --help
    cmd /k
) else if "%choice%"=="3" (
    echo 🧪 Running tests...
    python -m pytest tests/ -v
    pause
) else if "%choice%"=="4" (
    echo 📖 E.L.E.S. Help
    echo.
    echo Web Interface:
    echo   streamlit run ui/streamlit_app.py
    echo.
    echo CLI Examples:
    echo   python cli/main.py asteroid --diameter 2 --density 8000 --velocity 20
    echo   python cli/main.py pandemic --r0 3.5 --mortality 0.05
    echo   python cli/main.py supervolcano --name Yellowstone --vei 8
    echo.
    echo For more help: python cli/main.py --help
    pause
) else (
    echo ❌ Invalid choice. Please run the script again.
    pause
)
