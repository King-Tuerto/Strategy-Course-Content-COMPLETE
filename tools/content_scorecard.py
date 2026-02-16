"""
Content Scorecard Generator
============================
Scans all .md files in output/ and produces a scorecard report showing:
  - Body word count (excluding Key Terms, Knowledge Check, References)
  - Biblical/Scripture references found
  - Flesch-Kincaid Grade Level and Reading Ease
  - Target F-K compliance status
  - CWV Level (explicit metadata or estimated from content)

Usage:
    python tools/content_scorecard.py

Output:
    Prints scorecard table to console
    Saves full report to output/SCORECARD.md

Requires: pip install textstat

CWV Metadata Tag:
    To set CWV level explicitly, include this line anywhere in the .md file:
    <!-- CWV: 4 -->
    If no tag is found, the tool estimates CWV from scripture count and
    faith-language density.
"""

import os
import re
import sys
from datetime import datetime

try:
    import textstat
except ImportError:
    print("ERROR: textstat not installed. Run: pip install textstat")
    sys.exit(1)

# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")
SCORECARD_PATH = os.path.join(OUTPUT_DIR, "SCORECARD.md")

FK_TARGET_MIN = 16
FK_TARGET_MAX = 18

# Scripture detection pattern (handles 1/2/3 Book format)
SCRIPTURE_RE = re.compile(
    r'(?:1\s+|2\s+|3\s+)?'
    r'(?:Genesis|Exodus|Leviticus|Numbers|Deuteronomy|Joshua|Judges|Ruth|'
    r'Samuel|Kings|Chronicles|Ezra|Nehemiah|Esther|Job|Psalms?|Proverbs|'
    r'Ecclesiastes|Song|Isaiah|Jeremiah|Lamentations|Ezekiel|Daniel|'
    r'Hosea|Joel|Amos|Obadiah|Jonah|Micah|Nahum|Habakkuk|Zephaniah|'
    r'Haggai|Zechariah|Malachi|Matthew|Mark|Luke|John|Acts|Romans|'
    r'Corinthians|Galatians|Ephesians|Philippians|Colossians|'
    r'Thessalonians|Timothy|Titus|Philemon|Hebrews|James|Peter|'
    r'Jude|Revelation)\s+\d+[:\d\-]+',
    re.IGNORECASE
)

# CWV metadata tag pattern: <!-- CWV: 4 -->
CWV_TAG_RE = re.compile(r'<!--\s*CWV:\s*(\d+)\s*-->')

# Faith language indicators for CWV estimation
FAITH_WORDS = [
    "stewardship", "steward", "faithful", "faithfulness", "entrusted",
    "calling", "vocation", "scripture", "biblical", "christian",
    "god", "lord", "kingdom", "gospel", "prayer", "worship",
    "redemption", "grace", "mercy", "sin", "righteousness",
    "wisdom", "discernment", "providence", "covenant",
    "parable", "apostle", "discipleship", "ministry",
]


def find_md_files(root_dir):
    """Recursively find all .md files, skipping temp files."""
    files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in sorted(filenames):
            if f.endswith(".md") and not f.startswith("~$") and f != "SCORECARD.md":
                files.append(os.path.join(dirpath, f))
    return files


def extract_body(text):
    """Return body text only — everything before Key Terms or Knowledge Check,
    whichever comes first."""
    key_terms_pos = text.find("## Key Terms")
    knowledge_check_pos = text.find("## Knowledge Check")

    cutoffs = [pos for pos in [key_terms_pos, knowledge_check_pos] if pos != -1]
    if cutoffs:
        body = text[:min(cutoffs)]
    else:
        body = text

    return body.strip()


def detect_content_type(filepath, text):
    """Determine content type from path and content."""
    rel = filepath.lower()
    if "tool-guides" in rel or "tool_guides" in rel:
        return "Tool Guide"
    elif "chapters" in rel:
        return "Chapter"
    elif "cases" in rel:
        return "Case Study"
    elif "handouts" in rel:
        return "Handout"
    else:
        return "Other"


def get_cwv_explicit(text):
    """Look for explicit CWV metadata tag: <!-- CWV: N -->"""
    match = CWV_TAG_RE.search(text)
    if match:
        val = int(match.group(1))
        return min(max(val, 0), 10)  # clamp 0-10
    return None


def estimate_cwv(text, scripture_count, body_words):
    """Estimate CWV level from content when no explicit tag exists.

    Heuristic based on:
    - Number of scripture references
    - Density of faith-language words
    - Presence of dedicated biblical integration section
    """
    if body_words == 0:
        return 0

    # Count faith words (case-insensitive, whole-word-ish)
    text_lower = text.lower()
    faith_count = 0
    for word in FAITH_WORDS:
        faith_count += len(re.findall(r'\b' + re.escape(word) + r'\b', text_lower))

    # Faith density per 1000 words
    faith_density = (faith_count / body_words) * 1000

    # Has dedicated biblical section?
    has_bible_section = bool(re.search(
        r'##\s*(biblical\s+integration|a\s+note\s+on\s+stewardship|'
        r'ethical\s+considerations|faith\s+and\s+practice)',
        text, re.IGNORECASE
    ))

    # Estimation logic
    if scripture_count == 0 and faith_density < 1:
        return 0
    elif scripture_count == 0 and faith_density < 3:
        return 1
    elif scripture_count == 0 and faith_density >= 3:
        return 2
    elif scripture_count == 1 and not has_bible_section:
        return 3
    elif scripture_count == 1 and has_bible_section:
        return 4
    elif scripture_count == 2 and faith_density < 8:
        return 5
    elif scripture_count == 2 and faith_density >= 8:
        return 6
    elif scripture_count == 3:
        return 7
    elif scripture_count >= 4 and faith_density < 15:
        return 8
    elif scripture_count >= 4 and faith_density >= 15:
        return 9
    else:
        return 4  # default fallback


