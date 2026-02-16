# Content Settings Manager

**Version 2.0 — Organized by Content Type**

---

## What This Does

This settings manager lets you configure defaults for each content type separately:
- **Tool Guides** can have 4 questions at Analyze level
- **Chapters** can have 6 questions at Mixed levels
- **Case Studies** can have 8 questions at Evaluate level

When you generate content, Claude Code automatically uses the right defaults for that type.

---

## Current Settings

### Tool Guides (Default Settings)

| Parameter | Current Value |
|-----------|---------------|
| Word Count | 1000-1500 |
| Flesch-Kincaid | 12-14 |
| MC Questions | 4 |
| Bloom's Level | Analyze |
| Critical Thinking | 1 |
| Biblical Integration | Natural |

---

### Chapters (Default Settings)

| Parameter | Current Value |
|-----------|---------------|
| Word Count | 2000 |
| Flesch-Kincaid | 12-14 |
| MC Questions | 5 |
| Bloom's Level | Analyze |
| Critical Thinking | 1 |
| Biblical Integration | Natural |

---

### Case Studies (Default Settings)

| Parameter | Current Value |
|-----------|---------------|
| Word Count | 1200-1500 |
| Flesch-Kincaid | 12-14 |
| MC Questions | 6 |
| Bloom's Level | Analyze |
| Critical Thinking | 1 |
| Biblical Integration | Natural |

---

## How to Update Settings

### Option 1: Update One Content Type (Recommended)

Copy this prompt and paste into Claude Code:

```
I want to update my content generation settings for [TOOL GUIDES / CHAPTERS / CASE STUDIES].

Show me the current defaults for that content type, then ask me what I'd like to change.

After I tell you, update the appropriate section in skills/content/CONTENT_SYSTEM_README.md and confirm what changed.
```

**Replace the bracketed part** with the content type you want to configure.

---

### Option 2: Update All Content Types

Copy this prompt and paste into Claude Code:

```
I want to configure content generation settings for all content types.

Ask me for settings for each content type one at a time:
1. Tool Guides
2. Chapters
3. Case Studies

For each, show current defaults and ask what I want to change.

Settings to configure:
- Word count target
- Flesch-Kincaid level (10-12, 12-14, or 14-16)
- MC question count
- Bloom's Taxonomy level (Remember, Understand, Apply, Analyze, Evaluate, Create, or Mixed)
- Critical thinking question count
- Biblical integration preference (Natural, Frequent, Minimal)

After collecting all changes, update skills/content/CONTENT_SYSTEM_README.md and confirm all updates.
```

---

### Option 3: Quick Update (One-Liner)

If you just want to change one thing:

```
Update chapter defaults: MC questions = 6, Bloom's = Mixed
```

Or:

```
Update tool guide defaults: word count = 800, F-K = 11-13
```

Claude Code will update just those parameters.

---

## Understanding the Parameters

### Word Count
- **Tool Guides:** 1000-1500 (comprehensive explanation)
- **Chapters:** 2000 (full teaching content)
- **Case Studies:** 1200-1500 (scenario + context)
- **Quick Reference:** 500 (brief, bullets only)

Adjust based on your curriculum needs and student reading time.

---

### Flesch-Kincaid Level
- **10-12:** More accessible (undergrad, international students, quick reads)
- **12-14:** MBA standard (sophisticated but clear)
- **14-16:** Academic (peer-reviewed journals, research)

Start with 12-14 for MBA courses. Adjust if students struggle or find it too easy.

---

### MC Question Count
- **Tool Guides:** 3-5 (checks understanding of the framework)
- **Chapters:** 5-8 (comprehensive coverage of concepts)
- **Case Studies:** 6-10 (application and judgment questions)

More questions = more thorough assessment but longer to complete.

---

### Bloom's Taxonomy Levels

| Level | What Students Do | When to Use |
|-------|------------------|-------------|
| **Remember** | Recall facts, definitions | Intro courses, vocab checks |
| **Understand** | Explain concepts in own words | Foundational knowledge |
| **Apply** | Use tools in scenarios | Most tool guides |
| **Analyze** | Compare, contrast, break down | Most MBA courses (default) |
| **Evaluate** | Judge, critique, recommend | Advanced courses, cases |
| **Create** | Design new strategies, proposals | Capstone, final projects |
| **Mixed** | Variety of levels | Comprehensive exams, chapters |

**Mixed** means questions span multiple levels (e.g., 2 Apply, 2 Analyze, 1 Evaluate).

---

### Critical Thinking Questions

These are open-ended paragraph questions requiring judgment:
- **1 question:** Standard (most content)
- **2 questions:** Important topics needing deeper reflection
- **0 questions:** Quick assessments or when not needed

These questions focus on ethics, stakeholder dilemmas, and real-world complexity.

