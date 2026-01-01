"""
Measurement Tools for Quantum Orbitals
=======================================

Interactive measurement tools for probing quantum states:
- Click-to-probe probability measurements
- Region selection and integration
- Uncertainty principle calculations
- Expected value calculations
"""

import numpy as np
from dash import html, dcc
import plotly.graph_objects as go


def measure_probability_at_point(grid_data, x, y, z):
    """
    Measure probability density at a specific point in space.
    
    Parameters
    ----------
    grid_data : dict
        Orbital grid data
    x, y, z : float
        Coordinates to measure (in Bohr radii)
        
    Returns
    -------
    dict
        Measurement results including probability, wave function values
    """
    from quantum_engine.schrodinger import (
        hydrogen_wave_function, 
        probability_density
    )
    
    # Convert to spherical coordinates
    r = np.sqrt(x**2 + y**2 + z**2)
    r = max(r, 1e-10)  # Avoid division by zero
    
    theta = np.arccos(z / r)
    phi = np.arctan2(y, x)
    
    # Get quantum numbers
    n, l, m = grid_data['quantum_numbers']
    
    # Calculate wave function and probability
    psi = hydrogen_wave_function(r, theta, phi, n, l, m)
    prob = probability_density(r, theta, phi, n, l, m)
    
    return {
        'coordinates': {'x': x, 'y': y, 'z': z},
        'spherical': {'r': r, 'theta': theta, 'phi': phi},
        'wave_function': psi,
        'psi_real': np.real(psi),
        'psi_imag': np.imag(psi),
        'psi_magnitude': np.abs(psi),
        'probability_density': prob,
        'quantum_numbers': (n, l, m)
    }


def calculate_region_probability(grid_data, x_range, y_range, z_range):
    """
    Calculate total probability within a specified region.
    
    Parameters
    ----------
    grid_data : dict
        Orbital grid data
    x_range, y_range, z_range : tuple
        (min, max) ranges for each coordinate
        
    Returns
    -------
    dict
        Region probability and statistics
    """
    # Get grid coordinates
    X = grid_data['x']
    Y = grid_data['y']
    Z = grid_data['z']
    prob = grid_data['prob_density']
    
    # Create mask for region
    mask = (
        (X >= x_range[0]) & (X <= x_range[1]) &
        (Y >= y_range[0]) & (Y <= y_range[1]) &
        (Z >= z_range[0]) & (Z <= z_range[1])
    )
    
    # Calculate volume element (assuming uniform grid)
    dx = X[1, 0, 0] - X[0, 0, 0]
    dy = Y[0, 1, 0] - Y[0, 0, 0]
    dz = Z[0, 0, 1] - Z[0, 0, 0]
    volume_element = abs(dx * dy * dz)
    
    # Calculate probability in region
    region_prob = prob[mask]
    total_probability = np.sum(region_prob) * volume_element
    
    return {
        'total_probability': total_probability,
        'region_volume': np.sum(mask) * volume_element,
        'num_points': np.sum(mask),
        'average_density': np.mean(region_prob) if len(region_prob) > 0 else 0,
        'max_density': np.max(region_prob) if len(region_prob) > 0 else 0,
        'x_range': x_range,
        'y_range': y_range,
        'z_range': z_range
    }


