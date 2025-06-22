"""
Visualizations Module for E.L.E.S.

This module contains comprehensive data visualization tools and components for the
Extinction-Level Event Simulator.

Components:
    - charts.py: Chart generation and plotting functions
    - heatmaps.py: Geographic and risk heatmap visualization tools
    - 3d/: 3D visualization components and models
    - interactive.py: Interactive visualization components
    - animations.py: Animation and temporal visualization tools
    - maps.py: Geographic mapping and spatial analysis
    - dashboards.py: Dashboard and multi-panel visualizations
    - export.py: Export and rendering utilities
"""

"""
Visualizations Module for E.L.E.S.

This module contains comprehensive data visualization tools and components for the
Extinction-Level Event Simulator.

Components:
    - charts.py: Chart generation and plotting functions
    - heatmaps.py: Geographic and risk heatmap visualization tools
    - 3d/: 3D visualization components and models
    - interactive.py: Interactive visualization components
    - animations.py: Animation and temporal visualization tools
    - maps.py: Geographic mapping and spatial analysis
    - dashboards.py: Dashboard and multi-panel visualizations
    - export.py: Export and rendering utilities
    - networks.py: Network analysis and infrastructure visualizations
    - scientific.py: Scientific plotting and statistical analysis
    - comparative.py: Multi-scenario comparison and analysis tools
"""

# Core visualization functions (import only what exists)
try:
    from .charts import (
        plot_severity_distribution,
        plot_energy_comparison,
        plot_damage_zones,
        plot_epidemic_curve
    )
except ImportError:
    pass

try:
    from .heatmaps import (
        plot_geographic_heatmap,
        plot_risk_heatmap,
        plot_population_density_heatmap,
        plot_correlation_heatmap,
        plot_temporal_heatmap
    )
except ImportError:
    pass

# Advanced visualization modules (optional imports)
try:
    from .networks import (
        create_infrastructure_network,
        plot_infrastructure_vulnerability,
        plot_supply_chain_disruption,
        plot_ecosystem_food_web,
        calculate_network_resilience
    )
except ImportError:
    pass

try:
    from .scientific import (
        plot_phase_space,
        plot_spectral_analysis,
        plot_distribution_analysis,
        plot_monte_carlo_analysis,
        plot_parameter_sweep_3d,
        plot_uncertainty_bands
    )
except ImportError:
    pass

try:
    from .comparative import (
        compare_scenarios_overview,
        plot_scenario_timeline_comparison,
        plot_sensitivity_analysis,
        plot_scenario_ranking,
        plot_multi_scenario_uncertainty
    )
except ImportError:
    pass

# Version information
__version__ = "0.3.0"
__author__ = "E.L.E.S. Development Team"

# Module description
__description__ = "Comprehensive data visualization tools for E.L.E.S."

# Visualization themes and styles
ELES_STYLE = {
    'figure.figsize': (12, 8),
    'axes.titlesize': 16,
    'axes.labelsize': 14,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12,
    'font.family': 'sans-serif',
    'grid.alpha': 0.3
}

# Color palettes for different event types
EVENT_COLORS = {
    'asteroid': '#FF6B35',      # Orange-red
    'supervolcano': '#8B0000',  # Dark red
    'pandemic': '#228B22',      # Forest green
    'climate_collapse': '#4169E1',  # Royal blue
    'gamma_ray_burst': '#9370DB',   # Medium purple
    'ai_extinction': '#DC143C',     # Crimson
    'nuclear': '#FFD700'        # Gold
}

# Severity level colors
SEVERITY_COLORS = {
    1: '#90EE90',  # Light green
    2: '#FFD700',  # Gold
    3: '#FFA500',  # Orange
    4: '#FF6347',  # Tomato
    5: '#DC143C',  # Crimson
    6: '#8B0000'   # Dark red
}

def set_eles_style():
    """Apply E.L.E.S. visualization style."""
    try:
        import matplotlib.pyplot as plt
        plt.style.use('default')
        plt.rcParams.update(ELES_STYLE)
    except ImportError:
        pass

def get_event_color(event_type: str) -> str:
    """Get color for specific event type."""
    return EVENT_COLORS.get(event_type, '#808080')

def get_severity_color(severity: int) -> str:
    """Get color for severity level."""
    return SEVERITY_COLORS.get(severity, '#808080')
