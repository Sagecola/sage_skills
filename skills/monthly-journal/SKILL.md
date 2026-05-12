---
name: monthly-journal
description: "Generate monthly journal entries and monthly reviews directly from daily journal files. Use when the user asks to 写月记, 生成月记, 月度复盘, 本月总结, 这个月回顾, 根据日记整理月记, or consolidate a month into an Obsidian monthly note. Distill daily journals into a month-level note with 本月周记, 本月主线, 关键词, work review (保持 / 问题 / 尝试 / 里程碑), life review (生命之轮 / 高光 / 所幸 / 觉察 / 迁移 / 下月重点 / 本月回看). Use this instead of summarizing weekly journals when the goal is to preserve detail while identifying month-level patterns, texture, and action guidance."
---

# Monthly Journal Generator

Generate structured monthly journal entries from daily journal files, following the user's personal conventions.

## Quick Start

When the user requests a monthly journal, follow this workflow:

1. **Determine the target month** — identify which month to write for
2. **Gather content** — read daily journal files for that month directly
3. **Learn writing style** — check for `.monthly-style.md` profile
4. **Generate the monthly journal** following the template structure
5. **Save the file** as `YYYY-MM.md` in the current working directory

## File Naming Convention

Monthly journals use year-month format: `YYYY-MM.md`

- Examples: `2024-02.md`, `2024-12.md`, `2026-05.md`
- Use zero-padded month number
- If user says "this month" and today is 2026-05-12, that is `2026-05`

## Template Structure

```markdown
---
created: [Current datetime]
modified: [Current datetime]
tags:
  - 工作
  - 生活
  - 月记
---
## 本月索引

### 本月周记：
### [[YYYY-Www]]
... (all weeks of the month)

### 本月主线：
### 关键词：
- 关键词A / 关键词B / 关键词C

## 工作

### 保持：
### 问题：
### 尝试：
### 里程碑：

## 生活

### 生命之轮：
| 维度 | 分数 | 原因 |
|------|------|------|
| 工作 | /10 |  |
| 健康 | /10 |  |
| 财务 | /10 |  |
| 娱乐 | /10 |  |
| 成长 | /10 |  |
| 关系 | /10 |  |

### 高光：
### 所幸：
### 觉察：
> [!note]+
> - 
### 迁移：
### 下月重点：
### 本月回看：
```

Full template reference: [references/template.md](references/template.md)
Style profile template reference: [references/.monthly-style.md](references/.monthly-style.md)

**Hard rule for style profile source:**
- Treat `./.monthly-style.md` in the **current working directory** as the only real style profile.
- `skills/monthly-journal/references/.monthly-style.md` is a **template format reference only**.
- Never use `references/.monthly-style.md` as personal style data.

## Step 0: Determine the Target Month

1. If the user specifies a month (e.g., "3月", "2024-12", "十二月"), resolve it to `YYYY-MM`.
2. If the user says "this month" or gives no date, use the current date.
3. Compute the first and last day of that month.
4. Compute which ISO weeks overlap with the target month for the index section.

**ISO week calculation reference:**
- A month usually overlaps 4–5 ISO weeks
- Example: `2024-12` overlaps `2024-W48` to `2025-W01`

## Step 1: Locate Daily Journal Files

1. **Compute the date range** for the target month.
2. **Search in the current working directory first** for `YYYY-MM-DD.md` files matching the month.
3. **If no daily files found in cwd**, ask the user:
   > "没有在当前目录找到这个月的日记文件，请问日记存放在哪个目录？"
4. **Read each daily file found** — missing days are acceptable.
5. **If zero daily files found anywhere**: ask the user to describe the month before proceeding.

### Synthesis mindset when reading daily journals

Daily journals are raw and granular. Your job is to **elevate directly to the monthly perspective**, not to produce a bigger weekly note.

Think of the monthly journal as:
- **地图**: What really defined this month?
- **趋势识别**: What patterns repeated across multiple weeks?
- **行动指南**: What should continue, stop, or start next month?
- **生活质感保留**: What details made this month feel like itself?

The monthly journal should answer:
- What was the real main thread of the month?
- What patterns kept repeating?
- What is worth carrying into next month?

### What to DROP from daily journals

These daily journal details should usually not be carried over directly:
- Daily emotion tags (`#开心 #疲惫`)
- Memos
- Most timestamps and routine logistics
- Minor errands and repetitive meal details
- Repetitive "tomorrow plan" items, except when they become a month-end focus

### What to KEEP that weekly summaries often lose

Pay special attention to:
- Specific people, places, tools, and recurring contexts
- Emotional arc across the month
- Repeated friction points
- Specific moments that changed the month
- Small but revealing life details that give the month texture

## Step 2: Learn Writing Style

**This step can be skipped to save tokens if user prefers.**

### Option A: Use Existing Style Profile (Recommended)

1. Check for `.monthly-style.md` in the current working directory.
2. If found, read it (~200–400 tokens) and apply its style characteristics.
3. **Scope guard**: Only accept `./.monthly-style.md` (cwd). Ignore any `.monthly-style.md` under skill `references/` paths.

### Option B: Create New Style Profile (First Time Only)

If `.monthly-style.md` doesn't exist:

1. Find existing monthly journals matching `20[0-9][0-9]-[0-1][0-9].md`.
2. Read the 2–3 most recent ones.
3. Analyze:
   - Tone
   - Sentence structure
   - Detail level
   - Use of lists vs prose
   - Use of links, callouts, and personal phrases
