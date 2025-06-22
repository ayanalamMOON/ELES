"""
Dashboard and multi-panel visualization components for E.L.E.S.

This module provides comprehensive dashboard layouts for displaying
multiple visualization components in coordinated layouts.
"""

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
import matplotlib.pyplot as plt


def create_main_dashboard(simulation_data: Dict[str, Any]) -> go.Figure:
    """Create comprehensive main dashboard with multiple panels."""

    # Create subplot layout
    fig = make_subplots(
        rows=3, cols=3,
        subplot_titles=[
            'Severity Overview', 'Population Impact', 'Economic Impact',
            'Geographic Distribution', 'Timeline', 'Risk Factors',
            'Recovery Progress', 'Resource Status', 'Comparative Analysis'
        ],
        specs=[
            [{"type": "indicator"}, {"type": "bar"}, {"type": "indicator"}],
            [{"type": "scattergeo"}, {"type": "scatter"}, {"type": "bar"}],
            [{"type": "scatter"}, {"type": "bar"}, {"type": "radar"}]
        ]
    )

    # Panel 1: Severity Overview (Gauge)
    severity = simulation_data.get('severity', 3)
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=severity,
        title={'text': "Severity Level"},
        gauge={
            'axis': {'range': [None, 6]},
            'bar': {'color': "darkred"},
            'steps': [
                {'range': [0, 2], 'color': "lightgreen"},
                {'range': [2, 4], 'color': "yellow"},
                {'range': [4, 6], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 5
            }
        }
    ), row=1, col=1)

    # Panel 2: Population Impact (Bar Chart)
    regions = ['North America', 'Europe', 'Asia', 'Africa', 'South America', 'Oceania']
    casualties = np.random.exponential(1000000, len(regions))

    fig.add_trace(go.Bar(
        x=regions,
        y=casualties,
        name='Casualties',
        marker_color='red'
    ), row=1, col=2)

    # Panel 3: Economic Impact (Indicator)
    economic_impact = simulation_data.get('economic_impact', 1000000000000)
    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=economic_impact,
        title={'text': "Economic Loss ($)"},
        delta={'reference': 0, 'valueformat': '.2s'}
    ), row=1, col=3)

    # Panel 4: Geographic Distribution (Map)
    # Sample geographic impact points
    lats = np.random.uniform(-60, 60, 20)
    lons = np.random.uniform(-180, 180, 20)
    impact_values = np.random.exponential(2, 20)

    fig.add_trace(go.Scattergeo(
        lon=lons,
        lat=lats,
        mode='markers',
        marker=dict(
            size=impact_values * 3,
            color=impact_values,
            colorscale='Reds',
            cmin=0,
            cmax=max(impact_values)
        ),
        showlegend=False
    ), row=2, col=1)

    # Panel 5: Timeline (Line Chart)
    timeline_days = list(range(0, 365, 30))
    severity_over_time = [6, 5, 4, 4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

    fig.add_trace(go.Scatter(
        x=timeline_days,
        y=severity_over_time[:len(timeline_days)],
        mode='lines+markers',
        name='Severity Over Time',
        line=dict(color='orange')
    ), row=2, col=2)

    # Panel 6: Risk Factors (Bar Chart)
    risk_factors = ['Climate', 'Infrastructure', 'Social', 'Economic', 'Political']
    risk_levels = np.random.uniform(1, 6, len(risk_factors))

    fig.add_trace(go.Bar(
        x=risk_factors,
        y=risk_levels,
        name='Risk Levels',
        marker_color='orange'
    ), row=2, col=3)

    # Panel 7: Recovery Progress (Scatter)
    recovery_months = list(range(0, 61, 6))
    recovery_progress = [0, 10, 25, 45, 60, 70, 78, 85, 90, 94, 97]

    fig.add_trace(go.Scatter(
        x=recovery_months,
        y=recovery_progress[:len(recovery_months)],
        mode='lines+markers',
        name='Recovery Progress (%)',
        line=dict(color='green')
    ), row=3, col=1)

    # Panel 8: Resource Status (Bar Chart)
    resources = ['Food', 'Water', 'Energy', 'Medical', 'Transport']
    availability = [75, 60, 45, 80, 35]

    fig.add_trace(go.Bar(
        x=resources,
        y=availability,
        name='Resource Availability (%)',
        marker_color=['green' if x > 60 else 'orange' if x > 30 else 'red' for x in availability]
    ), row=3, col=2)

    # Panel 9: Comparative Analysis (Radar Chart)
    categories = ['Severity', 'Speed', 'Geographic Scope', 'Duration', 'Recovery Difficulty']
    current_values = [4, 3, 5, 4, 3]

    fig.add_trace(go.Scatterpolar(
        r=current_values,
        theta=categories,
        fill='toself',
        name='Current Event'
    ), row=3, col=3)

    # Update layout
    fig.update_layout(
        title_text="E.L.E.S. Comprehensive Dashboard",
        height=1000,
        showlegend=False
    )

    # Update geo subplot
    fig.update_geos(
        projection_type="natural earth",
        showland=True,
        landcolor="lightgray"
    )

    return fig


def create_event_dashboard(event_type: str, event_data: Dict[str, Any]) -> go.Figure:
    """Create event-specific dashboard."""

    if event_type == 'asteroid':
        return _create_asteroid_dashboard(event_data)
    elif event_type == 'pandemic':
        return _create_pandemic_dashboard(event_data)
    elif event_type == 'supervolcano':
        return _create_supervolcano_dashboard(event_data)
    else:
        return _create_generic_event_dashboard(event_type, event_data)


def _create_asteroid_dashboard(asteroid_data: Dict[str, Any]) -> go.Figure:
    """Create asteroid-specific dashboard."""

    fig = make_subplots(
        rows=2, cols=3,
        subplot_titles=[
            'Impact Energy', 'Damage Zones', 'Casualty Distribution',
            'Atmospheric Effects', 'Economic Impact by Sector', 'Recovery Timeline'
        ],
        specs=[
            [{"type": "indicator"}, {"type": "scatter"}, {"type": "bar"}],
            [{"type": "bar"}, {"type": "pie"}, {"type": "scatter"}]
        ]
    )

    # Impact Energy Gauge
    impact_energy = asteroid_data.get('impact_energy', 1e21)
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=np.log10(impact_energy),
        title={'text': "Impact Energy (log₁₀ J)"},
        gauge={
            'axis': {'range': [15, 25]},
            'bar': {'color': "red"},
            'steps': [
                {'range': [15, 19], 'color': "yellow"},
                {'range': [19, 22], 'color': "orange"},
                {'range': [22, 25], 'color': "red"}
            ]
        }
    ), row=1, col=1)

    # Damage Zones (Concentric circles visualization)
    distances = [0, 50, 150, 300, 500]
    damage_levels = [100, 80, 60, 30, 10]

    fig.add_trace(go.Scatter(
        x=distances,
        y=damage_levels,
        mode='lines+markers',
        name='Damage vs Distance',
        line=dict(color='red', width=3)
    ), row=1, col=2)

    # Casualty Distribution
    regions = ['Ground Zero', '50km', '150km', '300km', '500km+']
    casualties = [50000, 200000, 500000, 800000, 1000000]

    fig.add_trace(go.Bar(
        x=regions,
        y=casualties,
        name='Casualties by Zone',
        marker_color='darkred'
    ), row=1, col=3)

    # Atmospheric Effects
    effects = ['Dust Cloud', 'Temperature Drop', 'UV Reduction', 'Precipitation']
    intensity = [85, 60, 70, 40]

    fig.add_trace(go.Bar(
        x=effects,
        y=intensity,
        name='Atmospheric Effects (%)',
        marker_color='brown'
    ), row=2, col=1)

    # Economic Impact by Sector
    sectors = ['Agriculture', 'Industry', 'Services', 'Transport', 'Energy']
    impacts = [90, 70, 40, 80, 60]

    fig.add_trace(go.Pie(
        labels=sectors,
        values=impacts,
        name="Economic Impact"
    ), row=2, col=2)

    # Recovery Timeline
    years = [0, 1, 5, 10, 25, 50, 100]
    recovery = [0, 10, 30, 50, 70, 85, 95]

    fig.add_trace(go.Scatter(
        x=years,
        y=recovery,
        mode='lines+markers',
        name='Recovery Progress (%)',
        line=dict(color='green')
    ), row=2, col=3)

    fig.update_layout(
        title_text="Asteroid Impact Dashboard",
        height=700
    )

    return fig


