# Critical Coverage Findings — Independent Council Review

> **Scope:** `OPS-C01`, `OPS-C02`, `TUT-C01`, `TUT-C02`, `LANG-C03`, and `RPC-C02` only. This review was performed against repository revision `9dc36064459f3184404bdba4db9d95b843b6fcaa` on 2026-09-13. It makes no claim about the other coverage findings or the full 110-document corpus.

## Council Boundary

This council reopened the current English pages, the original completeness coverage entries, relevant official/extracted sources, pinned public-mod implementations, and substantive portions of the six user-supplied documents named in the dispatch. Prior audit acceptance and third-party popularity were not treated as authority. No server, client, compiler, packer, signer, or gameplay runtime was launched because runtime testing belongs to another worker; all behavior described as untested below remains untested.

Decision terms:

- **Approve** means the proposed bounded correction is supported by the reopened evidence.
- **Reject** means the current English claim is contradicted by, or materially exceeds, the reopened evidence.
- **Unresolved** means source inspection alone cannot satisfy the stated functional or runtime requirement.

The original observations were reopened in `.audit/en-2026-09-13/completeness/coverage-map.json:138,226,303-314,358-369`, SHA-256 `DDC94407289256CD8365B34784E5DEB5D7787A58A398FC3BDCA814E4277394DB`. The affected current page inputs at revision `9dc36064459f3184404bdba4db9d95b843b6fcaa` were:

| Page | SHA-256 |
|---|---|
| `en/09-server-admin/09-access-control.md` | `EA194B15CCEE5C095343DD9E635268A3396F0BA427841732218012B4627D7402` |
| `en/08-tutorials/12-trading-system.md` | `3461153FAFC68F8430D23A39274D097BAF26C52F6302B0BC65E3B95F3585D961` |
| `en/08-tutorials/09-professional-template.md` | `D6CEFE1BC942F9716A18221E059437207CADC8BF56E48281DD2A89A85EB707FB` |
| `en/01-enforce-script/09-casting-reflection.md` | `9B2015D2006504A4389407EBFFDA5DBE2F626D4CE60EB8F8C9B9912B57F40430` |
| `en/07-patterns/03-rpc-patterns.md` | `84F2CC3731D44BD07DB409FC999A2E09275128405B3E39E258F93F6E7ADC9688` |

## Decision Summary

| Finding | Current claim | Current claim | Proposed correction | Functional completion |
|---|---|---:|---:|---:|
| `OPS-C01` | `passwordAdmin` is also the BattlEye RCon password | **Reject** | **Approve** | **Unresolved** — exercise both login paths and inspect credential-related logs |
| `OPS-C02` | `#login` unlocks a built-in vanilla player/SteamID, kick/ban, teleport/map, and free-camera toolset | **Reject** | **Approve** | **Unresolved** — capture a retail client/server administration inventory |
| `TUT-C01` | the chapter builds a complete, working buy/sell transaction system | **Reject** | **Approve** | **Unresolved** — implement and failure-test an actual transaction fixture |
| `TUT-C02` | every template file is production-ready, copy-paste-ready, and complete | **Reject** | **Approve** | **Unresolved** — materialize and validate a renamed fixture end to end |
| `LANG-C03` | the TOC calls `IsKindOf` “String-Based Type Checking” | **Reject** | **Approve** | **Approve after edit** — static label/anchor verification is sufficient |
| `RPC-C02` | DayZ has a practical per-RPC ceiling/limit | **Reject** | **Approve** | **Unresolved** — measure explicitly scoped payload behavior |

The exact implementation surfaces below are suitable for a bounded Terra edit. Line numbers identify the current revision and will move after edits.

---

## OPS-C01 — Separate `passwordAdmin` from BattlEye `RConPassword`

### Decision

- Current claim: **reject**.
- Immediate correction: **approve**.
- Finding completion: **unresolved** until both administration paths and their log behavior are exercised in a disposable server setup.

### Affected text and reason

At `en/09-server-admin/09-access-control.md:33-38`, the page says the `serverDZ.cfg` value `passwordAdmin` is used both for in-game login and for a BattlEye RCon client. That conflates two separately documented settings. The saved Bohemia server-configuration page describes `passwordAdmin` as the password “to become a server admin” and separately places `RConPassword` in the BattlEye server configuration. BattlEye's own documentation requires `RConPassword` for RCon.

The page already shows `RConPassword` correctly at lines 115-122, so the present page contradicts itself. The official static sources establish separation, but this council did not independently execute the `#login` command, connect an RCon client, or inspect fresh server/BattlEye/RCon logs for secret exposure.

