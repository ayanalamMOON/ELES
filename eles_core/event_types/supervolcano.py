import math
from typing import Dict, Any, Optional


class Supervolcano:
    """Supervolcano eruption simulation class."""

    def __init__(self, name: str, vei: int, magma_volume_km3: Optional[float] = None):
        """
        Initialize supervolcano parameters.

        Args:
            name: Name of the volcano
            vei: Volcanic Explosivity Index (0-8)
            magma_volume_km3: Volume of magma in km³ (calculated from VEI if not provided)
        """
        self.name = name
        self.vei = vei
        self.magma_volume_km3 = magma_volume_km3 or self._calculate_magma_volume()

    def _calculate_magma_volume(self) -> float:
        """Calculate magma volume from VEI."""
        # VEI scale is logarithmic
        # VEI 8 = 1000+ km³, VEI 7 = 100-1000 km³, etc.
        if self.vei >= 8:
            return 1000 + (self.vei - 8) * 1000
        elif self.vei == 7:
            return 100
        elif self.vei == 6:
            return 10
        elif self.vei == 5:
            return 1
        else:
            return 0.1 * (10 ** (self.vei - 4))

    def simulate(self) -> Dict[str, Any]:
        """Run supervolcano eruption simulation."""
        results = {}

        # Basic eruption properties
        results['volcano_name'] = self.name
        results['vei'] = self.vei
        results['magma_volume_km3'] = self.magma_volume_km3
        results['ash_volume_km3'] = self.magma_volume_km3 * 2  # Ash expansion

        # Eruption energy (rough estimate)
        results['eruption_energy_j'] = self.magma_volume_km3 * 1e15  # Very rough

        # Ash dispersal
        ash_effects = self._calculate_ash_effects()
        results.update(ash_effects)

        # Climate effects
        climate_effects = self._calculate_climate_effects()
        results.update(climate_effects)

        # Local destruction
        local_effects = self._calculate_local_effects()
        results.update(local_effects)

        # Global impact assessment
        results['global_impact'] = self._assess_global_impact()

        return results

    def _calculate_ash_effects(self) -> Dict[str, Any]:
        """Calculate ash cloud and fallout effects."""
        effects = {}

        # Ash cloud height (empirical relationship with VEI)
        if self.vei >= 7:
            effects['ash_cloud_height_km'] = 35 + (self.vei - 7) * 10  # Into stratosphere
        else:
            effects['ash_cloud_height_km'] = 5 * self.vei

        # Ash dispersal area
        if self.vei >= 8:
            effects['ash_dispersal_area_km2'] = 50000000  # Continental scale
        elif self.vei == 7:
            effects['ash_dispersal_area_km2'] = 10000000  # Subcontinental
        else:
            effects['ash_dispersal_area_km2'] = 1000000 * (self.vei - 5)

        # Ash thickness at various distances
        effects['ash_thickness_10km_m'] = max(0, self.magma_volume_km3 / 10)
        effects['ash_thickness_100km_m'] = max(0, self.magma_volume_km3 / 100)
        effects['ash_thickness_1000km_m'] = max(0, self.magma_volume_km3 / 10000)

        return effects

    def _calculate_climate_effects(self) -> Dict[str, Any]:
        """Calculate global climate effects."""
        effects = {}

        # Temperature drop based on VEI and sulfur injection
        if self.vei >= 8:
            effects['temperature_drop_c'] = 5 + (self.vei - 8) * 2
            effects['cooling_duration_years'] = 5 + (self.vei - 8) * 3
        elif self.vei == 7:
            effects['temperature_drop_c'] = 3
            effects['cooling_duration_years'] = 3
        elif self.vei == 6:
            effects['temperature_drop_c'] = 1
            effects['cooling_duration_years'] = 1
        else:
            effects['temperature_drop_c'] = 0
            effects['cooling_duration_years'] = 0

        # Reduced sunlight
        if self.vei >= 7:
            effects['sunlight_reduction_percent'] = min(90, self.vei * 10)
            effects['darkness_duration_months'] = min(24, self.vei * 2)
        else:
            effects['sunlight_reduction_percent'] = 0
            effects['darkness_duration_months'] = 0

        return effects

    def _calculate_local_effects(self) -> Dict[str, Any]:
        """Calculate local destruction effects."""
        effects = {}

        # Pyroclastic flow range
        if self.vei >= 7:
            effects['pyroclastic_flow_range_km'] = 100 + (self.vei - 7) * 50
        else:
            effects['pyroclastic_flow_range_km'] = max(0, self.vei * 10)

        # Lava flow area
        effects['lava_flow_area_km2'] = self.magma_volume_km3 * 10  # Rough estimate

        # Local casualties
        destruction_area = math.pi * effects['pyroclastic_flow_range_km'] ** 2
        population_density = 50  # people per km²
        effects['immediate_casualties'] = int(destruction_area * population_density)

        return effects

    def _assess_global_impact(self) -> Dict[str, str]:
        """Assess global impact level."""
        impact = {}

        if self.vei >= 8:
            impact['severity'] = 'Extinction-level volcanic winter'
            impact['agriculture'] = 'Global crop failure for multiple years'
            impact['civilization'] = 'Collapse of modern civilization'
            impact['ecosystem'] = 'Mass extinction event'
        elif self.vei == 7:
            impact['severity'] = 'Global catastrophe'
            impact['agriculture'] = 'Widespread crop failures'
            impact['civilization'] = 'Severe disruption to global economy'
            impact['ecosystem'] = 'Significant species loss'
        elif self.vei == 6:
            impact['severity'] = 'Regional catastrophe with global effects'
            impact['agriculture'] = 'Regional crop failures'
            impact['civilization'] = 'Regional economic collapse'
            impact['ecosystem'] = 'Local ecosystem destruction'
        else:
            impact['severity'] = 'Local to regional impact'
            impact['agriculture'] = 'Local agricultural impact'
            impact['civilization'] = 'Local infrastructure damage'
            impact['ecosystem'] = 'Local environmental damage'

        return impact

    def get_historical_comparison(self) -> Dict[str, float]:
        """Compare to historical eruptions."""
        comparisons = {}

        # Toba supervolcano (74,000 years ago, VEI 8)
        if self.vei >= 8:
            comparisons['vs_toba'] = self.magma_volume_km3 / 2800

        # Tambora 1815 (VEI 7)
        if self.vei >= 6:
            comparisons['vs_tambora'] = self.magma_volume_km3 / 160

        # Krakatoa 1883 (VEI 6)
        if self.vei >= 5:
            comparisons['vs_krakatoa'] = self.magma_volume_km3 / 25

        return comparisons
