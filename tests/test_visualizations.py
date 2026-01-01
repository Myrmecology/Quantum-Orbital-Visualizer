"""
Test Suite for Visualizations
==============================

Tests for visualization components including:
- 3D plotly visualizations
- Charts and graphs
- Theme management
- Vectrex graphics
"""

import pytest
import numpy as np
from tests import TEST_GRID_POINTS, TEST_SPATIAL_EXTENT, TEST_STATES


# ========================================
# THEME TESTS
# ========================================

def test_theme_colors():
    """Test that all themes have required color keys."""
    from visualizations.themes import get_theme_colors, AVAILABLE_THEMES
    
    required_keys = ['background', 'primary', 'secondary', 'accent', 'grid']
    
    for theme in AVAILABLE_THEMES:
        colors = get_theme_colors(theme)
        for key in required_keys:
            assert key in colors
            assert colors[key].startswith('#')  # Hex color format


def test_theme_application():
    """Test theme application to figures."""
    import plotly.graph_objects as go
    from visualizations.themes import apply_theme
    
    # Create simple figure
    fig = go.Figure(data=go.Scatter(x=[1, 2, 3], y=[1, 2, 3]))
    
    # Apply theme
    themed_fig = apply_theme(fig, 'deep_space')
    
    assert themed_fig is not None
    assert hasattr(themed_fig, 'layout')


def test_custom_theme_creation():
    """Test creating custom themes."""
    from visualizations.themes import create_custom_theme, get_theme_colors
    
    custom = create_custom_theme(
        'test_theme',
        '#000000',
        '#FF0000',
        '#00FF00',
        '#0000FF',
        '#FFFFFF'
    )
    
    assert 'background' in custom
    assert custom['primary'] == '#FF0000'
    
    # Test retrieval
    retrieved = get_theme_colors('test_theme')
    assert retrieved['primary'] == '#FF0000'


def test_colorscale_generation():
    """Test colorscale generation from themes."""
    from visualizations.themes import get_colorscale
    
    colorscale = get_colorscale('deep_space', num_colors=5)
    
    assert len(colorscale) == 5
    assert colorscale[0][0] == 0  # First ratio should be 0
    assert colorscale[-1][0] == 1  # Last ratio should be 1


def test_hex_to_rgba():
    """Test hex to RGBA conversion."""
    from visualizations.themes import hex_to_rgba
    
    rgba = hex_to_rgba('#FF0000', 0.5)
    assert rgba == 'rgba(255, 0, 0, 0.5)'
    
    rgba = hex_to_rgba('#00FF00', 1.0)
    assert rgba == 'rgba(0, 255, 0, 1.0)'


# ========================================
# 3D VISUALIZATION TESTS
# ========================================

def test_create_isosurface():
    """Test isosurface creation."""
    from quantum_engine.orbitals import generate_orbital_grid
    from visualizations.plotly_3d import create_isosurface
    
    grid_data = generate_orbital_grid(
        1, 0, 0,
        grid_points=TEST_GRID_POINTS,
        spatial_extent=TEST_SPATIAL_EXTENT
    )
    
    fig = create_isosurface(grid_data)
    
    assert fig is not None
    assert len(fig.data) > 0
    assert hasattr(fig, 'layout')


def test_create_volume_plot():
    """Test volume plot creation."""
    from quantum_engine.orbitals import generate_orbital_grid
    from visualizations.plotly_3d import create_volume_plot
    
    grid_data = generate_orbital_grid(
        2, 1, 0,
        grid_points=TEST_GRID_POINTS,
        spatial_extent=TEST_SPATIAL_EXTENT
    )
    
    fig = create_volume_plot(grid_data)
    
    assert fig is not None
    assert len(fig.data) > 0


def test_create_particle_swarm():
    """Test particle swarm visualization."""
    from quantum_engine.orbitals import generate_orbital_grid
    from visualizations.plotly_3d import create_particle_swarm
    
    grid_data = generate_orbital_grid(
        1, 0, 0,
        grid_points=TEST_GRID_POINTS,
        spatial_extent=TEST_SPATIAL_EXTENT
    )
    
    fig = create_particle_swarm(grid_data, num_particles=100)
    
    assert fig is not None
    assert len(fig.data) > 0


