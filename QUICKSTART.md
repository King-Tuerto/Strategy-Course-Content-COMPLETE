# QUICKSTART GUIDE — Strategy Course Content Project

## What This Project Does

Generates written course content (tool guides, chapters, cases) in a consistent voice:
- Senior Christian executive speaking to new-hire MBAs
- Flesch-Kincaid grade level 12-14 (adjustable)
- Biblical integration where natural
- Bloom's Taxonomy-leveled questions

---

## ONE-TIME SETUP (Do This Once)

### Step 1: Make Sure You're in the Right Project
1. Open VS Code
2. **File → Open Folder**
3. Navigate to: `C:\Users\Paul\Desktop\Spring2026\660\strategy-course-content`
4. Click **Select Folder**

### Step 2: Verify Explorer Shows the Right Files
Look at Explorer panel (left sidebar). You should see:
```
STRATEGY-COURSE-CONTENT
├── UPDATE_SETTINGS.md      ← Configure global defaults
├── QUICKSTART.md           ← You're reading this
├── prompts/                ← Custom parameter templates
│   ├── TOOL_GUIDE_PROMPT.md
│   ├── CHAPTER_PROMPT.md
│   └── QUICK_OVERRIDE_GUIDE.md
├── uploads/                ← Put syllabi, vocab lists here
├── .claude/
├── skills/content/
└── output/
```

### Step 3: Open Claude Code
- Click the **Claude icon** on left sidebar (or View → Claude)
- At the bottom of Claude Code panel, verify it shows: `C:\...\strategy-course-content`

✅ **Setup complete!**

---

## EVERY SEMESTER — Configure Your Settings

### Step 1: Open SETTINGS_MANAGER.md
- In Explorer, click `SETTINGS_MANAGER.md`
- File opens in the editor

### Step 2: Decide What to Configure
- **One content type** (tool guides OR chapters OR cases) — Use Option 1
- **All content types** — Use Option 2

### Step 3: Copy the Prompt
- Scroll to the option you chose
- Copy the prompt in the code box
- **Ctrl+C**

### Step 4: Paste into Claude Code
- Click in the Claude Code chat input
- **Ctrl+V** to paste
- Press **Enter**

### Step 5: Answer the Questions
Claude Code shows current settings and asks what to change:
> "Current chapter settings: 5 questions at Analyze level. What would you like to change?"

Answer, and Claude updates the files automatically.

✅ **Settings configured for the semester!**

**Note:** Each content type (tool guides, chapters, cases) has separate defaults. Configure them independently or all at once.

---

## DAILY USE — Generate Content

### Using Global Defaults (Easy — 80% of the Time)

**Prompt:**
```
Write a complete tool guide for the IFE Matrix using all content skills.
```

Claude uses your semester settings automatically.

---

### Using Custom Parameters (When You Need Control)

**Option 1: Quick One-Liner**

Just specify what you want to override:
```
Write an IFE guide: 500 words, 3 Apply questions, F-K 10-12
```

See `prompts/QUICK_OVERRIDE_GUIDE.md` for full syntax.

---

**Option 2: Use a Template**

1. Open `prompts/TOOL_GUIDE_PROMPT.md` (or CHAPTER_PROMPT.md)
2. Fill in the blanks
3. Copy the completed prompt at the bottom
4. Paste into Claude Code

Gives you full control over every parameter.

---

### Example Workflows

**Example 1: Create a Tool Guide (Default Settings)**

**Prompt:**
```
Write a complete tool guide for the IFE Matrix using all content skills.
```

**What happens:**
- Uses your global settings
- Writes in your voice
- Saves to `output/tool-guides/`

---

**Example 2: Create a Short Tool Guide (Custom)**

**Prompt:**
```
Write an IFE guide: 500 words, 3 Apply questions, use Apple as example
```

**What happens:**
- Overrides word count and question level
- Still uses your voice and F-K setting
- Saves to `output/tool-guides/`

---

### Example 2: Write a Chapter

**Prompt:**
```
Write Chapter 3 on Internal Analysis. Include the IFE tool 
explanation. Use all content skills.
```

**What happens:**
- Follows chapter structure template
- F-K level matches your settings
- Includes biblical integration where natural
- Saves to `output/chapters/Chapter_03.md`

---

### Example 3: Create a Case Study

**Prompt:**
```
Create a case study on Starbucks' 2008 turnaround. 
Strategic challenge: declining same-store sales. 
Include ethical dimension. Use content skills.
```

**What happens:**
- Follows case template
- Includes discussion questions at your Bloom's level
- Saves to `output/cases/Starbucks_2008.md`

---

## CHECKING YOUR WORK

### Verify Flesch-Kincaid Level
1. Open the generated content in **Microsoft Word**
2. File → Options → Proofing
3. Check "Show readability statistics"
4. Press **F7** (spell check)
5. Readability stats appear at the end

Should match your target (e.g., 12-14).

### Verify Voice
Read a paragraph out loud. Does it sound like:
- A senior executive talking to new hires? ✅
- A textbook? ❌

If it sounds like a textbook, tell Claude Code:
```
Rewrite this in the voice from VOICE.md. Too formal right now.
```

---

## COMMON WORKFLOWS

### Workflow 1: Build All Tool Guides
```
For each of these tools: IFE, EFE, CPM, BCG, IE, GRAND, 
PERCEPTUAL, SWOT, QSPM, SPACE

Write a complete tool guide using all content skills.
```

Claude will generate all 10 guides.

---

### Workflow 2: Create Weekly Reading + Questions
```
Write a 3-page chapter on the SPACE Matrix. Include:
- Tool explanation
- Real company example
- 4 MC questions at Analyze level
- 1 critical thinking question

Use all content skills.
```

---

### Workflow 3: Adjust Difficulty Mid-Semester
If content is too hard for students:

1. Open `UPDATE_SETTINGS.md`
2. Copy the prompt
3. Paste into Claude Code
4. Change F-K level from 12-14 to 10-12
5. Regenerate the problematic content

---

## TROUBLESHOOTING

### "Claude Code is reading from the wrong project"
- **Fix:** Look at bottom of Claude Code panel. Click the folder path. Select `strategy-course-content`.

### "Where are my generated files?"
- **Location:** `output/` folder in Explorer
- **Note:** Claude Code creates subfolders automatically (tool-guides/, chapters/, cases/)

### "Content doesn't sound like my voice"
- **Check:** Did you configure settings using UPDATE_SETTINGS.md?
- **Fix:** Tell Claude: "Read VOICE.md again and rewrite this"

### "Flesch-Kincaid score is off"
- **Target too high:** Break long sentences, simplify words
- **Target too low:** Vary sentence length, use appropriate business terms
- **Ask Claude:** "Rewrite this at F-K grade level 12"

---

## REMEMBER

- **Tools project** (frozen) = `strategy-tools-skill` folder
- **Content project** (active) = `strategy-course-content` folder
- Keep them separate!
- Always have the right folder open in VS Code

---

## YOU'RE READY!

Next steps:
1. Run UPDATE_SETTINGS.md to configure parameters
2. Try generating one tool guide
3. Check the output in `output/tool-guides/`
4. Verify F-K score in Word
5. Adjust and iterate

**That's it. You're all set!**
