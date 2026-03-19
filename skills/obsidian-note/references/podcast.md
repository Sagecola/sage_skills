# 播客笔记模板

## YAML 示例

```yaml
created: 2026-03-19
modified: 2026-03-19
title: 硬地骇客 EP.123 如何建立第二大脑
url: https://example.com/episode-123
author: 硬地骇客
description: 讨论个人知识管理系统和第二大脑构建方法
tags:
  - 播客
  - 知识管理
  - 效率
slug: hard-core-hacker-ep123-second-brain
cover:
status: 已听
```

## 内容结构

```markdown
## 播客信息
- **播客名称**: [[]]
- **期数/标题**:
- **发布日期**:
- **主持人/嘉宾**:

## 封面图片
![播客封面]()

## 内容摘要

## 个人笔记
- **心得体会**:
- **学到的知识**:
- **行动计划**:

## 链接和资源

## One more thing—记录
```dataviewjs
dv.table(["日期", "行为"], dv.pages('#日记')
.sort(p => p.file.name,"desc")
.where(p => p.file.outlinks.includes(dv.current().file.link))
.file
.map(b=> [b.link, b.lists
                   .where(a => String(a.outlinks)
                   .contains(dv.current().file.name)).text]))
` ``
```

## 填写说明

- `title` 建议格式：`播客名 EP.xxx 期数标题`
- `author` 填播客节目名称
- `url` 如果用户提供了链接则填入
- `播客名称` 正文中用 `[[]]` 双链关联播客主页笔记
