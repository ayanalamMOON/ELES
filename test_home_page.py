#!/usr/bin/env python3
"""
Test script for the advanced home page
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_home_page_import():
    """Test if the home page can be imported successfully."""
    try:
        from ui.pages.home import run
        print("✅ Home page imported successfully!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_dependencies():
    """Test if all required dependencies are available."""
    dependencies = [
        'streamlit',
        'pandas',
        'plotly',
        'numpy',
        'pathlib'
    ]

    missing = []
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - Missing")
            missing.append(dep)

    return len(missing) == 0

def test_core_components():
    """Test if core E.L.E.S. components are accessible."""
    try:
        from eles_core.engine import Engine
        from config.constants import SEVERITY_LEVELS, SEVERITY_COLORS
        from eles_core.event_types import (
            AsteroidImpact, Supervolcano, ClimateCollapse,
            Pandemic, GammaRayBurst, AIExtinction
        )
        print("✅ All core components accessible!")
        return True
    except ImportError as e:
        print(f"❌ Core component import error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Advanced Home Page Components\n")

    print("📦 Testing Dependencies:")
    deps_ok = test_dependencies()

    print("\n🔧 Testing Core Components:")
    core_ok = test_core_components()

    print("\n🏠 Testing Home Page Import:")
    home_ok = test_home_page_import()

    print(f"\n{'='*50}")
    if deps_ok and core_ok and home_ok:
        print("🎉 All tests passed! The advanced home page is ready to use.")
        print("\nTo run the application:")
        print("1. streamlit run ui/pages/home.py")
        print("2. Or use: python run_app.py")
    else:
        print("⚠️  Some tests failed. Please check the error messages above.")
        if not deps_ok:
            print("- Install missing dependencies with: pip install -r requirements.txt")
        if not core_ok:
            print("- Check that the E.L.E.S. core modules are properly configured")
