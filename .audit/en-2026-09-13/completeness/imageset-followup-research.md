# Imageset format follow-up research

**Observed:** 2026-09-14 America/Sao_Paulo  
**Wiki revision:** `bbfa203d036e8f02c733e50011c89b9dfbdf9ecf`  
**Scope:** `en/03-gui-system/07-styles-fonts.md` and imageset-related statements in `en/04-file-formats`; `en/05-config-files/04-imagesets.md` was reopened only because it contains the current XML example named by the task. No English page was edited. No game, client, server, Workbench, compiler, packer, or site build was run.

## Result

The native evidence supports brace-delimited `ImageSetClass` resources, `CfgMods > defs > imageSets > files[]` registration for a mod, `.gproj imageSets` listing for a Workbench project, and `set:<declared Name> image:<declared Name>` consumption. It does **not** establish that the XML schema currently shown at `en/05-config-files/04-imagesets.md:140-183` is accepted by `LoadWidgetImageSet`, by `CfgMods` registration, or by any other native loader.

Community Framework has a third-party generic XML parser (`CF_XML.ReadDocument`/`CF_XML_Document.Read`), but the opened code contains no imageset adapter and no call to `LoadWidgetImageSet`. A generic parser is therefore not evidence that XML becomes a native widget imageset. No `<imageset ...>` file matching the wiki example was found in the pinned VPP, CF, COT, Expansion, or Editor checkouts, and no `LoadWidgetImageSet` call was found in those checkouts or the extracted DayZ scripts. These absences bound this review; they do not prove universal rejection.

## Claim dispositions

| ID | Current claim or gap | Verdict | Evidence and minimal disposition |
|---|---|---|---|
| IS-01 | `07-styles-fonts.md:236`: an imageset is “a single texture file” | **Reject as written** | `dayz_gui.imageset:4-12`, `playstation_buttons.imageset:4-12`, and other extracted sets contain two `ImageSetTextureClass` entries. Say “one named rectangle map with one or more atlas texture variants.” |
| IS-02 | `:236`: imagesets are the “most common” image source | **Unresolved** | The reviewed sources show frequent use, not a population-level comparison against direct file loads. Delete the quantifier or scope it to the examples reviewed. |
| IS-03 | `:249`: reference syntax is `set:<imageset_name> image:<image_name>` | **Accept with precision** | Vanilla layouts/scripts and pinned mods use this form. “imageset name” means the resource's internal `ImageSetClass.Name`, not necessarily its filename. |
| IS-04 | `:319-363`: native brace structure and fields | **Accept with two repairs** | All 11 extracted `.imageset` files begin `ImageSetClass {`; VPP, Expansion, and Editor custom sets do too. Add the trailing `Groups {}` block used by every extracted vanilla set and describe `RefSize` as the coordinate reference size, since a set can select multiple physical texture sizes. |
| IS-05 | `:323`: “Used by vanilla DayZ and most mods” | **Accept vanilla; reject “most mods”** | Vanilla is direct extraction evidence. Three reviewed projects ship custom brace sets and CF/COT `.gproj` files list brace resources, but that sample cannot establish “most.” |
| IS-06 | `:362`: `mpix` behavior | **Accept only the current bounded wording** | Extracted sets directly show `0`, `1`, `2`, and `3` values and multiple patterns. No loader declaration explains selection/fallback, so retain the instruction to copy a matching shipped pattern and test; do not assign universal semantics. |
| IS-07 | `:368-407`: custom native example | **Accept syntax direction; revise example** | It matches observed class names, but omits `Groups {}` and uses an unqualified invented resource path. Use the exact shipped excerpt below, then tell readers to substitute the complete Workbench-produced resource reference and their own coordinates. |
| IS-08 | `:409-429`: register under `CfgMods.defs.imageSets.files[]` | **Accept** | Official DayZ Modding Structure search-index content shows this exact optional custom-imageset block. Expansion `config.cpp:39-56` and Editor `config.cpp:23-37` independently implement it. The official page and API were directly inaccessible with HTTP 403, so the official evidence is limited to the search-index excerpt. |
| IS-09 | `:447-448,509`: no manual load after `config.cpp` registration / available “globally” | **Accept mechanism; narrow wording** | Expansion and Editor register sets and consume their names without a `LoadWidgetImageSet` call. Say that registered references are available to the client UI when the owning mod/PBO is loaded; do not imply proven collision order, failure logging, server-only availability, or eager startup/GPU behavior. |
| IS-10 | Native `LoadWidgetImageSet` contract | **Partly accepted, otherwise unresolved** | `enwidgets.c:692` declares `proto native bool LoadWidgetImageSet(string filename);`. The declaration establishes filename input and boolean return only; it does not document accepted grammar, XML, caching, call timing, registration scope, or errors. |
| IS-11 | `04-imagesets.md:140-183`: XML schema exists as an alternative imageset format, with feature comparisons and production recommendation | **Reject pending evidence** | No opened native or pinned-project source uses that schema. CF's parser is generic third-party code and has no imageset integration. The XML block is not currently a supported tutorial; remove or label it hypothetical/custom-loader input until an actual loader implementation or version-matched runtime proof is produced. |
| IS-12 | `04-file-formats/01-textures.md:6,15,55-59,341-345`: shipped imagesets reference EDDS atlases | **Accept, scoped to reviewed GUI resources** | Extracted `.imageset` paths resolve to extracted `.edds` resources. `dayz_gui.edds` starts with DDS magic and includes an `ENF1` extension marker; this supports the warning that an arbitrary DDS export or rename cannot be assumed to be a valid EDDS resource. It does not establish every GUI texture pipeline or conversion workflow. |
| IS-13 | `04-file-formats/06-pbo-packing.md:265`: keep `.edds` in the format referenced by the imageset | **Accept as packaging guidance** | Native and reviewed project imagesets name `.edds` paths. No pack/load test was run here, so do not expand this into a universal binarizer transformation rule. |
| IS-14 | `04-file-formats/07-workbench-guide.md:148-153,243`: `.gproj imageSets` entries support layout preview | **Accept project-registration structure; runtime UI effect untested** | Pinned CF, COT, and Editor `.gproj` files list vanilla/custom `.imageset` paths. Local build documentation §3.3.1 makes the same distinction. This is separate from runtime `CfgMods` registration; exact missing-resource preview behavior still needs a Workbench observation. |

