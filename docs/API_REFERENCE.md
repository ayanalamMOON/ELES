# E.L.E.S. API Reference

Complete API documentation for the Extinction-Level Event Simulator (E.L.E.S.) Python library.

## 🎯 Overview

The E.L.E.S. API provides programmatic access to extinction-level event simulations through Python. The API is designed to be intuitive, well-documented, and suitable for both interactive use and integration into larger applications.

## 📦 Package Structure

```
eles_core/
├── __init__.py              # Main package interface
├── engine.py                # Core simulation engine
├── extinction_result.py     # Result container and analysis
├── utils.py                 # Utility functions and calculations
└── event_types/
    ├── __init__.py          # Event types interface
    ├── asteroid.py          # Asteroid impact simulations
    ├── supervolcano.py      # Supervolcanic eruption simulations
    ├── climate_collapse.py  # Climate collapse simulations
    ├── pandemic.py          # Pandemic and disease simulations
    ├── gamma_ray_burst.py   # Gamma-ray burst simulations
    └── ai_extinction.py     # AI extinction risk simulations
```

## 🚀 Quick Start

### Basic Usage

```python
from eles_core import Engine, create_engine

# Create simulation engine
engine = create_engine()

# Run a basic asteroid simulation
result = engine.run_simulation('asteroid', {
    'diameter_km': 2.0,
    'velocity_km_s': 20.0,
    'density_kg_m3': 3500
})

# Analyze results
print(f"Severity: {result.severity}/6")
print(f"Casualties: {result.estimated_casualties:,}")
print(f"Economic Impact: ${result.economic_impact:.1f}B")
```

### Advanced Usage

```python
from eles_core import Engine, AsteroidImpact
from eles_core.utils import calculate_impact_energy

# Create engine with custom configuration
engine = Engine("config/custom_settings.yaml")

# Create event directly
asteroid = AsteroidImpact(
    diameter_km=1.0,
    density_kg_m3=3000,
    velocity_km_s=25.0,
    target_type="ocean"
)

# Run simulation
simulation_data = asteroid.simulate()

# Get impact energy
energy = calculate_impact_energy(asteroid.mass_kg, asteroid.velocity_ms)
print(f"Impact Energy: {energy:.2e} Joules")
```

## 🔧 Core Classes

### Engine

Main simulation engine for running extinction event simulations.

```python
class Engine:
    def __init__(self, config_path: str = "config/settings.yaml")
    def run_simulation(self, event_type: str, parameters: Dict[str, Any]) -> ExtinctionResult
    def load_scenario(self, scenario_path: str) -> Dict[str, Any]
    def run(self, scenario: str) -> Optional[ExtinctionResult]
```

#### Methods

##### `__init__(config_path: str = "config/settings.yaml")`

Initialize the simulation engine.

**Parameters:**

- `config_path` (str): Path to YAML configuration file

**Example:**

```python
engine = Engine("config/custom_settings.yaml")
```

##### `run_simulation(event_type: str, parameters: Dict[str, Any]) -> ExtinctionResult`

Run a simulation for a specific event type with custom parameters.

**Parameters:**

- `event_type` (str): Type of event ("asteroid", "pandemic", "supervolcano", "climate_collapse", "gamma_ray_burst", "ai_extinction")
- `parameters` (Dict[str, Any]): Event-specific parameters

**Returns:**

- `ExtinctionResult`: Complete simulation results

**Example:**

```python
result = engine.run_simulation('pandemic', {
    'r0': 3.5,
    'mortality_rate': 0.02
})
```

##### `load_scenario(scenario_path: str) -> Dict[str, Any]`

Load a predefined scenario from a YAML file.

**Parameters:**

- `scenario_path` (str): Path to scenario file

**Returns:**

- `Dict[str, Any]`: Scenario configuration

**Example:**

```python
scenario = engine.load_scenario("data/scenarios/chicxulub.yaml")
```

##### `run(scenario: str) -> Optional[ExtinctionResult]`

Run a simulation using a predefined scenario name.

**Parameters:**

- `scenario` (str): Name of predefined scenario

**Returns:**

- `ExtinctionResult` or `None`: Simulation results

