# English language audit — independent council

Date: 2026-09-13
Requested and checked baseline: `bf7ae1947876071ed4e25578dc595d896f2e6263`
Council scope: language report claims only; no documentation edits, build, runtime test, worktree, commit, translation, config, graph, agent, or specification changes.

## Verdict

The baseline commit exists and is the current checked-out commit. I reopened every one of the 16 candidate locations and the relevant surrounding examples. Twelve findings warrant repair, three warrant narrower repairs than the author proposed, and one (zero-vector normalization) remains unresolved. The prior report's continuation renumbered findings after `LANG-DC-003`; this council preserves the original IDs from `language.json.findings` so an editor cannot apply a repair to the wrong location.

The continuation's local SHA-256 values for `enscript.c`, `humaninventory.c`, and `entityai.c` are not reproducible from the named snapshot. The current snapshot hashes are respectively `1CA3897DF3F842E6EAACB5E771A4A04ECE1D77E2A7C987F0A8174351770B43D4`, `5895C6B599776D57843EFA2C668DA1C0DADF0B434A9FB38EDE0E2239C9112DD7`, and `AD08181C307BE03549ABC8AFD6A6CEB8532ECA88DA5DA648686CA9FD682A57F5`; therefore the prior hashes must not be copied into an applied-change receipt.

The stale continuation-ID mapping is: continuation 004 → original 005 (constants), continuation 005 → original 004 (`EEHitBy`), continuation 006 → original 006, 007 → 007, 008 → original 009 (casting), 009 → original 010 (logger), 010 → original 011 (inventory), 011 → original 012 (RPC), 012 → original 014 (defaults), 013 → original 013 (multiline calls), 014 → original 015 (spawn helper), and 015 → original 016 (`GetTransform`). Original 008 (zero normalization) disappeared from the promoted list and remains unresolved. Page, line, and quoted old text—not the stale continuation ID—are authoritative for application.

Internet verification was performed on 2026-09-13. The current official `BohemiaInteractive/DayZ-Script-Diff` `main` tip is `86974a0f5bd16b1ee3e334ad828133c93dca80a1`, and the live raw files agree with the relevant local declarations. The official BIKI page is currently reachable at <https://community.bistudio.com/wiki/DayZ:Enforce_Script_Syntax>; the historical revision used for stable wording is <https://community.bistudio.com/wiki?title=DayZ:Enforce_Script_Syntax&oldid=376851>. Community Framework is framework evidence, not vanilla evidence; its `production` tip observed today is `0763e7e7548c9a0bed6626afff835de80693ebf3`, and its RPC manager is <https://github.com/Arkensor/DayZ-CommunityFramework/blob/production/JM/CF/Scripts/3_Game/CommunityFramework/RPC/RPCManager.c>.

## Candidate dispositions and requested exact repairs

### LANG-DC-001 — accept revised exact repair (confirmed error)

At `en/01-enforce-script/01-variables-types.md:486`, replace exactly:

```text
// int to float (always safe, no data loss)
```

with:

```text
// int to float (large integer values can lose precision)
```

The official type table identifies the 32-bit integer range and the float range characteristic of binary32; “always” and “no data loss” are false. The example value 42 remains exact.

### LANG-DC-002 — accept revised exact repair (confirmed unsupported behavior claim)

At `en/01-enforce-script/02-arrays-maps-sets.md:950-958`, replace the complete paragraph and code block body with:

`Set` is the documented create-or-update operation. Use it when the key may already exist; the public `Insert` declaration only documents insertion of a new element, so do not rely on an undocumented duplicate-key result.

```c
map<string, int> data = new map<string, int>;
data.Insert("key", 100);  // Insert a new key
data.Set("key", 200);     // Create or update; value is now 200
```

`enscript.c:879-907` documents `Set` as create-or-update but gives no duplicate-key contract for `Insert`. Mod usage cannot establish native behavior.

### LANG-DC-003 — accept revised exact repair (essential omission)

At `en/01-enforce-script/02-arrays-maps-sets.md:560`, replace the comment with:

```text
// Access by internal index (O(n)); do not rely on a particular iteration order
```

