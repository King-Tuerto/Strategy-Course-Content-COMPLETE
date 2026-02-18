#!/usr/bin/env python3
"""
GCU Style Fix Tool
Applies mechanical formatting fixes to .md content files.

Fixes applied:
1. Scripture citations — adds (NIV) translation version
2. Key Terms bolded on first use in body text
3. APA in-text citation placeholders added where references exist

Usage:
    python tools/gcu_fix.py                    # Fix all output files
    python tools/gcu_fix.py --dry-run          # Show changes without writing
    python tools/gcu_fix.py --file <path>      # Fix one file
"""

import os
import re
import sys
from pathlib import Path
from copy import deepcopy

BASE = Path(__file__).resolve().parent.parent
CHAPTERS_DIR = BASE / "output" / "chapters"
TOOLGUIDES_DIR = BASE / "output" / "tool-guides"

BIBLE_BOOKS = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
    "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
    "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles",
    "Ezra", "Nehemiah", "Esther", "Job", "Psalm", "Psalms",
    "Proverbs", "Ecclesiastes", "Song of Solomon", "Isaiah",
    "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea",
    "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum",
    "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi",
    "Matthew", "Mark", "Luke", "John", "Acts", "Romans",
    "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
    "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians",
    "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews",
    "James", "1 Peter", "2 Peter", "1 John", "2 John", "3 John",
    "Jude", "Revelation",
]

TRANSLATIONS = {"NIV", "ESV", "KJV", "NKJV", "NLT", "NASB", "CSB", "RSV", "NRSV",
                "New International Version", "English Standard Version"}

NIV_REF = '\n\nNew International Version Bible. (2011). Zondervan. (Original work published 1978)\n'


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# ── Fix 1: Scripture Citations ───────────────────────────────────────────────

def fix_scripture_citations(text):
    """Add NIV translation to scripture references that don't have one."""
    changes = 0
    book_pattern = "|".join(re.escape(b) for b in BIBLE_BOOKS)
    # Match scripture references like "Proverbs 28:13" or "1 Peter 4:10"
    pattern = rf"(?<!\w)({book_pattern})\s+(\d+[:\d\-,\s]*\d+)"

    lines = text.split("\n")
    new_lines = []
    niv_added_to_refs = False

    for line in lines:
        # Skip code blocks, headings with just the ref, etc.
        if line.strip().startswith("```"):
            new_lines.append(line)
            continue

        # Check if line already has a translation marker near any scripture ref
        new_line = line
        for m in re.finditer(pattern, line):
            ref_text = m.group(0)
            # Check if translation already follows within 30 chars
            after = line[m.end():m.end() + 40]
            before_context = line[max(0, m.start() - 15):m.end() + 40]
            has_trans = any(t in before_context for t in TRANSLATIONS)

            if not has_trans:
                # Add (NIV) after the reference
                # Check what follows: if it's a quote or teaches/says, insert before that
                insert_pos = m.end()

                # Handle common patterns:
                # "Proverbs 28:13 teaches" -> "Proverbs 28:13 (NIV) teaches"
                # "Proverbs 28:13:" -> "Proverbs 28:13 (NIV):"
                # "(Proverbs 28:13)" -> "(Proverbs 28:13, NIV)"

                # Check if ref is inside parentheses
                paren_before = line[max(0, m.start()-2):m.start()]
                paren_after = line[m.end():m.end()+2].strip()

                if "(" in paren_before and paren_after.startswith(")"):
                    # Inside parentheses: add ", NIV" before closing paren
                    new_line = new_line.replace(ref_text + ")", ref_text + ", NIV)", 1)
                    changes += 1
                else:
                    # Not in parens: add (NIV) after reference
                    # But be careful not to double-add
                    if " (NIV)" not in new_line[m.start():m.end()+10]:
                        new_line = new_line[:insert_pos] + " (NIV)" + new_line[insert_pos:]
                        changes += 1

        new_lines.append(new_line)

    result = "\n".join(new_lines)

    # Add NIV to References section if not already there
    if changes > 0 and "New International Version Bible" not in result:
        # Find References section and add NIV entry
        ref_match = re.search(r"^(## References\s*\n)", result, re.MULTILINE)
        if ref_match:
            # Check if there's content after the heading
            after_heading = result[ref_match.end():]
            # Add NIV ref at end of references section
            # Find the next ## heading or end of file
            next_section = re.search(r"\n## ", after_heading)
            if next_section:
                insert_at = ref_match.end() + next_section.start()
                result = result[:insert_at] + NIV_REF + result[insert_at:]
            else:
                # End of file
                result = result.rstrip() + NIV_REF
            niv_added_to_refs = True

    return result, changes


