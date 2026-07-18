# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

A shared skill library for AI coding assistants. Skills are Markdown-defined agent instructions (SKILL.md) synced to local runtimes (Claude Code, Codex, Gemini, OpenCode) via a PowerShell installer. The repo also ships Python scripts for two skills: ammonia-tower-design (engineering calculator) and wiz-agent (disk space analyzer).

## Common Commands

```powershell
# Install all skills to all configured runtimes
./scripts/install-skills.ps1 -All

# Install one skill (safe default: dry run first)
./scripts/install-skills.ps1 -SkillName daily-journal -DryRun
./scripts/install-skills.ps1 -SkillName daily-journal

# Install to specific runtimes only
./scripts/install-skills.ps1 -SkillName daily-journal -Tool codex,claude_code

# Ammonia tower calculator (run from repo root)
cd skills/ammonia-tower-design
python -m scripts.calculate_two_stage_ammonia_towers --preset hanglian
python -m scripts.calculate_two_stage_ammonia_towers --preset hanglian --flooding-method mackowiak
```

There is no compile step, no linter, and no test framework. Validate changes by running `install-skills.ps1 -DryRun` and then installing to confirm files appear in target paths.

## Architecture

```
skills/
  <skill-name>/
    SKILL.md           # Primary skill spec (required, uppercase)
    references/        # Domain docs, style guides, schemas
    scripts/           # Python calculators (ammonia-tower-design, daylog, wiz-agent)
    assets/            # Templates, presets
scripts/
  install-skills.ps1   # Multi-runtime installer (main entry point)
  targets.example.json # Template for runtime output paths
.claude-plugin/
  plugin.json          # Marketplace metadata (name, version)
  marketplace.json     # Claude marketplace listing
```

## Adding a New Skill

1. Create `skills/<skill-name>/SKILL.md` — this is the required entry point.
2. Add `references/`, `scripts/`, or `assets/` subfolders only when needed.
3. Register in `skills/CATALOG.md`.
4. Validate: `./scripts/install-skills.ps1 -SkillName <skill-name> -DryRun`

Skill directories use kebab-case. The SKILL.md file must be uppercase. Keep skills self-contained.

## Key Conventions

- UTF-8 Markdown and PowerShell throughout.
- 4-space indentation in `.ps1` files.
- Scripts must be idempotent — re-running safely overwrites target skill folders.
- Commit messages: short, imperative, often in Chinese (e.g., `修正 README.md 中的 Sagecola 链接格式`).
- Version bumps go in `.claude-plugin/plugin.json` (`version`) and `.claude-plugin/marketplace.json` (`metadata.version` + `plugins[].version`).

## ammonia-tower-design Python Scripts

The `skills/ammonia-tower-design/scripts/` directory contains the calculator. Key modules:
- `calculate_two_stage_ammonia_towers.py` — CLI entry point
- `flooding_models.py` — Blackwell, Kister GPDC, Mackowiak SBD, Billet-Schultes
- `pressure_drop_models.py` — pressure drop correlations
- `packing_data.py` — HG/T 3986-2016 and HG/T 4374-2012 packing database
- `report_formatter.py` — text/Markdown output

Do not edit these scripts unless the user explicitly asks. If a new calculator is needed, create a new script.

## wiz-agent Skill

The `skills/wiz-agent/` directory contains a disk space analysis and cleanup skill for Windows. Key files:
- `scripts/live_analysis.py` — WizTree wrapper that scans drives and generates Markdown reports
- `references/cleanup-runbook.md` — safe cleanup command recipes (dev caches, system temp, WSL, etc.)

Requires WizTree CLI installed separately by the user. The script locates it via PATH or `--wiztree-path` argument.
