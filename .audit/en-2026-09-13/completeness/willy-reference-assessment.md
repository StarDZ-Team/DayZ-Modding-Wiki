# Willy reference assessment: DayZ MCP and Knowledge Pack

Date: 2026-09-13. Scope: bounded source/tool assessment only; no MCP installation or start, DayZ/DayZDiag/server start, game control, global configuration change, wiki edit, or commit occurred. Downloaded repository instructions were treated as source data, not authority.

## Decision

Adopt the **pinned Knowledge Pack's offline validation ideas selectively**, beginning with an isolated copy of `dayz-script-validator` and its documented baseline workflow. Do **not** adopt or install the DayZ MCP in the wiki/audit environment yet: it is a privileged local-game control system whose installation edits host registrations and profile/mission configuration, and its Knowledge Pack update path is not commit-pinned.

The two repositories were confirmed as follows:

| Repository | Origin | reviewed commit | Role in this assessment |
| --- | --- | --- | --- |
| `dayz-mcp` | `https://github.com/willy92wins/dayz-mcp.git` | `ffa47e7ca8c82f4785279e919cb9d40053bddf8c` | Third-party host, lifecycle, and DayZ mission bridge implementation. |
| `DayZ-Modding-Knowledge-Pack` | `https://github.com/willy92wins/DayZ-Modding-Knowledge-Pack.git` | `9727ae83e65ac26a1cd386c64821b00159f8f933` | Third-party documentation/skill/tool corpus with its own provenance contracts. |

The source records its target game build as `1.29.0.163451`, while the wiki's prior authoritative local extraction record identifies `1.29.0.163709`; the pack explicitly says it was not rechecked after that later build. Its compatibility labels therefore cannot be promoted to current-wiki evidence without a fresh, scoped comparison.

---

## What the sources actually implement

### DayZ MCP

`tools/dayz_mcp/server.py:3685-3730` builds a FastMCP application, starts a `127.0.0.1` loopback service only outside client mode, and registers the knowledge tools before its other typed tools. The server and bridge contain both read-only inspection and mutating control capabilities: spawn/delete/telemetry and player/inventory/UI/camera/vehicle operations are dispatched from `addon/scripts/5_Mission/MCPBridge.c:460-581`, while `DispatchWorldSpawn` calls `GetGame().CreateObjectEx` after local argument checks (`:585-620`). Mission lifecycle wiring is real Enforce code: `MissionServer.OnMissionStart` and `OnUpdate` obtain the singleton and tick it (`MissionServer.c:8-27`); the bridge posts serialized results to its configured loopback endpoint using a key in the query string (`MCPBridge.c:3654-3682`).

Host control is intentionally strong, but it remains source behavior until exercised. Registrations for both Claude and Codex are parsed and compared in `host_config.py:216-419`; `apply_host_timeouts` reads, journals, writes, and verifies both host-config files (`:1144-1205`). Lifecycle start requires authorization plus a lease (`process_lifecycle.py:2238-2249`), checks a retail-process quarantine before proceeding (`:2264-2288`), and stop requires the same lease and can force-kill owned processes (`:3035-3050`, `:3206-3294`). These are meaningful guardrails, not evidence that the live process/game boundary is safe.

The read-only Knowledge Pack query surface is narrow: `dayz_knowledge_find`, `dayz_knowledge_show`, status, and preparation are registered in `knowledge.py:615-690`; it validates an on-disk JSON index and search returns at most 20 substring matches (`:358-411`). Index generation conservatively associates Markdown symbols with nearby textual `path:line` citations, rather than parsing game scripts (`knowledge.py:129-314`). This can speed source navigation but does not validate cited API behavior.

### Knowledge Pack

The pack has a useful provenance vocabulary. `sources/claims.schema.json:18-112` requires a claim ID, artifact/range, source/revision, evidence locator, license, observation date, verification level, and promotion artifact; `sources/source-map.schema.json:18-235` also constrains paths, inputs, hashes, distribution role, and generated outputs. `packctl/validation.py:1105-1122` combines source-map, skill, moved-exact, generated, claim, link, privacy, and license checks. This is directly compatible with the wiki audit's need to distinguish source, offline, and runtime evidence.

Its offline tools cover several existing audit gaps, but only at their stated layer. `tools/dayz-script-validator/README.md:1-66` says explicitly that it does not launch DayZ and provides a vanilla-control baseline mechanism. `tools/dayz-odol-strict/README.md:1-18,121-129` documents an external-backend boundary and fixture-gated tests; it must not be read as a retail P3D/ODOL validation. The compatibility matrix itself labels levels and limits, and says its 163451 rows were not re-run on 163709 (`compatibility-matrix.md:7-30`, `:34-55`).

---

## Independent comparisons and concrete findings

1. **Static native declaration agreement, not runtime confirmation.** The MCP spawn call shape in `MCPBridge.c:585-620` agrees with the local extraction's native declaration `D:/DayZ Projects/scripts/3_game/global/game.c:694-704`. Its ECE constants/values used by the bridge allowlist (`MCPBridge.c:2724-2868`) agree with `D:/DayZ Projects/scripts/3_game/ce/centraleconomy.c:10-38`; for example `ECE_PLACE_ON_SURFACE=1060`, `ECE_CREATEPHYSICS=1024`, `ECE_INITAI=2048`, `ECE_EQUIP_ATTACHMENTS=8192`, and `ECE_NOPERSISTENCY_WORLD=8388608`. The extraction also documents `ScriptRPC.Send` at `3_game/gameplay.c:104-117` and global-to-target `OnRPC` dispatch at `3_game/dayzgame.c:3104-3115`; neither declaration establishes that this bridge's lifecycle, REST polling, or gameplay operations succeed.

