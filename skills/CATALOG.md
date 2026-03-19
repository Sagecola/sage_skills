# Skill Catalog

This catalog groups skills by purpose while keeping installation compatible with the current flat `skills/<name>` layout.

## Productivity

### daily-journal
- Path: `skills/daily-journal`
- Summary: Generate structured daily journals from free-form daily notes, with optional writing-style profiles and cross-entry references.
- Primary file: `skills/daily-journal/SKILL.md`
- Typical trigger: "write a daily journal", "生成今日日记"

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
