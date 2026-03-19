# sage_skills

由 [Sagecola](https://github.com/Sagecola) 维护的可复用技能库。

本仓库是个人与可共享技能的唯一事实来源。  
所有技能统一维护在 `skills/`，通过脚本同步到本地多运行时（Codex、Claude Code、Gemini、OpenCode）。

## 仓库目标

- 对外分享长期稳定可复用的技能。
- 每个技能只维护一份标准定义。
- 支持多设备、多运行时快速同步。

## 技能目录

当前技能清单见 [skills/CATALOG.md](skills/CATALOG.md)。

示例：
- `daily-journal`：将零散生活记录整理为结构化日记，支持写作风格档案与跨日期引用。
- `chinese-typeset-polish`：按中文与中英混排规范进行排版优化，并做最小化润色。
- `obsidian-note`：生成带有规范 YAML frontmatter 的 Obsidian 笔记，支持影视、书籍、人际、播客、代码、报告、通用共 7 种笔记类型。

## 目录结构

```text
skills/
  <skill-name>/
    SKILL.md
    references/   (可选)
    scripts/      (可选)
    assets/       (可选)
scripts/
  install-skills.ps1
  targets.example.json
.claude-plugin/
  marketplace.json
  plugin.json
```

## 快速开始

1. 克隆仓库并进入目录。
```powershell
git clone https://github.com/Sagecola/sage_skills.git
cd sage_skills
```

2. 创建运行时目标配置。
```powershell
Copy-Item ./scripts/targets.example.json ./scripts/targets.json
```

3. 先 DryRun，再正式安装。
```powershell
./scripts/install-skills.ps1 -DryRun
./scripts/install-skills.ps1
```

安装单个技能：
```powershell
./scripts/install-skills.ps1 -SkillName daily-journal
```

安装排版润色技能：
```powershell
./scripts/install-skills.ps1 -SkillName chinese-typeset-polish
```

安装 Obsidian 笔记技能：
```powershell
./scripts/install-skills.ps1 -SkillName obsidian-note
```

仅安装到指定运行时：
```powershell
./scripts/install-skills.ps1 -SkillName daily-journal -Tool codex,claude_code
```

## Claude Code Marketplace 安装

本仓库已提供 Claude marketplace 元数据：
- `.claude-plugin/marketplace.json`
- `.claude-plugin/plugin.json`

可在 Claude Code 中执行：

```text
/plugin marketplace add Sagecola/sage_skills
/plugin install sage-skills@sage-skills
```

## 运行时目标

在 `scripts/targets.json` 配置输出路径：
- `codex` -> `$HOME/.codex/skills`
- `claude_code` -> `$HOME/.claude/skills`
- `gemini` -> `$HOME/.gemini/skills`
- `opencode` -> `$HOME/.opencode/skills`

安装脚本会自动创建不存在的目录。

## 版本管理

本仓库对 marketplace 元数据使用手工版本管理：
- `.claude-plugin/marketplace.json` -> `metadata.version` 与 `plugins[].version`
- `.claude-plugin/plugin.json` -> `version`
