# Independent assets evidence council

**Observed:** 2026-09-13 America/Sao_Paulo (`2026-09-14T02:11:28Z`)  
**Wiki revision at final evidence check:** `5714990e98d67ee4782bb5be85aa9b5519ae6462`  
**Reviewed delivery:** `assets-evidence.md` SHA-256 `B1D893256493528304C699E457AD727D1AA19E7772679A63E2962C3E9777EAC9`; `assets-evidence.json` SHA-256 `0F5EB0C2E76A70383EA00B3ABA87550CB49C5B1E88A45BE352CA320B38333BF7`.

## Council outcome

The delivery's two correction directions are technically sound, but none of its replacement blocks should be copied verbatim. The imageset replacement is approved with a small reader-facing edit. The model paragraph and callout are approved in substance with revised wording; the proposed table rows are rejected because fixture-specific byte counts make a general reference table less useful and risk implying a stable size relationship.

This review independently reopened the cited extraction files, both pinned repositories, the relevant local documentation, installed-tool help and rules, both retained PBOs, and both retained extraction trees. It then extracted the retained PBOs again and repeated both Addon Builder paths under `TEMP/assets-council`. No DayZ, DayZ Diag, server, or game runtime was launched.

## Decision 1: brace imagesets versus XML and performance

**Claim:** `AGUI-DC-007`, `en/03-gui-system/07-styles-fonts.md:530`, page SHA-256 `95909F8CE4B19D4F9364915653FE33361557A56D97E8C3DE87E40C2D7522C5C7`.

**Verdict:** approve the correction; revise the proposed wording.

The extraction contains 11 `.imageset` files and all 11 start with `ImageSetClass {`. `dayz_gui.imageset:1-14` directly shows the brace-delimited structure. `LoadWidgetImageSet(string filename)` at `enwidgets.c:692` documents only a filename-taking native call: it says nothing about XML, functional equivalence, parsing work, timing, caching, GPU residency, or batching. The pinned Community Framework project lists brace-format vanilla resources, but it is a third-party project definition and not an engine benchmark.

The author's proposed replacement correctly withdraws XML and speed assertions. Its phrase “the reviewed sources” is audit-facing, so use this reader-facing text instead:

> | Imageset resource format | Extracted vanilla `.imageset` files use brace-delimited `ImageSetClass` syntax | Use this format for DayZ imagesets. XML loader support and any parsing-speed difference are unverified. |

This is an uncertainty statement, not an engine rejection claim. The absence of XML in the inspected extraction does not prove that a native loader rejects XML.

## Decision 2: MLOD, ODOL, and `model.cfg`

**Claim:** `AGUI-DC-010`, `en/04-file-formats/02-models.md:39,55-60`, page SHA-256 `D847E646348E3F763DCFB3655CC76AB2FA1FCCC4B8DA24C052004529D59A124E`.

### Introductory bullet

**Verdict:** approve the correction; revise the proposed wording.

The official DayZ Samples checkout is clean at commit `da5e5437c9502620d9853fb6eed14701135ab2ea`. Its `Test_Building/sample_building.p3d` is an 871,437-byte MLOD and is byte-identical to the fixture input. Installed `binMakeRules.txt:5-10` routes `.p3d` to `binarize.exe`. These facts establish the authoring-to-binarized pipeline, not current retail MLOD compatibility or a universal size/load-speed ordering.

Use:

> - **Binarized vs. unbinarized:** Object Builder uses editable MLOD P3D files. Binarize converts them to ODOL for distribution. Current retail loading of MLOD from a packed PBO is not established, and no universal MLOD-versus-ODOL size or loading-speed rule has been demonstrated.

This avoids making the current official-web search excerpt carry more weight than it can. The indexed Binarize page describes output suitable for fast engine loading, but direct page and API access were unavailable; in any event it is not a comparative DayZ benchmark.

### Comparison table

**Verdict:** reject the proposed replacement rows; replace them with general wording.

The author's exact byte counts are accurate for the retained fixture, but a reference table should not present one model's measurements as the main description of either format. Use:

> | File size | Depends on the model | Depends on the model |  
> | Load behavior | Loading from a packed PBO in current retail DayZ is unverified | Intended as the engine-ready distribution format; no comparative benchmark is available |  
> | Pipeline role | Editable authoring source | Binarized distribution output |

### Packaging callout

**Verdict:** approve the technical conclusion; revise the proposed wording.

