import math
from typing import Dict, Any


class GammaRayBurst:
    """Gamma-ray burst simulation class."""

    def __init__(self, distance_ly: float, duration_seconds: float = 10.0,
                 energy_erg: float = 1e44):
        """
        Initialize gamma-ray burst parameters.

        Args:
            distance_ly: Distance to GRB source in light-years
            duration_seconds: Duration of burst in seconds
            energy_erg: Total energy output in ergs
        """
        self.distance_ly = distance_ly
        self.duration_seconds = duration_seconds
        self.energy_erg = energy_erg

        # Convert distance to meters
        self.distance_m = distance_ly * 9.461e15  # meters per light-year

    def simulate(self) -> Dict[str, Any]:
        """Run gamma-ray burst simulation."""
        results = {}

        # Basic parameters
        results['distance_ly'] = self.distance_ly
        results['duration_seconds'] = self.duration_seconds
        results['energy_erg'] = self.energy_erg

        # Calculate energy flux at Earth
        flux_effects = self._calculate_flux_effects()
        results.update(flux_effects)

        # Atmospheric effects
        atmospheric_effects = self._calculate_atmospheric_effects()
        results.update(atmospheric_effects)

        # Biological effects
        biological_effects = self._calculate_biological_effects()
        results.update(biological_effects)

        # Climate effects
        climate_effects = self._calculate_climate_effects()
        results.update(climate_effects)

        return results

    def _calculate_flux_effects(self) -> Dict[str, Any]:
        """Calculate energy flux reaching Earth."""
        # Energy flux = Energy / (4π * distance²)
        flux_erg_cm2 = self.energy_erg / (4 * math.pi * (self.distance_m * 100) ** 2)

        # Convert to more manageable units
        flux_j_m2 = flux_erg_cm2 * 1e-7 * 1e4  # erg/cm² to J/m²

        return {
            'energy_flux_j_m2': flux_j_m2,
            'intensity': 1 / (self.distance_ly ** 2),  # Relative intensity
            'peak_flux_erg_cm2_s': flux_erg_cm2 / self.duration_seconds
        }

    def _calculate_atmospheric_effects(self) -> Dict[str, Any]:
        """Calculate effects on Earth's atmosphere."""
        effects = {}

        # Energy flux reaching Earth
        flux_j_m2 = self.energy_erg / (4 * math.pi * (self.distance_m * 100) ** 2) * 1e-7 * 1e4

        # Ozone depletion
        if self.distance_ly < 10000:
            # Severe ozone depletion
            ozone_depletion = min(95, 10000 / self.distance_ly * 10)
            effects['ozone_depletion_percent'] = ozone_depletion
            effects['uv_increase_factor'] = 1 + (ozone_depletion / 100) * 10
        else:
            effects['ozone_depletion_percent'] = 0
            effects['uv_increase_factor'] = 1

        # Atmospheric heating
        if flux_j_m2 > 1e6:
            effects['atmospheric_heating_k'] = min(100, flux_j_m2 / 1e6)
        else:
            effects['atmospheric_heating_k'] = 0

        # Nitrogen oxide production
        if self.distance_ly < 5000:
            effects['no2_production_increase'] = min(1000, 5000 / self.distance_ly)
        else:
            effects['no2_production_increase'] = 0

        return effects

    def _calculate_biological_effects(self) -> Dict[str, Any]:
        """Calculate biological effects."""
        effects = {}

        # UV radiation effects
        uv_factor = self._calculate_flux_effects().get('uv_increase_factor', 1)

        if uv_factor > 10:
            effects['dna_damage_level'] = 'Lethal'
            effects['surface_life_survival'] = 'Unlikely'
            effects['ocean_life_impact'] = 'Severe - phytoplankton collapse'
        elif uv_factor > 5:
            effects['dna_damage_level'] = 'Severe'
            effects['surface_life_survival'] = 'Difficult'
            effects['ocean_life_impact'] = 'Significant'
        elif uv_factor > 2:
            effects['dna_damage_level'] = 'Moderate'
            effects['surface_life_survival'] = 'Reduced'
            effects['ocean_life_impact'] = 'Moderate'
        else:
            effects['dna_damage_level'] = 'Minimal'
            effects['surface_life_survival'] = 'Normal'
            effects['ocean_life_impact'] = 'Minimal'

        # Extinction probability
        if self.distance_ly < 1000:
            effects['extinction_probability'] = 0.9
        elif self.distance_ly < 3000:
            effects['extinction_probability'] = 0.5
        elif self.distance_ly < 8000:
            effects['extinction_probability'] = 0.1
        else:
            effects['extinction_probability'] = 0.01

        return effects

    def _calculate_climate_effects(self) -> Dict[str, Any]:
        """Calculate climate effects."""
        effects = {}

        ozone_depletion = self._calculate_atmospheric_effects().get('ozone_depletion_percent', 0)

        if ozone_depletion > 50:
            effects['temperature_change_c'] = -5 - (ozone_depletion - 50) / 10
            effects['climate_disruption'] = 'Severe cooling, ecosystem collapse'
            effects['ice_age_trigger'] = True
        elif ozone_depletion > 20:
            effects['temperature_change_c'] = -2
            effects['climate_disruption'] = 'Moderate cooling'
            effects['ice_age_trigger'] = False
        else:
            effects['temperature_change_c'] = 0
            effects['climate_disruption'] = 'Minimal'
            effects['ice_age_trigger'] = False

        return effects

    def get_threat_level(self) -> str:
        """Determine threat level based on distance."""
        if self.distance_ly < 1000:
            return "Extinction-Level Threat"
        elif self.distance_ly < 3000:
            return "Catastrophic Threat"
        elif self.distance_ly < 8000:
            return "Severe Threat"
        elif self.distance_ly < 15000:
            return "Moderate Threat"
        else:
            return "Low Threat"

    def get_historical_context(self) -> Dict[str, Any]:
        """Provide historical context."""
        return {
            'ordovician_extinction': {
                'distance_estimate_ly': 6000,
                'time_ago_mya': 450,
                'extinction_rate': 0.85
            },
            'nearest_grb_candidate': {
                'name': 'WR 104',
                'distance_ly': 8000,
                'threat_level': 'Moderate'
            },
            'detection_rate': '1 per day (observable universe)',
            'milky_way_rate': '1 per 100,000 to 1,000,000 years'
        }
