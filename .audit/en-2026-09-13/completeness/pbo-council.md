# Independent Council Review: PBO Limits and Multi-PBO Packaging

**Review date:** 2026-09-13  
**Role:** independent reviewer; no English wiki edits  
**Author artifacts reviewed:** `pbo-research.md` SHA-256 `D0FE639B64A588109F633F8634D4A2466048A825D62E566FA120A1064D480BCF`; `pbo-evidence.json` SHA-256 `2C9D44E0F21FE5E22D59B56F055693ECC75B6EF5A57A36DFB19D18A2CCFF8A15`  
**Repository state reviewed:** branch `wiki-reorg`, HEAD `aa75472098d73db6b3c19b046438e530efc290f9`  
**Decision:** conditional acceptance. Six findings are supported as proposed; six require the exact revisions below. The proposed multi-PBO example is not yet an implementation-ready, end-to-end build.

---

## Executive decision

The research correctly rejects a universal 2 GiB or 4 GiB PBO claim: the reviewed reverse-engineered format describes unsigned 32-bit **member** size fields, not a single total-archive-size field, and no current authoritative DayZ source reviewed here supplies a total-PBO ceiling. That is not evidence that no engine, tool, distribution, or platform limit exists. The local greater-than-2-GiB report remains a useful historical lead, but its failing bytes, logs, and version receipt were not retained, so it cannot support a numeric wiki limit.

The package/archive/prefix/addon taxonomy, folder-level `-serverMod` boundary, virtual-path explanation, and `requiredAddons` initialization role are substantially supported. Required corrections remain for one-to-one PBO/addon wording, collision policy, the build/sign/verify workflow, cross-PBO path claims, signature verification, and source accounting.

Two author-accounting statements failed independent checking:

- `pbo-research.md:28` names `en/02-mod-structure/01-mod-overview.md`, which does not exist. The actual first page is `en/02-mod-structure/01-five-layers.md`.
- The `BIKI-SERVER` snapshot hash recorded in `pbo-evidence.json` is `B2D11EDE...0813997`; the actual file at the recorded path hashes to `B2D11B4CD7D973FF65FD9804406E02D4C091176F9926EE1AF1F04142FE4142F7`. Its relevant content supports the cited claims, but the receipt is invalid until repaired.

All other recorded source-file hashes and every recorded child-file hash in the pinned repositories were recomputed and matched. Repository origin and pinned HEAD also matched for DayZ Samples, Community Framework, Community Online Tools, VPP Admin Tools, DayZ Expansion Scripts, DayZ Editor, and armake2.

---

## Per-finding dispositions

### PBO-001 — Approved as written

Accept the proposed correction provided the page labels the layout as unofficial reverse engineering rather than a supported DayZ format contract. The reviewed layout has five 32-bit member fields; `OriginalSize` and `DataSize` are member sizes, while `Offset` is described as unused/reserved. Member payloads follow the header contiguously.

Evidence reopened: BIKI PBO File Format and Generic File Format Types, retail `dta/core.pbo`, and armake2 `src/pbo.rs` at commit `3cc3362101900ff41504db3e780dd1625634cf94`.

### PBO-002 — Approved as written

Accept the limit taxonomy and the refusal to publish 2 GiB or 4 GiB as a universal total-PBO ceiling. Use this exact safety sentence:

> The reviewed reverse-engineered layout can represent unsigned 32-bit sizes for individual members, up to 4,294,967,295 as a field-width fact. It does not establish a usable maximum member size or a maximum total PBO size. No current authoritative DayZ source reviewed here defines a total-PBO ceiling; engine, tool, distribution, and Workshop limits remain separate questions.

The current retail observation was reproduced: DayZ `1.29.0.163709`, Steam build `24689949`, 117 `Addons/*.pbo` files, 21,638,391,975 aggregate bytes, largest `structures_data.pbo` at 1,216,702,399 bytes. This is an observation, not a limit.

The local documentation claims a clean 1,471,395,178-byte PBO and an `ACCESS_VIOLATION` at 2,165,383,988 bytes, and separately reports a greater-than-4-GiB corruption symptom. No retained failing PBO, log, minidump, or immutable build receipt was found. Keep it as an unresolved project-specific lead; do not infer a signed-int boundary or a universal ceiling.

