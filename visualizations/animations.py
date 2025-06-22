"""
Animation and temporal visualization tools for E.L.E.S.

This module provides tools for creating animated visualizations
showing the temporal evolution of extinction events.
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Callable
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from matplotlib.patches import Circle


def create_impact_animation(impact_data: Dict[str, Any],
                          duration_frames: int = 100) -> animation.FuncAnimation:
    """Create animation showing asteroid impact progression."""

    # Setup figure and axis
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(-1000, 1000)
    ax.set_ylim(-1000, 1000)
    ax.set_aspect('equal')
    ax.set_title('Asteroid Impact Animation')
    ax.set_xlabel('Distance (km)')
    ax.set_ylabel('Distance (km)')

    # Impact parameters
    max_radius = impact_data.get('max_blast_radius', 1000)
    crater_radius = impact_data.get('crater_diameter_km', 10) / 2

    # Initialize plot elements
    crater_circle = Circle((0, 0), 0, color='red', alpha=0.8)
    blast_wave = Circle((0, 0), 0, fill=False, color='orange', linewidth=3)
    shockwave = Circle((0, 0), 0, fill=False, color='yellow', linewidth=2)

    ax.add_patch(crater_circle)
    ax.add_patch(blast_wave)
    ax.add_patch(shockwave)

    def animate(frame):
        """Animation function for each frame."""
        progress = frame / duration_frames

        # Crater forms immediately
        if progress > 0.1:
            crater_circle.set_radius(crater_radius)

        # Blast wave expansion
        blast_radius = max_radius * min(progress * 2, 1.0)
        blast_wave.set_radius(blast_radius)

        # Shockwave follows blast wave
        shock_radius = max_radius * min((progress - 0.1) * 2, 1.0)
        if shock_radius > 0:
            shockwave.set_radius(shock_radius)

        return crater_circle, blast_wave, shockwave

    # Create animation
    anim = animation.FuncAnimation(
        fig, animate, frames=duration_frames,
        interval=50, blit=True, repeat=True
    )

    return anim


def create_spread_animation(spread_data: Dict[str, Any]) -> go.Figure:
    """Create animated visualization of pandemic spread."""

    # Generate sample data if none provided
    if 'timeline' not in spread_data:
        days = list(range(0, 365, 7))  # Weekly data points
        countries = ['USA', 'China', 'India', 'Brazil', 'Russia', 'Japan']

        # Generate synthetic pandemic spread data
        data = []
        for day in days:
            for country in countries:
                base_cases = np.random.exponential(1000)
                growth_factor = min(day / 100, 3)  # Growth slows over time
                cases = int(base_cases * growth_factor * np.random.uniform(0.5, 1.5))

                data.append({
                    'day': day,
                    'country': country,
                    'cases': cases,
                    'deaths': int(cases * 0.02)  # 2% mortality rate
                })

        df = pd.DataFrame(data)
    else:
        df = pd.DataFrame(spread_data['timeline'])

    # Create animated scatter plot
    fig = px.scatter(
        df,
        x='cases',
        y='deaths',
        color='country',
        size='cases',
        animation_frame='day',
        hover_name='country',
        title='Pandemic Spread Animation',
        labels={'cases': 'Total Cases', 'deaths': 'Total Deaths'},
        size_max=50
    )

    # Update layout
    fig.update_layout(
        xaxis=dict(type='log', title='Total Cases (log scale)'),
        yaxis=dict(type='log', title='Total Deaths (log scale)'),
        height=600
    )

    return fig


def create_recovery_animation(recovery_data: Dict[str, Any]) -> go.Figure:
    """Create animation showing post-event recovery progress."""

    # Generate sample recovery data
    if 'recovery_timeline' not in recovery_data:
        months = list(range(0, 121, 6))  # 10 years, every 6 months
        sectors = ['Infrastructure', 'Agriculture', 'Economy', 'Population', 'Technology']

        data = []
        for month in months:
            for sector in sectors:
                # Different recovery rates for different sectors
                base_recovery = {
                    'Infrastructure': 0.8,
                    'Agriculture': 0.9,
                    'Economy': 0.7,
                    'Population': 0.6,
                    'Technology': 0.85
                }

                # Recovery follows exponential approach to base level
                recovery_rate = base_recovery[sector]
                progress = recovery_rate * (1 - np.exp(-month / 24))  # 24-month time constant

                data.append({
                    'month': month,
                    'sector': sector,
                    'recovery_percentage': progress * 100
                })

        df = pd.DataFrame(data)
    else:
        df = pd.DataFrame(recovery_data['recovery_timeline'])

    # Create animated bar chart
    fig = px.bar(
        df,
        x='sector',
        y='recovery_percentage',
        color='sector',
        animation_frame='month',
        title='Recovery Progress Animation',
        labels={'recovery_percentage': 'Recovery Progress (%)', 'sector': 'Sector'},
        range_y=[0, 100]
    )

    fig.update_layout(height=500)

    return fig


def animate_parameter_sweep(parameter_name: str,
                          parameter_values: List[float],
                          simulation_results: List[Dict[str, Any]]) -> go.Figure:
    """Create animation showing how results change with parameter sweep."""

    # Prepare data for animation
    data = []
    for i, (param_val, result) in enumerate(zip(parameter_values, simulation_results)):
        data.append({
            'parameter_value': param_val,
            'severity': result.get('severity', 0),
            'casualties': result.get('casualties', 0),
            'economic_impact': result.get('economic_impact', 0),
            'frame': i
        })

    df = pd.DataFrame(data)

    # Create animated scatter plot
    fig = px.scatter(
        df,
        x='parameter_value',
        y='severity',
        size='casualties',
        color='economic_impact',
        animation_frame='frame',
        title=f'Parameter Sweep Animation: {parameter_name}',
        labels={
            'parameter_value': parameter_name,
            'severity': 'Severity Level',
            'casualties': 'Casualties',
            'economic_impact': 'Economic Impact'
        },
        range_y=[0, 6]
    )

    fig.update_layout(height=500)

    return fig


def create_temporal_heatmap_animation(temporal_data: Dict[str, Any]) -> go.Figure:
    """Create animated heatmap showing temporal evolution."""

    # Generate sample temporal data
    if 'temporal_grid' not in temporal_data:
        # Create synthetic space-time data
        x_coords = np.linspace(-100, 100, 20)
        y_coords = np.linspace(-100, 100, 20)
        time_steps = list(range(0, 100, 5))

        frames = []
        for t in time_steps:
            # Create wave-like pattern that evolves over time
            X, Y = np.meshgrid(x_coords, y_coords)
            distance = np.sqrt(X**2 + Y**2)
            intensity = np.exp(-(distance - t*2)**2 / 500) * np.exp(-distance/50)

            frames.append({
                'time': t,
                'x': X.flatten(),
                'y': Y.flatten(),
                'intensity': intensity.flatten()
            })

        # Convert to DataFrame
        df_list = []
        for frame in frames:
            frame_df = pd.DataFrame({
                'x': frame['x'],
                'y': frame['y'],
                'intensity': frame['intensity'],
                'time': frame['time']
            })
            df_list.append(frame_df)

        df = pd.concat(df_list, ignore_index=True)
    else:
        df = pd.DataFrame(temporal_data['temporal_grid'])

    # Create animated heatmap using scatter plot
    fig = px.scatter(
        df,
        x='x',
        y='y',
        color='intensity',
        animation_frame='time',
        title='Temporal Impact Evolution',
        labels={'x': 'X Coordinate (km)', 'y': 'Y Coordinate (km)', 'intensity': 'Impact Intensity'},
        color_continuous_scale='Reds'
    )

    # Update traces to look more like heatmap
    fig.update_traces(marker=dict(size=8, symbol='square'))
    fig.update_layout(height=600)

    return fig


def create_multi_scenario_timeline(scenarios: List[Dict[str, Any]]) -> go.Figure:
    """Create animated timeline comparing multiple scenarios."""

    fig = go.Figure()

    # Create timeline data for each scenario
    for i, scenario in enumerate(scenarios):
        scenario_name = scenario.get('name', f'Scenario {i+1}')

        # Sample timeline events
        events = scenario.get('timeline_events', [
            {'time': 0, 'event': 'Initial Impact', 'severity': 6},
            {'time': 1, 'event': 'Immediate Effects', 'severity': 5},
            {'time': 7, 'event': 'Secondary Effects', 'severity': 4},
            {'time': 30, 'event': 'Recovery Begins', 'severity': 3},
            {'time': 365, 'event': 'Long-term Effects', 'severity': 2}
        ])

        times = [event['time'] for event in events]
        severities = [event['severity'] for event in events]
        event_names = [event['event'] for event in events]

        fig.add_trace(go.Scatter(
            x=times,
            y=severities,
            mode='lines+markers',
            name=scenario_name,
            text=event_names,
            hovertemplate='<b>%{text}</b><br>Day: %{x}<br>Severity: %{y}<extra></extra>'
        ))

    fig.update_layout(
        title='Multi-Scenario Timeline Comparison',
        xaxis_title='Time (days)',
        yaxis_title='Severity Level',
        yaxis=dict(range=[0, 6]),
        height=500
    )

    return fig


def save_animation(anim: animation.FuncAnimation,
                  filename: str,
                  writer: str = 'pillow') -> None:
    """Save matplotlib animation to file."""

    try:
        if writer == 'pillow':
            anim.save(filename, writer='pillow', fps=20)
        elif writer == 'ffmpeg':
            anim.save(filename, writer='ffmpeg', fps=20, bitrate=1800)
        else:
            anim.save(filename, writer=writer)

        print(f"Animation saved to {filename}")

    except Exception as e:
        print(f"Error saving animation: {e}")


def create_3d_animation(data_3d: Dict[str, Any]) -> go.Figure:
    """Create 3D animated visualization."""

    # Generate sample 3D data
    if '3d_data' not in data_3d:
        # Create synthetic 3D explosion data
        frames = []
        for t in range(0, 50, 2):
            # Create expanding sphere
            phi = np.linspace(0, 2*np.pi, 20)
            theta = np.linspace(0, np.pi, 20)

            phi_grid, theta_grid = np.meshgrid(phi, theta)

            radius = t * 2  # Expanding radius
            x = radius * np.sin(theta_grid) * np.cos(phi_grid)
            y = radius * np.sin(theta_grid) * np.sin(phi_grid)
            z = radius * np.cos(theta_grid)

            frames.append({
                'time': t,
                'x': x.flatten(),
                'y': y.flatten(),
                'z': z.flatten()
            })

        # Convert to DataFrame
        df_list = []
        for frame in frames:
            frame_df = pd.DataFrame({
                'x': frame['x'],
                'y': frame['y'],
                'z': frame['z'],
                'time': frame['time']
            })
            df_list.append(frame_df)

        df = pd.concat(df_list, ignore_index=True)
    else:
        df = pd.DataFrame(data_3d['3d_data'])

    # Create 3D animated scatter plot
    fig = px.scatter_3d(
        df,
        x='x',
        y='y',
        z='z',
        animation_frame='time',
        title='3D Impact Animation',
        labels={'x': 'X (km)', 'y': 'Y (km)', 'z': 'Z (km)'}
    )

    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[-100, 100]),
            yaxis=dict(range=[-100, 100]),
            zaxis=dict(range=[-100, 100])
        ),
        height=600
    )

    return fig