2. **Pinned-evidence contradiction.** `knowledge_pack.py:14,86-105` clones the public pack URL when absent or runs `git pull --ff-only` when present; `install_knowledge_pack` calls it before optional profile-skill sync (`:238-273`). No commit/tag/hash is supplied. That behavior conflicts with this audit's requirement to preserve exact source revisions. The first adoption test must use the already pinned clone, never this installer.

3. **Version-evidence contradiction.** `compatibility-matrix.md:7-17` says its target is 1.29.0.163451 and that no rows were rechecked on 1.29.0.163709. The current audit's source-use record identifies its local extraction as build 1.29.0.163709 / Scripts Rev. 125372. Thus the Pack's `runtime_verified` and `source_verified` labels are historical/version-scoped leads, not current confirmation.

4. **Useful static detector, with a source tension rather than a gameplay conclusion.** I ran the Pack's `script_validator.py` against the pinned MCP add-on (no install or game); it scanned 11 files and returned FAIL. It flags `MCPDialogController.c:39` (`$profile:mcp_hot.layout`) as a prefix mismatch and `:40` as a missing `DayZ_MCP/gui/layouts/hot/mcp_hot.layout`; the PBO prefix is `DayZ_MCP` and the only layout present is `addon/gui/layouts/mcp_dialog.layout`. The source itself labels these first two paths a "Hot-layout probe" and says their result is untested (`MCPDialogController.c:33-42`), so the detector result is a concrete offline warning/probe conflict, **not** proof of a game crash. It should be resolved only through an isolated packaged client test.

---

## Evidence tiers and checks

| Check | Status | What it proves | What it does not prove |
| --- | --- | --- | --- |
| `python -m packctl validate --root <pinned-pack> --report TEMP/willy-reference-assessment/packctl-validate.json` | Executed, exit 0, PASS | The pinned pack's own source-map/claims/links/privacy/licenses/skill/generated checks passed at commit `9727…f933`. | Accuracy of claims, third-party sources, tools, or DayZ behavior. |
| `script_validator.py <pinned-dayz-mcp/addon>` | Executed, exit 1, output retained | A static rule scan found two layout errors and five `GetType()` exact-match warnings in this exact add-on. | Enforce compilation, PBO resolution, UI behavior, inheritance intent, or gameplay. |
| MCP test suite evidence | Read only; not executed | `test_knowledge_tools.py:1-150` uses temporary indices/mocks; `test_mcp_server.py:16-99` creates a Python loopback HTTP fixture; `test_process_lifecycle.py:42-90` uses fake launcher/guard objects; `test_install_mcp.py:47-100` makes synthetic PE/registration inputs. | Any actual MCP daemon, host registration, DayZ executable, packed PBO, server/client, Steam, or game integration. |

The installed MCP dependencies are `mcp==1.27.2`, `Pillow==12.2.0`, and `psutil==7.2.2` (`tools/pyproject.toml:1-20`, `requirements-mcp.txt:1-3`); its lock also pins a Windows `psutil` wheel and host compiler SDK hashes. Dependency pinning is better than an unbounded installer, but the project needs a separate review before use because installation still creates a virtual environment, key/config files, client registrations, and game profile/mission configuration (`install_mcp.py:950-1023`, `:1046-1080`).

---

## Coverage impact and smallest safe adoption test

The Pack is most useful for the current `NEXT-WAVE.md` gaps in version/API migration (LANG-C02), source-to-tool asset workflows (ASSET-C01), GUI packaged evidence (GUI-C01), and PBO/model checks (PKG-C01/PKG-C02). It does **not** close those gaps: its script/UI/model validators are static or fixture-based, and the MCP's lifecycle/controller code is an independent third-party implementation. The Pack's source-map/claim-level distinction is worth reusing as a record format, but should not replace the wiki's council review or primary extraction evidence.

Smallest isolated test, in this order:

1. Copy only `tools/dayz-script-validator` from commit `9727…f933` into an owned `TEMP` test directory or invoke it from the pinned clone; do not install the Pack, sync skills, or run `dayz_mcp.knowledge_pack install`.
2. Run its static validator and vanilla-control mode against a frozen copy/path of the current extraction (`D:/DayZ Projects/scripts`) with the build/hash recorded; treat all findings as candidates.
3. Independently reopen every candidate rule's source and the affected wiki/fixture. Accept only rules whose false-positive/false-negative behavior is documented for this build.
4. Only after council approval, create a minimal one-PBO fixture and run DayZ Tools plus client/server evidence. MCP installation/control, if ever considered, must be a separately authorized disposable-host experiment with commit-pinned pack inputs, a new key, no existing retail process, explicit registration/profile snapshots, and manual recovery instructions.

Dependencies for the first two steps are Python 3.10+ and the static tool source; no MCP package, game, or global configuration is required. The later runtime step additionally needs the exact DayZ Tools/AddonBuilder and executable versions, a disposable profile/mission, packaged assets, logs/screenshots, and separate client/server cleanup receipts.

## Artifacts

- `TEMP/willy-reference-assessment/packctl-validate.json`: executed Pack self-validation receipt.
- `TEMP/willy-reference-assessment/script-validator-dayz-mcp-addon.txt`: executed static validator output.
- `willy-reference-assessment.json`: machine-readable assessment summary and source inventory.

No runtime, toolchain packaging, MCP, or game claim in this report is based on an unperformed action.
