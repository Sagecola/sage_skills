# 变更日志

本文件记录本仓库的重要变更。

格式参考 Keep a Changelog，版本遵循语义化版本（SemVer）。

## [Unreleased]

### 新增
- 面向公开分享的仓库文档结构。
- 技能目录文档（`skills/CATALOG.md`）。
- 初版发布自动化脚本（`scripts/release.ps1`）。
- marketplace 元数据文件（`marketplace.json`）。
- 中文 README（`README.zh.md`），补齐双语文档。
- `skills/daily-journal/README.md`，补充技能级使用说明。
- `skills/daily-journal/references/.journal-style.md`，作为写作风格档案模板与示例格式。

### 变更
- `daily-journal` 工作流更新为“可选风格档案优先分析 + 可选跨日记关联引用”。
- 同步更新仓库级 README 与技能目录中的 `daily-journal` 描述。
- 修复 `skills/daily-journal/references/template.md` 中情绪标签行格式。

## [0.4.0] - 2026-03-03

### Gong Neng
- $daily-journal: ben ci fa bu bao han gai ji neng geng xin

### Wen Dang
- README wen dang yi tong bu geng xin

## [0.3.0] - 2026-03-02

### 功能
- $daily-journal: ben ci fa bu bao han gai ji neng geng xin
- feat: add personalized writing style learning to diary generation skill

## [0.2.0] - 2026-03-02

### 功能
- feat: add release automation and restructure project

### 其他
- init sage_skills multi-runtime skill repo
- 修正 README.md 中的 Sagecola 链接格式

## [0.1.0] - 2026-03-02

### 新增
- 多运行时技能仓库初始脚手架。
- `daily-journal` 技能。
- 面向 Codex、Claude Code、Gemini、OpenCode 的安装脚本。