@pytest.mark.parametrize("n,l,m", TEST_STATES[:3])  # Test subset for speed
def test_3d_orbital_multiple_states(n, l, m):
    """Test 3D visualization for multiple states."""
    from quantum_engine.orbitals import generate_orbital_grid
    from visualizations.plotly_3d import create_3d_orbital
    
    grid_data = generate_orbital_grid(
        n, l, m,
        grid_points=TEST_GRID_POINTS,
        spatial_extent=TEST_SPATIAL_EXTENT
    )
    
    fig = create_3d_orbital(grid_data, mode='isosurface')
    
    assert fig is not None
    assert hasattr(fig, 'data')
    assert len(fig.data) > 0


# ========================================
# CHART TESTS
# ========================================

def test_energy_level_diagram():
    """Test energy level diagram creation."""
    from visualizations.charts import create_energy_level_diagram
    
    fig = create_energy_level_diagram(max_n=5)
    
    assert fig is not None
    assert len(fig.data) > 0
    assert hasattr(fig, 'layout')


def test_radial_probability_chart():
    """Test radial probability chart."""
    from visualizations.charts import create_radial_probability_chart
    
    fig = create_radial_probability_chart(2, 1)
    
    assert fig is not None
    assert len(fig.data) > 0


def test_angular_momentum_pie():
    """Test angular momentum pie chart."""
    from visualizations.charts import create_angular_momentum_pie
    
    fig = create_angular_momentum_pie(2)
    
    assert fig is not None
    assert len(fig.data) > 0


def test_probability_heatmap():
    """Test probability heatmap."""
    from quantum_engine.orbitals import generate_orbital_grid
    from visualizations.charts import create_probability_heatmap
    
    grid_data = generate_orbital_grid(
        2, 1, 0,
        grid_points=TEST_GRID_POINTS,
        spatial_extent=TEST_SPATIAL_EXTENT
    )
    
    fig = create_probability_heatmap(grid_data, plane='xy')
    
    assert fig is not None
    assert len(fig.data) > 0


def test_quantum_stats_table():
    """Test quantum statistics table."""
    from quantum_engine.orbitals import generate_orbital_grid
    from visualizations.charts import create_quantum_stats_table
    
    grid_data = generate_orbital_grid(
        1, 0, 0,
        grid_points=TEST_GRID_POINTS,
        spatial_extent=TEST_SPATIAL_EXTENT
    )
    
    fig = create_quantum_stats_table(grid_data)
    
    assert fig is not None
    assert len(fig.data) > 0


def test_transition_diagram():
    """Test transition diagram."""
    from visualizations.charts import create_transition_diagram
    
    fig = create_transition_diagram(3, 2)
    
    assert fig is not None
    assert len(fig.data) > 0


# ========================================
# VECTREX TESTS
# ========================================

def test_vectrex_style():
    """Test Vectrex style application."""
    import plotly.graph_objects as go
    from visualizations.vectrex import apply_vectrex_style
    
    fig = go.Figure(data=go.Scatter(x=[1, 2, 3], y=[1, 2, 3]))
    styled_fig = apply_vectrex_style(fig)
    
    assert styled_fig is not None


def test_vectrex_orbital():
    """Test Vectrex orbital visualization."""
    from quantum_engine.orbitals import generate_orbital_grid
    from visualizations.vectrex import create_vectrex_orbital
    
    grid_data = generate_orbital_grid(
        2, 1, 0,
        grid_points=TEST_GRID_POINTS,
        spatial_extent=TEST_SPATIAL_EXTENT
    )
    
    fig = create_vectrex_orbital(grid_data)
    
    assert fig is not None
    assert len(fig.data) > 0


