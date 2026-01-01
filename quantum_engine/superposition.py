"""
Quantum Superposition and State Mixing
=======================================

Functions for creating and analyzing superposition states,
calculating interference patterns, and normalizing combined wave functions.
"""

import numpy as np
from .schrodinger import hydrogen_wave_function, probability_density
from .orbitals import validate_quantum_numbers
import config


def create_superposition(states, coefficients, r, theta, phi):
    """
    Create superposition of multiple quantum states.
    
    ψ_total = Σ c_i * ψ_i
    
    where c_i are complex coefficients and ψ_i are individual states.
    
    Parameters
    ----------
    states : list of tuples
        List of (n, l, m) quantum number tuples
    coefficients : list of complex
        Complex coefficients for each state
    r, theta, phi : ndarray
        Coordinate grids (spherical)
        
    Returns
    -------
    complex ndarray
        Superposition wave function
    """
    if len(states) != len(coefficients):
        raise ValueError("Number of states must match number of coefficients")
    
    # Initialize superposition
    psi_superposition = np.zeros_like(r, dtype=complex)
    
    # Add each state with its coefficient
    for (n, l, m), coeff in zip(states, coefficients):
        validate_quantum_numbers(n, l, m)
        psi_i = hydrogen_wave_function(r, theta, phi, n, l, m)
        psi_superposition += coeff * psi_i
    
    return psi_superposition


def normalize_superposition(coefficients):
    """
    Normalize superposition coefficients so Σ|c_i|² = 1.
    
    Parameters
    ----------
    coefficients : array-like
        Complex coefficients
        
    Returns
    -------
    ndarray
        Normalized coefficients
    """
    coefficients = np.array(coefficients, dtype=complex)
    norm = np.sqrt(np.sum(np.abs(coefficients) ** 2))
    
    if norm == 0:
        raise ValueError("Cannot normalize zero coefficients")
    
    return coefficients / norm


def calculate_interference(states, coefficients, r, theta, phi):
    """
    Calculate interference pattern from superposition.
    
    Returns both the superposition probability density and
    the interference term (difference from classical sum).
    
    Parameters
    ----------
    states : list of tuples
        List of (n, l, m) quantum number tuples
    coefficients : list of complex
        Complex coefficients
    r, theta, phi : ndarray
        Coordinate grids
        
    Returns
    -------
    dict
        Dictionary containing:
        - 'superposition_prob': |ψ_total|²
        - 'classical_sum': Σ|c_i|² * |ψ_i|²
        - 'interference': Quantum interference term
        - 'interference_fraction': Fraction due to interference
    """
    # Normalize coefficients
    coefficients = normalize_superposition(coefficients)
    
    # Calculate superposition
    psi_total = create_superposition(states, coefficients, r, theta, phi)
    superposition_prob = np.abs(psi_total) ** 2
    
    # Calculate classical sum (no interference)
    classical_sum = np.zeros_like(r, dtype=float)
    for (n, l, m), coeff in zip(states, coefficients):
        psi_i = hydrogen_wave_function(r, theta, phi, n, l, m)
        classical_sum += np.abs(coeff) ** 2 * np.abs(psi_i) ** 2
    
    # Interference term
    interference = superposition_prob - classical_sum
    
    # Fraction of probability due to interference
    total_prob = np.sum(superposition_prob)
    interference_contribution = np.sum(np.abs(interference))
    interference_fraction = interference_contribution / total_prob if total_prob > 0 else 0
    
    return {
        'superposition_prob': superposition_prob,
        'classical_sum': classical_sum,
        'interference': interference,
        'interference_fraction': interference_fraction
    }


def time_evolution(states, coefficients, r, theta, phi, time):
    """
    Calculate time evolution of superposition state.
    
    ψ(t) = Σ c_i * ψ_i * exp(-iE_i*t/ℏ)
    
    Parameters
    ----------
    states : list of tuples
        List of (n, l, m) quantum number tuples
    coefficients : list of complex
        Complex coefficients
    r, theta, phi : ndarray
        Coordinate grids
    time : float
        Time in atomic units (ℏ/E_h)
        
    Returns
    -------
    complex ndarray
        Time-evolved wave function
    """
    from .constants import RYDBERG_ENERGY, HARTREE_TO_EV
    
    # Normalize coefficients
    coefficients = normalize_superposition(coefficients)
    
    # Initialize
    psi_t = np.zeros_like(r, dtype=complex)
    
    # Add each state with time evolution
    for (n, l, m), coeff in zip(states, coefficients):
        validate_quantum_numbers(n, l, m)
        
        # Energy eigenvalue
        E_n = -RYDBERG_ENERGY / (n ** 2)  # in eV
        E_n_hartree = E_n / HARTREE_TO_EV  # convert to atomic units
        
        # Time evolution phase
        phase = np.exp(-1j * E_n_hartree * time)
        
        # Add to superposition
        psi_i = hydrogen_wave_function(r, theta, phi, n, l, m)
        psi_t += coeff * psi_i * phase
    
    return psi_t


