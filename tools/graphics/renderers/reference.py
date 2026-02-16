"""
Reference Renderer
===================
Renders category graphics, hexagonal layouts, balanced scorecards,
Five Forces diagrams, and other specialized reference figures.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from tools.graphics.config import COLORS, FONTS, FIGURE
from tools.graphics.base import create_figure, save_figure, wrap_text, draw_rounded_box, draw_arrow, hide_axes


def render(figure_entry, data, output_path):
    """
    Render a reference figure.

    data keys:
        style:          str  – 'five_forces', 'balanced_scorecard', 'hexagon',
                               'category_grid', 'radial', 'cycle'

        For 'five_forces':
            center:     dict – center box {label, color, items}
            forces:     list of 4 dicts (top, right, bottom, left):
                label:  str
                color:  str
                items:  list of str

        For 'balanced_scorecard':
            perspectives: list of 4 dicts:
                name:   str  – perspective name
                color:  str
                measures: list of str – KPI measures
            center:     dict – {label, color} for center vision box

        For 'hexagon':
            hexagons:   list of dicts:
                label:  str
                color:  str
                items:  list of str (optional)
            center:     dict – {label, color} for center hex

        For 'category_grid':
            categories: list of dicts:
                header: str
                color:  str
                items:  list of str
            columns:    int (default 2)

        For 'radial':
            center:     dict – {label, color}
            spokes:     list of dicts:
                label:  str
                color:  str
                items:  list of str (optional)

        For 'cycle':
            stages:     list of dicts:
                label:  str
                color:  str
                sublabel: str (optional)
    """
    style = data.get('style', 'category_grid')

    dispatch = {
        'five_forces': _render_five_forces,
        'balanced_scorecard': _render_balanced_scorecard,
        'hexagon': _render_hexagon,
        'category_grid': _render_category_grid,
        'radial': _render_radial,
        'cycle': _render_cycle,
    }

    renderer = dispatch.get(style, _render_category_grid)
    renderer(figure_entry, data, output_path)


def _render_five_forces(figure_entry, data, output_path):
    """Render Porter's Five Forces diagram."""
    fig, ax = create_figure(figure_entry['figure_number'], figure_entry['title'])
    hide_axes(ax)

    center = data.get('center', {'label': 'Industry\nRivalry', 'color': 'navy'})
    forces = data.get('forces', [])

    # Center box
    cw, ch = 0.28, 0.18
    cx, cy = 0.5 - cw / 2, 0.5 - ch / 2
    center_color = center.get('color', 'navy')
    draw_rounded_box(ax, cx, cy, cw, ch,
                     center.get('label', ''),
                     color=center_color,
                     fontsize=FONTS['cell_label_size'])

    # Center items
    center_items = center.get('items', [])
    for j, item in enumerate(center_items[:3]):
        ax.text(0.5, 0.5 - ch / 2 - 0.04 - j * 0.035,
                f'• {item}',
                ha='center', va='top',
                fontsize=6,
                fontfamily=FONTS['family'],
                color=COLORS['text_secondary'])

    # Force positions: top, right, bottom, left
    force_positions = [
        {'cx': 0.5, 'cy': 0.88, 'arrow_to': (0.5, 0.5 + ch / 2)},        # top
        {'cx': 0.85, 'cy': 0.5, 'arrow_to': (0.5 + cw / 2, 0.5)},         # right
        {'cx': 0.5, 'cy': 0.12, 'arrow_to': (0.5, 0.5 - ch / 2)},         # bottom
        {'cx': 0.15, 'cy': 0.5, 'arrow_to': (0.5 - cw / 2, 0.5)},         # left
    ]

    fw, fh = 0.22, 0.12

    for i, force in enumerate(forces[:4]):
        fp = force_positions[i]
        fx = fp['cx'] - fw / 2
        fy = fp['cy'] - fh / 2
        f_color = force.get('color', 'steel_blue')

        draw_rounded_box(ax, fx, fy, fw, fh,
                         force.get('label', ''),
                         color=f_color,
                         fontsize=FONTS['body_size'])

        # Arrow from force to center
        arrow_from_x = fp['cx']
        arrow_from_y = fp['cy']

        # Adjust arrow start to box edge
        if i == 0:  # top
            arrow_from_y = fp['cy'] - fh / 2
        elif i == 1:  # right
            arrow_from_x = fp['cx'] - fw / 2
        elif i == 2:  # bottom
            arrow_from_y = fp['cy'] + fh / 2
        elif i == 3:  # left
            arrow_from_x = fp['cx'] + fw / 2

        draw_arrow(ax, arrow_from_x, arrow_from_y,
                   fp['arrow_to'][0], fp['arrow_to'][1],
                   color='orange', linewidth=2)

        # Force items
        items = force.get('items', [])
        for j, item in enumerate(items[:3]):
            if i == 0:  # top - items to right
                ix, iy = fp['cx'] + fw / 2 + 0.02, fp['cy'] - 0.01 - j * 0.03
                ha = 'left'
            elif i == 2:  # bottom - items to right
                ix, iy = fp['cx'] + fw / 2 + 0.02, fp['cy'] + 0.01 - j * 0.03
                ha = 'left'
            elif i == 1:  # right - items below
                ix, iy = fp['cx'], fp['cy'] - fh / 2 - 0.03 - j * 0.03
                ha = 'center'
            else:  # left - items below
                ix, iy = fp['cx'], fp['cy'] - fh / 2 - 0.03 - j * 0.03
                ha = 'center'

            ax.text(ix, iy, f'• {item}',
                    ha=ha, va='center',
                    fontsize=6,
                    fontfamily=FONTS['family'],
                    color=COLORS['text_secondary'])

    save_figure(fig, output_path)


