---
name: daily-journal
description: Generate daily journal entries from user's life content. Use when user wants to create a diary entry, write a journal, or document their daily activities. The skill transforms user's narrative into a structured journal format with work progress, reflections, emotions, gratitude, and thoughts sections.
---

# Daily Journal Generator

Generate structured daily journal entries from user's life content using a predefined template.

## Quick Start

When the user provides their daily life content, follow this workflow:

1. **Extract information** from user's narrative
2. **Generate journal entry** following the template structure
3. **Save the file** as `YYYY-MM-DD.md` in the current working directory

## Template Structure

The journal follows this structure:

```markdown
---
创建时间: [Current datetime]
更新时间: [Current datetime]
tags:
  - 日记
  - 工作
  - 生活
---
<< [[previous-day]] | [[next-day]] >>

## 工作
### 成果和进展
### 明日工作安排
### 复盘

## 生活
### 流水账
#### 情绪
#### 感恩
#### 成就
### 反思
### 思绪
### Memos
```

Full template reference: [references/template.md](references/template.md)
Style profile template reference: [references/.journal-style.md](references/.journal-style.md)

**Hard rule for style profile source:**
- Treat `./.journal-style.md` in the **current working directory** as the only real style profile.
- `skills/daily-journal/references/.journal-style.md` is a **template format reference only**.
- Never use `references/.journal-style.md` as personal style data.

## Generating the Journal

### Step 0: Learn Writing Style (Optional)

**This step can be skipped to save tokens if user prefers.**

Before generating the journal, learn the user's writing style using a style profile:

#### Option A: Use Existing Style Profile (Recommended - Saves Tokens)

1. **Check for style profile**: Look for `.journal-style.md` file in current directory
2. **If found**: Read the style profile (only ~200-500 tokens)
3. **Apply the style**: Use the documented style characteristics when generating the journal
4. **Scope guard**: Only accept `./.journal-style.md` (cwd). Ignore any `.journal-style.md` under skill `references/` paths.

#### Option B: Create New Style Profile (First Time Only)

If `.journal-style.md` doesn't exist:

1. **Check for recent journals**: Look for files matching `YYYY-MM-DD.md` pattern in current directory
2. **Read recent entries**: If found, read the 3-5 most recent journal files to gather sufficient style data
3. **Analyze writing style**:
   - Sentence structure (short vs long, simple vs complex)
   - Tone (casual vs formal, humorous vs serious)
   - Level of detail (concise vs elaborate)
   - Vocabulary choices (colloquial vs literary)
   - Emotional expression style (direct vs subtle)
   - Paragraph organization patterns
   - Common phrases and expressions
4. **Generate style profile**: Create `.journal-style.md` file with the analysis
5. **Use the style**: Apply the learned style to current journal generation

**Style Profile Format:**

```markdown
# 日记写作风格档案

## 语气特征
- 整体风格：[随意/正式/中性]
- 幽默感：[有/无，如何体现]
- 情绪表达：[直接/含蓄]

## 常用表达
- 口头禅：[列出常用词汇，如"哈哈"、"咔咔"、"挺"等]
- 语气词：[列出，如"嘛"、"呢"、"啊"等]
- 特色表达：[列出独特的表达方式]

## 句式特点
- 句子长度：[短句为主/长短结合/长句为主]
- 句式复杂度：[简单/中等/复杂]
- 段落组织：[一句一段/多句成段]

## 详细程度
- 工作部分：[简洁/适中/详细]
- 生活部分：[简洁/适中/详细]
- 情绪部分：[简洁/适中/详细]
- 反思部分：[简洁/适中/详细]

## 特殊习惯
- [列出任何特殊的写作习惯或偏好]

## 示例句子
- 工作：[1-2个典型句子]
- 生活：[1-2个典型句子]
- 情绪：[1-2个典型句子]
```

**Token Efficiency:**
- First time (create profile): ~7000-10000 tokens (analyze 3-5 journals + generate profile)
- Subsequent uses: ~2500-3000 tokens (read profile ~300 tokens + generate journal)
- **Average savings: 60-70% compared to reading full journals each time**

**If no journals or profile exist**: Use neutral, natural style based on user's input tone.

### Step 1: Process User Input

Analyze the user's narrative and extract:
- Work accomplishments and progress
- Tomorrow's work plans
- Work reflections
- Life events and details
- Emotions and feelings
- Things to be grateful for
- Achievements
- Reflections on choices and behaviors
- Random thoughts
- Quick notes

### Step 2: Replace Templater Syntax

Replace Obsidian Templater syntax with actual values:

- `<% tp.file.creation_date() %>` → Current datetime (e.g., "2026-01-26 14:30")
- `<% tp.file.last_modified_date() %>` → Current datetime
- `<% tp.date.now("YYYY-MM-DD", -1) %>` → Previous day (e.g., "2026-01-25")
- `<% tp.date.now("YYYY-MM-DD", 1) %>` → Next day (e.g., "2026-01-27")

