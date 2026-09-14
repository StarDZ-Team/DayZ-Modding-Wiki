# Entity-persistence fixture repair 2

**Date:** 2026-09-14  
**Scope:** the three bounded repairs requested by `persistence-fixture-repair-council.md/json`. Earlier repair, research, and council records are unchanged.

---

## Result

All three variants now declare `EntityPersistenceFixture/scripts/4_World` in `CfgMods.defs.worldScriptModule.files[]`. This follows the reopened pinned DayZ Samples `Test_GardenPlot/config.cpp` at commit `da5e5437c9502620d9853fb6eed14701135ab2ea` (SHA-256 `2C66BE131A55CFFDED96712245DD74D78E25D003C21A4F51F0B94587C666CD37`) and Community Framework `JM/CF/Scripts/config.cpp` at commit `0763e7e7548c9a0bed6626afff835de80693ebf3` (SHA-256 `8DA49AD88AB7387B4F5E6D5D2FDBC07005F908B537E7F723152BD41B6BDD1D41`); both use forward-slash script-module paths.

The README now separates the single-level manifest prefix `EntityPersistenceFixture` from that virtual script path. It makes no universal claim about backslashes outside this source-backed recipe.

`build.ps1` now rejects reparse points from the repository `TEMP` directory through the approved work root and generated run / Addon Builder `-clear` directory, creates every missing approved path component without `-Force`, and refuses a pre-existing generated run directory. It verifies ordinary-directory containment immediately before the destructive `-clear` invocation, and BankRev member checking now rejects case-insensitive duplicates and unequal cardinality before testing the complete expected/actual name sets.

The v1 public interface now has `SetFixtureCaseLabel(string)`, `GetFixtureCharges()`, and `GetFixtureCaseLabel()`; v2 has those methods plus `GetFixtureLocked()`. Their bodies and diagnostics match the existing matrix methods, and no persisted field order, schema number, or value changed; in particular, v1 still has no locked field.

---

## Checks performed

- PowerShell parser: `build.ps1` parsed with zero errors.
- Negative safety check: invoking the helper with repository root as `WorkRoot` failed with `WorkRoot must not be the repository root or an ancestor of it.` before packaging.
- Static helper checks added for the generated-run-exists, each reparse-point, and case-insensitive duplicate-member paths. No reparse point was created for testing and no directory was recursively deleted.
- Package-only rebuild and BankRev reinspection: all three commands completed successfully using installed DayZ Experimental Tools (`AddonBuilder.exe` 1.0.240.639; `BankRev.exe` 1.0.0.2), each with `-packonly`.
- Each fresh run contains exactly one canonical `EntityPersistenceFixture.pbo`; BankRev accepted its prefix and its two member names. The listing case differs from source casing, so comparisons are deliberately case-insensitive.

Compilation and game/server/client/runtime persistence remain explicitly pending. Addon Builder `-packonly` and BankRev verify archive packaging and listing only; they do not prove config parsing, Enforce compilation, module/class loading, callback execution, persistence, or restart behavior.

---

## Before and final file hashes

