import streamlit as st
import json
import yaml
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import math
from pathlib import Path
import sys
import os

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from eles_core.engine import Engine
from eles_core.event_types.asteroid import AsteroidImpact
from eles_core.event_types.supervolcano import Supervolcano
from eles_core.event_types.pandemic import Pandemic
from config.constants import SEVERITY_LEVELS, SEVERITY_COLORS


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="E.L.E.S. - Extinction-Level Event Simulator",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .event-card {
        background-color: #262730;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .severity-box {
        padding: 0.5rem;
        border-radius: 0.25rem;
        text-align: center;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown('<h1 class="main-header">🌍 E.L.E.S.</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center;">Extinction-Level Event Simulator</h3>', unsafe_allow_html=True)

    # Sidebar for event selection
    with st.sidebar:
        st.header("🎛️ Simulation Controls")

        event_type = st.selectbox(
            "Select Event Type:",
            ["asteroid", "supervolcano", "pandemic", "gamma_ray_burst", "climate_collapse", "ai_extinction"],
            format_func=lambda x: x.replace("_", " ").title()
        )

        st.markdown("---")

        # Event-specific parameters
        if event_type == "asteroid":
            params = get_asteroid_parameters()
        elif event_type == "supervolcano":
            params = get_supervolcano_parameters()
        elif event_type == "pandemic":
            params = get_pandemic_parameters()
        else:
            params = get_default_parameters(event_type)

        # Run simulation button
        if st.button("🚀 Run Simulation", type="primary"):
            run_simulation(event_type, params)

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("📊 Simulation Results")
        display_results()

    with col2:
        st.header("ℹ️ Event Information")
        display_event_info(event_type)

    # Footer
    st.markdown("---")
    st.markdown("*E.L.E.S. - Educational simulation for understanding extinction-level events*")


def get_asteroid_parameters():
    """Get asteroid impact parameters from user input."""
    st.subheader("☄️ Asteroid Parameters")

    # Preset options
    preset = st.selectbox(
        "Preset Scenarios:",
        ["Custom", "Tunguska (1908)", "Chicxulub (Dinosaurs)", "2km Metal Asteroid", "Apophis"]
    )

    if preset == "Tunguska (1908)":
        diameter = 0.06
        density = 3000
        velocity = 20
    elif preset == "Chicxulub (Dinosaurs)":
        diameter = 10
        density = 3000
        velocity = 20
    elif preset == "2km Metal Asteroid":
        diameter = 2
        density = 8000
        velocity = 20
    elif preset == "Apophis":
        diameter = 0.37
        density = 3000
        velocity = 20
    else:
        diameter = st.slider("Diameter (km)", 0.01, 50.0, 1.0, 0.01)
        density = st.slider("Density (kg/m³)", 1000, 10000, 3000, 100)
        velocity = st.slider("Velocity (km/s)", 10, 50, 20, 1)

    if preset != "Custom":
        st.write(f"**Diameter:** {diameter} km")
        st.write(f"**Density:** {density:,} kg/m³")
        st.write(f"**Velocity:** {velocity} km/s")

    target_type = st.selectbox("Impact Location:", ["continental", "ocean", "urban"])

    return {
        "diameter_km": diameter,
        "density_kg_m3": density,
        "velocity_km_s": velocity,
        "target_type": target_type
    }


def get_supervolcano_parameters():
    """Get supervolcano parameters from user input."""
    st.subheader("🌋 Supervolcano Parameters")

    volcano_name = st.selectbox(
        "Volcano:",
        ["Yellowstone", "Toba", "Campi Flegrei", "Long Valley", "Custom"]
    )

    if volcano_name == "Custom":
        volcano_name = st.text_input("Volcano Name:", "Custom Volcano")

    vei = st.slider("Volcanic Explosivity Index (VEI):", 4, 8, 6, 1)

    st.write(f"**VEI {vei}:** {get_vei_description(vei)}")

    return {
        "name": volcano_name,
        "vei": vei
    }


def get_pandemic_parameters():
    """Get pandemic parameters from user input."""
    st.subheader("🦠 Pandemic Parameters")

    preset = st.selectbox(
        "Preset Scenarios:",
        ["Custom", "COVID-19", "Spanish Flu", "MERS", "Hypothetical Severe"]
    )

    if preset == "COVID-19":
        r0 = 2.5
        mortality = 0.01
    elif preset == "Spanish Flu":
        r0 = 2.0
        mortality = 0.03
    elif preset == "MERS":
        r0 = 0.8
        mortality = 0.35
    elif preset == "Hypothetical Severe":
        r0 = 5.0
        mortality = 0.2
    else:
        r0 = st.slider("Basic Reproduction Number (R₀):", 0.5, 10.0, 2.5, 0.1)
        mortality = st.slider("Mortality Rate:", 0.001, 0.5, 0.02, 0.001)

    if preset != "Custom":
        st.write(f"**R₀:** {r0}")
        st.write(f"**Mortality Rate:** {mortality:.1%}")

    return {
        "r0": r0,
        "mortality_rate": mortality
    }


def get_default_parameters(event_type):
    """Get default parameters for other event types."""
    if event_type == "gamma_ray_burst":
        st.subheader("💫 Gamma-Ray Burst Parameters")
        distance = st.slider("Distance (light-years):", 100, 10000, 1000, 100)
        return {"distance_ly": distance}

    elif event_type == "climate_collapse":
        st.subheader("🌡️ Climate Collapse Parameters")
        temp_change = st.slider("Temperature Change (°C):", -20, 20, -5, 1)
        return {"temperature_change_c": temp_change}

    elif event_type == "ai_extinction":
        st.subheader("🤖 AI Extinction Parameters")
        ai_level = st.slider("AI Capability Level:", 1, 10, 5, 1)
        return {"ai_level": ai_level}

    return {}


def run_simulation(event_type, params):
    """Run the simulation and store results in session state."""
    try:
        engine = Engine()
        result = engine.run_simulation(event_type, params)

        st.session_state.simulation_result = result
        st.session_state.event_type = event_type
        st.success("✅ Simulation completed successfully!")

    except Exception as e:
        st.error(f"❌ Simulation failed: {str(e)}")


def display_results():
    """Display simulation results."""
    if 'simulation_result' not in st.session_state:
        st.info("👆 Configure parameters in the sidebar and run a simulation to see results.")
        return

    result = st.session_state.simulation_result
    event_type = st.session_state.event_type

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        severity_color = SEVERITY_COLORS.get(result.severity, "#808080")
        st.markdown(f"""
        <div class="severity-box" style="background-color: {severity_color}; color: white;">
            Severity: {result.severity}/6<br>
            {result.get_severity_description()}
        </div>
        """, unsafe_allow_html=True)

    with col2:
        casualties = getattr(result, 'estimated_casualties', 0)
        st.metric("Estimated Casualties", f"{casualties:,}")

    with col3:
        economic_impact = getattr(result, 'economic_impact', 0)
        st.metric("Economic Impact", f"${economic_impact:.1f}B")

    with col4:
        recovery_time = result.get_recovery_time_estimate()
        st.metric("Recovery Time", recovery_time)

    # Detailed results
    st.subheader("📋 Detailed Results")

    # Create tabs for different result views
    tab1, tab2, tab3, tab4 = st.tabs(["Summary", "Visualizations", "Risk Factors", "Raw Data"])

    with tab1:
        display_summary_tab(result)

    with tab2:
        display_visualizations_tab(result, event_type)

    with tab3:
        display_risk_factors_tab(result)

    with tab4:
        display_raw_data_tab(result)


def display_summary_tab(result):
    """Display summary information."""
    summary = result.summary()

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Event Type:**", summary['event_type'].replace('_', ' ').title())
        st.write("**Severity Level:**", f"{summary['severity']}/6 - {summary['severity_description']}")
        st.write("**Estimated Casualties:**", f"{summary['estimated_casualties']:,}")
        st.write("**Economic Impact:**", f"${summary['economic_impact_billion_usd']:.1f} billion USD")

    with col2:
        st.write("**Recovery Time:**", summary['recovery_time_estimate'])
        st.write("**Impacted Area:**", f"{summary['impacted_area_km2']:,.0f} km²")

        if 'global_effects' in summary and summary['global_effects']:
            st.write("**Global Effects:**")
            for key, value in summary['global_effects'].items():
                st.write(f"- **{key.title()}:** {value}")


def display_visualizations_tab(result, event_type):
    """Display visualizations."""
    if event_type == "asteroid":
        display_asteroid_visualizations(result)
    elif event_type == "pandemic":
        display_pandemic_visualizations(result)
    elif event_type == "supervolcano":
        display_supervolcano_visualizations(result)
    else:
        st.info("Visualizations not yet implemented for this event type.")


def display_asteroid_visualizations(result):
    """Display asteroid-specific visualizations."""
    sim_data = result.simulation_data

    col1, col2 = st.columns(2)

    with col1:
        # Energy comparison chart
        energies = {
            'This Impact': sim_data.get('impact_energy', 0),
            'Tunguska (1908)': 1e16,
            'Chicxulub': 1e23,
            'Tsar Bomba': 2.1e17
        }

        fig = px.bar(
            x=list(energies.keys()),
            y=list(energies.values()),
            title="Energy Comparison (Joules)",
            log_y=True
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Damage zones
        crater_diameter = sim_data.get('crater_diameter_km', 0)
        blast_severe = sim_data.get('blast_radius_severe_km', 0)
        blast_moderate = sim_data.get('blast_radius_moderate_km', 0)

        zones_data = pd.DataFrame({
            'Zone': ['Crater', 'Severe Blast', 'Moderate Blast'],
            'Radius (km)': [crater_diameter/2, blast_severe, blast_moderate],
            'Area (km²)': [3.14159*(crater_diameter/2)**2, 3.14159*blast_severe**2, 3.14159*blast_moderate**2]
        })

        fig = px.pie(zones_data, values='Area (km²)', names='Zone', title='Damage Zones')
        st.plotly_chart(fig, use_container_width=True)


def display_pandemic_visualizations(result):
    """Display pandemic-specific visualizations."""
    sim_data = result.simulation_data

    # Epidemic curve simulation (simplified)
    duration = sim_data.get('epidemic_duration_days', 365)
    peak_day = sim_data.get('peak_day', duration//3)
    peak_infected = sim_data.get('peak_infected', 0)

    # Generate simplified epidemic curve
    days = list(range(0, duration, 10))
    infected = []

    for day in days:
        if day < peak_day:
            # Rising phase
            infected.append(int(peak_infected * (day / peak_day) ** 2))
        else:
            # Declining phase
            decay = math.exp(-(day - peak_day) / (duration - peak_day) * 3)
            infected.append(int(peak_infected * decay))

    fig = px.line(x=days, y=infected, title="Epidemic Curve",
                  labels={'x': 'Days', 'y': 'Active Infections'})
    st.plotly_chart(fig, use_container_width=True)


def display_supervolcano_visualizations(result):
    """Display supervolcano-specific visualizations."""
    sim_data = result.simulation_data

    # VEI comparison
    vei_data = {
        'VEI 4': 0.1,
        'VEI 5': 1,
        'VEI 6': 10,
        'VEI 7': 100,
        'VEI 8': 1000,
        f"This Eruption (VEI {sim_data.get('vei', 6)})": sim_data.get('magma_volume_km3', 0)
    }

    fig = px.bar(
        x=list(vei_data.keys()),
        y=list(vei_data.values()),
        title="Magma Volume Comparison (km³)",
        log_y=True
    )
    st.plotly_chart(fig, use_container_width=True)


def display_risk_factors_tab(result):
    """Display risk factors."""
    risk_factors = result.get_risk_factors()

    if risk_factors:
        st.subheader("⚠️ Key Risk Factors")
        for factor in risk_factors:
            st.write(f"• {factor}")
    else:
        st.info("No specific risk factors identified for this scenario.")


def display_raw_data_tab(result):
    """Display raw simulation data."""
    st.subheader("🔍 Raw Simulation Data")
    st.json(result.simulation_data)

    # Download button
    json_str = result.to_json()
    st.download_button(
        label="📥 Download Results (JSON)",
        data=json_str,
        file_name=f"eles_simulation_{result.event_type}.json",
        mime="application/json"
    )


def display_event_info(event_type):
    """Display information about the selected event type."""
    event_info = {
        "asteroid": {
            "title": "☄️ Asteroid Impact",
            "description": "Asteroid impacts can cause devastation ranging from local damage to global extinction events. The size, composition, and velocity of the asteroid determine the severity of effects.",
            "examples": ["Tunguska (1908)", "Chicxulub (66 MYA)", "Meteor Crater, Arizona"],
            "timeframe": "Instantaneous impact, effects last years to millennia"
        },
        "supervolcano": {
            "title": "🌋 Supervolcanic Eruption",
            "description": "Supervolcanoes can inject massive amounts of ash and sulfur into the atmosphere, causing global climate effects and 'volcanic winter'.",
            "examples": ["Yellowstone", "Toba (74,000 years ago)", "Campi Flegrei"],
            "timeframe": "Effects develop over months to years"
        },
        "pandemic": {
            "title": "🦠 Global Pandemic",
            "description": "Highly contagious and deadly pathogens can spread globally, potentially causing societal collapse through direct mortality and system breakdown.",
            "examples": ["Spanish Flu (1918)", "Black Death", "COVID-19"],
            "timeframe": "Spreads over months, effects last years"
        }
    }

    info = event_info.get(event_type, {
        "title": event_type.replace("_", " ").title(),
        "description": "Information not available.",
        "examples": [],
        "timeframe": "Variable"
    })

    st.markdown(f"### {info['title']}")
    st.write(info['description'])

    if info['examples']:
        st.write("**Historical Examples:**")
        for example in info['examples']:
            st.write(f"• {example}")

    st.write(f"**Timeframe:** {info['timeframe']}")


def get_vei_description(vei):
    """Get VEI description."""
    descriptions = {
        4: "Cataclysmic - Column height 25-35 km",
        5: "Paroxysmal - Column height 25-35 km",
        6: "Colossal - Column height >35 km",
        7: "Super-colossal - Column height >35 km",
        8: "Mega-colossal - Column height >35 km"
    }
    return descriptions.get(vei, "Unknown")


if __name__ == "__main__":
    main()
