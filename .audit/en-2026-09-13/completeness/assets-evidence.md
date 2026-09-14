# Assets evidence: retained imageset and MLOD claims

**Observed:** 2026-09-13 America/Sao_Paulo (`2026-09-14T01:33Z`)  
**Wiki revision reviewed:** `103238a83078784b7ee6cd6486f63d7973e3fe92`  
**Scope:** `PKG-C02`, with the `ASSET-C01` and `GUI-C01` verification boundary. No English content was edited, no game/server/client executable was launched, and no retail compatibility or performance result is claimed.

## Outcome

Both retained claims still exceed the evidence. The extracted DayZ GUI resources establish the brace-delimited imageset format, but neither `LoadWidgetImageSet` nor the inspected official/community sources document XML support or a parser-speed ordering. A controlled Addon Builder fixture establishes that `-packonly` preserves an MLOD and that the binarizing path produces an ODOL and bakes/removes `model.cfg`; it does **not** establish that current retail DayZ loads an MLOD from a PBO.

The safe resolution is to replace both claims with source-bounded wording now and retain runtime work only for compatibility/performance questions that the documentation actually needs.

## Claim 1: “native imageset parses fastest”

**Page and hash:** `en/03-gui-system/07-styles-fonts.md:530`, SHA-256 `95909F8CE4B19D4F9364915653FE33361557A56D97E8C3DE87E40C2D7522C5C7`.

**Original text:**

> | Imageset XML and native formats are equivalent | Both define sprite regions | The native brace format is what the engine processes fastest. XML format works but adds a parsing step; use native format for production |

**Disposition:** unsupported. This contains three independent assertions—XML acceptance, functional equivalence, and relative parser performance—and none is established by the reviewed primary evidence.

**Exact supported replacement:**

> | Imageset resource format | The extracted vanilla `.imageset` files use brace-delimited `ImageSetClass` syntax | Use the brace-delimited format shown in this chapter. The reviewed sources do not establish XML loader support or any parser-speed difference. |

### Accepted evidence

- `D:/DayZ Projects/gui/imagesets/`: 11 extracted `.imageset` files were opened; every file begins with `ImageSetClass {`. `dayz_gui.imageset:1-14` shows `ImageSetClass`, `Name`, `RefSize`, `Textures`, and `Images`; SHA-256 `AD001B5391F351FFDC68CBB39B685D16E21F5313862C251CB48A65241FA1095A`.
- `D:/DayZ Projects/scripts/1_core/proto/enwidgets.c:688-693` declares `proto native bool LoadWidgetImageSet(string filename);`; SHA-256 `6BB20BAD5EFA498E584C7AE8976A1BF5310BCD9019215F31CB2990AF21CE0C9E`. The declaration names no accepted syntax, cache policy, or timing behavior.
- Pinned Community Framework commit `0763e7e7548c9a0bed6626afff835de80693ebf3`, `JM/CF/Workbench/dayz.gproj:14-28`, lists brace-format vanilla `.imageset` resources; file SHA-256 `B9198EDDA2A7620C967F0DEBCAAB61DA261108E018BF45734936B0FCB73C757F`. This is a third-party development setup, not engine-performance evidence.
- `D:/StarDZ/docs/REFERENCIA_TIPOS_DE_ARQUIVO.md:327-363` accurately records a brace-format project example, but is a fallible local reference. `D:/StarDZ/StarDZ_Market_Hub/StarDZ_MarketHub/GUI/imagesets/mh_icons.imageset:1-30` is XML, explicitly calls itself a placeholder at lines 3-4, and therefore proves only that XML-shaped source exists—not that DayZ loads it.

### Uncertainty retained

- XML imageset loading remains unverified. Absence of XML among the 11 extracted vanilla files is not an absence proof for a native loader.
- “Fastest,” “adds a parsing step,” startup loading, GPU residency, batching, and draw-call assertions require native documentation or a controlled runtime/profile result. None was found here.
- The adjacent performance statements at `07-styles-fonts.md:499,511,538` and similar assertions in `en/05-config-files/04-imagesets.md` were not expanded into a GUI rewrite; they should not be treated as validated by this report.