| File | Before SHA-256 | Final SHA-256 |
|---|---|---|
| `README.md` | `8C762FC90C02B097ACCD41F83CAA672B597F811565583C63C4A2938B34F31FFF` | `9C05BDEFF9926082671FB595CE9B571DFC1D0BDE2CCB67088FD321092F46F380` |
| `build.ps1` | `B70F3C378EEE774501424B71A683742A3349FD7CEA58259A2CE3FD86E6DC44C7` | `A71E0B8DA79C31BC8A4FDEB966B21A67686131E62DB808BDB95D1365417BE9D4` |
| `variants/v1/config.cpp` | `D9AB275AD77AE11CB5CC32EE7F7B8A16D81157C1ED554F1A2B04C3DBE26AF241` | `3C86A27699C7766F1C3EAA75DC9DF053520216216E7D090AFC5483C4CA51D82D` |
| `variants/v1/scripts/4_World/EntityPersistenceFixture/EntityPersistenceFixtureBattery.c` | `CD15FEBB6559B767D9ECC50F2632DC3D9F52D44326E72C6163C590607BD28205` | `12D071E4A45D71FBB78FA233AC7E061ECDB082A9F2A37626F3DCC8736C026B35` |
| `variants/v2/config.cpp` | `04295EC0927CF0ACF0913F2071765F70D87BD8ECB93DD4A74B71E4892AFF9C00` | `7B817238ABB2E8A0FD0F288C9C7E1B09910B327EAFF5F263FDEB17F2770E0147` |
| `variants/v2/scripts/4_World/EntityPersistenceFixture/EntityPersistenceFixtureBattery.c` | `4D745BE004293FDA27F094FF50BF473D1DD835969038DC0DB7B59DC9D565D85A` | `E167090471C1C6D732366680C97663BA2AC205936E4A21CA1406B0056536EFE0` |
| `variants/matrix/config.cpp` | `04530A93C2C6D4E7FF5EA72C5BC1D25CCA3CF31DD0E985AFECB3BD59BBF3186E` | `CA804F143033932C942ED18A185B0EAA9E44F127E8DCA100245413118B951D7C` |
| `variants/matrix/scripts/4_World/EntityPersistenceFixture/EntityPersistenceFixtureBattery.c` | `A3A8FCD3387773D915A31C2CA5035C07FB8A49CE7877867D37E629E2081A090D` | `A3A8FCD3387773D915A31C2CA5035C07FB8A49CE7877867D37E629E2081A090D` |
| `manifest.json` | `4701E996F8A0A01EE6D28C20779E1D5C843019AC452C728DECA2A25B377D69E9` | `4701E996F8A0A01EE6D28C20779E1D5C843019AC452C728DECA2A25B377D69E9` |

---

## Fresh archive receipts

| Variant | Run receipt SHA-256 | PBO bytes / SHA-256 | Config source SHA-256 | Script source SHA-256 | Addon Builder log SHA-256 |
|---|---|---|---|---|---|
| v1 | `83E17EC1EE874B2001AB84E67CE6C6BC1F11B2A8EA1D2E27BC6E4DEA31454D63` | `3682` / `EF6A8861099403779B1BB9583A0FC4339568ECEB73466C51824F2CA051DD4EDC` | `3C86A27699C7766F1C3EAA75DC9DF053520216216E7D090AFC5483C4CA51D82D` | `12D071E4A45D71FBB78FA233AC7E061ECDB082A9F2A37626F3DCC8736C026B35` | `340B4659289E7729223C609279070AE0F987A94F5520A1877750EB9173D84DE7` |
| v2 | `0DD7826C929F2F1668E700B2436C254227782457BDBC660844C39742981A96E7` | `4531` / `9A9F2924D14479C7939BDF6868D73882DA4D5629F77F4D980E842E03A7A473C7` | `7B817238ABB2E8A0FD0F288C9C7E1B09910B327EAFF5F263FDEB17F2770E0147` | `E167090471C1C6D732366680C97663BA2AC205936E4A21CA1406B0056536EFE0` | `0C5B4840014C0FC86441478EF478F9FA1AA124D2E6E4914D6337BBF0CC8C7EDD` |
| matrix | `05C7CA696F042F4B5407D4BDB00B1CCAA884972B7FEC1ABDFA73C2FFE6E90696` | `5340` / `B666AFD5BB75E737231CE9698644260323DBAF9C1F80A61EF28E7C8DEE706B5D` | `CA804F143033932C942ED18A185B0EAA9E44F127E8DCA100245413118B951D7C` | `A3A8FCD3387773D915A31C2CA5035C07FB8A49CE7877867D37E629E2081A090D` | `4C13B704810BE0443612C278DB7F0EFDF3FFE0C62445A75BCD6BE443C7114CCF` |

Each BankRev properties log has SHA-256 `566CF2D405F145D6E57560A3B91F5A13147DC2460CD2BD2741FB29E45DEB22A1`; each member log has SHA-256 `A4D6294CCAFF3BA4CE181CFCC86B27F49AD1F4FD891DC5C39789064194F4B934`. For every variant, the normalized BankRev member set is exactly `EntityPersistenceFixture\\config.cpp` and `EntityPersistenceFixture\\scripts\\4_world\\entitypersistencefixture\\entitypersistencefixturebattery.c`; its expected source-member names retain source casing and are compared case-insensitively.

The receipts are under the explicitly disposable `TEMP/entity-persistence-repair/` tree:

- `entity-persistence-v1-20260914-020656-a358fdf1/receipt.json`
- `entity-persistence-v2-20260914-020710-40a9d059/receipt.json`
- `entity-persistence-matrix-20260914-020723-616abcf1/receipt.json`
