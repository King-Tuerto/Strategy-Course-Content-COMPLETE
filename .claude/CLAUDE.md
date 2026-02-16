# Strategy Course Content — Writing Project

## What This Project Is

This project is for **writing instructional content** for your MBA strategy course:
- Tool guides (explications of strategic frameworks)
- Book chapters
- Case studies  
- Student handouts
- Knowledge check questions

This is NOT for building HTML tools. (That's a separate frozen project.)

---

## Voice & Style

All content written in this project follows the voice of a **senior Christian business executive speaking to newly hired MBAs**:
- Direct, honest, grounded in reality
- Biblically informed where natural (not preachy)
- Practical first, theoretical second
- Flesch-Kincaid grade level 16-18 (academic, adjustable)

All content must also comply with **GCU institutional writing standards** (documented in `VOICE.md > GCU Institutional Writing Standards`):
- APA citations throughout; References section at end of each chapter/guide
- Key terms bolded on first use; Key Terms section at end (alphabetical with definitions)
- No text emphasis (bold/italic/caps) except for key terms and APA formatting
- Tables/figures numbered by chapter; bolded number + italic title; alt text required
- Headings in title case, no colons, no periods
- Conclusions review concepts without listing; reinforce importance
- No external hyperlinks without pre-approval

---

## MANDATORY: Pre-Writing Checklist

**BEFORE writing ANY content (chapter, tool guide, case study, handout), you MUST complete BOTH steps below. No exceptions. No skipping. Every time.**

### Step 1 — Ask the User These Questions

Use AskUserQuestion to collect ALL of the following before writing. Do not start writing until every question is answered.

1. **Syllabus/Outline:** "Do you have a syllabus or course outline I should follow? If so, provide the file path or paste the relevant section."
2. **Vocabulary/Key Terms:** "Do you have a required vocabulary or key terms list for this piece? If so, provide it. Otherwise I will identify key terms as I write."
3. **Topic:** "What is the specific topic? (e.g., Chapter 3: Internal Analysis, Tool Guide: SPACE Matrix)"
4. **Company Examples:** "Which companies should I use as application examples, or should I choose?"
5. **Framework/Model:** "Any specific framework or textbook model to use — or avoid?"
6. **Special Instructions:** "Anything else specific to this piece? (word count override, extra sections, specific emphasis, etc.)"

### Step 2 — Read These Files

After getting user answers, read these files before writing:

1. `skills/content/VOICE.md` — How to write (tone, persona, style, GCU standards)
2. `skills/content/FLESCH_KINCAID.md` — Readability targeting
3. `skills/content/CONTENT_SYSTEM_README.md` — Complete system overview, templates, parameters

For specific content types also read:
- **Tool guides:** templates/TOOL_GUIDE.md (if it exists)
- **Chapters:** templates/CHAPTER.md (if it exists)
- **Cases:** templates/CASE_STUDY.md (if it exists)
- **Questions:** Check parameters in CONTENT_SYSTEM_README.md

---

## Default Parameters (Adjustable)

```yaml
flesch_kincaid_target: 16-18
mc_question_count: 4
blooms_level: analyze
critical_thinking_count: 1
biblical_integration: natural  # where it fits, not forced
```

Change these in the relevant `.md` files as needed.

---

## Output Location

Save all completed content to: `output/`

Organize by type:
- `output/tool-guides/` — Tool explications
- `output/chapters/` — Book chapters
- `output/cases/` — Case studies
- `output/handouts/` — Student materials

---

## Example Prompts

### Write a tool guide:
```
Write a complete tool guide for the IFE Matrix using all content 
skills. F-K 12-14, 4 Analyze-level MC questions, 1 critical 
thinking question.
```

### Write a chapter:
```
Write Chapter 3 on Internal Analysis using content skills. 
Include IFE tool explanation. F-K 12-14. Biblical integration 
where natural.
```

### Create a case:
```
Create a case study on [Company] using content skills. 
Strategic challenge: [topic]. Tools: IFE, SWOT. 
Include ethical dimension.
```

---

## This Project Does NOT

- Build HTML tools (that's the other project)
- Generate interactive widgets
- Create technical documentation

This project is purely for **written instructional content** in a consistent voice.
