#!/usr/bin/env python3
"""
GCU Style Guide Compliance Auditor
Scans .md content files against 12 GCU formatting requirements.
Outputs structured audit results (consumed by gcu_grade_pdf.py).

Usage:
    python tools/gcu_audit.py                  # Audit all output files
    python tools/gcu_audit.py --file <path>    # Audit one file
    python tools/gcu_audit.py --json           # Output JSON for PDF tool
"""

import os
import re
import sys
import json
from pathlib import Path
from datetime import datetime

# ── Configuration ────────────────────────────────────────────────────────────

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

# Words that should NOT be title-cased in headings (APA/standard style)
TITLE_CASE_SMALL = {
    "a", "an", "the", "and", "but", "or", "nor", "for", "yet", "so",
    "in", "on", "at", "to", "by", "of", "up", "as", "is", "it",
    "vs", "vs.", "with", "from", "into", "than", "that",
}

# ── Utility functions ────────────────────────────────────────────────────────

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def get_sections(text):
    """Split markdown into sections by ## headings."""
    parts = re.split(r"^(#{1,6}\s+.+)$", text, flags=re.MULTILINE)
    return parts


def get_body_text(text):
    """Return text excluding Key Terms, Knowledge Check, References sections."""
    lines = text.split("\n")
    body_lines = []
    skip = False
    for line in lines:
        if re.match(r"^##\s+(Key Terms|Knowledge Check|References)", line):
            skip = True
        elif re.match(r"^##\s+", line) and skip:
            skip = False
        if not skip:
            body_lines.append(line)
    return "\n".join(body_lines)


def get_headings(text):
    """Return list of (line_number, level, heading_text) tuples."""
    headings = []
    for i, line in enumerate(text.split("\n"), 1):
        m = re.match(r"^(#{1,6})\s+(.+)$", line)
        if m:
            headings.append((i, len(m.group(1)), m.group(2).strip()))
    return headings


def find_scripture_refs(text):
    """Find scripture references and return list of (line_num, ref_text, has_translation)."""
    refs = []
    book_pattern = "|".join(re.escape(b) for b in BIBLE_BOOKS)
    pattern = rf"(?:{book_pattern})\s+\d+[:\d\-,\s]*"
    for i, line in enumerate(text.split("\n"), 1):
        for m in re.finditer(pattern, line):
            ref_text = m.group(0).strip()
            # Check if translation version follows within 30 chars
            after = line[m.end():m.end()+40]
            has_trans = bool(re.search(
                r"(?:NIV|ESV|KJV|NKJV|NLT|NASB|CSB|RSV|NRSV|New International Version|English Standard Version)",
                after, re.IGNORECASE
            ))
            # Also check parenthetical around the ref
            before_start = max(0, m.start() - 5)
            context = line[before_start:m.end()+40]
            if not has_trans:
                has_trans = bool(re.search(
                    r"(?:NIV|ESV|KJV|NKJV|NLT|NASB|CSB|RSV|NRSV)",
                    context, re.IGNORECASE
                ))
            refs.append((i, ref_text, has_trans))
    return refs


# ── Individual Checks ────────────────────────────────────────────────────────

def check_references_section(text, filename):
    """Check 1: References section exists with APA entries."""
    findings = []
    has_section = bool(re.search(r"^##\s+References\s*$", text, re.MULTILINE))
    if not has_section:
        return "FAIL", ["No ## References section found"], 0

    # Extract references section content
    match = re.search(r"^##\s+References\s*\n(.*?)(?=^##\s|\Z)", text, re.MULTILINE | re.DOTALL)
    if match:
        ref_content = match.group(1).strip()
        if len(ref_content) < 20:
            return "FAIL", ["References section exists but appears empty"], 0
        # Check for APA-like entries (Author, Year pattern)
        apa_entries = re.findall(r"\([12]\d{3}\)", ref_content)
        if len(apa_entries) < 1:
            return "WARN", ["References section exists but no APA-formatted entries detected (Year in parentheses)"], 50
        return "PASS", [f"{len(apa_entries)} APA reference(s) found"], 100

    return "FAIL", ["References section header found but no content follows"], 0


