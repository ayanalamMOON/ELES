"""
Export and rendering utilities for E.L.E.S. visualizations.

This module provides tools for exporting visualizations to various formats
and creating publication-ready reports.
"""

import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Union
import os
from pathlib import Path
import json
from datetime import datetime


def export_plots(figures: Union[List[plt.Figure], List[go.Figure]],
                output_dir: str = "exports",
                formats: List[str] = ['png', 'pdf'],
                prefix: str = "eles_plot") -> List[str]:
    """Export multiple plots to various formats."""

    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    exported_files = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for i, fig in enumerate(figures):
        for fmt in formats:
            filename = f"{prefix}_{i:03d}_{timestamp}.{fmt}"
            filepath = os.path.join(output_dir, filename)

            try:
                if isinstance(fig, plt.Figure):
                    # Matplotlib figure
                    fig.savefig(filepath, dpi=300, bbox_inches='tight',
                               facecolor='white', edgecolor='none')
                elif isinstance(fig, go.Figure):
                    # Plotly figure
                    if fmt == 'png':
                        fig.write_image(filepath, width=1200, height=800, scale=2)
                    elif fmt == 'pdf':
                        fig.write_image(filepath, width=1200, height=800, scale=2)
                    elif fmt == 'html':
                        fig.write_html(filepath)
                    elif fmt == 'json':
                        fig.write_json(filepath)

                exported_files.append(filepath)
                print(f"Exported: {filepath}")

            except Exception as e:
                print(f"Error exporting {filepath}: {e}")

    return exported_files


