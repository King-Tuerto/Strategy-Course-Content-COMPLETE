# Chapter Custom Prompt Template

## When to Use This
Use when writing a chapter with custom specs.
For standard chapters, just say: "Write Chapter 3 on Internal Analysis"

---

## Instructions
1. Fill in ALL the **[blanks]** below
2. Upload syllabus/vocab to `uploads/` first if needed
3. Copy the filled-in prompt
4. Paste into Claude Code

---

## FILL-IN PROMPT

```
Write Chapter **[number]**: **[Chapter Title]** using all content skills.

Parameters:
- Word count: **[1500/2000/3000/4000]** words
- F-K level: **[10-12/12-14/14-16]**
- Learning objectives: **[list 3-5 objectives starting with action verbs]**

Content structure:
- Include tool(s): **[tool names, or "none"]**
- Real company examples: **[2-3 company names, or "your choice"]**
- Biblical integration: **[natural/frequent/minimal]**

Required vocabulary:
- **[term 1]**, **[term 2]**, **[term 3]**, **[etc]**

Assessment:
- MC questions: **[number]** at **[Bloom's level]** level
- Discussion questions: **[number]** open-ended

Context:
- Chapter **[X]** of **[total]** in the book
- Previous chapters covered: **[topics]**
- Next chapter will cover: **[topic]**
- See syllabus: uploads/**[filename if applicable]**

Special instructions:
- **[any specific requests or constraints]**

Save to: output/chapters/Chapter_**[XX]**_**[ShortTitle]**.md
```

---

## Example (Filled In)

```
Write Chapter 3: Internal Factor Analysis using all content skills.

Parameters:
- Word count: 2500 words
- F-K level: 12-14
- Learning objectives: 
  - Evaluate organizational strengths and weaknesses systematically
  - Calculate weighted scores for internal factors
  - Interpret IFE Matrix results for strategic decisions

Content structure:
- Include tool(s): IFE Matrix
- Real company examples: Starbucks, Apple
- Biblical integration: natural

Required vocabulary:
- internal factors, weighted score, competitive advantage, core competency, 
  distinctive competence, VRIO framework

Assessment:
- MC questions: 5 at analyze level
- Discussion questions: 3 open-ended

Context:
- Chapter 3 of 12 in the book
- Previous chapters covered: strategy overview, external analysis
- Next chapter will cover: matching stage tools (SWOT)
- See syllabus: uploads/MBA660_Syllabus_Spring2026.pdf

Special instructions:
- This is students' first exposure to internal analysis
- Emphasize honesty in self-assessment (link to Proverbs 28:13)
- Include a worked IFE example for a familiar company

Save to: output/chapters/Chapter_03_Internal_Analysis.md
```
