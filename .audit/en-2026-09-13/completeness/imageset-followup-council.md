# Imageset follow-up council

**Observed:** 2026-09-14 America/Sao_Paulo  
**Reviewed wiki revision:** `bbfa203d036e8f02c733e50011c89b9dfbdf9ecf`  
**Role:** independent source council; no EN page, game, Workbench, server, client, build, packer, installer, or commit was run or changed.

## Council result

The research is directionally sound and all 29 hashes in its `source_use` array match the independently reopened bytes. Its native-brace, registration, reference-syntax, and XML-evidence boundaries are accepted, but its proposed replacement is **returned with repairs**: observed recurrence does not prove that `Groups {}` or a GUID-prefixed resource reference is mandatory; the opened sources do not establish an EDDS import workflow or Workbench preview failure; and a stock excerpt alone would make the custom-mod tutorial less useful.

The XML tutorial is rejected more strongly than the author recorded. `D:/StarDZ/StarDZ_Market_Hub/StarDZ_MarketHub/GUI/imagesets/mh_icons.imageset` is the apparent local source of the wiki schema: it is an XML placeholder whose own comments say to replace a missing EDDS later. The directory contains no `mh_icons.edds`, no consumer was found, and the mod has no XML-to-imageset adapter. CF's opened XML code is a generic document parser; its concrete call in `ModStructure.c:193-211` parses `modded_inputs`, not imagesets.

## Decisions on all 14 findings

| ID | Council decision | Exact boundary |
|---|---|---|
| IS-01 | **Accepted with wording repair** | Replace “single texture file” with: “An imageset names rectangular regions and can reference one or more atlas texture resources.” Calling every entry a “variant” would infer loader semantics. |
| IS-02 | **Accepted unresolved** | Remove “most common”; no population comparison was performed. |
| IS-03 | **Accepted** | `set:<set-name> image:<image-name>` is directly observed in extracted layouts/scripts and pinned VPP, Expansion, and Editor usage. Both names come from internal `Name` fields, not filenames. |
| IS-04 | **Partly accepted** | Brace-delimited `ImageSetClass`, the shown member names, and a trailing `Groups {}` are observed in all 11 extracted sets and all 12 reopened pinned custom sets. Include an empty `Groups` block in the teaching template as the consistently observed shape, but do not call it required without grammar or A/B evidence. `RefSize` is a coordinate reference size: `dayz_gui` keeps `RefSize 1024 1024` while its two DDS headers are 1024×1024 and 2048×2048. |
| IS-05 | **Accepted split** | “Used by extracted vanilla DayZ” is supported. “Most mods” is rejected; the reviewed sample cannot establish prevalence. |
| IS-06 | **Accepted only for the bounded statement** | The extracted set values and pairings are facts. No source defines selection, ordering, fallback, DPI, or quality behavior. Remove stronger semantics still present in `04-imagesets.md:378-420`. |
| IS-07 | **Returned for repair** | Do not replace the useful custom-mod example with only a stock `bleedingdrops` excerpt. Retain a clearly marked teaching template with file placement, a non-literal resource-reference placeholder, `CfgMods` registration, layout and script consumption, client-UI context, and an explicit “not compiled/packed/rendered here” note. A brief attributed native excerpt may precede it as evidence; copy no stock asset content. |
| IS-08 | **Accepted as a registration mechanism, not a universal requirement** | Official BIKI text and Expansion/Editor configs support `CfgMods > defs > imageSets > files[]` for automatic mod registration. Replace “must” / “never loads” with “To register a packaged mod's custom imageset through `CfgMods`, list its virtual `.imageset` path…”. `LoadWidgetImageSet(string filename)` exists, so `CfgMods` cannot be presented as the only possible mechanism. |
| IS-09 | **Accepted as an observed implementation pattern; runtime claim unresolved** | Expansion and Editor register sets and reference their internal names without a repository call to `LoadWidgetImageSet`. Say exactly that. Do not claim global scope, eager/startup/GPU loading, collision order, silent failure, server availability, or a runtime guarantee; this council ran no client. |
| IS-10 | **Accepted split** | `enwidgets.c:692` establishes one `string` parameter named `filename` and a `bool` return type only. It does not define the boolean's meaning or the accepted grammar. Separately, the comment at `ImageWidget.LoadImageFile` lines 249-257 explicitly documents “True when image is loaded, false otherwise”; the proposed checked call is source-backed. |
| IS-11 | **Accepted rejection; expand removal scope** | Native support for the XML schema is unestablished, and the matching StarDZ file is explicitly an unfinished placeholder. Remove the XML section and every downstream claim/example that treats it as functional (`TOC`, worked example, best practice, theory table, compatibility claim); do not merely add a small warning beside lines 140-183. Keep a concise evidence-limit note if useful. |
| IS-12 | **Partly accepted** | Reviewed extracted and pinned GUI sets reference `.edds`; the extracted `dayz_gui.edds` has DDS magic and an `ENF1` marker. This does not establish every GUI pipeline, that Workbench imports/creates the resource in a particular way, or that renaming/converting a generic DDS succeeds or fails. Remove the unverified step-by-step EDDS conversion/import instructions. |
| IS-13 | **Accepted as narrow packaging guidance** | Preserve the `.edds` resource named by the imageset and its virtual path. Do not infer a binarizer conversion rule. |
| IS-14 | **Partly accepted** | CF/COT `.gproj` files directly contain `GameProjectConfigClass.imageSets`; this proves the project configuration structure. “Required for layout preview,” missing-image behavior, and the need to duplicate every runtime `CfgMods` entry are unresolved until a Workbench A/B observation. The two lists serve different configurations; mention `.gproj` only for readers maintaining a Workbench project. |

