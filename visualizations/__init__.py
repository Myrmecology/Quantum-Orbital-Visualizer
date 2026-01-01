"""
Visualizations Module
=====================

Interactive 3D visualizations, charts, and themed displays for quantum orbitals.

This module contains:
- 3D Plotly visualizations for orbitals
- 2D charts (bar graphs, pie charts, heatmaps)
- Theme management and styling
- Vectrex-style retro graphics

Author: Justin D
Version: 0.1.0
"""

from .plotly_3d import (
    create_3d_orbital,
    create_isosurface,
    create_volume_plot,
    create_particle_swarm,
    create_cross_section_3d
)

from .charts import (
    create_energy_level_diagram,
    create_radial_probability_chart,
    create_angular_momentum_pie,
    create_probability_heatmap,
    create_quantum_stats_table
)

from .themes import (
    apply_theme,
    get_theme_colors,
    create_custom_theme,
    AVAILABLE_THEMES
)

from .vectrex import (
    create_vectrex_orbital,
    apply_vectrex_style,
    create_scanline_effect,
    create_vector_wireframe
)

__all__ = [
    # 3D Visualizations
    'create_3d_orbital',
    'create_isosurface',
    'create_volume_plot',
    'create_particle_swarm',
    'create_cross_section_3d',
    
    # Charts
    'create_energy_level_diagram',
    'create_radial_probability_chart',
    'create_angular_momentum_pie',
    'create_probability_heatmap',
    'create_quantum_stats_table',
    
    # Themes
    'apply_theme',
    'get_theme_colors',
    'create_custom_theme',
    'AVAILABLE_THEMES',
    
    # Vectrex
    'create_vectrex_orbital',
    'apply_vectrex_style',
    'create_scanline_effect',
    'create_vector_wireframe'
]

__version__ = '0.1.0'
__author__ = 'Justin D'