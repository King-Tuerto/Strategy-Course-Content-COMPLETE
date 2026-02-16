"""
2x2 Matrix Renderer
====================
Renders BCG, Grand Strategy, Porter's Generic Strategies,
Integration-Responsiveness, and other 2x2 matrix graphics.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from tools.graphics.config import COLORS, FONTS, FIGURE, BCG_COLORS, SPACE_COLORS, STRATEGY_COLORS
from tools.graphics.base import create_figure, save_figure, wrap_text, hide_axes


def render(figure_entry, data, output_path):
    """
    Render a 2x2 matrix figure.

    data keys:
        x_label:        str  – X-axis label (e.g., "Relative Market Share")
        y_label:        str  – Y-axis label (e.g., "Industry Growth Rate")
        x_low_label:    str  – label at low end of X axis (optional)
        x_high_label:   str  – label at high end of X axis (optional)
        y_low_label:    str  – label at low end of Y axis (optional)
        y_high_label:   str  – label at high end of Y axis (optional)
        quadrants:      list of 4 dicts (TL, TR, BL, BR order):
            name:       str  – quadrant label
            color:      str  – hex color or COLORS key
            items:      list of str – bullet items inside quadrant (optional)
            subtitle:   str  – smaller text under name (optional)
        show_arrows:    bool – show axis direction arrows (default True)
        axis_reversed:  bool – if True, high is on left / bottom (BCG style)
    """
    fig, ax = create_figure(figure_entry['figure_number'], figure_entry['title'])
    hide_axes(ax)

    # Margins
    left, right, bottom, top = 0.12, 0.95, 0.08, 0.92
    mid_x = (left + right) / 2
    mid_y = (bottom + top) / 2
    qw = (right - left) / 2
    qh = (top - bottom) / 2

    # Quadrant positions: TL, TR, BL, BR
    positions = [
        (left, mid_y, qw, qh),      # TL = quadrants[0]
        (mid_x, mid_y, qw, qh),     # TR = quadrants[1]
        (left, bottom, qw, qh),     # BL = quadrants[2]
        (mid_x, bottom, qw, qh),    # BR = quadrants[3]
    ]

    quadrants = data.get('quadrants', [])
    for i, q in enumerate(quadrants[:4]):
        x, y, w, h = positions[i]
        color = COLORS.get(q.get('color', 'steel_blue'), q.get('color', COLORS['steel_blue']))

        # Draw filled rectangle
        rect = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle='round,pad=0.008',
            facecolor=color,
            edgecolor=COLORS['white'],
            linewidth=2,
            alpha=0.85,
            zorder=2
        )
        ax.add_patch(rect)

        # Quadrant name
        cx, cy = x + w / 2, y + h / 2
        name_text = q.get('name', '')

        # If there are items, shift name up
        items = q.get('items', [])
        subtitle = q.get('subtitle', '')

        if items:
            name_y = cy + h * 0.25
        elif subtitle:
            name_y = cy + h * 0.10
        else:
            name_y = cy

        ax.text(cx, name_y, name_text,
                ha='center', va='center',
                fontsize=FONTS['cell_label_size'],
                fontweight='bold',
                fontfamily=FONTS['family'],
                color=COLORS['text_on_dark'],
                zorder=3)

        # Subtitle
        if subtitle:
            sub_y = name_y - h * 0.12
            ax.text(cx, sub_y, subtitle,
                    ha='center', va='center',
                    fontsize=FONTS['note_size'],
                    fontfamily=FONTS['family'],
                    color=COLORS['text_on_dark'],
                    alpha=0.9,
                    zorder=3)

        # Bullet items
        if items:
            item_start_y = cy - h * 0.05
            spacing = h * 0.12
            for j, item in enumerate(items[:5]):
                iy = item_start_y - j * spacing
                display = wrap_text(item, 22)
                ax.text(cx, iy, f'• {display}',
                        ha='center', va='center',
                        fontsize=FONTS['note_size'],
                        fontfamily=FONTS['family'],
                        color=COLORS['text_on_dark'],
                        alpha=0.9,
                        zorder=3)

    # Axis labels
    x_label = data.get('x_label', '')
    y_label = data.get('y_label', '')

    if x_label:
        ax.text(mid_x, bottom - 0.05, x_label,
                ha='center', va='top',
                fontsize=FONTS['axis_label_size'],
                fontweight='bold',
                fontfamily=FONTS['family'],
                color=COLORS['text'])

    if y_label:
        ax.text(left - 0.06, mid_y, y_label,
                ha='center', va='center',
                fontsize=FONTS['axis_label_size'],
                fontweight='bold',
                fontfamily=FONTS['family'],
                color=COLORS['text'],
                rotation=90)

    # High/Low endpoint labels
    axis_reversed = data.get('axis_reversed', False)

    x_high = data.get('x_high_label', '')
    x_low = data.get('x_low_label', '')
    y_high = data.get('y_high_label', '')
    y_low = data.get('y_low_label', '')

    if x_high:
        xpos = left if axis_reversed else right
        ax.text(xpos, bottom - 0.02, x_high,
                ha='center', va='top',
                fontsize=FONTS['note_size'],
                fontfamily=FONTS['family'],
                color=COLORS['text_secondary'])
    if x_low:
        xpos = right if axis_reversed else left
        ax.text(xpos, bottom - 0.02, x_low,
                ha='center', va='top',
                fontsize=FONTS['note_size'],
                fontfamily=FONTS['family'],
                color=COLORS['text_secondary'])
    if y_high:
        ypos = top
        ax.text(left - 0.03, ypos, y_high,
                ha='right', va='center',
                fontsize=FONTS['note_size'],
                fontfamily=FONTS['family'],
                color=COLORS['text_secondary'])
    if y_low:
        ypos = bottom
        ax.text(left - 0.03, ypos, y_low,
                ha='right', va='center',
                fontsize=FONTS['note_size'],
                fontfamily=FONTS['family'],
                color=COLORS['text_secondary'])

    # Center cross-lines
    ax.plot([mid_x, mid_x], [bottom, top],
            color=COLORS['white'], linewidth=2, zorder=1)
    ax.plot([left, right], [mid_y, mid_y],
            color=COLORS['white'], linewidth=2, zorder=1)

    # Outer border
    border = patches.FancyBboxPatch(
        (left, bottom), right - left, top - bottom,
        boxstyle='round,pad=0.005',
        facecolor='none',
        edgecolor=COLORS['border'],
        linewidth=FIGURE['border_width'],
        zorder=5
    )
    ax.add_patch(border)

    save_figure(fig, output_path)