## Exact minimal EN change set authorized

The later implementation may edit the four pages below, and no broader imageset claims are approved by this council.

### `en/03-gui-system/07-styles-fonts.md`

1. Replace lines 232-249's “most common” / “single texture file” description with the IS-01 wording and clarify that `set:` and `image:` use internal names.
2. Keep a custom teaching example, add an empty `Groups {}` as the consistently observed shape, and label its resource ID/path and coordinates as substitutions. Do not call `Groups`, GUID prefixing, or a particular Workbench import workflow mandatory.
3. Describe `RefSize` only as the coordinate reference size. Keep the existing bounded `mpix` observations, but do not assign general selection/fallback semantics.
4. Keep the `CfgMods.defs.imageSets.files[]` shape and add a checked, client-side `ImageWidget.LoadImageFile` call after the widget exists. State that the reviewed mods use registered sets without a repository call to `LoadWidgetImageSet`; do not promise global availability.
5. Remove or narrow unsupported imageset performance/runtime claims at lines 499, 509, 511, and 538: batching efficiency, global scope, startup/GPU residency, and size-based VRAM recommendations were not established by this review.

### `en/05-config-files/04-imagesets.md`

1. Remove the XML TOC entry, XML section (current lines 140-183), XML worked example (695-715), XML best-practice endorsement (767), XML theory claim (780), and “active use” statement (790). Optionally replace them with one sentence: “No native loader contract or reviewed adapter establishes the XML schema formerly shown here; the matching local file is an unfinished placeholder.”
2. Preserve a custom brace-format tutorial and its placement/registration/consumption sequence. Include `Groups {}` as observed syntax, use a conspicuous non-literal resource reference placeholder, and state that the fixture still needs compile/pack/client render verification.
3. Change universal registration language at lines 44-47, 187-190, 516, 721-723, and 778 to the bounded `CfgMods` mechanism in IS-08. Remove silent-failure and global-scope claims.
4. Narrow `path` at line 91: pinned/extracted resources use GUID-prefixed virtual paths; StarDZ beta sets also contain plain paths, but no test in this review establishes whether either spelling is mandatory or interchangeable. Tell readers to preserve the complete reference and virtual path produced/recorded for their own resource; do not reuse an example GUID.
5. Remove unsupported `mpix` rules at 378-420, including higher-value selection, interchangeable single-set values, graceful fallback, high-DPI and quality-setting behavior. Retain only the observed values/pairings and the instruction to validate the intended scale.
6. Correct `RefSize` claims at 83, 744-746, 768-779: it defines the images' coordinate reference space and need not equal every physical texture variant. The extracted `dayz_gui` 1024/2048 pair is an attributable counterexample to the current universal wording.
7. Remove the unverified Workbench/Mikero/Pal2PacE EDDS workflow at 436-441 and the unverified runtime, collision, case-insensitivity, and performance claims at 723-790. Preserve only sourced syntax and clearly labeled untested guidance.

