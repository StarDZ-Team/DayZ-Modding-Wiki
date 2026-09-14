# Multi-PBO runtime council

Date of execution: 2026-09-14 UTC (2026-09-13 America/Sao_Paulo)  
Repository revision inspected: `5714990e98d67ee4782bb5be85aa9b5519ae6462`  
Runtime: `DayZDiag_x64.exe` product version `1.29.0.163709`, SHA-256 `34F6377BE4FD065D104E67263E0C96AC2CB2E348119A4838EBA08D2E61B7A69A`

## Council verdict on the prior evidence

The prior report's observations are accepted: the original four PBOs built and mounted, but the exact independent Mission probe could not resolve `PBOExample` or `PBOExampleServer`. That was a genuine runtime failure, not a successful test, and its retained evidence correctly withheld the function, server-component, and data-read claims.

The prior report's cause remained appropriately unresolved. This council reproduced the same failure from a fresh copy and then isolated it. The unresolved classes are a **fixture defect**, not a defect in the exact probe or in the retained launch topology: the manifest writes forward slashes into the PBO `prefix` property, while this DayZ runtime only resolved the same module paths after the prefix properties were rebuilt with backslashes.

The original manifest is SHA-256 `63D5E5E9468AF98B37B30AB71C3CCEA69D45694E266377025F68E6953F088582`. Its four relevant records are:

- line 10: `PBOExample/Core`
- line 18: `PBOExample/Scripts`
- line 26: `PBOExample/Data`
- line 34: `PBOExample/Server`

The failure is visible in `TEMP/multi-pbo-council/cases/baseline-exact/profiles/script_2026-09-13_22-48-04.log` lines 9-13: both class names are unresolved and Mission compilation stops. Its SHA-256 is `FD4B2013B47B8B43CF4E0AE4119DD4539E454167B3F6E3FA1C15E44B58A71A0B`.

## Council verdict on the proposed repair

Accepted for DayZ `1.29.0.163709`: change only the four `prefix` strings in `examples/en/multi-pbo/manifest.json`:

```diff
- "prefix": "PBOExample/Core"
+ "prefix": "PBOExample\\Core"
- "prefix": "PBOExample/Scripts"
+ "prefix": "PBOExample\\Scripts"
- "prefix": "PBOExample/Data"
+ "prefix": "PBOExample\\Data"
- "prefix": "PBOExample/Server"
+ "prefix": "PBOExample\\Server"
```

These are JSON source spellings: each `\\` encodes one backslash in the value passed to AddonBuilder. Do not change the `CfgMods.defs.files[]` strings; the repaired run kept their forward-slash form and succeeded. No `config.cpp`, script, `mod.cpp`, or build-script change was needed.

All 11 non-manifest fixture files in the repaired copy are byte-identical to the baseline copy. The repaired manifest is SHA-256 `679F31F1C7BB3440D37DE4FA7589203632B1A0D48799FFE41795CD7E20670C42`. Changing all four records is the smallest fixture-wide repair actually verified here; this run does not claim that each of the four changes is independently necessary for every possible consumer.

The versioned fixture was deliberately not edited. Integration should apply the four-line manifest repair, rebuild from that reviewed source, and rerun the same exact probe before describing the checked-in fixture as runtime-verified.

## Independent reproduction

Everything was run from copies under `TEMP/multi-pbo-council`. The baseline build used the repository's real `build.ps1` and installed DayZ Experimental Tools. Its receipt is `TEMP/multi-pbo-council/builds/baseline/pboexample-20260913-224605-771a9529/receipt.json`, SHA-256 `0C8A5D0E8F7B6F38C3074BD970AD3E8011676B6940DD276C29AD03EBC89F897D`.

The exact probe source is byte-identical to the prior probe source: SHA-256 `FAF495615C77E372498957487FE63156768B19C1DC2B85CEBE0E801B26E669C2`. Its rebuilt PBO is SHA-256 `279970F47E0348D598B0CE5F7722FF3FC6CD84018107411F6AFC138FB2F63849`. This removes a changed-probe explanation for the different outcomes.