def uncertainty_calculator(grid_data):
    """
    Calculate position and momentum uncertainties (Heisenberg principle).
    
    ΔxΔp ≥ ℏ/2
    
    Parameters
    ----------
    grid_data : dict
        Orbital grid data
        
    Returns
    -------
    dict
        Uncertainty values and Heisenberg product
    """
    from quantum_engine.constants import HBAR
    from quantum_engine.schrodinger import expectation_value_r
    
    n, l, m = grid_data['quantum_numbers']
    
    # Get coordinate grids
    X = grid_data['x']
    Y = grid_data['y']
    Z = grid_data['z']
    R = grid_data['r']
    prob = grid_data['prob_density']
    
    # Normalize probability (should be ~1 already)
    dx = X[1, 0, 0] - X[0, 0, 0]
    dy = Y[0, 1, 0] - Y[0, 0, 0]
    dz = Z[0, 0, 1] - Z[0, 0, 0]
    volume_element = abs(dx * dy * dz)
    
    total_prob = np.sum(prob) * volume_element
    prob_norm = prob / total_prob if total_prob > 0 else prob
    
    # Calculate <x>, <x²> for position uncertainty
    x_avg = np.sum(X * prob_norm) * volume_element
    x2_avg = np.sum(X**2 * prob_norm) * volume_element
    delta_x = np.sqrt(max(0, x2_avg - x_avg**2))
    
    # Similarly for y and z
    y_avg = np.sum(Y * prob_norm) * volume_element
    y2_avg = np.sum(Y**2 * prob_norm) * volume_element
    delta_y = np.sqrt(max(0, y2_avg - y_avg**2))
    
    z_avg = np.sum(Z * prob_norm) * volume_element
    z2_avg = np.sum(Z**2 * prob_norm) * volume_element
    delta_z = np.sqrt(max(0, z2_avg - z_avg**2))
    
    # Radial uncertainty
    r_avg = expectation_value_r(n, l)
    r2_avg = np.sum(R**2 * prob_norm) * volume_element
    delta_r = np.sqrt(max(0, r2_avg - r_avg**2))
    
    # Momentum uncertainty (from energy-time uncertainty)
    # For hydrogen: Δp ~ ℏ/Δx (simplified)
    delta_px = HBAR / delta_x if delta_x > 0 else float('inf')
    delta_py = HBAR / delta_y if delta_y > 0 else float('inf')
    delta_pz = HBAR / delta_z if delta_z > 0 else float('inf')
    
    # Heisenberg products
    heisenberg_x = delta_x * delta_px / HBAR
    heisenberg_y = delta_y * delta_py / HBAR
    heisenberg_z = delta_z * delta_pz / HBAR
    
    return {
        'position_uncertainty': {
            'delta_x': delta_x,
            'delta_y': delta_y,
            'delta_z': delta_z,
            'delta_r': delta_r
        },
        'momentum_uncertainty': {
            'delta_px': delta_px,
            'delta_py': delta_py,
            'delta_pz': delta_pz
        },
        'heisenberg_products': {
            'x': heisenberg_x,
            'y': heisenberg_y,
            'z': heisenberg_z,
            'minimum': 0.5  # ℏ/2 in units of ℏ
        },
        'expectation_values': {
            'x': x_avg,
            'y': y_avg,
            'z': z_avg,
            'r': r_avg
        }
    }


