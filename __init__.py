"""
E.L.E.S. - Extinction-Level Event Simulator

A comprehensive simulation platform for modeling and analyzing extinction-level
events including asteroid impacts, supervolcanoes, pandemics, climate collapse,
gamma-ray bursts, and AI extinction scenarios.

This package provides:
- Core simulation engine
- Multiple event type modules
- Interactive web interface (Streamlit)
- Command-line interface
- Data visualization tools
- Risk assessment models
- Educational scenarios

Usage:
    from eles_core import Engine, create_engine

    # Create simulation engine
    engine = create_engine()

    # Run a simulation
    result = engine.run_simulation('asteroid', {
        'diameter_km': 2.0,
        'velocity_km_s': 20.0,
        'density_kg_m3': 3500
    })

    # Analyze results
    print(f"Severity: {result.severity}")
    print(f"Impact area: {result.impacted_area} km²")

For more information, see the documentation in the README.md file.
"""

# Import core functionality
from eles_core import (
    Engine,
    ExtinctionResult,
    create_engine,
    get_version,
    get_supported_events,
    get_severity_description,
    SUPPORTED_EVENT_TYPES,
    SEVERITY_LEVELS
)

# Package information
__version__ = "0.1.0"
__author__ = "E.L.E.S. Development Team"
__title__ = "E.L.E.S."
__description__ = "Extinction-Level Event Simulator"
__url__ = "https://github.com/eles-project/eles"
__license__ = "MIT"

# What gets imported with "from eles import *"
__all__ = [
    'Engine',
    'ExtinctionResult',
    'create_engine',
    'get_version',
    'get_supported_events',
    'get_severity_description',
    'SUPPORTED_EVENT_TYPES',
    'SEVERITY_LEVELS'
]
