---
name: weekly-journal
description: Generate weekly journal entries from user's life content or daily journal files. Use when user wants to create a weekly review, write a weekly summary, or consolidate the week's work and life. The skill treats weekly journals as mid-level filters: screen daily details, identify repeated problems, valuable events, and emotional patterns, then turn "what happened" into "what this week means." Knows how to distill daily journal entries (流水账, 情绪, 感恩, 成就, 复盘, 思绪) into the weekly format (内容, 进展, 改进, 计划, 回顾, 健康, 社交, 成长, 娱乐, 思考).
---

# Weekly Journal Generator

Generate structured weekly journal entries from user's life content or daily journal files, following the user's personal conventions. The weekly journal is a sieve and first-pass synthesis layer: it filters detail, names patterns, and develops one meaningful thought from the week.

## Quick Start

When the user provides weekly content (or asks to generate from daily journals), follow this workflow:

1. **Determine the week** — identify which ISO week to write for
2. **Gather content** — from user input, or by reading daily journal files for that week
3. **Learn writing style** — check for `.weekly-style.md` profile
4. **Generate the weekly journal** following the template structure
5. **Save the file** as `YYYY-Www.md` in the current working directory

## File Naming Convention

Weekly journals use ISO week format: `YYYY-Www.md`

- Examples: `2024-W15.md`, `2024-W21.md`, `2026-W17.md`
- The week number is zero-padded to 2 digits
- Use the ISO 8601 week number (Monday = start of week)
- If user says "this week" and today is 2026-04-20, that is W17 → `2026-W17.md`

## Template Structure

```markdown
---
created: [Current datetime]
modified: [Current datetime]
tags:
  - 工作      # omit if no work content this week
  - 生活
  - 周记
---
## 本周日记汇总

### [YYYY-MM-DD](YYYY-MM-DD.md)
... (one line per day of the week, Mon–Sun)

## 工作

### 内容：
### 进展：
### 改进：
### 下周计划：

## 生活

### 回顾：
### 健康：
### 社交：
### 成长：
### 娱乐：
### 思考：
```

Full template reference: [references/template.md](references/template.md)
Style profile template reference: [references/.weekly-style.md](references/.weekly-style.md)

**Hard rule for style profile source:**
- Treat `./.weekly-style.md` in the **current working directory** as the only real style profile.
- `skills/weekly-journal/references/.weekly-style.md` is a **template format reference only**.
- Never use `references/.weekly-style.md` as personal style data.

---

## Step 0: Determine the Target Week

1. If the user specifies a week (e.g., "W15", "第15周", "上周"), resolve it to `YYYY-Www`.
2. If the user says "this week" or gives no date, use the current date to compute the ISO week number.
3. Compute the Monday–Sunday date range for that week (needed for the daily summary section and for finding daily journals).

**ISO week calculation reference:**
- Week starts on Monday
- Use `date -d "YYYY-MM-DD" +%V` logic or compute manually
- Example: 2026-04-20 (Monday) → W17 → range 2026-04-20 to 2026-04-26

---

## Step 1: Locate Daily Journal Files

1. **Compute the date range** for the target week (Mon–Sun).
2. **Search in the current working directory first**: use Glob for `YYYY-MM-DD.md` matching each of the 7 dates.
3. **If no daily files found in cwd**, ask the user:
   > "没有在当前目录找到这周的日记文件，请问日记存放在哪个目录？"
   Then search in the path the user provides.
4. **Read each daily file found** — it's fine if some days are missing (e.g., weekends with no entry).
5. **If zero daily files found anywhere**: ask the user to describe the week before proceeding.

### Synthesis mindset when reading daily journals

Daily journals are raw and granular. Your job is to **distill, not transcribe**. Think of it as:
- **工作部分**: What actually moved forward this week? What went wrong? What's next?
- **生活部分**: What moments were worth remembering? What was the emotional texture of the week?
- **成长部分**: What did the mind absorb this week — ideas, skills, perspectives?
- **思考部分**: Which single thought from the week deserves to be developed further?

The weekly journal should read like a thoughtful retrospective written by the person themselves — not a summary report of their diary.

