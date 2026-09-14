# PBO English Final Council

**Review date:** 2026-09-13  
**Baseline:** `0df58c20761f654cd91ece04d9469be4b1728c6b`  
**Reviewed state:** `103238a83078784b7ee6cd6486f63d7973e3fe92` plus the eight unstaged English files listed below; this HEAD contains independent language commit `46ba270` and a later unrelated diagnostic-evidence commit  
**Decision:** **reject the exact eight-file set pending bounded repairs.** The limit taxonomy, addon/package/path model, two-phase build workflow, DSCheck qualification, key-rotation rule, and main fixture route are substantively improved, but four pages still contain material contradictions or unsupported absolutes and the PBO page does not satisfy the accepted pinned-source-citation requirement.

No English content, configuration, fixture, or commit was changed. No game or full VitePress build was launched.

---

## Per-file disposition and exact identities

The Git blob OIDs below are from `git hash-object --no-filters` over the exact reviewed worktree bytes.

| File | Disposition | SHA-256 | Git blob OID |
|---|---|---|---|
| `en/02-mod-structure/01-five-layers.md` | **Approve** | `60269FB1AE83AED1D9C00BDE0AF94204ABF0056617EB16662E8ED0CC1574DA15` | `a0427e8398045579cfc27af9b3bc1178a50b490a` |
| `en/02-mod-structure/02-config-cpp.md` | **Reject** | `1AEB9C620B3800C51CCAD3BB13005B684102EA04D02A2DD5688C15F5B9FAAE7A` | `1d43b77c03d0cf851f6f36a2fe0d90638e174a18` |
| `en/02-mod-structure/03-mod-cpp.md` | **Reject** | `CEB5B1E3E8BEC93D21177A1C3D092225BB19BA0909EA02EA48F822AE52AB3506` | `6649fce42e852f9993869b73ba3d737670f3c5e5` |
| `en/02-mod-structure/04-minimum-viable-mod.md` | **Approve** | `A6209D15E139C5744B5D6A2479F9275C779FA0BF4B5610D98BA232FA38EF7C43` | `3bb56cff59b2b9e17e2279932bda56d026ee6ed8` |
| `en/02-mod-structure/05-file-organization.md` | **Approve** | `24AAAD4F0E5A522F23388891BC40393F763F27A1ADDC8C561526E59F04D3BC42` | `ae6ea80a5056e8e4ba828dab1c004f2b90457b5f` |
| `en/02-mod-structure/06-server-client-split.md` | **Reject** | `498131A57D410CEB4A65C061A26ADDFFAC8182E2E5E2166DD0E8233F9D5A5081` | `1f4c346a2eb7085d50d7042eb9cec9b7c0e95e17` |
| `en/04-file-formats/06-pbo-packing.md` | **Reject** | `42FBEB3CBA2C689CB9728EC83D9B21E55FF244EFB2E59FF122827523B727DDF9` | `69e48cda8c806453549fcf61add192154f5362a3` |
| `en/08-tutorials/07-publishing-workshop.md` | **Reject** | `141D973FB307ECB7DA39693ABDFE18D97D9D8A038B0A5A1837C802C86C844E0E` | `d7b39ad7d92364e03e82d78a1bec7883ac4fe795` |

All eight SHA-256 values match `pbo-en-implementation.md/json`.

---

## Finding dispositions

### EN-PBO-F01 — Size and limit taxonomy

**Accepted in `06-pbo-packing.md` lines 107-122.** The page correctly separates per-member `OriginalSize`/`DataSize` field width from total archive format, packer/signer, DayZ runtime, filesystem/deployment, and Workshop service boundaries. It does not turn the `u32` fields or the observed retail archive sizes into a universal 2 GiB/4 GiB ceiling.

The numeric format, tool, runtime, filesystem, and Workshop boundary matrix remains **unresolved** and must stay open.

### EN-PBO-F02 — Addon identity, launch availability, and virtual paths

**Accepted in `01-five-layers.md`, `04-minimum-viable-mod.md`, `05-file-organization.md`, and the relevant new passages of `02-config-cpp.md` and `06-pbo-packing.md`.** `requiredAddons[]` is now described as containing `CfgPatches` class names, not PBO filenames, prefixes, folders, or Workshop IDs; launch-list availability is kept separate; and `CfgMods.inputs`/`files[]` are described as mounted virtual paths. The dependency examples remain one-way and non-cyclic.

