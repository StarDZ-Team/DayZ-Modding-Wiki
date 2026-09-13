# English wiki second-pass audit

Baseline: `bf7ae1947876071ed4e25578dc595d896f2e6263`, branch `wiki-reorg`, 2026-09-13.

## Result

Reviewed all **105 English Markdown pages**, including indexes and references, in five disjoint domains. Applied **55 independently approved editorial repairs across 35 pages**. Separate final council reviews reconstructed the edited pages from the baseline and approved every changed scope for commit. No page is certified error-free merely because this pass found no defect.

The [disposition ledger](findings-dispositions.json) records **67 unique adjudicated items: 55 accepted, 4 rejected, and 8 unresolved and unchanged**. This includes nine inherited language leads. Trading findings are counted once after their revised review; the second CF notification occurrence belongs to the existing ENG-002 finding. Editorial acceptance can mean replacing an unsupported assertion with explicit uncertainty, not proving the underlying runtime behavior.

## Coverage and evidence

| Domain | Pages | Final applied findings | Final independent verification |
|---|---:|---:|---|
| Language and mod structure | 19 | 17 | [Language](final-language.json) |
| GUI and assets | 18 | 8 | [GUI/server group](final-early.json) |
| Engine APIs | 24 | 6 | [Engine](final-engine.json) |
| Patterns and tutorials | 20 | 19 | [Patterns/tutorials](final-tutorials.json), [trading](final-trading.json) |
| Configuration, server administration, references | 24 | 5 | [GUI/server group](final-early.json) |

The [coverage inventory](coverage-consolidated.json) preserves baseline hashes, actual reading provenance, checks, source pointers, and page-specific limitations. Its 105 entries match the recursive English tree exactly, without duplicate assignments. The [baseline inventory](coverage-baseline.json) preserves original checkout hashes.

Researchers independently reopened primary evidence; prior audit approvals were leads only. [Concrete source-use records](source-use-REPORT.md) name the actual line ranges and hashes read from three non-wiki local reference documents, five StarDZ beta implementations, VPP, COT, CF, and official extracted scripts. The [machine-readable corpus record](source-use.json) distinguishes file consultation from clone/version checks and records eight public repository origins and commits. Local docs and beta/mod implementations remain fallible corroboration, never proof of native behavior.

Official script evidence includes [Bohemia DayZ-Script-Diff at 86974a0](https://github.com/BohemiaInteractive/DayZ-Script-Diff/tree/86974a0f5bd16b1ee3e334ad828133c93dca80a1), identified upstream as Build 1.29.163709 / Scripts Rev. 125372. Some relevant extraction files matched upstream exactly; others are separately identified snapshots, not silently assigned that version. Council records contain precise source paths/lines and raw or LF-normalized hashes. Direct Bohemia Wiki requests sometimes returned HTTP 403; affected reviews explicitly distinguish indexed official text from a retrieved whole-page body.

## Repairs and rejected proposals

Changes cover incorrect widget/casting APIs, damage callbacks, reference/default-parameter examples, RPC prerequisites and collision claims, config activation/error reporting, CE terminology, input namespaces, notifications, and tutorial failure handling. The trading tutorial retains UI/configuration/RPC material and bounded server checks, but now refuses buy/sell requests before asset mutation: it does not implement or claim a safe live-economy transaction protocol.

Council rejected unsupported imageset parser/performance and retail MLOD conclusions, the attempt to disprove single-threaded gameplay from replication workers, and a timer replacement contradicted by vanilla profiler tests. It also required revised trading repairs rather than accepting error messages after irreversible loss. Three erroneous language source hashes and shifted author IDs were corrected before implementation.

Exact quotes, repairs, evidence, and reasons are in the council records: [GUI/assets and gameplay config](council-early-REPORT.md), [server additions](council-server-extra-REPORT.md), [language](council-language-REPORT.md), [patterns/tutorials](council-tutorials_patterns-REPORT.md), [trading](council-trading-REPORT.md), [engine](council-engine-REPORT.md), and [notification additions](council-notification-extra-REPORT.md).

## Actual validation and limits

[Final validation](validation-final.json) records:

- `git diff --check -- en`: exit 0.
- Existing English link/anchor checker: 105 pages, zero dead file links, 210 dead anchors across 41 pages. Strict mode exits 1 for those existing defects.
- Anchor identities match baseline exactly after ignoring insertion-driven line shifts: zero introduced or removed failures. Broad navigation cleanup was excluded.
- Independent scoped VitePress renderer checks confirm one rendered H1 and balanced fences; source and final page hashes are recorded in the five final review JSON files.

No full build, Enforce compilation, game/server/client runtime test, exploit test, asset-tool test, or transaction fault test was run. Unchanged unresolved items include zero-vector normalization, `typename.Spawn` constructor restrictions, omitted-`override` dispatch, `autoptr` alias lifetime, static lifetime across restart, `Object.IsDeleted` absence claims, listen-server semantics, and an underspecified global-scope `Print` lead. Custom CE globals, deletion replication/timing, and other qualified native questions remain unproven even where wording was repaired.

Original English bytes and intermediate checkpoints are preserved outside this curated commit. Translations, shared configuration, graph outputs, agent/specification/workflow files, and existing untracked user work were not edited. Initial default reviewers resolved to Astra before cost steering; subsequent substantive reviews used Sol, mechanical accounting used Luna, and implementation used Terra. All work used Orca Codex workers; no push was performed.