**Example:**

```python
result = engine.run("tunguska")
```

### ExtinctionResult

Container for simulation results with analysis methods.

```python
class ExtinctionResult:
    def __init__(self, event_type: str, parameters: Dict[str, Any],
                 simulation_data: Dict[str, Any], severity: int = 3)
    def summary(self) -> Dict[str, Any]
    def to_json(self) -> str
    def get_recovery_time_estimate(self) -> str
    def get_risk_factors(self) -> List[str]
```

#### Properties

- `event_type` (str): Type of extinction event
- `parameters` (Dict[str, Any]): Input parameters used
- `simulation_data` (Dict[str, Any]): Raw simulation output
- `severity` (int): Severity level (1-6)
- `estimated_casualties` (int): Estimated total casualties
- `economic_impact` (float): Economic impact in billions USD
- `impacted_area` (float): Directly impacted area in km²
- `global_effects` (Dict[str, Any]): Global effects and consequences

#### Methods

##### `summary() -> Dict[str, Any]`

Generate a comprehensive summary of simulation results.

**Returns:**

- `Dict[str, Any]`: Summary including key metrics and descriptions

**Example:**

```python
summary = result.summary()
print(f"Event: {summary['event_type']}")
print(f"Severity: {summary['severity_description']}")
```

##### `to_json() -> str`

Export complete results as JSON string.

**Returns:**

- `str`: JSON representation of all simulation data

**Example:**

```python
json_data = result.to_json()
with open('simulation_results.json', 'w') as f:
    f.write(json_data)
```

##### `get_recovery_time_estimate() -> str`

Get estimated recovery time based on severity.

**Returns:**

- `str`: Human-readable recovery time estimate

**Example:**

```python
recovery = result.get_recovery_time_estimate()
print(f"Recovery time: {recovery}")
```

##### `get_risk_factors() -> List[str]`

Get list of key risk factors for this event type.

**Returns:**

- `List[str]`: List of risk factor descriptions

**Example:**

```python
risks = result.get_risk_factors()
for risk in risks:
    print(f"- {risk}")
```

## 🌍 Event Types

### Asteroid Impact

Simulate asteroid or comet impacts with Earth.

```python
class AsteroidImpact:
    def __init__(self, diameter_km: float, density_kg_m3: float,
                 velocity_km_s: float, impact_angle: float = 45.0,
                 target_type: str = "continental")
    def simulate(self) -> Dict[str, Any]
```

#### Parameters

- `diameter_km` (float): Asteroid diameter in kilometers (0.01 - 50.0)
- `density_kg_m3` (float): Asteroid density in kg/m³ (1000 - 15000)
- `velocity_km_s` (float): Impact velocity in km/s (10 - 80)
- `impact_angle` (float): Impact angle in degrees (15 - 90)
- `target_type` (str): Target type ("ocean", "continental", "urban")

#### Example

```python
from eles_core.event_types import AsteroidImpact

asteroid = AsteroidImpact(
    diameter_km=2.0,
    density_kg_m3=3500,
    velocity_km_s=20.0,
    target_type="continental"
)

result = asteroid.simulate()
print(f"Crater diameter: {result['crater_diameter_km']:.1f} km")
print(f"Impact energy: {result['impact_energy']:.2e} J")
```

### Pandemic

Simulate global pandemic outbreaks.

```python
class Pandemic:
    def __init__(self, r0: float, mortality_rate: float,
                 incubation_period_days: float = 5.0)
    def simulate(self) -> Dict[str, Any]
```

#### Parameters

- `r0` (float): Basic reproduction number (0.1 - 20.0)
- `mortality_rate` (float): Case fatality rate (0.001 - 0.99)
- `incubation_period_days` (float): Incubation period in days (1 - 21)

#### Example

```python
from eles_core.event_types import Pandemic

pandemic = Pandemic(
    r0=3.5,
    mortality_rate=0.02,
    incubation_period_days=7.0
)

result = pandemic.simulate()
print(f"Total deaths: {result['total_deaths']:,}")
print(f"Peak infected: {result['peak_infected']:,}")
```

### Supervolcano

Simulate supervolcanic eruptions.