### Exact replacement English

Replace `en/09-server-admin/09-access-control.md:33-38` with:

```markdown
Bohemia documents `passwordAdmin` as the password used to become an in-game server administrator. It is not the BattlEye RCon credential:

1. **In-game administration** — use `#login <password>` with the `passwordAdmin` value. The command path still needs a disposable-server runtime check.
2. **BattlEye RCon** — configure a separate `RConPassword` in the BattlEye server configuration described below.

Keep the two secrets distinct and restrict both configuration files to the server service account. Store the in-game secret in the file passed with `-config`; store the RCon secret in the BattlEye configuration resolved by `-BEpath` and `-profiles`. This static review did not determine whether successful or failed credentials are echoed to any log, so inspect fresh server, admin, BattlEye, and RCon logs during the required runtime test before making a logging-safety claim.
```

### Evidence

- Bohemia saved server configuration, `D:\StarDZ\docs\DayZ\Server Configuration.md:19,150-175`, SHA-256 `D7126F849E9A460887A3B640068CA8C88304324EDFD3AFA1526AE69E4BECAA8E`, distinguishes `passwordAdmin`, BattlEye configuration, `RConPassword`, `-profiles`, and BattlEye path handling.
- BattlEye documentation, <https://www.battleye.com/support/documentation/>, accessed 2026-09-13, downloaded HTML lines 115-120, SHA-256 `3C971A531EC63E87F35D443DFC43363ABA1893D6E326538FE273E09DEB1865D3`, states that `RConPassword` is required for RCon while `RConPort` is required and `RConIP` optional.
- The live Bohemia Community Wiki request was blocked by Cloudflare with HTTP 403 on 2026-09-13. The saved local snapshot was read and is identified by hash; the live page was not represented as successfully read.

### Still required

Use a disposable server with distinct canary values for `passwordAdmin` and `RConPassword`; verify that each credential authenticates only its intended path. Record server build, command lines, resolved `-config`/`-profiles`/`-BEpath`, client and RCon versions, success/failure results, and whether either canary appears in server, script, admin, BattlEye, or RCon logs.

---

## OPS-C02 — Remove the unsupported vanilla admin-tool inventory

### Decision

- Current claim: **reject**.
- Immediate correction: **approve**.
- Finding completion: **unresolved** until a retail dedicated-server/client capture inventories the actual `#login` command and UI surfaces.

### Affected text and reason

At `en/09-server-admin/09-access-control.md:183-193`, the page attributes a SteamID-bearing player list, kick/ban UI, admin map teleport, and free camera to vanilla `#login`. The reviewed official retail player-list scripts show player names, microphone/mute state, and platform gamercard behavior, not those administrator controls. Bohemia's Diag Menu documentation places teleport and free camera in `DayZDiag_x64.exe`. The extracted developer free-camera and teleport implementation is correspondingly developer/diagnostic code.

Community Online Tools and VPP Admin Tools explicitly implement permissions and modules for map/player views, teleport, kick/ban, spectate, ESP, and free camera. Those repositories demonstrate third-party implementation choices; they do not by themselves prove a feature is absent from retail vanilla. The combined official UI and Diag evidence is sufficient to reject the current blanket attribution, while a retail runtime inventory remains necessary before publishing a complete vanilla feature list.

### Exact replacement English

Replace `en/09-server-admin/09-access-control.md:183-193` with:

```markdown
## Vanilla Administration Boundary

The reviewed official sources do not establish a retail in-game admin panel unlocked by `#login`. The vanilla multiplayer pause menu does synchronize a player list, but the extracted UI uses it for player names, mute state, and platform gamercards; it does not expose the SteamID, kick, or ban controls claimed by the previous version of this page.

Bohemia documents teleport and free camera in the Diag Menu, which is available in `DayZDiag_x64.exe`, not as a `passwordAdmin` feature of the retail client. Use BattlEye RCon for the documented remote-administration path. Admin maps, teleport panels, spectate or free-camera tools, and richer player management are supplied by mods such as Community Online Tools and VPP Admin Tools; document the selected mod and its own permission model rather than calling those features vanilla.

