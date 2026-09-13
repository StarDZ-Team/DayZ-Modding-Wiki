# English Internal Anchor Repair Report

## Scope and result

Only Markdown link fragments in `en/` were changed. No headings, prose, other locale destinations, scripts, configuration, or non-anchor user files were edited.

The fresh baseline (`anchors-before.json`) found 210 dead fragments in 41 of 105 English Markdown files, after checking 1,278 fragments against IDs emitted by the installed VitePress Markdown renderer. The final strict run (`anchors-after.json`) checked the same 1,278 fragments and found 0 dead fragments; it also checked 1,265 Markdown files for file links and found 0 dead file links.

## Evidence and mapping method

Commands and outcomes, executed with Node `v24.14.0` at Git `8fa131365f59a343602cefd682290535cd435cc2`:

1. `node scripts/check-links.mjs --anchors --json=.audit/en-2026-09-13/completeness/anchors-before.json` — exit 0; 210 dead anchors.
2. `node scripts/repair-anchors.mjs --json=.audit/en-2026-09-13/completeness/anchors-dry-run.json` — exit 0; 203 unique, safe rewrites and 7 withheld entries.
3. `node scripts/repair-anchors.mjs --apply --json=.audit/en-2026-09-13/completeness/anchors-applied-auto.json` — exit 0; wrote those 203 proven rewrites.
4. `node scripts/check-links.mjs --anchors --strict --json=.audit/en-2026-09-13/completeness/anchors-after.json` — exit 0; 0 dead anchors and 0 dead file links.
5. `git diff --check -- en` — exit 0.

The dry-run and applied JSON artifacts contain every automatic old-to-new fragment mapping, its source line, target page, VitePress ID, and rule (`github-slug` or `punctuation-insensitive`). The checker reads actual `id` attributes rendered by installed VitePress, rather than recreating a slug algorithm.

## Initially withheld cases

The helper intentionally withheld seven entries because their abbreviated legacy fragments did not match a heading under either automatic rule. Each was reviewed against the source link label and the exact single matching target heading, then corrected without changing link text or headings:

| Source | Old fragment | Final fragment | Reason |
| --- | --- | --- | --- |
| `09-casting-reflection.md:13` | `#obisinherited--runtime-type-checking` | `#obj-isinherited-—-runtime-type-checking` | Only rendered `obj.IsInherited` heading. |
| `09-casting-reflection.md:14` | `#obiskindof--string-based-type-checking` | `#obj-iskindof-—-config-based-type-checking` | Only rendered `obj.IsKindOf` heading. The unchanged link label says “String-Based,” while the existing heading says “Config-Based”; this pre-existing terminology discrepancy is out of scope. |
| `glossary.md:38,97,579` | `#pbo` | `#pbo-packed-bank-of-objects` | Single glossary heading for PBO. |
| `glossary.md:217` | `#cot` | `#cot-community-online-tools` | Single glossary heading for COT. |
| `glossary.md:411` | `#p-drive` | `#p-drive-workdrive` | Single glossary heading for P Drive. |

There are no unresolved dead English anchors in the final check. The final content hashes are recorded in `anchors-final-hashes.json`.
