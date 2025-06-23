# 🌍 E.L.E.S. Advanced Home Page

## Overview

The advanced home page provides a comprehensive introduction and interactive demonstration of the Extinction-Level Event Simulator (E.L.E.S.). This page serves as both an entry point for new users and a powerful dashboard for experienced researchers.

## 🎯 Key Features

### 1. **Hero Section & Platform Overview**

- Stunning gradient design with key statistics
- Real-time platform metrics (6 event types, 95% scientific accuracy)
- Quick overview of core capabilities

### 2. **Interactive Event Type Showcase**

- Detailed cards for all 6 extinction event types:
  - ☄️ **Asteroid Impact** - Size, velocity, composition modeling
  - 🦠 **Global Pandemic** - R₀, mortality, transmission analysis
  - 🌋 **Supervolcano Eruption** - VEI scale, ash dispersal, climate effects
  - 🌡️ **Climate Collapse** - Temperature change, tipping points, ecosystems
  - 💫 **Gamma-Ray Burst** - Distance, energy, atmospheric damage
  - 🤖 **AI Extinction Risk** - Capability levels, alignment, control measures

### 3. **Live Simulation Demo**

- Real-time parameter adjustment with instant results
- Interactive sliders for each event type's key parameters
- Live visualization of severity levels and impact metrics
- Immediate feedback on casualties, economic impact, and recovery time

### 4. **Advanced Capabilities Display**

- 🔬 Scientific modeling with peer-reviewed algorithms
- 📊 Real-time analysis and sensitivity testing
- 🌐 Global impact assessment with cascading effects
- 🎯 Multi-factor risk prediction models
- 📈 Recovery timeline modeling
- 💾 Comprehensive data export capabilities

### 5. **Scenario Impact Comparison**

- Interactive charts comparing different extinction scenarios
- Multi-dimensional analysis (severity, casualties, economic impact, recovery)
- Visual representation of relative impacts across event types

### 6. **Getting Started Pathways**

- 🎓 **Educational Mode** - Guided tutorials for beginners
- 🔬 **Research Mode** - Advanced parameters for scientists
- ⚡ **Quick Analysis** - Fast-track results with intelligent defaults

## 🎨 Design Features

### Modern UI/UX

- **Gradient Backgrounds**: Eye-catching linear gradients for visual appeal
- **Card-based Layout**: Clean, organized information presentation
- **Responsive Design**: Adapts to different screen sizes
- **Interactive Elements**: Hover effects and smooth transitions
- **Color-coded Severity**: Visual severity indicators using scientific color schemes

### Advanced Styling

- **Custom CSS**: Professional styling with modern design patterns
- **Typography Hierarchy**: Clear information structure
- **Visual Indicators**: Severity badges, status indicators, and progress bars
- **Consistent Branding**: Unified color scheme and visual identity

## 🔧 Technical Implementation

### Architecture

- **Modular Design**: Separate functions for each major section
- **Error Handling**: Graceful degradation for missing components
- **Performance Optimized**: Efficient data loading and rendering
- **State Management**: Proper handling of user interactions

### Dependencies

- **Streamlit**: Web framework and UI components
- **Plotly**: Interactive visualizations and charts
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **E.L.E.S. Core**: Simulation engine and event models

### Integration Points

- **Engine Integration**: Direct access to simulation capabilities
- **Constants Usage**: Proper severity levels and color schemes
- **Event Types**: Full integration with all extinction event models
- **Error Boundaries**: Safe handling of simulation failures

## 📊 Interactive Components

### Demo Simulation

The live demo allows users to:

- Select any of the 6 extinction event types
- Adjust key parameters using intuitive sliders
- See immediate results including:
  - Severity level (1-6 scale with color coding)
  - Estimated casualties
  - Economic impact in trillions USD
  - Recovery time estimates
  - Impacted area in km²

### Visualization Features

- **Severity Gauge**: Real-time gauge showing threat level
- **Comparison Charts**: Multi-scenario impact analysis
- **Color-coded Results**: Intuitive severity representation
- **Responsive Updates**: Instant parameter-to-result feedback

## 🚀 Usage

### Running the Home Page

```bash
# Option 1: Direct streamlit execution
streamlit run ui/pages/home.py

# Option 2: Through main application
python run_app.py
```

### Customization

The home page is designed to be easily customizable:

1. **Styling**: Modify the CSS in the `st.markdown()` sections
2. **Content**: Update event descriptions, capabilities, or statistics
3. **Parameters**: Adjust demo parameter ranges and defaults
4. **Visualizations**: Enhance or add new chart types

### Integration

To integrate with other parts of the application:

```python
from ui.pages.home import run

# Call the home page function
run()
```

## 🎓 Educational Value

The advanced home page serves multiple educational purposes:

### For Students

- Introduction to extinction risk concepts
- Visual understanding of relative threat levels
- Interactive exploration of "what-if" scenarios

### For Researchers

- Quick access to modeling capabilities
- Parameter sensitivity demonstration
- Comparative analysis tools

### For Policymakers

- Risk assessment overview
- Economic impact visualization
- Recovery planning insights

## 🔮 Future Enhancements

Planned improvements include:

- **3D Visualizations**: Integration with three_d models
- **Historical Data**: Display of past extinction events
- **Real-time Updates**: Live data feeds for current risks
- **Collaborative Features**: Multi-user scenario building
- **Mobile Optimization**: Enhanced mobile experience

## 📝 Notes

- The home page is fully self-contained and doesn't require external data files
- All simulations use the core E.L.E.S. engine for accuracy
- Error handling ensures graceful degradation if components are unavailable
- The design is optimized for both technical and general audiences

---

**E.L.E.S.** - *Understanding extinction risks to build a more resilient future*
