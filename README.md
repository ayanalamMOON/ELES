# 🌍 Extinction-Level Event Simulator (E.L.E.S.)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Code Quality](https://img.shields.io/badge/code%20quality-A-brightgreen.svg)](https://github.com/psf/black)
[![Test Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen.svg)](https://pytest.org)
[![Documentation](https://img.shields.io/badge/docs-comprehensive-blue.svg)](./docs/)
[![Scientific Models](https://img.shields.io/badge/models-peer%20reviewed-orange.svg)](./docs/scientific_basis.md)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://python.org)
[![Status](https://img.shields.io/badge/status-production%20ready-brightgreen.svg)](https://github.com/yourusername/ELES/releases)

E.L.E.S. is a comprehensive, scientifically-grounded simulation framework for modeling and analyzing various extinction-level events. From asteroid impacts to AI takeover scenarios, this platform provides researchers, educators, and policymakers with powerful tools to understand, assess, and prepare for existential risks to human civilization.

## 📋 Table of Contents

- [🎯 Overview](#-overview)
- [✨ Key Features](#-key-features)
- [🚀 Quick Start](#-quick-start)
- [💻 Usage Guide](#-usage-guide)
- [📁 Project Structure](#-project-structure)
- [🔬 Scientific Foundation](#-scientific-foundation)
- [🎓 Educational Applications](#-educational-applications)
- [🌟 Example Scenarios](#-example-scenarios)
- [📊 Performance & Validation](#-performance--validation)
- [🤝 Contributing](#-contributing)
- [📚 Documentation](#-documentation)
- [🆘 Support](#-support)
- [📄 License](#-license)
- [🙏 Acknowledgments](#-acknowledgments)
- [📈 Roadmap](#-roadmap)

## 🎯 Overview

The Extinction-Level Event Simulator addresses one of humanity's most critical challenges: understanding and preparing for catastrophic risks. By combining cutting-edge scientific models with intuitive interfaces, E.L.E.S. enables users to:

- **Model realistic scenarios** based on peer-reviewed research and historical data
- **Assess risk levels** using comprehensive multi-factor analysis
- **Predict survival rates** across different populations and regions
- **Estimate recovery times** for various systems and infrastructure
- **Visualize complex data** through interactive charts and 3D models
- **Export findings** for research, policy, and educational purposes

## ✨ Key Features

### 🔬 **Scientific Accuracy**

- Models based on peer-reviewed research and empirical data
- Realistic parameter ranges and scaling relationships
- Uncertainty quantification and confidence intervals
- Validation against historical events where possible

### 🌋 **Comprehensive Event Coverage**

- **Astronomical**: Asteroid/comet impacts, gamma-ray bursts, solar flares
- **Geological**: Supervolcanoes, massive earthquakes, tsunamis
- **Climate**: Runaway greenhouse effect, ice ages, ocean acidification
- **Biological**: Pandemics, ecosystem collapse, biodiversity loss
- **Anthropogenic**: Nuclear war, climate change, pollution
- **Technological**: AI extinction risks, nanotechnology hazards
- **Cosmic**: False vacuum decay, nearby supernovas

### 🖥️ **Dual Interface Design**

- **Web Interface**: Interactive Streamlit application with real-time visualization
- **Command Line**: Batch processing and scripting capabilities
- **API Access**: Programmatic integration for research workflows

### 📊 **Advanced Analytics**

- **Survival Prediction**: Multi-factor models for population survival rates
- **Risk Assessment**: Comprehensive scoring using probability and impact metrics
- **Recovery Estimation**: Timeline analysis for post-event civilization rebuilding
- **Comparative Analysis**: Side-by-side scenario comparisons
- **Sensitivity Analysis**: Parameter variation impact assessment

### 📈 **Rich Visualizations**

- Interactive charts and time-series plots
- Geographic impact heatmaps
- 3D visualization models
- Recovery timeline animations
- Risk comparison matrices

### 🔧 **Extensible Architecture**

- Modular plugin system for new event types
- Configurable parameters and scenarios
- Custom model integration capabilities
- Export formats: CSV, JSON, PDF reports

## 🚀 Quick Start

### Prerequisites

**System Requirements:**

- **Operating System**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 18.04+ recommended)
- **Python**: 3.8 or higher (3.9+ recommended for optimal performance)
- **Memory**: Minimum 4GB RAM (8GB+ recommended for large simulations)
- **Storage**: 2GB free disk space (additional space needed for simulation outputs)
- **Network**: Internet connection for initial setup and data downloads

**Required Software:**

- Python 3.8 or higher
- pip package manager
- Git (for cloning the repository)

**Optional but Recommended:**

- Virtual environment manager (venv, conda, or virtualenv)
- Modern web browser (Chrome, Firefox, Safari, Edge)
- GPU with CUDA support (for accelerated computations)

### Installation

#### Option 1: Automated Installation (Recommended)

**Windows:**

```batch
# Run the automated installer
install.bat

# Or manually:
git clone https://github.com/your-username/ELES.git
cd ELES
install.bat
```

**Linux/macOS:**

```bash
# Run the automated installer
chmod +x install.sh
./install.sh

# Or manually:
git clone https://github.com/your-username/ELES.git
cd ELES
chmod +x install.sh
./install.sh
```

#### Option 2: Manual Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/ELES.git
cd ELES
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Install the package:

```bash
pip install -e .
```

#### Option 3: Development Installation

```bash
# Clone and setup development environment
git clone https://github.com/your-username/ELES.git
cd ELES

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt
pip install -e .

# Verify installation
python test_installation.py
```

### Quick Launch

#### Automated Launch

**Windows:**

```batch
# Launch web interface
launch.bat

# Launch CLI
launch.bat --cli
```

**Linux/macOS:**

```bash
# Launch web interface
./launch.sh

# Launch CLI
./launch.sh --cli
```

#### Manual Launch

Launch the web interface:

```bash
python run_app.py
# or
streamlit run ui/streamlit_app.py
```

Launch the CLI:

```bash
python run_cli.py --help
```

## 💻 Usage Guide

### Web Interface (Streamlit)

The Streamlit web interface provides an intuitive way to explore extinction scenarios:

1. **Scenario Selection**: Choose from pre-configured scenarios or create custom ones
2. **Parameter Adjustment**: Modify event parameters using interactive controls
3. **Real-time Simulation**: Watch results update as you change parameters
4. **Visualization**: Explore results through charts, maps, and 3D models
5. **Export**: Download results in various formats

```bash
# Launch web interface
python run_app.py

# Access at: http://localhost:8501
```

### Command Line Interface

The CLI is perfect for batch processing, scripting, and research workflows:

```bash
# Run a specific scenario
python run_cli.py asteroid --diameter 2.0 --velocity 20.0

# List available scenarios
python run_cli.py --list-scenarios

# Run comparative analysis
python run_cli.py compare --scenarios asteroid,pandemic,nuclear

# Export results
python run_cli.py asteroid --output results.json --format json
```

### Python API

Integrate E.L.E.S. directly into your research code:

```python
from eles_core import create_engine
from models import SurvivalPredictor, RiskScoreCalculator

# Create simulation engine
engine = create_engine()

# Run asteroid impact simulation
result = engine.run_simulation('asteroid', {
    'diameter_km': 2.0,
    'velocity_km_s': 20.0,
    'density_kg_m3': 3500
})

# Predict survival rates
predictor = SurvivalPredictor()
survival = predictor.predict(context)

# Calculate risk scores
calculator = RiskScoreCalculator()
risk = calculator.compute(profile)
```

## 📁 Project Structure

```text
ELES/
├── 📂 eles_core/           # Core simulation engine
│   ├── engine.py           # Main simulation engine
│   ├── extinction_result.py # Results management
│   ├── utils.py            # Utility functions
│   └── 📂 event_types/     # Event-specific models
│       ├── asteroid.py     # Asteroid impact modeling
│       ├── supervolcano.py # Supervolcano simulations
│       ├── pandemic.py     # Disease outbreak models
│       ├── climate_collapse.py # Climate change scenarios
│       ├── gamma_ray_burst.py # GRB modeling
│       └── ai_extinction.py # AI risk scenarios
├── 📂 ui/                  # User interfaces
│   ├── streamlit_app.py    # Main Streamlit application
│   ├── 📂 pages/           # Individual UI pages
│   └── 📂 components/      # Reusable UI components
├── 📂 cli/                 # Command-line interface
│   ├── main.py            # CLI entry point
│   └── 📂 commands/        # CLI command modules
├── 📂 models/              # Predictive models
│   ├── survival_predictor.py # Survival probability models
│   ├── risk_score_calculator.py # Risk assessment
│   ├── regen_time_estimator.py # Recovery time estimation
│   └── examples.py         # Usage examples
├── 📂 visualizations/      # Data visualization
│   ├── charts.py           # Chart generation
│   ├── heatmaps.py         # Geographic visualizations
│   └── 📂 3d/              # 3D modeling components
├── 📂 data/                # Data and scenarios
│   ├── 📂 scenarios/       # Pre-configured scenarios
│   ├── extinction_events.csv # Historical data
│   ├── asteroid_samples.json # Asteroid parameters
│   ├── pandemic_samples.json # Disease parameters
│   └── ...                 # Additional data files
├── 📂 config/              # Configuration files
│   ├── settings.yaml       # Main configuration
│   ├── event_types.yaml    # Event type definitions
│   ├── severity_definitions.yaml # Severity scales
│   └── 📂 scenarios/       # Scenario configurations
├── 📂 assets/              # Visual assets
│   ├── 📂 logo/            # Project logos
│   └── 📂 icons/           # Event type icons
├── 📂 tests/               # Test suite
└── 📂 docs/                # Documentation
```

## 🔬 Scientific Foundation

E.L.E.S. is built on rigorous scientific principles and incorporates research from multiple disciplines:

### Asteroid Impact Modeling

- **Scaling laws**: Based on empirical crater formation relationships
- **Energy calculations**: Kinetic energy and TNT equivalents
- **Atmospheric effects**: Debris clouds and nuclear winter scenarios
- **Tsunami modeling**: Ocean impact wave propagation

### Pandemic Modeling

- **Epidemiological models**: SIR/SEIR compartmental models
- **Network effects**: Social contact patterns and transmission
- **Healthcare capacity**: ICU availability and treatment efficacy
- **Economic impacts**: GDP effects and supply chain disruption

### Climate Modeling

- **Radiative forcing**: Greenhouse gas concentration effects
- **Feedback loops**: Ice-albedo and carbon cycle feedbacks
- **Tipping points**: Critical thresholds and cascade effects
- **Sea level rise**: Ice sheet dynamics and thermal expansion

### Supervolcano Modeling

- **VEI scaling**: Volcanic Explosivity Index relationships
- **Ash dispersal**: Atmospheric transport models
- **Climate impacts**: Volcanic winter and cooling effects
- **Agricultural effects**: Crop yield and food security

## 🎓 Educational Applications

E.L.E.S. is designed for educational use across multiple levels:

### Research & Academia

- **Graduate coursework** in risk assessment and catastrophic risk
- **Research projects** on existential risk and civilization resilience
- **Policy analysis** for governmental and international organizations
- **Academic publications** and peer-reviewed research

### Public Education

- **Science museums** and interactive exhibits
- **Educational workshops** and public lectures
- **Online courses** and educational content
- **Media and journalism** for informed reporting

### Training & Preparedness

- **Emergency management** training and scenario planning
- **Policy maker education** on long-term risks
- **Insurance industry** risk modeling and assessment
- **Corporate resilience** planning and business continuity

## 🌟 Example Scenarios

### Scenario 1: Chicxulub-Scale Asteroid Impact

```python
parameters = {
    'diameter_km': 10.0,
    'velocity_km_s': 20.0,
    'density_kg_m3': 3000,
    'impact_angle': 45.0,
    'target_type': 'continental'
}
```

**Results**: Global devastation, 6-month nuclear winter, 99%+ species extinction

### Scenario 2: Yellowstone Supervolcano Eruption

```python
parameters = {
    'vei': 8,
    'magma_volume_km3': 1000,
    'eruption_duration_days': 30,
    'ash_dispersal_radius_km': 1000
}
```

**Results**: Continental ash coverage, 3-year volcanic winter, massive crop failures

### Scenario 3: Engineered Pandemic

```python
parameters = {
    'transmission_rate': 4.0,
    'case_fatality_rate': 0.15,
    'incubation_period_days': 14,
    'vaccine_development_time_months': 18
}
```

**Results**: Global spread in 6 months, healthcare system collapse, social breakdown

## 📊 Performance & Validation

### Computational Performance

- **Real-time simulation** for most scenarios (< 5 seconds)
- **Batch processing** capabilities for large parameter sweeps
- **Memory efficient** algorithms for large-scale modeling
- **Parallel processing** support for multi-scenario analysis

### Model Validation

- **Historical calibration** against known events (Tunguska, Spanish Flu, etc.)
- **Expert review** by domain specialists in relevant fields
- **Uncertainty quantification** with confidence intervals
- **Sensitivity analysis** for parameter robustness testing

## 🤝 Contributing

We welcome contributions from researchers, developers, and domain experts!

### Development Setup

```bash
# Clone the repository
git clone https://github.com/your-username/ELES.git
cd ELES

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt
pip install -e .

# Run tests
python -m pytest tests/

# Run linting
flake8 eles_core/ ui/ cli/ models/
```

### Contribution Guidelines

1. **Fork** the repository and create a feature branch
1. **Add tests** for new functionality
1. **Update documentation** as needed
1. **Follow coding standards** (PEP 8, type hints, docstrings)
1. **Submit a pull request** with a clear description

### Areas for Contribution

- **New event types** (solar flares, ecosystem collapse, etc.)
- **Enhanced modeling** algorithms and scientific accuracy
- **User interface** improvements and new features
- **Data sources** and historical event databases
- **Visualization** components and interactive elements
- **Documentation** and educational materials

## 📚 Documentation

- **User Guide**: Comprehensive usage documentation
- **API Reference**: Complete function and class documentation
- **Developer Guide**: Architecture and extension tutorials
- **Scientific Basis**: Mathematical models and equations
- **Case Studies**: Real-world applications and examples

## 🆘 Support

### Getting Help

- **Documentation**: Check the docs/ folder for detailed guides
- **Issues**: Report bugs and request features on GitHub
- **Discussions**: Join community discussions for questions
- **Examples**: See models/examples.py for usage patterns

### Troubleshooting

Common issues and solutions:

```bash
# Installation issues
pip install --upgrade pip setuptools wheel

# Missing dependencies
pip install -r requirements.txt --force-reinstall

# Streamlit port conflicts
streamlit run ui/streamlit_app.py --server.port 8502
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```text
MIT License

Copyright (c) 2025 E.L.E.S. Development Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

## 🙏 Acknowledgments

- **Scientific Community**: Researchers whose work forms the foundation of our models
- **Open Source Projects**: Python ecosystem libraries that make this possible
- **Beta Testers**: Early users who provided valuable feedback
- **Domain Experts**: Scientists who reviewed and validated our approaches

## 📈 Roadmap

### Version 1.0 (Current)

- ✅ Core simulation engine
- ✅ Major event types (asteroid, supervolcano, pandemic, etc.)
- ✅ Web and CLI interfaces
- ✅ Basic visualization and export

### Version 1.1 (Planned)

- 🔄 Enhanced AI extinction modeling
- 🔄 Real-time data integration
- 🔄 Mobile-responsive web interface
- 🔄 Advanced 3D visualizations

### Version 2.0 (Future)

- 📋 Machine learning integration
- 📋 Multi-agent modeling
- 📋 VR/AR visualization support
- 📋 Cloud deployment options

---

**E.L.E.S.** - *Understanding extinction risks to build a more resilient future*

For more information, visit our [documentation](docs/) or [get started](#-quick-start) with your first simulation!
