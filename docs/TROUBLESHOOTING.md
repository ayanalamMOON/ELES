# E.L.E.S. Troubleshooting Guide

This guide helps you resolve common issues when installing, running, or using the Extinction-Level Event Simulator (E.L.E.S.).

## 🚨 Quick Fixes

### ⚡ Common Issues - Try These First

1. **Restart the application** - Close and reopen the Streamlit app
2. **Refresh your browser** - Press F5 or Ctrl+R
3. **Check your internet connection** - Some visualizations may need external resources
4. **Ensure Python 3.8+** - Run `python --version` to check
5. **Update your browser** - Use a modern browser (Chrome, Firefox, Safari, Edge)

## 🔧 Installation Issues

### Python Version Problems

**Problem**: `E.L.E.S. requires Python 3.8 or higher`

**Solutions**:

```bash
# Check your Python version
python --version
python3 --version

# If using conda
conda install python=3.8

# If using pyenv
pyenv install 3.8.0
pyenv local 3.8.0
```

### Package Installation Failures

**Problem**: `pip install` fails with permission errors

**Solutions**:

```bash
# Use virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate    # Windows
source .venv/bin/activate # macOS/Linux

# Install with user flag
pip install --user -r requirements.txt

# Use conda instead
conda install --file requirements.txt
```

**Problem**: `No module named 'eles_core'`

**Solutions**:

```bash
# Install in development mode
pip install -e .

# Add to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"  # Linux/macOS
set PYTHONPATH=%PYTHONPATH%;%CD%         # Windows

# Run from project root directory
cd /path/to/ELES
python ui/streamlit_app.py
```

### Missing Dependencies

**Problem**: `ModuleNotFoundError: No module named 'streamlit'`

**Solutions**:

```bash
# Install missing packages
pip install streamlit
pip install -r requirements.txt

# Check if in correct environment
which python
pip list | grep streamlit
```

**Problem**: Visualization errors with matplotlib

**Solutions**:

```bash
# Install with conda (better for matplotlib)
conda install matplotlib

# Set backend for headless systems
export MPLBACKEND=Agg

# Update matplotlib
pip install --upgrade matplotlib
```

## 🌐 Web Interface Issues

### Streamlit App Won't Start

**Problem**: `streamlit: command not found`

**Solutions**:

```bash
# Check if streamlit is installed
pip show streamlit

# Install streamlit
pip install streamlit

# Run with python module
python -m streamlit run ui/streamlit_app.py

# Check PATH
echo $PATH  # Linux/macOS
echo %PATH% # Windows
```

**Problem**: App starts but shows errors

**Solutions**:

1. **Check the terminal output** for specific error messages
2. **Verify all imports** are working:

   ```bash
   python -c "from eles_core.engine import Engine; print('OK')"
   ```

3. **Run the test script**:

   ```bash
   python test_installation.py
   ```

### Browser Connection Issues

**Problem**: Cannot access <http://localhost:8501>

**Solutions**:

1. **Check if port is in use**:

   ```bash
   # Windows
   netstat -an | findstr 8501

   # Linux/macOS
   lsof -i :8501
   ```

2. **Use different port**:

   ```bash
   streamlit run ui/streamlit_app.py --server.port 8502
   ```

3. **Check firewall settings** - Allow Python/Streamlit through firewall

4. **Try different browser** - Use incognito/private mode

**Problem**: App loads but visualizations don't appear

**Solutions**:

1. **Disable ad blockers** - They may block chart rendering
2. **Enable JavaScript** - Required for interactive plots
3. **Clear browser cache** - Remove old cached files
4. **Check browser console** - Press F12, look for errors

### Performance Issues

**Problem**: App is slow or unresponsive

**Solutions**:

1. **Close other browser tabs** - Free up memory
2. **Restart the Streamlit server**
3. **Check system resources** - Monitor CPU and memory usage
4. **Use smaller parameter values** for testing
5. **Disable real-time updates** temporarily

## 📊 Simulation Issues

### Parameter Validation Errors

**Problem**: `ValueError: Invalid parameter range`

**Solutions**:

1. **Check parameter limits**:
   - Asteroid diameter: 0.01 - 50 km
   - Pandemic R₀: 0.5 - 10.0
   - Mortality rate: 0.1% - 50%
   - VEI: 4 - 8
   - Temperature change: -20°C to +20°C
   - GRB distance: 100 - 10,000 light-years
   - AI level: 1 - 10

2. **Use preset scenarios** first to verify functionality

3. **Check input format** - Ensure numbers, not text

**Problem**: Simulation returns zero casualties

**Solutions**:

1. **Increase parameter severity** - Use larger/more extreme values
2. **Check event type selection** - Ensure correct event is selected
3. **Verify parameter mapping** - Run validation test:

   ```bash
   python test_casualty_calculations.py
   ```

### Calculation Errors

**Problem**: `Mathematical error in calculations`

**Solutions**:

1. **Check for extreme values** that might cause overflow
2. **Use realistic parameter ranges**
3. **Report the issue** with specific parameters used

**Problem**: Inconsistent results

**Solutions**:

1. **Verify same parameters** are being used
2. **Check for random seed issues** (rare)
3. **Restart the application** to clear any cached state

## 🎨 Visualization Problems

### Charts Not Displaying

**Problem**: Blank visualization tabs

**Solutions**:

1. **Check matplotlib installation**:

   ```bash
   python -c "import matplotlib.pyplot as plt; print('OK')"
   ```

