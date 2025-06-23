#!/usr/bin/env python3
"""
Launch script for the E.L.E.S. Advanced Home Page
"""

import sys
import os
from pathlib import Path

def main():
    """Main launcher function."""
    print("🌍 E.L.E.S. Advanced Home Page Launcher")
    print("=" * 50)

    # Set up the project path
    project_root = Path(__file__).parent
    os.chdir(project_root)

    print(f"📁 Project Root: {project_root}")
    print(f"📂 Working Directory: {os.getcwd()}")

    # Test imports
    print("\n🔍 Testing Dependencies...")
    try:
        import streamlit as st
        print("✅ Streamlit")

        import pandas as pd
        print("✅ Pandas")

        import plotly.express as px
        print("✅ Plotly Express")

        import plotly.graph_objects as go
        print("✅ Plotly Graph Objects")

        import numpy as np
        print("✅ NumPy")

    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install requirements with: pip install -r requirements.txt")
        return False

    # Test E.L.E.S. core components
    print("\n🔧 Testing E.L.E.S. Components...")
    try:
        from eles_core.engine import Engine
        print("✅ Engine")

        from config.constants import SEVERITY_LEVELS, SEVERITY_COLORS
        print("✅ Constants")

        from eles_core.event_types import (
            AsteroidImpact, Supervolcano, ClimateCollapse,
            Pandemic, GammaRayBurst, AIExtinction
        )
        print("✅ Event Types")

    except ImportError as e:
        print(f"❌ E.L.E.S. component error: {e}")
        return False

    # Test home page
    print("\n🏠 Testing Home Page...")
    try:
        from ui.pages.home import run
        print("✅ Home page loaded successfully!")

        # Test that functions are defined
        import inspect
        home_module = sys.modules['ui.pages.home']
        functions = [name for name, obj in inspect.getmembers(home_module, inspect.isfunction)]
        print(f"✅ Functions defined: {', '.join(functions)}")

    except Exception as e:
        print(f"❌ Home page error: {e}")
        import traceback
        traceback.print_exc()
        return False

    print("\n🚀 Launch Options:")
    print("1. streamlit run ui/pages/home.py")
    print("2. python run_app.py (if main app exists)")
    print("\n✨ All systems ready!")

    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Launch successful! Use the commands above to start the application.")
    else:
        print("\n❌ Launch failed. Please fix the errors above.")
        sys.exit(1)
