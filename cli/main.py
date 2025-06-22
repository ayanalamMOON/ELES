import argparse
import sys
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from eles_core.engine import Engine
from config.constants import SEVERITY_LEVELS


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='E.L.E.S. - Extinction-Level Event Simulator CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli/main.py asteroid --diameter 2 --density 8000 --velocity 20
  python cli/main.py pandemic --r0 3.5 --mortality 0.05
  python cli/main.py supervolcano --name Yellowstone --vei 8
        """
    )

    parser.add_argument('event_type',
                       choices=['asteroid', 'supervolcano', 'pandemic', 'gamma_ray_burst', 'climate_collapse', 'ai_extinction'],
                       help='Type of extinction event to simulate')

    parser.add_argument('--output', '-o',
                       help='Output file for results (JSON format)')

    parser.add_argument('--verbose', '-v',
                       action='store_true',
                       help='Verbose output')

    # Asteroid-specific arguments
    asteroid_group = parser.add_argument_group('asteroid', 'Asteroid impact parameters')
    asteroid_group.add_argument('--diameter', type=float, default=1.0,
                               help='Asteroid diameter in km (default: 1.0)')
    asteroid_group.add_argument('--density', type=float, default=3000,
                               help='Asteroid density in kg/m³ (default: 3000)')
    asteroid_group.add_argument('--velocity', type=float, default=20.0,
                               help='Impact velocity in km/s (default: 20.0)')
    asteroid_group.add_argument('--target', choices=['continental', 'ocean', 'urban'], default='continental',
                               help='Impact target type (default: continental)')

    # Supervolcano-specific arguments
    volcano_group = parser.add_argument_group('supervolcano', 'Supervolcano parameters')
    volcano_group.add_argument('--name', default='Custom',
                              help='Volcano name (default: Custom)')
    volcano_group.add_argument('--vei', type=int, default=6,
                              help='Volcanic Explosivity Index (default: 6)')

    # Pandemic-specific arguments
    pandemic_group = parser.add_argument_group('pandemic', 'Pandemic parameters')
    pandemic_group.add_argument('--r0', type=float, default=2.5,
                               help='Basic reproduction number (default: 2.5)')
    pandemic_group.add_argument('--mortality', type=float, default=0.02,
                               help='Mortality rate (default: 0.02)')

    # Other event arguments
    other_group = parser.add_argument_group('other', 'Other event parameters')
    other_group.add_argument('--distance', type=float, default=1000,
                            help='Distance for gamma-ray burst in light-years (default: 1000)')
    other_group.add_argument('--temperature', type=float, default=-5.0,
                            help='Temperature change for climate collapse in °C (default: -5.0)')
    other_group.add_argument('--ai-level', type=int, default=5,
                            help='AI capability level for AI extinction (default: 5)')

    args = parser.parse_args()

    try:
        # Create parameters based on event type
        if args.event_type == 'asteroid':
            parameters = {
                'diameter_km': args.diameter,
                'density_kg_m3': args.density,
                'velocity_km_s': args.velocity,
                'target_type': args.target
            }
        elif args.event_type == 'supervolcano':
            parameters = {
                'name': args.name,
                'vei': args.vei
            }
        elif args.event_type == 'pandemic':
            parameters = {
                'r0': args.r0,
                'mortality_rate': args.mortality
            }
        elif args.event_type == 'gamma_ray_burst':
            parameters = {
                'distance_ly': args.distance
            }
        elif args.event_type == 'climate_collapse':
            parameters = {
                'temperature_change_c': args.temperature
            }
        elif args.event_type == 'ai_extinction':
            parameters = {
                'ai_level': args.ai_level
            }

        # Run simulation
        engine = Engine()
        result = engine.run_simulation(args.event_type, parameters)

        # Display results
        display_results(result, args.verbose)

        # Save to file if requested
        if args.output:
            save_results(result, args.output)
            print(f"\n✅ Results saved to: {args.output}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


def display_results(result, verbose=False):
    """Display simulation results to console."""
    print("\n" + "="*60)
    print(f"🌍 E.L.E.S. SIMULATION RESULTS")
    print("="*60)

    # Basic information
    print(f"Event Type: {result.event_type.replace('_', ' ').title()}")
    print(f"Severity: {result.severity}/6 - {result.get_severity_description()}")

    # Key metrics
    casualties = getattr(result, 'estimated_casualties', 0)
    economic_impact = getattr(result, 'economic_impact', 0)
    recovery_time = result.get_recovery_time_estimate()

    print(f"\n📊 KEY METRICS:")
    print(f"├─ Estimated Casualties: {casualties:,}")
    print(f"├─ Economic Impact: ${economic_impact:.1f} billion USD")
    print(f"├─ Recovery Time: {recovery_time}")
    print(f"└─ Impacted Area: {result.impacted_area:,.0f} km²")

    # Event-specific details
    if result.event_type == 'asteroid':
        display_asteroid_details(result)
    elif result.event_type == 'pandemic':
        display_pandemic_details(result)
    elif result.event_type == 'supervolcano':
        display_supervolcano_details(result)

    # Risk factors
    risk_factors = result.get_risk_factors()
    if risk_factors:
        print(f"\n⚠️ RISK FACTORS:")
        for i, factor in enumerate(risk_factors, 1):
            print(f"{i}. {factor}")

    # Verbose output
    if verbose:
        print(f"\n🔍 DETAILED DATA:")
        for key, value in result.simulation_data.items():
            if isinstance(value, (int, float)):
                if isinstance(value, float):
                    print(f"├─ {key}: {value:.3e}")
                else:
                    print(f"├─ {key}: {value:,}")
            else:
                print(f"├─ {key}: {value}")


def display_asteroid_details(result):
    """Display asteroid-specific details."""
    sim_data = result.simulation_data

    print(f"\n☄️ ASTEROID IMPACT DETAILS:")
    print(f"├─ Diameter: {sim_data.get('diameter_km', 0)} km")
    print(f"├─ Mass: {sim_data.get('mass_kg', 0):.2e} kg")
    print(f"├─ Impact Energy: {sim_data.get('impact_energy', 0):.2e} J")
    print(f"├─ TNT Equivalent: {sim_data.get('tnt_equivalent_mt', 0):.1f} megatons")
    print(f"├─ Crater Diameter: {sim_data.get('crater_diameter_km', 0):.1f} km")
    print(f"├─ Earthquake Magnitude: {sim_data.get('earthquake_magnitude', 0):.1f}")

    if 'blast_radius_severe_km' in sim_data:
        print(f"└─ Severe Blast Radius: {sim_data['blast_radius_severe_km']:.1f} km")


def display_pandemic_details(result):
    """Display pandemic-specific details."""
    sim_data = result.simulation_data

    print(f"\n🦠 PANDEMIC DETAILS:")
    print(f"├─ R₀: {sim_data.get('r0', 0)}")
    print(f"├─ Mortality Rate: {sim_data.get('mortality_rate', 0):.1%}")
    print(f"├─ Total Infected: {sim_data.get('total_infected', 0):,}")
    print(f"├─ Peak Infected: {sim_data.get('peak_infected', 0):,}")
    print(f"├─ Duration: {sim_data.get('epidemic_duration_days', 0)} days")
    print(f"└─ Healthcare Stress: {sim_data.get('healthcare_system_stress', 0):.1f}/10")


def display_supervolcano_details(result):
    """Display supervolcano-specific details."""
    sim_data = result.simulation_data

    print(f"\n🌋 SUPERVOLCANO DETAILS:")
    print(f"├─ Volcano: {sim_data.get('volcano_name', 'Unknown')}")
    print(f"├─ VEI: {sim_data.get('vei', 0)}")
    print(f"├─ Magma Volume: {sim_data.get('magma_volume_km3', 0)} km³")
    print(f"├─ Ash Cloud Height: {sim_data.get('ash_cloud_height_km', 0)} km")
    print(f"├─ Temperature Drop: {sim_data.get('temperature_drop_c', 0)}°C")
    print(f"└─ Cooling Duration: {sim_data.get('cooling_duration_years', 0)} years")


def save_results(result, filename):
    """Save results to JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(result.to_json())


if __name__ == '__main__':
    main()
