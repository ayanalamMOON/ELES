import math
from typing import Dict, Any, Tuple
from config.constants import CRATER_SCALING_FACTOR, EARTH_RADIUS_KM


def calculate_crater_diameter(energy_j: float, target_density: float = 2500) -> float:
    """
    Calculate crater diameter from impact energy.

    Args:
        energy_j: Impact energy in joules
        target_density: Target material density in kg/m³

    Returns:
        Crater diameter in kilometers
    """
    # Simplified scaling law: D ∝ E^0.25
    # Based on empirical crater scaling relationships
    scaling_constant = 1.8  # Empirical constant
    diameter_m = scaling_constant * (energy_j / (target_density * 1000)) ** 0.25
    return diameter_m / 1000  # Convert to km


def calculate_impact_energy(mass_kg: float, velocity_ms: float) -> float:
    """Calculate kinetic energy of impact."""
    return 0.5 * mass_kg * velocity_ms ** 2


def calculate_mass_from_diameter(diameter_km: float, density_kg_m3: float) -> float:
    """Calculate mass from diameter assuming spherical object."""
    radius_m = diameter_km * 500  # Convert km to m and get radius
    volume_m3 = (4/3) * math.pi * radius_m ** 3
    return volume_m3 * density_kg_m3


def tnt_equivalent(energy_j: float) -> float:
    """Convert energy to TNT equivalent in megatons."""
    # 1 megaton TNT = 4.184 × 10^15 joules
    return energy_j / 4.184e15


def richter_magnitude(energy_j: float) -> float:
    """Estimate earthquake magnitude from energy."""
    # Empirical relationship: log10(E) = 11.8 + 1.5*M
    if energy_j <= 0:
        return 0
    return (math.log10(energy_j) - 11.8) / 1.5


def tsunami_height(energy_j: float, distance_km: float) -> float:
    """Estimate tsunami height at given distance."""
    if distance_km <= 0:
        return 0
    # Very simplified model
    base_height = (energy_j / 1e20) ** 0.5
    decay_factor = 1 / (distance_km ** 0.5)
    return base_height * decay_factor


def atmospheric_effects(energy_j: float) -> Dict[str, Any]:
    """Calculate atmospheric effects from impact."""
    effects = {}

    # Dust and debris estimation
    if energy_j > 1e20:
        effects['dust_mass_kg'] = energy_j / 1e12
        effects['darkness_duration_days'] = min((energy_j / 1e21) * 30, 365)
        effects['temperature_drop_c'] = min((energy_j / 1e22) * 5, 15)
    else:
        effects['dust_mass_kg'] = 0
        effects['darkness_duration_days'] = 0
        effects['temperature_drop_c'] = 0

    return effects


def population_at_risk(crater_diameter_km: float,
                      destruction_radius_multiplier: float = 3.0) -> int:
    """
    Estimate population at risk based on crater size.

    Args:
        crater_diameter_km: Crater diameter in km
        destruction_radius_multiplier: How many crater radii define destruction zone

    Returns:
        Estimated population at risk
    """
    destruction_radius_km = (crater_diameter_km / 2) * destruction_radius_multiplier
    destruction_area_km2 = math.pi * destruction_radius_km ** 2

    # Global average population density: ~60 people per km²
    # Urban areas much higher, rural areas much lower
    avg_density = 60

    return int(destruction_area_km2 * avg_density)


def economic_damage_estimate(crater_diameter_km: float,
                           gdp_per_km2: float = 5e6) -> float:
    """
    Estimate economic damage in USD.

    Args:
        crater_diameter_km: Crater diameter in km
        gdp_per_km2: GDP per square kilometer in USD

    Returns:
        Estimated economic damage in USD
    """
    destruction_radius_km = crater_diameter_km * 2  # Damage extends beyond crater
    destruction_area_km2 = math.pi * destruction_radius_km ** 2

    return destruction_area_km2 * gdp_per_km2


def format_scientific_notation(value: float, precision: int = 2) -> str:
    """Format large numbers in scientific notation."""
    if value == 0:
        return "0"
    elif abs(value) < 1000:
        return f"{value:.{precision}f}"
    else:
        return f"{value:.{precision}e}"


def format_large_number(value: float) -> str:
    """Format large numbers with appropriate units."""
    if value < 1000:
        return f"{value:.1f}"
    elif value < 1e6:
        return f"{value/1000:.1f}K"
    elif value < 1e9:
        return f"{value/1e6:.1f}M"
    elif value < 1e12:
        return f"{value/1e9:.1f}B"
    else:
        return f"{value/1e12:.1f}T"


def distance_to_horizon(altitude_km: float) -> float:
    """Calculate distance to horizon from given altitude."""
    return math.sqrt(2 * EARTH_RADIUS_KM * altitude_km + altitude_km ** 2)


def escape_velocity(mass_kg: float, radius_m: float) -> float:
    """Calculate escape velocity for given mass and radius."""
    G = 6.674e-11  # Gravitational constant
    return math.sqrt(2 * G * mass_kg / radius_m)


def validate_parameters(params: Dict[str, Any], required_keys: list) -> bool:
    """Validate that all required parameters are present."""
    return all(key in params for key in required_keys)
