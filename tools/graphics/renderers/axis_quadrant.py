"""
Axis Quadrant Renderer
=======================
Renders four-quadrant axis diagrams like the SPACE Matrix and Perceptual Map.
These use actual X-Y axes (not filled matrix cells) with a coordinate-based layout.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from tools.graphics.config import COLORS, FONTS, FIGURE, SPACE_COLORS
from tools.graphics.base import create_figure, save_figure, wrap_text, hide_axes


def render(figure_entry, data, output_path):
    """
    Render an axis-quadrant figure.

    data keys:
        x_label:        str  – X-axis label (e.g., "Competitive Advantage")
        y_label:        str  – Y-axis label (e.g., "Industry Strength")
        x_pos_label:    str  – label at +X end
        x_neg_label:    str  – label at -X end
        y_pos_label:    str  – label at +Y end
        y_neg_label:    str  – label at -Y end
        quadrants:      list of 4 dicts (Q1=top-right, Q2=top-left, Q3=bottom-left, Q4=bottom-right):
            name:       str  – quadrant label
            color:      str  – hex color or COLORS key
            items:      list of str – strategies or items (optional)
        vector:         dict (optional) – directional vector arrow:
            x:          float – x component (-6 to +6)
            y:          float – y component (-6 to +6)
            label:      str  – vector label
        points:         list of dicts (optional) – plotted points:
            x:          float – x position
            y:          float – y position
            label:      str  – point label
            color:      str  – point color
            size:       int  – marker size (optional)
        axis_range:     float – axis range (default 6)
        show_grid:      bool – show grid lines (default True)
        scale_labels:   bool – show numeric scale on axes (default True)
    """
    fig, ax = create_figure(figure_entry['figure_number'], figure_entry['title'])

    axis_range = data.get('axis_range', 6)

    # Set up coordinate system
    ax.set_xlim(-axis_range - 0.5, axis_range + 0.5)
    ax.set_ylim(-axis_range - 0.5, axis_range + 0.5)
    ax.set_aspect('equal')

    # Grid
    if data.get('show_grid', True):
        for v in range(-int(axis_range), int(axis_range) + 1):
            if v == 0:
                continue
            ax.axhline(y=v, color=COLORS['grid'], linewidth=0.5, zorder=0)
            ax.axvline(x=v, color=COLORS['grid'], linewidth=0.5, zorder=0)

    # Quadrant background fills
    quadrants = data.get('quadrants', [])
    quad_positions = [
        (0, 0, axis_range, axis_range),             # Q1: top-right
        (-axis_range, 0, axis_range, axis_range),    # Q2: top-left
        (-axis_range, -axis_range, axis_range, axis_range),  # Q3: bottom-left
        (0, -axis_range, axis_range, axis_range),    # Q4: bottom-right
    ]

    for i, q in enumerate(quadrants[:4]):
        qx, qy, qw, qh = quad_positions[i]
        color = COLORS.get(q.get('color', 'grid'), q.get('color', COLORS['grid']))

        rect = patches.Rectangle(
            (qx, qy), qw, qh,
            facecolor=color,
            alpha=0.15,
            edgecolor='none',
            zorder=0
        )
        ax.add_patch(rect)

        # Quadrant label
        name = q.get('name', '')
        label_x = qx + qw / 2
        label_y = qy + qh * 0.80

        ax.text(label_x, label_y, name,
                ha='center', va='center',
                fontsize=FONTS['cell_label_size'],
                fontweight='bold',
                fontfamily=FONTS['family'],
                color=COLORS['text'],
                zorder=5)

        # Strategy items
        items = q.get('items', [])
        for j, item in enumerate(items[:5]):
            iy = label_y - (j + 1) * (qh * 0.13)
            ax.text(label_x, iy, f'• {item}',
                    ha='center', va='center',
                    fontsize=FONTS['note_size'],
                    fontfamily=FONTS['family'],
                    color=COLORS['text_secondary'],
                    zorder=5)

    # Main axes (bold cross)
    ax.axhline(y=0, color=COLORS['text'], linewidth=2, zorder=2)
    ax.axvline(x=0, color=COLORS['text'], linewidth=2, zorder=2)

    # Arrow tips on axes
    arrow_size = axis_range * 0.08
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        ax.annotate('', xy=(dx * axis_range, dy * axis_range),
                     xytext=(dx * (axis_range - arrow_size * 2),
                             dy * (axis_range - arrow_size * 2)),
                     arrowprops=dict(arrowstyle='->', color=COLORS['text'],
                                    lw=2),
                     zorder=3)

    # Axis endpoint labels
    offset = 0.4
    for key, pos in [('x_pos_label', (axis_range, -offset)),
                     ('x_neg_label', (-axis_range, -offset)),
                     ('y_pos_label', (offset, axis_range)),
                     ('y_neg_label', (offset, -axis_range))]:
        label = data.get(key, '')
        if label:
            ha = 'center' if 'x_' in key else 'left'
            va = 'top' if key == 'y_neg_label' else 'bottom' if key == 'y_pos_label' else 'top'
            ax.text(pos[0], pos[1], label,
                    ha=ha, va=va,
                    fontsize=FONTS['note_size'],
                    fontweight='bold',
                    fontfamily=FONTS['family'],
                    color=COLORS['text_secondary'],
                    zorder=5)

    # Scale labels
    if data.get('scale_labels', True):
        for v in range(-int(axis_range), int(axis_range) + 1):
            if v == 0:
                continue
            ax.text(v, -0.3, str(v),
                    ha='center', va='top',
                    fontsize=6, color=COLORS['text_secondary'],
                    fontfamily=FONTS['family'])
            ax.text(-0.3, v, str(v),
                    ha='right', va='center',
                    fontsize=6, color=COLORS['text_secondary'],
                    fontfamily=FONTS['family'])

    # Axis labels
    x_label = data.get('x_label', '')
    y_label = data.get('y_label', '')

    if x_label:
        ax.text(0, -axis_range - 0.3, x_label,
                ha='center', va='top',
                fontsize=FONTS['axis_label_size'],
                fontweight='bold',
                fontfamily=FONTS['family'],
                color=COLORS['text'])

    if y_label:
        ax.text(-axis_range - 0.3, 0, y_label,
                ha='center', va='center',
                fontsize=FONTS['axis_label_size'],
                fontweight='bold',
                fontfamily=FONTS['family'],
                color=COLORS['text'],
                rotation=90)

    # Vector arrow (SPACE style)
    vector = data.get('vector')
    if vector:
        vx, vy = vector.get('x', 0), vector.get('y', 0)
        ax.annotate('',
                    xy=(vx, vy), xytext=(0, 0),
                    arrowprops=dict(arrowstyle='->', color=COLORS['red'],
                                   lw=3),
                    zorder=6)
        # Vector label
        vlabel = vector.get('label', '')
        if vlabel:
            ax.text(vx * 1.1, vy * 1.1, vlabel,
                    ha='center', va='center',
                    fontsize=FONTS['body_size'],
                    fontweight='bold',
                    fontfamily=FONTS['family'],
                    color=COLORS['red'],
                    bbox=dict(boxstyle='round,pad=0.2',
                              facecolor=COLORS['bg'],
                              edgecolor=COLORS['red'],
                              alpha=0.9),
                    zorder=7)

    # Plotted points (Perceptual Map style)
    points = data.get('points', [])
    for pt in points:
        px, py = pt.get('x', 0), pt.get('y', 0)
        pc = COLORS.get(pt.get('color', 'teal'), pt.get('color', COLORS['teal']))
        ps = pt.get('size', 80)
        ax.scatter([px], [py], s=ps, c=[pc], edgecolors=COLORS['text'],
                   linewidths=0.8, zorder=6)
        plabel = pt.get('label', '')
        if plabel:
            ax.text(px + 0.2, py + 0.2, plabel,
                    ha='left', va='bottom',
                    fontsize=FONTS['note_size'],
                    fontfamily=FONTS['family'],
                    color=COLORS['text'],
                    zorder=7)

    # Clean up axes appearance
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    save_figure(fig, output_path)
