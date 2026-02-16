# Strategy Course Content System — Complete User Guide

**Version 1.0 | MBA Strategy Course Content Generation**

---

## Table of Contents

1. [What This System Does](#what-this-system-does)
2. [Getting Started](#getting-started)
3. [Understanding the File Structure](#understanding-the-file-structure)
4. [Configuring Your Settings](#configuring-your-settings)
5. [Generating Content — The Basics](#generating-content--the-basics)
6. [Advanced: Custom Parameters](#advanced-custom-parameters)
7. [Working with Uploaded Files](#working-with-uploaded-files)
8. [Quality Control](#quality-control)
9. [Common Workflows](#common-workflows)
10. [Troubleshooting](#troubleshooting)
11. [Best Practices](#best-practices)
12. [Appendix: File Reference](#appendix-file-reference)

---

## What This System Does

This project generates **written instructional content** for your MBA strategy course using AI (Claude Code) while maintaining:

- **Consistent voice** — A senior Christian business executive mentoring new-hire MBAs
- **Controlled readability** — Flesch-Kincaid grade level you specify (default 12-14)
- **Structured pedagogy** — Evidence-based learning design for MBA students
- **Biblical integration** — Natural faith-business connections (not forced or preachy)
- **Assessment alignment** — Questions at specific Bloom's Taxonomy levels
- **Professional quality** — Content ready for Canvas, textbooks, or handouts

### What You Can Generate

- **Tool Guides** — Explications of strategic frameworks (IFE, SWOT, BCG, etc.)
- **Book Chapters** — Full course content chapters with examples and questions
- **Case Studies** — Company scenarios with discussion questions
- **Student Handouts** — Quick reference materials
- **Knowledge Checks** — Multiple choice and critical thinking questions

---

## Getting Started

### Prerequisites

- **VS Code** installed on your computer
- **Claude Code extension** installed and authenticated in VS Code
- The **strategy-course-content** project folder downloaded and extracted

### Initial Setup (One Time Only)

#### Step 1: Install the Project

1. Download `Strategy-Course-Content-COMPLETE.zip`
2. Extract it to: `C:\Users\[YourName]\Desktop\Spring2026\660\strategy-course-content`
   (Adjust the path as needed for your file structure)

#### Step 2: Open in VS Code

1. Launch **VS Code**
2. Click **File → Open Folder**
3. Navigate to the `strategy-course-content` folder you just extracted
4. Click **Select Folder**

#### Step 3: Verify Setup

Look at the **Explorer panel** (left sidebar). You should see:

```
STRATEGY-COURSE-CONTENT
├── USER_GUIDE.md           ← This file
├── QUICKSTART.md
├── UPDATE_SETTINGS.md
├── prompts/
├── uploads/
├── .claude/
├── skills/
└── output/
```

If you see this structure ✅ you're ready to proceed.

#### Step 4: Open Claude Code

1. Look for the **Claude icon** on the left sidebar (looks like ⬡ or Anthropic logo)
2. Click it to open the Claude Code panel
3. At the **bottom** of the Claude Code panel, verify it shows your project path:
   `📁 C:\...\strategy-course-content`

If it shows a different folder, click the path and select the correct folder.

---

## Understanding the File Structure

### Core System Files

| File/Folder | What It Does | When You Use It |
|-------------|--------------|-----------------|
| **USER_GUIDE.md** | Complete documentation (this file) | Reference when learning the system |
| **QUICKSTART.md** | Quick reference for common tasks | Daily quick lookups |
| **UPDATE_SETTINGS.md** | Interactive settings configurator | Start of semester, when changing defaults |
| **.claude/CLAUDE.md** | Tells Claude Code what this project is | Never edit (auto-read by Claude Code) |
| **skills/** | The "brain" — writing rules and templates | Rarely view, sometimes edit parameters |
| **prompts/** | Fill-in templates for custom parameters | When you need non-default settings |
| **uploads/** | Your syllabi, vocab lists, reference docs | Put files here before referencing them |
| **output/** | Generated content appears here | Check here after Claude Code runs |

### Skills Folder Contents

| File | Purpose | Edit This? |
|------|---------|------------|
| `VOICE.md` | Defines your writing persona and tone | Rarely — only if voice needs adjustment |
| `FLESCH_KINCAID.md` | Readability targeting | Yes — to change default F-K level |
| `CONTENT_SYSTEM_README.md` | Complete specifications | Yes — to change default question counts, Bloom's level |
| `BIBLICAL_INTEGRATION.md` | Guidelines on faith integration | Read for reference, rarely edit |
| `templates/` | Folder for reusable structures | Future use (not critical now) |

### Prompts Folder Contents

| File | When to Use |
|------|-------------|
| `TOOL_GUIDE_PROMPT.md` | Creating a tool guide with custom parameters |
| `CHAPTER_PROMPT.md` | Writing a chapter with specific requirements |
| `QUICK_OVERRIDE_GUIDE.md` | Learning one-liner syntax for quick overrides |

---

## Configuring Your Settings

### Understanding: Global vs. Custom Settings

**Content-Type-Specific Defaults** (set once per semester):
- Different defaults for tool guides vs. chapters vs. cases
- Tool guides: 4 questions at Analyze level
- Chapters: 5 questions at Analyze level
- Cases: 6 questions at Analyze level
- Managed through SETTINGS_MANAGER.md

**Custom Settings** (per individual piece):
- Override any default for one specific output
- Add word count targets
- Include specific vocabulary
- Attach syllabi or reference materials

Most of the time, you'll use **content-type defaults**. Override only when needed.

---

### Setting Content-Type Defaults

**When:** Start of each semester, or when your audience/requirements change.

**How:**

1. In Explorer, click **SETTINGS_MANAGER.md**
2. Scroll to **"How to Update Settings"**
3. Choose **Option 1** (update one content type) or **Option 2** (update all)
4. Copy the prompt
5. Paste into **Claude Code** chat
6. Answer the questions Claude asks
7. Claude updates the settings and confirms changes

**Example prompt (Option 1):**
```
I want to update my content generation settings for CHAPTERS.
Show me the current defaults, then ask me what I'd like to change.
```

Claude Code will:
- Show you current chapter settings
- Ask what you want to change
- Update `CONTENT_SYSTEM_README.md`
- Confirm what changed

**Recommendation:** Start with these settings for MBA courses:
- Tool Guides: F-K 12-14, 4 Analyze questions, 1 critical thinking
- Chapters: F-K 12-14, 5 Analyze questions, 1 critical thinking  
- Cases: F-K 12-14, 6 Analyze questions, 1 critical thinking
- All: Biblical integration = Natural

You can always adjust later if content is too easy/hard for your students.

---

## Generating Content — The Basics

### The Simple Workflow (Uses Global Defaults)

This works for 80% of your content needs:

1. **Open Claude Code** (make sure project folder is correct)
2. **Type what you want:**
   ```
   Write a complete tool guide for the IFE Matrix using all content skills.
   ```
3. **Press Enter**
4. **Wait** while Claude Code generates (30-90 seconds for a tool guide)
5. **Find output** in `output/tool-guides/IFE_Tool_Guide.md`

That's it. No configuration needed — it uses your global settings automatically.

---

### What Claude Code Is Doing

When you type "Write a complete tool guide for the IFE Matrix":

1. Reads `.claude/CLAUDE.md` → understands this is a writing project
2. Reads `skills/content/VOICE.md` → learns your voice and tone
3. Reads `skills/content/FLESCH_KINCAID.md` → checks target reading level
4. Reads `skills/content/CONTENT_SYSTEM_README.md` → gets question count, Bloom's level
5. **Generates content** following all those rules
6. **Saves** to `output/` folder

All of this happens automatically. You just type what you want.

---

### Content Types You Can Generate

#### Tool Guides

**Prompt:**
```
Write a complete tool guide for the [TOOL NAME] using all content skills.
```

**Examples:**
- IFE Matrix
- EFE Matrix
- SWOT Analysis
- BCG Matrix
- SPACE Matrix
- Grand Strategy Matrix
- CPM (Competitive Profile Matrix)
- IE Matrix
- QSPM
- Perceptual Map

**Output:** A complete explication including purpose, instructions, scoring guide, interpretation, examples, and knowledge check questions.

---

#### Chapters

**Prompt:**
```
Write Chapter [N] on [TOPIC] using all content skills.
```

**Examples:**
```
Write Chapter 3 on Internal Analysis using all content skills.
```
```
Write Chapter 7 on Strategy Implementation using all content skills.
```

**Output:** Full chapter with opening hook, learning objectives, explanations, examples, tool instructions (if applicable), biblical integration, summary, and reflection questions.

---

#### Case Studies

**Prompt:**
```
Create a case study on [COMPANY] [SCENARIO] using all content skills.
```

**Examples:**
```
Create a case study on Starbucks' 2008 turnaround using all content skills.
```
```
Create a case study on Netflix's shift from DVDs to streaming using all content skills.
```

**Output:** Company background, strategic challenge, context, data, decision point, and discussion questions.

---

## Advanced: Custom Parameters

### When to Use Custom Parameters

Use custom settings when:
- You need a shorter/longer piece than normal
- You're writing for a different audience (undergrad vs. MBA vs. exec ed)
- You want more/fewer questions
- You need to include specific vocabulary
- You're referencing a syllabus section
- You want a specific company as the example

### Method 1: Quick One-Liner Overrides

Just tell Claude Code what you want to change:

**Example 1: Shorter guide with fewer questions**
```
Write an IFE guide: 500 words, 3 Apply questions
```

**Example 2: More accessible reading level**
```
Write a SWOT chapter: F-K 10-12, use simple examples
```

**Example 3: Specific vocabulary and example**
```
Write a BCG guide: include terms: market share, growth rate, cash cow, star; use Tesla as example
```

**Example 4: Custom everything**
```
Write an EFE guide: 800 words, F-K 11-12, 5 questions (3 Apply, 2 Analyze), 
define: opportunities, threats, external factors; use Walmart as example
```

Claude Code parses these natural language instructions and applies them.

**Full syntax guide:** See `prompts/QUICK_OVERRIDE_GUIDE.md`

---

### Method 2: Using the Fill-in Templates

For complex customization with many parameters, use the templates.

#### For Tool Guides:

1. Open `prompts/TOOL_GUIDE_PROMPT.md` in VS Code
2. Fill in the bracketed fields:
   ```
   Tool Name: [ SWOT Analysis ]
   Word Count Target: [ 600 ] words
   Flesch-Kincaid Level: [ 10-12 ]
   Multiple Choice Questions: [ 3 ] at [ Apply ] level
   ... etc.
   ```
3. Scroll to the bottom "COPY THIS PROMPT" section
4. The template auto-fills based on what you entered above
5. Copy that filled-in prompt
6. Paste into Claude Code
7. Press Enter

#### For Chapters:

Same process with `prompts/CHAPTER_PROMPT.md`.

**Advantages of templates:**
- Ensures you don't forget any parameters
- Easy to save and reuse configurations
- Clear structure for complex requests

---

## Working with Uploaded Files

### What You Can Upload

- **Syllabi** (PDF or Word) — for context on learning objectives
- **Vocabulary lists** (text or Word) — required terms to define
- **Reference materials** (PDF, text) — background on companies or concepts
- **Previous assignments** — to maintain consistency

### How to Upload and Reference

#### Step 1: Put Files in the Uploads Folder

1. In Windows Explorer, navigate to your project folder
2. Open the `uploads/` subfolder
3. Copy your files into this folder
4. Name them clearly: `syllabus-chapter3.pdf`, `vocab-week5.txt`, etc.

#### Step 2: Reference in Your Prompt

**For syllabi:**
```
Write Chapter 3 using the syllabus context from uploads/syllabus-chapter3.pdf.
Include all learning objectives listed there.
```

**For vocabulary:**
```
Write an IFE guide that defines all terms from uploads/vocab-internal-analysis.txt.
```

**For reference materials:**
```
Create a case study on Nike using background from uploads/nike-history.pdf.
```

#### Step 3: Alternatively, Attach Files Directly

Some versions of Claude Code allow file attachments. If available:
1. Type your prompt
2. Click the **attachment icon** (📎) in Claude Code
3. Select files from anywhere on your computer
4. Claude Code uploads them temporarily and reads them

---

## Quality Control

### Checking Flesch-Kincaid Scores

After Claude Code generates content, verify the reading level:

#### Using Microsoft Word:

1. Open the generated `.md` file in **Word**
2. **File → Options → Proofing**
3. Check ☑ **"Show readability statistics"**
4. Click **OK**
5. Press **F7** (or Review → Spelling & Grammar)
6. Let it run through the document
7. At the end, a dialog shows **Flesch-Kincaid Grade Level**

**Is it within your target range?**
- Target 12-14, got 13.2 → ✅ Perfect
- Target 12-14, got 16.5 → ❌ Too complex, ask Claude Code to simplify
- Target 12-14, got 9.8 → ❌ Too simple, ask Claude Code to add sophistication

#### If Score is Off:

**Too high (too complex):**
```
Rewrite this content at Flesch-Kincaid grade level 12. 
Break up long sentences and simplify vocabulary where possible.
```

**Too low (too simple):**
```
Rewrite this content at Flesch-Kincaid grade level 13. 
Add more sophisticated vocabulary and vary sentence length.
```

---

### Checking Voice and Tone

Read a paragraph out loud. Ask yourself:

**Does this sound like:**
- ✅ A senior executive with 20 years of experience talking to a new MBA hire?
- ✅ Direct, honest, grounded in reality?
- ✅ Practical examples before theory?

**Or does it sound like:**
- ❌ A generic business textbook?
- ❌ An academic journal article?
- ❌ A motivational speaker?

**If voice is off:**
```
Rewrite this following VOICE.md more closely. Too academic/formal right now. 
Should sound like an experienced executive mentoring a new hire.
```

---

### Checking Biblical Integration

Review any scripture references or faith-business connections:

**Good integration:**
- Feels natural, illuminates the business concept
- Uses wisdom literature (Proverbs, Ecclesiastes) or leadership passages
- Connects to stewardship, calling, integrity
- Example: "Proverbs 28:13 applies directly here: concealing weaknesses leads to failure, but honest assessment enables improvement."

**Forced integration:**
- Feels gimmicky or shoehorned in
- Uses obscure passages requiring explanation
- Makes tenuous connections
- Example: "Just as Jesus had 12 disciples, the QSPM has up to 12 factors..."

**If integration is forced:**
```
Remove the biblical reference on page 2. It feels forced. 
Only include scripture where it genuinely illuminates the concept.
```

---

### Checking Assessment Questions

Review the knowledge check questions:

**Multiple Choice:**
- Stem (question) is clear and unambiguous
- All 4 options are plausible
- Only one is clearly correct
- Distractors are based on common misconceptions
- At the Bloom's level you specified

**Critical Thinking:**
- Requires judgment, not just recall
- Multiple valid perspectives exist
- Connects to ethics or real-world dilemmas
- Can't be answered in one sentence

**If questions are weak:**
```
Rewrite question 3. Too easy — it's testing recall not analysis.
Make it require students to apply the IFE concept to a scenario.
```

---

## Common Workflows

### Workflow 1: Build a Complete Tool Library

**Goal:** Generate guides for all 10 strategic tools in one session.

**Prompt:**
```
Write complete tool guides for each of these tools using all content skills:
1. IFE Matrix
2. EFE Matrix
3. CPM
4. SWOT Analysis
5. SPACE Matrix
6. Grand Strategy Matrix
7. BCG Matrix
8. IE Matrix
9. QSPM
10. Perceptual Map

Save each to output/tool-guides/ with the tool name in the filename.
```

**Time:** 10-15 minutes total  
**Output:** 10 complete guides ready to upload to Canvas

---

### Workflow 2: Generate Week 3 Course Materials

**Goal:** Create all materials for one week of class.

**Step 1: Chapter**
```
Write Chapter 3 on Internal Analysis: 2000 words, 
include IFE Matrix explanation, 5 discussion questions
```

**Step 2: Tool Guide**
```
Write a detailed IFE Matrix guide: 1500 words, 
6 questions (4 Analyze, 2 Apply)
```

**Step 3: Case Study**
```
Create a case on Southwest Airlines' competitive advantage: 
1200 words, focus on how to use IFE to assess their position, 
include ethical considerations
```

**Step 4: Quick Reference**
```
Write a 1-page IFE quick reference card: 
bullet points only, F-K 10-11, no questions
```

---

### Workflow 3: Adjust Difficulty Mid-Semester

**Situation:** Your MBA students are struggling with the reading level. Content is too complex.

**Solution:**

1. Open `UPDATE_SETTINGS.md`
2. Run the settings update prompt
3. Change F-K from 12-14 to **10-12**
4. Regenerate the problematic content:
   ```
   Rewrite Chapter 4 at the updated Flesch-Kincaid level (10-12).
   ```

Or just override for that one piece:
```
Rewrite Chapter 4 at F-K 10-12, shorter sentences, simpler vocabulary.
```

---

### Workflow 4: Create Tiered Question Sets

**Goal:** Same content, but three difficulty levels for differentiation.

**Basic Level (Remember/Understand):**
```
Write 5 multiple choice questions on the IFE Matrix at Remember level. 
Students should only need to recall definitions and basic concepts.
```

**Standard Level (Apply/Analyze):**
```
Write 5 multiple choice questions on the IFE Matrix at Analyze level.
Students must interpret scenarios and apply the tool.
```

**Advanced Level (Evaluate/Create):**
```
Write 5 multiple choice questions on the IFE Matrix at Evaluate level.
Students must critique IFE analyses or design their own.
```

---

## Troubleshooting

### Problem: Claude Code reads from wrong project

**Symptoms:** You ask for a tool guide but Claude Code talks about HTML tools or different content.

**Fix:**
1. Look at the **bottom** of Claude Code panel
2. You'll see a folder path like `📁 C:\...\strategy-tools-skill`
3. **Click that path**
4. Navigate to `strategy-course-content`
5. Click **Select Folder**

Now Claude Code is looking at the right project.

---

### Problem: Generated files don't appear in output/

**Symptoms:** Claude Code says it created a file, but you don't see it.

**Fix:**
1. In Explorer, **right-click** the `output` folder
2. Click **Refresh** (or press F5)
3. File should appear

If still missing:
1. Ask Claude Code: "Where did you save that file?"
2. It will show you the exact path
3. Navigate there in Explorer

---

### Problem: Content sounds generic, not like my voice

**Symptoms:** Generated content reads like a textbook, not a senior executive.

**Likely Cause:** Claude Code didn't read VOICE.md

**Fix:**
```
Please read skills/content/VOICE.md and rewrite this content 
in that voice. Current version is too formal and academic.
```

Or check your global settings — run UPDATE_SETTINGS.md to verify voice preference.

---

### Problem: Flesch-Kincaid score way off target

**Symptoms:** You set F-K 12-14, but content scores 9 or 17.

**Fix for too high (complex):**
```
This content scored F-K 17. Please rewrite at F-K 12-14.
Break long sentences at natural pauses and simplify jargon.
```

**Fix for too low (simple):**
```
This content scored F-K 9. Please rewrite at F-K 12-14.
Vary sentence length and use appropriate business terminology.
```

**Prevention:** Always specify F-K level in your prompt if it's critical:
```
Write a chapter on SWOT: F-K 12-14 (verify score before finishing)
```

---

### Problem: Biblical references feel forced or inappropriate

**Symptoms:** Scripture citations don't fit naturally or seem gimmicky.

**Fix:**
```
Remove the biblical reference in paragraph 3. It feels forced.
Only include scripture where it genuinely illuminates the business concept.
Stewardship principles work here; Trinity analogies do not.
```

**Prevention:** Set biblical integration to "natural" in global settings, and remind Claude Code:
```
Write this chapter with biblical integration only where it naturally fits.
Don't force scripture into every section.
```

---

### Problem: Questions too easy or too hard

**Symptoms:** MC questions test recall when you wanted analysis, or vice versa.

**Fix:**
```
Rewrite questions 2-4 at Analyze level instead of Remember level.
They should require students to interpret scenarios, not just recall definitions.
```

Or use Bloom's level override:
```
Write 5 more questions for this chapter at Evaluate level.
Students should critique strategic decisions or judge alternatives.
```

---

### Problem: Output is way longer/shorter than expected

**Fix:**
- Specify word count: `Write this as 800 words`
- Ask for revision: `Condense this to 500 words maximum`
- Set target in template: Use TOOL_GUIDE_PROMPT.md and specify exact count

---

### Problem: Can't find a generated file

**Where to look:**

Generated content goes into subfolders of `output/`:
- Tool guides → `output/tool-guides/`
- Chapters → `output/chapters/`
- Cases → `output/cases/`
- Questions → `output/questions/`

If you still can't find it:
```
Where did you save the IFE guide I just asked for? 
Show me the exact file path.
```

---

## Best Practices

### Start with Defaults, Override Rarely

**Do this:**
- Set thoughtful global defaults at semester start
- Use them for 80% of content
- Override only when truly needed

**Don't do this:**
- Customize every single prompt
- Change settings constantly
- Never establish a baseline

**Why:** Consistency is valuable. Students benefit from predictable structure and difficulty.

---

### Test Content with Real Students

**Do this:**
- Generate a chapter, have a student read it, ask for feedback
- Check if F-K level matches their actual reading comfort
- Adjust based on real performance, not assumptions

**Measure:**
- Time to complete reading
- Comprehension (can they answer questions correctly?)
- Engagement (do they find it interesting or tedious?)

---

### Keep a Content Log

Create a simple document tracking what you've generated:

```
Date       | Content              | Settings                    | Notes
-----------|----------------------|-----------------------------|-----------------
2/15/2026  | IFE Tool Guide      | F-K 12-14, 4 Analyze Qs     | Used with Week 3
2/15/2026  | Chapter 3           | F-K 12-14, 5 questions      | Added Apple example
2/16/2026  | Starbucks Case      | 1200 words, ethics focus    | Updated for 2008 crisis
```

Helps you remember what settings produced good results.

---

### Maintain Version Control

**When updating existing content:**
1. Don't delete the old version immediately
2. Save new version as `Chapter_3_v2.md`
3. Compare, decide which is better
4. Then delete the old one

**Why:** Sometimes the "improved" version is actually worse. Keep originals until you're sure.

---

### Organize Output Folder

As content accumulates, organize it:

```
output/
├── tool-guides/
│   ├── published/          ← Finalized, uploaded to Canvas
│   └── drafts/             ← Still iterating
├── chapters/
│   ├── spring-2026/
│   └── fall-2026/
└── cases/
    └── reviewed/
```

Prevents clutter and confusion.

---

### Share Settings with TAs or Co-Instructors

If others will generate content:
1. Export your configured `FLESCH_KINCAID.md` and `CONTENT_SYSTEM_README.md`
2. Share those files
3. They replace theirs with yours
4. Now everyone generates consistent content

---

### Iterate, Don't Expect Perfection First Try

**Typical workflow:**
1. Generate content with prompt
2. Review output
3. Ask for 2-3 refinements
4. Final version is excellent

**Don't expect:**
- Perfect output on first generation
- Zero need for human review
- No editing required

AI is a drafting tool, not a replacement for your expertise.

---

## Appendix: File Reference

### Quick Lookup — "I need to..."

| I need to... | File to use |
|--------------|-------------|
| Set default F-K level | Edit `skills/content/FLESCH_KINCAID.md` |
| Change default question count | Edit `skills/content/CONTENT_SYSTEM_README.md` |
| Adjust voice/tone | Edit `skills/content/VOICE.md` (rarely needed) |
| Create tool guide with custom params | Use `prompts/TOOL_GUIDE_PROMPT.md` |
| Create chapter with syllabus | Use `prompts/CHAPTER_PROMPT.md` |
| Learn one-liner syntax | Read `prompts/QUICK_OVERRIDE_GUIDE.md` |
| Configure all settings at once | Run prompt from `UPDATE_SETTINGS.md` |
| Get quick help | Read `QUICKSTART.md` |
| Understand the system | Read `USER_GUIDE.md` (this file) |

---

### Complete File Tree

```
strategy-course-content/
│
├── USER_GUIDE.md                          ← You are here
├── QUICKSTART.md                          ← Quick reference
├── UPDATE_SETTINGS.md                     ← Interactive settings configurator
│
├── .claude/
│   └── CLAUDE.md                          ← Auto-read by Claude Code (don't edit)
│
├── skills/
│   └── content/
│       ├── VOICE.md                       ← Writing voice definition
│       ├── FLESCH_KINCAID.md             ← Readability settings
│       ├── CONTENT_SYSTEM_README.md       ← Complete specifications
│       ├── BIBLICAL_INTEGRATION.md        ← (Future - not critical)
│       ├── PEDAGOGY.md                    ← (Future - not critical)
│       ├── STRUCTURE.md                   ← (Future - not critical)
│       ├── ASSESSMENT.md                  ← (Future - not critical)
│       └── templates/                     ← (Future - not critical)
│
├── prompts/
│   ├── TOOL_GUIDE_PROMPT.md              ← Fill-in template for tool guides
│   ├── CHAPTER_PROMPT.md                  ← Fill-in template for chapters
│   └── QUICK_OVERRIDE_GUIDE.md           ← One-liner syntax reference
│
├── uploads/                               ← Put your syllabi, vocab lists here
│
└── output/                                ← Generated content appears here
    ├── tool-guides/
    ├── chapters/
    ├── cases/
    └── questions/
```

---

## Support and Updates

### Getting Help

**For technical issues:**
- Check the Troubleshooting section above first
- Try asking Claude Code directly: "Why isn't this working?"

**For content quality issues:**
- Review the Quality Control section
- Adjust settings in FLESCH_KINCAID.md or CONTENT_SYSTEM_README.md
- Use custom prompts to override specific aspects

**For questions about the system:**
- Reread relevant sections of this guide
- Check QUICKSTART.md for common tasks

---

### Future Enhancements

Potential additions to this system:
- Pre-built assessment question banks
- Slide deck generation
- Integration with Canvas LMS
- Student self-assessment tools
- Peer review rubrics

These can be added to the `skills/content/` folder as new `.md` files following the same pattern.

---

## Conclusion

You now have a complete content generation system that produces:
- Consistent, professional instructional materials
- At the exact reading level you specify
- In a voice that reflects your teaching philosophy
- With assessment aligned to learning objectives
- All while maintaining biblical integration where appropriate

**The system works in two modes:**

1. **Easy mode** (80% of the time): "Write an IFE guide" → done
2. **Custom mode** (20% of the time): Specify exactly what you need

Both modes produce publication-ready content that saves you dozens of hours of writing time while maintaining the quality and voice students deserve.

**Welcome to dramatically more efficient course development.**

---

*Version 1.0 | Created February 2026 | For questions or suggestions, update this guide and regenerate.*
