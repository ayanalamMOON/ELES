# E.L.E.S. Frequently Asked Questions (FAQ)

## 🎯 General Questions

### What is E.L.E.S.?

E.L.E.S. (Extinction-Level Event Simulator) is a comprehensive, scientifically-grounded simulation framework for modeling and analyzing various extinction-level events. It supports 6 event types: asteroid impacts, pandemics, supervolcanoes, climate collapse, gamma-ray bursts, and AI extinction risks.

### What can I do with E.L.E.S.?

- **Model realistic scenarios** based on peer-reviewed research
- **Assess risk levels** using comprehensive multi-factor analysis
- **Predict survival rates** and recovery times
- **Visualize complex data** through interactive charts
- **Export findings** for research and educational purposes

### Is E.L.E.S. scientifically accurate?

Yes! E.L.E.S. is based on peer-reviewed research, empirical data, and realistic parameter ranges. The models include uncertainty quantification and are validated against historical events.

## 📊 Using the Simulator

### How do I start the simulation?

There are three ways to use E.L.E.S.:

1. **Web Interface (Recommended):**

   ```bash
   streamlit run ui/streamlit_app.py
   ```

   Then open <http://localhost:8501>

2. **Command Line Interface:**

   ```bash
   python cli/main.py asteroid --diameter 2 --density 3000 --velocity 20
   ```

3. **Python API:**

   ```python
   from eles_core.engine import Engine
   engine = Engine()
   result = engine.run_simulation('asteroid', {'diameter_km': 2.0})
   ```

### What event types are supported?

E.L.E.S. supports 6 extinction-level event types:

- **☄️ Asteroid Impact** - Size, density, velocity, target type
- **🦠 Global Pandemic** - R₀ value, mortality rate
- **🌋 Supervolcanic Eruption** - VEI scale, volcano selection
- **🌡️ Climate Collapse** - Temperature change magnitude
- **💫 Gamma-Ray Burst** - Distance from Earth
- **🤖 AI Extinction Risk** - AI capability level

### How do I interpret the severity scale?

The severity scale ranges from 1-6:

1. **Minimal Impact** - Local effects only
2. **Local Disaster** - City/regional impact
3. **Regional Catastrophe** - Multi-state/province effects
4. **Continental Crisis** - Continent-wide impact
5. **Global Catastrophe** - Worldwide effects
6. **Extinction-Level Event** - Threatens human survival

### Can I use custom parameters?

Yes! All event types support custom parameter input:

- **Asteroid**: Diameter (0.01-50 km), density, velocity, target type
- **Pandemic**: R₀ (0.5-10.0), mortality rate (0.1%-50%)
- **Supervolcano**: VEI level (4-8), volcano selection
- **Climate**: Temperature change (-20°C to +20°C)
- **Gamma-Ray Burst**: Distance (100-10,000 light-years)
- **AI Extinction**: Capability level (1-10 scale)

### Are there preset scenarios?

Yes! E.L.E.S. includes historically-based presets:

**Asteroid Presets:**

- Tunguska (1908): 60m asteroid
- Chicxulub (Dinosaurs): 10km asteroid
- Apophis: 370m near-Earth asteroid

**Pandemic Presets:**

- COVID-19: R₀=2.5, mortality=1%
- Spanish Flu: R₀=2.0, mortality=3%
- MERS: R₀=0.8, mortality=35%

**Volcano Presets:**

- Yellowstone, Toba, Campi Flegrei, Long Valley

## 🔬 Technical Questions

### What programming language is E.L.E.S. written in?

E.L.E.S. is written in Python 3.8+ and uses scientific libraries like NumPy, SciPy, and Matplotlib for calculations and visualizations.

### What are the system requirements?

- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 1GB available space
- **OS**: Windows, macOS, or Linux

### How accurate are the casualty estimates?

Casualty estimates are based on:

- Population density models
- Historical event data
- Peer-reviewed impact studies
- Conservative scaling relationships

Results should be considered as order-of-magnitude estimates for educational and research purposes.

### How fast are the simulations?

- **Web Interface**: Real-time (< 1 second per simulation)
- **CLI**: Instantaneous for single scenarios
- **Batch Processing**: Depends on number of scenarios

### Can I export simulation results?

Yes! Results can be exported in multiple formats:

- **JSON**: Complete simulation data
- **CSV**: Tabular summary data
- **Images**: Visualization charts
- **PDF**: Summary reports (via print function)

## 🎨 Visualization Questions

### What visualizations are available?

Each event type includes specific visualizations:

- **Asteroid**: Energy comparison, damage zones, historical comparisons
- **Pandemic**: Epidemic curves, infection spread, peak analysis
- **Supervolcano**: VEI comparisons, magma volume, eruption history
- **Climate**: Temperature impacts, sectoral analysis
- **Gamma-Ray Burst**: Distance effects, radiation exposure
- **AI Extinction**: Capability progression, risk factors

### Can I customize the visualizations?

Currently, visualizations are automatically generated based on simulation parameters. Future versions may include customization options.

### Why do some visualizations take time to load?

Large-scale visualizations (especially maps and 3D plots) may take a few seconds to render. This is normal and depends on your system's graphics capabilities.

## 📱 Interface Questions

### Does E.L.E.S. work on mobile devices?

The Streamlit web interface is responsive and works on tablets and mobile devices, though desktop is recommended for the best visualization experience.

### Can I use E.L.E.S. offline?

Yes! Once installed, E.L.E.S. works completely offline. No internet connection is required for simulations.

### How do I save my simulation sessions?

Currently, you can export individual simulation results. Session saving is planned for future versions.

## 🔧 Installation Questions

### How do I install E.L.E.S.?

See the [Installation Guide](INSTALLATION.md) for detailed instructions. Quick start:

```bash
git clone https://github.com/your-username/ELES.git
cd ELES
pip install -r requirements.txt
streamlit run ui/streamlit_app.py
```

### Do I need special permissions to install?

No special permissions are required. E.L.E.S. can be installed in a virtual environment without administrator access.

### Can I use conda instead of pip?

Yes! E.L.E.S. is compatible with conda environments:

```bash
conda create -n eles python=3.8
conda activate eles
pip install -r requirements.txt
```

## 📚 Educational Use

### Is E.L.E.S. suitable for teaching?

Yes! E.L.E.S. is designed for educational use:

- **Interactive exploration** of scientific concepts
- **Visual learning** through charts and graphs
- **Quantitative analysis** of risk factors
- **Historical context** through preset scenarios

### What age group is E.L.E.S. appropriate for?

E.L.E.S. is suitable for:

- **High school** (ages 15+) - Basic concepts and preset scenarios
- **University** - Advanced parameters and research applications
- **Graduate/Research** - Custom analysis and data export

### Are there lesson plans available?

Currently, the documentation provides guidance for educational use. Formal lesson plans are being developed.

## 🤝 Contributing Questions

### How can I contribute to E.L.E.S.?

See the [Contributing Guide](CONTRIBUTING.md) for details. You can:

- Report bugs and issues
- Suggest new features
- Submit code improvements
- Add new event types
- Improve documentation

### Can I add new event types?

Yes! E.L.E.S. is designed to be extensible. New event types can be added by:

1. Creating a new event class in `eles_core/event_types/`
2. Registering it in the engine
3. Adding UI components
4. Including visualizations

### Is E.L.E.S. open source?

Yes! E.L.E.S. is released under the MIT License, making it free for educational, research, and commercial use.

## 📊 Data Questions

### Where does the scientific data come from?

E.L.E.S. uses data from:

- Peer-reviewed scientific publications
- NASA and ESA databases
- Historical event records
- Geological surveys
- Epidemiological studies

### How often is the data updated?

The core scientific models are stable, but data updates are released with new versions of E.L.E.S.

### Can I use my own data?

Yes! Advanced users can modify the data files in the `data/` directory or extend the event classes to use custom datasets.

## 🔮 Future Development

### What features are planned?

Future enhancements include:

- **More event types** (solar flares, supernovae)
- **Geographic specificity** (location-based simulations)
- **Economic modeling** (detailed economic impact analysis)
- **Mitigation strategies** (intervention scenario modeling)
- **Batch processing** (multiple scenario comparison)

### How do I request new features?

Create an issue on the project repository with the "feature request" label, describing:

- The proposed feature
- Use cases and benefits
- Implementation suggestions (if any)

### When will the next version be released?

E.L.E.S. follows a regular development cycle. Check the [Changelog](CHANGELOG.md) and project repository for update schedules.

---

## 💡 Still Have Questions?

If your question isn't answered here:

1. Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
2. Review the [Installation Guide](INSTALLATION.md)
3. Consult the [API Documentation](API_REFERENCE.md)
4. Create an issue on the project repository
5. Contact the development team

**Remember**: E.L.E.S. is designed to be educational and thought-provoking. The goal is to help understand and prepare for potential risks, not to cause alarm or distress.