Weekly-level principle:
- Start from the week, not from a universal life prompt
- Keep repeated signals, meaningful events, and obvious emotional patterns
- Drop daily noise unless it reveals a weekly pattern
- `思考` should grow from this week's materials, especially repeated `思绪`
- Broad life-direction questions are valid as fallback prompts when this week's material does not surface an obvious thought

---

## Step 2: Learn Writing Style

**This step can be skipped to save tokens if user prefers.**

#### Option A: Use Existing Style Profile (Recommended)

1. Check for `.weekly-style.md` in the current working directory.
2. If found, read it (~200–400 tokens) and apply its style characteristics.
3. **Scope guard**: Only accept `./.weekly-style.md` (cwd). Ignore any `.weekly-style.md` under skill `references/` paths.

#### Option B: Create New Style Profile (First Time Only)

If `.weekly-style.md` doesn't exist:

1. Use Glob to find existing weekly journals matching `20[0-9][0-9]-W[0-9][0-9].md` in the current directory.
2. Read the 3–5 most recent ones to gather style data.
3. Analyze:
   - Tone (casual vs formal, humorous vs serious)
   - Sentence structure and length
   - Vocabulary and expressions
   - Level of detail per section
   - Use of Obsidian links, callouts, tags
   - Paragraph vs list preference per section
4. Generate `.weekly-style.md` using the format in `references/.weekly-style.md`.
5. Apply the learned style to the current journal.

**Token efficiency:**
- First time (create profile): ~6000–9000 tokens
- Subsequent uses: ~2000–2500 tokens (profile ~300 tokens + generation)
- **Average savings: 60–70%**

**If no weekly journals or profile exist**: Use neutral, natural style based on user's input tone.

---

## Step 3: Build the Daily Summary Section

List each day of the week as a wikilink:

```markdown
## 本周日记汇总

### [2026-04-20](2026-04-20.md)
### [2026-04-21](2026-04-21.md)
### [2026-04-22](2026-04-22.md)
### [2026-04-23](2026-04-23.md)
### [2026-04-24](2026-04-24.md)
### [2026-04-25](2026-04-25.md)
### [2026-04-26](2026-04-26.md)
```

Include all 7 days (Mon–Sun) regardless of whether daily journal files exist.

---

## Step 4: Fill Content Sections

This is the core transformation step. Daily journals are detailed and granular; weekly journals are distilled and synthesized. The key principle: **keep what matters, drop what doesn't**.

### Pre-writing scan: find weekly patterns

Before writing any section, scan across all daily files for:
- **Mood arc**: Did energy/mood rise, fall, or stay flat? Was there a turning point?
- **Sleep/fatigue signals**: Recurring mentions of tiredness, poor sleep, or high energy?
- **Social density**: Socially rich week or isolated one?
- **Work rhythm**: Focused and productive, or fragmented and reactive?
- **Recurring themes**: Any topic, person, or concern that appeared on 3+ days?

Use these patterns as invisible scaffolding — they inform tone and emphasis across all sections, not as a separate output. A week where mood crashed on Wednesday should feel different from a week that built momentum.

### What to DROP from daily journals

These daily journal sections do NOT appear in the weekly journal:
- **情绪 tags** (`#开心 #疲惫` etc.) — emotion tags are daily-level granularity, not weekly
- **感恩 (Gratitude)** — the daily gratitude lists are not carried over
- **成就 (Achievements)** — the daily achievement lists are not carried over
- **流水账 details** — specific times, what was eaten, minor errands, trivial routines
- **明日工作安排** from each day — only the last day's plan informs 计划
- **Memos** — ephemeral notes not worth preserving at weekly level

### Work Section (工作)

**内容 (Overview)**
- Source: synthesize all days' "成果和进展" + "复盘"
- Write ONE paragraph covering the week's main work themes and directions
- Mention key projects, tasks, and collaborators
- This is a narrative overview, not a list — capture the arc of the week
- Open with a one-sentence "main thread" that names the week's core work focus: "本周工作的主线是 X。"
- Example: "本周工作主要集中在 X 项目的推进上，完成了 Y 和 Z，并与[人名]就 W 进行了深入讨论。"

