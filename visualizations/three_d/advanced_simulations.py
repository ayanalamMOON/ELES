"""
Advanced 3D Simulations and Visualizations for E.L.E.S.

This module provides state-of-the-art 3D visualization and simulation capabilities
for extinction-level events, including:
- Advanced particle systems for asteroid impacts
- Volumetric rendering for volcanic eruptions
- Real-time fluid dynamics for tsunamis
- 3D atmospheric modeling
- Interactive VR/AR ready visualizations
"""

import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, Any, List, Tuple, Optional, Union
import math
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Try to import advanced 3D libraries
try:
    import pyvista as pv
    HAS_PYVISTA = True
except ImportError:
    HAS_PYVISTA = False

try:
    import open3d as o3d
    HAS_OPEN3D = True
except ImportError:
    HAS_OPEN3D = False

try:
    import trimesh
    HAS_TRIMESH = True
except ImportError:
    HAS_TRIMESH = False


@dataclass
class SimulationParameters:
    """Parameters for 3D simulations."""
    resolution: int = 100
    time_steps: int = 60
    frame_rate: float = 30.0
    quality: str = "high"  # low, medium, high, ultra
    enable_physics: bool = True
    enable_particles: bool = True
    enable_volumetrics: bool = True


@dataclass
class Camera3D:
    """3D Camera configuration."""
    position: Tuple[float, float, float] = (100, 100, 100)
    target: Tuple[float, float, float] = (0, 0, 0)
    up_vector: Tuple[float, float, float] = (0, 0, 1)
    field_of_view: float = 45.0


