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
- `weekly-journal`：将一周的日记蒸馏为结构化周记，自动提炼流水账/情绪/感恩/成就为内容/进展/改进/回顾/成长/思考。说"帮我写 2026-W01 的周记"即可触发，自动定位日记文件并填充或新建周记。
- `monthly-journal`：将日记直接蒸馏为月记，包含本月主线/关键词、工作复盘（保持/问题/尝试/里程碑）、生活回顾（生命之轮/高光/所幸/觉察/迁移/本月回看）。月记是地图与战略指南，不是更长的周记。
- `chinese-typeset-polish`：按中文与中英混排规范进行排版优化，并做最小化润色。
- `obsidian-note`：生成带有规范 YAML frontmatter 的 Obsidian 笔记，支持影视、书籍、人际、播客、代码、报告、通用共 7 种笔记类型。
- `daylog`：从 AI 编程助手对话记录（Codex、Claude Code、Kimi Code、opencode）和浏览器历史生成可读的每日摘要和日记素材。输出叙事风格的工作日志或日记草稿。
- `file-organizer`：个人文件整理助手，帮助命名、分类并安全归档杂乱文件到「人生档案馆」系统。安全优先的工作流：先看后动，确认再操作。
- `ammonia-tower-design`：氨氮废水两段式吹脱+吸收填料塔工程计算。包含塔径、填料高度、填料对比、润湿/循环校核、Onda 传质计算，内置 HG/T 3986-2016 和 HG/T 4374-2012 填料数据。

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

安装周记技能：
```powershell
./scripts/install-skills.ps1 -SkillName weekly-journal
```

安装排版润色技能：
```powershell
./scripts/install-skills.ps1 -SkillName chinese-typeset-polish
```

安装 Obsidian 笔记技能：
```powershell
./scripts/install-skills.ps1 -SkillName obsidian-note
```

安装工作日志技能：
```powershell
./scripts/install-skills.ps1 -SkillName daylog
```

安装文件整理技能：
```powershell
./scripts/install-skills.ps1 -SkillName file-organizer
```

安装工程计算技能：
```powershell
./scripts/install-skills.ps1 -SkillName ammonia-tower-design
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
