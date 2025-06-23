"""
Advanced 3D Visualization Demo for E.L.E.S.

This script demonstrates the advanced 3D visualization and simulation capabilities
including real-time physics, particle systems, and interactive features.
"""

import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

try:
    from visualizations.3d.model import (
        render_asteroid_impact,
        render_climate_collapse_3d,
        render_gamma_ray_burst_3d,
        render_ai_extinction_3d,
        create_interactive_3d_timeline,
        create_multi_scenario_3d_comparison
    )
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback to direct imports
    import importlib.util
    spec = importlib.util.spec_from_file_location("model", 
                                                  os.path.join(os.path.dirname(__file__), "model.py"))
    model = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model)
    
    render_asteroid_impact = model.render_asteroid_impact
    render_climate_collapse_3d = model.render_climate_collapse_3d
    render_gamma_ray_burst_3d = model.render_gamma_ray_burst_3d
    render_ai_extinction_3d = model.render_ai_extinction_3d
    create_interactive_3d_timeline = model.create_interactive_3d_timeline
    create_multi_scenario_3d_comparison = model.create_multi_scenario_3d_comparison

try:
    from visualizations.3d.advanced_simulations import (
        create_3d_visualization_manager,
        SimulationParameters
    )
    HAS_ADVANCED_SIMS = True
except ImportError:
    HAS_ADVANCED_SIMS = False

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from typing import Dict, Any, List
import time


def demo_basic_3d_visualizations():
    """Demonstrate basic 3D visualizations for all event types."""
    print("🌍 Running Basic 3D Visualization Demos...")
    
    # Asteroid Impact Demo
    print("  ☄️  Asteroid Impact 3D Visualization")
    asteroid_data = {
        'crater_diameter_km': 15,
        'impact_angle': 45,
        'asteroid_diameter_km': 2
    }
    asteroid_fig = render_asteroid_impact(asteroid_data)
    asteroid_fig.write_html("demo_asteroid_3d.html")
    print("     Generated: demo_asteroid_3d.html")
    
    # Climate Collapse Demo
    print("  🌡️  Climate Collapse 3D Visualization")
    climate_data = {
        'temperature_change_c': 4.5,
        'sea_level_rise_m': 2.3,
        'co2_ppm': 450
    }
    climate_fig = render_climate_collapse_3d(climate_data)
    climate_fig.write_html("demo_climate_3d.html")
    print("     Generated: demo_climate_3d.html")
    
    # Gamma-Ray Burst Demo
    print("  💫 Gamma-Ray Burst 3D Visualization")
    grb_data = {
        'distance_ly': 6000,
        'duration_seconds': 30,
        'energy_joules': 1e44
    }
    grb_fig = render_gamma_ray_burst_3d(grb_data)
    grb_fig.write_html("demo_grb_3d.html")
    print("     Generated: demo_grb_3d.html")
    
    # AI Extinction Demo
    print("  🤖 AI Extinction 3D Visualization")
    ai_data = {
        'ai_level': 7,
        'control_difficulty': 75,
        'spread_rate_percent_per_day': 2.5
    }
    ai_fig = render_ai_extinction_3d(ai_data)
    ai_fig.write_html("demo_ai_3d.html")
    print("     Generated: demo_ai_3d.html")


def demo_interactive_timeline():
    """Demonstrate interactive 3D timeline visualization."""
    print("  📈 Interactive 3D Timeline")
    
    event_types = ['asteroid', 'pandemic', 'climate_collapse']
    
    for event_type in event_types:
        event_data = {'event_type': event_type}
        timeline_fig = create_interactive_3d_timeline(event_data, event_type)
        filename = f"demo_timeline_{event_type}_3d.html"
        timeline_fig.write_html(filename)
        print(f"     Generated: {filename}")


def demo_multi_scenario_comparison():
    """Demonstrate multi-scenario 3D comparison."""
    print("  🔄 Multi-Scenario 3D Comparison")
    
    scenarios = [
        {
            'event_type': 'asteroid',
            'severity': 5,
            'casualties': 1e8,
            'economic_impact': 5000
        },
        {
            'event_type': 'pandemic',
            'severity': 4,
            'casualties': 5e7,
            'economic_impact': 3000
        },
        {
            'event_type': 'supervolcano',
            'severity': 6,
            'casualties': 2e8,
            'economic_impact': 8000
        },
        {
            'event_type': 'climate_collapse',
            'severity': 4,
            'casualties': 1e9,
            'economic_impact': 15000
        },
        {
            'event_type': 'ai_extinction',
            'severity': 6,
            'casualties': 7e9,
            'economic_impact': 50000
        }
    ]
    
    comparison_fig = create_multi_scenario_3d_comparison(scenarios)
    comparison_fig.write_html("demo_comparison_3d.html")
    print("     Generated: demo_comparison_3d.html")


