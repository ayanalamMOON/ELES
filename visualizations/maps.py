"""
Geographic mapping and spatial analysis for E.L.E.S.

This module provides geographic visualization tools for displaying
spatial impact patterns and population analysis.
"""

import folium
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple, Optional


def plot_world_impact_map(impact_data: Dict[str, Any],
                         impact_location: Tuple[float, float] = (0, 0)) -> folium.Map:
    """Create world map showing impact zones and affected areas."""

    # Create base map centered on impact location
    lat, lon = impact_location
    m = folium.Map(location=[lat, lon], zoom_start=5)

    # Add impact crater
    crater_radius = impact_data.get('crater_diameter_km', 10) * 500  # Convert to meters for folium

    folium.Circle(
        location=[lat, lon],
        radius=crater_radius,
        popup='Impact Crater',
        color='red',
        fill=True,
        fillColor='red',
        fillOpacity=0.7
    ).add_to(m)

    # Add damage zones
    damage_zones = impact_data.get('damage_zones', {})
    colors = ['orange', 'yellow', 'lightblue', 'lightgreen']

    for i, (zone_name, radius_km) in enumerate(damage_zones.items()):
        if i < len(colors):
            folium.Circle(
                location=[lat, lon],
                radius=radius_km * 1000,  # Convert km to meters
                popup=f'{zone_name}: {radius_km} km',
                color=colors[i],
                fill=False,
                weight=3
            ).add_to(m)

    # Add affected population centers
    population_centers = impact_data.get('affected_cities', [])
    for city in population_centers:
        folium.Marker(
            location=[city.get('lat', 0), city.get('lon', 0)],
            popup=f"{city.get('name', 'Unknown')}<br>Population: {city.get('population', 0):,}",
            icon=folium.Icon(color='darkred', icon='home')
        ).add_to(m)

    return m


def plot_regional_damage_map(region_data: Dict[str, Any],
                           region_bounds: Tuple[Tuple[float, float], Tuple[float, float]]) -> folium.Map:
    """Create detailed regional damage assessment map."""

    # Calculate center of region
    ((south, west), (north, east)) = region_bounds
    center_lat = (south + north) / 2
    center_lon = (west + east) / 2

    # Create map
    m = folium.Map(location=[center_lat, center_lon], zoom_start=8)

    # Add damage intensity heatmap
    damage_points = region_data.get('damage_points', [])

    if damage_points:
        # Convert damage points to heatmap data
        heat_data = [[point['lat'], point['lon'], point['intensity']]
                    for point in damage_points]

        from folium.plugins import HeatMap
        HeatMap(heat_data).add_to(m)

    # Add infrastructure damage markers
    infrastructure = region_data.get('infrastructure_damage', [])

    for facility in infrastructure:
        damage_level = facility.get('damage_level', 0)
        color = 'red' if damage_level > 0.7 else 'orange' if damage_level > 0.3 else 'green'

        folium.CircleMarker(
            location=[facility.get('lat', 0), facility.get('lon', 0)],
            radius=8,
            popup=f"{facility.get('name', 'Unknown')}<br>Damage: {damage_level*100:.1f}%",
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.8
        ).add_to(m)

    return m


def plot_evacuation_zones(evacuation_data: Dict[str, Any]) -> folium.Map:
    """Create evacuation zone map with routes and safe areas."""

    center_location = evacuation_data.get('center', [40.0, -100.0])
    m = folium.Map(location=center_location, zoom_start=6)

    # Add evacuation zones
    zones = evacuation_data.get('zones', [])

    for zone in zones:
        # Create polygon for evacuation zone
        if 'boundary' in zone:
            folium.Polygon(
                locations=zone['boundary'],
                popup=f"Evacuation Zone: {zone.get('name', 'Unknown')}",
                color='red',
                fill=True,
                fillColor='red',
                fillOpacity=0.3
            ).add_to(m)

    # Add evacuation routes
    routes = evacuation_data.get('routes', [])

    for route in routes:
        if 'path' in route:
            folium.PolyLine(
                locations=route['path'],
                popup=f"Evacuation Route: {route.get('name', 'Unknown')}",
                color='blue',
                weight=5,
                opacity=0.8
            ).add_to(m)

    # Add safe zones
    safe_zones = evacuation_data.get('safe_zones', [])

    for safe_zone in safe_zones:
        folium.CircleMarker(
            location=[safe_zone.get('lat', 0), safe_zone.get('lon', 0)],
            radius=15,
            popup=f"Safe Zone: {safe_zone.get('name', 'Unknown')}<br>Capacity: {safe_zone.get('capacity', 0):,}",
            color='green',
            fill=True,
            fillColor='green',
            fillOpacity=0.8
        ).add_to(m)

    return m


