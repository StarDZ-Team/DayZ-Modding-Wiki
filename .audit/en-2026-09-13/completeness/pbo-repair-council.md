# PBO Repair Council

**Review date:** 2026-09-13  
**Repository state:** `wiki-reorg` at `9dc36064459f3184404bdba4db9d95b843b6fcaa`  
**Reviewer runtime:** Codex `gpt-5.6-sol`, high effort; PowerShell `7.6.0`; Windows `10.0.26200.0`  
**Scope:** independent final review of the six rejections in `pbo-final-council.md`. No English page or fixture file was edited, no child agent was used, and no game/client/server was launched.

**Decision:** **accept all six repairs and the exact hash-identified PBO research/evidence/fixture bundle for a scoped commit.** This is approval of the repaired static research and tool-tested fixture only, not a full-wiki or DayZ-runtime approval.

---

## Six repair dispositions

| # | Prior rejection | Disposition | Independent basis |
|---:|---|---|---|
| 1 | Missing `01-five-layers.md` source object | **Accepted** | `WIKI-FIVE-LAYERS` occurs once in `pbo-evidence.json`; the recorded path exists, the full-file review scope and line ranges are present, and recorded/actual SHA-256 both equal `1C8571C015339DD7508D92C519A0F6A563B3790D5120ED776832EFBA345C8413`. |
| 2 | DSCheck acceptance was not exhaustive | **Accepted** | The exact current function was loaded from the parsed `build.ps1` AST. It accepted the three-line valid package result and rejected duplicate and unexpected lines. Fresh installed-tool probes returned exit `0` for partial, missing-key, and wrong-signature sets, while the repaired parser rejected `No signature found`, `Key not found`, and `is wrong` respectively. |
| 3 | Collision scan occurred after signing | **Accepted** | Static review confirms phase 1 builds, final-names, BankRev-inspects, and collects all components; the global collision scan precedes the first `Get-FileHash`, `DSCreateKey`, or `DSSignFile`. A fresh duplicate-prefix run failed with four built PBOs but zero `.bisign`, zero private keys, and zero receipts. |
| 4 | BankRev members were whitespace-tokenized | **Accepted** | The current parser splits complete trimmed lines and enforces `normalizedPrefix + '/'`. Synthetic exact-boundary testing rejected `PBOExample/Database`; a fresh packed member named `data/member name.txt` remained one receipt member line. |
| 5 | `WorkRoot` could write into the fixture | **Accepted** | Both the exact `examples/en/multi-pbo` directory and a nonexistent descendant were rejected before tool use. The guard derives the protected fixture root from `$PSScriptRoot`, so a copy of the fixture protects its own tree without hard-coding this checkout path. The current fixture contains zero generated PBO, signature, key, log, or receipt files. |
| 6 | Required rerun matrix and regenerated receipts absent | **Accepted** | The author receipts and retained success/negative outputs were reopened and matched. Fresh council runs independently covered success, partial/missing/wrong signatures, duplicate collision, bad tool directory, stale parent output, fixture/descendant guards, and a spaced member name. |

No further repair is required by this council.

---

## Evidence and retained revision verification

The unchanged research report still hashes to `03FE483067A9259D6C0601A2F6FF9C9C7B6601201FAB6982343A8A15582D7949`, the exact report whose substance the prior final council accepted. I relied on that council's already independent 47 checks for the unchanged evidence set and reopened the new, changed `WIKI-FIVE-LAYERS` object and its source rather than repeating the full research wave. The repaired ledger hashes to `38E257ED0D88E286C84E24828068B9F5C96E58F0F4B0D2375EA427ED6AFE1BBA`.

The retained author success receipt at `TEMP/pbo-second-revision/success-work/pboexample-20260913-211644-14a6980d/receipt.json` hashes to `B9CD721C3B3C4AB59CC8C9822A6D1A28B1C1E8E72A65044E87C8FB61A9129E51`. Its four recorded PBO hashes, four `.bisign` hashes, and all BankRev member-line arrays match the retained files. The partial, missing-key, wrong-signature, bad-tool, duplicate, fixture-guard, stale-parent, and spaced-member outputs also exist and have the hashes recorded in `pbo-repair-council.json`.

The current repair receipts hash to:

- `pbo-revision.md`: `9826B798CA2E3AA0CFEEA7F700AF98F6BAAD5F0AFCBE0396812C9C73F23CDD29`
- `pbo-revision.json`: `5A8079BD674250BB66520C52F3D207003A28B94A01D3E58B59B89C6FD61C3DEA`

---

## Fresh independent execution

The current runner completed successfully with exit `0`:

```powershell
.\examples\en\multi-pbo\build.ps1 -ToolRoot 'D:\SteamLibrary\steamapps\common\DayZ Experimental Tools' -WorkRoot 'D:\StarDZ\docs\wiki\TEMP\pbo-repair-council\success-work'
```

Run root: `TEMP/pbo-repair-council/success-work/pboexample-20260913-212942-d64b7020`  
Receipt SHA-256: `CFF0D666723C8EF7DC34F874C1D05A4ADBEED14CC821F0371528EC1B72639C43`

The release contains four PBOs, four `.bisign` files, no private key, seven normalized members, and two exhaustive DSCheck package results. The shared package reported exactly three expected/OK signatures; the server package reported exactly one. Independent BankRev extraction reproduced all seven source members byte-for-byte.

