# PBO English Implementation Receipt

**Date:** 2026-09-13  
**Scope:** Accepted PBO council conclusions only; English files under `en/02-mod-structure/`, `en/04-file-formats/06-pbo-packing.md`, and `en/08-tutorials/07-publishing-workshop.md`. No fixture, locale, configuration, game, or commit changes were made.

---

## Implemented proposal mapping

| Proposals | Delivered change |
|-----------|------------------|
| PBO-001–003 | Corrected the member-header explanation; separated member-field widths from total archive, tool, runtime, filesystem, and Workshop boundaries; retained the scoped compression evidence. No universal 2 GiB, 4 GiB, or unlimited-size claim was made. |
| PBO-004, PBO-005, PBO-008 | Distinguished launch package, PBO filename, prefix/virtual root, and `CfgPatches` identity; stated that `requiredAddons[]` uses addon class names and `CfgMods` paths are mounted virtual paths; made duplicate normalized virtual paths a conservative release policy. |
| PBO-006 | Replaced the unreliable inline automation patterns with the two-phase build/inspect then hash/sign/package workflow and linked `examples/en/multi-pbo` with its prerequisites, command, receipt, and validation boundary. |
| PBO-007 | Moved the server-only boundary to a separate folder-level `@MyModServer` package loaded through `-serverMod`; no per-PBO routing claim remains. |
| PBO-009 | Replaced the publishing tutorial's textual `-mod=` load-order advice with `CfgPatches.requiredAddons[]` guidance. |
| PBO-010 | Scoped signature claims to configured server verification, required final-byte signing, retained the DSCheck stdout limitation, and aligned key reuse/rotation guidance. |
| PBO-011–012 | Retained pinned implementation provenance through the research record and separated Workshop service limits from PBO/runtime limits. |

---

## Reopened evidence

- `pbo-research.md`, `pbo-evidence.json`, `pbo-council.md`, `pbo-final-council.md`, and the accepted `pbo-repair-council.md/json`.
- Official-documentation snapshots: `D:/StarDZ/docs/DayZ/Modding Structure.md` lines 6–91; `C:/Users/Leonardo Mello/AppData/Local/Temp/wiki-audit-20260911/BIKI-Server-council-20260913.txt` lines 27 and 180–181.
- Official samples/extraction: DayZ Samples commit `da5e5437c9502620d9853fb6eed14701135ab2ea`, `Test_Inputs/config.cpp` lines 1–33; `D:/DayZ Projects/DZ/data_sakhal/config.cpp` lines 1–30.
- Installed official tools reopened on 2026-09-13: Addon Builder `1.0.240639` SHA-256 `C113DE9CAB5E91D27CA0630E360DB0A3ECA190EC797E1DCAD9CDFA70466B45E1`; DSSignFile `098F28B46BFE40AD4CF5C60DD3E570E984FE74AE423090B6D3F2DA8D7C4E1E78`; DSCheckSignatures `9BAFBBBDCE1E2792515039F99B7150CA1CE97ADF16AAB8CFC79BDC8938A8503C`.
- Reproducible fixture reopened but not changed: `examples/en/multi-pbo/README.md` SHA-256 `3449B09BBDD04A278A17DD8E3A79A1D27EEB76B173431A73A255C52EE23BC0CE`; `build.ps1` SHA-256 `38F24D830DBCB7985ABF1ED9636493C5BDFEA1E160169379FE10E8F50BADB956`.

---

## Validation

- `node scripts/check-links.mjs --anchors --strict en`: passed — 105 files, 0 dead file links, 0 dead anchors.
- `git diff --check -- <owned EN paths>`: passed — no whitespace errors. Line-ending notices are Git conversion warnings only.
- Each edited Markdown file has one top-level heading; no Mermaid fence was edited. A standalone Mermaid parser probe could not initialize DOMPurify under Node `v24.14.0`; the changed prose contains no Mermaid syntax to parse.
- `NODE_OPTIONS=--max-old-space-size=4096 npm run build` was attempted three times. Exec sessions `52`, `53`, and `61` each reached VitePress's `building client + server bundles` line, but their wrappers did not return a process exit code or a full stderr tail. The observed Node PID pairs were `49360/50404`, `52016/53224`, and `23672/41704`; all six were positively absent when rechecked at 2026-09-13 22:16 America/Sao_Paulo, so no owned build process remained to stop. No run produced a zero-exit receipt or `.vitepress/dist/index.html`; do not treat the current integrated build as passing.

Runtime and boundary experiments remain open: DayZ boot/Enforce compilation, mounted cross-PBO paths, missing `requiredAddons`, clean-client `-serverMod` distribution, `verifySignatures = 2` cases, serverMod-only signatures, PBO size boundaries, and Workshop upload/download behavior.

---

## Final English hashes

| Path | SHA-256 |
|------|---------|
| `en/02-mod-structure/01-five-layers.md` | `60269FB1AE83AED1D9C00BDE0AF94204ABF0056617EB16662E8ED0CC1574DA15` |
| `en/02-mod-structure/02-config-cpp.md` | `1AEB9C620B3800C51CCAD3BB13005B684102EA04D02A2DD5688C15F5B9FAAE7A` |
| `en/02-mod-structure/03-mod-cpp.md` | `CEB5B1E3E8BEC93D21177A1C3D092225BB19BA0909EA02EA48F822AE52AB3506` |
| `en/02-mod-structure/04-minimum-viable-mod.md` | `A6209D15E139C5744B5D6A2479F9275C779FA0BF4B5610D98BA232FA38EF7C43` |
| `en/02-mod-structure/05-file-organization.md` | `24AAAD4F0E5A522F23388891BC40393F763F27A1ADDC8C561526E59F04D3BC42` |
| `en/02-mod-structure/06-server-client-split.md` | `498131A57D410CEB4A65C061A26ADDFFAC8182E2E5E2166DD0E8233F9D5A5081` |
| `en/04-file-formats/06-pbo-packing.md` | `42FBEB3CBA2C689CB9728EC83D9B21E55FF244EFB2E59FF122827523B727DDF9` |
| `en/08-tutorials/07-publishing-workshop.md` | `141D973FB307ECB7DA39693ABDFE18D97D9D8A038B0A5A1837C802C86C844E0E` |