Installed Addon Builder `-help` explicitly says that `-packonly` only stores the folder and does not binarize files, while binarization is the default. The retained pack-only PBO contains `config.cpp`, `model.cfg`, and an MLOD identical to the input. The retained binarized PBO contains `config.bin` and ODOL, with no separate `model.cfg`; the saved DayZ “Doors on buildings” page at lines 25-28 independently says model configuration is baked into P3D during binarization.

Use:

> **Important:** `-packonly` stores source files without binarizing them, so an included MLOD remains MLOD and `model.cfg` remains a separate source file. With binarization enabled, Addon Builder processes MLOD as ODOL, compiles `config.cpp` to `config.bin`, and consumes `model.cfg` into the model output instead of packing it separately. Packing success alone does not prove that current retail DayZ loads MLOD. Use binarized output for release builds unless you have version-matched runtime evidence for a different workflow.

The first sentence deliberately says “included”: Addon Builder include/exclude rules can affect which source files enter any particular PBO.

## Retained artifact hash chain

The retained chain was independently verified as follows:

| Stage | Bytes | SHA-256 | Direct observation |
|---|---:|---|---|
| Official Samples `Test_Building/sample_building.p3d` | 871,437 | `42BFBC79AB47252B6DB69EF206F595D03B7A4F67F2C43F90FD6DB7DD07FF2427` | `MLOD`; clean pinned checkout |
| Fixture input P3D | 871,437 | `42BFBC79AB47252B6DB69EF206F595D03B7A4F67F2C43F90FD6DB7DD07FF2427` | Byte-identical to official sample |
| Retained pack-only PBO | 872,226 | `EA0434CAA2E5C4B81BB6EA1B18DF63BE6D3496717577C1856319F82DDF2169D1` | Prefix `AssetsEvidence\\TestAsset\\` |
| Fresh extraction of retained pack-only P3D | 871,437 | `42BFBC79AB47252B6DB69EF206F595D03B7A4F67F2C43F90FD6DB7DD07FF2427` | `MLOD`; exact input hash |
| Fresh extraction of retained pack-only `model.cfg` | 260 | `B49E9BE369841EA34E34124B0D3094011D477856974C297120AD7BF95AFA680C` | Exact fixture-source hash |
| Fresh extraction of retained pack-only `config.cpp` | 315 | `A0A3659A456B7857E686D5DFA251D98CA1B27D3B9D5CCE860EAF2989B571E829` | Exact fixture-source hash |
| Retained binarized PBO | 152,807 | `600C5A10091D150DAEB3EB3B56CE2B8DBB46BAD1A6D6F4BA466C31341F9855EC` | Prefix `AssetsEvidence\\TestAsset\\` |
| Fresh extraction of retained binarized P3D | 152,321 | `8AE946383C5111978FD3C2AFBB1532527CC8C4B2804D100139DEC6A6D49476F0` | `ODOL` |
| Fresh extraction of retained `config.bin` | 302 | `0023938CA79A42F1A82B8C96BC7DCE3BD6BA0F36EE708E1B5D35F339E5CFE38D` | Present; `config.cpp` absent |

BankRev `1.0.0.2` returned exit code `0` for both fresh extractions. Its full listings were exactly `sample_building.p3d`, `model.cfg`, `config.cpp` for pack-only and `sample_building.p3d`, `config.bin` for binarized output. The fresh files match the older retained extraction hashes as well.

The original Addon Builder console logs are not retained under `TEMP/assets-evidence`; only the author report and README record exit `0` and `Build Successful`. That is a provenance limitation for the original invocation, not a defect in the PBO-to-extraction hash chain. To check reproducibility independently, this council repeated both commands with the same installed tools and source into `TEMP/assets-council`; each returned `0` and printed `Build Successful`.

The repeated pack-only PBO is 872,226 bytes and its extracted source files match exactly. The repeated binarized PBO is 152,807 bytes and contains a 152,321-byte ODOL plus the same 302-byte `config.bin`, with no `model.cfg`. Rebuilt archive hashes differ from the retained hashes, and the rebuilt ODOL hash also differs; therefore no deterministic-byte claim is approved. The semantic observations—magic, sizes in this run, and file membership—reproduced.

## Primary sources reopened

