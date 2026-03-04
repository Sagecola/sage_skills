# Repository Guidelines

## Project Structure & Module Organization
This repository stores reusable agent skills and sync scripts.

- `skills/<skill-name>/SKILL.md`: each skill’s primary specification.
- Optional skill subfolders: `references/`, `scripts/`, `assets/`.
- Do not add per-skill `README.md`; keep skill instructions in `SKILL.md` and supporting details in `references/`.
- `scripts/install-skills.ps1`: main multi-runtime installer.
- `scripts/targets.example.json`: template for runtime target paths.

Keep each skill self-contained under its own folder (for example, `skills/daily-journal/`).

## Build, Test, and Development Commands
This repo has no compile step; use PowerShell scripts for validation and installation.

```powershell
Copy-Item ./scripts/targets.example.json ./scripts/targets.json
./scripts/install-skills.ps1
./scripts/install-skills.ps1 -All
./scripts/install-skills.ps1 -SkillName daily-journal -Tool codex,claude_code -DryRun
```

- `-DryRun` is the safest default during development.
- Use `-ConfigPath` to test alternate target configs without changing committed files.

## Coding Style & Naming Conventions
- Use UTF-8 Markdown and PowerShell.
- Prefer 4-space indentation in `.ps1` and stable, explicit parameter names.
- Skill directories use kebab-case (for example, `daily-journal`).
- Required skill entry file is uppercase `SKILL.md`.
- Keep scripts idempotent: re-running should safely overwrite target skill folders.

## Testing Guidelines
There is currently no formal test framework. Validate changes with:

1. Script syntax check by running target commands in `-DryRun` mode.
2. Functional check by installing one skill and confirming files appear in configured target paths.
3. Regression check by installing `-All` after adding or renaming skills.

When adding complex script logic, include a repeatable verification snippet in the PR description.

## Commit & Pull Request Guidelines
Current history uses short, imperative commit messages (including Chinese), e.g., `修正 README.md 中的 Sagecola 链接格式`.

- Keep subject lines concise and action-oriented.
- Commit one logical change per commit.
- PRs should include: purpose, changed paths, sample command(s) run, and before/after behavior.
- Link related issues/tasks when available.
- For README or skill UX changes, include a short usage example.
