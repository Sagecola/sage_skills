# Daily Journal Skill

[English](#english) | [中文](#中文)

---

## English

`daily-journal` converts free-form daily notes into a structured journal entry.

### Highlights

- Structured template for work + life sections
- Optional writing-style profile (`.journal-style.md`) for consistency
- Optional cross-entry references (`[[YYYY-MM-DD]]`) when context matches
- Date-based output file naming (`YYYY-MM-DD.md`)

### Install (from this monorepo)

```powershell
Copy-Item ./scripts/targets.example.json ./scripts/targets.json
./scripts/install-skills.ps1 -DryRun
./scripts/install-skills.ps1
```

Install this skill only:

```powershell
./scripts/install-skills.ps1 -SkillName daily-journal
```

### Usage

Trigger naturally, for example:

- "write today's journal"
- "根据这些记录帮我生成今日日记"

Primary instruction file:

- `skills/daily-journal/SKILL.md`

References:

- `skills/daily-journal/references/template.md`
- `skills/daily-journal/references/.journal-style.md`

---

## 中文

`daily-journal` 用于将零散口述或笔记整理成结构化日记。

### 特性

- 工作 + 生活双分区模板
- 可选写作风格档案（`.journal-style.md`）
- 可选跨日记关联引用（`[[YYYY-MM-DD]]`）
- 按日期输出文件名（`YYYY-MM-DD.md`）

### 安装（在本仓库中）

```powershell
Copy-Item ./scripts/targets.example.json ./scripts/targets.json
./scripts/install-skills.ps1 -DryRun
./scripts/install-skills.ps1
```

仅安装这个技能：

```powershell
./scripts/install-skills.ps1 -SkillName daily-journal
```

### 使用

直接自然语言触发即可，例如：

- “写今日日记”
- “根据这些记录帮我整理一篇日记”

主说明文件：

- `skills/daily-journal/SKILL.md`

参考文件：

- `skills/daily-journal/references/template.md`
- `skills/daily-journal/references/.journal-style.md`
