# Content Settings Configurator

**⚠️ NOTE: A newer, better version is available in SETTINGS_MANAGER.md**

The new Settings Manager organizes parameters by content type (tool guides, chapters, cases) making it easier to set different defaults for each. This file still works, but SETTINGS_MANAGER.md is recommended.

---

## Purpose
This file contains the prompt you paste into Claude Code to update all content parameters interactively.

---

## How to Use This File

1. Open Claude Code (in this project)
2. Copy the prompt below (everything in the box)
3. Paste it into Claude Code
4. Answer the questions Claude asks
5. Claude updates all your `.md` files automatically

---

## THE PROMPT (Copy everything below this line)

```
I need to update my content generation parameters. Please ask me for each setting one at a time, then update the appropriate .md files.

Ask me these questions:

1. What Flesch-Kincaid grade level should content target? (Current default: 12-14)
   Options: 10-12 (more accessible), 12-14 (MBA standard), 14-16 (academic)

2. How many multiple choice questions per tool guide? (Current default: 4)
   Enter a number: 3, 4, 5, etc.

3. What Bloom's Taxonomy level for MC questions? (Current default: analyze)
   Options: remember, understand, apply, analyze, evaluate, create

4. How many critical thinking questions per tool guide? (Current default: 1)
   Enter a number: 1, 2, etc.

5. Should biblical integration be: natural (where it fits), frequent (most sections), or minimal (rare)?
   (Current default: natural)

After I answer all questions, update these files:
- skills/content/FLESCH_KINCAID.md (update target_fk_grade_level)
- skills/content/CONTENT_SYSTEM_README.md (update mc_question_count, blooms_level, critical_thinking_count)
- skills/content/VOICE.md (add a note about biblical integration preference if needed)

Then confirm what you changed.
```

---

## After You Run This

Claude Code will ask you each question, wait for your answer, then update all the files. You'll see something like:

> "I've updated your settings:
> - F-K level: 12-14 → 10-12 (in FLESCH_KINCAID.md)
> - MC questions: 4 → 5 (in CONTENT_SYSTEM_README.md)
> - Bloom's level: analyze → apply (in CONTENT_SYSTEM_README.md)"

---

## When to Use This

- Start of each semester (set preferences for that cohort)
- When you want to adjust difficulty
- When you're writing for a different audience (undergrad vs MBA vs exec ed)

Just paste the prompt and answer the questions. That's it.
