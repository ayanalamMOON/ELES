"""
Geographic and risk heatmap visualization tools for E.L.E.S.

This module provides comprehensive heatmap visualization capabilities
for displaying spatial and temporal risk patterns.
"""

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List, Tuple, Optional, Union


def plot_geographic_heatmap(impact_data: Dict[str, Any],
                          grid_resolution: int = 50) -> plt.Figure:
    """Create geographic heatmap of impact intensity."""

    # Generate sample geographic grid if no data provided
    if 'geographic_grid' not in impact_data:
        # Create sample impact data centered around impact point
        impact_center = impact_data.get('impact_location', (40.0, -100.0))
        lat_center, lon_center = impact_center

        # Create coordinate grid
        lat_range = np.linspace(lat_center - 10, lat_center + 10, grid_resolution)
        lon_range = np.linspace(lon_center - 15, lon_center + 15, grid_resolution)

        lat_grid, lon_grid = np.meshgrid(lat_range, lon_range)

        # Calculate distance from impact center
        distance = np.sqrt((lat_grid - lat_center)**2 + (lon_grid - lon_center)**2)

        # Create impact intensity based on distance (inverse relationship)
        max_impact_radius = impact_data.get('max_impact_radius', 10.0)
        intensity = np.exp(-distance / max_impact_radius) * 100

        # Add some randomness
        intensity += np.random.normal(0, 5, intensity.shape)
        intensity = np.clip(intensity, 0, 100)

    else:
        # Use provided data
        lat_grid = impact_data['geographic_grid']['lat']
        lon_grid = impact_data['geographic_grid']['lon']
        intensity = impact_data['geographic_grid']['intensity']

    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 8))

    # Create heatmap
    heatmap = ax.contourf(lon_grid, lat_grid, intensity, levels=20, cmap='Reds', alpha=0.8)

    # Add contour lines
    contours = ax.contour(lon_grid, lat_grid, intensity, levels=10, colors='black', alpha=0.3, linewidths=0.5)
    ax.clabel(contours, inline=True, fontsize=8, fmt='%1.0f')

    # Add colorbar
    cbar = plt.colorbar(heatmap, ax=ax, shrink=0.8)
    cbar.set_label('Impact Intensity (%)', rotation=270, labelpad=20)

    # Formatting
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('Geographic Impact Intensity Heatmap')
    ax.grid(True, alpha=0.3)

    # Add impact center marker
    if 'impact_location' in impact_data:
        lat_center, lon_center = impact_data['impact_location']
        ax.plot(lon_center, lat_center, 'k*', markersize=20, markeredgecolor='white',
                markeredgewidth=2, label='Impact Center')
        ax.legend()

    plt.tight_layout()
    return fig


def plot_risk_heatmap(risk_data: Dict[str, Any]) -> plt.Figure:
    """Create risk assessment heatmap across different factors."""

    # Define risk factors and categories
    if 'risk_matrix' not in risk_data:
        # Create sample risk matrix
        risk_factors = ['Population Density', 'Infrastructure', 'Economic Activity',
                       'Emergency Preparedness', 'Geographic Vulnerability']
        risk_categories = ['Immediate', 'Short-term', 'Medium-term', 'Long-term']

        # Generate sample risk levels (1-5 scale)
        risk_matrix = np.random.uniform(1, 5, (len(risk_factors), len(risk_categories)))

        # Add some realistic patterns
        risk_matrix[0, 0] = 4.5  # Population density has high immediate risk
        risk_matrix[3, :] = np.array([2.0, 3.0, 3.5, 4.0])  # Emergency preparedness improves over time

    else:
        risk_matrix = np.array(risk_data['risk_matrix'])
        risk_factors = risk_data.get('risk_factors', [f'Factor {i+1}' for i in range(risk_matrix.shape[0])])
        risk_categories = risk_data.get('risk_categories', [f'Category {i+1}' for i in range(risk_matrix.shape[1])])

    # Create the heatmap
    fig, ax = plt.subplots(figsize=(10, 8))

    # Use seaborn heatmap for better formatting
    sns.heatmap(risk_matrix,
                xticklabels=risk_categories,
                yticklabels=risk_factors,
                annot=True,
                fmt='.1f',
                cmap='RdYlBu_r',
                cbar_kws={'label': 'Risk Level (1-5)'},
                ax=ax)

    ax.set_title('Risk Assessment Heatmap', fontsize=16, fontweight='bold')
    ax.set_xlabel('Time Categories', fontsize=12)
    ax.set_ylabel('Risk Factors', fontsize=12)

    # Rotate labels for better readability
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)

    plt.tight_layout()
    return fig


