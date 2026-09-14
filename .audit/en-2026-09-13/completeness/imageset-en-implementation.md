# Imageset EN implementation

**Implemented:** 2026-09-14 America/Sao_Paulo  
**Scope:** Council-approved edits only in the four assigned English pages. No PBO page, locale, tooling, game/client, Workbench, packer, dependency installation, full build, or commit was changed or run.

---

## Source evidence reopened

The implementation reopened these extracted DayZ artifacts and matched the council-recorded SHA-256 values:

| Source | SHA-256 | Evidence used |
|---|---|---|
| `D:/DayZ Projects/gui/imagesets/dayz_gui.imageset` | `AD001B5391F351FFDC68CBB39B685D16E21F5313862C251CB48A65241FA1095A` | Brace structure, two texture references, `RefSize`, `Groups {}`. |
| `D:/DayZ Projects/gui/imagesets/playstation_buttons.imageset` | `B47F8B0370328D8B5DF3937A7A17093E82ADD6C717D1B8589604C0B0D7C8E14A` | Observed `mpix 1`/`2` base/`@2x` pairing. |
| `D:/DayZ Projects/scripts/1_core/proto/enwidgets.c` | `6BB20BAD5EFA498E584C7AE8976A1BF5310BCD9019215F31CB2990AF21CE0C9E` | `ImageWidget.LoadImageFile` documentation and `LoadWidgetImageSet(string filename)` declaration. |

The implementation also reopened the pinned public DayZ Expansion registration/layout and Community Framework `.gproj` excerpts at their recorded commits. Those direct links now appear in the affected reader pages; they demonstrate source shape and consumption only, not runtime timing, preview behavior, or loader semantics.

---

## Scoped changes

- `en/03-gui-system/07-styles-fonts.md`: removed prevalence/single-texture, EDDS-workflow, global-loading, GPU, and atlas-performance assertions. The retained custom brace template now includes observed `Groups {}`, a non-literal resource-reference marker, coordinate-reference wording, bounded `mpix` observations, `CfgMods` registration, layout consumption, and a checked client-side `LoadImageFile` example marked uncompiled/unpacked/unrendered.
- `en/05-config-files/04-imagesets.md`: removed the unsupported XML tutorial, XML worked example, XML comparison/endorsement, and downstream XML-active-use claim. The page now bounds `CfgMods`, `LoadWidgetImageSet`, `path`, `RefSize`, `mpix`, conversion, collision, case, global-scope, silent-failure, GPU, and performance statements; its custom fixture retains placement, substitution markers, `Groups {}`, registration, layout/script consumption, and explicit verification limits.
- `en/04-file-formats/01-textures.md`: retained the scoped fact that reviewed imagesets name `.edds`, while replacing the Workbench-management instruction with the unvalidated-creation/import/conversion boundary.
- `en/04-file-formats/07-workbench-guide.md`: retained observed `.gproj imageSets` structure and replaced the preview-required/missing-image assertion with the untested-omission boundary, separate from runtime `CfgMods` registration.

Final coordinator review clarified that the resource-reference marker must stand for the complete quoted `path` value, not a prefix. The two imageset pages now say this directly, preserve intended virtual placement beside the template, and restore the major-section separator before **Common Mistakes**.

No removed heading has a detected caller outside the assigned files; the final strict EN anchor check is the controlling verification record below.

---

## Before and after hashes

| File | Before SHA-256 | After SHA-256 |
|---|---|---|
| `en/03-gui-system/07-styles-fonts.md` | `FBF0A50A5BA392359BB70D5D41F9BB1FA75379A0E16D66A23BF4F452DAFF7601` | `EF8A50E2A689DE88E15ABB14265A5A399D1CB25E7BC995E40B54A64A2409B484` |
| `en/05-config-files/04-imagesets.md` | `6759F4E2F50E1B293D7549D726A9616C08B5D9AE30890A9C3A6ECA3D886C7A8C` | `319A97B0F78C093044E7501487CABCCA7B9D3324C1BC1BD7D5FFD8CFA7FAB040` |
| `en/04-file-formats/01-textures.md` | `2B976BF1B8D141AA0B80328418D710E168F6D653D07EB21707237C4559E29C81` | `A733F705B5BDD13000B4C24937D408D4984743EA86A8BEB8743EFA11EA99BDC1` |
| `en/04-file-formats/07-workbench-guide.md` | `532C48DD4F1A41CFDFB5FA1284D4D7E759E246D7A318C2F3B09DD5AC80F289BE` | `ACAA8F66B4AC73A265266F50DC4CF278C6239BD48F8CFA1BF60CD437F6743504` |

---

## Verification limits

The requested strict EN anchor/link check and scoped `git diff --check` are run after this report is added and are recorded in the companion JSON. No render, VitePress build, script compile, client/server test, Workbench test, packer run, installation, or commit was run; the custom fixtures still require those gates before being presented as working assets.
