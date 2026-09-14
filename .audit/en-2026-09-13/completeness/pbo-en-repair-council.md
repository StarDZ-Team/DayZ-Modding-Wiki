# PBO English Repair Council

**Review date:** 2026-09-13 (America/Sao_Paulo)  
**Task:** `task_bdc972e36e5b` / dispatch `ctx_2a2d33dcb9d3`  
**Baseline HEAD:** `103238a83078784b7ee6cd6486f63d7973e3fe92`  
**Decision:** **Reject the exact eight-page wording set pending two bounded repairs.** EN-PBO-F04, F05, F07, F08, and F09 are fixed, but F03 and F06 each retain one contradictory sentence. This approval decision covers documentation wording and static link/render checks only; it does not approve the fixture's unresolved functional behavior.

No English page, fixture, configuration, runtime artifact, or commit was changed. No game/tool runtime or full VitePress build was run.

---

## Exact page dispositions and identities

SHA-256 and the raw Git blob OID cover the exact worktree bytes reviewed. The normalized Git blob OID is from `git hash-object --path=<path> <path>` and applies repository clean filters; it is deliberately distinguished from the raw `git hash-object --no-filters` identity. The normalized and raw OIDs differ where line-ending filters change the byte stream.

| Page | Disposition | SHA-256 (raw worktree bytes) | Normalized Git blob | Raw Git blob |
|---|---|---|---|---|
| `en/02-mod-structure/01-five-layers.md` | **Approve; previously approved and unchanged** | `60269FB1AE83AED1D9C00BDE0AF94204ABF0056617EB16662E8ED0CC1574DA15` | `5acd4acc3227965aecfca47f7eefb5de7553af24` | `a0427e8398045579cfc27af9b3bc1178a50b490a` |
| `en/02-mod-structure/02-config-cpp.md` | **Approve** | `BDD728C3D49EA79A87AF331A7079AB8DDDC683FDC254F19A57603226F1BDDC06` | `45313abe4d250d9cc5375252f621b6567b9bcec6` | `eb174a08987b55979494e33291e9e5c6c980014c` |
| `en/02-mod-structure/03-mod-cpp.md` | **Reject** | `00855928DF3601B91AE122DFF1F018B8D5E7129B662E6FD99B1F11FC2ECAB67A` | `856e66e34a407c0a0ee3d666ea995e7ed426d389` | `b7d6a64da917dd5b6d66acd1a5c474cfc176874e` |
| `en/02-mod-structure/04-minimum-viable-mod.md` | **Approve; previously approved and unchanged** | `A6209D15E139C5744B5D6A2479F9275C779FA0BF4B5610D98BA232FA38EF7C43` | `3bb56cff59b2b9e17e2279932bda56d026ee6ed8` | `3bb56cff59b2b9e17e2279932bda56d026ee6ed8` |
| `en/02-mod-structure/05-file-organization.md` | **Approve; previously approved and unchanged** | `24AAAD4F0E5A522F23388891BC40393F763F27A1ADDC8C561526E59F04D3BC42` | `ba5ee8dd733c2111f14ee01390dec6846024fb19` | `ae6ea80a5056e8e4ba828dab1c004f2b90457b5f` |
| `en/02-mod-structure/06-server-client-split.md` | **Reject** | `56151172A2744AF937B95DE2A2029E621321D32045D281BD10D1047715C12AE3` | `b32a34bc6e9412c00485f4c33df9480539aedc4a` | `5ddcda5a253d83d98ef7924ad1e52500e08dcb82` |
| `en/04-file-formats/06-pbo-packing.md` | **Approve for wording only** | `3756718C2343029369BB7E5647E6793DE836F6EF90964C74B41C308D57637D09` | `9c86cfec10b3cec6972499943cecefe8868c43db` | `5199702268d144293654b2bdae110ac0dc437dfd` |
| `en/08-tutorials/07-publishing-workshop.md` | **Approve for wording only** | `EA30075E8121EE03ECEF71F84EA2C5623EA687B03ECE9671EBD9B09C7B136CEF` | `41457260c5ed3b6bbc9ba80b957d4c719a24cf14` | `fb92dc3fea896ebe78d63d4282eddc1bb1ac782c` |

The three formerly approved pages match the final-council SHA-256 and raw blob identities exactly. Their normalized OIDs are newly reported here and are not interchangeable with the raw-byte identities recorded by the earlier council.

---

## Finding dispositions

### EN-PBO-F03 — not fully fixed

The examples and most prose now correctly use documented `CfgMods.type = "mod"`, omit `mod.cpp.type`, and assign folder routing to `-mod=`/`-serverMod=`. The fixture agrees: `examples/en/multi-pbo/src/Server/config.cpp:12-26` uses `type = "mod"`, while `examples/en/multi-pbo/package/Server/mod.cpp` contains no `type` field.

