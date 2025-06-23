# Advanced 3D Visualizations for E.L.E.S.

This document describes the advanced 3D visualization and simulation capabilities added to the E.L.E.S. (Extinction-Level Event Simulator) project.

## 🎯 Features

### Interactive 3D Visualizations
- **Asteroid Impact Craters**: Realistic 3D crater formation with terrain modeling
- **Explosion Spheres**: Multi-layered blast radius visualization with shock wave propagation  
- **Climate System Modeling**: 3D atmospheric and oceanic system visualization
- **Gamma-Ray Burst Patterns**: Radiation beam visualization and atmospheric effects
- **AI Development Risk**: Network-based visualization of AI capability growth
- **Geographic Impact Maps**: 3D global visualization of regional effects
- **Interactive Timelines**: Multi-dimensional event progression visualization
- **Multi-Scenario Comparisons**: Comparative risk assessment in 3D space

### Advanced Simulation Systems
- **Particle Systems**: Real-time debris and ejecta simulation
- **Volumetric Rendering**: Atmospheric effects and gas cloud modeling
- **Physics-Based Simulation**: Realistic impact dynamics and propagation
- **Fluid Dynamics**: Tsunami and atmospheric flow simulation
- **VR/AR Ready**: Immersive visualization support

## 🚀 Getting Started

### Prerequisites

Install the required 3D visualization libraries:

```bash
pip install pyvista>=0.43.0
pip install open3d>=0.18.0  
pip install trimesh>=4.0.0
pip install vtk>=9.3.0
pip install mayavi>=4.8.1
```

Note: Some libraries (mayavi, vtk) may require additional system dependencies.

### Basic Usage

#### In Streamlit App

1. Run the main Streamlit application:
   ```bash
   streamlit run ui/streamlit_app.py
   ```

2. Select an extinction event type and configure parameters

3. In the "Visualizations" tab, choose:
   - **2D Charts**: Traditional plots and graphs
   - **3D Interactive**: Interactive 3D visualizations  
   - **Advanced 3D Simulation**: Physics-based simulations

#### Demo Scripts

Run individual 3D demos:

```bash
# Simple demo (minimal dependencies)
python visualizations/demo_3d_simple.py

# Complete demo suite  
python demo_3d_complete.py

# Specific demo types
python demo_3d_complete.py asteroid
python demo_3d_complete.py climate
python demo_3d_complete.py particles
```

## 📊 Visualization Types

### 1. Asteroid Impact (render_asteroid_impact)

Creates realistic 3D crater visualization with:
- Parabolic crater profile based on impact energy
- Asteroid trajectory visualization
- Ejecta pattern and debris distribution
- Surrounding terrain modeling

**Parameters:**
- `crater_diameter_km`: Resulting crater size
- `impact_angle`: Asteroid approach angle
- `asteroid_diameter_km`: Impactor size
- `impact_velocity_km_s`: Impact speed
- `impact_energy_joules`: Total kinetic energy

### 2. Explosion Propagation (render_explosion_sphere)

Multi-layered explosion visualization showing:
- Expanding shock wave spheres
- Thermal radiation zones
- Overpressure effects
- Time-based propagation animation

**Parameters:**
- `max_blast_radius_km`: Maximum effective radius
- `explosion_energy_joules`: Total explosive energy
- `time_steps`: Animation frame count
- `shock_wave_velocity_km_s`: Propagation speed

### 3. Climate Collapse (render_climate_collapse_3d)

Global climate system visualization featuring:
- Temperature distribution maps
- Sea level change modeling
- Precipitation pattern changes
- Ice coverage variations
- Vegetation loss patterns

**Parameters:**
- `temperature_change_c`: Global temperature change
- `sea_level_change_m`: Sea level rise/fall
- `precipitation_change_percent`: Rainfall changes
- `duration_years`: Effect duration

### 4. Gamma-Ray Burst (render_gamma_ray_burst_3d)

High-energy radiation visualization showing:
- Directed energy beam patterns
- Atmospheric interaction effects
- Ozone layer depletion
- Earth exposure geometry

**Parameters:**
- `energy_joules`: Burst energy output
- `distance_light_years`: Source distance
- `ozone_depletion_percent`: Atmospheric damage
- `radiation_duration_seconds`: Burst duration

### 5. AI Extinction Risk (render_ai_extinction_3d)

Network-based risk modeling featuring:
- AI capability growth trajectories
- Risk propagation networks
- Control probability surfaces
- Timeline visualization

**Parameters:**
- `development_speed`: AI advancement rate
- `control_probability`: Human control likelihood
- `capability_growth_rate`: Exponential growth factor
- `timeline_years`: Development timeframe

## 🎮 Advanced Simulations

### Particle Systems

