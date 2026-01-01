"""
2D Charts and Data Visualizations
==================================

Creates bar graphs, pie charts, heatmaps, and statistical displays
for quantum orbital data.
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import config


def create_energy_level_diagram(max_n=7, theme='deep_space'):
    """
    Create interactive bar chart showing hydrogen energy levels.
    
    Parameters
    ----------
    max_n : int
        Maximum principal quantum number to display
    theme : str
        Color theme
        
    Returns
    -------
    plotly.graph_objects.Figure
    """
    from .themes import get_theme_colors
    from quantum_engine.constants import RYDBERG_ENERGY
    
    colors = get_theme_colors(theme)
    
    # Calculate energy levels
    n_values = np.arange(1, max_n + 1)
    energies = -RYDBERG_ENERGY / (n_values ** 2)
    
    # Create bar chart
    fig = go.Figure(data=go.Bar(
        x=n_values,
        y=energies,
        marker=dict(
            color=energies,
            colorscale=[
                [0, colors['primary']],
                [0.5, colors['secondary']],
                [1, colors['accent']]
            ],
            line=dict(color=colors['grid'], width=2),
            showscale=True,
            colorbar=dict(
                title="Energy (eV)",
                titleside="right",
                tickmode="linear"
            )
        ),
        text=[f"n={n}<br>{e:.2f} eV" for n, e in zip(n_values, energies)],
        textposition='outside',
        hovertemplate="<b>n = %{x}</b><br>Energy: %{y:.3f} eV<extra></extra>"
    ))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text="Hydrogen Atom Energy Levels",
            font=dict(size=20, color=colors['primary']),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title="Principal Quantum Number (n)",
            tickmode='linear',
            tick0=1,
            dtick=1,
            gridcolor=colors['grid'],
            color=colors['primary']
        ),
        yaxis=dict(
            title="Energy (eV)",
            gridcolor=colors['grid'],
            color=colors['primary'],
            zeroline=True,
            zerolinecolor=colors['accent'],
            zerolinewidth=2
        ),
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font=dict(color=colors['primary'], size=12),
        height=config.CHART_HEIGHT,
        hovermode='x unified'
    )
    
    return fig


def create_radial_probability_chart(n, l, theme='deep_space'):
    """
    Create line chart showing radial probability distribution P(r) = r²|R(r)|².
    
    Parameters
    ----------
    n : int
        Principal quantum number
    l : int
        Angular momentum quantum number
    theme : str
        Color theme
        
    Returns
    -------
    plotly.graph_objects.Figure
    """
    from .themes import get_theme_colors
    from quantum_engine.schrodinger import radial_probability_density
    from quantum_engine.orbitals import get_orbital_name
    
    colors = get_theme_colors(theme)
    
    # Create radial grid
    r_max = 5 * n ** 2  # Scale with n
    r = np.linspace(0, r_max, 500)
    
    # Calculate radial probability
    P_r = radial_probability_density(r, n, l)
    
    # Find maximum
    max_idx = np.argmax(P_r)
    r_max_prob = r[max_idx]
    P_max = P_r[max_idx]
    
    # Get orbital name
    orbital_name = get_orbital_name(n, l, 0)
    
    # Create line chart
    fig = go.Figure()
    
    # Add radial probability curve
    fig.add_trace(go.Scatter(
        x=r,
        y=P_r,
        mode='lines',
        name='P(r)',
        line=dict(color=colors['primary'], width=3),
        fill='tozeroy',
        fillcolor=f"rgba{tuple(list(int(colors['primary'][i:i+2], 16) for i in (1, 3, 5)) + [0.3])}",
        hovertemplate="r = %{x:.2f} a₀<br>P(r) = %{y:.4f}<extra></extra>"
    ))
    
    # Add marker at maximum
    fig.add_trace(go.Scatter(
        x=[r_max_prob],
        y=[P_max],
        mode='markers',
        name='Most Probable',
        marker=dict(
            color=colors['accent'],
            size=12,
            symbol='star',
            line=dict(color=colors['secondary'], width=2)
        ),
        hovertemplate=f"<b>Most Probable Radius</b><br>r = {r_max_prob:.2f} a₀<extra></extra>"
    ))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=f"Radial Probability Distribution: {orbital_name} (n={n}, l={l})",
            font=dict(size=18, color=colors['primary']),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title="Radial Distance r (Bohr radii)",
            gridcolor=colors['grid'],
            color=colors['primary']
        ),
        yaxis=dict(
            title="Radial Probability Density P(r)",
            gridcolor=colors['grid'],
            color=colors['primary']
        ),
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font=dict(color=colors['primary']),
        height=config.CHART_HEIGHT,
        showlegend=True,
        legend=dict(
            bgcolor=colors['background'],
            bordercolor=colors['grid'],
            borderwidth=1
        )
    )
    
    return fig


def create_angular_momentum_pie(l, theme='deep_space'):
    """
    Create pie chart showing angular momentum quantum number distribution.
    
    Parameters
    ----------
    l : int
        Angular momentum quantum number
    theme : str
        Color theme
        
    Returns
    -------
    plotly.graph_objects.Figure
    """
    from .themes import get_theme_colors
    from quantum_engine.constants import HBAR
    
    colors = get_theme_colors(theme)
    
    # Calculate angular momentum magnitude
    L_magnitude = HBAR * np.sqrt(l * (l + 1))
    
    # Possible m values
    m_values = list(range(-l, l + 1))
    num_states = len(m_values)
    
    # Equal probability for each m state (in absence of external field)
    probabilities = [1.0 / num_states] * num_states
    
    # Create color gradient
    color_list = []
    for i in range(num_states):
        ratio = i / max(num_states - 1, 1)
        # Interpolate between primary and accent
        color_list.append(colors['primary'] if ratio < 0.5 else colors['accent'])
    
    # Create pie chart
    fig = go.Figure(data=go.Pie(
        labels=[f"m = {m}" for m in m_values],
        values=probabilities,
        marker=dict(
            colors=color_list,
            line=dict(color=colors['background'], width=2)
        ),
        textinfo='label+percent',
        textfont=dict(size=14, color=colors['background']),
        hovertemplate="<b>m = %{label}</b><br>Probability: %{percent}<extra></extra>"
    ))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=f"Magnetic Quantum Number Distribution (l={l})<br>|L| = {L_magnitude:.3e} J·s",
            font=dict(size=18, color=colors['primary']),
            x=0.5,
            xanchor='center'
        ),
        paper_bgcolor=colors['background'],
        font=dict(color=colors['primary']),
        height=config.CHART_HEIGHT,
        showlegend=True,
        legend=dict(
            bgcolor=colors['background'],
            bordercolor=colors['grid'],
            borderwidth=1,
            font=dict(color=colors['primary'])
        )
    )
    
    return fig


def create_probability_heatmap(grid_data, plane='xy', theme='deep_space'):
    """
    Create 2D heatmap of probability density cross-section.
    
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
        prob_2d = grid_data['prob_density'][:, :, slice_idx]
        xlabel, ylabel = "x (Bohr radii)", "y (Bohr radii)"
    elif plane == 'xz':
        slice_idx = grid_data['y'].shape[1] // 2
        X = grid_data['x'][:, slice_idx, :]
        Y = grid_data['z'][:, slice_idx, :]
        prob_2d = grid_data['prob_density'][:, slice_idx, :]
        xlabel, ylabel = "x (Bohr radii)", "z (Bohr radii)"
    else:  # yz
        slice_idx = grid_data['x'].shape[0] // 2
        X = grid_data['y'][slice_idx, :, :]
        Y = grid_data['z'][slice_idx, :, :]
        prob_2d = grid_data['prob_density'][slice_idx, :, :]
        xlabel, ylabel = "y (Bohr radii)", "z (Bohr radii)"
    
    # Get quantum numbers
    n, l, m = grid_data['quantum_numbers']
    orbital_name = grid_data['orbital_name']
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        x=X[0, :],
        y=Y[:, 0],
        z=prob_2d,
        colorscale=[
            [0, colors['background']],
            [0.3, colors['primary']],
            [0.6, colors['secondary']],
            [1, colors['accent']]
        ],
        colorbar=dict(
            title="Probability<br>Density",
            titleside="right",
            tickmode="linear",
            titlefont=dict(color=colors['primary']),
            tickfont=dict(color=colors['primary'])
        ),
        hovertemplate=f"{xlabel.split()[0]} = %{{x:.2f}}<br>{ylabel.split()[0]} = %{{y:.2f}}<br>P = %{{z:.4e}}<extra></extra>"
    ))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=f"Probability Heatmap ({plane.upper()} plane): {orbital_name}",
            font=dict(size=18, color=colors['primary']),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title=xlabel,
            gridcolor=colors['grid'],
            color=colors['primary']
        ),
        yaxis=dict(
            title=ylabel,
            gridcolor=colors['grid'],
            color=colors['primary'],
            scaleanchor='x',
            scaleratio=1
        ),
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font=dict(color=colors['primary']),
        height=config.CHART_HEIGHT
    )
    
    return fig


