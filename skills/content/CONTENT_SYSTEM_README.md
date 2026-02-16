# MBA Strategy Course — Complete Content System

## Files Created

✅ `VOICE.md` — Senior Christian executive voice  
✅ `FLESCH_KINCAID.md` — Readability targeting (F-K 16-18 default, adjustable)

## Content Type Default Parameters

These parameters are automatically applied based on what type of content you're generating.

### Tool Guide Defaults

```yaml
word_count: 1000-1500
flesch_kincaid_level: 16-18
mc_question_count: 3
blooms_level: analyze
critical_thinking_count: 1
cwv_level: 4  # 0-10 scale. See VOICE.md for full CWV scale definitions.
```

### Chapter Defaults

```yaml
word_count: 4000
flesch_kincaid_level: 16-18
mc_question_count: 10
blooms_level: analyze
critical_thinking_count: 2
cwv_level: 4  # 0-10 scale. See VOICE.md for full CWV scale definitions.
```

### Case Study Defaults

```yaml
word_count: 1200-1500
flesch_kincaid_level: 16-18
mc_question_count: 0
blooms_level: analyze
critical_thinking_count: 2
cwv_level: 4  # 0-10 scale. See VOICE.md for full CWV scale definitions.
```

**To update these:** Use SETTINGS_MANAGER.md

---

## Files To Create Next (Instructions Below)

The following `.md` files need to be built based on the specifications in this document. Use Claude Code to generate them by providing the templates below.

---

## STRUCTURE.md — Universal Writing Structure

**Purpose:** Defines the structure for ALL written artifacts (tool guides, chapters, cases).

**Key Parameters:**
```yaml
content_type: [tool_guide | chapter | case_study | handout]
sections_required: [varies by type - see below]
flesch_kincaid_target: 12-14  # inherit from FLESCH_KINCAID.md
cwv_level: 4  # 0-10 scale. See VOICE.md for full CWV scale definitions.  # per VOICE.md guidelines
```

**Tool Guide Structure (for tool explications):**
1. **Title** + One-line summary
2. **Purpose** (2-3 sentences: what it does, when to use)
3. **Prerequisites** (what you need before using this)
4. **Step-by-Step Instructions** (numbered, <30 words each)
5. **Scoring Guide** (table format)
6. **Interpretation** (what results mean, thresholds)
7. **Real Example** (company or realistic scenario)
8. **Common Mistakes** (3-5 bullets)
9. **Biblical Integration** (1 paragraph if natural fit exists)
10. **Knowledge Check Questions** (see ASSESSMENT.md)

