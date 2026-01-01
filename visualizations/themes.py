"""
Theme Management and Color Schemes
===================================

Manages visual themes and color palettes for the application.
Supports Deep Space, Cyberpunk, Quantum Lab, Matrix, and Vectrex themes.
"""

import config


def get_theme_colors(theme_name='deep_space'):
    """
    Get color scheme for specified theme.
    
    Parameters
    ----------
    theme_name : str
        Theme name: 'deep_space', 'cyberpunk', 'quantum_lab', 'matrix', 'vectrex'
        
    Returns
    -------
    dict
        Dictionary with color keys: background, primary, secondary, accent, grid
    """
    if theme_name not in config.THEME_COLORS:
        theme_name = config.DEFAULT_THEME
    
    return config.THEME_COLORS[theme_name].copy()


def apply_theme(fig, theme_name='deep_space'):
    """
    Apply theme colors to existing plotly figure.
    
    Parameters
    ----------
    fig : plotly.graph_objects.Figure
        Figure to apply theme to
    theme_name : str
        Theme name
        
    Returns
    -------
    plotly.graph_objects.Figure
        Updated figure with theme applied
    """
    colors = get_theme_colors(theme_name)
    
    # Update layout colors
    fig.update_layout(
        paper_bgcolor=colors['background'],
        plot_bgcolor=colors['background'],
        font=dict(color=colors['primary'])
    )
    
    # Update axes if present
    if hasattr(fig, 'layout') and hasattr(fig.layout, 'xaxis'):
        fig.update_xaxes(
            gridcolor=colors['grid'],
            color=colors['primary']
        )
        fig.update_yaxes(
            gridcolor=colors['grid'],
            color=colors['primary']
        )
    
    # Update 3D scene if present
    if hasattr(fig, 'layout') and hasattr(fig.layout, 'scene'):
        fig.update_layout(
            scene=dict(
                xaxis=dict(
                    backgroundcolor=colors['background'],
                    gridcolor=colors['grid'],
                    color=colors['primary']
                ),
                yaxis=dict(
                    backgroundcolor=colors['background'],
                    gridcolor=colors['grid'],
                    color=colors['primary']
                ),
                zaxis=dict(
                    backgroundcolor=colors['background'],
                    gridcolor=colors['grid'],
                    color=colors['primary']
                ),
                bgcolor=colors['background']
            )
        )
    
    return fig


def create_custom_theme(name, background, primary, secondary, accent, grid):
    """
    Create custom color theme.
    
    Parameters
    ----------
    name : str
        Theme name
    background : str
        Background color (hex)
    primary : str
        Primary color (hex)
    secondary : str
        Secondary color (hex)
    accent : str
        Accent color (hex)
    grid : str
        Grid color (hex)
        
    Returns
    -------
    dict
        Custom theme dictionary
    """
    custom_theme = {
        'background': background,
        'primary': primary,
        'secondary': secondary,
        'accent': accent,
        'grid': grid
    }
    
    # Add to config (in-memory only, not persistent)
    config.THEME_COLORS[name] = custom_theme
    
    return custom_theme


def get_colorscale(theme_name='deep_space', num_colors=10):
    """
    Generate colorscale array for plotly from theme colors.
    
    Parameters
    ----------
    theme_name : str
        Theme name
    num_colors : int
        Number of color stops
        
    Returns
    -------
    list
        Plotly colorscale format: [[0, color1], [0.5, color2], [1, color3]]
    """
    colors = get_theme_colors(theme_name)
    
    # Create gradient from primary through secondary to accent
    colorscale = []
    
    for i in range(num_colors):
        ratio = i / (num_colors - 1) if num_colors > 1 else 0
        
        if ratio < 0.5:
            # Interpolate between primary and secondary
            color = colors['primary'] if ratio < 0.25 else colors['secondary']
        else:
            # Interpolate between secondary and accent
            color = colors['secondary'] if ratio < 0.75 else colors['accent']
        
        colorscale.append([ratio, color])
    
    return colorscale


def hex_to_rgba(hex_color, alpha=1.0):
    """
    Convert hex color to RGBA string.
    
    Parameters
    ----------
    hex_color : str
        Hex color (e.g., '#FF0000')
    alpha : float
        Alpha transparency (0-1)
        
    Returns
    -------
    str
        RGBA string (e.g., 'rgba(255, 0, 0, 1.0)')
    """
    # Remove '#' if present
    hex_color = hex_color.lstrip('#')
    
    # Convert to RGB
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    return f'rgba({r}, {g}, {b}, {alpha})'


def get_gradient_color(theme_name, ratio):
    """
    Get interpolated color from theme gradient.
    
    Parameters
    ----------
    theme_name : str
        Theme name
    ratio : float
        Position in gradient (0-1)
        
    Returns
    -------
    str
        Hex color
    """
    colors = get_theme_colors(theme_name)
    
    if ratio < 0.33:
        return colors['primary']
    elif ratio < 0.67:
        return colors['secondary']
    else:
        return colors['accent']