```python
class Supervolcano:
    def __init__(self, name: str, vei: int)
    def simulate(self) -> Dict[str, Any]
```

#### Parameters

- `name` (str): Volcano name ("Yellowstone", "Toba", "Campi Flegrei", "Long Valley")
- `vei` (int): Volcanic Explosivity Index (4 - 8)

#### Example

```python
from eles_core.event_types import Supervolcano

volcano = Supervolcano(
    name="Yellowstone",
    vei=7
)

result = volcano.simulate()
print(f"Magma volume: {result['magma_volume_km3']:.1f} km³")
print(f"VEI: {result['vei']}")
```

### Climate Collapse

Simulate rapid climate change scenarios.

```python
class ClimateCollapse:
    def __init__(self, temperature_change_c: float)
    def simulate(self) -> Dict[str, Any]
```

#### Parameters

- `temperature_change_c` (float): Global temperature change in Celsius (-25.0 to +15.0)

#### Example

```python
from eles_core.event_types import ClimateCollapse

climate = ClimateCollapse(
    temperature_change_c=-8.0
)

result = climate.simulate()
print(f"Temperature change: {result['temperature_change_c']}°C")
print(f"Sea level change: {result['sea_level_change_m']:.1f} m")
```

### Gamma-Ray Burst

Simulate nearby gamma-ray burst effects.

```python
class GammaRayBurst:
    def __init__(self, distance_ly: float)
    def simulate(self) -> Dict[str, Any]
```

#### Parameters

- `distance_ly` (float): Distance from Earth in light-years (10 - 50000)

#### Example

```python
from eles_core.event_types import GammaRayBurst

grb = GammaRayBurst(
    distance_ly=1000
)

result = grb.simulate()
print(f"Distance: {result['distance_ly']} light-years")
print(f"Radiation dose: {result['radiation_dose_sv']:.2e} Sv")
```

### AI Extinction

Simulate AI-related extinction risks.

```python
class AIExtinction:
    def __init__(self, ai_level: int)
    def simulate(self) -> Dict[str, Any]
```

#### Parameters

- `ai_level` (int): AI capability level (1 - 10)

#### Example

```python
from eles_core.event_types import AIExtinction

ai_risk = AIExtinction(
    ai_level=8
)

result = ai_risk.simulate()
print(f"AI level: {result['ai_level']}")
print(f"Control difficulty: {result['control_difficulty']}")
```

## 🛠️ Utility Functions

### Core Calculations

```python
from eles_core.utils import (
    calculate_crater_diameter,
    calculate_impact_energy,
    calculate_mass_from_diameter,
    tnt_equivalent,
    richter_magnitude,
    atmospheric_effects,
    population_at_risk,
    economic_damage_estimate
)
```

#### `calculate_crater_diameter(energy: float, target_density: float) -> float`

Calculate crater diameter from impact energy.

**Parameters:**

- `energy` (float): Impact energy in Joules
- `target_density` (float): Target material density in kg/m³

**Returns:**

- `float`: Crater diameter in kilometers

#### `calculate_impact_energy(mass: float, velocity: float) -> float`

Calculate kinetic energy of impact.

**Parameters:**

- `mass` (float): Object mass in kg
- `velocity` (float): Impact velocity in m/s

**Returns:**

- `float`: Kinetic energy in Joules

#### `calculate_mass_from_diameter(diameter: float, density: float) -> float`

Calculate mass from diameter and density (assuming spherical object).

**Parameters:**

- `diameter` (float): Diameter in kilometers
- `density` (float): Density in kg/m³

**Returns:**

- `float`: Mass in kilograms

#### `tnt_equivalent(energy: float) -> float`

Convert energy to TNT equivalent.

**Parameters:**

- `energy` (float): Energy in Joules

**Returns:**

- `float`: TNT equivalent in megatons

#### `population_at_risk(crater_diameter_km: float, destruction_radius_multiplier: float = 3.0) -> int`

Estimate population at risk from impact.

**Parameters:**

- `crater_diameter_km` (float): Crater diameter in kilometers
- `destruction_radius_multiplier` (float): Multiplier for destruction radius

