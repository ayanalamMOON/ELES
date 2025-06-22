"""
Interactive visualization components for E.L.E.S.

This module provides interactive visualization tools using Plotly and other
interactive libraries for dynamic exploration of simulation results.
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import streamlit as st


def create_interactive_timeline(simulation_data: Dict[str, Any]) -> go.Figure:
    """Create interactive timeline visualization of event progression."""

    # Extract timeline data
    timeline = simulation_data.get('timeline', {})

    fig = go.Figure()

    # Add timeline events
    if timeline:
        times = list(timeline.keys())
        events = list(timeline.values())

        fig.add_trace(go.Scatter(
            x=times,
            y=range(len(times)),
            mode='markers+text',
            text=events,
            textposition="middle right",
            marker=dict(size=15, color='red'),
            name='Events'
        ))

    fig.update_layout(
        title="Event Timeline",
        xaxis_title="Time",
        yaxis_title="Event Sequence",
        showlegend=False,
        height=400
    )

    return fig


def create_parameter_explorer(event_type: str, parameter_ranges: Dict[str, tuple]) -> go.Figure:
    """Create interactive parameter exploration interface."""

    # Create parameter sweep visualization
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=['Severity vs Parameter 1', 'Casualties vs Parameter 2',
                       'Economic Impact', 'Recovery Time'],
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )

    # Example parameter sweep data
    param1_values = np.linspace(*parameter_ranges.get('param1', (0, 10)), 20)
    severities = np.random.randint(1, 7, 20)
    casualties = np.random.exponential(1000000, 20)

    # Add traces
    fig.add_trace(
        go.Scatter(x=param1_values, y=severities, mode='markers+lines',
                  name='Severity', marker=dict(color='red')),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=param1_values, y=casualties, mode='markers+lines',
                  name='Casualties', marker=dict(color='blue')),
        row=1, col=2
    )

    # Economic impact heatmap
    fig.add_trace(
        go.Heatmap(z=np.random.random((10, 10)), colorscale='Reds',
                  name='Economic Impact'),
        row=2, col=1
    )

    # Recovery time bar chart
    regions = ['North America', 'Europe', 'Asia', 'Africa', 'South America']
    recovery_times = np.random.randint(10, 100, 5)

    fig.add_trace(
        go.Bar(x=regions, y=recovery_times, name='Recovery Time',
               marker=dict(color='green')),
        row=2, col=2
    )

    fig.update_layout(
        title=f"Parameter Explorer - {event_type.title()}",
        height=600,
        showlegend=False
    )

    return fig


def create_scenario_comparison(scenarios: List[Dict[str, Any]]) -> go.Figure:
    """Create interactive comparison of multiple scenarios."""

    fig = go.Figure()

    # Extract data for comparison
    scenario_names = [s.get('name', f'Scenario {i+1}') for i, s in enumerate(scenarios)]
    severities = [s.get('severity', 0) for s in scenarios]
    casualties = [s.get('casualties', 0) for s in scenarios]
    economic_impact = [s.get('economic_impact', 0) for s in scenarios]

    # Create multi-dimensional comparison
    fig.add_trace(go.Scatterpolar(
        r=severities,
        theta=scenario_names,
        fill='toself',
        name='Severity',
        line=dict(color='red')
    ))

    # Normalize other metrics to 0-6 scale for radar chart
    max_casualties = max(casualties) if casualties else 1
    max_economic = max(economic_impact) if economic_impact else 1

    normalized_casualties = [6 * c / max_casualties for c in casualties]
    normalized_economic = [6 * e / max_economic for e in economic_impact]

    fig.add_trace(go.Scatterpolar(
        r=normalized_casualties,
        theta=scenario_names,
        fill='toself',
        name='Casualties (normalized)',
        line=dict(color='blue')
    ))

    fig.add_trace(go.Scatterpolar(
        r=normalized_economic,
        theta=scenario_names,
        fill='toself',
        name='Economic Impact (normalized)',
        line=dict(color='green')
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 6]
            )),
        title="Scenario Comparison (Radar Chart)",
        height=500
    )

    return fig


def create_real_time_monitor(simulation_data: Dict[str, Any]) -> go.Figure:
    """Create real-time monitoring dashboard for ongoing simulation."""

    # Create subplots for different metrics
    fig = make_subplots(
        rows=2, cols=3,
        subplot_titles=['Population', 'Economic Impact', 'Infrastructure',
                       'Recovery Progress', 'Resource Availability', 'Risk Level'],
        specs=[[{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}],
               [{"type": "scatter"}, {"type": "bar"}, {"type": "gauge"}]]
    )

    # Population indicator
    current_population = simulation_data.get('current_population', 7800000000)
    population_loss = simulation_data.get('population_loss', 0.1)

    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=current_population,
        delta={'reference': 7800000000},
        title={'text': "Population"},
        gauge={'axis': {'range': [None, 8000000000]},
               'bar': {'color': "darkblue"},
               'bgcolor': "white",
               'borderwidth': 2,
               'bordercolor': "gray"}),
        row=1, col=1
    )

    # Economic impact indicator
    economic_loss = simulation_data.get('economic_loss', 1000000000000)

    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=economic_loss,
        title={'text': "Economic Loss ($)"},
        delta={'reference': 0, 'valueformat': '.0f'}),
        row=1, col=2
    )

    # Infrastructure indicator
    infrastructure_damage = simulation_data.get('infrastructure_damage', 25)

    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=infrastructure_damage,
        title={'text': "Infrastructure Damage (%)"},
        gauge={'axis': {'range': [None, 100]},
               'bar': {'color': "red"},
               'steps': [{'range': [0, 25], 'color': "lightgray"},
                        {'range': [25, 50], 'color': "yellow"},
                        {'range': [50, 100], 'color': "red"}]}),
        row=1, col=3
    )

    # Recovery progress timeline
    recovery_days = list(range(0, 365, 30))
    recovery_progress = [0, 5, 15, 30, 50, 65, 75, 85, 90, 95, 98, 100, 100]

    fig.add_trace(go.Scatter(
        x=recovery_days,
        y=recovery_progress[:len(recovery_days)],
        mode='lines+markers',
        name='Recovery Progress',
        line=dict(color='green')),
        row=2, col=1
    )

    # Resource availability
    resources = ['Food', 'Water', 'Energy', 'Medical', 'Transport']
    availability = [80, 60, 40, 70, 30]

    fig.add_trace(go.Bar(
        x=resources,
        y=availability,
        name='Resource Availability (%)',
        marker=dict(color=['green' if x > 60 else 'orange' if x > 30 else 'red' for x in availability])),
        row=2, col=2
    )

    # Overall risk level gauge
    risk_level = simulation_data.get('risk_level', 4)

    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=risk_level,
        title={'text': "Risk Level"},
        gauge={'axis': {'range': [None, 6]},
               'bar': {'color': "darkred"},
               'steps': [{'range': [0, 2], 'color': "lightgreen"},
                        {'range': [2, 4], 'color': "yellow"},
                        {'range': [4, 6], 'color': "red"}]}),
        row=2, col=3
    )

    fig.update_layout(
        title="Real-Time Simulation Monitor",
        height=700
    )

    return fig


def create_interactive_map(impact_data: Dict[str, Any]) -> go.Figure:
    """Create interactive geographical impact map."""

    # Sample geographic data
    lats = np.random.uniform(-60, 60, 100)
    lons = np.random.uniform(-180, 180, 100)
    impact_intensity = np.random.exponential(2, 100)

    fig = go.Figure(data=go.Scattergeo(
        lon=lons,
        lat=lats,
        text=[f'Impact: {i:.1f}' for i in impact_intensity],
        mode='markers',
        marker=dict(
            size=impact_intensity * 5,
            color=impact_intensity,
            colorscale='Reds',
            cmin=0,
            cmax=max(impact_intensity),
            colorbar=dict(title="Impact Intensity")
        )
    ))

    fig.update_layout(
        title='Global Impact Distribution',
        geo=dict(
            projection_type='natural earth',
            showland=True,
            landcolor='lightgray',
            showocean=True,
            oceancolor='lightblue'
        ),
        height=500
    )

    return fig


def create_parameter_slider_interface():
    """Create Streamlit slider interface for parameter exploration."""

    if 'st' in globals():
        st.sidebar.header("Parameter Controls")

        # Event type selection
        event_type = st.sidebar.selectbox(
            "Event Type",
            ['asteroid', 'supervolcano', 'pandemic', 'climate_collapse', 'gamma_ray_burst', 'ai_extinction']
        )

        # Event-specific parameters
        if event_type == 'asteroid':
            diameter = st.sidebar.slider("Asteroid Diameter (km)", 0.1, 10.0, 1.0)
            velocity = st.sidebar.slider("Impact Velocity (km/s)", 5.0, 50.0, 20.0)
            density = st.sidebar.slider("Density (kg/m³)", 1000, 8000, 3000)

            return {
                'diameter_km': diameter,
                'velocity_km_s': velocity,
                'density_kg_m3': density
            }

        elif event_type == 'pandemic':
            r0 = st.sidebar.slider("R₀ (Basic Reproduction Number)", 1.0, 10.0, 2.5)
            mortality = st.sidebar.slider("Mortality Rate", 0.001, 0.5, 0.02)

            return {
                'r0': r0,
                'mortality_rate': mortality
            }

        # Add more event types as needed

    return {}
