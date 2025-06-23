# Installation Guide

This guide will help you install and set up the **Extinction-Level Event Simulator (E.L.E.S.)** on your system.

## 🔧 System Requirements

### Minimum Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 1GB free space

### Recommended Requirements

- **Python**: 3.10 or higher
- **RAM**: 16GB for large simulations
- **Storage**: 2GB free space

## 📦 Installation Methods

### Method 1: Quick Install (Recommended)

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-org/ELES.git
   cd ELES
   ```

2. **Run the install script**:

   **Windows:**

   ```batch
   install.bat
   ```

   **macOS/Linux:**

   ```bash
   chmod +x install.sh
   ./install.sh
   ```

3. **Launch the application**:

   **Windows:**

   ```batch
   launch.bat
   ```

   **macOS/Linux:**

   ```bash
   ./launch.sh
   ```

### Method 2: Manual Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-org/ELES.git
   cd ELES
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**:

   **Windows:**

   ```batch
   .venv\Scripts\activate
   ```

   **macOS/Linux:**

   ```bash
   source .venv/bin/activate
   ```

4. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Install E.L.E.S. in development mode**:

   ```bash
   pip install -e .
   ```

### Method 3: Docker Installation

1. **Build the Docker image**:

   ```bash
   docker build -t eles .
   ```

2. **Run the container**:

   ```bash
   docker run -p 8501:8501 eles
   ```

3. **Access the application**:
   Open your browser to `http://localhost:8501`

## 🚀 Verification

### Test Installation

Run the quick test to verify everything is working:

```bash
python quick_test.py
```

Expected output:

```
✅ E.L.E.S. Installation Test
==========================
✅ Python version: 3.x.x
✅ Core modules imported successfully
✅ Simulation engine functional
✅ Visualization modules available
✅ All tests passed!
```

### Launch Applications

#### Streamlit Web App

```bash
streamlit run ui/streamlit_app.py
```

Then open `http://localhost:8501` in your browser.

#### Command Line Interface

```bash
python run_cli.py --help
```

#### Python API

```python
from eles_core.engine import Engine

engine = Engine()
result = engine.run_simulation('asteroid', {'diameter_km': 1.0})
print(f"Severity: {result.severity}")
```

## 🔧 Troubleshooting

### Common Issues

#### Issue: ModuleNotFoundError

**Symptoms**: Python can't find E.L.E.S. modules

**Solutions**:

1. Ensure virtual environment is activated
2. Run `pip install -e .` in the project root
3. Check Python path includes project directory

#### Issue: Streamlit app won't start

**Symptoms**: Error when running `streamlit run`

**Solutions**:

1. Install Streamlit: `pip install streamlit`
2. Check port availability: Try `--server.port 8502`
3. Update dependencies: `pip install -r requirements.txt --upgrade`

#### Issue: Visualization errors

**Symptoms**: Charts don't display or crash

**Solutions**:

1. Install visualization dependencies: `pip install matplotlib plotly`
2. Update graphics drivers
3. Try different browser

#### Issue: Permission errors (Windows)

**Symptoms**: Scripts won't execute

**Solutions**:

1. Run Command Prompt as Administrator
2. Set execution policy: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned`
3. Use PowerShell instead of Command Prompt

### Getting Help

If you encounter issues:

1. Check the [FAQ](FAQ.md)
2. Review the [Troubleshooting Guide](TROUBLESHOOTING.md)
3. Search existing issues on GitHub
4. Create a new issue with:
   - Your operating system
   - Python version
   - Error messages
   - Steps to reproduce

## 📋 Post-Installation Setup

### Optional Configuration

1. **Configure settings** (optional):
   Edit `config/settings.yaml` to customize default parameters

2. **Add custom scenarios** (optional):
   Place custom scenario files in `data/scenarios/`

3. **Set environment variables** (optional):

   ```bash
   export ELES_CONFIG_PATH=/path/to/custom/config
   export ELES_DATA_PATH=/path/to/custom/data
   ```

### Performance Optimization

1. **For large simulations**:
   - Increase system RAM
   - Use SSD storage
   - Close unnecessary applications

2. **For development**:
   - Install development dependencies: `pip install -e .[dev]`
   - Set up pre-commit hooks: `pre-commit install`

## ✅ Next Steps

After successful installation:

1. **Read the [Quick Start Guide](QUICK_START.md)** to run your first simulation
2. **Explore the [Streamlit App Guide](STREAMLIT_APP_GUIDE.md)** for web interface usage
3. **Check out [Event Types](EVENT_TYPES.md)** to understand available simulations
4. **Review [API Reference](API_REFERENCE.md)** for programmatic usage

---

**Congratulations! E.L.E.S. is now installed and ready to use.** 🎉
