import math
from typing import Dict, Any, Tuple
from ..utils import (
    calculate_crater_diameter, calculate_impact_energy,
    calculate_mass_from_diameter, tnt_equivalent,
    richter_magnitude, atmospheric_effects, population_at_risk
)


class AsteroidImpact:
    """Asteroid impact simulation class."""

    def __init__(self, diameter_km: float, density_kg_m3: float, velocity_km_s: float,
                 impact_angle: float = 45.0, target_type: str = "continental"):
        """
        Initialize asteroid impact parameters.

        Args:
            diameter_km: Asteroid diameter in kilometers
            density_kg_m3: Asteroid density in kg/m³
            velocity_km_s: Impact velocity in km/s
            impact_angle: Impact angle in degrees (0-90)
            target_type: Type of target ('ocean', 'continental', 'urban')
        """
        self.diameter_km = diameter_km
        self.density_kg_m3 = density_kg_m3
        self.velocity_km_s = velocity_km_s
        self.impact_angle = impact_angle
        self.target_type = target_type

        # Calculate derived properties
        self.mass_kg = calculate_mass_from_diameter(diameter_km, density_kg_m3)
        self.velocity_ms = velocity_km_s * 1000
        self.impact_energy = calculate_impact_energy(self.mass_kg, self.velocity_ms)

    def simulate(self) -> Dict[str, Any]:
        """Run complete asteroid impact simulation."""
        results = {}

        # Basic impact properties
        results['diameter_km'] = self.diameter_km
        results['mass_kg'] = self.mass_kg
        results['velocity_km_s'] = self.velocity_km_s
        results['impact_energy'] = self.impact_energy
        results['tnt_equivalent_mt'] = tnt_equivalent(self.impact_energy)

        # Crater formation
        target_density = self._get_target_density()
        crater_diameter = calculate_crater_diameter(self.impact_energy, target_density)
        results['crater_diameter_km'] = crater_diameter
        results['crater_depth_km'] = crater_diameter * 0.1  # Depth ~ 1/10 diameter

        # Seismic effects
        results['earthquake_magnitude'] = richter_magnitude(self.impact_energy)

        # Atmospheric effects
        atm_effects = atmospheric_effects(self.impact_energy)
        results.update(atm_effects)

        # Blast effects
        blast_results = self._calculate_blast_effects()
        results.update(blast_results)

        # Tsunami effects (if ocean impact)
        if self.target_type == 'ocean':
            tsunami_results = self._calculate_tsunami_effects()
            results.update(tsunami_results)

        # Population and economic impact
        results['population_at_risk'] = population_at_risk(crater_diameter)
        results['estimated_casualties'] = int(results['population_at_risk'] * 0.8)  # 80% casualty rate in destruction zone

        # Global effects assessment
        results['global_effects'] = self._assess_global_effects()

        return results

    def _get_target_density(self) -> float:
        """Get target material density based on impact location."""
        densities = {
            'ocean': 1000,      # Water
            'continental': 2500, # Average rock
            'urban': 2000       # Mixed materials
        }
        return densities.get(self.target_type, 2500)

    def _calculate_blast_effects(self) -> Dict[str, Any]:
        """Calculate blast wave effects."""
        # Overpressure at various distances
        # Using simplified blast wave equations

        blast_energy = self.impact_energy * 0.1  # ~10% goes into blast wave

        # Distance for 1 bar overpressure (severe structural damage)
        # Empirical formula: R ∝ E^(1/3)
        r_1bar_m = 45 * (blast_energy / 4.184e15) ** (1/3) * 1000  # Convert to meters

        # Distance for 0.1 bar overpressure (broken windows)
        r_01bar_m = r_1bar_m * 2.5

        return {
            'blast_radius_severe_km': r_1bar_m / 1000,
            'blast_radius_moderate_km': r_01bar_m / 1000,
            'peak_overpressure_bar': self._calculate_peak_overpressure()
        }

    def _calculate_peak_overpressure(self) -> float:
        """Calculate peak overpressure at ground zero."""
        # Simplified calculation based on energy
        if self.impact_energy > 1e20:
            return min(1000, self.impact_energy / 1e17)  # Cap at 1000 bar
        else:
            return self.impact_energy / 1e17

    def _calculate_tsunami_effects(self) -> Dict[str, Any]:
        """Calculate tsunami effects for ocean impacts."""
        if self.target_type != 'ocean':
            return {}

        # Tsunami generation depends on impact energy and water depth
        water_displacement_m3 = self.impact_energy / (1000 * 9.81 * 1000)  # Simplified
          # Wave height at source
        crater_diameter_km = calculate_crater_diameter(self.impact_energy, self._get_target_density())
        source_area_m2 = math.pi * (crater_diameter_km * 500) ** 2
        initial_height_m = water_displacement_m3 / source_area_m2

        return {
            'tsunami_source_height_m': min(initial_height_m, 1000),  # Cap at 1km
            'tsunami_energy_j': self.impact_energy * 0.05,  # 5% goes to tsunami
            'affected_coastlines': self._estimate_affected_coastlines()
        }

    def _estimate_affected_coastlines(self) -> int:
        """Estimate number of affected coastlines."""
        # Very rough estimate based on energy
        if self.impact_energy > 1e22:
            return 50  # Global
        elif self.impact_energy > 1e21:
            return 20  # Multi-ocean
        elif self.impact_energy > 1e20:
            return 10  # Regional ocean
        else:
            return 3   # Local

    def _assess_global_effects(self) -> Dict[str, str]:
        """Assess global-scale effects."""
        effects = {}

        if self.impact_energy > 1e23:  # Extinction-level
            effects['climate'] = 'Global impact winter, temperature drop >10°C'
            effects['ecology'] = 'Mass extinction event, >75% species loss'
            effects['civilization'] = 'Collapse of global civilization'
        elif self.impact_energy > 1e22:  # Global catastrophe
            effects['climate'] = 'Severe global cooling, crop failures worldwide'
            effects['ecology'] = 'Major extinctions, ecosystem disruption'
            effects['civilization'] = 'Collapse of technological civilization'
        elif self.impact_energy > 1e21:  # Continental scale
            effects['climate'] = 'Regional climate disruption'
            effects['ecology'] = 'Regional ecosystem damage'
            effects['civilization'] = 'Collapse of affected region, global economic crisis'
        elif self.impact_energy > 1e20:  # Regional scale
            effects['climate'] = 'Local weather pattern disruption'
            effects['ecology'] = 'Local habitat destruction'
            effects['civilization'] = 'Regional infrastructure damage'
        else:  # Local scale
            effects['climate'] = 'Minimal global impact'
            effects['ecology'] = 'Local environmental damage'
            effects['civilization'] = 'Local infrastructure damage'

        return effects

    def get_impact_classification(self) -> str:
        """Get impact classification based on energy."""
        if self.impact_energy > 1e23:
            return "Extinction-Level Event"
        elif self.impact_energy > 1e22:
            return "Global Catastrophe"
        elif self.impact_energy > 1e21:
            return "Continental Disaster"
        elif self.impact_energy > 1e20:
            return "Regional Catastrophe"
        elif self.impact_energy > 1e19:
            return "Local Disaster"
        else:
            return "Minor Impact"

    def compare_to_historical(self) -> Dict[str, Any]:
        """Compare to known historical impacts."""
        comparisons = {}

        # Chicxulub (dinosaur extinction)
        chicxulub_energy = 1e23
        comparisons['vs_chicxulub'] = self.impact_energy / chicxulub_energy

        # Tunguska (1908)
        tunguska_energy = 1e16
        comparisons['vs_tunguska'] = self.impact_energy / tunguska_energy

        # Meteor Crater, Arizona
        meteor_crater_energy = 1e16
        comparisons['vs_meteor_crater'] = self.impact_energy / meteor_crater_energy

        return comparisons
