"""
Vectrex-Style Retro Graphics
=============================

Creates retro vector graphics inspired by the Vectrex console.
Features glowing green lines, CRT scanline effects, and wireframe aesthetics.
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import config


def apply_vectrex_style(fig):
    """
    Apply Vectrex CRT styling to existing figure.
    
    Parameters
    ----------
    fig : plotly.graph_objects.Figure
        Figure to style
        
    Returns
    -------
    plotly.graph_objects.Figure
        Styled figure
    """
    from .themes import get_theme_colors
    
    colors = get_theme_colors('vectrex')
    
    # Update all traces to use glowing green
    for trace in fig.data:
        if hasattr(trace, 'line'):
            trace.line.color = colors['primary']
            trace.line.width = 2
        if hasattr(trace, 'marker'):
            trace.marker.color = colors['primary']
            trace.marker.line = dict(color=colors['accent'], width=1)
    
    # Update layout with Vectrex theme
    fig.update_layout(
        paper_bgcolor=colors['background'],
        plot_bgcolor=colors['background'],
        font=dict(color=colors['primary'], family='Courier New, monospace'),
        title=dict(font=dict(color=colors['primary'], size=24))
    )
    
    # Update axes
    fig.update_xaxes(
        gridcolor=colors['grid'],
        color=colors['primary'],
        showgrid=True,
        gridwidth=1
    )
    fig.update_yaxes(
        gridcolor=colors['grid'],
        color=colors['primary'],
        showgrid=True,
        gridwidth=1
    )
    
    return fig


def create_vectrex_orbital(grid_data, num_contours=8):
    """
    Create Vectrex-style wireframe orbital visualization.
    
    Parameters
    ----------
    grid_data : dict
        Orbital grid data
    num_contours : int
        Number of contour levels to display
        
    Returns
    -------
    plotly.graph_objects.Figure
    """
    from .themes import get_theme_colors
    
    colors = get_theme_colors('vectrex')
    
    # Get XY plane cross-section
    slice_idx = grid_data['z'].shape[2] // 2
    X = grid_data['x'][:, :, slice_idx]
    Y = grid_data['y'][:, :, slice_idx]
    prob_2d = grid_data['prob_density'][:, :, slice_idx]
    
    # Get quantum numbers
    n, l, m = grid_data['quantum_numbers']
    orbital_name = grid_data['orbital_name']
    
    # Create figure
    fig = go.Figure()
    
    # Add contour lines (vector-style)
    contour_levels = np.linspace(np.max(prob_2d) * 0.1, np.max(prob_2d), num_contours)
    
    fig.add_trace(go.Contour(
        x=X[0, :],
        y=Y[:, 0],
        z=prob_2d,
        contours=dict(
            start=contour_levels[0],
            end=contour_levels[-1],
            size=(contour_levels[-1] - contour_levels[0]) / num_contours,
            coloring='lines',
            showlabels=True,
            labelfont=dict(size=10, color=colors['primary'])
        ),
        line=dict(
            color=colors['primary'],
            width=2
        ),
        colorscale=[[0, colors['background']], [1, colors['primary']]],
        showscale=False,
        hovertemplate="x=%{x:.2f}<br>y=%{y:.2f}<br>|ψ|²=%{z:.4e}<extra></extra>"
    ))
    
    # Add glowing dots at contour intersections for extra Vectrex feel
    max_points_x, max_points_y = np.where(prob_2d > np.max(prob_2d) * 0.7)
    if len(max_points_x) > 0:
        sample_indices = np.random.choice(len(max_points_x), min(50, len(max_points_x)), replace=False)
        fig.add_trace(go.Scatter(
            x=X[max_points_x[sample_indices], max_points_y[sample_indices]],
            y=Y[max_points_x[sample_indices], max_points_y[sample_indices]],
            mode='markers',
            marker=dict(
                size=4,
                color=colors['accent'],
                symbol='circle',
                line=dict(color=colors['primary'], width=1)
            ),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Add border frame (classic Vectrex style)
    extent = np.max(np.abs(X))
    border_x = [-extent, extent, extent, -extent, -extent]
    border_y = [-extent, -extent, extent, extent, -extent]
    
    fig.add_trace(go.Scatter(
        x=border_x,
        y=border_y,
        mode='lines',
        line=dict(color=colors['primary'], width=3),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Update layout with Vectrex aesthetics
    fig.update_layout(
        title=dict(
            text=f"◄► VECTREX ◄►<br>{orbital_name} | n={n} l={l} m={m}",
            font=dict(
                size=20,
                color=colors['primary'],
                family='Courier New, monospace'
            ),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title="X",
            gridcolor=colors['grid'],
            color=colors['primary'],
            showgrid=True,
            zeroline=True,
            zerolinecolor=colors['accent'],
            zerolinewidth=2,
            scaleanchor='y',
            scaleratio=1
        ),
        yaxis=dict(
            title="Y",
            gridcolor=colors['grid'],
            color=colors['primary'],
            showgrid=True,
            zeroline=True,
            zerolinecolor=colors['accent'],
            zerolinewidth=2
        ),
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font=dict(color=colors['primary'], family='Courier New, monospace'),
        height=600,
        width=600,
        margin=dict(l=50, r=50, t=100, b=50)
    )
    
    return fig


def create_vector_wireframe(grid_data, iso_level=0.01):
    """
    Create 3D vector-style wireframe using sparse lines.
    
    Parameters
    ----------
    grid_data : dict
        Orbital grid data
    iso_level : float
        Isosurface threshold
        
    Returns
    -------
    plotly.graph_objects.Figure
    """
    from .themes import get_theme_colors
    from skimage import measure
    
    colors = get_theme_colors('vectrex')
    
    # Get data
    prob = grid_data['prob_density']
    threshold = iso_level * np.max(prob)
    
    # Extract isosurface using marching cubes
    try:
        verts, faces, normals, values = measure.marching_cubes(prob, threshold)
    except:
        # Fallback: create simple wireframe from slices
        return create_vectrex_orbital(grid_data)
    
    # Scale vertices to actual coordinates
    x_range = grid_data['x'][:, 0, 0]
    y_range = grid_data['y'][0, :, 0]
    z_range = grid_data['z'][0, 0, :]
    
    x_scale = (x_range[-1] - x_range[0]) / prob.shape[0]
    y_scale = (y_range[-1] - y_range[0]) / prob.shape[1]
    z_scale = (z_range[-1] - z_range[0]) / prob.shape[2]
    
    verts[:, 0] = verts[:, 0] * x_scale + x_range[0]
    verts[:, 1] = verts[:, 1] * y_scale + y_range[0]
    verts[:, 2] = verts[:, 2] * z_scale + z_range[0]
    
    # Sample subset of edges for wireframe effect (not all triangles)
    num_faces = len(faces)
    sample_size = min(500, num_faces)
    sampled_faces = faces[np.random.choice(num_faces, sample_size, replace=False)]
    
    # Create line segments for edges
    fig = go.Figure()
    
    for face in sampled_faces:
        # Draw edges of triangle
        for i in range(3):
            v1 = verts[face[i]]
            v2 = verts[face[(i+1)%3]]
            
            fig.add_trace(go.Scatter3d(
                x=[v1[0], v2[0]],
                y=[v1[1], v2[1]],
                z=[v1[2], v2[2]],
                mode='lines',
                line=dict(color=colors['primary'], width=2),
                showlegend=False,
                hoverinfo='skip'
            ))
    
    # Get quantum numbers
    n, l, m = grid_data['quantum_numbers']
    orbital_name = grid_data['orbital_name']
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=f"▲ VECTOR MODE ▲<br>{orbital_name}",
            font=dict(size=20, color=colors['primary'], family='Courier New, monospace'),
            x=0.5,
            xanchor='center'
        ),
        scene=dict(
            xaxis=dict(
                title="X",
                backgroundcolor=colors['background'],
                gridcolor=colors['grid'],
                showbackground=True,
                color=colors['primary']
            ),
            yaxis=dict(
                title="Y",
                backgroundcolor=colors['background'],
                gridcolor=colors['grid'],
                showbackground=True,
                color=colors['primary']
            ),
            zaxis=dict(
                title="Z",
                backgroundcolor=colors['background'],
                gridcolor=colors['grid'],
                showbackground=True,
                color=colors['primary']
            ),
            bgcolor=colors['background']
        ),
        paper_bgcolor=colors['background'],
        font=dict(color=colors['primary'], family='Courier New, monospace'),
        height=700
    )
    
    return fig


def create_scanline_effect(fig):
    """
    Add CRT scanline overlay effect to figure.
    
    Parameters
    ----------
    fig : plotly.graph_objects.Figure
        Figure to add scanlines to
        
    Returns
    -------
    plotly.graph_objects.Figure
        Figure with scanline effect
    """
    # Add horizontal lines to simulate CRT scanlines
    # This is a visual effect - in practice would be done with CSS/JS overlay
    
    # For now, we add subtle horizontal grid lines
    fig.update_yaxes(
        showgrid=True,
        gridwidth=0.5,
        gridcolor='rgba(0, 255, 0, 0.1)',
        dtick=0.5
    )
    
    return fig


def create_vectrex_energy_levels(max_n=7):
    """
    Create Vectrex-style energy level diagram.
    
    Parameters
    ----------
    max_n : int
        Maximum principal quantum number
        
    Returns
    -------
    plotly.graph_objects.Figure
    """
    from .themes import get_theme_colors
    from quantum_engine.constants import RYDBERG_ENERGY
    
    colors = get_theme_colors('vectrex')
    
    # Calculate energy levels
    n_values = np.arange(1, max_n + 1)
    energies = -RYDBERG_ENERGY / (n_values ** 2)
    
    fig = go.Figure()
    
    # Draw energy levels as horizontal lines
    for n, E in zip(n_values, energies):
        # Horizontal line
        fig.add_trace(go.Scatter(
            x=[0, 1],
            y=[E, E],
            mode='lines+text',
            line=dict(color=colors['primary'], width=3),
            text=[f'n={n}', ''],
            textposition='middle left',
            textfont=dict(color=colors['primary'], size=14, family='Courier New'),
            showlegend=False,
            hovertemplate=f"n={n}<br>E={E:.2f} eV<extra></extra>"
        ))
        
        # Add glowing dots at ends
        fig.add_trace(go.Scatter(
            x=[0, 1],
            y=[E, E],
            mode='markers',
            marker=dict(
                size=8,
                color=colors['accent'],
                symbol='circle',
                line=dict(color=colors['primary'], width=2)
            ),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text="═══ ENERGY LEVELS ═══",
            font=dict(size=22, color=colors['primary'], family='Courier New, monospace'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            range=[-0.2, 1.3]
        ),
        yaxis=dict(
            title="ENERGY (eV)",
            gridcolor=colors['grid'],
            color=colors['primary'],
            zeroline=True,
            zerolinecolor=colors['accent'],
            zerolinewidth=3,
            showgrid=True
        ),
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font=dict(color=colors['primary'], family='Courier New, monospace'),
        height=600
    )
    
    return fig


def create_vectrex_radial_plot(n, l):
    """
    Create Vectrex-style radial probability plot.
    
    Parameters
    ----------
    n : int
        Principal quantum number
    l : int
        Angular momentum quantum number
        
    Returns
    -------
    plotly.graph_objects.Figure
    """
    from .themes import get_theme_colors
    from quantum_engine.schrodinger import radial_probability_density
    from quantum_engine.orbitals import get_orbital_name
    
    colors = get_theme_colors('vectrex')
    
    # Create radial grid
    r_max = 5 * n ** 2
    r = np.linspace(0, r_max, 500)
    P_r = radial_probability_density(r, n, l)
    
    orbital_name = get_orbital_name(n, l, 0)
    
    fig = go.Figure()
    
    # Plot as lines (vector style)
    fig.add_trace(go.Scatter(
        x=r,
        y=P_r,
        mode='lines',
        line=dict(color=colors['primary'], width=3),
        fill='tozeroy',
        fillcolor='rgba(0, 255, 0, 0.1)',
        hovertemplate="r=%{x:.2f} a₀<br>P(r)=%{y:.4f}<extra></extra>"
    ))
    
    # Add marker at maximum
    max_idx = np.argmax(P_r)
    fig.add_trace(go.Scatter(
        x=[r[max_idx]],
        y=[P_r[max_idx]],
        mode='markers',
        marker=dict(
            size=12,
            color=colors['accent'],
            symbol='star',
            line=dict(color=colors['primary'], width=2)
        ),
        showlegend=False,
        hovertemplate=f"MAX @ r={r[max_idx]:.2f}<extra></extra>"
    ))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=f"▼ RADIAL P(r) ▼<br>{orbital_name}",
            font=dict(size=20, color=colors['primary'], family='Courier New, monospace'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title="RADIUS (Bohr)",
            gridcolor=colors['grid'],
            color=colors['primary'],
            showgrid=True
        ),
        yaxis=dict(
            title="PROBABILITY",
            gridcolor=colors['grid'],
            color=colors['primary'],
            showgrid=True
        ),
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font=dict(color=colors['primary'], family='Courier New, monospace'),
        height=500
    )
    
    return fig


def create_ascii_border(text, width=40):
    """
    Create ASCII art border around text (for retro feel).
    
    Parameters
    ----------
    text : str
        Text to border
    width : int
        Border width
        
    Returns
    -------
    str
        Bordered text
    """
    border_top = "╔" + "═" * (width - 2) + "╗"
    border_bot = "╚" + "═" * (width - 2) + "╝"
    text_line = f"║ {text.center(width - 4)} ║"
    
    return f"{border_top}\n{text_line}\n{border_bot}"