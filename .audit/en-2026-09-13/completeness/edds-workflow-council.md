# EDDS workflow independent council review

**Reviewed:** 2026-09-14 America/Sao_Paulo  
**Inputs:** `edds-workflow-research.md` SHA-256 `BF36CB2AEDC876184FA22DD17ACC5F06494F6198F3F979383CC2DA9F19D4C3AD`; `edds-workflow-research.json` SHA-256 `60E5B03A5F8F7D5268D50B96F3625DC4FBB0C8715CB0BDA51765A0598FCD7B2E`  
**Disposition:** **Returned with repairs; not ready to execute.**

This council independently reopened the relevant local binaries, extracted assets/scripts, pinned public repositories, and third-party writer code. It performed no conversion, packing, Workbench/GUI, game, server, client, build, install, or commit. All 24 research source hashes and all eight third-party inspected-file hashes matched.

---

## Decisions

| Finding | Decision | Reason and boundary |
|---|---|---|
| EW-01 — Workbench conversion | Accepted, bounded | Installed DayZ Workbench `1.29.163.401` contains the reported import/resource-class strings; extracted metadata and public source/output/meta triples corroborate the model. Menu behavior, defaults, emitted bytes, and success remain unobserved. |
| EW-02 — generated identity | Accepted with repair | Never infer or transplant a GUID. Reforger's indexed documentation supports copied `{GUID}path` identities, but DayZ **Copy Resource Name(s)** and GUID necessity are unproven. Pinned Dabs Framework uses a plain EDDS path. |
| EW-03 — EDDS structure | Accepted with repair | Generic DDS samples do not reproduce the observed `ENF1` and mip-table structure, so rename-only is not an evidence-backed recipe. No native DayZ rejection was tested, and the table is not universally at `0x80`. |
| EW-04 — PAA tools | Accepted | ImageToPAA strings, BinMake rules, TexConvert configuration, and indexed official text establish PAA/PAC support, not an identified EDDS command. This is an evidence boundary, not universal impossibility. |
| EW-05 — third-party writer | Accepted | Inspected tests establish same-library parsing/round trips, not DayZ rendering; the packer emits no Workbench metadata or allocated GUID. Keep it behind a passing Workbench baseline. |

Cross-cutting issues remain unresolved: `.edds.meta` runtime necessity, plain-path runtime viability, DayZ's generated-resource-name behavior, Workbench defaults, conversion, and client rendering. Include generated metadata in the baseline as a conservative control, not as a claimed runtime requirement. Do not imply the experiment passed.

---

## Dispositive reopened evidence

- `workbenchApp.exe`, SHA-256 `B61D240394845EF9EAB3B5F459D487B50DBF3C42713FB9E9E50CE945F5A894C6`, has raw file/product version `1.29.163.401`, a valid Bohemia signature, and the strings `Register resource and import`, `Reimport`, `Resource manager`, `PNGResourceClass`, `TGAResourceClass`, and `DDSResourceClass`. `Copy Resource Name(s)` was not found in the ASCII scan.
- Steam's local manifest reports app `2909700`, build `23909709`, and depot manifest `8240607442694517654`. This is installation provenance, not a conversion receipt.
- `dayz.gproj`, SHA-256 `269DAAD629D0007176B4B81ADFB52740A23A11955C24C414B82727F15EE41928`, maps Workdrive `P:/` but contains local StarDZ entries. `P:` and `P:/EDDSProbe` are currently absent, so the exact project/source mount is a concrete prerequisite.
- The `D:/DayZ Projects` census found 454 EDDS files: all 454 had `DDS ` and `ENF1`; 433 legacy-header files had a `COPY`/`LZ4 ` table at `0x80`, while 21 DX10-header files placed it at `0x94`. The author's four selected `0x80` examples are accurate but not universal.
- The same corpus has 437 `.edds.meta` files, while 17 EDDS files lack a sibling metadata file in the extraction. This extraction records provenance but cannot prove runtime metadata requirements.
- `bleedingdrops.edds.meta`, SHA-256 `70615CD8100AA1C2D823A67DA4B79DFC0E6AEDC5885685872F1BB5F3847925DD`, names source GUID `FEAD63B1347867F9`; its imageset, SHA-256 `D153C931D28560C50D5DE645D59E6AEAC6F88B2EBC4CB4FCA1E98A75E5CC5A19`, references EDDS GUID `35363C01F72D2EBE`. The output identity cannot be inferred from that metadata name.
- Pinned Dabs Framework `fd859fd891f45a4a9c9089597db0c621ef3a9de5` uses plain `DabsFramework\GUI\icons\brands.edds` at `brands.imageset:7` (SHA-256 `1DE25A2BA41771632814F126C2C326B5D8A2F1DF74BEA2344CF56120081D101D`) and registers its image sets at `Scripts/config.cpp:27-37` (SHA-256 `74E0CC3791ADD0F6F7E650162B3BD96D2F8188A9F130209965AAE00E26D372D1`). This is public implementation evidence, not this council's runtime proof.
- `enwidgets.c`, SHA-256 `6BB20A54119A25BAB3933607BF8B703C3123853B36BF2E4141AEAC83CF215C9E`, exposes `CreateWidgets:176-182`, documented boolean `LoadImageFile:247-257`, `SetImage:262-267`, and `SOURCEALPHA`/`BLEND` flags at `57-84`. These support a deterministic fixture and show why alpha acceptance must account for widget state.
- Installed ImageToPAA SHA-256 `0B786037FC708931BCC85088BA69648BCF57463BCF3B1D3A21A35F29B9C2344A`, BinMake rules SHA-256 `916287C273749B5FA4F682005847D0425187BB60EE791B2E79B6D5FCFB595DD6`, and TexConvert configuration SHA-256 `066202E8D7F7D30449FF192AD338AE42C04947515D93DBAB41D2D82004C8753E` did not expose an EDDS recipe. `workbenchapi.c:1-17`, SHA-256 `24931BEBAC51AFD59DC35216AE98FC6AD75C2271909A79936872DD14E41DD6A36`, exposes editor controls but no identified texture import/register API; do not fabricate one.
- `WoozyMasta/edds` commit `55a8e8620d444edf81d8e5aaf0bf671aa0bde20d` writes the observed marker/table design; `imageset-packer` commit `3e70e3df55e7a142112298dfc6a61a90ee6b346a` delegates to it and emits a plain path. Their inspected tests and corpus claim do not establish DayZ client rendering.