def analyze_file(filepath):
    """Analyze a single .md file and return metrics dict."""
    with open(filepath, "r", encoding="utf-8") as f:
        full_text = f.read()

    filename = os.path.basename(filepath)
    content_type = detect_content_type(filepath, full_text)

    # Body text (excludes glossary, questions, references)
    body = extract_body(full_text)
    body_words = len(body.split())

    # F-K metrics on body text only
    if body_words > 30:
        fk_grade = round(textstat.flesch_kincaid_grade(body), 1)
        fk_ease = round(textstat.flesch_reading_ease(body), 1)
    else:
        fk_grade = 0.0
        fk_ease = 0.0

    # Scripture references (search full text)
    scripture_full = re.findall(
        r'(?:1\s+|2\s+|3\s+)?'
        r'(?:Genesis|Exodus|Leviticus|Numbers|Deuteronomy|Joshua|Judges|Ruth|'
        r'Samuel|Kings|Chronicles|Ezra|Nehemiah|Esther|Job|Psalms?|Proverbs|'
        r'Ecclesiastes|Song|Isaiah|Jeremiah|Lamentations|Ezekiel|Daniel|'
        r'Hosea|Joel|Amos|Obadiah|Jonah|Micah|Nahum|Habakkuk|Zephaniah|'
        r'Haggai|Zechariah|Malachi|Matthew|Mark|Luke|John|Acts|Romans|'
        r'Corinthians|Galatians|Ephesians|Philippians|Colossians|'
        r'Thessalonians|Timothy|Titus|Philemon|Hebrews|James|Peter|'
        r'Jude|Revelation)\s+\d+[:\d\-]+',
        full_text, re.IGNORECASE
    )
    # Deduplicate within file
    seen = set()
    unique_scriptures = []
    for s in scripture_full:
        s_clean = s.strip()
        if s_clean not in seen:
            seen.add(s_clean)
            unique_scriptures.append(s_clean)

    # CWV level — explicit tag or estimated
    cwv_explicit = get_cwv_explicit(full_text)
    if cwv_explicit is not None:
        cwv_level = cwv_explicit
        cwv_source = "set"
    else:
        cwv_level = estimate_cwv(full_text, len(unique_scriptures), body_words)
        cwv_source = "est"

    # F-K target compliance
    if fk_grade >= FK_TARGET_MIN and fk_grade <= FK_TARGET_MAX:
        fk_status = "On Target"
    elif fk_grade > FK_TARGET_MAX:
        fk_status = "Above Target"
    elif fk_grade >= FK_TARGET_MIN - 2:
        fk_status = "Near Target"
    else:
        fk_status = "Below Target"

    return {
        "filename": filename,
        "content_type": content_type,
        "body_words": body_words,
        "fk_grade": fk_grade,
        "fk_ease": fk_ease,
        "fk_status": fk_status,
        "scriptures": unique_scriptures,
        "cwv_level": cwv_level,
        "cwv_source": cwv_source,
    }


