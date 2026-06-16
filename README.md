# sage_skills

Shared skill library by [Sagecola](https://github.com/Sagecola).

This repository is the source of truth for personal and reusable agent skills.  
Skills are authored once in `skills/` and synced to local runtimes (Codex, Claude Code, Gemini, OpenCode) via scripts.

## Why This Repo

- Share battle-tested skills publicly.
- Keep one canonical definition per skill.
- Sync quickly across machines and AI runtimes.

## Skill Catalog

Current skills are documented in [skills/CATALOG.md](skills/CATALOG.md).

Example:
- `daily-journal`: generate structured daily journal entries from raw life notes, with optional style profile learning and cross-entry references.
- `weekly-journal`: synthesize a week's daily journals into a structured weekly review — distills 流水账/情绪/感恩/成就 into 内容/进展/改进/回顾/成长/思考. Triggered by "帮我写 2026-W01 的周记"; auto-locates daily files and fills or creates the weekly file.
- `monthly-journal`: distill daily journals directly into a month-level note — 本月主线/关键词, work review (保持/问题/尝试/里程碑), life review (生命之轮/高光/所幸/觉察/迁移/本月回看). Treats the monthly note as a map and strategy guide rather than a bigger weekly summary.
- `chinese-typeset-polish`: polish Chinese/mixed-language writing with consistent typesetting rules and minimal semantic edits.
- `obsidian-note`: generate structured Obsidian notes with correct YAML frontmatter for 7 note types — media, book, person, podcast, code, report, and general.
- `daylog`: generate readable daily summaries and diary material from AI coding assistant conversation history (Codex, Claude Code, Kimi Code, opencode) and browser history. Outputs narrative-style work logs or diary drafts.
- `file-organizer`: personal file organization assistant for naming, classifying, and safely archiving messy files into a structured system. Safety-first workflow: inspect, plan, confirm, then act.
- `ammonia-tower-design`: ammonia nitrogen stripping and absorption packed-tower design workflow for wastewater treatment. Includes tower diameter, packing height, packing comparison, wetting/circulation checks, and Onda mass-transfer sizing with HG/T 3986-2016 and HG/T 4374-2012 packing data.

## Repository Layout

```text
skills/
  <skill-name>/
    SKILL.md
    references/   (optional)
    scripts/      (optional)
    assets/       (optional)
scripts/
  install-skills.ps1
  targets.example.json
.claude-plugin/
  marketplace.json
  plugin.json
```

## Quick Start

1. Clone and enter repo.
```powershell
git clone https://github.com/Sagecola/sage_skills.git
cd sage_skills
```

2. Create runtime target config.
```powershell
Copy-Item ./scripts/targets.example.json ./scripts/targets.json
```

3. Dry run first, then install.
```powershell
./scripts/install-skills.ps1 -DryRun
./scripts/install-skills.ps1
```

Install one specific skill:
```powershell
./scripts/install-skills.ps1 -SkillName daily-journal
```

For weekly reviews:
```powershell
./scripts/install-skills.ps1 -SkillName weekly-journal
```

For copywriting/typesetting:
```powershell
./scripts/install-skills.ps1 -SkillName chinese-typeset-polish
```

For Obsidian notes:
```powershell
./scripts/install-skills.ps1 -SkillName obsidian-note
```

For work logging:
```powershell
./scripts/install-skills.ps1 -SkillName daylog
```

For file organization:
```powershell
./scripts/install-skills.ps1 -SkillName file-organizer
```

For engineering calculations:
```powershell
./scripts/install-skills.ps1 -SkillName ammonia-tower-design
```

Install to selected runtimes only:
```powershell
./scripts/install-skills.ps1 -SkillName daily-journal -Tool codex,claude_code
```

## Claude Code Marketplace

This repo now includes Claude marketplace metadata at:
- `.claude-plugin/marketplace.json`
- `.claude-plugin/plugin.json`

Typical install flow:
```text
/plugin marketplace add Sagecola/sage_skills
/plugin install sage-skills@sage-skills
```

## Runtime Targets

Configure local output paths in `scripts/targets.json`:
- `codex` -> `$HOME/.codex/skills`
- `claude_code` -> `$HOME/.claude/skills`
- `gemini` -> `$HOME/.gemini/skills`
- `opencode` -> `$HOME/.opencode/skills`

The installer auto-creates missing target directories.

## Versioning

This repo uses manual versioning for marketplace metadata:
- `.claude-plugin/marketplace.json` -> `metadata.version` and `plugins[].version`
- `.claude-plugin/plugin.json` -> `version`
