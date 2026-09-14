# English wiki completeness and verification map

Date: 2026-09-13
Content-inventory base revision: `8fa131365f59a343602cefd682290535cd435cc2`
Current revision at final review: `aa75472098d73db6b3c19b046438e530efc290f9`
Scope: the current `en/` tree only; no wiki page, shared configuration, translation, or commit was changed.

## Result

The English wiki has broad subject coverage, but it is not yet a reliable end-to-end knowledge base. The existing 105-page tree explains most common APIs and workflows; the remaining risk is concentrated in unexecuted language/runtime claims, multi-package dependency behavior, asset/tool output, network abuse and recovery, entity persistence migrations, Central Economy terrain authoring, production operations, and tutorial artifacts that have never been compiled or exercised as a whole.

This map distinguishes three things:

- **Observed gap:** the live wiki omits the topic, explicitly says it is not covered, contradicts itself, or makes a claim that the prior council left unsupported.
- **Verification gap:** prose exists, but its example or behavior still needs a compiler, tool, client/server, or operational test.
- **Candidate topic:** useful future breadth whose necessity has not yet been established. These are not counted as defects.

The previous second-pass report remains a defect audit, not a completeness certificate. It recorded 55 accepted repairs, four rejected proposals, eight unresolved leads, 210 pre-existing anchor failures, and no full build, Enforce compile, game/server/client run, exploit test, asset-tool run, or transaction fault test. The independently reviewed anchor repair is now integrated at commit `789abaf29df2642912c4b7c7e05b18ff514d1665`: its final renderer-backed strict check scanned 105 EN files and 1,278 fragments with zero dead fragments, and its separate file-link scan reported zero dead file links. That resolves the navigation defect class, but not the casting label mismatch or any technical/runtime gap below.

## Method and inventory

- Used the existing Graphify graph first for orientation. Its RPC/server path found the expected links among `06-engine-api/09-networking.md`, `02-mod-structure/06-server-client-split.md`, mission classes, and `requiredAddons`; it is an orientation aid, not evidence.
- Enumerated all Markdown files and all level 1-3 headings under `en/` with `rg` and PowerShell, then read the pages named below. The tree contains 105 pages: 13 language, 6 mod structure, 10 GUI, 8 file-format/tool, 6 config, 24 engine API, 7 patterns, 13 tutorials, 12 server administration, and 6 root/reference pages.
- Raw heading counts in code-heavy pages include shell comments such as `# Generate a key pair`; therefore raw `#` counts are not rendered-H1 counts. The previous renderer check, not this raw scan, is the relevant evidence for one rendered H1 per page.
- Reopened `.audit/en-2026-09-13/doublecheck/REPORT.md`, `findings-dispositions.json`, `coverage-consolidated-REPORT.md`, `source-use-REPORT.md`, and the language/trading council reports. Prior conclusions were treated as leads and checked against the live pages and sources where used here.
- Opened representative local non-wiki documentation, extracted game declarations, StarDZ beta code, official sample repositories, and public mod code. Source provenance is recorded below.

## Existing-domain inventory

| Existing domain | Pages | What the headings already cover | Completeness judgment |
|---|---:|---|---|
| `01-enforce-script` | 13 | Types, collections, classes, modded classes, control flow, strings, math, memory, reflection, preprocessor, errors, gotchas, functions | Broad reference; eight runtime/compiler leads remain, and there is no reproducible version-compatibility workflow. |
| `02-mod-structure` | 6 | Script modules, `config.cpp`, `mod.cpp`, minimal mod, file organization, client/server split | Broad overview; multi-PBO/dependency behavior is fragmented and not validated as one build/load matrix. |
| `03-gui-system` | 10 | Widgets, layouts, sizing, containers, creation, events, styles, dialogs, production patterns, advanced widgets | Broad script/UI reference; asset registration and focus/input behavior lack packaged client evidence. Two unsupported asset-performance claims remain live. |
| `04-file-formats` | 8 | Textures, models, materials, audio, tools, PBOs, Workbench, buildings | Broad descriptive coverage; the source-to-packed-to-retail pipeline has not been executed for the examples. Multi-PBO depth belongs to the separate PBO research task. |
| `05-config-files` | 6 | Localization, inputs, credits, imagesets, server/mission config, spawn gear | Good file-by-file reference; schema/version provenance and failure fixtures are inconsistent across files. |
| `06-engine-api` | 24 | Entity, vehicles, world systems, GUI-adjacent effects, I/O, RPC, CE, hooks, actions, player, sound, crafting, construction, animation, terrain, particles, AI, admin, quick reference | Large static API survey; public declarations do not validate native outcomes. Entity persistence extension and API-version migration are conspicuous omissions. |
| `07-patterns` | 7 | Singleton, modules, RPC, config persistence, permissions, events, performance | Useful patterns; no executed fault-injection suite, durable transaction pattern, or entity persistence migration pattern. |
| `08-tutorials` | 13 | First mod, content mods, admin/RPC/UI, scaffolding, debugging, publishing, templates, trading, diagnostics | High apparent usability, but no tutorial was compiled/packaged/run in the recorded audit. Trading and “production-ready” claims need immediate correction or evidence. |
| `09-server-admin` | 12 | Install, layout, config, CE, spawning, persistence, tuning, access, mods, troubleshooting, advanced operations | Stronger after the server audit, but production hardening, restore drills, update rollback, log/crash operations, and several access-control claims remain weak or absent. |
| Root references | 6 | Index/README, cheatsheet, FAQ, glossary, troubleshooting | Useful navigation; must be regenerated or cross-checked whenever canonical pages change. The casting TOC currently says “String-Based” while the section correctly says “Config-Based.” |