4. Generate `.monthly-style.md` using the format in `references/.monthly-style.md`.
5. Apply the learned style.

**If no monthly journals or profile exist**: use neutral, natural style based on the user's input tone.

## Step 3: Build the Index Section

### 本月周记：

List all overlapping ISO weeks as wikilinks:

```markdown
### [[2024-W48]]
### [[2024-W49]]
### [[2024-W50]]
### [[2024-W51]]
### [[2024-W52]]
```

This section is navigation only, not the content source.

### 本月主线：

Write 3–5 sentences that answer:
- What actually drove this month?
- What was the lived main thread, not the intended goal?

Then add a separate keyword heading:

```markdown
### 关键词：
- 关键词A / 关键词B / 关键词C
```

Use 3–4 keywords. Prefer plain text keywords, not global tags.

## Step 4: Fill Content Sections

Before writing, scan all daily files for:
- Mood arc across the month
- Work rhythm shifts
- Sleep/fatigue patterns
- Recurring social themes
- Repeated topics in reflections and thoughts
- What kept coming back on 3+ days

Use those patterns as hidden scaffolding.

### Work Section (工作)

#### 保持
- Source: recurring strengths from "成果和进展" and "复盘"
- Keep only patterns worth carrying forward
- Focus on habits, workflows, judgment, collaboration, or discipline that proved useful
- Bullet list

#### 问题
- Source: recurring work friction from "复盘" and failed/blocked progress
- Keep only the real problems that repeated or mattered
- Prefer patterns over one-off complaints
- Bullet list

#### 尝试
- Source: next-step improvements implied by the month
- Write 1–3 concrete adjustments for next month
- These should be experiments, not grand goals
- Bullet list

#### 里程碑
- Source: the most important completed items, decisions, or turning points
- Write 3–5 items max
- Only include things that actually changed the month
- Bullet list

### Life Section (生活)

#### 生命之轮
- Rate exactly these six dimensions:
  - 工作
  - 健康
  - 财务
  - 娱乐
  - 成长
  - 关系
- Use a Markdown table
- Give each row a short, specific reason
- **This is AI-inferred** and should stay modest, concrete, and revisable

#### 高光
- Write 3–5 items
- Can include events, turning points, relational shifts, emotional peaks, or especially memorable moments
- If something feels like "best of the month", fold it into 高光 instead of creating a separate section

#### 所幸
- Source: daily "感恩", plus recurring people, tools, places, or fortunate turns
- Write 3–5 selected items
- This section is broader than gratitude: include what felt worth庆幸、感谢、珍惜
- Use links naturally when relevant

#### 觉察
- This is the most month-specific section
- Write only **cross-week patterns or trends**
- Use a single callout block
- Let the title be generated freely based on the month's core insight
- Example shape:

```markdown
> [!note]+ 恢复不是躺平
> - 我发现……
> - 这个月反复出现……
```

- Good 觉察 usually answers one or more of:
  - What did I keep falling into?
  - What reliably restored me?
  - What started to shift this month?
  - What is becoming more true about me?

#### 迁移
- This is a month-end filter, not a wish list
- Use exactly three bullets:
  - `继续`
  - `停止`
  - `开始`
- Keep them short and decision-oriented

#### 下月重点
- Write 1–3 real priorities
- Avoid grand ambition
- Prioritize directional clarity over completeness

#### 本月回看
- This section may be longer and more literary than the others
- Use it to preserve the month's texture, atmosphere, and memorable fragments
- It should feel like: "What did this month actually feel like?"
- Do **not** rewrite all of the above sections in longer form
- Do **not** turn it into a daily timeline
- Prefer thematic prose over bullet lists

## Step 5: Apply Writing Style and Cross-References

1. Match the user's tone, vocabulary, and detail level from the style profile.
2. Add cross-references when naturally useful:
   - previous monthly journals: `[[2024-11]]`
   - weekly journals: `[[2024-W52]]`
   - important daily entries: `[[2024-12-20]]`
   - projects or people: `[[项目名称]]`, `[[真名|昵称]]`
3. Do not force links for the sake of density.

## Step 6: Save or Fill the Monthly Journal File

1. Check whether `./YYYY-MM.md` already exists.
2. If it exists and is blank or still template-like, fill it in.
3. If it does not exist, create it.
4. If it already has substantial content, ask before overwriting:
   > "检测到 2024-12.md 已经有内容了，要覆盖吗？"

## Writing Guidelines

- Keep the original section structure intact
- Write in first person for personal sections
- Be specific and concrete
- Sparse months can stay short; do not pad
- Maintain Chinese headings and structure
- Preserve month-specific texture while still making decisions
- Keep heading punctuation consistent with the template, including full-width `：`

### Anti-AI-smell rules

1. **Do not turn monthlies into bigger weeklies**
2. **Do not repeat the same point across 主线 / 觉察 / 回看 unless the later section meaningfully deepens it**
3. **Do not use vague praise words** like "收获很多" without saying what the gain was
4. **Do not force symmetry** across sections
5. **Do not end with generic optimism**
6. **Let emotions be earned by concrete events**

## Example Usage

**User input:**
"帮我写 2024-12 的月记"

**Generated file**: `2024-12.md` based on that month's daily journals.

## Important Notes

- Always save files with UTF-8 encoding
- Use `YYYY-MM` format — never `YYYY-M`
- Read daily journals directly instead of summarizing weekly journals
- Check for `.monthly-style.md` first
- Create a style profile on first use if helpful
- The 本月周记索引 section should list all overlapping weeks, even if some files are missing