Also delete the exact expected-order comments at lines 582 and 586 (`// keys: ...` and `// values: ...`). `enscript.c:860-878,910-925` specifies internal positional access and O(n), but no insertion-order guarantee.

### LANG-DC-004 — accept revised exact repair (confirmed error)

This is the original `EEHitBy` candidate at `en/01-enforce-script/04-modded-classes.md:464-470`. Replace that entire method with:

```c
// Veto calculated damage while god mode is enabled
override bool EEOnDamageCalculated(TotalDamageResult damageResult, int damageType, EntityAI source, int component, string dmgZone, string ammo, vector modelPos, float speedCoef)
{
    if (m_LNT_GodMode)
        return false;

    return super.EEOnDamageCalculated(damageResult, damageType, source, component, dmgZone, ammo, modelPos, speedCoef);
}
```

Then replace the fall-damage example at lines 897-910 with the same callback shape, returning `false` for `DT_FALL` and otherwise returning `super.EEOnDamageCalculated(...)`. Finally change exercise item 3 at line 1189 from `EEHitBy` to `EEOnDamageCalculated`. Official snapshot `object.c:1136-1143` says `EEOnDamageCalculated` runs immediately before application and its Boolean decides whether damage applies; `EEHitBy` is notification, so skipping `super.EEHitBy` does not veto engine damage.

### LANG-DC-005 — accept revised exact repair (confirmed error)

At `en/01-enforce-script/04-modded-classes.md:294`, replace the paragraph with:

```text
A `modded class` can redefine an inherited or existing constant; the last loaded mod wins, so the result depends on mod load order. Prefer overriding a method when you need behavior that other mods can chain with `super`.
```

At line 1213 replace the table cell text `Can be added; to change a vanilla value, override the method that uses it` with `Can be added or redefined; the last loaded mod wins, so redefinition is load-order-dependent`. The official BIKI “Modded constants” section explicitly demonstrates overriding base and local constants.

### LANG-DC-006 — accept exact repair (confirmed error)

At `en/01-enforce-script/05-control-flow.md:59`, replace exactly:

```c
if (player.GetHealth("", "Blood") < 3000 || player.GetHealth("", "Health") < 25)
```

with:

```c
if (player && (player.GetHealth("", "Blood") < 3000 || player.GetHealth("", "Health") < 25))
```

The function parameter may be null; the first independent `if` does not terminate the function. This is proven by the local control flow and the documented logical operators.

### LANG-DC-007 — accept revised exact repair (essential omission)

At `en/01-enforce-script/06-strings.md:34`, replace the sentence with:

```text
Returns the base string length. For the number of characters in UTF-8 text, use `LengthUtf8()`.
```

Do not claim that `Length()` “counts bytes”: the official declaration documents only “length of string,” while `enstring.c:201-212` expressly documents `LengthUtf8()` as the number of UTF-8 characters. The distinction is essential, but byte semantics were not proved.

### LANG-DC-008 — unresolved uncertainty

At `en/01-enforce-script/07-math-vectors.md:664,700`, the claim that zero normalization produces NaN is not established by a script declaration, official documentation, or an executed runtime test. Do not preserve that outcome claim as fact. If the editor needs a conservative documentation-only repair, replace line 664 with `Check v.Length() > 0 before Normalize() when your calculation requires a nonzero direction` and replace the line-700 effect with `No usable direction`; this remains a defensive recommendation, not proof of native zero-vector behavior.

### LANG-DC-009 — accept exact repair (confirmed error)

At `en/01-enforce-script/09-casting-reflection.md:50`, replace the paragraph with:

```text
Calling a method that is not declared on the variable's static type is a compile error. Cast to the appropriate derived type and check the result before calling derived-only methods.
```

Official syntax documents strong/static typing, class inheritance, virtual methods, and compiler signature checking. Runtime virtual dispatch does not bypass compile-time member lookup.

### LANG-DC-010 — accept revised exact repair (confirmed error)

In `en/01-enforce-script/11-error-handling.md:463-476`, replace the early return and unconditional print with:

```c
if (level < s_ConsoleMinLevel && level < s_FileMinLevel)
    return;

string levelName = typename.EnumToString(LNT_LogLevel, level);
string line = string.Format("[Lantern] [%1] [%2] %3", levelName, source, message);

if (level >= s_ConsoleMinLevel)
    Print(line);

if (level >= s_FileMinLevel)
    WriteToFile(line);
```

The old early return makes the file threshold subordinate to the console threshold, contradicting the example's two independent settings.

### LANG-DC-011 — accept revised exact repair (confirmed error plus authority omission)

At `en/01-enforce-script/11-error-handling.md:673-676`, replace the unused reservation lookup with:

```c
// This operation is server-authoritative, and the source must own the item
if (!GetGame().IsServer() || item.GetHierarchyRootPlayer() != fromPlayer)
    return false;
```

`humaninventory.c:46-53` shows that `FindUserReservedLocationIndex` returns a reservation index, not an attachment slot; the old `checkItem` is never checked. `entityai.c:874-881` documents `GetHierarchyRootPlayer`. This repair covers hierarchy ownership and the use of `InventoryMode.SERVER`; it does not add permissions, locking, or transactional guarantees that the example never claimed.

### LANG-DC-012 — accept revised exact repair (essential omission; framework-dependent)

At `en/01-enforce-script/11-error-handling.md:601`, replace the heading with `### Framework-Dependent RPC Handler Skeleton`. Immediately before the code block insert:

```text
This callback signature and `CallType` come from Community Framework's RPC manager, not vanilla DayZ. Register the handler through that framework and declare the dependency. The skeleton is not safe to expose to untrusted clients until you provide a server-owned permission implementation, an explicit spawn-class allowlist, finite and server-bounded position validation, and per-sender rate limiting.
```

At line 642 replace `// All guards passed — execute` with `// Execute only after the allowlist, position bounds, and rate limit described above pass`. Rename the section; do not label the present code “safe.” CF source defines `CallType` and constructs the four callback arguments. The current code trusts arbitrary class and position input and references an undefined permission function. A complete runnable “safe” replacement is blocked on policy choices (allowed classes, region, distance, and rate); the editor must not invent them.

### LANG-DC-013 — accept exact repair (confirmed error)

At `en/01-enforce-script/12-gotchas.md:360-378`, replace the entire subsection with:

### Multiline Function Calls Are Supported

Function calls may span lines. Keep delimiters and argument expressions balanced; line breaks alone do not cause a compile error.

```c
string msg = string.Format(
    "Player %1 at %2",
    name,
    pos
);
```

Shipped extraction has executable multiline calls, for example `scripts/3_game/particles/tests/pmtf.c:27-29` (SHA-256 `0ACC6E8734BCF1C9DF448F17746912307E6DCBBFBFA9CD9A260629CD4B73C8A2`).

### LANG-DC-014 — accept revised exact repair (confirmed error)

At `en/01-enforce-script/12-gotchas.md:182`, replace the first sentence with `Default parameter values may use literals, NULL, and supported compile-time constants such as enum members; runtime function calls are not valid defaults.` Preserve the vector example and wrapper advice. Make the same terminology correction at `en/01-enforce-script/13-functions-methods.md:1062,1135,1185`; otherwise the chapter remains internally contradictory. Shipped `tools.c:115-123` uses enum members as defaults.

### LANG-DC-015 — accept exact repair (confirmed error)

At `en/01-enforce-script/13-functions-methods.md:397-403`, replace the function body with:

```c
void SpawnItem(string className, vector pos, float quantity = -1, bool withAttachments = true)
{
    // quantity defaults to -1 (full), withAttachments defaults to true
    ItemBase item = ItemBase.Cast(GetGame().CreateObject(className, pos, false, false, withAttachments));
    if (item && quantity >= 0)
        item.SetQuantity(quantity);
}
```

`SetQuantity` is declared on `ItemBase` (`itembase.c:3337-3346`), not on the example's `EntityAI`; the old code also ignored `withAttachments` by hard-coding `true`.

### LANG-DC-016 — accept revised exact repair (confirmed error)

At `en/01-enforce-script/13-functions-methods.md:859-862`, delete the `GetTransform` item. At lines 871-882 replace the example and lead-in with:

Event signatures are engine-defined and must be verified on the exact parent class and build feature set before overriding them. For example, `PawnMove.GetTransform` exists only when both `FEATURE_NETWORK_RECONCILIATION` and `DIAG_DEVELOPER` expose the relevant classes:

```c
#ifdef FEATURE_NETWORK_RECONCILIATION
#ifdef DIAG_DEVELOPER
class MyMove extends PawnMove
{
    override event void GetTransform(inout vector transform[4])
    {
        super.GetTransform(transform);
    }
}
#endif
#endif
```

`pawn.c` is wholly gated by `FEATURE_NETWORK_RECONCILIATION`, and `GetTransform` is additionally gated by `DIAG_DEVELOPER`; `Transport` only extends `Pawn` under the first flag. The prior unguarded `MyVehicle extends Transport` override is not portable.

## Inherited leads

- `typename.Spawn()` constructor restriction — **unresolved**. The pages' parameterless-only claim was not proved by a current official declaration or compiler test. Do not change it on mod examples alone.
- Missing `override` semantics — **unresolved and potentially serious**. Official BIKI says class methods are virtual and `override` makes the compiler check the parent signature; it does not prove the wiki's claim that omitting the keyword creates a distinct method selected by static reference type. Request a minimal compiler/runtime fixture before editing repeated claims at 1.3 and 1.13.
- `autoptr` equivalence — **unresolved**. Official wording distinguishes `autoptr` automatic destruction from ordinary strong-reference release, while the wiki calls them identical. Request an alias-survival runtime fixture; do not infer equivalence from usage frequency.
- Static lifetime across mission reload — **unresolved**. No executed mission-restart test establishes all stated restart cases. Preserve the explicit uncertainty until dedicated/listen/client lifecycle tests exist.
- “There is no `Object.IsDeleted()`” — **unresolved**. Absence from an incomplete extracted surface cannot prove nonexistence. Rephrase as “not found in the pinned public script declarations” unless engine documentation is obtained.
- “There is no `const` for reference types” — **confirmed error, accept revised repair**. Replace `en/01-enforce-script/10-enums-preprocessor.md:275` with `Reference variables can be declared const (vanilla uses const ref combinations); verify the exact rebinding/mutation semantics before relying on const for immutability.` Vanilla itself uses `protected static const ref TStringArray` in `3_game/objectspawner.c`.
- `SERVER` / listen-server truth tables and dual mission lifecycle — **unresolved**. Static declarations and mod practice do not substitute for the requested dedicated/listen/client runtime matrix. No council approval for those categorical claims.
- Global-scope `Print` load-order advice — **unresolved**. No precise candidate location or primary proof was supplied; no repair is approved.
- Raw RPC constants 1, 2, and 3 — **confirmed collision risk, accept revised repair**. At `en/02-mod-structure/01-five-layers.md:209-211`, replace the values with a clearly namespaced high range already reserved for the example (for example `1234501`, `1234502`, `1234503`) and add `Choose IDs that do not overlap vanilla or another mod.` Vanilla `3_game/constants.c:259-261` already assigns raw IDs 1-3.

## Blockers and verification limits

- No Enforce compiler, game runtime, listen server, dedicated server, client, mission restart, RPC exploit, or inventory transaction test was run.
- Zero-vector normalization, omitted-`override` dispatch, `autoptr` alias lifetime, static lifetime, listen-server truth tables, and `typename.Spawn()` constructor rules require runtime/compiler evidence before categorical documentation.
- A fully runnable secure spawn RPC requires product policy (allowlist, bounds, permission source, and rate). The council approves only relabeling and explicit prerequisites until those choices are supplied.
- The official public script repository is a diff/declaration source, not the full native implementation. Undocumented native outcomes remain undocumented.

## Apply gate

Terra may apply only the exact accepted repairs above. For LANG-DC-008 and every inherited item marked unresolved, it must either use the explicitly conservative rewording or leave the text unchanged; it must not promote an untested outcome to fact. After application, council verification must compare the final diff to this list and record SHA-256 hashes for every changed English page.