## Actionable cross-domain matrix

### 1. Language and runtime

| ID | State | Concrete gap or risk | Target | Acceptance and evidence needed |
|---|---|---|---|---|
| LANG-C01 | P0 verification | Eight inherited/runtime leads remain unresolved; see the dedicated table below. | Existing pages named below plus a durable runtime report under `.audit/`. | Run minimal isolated fixtures against the installed stable `DayZDiag_x64.exe` 1.29.0.163709 and, where meaningful, dedicated/listen/client contexts. Capture source, launch line, fresh log identity, expected/actual output, executable hash, and cleanup. |
| LANG-C02 | P1 observed gap | No EN page teaches how to pin a DayZ build, use `DayZ-Script-Diff`, compare local extraction with line-ending normalization, or audit changed/obsolete signatures after an update. Searches found no `DayZ-Script-Diff`, `Scripts Rev`, build-provenance, or compatibility-matrix coverage. | Expand gotchas/debugging/engine quick reference or add a focused `en/01-enforce-script/14-versioning-api-migration.md`; choose the smallest canonical home and update EN/shared navigation if a page is added. | Demonstrate a real two-commit API diff, identify build and script revision, separate declarations from native behavior, and include an update checklist. Verify links and commands against the official repository HEAD used for the article. |
| LANG-C03 | P2 correction | `en/01-enforce-script/09-casting-reflection.md:14` calls `IsKindOf` “String-Based Type Checking,” while the live heading at line 201 says “Config-Based Type Checking.” | `en/01-enforce-script/09-casting-reflection.md` TOC only. | Make terminology match, then run the strict anchor checker and render the page. No runtime test is needed. |

### 2. Packaging, multi-PBO, and dependencies

The separate PBO worker owns deep format/limit research. This map inventories the documentation need without asserting a numeric limit or duplicating that investigation.

| ID | State | Concrete gap or risk | Target | Acceptance and evidence needed |
|---|---|---|---|---|
| PKG-C01 | P0 observed gap | Multi-PBO material is split among `02-config-cpp`, `02-server-client-split`, `04-pbo-packing`, per-PBO stringtables, and server mod management. There is no single end-to-end example with three PBO prefixes, distinct `CfgPatches`, cross-PBO `requiredAddons`, `CfgMods` script modules, client/server packages, build order, signing, deployment, and expected load logs. | Expand `en/04-file-formats/06-pbo-packing.md` or add `en/04-file-formats/09-multi-pbo-design.md`; cross-link the canonical dependency section. | Await the PBO worker's evidence. Then build and inspect every PBO, record stored prefixes/config entries/signatures, boot with packed files and no file patching, and test missing/cyclic dependency failures. Do not publish any size ceiling without scoped evidence. |
| DEP-C01 | P1 verification | `en/02-mod-structure/02-config-cpp.md:130-135` emphasizes the addon dependency graph, while `en/09-server-admin/10-mod-management.md:117-124` recommends launch-line ordering but admits Bohemia does not document it as the resolver. The relationship among `requiredAddons[]`, `CfgMods.dependencies[]`, `defines[]`, `-mod`, `-serverMod`, and Workshop “Required Items” is not verified as a matrix. | Canonical dependency table in `02-config-cpp`; operator consequences in `09-server-admin/10-mod-management.md`. | Construct small A/B/C PBO fixtures and test present, missing, transitive, reversed launch order, optional define, cross-`-mod`/`-serverMod`, and cycle cases. Record RPT and compile logs separately. |
| PKG-C02 | P1 retained unsupported claims | Prior council rejected the proposed evidence for “native imageset parses fastest” (`03-gui-system/07-styles-fonts.md:530`) and retail MLOD loading (`04-file-formats/02-models.md:39,60`). The unsupported original wording remains live. | Those two pages; packaging conclusions may depend on the PBO worker. | Either obtain version-specific tool/runtime evidence or replace with neutral, source-bounded wording. Independent council must reopen the actual source/tool result. |

### 3. GUI, assets, and tools