**Returns:**

- `int`: Estimated population at risk

### Formatting Functions

#### `format_large_number(value: float) -> str`

Format large numbers with appropriate units.

**Example:**

```python
formatted = format_large_number(1234567890)
print(formatted)  # "1.23 billion"
```

#### `format_scientific_notation(value: float, precision: int = 2) -> str`

Format numbers in scientific notation.

**Example:**

```python
formatted = format_scientific_notation(1.23e15, precision=3)
print(formatted)  # "1.230e+15"
```

### Validation Functions

#### `validate_parameters(params: Dict[str, Any], required_keys: list) -> bool`

Validate that all required parameters are present.

**Parameters:**

- `params` (Dict[str, Any]): Parameter dictionary
- `required_keys` (list): List of required parameter names

**Returns:**

- `bool`: True if all required parameters are present

## 📊 Constants and Enumerations

### Supported Event Types

```python
from eles_core import SUPPORTED_EVENT_TYPES

print(SUPPORTED_EVENT_TYPES)
# ['asteroid', 'pandemic', 'supervolcano', 'climate_collapse', 'gamma_ray_burst', 'ai_extinction']
```

### Severity Levels

```python
from eles_core import SEVERITY_LEVELS

print(SEVERITY_LEVELS)
# {
#     1: "Minimal Impact",
#     2: "Local Disaster",
#     3: "Regional Catastrophe",
#     4: "Continental Crisis",
#     5: "Global Catastrophe",
#     6: "Extinction-Level Event"
# }
```

### Helper Functions

#### `get_supported_events() -> List[str]`

Get list of supported event types.

#### `get_severity_description(level: int) -> str`

Get human-readable description for severity level.

#### `get_version() -> str`

Get E.L.E.S. version string.

#### `create_engine(config_path: Optional[str] = None) -> Engine`

Convenience function to create a new simulation engine.

## 🔍 Error Handling

### Common Exceptions

```python
try:
    result = engine.run_simulation('unknown_event', {})
except ValueError as e:
    print(f"Invalid event type: {e}")

try:
    asteroid = AsteroidImpact(diameter_km=-1.0, density_kg_m3=3000, velocity_km_s=20)
except ValueError as e:
    print(f"Invalid parameter: {e}")
```

### Parameter Validation

All event types validate input parameters and raise `ValueError` for invalid inputs:

- **Asteroid**: Diameter must be positive, density 100-15000 kg/m³, velocity 5-100 km/s
- **Pandemic**: R₀ must be positive, mortality rate 0-1
- **Supervolcano**: VEI must be 0-8
- **Climate**: Temperature change must be reasonable (-50°C to +50°C)
- **GRB**: Distance must be positive
- **AI**: Level must be 1-10

## 💾 Data Export

### JSON Export

```python
# Export complete results
json_str = result.to_json()

# Save to file
with open('results.json', 'w') as f:
    f.write(json_str)

# Load from JSON
import json
data = json.loads(json_str)
```

### Summary Export

```python
# Get summary data
summary = result.summary()

# Export as CSV-friendly format
import csv
with open('summary.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=summary.keys())
    writer.writeheader()
    writer.writerow(summary)
```

## 🧪 Testing and Validation

### Running Tests

```python
# Test basic functionality
from eles_core import Engine

def test_basic_simulation():
    engine = Engine()
    result = engine.run_simulation('asteroid', {
        'diameter_km': 1.0,
        'density_kg_m3': 3000,
        'velocity_km_s': 20.0
    })
    assert result.severity >= 1
    assert result.severity <= 6
    print("✅ Basic simulation test passed")

test_basic_simulation()
```

### Parameter Range Testing

```python
def test_parameter_ranges():
    engine = Engine()

    # Test extreme values
    test_cases = [
        ('asteroid', {'diameter_km': 0.01, 'density_kg_m3': 1000, 'velocity_km_s': 10}),
        ('asteroid', {'diameter_km': 50.0, 'density_kg_m3': 15000, 'velocity_km_s': 80}),
        ('pandemic', {'r0': 0.1, 'mortality_rate': 0.001}),
        ('pandemic', {'r0': 10.0, 'mortality_rate': 0.5}),
    ]

    for event_type, params in test_cases:
        result = engine.run_simulation(event_type, params)
        assert result is not None
        print(f"✅ {event_type} with {params} -> Severity {result.severity}")

test_parameter_ranges()
```

