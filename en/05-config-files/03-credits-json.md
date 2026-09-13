# Credits.json


---

> **Summary:** The `Credits.json` file defines the credits that DayZ displays for your mod in the game's mod menu. It lists team members, contributors, and acknowledgments organized by departments and sections. While purely cosmetic, it is the standard way to give credit to your development team.

---

## Table of Contents

- [Overview](#overview)
- [File Location](#file-location)
- [JSON Structure](#json-structure)
- [How DayZ Displays Credits](#how-dayz-displays-credits)
- [Using Localized Section Names](#using-localized-section-names)
- [Templates](#templates)
- [Worked Examples](#worked-examples)
- [Common Mistakes](#common-mistakes)

---

## Overview

A mod credits file is a JSON document describing departments, sections and contributor lines, rendered in the main menu's scrolling credits view --- similar to movie credits.

> **Important --- `creditsJson` is a Community Framework feature, not a vanilla one.**

Two separate things are often conflated here, and it matters for whether your credits ever appear:

- **The JSON schema** (`Departments` / `Sections` / `SectionLines`) *is* vanilla. It is defined by `JsonDataCredits`, `JsonDataCreditsDepartment` and `JsonDataCreditsSection` in `3_Game/gui/credits/`, and the vanilla `CreditsMenu` renders exactly that shape.
- **Loading a *mod's* credits file** is not vanilla. Vanilla `CreditsLoader.GetData()` loads one hard-coded path --- `scripts/data/credits.json`, the game's own credits --- and no vanilla script anywhere reads a `creditsJson` key from `CfgMods`.

The `creditsJson` key is a convention introduced by **Community Framework** (originally from DayZ SA Epoch; CF's `CreditsLoader.c` changelog credits it to AWOL, 2019-01-20). CF supplies a `modded class CreditsLoader` that walks `ModLoader.GetMods()` and a `ModStructure` that reads `CfgMods <YourMod> creditsJson` and loads that file. Without CF --- or another mod that implements the same aggregation --- declaring `creditsJson` has no effect and your credits are never shown.

So: write the JSON against the vanilla schema below, declare `creditsJson` in `CfgMods`, and treat CF (or an equivalent) as the dependency that actually makes it visible.

Declare the key in your `CfgMods` block in `config.cpp`:

```cpp
class CfgMods
{
    class MyMod
    {
        creditsJson = "MyMod/Scripts/Data/Credits.json";
    };
};
```

The file is optional. Including one is good practice: it acknowledges your team's work and gives your mod a professional appearance.

---

## File Location

Place `Credits.json` inside a `Data` subfolder of your Scripts directory, or directly in the Scripts root:

```
@MyMod/
  Addons/
    MyMod_Scripts.pbo
      Scripts/
        Data/
          Credits.json       <-- Common location
        Credits.json         <-- Also valid
```

Both locations are seen in published mods.

The file may live anywhere in the PBO. What matters is that the `creditsJson` value in your `CfgMods` block points to its exact path (case-sensitive on some platforms).

---

## JSON Structure

The file uses a straightforward JSON structure with three levels of hierarchy:

```json
{
    "Departments": [
        {
            "DepartmentName": "Department Title",
            "Sections": [
                {
                    "SectionName": "Section Title",
                    "SectionLines": ["Person 1", "Person 2"]
                }
            ]
        }
    ]
}
```

### Top-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `Departments` | array | Yes | Array of department objects |

The vanilla parser class `JsonDataCredits` (`3_Game/gui/credits/jsondatacredits.c`) declares exactly one field, `ref array<ref JsonDataCreditsDepartment> Departments`. There is no top-level `Header` field, so a `Header` key is simply not deserialized. To show a title at the top of the credits, use the first `DepartmentName` instead.

Note that Community Framework, which is what actually loads a mod's file, may rewrite your first `DepartmentName` to your mod's `name` when the two do not resemble each other (`ModStructure.LoadData()`), so do not rely on that first entry surviving verbatim.

### Department Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `DepartmentName` | string | Yes | Section header text. Can be empty `""` for visual grouping without a header. |
| `Sections` | array | Yes | Array of section objects within this department |

### Section Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `SectionName` | string | Yes | Sub-header within the department |
| `SectionLines` | array of strings | Yes | List of contributor names or text lines |

The vanilla section class `JsonDataCreditsSection` (`3_Game/gui/credits/jsondatacreditssection.c`) declares exactly two fields, `string SectionName` and `ref array<string> SectionLines`. You may see some mods use a `Names` key, but there is no such field to deserialize into --- it renders nothing. Always use `SectionLines` for the list of names.

---

## How DayZ Displays Credits

The credits display follows this visual hierarchy:

```
╔══════════════════════════════════╗
║     DEPARTMENT NAME              ║  <-- DepartmentName (medium, centered)
║                                  ║
║     Section Name                 ║  <-- SectionName (small, centered)
║     Person 1                     ║  <-- SectionLines (list)
║     Person 2                     ║
║     Person 3                     ║
║                                  ║
║     Another Section              ║
║     Person A                     ║
║     Person B                     ║
║                                  ║
║     ANOTHER DEPARTMENT           ║
║     ...                          ║
╚══════════════════════════════════╝
```

- Each `DepartmentName` acts as a major section divider
- Each `SectionName` acts as a sub-heading
- `SectionLines` scroll vertically in the credits view

### Empty Strings for Spacing

An empty `DepartmentName` or `SectionName` is handled explicitly: the element hides both its title widget and its separator panel rather than drawing an empty heading. That makes empty names a reliable spacing device. Combine them with whitespace-only entries in `SectionLines`:

```json
{
    "DepartmentName": "",
    "Sections": [{
        "SectionName": "",
        "SectionLines": ["           "]
    }]
}
```

This is a common trick for controlling visual layout in the credits scroll.

---

## Using Localized Section Names

Section names can reference stringtable keys using the `#` prefix, just like UI text:

```json
{
    "SectionName": "#STR_LNT_CREDITS_SCRIPTERS",
    "SectionLines": ["Firefly", "Wick"]
}
```

Every credits string --- department title, section title, and each `SectionLines` entry --- reaches the screen through `TextWidget.SetText()` (`CreditsDepartmentElement` / `CreditsDepartmentSection` in `5_Mission/gui/newui/credits/elements/`). So a `#`-prefixed value gets exactly the same handling any other widget text does; vanilla's own `credits.json` does not use stringtable keys, so verify the result in-game rather than assuming. If you want a guaranteed resolved string, you cannot intervene here --- the JSON is passed straight through.

Department names can also use stringtable references:

```json
{
    "DepartmentName": "#legal_notices",
    "Sections": [...]
}
```

---

## Templates

### Solo Developer

```json
{
    "Departments": [
        {
            "DepartmentName": "My Awesome Mod",
            "Sections": [
                {
                    "SectionName": "Developer",
                    "SectionLines": ["YourName"]
                }
            ]
        }
    ]
}
```

### Small Team

```json
{
    "Departments": [
        {
            "DepartmentName": "My Mod",
            "Sections": [
                {
                    "SectionName": "Developers",
                    "SectionLines": ["Lead Dev", "Co-Developer"]
                },
                {
                    "SectionName": "3D Artists",
                    "SectionLines": ["Modeler1", "Modeler2"]
                },
                {
                    "SectionName": "Translators",
                    "SectionLines": [
                        "Translator1 (French)",
                        "Translator2 (German)",
                        "Translator3 (Russian)"
                    ]
                }
            ]
        }
    ]
}
```

### Full Professional Structure

```json
{
    "Departments": [
        {
            "DepartmentName": "My Big Mod",
            "Sections": [
                {
                    "SectionName": "Lead Developer",
                    "SectionLines": ["ProjectLead"]
                },
                {
                    "SectionName": "Scripters",
                    "SectionLines": ["Dev1", "Dev2", "Dev3"]
                },
                {
                    "SectionName": "3D Artists",
                    "SectionLines": ["Artist1", "Artist2"]
                },
                {
                    "SectionName": "Mapping",
                    "SectionLines": ["Mapper1"]
                }
            ]
        },
        {
            "DepartmentName": "Community",
            "Sections": [
                {
                    "SectionName": "Translators",
                    "SectionLines": [
                        "Translator1 (Czech)",
                        "Translator2 (German)",
                        "Translator3 (Russian)"
                    ]
                },
                {
                    "SectionName": "Testers",
                    "SectionLines": ["Tester1", "Tester2", "Tester3"]
                }
            ]
        },
        {
            "DepartmentName": "Legal Notices",
            "Sections": [
                {
                    "SectionName": "Licenses",
                    "SectionLines": [
                        "Font Awesome - CC BY 4.0 License",
                        "Some assets licensed under ADPL-SA"
                    ]
                }
            ]
        }
    ]
}
```

---

## Worked Examples

The two examples below use **Lantern**, the fictional framework this wiki builds throughout its chapters, and **NightPatrol**, a small companion content mod. All names are invented for teaching -- swap in your own team.

### Lantern Core

A complete multi-department credits file for a framework-style mod. It combines every technique from this chapter: localized section names via stringtable references, an empty-string spacer department between major blocks, and a legal notices department at the end:

```json
{
    "Departments": [
        {
            "DepartmentName": "Lantern Core",
            "Sections": [
                {
                    "SectionName": "#STR_LNT_CREDITS_SCRIPTERS",
                    "SectionLines": ["Firefly", "Wick"]
                },
                {
                    "SectionName": "#STR_LNT_CREDITS_ARTISTS",
                    "SectionLines": ["Glowworm", "Tinder"]
                }
            ]
        },
        {
            "DepartmentName": "",
            "Sections": [
                {
                    "SectionName": "",
                    "SectionLines": ["           "]
                }
            ]
        },
        {
            "DepartmentName": "Community",
            "Sections": [
                {
                    "SectionName": "Translators",
                    "SectionLines": [
                        "Lampe (French)",
                        "Laterne (German)",
                        "Lucerna (Czech)"
                    ]
                },
                {
                    "SectionName": "Testers",
                    "SectionLines": ["Beacon", "Ember", "Spark"]
                }
            ]
        },
        {
            "DepartmentName": "Legal Notices",
            "Sections": [
                {
                    "SectionName": "Licenses",
                    "SectionLines": [
                        "Icon set - CC BY 4.0 License"
                    ]
                }
            ]
        }
    ]
}
```

Notable points:

- The first `DepartmentName` ("Lantern Core") doubles as the credits title, matching the mod's `name` in `CfgMods`.
- The `#STR_LNT_*` section names resolve through the stringtable, so a French player sees "Scripteurs" while a German player sees "Skripter" -- useful when the mod itself ships in multiple languages.
- The empty department between "Lantern Core" and "Community" is pure spacing: an empty `DepartmentName`, an empty `SectionName`, and a whitespace-only line render as a visual gap in the scroll.
- Legal notices get their own department so license attributions do not mix with contributor names.

### NightPatrol

A minimal single-department file for a small content mod -- one department, one section, done:

```json
{
    "Departments": [
        {
            "DepartmentName": "NightPatrol",
            "Sections": [
                {
                    "SectionName": "Developers",
                    "SectionLines": ["Firefly", "Moth"]
                }
            ]
        }
    ]
}
```

Most mods need nothing more than this. Add departments only when the list of contributors grows large enough to need grouping.

---

## Common Mistakes

### Invalid JSON Syntax

The most common issue. JSON is strict about:
- **Trailing commas**: `["a", "b",]` is invalid JSON (the trailing comma after `"b"`)
- **Single quotes**: Use `"double quotes"`, not `'single quotes'`
- **Unquoted keys**: `DepartmentName` must be `"DepartmentName"`

Use a JSON validator before shipping.

### Path Mismatch Between `creditsJson` and the Actual File

There is no required file name. The loader takes whatever string you put in `creditsJson` and passes it straight to `JsonFileLoader.LoadFile()`, so the only requirement is that the two match. `Credits.json` is simply the community convention --- Community Framework, Community Online Tools, DayZ-Expansion, Dabs Framework and the DayZ SampleMod all happen to use that name, at differing paths.

The realistic failure is a typo or a case difference between the `creditsJson` value and the packed path. A mismatch produces no credits and no crash.

### Using the `Names` Key

Some mods write a `Names` array, but `JsonDataCreditsSection` has no such field, so it is never deserialized. Only `SectionLines` is parsed:

```json
{
    "SectionName": "Developers",
    "Names": ["Dev1"]
}
```

In this example, "Dev1" never appears in-game --- the section renders empty. Always list contributors under `SectionLines`.

### Encoding Issues

Save the file as UTF-8. Non-ASCII characters (accented names, CJK characters) require UTF-8 encoding to display correctly in-game.

---

## Best Practices

- Validate your JSON with an external tool before packing into a PBO. Community Framework does surface a load failure, but only as a `CF_Log.Warn` line naming the path and the serializer's error message -- easy to miss unless you are reading the log.
- Use `SectionLines` for every name list. It is the only list field the schema defines.
- Include a "Legal Notices" department if your mod bundles third-party assets (fonts, icons, sounds) with attribution requirements.
- Use the first `DepartmentName` as a title matching your mod's `name` in `mod.cpp` and `config.cpp` for a consistent identity.
- Use empty `DepartmentName` and `SectionName` strings sparingly for visual spacing -- overuse makes credits look fragmented.

---

## Compatibility & Impact

- **Multi-Mod:** Each mod points `creditsJson` at its own file, so there is no file-level collision. Community Framework concatenates every mod's `Departments` into one list for the single credits screen, in `ModLoader.GetMods()` order, and appends the DayZ game credits after them --- so your entry's position depends on load order, not on anything you control.
- **Performance:** Credits are parsed when the mod list is built and rendered when the player opens the Credits screen, never during gameplay. File size has no impact on gameplay performance.
