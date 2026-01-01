"""
Quantum Engine Module
=====================

Core quantum mechanics calculations for the Quantum Orbital Visualizer.

This module contains:
- Schrödinger equation solutions
- Orbital wave function calculations
- Quantum superposition handling
- Physical constants and utilities

Author: Justin D
Version: 0.1.0
"""

from .schrodinger import (
    hydrogen_wave_function,
    radial_wave_function,
    spherical_harmonic,
    probability_density
)

from .orbitals import (
    generate_orbital_grid,
    calculate_orbital_energy,
    get_orbital_name,
    validate_quantum_numbers
)

from .superposition import (
    create_superposition,
    normalize_superposition,
    calculate_interference
)

from .constants import (
    BOHR_RADIUS,
    RYDBERG_ENERGY,
    atomic_units_to_si,
    si_to_atomic_units
)

__all__ = [
    # Schrödinger equation
    'hydrogen_wave_function',
    'radial_wave_function',
    'spherical_harmonic',
    'probability_density',
    
    # Orbitals
    'generate_orbital_grid',
    'calculate_orbital_energy',
    'get_orbital_name',
    'validate_quantum_numbers',
    
    # Superposition
    'create_superposition',
    'normalize_superposition',
    'calculate_interference',
    
    # Constants
    'BOHR_RADIUS',
    'RYDBERG_ENERGY',
    'atomic_units_to_si',
    'si_to_atomic_units'
]

__version__ = '0.1.0'
__author__ = 'Justin D'