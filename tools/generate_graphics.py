"""
Course Graphics Generator
==========================
CLI entry point for generating all course figures.

Usage:
    python tools/generate_graphics.py              # Generate all figures
    python tools/generate_graphics.py --topic 3    # Generate one topic
    python tools/generate_graphics.py --id vrio_tree  # Generate one figure
    python tools/generate_graphics.py --verify     # Verify all outputs exist
    python tools/generate_graphics.py --list       # List all registered figures
"""

import argparse
import importlib
import os
import sys
import time

# Ensure project root is on the path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from tools.graphics.manifest import (
    load_manifest, load_data_file, filter_figures,
    get_output_path, validate_manifest, generate_manifest_md
)


# ── Renderer Registry ──────────────────────────────────────────────────

RENDERERS = {
    'matrix_2x2':    'tools.graphics.renderers.matrix_2x2',
    'flowchart':     'tools.graphics.renderers.flowchart',
    'matrix_grid':   'tools.graphics.renderers.matrix_grid',
    'axis_quadrant': 'tools.graphics.renderers.axis_quadrant',
    'hierarchy':     'tools.graphics.renderers.hierarchy',
    'comparison':    'tools.graphics.renderers.comparison',
    'linear_flow':   'tools.graphics.renderers.linear_flow',
    'chart':         'tools.graphics.renderers.chart',
    'reference':     'tools.graphics.renderers.reference',
}

_renderer_cache = {}


def get_renderer(name):
    """Import and cache a renderer module."""
    if name not in _renderer_cache:
        if name not in RENDERERS:
            raise ValueError(f"Unknown renderer: '{name}'. "
                             f"Available: {list(RENDERERS.keys())}")
        _renderer_cache[name] = importlib.import_module(RENDERERS[name])
    return _renderer_cache[name]


# ── Paths ───────────────────────────────────────────────────────────────

MANIFEST_PATH = os.path.join(PROJECT_ROOT, 'tools', 'graphics', 'data', 'manifest.yaml')
DATA_DIR = os.path.join(PROJECT_ROOT, 'tools', 'graphics', 'data')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'output', 'graphics')
MANIFEST_MD_PATH = os.path.join(OUTPUT_DIR, 'MANIFEST.md')


# ── Core Functions ──────────────────────────────────────────────────────

def generate_figure(figure_entry):
    """Generate a single figure from its manifest entry."""
    fid = figure_entry['id']
    renderer_name = figure_entry['renderer']
    data_file = figure_entry.get('data_file', '')

    # Load figure-specific data
    data_path = os.path.join(DATA_DIR, data_file)
    if not os.path.exists(data_path):
        print(f"  ERROR: Data file not found: {data_file}")
        return False

    all_data = load_data_file(data_path)
    figure_data = all_data.get(fid, {})

    if not figure_data:
        print(f"  ERROR: No data for figure '{fid}' in {data_file}")
        return False

    # Build output path and ensure directory exists
    output_path = get_output_path(figure_entry, OUTPUT_DIR)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Get renderer and generate
    try:
        renderer = get_renderer(renderer_name)
        renderer.render(figure_entry, figure_data, output_path)
        return True
    except Exception as e:
        print(f"  ERROR generating '{fid}': {e}")
        import traceback
        traceback.print_exc()
        return False


def generate_all(figures):
    """Generate all figures in the list."""
    total = len(figures)
    success = 0
    failed = []

    print(f"\n{'='*60}")
    print(f"  COURSE GRAPHICS GENERATOR")
    print(f"  Generating {total} figures...")
    print(f"{'='*60}\n")

    start_time = time.time()

    for i, fig in enumerate(figures, 1):
        fid = fig['id']
        fnum = fig['figure_number']
        title = fig['title'][:40]

        print(f"  [{i:2d}/{total}]  Fig {fnum:6s}  {fid:30s}  ", end='', flush=True)

        if generate_figure(fig):
            print("OK")
            success += 1
        else:
            print("FAILED")
            failed.append(fid)

    elapsed = time.time() - start_time

    print(f"\n{'='*60}")
    print(f"  RESULTS: {success}/{total} generated successfully ({elapsed:.1f}s)")
    if failed:
        print(f"  FAILED ({len(failed)}): {', '.join(failed)}")
    print(f"{'='*60}\n")

    return success, failed


