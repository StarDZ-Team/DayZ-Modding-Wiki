# Persistence harness implementation receipt

**Recorded:** 2026-09-14  
**Scope:** `examples/en/entity-persistence/**` and the two permitted disposable `TEMP` roots only.  
**Result:** source, template, static, preparation, and package-only delivery; no DayZ/server/client/Workbench/wiki-build process was launched.

---

## Delivery

- Added `harness/Invoke-EntityPersistenceHarness.ps1`: separate `Static`, `Prepare`, `Package`, `Smoke`, and `Phase` actions. `Prepare`, `Package`, and `Static` cannot launch; `Smoke` and `Phase` fail closed unless the operator adds `-Launch` and supplies an explicit single reviewed PBO path.
- Added private no-mod/v1/v2/matrix `init.c` templates, the CE `types.xml` include and controlled type record, an active private five-minute `messages.xml`, and the operator guide. Preparation uses one physical private mission copy, `instanceId = 1`, `storageAutoFix = 0`, unique profile/log/run paths, a shared source-location line for strict diagnostic comparison, and roots confined to the two named disposable TEMP paths.
- Updated all fixture variants so `SAVE`, `LOAD_OK`, and `LOAD_FAIL` include phase/run ID, label, charges, and four PID blocks. Context is read from `$profile:EntityPersistenceFixture/context.txt`, not `ParamsWriteContext`, preserving the v1 `schema/charges/label` and v2/matrix `schema/charges/label/locked` record orders; v1 never calls locked/omit APIs and v2 never calls omit APIs.

## Contract controls encoded

- The controller uses the retained DayZDiag path and hidden owned process recipe; it waits for CE completion, current run module markers, and required reload callbacks before writing the exact trigger. It stops state changes at T+180, requires phase-ready by T+210, records self-exit through T+420, checks the owned port triple is released, and marks an overdue process invalid before permitted owned-PID termination.
- Phase routing implements `seed-v1`, same-v1, migration, non-default true, and two independent bad write/read branches. It creates no `baseline-v1`/`pre-bad` process, makes their post-exit storage snapshots with sorted path/size/SHA-256 manifests, rejects links/reparse points/hardlinks, and rehashes the immutable source immediately before cloning.
- The no-mod smoke source contains neither the candidate type nor `ConfigIsExisting` fixture witness. Candidate smokes have typed World resolution plus Game/World/Mission/private-init/config witnesses; diagnostics compare exactly after only recorded timestamp, PID, and profile-path-prefix normalization. Runtime outcomes, including the malformed record's native disposition, remain unobserved.

## Validation performed

1. Reopened extracted `D:/DayZ Projects` API declarations for `OnStoreSave`/`OnStoreLoad`, four-block `GetPersistentID`, `CreateObjectEx`, object enumeration, economy profile/lifetime, CE flags, `FileExist`/`OpenFile`/`FGets`, and the callback queue. Reopened the pinned official CE mission XML/init and Samples `Test_GardenPlot` config, plus pinned CF `MissionBase.c` only as a non-authoritative deferred-mission pattern; no wider research was performed.
2. `Invoke-EntityPersistenceHarness.ps1 -Action Static` passed: PowerShell AST, XML, APIs, variant restrictions, and fixture-free no-mod checks. `Prepare` passed for all four templates and produced `CreateCustomMission` at line 511 in every generated private init file, avoiding a run-variable source-stack location in baseline comparison.
3. `Package` passed for v1, v2, and matrix with Addon Builder `-packonly` plus BankRev; receipts are listed below. This is archive inspection only, not Enforce compilation or runtime evidence. `git diff --check` passed (Git printed only existing CRLF conversion warnings).

## Hashes and receipts

| Item | Before | After / receipt |
|---|---|---|
| v1 fixture | `12D071E4A45D71FBB78FA233AC7E061ECDB082A9F2A37626F3DCC8736C026B35` | `169357CCCF2E8797D7791A2AA842DAA755ACDF8527DBB59A9FE6204C1A5536D2` |
| v2 fixture | `E167090471C1C6D732366680C97663BA2AC205936E4A21CA1406B0056536EFE0` | `10386F5419115F2F81F3B039499493D872BCB5FA37A65F837FD6CD04DBDE0818` |
| matrix fixture | `A3A8FCD3387773D915A31C2CA5035C07FB8A49CE7877867D37E629E2081A090D` | `0573DFFDDEF375456E51459249C3367A8F2125FE085991AF4672E14F23A7A678` |
| controller | absent | `10CFBB244750D6A8E9193CF147FA7583023BD7001D907126A7EDDB4CAC3C68A8` |
| v1 archive | n/a | PBO `65684488B611F7A596D99C0301DF0B79C14F70D5A154F5BB2756574E26917D64`; `TEMP/entity-persistence-repair/entity-persistence-v1-20260914-024309-ffe8e11c/receipt.json` |
| v2 archive | n/a | PBO `8D778AB27F31A0D3308F84A59CC29365744E7AFFA993F6E2CBDD9D3F5BC36AF8`; `TEMP/entity-persistence-repair/entity-persistence-v2-20260914-024311-8a1f6fbf/receipt.json` |
| matrix archive | n/a | PBO `B9EDFE4C4116CA3FED3BA4FE0C9DD3A24EFE03DAFC95273D09365D560E06D449`; `TEMP/entity-persistence-repair/entity-persistence-matrix-20260914-024313-4f47e82e/receipt.json` |

The before hashes are the accepted final-interface hashes recorded in `persistence-harness-closeout.json`; the controller/template files did not exist in commit `326ab03`. Full structured source and validation data is in the adjacent JSON receipt.

## Remaining gates

An independent source review must inspect the final files and package receipts before any `-Launch`. Then the mandatory fixture-free control, three candidate smokes, and all nine persistence phases must run on the pinned executable; only fresh-process callback/readback can establish the persistence claims, and no native faulty-record framing or flush guarantee is asserted here.
