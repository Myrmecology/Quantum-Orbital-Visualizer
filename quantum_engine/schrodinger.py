"""
Schrödinger Equation Solutions for Hydrogen Atom
=================================================

Implements analytical solutions to the time-independent Schrödinger equation
for the hydrogen atom, including radial wave functions, spherical harmonics,
and complete wave function calculations.
"""

import numpy as np
from scipy.special import sph_harm, genlaguerre, factorial
from scipy.integrate import simps
import config


def radial_wave_function(r, n, l):
    """
    Calculate the radial wave function R_n,l(r) for hydrogen atom.
    
    The radial wave function is given by:
    R_n,l(r) = sqrt[(2/na₀)³ * (n-l-1)! / (2n[(n+l)!])] * 
               exp(-r/na₀) * (2r/na₀)^l * L^(2l+1)_(n-l-1)(2r/na₀)
    
    Parameters
    ----------
    r : float or ndarray
        Radial distance from nucleus (in Bohr radii)
    n : int
        Principal quantum number (n ≥ 1)
    l : int
        Angular momentum quantum number (0 ≤ l < n)
        
    Returns
    -------
    float or ndarray
        Radial wave function value(s)
    """
    # Validate quantum numbers
    if n < 1:
        raise ValueError("n must be >= 1")
    if l < 0 or l >= n:
        raise ValueError(f"l must satisfy 0 <= l < n, got l={l}, n={n}")
    
    # Convert to array for vectorized operations
    r = np.asarray(r, dtype=float)
    
    # Avoid division by zero
    r = np.where(r == 0, 1e-10, r)
    
    # Normalization constant
    a0 = 1.0  # In atomic units, Bohr radius = 1
    rho = 2.0 * r / (n * a0)
    
    # Normalization factor
    norm = np.sqrt(
        (2.0 / (n * a0)) ** 3 * 
        factorial(n - l - 1) / 
        (2.0 * n * factorial(n + l))
    )
    
    # Exponential and power terms
    exp_term = np.exp(-rho / 2.0)
    power_term = rho ** l
    
    # Associated Laguerre polynomial L^(2l+1)_(n-l-1)(rho)
    laguerre_poly = genlaguerre(n - l - 1, 2 * l + 1)
    laguerre_term = laguerre_poly(rho)
    
    # Complete radial wave function
    R_nl = norm * exp_term * power_term * laguerre_term
    
    return R_nl


def spherical_harmonic(theta, phi, l, m):
    """
    Calculate spherical harmonic Y_l^m(θ, φ).
    
    Uses scipy's sph_harm which implements:
    Y_l^m(θ,φ) = sqrt[(2l+1)/(4π) * (l-m)!/(l+m)!] * P_l^m(cos θ) * exp(imφ)
    
    Parameters
    ----------
    theta : float or ndarray
        Polar angle (0 to π)
    phi : float or ndarray
        Azimuthal angle (0 to 2π)
    l : int
        Angular momentum quantum number (l ≥ 0)
    m : int
        Magnetic quantum number (-l ≤ m ≤ l)
        
    Returns
    -------
    complex or ndarray
        Spherical harmonic value(s)
    """
    # Validate quantum numbers
    if l < 0:
        raise ValueError("l must be >= 0")
    if abs(m) > l:
        raise ValueError(f"m must satisfy -l <= m <= l, got m={m}, l={l}")
    
    # Note: scipy.special.sph_harm uses (m, l, phi, theta) order
    Y_lm = sph_harm(m, l, phi, theta)
    
    return Y_lm


def hydrogen_wave_function(r, theta, phi, n, l, m):
    """
    Calculate complete hydrogen atom wave function ψ_nlm(r, θ, φ).
    
    ψ_nlm(r,θ,φ) = R_n,l(r) * Y_l^m(θ,φ)
    
    Parameters
    ----------
    r : float or ndarray
        Radial distance (in Bohr radii)
    theta : float or ndarray
        Polar angle (0 to π)
    phi : float or ndarray
        Azimuthal angle (0 to 2π)
    n : int
        Principal quantum number (n ≥ 1)
    l : int
        Angular momentum quantum number (0 ≤ l < n)
    m : int
        Magnetic quantum number (-l ≤ m ≤ l)
        
    Returns
    -------
    complex or ndarray
        Complete wave function ψ_nlm
    """
    # Calculate radial and angular parts
    R_nl = radial_wave_function(r, n, l)
    Y_lm = spherical_harmonic(theta, phi, l, m)
    
    # Complete wave function
    psi_nlm = R_nl * Y_lm
    
    return psi_nlm


