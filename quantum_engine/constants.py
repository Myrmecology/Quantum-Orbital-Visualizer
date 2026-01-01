"""
Physical Constants and Unit Conversions
========================================

Contains fundamental physical constants and utility functions
for unit conversions between SI and atomic units.
"""

import numpy as np

# ========================================
# FUNDAMENTAL PHYSICAL CONSTANTS (SI Units)
# ========================================

# Planck constant
H = 6.62607015e-34  # J·s
HBAR = 1.054571817e-34  # J·s (reduced Planck constant)

# Electron properties
ELECTRON_MASS = 9.1093837015e-31  # kg
ELECTRON_CHARGE = 1.602176634e-19  # C

# Electromagnetic constants
EPSILON_0 = 8.8541878128e-12  # F/m (vacuum permittivity)
MU_0 = 1.25663706212e-6  # H/m (vacuum permeability)
SPEED_OF_LIGHT = 299792458  # m/s

# ========================================
# ATOMIC UNITS
# ========================================

# Bohr radius (fundamental length scale)
BOHR_RADIUS = 5.29177210903e-11  # m (a₀)

# Hartree energy (fundamental energy scale)
HARTREE_ENERGY = 4.3597447222071e-18  # J
RYDBERG_ENERGY = 13.605693122994  # eV (hydrogen ground state)

# Fine structure constant
FINE_STRUCTURE = 7.2973525693e-3  # α (dimensionless)

# ========================================
# CONVERSION FACTORS
# ========================================

# Energy conversions
EV_TO_JOULES = 1.602176634e-19
JOULES_TO_EV = 6.241509074e18
HARTREE_TO_EV = 27.211386245988

# Length conversions
ANGSTROM_TO_BOHR = 1.8897261246257702
BOHR_TO_ANGSTROM = 0.529177210903
BOHR_TO_NANOMETER = 0.0529177210903

# Time conversions
ATOMIC_TIME_UNIT = 2.4188843265857e-17  # s

# ========================================
# HYDROGEN ATOM SPECIFIC
# ========================================

# Quantum number limits
N_MIN = 1  # Principal quantum number minimum
L_MIN = 0  # Angular momentum quantum number minimum

# Energy level formula constant
HYDROGEN_IONIZATION = 13.598434005136  # eV

# ========================================
# MATHEMATICAL CONSTANTS
# ========================================

PI = np.pi
TWO_PI = 2 * np.pi
SQRT_PI = np.sqrt(np.pi)
SQRT_2PI = np.sqrt(2 * np.pi)


# ========================================
# UNIT CONVERSION FUNCTIONS
# ========================================

def atomic_units_to_si(value, quantity='length'):
    """
    Convert from atomic units to SI units.
    
    Parameters
    ----------
    value : float or array
        Value in atomic units
    quantity : str
        Type of quantity: 'length', 'energy', 'time'
        
    Returns
    -------
    float or array
        Value in SI units
    """
    conversions = {
        'length': BOHR_RADIUS,
        'energy': HARTREE_ENERGY,
        'time': ATOMIC_TIME_UNIT
    }
    
    if quantity not in conversions:
        raise ValueError(f"Unknown quantity: {quantity}")
    
    return value * conversions[quantity]


def si_to_atomic_units(value, quantity='length'):
    """
    Convert from SI units to atomic units.
    
    Parameters
    ----------
    value : float or array
        Value in SI units
    quantity : str
        Type of quantity: 'length', 'energy', 'time'
        
    Returns
    -------
    float or array
        Value in atomic units
    """
    conversions = {
        'length': 1.0 / BOHR_RADIUS,
        'energy': 1.0 / HARTREE_ENERGY,
        'time': 1.0 / ATOMIC_TIME_UNIT
    }
    
    if quantity not in conversions:
        raise ValueError(f"Unknown quantity: {quantity}")
    
    return value * conversions[quantity]


def energy_ev_to_hartree(energy_ev):
    """Convert energy from eV to Hartree."""
    return energy_ev / HARTREE_TO_EV


def energy_hartree_to_ev(energy_hartree):
    """Convert energy from Hartree to eV."""
    return energy_hartree * HARTREE_TO_EV


def length_bohr_to_angstrom(length_bohr):
    """Convert length from Bohr radii to Angstroms."""
    return length_bohr * BOHR_TO_ANGSTROM


def length_angstrom_to_bohr(length_angstrom):
    """Convert length from Angstroms to Bohr radii."""
    return length_angstrom * ANGSTROM_TO_BOHR


# ========================================
# UTILITY FUNCTIONS
# ========================================

def validate_quantum_number_bounds(n, l, m):
    """
    Validate quantum numbers are within physical bounds.
    
    Parameters
    ----------
    n : int
        Principal quantum number
    l : int
        Angular momentum quantum number
    m : int
        Magnetic quantum number
        
    Returns
    -------
    bool
        True if valid, False otherwise
    """
    if n < N_MIN:
        return False
    if l < L_MIN or l >= n:
        return False
    if abs(m) > l:
        return False
    return True


def get_energy_level_ev(n):
    """
    Calculate energy level for hydrogen atom in eV.
    
    Parameters
    ----------
    n : int
        Principal quantum number
        
    Returns
    -------
    float
        Energy in eV (negative for bound states)
    """
    return -RYDBERG_ENERGY / (n ** 2)


def get_orbital_angular_momentum(l):
    """
    Calculate orbital angular momentum magnitude.
    
    Parameters
    ----------
    l : int
        Angular momentum quantum number
        
    Returns
    -------
    float
        |L| = ℏ√(l(l+1))
    """
    return HBAR * np.sqrt(l * (l + 1))