- `D:/DayZ Projects/gui/imagesets/dayz_gui.imageset:1-14`, SHA-256 `AD001B5391F351FFDC68CBB39B685D16E21F5313862C251CB48A65241FA1095A`; all 11 sibling `.imageset` files were individually opened at line 1 and began with `ImageSetClass {`.
- `D:/DayZ Projects/scripts/1_core/proto/enwidgets.c:688-693`, SHA-256 `6BB20BAD5EFA498E584C7AE8976A1BF5310BCD9019215F31CB2990AF21CE0C9E`.
- `BohemiaInteractive/DayZ-Samples` at clean commit `da5e5437c9502620d9853fb6eed14701135ab2ea`: `Test_Building/model.cfg:1-71`, SHA-256 `35BFFAB1F2247952C781DA1701A5AC66281594E73191B9FF7ECC078F2541E903`, and `sample_building.p3d`, SHA-256 `42BFBC79AB47252B6DB69EF206F595D03B7A4F67F2C43F90FD6DB7DD07FF2427`.
- `Arkensor/DayZ-CommunityFramework` at clean commit `0763e7e7548c9a0bed6626afff835de80693ebf3`: `JM/CF/Workbench/dayz.gproj:14-28`, SHA-256 `B9198EDDA2A7620C967F0DEBCAAB61DA261108E018BF45734936B0FCB73C757F`.
- Saved DayZ “Doors on buildings” page, substantively reopened at `D:/StarDZ/docs/DayZ/Doors on buildings.md:6-10,25-35,106-111,267,286-287`, SHA-256 `C4CC65E7504741B94268A185FAD829E2A536A6A365E3E4E23A832248A4F94306`.
- Installed Addon Builder `1.0.240.639`, SHA-256 `C113DE9CAB5E91D27CA0630E360DB0A3ECA190EC797E1DCAD9CDFA70466B45E1`; its live `-help` text supplied the `-packonly` semantics.
- Installed `Bin/BinMake/binMakeRules.txt:5-10`, SHA-256 `916287C23744823E02CF194A861014B3AF42A128ECED44C0ADDED9D65E52ADD6`, and Binarize `1.29.0.163401`, SHA-256 `9D79B76F132EB5879821C617A1B509172DE38E2EDCBAFD9F0022882FDBB027C9`.
- BankRev `1.0.0.2`, SHA-256 `2C35799EB437DEACB3720F8D322A399D935739537EBA335839E873AA21A26A75`.

The relevant sections of `REFERENCIA_TIPOS_DE_ARQUIVO.md`, `GUIA_FERRAMENTAS_E_BUILD.md`, `GUIA_CRIAR_ITEM_DO_ZERO.md`, `DAYZ_GUI_REFERENCE.md`, and `AI/01-colorful-ui.md` were reopened as local leads. Their claims were not treated as independent engine proof. The `D:/DayZ Projects/DZ` scan was also repeated: all 8,188 `.p3d` files had `ODOL` magic, but no adjacent metadata maps that tree to a public game build, so this remains an inventory observation only.

## Follow-up claims not validated by this council

These nearby statements need their own evidence or safer wording:

- `en/03-gui-system/07-styles-fonts.md:499,511,527-531,537-538`: batching efficiency, recommended atlas sizes, SDF thresholds, resolution-dependent text behavior, style prevalence, tint multiplication, collision resolution, startup/GPU residency, and VRAM advice.
- `en/05-config-files/04-imagesets.md:34,44,140-183,695-715,723-790`: the entire XML loader/tutorial path; claimed XML feature differences; startup registration behavior; silent failures and last-wins behavior; `mpix` fallback/quality selection; case behavior; texture-format absolutes; power-of-two and padding performance advice; draw-call comparisons; and the claim that XML is in active DayZ use. XML-shaped files in local mods are implementation evidence only, not proof that DayZ loads them.
- `en/04-file-formats/02-models.md:32,38,45,58,179,558,577`: “compiled, engine-ready,” “no runtime conversion,” table descriptions that may overgeneralize format contents, fixed geometry-triangle guidance, the unbinarized file-patching workflow, and material-count/draw-call thresholds.

No inference from missing declarations, absent XML examples, an all-ODOL extraction, or a missing runtime log should be converted into a claim that the engine rejects a source format. Retail MLOD compatibility and imageset XML compatibility remain runtime/authoritative-document questions.

## Boundary check

The `TEMP/assets-evidence/tools/DayZTools` junction still points to `D:/SteamLibrary/steamapps/common/DayZ Experimental Tools`. The `project/DZ` and `source/DZ` junctions still point to `D:/DayZ Projects/DZ`. This review did not clean, rewrite, or traverse either target for deletion. It edited no English page or fixture source and made no commit.
