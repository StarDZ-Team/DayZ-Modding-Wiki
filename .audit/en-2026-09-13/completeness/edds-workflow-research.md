# EDDS creation workflow research

**Observed:** 2026-09-14 America/Sao_Paulo  
**Wiki revision:** `7dd37924983a71a7835c5a926b9cd7b284a84a3d`  
**Scope:** source-first research only. No EN/locale edit, conversion, Workbench/game/client/server launch, pack, build, install, or commit was performed.

## Outcome

The best-supported DayZ path is **source PNG or TGA inside the mounted Workbench source tree -> DayZ Workbench Resource Browser -> `Register resource and import` -> sibling `.edds` plus `.edds.meta` -> copy the generated EDDS resource name -> reference that whole value from the `.imageset`**. This is an implementable experiment, not yet a locally reproduced conversion receipt: the installed DayZ Experimental Workbench binary contains the exact action text and `PNGResourceClass`, `TGAResourceClass`, and `DDSResourceClass`; extracted DayZ and pinned public mods contain matching source/output/meta triples; and a DayZ Expansion workflow independently gives the same UI action. No current DayZ-specific official page found in this pass documents the conversion dialog or a command-line resource compiler.

The installed `ImageToPAA.exe`, TexView/ImageToPAA documentation, and BinMake rules support the Real Virtuality PAA/PAC pipeline, **not an EDDS output recipe**. A generic DDS rename is rejected: reviewed EDDS files are extended containers with `ENF1` in the DDS reserved area and a per-mipmap `COPY`/`LZ4 ` block table. A new third-party packer writes this structure, but it creates no `.edds.meta`/GUID and its tests establish self-round-trip and parsing of a claimed Workbench corpus, not DayZ client rendering.

## Accepted findings

### EW-01 — Workbench is the primary conversion hypothesis

- Installed tool: `D:/SteamLibrary/steamapps/common/DayZ Experimental Tools/Bin/Workbench/workbenchApp.exe`, file version `1.29.163.401`, SHA-256 `B61D240394845EF9EAB3B5F459D487B50DBF3C42713FB9E9E50CE945F5A894C6`.
- Steam receipt: app `2909700`, build `23909709`, depot manifest `8240607442694517654`; manifest `LastUpdated=1782962909`.
- Read-only binary-string inspection found `Register resource and import`, `Reimport`, `Resource manager`, `PNGResourceClass`, `TGAResourceClass`, and `DDSResourceClass` in that exact DayZ Workbench executable.
- Extracted `D:/DayZ Projects` contains 437 `.edds.meta` files: 316 `TGAResourceClass/.tga`, 96 `DDSResourceClass/.dds`, 24 `PNGResourceClass/.png`, and one anomalous `PNGResourceClass/.tga`. The 197 GUI metadata files no longer have their source siblings in the extraction, so the extraction proves recorded provenance, not a rerunnable source checkout.
- Extracted GUI examples show the expected shape. `dayz_gui.edds.meta` names `TGAResourceClass PC`, `SourceFile "dayz_gui.tga"`, `FormatCompress Copy`, and `TiledTexture 0`; `map2d_ui.edds.meta` names `PNGResourceClass PC` and `SourceFile "Map2D_UI.png"`.
- Pinned public-mod triples corroborate the path: VPP has `vpp_icons.tga`, `vpp_icons.edds`, `vpp_icons.edds.meta`, and an imageset at commit `dc22e420...`; DayZ Editor has source `Sauce/ImageSets/dayz_editor_gui.tga` plus output/meta/imageset at commit `992e6b2...`; CF has `cf_icon.edds` and metadata recording `cf_icon.tga` at commit `0763e7e...`. These are implementation examples, not authoritative tool documentation or runtime receipts from this pass.
- The DayZ Expansion community workflow says to place a TGA in the desired directory and right-click `Register Resource and import` in DayZ Tools Workbench. This corroborates the installed binary but is not an official Bohemia source.

**Boundary:** because this task prohibited launching Workbench, the exact menu visibility, dialog defaults, console messages, and bytes produced by build `23909709` remain to be observed.

Pinned public code actually opened:

