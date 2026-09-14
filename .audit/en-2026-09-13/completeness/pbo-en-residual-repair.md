# PBO English Residual Repair

**Date:** 2026-09-13  
**Scope:** Exactly the two residual sentences identified by `pbo-en-repair-council.md/json`; no build, runtime test, or commit.

## Repairs

| File | Before | After | Reason |
|---|---|---|---|
| `en/02-mod-structure/03-mod-cpp.md:513` | `Two mods with identical field values will not conflict -- only CfgPatches class names in config.cpp can collide.` | `Identical mod.cpp presentation values do not create load-order conflicts; separately, duplicate CfgPatches names and duplicate mounted virtual paths can collide.` | Removes the false absolute and acknowledges both the CfgPatches and mounted virtual-path namespaces, as required by EN-PBO-F06. |
| `en/02-mod-structure/06-server-client-split.md:229` | `Inside config.cpp (in the CfgMods section), there is also a type field. This one controls how the engine treats the mod internally:` | `Inside config.cpp (in the CfgMods section), there is also a type field; Bohemia's published example marks type = "mod" as required, but the reviewed sources do not establish another value or a routing behavior for the field:` | Replaces unsupported internal-behavior wording with the council-approved documented-syntax and evidence-boundary wording for EN-PBO-F03. |

## Exact identities after repair

SHA-256 covers raw worktree bytes. Normalized identity is `git hash-object --path=<path> <path>`.

| File | SHA-256 | Normalized Git blob |
|---|---|---|
| `en/02-mod-structure/03-mod-cpp.md` | `A5B78D9440C5876B4A9C8DE0C60ADFFB2D94B1D22FFCC452EE7D526605A2AAAE` | `1140bddb74229d09d447887dcdda4f8247d578b9` |
| `en/02-mod-structure/06-server-client-split.md` | `C20891B4D7F43C0C43B9623C589F10EC1D4262F2A9019F9020ACAC1849F45B0D` | `eda13db3399a0b0d26323c7880d27ee99b0ae2de` |

## Six approved-page identity verification

All six approved pages match the council's recorded raw SHA-256 and normalized Git blob identities: `01-five-layers.md`, `02-config-cpp.md`, `04-minimum-viable-mod.md`, `05-file-organization.md`, `04-file-formats/06-pbo-packing.md`, and `08-tutorials/07-publishing-workshop.md` — **6/6 match**. No other English page was changed by this repair.

## Validation

`git diff --check -- en/02-mod-structure/03-mod-cpp.md en/02-mod-structure/06-server-client-split.md` passed (exit 0; only line-ending conversion notices). Runtime, signing, distribution, limits, Workshop, and other council-open uncertainties remain unchanged; final exact-change inspection is still required by the council.
