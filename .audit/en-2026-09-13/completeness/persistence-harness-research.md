# Entity-persistence harness prerequisites and operator recipe

**Research date:** 2026-09-14

**Repository revision inspected:** `bbfa203d036e8f02c733e50011c89b9dfbdf9ecf`

**Scope:** source-first design only; no game, server, client, compiler, packer, or installer was launched

**Decision:** the harness can be implemented on the already demonstrated DayZDiag `1.29.0.163709` server recipe, but successful persistence remains a runtime result to obtain. The plan below does not treat native declarations, a clean process exit, changed file hashes, or public-mod behavior as proof of a CE flush.

This report owns no fixture or EN edits. It is an implementation contract for the fixture author and operator.

---

## Minimal accepted design

Use a private byte-copy of the pinned official `dayzOffline.chernarusplus` mission, the previously successful explicit `instanceId = 1` launch pattern, one isolated profile per process, and one isolated storage tree per test branch. Add the fixture through a CE `types` include, and keep the official mission's `dynamic init="1" load="1" respawn="1" save="1"` setting. Spawn and enumerate only after the controller observes the CE completion marker and supplies a trigger file. End every state-changing process through the official `messages.xml` countdown/shutdown path; the controller waits for self-exit and never calls `Kill()` on a passing run.

The fixture PBO stays the only mod in `-mod`. All variants retain the same `CfgPatches`, `CfgVehicles` classname, virtual prefix, PBO name, and script identity. At the inspected snapshot, the current interfaces are not yet sufficient for the operator:

| Variant | Implemented public harness methods | Missing prerequisite |
|---|---|---|
| v1 | none | label setter plus label/charge getters |
| v2 | `SetFixtureLocked` | label setter plus label/charge/locked getters |
| matrix | label/locked/omit setters and label/charge/locked/omit getters | none for this plan |

The repair target is therefore variant-specific:

```c
// v1, v2, matrix
void SetFixtureCaseLabel(string caseLabel);
int GetFixtureCharges();
string GetFixtureCaseLabel();

// v2, matrix
void SetFixtureLocked(bool locked);
bool GetFixtureLocked();

// matrix only; flag remains non-serialized
void SetFixtureOmitLockedOnSave(bool omit);
bool GetFixtureOmitLockedOnSave();
```

Without the v1 repair, several seed entities all persist as `v1-control` and the requested matrix is not deterministically addressable. Without the v2 repair, the migration and true-resave stages cannot identify and assert all three controls through public methods. These are implementation prerequisites, not claims that the inspected files already provide the API.

### Disposable layout

```text
TEMP/persistence-harness-research/runtime/
  mission/dayzOffline.chernarusplus/       # private copy of official pinned CE mission
    EntityPersistenceFixture/types.xml
    cfgeconomycore.xml                     # one appended <ce> include
    db/messages.xml                        # test-only timed graceful shutdown
    init.c                                 # harness CustomMission
  mods/@EntityPersistenceFixture/Addons/EntityPersistenceFixture.pbo
  config/serverDZ.cfg
  profiles/<run-id>/                       # unique for every process
  branches/
    seed-v1/                               # first writer only
    baseline-v1/                           # immutable copy after seed shutdown
    verify-v1/                             # clone of baseline-v1
    upgrade-chain/                         # clone of baseline-v1
    pre-bad/                               # immutable copy after v2 true reload
    bad-a/                                 # clone of pre-bad
    bad-b/                                 # independent repeat clone
  receipts/<run-id>/
```

The already successful storage mapping was `-storage=<root>` plus `instanceId = 1`, producing `<root>\storage_1\`; the runtime console explicitly selected that directory. Do not point either option at a real server. Preflight must reject any target outside this exact disposable root and reject a seed run if `branches/seed-v1/storage_1` already exists.

### Server configuration and launch

Keep the demonstrated controlled configuration and change only names, ports, mission path, and log paths needed for isolation:

```cpp
hostname = "Entity persistence fixture";
password = "";
passwordAdmin = "fixture-local-only";
maxPlayers = 1;
verifySignatures = 0;
forceSameBuild = 1;
BattlEye = 0;
steamQueryPort = 27983;
instanceId = 1;
logFile = "server_console.log";

