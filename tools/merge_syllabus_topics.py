"""
Syllabus Topic Merger
======================
Merges the 8 Topic files from "Syallabus As is" into combined documents.

- Fused PDF: merges 8 PDFs into one combined PDF using PyPDF2
- Fused Word: merges 8 Word docs into one combined Word doc using PowerShell/Word COM

Each Topic starts on a fresh page in the combined files.
Existing individual files are left untouched.

Usage:
    python tools/merge_syllabus_topics.py
"""

import os
import sys
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Source directories (note the spelling in the actual folder name)
SYLLABUS_DIR = os.path.join(PROJECT_ROOT, '..', 'Syallabus As is')
PDF_DIR = os.path.join(SYLLABUS_DIR, 'Fused PDF')
WORD_DIR = os.path.join(SYLLABUS_DIR, 'Fused Word')

# Output files (saved alongside the source folders)
OUTPUT_PDF = os.path.join(SYLLABUS_DIR, 'Syllabus-All-Topics-Combined.pdf')
OUTPUT_DOCX = os.path.join(SYLLABUS_DIR, 'Syllabus-All-Topics-Combined.docx')

# File ordering
PDF_FILES = [
    'Topic1_Fused.pdf',
    'Topic2_Fused.pdf',
    'Topic3_Fused.pdf',
    'Topic4_Fused.pdf',
    'Topic5_Fused.pdf',
    'Topic6_Fused.pdf',
    'Topic7_Fused.pdf',
    'Topic8_Fused.pdf',
]

WORD_FILES = [
    'Topic1_Fused.docx',
    'Topic2_Fused_v2.docx',
    'Topic3_Fused_v2.docx',
    'Topic4_Fused_v2.docx',
    'Topic5_Fused.docx',
    'Topic6_Fused.docx',
    'Topic7_Fused.docx',
    'Topic8_Fused.docx',
]


def merge_pdfs():
    """Merge all Topic PDFs into one combined PDF using PyPDF2."""
    print("\n  Merging PDFs...")

    try:
        from PyPDF2 import PdfMerger
    except ImportError:
        print("  ERROR: PyPDF2 not installed. Run: python -m pip install PyPDF2")
        return False

    merger = PdfMerger()
    files_added = 0

    for filename in PDF_FILES:
        filepath = os.path.join(PDF_DIR, filename)
        if not os.path.exists(filepath):
            print(f"    SKIP: {filename} not found")
            continue
        merger.append(filepath)
        size_kb = os.path.getsize(filepath) / 1024
        print(f"    Added: {filename} ({size_kb:.0f} KB)")
        files_added += 1

    if files_added == 0:
        print("  ERROR: No PDF files found to merge")
        merger.close()
        return False

    merger.write(OUTPUT_PDF)
    merger.close()

    size_mb = os.path.getsize(OUTPUT_PDF) / (1024 * 1024)
    print(f"\n  PDF merged: {files_added} files -> {OUTPUT_PDF}")
    print(f"  Size: {size_mb:.1f} MB")
    return True


def merge_word_docs():
    """Merge all Topic Word docs into one combined document using PowerShell/Word COM.

    Uses Word COM automation to preserve all formatting, styles, headers,
    footers, and images from the original documents. Inserts page breaks
    between each topic.
    """
    print("\n  Merging Word documents...")

    # Build the list of absolute paths for files that exist
    file_paths = []
    for filename in WORD_FILES:
        filepath = os.path.join(WORD_DIR, filename)
        if not os.path.exists(filepath):
            print(f"    SKIP: {filename} not found")
            continue
        abs_path = os.path.abspath(filepath).replace('\\', '\\\\')
        print(f"    Queued: {filename}")
        file_paths.append(abs_path)

    if not file_paths:
        print("  ERROR: No Word files found to merge")
        return False

    abs_output = os.path.abspath(OUTPUT_DOCX).replace('\\', '\\\\')

    # Build PowerShell script that:
    # 1. Opens the first doc as the base
    # 2. For each subsequent doc: insert page break, then insert file content
    # 3. Save as the combined output
    files_array = ', '.join([f'"{p}"' for p in file_paths])

    ps_script = f'''
$files = @({files_array})
$outputPath = "{abs_output}"

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0

# Open the first document as our base
$baseDoc = $word.Documents.Open($files[0])

# Append each subsequent document with a page break before it
for ($i = 1; $i -lt $files.Count; $i++) {{
    $range = $baseDoc.Content
    $range.Collapse(0)  # wdCollapseEnd
    $range.InsertBreak(7)  # wdSectionBreakNextPage

    $range2 = $baseDoc.Content
    $range2.Collapse(0)
    $range2.InsertFile($files[$i])

    Write-Host "  Inserted: $($files[$i])"
}}

# Save as new file
$baseDoc.SaveAs([ref]$outputPath, [ref]16)  # wdFormatDocumentDefault
$baseDoc.Close()
$word.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
Write-Host "  Word merge complete"
'''

    try:
        result = subprocess.run(
            ['powershell', '-NoProfile', '-Command', ps_script],
            capture_output=True, text=True, timeout=120
        )

        if result.stdout:
            for line in result.stdout.strip().split('\n'):
                print(f"    {line.strip()}")

        if os.path.exists(OUTPUT_DOCX) and os.path.getsize(OUTPUT_DOCX) > 0:
            size_mb = os.path.getsize(OUTPUT_DOCX) / (1024 * 1024)
            print(f"\n  Word merged: {len(file_paths)} files -> {OUTPUT_DOCX}")
            print(f"  Size: {size_mb:.1f} MB")
            return True
        else:
            print(f"  ERROR: Word merge failed.")
            if result.stderr:
                print(f"  {result.stderr[:300]}")
            return False

    except Exception as e:
        print(f"  ERROR: Word merge failed: {e}")
        return False


def main():
    print(f"\n{'='*60}")
    print(f"  SYLLABUS TOPIC MERGER")
    print(f"  Source: Syallabus As is/")
    print(f"{'='*60}")

    # Verify source directories exist
    if not os.path.exists(PDF_DIR):
        print(f"\n  ERROR: PDF directory not found: {PDF_DIR}")
        sys.exit(1)
    if not os.path.exists(WORD_DIR):
        print(f"\n  ERROR: Word directory not found: {WORD_DIR}")
        sys.exit(1)

    pdf_ok = merge_pdfs()
    word_ok = merge_word_docs()

    print(f"\n{'='*60}")
    print(f"  MERGE COMPLETE")
    if pdf_ok:
        print(f"  PDF:  {OUTPUT_PDF}")
    else:
        print(f"  PDF:  FAILED")
    if word_ok:
        print(f"  Word: {OUTPUT_DOCX}")
    else:
        print(f"  Word: FAILED")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
