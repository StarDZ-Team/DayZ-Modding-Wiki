# AGENTS.md

Agent guide for `D:\StarDZ\docs\wiki`.

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
Build results are revision-specific. Earlier runs encountered JavaScript heap exhaustion; a later isolated build succeeded, but that does not validate subsequent edits. Do not claim the current build passes unless you run it and confirm a zero exit code. Record the revision, Node version, memory settings, command, and result.
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

## EN Audit Agreement

These instructions consolidate the user's decisions from the audit conversation on 2026-09-13. They guide continuing work and can be improved with the user. New user instructions take precedence. Historical findings belong in audit reports; do not treat this file as proof that any technical claim is correct.

### Objective and Scope

- Make the English wiki a reliable knowledge base for DayZ modders and server administrators, with accurate explanations and useful, verifiable examples.
- Audit both correctness and completeness: hierarchy, navigation, concepts, API names, configuration, workflows, examples, limitations, and missing topics.
- Reading every existing page does not prove that all necessary topics are covered. Maintain a coverage map and actively search for omissions.
- The user's target is no remaining repairs and complete reliability. Do not turn that target into an unsupported claim of 100% correctness. Keep unresolved claims, missing tests, and known gaps visible until addressed.
- This audit targets `en/`. Preserve other locales. If EN structure changes, update the affected EN navigation and shared configuration without generating broken routes for other locales; record translation parity work separately.
- Improvements to wiki pages are authorized when they support this objective. Avoid unrelated cleanup.

### Sources That Must Be Consulted

| Source | Location or examples | How to use it |
|---|---|---|
| Extracted game files | `D:\DayZ Projects` | Open relevant scripts, configs, and assets from the official-tool extraction; establish version provenance where possible. |
| User's beta mods | `D:\StarDZ` | Inspect real implementations and edge cases; these mods may contain errors and are not authoritative. |
| Local documentation | `D:\StarDZ\docs` | Read relevant documents outside this wiki too; validate their claims independently. |
| Official sources | Bohemia documentation, DayZ Samples, DayZ Script Diff, Central Economy repositories | Prefer direct, version-specific evidence and distinguish DayZ from other Bohemia games. |
| Public mods | VPP Admin Tools, Community Framework, Community Online Tools, DayZ Expansion, DayZ Editor, and other relevant GitHub projects | Download and inspect relevant code, with pinned commits. Seek additional projects when existing references do not cover a topic. |
| Modding community | Discord community `https://discord.com/channels/452035973786632194`, when accessible through Orca | Use discussions as research leads and corroborating evidence. Do not send messages without explicit authorization. |

- Actually open the relevant files. A clone, search result, repository name, or agent assertion is not evidence that code was examined.
- Record repository URL and commit, file path and relevant lines or symbols, game/tool version when known, and access date for web sources. Use hashes when recording the exact local source or reviewed delivery.
- Separate official behavior, third-party implementation choices, community advice, and inference. Popular mods can also contain bugs.
- Corroborate disputed or consequential claims with independent evidence. Multiple projects copying the same implementation are not independent proof.
- Missing script declarations do not prove that a native feature is absent. Empty or incomplete extracted files cannot establish absence either.
- State access failures and evidence limits honestly. Do not cite inaccessible material as if it was read.

The user explicitly supplied a local reference corpus on 2026-09-13. Its exact paths are preserved in [the source list](.audit/en-2026-09-13/completeness/user-source-paths.txt), including `plans/`, `vanilla_metadata/`, `AI/`, `DayZ/`, technical references, cookbooks, guides, and StarDZ specifications/contracts. Consult relevant contents by domain and track actual reading separately from inventory. A document's own verification label or claim that tests passed is a lead to verify, not independent proof. Product plans and designs must not be represented as implemented DayZ behavior.

### Coverage of Limits and Packaging

Include PBO packaging and multi-PBO design in the coverage map, alongside language, GUI, assets, engine APIs, patterns, tutorials, and server administration.

- Investigate PBO size claims rather than assuming a universal limit from the phrase "32-bit." Distinguish format field widths, individual entries, total archive size, compression, packing tools, engine loading, and distribution limits. Document a numeric limit only with evidence for its scope and version.
- Cover multi-PBO directory layouts, prefixes and virtual paths, `CfgPatches`, `requiredAddons`, `CfgMods`, script modules, dependencies, load behavior, and client/server packaging where supported by sources.
- Include practical build, signing, deployment, update, and troubleshooting examples, with their prerequisites and expected results.
- Investigate other relevant limits in scripting, networking/RPC, persistence, Central Economy, assets, tools, and server operation. Separate hard limits from configurable settings, measured behavior, and recommendations.
- Do not invent precise limits or imply that an example was compiled, packaged, or run without performing that validation.