## Claim 2: MLOD loading in retail

**Page and hash:** `en/04-file-formats/02-models.md:39,51-60`, SHA-256 `D847E646348E3F763DCFB3655CC76AB2FA1FCCC4B8DA24C052004529D59A124E`.

**Original text at line 39:**

> - **Binarized vs. unbinarized:** Source P3D files from Object Builder are "MLOD" (editable). Binarize converts them to "ODOL" (optimized, read-only). The game can load both, but ODOL loads faster and is smaller.

**Exact supported replacement for line 39:**

> - **Binarized vs. unbinarized:** Object Builder source P3D files use MLOD. Binarize produces ODOL output that Bohemia describes as suitable for fast engine loading. This audit did not verify that current retail DayZ loads MLOD from a packed PBO.

**Original table rows at lines 55-57:**

> | File size | Larger | Smaller |  
> | Load speed | Slower | Faster |  
> | Used during | Development | Release |

**Exact supported replacement for those rows:**

> | File size | Source-dependent; 871,437 bytes in the recorded fixture | Source-dependent; 152,321 bytes in the recorded fixture |  
> | Load behavior | Retail PBO loading was not verified | Binarize documentation describes its output as suitable for fast engine loading; no comparative benchmark was run |  
> | Pipeline role | Editable authoring source | Binarized distribution output |

The fixture sizes are observations, not universal ratios or format limits.

**Original callout at line 60:**

> **Important:** When you pack a PBO with binarization enabled, your MLOD P3D files are automatically converted to ODOL. If you pack with `-packonly`, the MLOD files are included as-is. Both work in-game, but ODOL is preferred for release builds.

**Exact supported replacement for the callout:**

> **Important:** Addon Builder's `-packonly` option stores source files without binarizing them; the recorded fixture preserved its MLOD byte-for-byte. With binarization enabled, the same fixture produced ODOL and `config.bin`, while the source `model.cfg` was absent because model configuration is baked during binarization. This audit did not launch the game and therefore does not establish retail MLOD compatibility. Use verified binarized output for the documented release workflow until a version-matched retail test proves otherwise.

### Accepted evidence

- Official DayZ Samples clone: `https://github.com/BohemiaInteractive/DayZ-Samples.git`, pinned commit `da5e5437c9502620d9853fb6eed14701135ab2ea`. `Test_Building/sample_building.p3d` is an MLOD source file (871,437 bytes, SHA-256 `42BFBC79AB47252B6DB69EF206F595D03B7A4F67F2C43F90FD6DB7DD07FF2427`); `Test_Building/model.cfg:1-71` supplies the skeleton/animations (SHA-256 `35BFFAB1F2247952C781DA1701A5AC66281594E73191B9FF7ECC078F2541E903`). Samples provide authoring source, not a retail-loading guarantee.
- Saved official DayZ page `D:/StarDZ/docs/DayZ/Doors on buildings.md:6-10,25-35,106-111,267,286-287` requires binarization/packing, says `model.cfg` information is baked into P3D during binarization, and calls `Test_Building` ready to be packed. SHA-256 `C4CC65E7504741B94268A185FAD829E2A536A6A365E3E4E23A832248A4F94306`.
- Installed Addon Builder help says `-packonly` stores the folder and “Does NOT binarize files,” while binarization is default. Installed version `1.0.240.639`, SHA-256 `C113DE9CAB5E91D27CA0630E360DB0A3ECA190EC797E1DCAD9CDFA70466B45E1`.
- Installed `BinMake/binMakeRules.txt:5-10` sends `.p3d` inputs to `binarize.exe`; SHA-256 `916287C23744823E02CF194A861014B3AF42A128ECED44C0ADDED9D65E52ADD6`. Installed Binarize version `1.29.0.163401`, SHA-256 `9D79B76F132EB5879821C617A1B509172DE38E2EDCBAFD9F0022882FDBB027C9`.
- Controlled fixture under `TEMP/assets-evidence`:
  - `out-packonly-aligned/TestAsset.pbo`: exit `0` plus `Build Successful`; 872,226 bytes; SHA-256 `EA0434CAA2E5C4B81BB6EA1B18DF63BE6D3496717577C1856319F82DDF2169D1`. BankRev extraction contains `config.cpp`, `model.cfg`, and an MLOD exactly hash-identical to input.
  - `out-binarized-aligned/TestAsset.pbo`: exit `0` plus `Build Successful`; 152,807 bytes; SHA-256 `600C5A10091D150DAEB3EB3B56CE2B8DBB46BAD1A6D6F4BA466C31341F9855EC`. BankRev extraction contains `config.bin` and an ODOL P3D (152,321 bytes; SHA-256 `8AE946383C5111978FD3C2AFBB1532527CC8C4B2804D100139DEC6A6D49476F0`), with no `model.cfg`.