### PBO-003 — Approved as written

Accept the distinction between a format marker and current tool UI/CLI. `Cprs` appears in the unofficial format description; installed Addon Builder `1.0.240639` and the installed FileBank help expose no compression switch. Do not turn that version-specific negative observation into a claim about all packers or all DayZ versions.

### PBO-004 — Revision required

The four-name model is useful, but a physical PBO and a `CfgPatches` identity are not necessarily one-to-one. Official cross-game documentation permits additional configuration roots to define additional addon identities, while the current retail install also contains resource PBOs without a root `config.cpp`/`config.bin`. Replace the proposal with:

> A mod-folder launch name, physical PBO filename, virtual prefix, and configuration-addon identity are different names. `requiredAddons[]` refers to `CfgPatches` class names, not PBO filenames, prefixes, or mod folders, and controls addon/configuration initialization dependencies. Give every independently load-ordered configuration addon a unique `CfgPatches` class. Do not assert one `CfgPatches` identity per physical PBO: a PBO can expose additional configuration roots, and shipping resource PBOs can be observed without a root config. Treat those observations as evidence of engine content layout, not as a documented public-mod contract.

> `CfgMods` registers script modules, input mappings, and their mounted virtual paths. Its `dependencies[]` values in official examples are module labels; do not use that array as a substitute for `CfgPatches.requiredAddons[]` or as a physical-PBO dependency declaration.

The proposed Core and Scripts `config.cpp` fragments were parsed successfully by the installed `CfgConvert.exe`, but parsing proves only syntax. The fragments do not constitute a complete four-PBO mod and do not verify cross-PBO resolution at runtime.

### PBO-005 — Revision required

