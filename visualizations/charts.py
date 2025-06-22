import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from typing import Dict, Any, List, Optional
from matplotlib.figure import Figure
from matplotlib.patches import Circle
import plotly.express as px
import plotly.graph_objects as go


def plot_severity_distribution(results: List[Dict[str, Any]]) -> Figure:
    """Plot distribution of severity levels across multiple simulations."""
    severities = [r.get('severity', 0) for r in results]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(severities, bins=range(1, 8), alpha=0.7, edgecolor='black')
    ax.set_xlabel('Severity Level')
    ax.set_ylabel('Number of Simulations')
    ax.set_title('Distribution of Extinction Event Severity Levels')
    ax.set_xticks(range(1, 7))
    ax.grid(True, alpha=0.3)

    return fig


def plot_energy_comparison(energies: Dict[str, float]) -> Figure:
    """Plot energy comparison chart."""
    fig, ax = plt.subplots(figsize=(12, 8))

    names = list(energies.keys())
    values = list(energies.values())

    bars = ax.bar(names, values)
    ax.set_yscale('log')
    ax.set_ylabel('Energy (Joules)')
    ax.set_title('Impact Energy Comparison')
    ax.tick_params(axis='x', rotation=45)

    # Add value labels on bars
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{value:.1e}', ha='center', va='bottom')

    plt.tight_layout()
    return fig


def plot_damage_zones(crater_diameter: float, blast_radii: Dict[str, float]) -> Figure:
    """Plot concentric damage zones."""
    fig, ax = plt.subplots(figsize=(10, 10))

    # Create circles for damage zones
    center = (0, 0)

    # Crater
    crater_circle = Circle(center, crater_diameter/2, color='red', alpha=0.8, label='Crater')
    ax.add_patch(crater_circle)

    # Blast zones
    colors = ['orange', 'yellow', 'lightblue']
    labels = ['Severe Blast', 'Moderate Blast', 'Light Damage']

    for i, (zone, radius) in enumerate(blast_radii.items()):
        if i < len(colors):
            circle = Circle(center, radius, fill=False,
                           edgecolor=colors[i], linewidth=3,
                           label=f'{zone}: {radius:.1f} km')
            ax.add_patch(circle)

    # Set equal aspect ratio and limits
    max_radius = max(blast_radii.values()) if blast_radii else crater_diameter
    ax.set_xlim(-max_radius*1.1, max_radius*1.1)
    ax.set_ylim(-max_radius*1.1, max_radius*1.1)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_xlabel('Distance (km)')
    ax.set_ylabel('Distance (km)')
    ax.set_title('Impact Damage Zones')

    return fig


def plot_epidemic_curve(days: List[int], infected: List[int],
                       deaths: Optional[List[int]] = None) -> Figure:
    """Plot epidemic curve."""
    fig, ax = plt.subplots(figsize=(12, 8))

    ax.plot(days, infected, 'b-', linewidth=2, label='Active Infections')

    if deaths:
        ax.plot(days, deaths, 'r-', linewidth=2, label='Cumulative Deaths')

    ax.set_xlabel('Days since outbreak')
    ax.set_ylabel('Number of people')
    ax.set_title('Epidemic Progression')
    ax.legend()
    ax.grid(True, alpha=0.3)

    return fig


def plot_temperature_timeline(years: List[int], temperature: List[float]) -> Figure:
    """Plot temperature change over time."""
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(years, temperature, 'r-', linewidth=2)
    ax.axhline(y=0, color='k', linestyle='--', alpha=0.5)
    ax.set_xlabel('Years')
    ax.set_ylabel('Temperature Change (°C)')
    ax.set_title('Climate Change Timeline')
    ax.grid(True, alpha=0.3)

    # Highlight dangerous thresholds
    ax.axhline(y=1.5, color='orange', linestyle=':', alpha=0.7, label='1.5°C threshold')
    ax.axhline(y=2.0, color='red', linestyle=':', alpha=0.7, label='2.0°C threshold')
    ax.legend()

    return fig