def _create_pandemic_dashboard(pandemic_data: Dict[str, Any]) -> go.Figure:
    """Create pandemic-specific dashboard."""

    fig = make_subplots(
        rows=2, cols=3,
        subplot_titles=[
            'Infection Rate', 'Geographic Spread', 'Age Group Impact',
            'Healthcare Capacity', 'Economic Sectors', 'Intervention Timeline'
        ],
        specs=[
            [{"type": "indicator"}, {"type": "scattergeo"}, {"type": "bar"}],
            [{"type": "bar"}, {"type": "pie"}, {"type": "scatter"}]
        ]
    )

    # R₀ Value
    r0 = pandemic_data.get('r0', 2.5)
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=r0,
        title={'text': "R₀ (Reproduction Number)"},
        gauge={
            'axis': {'range': [0, 10]},
            'bar': {'color': "blue"},
            'steps': [
                {'range': [0, 1], 'color': "green"},
                {'range': [1, 3], 'color': "yellow"},
                {'range': [3, 10], 'color': "red"}
            ]
        }
    ), row=1, col=1)

    # Geographic spread would go here - simplified for now
    fig.add_trace(go.Scattergeo(
        lon=[0, 30, 100, -100],
        lat=[0, 50, 30, 40],
        mode='markers',
        marker=dict(size=[20, 15, 25, 18], color='red')
    ), row=1, col=2)

    # Continue with other panels...
    # Age group impact
    age_groups = ['0-18', '19-35', '36-50', '51-65', '65+']
    mortality_rates = [0.1, 0.2, 0.5, 2.0, 8.0]

    fig.add_trace(go.Bar(
        x=age_groups,
        y=mortality_rates,
        name='Mortality Rate (%)',
        marker_color='red'
    ), row=1, col=3)

    fig.update_layout(
        title_text="Pandemic Dashboard",
        height=700
    )

    return fig


