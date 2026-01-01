"""
Test Suite for Quantum Engine
==============================

Tests for quantum mechanics calculations including:
- Schrödinger equation solutions
- Orbital generation
- Superposition states
- Physical constants
"""

import pytest
import numpy as np
from tests import TEST_GRID_POINTS, TEST_SPATIAL_EXTENT, TEST_TOLERANCE, TEST_STATES


# ========================================
# CONSTANTS TESTS
# ========================================

def test_constants_import():
    """Test that physical constants can be imported."""
    from quantum_engine.constants import (
        BOHR_RADIUS, RYDBERG_ENERGY, HBAR, ELECTRON_MASS
    )
    
    assert BOHR_RADIUS > 0
    assert RYDBERG_ENERGY > 0
    assert HBAR > 0
    assert ELECTRON_MASS > 0


def test_unit_conversions():
    """Test unit conversion functions."""
    from quantum_engine.constants import (
        atomic_units_to_si, si_to_atomic_units
    )
    
    # Test round-trip conversion
    value = 5.0
    si_value = atomic_units_to_si(value, 'length')
    au_value = si_to_atomic_units(si_value, 'length')
    
    assert np.isclose(au_value, value, rtol=TEST_TOLERANCE)


def test_energy_level_calculation():
    """Test hydrogen energy level calculation."""
    from quantum_engine.constants import get_energy_level_ev, RYDBERG_ENERGY
    
    # Ground state energy should be -13.6 eV
    E1 = get_energy_level_ev(1)
    assert np.isclose(E1, -RYDBERG_ENERGY, rtol=TEST_TOLERANCE)
    
    # n=2 should be -3.4 eV
    E2 = get_energy_level_ev(2)
    assert np.isclose(E2, -RYDBERG_ENERGY / 4, rtol=TEST_TOLERANCE)


# ========================================
# SCHRÖDINGER EQUATION TESTS
# ========================================

def test_radial_wave_function():
    """Test radial wave function calculation."""
    from quantum_engine.schrodinger import radial_wave_function
    
    r = np.linspace(0.1, 10, 50)
    
    # Test 1s orbital
    R_1s = radial_wave_function(r, 1, 0)
    assert R_1s.shape == r.shape
    assert np.all(np.isfinite(R_1s))
    
    # Test 2p orbital
    R_2p = radial_wave_function(r, 2, 1)
    assert R_2p.shape == r.shape
    assert np.all(np.isfinite(R_2p))


def test_spherical_harmonic():
    """Test spherical harmonic calculation."""
    from quantum_engine.schrodinger import spherical_harmonic
    
    theta = np.linspace(0, np.pi, 30)
    phi = np.linspace(0, 2*np.pi, 30)
    
    # Test s orbital (l=0, m=0)
    Y_00 = spherical_harmonic(theta, phi, 0, 0)
    assert Y_00.shape == theta.shape
    assert np.all(np.isfinite(Y_00))
    
    # Test p orbital (l=1, m=0)
    Y_10 = spherical_harmonic(theta, phi, 1, 0)
    assert Y_10.shape == theta.shape
    assert np.all(np.isfinite(Y_10))


def test_hydrogen_wave_function():
    """Test complete hydrogen wave function."""
    from quantum_engine.schrodinger import hydrogen_wave_function
    
    r = np.array([1.0, 2.0, 3.0])
    theta = np.array([np.pi/4, np.pi/2, 3*np.pi/4])
    phi = np.array([0, np.pi/2, np.pi])
    
    # Test 1s orbital
    psi_1s = hydrogen_wave_function(r, theta, phi, 1, 0, 0)
    assert psi_1s.shape == r.shape
    assert np.all(np.isfinite(psi_1s))


def test_probability_density():
    """Test probability density calculation."""
    from quantum_engine.schrodinger import probability_density
    
    r = np.array([1.0, 2.0, 3.0])
    theta = np.array([np.pi/4, np.pi/2, 3*np.pi/4])
    phi = np.array([0, np.pi/2, np.pi])
    
    prob = probability_density(r, theta, phi, 1, 0, 0)
    
    assert prob.shape == r.shape
    assert np.all(prob >= 0)  # Probability must be non-negative
    assert np.all(np.isfinite(prob))