| Repository and commit | Opened paths/symbols | What it establishes |
|---|---|---|
| VPP Admin Tools `dc22e420df3b54e821055f9764da1e48f4a31e71` | `GUI/Textures/vpp_icons.{tga,edds,edds.meta,imageset}`; layout consumers | Source/output/meta coexistence, GUID-prefixed imageset reference, real consumption. Its `DesignSystem.md:233-234` says to “re-convert” after atlas generation but supplies no converter; the referenced `tools/build_ui_atlas.py` is absent at this commit. |
| Expansion `6dacd00f6d943ebbd99e0cf1baad93f470d96419` | `Core/Scripts/config.cpp:12-56`; `Core/GUI/imagesets/expansion_gui.imageset:1-26`; `GUI/layouts/expansion_loading.layout:48-75` | `CfgMods` registration, GUID-prefixed EDDS resource, and layout consumption; repository does not supply the EDDS/source/meta triple for that atlas. |
| DayZ Editor `992e6b29b42b5d8e609632b59771335a23d205eb` | `Scripts/config.cpp:10-37`; `GUI/imagesets/dayz_editor_gui.{imageset,edds,edds.meta}`; `Sauce/ImageSets/dayz_editor_gui.tga` | Source-art-to-output provenance plus registration/descriptor. |
| Community Framework `0763e7e7548c9a0bed6626afff835de80693ebf3` | `JM/CF/GUI/textures/cf_icon.{edds,edds.meta}`; `JM/CF/Workbench/dayz.gproj:14-28` | TGA provenance and Workbench project resource-list context; no converter command. |

### EW-02 — Preserve and copy the generated resource identity; do not infer it

Official Enfusion Resource Manager documentation for Arma Reforger says registration creates `.meta`, import converts source files to Enfusion outputs including `.edds`, and **Copy Resource Name(s)** yields `{GUID}path/to/file.ext`. That is the correct model, but it is from a later/sibling Enfusion product and is used only as a hypothesis for the DayZ observation.

Do not derive the imageset GUID from the `.edds.meta` text alone. Most extracted pairs match, but `bleedingdrops.imageset` references `{35363C01F72D2EBE}Gui/imagesets/BleedingDrops.edds` while `bleedingdrops.edds.meta` has `Name "{FEAD63B1347867F9}Gui/imagesets/BleedingDrops.png"`. The output experiment must select the generated `.edds` in the DayZ Resource Browser and copy its resource name; if that action is absent, record the exact UI and stop rather than minting a GUID.

### EW-03 — EDDS is extended DDS, not a suffix convention

`dayz_gui.edds`, VPP `vpp_icons.edds`, DayZ Editor `dayz_editor_gui.edds`, and the StarDZ beta `PixelMask_White.edds` all have:

- `DDS ` magic at offset `0x00`;
- `ENF1` at offset `0x24` inside the DDS reserved words;
- a table beginning at offset `0x80`, with one `COPY` or `LZ4 ` entry per mip before payloads.

This directly rejects “standard DDS plus a renamed extension” as a recipe. It still does not by itself prove runtime acceptance of every EDDS writer.

### EW-04 — ImageToPAA/TexView/Pal2PacE do not establish EDDS creation

- Installed `ImageToPAA.exe` version `1.0.0.5`, SHA-256 `0B786037FC708931BCC85088BA69648BCF57463BCF3B1D3A21A35F29B9C2344A`, reports itself as `pal2pace` for `-?`, `--help`, and `-help`; its only printed option is `-size=<n>`.
- Installed `BinMake/binMakeRules.txt` has TGA/PNG/GIF -> PAA/PAC/BI rules through ImageToPAA and no `.edds` destination rule.
- Installed `TexConvert.cfg` describes PAA-oriented suffix compression and channel transforms; it is not an EDDS resource manifest.
- The official ImageToPAA page is categorized for Arma 3 and lists PAA/PAC/TGA/PNG output, not EDDS. It says ImageToPAA and TexView 2 share the conversion engine.
- No `Pal2PacE.exe` was found in the installed DayZ Experimental Tools tree; `Pal2Pac.dll` exists under Object Builder. Absence of an executable is not proof that no internal component can create EDDS, only that no supported Pal2PacE EDDS command was identified here.

Therefore the current EN boundary—use these tools only for its PAA workflow—is retained.

### EW-05 — Third-party writer is a candidate, not the baseline

Pinned for inspection under disposable `TEMP/edds-workflow-research/`:

- `WoozyMasta/edds` `v0.4.0`, commit `55a8e8620d444edf81d8e5aaf0bf671aa0bde20d`. `format.go` writes `ENF1`; `write.go` writes a reverse-ordered mip table and `COPY`/`LZ4 ` bodies. Its corpus README says the fixtures were created by Workbench, while its tests parse those fixtures and round-trip files written by the same library.
- `WoozyMasta/imageset-packer` `v0.1.3`, commit `3e70e3df55e7a142112298dfc6a61a90ee6b346a`. `pack.go` emits `.imageset` and `.edds`; `imageio/write.go` delegates EDDS writing to `WoozyMasta/edds`. It emits a plain virtual path from `--edds-path`, and does not emit `.edds.meta` or a GUID.

