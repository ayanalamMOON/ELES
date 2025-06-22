import math
from typing import Dict, Any


class Pandemic:
    """Pandemic simulation class using epidemiological models."""

    def __init__(self, r0: float, mortality_rate: float,
                 incubation_period_days: int = 14,
                 infectious_period_days: int = 10,
                 population: int = 8000000000):
        """
        Initialize pandemic parameters.

        Args:
            r0: Basic reproduction number
            mortality_rate: Case fatality rate (0-1)
            incubation_period_days: Time from infection to symptoms
            infectious_period_days: Time person remains infectious
            population: Total susceptible population
        """
        self.r0 = r0
        self.mortality_rate = mortality_rate
        self.incubation_period_days = incubation_period_days
        self.infectious_period_days = infectious_period_days
        self.population = population

    def simulate(self) -> Dict[str, Any]:
        """Run pandemic simulation using SIR model."""
        results = {}

        # Basic parameters
        results['r0'] = self.r0
        results['mortality_rate'] = self.mortality_rate
        results['population'] = self.population

        # SIR model calculations
        if self.r0 > 1:
            # Calculate final epidemic size using SIR model
            final_size = self._calculate_final_epidemic_size()
            results['total_infected'] = int(final_size * self.population)
            results['total_deaths'] = int(results['total_infected'] * self.mortality_rate)
            results['peak_infected'] = int(results['total_infected'] * 0.1)  # Rough estimate

            # Timeline estimates
            results['epidemic_duration_days'] = self._estimate_duration()
            results['peak_day'] = results['epidemic_duration_days'] // 3

        else:
            # R0 <= 1 means outbreak dies out
            results['total_infected'] = min(1000, int(self.population * 0.001))
            results['total_deaths'] = int(results['total_infected'] * self.mortality_rate)
            results['peak_infected'] = results['total_infected']
            results['epidemic_duration_days'] = 30
            results['peak_day'] = 15

        # Healthcare impact
        healthcare_impact = self._calculate_healthcare_impact(results['peak_infected'])
        results.update(healthcare_impact)

        # Economic impact
        economic_impact = self._calculate_economic_impact(results['total_infected'])
        results.update(economic_impact)

        # Social disruption
        social_impact = self._calculate_social_impact()
        results.update(social_impact)

        return results

    def _calculate_final_epidemic_size(self) -> float:
        """Calculate final epidemic size using SIR model approximation."""
        if self.r0 <= 1:
            return 0.001  # Minimal outbreak

        # Numerical solution to: z = 1 - exp(-R0 * z)
        # where z is the final fraction infected
        z = 0.5  # Initial guess
        for _ in range(20):  # Iterative solution
            z_new = 1 - math.exp(-self.r0 * z)
            if abs(z_new - z) < 0.001:
                break
            z = z_new

        return min(z, 0.95)  # Cap at 95% of population

    def _estimate_duration(self) -> int:
        """Estimate total epidemic duration."""
        # Rough estimate based on R0 and infectious period
        if self.r0 > 3:
            return 365 * 2  # 2 years for highly contagious
        elif self.r0 > 2:
            return 365  # 1 year
        else:
            return 180  # 6 months

    def _calculate_healthcare_impact(self, peak_infected: int) -> Dict[str, Any]:
        """Calculate healthcare system impact."""
        # Assume hospitalization rate based on severity
        if self.mortality_rate > 0.1:
            hospitalization_rate = 0.3
        elif self.mortality_rate > 0.05:
            hospitalization_rate = 0.2
        else:
            hospitalization_rate = 0.1

        peak_hospitalizations = int(peak_infected * hospitalization_rate)

        # Global hospital capacity (very rough estimate)
        global_hospital_beds = 15000000  # ~15M beds globally

        return {
            'peak_hospitalizations': peak_hospitalizations,
            'hospital_capacity_exceeded': peak_hospitalizations > global_hospital_beds,
            'healthcare_system_stress': min(10, peak_hospitalizations / global_hospital_beds * 10)
        }

    def _calculate_economic_impact(self, total_infected: int) -> Dict[str, Any]:
        """Calculate economic impact."""
        # Global GDP roughly $100 trillion
        global_gdp = 100e12

        # Economic impact based on infection rate and mortality
        infection_rate = total_infected / self.population

        # GDP loss percentage
        if infection_rate > 0.5 and self.mortality_rate > 0.1:
            gdp_loss_percent = 50  # Civilization collapse level
        elif infection_rate > 0.3 and self.mortality_rate > 0.05:
            gdp_loss_percent = 30  # Severe recession
        elif infection_rate > 0.1:
            gdp_loss_percent = 15  # Major recession
        else:
            gdp_loss_percent = 5   # Moderate impact

        economic_loss = global_gdp * (gdp_loss_percent / 100)

        return {
            'gdp_loss_percent': gdp_loss_percent,
            'economic_loss_usd': economic_loss,
            'unemployment_rate_peak': min(50, gdp_loss_percent * 0.8)
        }

    def _calculate_social_impact(self) -> Dict[str, str]:
        """Calculate social and civilization impact."""
        impact = {}

        if self.mortality_rate > 0.3 and self.r0 > 5:
            impact['social_order'] = 'Complete breakdown of social institutions'
            impact['governance'] = 'Collapse of government structures'
            impact['technology'] = 'Loss of technological civilization'
        elif self.mortality_rate > 0.15 and self.r0 > 3:
            impact['social_order'] = 'Severe social disruption'
            impact['governance'] = 'Martial law, authoritarian measures'
            impact['technology'] = 'Significant technological regression'
        elif self.mortality_rate > 0.05:
            impact['social_order'] = 'Moderate social disruption'
            impact['governance'] = 'Emergency powers, restricted freedoms'
            impact['technology'] = 'Temporary technological disruption'
        else:
            impact['social_order'] = 'Manageable social stress'
            impact['governance'] = 'Enhanced public health measures'
            impact['technology'] = 'Accelerated digital transformation'

        return impact

    def get_severity_classification(self) -> str:
        """Get pandemic severity classification."""
        if self.mortality_rate > 0.3:
            return "Civilization-Ending Pandemic"
        elif self.mortality_rate > 0.15:
            return "Catastrophic Pandemic"
        elif self.mortality_rate > 0.05:
            return "Severe Pandemic"
        elif self.mortality_rate > 0.02:
            return "Major Pandemic"
        else:
            return "Moderate Pandemic"

    def compare_to_historical(self) -> Dict[str, float]:
        """Compare to historical pandemics."""
        comparisons = {}

        # 1918 Spanish Flu (R0~2, mortality ~3%)
        spanish_flu_severity = 2.0 * 0.03
        current_severity = self.r0 * self.mortality_rate
        comparisons['vs_spanish_flu'] = current_severity / spanish_flu_severity

        # Black Death (~50% mortality, lower R0)
        black_death_severity = 1.5 * 0.5
        comparisons['vs_black_death'] = current_severity / black_death_severity

        # COVID-19 (R0~2.5, mortality ~1%)
        covid_severity = 2.5 * 0.01
        comparisons['vs_covid19'] = current_severity / covid_severity

        return comparisons
