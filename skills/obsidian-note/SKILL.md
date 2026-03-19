---
name: obsidian-note
description: >
  Generate structured Obsidian notes with correct YAML frontmatter and content
  sections, following the user's personal conventions. Use this skill whenever
  the user wants to create an Obsidian note, build a note template, or document
  something in their vault — including movies, TV shows, books, people, podcasts,
  code snippets, experiment reports, or general notes. Trigger on phrases like
  "帮我写一篇笔记", "新建一个 Obsidian 笔记", "创建影视笔记", "书籍笔记", "人际档案",
  "记录这期播客", "obsidian note", "写个实验报告", "代码笔记", or any request to
  document content in Obsidian format.
---

# Obsidian Note Generator

Generate complete Obsidian notes with YAML frontmatter and structured content sections.

## Step 1 — Identify Note Type

Determine the note type from the user's request:

| Type     | Keywords / Signals                              |
|----------|-------------------------------------------------|
| `media`  | 电影、电视剧、综艺、剧、片、影视、番               |
| `book`   | 书、书籍、读书、小说、阅读                         |
| `person` | 人名、认识某人、人际、联系人、档案                  |
| `podcast`| 播客、podcast、节目、期                           |
| `code`   | 代码、脚本、函数、python、js、bash 等              |
| `report` | 实验报告、报告、实验                               |
| `default`| 未指定类型，或不属于以上任何类型                    |

If the type is ambiguous, ask the user before proceeding.

## Step 2 — Read the Reference Template

Read the corresponding reference file for the identified type:

- `media` → `references/media.md`
- `book` → `references/book.md`
- `person` → `references/person.md`
- `podcast` → `references/podcast.md`
- `code` → `references/code.md`
- `report` → `references/report.md`
- `default` → `references/default.md`

Also read `references/yaml-schema.md` for the full YAML field rules.

## Step 3 — Generate the Note

### YAML Frontmatter Rules

Follow the required field order from `yaml-schema.md`:
`created → modified → title → url → author → description → tags → slug → cover`

Then append any relevant optional fields for the note type.

Key behaviors:
- **created / modified**: today's date in `YYYY-MM-DD` format
- **slug**: auto-generate from the title as kebab-case English
  - Chinese titles: transliterate or translate meaningfully (`深度学习` → `deep-learning`, `奥本海默` → `oppenheimer`)
  - English titles: lowercase and hyphenate (`Steve Jobs` → `steve-jobs`)
- **cover**: always leave empty
- **url**: leave empty unless the user provides a link
- Only include optional fields that are relevant to the note type — don't add unused fields

### Content

Use the content structure from the reference file. Fill in whatever information the user has provided; leave other fields blank for the user to complete later.

Do not invent facts (cast, plot, author, etc.) unless the user provided them or they are universally well-known and unambiguous (e.g., director of a famous film). When in doubt, leave the field blank.

## Step 4 — Output

Output the complete note as a Markdown code block so the user can copy it directly into Obsidian.

If the user asks to save the note to their vault directly, use the `obsidian-cli` skill if available.

## Examples

**Request**: "帮我写一篇《请回答1988》的影视笔记"
→ type: `media`, read `references/media.md`, generate with title=请回答1988, slug=reply-1988, tags=[影视, 韩剧], country=韩国

**Request**: "新建一个书籍笔记，《原则》，作者瑞·达利欧"
→ type: `book`, read `references/book.md`, generate with title=原则, author=瑞·达利欧, slug=principles

**Request**: "为李明创建一个人际档案，他是我大学同学"
→ type: `person`, read `references/person.md`, generate with title=李明, slug=li-ming, description=大学同学

**Request**: "记录一下这期播客，硬地骇客 EP.88，聊的是睡眠"
→ type: `podcast`, read `references/podcast.md`, generate with title=硬地骇客 EP.88 睡眠管理