def generate_report(results):
    """Generate the SCORECARD.md content."""
    now = datetime.now().strftime("%B %d, %Y at %I:%M %p")

    # CWV level labels
    cwv_labels = {
        0: "Secular", 1: "Trace", 2: "Subtle", 3: "Light Touch",
        4: "Natural", 5: "Moderate", 6: "Engaged", 7: "Prominent",
        8: "Strong", 9: "Pervasive", 10: "Maximum"
    }

    lines = []
    lines.append("# Content Scorecard")
    lines.append("")
    lines.append(f"Generated: {now}")
    lines.append(f"F-K Target: {FK_TARGET_MIN}-{FK_TARGET_MAX}")
    lines.append(f"CWV Default: 4 (Natural)")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Main scorecard table
    lines.append("## Scorecard")
    lines.append("")
    lines.append("| Content | Type | Body Words | F-K Grade | F-K Status | CWV | Scripture |")
    lines.append("|---------|------|-----------|-----------|------------|-----|-----------|")

    total_words = 0
    all_scriptures = []
    fk_grades = []
    cwv_levels = []

    for r in results:
        scripture_str = ", ".join(r["scriptures"]) if r["scriptures"] else "None"
        cwv_display = f"{r['cwv_level']} ({cwv_labels.get(r['cwv_level'], '?')})"
        if r["cwv_source"] == "est":
            cwv_display += "*"

        lines.append(
            f"| {r['filename'].replace('.md','')} "
            f"| {r['content_type']} "
            f"| {r['body_words']:,} "
            f"| {r['fk_grade']} "
            f"| {r['fk_status']} "
            f"| {cwv_display} "
            f"| {scripture_str} |"
        )
        total_words += r["body_words"]
        all_scriptures.extend(r["scriptures"])
        if r["fk_grade"] > 0:
            fk_grades.append(r["fk_grade"])
        cwv_levels.append(r["cwv_level"])

    lines.append("")
    lines.append("*\\* = estimated from content (no explicit `<!-- CWV: N -->` tag found)*")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Aggregate stats
    avg_fk = round(sum(fk_grades) / len(fk_grades), 1) if fk_grades else 0
    avg_cwv = round(sum(cwv_levels) / len(cwv_levels), 1) if cwv_levels else 0
    unique_scripture_count = len(set(all_scriptures))
    on_target = sum(1 for r in results if r["fk_status"] == "On Target")
    above = sum(1 for r in results if r["fk_status"] == "Above Target")
    near = sum(1 for r in results if r["fk_status"] == "Near Target")
    below = sum(1 for r in results if r["fk_status"] == "Below Target")

    lines.append("## Summary Statistics")
    lines.append("")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Total Content Pieces | {len(results)} |")
    lines.append(f"| Total Body Words | {total_words:,} |")
    lines.append(f"| Average F-K Grade Level | {avg_fk} |")
    lines.append(f"| F-K Target Range | {FK_TARGET_MIN}-{FK_TARGET_MAX} |")
    lines.append(f"| On Target | {on_target} of {len(results)} |")
    lines.append(f"| Above Target | {above} |")
    lines.append(f"| Near Target (within 2 grades) | {near} |")
    lines.append(f"| Below Target | {below} |")
    lines.append(f"| Average CWV Level | {avg_cwv} |")
    lines.append(f"| CWV Range | {min(cwv_levels)}-{max(cwv_levels)} |")
    lines.append(f"| Unique Scripture References | {unique_scripture_count} |")
    lines.append(f"| Scripture Duplicates | {'None' if unique_scripture_count == len(all_scriptures) else 'DUPLICATES DETECTED'} |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Scripture tracker
    lines.append("## Scripture Reference Tracker")
    lines.append("")
    lines.append("| Scripture | Used In |")
    lines.append("|-----------|---------|")

    scripture_map = {}
    for r in results:
        for s in r["scriptures"]:
            if s not in scripture_map:
                scripture_map[s] = []
            scripture_map[s].append(r["filename"].replace(".md", ""))

    for scripture, files in sorted(scripture_map.items()):
        status = " **DUPLICATE**" if len(files) > 1 else ""
        lines.append(f"| {scripture} | {', '.join(files)}{status} |")

    lines.append("")
    lines.append("---")
    lines.append("")

    # CWV distribution
    lines.append("## CWV Level Distribution")
    lines.append("")
    lines.append("| CWV Level | Label | Count |")
    lines.append("|-----------|-------|-------|")
    cwv_counts = {}
    for level in cwv_levels:
        cwv_counts[level] = cwv_counts.get(level, 0) + 1
    for level in sorted(cwv_counts.keys()):
        lines.append(f"| {level} | {cwv_labels.get(level, '?')} | {cwv_counts[level]} |")

    lines.append("")
    lines.append("---")
    lines.append("")

    # F-K observations
    lines.append("## F-K Grade Level Observations")
    lines.append("")
    if below > 0:
        below_items = [r for r in results if r["fk_status"] == "Below Target"]
        lines.append(f"**{below} piece(s) below target range:**")
        for r in below_items:
            gap = FK_TARGET_MIN - r["fk_grade"]
            lines.append(f"- {r['filename'].replace('.md','')}: F-K {r['fk_grade']} ({gap:.1f} grades below minimum)")
        lines.append("")
        lines.append("Tool guides typically score lower than chapters because they use shorter, procedural sentences. ")
        lines.append("Consider whether the F-K target should differ by content type (e.g., 12-14 for tool guides, 16-18 for chapters).")
    else:
        lines.append("All content is within or above the target F-K range.")

    lines.append("")

    return "\n".join(lines)


def main():
    if not os.path.isdir(OUTPUT_DIR):
        print(f"ERROR: Output directory not found: {OUTPUT_DIR}")
        sys.exit(1)

    files = find_md_files(OUTPUT_DIR)
    if not files:
        print("No .md files found in output/")
        sys.exit(0)

    results = []
    for f in files:
        results.append(analyze_file(f))

    # Sort: chapters first, then tool guides, then others
    type_order = {"Chapter": 0, "Tool Guide": 1, "Case Study": 2, "Handout": 3, "Other": 4}
    results.sort(key=lambda r: (type_order.get(r["content_type"], 99), r["filename"]))

    # Generate and save report
    report = generate_report(results)

    with open(SCORECARD_PATH, "w", encoding="utf-8") as f:
        f.write(report)

    # Also print to console
    print(report)
    print(f"\nScorecard saved to: {SCORECARD_PATH}")


if __name__ == "__main__":
    main()