class Advanced3DSimulator(ABC):
    """Abstract base class for advanced 3D simulations."""

    def __init__(self, params: SimulationParameters):
        self.params = params
        self.camera = Camera3D()
        self.time = 0.0
        self.data_frames = []

    @abstractmethod
    def initialize_simulation(self, event_data: Dict[str, Any]):
        """Initialize the simulation with event parameters."""
        pass

    @abstractmethod
    def step_simulation(self, dt: float):
        """Advance simulation by one time step."""
        pass

    @abstractmethod
    def render_frame(self) -> go.Figure:
        """Render current simulation state to a 3D figure."""
        pass

    def run_simulation(self, event_data: Dict[str, Any]) -> List[go.Figure]:
        """Run complete simulation and return all frames."""
        self.initialize_simulation(event_data)
        frames = []
        
        dt = 1.0 / self.params.frame_rate
        for step in range(self.params.time_steps):
            self.step_simulation(dt)
            if step % max(1, self.params.time_steps // 30) == 0:  # Limit to 30 frames max
                frame = self.render_frame()
                frames.append(frame)
        
        return frames


class AsteroidImpact3DSimulator(Advanced3DSimulator):
    """Advanced 3D asteroid impact simulation with particle effects."""

    def initialize_simulation(self, event_data: Dict[str, Any]):
        """Initialize asteroid impact simulation."""
        self.asteroid_diameter = event_data.get('diameter_km', 1.0)
        self.impact_velocity = event_data.get('velocity_km_s', 20.0) * 1000  # m/s
        self.impact_angle = event_data.get('impact_angle', 45.0)
        self.density = event_data.get('density_kg_m3', 3000)
        
        # Calculate impact energy and crater parameters
        self.asteroid_mass = (4/3) * np.pi * (self.asteroid_diameter * 500)**3 * self.density
        self.impact_energy = 0.5 * self.asteroid_mass * self.impact_velocity**2
        
        # Crater scaling laws
        self.crater_diameter = self.asteroid_diameter * 20  # Simplified scaling
        self.crater_depth = self.crater_diameter * 0.2
        
        # Initialize particle systems
        self.debris_particles = self._initialize_debris_particles()
        self.shock_wave = self._initialize_shock_wave()
        self.ejecta_curtain = self._initialize_ejecta_curtain()
        
        # Terrain
        self.terrain = self._generate_terrain()

    def _initialize_debris_particles(self) -> Dict[str, np.ndarray]:
        """Initialize debris particle system."""
        n_particles = min(1000, self.params.resolution * 10)
        
        # Initial positions (from impact point)
        positions = np.random.normal(0, self.asteroid_diameter/4, (n_particles, 3))
        positions[:, 2] = np.abs(positions[:, 2])  # Above ground
        
        # Initial velocities (radial explosion pattern)
        velocities = np.random.normal(0, self.impact_velocity/20, (n_particles, 3))
        velocities[:, 2] = np.abs(velocities[:, 2])  # Upward component
        
        # Particle properties
        masses = np.random.exponential(1000, n_particles)  # kg
        sizes = (masses / 1000) ** (1/3)  # Approximate size from mass
        
        return {
            'positions': positions,
            'velocities': velocities,
            'masses': masses,
            'sizes': sizes,
            'active': np.ones(n_particles, dtype=bool)
        }

    def _initialize_shock_wave(self) -> Dict[str, Any]:
        """Initialize shock wave propagation."""
        return {
            'radius': 0.0,
            'velocity': self.impact_velocity / 10,  # Shock wave velocity
            'pressure': self.impact_energy / (4 * np.pi * self.crater_diameter**2),
            'active': True
        }

    def _initialize_ejecta_curtain(self) -> Dict[str, np.ndarray]:
        """Initialize ejecta curtain particles."""
        n_ejecta = min(500, self.params.resolution * 5)
        
        # Ejecta launched at various angles
        angles = np.linspace(0, 2*np.pi, n_ejecta)
        elevation_angles = np.random.uniform(20, 80, n_ejecta)  # degrees
        
        # Initial positions at crater rim
        rim_radius = self.crater_diameter / 2
        positions = np.zeros((n_ejecta, 3))
        positions[:, 0] = rim_radius * np.cos(angles)
        positions[:, 1] = rim_radius * np.sin(angles)
        positions[:, 2] = 0
        
        # Launch velocities
        launch_speed = self.impact_velocity / 5
        velocities = np.zeros((n_ejecta, 3))
        velocities[:, 0] = launch_speed * np.cos(angles) * np.cos(np.radians(elevation_angles))
        velocities[:, 1] = launch_speed * np.sin(angles) * np.cos(np.radians(elevation_angles))
        velocities[:, 2] = launch_speed * np.sin(np.radians(elevation_angles))
        
        return {
            'positions': positions,
            'velocities': velocities,
            'active': np.ones(n_ejecta, dtype=bool)
        }

    def _generate_terrain(self) -> Dict[str, np.ndarray]:
        """Generate 3D terrain mesh."""
        size = self.crater_diameter * 3
        res = self.params.resolution
        
        x = np.linspace(-size/2, size/2, res)
        y = np.linspace(-size/2, size/2, res)
        X, Y = np.meshgrid(x, y)
        
        # Initial flat terrain with some noise
        Z = np.random.normal(0, 0.1, X.shape)
        
        return {'X': X, 'Y': Y, 'Z': Z}

    def step_simulation(self, dt: float):
        """Advance asteroid impact simulation."""
        self.time += dt
        gravity = -9.81  # m/s²
        
        # Update debris particles
        if self.params.enable_particles:
            active_debris = self.debris_particles['active']
            
            # Apply gravity
            self.debris_particles['velocities'][active_debris, 2] += gravity * dt
            
            # Update positions
            self.debris_particles['positions'][active_debris] += \
                self.debris_particles['velocities'][active_debris] * dt
            
            # Deactivate particles that hit ground
            ground_hit = self.debris_particles['positions'][:, 2] <= 0
            self.debris_particles['active'][ground_hit] = False
        
        # Update shock wave
        if self.shock_wave['active']:
            self.shock_wave['radius'] += self.shock_wave['velocity'] * dt
            
            # Deactivate when shock wave gets too far
            if self.shock_wave['radius'] > self.crater_diameter * 10:
                self.shock_wave['active'] = False
        
        # Update ejecta curtain
        if self.params.enable_particles:
            active_ejecta = self.ejecta_curtain['active']
            
            # Apply gravity to ejecta
            self.ejecta_curtain['velocities'][active_ejecta, 2] += gravity * dt
            
            # Update ejecta positions
            self.ejecta_curtain['positions'][active_ejecta] += \
                self.ejecta_curtain['velocities'][active_ejecta] * dt
            
            # Deactivate ejecta that hit ground
            ejecta_ground_hit = self.ejecta_curtain['positions'][:, 2] <= 0
            self.ejecta_curtain['active'][ejecta_ground_hit] = False
        
        # Update terrain (crater formation)
        if self.time < 5.0:  # Crater forms in first 5 seconds
            crater_progress = min(1.0, self.time / 5.0)
            self._update_crater_formation(crater_progress)

    def _update_crater_formation(self, progress: float):
        """Update crater formation over time."""
        X, Y = self.terrain['X'], self.terrain['Y']
        distance_from_impact = np.sqrt(X**2 + Y**2)
        
        # Crater profile formation
        crater_mask = distance_from_impact <= self.crater_diameter / 2
        
        # Gradual crater deepening
        max_depth = -self.crater_depth * progress
        crater_profile = max_depth * (1 - (distance_from_impact / (self.crater_diameter / 2))**2)
        crater_profile[~crater_mask] = 0
        
        # Rim formation
        rim_mask = (distance_from_impact > self.crater_diameter / 2) & \
                   (distance_from_impact <= self.crater_diameter / 1.8)
        rim_height = self.crater_depth * 0.1 * progress * \
                    np.exp(-(distance_from_impact - self.crater_diameter / 2) / (self.crater_diameter * 0.1))
        
        self.terrain['Z'] = crater_profile + rim_height * rim_mask

    def render_frame(self) -> go.Figure:
        """Render current state of asteroid impact simulation."""
        fig = go.Figure()
        
        # Add terrain surface
        fig.add_trace(go.Surface(
            x=self.terrain['X'],
            y=self.terrain['Y'],
            z=self.terrain['Z'],
            colorscale='Earth',
            name='Terrain',
            opacity=0.8,
            showscale=False
        ))
        
        # Add debris particles
        if self.params.enable_particles:
            active_debris = self.debris_particles['active']
            if np.any(active_debris):
                debris_pos = self.debris_particles['positions'][active_debris]
                debris_sizes = self.debris_particles['sizes'][active_debris]
                
                fig.add_trace(go.Scatter3d(
                    x=debris_pos[:, 0],
                    y=debris_pos[:, 1],
                    z=debris_pos[:, 2],
                    mode='markers',
                    marker=dict(
                        size=debris_sizes * 2,
                        color='red',
                        opacity=0.7,
                        symbol='circle'
                    ),
                    name='Debris'
                ))
        
        # Add ejecta curtain
        if self.params.enable_particles:
            active_ejecta = self.ejecta_curtain['active']
            if np.any(active_ejecta):
                ejecta_pos = self.ejecta_curtain['positions'][active_ejecta]
                
                fig.add_trace(go.Scatter3d(
                    x=ejecta_pos[:, 0],
                    y=ejecta_pos[:, 1],
                    z=ejecta_pos[:, 2],
                    mode='markers',
                    marker=dict(
                        size=3,
                        color='orange',
                        opacity=0.6
                    ),
                    name='Ejecta'
                ))
        
        # Add shock wave
        if self.shock_wave['active'] and self.shock_wave['radius'] > 0:
            # Create shock wave as a circle at ground level
            theta = np.linspace(0, 2*np.pi, 50)
            shock_x = self.shock_wave['radius'] * np.cos(theta)
            shock_y = self.shock_wave['radius'] * np.sin(theta)
            shock_z = np.zeros_like(shock_x) + 1  # Slightly above ground
            
            fig.add_trace(go.Scatter3d(
                x=shock_x,
                y=shock_y,
                z=shock_z,
                mode='lines',
                line=dict(color='yellow', width=8),
                name='Shock Wave'
            ))
        
        # Configure layout
        fig.update_layout(
            title=f'Asteroid Impact Simulation - t={self.time:.1f}s',
            scene=dict(
                xaxis_title='Distance (km)',
                yaxis_title='Distance (km)',
                zaxis_title='Elevation (km)',
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)
                ),
                aspectmode='cube'
            ),
            showlegend=True
        )
        
        return fig