def create_risk_heatmap(risk_matrix: Dict[str, Dict[str, float]]) -> Figure:
    """Create a risk assessment heatmap."""
    # Convert dict to matrix format
    categories = list(risk_matrix.keys())
    scenarios = list(next(iter(risk_matrix.values())).keys())

    matrix = np.array([[risk_matrix[cat][scen] for scen in scenarios]
                      for cat in categories])

    fig, ax = plt.subplots(figsize=(10, 8))

    sns.heatmap(matrix,
                xticklabels=scenarios,
                yticklabels=categories,
                annot=True,
                cmap='YlOrRd',
                cbar_kws={'label': 'Risk Level'},
                ax=ax)

    ax.set_title('Multi-Scenario Risk Assessment')
    plt.tight_layout()

    return fig


def plot_cascading_effects(effects_timeline: Dict[str, List[float]]) -> Figure:
    """Plot cascading effects over time."""
    fig, ax = plt.subplots(figsize=(14, 8))

    colors = plt.get_cmap('tab10')(np.linspace(0, 1, len(effects_timeline)))

    for i, (effect, values) in enumerate(effects_timeline.items()):
        time_points = list(range(len(values)))
        ax.plot(time_points, values, color=colors[i],
               linewidth=2, label=effect, marker='o')

    ax.set_xlabel('Time Period')
    ax.set_ylabel('Effect Magnitude')
    ax.set_title('Cascading Effects Timeline')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def create_interactive_impact_map(impact_data: Dict[str, Any]) -> go.Figure:
    """Create interactive map showing impact zones."""
    # This would require geographical data - placeholder implementation
    fig = go.Figure()

    # Add crater location (example coordinates)
    crater_lat, crater_lon = impact_data.get('latitude', 0), impact_data.get('longitude', 0)
    crater_radius = impact_data.get('crater_diameter_km', 1) / 2

    # Add crater
    fig.add_trace(go.Scattermapbox(
        lat=[crater_lat],
        lon=[crater_lon],
        mode='markers',
        marker=dict(size=crater_radius*2, color='red'),
        name='Crater',
        text=f"Crater: {crater_radius*2:.1f} km diameter"
    ))

    # Add blast zones
    blast_radius = impact_data.get('blast_radius_severe_km', 10)
    fig.add_trace(go.Scattermapbox(
        lat=[crater_lat],
        lon=[crater_lon],
        mode='markers',
        marker=dict(size=blast_radius*2, color='orange', opacity=0.5),
        name='Blast Zone',
        text=f"Severe damage: {blast_radius:.1f} km radius"
    ))

    fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=crater_lat, lon=crater_lon),
            zoom=6
        ),
        title="Impact Zone Visualization"
    )

    return fig


def plot_result(result):
    """Legacy function for compatibility."""
    fig, ax = plt.subplots()
    ax.bar(['Impacted Area'], [result.impacted_area])
    return fig


def plot_timeline_comparison(scenarios: List[Dict[str, Any]]) -> Figure:
    """Plot timeline comparison between multiple scenarios."""
    fig, ax = plt.subplots(figsize=(12, 8))

    for i, scenario in enumerate(scenarios):
        name = scenario.get('name', f'Scenario {i+1}')
        timeline = scenario.get('timeline', {})

        if timeline:
            times = list(timeline.keys())
            severities = [timeline[t].get('severity', 0) for t in times]

            ax.plot(times, severities, 'o-', linewidth=2, label=name)

    ax.set_xlabel('Time (days)')
    ax.set_ylabel('Severity Level')
    ax.set_title('Timeline Comparison Across Scenarios')
    ax.legend()
    ax.grid(True, alpha=0.3)

    return fig


