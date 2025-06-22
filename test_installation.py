#!/usr/bin/env python3
"""
Test script for E.L.E.S. project to verify installation and basic functionality.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all core modules can be imported."""
    print("Testing imports...")

    try:
        from eles_core.engine import Engine
        print("✅ Engine import successful")
    except Exception as e:
        print(f"❌ Engine import failed: {e}")
        return False

    try:
        from eles_core.extinction_result import ExtinctionResult
        print("✅ ExtinctionResult import successful")
    except Exception as e:
        print(f"❌ ExtinctionResult import failed: {e}")
        return False

    try:
        from eles_core.event_types.asteroid import AsteroidImpact
        from eles_core.event_types.supervolcano import Supervolcano
        from eles_core.event_types.pandemic import Pandemic
        print("✅ Event types import successful")
    except Exception as e:
        print(f"❌ Event types import failed: {e}")
        return False

    return True

def test_basic_simulation():
    """Test basic simulation functionality."""
    print("\nTesting basic simulation...")

    try:
        from eles_core.engine import Engine

        # Initialize engine
        engine = Engine()
        print("✅ Engine initialization successful")

        # Test asteroid simulation
        result = engine.run_simulation('asteroid', {
            'diameter_km': 1.0,
            'density_kg_m3': 3000,
            'velocity_km_s': 20.0
        })

        print(f"✅ Asteroid simulation successful - Severity: {result.severity}")

        # Test pandemic simulation
        result = engine.run_simulation('pandemic', {
            'r0': 2.5,
            'mortality_rate': 0.02
        })

        print(f"✅ Pandemic simulation successful - Severity: {result.severity}")

        return True

    except Exception as e:
        print(f"❌ Simulation test failed: {e}")
        return False

def test_cli():
    """Test CLI functionality."""
    print("\nTesting CLI...")

    try:
        from cli.main import main
        print("✅ CLI module import successful")
        return True
    except Exception as e:
        print(f"❌ CLI test failed: {e}")
        return False

def test_streamlit_app():
    """Test Streamlit app import."""
    print("\nTesting Streamlit app...")

    try:
        # Check if streamlit is available
        import streamlit as st
        print("✅ Streamlit available")

        # Try importing the app (may fail due to missing dependencies)
        try:
            from ui.streamlit_app import main
            print("✅ Streamlit app import successful")
        except ImportError as e:
            print(f"⚠️ Streamlit app import failed (may need dependencies): {e}")

        return True
    except ImportError:
        print("⚠️ Streamlit not installed - web interface unavailable")
        return True

def main():
    """Run all tests."""
    print("🌍 E.L.E.S. Test Suite")
    print("=" * 50)

    tests = [
        test_imports,
        test_basic_simulation,
        test_cli,
        test_streamlit_app
    ]

    passed = 0
    for test in tests:
        if test():
            passed += 1

    print("\n" + "=" * 50)
    print(f"Tests passed: {passed}/{len(tests)}")

    if passed == len(tests):
        print("🎉 All tests passed! E.L.E.S. is ready to use.")
        print("\nTo run the application:")
        print("- CLI: python run_cli.py asteroid --diameter 2 --density 8000")
        print("- Web: python run_app.py")
    else:
        print("⚠️ Some tests failed. Check dependencies and installation.")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
