# Quantum Orbital Visualizer

An interactive 3D quantum mechanics visualization application that brings the Schrödinger equation to life in your browser. Explore hydrogen atom wave functions, probability distributions, and quantum phenomena with real-time controls and stunning visualizations.

## Overview

This project creates a fully interactive web-based application for visualizing hydrogen atom orbitals, quantum wave functions, and probability distributions. Users can manipulate quantum numbers in real-time, measure probabilities, create superposition states, and explore quantum mechanics through engaging visualizations and gamification.

## Features

### Core Functionality
- **Interactive 3D Orbital Visualization**: Real-time rendering of quantum orbitals with multiple render modes
- **Quantum Number Controls**: Intuitive sliders for n (principal), l (angular momentum), and m (magnetic) quantum numbers
- **Multiple Render Modes**: Isosurface, volume rendering, wireframe, particle swarm, and cross-sections
- **Schrödinger Equation Solver**: Analytical solutions for hydrogen atom wave functions

### Visualizations & Charts
- **Energy Level Diagrams**: Interactive bar charts showing hydrogen energy levels
- **Radial Probability Distributions**: Line graphs of P(r) = r²|R(r)|²
- **Angular Momentum Pie Charts**: Visual breakdown of quantum states
- **Probability Heatmaps**: 2D cross-sectional views
- **Statistics Tables**: Real-time quantum state properties

### Advanced Features
- **Superposition Builder**: Combine multiple quantum states and visualize interference
- **Measurement Tools**: Click-to-probe probability, region integration, uncertainty calculations
- **Multiple Themes**: Deep Space, Cyberpunk, Quantum Lab, Matrix, and Vectrex retro graphics
- **Gamification**: Orbital matching games, probability challenges, and achievement tracking
- **Time Evolution**: Animate superposition states over time

## Installation

### Prerequisites
- Python 3.12 or higher
- pip package manager
- Git

### Setup Instructions

1. **Clone the repository:**
```bash
git clone https://github.com/Myrmecology/Quantum-Orbital-Visualizer.git
cd quantum-orbital-visualizer
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt --break-system-packages
```

Note: The `--break-system-packages` flag is required on some systems. If you encounter issues, try without it:
```bash
pip install -r requirements.txt
```

3. **Verify installation:**
All required packages should install successfully. You may see PATH warnings - these are safe to ignore.

## Running the Application

### Start the server:
```bash
python app.py
```

### Access the application:
Open your web browser and navigate to:
```
http://127.0.0.1:8050
```

The terminal will display:
```
============================================================
⚛️  QUANTUM ORBITAL VISUALIZER
============================================================
Version: 0.1.0
...
📡 Server running at: http://127.0.0.1:8050
============================================================
```

### Stop the server:
Press `Ctrl+C` in the terminal

## Usage Guide

### Basic Workflow

1. **Select Quantum Numbers:**
   - Use the sliders in the "Quantum" tab to set n, l, and m values
   - The visualization updates in real-time
   - Valid ranges: n (1-7), l (0 to n-1), m (-l to +l)

2. **Change Visualization Mode:**
   - Go to the "Visual" tab
   - Select render mode: Isosurface, Volume, Wireframe, or Particle Swarm
   - Adjust isosurface level for different probability thresholds
   - Choose grid quality (Low/Medium/High)

3. **Switch Themes:**
   - Select from available themes in the "Visual" tab
   - Try "Vectrex" for retro CRT graphics!
   - Each theme has unique color palettes and styling

4. **Create Superpositions:**
   - Navigate to the "Superposition" tab
   - Enter quantum numbers for two states
   - Set complex coefficients (real and imaginary parts)
   - Click "Create Superposition" to visualize interference

5. **Measure Probabilities:**
   - Go to the "Measure" tab
   - Enter coordinates or use region selectors
   - Calculate Heisenberg uncertainty relations

6. **Play Games:**
   - Visit the "Games" tab
   - Try orbital matching challenges
   - Complete probability hunts
   - Unlock achievements

