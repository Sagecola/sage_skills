# Obsidian YAML Schema

## Required Fields (fixed order)

All notes must include these fields in this exact order:

```yaml
created: YYYY-MM-DD
modified: YYYY-MM-DD
title: 笔记标题
url:
author:
description:
tags:
  - tag1
slug: kebab-case-title
cover:
```

## Field Behavior

- **created / modified**: Use today's date in ISO format (`YYYY-MM-DD`)
- **slug**: Auto-generate from title as kebab-case English. Examples:
  - `奥本海默` → `oppenheimer`
  - `三体` → `three-body-problem`
  - `Steve Jobs` → `steve-jobs`
  - `深度学习入门` → `intro-to-deep-learning`
- **cover**: Leave empty — user fills manually
- **url**: Leave empty if not provided by user
- **tags**: Use the note type as the first tag (e.g., `影视`, `书籍`, `人际`, etc.)

## Optional Fields by Note Type

Add these fields after `cover`, only when relevant:

| Field      | Type   | Description              | Note Types        |
|------------|--------|--------------------------|-------------------|
| `status`   | string | 在读/已读/未读/在看/已看/未看/进行中 | all types |
| `score`    | number | Rating 1–10              | 影视, 书籍         |
| `country`  | string | 国家/地区                  | 影视               |
| `isbn`     | string | ISBN number              | 书籍               |
| `started`  | date   | Start date (YYYY-MM-DD)  | 影视, 书籍         |
| `finished` | date   | End date (YYYY-MM-DD)    | 影视, 书籍         |
| `birthday` | date   | Birthday (YYYY-MM-DD)    | 人际               |
| `phone`    | string | Phone number             | 人际               |
| `email`    | string | Email address            | 人际               |
| `source`   | string | 来源网站名 (少数派, 知乎…)   | clippings          |

## Naming Rules

- All field names: lowercase English
- Multi-word fields: underscore (`reading_status`, not `readingStatus`)
- No Chinese field names
