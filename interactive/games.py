"""
Gamification and Challenges
============================

Interactive games and challenges to make learning quantum mechanics fun:
- Orbital matching game
- Probability challenges
- Speed run modes
- Achievement tracking
"""

import numpy as np
from dash import html, dcc
import random
import config


def orbital_matching_game(difficulty='medium'):
    """
    Generate orbital matching challenge.
    
    Player is shown an orbital shape and must identify the quantum numbers.
    
    Parameters
    ----------
    difficulty : str
        'easy', 'medium', 'hard', 'expert'
        
    Returns
    -------
    dict
        Challenge data including correct answer and options
    """
    # Define difficulty ranges
    difficulty_ranges = {
        'easy': {'n': (1, 3), 'l_max': 1},      # 1s, 2s, 2p
        'medium': {'n': (1, 4), 'l_max': 2},    # up to 3d
        'hard': {'n': (1, 5), 'l_max': 3},      # up to 4f
        'expert': {'n': (1, 7), 'l_max': 4}     # up to 5g
    }
    
    ranges = difficulty_ranges.get(difficulty, difficulty_ranges['medium'])
    
    # Generate random target orbital
    n = random.randint(ranges['n'][0], ranges['n'][1])
    l = random.randint(0, min(n - 1, ranges['l_max']))
    m = random.randint(-l, l)
    
    # Generate wrong options
    wrong_options = []
    while len(wrong_options) < 3:
        wrong_n = random.randint(ranges['n'][0], ranges['n'][1])
        wrong_l = random.randint(0, min(wrong_n - 1, ranges['l_max']))
        wrong_m = random.randint(-wrong_l, wrong_l)
        
        option = (wrong_n, wrong_l, wrong_m)
        if option != (n, l, m) and option not in wrong_options:
            wrong_options.append(option)
    
    # Create answer options
    from quantum_engine.orbitals import get_orbital_name
    
    correct_answer = (n, l, m)
    all_options = [correct_answer] + wrong_options
    random.shuffle(all_options)
    
    options_display = [
        {
            'label': f"{get_orbital_name(*opt)} (n={opt[0]}, l={opt[1]}, m={opt[2]})",
            'value': str(opt)
        }
        for opt in all_options
    ]
    
    return {
        'type': 'orbital_matching',
        'difficulty': difficulty,
        'target_orbital': correct_answer,
        'target_name': get_orbital_name(n, l, m),
        'options': options_display,
        'correct_answer': str(correct_answer),
        'hint': f"Look at the shape and number of nodes"
    }


def probability_challenge(grid_data, difficulty='medium'):
    """
    Generate probability finding challenge.
    
    Player must find a point/region with specific probability threshold.
    
    Parameters
    ----------
    grid_data : dict
        Orbital grid data
    difficulty : str
        Challenge difficulty
        
    Returns
    -------
    dict
        Challenge specifications
    """
    # Define thresholds based on difficulty
    thresholds = {
        'easy': 0.001,
        'medium': 0.005,
        'hard': 0.01,
        'expert': 0.05
    }
    
    threshold = thresholds.get(difficulty, 0.005)
    max_prob = np.max(grid_data['prob_density'])
    target_prob = threshold * max_prob
    
    # Find points that meet criteria
    prob = grid_data['prob_density']
    valid_mask = prob >= target_prob
    
    num_valid = np.sum(valid_mask)
    
    return {
        'type': 'probability_challenge',
        'difficulty': difficulty,
        'target_probability': target_prob,
        'threshold_percent': threshold * 100,
        'num_valid_points': num_valid,
        'max_probability': max_prob,
        'challenge_text': f"Find a point with probability ≥ {target_prob:.4e}",
        'hint': "Look near the nucleus for s orbitals, or lobes for p/d orbitals"
    }


def speed_run_challenge(max_time=60):
    """
    Generate speed run challenge: identify as many orbitals as possible.
    
    Parameters
    ----------
    max_time : int
        Time limit in seconds
        
    Returns
    -------
    dict
        Challenge configuration
    """
    # Generate sequence of orbitals to identify
    num_challenges = 10
    challenges = []
    
    for _ in range(num_challenges):
        n = random.randint(1, 4)
        l = random.randint(0, min(n - 1, 2))
        m = random.randint(-l, l)
        challenges.append((n, l, m))
    
    return {
        'type': 'speed_run',
        'time_limit': max_time,
        'challenges': challenges,
        'num_challenges': num_challenges,
        'points_per_correct': 10,
        'time_bonus_threshold': 30  # Bonus if completed in under 30s
    }


def generate_challenge(challenge_type='random', difficulty='medium', grid_data=None):
    """
    Generate a random challenge of specified type.
    
    Parameters
    ----------
    challenge_type : str
        'random', 'orbital_matching', 'probability', 'speed_run'
    difficulty : str
        Challenge difficulty
    grid_data : dict, optional
        Orbital data (needed for probability challenges)
        
    Returns
    -------
    dict
        Challenge specification
    """
    if challenge_type == 'random':
        challenge_type = random.choice(['orbital_matching', 'probability'])
    
    if challenge_type == 'orbital_matching':
        return orbital_matching_game(difficulty)
    elif challenge_type == 'probability' and grid_data is not None:
        return probability_challenge(grid_data, difficulty)
    elif challenge_type == 'speed_run':
        return speed_run_challenge()
    else:
        # Default to orbital matching
        return orbital_matching_game(difficulty)


