"""
Event types module for E.L.E.S.

This module contains all extinction event type classes for simulation.
"""

from .asteroid import AsteroidImpact
from .supervolcano import Supervolcano
from .climate_collapse import ClimateCollapse
from .pandemic import Pandemic
from .gamma_ray_burst import GammaRayBurst
from .ai_extinction import AIExtinction

__all__ = [
    'AsteroidImpact',
    'Supervolcano',
    'ClimateCollapse',
    'Pandemic',
    'GammaRayBurst',
    'AIExtinction'
]
