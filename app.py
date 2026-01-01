"""
Quantum Orbital Visualizer - Main Application
==============================================

Interactive 3D quantum mechanics visualization application.
Displays hydrogen atom orbitals with real-time controls, measurements,
and gamification features.

Author: Your Name
Version: 0.1.0
"""

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# Import configuration
import config

# Import modules
from interactive.controls import (
    create_quantum_number_controls,
    create_theme_selector,
    create_render_mode_selector,
    create_superposition_builder,
    create_animation_controls,
    create_export_controls,
    create_help_panel
)

from interactive.measurements import create_measurement_tools
from interactive.games import create_game_ui, create_achievement_tracker, create_achievement_ui
from interactive.callbacks import register_all_callbacks

# Initialize Dash app with Bootstrap theme
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG],
    suppress_callback_exceptions=True,
    title="Quantum Orbital Visualizer"
)

# Server for deployment
server = app.server

# ========================================
# APPLICATION LAYOUT
# ========================================

app.layout = html.Div([
    
    # Header
    html.Div([
        html.H1("⚛️ QUANTUM ORBITAL VISUALIZER ⚛️",
                style={
                    'textAlign': 'center',
                    'color': '#4CC9F0',
                    'marginBottom': '10px',
                    'fontFamily': 'Courier New, monospace',
                    'textShadow': '0 0 10px #4CC9F0'
                }),
        html.P("Interactive 3D Visualization of Hydrogen Atom Wave Functions",
               style={
                   'textAlign': 'center',
                   'color': '#F72585',
                   'fontSize': '16px',
                   'marginBottom': '20px'
               })
    ], style={
        'backgroundColor': '#000814',
        'padding': '20px',
        'borderBottom': '3px solid #4CC9F0'
    }),
    
    # Main container
    dbc.Container([
        
        dbc.Row([
            
            # Left sidebar - Controls
            dbc.Col([
                
                # Tabs for different control sections
                dcc.Tabs(id='control-tabs', value='quantum-controls', children=[
                    
                    # Quantum Numbers Tab
                    dcc.Tab(label='⚛️ Quantum', value='quantum-controls', children=[
                        create_quantum_number_controls()
                    ], style={'backgroundColor': '#1B263B'}, 
                       selected_style={'backgroundColor': '#0A0E27'}),
                    
                    # Visualization Settings Tab
                    dcc.Tab(label='🎨 Visual', value='visual-controls', children=[
                        create_theme_selector(),
                        html.Hr(),
                        create_render_mode_selector()
                    ], style={'backgroundColor': '#1B263B'}, 
                       selected_style={'backgroundColor': '#0A0E27'}),
                    
                    # Superposition Tab
                    dcc.Tab(label='🌊 Superposition', value='superposition-controls', children=[
                        create_superposition_builder()
                    ], style={'backgroundColor': '#1B263B'}, 
                       selected_style={'backgroundColor': '#0A0E27'}),
                    
                    # Measurements Tab
                    dcc.Tab(label='🔬 Measure', value='measurement-controls', children=[
                        create_measurement_tools()
                    ], style={'backgroundColor': '#1B263B'}, 
                       selected_style={'backgroundColor': '#0A0E27'}),
                    
                    # Games Tab
                    dcc.Tab(label='🎮 Games', value='game-controls', children=[
                        create_game_ui()
                    ], style={'backgroundColor': '#1B263B'}, 
                       selected_style={'backgroundColor': '#0A0E27'}),
                    
                    # Help Tab
                    dcc.Tab(label='ℹ️ Help', value='help-panel', children=[
                        create_help_panel()
                    ], style={'backgroundColor': '#1B263B'}, 
                       selected_style={'backgroundColor': '#0A0E27'})
                    
                ], style={'marginBottom': '20px'}),
                
            ], width=3, style={
                'backgroundColor': '#0A0E27',
                'padding': '0',
                'height': '100vh',
                'overflowY': 'auto'
            }),
            
            # Main visualization area
            dbc.Col([
                
                # Main 3D plot
                dbc.Card([
                    dbc.CardHeader(html.H4("3D Orbital Visualization", 
                                          style={'margin': '0', 'color': '#4CC9F0'})),
                    dbc.CardBody([
                        dcc.Loading(
                            id="loading-3d",
                            type="circle",
                            color="#4CC9F0",
                            children=[
                                dcc.Graph(
                                    id='main-3d-plot',
                                    config={
                                        'displayModeBar': True,
                                        'displaylogo': False,
                                        'toImageButtonOptions': {
                                            'format': 'png',
                                            'filename': 'quantum_orbital',
                                            'height': 1200,
                                            'width': 1200,
                                            'scale': 2
                                        }
                                    },
                                    style={'height': '700px'}
                                )
                            ]
                        )
                    ])
                ], style={'marginBottom': '20px'}),
                
                # Charts row
                dbc.Row([
                    
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader(html.H5("Energy Levels", style={'margin': '0'})),
                            dbc.CardBody([
                                dcc.Graph(id='energy-level-chart', 
                                         config={'displayModeBar': False})
                            ])
                        ])
                    ], width=6),
                    
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader(html.H5("Radial Probability", style={'margin': '0'})),
                            dbc.CardBody([
                                dcc.Graph(id='radial-probability-chart',
                                         config={'displayModeBar': False})
                            ])
                        ])
                    ], width=6)
                    
                ], style={'marginBottom': '20px'}),
                
                # Second charts row
                dbc.Row([
                    
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader(html.H5("Angular Distribution", style={'margin': '0'})),
                            dbc.CardBody([
                                dcc.Graph(id='angular-momentum-pie',
                                         config={'displayModeBar': False})
                            ])
                        ])
                    ], width=4),
                    
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader(html.H5("Probability Heatmap", style={'margin': '0'})),
                            dbc.CardBody([
                                dcc.Graph(id='probability-heatmap',
                                         config={'displayModeBar': False})
                            ])
                        ])
                    ], width=4),
                    
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader(html.H5("Statistics", style={'margin': '0'})),
                            dbc.CardBody([
                                dcc.Graph(id='quantum-stats-table',
                                         config={'displayModeBar': False})
                            ])
                        ])
                    ], width=4)
                    
                ])
                
            ], width=9, style={'padding': '20px'})
            
        ])
        
    ], fluid=True, style={'padding': '0'}),
    
    # Footer
    html.Div([
        html.P([
            "Built with Python, Plotly, and Dash | ",
            html.A("Schrödinger Equation", 
                   href="https://en.wikipedia.org/wiki/Schr%C3%B6dinger_equation",
                   target="_blank",
                   style={'color': '#4CC9F0'}),
            " | ",
            f"Version {config.APP_VERSION}"
        ], style={
            'textAlign': 'center',
            'color': '#888',
            'margin': '0',
            'fontSize': '12px'
        })
    ], style={
        'backgroundColor': '#000814',
        'padding': '15px',
        'borderTop': '2px solid #4CC9F0',
        'position': 'fixed',
        'bottom': '0',
        'width': '100%',
        'zIndex': '1000'
    })
    
], style={
    'backgroundColor': '#000814',
    'minHeight': '100vh',
    'paddingBottom': '50px'
})


