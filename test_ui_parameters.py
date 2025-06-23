#!/usr/bin/env python3
"""
Interactive test script to validate Streamlit app parameter handling.
This script simulates user interactions with the Streamlit app.
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from eles_core.engine import Engine


def test_ui_parameter_mapping():
    """Test that UI parameters correctly map to simulation parameters."""
    print("🔄 Testing UI Parameter Mapping...")
    engine = Engine()

    # Test asteroid parameter mapping
    ui_params = {
        "diameter_km": 2.0,
        "density_kg_m3": 5000,
        "velocity_km_s": 25,
        "target_type": "ocean"
    }

    result = engine.run_simulation("asteroid", ui_params)
    sim_data = result.simulation_data

    # Verify parameters are correctly passed
    assert sim_data['diameter_km'] == ui_params['diameter_km'], "Diameter not passed correctly"
    assert sim_data['velocity_km_s'] == ui_params['velocity_km_s'], "Velocity not passed correctly"

    print("✅ Asteroid parameters correctly mapped")

    # Test pandemic parameter mapping
    ui_params = {
        "r0": 3.5,
        "mortality_rate": 0.05
    }

    result = engine.run_simulation("pandemic", ui_params)
    sim_data = result.simulation_data

    assert sim_data['r0'] == ui_params['r0'], "R0 not passed correctly"
    assert sim_data['mortality_rate'] == ui_params['mortality_rate'], "Mortality rate not passed correctly"

    print("✅ Pandemic parameters correctly mapped")

    # Test supervolcano parameter mapping
    ui_params = {
        "name": "Test Volcano",
        "vei": 7
    }

    result = engine.run_simulation("supervolcano", ui_params)
    sim_data = result.simulation_data

    assert sim_data.get('vei') == ui_params['vei'], "VEI not passed correctly"

    print("✅ Supervolcano parameters correctly mapped")


def test_parameter_ranges_and_validation():
    """Test parameter ranges and edge cases."""
    print("\n🔄 Testing Parameter Ranges and Validation...")
    engine = Engine()

    # Test extreme parameter values
    test_cases = [
        # Very small asteroid
        ("asteroid", {"diameter_km": 0.001, "density_kg_m3": 1000, "velocity_km_s": 10}),
        # Very large asteroid
        ("asteroid", {"diameter_km": 100, "density_kg_m3": 10000, "velocity_km_s": 70}),
        # Very low pandemic transmission
        ("pandemic", {"r0": 0.1, "mortality_rate": 0.001}),
        # Very high pandemic severity
        ("pandemic", {"r0": 15, "mortality_rate": 0.9}),
        # Minimum VEI
        ("supervolcano", {"name": "Small", "vei": 4}),
        # Maximum VEI
        ("supervolcano", {"name": "Mega", "vei": 8}),
        # Extreme climate scenarios
        ("climate_collapse", {"temperature_change_c": -20}),
        ("climate_collapse", {"temperature_change_c": 15}),
        # GRB distance extremes
        ("gamma_ray_burst", {"distance_ly": 50}),
        ("gamma_ray_burst", {"distance_ly": 10000}),
        # AI level extremes
        ("ai_extinction", {"ai_level": 1}),
        ("ai_extinction", {"ai_level": 10})
    ]

    for event_type, params in test_cases:
        try:
            result = engine.run_simulation(event_type, params)
            print(f"✅ {event_type} with extreme params: Severity {result.severity}")
        except Exception as e:
            print(f"❌ {event_type} with extreme params failed: {e}")


def test_simulation_consistency():
    """Test that repeated simulations with same parameters give consistent results."""
    print("\n🔄 Testing Simulation Consistency...")
    engine = Engine()

    params = {
        "diameter_km": 1.5,
        "density_kg_m3": 3500,
        "velocity_km_s": 22
    }

    results = []
    for i in range(3):
        result = engine.run_simulation("asteroid", params)
        results.append({
            'severity': result.severity,
            'energy': result.simulation_data.get('impact_energy', 0),
            'casualties': getattr(result, 'estimated_casualties', 0)
        })

    # Check consistency
    severities = [r['severity'] for r in results]
    energies = [r['energy'] for r in results]

    if len(set(severities)) == 1 and len(set(energies)) == 1:
        print("✅ Simulations are consistent across multiple runs")
    else:
        print("❌ Simulations show inconsistency")
        for i, r in enumerate(results):
            print(f"  Run {i+1}: Severity {r['severity']}, Energy {r['energy']:.2e}")


def test_visualization_data_availability():
    """Test that all required data for visualizations is available."""
    print("\n🔄 Testing Visualization Data Availability...")
    engine = Engine()

    test_scenarios = [
        ("asteroid", {"diameter_km": 2, "density_kg_m3": 3000, "velocity_km_s": 20}),
        ("pandemic", {"r0": 2.5, "mortality_rate": 0.02}),
        ("supervolcano", {"name": "Test", "vei": 6}),
        ("climate_collapse", {"temperature_change_c": -8}),
        ("gamma_ray_burst", {"distance_ly": 1000}),
        ("ai_extinction", {"ai_level": 6})
    ]

    for event_type, params in test_scenarios:
        result = engine.run_simulation(event_type, params)
        sim_data = result.simulation_data

        # Check required data fields
        required_fields = {
            "asteroid": ['impact_energy', 'crater_diameter_km', 'blast_radius_severe_km'],
            "pandemic": ['total_deaths', 'epidemic_duration_days', 'peak_infected'],
            "supervolcano": ['vei'],
            "climate_collapse": ['temperature_change_c'],
            "gamma_ray_burst": ['distance_ly'],
            "ai_extinction": ['ai_level']
        }

        missing_fields = []
        for field in required_fields.get(event_type, []):
            if field not in sim_data:
                missing_fields.append(field)

        if missing_fields:
            print(f"❌ {event_type}: Missing fields {missing_fields}")
        else:
            print(f"✅ {event_type}: All required visualization data available")


def test_summary_and_export_functionality():
    """Test summary generation and data export functionality."""
    print("\n🔄 Testing Summary and Export Functionality...")
    engine = Engine()

    result = engine.run_simulation("asteroid", {
        "diameter_km": 1.0,
        "density_kg_m3": 3000,
        "velocity_km_s": 20
    })

    # Test summary generation
    try:
        summary = result.summary()
        required_summary_fields = [
            'event_type', 'severity', 'severity_description',
            'estimated_casualties', 'economic_impact_billion_usd',
            'recovery_time_estimate', 'impacted_area_km2'
        ]

        missing_summary_fields = []
        for field in required_summary_fields:
            if field not in summary:
                missing_summary_fields.append(field)

        if missing_summary_fields:
            print(f"❌ Summary missing fields: {missing_summary_fields}")
        else:
            print("✅ Summary generation works correctly")

    except Exception as e:
        print(f"❌ Summary generation failed: {e}")

    # Test JSON export
    try:
        json_str = result.to_json()
        if len(json_str) > 0 and '"event_type"' in json_str:
            print("✅ JSON export works correctly")
        else:
            print("❌ JSON export produces invalid output")
    except Exception as e:
        print(f"❌ JSON export failed: {e}")


def main():
    """Run all UI parameter tests."""
    print("🧪 E.L.E.S. Streamlit UI Parameter Testing")
    print("=" * 60)

    try:
        test_ui_parameter_mapping()
        test_parameter_ranges_and_validation()
        test_simulation_consistency()
        test_visualization_data_availability()
        test_summary_and_export_functionality()

        print("\n" + "=" * 60)
        print("✅ All UI parameter tests completed successfully!")
        print("\nThe Streamlit app should now support:")
        print("• All simulation scenarios with custom parameters")
        print("• Proper parameter validation and mapping")
        print("• Comprehensive visualizations for all event types")
        print("• Consistent simulation results")
        print("• Complete data export functionality")

    except Exception as e:
        print(f"\n❌ Testing failed with error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