def check_apa_citations(text, filename):
    """Check 2: In-text citations use (Author, Year) format."""
    body = get_body_text(text)
    findings = []

    # Look for APA in-text citations: (Author, Year) or (Author & Author, Year)
    apa_cites = re.findall(r"\([A-Z][a-z]+(?:\s(?:et al\.|&\s[A-Z][a-z]+))?,\s*[12]\d{3}\)", body)

    # Look for common non-APA patterns that suggest missing citations
    # Phrases like "according to David" without (Year)
    uncited = re.findall(r"(?:according to|as [\w]+ (?:argues?|notes?|suggests?|states?))\s+[A-Z][a-z]+(?!\s*\(\d{4})", body, re.IGNORECASE)

    if len(apa_cites) >= 2:
        if uncited:
            return "WARN", [f"{len(apa_cites)} APA citations found, but {len(uncited)} potential uncited author reference(s)"], 75
        return "PASS", [f"{len(apa_cites)} APA in-text citations found"], 100
    elif len(apa_cites) == 1:
        return "WARN", ["Only 1 APA citation found; academic content typically needs more"], 50
    else:
        # Check if there's a References section (might just be missing in-text format)
        if re.search(r"^##\s+References", text, re.MULTILINE):
            return "WARN", ["References section exists but no (Author, Year) in-text citations detected in body"], 25
        return "FAIL", ["No APA in-text citations detected"], 0


def check_scripture_citations(text, filename):
    """Check 3: Scripture citations include translation version."""
    refs = find_scripture_refs(text)
    if not refs:
        return "PASS", ["No scripture references found (N/A)"], 100

    missing = [(ln, ref) for ln, ref, has_t in refs if not has_t]
    total = len(refs)
    with_trans = total - len(missing)

    if not missing:
        return "PASS", [f"All {total} scripture reference(s) include translation version"], 100

    findings = [f"{len(missing)} of {total} scripture ref(s) missing translation version:"]
    for ln, ref in missing[:5]:
        findings.append(f"  Line {ln}: {ref}")
    if len(missing) > 5:
        findings.append(f"  ... and {len(missing) - 5} more")

    score = int((with_trans / total) * 100) if total else 100
    status = "WARN" if score >= 50 else "FAIL"
    return status, findings, score


def check_key_terms_section(text, filename):
    """Check 4: Key Terms section exists."""
    has_section = bool(re.search(r"^##\s+Key Terms\s*$", text, re.MULTILINE))
    if has_section:
        match = re.search(r"^##\s+Key Terms\s*\n(.*?)(?=^##\s|\Z)", text, re.MULTILINE | re.DOTALL)
        if match:
            content = match.group(1).strip()
            bold_terms = re.findall(r"\*\*(.+?)\*\*", content)
            if len(bold_terms) >= 3:
                return "PASS", [f"Key Terms section found with {len(bold_terms)} terms"], 100
            elif len(bold_terms) >= 1:
                return "WARN", [f"Key Terms section found but only {len(bold_terms)} term(s)"], 75
            else:
                return "WARN", ["Key Terms section exists but no bolded terms detected"], 50
    return "FAIL", ["No ## Key Terms section found"], 0


