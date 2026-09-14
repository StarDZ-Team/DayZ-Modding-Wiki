# Independent council: entity-persistence scaffold repair

**Review date:** 2026-09-14  
**Role:** independent final reviewer; not the author  
**Repository HEAD:** `bbfa203d036e8f02c733e50011c89b9dfbdf9ecf`  
**Decision:** reject archive-scaffold integration pending three small code/config repairs. Full migration/runtime completion remains separately unresolved and is not a condition for this archive-only judgment.

No game, server, client, Workbench, compiler, Addon Builder, BankRev, VitePress build/dev process, install, commit, or sub-worker was run. This review used read-only source/report/log inspection, SHA-256 hashing, JSON and PowerShell AST parsing, and direct parsing of the three retained PBO headers and uncompressed payloads.

## Executive result

EPF-C03, the archive evidence portion of C04, C05, and the provenance portion of C07 are repaired in the inspected artifacts. Each fresh run contains exactly one canonically named `EntityPersistenceFixture.pbo`; direct PBO parsing found exactly `config.cpp` and the 4_World script, and each embedded payload hashes exactly to the corresponding current source. The three readers now fail fast at parent, schema, each required common field, and `locked`; the matrix flag is initialized `false`, marked `[NonSerialized()]`, and never passed to `ctx.Write` or `ctx.Read`, so the custom stream contains no flag value. Matrix exposes the seven stated setters/getters and can statically represent one bad writer plus at least two separately labeled valid controls.

Integration is nevertheless rejected because the repair leaves three bounded scaffold defects:

1. All three `CfgMods.defs.worldScriptModule.files[]` values use backslashes. The pinned official Samples and CF configs use forward slashes, and the retained DayZDiag multi-PBO result explicitly preserved forward slashes in `files[]` while requiring backslashes only in PBO prefix properties. The single-level manifest prefix here contains no slash at all, so README's “raw-backslash PBO prefix” wording is also false and generalizes the earlier prefix result to a different field.
2. `build.ps1` does not reject reparse points in the accepted `TEMP/entity-persistence-repair` path chain and creates the proposed run directory with `-Force` without first proving it did not exist. Its string containment checks therefore do not establish ownership/physical containment for Addon Builder's destructive `-clear` target. The retained three runs are ordinary non-reparse directories, but the reusable helper invariant is not repaired.
3. The public harness interface is incomplete across upgrade variants: v1 lacks `SetFixtureCaseLabel`, `GetFixtureCharges`, and `GetFixtureCaseLabel`; v2 lacks those three plus `GetFixtureLocked`. This is a code gap in the scaffold, independent of whether the separate mission/CE/save/shutdown harness has been implemented.

## Dispositions

| Finding | Decision | Reopened evidence | Minimal repair |
|---|---|---|---|
| EPF-C03 canonical output | **Accepted for the three retained runs** | Manifest names `EntityPersistenceFixture.pbo`; every build directory contains exactly one PBO with that exact name, and receipt name/hash/size match the file. No stale `v1.pbo`, `v2.pbo`, or `matrix.pbo` remains in a build directory. | None for the current artifacts. |
| EPF-C04 per-instance matrix | **Accepted for matrix; upgrade API still rejected** | `m_OmitLockedOnSave = false`, `[NonSerialized()]`, setter/getter, conditional omission of only `locked`, persisted label setter, locked setter, and four assertion getters are all present. Two or more instances can retain `false` while one is set `true`. v1/v2 API parity is absent. | Add the variant-appropriate public methods: v1 label setter plus charge/label getters; v2 the same plus locked getter. Repackage all affected variants. |
| EPF-C05 fail-fast reader | **Accepted statically** | Every variant returns immediately after parent/schema/charges/label failure; v2/matrix reject unsupported schemas before common fields and return immediately on `locked` failure. `LOAD_OK`/`LOAD_FAIL`, stage, schema, label, position, and four persistent-ID blocks are present. `GetPersistentID(out int, out int, out int, out int)` is declared in extracted `EntityAI`. | No reader repair. Compilation/load/runtime remain unproved. |
| EPF-C06 archive/member checks | **Actual archives accepted; helper rejected** | Direct PBO parsing independently found exactly two entries in every archive and payload hashes equal current source. The helper compares every observed member to the generated expected list, but does not enforce equal cardinality/uniqueness and lacks reparse/pre-existing-run protection. | Reject any reparse point from repository `TEMP` through `WorkRoot` and the generated run/clear path; require the candidate run not to exist, create it without `-Force`, then recheck ordinary-directory containment. Compare member counts and reject case-insensitive duplicates as well as missing/unexpected names. |
| EPF-C07 source ledger | **Accepted with a config correction** | Battery9V/config, EntityAI, serializer, official Samples commit/path, and CF commit/paths were reopened and their hashes match the repair ledger. CF remains correctly classified third-party. | Change all three `files[]` values to `EntityPersistenceFixture/scripts/4_World`; repackage and replace the receipts. Remove “raw-backslash” from README and describe the single-level prefix separately from the forward-slash `CfgMods.files[]` virtual path. |