**进展 (Progress)**
- Source: "成果和进展" from each day — extract only the substantive items
- DROP: "摸鱼", routine platform updates, trivial logistics
- KEEP: completed deliverables, key decisions, meaningful conversations, milestones
- Bullet list, use Obsidian links for projects/people/places

**改进 (Improvements)**
- Source: "复盘" sections across the week — extract problems and lessons
- DROP: generic reflections ("要继续努力"), positive self-praise
- KEEP: specific mistakes, process failures, actionable lessons
- Bullet list, focus on what can be done differently
- If no genuine improvement items exist, write `- 本周无明显改进事项` — do not invent weak entries to fill the section

**下周计划 (Next Week Plan)**
- Source: the last working day's "明日工作安排" + any forward-looking items mentioned during the week
- Bullet list of next week's priorities, scheduled events, and goals
- Mark the single most important item with `**[重点]**` prefix

### Life Section (生活)

**回顾 (Review)**
- Source: "流水账" from all days — select only the meaningful moments
- DROP: waking times, meal details, minor errands, routine commutes
- KEEP: notable outings, meaningful conversations, pleasant surprises, emotional highlights
- Write as paragraph-style prose, but each paragraph/sentence prefixed with `- `
- Include the emotional tone naturally (without using hashtag tags)

**健康 (Health)**
- Source: exercise mentions, diet comments, sleep/fatigue mentions across all days
- Write as paragraph-style prose prefixed with `- `, covering exercise, diet, sleep, and any body signals worth noting
- Note any patterns, concerns, or improvements
- Include body signals worth noting (headaches, fatigue patterns, tension)
- If last week's health was notably different, briefly note the comparison

**社交 (Social)**
- Source: all interpersonal interactions from "流水账" across the week
- DROP: brief work coordination (unless it had personal significance)
- KEEP: meals with friends, meaningful conversations, new connections, group activities
- Write as paragraph-style prose prefixed with `- `, use Obsidian links for people: `[[真名|昵称]]`
- Capture the quality of connections, not just the events
- Note frequency anomalies: someone you usually see but didn't, or an unexpected reconnection

**成长 (Growth)**
- Source: podcasts, books, articles, tools learned, realizations from "思绪" and "流水账"
- KEEP: specific insights, new skills, knowledge gained, perspective shifts
- DROP: generic "learned a lot" statements
- Write as paragraph-style prose prefixed with `- `, be specific about what was learned and why it matters
- If multiple learning inputs exist (podcasts, books, articles), look for connections — a shared theme or tension is more interesting than a list

**娱乐 (Entertainment)**
- Source: shows watched, games played, live streams, music, outings for fun
- Write as paragraph-style prose prefixed with `- `
- Be honest — `- 主要是躺着休息` is a valid entry

**思考 (Reflection)**
- Source: the most interesting/deep item from "思绪" across the week — pick ONE topic
- **If the user's daily journals have a strong "思绪"**: develop it into a callout block:
  - Use `> [!summary]+` for concise reflections — drawn from this week's diary, a few paragraphs of personal insight
  - Use `> [!help]+` for deeper explorations — when a theme has been building across multiple weeks or the topic is rich enough to warrant quoting external material, structuring a multi-part argument, or going beyond personal feeling into broader questions. In continuous conversations the AI should have context from prior weeks to draw on
  - Generate the callout title from the reflection content after deciding what to write; it should name the actual topic, not reuse a fixed prompt
  - Expand the thought: add context, reasoning, connections to other ideas
  - This should feel like genuine reflection, not a recap
- **If no strong "思绪" exists this week**: use one of these angles (or any other that fits):
    - **Trigger mode**: "这件事让我想到……" — follow the thread of one specific moment
    - **Comparison mode**: "和上周/上个月相比……" — what has shifted?
    - **Question mode**: pose one genuine open question the week raised, without forcing an answer
    - **Emergent insight**: "有没有什么事情我没有写进日记，但现在回头看才意识到的？"
    - Or freely pick any other angle that feels right for the week
  - Mark this as a "思考方向提示" so the user knows it's a prompt, not a completed reflection

---

## Step 5: Apply Writing Style and Cross-References