However, `en/02-mod-structure/06-server-client-split.md:229` still says the `CfgMods` type field “controls how the engine treats the mod internally.” That positive behavior claim contradicts lines 242-242, which correctly say only `"mod"` is documented, native behavior is not established, and launch flags perform routing.

**Actionable repair:** replace line 229 with neutral documented-syntax wording, for example: “Inside `config.cpp`, `CfgMods` also contains a `type` field; Bohemia's published example marks `type = \"mod\"` required, but the reviewed sources do not establish another value or a routing behavior for the field.”

### EN-PBO-F04 — fixed statically; runtime remains open

The five repaired pages no longer say that `-mod=` streams a package from the server, that every server package runs only on a dedicated server, or that a `-serverMod` PBO categorically needs no signing. They consistently say clients already need the shared package installed, `-serverMod` selects a separate server-side folder that official documentation calls not broadcast, and clean-client distribution remains a test.

### EN-PBO-F05 — fixed statically; enforcement remains open

The no-signing and exactly-one-public-key absolutes are gone. The pages require signing final distributed shared/client PBO bytes, scope acceptance to server configuration, treat DSCheck as a strict stdout build check rather than byte-pair/server proof, permit component keys and an old/new rotation window, and reuse an available uncompromised key for ordinary updates. ServerMod-only enforcement and the `verifySignatures = 2` matrix remain explicitly unresolved.

### EN-PBO-F06 — not fully fixed

`en/04-file-formats/06-pbo-packing.md:53,426,499,620` now consistently treats prefixes as a virtual namespace and normalized duplicate paths as a conservative release failure, without claiming the engine prevents collisions or establishing a winning archive.

However, `en/02-mod-structure/03-mod-cpp.md:513` still says “only `CfgPatches` class names in `config.cpp` can collide.” That absolute contradicts the corrected PBO page and the retained local inventory showing duplicate normalized virtual members can exist.

**Actionable repair:** limit the sentence to presentation metadata and acknowledge both namespaces, for example: “Identical `mod.cpp` presentation values do not create load-order conflicts; separately, duplicate `CfgPatches` names and duplicate mounted virtual paths can collide.”

### EN-PBO-F07 — fixed

`en/04-file-formats/06-pbo-packing.md:185-193,260-283` now states that text `config.cpp` can contain `CfgVehicles` and separates config binarization from model, animation, and texture conversion. The mere presence of `CfgVehicles` no longer forces binarization.

### EN-PBO-F08 — fixed

`en/04-file-formats/06-pbo-packing.md:614,628` now links pinned blobs rather than repository roots and names the reviewed files/symbols. Independent local reopen confirmed the cited commits and contents:

- official DayZ Samples `da5e5437c9502620d9853fb6eed14701135ab2ea`, `Test_Inputs/config.cpp:1-33`, SHA-256 `71B869D713C15D38037B0B8B6CC682CCAEA03599DDFF370DA786D42CD813121C` (`CfgPatches`, `CfgMods`, `inputs`, and script-module `files[]`);
- Community Framework `0763e7e7548c9a0bed6626afff835de80693ebf3`, `JM/CF/GUI/config.cpp`, SHA-256 `3AA877B37DE71F381C7DD04D9A7DBB23761621A7BA9D85798528F1B1AA36F3D0`, and `JM/CF/Scripts/config.cpp`, SHA-256 `8DA49AD88AB7387B4F5E6D5D2FDBC07005F908B537E7F723152BD41B6BDD1D41`;
- Community Online Tools `41f2c2b99565d0e3970163e162efbf1283fdca62`, `JM/COT/Scripts/config.cpp`, SHA-256 `BD536BE5FB6E4053F8879D82779C8FE952FD95081F24B088D2C11BCC46EE2382`;
- DayZ Expansion Scripts `6dacd00f6d943ebbd99e0cf1baad93f470d96419`, `DayZExpansion/Core/Scripts/config.cpp`, SHA-256 `8973F7648357EF6B1FFA70F0E8168915052674F412EB15B7090E6E38B41826EA`;
- DayZ Editor `992e6b29b42b5d8e609632b59771335a23d205eb`, `DayZEditor/Scripts/config.cpp`, SHA-256 `1B0D5EC71A26F8B73BFBC2156CE303F65028C0CF6AFB09416AFA84F49A1BA39A`, and `DayZEditor/GUI/config.cpp`, SHA-256 `39952D741DC3075102A923D93D24B74A63EBA0DD04DA7D1FECB8B1C225DC7447`;
- VPP Admin Tools `dc22e420df3b54e821055f9764da1e48f4a31e71`, root `config.cpp`, SHA-256 `39BD991B0E0CF043BAD82EF5D8F4C8FFCF9538D6E4E41C7B3CB81EC5A89E9061`.