def create_quantum_stats_table(grid_data, theme='deep_space'):
    """
    Create table displaying quantum statistics and properties.
    
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
    from quantum_engine.orbitals import calculate_orbital_energy
    from quantum_engine.schrodinger import expectation_value_r, most_probable_radius
    
    colors = get_theme_colors(theme)
    
    # Get quantum numbers
    n, l, m = grid_data['quantum_numbers']
    orbital_name = grid_data['orbital_name']
    
    # Calculate properties
    energy = calculate_orbital_energy(n)
    exp_r = expectation_value_r(n, l)
    r_prob = most_probable_radius(n, l)
    max_prob = np.max(grid_data['prob_density'])
    
    # Create table data
    properties = [
        "Orbital",
        "Principal (n)",
        "Angular (l)",
        "Magnetic (m)",
        "Energy",
        "⟨r⟩",
        "r<sub>max prob</sub>",
        "Max |ψ|²"
    ]
    
    values = [
        orbital_name,
        str(n),
        str(l),
        str(m),
        f"{energy:.3f} eV",
        f"{exp_r:.2f} a₀",
        f"{r_prob:.2f} a₀",
        f"{max_prob:.4e}"
    ]
    
    # Create table
    fig = go.Figure(data=go.Table(
        header=dict(
            values=["<b>Property</b>", "<b>Value</b>"],
            fill_color=colors['primary'],
            align='center',
            font=dict(color=colors['background'], size=14)
        ),
        cells=dict(
            values=[properties, values],
            fill_color=colors['background'],
            align=['left', 'right'],
            font=dict(color=colors['primary'], size=12),
            line=dict(color=colors['grid'], width=1),
            height=30
        )
    ))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text="Quantum State Properties",
            font=dict(size=18, color=colors['primary']),
            x=0.5,
            xanchor='center'
        ),
        paper_bgcolor=colors['background'],
        height=400,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig


def create_transition_diagram(n_initial, n_final, theme='deep_space'):
    """
    Create diagram showing energy transition and photon emission.
    
    Parameters
    ----------
    n_initial : int
        Initial energy level
    n_final : int
        Final energy level
    theme : str
        Color theme
        
    Returns
    -------
    plotly.graph_objects.Figure
    """
    from .themes import get_theme_colors
    from quantum_engine.orbitals import calculate_energy_difference, calculate_photon_wavelength
    
    colors = get_theme_colors(theme)
    
    # Calculate properties
    delta_E = calculate_energy_difference(n_initial, n_final)
    wavelength = calculate_photon_wavelength(n_initial, n_final)
    
    # Create energy levels
    n_range = range(min(n_initial, n_final), max(n_initial, n_final) + 1)
    energies = [-13.6 / n**2 for n in n_range]
    
    # Create figure
    fig = go.Figure()
    
    # Add energy levels as horizontal lines
    for i, (n, E) in enumerate(zip(n_range, energies)):
        color = colors['accent'] if n in [n_initial, n_final] else colors['primary']
        width = 3 if n in [n_initial, n_final] else 2
        
        fig.add_trace(go.Scatter(
            x=[0, 1],
            y=[E, E],
            mode='lines',
            line=dict(color=color, width=width),
            name=f"n={n}",
            hovertemplate=f"n={n}<br>E={E:.2f} eV<extra></extra>"
        ))
    
    # Add transition arrow
    E_initial = -13.6 / n_initial**2
    E_final = -13.6 / n_final**2
    
    fig.add_annotation(
        x=0.5,
        y=E_initial,
        ax=0.5,
        ay=E_final,
        xref="x",
        yref="y",
        axref="x",
        ayref="y",
        showarrow=True,
        arrowhead=2,
        arrowsize=1.5,
        arrowwidth=3,
        arrowcolor=colors['secondary']
    )
    
    # Add text annotation
    mid_E = (E_initial + E_final) / 2
    fig.add_annotation(
        x=0.7,
        y=mid_E,
        text=f"ΔE = {abs(delta_E):.2f} eV<br>λ = {wavelength:.1f} nm",
        showarrow=False,
        font=dict(size=12, color=colors['accent']),
        bgcolor=colors['background'],
        bordercolor=colors['grid'],
        borderwidth=1,
        borderpad=4
    )
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=f"Transition: n={n_initial} → n={n_final}",
            font=dict(size=18, color=colors['primary']),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            range=[-0.2, 1.2]
        ),
        yaxis=dict(
            title="Energy (eV)",
            gridcolor=colors['grid'],
            color=colors['primary'],
            zeroline=True,
            zerolinecolor=colors['accent']
        ),
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font=dict(color=colors['primary']),
        height=config.CHART_HEIGHT,
        showlegend=True,
        legend=dict(
            bgcolor=colors['background'],
            bordercolor=colors['grid'],
            borderwidth=1
        )
    )
    
    return fig