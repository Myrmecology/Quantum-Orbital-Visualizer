"""
Orbital Generation and Management
==================================

Functions for generating 3D orbital grids, calculating orbital properties,
and managing quantum state information.
"""

import numpy as np
from .schrodinger import (
    hydrogen_wave_function,
    probability_density,
    radial_wave_function,
    spherical_harmonic
)
from .constants import RYDBERG_ENERGY, validate_quantum_number_bounds
import config


# ========================================
# ORBITAL NAMING
# ========================================

ORBITAL_LETTERS = {
    0: 's',
    1: 'p',
    2: 'd',
    3: 'f',
    4: 'g',
    5: 'h',
    6: 'i'
}

ANGULAR_MOMENTUM_NAMES = {
    0: 'sharp',
    1: 'principal',
    2: 'diffuse',
    3: 'fundamental',
    4: 'g-orbital',
    5: 'h-orbital',
    6: 'i-orbital'
}


def get_orbital_name(n, l, m):
    """
    Get standard orbital notation (e.g., 1s, 2p, 3d).
    
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
    str
        Orbital name (e.g., '1s', '2p_z', '3d_xy')
    """
    letter = ORBITAL_LETTERS.get(l, f'l={l}')
    
    # Add magnetic quantum number subscript for clarity
    m_subscript = ''
    if l == 1:  # p orbitals
        m_labels = {-1: 'x', 0: 'z', 1: 'y'}
        m_subscript = f'_{m_labels.get(m, m)}'
    elif l == 2:  # d orbitals
        m_labels = {-2: 'xy', -1: 'yz', 0: 'z²', 1: 'xz', 2: 'x²-y²'}
        m_subscript = f'_{m_labels.get(m, m)}'
    elif l > 2 and m != 0:
        m_subscript = f'_m={m}'
    
    return f'{n}{letter}{m_subscript}'


def validate_quantum_numbers(n, l, m):
    """
    Validate quantum numbers and raise descriptive errors if invalid.
    
    Parameters
    ----------
    n : int
        Principal quantum number
    l : int
        Angular momentum quantum number
    m : int
        Magnetic quantum number
        
    Raises
    ------
    ValueError
        If quantum numbers are invalid
        
    Returns
    -------
    bool
        True if valid
    """
    if not isinstance(n, int) or not isinstance(l, int) or not isinstance(m, int):
        raise ValueError("Quantum numbers must be integers")
    
    if n < 1:
        raise ValueError(f"Principal quantum number n must be ≥ 1, got n={n}")
    
    if l < 0:
        raise ValueError(f"Angular momentum quantum number l must be ≥ 0, got l={l}")
    
    if l >= n:
        raise ValueError(f"Angular momentum l must be < n, got l={l}, n={n}")
    
    if abs(m) > l:
        raise ValueError(f"Magnetic quantum number m must satisfy |m| ≤ l, got m={m}, l={l}")
    
    return True


