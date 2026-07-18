---
name: wiz-agent
description: AI-driven disk space analysis and intelligent cleanup for Windows. Use this skill whenever the user wants to check disk usage, find what's taking up space, analyze a drive (C:, D:, etc.), clean up disk space, or asks "why is my disk full". Covers scanning with WizTree, generating space reports, identifying large files and space hogs, and executing safe cleanup commands for developer caches, system temp files, and more.
---

# WizAgent — 磁盘空间分析与智能清理

## 前置依赖

本技能依赖 WizTree CLI 进行磁盘扫描。用户需自行安装 WizTree：
- 下载地址：https://www.diskanalyzer.com/
- 便携版解压后，将目录加入系统 PATH，或在运行脚本时通过 `--wiztree-path` 指定 `WizTree64.exe` 的完整路径
- 管理员权限运行可启用 MFT 快速扫描，速度提升 10 倍以上

## 工作流程

当用户请求分析磁盘空间或清理磁盘时，按以下步骤执行：

### 1. 执行扫描

运行 `scripts/live_analysis.py` 扫描目标路径：

```bash
# 扫描 C 盘（默认）
python skills/wiz-agent/scripts/live_analysis.py

# 扫描指定盘符或目录
python skills/wiz-agent/scripts/live_analysis.py D:
python skills/wiz-agent/scripts/live_analysis.py "C:\Users"

# 指定 WizTree 路径
python skills/wiz-agent/scripts/live_analysis.py --wiztree-path /path/to/WizTree64.exe C:
```

脚本会生成 `live_analysis_report.md` 报告文件。

### 2. 阅读报告

读取生成的报告，重点关注：
- 磁盘容量概况（已用/剩余）
- 直接子项大小排行（定位大户目录）
- 二级子目录排行（深入排查）
- 空间大户分类统计（开发缓存、系统文件等）
- 超大文件排行

### 3. 诊断与建议

根据报告内容：
1. 识别占用空间最大的目录和文件
2. 区分**安全可清理**和**不可动**的内容
3. 参考 `references/cleanup-runbook.md` 中的清理命令，匹配可执行的清理项
4. 向用户汇报分析结果，列出可清理项及预计释放空间

### 4. 执行清理

用户确认后，按 Runbook 中的命令执行安全清理。清理前务必：
- 确认目标路径正确，不要误删重要数据
- 开发者缓存（npm/pip/bun）可安全清除，重建即可
- 系统级操作（Windows Update 缓存、WSL）需管理员权限，提前告知用户
- 每项清理操作单独执行，不要批量运行

## 安全原则

- **先扫后清**：永远先运行扫描、阅读报告，再决定清理什么
- **用户确认**：每项清理操作执行前需用户明确同意
- **保守优先**：不确定的内容宁可不动，不清理系统关键文件
- **最小权限**：非管理员能完成的操作不提权，需要管理员权限时明确说明
