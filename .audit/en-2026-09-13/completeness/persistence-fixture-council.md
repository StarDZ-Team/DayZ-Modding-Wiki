# Independent Council: Entity Persistence Fixture

**Review date:** 2026-09-14  
**Role:** independent reviewer; not the author  
**Repository revision:** `63fde8a84c4766ab7e587afa811882b7dccdf448`  
**Reviewed delivery:** `examples/en/entity-persistence/` plus `persistence-fixture-implementation.md` / `.json` and all retained `TEMP/entity-persistence-fixture/` receipts, logs, PBOs, and BankRev member listings  
**Decision:** accept the package-only scaffold and its archive receipts with the qualifications below; reject any claim that the required migration fixture, executable matrix, Enforce compilation, or healthy persistence is complete.

No game, server, client, Workbench, development server, full VitePress build, packer, or compiler was launched by this council. The only validations run were read-only source/config/report inspection, SHA-256 hashing, JSON parsing, and PowerShell AST parsing.

---

## Executive decision

The delivery is a useful and mostly coherent **packaged scaffold**. All three variants have the same `CfgPatches` identity, configured entity classname, base class, virtual prefix, 4_World module path, and custom field order appropriate to their stated layouts. The final retained receipts match the current variant-source hashes; Addon Builder logged `Build Successful`; BankRev recorded prefix `EntityPersistenceFixture\` and the two expected members.

That acceptance stops at packaging. The helper emits `v1.pbo`, `v2.pbo`, and `declared-v2-missing-field.pbo`, not the manifest/report/README's claimed common `EntityPersistenceFixture.pbo`. More importantly, the missing-field writer is a globally selected class implementation: the README correctly says not to install two variants together, so every `EntityPersistenceFixtureBattery` in a bad-writer run uses the bad writer. There is no per-instance switch with which one entity can omit `locked` while separately identified valid v2 controls write it. The proposed bad-writer-plus-valid-control matrix is therefore not executable as delivered.

The scaffold also has no mission or operator harness, no deterministic spawn-once mechanism, no per-instance case label/setter and assertion API, no established custom-class Central Economy registration/lifetime rule, no controlled save trigger, and no clean-shutdown implementation. The README marks the mission harness and generic save/clean-shutdown mechanism as future work, but it does not explicitly mark the missing per-instance bad-writer control and still presents the mixed-control step as a future runnable procedure. Packaging cannot substitute for any of those prerequisites.

---

## Finding dispositions

### EPF-C01 — accepted: configured package scaffold

The three `config.cpp` files differ only in `descriptionShort`. They consistently declare:

- patch `EntityPersistenceFixture` with `requiredAddons[] = { "DZ_Gear_Consumables" }`;
- configured class `EntityPersistenceFixtureBattery : Battery9V`;
- a `worldScriptModule` rooted at `EntityPersistenceFixture\scripts\4_World`;
- raw virtual prefix `EntityPersistenceFixture` and the same script member path.

The extracted source independently confirms `Battery9V : ItemBase`, the `Battery9V: Inventory_Base` config/model, and the vanilla patch name `DZ_Gear_Consumables`. The official DayZ Samples checkout at commit `da5e5437c9502620d9853fb6eed14701135ab2ea` confirms the basic `CfgPatches`/`CfgVehicles` pattern in `Test_Building/config.cpp` and the `worldScriptModule`/`files[]` pattern in `Test_GardenPlot/config.cpp`. CF commit `0763e7e7548c9a0bed6626afff835de80693ebf3` independently demonstrates ordered script modules and a 4_World path, but CF remains third-party evidence.

This is static configuration review only. Because `-packonly` retained `config.cpp` and did not compile Enforce Script, this finding does not approve config parsing, module loading, class resolution, or script compilation.

### EPF-C02 — accepted: archive-only receipts, with a supersession qualification

Seven retained package runs were inspected. Six contain receipts; the earliest v1 run has successful Addon Builder and BankRev logs plus a PBO but no `receipt.json`, so it is an unreceipted preliminary artifact. The three `final-build` receipts are the relevant current-source receipts:

| Variant | Actual output | Bytes | SHA-256 | Receipt SHA-256 |
|---|---|---:|---|---|
| v1 | `v1.pbo` | 2373 | `146890DF99DC32188BB87C39D39ECE3A2A11E9A77B4E50042178D0CFE2FE0730` | `AF62F2264AB2217710972A4D9DEC121D4E333511DCA561B5F85CA9DE3BF3636C` |
| v2 | `v2.pbo` | 3111 | `1EAC1A7207E94EE346C789AD78076DA81E101CDED1B0D4E0E2DCD8C908719A3A` | `45AF99453B74DE64B40395C11B3D8A746E68C6FE5EFDA784FBA60D2F03D2C703` |
| declared-v2-missing-field | `declared-v2-missing-field.pbo` | 2621 | `73E348B80FCDF4516BFD95815A56DC3D6A34C1B8386A4431625BB0DEA3CB6753` | `40FCDDA9123FF5EBC8CE85CD5435723F21C5457BE5EE7B4E92415B627507FDDF` |

All final receipts contain the current config/script hashes. All retained BankRev property logs have SHA-256 `566CF2D405F145D6E57560A3B91F5A13147DC2460CD2BD2741FB29E45DEB22A1` and report `prefix = EntityPersistenceFixture\`. All member logs have SHA-256 `A4D6294CCAFF3BA4CE181CFCC86B27F49AD1F4FD891DC5C39789064194F4B934` and list:

- `EntityPersistenceFixture\scripts\4_world\entitypersistencefixture\entitypersistencefixturebattery.c`
- `EntityPersistenceFixture\config.cpp`

These facts prove archive production, the recorded property, and those member names only. They do not prove that the internal config parses, that the script compiles, that the module is loaded, or that callbacks run.

### EPF-C03 — rejected: common PBO-name claim

`manifest.json` declares `"pbo": "EntityPersistenceFixture.pbo"`, the README says all variants have the same PBO name, and both implementation reports repeat that claim. `build.ps1` never reads `manifest.pbo` and accepts whatever single PBO Addon Builder emits. The actual logs and receipts show variant-directory-derived names: `v1.pbo`, `v2.pbo`, and `declared-v2-missing-field.pbo`.

**Exact repair:** make the helper copy or rename the sole produced archive to `manifest.pbo`, fail unless the final name is exactly `EntityPersistenceFixture.pbo`, record both original and canonical output names if provenance matters, and rebuild/reinspect all variants. Alternatively, remove the common-name claim everywhere and document an explicit, verified deployment rename. Do not leave an unused manifest invariant.

### EPF-C04 — rejected: bad-writer plus valid-control matrix is not possible as delivered

The bad behavior is compiled into the only `EntityPersistenceFixtureBattery.OnStoreSave` implementation in the `declared-v2-missing-field` variant. The v2 implementation always writes `locked`; the bad variant always omits it. Because only one variant may be installed, there is no run in which one instance is the bad writer and neighboring or otherwise separately identified instances are valid v2 writers. Timed or shutdown saves could rewrite every control under the selected global implementation, so pre-existing controls do not repair this design.

**Exact repair:** provide a single council-reviewed matrix build in which a non-persisted per-instance flag controls only whether `locked` is written. The harness must set that flag on exactly one identified entity and leave it false on at least two separately identified controls. Add setters for a unique persisted case label and the locked value, plus getters or explicit success/failure assertion markers. On restart, use the normal schema-v2 reader for all instances; do not persist the omission-control flag. Keep the v1 and normal-v2 upgrade identity unchanged.

Until that exists, change the README and implementation reports to say explicitly:

> The delivered variants do not implement per-instance writer selection. Therefore a declared-v2 missing-field record cannot yet be generated in the same controlled save as valid v2 controls; the bad-writer/control matrix is not runnable.

### EPF-C05 — repair required: read validation and diagnostic markers

The basic layouts are coherent:

- v1 writes and reads `schema`, `charges`, `label`;
- v2 reads the common fields, maps schema 1 to `locked = false`, and reads `locked` for schema 2;
- the bad writer declares schema 2 but omits `locked` while its reader requires it.

However, v1 and the bad reader execute later reads even when an earlier required read failed, then return a conjunction. This conflicts with the reopened `EntityAI` example and the prior council wording to return immediately after a required `Read` returns `false`. The v2 reader also waits until after reading `charges` and `label` to reject an unsupported schema. Current grouped logs do not identify parent-load failure, unsupported schema, or a unique entity/case, and there is no single unambiguous `LOAD_OK` marker.

**Exact repair:** after `super`, log and return immediately on parent failure; read and validate the schema before any schema-dependent fields; reject values other than 1 or 2 before consuming the common fields; check/log each required read before attempting the next; and emit explicit terminal markers such as `LOAD_OK`, `LOAD_FAIL stage=<field>`, schema, case label, position, and persistent-ID blocks. The bad reader may then distinguish the expected `locked` failure without obscuring an earlier failure.

### EPF-C06 — accepted with limits: PowerShell construction and archive checks

PowerShell AST parsing returned zero errors, and `manifest.json` parsed successfully. The helper uses `PSScriptRoot`, `Resolve-Path`/`GetFullPath`, `-LiteralPath`, a unique timestamp-plus-GUID run directory, and sends Addon Builder's `-clear` to a newly created temp directory under that run. It rejects a `WorkRoot` equal to or below the versioned fixture directory and does not itself recursively delete or move files. Within its documented disposable-work-root use, the destructive scope is reasonably bounded.

The archive checks are narrower than the manifest and reports imply. They require one non-empty PBO, a matching BankRev prefix, and presence of two members, but they do not enforce the manifest PBO name, reject unexpected members, hash extracted member contents, parse `config.cpp`, or compile scripts. `$inspectRoot` is created but unused. A repository ancestor is also accepted as `WorkRoot`, which can pollute the checkout even though the unique child limits destructive risk.

**Exact repair:** enforce the canonical PBO name; compare the complete normalized member set against the expected set (or record justified extras); record receipt/log hashes; ensure the newly selected run path did not pre-exist and resolves inside the requested disposable root; and reject the repository/fixture tree and their ancestors as work roots. Keep config parsing and Enforce compilation as separate gates rather than describing these archive checks as either.

### EPF-C07 — repair required: source ledger precision

The implementation correctly limits CF's significance and correctly cites the extracted serializer and persistence hooks. It must add the previously omitted hashes for the reopened `Battery9V` script and consumables config. It must also pin the official Samples evidence in the report and cite `Test_GardenPlot/config.cpp` for `worldScriptModule`; `Test_Building/config.cpp` does not contain that module block.

**Exact repair:** record official repository `https://github.com/BohemiaInteractive/DayZ-Samples.git`, commit `da5e5437c9502620d9853fb6eed14701135ab2ea`, clean checkout observation on 2026-09-14, exact paths/symbols, and the hashes in the ledger below.