Real-time physics simulation with:
- Debris trajectory calculation
- Gravitational effects
- Atmospheric drag modeling
- Collision detection

### Volumetric Rendering

3D atmospheric effects including:
- Ash cloud propagation
- Gas dispersal patterns
- Thermal gradients
- Opacity modeling

### Simulation Parameters

Configure simulation quality and features:

```python
params = SimulationParameters(
    resolution=100,        # Spatial resolution (50-200)
    time_steps=60,        # Temporal resolution (10-120)
    frame_rate=30.0,      # Animation speed (10-60 fps)
    quality="high",       # "low", "medium", "high", "ultra"
    enable_physics=True,  # Physics simulation
    enable_particles=True, # Particle systems
    enable_volumetrics=True # Volumetric effects
)
```

## 🔧 Technical Architecture

### Module Structure

```
visualizations/3d/
├── __init__.py              # Package initialization
├── model.py                 # Core 3D visualization functions
├── advanced_simulations.py  # Physics-based simulation classes
├── demo_advanced.py         # Complex demonstration script
└── README.md               # This documentation
```

### Key Classes

- **Advanced3DSimulator**: Base class for physics simulations
- **AsteroidImpact3DSimulator**: Specialized asteroid impact simulation
- **VolcanicEruption3DSimulator**: Volcanic eruption modeling
- **Pandemic3DSimulator**: Disease spread simulation
- **SimulationParameters**: Configuration container
- **Camera3D**: 3D camera positioning

### Integration Points

The 3D visualizations integrate with:
- Streamlit UI (`ui/streamlit_app.py`)
- Core simulation engine (`eles_core/engine.py`)
- Event type modules (`eles_core/event_types/`)
- Configuration system (`config/`)

## 🎨 Customization

### Styling and Themes

Modify visualization appearance:

```python
fig.update_layout(
    scene=dict(
        bgcolor='black',           # Background color
        camera=dict(
            eye=dict(x=1.5, y=1.5, z=1.2),  # Camera position
            center=dict(x=0, y=0, z=0)       # Look-at point
        ),
        aspectmode='cube'          # Aspect ratio
    ),
    colorscale='Viridis',         # Color scheme
    title_font_size=20            # Title styling
)
```

### Color Schemes

Available color schemes:
- `'Earth'`: Natural earth tones
- `'Viridis'`: Scientific visualization
- `'Plasma'`: High-energy events
- `'Inferno'`: Thermal effects
- `'Magma'`: Volcanic events

### Camera Controls

Interactive camera positioning:
- **Orbit**: Click and drag to rotate
- **Pan**: Shift + click and drag
- **Zoom**: Mouse wheel or pinch gesture
- **Reset**: Double-click to reset view

## 📈 Performance Optimization

### Quality Settings

Optimize performance vs. quality:

- **Low**: Basic geometry, minimal particles
- **Medium**: Standard detail, moderate particles  
- **High**: Detailed geometry, full particle systems
- **Ultra**: Maximum detail, advanced effects

### Hardware Requirements

Recommended specifications:
- **Minimum**: 4GB RAM, integrated graphics
- **Recommended**: 8GB RAM, dedicated GPU
- **Optimal**: 16GB RAM, modern GPU with 4GB+ VRAM

### Browser Compatibility

Tested browsers:
- Chrome 90+ (recommended)
- Firefox 88+
- Safari 14+
- Edge 90+

## 🐛 Troubleshooting

### Common Issues

**ImportError: No module named 'pyvista'**
```bash
pip install pyvista open3d trimesh vtk
```

**WebGL errors in browser**
- Update graphics drivers
- Enable hardware acceleration in browser
- Try different browser

**Performance issues**
- Reduce resolution parameter
- Disable particles/volumetrics
- Lower quality setting

**Memory errors**
- Reduce time_steps
- Lower resolution
- Close other applications

### Debug Mode

Enable debug output:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

### Adding New Visualizations

1. Create visualization function in `model.py`:
   ```python
   def render_new_event_3d(event_data: Dict[str, Any]) -> go.Figure:
       # Implementation
       pass
   ```

2. Add to `__init__.py` exports
3. Integrate with Streamlit UI
4. Add demo function
5. Update documentation

### Simulation Classes

1. Inherit from `Advanced3DSimulator`
2. Implement required methods:
   - `initialize_simulation()`
   - `step_simulation()`
   - `render_frame()`
3. Add to advanced_simulations.py
4. Test with demo script

## 📚 Examples

See the `demo_3d_complete.py` script for comprehensive examples of all visualization types and simulation capabilities.

## 📝 License

Same as main E.L.E.S. project license.

## 🆘 Support

For issues or questions:
1. Check troubleshooting section
2. Review demo scripts for examples
3. Check GitHub issues
4. Contact project maintainers
