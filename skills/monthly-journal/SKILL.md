---
name: monthly-journal
description: Generate monthly journal entries from daily journal files. Use when user wants to create a monthly review, write a monthly summary, or consolidate the month's work and life. The skill distills daily journals (skipping the weekly layer) into a structured monthly format with work summary, life review with ratings, achievements, challenges, gratitude, and reflection. Reads daily journals directly to avoid compounding information loss from weekly distillation.
---

# Monthly Journal Generator

Generate structured monthly journal entries from daily journal files, following the user's personal conventions.

## Quick Start

When the user requests a monthly journal, follow this workflow:

1. **Determine the target month** — identify which month to write for
2. **Gather content** — by reading daily journal files for that month
3. **Learn writing style** — check for `.monthly-style.md` profile
4. **Generate the monthly journal** following the template structure
5. **Save the file** as `YYYY-MM.md` in the current working directory

## File Naming Convention

Monthly journals use year-month format: `YYYY-MM.md`

- Examples: `2024-02.md`, `2024-03.md`, `2026-05.md`
- Use zero-padded month number
- If user says "this month" and today is 2026-05-03, that is `2026-05`

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
## 本月周记汇总
### [[YYYY-Www]]
... (all weeks of the month)

## 工作

### 总结：
### 内容：
### 改进：
### 下月计划：
### 反思：

## 生活

### 评估：
- **工作**：X/10，**原因**：
- **健康**：X/10，**原因**：
- **财务**：X/10，**原因**：
- **娱乐**：X/10，**原因**：
- **成长**：X/10，**原因**：
- **家庭**：X/10，**原因**：
- **朋友**：X/10，**原因**：
- **伴侣**：X/10，**原因**：

### 成就：
### 挑战：
### 感恩：
### 展望：
### 感想：
```

Full template reference: [references/template.md](references/template.md)
Style profile template reference: [references/.monthly-style.md](references/.monthly-style.md)

**Hard rule for style profile source:**
- Treat `./.monthly-style.md` in the **current working directory** as the only real style profile.
- `skills/monthly-journal/references/.monthly-style.md` is a **template format reference only**.
- Never use `references/.monthly-style.md` as personal style data.

---

## Step 0: Determine the Target Month

1. If the user specifies a month (e.g., "3月", "2024-02", "二月"), resolve it to `YYYY-MM`.
2. If the user says "this month" or gives no date, use the current date.
3. Compute the first and last day of that month (needed for finding daily journals).
4. Compute which ISO weeks overlap with the target month (for the weekly summary section).

**ISO week calculation reference:**
- Find which ISO weeks overlap with the target month
- A month typically contains 4–5 weeks
- Example: 2024-02 contains W05, W06, W07, W08, W09

---

## Step 1: Locate Daily Journal Files

1. **Compute the date range** for the target month (first day to last day).
2. **Search in the current working directory first**: use Glob for `YYYY-MM-DD.md` matching each day of the month.
3. **If no daily files found in cwd**, ask the user:
   > "没有在当前目录找到这月的日记文件，请问日记存放在哪个目录？"
   Then search in the path the user provides.
4. **Read each daily file found** — it's fine if some days are missing.
5. **If zero daily files found anywhere**: ask the user to describe the month before proceeding.

### Synthesis mindset when reading daily journals

Daily journals are raw and granular. Your job is to **elevate directly to the monthly perspective**, skipping the weekly abstraction layer entirely. Think of it as:
- **工作部分**: What were the major projects and themes this month? What moved forward from start to end? What's the overall trajectory?
- **生活部分**: What moments mattered? What patterns emerged across the month? What were the emotional highlights?
- **成就部分**: Which accomplishments from across the month are truly significant at the monthly level?
- **感恩部分**: Who and what left a lasting impression this month?
- **评估部分**: Based on the full month's daily details, how would you rate each life dimension?

The monthly journal should read like a thoughtful monthly retrospective — not a concatenation of daily or weekly entries. Reading daily journals directly gives you access to details (specific meals, people, small wins) that would be lost if only reading weekly summaries.

---

## Step 2: Learn Writing Style

**This step can be skipped to save tokens if user prefers.**

#### Option A: Use Existing Style Profile (Recommended)

1. Check for `.monthly-style.md` in the current working directory.
2. If found, read it (~200–400 tokens) and apply its style characteristics.
3. **Scope guard**: Only accept `./.monthly-style.md` (cwd). Ignore any `.monthly-style.md` under skill `references/` paths.

#### Option B: Create New Style Profile (First Time Only)

If `.monthly-style.md` doesn't exist:

1. Use Glob to find existing monthly journals matching `20[0-9][0-9]-[0-1][0-9].md` in the current directory.
2. Read the 2–3 most recent ones to gather style data.
3. Analyze:
   - Tone (casual vs formal, humorous vs serious)
   - Sentence structure and length
   - Vocabulary and expressions
   - Level of detail per section
   - Use of Obsidian links, callouts, tags
   - Paragraph vs list preference per section
4. Generate `.monthly-style.md` using the format in `references/.monthly-style.md`.
5. Apply the learned style to the current journal.

**Token efficiency:**
- First time (create profile): ~5000–8000 tokens
- Subsequent uses: ~1500–2000 tokens (profile ~300 tokens + generation)
- **Average savings: 60–70%**

**If no monthly journals or profile exist**: Use neutral, natural style based on the user's input tone.

---

## Step 3: Build the Weekly Summary Section

List all weeks of the month as wikilinks (this section is for navigation, not content source):

```markdown
## 本月周记汇总