def _create_supervolcano_dashboard(volcano_data: Dict[str, Any]) -> go.Figure:
    """Create supervolcano-specific dashboard."""

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=[
            'VEI Scale', 'Ash Dispersal', 'Climate Impact', 'Agricultural Effects'
        ]
    )

    # VEI Scale
    vei = volcano_data.get('vei', 6)
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=vei,
        title={'text': "Volcanic Explosivity Index"},
        gauge={'axis': {'range': [0, 8]}}
    ), row=1, col=1)

    # Other panels would follow similar pattern

    fig.update_layout(
        title_text="Supervolcano Dashboard",
        height=600
    )

    return fig


def _create_generic_event_dashboard(event_type: str, event_data: Dict[str, Any]) -> go.Figure:
    """Create generic event dashboard for other event types."""

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=[
            'Severity Level', 'Impact Distribution', 'Timeline', 'Recovery'
        ]
    )

    # Basic severity gauge
    severity = event_data.get('severity', 3)
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=severity,
        title={'text': f"{event_type.title()} Severity"}
    ), row=1, col=1)

    fig.update_layout(
        title_text=f"{event_type.title()} Dashboard",
        height=600
    )

    return fig


def create_comparison_dashboard(scenarios: List[Dict[str, Any]]) -> go.Figure:
    """Create dashboard comparing multiple scenarios."""

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=[
            'Severity Comparison', 'Casualty Comparison',
            'Economic Impact', 'Recovery Time'
        ]
    )

    # Extract data for comparison
    scenario_names = [s.get('name', f'Scenario {i+1}') for i, s in enumerate(scenarios)]
    severities = [s.get('severity', 0) for s in scenarios]
    casualties = [s.get('casualties', 0) for s in scenarios]
    economic_impacts = [s.get('economic_impact', 0) for s in scenarios]
    recovery_times = [s.get('recovery_time_years', 0) for s in scenarios]

    # Severity comparison
    fig.add_trace(go.Bar(
        x=scenario_names,
        y=severities,
        name='Severity',
        marker_color='red'
    ), row=1, col=1)

    # Casualty comparison
    fig.add_trace(go.Bar(
        x=scenario_names,
        y=casualties,
        name='Casualties',
        marker_color='blue'
    ), row=1, col=2)

    # Economic impact comparison
    fig.add_trace(go.Bar(
        x=scenario_names,
        y=economic_impacts,
        name='Economic Impact',
        marker_color='green'
    ), row=2, col=1)

    # Recovery time comparison
    fig.add_trace(go.Bar(
        x=scenario_names,
        y=recovery_times,
        name='Recovery Time (Years)',
        marker_color='orange'
    ), row=2, col=2)

    fig.update_layout(
        title_text="Scenario Comparison Dashboard",
        height=700,
        showlegend=False
    )

    return fig


def create_streamlit_dashboard(simulation_data: Dict[str, Any]) -> None:
    """Create Streamlit-based dashboard layout."""

    if 'st' not in globals():
        return

    st.title("🌍 E.L.E.S. Simulation Dashboard")

    # Sidebar controls
    st.sidebar.header("Dashboard Controls")
    view_mode = st.sidebar.selectbox(
        "View Mode",
        ["Overview", "Detailed Analysis", "Comparison", "Real-time Monitor"]
    )

    # Main content area
    if view_mode == "Overview":
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Severity Level",
                simulation_data.get('severity', 0),
                delta=None
            )

        with col2:
            st.metric(
                "Casualties",
                f"{simulation_data.get('casualties', 0):,}",
                delta=None
            )

        with col3:
            st.metric(
                "Economic Impact",
                f"${simulation_data.get('economic_impact', 0)/1e9:.1f}B",
                delta=None
            )

    elif view_mode == "Detailed Analysis":
        # Show detailed charts
        st.subheader("Detailed Impact Analysis")

        # Create and display main dashboard
        dashboard_fig = create_main_dashboard(simulation_data)
        st.plotly_chart(dashboard_fig, use_container_width=True)

    # Add more view modes as needed
