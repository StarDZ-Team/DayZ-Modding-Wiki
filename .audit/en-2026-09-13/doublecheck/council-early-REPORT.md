# Council Early Evidence Review

## Scope and method

Independent review of the source-backed findings in `assets_gui-astra-partial.json` and `server_reference-astra-partial.json`, plus coordinator-requested `AGUI-DC-008` through `AGUI-DC-010` from the finalized GUI/assets report. The audited English pages remain byte-identical to baseline `bf7ae1947876071ed4e25578dc595d896f2e6263`; no English content was edited and no runtime behavior was tested.

The local official extraction was reopened and byte-compared with a fresh shallow clone of BohemiaInteractive/DayZ-Script-Diff at commit `86974a0f5bd16b1ee3e334ad828133c93dca80a1` (Build 1.29.163709, Scripts Rev. 125372). The relevant files are byte-identical in both locations:

- `scripts/1_core/proto/enwidgets.c`: `6BB20BAD5EFA498E584C7AE8976A1BF5310BCD9019215F31CB2990AF21CE0C9E`
- `scripts/3_game/tools/uiscriptedmenu.c`: `69E45D6C74380BA23A30C8A66E0721A9CE618C49C8AD4AF08920639A2438484B`
- `scripts/3_game/cfggameplayhandler.c`: `C00C41C9AD8BBB28A8269E73971AD5ECC63A54025C7DDD8F0576692558217974`
- `scripts/2_gamelib/tools.c`: `48E8DAFACF8D8BD6D38A141896039720507488E45E1EFB369958B29BEC68D38B` (reopened at the same pinned commit for `ScriptInvoker`/`func` support).

Pinned source URLs use `https://github.com/BohemiaInteractive/DayZ-Script-Diff/blob/86974a0f5bd16b1ee3e334ad828133c93dca80a1/...`. Official BIKI pages were independently requested on 2026-09-13 but direct requests returned HTTP 403; indexed official page bodies corroborated the gameplay activation requirement and the `verifySignatures` setting. No web-body hash is claimed.

## Dispositions

### Accept exact repair

- `AGUI-DC-001`, `AGUI-DC-002`, `AGUI-DC-003`: `CheckBoxWidget` declares `IsChecked()` and `SetChecked(bool)` at pinned `enwidgets.c` lines 418-423; `GetState()`/`SetState()` are not its API. Use each proposed old/new replacement exactly.
- `AGUI-DC-005`: pinned `UIScriptedMenu.OnShow()` lines 173-181 performs control locking and conditional death-callback registration, while pinned `enwidgets.c` lines 694-698 states that `SetActiveWindow(..., true)` selects a focusable child and `SetFocus` requires an input-capable widget. Use the proposed old/new replacement exactly. This is static API/lifecycle evidence, not a runtime guarantee.
- `AGUI-DC-006`: pinned `enwidgets.c` line 590 accepts a `func` callback and pinned `tools.c` lines 115-127 provides `ScriptInvoker` over `func`; the absolute claim that name-string routing is the standard mechanism for every arbitrary caller is false. Use the proposed old/new replacement exactly.
- `AGUI-DC-008`: official Addon Builder revision 341605 states that `-prefix` is calculated automatically when absent. Use the proposed old/new replacement exactly; wording correctly tells readers to verify the resulting virtual prefix.
- `AGUI-DC-009`: official server configuration exposes server-side `verifySignatures`; multiplayer itself does not inherently require signatures. Use the proposed old/new replacement exactly.
- `SR2-001`: pinned `cfggameplayhandler.c` lines 53-67 gates the mission file on `enableCfgGameplayFile` and file existence. Official Gameplay Settings independently says to set `enableCfgGameplayFile = 1`. Use the proposed old/new replacement exactly.
- `SR2-002`, `SR2-003`: pinned `cfggameplayhandler.c` lines 70-77 calls `ErrorEx(errorMessage)` on JSON load failure, then continues validation/loading. The proposed repairs carefully avoid asserting a fully default fallback. Use each proposed old/new replacement exactly.

### Accept with revised exact repair

- `AGUI-DC-004`: the omission is real, but the proposed comment says “source layout” inside an example whose widget was created programmatically. Replace the exact line `tw.SetTextExactSize(16);           // Font size in pixels` with `tw.SetTextExactSize(16);           // Only works when the Exact Text flag is already enabled` and add immediately after the code block: `\`SetTextExactSize()\` does not enable Exact Text mode; configure that flag in the widget's layout before relying on the requested size.` This follows pinned `enwidgets.c` lines 192-193 without implying the shown `CreateWidget()` call can configure the native flag.

### Reject

- `AGUI-DC-007`: the cited `LoadWidgetImageSet(string filename)` declaration proves neither XML support nor relative parsing performance, and the candidate is itself labeled an unresolved uncertainty. Reject the proposed replacement as a source-backed correction; it substitutes another unsupported recommendation (“use the native ... format”) instead of establishing what formats the target build accepts.
- `AGUI-DC-010`: official model documentation establishes that `model.cfg` data is processed/baked during binarization, but that does not disprove the page's distinct claim that an MLOD stored with `-packonly` can load in the retail game. Reject this finding and replacement unless target-build runtime evidence or an explicit authoritative compatibility statement establishes MLOD loading behavior. The release recommendation may be sensible, but it is not an evidence-complete correction of the quoted claim.

## Exact repair inventory

The authoritative machine-readable old/new strings are in `council-early.json`. Accepted exact repairs preserve the authors' proposed strings; the sole revised repair is `AGUI-DC-004`. Rejected candidates have `final_new_text: null` and must not be applied.

## Limitations

This is a static evidence review. It does not guarantee runtime correctness, native parser behavior, focus behavior for every concrete widget tree, log sink/location, or MLOD compatibility. No full build was run because the dispatch prohibited it.
