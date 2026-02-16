"""
Manifest Manager
=================
Reads the YAML manifest and provides lookup/validation utilities.
"""

import os
import yaml


def load_manifest(manifest_path):
    """Load the master manifest YAML file."""
    with open(manifest_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data.get('figures', [])


def load_data_file(data_path):
    """Load a per-topic YAML data file."""
    with open(data_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def filter_figures(figures, topic=None, figure_id=None):
    """Filter manifest figures by topic number or figure ID."""
    if figure_id:
        return [f for f in figures if f['id'] == figure_id]
    if topic is not None:
        return [f for f in figures if f.get('topic') == topic]
    return figures


def get_output_path(figure_entry, base_output_dir):
    """Build the full output file path for a figure."""
    topic = figure_entry.get('topic')
    if topic == 'TG':
        subdir = 'tool-guides'
    else:
        subdir = f'topic-{topic}'
    return os.path.join(base_output_dir, subdir, figure_entry['filename'])


def validate_manifest(figures):
    """Check manifest for common issues. Returns list of warning strings."""
    warnings = []
    seen_numbers = {}
    seen_ids = set()

    for f in figures:
        # Check required fields
        for field in ['id', 'figure_number', 'topic', 'title', 'filename',
                      'renderer', 'alt_text']:
            if field not in f:
                warnings.append(f"Figure '{f.get('id', 'UNKNOWN')}' missing '{field}'")

        # Check unique IDs
        fid = f.get('id')
        if fid in seen_ids:
            warnings.append(f"Duplicate figure ID: '{fid}'")
        seen_ids.add(fid)

        # Check unique figure numbers
        fnum = f.get('figure_number')
        if fnum in seen_numbers:
            warnings.append(
                f"Duplicate figure number {fnum}: "
                f"'{fid}' and '{seen_numbers[fnum]}'")
        seen_numbers[fnum] = fid

    return warnings


def generate_manifest_md(figures, output_path):
    """Generate human-readable MANIFEST.md from figure list."""
    from datetime import datetime

    lines = [
        '# Course Graphics Manifest\n',
        f'Generated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}\n',
        '---\n',
    ]

    # Group by topic
    topics = {}
    for f in figures:
        t = f.get('topic', 'Unknown')
        topics.setdefault(t, []).append(f)

    topic_names = {
        1: 'Foundations of Strategic Management',
        2: 'External Analysis and International Strategy',
        3: 'Internal Analysis and Strategy Types',
        4: 'Strategy Analysis and Implementation',
        6: 'Strategy Evaluation and Control',
        7: 'Finance and Accounting in Strategy Implementation',
        'TG': 'Tool Guide Examples',
    }

    total = 0
    for topic_num in sorted(topics.keys(), key=lambda x: (0, x) if isinstance(x, int) else (1, 0)):
        name = topic_names.get(topic_num, f'Topic {topic_num}')
        label = f'Topic {topic_num}' if isinstance(topic_num, int) else 'Tool Guides'
        lines.append(f'\n## {label}: {name}\n')
        lines.append('| Figure | Title | Filename | Alt Text |')
        lines.append('|--------|-------|----------|----------|')
        for f in topics[topic_num]:
            alt_short = f.get('alt_text', '')[:60] + '...' if len(f.get('alt_text', '')) > 60 else f.get('alt_text', '')
            lines.append(
                f"| {f['figure_number']} | {f['title']} | "
                f"{f['filename']} | {alt_short} |")
            total += 1

    lines.append(f'\n---\n\n**Total figures: {total}**\n')

    with open(output_path, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines))

    return total