A retail dedicated-server/client capture is still required before this wiki lists any additional vanilla `#login` commands or administrator UI. Keep admin-log configuration separate from claims about an in-game tool panel.
```

Update the TOC entry at `en/09-server-admin/09-access-control.md:20` to:

```markdown
- [Vanilla Administration Boundary](#vanilla-administration-boundary)
```

### Evidence

- Official DayZ Script Diff, repository <https://github.com/BohemiaInteractive/DayZ-Script-Diff>, commit `86974a0f5bd16b1ee3e334ad828133c93dca80a1` (`Build 1.29.163709, Scripts Rev. 125372`), `scripts/5_mission/gui/ingamemenuxbox.c:189-225`, SHA-256 `BDF8060E99ACD2A89C11A97C94CCE66F26717BCFDE69407AE49F20123C24D388`, constructs the ordinary online player panel.
- Same official commit, `scripts/5_mission/gui/ingamemenu_xbox/playerlistentryscriptedwidget.c:18-35`, SHA-256 `EAB836286CBC02181AF92ADE0719DA73187778BE82BB4FA32D928D01F3D24D32`, populates name/avatar/mic/mute behavior, not the asserted SteamID/kick/ban controls.
- Same official commit, `scripts/3_game/client/syncplayer.c:1-12`, SHA-256 `B42FF2DD82D09F3F47ECC8A6C4FB9829D6C9B8798820AA14897BA046B2A6ACB7`, carries the identity used by that player list; the UI evidence above determines what is displayed.
- Official extraction mirror, `D:\DayZ Projects\scripts`, last modified 2026-09-10, was byte-identical for the cited files to the pinned official commit.
- Bohemia saved Diag Menu, `D:\StarDZ\docs\DayZ\Diag Menu.md:1,690-694,801-854`, SHA-256 `58CAD3A5194F0237A99D30C08BE68F60B5B2A531C605817022E50397D14FE616`, limits the documented menu to `DayZDiag_x64.exe` and describes Free Camera plus Insert/Home teleport behavior.
- Official extraction, `scripts/4_world/plugins/pluginbase/plugindeveloper/developerfreecamera.c:1-93`, same pinned official commit, SHA-256 `7862CA2430C97C2353C04E7E89B499145B9E99BB6D25456E1382ACA1B5E98149`, implements the developer free camera. `scripts/4_world/plugins/pluginbase/plugindeveloper.c:61-100`, SHA-256 `18B6DEA92E951A62216AB6070F2A464F5A700C5B183DF58F5853B983F079FBF4`, gates developer RPC dispatch with `DIAG_DEVELOPER`.
- Community Online Tools, <https://github.com/Jacob-Mango/DayZ-CommunityOnlineTools.git>, pinned and then-current commit `41f2c2b99565d0e3970163e162efbf1283fdca62`, `JM/COT/Scripts/5_Mission/CommunityOnlineTools/modules/COTMap/JMMapModule.c:1-40`, SHA-256 `9CE6B779EA5D1848F3A887D3447993205A74616C08D8F74B079E477B41313536`, declares admin map/player-view/teleport permissions.
- Same COT commit, `JM/COT/Scripts/5_Mission/CommunityOnlineTools/modules/Player/JMPlayerModule.c:1-40`, SHA-256 `A40D2E6626B55C2E2CF069C210D44AB21208DFFF371C54E4EFA267D97E1AC5ED`, declares spectate, kick, ban, and teleport permissions.
- VPP Admin Tools, <https://github.com/VanillaPlusPlus/VPP-Admin-Tools.git>, reviewed pinned commit `dc22e420df3b54e821055f9764da1e48f4a31e71` (remote `master`/HEAD was `646fd89d38d6c7b4eb4da1a31cb69f271b2396c8` on 2026-09-13), `4_World/VPPAdminTools/Plugins/PluginManager.c:19-44`, SHA-256 `0C1E74E4595A1B05E98A653F501DF03E3D4A377735010CC56308CF23D632592A`, registers mod-specific player, teleport, ESP, and spectate managers; `4_World/VPPAdminTools/Plugins/PluginBase/TeleportManager/TeleportManager.c:267-317`, SHA-256 `A042E545E75871795374F3EFBCB99D5164DF23E9BA0C0A4873FE5C4A905EBCB4`, performs permission-checked teleport/map updates; `5_Mission/VPPAdminTools/Freecamera.c:1-25`, SHA-256 `58BE976F775AEED2F9642EB175799B04A792A6843DDCA0BB57EDB4988121D28A`, is a mod-specific free-camera helper.

### Still required

On a matching retail client and dedicated server, record the pre-login and post-login chat commands, menus, keybinds, player-list fields, privilege checks, and relevant server/admin logs. Test without admin mods loaded. Absence from an extracted script search is not alone proof of native absence, so retain this runtime requirement even after the prose correction.

---

## TUT-C01 — Describe the trading chapter as a safe-refusal prototype

### Decision

- Current claim: **reject**.
- Immediate correction: **approve**.
- Finding completion: **unresolved**. Downgrading prose does not satisfy the functional trading-example requirement.

### Affected text and reason

`en/08-tutorials/12-trading-system.md:1,6,28-61` promises a complete trading system and diagrams successful debit/spawn transactions. The actual handlers at lines 326 and 344 deliberately return failure before mutation, and line 412 correctly says no atomic or runtime-proven compensation protocol is demonstrated. The promises and diagrams are therefore false descriptions of the delivered example.

The official inventory APIs show that creation can return null and expose no transaction guarantee. The StarDZ currency-bridge contract and beta recovery code contain useful transaction/idempotency/compensation design leads, but the contract says its Enforce integration is still under construction and the recovery code has documented loss paths. They cannot validate this tutorial as a complete transaction implementation.

### Exact replacement English

At `en/08-tutorials/12-trading-system.md:1`, replace the H1 with:

```markdown
# Shop UI, Catalog RPC, and Safe Refusal
```

At line 6, replace the summary with:

```markdown
> **Summary:** Build a non-transactional shop prototype with JSON catalog data, a categorized UI, server-owned validation, and buy/sell requests that intentionally refuse before inventory or currency changes. This chapter teaches the request/response boundary; it does not implement a working trading transaction.
```

Replace `en/08-tutorials/12-trading-system.md:28-61` with:

~~~~markdown
## What We Are Building

Players press F6 to open a shop menu and browse server-supplied categories and items. Buy and sell requests bind to the authenticated sender, validate quantity and the server catalog, and then return a disabled result without changing inventory or currency. The refusal is intentional: this chapter does not provide the persistence, idempotency, compensation, and failure handling required for a working trading system.

```mermaid
sequenceDiagram
    participant P as Player (Client)
    participant UI as ShopMenu
    participant S as ShopManager (Server)

    P->>UI: Open shop
    UI->>S: RequestShopData
    S-->>UI: ShopDataResponse(categories, items)
    P->>UI: Click Buy or Sell
    UI->>S: Request(className, quantity)
    S->>S: Bind sender; validate quantity and catalog
    S->>S: Refuse before mutation
    S-->>UI: TransactionResult(false, reason, unchanged balance)
```

```text
CLIENT                                SERVER
1. Press F6 -> REQUEST_SHOP_DATA ->   2. Load catalog and count currency
                                          SHOP_DATA_RESPONSE ->
3. Show categories and items
   Click Buy/Sell -> REQUEST ------>  4. Bind sender, validate, refuse
                                          TRANSACTION_RESULT(false) ->
5. Show disabled result; balance and inventory remain unchanged
```

**Key rule:** The client sends `(className, quantity)` only. The server looks up the catalog entry, but the provided handlers never debit, credit, spawn, or delete items.
~~~~

Apply the following navigation-label changes without changing the route:

- `.vitepress/config.mts:137`: `Shop UI & Safe Refusal`
- `README.md:57`: replace the final `Trading System` with `Shop UI & Safe Refusal`
- `en/README.md:145` and `en/index.md:144`: `Shop UI, Catalog RPC, and Safe Refusal`
- `en/glossary.md:1126`: `Shop UI and Safe Refusal`; line 1129 link label `8.12 Shop UI, Catalog RPC, and Safe Refusal`
- `en/08-tutorials/08-hud-overlay.md:604`: replace “trading-system tutorial ([Trading System]...)” with “shop RPC tutorial ([Shop UI and Safe Refusal]...)”.

Rename the TOC label and section at `en/08-tutorials/12-trading-system.md:23,849` from `Complete Code Reference` to `Provided Code Reference`.

### Evidence

- Current page handlers, `en/08-tutorials/12-trading-system.md:315-352`, explicitly refuse buying and selling; line 412 explicitly says no transaction-safe subsystem is demonstrated. Current file SHA-256: `3461153FAFC68F8430D23A39274D097BAF26C52F6302B0BC65E3B95F3585D961`.
- Official DayZ Script Diff, commit `86974a0f5bd16b1ee3e334ad828133c93dca80a1`, `scripts/3_game/systems/inventory/inventory.c:870-893`, SHA-256 `F83FD3501DF9F99BB9BDEB2AACEE7608E1C15E101DB5A9F099458ABCD7C51C17`, includes creation paths that can return null.
- Same official commit, `scripts/3_game/global/game.c:694-702`, SHA-256 `CF529055C48596108034CE6B11826B09BBF5D93E6C550E37785947873D8C3158`, declares object creation without an inventory/currency transaction guarantee.
- Same official commit, `scripts/3_game/entities/entityai.c:786-810`, SHA-256 `AD08181C307BE03549ABC8AFD6A6CEB8532ECA88DA5DA648686CA9FD682A57F5`, exposes safe deletion behavior but no cross-system transaction result.
- `D:\StarDZ\docs\STARDZ_CURRENCY_BRIDGE_CONTRACT.md:1-124`, SHA-256 `2CCF77EDC3DC6F0E3CD3FD8AC7B3CBDB8A85EBCCB845C88223958AA15DA2EEE9`, was read for status, debit-first risk, reference IDs, outcomes/timeouts, idempotency, sequence, and missing Enforce boot. Its own lines 3-4 say the Enforce integration is under construction and production remains blocked.
- `D:\StarDZ\StarDZ_Market_Hub\StarDZ_MarketHub_Server\Scripts\4_World\Models\MHSerializedItem.c:80-180`, SHA-256 `9A3EDA11E88A8E28CAA5FCD76873747D12788EB1A2F750BEBFF2E7D2E9555CB4`, and `D:\StarDZ\StarDZ_Market_Hub\StarDZ_MarketHub_Server\Scripts\4_World\Systems\MHItemRecovery.c:1-50,120-260`, SHA-256 `CE2C824C75E94AF3A0B41CC0FCD05E6A3FC8144EC3966952D115BFD544BFC015`, were inspected as beta recovery/escrow leads. They include null/failure paths and do not constitute a validated transaction fixture.

### Still required functional fixture

Implement a server-owned transaction state machine with durable identity/reference IDs, server-owned catalog and prices, reservation or durable compensation, idempotency across duplicate/replayed requests and restart, and disconnect recovery. Exercise at least two clients against a dedicated server and inject malformed/truncated payloads, invalid quantities/classes, spoofed targets, unauthorized/replayed/duplicate requests, debit failure, create/spawn failure, persistence failure, disconnect, and restart at each transition. Record starting and ending balances/inventories plus durable state and logs for every case. Until that artifact exists, the wiki may teach safe refusal but must not claim functional trading.

---

## TUT-C02 — Downgrade unvalidated “production-ready” template claims

### Decision

- Current claim: **reject**.
- Immediate correction: **approve**.
- Finding completion: **unresolved**. The complete-template requirement still needs a materialized and runtime-tested fixture.

### Affected text and reason

`en/08-tutorials/09-professional-template.md:6,36-55` says every file is complete, production-ready, copy-paste-ready, leak-free, and provided out of the box. The displayed output tree at lines 83-92 contains a signed PBO, key, and Workshop `meta.cpp`, while the batch script at lines 1484-1563 only invokes Addon Builder and copies `mod.cpp`. It does not compile Enforce Script, sign the PBO, create/copy a `.bikey`, or create `meta.cpp`. Its line 1541 also says a `.c` syntax error prevents packing, whereas the local cookbook correctly cautions that packing does not compile Enforce Script. The verification step at lines 1636-1644 is an instruction to launch and inspect one log tag, not evidence that the supplied files were ever materialized or passed that check.

The user corpus includes additional documents that label their own examples complete, tested, or production-ready. Those self-labels are leads, not independent evidence. No recorded compiler, packer, signing, dedicated-server, client, UI, RPC, configuration-reload, or shutdown fixture was found for this chapter.

### Exact replacement English

Replace `en/08-tutorials/09-professional-template.md:6` with:

```markdown
> **Summary:** This chapter presents an illustrative, feature-rich DayZ mod skeleton with a config system, singleton manager, client-server RPC, UI panel, keybinds, localization, and packing automation. The listings have not been materialized and passed compiler, packer/signing, dedicated-server, or client tests as one fixture; treat them as a starting point, not as production-ready or copy-paste-validated code.
```

At lines 36-49, replace the lead/table claims with:

```markdown
A “Hello World” mod proves only a small part of the toolchain. This illustrative skeleton adds more moving parts:

| Concern | Hello World | Illustrative Template |
|---------|-------------|-----------------------|
| Configuration | Hardcoded values | JSON config load/save/default pattern |
| Communication | Print statements | String-routed RPC example |
| Architecture | One file, one function | Singleton manager and layered lifecycle hooks |
| User interface | None | Layout-driven UI panel example |
| Input binding | None | Custom keybind example |
| Localization | None | `stringtable.csv` entries for 13 languages |
| Build pipeline | Manual Addon Builder | Batch wrapper around Addon Builder |
| Cleanup | None | Cleanup hooks whose runtime behavior remains unverified |

Use this as a candidate starting point after you materialize, rename, inspect, compile, pack, and test it. Delete systems you do not need only after the renamed fixture passes the relevant checks.
```

Change `Complete Directory Structure` at the TOC and heading (`:13,53`) to `Provided Directory Structure`, and replace line 55 with:

```markdown
This is the intended source layout for the listings below. It is not evidence that the files have been assembled and validated as one working fixture.
```

Immediately after the build-script block ending at current line 1563, add:

```markdown
> **Build boundary:** This batch file packs the `Scripts` directory and copies `mod.cpp`. It does not compile Enforce Script, sign the PBO, produce or copy a `.bikey`, or create Workshop `meta.cpp`. The distributable tree shown above therefore requires separate compilation/runtime validation, signing, key-copy, and Workshop-metadata steps. Addon Builder success alone does not prove that the `.c` files compile.
```

Delete the line `echo   - A .c file has a syntax error that prevents packing` from the batch example.

Replace `en/08-tutorials/09-professional-template.md:1636-1644` with:

```markdown
### Step 4: Validate the Renamed Fixture

The following is a required validation checklist, not a record of results:

1. Materialize every listed file and confirm the paths and PBO prefix.
2. Compile the Enforce Script through the intended game/tool workflow and preserve diagnostics.
3. Pack the PBO, inspect its contents and prefix, sign it, and verify the copied public key and Workshop metadata.
4. Boot a dedicated server with the packaged mod and preserve configuration and script logs.
5. Join with a matching client and exercise the keybind, UI open/close, RPC request/response, config creation/reload, disconnect, clean shutdown, and restart.
6. Record the DayZ and DayZ Tools builds, commands, fixture hash, expected results, actual results, and any known limitations.

Until those checks pass, describe the chapter as illustrative and unvalidated.
```

Apply these cross-page wording changes:

- `README.md:77`: `Feature-rich illustrative starter (not runtime-validated)`.
- `en/08-tutorials/05-mod-template.md:57`: replace “full production template” with “feature-rich illustrative template (not runtime-validated)”.
- `en/08-tutorials/05-mod-template.md:67`: replace the paragraph with: `Chapter 8.9 is a feature-rich illustrative skeleton, not a validated production fixture. If you use it as a personal scaffold, first materialize and test the renamed version, then remove systems you do not want while repeating the relevant checks.`
- `en/glossary.md:851`: replace `Copy-paste ready.` with `Illustrative only; the combined fixture has not been runtime-validated.`

### Evidence

- Current template page SHA-256 `D6CEFE1BC942F9716A18221E059437207CADC8BF56E48281DD2A89A85EB707FB`; current lines 83-92 promise output that its lines 1484-1563 do not produce, and lines 1636-1644 contain instructions rather than recorded results.
- `D:\StarDZ\docs\COOKBOOK_RECEITAS_COMPLETAS.md:1-271`, SHA-256 `0D05D8B011933D7E9ADC246CA3180C14A6EC2681F39CC91C655458509DEB9B9A`, was read for its definition of complete examples and its validation loop. Lines 250-254 explicitly distinguish PBO packing from Enforce compilation. Its own “working/verified” labels were not treated as validation of this wiki page.
- `D:\StarDZ\docs\DAYZ_MOD_ARCHITECTURE_PATTERNS.md:1-130,408-605,1792-1913`, SHA-256 `315C4C07A240C46D239984288F903860D46076A34376AC9CEDF5281D57D87B5B`, was read for claimed readiness, lifecycle/RPC patterns, and validation framing. Its self-description as production-ready is not independent runtime evidence.

### Still required functional fixture

Materialize the exact chapter files in an isolated fixture, rename all placeholders, hash the delivery, and run the checklist above. Include negative paths: invalid/missing JSON, incompatible client/server payload version, malformed/truncated RPC, absent UI/layout resource, repeated mission initialization, disconnect during RPC, shutdown/restart, pack/sign/key mistakes, and missing dependencies. A prose downgrade prevents readers from being misled but does not complete the promised full-template example.

---

## LANG-C03 — Correct `IsKindOf` terminology in the TOC

### Decision

- Current TOC label: **reject**.
- Exact correction: **approve**.
- Completion: **approve after the one-line edit and static anchor check**; no runtime behavior changes.

### Affected text and exact replacement

At `en/01-enforce-script/09-casting-reflection.md:14`, replace:

```markdown
- [obj.IsKindOf — String-Based Type Checking](#obj-iskindof-—-config-based-type-checking)
```

with:

```markdown
- [obj.IsKindOf — Config-Based Type Checking](#obj-iskindof-—-config-based-type-checking)
```

The body heading and explanation at lines 201-226 are already the intended terminology. `string` describes the argument representation; the behavior being taught is checking the config-class hierarchy.

### Evidence

- Current page SHA-256 `9B2015D2006504A4389407EBFFDA5DBE2F626D4CE60EB8F8C9B9912B57F40430`; lines 201-226 consistently describe config-class checking.
- Official DayZ Script Diff, commit `86974a0f5bd16b1ee3e334ad828133c93dca80a1`, `scripts/3_game/entities/object.c:513-520`, SHA-256 `EBAC48FF196148AB4722A9D9A81C277796D4EA07896A5CF09742213D32424B4C`, comments `IsKindOf` as checking the config class name and delegates to `g_Game.ObjectIsKindOf(this, type)`.

### Verification

After editing, run the repository's anchor/link check or build and verify that the unchanged `#obj-iskindof-—-config-based-type-checking` target resolves. This is a documentation-label correction, not a gameplay claim.

---

## RPC-C02 — Remove the unmeasured per-RPC ceiling claim

### Decision

- Current ceiling/limit claim: **reject**.
- Immediate qualification: **approve**.
- Numeric or behavioral limit: **unresolved** until a build-scoped measurement fixture is run.

### Affected text and reason

`en/07-patterns/03-rpc-patterns.md:825,840` states that DayZ has a practical per-RPC ceiling/limit. The reviewed official `ScriptRPC.Send` declaration documents direction, target, reliable/unreliable delivery, and recipient semantics, but publishes no maximum payload, fragmentation behavior, or failure threshold. Neither the pinned Community Framework RPC manager nor the inspected local RPC/security references supply an independently measured native ceiling. General advice to bound and paginate payloads is sound, but presenting a ceiling as a DayZ fact is not supported.

### Exact replacement English

Replace line 825 with:

```markdown
5. **Keep payloads deliberately bounded.** The reviewed DayZ script declarations do not publish a maximum `ScriptRPC` payload, fragmentation behavior, or drop threshold. Paginate large datasets and treat any size threshold as build- and delivery-mode-specific until you measure it.
```

Replace line 840 with:

```markdown
- **Performance:** Both dispatch work and serialization/payload cost should be measured for the actual mod. Payload failure behavior has not been measured here; paginate large datasets, and report the client/server build plus the `guaranteed` mode with any observed threshold.
```

### Evidence

- Official DayZ Script Diff, commit `86974a0f5bd16b1ee3e334ad828133c93dca80a1`, `scripts/3_game/gameplay.c:104-117`, SHA-256 `AA12624843F51C70200D37449559FDBADB042D333D4EE74C989E0CA632D2F0FE`, documents `ScriptRPC.Send` but no size limit. The corresponding extraction file under `D:\DayZ Projects\scripts` was byte-identical.
- Community Framework, <https://github.com/Arkensor/DayZ-CommunityFramework.git>, pinned and then-current production commit `0763e7e7548c9a0bed6626afff835de80693ebf3`, `JM/CF/Scripts/3_Game/CommunityFramework/RPC/RPCManager.c:45-215`, SHA-256 `377E40A999D5465EC754DDAD98EE96AC16218613187261CEAFBFA29A0F21C622`, implements framework routing/registration/read/send behavior but does not establish a native payload ceiling.
- `D:\StarDZ\docs\GUIA_SEGURANCA_E_MULTIPLAYER.md:185-330,929-1195,1526-1620`, SHA-256 `43AAECA6B5A5353499FE592C47615766EDE14DC8AB53B9E21B6551E32CFB07E8`, was read for extracted RPC declarations, authentication/trust/idempotency/rate-limit guidance, unicast, and the limits register. Its lines 1581-1593 state that maximum payload, rate limit, and unreliable-delivery behavior were not measured.
- `D:\StarDZ\docs\CF_COMPLETE_REFERENCE.md:281-386,1295-1415`, SHA-256 `AB0428821B300FB42ADF3170B3BA9ED4C00302EF460362A4F4BD2FA98FD10A61`, was read for its CF/RPCManager description and source pointers. It corroborates where to inspect CF but is not engine authority.
- `D:\StarDZ\docs\DAYZ_MOD_ARCHITECTURE_PATTERNS.md:408-605`, SHA-256 `315C4C07A240C46D239984288F903860D46076A34376AC9CEDF5281D57D87B5B`, was read for RPC and trust patterns. It does not contain a build-scoped payload measurement.

### Still required measurement

Run a dedicated server with at least two clients on a recorded stable build, beginning with `1.29.163709` if it remains the target. For client-to-server, server-to-one-client, and server broadcast, test both `guaranteed=true` and `false`, several serialization shapes, and increasing payload sizes across repeated trials. Record intended bytes/fields, received bytes/field count/checksum, latency, timeout, drop, disconnect, and client/server logs. Report only the observed range and failure behavior for that exact build, direction, serialization, and delivery mode; do not convert one observed breakpoint into a universal protocol ceiling.

---

## User Corpus Crosswalk Actually Read

This is not a claim that the whole 110-file corpus was audited. These are the substantive ranges reopened for this six-finding council:

| Document | SHA-256 | Substantive ranges read | Use in this council | Authority limit |
|---|---|---|---|---|
| `D:\StarDZ\docs\GUIA_SEGURANCA_E_MULTIPLAYER.md` | `43AAECA6B5A5353499FE592C47615766EDE14DC8AB53B9E21B6551E32CFB07E8` | 185-330; 929-1195; 1526-1620 | RPC declarations, sender/trust, rate limiting, idempotency, and explicit unmeasured limits | Local secondary reference; its project claims require independent validation |
| `D:\StarDZ\docs\CF_COMPLETE_REFERENCE.md` | `AB0428821B300FB42ADF3170B3BA9ED4C00302EF460362A4F4BD2FA98FD10A61` | 281-386; 1295-1415 | CF RPCManager structure and pointers | Secondary reference; reopened pinned CF code controls |
| `D:\StarDZ\docs\COOKBOOK_RECEITAS_COMPLETAS.md` | `0D05D8B011933D7E9ADC246CA3180C14A6EC2681F39CC91C655458509DEB9B9A` | 1-271 | Complete-example criteria, validation loop, pack-vs-compile warning | Self-reported verification is not independent proof |
| `D:\StarDZ\docs\STARDZ_CURRENCY_BRIDGE_CONTRACT.md` | `2CCF77EDC3DC6F0E3CD3FD8AC7B3CBDB8A85EBCCB845C88223958AA15DA2EEE9` | 1-124 | Trading outcomes, idempotency, reference IDs, debit-first risks, missing integration status | Product contract/design; not implemented DayZ behavior |
| `D:\StarDZ\docs\DAYZ_MOD_ARCHITECTURE_PATTERNS.md` | `315C4C07A240C46D239984288F903860D46076A34376AC9CEDF5281D57D87B5B` | 1-130; 408-605; 1792-1913 | Architecture/RPC/lifecycle patterns and readiness claims | Local secondary reference; “production-ready” labels are unverified |
| `D:\StarDZ\docs\DayZ\Server Configuration.md` | `D7126F849E9A460887A3B640068CA8C88304324EDFD3AFA1526AE69E4BECAA8E` | 1-202, especially 19 and 150-175 | Official saved `passwordAdmin`, BattlEye/RCon, profile/path/log configuration | Saved snapshot; live BIKI access returned HTTP 403 |

The saved official `D:\StarDZ\docs\DayZ\Diag Menu.md` was also read at lines 1, 690-694, and 801-854 for `DayZDiag_x64.exe`, teleport, and free-camera scope; SHA-256 `58CAD3A5194F0237A99D30C08BE68F60B5B2A531C605817022E50397D14FE616`.

## Bounded Terra Implementation Set

The immediate edit should contain exactly these six finding repairs:

1. `OPS-C01`: separate `passwordAdmin` from `RConPassword`, preserve the runtime/log test caveat.
2. `OPS-C02`: replace the asserted vanilla tool list with the evidence-bounded retail/Diag/mod distinction and preserve the retail inventory test.
3. `TUT-C01`: rename/reframe the chapter and diagrams as safe refusal, update its EN/shared labels, and retain the full transaction fixture as open work.
4. `TUT-C02`: remove production/copy-paste/completeness promises, correct the build boundary, add the fixture checklist, and retain end-to-end validation as open work.
5. `LANG-C03`: change only the TOC terminology to “Config-Based Type Checking” and verify the existing anchor.
6. `RPC-C02`: replace both ceiling/limit claims with explicit unknown/measure language and retain the two-client measurement fixture as open work.

Do not mark `OPS-C01`, `OPS-C02`, `TUT-C01`, `TUT-C02`, or `RPC-C02` functionally complete merely because the immediate English corrections land. The correction commit can close the misleading prose portion; the runtime/fixture portion must remain visible in the coverage ledger.
