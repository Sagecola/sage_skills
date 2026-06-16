# Skill Catalog

This catalog groups skills by purpose while keeping installation compatible with the current flat `skills/<name>` layout.

## Productivity

### daily-journal
- Path: `skills/daily-journal`
- Summary: Generate structured daily journals from free-form daily notes, with optional writing-style profiles and cross-entry references.
- Primary file: `skills/daily-journal/SKILL.md`
- Typical trigger: "write a daily journal", "生成今日日记"

### weekly-journal
- Path: `skills/weekly-journal`
- Summary: Generate structured weekly journals from daily journal files. Distills daily entries (流水账, 情绪, 感恩, 成就, 复盘, 思绪) into weekly format (内容, 进展, 改进, 计划, 回顾, 健康, 社交, 成长, 娱乐, 思考). When no strong reflection exists, offers contextual thinking prompts. Checks for existing blank weekly file first, then fills or creates.
- Primary file: `skills/weekly-journal/SKILL.md`
- Typical trigger: "帮我写 2026-W01 的周记", "生成本周周记", "写周记"

### monthly-journal
- Path: `skills/monthly-journal`
- Summary: Generate structured monthly journals from daily journal files (skipping the weekly layer to avoid compounding information loss). Distills daily entries directly into monthly format: 本月索引 (本周周记 / 本月主线 / 关键词), work review (保持 / 问题 / 尝试 / 里程碑), life review (生命之轮 / 高光 / 所幸 / 觉察 / 迁移 / 下月重点 / 本月回看). Treats the monthly note as a map and strategy guide rather than an expanded weekly summary. Checks for existing blank monthly file first, then fills or creates.
- Primary file: `skills/monthly-journal/SKILL.md`
- Typical trigger: "帮我写 2024-02 的月记", "生成本月月记", "写月记"

### obsidian-note
- Path: `skills/obsidian-note`
- Summary: Generate structured Obsidian notes with correct YAML frontmatter and content sections for 7 note types: 影视, 书籍, 人际, 播客, 代码, 报告, 通用.
- Primary file: `skills/obsidian-note/SKILL.md`
- Typical trigger: "帮我写一篇笔记", "新建影视笔记", "创建人际档案", "obsidian note"

### chinese-typeset-polish
- Path: `skills/chinese-typeset-polish`
- Summary: Apply Chinese/mixed-language typesetting standards and light polishing with strict meaning preservation, rule priorities, and file-vs-dialog output modes.
- Primary file: `skills/chinese-typeset-polish/SKILL.md`
- Typical trigger: "中文排版优化", "润色这段文案", "处理中英混排", "按规范整理这篇文章"

### file-organizer
- Path: `skills/file-organizer`
- Summary: Personal file organization assistant for naming, classifying, and safely archiving messy files into the "人生档案馆" system. Safety-first workflow: inspect first, present classification plan, wait for confirmation, then move or rename.
- Primary file: `skills/file-organizer/SKILL.md`
- Typical trigger: "帮我整理文件", "这个文件放哪", "Downloads 好乱", "帮我分类", "按规则重命名"

### daylog
- Path: `skills/daylog`
- Summary: Generate readable daily summaries and diary material from local AI coding assistant conversation history and browser history. Extracts raw logs from Codex, Claude Code, Kimi Code CLI, and opencode, then writes narrative summaries. Supports migration from backup data on another computer.
- Primary file: `skills/daylog/SKILL.md`
- Typical trigger: "查 AI 对话记录", "整理工作日志", "写日记素材", "summarize my coding sessions"

## Engineering

### ammonia-tower-design
- Path: `skills/ammonia-tower-design`
- Summary: Ammonia nitrogen stripping and absorption packed-tower design workflow for wastewater treatment. Includes tower diameter, packing height, packing comparison, wetting/circulation checks, Blackwell/Kister GPDC/Mackowiak SBD hydraulics, and Onda mass-transfer sizing. Python calculator with HG/T 3986-2016 and HG/T 4374-2012 packing data.
- Primary file: `skills/ammonia-tower-design/SKILL.md`
- Typical trigger: "氨氮吹脱塔设计", "填料塔计算", "ammonia tower design"

## Naming Rules

- Skill directory: kebab-case, e.g., `meeting-notes-cleaner`
- Required entry file: `SKILL.md`
- Optional support folders: `references/`, `scripts/`, `assets/`

## Add a New Skill

1. Create `skills/<skill-name>/SKILL.md`.
2. Add references/scripts/assets only when needed.
3. Register the skill in this catalog.
4. Validate with:
   - `./scripts/install-skills.ps1 -DryRun`
   - `./scripts/install-skills.ps1`
   - `./scripts/install-skills.ps1 -SkillName <skill-name>`
