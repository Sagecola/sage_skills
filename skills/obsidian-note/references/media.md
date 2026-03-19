# 影视笔记模板

## YAML 示例

```yaml
created: 2026-03-19T09:22:00+08:00
modified: 2026-03-19T09:22:00+08:00
title: 奥本海默
url:
author:
description: 关于原子弹之父奥本海默生平的传记电影
tags:
  - 影视
  - 传记
  - 历史
slug: oppenheimer
cover:
status: 已看
score: 9
country: 美国
started: 2026-01-10
finished: 2026-01-10
```

## 内容结构

```markdown
## 海报
![奥本海默|350]()

## 基本信息
- **播出年份**: [[2023]]
- **导演**:
- **编剧**:
- **主演**:
- **类型**:
- **集数**:

## 简介
《奥本海默》是一部……

## 个人观后感

## 精彩瞬间
> "台词内容" —— 角色名

## 主题与反思

## 相关链接
- [豆瓣页面]()
- [IMDb页面]()

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

- 如果用户只提供了影片名，其余字段留空，让用户自填
- 如果用户提供了详细信息（导演、演员等），直接填入
- `集数` 字段：电影可省略，电视剧必填
- `score` 仅在用户明确给出评分时填写，否则留空
