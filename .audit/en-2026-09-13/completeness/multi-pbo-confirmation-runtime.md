# Multi-PBO post-integration runtime completion

Executed 2026-09-14, America/Sao_Paulo, after the initial staging-only preflight record. This report leaves `multi-pbo-confirmation.md` and `.json` unchanged as history.

## Mechanical staging correction

Before copying, the reviewed source `TEMP/multi-pbo-council/mission/dayzOffline.chernarusplus` was enumerated as a complete 43-file manifest. The sorted `relative-path|bytes|SHA-256` manifest has SHA-256 `1260F07AC011D4CFDA66BF0915D8475ECDD072776CCD3B2BE8A43EF4B3B7EA3E`; the earlier direct copy at `TEMP/multi-pbo-confirmation/mission` matched that manifest byte-for-byte.

Only the missing recipe-required child directory was added: `TEMP/multi-pbo-confirmation/mission/dayzOffline.chernarusplus`. The 43 files were copied directly from the reviewed source into that path, then re-enumerated; count and the complete member/hash manifest matched exactly (`1260F07AC011D4CFDA66BF0915D8475ECDD072776CCD3B2BE8A43EF4B3B7EA3E`). No fixture, probe, config, engine flag, or code changed, and no build was run in this follow-up.

## Runtime input provenance

- Checked-in 12-file fixture matched the reviewed fixed copy before the prior build; manifest SHA-256: `679F31F1C7BB3440D37DE4FA7589203632B1A0D48799FFE41795CD7E20670C42`.
- Reused build receipt: `TEMP/multi-pbo-confirmation/build/pboexample-20260914-002734-8140c691/receipt.json`, SHA-256 `E8E483389F85C84FA819B16EE36C16EF2CE88DDB0E17F460076F765DAE487C1B`.
- Exact retained probe PBO: `TEMP/multi-pbo-confirmation/runtime-mods/@MultiPboRuntimeProbeExact/Addons/MultiPboRuntimeProbe.pbo`, SHA-256 `279970F47E0348D598B0CE5F7722FF3FC6CD84018107411F6AFC138FB2F63849`.
- Reused recipe: `TEMP/multi-pbo-confirmation/run-case.ps1`, SHA-256 `FBAC12CD27A18E254D72CB4F6C9AC5FCF34775BF24D8A3BBD567D980040C4E55`.
- Unchanged config: `TEMP/multi-pbo-confirmation/runtime-26280.cfg`, SHA-256 `E1D27E0535C21CD10DB9F710FDABA1C8177F14EFE01456DE92A99DEF31933171`.
- Executable: `D:/SteamLibrary/steamapps/common/DayZ/DayZDiag_x64.exe`, product version `1.29.0.163709`, SHA-256 `34F6377BE4FD065D104E67263E0C96AC2CB2E348119A4838EBA08D2E61B7A69A`.

## One bounded runtime case

The unchanged recipe ran case `post-integration-exact`, instance ID `780`, and ports `26280` (game), `26281` (Steam query), and `26282` (observed additional UDP). It validated the 43-file child mission, single numeric instance ID, expected query-port relationship, and free ports before launch; the captured PID was `18416`.

Process record: `TEMP/multi-pbo-confirmation/cases/post-integration-exact/process.json`, SHA-256 `1C385955A1B4F77978DDF2EC9F5F28D16C1E4AEB859B8ABA0865ED0F2EBC2B68`. The recipe sampled all three bound endpoints under PID `18416`, then performed its owned bounded cleanup: `killedByHarness=true`, exit `-1` / `0xFFFFFFFF`, and `portsAfterCleanup=[]`; an independent post-run check also found neither PID `18416` nor endpoints on those ports.

Both independent log channels contain the full seven-marker block:

```text
MULTIPBO:RUNTIME:BEGIN
MULTIPBO:RUNTIME:FIXTURE=PBOExample
MULTIPBO:RUNTIME:SERVER_COMPONENT=true
MULTIPBO:RUNTIME:DATA_PATH=PBOExample/Data/data/example.txt
MULTIPBO:RUNTIME:DATA_READ_BYTES=81
MULTIPBO:RUNTIME:DATA_SENTINEL=This fixture's Data archive has a unique prefix and its own CfgPatches identity.
MULTIPBO:RUNTIME:END
```

- RPT: `TEMP/multi-pbo-confirmation/cases/post-integration-exact/profiles/DayZDiag_x64_2026-09-14_00-31-40.RPT`, SHA-256 `48D4A4513A2B094811A0ABBD95D7CC953BEC60944F497714DD1106D15F9A8FC5`, lines 1426–1432.
- Script log: `TEMP/multi-pbo-confirmation/cases/post-integration-exact/profiles/script_2026-09-14_00-31-42.log`, SHA-256 `9034724DC14FE8531A0CC874A3287A4FF78994542C6E35D495FB3B0B644992E2`, lines 20–26.
- Console log: `TEMP/multi-pbo-confirmation/cases/post-integration-exact/profiles/server_console.log`, SHA-256 `EAB28DA6B4647CC8B2DC4AABBAD5C4D7E89D592C50A49519A137E58C33A27F13`.

The RPT records Game `417 files / 1393 classes` and Mission `211 files / 445 classes` before the marker block. This is direct proof of the named script resolution, server-component call, and 81-byte data read for this fixed fixture in this bounded headless DayZDiag server run.

## Limits

This is not evidence of client join, public reachability, production-server behavior, signature enforcement, size limits, Workshop distribution, or behavior on other game/tool versions. The CE logs include CE XML parse warnings; they do not negate the marker evidence but are not presented as CE certification.
