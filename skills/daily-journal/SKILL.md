---
name: daily-journal
description: Generate daily journal entries from user's life content with personalized writing style. Use when user wants to create a diary entry, write a journal, or document their daily activities. The skill learns from user's past entries to mimic their unique writing style, tone, and expression patterns.
---

# Daily Journal Generator

Generate structured daily journal entries from user's life content using a predefined template. This skill **learns and adapts** to your personal writing style over time.

## Quick Start

When the user provides their daily life content, follow this workflow:

1. **Analyze writing style** from past journal entries (if available)
2. **Extract information** from user's narrative
3. **Generate journal entry** following the template structure with personalized style
4. **Save the file** as `YYYY-MM-DD.md` in the output directory

### Output Directory Selection

Determine the output directory in this priority order:
1. **User-specified path** - If user explicitly mentions where to save (e.g., "保存到桌面", "放在 D:\\Notes 文件夹")
2. **Current working directory** - Default if no path is specified (the directory where the user is running this command)
3. **Desktop fallback** - If current directory is unavailable or inappropriate, use the user's Desktop (`%USERPROFILE%\\Desktop` or `~/Desktop`)

Use the `pwd` or equivalent command to check the current working directory before saving.

## Personalized Style Learning

### Step 1: Analyze Past Entries

Before generating a new journal entry, **scan the output directory for existing journal files** (pattern: `YYYY-MM-DD.md` or `*.md`).

If history entries exist (≥1 file), analyze the user's writing style by examining:

**Style Dimensions to Extract:**

| Dimension | What to Look For | Examples |
|-----------|------------------|----------|
| **Tone** | Formal vs casual, emotional vs factual | "甚是疲惫" vs "累死了" |
| **Sentence Length** | Short/brief vs long/detailed | "搞定" vs "终于完成了这个困扰已久的任务" |
| **Vocabulary** | Preferred words, catchphrases, emoji usage | 常用 "芜湖"、"绝了"、"🎉" |
| **Expression Style** | Direct vs poetic, literal vs metaphorical | "工作很多" vs "今天像是被任务追着跑" |
| **Detail Level** | Minimal vs comprehensive | 一句话带过 vs 多维度描述 |
| **Humor Level** | Serious vs playful | "又加班了😭" vs "今日加班成就达成（1/1）" |
| **Reflection Depth** | Surface-level vs introspective | "今天不错" vs "意识到自己的焦虑源于对完美的执着" |
| **Structuring Preference** | Bullet-heavy vs paragraph style | 多条简短要点 vs 连贯叙述 |

**Analysis Method:**
1. Read the most recent 3-5 journal entries
2. Extract 3-5 representative phrases/sentences from each
3. Summarize the dominant style characteristics

### Step 2: Apply Style to New Entry

When generating content, apply the learned style:

- **Match the vocabulary**: Use words and phrases the user commonly uses
- **Match the tone**: If user is casual/funny, be casual/funny; if serious/reflective, be serious
- **Match the detail level**: Don't add elaborate descriptions if user prefers brevity
- **Match the sentence structure**: Mirror the user's sentence length and rhythm
- **Preserve catchphrases**: If user has signature expressions, use them appropriately

**If no history exists** (first-time user), use a balanced, natural conversational style as default.

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

## Generating the Journal

### Step 3: Process User Input

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

### Step 4: Replace Templater Syntax

Replace Obsidian Templater syntax with actual values:

- `<% tp.file.creation_date() %>` → Current datetime (e.g., "2026-01-26 14:30")
- `<% tp.file.last_modified_date() %>` → Current datetime
- `<% tp.date.now("YYYY-MM-DD", -1) %>` → Previous day (e.g., "2026-01-25")
- `<% tp.date.now("YYYY-MM-DD", 1) %>` → Next day (e.g., "2026-01-27")

### Step 5: Fill Content with Personalized Style

Map extracted information to template sections, applying the learned style:

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

### Step 6: Save File

