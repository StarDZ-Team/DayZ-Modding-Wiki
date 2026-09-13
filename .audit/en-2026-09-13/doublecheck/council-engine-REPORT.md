# Engine second-pass council

Status: complete independent council review; baseline `bf7ae1947876071ed4e25578dc595d896f2e6263`; no runtime test or build performed.

## Decision summary

| ID | Classification | Disposition |
|---|---|---|
| ENG-001 | Confirmed error | Accept revised exact repair |
| ENG-002 | Confirmed error | Accept exact repair |
| ENG-003 | Essential omission | Accept revised exact repair |
| ENG-004 | Unresolved uncertainty | Unresolved; accept only the conservative exact repair below |
| ENG-005 | Unresolved uncertainty | Accept revised exact repair |

The five quoted anchors exist at the stated baseline commit. Hashes below are hashes of the exact on-disk bytes, independently computed with `File.ReadAllBytes` plus SHA-256; they are not hashes of decoded or newline-normalized text. In particular, `enscript.c` is 24,588 bytes with 1,028 CRLF sequences: raw SHA-256 `1CA3897DF3F842E6EAACB5E771A4A04ECE1D77E2A7C987F0A8174351770B43D4`, while the deliberately LF-normalized UTF-8 identity is `DB32B8CBDBD2D8A962319F36DEC55D0322C6183CFE612B2ECC1E461F0E07F565`. The four raw extraction hashes in the author report match the files independently reopened under `D:/DayZ Projects`; `Object.Delete()` was also checked in `scripts/3_game/entities/object.c` (raw SHA-256 `EBAC48FF196148AB4722A9D9A81C277796D4EA07896A5CF09742213D32424B4C`). The current working-tree versions of the four affected English pages still match the baseline because the unrelated dirty files are outside this domain.

## Findings and exact author requests

### ENG-001 — confirmed error; accept revised exact repair

At `en/06-engine-api/01-entity-system.md:1555`, replace exactly:

```markdown
- **Cast with `Class.CastTo()` instead of direct casts.** `Class.CastTo(result, source)` returns false on failure without crashing, while a direct cast to a wrong type produces undefined behavior.
```

with:

```markdown
- **Use either documented safe-cast form.** `ClassName.Cast(source)` returns the cast value or `null`; `Class.CastTo(result, source)` returns `true` on success and writes the result. Choose the form that makes the surrounding null handling clearest.
```

Rationale: `D:/DayZ Projects/scripts/1_core/proto/enscript.c:80-110` explicitly documents both operations as safe down-casts and invalid `Cast` as returning null. The revision uses the reader-facing `ClassName.Cast` form rather than the author's abstract `Type.Cast`, while preserving the substance of the proposed fix.

### ENG-002 — confirmed error; accept exact repair

At `en/06-engine-api/06-notifications.md:397`, replace the complete existing bullet with:

```markdown
- **Multi-Mod:** The vanilla `NotificationSystem` is shared by all mods, so simultaneous notifications can contend for its visible stack. Do not assume a framework is independent: CommunityFramework mods the vanilla `NotificationSystem`; inspect the specific framework/version before reasoning about queue or layer isolation.
```

Rationale: pinned CommunityFramework commit `0763e7e7548c9a0bed6626afff835de80693ebf3`, `NotificationSystem.c:1-165`, declares `modded class NotificationSystem`; its creation paths ultimately call `m_Instance.AddNotif`, which operates on the inherited notification arrays. This disproves the page's universal independence claim without pretending every framework has the same design.

### ENG-003 — essential omission; accept revised exact repair

Insert the following immediately after the rule-of-thumb paragraph ending at `en/06-engine-api/13-input-system.md:258`, before `## KeyCode Reference`:

```markdown
> **UA button names and raw `KeyCode` constants are different namespaces.** UA bindings use names such as `kLMenu`, `kRMenu`, and `kBackspace`; raw-key APIs use `KeyCode.KC_LMENU`, `KeyCode.KC_RMENU`, and `KeyCode.KC_BACK`. In the inspected build's `bin/constants.xml` button table, the corresponding UA button IDs are 505, 567, and 463. Prefer the names in XML and `BindCombo()` calls, and verify numeric IDs against the installed build before storing them.
```

Rationale: `D:/DayZ Projects/bin/constants.xml:463,505,567` contains the three required `k...` entries, while `scripts/3_game/inputapi/uainput.c:33-34` documents name/hash combo binding. Bohemia's pinned `Test_Inputs/scripts/gameModule/MyGameImplement.c` uses `BindCombo("kLControl")` and `BindCombo("kP")`. Moving the note to the UA/raw transition gives it an exact, relevant insertion point; the original anchor was merely a row inside the raw-key table. This is static evidence only, not a combo runtime test.