The advertised command is concrete—e.g. `imageset-packer pack ./icons ./out -F bgra8 -x 1 -P EDDSProbe/GUI/imagesets`—but it was not run because this task prohibited installs/conversions. Its own `TestWriteWithOptionsEDDSCompressed` only writes an 8x8 file and reads its configuration back using the same EDDS library. It belongs in a later A/B only after the Workbench-produced fixture renders.

## Rejected findings

| Claim | Disposition | Reason |
|---|---|---|
| Rename a DirectXTex/generic `.dds` to `.edds` | Rejected | Generic DDS lacks the observed `ENF1` marker and EDDS block table; a DDS header alone is insufficient. |
| Use ImageToPAA, TexView, or Pal2PacE to make GUI EDDS | Rejected as unsupported | Installed help/rules and official ImageToPAA output list establish PAA/PAC, not EDDS. |
| Hand-write `.edds.meta` and invent/reuse a GUID | Rejected | Registration semantics and GUID allocation were not reproduced; extracted metadata names can even point at the source rather than the EDDS GUID consumed by an imageset. |
| Treat `.edds.meta` as proven runtime-required PBO content | Rejected as unproven | Public mods ship it, but no pack/client A/B in this pass establishes whether runtime needs it. Include it in the first fixture to preserve provenance, then test omission separately only if useful. |
| Promote `imageset-packer` as production-ready DayZ conversion | Rejected pending client evidence | It implements the observed container and has tests, but no inspected receipt proves DayZ pack/client render, and it omits Workbench registration metadata/GUID. |
| Claim Workbench automatically creates the `.imageset` | Rejected | The established action concerns texture registration/import. The `.imageset` remains a separate descriptor unless the DayZ UI exposes and successfully runs an Image Set Generator, which was not observed. |

## Unresolved findings

1. DayZ Workbench build `23909709` menu/dialog behavior and default texture import profile for an unsuffixed GUI PNG.
2. Exact generated `.edds.meta` `Name`, GUID behavior, `ChangeDate`, compression, mip count, and whether **Copy Resource Name(s)** is present on the DayZ EDDS output.
3. Whether `.edds.meta` must be packed for runtime, or only retained beside source/output for Workbench provenance and reimport.
4. Whether registration is stable when the source tree is outside `P:/` but included by another `.gproj` `FileSystemPathClass`.
5. Whether DayZ Workbench provides an externally supported resource-compiler command/API. No such command was found; `workbenchapi.c` covers editor/plugin control but no texture-import API was identified in the relevant local documentation.
6. Exact client behavior of the third-party writer and plain (non-GUID) imageset texture paths.

## Minimal conversion and render experiment

This is the next authorized observation, not a claim that it has passed.

### A. Original-art conversion fixture

Create `P:/EDDSProbe/GUI/imagesets/probe_ui.png` as an original **64x32 RGBA8** image:

- transparent canvas;
- left cell (`0..31,0..31`): an opaque white asymmetric `L`, vertical bar `x=4..11,y=4..27`, horizontal bar `x=4..27,y=20..27`;
- right cell (`32..63,0..31`): a cyan square `x=36..59,y=4..27` at alpha 128, with an opaque magenta 4x4 marker at its top-right.

The two cells expose vertical flips, rectangle mistakes, lost alpha, and color-channel swaps without copying stock art. Record the PNG SHA-256 and a screenshot from the source editor.

1. Snapshot the directory listing and hashes.
2. Start installed DayZ Experimental Workbench `1.29.163.401` with the mounted source data/project that exposes `P:/EDDSProbe`.
3. In Resource Browser, select `probe_ui.png`, right-click **Register resource and import**, accept defaults once, and save the console log.
4. Record every created/changed file, byte length, SHA-256, timestamp, and the import-settings screenshot. Expected candidates are retained `probe_ui.png`, new `probe_ui.edds`, and new `probe_ui.edds.meta`.
5. Select the generated `.edds` (not the PNG or metadata text) and use **Copy Resource Name(s)** if available. Record the exact clipboard value. Never transplant an example GUID.
6. Inspect without modifying: the EDDS must have `DDS ` at `0x00`, `ENF1` at `0x24`, sane `64x32` dimensions, at least one mip, and a complete `COPY`/`LZ4 ` table. The metadata should identify `PNGResourceClass PC` and `SourceFile "probe_ui.png"`; record deviations rather than editing it.

