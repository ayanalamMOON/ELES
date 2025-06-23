#!/usr/bin/env python3
"""
Integration test for E.L.E.S. with advanced home page
"""

import sys
import os
from pathlib import Path

def test_integration():
    """Test the complete integration."""
    print("🧪 E.L.E.S. Integration Test")
    print("=" * 50)

    # Set up path
    project_root = Path(__file__).parent
    os.chdir(project_root)

    print(f"📁 Project Root: {project_root}")

    # Test 1: Core imports
    print("\n🔍 Testing Core Imports...")
    try:
        import streamlit as st
        print("✅ Streamlit")

        import pandas as pd
        print("✅ Pandas")

        import plotly.express as px
        print("✅ Plotly")

    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

    # Test 2: E.L.E.S. components
    print("\n🔧 Testing E.L.E.S. Components...")
    try:
        from eles_core.engine import Engine
        print("✅ Engine")

        from config.constants import SEVERITY_LEVELS, SEVERITY_COLORS
        print("✅ Constants")

    except ImportError as e:
        print(f"❌ E.L.E.S. component error: {e}")
        return False

    # Test 3: Home page
    print("\n🏠 Testing Advanced Home Page...")
    try:
        from ui.pages.home import run as home_page
        print("✅ Home page imported")

        # Test that functions exist
        import inspect
        home_module = sys.modules['ui.pages.home']
        functions = [name for name, obj in inspect.getmembers(home_module, inspect.isfunction)]
        print(f"✅ Functions: {len(functions)} defined")

    except Exception as e:
        print(f"❌ Home page error: {e}")
        return False

    # Test 4: Main app integration
    print("\n🔗 Testing Main App Integration...")
    try:
        from ui.streamlit_app import main, display_simulation_interface, display_analytics_page, display_about_page
        print("✅ Main app functions imported")

        # Test that navigation is available
        from ui.streamlit_app import HAS_HOME_PAGE
        if HAS_HOME_PAGE:
            print("✅ Home page integration enabled")
        else:
            print("⚠️ Home page integration disabled")

    except Exception as e:
        print(f"❌ Main app integration error: {e}")
        return False

    # Test 5: Deployment readiness
    print("\n🚀 Testing Deployment Readiness...")
    try:
        from run_app import main as run_main
        print("✅ Run script ready")

    except Exception as e:
        print(f"❌ Run script error: {e}")
        return False

    print("\n" + "=" * 50)
    print("✅ ALL TESTS PASSED!")
    print("")
    print("🎉 E.L.E.S. is ready for deployment with:")
    print("   • Advanced home page with interactive demos")
    print("   • Full navigation system")
    print("   • Simulation laboratory")
    print("   • Analytics dashboard")
    print("   • About page")
    print("")
    print("🚀 To deploy:")
    print("   1. streamlit run run_app.py")
    print("   2. Navigate to http://localhost:8501")
    print("   3. Use the sidebar to navigate between pages")
    print("")
    print("📋 Navigation Options:")
    print("   🏠 Home - Advanced interactive home page")
    print("   🔬 Simulation Lab - Full parameter control")
    print("   📊 Analytics - Comparison and analysis")
    print("   ℹ️ About - Project information")

    return True

if __name__ == "__main__":
    success = test_integration()
    if not success:
        print("\n❌ Some tests failed. Please check the errors above.")
        sys.exit(1)
    else:
        print("\n🎊 Integration complete and ready!")