Use Write tool to save the journal entry:
- **File path**: `{output_dir}/YYYY-MM-DD.md` (use today's date)
  - `{output_dir}`: The output directory determined above (current working directory or user-specified path)
- **Content**: The complete journal entry with all sections filled

**Examples:**
- Current directory: `2026-01-26.md`
- Desktop: `C:\Users\MSA\Desktop\2026-01-26.md`
- User-specified: `D:\Notes\Journal\2026-01-26.md`

**Before saving**, confirm the path with the user if it's not the current working directory.

## Style Adaptation Examples

### Example 1: Casual & Humorous Style

**User's past style:**
> "今天终于把那个破bug修好了，芜湖！🎉 感觉像是打赢了一场boss战。明天继续肝下一个功能，希望能早点下班..."

**New entry (matching style):**
> "成果和进展：
> - 搞定了用户模块的重构，代码从 spaghetti 变成了勉强能看的 pasta ✓
> - 和 PM  battle 了三轮，终于把需求定下来了
>
> 复盘：
> - 今天状态还行，没有摸鱼太久（大概）。重构的时候差点被旧代码气死，还好忍住了没有重写整个项目。"

### Example 2: Concise & Factual Style

**User's past style:**
> "完成 API 文档。修复 2 个 bug。明日计划：接口联调。"

**New entry (matching style):**
> "成果和进展：
> - 完成支付模块接口开发
> - 更新 API 文档
> - 修复订单查询异常
>
> 明日工作安排：
> - 接口联调
> - 单元测试"

### Example 3: Reflective & Poetic Style

**User's past style:**
> "今日像是被时间推着走，事情一件接着一件。但傍晚的夕阳让我停下了脚步，突然意识到忙碌中遗漏了很多美好..."

**New entry (matching style):**
> "流水账：
> - 晨会、代码评审、需求讨论，一天在会议室与工位之间流转
> - 傍晚归途，看见银杏叶在路灯下泛着温柔的金光，莫名被治愈
>
> 情绪：
> #平静 #疲惫
> - 今天我感到一种奇怪的平静，像是暴风雨后的湖面。忙碌是表象，内心却在寻找某种锚点。"

## Writing Guidelines

- **Learn from history**: Always analyze past entries first to understand user's unique voice
- **Stay consistent**: Match the user's preferred level of detail and formality
- **Keep the structure**: Maintain the template sections regardless of style
- **Respect preferences**: If user writes short entries, don't generate long ones
- **Adapt vocabulary**: Use words and phrases the user commonly uses
- **Mirror emotion expression**: Some users are explicit about feelings, others are subtle
- **Use first person**: Always write from the user's perspective
- **Maintain Chinese headers**: Keep section headers in Chinese as per template

## Example Usage

**User input:**
"今天完成了项目的核心功能开发，修复了3个bug。明天计划进行测试。工作上感觉很有成就感。晚上和朋友吃饭，聊得很开心。我感激朋友的陪伴，让我感到温暖。"

**With casual style learned from history:**

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
- 核心功能开发 ✓ 终于搞完了！
- 顺手修了 3 个 bug，感觉自己今天像个代码杀手

### 明日工作安排：
- 开始测试，希望能少踩点坑

### 复盘：
- 今天效率在线，核心功能一次过（意外之喜）。修bug的时候差点被其中一个搞崩溃，还好最后解决了。

## 生活

### 流水账：
- 晚上和朋友约饭，聊得超嗨，时间居然过得这么快

#### 情绪：
#开心 #暖心 #充实
- 今天心情不错，工作顺利 + 朋友聚会，double快乐！

#### 感恩：
1. 感激朋友抽空陪我吃饭，忙了一天后有人陪着聊聊天，真的很治愈

#### 成就：
1. 项目核心功能开发完成
2. 修复 3 个 bug

### 反思：
- 今天工作与生活平衡得还行，没加班太久，给自己点个赞

### 思绪：
- 有时候觉得，工作上的成就感和朋友的陪伴，是生活里缺一不可的两部分

### Memos：
- 继续保持这个节奏
```

## Important Notes

- **Style learning is continuous**: Each new entry improves the style understanding
- **No history = neutral default**: For first-time users, use balanced, natural style
- **Always read before writing**: Scan the output directory before generating to check for existing entries
- **Save with UTF-8 encoding** to support Chinese characters properly
- **Use today's date** if user doesn't specify a date
- **Preserve template structure** even when adapting to user's writing style
- **Ask for clarification** if user's input is too minimal to understand their intent