def check_key_terms_bolded(text, filename):
    """Check 5: Key terms are bolded on first use in body."""
    # Extract key terms from Key Terms section
    match = re.search(r"^##\s+Key Terms\s*\n(.*?)(?=^##\s|\Z)", text, re.MULTILINE | re.DOTALL)
    if not match:
        return "PASS", ["No Key Terms section to validate against (N/A)"], 100

    content = match.group(1)
    # Find terms defined in Key Terms: look for **Term**: or - **Term**:
    terms = re.findall(r"\*\*(.+?)\*\*", content)
    if not terms:
        return "PASS", ["No key terms defined to check (N/A)"], 100

    body = get_body_text(text)
    not_bolded = []
    for term in terms:
        escaped = re.escape(term)
        # Check if term appears bolded at least once in body (exact case)
        if re.search(rf"\*\*{escaped}\*\*", body):
            continue
        # Check case-insensitive bolded match
        if re.search(rf"\*\*{escaped}\*\*", body, re.IGNORECASE):
            continue
        # Check if the term (or close variant) appears bolded as part of a larger phrase
        # e.g., Key Term "Weighted Score" might appear in bold as "total weighted score"
        term_words = term.lower().split()
        if len(term_words) >= 2:
            # Check if all words of the term appear in any bolded phrase in body
            body_bolds = re.findall(r"\*\*(.+?)\*\*", body)
            found_in_phrase = False
            for bb in body_bolds:
                bb_lower = bb.lower()
                if all(w in bb_lower for w in term_words):
                    found_in_phrase = True
                    break
            if found_in_phrase:
                continue

        # Check if the term appears anywhere in body (unbolded)
        if re.search(re.escape(term), body, re.IGNORECASE):
            not_bolded.append(term)

    if not not_bolded:
        return "PASS", [f"All {len(terms)} key terms bolded on first use in body"], 100

    score = int(((len(terms) - len(not_bolded)) / len(terms)) * 100)
    findings = [f"{len(not_bolded)} of {len(terms)} key term(s) not bolded in body text:"]
    for t in not_bolded[:5]:
        findings.append(f"  - {t}")
    status = "WARN" if score >= 50 else "FAIL"
    return status, findings, score


def check_headings_no_colons(text, filename):
    """Check 6: Headings don't end with colons or periods."""
    headings = get_headings(text)
    violations = []
    for ln, level, heading in headings:
        clean = heading.rstrip()
        if clean.endswith(":"):
            violations.append((ln, heading, "ends with colon"))
        elif clean.endswith("."):
            violations.append((ln, heading, "ends with period"))

    if not violations:
        return "PASS", [f"All {len(headings)} headings clean (no colons/periods)"], 100

    findings = [f"{len(violations)} heading(s) with trailing punctuation:"]
    for ln, h, issue in violations[:5]:
        findings.append(f"  Line {ln}: \"{h}\" ({issue})")
    score = int(((len(headings) - len(violations)) / max(len(headings), 1)) * 100)
    return "FAIL", findings, score


def check_headings_title_case(text, filename):
    """Check 7: Headings use title case."""
    headings = get_headings(text)
    violations = []
    for ln, level, heading in headings:
        # Skip HTML comments, code-like headings
        if heading.startswith("<!--") or heading.startswith("`"):
            continue
        words = heading.split()
        for i, word in enumerate(words):
            # Strip markdown formatting
            clean = re.sub(r"[*_`\[\](){}]", "", word).strip("—-:,;")
            if not clean or clean.isdigit():
                continue
            if i == 0:
                # First word must always be capitalized
                if clean[0].islower() and clean.lower() not in {"vs", "vs."}:
                    violations.append((ln, heading, f"'{word}' should be capitalized (first word)"))
                    break
            else:
                # Small words can be lowercase unless they're the last word
                if clean.lower() in TITLE_CASE_SMALL and i < len(words) - 1:
                    continue
                if clean[0].islower() and len(clean) > 3:
                    violations.append((ln, heading, f"'{word}' should be capitalized"))
                    break

    if not violations:
        return "PASS", [f"All {len(headings)} headings in title case"], 100

    findings = [f"{len(violations)} heading(s) with title case issues:"]
    for ln, h, issue in violations[:5]:
        findings.append(f"  Line {ln}: \"{h}\" - {issue}")
    score = int(((len(headings) - len(violations)) / max(len(headings), 1)) * 100)
    status = "WARN" if score >= 70 else "FAIL"
    return status, findings, score


