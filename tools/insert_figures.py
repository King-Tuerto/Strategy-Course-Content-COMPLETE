"""
Figure Insertion Tool
======================
Copies chapters from output/chapters/ to output/chapters-with-figures/
and inserts GCU-compliant figure references at the correct locations.

Original files are NEVER modified.

Usage:
    python tools/insert_figures.py              # Process all topics
    python tools/insert_figures.py --topic 3    # Process one topic
    python tools/insert_figures.py --verify     # Verify insertions

GCU figure reference format:
    **Figure X.Y.** *Title Here*
    ![Alt text](../graphics/topic-X/filename.png)
"""

import os
import re
import sys
import shutil

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SRC_DIR = os.path.join(PROJECT_ROOT, 'output', 'chapters')
DST_DIR = os.path.join(PROJECT_ROOT, 'output', 'chapters-with-figures')


# =============================================================================
# FIGURE INSERTION MAP
# =============================================================================
# Each entry: (heading_text_to_match, figure_dict)
#
# The tool scans each line. When it finds a heading that matches, it inserts
# the figure reference AFTER the first complete paragraph following that heading.
# This ensures figures appear in context, not awkwardly between a heading and
# its opening sentence.
#
# match_mode:
#   'after_heading' – insert after the first paragraph following the heading
#   'before_heading' – insert immediately before the heading line
#   'end_of_section' – insert before the next H2/H3 heading
# =============================================================================