def verify_outputs(figures):
    """Verify all expected output files exist and have non-zero size."""
    print(f"\n{'='*60}")
    print(f"  VERIFICATION: Checking {len(figures)} figures...")
    print(f"{'='*60}\n")

    missing = []
    empty = []
    ok = 0

    for fig in figures:
        output_path = get_output_path(fig, OUTPUT_DIR)
        if not os.path.exists(output_path):
            missing.append(fig['id'])
            print(f"  MISSING: {fig['figure_number']} — {output_path}")
        elif os.path.getsize(output_path) == 0:
            empty.append(fig['id'])
            print(f"  EMPTY:   {fig['figure_number']} — {output_path}")
        else:
            size_kb = os.path.getsize(output_path) / 1024
            print(f"  OK:      {fig['figure_number']:6s}  {fig['id']:30s}  {size_kb:6.1f} KB")
            ok += 1

    print(f"\n{'='*60}")
    print(f"  VERIFICATION RESULTS:")
    print(f"    OK:      {ok}")
    print(f"    Missing: {len(missing)}")
    print(f"    Empty:   {len(empty)}")
    if missing:
        print(f"    Missing IDs: {', '.join(missing)}")
    if empty:
        print(f"    Empty IDs:   {', '.join(empty)}")
    print(f"{'='*60}\n")

    return len(missing) == 0 and len(empty) == 0


def list_figures(figures):
    """Print a table of all registered figures."""
    print(f"\n{'='*70}")
    print(f"  REGISTERED FIGURES: {len(figures)}")
    print(f"{'='*70}")
    print(f"  {'#':6s}  {'ID':30s}  {'Renderer':15s}  {'Topic'}")
    print(f"  {'-'*6}  {'-'*30}  {'-'*15}  {'-'*6}")
    for fig in figures:
        print(f"  {fig['figure_number']:6s}  {fig['id']:30s}  "
              f"{fig['renderer']:15s}  {fig.get('topic', '?')}")
    print(f"{'='*70}\n")


# ── CLI ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Generate course graphics from YAML data files.')
    parser.add_argument('--topic', type=str, default=None,
                        help='Generate figures for one topic (1-7 or TG)')
    parser.add_argument('--id', type=str, default=None,
                        help='Generate a single figure by ID')
    parser.add_argument('--verify', action='store_true',
                        help='Verify all output files exist')
    parser.add_argument('--list', action='store_true',
                        help='List all registered figures')
    parser.add_argument('--manifest-md', action='store_true',
                        help='Regenerate MANIFEST.md')
    parser.add_argument('--validate', action='store_true',
                        help='Validate manifest for errors')

    args = parser.parse_args()

    # Load manifest
    if not os.path.exists(MANIFEST_PATH):
        print(f"ERROR: Manifest not found at {MANIFEST_PATH}")
        sys.exit(1)

    figures = load_manifest(MANIFEST_PATH)
    print(f"  Loaded {len(figures)} figures from manifest.")

    # Validate
    if args.validate:
        warnings = validate_manifest(figures)
        if warnings:
            print("\n  MANIFEST WARNINGS:")
            for w in warnings:
                print(f"    - {w}")
        else:
            print("\n  Manifest is valid. No issues found.")
        return

    # List
    if args.list:
        list_figures(figures)
        return

    # Filter
    if args.id:
        figures = filter_figures(figures, figure_id=args.id)
        if not figures:
            print(f"ERROR: No figure found with ID '{args.id}'")
            sys.exit(1)
    elif args.topic:
        # Parse topic: could be int or 'TG'
        try:
            topic_val = int(args.topic)
        except ValueError:
            topic_val = args.topic
        figures = filter_figures(figures, topic=topic_val)
        if not figures:
            print(f"ERROR: No figures found for topic '{args.topic}'")
            sys.exit(1)

    # Verify mode
    if args.verify:
        all_ok = verify_outputs(figures)
        sys.exit(0 if all_ok else 1)

    # Generate
    success, failed = generate_all(figures)

    # Auto-generate MANIFEST.md
    if args.manifest_md or (not args.id and not failed):
        all_figures = load_manifest(MANIFEST_PATH)
        count = generate_manifest_md(all_figures, MANIFEST_MD_PATH)
        print(f"  MANIFEST.md updated ({count} figures documented).")

    sys.exit(0 if not failed else 1)


if __name__ == '__main__':
    main()
