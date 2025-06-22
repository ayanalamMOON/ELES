@echo off
REM Installation script for E.L.E.S. (Extinction-Level Event Simulator) on Windows

echo 🌍 Installing E.L.E.S. - Extinction-Level Event Simulator
echo ==================================================

REM Check Python version
python --version

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
pip install --upgrade pip

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Install package in development mode
echo Installing E.L.E.S. package...
pip install -e .

REM Run tests
echo Running installation tests...
python test_installation.py

echo.
echo 🎉 Installation complete!
echo.
echo To run E.L.E.S.:
echo 1. Activate the virtual environment: .venv\Scripts\activate.bat
echo 2. Run the CLI: python run_cli.py asteroid --diameter 2
echo 3. Run the web app: python run_app.py
echo.
echo Example commands:
echo   python run_cli.py asteroid --diameter 10 --density 3000 --velocity 20
echo   python run_cli.py pandemic --r0 3.5 --mortality 0.05
echo   python run_cli.py supervolcano --name Yellowstone --vei 8

pause