| ID | State | Concrete gap or risk | Target | Acceptance and evidence needed |
|---|---|---|---|---|
| GUI-C01 | P1 verification | The pages describe layouts, imagesets, focus, input exclusion, scaling, and advanced widgets, but no packaged sample is shown working across common aspect ratios, UI scales, reopen/close cycles, disconnect, and dedicated-server absence of presentation code. | `03-gui-system/02-layout-files.md`, `03-sizing-positioning.md`, `06-event-handling.md`, `08-dialogs-modals.md`, plus `08-tutorials/08-hud-overlay.md`. | Package a minimal UI fixture; capture screenshots/logs at two aspect ratios and UI scales; test keyboard/mouse focus restoration, repeated open/close, reconnect, and dedicated server boot. |
| ASSET-C01 | P0 verification | Texture/model/material/audio/build pages have not been passed through the installed DayZ Tools and then loaded in retail/Diag. Static prose cannot establish Binarize output, baked paths, material stages, geometry behavior, audio attenuation, or retail compatibility. | `04-file-formats/01-textures.md` through `08-building-modeling.md`; prioritize model/material and the custom-item/vehicle tutorials. | For one minimal asset of each type, record source placement, tool versions/hashes, exact commands/options, exit code plus logs, PBO inspection, clean retail/Diag load, and expected visual/audio result. Keep MLOD/ODOL and imageset claims unresolved until this exists. |
| GUI-C02 | Candidate, not defect | Vanilla/community UI ecosystems include animation helpers and MVC-style binding not covered as named APIs. The wiki already teaches simpler native patterns, so this is optional advanced breadth rather than a reliability blocker. | Possible future advanced UI chapter only after source/license review. | Show that the chosen API is current, reusable outside one framework, and materially improves a tested example. Do not copy third-party code beyond license terms. |

### 4. RPC, server authority, and security

| ID | State | Concrete gap or risk | Target | Acceptance and evidence needed |
|---|---|---|---|---|
| RPC-C01 | P0 observed/verification gap | The RPC pages cover sender validation, permission checks, target binding, small payloads, payload versioning, and one sentence on request IDs/idempotency. They do not implement replay suppression, response correlation, bounded queues, timeout/cancel behavior, disconnect cleanup, or per-sender rate limiting. The extracted API does not document native payload or rate limits. | Add a worked hardened protocol to `en/07-patterns/03-rpc-patterns.md`; keep raw API facts in `06-engine-api/09-networking.md`. | Implement a minimal request ID + duplicate cache + bounded payload/count + per-sender limiter; test duplicate, malformed/truncated, wrong target, unauthorized, flood, disconnect, stale response, and broadcast/privacy cases with two clients. Report measured payload behavior without presenting it as a universal limit. |
| RPC-C02 | P1 correction/qualification | `07-patterns/03-rpc-patterns.md:825,840` states there is a practical per-RPC ceiling but records no measurement or source. Local security research explicitly found the maximum, fragmentation/drop behavior, and native limiter undocumented. | Same RPC pattern page. | Qualify as unmeasured or replace with a build-scoped measured result. Record client/server versions and whether guaranteed/unreliable delivery changes the outcome. |
| SEC-C01 | P1 evidence gap | Public and beta mods demonstrate useful authorization patterns but also show why popularity is not proof: VPP checks permission before delete/free-camera, while its file logs plaintext IDs contrary to the vanilla privacy comment; StarDZ correctly derives identity from `sender` and guards target equality, but remains beta code. | Source notes in `06-engine-api/22-admin-server.md`, `07-patterns/05-permissions.md`, and the hardened RPC example. | Label each as third-party behavior at a pinned commit; corroborate native claims from extracted declarations; execute abuse tests rather than treating code review as exploit proof. |

### 5. Persistence and Central Economy

| ID | State | Concrete gap or risk | Target | Acceptance and evidence needed |
|---|---|---|---|---|
| PERSIST-C01 | P0 observed gap | `07-patterns/04-config-persistence.md` covers JSON config migration, but the EN tree has no canonical treatment of entity `OnStoreSave`/`OnStoreLoad`, ordered read/write contracts, per-mod storage versions, failure returns, or `GAME_STORAGE_VERSION`. Searches found `OnStoreSave` only in construction/troubleshooting, `OnStoreLoad` only in troubleshooting, and no `GAME_STORAGE_VERSION`. | Add a focused section to the canonical persistence pattern or create `en/07-patterns/08-entity-persistence-migration.md`; link from entity, construction, server persistence, and troubleshooting pages. | Build a version 1 entity, save, upgrade to version 2, load successfully, test truncated/wrong-order data, preserve `super`, and capture clean restart logs. Distinguish engine storage version from a mod-owned schema version. |
| PERSIST-C02 | P1 verification gap | JSON pages check bool/error and suggest `.bak`, but do not provide a proven atomic replacement/recovery protocol or fault tests for write interruption. The server persistence page recommends backups but no restore drill. | `06-engine-api/08-file-io.md`, `07-patterns/04-config-persistence.md`, `09-server-admin/07-persistence.md`. | Test save failure, truncated JSON, stale/corrupt primary, backup selection, and restore. If rename/atomicity cannot be proved with exposed APIs, state that and document bounded best effort rather than promising atomic writes. |
| CE-C01 | P0 observed gap | `09-server-admin/04-loot-economy.md:67-72` explicitly lists `mapgrouppos.xml`, `mapgroupcluster*.xml`, `mapclusterproto.xml`, `mapgroupdirt.xml`, and `areaflags.map` as not covered. These are essential for custom terrains and non-building loot placement. | Expand the canonical CE chapter or add a focused terrain-authoring chapter under `09-server-admin`, cross-linked from terrain queries and building modeling. | Use official CE repository and extracted mission data; explain generation vs hand editing, local/world coordinates, building prototypes, clusters, CETool area flags, map-specific differences, and expected output. Validate on an offline Diag mission before any server claim. |
| CE-C02 | P1 observed gap | CE diagnostics (`SpawnAnalyze`, `EconomyLog`, `EconomyMap`, `EconomyOutput`) are named in API/Diag pages but the operator chapter lacks a task-oriented “item does not spawn” lab with inputs, outputs, interpretation, and destructive-tool boundaries. | Add a diagnostic workflow to `09-server-admin/04-loot-economy.md` or `11-troubleshooting.md`. | Run `SpawnAnalyze("*")`, one class-specific map, `setupfail`, and non-destructive `EconomyOutput` modes on the pinned Diag build; preserve generated CSV/TGA/log samples and explicitly gate `Mark/Remove/CleanMap`. |
| CE-C03 | P1 verification | Several CE semantics and numeric ranges remain build/map-specific or unconfirmed (for example custom globals, cluster flags, event limit modes, and restart respawn behavior). | Existing CE API/admin pages with source/version annotations. | Maintain a per-build/map evidence table; do not generalize Chernarus counts or a native declaration to all maps/builds. |

