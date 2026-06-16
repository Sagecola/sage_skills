# 更新日志

本文件记录此仓库的重要变更。

## 0.8.0 - 2026-06-16

### 新增
- `daylog`：新增从 AI 编程助手对话记录和浏览器历史生成每日摘要和日记素材的技能
- `ammonia-tower-design`：新增氨氮吹脱吸收填料塔工程计算技能，含 Python 计算器、HG/T 国标填料数据和多种水力学模型

## 0.7.0 - 2026-05-22

### 功能
- `obsidian-note`：新增 `references/title-formulas.md`，提供 8 种标题钩子公式与直白风格，并将标题生成工作流从 4 步扩展到 8 步

### 修复
- `monthly-journal`：增加最近月对照流程，并强化栏目权重与 `本月回看` 开头的变化控制，避免退化为时间线叙事

### 文档
- `monthly-journal`：同步更新 `.monthly-style.md` 与模板说明，使其和新的 `本月回看` 偏好保持一致

## 0.6.2 - 2026-05-14

### 修复
- `monthly-journal`：同步更新 `.monthly-style.md`，让 `本月回看` 默认偏好月末判断式开头，同时保留场景式开头作为合理例外

## 0.6.1 - 2026-05-14

### 修复
- `daily-journal`：为 frontmatter 的 `description` 加引号，并恢复可读的 UTF-8 中文模板内容
- `weekly-journal`：为 frontmatter 的 `description` 加引号，并恢复可读的 UTF-8 中文 skill、模板和风格参考内容
- `monthly-journal`：调整 `本月回看` 规则，默认偏好月末判断式开头，同时保留有充分理由的场景式例外