class Missions
{
    class PersistenceFixture
    {
        template = "D:\\StarDZ\\docs\\wiki\\TEMP\\persistence-harness-research\\runtime\\mission\\dayzOffline.chernarusplus";
    };
};
```

Use `ProcessStartInfo.ArgumentList`, `UseShellExecute = false`, `WindowStyle = Hidden`, and `CreateNoWindow = true`, as in the retained successful launcher. A concrete argument vector is:

```text
D:\SteamLibrary\steamapps\common\DayZ\DayZDiag_x64.exe
-server
-ip=127.0.0.1
-port=27982
-profiles=D:\StarDZ\docs\wiki\TEMP\persistence-harness-research\runtime\profiles\<run-id>
-storage=D:\StarDZ\docs\wiki\TEMP\persistence-harness-research\runtime\branches\<branch>
-config=D:\StarDZ\docs\wiki\TEMP\persistence-harness-research\runtime\config\serverDZ.cfg
-mod=D:\StarDZ\docs\wiki\TEMP\persistence-harness-research\runtime\mods\@EntityPersistenceFixture
-doLogs
-scriptDebug=true
-noSplash
-limitFPS=30
-fixturePhase=<phase>
```

The retained diagnostic executable is 20,245,560 bytes, product `1.29.0.163709`, SHA-256 `34F6377BE4FD065D104E67263E0C96AC2CB2E348119A4838EBA08D2E61B7A69A`. The prior independent council reproduced that `instanceId = 1` was the sole semantic delta needed to reach `MissionServer.OnInit()` in this exact recipe. This is a version-scoped diagnostic substrate, not production-server certification.

---

## Central Economy registration

Append this block before `</economycore>` in the private mission copy:

```xml
<ce folder="EntityPersistenceFixture">
    <file name="types.xml" type="types" />
</ce>
```

Create `EntityPersistenceFixture/types.xml`:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<types>
    <type name="EntityPersistenceFixtureBattery">
        <nominal>0</nominal>
        <lifetime>3888000</lifetime>
        <restock>0</restock>
        <min>0</min>
        <quantmin>-1</quantmin>
        <quantmax>-1</quantmax>
        <cost>100</cost>
        <flags count_in_cargo="0" count_in_hoarder="0" count_in_map="1" count_in_player="0" crafted="0" deloot="0"/>
    </type>
</types>
```

Why these values are bounded and suitable:

- The official CE mission's `cfgeconomycore.xml:11` includes `Inventory_Base` as an economy root. The configured fixture derives from configured `Battery9V : Inventory_Base`, so it falls under that root; this still requires runtime confirmation through `GetEconomyProfile()`.
- The official mission's `db/economy.xml:3` enables dynamic initialization, loading, respawn, and saving. An inventory item on the ground belongs to the dynamic path for this recipe.
- The official CE documentation says a `type="types"` file under `<ce>` appends/overrides types data and requires all multi-value flags to be explicit. This avoids editing the 900 KB base `db/types.xml`.
- `nominal=0`, `min=0`, no usage/tag/value, and `restock=0` prevent this test type from requesting ordinary loot placement. The official file uses the same zero nominal/min/restock pattern for persisted player-created entities such as `Fence` and `WoodenCrate` (`types.xml:7259-7268`, `21983-21993`).
- `lifetime=3888000` is the official 45-day value for those durable entries, safely longer than the test. `count_in_map=1` matches their world-counting flag. It is not described here as a persistence switch; persistence comes from CE eligibility, dynamic load/save, and creation without a no-persist flag.
- The remaining counting flags are zero because the fixtures stay on the ground and are neither cargo nor player inventory. `crafted=0` reflects script creation. The flags are limiter inputs, not serializer framing.

At runtime, seed must assert `fixture.GetEconomyProfile() != null`, log `GetEconomyProfile().GetLifetime()`, `GetLifetimeMax()`, and `GetLifetime()`, and abort the phase if the profile is absent or the lifetime is non-positive. Static inheritance and XML presence alone do not prove successful CE binding.