# ── Fix 2: Bold Key Terms on First Use ───────────────────────────────────────

def fix_key_terms_bolding(text):
    """Find terms in Key Terms section and bold their first occurrence in body."""
    changes = 0

    # Extract key terms
    match = re.search(r"^## Key Terms\s*\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    if not match:
        return text, 0

    terms_content = match.group(1)
    terms = re.findall(r"\*\*(.+?)\*\*", terms_content)
    if not terms:
        return text, 0

    # Split into body and non-body sections
    # Body = everything before Key Terms, Knowledge Check, or References
    body_end_patterns = [
        r"^## Key Terms",
        r"^## Knowledge Check",
        r"^## References",
    ]

    # Find earliest section boundary
    body_end = len(text)
    for pat in body_end_patterns:
        m = re.search(pat, text, re.MULTILINE)
        if m and m.start() < body_end:
            body_end = m.start()

    body = text[:body_end]
    rest = text[body_end:]

    # For each term, check if it's already bolded somewhere in body
    for term in terms:
        escaped = re.escape(term)
        # Check if already bolded
        if re.search(rf"\*\*{escaped}\*\*", body):
            continue

        # Find first occurrence in body (case-sensitive)
        # Skip occurrences in headings (lines starting with #)
        # Skip occurrences already inside bold markers
        lines = body.split("\n")
        found = False
        new_body_lines = []
        for line in lines:
            if not found and not line.startswith("#") and not line.startswith("|"):
                # Try exact match first
                idx = line.find(term)
                if idx >= 0:
                    # Make sure we're not inside existing bold markers
                    before = line[:idx]
                    if before.count("**") % 2 == 0:  # Even number = not inside bold
                        line = line[:idx] + "**" + term + "**" + line[idx + len(term):]
                        found = True
                        changes += 1
            new_body_lines.append(line)

        if found:
            body = "\n".join(new_body_lines)

    return body + rest, changes


# ── Main ─────────────────────────────────────────────────────────────────────

def fix_file(filepath, dry_run=False):
    """Apply all fixes to a single file."""
    text = read_file(filepath)
    original = text
    name = Path(filepath).stem
    total_changes = 0

    # Fix 1: Scripture citations
    text, n = fix_scripture_citations(text)
    if n:
        print(f"  [FIX] {name}: Added NIV translation to {n} scripture reference(s)")
        total_changes += n

    # Fix 2: Key terms bolding
    text, n = fix_key_terms_bolding(text)
    if n:
        print(f"  [FIX] {name}: Bolded {n} key term(s) on first use")
        total_changes += n

    if total_changes == 0:
        print(f"  [OK]  {name}: No mechanical fixes needed")

    if not dry_run and text != original:
        write_file(filepath, text)
        print(f"  [SAVE] {name}: {total_changes} fix(es) written")

    return total_changes


def collect_files():
    """Gather all .md files from output directories."""
    files = []
    for d in [CHAPTERS_DIR, TOOLGUIDES_DIR]:
        if d.exists():
            for f in sorted(d.glob("*.md")):
                files.append(f)
    return files


def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args

    if "--file" in args:
        idx = args.index("--file")
        files = [Path(args[idx + 1])]
    else:
        files = collect_files()

    if not files:
        print("No .md files found.")
        sys.exit(1)

    if dry_run:
        print("DRY RUN — no files will be modified\n")

    print(f"Processing {len(files)} file(s)...\n")
    total = 0
    for f in files:
        n = fix_file(f, dry_run)
        total += n

    print(f"\nTotal fixes applied: {total}")
    if dry_run:
        print("(DRY RUN — no files were modified)")


if __name__ == "__main__":
    main()
