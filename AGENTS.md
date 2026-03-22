# AGENTS.md

Agent guide for `D:\DayZProjects\docs\wiki`.

## What This Repo Is
- 12-language DayZ modding wiki built with VitePress
- Main content is Markdown; primary code file is `.vitepress/config.mts`
- English in `en/` is the source of truth
- Other locale folders mirror the English tree exactly
- CI builds and deploys GitHub Pages from `.vitepress/dist`

## Rule Files
- `AGENTS.md`: this file
- `CLAUDE.md`: repository-specific guidance in the repo root
- Cursor rules: none found (`.cursor/rules/` absent, `.cursorrules` absent)
- Copilot rules: none found (`.github/copilot-instructions.md` absent)

If new Cursor or Copilot rule files are added later, follow them too.

## Tooling Snapshot
- Package manager: `npm`
- Lockfile: `package-lock.json`
- CI Node version: 22
- Key dependencies: `vitepress`, `vitepress-plugin-mermaid`, `mermaid`

## Commands
### Install dependencies
```bash
npm ci
```
Use `npm ci` for reproducible installs.
### Start local dev server
```bash
npm run dev
```
Starts VitePress with hot reload.
### Build static site
```bash
npm run build
```
Primary verification command.
Latest verified local result in this environment: VitePress began building successfully, then Node crashed with JavaScript heap out of memory. Do not claim builds pass unless you re-run and confirm a zero exit code.
### Preview built site
```bash
npm run preview
```
Requires a successful build first.

## Lint And Test Status
- No `lint` script exists in `package.json`
- No `test` script exists in `package.json`
- No ESLint config found
- No Prettier config found
- No markdownlint config found
- No Jest, Vitest, Mocha, or other automated test runner found
Do not invent extra tooling unless the user asks.

## Running A Single Test
There is no automated test framework here, so there is no single-test command.
Use the smallest relevant validation instead:
1. Content-only change: run `npm run dev` and inspect the changed page.
2. Link or sidebar change: run `npm run build` and read the failing output carefully.
3. `.vitepress/config.mts` change: verify the affected route in dev, then run `npm run build`.
4. Translation-only change: compare against the matching English page and nearby translations.

## Common Files Agents Edit
- `README.md`
- `CONTRIBUTING.md`
- `.vitepress/config.mts`
- Locale docs under `en/`, `pt/`, `de/`, `ru/`, `es/`, `fr/`, `ja/`, `zh-hans/`, `cs/`, `pl/`, `hu/`, `it/`
- Reference docs like `cheatsheet.md`, `glossary.md`, `faq.md`, `troubleshooting.md`
## Repository Structure
- Chapter folders use numbered sections such as `01-enforce-script/` and `08-tutorials/`
- File naming convention:
```text
<part-number>-<section-name>/<sequence-number>-<topic-slug>.md
```
- Examples:
  - `en/01-enforce-script/01-variables-types.md`
  - `pt/08-tutorials/01-first-mod.md`

## Markdown And Content Style
- Use ATX headings only: `#`, `##`, `###`
- Keep exactly one `#` heading per file
- Use `---` between major sections
- Prefer relative links for internal links
- Use ordered lists for sequences and `-` bullets for non-sequential items
- Use tables for structured references when they help readability
- Write in second person when instructing the reader
- Use present tense
- Prefer plain English unless DayZ-specific terms are required

## Typical Chapter Shape
```markdown
# Chapter X.Y: Title
> **Summary:** One or two sentences.
---
## Table of Contents
---
## Section
---
**Previous:** [link] | [Home](../../README.md) | **Next:** [link]
```
Some older pages use a top navigation line instead. Match the surrounding file unless the task includes cleanup.
## Code Style For `.mts` And Embedded Examples

### Imports
- Keep imports at the top of the file
- Use straightforward named imports
- Match the existing quote and semicolon style of the file you edit
- Do not add helper layers unless they materially simplify the file

### Formatting
- Follow the existing file style; there is no formatter enforcing a different one
- Keep arrays and objects readable in `.vitepress/config.mts`
- Avoid whitespace-only churn
- Do not reflow Markdown tables carelessly

### Types And Abstractions
- Preserve existing TypeScript patterns
- Prefer simple explicit structures over clever abstractions
- Do not add type-heavy helpers unless clearly justified

### Naming
- Match naming already used in the file
- Config helpers use `camelCase` like `sidebarEN`
- Constants in examples may use `UPPER_SNAKE_CASE`
- Markdown filenames use numeric prefixes and kebab-case slugs
- Keep terminology consistent with existing chapter titles

### Error Handling
- For docs, "error handling" mostly means avoiding broken links, anchors, and navigation
- For config changes, prefer explicit simple logic over indirection
- Report actual command failures instead of guessing
- Do not claim success without fresh command output
## Translation Rules
- Translate prose, headings, link labels, and code comments
- Do not translate code keywords, class names, method names, file names, or config syntax
- Keep links pointing at the correct locale directory
- Preserve parity with the English source unless the user explicitly wants divergence

## When Adding Or Renaming Chapters
Update all affected navigation surfaces together:
1. Root `README.md`
2. Relevant locale `README.md` files
3. Previous/next links in adjacent chapters
4. `.vitepress/config.mts` sidebar entries

## Verification Checklist
- Small text edit: read the final file for structure and links
- Link-heavy edit: prefer `npm run build`
- Sidebar/nav edit: verify in dev, then build if possible
- Locale edit: compare to the matching English page
- If validation fails, state the real failure and whether it appears pre-existing

## Agent Priorities
1. Preserve structure and cross-file consistency
2. Keep edits minimal and easy to review
3. Avoid introducing tooling the repo does not use
4. Fix the requested scope without unrelated cleanup
5. Call out real validation issues when they affect confidence
