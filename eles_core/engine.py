import yaml
import json
import os
from typing import Dict, Any, Optional
from .extinction_result import ExtinctionResult
from .event_types.asteroid import AsteroidImpact
from .event_types.supervolcano import Supervolcano
from .event_types.climate_collapse import ClimateCollapse
from .event_types.pandemic import Pandemic
from .event_types.gamma_ray_burst import GammaRayBurst
from .event_types.ai_extinction import AIExtinction


class Engine:
    """Main simulation engine for E.L.E.S."""

    def __init__(self, config_path: str = "config/settings.yaml"):
        """Initialize the engine with configuration."""
        self.config_path = config_path
        self.settings = self._load_config()
        self.event_handlers = {
            'asteroid': AsteroidImpact,
            'supervolcano': Supervolcano,
            'climate_collapse': ClimateCollapse,
            'pandemic': Pandemic,
            'gamma_ray_burst': GammaRayBurst,
            'ai_extinction': AIExtinction
        }

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            # Return default config if file not found
            return {
                'app_name': 'E.L.E.S.',
                'version': '0.1.0',
                'simulation': {'max_iterations': 1000}
            }

    def load_scenario(self, scenario_path: str) -> Dict[str, Any]:
        """Load scenario from YAML file."""
        with open(scenario_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def run_simulation(self, event_type: str, parameters: Dict[str, Any]) -> ExtinctionResult:
        """Run simulation for a specific event type."""
        if event_type not in self.event_handlers:
            raise ValueError(f"Unknown event type: {event_type}")

        # Create event instance
        event_class = self.event_handlers[event_type]

        # Handle different parameter structures for different event types
        if event_type == 'asteroid':
            event = event_class(
                diameter_km=parameters.get('diameter_km', 1.0),
                density_kg_m3=parameters.get('density_kg_m3', 3000),
                velocity_km_s=parameters.get('velocity_km_s', 20.0)
            )
        elif event_type == 'supervolcano':
            event = event_class(
                name=parameters.get('name', 'Unknown'),
                vei=parameters.get('vei', 6)
            )
        elif event_type == 'climate_collapse':
            event = event_class(
                temperature_change_c=parameters.get('temperature_change_c', -5.0)
            )
        elif event_type == 'pandemic':
            event = event_class(
                r0=parameters.get('r0', 2.5),
                mortality_rate=parameters.get('mortality_rate', 0.1)
            )
        elif event_type == 'gamma_ray_burst':
            event = event_class(
                distance_ly=parameters.get('distance_ly', 1000)
            )
        elif event_type == 'ai_extinction':
            event = event_class(
                ai_level=parameters.get('ai_level', 5)
            )

        # Run simulation
        simulation_result = event.simulate()

        # Create extinction result
        return ExtinctionResult(
            event_type=event_type,
            parameters=parameters,
            simulation_data=simulation_result,
            severity=self._calculate_severity(event_type, simulation_result)
        )

    def _calculate_severity(self, event_type: str, simulation_data: Dict[str, Any]) -> int:
        """Calculate severity level based on simulation results."""
        # Simple severity calculation - can be enhanced
        if event_type == 'asteroid':
            energy = simulation_data.get('impact_energy', 0)
            if energy > 1e23:
                return 6  # Extinction level
            elif energy > 1e22:
                return 5  # Global
            elif energy > 1e21:
                return 4  # Continental
            elif energy > 1e20:
                return 3  # Regional
            elif energy > 1e19:
                return 2  # Local
            else:
                return 1  # Minimal

        # Default severity for other event types
        return 3

    def run(self, scenario: str) -> Optional[ExtinctionResult]:
        """Run simulation based on scenario name or parameters."""
        if isinstance(scenario, str):
            # Load scenario file
            scenario_path = os.path.join(
                self.settings.get('data', {}).get('scenarios', 'data/scenarios'),
                f"{scenario}.yaml"
            )
            if os.path.exists(scenario_path):
                scenario_data = self.load_scenario(scenario_path)
                event_type = scenario_data.get('event_type', 'asteroid')
                parameters = scenario_data.get('parameters', {})
                return self.run_simulation(event_type, parameters)
            else:
                # Default asteroid scenario
                return self.run_simulation('asteroid', {
                    'diameter_km': 1.0,
                    'density_kg_m3': 3000,
                    'velocity_km_s': 20.0
                })

        return None
