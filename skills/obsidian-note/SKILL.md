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

## Step 2 — Pre-process Source Content (Optional)

When the user provides raw text content to include in the note, and the note type is `default` (no structured template), check if the content needs formatting:

- If the content is well-structured → skip to Step 3
- If the content is messy (no headings, walls of text, no lists where lists should be) → use `baoyu-format-markdown` to format it first

**Important**: Even after `baoyu-format-markdown` processing, the YAML frontmatter MUST follow `obsidian-note`'s schema (`references/yaml-schema.md`), not baoyu's frontmatter format. Only the body content formatting is borrowed.

For structured template types (`media`, `book`, `person`, `podcast`, `code`, `report`), skip this step — those templates have their own content structure.

## Step 3 — Read the Reference Template

Read the corresponding reference file for the identified type:

- `media` → `references/media.md`
- `book` → `references/book.md`
- `person` → `references/person.md`
- `podcast` → `references/podcast.md`
- `code` → `references/code.md`
- `report` → `references/report.md`
- `default` → `references/default.md`

Also read `references/yaml-schema.md` for the full YAML field rules.

## Step 4 — Generate Title

Read `references/title-formulas.md` for the title formula reference.

Extract from the content:
- Core argument (what is this note about?)
- Most impactful opinion or conclusion
- Reader pain point or curiosity trigger
- Most memorable metaphor or golden quote

Generate **4-5 title candidates**:
1. Select **2-3 hook formulas** that best match the content (see "When to pick each formula" in the reference)
2. Generate **1-2 straightforward titles** (descriptive or declarative)

**Pick the best candidate as the note title** (use the strongest hook formula). Place the remaining candidates in the note body under a section called `## 备选标题` so the user can manually swap if preferred.

**Skip behavior**: If the user already provided a clear title, use it directly and skip candidate generation. Do not generate `## 备选标题` section in that case.

## Step 5 — Generate the Note

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

## Step 6 — Output

Output the complete note as a Markdown code block so the user can copy it directly into Obsidian.

If the user asks to save the note to their vault directly, use the `obsidian-cli` skill if available.

## Step 7 — Post-Processing

After the note is generated, run `chinese-typeset-polish` on the note body (not the YAML frontmatter) by default.

**Do not** run `chinese-typeset-polish` on the YAML frontmatter block — only on the Markdown body content.

Skip this step only if the user explicitly says "不需要润色", "不用排版", or similar.

## Step 8 — Completion Report

Output a brief summary in chat (do not save as a file):

```
笔记已生成

- 类型: {note type}
- 标题: {title}
- Slug: {slug}
- 包含字段: {list of YAML fields filled}
- 后处理: {排版润色 / 无}
```

## Examples

**Request**: "帮我写一篇《请回答1988》的影视笔记"
→ type: `media`, read `references/media.md`, generate with title=请回答1988, slug=reply-1988, tags=[影视, 韩剧], country=韩国

**Request**: "新建一个书籍笔记，《原则》，作者瑞·达利欧"
→ type: `book`, read `references/book.md`, generate with title=原则, author=瑞·达利欧, slug=principles

**Request**: "为李明创建一个人际档案，他是我大学同学"
→ type: `person`, read `references/person.md`, generate with title=李明, slug=li-ming, description=大学同学

**Request**: "记录一下这期播客，硬地骇客 EP.88，聊的是睡眠"
→ type: `podcast`, read `references/podcast.md`, generate with title=硬地骇客 EP.88 睡眠管理
