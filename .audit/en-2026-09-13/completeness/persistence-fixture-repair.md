# Entity Persistence Fixture Repair Receipt

**Date:** 2026-09-14  
**Repository HEAD when checked:** `bbfa203d036e8f02c733e50011c89b9dfbdf9ecf`  
**Scope:** supersedes the implementation assertions rejected as EPF-C03 through EPF-C07 in `persistence-fixture-council.md/json`. The original implementation and council reports remain historical evidence and were not edited.

## Result

The isolated archive scaffold was repaired and freshly packaged for `v1`, `v2`, and `matrix`. The helper now requires a disposable repository `TEMP/entity-persistence-repair` work root, creates a unique run beneath it, keeps Addon Builder's `-clear` path beneath that run, rejects the repository root or its ancestors, renames the sole fresh archive to the manifest's `EntityPersistenceFixture.pbo`, and checks the requested prefix plus the complete source-derived member set with BankRev.

`matrix` replaces the global bad-writer variant. Its `[NonSerialized()] m_OmitLockedOnSave` is `false` by default and is only consulted by `OnStoreSave`; the instance setters and getters allow a future harness to label a bad entity separately from normal v2 controls. `v1`, `v2`, and `matrix` validate the schema before schema-specific reads, stop at each required failed read, propagate and mark parent failure, mark unsupported schemas, and emit `LOAD_OK` or `LOAD_FAIL` with the case label, `GetPosition()`, and four `GetPersistentID(...)` blocks.

## Fresh archive receipts

All three runs used the installed `AddonBuilder.exe` version `1.0.240.639`, SHA-256 `C113DE9CAB5E91D27CA0630E360DB0A3ECA190EC797E1DCAD9CDFA70466B45E1`, and `BankRev.exe` version `1.0.0.2`, SHA-256 `2C35799EB437DEACB3720F8D322A399D935739537EBA335839E873AA21A26A75`. Each receipt records the `-packonly` command, two expected members, the actual prefix, source hashes, and hashes of Addon Builder, BankRev properties, and BankRev member logs.

| Variant | Fresh run | Canonical PBO / SHA-256 | Addon Builder log SHA-256 |
|---|---|---|---|
| `v1` | `TEMP/entity-persistence-repair/entity-persistence-v1-20260914-014139-5db8983a` | `EntityPersistenceFixture.pbo` / `B08F692885597DE0FE87DC3C82F25C49696BA93CCFDA7AAA5F42BB801DA45D79` | `1CC411424CE07B88C9BCA95B42F4FA3D371005BF760962603D09253F7838DC39` |
| `v2` | `TEMP/entity-persistence-repair/entity-persistence-v2-20260914-014152-c2958384` | `EntityPersistenceFixture.pbo` / `A499F69E2A801226D6200941EC2965E9F778A6CFD61A716F38EF9BEA4DF5C5CA` | `5F22AE65CADF7CE3920753E26FA725FB4E44851D6CD9737AFD7CEB6444F649EB` |
| `matrix` | `TEMP/entity-persistence-repair/entity-persistence-matrix-20260914-014154-34d9c618` | `EntityPersistenceFixture.pbo` / `94950B74AD00A1B7658BA54C5B40A4A85C6101BA0FC47E48F11BA2EA34933782` | `D96C8F923AC12BFED57E7908F59F14F106C695D14CAC39754EBDFBCDBC50E4F9` |

Every properties log hashes to `566CF2D405F145D6E57560A3B91F5A13147DC2460CD2BD2741FB29E45DEB22A1`; every member log hashes to `A4D6294CCAFF3BA4CE181CFCC86B27F49AD1F4FD891DC5C39789064194F4B934`. The only listed members are `EntityPersistenceFixture\config.cpp` and `EntityPersistenceFixture\scripts\4_world\entitypersistencefixture\entitypersistencefixturebattery.c`, case-insensitively matched to the complete source-derived set.

## Static checks

- PowerShell AST parser: passed for `examples/en/entity-persistence/build.ps1`.
- Dangerous-root check: invoking the helper with `D:\StarDZ\docs\wiki` produced `WorkRoot must not be the repository root or an ancestor of it.` before any packer operation.
- Manifest JSON parse: passed; it declares exactly `v1`, `v2`, and `matrix`, with canonical `EntityPersistenceFixture.pbo`.
- No DayZ game, dedicated server, client, Workbench, standalone compiler, VitePress dev server, or VitePress build was launched.

Archive packaging proves only the named PBOs and BankRev inspection. It does **not** prove config parsing, script-module loading, Enforce compilation, persistence save/load, serializer behavior, record isolation, or runtime assertion results.

## Raw source hash ledger

“Before” is the exact raw SHA-256 recorded by the rejected council delivery. Unchanged files retain their hash; `declared-v2-missing-field` was renamed and replaced by `matrix` as the requested per-instance matrix implementation.