Exact aligned commands (PowerShell call operator; both returned exit code `0` and printed `Build Successful`):

```powershell
& 'D:\SteamLibrary\steamapps\common\DayZ Experimental Tools\Bin\AddonBuilder\AddonBuilder.exe' `
  'D:\StarDZ\docs\wiki\TEMP\assets-evidence\project\AssetsEvidence\TestAsset' `
  'D:\StarDZ\docs\wiki\TEMP\assets-evidence\out-packonly-aligned' `
  '-packonly' '-prefix=AssetsEvidence\TestAsset' '-clear' `
  '-temp=D:\StarDZ\docs\wiki\TEMP\assets-evidence\tool-temp-packonly-aligned' `
  '-toolsDirectory=D:\StarDZ\docs\wiki\TEMP\assets-evidence\tools\DayZTools'

& 'D:\SteamLibrary\steamapps\common\DayZ Experimental Tools\Bin\AddonBuilder\AddonBuilder.exe' `
  'D:\StarDZ\docs\wiki\TEMP\assets-evidence\project\AssetsEvidence\TestAsset' `
  'D:\StarDZ\docs\wiki\TEMP\assets-evidence\out-binarized-aligned' `
  '-prefix=AssetsEvidence\TestAsset' `
  '-project=D:\StarDZ\docs\wiki\TEMP\assets-evidence\project' '-clear' `
  '-temp=D:\StarDZ\docs\wiki\TEMP\assets-evidence\tool-temp-binarized-aligned' `
  '-toolsDirectory=D:\StarDZ\docs\wiki\TEMP\assets-evidence\tools\DayZTools' `
  '-binarizeFullLogs'
```

BankRev extraction commands used `BankRev.exe -f <owned-output-directory> <PBO>` against each aligned artifact. Earlier failed and prefix-misaligned attempts are preserved alongside the aligned outputs; they are not evidence for the conclusions.
- Read-only extraction scan: all 8,188 `.p3d` files under `D:/DayZ Projects/DZ` had `ODOL` magic. This is a local official-tool extraction observation only; no adjacent metadata file maps the `DZ` tree to a public patch/build. Separately, `D:/DayZ Projects/gui.txt` describes the GUI extraction as `prefix=gui`, `product=dayz`, `version=124588` (timestamp 2026-09-11; SHA-256 `842BADDDFAC0C005B23766ED0A8ED75A60A65AFF952166DA2A181930E6CAF258`), but that metadata does not version the `DZ` model tree.

### Uncertainty retained