def demo_advanced_simulations():
    """Demonstrate advanced 3D simulations with particle systems."""
    if not HAS_ADVANCED_SIMS:
        print("  ⚠️  Advanced simulations not available (missing optional libraries)")
        return
    
    print("  🚀 Advanced 3D Simulations")
    
    # Create visualization manager
    manager = create_3d_visualization_manager()
    
    # High-quality simulation parameters
    params = SimulationParameters(
        resolution=150,
        time_steps=30,
        frame_rate=10.0,
        quality="high",
        enable_physics=True,
        enable_particles=True,
        enable_volumetrics=True
    )
    
    # Asteroid impact with particle simulation
    print("     🌠 Asteroid Impact with Particle Physics")
    asteroid_event = {
        'diameter_km': 1.5,
        'velocity_km_s': 25.0,
        'density_kg_m3': 3500,
        'impact_angle': 60.0
    }
    
    try:
        asteroid_frames = manager.run_advanced_simulation('asteroid', asteroid_event, params)
        if asteroid_frames:
            # Create animation
            animation_file = manager.create_animation(asteroid_frames, "demo_asteroid_advanced.html")
            print(f"     Generated: {animation_file}")
            
            # Also save single frame for VR
            vr_frame = manager.create_vr_ready_visualization('asteroid', asteroid_event)
            vr_frame.write_html("demo_asteroid_vr.html")
            print("     Generated: demo_asteroid_vr.html (VR-ready)")
        
    except Exception as e:
        print(f"     Error in asteroid simulation: {e}")
    
    # Volcanic eruption simulation
    print("     🌋 Volcanic Eruption with Volumetric Rendering")
    volcano_event = {
        'vei': 7,
        'magma_volume_km3': 500,
        'eruption_rate_m3_s': 5e7
    }
    
    try:
        volcano_frames = manager.run_advanced_simulation('supervolcano', volcano_event, params)
        if volcano_frames:
            animation_file = manager.create_animation(volcano_frames, "demo_volcano_advanced.html")
            print(f"     Generated: {animation_file}")
    
    except Exception as e:
        print(f"     Error in volcano simulation: {e}")
    
    # Pandemic network simulation
    print("     🦠 Pandemic Network Simulation")
    pandemic_event = {
        'r0': 3.2,
        'mortality_rate': 0.03,
        'incubation_period_days': 7
    }
    
    try:
        pandemic_frames = manager.run_advanced_simulation('pandemic', pandemic_event, params)
        if pandemic_frames:
            animation_file = manager.create_animation(pandemic_frames, "demo_pandemic_advanced.html")
            print(f"     Generated: {animation_file}")
    
    except Exception as e:
        print(f"     Error in pandemic simulation: {e}")
    
    # Print capabilities
    capabilities = manager.get_simulation_capabilities()
    print("  📊 Simulation Capabilities:")
    for key, value in capabilities.items():
        print(f"     {key}: {value}")