def _render_balanced_scorecard(figure_entry, data, output_path):
    """Render Balanced Scorecard with four perspectives."""
    fig, ax = create_figure(figure_entry['figure_number'], figure_entry['title'])
    hide_axes(ax)

    perspectives = data.get('perspectives', [])
    center = data.get('center', {'label': 'Vision &\nStrategy', 'color': 'navy'})

    # Center circle
    center_color = COLORS.get(center.get('color', 'navy'), COLORS['navy'])
    circle = patches.Circle(
        (0.5, 0.5), 0.10,
        facecolor=center_color,
        edgecolor=COLORS['white'],
        linewidth=2,
        zorder=4
    )
    ax.add_patch(circle)

    rgb = tuple(int(center_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    brightness = (rgb[0] * 299 + rgb[1] * 587 + rgb[2] * 114) / 1000
    tc = COLORS['text_on_dark'] if brightness < 128 else COLORS['text']

    ax.text(0.5, 0.5, wrap_text(center.get('label', ''), 12),
            ha='center', va='center',
            fontsize=FONTS['body_size'],
            fontweight='bold',
            fontfamily=FONTS['family'],
            color=tc,
            zorder=5)

    # Perspective positions: top, right, bottom, left
    persp_positions = [
        {'cx': 0.5, 'cy': 0.85, 'w': 0.35, 'h': 0.14},   # top
        {'cx': 0.82, 'cy': 0.5, 'w': 0.28, 'h': 0.20},    # right
        {'cx': 0.5, 'cy': 0.15, 'w': 0.35, 'h': 0.14},    # bottom
        {'cx': 0.18, 'cy': 0.5, 'w': 0.28, 'h': 0.20},    # left
    ]

    for i, persp in enumerate(perspectives[:4]):
        pp = persp_positions[i]
        p_color = COLORS.get(persp.get('color', 'steel_blue'),
                             persp.get('color', COLORS['steel_blue']))

        # Header box
        hh = 0.05
        hx = pp['cx'] - pp['w'] / 2
        hy = pp['cy'] + pp['h'] / 2 - hh

        header = patches.FancyBboxPatch(
            (hx, hy), pp['w'], hh,
            boxstyle='round,pad=0.005',
            facecolor=p_color,
            edgecolor='none',
            zorder=2
        )
        ax.add_patch(header)

        p_rgb = tuple(int(p_color.lstrip('#')[j:j+2], 16) for j in (0, 2, 4))
        p_bright = (p_rgb[0] * 299 + p_rgb[1] * 587 + p_rgb[2] * 114) / 1000
        p_tc = COLORS['text_on_dark'] if p_bright < 128 else COLORS['text']

        ax.text(pp['cx'], hy + hh / 2,
                persp.get('name', ''),
                ha='center', va='center',
                fontsize=FONTS['body_size'],
                fontweight='bold',
                fontfamily=FONTS['family'],
                color=p_tc,
                zorder=3)

        # Content box
        content_h = pp['h'] - hh - 0.01
        content = patches.FancyBboxPatch(
            (hx, pp['cy'] - pp['h'] / 2), pp['w'], content_h,
            boxstyle='round,pad=0.005',
            facecolor=COLORS['white'],
            edgecolor=COLORS['border'],
            linewidth=1,
            zorder=1
        )
        ax.add_patch(content)

        # Measures
        measures = persp.get('measures', [])
        measure_spacing = min(0.035, content_h / max(len(measures) + 0.5, 1))
        for j, m in enumerate(measures[:5]):
            my = pp['cy'] - pp['h'] / 2 + content_h - 0.02 - j * measure_spacing
            ax.text(hx + 0.02, my, f'• {m}',
                    ha='left', va='top',
                    fontsize=6,
                    fontfamily=FONTS['family'],
                    color=COLORS['text'],
                    zorder=3)

        # Arrow from perspective to center
        dx = 0.5 - pp['cx']
        dy = 0.5 - pp['cy']
        dist = (dx**2 + dy**2)**0.5
        if dist > 0:
            # Start from box edge
            start_x = pp['cx'] + dx * (0.12 / dist) * (pp['w'] / 0.3)
            start_y = pp['cy'] + dy * (0.12 / dist) * (pp['h'] / 0.18)
            end_x = 0.5 - dx * (0.10 / dist)
            end_y = 0.5 - dy * (0.10 / dist)
            draw_arrow(ax, start_x, start_y, end_x, end_y,
                       color='steel_blue', style='<->', linewidth=1.5)

    save_figure(fig, output_path)


def _render_hexagon(figure_entry, data, output_path):
    """Render hexagonal layout (e.g., PESTEL factors)."""
    fig, ax = create_figure(figure_entry['figure_number'], figure_entry['title'])
    hide_axes(ax)

    hexagons = data.get('hexagons', [])
    center = data.get('center')

    # Center hex
    if center:
        _draw_hex(ax, 0.5, 0.5, 0.10,
                  center.get('label', ''),
                  COLORS.get(center.get('color', 'navy'), COLORS['navy']),
                  fontsize=FONTS['body_size'])

    # Surrounding hexagons
    n = len(hexagons)
    radius = 0.28
    for i, h in enumerate(hexagons):
        angle = 2 * np.pi * i / n - np.pi / 2  # start from top
        hx = 0.5 + radius * np.cos(angle)
        hy = 0.5 + radius * np.sin(angle) * 0.85  # scale for aspect ratio

        color = COLORS.get(h.get('color', 'steel_blue'),
                           h.get('color', COLORS['steel_blue']))
        _draw_hex(ax, hx, hy, 0.09, h.get('label', ''), color)

        # Connector to center
        if center:
            draw_arrow(ax,
                       0.5 + 0.12 * np.cos(angle),
                       0.5 + 0.12 * np.sin(angle) * 0.85,
                       hx - 0.08 * np.cos(angle),
                       hy - 0.08 * np.sin(angle) * 0.85,
                       color='border', style='-', linewidth=1)

        # Items
        items = h.get('items', [])
        for j, item in enumerate(items[:3]):
            # Place items outside the hex
            item_angle = angle
            item_r = radius + 0.14 + j * 0.03
            ix = 0.5 + item_r * np.cos(item_angle)
            iy = 0.5 + item_r * np.sin(item_angle) * 0.85
            ha = 'left' if np.cos(angle) > 0.1 else 'right' if np.cos(angle) < -0.1 else 'center'
            ax.text(ix, iy, f'• {item}',
                    ha=ha, va='center',
                    fontsize=6,
                    fontfamily=FONTS['family'],
                    color=COLORS['text_secondary'])

    save_figure(fig, output_path)


def _draw_hex(ax, cx, cy, size, label, color, fontsize=None):
    """Draw a single hexagon."""
    angles = np.linspace(0, 2 * np.pi, 7)[:-1] + np.pi / 6
    xs = cx + size * np.cos(angles)
    ys = cy + size * np.sin(angles) * 0.85

    hex_patch = plt.Polygon(
        list(zip(xs, ys)),
        facecolor=color,
        edgecolor=COLORS['white'],
        linewidth=2,
        zorder=2
    )
    ax.add_patch(hex_patch)

    rgb = tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    brightness = (rgb[0] * 299 + rgb[1] * 587 + rgb[2] * 114) / 1000
    tc = COLORS['text_on_dark'] if brightness < 128 else COLORS['text']

    fs = fontsize or FONTS['note_size']
    ax.text(cx, cy, wrap_text(label, 10),
            ha='center', va='center',
            fontsize=fs, fontweight='bold',
            fontfamily=FONTS['family'],
            color=tc, zorder=3)


def _render_category_grid(figure_entry, data, output_path):
    """Render a grid of category cards."""
    fig, ax = create_figure(figure_entry['figure_number'], figure_entry['title'])
    hide_axes(ax)

    categories = data.get('categories', [])
    n_cols = data.get('columns', 2)
    n = len(categories)
    n_rows = (n + n_cols - 1) // n_cols

    margin = 0.05
    gap = 0.03
    card_w = (1.0 - 2 * margin - gap * (n_cols - 1)) / n_cols
    card_h = (1.0 - 2 * margin - gap * (n_rows - 1)) / n_rows
    header_h = min(0.06, card_h * 0.25)

    for i, cat in enumerate(categories):
        row = i // n_cols
        col = i % n_cols
        x = margin + col * (card_w + gap)
        y = 1.0 - margin - (row + 1) * (card_h + gap) + gap

        color = COLORS.get(cat.get('color', 'navy'), cat.get('color', COLORS['navy']))

        # Header
        h_rect = patches.FancyBboxPatch(
            (x, y + card_h - header_h), card_w, header_h,
            boxstyle='round,pad=0.005',
            facecolor=color,
            edgecolor='none',
            zorder=2
        )
        ax.add_patch(h_rect)

        rgb = tuple(int(color.lstrip('#')[j:j+2], 16) for j in (0, 2, 4))
        brightness = (rgb[0] * 299 + rgb[1] * 587 + rgb[2] * 114) / 1000
        tc = COLORS['text_on_dark'] if brightness < 128 else COLORS['text']

        ax.text(x + card_w / 2, y + card_h - header_h / 2,
                cat.get('header', ''),
                ha='center', va='center',
                fontsize=FONTS['body_size'],
                fontweight='bold',
                fontfamily=FONTS['family'],
                color=tc,
                zorder=3)

        # Content area
        content_rect = patches.FancyBboxPatch(
            (x, y), card_w, card_h - header_h - 0.005,
            boxstyle='round,pad=0.005',
            facecolor=COLORS['white'],
            edgecolor=COLORS['border'],
            linewidth=0.8,
            zorder=1
        )
        ax.add_patch(content_rect)

        # Items
        items = cat.get('items', [])
        content_avail = card_h - header_h - 0.02
        item_spacing = min(0.035, content_avail / max(len(items), 1))
        for j, item in enumerate(items):
            iy = y + card_h - header_h - 0.02 - j * item_spacing
            ax.text(x + 0.015, iy, f'• {wrap_text(item, 24)}',
                    ha='left', va='top',
                    fontsize=6,
                    fontfamily=FONTS['family'],
                    color=COLORS['text'],
                    zorder=3)

    save_figure(fig, output_path)


def _render_radial(figure_entry, data, output_path):
    """Render a radial/spoke diagram."""
    fig, ax = create_figure(figure_entry['figure_number'], figure_entry['title'])
    hide_axes(ax)

    center = data.get('center', {'label': 'Center', 'color': 'navy'})
    spokes = data.get('spokes', [])
    n = len(spokes)

    # Center box
    cw, ch = 0.20, 0.12
    center_color = center.get('color', 'navy')
    draw_rounded_box(ax, 0.5 - cw / 2, 0.5 - ch / 2, cw, ch,
                     center.get('label', ''),
                     color=center_color,
                     fontsize=FONTS['cell_label_size'])

    # Spokes
    radius = 0.32
    spoke_w, spoke_h = 0.18, 0.08

    for i, spoke in enumerate(spokes):
        angle = 2 * np.pi * i / n - np.pi / 2
        sx = 0.5 + radius * np.cos(angle)
        sy = 0.5 + radius * np.sin(angle) * 0.85

        color = spoke.get('color', 'steel_blue')
        draw_rounded_box(ax, sx - spoke_w / 2, sy - spoke_h / 2,
                         spoke_w, spoke_h,
                         spoke.get('label', ''),
                         color=color,
                         fontsize=FONTS['note_size'],
                         text_wrap=14)

        # Connector
        inner_x = 0.5 + 0.11 * np.cos(angle)
        inner_y = 0.5 + 0.11 * np.sin(angle) * 0.85
        outer_x = sx - 0.09 * np.cos(angle)
        outer_y = sy - 0.09 * np.sin(angle) * 0.85
        draw_arrow(ax, inner_x, inner_y, outer_x, outer_y,
                   color='steel_blue', linewidth=1.5)

        # Items
        items = spoke.get('items', [])
        for j, item in enumerate(items[:3]):
            ext_r = radius + 0.10 + j * 0.035
            ix = 0.5 + ext_r * np.cos(angle)
            iy = 0.5 + ext_r * np.sin(angle) * 0.85
            ha = 'left' if np.cos(angle) > 0.1 else 'right' if np.cos(angle) < -0.1 else 'center'
            ax.text(ix, iy, f'• {item}',
                    ha=ha, va='center',
                    fontsize=6,
                    fontfamily=FONTS['family'],
                    color=COLORS['text_secondary'])

    save_figure(fig, output_path)


def _render_cycle(figure_entry, data, output_path):
    """Render a circular cycle diagram."""
    fig, ax = create_figure(figure_entry['figure_number'], figure_entry['title'])
    hide_axes(ax)

    stages = data.get('stages', [])
    n = len(stages)
    if n == 0:
        save_figure(fig, output_path)
        return

    radius = 0.30
    box_w, box_h = 0.16, 0.08

    for i, stage in enumerate(stages):
        angle = 2 * np.pi * i / n - np.pi / 2
        sx = 0.5 + radius * np.cos(angle)
        sy = 0.5 + radius * np.sin(angle) * 0.85

        color = stage.get('color', 'navy')
        draw_rounded_box(ax, sx - box_w / 2, sy - box_h / 2,
                         box_w, box_h,
                         stage.get('label', ''),
                         color=color,
                         fontsize=FONTS['note_size'],
                         text_wrap=14)

        # Sublabel
        sublabel = stage.get('sublabel', '')
        if sublabel:
            ax.text(sx, sy - box_h / 2 - 0.03,
                    wrap_text(sublabel, 18),
                    ha='center', va='top',
                    fontsize=6,
                    fontfamily=FONTS['family'],
                    color=COLORS['text_secondary'])

        # Arrow to next stage
        next_i = (i + 1) % n
        next_angle = 2 * np.pi * next_i / n - np.pi / 2

        # Arrow start/end on box edges
        mid_angle = (angle + next_angle) / 2
        if next_angle < angle:
            mid_angle += np.pi

        a_start_x = sx + box_w / 2 * np.cos(mid_angle - angle + np.pi / 2)
        a_start_y = sy + box_h / 2 * np.sin(mid_angle - angle + np.pi / 2) * 0.85

        next_sx = 0.5 + radius * np.cos(next_angle)
        next_sy = 0.5 + radius * np.sin(next_angle) * 0.85

        # Simplified: draw arc-like arrow between stages
        ctrl_x = 0.5 + (radius * 0.6) * np.cos((angle + next_angle) / 2 + (np.pi if next_angle < angle else 0))
        ctrl_y = 0.5 + (radius * 0.6) * np.sin((angle + next_angle) / 2 + (np.pi if next_angle < angle else 0)) * 0.85

        draw_arrow(ax,
                   sx + 0.09 * np.cos(mid_angle),
                   sy + 0.09 * np.sin(mid_angle) * 0.85,
                   next_sx - 0.09 * np.cos(mid_angle),
                   next_sy - 0.09 * np.sin(mid_angle) * 0.85,
                   color='steel_blue', linewidth=1.5)

    save_figure(fig, output_path)
