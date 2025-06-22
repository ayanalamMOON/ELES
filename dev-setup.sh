#!/bin/bash

# ELES Development Environment Setup Script
# This script helps set up the development environment for the ELES project

set -e

echo "🚀 Setting up ELES Development Environment..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✓ Python version: $PYTHON_VERSION"

if ! python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo "❌ Python 3.8+ is required. Current version: $PYTHON_VERSION"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Install development dependencies
echo "🛠️  Installing development dependencies..."
pip install \
    pytest \
    pytest-cov \
    pytest-xdist \
    flake8 \
    black \
    isort \
    mypy \
    bandit \
    safety \
    pip-audit \
    sphinx \
    sphinx-rtd-theme \
    sphinx-autodoc-typehints

# Install package in development mode
echo "📦 Installing ELES in development mode..."
pip install -e .

# Run initial tests
echo "🧪 Running initial tests..."
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Test installation
echo "   Testing installation..."
python test_installation.py

# Test quick functionality
echo "   Running quick test..."
python quick_test.py

# Test imports
echo "   Testing imports..."
python -c "
try:
    from eles_core.engine import SimulationEngine
    print('✓ Core engine import successful')
except ImportError as e:
    print(f'⚠️  Core engine import failed: {e}')

try:
    import visualizations
    print('✓ Visualizations module import successful')
except ImportError as e:
    print(f'⚠️  Visualizations import failed: {e}')
"

# Test basic visualizations (headless)
echo "   Testing basic visualizations..."
export MPLBACKEND=Agg
python -c "
try:
    from visualizations.demo import run_basic_demo
    run_basic_demo()
    print('✓ Basic visualization demo successful')
except Exception as e:
    print(f'⚠️  Basic visualization demo failed: {e}')
"

# Create .env file for development
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file for development..."
    cat > .env << EOF
# ELES Development Environment Configuration
PYTHONPATH=\$(pwd)
MPLBACKEND=Agg
DEVELOPMENT_MODE=true
DEBUG=true
EOF
else
    echo "✓ .env file already exists"
fi

# Create pre-commit configuration
if [ ! -f ".pre-commit-config.yaml" ]; then
    echo "🔧 Creating pre-commit configuration..."
    cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=127, --extend-ignore=E203,W503]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.1
    hooks:
      - id: mypy
        args: [--ignore-missing-imports, --no-strict-optional]
        additional_dependencies: [types-PyYAML, types-requests]
EOF

    # Install pre-commit hooks
    pip install pre-commit
    pre-commit install
    echo "✓ Pre-commit hooks installed"
else
    echo "✓ Pre-commit configuration already exists"
fi

# Setup IDE configuration for VS Code
if [ ! -d ".vscode" ]; then
    echo "💻 Creating VS Code configuration..."
    mkdir -p .vscode

    cat > .vscode/settings.json << EOF
{
    "python.defaultInterpreterPath": "./.venv/bin/python",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": [
        "tests"
    ],
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    },
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        ".pytest_cache": true
    }
}
EOF

    cat > .vscode/launch.json << EOF
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Run ELES App",
            "type": "python",
            "request": "launch",
            "program": "run_app.py",
            "console": "integratedTerminal",
            "env": {
                "PYTHONPATH": "\${workspaceFolder}"
            }
        },
        {
            "name": "Run ELES CLI",
            "type": "python",
            "request": "launch",
            "program": "run_cli.py",
            "console": "integratedTerminal",
            "args": ["--help"],
            "env": {
                "PYTHONPATH": "\${workspaceFolder}"
            }
        },
        {
            "name": "Debug Tests",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": ["tests/", "-v"],
            "console": "integratedTerminal",
            "env": {
                "PYTHONPATH": "\${workspaceFolder}"
            }
        }
    ]
}
EOF
    echo "✓ VS Code configuration created"
fi

# Create development scripts
echo "📜 Creating development scripts..."

cat > dev-test.sh << 'EOF'
#!/bin/bash
# Development testing script
set -e

echo "🧪 Running development tests..."

# Activate virtual environment
source .venv/bin/activate

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
export MPLBACKEND=Agg

# Run tests
echo "Running pytest..."
pytest tests/ -v --cov=eles_core --cov=visualizations

echo "Running visualization demos..."
python -c "
from visualizations.demo import run_basic_demo, run_scientific_demo
run_basic_demo()
run_scientific_demo()
print('✓ Visualization demos completed')
"

echo "✅ All tests completed successfully!"
EOF

cat > dev-lint.sh << 'EOF'
#!/bin/bash
# Development linting script
set -e

echo "🔍 Running code quality checks..."

# Activate virtual environment
source .venv/bin/activate

echo "Running black..."
black --check --diff .

echo "Running isort..."
isort --check-only --diff .

echo "Running flake8..."
flake8 .

echo "Running mypy..."
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
mypy eles_core/ --ignore-missing-imports --no-strict-optional
mypy visualizations/ --ignore-missing-imports --no-strict-optional

echo "Running bandit..."
bandit -r eles_core/ visualizations/ -f json -o bandit-report.json || true

echo "✅ Code quality checks completed!"
EOF

chmod +x dev-test.sh dev-lint.sh

echo ""
echo "🎉 ELES Development Environment Setup Complete!"
echo ""
echo "📋 What was set up:"
echo "   ✓ Virtual environment (.venv)"
echo "   ✓ All dependencies installed"
echo "   ✓ Package installed in development mode"
echo "   ✓ Pre-commit hooks configured"
echo "   ✓ VS Code configuration"
echo "   ✓ Development scripts (dev-test.sh, dev-lint.sh)"
echo "   ✓ Environment configuration (.env)"
echo ""
echo "🚀 Next steps:"
echo "   1. Activate the environment: source .venv/bin/activate"
echo "   2. Run tests: ./dev-test.sh"
echo "   3. Check code quality: ./dev-lint.sh"
echo "   4. Start coding! 🎯"
echo ""
echo "📚 Useful commands:"
echo "   • Run app: python run_app.py"
echo "   • Run CLI: python run_cli.py --help"
echo "   • Run tests: pytest tests/"
echo "   • Format code: black ."
echo "   • Sort imports: isort ."
echo ""
echo "Happy coding! 🚀"
