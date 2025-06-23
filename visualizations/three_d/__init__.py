"""
3D Visualization Components for E.L.E.S.

This module provides 3D visualization capabilities for extinction events,
including impact craters, explosion spheres, and atmospheric models.

Components:
    - model.py: Core 3D rendering functions
"""

from .model import (
    render_asteroid_impact,
    render_explosion_sphere,
    render_damage_zones_3d,
    render_geographic_model,
    create_atmospheric_model_3d,
    render_climate_collapse_3d,
    render_gamma_ray_burst_3d,
    render_ai_extinction_3d,
    create_interactive_3d_timeline,
    create_multi_scenario_3d_comparison
)

# Try to import advanced simulation capabilities
try:
    from .advanced_simulations import (
        Advanced3DVisualizationManager,
        SimulationParameters,
        create_3d_visualization_manager
    )
    __all_advanced__ = [
        'Advanced3DVisualizationManager',
        'SimulationParameters', 
        'create_3d_visualization_manager'
    ]
except ImportError:
    __all_advanced__ = []

# Version information
__version__ = "0.2.0"

# Module description
__description__ = "3D visualization tools for E.L.E.S."

# Define what gets imported with "from visualizations.3d import *"
__all__ = [
    'render_asteroid_impact',
    'render_explosion_sphere',
    'render_damage_zones_3d',
    'render_geographic_model',
    'create_atmospheric_model_3d',
    'render_climate_collapse_3d',
    'render_gamma_ray_burst_3d',
    'render_ai_extinction_3d',
    'create_interactive_3d_timeline',
    'create_multi_scenario_3d_comparison'
]

# Add advanced simulation functions if available
__all__.extend(__all_advanced__)
