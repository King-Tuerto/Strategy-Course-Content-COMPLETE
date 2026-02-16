"""
Matrix Grid Renderer
=====================
Renders N×M grid matrices such as the IE Matrix (3×3),
SWOT (2×2 with headers), and similar grid-based frameworks.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from tools.graphics.config import COLORS, FONTS, FIGURE, REGION_COLORS, IE_COLORS
from tools.graphics.base import create_figure, save_figure, wrap_text, hide_axes


def render(figure_entry, data, output_path):
    """
    Render a grid matrix figure.

    data keys:
        rows:           int  – number of rows (default 3)
        cols:           int  – number of columns (default 3)
        x_label:        str  – X-axis label
        y_label:        str  – Y-axis label
        col_labels:     list of str – labels across top columns
        row_labels:     list of str – labels down left side rows
        cells:          list of dicts (row-major order, row 0 = top):
            row:        int  – row index (0 = top)
            col:        int  – column index (0 = left)
            label:      str  – cell text
            color:      str  – COLORS key or hex
            items:      list of str – bullet items (optional)
            region:     str  – 'grow', 'hold', 'harvest' for background fill
        x_scale:        list of str – scale labels under columns (optional)
        y_scale:        list of str – scale labels beside rows (optional)
        show_grid_lines: bool – show cell borders (default True)
        header_colors:  dict – 'col' and 'row' header background colors
        style:          str  – 'ie' for IE Matrix styling, 'swot' for SWOT, 'basic' (default)
    """
    fig, ax = create_figure(figure_entry['figure_number'], figure_entry['title'])
    hide_axes(ax)

    rows = data.get('rows', 3)
    cols = data.get('cols', 3)
    style = data.get('style', 'basic')

    # Layout bounds
    left = 0.15
    right = 0.95
    bottom = 0.10
    top_ = 0.88

    grid_w = right - left
    grid_h = top_ - bottom
    cell_w = grid_w / cols
    cell_h = grid_h / rows

    # Header area
    col_labels = data.get('col_labels', [])
    row_labels = data.get('row_labels', [])
    header_colors = data.get('header_colors', {})
    col_header_color = COLORS.get(header_colors.get('col', 'navy'), COLORS['navy'])
    row_header_color = COLORS.get(header_colors.get('row', 'steel_blue'), COLORS['steel_blue'])

    # Draw column headers
    if col_labels:
        for j, label in enumerate(col_labels[:cols]):
            hx = left + j * cell_w
            hy = top_
            hh = 0.05

            rect = patches.FancyBboxPatch(
                (hx, hy), cell_w, hh,
                boxstyle='round,pad=0.003',
                facecolor=col_header_color,
                edgecolor=COLORS['white'],
                linewidth=1,
                zorder=2
            )
            ax.add_patch(rect)
            ax.text(hx + cell_w / 2, hy + hh / 2, label,
                    ha='center', va='center',
                    fontsize=FONTS['note_size'],
                    fontweight='bold',
                    fontfamily=FONTS['family'],
                    color=COLORS['text_on_dark'],
                    zorder=3)

    # Draw row headers
    if row_labels:
        rw = 0.08
        for i, label in enumerate(row_labels[:rows]):
            ry = top_ - (i + 1) * cell_h
            rect = patches.FancyBboxPatch(
                (left - rw, ry), rw, cell_h,
                boxstyle='round,pad=0.003',
                facecolor=row_header_color,
                edgecolor=COLORS['white'],
                linewidth=1,
                zorder=2
            )
            ax.add_patch(rect)
            ax.text(left - rw / 2, ry + cell_h / 2,
                    wrap_text(label, 10),
                    ha='center', va='center',
                    fontsize=FONTS['note_size'],
                    fontweight='bold',
                    fontfamily=FONTS['family'],
                    color=COLORS['text_on_dark'],
                    rotation=0,
                    zorder=3)

    # Draw cells
    cells = data.get('cells', [])
    cell_lookup = {}
    for c in cells:
        cell_lookup[(c['row'], c['col'])] = c

    for i in range(rows):
        for j in range(cols):
            cx = left + j * cell_w
            cy = top_ - (i + 1) * cell_h

            cell = cell_lookup.get((i, j), {})

            # Background color
            region = cell.get('region', '')
            if region and region in REGION_COLORS:
                bg = REGION_COLORS[region]
            elif cell.get('color'):
                c_str = cell['color']
                bg = COLORS.get(c_str, c_str)
            else:
                bg = COLORS['white']

            rect = patches.Rectangle(
                (cx, cy), cell_w, cell_h,
                facecolor=bg,
                edgecolor=COLORS['border'] if data.get('show_grid_lines', True) else 'none',
                linewidth=1,
                zorder=1
            )
            ax.add_patch(rect)

            # Cell label
            label = cell.get('label', '')
            items = cell.get('items', [])

            if label:
                label_y = cy + cell_h * 0.7 if items else cy + cell_h / 2
                ax.text(cx + cell_w / 2, label_y,
                        wrap_text(label, 18),
                        ha='center', va='center',
                        fontsize=FONTS['body_size'],
                        fontweight='bold',
                        fontfamily=FONTS['family'],
                        color=COLORS['text'],
                        zorder=3)

            # Bullet items in cell
            if items:
                item_start = cy + cell_h * 0.5
                spacing = cell_h * 0.14
                for k, item in enumerate(items[:4]):
                    iy = item_start - k * spacing
                    ax.text(cx + cell_w * 0.15, iy,
                            f'• {item}',
                            ha='left', va='center',
                            fontsize=FONTS['note_size'],
                            fontfamily=FONTS['family'],
                            color=COLORS['text_secondary'],
                            zorder=3)

    # Scale labels
    x_scale = data.get('x_scale', [])
    y_scale = data.get('y_scale', [])

    for j, s in enumerate(x_scale[:cols]):
        sx = left + j * cell_w + cell_w / 2
        ax.text(sx, bottom - 0.03, s,
                ha='center', va='top',
                fontsize=FONTS['note_size'],
                fontfamily=FONTS['family'],
                color=COLORS['text_secondary'])

    for i, s in enumerate(y_scale[:rows]):
        sy = top_ - i * cell_h - cell_h / 2
        ax.text(left - 0.12, sy, s,
                ha='center', va='center',
                fontsize=FONTS['note_size'],
                fontfamily=FONTS['family'],
                color=COLORS['text_secondary'])

    # Axis labels
    x_label = data.get('x_label', '')
    y_label = data.get('y_label', '')

    if x_label:
        ax.text((left + right) / 2, bottom - 0.06, x_label,
                ha='center', va='top',
                fontsize=FONTS['axis_label_size'],
                fontweight='bold',
                fontfamily=FONTS['family'],
                color=COLORS['text'])

    if y_label:
        ax.text(left - 0.12 - (0.04 if row_labels else 0), (bottom + top_) / 2,
                y_label,
                ha='center', va='center',
                fontsize=FONTS['axis_label_size'],
                fontweight='bold',
                fontfamily=FONTS['family'],
                color=COLORS['text'],
                rotation=90)

    # Outer border
    border = patches.Rectangle(
        (left, bottom), grid_w, grid_h,
        facecolor='none',
        edgecolor=COLORS['border'],
        linewidth=FIGURE['border_width'],
        zorder=5
    )
    ax.add_patch(border)

    save_figure(fig, output_path)
