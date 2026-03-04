# Rules

## Core Rules

1. Add spaces between Chinese and English tokens.
2. Add spaces between Chinese and Arabic numerals.
3. Add spaces between numbers and units.
4. Do not repeat punctuation marks for emphasis.
5. Use fullwidth punctuation in Chinese sentences; keep digits halfwidth.
6. Keep full English sentences with halfwidth punctuation.
7. Use canonical casing for proper nouns (for example: GitHub, TypeScript, Next.js).
8. Avoid non-standard abbreviations (for example: use HTML5, not h5).
9. Keep spaces around inline links in Chinese sentences when readability needs it.
10. Prefer corner quotes in Simplified Chinese: `「...」`, nested `『...』`.

## Examples

### Core Rules Examples

1. Chinese-English spacing  
Correct: `在 LeanCloud 上，数据围绕 AVObject 组织。`  
Wrong: `在LeanCloud上，数据围绕AVObject组织。`

2. Chinese-number spacing  
Correct: `今天花了 5000 元。`  
Wrong: `今天花了5000元。`

3. Number-unit spacing  
Correct: `宽带有 10 Gbps，磁盘有 20 TB。`  
Wrong: `宽带有10Gbps，磁盘有20TB。`

4. No repeated punctuation  
Correct: `德国队竟然赢了！`  
Wrong: `德国队竟然赢了！！！`

5. Fullwidth punctuation in Chinese + halfwidth digits  
Correct: `这个蛋糕只卖 1000 元。`  
Wrong: `这个蛋糕只卖１０００元!`

6. Full English sentence uses halfwidth punctuation  
Correct: `乔布斯说：「Stay hungry, stay foolish.」`  
Wrong: `乔布斯说：「Stay hungry，stay foolish。」`

7. Proper noun casing  
Correct: `使用 GitHub 登录。`  
Wrong: `使用 github 登录。`

8. Avoid non-standard abbreviations  
Correct: `熟悉 TypeScript、HTML5。`  
Wrong: `熟悉 Ts、h5。`

9. Space around inline links in Chinese  
Correct: `请 [提交一个 issue](#) 并分配给同事。`  
Wrong: `请[提交一个 issue](#)并分配给同事。`

10. Corner quotes in Simplified Chinese  
Correct: `「老师，『有条不紊』是什么意思？」`  
Wrong: `“老师，‘有条不紊’是什么意思？”`

## Priority and Exceptions

Apply these with higher priority than general spacing rules:

1. Number + percent: no space, for example `15%`.
2. Number + degree symbol: no space, for example `90°`.
3. Official brand spellings override generic normalization, for example `豆瓣FM`.
4. Existing correct glossary term forms must not be normalized away.

Examples:

- Percent: Correct `性能提升 15%` / Wrong `性能提升 15 %`
- Degree: Correct `角度为 90°` / Wrong `角度为 90 °`
- Official brand form: Correct `豆瓣FM` / Wrong `豆瓣 FM`
- Glossary lock: Correct `Next.js` / Wrong `nextjs`

If rules conflict, follow this order:

1. Immutable constraints
2. Priority exceptions
3. Core mechanical rules
4. Semantic polishing

## Polishing Scope

- Keep original meaning.
- Improve logic flow and sentence clarity.
- Prefer local edits over full rewrites.
- Preserve paragraph structure unless clarity requires minor restructuring.

## Do Not Touch by Default

- Markdown link targets: `(https://...)`
- Code fences and inline code
- CLI commands, API names, identifiers, file paths
- Verbatim citations

## Output Templates

### File Mode

- Edit file content in place.
- In chat, provide concise change summary:
  - spacing and punctuation fixes
  - term/casing fixes
  - semantic polishing highlights

### Dialog Mode

- Return polished text.
- Then return `修改说明` with grouped bullets:
  - `排版规范`
  - `术语与大小写`
  - `表达与逻辑`