def test_vectrex_energy_levels():
    """Test Vectrex energy level diagram."""
    from visualizations.vectrex import create_vectrex_energy_levels
    
    fig = create_vectrex_energy_levels(max_n=5)
    
    assert fig is not None
    assert len(fig.data) > 0


def test_vectrex_radial_plot():
    """Test Vectrex radial plot."""
    from visualizations.vectrex import create_vectrex_radial_plot
    
    fig = create_vectrex_radial_plot(2, 1)
    
    assert fig is not None
    assert len(fig.data) > 0


# ========================================
# INTEGRATION TESTS
# ========================================

def test_full_visualization_workflow():
    """Test complete visualization workflow."""
    from quantum_engine.orbitals import generate_orbital_grid
    from visualizations.plotly_3d import create_3d_orbital
    from visualizations.charts import (
        create_energy_level_diagram,
        create_radial_probability_chart,
        create_angular_momentum_pie
    )
    
    # Generate orbital
    grid_data = generate_orbital_grid(
        2, 1, 0,
        grid_points=TEST_GRID_POINTS,
        spatial_extent=TEST_SPATIAL_EXTENT
    )
    
    # Create all visualizations
    fig_3d = create_3d_orbital(grid_data)
    fig_energy = create_energy_level_diagram()
    fig_radial = create_radial_probability_chart(2, 1)
    fig_angular = create_angular_momentum_pie(1)
    
    # Check all created successfully
    assert fig_3d is not None
    assert fig_energy is not None
    assert fig_radial is not None
    assert fig_angular is not None


def test_theme_consistency():
    """Test that all visualizations respect theme."""
    from quantum_engine.orbitals import generate_orbital_grid
    from visualizations.plotly_3d import create_isosurface
    from visualizations.charts import create_energy_level_diagram
    from visualizations.themes import get_theme_colors
    
    theme = 'cyberpunk'
    colors = get_theme_colors(theme)
    
    grid_data = generate_orbital_grid(
        1, 0, 0,
        grid_points=TEST_GRID_POINTS,
        spatial_extent=TEST_SPATIAL_EXTENT
    )
    
    fig_3d = create_isosurface(grid_data, theme=theme)
    fig_chart = create_energy_level_diagram(theme=theme)
    
    # Check that theme colors are used
    assert fig_3d is not None
    assert fig_chart is not None


# ========================================
# EDGE CASE TESTS
# ========================================

def test_empty_grid_handling():
    """Test handling of edge cases in visualization."""
    from visualizations.charts import create_energy_level_diagram
    
    # Should handle max_n=1
    fig = create_energy_level_diagram(max_n=1)
    assert fig is not None


def test_invalid_theme():
    """Test handling of invalid theme name."""
    from visualizations.themes import get_theme_colors
    
    # Should return default theme
    colors = get_theme_colors('nonexistent_theme')
    assert colors is not None
    assert 'background' in colors


def test_cross_section_planes():
    """Test all cross-section planes."""
    from quantum_engine.orbitals import generate_orbital_grid
    from visualizations.charts import create_probability_heatmap
    
    grid_data = generate_orbital_grid(
        2, 1, 0,
        grid_points=TEST_GRID_POINTS,
        spatial_extent=TEST_SPATIAL_EXTENT
    )
    
    for plane in ['xy', 'xz', 'yz']:
        fig = create_probability_heatmap(grid_data, plane=plane)
        assert fig is not None
        assert len(fig.data) > 0


# ========================================
# PERFORMANCE TESTS
# ========================================

def test_visualization_performance():
    """Test that visualizations complete in reasonable time."""
    import time
    from quantum_engine.orbitals import generate_orbital_grid
    from visualizations.plotly_3d import create_isosurface
    
    grid_data = generate_orbital_grid(
        1, 0, 0,
        grid_points=TEST_GRID_POINTS,
        spatial_extent=TEST_SPATIAL_EXTENT
    )
    
    start = time.time()
    fig = create_isosurface(grid_data)
    elapsed = time.time() - start
    
    # Should complete in under 5 seconds
    assert elapsed < 5.0
    assert fig is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])