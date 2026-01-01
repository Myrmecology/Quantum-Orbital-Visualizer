"""
Interactive Controls for Quantum Visualizer
============================================

Creates Dash components for user interaction:
- Quantum number sliders
- Theme selectors
- Render mode controls
- Superposition state builders
"""

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import config


def create_quantum_number_controls():
    """
    Create sliders for quantum numbers n, l, m.
    
    Returns
    -------
    dash.html.Div
        Div containing all quantum number controls
    """
    controls = html.Div([
        # Principal quantum number (n)
        html.Div([
            html.Label("Principal Quantum Number (n)", 
                      style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            dcc.Slider(
                id='n-slider',
                min=config.N_MIN,
                max=config.N_MAX,
                step=1,
                value=2,
                marks={i: str(i) for i in range(config.N_MIN, config.N_MAX + 1)},
                tooltip={"placement": "bottom", "always_visible": True}
            ),
        ], style={'marginBottom': '30px'}),
        
        # Angular momentum quantum number (l)
        html.Div([
            html.Label("Angular Momentum Quantum Number (l)", 
                      style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            dcc.Slider(
                id='l-slider',
                min=0,
                max=config.L_MAX,
                step=1,
                value=1,
                marks={i: f"{i} ({config.ORBITAL_LETTERS.get(i, '?')})" 
                       for i in range(config.L_MAX + 1)},
                tooltip={"placement": "bottom", "always_visible": True}
            ),
        ], style={'marginBottom': '30px'}),
        
        # Magnetic quantum number (m)
        html.Div([
            html.Label("Magnetic Quantum Number (m)", 
                      style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            dcc.Slider(
                id='m-slider',
                min=-config.M_MAX,
                max=config.M_MAX,
                step=1,
                value=0,
                marks={i: str(i) for i in range(-config.M_MAX, config.M_MAX + 1)},
                tooltip={"placement": "bottom", "always_visible": True}
            ),
        ], style={'marginBottom': '30px'}),
        
        # Current orbital display
        html.Div([
            html.H4("Current Orbital:", style={'marginBottom': '10px'}),
            html.Div(id='current-orbital-display', 
                    style={'fontSize': '24px', 'fontWeight': 'bold', 'color': '#4CC9F0'})
        ], style={'marginTop': '20px', 'padding': '15px', 
                 'border': '2px solid #4CC9F0', 'borderRadius': '5px'})
    ], style={'padding': '20px'})
    
    return controls


def create_theme_selector():
    """
    Create dropdown for theme selection.
    
    Returns
    -------
    dash.html.Div
        Div containing theme selector
    """
    from visualizations.themes import AVAILABLE_THEMES, get_theme_description
    
    theme_options = [
        {'label': get_theme_description(theme), 'value': theme}
        for theme in AVAILABLE_THEMES
    ]
    
    selector = html.Div([
        html.Label("Visual Theme", style={'fontWeight': 'bold', 'marginBottom': '10px'}),
        dcc.Dropdown(
            id='theme-dropdown',
            options=theme_options,
            value=config.DEFAULT_THEME,
            clearable=False,
            style={'color': '#000000'}
        ),
        html.Div([
            html.Small("Choose your visual style", 
                      style={'color': '#888', 'fontStyle': 'italic'})
        ], style={'marginTop': '5px'})
    ], style={'padding': '20px'})
    
    return selector


def create_render_mode_selector():
    """
    Create buttons/dropdown for render mode selection.
    
    Returns
    -------
    dash.html.Div
        Div containing render mode controls
    """
    render_options = [
        {'label': 'Isosurface', 'value': 'isosurface'},
        {'label': 'Volume', 'value': 'volume'},
        {'label': 'Wireframe', 'value': 'wireframe'},
        {'label': 'Particle Swarm', 'value': 'particle_swarm'},
        {'label': 'Cross-Section', 'value': 'cross_section'}
    ]
    
    selector = html.Div([
        html.Label("Render Mode", style={'fontWeight': 'bold', 'marginBottom': '10px'}),
        dcc.Dropdown(
            id='render-mode-dropdown',
            options=render_options,
            value=config.DEFAULT_RENDER_MODE,
            clearable=False,
            style={'color': '#000000'}
        ),
        
        # Additional controls that appear based on render mode
        html.Div([
            html.Label("Isosurface Level", style={'fontWeight': 'bold', 'marginTop': '15px'}),
            dcc.Slider(
                id='iso-level-slider',
                min=0.001,
                max=0.1,
                step=0.001,
                value=config.DEFAULT_ISO_LEVEL,
                marks={0.001: '0.001', 0.05: '0.05', 0.1: '0.1'},
                tooltip={"placement": "bottom", "always_visible": True}
            ),
        ], id='iso-level-control', style={'marginTop': '15px'}),
        
        html.Div([
            html.Label("Grid Quality", style={'fontWeight': 'bold', 'marginTop': '15px'}),
            dcc.RadioItems(
                id='grid-quality-radio',
                options=[
                    {'label': ' Low (Fast)', 'value': config.GRID_POINTS_LOW},
                    {'label': ' Medium', 'value': config.GRID_POINTS_MEDIUM},
                    {'label': ' High (Slow)', 'value': config.GRID_POINTS_HIGH}
                ],
                value=config.DEFAULT_GRID_POINTS,
                inline=False,
                style={'marginTop': '10px'}
            )
        ], style={'marginTop': '15px'})
    ], style={'padding': '20px'})
    
    return selector


def create_superposition_builder():
    """
    Create interface for building superposition states.
    
    Returns
    -------
    dash.html.Div
        Div containing superposition builder controls
    """
    builder = html.Div([
        html.H4("Superposition Builder", style={'marginBottom': '15px'}),
        html.P("Combine multiple quantum states", style={'color': '#888', 'fontSize': '14px'}),
        
        # State 1
        html.Div([
            html.Label("State 1 (n, l, m):", style={'fontWeight': 'bold'}),
            html.Div([
                dcc.Input(id='state1-n', type='number', min=1, max=7, value=1, 
                         style={'width': '60px', 'marginRight': '5px'}),
                dcc.Input(id='state1-l', type='number', min=0, max=6, value=0, 
                         style={'width': '60px', 'marginRight': '5px'}),
                dcc.Input(id='state1-m', type='number', min=-6, max=6, value=0, 
                         style={'width': '60px'}),
            ], style={'display': 'flex', 'marginTop': '5px'}),
            html.Div([
                html.Label("Coefficient (real, imag):", style={'fontSize': '12px', 'marginTop': '5px'}),
                dcc.Input(id='state1-coeff-real', type='number', value=1.0, step=0.1,
                         style={'width': '80px', 'marginRight': '5px'}),
                dcc.Input(id='state1-coeff-imag', type='number', value=0.0, step=0.1,
                         style={'width': '80px'}),
            ], style={'display': 'flex', 'marginTop': '5px'})
        ], style={'marginBottom': '20px', 'padding': '10px', 
                 'border': '1px solid #4CC9F0', 'borderRadius': '5px'}),
        
        # State 2
        html.Div([
            html.Label("State 2 (n, l, m):", style={'fontWeight': 'bold'}),
            html.Div([
                dcc.Input(id='state2-n', type='number', min=1, max=7, value=2, 
                         style={'width': '60px', 'marginRight': '5px'}),
                dcc.Input(id='state2-l', type='number', min=0, max=6, value=0, 
                         style={'width': '60px', 'marginRight': '5px'}),
                dcc.Input(id='state2-m', type='number', min=-6, max=6, value=0, 
                         style={'width': '60px'}),
            ], style={'display': 'flex', 'marginTop': '5px'}),
            html.Div([
                html.Label("Coefficient (real, imag):", style={'fontSize': '12px', 'marginTop': '5px'}),
                dcc.Input(id='state2-coeff-real', type='number', value=1.0, step=0.1,
                         style={'width': '80px', 'marginRight': '5px'}),
                dcc.Input(id='state2-coeff-imag', type='number', value=0.0, step=0.1,
                         style={'width': '80px'}),
            ], style={'display': 'flex', 'marginTop': '5px'})
        ], style={'marginBottom': '20px', 'padding': '10px', 
                 'border': '1px solid #F72585', 'borderRadius': '5px'}),
        
        # Buttons
        html.Div([
            html.Button("Create Superposition", id='create-superposition-btn',
                       style={'backgroundColor': '#7209B7', 'color': 'white', 
                             'border': 'none', 'padding': '10px 20px', 
                             'borderRadius': '5px', 'cursor': 'pointer',
                             'marginRight': '10px'}),
            html.Button("Reset", id='reset-superposition-btn',
                       style={'backgroundColor': '#888', 'color': 'white', 
                             'border': 'none', 'padding': '10px 20px', 
                             'borderRadius': '5px', 'cursor': 'pointer'})
        ], style={'marginTop': '15px'}),
        
        # Status display
        html.Div(id='superposition-status', 
                style={'marginTop': '15px', 'padding': '10px', 
                      'backgroundColor': '#1B263B', 'borderRadius': '5px'})
    ], style={'padding': '20px'})
    
    return builder


def create_animation_controls():
    """
    Create controls for time evolution animation.
    
    Returns
    -------
    dash.html.Div
        Div containing animation controls
    """
    controls = html.Div([
        html.H4("Time Evolution", style={'marginBottom': '15px'}),
        
        html.Div([
            html.Label("Animation Speed", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            dcc.Slider(
                id='animation-speed-slider',
                min=1,
                max=10,
                step=1,
                value=5,
                marks={i: str(i) for i in range(1, 11)},
                tooltip={"placement": "bottom", "always_visible": True}
            ),
        ], style={'marginBottom': '20px'}),
        
        html.Div([
            html.Button("▶ Play", id='play-animation-btn',
                       style={'backgroundColor': '#4CC9F0', 'color': '#000', 
                             'border': 'none', 'padding': '10px 20px', 
                             'borderRadius': '5px', 'cursor': 'pointer',
                             'marginRight': '10px'}),
            html.Button("⏸ Pause", id='pause-animation-btn',
                       style={'backgroundColor': '#F72585', 'color': 'white', 
                             'border': 'none', 'padding': '10px 20px', 
                             'borderRadius': '5px', 'cursor': 'pointer',
                             'marginRight': '10px'}),
            html.Button("⏹ Stop", id='stop-animation-btn',
                       style={'backgroundColor': '#7209B7', 'color': 'white', 
                             'border': 'none', 'padding': '10px 20px', 
                             'borderRadius': '5px', 'cursor': 'pointer'})
        ]),
        
        # Animation interval component
        dcc.Interval(
            id='animation-interval',
            interval=1000,  # milliseconds
            n_intervals=0,
            disabled=True
        )
    ], style={'padding': '20px'})
    
    return controls


def create_export_controls():
    """
    Create controls for exporting visualizations.
    
    Returns
    -------
    dash.html.Div
        Div containing export controls
    """
    controls = html.Div([
        html.H4("Export Options", style={'marginBottom': '15px'}),
        
        html.Div([
            html.Label("Export Format", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            dcc.Dropdown(
                id='export-format-dropdown',
                options=[
                    {'label': 'PNG Image', 'value': 'png'},
                    {'label': 'Interactive HTML', 'value': 'html'},
                    {'label': 'Data (JSON)', 'value': 'json'}
                ],
                value='png',
                clearable=False,
                style={'color': '#000000'}
            ),
        ], style={'marginBottom': '15px'}),
        
        html.Button("📥 Download", id='export-btn',
                   style={'backgroundColor': '#00B4D8', 'color': 'white', 
                         'border': 'none', 'padding': '10px 20px', 
                         'borderRadius': '5px', 'cursor': 'pointer',
                         'width': '100%'}),
        
        # Download component
        dcc.Download(id='download-file')
    ], style={'padding': '20px'})
    
    return controls


def create_help_panel():
    """
    Create help/info panel with instructions.
    
    Returns
    -------
    dash.html.Div
        Div containing help information
    """
    panel = html.Div([
        html.H4("ℹ️ Quick Guide", style={'marginBottom': '15px'}),
        
        html.Div([
            html.H5("Quantum Numbers:", style={'color': '#4CC9F0'}),
            html.Ul([
                html.Li("n: Shell (energy level, 1-7)"),
                html.Li("l: Shape (0=s, 1=p, 2=d, 3=f)"),
                html.Li("m: Orientation (-l to +l)")
            ]),
            
            html.H5("Render Modes:", style={'color': '#4CC9F0', 'marginTop': '15px'}),
            html.Ul([
                html.Li("Isosurface: 3D probability surface"),
                html.Li("Volume: Volumetric cloud"),
                html.Li("Wireframe: Mesh structure"),
                html.Li("Particle Swarm: Monte Carlo dots")
            ]),
            
            html.H5("Tips:", style={'color': '#4CC9F0', 'marginTop': '15px'}),
            html.Ul([
                html.Li("Use lower grid quality for faster rendering"),
                html.Li("Try Vectrex theme for retro graphics"),
                html.Li("Build superpositions to see interference")
            ])
        ], style={'fontSize': '14px'})
    ], style={'padding': '20px', 'backgroundColor': '#0A0E27', 'borderRadius': '5px'})
    
    return panel


# Orbital letter mapping for display
from quantum_engine.orbitals import ORBITAL_LETTERS
config.ORBITAL_LETTERS = ORBITAL_LETTERS