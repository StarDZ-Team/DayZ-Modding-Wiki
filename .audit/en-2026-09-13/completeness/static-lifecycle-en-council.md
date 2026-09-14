# Static Lifecycle EN Final Council

Reviewed 2026-09-14 against repository HEAD `5063a81ffe75ab7a44f5dec4bf6c7fc3ac51109f` and the complete uncommitted diff for `en/07-patterns/01-singletons.md` and `en/07-patterns/02-module-systems.md`. This council performed no EN edit, build, install, test, launch, staging action, or commit; its only writes are this report and its JSON companion.

## Verdict

**Changes required before acceptance.** The implementation accurately carries the retained two-field observation and its important limitations into the edited lifecycle passages and both cleanup table rows. However, the singleton page still contains the explicitly targeted blanket statement that static fields live for the process, and the next paragraph adds cleanup/performance absolutes (`the only thing` and `costs nothing`) that the evidence does not establish.

## Evidence reopened

The council reopened the exact retained probe sources, runtime log, process receipt, investigation report, and prior independent council named by `static-lifecycle-en-implementation.json`, then verified their SHA-256 values against that receipt.

- `4_World/world_state.c` initializes `SMI_WorldState.s_Count` to `200`.
- `5_Mission/lifecycle.c` initializes `SMI_MissionState.s_Count` to `100`; each `MissionServer.OnInit()` increments and logs both fields; its scheduled mission-owned callback directly calls `GetGame().RestartMission()` after writing a one-shot marker.
- The retained log records first `MISSION_STATIC=101 WORLD_STATIC=201`, the direct restart call, `OnMissionFinish`, destruction and Mission-module reload, then second `MISSION_STATIC=101 WORLD_STATIC=202` in the same run. It contains neither `SMI:RESTART_MISSION:RETURN` nor `SMI:SECOND_LIFECYCLE:REQUEST_EXIT`.
- `lifecycle.process.json` identifies PID `33556` and records exit code `-1073741819`, which is `0xC0000005`.

This supports only the observed Mission `101 -> 101` reinitialization and World `201 -> 202` persistence for those two fields during that failed direct-restart probe. It does not demonstrate a healthy restart, client reconnect behavior, authenticated administrator `#restart`, a general process-lifetime rule, game-layer behavior, or a native guarantee.

## Findings and dispositions

### Accepted

1. **A1 — Bounded direct-restart observation.** The new paragraphs at `01-singletons.md:157` and `:463` accurately identify DayZDiag `1.29.0.163709`, PID `33556`, the direct scheduled `GetGame().RestartMission()` call, Mission `101 -> 101`, World `201 -> 202`, Mission-module reload, missing return/clean-exit markers, and the later access-violation exit.
2. **A2 — Required limitations retained.** Those paragraphs expressly deny a healthy-restart result and deny generalization to other fields, administrator `#restart`, client reconnects, and game-layer state.
3. **A3 — Cleanup table rows remain defensive.** The edited rows at `01-singletons.md:587` and `02-module-systems.md:712` say mutable state *may* outlive the expected lifecycle, scope the observation to one failed direct-restart probe, and keep the behavior beyond the tested fields unverified. The fixes recommend defensive cleanup without asserting persistence as a universal rule.

### Rejected pending correction

1. **R1 — Requested blanket sentence was not repaired.** `01-singletons.md:155` still says: `static fields -- which live as long as the process -- survive that transition.` This conflicts with the retained observation that the tested Mission-module static reinitialized while the process continued, and it overstates the evidence for all static fields.

   Replace the final two sentences of that paragraph with exactly:

   > A client therefore moves between the main-menu mission and a gameplay mission without relaunching. That transition creates a cleanup boundary for static references: do not assume a static field resets or persists without evidence for its script module and transition. Stale `s_Instance` values, dead objects and orphaned callbacks are therefore lifecycle risks.

2. **R2 — Cleanup and performance absolutes are unsupported.** `01-singletons.md:157` says cleanup is `the only thing that saves you` and `costs nothing`. Other cleanup designs can exist, and no performance or side-effect measurement establishes zero cost.

   Replace the final sentence of that paragraph with exactly:

   > Wiring `DestroyInstance()` into `OnMissionFinish` remains a defensive cleanup step: it releases owned references when the field survives the transition and makes shutdown ownership explicit even when a later process exit clears static state.

### Unresolved evidence boundaries

1. **U1 — Healthy restart remains unverified.** The process failed before the restart call returned or the planned clean exit ran.
2. **U2 — Other lifecycle paths remain unverified.** No client reconnect, authenticated administrator `#restart`, separate-process restart, or production server lifecycle was tested by this retained probe.
3. **U3 — Broader static behavior remains unverified.** No inference is supported for untested fields or script modules, including game-layer fields, and the retained result is not a native guarantee.

These unresolved items do not require new experiments for this narrow documentation repair; they require the limitations to remain explicit.

## Machine-generated fingerprints

| Artifact | SHA-256 |
|---|---|
| `.audit/en-2026-09-13/completeness/static-lifecycle-en-implementation.json` | `0E7AA690F14836CDCE37026134647D5FD44DC900E2F9AA483D6AB4F18F1AC5F7` |
| `.audit/en-2026-09-13/completeness/server-mission-investigation.md` | `71F0DC51C1D094951FC4AEBF736B1B49D7D3098849E1E1BE16282EB89BE18269` |
| `.audit/en-2026-09-13/completeness/server-mission-investigation.json` | `241F2EC02B1E4689654EB65E9C98AF5B726B740DF041E720861B2503E1CE3A05` |
| `.audit/en-2026-09-13/completeness/server-mission-council.md` | `B38247EE24ED756153BBA093D97DB00D09D39F2A4F775A6141272AE51CCCD0CE` |
| `.audit/en-2026-09-13/completeness/server-mission-council.json` | `82E108E0308052D547A25E2F822C4A0902FC9F4F579B5D5FA45E2701891CF5E8` |
| `TEMP/server-mission-investigation/profiles/lifecycle/script_2026-09-13_22-00-34.log` | `6A285E1FF7ED2AF3A16E5E4F3F1E1798B3BA50FBBC15D08F077016E4ECD5E427` |
| `TEMP/server-mission-investigation/source/lifecycle/Scripts/4_World/world_state.c` | `F489A4D7E07F74E420B028AEF1A8EC9E799AA43761705297C56D34171F6636F7` |
| `TEMP/server-mission-investigation/source/lifecycle/Scripts/5_Mission/lifecycle.c` | `69C2A3AAB8811989B6DAB0465CF435CE9EF19C14066E1423504AA376C3C27732` |
| `TEMP/server-mission-investigation/lifecycle.process.json` | `A69F57F7D1C4C1C4E2CB9BB1763FE4348145B16582818A0DB348CD9CFC9FC8F6` |
| `en/07-patterns/01-singletons.md` | `13034647C9A6094391A8E69568378EB9175302639DA6EE0C4A895CAA90BCAC3C` |
| `en/07-patterns/02-module-systems.md` | `B7A2DA10B1924E80876F957BF9E92EE75C42D9D123B013A3558DB3CBB55D3DDF` |

The Git object ID generated from the reviewed two-file textual diff is `210f4c5fa149138a4cf355a7d40f285d01081e29` (repository object format SHA-1). The EN file hashes match the implementation receipt, so this verdict applies to the exact delivered files reviewed here.
