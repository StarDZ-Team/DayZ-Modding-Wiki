# Multi-PBO post-integration confirmation

Executed 2026-09-14, America/Sao_Paulo. Repository HEAD was `23c336eb5740b6b5e5d2d8bc2329288b70ccc26c` (`docs(en): point contribution links to published source`), after the requested integration. This is a bounded confirmation record, not a general compatibility claim.

## Scope and immutable inputs

The checked-in twelve-file fixture was compared byte-for-byte to the reviewed fixed copy at `TEMP/multi-pbo-council/sources/backslash-prefixes`. All 12 matched, including `manifest.json` SHA-256 `679F31F1C7BB3440D37DE4FA7589203632B1A0D48799FFE41795CD7E20670C42`; its only four semantic repair values are raw PBO prefixes with backslashes. The `CfgMods.files[]` values were not changed.

The exact retained probe source is `TEMP/multi-pbo-council/probe-exact/scripts/5_Mission/multi_pbo_runtime_probe.c`; its retained built PBO, copied unchanged into the isolated workspace, has SHA-256 `279970F47E0348D598B0CE5F7722FF3FC6CD84018107411F6AFC138FB2F63849`. The copied recipe `TEMP/multi-pbo-confirmation/run-case.ps1` has SHA-256 `FBAC12CD27A18E254D72CB4F6C9AC5FCF34775BF24D8A3BBD567D980040C4E55`, identical to the reviewed recipe.

## One allowed build

Command:

```powershell
& 'examples\en\multi-pbo\build.ps1' -ToolRoot 'D:\SteamLibrary\steamapps\common\DayZ Experimental Tools' -WorkRoot 'D:\StarDZ\docs\wiki\TEMP\multi-pbo-confirmation\build'
```

Result: exit code 0; receipt `TEMP/multi-pbo-confirmation/build/pboexample-20260914-002734-8140c691/receipt.json`, SHA-256 `E8E483389F85C84FA819B16EE36C16EF2CE88DDB0E17F460076F765DAE487C1B`. Addon Builder SHA-256 was `C113DE9CAB5E91D27CA0630E360DB0A3ECA190EC797E1DCAD9CDFA70466B45E1`; the receipt records BankRev inspection and one-to-one OK DSCheck results for all four built PBOs.

| Component | Built PBO SHA-256 |
| --- | --- |
| Core | `6A20B58DF2FD56CE4CBFA76FBC11D0563090D27A93198ED708CE1E94F0C7A636` |
| Scripts | `23C2791D782EC81E442F791D6D411908878FDD65F997E2CEEC5EE8EE7BFE6116` |
| Data | `1CE4ADB9D28C778E083CA506E0042217CE6A68FF2EC7FC085E2E19596D619071` |
| Server | `0E8B08052E2777D33CA4FDC9664D42E42501CB35ED215578A4420B2D39467236` |

## Runtime preflight failure — no launch

The planned one runtime invocation used `DayZDiag_x64.exe` product version `1.29.0.163709`, SHA-256 `34F6377BE4FD065D104E67263E0C96AC2CB2E348119A4838EBA08D2E61B7A69A`, isolated port set `26280`–`26282`, and instance ID `780`. Immediately before invocation, no `DayZDiag_x64` process was present and no UDP endpoint owned ports `26280`, `26281`, or `26282`.

The exact recipe stopped before creating a process, with:

```text
Private mission was not found: D:\StarDZ\docs\wiki\TEMP\multi-pbo-confirmation\mission\dayzOffline.chernarusplus
```

The private CE copy exists but was copied directly to `TEMP/multi-pbo-confirmation/mission` (43 files) rather than to the required child path `mission/dayzOffline.chernarusplus`. The config SHA-256 is `E1D27E0535C21CD10DB9F710FDABA1C8177F14EFE01456DE92A99DEF31933171`; the failure occurred during the recipe's mission-containment preflight, so PID, process record, RPT, script log, all seven markers, and 81-byte data result are absent/not observed.

No retry, configuration variation, or repair was attempted, as required. Post-failure inspection again found no `DayZDiag_x64` process and no owned UDP endpoints on `26280`–`26282`; no process cleanup was necessary. All created files remain under `TEMP/multi-pbo-confirmation`; no pre-existing TEMP junction target was changed.

## Limits

This record confirms the checked-in fixture hashes and one post-integration packaging build only. It does not confirm the seven runtime markers or data sentinel for this revision, and makes no claim about client join, signature enforcement, size limits, or general version compatibility.
