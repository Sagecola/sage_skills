---
name: daylog
description: |
  Generate readable daily summaries from local AI coding assistant conversation history and browser history. Triggers on: "查 AI 对话记录", "整理工作日志", "总结每天和 AI 干了什么", "上周用 AI 做了啥", "帮我看看我最近和 AI 聊了啥", "summarize my coding sessions", "generate work log", "what did I work on with AI", "写日记", "回忆今天干了什么", "帮我写日记素材", "diary material", or any request to review, summarize, or report on daily activities. Also triggers when migrating this workflow to another computer.
---

# Daylog

帮用户回忆：这段时间用了哪些 AI 工具、每天聊了什么、做了什么事。

核心流程：**脚本提取原始数据 → 你阅读分析 → 你写出叙事性摘要**。脚本只负责提取，真正的总结是你来写的。

## 支持的工具

| 工具 | Windows 默认路径 |
|------|-----------------|
| Codex | `%USERPROFILE%\.codex\sessions` |
| Claude Code | `%USERPROFILE%\.claude\projects` |
| Kimi Code CLI | `%USERPROFILE%\.kimi\sessions` |
| opencode | `%USERPROFILE%\.local\share\opencode\opencode.db` |

补充检查路径（有需要时）：`%APPDATA%\opencode`、`%LOCALAPPDATA%\opencode`

## 安全规则

原始历史文件不可替代，严格只读 —— 不得编辑、移动、删除、压缩 `.codex`、`.claude`、`.kimi`、`.opencode` 或 opencode 数据库。生成的索引和报告只写到用户指定的输出目录。

日期默认按北京时间（`Asia/Shanghai`，UTC+8）分组。

---

## 工作流：生成工作日志

### 第一步：提取原始对话

确认日期范围（默认当天所在周或用户指定），然后运行提取脚本：

```powershell
python scripts\extract_ai_logs.py --start YYYY-MM-DD --end YYYY-MM-DD --out ai-log-index.json
python scripts\generate_worklog.py --index ai-log-index.json --out ai-worklog.md
```

如果是从另一台电脑拷贝的备份（迁移场景），加 `--source-root` 参数：
```powershell
python scripts\extract_ai_logs.py --start YYYY-MM-DD --end YYYY-MM-DD --source-root D:\AI聊天记录导出 --out ai-log-index.json
```

备份目录结构应为：
```
backup-root/
  codex/sessions/
  claude/projects/
  kimi/sessions/
  opencode/opencode.db
```

### 第二步：阅读并写出摘要

脚本生成的 `ai-worklog.md` 是原始提取结果，内容比较杂。**你需要阅读这份文件，然后重新写出一份干净的摘要**，这才是用户真正想要的东西。

好的摘要长这样：

```
## 2026-05-26

**Claude Code** — 填料塔设计 skill 开发
- 对比了 Blackwell 和 Kister GPDC 两种泛点计算模型，选用 Kister 方案
- 加入国产散堆填料数据（HG/T 3986-2016），与外国数据偏差 < 5%
- 脚本拆分为压降模块和泛点模块两个独立文件

**Kimi Code** — 填料塔压降模型调研
- 从 PDF 文献中提取 Kessler & Wankat 数学模型，用 Python 实现
- 对比了 Billet-Schultes 模型的适用填料范围
```

写摘要的原则：
- 每天一个 `## YYYY-MM-DD` 段落
- 每个工具单独一个小标题（**Claude Code**、**Kimi Code** 等）
- 每条 bullet 说清楚：做了什么事、结论是什么、有没有产出文件
- 跳过噪音：系统消息、工具调用细节、续接上下文、`/model` 命令
- 用中文写（除非用户用英文问）

### 第三步：告知结果

回复用户时说明：
- 找到了哪些工具的记录，各有几个会话
- 哪些工具没有找到记录（比如 opencode 未安装）
- 生成的报告保存在哪里

---

## 工作流：生成日记素材稿

当用户需要写日记或回忆某天的生活时，使用此流程。**最终输出是一份叙事性的素材稿，由 AI 阅读原始数据后生成，不是脚本直接拼接的列表。**

### 第一步：提取原始数据

同时运行两个脚本，生成 AI 对话索引和浏览器时间线：

```powershell
# 1. 提取 AI 对话记录
python scripts\extract_ai_logs.py --start YYYY-MM-DD --end YYYY-MM-DD --out ai-log-index.json

# 2. 清洗浏览器历史
python scripts\process_history.py -i <BrowserHistory.csv 路径> --start YYYY-MM-DD --end YYYY-MM-DD
```

产出文件（默认在当前工作目录）：
- `ai-log-index.json` — AI 对话结构化索引
- `timeline_YYYY-MM-DD.md` — 每天的浏览器活动时间线

### 第二步：阅读两份数据，生成叙事性素材稿

**这是核心步骤。你必须先阅读两份原始数据，理解用户那天干了什么，然后写出叙事性素材稿。**

