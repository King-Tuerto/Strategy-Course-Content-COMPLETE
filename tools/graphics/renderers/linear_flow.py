"""
Linear Flow Renderer
=====================
Renders value chains, spectrums, process arrows, and step-by-step sequences.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from tools.graphics.config import COLORS, FONTS, FIGURE
from tools.graphics.base import create_figure, save_figure, wrap_text, draw_rounded_box, hide_axes


def render(figure_entry, data, output_path):
    """
    Render a linear flow figure.

    data keys:
        style:          str  – 'arrows' (default), 'chevrons', 'spectrum', 'value_chain'
        orientation:    str  – 'horizontal' (default), 'vertical'
        steps:          list of dicts:
            label:      str  – step text
            color:      str  – COLORS key or hex
            sublabel:   str  – smaller text below label (optional)
            items:      list of str – detail items below step (optional)
        connectors:     str  – 'arrows' (default), 'lines', 'none'
        header:         str  – overall header text (optional)
        footer:         str  – footer annotation (optional)
        spectrum_labels: dict – for spectrum style:
            left:       str  – left end label
            right:      str  – right end label
        support_bar:    dict (optional) – value chain support activities bar:
            label:      str
            color:      str
            items:      list of str
    """
    style = data.get('style', 'arrows')

    if style == 'chevrons':
        _render_chevrons(figure_entry, data, output_path)
    elif style == 'spectrum':
        _render_spectrum(figure_entry, data, output_path)
    elif style == 'value_chain':
        _render_value_chain(figure_entry, data, output_path)
    else:
        _render_arrows(figure_entry, data, output_path)


def _render_arrows(figure_entry, data, output_path):
    """Render step-by-step arrow flow."""
    fig, ax = create_figure(figure_entry['figure_number'], figure_entry['title'])
    hide_axes(ax)

    steps = data.get('steps', [])
    n = len(steps)
    if n == 0:
        save_figure(fig, output_path)
        return

    orientation = data.get('orientation', 'horizontal')
    margin = 0.08
    gap = 0.04

    if orientation == 'horizontal':
        step_w = (1.0 - 2 * margin - gap * (n - 1)) / n
        step_h = 0.25
        y_center = 0.55

        for i, step in enumerate(steps):
            x = margin + i * (step_w + gap)
            color = step.get('color', 'navy')

            draw_rounded_box(ax, x, y_center - step_h / 2,
                             step_w, step_h,
                             step.get('label', ''),
                             color=color,
                             fontsize=FONTS['body_size'],
                             text_wrap=14)

            # Sublabel
            sublabel = step.get('sublabel', '')
            if sublabel:
                ax.text(x + step_w / 2, y_center - step_h / 2 - 0.04,
                        wrap_text(sublabel, 18),
                        ha='center', va='top',
                        fontsize=FONTS['note_size'],
                        fontfamily=FONTS['family'],
                        color=COLORS['text_secondary'])

            # Detail items below
            items = step.get('items', [])
            for j, item in enumerate(items[:4]):
                iy = y_center - step_h / 2 - 0.08 - j * 0.04
                ax.text(x + step_w / 2, iy, f'• {item}',
                        ha='center', va='top',
                        fontsize=6,
                        fontfamily=FONTS['family'],
                        color=COLORS['text_secondary'])

            # Arrow connector
            if i < n - 1 and data.get('connectors', 'arrows') != 'none':
                ax_end = x + step_w
                ax_start = ax_end + gap * 0.15
                ax_tip = ax_end + gap * 0.85
                ax.annotate('', xy=(ax_tip, y_center),
                            xytext=(ax_start, y_center),
                            arrowprops=dict(arrowstyle='->', lw=2,
                                            color=COLORS['steel_blue']),
                            zorder=5)
    else:
        # Vertical layout
        step_w = 0.35
        step_h = (1.0 - 2 * margin - gap * (n - 1)) / n
        x_center = 0.35

        for i, step in enumerate(steps):
            y = 1.0 - margin - (i + 1) * (step_h + gap) + gap
            color = step.get('color', 'navy')

            draw_rounded_box(ax, x_center - step_w / 2, y,
                             step_w, step_h,
                             step.get('label', ''),
                             color=color,
                             fontsize=FONTS['body_size'],
                             text_wrap=20)

            # Items to the right
            items = step.get('items', [])
            for j, item in enumerate(items[:4]):
                ix = x_center + step_w / 2 + 0.05
                iy = y + step_h / 2 + 0.02 - j * 0.035
                ax.text(ix, iy, f'• {item}',
                        ha='left', va='center',
                        fontsize=FONTS['note_size'],
                        fontfamily=FONTS['family'],
                        color=COLORS['text_secondary'])

            # Arrow connector
            if i < n - 1 and data.get('connectors', 'arrows') != 'none':
                ay_start = y
                ay_tip = y - gap * 0.8
                ax.annotate('', xy=(x_center, ay_tip),
                            xytext=(x_center, ay_start - 0.01),
                            arrowprops=dict(arrowstyle='->', lw=2,
                                            color=COLORS['steel_blue']),
                            zorder=5)

    # Header
    header = data.get('header', '')
    if header:
        ax.text(0.5, 0.97, header,
                ha='center', va='top',
                fontsize=FONTS['cell_label_size'],
                fontweight='bold',
                fontfamily=FONTS['family'],
                color=COLORS['text'])

    # Footer
    footer = data.get('footer', '')
    if footer:
        ax.text(0.5, 0.02, footer,
                ha='center', va='bottom',
                fontsize=FONTS['note_size'],
                fontstyle='italic',
                fontfamily=FONTS['family'],
                color=COLORS['text_secondary'])

    save_figure(fig, output_path)


def _render_chevrons(figure_entry, data, output_path):
    """Render chevron-style (arrow-shaped boxes) flow."""
    fig, ax = create_figure(figure_entry['figure_number'], figure_entry['title'])
    hide_axes(ax)

    steps = data.get('steps', [])
    n = len(steps)
    if n == 0:
        save_figure(fig, output_path)
        return

    margin = 0.05
    chevron_h = 0.22
    y_center = 0.55
    arrow_indent = 0.025
    total_w = 1.0 - 2 * margin
    chev_w = total_w / n

    for i, step in enumerate(steps):
        x = margin + i * chev_w
        color = COLORS.get(step.get('color', 'navy'), step.get('color', COLORS['navy']))

        # Chevron polygon
        if i == 0:
            # First: flat left edge
            pts = [
                (x, y_center - chevron_h / 2),
                (x + chev_w - arrow_indent, y_center - chevron_h / 2),
                (x + chev_w + arrow_indent, y_center),
                (x + chev_w - arrow_indent, y_center + chevron_h / 2),
                (x, y_center + chevron_h / 2),
            ]
        elif i == n - 1:
            # Last: pointed right, indented left
            pts = [
                (x - arrow_indent, y_center - chevron_h / 2),
                (x + chev_w, y_center - chevron_h / 2),
                (x + chev_w, y_center + chevron_h / 2),
                (x - arrow_indent, y_center + chevron_h / 2),
                (x + arrow_indent, y_center),
            ]
        else:
            # Middle: both indented
            pts = [
                (x - arrow_indent, y_center - chevron_h / 2),
                (x + chev_w - arrow_indent, y_center - chevron_h / 2),
                (x + chev_w + arrow_indent, y_center),
                (x + chev_w - arrow_indent, y_center + chevron_h / 2),
                (x - arrow_indent, y_center + chevron_h / 2),
                (x + arrow_indent, y_center),
            ]

        chev = plt.Polygon(pts, facecolor=color, edgecolor=COLORS['white'],
                           linewidth=2, zorder=2)
        ax.add_patch(chev)

        # Text
        rgb = tuple(int(color.lstrip('#')[j:j+2], 16) for j in (0, 2, 4))
        brightness = (rgb[0] * 299 + rgb[1] * 587 + rgb[2] * 114) / 1000
        tc = COLORS['text_on_dark'] if brightness < 128 else COLORS['text']

        ax.text(x + chev_w / 2, y_center,
                wrap_text(step.get('label', ''), 12),
                ha='center', va='center',
                fontsize=FONTS['body_size'],
                fontweight='bold',
                fontfamily=FONTS['family'],
                color=tc,
                zorder=3)

        # Items below
        items = step.get('items', [])
        for j, item in enumerate(items[:4]):
            iy = y_center - chevron_h / 2 - 0.05 - j * 0.04
            ax.text(x + chev_w / 2, iy, f'• {item}',
                    ha='center', va='top',
                    fontsize=6,
                    fontfamily=FONTS['family'],
                    color=COLORS['text_secondary'])

    save_figure(fig, output_path)


def _render_spectrum(figure_entry, data, output_path):
    """Render a continuous spectrum/gradient bar."""
    fig, ax = create_figure(figure_entry['figure_number'], figure_entry['title'])
    hide_axes(ax)

    steps = data.get('steps', [])
    n = len(steps)
    spectrum_labels = data.get('spectrum_labels', {})

    margin = 0.08
    bar_h = 0.15
    y_center = 0.55
    bar_w = 1.0 - 2 * margin
    seg_w = bar_w / max(n, 1)

    for i, step in enumerate(steps):
        x = margin + i * seg_w
        color = COLORS.get(step.get('color', 'teal'), step.get('color', COLORS['teal']))

        rect = patches.Rectangle(
            (x, y_center - bar_h / 2), seg_w, bar_h,
            facecolor=color,
            edgecolor=COLORS['white'],
            linewidth=1,
            zorder=2
        )
        ax.add_patch(rect)

        rgb = tuple(int(color.lstrip('#')[j:j+2], 16) for j in (0, 2, 4))
        brightness = (rgb[0] * 299 + rgb[1] * 587 + rgb[2] * 114) / 1000
        tc = COLORS['text_on_dark'] if brightness < 128 else COLORS['text']

        ax.text(x + seg_w / 2, y_center,
                wrap_text(step.get('label', ''), 14),
                ha='center', va='center',
                fontsize=FONTS['note_size'],
                fontweight='bold',
                fontfamily=FONTS['family'],
                color=tc,
                zorder=3)

        # Items below
        items = step.get('items', [])
        for j, item in enumerate(items[:3]):
            iy = y_center - bar_h / 2 - 0.04 - j * 0.04
            ax.text(x + seg_w / 2, iy, f'• {item}',
                    ha='center', va='top',
                    fontsize=6,
                    fontfamily=FONTS['family'],
                    color=COLORS['text_secondary'])

    # Spectrum endpoint labels
    left_label = spectrum_labels.get('left', '')
    right_label = spectrum_labels.get('right', '')
    if left_label:
        ax.text(margin, y_center + bar_h / 2 + 0.04, f'← {left_label}',
                ha='left', va='bottom',
                fontsize=FONTS['body_size'],
                fontweight='bold',
                fontfamily=FONTS['family'],
                color=COLORS['text'])
    if right_label:
        ax.text(1.0 - margin, y_center + bar_h / 2 + 0.04, f'{right_label} →',
                ha='right', va='bottom',
                fontsize=FONTS['body_size'],
                fontweight='bold',
                fontfamily=FONTS['family'],
                color=COLORS['text'])

    save_figure(fig, output_path)


def _render_value_chain(figure_entry, data, output_path):
    """Render Porter's Value Chain style with primary + support activities."""
    fig, ax = create_figure(figure_entry['figure_number'], figure_entry['title'])
    hide_axes(ax)

    steps = data.get('steps', [])
    support_bar = data.get('support_bar', {})
    n = len(steps)
    if n == 0:
        save_figure(fig, output_path)
        return

    margin = 0.06
    # Support bar at top
    support_h = 0.18 if support_bar else 0.0
    primary_top = 0.92 - support_h
    primary_h = 0.30
    primary_y = primary_top - primary_h

    # Support activities bar
    if support_bar:
        sb_color = COLORS.get(support_bar.get('color', 'steel_blue'),
                              support_bar.get('color', COLORS['steel_blue']))
        sb_rect = patches.FancyBboxPatch(
            (margin, primary_top + 0.02), 1.0 - 2 * margin, support_h - 0.04,
            boxstyle='round,pad=0.008',
            facecolor=sb_color,
            edgecolor=COLORS['border'],
            linewidth=1,
            alpha=0.3,
            zorder=1
        )
        ax.add_patch(sb_rect)

        ax.text(margin + 0.03, primary_top + support_h / 2,
                support_bar.get('label', 'Support Activities'),
                ha='left', va='center',
                fontsize=FONTS['body_size'],
                fontweight='bold',
                fontfamily=FONTS['family'],
                color=COLORS['text'])

        items = support_bar.get('items', [])
        item_w = (1.0 - 2 * margin - 0.25) / max(len(items), 1)
        for j, item in enumerate(items):
            ix = margin + 0.25 + j * item_w
            ax.text(ix, primary_top + support_h / 2,
                    f'• {item}',
                    ha='left', va='center',
                    fontsize=FONTS['note_size'],
                    fontfamily=FONTS['family'],
                    color=COLORS['text_secondary'])

    # Primary activities as chevrons
    arrow_indent = 0.02
    total_w = 1.0 - 2 * margin
    chev_w = total_w / n

    for i, step in enumerate(steps):
        x = margin + i * chev_w
        color = COLORS.get(step.get('color', 'navy'), step.get('color', COLORS['navy']))

        # Chevron
        if i == n - 1:
            # Last: margin arrow on right
            pts = [
                (x + arrow_indent, primary_y),
                (x + chev_w, primary_y),
                (x + chev_w, primary_y + primary_h),
                (x + arrow_indent, primary_y + primary_h),
                (x - arrow_indent, primary_y + primary_h / 2),
            ]
        elif i == 0:
            pts = [
                (x, primary_y),
                (x + chev_w - arrow_indent, primary_y),
                (x + chev_w + arrow_indent, primary_y + primary_h / 2),
                (x + chev_w - arrow_indent, primary_y + primary_h),
                (x, primary_y + primary_h),
            ]
        else:
            pts = [
                (x + arrow_indent, primary_y),
                (x + chev_w - arrow_indent, primary_y),
                (x + chev_w + arrow_indent, primary_y + primary_h / 2),
                (x + chev_w - arrow_indent, primary_y + primary_h),
                (x + arrow_indent, primary_y + primary_h),
                (x - arrow_indent, primary_y + primary_h / 2),
            ]

        chev = plt.Polygon(pts, facecolor=color, edgecolor=COLORS['white'],
                           linewidth=2, zorder=2)
        ax.add_patch(chev)

        rgb = tuple(int(color.lstrip('#')[j:j+2], 16) for j in (0, 2, 4))
        brightness = (rgb[0] * 299 + rgb[1] * 587 + rgb[2] * 114) / 1000
        tc = COLORS['text_on_dark'] if brightness < 128 else COLORS['text']

        cy = primary_y + primary_h / 2
        ax.text(x + chev_w / 2, cy + 0.03,
                wrap_text(step.get('label', ''), 12),
                ha='center', va='center',
                fontsize=FONTS['body_size'],
                fontweight='bold',
                fontfamily=FONTS['family'],
                color=tc,
                zorder=3)

        # Sub-items within chevron
        items = step.get('items', [])
        for j, item in enumerate(items[:3]):
            iy = cy - 0.04 - j * 0.04
            ax.text(x + chev_w / 2, iy,
                    item,
                    ha='center', va='center',
                    fontsize=6,
                    fontfamily=FONTS['family'],
                    color=tc,
                    alpha=0.85,
                    zorder=3)

    # Margin arrow at right end (profit wedge)
    margin_x = margin + total_w
    margin_w = 0.06
    margin_pts = [
        (margin_x - 0.01, primary_y),
        (margin_x + margin_w, primary_y + primary_h / 2),
        (margin_x - 0.01, primary_y + primary_h),
    ]
    margin_arrow = plt.Polygon(margin_pts, facecolor=COLORS['gold'],
                               edgecolor=COLORS['border'],
                               linewidth=1, zorder=2)
    ax.add_patch(margin_arrow)
    ax.text(margin_x + margin_w * 0.35, primary_y + primary_h / 2,
            'M\nA\nR\nG\nI\nN',
            ha='center', va='center',
            fontsize=5, fontweight='bold',
            fontfamily=FONTS['family'],
            color=COLORS['text'],
            linespacing=0.8,
            zorder=3)

    save_figure(fig, output_path)