### 6. Administration, deployment, security, and performance

| ID | State | Concrete gap or risk | Target | Acceptance and evidence needed |
|---|---|---|---|---|
| OPS-C01 | P0 correction | `09-server-admin/09-access-control.md:27-38` says `passwordAdmin` is also used for RCON, but the same page later configures the separate `RConPassword` in `beserver_x64.cfg`. This is an internal contradiction and the official server configuration reference separates the settings. | `09-server-admin/09-access-control.md`. | Correct the credential mapping from official docs, test both login paths on a disposable server, and document where each secret is stored and logged. |
| OPS-C02 | P1 verification/correction | `09-server-admin/09-access-control.md:183-193` attributes a player list, teleport, admin map, and free camera to built-in vanilla admin tools without a primary source or runtime capture. These may describe third-party tools. | Same page. | Inventory actual vanilla commands/UI on the pinned server/client, separate them from VPP/COT features, and retain only demonstrated capabilities. |
| OPS-C03 | P1 observed gap | No EN page covers least-privilege service identity, secret handling/rotation, RCON bind/firewall exposure, file ACLs, or separation of server, SteamCMD, backup, and webhook credentials. Searches found no “service account,” “least privilege,” or “credential rotation.” | New hardening section in `09-access-control.md` and deployment checklist in `01-server-setup.md`. | Provide Windows and Linux threat-bounded procedures, verify resulting listener/bind behavior, show secrets excluded from artifacts/logs, and test credential rotation without losing access. Avoid undocumented BattlEye promises. |
| OPS-C04 | P1 observed gap | Backups are described, but there is no checksum/restore drill, recovery-time objective, rollback gate for mod/server updates, or proof that a restored generation boots. Log rotation, retention, disk alerts, and native crash/minidump triage are also absent. | `07-persistence.md`, `10-mod-management.md`, `11-troubleshooting.md`, `12-advanced.md`. | Perform a stop-save-backup-update-fail-restore-boot drill; verify storage generation and player/world state. Add log/dump identity, retention, free-space alert, and stale-log avoidance checks. |
| PERF-C01 | P1 verification | Performance pages mix declarations, community rules of thumb, recommended values, and unmeasured causal statements. No repeatable baseline/experiment protocol ties server FPS, population, CE load, script profiler, and hardware to a build. | `07-patterns/07-performance.md`, `09-server-admin/08-performance.md`, debugging chapter. | Define a controlled workload and before/after metrics, preserve configuration and logs, repeat runs, and label measurements as build/hardware/map/mod-set specific. Do not promote rules of thumb to thresholds. |

### 7. Genuinely usable tutorials and examples