### Creation flags

Use a terrain-derived Y coordinate and the persistent form of the extracted object-spawner flags:

```c
vector pos = "7500 0 7500";
pos[1] = GetGame().SurfaceY(pos[0], pos[2]) + 0.05;
EntityPersistenceFixtureBattery fixture = EntityPersistenceFixtureBattery.Cast(
    GetGame().CreateObjectEx(
        "EntityPersistenceFixtureBattery",
        pos,
        ECE_SETUP | ECE_UPDATEPATHGRAPH | ECE_CREATEPHYSICS
    )
);
```

Use X/Z pairs `7500/7500`, `7502/7500`, and `7504/7500`. `objectspawner.c:48-56` starts with those three setup flags plus `ECE_NOLIFETIME | ECE_DYNAMIC_PERSISTENCY`, then removes both latter bits when `enableCEPersistency` is true. The harness therefore uses the resulting persistent combination directly. It must not add:

- `ECE_NOPERSISTENCY_WORLD` (`centraleconomy.c:30`, explicitly “do not save this object in world”);
- `ECE_DYNAMIC_PERSISTENCY` (`:32`, starts without persistence until a player takes it; this headless test has no player);
- `ECE_NOLIFETIME` (`:29`, only suppresses lifetime assignment and does not mean persistence);
- `ECE_LOCAL` (local-only creation).

VPP at pinned commit `dc22e420...` independently uses `ECE_SETUP` and surface/physics-related flags for item creation, but that third-party practice is corroboration only.

The local StarDZ beta at repository commit `24a465d28d7c322cfdaf1af5d2484614f7c1d690` supplies a useful negative control, not authority. `SDZ_GroupStashServerRPC.c:88-99` script-spawns a vanilla barrel with `ECE_PLACE_ON_SURFACE` and then records its logical owner/position separately in JSON. Its companion `SDZ_GroupStash.c:53-59` explicitly says that world-entity persistence was expected but not independently tested. The harness therefore does not copy that beta's assumption: it uses the stricter CE registration, persistent creation flags, isolated next-process readback, and label/PID/value assertions above.

---

## Mission harness contract

Retain the official mission's `main()` (`CreateHive(); ce.InitOffline();`) and `CustomMission : MissionServer` structure. Add a one-second poll from `CustomMission.OnInit()` for `$profile:fixture-trigger.txt`. Read the phase with `GetCLIParam("fixturePhase", phase)` and require the trigger file's single line to equal the CLI phase before doing anything. `GetCLIParam`, `FileExist`, `OpenFile`, `FGets`, and `FPrintln` are declared in extracted `ensystem.c:125-128,397-501`.

The external controller creates the trigger only after it has observed all prerequisites in the current logs:

1. Mission and mission `init.c` compiled and loaded with no config/script errors.
2. `[CE][Hive] :: Init sequence finished.` appears in the current RPT or server console. This exact marker was observed in retained successful runs, including `TEMP/server-mission-council/...RPT:4654` and `TEMP/multi-pbo-council/...RPT:5117`.
3. For reload phases, the expected entity `LOAD_OK` / expected `LOAD_FAIL` callback markers have appeared, or a bounded 120-second post-CE timeout expires. A timeout is failure, never permission to spawn.

This is intentionally stronger than running on `MissionServer.OnInit()`: retained logs place OnInit before CE initialization, and neither vanilla `MissionServer` nor native declarations expose a reviewed “world entity restoration complete” callback. CF's pinned `MissionBase.c:45-58` uses `g_Game.IsLoading()` to synthesize `OnMissionLoaded`, while COT consumes that CF callback, but on a no-GUI dedicated server this is third-party convention rather than proof of CE completion. The observed CE marker plus expected callbacks is the test gate.

### Enumeration and identity

Call `GetGame().GetObjectsAtPosition3D("7502 0 7500" with SurfaceY, 10.0, objects, cargos)` and retain only successful `EntityPersistenceFixtureBattery.Cast` results. `game.c:929` declares the sphere query. Never treat the returned order as stable; build a label map and reject:

- duplicate labels;
- unknown labels;
- a fixture more than 0.75 m horizontally from its assigned X/Z;
- missing or extra fixtures outside the phase-specific expected outcome.

Every marker includes phase, label, `charges`, `locked` when available, position, and the four `GetPersistentID` blocks. Extracted `entityai.c:3380` explicitly documents that this ID stays the same after server restart. Treat the persisted label as the primary case key and the persistent ID plus fixed position as independent continuity checks. On seed, reject an all-zero persistent ID as an assertion key; record it and require a non-zero ID on the first reload rather than inventing when the engine assigns it.

Use these exact labels and positions:

| Label | X/Z | Role after migration |
|---|---:|---|
| `control-false` | `7500/7500` | valid v2 writer, `locked=false` |
| `faulty-writer` | `7502/7500` | one matrix writer that omits only `locked` |
| `control-true` | `7504/7500` | valid v2 writer, `locked=true` |

Only `seed-v1` may call `CreateObjectEx`. It requires the controller's preflight that the storage path did not exist, the CE completion gate, and an enumeration count of zero. All other phases abort on missing entities rather than spawning replacements. A repeated `seed-v1` against existing storage therefore logs `SPAWN_REFUSED existing=<n>` and makes no change.

Recommended terminal markers are `PHASE_BEGIN`, `SPAWN_OK`, `ENUM_OK`, `ASSERT_OK`, `ASSERT_FAIL`, `PHASE_READY_FOR_SHUTDOWN`, plus the fixture's `SAVE`, `LOAD_OK`, and `LOAD_FAIL stage=<field>`. `PHASE_READY_FOR_SHUTDOWN` means mutations and in-process assertions are complete; it does not claim the CE has saved them.

---

## Save boundary and graceful process control

Put this test-only entry in the private mission's `db/messages.xml`:

```xml
<message>
    <deadline>5</deadline>
    <shutdown>1</shutdown>
    <text>Entity persistence fixture shutdown in #tmin minute(s).</text>
</message>
```

The pinned official CE mission contains the same `deadline`/`shutdown` form at `db/messages.xml:11-15`. The official DayZ Server Messages page says `shutdown` terminates after the countdown and specifically recommends this graceful path to avoid adverse effects on player characters and server storage saving. The official DayZ error-code page describes the one-minute `SERVER_SHUTDOWN` state as saving, kicking players, and locking the server for proper shutdown. Direct full-body requests to the current Bohemia wiki returned HTTP 403 on 2026-09-14; these statements were read from the web search index, and the exact XML shape was independently reopened in the pinned official checkout and installed server mission.

The operator launches early enough for `PHASE_READY_FOR_SHUTDOWN` to precede the one-minute shutdown state. The controller records the owned PID and only waits for self-exit. A passing shutdown receipt requires:

- the phase-ready marker occurred before shutdown began;
- the shutdown/save/termination markers available in RPT/console were retained;
- the owned process exited by itself within a bounded deadline;
- `killedByHarness=false` and no `RestartMission()` call;
- recursive storage metadata and SHA-256 manifests were captured before launch and after exit.

If the process remains live after the bound, mark the run invalid first. Cleanup may then terminate only the retained owned Process object, but that run cannot be persistence evidence.

### What proves what

| Observation | Permitted conclusion |
|---|---|
| Process self-exits; no harness kill | only that the process ended through the configured path |
| Exit status is zero or a log says termination completed | clean-exit evidence, not storage flush proof |
| storage files change size/time/hash | bytes changed, not that the target record is complete or readable |
| `OnStoreSave` markers run | the callback was entered and writes returned their recorded booleans, not that native storage committed them |
| Next fresh process reads the same labels/PIDs/values via `OnStoreLoad`, and harness assertions pass | end-to-end observed save/reload for those records and that exact build/config/storage chain |
| Official graceful-shutdown guidance plus successful next reload | strongest available practical evidence here; still not a native call trace or OS `FlushFileBuffers` proof |