**Chapter Structure:**
1. **Opening Hook** (real scenario or provocative question)
2. **Learning Objectives** (what you'll be able to do)
3. **Core Concept** (theory explained practically)
4. **Application Examples** (2-3 real companies)
5. **Tool/Framework Introduction** (if applicable)
6. **Ethical Considerations** (faith-business integration)
7. **Summary** (key takeaways, 3-5 bullets)
8. **For Further Reflection** (discussion questions)

**Case Study Structure:**
1. **Company Background** (brief context)
2. **Strategic Challenge** (the problem)
3. **Market/Industry Context**
4. **Financial Data** (if relevant)
5. **Decision Point** (what needs to be decided)
6. **Discussion Questions** (open-ended, require analysis)

---

## PEDAGOGY.md — MBA Learning Design

**Core Principle:**  
MBAs learn by doing, not by reading about doing. Every piece of content must be action-oriented.

**Learning Sequence:**
1. Activate prior knowledge ("You already know...")
2. Introduce new concept 
3. Show structure/framework
4. Guided practice (work through together)
5. Independent application
6. Reflection

**Cognitive Load:**
- One new concept per section
- Use familiar examples (Apple, Starbucks, etc.)
- Build complexity gradually
- Provide worked examples before independent work

**Accessibility:**
- Text at target F-K level (default 12-14)
- Define jargon first use, inline
- Headers every 3-4 paragraphs
- Visual + text explanations

---

## BIBLICAL_INTEGRATION.md — Faith-Business Integration

**When to Integrate:**
- Strategy as stewardship (managing God-given resources)
- Ethics in competition (competitors as image-bearers)
- Purpose beyond profit (kingdom alignment)
- Decision-making under uncertainty (wisdom literature)

**When NOT to Integrate:**
- Don't force scripture into every section
- Avoid gimmicky connections (12 disciples ≠ 12 factors)
- Skip theological debates
- If it feels forced, skip it

**Preferred Sources — Use the full Scripture Reference Bank in VOICE.md:**

A diverse bank of 35+ passages is organized by strategic theme in VOICE.md under "Scripture Reference Bank." Themes include: Stewardship and Resource Allocation, Honest Assessment, Wisdom and Decision-Making, Leadership and Organizational Character, Competition and Ethics, Purpose Beyond Profit, and Perseverance and Long-Term Thinking.

**ANTI-REPETITION RULE:** Before selecting a scripture reference, check all previously completed content in `output/` to confirm the passage has not already been used. Never repeat the same verse or parable across two pieces of content. Select a different passage from the relevant theme category each time.

**Avoid:**
- Obscure OT passages
- Revelation/apocalyptic
- Denominationally divisive passages
- Proof-texting
- Reusing any passage already used in another piece of content

---

## ASSESSMENT.md — Question Design & Rubrics

### Parameters (Adjustable)

```yaml
mc_question_count: 4           # number of multiple choice per tool
blooms_level: analyze          # remember|understand|apply|analyze|evaluate|create
critical_thinking_count: 1     # paragraph questions per tool
rubric_style: holistic         # holistic|analytic
```

### Multiple Choice Question Template

**Structure:**
- Stem: 1-2 sentences, clear scenario
- 4 options (A-D)
- 1 correct, 3 plausible distractors
- Avoid "all of the above" or "none of the above"

**Bloom's Level Definitions:**

| Level | Question Type | Example Stem |
|-------|--------------|-------------|
| Remember | Recall facts | "Which quadrant in the SPACE Matrix indicates..." |
| Understand | Explain concepts | "Why does a negative CA score indicate..." |
| Apply | Use in new situation | "Given this company data, which quadrant..." |
| Analyze | Break down, compare | "Compare Company A's position to Company B's..." |
| Evaluate | Judge, critique | "Which strategic option best addresses..." |
| Create | Design, propose | "Develop a SPACE analysis that would justify..." |

**Default: Analyze level** (requires application + interpretation)

### Critical Thinking Question Template

**Structure:**
- Scenario (2-3 sentences of context)
- Question (requires judgment, multiple valid perspectives)
- Length: 1-2 paragraphs expected

**Topics:**
- Ethical dilemmas
- Stakeholder conflicts
- Values vs. profits
- Long-term vs. short-term
- Justice vs. efficiency

**Example:**
> A pharmaceutical company's SWOT analysis reveals a major opportunity: expanding into low-income international markets where regulatory oversight is minimal. The profit potential is substantial, but quality control standards would be lower than in developed markets. As a Christian executive, how do you weigh this opportunity against the company's stewardship responsibility? Address both the business case and the ethical considerations in your answer.

### Rubric Structure (For Critical Thinking Questions)

**Holistic Rubric (Default):**

| Score | Criteria |
|-------|----------|
| **Excellent (9-10)** | Demonstrates nuanced understanding of both business and ethical dimensions. Engages multiple stakeholder perspectives. References course concepts accurately. Shows integration of faith and practice. Well-organized with clear reasoning. |
| **Proficient (7-8)** | Addresses both business and ethical aspects. Applies course concepts correctly. Shows some integration of faith principles. Clear reasoning with minor gaps. |
| **Developing (5-6)** | Addresses question but may overemphasize one dimension (business OR ethics). Limited application of course concepts. Superficial faith integration. Some logical gaps. |
| **Needs Work (3-4)** | Misses key dimensions. Minimal course concept application. No faith integration or forced/inappropriate references. Unclear reasoning. |
| **Insufficient (0-2)** | Off-topic, plagiarized, or demonstrates fundamental misunderstanding. |

**Analytic Rubric (Optional - more detailed):**

| Criterion | Weight | Excellent | Proficient | Developing |
|-----------|--------|-----------|------------|------------|
| Business Analysis | 30% | Uses course tools correctly, considers multiple strategic options | Applies tools, identifies options | Mentions tools but doesn't apply |
| Ethical Reasoning | 30% | Engages competing values, shows moral imagination | Identifies ethical issues, takes position | Acknowledges ethics superficially |
| Faith Integration | 20% | Natural biblical wisdom application, avoids proof-texting | References faith principles appropriately | Forced or absent integration |
| Writing Quality | 20% | Clear, organized, persuasive | Generally clear with minor issues | Unclear or disorganized |

---

## Template Files (Create These)

### templates/TOOL_GUIDE.md

Use this fill-in template for every strategic management tool guide:

```markdown
# [TOOL NAME] — [Subtitle]

## What This Tool Does
[2-3 sentences. Lead with action verb. F-K 12-14.]

## When to Use It
[Stage in process. Prerequisites. When in the semester.]

## Before You Start
- [Prerequisite 1]
- [Prerequisite 2]
- [Data/resources needed]

---

## Step-by-Step Instructions

### Step 1: [Action Title]
[Instructions, <30 words. What to do, not how it works.]

### Step 2: [Action Title]
[Instructions, <30 words.]

[Continue for all steps...]

---

## Scoring Guide

| Factor | Scale | What It Means |
|--------|-------|---------------|
| [Name] | [Range] | [Brief explanation] |

---

## Interpreting Your Results

[Score ranges and what they mean. Thresholds. Decision rules.]

**If your score is > X:** [Interpretation and recommended actions]
**If your score is between X and Y:** [Interpretation and actions]
**If your score is < Y:** [Interpretation and actions]

---

## Real-World Example

[Company name and brief background]

[Show the tool being applied with actual numbers]

[What the company learned and what they did with it]

---

## Common Mistakes

**Mistake 1: [Description]**  
Why it happens: [explanation]  
How to avoid: [corrective action]

**Mistake 2: [Description]**  
[same structure...]

[3-5 mistakes total]

---

## A Note on Stewardship [OR: Ethical Considerations, OR: Biblical Wisdom]

[1 paragraph of biblical integration IF it fits naturally. Otherwise omit this section entirely.]

[Use BIBLICAL_INTEGRATION.md guidelines]

---

## Knowledge Check

### Multiple Choice

**Question 1 [Blooms: Analyze]:**  
[Stem with scenario]

A) [Option]  
B) [Option]  
C) [Option - CORRECT]  
D) [Option]

*Correct Answer: C*  
*Rationale: [Why C is correct and others are wrong]*

[Repeat for number specified in parameters - default 4 questions]

### Critical Thinking

[Scenario paragraph]

**Question:** [Open-ended question requiring judgment]

**Rubric:** [Use rubric from ASSESSMENT.md]
```

---

### templates/CHAPTER.md

```markdown
# Chapter [N]: [Chapter Title]

## Opening

[Real scenario, provocative question, or surprising fact. 2-3 paragraphs. Hook reader immediately.]

---

## Learning Objectives

By the end of this chapter, you will be able to:
- [Objective 1 - starts with action verb]
- [Objective 2]
- [Objective 3]

---

## Core Concept: [Main Idea]

[Explanation of the central framework/theory. Build from familiar to new. 3-5 paragraphs.]

[Visual diagram if applicable]

---

## Application Example 1: [Company Name]

[Real company applying the concept. Show how it worked (or didn't). 2-3 paragraphs.]

---

## Application Example 2: [Company Name]

[Different industry or different outcome. Show range of applications.]

---

## [Tool/Framework Name] — Putting It Into Practice

[If chapter introduces a strategic tool, full explanation here using TOOL_GUIDE structure]

---

## Ethical Considerations

[Faith-business integration. How does this framework align with (or tension with) Christian values? 2-3 paragraphs.]

[Biblical reference if natural]

---

## Summary

**Key Takeaways:**
- [Bullet 1]
- [Bullet 2]
- [Bullet 3]
- [Bullet 4]
- [Bullet 5]

---

## For Further Reflection

[3-5 discussion questions. Open-ended, require synthesis.]

1. [Question requiring application to student's own context]
2. [Question connecting to earlier chapters]
3. [Question exploring ethical tensions]
```

---

### templates/CASE_STUDY.md

```markdown
# Case Study: [Company Name]

## Company Background

[Who they are, what they do, size, market position. 2-3 paragraphs.]

---

## The Strategic Challenge

[The problem they faced. Set the decision context. What was at stake? 2-3 paragraphs.]

---

## Industry Context

[Market dynamics, competitive landscape, external factors. 1-2 paragraphs.]

---

## Financial/Operational Data

[Tables, charts, relevant metrics. Only include what's decision-relevant.]

---

## The Decision Point

[Describe the moment of choice. What needed to be decided? By when? With what constraints?]

---

## Discussion Questions

**Analysis Questions:**
1. [Tool application: "Complete a SWOT analysis for..."]
2. [Comparison: "How does Company X's position compare to..."]
3. [Interpretation: "What do the numbers tell you about..."]

**Strategic Judgment Questions:**
4. [Open-ended: "What would you recommend and why?"]
5. [Ethical: "How should Christian values inform this decision?"]
6. [Stakeholder: "Who wins and who loses under each option?"]

**Reflection Questions:**
7. [Personal: "If you were the CEO, what would keep you up at night?"]
8. [Learning: "What does this case teach you about [concept]?"]
```

---

## How to Use This System

### For Writing a Tool Guide:

1. In Claude Code, prompt:
```
Read skills/content/VOICE.md, FLESCH_KINCAID.md, STRUCTURE.md, 
BIBLICAL_INTEGRATION.md, and ASSESSMENT.md.

Then write a complete tool guide for the IFE Matrix using 
templates/TOOL_GUIDE.md. 

Parameters:
- F-K level: 12-14
- MC questions: 4 at Analyze level
- Critical thinking: 1 question
```

2. Claude Code generates the guide following all specs
3. Check F-K score, adjust if needed
4. Save to your course materials

### For Writing a Chapter:

```
Read all content skill files, then write Chapter 3 on Internal 
Analysis using templates/CHAPTER.md.

Parameters:
- F-K level: 12-14
- Include IFE tool explanation
- Biblical integration where natural
```

### For Creating a Case:

```
Read content skills, then create a case study on [Company] 
using templates/CASE_STUDY.md.

Topic: [Strategic challenge]
Tools to apply: IFE, SWOT
Include ethical dimension
```

---

## Post-Writing: Content Scorecard

**After completing ANY content piece (chapter, tool guide, case study, handout), run the scorecard tool:**

```
python tools/content_scorecard.py
```

This automatically scans all content in `output/` and generates `output/SCORECARD.md` with:
- Body word count (excluding Key Terms, Knowledge Check, and References)
- Flesch-Kincaid Grade Level and Reading Ease
- F-K target compliance status
- Scripture references used (with duplicate detection)
- Summary statistics across all content

The scorecard ensures consistency, tracks scripture diversity, and flags readability issues before they accumulate.

---

## Next Steps

1. Create the remaining `.md` template files based on specifications above
2. Test with one tool guide (IFE recommended)
3. Adjust parameters as needed
4. Build full course content suite

All content will have consistent voice, structure, readability, and biblical integration following these specifications.
