"""
Comparison Renderer
====================
Renders side-by-side comparison infographics, versus layouts,
and multi-column feature comparisons.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from tools.graphics.config import COLORS, FONTS, FIGURE
from tools.graphics.base import create_figure, save_figure, wrap_text, hide_axes


def render(figure_entry, data, output_path):
    """
    Render a comparison figure.

    data keys:
        style:          str  – 'side_by_side' (default), 'table', 'versus'
        columns:        list of dicts:
            header:     str  – column header
            color:      str  – header color (COLORS key or hex)
            items:      list of str – content items
        center_label:   str  – center divider label (optional, e.g., "VS")
        categories:     list of str – row category labels (for 'table' style)
        rows:           list of dicts (for 'table' style):
            category:   str  – row label
            values:     list of str – one value per column
        footer:         str  – footer text (optional)
    """
    style = data.get('style', 'side_by_side')

    if style == 'table':
        _render_table(figure_entry, data, output_path)
    elif style == 'versus':
        _render_versus(figure_entry, data, output_path)
    else:
        _render_side_by_side(figure_entry, data, output_path)


def _render_side_by_side(figure_entry, data, output_path):
    """Render side-by-side comparison columns."""
    fig, ax = create_figure(figure_entry['figure_number'], figure_entry['title'])
    hide_axes(ax)

    columns = data.get('columns', [])
    n = len(columns)
    if n == 0:
        save_figure(fig, output_path)
        return

    margin = 0.05
    gap = 0.03
    total_gap = gap * (n - 1)
    col_w = (1.0 - 2 * margin - total_gap) / n
    header_h = 0.08
    content_top = 0.92 - header_h

    center_label = data.get('center_label', '')

    for i, col in enumerate(columns):
        x = margin + i * (col_w + gap)
        color = COLORS.get(col.get('color', 'navy'), col.get('color', COLORS['navy']))

        # Header
        header = patches.FancyBboxPatch(
            (x, content_top + 0.01), col_w, header_h,
            boxstyle='round,pad=0.008',
            facecolor=color,
            edgecolor=COLORS['white'],
            linewidth=1.5,
            zorder=2
        )
        ax.add_patch(header)

        rgb = tuple(int(color.lstrip('#')[j:j+2], 16) for j in (0, 2, 4))
        brightness = (rgb[0] * 299 + rgb[1] * 587 + rgb[2] * 114) / 1000
        tc = COLORS['text_on_dark'] if brightness < 128 else COLORS['text']

        ax.text(x + col_w / 2, content_top + 0.01 + header_h / 2,
                col.get('header', ''),
                ha='center', va='center',
                fontsize=FONTS['cell_label_size'],
                fontweight='bold',
                fontfamily=FONTS['family'],
                color=tc,
                zorder=3)

        # Content area
        content_rect = patches.FancyBboxPatch(
            (x, margin), col_w, content_top - margin,
            boxstyle='round,pad=0.005',
            facecolor=COLORS['white'],
            edgecolor=COLORS['border'],
            linewidth=1,
            zorder=1
        )
        ax.add_patch(content_rect)

        # Items
        items = col.get('items', [])
        item_spacing = min(0.055, (content_top - margin - 0.04) / max(len(items), 1))
        for j, item in enumerate(items):
            iy = content_top - 0.03 - j * item_spacing
            ax.text(x + 0.02, iy, f'• {wrap_text(item, 28)}',
                    ha='left', va='top',
                    fontsize=FONTS['note_size'],
                    fontfamily=FONTS['family'],
                    color=COLORS['text'],
                    zorder=3)

    # Center divider label
    if center_label and n == 2:
        cx = margin + col_w + gap / 2
        cy = (content_top + margin) / 2
        ax.text(cx, cy, center_label,
                ha='center', va='center',
                fontsize=FONTS['axis_label_size'] + 2,
                fontweight='bold',
                fontfamily=FONTS['family'],
                color=COLORS['orange'],
                zorder=5)

    # Footer
    footer = data.get('footer', '')
    if footer:
        ax.text(0.5, 0.01, footer,
                ha='center', va='bottom',
                fontsize=FONTS['note_size'],
                fontstyle='italic',
                fontfamily=FONTS['family'],
                color=COLORS['text_secondary'])

    save_figure(fig, output_path)


def _render_versus(figure_entry, data, output_path):
    """Render a versus-style comparison with central divider."""
    fig, ax = create_figure(figure_entry['figure_number'], figure_entry['title'])
    hide_axes(ax)

    columns = data.get('columns', [])
    if len(columns) < 2:
        save_figure(fig, output_path)
        return

    left_col = columns[0]
    right_col = columns[1]

    margin = 0.05
    mid = 0.5
    col_w = mid - margin - 0.04

    for side, col, x_start in [('left', left_col, margin),
                                ('right', right_col, mid + 0.04)]:
        color = COLORS.get(col.get('color', 'navy'), col.get('color', COLORS['navy']))

        # Full column background
        bg = patches.FancyBboxPatch(
            (x_start, margin), col_w, 0.88,
            boxstyle='round,pad=0.008',
            facecolor=color,
            alpha=0.08,
            edgecolor=COLORS['border'],
            linewidth=1,
            zorder=0
        )
        ax.add_patch(bg)

        # Header
        header = patches.FancyBboxPatch(
            (x_start, 0.85), col_w, 0.08,
            boxstyle='round,pad=0.008',
            facecolor=color,
            edgecolor='none',
            linewidth=0,
            zorder=2
        )
        ax.add_patch(header)

        rgb = tuple(int(color.lstrip('#')[j:j+2], 16) for j in (0, 2, 4))
        brightness = (rgb[0] * 299 + rgb[1] * 587 + rgb[2] * 114) / 1000
        tc = COLORS['text_on_dark'] if brightness < 128 else COLORS['text']

        ax.text(x_start + col_w / 2, 0.89,
                col.get('header', ''),
                ha='center', va='center',
                fontsize=FONTS['cell_label_size'],
                fontweight='bold',
                fontfamily=FONTS['family'],
                color=tc,
                zorder=3)

        # Items
        items = col.get('items', [])
        item_spacing = min(0.055, 0.75 / max(len(items), 1))
        for j, item in enumerate(items):
            iy = 0.82 - j * item_spacing
            ax.text(x_start + 0.02, iy, f'• {wrap_text(item, 26)}',
                    ha='left', va='top',
                    fontsize=FONTS['note_size'],
                    fontfamily=FONTS['family'],
                    color=COLORS['text'],
                    zorder=3)

    # VS circle in center
    center_label = data.get('center_label', 'VS')
    circle = patches.Circle(
        (mid, 0.5), 0.035,
        facecolor=COLORS['orange'],
        edgecolor=COLORS['white'],
        linewidth=2,
        zorder=5
    )
    ax.add_patch(circle)
    ax.text(mid, 0.5, center_label,
            ha='center', va='center',
            fontsize=FONTS['body_size'],
            fontweight='bold',
            fontfamily=FONTS['family'],
            color=COLORS['text_on_dark'],
            zorder=6)

    # Divider line
    ax.plot([mid, mid], [margin, 0.46], color=COLORS['border'],
            linewidth=1.5, linestyle='--', zorder=4)
    ax.plot([mid, mid], [0.54, 0.93], color=COLORS['border'],
            linewidth=1.5, linestyle='--', zorder=4)

    save_figure(fig, output_path)


def _render_table(figure_entry, data, output_path):
    """Render a comparison table with categories and values."""
    fig, ax = create_figure(figure_entry['figure_number'], figure_entry['title'])
    hide_axes(ax)

    columns = data.get('columns', [])
    rows = data.get('rows', [])
    n_cols = len(columns)
    n_rows = len(rows)

    if n_cols == 0 or n_rows == 0:
        save_figure(fig, output_path)
        return

    margin = 0.05
    cat_col_w = 0.20  # category column width
    data_w = 1.0 - 2 * margin - cat_col_w
    col_w = data_w / n_cols

    header_h = 0.07
    row_h = min(0.08, (0.88 - header_h) / n_rows)
    table_top = 0.93

    # Column headers
    for j, col in enumerate(columns):
        x = margin + cat_col_w + j * col_w
        color = COLORS.get(col.get('color', 'navy'), col.get('color', COLORS['navy']))

        rect = patches.Rectangle(
            (x, table_top - header_h), col_w, header_h,
            facecolor=color,
            edgecolor=COLORS['white'],
            linewidth=1,
            zorder=2
        )
        ax.add_patch(rect)

        rgb = tuple(int(color.lstrip('#')[k:k+2], 16) for k in (0, 2, 4))
        brightness = (rgb[0] * 299 + rgb[1] * 587 + rgb[2] * 114) / 1000
        tc = COLORS['text_on_dark'] if brightness < 128 else COLORS['text']

        ax.text(x + col_w / 2, table_top - header_h / 2,
                col.get('header', ''),
                ha='center', va='center',
                fontsize=FONTS['body_size'],
                fontweight='bold',
                fontfamily=FONTS['family'],
                color=tc,
                zorder=3)

    # Category header
    cat_rect = patches.Rectangle(
        (margin, table_top - header_h), cat_col_w, header_h,
        facecolor=COLORS['steel_blue'],
        edgecolor=COLORS['white'],
        linewidth=1,
        zorder=2
    )
    ax.add_patch(cat_rect)
    ax.text(margin + cat_col_w / 2, table_top - header_h / 2,
            'Category',
            ha='center', va='center',
            fontsize=FONTS['body_size'],
            fontweight='bold',
            fontfamily=FONTS['family'],
            color=COLORS['text_on_dark'],
            zorder=3)

    # Data rows
    for i, row in enumerate(rows):
        y = table_top - header_h - (i + 1) * row_h
        stripe = COLORS['white'] if i % 2 == 0 else COLORS['grid']

        # Category cell
        cat_rect = patches.Rectangle(
            (margin, y), cat_col_w, row_h,
            facecolor=stripe,
            edgecolor=COLORS['border'],
            linewidth=0.5,
            zorder=1
        )
        ax.add_patch(cat_rect)
        ax.text(margin + 0.02, y + row_h / 2,
                row.get('category', ''),
                ha='left', va='center',
                fontsize=FONTS['note_size'],
                fontweight='bold',
                fontfamily=FONTS['family'],
                color=COLORS['text'],
                zorder=3)

        # Value cells
        values = row.get('values', [])
        for j, val in enumerate(values[:n_cols]):
            x = margin + cat_col_w + j * col_w
            val_rect = patches.Rectangle(
                (x, y), col_w, row_h,
                facecolor=stripe,
                edgecolor=COLORS['border'],
                linewidth=0.5,
                zorder=1
            )
            ax.add_patch(val_rect)
            ax.text(x + col_w / 2, y + row_h / 2,
                    wrap_text(str(val), 18),
                    ha='center', va='center',
                    fontsize=FONTS['note_size'],
                    fontfamily=FONTS['family'],
                    color=COLORS['text'],
                    zorder=3)

    save_figure(fig, output_path)
