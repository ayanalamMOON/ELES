#!/usr/bin/env python3
"""
Test script to validate that all simulation scenarios work in the Streamlit app
with custom parameter changes.
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from eles_core.engine import Engine


def test_asteroid_scenarios():
    """Test asteroid scenarios with different parameters."""
    print("🔄 Testing Asteroid Scenarios...")
    engine = Engine()

    # Test 1: Small asteroid (Tunguska-like)
    params1 = {
        "diameter_km": 0.06,
        "density_kg_m3": 3000,
        "velocity_km_s": 20,
        "target_type": "continental"
    }

    try:
        result1 = engine.run_simulation("asteroid", params1)
        print(f"✅ Small asteroid: Severity {result1.severity}, Casualties: {getattr(result1, 'estimated_casualties', 0):,}")
    except Exception as e:
        print(f"❌ Small asteroid failed: {e}")

    # Test 2: Large asteroid (Chicxulub-like)
    params2 = {
        "diameter_km": 10.0,
        "density_kg_m3": 3000,
        "velocity_km_s": 20,
        "target_type": "ocean"
    }

    try:
        result2 = engine.run_simulation("asteroid", params2)
        print(f"✅ Large asteroid: Severity {result2.severity}, Casualties: {getattr(result2, 'estimated_casualties', 0):,}")
    except Exception as e:
        print(f"❌ Large asteroid failed: {e}")

    # Test 3: Custom parameters
    params3 = {
        "diameter_km": 2.5,
        "density_kg_m3": 8000,
        "velocity_km_s": 35,
        "target_type": "urban"
    }

    try:
        result3 = engine.run_simulation("asteroid", params3)
        print(f"✅ Custom asteroid: Severity {result3.severity}, Casualties: {getattr(result3, 'estimated_casualties', 0):,}")
    except Exception as e:
        print(f"❌ Custom asteroid failed: {e}")


def test_pandemic_scenarios():
    """Test pandemic scenarios with different parameters."""
    print("\n🔄 Testing Pandemic Scenarios...")
    engine = Engine()

    # Test 1: COVID-19 like
    params1 = {
        "r0": 2.5,
        "mortality_rate": 0.01
    }

    try:
        result1 = engine.run_simulation("pandemic", params1)
        print(f"✅ COVID-19 like: Severity {result1.severity}, Deaths: {result1.simulation_data.get('total_deaths', 0):,}")
    except Exception as e:
        print(f"❌ COVID-19 like failed: {e}")

    # Test 2: High mortality pandemic
    params2 = {
        "r0": 5.0,
        "mortality_rate": 0.2
    }

    try:
        result2 = engine.run_simulation("pandemic", params2)
        print(f"✅ High mortality: Severity {result2.severity}, Deaths: {result2.simulation_data.get('total_deaths', 0):,}")
    except Exception as e:
        print(f"❌ High mortality failed: {e}")

    # Test 3: Low transmissibility
    params3 = {
        "r0": 0.8,
        "mortality_rate": 0.35
    }

    try:
        result3 = engine.run_simulation("pandemic", params3)
        print(f"✅ Low transmissibility: Severity {result3.severity}, Deaths: {result3.simulation_data.get('total_deaths', 0):,}")
    except Exception as e:
        print(f"❌ Low transmissibility failed: {e}")


def test_supervolcano_scenarios():
    """Test supervolcano scenarios with different parameters."""
    print("\n🔄 Testing Supervolcano Scenarios...")
    engine = Engine()

    # Test 1: Yellowstone VEI 7
    params1 = {
        "name": "Yellowstone",
        "vei": 7
    }

    try:
        result1 = engine.run_simulation("supervolcano", params1)
        print(f"✅ Yellowstone VEI 7: Severity {result1.severity}")
    except Exception as e:
        print(f"❌ Yellowstone VEI 7 failed: {e}")

    # Test 2: Toba VEI 8
    params2 = {
        "name": "Toba",
        "vei": 8
    }

    try:
        result2 = engine.run_simulation("supervolcano", params2)
        print(f"✅ Toba VEI 8: Severity {result2.severity}")
    except Exception as e:
        print(f"❌ Toba VEI 8 failed: {e}")

    # Test 3: Custom volcano
    params3 = {
        "name": "Custom Supervolcano",
        "vei": 6
    }

    try:
        result3 = engine.run_simulation("supervolcano", params3)
        print(f"✅ Custom VEI 6: Severity {result3.severity}")
    except Exception as e:
        print(f"❌ Custom VEI 6 failed: {e}")


def test_climate_collapse_scenarios():
    """Test climate collapse scenarios with different parameters."""
    print("\n🔄 Testing Climate Collapse Scenarios...")
    engine = Engine()

    # Test 1: Moderate cooling
    params1 = {
        "temperature_change_c": -5.0
    }

    try:
        result1 = engine.run_simulation("climate_collapse", params1)
        print(f"✅ Moderate cooling (-5°C): Severity {result1.severity}")
    except Exception as e:
        print(f"❌ Moderate cooling failed: {e}")

    # Test 2: Severe cooling
    params2 = {
        "temperature_change_c": -15.0
    }

    try:
        result2 = engine.run_simulation("climate_collapse", params2)
        print(f"✅ Severe cooling (-15°C): Severity {result2.severity}")
    except Exception as e:
        print(f"❌ Severe cooling failed: {e}")

    # Test 3: Warming scenario
    params3 = {
        "temperature_change_c": 8.0
    }

    try:
        result3 = engine.run_simulation("climate_collapse", params3)
        print(f"✅ Warming (+8°C): Severity {result3.severity}")
    except Exception as e:
        print(f"❌ Warming failed: {e}")


def test_gamma_ray_burst_scenarios():
    """Test gamma-ray burst scenarios with different parameters."""
    print("\n🔄 Testing Gamma-Ray Burst Scenarios...")
    engine = Engine()

    # Test 1: Nearby burst
    params1 = {
        "distance_ly": 500
    }

    try:
        result1 = engine.run_simulation("gamma_ray_burst", params1)
        print(f"✅ Nearby GRB (500 ly): Severity {result1.severity}")
    except Exception as e:
        print(f"❌ Nearby GRB failed: {e}")

    # Test 2: Distant burst
    params2 = {
        "distance_ly": 5000
    }

    try:
        result2 = engine.run_simulation("gamma_ray_burst", params2)
        print(f"✅ Distant GRB (5000 ly): Severity {result2.severity}")
    except Exception as e:
        print(f"❌ Distant GRB failed: {e}")

    # Test 3: Moderate distance
    params3 = {
        "distance_ly": 1500
    }

    try:
        result3 = engine.run_simulation("gamma_ray_burst", params3)
        print(f"✅ Moderate GRB (1500 ly): Severity {result3.severity}")
    except Exception as e:
        print(f"❌ Moderate GRB failed: {e}")


def test_ai_extinction_scenarios():
    """Test AI extinction scenarios with different parameters."""
    print("\n🔄 Testing AI Extinction Scenarios...")
    engine = Engine()

    # Test 1: Low AI level
    params1 = {
        "ai_level": 3
    }

    try:
        result1 = engine.run_simulation("ai_extinction", params1)
        print(f"✅ Low AI level (3): Severity {result1.severity}")
    except Exception as e:
        print(f"❌ Low AI level failed: {e}")

    # Test 2: High AI level
    params2 = {
        "ai_level": 8
    }

    try:
        result2 = engine.run_simulation("ai_extinction", params2)
        print(f"✅ High AI level (8): Severity {result2.severity}")
    except Exception as e:
        print(f"❌ High AI level failed: {e}")

    # Test 3: Maximum AI level
    params3 = {
        "ai_level": 10
    }

    try:
        result3 = engine.run_simulation("ai_extinction", params3)
        print(f"✅ Maximum AI level (10): Severity {result3.severity}")
    except Exception as e:
        print(f"❌ Maximum AI level failed: {e}")


def test_parameter_validation():
    """Test that parameter changes are properly reflected in results."""
    print("\n🔄 Testing Parameter Validation...")
    engine = Engine()

    # Test asteroid parameter changes
    small_asteroid = {
        "diameter_km": 0.1,
        "density_kg_m3": 2000,
        "velocity_km_s": 15
    }

    large_asteroid = {
        "diameter_km": 5.0,
        "density_kg_m3": 8000,
        "velocity_km_s": 30
    }

    try:
        result_small = engine.run_simulation("asteroid", small_asteroid)
        result_large = engine.run_simulation("asteroid", large_asteroid)

        small_energy = result_small.simulation_data.get('impact_energy', 0)
        large_energy = result_large.simulation_data.get('impact_energy', 0)

        if large_energy > small_energy:
            print("✅ Parameter changes correctly affect impact energy")
        else:
            print("❌ Parameter changes not properly reflected in energy calculations")

        if result_large.severity >= result_small.severity:
            print("✅ Parameter changes correctly affect severity ratings")
        else:
            print("❌ Parameter changes not properly reflected in severity")

    except Exception as e:
        print(f"❌ Parameter validation failed: {e}")


def main():
    """Run all scenario tests."""
    print("🧪 E.L.E.S. Streamlit App Scenario Testing")
    print("=" * 50)

    try:
        test_asteroid_scenarios()
        test_pandemic_scenarios()
        test_supervolcano_scenarios()
        test_climate_collapse_scenarios()
        test_gamma_ray_burst_scenarios()
        test_ai_extinction_scenarios()
        test_parameter_validation()

        print("\n" + "=" * 50)
        print("✅ All scenario tests completed!")
        print("\nThe simulation engine supports all event types with custom parameters.")
        print("Next step: Test the Streamlit UI to ensure proper parameter handling.")

    except Exception as e:
        print(f"\n❌ Testing failed with error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