def create_measurement_tools():
    """
    Create UI components for measurement tools.
    
    Returns
    -------
    dash.html.Div
        Div containing measurement tool interface
    """
    tools = html.Div([
        html.H4("🔬 Measurement Tools", style={'marginBottom': '15px'}),
        
        # Point measurement
        html.Div([
            html.H5("Point Probe", style={'color': '#4CC9F0', 'marginBottom': '10px'}),
            html.P("Click on the 3D plot to measure probability", 
                   style={'fontSize': '12px', 'color': '#888'}),
            
            html.Div([
                html.Label("Manual Coordinates (x, y, z):", style={'fontSize': '12px'}),
                html.Div([
                    dcc.Input(id='probe-x', type='number', placeholder='x', 
                             style={'width': '60px', 'marginRight': '5px'}),
                    dcc.Input(id='probe-y', type='number', placeholder='y', 
                             style={'width': '60px', 'marginRight': '5px'}),
                    dcc.Input(id='probe-z', type='number', placeholder='z', 
                             style={'width': '60px', 'marginRight': '5px'}),
                    html.Button("Measure", id='probe-btn', 
                               style={'padding': '5px 10px', 'fontSize': '12px'})
                ], style={'display': 'flex', 'marginTop': '5px'})
            ]),
            
            html.Div(id='point-measurement-result',
                    style={'marginTop': '10px', 'padding': '10px',
                          'backgroundColor': '#1B263B', 'borderRadius': '5px',
                          'fontSize': '12px'})
        ], style={'marginBottom': '25px', 'padding': '15px',
                 'border': '1px solid #4CC9F0', 'borderRadius': '5px'}),
        
        # Region selection
        html.Div([
            html.H5("Region Integration", style={'color': '#F72585', 'marginBottom': '10px'}),
            html.P("Calculate probability in a box region", 
                   style={'fontSize': '12px', 'color': '#888'}),
            
            html.Div([
                html.Label("X Range:", style={'fontSize': '12px'}),
                dcc.RangeSlider(
                    id='region-x-range',
                    min=-20, max=20, step=0.5, value=[-5, 5],
                    marks={-20: '-20', 0: '0', 20: '20'},
                    tooltip={"placement": "bottom", "always_visible": False}
                )
            ], style={'marginBottom': '10px'}),
            
            html.Div([
                html.Label("Y Range:", style={'fontSize': '12px'}),
                dcc.RangeSlider(
                    id='region-y-range',
                    min=-20, max=20, step=0.5, value=[-5, 5],
                    marks={-20: '-20', 0: '0', 20: '20'},
                    tooltip={"placement": "bottom", "always_visible": False}
                )
            ], style={'marginBottom': '10px'}),
            
            html.Div([
                html.Label("Z Range:", style={'fontSize': '12px'}),
                dcc.RangeSlider(
                    id='region-z-range',
                    min=-20, max=20, step=0.5, value=[-5, 5],
                    marks={-20: '-20', 0: '0', 20: '20'},
                    tooltip={"placement": "bottom", "always_visible": False}
                )
            ], style={'marginBottom': '10px'}),
            
            html.Button("Calculate", id='region-calc-btn',
                       style={'width': '100%', 'padding': '8px',
                             'backgroundColor': '#F72585', 'color': 'white',
                             'border': 'none', 'borderRadius': '5px',
                             'cursor': 'pointer'}),
            
            html.Div(id='region-measurement-result',
                    style={'marginTop': '10px', 'padding': '10px',
                          'backgroundColor': '#1B263B', 'borderRadius': '5px',
                          'fontSize': '12px'})
        ], style={'marginBottom': '25px', 'padding': '15px',
                 'border': '1px solid #F72585', 'borderRadius': '5px'}),
        
        # Uncertainty principle
        html.Div([
            html.H5("Heisenberg Uncertainty", style={'color': '#7209B7', 'marginBottom': '10px'}),
            html.P("Position-momentum uncertainty relation", 
                   style={'fontSize': '12px', 'color': '#888'}),
            
            html.Button("Calculate ΔxΔp", id='uncertainty-calc-btn',
                       style={'width': '100%', 'padding': '8px',
                             'backgroundColor': '#7209B7', 'color': 'white',
                             'border': 'none', 'borderRadius': '5px',
                             'cursor': 'pointer'}),
            
            html.Div(id='uncertainty-result',
                    style={'marginTop': '10px', 'padding': '10px',
                          'backgroundColor': '#1B263B', 'borderRadius': '5px',
                          'fontSize': '12px'})
        ], style={'padding': '15px', 'border': '1px solid #7209B7', 
                 'borderRadius': '5px'})
        
    ], style={'padding': '20px'})
    
    return tools


def format_measurement_result(measurement):
    """
    Format measurement result for display.
    
    Parameters
    ----------
    measurement : dict
        Measurement result dictionary
        
    Returns
    -------
    dash.html.Div
        Formatted display
    """
    coords = measurement['coordinates']
    spherical = measurement['spherical']
    
    result = html.Div([
        html.Strong("📍 Measurement Result"),
        html.Hr(style={'margin': '5px 0'}),
        html.P([
            html.Strong("Cartesian: "),
            f"({coords['x']:.2f}, {coords['y']:.2f}, {coords['z']:.2f}) a₀"
        ], style={'margin': '3px 0'}),
        html.P([
            html.Strong("Spherical: "),
            f"r={spherical['r']:.2f}, θ={spherical['theta']:.2f}, φ={spherical['phi']:.2f}"
        ], style={'margin': '3px 0'}),
        html.Hr(style={'margin': '5px 0'}),
        html.P([
            html.Strong("ψ (real): "),
            f"{measurement['psi_real']:.4e}"
        ], style={'margin': '3px 0'}),
        html.P([
            html.Strong("ψ (imag): "),
            f"{measurement['psi_imag']:.4e}"
        ], style={'margin': '3px 0'}),
        html.P([
            html.Strong("|ψ|: "),
            f"{measurement['psi_magnitude']:.4e}"
        ], style={'margin': '3px 0'}),
        html.P([
            html.Strong("Probability Density |ψ|²: "),
            f"{measurement['probability_density']:.4e}"
        ], style={'margin': '3px 0', 'color': '#4CC9F0', 'fontWeight': 'bold'})
    ])
    
    return result


