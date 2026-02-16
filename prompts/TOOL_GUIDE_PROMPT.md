# Tool Guide Custom Prompt Template

## When to Use This
Use when you need specifications different from your global defaults.
For standard guides, just say: "Write an IFE Matrix guide"

---

## Instructions
1. Fill in ALL the **[blanks]** below
2. Upload any files (syllabus, vocab) to `uploads/` folder first
3. Copy the entire filled-in prompt
4. Paste into Claude Code

---

## FILL-IN PROMPT (Replace all **[blanks]**)

```
Write a tool guide for the **[TOOL NAME]** using all content skills.

Parameters:
- Word count: **[500/1000/1500/2000]** words  
- F-K level: **[10-12/12-14/14-16]**
- MC questions: **[number]** at **[Bloom's level]** level
- Critical thinking: **[0/1/2]** questions on **[ethics/judgment/application]**

Required vocabulary (define naturally):
- **[term 1]**, **[term 2]**, **[term 3]**

Context:
- Week **[X]** of course
- Students already know: **[concepts]**
- See syllabus: uploads/**[filename if uploaded]**

Save to: output/tool-guides/**[TOOL_NAME]**_Guide.md
```

---

## Example (Filled In)

```
Write a tool guide for the IFE Matrix using all content skills.

Parameters:
- Word count: 500 words
- F-K level: 10-12
- MC questions: 3 at apply level
- Critical thinking: 1 question on application

Required vocabulary (define naturally):
- weighted score, internal factors, competitive advantage

Context:
- Week 3 of course
- Students already know: basic strategy concepts
- See syllabus: uploads/MBA660_Syllabus.pdf

Save to: output/tool-guides/IFE_Guide.md
```
