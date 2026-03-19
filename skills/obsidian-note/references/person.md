# 人际笔记模板

## YAML 示例

```yaml
created: 2026-03-19T09:22:00+08:00
modified: 2026-03-19T09:22:00+08:00
title: 张三
url:
author:
description: 同事，技术部工程师
tags:
  - 人际
  - 同事
slug: zhang-san
cover:
birthday: 1990-06-15
phone:
email:
```

## 内容结构

```markdown
## 基本信息
- **姓名:**
- **性别:**
- **年龄:**
- **联系方式:**
- **婚姻状况:**
- **家乡:**
- **居住地/暂住地:**

## 背景
### 家庭情况

### 教育经历

### 职业经历

## 性格与爱好
### 性格特点

### 爱好专长

## 相关人

## 互动记录
### 第一印象

### 共同话题

### 交往轨迹

### 礼尚往来

## 备注

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

- `title` 直接用人名
- `slug` 用拼音或英文名转 kebab-case（如 `zhang-san`、`john-doe`）
- `phone`、`email`、`birthday` 仅在用户提供时填写，否则留空
- `description` 简短描述关系（如"大学同学"、"前同事"）