def check_emphasis_abuse(text, filename):
    """Check 8: No bold/italic/caps used for emphasis in body (bold only for key terms)."""
    body = get_body_text(text)
    findings = []

    # Extract key terms for cross-reference
    key_terms = []
    kt_match = re.search(r"^##\s+Key Terms\s*\n(.*?)(?=^##\s|\Z)", text, re.MULTILINE | re.DOTALL)
    if kt_match:
        key_terms = re.findall(r"\*\*(.+?)\*\*", kt_match.group(1))
    key_terms_lower = {t.lower() for t in key_terms}

    # Known legitimate acronyms that appear as ALL-CAPS
    KNOWN_ACRONYMS = {
        "PESTEL", "EPSEBIT", "SWOT", "VRIO", "SMART", "QSPM", "SPACE",
        "EBITDA", "GAAP", "IFRS", "NAFTA", "USMCA", "OPEC",
    }

    # Find bold text in body that isn't in a heading, table header, or key term definition context
    lines = body.split("\n")
    suspicious_bold = []
    for i, line in enumerate(lines, 1):
        # Skip headings, table rows, code blocks
        if line.startswith("#") or line.startswith("|") or line.startswith("```"):
            continue
        # Skip lines that are clearly labels/headers (Table X, Figure X, etc.)
        if re.match(r"^\*\*(?:Table|Figure|Equation|Exhibit)\s+\d", line):
            continue
        # Skip Key Terms section definitions
        if re.match(r"^-\s+\*\*", line):
            continue
        # Skip question/answer labels (e.g., **Question 1**, **Mistake 1**)
        if re.match(r"^\*\*(Question|Mistake|Step|Option|Bloom)", line):
            continue

        # Find bold words/phrases that look like emphasis
        bolds = re.findall(r"\*\*(.+?)\*\*", line)
        for b in bolds:
            # Allow: single-word bold (key terms, proper nouns)
            if len(b.split()) <= 1:
                continue

            # Allow: two-word bold starting with capital (proper terms)
            if len(b.split()) <= 2 and b[0].isupper():
                continue

            # Allow: phrases that introduce acronyms e.g. "Financial Position (FP)"
            if re.search(r"\([A-Z]{2,}\)$", b):
                continue

            # Allow: phrases that match or relate to a key term
            if b.lower() in key_terms_lower:
                continue
            # Partial match: bold text contains or is contained by a key term
            is_key_related = False
            for kt in key_terms:
                if kt.lower() in b.lower() or b.lower() in kt.lower():
                    is_key_related = True
                    break
            if is_key_related:
                continue

            # Allow: bold at start of paragraph introducing a topic (functional area style)
            # Pattern: line starts with **Bold Text** followed by descriptive text
            if line.strip().startswith(f"**{b}**") and not b.endswith(":"):
                continue

            # Allow: lowercase multi-word terms that are compound key concepts (e.g., "market growth rate")
            if len(b.split()) <= 3 and b[0].islower():
                # These are often compound key terms being introduced
                continue

            # Flag: bold text ending with colon (emphasis/structural marker)
            if b.rstrip().endswith(":"):
                suspicious_bold.append((i, b[:60]))
                continue

            # Flag multi-word bold (3+ words) that doesn't match any allowed pattern
            if len(b.split()) >= 3:
                suspicious_bold.append((i, b[:60]))

    # Check for ALL CAPS words in body (excluding known acronyms and short acronyms <=6 chars)
    caps_abuse = []
    for i, line in enumerate(lines, 1):
        if line.startswith("#") or line.startswith("|") or line.startswith("```"):
            continue
        words = line.split()
        for w in words:
            clean = re.sub(r"[^A-Za-z]", "", w)
            if clean.isupper() and len(clean) > 6 and clean not in KNOWN_ACRONYMS:
                caps_abuse.append((i, clean))

    total_issues = len(suspicious_bold) + len(caps_abuse)
    if total_issues == 0:
        return "PASS", ["No emphasis abuse detected"], 100

    if suspicious_bold:
        findings.append(f"{len(suspicious_bold)} potential bold emphasis issue(s):")
        for ln, b in suspicious_bold[:3]:
            findings.append(f"  Line {ln}: **{b}**")
    if caps_abuse:
        findings.append(f"{len(caps_abuse)} ALL-CAPS word(s) in body:")
        for ln, w in caps_abuse[:3]:
            findings.append(f"  Line {ln}: {w}")

    score = max(0, 100 - total_issues * 10)
    status = "WARN" if score >= 50 else "FAIL"
    return status, findings, score


