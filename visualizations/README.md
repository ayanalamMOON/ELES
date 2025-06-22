# E.L.E.S. Visualization Module Documentation

## Overview

The E.L.E.S. (Extinction-Level Event Simulator) visualization module provides comprehensive data visualization tools for analyzing and presenting extinction event simulations. The module is designed to be modular, robust, and extensible.

## Module Structure

```
visualizations/
├── __init__.py              # Main module initialization and utilities
├── charts.py                # Basic chart generation functions
├── heatmaps.py             # Geographic and risk heatmap tools
├── interactive.py          # Interactive Plotly/Streamlit visualizations
├── animations.py           # Animation and temporal visualizations
├── maps.py                 # Geographic mapping with folium/plotly
├── dashboards.py           # Multi-panel dashboard layouts
├── export.py               # Export utilities for plots and data
├── networks.py             # Network analysis visualizations (NEW)
├── scientific.py           # Scientific plotting and analysis (NEW)
├── comparative.py          # Multi-scenario comparison tools (NEW)
├── demo.py                 # Comprehensive demonstrations
└── 3d/
    ├── __init__.py         # 3D module initialization
    └── model.py            # 3D rendering and modeling
```

## Dependencies

### Core Dependencies

- `matplotlib>=3.7.0` - Basic plotting
- `seaborn>=0.12.0` - Statistical visualizations
- `pandas>=2.0.0` - Data manipulation
- `numpy>=1.24.0` - Numerical computations
- `plotly>=5.15.0` - Interactive visualizations

### Optional Dependencies

- `streamlit>=1.28.0` - Web-based dashboards
- `folium>=0.14.0` - Geographic mapping
- `networkx>=3.0` - Network analysis (for networks.py)
- `scipy` - Scientific computing (for scientific.py)

## Core Modules

### 1. charts.py - Basic Chart Generation

Provides fundamental charting capabilities for extinction event data.

**Key Functions:**

- `plot_severity_distribution(results)` - Distribution of event severities
- `plot_energy_comparison(energy_data)` - Comparative energy release plots
- `plot_damage_zones(center_lat, blast_radii)` - Geographic damage zone visualization
- `plot_epidemic_curve(timeline_data)` - Epidemic progression curves
- `plot_timeline_comparison(scenarios)` - Multi-scenario timeline comparison
- `plot_risk_assessment_matrix(scenarios)` - Risk assessment visualization
- `plot_recovery_phases(recovery_data)` - Recovery timeline analysis
- `plot_parameter_sensitivity(param_data)` - Parameter sensitivity analysis

**Example Usage:**

```python
from visualizations.charts import plot_severity_distribution

# Sample results data
results = [{'severity': 3}, {'severity': 5}, {'severity': 2}]
fig = plot_severity_distribution(results)
fig.show()
```

### 2. heatmaps.py - Heatmap Visualizations

Specialized heatmap functions for geographic and risk analysis.

**Key Functions:**

- `plot_geographic_heatmap(data, lat_col, lon_col, value_col)` - Geographic data heatmaps
- `plot_risk_heatmap(risk_matrix)` - Risk assessment heatmaps
- `plot_population_density_heatmap(population_data)` - Population impact analysis
- `plot_correlation_heatmap(data_matrix)` - Variable correlation analysis
- `plot_temporal_heatmap(time_series_data)` - Time-based evolution heatmaps
- `plot_multi_layer_heatmap(layers_data)` - Multi-dimensional heatmaps
- `create_interactive_heatmap(data)` - Interactive heatmap with Plotly

**Example Usage:**

```python
from visualizations.heatmaps import plot_geographic_heatmap
import pandas as pd

# Sample geographic data
data = pd.DataFrame({
    'latitude': [40.7, 34.0, 41.9],
    'longitude': [-74.0, -118.2, -87.6],
    'impact_severity': [8.5, 7.2, 6.8]
})

fig = plot_geographic_heatmap(data, 'latitude', 'longitude', 'impact_severity')
```

### 3. interactive.py - Interactive Visualizations

Interactive components using Plotly and Streamlit for dynamic exploration.

**Key Functions:**

- `create_interactive_timeline(simulation_data)` - Interactive event timelines
- `create_parameter_explorer(event_type, parameter_ranges)` - Parameter exploration interface
- `create_damage_assessment_dashboard(damage_data)` - Interactive damage assessment
- `create_scenario_comparison_tool(scenarios)` - Multi-scenario comparison interface

### 4. animations.py - Temporal Animations

Tools for creating animated visualizations showing event evolution over time.

**Key Functions:**

- `create_impact_animation(impact_data, duration_frames)` - Asteroid impact progression
- `create_spread_animation(spread_data)` - Pandemic/contamination spread
- `create_recovery_animation(recovery_data)` - Recovery process visualization
- `create_climate_animation(climate_data)` - Climate change progression

