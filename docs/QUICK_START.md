# Quick Start Guide

Get up and running with **E.L.E.S. (Extinction-Level Event Simulator)** in 5 minutes!

## 🚀 Prerequisites

Before starting, ensure you have:

- Python 3.8+ installed
- Git (for cloning the repository)
- 4GB+ RAM available

## ⚡ 5-Minute Setup

### 1. Install E.L.E.S. (2 minutes)

```bash
# Clone the repository
git clone https://github.com/your-org/ELES.git
cd ELES

# Quick install (Windows)
install.bat

# Quick install (macOS/Linux)
chmod +x install.sh && ./install.sh
```

### 2. Launch the Web App (1 minute)

```bash
# Windows
launch.bat

# macOS/Linux
./launch.sh
```

The app will open automatically at `http://localhost:8501`

### 3. Run Your First Simulation (2 minutes)

1. **Select Event Type**: Choose "asteroid" from the dropdown
2. **Set Parameters**:
   - Diameter: 1.0 km
   - Density: 3000 kg/m³
   - Velocity: 20 km/s
3. **Click "Run Simulation"**
4. **Explore Results**: Check the Summary, Visualizations, and Risk Factors tabs

🎉 **Congratulations!** You've successfully run your first extinction-level event simulation.

## 🎯 What You Can Do Next

### Try Different Scenarios

#### Small Asteroid (Tunguska-like)

- Event Type: Asteroid
- Diameter: 0.06 km
- Expected: Local impact, minimal casualties

#### Global Pandemic

- Event Type: Pandemic
- R₀: 3.0
- Mortality Rate: 2%
- Expected: Millions of casualties, economic disruption

#### Supervolcano Eruption

- Event Type: Supervolcano
- Volcano: Yellowstone
- VEI: 7
- Expected: Continental effects, climate impact

#### Climate Catastrophe

- Event Type: Climate Collapse
- Temperature Change: -8°C
- Expected: Global ice age scenario

### Explore Features

- **Preset Scenarios**: Quick access to historical events
- **Custom Parameters**: Adjust any simulation variable
- **Interactive Visualizations**: Charts update in real-time
- **Data Export**: Download results as JSON

## 📊 Understanding Results

### Severity Scale (1-6)

- **1-2**: Local to regional impact
- **3-4**: Continental to global effects
- **5-6**: Civilization-threatening to extinction-level

### Key Metrics

- **Casualties**: Estimated human deaths
- **Economic Impact**: Financial damage in billions USD
- **Recovery Time**: How long to rebuild/recover

### Visualization Tabs

- **Summary**: Quick overview and key statistics
- **Visualizations**: Charts and graphs specific to event type
- **Risk Factors**: Secondary effects and hazards
- **Raw Data**: Complete simulation parameters and results

## 🔧 Common Use Cases

### Educational

- **Compare event severities**: Run different scenarios with varying parameters
- **Historical analysis**: Use preset scenarios based on real events
- **Risk assessment**: Understand potential future threats

### Research

- **Parameter sensitivity**: See how changes affect outcomes
- **Scenario planning**: Model different disaster preparedness strategies
- **Data analysis**: Export results for further analysis

### Demonstration

- **Interactive presentations**: Real-time parameter adjustment
- **Comparative studies**: Side-by-side scenario comparisons
- **Public engagement**: Accessible science communication

## 💡 Pro Tips

### Efficient Workflow

1. **Start with presets** to understand typical scenarios
2. **Make incremental changes** to see parameter effects
3. **Use the severity scale** to compare different event types
4. **Export data** for detailed analysis outside the app

### Parameter Guidelines

- **Asteroid**: Size matters most - small changes in diameter create large impact differences
- **Pandemic**: R₀ and mortality rate work together - high transmission + high mortality = worst case
- **Supervolcano**: VEI scale is logarithmic - each level up is ~10x more severe
- **Climate**: Temperature changes >5°C typically cause civilization-level impacts

### Troubleshooting Quick Fixes

- **App won't start**: Try a different port with `--server.port 8502`
- **Slow performance**: Close other browser tabs and applications
- **Visualization errors**: Refresh the browser page
- **Installation issues**: Check you're in the right directory and Python version

## 📚 Next Steps

### Learn More

- **[Streamlit App Guide](STREAMLIT_APP_GUIDE.md)**: Complete interface documentation
- **[Event Types](EVENT_TYPES.md)**: Scientific details on each simulation type
- **[API Reference](API_REFERENCE.md)**: Use E.L.E.S. programmatically

### Get Involved

- **[Contributing Guide](CONTRIBUTING.md)**: Help improve E.L.E.S.
- **[Development Setup](DEVELOPMENT.md)**: Set up a development environment

### Need Help?

- **[FAQ](FAQ.md)**: Common questions and answers
- **[Troubleshooting](TROUBLESHOOTING.md)**: Detailed problem-solving guide

## 🎬 Demo Scenarios to Try

### Beginner-Friendly

1. **Apophis Asteroid** (preset) - Shows a realistic near-miss scenario
2. **COVID-19 Pandemic** (preset) - Familiar reference point
3. **VEI 6 Supervolcano** - Regional impact example

### Advanced

1. **Chicxulub-scale Impact** - The dinosaur extinction event
2. **Spanish Flu + Modern Population** - Historical pandemic scaled up
3. **Runaway Climate Change** (+10°C) - Extreme warming scenario

### Comparative Studies

1. **Asteroid Size Comparison**: 0.1km vs 1km vs 10km
2. **Pandemic Severity Scaling**: R₀ 1.5 vs 3.0 vs 6.0
3. **Climate Sensitivity**: -3°C vs -8°C vs -15°C

---

**Welcome to E.L.E.S.! Start exploring the science of extinction-level events.** 🌍