These projects support the page's limited statement that real projects choose different config/addon layouts; the page correctly labels them implementation examples rather than engine contracts.

### EN-PBO-F09 — fixed

The only published fixture link is `../../examples/en/multi-pbo/README.md`; no direct Markdown link to `manifest.json` and no `.audit` reference remains in the eight pages. Installed VitePress `resolveConfig` includes `examples/en/multi-pbo/README.md`, excludes `.audit` pages, and the renderer rewrites the link to `./../../examples/en/multi-pbo/README.html`.

The new runtime report does not justify a runtime-verified claim. The PBO page correctly limits the fixture to static packaging/tool output at line 440 and explicitly excludes DayZ boot, Enforce compilation, mounted `CfgMods` resolution, distribution, dependency behavior, signature enforcement, size limits, and Workshop behavior.

---

## Primary evidence independently reopened

- Official DayZ Modding Structure snapshot: `D:/StarDZ/docs/DayZ/Modding Structure.md`, SHA-256 `4AD1DABE620A25FFF043077D012BEBAAA663953355575B3F0AB52936AADB5AFA`, especially lines 6-14 and 20-91. It documents `-mod`, folder contents, `CfgPatches`, only `CfgMods.type = "mod"`, and virtual module/input paths; it does not document `"servermod"` metadata.
- Official DayZ Server Configuration snapshot: `C:/Users/Leonardo Mello/AppData/Local/Temp/wiki-audit-20260911/BIKI-Server-council-20260913.txt`, SHA-256 `B2D11B4CD7D973FF65FD9804406E02D4C091176F9926EE1AF1F04142FE4142F7`, lines 180-181. It describes `-mod` and folder-level `-serverMod`, with the latter “not broadcasted to clients.”
- Official-tool extraction: `D:/DayZ Projects/DZ/data_sakhal/config.cpp`, SHA-256 `D2074F7E019B1359A8BA00DF5ABEC5A9B459F3F4A0028A18A2D1C9CFB078FB34`, lines 1-30. It shows `CfgPatches.requiredAddons`, `CfgMods.type = "mod"`, and a mounted `DZ/data_sakhal/scripts/4_World` path. The extraction has no immutable build receipt and is static evidence only.
- Exact fixture: server config SHA-256 `4FA89581708F159CFCA491252F494A5E9A6A1AE003D165370EA3F12F5245E102`; server `mod.cpp` SHA-256 `726A2E560854E619DD2A851F5E9EA08D216D673278452CC8C6C5AE449C1DC2C8`; README SHA-256 `3449B09BBDD04A278A17DD8E3A79A1D27EEB76B173431A73A255C52EE23BC0CE`; manifest SHA-256 `63D5E5E9468AF98B37B30AB71C3CCEA69D45694E266377025F68E6953F088582`.
- `.audit/en-2026-09-13/completeness/multi-pbo-runtime.md` was reopened as contrary runtime evidence. DayZDiag mounted the four PBOs but the independent Mission probe could not resolve `PBOExample` or `PBOExampleServer`, so there are no function, server-component, or data-sentinel success markers. This council approves no functional result.

---

## Scoped validation

- Exact eight-file installed-renderer check: 8 pages, one `h1` each, 143 local references inspected, 117 anchor references checked, 0 dead file links, and 0 dead anchors.
- Fresh VitePress route check: fixture README included; 0 `.audit` pages included; fixture href rendered as `./../../examples/en/multi-pbo/README.html`; no direct manifest link present.
- `git diff --check HEAD -- <eight exact paths>`: exit 0; Git emitted line-ending conversion notices only.
- Scoped contradiction scan: no remaining client-stream/download claim, categorical serverMod signing claim, exactly-one-key rule, `type = "servermod"` example, `CfgVehicles`-requires-binarization rule, raw manifest link, or repository-root-tree citation in the repaired text. The two contradictory sentences identified above remain the only bounded F03-F09 wording residuals found.

No full build or runtime was performed by instruction.

---

## Approval boundary and preserved open gates

Even after the two wording repairs, final approval would remain **wording-only**. The runtime report leaves the fixture classes unresolved. DayZ boot/Enforce compilation, mounted cross-PBO paths, missing/renamed `requiredAddons`, clean-client distribution, `verifySignatures = 2` cases, serverMod-only signature behavior, numeric member/archive/tool/runtime/deployment limits, and Workshop upload/download/update behavior remain open and must not be represented as verified.