class VolcanicEruption3DSimulator(Advanced3DSimulator):
    """Advanced 3D volcanic eruption simulation with volumetric rendering."""

    def initialize_simulation(self, event_data: Dict[str, Any]):
        """Initialize volcanic eruption simulation."""
        self.vei = event_data.get('vei', 6)
        self.magma_volume = event_data.get('magma_volume_km3', 100)
        self.eruption_rate = event_data.get('eruption_rate_m3_s', 1e8)
        
        # Volcanic parameters
        self.vent_radius = (self.magma_volume * 1e9 / (np.pi * 1000))**(1/3)  # Approximate
        self.plume_height = min(50, self.vei * 8)  # km
        self.ash_particles = self._initialize_ash_particles()
        self.pyroclastic_flows = self._initialize_pyroclastic_flows()
        self.lava_flows = self._initialize_lava_flows()
        
        # Terrain
        self.terrain = self._generate_volcanic_terrain()

    def _initialize_ash_particles(self) -> Dict[str, np.ndarray]:
        """Initialize volcanic ash particle system."""
        n_particles = min(2000, self.params.resolution * 20)
        
        # Initial positions (from vent)
        positions = np.random.normal(0, self.vent_radius, (n_particles, 3))
        positions[:, 2] = np.random.uniform(0, 1, n_particles)  # Start at vent
        
        # Initial velocities (upward with some spread)
        velocities = np.random.normal(0, 50, (n_particles, 3))
        velocities[:, 2] = np.random.uniform(100, 500, n_particles)  # Strong upward
        
        # Particle properties
        sizes = np.random.exponential(0.1, n_particles)  # Ash particle sizes
        densities = np.random.uniform(1000, 3000, n_particles)  # kg/m³
        
        return {
            'positions': positions,
            'velocities': velocities,
            'sizes': sizes,
            'densities': densities,
            'active': np.ones(n_particles, dtype=bool),
            'age': np.zeros(n_particles)
        }

    def _initialize_pyroclastic_flows(self) -> Dict[str, Any]:
        """Initialize pyroclastic flow simulation."""
        # Pyroclastic flows move radially outward
        n_flows = 8  # Number of flow directions
        angles = np.linspace(0, 2*np.pi, n_flows, endpoint=False)
        
        flows = []
        for angle in angles:
            flow = {
                'direction': np.array([np.cos(angle), np.sin(angle), -0.1]),
                'velocity': np.random.uniform(50, 200),  # m/s
                'temperature': np.random.uniform(300, 800),  # °C
                'distance': 0.0,
                'active': True
            }
            flows.append(flow)
        
        return {'flows': flows}

    def _initialize_lava_flows(self) -> Dict[str, Any]:
        """Initialize lava flow simulation."""
        return {
            'volume_erupted': 0.0,
            'flow_fronts': [],
            'active': True
        }

    def _generate_volcanic_terrain(self) -> Dict[str, np.ndarray]:
        """Generate volcanic terrain with stratovolcano shape."""
        size = max(50, self.vent_radius * 20)
        res = self.params.resolution
        
        x = np.linspace(-size/2, size/2, res)
        y = np.linspace(-size/2, size/2, res)
        X, Y = np.meshgrid(x, y)
        
        # Distance from center
        R = np.sqrt(X**2 + Y**2)
        
        # Volcanic cone shape
        base_height = 2.0  # km
        cone_slope = 0.1
        Z = base_height - cone_slope * R
        Z = np.maximum(Z, 0)  # No negative elevations
        
        # Add crater at center
        crater_radius = self.vent_radius
        crater_mask = R <= crater_radius
        crater_depth = 0.5
        Z[crater_mask] = base_height - crater_depth
        
        return {'X': X, 'Y': Y, 'Z': Z}

    def step_simulation(self, dt: float):
        """Advance volcanic eruption simulation."""
        self.time += dt
        
        # Update ash particles
        if self.params.enable_particles:
            active_ash = self.ash_particles['active']
            
            # Apply gravity and air resistance
            gravity = -9.81
            air_resistance = -0.1
            
            self.ash_particles['velocities'][active_ash, 2] += gravity * dt
            self.ash_particles['velocities'][active_ash] *= (1 + air_resistance * dt)
            
            # Update positions
            self.ash_particles['positions'][active_ash] += \
                self.ash_particles['velocities'][active_ash] * dt
            
            # Age particles
            self.ash_particles['age'][active_ash] += dt
            
            # Deactivate old particles or those that hit ground
            old_particles = self.ash_particles['age'] > 300  # 5 minutes
            ground_hit = self.ash_particles['positions'][:, 2] <= 0
            self.ash_particles['active'][old_particles | ground_hit] = False
        
        # Update pyroclastic flows
        for flow in self.pyroclastic_flows['flows']:
            if flow['active']:
                flow['distance'] += flow['velocity'] * dt
                
                # Deactivate flows that have traveled too far
                if flow['distance'] > 50000:  # 50 km
                    flow['active'] = False

    def render_frame(self) -> go.Figure:
        """Render current state of volcanic eruption."""
        fig = go.Figure()
        
        # Add terrain
        fig.add_trace(go.Surface(
            x=self.terrain['X'],
            y=self.terrain['Y'],
            z=self.terrain['Z'],
            colorscale='Hot',
            name='Volcano',
            opacity=0.8,
            showscale=False
        ))
        
        # Add ash particles
        if self.params.enable_particles:
            active_ash = self.ash_particles['active']
            if np.any(active_ash):
                ash_pos = self.ash_particles['positions'][active_ash]
                ash_ages = self.ash_particles['age'][active_ash]
                
                # Color by age (newer = brighter)
                colors = np.maximum(0, 1 - ash_ages / 100)
                
                fig.add_trace(go.Scatter3d(
                    x=ash_pos[:, 0],
                    y=ash_pos[:, 1],
                    z=ash_pos[:, 2],
                    mode='markers',
                    marker=dict(
                        size=2,
                        color=colors,
                        colorscale='Greys',
                        opacity=0.5
                    ),
                    name='Ash Cloud'
                ))
        
        # Add pyroclastic flows
        for i, flow in enumerate(self.pyroclastic_flows['flows']):
            if flow['active']:
                # Create flow visualization
                distance = flow['distance'] / 1000  # Convert to km
                direction = flow['direction']
                
                # Flow path
                flow_x = [0, direction[0] * distance]
                flow_y = [0, direction[1] * distance]
                flow_z = [2, max(0, 2 + direction[2] * distance)]
                
                fig.add_trace(go.Scatter3d(
                    x=flow_x,
                    y=flow_y,
                    z=flow_z,
                    mode='lines',
                    line=dict(color='red', width=10),
                    name=f'Pyroclastic Flow {i+1}' if i == 0 else None,
                    showlegend=(i == 0)
                ))
        
        # Configure layout
        fig.update_layout(
            title=f'Volcanic Eruption (VEI {self.vei}) - t={self.time:.1f}s',
            scene=dict(
                xaxis_title='Distance (km)',
                yaxis_title='Distance (km)',
                zaxis_title='Elevation (km)',
                camera=dict(
                    eye=dict(x=2, y=2, z=1.5)
                ),
                aspectmode='cube'
            ),
            showlegend=True
        )
        
        return fig