## Proposed minimal English replacement

This wording is a proposal for independent council review, not authorization to edit EN.

### Replace the opening and format claim in `07-styles-fonts.md`

> An imageset maps names to rectangular regions in an atlas coordinate space and can provide one or more texture variants. Layouts and `ImageWidget.LoadImageFile` refer to an entry as `set:<set-name> image:<image-name>`, where both names come from the `Name` fields inside the imageset resource.
>
> Extracted DayZ resources and the reviewed VPP, Expansion, and Editor resources use brace-delimited `ImageSetClass` syntax. Native support for the XML schema shown elsewhere in this wiki is unverified.

### Replace the invented format example with a source-backed excerpt

The following is shortened from extracted `gui/imagesets/bleedingdrops.imageset`; it is a syntax reference, not an asset for a mod to copy:

```text
ImageSetClass {
 Name "BleedingDrops"
 RefSize 512 512
 Textures {
  ImageSetTextureClass {
   mpix 0
   path "{35363C01F72D2EBE}Gui/imagesets/BleedingDrops.edds"
  }
 }
 Images {
  ImageSetDefClass Bleeding1 {
   Name "Bleeding1"
   Pos 0 0
   Size 128 128
   Flags 0
  }
 }
 Groups {
 }
}
```

> For your mod, import/create the EDDS resource through the GUI resource workflow, preserve the complete resource reference produced for it, and replace the set name, rectangle names, coordinates, and sizes. `RefSize` is the coordinate reference size. `mpix` patterns vary among shipped sets; copy a matching shipped pattern and verify scaling instead of treating the number as a universal quality flag.

### Keep registration, but state its two contexts

> Add the `.imageset` virtual path to `CfgMods > <YourMod> > defs > imageSets > files[]` in the `config.cpp` packaged with the client-loaded mod. This is runtime mod registration. For Workbench layout preview, also list the resource in the active project's `GameProjectConfigClass.imageSets`; the `.gproj` list does not replace the packaged `CfgMods` entry.

The current `CfgMods` code shape at lines 413-429 is consistent with the official example and pinned projects. Do not say it proves silent failure, collision order, startup timing, or GPU residency.

### Give a real consumption API and context

```c
ImageWidget icon = ImageWidget.Cast(root.FindAnyWidget("MissionIcon"));
if (icon)
{
    bool loaded = icon.LoadImageFile(0, "set:mymod_icons image:icon_mission");
}
```

> Run this in client-side UI code after the widget exists. `LoadImageFile` returns whether the image loaded. This loads a named image into widget slot `0`; it is not the same operation as `LoadWidgetImageSet(filename)`. When the set is registered through `CfgMods`, no separate `LoadWidgetImageSet` call is shown by the reviewed Expansion/Editor usage.

### Remove or quarantine the XML tutorial

> The native declaration `LoadWidgetImageSet(string filename)` does not document an XML grammar. The XML example below has not been tied to a native loader or to a custom imageset adapter, so do not present it as a working DayZ imageset. A third-party XML parser by itself only produces an XML document; it does not register named GUI images.