def format_region_result(region):
    """
    Format region measurement result for display.
    
    Parameters
    ----------
    region : dict
        Region measurement result
        
    Returns
    -------
    dash.html.Div
        Formatted display
    """
    prob_percent = region['total_probability'] * 100
    
    result = html.Div([
        html.Strong("📦 Region Analysis"),
        html.Hr(style={'margin': '5px 0'}),
        html.P([
            html.Strong("Total Probability: "),
            f"{region['total_probability']:.4f} ({prob_percent:.2f}%)"
        ], style={'margin': '3px 0', 'color': '#4CC9F0', 'fontWeight': 'bold'}),
        html.P([
            html.Strong("Region Volume: "),
            f"{region['region_volume']:.2f} a₀³"
        ], style={'margin': '3px 0'}),
        html.P([
            html.Strong("Average Density: "),
            f"{region['average_density']:.4e}"
        ], style={'margin': '3px 0'}),
        html.P([
            html.Strong("Max Density: "),
            f"{region['max_density']:.4e}"
        ], style={'margin': '3px 0'}),
        html.P([
            html.Strong("Grid Points: "),
            f"{region['num_points']}"
        ], style={'margin': '3px 0'})
    ])
    
    return result


def format_uncertainty_result(uncertainty):
    """
    Format uncertainty calculation result for display.
    
    Parameters
    ----------
    uncertainty : dict
        Uncertainty calculation result
        
    Returns
    -------
    dash.html.Div
        Formatted display
    """
    pos = uncertainty['position_uncertainty']
    mom = uncertainty['momentum_uncertainty']
    heis = uncertainty['heisenberg_products']
    
    result = html.Div([
        html.Strong("⚛️ Uncertainty Principle"),
        html.Hr(style={'margin': '5px 0'}),
        
        html.P(html.Strong("Position Uncertainty:"), style={'margin': '8px 0 3px 0'}),
        html.P(f"Δx = {pos['delta_x']:.3f} a₀", style={'margin': '2px 0 2px 10px'}),
        html.P(f"Δy = {pos['delta_y']:.3f} a₀", style={'margin': '2px 0 2px 10px'}),
        html.P(f"Δz = {pos['delta_z']:.3f} a₀", style={'margin': '2px 0 2px 10px'}),
        html.P(f"Δr = {pos['delta_r']:.3f} a₀", style={'margin': '2px 0 2px 10px'}),
        
        html.P(html.Strong("Heisenberg Products (in units of ℏ):"), 
               style={'margin': '8px 0 3px 0'}),
        html.P(f"ΔxΔpₓ/ℏ = {heis['x']:.3f}", style={'margin': '2px 0 2px 10px'}),
        html.P(f"ΔyΔpᵧ/ℏ = {heis['y']:.3f}", style={'margin': '2px 0 2px 10px'}),
        html.P(f"ΔzΔp_z/ℏ = {heis['z']:.3f}", style={'margin': '2px 0 2px 10px'}),
        
        html.Hr(style={'margin': '5px 0'}),
        html.P([
            html.Strong("Minimum (ℏ/2): "),
            f"{heis['minimum']:.3f}"
        ], style={'margin': '3px 0', 'color': '#7209B7'}),
        
        # Check if uncertainty principle is satisfied
        html.P([
            "✓ Uncertainty principle satisfied!" if min(heis['x'], heis['y'], heis['z']) >= heis['minimum'] * 0.99
            else "⚠ Check calculations"
        ], style={'margin': '8px 0', 'color': '#4CC9F0', 'fontWeight': 'bold'})
    ])
    
    return result


def create_distance_ruler(grid_data, point1, point2):
    """
    Create distance measurement tool between two points.
    
    Parameters
    ----------
    grid_data : dict
        Orbital grid data
    point1, point2 : tuple
        (x, y, z) coordinates
        
    Returns
    -------
    dict
        Distance and probability along line
    """
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    
    # Calculate distance
    distance = np.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
    
    # Create line of points
    num_points = 100
    t = np.linspace(0, 1, num_points)
    
    x_line = x1 + t * (x2 - x1)
    y_line = y1 + t * (y2 - y1)
    z_line = z1 + t * (z2 - z1)
    
    # Calculate probability along line
    from quantum_engine.schrodinger import probability_density
    
    n, l, m = grid_data['quantum_numbers']
    
    r_line = np.sqrt(x_line**2 + y_line**2 + z_line**2)
    r_line = np.maximum(r_line, 1e-10)
    theta_line = np.arccos(z_line / r_line)
    phi_line = np.arctan2(y_line, x_line)
    
    prob_line = probability_density(r_line, theta_line, phi_line, n, l, m)
    
    return {
        'distance': distance,
        'point1': point1,
        'point2': point2,
        'line_coordinates': (x_line, y_line, z_line),
        'probability_profile': prob_line,
        'average_probability': np.mean(prob_line),
        'max_probability': np.max(prob_line)
    }