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
        self.global_effects = global_effects or {}

        # Calculate derived metrics
        self._calculate_derived_metrics()

    def _calculate_derived_metrics(self):
        """Calculate additional metrics based on simulation data."""
        # Calculate estimated casualties
        if self.event_type == 'asteroid':
            # Rough estimate based on crater size and population density
            crater_diameter = self.simulation_data.get('crater_diameter_km', 0)
            self.estimated_casualties = int(crater_diameter * 1000000)  # Rough estimate

            # Calculate economic impact (in billions USD)
            energy = self.simulation_data.get('impact_energy', 0)
            self.economic_impact = energy / 1e18  # Very rough scaling

        elif self.event_type == 'pandemic':
            r0 = self.simulation_data.get('r0', 1.0)
            mortality = self.simulation_data.get('mortality_rate', 0.01)
            world_population = 8e9

            # Simple epidemic model
            if r0 > 1:
                infected_fraction = 1 - (1/r0)
                self.estimated_casualties = int(world_population * infected_fraction * mortality)
            else:
                self.estimated_casualties = 0

            self.economic_impact = self.estimated_casualties * 0.01  # $10M per casualty rough estimate

        else:
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