On 2026-09-14, official Bohemia search-index text was read for Reforger Resource Manager/Textures/File Types/Metadata, ImageToPAA, and DayZ Workbench Script Debugging. Direct opens returned HTTP 403, so the pages were not treated as fully opened prose. Reforger material is sibling-product evidence; the DayZ Expansion guide is third-party corroboration only.

---

## Exact repairs and execution gate

1. Mount and record the exact project/source root exposing `P:/EDDSProbe`; hash the selected `.gproj` and record the Workbench executable/version/hash.
2. Replace “generic DDS rename is rejected” with “the reviewed generic DDS samples are structurally different, so rename-only is not a controlled recipe; DayZ runtime behavior was not tested.” Inspect the block table after the effective DDS header: `0x80` for reviewed legacy headers, `0x94` for DX10.
3. Keep the original source-generated 64x32 RGBA fixture and one default import attempt. Retain logs, settings, and before/after hashes. Treat metadata class, compression, mips, and generated identity as observations, not expected values to force.
4. Use an exact EDDS resource name if DayZ exposes one. Otherwise use `EDDSProbe/GUI/imagesets/probe_ui.edds` as the predeclared plain-path hypothesis for the same single attempt; record that this does not test GUID identity. Never mint a GUID.
5. Provide one standalone client PBO with prefix `EDDSProbe`, no CF/third-party dependency, and exact `CfgPatches`, `CfgMods`, imageset registration, `Game`/`World`/`Mission` dependencies, justified `requiredAddons`, and `missionScriptModule.files[] = {"EDDSProbe/Scripts/5_Mission"}`.
6. Use a deterministic `modded MissionGameplay.OnInit()` after `super.OnInit()` to create `EDDSProbe/GUI/layouts/probe_ui.layout`, null-guard the root and both `ImageWidget`s, log unique create/load tokens and both `LoadImageFile` booleans, then call `SetImage(0)`. Inspect the packed table for every expected virtual path before launch.
7. Set widget color to `1 1 1 1`, use blend with source alpha, and render the half-alpha cyan region across known contrasting backgrounds. Retain lossless pixel evidence plus the opaque magenta control. Report preserved translucency, orientation, and channels; do not claim exact alpha 128 from unaided screenshot inspection.

Make one default import and one baseline client run, with at most one rerun for an objectively identified packaging/reference defect. Do not test generic DDS, metadata/GUID omission, alternate compression, or third-party bytes before the baseline passes.

**Gate:** after these textual repairs and the project-mount receipt, the evidence is sufficient to implement one bounded experiment. It is not sufficient to claim Workbench conversion, generated identity, metadata necessity, plain-path viability, or client rendering has passed.

The JSON companion is `edds-workflow-council.json`, SHA-256 `BCBCF80450889F4C81A21EEB42F62A56BC13B3778374E6AF14FBB711E08E2E31`; it records the same decisions, gate, concise evidence receipt, and hash-audit counts.