def check_table_figure_numbering(text, filename):
    """Check 9: Tables/figures use GCU format (bold number + italic title, no periods)."""
    findings = []
    violations = []

    # Find table/figure references
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Pattern: **Table X.Y** or **Figure X.Y** (correct GCU format)
        gcu_match = re.match(r"^\*\*(?:Table|Figure)\s+\d+(?:\.\d+)?\*\*\s*$", line)

        # Pattern: Table X / Figure X without bold or with period
        plain_match = re.match(r"^(?:\*\*)?(?:Table|Figure)\s+\d+(?:\.\d+)?(?:\*\*)?\s*\.?\s*$", line)

        # Pattern with inline title (not GCU compliant — title should be on next line)
        inline_match = re.match(r"^(?:\*\*)?(?:Table|Figure)\s+\d+(?:\.\d+)?(?:\*\*)?\s*[:\.]?\s*\S", line)

        if gcu_match:
            # Check next line for italic title
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line.startswith("*") and not next_line.startswith("**"):
                    # Italic title — check no period at end
                    if next_line.rstrip("*").endswith("."):
                        violations.append((i + 2, f"Title ends with period: {next_line}"))
                else:
                    if next_line and not next_line.startswith("|") and not next_line.startswith("```"):
                        violations.append((i + 2, f"Expected italic title after figure/table number, got: {next_line[:50]}"))
        elif inline_match and not gcu_match:
            violations.append((i + 1, f"Non-GCU format (number and title on same line): {line[:60]}"))
        elif plain_match and not gcu_match:
            if "**" not in line:
                violations.append((i + 1, f"Figure/table number not bolded: {line[:60]}"))

        i += 1

    # Count total tables/figures
    total = len(re.findall(r"(?:Table|Figure)\s+\d+", text))
    if total == 0:
        return "PASS", ["No tables or figures found (N/A)"], 100

    if not violations:
        return "PASS", [f"All {total} table/figure reference(s) use GCU format"], 100

    findings = [f"{len(violations)} table/figure formatting issue(s):"]
    for ln, issue in violations[:5]:
        findings.append(f"  Line {ln}: {issue}")
    score = int(((total - len(violations)) / max(total, 1)) * 100)
    status = "WARN" if score >= 50 else "FAIL"
    return status, findings, score


def check_no_external_links(text, filename):
    """Check 10 & 12: No external hyperlinks in body text."""
    body = get_body_text(text)
    findings = []

    # Find URLs
    urls = re.findall(r"https?://[^\s\)]+", body)
    # Filter out markdown reference-style links that might be in footnotes
    # Also allow URLs inside code blocks
    in_code = False
    real_urls = []
    for line in body.split("\n"):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        for url in re.findall(r"https?://[^\s\)]+", line):
            real_urls.append(url)

    if not real_urls:
        return "PASS", ["No external hyperlinks in body text"], 100

    findings = [f"{len(real_urls)} external URL(s) found in body text:"]
    for url in real_urls[:5]:
        findings.append(f"  {url[:80]}")
    return "FAIL", findings, 0


def check_block_quotes(text, filename):
    """Check 11: Any 40+ word direct quotes use block format."""
    # Look for quoted text over 40 words
    # Pattern: text within quotation marks
    long_quotes = []
    for i, line in enumerate(text.split("\n"), 1):
        # Find text in double quotes
        for m in re.finditer(r'"([^"]{200,})"', line):
            word_count = len(m.group(1).split())
            if word_count >= 40:
                long_quotes.append((i, word_count, m.group(1)[:60]))

    if not long_quotes:
        return "PASS", ["No 40+ word inline quotes found"], 100

    findings = [f"{len(long_quotes)} long quote(s) should be in block format:"]
    for ln, wc, preview in long_quotes[:3]:
        findings.append(f"  Line {ln}: {wc} words - \"{preview}...\"")
    return "WARN", findings, 50


# ── Main Audit Runner ────────────────────────────────────────────────────────