### `en/04-file-formats/01-textures.md`

Keep the scoped fact that reviewed imagesets reference `.edds`. Replace “Use Workbench to manage GUI texture resources” with an evidence boundary: this review did not validate a creation/import/conversion recipe, and a DDS header alone does not prove that an arbitrary export or rename is a usable DayZ EDDS resource.

### `en/04-file-formats/06-pbo-packing.md` and `07-workbench-guide.md`

Keep packing line 265 as narrow preservation guidance. In the Workbench page, retain the observed `.gproj imageSets` structure but replace “required for layout preview” and definite missing-image behavior with “reviewed projects list these resources here; the effect of omission was not A/B tested.” Do not instruct readers to duplicate every `CfgMods` entry unless they are also configuring a Workbench project that needs that resource.

## Evidence reopened independently

### Inputs and current pages

| Path | SHA-256 |
|---|---|
| `.audit/en-2026-09-13/completeness/imageset-followup-research.md` | `5C487CDFFB6719AD639341064E1E9CC2D9590868AE4A393CEA6ABBCECA35ED7A` |
| `.audit/en-2026-09-13/completeness/imageset-followup-research.json` | `8ADD18CBB86EF4DBF7ABE5EC2A0A3D1C363357A5CD807712CEBC909E4CA95A0A` |
| `en/03-gui-system/07-styles-fonts.md` | `FBF0A50A5BA392359BB70D5D41F9BB1FA75379A0E16D66A23BF4F452DAFF7601` |
| `en/05-config-files/04-imagesets.md` | `6759F4E2F50E1B293D7549D726A9616C08B5D9AE30890A9C3A6ECA3D886C7A8C` |
| `en/04-file-formats/01-textures.md` | `2B976BF1B8D141AA0B80328418D710E168F6D653D07EB21707237C4559E29C81` |
| `en/04-file-formats/06-pbo-packing.md` | `85826A8F40B7DFBA6DD32E0B686CE3DA7892BD8048AC2FEC0135460206226914` |
| `en/04-file-formats/07-workbench-guide.md` | `532C48DD4F1A41CFDFB5FA1284D4D7E759E246D7A318C2F3B09DD5AC80F289BE` |

All 29 `source_use` hashes supplied by the author were recomputed and matched. The pinned repository origins and HEADs also matched the report: VPP `dc22e420…`, CF `0763e7e…`, COT `41f2c2b…`, Expansion `6dacd00…`, Editor `992e6b2…`, and DayZ Samples `da5e543…`.

### Decisive primary/direct artifacts