def save_dashboard(dashboard_fig: go.Figure,
                  filename: str = None,
                  output_dir: str = "dashboards") -> str:
    """Save dashboard as interactive HTML file."""

    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"eles_dashboard_{timestamp}.html"

    # Ensure filename has .html extension
    if not filename.endswith('.html'):
        filename += '.html'

    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    # Add custom CSS and configuration
    config = {
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
        'toImageButtonOptions': {
            'format': 'png',
            'filename': 'eles_dashboard',
            'height': 1000,
            'width': 1400,
            'scale': 2
        }
    }

    # Custom HTML template with E.L.E.S. branding
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>E.L.E.S. Dashboard - {title}</title>
        <meta charset="utf-8" />
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .header {{
                text-align: center;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
            }}
            .dashboard-container {{
                background: white;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            .footer {{
                text-align: center;
                margin-top: 20px;
                color: #666;
                font-size: 0.9em;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🌍 E.L.E.S. - Extinction-Level Event Simulator</h1>
            <p>Interactive Dashboard - Generated on {timestamp}</p>
        </div>
        <div class="dashboard-container">
            {plot_div}
        </div>
        <div class="footer">
            <p>E.L.E.S. Dashboard | <a href="https://github.com/eles-project/eles">Project Homepage</a></p>
        </div>
    </body>
    </html>
    """

    # Generate the plot HTML
    plot_html = pio.to_html(dashboard_fig, config=config, include_plotlyjs=True, div_id="dashboard")

    # Extract just the div content
    import re
    div_match = re.search(r'<div id="dashboard".*?</div>', plot_html, re.DOTALL)
    plot_div = div_match.group() if div_match else plot_html

    # Fill template
    html_content = html_template.format(
        title=dashboard_fig.layout.title.text if dashboard_fig.layout.title else "Dashboard",
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        plot_div=plot_div
    )

    # Write to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Dashboard saved: {filepath}")
    return filepath


def create_report_plots(simulation_data: Dict[str, Any],
                       event_type: str,
                       output_dir: str = "reports") -> Dict[str, str]:
    """Create standardized report plots for a simulation."""

    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    report_files = {}

    # 1. Summary Overview Plot
    fig_summary = plt.figure(figsize=(12, 8))
    gs = fig_summary.add_gridspec(2, 3, hspace=0.3, wspace=0.3)

    # Severity gauge (text-based for matplotlib)
    ax1 = fig_summary.add_subplot(gs[0, 0])
    severity = simulation_data.get('severity', 0)
    ax1.text(0.5, 0.5, f"Severity\n{severity}/6",
             ha='center', va='center', fontsize=20, fontweight='bold')
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_title('Severity Level')

    # Casualties bar
    ax2 = fig_summary.add_subplot(gs[0, 1])
    regions = ['Local', 'Regional', 'National', 'Global']
    casualties = np.random.exponential(1000000, 4)
    ax2.bar(regions, casualties, color='red', alpha=0.7)
    ax2.set_title('Casualties by Scope')
    ax2.set_ylabel('Number of People')
    ax2.tick_params(axis='x', rotation=45)

    # Economic impact
    ax3 = fig_summary.add_subplot(gs[0, 2])
    sectors = ['Agriculture', 'Industry', 'Services', 'Infrastructure']
    impacts = np.random.uniform(10, 90, 4)
    ax3.bar(sectors, impacts, color='orange', alpha=0.7)
    ax3.set_title('Economic Impact by Sector')
    ax3.set_ylabel('Impact (%)')
    ax3.tick_params(axis='x', rotation=45)

    # Timeline
    ax4 = fig_summary.add_subplot(gs[1, :])
    days = list(range(0, 365, 30))
    severity_timeline = [6, 5, 4, 4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    ax4.plot(days, severity_timeline[:len(days)], 'o-', linewidth=2, markersize=6)
    ax4.set_title('Severity Evolution Over Time')
    ax4.set_xlabel('Days Since Event')
    ax4.set_ylabel('Severity Level')
    ax4.grid(True, alpha=0.3)

    fig_summary.suptitle(f'{event_type.title()} Impact Summary', fontsize=16, fontweight='bold')

    # Save summary plot
    summary_file = os.path.join(output_dir, f"{event_type}_summary_{timestamp}.png")
    fig_summary.savefig(summary_file, dpi=300, bbox_inches='tight')
    report_files['summary'] = summary_file
    plt.close(fig_summary)

    # 2. Geographic Impact Plot
    fig_geo = plt.figure(figsize=(10, 8))
    ax = fig_geo.add_subplot(111)

    # Create concentric circles for impact zones
    from matplotlib.patches import Circle

    center = (0, 0)
    radii = [10, 50, 150, 300, 500]  # km
    colors = ['red', 'orange', 'yellow', 'lightblue', 'lightgreen']
    labels = ['Crater', 'Severe', 'Moderate', 'Light', 'Minimal']

    for radius, color, label in zip(radii, colors, labels):
        circle = Circle(center, radius, fill=(radius == radii[0]),
                       facecolor=color, edgecolor=color, alpha=0.6, linewidth=2)
        ax.add_patch(circle)
        ax.text(radius*0.7, radius*0.7, label, fontsize=10, fontweight='bold')

    ax.set_xlim(-600, 600)
    ax.set_ylim(-600, 600)
    ax.set_aspect('equal')
    ax.set_xlabel('Distance (km)')
    ax.set_ylabel('Distance (km)')
    ax.set_title(f'{event_type.title()} Impact Zones')
    ax.grid(True, alpha=0.3)

    # Save geographic plot
    geo_file = os.path.join(output_dir, f"{event_type}_geographic_{timestamp}.png")
    fig_geo.savefig(geo_file, dpi=300, bbox_inches='tight')
    report_files['geographic'] = geo_file
    plt.close(fig_geo)

    # 3. Risk Assessment Plot
    fig_risk = plt.figure(figsize=(10, 6))
    ax = fig_risk.add_subplot(111)

    risk_categories = ['Immediate', 'Short-term', 'Medium-term', 'Long-term']
    risk_levels = np.random.uniform(2, 6, len(risk_categories))
    colors = ['red', 'orange', 'yellow', 'green']

    bars = ax.bar(risk_categories, risk_levels, color=colors, alpha=0.7)
    ax.set_title(f'{event_type.title()} Risk Assessment Timeline')
    ax.set_ylabel('Risk Level')
    ax.set_ylim(0, 6)

    # Add value labels on bars
    for bar, value in zip(bars, risk_levels):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{value:.1f}', ha='center', va='bottom', fontweight='bold')

    # Save risk plot
    risk_file = os.path.join(output_dir, f"{event_type}_risk_{timestamp}.png")
    fig_risk.savefig(risk_file, dpi=300, bbox_inches='tight')
    report_files['risk'] = risk_file
    plt.close(fig_risk)

    return report_files


def batch_export(simulation_results: List[Dict[str, Any]],
                output_dir: str = "batch_exports") -> str:
    """Export multiple simulation results in batch."""

    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create summary CSV
    summary_data = []
    for i, result in enumerate(simulation_results):
        summary_data.append({
            'simulation_id': i,
            'event_type': result.get('event_type', 'unknown'),
            'severity': result.get('severity', 0),
            'casualties': result.get('casualties', 0),
            'economic_impact': result.get('economic_impact', 0),
            'recovery_time_years': result.get('recovery_time_years', 0)
        })

    summary_df = pd.DataFrame(summary_data)
    summary_file = os.path.join(output_dir, f"simulation_summary_{timestamp}.csv")
    summary_df.to_csv(summary_file, index=False)

    # Create batch comparison plot
    fig = plt.figure(figsize=(15, 10))

    # Severity distribution
    ax1 = plt.subplot(2, 3, 1)
    severities = [r.get('severity', 0) for r in simulation_results]
    ax1.hist(severities, bins=range(1, 8), alpha=0.7, edgecolor='black')
    ax1.set_title('Severity Distribution')
    ax1.set_xlabel('Severity Level')
    ax1.set_ylabel('Count')

    # Event type distribution
    ax2 = plt.subplot(2, 3, 2)
    event_types = [r.get('event_type', 'unknown') for r in simulation_results]
    unique_events, counts = np.unique(event_types, return_counts=True)
    ax2.bar(unique_events, counts)
    ax2.set_title('Event Type Distribution')
    ax2.tick_params(axis='x', rotation=45)

    # Casualties vs Severity scatter
    ax3 = plt.subplot(2, 3, 3)
    casualties = [r.get('casualties', 0) for r in simulation_results]
    ax3.scatter(severities, casualties, alpha=0.6)
    ax3.set_title('Casualties vs Severity')
    ax3.set_xlabel('Severity Level')
    ax3.set_ylabel('Casualties')
    ax3.set_yscale('log')

    # Economic impact distribution
    ax4 = plt.subplot(2, 3, 4)
    economic_impacts = [r.get('economic_impact', 0) for r in simulation_results]
    ax4.hist(economic_impacts, bins=20, alpha=0.7, edgecolor='black')
    ax4.set_title('Economic Impact Distribution')
    ax4.set_xlabel('Economic Impact ($)')
    ax4.set_ylabel('Count')
    ax4.ticklabel_format(style='scientific', axis='x', scilimits=(0,0))

    # Recovery time vs Severity
    ax5 = plt.subplot(2, 3, 5)
    recovery_times = [r.get('recovery_time_years', 0) for r in simulation_results]
    ax5.scatter(severities, recovery_times, alpha=0.6, color='green')
    ax5.set_title('Recovery Time vs Severity')
    ax5.set_xlabel('Severity Level')
    ax5.set_ylabel('Recovery Time (years)')

    # Summary statistics
    ax6 = plt.subplot(2, 3, 6)
    ax6.axis('off')

    stats_text = f"""
    Batch Analysis Summary
    =====================
    Total Simulations: {len(simulation_results)}
    Average Severity: {np.mean(severities):.1f}
    Max Casualties: {max(casualties):,.0f}
    Total Economic Impact: ${sum(economic_impacts)/1e12:.1f}T
    Avg Recovery Time: {np.mean(recovery_times):.1f} years

    Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """

    ax6.text(0.1, 0.9, stats_text, transform=ax6.transAxes,
             fontsize=10, verticalalignment='top', fontfamily='monospace')

    plt.tight_layout()

    # Save batch comparison plot
    batch_file = os.path.join(output_dir, f"batch_comparison_{timestamp}.png")
    fig.savefig(batch_file, dpi=300, bbox_inches='tight')
    plt.close(fig)

    # Create summary report
    report_file = os.path.join(output_dir, f"batch_report_{timestamp}.json")
    report_data = {
        'timestamp': timestamp,
        'total_simulations': len(simulation_results),
        'summary_statistics': {
            'average_severity': float(np.mean(severities)),
            'max_casualties': int(max(casualties)),
            'total_economic_impact': float(sum(economic_impacts)),
            'average_recovery_time': float(np.mean(recovery_times))
        },
        'files_created': {
            'summary_csv': summary_file,
            'comparison_plot': batch_file,
            'report_json': report_file
        }
    }

    with open(report_file, 'w') as f:
        json.dump(report_data, f, indent=2)

    print(f"Batch export completed. Files saved to: {output_dir}")
    print(f"Summary: {summary_file}")
    print(f"Plot: {batch_file}")
    print(f"Report: {report_file}")

    return output_dir


def create_publication_figure(data: Dict[str, Any],
                            figure_type: str = "impact_zones",
                            style: str = "scientific") -> plt.Figure:
    """Create publication-ready figures with proper formatting."""

    # Set publication style
    if style == "scientific":
        plt.style.use('default')
        plt.rcParams.update({
            'font.size': 12,
            'axes.titlesize': 14,
            'axes.labelsize': 12,
            'xtick.labelsize': 10,
            'ytick.labelsize': 10,
            'legend.fontsize': 10,
            'figure.titlesize': 16,
            'font.family': 'serif',
            'font.serif': ['Times New Roman'],
            'text.usetex': False,  # Set to True if LaTeX is available
            'axes.linewidth': 1.2,
            'grid.alpha': 0.3
        })

    if figure_type == "impact_zones":
        fig, ax = plt.subplots(figsize=(8, 6))

        # Create professional impact zones plot
        distances = np.array([10, 50, 150, 300, 500])
        damage_percentages = np.array([100, 80, 60, 30, 10])

        ax.plot(distances, damage_percentages, 'o-', linewidth=2,
               markersize=8, color='#2E8B57', markerfacecolor='white',
               markeredgecolor='#2E8B57', markeredgewidth=2)

        ax.set_xlabel('Distance from Impact (km)')
        ax.set_ylabel('Damage Level (%)')
        ax.set_title('Asteroid Impact Damage vs Distance')
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_xlim(0, 550)
        ax.set_ylim(0, 105)

        # Add annotations
        for x, y in zip(distances, damage_percentages):
            ax.annotate(f'{y}%', (x, y), textcoords="offset points",
                       xytext=(0,10), ha='center', fontsize=9)

        return fig

    # Add more figure types as needed
    else:
        # Default figure
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.text(0.5, 0.5, f'Figure type "{figure_type}" not implemented',
                ha='center', va='center', transform=ax.transAxes)
        return fig
