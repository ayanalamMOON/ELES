#!/usr/bin/env python3
"""
Quick test script to verify E.L.E.S. installation and basic functionality.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import core modules at module level
try:
    from eles_core.engine import Engine
    from eles_core.extinction_result import ExtinctionResult
    from eles_core.event_types.asteroid import AsteroidImpact
    from eles_core.event_types.supervolcano import Supervolcano
    from eles_core.event_types.pandemic import Pandemic
    IMPORTS_AVAILABLE = True
except ImportError as import_error:
    IMPORTS_AVAILABLE = False
    IMPORT_ERROR = import_error

def test_imports():
    """Test that all core modules can be imported."""
    print("🔧 Testing imports...")

    if IMPORTS_AVAILABLE:
        print("✅ All core modules imported successfully!")
        return True
    else:
        print(f"❌ Import error: {IMPORT_ERROR}")
        return False

def test_asteroid_simulation():
    """Test basic asteroid simulation."""
    print("\n☄️ Testing asteroid simulation...")

    if not IMPORTS_AVAILABLE:
        print("❌ Cannot test - imports failed")
        return False

    try:
        engine = Engine()
        result = engine.run_simulation('asteroid', {
            'diameter_km': 1.0,
            'density_kg_m3': 3000,
            'velocity_km_s': 20.0
        })

        print(f"   Severity: {result.severity}/6")
        print(f"   Casualties: {getattr(result, 'estimated_casualties', 0):,}")
        print("✅ Asteroid simulation successful!")
        return True
    except Exception as e:
        print(f"❌ Asteroid simulation failed: {e}")
        return False

def test_pandemic_simulation():
    """Test basic pandemic simulation."""
    print("\n🦠 Testing pandemic simulation...")

    if not IMPORTS_AVAILABLE:
        print("❌ Cannot test - imports failed")
        return False

    try:
        engine = Engine()
        result = engine.run_simulation('pandemic', {
            'r0': 2.5,
            'mortality_rate': 0.02
        })

        print(f"   Severity: {result.severity}/6")
        print(f"   Total Infected: {result.simulation_data.get('total_infected', 0):,}")
        print("✅ Pandemic simulation successful!")
        return True
    except Exception as e:
        print(f"❌ Pandemic simulation failed: {e}")
        return False

def test_file_structure():
    """Test that required files and directories exist."""
    print("\n📁 Testing file structure...")

    required_paths = [
        "config/settings.yaml",
        "data/scenarios/default.yaml",
        "eles_core/engine.py",
        "ui/streamlit_app.py",
        "cli/main.py"
    ]

    missing_files = []
    for path in required_paths:
        if not os.path.exists(path):
            missing_files.append(path)

    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files present!")
        return True

def main():
    """Run all tests."""
    print("🧪 E.L.E.S. Quick Test Suite")
    print("=" * 40)

    tests = [
        test_file_structure,
        test_imports,
        test_asteroid_simulation,
        test_pandemic_simulation
    ]

    passed = 0
    failed = 0

    for test in tests:
        if test():
            passed += 1
        else:
            failed += 1

    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed} passed, {failed} failed")

    if failed == 0:
        print("🎉 All tests passed! E.L.E.S. is ready to use.")
        print("\nTo get started:")
        print("  🌐 Web interface: streamlit run ui/streamlit_app.py")
        print("  💻 CLI interface: python cli/main.py --help")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