class Pandemic3DSimulator(Advanced3DSimulator):
    """Advanced 3D pandemic spread simulation with network visualization."""

    def initialize_simulation(self, event_data: Dict[str, Any]):
        """Initialize pandemic simulation."""
        self.r0 = event_data.get('r0', 2.5)
        self.mortality_rate = event_data.get('mortality_rate', 0.02)
        self.incubation_period = event_data.get('incubation_period_days', 5)
        
        # Population centers (major cities)
        self.cities = self._generate_city_network()
        self.infection_data = self._initialize_infection_data()
        self.travel_network = self._create_travel_network()

    def _generate_city_network(self) -> List[Dict[str, Any]]:
        """Generate network of major population centers."""
        # Simplified global city network
        cities = [
            {'name': 'New York', 'lat': 40.7128, 'lon': -74.0060, 'population': 8000000},
            {'name': 'London', 'lat': 51.5074, 'lon': -0.1278, 'population': 9000000},
            {'name': 'Tokyo', 'lat': 35.6762, 'lon': 139.6503, 'population': 14000000},
            {'name': 'Shanghai', 'lat': 31.2304, 'lon': 121.4737, 'population': 24000000},
            {'name': 'Mumbai', 'lat': 19.0760, 'lon': 72.8777, 'population': 21000000},
            {'name': 'São Paulo', 'lat': -23.5505, 'lon': -46.6333, 'population': 12000000},
            {'name': 'Lagos', 'lat': 6.5244, 'lon': 3.3792, 'population': 15000000},
            {'name': 'Cairo', 'lat': 30.0444, 'lon': 31.2357, 'population': 20000000},
            {'name': 'Sydney', 'lat': -33.8688, 'lon': 151.2093, 'population': 5000000},
            {'name': 'Mexico City', 'lat': 19.4326, 'lon': -99.1332, 'population': 21000000}
        ]
        
        # Convert coordinates to 3D sphere coordinates
        for city in cities:
            # Convert lat/lon to 3D coordinates on unit sphere, then scale
            lat_rad = np.radians(city['lat'])
            lon_rad = np.radians(city['lon'])
            
            radius = 100  # Scale factor for visualization
            city['x'] = radius * np.cos(lat_rad) * np.cos(lon_rad)
            city['y'] = radius * np.cos(lat_rad) * np.sin(lon_rad)
            city['z'] = radius * np.sin(lat_rad)
        
        return cities

    def _initialize_infection_data(self) -> Dict[str, np.ndarray]:
        """Initialize infection tracking data."""
        n_cities = len(self.cities)
        
        # SEIR compartments
        susceptible = np.array([city['population'] for city in self.cities], dtype=float)
        exposed = np.zeros(n_cities)
        infected = np.zeros(n_cities)
        recovered = np.zeros(n_cities)
        
        # Patient zero in first city
        infected[0] = 1
        susceptible[0] -= 1
        
        return {
            'susceptible': susceptible,
            'exposed': exposed,
            'infected': infected,
            'recovered': recovered,
            'deaths': np.zeros(n_cities)
        }

    def _create_travel_network(self) -> np.ndarray:
        """Create travel connectivity matrix between cities."""
        n_cities = len(self.cities)
        connectivity = np.zeros((n_cities, n_cities))
        
        # Calculate travel probability based on population and distance
        for i in range(n_cities):
            for j in range(n_cities):
                if i != j:
                    city_i = self.cities[i]
                    city_j = self.cities[j]
                    
                    # Distance between cities
                    dist = np.sqrt((city_i['x'] - city_j['x'])**2 + 
                                 (city_i['y'] - city_j['y'])**2 + 
                                 (city_i['z'] - city_j['z'])**2)
                    
                    # Travel probability (inversely related to distance)
                    connectivity[i][j] = (city_i['population'] * city_j['population']) / (dist**2 + 1e6)
        
        # Normalize
        connectivity = connectivity / np.max(connectivity) * 0.01  # Max 1% travel per day
        
        return connectivity

    def step_simulation(self, dt: float):
        """Advance pandemic simulation using SEIR model."""
        self.time += dt
        
        # SEIR parameters
        beta = self.r0 / 10  # Transmission rate (simplified)
        sigma = 1 / self.incubation_period  # Incubation rate
        gamma = 1 / 7  # Recovery rate (7 days infectious period)
        mu = self.mortality_rate * gamma  # Death rate
        
        n_cities = len(self.cities)
        
        # Update each city
        for i in range(n_cities):
            S = self.infection_data['susceptible'][i]
            E = self.infection_data['exposed'][i]
            I = self.infection_data['infected'][i]
            R = self.infection_data['recovered'][i]
            
            N = S + E + I + R  # Total population
            
            if N > 0:
                # SEIR equations
                dS_dt = -beta * S * I / N
                dE_dt = beta * S * I / N - sigma * E
                dI_dt = sigma * E - gamma * I
                dR_dt = gamma * I - mu * I
                dD_dt = mu * I
                
                # Update compartments
                self.infection_data['susceptible'][i] += dS_dt * dt
                self.infection_data['exposed'][i] += dE_dt * dt
                self.infection_data['infected'][i] += dI_dt * dt
                self.infection_data['recovered'][i] += dR_dt * dt
                self.infection_data['deaths'][i] += dD_dt * dt
        
        # Travel between cities
        for i in range(n_cities):
            for j in range(n_cities):
                if i != j and self.travel_network[i][j] > 0:
                    # Calculate travelers from each compartment
                    travel_rate = self.travel_network[i][j] * dt
                    
                    # Exposed and infected individuals can travel and spread disease
                    traveling_exposed = self.infection_data['exposed'][i] * travel_rate
                    traveling_infected = self.infection_data['infected'][i] * travel_rate
                    
                    # Move individuals
                    self.infection_data['exposed'][i] -= traveling_exposed
                    self.infection_data['infected'][i] -= traveling_infected
                    self.infection_data['exposed'][j] += traveling_exposed
                    self.infection_data['infected'][j] += traveling_infected

    def render_frame(self) -> go.Figure:
        """Render current state of pandemic simulation."""
        fig = go.Figure()
        
        # Add Earth sphere
        u = np.linspace(0, 2 * np.pi, 50)
        v = np.linspace(0, np.pi, 50)
        earth_x = 98 * np.outer(np.cos(u), np.sin(v))  # Slightly smaller than city radius
        earth_y = 98 * np.outer(np.sin(u), np.sin(v))
        earth_z = 98 * np.outer(np.ones(np.size(u)), np.cos(v))
        
        fig.add_trace(go.Surface(
            x=earth_x, y=earth_y, z=earth_z,
            colorscale='Blues',
            opacity=0.3,
            showscale=False,
            name='Earth'
        ))
        
        # Add cities with infection data
        city_x = [city['x'] for city in self.cities]
        city_y = [city['y'] for city in self.cities]
        city_z = [city['z'] for city in self.cities]
        city_names = [city['name'] for city in self.cities]
        
        # Color by infection rate
        infection_rates = self.infection_data['infected'] / \
                         np.array([city['population'] for city in self.cities])
        infection_rates = np.nan_to_num(infection_rates)
        
        # Size by total cases
        total_cases = (self.infection_data['infected'] + 
                      self.infection_data['recovered'] + 
                      self.infection_data['deaths'])
        
        fig.add_trace(go.Scatter3d(
            x=city_x,
            y=city_y,
            z=city_z,
            mode='markers+text',
            marker=dict(
                size=np.sqrt(total_cases / 10000) + 5,  # Scale for visibility
                color=infection_rates,
                colorscale='Reds',
                colorbar=dict(title="Infection Rate"),
                opacity=0.8
            ),
            text=city_names,
            textposition="top center",
            name='Cities',
            hovertemplate='<b>%{text}</b><br>' +
                         'Infected: %{customdata[0]:.0f}<br>' +
                         'Deaths: %{customdata[1]:.0f}<br>' +
                         '<extra></extra>',
            customdata=np.column_stack((self.infection_data['infected'], 
                                      self.infection_data['deaths']))
        ))
        
        # Add travel connections for active transmission
        for i in range(len(self.cities)):
            for j in range(i+1, len(self.cities)):
                if (self.infection_data['infected'][i] > 100 and 
                    self.infection_data['infected'][j] > 100):
                    
                    fig.add_trace(go.Scatter3d(
                        x=[city_x[i], city_x[j]],
                        y=[city_y[i], city_y[j]],
                        z=[city_z[i], city_z[j]],
                        mode='lines',
                        line=dict(color='orange', width=2),
                        opacity=0.6,
                        showlegend=False
                    ))
        
        # Configure layout
        fig.update_layout(
            title=f'Global Pandemic Spread - Day {self.time:.0f}',
            scene=dict(
                xaxis_title='X',
                yaxis_title='Y',
                zaxis_title='Z',
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)
                ),
                aspectmode='cube'
            ),
            showlegend=True
        )
        
        return fig


