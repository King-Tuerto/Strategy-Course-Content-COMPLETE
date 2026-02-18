#!/usr/bin/env python3
"""
GCU Grade Sheet PDF Generator
Reads audit results from gcu_audit.py and generates one PDF grade sheet per file.

Usage:
    python tools/gcu_grade_pdf.py               # Generate all grade PDFs
    python tools/gcu_grade_pdf.py --run-audit    # Run audit first, then generate PDFs

Output: output/qr-grades/<filename>_GCU_Grade.pdf
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

try:
    from fpdf import FPDF
except ImportError:
    print("ERROR: fpdf2 not installed. Run: python -m pip install fpdf2")
    sys.exit(1)

# ── Configuration ────────────────────────────────────────────────────────────

BASE = Path(__file__).resolve().parent.parent
GRADES_DIR = BASE / "output" / "qr-grades"
AUDIT_JSON = GRADES_DIR / "audit_results.json"

# Colors (RGB tuples)
NAVY = (15, 35, 66)
WHITE = (255, 255, 255)
LIGHT_GRAY = (241, 245, 249)
BORDER_GRAY = (226, 232, 240)
TEXT_DARK = (30, 41, 59)
PASS_GREEN = (16, 185, 129)
WARN_AMBER = (245, 158, 11)
FAIL_RED = (239, 68, 68)
STEEL = (100, 116, 139)


class GradeSheetPDF(FPDF):
    """Custom PDF class for GCU grade sheets."""

    def __init__(self, result):
        super().__init__()
        self.result = result
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        # Navy header bar
        self.set_fill_color(*NAVY)
        self.rect(0, 0, 210, 32, "F")

        self.set_font("Helvetica", "B", 14)
        self.set_text_color(*WHITE)
        self.set_y(8)
        self.cell(0, 8, "GCU Style Guide Compliance Report", align="C", new_x="LMARGIN", new_y="NEXT")

        self.set_font("Helvetica", "", 8)
        self.set_text_color(148, 163, 184)
        self.cell(0, 5, "Grand Canyon University Custom Resource Standards", align="C", new_x="LMARGIN", new_y="NEXT")

        self.set_y(36)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*STEEL)
        self.cell(0, 10, f"Generated {datetime.now().strftime('%Y-%m-%d %H:%M')} | Page {self.page_no()}/{{nb}}", align="C")

    def add_meta_section(self):
        """File metadata box."""
        r = self.result

        self.set_fill_color(*LIGHT_GRAY)
        self.set_draw_color(*BORDER_GRAY)
        y_start = self.get_y()
        self.rect(10, y_start, 190, 28, "DF")

        self.set_xy(14, y_start + 3)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*TEXT_DARK)
        self.cell(90, 6, f"File: {r['filename']}", new_x="RIGHT")

        self.set_font("Helvetica", "", 9)
        self.set_text_color(*STEEL)
        self.cell(90, 6, f"Date: {r['timestamp']}", align="R", new_x="LMARGIN", new_y="NEXT")

        self.set_x(14)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*STEEL)
        self.cell(90, 6, f"Content Type: {r['content_type']}", new_x="RIGHT")

        # Overall score badge
        score = r["overall_score"]
        status = r["overall_status"]
        if status == "COMPLIANT":
            badge_color = PASS_GREEN
        elif "MAJOR" in status:
            badge_color = FAIL_RED
        else:
            badge_color = WARN_AMBER

        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*badge_color)
        self.cell(90, 6, f"Score: {score:.1f}% - {status}", align="R", new_x="LMARGIN", new_y="NEXT")

        self.set_y(y_start + 32)

    def add_rubric_table(self):
        """Main rubric table with all 11 checks."""
        checks = self.result["checks"]

        # Table header
        self.set_fill_color(*NAVY)
        self.set_text_color(*WHITE)
        self.set_font("Helvetica", "B", 8)
        self.set_draw_color(*BORDER_GRAY)

        col_widths = [8, 82, 16, 16, 68]  # #, Check, Status, Score, Findings
        headers = ["#", "Compliance Check", "Status", "Score", "Key Findings"]

        for i, (w, h) in enumerate(zip(col_widths, headers)):
            self.cell(w, 8, h, border=1, fill=True, align="C" if i >= 2 else "L")
        self.ln()

        # Table rows
        self.set_font("Helvetica", "", 7.5)
        for idx, check in enumerate(checks, 1):
            # Alternating row colors
            if idx % 2 == 0:
                self.set_fill_color(*LIGHT_GRAY)
            else:
                self.set_fill_color(*WHITE)

            row_height = 10
            # Calculate row height based on findings
            findings_text = "; ".join(check["findings"])
            if len(findings_text) > 80:
                row_height = 14
            if len(findings_text) > 140:
                row_height = 18

            y_before = self.get_y()

            # Check number
            self.set_text_color(*TEXT_DARK)
            self.cell(col_widths[0], row_height, str(idx), border=1, fill=True, align="C")

            # Check name
            self.cell(col_widths[1], row_height, check["name"], border=1, fill=True)

            # Status with color
            status = check["status"]
            if status == "PASS":
                self.set_text_color(*PASS_GREEN)
            elif status == "WARN":
                self.set_text_color(*WARN_AMBER)
            else:
                self.set_text_color(*FAIL_RED)
            self.set_font("Helvetica", "B", 7.5)
            self.cell(col_widths[2], row_height, status, border=1, fill=True, align="C")

            # Score
            self.set_text_color(*TEXT_DARK)
            self.set_font("Helvetica", "", 7.5)
            self.cell(col_widths[3], row_height, f"{check['score']}%", border=1, fill=True, align="C")

            # Findings (truncated to fit)
            self.set_text_color(*STEEL)
            self.set_font("Helvetica", "", 6.5)
            truncated = findings_text[:120]
            if len(findings_text) > 120:
                truncated += "..."
            self.cell(col_widths[4], row_height, truncated, border=1, fill=True)

            self.ln()

        self.ln(4)

    def add_detailed_findings(self):
        """Detailed findings for non-passing checks."""
        checks = self.result["checks"]
        non_pass = [c for c in checks if c["status"] != "PASS"]

        if not non_pass:
            self.set_font("Helvetica", "B", 10)
            self.set_text_color(*PASS_GREEN)
            self.cell(0, 10, "ALL CHECKS PASSED - File is GCU compliant.", align="C", new_x="LMARGIN", new_y="NEXT")
            return

        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*TEXT_DARK)
        self.cell(0, 8, "Detailed Findings", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*NAVY)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

        for check in non_pass:
            # Check header
            if check["status"] == "FAIL":
                self.set_text_color(*FAIL_RED)
                marker = "FAIL"
            else:
                self.set_text_color(*WARN_AMBER)
                marker = "WARN"

            self.set_font("Helvetica", "B", 8)
            self.cell(0, 6, f"[{marker}] {check['name']} ({check['score']}%)", new_x="LMARGIN", new_y="NEXT")

            # Finding details
            self.set_font("Helvetica", "", 7)
            self.set_text_color(*STEEL)
            for finding in check["findings"]:
                # Wrap long lines
                if len(finding) > 110:
                    self.multi_cell(185, 4, f"  {finding}", new_x="LMARGIN", new_y="NEXT")
                else:
                    self.cell(0, 4, f"  {finding}", new_x="LMARGIN", new_y="NEXT")

            self.ln(2)

    def add_recommendation(self):
        """Final recommendation box."""
        status = self.result["overall_status"]
        score = self.result["overall_score"]

        self.ln(4)
        if status == "COMPLIANT":
            color = PASS_GREEN
            text = "This file meets GCU Style Guide requirements. No revisions needed."
        elif "MAJOR" in status:
            color = FAIL_RED
            text = "This file requires significant formatting revisions to meet GCU Style Guide requirements. Address all FAIL items before submission."
        elif "NEEDS" in status:
            color = FAIL_RED
            text = "This file requires revisions to meet GCU Style Guide requirements. Address all FAIL items and review WARN items."
        else:
            color = WARN_AMBER
            text = "This file is close to compliance. Address WARN items to achieve full compliance."

        self.set_fill_color(*color)
        self.rect(10, self.get_y(), 190, 1.5, "F")
        self.ln(4)

        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*color)
        self.cell(0, 6, f"Recommendation: {status}", new_x="LMARGIN", new_y="NEXT")

        self.set_font("Helvetica", "", 8)
        self.set_text_color(*TEXT_DARK)
        self.multi_cell(185, 5, text, new_x="LMARGIN", new_y="NEXT")


def generate_pdf(result, output_dir):
    """Generate a single PDF grade sheet for one audit result."""
    pdf = GradeSheetPDF(result)
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.add_meta_section()
    pdf.add_rubric_table()
    pdf.add_detailed_findings()
    pdf.add_recommendation()

    filename = f"{result['filename']}_GCU_Grade.pdf"
    filepath = output_dir / filename
    pdf.output(str(filepath))
    return filepath


def main():
    args = sys.argv[1:]

    # Run audit first if requested
    if "--run-audit" in args:
        print("Running GCU audit first...")
        import subprocess
        subprocess.run([sys.executable, str(BASE / "tools" / "gcu_audit.py")], check=True)

    # Load audit results
    if not AUDIT_JSON.exists():
        print(f"ERROR: No audit results found at {AUDIT_JSON}")
        print("Run: python tools/gcu_audit.py  first, or use --run-audit flag")
        sys.exit(1)

    with open(AUDIT_JSON, "r", encoding="utf-8") as f:
        all_results = json.load(f)

    # Ensure output directory
    GRADES_DIR.mkdir(parents=True, exist_ok=True)

    # Generate PDFs
    print(f"\nGenerating {len(all_results)} PDF grade sheet(s)...")
    for result in all_results:
        pdf_path = generate_pdf(result, GRADES_DIR)
        status_icon = {
            "COMPLIANT": "PASS",
            "MINOR REVISION": "WARN",
            "NEEDS REVISION": "FAIL",
            "MAJOR REVISION": "FAIL",
        }.get(result["overall_status"], "?")
        print(f"  [{status_icon}] {result['filename']:<50} -> {pdf_path.name}")

    print(f"\nAll grade sheets saved to: {GRADES_DIR}")
    print(f"Total: {len(all_results)} files audited")

    compliant = sum(1 for r in all_results if r["overall_status"] == "COMPLIANT")
    print(f"Compliant: {compliant}/{len(all_results)}")


if __name__ == "__main__":
    main()