### EPF-C08 — unresolved and required: harness and persistence prerequisites

`SetFixtureLocked(bool)` is not a harness. There is no 5_Mission code or mission `init.c`, spawn-once guard, selected coordinates, unique per-case identity, cleanup/reset procedure, assertion routine, save trigger, clean shutdown controller, or storage snapshot collector. The custom classname also has no delivered `types.xml` entry, while the extracted world economy files register `Battery9V`, not `EntityPersistenceFixtureBattery`. This council does not infer whether inheritance alone makes the custom class eligible for the intended world persistence path.

Before a persistence test, a reviewed harness plan must establish:

1. an isolated `@EntityPersistenceFixture/Addons/EntityPersistenceFixture.pbo` deployment and exact mod order;
2. a known-good disposable mission/profile/storage path and the custom class's CE/persistence registration and lifetime behavior;
3. deterministic spawn-once behavior with fixed, recorded positions and persistent-ID blocks;
4. per-instance case labels, normal/bad writer selection, locked-value setters, and readback/assertion markers;
5. a source-backed save trigger or a precisely controlled wait, plus an externally controlled graceful shutdown whose exit is recorded;
6. storage and log hashes before/after every transition and a restore procedure for the preserved v1 baseline;
7. a rule preventing startup from respawning duplicate fixtures after reload.

