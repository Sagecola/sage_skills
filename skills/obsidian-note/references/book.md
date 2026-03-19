# 书籍笔记模板

## YAML 示例

```yaml
created: 2026-03-19T09:22:00+08:00
modified: 2026-03-19T09:22:00+08:00
title: 三体
url:
author: 刘慈欣
description: 中国科幻小说，讲述人类与三体文明的接触与对抗
tags:
  - 书籍
  - 科幻
  - 中国文学
slug: three-body-problem
cover:
status: 已读
score: 10
isbn: 9787536692930
started: 2026-02-01
finished: 2026-03-01
```

## 内容结构

```markdown
## 封面
![三体|350]()

## 基本信息
- **作者**:
- **出版社**:
- **出版年份**:
- **页数**:
- **ISBN**:

## 内容简介

## 核心观点 / 章节笔记

## 金句摘录
> "摘录内容"

## 个人感悟

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

- `author` 字段同时写入 YAML 和正文基本信息
- `isbn` 仅在用户提供时填写，否则留空
- `score` 仅在用户明确给出评分时填写，否则留空