### 5. 3d/ - 3D Visualizations

Advanced 3D rendering capabilities for immersive visualization.

**Key Functions:**

- `render_asteroid_impact(impact_parameters)` - 3D asteroid impact crater
- `render_explosion_sphere(explosion_data)` - 3D explosion visualization
- `render_damage_zones_3d(blast_data)` - 3D damage zone mapping
- `render_geographic_model(terrain_data, overlay_data)` - 3D geographic models
- `create_atmospheric_model_3d(atmospheric_data)` - 3D atmospheric effects

## Advanced Modules (NEW)

### 6. networks.py - Network Analysis

Network-based visualizations for modeling interconnected systems during extinction events.

**Key Features:**

- Infrastructure dependency networks
- Supply chain disruption analysis
- Ecosystem food web modeling
- Cascade failure visualization
- Network resilience metrics

**Key Functions:**

- `create_infrastructure_network(nodes_data, dependencies)` - Build infrastructure networks
- `plot_infrastructure_vulnerability(network, event_impact)` - Vulnerability analysis
- `plot_supply_chain_disruption(supply_data, disruption_points)` - Supply chain analysis
- `plot_ecosystem_food_web(species_data, extinction_cascade)` - Ecosystem modeling
- `calculate_network_resilience(network, failure_cascade)` - Resilience metrics

**Example Usage:**

```python
from visualizations.networks import create_infrastructure_network, plot_infrastructure_vulnerability

# Define infrastructure nodes
nodes_data = {
    'power_plant_1': {'type': 'power', 'capacity': 1000, 'critical': True},
    'hospital_1': {'type': 'healthcare', 'capacity': 200, 'critical': True},
    'data_center': {'type': 'communications', 'capacity': 100, 'critical': True}
}

# Define dependencies
dependencies = [
    ('power_plant_1', 'hospital_1'),
    ('power_plant_1', 'data_center')
]

# Create network and analyze vulnerability
network = create_infrastructure_network(nodes_data, dependencies)
event_impact = {'power_plant_1': 0.9, 'hospital_1': 0.3}
fig = plot_infrastructure_vulnerability(network, event_impact)
```

### 7. scientific.py - Scientific Plotting

Advanced scientific visualization tools for rigorous analysis.

**Key Features:**

- Phase space analysis
- Spectral analysis (FFT, spectrograms)
- Statistical distribution fitting
- Monte Carlo simulation analysis
- Uncertainty quantification
- Multi-dimensional parameter sweeps

**Key Functions:**

- `plot_phase_space(data, x_var, y_var)` - Phase space dynamics
- `plot_spectral_analysis(time_series, sampling_rate)` - Frequency domain analysis
- `plot_distribution_analysis(data, distribution_types)` - Statistical distribution fitting
- `plot_monte_carlo_analysis(simulation_results, confidence_levels)` - Monte Carlo analysis
- `plot_parameter_sweep_3d(parameter_data, x_param, y_param, z_param)` - 3D parameter sweeps
- `plot_uncertainty_bands(time_data, ensemble_data)` - Uncertainty visualization

**Example Usage:**

```python
from visualizations.scientific import plot_monte_carlo_analysis

# Monte Carlo simulation results
simulation_results = {
    'casualties': [1e6, 2e6, 1.5e6, 3e6, ...],  # List of simulation outcomes
    'economic_damage': [1e12, 2e12, 1.8e12, ...],
    'recovery_time': [10, 15, 12, 18, ...]
}

fig = plot_monte_carlo_analysis(simulation_results, confidence_levels=[0.68, 0.95])
```

### 8. comparative.py - Multi-Scenario Comparison

Tools for comparing multiple extinction event scenarios.

**Key Features:**

- Multi-metric scenario comparison
- Timeline comparison across scenarios
- Sensitivity analysis
- Scenario ranking with weighted criteria
- Uncertainty comparison across scenarios

**Key Functions:**

- `compare_scenarios_overview(scenarios, metrics)` - Comprehensive scenario comparison
- `plot_scenario_timeline_comparison(scenario_timelines)` - Timeline comparison
- `plot_sensitivity_analysis(base_scenario, parameter_variations)` - Parameter sensitivity
- `plot_scenario_ranking(scenarios, ranking_criteria, weights)` - Weighted scenario ranking
- `plot_multi_scenario_uncertainty(scenario_ensembles, metric)` - Uncertainty comparison

**Example Usage:**

