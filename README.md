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
- `daily-journal`: generate structured daily journal entries from raw life notes.

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
  install-codex-skill.ps1
  release.ps1
  targets.example.json
CHANGELOG.md
CHANGELOG.zh.md
marketplace.json
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
./scripts/install-skills.ps1 -SkillName daily-journal -DryRun
./scripts/install-skills.ps1 -SkillName daily-journal
```

Install all skills:
```powershell
./scripts/install-skills.ps1 -All
```

Install to selected runtimes only:
```powershell
./scripts/install-skills.ps1 -SkillName daily-journal -Tool codex,claude_code
```

## Runtime Targets

Configure local output paths in `scripts/targets.json`:
- `codex` -> `$HOME/.codex/skills`
- `claude_code` -> `$HOME/.claude/skills`
- `gemini` -> `$HOME/.gemini/skills`
- `opencode` -> `$HOME/.opencode/skills`

The installer auto-creates missing target directories.

## Versioning & Changelog

- English changelog: [CHANGELOG.md](CHANGELOG.md)
- Chinese changelog: [CHANGELOG.zh.md](CHANGELOG.zh.md)

Use semantic version tags such as `v0.1.0`, `v0.2.0`.

## Release Workflow

Preview release only:
```powershell
./scripts/release.ps1 -DryRun
```

Execute release (update changelogs + bump marketplace version + commit + tag):
```powershell
./scripts/release.ps1
```

Force bump type:
```powershell
./scripts/release.ps1 -Minor
./scripts/release.ps1 -Patch
./scripts/release.ps1 -Major
```