The README already acknowledges the missing mission harness and generic save/clean-shutdown API; the implementation is still incomplete until these are supplied and independently reviewed.

---

## Smallest compilation gate before runtime persistence testing

The smallest justified Enforce gate is a **disposable dedicated-server startup smoke**, separated from the persistence matrix: deploy the canonical PBO with only the required base game and a known-good minimal mission, start a pinned/hash-recorded server build with isolated profile/log paths, and require evidence that configuration loading, `worldScriptModule` compilation, `Battery9V` inheritance, and `EntityPersistenceFixtureBattery` class resolution complete without script/config errors. Then stop cleanly without spawning the fixture or interpreting any persistence behavior.

Addon Builder `-packonly` and BankRev cannot satisfy this gate. A standalone Enforce compiler command was not established in the reopened evidence, so this council does not invent one. Before the smoke launch, repair the PBO naming invariant and diagnostic source, deliver the minimal mission/deployment files and exact launch/exit procedure, and have an independent reviewer inspect them. Only after that smoke passes should the save/restart matrix begin.

---

## Mechanically generated source hashes

### Reviewed delivery

| Path | SHA-256 |
|---|---|
| `examples/en/entity-persistence/README.md` | `568E0102C7DBA4A65251CAD27E4B11916BC7BF070293D4C847297E2BBFA3AEAA` |
| `examples/en/entity-persistence/manifest.json` | `41861A5D91D079C4FC96D6CDEC60F62225546A0C420F7ADD8ACFE957CD4CCF44` |
| `examples/en/entity-persistence/build.ps1` | `D85843609BAE0395B6975BC19EA1FD61F06ABDBAC7C07DCB3F01C7C4DC30F6D8` |
| `variants/v1/config.cpp` | `D9AB275AD77AE11CB5CC32EE7F7B8A16D81157C1ED554F1A2B04C3DBE26AF241` |
| `variants/v1/.../EntityPersistenceFixtureBattery.c` | `0BA2A5B2848895869D6D00B22DC9B571211BDD3CB048959A291AB0A6D75345E9` |
| `variants/v2/config.cpp` | `04295EC0927CF0ACF0913F2071765F70D87BD8ECB93DD4A74B71E4892AFF9C00` |
| `variants/v2/.../EntityPersistenceFixtureBattery.c` | `5D0CD1745B654348937F972FED39BD1B5A43BB8682C128DE949A94CA0755326C` |
| `variants/declared-v2-missing-field/config.cpp` | `27CDE1B215676C87F0CF8811F7D6D9ECE511F1EF6C7E659C151F09E67B0C1B91` |
| `variants/declared-v2-missing-field/.../EntityPersistenceFixtureBattery.c` | `963F91C1BE77E6EB02F82B80E05726553E0AA663C0F849581B5BA2E4B23A8C74` |
| `persistence-fixture-implementation.md` | `12235F9984D6142EF1247C46261CECAF4C63822AF7C7B803BEB080EB393BD6E6` |
| `persistence-fixture-implementation.json` | `1318BBA4F35B003956ED2EE229ADF872246D938EC55EF78FF681BEFC6BA7E82A` |
| prior `persistence-source-council.md` | `317093AD43155012AE0EBBA136CBD730C98239210F2C3650AADA257FFAC15398` |
| prior `persistence-source-council.json` | `5BA2DDF9531365447183944ADA17E93F7195DA52850CC646147DA921F78A821F` |