def plot_population_centers(population_data: Dict[str, Any]) -> go.Figure:
    """Create interactive population centers visualization."""

    # Extract population center data
    cities = population_data.get('cities', [])

    if not cities:
        # Generate sample data
        cities = [
            {'name': 'New York', 'lat': 40.7128, 'lon': -74.0060, 'population': 8400000},
            {'name': 'Los Angeles', 'lat': 34.0522, 'lon': -118.2437, 'population': 3900000},
            {'name': 'Chicago', 'lat': 41.8781, 'lon': -87.6298, 'population': 2700000},
            {'name': 'Houston', 'lat': 29.7604, 'lon': -95.3698, 'population': 2300000},
            {'name': 'Phoenix', 'lat': 33.4484, 'lon': -112.0740, 'population': 1600000}
        ]

    # Create scatter plot on map
    lats = [city['lat'] for city in cities]
    lons = [city['lon'] for city in cities]
    populations = [city['population'] for city in cities]
    names = [city['name'] for city in cities]

    fig = go.Figure(data=go.Scattergeo(
        lon=lons,
        lat=lats,
        text=names,
        mode='markers+text',
        marker=dict(
            size=[np.log10(pop) * 3 for pop in populations],
            color=populations,
            colorscale='Viridis',
            cmin=min(populations),
            cmax=max(populations),
            colorbar=dict(title="Population"),
            line=dict(width=1, color='white')
        ),
        textposition="top center"
    ))

    fig.update_layout(
        title='Population Centers',
        geo=dict(
            projection_type='albers usa',
            showland=True,
            landcolor='lightgray',
            showocean=True,
            oceancolor='lightblue',
            showcountries=True,
            countrycolor='white'
        ),
        height=600
    )

    return fig


def plot_global_risk_assessment(risk_data: Dict[str, Any]) -> go.Figure:
    """Create global risk assessment choropleth map."""

    # Sample country risk data
    countries = ['United States', 'China', 'India', 'Brazil', 'Russia',
                'Japan', 'Germany', 'United Kingdom', 'France', 'Italy']
    risk_levels = np.random.uniform(1, 6, len(countries))

    fig = go.Figure(data=go.Choropleth(
        locations=countries,
        z=risk_levels,
        locationmode='country names',
        colorscale='Reds',
        colorbar=dict(title="Risk Level (1-6)"),
        hovertemplate='<b>%{locations}</b><br>Risk Level: %{z:.1f}<extra></extra>'
    ))

    fig.update_layout(
        title='Global Risk Assessment by Country',
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='equirectangular'
        ),
        height=500
    )

    return fig


def create_impact_radius_visualization(center_coords: Tuple[float, float],
                                     radii: Dict[str, float]) -> folium.Map:
    """Create visualization showing different impact radii."""

    lat, lon = center_coords
    m = folium.Map(location=[lat, lon], zoom_start=6)

    # Define colors for different damage zones
    zone_colors = {
        'crater': '#8B0000',
        'severe_blast': '#FF0000',
        'moderate_blast': '#FF8C00',
        'light_damage': '#FFD700',
        'thermal_radiation': '#FFA500'
    }

    # Add circles for each radius
    for zone_name, radius_km in radii.items():
        color = zone_colors.get(zone_name, '#808080')

        folium.Circle(
            location=[lat, lon],
            radius=radius_km * 1000,  # Convert km to meters
            popup=f'{zone_name.replace("_", " ").title()}: {radius_km:.1f} km',
            color=color,
            fill=zone_name == 'crater',
            fillColor=color,
            fillOpacity=0.3 if zone_name == 'crater' else 0,
            weight=3
        ).add_to(m)

    # Add center marker
    folium.Marker(
        location=[lat, lon],
        popup='Impact Center',
        icon=folium.Icon(color='red', icon='crosshairs')
    ).add_to(m)

    return m


def plot_population_density_impact(density_data: pd.DataFrame) -> go.Figure:
    """Create population density impact visualization."""

    # If no data provided, create sample data
    if density_data.empty:
        # Create sample grid
        lats = np.linspace(35, 45, 20)
        lons = np.linspace(-125, -115, 20)

        lat_grid, lon_grid = np.meshgrid(lats, lons)
        density_grid = np.random.exponential(100, (20, 20))

        # Flatten for plotting
        density_data = pd.DataFrame({
            'lat': lat_grid.flatten(),
            'lon': lon_grid.flatten(),
            'density': density_grid.flatten()
        })

    fig = px.density_mapbox(
        density_data,
        lat='lat',
        lon='lon',
        z='density',
        radius=10,
        center=dict(lat=density_data['lat'].mean(), lon=density_data['lon'].mean()),
        zoom=5,
        mapbox_style="open-street-map",
        title="Population Density Impact Analysis"
    )

    fig.update_layout(height=600)

    return fig