### [[2024-W05]]
### [[2024-W06]]
### [[2024-W07]]
### [[2024-W08]]
### [[2024-W09]]
```

Include all weeks that overlap with the target month (typically 4–5 weeks), regardless of whether weekly journal files exist.

---

## Step 4: Fill Content Sections

This is the core transformation step. Daily journals are raw and granular; monthly journals are synthesized and high-level. The key principle: **elevate directly from daily to monthly, capturing details that weekly summaries would lose**.

### What to DROP from daily journals

These daily journal sections do NOT appear in the monthly journal:
- **情绪 tags** (`#开心 #疲惫` etc.) — daily-level granularity, but their content informs 评估
- **Memos** — ephemeral notes not worth preserving at monthly level
- **明日工作安排** from each day — only the last day's plan informs 下月计划
- **Minor daily details** — what was eaten, routine commutes, trivial errands
- **流水账 timestamps** — specific times of day are not relevant at monthly level

### What to KEEP that weekly summaries would lose

Pay special attention to these details that often get filtered out in weekly journals:
- **Specific achievements** — tasks completed, skills learned, problems solved
- **Specific people mentioned** — colleagues, friends, family who appear repeatedly
- **Specific places, restaurants, tools** — concrete details that make the journal feel personal
- **Emotional arc** — how feelings evolved across the month
- **Recurring themes** — patterns that appear across multiple days

### Work Section (工作)

**总结 (Summary)**
- Source: synthesize all days' "成果和进展" and "复盘"
- Write ONE paragraph covering the month's main work themes and trajectory
- Mention key projects, major milestones, and overall progress direction
- This should capture the arc of the month — what was the story?
- Example: "在3月份，我的工作重心主要围绕X项目的推进和Y工艺的优化展开。通过多次实验和现场调试，我们在X方面取得了突破性进展，同时也积累了宝贵的经验教训。"

**内容 (Content)**
- Source: all days' "成果和进展" — extract only the substantive monthly-level items
- DROP: routine tasks, minor fixes, single-day activities
- KEEP: major deliverables, key decisions, project milestones, significant conversations
- Bullet list, use Obsidian links for projects/people/places

**改进 (Improvements)**
- Source: all days' "复盘" — extract only the recurring or impactful lessons
- DROP: day-specific tactical fixes
- KEEP: systemic process improvements, behavioral patterns to change
- Bullet list, focus on what can be done differently at a higher level

**下月计划 (Next Month Plan)**
- Source: the last few days' "明日工作安排" + any forward-looking items mentioned across the month
- Bullet list of next month's priorities, scheduled events, and goals

**反思 (Reflection)**
- Source: all days' "反思" and "思绪" — synthesize into a cohesive monthly reflection
- This should feel like genuine insight, not a recap
- Connect the dots between different days' experiences

### Life Section (生活)

**评估 (Rating)**
- Source: infer from daily journals' 流水账, 情绪, 感恩, 成就, 反思, 思绪 across the entire month
- Rate each dimension on a 1–10 scale with a brief reason
- Dimensions: 工作, 健康, 财务, 娱乐, 成长, 家庭, 朋友, 伴侣
- **This is AI-inferred — the user will manually adjust**
- Be honest and specific in the reason — use concrete details from the daily journals
- Example: `- **健康**：7/10，**原因**：运动频率有所提升，但饮食习惯仍需改善，外卖次数偏多。`

**成就 (Achievements)**
- Source: all days' "成就" and "成果和进展" — select only the most significant ones
- DROP: trivial achievements, routine completions
- KEEP: major milestones, skill acquisitions, meaningful accomplishments
- Bullet list, be specific about why each matters
- This is where reading daily journals pays off — capture achievements that weekly summaries miss