def plot_population_density_heatmap(population_data: Dict[str, Any]) -> go.Figure:
    """Create interactive population density heatmap using Plotly."""

    # Generate sample population data if none provided
    if 'population_grid' not in population_data:
        # Create sample population density grid
        grid_size = 50
        x_coords = np.linspace(-10, 10, grid_size)
        y_coords = np.linspace(-10, 10, grid_size)

        X, Y = np.meshgrid(x_coords, y_coords)

        # Create realistic population density pattern
        # Higher density near center, with some random urban centers
        center_density = 1000 * np.exp(-(X**2 + Y**2) / 20)

        # Add some random urban centers
        for _ in range(5):
            center_x = np.random.uniform(-8, 8)
            center_y = np.random.uniform(-8, 8)
            urban_density = 500 * np.exp(-((X - center_x)**2 + (Y - center_y)**2) / 5)
            center_density += urban_density

        # Add noise and ensure non-negative
        population_density = center_density + np.random.exponential(50, (grid_size, grid_size))
        population_density = np.maximum(population_density, 10)  # Minimum density

    else:
        X = population_data['population_grid']['x']
        Y = population_data['population_grid']['y']
        population_density = population_data['population_grid']['density']

    # Create Plotly heatmap
    fig = go.Figure(data=go.Heatmap(
        z=population_density,
        x=X[0, :] if X.ndim == 2 else X,
        y=Y[:, 0] if Y.ndim == 2 else Y,
        colorscale='Viridis',
        colorbar=dict(title="Population Density<br>(people/km²)"),
        hoverontemplate='<b>Population Density</b><br>' +
                       'X: %{x:.1f}<br>' +
                       'Y: %{y:.1f}<br>' +
                       'Density: %{z:.0f} people/km²<extra></extra>'
    ))

    fig.update_layout(
        title='Population Density Heatmap',
        xaxis_title='Longitude Offset (degrees)',
        yaxis_title='Latitude Offset (degrees)',
        width=800,
        height=600
    )

    return fig


def plot_correlation_heatmap(correlation_data: pd.DataFrame) -> plt.Figure:
    """Create correlation heatmap for multiple variables."""

    # Generate sample correlation data if none provided
    if correlation_data.empty:
        # Create sample dataset with extinction event variables
        variables = ['Severity', 'Casualties', 'Economic_Impact', 'Recovery_Time',
                    'Population_Density', 'Infrastructure_Quality', 'Emergency_Preparedness']

        # Generate synthetic correlated data
        n_samples = 100
        data = np.random.multivariate_normal(
            mean=np.zeros(len(variables)),
            cov=np.random.rand(len(variables), len(variables)) * 0.5 + np.eye(len(variables)) * 0.5,
            size=n_samples
        )

        correlation_data = pd.DataFrame(data, columns=variables)

    # Calculate correlation matrix
    correlation_matrix = correlation_data.corr()

    # Create the heatmap
    fig, ax = plt.subplots(figsize=(10, 8))

    # Create mask for upper triangle (optional)
    mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))

    # Generate heatmap
    sns.heatmap(correlation_matrix,
                mask=mask,
                annot=True,
                cmap='RdBu_r',
                vmin=-1, vmax=1,
                center=0,
                square=True,
                fmt='.2f',
                cbar_kws={'label': 'Correlation Coefficient'},
                ax=ax)

    ax.set_title('Variable Correlation Heatmap', fontsize=16, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)

    plt.tight_layout()
    return fig


def plot_temporal_heatmap(temporal_data: Dict[str, Any]) -> go.Figure:
    """Create temporal heatmap showing evolution over time."""

    # Generate sample temporal data if none provided
    if 'temporal_matrix' not in temporal_data:
        # Create sample time series data
        time_points = 365  # Days
        regions = ['Region A', 'Region B', 'Region C', 'Region D', 'Region E']

        # Generate synthetic impact evolution data
        impact_matrix = np.zeros((len(regions), time_points))

        for i, region in enumerate(regions):
            # Different regions have different impact patterns
            peak_day = np.random.randint(1, 30)  # Peak impact within first month
            decay_rate = np.random.uniform(0.01, 0.05)

            for day in range(time_points):
                if day <= peak_day:
                    # Rising to peak
                    impact = (day / peak_day) * np.random.uniform(80, 100)
                else:
                    # Exponential decay
                    peak_impact = np.random.uniform(80, 100)
                    impact = peak_impact * np.exp(-decay_rate * (day - peak_day))

                # Add some noise
                impact += np.random.normal(0, 2)
                impact_matrix[i, day] = max(0, impact)

        days = list(range(1, time_points + 1))

    else:
        impact_matrix = np.array(temporal_data['temporal_matrix'])
        regions = temporal_data.get('regions', [f'Region {i+1}' for i in range(impact_matrix.shape[0])])
        days = temporal_data.get('time_points', list(range(1, impact_matrix.shape[1] + 1)))

    # Create Plotly heatmap
    fig = go.Figure(data=go.Heatmap(
        z=impact_matrix,
        x=days,
        y=regions,
        colorscale='Reds',
        colorbar=dict(title="Impact Intensity"),
        hoverontemplate='<b>%{y}</b><br>' +
                       'Day: %{x}<br>' +
                       'Impact: %{z:.1f}%<extra></extra>'
    ))

    fig.update_layout(
        title='Temporal Impact Evolution Heatmap',
        xaxis_title='Days Since Event',
        yaxis_title='Affected Regions',
        width=1000,
        height=500
    )

    # Add annotation for peak impact period
    fig.add_vline(x=30, line_dash="dash", line_color="yellow",
                  annotation_text="Peak Impact Period")

    return fig


