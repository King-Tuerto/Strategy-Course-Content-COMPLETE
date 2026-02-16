"""
Flowchart Renderer
===================
Renders process flows, decision trees, cascades, and multi-step diagrams.
Supports horizontal and vertical layouts with branching.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from tools.graphics.config import COLORS, FONTS, FIGURE
from tools.graphics.base import create_figure, save_figure, wrap_text, draw_rounded_box, draw_arrow, hide_axes


def render(figure_entry, data, output_path):
    """
    Render a flowchart figure.

    data keys:
        orientation:    str  – "vertical" (default), "horizontal", or "cascade"
        nodes:          list of dicts:
            id:         str  – unique node identifier
            label:      str  – display text
            color:      str  – COLORS key or hex (default 'navy')
            level:      int  – vertical tier (0 = top), used for vertical/cascade
            col:        int  – horizontal position (0 = leftmost)
            width:      float – override width (0-1 scale, optional)
            shape:      str  – 'box' (default), 'diamond', 'oval'
        connections:    list of dicts:
            from:       str  – source node id
            to:         str  – target node id
            label:      str  – connection label (optional)
        title_box:      dict (optional) – top header box
            label:      str
            color:      str
        col_count:      int  – total columns in layout (default auto)
        level_count:    int  – total levels in layout (default auto)
    """
    fig, ax = create_figure(figure_entry['figure_number'], figure_entry['title'])
    hide_axes(ax)

    nodes = data.get('nodes', [])
    connections = data.get('connections', [])
    orientation = data.get('orientation', 'vertical')

    # Calculate grid dimensions
    if nodes:
        max_level = max(n.get('level', 0) for n in nodes)
        max_col = max(n.get('col', 0) for n in nodes)
    else:
        max_level, max_col = 0, 0

    level_count = data.get('level_count', max_level + 1)
    col_count = data.get('col_count', max_col + 1)

    # Layout parameters
    margin_x, margin_y = 0.06, 0.04
    usable_w = 1.0 - 2 * margin_x
    usable_h = 1.0 - 2 * margin_y

    # Check for title_box and adjust
    title_box = data.get('title_box')
    if title_box:
        tb_h = 0.08
        draw_rounded_box(ax, margin_x, 1.0 - margin_y - tb_h,
                         usable_w, tb_h,
                         title_box.get('label', ''),
                         color=title_box.get('color', 'navy'),
                         fontsize=FONTS['cell_label_size'])
        usable_h -= (tb_h + 0.02)
        top_start = 1.0 - margin_y - tb_h - 0.02
    else:
        top_start = 1.0 - margin_y

    # Node sizing
    if orientation == 'horizontal':
        node_w = min(0.18, usable_w / (col_count + 0.5))
        node_h = min(0.12, usable_h / (level_count + 0.5))
    else:
        node_w = min(0.22, usable_w / (col_count + 0.5))
        node_h = min(0.08, usable_h / (level_count + 0.5))

    # Calculate node positions
    node_positions = {}
    for n in nodes:
        level = n.get('level', 0)
        col = n.get('col', 0)
        nw = n.get('width', node_w)

        if orientation == 'horizontal':
            # Levels go left-to-right, cols go top-to-bottom
            cell_w = usable_w / level_count
            cell_h = usable_h / col_count
            cx = margin_x + level * cell_w + cell_w / 2
            cy = top_start - col * cell_h - cell_h / 2
        else:
            # Levels go top-to-bottom, cols go left-to-right
            cell_w = usable_w / col_count
            cell_h = usable_h / level_count
            cx = margin_x + col * cell_w + cell_w / 2
            cy = top_start - level * cell_h - cell_h / 2

        node_positions[n['id']] = {
            'cx': cx, 'cy': cy,
            'w': nw, 'h': node_h,
            'x': cx - nw / 2, 'y': cy - node_h / 2,
        }

        # Draw node
        shape = n.get('shape', 'box')
        color = n.get('color', 'navy')

        if shape == 'diamond':
            _draw_diamond(ax, cx, cy, nw, node_h,
                          n.get('label', ''), color)
        elif shape == 'oval':
            _draw_oval(ax, cx, cy, nw, node_h,
                       n.get('label', ''), color)
        else:
            draw_rounded_box(ax, cx - nw / 2, cy - node_h / 2,
                             nw, node_h,
                             n.get('label', ''),
                             color=color,
                             fontsize=FONTS['body_size'],
                             text_wrap=18)

    # Draw connections
    for conn in connections:
        from_id = conn.get('from', conn.get('from_id', ''))
        to_id = conn.get('to', conn.get('to_id', ''))
        label = conn.get('label', '')

        if from_id not in node_positions or to_id not in node_positions:
            continue

        fp = node_positions[from_id]
        tp = node_positions[to_id]

        # Determine connection points based on relative position
        fx, fy = _get_connection_point(fp, tp, 'out', orientation)
        tx, ty = _get_connection_point(tp, fp, 'in', orientation)

        draw_arrow(ax, fx, fy, tx, ty, label=label,
                   color='steel_blue', linewidth=1.5)

    save_figure(fig, output_path)


def _get_connection_point(src, dst, direction, orientation):
    """Calculate best connection point on a node edge."""
    cx, cy = src['cx'], src['cy']
    w, h = src['w'], src['h']
    dx = dst['cx'] - cx
    dy = dst['cy'] - cy

    # Prefer vertical connections for vertical layout
    if orientation == 'horizontal':
        if direction == 'out':
            return cx + w / 2, cy  # right edge
        else:
            return cx - w / 2, cy  # left edge
    else:
        if abs(dx) > abs(dy) * 1.5:
            # Side connection
            if dx > 0:
                return cx + w / 2, cy
            else:
                return cx - w / 2, cy
        else:
            # Top/bottom connection
            if direction == 'out':
                return cx, cy - h / 2  # bottom
            else:
                return cx, cy + h / 2  # top


def _draw_diamond(ax, cx, cy, w, h, text, color='gold'):
    """Draw a diamond shape (for decisions)."""
    fill_color = COLORS.get(color, color)
    s = max(w, h) * 0.7
    diamond = plt.Polygon(
        [(cx, cy + s / 2), (cx + s / 2, cy),
         (cx, cy - s / 2), (cx - s / 2, cy)],
        facecolor=fill_color,
        edgecolor=COLORS['border'],
        linewidth=1.5,
        zorder=2
    )
    ax.add_patch(diamond)

    # Text color
    rgb = tuple(int(fill_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    brightness = (rgb[0] * 299 + rgb[1] * 587 + rgb[2] * 114) / 1000
    tc = COLORS['text_on_dark'] if brightness < 128 else COLORS['text']

    ax.text(cx, cy, wrap_text(text, 14),
            ha='center', va='center',
            fontsize=FONTS['note_size'],
            fontweight='bold',
            fontfamily=FONTS['family'],
            color=tc, zorder=3)


def _draw_oval(ax, cx, cy, w, h, text, color='teal'):
    """Draw an oval/ellipse shape (for start/end)."""
    fill_color = COLORS.get(color, color)
    ellipse = patches.Ellipse(
        (cx, cy), w, h,
        facecolor=fill_color,
        edgecolor=COLORS['border'],
        linewidth=1.5,
        zorder=2
    )
    ax.add_patch(ellipse)

    rgb = tuple(int(fill_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    brightness = (rgb[0] * 299 + rgb[1] * 587 + rgb[2] * 114) / 1000
    tc = COLORS['text_on_dark'] if brightness < 128 else COLORS['text']

    ax.text(cx, cy, wrap_text(text, 16),
            ha='center', va='center',
            fontsize=FONTS['body_size'],
            fontweight='bold',
            fontfamily=FONTS['family'],
            color=tc, zorder=3)