| ID | State | Concrete gap or risk | Target | Acceptance and evidence needed |
|---|---|---|---|---|
| TUT-C01 | P0 contradiction and incomplete example | `08-tutorials/12-trading-system.md:6,28-59` still promises and diagrams a complete currency transaction, while the current handlers at lines 326 and 344 deliberately refuse and the safety boundary at line 412 says no transaction protocol exists. The chapter is a UI/RPC/catalog/refusal tutorial, not a trading system. | Trading summary, “What We Are Building,” both diagrams, Step 9 expectations, and navigation descriptions; then the missing functional transaction example. | Immediately align all claims with the refusal behavior, but do not count wording repair as completion. Deliver a genuinely usable purchase path with reservation/escrow or compensation, durable state, idempotency, disconnect/restart recovery, and fault tests before any “complete” claim. |
| TUT-C02 | P0 verification/wording and incomplete example | `08-tutorials/09-professional-template.md:6` calls the artifact complete, production-ready, and copy-paste ready, but the recorded audit ran no compiler, packer, dedicated server, or client. | Professional template, plus scaffold pages that call it battle-tested, and an exact functional fixture. | Downgrade unsupported claims immediately, but do not count that as usable-template completion. Materialize the exact files and pass config parse, Enforce compile, PBO build/inspection/signing, dedicated boot, client join, UI/RPC/config tests, clean shutdown, and restart. |
| TUT-C03 | P1 coverage quality | Across 13 tutorial files, only 6 have an explicit `## Prerequisites`, 7 have a “Complete File/Code Reference,” and 4 contain the word “expected.” These lexical counts do not prove quality, but they identify inconsistent teaching contracts. | All tutorials, starting with 03, 04, 09, 10, 11, and 12. | Every build tutorial must state dependencies, exact placement, execution side/layer, expected observable result, negative/error path, and what was actually validated. Reference-only chapters (debugging, publishing, Diag menu) should say they are reference/workflow pages rather than pretend to build a feature. |
| TUT-C04 | P1 verification | “Complete” snippets are embedded in Markdown, not extracted into buildable fixtures; edits can make repeated snippets drift. | Create versioned fixture directories outside prose, then include or mechanically compare snippets. | Add a manifest mapping every tutorial file to fixture files and hashes; compile/package/run fixtures on the target build and fail verification when prose snippets diverge. This is documentation validation, not a new general test framework for the repo. |

### 8. Supplied local corpus follow-up

| ID | State | Concrete gap or risk | Target | Acceptance and evidence needed |
|---|---|---|---|---|
| CORPUS-C01 | P1 required verification follow-up | The user-supplied local corpus is wider than the representative documents opened for this bounded map. Its 64 requested entries are now preserved in `user-source-inventory.json` as inventoried or enumerated, not reviewed. It includes additional `GUIA_*`, `REFERENCIA_*`, `API_*`, `DAYZ_*_REFERENCE`, architecture/deep-study/cookbook/CF references, plus `plans/`, `vanilla_metadata/`, `AI/`, `DayZ/`, and StarDZ specifications, plans, contracts, HTML, and JSON. No claim is made here that all files were read, authoritative, or implemented. | A durable local-corpus-to-EN crosswalk under `.audit/en-2026-09-13/completeness/`, followed by only independently verified wiki proposals. | Starting from `user-source-paths.txt` and `user-source-inventory.json`, classify each source as extracted fact, implemented code, design contract, product proposal, local research, or third-party note; map unique claims to existing EN pages and current findings; reopen the underlying official/code evidence before promoting a claim. Prioritize numeric limits, version migration, and the currency-bridge/transaction contract, and explicitly separate shipped behavior from planned behavior. |

## Eight unresolved prior leads

All eight are still unresolved in `findings-dispositions.json`; none should be silently counted as verified. The installed runtime inventory at `.audit/en-2026-09-13/completeness/runtime-inventory.json` shows stable Diag 1.29.0.163709 and Experimental server/Diag 1.29.0.163401 are available. A separate runtime-probe task was active at delivery time, but it had not yet returned reviewed results, so this map keeps every lead unresolved.

| Prior ID | Live claim/location | Bounded probe |
|---|---|---|
| `LANG-DC-008` | `01-enforce-script/07-math-vectors.md:664,700` says zero normalization produces NaN. The extracted declaration documents nonzero behavior only. | Print the pre/post vector and returned length for zero and control vectors; use explicit finite/NaN checks if exposed. Run in a fresh Diag script fixture and record exact output. |
| `LANG-INHERITED-001` | `01-enforce-script/09-casting-reflection.md:313,582` says `typename.Spawn()` only works for a parameterless constructor. The exposed method takes no arguments but does not document failure behavior. | Compile/run classes with no explicit constructor, parameterless constructor, and only parameterized constructor; capture compile diagnostics, returned class/null, and destructor behavior. |
| `LANG-INHERITED-002` | `01-enforce-script/03-classes-inheritance.md:901` and `13-functions-methods.md:746,1068` say omitted `override` creates a distinct method selected by static type. | Compile parent/child fixtures with and without `override`; call through parent- and child-typed references and record warnings plus output. |
| `LANG-INHERITED-003` | `01-enforce-script/08-memory-management.md:215-245,699,729,753` says `autoptr` is equivalent to ordinary strong references and “adds nothing.” | Retain an alias outside an `autoptr` scope and compare against `ref`/plain-local controls; log destructor and alias validity. Run more than once to avoid stale-log inference. |
| `LANG-INHERITED-004` | `01-enforce-script/08-memory-management.md:469-497` categorically says statics survive mission restart/reconnect and initialize once per process. | Increment static markers in engine/game/world/mission layers; test reconnect, `#restart`, mission reload, dedicated restart, listen host, and client process restart separately. |
| `LANG-INHERITED-005` | `01-enforce-script/08-memory-management.md:499` says there is no `Object.IsDeleted()`. Absence from public scripts cannot prove the native surface globally. | First rephrase to “not found in pinned public declarations” unless documentation exists. A negative compile fixture on the target build can establish availability for that build only. |
| `LANG-INHERITED-007` | `02-mod-structure/06-server-client-split.md:79-140,416-707` and `01-enforce-script/12-gotchas.md:704` contain categorical listen/client/server truth tables and load-phase behavior. | Emit compile-time `SERVER` markers and runtime `IsDedicatedServer/IsServer/IsClient/IsMultiplayer` values from early and mission hooks on dedicated, remote client, offline, and listen contexts. Capture which mission classes instantiate. |
| `LANG-INHERITED-008` | “Global-scope `Print` load-order advice” has no precise candidate location in the prior ledger. | Before testing, identify the exact wiki claim. Then compile top-level `Print` fixtures in each module and record whether it parses/executes and at what point. Do not edit a guessed location. |