def calculate_orbital_energy(n):
    """
    Calculate energy eigenvalue for hydrogen orbital.
    
    E_n = -13.6 eV / n²
    
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


def calculate_energy_difference(n1, n2):
    """
    Calculate energy difference between two levels (for transitions).
    
    Parameters
    ----------
    n1 : int
        Initial principal quantum number
    n2 : int
        Final principal quantum number
        
    Returns
    -------
    float
        Energy difference in eV (positive if n2 > n1)
    """
    E1 = calculate_orbital_energy(n1)
    E2 = calculate_orbital_energy(n2)
    return E2 - E1


def calculate_photon_wavelength(n1, n2):
    """
    Calculate photon wavelength for transition between levels.
    
    λ = hc / ΔE
    
    Parameters
    ----------
    n1, n2 : int
        Initial and final quantum numbers
        
    Returns
    -------
    float
        Wavelength in nanometers
    """
    from .constants import H, SPEED_OF_LIGHT, EV_TO_JOULES
    
    delta_E = abs(calculate_energy_difference(n1, n2))
    delta_E_joules = delta_E * EV_TO_JOULES
    
    wavelength_m = (H * SPEED_OF_LIGHT) / delta_E_joules
    wavelength_nm = wavelength_m * 1e9
    
    return wavelength_nm


# ========================================
# GRID GENERATION
# ========================================

def generate_orbital_grid(n, l, m, grid_points=None, spatial_extent=None):
    """
    Generate 3D grid of wave function or probability density values.
    
    Parameters
    ----------
    n, l, m : int
        Quantum numbers
    grid_points : int, optional
        Number of points per dimension (default from config)
    spatial_extent : float, optional
        Maximum extent in Bohr radii (default from config)
        
    Returns
    -------
    dict
        Dictionary containing:
        - 'x', 'y', 'z': Cartesian coordinate grids
        - 'r', 'theta', 'phi': Spherical coordinate grids
        - 'psi': Complex wave function values
        - 'psi_real': Real part of wave function
        - 'psi_imag': Imaginary part of wave function
        - 'prob_density': Probability density |ψ|²
        - 'quantum_numbers': (n, l, m)
        - 'energy': Energy eigenvalue
    """
    # Validate quantum numbers
    validate_quantum_numbers(n, l, m)
    
    # Set defaults
    if grid_points is None:
        grid_points = config.DEFAULT_GRID_POINTS
    if spatial_extent is None:
        spatial_extent = config.SPATIAL_EXTENT
    
    # Create Cartesian grid
    extent = spatial_extent
    x = np.linspace(-extent, extent, grid_points)
    y = np.linspace(-extent, extent, grid_points)
    z = np.linspace(-extent, extent, grid_points)
    
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    
    # Convert to spherical coordinates
    R = np.sqrt(X**2 + Y**2 + Z**2)
    R = np.where(R == 0, 1e-10, R)  # Avoid division by zero
    
    THETA = np.arccos(Z / R)
    PHI = np.arctan2(Y, X)
    
    # Calculate wave function
    PSI = hydrogen_wave_function(R, THETA, PHI, n, l, m)
    
    # Calculate probability density
    PROB = probability_density(R, THETA, PHI, n, l, m)
    
    # Calculate energy
    energy = calculate_orbital_energy(n)
    
    return {
        'x': X,
        'y': Y,
        'z': Z,
        'r': R,
        'theta': THETA,
        'phi': PHI,
        'psi': PSI,
        'psi_real': np.real(PSI),
        'psi_imag': np.imag(PSI),
        'prob_density': PROB,
        'quantum_numbers': (n, l, m),
        'energy': energy,
        'orbital_name': get_orbital_name(n, l, m)
    }


def generate_cross_section(n, l, m, plane='xy', grid_points=None, spatial_extent=None):
    """
    Generate 2D cross-section of orbital through specified plane.
    
    Parameters
    ----------
    n, l, m : int
        Quantum numbers
    plane : str
        Plane to slice: 'xy', 'xz', or 'yz'
    grid_points : int, optional
        Number of points per dimension
    spatial_extent : float, optional
        Maximum extent in Bohr radii
        
    Returns
    -------
    dict
        Dictionary with coordinate grids and probability density
    """
    validate_quantum_numbers(n, l, m)
    
    if grid_points is None:
        grid_points = config.DEFAULT_GRID_POINTS
    if spatial_extent is None:
        spatial_extent = config.SPATIAL_EXTENT
    
    extent = spatial_extent
    coord = np.linspace(-extent, extent, grid_points)
    
    if plane == 'xy':
        X, Y = np.meshgrid(coord, coord)
        Z = np.zeros_like(X)
    elif plane == 'xz':
        X, Z = np.meshgrid(coord, coord)
        Y = np.zeros_like(X)
    elif plane == 'yz':
        Y, Z = np.meshgrid(coord, coord)
        X = np.zeros_like(Y)
    else:
        raise ValueError(f"Invalid plane: {plane}. Must be 'xy', 'xz', or 'yz'")
    
    # Convert to spherical
    R = np.sqrt(X**2 + Y**2 + Z**2)
    R = np.where(R == 0, 1e-10, R)
    THETA = np.arccos(Z / R)
    PHI = np.arctan2(Y, X)
    
    # Calculate probability density
    PROB = probability_density(R, THETA, PHI, n, l, m)
    
    return {
        'x': X,
        'y': Y,
        'z': Z,
        'prob_density': PROB,
        'plane': plane,
        'quantum_numbers': (n, l, m)
    }


def calculate_grid_statistics(grid_data):
    """
    Calculate statistical properties of orbital grid.
    
    Parameters
    ----------
    grid_data : dict
        Output from generate_orbital_grid
        
    Returns
    -------
    dict
        Statistics including max probability, total probability, etc.
    """
    prob = grid_data['prob_density']
    
    return {
        'max_probability': np.max(prob),
        'min_probability': np.min(prob),
        'mean_probability': np.mean(prob),
        'total_probability': np.sum(prob),
        'nonzero_points': np.sum(prob > 1e-10)
    }


def get_isosurface_value(grid_data, threshold=None):
    """
    Get appropriate isosurface threshold for visualization.
    
    Parameters
    ----------
    grid_data : dict
        Orbital grid data
    threshold : float, optional
        Manual threshold (default uses config)
        
    Returns
    -------
    float
        Isosurface threshold value
    """
    if threshold is None:
        threshold = config.DEFAULT_ISO_LEVEL
    
    max_prob = np.max(grid_data['prob_density'])
    return threshold * max_prob