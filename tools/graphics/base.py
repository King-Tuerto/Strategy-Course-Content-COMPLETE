"""
Base Figure Utilities
======================
Creates figures with GCU-compliant labeling, provides save and text utilities.
All renderers use these functions.
"""

import textwrap
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for PNG generation
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from tools.graphics.config import COLORS, FONTS, FIGURE


def create_figure(figure_number, title, tall=False):
    """
    Create a matplotlib figure with GCU-compliant title area.

    Args:
        figure_number: str like "3.1" or "TG.5"
        title: str, the figure title (italic)
        tall: bool, use portrait orientation if True

    Returns:
        (fig, ax) - figure and content axes
    """
    w = FIGURE['tall_width'] if tall else FIGURE['width']
    h = FIGURE['tall_height'] if tall else FIGURE['height']

    fig = plt.figure(figsize=(w, h), dpi=FIGURE['dpi'],
                     facecolor=FIGURE['bg_color'])

    # Title area at top
    title_h = FIGURE['title_height']
    fig.text(0.5, 1 - title_h * 0.35, f'Figure {figure_number}',
             ha='center', va='center',
             fontsize=FONTS['figure_num_size'],
             fontweight='bold',
             fontfamily=FONTS['family'],
             color=COLORS['text'])
    fig.text(0.5, 1 - title_h * 0.70, title,
             ha='center', va='center',
             fontsize=FONTS['title_size'],
             fontstyle='italic',
             fontfamily=FONTS['family'],
             color=COLORS['text_secondary'])

    # Content axes below title
    ax = fig.add_axes([0.08, 0.06, 0.84, 1 - title_h - 0.08])
    ax.set_facecolor(FIGURE['bg_color'])

    return fig, ax


def save_figure(fig, filepath):
    """Save figure to PNG with design system settings."""
    fig.savefig(filepath, dpi=FIGURE['dpi'],
                facecolor=fig.get_facecolor(),
                bbox_inches='tight',
                pad_inches=0.3)
    plt.close(fig)


def wrap_text(text, width=20):
    """Wrap text at specified character width."""
    return '\n'.join(textwrap.wrap(text, width=width))


def draw_rounded_box(ax, x, y, w, h, text, color='navy',
                     text_color=None, fontsize=None, alpha=1.0,
                     linewidth=1.5, text_wrap=18):
    """
    Draw a rounded rectangle with centered text.

    Args:
        ax: matplotlib axes
        x, y: bottom-left corner (data coords)
        w, h: width and height
        text: label text
        color: key from COLORS dict or hex string
        text_color: override text color (auto-detects light/dark)
        fontsize: override font size
        alpha: fill alpha
        text_wrap: character width for text wrapping
    """
    fill_color = COLORS.get(color, color)

    box = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle='round,pad=0.02',
        facecolor=fill_color,
        edgecolor=COLORS.get('border', '#DEE2E6'),
        linewidth=linewidth,
        alpha=alpha,
        zorder=2
    )
    ax.add_patch(box)

    # Auto-detect text color based on background brightness
    if text_color is None:
        rgb = tuple(int(fill_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        brightness = (rgb[0] * 299 + rgb[1] * 587 + rgb[2] * 114) / 1000
        text_color = COLORS['text_on_dark'] if brightness < 128 else COLORS['text']

    if text_wrap and len(text) > text_wrap:
        text = wrap_text(text, text_wrap)

    fs = fontsize or FONTS['body_size']
    ax.text(x + w / 2, y + h / 2, text,
            ha='center', va='center',
            fontsize=fs, fontfamily=FONTS['family'],
            fontweight='bold', color=text_color,
            zorder=3)


def draw_arrow(ax, x1, y1, x2, y2, label='', color='steel_blue',
               style='->', linewidth=1.5, fontsize=None):
    """Draw an arrow between two points with optional label."""
    arrow_color = COLORS.get(color, color)
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style,
                                color=arrow_color,
                                lw=linewidth),
                zorder=1)
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        fs = fontsize or FONTS['note_size']
        ax.text(mx, my, label,
                ha='center', va='center',
                fontsize=fs, fontfamily=FONTS['family'],
                color=COLORS['text'],
                bbox=dict(boxstyle='round,pad=0.15',
                          facecolor=COLORS['bg'], edgecolor='none',
                          alpha=0.9),
                zorder=4)


def hide_axes(ax):
    """Remove all axis decorations for diagram-style figures."""
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
