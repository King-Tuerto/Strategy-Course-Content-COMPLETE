# Prompt System Quick Reference

## Two Ways to Generate Content

### Method 1: Quick Default (80% of the time)
Just tell Claude what you want. Uses global defaults.

**Examples:**
- `Write an IFE Matrix tool guide`
- `Write Chapter 5 on Matching Stage Tools`
- `Create a case study on Netflix's pivot to streaming`

→ Uses settings from UPDATE_SETTINGS.md  
→ Fast, simple, consistent

---

### Method 2: Custom Specifications (20% of the time)
Use a template when you need different specs.

**When to use:**
- Different word count
- Different F-K level
- Specific vocabulary required
- Uploaded syllabus/context
- Different question count/Bloom's level

**How:**
1. Open the template:
   - `prompts/TOOL_GUIDE_PROMPT.md` for tool guides
   - `prompts/CHAPTER_PROMPT.md` for chapters
2. Fill in the [blanks]
3. Upload any files to `uploads/` first
4. Copy the filled prompt
5. Paste into Claude Code

---

## Parameter Quick Reference

### Word Counts
| Type | Short | Standard | Long | Very Long |
|------|-------|----------|------|-----------|
| Tool Guide | 500 | 1000 | 1500 | 2000 |
| Chapter | 1500 | 2500 | 3500 | 5000 |
| Case Study | 800 | 1200 | 1800 | 2500 |

### Flesch-Kincaid Levels
- **10-12**: More accessible (undergrad, international students)
- **12-14**: MBA standard
- **14-16**: Academic/rigorous

### Bloom's Taxonomy Levels (Easiest → Hardest)
1. **Remember**: Recall facts
2. **Understand**: Explain concepts
3. **Apply**: Use in new situation
4. **Analyze**: Break down, compare ← *Default*
5. **Evaluate**: Judge, critique
6. **Create**: Design, propose

---

## Common Workflows

### Workflow 1: Standard Semester Content
```
Set globals once (UPDATE_SETTINGS.md):
- F-K 12-14
- 4 MC at Analyze
- 1 Critical Thinking

Then just say:
- "Write an IFE guide"
- "Write Chapter 2"
- etc.
```

### Workflow 2: Quick Student Handout
```
Open: prompts/TOOL_GUIDE_PROMPT.md
Fill in:
- Word count: 500
- F-K: 10-12  
- MC: 2 at Apply
- Critical: 0

Paste into Claude Code
```

### Workflow 3: Comprehensive Chapter
```
Upload syllabus to uploads/
Open: prompts/CHAPTER_PROMPT.md
Fill in all specs
Reference: uploads/Syllabus_Spring2026.pdf
Paste into Claude Code
```

---

## File Upload Tips

### Where to Put Files
Always upload to: `uploads/` folder

### Supported File Types
- PDFs (syllabi, articles)
- Word docs (.docx)
- Text files (.txt, .md)
- Excel (.xlsx) for vocab lists

### How to Reference
In your prompt, write:
- `See syllabus: uploads/MBA660_Syllabus.pdf`
- `Vocabulary list: uploads/Chapter3_Vocab.txt`

Claude Code reads these files automatically.

---

## Default vs Custom — Decision Tree

```
Do you need custom specs? 
    ↓
   NO → Just say "Write an IFE guide"
    ↓
   YES → Is it VERY custom (many parameters)?
        ↓
       YES → Use template (prompts/TOOL_GUIDE_PROMPT.md)
        ↓
        NO → Just override in the prompt:
             "Write an IFE guide, 500 words, F-K 10-12"
```

---

## Remember

**Global defaults** (UPDATE_SETTINGS.md) = baseline for the semester  
**Prompt templates** (prompts/ folder) = when you need different specs  
**Quick overrides** = mention in prompt ("500 words, 3 questions")

Most of the time, defaults work fine. Templates are there when you need precision.
