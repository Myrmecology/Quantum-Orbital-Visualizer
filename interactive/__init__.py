"""
Interactive Components Module
==============================

Interactive controls, measurements, games, and callbacks for the application.

This module contains:
- Interactive controls (sliders, dropdowns, buttons)
- Measurement tools (click-to-probe, region selection)
- Gamification and challenges
- Dash callbacks for interactivity

Author: Justin D
Version: 0.1.0
"""

from .controls import (
    create_quantum_number_controls,
    create_theme_selector,
    create_render_mode_selector,
    create_superposition_builder
)

from .measurements import (
    measure_probability_at_point,
    calculate_region_probability,
    create_measurement_tools,
    uncertainty_calculator
)

from .games import (
    orbital_matching_game,
    probability_challenge,
    create_achievement_tracker,
    generate_challenge
)

from .callbacks import (
    register_all_callbacks,
    update_orbital_callback,
    update_theme_callback,
    measurement_callback
)

__all__ = [
    # Controls
    'create_quantum_number_controls',
    'create_theme_selector',
    'create_render_mode_selector',
    'create_superposition_builder',
    
    # Measurements
    'measure_probability_at_point',
    'calculate_region_probability',
    'create_measurement_tools',
    'uncertainty_calculator',
    
    # Games
    'orbital_matching_game',
    'probability_challenge',
    'create_achievement_tracker',
    'generate_challenge',
    
    # Callbacks
    'register_all_callbacks',
    'update_orbital_callback',
    'update_theme_callback',
    'measurement_callback'
]

__version__ = '0.1.0'
__author__ = 'Justin D'