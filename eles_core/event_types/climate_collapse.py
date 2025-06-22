import math
from typing import Dict, Any


class ClimateCollapse:
    """Climate collapse simulation class."""

    def __init__(self, temperature_change_c: float,
                 co2_concentration_ppm: float = 400,
                 timeframe_years: int = 100):
        """
        Initialize climate collapse parameters.

        Args:
            temperature_change_c: Global temperature change in Celsius
            co2_concentration_ppm: Atmospheric CO2 concentration in ppm
            timeframe_years: Timeframe over which change occurs
        """
        self.temperature_change_c = temperature_change_c
        self.co2_concentration_ppm = co2_concentration_ppm
        self.timeframe_years = timeframe_years

    def simulate(self) -> Dict[str, Any]:
        """Run climate collapse simulation."""
        results = {}

        # Basic parameters
        results['temperature_change_c'] = self.temperature_change_c
        results['co2_concentration_ppm'] = self.co2_concentration_ppm
        results['timeframe_years'] = self.timeframe_years

        # Sea level effects
        sea_level_effects = self._calculate_sea_level_effects()
        results.update(sea_level_effects)

        # Agricultural effects
        agricultural_effects = self._calculate_agricultural_effects()
        results.update(agricultural_effects)

        # Ecosystem effects
        ecosystem_effects = self._calculate_ecosystem_effects()
        results.update(ecosystem_effects)

        # Human impacts
        human_impacts = self._calculate_human_impacts()
        results.update(human_impacts)

        # Tipping points
        tipping_points = self._assess_tipping_points()
        results.update(tipping_points)

        return results

    def _calculate_sea_level_effects(self) -> Dict[str, Any]:
        """Calculate sea level rise effects."""
        effects = {}

        # Sea level rise based on temperature change
        # Rough estimate: ~2.3m per degree of warming (long-term)
        if self.temperature_change_c > 0:
            sea_level_rise_m = self.temperature_change_c * 2.3
            effects['sea_level_rise_m'] = sea_level_rise_m

            # Coastal flooding
            if sea_level_rise_m > 5:
                effects['coastal_cities_flooded'] = 'Most major coastal cities uninhabitable'
                effects['displaced_population'] = 1e9  # 1 billion people
            elif sea_level_rise_m > 2:
                effects['coastal_cities_flooded'] = 'Many coastal areas flooded'
                effects['displaced_population'] = 5e8  # 500 million people
            elif sea_level_rise_m > 0.5:
                effects['coastal_cities_flooded'] = 'Some coastal flooding'
                effects['displaced_population'] = 1e8  # 100 million people
            else:
                effects['coastal_cities_flooded'] = 'Minimal coastal impact'
                effects['displaced_population'] = 1e6  # 1 million people
        else:
            # Cooling scenario - potential ice age
            if self.temperature_change_c < -5:
                effects['ice_sheet_expansion'] = 'Major ice sheet advance'
                effects['sea_level_rise_m'] = -50  # Sea level drop
                effects['displaced_population'] = 2e9  # 2 billion due to ice advance
            else:
                effects['ice_sheet_expansion'] = 'Minimal'
                effects['sea_level_rise_m'] = 0
                effects['displaced_population'] = 0

        return effects

    def _calculate_agricultural_effects(self) -> Dict[str, Any]:
        """Calculate effects on agriculture."""
        effects = {}

        if self.temperature_change_c > 0:  # Warming scenario
            if self.temperature_change_c > 4:
                effects['crop_yield_change'] = -0.6  # 60% reduction
                effects['arable_land_change'] = -0.3  # 30% loss
                effects['food_security'] = 'Severe global famine'
            elif self.temperature_change_c > 2:
                effects['crop_yield_change'] = -0.3  # 30% reduction
                effects['arable_land_change'] = -0.1  # 10% loss
                effects['food_security'] = 'Significant food shortages'
            else:
                effects['crop_yield_change'] = -0.1  # 10% reduction
                effects['arable_land_change'] = 0.05  # 5% gain (northern regions)
                effects['food_security'] = 'Regional food stress'

        else:  # Cooling scenario
            if self.temperature_change_c < -3:
                effects['crop_yield_change'] = -0.8  # 80% reduction
                effects['arable_land_change'] = -0.5  # 50% loss
                effects['food_security'] = 'Civilizational collapse due to famine'
            elif self.temperature_change_c < -1:
                effects['crop_yield_change'] = -0.4  # 40% reduction
                effects['arable_land_change'] = -0.2  # 20% loss
                effects['food_security'] = 'Major global famine'
            else:
                effects['crop_yield_change'] = -0.1  # 10% reduction
                effects['arable_land_change'] = -0.05  # 5% loss
                effects['food_security'] = 'Regional crop failures'

        return effects

    def _calculate_ecosystem_effects(self) -> Dict[str, Any]:
        """Calculate ecosystem effects."""
        effects = {}

        temp_change_abs = abs(self.temperature_change_c)

        if temp_change_abs > 5:
            effects['species_extinction_rate'] = 0.7  # 70% species loss
            effects['ecosystem_collapse'] = 'Complete biosphere collapse'
            effects['coral_reef_survival'] = 0  # Total bleaching
        elif temp_change_abs > 3:
            effects['species_extinction_rate'] = 0.4  # 40% species loss
            effects['ecosystem_collapse'] = 'Major ecosystem disruption'
            effects['coral_reef_survival'] = 0.1  # 90% loss
        elif temp_change_abs > 2:
            effects['species_extinction_rate'] = 0.2  # 20% species loss
            effects['ecosystem_collapse'] = 'Significant ecosystem stress'
            effects['coral_reef_survival'] = 0.3  # 70% loss
        else:
            effects['species_extinction_rate'] = 0.05  # 5% species loss
            effects['ecosystem_collapse'] = 'Ecosystem adaptation'
            effects['coral_reef_survival'] = 0.7  # 30% loss

        # Forest effects
        if self.temperature_change_c > 3:
            effects['forest_dieback'] = 'Amazon and boreal forest collapse'
        elif self.temperature_change_c > 1.5:
            effects['forest_dieback'] = 'Significant forest stress'
        elif self.temperature_change_c < -2:
            effects['forest_dieback'] = 'Temperate forest die-off'
        else:
            effects['forest_dieback'] = 'Forest migration'

        return effects

    def _calculate_human_impacts(self) -> Dict[str, Any]:
        """Calculate impacts on human civilization."""
        effects = {}

        # Population at risk
        displaced_pop = self._calculate_sea_level_effects().get('displaced_population', 0)
        food_security = self._calculate_agricultural_effects().get('food_security', '')

        if 'civilizational collapse' in food_security.lower():
            effects['population_at_risk'] = 7e9  # Nearly all humanity
            effects['civilization_status'] = 'Collapse of technological civilization'
            effects['economic_impact_percent'] = 90
        elif 'severe' in food_security.lower() or displaced_pop > 5e8:
            effects['population_at_risk'] = 4e9  # 4 billion people
            effects['civilization_status'] = 'Severe regression of civilization'
            effects['economic_impact_percent'] = 60
        elif 'significant' in food_security.lower() or displaced_pop > 1e8:
            effects['population_at_risk'] = 2e9  # 2 billion people
            effects['civilization_status'] = 'Major social upheaval'
            effects['economic_impact_percent'] = 30
        else:
            effects['population_at_risk'] = 5e8  # 500 million people
            effects['civilization_status'] = 'Adaptation with stress'
            effects['economic_impact_percent'] = 10

        # Migration and conflict
        if displaced_pop > 1e9:
            effects['migration_crisis'] = 'Unprecedented global migration'
            effects['conflict_risk'] = 'High - resource wars likely'
        elif displaced_pop > 5e8:
            effects['migration_crisis'] = 'Massive regional migrations'
            effects['conflict_risk'] = 'Elevated - regional conflicts'
        else:
            effects['migration_crisis'] = 'Manageable migration'
            effects['conflict_risk'] = 'Moderate - local tensions'

        return effects

    def _assess_tipping_points(self) -> Dict[str, Any]:
        """Assess climate tipping points."""
        tipping_points = {}

        if self.temperature_change_c > 1.5:
            triggered_points = []

            if self.temperature_change_c > 1.5:
                triggered_points.append('Arctic sea ice loss')
            if self.temperature_change_c > 2:
                triggered_points.append('Greenland ice sheet collapse')
            if self.temperature_change_c > 3:
                triggered_points.append('Amazon rainforest dieback')
                triggered_points.append('West Antarctic ice sheet collapse')
            if self.temperature_change_c > 4:
                triggered_points.append('Permafrost thaw and methane release')
                triggered_points.append('Atlantic circulation shutdown')

            tipping_points['triggered_tipping_points'] = triggered_points
            tipping_points['cascading_risk'] = len(triggered_points) > 2
        else:
            tipping_points['triggered_tipping_points'] = []
            tipping_points['cascading_risk'] = False

        return tipping_points

    def get_scenario_type(self) -> str:
        """Get climate scenario classification."""
        if self.temperature_change_c > 5:
            return "Runaway Greenhouse Effect"
        elif self.temperature_change_c > 3:
            return "Catastrophic Warming"
        elif self.temperature_change_c > 2:
            return "Dangerous Warming"
        elif self.temperature_change_c > 0:
            return "Moderate Warming"
        elif self.temperature_change_c < -5:
            return "Snowball Earth"
        elif self.temperature_change_c < -2:
            return "Ice Age"
        else:
            return "Moderate Cooling"

    def get_timeline_effects(self) -> Dict[str, str]:
        """Get timeline of effects."""
        timeline = {}

        if self.timeframe_years <= 10:
            timeline['immediate'] = 'Rapid climate shock'
            timeline['short_term'] = 'Ecosystem collapse'
            timeline['long_term'] = 'Civilization adaptation or collapse'
        elif self.timeframe_years <= 50:
            timeline['immediate'] = 'Accelerating change'
            timeline['short_term'] = 'Infrastructure stress'
            timeline['long_term'] = 'Managed adaptation'
        else:
            timeline['immediate'] = 'Gradual change'
            timeline['short_term'] = 'Adaptive measures'
            timeline['long_term'] = 'Long-term adaptation'

        return timeline
