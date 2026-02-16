"""
Chart Renderer
===============
Renders line charts, bar charts, and financial analysis graphics
such as EPS/EBIT analysis.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from tools.graphics.config import COLORS, FONTS, FIGURE
from tools.graphics.base import create_figure, save_figure, wrap_text


def render(figure_entry, data, output_path):
    """
    Render a chart figure.

    data keys:
        style:          str  – 'line' (default), 'bar', 'eps_ebit', 'stacked_bar'
        x_label:        str  – X-axis label
        y_label:        str  – Y-axis label
        x_values:       list – X-axis values or labels
        datasets:       list of dicts:
            label:      str  – series label
            values:     list  – Y values matching x_values
            color:      str  – COLORS key or hex
            style:      str  – line style: 'solid', 'dashed', 'dotted' (line charts)
        show_legend:    bool – show legend (default True)
        show_grid:      bool – show grid (default True)
        annotations:    list of dicts (optional):
            x:          float/int – x position
            y:          float/int – y position
            text:       str  – annotation text
        crossover:      dict (optional, for eps_ebit):
            x:          float – crossover EBIT value
            label:      str  – crossover label
        y_format:       str  – 'currency', 'percent', 'number' (default 'number')
    """
    style = data.get('style', 'line')

    if style == 'eps_ebit':
        _render_eps_ebit(figure_entry, data, output_path)
    elif style == 'bar':
        _render_bar(figure_entry, data, output_path)
    elif style == 'stacked_bar':
        _render_stacked_bar(figure_entry, data, output_path)
    else:
        _render_line(figure_entry, data, output_path)


def _render_line(figure_entry, data, output_path):
    """Render a line chart."""
    fig, ax = create_figure(figure_entry['figure_number'], figure_entry['title'])

    x_values = data.get('x_values', [])
    datasets = data.get('datasets', [])

    for ds in datasets:
        color = COLORS.get(ds.get('color', 'navy'), ds.get('color', COLORS['navy']))
        line_styles = {'solid': '-', 'dashed': '--', 'dotted': ':'}
        ls = line_styles.get(ds.get('style', 'solid'), '-')

        ax.plot(x_values[:len(ds.get('values', []))],
                ds.get('values', []),
                color=color,
                linewidth=2.5,
                linestyle=ls,
                label=ds.get('label', ''),
                marker='o',
                markersize=5,
                zorder=3)

    _apply_chart_styling(ax, data)
    save_figure(fig, output_path)


def _render_eps_ebit(figure_entry, data, output_path):
    """Render EPS/EBIT analysis chart with crossover point."""
    fig, ax = create_figure(figure_entry['figure_number'], figure_entry['title'])

    x_values = data.get('x_values', [])
    datasets = data.get('datasets', [])

    for ds in datasets:
        color = COLORS.get(ds.get('color', 'navy'), ds.get('color', COLORS['navy']))
        line_styles = {'solid': '-', 'dashed': '--', 'dotted': ':'}
        ls = line_styles.get(ds.get('style', 'solid'), '-')
        values = ds.get('values', [])

        ax.plot(x_values[:len(values)],
                values,
                color=color,
                linewidth=2.5,
                linestyle=ls,
                label=ds.get('label', ''),
                marker='o',
                markersize=5,
                zorder=3)

    # Crossover point
    crossover = data.get('crossover')
    if crossover:
        cx = crossover.get('x', 0)
        cy = crossover.get('y', 0)

        # Calculate crossover y if not given
        if cy == 0 and len(datasets) >= 2 and len(x_values) >= 2:
            # Interpolate
            for ds in datasets:
                vals = ds.get('values', [])
                if len(vals) >= 2:
                    for j in range(len(vals) - 1):
                        if x_values[j] <= cx <= x_values[j+1]:
                            t = (cx - x_values[j]) / (x_values[j+1] - x_values[j])
                            cy = vals[j] + t * (vals[j+1] - vals[j])
                            break

        ax.scatter([cx], [cy], s=120, c=[COLORS['orange']],
                   edgecolors=COLORS['text'], linewidths=2, zorder=5)

        clabel = crossover.get('label', 'Crossover Point')
        ax.annotate(clabel,
                    xy=(cx, cy),
                    xytext=(cx + (max(x_values) - min(x_values)) * 0.08,
                            cy + (max(max(ds.get('values', [0])) for ds in datasets) -
                                  min(min(ds.get('values', [0])) for ds in datasets)) * 0.12),
                    fontsize=FONTS['body_size'],
                    fontweight='bold',
                    fontfamily=FONTS['family'],
                    color=COLORS['orange'],
                    arrowprops=dict(arrowstyle='->',
                                    color=COLORS['orange'],
                                    lw=1.5),
                    bbox=dict(boxstyle='round,pad=0.3',
                              facecolor=COLORS['bg'],
                              edgecolor=COLORS['orange'],
                              alpha=0.9),
                    zorder=6)

        # Vertical dashed line at crossover
        ax.axvline(x=cx, color=COLORS['border'], linewidth=1,
                   linestyle='--', zorder=1)

        # Region labels
        if len(datasets) >= 2:
            x_range = max(x_values) - min(x_values)
            ax.text(cx - x_range * 0.15, ax.get_ylim()[1] * 0.9,
                    f'Favor\n{datasets[0].get("label", "Option A")}',
                    ha='center', va='top',
                    fontsize=FONTS['note_size'],
                    fontfamily=FONTS['family'],
                    color=COLORS.get(datasets[0].get('color', 'navy'),
                                     COLORS['navy']),
                    fontweight='bold',
                    alpha=0.7)
            ax.text(cx + x_range * 0.15, ax.get_ylim()[1] * 0.9,
                    f'Favor\n{datasets[1].get("label", "Option B")}',
                    ha='center', va='top',
                    fontsize=FONTS['note_size'],
                    fontfamily=FONTS['family'],
                    color=COLORS.get(datasets[1].get('color', 'teal'),
                                     COLORS['teal']),
                    fontweight='bold',
                    alpha=0.7)

    _apply_chart_styling(ax, data)
    save_figure(fig, output_path)


def _render_bar(figure_entry, data, output_path):
    """Render a bar chart."""
    fig, ax = create_figure(figure_entry['figure_number'], figure_entry['title'])

    x_values = data.get('x_values', [])
    datasets = data.get('datasets', [])
    n_ds = len(datasets)

    if n_ds == 0:
        save_figure(fig, output_path)
        return

    x = np.arange(len(x_values))
    bar_width = 0.7 / n_ds

    for i, ds in enumerate(datasets):
        color = COLORS.get(ds.get('color', 'navy'), ds.get('color', COLORS['navy']))
        values = ds.get('values', [])
        offset = (i - n_ds / 2 + 0.5) * bar_width

        ax.bar(x[:len(values)] + offset, values,
               bar_width, label=ds.get('label', ''),
               color=color, edgecolor=COLORS['white'],
               linewidth=0.5, zorder=3)

    ax.set_xticks(x)
    ax.set_xticklabels(x_values, fontsize=FONTS['note_size'],
                       fontfamily=FONTS['family'])

    _apply_chart_styling(ax, data)
    save_figure(fig, output_path)


def _render_stacked_bar(figure_entry, data, output_path):
    """Render a stacked bar chart."""
    fig, ax = create_figure(figure_entry['figure_number'], figure_entry['title'])

    x_values = data.get('x_values', [])
    datasets = data.get('datasets', [])

    if not datasets:
        save_figure(fig, output_path)
        return

    x = np.arange(len(x_values))
    bar_width = 0.5
    bottom = np.zeros(len(x_values))

    for ds in datasets:
        color = COLORS.get(ds.get('color', 'navy'), ds.get('color', COLORS['navy']))
        values = np.array(ds.get('values', []))
        ax.bar(x[:len(values)], values[:len(x)],
               bar_width, bottom=bottom[:len(values)],
               label=ds.get('label', ''),
               color=color, edgecolor=COLORS['white'],
               linewidth=0.5, zorder=3)
        bottom[:len(values)] += values[:len(x)]

    ax.set_xticks(x)
    ax.set_xticklabels(x_values, fontsize=FONTS['note_size'],
                       fontfamily=FONTS['family'])

    _apply_chart_styling(ax, data)
    save_figure(fig, output_path)


def _apply_chart_styling(ax, data):
    """Apply consistent styling to chart axes."""
    # Grid
    if data.get('show_grid', True):
        ax.grid(True, axis='y', color=COLORS['grid'], linewidth=0.5,
                alpha=0.7, zorder=0)
        ax.set_axisbelow(True)

    # Axis labels
    x_label = data.get('x_label', '')
    y_label = data.get('y_label', '')

    if x_label:
        ax.set_xlabel(x_label, fontsize=FONTS['axis_label_size'],
                      fontfamily=FONTS['family'],
                      fontweight='bold', color=COLORS['text'],
                      labelpad=8)
    if y_label:
        ax.set_ylabel(y_label, fontsize=FONTS['axis_label_size'],
                      fontfamily=FONTS['family'],
                      fontweight='bold', color=COLORS['text'],
                      labelpad=8)

    # Tick styling
    ax.tick_params(axis='both', labelsize=FONTS['note_size'],
                   colors=COLORS['text_secondary'])

    # Y-axis formatting
    y_format = data.get('y_format', 'number')
    if y_format == 'currency':
        from matplotlib.ticker import FuncFormatter
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f'${v:,.0f}'))
    elif y_format == 'percent':
        from matplotlib.ticker import FuncFormatter
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{v:.0f}%'))

    # Spine styling
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    for spine in ['bottom', 'left']:
        ax.spines[spine].set_color(COLORS['border'])

    ax.set_facecolor(COLORS['bg'])

    # Legend
    if data.get('show_legend', True):
        leg = ax.legend(fontsize=FONTS['note_size'],
                        frameon=True,
                        facecolor=COLORS['bg'],
                        edgecolor=COLORS['border'],
                        loc='best')
        for text in leg.get_texts():
            text.set_fontfamily(FONTS['family'])

    # Annotations
    for ann in data.get('annotations', []):
        ax.annotate(ann.get('text', ''),
                    xy=(ann.get('x', 0), ann.get('y', 0)),
                    fontsize=FONTS['note_size'],
                    fontfamily=FONTS['family'],
                    color=COLORS['text'],
                    fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.2',
                              facecolor=COLORS['bg'],
                              edgecolor=COLORS['border'],
                              alpha=0.9),
                    zorder=6)