| Case | Isolated change | Runtime result |
|---|---|---|
| `baseline-exact` | Fresh build of unchanged fixture copy | Reproduced both unresolved variables; Game `416 files / 1392 classes` |
| `cfgmods-renamed` | Renamed `CfgMods` class identities | Both variables still unresolved |
| `flattened-exact` | Removed the extra source-side `scripts/` nesting and adjusted `files[]` | Both variables still unresolved |
| `cfgmods-patch-identities-exact` | Matched `CfgMods` names to `CfgPatches` identities | Both variables still unresolved |
| `modcpp-defs-exact` | Added dependency/Defs material patterned after `StarDZ_Weapons` | Both variables still unresolved |
| `backslash-prefixes-exact` | Changed only the four manifest prefix values to backslashes | Both classes resolved; Mission compiled; exact data file read |

The repaired build receipt is `TEMP/multi-pbo-council/builds/backslash-prefixes/pboexample-20260913-230553-89a0b34e/receipt.json`, SHA-256 `60CC435CBE8A8E56DFED6C12DEDB9D95BD33705EE55BAEFE18FAFF3147AF74E0`. BankRev recorded:

| PBO | Prefix | First relevant member | SHA-256 |
|---|---|---|---|
| `PBOExample_Core.pbo` | `PBOExample\Core` | `PBOExample\Core\config.cpp` | `366F6FE34072B71AF3FDCA7EDED117F3F3F1C574E1410110023FDB0D3F64092F` |
| `PBOExample_Scripts.pbo` | `PBOExample\Scripts` | `PBOExample\Scripts\scripts\3_game\pboexample.c` | `889797B200BA32302CC43B4BCF2D62734141B062D6C9E1D7C0EFF33162D4FEF2` |
| `PBOExample_Data.pbo` | `PBOExample\Data` | `PBOExample\Data\data\example.txt` | `3A713D987C35356C428D09C2DD5175ABC4443B8084460E4B7189DA33313BD869` |
| `PBOExample_Server.pbo` | `PBOExample\Server` | `PBOExample\Server\scripts\5_mission\pboexampleserver.c` | `5BB685037CF0D37CA7B12FBC97152ED2F28B26E0D148C380F8508DD102974E82` |

## Positive runtime proof

The successful case used instance ID `748`, a private 43-file CE mission, game port `26180`, Steam query port `26181`, and the observed additional UDP port `26182`. The harness validated the single numeric instance ID, mission containment/file count, query-port relation, and free ports before launch.

`TEMP/multi-pbo-council/cases/backslash-prefixes-exact/profiles/DayZDiag_x64_2026-09-13_23-06-09.RPT` (SHA-256 `20F02A61993E12CAEC062775C8D8DA584312C03425475AAB7112CC5CAE68EF40`) records:

- line 236: Game loaded `417 files / 1393 classes`, one file and one class more than the failed baseline;
- line 1415: Mission loaded `211 files / 445 classes`;
- lines 1426-1432: the complete marker block;
- line 5143: `Player connect enabled`.

The independent script log `TEMP/multi-pbo-council/cases/backslash-prefixes-exact/profiles/script_2026-09-13_23-06-11.log` (SHA-256 `87B9B99558513AC80A7715F0DC65AEC0E3D28E6482B2E789B7FEF29D18DD185A`) contains the same marker block at lines 20-26:

```text
MULTIPBO:RUNTIME:BEGIN
MULTIPBO:RUNTIME:FIXTURE=PBOExample
MULTIPBO:RUNTIME:SERVER_COMPONENT=true
MULTIPBO:RUNTIME:DATA_PATH=PBOExample/Data/data/example.txt
MULTIPBO:RUNTIME:DATA_READ_BYTES=81
MULTIPBO:RUNTIME:DATA_SENTINEL=This fixture's Data archive has a unique prefix and its own CfgPatches identity.
MULTIPBO:RUNTIME:END
```

