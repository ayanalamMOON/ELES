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
    create_atmospheric_model_3d
)

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
    'create_atmospheric_model_3d'
]