There is no reviewed generic script API for “save the entity world now.” The DayZ Diag Menu documentation exposes a UI **Force Save** operation, but no callable declaration was found in the extracted CE API. Do not invent `SaveHive`, `SaveMission`, or equivalent. Ordinary segment saving has no precise timing established by the reviewed sources, so the matrix relies on the documented graceful shutdown plus next-process readback rather than a guessed wait interval.

---

## Required matrix and immutable branches

1. **`seed-v1`** — fresh `branches/seed-v1`; v1 PBO. After the CE gate, require zero fixtures, spawn the three labeled fixtures, validate economy profiles/lifetimes and fixed positions, emit `PHASE_READY_FOR_SHUTDOWN`, and let messages shutdown. Hash all logs, PBO/source/config/mission files, and storage.
2. **Freeze `baseline-v1`** — only after self-exit, copy `seed-v1/storage_1` to immutable `baseline-v1/storage_1`; make a complete relative-path/size/SHA-256 manifest. Never run a process against this baseline.
3. **v1 same-version baseline** — clone baseline to `verify-v1`; start the same v1 PBO. Require exactly three `LOAD_OK variant=v1 schema=1` callbacks and exact labels/charges/positions/non-zero IDs; no spawn. Gracefully shut down. This is the mandatory same-version control.
4. **v1 to v2, default false** — clone baseline to `upgrade-chain`; replace only the canonical PBO with v2. Require all three records to load schema 1 with `migratedLocked=false`; assert every getter is false. Gracefully shut down, which writes normal schema 2 records.
5. **true resave/reload** — start v2 on `upgrade-chain`, find by labels, set only `control-true` to true, assert the other two remain false, then gracefully shut down. Start v2 again and require schema 2 `control-true locked=true`, `control-false locked=false`, and `faulty-writer locked=false`. Gracefully shut down and freeze an immutable `pre-bad` snapshot. This is stronger than merely resaving the default.
6. **bad/control trial A** — clone `pre-bad` to `bad-a`, use the matrix PBO, and require the same three normal v2 records first. Set `faulty-writer.locked=true` and `faulty-writer.omitLockedOnSave=true`; leave the non-serialized omit flag false on both controls. Before shutdown, assert `control-true=true`, `control-false=false`, and exactly one omit flag is true. During graceful shutdown require `SAVE ... locked=OMITTED case=faulty-writer` and ordinary locked writes for both controls. Restart matrix on `bad-a`; require `LOAD_FAIL stage=locked-read case=faulty-writer` plus `LOAD_OK locked=true case=control-true` and `LOAD_OK locked=false case=control-false`.
7. **bad/control trial B** — independently clone the same immutable `pre-bad` to `bad-b` and repeat step 6. This supplies the council's repeated bad/control pair without carrying corruption from trial A. Each trial contains one faulty writer alongside two valid controls.

Do not require the faulty entity to be present or absent after its reader returns false; that native consequence is the subject of the trial. Do require both valid controls to remain readable and correctly valued. Record whether the faulty object is enumerated, deleted, quarantined, or reloads unexpectedly as the runtime result.

Stop after the valid chain and two consistent bad/control trials. On any inconsistent callback order, control failure, duplicate, ID discontinuity, or unexpected respawn, preserve artifacts and return to source analysis instead of varying timers or repeating blind runs.

---

## Separate compilation smoke gate

Before any matrix run, use a distinct `profiles/compile-smoke` and `branches/compile-smoke` with a fresh empty storage root. Use the candidate PBO and a tiny private `init.c` whose `CustomMission` includes a never-called method taking `EntityPersistenceFixtureBattery` as a typed parameter, so the mission compiler must resolve the script class. In `OnInit`, check only:

```c
bool configured = GetGame().ConfigIsExisting("CfgVehicles EntityPersistenceFixtureBattery");
Print("[EntityPersistenceFixture] COMPILE_SMOKE configured=" + configured);
```

The smoke passes only if Game/World/Mission and mission `init.c` load, the World module compiles without script/config errors, the typed mission source compiles, `configured=true`, and the process self-exits through the same messages shutdown. It must not call `CreateObjectEx`, enumerate fixtures, interpret persistence, or assert `OnStoreSave`/`OnStoreLoad`. Run it separately for v1, v2, and matrix because they are different script sources/PBO hashes.