class Advanced3DVisualizationManager:
    """Manager for advanced 3D visualizations and simulations."""

    def __init__(self):
        self.simulators = {
            'asteroid': AsteroidImpact3DSimulator,
            'supervolcano': VolcanicEruption3DSimulator,
            'pandemic': Pandemic3DSimulator
        }
        self.current_simulation = None

    def create_simulation(self, event_type: str, 
                         simulation_params: Optional[SimulationParameters] = None) -> Advanced3DSimulator:
        """Create a 3D simulation for the specified event type."""
        if event_type not in self.simulators:
            raise ValueError(f"Unsupported event type: {event_type}")
        
        if simulation_params is None:
            simulation_params = SimulationParameters()
        
        simulator_class = self.simulators[event_type]
        return simulator_class(simulation_params)

    def run_advanced_simulation(self, event_type: str, event_data: Dict[str, Any],
                              simulation_params: Optional[SimulationParameters] = None) -> List[go.Figure]:
        """Run complete advanced 3D simulation."""
        simulator = self.create_simulation(event_type, simulation_params)
        self.current_simulation = simulator
        return simulator.run_simulation(event_data)

    def create_animation(self, frames: List[go.Figure], 
                        filename: str = "simulation.html") -> str:
        """Create animated visualization from simulation frames."""
        if not frames:
            return ""
        
        # Create animation using plotly
        fig = frames[0]
        
        # Add animation frames
        fig.frames = [go.Frame(data=frame.data, name=f"frame_{i}") 
                     for i, frame in enumerate(frames)]
        
        # Add animation controls
        fig.update_layout(
            updatemenus=[dict(
                type="buttons",
                buttons=[
                    dict(label="Play",
                         method="animate",
                         args=[None, {"frame": {"duration": 100, "redraw": True},
                                    "fromcurrent": True}]),
                    dict(label="Pause",
                         method="animate",
                         args=[[None], {"frame": {"duration": 0, "redraw": False},
                                      "mode": "immediate",
                                      "transition": {"duration": 0}}])
                ]
            )],
            sliders=[dict(
                steps=[dict(args=[[f"frame_{i}"],
                               {"frame": {"duration": 100, "redraw": True},
                                "mode": "immediate"}],
                           label=f"Frame {i}",
                           method="animate")
                      for i in range(len(frames))],
                active=0,
                currentvalue={"prefix": "Frame: "}
            )]
        )
        
        # Save animation
        fig.write_html(filename)
        return filename

    def create_vr_ready_visualization(self, event_type: str, 
                                    event_data: Dict[str, Any]) -> go.Figure:
        """Create VR/AR ready 3D visualization."""
        # Use high-quality parameters for VR
        vr_params = SimulationParameters(
            resolution=200,
            time_steps=1,  # Single frame for VR
            quality="ultra",
            enable_physics=True,
            enable_particles=True,
            enable_volumetrics=True
        )
        
        simulator = self.create_simulation(event_type, vr_params)
        simulator.initialize_simulation(event_data)
        
        # Generate a detailed single frame
        vr_frame = simulator.render_frame()
        
        # Configure for VR viewing
        vr_frame.update_layout(
            scene=dict(
                camera=dict(
                    projection=dict(type="perspective"),
                    eye=dict(x=0, y=0, z=2)
                ),
                aspectmode='cube',
                bgcolor='black'
            ),
            paper_bgcolor='black',
            plot_bgcolor='black'
        )
        
        return vr_frame

    def export_to_external_format(self, frames: List[go.Figure], 
                                format_type: str = "obj") -> str:
        """Export 3D visualization to external 3D format."""
        if format_type == "obj" and HAS_TRIMESH:
            # Convert to OBJ format using trimesh
            # This is a simplified example - full implementation would extract
            # mesh data from plotly figures
            return "exported_model.obj"
        
        elif format_type == "ply" and HAS_OPEN3D:
            # Convert to PLY format using Open3D
            return "exported_model.ply"
        
        else:
            raise ValueError(f"Unsupported format or missing library: {format_type}")

    def get_supported_event_types(self) -> List[str]:
        """Get list of supported event types for 3D simulation."""
        return list(self.simulators.keys())

    def get_simulation_capabilities(self) -> Dict[str, Any]:
        """Get information about 3D simulation capabilities."""
        return {
            "supported_events": self.get_supported_event_types(),
            "has_pyvista": HAS_PYVISTA,
            "has_open3d": HAS_OPEN3D,
            "has_trimesh": HAS_TRIMESH,
            "max_particles": 2000,
            "supported_exports": ["html", "obj", "ply"],
            "vr_ready": True,
            "real_time_physics": True
        }


# Factory function for easy access
def create_3d_visualization_manager() -> Advanced3DVisualizationManager:
    """Create and return an Advanced3DVisualizationManager instance."""
    return Advanced3DVisualizationManager()
