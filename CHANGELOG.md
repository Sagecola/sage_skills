# Changelog

All notable changes to this repository are documented in this file.

The format is based on Keep a Changelog, and this project follows Semantic Versioning.

## [Unreleased]

### Added
- Public-facing repository documentation structure.
- Skill catalog document (`skills/CATALOG.md`).
- Initial release automation script (`scripts/release.ps1`).
- Marketplace metadata file (`marketplace.json`).
- Chinese README (`README.zh.md`) for bilingual docs.
- `skills/daily-journal/README.md` for skill-level usage guidance.
- `skills/daily-journal/references/.journal-style.md` as writing-style profile template and sample format.

### Changed
- `daily-journal` workflow now uses optional style-profile-first analysis and optional cross-entry references.
- Updated repository-level and catalog descriptions for `daily-journal` to match new behavior.
- Fixed emotion tag line format in `skills/daily-journal/references/template.md`.

## [0.4.0] - 2026-03-03

### Features
- $daily-journal: skill updates included in this release

### Documentation
- README updated for release

## [0.3.0] - 2026-03-02

### Features
- $daily-journal: skill updates included in this release
- feat: add personalized writing style learning to diary generation skill

## [0.2.0] - 2026-03-02

### Features
- feat: add release automation and restructure project

### Other
- init sage_skills multi-runtime skill repo
- fix Sagecola link format in README.md

## [0.1.0] - 2026-03-02

### Added
- Initial multi-runtime skill repository scaffold.
- `daily-journal` skill.
- Multi-target installer scripts for Codex, Claude Code, Gemini, and OpenCode.