```python
from visualizations.comparative import compare_scenarios_overview

# Define multiple scenarios
scenarios = {
    'Asteroid Impact': {
        'severity': 8.5, 'casualties': 2e9,
        'economic_damage': 1e15, 'recovery_time': 50
    },
    'Pandemic': {
        'severity': 6.8, 'casualties': 5e8,
        'economic_damage': 2e13, 'recovery_time': 15
    }
}

fig = compare_scenarios_overview(scenarios)
```

## Utility Features

### Styling and Themes

The module provides consistent styling through the main `__init__.py`:

```python
from visualizations import set_eles_style, get_event_color, get_severity_color

# Apply E.L.E.S. styling
set_eles_style()

# Get consistent colors
asteroid_color = get_event_color('asteroid')
high_severity_color = get_severity_color(6)
```

### Export Capabilities

The `export.py` module provides comprehensive export functionality:

```python
from visualizations.export import export_plots, create_report_plots

# Export multiple plots
figures = [fig1, fig2, fig3]
export_plots(figures, output_dir='./reports', formats=['png', 'pdf'])

# Create standardized report plots
report_data = {...}
create_report_plots(report_data, output_path='./extinction_report.pdf')
```

## Usage Patterns

### Basic Usage Pattern

```python
# Import what you need
from visualizations.charts import plot_severity_distribution
from visualizations.heatmaps import plot_geographic_heatmap
from visualizations import set_eles_style

# Apply consistent styling
set_eles_style()

# Create visualizations
severity_fig = plot_severity_distribution(simulation_results)
heatmap_fig = plot_geographic_heatmap(geographic_data, 'lat', 'lon', 'impact')

# Show or save
severity_fig.show()
heatmap_fig.savefig('impact_heatmap.png', dpi=300, bbox_inches='tight')
```

### Advanced Analysis Pattern

```python
# Full analysis workflow
from visualizations.scientific import plot_monte_carlo_analysis
from visualizations.comparative import compare_scenarios_overview
from visualizations.networks import plot_infrastructure_vulnerability
from visualizations.export import create_report_plots

# 1. Monte Carlo uncertainty analysis
mc_fig = plot_monte_carlo_analysis(monte_carlo_results)

# 2. Compare multiple scenarios
comparison_fig = compare_scenarios_overview(all_scenarios)

# 3. Analyze infrastructure vulnerability
network_fig = plot_infrastructure_vulnerability(infrastructure_network, damages)

# 4. Export comprehensive report
report_data = {
    'monte_carlo': monte_carlo_results,
    'scenarios': all_scenarios,
    'infrastructure': infrastructure_analysis
}
create_report_plots(report_data, 'comprehensive_analysis.pdf')
```

## Running Demonstrations

The module includes comprehensive demonstrations:

```bash
# Run all demonstrations
python visualizations/demo.py

# Run specific demonstration
python visualizations/demo.py basic          # Basic charts
python visualizations/demo.py networks       # Network analysis
python visualizations/demo.py scientific     # Scientific plotting
python visualizations/demo.py comparative    # Comparative analysis
python visualizations/demo.py advanced       # All advanced features
```

## Error Handling and Robustness

The visualization module is designed to be robust:

1. **Graceful degradation**: Missing optional dependencies don't break the module
2. **Sample data generation**: Functions provide meaningful sample data when input is missing
3. **Error catching**: Import errors are caught and reported without crashing
4. **Type hints**: Comprehensive type hints for better IDE support and debugging

## Performance Considerations

- **Large datasets**: Use sampling or aggregation for datasets >10,000 points
- **Interactive plots**: Plotly plots may be slower than matplotlib for very large datasets
- **Network analysis**: NetworkX operations scale poorly beyond ~1,000 nodes
- **3D rendering**: 3D plots are memory-intensive; use sparingly

## Extension Guidelines

To add new visualization capabilities:

1. Create a new module file (e.g., `new_viz.py`)
2. Follow the existing function signature patterns
3. Include comprehensive docstrings and type hints
4. Add sample data generation for robustness
5. Update `__init__.py` with optional imports
6. Add demonstrations to `demo.py`
7. Update this documentation

## Troubleshooting

### Common Issues

1. **Import errors**: Check that all required dependencies are installed
2. **NetworkX not found**: Install with `pip install networkx`
3. **Empty plots**: Verify your data format matches expected input
4. **Performance issues**: Reduce data size or use sampling

### Getting Help

1. Run the demonstrations to see expected usage patterns
2. Check function docstrings for detailed parameter information
3. Look at the sample data generation code for format examples
4. Use the robust error handling to identify specific issues

## Version History

- **v0.1.0**: Initial release with basic charts and heatmaps
- **v0.2.0**: Added interactive, animations, maps, dashboards, export, and 3D modules
- **v0.3.0**: Added networks, scientific, and comparative analysis modules

## License

This module is part of the E.L.E.S. project and follows the same licensing terms.
