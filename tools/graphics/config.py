"""
Design System Constants
========================
All visual design constants for course graphics.
Change values here to update all graphics globally.
"""


# ── Utility Functions ────────────────────────────────────────────────────

def _hex_to_rgb(hex_color):
    """Convert hex color string to RGB tuple (0-1 range)."""
    h = hex_color.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4))


def hex_to_rgba(hex_color, alpha=1.0):
    """Convert hex color to RGBA tuple (0-1 range)."""
    return (*_hex_to_rgb(hex_color), alpha)


# ── Color Palette (Modern/Bold) ──────────────────────────────────────────

COLORS = {
    # Primary
    'navy':         '#1B2A4A',
    'steel_blue':   '#3D5A80',

    # Accents
    'teal':         '#2A9D8F',
    'gold':         '#E9C46A',
    'orange':       '#E76F51',
    'red':          '#C1292E',

    # Neutrals
    'bg':           '#F8F9FA',
    'grid':         '#E9ECEF',
    'border':       '#DEE2E6',
    'text':         '#212529',
    'text_secondary': '#495057',
    'text_on_dark': '#F8F9FA',
    'white':        '#FFFFFF',
}

# Region fills (with alpha for translucency)
REGION_COLORS = {
    'grow':    hex_to_rgba(COLORS['teal'], 0.20),
    'hold':    hex_to_rgba(COLORS['gold'], 0.20),
    'harvest': hex_to_rgba(COLORS['red'], 0.20),
    'neutral': hex_to_rgba(COLORS['grid'], 1.0),
}

# ── Typography ───────────────────────────────────────────────────────────

FONTS = {
    'family':           ['Segoe UI', 'Arial', 'sans-serif'],
    'figure_num_size':  13,
    'title_size':       12,
    'axis_label_size':  11,
    'cell_label_size':  11,
    'body_size':        9,
    'note_size':        8,
}

# ── Layout ───────────────────────────────────────────────────────────────

FIGURE = {
    'width':        10,
    'height':       7,
    'tall_width':   8,
    'tall_height':  10,
    'dpi':          200,
    'bg_color':     COLORS['bg'],
    'border_color': COLORS['border'],
    'border_width': 1.0,
    'title_height': 0.10,   # fraction of figure height reserved for title
}

# ── Quadrant / Matrix Color Maps ─────────────────────────────────────────

# BCG Matrix
BCG_COLORS = {
    'stars':          COLORS['teal'],
    'question_marks': COLORS['orange'],
    'cash_cows':      COLORS['gold'],
    'dogs':           COLORS['red'],
}

# IE Matrix regions
IE_COLORS = {
    'grow_build':     COLORS['teal'],
    'hold_maintain':  COLORS['gold'],
    'harvest_divest': COLORS['red'],
}

# SPACE Matrix postures
SPACE_COLORS = {
    'aggressive':   COLORS['teal'],
    'conservative': COLORS['steel_blue'],
    'defensive':    COLORS['red'],
    'competitive':  COLORS['orange'],
}

# Generic strategy mapping
STRATEGY_COLORS = {
    'positive':  COLORS['teal'],
    'neutral':   COLORS['gold'],
    'caution':   COLORS['orange'],
    'negative':  COLORS['red'],
    'primary':   COLORS['navy'],
    'secondary': COLORS['steel_blue'],
}
