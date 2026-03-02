# Skill Catalog

This catalog groups skills by purpose while keeping installation compatible with the current flat `skills/<name>` layout.

## Productivity

### daily-journal
- Path: `skills/daily-journal`
- Summary: Generate structured daily journals from free-form daily notes.
- Primary file: `skills/daily-journal/SKILL.md`
- Typical trigger: "write a daily journal", "生成今日日记"

## Naming Rules

- Skill directory: kebab-case, e.g., `meeting-notes-cleaner`
- Required entry file: `SKILL.md`
- Optional support folders: `references/`, `scripts/`, `assets/`

## Add a New Skill

1. Create `skills/<skill-name>/SKILL.md`.
2. Add references/scripts/assets only when needed.
3. Register the skill in this catalog.
4. Validate with:
   - `./scripts/install-skills.ps1 -SkillName <skill-name> -DryRun`
   - `./scripts/install-skills.ps1 -SkillName <skill-name>`