This is sufficient to claim runtime script resolution for both client/shared and server components plus an exact data read in the tested headless server context. The 81-byte sentinel source is SHA-256 `C460C6E58E3051A463E565F55D835469415E3536B9EF6095178D3D60041CB941`; the versioned source, baseline copy, and repaired copy all match this digest.

## Process bounds and cleanup

`TEMP/multi-pbo-council/run-case.ps1` (SHA-256 `FBAC12CD27A18E254D72CB4F6C9AC5FCF34775BF24D8A3BBD567D980040C4E55`) launched each owned process with `UseShellExecute=false`, `CreateNoWindow=true`, and `WindowStyle=Hidden`, sampled its endpoints, killed only the captured process after the bound, waited for exit, and checked its ports again.

| Case | PID | Instance | Ports checked | End state |
|---|---:|---:|---|---|
| `baseline-exact` | 53828 | 742 | 26120-26122, independently observed free before launch | harness kill; exit `-1` / `0xFFFFFFFF`; no ports after cleanup |
| `cfgmods-renamed` | 53188 | 743 | 26130-26132 | harness kill; exit `-1` / `0xFFFFFFFF`; no ports after cleanup |
| `flattened-exact` | 55836 | 745 | 26150-26152 | harness kill; exit `-1` / `0xFFFFFFFF`; no ports after cleanup |
| `cfgmods-patch-identities-exact` | 59268 | 746 | 26160-26162 | harness kill; exit `-1` / `0xFFFFFFFF`; no ports after cleanup |
| `modcpp-defs-exact` | 15020 | 747 | 26170-26172 | harness kill; exit `-1` / `0xFFFFFFFF`; no ports after cleanup |
| `backslash-prefixes-exact` | 60068 | 748 | 26180-26182 | harness kill; exit `-1` / `0xFFFFFFFF`; no ports after cleanup |

The first case's `process.json` has a recording-only PowerShell expression defect: its `portsCheckedFreeBeforeLaunch` array serializes as `26120,26120,1,26120,2`. The intended three ports were separately checked/observed, and the expression was fixed before every subsequent case. This defect does not affect the runtime comparison, but the malformed first record is not presented as valid proof of that preflight by itself.

Two exploratory setup artifacts were excluded from the verdict. An initial `Copy-Item -LiteralPath ...\*` mistake supplied an empty probe source tree and produced a 140-byte PBO (SHA-256 `D0C9FC4C23DF273FAAA5E70D19E348932F46953018CFA64F8A91CDDCF8C7F5FA`); it was never used as the exact probe. A later `baseline-inspect` process (PID 47848, instance 744, ports 26140-26142) compiled Mission but emitted none of that experimental probe's intended markers within its bound, so it establishes no class-resolution result and is not counted in the six-case causal matrix. Both are retained rather than erased.

No `DayZDiag_x64` process and no UDP endpoint in the test range `26120-26182` remained at final cleanup. The negative runs did display native DayZDiag compile-error dialogs, including the screenshots supplied by the user. The process flags therefore describe bounded hidden launch intent but did **not** suppress the engine's modal UI; the positive run produced no compile dialog.

An incorrect exploratory `BankRev` option created an extracted `StarDZ_Weapons_Scripts` directory beside the source PBO. After validating both paths, it was moved intact to `TEMP/multi-pbo-council/accidental-bankrev-output`; nothing was deleted and no artifact remains beside the source PBO.

## Source provenance and reasoning

