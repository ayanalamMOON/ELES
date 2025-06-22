"""
Comparative Analysis Visualizations for E.L.E.S.

This module provides tools for comparing multiple extinction event scenarios,
including side-by-side comparisons, scenario ranking, and sensitivity analysis.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.figure import Figure
import seaborn as sns
from typing import Dict, Any, List, Optional, Tuple, Union


def compare_scenarios_overview(scenarios: Dict[str, Dict[str, Any]],
                             metrics: List[str] = None,
                             figsize: Tuple[int, int] = (16, 12)) -> Figure:
    """Create comprehensive overview comparison of multiple scenarios."""

    if metrics is None:
        metrics = ['severity', 'casualties', 'economic_damage', 'recovery_time']

    # Generate sample data if none provided
    if not scenarios:
        scenarios = {
            'Asteroid Impact': {
                'severity': 8.5, 'casualties': 2e9,
                'economic_damage': 1e15, 'recovery_time': 50
            },
            'Supervolcano': {
                'severity': 9.2, 'casualties': 3e9,
                'economic_damage': 5e14, 'recovery_time': 100
            },
            'Pandemic': {
                'severity': 6.8, 'casualties': 5e8,
                'economic_damage': 2e13, 'recovery_time': 15
            },
            'Climate Collapse': {
                'severity': 7.5, 'casualties': 1e9,
                'economic_damage': 8e14, 'recovery_time': 200
            }
        }

    fig, axes = plt.subplots(2, 3, figsize=figsize)
    axes = axes.flatten()

    scenario_names = list(scenarios.keys())
    colors = plt.cm.Set3(np.linspace(0, 1, len(scenario_names)))

    # Plot 1: Radar chart for multi-metric comparison
    ax = axes[0]    # Prepare data for radar chart
    df = pd.DataFrame(scenarios).T
    df_normalized = df.copy()

    # Find available metrics that exist in the data
    available_metrics = [metric for metric in metrics if metric in df.columns]

    # Normalize each available metric to 0-1 scale
    for metric in available_metrics:
        min_val = df[metric].min()
        max_val = df[metric].max()
        if max_val > min_val:
            df_normalized[metric] = (df[metric] - min_val) / (max_val - min_val)
        else:
            df_normalized[metric] = 0.5

    # Create radar chart only with available metrics
    if not available_metrics:
        ax.text(0.5, 0.5, 'No metrics available for radar chart',
               ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Multi-Metric Comparison (No Data)', fontsize=14)
    else:
        angles = np.linspace(0, 2*np.pi, len(available_metrics), endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle

        for i, scenario in enumerate(scenario_names):
            values = []
            for metric in available_metrics:
                values.append(df_normalized.loc[scenario, metric])
            values += values[:1]  # Complete the circle

            ax.plot(angles, values, 'o-', linewidth=2, label=scenario, color=colors[i])
            ax.fill(angles, values, alpha=0.25, color=colors[i])

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(available_metrics)
        ax.set_ylim(0, 1)
        ax.set_title('Multi-Metric Comparison (Normalized)', fontsize=14)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1))
        ax.grid(True)

    # Plot 2: Severity comparison
    ax = axes[1]
    severities = [scenarios[s].get('severity', 0) for s in scenario_names]
    bars = ax.bar(scenario_names, severities, color=colors)
    ax.set_ylabel('Severity Score')
    ax.set_title('Severity Comparison')
    ax.tick_params(axis='x', rotation=45)

    # Add value labels on bars
    for bar, value in zip(bars, severities):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
               f'{value:.1f}', ha='center', va='bottom')

    # Plot 3: Casualties comparison (log scale)
    ax = axes[2]
    casualties = [scenarios[s].get('casualties', 1) for s in scenario_names]
    bars = ax.bar(scenario_names, casualties, color=colors)
    ax.set_yscale('log')
    ax.set_ylabel('Casualties (log scale)')
    ax.set_title('Casualties Comparison')
    ax.tick_params(axis='x', rotation=45)

    # Add value labels
    for bar, value in zip(bars, casualties):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height * 1.1,
               f'{value:.1e}', ha='center', va='bottom', fontsize=8)

    # Plot 4: Economic damage comparison
    ax = axes[3]
    economic_damage = [scenarios[s].get('economic_damage', 1) for s in scenario_names]
    bars = ax.bar(scenario_names, economic_damage, color=colors)
    ax.set_yscale('log')
    ax.set_ylabel('Economic Damage ($, log scale)')
    ax.set_title('Economic Impact Comparison')
    ax.tick_params(axis='x', rotation=45)

    # Plot 5: Recovery time comparison
    ax = axes[4]
    recovery_times = [scenarios[s].get('recovery_time', 0) for s in scenario_names]
    bars = ax.bar(scenario_names, recovery_times, color=colors)
    ax.set_ylabel('Recovery Time (years)')
    ax.set_title('Recovery Time Comparison')
    ax.tick_params(axis='x', rotation=45)

    # Plot 6: Risk matrix
    ax = axes[5]

    # Create risk matrix (probability vs impact)
    # Generate probability values matching number of scenarios
    probabilities = np.linspace(0.01, 0.1, len(scenario_names)).tolist()
    impacts = severities

    scatter = ax.scatter(probabilities, impacts, s=200, c=colors, alpha=0.7)

    for i, scenario in enumerate(scenario_names):
        ax.annotate(scenario, (probabilities[i], impacts[i]),
                   xytext=(5, 5), textcoords='offset points', fontsize=9)

    ax.set_xscale('log')
    ax.set_xlabel('Probability (log scale)')
    ax.set_ylabel('Impact (Severity)')
    ax.set_title('Risk Matrix')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def plot_scenario_timeline_comparison(scenario_timelines: Dict[str, Dict[str, Any]],
                                    figsize: Tuple[int, int] = (14, 10)) -> Figure:
    """Compare event timelines across multiple scenarios."""

    # Generate sample data if none provided
    if not scenario_timelines:
        scenario_timelines = {
            'Asteroid Impact': {
                'impact': 0, 'global_winter': 0.5, 'crop_failure': 1,
                'mass_starvation': 2, 'societal_collapse': 5
            },
            'Pandemic': {
                'outbreak': 0, 'global_spread': 0.25, 'peak_mortality': 1.5,
                'vaccine_development': 2, 'recovery_start': 3
            },
            'Climate Collapse': {
                'tipping_point': 0, 'extreme_weather': 2, 'sea_level_rise': 10,
                'ecosystem_collapse': 20, 'mass_migration': 30
            }
        }

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize)

    # Plot 1: Timeline comparison chart
    y_positions = {}
    y_pos = 0
    colors = plt.cm.get_cmap('Set3')(np.linspace(0, 1, len(scenario_timelines)))

    for i, (scenario, timeline) in enumerate(scenario_timelines.items()):
        y_positions[scenario] = y_pos

        events = list(timeline.keys())
        times = list(timeline.values())

        # Plot timeline
        ax1.plot(times, [y_pos] * len(times), 'o-',
                color=colors[i], linewidth=3, markersize=8, label=scenario)

        # Add event labels
        for event, time in timeline.items():
            ax1.annotate(event, (time, y_pos), xytext=(0, 10),
                        textcoords='offset points', ha='center',
                        fontsize=9, rotation=45)

        y_pos += 1

    ax1.set_xlabel('Time (years from onset)')
    ax1.set_ylabel('Scenarios')
    ax1.set_title('Timeline Comparison Across Scenarios')
    ax1.set_yticks(list(y_positions.values()))
    ax1.set_yticklabels(list(y_positions.keys()))
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    # Plot 2: Event density over time
    all_times = []
    for timeline in scenario_timelines.values():
        all_times.extend(timeline.values())

    if all_times:
        ax2.hist(all_times, bins=20, alpha=0.7, edgecolor='black')
        ax2.set_xlabel('Time (years from onset)')
        ax2.set_ylabel('Number of Events')
        ax2.set_title('Event Density Distribution')
        ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def plot_sensitivity_analysis(base_scenario: Dict[str, Any],
                            parameter_variations: Dict[str, np.ndarray],
                            outcome_metric: str = 'severity',
                            figsize: Tuple[int, int] = (14, 8)) -> Figure:
    """Create sensitivity analysis plots showing parameter influence."""

    # Generate sample data if none provided
    if not parameter_variations:
        parameter_variations = {
            'asteroid_size': np.linspace(0.5, 5.0, 20),
            'impact_angle': np.linspace(15, 90, 20),
            'population_density': np.linspace(100, 1000, 20),
            'preparedness_level': np.linspace(0.1, 1.0, 20)
        }

    fig, axes = plt.subplots(2, 2, figsize=figsize)
    axes = axes.flatten()

    parameters = list(parameter_variations.keys())

    for i, param in enumerate(parameters[:4]):  # Limit to 4 parameters
        if i >= len(axes):
            break

        ax = axes[i]
        param_values = parameter_variations[param]

        # Simulate outcome values (in real scenario, these would be computed)
        if param == 'asteroid_size':
            outcomes = param_values ** 2 * 2  # Quadratic relationship
        elif param == 'impact_angle':
            outcomes = 10 - (param_values - 45) ** 2 / 200  # Parabolic
        elif param == 'population_density':
            outcomes = np.log(param_values)  # Logarithmic
        else:
            outcomes = 10 * (1 - param_values)  # Linear inverse

        # Add some noise
        outcomes += np.random.normal(0, 0.5, len(outcomes))

        # Create scatter plot
        ax.scatter(param_values, outcomes, alpha=0.7, s=50)

        # Fit trend line
        try:
            z = np.polyfit(param_values, outcomes, 2)  # Quadratic fit
            p = np.poly1d(z)
            x_smooth = np.linspace(param_values.min(), param_values.max(), 100)
            ax.plot(x_smooth, p(x_smooth), 'r--', alpha=0.8, linewidth=2)

            # Calculate correlation
            correlation = np.corrcoef(param_values, outcomes)[0, 1]
            ax.text(0.05, 0.95, f'Correlation: {correlation:.3f}',
                   transform=ax.transAxes, bbox=dict(boxstyle='round',
                   facecolor='white', alpha=0.8))
        except:
            pass

        ax.set_xlabel(param.replace('_', ' ').title())
        ax.set_ylabel(outcome_metric.replace('_', ' ').title())
        ax.set_title(f'Sensitivity: {outcome_metric} vs {param}')
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def plot_scenario_ranking(scenarios: Dict[str, Dict[str, Any]],
                        ranking_criteria: Optional[List[str]] = None,
                        weights: Optional[Dict[str, float]] = None,
                        figsize: Tuple[int, int] = (12, 8)) -> Figure:
    """Create scenario ranking visualization with weighted scoring."""

    if ranking_criteria is None:
        ranking_criteria = ['severity', 'casualties', 'economic_damage', 'recovery_time']

    if weights is None:
        weights = {criterion: 1.0 for criterion in ranking_criteria}

    # Generate sample data if none provided
    if not scenarios:
        scenarios = {
            'Asteroid Impact': {'severity': 8.5, 'casualties': 2e9, 'economic_damage': 1e15, 'recovery_time': 50},
            'Supervolcano': {'severity': 9.2, 'casualties': 3e9, 'economic_damage': 5e14, 'recovery_time': 100},
            'Pandemic': {'severity': 6.8, 'casualties': 5e8, 'economic_damage': 2e13, 'recovery_time': 15},
            'Climate Collapse': {'severity': 7.5, 'casualties': 1e9, 'economic_damage': 8e14, 'recovery_time': 200},
            'AI Extinction': {'severity': 9.8, 'casualties': 7e9, 'economic_damage': 1e16, 'recovery_time': 0},
            'Nuclear War': {'severity': 8.0, 'casualties': 1.5e9, 'economic_damage': 3e14, 'recovery_time': 75}
        }

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

    # Calculate weighted scores
    df = pd.DataFrame(scenarios).T

    # Normalize criteria (higher values = worse for all criteria)
    df_normalized = df.copy()
    for criterion in ranking_criteria:
        if criterion in df.columns:
            max_val = df[criterion].max()
            min_val = df[criterion].min()
            if max_val > min_val:
                df_normalized[criterion] = (df[criterion] - min_val) / (max_val - min_val)
            else:
                df_normalized[criterion] = 0.5    # Calculate weighted composite score
    composite_scores = {}
    for scenario in scenarios.keys():
        score = 0.0
        total_weight = 0.0
        for criterion in ranking_criteria:
            if criterion in df_normalized.columns:
                weight = weights.get(criterion, 1.0)
                try:
                    value = float(df_normalized.loc[scenario, criterion])  # type: ignore
                    score += value * weight
                    total_weight += weight
                except (ValueError, TypeError):
                    # Skip non-numeric values
                    continue

        composite_scores[scenario] = score / total_weight if total_weight > 0 else 0.0

    # Sort scenarios by composite score (highest = most dangerous)
    sorted_scenarios = sorted(composite_scores.items(), key=lambda x: x[1], reverse=True)

    # Plot 1: Ranking bar chart
    scenario_names = [item[0] for item in sorted_scenarios]
    scores = [item[1] for item in sorted_scenarios]

    colors = plt.cm.get_cmap('Reds')(np.linspace(0.3, 1.0, len(scenario_names)))
    bars = ax1.barh(scenario_names, scores, color=colors)

    ax1.set_xlabel('Composite Risk Score')
    ax1.set_title('Scenario Risk Ranking')
    ax1.set_xlim(0, 1)

    # Add score labels
    for bar, score in zip(bars, scores):
        width = bar.get_width()
        ax1.text(width + 0.01, bar.get_y() + bar.get_height()/2,
                f'{score:.3f}', ha='left', va='center')

    # Plot 2: Criteria breakdown for top scenarios
    top_scenarios = scenario_names[:5]  # Top 5 most dangerous

    criteria_data = []
    for scenario in top_scenarios:
        for criterion in ranking_criteria:
            if criterion in df_normalized.columns:
                criteria_data.append({
                    'Scenario': scenario,
                    'Criterion': criterion,
                    'Normalized_Score': df_normalized.loc[scenario, criterion],
                    'Weight': weights.get(criterion, 1.0)
                })

    criteria_df = pd.DataFrame(criteria_data)

    # Create grouped bar chart
    scenario_positions = np.arange(len(top_scenarios))
    bar_width = 0.8 / len(ranking_criteria)

    for i, criterion in enumerate(ranking_criteria):
        criterion_data = criteria_df[criteria_df['Criterion'] == criterion]
        values = [criterion_data[criterion_data['Scenario'] == s]['Normalized_Score'].iloc[0]
                 if len(criterion_data[criterion_data['Scenario'] == s]) > 0 else 0
                 for s in top_scenarios]

        ax2.bar(scenario_positions + i * bar_width, values,
               width=bar_width, label=criterion, alpha=0.8)

    ax2.set_xlabel('Scenarios')
    ax2.set_ylabel('Normalized Score')
    ax2.set_title('Criteria Breakdown (Top 5 Scenarios)')
    ax2.set_xticks(scenario_positions + bar_width * (len(ranking_criteria) - 1) / 2)
    ax2.set_xticklabels(top_scenarios, rotation=45, ha='right')
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    return fig


def plot_multi_scenario_uncertainty(scenario_ensembles: Dict[str, Dict[str, List[float]]],
                                  metric: str = 'severity',
                                  figsize: Tuple[int, int] = (14, 8)) -> Figure:
    """Plot uncertainty comparisons across multiple scenarios."""

    # Generate sample data if none provided
    if not scenario_ensembles:
        np.random.seed(42)
        scenario_ensembles = {
            'Asteroid Impact': {
                'severity': np.random.normal(8.5, 1.5, 1000).tolist(),
                'casualties': np.random.lognormal(21, 0.5, 1000).tolist()
            },
            'Pandemic': {
                'severity': np.random.normal(6.8, 2.0, 1000).tolist(),
                'casualties': np.random.lognormal(20, 0.8, 1000).tolist()
            },            'Climate Collapse': {
                'severity': np.random.normal(7.5, 1.0, 1000).tolist(),
                'casualties': np.random.lognormal(20.7, 0.6, 1000).tolist()
            }
        }

    fig, axes = plt.subplots(2, 2, figsize=figsize)
    axes = axes.flatten()

    scenario_names = list(scenario_ensembles.keys())
    colors = plt.cm.get_cmap('Set3')(np.linspace(0, 1, len(scenario_names)))

    # Plot 1: Box plots comparison
    ax = axes[0]
    data_for_boxplot = []
    labels = []

    for scenario in scenario_names:
        if metric in scenario_ensembles[scenario]:
            data_for_boxplot.append(scenario_ensembles[scenario][metric])
            labels.append(scenario)

    if data_for_boxplot:
        bp = ax.boxplot(data_for_boxplot, labels=labels, patch_artist=True)
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)

    ax.set_ylabel(metric.replace('_', ' ').title())
    ax.set_title(f'{metric.title()} Distribution Comparison')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, alpha=0.3)

    # Plot 2: Overlapping histograms
    ax = axes[1]
    for i, scenario in enumerate(scenario_names):
        if metric in scenario_ensembles[scenario]:
            data = scenario_ensembles[scenario][metric]
            ax.hist(data, bins=30, alpha=0.6, label=scenario,
                   color=colors[i], density=True)

    ax.set_xlabel(metric.replace('_', ' ').title())
    ax.set_ylabel('Density')
    ax.set_title(f'{metric.title()} Distribution Overlap')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot 3: Cumulative distributions
    ax = axes[2]
    for i, scenario in enumerate(scenario_names):
        if metric in scenario_ensembles[scenario]:
            data = np.sort(scenario_ensembles[scenario][metric])
            cumulative = np.arange(1, len(data) + 1) / len(data)
            ax.plot(data, cumulative, label=scenario, color=colors[i], linewidth=2)

    ax.set_xlabel(metric.replace('_', ' ').title())
    ax.set_ylabel('Cumulative Probability')
    ax.set_title(f'{metric.title()} Cumulative Distributions')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot 4: Uncertainty metrics comparison
    ax = axes[3]

    uncertainty_metrics = ['Mean', 'Std Dev', '95th %ile', '5th %ile']
    metric_values = {metric_name: [] for metric_name in uncertainty_metrics}

    for scenario in scenario_names:
        if metric in scenario_ensembles[scenario]:
            data = scenario_ensembles[scenario][metric]
            metric_values['Mean'].append(np.mean(data))
            metric_values['Std Dev'].append(np.std(data))
            metric_values['95th %ile'].append(np.percentile(data, 95))
            metric_values['5th %ile'].append(np.percentile(data, 5))

    x = np.arange(len(scenario_names))
    width = 0.2

    for i, (metric_name, values) in enumerate(metric_values.items()):
        ax.bar(x + i * width, values, width, label=metric_name, alpha=0.8)

    ax.set_xlabel('Scenarios')
    ax.set_ylabel('Value')
    ax.set_title(f'{metric.title()} Uncertainty Metrics')
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(scenario_names, rotation=45, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    return fig


# Demo function
def demo_comparative_analysis():
    """Demonstrate comparative analysis capabilities."""

    print("📊 Demonstrating Comparative Analysis Capabilities")
    print("=" * 50)

    # Demo 1: Scenarios overview
    print("1. Creating scenarios overview comparison...")
    try:
        scenarios = {}  # Will use default sample data
        fig1 = compare_scenarios_overview(scenarios)
        print("   ✅ Scenarios overview created")
        plt.close(fig1)
    except Exception as e:
        print(f"   ❌ Error creating scenarios overview: {e}")

    # Demo 2: Timeline comparison
    print("2. Creating timeline comparison...")
    try:
        timelines = {}  # Will use default sample data
        fig2 = plot_scenario_timeline_comparison(timelines)
        print("   ✅ Timeline comparison created")
        plt.close(fig2)
    except Exception as e:
        print(f"   ❌ Error creating timeline comparison: {e}")

    # Demo 3: Sensitivity analysis
    print("3. Creating sensitivity analysis...")
    try:
        base_scenario = {}
        param_variations = {}  # Will use default sample data
        fig3 = plot_sensitivity_analysis(base_scenario, param_variations)
        print("   ✅ Sensitivity analysis created")
        plt.close(fig3)
    except Exception as e:
        print(f"   ❌ Error creating sensitivity analysis: {e}")

    # Demo 4: Scenario ranking
    print("4. Creating scenario ranking...")
    try:
        scenarios = {}  # Will use default sample data
        fig4 = plot_scenario_ranking(scenarios)
        print("   ✅ Scenario ranking created")
        plt.close(fig4)
    except Exception as e:
        print(f"   ❌ Error creating scenario ranking: {e}")

    print("\n✅ Comparative analysis demonstrations completed!")


if __name__ == "__main__":
    demo_comparative_analysis()