# ========================================
# REGISTER CALLBACKS
# ========================================

register_all_callbacks(app)


# ========================================
# ADDITIONAL STYLING
# ========================================

# Custom CSS for better appearance
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                margin: 0;
                padding: 0;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            }
            
            /* Custom scrollbar */
            ::-webkit-scrollbar {
                width: 10px;
            }
            
            ::-webkit-scrollbar-track {
                background: #1B263B;
            }
            
            ::-webkit-scrollbar-thumb {
                background: #4CC9F0;
                border-radius: 5px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: #7209B7;
            }
            
            /* Tab styling */
            .tab {
                color: #AAA !important;
            }
            
            .tab--selected {
                color: #4CC9F0 !important;
                border-bottom: 3px solid #4CC9F0 !important;
            }
            
            /* Card styling */
            .card {
                background-color: #1B263B !important;
                border: 1px solid #4CC9F0 !important;
            }
            
            .card-header {
                background-color: #0A0E27 !important;
                border-bottom: 2px solid #4CC9F0 !important;
                color: #4CC9F0 !important;
            }
            
            /* Input styling */
            input[type="number"] {
                background-color: #0A0E27 !important;
                color: #FFF !important;
                border: 1px solid #4CC9F0 !important;
                padding: 5px !important;
                border-radius: 3px !important;
            }
            
            /* Slider styling */
            .rc-slider-track {
                background-color: #4CC9F0 !important;
            }
            
            .rc-slider-handle {
                border-color: #4CC9F0 !important;
            }
            
            .rc-slider-handle:hover {
                border-color: #7209B7 !important;
            }
            
            /* Loading spinner */
            ._loading {
                color: #4CC9F0 !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''


# ========================================
# RUN APPLICATION
# ========================================

if __name__ == '__main__':
    print("=" * 60)
    print("⚛️  QUANTUM ORBITAL VISUALIZER")
    print("=" * 60)
    print(f"Version: {config.APP_VERSION}")
    print(f"Author: {config.APP_AUTHOR}")
    print("=" * 60)
    print("\n🚀 Starting application...")
    print("📡 Server running at: http://127.0.0.1:8050")
    print("\n💡 Tips:")
    print("   - Use sliders to change quantum numbers")
    print("   - Try different themes and render modes")
    print("   - Explore measurements and games!")
    print("\n" + "=" * 60 + "\n")
    
    app.run_server(
        debug=config.DEBUG_MODE,
        host='0.0.0.0',
        port=8050
    )