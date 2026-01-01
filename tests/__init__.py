"""
Quantum Orbital Visualizer - Test Suite
========================================

Unit tests for quantum calculations and visualizations.

Run tests with:
    pytest tests/
    pytest tests/test_quantum_engine.py -v
    pytest tests/test_visualizations.py -v

Author: Justin D
Version: 0.1.0
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

__version__ = '0.1.0'
__author__ = 'Justin D'

# Test configuration
TEST_GRID_POINTS = 30  # Use smaller grid for faster tests
TEST_SPATIAL_EXTENT = 20.0  # Smaller extent for tests
TEST_TOLERANCE = 1e-6  # Numerical tolerance for comparisons

# Common test quantum numbers
TEST_STATES = [
    (1, 0, 0),  # 1s
    (2, 0, 0),  # 2s
    (2, 1, 0),  # 2p
    (2, 1, 1),  # 2p
    (3, 0, 0),  # 3s
    (3, 1, 0),  # 3p
    (3, 2, 0),  # 3d
]