ALL_CHECKS = [
    ("References Section Exists", check_references_section),
    ("APA Citation Format", check_apa_citations),
    ("Scripture Citations Include Translation", check_scripture_citations),
    ("Key Terms Section Exists", check_key_terms_section),
    ("Key Terms Bolded on First Use", check_key_terms_bolded),
    ("Headings: No Colons or Periods", check_headings_no_colons),
    ("Headings: Title Case", check_headings_title_case),
    ("No Emphasis Abuse", check_emphasis_abuse),
    ("Table/Figure Numbering (GCU Format)", check_table_figure_numbering),
    ("No External Hyperlinks in Body", check_no_external_links),
    ("Block Quotes Formatted", check_block_quotes),
]


def audit_file(filepath):
    """Run all checks on a single file. Returns dict of results."""
    text = read_file(filepath)
    name = Path(filepath).stem
    content_type = "Chapter" if "chapter" in str(filepath).lower() or "topic" in name.lower() else "Tool Guide"

    results = {
        "filename": name,
        "filepath": str(filepath),
        "content_type": content_type,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "checks": [],
        "overall_score": 0,
        "overall_status": "",
    }

    total_score = 0
    statuses = []

    for check_name, check_fn in ALL_CHECKS:
        status, findings, score = check_fn(text, name)
        results["checks"].append({
            "name": check_name,
            "status": status,
            "score": score,
            "findings": findings,
        })
        total_score += score
        statuses.append(status)

    results["overall_score"] = round(total_score / len(ALL_CHECKS), 1)

    if all(s == "PASS" for s in statuses):
        results["overall_status"] = "COMPLIANT"
    elif any(s == "FAIL" for s in statuses):
        fail_count = statuses.count("FAIL")
        results["overall_status"] = "MAJOR REVISION" if fail_count >= 3 else "NEEDS REVISION"
    else:
        results["overall_status"] = "MINOR REVISION"

    return results


def collect_files():
    """Gather all .md files from output directories."""
    files = []
    for d in [CHAPTERS_DIR, TOOLGUIDES_DIR]:
        if d.exists():
            for f in sorted(d.glob("*.md")):
                files.append(f)
    return files


def print_summary(all_results):
    """Print a console summary table."""
    print("\n" + "=" * 90)
    print("GCU COMPLIANCE AUDIT SUMMARY")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 90)
    print(f"{'File':<50} {'Type':<12} {'Score':>6}  {'Status'}")
    print("-" * 90)
    for r in all_results:
        print(f"{r['filename']:<50} {r['content_type']:<12} {r['overall_score']:>5.1f}%  {r['overall_status']}")
    print("-" * 90)

    avg = sum(r["overall_score"] for r in all_results) / len(all_results)
    compliant = sum(1 for r in all_results if r["overall_status"] == "COMPLIANT")
    print(f"{'AVERAGE':<50} {'':12} {avg:>5.1f}%  {compliant}/{len(all_results)} compliant")
    print("=" * 90)


def main():
    args = sys.argv[1:]
    output_json = "--json" in args

    if "--file" in args:
        idx = args.index("--file")
        filepath = Path(args[idx + 1])
        files = [filepath]
    else:
        files = collect_files()

    if not files:
        print("No .md files found in output directories.")
        sys.exit(1)

    all_results = []
    for f in files:
        result = audit_file(f)
        all_results.append(result)

    if output_json:
        print(json.dumps(all_results, indent=2))
    else:
        print_summary(all_results)

        # Also print details for non-compliant files
        for r in all_results:
            if r["overall_status"] != "COMPLIANT":
                print(f"\n--- {r['filename']} ({r['overall_status']}) ---")
                for c in r["checks"]:
                    if c["status"] != "PASS":
                        print(f"  [{c['status']}] {c['name']} ({c['score']}%)")
                        for f in c["findings"]:
                            print(f"    {f}")

    # Save JSON for PDF generator
    json_path = BASE / "output" / "qr-grades" / "audit_results.json"
    json_path.parent.mkdir(parents=True, exist_ok=True)
    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(all_results, jf, indent=2)
    if not output_json:
        print(f"\nAudit results saved to: {json_path}")

    return all_results


if __name__ == "__main__":
    main()