Cross-PBO mounted-path execution and missing/renamed `requiredAddons` runtime behavior remain **unresolved**.

### EN-PBO-F03 — `CfgMods.type` and the fixture disagree

**Rejected in `02-config-cpp.md`, `03-mod-cpp.md`, and `06-server-client-split.md`.** The official snapshot documents only `CfgMods.type = "mod"`; folder-level `-mod`/`-serverMod` performs routing. The unchanged accepted fixture follows that evidence: its server component uses `CfgMods.type = "mod"`, and its server `mod.cpp` has no `type` field. In contrast:

- `02-config-cpp.md:210` says the field declares `"mod"` or `"servermod"` and should match how the package ships;
- `03-mod-cpp.md:177-181` says `mod.cpp.type` declares regular versus server-only loading;
- `06-server-client-split.md:241` says `CfgMods.type` controls how the engine treats the mod, and `:1074-1075` requires `servermod` in both files.

Reconcile these pages with the evidence and linked fixture. Do not promote the undocumented `servermod` metadata value into the routing mechanism.

### EN-PBO-F04 — Folder-level server package boundary

**Partly accepted, then rejected for remaining contradictions.** The new high-level wording correctly says `-serverMod` selects a separate folder and that selective per-PBO routing inside one shared folder is undocumented. However:

- `03-mod-cpp.md:215-218` still says the package runs only on a dedicated server, clients never download it, and “No key signing required”; serverMod-only signature behavior is explicitly unresolved.
- `06-server-client-split.md:197` still says the server loads the shared mod and clients “download” it, recreating the server-streaming implication PBO-007 required removing; `:216` repeats an unqualified “never see it, never download it.”

Use the accepted narrow wording: clients must already have the shared package installed through the launcher/Workshop workflow; a separate `-serverMod` folder is not broadcast. Keep clean-client distribution and serverMod-only signature enforcement as runtime tests.

### EN-PBO-F05 — Build, signing, DSCheck, and key rotation

**Accepted in the new `06-pbo-packing.md:419-441` and `:288-352` passages and in the new `07-publishing-workshop.md:170-266,414-418` passages.** They require final naming/inspection/collision checking before signing, qualify DSCheck as a strict stdout check rather than PBO-byte or server-enforcement proof, and reuse uncompromised keys across ordinary updates while making rotation an explicit trust operation.

**Rejected at the file-set level** because `03-mod-cpp.md:218` still asserts no signing is required for server mods, while `07-publishing-workshop.md:555` says to place exactly one `.bikey` per mod. The latter is too absolute for component keys and old/new-key transition windows and conflicts with the new deliberate-rotation guidance.

### EN-PBO-F06 — Prefix collision contradiction

**Rejected in `06-pbo-packing.md`.** Line 53 says the prefix system “ensures no path collisions between mods,” but lines 427, 500, and 621 correctly treat duplicate normalized virtual paths as possible and require a conservative release failure. Replace the absolute line 53 claim with namespace/diagnostic wording that does not claim automatic collision prevention.

### EN-PBO-F07 — `-packonly` contradiction

**Rejected in `06-pbo-packing.md`.** Line 192 says a `config.cpp` containing `CfgVehicles` requires binarization, while lines 263-284 correctly say a text config can define those classes and that binarization depends on the asset/release workflow. Make the table agree with the later explanation; model/animation/texture conversion needs are separate from the mere presence of `CfgVehicles`.

### EN-PBO-F08 — Pinned public source citations

**Rejected in `06-pbo-packing.md`.** Line 615 pins five repository root trees but identifies no reviewed file, symbol, or line/range. PBO-011 explicitly required meaningful pinned examples rather than repository names alone. The hidden audit ledger cannot substitute for public page citations because VitePress excludes `.audit`; link each claim to the relevant pinned blob (or name the exact pinned path/symbol next to its commit link), and pin the official DayZ Samples citation used at line 629.

### EN-PBO-F09 — Published fixture route and hidden audit links