The canonical filename and actual member set are therefore real archive facts, not claims inferred from the author report. Conversely, `Build Successful` under `-packonly` remains packaging evidence only: it proves neither config parsing nor Enforce compilation, module/class loading, callback execution, persistence, omitted-field behavior, restart behavior, nor record isolation.

## Matrix and API checks

- Matrix-only public API found: `SetFixtureCaseLabel`, `SetFixtureLocked`, `SetFixtureOmitLockedOnSave`, `GetFixtureCharges`, `GetFixtureCaseLabel`, `GetFixtureLocked`, and `GetFixtureOmitLockedOnSave`.
- Extracted API found: `Serializer.Write(void)` and `Serializer.Read(void)` both return `bool`; `[NonSerialized()]` is a declared serializer attribute; `EntityAI.GetPersistentID(out int, out int, out int, out int)` is declared and documented stable across restart.
- The static no-persistence conclusion for `m_OmitLockedOnSave` is limited to the delivered custom layout: it has an explicit false initializer and is never written/read by these overrides. No restart was run.
- v1 has no public harness method. v2 has only `SetFixtureLocked`. Fixed positions and IDs could aid a future harness, but they do not replace the requested persisted case-label and assertion interface for three baseline/upgrade records.

## Archive verification

The retained Addon Builder logs all say `Build Successful`, show `-packonly`, and record an original variant-named output before the helper's rename. The retained BankRev logs report `prefix = EntityPersistenceFixture\` and exactly two mounted member lines. Direct binary parsing, without launching either tool, found the extension property value `EntityPersistenceFixture`, two uncompressed entries, and payload hashes matching current files:

| Variant | Receipt SHA-256 | Canonical PBO bytes / SHA-256 | Config payload SHA-256 | Script payload SHA-256 |
|---|---|---|---|---|
| v1 | `BC6A70FECE9AFEBF9C49649FB374A11DD4B603E5707A063A81562E9385A95719` | 3362 / `B08F692885597DE0FE87DC3C82F25C49696BA93CCFDA7AAA5F42BB801DA45D79` | `D9AB275AD77AE11CB5CC32EE7F7B8A16D81157C1ED554F1A2B04C3DBE26AF241` | `CD15FEBB6559B767D9ECC50F2632DC3D9F52D44326E72C6163C590607BD28205` |
| v2 | `FC90DDE9006779640FB729646EE3BDA30949208CD43A41D2FB4B931D7155DC31` | 4145 / `A499F69E2A801226D6200941EC2965E9F778A6CFD61A716F38EF9BEA4DF5C5CA` | `04295EC0927CF0ACF0913F2071765F70D87BD8ECB93DD4A74B71E4892AFF9C00` | `4D745BE004293FDA27F094FF50BF473D1DD835969038DC0DB7B59DC9D565D85A` |
| matrix | `A1FE50E3FE9BDE6B85F321A7A043965BE652862ADFEEAAC28A1C8B4648A77C6D` | 5340 / `94950B74AD00A1B7658BA54C5B40A4A85C6101BA0FC47E48F11BA2EA34933782` | `04530A93C2C6D4E7FF5EA72C5BC1D25CCA3CF31DD0E985AFECB3BD59BBF3186E` | `A3A8FCD3387773D915A31C2CA5035C07FB8A49CE7877867D37E629E2081A090D` |

