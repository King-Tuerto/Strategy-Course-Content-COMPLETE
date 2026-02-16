"""
Hierarchy Renderer
===================
Renders pyramids, organizational trees, and tiered hierarchy diagrams.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from tools.graphics.config import COLORS, FONTS, FIGURE
from tools.graphics.base import create_figure, save_figure, wrap_text, draw_rounded_box, draw_arrow, hide_axes


def render(figure_entry, data, output_path):
    """
    Render a hierarchy figure.

    data keys:
        style:          str  – 'pyramid', 'tree', or 'tiers' (default 'pyramid')

        For 'pyramid':
            levels:     list of dicts (top to bottom):
                label:  str  – level text
                color:  str  – COLORS key or hex
                items:  list of str – annotation bullets (optional)
            annotation_side: str – 'right' (default), 'left', or 'both'

        For 'tree':
            nodes:      list of dicts:
                id:     str  – unique identifier
                label:  str  – display text
                color:  str  – COLORS key or hex
                parent: str  – parent node id (None for root)
                level:  int  – depth level (0 = root)
            spacing:    float – horizontal spread factor (default 1.0)

        For 'tiers':
            tiers:      list of dicts (top to bottom):
                label:  str  – tier header
                color:  str  – COLORS key or hex
                items:  list of str – items within tier
                columns: int  – number of columns for items (default 1)
    """
    style = data.get('style', 'pyramid')

    if style == 'pyramid':
        _render_pyramid(figure_entry, data, output_path)
    elif style == 'tree':
        _render_tree(figure_entry, data, output_path)
    elif style == 'tiers':
        _render_tiers(figure_entry, data, output_path)
    else:
        _render_pyramid(figure_entry, data, output_path)


def _render_pyramid(figure_entry, data, output_path):
    """Render a pyramid/triangle hierarchy."""
    fig, ax = create_figure(figure_entry['figure_number'], figure_entry['title'])
    hide_axes(ax)

    levels = data.get('levels', [])
    n = len(levels)
    if n == 0:
        save_figure(fig, output_path)
        return

    # Pyramid geometry
    px_center = 0.45  # shift left to make room for annotations
    py_bottom = 0.05
    py_top = 0.95
    max_width = 0.55
    min_width = 0.12

    tier_height = (py_top - py_bottom) / n

    annotation_side = data.get('annotation_side', 'right')

    for i, level in enumerate(levels):
        # i=0 is the top (narrowest)
        y_top_tier = py_top - i * tier_height
        y_bot_tier = y_top_tier - tier_height

        # Width interpolation: narrow at top, wide at bottom
        frac_top = i / n
        frac_bot = (i + 1) / n
        w_top = min_width + (max_width - min_width) * frac_top
        w_bot = min_width + (max_width - min_width) * frac_bot

        # Trapezoid vertices
        x_tl = px_center - w_top / 2
        x_tr = px_center + w_top / 2
        x_bl = px_center - w_bot / 2
        x_br = px_center + w_bot / 2

        color = COLORS.get(level.get('color', 'navy'), level.get('color', COLORS['navy']))

        trap = plt.Polygon(
            [(x_tl, y_top_tier), (x_tr, y_top_tier),
             (x_br, y_bot_tier), (x_bl, y_bot_tier)],
            facecolor=color,
            edgecolor=COLORS['white'],
            linewidth=2,
            zorder=2
        )
        ax.add_patch(trap)

        # Label
        cy = (y_top_tier + y_bot_tier) / 2
        rgb = tuple(int(color.lstrip('#')[i2:i2+2], 16) for i2 in (0, 2, 4))
        brightness = (rgb[0] * 299 + rgb[1] * 587 + rgb[2] * 114) / 1000
        tc = COLORS['text_on_dark'] if brightness < 128 else COLORS['text']

        ax.text(px_center, cy, wrap_text(level.get('label', ''), 20),
                ha='center', va='center',
                fontsize=FONTS['body_size'],
                fontweight='bold',
                fontfamily=FONTS['family'],
                color=tc,
                zorder=3)

        # Annotation items
        items = level.get('items', [])
        if items:
            if annotation_side in ('right', 'both'):
                ann_x = px_center + w_bot / 2 + 0.08
                for j, item in enumerate(items[:4]):
                    iy = cy + 0.02 - j * 0.04
                    ax.text(ann_x, iy, f'• {item}',
                            ha='left', va='center',
                            fontsize=FONTS['note_size'],
                            fontfamily=FONTS['family'],
                            color=COLORS['text_secondary'],
                            zorder=3)
                # Connector line
                ax.plot([px_center + (w_top + w_bot) / 4, ann_x - 0.02],
                        [cy, cy],
                        color=COLORS['border'], linewidth=0.8,
                        linestyle='--', zorder=1)

            if annotation_side in ('left', 'both'):
                ann_x = px_center - w_bot / 2 - 0.08
                for j, item in enumerate(items[:4]):
                    iy = cy + 0.02 - j * 0.04
                    ax.text(ann_x, iy, f'• {item}',
                            ha='right', va='center',
                            fontsize=FONTS['note_size'],
                            fontfamily=FONTS['family'],
                            color=COLORS['text_secondary'],
                            zorder=3)
                ax.plot([px_center - (w_top + w_bot) / 4, ann_x + 0.02],
                        [cy, cy],
                        color=COLORS['border'], linewidth=0.8,
                        linestyle='--', zorder=1)

    save_figure(fig, output_path)


def _render_tree(figure_entry, data, output_path):
    """Render a tree hierarchy (org chart style)."""
    fig, ax = create_figure(figure_entry['figure_number'], figure_entry['title'])
    hide_axes(ax)

    nodes = data.get('nodes', [])
    if not nodes:
        save_figure(fig, output_path)
        return

    spacing = data.get('spacing', 1.0)

    # Build tree structure
    children = {}
    node_map = {}
    for n in nodes:
        node_map[n['id']] = n
        parent = n.get('parent')
        if parent:
            children.setdefault(parent, []).append(n['id'])

    # Find root(s)
    roots = [n['id'] for n in nodes if not n.get('parent')]

    # Calculate positions using BFS
    max_level = max(n.get('level', 0) for n in nodes)
    positions = {}

    # Count nodes at each level
    level_counts = {}
    for n in nodes:
        lv = n.get('level', 0)
        level_counts[lv] = level_counts.get(lv, 0) + 1

    # Assign x positions by level
    level_indices = {}
    for n in nodes:
        lv = n.get('level', 0)
        idx = level_indices.get(lv, 0)
        level_indices[lv] = idx + 1
        count = level_counts[lv]
        x = (idx + 0.5) / count
        y = 1.0 - (lv + 0.5) / (max_level + 1) * 0.85 - 0.05
        positions[n['id']] = (x, y)

    # Node dimensions
    node_w = min(0.18, 0.7 / max(level_counts.values())) * spacing
    node_h = 0.06

    # Draw connections first
    for n in nodes:
        parent = n.get('parent')
        if parent and parent in positions:
            px, py = positions[parent]
            cx, cy = positions[n['id']]
            # Elbow connector
            mid_y = (py - node_h / 2 + cy + node_h / 2) / 2
            ax.plot([px, px], [py - node_h / 2, mid_y],
                    color=COLORS['steel_blue'], linewidth=1.5, zorder=1)
            ax.plot([px, cx], [mid_y, mid_y],
                    color=COLORS['steel_blue'], linewidth=1.5, zorder=1)
            ax.plot([cx, cx], [mid_y, cy + node_h / 2],
                    color=COLORS['steel_blue'], linewidth=1.5, zorder=1)

    # Draw nodes
    for n in nodes:
        x, y = positions[n['id']]
        color = n.get('color', 'navy')
        draw_rounded_box(ax, x - node_w / 2, y - node_h / 2,
                         node_w, node_h,
                         n.get('label', ''),
                         color=color,
                         fontsize=FONTS['note_size'],
                         text_wrap=16)

    save_figure(fig, output_path)


def _render_tiers(figure_entry, data, output_path):
    """Render horizontal tiers with items."""
    fig, ax = create_figure(figure_entry['figure_number'], figure_entry['title'])
    hide_axes(ax)

    tiers = data.get('tiers', [])
    n = len(tiers)
    if n == 0:
        save_figure(fig, output_path)
        return

    margin = 0.05
    tier_h = (1.0 - 2 * margin) / n
    gap = 0.01

    for i, tier in enumerate(tiers):
        y = 1.0 - margin - (i + 1) * tier_h + gap / 2
        color = COLORS.get(tier.get('color', 'navy'), tier.get('color', COLORS['navy']))

        # Header strip
        header_w = 0.22
        rect = patches.FancyBboxPatch(
            (margin, y), header_w, tier_h - gap,
            boxstyle='round,pad=0.005',
            facecolor=color,
            edgecolor=COLORS['white'],
            linewidth=1.5,
            zorder=2
        )
        ax.add_patch(rect)

        rgb = tuple(int(color.lstrip('#')[j:j+2], 16) for j in (0, 2, 4))
        brightness = (rgb[0] * 299 + rgb[1] * 587 + rgb[2] * 114) / 1000
        tc = COLORS['text_on_dark'] if brightness < 128 else COLORS['text']

        ax.text(margin + header_w / 2, y + (tier_h - gap) / 2,
                wrap_text(tier.get('label', ''), 14),
                ha='center', va='center',
                fontsize=FONTS['body_size'],
                fontweight='bold',
                fontfamily=FONTS['family'],
                color=tc,
                zorder=3)

        # Content area
        items = tier.get('items', [])
        columns = tier.get('columns', 1)
        content_x = margin + header_w + 0.03
        content_w = 1.0 - margin - content_x

        # Content background
        content_rect = patches.FancyBboxPatch(
            (content_x, y), content_w, tier_h - gap,
            boxstyle='round,pad=0.005',
            facecolor=COLORS['white'],
            edgecolor=COLORS['border'],
            linewidth=0.8,
            zorder=1
        )
        ax.add_patch(content_rect)

        # Layout items in columns
        col_w = content_w / columns
        for k, item in enumerate(items):
            col = k % columns
            row = k // columns
            max_rows = max(1, len(items) // columns + (1 if len(items) % columns else 0))
            item_h = (tier_h - gap) / (max_rows + 0.5)

            ix = content_x + col * col_w + 0.02
            iy = y + (tier_h - gap) - (row + 1) * item_h

            ax.text(ix, iy + item_h * 0.3, f'• {item}',
                    ha='left', va='center',
                    fontsize=FONTS['note_size'],
                    fontfamily=FONTS['family'],
                    color=COLORS['text'],
                    zorder=3)

    save_figure(fig, output_path)
