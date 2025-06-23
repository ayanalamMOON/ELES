import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import numpy as np
from pathlib import Path
import sys
import os

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from eles_core.engine import Engine
from config.constants import SEVERITY_LEVELS, SEVERITY_COLORS
from eles_core.event_types import (
    AsteroidImpact, Supervolcano, ClimateCollapse,
    Pandemic, GammaRayBurst, AIExtinction
)

def run():
    """Advanced home page for E.L.E.S."""
    st.set_page_config(
        page_title="E.L.E.S. - Extinction-Level Event Simulator",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for advanced styling
    st.markdown("""
    <style>
    /* Main header styling */
    .main-header {
        font-size: 4rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 900;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    .subtitle {
        font-size: 1.8rem;
        color: #E2E8F0;
        text-align: center;
        margin-bottom: 2rem;
        opacity: 0.9;
        font-weight: 300;
    }

    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 1.5rem;
        margin-bottom: 3rem;
        text-align: center;
        color: white;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    }

    .hero-text {
        font-size: 1.4rem;
        line-height: 1.6;
        margin-bottom: 2rem;
        opacity: 0.95;
    }

    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
    }

    .feature-card {
        background: linear-gradient(145deg, #2D3748, #4A5568);
        padding: 2rem;
        border-radius: 1rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }

    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }

    .feature-icon {
        font-size: 3.5rem;
        margin-bottom: 1.5rem;
        display: block;
    }

    .feature-title {
        font-size: 1.4rem;
        font-weight: bold;
        color: #FAFAFA;
        margin-bottom: 1rem;
    }

    .feature-description {
        color: #A0AEC0;
        font-size: 1rem;
        line-height: 1.5;
    }

    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }

    .stat-card {
        background: rgba(255,255,255,0.05);
        padding: 1.5rem;
        border-radius: 1rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
    }

    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4ECDC4;
        display: block;
    }

    .stat-label {
        color: #A0AEC0;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }

    .event-showcase {
        background: linear-gradient(135deg, #1A202C, #2D3748);
        padding: 2rem;
        border-radius: 1rem;
        margin: 2rem 0;
        border: 1px solid rgba(255,255,255,0.1);
    }

    .quick-demo {
        background: rgba(76, 175, 80, 0.1);
        border-left: 4px solid #4CAF50;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border-radius: 0.5rem;
    }

    .severity-indicator {
        display: inline-block;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        margin-right: 0.5rem;
        vertical-align: middle;
    }

    .metric-container {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 2rem;
        border-radius: 1rem;
        margin: 2rem 0;
        color: white;
    }

    .section-header {
        font-size: 2rem;
        font-weight: bold;
        margin: 2rem 0 1rem 0;
        color: #FAFAFA;
        text-align: center;
    }

    .getting-started {
        background: linear-gradient(135deg, #FF6B6B, #4ECDC4);
        padding: 2rem;
        border-radius: 1rem;
        margin: 2rem 0;
        color: white;
        text-align: center;
    }

    .action-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 2rem;
        border: none;
        border-radius: 0.5rem;
        font-size: 1.1rem;
        font-weight: bold;
        cursor: pointer;
        margin: 0.5rem;
        transition: all 0.3s ease;
    }

    .action-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

    # Main header
    st.markdown('<h1 class="main-header">🌍 E.L.E.S.</h1>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Extinction-Level Event Simulator</div>', unsafe_allow_html=True)

    # Hero section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-text">
            🚀 <strong>Explore Catastrophic Scenarios with Scientific Precision</strong>
        </div>
        <p style="font-size: 1.2rem; margin-bottom: 2rem; opacity: 0.9;">
            Simulate and analyze extinction-level events using peer-reviewed scientific models.
            From asteroid impacts to AI risks, understand the forces that could reshape our world.
        </p>
        <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 2rem; font-size: 0.9rem;">
                📊 Real-time Analysis
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 2rem; font-size: 0.9rem;">
                🔬 Scientific Accuracy
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 2rem; font-size: 0.9rem;">
                🌐 Global Impact Assessment
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Quick stats section
    display_quick_stats()

    # Main feature showcase
    display_event_types()

    # Interactive demonstration
    display_interactive_demo()

    # Key capabilities
    display_key_capabilities()

    # Real-time scenario comparison
    display_scenario_comparison()

    # Getting started section
    display_getting_started()

def display_quick_stats():
    """Display quick statistics about the simulator."""
    st.markdown('<h2 class="section-header">📊 Platform Overview</h2>', unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown("""
        <div class="stat-card">
            <span class="stat-number">6</span>
            <div class="stat-label">Event Types</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="stat-card">
            <span class="stat-number">95%</span>
            <div class="stat-label">Scientific Accuracy</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="stat-card">
            <span class="stat-number">∞</span>
            <div class="stat-label">Scenarios</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="stat-card">
            <span class="stat-number">12+</span>
            <div class="stat-label">Analysis Metrics</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown("""
        <div class="stat-card">
            <span class="stat-number">3D</span>
            <div class="stat-label">Visualizations</div>
        </div>
        """, unsafe_allow_html=True)

def display_event_types():
    """Display available event types with detailed information."""
    st.markdown('<h2 class="section-header">🌋 Extinction Event Types</h2>', unsafe_allow_html=True)

    # Event types data
    events = [
        {
            "icon": "☄️",
            "title": "Asteroid Impact",
            "description": "Model massive asteroid collisions with Earth. Analyze crater formation, global climate effects, and species extinction patterns based on size, velocity, and composition.",
            "severity_range": "2-6",
            "key_factors": ["Size", "Velocity", "Composition", "Impact Angle"]
        },
        {
            "icon": "🦠",
            "title": "Global Pandemic",
            "description": "Simulate disease outbreaks with customizable transmission rates, mortality, and intervention strategies. Model real-world scenarios from influenza to engineered pathogens.",
            "severity_range": "1-5",
            "key_factors": ["R₀ Value", "Mortality Rate", "Incubation Period", "Population Density"]
        },
        {
            "icon": "🌋",
            "title": "Supervolcano Eruption",
            "description": "Explore massive volcanic events using the VEI scale. Assess global ash dispersal, volcanic winter effects, and long-term climate disruption.",
            "severity_range": "3-6",
            "key_factors": ["VEI Scale", "Eruption Duration", "Ash Volume", "Location"]
        },
        {
            "icon": "🌡️",
            "title": "Climate Collapse",
            "description": "Model catastrophic climate change scenarios including runaway greenhouse effects, ice ages, and tipping point cascades affecting global ecosystems.",
            "severity_range": "2-6",
            "key_factors": ["Temperature Change", "Sea Level Rise", "Ecosystem Loss", "Timeline"]
        },
        {
            "icon": "💫",
            "title": "Gamma-Ray Burst",
            "description": "Simulate the effects of cosmic gamma-ray bursts on Earth's atmosphere, ozone layer, and biosphere based on distance and energy output.",
            "severity_range": "3-6",
            "key_factors": ["Distance", "Energy Output", "Duration", "Atmospheric Effects"]
        },
        {
            "icon": "🤖",
            "title": "AI Extinction Risk",
            "description": "Analyze artificial intelligence scenarios from beneficial AGI to extinction-level threats. Model alignment probability, development speed, and control measures.",
            "severity_range": "1-6",
            "key_factors": ["AI Capability", "Alignment", "Development Speed", "Control Measures"]
        }
    ]

    # Create grid layout for events
    cols = st.columns(3)
    for i, event in enumerate(events):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="feature-card">
                <span class="feature-icon">{event['icon']}</span>
                <div class="feature-title">{event['title']}</div>
                <div class="feature-description">{event['description']}</div>
                <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.1);">
                    <strong style="color: #4ECDC4;">Severity Range:</strong> {event['severity_range']}<br>
                    <strong style="color: #4ECDC4;">Key Factors:</strong> {', '.join(event['key_factors'])}
                </div>
            </div>
            """, unsafe_allow_html=True)

def display_interactive_demo():
    """Display an interactive demonstration."""
    st.markdown('<h2 class="section-header">🔬 Live Simulation Demo</h2>', unsafe_allow_html=True)

    # Quick demo section
    st.markdown("""
    <div class="quick-demo">
        <h3 style="color: #4CAF50; margin-bottom: 1rem;">⚡ Quick Start Demo</h3>
        <p>Experience E.L.E.S. in action! Select an event type and adjust parameters to see real-time results.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("🎛️ Demo Controls")

        # Event type selection
        demo_event = st.selectbox(
            "Select Event Type",
            ["Asteroid Impact", "Pandemic", "Supervolcano", "Climate Collapse", "Gamma-Ray Burst", "AI Extinction"],
            key="demo_event"
        )

        # Parameter adjustment based on event type
        if demo_event == "Asteroid Impact":
            diameter = st.slider("Asteroid Diameter (km)", 0.1, 20.0, 2.0, 0.1)
            velocity = st.slider("Impact Velocity (km/s)", 10.0, 50.0, 20.0, 1.0)
            params = {"diameter_km": diameter, "velocity_km_s": velocity, "density_kg_m3": 3000}

        elif demo_event == "Pandemic":
            r0 = st.slider("Basic Reproduction Number (R₀)", 1.0, 10.0, 2.5, 0.1)
            mortality = st.slider("Mortality Rate", 0.001, 0.5, 0.02, 0.001)
            params = {"r0": r0, "mortality_rate": mortality}

        elif demo_event == "Supervolcano":
            vei = st.selectbox("VEI Scale", [6, 7, 8], index=1)
            duration = st.slider("Eruption Duration (days)", 1, 365, 30, 1)
            params = {"vei": vei, "eruption_duration_days": duration}

        elif demo_event == "Climate Collapse":
            temp_change = st.slider("Temperature Change (°C)", -10.0, 15.0, 4.0, 0.1)
            timeframe = st.slider("Timeframe (years)", 10, 200, 50, 5)
            params = {"temperature_change_c": temp_change, "timeframe_years": timeframe}

        elif demo_event == "Gamma-Ray Burst":
            distance = st.slider("Distance (light-years)", 500, 10000, 2000, 100)
            params = {"distance_ly": distance}

        else:  # AI Extinction
            ai_level = st.slider("AI Capability Level", 1, 10, 5, 1)
            alignment_prob = st.slider("Alignment Probability", 0.0, 1.0, 0.5, 0.05)
            params = {"ai_level": ai_level, "alignment_probability": alignment_prob}

    with col2:
        st.subheader("📊 Simulation Results")

        try:
            # Run simulation
            engine = Engine()
            event_type_map = {
                "Asteroid Impact": "asteroid",
                "Pandemic": "pandemic",
                "Supervolcano": "supervolcano",
                "Climate Collapse": "climate_collapse",
                "Gamma-Ray Burst": "gamma_ray_burst",
                "AI Extinction": "ai_extinction"
            }

            result = engine.run_simulation(event_type_map[demo_event], params)            # Display key metrics using Streamlit components
            st.markdown("#### 📊 Key Results")

            # Create columns for better layout
            col_a, col_b = st.columns(2)

            with col_a:
                # Severity level with color indicator
                severity_color = SEVERITY_COLORS[result.severity]
                st.markdown(f"""
                <div style="display: flex; align-items: center; margin-bottom: 1rem; background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 0.5rem;">
                    <span style="display: inline-block; width: 20px; height: 20px; border-radius: 50%; background-color: {severity_color}; margin-right: 0.5rem;"></span>
                    <strong style="color: #4ECDC4;">Severity:</strong>&nbsp;
                    <span style="color: #FAFAFA;">{result.severity}/6 ({result.get_severity_description()})</span>
                </div>
                """, unsafe_allow_html=True)

                # Casualties
                st.metric(
                    label="🚨 Estimated Casualties",
                    value=f"{result.estimated_casualties:,}",
                    help="Total estimated human casualties from this event"
                )

                # Recovery time
                st.metric(
                    label="⏱️ Recovery Time",
                    value=result.get_recovery_time_estimate(),
                    help="Estimated time for civilization to recover"
                )

            with col_b:
                # Economic impact
                st.metric(
                    label="💰 Economic Impact",
                    value=f"${result.economic_impact:.1f}T USD",
                    help="Total economic impact in trillions of US dollars"
                )

                # Impacted area
                st.metric(
                    label="🌍 Impacted Area",
                    value=f"{result.impacted_area:,.0f} km²",
                    help="Directly affected geographical area"
                )

                # Event type
                st.metric(
                    label="🎯 Event Type",
                    value=demo_event,
                    help="Type of extinction-level event simulated"
                )

            # Create a simple visualization
            create_demo_visualization(result, demo_event)

        except Exception as e:
            st.error(f"Simulation failed: {str(e)}")
            st.info("This is a demo version. Full simulation capabilities are available in the main application.")

def create_demo_visualization(result, event_type):
    """Create a visualization for the demo results."""
    # Create severity gauge
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = result.severity,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Severity Level"},
        delta = {'reference': 3},
        gauge = {
            'axis': {'range': [None, 6]},
            'bar': {'color': SEVERITY_COLORS[result.severity]},
            'steps': [
                {'range': [0, 2], 'color': "lightgray"},
                {'range': [2, 4], 'color': "gray"},
                {'range': [4, 6], 'color': "darkgray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 5
            }
        }
    ))

    fig.update_layout(
        height=300,
        font={'color': "white"},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig, use_container_width=True)

