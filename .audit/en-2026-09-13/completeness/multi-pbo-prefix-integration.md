# Multi-PBO prefix integration receipt

Date: 2026-09-13 (America/Sao_Paulo)

This receipt records mechanical integration of the previously tested, source-backed backslash-prefix copy. No game launch, rebuild, search, or new experiment was performed.

## Manifest verification

- Baseline `examples/en/multi-pbo/manifest.json`: `63D5E5E9468AF98B37B30AB71C3CCEA69D45694E266377025F68E6953F088582`.
- Tested copy `TEMP/multi-pbo-council/sources/backslash-prefixes/manifest.json`: `679F31F1C7BB3440D37DE4FA7589203632B1A0D48799FFE41795CD7E20670C42`.
- Integrated manifest: `679F31F1C7BB3440D37DE4FA7589203632B1A0D48799FFE41795CD7E20670C42`; it is byte-identical to the tested copy.
- The only manifest delta is the four `prefix` values changing from forward slashes to backslashes. `CfgMods.defs.files[]`, all source files, `build.ps1`, and `README.md` were not changed.

The baseline and tested source trees each contain 12 files. The other 11 files are byte-identical: `build.ps1`, `README.md`, `package/Server/mod.cpp`, `package/Shared/mod.cpp`, `src/Core/config.cpp`, `src/Data/config.cpp`, `src/Data/data/example.txt`, `src/Scripts/config.cpp`, `src/Scripts/scripts/3_Game/PBOExample.c`, `src/Server/config.cpp`, and `src/Server/scripts/5_Mission/PBOExampleServer.c`.

## Exact applied diffs

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

In `.audit/en-2026-09-13/completeness/multi-pbo-runtime-council.md`, the Core PBO table literal was corrected from the 62-character digest `366F6FE34072B71AF3FDCA7EDED117F3F1C574E1410110023FDB0D3F64092F` to the receipt-backed `366F6FE34072B71AF3FDCA7EDED117F3F3F1C574E1410110023FDB0D3F64092F`. The council report narrative and history were otherwise preserved.

## Evidence and limits

The correction matches `TEMP/multi-pbo-council/builds/backslash-prefixes/pboexample-20260913-230553-89a0b34e/receipt.json` (receipt SHA-256 `60CC435CBE8A8E56DFED6C12DEDB9D95BD33705EE55BAEFE18FAFF3147AF74E0`) and the council JSON component record. The tested runtime evidence remains scoped to DayZDiag `1.29.0.163709`; this integration is not a new runtime result and does not expand the council's documented limitations.