- Repository fixture at revision `5714990e98d67ee4782bb5be85aa9b5519ae6462`: `examples/en/multi-pbo/manifest.json` lines 10, 18, 26, and 34, plus the actual `config.cpp`, script, probe, build script, receipts, BankRev member logs, RPT, and script logs retained under the council directory.
- User-supplied `D:\StarDZ\StarDZ_Weapons`, enclosing repository revision `24a465d28d7c322cfdaf1af5d2484614f7c1d690`: `D:\StarDZ\dev.py` lines 238-263 passes raw backslash prefixes, while `StarDZ_Weapons\StarDZ_Weapons\Scripts\config.cpp` lines 49-57 keeps forward slashes in `files[]`. The actual built Scripts PBO (SHA-256 `CA60692DB3BAFA657E7064E3174353164DAE9E9FFB6933C1F05FBA48C9836709`) reports `prefix = StarDZ_Weapons\Scripts\`; the captured output is `TEMP/multi-pbo-council/sources/stardz-weapons-bankrev.txt`. This project is fallible corroboration, not authority; the controlled fixture run supplies the causal evidence.
- Current extraction `D:\DayZ Projects`: `scripts.txt` lines 1-3 records `prefix=scripts\`, `product=dayz`, `version=124588` (SHA-256 `E45D501E4FB29587FA1E8BF553B0A7B33B751AA32C5AA5ECB1D03B8B6026F55F`); `scripts\3_game\global\game.c` lines 554-570 declares the config array accessors inspected; `scripts\5_mission\mission\missionserver.c` line 83 is the overridden `OnInit()` context. The extraction version record is preserved as provenance and is not asserted to be the same number as the executable build.
- Official DayZ Samples, `https://github.com/BohemiaInteractive/DayZ-Samples.git`, commit `da5e5437c9502620d9853fb6eed14701135ab2ea`: `Test_Inputs/config.cpp` lines 21 and 27 uses forward-slash `files[]` values (SHA-256 `71B869D713C15D38037B0B8B6CC682CCAEA03599DDFF370DA786D42CD813121C`). This is contextual support for leaving `files[]` unchanged, not direct proof of a prefix rule.
- Bohemia Interactive Community Wiki, `https://community.bistudio.com/wiki/Arma_3%3A_Creating_an_Addon`, section **Addon Prefix**: the indexed publisher-page content specifies `\` between pseudo-directories and says the prefix character set includes backslash. This is the shared addon/PBO convention on an Arma 3 page, so it is external corroboration rather than DayZ runtime proof. Direct page/API fetches returned HTTP 403; the access limitation is recorded rather than hidden.
- Real public DayZ implementations, pinned and fetched from their primary GitHub repositories on 2026-09-14 UTC: Community Framework `0763e7e7548c9a0bed6626afff835de80693ebf3` has `JM/CF/Legacy/$PBOPREFIX$.txt` with `prefix=JM\CF\Defines;`, while CF Scripts, DayZ Expansion Groups `6dacd00f6d943ebbd99e0cf1baad93f470d96419`, Community Online Tools `41f2c2b99565d0e3970163e162efbf1283fdca62`, and DayZ Editor `992e6b29b42b5d8e609632b59771335a23d205eb` use forward slashes in their `CfgMods.files[]` paths. These independently corroborate the separator distinction without supplanting the controlled runtime proof. Exact URLs, file hashes, and lines are in `TEMP/multi-pbo-council/sources/external-source-access.txt`.
- A read-only attempt to inspect `https://discord.com/channels/452035973786632194` loaded a Discord tab but returned no accessibility content and timed out on the follow-up snapshot. The tab was closed, no message was sent, and no Discord evidence is claimed.
- The supplied `dayz-mcp` commit `ffa47e7ca8c82f4785279e919cb9d40053bddf8c` and `DayZ-Modding-Knowledge-Pack` commit `9727ae83e65ac26a1cd386c64821b00159f8f933` were verified but were not needed as evidence. No MCP was installed or started.

## Limits

The supported cause and repair are scoped to the tested Windows DayZDiag server runtime `1.29.0.163709`. This run does not establish client join behavior, public reachability, production server behavior, Workshop distribution, signature enforcement, tamper rejection, or behavior on other DayZ/tool versions. No full wiki build was run because it cannot validate Enforce Script or game runtime and was outside this task.

No versioned fixture or English page was mutated, and no commit was created. All copied sources, experimental variants, PBOs, keys/signatures, logs, profiles, private CE state, process records, and the accidental BankRev output are preserved under `TEMP/multi-pbo-council`.