**Accepted for the fixture README; unresolved/rejected for the adjacent manifest link.** Installed VitePress `resolveConfig` included `examples/en/multi-pbo/README.md`, excluded every `.audit` page, and the installed Markdown renderer rewrote the page link to `./../../examples/en/multi-pbo/README.html`. All eight pages contain zero `.audit` references.

The adjacent `manifest.json` link remains a raw relative JSON URL, is not a resolved Markdown page, and has no copy under `public/`. Without a controlled build artifact proving it is emitted, do not approve that published link; either publish it from `public/`, render its content in a resolved page, or remove the direct link.

### EN-PBO-F10 — Documentation build accounting

**Accepted as honest failure accounting.** The author records three 4 GiB old-space attempts as not passed because no wrapper produced a zero exit and `.vitepress/dist/index.html` was not generated. This review confirmed that file is still absent and did not run another full build, as instructed. The final controlled-content build remains separate and pending.

---

## Evidence reopened and hash-verified

- `pbo-research.md` remained `03FE483067A9259D6C0601A2F6FF9C9C7B6601201FAB6982343A8A15582D7949`; `pbo-evidence.json` remained `38E257ED0D88E286C84E24828068B9F5C96E58F0F4B0D2375EA427ED6AFE1BBA`.
- All fourteen paths in `pbo-repair-council.json.scoped_content_sha256` matched, including fixture README `3449B09BBDD04A278A17DD8E3A79A1D27EEB76B173431A73A255C52EE23BC0CE`, runner `38F24D830DBCB7985ABF1ED9636493C5BDFEA1E160169379FE10E8F50BADB956`, and manifest `63D5E5E9468AF98B37B30AB71C3CCEA69D45694E266377025F68E6953F088582`.
- Official Modding Structure snapshot matched `4AD1DABE620A25FFF043077D012BEBAAA663953355575B3F0AB52936AADB5AFA`; server configuration snapshot matched `B2D11B4CD7D973FF65FD9804406E02D4C091176F9926EE1AF1F04142FE4142F7`.
- Official DayZ Samples checkout remained at `da5e5437c9502620d9853fb6eed14701135ab2ea`; `Test_Inputs/config.cpp` matched `71B869D713C15D38037B0B8B6CC682CCAEA03599DDFF370DA786D42CD813121C`.
- Extracted `DZ/data_sakhal/config.cpp` matched `D2074F7E019B1359A8BA00DF5ABEC5A9B459F3F4A0028A18A2D1C9CFB078FB34`.
- armake2 checkout remained at `3cc3362101900ff41504db3e780dd1625634cf94`; `src/pbo.rs` matched `BEC43AC4560626FE4B154922938D0A2BDEDB0561D68118AE822AB9C030387549`.
- Installed `DSCheckSignatures.exe` matched `9BAFBBBDCE1E2792515039F99B7150CA1CE97ADF16AAB8CFC79BDC8938A8503C`; retail `core.pbo` matched `36ECFCE1062C31EAAEDC59F23D64CEA84DD79A52482145402582EB35BC1AB043`.

The relevant source lines were reopened, not inferred from the prior councils. No full research/tool matrix was repeated because the research, evidence, and fixture bytes remained unchanged.

---

## Validation

- Exact eight-file Markdown check using the installed VitePress renderer: 0 dead file links, 0 dead anchors, 117 anchor references checked.
- Installed VitePress page resolution: 1,306 Markdown pages at review time; fixture README included; 0 `.audit` pages included.
- `git diff --check 0df58c2 -- <eight exact paths>`: exit 0; only Git line-ending notices.
- Heading rendering: no newly introduced heading/anchor defect; each file renders one document title.
- Full VitePress build: not run. Game/server/client launch: not run.

---

## Open gates preserved

- DayZ boot, Enforce compilation, mounted cross-PBO `CfgMods` paths, missing/renamed `requiredAddons`, and clean-client `-serverMod` distribution.
- `verifySignatures = 2` valid/modified/missing/wrong/rotated-key cases and serverMod-only signature behavior.
- Numeric member, total-archive, compression, packer/signer, runtime, filesystem/deployment, and Workshop boundaries.
- Workshop upload, download, update, and service-side limits.

These broad gates are not reasons to erase the accepted static improvements, but they prevent runtime/size/Workshop completion claims.