def plot_risk_assessment(risk_data: Dict[str, Any]) -> Figure:
    """Plot comprehensive risk assessment visualization."""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

    # Risk by category
    categories = risk_data.get('categories', ['Environmental', 'Social', 'Economic', 'Political'])
    risk_levels = risk_data.get('risk_levels', [3.5, 4.2, 3.8, 2.9])

    bars = ax1.bar(categories, risk_levels, color=['green', 'blue', 'orange', 'red'], alpha=0.7)
    ax1.set_title('Risk Assessment by Category')
    ax1.set_ylabel('Risk Level (1-5)')
    ax1.set_ylim(0, 5)

    # Add value labels
    for bar, value in zip(bars, risk_levels):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{value:.1f}', ha='center', va='bottom')

    # Risk evolution over time
    time_periods = ['Immediate', 'Short-term', 'Medium-term', 'Long-term']
    risk_evolution = risk_data.get('evolution', [4.5, 3.8, 3.2, 2.5])

    ax2.plot(time_periods, risk_evolution, 'ro-', linewidth=3, markersize=8)
    ax2.set_title('Risk Evolution Over Time')
    ax2.set_ylabel('Risk Level')
    ax2.grid(True, alpha=0.3)
    ax2.tick_params(axis='x', rotation=45)

    # Risk probability distribution
    probabilities = risk_data.get('probabilities', [0.1, 0.2, 0.3, 0.25, 0.15])
    severity_levels = range(1, 6)

    ax3.bar(severity_levels, probabilities, color='skyblue', alpha=0.7, edgecolor='black')
    ax3.set_title('Risk Probability Distribution')
    ax3.set_xlabel('Severity Level')
    ax3.set_ylabel('Probability')
    ax3.set_xticks(severity_levels)

    # Risk impact matrix
    likelihood = ['Very Low', 'Low', 'Medium', 'High', 'Very High']
    impact = ['Minor', 'Moderate', 'Major', 'Severe', 'Catastrophic']
    risk_matrix = np.random.randint(1, 6, (5, 5))

    im = ax4.imshow(risk_matrix, cmap='Reds', aspect='auto')
    ax4.set_title('Risk Impact Matrix')
    ax4.set_xlabel('Impact')
    ax4.set_ylabel('Likelihood')
    ax4.set_xticks(range(5))
    ax4.set_xticklabels(impact, rotation=45)
    ax4.set_yticks(range(5))
    ax4.set_yticklabels(likelihood)

    # Add text annotations
    for i in range(5):
        for j in range(5):
            ax4.text(j, i, str(risk_matrix[i, j]), ha='center', va='center')

    plt.tight_layout()
    return fig