## Tutorial readiness snapshot

“Static” below means only that the current Markdown contains a plausible workflow; it is not runtime approval.

| Tutorial | Current teaching value | Remaining proof before calling it runnable |
|---|---|---|
| 01 First Mod | End-to-end folder/config/script/pack/log sequence | Exact fixture, Addon Builder result, packed retail/Diag load, fresh log marker. |
| 02 Custom Item | Config, texture, CE, localization, test steps | Binarized asset, PBO inspection, inventory spawn, CE spawn, material/render check. |
| 03 Admin Panel | Detailed UI/RPC/permission roundtrip | Two-client authorization, malformed RPC, timeout/disconnect, focus restore, dedicated boot. |
| 04 Chat Commands | Detailed command path; one permission block is explicitly conceptual | Replace/implement the conceptual permission source, test ambiguous names, unauthorized/crafted input, and response routing. |
| 05 Mod Template | Useful scaffold workflow | Materialize the scaffold and verify rename, compile, pack, no stale identifiers/prefixes. |
| 06 Debugging/Testing | Reference workflow | Verify each command/tool on the pinned build and demonstrate fresh-log identity plus one controlled failure. |
| 07 Workshop Publishing | Deployment checklist | Use a disposable/private Workshop item or clearly label unexecuted steps; test key rotation and rollback. |
| 08 HUD Overlay | Detailed client/server HUD | Package, two resolutions/scales, reconnect, missing response, input/focus cleanup, dedicated boot. |
| 09 Professional Template | Extensive copyable prose | Highest priority fixture because “production-ready/copy-paste ready” is currently unproved. |
| 10 Vehicle Mod | Config/script/event coverage | Binarize/load/physics/doors/wheels/event-spawn tests; placeholder geometry comments must not imply a custom model is complete. |
| 11 Clothing Mod | Config/texture/cargo/localization coverage | Binarize/load, wearable model/slot/attachments, inventory/CE spawn, client visual test. |
| 12 Trading System | Strong safety explanation, but handlers refuse | Relabel as non-transactional now; a live version needs durable, idempotent, fault-tested transaction design. |
| 13 Diag Menu | Useful reference, not a feature build | Verify shortcuts/menu availability and developer-only operations on the pinned Diag executable. |

## Source use and provenance

### Official and extracted evidence

- Official repositories were checked live on 2026-09-13: `BohemiaInteractive/DayZ-Script-Diff` HEAD `86974a0f5bd16b1ee3e334ad828133c93dca80a1`; `DayZ-Samples` HEAD `da5e5437c9502620d9853fb6eed14701135ab2ea`; `DayZ-Central-Economy` HEAD `9a21bb9f5fb9c62a7ce2761402196091588133e6`.
- Direct GETs to the official/community BIKI pages for Modding Basics, Modding Structure, Server Configuration, and Central Economy returned HTTP 403 on 2026-09-13. Search-indexed official text was readable and was used only for the documented facts it displayed; local mirrors under `D:/StarDZ/docs/DayZ` remain fallible copies.
- Official URLs consulted: `https://community.bistudio.com/wiki/DayZ:Modding_Basics`, `https://community.bistudio.com/wiki/DayZ:Modding_Structure`, `https://community.bistudio.com/wiki/DayZ:Server_Configuration`, `https://community.bistudio.com/wiki/DayZ:Central_Economy_Configuration`, `https://community.bistudio.com/wiki/DayZ:Central_Economy_setup_for_custom_terrains`, and the three official GitHub repositories above.
- Extracted `D:/DayZ Projects/scripts/3_game/gameplay.c:104-117`, SHA-256 `AA12624843F51C70200D37449559FDBADB042D333D4EE74C989E0CA632D2F0FE`, documents `ScriptRPC.Send`, direction, repeated-buffer behavior, target, ID, and recipient/privacy guidance.
- Extracted `scripts/3_game/dayzgame.c:3104-3118`, SHA-256 `75CD42B6CBE689F0903F23CDEE46FD41545946B0046D3816B15B4F36044C8992`, shows global event invocation and target-object forwarding.
- Extracted `scripts/3_game/entities/entityai.c:2913-2995`, SHA-256 `AD08181C307BE03549ABC8AFD6A6CEB8532ECA88DA5DA648686CA9FD682A57F5`, documents ordered `OnStoreSave`/`OnStoreLoad`, `super`, `ctx.Read` failures, and server-side context.
- Extracted `scripts/3_game/ce/centraleconomy.c:157-208,285-309,505-530`, SHA-256 `6948B104DB21F468E5E4967893B3AB8B7938944731C6B5BC8BC5706910F446A3`, exposes `EconomyOutput`, `SpawnAnalyze`, `EconomyLog`, and `EconomyMap` diagnostics and their developer/Diag limits.
- Extracted `scripts/1_core/proto/enconvert.c:140-156,521-530`, SHA-256 `ABF20B92773A0872EB890F5A36EA3E4A228E4D4724BB9CD3ED86FC534A718CD4`, documents only nonzero normalization example and a no-argument `typename.Spawn`; it does not establish the disputed outcomes.
- Extracted `scripts/3_game/global/game.c:1120-1127`, SHA-256 `CF529055C48596108034CE6B11826B09BBF5D93E6C550E37785947873D8C3158`, declares side checks and says `IsDedicatedServer` is valid sooner, but does not prove the wiki's full load/listen truth table.

