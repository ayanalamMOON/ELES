"""
E.L.E.S. Core Module

Extinction-Level Event Simulator - Core simulation engine and utilities.

This module provides the core functionality for simulating various extinction-level
events including asteroid impacts, supervolcanoes, pandemics, climate collapse,
gamma-ray bursts, and AI extinction scenarios.

Classes:
    Engine: Main simulation engine
    ExtinctionResult: Results container and analysis

Event Types:
    AsteroidImpact: Asteroid impact simulations
    Supervolcano: Supervolcanic eruption simulations
    ClimateCollapse: Climate change and collapse simulations
    Pandemic: Pandemic and disease outbreak simulations
    GammaRayBurst: Gamma-ray burst impact simulations
    AIExtinction: AI extinction risk simulations

Utilities:
    Various calculation and helper functions for simulations
"""

from typing import Optional

# Core engine and result classes
from .engine import Engine
from .extinction_result import ExtinctionResult

# Event type classes
from .event_types import (
    AsteroidImpact,
    Supervolcano,
    ClimateCollapse,
    Pandemic,
    GammaRayBurst,
    AIExtinction
)

# Utility functions - import commonly used ones
from .utils import (
    calculate_crater_diameter,
    calculate_impact_energy,
    calculate_mass_from_diameter,
    tnt_equivalent,
    richter_magnitude,
    atmospheric_effects,
    population_at_risk,
    format_large_number,
    format_scientific_notation,
    distance_to_horizon,
    escape_velocity,
    validate_parameters
)

# Version information
__version__ = "0.1.0"
__author__ = "E.L.E.S. Development Team"
__email__ = "contact@eles-project.org"
__license__ = "MIT"

# Package metadata
__title__ = "eles_core"
__description__ = "Core simulation engine for Extinction-Level Event Simulator"
__url__ = "https://github.com/eles-project/eles"

# Define what gets imported with "from eles_core import *"
__all__ = [
    # Core classes
    'Engine',
    'ExtinctionResult',

    # Event types
    'AsteroidImpact',
    'Supervolcano',
    'ClimateCollapse',
    'Pandemic',
    'GammaRayBurst',
    'AIExtinction',
      # Utility functions
    'calculate_crater_diameter',
    'calculate_impact_energy',
    'calculate_mass_from_diameter',
    'tnt_equivalent',
    'richter_magnitude',
    'atmospheric_effects',
    'population_at_risk',
    'format_large_number',
    'format_scientific_notation',
    'distance_to_horizon',
    'escape_velocity',
    'validate_parameters'
]

# Module-level constants
DEFAULT_CONFIG_PATH = "config/settings.yaml"
SUPPORTED_EVENT_TYPES = [
    'asteroid',
    'supervolcano',
    'climate_collapse',
    'pandemic',
    'gamma_ray_burst',
    'ai_extinction'
]

# Severity levels
SEVERITY_LEVELS = {
    1: "Minimal Impact",
    2: "Local Disaster",
    3: "Regional Catastrophe",
    4: "Continental Crisis",
    5: "Global Catastrophe",
    6: "Extinction-Level Event"
}


def get_version():
    """Return the version string."""
    return __version__


def get_supported_events():
    """Return list of supported event types."""
    return SUPPORTED_EVENT_TYPES.copy()


def get_severity_description(level: int) -> str:
    """Get human-readable description for severity level."""
    return SEVERITY_LEVELS.get(level, "Unknown Severity")


def create_engine(config_path: Optional[str] = None) -> Engine:
    """
    Convenience function to create a new simulation engine.

    Args:
        config_path: Path to configuration file (optional)

    Returns:
        Configured Engine instance
    """
    if config_path is None:
        config_path = DEFAULT_CONFIG_PATH
    return Engine(config_path)


# Module initialization
def _check_dependencies():
    """Check if required dependencies are available."""
    import importlib
    required = ['yaml', 'json', 'math', 'typing']
    missing = []

    for module in required:
        try:
            importlib.import_module(module)
        except ImportError:
            missing.append(module)

    if missing:
        raise ImportError(f"Missing required dependencies: {', '.join(missing)}")


# Run dependency check on import
try:
    _check_dependencies()
except ImportError:
    pass

# Optional: Print initialization message for debugging
import os
if os.environ.get('ELES_DEBUG', '').lower() in ('1', 'true', 'yes'):
    print(f"E.L.E.S. Core Module {__version__} initialized")
    print(f"Supported event types: {', '.join(SUPPORTED_EVENT_TYPES)}")