Addon Builder `-packonly` and BankRev inspection remain package gates, not this compilation gate.

---

## Rejected assumptions and alternatives

| Rejected shortcut | Reason |
|---|---|
| Inheritance from `Battery9V` alone makes the custom class persist | No custom-class CE binding was previously tested. Supply a types entry and assert `GetEconomyProfile()` at runtime. |
| `count_in_map=1` is a persistence-enable flag | It controls CE counting. The reviewed evidence does not define it as save eligibility. |
| `ECE_NOLIFETIME` means “persistent forever” | The extracted declaration only says not to set lifetime. It says nothing about saving. |
| `ECE_DYNAMIC_PERSISTENCY` is suitable for the headless fixture | It begins without persistence until a player takes the item; no player participates. |
| Spawn on `MissionServer.OnInit()` or immediately when enumeration returns zero | Retained logs put OnInit before CE initialization; a premature zero can create duplicates. |
| Direct `GetGame().RestartMission()` | The retained dedicated-server probe reloaded the Mission module and then exited with `0xC0000005`; both councils reject it as a reusable healthy loop. |
| Public-mod restart/exit code proves flush semantics | VPP calls `RestartMission()` and Expansion schedules `RequestExit()`, but neither source contains native CE commit/flush evidence. They are implementation examples only. |
| `RequestExit(0)`, Ctrl+C, `Stop-Process`, or harness `Kill()` is automatically equivalent to the documented messages shutdown | No reviewed source establishes that equivalence. The messages route is the explicit official storage-safety recommendation. |
| A zero exit code or changed `dynamic_*.bin` hash proves the record was flushed | Only the next isolated process reading and asserting the record establishes practical end-to-end persistence. |
| The Diag Menu's Force Save implies an available Enforce call | No corresponding callable was found in the extracted `CEApi`; do not invent one. |
| A single bad trial after mutating the only working storage is sufficient | Use two clones of one immutable pre-bad snapshot so valid controls and repeatability remain interpretable. |

---

## Source ledger and provenance

### Official/extracted sources actually opened

| Source | Revision/version; relevant path/symbol | SHA-256 | What it supports |
|---|---|---|---|
| Extracted DayZ scripts | extraction metadata `product=dayz`, raw `version=124588`; `scripts/3_game/ce/centraleconomy.c:9,29-40,745,761` | `6948B104DB21F468E5E4967893B3AB8B7938944731C6B5BC8BC5706910F446A3` | Creation/no-lifetime/no-persist/dynamic flags; CE access and lifetime meaning |
| Extracted DayZ scripts | `scripts/3_game/entities/entityai.c:884,3380-3391` | `AD08181C307BE03549ABC8AFD6A6CEB8532ECA88DA5DA648686CA9FD682A57F5` | Economy profile; persistent ID documented stable across restart; lifetime APIs |
| Extracted DayZ scripts | `scripts/3_game/global/game.c:611,702,929,1162` | `CF529055C48596108034CE6B11826B09BBF5D93E6C550E37785947873D8C3158` | Config lookup, object creation, sphere enumeration, terrain Y |
| Extracted DayZ scripts | `scripts/3_game/objectspawner.c:48-56` | `6CC150C3AAF39B94E9BC1C92F8F4BB9819356E637619FBCA28779DAA7E0DF4B9` | Official persistent object-spawner flag subtraction |
| Extracted DayZ scripts | `scripts/1_core/proto/ensystem.c:125-128,397-501` | `8BE625999A04DF22813052E93FE658C24C82C97B257EBEF86B106279A95DB188` | CLI phase and trigger-file APIs |
| Official CE | `https://github.com/BohemiaInteractive/DayZ-Central-Economy.git`, commit `9a21bb9f5fb9c62a7ce2761402196091588133e6`; `dayzOffline.chernarusplus/init.c` | `73658FCA45ADE1C54D7EE729B31F78F3C27B46282FFD3D503D10B524B8A20AFB` | `CreateHive/InitOffline`, `CustomMission`, mission factory |
| Official CE | same commit; `db/economy.xml` | `62C140967C6040C8E38C7BC5D9FBBFD3966B3EA97A2FEC2AF2D409621EC1F8F8` | dynamic init/load/respawn/save enabled |
| Official CE | same commit; `cfgeconomycore.xml` | `095417FE00A264150D07AB2C1C1A922212D39A041D9554308134ED47408A4615` | `Inventory_Base` root and defaults |
| Official CE | same commit; `db/types.xml:3181-3194,7259-7268,21983-21993` | `59093B764FB976B39BF3A6B74A9156D75529C065C2913B20F7310D42EF85AFA8` | Battery and durable zero-nominal patterns |
| Official CE | same commit; `db/messages.xml:5-15` | `55C9C2DBEC63CEB5059DC38310C4539BA1BFB46EE7AAAD73C8F063A3238B0C8A` | exact scheduled shutdown XML form |
| Official Samples | `https://github.com/BohemiaInteractive/DayZ-Samples.git`, commit `da5e5437c9502620d9853fb6eed14701135ab2ea`; `Test_GardenPlot/config.cpp:1-34` | `2C66BE131A55CFFDED96712245DD74D78E25D003C21A4F51F0B94587C666CD37` | worldScriptModule and configured `Inventory_Base` pattern |
| Installed official server mission | `D:/SteamLibrary/.../dayzOffline.chernarusplus/db/messages.xml` | `55C9C2DBEC63CEB5059DC38310C4539BA1BFB46EE7AAAD73C8F063A3238B0C8A` | byte-identical shutdown example to pinned checkout |

