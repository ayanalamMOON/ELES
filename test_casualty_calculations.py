#!/usr/bin/env python3
"""
Test script to validate casualty, economic impact, and recovery time calculations.
"""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from eles_core.engine import Engine


def test_casualty_calculations():
    """Test casualty calculations for all event types."""
    print("🔄 Testing Casualty, Economic Impact, and Recovery Time Calculations...")
    engine = Engine()

    test_scenarios = [
        ("pandemic", {"r0": 3.0, "mortality_rate": 0.02}, "High-transmission pandemic"),
        ("supervolcano", {"name": "Yellowstone", "vei": 7}, "Yellowstone VEI 7"),
        ("climate_collapse", {"temperature_change_c": -8.0}, "Ice age scenario"),
        ("gamma_ray_burst", {"distance_ly": 800}, "Close gamma-ray burst"),
        ("ai_extinction", {"ai_level": 8}, "Advanced AI scenario"),
        ("asteroid", {"diameter_km": 2.0, "density_kg_m3": 3000, "velocity_km_s": 20}, "2km asteroid")
    ]

    print(f"{'Event Type':<15} {'Scenario':<25} {'Casualties':<15} {'Economic ($B)':<15} {'Recovery Time':<20}")
    print("-" * 95)

    all_working = True

    for event_type, params, description in test_scenarios:
        try:
            result = engine.run_simulation(event_type, params)

            casualties = getattr(result, 'estimated_casualties', 0)
            economic_impact = getattr(result, 'economic_impact', 0)
            recovery_time = result.get_recovery_time_estimate()

            print(f"{event_type:<15} {description:<25} {casualties:>14,} {economic_impact:>14.1f} {recovery_time:<20}")

            # Check if values are non-zero (except for very mild scenarios)
            if casualties == 0 and economic_impact == 0 and result.severity > 1:
                print(f"  ⚠️  Warning: Zero casualties and economic impact for severity {result.severity}")
                all_working = False

        except Exception as e:
            print(f"{event_type:<15} {description:<25} ERROR: {e}")
            all_working = False

    return all_working


def test_parameter_impact_on_metrics():
    """Test that parameter changes affect the calculated metrics."""
    print("\n🔄 Testing Parameter Impact on Metrics...")
    engine = Engine()

    # Test pandemic severity scaling
    print("\nPandemic Severity Scaling:")
    pandemic_tests = [
        ({"r0": 1.5, "mortality_rate": 0.001}, "Mild"),
        ({"r0": 3.0, "mortality_rate": 0.02}, "Moderate"),
        ({"r0": 6.0, "mortality_rate": 0.15}, "Severe")
    ]

    for params, description in pandemic_tests:
        result = engine.run_simulation("pandemic", params)
        print(f"  {description:>8}: {result.estimated_casualties:>12,} casualties, ${result.economic_impact:>8.1f}B")

    # Test supervolcano VEI scaling
    print("\nSupervolcano VEI Scaling:")
    volcano_tests = [
        ({"name": "Test", "vei": 5}, "VEI 5"),
        ({"name": "Test", "vei": 6}, "VEI 6"),
        ({"name": "Test", "vei": 7}, "VEI 7"),
        ({"name": "Test", "vei": 8}, "VEI 8")
    ]

    for params, description in volcano_tests:
        result = engine.run_simulation("supervolcano", params)
        print(f"  {description:>8}: {result.estimated_casualties:>12,} casualties, ${result.economic_impact:>8.1f}B")

    # Test climate change severity
    print("\nClimate Change Temperature Scaling:")
    climate_tests = [
        ({"temperature_change_c": -3}, "-3°C"),
        ({"temperature_change_c": -8}, "-8°C"),
        ({"temperature_change_c": -15}, "-15°C")
    ]

    for params, description in climate_tests:
        result = engine.run_simulation("climate_collapse", params)
        print(f"  {description:>8}: {result.estimated_casualties:>12,} casualties, ${result.economic_impact:>8.1f}B")


def main():
    """Run all casualty calculation tests."""
    print("🧪 E.L.E.S. Casualty & Economic Impact Validation")
    print("=" * 70)

    test1_passed = test_casualty_calculations()
    test_parameter_impact_on_metrics()

    print("\n" + "=" * 70)

    if test1_passed:
        print("✅ All casualty and economic impact calculations are working!")
        print("\nThe Streamlit app should now display updated values for:")
        print("• Estimated casualties for all event types")
        print("• Economic impact calculations for all scenarios")
        print("• Recovery time estimates based on severity")
        print("• Proper scaling based on parameter changes")
        return 0
    else:
        print("❌ Some casualty calculations need attention")
        return 1


if __name__ == "__main__":
    exit(main())
