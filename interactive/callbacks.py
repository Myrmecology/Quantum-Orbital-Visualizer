"""
Dash Callbacks for Interactive Components
==========================================

Registers all callback functions to connect UI components with visualizations
and data processing.
"""

from dash import Input, Output, State, callback_context
import plotly.graph_objects as go
import numpy as np


def register_all_callbacks(app):
    """
    Register all Dash callbacks for the application.
    
    Parameters
    ----------
    app : dash.Dash
        Dash application instance
    """
    
    # ========================================
    # ORBITAL VISUALIZATION CALLBACKS
    # ========================================
    
    @app.callback(
        [Output('main-3d-plot', 'figure'),
         Output('current-orbital-display', 'children')],
        [Input('n-slider', 'value'),
         Input('l-slider', 'value'),
         Input('m-slider', 'value'),
         Input('render-mode-dropdown', 'value'),
         Input('iso-level-slider', 'value'),
         Input('grid-quality-radio', 'value'),
         Input('theme-dropdown', 'value')]
    )
    def update_orbital_visualization(n, l, m, render_mode, iso_level, grid_points, theme):
        """Update main 3D orbital visualization."""
        from quantum_engine.orbitals import (
            generate_orbital_grid, 
            validate_quantum_numbers,
            get_orbital_name
        )
        from visualizations.plotly_3d import create_3d_orbital
        
        # Validate quantum numbers
        try:
            validate_quantum_numbers(n, l, m)
        except ValueError as e:
            # Return empty figure with error message
            fig = go.Figure()
            fig.add_annotation(
                text=str(e),
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="red")
            )
            return fig, "Invalid quantum numbers"
        
        # Generate orbital grid
        grid_data = generate_orbital_grid(n, l, m, grid_points=grid_points)
        
        # Create visualization
        fig = create_3d_orbital(grid_data, mode=render_mode, iso_level=iso_level, theme=theme)
        
        # Get orbital name for display
        orbital_name = get_orbital_name(n, l, m)
        display_text = f"{orbital_name} (n={n}, l={l}, m={m})"
        
        return fig, display_text
    
    
    @app.callback(
        Output('l-slider', 'max'),
        Input('n-slider', 'value')
    )
    def update_l_max(n):
        """Update maximum l value based on n."""
        return n - 1
    
    
    @app.callback(
        Output('m-slider', 'max'),
        Output('m-slider', 'min'),
        Input('l-slider', 'value')
    )
    def update_m_range(l):
        """Update m range based on l."""
        return l, -l
    
    
    # ========================================
    # CHART CALLBACKS
    # ========================================
    
    @app.callback(
        Output('energy-level-chart', 'figure'),
        Input('theme-dropdown', 'value')
    )
    def update_energy_levels(theme):
        """Update energy level diagram."""
        from visualizations.charts import create_energy_level_diagram
        return create_energy_level_diagram(max_n=7, theme=theme)
    
    
    @app.callback(
        Output('radial-probability-chart', 'figure'),
        [Input('n-slider', 'value'),
         Input('l-slider', 'value'),
         Input('theme-dropdown', 'value')]
    )
    def update_radial_chart(n, l, theme):
        """Update radial probability chart."""
        from visualizations.charts import create_radial_probability_chart
        from quantum_engine.orbitals import validate_quantum_numbers
        
        try:
            validate_quantum_numbers(n, l, 0)
            return create_radial_probability_chart(n, l, theme=theme)
        except ValueError:
            return go.Figure()
    
    
    @app.callback(
        Output('angular-momentum-pie', 'figure'),
        [Input('l-slider', 'value'),
         Input('theme-dropdown', 'value')]
    )
    def update_angular_pie(l, theme):
        """Update angular momentum pie chart."""
        from visualizations.charts import create_angular_momentum_pie
        return create_angular_momentum_pie(l, theme=theme)
    
    
    @app.callback(
        Output('probability-heatmap', 'figure'),
        [Input('n-slider', 'value'),
         Input('l-slider', 'value'),
         Input('m-slider', 'value'),
         Input('theme-dropdown', 'value')]
    )
    def update_heatmap(n, l, m, theme):
        """Update probability heatmap."""
        from quantum_engine.orbitals import generate_orbital_grid, validate_quantum_numbers
        from visualizations.charts import create_probability_heatmap
        
        try:
            validate_quantum_numbers(n, l, m)
            grid_data = generate_orbital_grid(n, l, m, grid_points=100)
            return create_probability_heatmap(grid_data, plane='xy', theme=theme)
        except ValueError:
            return go.Figure()
    
    
    @app.callback(
        Output('quantum-stats-table', 'figure'),
        [Input('n-slider', 'value'),
         Input('l-slider', 'value'),
         Input('m-slider', 'value'),
         Input('theme-dropdown', 'value')]
    )
    def update_stats_table(n, l, m, theme):
        """Update quantum statistics table."""
        from quantum_engine.orbitals import generate_orbital_grid, validate_quantum_numbers
        from visualizations.charts import create_quantum_stats_table
        
        try:
            validate_quantum_numbers(n, l, m)
            grid_data = generate_orbital_grid(n, l, m, grid_points=50)
            return create_quantum_stats_table(grid_data, theme=theme)
        except ValueError:
            return go.Figure()
    
    
    # ========================================
    # MEASUREMENT CALLBACKS
    # ========================================
    
    @app.callback(
        Output('point-measurement-result', 'children'),
        [Input('probe-btn', 'n_clicks')],
        [State('probe-x', 'value'),
         State('probe-y', 'value'),
         State('probe-z', 'value'),
         State('n-slider', 'value'),
         State('l-slider', 'value'),
         State('m-slider', 'value')]
    )
    def measure_point(n_clicks, x, y, z, n, l, m):
        """Measure probability at specific point."""
        if n_clicks is None or x is None or y is None or z is None:
            return "Enter coordinates and click Measure"
        
        from quantum_engine.orbitals import generate_orbital_grid, validate_quantum_numbers
        from interactive.measurements import measure_probability_at_point, format_measurement_result
        
        try:
            validate_quantum_numbers(n, l, m)
            grid_data = generate_orbital_grid(n, l, m, grid_points=50)
            measurement = measure_probability_at_point(grid_data, x, y, z)
            return format_measurement_result(measurement)
        except Exception as e:
            return f"Error: {str(e)}"
    
    
    @app.callback(
        Output('region-measurement-result', 'children'),
        [Input('region-calc-btn', 'n_clicks')],
        [State('region-x-range', 'value'),
         State('region-y-range', 'value'),
         State('region-z-range', 'value'),
         State('n-slider', 'value'),
         State('l-slider', 'value'),
         State('m-slider', 'value')]
    )
    def measure_region(n_clicks, x_range, y_range, z_range, n, l, m):
        """Calculate probability in region."""
        if n_clicks is None:
            return "Set ranges and click Calculate"
        
        from quantum_engine.orbitals import generate_orbital_grid, validate_quantum_numbers
        from interactive.measurements import calculate_region_probability, format_region_result
        
        try:
            validate_quantum_numbers(n, l, m)
            grid_data = generate_orbital_grid(n, l, m, grid_points=100)
            region = calculate_region_probability(
                grid_data, 
                tuple(x_range), 
                tuple(y_range), 
                tuple(z_range)
            )
            return format_region_result(region)
        except Exception as e:
            return f"Error: {str(e)}"
    
    
    @app.callback(
        Output('uncertainty-result', 'children'),
        [Input('uncertainty-calc-btn', 'n_clicks')],
        [State('n-slider', 'value'),
         State('l-slider', 'value'),
         State('m-slider', 'value')]
    )
    def calculate_uncertainty(n_clicks, n, l, m):
        """Calculate Heisenberg uncertainty."""
        if n_clicks is None:
            return "Click to calculate uncertainties"
        
        from quantum_engine.orbitals import generate_orbital_grid, validate_quantum_numbers
        from interactive.measurements import uncertainty_calculator, format_uncertainty_result
        
        try:
            validate_quantum_numbers(n, l, m)
            grid_data = generate_orbital_grid(n, l, m, grid_points=80)
            uncertainty = uncertainty_calculator(grid_data)
            return format_uncertainty_result(uncertainty)
        except Exception as e:
            return f"Error: {str(e)}"
    
    
    # ========================================
    # SUPERPOSITION CALLBACKS
    # ========================================
    
    @app.callback(
        Output('superposition-status', 'children'),
        [Input('create-superposition-btn', 'n_clicks')],
        [State('state1-n', 'value'),
         State('state1-l', 'value'),
         State('state1-m', 'value'),
         State('state1-coeff-real', 'value'),
         State('state1-coeff-imag', 'value'),
         State('state2-n', 'value'),
         State('state2-l', 'value'),
         State('state2-m', 'value'),
         State('state2-coeff-real', 'value'),
         State('state2-coeff-imag', 'value')]
    )
    def create_superposition(n_clicks, n1, l1, m1, c1r, c1i, n2, l2, m2, c2r, c2i):
        """Create superposition state."""
        if n_clicks is None:
            return "Configure states and click Create Superposition"
        
        from quantum_engine.superposition import (
            create_superposition as create_sup,
            normalize_superposition,
            calculate_expectation_energy
        )
        from quantum_engine.orbitals import validate_quantum_numbers, get_orbital_name
        
        try:
            # Validate states
            validate_quantum_numbers(n1, l1, m1)
            validate_quantum_numbers(n2, l2, m2)
            
            # Create coefficients
            states = [(n1, l1, m1), (n2, l2, m2)]
            coefficients = [c1r + 1j*c1i, c2r + 1j*c2i]
            
            # Normalize
            norm_coeffs = normalize_superposition(coefficients)
            
            # Calculate expectation energy
            exp_energy = calculate_expectation_energy(states, norm_coeffs)
            
            # Format result
            orbital1 = get_orbital_name(n1, l1, m1)
            orbital2 = get_orbital_name(n2, l2, m2)
            
            result = [
                f"✓ Superposition created!",
                f"States: {orbital1} + {orbital2}",
                f"Normalized coefficients:",
                f"  c₁ = {norm_coeffs[0]:.3f}",
                f"  c₂ = {norm_coeffs[1]:.3f}",
                f"⟨E⟩ = {exp_energy:.3f} eV"
            ]
            
            return [item + "\n" for item in result]
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    
    # ========================================
    # THEME CONTROL
    # ========================================
    
    @app.callback(
        Output('iso-level-control', 'style'),
        Input('render-mode-dropdown', 'value')
    )
    def toggle_iso_control(render_mode):
        """Show/hide iso level control based on render mode."""
        if render_mode in ['isosurface', 'wireframe']:
            return {'marginTop': '15px', 'display': 'block'}
        return {'marginTop': '15px', 'display': 'none'}
    
    
    # ========================================
    # CHALLENGE/GAME CALLBACKS
    # ========================================
    
    @app.callback(
        Output('challenge-display', 'children'),
        [Input('start-challenge-btn', 'n_clicks')],
        [State('challenge-type-dropdown', 'value'),
         State('difficulty-selector', 'value')]
    )
    def start_challenge(n_clicks, challenge_type, difficulty):
        """Start a new challenge."""
        if n_clicks is None:
            return "Click 'Start Challenge' to begin!"
        
        from interactive.games import generate_challenge
        from dash import dcc, html
        
        challenge = generate_challenge(challenge_type, difficulty)
        
        if challenge['type'] == 'orbital_matching':
            return html.Div([
                html.H5("🎯 Identify This Orbital!", style={'color': '#4CC9F0'}),
                html.P(f"Difficulty: {difficulty.capitalize()}", style={'fontSize': '12px', 'color': '#888'}),
                html.Hr(),
                html.P("Look at the visualization above and identify the quantum numbers:"),
                html.Div([
                    dcc.RadioItems(
                        id='challenge-answer',
                        options=challenge['options'],
                        style={'marginTop': '10px'}
                    )
                ]),
                html.Button("Submit Answer", id='submit-answer-btn',
                           style={'marginTop': '15px', 'padding': '8px 20px',
                                 'backgroundColor': '#7209B7', 'color': 'white',
                                 'border': 'none', 'borderRadius': '5px'}),
                html.Div(id='answer-feedback', style={'marginTop': '10px'})
            ])
        
        return "Challenge loaded!"


def update_orbital_callback(app):
    """Legacy function - kept for compatibility."""
    pass


def update_theme_callback(app):
    """Legacy function - kept for compatibility."""
    pass


def measurement_callback(app):
    """Legacy function - kept for compatibility."""
    pass