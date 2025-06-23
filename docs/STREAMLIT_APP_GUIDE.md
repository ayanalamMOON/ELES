# E.L.E.S. Streamlit App - User Guide

## 🌍 Enhanced Extinction-Level Event Simulator

The E.L.E.S. Streamlit app now supports **all simulation scenarios** with **custom parameter changes**. Here's how to use the enhanced features:

## 🚀 Getting Started

1. **Start the app:**

   ```bash
   cd /path/to/ELES
   streamlit run ui/streamlit_app.py
   ```

2. **Open in browser:** <http://localhost:8501>

## 🎛️ Supported Event Types

### ☄️ Asteroid Impact

- **Custom Parameters:**
  - Diameter (0.01 - 50 km)
  - Density (1,000 - 10,000 kg/m³)
  - Velocity (10 - 50 km/s)
  - Target type (continental, ocean, urban)

- **Preset Scenarios:**
  - Tunguska (1908): 60m asteroid
  - Chicxulub (Dinosaurs): 10km asteroid
  - 2km Metal Asteroid: Dense iron asteroid
  - Apophis: 370m near-Earth asteroid

### 🦠 Global Pandemic

- **Custom Parameters:**
  - Basic Reproduction Number (R₀: 0.5 - 10.0)
  - Mortality Rate (0.1% - 50%)

- **Preset Scenarios:**
  - COVID-19: R₀=2.5, mortality=1%
  - Spanish Flu: R₀=2.0, mortality=3%
  - MERS: R₀=0.8, mortality=35%
  - Hypothetical Severe: R₀=5.0, mortality=20%

### 🌋 Supervolcanic Eruption

- **Custom Parameters:**
  - Volcano name (preset or custom)
  - Volcanic Explosivity Index (VEI 4-8)

- **Preset Volcanoes:**
  - Yellowstone, Toba, Campi Flegrei, Long Valley

### 🌡️ Climate Collapse

- **Custom Parameters:**
  - Temperature Change (-20°C to +20°C)

### 💫 Gamma-Ray Burst

- **Custom Parameters:**
  - Distance from Earth (100 - 10,000 light-years)

### 🤖 AI Extinction Risk

- **Custom Parameters:**
  - AI Capability Level (1-10 scale)

## 📊 Enhanced Visualizations

Each event type now includes specific visualizations:

### Asteroid Impacts

- Energy comparison charts
- Damage zone analysis (crater, blast radii)
- Historical impact comparisons

### Pandemics

- Epidemic curve simulation
- Timeline of infection spread
- Peak infection analysis

### Supervolcanoes

- VEI magnitude comparisons
- Magma volume analysis
- Historical eruption context

### Climate Collapse

- Temperature change impacts
- Sectoral impact analysis (agriculture, sea level, etc.)

### Gamma-Ray Bursts

- Distance effect modeling
- Radiation exposure analysis
- Ozone depletion calculations

### AI Extinction

- Capability level progression
- Risk factor analysis
- Control difficulty assessment

## 🎯 How Parameters Affect Results

### Severity Calculation

The app now calculates severity (1-6 scale) based on:

- **Asteroid:** Impact energy (determines global vs local effects)
- **Pandemic:** Total estimated deaths
- **Supervolcano:** VEI scale rating
- **Climate:** Magnitude of temperature change
- **GRB:** Distance from Earth
- **AI:** Capability level and risk factors

### Parameter Validation

- All parameters are validated for realistic ranges
- Edge cases are handled gracefully
- Extreme values show appropriate warnings

## 📋 Using the Interface

1. **Select Event Type:** Choose from dropdown in sidebar
2. **Adjust Parameters:** Use sliders and inputs for custom values
3. **Choose Presets:** Quick access to historical/reference scenarios
4. **Run Simulation:** Click "Run Simulation" button
5. **View Results:** Explore tabs for summary, visualizations, risk factors, and raw data

## 📈 Result Interpretation

### Summary Tab

- Event overview and severity rating
- Casualty estimates and economic impact
- Recovery time projections
- Affected area calculations

### Visualizations Tab

- Event-specific charts and graphs
- Comparative analysis with historical events
- Impact zone mapping

### Risk Factors Tab

- Key hazards and secondary effects
- Vulnerability assessments
- Mitigation considerations

### Raw Data Tab

- Complete simulation parameters
- Detailed calculation results
- JSON export for further analysis

## 🔄 Testing Different Scenarios

### Recommended Test Scenarios

1. **Compare Asteroid Sizes:**
   - Run small (0.1km) vs large (10km) asteroids
   - Compare density effects (rock vs metal)
   - Test different impact locations

2. **Pandemic Severity Scaling:**
   - Low transmission, high mortality (MERS-like)
   - High transmission, low mortality (seasonal flu)
   - Severe scenario (high transmission + mortality)

3. **Supervolcano Scale:**
   - VEI 6 (regional effects)
   - VEI 7 (continental effects)
   - VEI 8 (global catastrophe)

4. **Climate Extremes:**
   - Moderate cooling (-5°C)
   - Severe ice age (-15°C)
   - Runaway greenhouse (+10°C)

## ⚡ Performance Notes

- Simulations run in real-time (< 1 second)
- All visualizations generate dynamically
- Parameter changes immediately affect results
- Consistent results across multiple runs with same parameters

## 🔧 Troubleshooting

- **Slow loading:** Check network connection for external data
- **Visualization errors:** Refresh browser or restart app
- **Parameter limits:** Use suggested ranges for realistic results
- **Performance:** Close other browser tabs for better responsiveness

## 📱 Mobile Compatibility

The app is responsive and works on tablets/mobile devices, though desktop is recommended for the best visualization experience.

---

**🎯 Key Achievement:** The E.L.E.S. Streamlit app now successfully supports all simulation scenarios with full custom parameter functionality, comprehensive visualizations, and professional presentation suitable for educational and research purposes.