| Path | SHA-256 | Use |
|---|---|---|
| `D:/DayZ Projects/gui/imagesets/dayz_gui.imageset` | `AD001B5391F351FFDC68CBB39B685D16E21F5313862C251CB48A65241FA1095A` | brace syntax, two textures, names, `RefSize`, `Groups` |
| `D:/DayZ Projects/gui/imagesets/playstation_buttons.imageset` | `B47F8B0370328D8B5DF3937A7A17093E82ADD6C717D1B8589604C0B0D7C8E14A` | differing observed `mpix` pair |
| `D:/DayZ Projects/gui/imagesets/bleedingdrops.imageset` | `D153C931D28560C50D5DE645D59E6AEAC6F88B2EBC4CB4FCA1E98A75E5CC5A19` | one-texture native shape |
| `D:/DayZ Projects/scripts/1_core/proto/enwidgets.c` | `6BB20BAD5EFA498E584C7AE8976A1BF5310BCD9019215F31CB2990AF21CE0C9E` | both native API declarations and `LoadImageFile` comment |
| `D:/DayZ Projects/gui/imagesets/dayz_gui.edds` | `243EEE81BE40A3C4E03FBDBDA8AEAFFAE2759AF42B3051C831A940F60E4C96ED` | DDS header, 1024×1024 |
| `D:/DayZ Projects/gui/imagesets/dayz_gui@2x.edds` | `8C45EEE54B90662558C16E8A3CF2052D0EBAB2535138E4ADBEEC5317B9B25F27` | DDS header, 2048×2048 |
| `D:/DayZ Projects/gui.txt` | `842BADDDFAC0C005B23766ED0A8ED75A60A65AFF952166DA2A181930E6CAF258` | extraction metadata `product=dayz`, `version=124588` only |
| `D:/DayZ Projects/scripts.txt` | `E45D501E4FB29587FA1E8BF553B0A7B33B751AA32C5AA5ECB1D03B8B6026F55F` | extraction metadata `product=dayz`, `version=124588` only |
| cached `BIKI-Modding-Structure.txt` | `192AC8BA4359CBD18BA643508E6615B72B1BEB1282D3361900D832ADA9837126` | full captured page text, including optional `imageSets.files[]`; capture time/transport is not embedded |
| `D:/StarDZ/StarDZ_Market_Hub/StarDZ_MarketHub/GUI/imagesets/mh_icons.imageset` | `650C76F789C2E9568BE558B57AAA65F9C557D00820C4B2F30D1E149BD102B19E` | matching XML placeholder; no EDDS sibling |
| `D:/StarDZ/StarDZ_Core/StarDZ_Core/GUI/icons/brands.imageset` | `3CB0C7322D4675C6B13718BEEA4874F89FFB991D66B74F5E689A93CEE9C3C83D` | beta brace set with plain path; not runtime proof |
| CF `CF_XML.c` | `E8FABC34831789D1A0E97CE8DBF57A0963224B0F9EFD5913E8CC80A26FA76A6C` | generic XML entry points |
| CF `CF_XML_Document.c` | `2BDABA2ACF7AC97F40DD3681823DE9519FCED18264CD11FBCF38F4EE35040F81` | generic tag/attribute document parser |
| CF `Mods/ModStructure.c` | `E1257321B4F711A72C1703319DB980CDA376C7CFC24955723720BEDA23C131A8` | parser consumer is mod inputs, not imagesets |

The 11 extracted `.imageset` files and 12 pinned custom brace sets were mechanically reopened; all contained `Groups {}` and GUID-prefixed texture references. This is an observed corpus fact, not a grammar requirement. Five StarDZ Core beta brace sets use plain texture paths, but no runtime receipt was available, so they do not prove plain-path support.

### Official web limitation

On 2026-09-14, direct retrieval of `https://community.bohemia.net/wiki/DayZ:Modding_Structure` returned HTTP 403. The search index exposed the page and exact optional `class imageSets { files[] = {...}; };` block, and the local cached text contains the full page with “last edited 3 August 2021”; the cache has no embedded capture receipt, so it is corroborating text rather than independently timestamped web provenance. No other official page was used to infer imageset grammar, EDDS creation, or runtime behavior.

## Unresolved verification gates

- Minimal custom brace fixture: config compile, PBO inventory/prefix, client load, `LoadImageFile` boolean/logs, and rendered layout/script images.
- Grammar A/B tests for omitted `Groups`, GUID-prefixed versus plain resource paths, and deliberate `RefSize`/`mpix` variants.
- Source-backed EDDS creation/import workflow before recommending a specific tool sequence.
- Workbench preview A/B test with and without a `.gproj imageSets` entry.
- Any XML test only after a documented native schema or concrete adapter is identified; do not brute-force the placeholder schema.

