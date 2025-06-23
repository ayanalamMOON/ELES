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
            )        # Run simulation
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

        elif event_type == 'pandemic':
            total_deaths = simulation_data.get('total_deaths', 0)
            if total_deaths > 2e9:  # > 2 billion deaths
                return 6  # Extinction level
            elif total_deaths > 1e9:  # > 1 billion deaths
                return 5  # Global catastrophe
            elif total_deaths > 1e8:  # > 100 million deaths
                return 4  # Continental
            elif total_deaths > 1e7:  # > 10 million deaths
                return 3  # Regional
            elif total_deaths > 1e6:  # > 1 million deaths
                return 2  # Local
            else:
                return 1  # Minimal

        elif event_type == 'supervolcano':
            vei = simulation_data.get('vei', 6)
            if vei >= 8:
                return 6  # Extinction level
            elif vei >= 7:
                return 5  # Global catastrophe
            elif vei >= 6:
                return 4  # Continental
            elif vei >= 5:
                return 3  # Regional
            elif vei >= 4:
                return 2  # Local
            else:
                return 1  # Minimal

        elif event_type == 'climate_collapse':
            temp_change = abs(simulation_data.get('temperature_change_c', 0))
            if temp_change >= 15:
                return 6  # Extinction level
            elif temp_change >= 10:
                return 5  # Global catastrophe
            elif temp_change >= 7:
                return 4  # Continental
            elif temp_change >= 5:
                return 3  # Regional
            elif temp_change >= 3:
                return 2  # Local
            else:
                return 1  # Minimal

        elif event_type == 'gamma_ray_burst':
            distance = simulation_data.get('distance_ly', 1000)
            if distance <= 500:
                return 6  # Extinction level
            elif distance <= 1000:
                return 5  # Global catastrophe
            elif distance <= 2000:
                return 4  # Continental
            elif distance <= 3000:
                return 3  # Regional
            elif distance <= 5000:
                return 2  # Local
            else:
                return 1  # Minimal

        elif event_type == 'ai_extinction':
            ai_level = simulation_data.get('ai_level', 5)
            if ai_level >= 9:
                return 6  # Extinction level
            elif ai_level >= 8:
                return 5  # Global catastrophe
            elif ai_level >= 7:
                return 4  # Continental
            elif ai_level >= 6:
                return 3  # Regional
            elif ai_level >= 4:
                return 2  # Local
            else:
                return 1  # Minimal

        # Default severity for unknown event types
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