def plot_recovery_phases(recovery_data: Dict[str, Any]) -> Figure:
    """Plot recovery phases and milestones."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    # Recovery progress over time
    months = recovery_data.get('months', list(range(0, 121, 6)))  # 10 years
    overall_progress = recovery_data.get('overall_progress',
                                       [0, 5, 15, 30, 45, 55, 65, 72, 78, 83, 87, 90, 92, 94, 95, 96, 97, 98, 99, 99.5, 100])

    ax1.plot(months, overall_progress[:len(months)], 'g-', linewidth=3, label='Overall Recovery')

    # Individual sector recovery
    sectors = recovery_data.get('sectors', ['Infrastructure', 'Economy', 'Population', 'Environment'])
    colors = ['blue', 'orange', 'red', 'brown']

    for sector, color in zip(sectors, colors):
        # Generate sector-specific recovery curve
        sector_progress = []
        for month in months:
            if sector == 'Infrastructure':
                progress = min(100, month * 1.2 + np.random.normal(0, 5))
            elif sector == 'Economy':
                progress = min(100, month * 0.8 + np.random.normal(0, 3))
            elif sector == 'Population':
                progress = min(100, month * 0.6 + np.random.normal(0, 2))
            else:  # Environment
                progress = min(100, month * 0.4 + np.random.normal(0, 1))

            sector_progress.append(max(0, progress))

        ax1.plot(months, sector_progress, '--', linewidth=2, color=color, label=sector, alpha=0.7)

    ax1.set_xlabel('Months Since Event')
    ax1.set_ylabel('Recovery Progress (%)')
    ax1.set_title('Recovery Progress by Sector')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 105)

    # Recovery milestones
    milestones = recovery_data.get('milestones', [
        {'month': 1, 'milestone': 'Emergency Response', 'completion': 90},
        {'month': 6, 'milestone': 'Basic Services Restored', 'completion': 70},
        {'month': 12, 'milestone': 'Infrastructure Rebuilt', 'completion': 50},
        {'month': 24, 'milestone': 'Economic Recovery', 'completion': 60},
        {'month': 60, 'milestone': 'Full Normalization', 'completion': 80}
    ])

    milestone_months = [m['month'] for m in milestones]
    milestone_names = [m['milestone'] for m in milestones]
    completion_rates = [m['completion'] for m in milestones]

    bars = ax2.barh(milestone_names, completion_rates, color='lightcoral', alpha=0.7, edgecolor='black')
    ax2.set_xlabel('Completion Rate (%)')
    ax2.set_title('Recovery Milestones')
    ax2.set_xlim(0, 100)

    # Add completion percentage labels
    for bar, rate in zip(bars, completion_rates):
        width = bar.get_width()
        ax2.text(width + 1, bar.get_y() + bar.get_height()/2,
                f'{rate}%', ha='left', va='center')

    plt.tight_layout()
    return fig


def plot_parameter_sensitivity(sensitivity_data: Dict[str, Any]) -> Figure:
    """Plot parameter sensitivity analysis."""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))

    parameters = sensitivity_data.get('parameters', ['Diameter', 'Velocity', 'Density', 'Angle'])

    for i, param in enumerate(parameters):
        row = i // 2
        col = i % 2
        ax = axes[row, col]

        # Generate sensitivity data
        param_values = np.linspace(0.5, 2.0, 20)  # Normalized parameter values
        base_severity = 3.5

        # Different sensitivity patterns for different parameters
        if param == 'Diameter':
            sensitivities = base_severity * param_values**1.5
        elif param == 'Velocity':
            sensitivities = base_severity * param_values**1.2
        elif param == 'Density':
            sensitivities = base_severity * param_values**0.8
        else:  # Angle
            sensitivities = base_severity * (1 + 0.3 * np.sin(param_values * np.pi))

        # Add some noise
        sensitivities += np.random.normal(0, 0.1, len(sensitivities))
        sensitivities = np.clip(sensitivities, 1, 6)

        ax.plot(param_values, sensitivities, 'o-', linewidth=2, markersize=6)
        ax.set_xlabel(f'{param} (Normalized)')
        ax.set_ylabel('Severity Level')
        ax.set_title(f'Sensitivity to {param}')
        ax.grid(True, alpha=0.3)
        ax.set_ylim(1, 6)

        # Add baseline reference
        ax.axhline(y=base_severity, color='red', linestyle='--', alpha=0.7, label='Baseline')
        ax.axvline(x=1.0, color='gray', linestyle='--', alpha=0.7, label='Nominal Value')
        ax.legend()

    plt.suptitle('Parameter Sensitivity Analysis', fontsize=16, fontweight='bold')
    plt.tight_layout()
    return fig


def create_comprehensive_summary_chart(simulation_data: Dict[str, Any]) -> Figure:
    """Create comprehensive summary chart with multiple panels."""
    fig = plt.figure(figsize=(16, 12))
    gs = fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)

    # Panel 1: Severity gauge (text-based)
    ax1 = fig.add_subplot(gs[0, 0])
    severity = simulation_data.get('severity', 3)
    colors = ['green', 'yellow', 'orange', 'red', 'darkred', 'black']
    color = colors[min(severity-1, 5)]

    ax1.text(0.5, 0.5, f"{severity}", ha='center', va='center',
             fontsize=48, fontweight='bold', color=color)
    ax1.text(0.5, 0.2, "Severity Level", ha='center', va='center', fontsize=12)
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_title('Severity Assessment')

    # Panel 2: Casualties breakdown
    ax2 = fig.add_subplot(gs[0, 1])
    casualty_types = ['Immediate', 'Short-term', 'Long-term']
    casualties = simulation_data.get('casualties_breakdown', [100000, 200000, 150000])

    wedges, texts, *autotexts = ax2.pie(casualties, labels=casualty_types, autopct='%1.1f%%',
                                      startangle=140)
    ax2.set_title('Casualty Distribution')

    # Panel 3: Economic sectors impact
    ax3 = fig.add_subplot(gs[0, 2])
    sectors = ['Agriculture', 'Industry', 'Services', 'Energy']
    impacts = simulation_data.get('sector_impacts', [80, 60, 40, 70])

    bars = ax3.bar(sectors, impacts, color=['green', 'blue', 'purple', 'orange'], alpha=0.7)
    ax3.set_title('Economic Impact by Sector')
    ax3.set_ylabel('Impact (%)')
    ax3.tick_params(axis='x', rotation=45)

    # Panel 4: Geographic spread
    ax4 = fig.add_subplot(gs[0, 3])
    distances = [10, 50, 150, 300, 500]
    affected_pop = [100, 80, 60, 30, 10]  # Percentage affected

    ax4.plot(distances, affected_pop, 'ro-', linewidth=2, markersize=6)
    ax4.set_title('Population Impact vs Distance')
    ax4.set_xlabel('Distance (km)')
    ax4.set_ylabel('Population Affected (%)')
    ax4.set_xscale('log')
    ax4.grid(True, alpha=0.3)

    # Panel 5: Timeline (spans 2 columns)
    ax5 = fig.add_subplot(gs[1, :2])
    timeline_days = [0, 1, 7, 30, 90, 365, 1825]  # 0 to 5 years
    timeline_labels = ['Impact', '1 Day', '1 Week', '1 Month', '3 Months', '1 Year', '5 Years']
    severity_timeline = [6, 5, 4, 3, 3, 2, 1]

    ax5.plot(timeline_days, severity_timeline, 'o-', linewidth=3, markersize=8, color='red')
    ax5.set_title('Severity Evolution Timeline')
    ax5.set_xlabel('Time Since Event')
    ax5.set_ylabel('Severity Level')
    ax5.set_xscale('log')
    ax5.set_xticks(timeline_days)
    ax5.set_xticklabels(timeline_labels, rotation=45)
    ax5.grid(True, alpha=0.3)
    ax5.set_ylim(0, 6.5)

    # Panel 6: Resource availability
    ax6 = fig.add_subplot(gs[1, 2:])
    resources = ['Food', 'Water', 'Energy', 'Medical', 'Transport', 'Communication']
    availability = simulation_data.get('resource_availability', [60, 80, 40, 70, 30, 50])

    colors_res = ['green' if x > 70 else 'orange' if x > 40 else 'red' for x in availability]
    bars_res = ax6.barh(resources, availability, color=colors_res, alpha=0.7)
    ax6.set_title('Resource Availability')
    ax6.set_xlabel('Availability (%)')
    ax6.set_xlim(0, 100)

    # Add percentage labels
    for bar, avail in zip(bars_res, availability):
        width = bar.get_width()
        ax6.text(width + 1, bar.get_y() + bar.get_height()/2,
                f'{avail}%', ha='left', va='center')

    # Panel 7: Recovery projection
    ax7 = fig.add_subplot(gs[2, :2])
    recovery_years = list(range(0, 21))  # 20 years
    recovery_progress = [0]
    for year in recovery_years[1:]:
        # Exponential recovery model
        progress = 100 * (1 - np.exp(-year/5))
        recovery_progress.append(min(100, progress))

    ax7.plot(recovery_years, recovery_progress, 'g-', linewidth=3)
    ax7.fill_between(recovery_years, recovery_progress, alpha=0.3, color='green')
    ax7.set_title('Recovery Projection')
    ax7.set_xlabel('Years Since Event')
    ax7.set_ylabel('Recovery Progress (%)')
    ax7.grid(True, alpha=0.3)
    ax7.set_ylim(0, 105)

    # Panel 8: Risk factors radar
    ax8 = fig.add_subplot(gs[2, 2:], projection='polar')
    risk_categories = ['Environmental', 'Social', 'Economic', 'Political', 'Technical']
    risk_values = simulation_data.get('risk_values', [4, 3, 5, 2, 3])

    # Add first value at end to close the polygon
    angles = np.linspace(0, 2*np.pi, len(risk_categories), endpoint=False).tolist()
    risk_values_plot = risk_values + [risk_values[0]]
    angles += [angles[0]]

    ax8.plot(angles, risk_values_plot, 'o-', linewidth=2, color='red')
    ax8.fill(angles, risk_values_plot, alpha=0.25, color='red')
    ax8.set_xticks(angles[:-1])
    ax8.set_xticklabels(risk_categories)
    ax8.set_ylim(0, 6)
    ax8.set_title('Risk Factor Assessment')
    ax8.grid(True)

    plt.suptitle(f'{simulation_data.get("event_type", "Event").title()} Impact Summary',
                 fontsize=18, fontweight='bold')

    return fig
