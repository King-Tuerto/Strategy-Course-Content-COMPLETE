#!/usr/bin/env python3
"""
GCU Style Fix Tool v2 — Comprehensive Compliance Fixer
Applies all remaining formatting fixes to .md content files.

Fixes applied:
1. Bold emphasis abuse — unbolding structural/emphasis bold that isn't key terms
2. Key Terms bolded on first use (case-insensitive matching)
3. APA in-text citations — adds (Author, Year) format where references are discussed
4. Block quotes — converts 40+ word inline quotes to block format

Usage:
    python tools/gcu_fix_v2.py                    # Fix all output files
    python tools/gcu_fix_v2.py --dry-run          # Show changes without writing
    python tools/gcu_fix_v2.py --file <path>      # Fix one file
"""

import os
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


def get_key_terms(text):
    """Extract key terms from Key Terms section."""
    match = re.search(r"^## Key Terms\s*\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    if not match:
        return []
    content = match.group(1)
    terms = re.findall(r"\*\*(.+?)\*\*", content)
    return terms


def get_body_text_range(text):
    """Return (start, end) indices for body text (excluding Key Terms, Knowledge Check, References)."""
    end_patterns = [
        r"^## Key Terms",
        r"^## Knowledge Check",
        r"^## References",
    ]
    body_end = len(text)
    for pat in end_patterns:
        m = re.search(pat, text, re.MULTILINE)
        if m and m.start() < body_end:
            body_end = m.start()
    return 0, body_end


def extract_references(text):
    """Extract reference entries from References section.
    Returns list of dicts with author, year, title info."""
    match = re.search(r"^## References\s*\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    if not match:
        return []

    refs = []
    ref_text = match.group(1)

    # Parse APA-style references: Author, A. B. (Year). Title...
    # Pattern: captures author surname(s) and year
    for line in ref_text.split("\n"):
        line = line.strip().lstrip("- ")
        if not line or line.startswith("#"):
            continue

        # Try to extract author surname and year
        # Common patterns:
        # David, F. R., & David, F. R. (2017).
        # Porter, M. E. (1980).
        # New International Version Bible. (2011).
        m = re.match(r"^([A-Z][a-z]+(?:\s+(?:&|and)\s+[A-Z][a-z]+)?)[^(]*\((\d{4})\)", line)
        if m:
            author = m.group(1).strip()
            year = m.group(2)
            refs.append({"author": author, "year": year, "full_line": line})
            continue

        # Try: Author, I. I. (Year)
        m = re.match(r"^([A-Z][a-z]+),\s+[A-Z]\.\s*[A-Z]?\.\s*(?:,\s*(?:&|and)\s+([A-Z][a-z]+))?\s*[^(]*\((\d{4})\)", line)
        if m:
            author1 = m.group(1)
            author2 = m.group(2)
            year = m.group(3)
            if author2:
                author = f"{author1} & {author2}"
            else:
                author = author1
            refs.append({"author": author, "year": year, "full_line": line})

    return refs


# ── Fix 1: Bold Emphasis Abuse ──────────────────────────────────────────────

def fix_emphasis_abuse(text):
    """Remove bold from multi-word phrases that are emphasis, not key terms.

    Keep bold on:
    - Key terms on first use (2+ word terms from Key Terms section)
    - Single-word functional area names at start of paragraphs (Management, Marketing, etc.)
    - Terms that introduce acronyms: **Resource-Based View (RBV)**
    - Table/Figure labels
    - Question/Step/Mistake labels

    Remove bold from:
    - Multi-word bold phrases followed by colons (emphasis structure markers)
    - Bold phrases that are clearly used for emphasis rather than term introduction
    - ALL-CAPS words > 5 chars (convert to normal case if appropriate)
    """
    key_terms = get_key_terms(text)
    key_terms_lower = {t.lower() for t in key_terms}
    body_start, body_end = get_body_text_range(text)

    changes = 0
    lines = text.split("\n")
    new_lines = []
    in_code = False
    in_back_section = False

    for i, line in enumerate(lines):
        # Track code blocks
        if line.strip().startswith("```"):
            in_code = not in_code
            new_lines.append(line)
            continue
        if in_code:
            new_lines.append(line)
            continue

        # Track if we're past body into Key Terms / Knowledge Check / References
        if re.match(r"^## (Key Terms|Knowledge Check|References)", line):
            in_back_section = True
        elif re.match(r"^## ", line) and in_back_section:
            # Could be back in body (unlikely but handle)
            pass

        if in_back_section:
            new_lines.append(line)
            continue

        # Skip headings, table rows
        if line.startswith("#") or line.startswith("|"):
            new_lines.append(line)
            continue

        # Skip Table/Figure labels, Key Term definitions, Question labels
        if re.match(r"^\*\*(?:Table|Figure|Equation|Exhibit)\s+\d", line):
            new_lines.append(line)
            continue
        if re.match(r"^-\s+\*\*", line):
            new_lines.append(line)
            continue
        if re.match(r"^\*\*(Question|Mistake|Step|Option|Bloom)", line):
            new_lines.append(line)
            continue

        # Find all bold phrases in this line
        new_line = line
        offset = 0
        for m in re.finditer(r"\*\*(.+?)\*\*", line):
            bold_text = m.group(1)
            words = bold_text.split()

            # Skip single-word bold (generally acceptable for key terms)
            if len(words) <= 1:
                continue

            # Skip two-word bold that starts with capital (likely a proper term)
            if len(words) == 2 and words[0][0].isupper():
                # But check if it ends with colon - that's emphasis
                if bold_text.rstrip().endswith(":"):
                    pass  # Will be handled below
                else:
                    continue

            # Check if this is a key term from Key Terms section
            if bold_text.lower() in key_terms_lower:
                continue

            # Check if it introduces an acronym like "Resource-Based View (RBV)"
            if re.search(r"\([A-Z]{2,}\)$", bold_text):
                continue

            # Check if it's a known functional area name at paragraph start
            functional_areas = [
                "Finance and Accounting", "Production and Operations",
                "Research and Development", "Management Information Systems",
                "Research and Development (R&D)", "Management Information Systems (MIS)",
            ]
            if bold_text in functional_areas:
                continue

            # --- Cases to UNBOLD ---

            # Bold text ending with colon is emphasis structure: **When SO strategies dominate:**
            if bold_text.rstrip().endswith(":"):
                start = m.start() + offset
                end = m.end() + offset
                replacement = bold_text  # Just remove the **...**
                new_line = new_line[:start] + replacement + new_line[end:]
                offset += len(replacement) - (end - start)
                changes += 1
                continue

            # Multi-word bold (3+ words) that's not a key term and doesn't introduce an acronym
            if len(words) >= 3:
                # Check if it matches any key term (case-insensitive partial)
                is_key_related = False
                for kt in key_terms:
                    if kt.lower() in bold_text.lower() or bold_text.lower() in kt.lower():
                        is_key_related = True
                        break

                if not is_key_related:
                    start = m.start() + offset
                    end = m.end() + offset
                    replacement = bold_text
                    new_line = new_line[:start] + replacement + new_line[end:]
                    offset += len(replacement) - (end - start)
                    changes += 1

        new_lines.append(new_line)

    return "\n".join(new_lines), changes


# ── Fix 2: Key Terms Bolding (case-insensitive) ─────────────────────────────

def fix_key_terms_bolding_v2(text):
    """Bold key terms on first use in body text using case-insensitive matching."""
    changes = 0
    key_terms = get_key_terms(text)
    if not key_terms:
        return text, 0

    body_start, body_end = get_body_text_range(text)
    body = text[:body_end]
    rest = text[body_end:]

    for term in key_terms:
        escaped = re.escape(term)

        # Check if already bolded anywhere in body (exact case)
        if re.search(rf"\*\*{escaped}\*\*", body):
            continue

        # Check case-insensitive: is the exact form bolded?
        if re.search(rf"\*\*{escaped}\*\*", body, re.IGNORECASE):
            continue

        # Find first occurrence in body (case-insensitive)
        # Must be on word boundaries to avoid partial matches
        pattern = rf"(?<![*\w])({re.escape(term)})(?![*\w])"

        lines = body.split("\n")
        found = False
        new_body_lines = []

        for line in lines:
            if not found and not line.startswith("#") and not line.startswith("|") and not line.startswith("```"):
                # Case-insensitive search
                m = re.search(pattern, line, re.IGNORECASE)
                if m:
                    # Make sure we're not inside existing bold markers
                    before = line[:m.start()]
                    if before.count("**") % 2 == 0:
                        actual_text = m.group(1)
                        line = line[:m.start()] + "**" + actual_text + "**" + line[m.end():]
                        found = True
                        changes += 1
            new_body_lines.append(line)

        if found:
            body = "\n".join(new_body_lines)

    return body + rest, changes


# ── Fix 3: APA In-Text Citations ─────────────────────────────────────────────

def fix_apa_citations(text):
    """Add (Author, Year) in-text citations where authors from References are mentioned.

    Strategy: For each reference author, find mentions of their name in body text
    and add the (Author, Year) citation if not already present.
    """
    refs = extract_references(text)
    if not refs:
        return text, 0

    body_start, body_end = get_body_text_range(text)
    body = text[:body_end]
    rest = text[body_end:]
    changes = 0

    # Skip Bible references — those use scripture citation format
    refs = [r for r in refs if "Bible" not in r.get("full_line", "")
            and "International Version" not in r.get("author", "")]

    for ref in refs:
        author = ref["author"]
        year = ref["year"]

        # Get primary author surname
        primary_surname = author.split(",")[0].split("&")[0].strip().split()[-1] if author else ""
        if not primary_surname or len(primary_surname) < 3:
            continue

        # Check if (Author, Year) already exists in body
        cite_pattern = rf"\({re.escape(primary_surname)}.*?,\s*{re.escape(year)}\)"
        if re.search(cite_pattern, body):
            continue

        # Build the citation string
        if "&" in author:
            # Two authors: (David & David, 2017)
            parts = [a.strip() for a in author.split("&")]
            cite_str = f"({parts[0]} & {parts[1]}, {year})"
        else:
            cite_str = f"({primary_surname}, {year})"

        # Find where the author's work is discussed in body
        # Look for patterns like:
        # "According to David" / "David argues" / "David (2017)" / "David's model"
        # Or references to the framework/concept from that source

        # First try: direct author name mention
        name_pattern = rf"(?<![A-Za-z])({re.escape(primary_surname)})(?!\s*[,&]\s*[A-Z])(?!\s*\(\d{{4}}\))(?![A-Za-z])"

        lines = body.split("\n")
        found = False
        new_body_lines = []

        for line in lines:
            if not found and not line.startswith("#") and not line.startswith("|") and not line.startswith("```"):
                m = re.search(name_pattern, line)
                if m:
                    # Check if citation already follows
                    after = line[m.end():m.end()+30]
                    if not re.search(rf"\(\d{{4}}\)", after) and not re.search(rf"{re.escape(year)}", after):
                        # Add citation after the surname
                        insert_pos = m.end()
                        line = line[:insert_pos] + f" {cite_str}" + line[insert_pos:]
                        found = True
                        changes += 1
            new_body_lines.append(line)

        if found:
            body = "\n".join(new_body_lines)

    return body + rest, changes


# ── Fix 4: Block Quotes ─────────────────────────────────────────────────────

def fix_block_quotes(text):
    """Convert 40+ word inline quotes to block quote format."""
    changes = 0
    lines = text.split("\n")
    new_lines = []
    in_code = False

    for i, line in enumerate(lines):
        if line.strip().startswith("```"):
            in_code = not in_code
            new_lines.append(line)
            continue
        if in_code:
            new_lines.append(line)
            continue

        # Find long quotes in double quotes
        matches = list(re.finditer(r'"([^"]{200,})"', line))
        if not matches:
            new_lines.append(line)
            continue

        for m in matches:
            quote_text = m.group(1)
            word_count = len(quote_text.split())
            if word_count >= 40:
                # This is a long quote that should be block format
                # Extract the text before and after the quote
                before = line[:m.start()].rstrip()
                after = line[m.end():].strip()

                # Build block quote
                if before:
                    new_lines.append(before)
                new_lines.append("")
                # Wrap the quote text into block format (> prefix)
                # Split into ~80 char lines for readability
                words = quote_text.split()
                current_line = "> "
                for word in words:
                    if len(current_line) + len(word) + 1 > 80:
                        new_lines.append(current_line)
                        current_line = "> " + word
                    else:
                        if current_line == "> ":
                            current_line += word
                        else:
                            current_line += " " + word
                if current_line.strip() != ">":
                    new_lines.append(current_line)

                new_lines.append("")
                if after:
                    new_lines.append(after)

                changes += 1
                # Don't add the original line
                break
        else:
            new_lines.append(line)

    return "\n".join(new_lines), changes


# ── Main ─────────────────────────────────────────────────────────────────────

def fix_file(filepath, dry_run=False):
    """Apply all v2 fixes to a single file."""
    text = read_file(filepath)
    original = text
    name = Path(filepath).stem
    total_changes = 0

    # Fix 1: Emphasis abuse
    text, n = fix_emphasis_abuse(text)
    if n:
        print(f"  [FIX] {name}: Removed {n} emphasis-style bold(s)")
        total_changes += n

    # Fix 2: Key terms bolding (case-insensitive)
    text, n = fix_key_terms_bolding_v2(text)
    if n:
        print(f"  [FIX] {name}: Bolded {n} key term(s) on first use (case-insensitive)")
        total_changes += n

    # Fix 3: APA in-text citations
    text, n = fix_apa_citations(text)
    if n:
        print(f"  [FIX] {name}: Added {n} APA in-text citation(s)")
        total_changes += n

    # Fix 4: Block quotes
    text, n = fix_block_quotes(text)
    if n:
        print(f"  [FIX] {name}: Converted {n} long quote(s) to block format")
        total_changes += n

    if total_changes == 0:
        print(f"  [OK]  {name}: No additional fixes needed")

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