### Step 3: Fill Content

Map extracted information to template sections:

**Work Section:**
- List concrete tasks and achievements under "成果和进展"
- Write tomorrow's plans under "明日工作安排"
- Reflect on workflow and improvements under "复盘"

**Life Section:**
- Record meaningful life details under "流水账"
- Describe emotions with format: "今天我感到 [情绪]，因为 [事件描述]" under "情绪"
  - Available emotion tags: #开心 #充实 #惊喜 #得意 #暖心 #平静 #难过 #烦躁 #迷惘 #孤独 #生气 #尴尬 #委屈 #甜蜜 #梦境 #疲惫 #逃避 #不知道
- Write gratitude items with format: "今天我感激 [人或事]，因为 [具体原因]。这让我意识到 [个人感悟]" under "感恩"
- List achievements under "成就"
- Reflect on choices and their impact under "反思"
- Write free-form thoughts under "思绪"
- Add quick notes under "Memos"

### Step 4: Apply Writing Style and Add Cross-References

Before finalizing the journal content:

1. **Apply learned writing style**:
   - Match the sentence structure, tone, and vocabulary from recent journals
   - Maintain consistency in emotional expression
   - Use similar level of detail and paragraph organization

2. **Add cross-references** (if recurring themes detected):
   - When mentioning ongoing projects/events, add reference to previous mention
   - Example: "继续推进 X 项目（参见 [[2026-10-01]]）"
   - When emotions are similar to recent days, optionally note the pattern
   - Example: "情绪依然有些低落（和 [[2026-10-05]] 类似）"
   - When completing yesterday's planned tasks, reference yesterday's journal
   - Example: "完成了昨天计划的任务（[[2026-10-06]]）"

3. **Check yesterday's "明日工作安排"**:
   - If yesterday's journal was read in Step 0, compare with today's accomplishments
   - Optionally add a note about completion status

**Cross-reference guidelines:**
- Use Obsidian-style links: `[[YYYY-MM-DD]]`
- Only add references when naturally relevant, don't force it
- Keep references concise and helpful

### Step 5: Save File

Use Write tool to save the journal entry:
- **File path**: `./YYYY-MM-DD.md` (use today's date in current working directory)
- **Content**: The complete journal entry with all sections filled, styled consistently, and with relevant cross-references

The file will be saved in the current working directory where the user runs the command.

Example filename: `./2026-01-26.md` (saved in current directory)

## Writing Guidelines

- Keep the original template structure intact
- Use bullet points for lists
- Write in first person for personal sections
- Be specific and concrete, not generic
- If user doesn't provide information for a section, keep the section header but leave it empty or write minimal content
- Maintain the Chinese language for section headers and structure
- **Match the user's personal writing style** learned from recent journals (tone, vocabulary, sentence structure)
- **Add cross-references** to related previous entries when naturally relevant
- Use natural, conversational tone that reflects the user's voice

## Example Usage

**User input:**
"今天完成了项目的核心功能开发，修复了3个bug。明天计划进行测试。工作上感觉很有成就感。晚上和朋友吃饭，聊得很开心。我感激朋友的陪伴，让我感到温暖。"

**Generated journal** (saved as 2026-01-26.md):
```markdown
---
创建时间: 2026-01-26 20:30
更新时间: 2026-01-26 20:30
tags:
  - 日记
  - 工作
  - 生活
---
<< [[2026-01-25]] | [[2026-01-27]] >>

## 工作

### 成果和进展：
- 完成了项目的核心功能开发
- 修复了3个bug

### 明日工作安排：
- 进行项目测试

### 复盘：
- 今天的工作效率很高，核心功能顺利完成，感觉很有成就感

## 生活

### 流水账：
- 晚上和朋友吃饭，聊得很开心

#### 情绪：
#开心 #暖心
- 今天我感到开心，因为工作完成得很顺利，晚上和朋友的聚会也很愉快。

#### 感恩：
1. 今天我感激朋友的陪伴，因为让我感到温暖。这让我意识到友情的珍贵。

#### 成就：
1. 完成项目核心功能开发

### 反思：
- 今天工作和生活都很充实，平衡得不错

### 思绪：
- 工作带来的成就感和朋友的陪伴，都是生活中重要的部分

### Memos：
- 继续保持工作和生活的平衡
```

## Important Notes

- Always save files with UTF-8 encoding
- Use today's date if user doesn't specify a date
- If user provides minimal information, generate concise content rather than leaving sections completely empty
- Preserve all Chinese section headers and structure from the template
- **Check for `.journal-style.md` first** before reading full journal files (saves tokens)
- **Create style profile on first use** if multiple journal files exist but no profile found
- **Use Glob tool** to find files: `.journal-style.md` for profile, `20*.md` for journals
- **Profile path rule**: profile file must be `./.journal-style.md` in current working directory; do not treat skill reference files as user profile
- **Add cross-references naturally** when mentioning recurring themes, ongoing projects, or related events
- **Maintain style consistency** by following the style profile or learned patterns
