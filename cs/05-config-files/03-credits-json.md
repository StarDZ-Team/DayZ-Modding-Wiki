# Chapter 5.3: Credits.json

[Domů](../../README.md) | [<< Předchozí: inputs.xml](02-inputs-xml.md) | **Credits.json** | [Další: Formát ImageSet >>](04-imagesets.md)

---

> **Shrnutí:** The `Credits.json` file defines the credits that DayZ displays for your mod in the game's mod menu. It lists team members, contributors, and acknowledgments organized by departments and sections. Zatímco purely cosmetic, it is the standard way to give credit to your development team.

---

## Obsah

- [Overview](#overview)
- [File Location](#file-location)
- [JSON Structure](#json-structure)
- [How DayZ Displays Credits](#how-dayz-displays-credits)
- [Using Localized Section Names](#using-lokálníized-section-names)
- [Templates](#templates)
- [Real Examples](#real-examples)
- [Běžné Mistakes](#common-mistakes)

---

## Přehled

When hráč selects your mod in the DayZ launcher or ve hře mod menu, engine looks for a `Credits.json` file inside your mod's PBO. If found, the credits are displayed in a scrolling view organized into departments and sections --- similar to movie credits.

Soubor je volitelný. If absent, no credits section appears for your mod. But including one is good practice: it acknowledges your team's work and gives your mod a professional appearance.

---

## Umístění souboru

Place `Credits.json` inside a `Data` subfolder of your Scripts directory, or přímo in the Scripts root:

```
@MyMod/
  Addons/
    MyMod_Scripts.pbo
      Scripts/
        Data/
          Credits.json       <-- Common location (COT, Expansion, DayZ Editor)
        Credits.json         <-- Also valid (DabsFramework, Colorful-UI)
```

Obě umístění fungují. Engine scans the PBO contents for a file named `Credits.json` (case-sensitive on některé platforms).

---

## Struktura JSON

Soubor používá přímočarou strukturu JSON se třemi úrovněmi hierarchie:

```json
{
    "Header": "My Mod Name",
    "Departments": [
        {
            "DepartmentName": "Department Title",
            "Sections": [
                {
                    "SectionName": "Section Title",
                    "Names": ["Person 1", "Person 2"]
                }
            ]
        }
    ]
}
```

### Pole nejvyšší úrovně

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `Header` | string | No | Main title displayed at the top of the credits. If omitted, no header is shown. |
| `Departments` | array | Yes | Array of department objects |

### Objekt oddělení

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `DepartmentName` | string | Yes | Section header text. Can be prázdný `""` for visual grouping without a header. |
| `Sections` | array | Yes | Array of section objects within this department |

### Objekt sekce

Two variants exist in the wild for listing names. Engine supports oba.

**Variant 1: `Names` array** (used by MyMod Core)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `SectionName` | string | Yes | Sub-header within the department |
| `Names` | array of strings | Yes | List of contributor names |

**Variant 2: `SectionLines` array** (used by COT, Expansion, DabsFramework)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `SectionName` | string | Yes | Sub-header within the department |
| `SectionLines` | array of strings | Yes | List of contributor names or text lines |

Oba `Names` and `SectionLines` serve the stejný purpose. Use whichever you prefer --- engine renders them identicky.

---

## Jak DayZ zobrazuje titulky

Zobrazení titulků sleduje tuto vizuální hierarchii:

```
╔══════════════════════════════════╗
║         MY MOD NAME              ║  <-- Header (large, centered)
║                                  ║
║     DEPARTMENT NAME              ║  <-- DepartmentName (medium, centered)
║                                  ║
║     Section Name                 ║  <-- SectionName (small, centered)
║     Person 1                     ║  <-- Names/SectionLines (list)
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

- The `Header` appears once at the top
- Každý `DepartmentName` funguje jako hlavní oddělovač sekcí
- Každý `SectionName` funguje jako podnadpis
- Jména se rolují vertikálně v zobrazení titulků

### Prázdné řetězce pro odsazení

Expansion uses prázdný `DepartmentName` and `SectionName` strings, plus whitespace-only entries in `SectionLines`, to create visual spacing:

```json
{
    "DepartmentName": "",
    "Sections": [{
        "SectionName": "",
        "SectionLines": ["           "]
    }]
}
```

This is běžný trick for controlling visual layout in the credits scroll.

---

## Použití lokalizovaných názvů sekcí

Názvy sekcí mohou odkazovat na klíče stringtable pomocí `#` prefix, jen like UI text:

```json
{
    "SectionName": "#STR_EXPANSION_CREDITS_SCRIPTERS",
    "SectionLines": ["Steve aka Salutesh", "LieutenantMaster"]
}
```

When engine renders this, it resolves `#STR_EXPANSION_CREDITS_SCRIPTERS` to the lokálníized text matching hráč's language. This is užitečný if your mod supports více languages and chcete the credits section headers to be translated.

Department names can také use stringtable references:

```json
{
    "DepartmentName": "#legal_notices",
    "Sections": [...]
}
```

---

## Šablony

### Samostatný vývojář

```json
{
    "Header": "My Awesome Mod",
    "Departments": [
        {
            "DepartmentName": "Development",
            "Sections": [
                {
                    "SectionName": "Developer",
                    "Names": ["YourName"]
                }
            ]
        }
    ]
}
```

### Malý tým

```json
{
    "Header": "My Mod",
    "Departments": [
        {
            "DepartmentName": "Development",
            "Sections": [
                {
                    "SectionName": "Developers",
                    "Names": ["Lead Dev", "Co-Developer"]
                },
                {
                    "SectionName": "3D Artists",
                    "Names": ["Modeler1", "Modeler2"]
                },
                {
                    "SectionName": "Translators",
                    "Names": [
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

### Plná profesionální struktura

```json
{
    "Header": "My Big Mod",
    "Departments": [
        {
            "DepartmentName": "Core Team",
            "Sections": [
                {
                    "SectionName": "Lead Developer",
                    "Names": ["ProjectLead"]
                },
                {
                    "SectionName": "Scripters",
                    "Names": ["Dev1", "Dev2", "Dev3"]
                },
                {
                    "SectionName": "3D Artists",
                    "Names": ["Artist1", "Artist2"]
                },
                {
                    "SectionName": "Mapping",
                    "Names": ["Mapper1"]
                }
            ]
        },
        {
            "DepartmentName": "Community",
            "Sections": [
                {
                    "SectionName": "Translators",
                    "Names": [
                        "Translator1 (Czech)",
                        "Translator2 (German)",
                        "Translator3 (Russian)"
                    ]
                },
                {
                    "SectionName": "Testers",
                    "Names": ["Tester1", "Tester2", "Tester3"]
                }
            ]
        },
        {
            "DepartmentName": "Legal Notices",
            "Sections": [
                {
                    "SectionName": "Licenses",
                    "Names": [
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

## Reálné příklady

### MyMod Core

A minimal but complete credits file using the `Names` variant:

```json
{
    "Header": "MyMod Core",
    "Departments": [
        {
            "DepartmentName": "Development",
            "Sections": [
                {
                    "SectionName": "Framework",
                    "Names": ["Documentation Team"]
                }
            ]
        }
    ]
}
```

### Community Online Tools (COT)

Uses the `SectionLines` variant with více sections and acknowledgments:

```json
{
    "Departments": [
        {
            "DepartmentName": "Community Online Tools",
            "Sections": [
                {
                    "SectionName": "Active Developers",
                    "SectionLines": [
                        "LieutenantMaster",
                        "LAVA (liquidrock)"
                    ]
                },
                {
                    "SectionName": "Inactive Developers",
                    "SectionLines": [
                        "Jacob_Mango",
                        "Arkensor",
                        "DannyDog68",
                        "Thurston",
                        "GrosTon1"
                    ]
                },
                {
                    "SectionName": "Thank you to the following communities",
                    "SectionLines": [
                        "PIPSI.NET AU/NZ",
                        "1SKGaming",
                        "AWG",
                        "Expansion Mod Team",
                        "Bohemia Interactive"
                    ]
                }
            ]
        }
    ]
}
```

Notable: COT omits the `Header` field celýly. The mod name comes from jiný metadata (config.cpp `CfgMods`).

### DabsFramework

```json
{
    "Departments": [{
        "DepartmentName": "Development",
        "Sections": [{
                "SectionName": "Developers",
                "SectionLines": [
                    "InclementDab",
                    "Gormirn"
                ]
            },
            {
                "SectionName": "Translators",
                "SectionLines": [
                    "InclementDab",
                    "DanceOfJesus (French)",
                    "MarioE (Spanish)",
                    "Dubinek (Czech)",
                    "Steve AKA Salutesh (German)",
                    "Yuki (Russian)",
                    ".magik34 (Polish)",
                    "Daze (Hungarian)"
                ]
            }
        ]
    }]
}
```

### DayZ Expansion

Expansion demonstrates the většina sophisticated use of Credits.json, including:
- Localized section names viřetězectable references (`#STR_EXPANSION_CREDITS_SCRIPTERS`)
- Legal notices as a oddělený department
- Empty department and section names for visual spacing
- A supporters list with dozens of names

---

## Časté chyby

### Neplatná syntaxe JSON

Nejčastější problém. JSON je přísný ohledně:
- **Trailing commas**: `["a", "b",]` is neplatný JSON (the trailing comma after `"b"`)
- **Single quotes**: Use `"double quotes"`, not `'single quotes'`
- **Unquoted keys**: `DepartmentName` musí být `"DepartmentName"`

Před distribucí použijte platnýátor JSON.

### Špatný název souboru

The file musí být named exactly `Credits.json` (capital C). Na souborových systémech citlivých na velikost písmen, `credits.json` or `CREDITS.JSON` nebude nalezen.

### Míchání Names a SectionLines

V rámci a jeden section, use one or the jiný:

```json
{
    "SectionName": "Developers",
    "Names": ["Dev1"],
    "SectionLines": ["Dev2"]
}
```

This is ambiguous. Pick one format and use it konzistentně throughout soubor.

### Problémy s kódováním

Uložte soubor jako UTF-8. Non-ASCII characters (accented names, CJK characters) require UTF-8 encoding to display správně ve hře.

---

## Osvědčené postupy

- Validate your JSON with an externí přílišl before packing into a PBO -- engine gives no užitečný error message for malformed JSON.
- Use the `SectionLines` variant pro konzistenci, protože je to formát používaný COT, Expansion a DabsFramework.
- Zahrňte a "Legal Notices" department if your mod bundles od třetích stran assets (fonts, icons, sounds) with attribution requirements.
- Udržujte the `Header` field matching your mod's `name` in `mod.cpp` and `config.cpp` for a consistent identity.
- Use prázdný `DepartmentName` and `SectionName` strings sparingly for visual spacing -- overuse makes credits look fragmented.

---

## Kompatibilita a dopad

- **Více modů:** Each mod has its own nezávislý `Credits.json`. There is no risk of collision -- engine reads soubor from within každý mod's PBO samostatně.
- **Výkon:** Credits are loaded pouze when hráč opens the mod details screen. File size has no impact on gameplay performance.
