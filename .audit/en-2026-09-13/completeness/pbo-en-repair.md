# PBO English Bounded Repair

**Date:** 2026-09-13  
**Task:** `task_90601a45da66` / dispatch `ctx_9861a62e7c11`  
**Baseline HEAD:** `103238a83078784b7ee6cd6486f63d7973e3fe92`  
**Evidence record root:** `.audit/en-2026-09-13/completeness`  
**Result:** Implemented the exact EN-PBO-F03 through EN-PBO-F09 repairs in the five rejected English pages. No configuration, public asset, fixture, approved English page, or commit was changed.

---

## Repair Dispositions

| Finding | Repair |
|---|---|
| EN-PBO-F03 | `CfgMods.type` now uses the only documented value, `"mod"`, in shared and separately launched server-package examples. The pages identify `mod.cpp.type` and `"servermod"` metadata as undocumented and make `-mod=`/`-serverMod=` folder routing authoritative. |
| EN-PBO-F04 | Removed implications that a server streams shared mods, that every server package runs only on a dedicated server, and that a `-serverMod` package needs no signing. Clients must already have shared packages installed; separate server folders are not broadcast; clean-client distribution and serverMod-only signatures remain runtime tests. |
| EN-PBO-F05 | Replaced the exactly-one-`.bikey` rule with an explicit configured-trust rule that allows component keys and an old/new-key transition window. Ordinary updates reuse an available uncompromised key; old keys leave only after the supported transition and dependency scope ends. |
| EN-PBO-F06 | Replaced automatic collision-prevention wording with virtual-namespace diagnostic wording and a conservative normalized-path collision check. |
| EN-PBO-F07 | The `-packonly` table now says text `config.cpp` can contain `CfgVehicles`; asset conversion and release workflow determine binarization. |
| EN-PBO-F08 | Replaced repository-root citations with pinned blob links naming reviewed config files, `CfgPatches`/`CfgMods` symbols, and relevant line ranges for CF, COT, Expansion, DayZ Editor, VPP, and official DayZ Samples. |
| EN-PBO-F09 | Removed the raw published `manifest.json` link. The resolved fixture README remains linked and explains the local manifest and invocation route. |

---

## Exact Content Identities

SHA-256 is over exact worktree bytes. The normalized Git blob OID uses repository clean filters (`git hash-object --path=<path> <path>`); the raw blob OID uses `git hash-object --no-filters`.

| File | SHA-256 | Normalized Git blob | Raw Git blob |
|---|---|---|---|
| `en/02-mod-structure/02-config-cpp.md` | `BDD728C3D49EA79A87AF331A7079AB8DDDC683FDC254F19A57603226F1BDDC06` | `45313abe4d250d9cc5375252f621b6567b9bcec6` | `eb174a08987b55979494e33291e9e5c6c980014c` |
| `en/02-mod-structure/03-mod-cpp.md` | `00855928DF3601B91AE122DFF1F018B8D5E7129B662E6FD99B1F11FC2ECAB67A` | `856e66e34a407c0a0ee3d666ea995e7ed426d389` | `b7d6a64da917dd5b6d66acd1a5c474cfc176874e` |
| `en/02-mod-structure/06-server-client-split.md` | `56151172A2744AF937B95DE2A2029E621321D32045D281BD10D1047715C12AE3` | `b32a34bc6e9412c00485f4c33df9480539aedc4a` | `5ddcda5a253d83d98ef7924ad1e52500e08dcb82` |
| `en/04-file-formats/06-pbo-packing.md` | `3756718C2343029369BB7E5647E6793DE836F6EF90964C74B41C308D57637D09` | `9c86cfec10b3cec6972499943cecefe8868c43db` | `5199702268d144293654b2bdae110ac0dc437dfd` |
| `en/08-tutorials/07-publishing-workshop.md` | `EA30075E8121EE03ECEF71F84EA2C5623EA687B03ECE9671EBD9B09C7B136CEF` | `41457260c5ed3b6bbc9ba80b957d4c719a24cf14` | `fb92dc3fea896ebe78d63d4282eddc1bb1ac782c` |

The three approved pages stayed byte-identical to the final-council identities:

| File | SHA-256 | Raw Git blob |
|---|---|---|
| `en/02-mod-structure/01-five-layers.md` | `60269FB1AE83AED1D9C00BDE0AF94204ABF0056617EB16662E8ED0CC1574DA15` | `a0427e8398045579cfc27af9b3bc1178a50b490a` |
| `en/02-mod-structure/04-minimum-viable-mod.md` | `A6209D15E139C5744B5D6A2479F9275C779FA0BF4B5610D98BA232FA38EF7C43` | `3bb56cff59b2b9e17e2279932bda56d026ee6ed8` |
| `en/02-mod-structure/05-file-organization.md` | `24AAAD4F0E5A522F23388891BC40393F763F27A1ADDC8C561526E59F04D3BC42` | `ae6ea80a5056e8e4ba828dab1c004f2b90457b5f` |