不要直接把浏览器记录拼接成列表输出。要像写日记一样，用自然语言描述用户那天的活动：

1. **先读 `ai-log-index.json`**，理解用户和 AI 聊了什么、做了什么项目
2. **再读 `timeline_YYYY-MM-DD.md`**，理解用户浏览了什么网站、看了什么内容
3. **交叉分析**：AI 对话中提到的操作可能对应浏览器中的某些页面；浏览器中的搜索可能对应 AI 对话中的某个任务
4. **写出叙事稿**：按时间线，用自然语言描述用户一天的活动

### 输出格式

每天一个 `## YYYY-MM-DD` 段落，按时间线用自然语言描述：

```markdown
## 2026-03-10

早上到公司后先刷了一会儿少数派，看了几篇文章，包括一篇关于 AI 帮助建数字人生档案馆的征文，还有派早报和派评。之后在起点中文网追了《没钱修什么仙》第828章。

上午主要在 GitHub 上折腾博客。先是看了一个叫 Happy 的 Claude Code 移动端项目，然后配置自己 quartz 博客的 GitHub Actions，创建和管理了好几个 Token。中间还搜了一下 Obsidian 的 skills 插件，下载试了一下。

下午在腾讯云上操作了一阵子，开了个 OrcaTerm 终端。之后又去少数派看了几篇文章，刷了会儿虎扑步行街，看了两个帖子——一个讨论体制内微信礼仪，一个聊为了美食去哪座城市。

傍晚用了一会儿 ChatGPT 和 Codex，然后在知乎看了一篇 Claude 官方 Skill-Creator 的深度分析文章，顺手去 GitHub 上 anthropics/skills 仓库看了一下。
```

写素材稿的原则：
- 用**自然语言叙事**，不是列表拼接
- 描述用户做了什么，但**不编造感受**——感受留给用户自己写
- 把相关活动串联起来（比如"在 GitHub 上折腾博客"把多个 GitHub 操作归纳为一件事）
- 跳过无意义的操作（反复刷新同一页面、登录页等）
- 如果 AI 对话和浏览器记录有交叉（比如 AI 里聊了某个工具，浏览器里也搜了），合并描述
- 用中文写

### 第三步：告知结果

回复用户时说明：
- 生成了哪些天的素材稿
- 覆盖了哪些数据源（AI 对话 / 浏览器历史）
- 输出文件在哪里

---

## 浏览器历史记录（数据源说明）

### 数据来源

浏览器历史 CSV 文件（Chrome/Edge 导出），需由用户指定路径，例如：`--input C:\Users\<用户名>\Desktop\History\BrowserHistory.csv`

### 处理脚本

`scripts/process_history.py` 负责清洗和分类：
- 过滤噪音（搜索中间页、Chrome内部页面、认证回调等）
- 按域名自动分类（视频/社交/购物/AI/开发/阅读等）
- 同一分钟同标题去重
- 输出 `timeline_YYYY-MM-DD.md`（紧凑时间线）和 `history_YYYY-MM-DD.md`（完整分类报告）

### 分类说明

| 类别 | emoji | 包含网站 |
|------|-------|----------|
| dev | 💻 | GitHub, GitLab, StackOverflow |
| ai | 🤖 | Claude, ChatGPT, Gemini, 智谱, Kimi, Cursor |
| reading | 📖 | 少数派, 掘金, CSDN, Medium, Notion |
| video | 🎬 | B站, YouTube, Netflix, Disney+ |
| social | 💬 | 小红书, Twitter, 虎扑, 知乎, 微博 |
| shopping | 🛒 | 淘宝, 京东, 拼多多 |
| music | 🎵 | 网易云, Spotify, Apple Music |
| food | 🐦 | 大众点评, 美团, 饿了么 |
| tool | 🔧 | Figma, Canva, Excalidraw |
| other | 🌐 | 未归类网站 |

可在 `process_history.py` 的 `DOMAIN_RULES` 和 `generate_diary_material.py` 的 `EXTRA_CN` 中添加更多规则。

---

## 解析说明（遇到问题时参考）

- **Codex**：JSONL 文件，按 年/月/日 目录存放
- **Claude Code**：`.claude/projects` 下的 JSONL 文件，跳过 `subagents/` 和 `tool-results/` 子目录
- **Kimi Code CLI**：`~/.kimi/sessions/<hash>/<uuid>/wire.jsonl`，`TurnBegin` = 用户发言，`ContentPart` = AI 回复，`ToolCall` = 执行的命令
- **opencode**：SQLite 数据库，`message` 表 join `part` 表，文本在 `part.data` 的 `type=text` 记录里
- 日期分组用消息时间戳（转换为北京时间），不用文件名
- 跨午夜的会话：按第一条用户可见消息归到当天
- **浏览器历史**：CSV 格式（DateTime, NavigatedToUrl, PageTitle），UTC 时间自动转北京时间