FIGURE_MAP = {
    # ─── TOPIC 1 ──────────────────────────────────────────────────────
    'Topic-1-Foundations-of-Strategic-Management.md': [
        {
            'match': '## The Comprehensive Strategic Management Model',
            'mode': 'after_heading',
            'figure_number': '1.1',
            'title': 'Comprehensive Strategic Management Model',
            'filename': 'fig-1-1-sm-model.png',
            'topic_dir': 'topic-1',
            'alt_text': 'Flowchart showing the three stages of strategic management: formulation, implementation, and evaluation with feedback loops',
        },
        {
            'match': '### Vision Statements',
            'mode': 'before_heading',
            'figure_number': '1.2',
            'title': 'From Vision to Competitive Advantage',
            'filename': 'fig-1-2-vision-cascade.png',
            'topic_dir': 'topic-1',
            'alt_text': 'Cascade diagram showing vision flowing through mission, objectives, strategies, and policies to competitive advantage',
        },
        {
            'match': '### The Triple Bottom Line',
            'mode': 'after_heading',
            'figure_number': '1.3',
            'title': 'The Triple Bottom Line Framework',
            'filename': 'fig-1-3-triple-bottom-line.png',
            'topic_dir': 'topic-1',
            'alt_text': 'Three overlapping circles showing profit, people, and planet dimensions of sustainability',
        },
        {
            'match': '### Benefits of Strategic Management',
            'mode': 'after_heading',
            'figure_number': '1.4',
            'title': 'Financial and Nonfinancial Benefits of Strategic Management',
            'filename': 'fig-1-4-strategy-benefits.png',
            'topic_dir': 'topic-1',
            'alt_text': 'Side-by-side comparison of financial benefits and nonfinancial benefits of strategic management',
        },
        {
            'match': '### Ethical Decision-Making Frameworks',
            'mode': 'after_heading',
            'figure_number': '1.5',
            'title': 'Business Ethics Decision Framework',
            'filename': 'fig-1-5-ethics-framework.png',
            'topic_dir': 'topic-1',
            'alt_text': 'Decision tree showing ethical analysis process for strategic decisions',
        },
    ],

    # ─── TOPIC 2 ──────────────────────────────────────────────────────
    'Topic-2-External-Analysis-and-International-Strategy.md': [
        {
            'match': '## The External Factor Evaluation Matrix',
            'mode': 'before_heading',
            'figure_number': '2.1',
            'title': 'External Factor Evaluation Process',
            'filename': 'fig-2-1-efe-process.png',
            'topic_dir': 'topic-2',
            'alt_text': 'Flowchart showing the five steps of constructing an EFE Matrix',
        },
        {
            'match': '## Porter\'s Five Forces Model',
            'mode': 'after_heading',
            'figure_number': '2.2',
            'title': 'Porter\'s Five Forces Model',
            'filename': 'fig-2-2-five-forces.png',
            'topic_dir': 'topic-2',
            'alt_text': 'Diagram showing five competitive forces: rivalry, new entrants, substitutes, buyer power, and supplier power',
        },
        {
            'match': '## PESTEL Analysis',
            'mode': 'after_heading',
            'figure_number': '2.3',
            'title': 'PESTEL Analysis Framework',
            'filename': 'fig-2-3-pestel.png',
            'topic_dir': 'topic-2',
            'alt_text': 'Hexagonal diagram showing six PESTEL factors: political, economic, social, technological, environmental, and legal',
        },
        {
            'match': '## The Competitive Profile Matrix',
            'mode': 'after_heading',
            'figure_number': '2.4',
            'title': 'Competitive Profile Matrix Overview',
            'filename': 'fig-2-4-cpm-overview.png',
            'topic_dir': 'topic-2',
            'alt_text': 'Table showing CPM structure with critical success factors, weights, ratings, and scores for multiple competitors',
        },
        {
            'match': '### The Integration-Responsiveness Framework',
            'mode': 'after_heading',
            'figure_number': '2.5',
            'title': 'Integration-Responsiveness Framework',
            'filename': 'fig-2-5-integration-responsiveness.png',
            'topic_dir': 'topic-2',
            'alt_text': 'Two-by-two matrix showing four international strategies based on global integration and local responsiveness',
        },
        {
            'match': '### Foreign Market Entry Strategies',
            'mode': 'after_heading',
            'figure_number': '2.6',
            'title': 'International Market Entry Modes',
            'filename': 'fig-2-6-entry-modes.png',
            'topic_dir': 'topic-2',
            'alt_text': 'Spectrum showing market entry modes from low to high commitment: exporting, licensing, joint ventures, acquisition, greenfield',
        },
    ],

    # ─── TOPIC 3 ──────────────────────────────────────────────────────
    'Topic-3-Internal-Analysis-and-Strategy-Types.md': [
        {
            'match': '### The Resource-Based View',
            'mode': 'after_heading',
            'figure_number': '3.1',
            'title': 'Resource-Based View versus Industrial Organization View',
            'filename': 'fig-3-1-rbv-vs-io.png',
            'topic_dir': 'topic-3',
            'alt_text': 'Side-by-side comparison of RBV and IO perspectives on competitive advantage',
        },
        {
            'match': '### The VRIO Framework',
            'mode': 'after_heading',
            'figure_number': '3.2',
            'title': 'VRIO Decision Tree',
            'filename': 'fig-3-2-vrio-tree.png',
            'topic_dir': 'topic-3',
            'alt_text': 'Decision tree showing VRIO analysis with four sequential tests leading to competitive outcomes',
        },
        {
            'match': '### Value Chain Analysis',
            'mode': 'after_heading',
            'figure_number': '3.3',
            'title': 'Porter\'s Value Chain',
            'filename': 'fig-3-3-value-chain.png',
            'topic_dir': 'topic-3',
            'alt_text': 'Value chain showing five primary activities and four support activities leading to profit margin',
        },
        {
            'match': '### Connecting Internal and External Assessment',
            'mode': 'before_heading',
            'figure_number': '3.4',
            'title': 'Internal Factor Evaluation Process',
            'filename': 'fig-3-4-ife-process.png',
            'topic_dir': 'topic-3',
            'alt_text': 'Flowchart showing the five steps of constructing an IFE Matrix',
        },
        {
            'match': '### The Six Functional Areas',
            'mode': 'after_heading',
            'figure_number': '3.5',
            'title': 'Six Functional Areas for Internal Audit',
            'filename': 'fig-3-5-functional-areas.png',
            'topic_dir': 'topic-3',
            'alt_text': 'Radial diagram showing six functional audit areas: management, marketing, finance, production, research, and information systems',
        },
        {
            'match': '### Financial Ratio Analysis',
            'mode': 'after_heading',
            'figure_number': '3.6',
            'title': 'Five Categories of Financial Ratios',
            'filename': 'fig-3-6-financial-ratios.png',
            'topic_dir': 'topic-3',
            'alt_text': 'Category grid showing five financial ratio categories with example ratios for each',
        },
        {
            'match': '## Part Two: Types of Strategies',
            'mode': 'after_heading',
            'figure_number': '3.7',
            'title': 'Strategy Types and Alternatives',
            'filename': 'fig-3-7-strategy-types.png',
            'topic_dir': 'topic-3',
            'alt_text': 'Hierarchical tree showing four strategy categories and their specific alternatives',
        },
        {
            'match': '### Integration Strategies',
            'mode': 'after_heading',
            'figure_number': '3.8',
            'title': 'Integration Strategies Spectrum',
            'filename': 'fig-3-8-integration-strategies.png',
            'topic_dir': 'topic-3',
            'alt_text': 'Spectrum showing forward, backward, and horizontal integration strategies with examples',
        },
        {
            'match': '### Intensive Strategies',
            'mode': 'after_heading',
            'figure_number': '3.9',
            'title': 'Intensive Growth Strategies',
            'filename': 'fig-3-9-intensive-strategies.png',
            'topic_dir': 'topic-3',
            'alt_text': 'Category grid showing three intensive strategies: market penetration, market development, and product development',
        },
        {
            'match': '### Diversification Strategies',
            'mode': 'after_heading',
            'figure_number': '3.10',
            'title': 'Related versus Unrelated Diversification',
            'filename': 'fig-3-10-diversification.png',
            'topic_dir': 'topic-3',
            'alt_text': 'Comparison of related and unrelated diversification strategies with characteristics and examples',
        },
        {
            'match': '### Defensive Strategies',
            'mode': 'after_heading',
            'figure_number': '3.11',
            'title': 'Defensive Strategy Cascade',
            'filename': 'fig-3-11-defensive-strategies.png',
            'topic_dir': 'topic-3',
            'alt_text': 'Cascade showing retrenchment, divestiture, and liquidation as escalating defensive strategies',
        },
        {
            'match': '### Porter\'s Generic Strategies',
            'mode': 'after_heading',
            'figure_number': '3.12',
            'title': 'Porter\'s Generic Strategies',
            'filename': 'fig-3-12-porter-generic.png',
            'topic_dir': 'topic-3',
            'alt_text': 'Two-by-two matrix showing four generic strategies based on competitive scope and source of advantage',
        },
        {
            'match': '### Organic Growth Versus Growth Through Acquisition',
            'mode': 'after_heading',
            'figure_number': '3.13',
            'title': 'Organic Growth versus Acquisition Growth',
            'filename': 'fig-3-13-organic-vs-acquisition.png',
            'topic_dir': 'topic-3',
            'alt_text': 'Comparison table of organic growth and acquisition growth approaches',
        },
        {
            'match': '### Long-Term Objectives',
            'mode': 'after_heading',
            'figure_number': '3.14',
            'title': 'Seven Characteristics of Long-Term Objectives',
            'filename': 'fig-3-14-objectives-characteristics.png',
            'topic_dir': 'topic-3',
            'alt_text': 'Category grid listing seven desirable characteristics of long-term strategic objectives',
        },
    ],

    # ─── TOPIC 4 ──────────────────────────────────────────────────────
    'Topic-4-Strategy-Analysis-and-Implementation.md': [
        {
            'match': '### The Three-Stage Framework',
            'mode': 'after_heading',
            'figure_number': '4.1',
            'title': 'Strategy Formulation Analytical Framework',
            'filename': 'fig-4-1-formulation-framework.png',
            'topic_dir': 'topic-4',
            'alt_text': 'Three-tier framework showing Input Stage, Matching Stage, and Decision Stage of strategy formulation',
        },
        {
            'match': '#### The SWOT Matrix',
            'mode': 'after_heading',
            'figure_number': '4.2',
            'title': 'SWOT Matrix with Strategy Combinations',
            'filename': 'fig-4-2-swot-matrix.png',
            'topic_dir': 'topic-4',
            'alt_text': 'Four-quadrant SWOT matrix showing SO, WO, ST, and WT strategy combinations',
            'heading_level': 4,
        },
        {
            'match': '#### The SPACE Matrix',
            'mode': 'after_heading',
            'figure_number': '4.3',
            'title': 'SPACE Matrix with Four Strategic Postures',
            'filename': 'fig-4-3-space-matrix.png',
            'topic_dir': 'topic-4',
            'alt_text': 'Four-quadrant axis diagram showing aggressive, conservative, defensive, and competitive postures',
            'heading_level': 4,
        },
        {
            'match': '#### The BCG Matrix',
            'mode': 'after_heading',
            'figure_number': '4.4',
            'title': 'BCG Growth-Share Matrix',
            'filename': 'fig-4-4-bcg-matrix.png',
            'topic_dir': 'topic-4',
            'alt_text': 'Two-by-two matrix showing Stars, Question Marks, Cash Cows, and Dogs based on growth rate and market share',
            'heading_level': 4,
        },
        {
            'match': '#### The Internal-External Matrix',
            'mode': 'after_heading',
            'figure_number': '4.5',
            'title': 'Internal-External Matrix',
            'filename': 'fig-4-5-ie-matrix.png',
            'topic_dir': 'topic-4',
            'alt_text': 'Three-by-three grid showing grow-build, hold-maintain, and harvest-divest regions based on IFE and EFE scores',
            'heading_level': 4,
        },
        {
            'match': '#### The Grand Strategy Matrix',
            'mode': 'after_heading',
            'figure_number': '4.6',
            'title': 'Grand Strategy Matrix',
            'filename': 'fig-4-6-grand-strategy.png',
            'topic_dir': 'topic-4',
            'alt_text': 'Two-by-two matrix showing four quadrants based on competitive position and market growth',
            'heading_level': 4,
        },
        {
            'match': '### The Decision Stage',
            'mode': 'after_heading',
            'figure_number': '4.7',
            'title': 'QSPM Decision Matrix Overview',
            'filename': 'fig-4-7-qspm-overview.png',
            'topic_dir': 'topic-4',
            'alt_text': 'Table showing QSPM structure with key factors, weights, and attractiveness scores for strategy alternatives',
        },
        {
            'match': '### Why Implementation Is Harder Than Formulation',
            'mode': 'after_heading',
            'figure_number': '4.8',
            'title': 'Strategy Formulation versus Strategy Implementation',
            'filename': 'fig-4-8-formulation-vs-implementation.png',
            'topic_dir': 'topic-4',
            'alt_text': 'Side-by-side comparison of strategy formulation and strategy implementation characteristics',
        },
        {
            'match': '### Organizational Structure and Strategy',
            'mode': 'after_heading',
            'figure_number': '4.9',
            'title': 'Organizational Structure Types',
            'filename': 'fig-4-9-org-structures.png',
            'topic_dir': 'topic-4',
            'alt_text': 'Comparison of four organizational structure types: functional, divisional, matrix, and SBU',
        },
        {
            'match': '### Organizational Structure and Strategy',
            'mode': 'end_of_section',
            'figure_number': '4.10',
            'title': 'Structure Follows Strategy Model',
            'filename': 'fig-4-10-structure-strategy.png',
            'topic_dir': 'topic-4',
            'alt_text': 'Flowchart showing how new strategy leads to new administrative problems and then new organizational structure',
        },
        {
            'match': '### Annual Objectives',
            'mode': 'after_heading',
            'figure_number': '4.11',
            'title': 'From Long-Term Objectives to Annual Objectives',
            'filename': 'fig-4-11-objectives-cascade.png',
            'topic_dir': 'topic-4',
            'alt_text': 'Cascade showing long-term objectives breaking down into divisional and departmental annual objectives',
        },
        {
            'match': '### Managing Resistance to Change',
            'mode': 'after_heading',
            'figure_number': '4.12',
            'title': 'Force Field Analysis for Managing Change',
            'filename': 'fig-4-12-force-field.png',
            'topic_dir': 'topic-4',
            'alt_text': 'Force field diagram showing driving forces and restraining forces in strategy implementation',
        },
        {
            'match': '### Marketing Implementation',
            'mode': 'after_heading',
            'figure_number': '4.13',
            'title': 'Marketing Implementation Framework',
            'filename': 'fig-4-13-marketing-4ps.png',
            'topic_dir': 'topic-4',
            'alt_text': 'Diagram showing market segmentation, product positioning, and the marketing mix (4Ps)',
        },
        {
            'match': '### Restructuring, Reengineering, and E-Commerce',
            'mode': 'after_heading',
            'figure_number': '4.14',
            'title': 'Restructuring, Reengineering, and E-Commerce',
            'filename': 'fig-4-14-restructuring.png',
            'topic_dir': 'topic-4',
            'alt_text': 'Comparison of restructuring, reengineering, and e-commerce as implementation approaches',
        },
    ],

    # ─── TOPIC 6 ──────────────────────────────────────────────────────
    'Topic-6-Strategy-Evaluation-and-Control.md': [
        {
            'match': '## The Three Fundamental Evaluation Activities',
            'mode': 'after_heading',
            'figure_number': '6.1',
            'title': 'Strategy Evaluation Framework',
            'filename': 'fig-6-1-evaluation-framework.png',
            'topic_dir': 'topic-6',
            'alt_text': 'Flowchart showing the three activities of strategy evaluation: reviewing bases, measuring performance, and taking corrective actions',
        },
        {
            'match': '## Rumelt\'s Four Criteria for Strategy Evaluation',
            'mode': 'after_heading',
            'figure_number': '6.2',
            'title': 'Rumelt\'s Four Criteria for Strategy Evaluation',
            'filename': 'fig-6-2-rumelt-criteria.png',
            'topic_dir': 'topic-6',
            'alt_text': 'Category grid showing Rumelt\'s four evaluation criteria: consistency, consonance, feasibility, and advantage',
        },
        {
            'match': '## The Balanced Scorecard',
            'mode': 'after_heading',
            'figure_number': '6.3',
            'title': 'The Balanced Scorecard',
            'filename': 'fig-6-3-balanced-scorecard.png',
            'topic_dir': 'topic-6',
            'alt_text': 'Four-perspective Balanced Scorecard with financial, customer, internal process, and learning/growth dimensions',
        },
        {
            'match': '## Characteristics of an Effective Evaluation System',
            'mode': 'after_heading',
            'figure_number': '6.4',
            'title': 'Characteristics of an Effective Evaluation System',
            'filename': 'fig-6-4-evaluation-characteristics.png',
            'topic_dir': 'topic-6',
            'alt_text': 'Category grid listing key characteristics of effective strategy evaluation systems',
        },
        {
            'match': '## Contingency Planning',
            'mode': 'after_heading',
            'figure_number': '6.5',
            'title': 'Contingency Planning Process',
            'filename': 'fig-6-5-contingency-planning.png',
            'topic_dir': 'topic-6',
            'alt_text': 'Flowchart showing the contingency planning process from identifying trigger events to activating alternative strategies',
        },
        {
            'match': '### Taking Corrective Actions',
            'mode': 'after_heading',
            'figure_number': '6.6',
            'title': 'Taking Corrective Actions Decision Flow',
            'filename': 'fig-6-6-corrective-actions.png',
            'topic_dir': 'topic-6',
            'alt_text': 'Decision tree for determining appropriate corrective actions based on evaluation findings',
        },
        {
            'match': '## Why Strategy Evaluation Is Increasingly Difficult',
            'mode': 'after_heading',
            'figure_number': '6.7',
            'title': 'Why Strategy Evaluation Is Increasingly Difficult',
            'filename': 'fig-6-7-evaluation-difficulty.png',
            'topic_dir': 'topic-6',
            'alt_text': 'Category grid showing factors that make strategy evaluation more challenging in modern business',
        },
    ],

    # ─── TOPIC 7 ──────────────────────────────────────────────────────
    'Topic-7-Finance-and-Accounting-in-Strategy-Implementation.md': [
        {
            'match': '## EPS/EBIT Analysis',
            'mode': 'after_heading',
            'figure_number': '7.1',
            'title': 'EPS/EBIT Analysis Chart',
            'filename': 'fig-7-1-eps-ebit.png',
            'topic_dir': 'topic-7',
            'alt_text': 'Line chart comparing earnings per share under debt and equity financing across EBIT levels with crossover point',
        },
        {
            'match': '## Financial Budgeting',
            'mode': 'after_heading',
            'figure_number': '7.2',
            'title': 'Financial Budget Hierarchy',
            'filename': 'fig-7-2-budget-hierarchy.png',
            'topic_dir': 'topic-7',
            'alt_text': 'Pyramid showing budget hierarchy from master budget down through capital, operating, cash, sales, and profit budgets',
        },
        {
            'match': '## Evaluating Business Worth',
            'mode': 'after_heading',
            'figure_number': '7.3',
            'title': 'Four Business Valuation Methods',
            'filename': 'fig-7-3-valuation-methods.png',
            'topic_dir': 'topic-7',
            'alt_text': 'Comparison of four valuation methods: net worth, market capitalization, P/E ratio, and discounted cash flow',
        },
        {
            'match': '## Projected Financial Statements',
            'mode': 'after_heading',
            'figure_number': '7.4',
            'title': 'Pro Forma Financial Statement Process',
            'filename': 'fig-7-4-pro-forma.png',
            'topic_dir': 'topic-7',
            'alt_text': 'Flowchart showing the process of creating pro forma income statements and balance sheets',
        },
        {
            'match': '## Acquiring Capital',
            'mode': 'after_heading',
            'figure_number': '7.5',
            'title': 'Capital Structure Decision Framework',
            'filename': 'fig-7-5-capital-structure.png',
            'topic_dir': 'topic-7',
            'alt_text': 'Comparison of debt and equity financing with advantages, disadvantages, and considerations',
        },
        {
            'match': '## Financial Ratios in Implementation Monitoring',
            'mode': 'after_heading',
            'figure_number': '7.6',
            'title': 'Financial Ratio Monitoring in Implementation',
            'filename': 'fig-7-6-ratio-monitoring.png',
            'topic_dir': 'topic-7',
            'alt_text': 'Category grid showing key financial ratios monitored during strategy implementation',
        },
        {
            'match': '## Dividends and Stock Buybacks',
            'mode': 'after_heading',
            'figure_number': '7.7',
            'title': 'Dividend and Stock Buyback Decision Factors',
            'filename': 'fig-7-7-dividend-decisions.png',
            'topic_dir': 'topic-7',
            'alt_text': 'Radial diagram showing factors influencing dividend and stock buyback decisions',
        },
        {
            'match': '## Integrating Financial Analysis with Strategic Recommendations',
            'mode': 'after_heading',
            'figure_number': '7.8',
            'title': 'Integrating Financial Analysis with Strategy',
            'filename': 'fig-7-8-financial-integration.png',
            'topic_dir': 'topic-7',
            'alt_text': 'Flowchart showing how financial analysis integrates with strategic recommendations',
        },
    ],
}


