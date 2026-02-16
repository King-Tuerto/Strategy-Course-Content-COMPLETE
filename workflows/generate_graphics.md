# Workflow: Generate Course Graphics

## Objective
Generate all programmatic figures for the MBA Strategy Course using the Python graphics pipeline.

## Prerequisites
- Python 3.x with `matplotlib`, `numpy`, `pillow`, `pyyaml` installed
- All files in `tools/graphics/` intact

## Quick Commands

```bash
# Generate ALL 64 figures (~10 seconds)
python tools/generate_graphics.py

# Generate one topic only
python tools/generate_graphics.py --topic 3

# Generate a single figure by ID
python tools/generate_graphics.py --id bcg_matrix

# Verify all outputs exist and have content
python tools/generate_graphics.py --verify

# List all registered figures
python tools/generate_graphics.py --list

# Validate manifest for errors
python tools/generate_graphics.py --validate

# Regenerate MANIFEST.md only
python tools/generate_graphics.py --manifest-md
```

## File Structure

```
tools/
  generate_graphics.py          ← CLI entry point
  graphics/
    __init__.py
    config.py                   ← Design constants (colors, fonts, sizes)
    base.py                     ← Figure creation, GCU labeling, drawing utilities
    manifest.py                 ← YAML manifest reader/validator
    renderers/
      __init__.py
      matrix_2x2.py             ← BCG, Grand Strategy, Porter's Generic (2x2 grids)
      flowchart.py              ← Process flows, decision trees, cascades
      matrix_grid.py            ← IE Matrix (3x3), SWOT (2x2 with headers)
      axis_quadrant.py          ← SPACE Matrix, Perceptual Map (coordinate axes)
      hierarchy.py              ← Pyramids, org trees, tiered layouts
      comparison.py             ← Side-by-side, versus, comparison tables
      linear_flow.py            ← Value chain, chevrons, spectrums, process arrows
      chart.py                  ← EPS/EBIT, bar charts, line charts
      reference.py              ← Five Forces, Balanced Scorecard, hexagons, radial
    data/
      manifest.yaml             ← Master figure registry (64 figures)
      topic1.yaml - topic7.yaml ← Per-topic figure parameters
      tool_guides.yaml          ← Tool guide worked example parameters

output/graphics/
  topic-1/ through topic-7/     ← PNG outputs by topic
  tool-guides/                  ← Tool guide PNGs
  MANIFEST.md                   ← Auto-generated figure inventory
```

## How to Add a New Figure

1. **Register in manifest.yaml** — Add an entry with id, figure_number, title, filename, renderer, data_file, and alt_text
2. **Add data to the topic YAML** — Add a new key matching the figure id with all renderer-required parameters
3. **Run generation** — `python tools/generate_graphics.py --id your_new_id`
4. **Verify** — Check the output PNG visually

## How to Change the Design System

All visual constants live in `tools/graphics/config.py`:

- **Colors**: Change any hex value in the `COLORS` dict
- **Fonts**: Change family or sizes in the `FONTS` dict
- **Figure size**: Change dimensions or DPI in the `FIGURE` dict

After any change, re-run `python tools/generate_graphics.py` to regenerate all 64 figures with the updated design.

## Renderers Available

| Renderer | Style Options | Use For |
|----------|--------------|---------|
| matrix_2x2 | (default) | 2x2 quadrant matrices with colored cells |
| flowchart | vertical, horizontal, cascade | Process flows, decision trees |
| matrix_grid | basic, ie, swot | N×M grids with regions and headers |
| axis_quadrant | (default) | X-Y coordinate diagrams with quadrants |
| hierarchy | pyramid, tree, tiers | Pyramids, org charts, tiered layouts |
| comparison | side_by_side, versus, table | Feature comparisons, VS layouts |
| linear_flow | arrows, chevrons, spectrum, value_chain | Step sequences, spectrums |
| chart | line, bar, stacked_bar, eps_ebit | Data charts with financial formatting |
| reference | five_forces, balanced_scorecard, hexagon, category_grid, radial, cycle | Specialized frameworks |

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError: yaml` | Run `python -m pip install pyyaml` |
| `No data for figure 'xyz'` | Check that the figure id in manifest.yaml matches the key in the topic YAML |
| Font warnings | Segoe UI may not be available on non-Windows systems; Arial/sans-serif fallback is automatic |
| Figure looks wrong | Check the data YAML for correct key names; each renderer documents its expected data keys in the module docstring |

## GCU Compliance Checklist

- [x] Bold figure number (e.g., **Figure 4.4**)
- [x] Italic title below number
- [x] Alt text in manifest for every figure
- [x] Consistent figure numbering by topic
- [x] No external hyperlinks in graphics