The extraction's `scripts.txt` hash is `E45D501E4FB29587FA1E8BF553B0A7B33B751AA32C5AA5ECB1D03B8B6026F55F`; raw `124588` was not mapped to a public game version. Runtime conclusions must remain tied to the hashed `1.29.0.163709` diagnostic executable.

### Pinned public mods actually opened

| Project | Commit; file | SHA-256 | Bounded use |
|---|---|---|---|
| CF | `0763e7e7548c9a0bed6626afff835de80693ebf3`; `JM/CF/Scripts/5_Mission/CommunityFramework/Mission/MissionBase.c` | `351EC4DFB278D059A35D90F2BB5857F93C60D7CF235C549CC2052B957F247942` | third-party deferred mission-loaded pattern; not CE completion proof |
| COT | `41f2c2b99565d0e3970163e162efbf1283fdca62`; `JM/COT/Scripts/5_Mission/CommunityOnlineTools/MissionServer.c` | `608F0F18F6C8FFA92E0BDAA95197FCEB0B911577DBF0412B34559966741FE67E` | consumes CF `OnMissionLoaded`; no native save/flush semantics |
| Expansion | `6dacd00f6d943ebbd99e0cf1baad93f470d96419`; `DayZExpansion/Core/.../Mission/MissionServer.c:67-85` | `32C1A6FBED8F912E239DAFF0F3860DA2943B627523764D39E23CAACA25F58EEC` | custom CLI parameter and scheduled `RequestExit`; explicitly not flush proof |
| VPP Admin Tools | `dc22e420df3b54e821055f9764da1e48f4a31e71`; `.../ItemManager/ItemManager.c:168-179` | `7130FBB6764792D4114D3FFB688FA2040C00A27B03D1A7E91B53D61E8E8CF17E` | item creation flags corroboration |
| VPP Admin Tools | same commit; `.../ServerManager/ServerManager.c:39-46` | `5D4A26E0693089E16DA99E60F4E3346BFF97D36182B5E34F430773B1A2802756` | direct restart example rejected for this harness |

### Local StarDZ beta implementation actually opened

The local beta is explicitly non-authoritative and was used to identify an unverified shortcut that this recipe must not inherit.