def create_multi_layer_heatmap(multi_data: Dict[str, Any]) -> plt.Figure:
    """Create multi-layer heatmap with different data overlays."""

    fig, axes = plt.subplots(2, 2, figsize=(15, 12))

    # Layer 1: Population Density
    ax1 = axes[0, 0]
    pop_data = np.random.exponential(100, (20, 20))
    im1 = ax1.imshow(pop_data, cmap='Blues', aspect='auto')
    ax1.set_title('Population Density')
    plt.colorbar(im1, ax=ax1, shrink=0.8)

    # Layer 2: Infrastructure Quality
    ax2 = axes[0, 1]
    infra_data = np.random.uniform(0, 100, (20, 20))
    im2 = ax2.imshow(infra_data, cmap='Greens', aspect='auto')
    ax2.set_title('Infrastructure Quality')
    plt.colorbar(im2, ax=ax2, shrink=0.8)

    # Layer 3: Impact Intensity
    ax3 = axes[1, 0]
    impact_data = np.random.exponential(50, (20, 20))
    im3 = ax3.imshow(impact_data, cmap='Reds', aspect='auto')
    ax3.set_title('Impact Intensity')
    plt.colorbar(im3, ax=ax3, shrink=0.8)

    # Layer 4: Combined Risk
    ax4 = axes[1, 1]
    # Combine all layers into risk assessment
    combined_risk = (pop_data * 0.3 + (100 - infra_data) * 0.3 + impact_data * 0.4)
    im4 = ax4.imshow(combined_risk, cmap='RdYlBu_r', aspect='auto')
    ax4.set_title('Combined Risk Assessment')
    plt.colorbar(im4, ax=ax4, shrink=0.8)

    plt.suptitle('Multi-Layer Risk Analysis Heatmaps', fontsize=16, fontweight='bold')
    plt.tight_layout()

    return fig


def plot_interactive_risk_heatmap(risk_data: Dict[str, Any]) -> go.Figure:
    """Create interactive risk heatmap with drill-down capability."""

    # Generate sample risk data
    if 'interactive_risk_data' not in risk_data:
        # Create hierarchical risk data
        sectors = ['Healthcare', 'Transportation', 'Communication', 'Energy', 'Water', 'Food']
        subsectors = {
            'Healthcare': ['Hospitals', 'Clinics', 'Emergency Services', 'Medical Supply'],
            'Transportation': ['Roads', 'Railways', 'Airports', 'Ports'],
            'Communication': ['Internet', 'Phone', 'Broadcasting', 'Satellites'],
            'Energy': ['Power Plants', 'Grid', 'Fuel Supply', 'Renewables'],
            'Water': ['Treatment Plants', 'Distribution', 'Storage', 'Quality'],
            'Food': ['Production', 'Processing', 'Distribution', 'Storage']
        }

        # Create risk matrix
        risk_matrix = []
        sector_labels = []
        subsector_labels = []

        for sector in sectors:
            for subsector in subsectors[sector]:
                risk_values = np.random.uniform(1, 5, 4)  # 4 time periods
                risk_matrix.append(risk_values)
                sector_labels.append(sector)
                subsector_labels.append(subsector)

        risk_matrix = np.array(risk_matrix)
        time_periods = ['Immediate', 'Short-term', 'Medium-term', 'Long-term']

    else:
        risk_matrix = risk_data['interactive_risk_data']['matrix']
        sector_labels = risk_data['interactive_risk_data']['sectors']
        subsector_labels = risk_data['interactive_risk_data']['subsectors']
        time_periods = risk_data['interactive_risk_data']['time_periods']

    # Create interactive heatmap
    fig = go.Figure(data=go.Heatmap(
        z=risk_matrix,
        x=time_periods,
        y=[f"{sector}<br>{subsector}" for sector, subsector in zip(sector_labels, subsector_labels)],
        colorscale='RdYlBu_r',
        colorbar=dict(title="Risk Level"),
        hoverontemplate='<b>%{y}</b><br>' +
                       'Period: %{x}<br>' +
                       'Risk Level: %{z:.1f}<extra></extra>'
    ))

    fig.update_layout(
        title='Interactive Infrastructure Risk Assessment',
        xaxis_title='Time Period',
        yaxis_title='Infrastructure Components',
        width=800,
        height=800,
        yaxis=dict(tickmode='linear')
    )

    return fig
