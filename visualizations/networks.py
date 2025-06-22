"""
Network Analysis Visualizations for E.L.E.S.

This module provides network-based visualizations for modeling complex
interdependent systems during extinction events, such as:
- Infrastructure networks
- Supply chain networks
- Social networks
- Ecosystem food webs
- Economic dependencies
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import Dict, Any, List, Optional, Tuple
from matplotlib.figure import Figure

try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False
    print("NetworkX not available. Install with: pip install networkx")

try:
    from scipy.spatial.distance import pdist, squareform
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False


def create_infrastructure_network(nodes_data: Dict[str, Any],
                                dependencies: List[Tuple[str, str]]) -> nx.Graph:
    """Create infrastructure network showing critical dependencies."""

    G = nx.Graph()

    # Add nodes with attributes
    for node_id, attributes in nodes_data.items():
        G.add_node(node_id, **attributes)

    # Add edges representing dependencies
    for source, target in dependencies:
        if source in nodes_data and target in nodes_data:
            G.add_edge(source, target)

    return G


def plot_infrastructure_vulnerability(G,
                                    event_impact: Dict[str, float],
                                    figsize: Tuple[int, int] = (12, 10)) -> Figure:
    """Visualize infrastructure network vulnerability during extinction event."""

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

    # Calculate layout
    pos = nx.spring_layout(G, k=1, iterations=50)

    # Plot 1: Network before event
    ax1.set_title("Infrastructure Network - Before Event", fontsize=14)

    # Draw nodes
    node_colors = ['lightblue' for _ in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_color=node_colors,
                          node_size=1000, ax=ax1)

    # Draw edges
    nx.draw_networkx_edges(G, pos, edge_color='gray', ax=ax1)

    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=8, ax=ax1)

    ax1.axis('off')

    # Plot 2: Network after event impact
    ax2.set_title("Infrastructure Network - After Event Impact", fontsize=14)

    # Color nodes based on damage level
    damaged_colors = []
    for node in G.nodes():
        damage = event_impact.get(node, 0)
        if damage > 0.8:
            damaged_colors.append('red')  # Severely damaged
        elif damage > 0.5:
            damaged_colors.append('orange')  # Moderately damaged
        elif damage > 0.2:
            damaged_colors.append('yellow')  # Lightly damaged
        else:
            damaged_colors.append('lightgreen')  # Undamaged

    nx.draw_networkx_nodes(G, pos, node_color=damaged_colors,
                          node_size=1000, ax=ax2)

    # Draw edges with varying opacity based on functionality
    edge_colors = []
    edge_alphas = []
    for edge in G.edges():
        source_damage = event_impact.get(edge[0], 0)
        target_damage = event_impact.get(edge[1], 0)
        avg_damage = (source_damage + target_damage) / 2

        if avg_damage > 0.7:
            edge_colors.append('red')
            edge_alphas.append(0.3)
        elif avg_damage > 0.4:
            edge_colors.append('orange')
            edge_alphas.append(0.6)
        else:
            edge_colors.append('gray')
            edge_alphas.append(1.0)

    for i, edge in enumerate(G.edges()):
        nx.draw_networkx_edges(G, pos, edgelist=[edge],
                             edge_color=edge_colors[i],
                             alpha=edge_alphas[i], ax=ax2)

    nx.draw_networkx_labels(G, pos, font_size=8, ax=ax2)
    ax2.axis('off')

    # Add legend
    legend_elements = [
        patches.Patch(color='red', label='Severely Damaged (>80%)'),
        patches.Patch(color='orange', label='Moderately Damaged (50-80%)'),
        patches.Patch(color='yellow', label='Lightly Damaged (20-50%)'),
        patches.Patch(color='lightgreen', label='Undamaged (<20%)')
    ]
    ax2.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1))

    plt.tight_layout()
    return fig


def plot_supply_chain_disruption(supply_data: Dict[str, Any],
                               disruption_points: List[str],
                               figsize: Tuple[int, int] = (14, 10)) -> Figure:
    """Visualize supply chain network and disruption cascades."""

    fig, ax = plt.subplots(figsize=figsize)

    # Create supply chain network
    G = nx.DiGraph()  # Directed graph for supply chains

    # Add nodes from supply data
    suppliers = supply_data.get('suppliers', {})
    manufacturers = supply_data.get('manufacturers', {})
    distributors = supply_data.get('distributors', {})
    retailers = supply_data.get('retailers', {})

    # Add all nodes with types
    for node_type, nodes in [('supplier', suppliers),
                           ('manufacturer', manufacturers),
                           ('distributor', distributors),
                           ('retailer', retailers)]:
        for node_id, attributes in nodes.items():
            G.add_node(node_id, type=node_type, **attributes)

    # Add supply relationships
    relationships = supply_data.get('relationships', [])
    for source, target, attributes in relationships:
        G.add_edge(source, target, **attributes)

    # Calculate hierarchical layout
    pos = {}
    y_positions = {'supplier': 3, 'manufacturer': 2, 'distributor': 1, 'retailer': 0}

    for node_type in ['supplier', 'manufacturer', 'distributor', 'retailer']:
        nodes_of_type = [n for n in G.nodes() if G.nodes[n].get('type') == node_type]
        x_spacing = 2.0 / (len(nodes_of_type) + 1) if nodes_of_type else 1
        for i, node in enumerate(nodes_of_type):
            pos[node] = ((i + 1) * x_spacing - 1, y_positions[node_type])

    # Color nodes based on disruption
    node_colors = []
    for node in G.nodes():
        if node in disruption_points:
            node_colors.append('red')
        else:
            node_type = G.nodes[node].get('type', '')
            type_colors = {
                'supplier': 'lightblue',
                'manufacturer': 'lightgreen',
                'distributor': 'lightyellow',
                'retailer': 'lightpink'
            }
            node_colors.append(type_colors.get(node_type, 'gray'))

    # Draw network
    nx.draw_networkx_nodes(G, pos, node_color=node_colors,
                          node_size=1500, ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color='gray',
                          arrows=True, arrowsize=20, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=8, ax=ax)

    # Add title and legend
    ax.set_title("Supply Chain Network - Disruption Analysis", fontsize=16)

    legend_elements = [
        patches.Patch(color='red', label='Disrupted Nodes'),
        patches.Patch(color='lightblue', label='Suppliers'),
        patches.Patch(color='lightgreen', label='Manufacturers'),
        patches.Patch(color='lightyellow', label='Distributors'),
        patches.Patch(color='lightpink', label='Retailers')
    ]
    ax.legend(handles=legend_elements, loc='upper right')

    ax.axis('off')
    plt.tight_layout()
    return fig


def plot_ecosystem_food_web(species_data: Dict[str, Any],
                          extinction_cascade: List[str],
                          figsize: Tuple[int, int] = (12, 10)) -> Figure:
    """Visualize ecosystem food web and extinction cascades."""

    fig, ax = plt.subplots(figsize=figsize)

    # Create food web network
    G = nx.DiGraph()

    # Add species nodes
    species = species_data.get('species', {})
    for species_id, attributes in species.items():
        G.add_node(species_id, **attributes)

    # Add predator-prey relationships
    relationships = species_data.get('feeding_relationships', [])
    for predator, prey in relationships:
        if predator in species and prey in species:
            G.add_edge(prey, predator)  # Prey -> Predator

    # Calculate trophic levels for layout
    trophic_levels = {}

    # Start with primary producers (no incoming edges)
    primary_producers = [n for n in G.nodes() if G.in_degree(n) == 0]
    for producer in primary_producers:
        trophic_levels[producer] = 0

    # Calculate trophic levels iteratively
    for level in range(1, 6):  # Max 5 trophic levels
        for node in G.nodes():
            if node not in trophic_levels:
                predecessors = list(G.predecessors(node))
                if predecessors and all(pred in trophic_levels for pred in predecessors):
                    max_pred_level = max(trophic_levels[pred] for pred in predecessors)
                    trophic_levels[node] = max_pred_level + 1

    # Set remaining nodes to level 0 if not assigned
    for node in G.nodes():
        if node not in trophic_levels:
            trophic_levels[node] = 0

    # Create positions based on trophic levels
    pos = {}
    level_counts = {}
    for node, level in trophic_levels.items():
        level_counts[level] = level_counts.get(level, 0) + 1

    level_positions = {}
    for level in level_counts:
        level_positions[level] = 0

    for node, level in trophic_levels.items():
        x_pos = level_positions[level] * 2.0 / max(level_counts[level], 1) - 1
        y_pos = level
        pos[node] = (x_pos, y_pos)
        level_positions[level] += 1

    # Color nodes based on extinction status
    node_colors = []
    for node in G.nodes():
        if node in extinction_cascade:
            node_colors.append('red')
        else:
            # Color by trophic level
            level = trophic_levels[node]
            level_colors = ['green', 'lightgreen', 'yellow', 'orange', 'red', 'darkred']
            color_index = min(level, len(level_colors) - 1)
            node_colors.append(level_colors[color_index])

    # Draw network
    nx.draw_networkx_nodes(G, pos, node_color=node_colors,
                          node_size=800, ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color='gray',
                          arrows=True, arrowsize=15, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=8, ax=ax)

    # Add title and labels
    ax.set_title("Ecosystem Food Web - Extinction Cascade", fontsize=16)
    ax.set_xlabel("Species Distribution")
    ax.set_ylabel("Trophic Level")

    # Add legend
    legend_elements = [
        patches.Patch(color='red', label='Extinct Species'),
        patches.Patch(color='green', label='Primary Producers'),
        patches.Patch(color='lightgreen', label='Primary Consumers'),
        patches.Patch(color='yellow', label='Secondary Consumers'),
        patches.Patch(color='orange', label='Tertiary Consumers'),
        patches.Patch(color='darkred', label='Apex Predators')
    ]
    ax.legend(handles=legend_elements, loc='upper right')

    plt.tight_layout()
    return fig


def calculate_network_resilience(G: nx.Graph,
                               failure_cascade: List[str]) -> Dict[str, float]:
    """Calculate network resilience metrics during cascade failure."""

    metrics = {}

    # Original network metrics
    metrics['original_nodes'] = G.number_of_nodes()
    metrics['original_edges'] = G.number_of_edges()
    metrics['original_connectivity'] = nx.average_node_connectivity(G)

    # Create damaged network
    G_damaged = G.copy()
    G_damaged.remove_nodes_from(failure_cascade)

    # Damaged network metrics
    metrics['remaining_nodes'] = G_damaged.number_of_nodes()
    metrics['remaining_edges'] = G_damaged.number_of_edges()

    if G_damaged.number_of_nodes() > 0:
        if nx.is_connected(G_damaged):
            metrics['damaged_connectivity'] = nx.average_node_connectivity(G_damaged)
        else:
            # For disconnected graphs, calculate for largest component
            largest_cc = max(nx.connected_components(G_damaged), key=len)
            G_largest = G_damaged.subgraph(largest_cc)
            metrics['damaged_connectivity'] = nx.average_node_connectivity(G_largest)
            metrics['largest_component_size'] = len(largest_cc)
    else:
        metrics['damaged_connectivity'] = 0
        metrics['largest_component_size'] = 0

    # Calculate resilience ratios
    metrics['node_survival_ratio'] = metrics['remaining_nodes'] / metrics['original_nodes']
    metrics['edge_survival_ratio'] = metrics['remaining_edges'] / metrics['original_edges']
    metrics['connectivity_ratio'] = (metrics['damaged_connectivity'] /
                                   metrics['original_connectivity']
                                   if metrics['original_connectivity'] > 0 else 0)

    return metrics


# Example usage and demo functions
def demo_infrastructure_network():
    """Demonstrate infrastructure network visualization."""

    # Sample infrastructure data
    nodes_data = {
        'power_plant_1': {'type': 'power', 'capacity': 1000, 'critical': True},
        'power_plant_2': {'type': 'power', 'capacity': 800, 'critical': False},
        'water_treatment': {'type': 'water', 'capacity': 500, 'critical': True},
        'hospital_1': {'type': 'healthcare', 'capacity': 200, 'critical': True},
        'hospital_2': {'type': 'healthcare', 'capacity': 150, 'critical': False},
        'data_center': {'type': 'communications', 'capacity': 100, 'critical': True},
        'fuel_depot': {'type': 'fuel', 'capacity': 1000, 'critical': True}
    }

    dependencies = [
        ('power_plant_1', 'hospital_1'),
        ('power_plant_1', 'water_treatment'),
        ('power_plant_2', 'hospital_2'),
        ('power_plant_1', 'data_center'),
        ('fuel_depot', 'power_plant_1'),
        ('fuel_depot', 'power_plant_2'),
        ('water_treatment', 'hospital_1'),
        ('data_center', 'hospital_1')
    ]

    # Create network
    G = create_infrastructure_network(nodes_data, dependencies)

    # Simulate event impact
    event_impact = {
        'power_plant_1': 0.9,  # Heavily damaged
        'fuel_depot': 0.7,     # Moderately damaged
        'hospital_1': 0.3,     # Lightly damaged
        'data_center': 0.8,    # Heavily damaged
        'power_plant_2': 0.1,  # Minimal damage
        'water_treatment': 0.2, # Light damage
        'hospital_2': 0.1      # Minimal damage
    }

    # Create visualization
    fig = plot_infrastructure_vulnerability(G, event_impact)
    plt.show()

    # Calculate resilience
    failed_nodes = [node for node, damage in event_impact.items() if damage > 0.5]
    resilience = calculate_network_resilience(G, failed_nodes)

    print("Network Resilience Analysis:")
    for metric, value in resilience.items():
        print(f"  {metric}: {value:.3f}")


if __name__ == "__main__":
    demo_infrastructure_network()