Common log hashes are BankRev properties `566CF2D405F145D6E57560A3B91F5A13147DC2460CD2BD2741FB29E45DEB22A1` and members `A4D6294CCAFF3BA4CE181CFCC86B27F49AD1F4FD891DC5C39789064194F4B934`. Addon Builder log hashes are v1 `1CC411424CE07B88C9BCA95B42F4FA3D371005BF760962603D09253F7838DC39`, v2 `5F22AE65CADF7CE3920753E26FA725FB4E44851D6CD9737AFD7CEB6444F649EB`, and matrix `D96C8F923AC12BFED57E7908F59F14F106C695D14CAC39754EBDFBCDBC50E4F9`.

## Current file and source hashes

| Path | SHA-256 |
|---|---|
| `examples/en/entity-persistence/README.md` | `8C762FC90C02B097ACCD41F83CAA672B597F811565583C63C4A2938B34F31FFF` |
| `examples/en/entity-persistence/manifest.json` | `4701E996F8A0A01EE6D28C20779E1D5C843019AC452C728DECA2A25B377D69E9` |
| `examples/en/entity-persistence/build.ps1` | `B70F3C378EEE774501424B71A683742A3349FD7CEA58259A2CE3FD86E6DC44C7` |
| v1 config / script | `D9AB275AD77AE11CB5CC32EE7F7B8A16D81157C1ED554F1A2B04C3DBE26AF241` / `CD15FEBB6559B767D9ECC50F2632DC3D9F52D44326E72C6163C590607BD28205` |
| v2 config / script | `04295EC0927CF0ACF0913F2071765F70D87BD8ECB93DD4A74B71E4892AFF9C00` / `4D745BE004293FDA27F094FF50BF473D1DD835969038DC0DB7B59DC9D565D85A` |
| matrix config / script | `04530A93C2C6D4E7FF5EA72C5BC1D25CCA3CF31DD0E985AFECB3BD59BBF3186E` / `A3A8FCD3387773D915A31C2CA5035C07FB8A49CE7877867D37E629E2081A090D` |
| `persistence-fixture-council.md` / `.json` | `43F52A66F99E2DEB9A76FBF067CFC905FB50BC042BF450A6A85FE0C91CB97FA6` / `A442D9EF2F030BEE438ED40EF5B280A787D729A809B7E4C2351F0B9FE2581805` |
| `persistence-fixture-repair.md` / `.json` | `0C45BCC10240B93E8BB86E3D7542EF17964DE70E0BFADB883CC53B5E613E5928` / `94BFF201702DA788CED99E9CB74A106C8D5333B2FCFC47B3C205DB867D5C391F` |
| `persistence-source-council.md` / `.json` | `317093AD43155012AE0EBBA136CBD730C98239210F2C3650AADA257FFAC15398` / `5BA2DDF9531365447183944ADA17E93F7195DA52850CC646147DA921F78A821F` |
| extracted Battery9V / consumables config | `98D4376AEF70324F7C9FD4DDEB5098D6E0B731EE9CDB4352A6A7166C03838A34` / `360DF711C194F9264C232C9296FD4DA5B92EBCE731FC25E0908036EA07CB745B` |
| extracted EntityAI / serializer | `AD08181C307BE03549ABC8AFD6A6CEB8532ECA88DA5DA648686CA9FD682A57F5` / `3C365E5EF418438220CD2A2012C57EF385DDCAD835D712D136D31E6DFE7D2F5D` |
| official Samples `Test_GardenPlot/config.cpp`, commit `da5e5437...` | `2C66BE131A55CFFDED96712245DD74D78E25D003C21A4F51F0B94587C666CD37` |
| CF `JM/CF/Scripts/config.cpp`, commit `0763e7e...` | `8DA49AD88AB7387B4F5E6D5D2FDBC07005F908B537E7F723152BD41B6BDD1D41` |
| CF `CF_ModStorageObject.c` / `CF_ModStorage.c` | `4B37540E26D7F708AA8B53715C7D11B2F95C7FC18A9E7ADBF5D6E244A9B6F242` / `6FCF72DDC889D751F02BE1097DBC19126F851E7712A90EC2F52FA61B4E59D7B0` |

The repair report's “Before” hashes are historical values copied from the earlier council record. They were not freshly recomputed from verified pre-edit filesystem files during this review and must not be described as current preimage verification.

## Boundary after repair

After the three minimal repairs above and fresh archive receipts, the package-only scaffold may be reconsidered for integration without waiting for the separate harness/CE/save/clean-shutdown research. Full migration completion still requires the separately reviewed compilation/load gate and controlled persistence runtime matrix; neither is claimed or evaluated here.