The two local rifle PBOs do share prefix `StarDZ_Weapons\Data\Weapons\Rifles\` and overlap at `config.cpp` and `texHeaders.bin`; the latter has different stored sizes. No controlled client/server test established which bytes win. Replace the absolute rule with this explicit project policy:

> Sharing a prefix is not itself a dependency mechanism or proof of an error. As a release policy, normalize virtual paths case-insensitively across all PBOs and fail on duplicate paths by default. Permit a duplicate only through a documented allowlist backed by a controlled runtime test for the supported DayZ build; never rely on textual launch order to choose a winner.

This is a conservative CI policy, not a demonstrated engine requirement that same-prefix PBOs must always have disjoint paths. Generated `texHeaders.bin` and zero-length `config.cpp` entries need deliberate handling rather than silent exclusion.

### PBO-006 — Revision required

The proposed workflow is directionally correct but is not runnable as delivered. The council experiment found that Addon Builder can exit zero after fatal missing-tool messages and create no PBO, and that its output used the source-directory name rather than a requested final component name. Replace the workflow with:

> Build each component from a separate source root with separate temporary and output directories. Invoke Addon Builder with a validated `-toolsDirectory` or explicit dependency-tool paths, capture its log, reject `FATAL`/`ERROR`, and require exactly one newly created PBO. Discover that output, rename it to the manifest's final filename, and inspect the final PBO's prefix and member table with an independent reader. Scan normalized virtual paths across the whole release, hash the final PBO, sign those final bytes, require the expected `.bisign`, and record the manifest, tool hashes, command line, output hashes, and inspection results.

> Do not treat process exit code alone as success. Do not sign before a final rename or modification. `DSCheckSignatures checked_dir keys_dir` can validate that a `.bisign` is accepted under an available public key in this installed build, but it did not bind the neighboring PBO bytes in the council experiment and returned exit code zero even when the key was missing. Capture and interpret stdout, and reserve end-to-end content enforcement claims for a clean `verifySignatures=2` server join.

Implementation acceptance requires a real script or exact commands, not prose: include a component manifest, four source trees/configs, unique temp/output locations, explicit installed tool paths, output discovery/rename, BankRev inspection, normalized collision scan, final-byte signing, stdout-aware checks, and artifact receipts. The current proposal supplies only Core/Scripts config fragments and no buildable Data/Server components.

### PBO-007 — Approved as written, with runtime gate retained

Official server documentation describes `-mod` and `-serverMod` as loading mod folders/subfolders, with `-serverMod` content not broadcast to clients. No reviewed official source documents selective server-only routing of individual PBOs within one shared mod folder. Accept folder/package granularity and keep the clean-client distribution/join test outstanding.

### PBO-008 — Revision required

Accept the virtual-path correction, but qualify cross-PBO supply. Use:

> `CfgMods.inputs` and each script module `files[]` entry name mounted virtual paths, not paths relative to the physical PBO root. Official samples use full virtual paths such as `Test_Inputs/inputs.xml` and `Test_Inputs/scripts/...`. A path may be authored in one configuration and supplied from another archive only if the final mounted namespace resolves it; validate that cross-PBO arrangement in the packaged runtime instead of presenting it as proven by syntax alone.

### PBO-009 — Approved as written

Accept the narrow correction: launch arguments make mod folders available, while `CfgPatches.requiredAddons[]` declares addon/configuration initialization dependencies. Do not use textual `-mod` order as a substitute. Keep the claim narrow; this review does not establish that command-line order is irrelevant to every other subsystem.

### PBO-010 — Revision required

Key reuse and final-byte signing are supported, but the proposed static-check claim and rotation reasons are incomplete. Replace with:

> Sign every distributed final PBO after its last byte-changing operation. Keep the private key out of the release and distribute the public `.bikey` to servers. Reuse an uncompromised, available key across ordinary updates; rotate after compromise, loss/unavailability of the private key, or an intentional trust reset. Rotation requires servers to install the new public key.

> Installed `DSSignFile` reports signature version 3 as its default and `-v2` as an option. This is unrelated to the server setting `verifySignatures=2`. In this council experiment, `DSCheckSignatures` accepted an old `.bisign` next to a newly rebuilt PBO and returned zero even for a missing public key, so document it only as a narrow signature/key check whose stdout must be interpreted—not as proof that adjacent PBO bytes match. Prove actual release enforcement with controlled `verifySignatures=2` joins using valid, modified, missing-signature, and wrong-key cases.

Whether content loaded only through `-serverMod` is operationally signature-checked remains a runtime question. Do not state a universal answer without the pending server test.

### PBO-011 — Revision required

The pinned repository commits and all recorded child-file hashes were independently verified. However, source accounting must be repaired before implementation:

- replace the nonexistent `en/02-mod-structure/01-mod-overview.md` read claim with the actual file/read scope, `en/02-mod-structure/01-five-layers.md` if that is what was read;
- correct the `BIKI-SERVER` snapshot SHA-256 to `B2D11B4CD7D973FF65FD9804406E02D4C091176F9926EE1AF1F04142FE4142F7` or regenerate and identify a different immutable snapshot;
- add explicit pinned-path bullets for DayZ Editor and VPP if their IDs remain evidence for this finding, or remove those IDs from the finding; and
- identify the local checkout path for each pinned repository in the durable record, not only a remote URL and relative child path.

The actual reopened implementations support examples of separate GUI/Scripts identities and `requiredAddons` chains, but they remain third-party design choices, not independent proof of engine rules. CF's deployment script uses Mikero MakePbo rather than the installed Addon Builder, so it cannot validate Addon Builder naming or exit behavior.

### PBO-012 — Approved as written

Accept the separation of Workshop service behavior from PBO format and engine loading. The reviewed current Steamworks implementation page documents content-folder submission/update APIs but supplies no fixed DayZ item-content ceiling. Say that no ceiling was found on that reviewed page; do not say Steam or DayZ has no service/app-specific limit.

---

## Isolated tool experiment

The experiment is retained under `TEMP/pbo-council`; no game was launched.

1. `AddonBuilder.exe <source> <output> -packonly -clear -prefix=PBOCouncil\Scripts\` used a stale registered tools location, logged fatal missing Binarize/CfgConvert/DSSignFile/FileBank errors, exited `0`, and created no PBO.
2. Adding `-toolsDirectory=D:\SteamLibrary\steamapps\common\DayZ Experimental Tools` produced `ComponentSource.pbo`. BankRev showed prefix `PBOCouncil\Scripts\`. The output name followed the source folder, so a manifest-driven rename was necessary.
3. `CfgConvert.exe -bin -dst <output> <config.cpp>` parsed both proposed Core and Scripts snippets successfully. This validates syntax only.
4. `DSCreateKey PBOCouncilTest`, then `DSSignFile <private-key> MyMod_Scripts.pbo`, produced a `.bikey` and `.bisign`; the PBO hash did not change during signing.
5. `DSCheckSignatures <release> <keys>` printed `Signature ... is OK` for the signed release. After rebuilding the PBO to different bytes and placing the old `.bisign` beside it, the tool still printed `Signature ... is OK` and exited `0`. Re-signing the rebuilt bytes produced a different `.bisign` hash. An empty keys directory printed `Key not found...` and still exited `0`; an orphan `.bisign` produced no useful output and exited `0`.

These observations are installed-tool behavior, not engine behavior. They justify strict artifact/log inspection and show that this DSCheck invocation is not an end-to-end substitute for a server join.

---

## Sources reopened

### Official and primary-adjacent web sources

- Bohemia Interactive Community Wiki, [PBO File Format](https://community.bistudio.com/wiki/PBO_File_Format) and [Generic File Format Data Types](https://community.bistudio.com/wiki/Generic_File_Format_Data_Types), accessed 2026-09-13. The PBO page explicitly labels the description unofficial/undocumented.
- Bohemia Interactive Community Wiki, [Addon Builder](https://community.bistudio.com/wiki/Addon_Builder?oldid=341605), [DayZ Modding Basics](https://community.bistudio.com/wiki/DayZ:Modding_Basics), [DayZ Modding Structure](https://community.bistudio.com/wiki/DayZ:Modding_Structure), [CfgPatches](https://community.bistudio.com/wiki/CfgPatches), [DayZ Server Configuration](https://community.bistudio.com/wiki/DayZ:Server_Configuration), and [Arma 3: Creating an Addon](https://community.bistudio.com/wiki/Arma_3:_Creating_an_Addon), accessed 2026-09-13. Direct BIKI requests intermittently returned HTTP 403, so indexed current pages and the identified local snapshots were reopened together with installed tools and code; cross-game pages are identified as such.
- Valve, [Steam Workshop Implementation Guide](https://partner.steamgames.com/doc/features/workshop/implementation), accessed 2026-09-13.

### Installed game, official tools, extraction, and official sample

- DayZ `1.29.0.163709`, Steam build `24689949`; retail `dta/core.pbo` SHA-256 `36ECFCE1062C31EAAEDC59F23D64CEA84DD79A52482145402582EB35BC1AB043`; current `Addons` inventory reproduced.
- Addon Builder SHA-256 `C113DE9CAB5E91D27CA0630E360DB0A3ECA190EC797E1DCAD9CDFA70466B45E1`; FileBank `F89AAEB22421B9158FBBF173F75D52B6F3DE69986CB462E58956C78DA82C4CAF`; DSCreateKey `81A100EEB190FAB4492970D0E6F051DB5C025BF8A4ADC2815C57ED9FE3022067`; DSSignFile `098F28B46BFE40AD4CF5C60DD3E570E984FE74AE423090B6D3F2DA8D7C4E1E78`; DSCheckSignatures `9BAFBBBDCE1E2792515039F99B7150CA1CE97ADF16AAB8CFC79BDC8938A8503C`.
- Extracted `D:/DayZ Projects/scripts/config.cpp` SHA-256 `F086DB66CDE5E60089C78FF170AA0488F5ABF7ABB37E6C13D404116D6D05A90A` and `D:/DayZ Projects/DZ/data_sakhal/config.cpp` `D2074F7E019B1359A8BA00DF5ABEC5A9B459F3F4A0028A18A2D1C9CFB078FB34`; extraction/build provenance remains incomplete.
- DayZ Samples commit `da5e5437c9502620d9853fb6eed14701135ab2ea`, with all three recorded child hashes matched.

### Pinned third-party code and local sources

- armake2 `3cc3362101900ff41504db3e780dd1625634cf94`; CF `0763e7e7548c9a0bed6626afff835de80693ebf3`; COT `41f2c2b99565d0e3970163e162efbf1283fdca62`; VPP `dc22e420df3b54e821055f9764da1e48f4a31e71`; Expansion Scripts `6dacd00f6d943ebbd99e0cf1baad93f470d96419`; DayZ Editor `992e6b29b42b5d8e609632b59771335a23d205eb`. Origins, pinned HEADs, and every author-recorded child-file hash matched.
- `D:/StarDZ/dev.py` SHA-256 `E6862C2AB958B734B5A95B6FD3A0BA6B9B3AA066069188804A4BB2A0C23CC64F`; local Core client/server configs matched the recorded hashes.
- Rifle PBOs SHA-256 `EB78111710486405344A55FA8C00E3061D2CA9990CEF250969C40A66B84E2DD8` and `C385E6DBB96C09FC6C1175317BB00EADB94915E039AA71A8F2C5B1EEFDF50FAD`; prefix/member claims reproduced.
- Local reference documents were reopened and hash-matched: `REFERENCIA_LIMITES_E_MUROS.md` `726033DB...EA18EA0`, `REFERENCIA_TIPOS_DE_ARQUIVO.md` `BCC70BBA...FAD1C1`, `REFERENCIA_VERSOES_E_MIGRACAO.md` `E3BBC9D5...7EFCD`, `GUIA_FERRAMENTAS_E_BUILD.md` `2ECAC825...367D9`, `GUIA_DEBUG_E_PERFORMANCE.md` `86D3AD63...03835`, `DAYZ_MOD_ARCHITECTURE_PATTERNS.md` `315C4C07...7B5B`, and `REFERENCE_MODS_DEEP_STUDY.md` `4EBFE019...6F91`. They were treated as non-authoritative leads. A fresh current retail scan found 11 root-configless PBOs, not the 16 stated in the local build guide.

---

## Implementation acceptance criteria

Do not implement the twelve repairs until the source-accounting errors and the six required wording/workflow revisions are applied to the delivery. An implementation is acceptable only when it:

1. preserves the reverse-engineered/status and absence-of-evidence qualifications;
2. does not publish 2 GiB or 4 GiB as a universal ceiling;
3. distinguishes mod folder, PBO, prefix, and config-addon identity without claiming a one-to-one mapping;
4. presents duplicate-path rejection as an explicit conservative release policy;
5. provides an actually runnable isolated four-component build with a manifest and source trees for Core, Scripts, Data, and Server;
6. validates output existence, logs, final name, prefix, members, normalized collisions, hashes, final-byte signing, and expected stdout rather than exit codes alone;
7. documents DSCheck's observed limitation and reserves enforcement claims for runtime tests;
8. keeps third-party patterns labeled as examples and records URL, pinned commit, checkout path, file path/range, hash, and access/review date; and
9. receives an independent final-diff review after author repairs.

No VitePress build was needed because this council changed no wiki content. Config syntax checks and packaging/signature experiments are not Enforce compilation or game/server validation.

---

## Runtime-dependent tests still outstanding

- Controlled PBO boundary matrix around the reported 2-GiB region, with exact DayZ/tool build, retained bytes, packer logs, client/server RPTs, and crash artifact; separate member-size and total-archive-size variables.
- Duplicate virtual-path winner test across PBO name/order, launch order, and supported DayZ build, including `config.cpp` and generated `texHeaders.bin` cases.
- Packaged cross-PBO `CfgMods.inputs`/`files[]` resolution test.
- `requiredAddons` missing/renamed dependency and initialization-order test for the proposed component graph.
- Clean-client `-serverMod` distribution/join test at folder granularity.
- `verifySignatures=2` matrix: valid final PBO, changed PBO with old signature, missing signature, wrong key, rotated key, and ordinary update under reused key.
- Determine whether PBOs loaded only through `-serverMod` are checked operationally in the target server configuration.
- Current DayZ Workshop upload/update test, including any app-specific service ceiling and client download behavior.

