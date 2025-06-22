"""
Visualization Examples and Demos for E.L.E.S.

This module provides examples and demonstrations of the various visualization
capabilities available in the E.L.E.S. visualization package.
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from visualizations.charts import (
        plot_severity_distribution,
        plot_energy_comparison,
        plot_damage_zones,
        plot_epidemic_curve
    )
    from visualizations.heatmaps import (
        plot_geographic_heatmap,
        plot_risk_heatmap,
        plot_correlation_heatmap
    )
    from visualizations.export import export_plots, create_report_plots
    VISUALIZATIONS_AVAILABLE = True
except ImportError as e:
    print(f"Some visualization modules not available: {e}")
    VISUALIZATIONS_AVAILABLE = False

# Advanced visualization modules
try:
    from visualizations.networks import (
        demo_infrastructure_network,
        create_infrastructure_network,
        plot_infrastructure_vulnerability
    )
    NETWORKS_AVAILABLE = True
except ImportError as e:
    print(f"Networks module not available: {e}")
    NETWORKS_AVAILABLE = False

try:
    from visualizations.scientific import (
        demo_scientific_plots,
        plot_phase_space,
        plot_monte_carlo_analysis
    )
    SCIENTIFIC_AVAILABLE = True
except ImportError as e:
    print(f"Scientific module not available: {e}")
    SCIENTIFIC_AVAILABLE = False

try:
    from visualizations.comparative import (
        demo_comparative_analysis,
        compare_scenarios_overview,
        plot_scenario_ranking,
        plot_scenario_timeline_comparison,
        plot_sensitivity_analysis
    )
    COMPARATIVE_AVAILABLE = True
except ImportError as e:
    print(f"Comparative module not available: {e}")
    COMPARATIVE_AVAILABLE = False


def demo_basic_charts():
    """Demonstrate basic chart capabilities."""
    if not VISUALIZATIONS_AVAILABLE:
        print("Visualization modules not available")
        return

    print("🎨 Demonstrating Basic Chart Capabilities")
    print("=" * 50)

    # Demo 1: Severity Distribution
    print("1. Creating severity distribution chart...")
    sample_results = [
        {'severity': 3}, {'severity': 4}, {'severity': 2},
        {'severity': 5}, {'severity': 3}, {'severity': 6},
        {'severity': 1}, {'severity': 4}, {'severity': 3}
    ]

    try:
        fig1 = plot_severity_distribution(sample_results)
        print("   ✅ Severity distribution chart created")
        plt.close(fig1)
    except Exception as e:
        print(f"   ❌ Error creating severity chart: {e}")

    # Demo 2: Energy Comparison
    print("2. Creating energy comparison chart...")
    energy_data = {
        'Tunguska (1908)': 1.2e16,
        'Chicxulub (65 Mya)': 4.2e23,
        'Tsar Bomba (1961)': 2.1e17,
        'Mt. St. Helens (1980)': 2.4e15
    }

    try:
        fig2 = plot_energy_comparison(energy_data)
        print("   ✅ Energy comparison chart created")
        plt.close(fig2)
    except Exception as e:
        print(f"   ❌ Error creating energy chart: {e}")

    # Demo 3: Damage Zones
    print("3. Creating damage zones visualization...")
    blast_radii = {
        'severe_blast': 50,
        'moderate_blast': 150,
        'light_damage': 300
    }

    try:
        fig3 = plot_damage_zones(10, blast_radii)
        print("   ✅ Damage zones chart created")
        plt.close(fig3)
    except Exception as e:
        print(f"   ❌ Error creating damage zones chart: {e}")


def demo_heatmaps():
    """Demonstrate heatmap capabilities."""
    if not VISUALIZATIONS_AVAILABLE:
        print("Visualization modules not available")
        return

    print("\n🔥 Demonstrating Heatmap Capabilities")
    print("=" * 50)

    # Demo 1: Geographic Heatmap
    print("1. Creating geographic impact heatmap...")
    impact_data = {
        'impact_location': (40.0, -100.0),
        'max_impact_radius': 200.0
    }

    try:
        fig1 = plot_geographic_heatmap(impact_data, grid_resolution=30)
        print("   ✅ Geographic heatmap created")
        plt.close(fig1)
    except Exception as e:
        print(f"   ❌ Error creating geographic heatmap: {e}")

    # Demo 2: Risk Assessment Heatmap
    print("2. Creating risk assessment heatmap...")
    risk_data = {
        'risk_matrix': [
            [4.5, 3.8, 3.2, 2.5],  # Population Density
            [3.2, 4.1, 4.5, 4.8],  # Infrastructure
            [5.0, 4.5, 3.8, 2.9],  # Economic Activity
            [2.0, 3.0, 3.5, 4.0],  # Emergency Preparedness
            [3.8, 3.9, 4.1, 4.2]   # Geographic Vulnerability
        ],
        'risk_factors': ['Population Density', 'Infrastructure', 'Economic Activity',
                        'Emergency Preparedness', 'Geographic Vulnerability'],
        'risk_categories': ['Immediate', 'Short-term', 'Medium-term', 'Long-term']
    }

    try:
        fig2 = plot_risk_heatmap(risk_data)
        print("   ✅ Risk assessment heatmap created")
        plt.close(fig2)
    except Exception as e:
        print(f"   ❌ Error creating risk heatmap: {e}")

    # Demo 3: Correlation Heatmap
    print("3. Creating correlation heatmap...")

    # Generate sample correlated data
    np.random.seed(42)
    variables = ['Severity', 'Casualties', 'Economic_Impact', 'Recovery_Time',
                'Population_Density', 'Infrastructure_Quality']

    # Create correlation matrix
    n_vars = len(variables)
    correlation_matrix = np.random.rand(n_vars, n_vars)
    correlation_matrix = (correlation_matrix + correlation_matrix.T) / 2  # Make symmetric
    np.fill_diagonal(correlation_matrix, 1)  # Perfect self-correlation

    # Convert to DataFrame
    correlation_df = pd.DataFrame(correlation_matrix,
                                 index=variables,
                                 columns=variables)

    try:
        fig3 = plot_correlation_heatmap(correlation_df)
        print("   ✅ Correlation heatmap created")
        plt.close(fig3)
    except Exception as e:
        print(f"   ❌ Error creating correlation heatmap: {e}")


def demo_export_capabilities():
    """Demonstrate export and report generation capabilities."""
    if not VISUALIZATIONS_AVAILABLE:
        print("Visualization modules not available")
        return

    print("\n📊 Demonstrating Export Capabilities")
    print("=" * 50)

    # Create sample simulation data
    simulation_data = {
        'event_type': 'asteroid',
        'severity': 4,
        'casualties': 2500000,
        'economic_impact': 1.5e12,
        'recovery_time_years': 25,
        'casualties_breakdown': [500000, 1000000, 1000000],
        'sector_impacts': [85, 70, 45, 80],
        'resource_availability': [65, 85, 35, 75, 25, 55],
        'risk_values': [4, 3, 5, 2, 3]
    }

    # Demo report generation
    print("1. Creating standardized report plots...")
    try:
        report_files = create_report_plots(simulation_data, 'asteroid', 'demo_reports')
        print(f"   ✅ Report plots created: {len(report_files)} files")
        for plot_type, filename in report_files.items():
            print(f"      - {plot_type}: {filename}")
    except Exception as e:
        print(f"   ❌ Error creating report plots: {e}")


def demo_comprehensive_example():
    """Create a comprehensive visualization example."""
    print("\n🌟 Comprehensive Visualization Example")
    print("=" * 50)

    # Create a detailed asteroid impact scenario
    asteroid_scenario = {
        'name': 'Chicxulub-Scale Impact',
        'event_type': 'asteroid',
        'parameters': {
            'diameter_km': 10.0,
            'velocity_km_s': 20.0,
            'density_kg_m3': 3000,
            'impact_angle': 45
        },
        'results': {
            'severity': 6,
            'crater_diameter_km': 150,
            'impact_energy_joules': 4.2e23,
            'casualties': 7500000000,  # Near-extinction
            'economic_impact': 1e15,   # Global economy collapse
            'recovery_time_years': 1000
        },
        'damage_zones': {
            'crater': 75,
            'severe_blast': 500,
            'moderate_blast': 1500,
            'light_damage': 3000,
            'global_effects': 20000
        },
        'timeline': {
            0: {'event': 'Impact', 'severity': 6},
            1: {'event': 'Immediate Effects', 'severity': 6},
            7: {'event': 'Impact Winter Begins', 'severity': 5},
            30: {'event': 'Global Cooling', 'severity': 5},
            365: {'event': 'Agricultural Collapse', 'severity': 4},
            1825: {'event': 'Recovery Begins', 'severity': 3},
            18250: {'event': 'Ecosystem Recovery', 'severity': 2}
        }
    }

    print("Creating comprehensive visualization set...")

    # Create multiple visualizations
    figures = []

    try:
        # 1. Energy comparison with historical events
        energy_comparison = {
            'Chicxulub Impact': asteroid_scenario['results']['impact_energy_joules'],
            'Tunguska Event': 1.2e16,
            'Tsar Bomba': 2.1e17,
            'Mt. Tambora': 8.4e19,
            'Krakatoa': 2.0e17
        }

        fig1 = plot_energy_comparison(energy_comparison)
        figures.append(fig1)
        print("   ✅ Energy comparison chart")

        # 2. Damage zones
        fig2 = plot_damage_zones(
            asteroid_scenario['results']['crater_diameter_km'],
            asteroid_scenario['damage_zones']
        )
        figures.append(fig2)
        print("   ✅ Damage zones visualization")

        # 3. Geographic impact
        impact_data = {
            'impact_location': (21.4, -89.5),  # Chicxulub coordinates
            'max_impact_radius': 3000,
            'crater_diameter_km': asteroid_scenario['results']['crater_diameter_km']
        }

        fig3 = plot_geographic_heatmap(impact_data, grid_resolution=40)
        figures.append(fig3)
        print("   ✅ Geographic impact heatmap")

        # Export all figures
        if figures:
            exported_files = export_plots(
                figures,
                output_dir='demo_exports',
                formats=['png', 'pdf'],
                prefix='chicxulub_demo'
            )
            print(f"   ✅ Exported {len(exported_files)} visualization files")

        # Close figures to free memory
        for fig in figures:
            plt.close(fig)

    except Exception as e:
        print(f"   ❌ Error in comprehensive example: {e}")


def demo_networks():
    """Demonstrate network visualizations."""
    if not NETWORKS_AVAILABLE:
        print("Network visualization modules not available")
        return

    print("\n🌐 Demonstrating Network Visualizations")
    print("=" * 50)

    # Demo: Infrastructure Network Analysis (comprehensive)
    print("1. Running infrastructure network analysis...")
    try:
        demo_infrastructure_network()
        print("   ✅ Infrastructure network analysis completed")
    except Exception as e:
        print(f"   ❌ Error in infrastructure network analysis: {e}")

    print("   🌐 Network visualization demonstrations completed!")


def demo_scientific_visualizations():
    """Demonstrate scientific visualizations."""
    if not SCIENTIFIC_AVAILABLE:
        print("Scientific visualization modules not available")
        return

    print("\n🔬 Demonstrating Scientific Visualizations")
    print("=" * 50)

    # Demo 1: Phase Space Plot
    print("1. Creating phase space plot...")
    try:
        # Create sample data for phase space
        sample_data = {}  # Function will generate sample data
        fig1 = plot_phase_space(sample_data, 'x', 'y')
        print("   ✅ Phase space plot created")
        plt.close(fig1)
    except Exception as e:
        print(f"   ❌ Error creating phase space plot: {e}")

    # Demo 2: Monte Carlo Analysis
    print("2. Running Monte Carlo analysis...")
    try:
        # Create sample Monte Carlo results
        sample_results = {}  # Function will generate sample data
        fig2 = plot_monte_carlo_analysis(sample_results)
        print("   ✅ Monte Carlo analysis plot created")
        plt.close(fig2)
    except Exception as e:
        print(f"   ❌ Error running Monte Carlo analysis: {e}")

    print("   🔬 Scientific visualization demonstrations completed!")


def demo_comparative_analysis():
    """Demonstrate comparative analysis visualizations."""
    if not COMPARATIVE_AVAILABLE:
        print("Comparative analysis modules not available")
        return

    print("\n📊 Demonstrating Comparative Analysis Visualizations")
    print("=" * 50)

    # Demo 1: Scenario Comparison Overview
    print("1. Creating scenario comparison overview...")
    try:
        # Create sample scenarios data
        sample_scenarios = {
            'Asteroid Impact': {
                'severity': 8.5, 'casualties': 2e9,
                'economic_damage': 1e15, 'recovery_time': 50
            },
            'Pandemic': {
                'severity': 6.8, 'casualties': 5e8,
                'economic_damage': 2e13, 'recovery_time': 15
            },
            'Climate Collapse': {
                'severity': 7.5, 'casualties': 1e9,
                'economic_damage': 8e14, 'recovery_time': 200
            }
        }

        fig1 = compare_scenarios_overview(sample_scenarios)
        print("   ✅ Scenario comparison overview created")
        plt.close(fig1)
    except Exception as e:
        print(f"   ❌ Error creating scenario comparison overview: {e}")

    # Demo 2: Scenario Ranking
    print("2. Creating scenario ranking plot...")
    try:
        # Use the same sample scenarios
        fig2 = plot_scenario_ranking(sample_scenarios)
        print("   ✅ Scenario ranking plot created")
        plt.close(fig2)
    except Exception as e:
        print(f"   ❌ Error creating scenario ranking plot: {e}")

    # Demo 3: Timeline Comparison
    print("3. Creating timeline comparison...")
    try:
        # Create sample timeline data
        sample_timelines = {
            'Asteroid Impact': {
                'impact': 0, 'global_winter': 0.5, 'crop_failure': 1,
                'mass_starvation': 2, 'societal_collapse': 5
            },
            'Pandemic': {
                'outbreak': 0, 'global_spread': 0.25, 'peak_mortality': 1.5,
                'vaccine_development': 2, 'recovery_start': 3
            }
        }

        fig3 = plot_scenario_timeline_comparison(sample_timelines)
        print("   ✅ Timeline comparison created")
        plt.close(fig3)
    except Exception as e:
        print(f"   ❌ Error creating timeline comparison: {e}")

    # Demo 4: Sensitivity Analysis
    print("4. Creating sensitivity analysis...")
    try:
        # Create sample parameter variations
        sample_base_scenario = {'severity': 7.0}
        sample_variations = {
            'asteroid_size': np.linspace(0.5, 5.0, 20),
            'impact_angle': np.linspace(15, 90, 20)
        }

        fig4 = plot_sensitivity_analysis(sample_base_scenario, sample_variations)
        print("   ✅ Sensitivity analysis created")
        plt.close(fig4)
    except Exception as e:
        print(f"   ❌ Error creating sensitivity analysis: {e}")

    print("   📊 Comparative analysis demonstrations completed!")


def demo_advanced_visualizations():
    """Demonstrate advanced visualization capabilities."""
    if not VISUALIZATIONS_AVAILABLE:
        print("Basic visualization modules not available")
        return

    print("\n🚀 Demonstrating Advanced Visualization Capabilities")
    print("=" * 60)

    # Demo Networks Module
    if NETWORKS_AVAILABLE:
        print("\n📊 Network Analysis Visualizations")
        print("-" * 40)
        try:
            demo_infrastructure_network()
            print("   ✅ Infrastructure network demo completed")
        except Exception as e:
            print(f"   ❌ Error in network demo: {e}")
    else:
        print("   ⚠️  Networks module not available (missing networkx)")

    # Demo Scientific Module
    if SCIENTIFIC_AVAILABLE:
        print("\n🔬 Scientific Plotting Visualizations")
        print("-" * 40)
        try:
            demo_scientific_plots()
            print("   ✅ Scientific plotting demo completed")
        except Exception as e:
            print(f"   ❌ Error in scientific demo: {e}")
    else:
        print("   ⚠️  Scientific module not available")

    # Demo Comparative Module
    if COMPARATIVE_AVAILABLE:
        print("\n📈 Comparative Analysis Visualizations")
        print("-" * 40)
        try:
            demo_comparative_analysis()
            print("   ✅ Comparative analysis demo completed")
        except Exception as e:
            print(f"   ❌ Error in comparative demo: {e}")
    else:
        print("   ⚠️  Comparative module not available")


def run_comprehensive_demo():
    """Run complete demonstration of all visualization capabilities."""
    print("🎨 E.L.E.S. Visualization Module - Comprehensive Demo")
    print("=" * 60)

    # Run basic demos
    demo_basic_charts()
    demo_heatmaps()
    demo_export_capabilities()
    demo_comprehensive_example()

    # Run advanced demos
    demo_advanced_visualizations()

    print("\n🎉 All visualization demonstrations completed!")
    print("=" * 60)


# Main execution
if __name__ == "__main__":
    # You can run specific demos or the comprehensive demo
    import sys

    if len(sys.argv) > 1:
        demo_type = sys.argv[1].lower()
        if demo_type == "basic":
            demo_basic_charts()
        elif demo_type == "heatmaps":
            demo_heatmaps()
        elif demo_type == "export":
            demo_export_capabilities()
        elif demo_type == "comprehensive":
            demo_comprehensive_example()
        elif demo_type == "networks" and NETWORKS_AVAILABLE:
            demo_infrastructure_network()
        elif demo_type == "scientific" and SCIENTIFIC_AVAILABLE:
            demo_scientific_plots()
        elif demo_type == "comparative" and COMPARATIVE_AVAILABLE:
            demo_comparative_analysis()
        elif demo_type == "advanced":
            demo_advanced_visualizations()
        else:
            print(f"Unknown demo type: {demo_type}")
            print("Available demos: basic, heatmaps, export, comprehensive, networks, scientific, comparative, advanced")
    else:
        # Run comprehensive demo by default
        run_comprehensive_demo()