## Project Structure
```
quantum-orbital-visualizer/
├── app.py                          # Main Dash application
├── config.py                       # Configuration and constants
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── .gitignore                      # Git ignore rules
│
├── quantum_engine/                 # Quantum mechanics core
│   ├── __init__.py
│   ├── constants.py               # Physical constants
│   ├── schrodinger.py             # Wave function calculations
│   ├── orbitals.py                # Orbital generation
│   └── superposition.py           # State mixing
│
├── visualizations/                 # Plotting and graphics
│   ├── __init__.py
│   ├── plotly_3d.py               # 3D visualizations
│   ├── charts.py                  # 2D charts and graphs
│   ├── themes.py                  # Theme management
│   └── vectrex.py                 # Retro vector graphics
│
├── interactive/                    # UI components
│   ├── __init__.py
│   ├── controls.py                # Sliders, dropdowns, buttons
│   ├── measurements.py            # Measurement tools
│   ├── games.py                   # Gamification features
│   └── callbacks.py               # Dash callbacks
│
├── assets/                         # Static files
│   ├── custom.css                 # Main stylesheet
│   ├── vectrex.css                # Vectrex theme CSS
│   ├── animations.js              # JavaScript effects
│   └── themes/                    # Individual theme CSS
│       ├── deep_space.css
│       ├── cyberpunk.css
│       ├── quantum_lab.css
│       └── matrix.css
│
├── data/                           # Data storage
│   ├── cache/                     # Cached calculations
│   └── precomputed/               # Precomputed orbitals
│
└── tests/                          # Test suite
    ├── __init__.py
    ├── test_quantum_engine.py
    └── test_visualizations.py
```

## Technologies Used

### Backend
- **Python 3.12**: Core programming language
- **NumPy**: Numerical computations
- **SciPy**: Special functions (spherical harmonics, Laguerre polynomials)
- **SymPy**: Symbolic mathematics

### Frontend
- **Dash**: Web framework for interactive applications
- **Plotly**: Interactive 3D graphics and charts
- **Dash Bootstrap Components**: UI components
- **Custom CSS**: Theme styling and animations

### Scientific Computing
- **Numba**: JIT compilation for performance
- **Pandas**: Data processing
- **Matplotlib**: Additional plotting capabilities

## Mathematics

The visualizer solves the time-independent Schrödinger equation for the hydrogen atom:
```
Ĥψ(r,θ,φ) = Eψ(r,θ,φ)
```

### Key Components:
- **Wave Function**: ψ_nlm(r,θ,φ) = R_nl(r) × Y_l^m(θ,φ)
- **Radial Function**: R_nl(r) with associated Laguerre polynomials
- **Angular Function**: Y_l^m(θ,φ) spherical harmonics
- **Energy Eigenvalues**: E_n = -13.6 eV / n²
- **Probability Density**: |ψ|² visualization

## Testing

Run the test suite:
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_quantum_engine.py -v

# Run with coverage
pytest tests/ --cov=quantum_engine --cov=visualizations
```

## Troubleshooting

### Installation Issues

**Problem**: `ModuleNotFoundError: No module named 'distutils'`
**Solution**: Update to Python 3.12-compatible package versions (already in requirements.txt)

**Problem**: PATH warnings during installation
**Solution**: Safe to ignore - the application will run correctly

### Runtime Issues

**Problem**: Application won't start
**Solution**: Ensure all dependencies are installed: `pip install -r requirements.txt --break-system-packages`

**Problem**: Slow rendering on large grid sizes
**Solution**: Use "Low" or "Medium" grid quality in Visual settings

**Problem**: Callbacks not responding
**Solution**: Clear browser cache and restart the application

### Performance Optimization

- Use lower grid points (30-50) for faster rendering
- Enable caching in config.py
- Close unused browser tabs
- Use Isosurface mode instead of Volume for better performance

## Configuration

Edit `config.py` to customize:

- Grid resolution (`GRID_POINTS_LOW`, `GRID_POINTS_MEDIUM`, `GRID_POINTS_HIGH`)
- Spatial extent (`SPATIAL_EXTENT`)
- Color themes (`THEME_COLORS`)
- Debug mode (`DEBUG_MODE`)
- Performance settings (`USE_NUMBA`, `MAX_THREADS`)

## Future Enhancements

Potential features for future development:

- Multi-electron atoms and molecules
- Spin visualization
- Magnetic field interactions (Zeeman effect)
- Export animations as video
- VR/AR support
- Collaborative features
- Advanced quantum algorithms

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Built with Python, Dash, and Plotly
- Quantum mechanics calculations based on analytical solutions
- Inspired by the beauty of quantum physics



---

**Enjoy exploring the quantum world!** ⚛️✨
Happy coding 