### Local documentation opened as leads

- `D:/StarDZ/docs/GUIA_SEGURANCA_E_MULTIPLAYER.md:929-1008,1086-1195,1572-1601`, SHA-256 `43AAECA6B5A5353499FE592C47615766EDE14DC8AB53B9E21B6551E32CFB07E8`: rate limiting, malformed reads, target spoofing, replay/idempotency, recipient privacy, and explicit unmeasured network limits. This is local research, not native proof.
- `D:/StarDZ/docs/GUIA_ECONOMIA_E_LOOT.md:434-551,1708-1851`, SHA-256 `25EEB8790E5FBDAECFE6A3FC04E709BDC6F6B93E5DDC9DC38E6132045A465F75`: map-group/cluster concepts and task-oriented CE diagnostics. Counts and interpretations are build/map-specific leads.
- `D:/StarDZ/docs/REFERENCIA_VERSOES_E_MIGRACAO.md:156-235,374-503`, SHA-256 `E3BBC9D5295202BA063F7D3B3659B2928F32171F811BBA8B8B0A201B6F97EFCD`: script-diff provenance workflow and entity persistence migration. Its recorded local build is older than the stable executable now inventoried, so every version statement must be refreshed.
- Headings were also inspected in `GUIA_FERRAMENTAS_E_BUILD.md`, `GUIA_DEBUG_E_PERFORMANCE.md`, `REFERENCIA_LIMITES_E_MUROS.md`, `COOKBOOK_RECEITAS_COMPLETAS.md`, and `DAYZ_GUI_REFERENCE.md` to identify candidate omissions. Their unverified assertions were not promoted into this map.

### Public mods and beta implementations opened as fallible examples

- Official `DayZ-Samples` commit `da5e5437c9502620d9853fb6eed14701135ab2ea`: `Test_Inputs/config.cpp:1-33` (SHA-256 `71B869D713C15D38037B0B8B6CC682CCAEA03599DDFF370DA786D42CD813121C`) and `Test_Building/config.cpp:1-124` (SHA-256 `3A6FB41F49D418637A8513383D3CB1E2F84B95EFE962EE0FD755F1B6268F56EE`) show real `CfgPatches`/`CfgMods`/input and building-config shapes, not multi-PBO or runtime proof.
- Community Framework commit `0763e7e7548c9a0bed6626afff835de80693ebf3`: `RPCManager.c:45-215` (SHA-256 `377E40A999D5465EC754DDAD98EE96AC16218613187261CEAFBFA29A0F21C622`) shows one engine ID plus string routes and reflective dispatch; `CF_ModStorage.c:1-125` (SHA-256 `6FCF72DDC889D751F02BE1097DBC19126F851E7712A90EC2F52FA61B4E59D7B0`) shows framework-owned versioned storage. These are framework choices, not vanilla contracts.
- VPP Admin Tools commit `dc22e420df3b54e821055f9764da1e48f4a31e71`: `AdminTools.c:1-95` (SHA-256 `1806BF6FD6C4E07E6D81AF0142254AFF7233CB0C1A109CEA057C517072BC9208`) checks permissions before privileged actions but also logs plaintext IDs. It demonstrates both a useful pattern and why public code is not authority.
- StarDZ beta `SDZ_ServerAdminRPC.c:46-130` (SHA-256 `C2EDCD688061EC589674F7D6084B6B96EF100896FCA410D204632EAF48A3C03E`) and `MHRPCServerHandler.c:1-130` (SHA-256 `7A24F9EB3095F041B5BC3FDFEB59AFE1E3332E74B3F140B98DEDCCE025A3F0F7`) show sender-owned permission and target-spoof guards. `MHSerializedItem.c:80-180` (SHA-256 `9A3EDA11E88A8E28CAA5FCD76873747D12788EB1A2F750BEBFF2E7D2E9555CB4`) checks deserialization/creation but does not establish full transaction recovery. These beta implementations may contain defects.

## Prioritized bounded next tasks

