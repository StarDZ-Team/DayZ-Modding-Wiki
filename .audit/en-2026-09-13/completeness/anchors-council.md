# English Anchor Repair — Independent Council Review

## Decision

**APPROVE exact current EN diff against `8fa131365f59a343602cefd682290535cd435cc2`.**

The reviewed delivery is 210 fragment-only corrections across 209 source lines in 41 English Markdown files. Every changed destination resolves to exactly one heading ID emitted by the installed VitePress renderer, every mapping preserves the link label and file target, and no heading or other prose changed. This approval is bound to the hashes in `anchors-council.json`; later edits require re-review.

## Independent verification

- Baseline: Git HEAD and comparison base were both `8fa131365f59a343602cefd682290535cd435cc2`.
- Runtime: Node `v24.14.0`; installed VitePress `1.6.4`.
- Checker inspection: `scripts/check-links.mjs` imports VitePress `createMarkdownRenderer`, renders the current target source, and reads the resulting `h1`–`h6` `id` attributes. The installed VitePress bundle passes its own `slugify` to `markdown-it-anchor`; that slugifier handles punctuation, numeric prefixes, inline heading text, and duplicate IDs. The checker therefore uses renderer IDs rather than treating a GitHub-style slug recreation as authoritative.
- Fresh strict run: `node scripts/check-links.mjs --anchors --strict` exited 0; 1,265 Markdown files had zero dead file links, and 105 English files had 1,278 fragment links checked with zero dead fragments.
- Fresh diff check: `git diff --check -- en` exited 0.
- Independent source comparison found 41 changed files and 209 changed lines. Replacing only Markdown-link fragments with a sentinel made every changed baseline/current line identical; the sole two-repair line is `en/08-tutorials/05-mod-template.md:90`.
- Independent rendered-link comparison found exactly 210 changed links. Each retained the same rendered label and path component, and each new fragment matched exactly one current rendered heading.
- The 210 baseline failures partition exactly into 171 `github-slug`, 32 `punctuation-insensitive`, and seven manual occurrences. No valid baseline link was changed outside that set.
- All 41 current file hashes match `anchors-final-hashes.json`. The raw binary EN diff SHA-256 is `73e8ab04b29fa2f9fc7ab441356f82be4a3b08a8108ee9fe655b677a32fc064d`.

The checker deliberately does not validate reference-style links, inline HTML links, or absolute site paths. That limitation does not weaken this decision: all 210 changed links are inline Markdown fragments harvested by the checker, and the independent rendered-link comparison separately accounted for every changed link.

## Mapping decisions

All 171 GitHub-slug mappings are approved. For each, the old fragment identifies exactly one target heading under the repository’s legacy GitHub-style slug convention, while the replacement is the installed renderer’s ID for that same heading.

All 32 punctuation-insensitive occurrences are approved individually in `anchors-council.json` (30 unique old/new/target triples). The mappings cover punctuation that VitePress treats differently: periods in filenames and API names, em dashes, ampersands, slashes, underscores, and numeric-prefix IDs. Each replacement was independently reopened against the rendered target heading.

All seven manual occurrences are approved:

| Source | Link label | Old → new | Decision |
| --- | --- | --- | --- |
| `en/01-enforce-script/09-casting-reflection.md:13` | `obj.IsInherited — Runtime Type Checking` | `#obisinherited--runtime-type-checking` → `#obj-isinherited-—-runtime-type-checking` | Approve: exact subject and heading label. |
| `en/01-enforce-script/09-casting-reflection.md:14` | `obj.IsKindOf — String-Based Type Checking` | `#obiskindof--string-based-type-checking` → `#obj-iskindof-—-config-based-type-checking` | Approve: the only `obj.IsKindOf` heading is the intended section. “String-Based” versus “Config-Based” is a pre-existing label/heading wording difference, not a wrong target introduced by this repair. |
| `en/glossary.md:38` | `PBO` | `#pbo` → `#pbo-packed-bank-of-objects` | Approve: unique PBO glossary definition. |
| `en/glossary.md:97` | `PBO` | same as above | Approve: unique PBO glossary definition. |
| `en/glossary.md:217` | `COT` | `#cot` → `#cot-community-online-tools` | Approve: unique COT glossary definition. |
| `en/glossary.md:411` | `P Drive` | `#p-drive` → `#p-drive-workdrive` | Approve: unique P Drive glossary definition. |
| `en/glossary.md:579` | `PBO` | `#pbo` → `#pbo-packed-bank-of-objects` | Approve: unique PBO glossary definition. |

The contextual link labels that are shorter than their headings (for example “Section 4,” “Step 5,” “below,” and “same chapter”) were also checked against their surrounding text and target subject. None redirects to an unrelated heading.

## Hash-bound delivery

`anchors-council.json` records:

- all 41 final English file SHA-256 hashes;
- all 32 punctuation-based occurrence decisions and all seven manual occurrence decisions;
- hashes of the checker, repair plan, author artifacts, and installed VitePress bundle;
- the exact raw EN diff SHA-256.

No English content, checker, configuration, or author artifact was edited during this review.