1. **Apply learned style**: Match tone, vocabulary, sentence structure, and detail level from the style profile.
2. **Add cross-references** when naturally relevant:
   - Reference previous weekly journals: `[[2026-W16]]`
   - Reference specific daily journals: `[[2026-04-18]]`
   - Reference ongoing projects or notes: `[[项目名称]]`
   - Only add when it genuinely adds context — don't force it.
3. **Use Obsidian links** for people (`[[真名|昵称]]`), places, and recurring topics, consistent with the user's existing style.

---

## Step 6: Save or Fill the Weekly Journal File

1. **Check if the file already exists**: use Glob or Read to check for `./YYYY-Www.md` in the current directory.
2. **If the file exists and is blank or has only the template structure**:
   - Read the existing file
   - Fill in the content sections while preserving the frontmatter and structure
   - Use Edit tool to replace the empty sections with generated content
3. **If the file doesn't exist**:
   - Use Write tool to create `./YYYY-Www.md` with complete content
4. **File path**: always save in the current working directory as `YYYY-Www.md`

Example: `./2026-W17.md`

**Important**: If the existing file already has substantial content (not just template headers), ask the user before overwriting:
> "检测到 2026-W17.md 已经有内容了，要覆盖吗？"

---

## Writing Guidelines

- Keep the original template structure intact — all section headers must be present
- Write in first person for personal sections
- Be specific and concrete, not generic
- If a section has no content, keep the header and write a brief honest note (e.g., "本周无特别运动记录")
- **Sparse week**: if daily journals are thin (many days missing, or mostly "tired / nothing special"), let the output be proportionally shorter — a genuine short week is better than a padded one
- Maintain Chinese for all section headers and structure
- **Match the user's personal writing style** from the style profile
- **Work section**: prefer bullet lists for 进展/改进/计划; paragraph for 内容
- **Life section**: prefer paragraph narrative for 回顾/社交/成长; brief paragraph or bullets for 健康/娱乐; callout block for 思考
- The 思考 section should feel like genuine reflection, not a summary — encourage depth over breadth

### Anti-AI-smell rules

1. **No opening meta-summaries**: Don't start sections with "本周……总体来说……" — start with the actual content
2. **No closing affirmations**: Remove "期待下周继续努力" / "相信会越来越好" type endings
3. **No symmetry padding**: Uneven sections are fine; don't add bullets just to balance
4. **No vague positives**: Replace "收获颇丰" / "感触很深" / "受益匪浅" with the specific thing gained or felt
5. **No transition filler**: Remove "总的来说，这周……" sentences that exist only to connect paragraphs
6. **Emotion must be earned**: Only write emotional language (感动、感慨) when the daily journals contain the event that earned it

---

## Example Usage

**User input:**
"帮我写本周（W17）的周记。这周主要在做新功能开发，修了几个 bug，周五上线了。生活上和朋友吃了顿饭，看了部电影，运动坚持了三天。"

**Generated file**: `2026-W17.md` with all sections filled based on the input and any available daily journals.

---

## Important Notes

- Always save files with UTF-8 encoding
- Use ISO week format `YYYY-Www` — never `YYYY-W#` (single digit)
- If user doesn't specify a week, default to the current week
- When reading daily journals to synthesize, **summarize and find patterns** — don't just copy-paste
- **Check for `.weekly-style.md` first** before reading full weekly journal files (saves tokens)
- **Create style profile on first use** if multiple weekly journals exist but no profile found
- **Profile path rule**: profile must be `./.weekly-style.md` in cwd; never treat skill reference files as user profile
- The 本周日记汇总 section always lists all 7 days, even if no daily files exist for some days

---

## Usage Pattern

The user will explicitly request weekly journal generation when ready:
- "帮我写 2026-W01 的周记"
- "生成本周的周记"
- "根据这周的日记写周记"

When invoked:
1. Determine the target week (from user input or current date)
2. Calculate the Monday–Sunday date range for that week
3. Use Glob to find daily journal files matching `YYYY-MM-DD.md` in the current directory
4. Filter to only the 7 days of the target week
5. Read each daily journal file found
6. Check for `.weekly-style.md` profile (or create one if multiple weekly journals exist)
7. Synthesize the content following the distillation rules in Step 4
8. Generate and save `YYYY-Www.md`

The user maintains full control over when to generate and can review/edit the output afterward.