2. **Test visualization demo**:

   ```bash
   python visualizations/demo.py
   ```

3. **Set proper backend**:

   ```bash
   export MPLBACKEND=Agg     # For headless
   export MPLBACKEND=TkAgg   # For GUI
   ```

4. **Update graphics drivers** (for 3D visualizations)

**Problem**: Visualization errors in console

**Solutions**:

1. **Install missing packages**:

   ```bash
   pip install plotly seaborn networkx
   ```

2. **Downgrade problematic packages** if needed:

   ```bash
   pip install matplotlib==3.5.0
   ```

### Interactive Features Not Working

**Problem**: Can't zoom or pan charts

**Solutions**:

1. **Enable JavaScript** in browser
2. **Use supported browser** (Chrome, Firefox recommended)
3. **Check plotly installation**:

   ```bash
   pip install --upgrade plotly
   ```

## 💻 Command Line Interface Issues

### CLI Commands Fail

**Problem**: `python cli/main.py` not found

**Solutions**:

```bash
# Run from project root
cd /path/to/ELES

# Check file exists
ls cli/main.py

# Use absolute path
python /full/path/to/ELES/cli/main.py

# Add to PATH
export PATH="${PATH}:/path/to/ELES/cli"
```

**Problem**: CLI parameter errors

**Solutions**:

1. **Check help text**:

   ```bash
   python cli/main.py --help
   python cli/main.py asteroid --help
   ```

2. **Use proper syntax**:

   ```bash
   # Correct
   python cli/main.py asteroid --diameter 2.0 --density 3000

   # Incorrect
   python cli/main.py asteroid diameter=2.0
   ```

## 🧪 Testing and Validation

### Test Scripts Fail

**Problem**: `test_installation.py` reports errors

**Solutions**:

1. **Read error messages carefully** - They indicate specific issues
2. **Fix imports first**:

   ```bash
   pip install -e .
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```

3. **Run individual tests**:

   ```bash
   python test_casualty_calculations.py
   python test_streamlit_scenarios.py
   ```

**Problem**: Validation tests fail

**Solutions**:

1. **Check Python environment** is properly set up
2. **Verify all dependencies** are installed
3. **Run quick test first**:

   ```bash
   python quick_test.py
   ```

## 🔍 Debugging Tips

### Getting More Information

1. **Enable debug mode**:

   ```bash
   export DEBUG=true
   streamlit run ui/streamlit_app.py
   ```

2. **Check log files** in the `.streamlit/logs/` directory

3. **Use verbose output**:

   ```bash
   python -v cli/main.py asteroid --diameter 1
   ```

### Common Error Messages

| Error Message | Likely Cause | Solution |
|---------------|--------------|----------|
| `ImportError: No module named...` | Missing dependency | `pip install <module>` |
| `FileNotFoundError: config/settings.yaml` | Wrong directory | Run from project root |
| `ValueError: Invalid parameter` | Parameter out of range | Check parameter limits |
| `ConnectionError` | Network/port issue | Check firewall/port |
| `MemoryError` | Insufficient RAM | Use smaller datasets |

### System-Specific Issues

#### Windows

- **Use `python` instead of `python3`**
- **Activate virtual environment**: `.venv\Scripts\activate.bat`
- **Check Windows Defender** isn't blocking files
- **Use PowerShell or Command Prompt** instead of Git Bash for some commands

#### macOS

- **Use `python3` explicitly**
- **Install Xcode command line tools**: `xcode-select --install`
- **Check Homebrew Python** vs system Python conflicts
- **Set PYTHONPATH** in shell profile (.bashrc, .zshrc)

#### Linux

- **Install system dependencies**:

  ```bash
  sudo apt-get install python3-dev python3-pip python3-venv
  ```

- **Check permissions** on project directory
- **Use virtual environment** to avoid system package conflicts

## 📞 Getting Additional Help

### Before Reporting Issues

1. **Update to latest version** of E.L.E.S.
2. **Try in a fresh virtual environment**
3. **Check existing issues** on the project repository
4. **Gather system information**:

   ```bash
   python --version
   pip --version
   pip list
   ```

### Reporting Bugs

When reporting issues, include:

1. **Operating System** (Windows 10, macOS Big Sur, Ubuntu 20.04, etc.)
2. **Python version** (`python --version`)
3. **E.L.E.S. version**
4. **Full error message** (copy from terminal)
5. **Steps to reproduce** the issue
6. **Expected vs actual behavior**

### Community Resources

- **Project Repository**: Check issues and discussions
- **Documentation**: Complete guides in `docs/` folder
- **Stack Overflow**: Tag with `eles` and `extinction-simulator`
- **Reddit**: `/r/Python` community for general Python issues

### Emergency Recovery

If E.L.E.S. is completely broken:

```bash
# Nuclear option: Fresh install
rm -rf .venv/
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

---

## ✅ Prevention Tips

### Best Practices

1. **Always use virtual environments**
2. **Keep requirements.txt updated**
3. **Test after major changes**
4. **Backup your custom scenarios**
5. **Read error messages carefully**
6. **Update regularly but carefully**
7. **Document your custom configurations**

### Performance Optimization

1. **Close unused browser tabs**
2. **Use appropriate parameter ranges**
3. **Monitor system resources**
4. **Clear cache periodically**
5. **Restart app after heavy use**

Remember: Most issues have simple solutions. Take your time, read error messages carefully, and don't hesitate to ask for help!