---

## Reopened Source Mapping

The repair reused the accepted evidence in `pbo-research.md`, `pbo-evidence.json`, and `pbo-en-final-council.md/json`; it did not repeat the broader research. The precise cached files below were reopened on 2026-09-13.

| Repair | Evidence reopened |
|---|---|
| Folder routing and `CfgMods.type` | Official DayZ Modding Structure snapshot, `D:/StarDZ/docs/DayZ/Modding Structure.md`, SHA-256 `4AD1DABE620A25FFF043077D012BEBAAA663953355575B3F0AB52936AADB5AFA`, lines 6-14 and 37-85; official DayZ Server Configuration snapshot, `BIKI-Server-council-20260913.txt`, SHA-256 `B2D11B4CD7D973FF65FD9804406E02D4C091176F9926EE1AF1F04142FE4142F7`, lines 180-181. |
| Pinned official sample citation | DayZ Samples commit `da5e5437c9502620d9853fb6eed14701135ab2ea`, `Test_Inputs/config.cpp` lines 1-33, symbols `CfgPatches`, `CfgMods.inputs`, and `class defs`, SHA-256 `71B869D713C15D38037B0B8B6CC682CCAEA03599DDFF370DA786D42CD813121C`. |
| Pinned third-party layout examples | CF commit `0763e7e7548c9a0bed6626afff835de80693ebf3`, `JM/CF/GUI/config.cpp` and `JM/CF/Scripts/config.cpp`; COT commit `41f2c2b99565d0e3970163e162efbf1283fdca62`, `JM/COT/Scripts/config.cpp`; Expansion commit `6dacd00f6d943ebbd99e0cf1baad93f470d96419`, `DayZExpansion/Core/Scripts/config.cpp`; DayZ Editor commit `992e6b29b42b5d8e609632b59771335a23d205eb`, `DayZEditor/Scripts/config.cpp` and `DayZEditor/GUI/config.cpp`; VPP commit `dc22e420df3b54e821055f9764da1e48f4a31e71`, root `config.cpp`. Each page link now points to the pinned blob and names the relevant `CfgPatches`/`CfgMods` symbol. |
| Key trust and rotation scope | Accepted PBO-010 evidence and wording in `pbo-research.md`, including the official cross-game signing reference qualified by DayZ server/tool evidence. No new enforcement claim was added. |
| Collision and `-packonly` contradictions | Accepted PBO-005/PBO-006/PBO-007 reasoning and installed-tool observations already recorded in `pbo-research.md` and `pbo-evidence.json`; no tool was rerun. |

Third-party projects remain implementation examples, not engine contracts.

---

## Validation

- Installed VitePress renderer/config loaded successfully under Node `v24.14.0`.
- Five repaired pages render exactly one `h1`; the three approved pages also still render exactly one `h1`.
- Renderer-based local-link validation checked 377 local references, including 363 anchor references: 0 missing destinations and 0 missing anchors.
- VitePress page resolution includes `examples/en/multi-pbo/README.md`; the fixture link renders to `./../../examples/en/multi-pbo/README.html`; zero `.audit` pages are in the resolved page set; no direct manifest link remains.
- `git diff --check 0df58c20761f654cd91ece04d9469be4b1728c6b -- <five owned EN paths>` exited 0, with only Git's CRLF conversion notices.
- Scoped contradiction scan found no exactly-one-key rule, no no-signing-required claim, no client-download/streaming claim, no automatic collision-prevention claim, no `CfgVehicles`-requires-binarization row, no raw manifest link, and no pinned repository-root tree link in the five pages.
- No full VitePress build, game/client/server launch, PBO tool run, fixture modification, or build retry was performed by instruction.

---

## Unresolved Tests Preserved

- DayZ boot and Enforce compilation for the example packages.
- Cross-PBO mounted `CfgMods` paths and missing/renamed `requiredAddons` behavior.
- Clean-client `-serverMod` distribution in the target launcher/Workshop workflow.
- `verifySignatures = 2` valid, modified, missing-signature, wrong-key, and rotated-key cases, including serverMod-only signature behavior; DSCheck remains only a strict stdout build check.
- Numeric member, total-archive, compression, packer/signer, runtime, filesystem/deployment, and Workshop boundaries.
- Workshop upload, download, update, and service-side limits.

These open gates prevent runtime, signature-enforcement, numeric-limit, and Workshop-completion claims; they do not undo the bounded static repairs above.
