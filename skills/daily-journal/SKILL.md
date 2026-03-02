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
3. **Save the file** as `YYYY-MM-DD.md` in `C:\Users\MSA\Desktop\test`

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

### Step 4: Save File

Use Write tool to save the journal entry:
- **File path**: `C:\Users\MSA\Desktop\test\YYYY-MM-DD.md` (use today's date)
- **Content**: The complete journal entry with all sections filled

Example filename: `C:\Users\MSA\Desktop\test\2026-01-26.md`

## Writing Guidelines

- Keep the original template structure intact
- Use bullet points for lists
- Write in first person for personal sections
- Be specific and concrete, not generic
- If user doesn't provide information for a section, keep the section header but leave it empty or write minimal content
- Maintain the Chinese language for section headers and structure
- Use natural, conversational tone for content

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
