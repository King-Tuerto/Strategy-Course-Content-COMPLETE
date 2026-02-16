# Flesch-Kincaid Readability Targeting

## Current Target Settings

```yaml
target_fk_grade_level: 16-18    # Adjust this number to change readability
target_fk_reading_ease: 30-40   # Adjust if needed (0-100 scale)
acceptable_variance: ±1 grade   # How much deviation is OK
```

---

## What These Numbers Mean

**Grade Level 12-14:**
- Appropriate for MBA students
- Assumes college-level vocabulary
- Allows complex sentences when needed for precision
- Balances accessibility with sophistication

**Reading Ease 50-60:**
- "Fairly Difficult" on Flesch scale
- Appropriate for educated adult audience
- Not conversational (that's 60-70)
- Not academic jargon (that's <30)

---

## How to Adjust

### To Make Content More Accessible (Lower Grade Level)

Change settings to:
```yaml
target_fk_grade_level: 10-12
target_fk_reading_ease: 60-70
```

This produces:
- Shorter average sentences (12-16 words vs. 14-18)
- Simpler vocabulary where possible
- More frequent paragraph breaks
- Still professional, just clearer

**When to use:** Student handouts, quick reference guides, international students

---

### To Make Content More Sophisticated (Higher Grade Level)

Change settings to:
```yaml
target_fk_grade_level: 14-16
target_fk_reading_ease: 40-50
```

This produces:
- Longer sentences when precision requires it
- Technical vocabulary without over-explanation
- Denser paragraphs
- Academic journal tone

**When to use:** Peer-reviewed publications, academic conferences

---

## Checking Your Content

After Claude generates content, verify F-K scores using:

**Option 1 — Microsoft Word:**
1. Open the document in Word
2. File → Options → Proofing
3. Check "Show readability statistics"
4. Run spell check (F7)
5. Readability stats appear at the end

**Option 2 — Online Tool:**
- https://readable.com/text/ (paste text, get instant score)

**Option 3 — Hemingway Editor:**
- https://hemingwayapp.com/ (also highlights complex sentences)

---

## What to Do If Scores Are Off

### If F-K Grade Level is Too HIGH (e.g., 16 when target is 12-14):

**Causes:**
- Sentences over 25 words
- Excessive jargon or multi-syllable words
- Passive voice
- Nested clauses

**Fixes:**
- Break long sentences at natural pauses
- Replace jargon with simpler synonyms where meaning allows
- Convert passive to active voice
- Simplify clause structures

**Example Revision:**

❌ TOO HIGH (F-K 16):
> "The utilization of the Internal Factor Evaluation Matrix facilitates the comprehensive assessment of organizational capabilities through the systematic application of weighted scoring methodologies, enabling strategic decision-makers to ascertain relative strengths."

✅ TARGET (F-K 12-14):
> "The IFE Matrix helps you assess your organization's capabilities systematically. You assign each factor a weight and rating, then calculate which strengths matter most. This gives decision-makers a clear picture of relative advantages."

---

### If F-K Grade Level is Too LOW (e.g., 8 when target is 12-14):

**Causes:**
- Every sentence is short (under 10 words)
- Oversimplified vocabulary
- Choppy rhythm
- Sounds like talking to children

**Fixes:**
- Vary sentence length (use 12-18 word sentences mixed with short punches)
- Use appropriate business terminology (don't avoid "strategy," "competitive advantage," etc.)
- Combine related short sentences

**Example Revision:**

❌ TOO LOW (F-K 8):
> "Use the IFE tool. It helps you. You rate factors. You add weights. You get a score. The score shows strengths."

✅ TARGET (F-K 12-14):
> "The IFE Matrix produces a weighted score showing your organization's overall internal position. You'll rate each strength and weakness, assign importance weights, and calculate which capabilities provide the greatest advantage."

---

## Sentence Length Guidelines by F-K Target

| Target F-K | Avg Sentence Length | Max Sentence | Notes |
|------------|---------------------|--------------|-------|
| 10-12 | 12-16 words | 22 words | Clear, accessible |
| 12-14 | 14-18 words | 25 words | MBA default |
| 14-16 | 16-20 words | 30 words | Academic |

**Remember:** These are AVERAGES. Mix short (8-10 word) punches with longer (20-25 word) explanations.

---

## Vocabulary Complexity by F-K Target

### F-K 10-12 (Accessible)
- Use: company, find, use, help, show
- Avoid: entity, ascertain, utilize, facilitate, demonstrate

### F-K 12-14 (MBA Default)
- Use: organization, competitive advantage, strategic positioning
- Avoid: synergistic optimization, paradigmatic framework, holistic ecosystem

### F-K 14-16 (Academic)
- Use: operationalize, instantiate, exogenous factors
- Acceptable but use sparingly

---

## Biblical Language & F-K Scores

Scripture quotations often have LOW F-K scores (King James = 6th grade, NIV = 7th grade) because:
- Short sentences
- Simple Anglo-Saxon words
- Concrete imagery

**Don't let this drag your score down.** The surrounding analysis should balance it:

✅ **BALANCED**:
> "Proverbs 28:13 teaches: 'Whoever conceals their sins does not prosper, but the one who confesses and renounces them finds mercy.' [F-K ~6]
>
> In organizational terms, this principle directly applies to internal factor evaluation. [F-K ~14] Leaders who rationalize weaknesses as 'areas for development' or hide capability gaps from boards create strategic blind spots. [F-K ~16] Honest assessment—even when uncomfortable—enables genuine improvement." [F-K ~12]
>
> **Paragraph F-K Average: ~12** ✓

---

## Content-Type Specific Targets

| Content Type | Recommended F-K | Rationale |
|--------------|-----------------|-----------|
| Tool instructions (in HTML) | 10-12 | Quick reference, scan-friendly |
| Tool guide (full explication) | 12-14 | Default MBA |
| Chapter prose | 12-14 | Default MBA |
| Case studies | 11-13 | Narrative flow, mixed complexity |
| Knowledge check questions | 11-13 | Clear, unambiguous |
| Critical thinking prompts | 13-15 | Nuance requires precision |
| Rubrics | 10-12 | Clarity for grading |

---

## Prompt for Claude Code

When generating content, include F-K target in your prompt:

```
Write a tool guide for the IFE Matrix following VOICE.md and 
STRUCTURE.md. Target Flesch-Kincaid grade level 12-14.
```

Claude Code will aim for that range and you can verify with the checking tools above.