- No current retail/Diag executable was launched. The inspected retail client is `1.29.0.163709` (SHA-256 `6E1719275798A69D61DA4F80FA57FB5F2B8D1910C95477ACF1CDC73DA9AF3129`), while installed Binarize is `1.29.0.163401`; that mismatch must be recorded in any later compatibility result.
- A source declaration, a successfully packed PBO, or an all-ODOL retail inventory does not prove that retail rejects or accepts MLOD. Likewise, the Binarize description supports its intended fast-loading output, not a measured MLOD-versus-ODOL speed ratio.
- The one model shrinking during binarization does not establish a universal size relationship.

## Current official web documentation access

On 2026-09-13, current search retrieval returned recent indexed bodies for the official Bohemia pages below (reported as crawled in the prior month), but direct page opens and the MediaWiki API returned HTTP 403 from both `community.bohemia.net` and `community.bistudio.com`. The exact access limit is retained rather than presenting the pages as directly reopened.

- `https://community.bohemia.net/wiki/Addon_Builder`: indexed body documents `-packonly` and default binarization.
- `https://community.bohemia.net/wiki/Binarize`: indexed body describes a model/world optimizing tool that produces a representation suitable for fast engine loading.
- `https://community.bohemia.net/wiki/DayZ%3ADoors_on_buildings`: indexed body matches the saved official page's statement that `model.cfg` is baked during binarization.
- `https://community.bohemia.net/wiki/CfgModels`: indexed body states that model configuration is processed during model binarization.
- `https://community.bohemia.net/wiki/P3D_File_Format_-_MLOD`: indexed body documents MLOD structure, not retail-loader compatibility.

The saved Bohemia pages were treated as primary-document mirrors with this access caveat; official DayZ Samples and installed official tools independently corroborate the pipeline behavior actually accepted above.

## Substantive local-document reading ledger

| Document | Lines substantively read | SHA-256 | Use and limitation |
|---|---|---|---|
| `D:/StarDZ/docs/DAYZ_GUI_REFERENCE.md` | 1-25, 177-207, 558-588, 2097-2338 | `F83CD7E9843AAD1001B36E40883E3FF876FE645489C958DBFD83067A35AB9063` | Image attributes/API and its full performance section; no imageset syntax/parser benchmark. |
| `D:/StarDZ/docs/REFERENCIA_TIPOS_DE_ARQUIVO.md` | 1-207, 230-365, 451-505 | `BCC70BBA5733111C8EF513A1B2A2735A9B9D71C5A282B1D70CC86643ECFAD1C1` | MLOD/ODOL, EDDS/imageset, PBO, and declared limits; fallible local observations. |
| `D:/StarDZ/docs/GUIA_FERRAMENTAS_E_BUILD.md` | 1-178, 429-633, 853-960, 1337-1477, 1598-1620, 1910-1957, 2046-2162 | `2ECAC825A7CC0995A2A97F5040CA26291A484E2CB5F5E42EBCC0195C5E9367D9` | Toolchain, pack-only/binarization, model paths, retail/Diag boundary, limitations, release checklist. Assertions were rechecked, not inherited. |
| `D:/StarDZ/docs/TUTORIAL_CRIAR_ANEXOS.md` | 1-41, 194-335, 344-378 | `DF3FDD6FA4E52CF24F7453392698172255DDD09AC4A339EC0AA0AF6D5C27271A` | Model/proxy paths and model.cfg workflow; project implementation is not authoritative. |
| `D:/StarDZ/docs/AI/01-colorful-ui.md` | 208-308, 837-905, 972-985, 1102-1130 | `91177BBFE484EF26BA6B365862BC117F73C879299136ADA3CA85BC2842574D78` | Imageset registration/build example; contains unrelated inaccurate “layout XML” wording and is only a lead. |
| `D:/StarDZ/docs/GUIA_CRIAR_ITEM_DO_ZERO.md` | 394-494, 1555-1649, 1811-1832, 1913-1923, 2202-2255 | `E6D837BB74CA8ABD5BDA5E532EAAEB08C3E847E01FAA85F085C77FC94AADD359` | Model/source/packaging and explicitly declared uncertainty. |
| `D:/StarDZ/docs/DayZ/Doors on buildings.md` | Full, 1-287 | `C4CC65E7504741B94268A185FAD829E2A536A6A365E3E4E23A832248A4F94306` | Saved official DayZ workflow; key lines cited above. |
| `D:/StarDZ/docs/DayZ/Buldozer for Object Builder.md` | Full, 1-65 | `9052B25127877C26311696E1AA514531AF5CFEEF9A856CBA0CAED948E2F94ECC` | Preview context only; Buldozer is not a retail compatibility test. |
| `D:/StarDZ/docs/DayZ/CfgConvert.md` | Full, 1-50 | `56B9143140DC6DD92949B6B1C311096FA0D209CADE620F52776F8DBAA41EAE4A` | Config conversion only, separated from P3D Binarize. |
| `D:/StarDZ/docs/DayZ/Tools Launcher.md` | Full, 1-35 | `14B4E44A29D8E3DBCE7B373D0691B3634D3A7B98FC69411C588629318313182A` | Tool-launcher context only. |
| `D:/StarDZ/docs/DayZ/Modding Basics.md` | Full, 1-198 | `1A0B2C1F7A69E369E74D923CB77D4716B9DD21941B0C02DA5015FA7F708B5839` | Saved official pack/test workflow; does not settle MLOD retail behavior. |
| `en/05-config-files/04-imagesets.md` | Targeted 120-160, 680-790 plus claim scan | `6759F4E2F50E1B293D7549D726A9616C08B5D9AE30890A9C3A6ECA3D886C7A8C` | Context only; its XML/performance claims remain unverified and were not edited. |