**Conversion success:** Workbench reports a successful import, produces an openable 64x32 EDDS with the structural markers, produces registration metadata, and exposes an exact resource name for the EDDS.  
**Conversion failure:** the action is absent/disabled, the import log reports an error, no EDDS is created, the output is malformed, or the output cannot be opened in Workbench.  
**Stopping condition:** make one default import attempt. If it fails, capture the log and inspect the one visible import-settings/resource-registration screen; do not cycle formats, extensions, compression profiles, or hand-authored metadata. Return to source research with the exact error.

### B. Descriptor, pack, and client render

Only after A succeeds, create a minimal `EDDSProbe` client mod with PBO prefix `EDDSProbe`:

- `GUI/imagesets/probe_ui.edds` and its generated `.meta` unchanged;
- `GUI/imagesets/probe_ui.imageset` with internal `Name "edds_probe"`, `RefSize 64 32`, one `mpix 1` texture whose `path` is the **exact copied EDDS resource name**, images `left_l` at `Pos 0 0 Size 32 32` and `alpha_marker` at `Pos 32 0 Size 32 32`, and an empty `Groups {}`;
- `CfgMods > defs > imageSets > files[] = {"EDDSProbe/GUI/imagesets/probe_ui.imageset"};`;
- a client-only layout/script that creates two 64x64 `ImageWidget`s, calls `LoadImageFile(0, "set:edds_probe image:left_l")` and `LoadImageFile(0, "set:edds_probe image:alpha_marker")`, records each boolean, calls `SetImage(0)`, and leaves both widgets untinted on a dark panel.

Pack once using the existing normal mod packer with the established prefix; do not ask Binarize/ImageToPAA to convert the EDDS. Inspect the PBO table before launch and require the exact virtual paths for `.edds`, `.edds.meta`, `.imageset`, config, layout, and script. Launch the matching diagnostic client with only required dependencies and this probe.

**Render success markers:** config/script load without relevant errors; both `LoadImageFile` calls return true; no `RESOURCES (E)` names the probe; the white L is upright; the second sprite retains 50% cyan transparency and its opaque magenta marker at top-right; screenshot, RPT, script log, launch command, PBO hash/table, and source/output hashes are retained.  
**Failure markers:** false return, missing-resource/config error, blank/error texture, wrong sprite rectangle, flip, channel swap, alpha loss, or a PBO path/reference mismatch.  
**Stopping condition:** diagnose path/prefix and exact resource-name mismatch first. Perform at most one corrected rerun for an objective packaging/reference defect. Do not test generic DDS, GUID removal, metadata removal, alternate compression, or third-party output until the Workbench baseline passes; if the baseline still fails, preserve evidence and return to council.

### C. Optional later third-party A/B

After B passes, replace only the EDDS bytes with `imageset-packer v0.1.3` BGRA8/one-mip output generated from the same PNG, keeping the descriptor, virtual path, and all other files fixed. A matching successful render would validate that writer for this bounded fixture; a failure would not prove all third-party EDDS generation impossible. Stop after this single controlled A/B.

## Local corpus actually read

| Source | Sections/files read | Use |
|---|---|---|
| `imageset-followup-council.md/json`; `imageset-en-closeout.json` | full | prior decisions and remaining EDDS gate |
| `D:/StarDZ/docs/DAYZ_GUI_REFERENCE.md` | lines 80-115, 180-210, 1350-1385 | layout/image reference context |
| `D:/StarDZ/docs/GUIA_FERRAMENTAS_E_BUILD.md` | lines 30-110, 180-210, 270-330, 515-595 | installed tool roles, gproj, ImageToPAA/BinMake evidence |
| `D:/StarDZ/docs/REFERENCIA_TIPOS_DE_ARQUIVO.md` | lines 1-125, 327-370, 480-510 | EDDS/meta/imageset claims and unresolved metadata requirement |
| `D:/StarDZ/docs/STARDZ_ICON_PIPELINE_SPEC.md` | embedded production-pipeline and adversarial-verification sections | fallible texconv/rename proposal and its later rejection |
| Current EN | targeted EDDS/imageset/workbench passages | confirmed the recipe is explicitly withheld |
| Installed DayZ Experimental Tools | manifest, Workbench/ImageToPAA version/hash/strings, BinMake rules, TexConvert config | exact local tool capability boundary |
| `D:/DayZ Projects/gui/imagesets` | directory, all metadata files, selected imagesets/EDDS headers | extracted source/output metadata and GUID counterexample |
| Pinned VPP/Expansion/Editor/CF | imagesets, configs/gproj, selected source/output/meta and consumer paths | real implementation shape; no runtime inference |
| `WoozyMasta/edds` and `imageset-packer` | README, go.mod, format/write/block, pack/convert/image-write and tests/corpus provenance | third-party implementation and test boundary |