def test_radial_probability_density():
    """Test radial probability density."""
    from quantum_engine.schrodinger import radial_probability_density
    
    r = np.linspace(0.1, 10, 100)
    
    # Test 1s orbital
    P_1s = radial_probability_density(r, 1, 0)
    assert P_1s.shape == r.shape
    assert np.all(P_1s >= 0)
    assert np.all(np.isfinite(P_1s))
    
    # Maximum should be around 1 Bohr radius for 1s
    max_idx = np.argmax(P_1s)
    assert 0.5 < r[max_idx] < 1.5


# ========================================
# ORBITAL TESTS
# ========================================

def test_quantum_number_validation():
    """Test quantum number validation."""
    from quantum_engine.orbitals import validate_quantum_numbers
    
    # Valid quantum numbers
    assert validate_quantum_numbers(1, 0, 0) == True
    assert validate_quantum_numbers(2, 1, 0) == True
    assert validate_quantum_numbers(3, 2, -1) == True
    
    # Invalid quantum numbers
    with pytest.raises(ValueError):
        validate_quantum_numbers(0, 0, 0)  # n must be >= 1
    
    with pytest.raises(ValueError):
        validate_quantum_numbers(2, 2, 0)  # l must be < n
    
    with pytest.raises(ValueError):
        validate_quantum_numbers(2, 1, 2)  # |m| must be <= l


def test_orbital_name():
    """Test orbital naming convention."""
    from quantum_engine.orbitals import get_orbital_name
    
    assert '1s' in get_orbital_name(1, 0, 0)
    assert '2s' in get_orbital_name(2, 0, 0)
    assert '2p' in get_orbital_name(2, 1, 0)
    assert '3d' in get_orbital_name(3, 2, 0)


def test_orbital_energy():
    """Test orbital energy calculation."""
    from quantum_engine.orbitals import calculate_orbital_energy
    from quantum_engine.constants import RYDBERG_ENERGY
    
    E1 = calculate_orbital_energy(1)
    assert np.isclose(E1, -RYDBERG_ENERGY, rtol=TEST_TOLERANCE)
    
    E2 = calculate_orbital_energy(2)
    assert E2 > E1  # Higher n means less negative (higher) energy


def test_generate_orbital_grid():
    """Test orbital grid generation."""
    from quantum_engine.orbitals import generate_orbital_grid
    
    grid_data = generate_orbital_grid(
        1, 0, 0, 
        grid_points=TEST_GRID_POINTS, 
        spatial_extent=TEST_SPATIAL_EXTENT
    )
    
    # Check that all required keys are present
    required_keys = ['x', 'y', 'z', 'r', 'theta', 'phi', 
                     'psi', 'prob_density', 'quantum_numbers', 'energy']
    for key in required_keys:
        assert key in grid_data
    
    # Check shapes
    assert grid_data['x'].shape == (TEST_GRID_POINTS, TEST_GRID_POINTS, TEST_GRID_POINTS)
    assert grid_data['prob_density'].shape == (TEST_GRID_POINTS, TEST_GRID_POINTS, TEST_GRID_POINTS)
    
    # Check probability is non-negative
    assert np.all(grid_data['prob_density'] >= 0)


@pytest.mark.parametrize("n,l,m", TEST_STATES)
def test_multiple_orbitals(n, l, m):
    """Test generation of multiple orbital states."""
    from quantum_engine.orbitals import generate_orbital_grid
    
    grid_data = generate_orbital_grid(
        n, l, m,
        grid_points=TEST_GRID_POINTS,
        spatial_extent=TEST_SPATIAL_EXTENT
    )
    
    assert grid_data is not None
    assert grid_data['quantum_numbers'] == (n, l, m)
    assert np.all(np.isfinite(grid_data['prob_density']))


# ========================================
# SUPERPOSITION TESTS
# ========================================

