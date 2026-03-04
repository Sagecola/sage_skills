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
- `chinese-typeset-polish`: polish Chinese/mixed-language writing with consistent typesetting rules and minimal semantic edits.

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

For copywriting/typesetting:
```powershell
./scripts/install-skills.ps1 -SkillName chinese-typeset-polish
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