## What still requires compile/load/render evidence

1. Build a minimal client PBO containing one Workbench-produced `.edds`, one brace `.imageset`, `CfgMods.defs.imageSets`, one layout, and one client UI controller. Record tool/game versions, config compilation result, PBO contents, virtual prefix, and hashes.
2. Launch a version-matched client with the mod, inspect RPT/script logs, call `ImageWidget.LoadImageFile`, record its boolean result, and capture the rendered icon. Repeat once from a layout `image0` reference.
3. For XML only, first identify a documented native schema or an actual custom adapter. Then test an otherwise identical XML fixture both through `CfgMods` and through `LoadWidgetImageSet`, recording return values, logs, and render output. Stop if no source identifies the schema/loader contract; do not brute-force XML variants.
4. For Workbench claims, open the same layout with and without its `.gproj imageSets` entry and capture the preview/resource errors. This validates editor behavior, not retail runtime behavior.
5. Collision order, eager loading, caching, GPU residency, and failure-mode claims require separate instrumented tests; none follows from successful registration or one rendered image.

## Sources actually opened

### Current audit inputs and pages

- `.audit/en-2026-09-13/completeness/assets-evidence-council.md`, SHA-256 `D9E2A51C1DA526CEF953635C733A69BE3483FA3AD2A2FB0DB9F678988B8DD9A3`, especially Decision 1, primary sources, and follow-up claims.
- `.audit/en-2026-09-13/completeness/assets-en-council.json`, SHA-256 `C7DB67DC64B37567BB0321BABBA1AC46B18BA354237DF91884C767E30533617C`.
- `en/03-gui-system/07-styles-fonts.md`, SHA-256 `FBF0A50A5BA392359BB70D5D41F9BB1FA75379A0E16D66A23BF4F452DAFF7601`.
- Related current pages: `en/04-file-formats/01-textures.md` SHA-256 `2B976BF1B8D141AA0B80328418D710E168F6D653D07EB21707237C4559E29C81`; `06-pbo-packing.md` SHA-256 `85826A8F40B7DFBA6DD32E0B686CE3DA7892BD8048AC2FEC0135460206226914`; `07-workbench-guide.md` SHA-256 `532C48DD4F1A41CFDFB5FA1284D4D7E759E246D7A318C2F3B09DD5AC80F289BE`.
- `en/05-config-files/04-imagesets.md`, SHA-256 `6759F4E2F50E1B293D7549D726A9616C08B5D9AE30890A9C3A6ECA3D886C7A8C`, reopened only for the XML claims requested in this task.

### Extracted DayZ material

- `D:/DayZ Projects/gui/imagesets/dayz_gui.imageset:1-25`, SHA-256 `AD001B5391F351FFDC68CBB39B685D16E21F5313862C251CB48A65241FA1095A`.
- `D:/DayZ Projects/gui/imagesets/playstation_buttons.imageset:1-20`, SHA-256 `B47F8B0370328D8B5DF3937A7A17093E82ADD6C717D1B8589604C0B0D7C8E14A`.
- `D:/DayZ Projects/gui/imagesets/bleedingdrops.imageset:1-35`, SHA-256 `D153C931D28560C50D5DE645D59E6AEAC6F88B2EBC4CB4FCA1E98A75E5CC5A19`. All 11 sibling `.imageset` files were read mechanically for first line, texture count, image count, and `Groups`; all start with `ImageSetClass {` and all contain `Groups {}`.
- `D:/DayZ Projects/scripts/1_core/proto/enwidgets.c:247-291,688-693`, SHA-256 `6BB20BAD5EFA498E584C7AE8976A1BF5310BCD9019215F31CB2990AF21CE0C9E` (`ImageWidget.LoadImageFile`; global `LoadWidgetImageSet`).
- `D:/DayZ Projects/gui/looknfeel/dayzwidgets.styles:1-25`, SHA-256 `5F7DD4DEC94FAC2B937A3ED1209ED4D17B15220BBCD74A77FB28FA5F0D286240`, opened to distinguish native XML widget-style resources from brace imagesets.
- `gui.txt` and `scripts.txt` both state `product=dayz`, `version=124588`; hashes `842BADDDFAC0C005B23766ED0A8ED75A60A65AFF952166DA2A181930E6CAF258` and `E45D501E4FB29587FA1E8BF553B0A7B33B751AA32C5AA5ECB1D03B8B6026F55F`. This is extraction metadata, not a proven public game version mapping.

### Local documentation (leads, not independent engine proof)

