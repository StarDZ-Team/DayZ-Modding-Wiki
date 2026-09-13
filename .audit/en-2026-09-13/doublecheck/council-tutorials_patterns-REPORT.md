# Council review — tutorials_patterns

Baseline and current HEAD: `bf7ae1947876071ed4e25578dc595d896f2e6263`. I independently reopened all 20 candidate locations, the surrounding examples, and the cited extraction files. No runtime, network, UI, CE, packing, or compilation test was run. English pages were not edited.

The Bohemia Community Wiki URLs were re-requested on 2026-09-13. They remain the current official URLs, but returned HTTP 403 to this worker, so I do not treat the earlier report's page summaries as independently retrieved content. Acceptances below therefore rely on reproducible pinned/local primary evidence or on narrowly scoped corrections that remove an unsupported absolute claim; web-only semantics remain qualified.

## Evidence anchors

- Audited commit: `bf7ae1947876071ed4e25578dc595d896f2e6263`; all page SHA-256 values match `tutorials_patterns.json`.
- `D:/DayZ Projects/scripts/4_world/plugins/pluginbase.c`, SHA-256 `D48AEE5C96277E87EA9FBB779FD9286DAFE7582365EFFE7BFC89BF4EA1863F7E`, lines 6-8 and 134-150: native plugin callbacks are `OnInit`, `OnUpdate`, and `OnDestroy`.
- `D:/DayZ Projects/scripts/3_game/tools/jsonfileloader.c`, SHA-256 `2D96C61DFABD99967683D0856EE5E2B1C7D06C18166B7F245BBA4DA1617BFFF4`, lines 42-61: `SaveFile` opens the supplied path and does not create its parent. Vanilla callers create directories separately.
- `D:/DayZ Projects/scripts/3_game/global/game.c`, SHA-256 `CF529055C48596108034CE6B11826B09BBF5D93E6C550E37785947873D8C3158`, lines 702 and 913: `CreateObjectEx` returns `Object`; `GetTickTime` is a native float timer.
- `D:/DayZ Projects/scripts/3_game/systems/tftests/enprofilertests.c`: vanilla profiler tests repeatedly measure intervals with `g_Game.GetTickTime()` (including lines 709-791). This defeats TP2-010's claimed reason for replacement.
- `D:/DayZ Projects/scripts/3_game/systems/tftests/scriptinvokertests.c`, SHA-256 `6219E68D6B8AB156B04FEE44BBB3B404C795E94A6FF28CF3CCD6572AD00E5D6C`: ScriptInvoker has a test corpus, but it does not prove the tutorial's unconditional non-Managed crash sentence.
- Extracted `DZ/weapons/**/config.cpp` contains actual `CfgWeapons` roots (for example `weapons/firearms/pm73rak/config.cpp:23`) and `CfgMagazines`; the extraction is snapshot evidence, not a current-runtime guarantee.
- `D:/DayZ Projects/bin/constants.xml`, SHA-256 `A2757261E565F84B04B19EB8FF6CE25D7DB60C047F09F4D2A92CB96576746BCE`, lines 463/505/567: `kBackspace`, `kLMenu`, and `kRMenu` are distinct constants.
- Current official URLs checked: `https://community.bohemia.net/wiki/DayZ:Modding_Structure`, `DayZ:Server_Configuration`, `DayZ:Diag_Menu`, `DayZ:Central_Economy_Configuration`, `Texture_Map_Types`, and `DayZ:Modding_Basics` (HTTP 403 in this environment).

## Decisions and exact repair requirements

### TP2-001 — confirmed error; accept revised exact repair

At `en/07-patterns/01-singletons.md:195`, replace:

`        s_Instance = null;  // Drops the ref, destructor runs`

with:

`        s_Instance = null;  // Releases this strong reference; destruction waits until no strong references remain.`

The old comment promises immediate destruction although another `ref` owner can remain. This is a comment-only ownership correction and does not claim a precise destructor schedule.

### TP2-002 — confirmed error; accept revised exact repair

At `en/07-patterns/01-singletons.md:600`, replace the entire bullet with:

`- Enforce Script has no built-in dependency-injection container, but you can still pass dependencies explicitly through constructors or initialization methods. Singletons are one option, not a language requirement.`

The page itself demonstrates constructors and initialization arguments; “no dependency injection” and “standard approach” are unjustified absolutes.

### TP2-003 — confirmed error; accept exact repair

At `en/07-patterns/02-module-systems.md:507`, replace the sentence with:

`The following mission lifecycle is the contract of the custom managers in this chapter. Vanilla PluginBase supplies OnInit(), OnUpdate(), and OnDestroy(); mission-start and mission-finish forwarding requires your own integration.`

This matches `pluginbase.c:6-8,134-150` and prevents readers from assuming vanilla dispatches the custom callbacks.

### TP2-004 — essential omission; accept revised exact repair

In `LNT_AutoConfigPlugin.SaveConfig()` at `en/07-patterns/02-module-systems.md:194`, insert immediately before `string path = GetConfigPath();`:

```c
        if (!FileExist("$profile:LanternAdmin"))
            MakeDirectory("$profile:LanternAdmin");
```

`JsonFileLoader.SaveFile` does not create a missing parent. This is sufficient for the one-level example; a production example should also report directory-creation failure.

### TP2-005 — confirmed error; accept revised exact repair

At `en/07-patterns/03-rpc-patterns.md:729`, replace the pros/cons paragraph with:

`**Pros:** namespaced route keys reduce collisions inside this router; \`CreateRPC()\` removes header-writing boilerplate; handlers are easy to enumerate and clean up (\`s_Handlers\`). **Cons:** \`LNT_RPC_ENGINE_ID\` is still a global integer RPC ID that must not collide with other mods, route keys must remain unique, dispatch reads two extra strings, and independent mods do not automatically discover this registry.`

Also change the String-Routed “Collision risk” cell in the immediately following table from `None (namespaced)` to `Reduced inside the router; engine ID still global`. The implementation visibly reserves integer `1000042`; “zero”/“None” is false.

### TP2-006 — confirmed error; accept exact repair

At `en/07-patterns/03-rpc-patterns.md:851`, replace the row with:

`| RPCs should be idempotent | Design retries explicitly: use request IDs and duplicate suppression for mutations such as spawning; permission checks alone do not prevent repeated authorized execution. |`

Authorization and duplicate suppression solve different problems.

### TP2-007 — essential omission; accept revised exact repair

At `en/07-patterns/05-permissions.md:98`, replace:

```c
    if (!m_Permissions.Find(plainId, perms))
```

with:

```c
    if (!m_Permissions.Find(plainId, perms) || !perms)
```

This preserves the chapter's fail-closed promise for a present key whose decoded array is null. Malformed-JSON behavior itself was not runtime-tested.

### TP2-008 — unresolved native lifetime semantics; accept cautious exact repair

At `en/07-patterns/06-events.md:476`, replace item 2 with:

`2. **For other subscriber types:** remove the subscription before subscriber teardown. The extracted declarations/tests do not establish that every stale callback produces the same failure mode, so do not rely on an automatic cleanup guarantee.`

The categorical “dangling pointer … Crash” is not supported by the cited test corpus. The replacement intentionally preserves uncertainty.

### TP2-009 — confirmed error; accept revised coordinated repair

In `en/07-patterns/07-performance.md:356-379`, change the heading `CfgVehicles Scan Cache` to `CfgWeapons Scan Cache`, change the prose's `CfgVehicles` to `CfgWeapons`, and replace all three string literals `"CfgVehicles"` in the shown `WeaponRegistry` block with `"CfgWeapons"`. The extracted firearm configs use `CfgWeapons`; changing only the first count call would leave mismatched paths and is not acceptable.

### TP2-010 — reject

Do not replace `GetGame().GetTickTime()` with `DiagTickTime()`. Vanilla `enprofilertests.c` uses `g_Game.GetTickTime()` for elapsed measurements, including tight test loops. The candidate supplied no primary declaration or resolution evidence for `DiagTickTime`, and its claim that tick time cannot advance within an update is contradicted by that primary usage.

### TP2-011 — confirmed error; accept exact repair

At `en/08-tutorials/01-first-mod.md:226`, use the submitted replacement:

`- \`type = "mod";\` -- Declares the required CfgMods mod type. To keep an addon server-side, load it with the server startup parameter \`-serverMod=\`; do not change this value to \`"servermod"\`.`

This removes the invented `CfgMods` value distinction. The current official URLs were checked but could not be content-retrieved here.

### TP2-012 — essential prerequisite omission; accept revised exact repair

At `en/08-tutorials/01-first-mod.md:389`, replace the paragraph with:

`For offline testing, install a compatible offline mission and launch it using that mission's documented procedure. “Community Offline Mode” is a separate community tool and is not installed by this tutorial; otherwise, test by starting a local DayZ server with the mod loaded and joining it.`

The old main-menu instruction asserts an option/prerequisite the tutorial never provides. No current diagnostic executable was launched.

### TP2-013 — confirmed error; accept revised coordinated repair

In `en/08-tutorials/02-custom-item.md`, replace line 286's `_as` parenthetical with `_as (ambient shadow)`, and replace the line 295 row with:

`| \`_as\` | Ambient shadow | Baked ambient-shadow/occlusion information |`

Do not apply only the table edit, because the preceding prose repeats the same error. The official texture URL was checked but returned 403; this acceptance is based on established engine suffix semantics and should retain no claim about alpha.

### TP2-014 and TP2-014B — confirmed errors; accept exact repairs

Accept both submitted replacements at `en/08-tutorials/02-custom-item.md:349` and `en/08-tutorials/11-clothing-mod.md:292`. They correctly stop presenting a per-type restock delay as the frequency of all CE checks. Because the official CE page was not content-retrievable in this pass, keep the wording limited to “minimum restock delay” and do not add scheduler mechanics.

### TP2-015 — confirmed overclaim; accept exact repair

At `en/08-tutorials/02-custom-item.md:548`, replace the entire step with:

`1. Create a \`.ogg\` audio file in OGG Vorbis format.`

This preserves the tutorial's chosen format while removing the unproved “only format DayZ supports” assertion. The official sound-format proof needed to enumerate all supported alternatives was not available, so add no WAV/WSS list here.

### TP2-016 — confirmed error; accept exact repair

At `en/08-tutorials/02-custom-item.md:64`, accept the submitted replacement. Extracted primary configs demonstrate separate `CfgWeapons` and `CfgMagazines` roots, so “ALL entity types” is false.

### TP2-017 — essential omission; reject submitted repair, author blocker

The finding is valid, but the proposed `spawnedCount` block is not an acceptable tutorial-safety repair: it deletes the buyer's currency first, leaves any partially spawned goods in place, and merely reports the irreversible loss. The author must supply an exact replacement that either (a) stages all goods successfully before committing currency removal, deleting staged goods on failure, or (b) fully rolls back both currency and any partial goods, with every rollback result checked and logged. It must also preserve server authority and bind the request to the `sender` identity already used by the RPC handler. Until exact compilable old/new text and evidence are supplied, disposition is unresolved.

### TP2-018 — essential omission; reject submitted repair, author blocker

The finding is valid, but checking `GiveCurrency` only after deleting sale items does not repair the loss; it reports it. The author must provide exact replacement text that stages/validates payout before deleting items, or implements checked restoration of every removed item on payout failure. The repair must define handling for inventory-full and ground-spawn failure and must not report transaction success after partial settlement. Until then, disposition is unresolved.

### TP2-019 — confirmed error; accept exact repair

Accept the submitted modifier paragraph. The official table does not prove that both sides work, while the extraction distinguishes `kLMenu` and `kRMenu`; exact native combo behavior remains unverified without the current diag executable.

## Blockers for the author/Terra

1. Do not apply TP2-017 or TP2-018 as submitted. Return exact compilable transactional replacements satisfying the rollback/staging requirements above for a new council decision.
2. TP2-009 is a coordinated four-edit repair; a one-literal edit is rejected.
3. TP2-013 requires both prose and table edits.
4. After applying only approved edits, return the exact diff plus post-edit SHA-256 values for every changed page. Council must verify that final diff/hashes before translation propagation.

No page is certified generally correct; these decisions address only the enumerated candidates.