**挑战 (Challenges)**
- Source: all days' "反思" and "思绪" where challenges are discussed
- Consolidate recurring or major challenges
- DROP: one-off minor issues
- KEEP: persistent problems, significant obstacles, lessons from failures
- Include how they were addressed (or not)

**感恩 (Gratitude)**
- Source: all days' "感恩" — merge and deduplicate
- **Pay attention to specific names** — people, restaurants, tools, platforms that appear repeatedly
- DROP: routine thank-yous, minor acknowledgments
- KEEP: deeply felt gratitude, significant people/organizations/events
- Group by theme (people, tools, experiences) if natural
- Use Obsidian links for people: `[[真名|昵称]]`

**展望 (Outlook)**
- Source: synthesize all forward-looking items from across the month
- Focus on 2–3 key areas for next month
- Include specific actionable items, not vague aspirations

**感想 (Reflections)**
- Source: the most meaningful thought or realization from the month (from "思绪" sections)
- This should be a genuine, personal reflection — not a summary
- Write as if talking to yourself about what this month meant

---

## Step 5: Apply Writing Style and Cross-References

1. **Apply learned style**: Match tone, vocabulary, sentence structure, and detail level from the style profile.
2. **Add cross-references** when naturally relevant:
   - Reference previous monthly journals: `[[2024-01]]`
   - Reference specific weekly journals: `[[2024-W08]]`
   - Reference ongoing projects or notes: `[[项目名称]]`
   - Only add when it genuinely adds context — don't force it.
3. **Use Obsidian links** for people (`[[真名|昵称]]`), places, and recurring topics, consistent with the user's existing style.

---

## Step 6: Save or Fill the Monthly Journal File

1. **Check if the file already exists**: use Glob or Read to check for `./YYYY-MM.md` in the current directory.
2. **If the file exists and is blank or has only the template structure**:
   - Read the existing file
   - Fill in the content sections while preserving the frontmatter and structure
   - Use Edit tool to replace the empty sections with generated content
3. **If the file doesn't exist**:
   - Use Write tool to create `./YYYY-MM.md` with complete content
4. **File path**: always save in the current working directory as `YYYY-MM.md`

Example: `./2024-02.md`

**Important**: If the existing file already has substantial content (not just template headers), ask the user before overwriting:
> "检测到 2024-02.md 已经有内容了，要覆盖吗？"

---

## Writing Guidelines

- Keep the original template structure intact — all section headers must be present
- Write in first person for personal sections
- Be specific and concrete, not generic
- If a section has no content, keep the header and write a brief honest note (e.g., "本月无特别挑战记录")
- Maintain Chinese for all section headers and structure
- **Match the user's personal writing style** from the style profile
- **Work section**: prefer paragraph for 总结/反思; bullet lists for 内容/改进/计划
- **Life section**: bullet list for 评估; paragraph narrative for 感想; bullet lists for 成就/挑战/感恩/展望
- The 感想 section should feel like genuine reflection, not a summary — encourage depth over breadth
- **评估 ratings should be AI-inferred** from daily journal content, with a note that the user will adjust
- **Preserve specific details** from daily journals — names, places, tools, restaurants — these make the journal personal

---

## Example Usage

**User input:**
"帮我写2月的月记"

**Generated file**: `2024-02.md` with all sections filled based on the daily journals found for February.

---

## Important Notes

- Always save files with UTF-8 encoding
- Use `YYYY-MM` format — never `YYYY-M` (single digit)
- If user doesn't specify a month, default to the current month
- When reading daily journals to synthesize, **elevate to monthly perspective** — don't just concatenate
- **Read daily journals directly** to avoid compounding information loss from weekly distillation
- **Check for `.monthly-style.md` first** before reading full monthly journal files (saves tokens)
- **Create style profile on first use** if multiple monthly journals exist but no profile found
- **Profile path rule**: profile must be `./.monthly-style.md` in cwd; never treat skill reference files as user profile
- The 本月周记汇总 section always lists all weeks of the month, even if no weekly files exist for some weeks

---

## Usage Pattern

The user will explicitly request monthly journal generation when ready:
- "帮我写 2024-02 的月记"
- "生成本月月记"
- "根据日记写月记"

When invoked:
1. Determine the target month (from user input or current date)
2. Calculate the first and last day of the month
3. Calculate which ISO weeks overlap with that month (for the summary section)
4. Use Glob to find daily journal files matching `YYYY-MM-DD.md` in the current directory
5. Filter to only the days within the target month
6. Read each daily journal file found
7. Check for `.monthly-style.md` profile (or create one if multiple monthly journals exist)
8. Synthesize the content following the distillation rules in Step 4
9. Generate and save `YYYY-MM.md`

The user maintains full control over when to generate and can review/edit the output afterward.
