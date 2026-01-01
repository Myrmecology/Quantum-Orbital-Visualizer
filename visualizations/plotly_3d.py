"""
3D Plotly Visualizations for Quantum Orbitals
==============================================

Creates interactive 3D visualizations of hydrogen orbitals using Plotly.
Supports multiple rendering modes: isosurface, volume, wireframe, particle swarm.
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import config


def create_3d_orbital(grid_data, mode='isosurface', iso_level=None, theme='deep_space'):
    """
    Create 3D visualization of quantum orbital.
    
    Parameters
    ----------
    grid_data : dict
        Output from generate_orbital_grid
    mode : str
        Rendering mode: 'isosurface', 'volume', 'wireframe', 'particle_swarm'
    iso_level : float, optional
        Isosurface threshold (default from config)
    theme : str
        Color theme name
        
    Returns
    -------
    plotly.graph_objects.Figure
        3D visualization figure
    """
    if mode == 'isosurface':
        return create_isosurface(grid_data, iso_level, theme)
    elif mode == 'volume':
        return create_volume_plot(grid_data, theme)
    elif mode == 'wireframe':
        return create_wireframe(grid_data, iso_level, theme)
    elif mode == 'particle_swarm':
        return create_particle_swarm(grid_data, theme)
    else:
        raise ValueError(f"Unknown mode: {mode}")


def create_isosurface(grid_data, iso_level=None, theme='deep_space'):
    """
    Create isosurface plot of probability density.
    
    Parameters
    ----------
    grid_data : dict
        Orbital grid data
    iso_level : float, optional
        Isosurface threshold value
    theme : str
        Color theme
        
    Returns
    -------
    plotly.graph_objects.Figure
    """
    from .themes import get_theme_colors
    
    colors = get_theme_colors(theme)
    
    # Get data
    x = grid_data['x']
    y = grid_data['y']
    z = grid_data['z']
    prob = grid_data['prob_density']
    
    # Determine isosurface value
    if iso_level is None:
        iso_level = config.DEFAULT_ISO_LEVEL
    
    iso_value = iso_level * np.max(prob)
    
    # Get quantum numbers
    n, l, m = grid_data['quantum_numbers']
    orbital_name = grid_data['orbital_name']
    energy = grid_data['energy']
    
    # Create isosurface
    fig = go.Figure(data=go.Isosurface(
        x=x.flatten(),
        y=y.flatten(),
        z=z.flatten(),
        value=prob.flatten(),
        isomin=iso_value,
        isomax=np.max(prob),
        surface_count=3,
        colorscale=[
            [0, colors['primary']],
            [0.5, colors['secondary']],
            [1, colors['accent']]
        ],
        opacity=0.6,
        caps=dict(x_show=False, y_show=False, z_show=False),
        showscale=True,
        colorbar=dict(
            title="Probability<br>Density",
            titleside="right",
            tickmode="linear",
            tick0=0,
            dtick=iso_value,
            titlefont=dict(color=colors['primary']),
            tickfont=dict(color=colors['primary'])
        )
    ))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=f"Orbital {orbital_name} | n={n}, l={l}, m={m}<br>Energy: {energy:.3f} eV",
            font=dict(size=20, color=colors['primary']),
            x=0.5,
            xanchor='center'
        ),
        scene=dict(
            xaxis=dict(
                title="x (Bohr radii)",
                backgroundcolor=colors['background'],
                gridcolor=colors['grid'],
                showbackground=True,
                color=colors['primary']
            ),
            yaxis=dict(
                title="y (Bohr radii)",
                backgroundcolor=colors['background'],
                gridcolor=colors['grid'],
                showbackground=True,
                color=colors['primary']
            ),
            zaxis=dict(
                title="z (Bohr radii)",
                backgroundcolor=colors['background'],
                gridcolor=colors['grid'],
                showbackground=True,
                color=colors['primary']
            ),
            bgcolor=colors['background'],
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        paper_bgcolor=colors['background'],
        plot_bgcolor=colors['background'],
        font=dict(color=colors['primary']),
        margin=dict(l=0, r=0, t=80, b=0),
        height=config.MAIN_VIEWPORT_HEIGHT
    )
    
    return fig


def create_volume_plot(grid_data, theme='deep_space'):
    """
    Create volumetric rendering of probability density.
    
    Parameters
    ----------
    grid_data : dict
        Orbital grid data
    theme : str
        Color theme
        
    Returns
    -------
    plotly.graph_objects.Figure
    """
    from .themes import get_theme_colors
    
    colors = get_theme_colors(theme)
    
    # Get data
    x = grid_data['x']
    y = grid_data['y']
    z = grid_data['z']
    prob = grid_data['prob_density']
    
    # Normalize probability for visualization
    prob_norm = prob / np.max(prob)
    
    # Get quantum numbers
    n, l, m = grid_data['quantum_numbers']
    orbital_name = grid_data['orbital_name']
    
    # Create volume plot
    fig = go.Figure(data=go.Volume(
        x=x.flatten(),
        y=y.flatten(),
        z=z.flatten(),
        value=prob_norm.flatten(),
        isomin=0.01,
        isomax=1.0,
        opacity=0.1,
        surface_count=15,
        colorscale=[
            [0, colors['background']],
            [0.3, colors['primary']],
            [0.6, colors['secondary']],
            [1, colors['accent']]
        ],
        caps=dict(x_show=False, y_show=False, z_show=False),
        showscale=True
    ))
    
    # Update layout
    fig.update_layout(
        title=f"Volume: {orbital_name} (n={n}, l={l}, m={m})",
        scene=dict(
            xaxis=dict(title="x", backgroundcolor=colors['background'], gridcolor=colors['grid']),
            yaxis=dict(title="y", backgroundcolor=colors['background'], gridcolor=colors['grid']),
            zaxis=dict(title="z", backgroundcolor=colors['background'], gridcolor=colors['grid']),
            bgcolor=colors['background']
        ),
        paper_bgcolor=colors['background'],
        font=dict(color=colors['primary']),
        height=config.MAIN_VIEWPORT_HEIGHT
    )
    
    return fig


def create_wireframe(grid_data, iso_level=None, theme='deep_space'):
    """
    Create wireframe mesh visualization.
    
    Parameters
    ----------
    grid_data : dict
        Orbital grid data
    iso_level : float, optional
        Threshold for wireframe
    theme : str
        Color theme
        
    Returns
    -------
    plotly.graph_objects.Figure
    """
    from .themes import get_theme_colors
    from skimage import measure
    
    colors = get_theme_colors(theme)
    
    # Get data
    prob = grid_data['prob_density']
    
    # Determine threshold
    if iso_level is None:
        iso_level = config.DEFAULT_ISO_LEVEL
    
    threshold = iso_level * np.max(prob)
    
    # Extract isosurface mesh using marching cubes
    try:
        verts, faces, normals, values = measure.marching_cubes(prob, threshold)
    except:
        # Fallback if marching cubes fails
        return create_isosurface(grid_data, iso_level, theme)
    
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
    
    # Create mesh
    fig = go.Figure(data=[
        go.Mesh3d(
            x=verts[:, 0],
            y=verts[:, 1],
            z=verts[:, 2],
            i=faces[:, 0],
            j=faces[:, 1],
            k=faces[:, 2],
            color=colors['primary'],
            opacity=0.3,
            flatshading=True
        )
    ])
    
    # Get quantum numbers
    n, l, m = grid_data['quantum_numbers']
    orbital_name = grid_data['orbital_name']
    
    # Update layout
    fig.update_layout(
        title=f"Wireframe: {orbital_name} (n={n}, l={l}, m={m})",
        scene=dict(
            xaxis=dict(title="x", backgroundcolor=colors['background'], gridcolor=colors['grid']),
            yaxis=dict(title="y", backgroundcolor=colors['background'], gridcolor=colors['grid']),
            zaxis=dict(title="z", backgroundcolor=colors['background'], gridcolor=colors['grid']),
            bgcolor=colors['background']
        ),
        paper_bgcolor=colors['background'],
        font=dict(color=colors['primary']),
        height=config.MAIN_VIEWPORT_HEIGHT
    )
    
    return fig


def create_particle_swarm(grid_data, num_particles=5000, theme='deep_space'):
    """
    Create particle swarm visualization where particles follow probability distribution.
    
    Parameters
    ----------
    grid_data : dict
        Orbital grid data
    num_particles : int
        Number of particles to display
    theme : str
        Color theme
        
    Returns
    -------
    plotly.graph_objects.Figure
    """
    from .themes import get_theme_colors
    
    colors = get_theme_colors(theme)
    
    # Get flattened data
    x = grid_data['x'].flatten()
    y = grid_data['y'].flatten()
    z = grid_data['z'].flatten()
    prob = grid_data['prob_density'].flatten()
    
    # Normalize probabilities
    prob = prob / np.sum(prob)
    
    # Sample points based on probability
    indices = np.random.choice(len(x), size=num_particles, p=prob, replace=True)
    
    sample_x = x[indices]
    sample_y = y[indices]
    sample_z = z[indices]
    
    # Get quantum numbers
    n, l, m = grid_data['quantum_numbers']
    orbital_name = grid_data['orbital_name']
    
    # Create scatter plot
    fig = go.Figure(data=go.Scatter3d(
        x=sample_x,
        y=sample_y,
        z=sample_z,
        mode='markers',
        marker=dict(
            size=2,
            color=prob[indices],
            colorscale=[
                [0, colors['primary']],
                [0.5, colors['secondary']],
                [1, colors['accent']]
            ],
            opacity=0.6,
            showscale=True,
            colorbar=dict(title="Probability")
        )
    ))
    
    # Update layout
    fig.update_layout(
        title=f"Particle Swarm: {orbital_name} (n={n}, l={l}, m={m})",
        scene=dict(
            xaxis=dict(title="x", backgroundcolor=colors['background'], gridcolor=colors['grid']),
            yaxis=dict(title="y", backgroundcolor=colors['background'], gridcolor=colors['grid']),
            zaxis=dict(title="z", backgroundcolor=colors['background'], gridcolor=colors['grid']),
            bgcolor=colors['background']
        ),
        paper_bgcolor=colors['background'],
        font=dict(color=colors['primary']),
        height=config.MAIN_VIEWPORT_HEIGHT
    )
    
    return fig


def create_cross_section_3d(grid_data, plane='xy', theme='deep_space'):
    """
    Create 3D visualization with cross-section overlay.
    
    Parameters
    ----------
    grid_data : dict
        Orbital grid data
    plane : str
        Cross-section plane: 'xy', 'xz', 'yz'
    theme : str
        Color theme
        
    Returns
    -------
    plotly.graph_objects.Figure
    """
    from .themes import get_theme_colors
    
    colors = get_theme_colors(theme)
    
    # Get cross-section data
    if plane == 'xy':
        slice_idx = grid_data['z'].shape[2] // 2
        X = grid_data['x'][:, :, slice_idx]
        Y = grid_data['y'][:, :, slice_idx]
        Z = grid_data['z'][:, :, slice_idx]
        prob_2d = grid_data['prob_density'][:, :, slice_idx]
    elif plane == 'xz':
        slice_idx = grid_data['y'].shape[1] // 2
        X = grid_data['x'][:, slice_idx, :]
        Y = grid_data['y'][:, slice_idx, :]
        Z = grid_data['z'][:, slice_idx, :]
        prob_2d = grid_data['prob_density'][:, slice_idx, :]
    else:  # yz
        slice_idx = grid_data['x'].shape[0] // 2
        X = grid_data['x'][slice_idx, :, :]
        Y = grid_data['y'][slice_idx, :, :]
        Z = grid_data['z'][slice_idx, :, :]
        prob_2d = grid_data['prob_density'][slice_idx, :, :]
    
    # Create surface plot for cross-section
    fig = go.Figure(data=go.Surface(
        x=X,
        y=Y,
        z=Z,
        surfacecolor=prob_2d,
        colorscale=[
            [0, colors['background']],
            [0.5, colors['primary']],
            [1, colors['accent']]
        ],
        showscale=True,
        colorbar=dict(title="Probability")
    ))
    
    # Get quantum numbers
    n, l, m = grid_data['quantum_numbers']
    orbital_name = grid_data['orbital_name']
    
    # Update layout
    fig.update_layout(
        title=f"Cross-section {plane.upper()}: {orbital_name}",
        scene=dict(
            xaxis=dict(title="x", backgroundcolor=colors['background'], gridcolor=colors['grid']),
            yaxis=dict(title="y", backgroundcolor=colors['background'], gridcolor=colors['grid']),
            zaxis=dict(title="z", backgroundcolor=colors['background'], gridcolor=colors['grid']),
            bgcolor=colors['background']
        ),
        paper_bgcolor=colors['background'],
        font=dict(color=colors['primary']),
        height=config.MAIN_VIEWPORT_HEIGHT
    )
    
    return fig


def create_multi_orbital_comparison(grid_data_list, theme='deep_space'):
    """
    Create side-by-side comparison of multiple orbitals.
    
    Parameters
    ----------
    grid_data_list : list of dict
        List of orbital grid data (max 4)
    theme : str
        Color theme
        
    Returns
    -------
    plotly.graph_objects.Figure
    """
    num_orbitals = min(len(grid_data_list), 4)
    
    # Create subplots
    if num_orbitals <= 2:
        rows, cols = 1, num_orbitals
    else:
        rows, cols = 2, 2
    
    specs = [[{'type': 'surface'}] * cols for _ in range(rows)]
    
    fig = make_subplots(
        rows=rows, cols=cols,
        specs=specs,
        subplot_titles=[gd['orbital_name'] for gd in grid_data_list[:num_orbitals]],
        horizontal_spacing=0.05,
        vertical_spacing=0.1
    )
    
    # Add each orbital
    for idx, grid_data in enumerate(grid_data_list[:num_orbitals]):
        row = idx // cols + 1
        col = idx % cols + 1
        
        # Create isosurface for this orbital
        iso_fig = create_isosurface(grid_data, theme=theme)
        
        # Add to subplot
        for trace in iso_fig.data:
            fig.add_trace(trace, row=row, col=col)
    
    # Update layout
    from .themes import get_theme_colors
    colors = get_theme_colors(theme)
    
    fig.update_layout(
        title="Orbital Comparison",
        paper_bgcolor=colors['background'],
        font=dict(color=colors['primary']),
        height=800,
        showlegend=False
    )
    
    return fig