### Reopened primary and pinned sources

| Classification | Path / revision | SHA-256 | Use |
|---|---|---|---|
| Extracted DayZ snapshot | `D:/DayZ Projects/scripts/4_world/entities/itembase/battery9v.c` | `98D4376AEF70324F7C9FD4DDEB5098D6E0B731EE9CDB4352A6A7166C03838A34` | Actual script base class; no direct persistence override |
| Extracted DayZ snapshot | `D:/DayZ Projects/DZ/gear/consumables/config.cpp` | `360DF711C194F9264C232C9296FD4DA5B92EBCE731FC25E0908036EA07CB745B` | Patch name and Battery9V config/model |
| Extracted DayZ snapshot | `D:/DayZ Projects/scripts/3_game/entities/entityai.c` | `AD08181C307BE03549ABC8AFD6A6CEB8532ECA88DA5DA648686CA9FD682A57F5` | Callback hierarchy, order, reads, engine-version branches |
| Extracted DayZ snapshot | `D:/DayZ Projects/scripts/1_core/proto/serializer.c` | `3C365E5EF418438220CD2A2012C57EF385DDCAD835D712D136D31E6DFE7D2F5D` | `Read`/`Write` boolean declarations |
| Extracted DayZ snapshot | `D:/DayZ Projects/scripts/3_game/gameplay.c` | `AA12624843F51C70200D37449559FDBADB042D333D4EE74C989E0CA632D2F0FE` | Context aliases |
| Extracted DayZ snapshot | `D:/DayZ Projects/scripts/4_world/entities/core/inherited/itemoptics.c` | `814AB79D363BCC0AF6FB3434D391FE1059840562DCC0A5001193B489DE03B9B3` | Parent-first and version gate |
| Extracted DayZ snapshot | `D:/DayZ Projects/scripts/4_world/entities/itembase/basebuildingbase.c` | `22283A8E3869CAF8CE1D6BFE5606057575C4F2C315E766723D3F44DAA7E47F4F` | Ordered reads/writes and fail-fast pattern |
| Extracted DayZ snapshot | `D:/DayZ Projects/scripts/4_world/entities/itembase/basebuildingbase/fence.c` | `38059886AF6313CF8442D1362A183021A863616E1CD12878D6663BFCC1C65B60` | Compatibility branch and stream position |
| Extracted DayZ snapshot | `D:/DayZ Projects/scripts/3_game/global/game.c` | `CF529055C48596108034CE6B11826B09BBF5D93E6C550E37785947873D8C3158` | `CreateObjectEx`; engine storage registration in prior review |
| Extracted DayZ snapshot | `D:/DayZ Projects/scripts/5_mission/mission/missionserver.c` | `92A2FF171ED550BF2E93E7C983479613CFB0EE7A521D7C1958CECA9647B786F0` | `MissionServer.OnInit`; not a delivered harness |
| Extraction metadata | `D:/DayZ Projects/scripts.txt` | `E45D501E4FB29587FA1E8BF553B0A7B33B751AA32C5AA5ECB1D03B8B6026F55F` | `product=dayz`, raw `version=124588` only |
| Official Samples, commit `da5e5437...` | `Test_Building/config.cpp` | `3A6FB41F49D418637A8513383D3CB1E2F84B95EFE962EE0FD755F1B6268F56EE` | Basic configured-entity pattern |
| Official Samples, commit `da5e5437...` | `Test_GardenPlot/config.cpp` | `2C66BE131A55CFFDED96712245DD74D78E25D003C21A4F51F0B94587C666CD37` | 4_World module/files layout |
| CF, commit `0763e7e...` | `CF_ModStorageObject.c` | `4B37540E26D7F708AA8B53715C7D11B2F95C7FC18A9E7ADBF5D6E244A9B6F242` | Third-party framing boundary |
| CF, commit `0763e7e...` | `CF_ModStorage.c` | `6FCF72DDC889D751F02BE1097DBC19126F851E7712A90EC2F52FA61B4E59D7B0` | Third-party schema/type framing |
| CF, commit `0763e7e...` | `JM/CF/Scripts/config.cpp` | `8DA49AD88AB7387B4F5E6D5D2FDBC07005F908B537E7F723152BD41B6BDD1D41` | Script-module ordering example |

Tool hashes were independently recomputed: Addon Builder `C113DE9CAB5E91D27CA0630E360DB0A3ECA190EC797E1DCAD9CDFA70466B45E1`, BankRev `2C35799EB437DEACB3720F8D322A399D935739537EBA335839E873AA21A26A75`. Addon Builder file/product version is `1.0.240.639`.

---

## Unresolved after this council

- Enforce compilation, config parsing, module loading, and configured-class resolution.
- Custom-class CE/persistence eligibility and lifetime configuration for the selected mission.
- Native behavior for an omitted final field, wrong type, or bytes following the override.
- Runtime treatment of `OnStoreLoad(false)` and isolation of later entity records.
- Native forwarding of engine storage version into the callback parameter.
- Exact save timing/trigger and a demonstrated graceful shutdown path.
- v1 same-build persistence, v1-to-v2 migration, v2 `locked=true` resave/reload, and the mixed bad/control case.
- Shared inheritance patches, mod removal/reinstallation, and pre-marker legacy data.

The required migration fixture remains incomplete until the repairs and compile gate above are independently reviewed and passed.