## Bounded reproducible fixture plan

### Imageset loader and performance

1. Use the owned `TEMP/assets-evidence/source/TestImageSet` seed and create two genuinely equivalent two-pixel atlases: one brace-format `ImageSetClass`, one XML candidate. Give every test set a unique name and register each in its own minimal PBO; keep EDDS bytes, texture dimensions, packing, and layout identical.
2. With file patching disabled, server council runs version-recorded retail and Diag clients separately. Capture `LoadWidgetImageSet` return values, `.RPT` resource messages, a deterministic screenshot/pixel check, and the exact mod/PBO hashes. Success means the named image visibly resolves, not merely that packing succeeded.
3. Only if both syntaxes load, test timing through repeated fresh-process runs or native profiler instrumentation. Randomize syntax order; separate cold and warm cache runs; record timer resolution, sample count, median/spread, hardware, executable hash, and raw results. Whole-startup time is not parser time.
4. If the loader cannot be isolated with adequate timer resolution, publish no ranking. Replace “fastest” with the source-bounded format recommendation above.

### MLOD/ODOL packaging and retail compatibility

1. Reuse the two preserved PBOs and rebuild them with a Binarize version aligned to the target retail build if available. Record tool hashes, complete console logs, exit code, PBO hashes, BankRev manifests, model magic, and `model.cfg` presence/absence.
2. Server council launches a clean retail client with file patching disabled and each PBO separately, spawns only `AssetsEvidence_TestAsset`, and captures `.RPT`, object visibility, model identity, and a screenshot. Repeat in Diag, clearly labeling any executable-specific result.
3. Add one animation from the official `Test_Building/model.cfg`; verify that the binarized output animates and test the pack-only path separately. This distinguishes “file opened” from “model configuration was processed.”
4. Treat a pack/tool success, a source declaration, or a missing log line as insufficient. The claim is resolved only by positive versioned load evidence or an explicit authoritative compatibility statement.

## Artifact boundary

All generated sources, PBOs, extracted manifests, hashes, the pinned CF checkout, and failed/aligned tool attempts remain under `TEMP/assets-evidence`. Junctions under `TEMP/assets-evidence/tools`, `project/DZ`, and `source/DZ` point to installed/extracted read-only inputs and must not be recursively cleaned or treated as owned copies.