# Available themes for UI selection
AVAILABLE_THEMES = list(config.THEME_COLORS.keys())


def get_theme_description(theme_name):
    """
    Get human-readable description of theme.
    
    Parameters
    ----------
    theme_name : str
        Theme name
        
    Returns
    -------
    str
        Theme description
    """
    descriptions = {
        'deep_space': 'Deep Space - Dark cosmic theme with blue/purple accents',
        'cyberpunk': 'Cyberpunk - Neon electric blues and hot pinks',
        'quantum_lab': 'Quantum Lab - Clean scientific white background',
        'matrix': 'Matrix - Classic green phosphor terminal aesthetic',
        'vectrex': 'Vectrex - Retro vector graphics with glowing green lines'
    }
    
    return descriptions.get(theme_name, 'Custom theme')


def get_contrast_color(background_color):
    """
    Get contrasting text color (black or white) for given background.
    
    Parameters
    ----------
    background_color : str
        Background hex color
        
    Returns
    -------
    str
        '#FFFFFF' or '#000000'
    """
    # Remove '#' if present
    bg = background_color.lstrip('#')
    
    # Convert to RGB
    r = int(bg[0:2], 16)
    g = int(bg[2:4], 16)
    b = int(bg[4:6], 16)
    
    # Calculate luminance
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    
    # Return white for dark backgrounds, black for light
    return '#FFFFFF' if luminance < 0.5 else '#000000'


def generate_theme_preview(theme_name):
    """
    Generate simple preview visualization of theme colors.
    
    Parameters
    ----------
    theme_name : str
        Theme name
        
    Returns
    -------
    plotly.graph_objects.Figure
        Preview figure showing theme colors
    """
    import plotly.graph_objects as go
    
    colors = get_theme_colors(theme_name)
    
    # Create color swatches
    color_names = ['Background', 'Primary', 'Secondary', 'Accent', 'Grid']
    color_values = [
        colors['background'],
        colors['primary'],
        colors['secondary'],
        colors['accent'],
        colors['grid']
    ]
    
    fig = go.Figure()
    
    # Add rectangles for each color
    for i, (name, color) in enumerate(zip(color_names, color_values)):
        fig.add_trace(go.Bar(
            x=[name],
            y=[1],
            marker=dict(color=color),
            name=name,
            hovertemplate=f"<b>{name}</b><br>{color}<extra></extra>",
            showlegend=False
        ))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=f"Theme Preview: {theme_name.replace('_', ' ').title()}",
            font=dict(size=18, color=colors['primary']),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title="Color Role",
            color=colors['primary'],
            gridcolor=colors['grid']
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False
        ),
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font=dict(color=colors['primary']),
        height=300,
        bargap=0.2
    )
    
    return fig


def apply_glow_effect(color, intensity=0.5):
    """
    Create glowing effect color (for Vectrex style).
    
    Parameters
    ----------
    color : str
        Base hex color
    intensity : float
        Glow intensity (0-1)
        
    Returns
    -------
    str
        RGBA color with glow
    """
    return hex_to_rgba(color, intensity)


def get_theme_css_variables(theme_name):
    """
    Get CSS custom properties for theme.
    
    Parameters
    ----------
    theme_name : str
        Theme name
        
    Returns
    -------
    dict
        CSS variable mappings
    """
    colors = get_theme_colors(theme_name)
    
    return {
        '--bg-color': colors['background'],
        '--primary-color': colors['primary'],
        '--secondary-color': colors['secondary'],
        '--accent-color': colors['accent'],
        '--grid-color': colors['grid'],
        '--text-color': get_contrast_color(colors['background'])
    }


def interpolate_colors(color1, color2, ratio):
    """
    Linearly interpolate between two hex colors.
    
    Parameters
    ----------
    color1 : str
        Starting hex color
    color2 : str
        Ending hex color
    ratio : float
        Interpolation ratio (0-1)
        
    Returns
    -------
    str
        Interpolated hex color
    """
    # Remove '#' if present
    c1 = color1.lstrip('#')
    c2 = color2.lstrip('#')
    
    # Convert to RGB
    r1, g1, b1 = int(c1[0:2], 16), int(c1[2:4], 16), int(c1[4:6], 16)
    r2, g2, b2 = int(c2[0:2], 16), int(c2[2:4], 16), int(c2[4:6], 16)
    
    # Interpolate
    r = int(r1 + (r2 - r1) * ratio)
    g = int(g1 + (g2 - g1) * ratio)
    b = int(b1 + (b2 - b1) * ratio)
    
    # Convert back to hex
    return f'#{r:02x}{g:02x}{b:02x}'