def calculate_expectation_energy(states, coefficients):
    """
    Calculate expectation value of energy for superposition state.
    
    <E> = Σ |c_i|² * E_i
    
    Parameters
    ----------
    states : list of tuples
        List of (n, l, m) quantum number tuples
    coefficients : list of complex
        Complex coefficients
        
    Returns
    -------
    float
        Expectation value of energy in eV
    """
    from .constants import RYDBERG_ENERGY
    
    # Normalize coefficients
    coefficients = normalize_superposition(coefficients)
    
    # Calculate expectation value
    expectation = 0.0
    for (n, l, m), coeff in zip(states, coefficients):
        E_n = -RYDBERG_ENERGY / (n ** 2)
        expectation += np.abs(coeff) ** 2 * E_n
    
    return expectation


def calculate_uncertainty_energy(states, coefficients):
    """
    Calculate energy uncertainty (standard deviation) for superposition.
    
    ΔE = sqrt(<E²> - <E>²)
    
    Parameters
    ----------
    states : list of tuples
        List of (n, l, m) quantum number tuples
    coefficients : list of complex
        Complex coefficients
        
    Returns
    -------
    float
        Energy uncertainty in eV
    """
    from .constants import RYDBERG_ENERGY
    
    # Normalize coefficients
    coefficients = normalize_superposition(coefficients)
    
    # Calculate <E> and <E²>
    E_avg = 0.0
    E2_avg = 0.0
    
    for (n, l, m), coeff in zip(states, coefficients):
        E_n = -RYDBERG_ENERGY / (n ** 2)
        prob = np.abs(coeff) ** 2
        E_avg += prob * E_n
        E2_avg += prob * E_n ** 2
    
    # Uncertainty
    variance = E2_avg - E_avg ** 2
    uncertainty = np.sqrt(max(0, variance))  # Ensure non-negative
    
    return uncertainty


def get_dominant_state(states, coefficients):
    """
    Find the state with largest contribution to superposition.
    
    Parameters
    ----------
    states : list of tuples
        List of (n, l, m) quantum number tuples
    coefficients : list of complex
        Complex coefficients
        
    Returns
    -------
    tuple
        (dominant_state, probability) where dominant_state is (n, l, m)
    """
    # Normalize coefficients
    coefficients = normalize_superposition(coefficients)
    
    # Calculate probabilities
    probabilities = np.abs(coefficients) ** 2
    
    # Find maximum
    max_idx = np.argmax(probabilities)
    
    return states[max_idx], probabilities[max_idx]


def decompose_superposition(psi, states, r, theta, phi):
    """
    Decompose arbitrary wave function into basis states.
    
    This performs a projection to find coefficients c_i such that:
    ψ ≈ Σ c_i * ψ_i
    
    Parameters
    ----------
    psi : ndarray
        Wave function to decompose
    states : list of tuples
        Basis states (n, l, m)
    r, theta, phi : ndarray
        Coordinate grids
        
    Returns
    -------
    ndarray
        Coefficients for each basis state
    """
    coefficients = []
    
    for (n, l, m) in states:
        psi_i = hydrogen_wave_function(r, theta, phi, n, l, m)
        
        # Inner product <ψ_i|ψ>
        # Using volume element r² sin(θ) for spherical integration
        volume_element = r ** 2 * np.sin(theta)
        overlap = np.sum(np.conj(psi_i) * psi * volume_element)
        
        coefficients.append(overlap)
    
    return np.array(coefficients)


def generate_random_superposition(max_n=3, num_states=3):
    """
    Generate random superposition for testing/demonstration.
    
    Parameters
    ----------
    max_n : int
        Maximum principal quantum number
    num_states : int
        Number of states to include
        
    Returns
    -------
    tuple
        (states, coefficients) ready for use
    """
    states = []
    
    # Generate random valid quantum numbers
    for _ in range(num_states):
        n = np.random.randint(1, max_n + 1)
        l = np.random.randint(0, n)
        m = np.random.randint(-l, l + 1)
        states.append((n, l, m))
    
    # Generate random complex coefficients
    real_parts = np.random.randn(num_states)
    imag_parts = np.random.randn(num_states)
    coefficients = real_parts + 1j * imag_parts
    
    # Normalize
    coefficients = normalize_superposition(coefficients)
    
    return states, coefficients


def calculate_purity(coefficients):
    """
    Calculate purity of superposition state.
    
    Purity = Σ |c_i|⁴
    
    Purity = 1 for pure state (single component)
    Purity < 1 for mixed state
    
    Parameters
    ----------
    coefficients : array-like
        Complex coefficients
        
    Returns
    -------
    float
        Purity measure (0 < purity ≤ 1)
    """
    coefficients = normalize_superposition(coefficients)
    probabilities = np.abs(coefficients) ** 2
    purity = np.sum(probabilities ** 2)
    return purity