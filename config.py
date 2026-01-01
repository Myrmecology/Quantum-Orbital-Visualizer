"""
Configuration file for Quantum Orbital Visualizer
Contains all constants, settings, and configuration parameters
"""

import numpy as np

# ========================================
# PHYSICAL CONSTANTS
# ========================================

# Fundamental constants (SI units)
HBAR = 1.054571817e-34  # Reduced Planck constant (J·s)
ELECTRON_MASS = 9.1093837015e-31  # Electron mass (kg)
ELECTRON_CHARGE = 1.602176634e-19  # Elementary charge (C)
BOHR_RADIUS = 5.29177210903e-11  # Bohr radius (m)
RYDBERG_ENERGY = 13.605693122994  # Rydberg energy (eV)
EPSILON_0 = 8.8541878128e-12  # Vacuum permittivity (F/m)

# ========================================
# QUANTUM NUMBER LIMITS
# ========================================

N_MIN = 1
N_MAX = 7
L_MAX = 6
M_MAX = 6

# ========================================
# VISUALIZATION SETTINGS
# ========================================

# 3D Grid resolution
GRID_POINTS_LOW = 50      # Low quality (fast)
GRID_POINTS_MEDIUM = 100  # Medium quality
GRID_POINTS_HIGH = 150    # High quality (slow)
DEFAULT_GRID_POINTS = GRID_POINTS_MEDIUM

# Spatial extent (in Bohr radii)
SPATIAL_EXTENT = 30.0

# Probability density thresholds
ISO_SURFACE_LEVELS = [0.001, 0.01, 0.05, 0.1]
DEFAULT_ISO_LEVEL = 0.01

# ========================================
# COLOR SCHEMES
# ========================================

THEME_COLORS = {
    'deep_space': {
        'background': '#000814',
        'primary': '#4CC9F0',
        'secondary': '#F72585',
        'accent': '#7209B7',
        'grid': '#1B263B'
    },
    'cyberpunk': {
        'background': '#0A0E27',
        'primary': '#00F0FF',
        'secondary': '#FF006E',
        'accent': '#FFBE0B',
        'grid': '#3A0CA3'
    },
    'quantum_lab': {
        'background': '#F8F9FA',
        'primary': '#0077B6',
        'secondary': '#00B4D8',
        'accent': '#90E0EF',
        'grid': '#CAF0F8'
    },
    'matrix': {
        'background': '#000000',
        'primary': '#00FF41',
        'secondary': '#008F11',
        'accent': '#00FF41',
        'grid': '#003B00'
    },
    'vectrex': {
        'background': '#000000',
        'primary': '#00FF00',
        'secondary': '#00DD00',
        'accent': '#00BB00',
        'grid': '#003300'
    }
}

DEFAULT_THEME = 'deep_space'

# ========================================
# RENDERING MODES
# ========================================

RENDER_MODES = [
    'volumetric',
    'isosurface',
    'wireframe',
    'cross_section',
    'particle_swarm'
]

DEFAULT_RENDER_MODE = 'isosurface'

# ========================================
# CHART SETTINGS
# ========================================

CHART_HEIGHT = 400
CHART_WIDTH = 600
ANIMATION_DURATION = 500  # milliseconds

# ========================================
# PERFORMANCE SETTINGS
# ========================================

# Caching
ENABLE_CACHE = True
CACHE_DIR = 'data/cache'
PRECOMPUTE_DIR = 'data/precomputed'

# Computation
USE_NUMBA = True
MAX_THREADS = 4

# ========================================
# UI SETTINGS
# ========================================

# Layout
SIDEBAR_WIDTH = 300
MAIN_VIEWPORT_HEIGHT = 700

# Update intervals
REALTIME_UPDATE_INTERVAL = 100  # milliseconds
ANIMATION_FPS = 30

# ========================================
# GAME/CHALLENGE SETTINGS
# ========================================

DIFFICULTY_LEVELS = ['easy', 'medium', 'hard', 'expert']
ACHIEVEMENT_THRESHOLDS = {
    'orbital_master': 50,
    'superposition_guru': 20,
    'speed_runner': 10
}

# ========================================
# EXPORT SETTINGS
# ========================================

EXPORT_FORMATS = ['png', 'html', 'json']
DEFAULT_EXPORT_DPI = 300

# ========================================
# DEBUG/DEVELOPMENT
# ========================================

DEBUG_MODE = False
VERBOSE_LOGGING = False
SHOW_COMPUTATION_TIME = True

# ========================================
# APP METADATA
# ========================================

APP_TITLE = "Quantum Orbital Visualizer"
APP_VERSION = "0.1.0"
APP_AUTHOR = "Your Name"
APP_DESCRIPTION = "Interactive 3D Quantum Mechanics Visualization"