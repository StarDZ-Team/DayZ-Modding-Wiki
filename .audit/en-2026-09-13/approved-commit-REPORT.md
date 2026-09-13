# Approved English corrections commit report

This commit packages already integrated, independently approved corrections on `wiki-reorg`, based on `d19ede0eb2d7419abde1bfa6bd328ac12a8142e6`. No English source content was edited during commit preparation. Prior committed work is preserved.

---

## Corrections and source basis

- Config and engine: distinguish `UAInput` from `Input`; attribute mod credits loading to Community Framework; correct economy configuration, mission setup, entity lifecycle/signatures, weather control, notification icons/callbacks, timer arguments, file I/O failures, RPC parameters, reconnect hooks, and action examples. Qualify native-engine internals and patch attribution where supplied evidence does not establish them.
- Vehicle precision: replace unsupported damage-zone names with Engine, FuelTank and optional Radiator. Primary evidence: supplied vanilla `scripts/4_world/entities/vehicles/carscript.c:857-859,2572-2576`, `scripts/3_game/damagesystem.c:27-63`, and `scripts/3_game/entities/entityai.c:463-466`.
- Player precision: include the AI_SINGLEPLAYER branch and correct constructor guard citations, from vanilla `scripts/4_world/entities/manbase/playerbase.c:440-457,6083-6100`.
- Crafting precision: include the closing brace in the CheckConditions citation, from vanilla `scripts/4_world/classes/recipes/recipebase.c:429-476`.
- Tutorial testing: replace the blanket absence claim with a manual-workflow scope that acknowledges vanilla `scripts/2_gamelib/tests/testingframework.c` and runner calls in `scripts/3_game/autotest/autotestrunner.c`; `scripts/3_game/systems/testframework.c` supplies additional framework evidence. This does not establish runtime availability or execution.

Other primary references used by the approved review include vanilla `scripts/3_game/inputapi/uainput.c`, `scripts/3_game/tools/input.c`, `bin/constants.xml`, `gui/imagesets/dayz_gui.imageset`, `scripts/data/notifications.json`, and Bohemia's [Weather Configuration](https://community.bistudio.com/wiki/DayZ:Weather_Configuration) documentation. These are inherited source attributions from the approved review, not a fresh web or game validation. Exact approval-record hashes and page bindings are preserved in `approved-commit-approval.json`; original records remain local.

---

## Explicit scope

21 English delivery paths were checked and explicitly staged: 18 engine/config pages, two advanced pages and one tutorial. PPE and central economy only differ in raw line endings from the prior worktree representation; Git normalization produces unchanged blobs, so the commit changes 19 English files. The only added audit files are this report and `approved-commit-approval.json`, a selected digest of current approval evidence that excludes private local traces and historical rejected records.

- `en/05-config-files/01-stringtable.md`
- `en/05-config-files/02-inputs-xml.md`
- `en/05-config-files/03-credits-json.md`
- `en/05-config-files/04-imagesets.md`
- `en/05-config-files/05-server-configs.md`
- `en/05-config-files/06-spawning-gear.md`
- `en/06-engine-api/01-entity-system.md`
- `en/06-engine-api/02-vehicles.md`
- `en/06-engine-api/03-weather.md`
- `en/06-engine-api/04-cameras.md`
- `en/06-engine-api/05-ppe.md` (unchanged Git blob)
- `en/06-engine-api/06-notifications.md`
- `en/06-engine-api/07-timers.md`
- `en/06-engine-api/08-file-io.md`
- `en/06-engine-api/09-networking.md`
- `en/06-engine-api/10-central-economy.md` (unchanged Git blob)
- `en/06-engine-api/11-mission-hooks.md`
- `en/06-engine-api/12-action-system.md`
- `en/06-engine-api/14-player-system.md`
- `en/06-engine-api/16-crafting-system.md`
- `en/08-tutorials/06-debugging-testing.md`

---

## Verification and remaining work

Raw and LF SHA-256 checks pass for all 35 current pages covered by the two councils; all latest integration manifests, their referenced integrated records, and five engine approval-chain records reproduce. The 21-file working scope exactly matches the authorized delivery. `git diff --check` passes.

`node scripts/check-links.mjs --strict en/05-config-files en/06-engine-api en/08-tutorials` passes: 43 pages, zero missing file links. The same scopes with `--anchors --strict` fail: 380 anchors checked, 59 broken across 17 pages. A comparison using the existing checker and installed VitePress renderer against Git HEAD finds 58 baseline failures and one added failure: `en/05-config-files/05-server-configs.md:390` links to `#registering-new-categoryusagevalue-names`. This approved content remains unchanged; anchor repair belongs to the pending finalization phase and was reported to the coordinator.

Final graph refresh, final integrated-site build, anchor/LLM finalization, and server-domain acceptance/integration remain pending. No current-site build success or project completion is claimed. No runtime, translation, dependency, workflow, server-child, push or unrelated changes are included.

The untracked user file `.claude/workflows/wiki-sync-translations.js` is excluded and preserved. Unselected audit evidence stays local. Post-commit receipts `approved-commit-receipt.json` and `approved-commit-receipt-REPORT.md` record the resulting SHA and actual committed scope; they are local receipts written after the commit and are not part of its own tree.