def create_achievement_tracker():
    """
    Create achievement tracking system.
    
    Returns
    -------
    dict
        Achievement definitions and tracking
    """
    achievements = {
        'first_orbital': {
            'name': 'First Steps',
            'description': 'View your first orbital',
            'icon': '🌟',
            'unlocked': False
        },
        'orbital_explorer': {
            'name': 'Orbital Explorer',
            'description': 'View 10 different orbitals',
            'icon': '🔭',
            'threshold': 10,
            'progress': 0,
            'unlocked': False
        },
        'orbital_master': {
            'name': 'Orbital Master',
            'description': 'View all orbitals up to n=4',
            'icon': '👑',
            'threshold': config.ACHIEVEMENT_THRESHOLDS['orbital_master'],
            'progress': 0,
            'unlocked': False
        },
        'superposition_novice': {
            'name': 'Superposition Novice',
            'description': 'Create your first superposition state',
            'icon': '🌊',
            'unlocked': False
        },
        'superposition_guru': {
            'name': 'Superposition Guru',
            'description': 'Create 20 superposition states',
            'icon': '🧙',
            'threshold': config.ACHIEVEMENT_THRESHOLDS['superposition_guru'],
            'progress': 0,
            'unlocked': False
        },
        'measurement_pro': {
            'name': 'Measurement Pro',
            'description': 'Perform 50 measurements',
            'icon': '🔬',
            'threshold': 50,
            'progress': 0,
            'unlocked': False
        },
        'theme_collector': {
            'name': 'Theme Collector',
            'description': 'Try all visual themes',
            'icon': '🎨',
            'threshold': 5,
            'progress': 0,
            'unlocked': False
        },
        'speed_runner': {
            'name': 'Speed Runner',
            'description': 'Complete speed run in under 30 seconds',
            'icon': '⚡',
            'threshold': config.ACHIEVEMENT_THRESHOLDS['speed_runner'],
            'progress': 0,
            'unlocked': False
        },
        'challenge_master': {
            'name': 'Challenge Master',
            'description': 'Complete 10 challenges successfully',
            'icon': '🏆',
            'threshold': 10,
            'progress': 0,
            'unlocked': False
        },
        'vectrex_veteran': {
            'name': 'Vectrex Veteran',
            'description': 'Use Vectrex theme for 10 orbitals',
            'icon': '📺',
            'threshold': 10,
            'progress': 0,
            'unlocked': False
        }
    }
    
    return achievements


def check_achievement_unlock(achievements, achievement_key, increment=False):
    """
    Check if achievement should be unlocked.
    
    Parameters
    ----------
    achievements : dict
        Achievement tracker
    achievement_key : str
        Achievement to check
    increment : bool
        Whether to increment progress
        
    Returns
    -------
    bool
        True if newly unlocked
    """
    if achievement_key not in achievements:
        return False
    
    achievement = achievements[achievement_key]
    
    # Already unlocked
    if achievement.get('unlocked', False):
        return False
    
    # Increment progress if requested
    if increment and 'progress' in achievement:
        achievement['progress'] += 1
    
    # Check if threshold met
    if 'threshold' in achievement:
        if achievement['progress'] >= achievement['threshold']:
            achievement['unlocked'] = True
            return True
    else:
        # No threshold, unlock immediately
        achievement['unlocked'] = True
        return True
    
    return False