# =============================================================================
# INSERTION ENGINE
# =============================================================================

def build_figure_block(fig):
    """Build GCU-compliant Markdown figure reference block."""
    rel_path = f'../graphics/{fig["topic_dir"]}/{fig["filename"]}'
    return (
        f'\n'
        f'**Figure {fig["figure_number"]}.** *{fig["title"]}*\n'
        f'\n'
        f'![{fig["alt_text"]}]({rel_path})\n'
        f'\n'
    )


def insert_figures_into_chapter(src_path, dst_path, figures):
    """
    Copy a chapter file and insert figure references.

    Strategy:
    - 'after_heading': Find the heading, then skip past the first complete
      paragraph (text block followed by blank line), insert figure there.
    - 'before_heading': Insert immediately before the heading line.
    - 'end_of_section': Insert before the next heading at same or higher level.
    """
    with open(src_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Build insertion plan: map line numbers to figure blocks
    insertions = {}  # line_number -> list of figure blocks to insert BEFORE this line

    for fig in figures:
        match_text = fig['match']
        mode = fig['mode']
        block = build_figure_block(fig)

        # Find the heading line
        heading_line = None
        for i, line in enumerate(lines):
            if line.strip() == match_text or line.strip().startswith(match_text):
                heading_line = i
                break

        if heading_line is None:
            # Try partial match (heading might have slightly different formatting)
            match_core = match_text.lstrip('#').strip()
            for i, line in enumerate(lines):
                line_core = line.strip().lstrip('#').strip()
                if match_core.lower() in line_core.lower() and line.strip().startswith('#'):
                    heading_line = i
                    break

        if heading_line is None:
            print(f"  WARNING: Could not find heading '{match_text}' in {os.path.basename(src_path)}")
            continue

        if mode == 'before_heading':
            insert_at = heading_line
        elif mode == 'after_heading':
            # Skip past the first paragraph after the heading
            insert_at = _find_end_of_first_paragraph(lines, heading_line)
        elif mode == 'end_of_section':
            # Find next heading at same or higher level
            heading_level = fig.get('heading_level', _get_heading_level(lines[heading_line]))
            insert_at = _find_next_heading(lines, heading_line, heading_level)
        else:
            insert_at = heading_line

        insertions.setdefault(insert_at, []).append(block)

    # Build output with insertions
    output_lines = []
    for i, line in enumerate(lines):
        if i in insertions:
            for block in insertions[i]:
                output_lines.append(block)
        output_lines.append(line)

    # Check if last line needs insertions too
    end_idx = len(lines)
    if end_idx in insertions:
        for block in insertions[end_idx]:
            output_lines.append(block)

    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)

    return len(figures)


