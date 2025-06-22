# Constants for E.L.E.S. project
import os

# File paths
DEFAULT_SCENARIO_PATH = "data/scenarios"
CONFIG_FILE = "config/settings.yaml"
DATA_DIR = "data"

# Physical constants
EARTH_RADIUS_KM = 6371
EARTH_MASS_KG = 5.972e24
GRAVITATIONAL_CONSTANT = 6.674e-11

# Asteroid impact constants
CRATER_SCALING_FACTOR = 1.8
ENERGY_SCALING_FACTOR = 0.5

# Extinction event severity levels
SEVERITY_LEVELS = {
    "MINIMAL": 1,
    "LOCAL": 2,
    "REGIONAL": 3,
    "CONTINENTAL": 4,
    "GLOBAL": 5,
    "EXTINCTION": 6
}

# Default simulation parameters
DEFAULT_VELOCITY_KMS = 20.0
DEFAULT_IMPACT_ANGLE = 45.0
SECONDS_PER_YEAR = 31536000

# Color schemes for visualizations
SEVERITY_COLORS = {
    1: "#00ff00",  # Green
    2: "#ffff00",  # Yellow
    3: "#ff8000",  # Orange
    4: "#ff0000",  # Red
    5: "#800080",  # Purple
    6: "#000000"   # Black
}
