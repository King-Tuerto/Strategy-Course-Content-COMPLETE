#!/usr/bin/env python3
"""
GCU Figure Numbering Fix
Converts figure captions from single-line format to GCU two-line format.

Before: **Figure 3.5.** *Title Text*
After:  **Figure 3.5**
        *Title Text*

Also removes periods after figure numbers and strips any bold markers
inside italic figure titles (caused by key-term bolding running on captions).

Usage:
    python tools/gcu_fix_figures.py
    python tools/gcu_fix_figures.py --dry-run
"""

import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CHAPTERS_DIR = BASE / "output" / "chapters"
TOOLGUIDES_DIR = BASE / "output" / "tool-guides"


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def fix_figure_numbering(text):
    """Fix figure captions to GCU two-line format."""
    changes = 0
    lines = text.split("\n")
    new_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Match: **Figure X.Y.** *Title* or **Figure X.Y** *Title* (on same line)
        m = re.match(
            r'^(\*\*(?:Figure|Table)\s+\d+(?:\.\d+)?)\.*\*\*\s*\*(.+)\*\s*$',
            line.strip()
        )
        if m:
            # Extract number and title
            number_part = m.group(1) + "**"  # e.g., **Figure 3.5**
            title_text = m.group(2)  # e.g., Title Text

            # Clean any bold markers from inside the italic title
            # e.g., *Six **Functional Areas** for Internal Audit*
            title_text = re.sub(r'\*\*(.+?)\*\*', r'\1', title_text)

            # Build GCU format: number on own line, italic title on next
            new_lines.append(number_part)
            new_lines.append(f"*{title_text}*")
            changes += 1
            i += 1
            continue

        # Also catch variants with period: **Figure 7.1.** *Title*
        m2 = re.match(
            r'^(\*\*(?:Figure|Table)\s+\d+(?:\.\d+)?)\.?\*\*\.?\s*\*(.+)\*\s*$',
            line.strip()
        )
        if m2 and not m:
            number_part = m2.group(1) + "**"
            title_text = m2.group(2)
            title_text = re.sub(r'\*\*(.+?)\*\*', r'\1', title_text)
            new_lines.append(number_part)
            new_lines.append(f"*{title_text}*")
            changes += 1
            i += 1
            continue

        new_lines.append(line)
        i += 1

    return "\n".join(new_lines), changes


def collect_files():
    files = []
    for d in [CHAPTERS_DIR, TOOLGUIDES_DIR]:
        if d.exists():
            for f in sorted(d.glob("*.md")):
                files.append(f)
    return files


def main():
    dry_run = "--dry-run" in sys.argv

    files = collect_files()
    if not files:
        print("No .md files found.")
        sys.exit(1)

    if dry_run:
        print("DRY RUN — no files will be modified\n")

    print(f"Processing {len(files)} file(s)...\n")
    total = 0

    for f in files:
        text = read_file(f)
        new_text, n = fix_figure_numbering(text)
        name = f.stem

        if n > 0:
            print(f"  [FIX] {name}: Fixed {n} figure/table caption(s) to GCU format")
            if not dry_run:
                write_file(f, new_text)
                print(f"  [SAVE] {name}")
            total += n
        else:
            print(f"  [OK]  {name}: No figure formatting issues")

    print(f"\nTotal fixes: {total}")
    if dry_run:
        print("(DRY RUN — no files modified)")


if __name__ == "__main__":
    main()