## 📈 Performance Considerations

### Simulation Speed

- **Real-time**: All simulations complete in < 1 second
- **Memory usage**: Minimal memory footprint (~10-50 MB per simulation)
- **CPU usage**: Single-threaded calculations, optimized for accuracy over speed

### Batch Processing

```python
def run_batch_simulations(scenarios):
    engine = Engine()
    results = []

    for scenario in scenarios:
        result = engine.run_simulation(scenario['type'], scenario['params'])
        results.append(result)

    return results

# Example batch run
scenarios = [
    {'type': 'asteroid', 'params': {'diameter_km': 1.0, 'density_kg_m3': 3000, 'velocity_km_s': 20}},
    {'type': 'pandemic', 'params': {'r0': 3.0, 'mortality_rate': 0.02}},
    {'type': 'supervolcano', 'params': {'name': 'Yellowstone', 'vei': 7}},
]

batch_results = run_batch_simulations(scenarios)
```

## 🔧 Configuration

### Configuration File Format

E.L.E.S. uses YAML configuration files:

```yaml
# config/settings.yaml
app_name: "E.L.E.S."
version: "0.2.0"

simulation:
  max_iterations: 1000
  default_world_population: 8000000000

data:
  scenarios: "data/scenarios"
  assets: "data/assets"

visualization:
  default_style: "scientific"
  export_dpi: 300
```

### Custom Configuration

```python
# Create engine with custom config
engine = Engine("config/research_settings.yaml")

# Override specific settings
engine.settings['simulation']['max_iterations'] = 5000
```

## 🚀 Integration Examples

### Web Application Integration

```python
from flask import Flask, jsonify, request
from eles_core import create_engine

app = Flask(__name__)
engine = create_engine()

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.get_json()
    event_type = data.get('event_type')
    parameters = data.get('parameters')

    try:
        result = engine.run_simulation(event_type, parameters)
        return jsonify(result.summary())
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
```

### Data Analysis Integration

```python
import pandas as pd
import matplotlib.pyplot as plt
from eles_core import create_engine

def analyze_asteroid_sizes():
    engine = create_engine()
    diameters = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
    results = []

    for diameter in diameters:
        result = engine.run_simulation('asteroid', {
            'diameter_km': diameter,
            'density_kg_m3': 3000,
            'velocity_km_s': 20.0
        })
        results.append({
            'diameter': diameter,
            'severity': result.severity,
            'casualties': result.estimated_casualties,
            'economic_impact': result.economic_impact
        })

    df = pd.DataFrame(results)

    # Plot results
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.loglog(df['diameter'], df['casualties'], 'o-')
    ax1.set_xlabel('Diameter (km)')
    ax1.set_ylabel('Casualties')
    ax1.set_title('Casualties vs Asteroid Size')

    ax2.loglog(df['diameter'], df['economic_impact'], 's-')
    ax2.set_xlabel('Diameter (km)')
    ax2.set_ylabel('Economic Impact ($B)')
    ax2.set_title('Economic Impact vs Asteroid Size')

    plt.tight_layout()
    plt.show()

    return df

# Run analysis
results_df = analyze_asteroid_sizes()
```

## 📝 Version History

- **v0.1.0**: Initial release with basic simulation capabilities
- **v0.2.0**: Enhanced parameter validation, improved accuracy, added AI extinction scenarios

## 📄 License

E.L.E.S. is released under the MIT License. See [LICENSE](../LICENSE) for details.

## 🤝 Contributing

See the [Contributing Guide](CONTRIBUTING.md) for information on how to contribute to the E.L.E.S. API.

## 🆘 Support

- **Documentation**: Complete guides in the [docs/](.) folder
- **Issues**: Report bugs and request features on the project repository
- **FAQ**: See [FAQ.md](FAQ.md) for common questions
- **Troubleshooting**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for problem-solving

---

**Happy simulating!** 🌍💥