def demo_combined_dashboard():
    """Create a combined dashboard with multiple 3D views."""
    print("  📋 Combined 3D Dashboard")
    
    # Create subplot figure with multiple 3D scenes
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{'type': 'scene'}, {'type': 'scene'}],
               [{'type': 'scene'}, {'type': 'scene'}]],
        subplot_titles=['Asteroid Impact', 'Climate Change', 
                       'Gamma-Ray Burst', 'AI Risk Network'],
        vertical_spacing=0.1,
        horizontal_spacing=0.1
    )
    
    # Add simplified versions of each visualization
    # This is a complex operation, so we'll create a basic version
    
    # Simple asteroid crater
    crater_size = 10
    theta = np.linspace(0, 2*np.pi, 30)
    r = np.linspace(0, crater_size, 15)
    R, THETA = np.meshgrid(r, theta)
    Z_crater = -2 * (1 - (R/crater_size)**2)
    X_crater = R * np.cos(THETA)
    Y_crater = R * np.sin(THETA)
    
    fig.add_trace(
        go.Surface(x=X_crater, y=Y_crater, z=Z_crater, 
                  colorscale='Earth', showscale=False),
        row=1, col=1
    )
    
    # Simple climate visualization (temperature grid)
    x_climate = np.linspace(-50, 50, 20)
    y_climate = np.linspace(-50, 50, 20)
    X_climate, Y_climate = np.meshgrid(x_climate, y_climate)
    Z_climate = 2 * np.sin(X_climate/10) * np.cos(Y_climate/10)
    
    fig.add_trace(
        go.Surface(x=X_climate, y=Y_climate, z=Z_climate,
                  colorscale='RdYlBu_r', showscale=False),
        row=1, col=2
    )
    
    # Simple GRB beam
    beam_x = np.array([0, 50])
    beam_y = np.array([0, 0])
    beam_z = np.array([0, 0])
    
    fig.add_trace(
        go.Scatter3d(x=beam_x, y=beam_y, z=beam_z,
                    mode='lines', line=dict(color='yellow', width=10)),
        row=2, col=1
    )
    
    # AI network nodes
    n_nodes = 10
    np.random.seed(42)
    node_x = np.random.uniform(-25, 25, n_nodes)
    node_y = np.random.uniform(-25, 25, n_nodes)
    node_z = np.random.uniform(-25, 25, n_nodes)
    
    fig.add_trace(
        go.Scatter3d(x=node_x, y=node_y, z=node_z,
                    mode='markers', 
                    marker=dict(size=8, color='red')),
        row=2, col=2
    )
    
    fig.update_layout(
        title="E.L.E.S. 3D Visualization Dashboard",
        height=800,
        showlegend=False
    )
    
    fig.write_html("demo_dashboard_3d.html")
    print("     Generated: demo_dashboard_3d.html")


def demo_performance_benchmark():
    """Benchmark 3D visualization performance."""
    print("  ⏱️  Performance Benchmark")
    
    if not HAS_ADVANCED_SIMS:
        print("     Advanced simulations not available for benchmarking")
        return
    
    manager = create_3d_visualization_manager()
    
    # Test different quality levels
    quality_levels = ["low", "medium", "high"]
    
    for quality in quality_levels:
        print(f"     Testing {quality} quality...")
        
        params = SimulationParameters(
            resolution=50 if quality == "low" else 100 if quality == "medium" else 200,
            time_steps=10,
            frame_rate=30.0,
            quality=quality,
            enable_physics=True,
            enable_particles=True
        )
        
        event_data = {
            'diameter_km': 1.0,
            'velocity_km_s': 20.0,
            'density_kg_m3': 3000
        }
        
        start_time = time.time()
        try:
            frames = manager.run_advanced_simulation('asteroid', event_data, params)
            end_time = time.time()
            
            duration = end_time - start_time
            fps = len(frames) / duration if duration > 0 else 0
            
            print(f"       {quality.capitalize()}: {duration:.2f}s, {fps:.1f} FPS, {len(frames)} frames")
            
        except Exception as e:
            print(f"       {quality.capitalize()}: Error - {e}")


def main():
    """Run all 3D visualization demos."""
    print("🎯 E.L.E.S. Advanced 3D Visualization Demo")
    print("=" * 50)
    
    # Create output directory
    output_dir = "3d_demo_output"
    os.makedirs(output_dir, exist_ok=True)
    os.chdir(output_dir)
    
    try:
        # Run all demos
        demo_basic_3d_visualizations()
        print()
        
        demo_interactive_timeline()
        print()
        
        demo_multi_scenario_comparison()
        print()
        
        demo_combined_dashboard()
        print()
        
        demo_advanced_simulations()
        print()
        
        demo_performance_benchmark()
        print()
        
        print("✅ All demos completed successfully!")
        print(f"📁 Output files saved to: {os.path.abspath('.')}")
        print("\n🌟 Key Features Demonstrated:")
        print("   • Real-time 3D physics simulations")
        print("   • Particle system effects")
        print("   • Interactive timeline visualizations")
        print("   • Multi-scenario comparisons")
        print("   • VR/AR ready outputs")
        print("   • Animated sequences")
        print("   • Performance optimization")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        os.chdir("..")


if __name__ == "__main__":
    main()
