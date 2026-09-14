# PBO Council Second Revision

**Date:** 2026-09-13  
**Scope:** The six final-council repairs in `pbo-final-council.md`, limited to the PBO evidence ledger, fixture, receipts, and `TEMP/pbo-second-revision`. No English wiki page, game/server launch, or unrelated file was changed.

---

## Historical receipt preservation

Before replacing this receipt, the prior `pbo-revision.md` and `pbo-revision.json` were copied byte-for-byte to `TEMP/pbo-second-revision/pre-repair-receipts/`; their SHA-256 values remain `A443203C0321F5FD313ED9FF67AB40D7BD7CC51DE14802AC60933A65E7405DD7` and `9301E870FFE255D71447C2812A309664145C1024CA4CA7EDA3AC5934288ACB78`.

`pbo-evidence.json` now contains `WIKI-FIVE-LAYERS`, a `current_wiki` record for the actually reopened `en/02-mod-structure/01-five-layers.md`. Its hash was recomputed as `1C8571C015339DD7508D92C519A0F6A563B3790D5120ED776832EFBA345C8413`; the read covered the full file, particularly script-module hierarchy, compile-time visibility, and `requiredAddons` load-order claims.

---

## Runner repairs

The runner now performs two distinct phases. It builds, assigns final names, runs BankRev property/member inspection, and collects normalized virtual paths for every component before collision scanning; no hashing, key generation, or signing occurs until that global scan passes.

`BankRev -logFull` is parsed as full trimmed lines. Each line must fall below the exact normalized manifest prefix boundary, then it is case-insensitively normalized; the retained success receipt includes the original full member lines. `WorkRoot` is rejected when it is the fixture directory or a descendant, preventing generated keys, PBOs, logs, or receipts in versioned fixture paths.

DSCheck accepts only nonblank lines exactly shaped as `Signature <path> is OK`; it resolves every output path, rejects duplicate/missing/unexpected results and any other text, and requires a one-to-one match with the expected `.bisign` set for each package. This is a bounded tool-output assertion, not a DayZ signature-enforcement or PBO-byte-binding claim.

---

## Executed source/tool validation

The successful isolated run exited `0`:

```powershell
.\examples\en\multi-pbo\build.ps1 -ToolRoot 'D:\SteamLibrary\steamapps\common\DayZ Experimental Tools' -WorkRoot 'D:\StarDZ\docs\wiki\TEMP\pbo-second-revision\success-work'
```

Run root: `TEMP/pbo-second-revision/success-work/pboexample-20260913-211644-14a6980d`  
Receipt SHA-256: `B9CD721C3B3C4AB59CC8C9822A6D1A28B1C1E8E72A65044E87C8FB61A9129E51`

| Component | PBO SHA-256 | `.bisign` SHA-256 | Observed members |
|---|---|---|---:|
| Core | `0F6C0CB0CD4C352029F78A612AA4076CB44FD39172B547EEEB13692BF65A87A0` | `F855201A207663437BA5FACA33D6773A0F72AA07FDC1A52C4DCB65233F17FC3E` | 1 |
| Scripts | `2901BC2B730C9143E6E24778F7F8A7A0B7F7B619B77446AA0E39123B4ABB9333` | `ED3ABC66A5D44EB4CC8BB75A41739DF3EA029B64F365A052063A43556E502BFE` | 2 |
| Data | `2638F46BD316F8D15C488D5ADD4E7F735EFC290B93BAEF8413CE1EB9159EAABF` | `07A48F1C65FF3EC511763A77CB0E49029C7526FCB470B84650D0693FD5A196FF` | 2 |
| Server | `EC66DCD8B71C6181965D4E631A79DFBFC531D4044920E481666DFE62B9B61638` | `24644DEE80BC71230FFBB76FB3C0C8DC39F8780E277B4A30CFDE81B3B25FB4EF` | 2 |

Tool hashes in the receipt: AddonBuilder `C113DE9CAB5E91D27CA0630E360DB0A3ECA190EC797E1DCAD9CDFA70466B45E1`; BankRev `2C35799EB437DEACB3720F8D322A399D935739537EBA335839E873AA21A26A75`; DSCreateKey `81A100EEB190FAB4492970D0E6F051DB5C025BF8A4ADC2815C57ED9FE3022067`; DSSignFile `098F28B46BFE40AD4CF5C60DD3E570E984FE74AE423090B6D3F2DA8D7C4E1E78`; DSCheckSignatures `9BAFBBBDCE1E2792515039F99B7150CA1CE97ADF16AAB8CFC79BDC8938A8503C`.

---

## Reproduced negative cases

- Partial signatures: three PBOs with two `.bisign` files returned exit `0`, two `is OK` lines, and `No signature found`; retained at `TEMP/pbo-second-revision/negative/partial/dscheck.log`. The runner rejects the non-OK line and incomplete set.
- Missing key: a signed PBO with an empty keys directory returned exit `0` and `Key not found`; retained at `TEMP/pbo-second-revision/negative/missing/dscheck.log`. The runner rejects it.
- Wrong signature: a Core PBO paired with the Scripts signature returned exit `0` and `is wrong`; retained at `TEMP/pbo-second-revision/negative/wrong/dscheck.log`. The runner rejects it.
- Duplicate path: a copied fixture with Data prefix changed to Core failed before hashing/signing; its run has zero `.bisign`, zero private keys, and no receipt. Transcript: `TEMP/pbo-second-revision/duplicate.log`; tool logs remain in `duplicate-work/pboexample-20260913-211923-1f9fff8c/logs/`.
- Bad tools path: Addon Builder returned exit `0`, wrote `[ERROR]`, and produced no PBO; its output is retained at `TEMP/pbo-second-revision/negative/bad-tool-output/addonbuilder.log`, matching the runner's fatal/error guard.
- Stale parent output: `TEMP/pbo-second-revision/stale-work/unrelated-stale.pbo` remained present while the fresh child run `pboexample-20260913-211845-6205897a` succeeded. Its receipt SHA-256 is `1B4E39D2745E88146639BD4420DA742E7ACC92D081557EBC9A7ED3A9AD6B711E`.
- Fixture WorkRoot guard: a direct run with `WorkRoot` equal to `examples/en/multi-pbo` failed before tool use; retained at `TEMP/pbo-second-revision/workroot-guard.log`.
- Full-line BankRev member handling: a temporary copy containing `data/member name.txt` built successfully; the Data receipt retained `PBOExample/Data\\data\\member name.txt` as one full member line. Run root: `TEMP/pbo-second-revision/space-work/pboexample-20260913-212329-5e8aab04`; receipt SHA-256: `D3790B24821FDACF0449B02119B78A07156560C58C434D4AD1A0911AF31E07F0`.

No runtime or controlled PBO boundary verification was performed. DayZ boot, Enforce compilation, client/server distribution, mounted-path behavior, `requiredAddons`, `verifySignatures=2`, serverMod enforcement, and Workshop behavior remain outside this revision.
