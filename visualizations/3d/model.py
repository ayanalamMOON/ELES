"""
3D visualization models and rendering for E.L.E.S.

This module provides 3D visualization capabilities for extinction events,
including asteroid impacts, explosion spheres, and geographic models.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List, Tuple, Optional
import math


def render_asteroid_impact(impact_data: Dict[str, Any]) -> go.Figure:
    """Render 3D visualization of asteroid impact and resulting crater."""

    # Extract impact parameters
    crater_diameter = impact_data.get('crater_diameter_km', 10)
    impact_angle = impact_data.get('impact_angle', 45)  # degrees
    asteroid_diameter = impact_data.get('asteroid_diameter_km', 1)

    # Create crater geometry
    crater_radius = crater_diameter / 2
    crater_depth = crater_radius * 0.2  # Typical depth-to-diameter ratio

    # Generate crater mesh
    theta = np.linspace(0, 2*np.pi, 50)
    r = np.linspace(0, crater_radius, 25)
    R, THETA = np.meshgrid(r, theta)

    # Crater profile (parabolic)
    Z_crater = -crater_depth * (1 - (R/crater_radius)**2)
    X_crater = R * np.cos(THETA)
    Y_crater = R * np.sin(THETA)

    # Create surrounding terrain
    terrain_size = crater_radius * 3
    x_terrain = np.linspace(-terrain_size, terrain_size, 100)
    y_terrain = np.linspace(-terrain_size, terrain_size, 100)
    X_terrain, Y_terrain = np.meshgrid(x_terrain, y_terrain)

    # Terrain height (slightly undulating)
    Z_terrain = np.sin(X_terrain/10) * np.cos(Y_terrain/10) * 0.1

    # Combine crater and terrain
    distance_from_center = np.sqrt(X_terrain**2 + Y_terrain**2)
    crater_mask = distance_from_center <= crater_radius

    # Smooth transition from crater to terrain
    transition_zone = (distance_from_center > crater_radius) & (distance_from_center <= crater_radius * 1.2)

    Z_combined = Z_terrain.copy()
    Z_combined[crater_mask] = np.interp(distance_from_center[crater_mask],
                                       [0, crater_radius],
                                       [-crater_depth, 0])

    # Create 3D surface plot
    fig = go.Figure()

    # Add terrain surface
    fig.add_trace(go.Surface(
        x=X_terrain,
        y=Y_terrain,
        z=Z_combined,
        colorscale='Earth',
        name='Impact Crater',
        showscale=True,
        colorbar=dict(title="Elevation (km)")
    ))

    # Add asteroid trajectory
    if impact_angle != 90:  # Not vertical impact
        trajectory_length = crater_radius * 2
        traj_x = np.linspace(-trajectory_length * np.cos(np.radians(impact_angle)), 0, 50)
        traj_y = np.zeros_like(traj_x)
        traj_z = np.linspace(trajectory_length * np.sin(np.radians(impact_angle)), 0, 50)

        fig.add_trace(go.Scatter3d(
            x=traj_x,
            y=traj_y,
            z=traj_z,
            mode='lines+markers',
            line=dict(color='red', width=8),
            marker=dict(size=3),
            name='Asteroid Trajectory'
        ))

    # Add impact point marker
    fig.add_trace(go.Scatter3d(
        x=[0],
        y=[0],
        z=[0],
        mode='markers',
        marker=dict(size=10, color='red', symbol='x'),
        name='Impact Point'
    ))

    # Add ejecta pattern (simplified)
    ejecta_angles = np.linspace(0, 2*np.pi, 20)
    ejecta_distances = np.random.uniform(crater_radius*1.5, crater_radius*3, 20)
    ejecta_heights = np.random.uniform(0.1, 0.5, 20)

    ejecta_x = ejecta_distances * np.cos(ejecta_angles)
    ejecta_y = ejecta_distances * np.sin(ejecta_angles)
    ejecta_z = ejecta_heights

    fig.add_trace(go.Scatter3d(
        x=ejecta_x,
        y=ejecta_y,
        z=ejecta_z,
        mode='markers',
        marker=dict(size=5, color='orange', opacity=0.7),
        name='Ejecta'
    ))

    # Update layout
    fig.update_layout(
        title='3D Asteroid Impact Visualization',
        scene=dict(
            xaxis_title='Distance X (km)',
            yaxis_title='Distance Y (km)',
            zaxis_title='Elevation (km)',
            aspectmode='cube',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.2)
            )
        ),
        height=700
    )

    return fig


def render_explosion_sphere(explosion_data: Dict[str, Any]) -> go.Figure:
    """Render 3D explosion sphere with shock wave propagation."""

    # Explosion parameters
    max_radius = explosion_data.get('max_blast_radius_km', 100)
    energy = explosion_data.get('explosion_energy_joules', 1e20)
    time_steps = explosion_data.get('time_steps', 10)

    fig = go.Figure()

    # Create sphere geometry
    phi = np.linspace(0, 2*np.pi, 30)
    theta = np.linspace(0, np.pi, 20)
    phi_grid, theta_grid = np.meshgrid(phi, theta)

    # Multiple spheres for different blast zones
    blast_zones = [
        {'radius': max_radius * 0.2, 'color': 'red', 'name': 'Fireball', 'opacity': 0.9},
        {'radius': max_radius * 0.5, 'color': 'orange', 'name': 'Severe Blast', 'opacity': 0.6},
        {'radius': max_radius * 0.8, 'color': 'yellow', 'name': 'Moderate Blast', 'opacity': 0.4},
        {'radius': max_radius, 'color': 'lightblue', 'name': 'Light Damage', 'opacity': 0.2}
    ]

    for zone in blast_zones:
        radius = zone['radius']

        x = radius * np.sin(theta_grid) * np.cos(phi_grid)
        y = radius * np.sin(theta_grid) * np.sin(phi_grid)
        z = radius * np.cos(theta_grid)

        fig.add_trace(go.Surface(
            x=x, y=y, z=z,
            colorscale=[[0, zone['color']], [1, zone['color']]],
            opacity=zone['opacity'],
            name=zone['name'],
            showscale=False
        ))

    # Add ground plane
    ground_size = max_radius * 1.2
    x_ground = np.linspace(-ground_size, ground_size, 20)
    y_ground = np.linspace(-ground_size, ground_size, 20)
    X_ground, Y_ground = np.meshgrid(x_ground, y_ground)
    Z_ground = np.zeros_like(X_ground)

    fig.add_trace(go.Surface(
        x=X_ground,
        y=Y_ground,
        z=Z_ground,
        colorscale='Greys',
        opacity=0.3,
        name='Ground Level',
        showscale=False
    ))

    # Add explosion center
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode='markers',
        marker=dict(size=15, color='white',
                   line=dict(color='red', width=3)),
        name='Explosion Center'
    ))

    # Update layout
    fig.update_layout(
        title='3D Explosion Blast Zones',
        scene=dict(
            xaxis_title='Distance X (km)',
            yaxis_title='Distance Y (km)',
            zaxis_title='Height Z (km)',
            aspectmode='cube',
            camera=dict(
                eye=dict(x=1.2, y=1.2, z=0.8)
            )
        ),
        height=700
    )

    return fig


def render_damage_zones_3d(damage_data: Dict[str, Any]) -> go.Figure:
    """Render 3D damage zones with varying intensities."""

    # Damage zone parameters
    zones = damage_data.get('zones', {
        'crater': 5,
        'severe': 25,
        'moderate': 75,
        'light': 150,
        'minimal': 300
    })

    center = damage_data.get('center', (0, 0, 0))

    fig = go.Figure()

    # Color scheme for damage zones
    zone_colors = {
        'crater': 'black',
        'severe': 'red',
        'moderate': 'orange',
        'light': 'yellow',
        'minimal': 'lightgreen'
    }

    zone_opacities = {
        'crater': 0.9,
        'severe': 0.7,
        'moderate': 0.5,
        'light': 0.3,
        'minimal': 0.2
    }

    # Create cylindrical damage zones
    theta = np.linspace(0, 2*np.pi, 50)

    for zone_name, radius in zones.items():
        # Create cylinder for each zone
        height = radius * 0.1  # Height proportional to radius

        # Top and bottom circles
        x_circle = radius * np.cos(theta)
        y_circle = radius * np.sin(theta)
        z_top = np.full_like(theta, height)
        z_bottom = np.zeros_like(theta)

        # Cylindrical surface
        z_cyl = np.linspace(0, height, 20)
        theta_cyl, z_mesh = np.meshgrid(theta, z_cyl)
        x_cyl = radius * np.cos(theta_cyl)
        y_cyl = radius * np.sin(theta_cyl)

        # Add cylindrical surface
        fig.add_trace(go.Surface(
            x=x_cyl + center[0],
            y=y_cyl + center[1],
            z=z_mesh + center[2],
            colorscale=[[0, zone_colors[zone_name]], [1, zone_colors[zone_name]]],
            opacity=zone_opacities[zone_name],
            name=f'{zone_name.title()} Zone',
            showscale=False
        ))

    # Add buildings/structures for scale
    building_positions = [
        (50, 50, 0), (-50, 50, 0), (50, -50, 0), (-50, -50, 0),
        (100, 0, 0), (-100, 0, 0), (0, 100, 0), (0, -100, 0)
    ]

    for pos in building_positions:
        # Simple building representation
        building_height = np.random.uniform(5, 20)

        fig.add_trace(go.Scatter3d(
            x=[pos[0], pos[0]],
            y=[pos[1], pos[1]],
            z=[0, building_height],
            mode='lines',
            line=dict(color='gray', width=8),
            showlegend=False
        ))

        # Building top
        fig.add_trace(go.Scatter3d(
            x=[pos[0]],
            y=[pos[1]],
            z=[building_height],
            mode='markers',
            marker=dict(size=5, color='gray'),
            showlegend=False
        ))

    # Add impact center
    fig.add_trace(go.Scatter3d(
        x=[center[0]],
        y=[center[1]],
        z=[center[2]],
        mode='markers',
        marker=dict(size=15, color='red', symbol='x'),
        name='Impact Center'
    ))

    # Update layout
    fig.update_layout(
        title='3D Damage Zones Visualization',
        scene=dict(
            xaxis_title='Distance X (km)',
            yaxis_title='Distance Y (km)',
            zaxis_title='Height Z (km)',
            aspectmode='cube',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.0)
            )
        ),
        height=700
    )

    return fig


def render_geographic_model(geo_data: Dict[str, Any]) -> go.Figure:
    """Render 3D geographic model with topography and impact overlay."""

    # Geographic parameters
    lat_range = geo_data.get('lat_range', (35, 45))
    lon_range = geo_data.get('lon_range', (-125, -115))
    resolution = geo_data.get('resolution', 50)

    # Create coordinate grids
    lats = np.linspace(lat_range[0], lat_range[1], resolution)
    lons = np.linspace(lon_range[0], lon_range[1], resolution)
    LON, LAT = np.meshgrid(lons, lats)

    # Generate synthetic elevation data
    if 'elevation' not in geo_data:
        # Create realistic-looking terrain
        elevation = np.zeros_like(LON)

        # Add mountain ranges
        for _ in range(3):
            center_lat = np.random.uniform(lat_range[0], lat_range[1])
            center_lon = np.random.uniform(lon_range[0], lon_range[1])
            mountain_height = np.random.uniform(1, 3)  # km
            mountain_width = np.random.uniform(1, 3)

            distance = np.sqrt((LAT - center_lat)**2 + (LON - center_lon)**2)
            mountain = mountain_height * np.exp(-distance**2 / mountain_width)
            elevation += mountain

        # Add valleys
        for _ in range(2):
            center_lat = np.random.uniform(lat_range[0], lat_range[1])
            center_lon = np.random.uniform(lon_range[0], lon_range[1])
            valley_depth = np.random.uniform(0.2, 0.8)
            valley_width = np.random.uniform(2, 4)

            distance = np.sqrt((LAT - center_lat)**2 + (LON - center_lon)**2)
            valley = -valley_depth * np.exp(-distance**2 / valley_width)
            elevation += valley

        # Add noise for realism
        elevation += np.random.normal(0, 0.1, elevation.shape)

    else:
        elevation = geo_data['elevation']

    # Create 3D surface
    fig = go.Figure()

    # Add topographic surface
    fig.add_trace(go.Surface(
        x=LON,
        y=LAT,
        z=elevation,
        colorscale='Earth',
        name='Topography',
        colorbar=dict(title="Elevation (km)")
    ))

    # Add impact overlay if specified
    if 'impact_location' in geo_data:
        impact_lat, impact_lon = geo_data['impact_location']
        impact_radius = geo_data.get('impact_radius_km', 50)

        # Create impact crater
        distance_from_impact = np.sqrt((LAT - impact_lat)**2 + (LON - impact_lon)**2)
        impact_mask = distance_from_impact <= (impact_radius / 111)  # Convert km to degrees roughly

        # Modify elevation at impact site
        crater_depth = geo_data.get('crater_depth_km', 0.5)
        elevation_with_crater = elevation.copy()
        elevation_with_crater[impact_mask] -= crater_depth

        # Add crater surface
        fig.add_trace(go.Surface(
            x=LON,
            y=LAT,
            z=elevation_with_crater,
            colorscale='Reds',
            opacity=0.7,
            name='Impact Crater',
            showscale=False
        ))

        # Add impact point marker
        impact_elevation = np.interp([impact_lat, impact_lon],
                                   [LAT.flatten(), LON.flatten()],
                                   elevation.flatten())

        fig.add_trace(go.Scatter3d(
            x=[impact_lon],
            y=[impact_lat],
            z=[impact_elevation[0] if len(impact_elevation) > 0 else 0],
            mode='markers',
            marker=dict(size=15, color='red', symbol='x'),
            name='Impact Point'
        ))

    # Add population centers
    if 'cities' in geo_data:
        cities = geo_data['cities']
        for city in cities:
            city_elevation = np.interp([city['lat'], city['lon']],
                                     [LAT.flatten(), LON.flatten()],
                                     elevation.flatten())

            fig.add_trace(go.Scatter3d(
                x=[city['lon']],
                y=[city['lat']],
                z=[city_elevation[0] if len(city_elevation) > 0 else 0],
                mode='markers+text',
                marker=dict(size=8, color='blue'),
                text=[city['name']],
                textposition="top center",
                name=city['name']
            ))

    # Update layout
    fig.update_layout(
        title='3D Geographic Impact Model',
        scene=dict(
            xaxis_title='Longitude',
            yaxis_title='Latitude',
            zaxis_title='Elevation (km)',
            camera=dict(
                eye=dict(x=1.2, y=1.2, z=1.0)
            )
        ),
        height=700
    )

    return fig


def create_atmospheric_model_3d(atmosphere_data: Dict[str, Any]) -> go.Figure:
    """Create 3D model of atmospheric effects."""

    # Atmospheric parameters
    max_altitude = atmosphere_data.get('max_altitude_km', 100)
    debris_cloud_radius = atmosphere_data.get('debris_cloud_radius_km', 500)

    fig = go.Figure()

    # Create atmospheric layers
    altitudes = [0, 10, 50, 100]  # km
    layer_names = ['Troposphere', 'Stratosphere', 'Mesosphere', 'Thermosphere']
    layer_colors = ['lightblue', 'lightgreen', 'lightyellow', 'lightcoral']

    for i, (alt, name, color) in enumerate(zip(altitudes[:-1], layer_names, layer_colors)):
        next_alt = altitudes[i + 1]

        # Create cylindrical layer
        theta = np.linspace(0, 2*np.pi, 30)
        r = np.linspace(0, debris_cloud_radius, 20)
        R, THETA = np.meshgrid(r, theta)

        X = R * np.cos(THETA)
        Y = R * np.sin(THETA)
        Z_bottom = np.full_like(X, alt)
        Z_top = np.full_like(X, next_alt)

        # Add layer boundaries
        fig.add_trace(go.Surface(
            x=X, y=Y, z=Z_bottom,
            colorscale=[[0, color], [1, color]],
            opacity=0.2,
            name=f'{name} Bottom',
            showscale=False
        ))

    # Add debris cloud
    debris_altitude = atmosphere_data.get('debris_altitude_km', 30)
    debris_thickness = atmosphere_data.get('debris_thickness_km', 20)

    # Create debris particles
    n_particles = 200
    particle_r = np.random.uniform(0, debris_cloud_radius, n_particles)
    particle_theta = np.random.uniform(0, 2*np.pi, n_particles)
    particle_z = np.random.uniform(debris_altitude, debris_altitude + debris_thickness, n_particles)

    particle_x = particle_r * np.cos(particle_theta)
    particle_y = particle_r * np.sin(particle_theta)

    # Color particles by density/size
    particle_sizes = np.random.exponential(5, n_particles)

    fig.add_trace(go.Scatter3d(
        x=particle_x,
        y=particle_y,
        z=particle_z,
        mode='markers',
        marker=dict(
            size=particle_sizes,
            color=particle_z,
            colorscale='Greys',
            opacity=0.6,
            colorbar=dict(title="Altitude (km)")
        ),
        name='Debris Cloud'
    ))

    # Add ground level
    ground_theta = np.linspace(0, 2*np.pi, 50)
    ground_r = np.linspace(0, debris_cloud_radius * 1.1, 30)
    GROUND_R, GROUND_THETA = np.meshgrid(ground_r, ground_theta)

    ground_x = GROUND_R * np.cos(GROUND_THETA)
    ground_y = GROUND_R * np.sin(GROUND_THETA)
    ground_z = np.zeros_like(ground_x)

    fig.add_trace(go.Surface(
        x=ground_x,
        y=ground_y,
        z=ground_z,
        colorscale='Browns',
        opacity=0.5,
        name='Ground',
        showscale=False
    ))

    # Update layout
    fig.update_layout(
        title='3D Atmospheric Effects Model',
        scene=dict(
            xaxis_title='Distance X (km)',
            yaxis_title='Distance Y (km)',
            zaxis_title='Altitude (km)',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.2)
            )
        ),
        height=700
    )

    return fig