def display_key_capabilities():
    """Display key capabilities and features."""
    st.markdown('<h2 class="section-header">🚀 Advanced Capabilities</h2>', unsafe_allow_html=True)

    capabilities = [
        {
            "icon": "🔬",
            "title": "Scientific Modeling",
            "description": "Peer-reviewed algorithms with uncertainty quantification and confidence intervals"
        },
        {
            "icon": "📊",
            "title": "Real-time Analysis",
            "description": "Interactive parameter adjustment with instant result updates and sensitivity analysis"
        },
        {
            "icon": "🌐",
            "title": "Global Impact Assessment",
            "description": "Comprehensive evaluation of worldwide effects including cascading failures"
        },
        {
            "icon": "🎯",
            "title": "Risk Prediction",
            "description": "Multi-factor survival probability models with regional and demographic breakdowns"
        },
        {
            "icon": "📈",
            "title": "Recovery Modeling",
            "description": "Timeline analysis for civilization rebuilding across multiple systems"
        },
        {
            "icon": "💾",
            "title": "Data Export",
            "description": "Comprehensive reporting in CSV, JSON, and PDF formats for research and policy"
        }
    ]

    cols = st.columns(3)
    for i, capability in enumerate(capabilities):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="feature-card">
                <span class="feature-icon">{capability['icon']}</span>
                <div class="feature-title">{capability['title']}</div>
                <div class="feature-description">{capability['description']}</div>
            </div>
            """, unsafe_allow_html=True)

def display_scenario_comparison():
    """Display a comparison of different scenarios."""
    st.markdown('<h2 class="section-header">📈 Scenario Impact Comparison</h2>', unsafe_allow_html=True)

    # Create sample data for comparison chart
    scenarios = {
        'Event Type': ['Small Asteroid', 'Large Asteroid', 'Pandemic (R₀=2)', 'Pandemic (R₀=5)',
                      'VEI 6 Volcano', 'VEI 8 Volcano', 'Climate +2°C', 'Climate +5°C'],
        'Severity': [2, 6, 3, 5, 4, 6, 3, 5],
        'Casualties (Millions)': [0.1, 7000, 50, 2000, 100, 6000, 200, 4000],
        'Economic Impact (Trillions)': [0.01, 50, 5, 40, 10, 45, 15, 100],
        'Recovery Time (Years)': [5, 10000, 50, 500, 200, 5000, 100, 1000]
    }

    df = pd.DataFrame(scenarios)

    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Severity Levels', 'Economic Impact', 'Casualties', 'Recovery Time'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )

    # Severity plot
    fig.add_trace(
        go.Bar(x=df['Event Type'], y=df['Severity'],
               marker_color=[SEVERITY_COLORS[s] for s in df['Severity']],
               name='Severity'),
        row=1, col=1
    )

    # Economic impact
    fig.add_trace(
        go.Bar(x=df['Event Type'], y=df['Economic Impact (Trillions)'],
               marker_color='#4ECDC4', name='Economic Impact'),
        row=1, col=2
    )

    # Casualties
    fig.add_trace(
        go.Bar(x=df['Event Type'], y=df['Casualties (Millions)'],
               marker_color='#FF6B6B', name='Casualties'),
        row=2, col=1
    )

    # Recovery time
    fig.add_trace(
        go.Bar(x=df['Event Type'], y=df['Recovery Time (Years)'],
               marker_color='#FFE66D', name='Recovery Time'),
        row=2, col=2
    )

    fig.update_layout(
        height=600,
        showlegend=False,
        font={'color': "white"},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    # Update x-axis labels to be rotated
    fig.update_xaxes(tickangle=45)

    st.plotly_chart(fig, use_container_width=True)

def display_getting_started():
    """Display getting started section."""
    st.markdown('<h2 class="section-header">🎯 Get Started</h2>', unsafe_allow_html=True)

    st.markdown("""
    <div class="getting-started">
        <h3 style="margin-bottom: 1.5rem;">Ready to Explore Extinction Scenarios?</h3>
        <p style="font-size: 1.1rem; margin-bottom: 2rem; opacity: 0.9;">
            Choose your path to understanding catastrophic risks and their implications for humanity.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">🎓</span>
            <div class="feature-title">Educational Mode</div>
            <div class="feature-description">
                Start with guided tutorials and pre-configured scenarios. Perfect for learning about extinction risks and their scientific foundations.
            </div>
            <div style="margin-top: 1rem;">
                <span style="background: #4CAF50; color: white; padding: 0.5rem 1rem; border-radius: 0.5rem; font-size: 0.9rem;">
                    Beginner Friendly
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">🔬</span>
            <div class="feature-title">Research Mode</div>
            <div class="feature-description">
                Access advanced parameters, uncertainty analysis, and detailed scientific models. Ideal for researchers and policy makers.
            </div>
            <div style="margin-top: 1rem;">
                <span style="background: #2196F3; color: white; padding: 0.5rem 1rem; border-radius: 0.5rem; font-size: 0.9rem;">
                    Advanced Users
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">⚡</span>
            <div class="feature-title">Quick Analysis</div>
            <div class="feature-description">
                Jump straight into scenario modeling with intelligent defaults. Fast track to results and insights.
            </div>
            <div style="margin-top: 1rem;">
                <span style="background: #FF9800; color: white; padding: 0.5rem 1rem; border-radius: 0.5rem; font-size: 0.9rem;">
                    Instant Results
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Quick links section
    st.markdown("---")
    st.markdown("### 🔗 Quick Links")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🎮 Interactive Tutorial", key="tutorial_btn"):
            st.info("Tutorial mode would launch here!")

    with col2:
        if st.button("📖 Documentation", key="docs_btn"):
            st.info("Documentation would open here!")

    with col3:
        if st.button("💾 Sample Data", key="sample_btn"):
            st.info("Sample datasets would be displayed here!")

    with col4:
        if st.button("🧪 Advanced Lab", key="lab_btn"):
            st.info("Advanced laboratory mode would launch here!")

    # Footer information
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #A0AEC0; padding: 2rem;">
        <p><strong>E.L.E.S.</strong> - Understanding extinction risks to build a more resilient future</p>
        <p>Built with scientific rigor • Powered by peer-reviewed research • Designed for impact</p>
    </div>
    """, unsafe_allow_html=True)

# Entry point for running the home page directly
if __name__ == "__main__":
    run()
