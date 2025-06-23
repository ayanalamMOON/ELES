from typing import Dict, Any, List, Optional
import json


class ExtinctionResult:
    """Class to store and manage extinction simulation results."""

    def __init__(self,
                 event_type: str,
                 parameters: Dict[str, Any],
                 simulation_data: Dict[str, Any],
                 severity: int = 3,
                 impacted_area: float = 0.0,
                 global_effects: Optional[Dict[str, Any]] = None):
        """
        Initialize extinction result.

        Args:
            event_type: Type of extinction event
            parameters: Input parameters for the simulation
            simulation_data: Raw simulation output data
            severity: Severity level (1-6)
            impacted_area: Directly impacted area in km²
            global_effects: Dictionary of global effects
        """
        self.event_type = event_type
        self.parameters = parameters
        self.simulation_data = simulation_data
        self.severity = severity
        self.impacted_area = impacted_area
        self.global_effects = global_effects or {}        # Calculate derived metrics
        self._calculate_derived_metrics()

    def _calculate_derived_metrics(self):
        """Calculate additional metrics based on simulation data."""
        world_population = 8e9

        # Calculate estimated casualties and economic impact based on event type
        if self.event_type == 'asteroid':
            # Use data from simulation if available, otherwise estimate
            if 'estimated_casualties' in self.simulation_data:
                self.estimated_casualties = self.simulation_data['estimated_casualties']
            else:
                # Rough estimate based on crater size and population density
                crater_diameter = self.simulation_data.get('crater_diameter_km', 0)
                self.estimated_casualties = int(crater_diameter * 1000000)

            # Calculate economic impact (in billions USD)
            if 'economic_impact_billion_usd' in self.simulation_data:
                self.economic_impact = self.simulation_data['economic_impact_billion_usd']
            else:
                energy = self.simulation_data.get('impact_energy', 0)
                self.economic_impact = energy / 1e18  # Very rough scaling

        elif self.event_type == 'pandemic':
            # Use simulation data directly if available
            if 'total_deaths' in self.simulation_data:
                self.estimated_casualties = self.simulation_data['total_deaths']
            else:
                r0 = self.simulation_data.get('r0', 1.0)
                mortality = self.simulation_data.get('mortality_rate', 0.01)

                # Simple epidemic model
                if r0 > 1:
                    infected_fraction = 1 - (1/r0)
                    self.estimated_casualties = int(world_population * infected_fraction * mortality)
                else:
                    self.estimated_casualties = 0            # Economic impact based on casualties and disruption
            if 'economic_impact_billion_usd' in self.simulation_data:
                self.economic_impact = self.simulation_data['economic_impact_billion_usd']
            else:
                # More realistic economic impact: $1M per casualty + disruption costs
                self.economic_impact = (self.estimated_casualties / 1000000) + (self.estimated_casualties * 0.001)

        elif self.event_type == 'supervolcano':
            vei = self.simulation_data.get('vei', 6)

            # Estimate casualties based on VEI scale
            if vei >= 8:
                self.estimated_casualties = int(world_population * 0.75)  # 75% of world population
            elif vei >= 7:
                self.estimated_casualties = int(world_population * 0.25)  # 25% of world population
            elif vei >= 6:
                self.estimated_casualties = int(world_population * 0.05)  # 5% of world population
            elif vei >= 5:
                self.estimated_casualties = int(world_population * 0.01)  # 1% of world population
            else:
                self.estimated_casualties = int(world_population * 0.001)  # 0.1% of world population
              # Economic impact based on global disruption (more realistic scaling)
            if vei >= 8:
                self.economic_impact = 50000  # $50 trillion for VEI 8
            elif vei >= 7:
                self.economic_impact = 20000  # $20 trillion for VEI 7
            elif vei >= 6:
                self.economic_impact = 5000   # $5 trillion for VEI 6
            else:
                self.economic_impact = vei * 500  # $500B per VEI level for smaller eruptions

        elif self.event_type == 'climate_collapse':
            temp_change = abs(self.simulation_data.get('temperature_change_c', 0))

            # Estimate casualties based on temperature change severity
            if temp_change >= 15:
                self.estimated_casualties = int(world_population * 0.90)  # 90% population loss
            elif temp_change >= 10:
                self.estimated_casualties = int(world_population * 0.60)  # 60% population loss
            elif temp_change >= 7:
                self.estimated_casualties = int(world_population * 0.30)  # 30% population loss
            elif temp_change >= 5:
                self.estimated_casualties = int(world_population * 0.10)  # 10% population loss
            elif temp_change >= 3:
                self.estimated_casualties = int(world_population * 0.02)  # 2% population loss
            else:
                self.estimated_casualties = int(world_population * 0.005)  # 0.5% population loss
              # Economic impact based on global economic disruption (more realistic)
            if temp_change >= 15:
                self.economic_impact = 100000  # $100 trillion for extreme scenarios
            elif temp_change >= 10:
                self.economic_impact = 50000   # $50 trillion
            elif temp_change >= 7:
                self.economic_impact = 20000   # $20 trillion
            elif temp_change >= 5:
                self.economic_impact = 10000   # $10 trillion
            else:
                self.economic_impact = temp_change * 1000  # $1 trillion per degree

        elif self.event_type == 'gamma_ray_burst':
            distance = self.simulation_data.get('distance_ly', 1000)

            # Estimate casualties based on distance (closer = more dangerous)
            if distance <= 500:
                self.estimated_casualties = int(world_population * 0.95)  # 95% population loss
            elif distance <= 1000:
                self.estimated_casualties = int(world_population * 0.70)  # 70% population loss
            elif distance <= 2000:
                self.estimated_casualties = int(world_population * 0.40)  # 40% population loss
            elif distance <= 3000:
                self.estimated_casualties = int(world_population * 0.15)  # 15% population loss
            elif distance <= 5000:
                self.estimated_casualties = int(world_population * 0.05)  # 5% population loss
            else:
                self.estimated_casualties = int(world_population * 0.01)  # 1% population loss
              # Economic impact based on radiation damage and recovery costs (more realistic)
            if distance <= 500:
                self.economic_impact = 80000  # $80 trillion for close bursts
            elif distance <= 1000:
                self.economic_impact = 40000  # $40 trillion
            elif distance <= 2000:
                self.economic_impact = 15000  # $15 trillion
            elif distance <= 3000:
                self.economic_impact = 5000   # $5 trillion
            else:
                self.economic_impact = max(100, 10000 / (distance / 1000))  # Scaling with distance

        elif self.event_type == 'ai_extinction':
            ai_level = self.simulation_data.get('ai_level', 5)

            # Estimate casualties based on AI capability level
            if ai_level >= 9:
                self.estimated_casualties = int(world_population * 0.99)  # 99% population loss
            elif ai_level >= 8:
                self.estimated_casualties = int(world_population * 0.85)  # 85% population loss
            elif ai_level >= 7:
                self.estimated_casualties = int(world_population * 0.60)  # 60% population loss
            elif ai_level >= 6:
                self.estimated_casualties = int(world_population * 0.30)  # 30% population loss
            elif ai_level >= 4:
                self.estimated_casualties = int(world_population * 0.10)  # 10% population loss
            else:
                self.estimated_casualties = int(world_population * 0.01)  # 1% population loss
              # Economic impact based on technological disruption (more realistic)
            if ai_level >= 9:
                self.economic_impact = 120000  # $120 trillion for extreme AI scenarios
            elif ai_level >= 8:
                self.economic_impact = 60000   # $60 trillion
            elif ai_level >= 7:
                self.economic_impact = 25000   # $25 trillion
            elif ai_level >= 6:
                self.economic_impact = 10000   # $10 trillion
            else:
                self.economic_impact = ai_level * 1000  # $1 trillion per AI level

        else:
            # Default values for unknown event types
            self.estimated_casualties = 0
            self.economic_impact = 0.0

    def get_severity_description(self) -> str:
        """Get human-readable severity description."""
        severity_map = {
            1: "Minimal Impact",
            2: "Local Catastrophe",
            3: "Regional Disaster",
            4: "Continental Crisis",
            5: "Global Catastrophe",
            6: "Extinction Level Event"
        }
        return severity_map.get(self.severity, "Unknown")

    def get_recovery_time_estimate(self) -> str:
        """Estimate recovery time based on severity."""
        if self.severity <= 2:
            return "1-10 years"
        elif self.severity == 3:
            return "10-100 years"
        elif self.severity == 4:
            return "100-1000 years"
        elif self.severity == 5:
            return "1000-10000 years"
        else:
            return "May never recover"

    def summary(self) -> Dict[str, Any]:
        """Return comprehensive summary of results."""
        return {
            "event_type": self.event_type,
            "severity": self.severity,
            "severity_description": self.get_severity_description(),
            "parameters": self.parameters,
            "impacted_area_km2": self.impacted_area,
            "estimated_casualties": getattr(self, 'estimated_casualties', 0),
            "economic_impact_billion_usd": getattr(self, 'economic_impact', 0),
            "recovery_time_estimate": self.get_recovery_time_estimate(),
            "global_effects": self.global_effects,
            "simulation_data": self.simulation_data
        }

    def to_json(self, indent: int = 2) -> str:
        """Export results to JSON string."""
        return json.dumps(self.summary(), indent=indent, default=str)

    def save_to_file(self, filepath: str):
        """Save results to JSON file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.to_json())

    def get_risk_factors(self) -> List[str]:
        """Get list of key risk factors based on event type."""
        risk_factors = []

        if self.event_type == 'asteroid':
            energy = self.simulation_data.get('impact_energy', 0)
            if energy > 1e21:
                risk_factors.append("Global climate disruption")
                risk_factors.append("Agricultural collapse")
                risk_factors.append("Massive tsunamis")
            if energy > 1e20:
                risk_factors.append("Regional infrastructure destruction")
                risk_factors.append("Firestorms")

        elif self.event_type == 'pandemic':
            r0 = self.simulation_data.get('r0', 1.0)
            mortality = self.simulation_data.get('mortality_rate', 0.01)

            if r0 > 3:
                risk_factors.append("Rapid global spread")
            if mortality > 0.1:
                risk_factors.append("High mortality rate")
            if r0 > 2 and mortality > 0.05:
                risk_factors.append("Healthcare system collapse")
                risk_factors.append("Economic disruption")

        elif self.event_type == 'supervolcano':
            vei = self.simulation_data.get('vei', 6)
            if vei >= 7:
                risk_factors.append("Global volcanic winter")
                risk_factors.append("Atmospheric ash blocking sunlight")
                risk_factors.append("Agricultural failure")

        return risk_factors

    def __str__(self) -> str:
        """String representation of the result."""
        return f"ExtinctionResult({self.event_type}, severity={self.severity})"

    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"ExtinctionResult(event_type='{self.event_type}', severity={self.severity}, casualties={getattr(self, 'estimated_casualties', 0)})"