def test_normalize_superposition():
    """Test coefficient normalization."""
    from quantum_engine.superposition import normalize_superposition
    
    coeffs = [1.0, 1.0]
    norm_coeffs = normalize_superposition(coeffs)
    
    # Check normalization
    total = np.sum(np.abs(norm_coeffs) ** 2)
    assert np.isclose(total, 1.0, rtol=TEST_TOLERANCE)


def test_create_superposition():
    """Test superposition state creation."""
    from quantum_engine.superposition import create_superposition
    
    states = [(1, 0, 0), (2, 0, 0)]
    coefficients = [1.0, 1.0]
    
    # Create coordinate grids
    r = np.linspace(0.1, 10, 20)
    theta = np.linspace(0, np.pi, 20)
    phi = np.linspace(0, 2*np.pi, 20)
    R, THETA, PHI = np.meshgrid(r, theta, phi, indexing='ij')
    
    psi_super = create_superposition(states, coefficients, R, THETA, PHI)
    
    assert psi_super.shape == R.shape
    assert np.all(np.isfinite(psi_super))


def test_expectation_energy():
    """Test expectation value of energy."""
    from quantum_engine.superposition import calculate_expectation_energy
    from quantum_engine.constants import RYDBERG_ENERGY
    
    # Equal superposition of 1s and 2s
    states = [(1, 0, 0), (2, 0, 0)]
    coefficients = [1.0, 1.0]
    
    exp_energy = calculate_expectation_energy(states, coefficients)
    
    # Should be between -13.6 and -3.4 eV
    assert -RYDBERG_ENERGY < exp_energy < -RYDBERG_ENERGY / 4


def test_purity():
    """Test purity calculation."""
    from quantum_engine.superposition import calculate_purity
    
    # Pure state (single component)
    pure_coeffs = [1.0, 0.0]
    purity_pure = calculate_purity(pure_coeffs)
    assert np.isclose(purity_pure, 1.0, rtol=TEST_TOLERANCE)
    
    # Mixed state
    mixed_coeffs = [1.0, 1.0]
    purity_mixed = calculate_purity(mixed_coeffs)
    assert purity_mixed < 1.0


# ========================================
# EDGE CASE TESTS
# ========================================

def test_zero_radius_handling():
    """Test that zero radius is handled properly."""
    from quantum_engine.schrodinger import radial_wave_function
    
    r = np.array([0.0, 1.0, 2.0])
    R = radial_wave_function(r, 1, 0)
    
    # Should not have NaN or inf
    assert np.all(np.isfinite(R))


def test_large_quantum_numbers():
    """Test handling of large quantum numbers."""
    from quantum_engine.orbitals import generate_orbital_grid
    
    # Test n=5
    grid_data = generate_orbital_grid(
        5, 2, 0,
        grid_points=20,
        spatial_extent=50.0
    )
    
    assert grid_data is not None
    assert np.all(np.isfinite(grid_data['prob_density']))


def test_negative_energy():
    """Test that bound states have negative energy."""
    from quantum_engine.orbitals import calculate_orbital_energy
    
    for n in range(1, 8):
        E = calculate_orbital_energy(n)
        assert E < 0  # Bound states have negative energy


# ========================================
# INTEGRATION TESTS
# ========================================

def test_full_workflow():
    """Test complete workflow from quantum numbers to visualization data."""
    from quantum_engine.orbitals import generate_orbital_grid, get_orbital_name
    
    # Generate orbital
    grid_data = generate_orbital_grid(
        2, 1, 0,
        grid_points=TEST_GRID_POINTS,
        spatial_extent=TEST_SPATIAL_EXTENT
    )
    
    # Check all components
    assert grid_data['orbital_name'] == get_orbital_name(2, 1, 0)
    assert grid_data['energy'] < 0
    assert np.max(grid_data['prob_density']) > 0
    
    # Check coordinate system consistency
    X, Y, Z = grid_data['x'], grid_data['y'], grid_data['z']
    R_check = np.sqrt(X**2 + Y**2 + Z**2)
    assert np.allclose(R_check, grid_data['r'], rtol=TEST_TOLERANCE)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])