def probability_density(r, theta, phi, n, l, m):
    """
    Calculate probability density |ψ_nlm|² at given coordinates.
    
    Parameters
    ----------
    r : float or ndarray
        Radial distance (in Bohr radii)
    theta : float or ndarray
        Polar angle (0 to π)
    phi : float or ndarray
        Azimuthal angle (0 to 2π)
    n : int
        Principal quantum number
    l : int
        Angular momentum quantum number
    m : int
        Magnetic quantum number
        
    Returns
    -------
    float or ndarray
        Probability density |ψ|²
    """
    psi = hydrogen_wave_function(r, theta, phi, n, l, m)
    return np.abs(psi) ** 2


def radial_probability_density(r, n, l):
    """
    Calculate radial probability density P(r) = r² * |R_n,l(r)|².
    
    This gives the probability of finding the electron at distance r
    (integrated over all angles).
    
    Parameters
    ----------
    r : float or ndarray
        Radial distance (in Bohr radii)
    n : int
        Principal quantum number
    l : int
        Angular momentum quantum number
        
    Returns
    -------
    float or ndarray
        Radial probability density
    """
    R_nl = radial_wave_function(r, n, l)
    return r ** 2 * np.abs(R_nl) ** 2


def angular_probability_density(theta, phi, l, m):
    """
    Calculate angular probability density |Y_l^m(θ,φ)|².
    
    Parameters
    ----------
    theta : float or ndarray
        Polar angle (0 to π)
    phi : float or ndarray
        Azimuthal angle (0 to 2π)
    l : int
        Angular momentum quantum number
    m : int
        Magnetic quantum number
        
    Returns
    -------
    float or ndarray
        Angular probability density
    """
    Y_lm = spherical_harmonic(theta, phi, l, m)
    return np.abs(Y_lm) ** 2


def expectation_value_r(n, l):
    """
    Calculate expectation value <r> for given quantum state.
    
    For hydrogen atom:
    <r> = (a₀/2) * [3n² - l(l+1)]
    
    Parameters
    ----------
    n : int
        Principal quantum number
    l : int
        Angular momentum quantum number
        
    Returns
    -------
    float
        Expectation value of r (in Bohr radii)
    """
    a0 = 1.0  # Bohr radius in atomic units
    return (a0 / 2.0) * (3 * n**2 - l * (l + 1))


def most_probable_radius(n, l):
    """
    Calculate most probable radius (maximum of radial probability).
    
    For hydrogen atom, this is approximately:
    r_max ≈ n² * a₀ for l = n-1
    
    Parameters
    ----------
    n : int
        Principal quantum number
    l : int
        Angular momentum quantum number
        
    Returns
    -------
    float
        Most probable radius (in Bohr radii)
    """
    # Create radial grid
    r_grid = np.linspace(0, 5 * n**2, 1000)
    
    # Calculate radial probability density
    P_r = radial_probability_density(r_grid, n, l)
    
    # Find maximum
    max_idx = np.argmax(P_r)
    return r_grid[max_idx]


def verify_normalization(n, l, m, r_max=50, num_points=100):
    """
    Verify that wave function is normalized (integral = 1).
    
    Integrates |ψ|² over all space in spherical coordinates.
    
    Parameters
    ----------
    n, l, m : int
        Quantum numbers
    r_max : float
        Maximum radius for integration
    num_points : int
        Number of grid points per dimension
        
    Returns
    -------
    float
        Integral value (should be ≈ 1 if normalized)
    """
    # Create integration grid
    r = np.linspace(0, r_max, num_points)
    theta = np.linspace(0, np.pi, num_points)
    phi = np.linspace(0, 2*np.pi, num_points)
    
    R, THETA, PHI = np.meshgrid(r, theta, phi, indexing='ij')
    
    # Calculate probability density
    prob_density = probability_density(R, THETA, PHI, n, l, m)
    
    # Volume element in spherical coordinates: r² sin(θ) dr dθ dφ
    volume_element = R**2 * np.sin(THETA)
    integrand = prob_density * volume_element
    
    # Integrate using Simpson's rule
    dr = r[1] - r[0]
    dtheta = theta[1] - theta[0]
    dphi = phi[1] - phi[0]
    
    integral = simps(simps(simps(integrand, phi), theta), r)
    
    return integral