### Orchestration and Model Selection

- Use Orca CLI and its orchestration skill for supervised workers, task dispatch, delivery tracking, and worktree management. Read the installed, version-matched skill guidance before operating it.
- Use Codex/ChatGPT agents only. The later instruction excluding Claude supersedes the earlier permission to use Claude with bypass.
- Choose models according to the task and evidence risk, aiming to save tokens without weakening accuracy. Suggested allocation: Luna for mechanical inventory and checks; Terra for bounded implementation; Sol for factual research and independent review; Astra for difficult conflicts or deeper reasoning when justified.
- These are guidelines, not a requirement to use every model. Confirm the model identifiers supported by the current runtime and record the model actually used.
- Keep the root primarily focused on orchestration, integration, and decisions. Delegate bounded research and reviews instead of doing everything in the root context.
- Workers may request or delegate specialist help when needed, within concurrency and ownership constraints. Give each worker explicit scope, source requirements, output paths, and acceptance criteria.
- Avoid overlapping edits. Preserve partial deliveries and usable evidence when an agent fails or is replaced.
- Use graphify for project relationships and refresh the graph after accepted content changes. A graph is an orientation aid, not factual proof. Cartographer may also be used if available and useful.
- Use other Orca capabilities when relevant; do not create unrelated tickets or environments merely because a skill was mentioned.

### Independent Council and Integration

1. The author reports each proposed correction or addition with the affected page, original claim or gap, proposed wording/example, reason, and source evidence.
2. An independent reviewer reopens the relevant sources and evaluates the reasoning and examples. Another model agreeing with the author's summary alone is insufficient.
3. The council records accepted, rejected, and unresolved findings explicitly. Return unsupported or incorrect deliveries to the author for repair and another review.
4. Check the final diff or exact delivered files after repairs. Approval of an earlier draft does not approve later changes.
5. Integrate approved deliveries into the current branch incrementally, so completed work is not stranded in worktrees. Commit approved changes; do not push unless requested.
6. Before closing a worktree, check its unique commits and tracked/untracked changes. Integrate approved work and preserve remaining recoverable material with a receipt before removal through Orca.
7. Settle and release completed workers according to Orca's lifecycle. Keep a clear record of active work and retained worktrees.

Downloading reference repositories, creating checkouts, making relevant reversible edits, delegating, and committing approved work to the current branch are already authorized. Preserve unrelated user changes and do not use broad staging commands that include them accidentally.

### Verification and Completion Criteria

- Maintain a page/topic coverage map, a findings ledger, source-use records, and council decisions. Reuse prior evidence when still applicable, but check whether revisions invalidate it.
- Distinguish static source review, documentation build, script compilation, tool execution, and actual game/server/client tests. A VitePress build does not validate Enforce Script or gameplay behavior.
- Examples must state dependencies, file placement, execution context, and expected behavior where relevant. Mark conceptual or incomplete examples clearly; do not present a placeholder as a complete working system.
- Validate error paths and client/server trust boundaries for consequential examples, including permissions, RPC, persistence, and transactions.
- Repair known navigation and anchor defects, verify changed routes, and run the current integrated build. Report actual failures and their scope.
- Regenerate affected generated documentation and the graph after final accepted edits, then verify the resulting artifacts before committing them.
- Do not close the overall goal merely because all workers finished or all existing pages were read. Known errors, missing required coverage, and required verification must be resolved; remaining uncertainty must never be silently counted as verified.
- Report concrete outcomes, commits, sources consulted, and remaining limitations. Never fabricate confidence, test results, or source access.

### Resume From Recorded Evidence

The second-pass audit checkpoint is recorded in [the audit report](.audit/en-2026-09-13/doublecheck/REPORT.md), [source-use report](.audit/en-2026-09-13/doublecheck/source-use-REPORT.md), and [findings ledger](.audit/en-2026-09-13/doublecheck/findings-dispositions.json). Consult those artifacts before repeating work, and verify the current Git and Orca state instead of assuming the checkpoint is current.

At that checkpoint, commit `99327d83c22e9585df27ce8edd9d510e7fc42e25` contained second-pass corrections. Unresolved technical claims, existing anchor defects, final graph/build verification, and broader coverage of limitations and multi-PBO remained follow-up work. This is a dated handoff, not a completion declaration.