def create_game_ui():
    """
    Create game/challenge UI components.
    
    Returns
    -------
    dash.html.Div
        Game interface
    """
    ui = html.Div([
        html.H4("🎮 Challenges & Games", style={'marginBottom': '15px'}),
        
        # Difficulty selector
        html.Div([
            html.Label("Difficulty Level", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            dcc.RadioItems(
                id='difficulty-selector',
                options=[
                    {'label': ' Easy', 'value': 'easy'},
                    {'label': ' Medium', 'value': 'medium'},
                    {'label': ' Hard', 'value': 'hard'},
                    {'label': ' Expert', 'value': 'expert'}
                ],
                value='medium',
                inline=True,
                style={'marginTop': '5px'}
            )
        ], style={'marginBottom': '20px'}),
        
        # Challenge type selector
        html.Div([
            html.Label("Challenge Type", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            dcc.Dropdown(
                id='challenge-type-dropdown',
                options=[
                    {'label': '🎯 Orbital Matching', 'value': 'orbital_matching'},
                    {'label': '📍 Probability Hunt', 'value': 'probability'},
                    {'label': '⚡ Speed Run', 'value': 'speed_run'},
                    {'label': '🎲 Random', 'value': 'random'}
                ],
                value='orbital_matching',
                clearable=False,
                style={'color': '#000000'}
            )
        ], style={'marginBottom': '20px'}),
        
        # Start button
        html.Button("🚀 Start Challenge", id='start-challenge-btn',
                   style={'width': '100%', 'padding': '12px',
                         'backgroundColor': '#4CC9F0', 'color': '#000',
                         'border': 'none', 'borderRadius': '5px',
                         'cursor': 'pointer', 'fontSize': '16px',
                         'fontWeight': 'bold', 'marginBottom': '20px'}),
        
        # Challenge display area
        html.Div(id='challenge-display',
                style={'padding': '15px', 'backgroundColor': '#1B263B',
                      'borderRadius': '5px', 'minHeight': '200px'}),
        
        # Score display
        html.Div([
            html.H5("Score", style={'marginBottom': '10px'}),
            html.Div([
                html.Span("Current: ", style={'fontWeight': 'bold'}),
                html.Span(id='current-score', children='0', 
                         style={'fontSize': '24px', 'color': '#4CC9F0'}),
                html.Span(" | ", style={'margin': '0 10px'}),
                html.Span("Best: ", style={'fontWeight': 'bold'}),
                html.Span(id='best-score', children='0',
                         style={'fontSize': '24px', 'color': '#F72585'})
            ])
        ], style={'marginTop': '20px', 'padding': '15px',
                 'backgroundColor': '#0A0E27', 'borderRadius': '5px'}),
        
        # Timer (for speed runs)
        html.Div([
            html.Div(id='challenge-timer',
                    style={'fontSize': '32px', 'fontWeight': 'bold',
                          'color': '#7209B7', 'textAlign': 'center'})
        ], style={'marginTop': '15px', 'padding': '10px'}),
        
        # Timer interval
        dcc.Interval(
            id='challenge-timer-interval',
            interval=100,  # 100ms
            n_intervals=0,
            disabled=True
        )
        
    ], style={'padding': '20px'})
    
    return ui


def create_achievement_ui(achievements):
    """
    Create achievement display UI.
    
    Parameters
    ----------
    achievements : dict
        Achievement tracker
        
    Returns
    -------
    dash.html.Div
        Achievement display
    """
    achievement_items = []
    
    for key, achievement in achievements.items():
        unlocked = achievement.get('unlocked', False)
        
        # Progress bar if applicable
        progress_bar = None
        if 'threshold' in achievement and 'progress' in achievement:
            progress_percent = (achievement['progress'] / achievement['threshold']) * 100
            progress_bar = html.Div([
                html.Div(
                    style={
                        'width': f'{progress_percent}%',
                        'height': '4px',
                        'backgroundColor': '#4CC9F0' if unlocked else '#7209B7',
                        'transition': 'width 0.3s'
                    }
                )
            ], style={
                'width': '100%',
                'height': '4px',
                'backgroundColor': '#1B263B',
                'borderRadius': '2px',
                'marginTop': '5px'
            })
        
        item = html.Div([
            html.Div([
                html.Span(achievement['icon'], style={'fontSize': '24px', 'marginRight': '10px'}),
                html.Div([
                    html.Strong(achievement['name'], 
                              style={'color': '#4CC9F0' if unlocked else '#888'}),
                    html.Br(),
                    html.Small(achievement['description'], 
                             style={'color': '#AAA' if unlocked else '#666'})
                ], style={'flex': '1'}),
                html.Span('✓' if unlocked else '🔒',
                         style={'fontSize': '20px',
                               'color': '#4CC9F0' if unlocked else '#666'})
            ], style={'display': 'flex', 'alignItems': 'center'}),
            progress_bar
        ], style={
            'padding': '10px',
            'marginBottom': '10px',
            'backgroundColor': '#0A0E27' if unlocked else '#1B263B',
            'borderRadius': '5px',
            'border': f'2px solid {"#4CC9F0" if unlocked else "#3A3A3A"}'
        })
        
        achievement_items.append(item)
    
    ui = html.Div([
        html.H4("🏆 Achievements", style={'marginBottom': '15px'}),
        html.Div(achievement_items)
    ], style={'padding': '20px'})
    
    return ui


def validate_challenge_answer(challenge, user_answer):
    """
    Validate user's answer to challenge.
    
    Parameters
    ----------
    challenge : dict
        Challenge specification
    user_answer : str or dict
        User's answer
        
    Returns
    -------
    dict
        Validation result with feedback
    """
    if challenge['type'] == 'orbital_matching':
        correct = (str(user_answer) == challenge['correct_answer'])
        
        return {
            'correct': correct,
            'feedback': "🎉 Correct! Well done!" if correct else "❌ Not quite. Try again!",
            'points': 10 if correct else 0,
            'correct_answer': challenge['correct_answer']
        }
    
    elif challenge['type'] == 'probability_challenge':
        # Check if measured probability meets threshold
        measured_prob = user_answer.get('probability', 0)
        target = challenge['target_probability']
        
        correct = measured_prob >= target
        
        return {
            'correct': correct,
            'feedback': f"🎉 Found it! Probability: {measured_prob:.4e}" if correct 
                       else f"❌ Too low. Found: {measured_prob:.4e}, Need: ≥{target:.4e}",
            'points': 15 if correct else 0,
            'measured': measured_prob,
            'target': target
        }
    
    return {
        'correct': False,
        'feedback': "Unknown challenge type",
        'points': 0
    }