1. **P0 language runtime probe:** execute the eight fixtures above using the inventoried stable/experimental binaries; author exact proposed edits only after results.
2. **P0 trading consistency and completion:** make the existing chapter honestly teach catalog/UI/RPC validation plus pre-mutation refusal, then deliver the still-missing functional transaction fixture with a state machine and fault matrix; wording repair alone does not satisfy coverage.
3. **P0 PBO integration:** receive the separate worker's deep PBO evidence, then build one three-PBO client/server fixture and reconcile dependency/prefix/signing/deployment prose.
4. **P0 entity persistence chapter:** implement and test versioned `OnStoreSave`/`OnStoreLoad` with corrupt/truncated/upgrade cases.
5. **P1 hardened RPC example:** implement request IDs, duplicate suppression, bounds, rate control, response correlation, timeout/disconnect cleanup, and two-client abuse tests.
6. **P1 version/provenance chapter:** teach script-diff pinning, local-extraction comparison, versioned claims, and migration review.
7. **P1 CE terrain and diagnostics lab:** cover map prototypes/positions/clusters/area flags and preserve actual Diag outputs.
8. **P1 operator hardening and recovery:** correct credentials/vanilla-admin claims; add least privilege, listener/firewall, secret rotation, log/dump retention, update rollback, and restore drill.
9. **P1 tutorial fixture wave:** materialize tutorials 01, 03, 04, 08, 09, 10, 11, and 12 as exact files, then compile/package/run them in increasing risk order.
10. **P1 supplied-corpus crosswalk:** inventory and compare the newly enumerated local documentation/specification corpus against EN, classifying implemented behavior separately from proposals and independently validating any promoted claim; prioritize limits, version migration, and currency-bridge contracts.
11. **P2 optional breadth review:** only after reliability work, assess MVC/animation helpers, accessibility/keyboard navigation, terrain creation, weapon/firearm authoring, REST/backend integration, database adapters, and CI automation as candidate topics. Their absence is not currently classified as a defect.

Each author delivery should name the page, current claim/gap, proposed text/example, exact source locations, tool/runtime evidence, and remaining limitations. An independent council must reopen the sources and the final delivered files; agreeing with an author's summary is insufficient.

## Sufficient-coverage criteria

The EN wiki is sufficiently covered for its stated audience when all of the following are true; this is a bounded release gate, not a claim of universal completeness:

1. Every existing domain has an explicit capability map, prerequisites, supported build/source provenance, and links to adjacent workflows.
2. Every hard limit or native behavior is sourced to current official documentation/declarations or measured with a versioned reproducible fixture; recommendations and community practice are labeled separately.
3. All eight unresolved language leads have a disposition based on compiler/runtime evidence or conservative wording that preserves uncertainty.
4. Multi-PBO, dependency, client/server, build, signing, deployment, update, and rollback are demonstrated in one packed, inspected, booted fixture.
5. Consequential RPC, permissions, persistence, CE, and transaction examples include malformed input, authorization, replay, disconnect, restart, partial-failure, and recovery checks appropriate to their risk.
6. Entity persistence migration and CE terrain/diagnostic workflows are covered, not merely named.
7. Every tutorial states dependencies, placement, execution context, expected result, error path, and validation level; “complete,” “production-ready,” and “tested” appear only with fresh recorded proof.
8. Operator guidance includes credential separation, least privilege, network exposure, observability, clean shutdown, verified backups/restores, update rollback, and build/mod compatibility.
9. The supplied local corpus has a source-classified crosswalk to EN; planned contracts and beta behavior are never described as shipped engine/mod behavior without independent evidence.
10. Current EN links/anchors and the VitePress build pass after integration; rendered pages and generated graph/artifacts are refreshed and reviewed.
11. Remaining unknowns and candidate topics stay visible. No reading count, clean build, worker completion, or absence of new findings is treated as proof of perfect correctness.

## Artifact checks

- PowerShell `ConvertFrom-Json -Depth 100` parsed `coverage-map.json` successfully.
- The Markdown and JSON each contain the same 27 unique finding IDs; the JSON contains exactly eight unresolved prior leads and 13 tutorial-readiness records.
- Inventory references resolve to a finding ID, existing page paths resolve except for explicitly proposed optional new pages, and neither artifact contains trailing whitespace.
- No VitePress build was run for this delivery because only `.audit/` artifacts changed. The integrated anchor commit's separate renderer-backed check is reported above; future wiki integration still requires a fresh build.

## Current limitations

- No compiler, game, server, client, asset tool, PBO build, exploit, transaction, performance, backup-restore, Workshop, or CE diagnostic command was executed for this map.
- Direct BIKI bodies were inaccessible (HTTP 403); indexed official text and pinned official repositories were used with that limitation recorded.
- The local extraction and non-wiki documents are snapshots. Missing declarations cannot prove native absence, and local/beta/public mod code is fallible.
- Only the local documents and code paths named in Source use and provenance were opened for this bounded map. The wider corpus is preserved in `user-source-paths.txt` and `user-source-inventory.json` but requires `CORPUS-C01`; inventory status is not review status.
- The separate PBO research and language runtime probes were still in flight. Their accepted final evidence must be merged into this map before an overall closeout; the anchor repair is integrated and independently reviewed.
