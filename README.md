# sage_skills

Personal skill repository for **(Sagecola)[https://github.com/Sagecola]**.

This repo is the single source of truth for custom skills, then synced to local runtimes (Codex, Claude Code, Gemini, OpenCode).

## Repo Structure

- `skills/<skill-name>/SKILL.md`
- Optional per skill: `references/`, `scripts/`, `assets/`
- Multi-runtime installer: `scripts/install-skills.ps1`
- Runtime target template: `scripts/targets.example.json`

Current skills:
- `daily-journal`

## Quick Start

1. Copy target template and edit local paths.

```powershell
Copy-Item ./scripts/targets.example.json ./scripts/targets.json
```

2. Install one skill to all enabled runtimes.

```powershell
./scripts/install-skills.ps1 -SkillName daily-journal
```

3. Install all skills to all enabled runtimes.

```powershell
./scripts/install-skills.ps1 -All
```

4. Install only to selected runtimes.

```powershell
./scripts/install-skills.ps1 -SkillName daily-journal -Tool codex,claude_code
```

## Runtime Targets

`targets.json` controls where skills are synced. You can configure:
- `codex`
- `claude_code`
- `gemini`
- `opencode`

Each runtime path is local and user-defined. Installer will create missing target directories automatically.

## GitHub Sync Workflow

1. Create repo `sage_skills` under `Sgaecola`.
2. Commit and push `main`.
3. Tag releases when needed (`v0.1.0`, `v0.2.0`, ...).
4. On another machine: pull latest, run installer, restart relevant tools.
