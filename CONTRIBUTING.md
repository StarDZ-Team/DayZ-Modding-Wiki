# Contributing to the DayZ Modding Wiki

Thank you for your interest in improving this documentation. Contributions of all sizes are welcome, from fixing a typo to writing an entire new chapter.

---

## Table of Contents

- [How to Report Errors](#how-to-report-errors)
- [How to Submit Corrections](#how-to-submit-corrections)
- [Adding New Chapters](#adding-new-chapters)
- [Translation Guidelines](#translation-guidelines)
- [Style Guide](#style-guide)
- [Code Examples](#code-examples)
- [Review Process](#review-process)

---

## How to Report Errors

If you find an error but do not want to fix it yourself, open a GitHub Issue:

1. Go to the repository's **Issues** tab
2. Click **New Issue**
3. Use a descriptive title (e.g., "Chapter 6.1: GetHealth() parameter order is wrong")
4. Include:
   - The file path or chapter number
   - What is currently written
   - What it should say
   - A source or reference if possible (vanilla script file, tested in-game result)

Even small reports are valuable. Incorrect API signatures or outdated method names can waste hours of a modder's time.

---

## How to Submit Corrections

### Quick Fixes (Typos, Small Errors)

1. Fork the repository
2. Edit the file directly on GitHub or in your local clone
3. Create a pull request with a clear description of what you changed and why

### Larger Changes (Rewriting Sections, Adding Content)

1. Fork the repository
2. Create a branch named after the change (e.g., `fix/chapter-6-vehicle-api` or `add/chapter-9-modding-tools`)
3. Make your changes
4. Test any code examples if possible (build a PBO, load in-game, verify behavior)
5. Submit a pull request

### Pull Request Guidelines

- **One topic per PR.** Do not mix a typo fix with a new chapter.
- **Describe what changed.** Include the chapter number and a brief summary.
- **Reference sources.** If correcting an API signature, mention the vanilla script file (e.g., `scripts/3_Game/entities/entityai.c`) or link to tested behavior.
- **Keep existing formatting.** Match the style of surrounding content (see Style Guide below).

---

## Adding New Chapters

### File Naming

All chapter files follow this naming convention:

```
<part-number>-<section-name>/<sequence-number>-<topic-slug>.md
```

Examples:
- `01-enforce-script/05-control-flow.md`
- `08-tutorials/03-admin-panel.md`

### File Structure

Every chapter should follow this structure:

```markdown
# Chapter X.Y: Title

> **Summary:** One or two sentences describing what this chapter covers.

---

## Table of Contents

- [Section 1](#section-1)
- [Section 2](#section-2)

---

## Section 1

Content here.

---

## Section 2

Content here.

---

**Previous:** [Chapter X.Y-1](previous-file.md) | [Home](../../README.md) | **Next:** [Chapter X.Y+1](next-file.md)
```

### Updating the Table of Contents

When adding a new chapter, update these files:

1. **`README.md`** (root) -- Add the chapter to the appropriate Part table
2. **`en/README.md`** -- Add the chapter to the English table of contents
3. **Navigation links** in the previous and next chapters (update "Next" and "Previous" links)

---

## Translation Guidelines

This wiki supports 12 languages. When translating:

### What to Translate

- All prose, headings, summaries, and explanatory text
- Table headers and descriptions
- Comments inside code blocks (the `//` lines)
- Alt text and link labels

### What NOT to Translate

- **Code keywords and identifiers:** `class`, `modded`, `override`, `super`, `void`, `int`, `float`, `bool`, `string`, `vector`, `null`, `true`, `false`
- **Class names:** `MissionServer`, `PlayerBase`, `ItemBase`, `EntityAI`
- **Method names:** `GetPosition()`, `SetHealth()`, `OnInit()`
- **File names:** `config.cpp`, `mod.cpp`, `stringtable.csv`
- **Config syntax:** `CfgPatches`, `CfgMods`, `requiredAddons[]`
- **Path prefixes:** `$profile:`, `$saves:`, `$mission:`
- **Tool names:** Addon Builder, Workbench, Object Builder

### File Structure for Translations

Translations mirror the English structure exactly:

```
en/01-enforce-script/01-variables-types.md    (English original)
pt/01-enforce-script/01-variables-types.md    (Portuguese translation)
de/01-enforce-script/01-variables-types.md    (German translation)
```

### Translation Checklist

- [ ] All headings translated
- [ ] All prose translated
- [ ] Code blocks unchanged (except comments)
- [ ] Internal links updated to point to the correct language folder (e.g., `../pt/` instead of `../en/`)
- [ ] Table of contents anchors still work (anchors are auto-generated from heading text)
- [ ] README.md for the language updated with all chapter links

---

## Style Guide

### Markdown Formatting

- Use **ATX headings** (`#`, `##`, `###`). Do not use underline-style headings.
- Use `---` horizontal rules to separate major sections.
- Use **bold** for UI element names, file names in prose, and emphasis. Use `code` for class names, method names, code snippets, and paths.
- Use tables for API references and structured data.
- Use ordered lists (`1.`, `2.`, `3.`) for sequential steps.
- Use unordered lists (`-`) for non-sequential items.

### Headings

- `#` -- Chapter title (one per file)
- `##` -- Major sections
- `###` -- Subsections
- `####` -- Rare; use only when a subsection genuinely needs further subdivision

### Writing Style

- Write in **second person** ("you") when giving instructions.
- Write in **present tense** ("This method returns..." not "This method will return...").
- Use **plain English**. Avoid jargon unless it is DayZ-specific terminology that modders need to know.
- Use **em dashes** (`---` rendered as ---) instead of parenthetical asides where possible.
- Spell out numbers under 10 in prose. Use digits for technical values (10, 100, 5000).
- Use **double dashes** (`--`) for inline parenthetical thoughts (Markdown renders these as an em dash in most renderers).

### Links

- Internal links use **relative paths** (e.g., `../02-mod-structure/02-config-cpp.md`).
- External links use full URLs.
- Always include link text that describes the destination (not "click here").

---

## Code Examples

### Language Tags

Use the appropriate language tag for fenced code blocks:

- `` ```c `` -- Enforce Script (`.c` files)
- `` ```cpp `` -- config.cpp, mod.cpp (C++-like syntax)
- `` ```xml `` -- XML files (stringtable.csv is XML despite the extension, types.xml, etc.)
- `` ```json `` -- JSON files
- `` ```batch `` -- Windows batch files
- `` ```bash `` -- Shell commands
- No tag -- Plain text output, file paths, directory trees

### Code Accuracy

- **Test code examples before submitting.** At minimum, verify they compile (pack a PBO with them). Ideally, test them in-game.
- **Keep examples minimal.** Show only what is necessary to demonstrate the concept. Do not include unrelated boilerplate.
- **Add comments.** Explain non-obvious lines with inline comments.
- **Use realistic names.** `MyItem` and `PlayerBase` are fine. `foo` and `bar` are not.

### Code Blocks in Tables

For single-line code in tables, use inline code: `` `GetPosition()` ``. Do not put fenced code blocks inside table cells.

---

## Review Process

1. **Automated checks:** None currently. We rely on manual review.
2. **Content review:** A maintainer will read your changes for accuracy and style.
3. **Merge:** Once approved, your changes are merged into the main branch.
4. **Credit:** Contributors are acknowledged. Significant contributions are added to the Credits section of the README.

---

## Questions?

If you are unsure about anything, open a GitHub Issue with the `question` label and ask. We would rather answer a question than receive an incorrect contribution.

---

*Thank you for helping make DayZ modding documentation better for everyone.*