def _find_end_of_first_paragraph(lines, heading_idx):
    """Find the line after the first complete paragraph following a heading."""
    i = heading_idx + 1

    # Skip blank lines after heading
    while i < len(lines) and lines[i].strip() == '':
        i += 1

    # Skip the paragraph text (non-blank lines)
    while i < len(lines) and lines[i].strip() != '':
        i += 1

    # Skip the blank line after the paragraph
    while i < len(lines) and lines[i].strip() == '':
        i += 1

    return i


def _find_next_heading(lines, start_idx, max_level):
    """Find the next heading at the same or higher level."""
    for i in range(start_idx + 1, len(lines)):
        line = lines[i].strip()
        if line.startswith('#'):
            level = _get_heading_level(line)
            if level <= max_level:
                return i
    return len(lines)


def _get_heading_level(line):
    """Get heading level from a Markdown heading line."""
    stripped = line.strip()
    level = 0
    for ch in stripped:
        if ch == '#':
            level += 1
        else:
            break
    return level


# =============================================================================
# MAIN
# =============================================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description='Insert figure references into chapter copies.')
    parser.add_argument('--topic', type=str, default=None,
                        help='Process one topic only (1-7)')
    parser.add_argument('--verify', action='store_true',
                        help='Verify insertions')
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"  FIGURE INSERTION TOOL")
    print(f"  Source: output/chapters/ (NEVER modified)")
    print(f"  Target: output/chapters-with-figures/")
    print(f"{'='*60}\n")

    total_inserted = 0
    files_processed = 0

    for filename, figures in FIGURE_MAP.items():
        # Topic filter
        if args.topic:
            topic_num = filename.split('-')[0].replace('Topic', '')
            # Extract the number part
            match = re.search(r'Topic-(\d+)', filename)
            if match and match.group(1) != args.topic:
                continue

        src_path = os.path.join(SRC_DIR, filename)
        dst_path = os.path.join(DST_DIR, filename)

        if not os.path.exists(src_path):
            print(f"  SKIP: {filename} (source not found)")
            continue

        count = insert_figures_into_chapter(src_path, dst_path, figures)
        total_inserted += count
        files_processed += 1
        print(f"  OK: {filename} — {count} figures inserted")

    # Verify mode
    if args.verify:
        print(f"\n  VERIFICATION:")
        for filename in FIGURE_MAP:
            dst_path = os.path.join(DST_DIR, filename)
            if os.path.exists(dst_path):
                with open(dst_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                fig_count = content.count('**Figure ')
                img_count = content.count('![')
                print(f"    {filename}: {fig_count} figure labels, {img_count} images")
            else:
                print(f"    {filename}: MISSING")

    # Verify originals are untouched
    print(f"\n  SAFETY CHECK — Original files:")
    for filename in FIGURE_MAP:
        src = os.path.join(SRC_DIR, filename)
        dst = os.path.join(DST_DIR, filename)
        if os.path.exists(src) and os.path.exists(dst):
            src_size = os.path.getsize(src)
            dst_size = os.path.getsize(dst)
            if dst_size > src_size:
                print(f"    {filename}: Original {src_size:,} bytes -> Enhanced {dst_size:,} bytes  OK")
            else:
                print(f"    {filename}: WARNING - Enhanced file is not larger than original")
        elif os.path.exists(src):
            print(f"    {filename}: Original intact, no enhanced copy yet")

    print(f"\n{'='*60}")
    print(f"  RESULTS: {total_inserted} figures inserted across {files_processed} files")
    print(f"  Originals in output/chapters/ are UNTOUCHED")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