- `D:/StarDZ/docs/DAYZ_GUI_REFERENCE.md` §2 image attributes (`:194-205`) and notification example (`:1360-1380`), SHA-256 `F83CD7E9843AAD1001B36E40883E3FF876FE645489C958DBFD83067A35AB9063`.
- `D:/StarDZ/docs/REFERENCIA_TIPOS_DE_ARQUIVO.md` `.edds`/`.edds.meta` (`:78-118`) and `.imageset` (`:327-363`), SHA-256 `BCC70BBA5733111C8EF513A1B2A2735A9B9D71C5A282B1D70CC86643ECFAD1C1`.
- `D:/StarDZ/docs/GUIA_FERRAMENTAS_E_BUILD.md` §3.3.1 (`:270-324`), SHA-256 `2ECAC825A7CC0995A2A97F5040CA26291A484E2CB5F5E42EBCC0195C5E9367D9`.

### Pinned public repositories

- VPP Admin Tools, `https://github.com/VanillaPlusPlus/VPP-Admin-Tools.git`, commit `dc22e420df3b54e821055f9764da1e48f4a31e71`: `GUI/Textures/vpp_icons.imageset:1-20`, SHA-256 `C80AE1549BF850399FE56AD133FD13ADBE3891982D55D49ED5502351A3B38546`; `VPPCollapsibleSection.c:24-32`, SHA-256 `FA4CC67DB449AAE44CAD8E5C0A0306D2E1F284E459867041012CC3C3418DBF76`.
- Community Framework, `https://github.com/Arkensor/DayZ-CommunityFramework.git`, commit `0763e7e7548c9a0bed6626afff835de80693ebf3`: `JM/CF/Workbench/dayz.gproj:14-28`, SHA-256 `B9198EDDA2A7620C967F0DEBCAAB61DA261108E018BF45734936B0FCB73C757F`; `CF_XML.c:1-66`, SHA-256 `E8FABC34831789D1A0E97CE8DBF57A0963224B0F9EFD5913E8CC80A26FA76A6C`; `CF_XML_Document.c:1-180`, SHA-256 `2BDABA2ACF7AC97F40DD3681823DE9519FCED18264CD11FBCF38F4EE35040F81`.
- Community Online Tools, `https://github.com/Jacob-Mango/DayZ-CommunityOnlineTools.git`, commit `41f2c2b99565d0e3970163e162efbf1283fdca62`: `JM/COT/Workbench/dayz.gproj:14-29`, SHA-256 `DAE014105C1143D120B714673C10B183886408369E16C2FA5869204E32F94429`.
- DayZ Expansion Scripts, `https://github.com/salutesh/DayZ-Expansion-Scripts.git`, commit `6dacd00f6d943ebbd99e0cf1baad93f470d96419`: `Core/Scripts/config.cpp:12-56`, SHA-256 `8973F7648357EF6B1FFA70F0E8168915052674F412EB15B7090E6E38B41826EA`; `Core/GUI/imagesets/expansion_gui.imageset:1-26`, SHA-256 `F598C8741A4AB13F17B5E2534FDAD0A0512BFD5C9095C7A5ABAE2F8572326A9B`; `GUI/layouts/expansion_loading.layout:48-75`, SHA-256 `88D29E0A21A7672F0B7EB4E5FB96654B53D4E550D42907EEF7031EED72E1E68A`.
- DayZ Editor, `https://github.com/InclementDab/DayZ-Editor.git`, commit `992e6b29b42b5d8e609632b59771335a23d205eb`: `DayZEditor/Scripts/config.cpp:10-37`, SHA-256 `1B0D5EC71A26F8B73BFBC2156CE303F65028C0CF6AFB09416AFA84F49A1BA39A`; `dayz_editor_gui.imageset:1-30`, SHA-256 `DD9A882D0AE0A3923C473F8A812DC12B35C8E2B31F3EE468B4DE422993F2F0A8`; `EditorHud.layout:2290-2350`, SHA-256 `CC5481DD19B6EAF82C6ABB7310EC69B6EFCA31C2F4E3880B50A49F20492A8674`.
- Official DayZ Samples, `https://github.com/BohemiaInteractive/DayZ-Samples.git`, commit `da5e5437c9502620d9853fb6eed14701135ab2ea`: repository-wide imageset search returned no relevant file; this is not absence proof.

### Official web access

- `https://community.bohemia.net/wiki/DayZ:Modding_Structure`, accessed 2026-09-14. Search-index content exposed the exact `CfgMods.defs.imageSets.files[]` example. Direct page and old-domain access both returned HTTP 403; no claim here relies on unseen page text beyond that captured excerpt.

## Council gate

An independent reviewer must reopen the cited extraction, official snippet/access failure, CF XML parser, at least one registered brace implementation and its consumer, and the exact proposed wording. No EN edit should occur until that council explicitly accepts, rejects, or returns each disposition and verifies the final proposed bytes.