---

### Biblical Integration

| Setting | What It Means | When to Use |
|---------|---------------|-------------|
| **Natural** | Include scripture where it genuinely illuminates | Default for MBA courses |
| **Frequent** | Most sections have some faith connection | Christian university, theology focus |
| **Minimal** | Rare, only when very natural | Secular context, diverse students |

See `skills/content/VOICE.md` for examples of good vs. forced integration.

---

## Viewing Current Settings

To see what's currently configured without changing anything:

```
Show me my current content generation settings for all content types
```

Claude Code will display a table with all defaults.

---

## Resetting to Defaults

To restore original recommended settings:

```
Reset all content settings to recommended MBA defaults
```

This sets:
- All F-K levels to 12-14
- Tool guides: 4 Analyze questions
- Chapters: 5 Analyze questions  
- Cases: 6 Analyze questions
- Biblical integration: Natural

---

## After Changing Settings

Settings take effect **immediately** for new content generation.

**Test it:**
```
Write a chapter on SWOT Analysis
```

Claude Code will use your new chapter defaults automatically.

---

## Tips for Effective Settings

### Start Conservative, Adjust Based on Evidence

**Initial settings:**
- F-K 12-14 (standard MBA)
- 4-6 questions per piece
- Analyze level (requires thinking, not just recall)

**After 2-3 weeks:**
- Check student performance on questions
- Too easy? Increase Bloom's level or question count
- Too hard? Reduce F-K level or simplify Bloom's level

---

### Different Settings for Different Points in Semester

**Early semester (Weeks 1-4):**
- Lower F-K (11-12)
- More Remember/Understand questions
- Shorter content

**Mid-semester (Weeks 5-10):**
- Standard F-K (12-14)
- Analyze questions
- Standard length

**Late semester (Weeks 11-15):**
- Higher F-K (13-15)
- Evaluate/Create questions
- Longer, more complex content

Update settings every few weeks as students develop sophistication.

---

### Content Type Differences

**Tool Guides = Procedural**
- How to use the framework
- Analyze level (can you apply it?)
- Fewer questions (focused assessment)

**Chapters = Conceptual**
- Why the concept matters, theory
- Mixed levels (build up complexity)
- More questions (comprehensive coverage)

**Cases = Application**
- Real-world judgment calls
- Evaluate level (what would you do?)
- Most questions (deepest assessment)

---

## Troubleshooting

### "I changed settings but new content still uses old defaults"

**Fix:** Make sure you're running the update prompt and Claude Code confirms the change.

After updating, verify:
```
Show me current chapter defaults
```

If they're wrong, try updating again.

---

### "I want different settings for one chapter but not all chapters"

**Fix:** Use prompt overrides instead of changing defaults:
```
Write Chapter 5: F-K 11-12, 8 questions, Mixed Bloom's levels
```

This overrides just for that one piece. Defaults stay the same for other chapters.

---

### "How do I know which content type Claude is using?"

Claude Code determines content type from your prompt:
- "tool guide" → Uses tool guide defaults
- "chapter" → Uses chapter defaults
- "case study" → Uses case defaults

If ambiguous, Claude will ask or default to the most logical type.

---

## What Gets Updated

When you run the settings manager, Claude Code updates this file:
- `skills/content/CONTENT_SYSTEM_README.md`

Specifically, it updates the parameters section for each content type.

You don't need to manually edit that file — the settings manager does it for you.

---

## Examples

### Example 1: Make Chapters Longer with More Questions

**Prompt:**
```
Update chapter defaults: word count = 2500, MC questions = 7, Bloom's = Mixed
```

**Result:**
All future chapters will be 2500 words with 7 mixed-level questions automatically.

---

### Example 2: Make Tool Guides More Accessible

**Prompt:**
```
Update tool guide defaults: F-K = 10-12, Bloom's = Apply
```

**Result:**
All future tool guides will be written at grade level 10-12 with Apply-level questions.

---

### Example 3: Configure Everything for Executive Ed Course

**Prompt:**
```
I want to update settings for an executive education course (not MBA).

Tool guides: 600 words, F-K 11-12, 3 Apply questions
Chapters: 1500 words, F-K 12-13, 4 Analyze questions
Cases: 1000 words, F-K 12-13, 5 Evaluate questions
All: Minimal biblical integration
```

**Result:**
All defaults adjusted for exec ed audience.

---

## Quick Reference Card

| Action | Prompt |
|--------|--------|
| See all settings | `Show me current content settings` |
| Update one type | `Update [type] defaults: [changes]` |
| Update all types | Use Option 2 full prompt above |
| Reset to defaults | `Reset content settings to MBA defaults` |
| Test new settings | `Write a [type] on [topic]` |

---

**Use this manager at the start of each semester or whenever your needs change.**