| Path | Before | After |
|---|---|---|
| `examples/en/entity-persistence/README.md` | `568E0102C7DBA4A65251CAD27E4B11916BC7BF070293D4C847297E2BBFA3AEAA` | `8C762FC90C02B097ACCD41F83CAA672B597F811565583C63C4A2938B34F31FFF` |
| `examples/en/entity-persistence/manifest.json` | `41861A5D91D079C4FC96D6CDEC60F62225546A0C420F7ADD8ACFE957CD4CCF44` | `4701E996F8A0A01EE6D28C20779E1D5C843019AC452C728DECA2A25B377D69E9` |
| `examples/en/entity-persistence/build.ps1` | `D85843609BAE0395B6975BC19EA1FD61F06ABDBAC7C07DCB3F01C7C4DC30F6D8` | `B70F3C378EEE774501424B71A683742A3349FD7CEA58259A2CE3FD86E6DC44C7` |
| `variants/v1/config.cpp` | `D9AB275AD77AE11CB5CC32EE7F7B8A16D81157C1ED554F1A2B04C3DBE26AF241` | `D9AB275AD77AE11CB5CC32EE7F7B8A16D81157C1ED554F1A2B04C3DBE26AF241` |
| `variants/v1/.../EntityPersistenceFixtureBattery.c` | `0BA2A5B2848895869D6D00B22DC9B571211BDD3CB048959A291AB0A6D75345E9` | `CD15FEBB6559B767D9ECC50F2632DC3D9F52D44326E72C6163C590607BD28205` |
| `variants/v2/config.cpp` | `04295EC0927CF0ACF0913F2071765F70D87BD8ECB93DD4A74B71E4892AFF9C00` | `04295EC0927CF0ACF0913F2071765F70D87BD8ECB93DD4A74B71E4892AFF9C00` |
| `variants/v2/.../EntityPersistenceFixtureBattery.c` | `5D0CD1745B654348937F972FED39BD1B5A43BB8682C128DE949A94CA0755326C` | `4D745BE004293FDA27F094FF50BF473D1DD835969038DC0DB7B59DC9D565D85A` |
| `variants/declared-v2-missing-field/config.cpp` → `variants/matrix/config.cpp` | `27CDE1B215676C87F0CF8811F7D6D9ECE511F1EF6C7E659C151F09E67B0C1B91` | `04530A93C2C6D4E7FF5EA72C5BC1D25CCA3CF31DD0E985AFECB3BD59BBF3186E` |
| `variants/declared-v2-missing-field/.../EntityPersistenceFixtureBattery.c` → `variants/matrix/.../EntityPersistenceFixtureBattery.c` | `963F91C1BE77E6EB02F82B80E05726553E0AA663C0F849581B5BA2E4B23A8C74` | `A3A8FCD3387773D915A31C2CA5035C07FB8A49CE7877867D37E629E2081A090D` |

## Source-use ledger

| Classification | Source opened | Exact version / hash | Use in this repair |
|---|---|---|---|
| Extracted DayZ snapshot | `D:/DayZ Projects/scripts/4_world/entities/itembase/battery9v.c` | SHA-256 `98D4376AEF70324F7C9FD4DDEB5098D6E0B731EE9CDB4352A6A7166C03838A34` | Confirmed `Battery9V : ItemBase` before retaining the configured leaf base. |
| Extracted DayZ snapshot | `D:/DayZ Projects/DZ/gear/consumables/config.cpp:913-957` | SHA-256 `360DF711C194F9264C232C9296FD4DA5B92EBCE731FC25E0908036EA07CB745B` | Rechecked the vanilla `Battery9V` config entry. |
| Extracted DayZ snapshot | `D:/DayZ Projects/scripts/3_game/entities/entityai.c:2913-3070,3378-3380` | SHA-256 `AD08181C307BE03549ABC8AFD6A6CEB8532ECA88DA5DA648686CA9FD682A57F5` | Rechecked callback ordering/read failures and the available `GetPersistentID(out int, out int, out int, out int)` API used in diagnostics. |
| Extracted DayZ snapshot | `D:/DayZ Projects/scripts/1_core/proto/serializer.c:1-65` | SHA-256 `3C365E5EF418438220CD2A2012C57EF385DDCAD835D712D136D31E6DFE7D2F5D` | Rechecked `Read`/`Write` boolean declarations and `[NonSerialized()]` documentation. |
| Extraction metadata | `D:/DayZ Projects/scripts.txt` | raw `product=dayz`, `version=124588`; SHA-256 `E45D501E4FB29587FA1E8BF553B0A7B33B751AA32C5AA5ECB1D03B8B6026F55F` | Records only the snapshot's raw metadata, not a claimed game build identity. |
| Official Samples | `https://github.com/BohemiaInteractive/DayZ-Samples.git`, `Test_GardenPlot/config.cpp` | commit `da5e5437c9502620d9853fb6eed14701135ab2ea`; SHA-256 `2C66BE131A55CFFDED96712245DD74D78E25D003C21A4F51F0B94587C666CD37` | Reopened the `worldScriptModule` config pattern. |
| Third-party reference | `https://github.com/Arkensor/DayZ-CommunityFramework.git`, `CF_ModStorageObject.c`, `CF_ModStorage.c` | commit `0763e7e7548c9a0bed6626afff835de80693ebf3`; SHA-256 `4B37540E26D7F708AA8B53715C7D11B2F95C7FC18A9E7ADBF5D6E244A9B6F242`, `6FCF72DDC889D751F02BE1097DBC19126F851E7712A90EC2F52FA61B4E59D7B0` | Reopened as a non-authoritative framing/version comparison; no CF behavior was claimed as vanilla behavior. |

## Remaining gates

The separate harness research for Central Economy eligibility, spawn-once controls, save timing, and graceful shutdown is pending; this repair intentionally does not fill those gaps. Still required are independent review of this exact repair, a council-approved compile/config-load smoke gate, and then a controlled runtime matrix with fixed positions, persistent-ID capture, setter/getter assertions, storage hashes, and clean exit evidence.