### ENG-004 — unresolved uncertainty; conservative repair only

At `en/06-engine-api/10-central-economy.md`, delete this complete code line at baseline line 341:

```c
string custom = ce.GetCEGlobalString("MyCustomVar");     // returns "" if not found
```

Then replace the complete paragraph at baseline line 344 with:

```markdown
`CEApi` exposes typed getters for entries loaded from `globals.xml`. The inspected declarations and official CE documentation do not establish whether arbitrary custom `<var>` names are supported in every build, so treat custom globals as version-specific until tested on the target server. Use a mod-owned config file when portability matters. The full parameter reference for the documented variables is in [Loot Economy Deep Dive](../09-server-admin/04-loot-economy.md#globalsxml----economy-parameters).
```

Rationale: `centraleconomy.c:578-598` proves typed lookup by name and sentinel returns, but not acceptance or persistence of arbitrary user-defined names. Bohemia's current CE configuration page and pinned Central Economy repository enumerate known variables and do not document a custom-variable extension contract. Removing only the paragraph, as originally proposed, would leave the `MyCustomVar` example asserting the same unproved behavior. The underlying feature remains unresolved, not disproved.

### ENG-005 — unresolved uncertainty; accept revised exact repair

Three exact changes are required in `en/06-engine-api/01-entity-system.md` so the section does not contradict itself.

Replace baseline line 1444:

```markdown
Immediate server-authoritative deletion. Removes the object from the server and replicates the removal to all clients.
```

with:

```markdown
Invokes the native `ObjectDelete()` operation for the object. For synchronized gameplay objects, call it from authoritative server code; the inspected script declaration does not document replication timing or an all-clients guarantee.
```

Replace the example comment at baseline line 1460:

```c
// Immediate: when you need it gone right now
```

with:

```c
// Direct native deletion call from authoritative code
```

Replace the complete best-practice bullet at baseline line 1554:

```markdown
- **Prefer `obj.Delete()` (deferred) over `GetGame().ObjectDelete()` (immediate).** Immediate deletion during iteration or event processing can cause null pointer crashes. Deferred deletion is safe in all contexts.
```

with:

```markdown
- **Use `obj.Delete()` when deletion can wait until the next frame.** Its script implementation queues `GetGame().ObjectDelete()` on `CALL_CATEGORY_SYSTEM`, which avoids deleting the object in the current call stack. Use the native call directly only when that deferral is unsuitable and you have accounted for current references and iteration.
```

Rationale: `game.c:704-706` declares `ObjectDelete`, `ObjectDeleteOnClient`, and `RemoteObjectDelete` but supplies no replication/timing guarantee for `ObjectDelete`. `object.c:74-85` does prove that `Object.Delete()` queues the native call for the next frame. The author's single-line repair was insufficient because the example and best-practice bullet continued to assert immediate behavior and absolute safety; the revised wording stays within the available proof.

## Current official web verification

- BohemiaInteractive `DayZ-Samples` pinned `Test_Inputs` URL returned HTTP 200 on 2026-09-13: <https://github.com/BohemiaInteractive/DayZ-Samples/tree/da5e5437c9502620d9853fb6eed14701135ab2ea/Test_Inputs>.
- BohemiaInteractive `DayZ-Central-Economy` pinned repository URL returned HTTP 200 on 2026-09-13: <https://github.com/BohemiaInteractive/DayZ-Central-Economy/tree/9a21bb9f5fb9c62a7ce2761402196091588133e6>.
- The current official CE configuration page remains indexed and readable through web search, but direct automated HEAD access returned HTTP 403 on 2026-09-13: <https://community.bistudio.com/wiki/DayZ:Central_Economy_Configuration>. That access restriction is not evidence for or against custom globals.
- The pinned CommunityFramework source URL returned HTTP 200 on 2026-09-13: <https://github.com/Arkensor/DayZ-CommunityFramework/blob/0763e7e7548c9a0bed6626afff835de80693ebf3/JM/CF/Scripts/3_Game/CommunityFramework/Notification/NotificationSystem.c>.

## Explicit blockers and limits

- No official prose, public native implementation, or executed target-server test was found that establishes arbitrary custom CE globals across builds. ENG-004 must remain uncertainty even after its misleading example is removed.
- No public native implementation or executed client/server trace was found for `ObjectDelete()` replication scope or timing. ENG-005 removes the guarantee; it does not replace it with a new one.
- The extraction is snapshot/static evidence and does not identify a game build manifest. Numeric UA IDs must remain build-qualified.
- No game, server, build, callback harness, RPC test, or modifier-combo runtime test was run. Mod usage is corroboration only.

Only the exact changes approved above are council-approved for the later Terra application pass. Final council verification must compare the applied bytes and new SHA-256 hashes against these anchors and confirm no other English lines changed.
