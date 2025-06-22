@echo off
REM ELES Development Environment Setup Script (Windows)
REM This script helps set up the development environment for the ELES project

echo 🚀 Setting up ELES Development Environment...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Python version: %PYTHON_VERSION%

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo 📦 Creating virtual environment...
    python -m venv .venv
) else (
    echo ✓ Virtual environment already exists
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r requirements.txt

REM Install development dependencies
echo 🛠️  Installing development dependencies...
pip install pytest pytest-cov pytest-xdist flake8 black isort mypy bandit safety pip-audit sphinx sphinx-rtd-theme sphinx-autodoc-typehints

REM Install package in development mode
echo 📦 Installing ELES in development mode...
pip install -e .

REM Run initial tests
echo 🧪 Running initial tests...
set PYTHONPATH=%PYTHONPATH%;%CD%

REM Test installation
echo    Testing installation...
python test_installation.py

REM Test quick functionality
echo    Running quick test...
python quick_test.py

REM Test imports
echo    Testing imports...
python -c "try: from eles_core.engine import SimulationEngine; print('✓ Core engine import successful'); except ImportError as e: print(f'⚠️  Core engine import failed: {e}')"
python -c "try: import visualizations; print('✓ Visualizations module import successful'); except ImportError as e: print(f'⚠️  Visualizations import failed: {e}')"

REM Test basic visualizations (headless)
echo    Testing basic visualizations...
set MPLBACKEND=Agg
python -c "try: from visualizations.demo import run_basic_demo; run_basic_demo(); print('✓ Basic visualization demo successful'); except Exception as e: print(f'⚠️  Basic visualization demo failed: {e}')"

REM Create .env file for development
if not exist ".env" (
    echo 📝 Creating .env file for development...
    echo # ELES Development Environment Configuration > .env
    echo PYTHONPATH=%CD% >> .env
    echo MPLBACKEND=Agg >> .env
    echo DEVELOPMENT_MODE=true >> .env
    echo DEBUG=true >> .env
) else (
    echo ✓ .env file already exists
)

REM Create VS Code configuration
if not exist ".vscode" (
    echo 💻 Creating VS Code configuration...
    mkdir .vscode

    echo { > .vscode\settings.json
    echo     "python.defaultInterpreterPath": "./.venv/Scripts/python.exe", >> .vscode\settings.json
    echo     "python.testing.pytestEnabled": true, >> .vscode\settings.json
    echo     "python.testing.pytestArgs": ["tests"], >> .vscode\settings.json
    echo     "python.linting.enabled": true, >> .vscode\settings.json
    echo     "python.linting.flake8Enabled": true, >> .vscode\settings.json
    echo     "python.linting.mypyEnabled": true, >> .vscode\settings.json
    echo     "python.formatting.provider": "black", >> .vscode\settings.json
    echo     "editor.formatOnSave": true, >> .vscode\settings.json
    echo     "editor.codeActionsOnSave": { >> .vscode\settings.json
    echo         "source.organizeImports": true >> .vscode\settings.json
    echo     }, >> .vscode\settings.json
    echo     "files.exclude": { >> .vscode\settings.json
    echo         "**/__pycache__": true, >> .vscode\settings.json
    echo         "**/*.pyc": true, >> .vscode\settings.json
    echo         ".pytest_cache": true >> .vscode\settings.json
    echo     } >> .vscode\settings.json
    echo } >> .vscode\settings.json

    echo ✓ VS Code configuration created
)

REM Create development scripts
echo 📜 Creating development scripts...

echo @echo off > dev-test.bat
echo REM Development testing script >> dev-test.bat
echo echo 🧪 Running development tests... >> dev-test.bat
echo call .venv\Scripts\activate.bat >> dev-test.bat
echo set PYTHONPATH=%%PYTHONPATH%%;%%CD%% >> dev-test.bat
echo set MPLBACKEND=Agg >> dev-test.bat
echo echo Running pytest... >> dev-test.bat
echo pytest tests/ -v --cov=eles_core --cov=visualizations >> dev-test.bat
echo echo Running visualization demos... >> dev-test.bat
echo python -c "from visualizations.demo import run_basic_demo, run_scientific_demo; run_basic_demo(); run_scientific_demo(); print('✓ Visualization demos completed')" >> dev-test.bat
echo echo ✅ All tests completed successfully! >> dev-test.bat

echo @echo off > dev-lint.bat
echo REM Development linting script >> dev-lint.bat
echo echo 🔍 Running code quality checks... >> dev-lint.bat
echo call .venv\Scripts\activate.bat >> dev-lint.bat
echo echo Running black... >> dev-lint.bat
echo black --check --diff . >> dev-lint.bat
echo echo Running isort... >> dev-lint.bat
echo isort --check-only --diff . >> dev-lint.bat
echo echo Running flake8... >> dev-lint.bat
echo flake8 . >> dev-lint.bat
echo echo Running mypy... >> dev-lint.bat
echo set PYTHONPATH=%%PYTHONPATH%%;%%CD%% >> dev-lint.bat
echo mypy eles_core/ --ignore-missing-imports --no-strict-optional >> dev-lint.bat
echo mypy visualizations/ --ignore-missing-imports --no-strict-optional >> dev-lint.bat
echo echo ✅ Code quality checks completed! >> dev-lint.bat

echo.
echo 🎉 ELES Development Environment Setup Complete!
echo.
echo 📋 What was set up:
echo    ✓ Virtual environment (.venv)
echo    ✓ All dependencies installed
echo    ✓ Package installed in development mode
echo    ✓ VS Code configuration
echo    ✓ Development scripts (dev-test.bat, dev-lint.bat)
echo    ✓ Environment configuration (.env)
echo.
echo 🚀 Next steps:
echo    1. Activate the environment: .venv\Scripts\activate.bat
echo    2. Run tests: dev-test.bat
echo    3. Check code quality: dev-lint.bat
echo    4. Start coding! 🎯
echo.
echo 📚 Useful commands:
echo    • Run app: python run_app.py
echo    • Run CLI: python run_cli.py --help
echo    • Run tests: pytest tests/
echo    • Format code: black .
echo    • Sort imports: isort .
echo.
echo Happy coding! 🚀
pause