| Component | PBO SHA-256 | `.bisign` SHA-256 | Members |
|---|---|---|---:|
| Core | `7D7D0749107BB888E328D9FF335154DAADF7588E8858EB0B11A47C40E6E24918` | `F57D798F7157B52F5D1AD59E61AF07301EFF11B3D7D0512F0E9D30D67D505C58` | 1 |
| Scripts | `435094EC2CCA116144B300524E017C6B4F70B6E8D9E2C574F6E448B0EA07A75D` | `9F130C7BF8E8D75186E0A626C4D27800D3F8D1EF1B151D7CEEA884FAF88B90B5` | 2 |
| Data | `9DB370CA067894ACB7BF6A5D3213F842ED9B1BFA7948B4D52032C27947C44A5C` | `0A9CFA9F8DB7ACD417DB32E9D5C0A63880DC4CC196405569C7FCC1C9F7BD0A71` | 2 |
| Server | `96C734B4BAD436D194DC3DC9E0AA05E3A616C62CC6B5B03483C7D3C6CBB38503` | `BBC930DFD6F6FEA5758AB4F53B64889CFA5E8BF08175F252B4870475764D57B6` | 2 |

Fresh negative and edge results:

- Partial signature set: tool exit `0`, two `is OK` lines plus `No signature found`; parser rejected.
- Empty keys directory: tool exit `0` plus `Key not found`; parser rejected.
- Wrong signature: tool exit `0` plus `is wrong`; parser rejected.
- Duplicate Core/Data normalized member: build failed before hashing/signing; four PBOs, zero signatures, zero private keys, zero receipt.
- Bad tool directory: Addon Builder exit `0` with `[ERROR]`, zero PBO; `Invoke-Tool` rejected.
- Stale parent marker remained byte-identical while a fresh timestamped child run succeeded.
- Spaced member run succeeded and retained `PBOExample/Data\data\member name.txt` as one line.
- Fixture root and descendant `WorkRoot` probes both failed before tool use.

`build.ps1` parsed without PowerShell syntax errors, and both JSON artifacts parse successfully. A VitePress build was not run because neither English content nor the fixture was changed by this review; the executable fixture checks are the directly relevant validation.

---

## Exact scoped content hashes

| Path | SHA-256 |
|---|---|
| `.audit/en-2026-09-13/completeness/pbo-research.md` | `03FE483067A9259D6C0601A2F6FF9C9C7B6601201FAB6982343A8A15582D7949` |
| `.audit/en-2026-09-13/completeness/pbo-evidence.json` | `38E257ED0D88E286C84E24828068B9F5C96E58F0F4B0D2375EA427ED6AFE1BBA` |
| `examples/en/multi-pbo/README.md` | `3449B09BBDD04A278A17DD8E3A79A1D27EEB76B173431A73A255C52EE23BC0CE` |
| `examples/en/multi-pbo/build.ps1` | `38F24D830DBCB7985ABF1ED9636493C5BDFEA1E160169379FE10E8F50BADB956` |
| `examples/en/multi-pbo/manifest.json` | `63D5E5E9468AF98B37B30AB71C3CCEA69D45694E266377025F68E6953F088582` |
| `examples/en/multi-pbo/src/Core/config.cpp` | `E45F745E19E2EF1943A477E66B202D70D10A14A275EC6C7CE4FD56F80C2D712F` |
| `examples/en/multi-pbo/src/Scripts/config.cpp` | `0C2DB149738083D7FDA1F616051C7F0C8C548B0175222369F1171A1FA197D787` |
| `examples/en/multi-pbo/src/Scripts/scripts/3_Game/PBOExample.c` | `537D9A11B33ED7CCBF2DC7A41353F457629EC9CEBDF96EB01D53652B6E7ACF8B` |
| `examples/en/multi-pbo/src/Data/config.cpp` | `AB459018DC30DD5188820398E56B16A3DA426929BB0111C4A3F47819DCED5F31` |
| `examples/en/multi-pbo/src/Data/data/example.txt` | `C460C6E58E3051A463E565F55D835469415E3536B9EF6095178D3D60041CB941` |
| `examples/en/multi-pbo/src/Server/config.cpp` | `4FA89581708F159CFCA491252F494A5E9A6A1AE003D165370EA3F12F5245E102` |
| `examples/en/multi-pbo/src/Server/scripts/5_Mission/PBOExampleServer.c` | `CCECF9E3AEDC044CA44A3C22537BE504BEE5AC71042EA4E6EA8DAA1567F12373` |
| `examples/en/multi-pbo/package/Shared/mod.cpp` | `8A3FB89471F6CA617674B997EFA37AF2DDCC2DB33DC471C68320D58A2FF2CFA9` |
| `examples/en/multi-pbo/package/Server/mod.cpp` | `726A2E560854E619DD2A851F5E9EA08D216D673278452CC8C6C5AE449C1DC2C8` |

---

## Explicit unresolved gates

This acceptance does not resolve or validate:

- DayZ boot, Enforce compilation, mounted `CfgMods` paths, client join/distribution, or missing/renamed `requiredAddons` behavior.
- Numeric PBO format, entry, total-archive, compression, tool, engine-loading, or distribution limits; no controlled boundary matrix was run.
- `verifySignatures=2` enforcement for valid, modified, missing, wrong-key, or rotated-key cases, including whether serverMod-only PBO signatures are operationally enforced. DSCheck here is only a bounded tool-output check and is not PBO-byte-binding or server-enforcement proof.
- Steam Workshop upload, download, update, or service-side limits and behavior.

Those remain assigned to runtime/limits/service follow-up work and must not be inferred from this scoped static-and-tool approval.
