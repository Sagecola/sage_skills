# sage_skills

由 [Sagecola](https://github.com/Sagecola) 维护的可复用技能库。

本仓库是个人与可分享技能的唯一事实来源。  
所有技能统一维护在 `skills/`，通过脚本同步到本地多运行时（Codex、Claude Code、Gemini、OpenCode）。

## 仓库目标

- 对外分享自己长期使用且稳定的技能。
- 每个技能只维护一份标准定义。
- 支持多设备、多运行时快速同步。

## 技能目录

当前技能清单见 [skills/CATALOG.md](skills/CATALOG.md)。

示例：
- `daily-journal`：将零散生活记录整理为结构化日记，并支持写作风格档案与跨日记关联引用。

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
  release.ps1
  targets.example.json
CHANGELOG.md
CHANGELOG.zh.md
marketplace.json
```

## 快速开始

1. 克隆仓库并进入目录。
```powershell
git clone https://github.com/Sagecola/sage_skills.git
cd sage_skills
```

2. 复制并编辑目标运行时配置。
```powershell
Copy-Item ./scripts/targets.example.json ./scripts/targets.json
```

3. 先 dry-run，再安装。
```powershell
./scripts/install-skills.ps1 -DryRun
./scripts/install-skills.ps1
```

安装全部技能：
```powershell
./scripts/install-skills.ps1
```

仅安装到指定运行时：
```powershell
./scripts/install-skills.ps1 -SkillName daily-journal -Tool codex,claude_code
```

## 发布流程

预览发布内容（不改文件）：
```powershell
./scripts/release.ps1 -DryRun
```

执行发布（更新 changelog + 更新 marketplace 版本 + 提交 + 打 tag）：
```powershell
./scripts/release.ps1
```

强制版本类型：
```powershell
./scripts/release.ps1 -Minor
./scripts/release.ps1 -Patch
./scripts/release.ps1 -Major
```

## 版本与变更

- 英文日志：[CHANGELOG.md](CHANGELOG.md)
- 中文日志：[CHANGELOG.zh.md](CHANGELOG.zh.md)
- 市场元数据：[marketplace.json](marketplace.json)