## Internet access record

Access date: 2026-09-14.

- Official Bohemia search-index text was read for [ImageToPAA](https://community.bohemia.net/wiki/ImageToPAA), [Arma Reforger Resource Manager](https://community.bohemia.net/wiki/Arma_Reforger%3AResource_Manager), [File Types](https://community.bohemia.net/wiki/Arma_Reforger%3AFile_Types), [Textures](https://community.bohemia.net/wiki/Arma_Reforger%3ATextures), and [DayZ Workbench Script Debugging](https://community.bohemia.net/wiki/DayZ%3AWorkbench_Script_Debugging). Direct opens returned HTTP 403 for four pages; the Textures open timed out with HTTP 400. These endpoints were not retried or treated as directly opened prose.
- The official Reforger pages are sibling-engine evidence, not proof that DayZ exposes identical UI/defaults.
- The pinned third-party source was downloaded from `https://github.com/WoozyMasta/edds.git` and `https://github.com/WoozyMasta/imageset-packer.git`; exact commits are recorded above.
- A DayZ Expansion workflow page was found via search and used only as third-party corroboration for the exact menu action.

## Selected source hashes

| Path | SHA-256 |
|---|---|
| `.audit/.../imageset-followup-council.md` | `F30633F89111AC8EE594AD8A05E089847FDDD71B10D3E450CC571F2CF43B1BCF` |
| `.audit/.../imageset-followup-council.json` | `11AFD261C4E501BEE5618765962B8ECD1DFD07FFCBE8188598F2E4DF7DE65D29` |
| `.audit/.../imageset-en-closeout.json` | `27001B3B9460A28F94C86E1AD19636A2150F64050AD1F4EA14A60DC7C6D2199E` |
| `D:/StarDZ/docs/DAYZ_GUI_REFERENCE.md` | `F83CD7E9843AAD1001B36E40883E3FF876FE645489C958DBFD83067A35AB9063` |
| `D:/StarDZ/docs/GUIA_FERRAMENTAS_E_BUILD.md` | `2ECAC825A7CC0995A2A97F5040CA26291A484E2CB5F5E42EBCC0195C5E9367D9` |
| `D:/StarDZ/docs/REFERENCIA_TIPOS_DE_ARQUIVO.md` | `BCC70BBA5733111C8EF513A1B2A2735A9B9D71C5A282B1D70CC86643ECFAD1C1` |
| `D:/StarDZ/docs/STARDZ_ICON_PIPELINE_SPEC.md` | `592AAE1BE64F883704353C1FF14A922E0CBDAF30A8C992277C3E7AC1B83D9347` |
| `D:/DayZ Projects/gui/imagesets/dayz_gui.edds` | `243EEE81BE40A3C4E03FBDBDA8AEAFFAE2759AF42B3051C831A940F60E4C96ED` |
| `D:/DayZ Projects/gui/imagesets/dayz_gui.edds.meta` | `29DE0F1413360C1833E698CB681CB99A70ECFB0A22BFB6897A1524CCD741DEDE` |
| `D:/DayZ Projects/gui/imagesets/dayz_gui.imageset` | `AD001B5391F351FFDC68CBB39B685D16E21F5313862C251CB48A65241FA1095A` |
| VPP `vpp_icons.tga` / `.edds` / `.meta` / `.imageset` | `EA4CF06F...` / `BF92B942...` / `203E7399...` / `C80AE154...` |
| Editor source TGA / output EDDS / metadata | `E00B42A7...` / `FEE86854...` / `78DCB9C1...` |
| Expansion config / imageset / consuming layout | `8973F764...` / `F598C874...` / `88D29E0A...` |
| Editor config / imageset | `1B0D5EC7...` / `DD9A882D...` |
| CF gproj / icon metadata | `B9198EDD...` / `5E0698C3...` |
| `WoozyMasta/edds` `format.go` / `write.go` / `edds_test.go` | `89EB5486...` / `41399AA0...` / `5EAE13D8...` |
| `imageset-packer` README / `pack.go` / `imageio/write.go` / test | `2F571CE4...` / `E149FDA2...` / `6B4021E8...` / `6A4B9358...` |

Abbreviated hashes in the last four rows are expanded in the JSON companion.