| Repository | Revision; file | SHA-256 | Bounded use |
|---|---|---|---|
| `git@github.com:leonardommello/StarDZ.git` | `24a465d28d7c322cfdaf1af5d2484614f7c1d690`; `StarDZ_Systems_Server/Scripts/4_World/StarDZ_SystemsServer/SDZ_GroupStashServerRPC.c:88-99` | `D7F068DFF77E726CE9F7B35CC8DA076FC4E0A172A062C7AF9A72B2DD3E82BE3E` | real beta spawn path using `CreateObjectEx(..., ECE_PLACE_ON_SURFACE)` plus separate logical-record registration |
| same | same commit; `StarDZ_Systems/Scripts/3_Game/StarDZ_Systems/Groups/SDZ_GroupStash.c:53-59,230-244` | `4A8149C81E759084D7A1973A7E8E3173F8A2C5CE603198075EB44025474C47AA` | source itself labels spawned-object restart persistence as expected and not independently verified; this is a rejected assumption, not evidence of flush |

### Official web sources and access limits

- `https://community.bohemia.net/wiki/DayZ:Server_Messages`, search-index body accessed 2026-09-14: countdown/shutdown behavior and explicit storage-saving safety recommendation. Direct page and MediaWiki API requests returned HTTP 403.
- `https://community.bohemia.net/wiki/DayZ:Error_Codes`, search-index body accessed 2026-09-14: `SERVER_SHUTDOWN` one-minute saving/kick/lock description.
- `https://community.bohemia.net/wiki/DayZ:Server_Configuration`, search-index body accessed 2026-09-14: `instanceId`, `-profiles`, `-storage`, `-mission`, and graceful-shutdown warning.
- `https://community.bohemia.net/wiki/DayZ:Central_Economy_Configuration`, search-index body accessed 2026-09-14: root classes, world segments, save/load effects, and backup configuration.
- `https://community.bohemia.net/wiki/DayZ:Central_Economy_mission_files_modding`, search-index body accessed 2026-09-14: `<ce>` custom `types` inclusion and multi-value-field rule.
- `https://community.bohemia.net/wiki/DayZ:Diag_Menu`, search-index body accessed 2026-09-14: Diag UI Force Save description. Direct full-body request returned HTTP 403; no script call was inferred.

Local mirrors `D:/StarDZ/docs/DayZ/Server Configuration.md` (SHA-256 `D7126F...`) and `Central Economy mission files modding.md` (`F49B20...`) were opened as reference copies, then their claims were checked against the official checkout/search-index evidence. They are not independent runtime proof.

The exact local-document hashes are `D7126F849E9A460887A3B640068CA8C88304324EDFD3AFA1526AE69E4BECAA8E` and `F49B20D4A362FFD0EF4E19429023C8A3CBFB7463E71C26408640DA78B6D9B09C`, respectively. The required prior councils were also reopened rather than treated as proof: `persistence-fixture-council.md` (`43F52A66F99E2DEB9A76FBF067CFC905FB50BC042BF450A6A85FE0C91CB97FA6`), `persistence-source-council.md` (`317093AD43155012AE0EBBA136CBD730C98239210F2C3650AADA257FFAC15398`), `server-mission-investigation.md` (`71F0DC51C1D094951FC4AEBF736B1B49D7D3098849E1E1BE16282EB89BE18269`), and `server-mission-council.md` (`B38247EE24ED756153BBA093D97DB00D09D39F2A4F775A6141272AE51CCCD0CE`). Their retained successful `instanceId=1` receipt and failed direct-restart receipt constrain this recipe; they do not replace a fresh matrix run.

---

## Remaining runtime questions

1. Whether this custom `Battery9V` subclass receives a non-null economy profile and the expected 3,888,000-second lifetime in the tested build.
2. Exact native handling of the matrix record whose final `locked` read fails: entity retention/deletion and following-record isolation.
3. Whether persistent IDs are non-zero immediately after script creation or only after the first save/reload.
4. Which exact log markers and exit status the messages shutdown produces on DayZDiag `1.29.0.163709`; do not predeclare a required numeric exit code.
5. Native OS-level flush implementation remains unopened. Successful next-process readback is practical end-to-end evidence, not a native flush call trace.
6. No stable `DayZServer_x64.exe` was present at the inspected path, so this recipe is presently versioned only for the hashed diagnostic executable.

These questions are bounded by the matrix. No further source-wide audit or direct `RestartMission()` variation is justified before implementing the compile smoke and the first clean seed/reload chain.
