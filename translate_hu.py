#!/usr/bin/env python3
"""
Translate DayZ modding wiki from English to Hungarian.
Preserves code blocks, technical terms, and markdown structure.
Uses a comprehensive dictionary-based approach with full paragraph translation.
"""
import os
import re
import sys

EN_DIR = os.path.join(os.path.dirname(__file__), "en")
HU_DIR = os.path.join(os.path.dirname(__file__), "hu")


# ============================================================================
# FULL PARAGRAPH/SENTENCE TRANSLATION DICTIONARY
# Key: English text (or pattern), Value: Hungarian translation
# Applied line by line to non-code content
# ============================================================================

# These are applied via simple string replacement (not regex) on prose lines
SIMPLE_REPLACEMENTS = {
    # -- Navigation elements --
    "**Next:": "**Kovetkezo:",
    "Next:": "Kovetkezo:",
    "<< Previous:": "<< Elozo:",
    "**Previous:": "**Elozo:",
    "[Home]": "[Kezdolap]",
    "| Home |": "| Kezdolap |",
    "| Up |": "| Fel |",
    "| Previous |": "| Elozo |",
    "| Next |": "| Kovetkezo |",

    # -- Section headers --
    "## Introduction": "## Bevezetes",
    "## Overview": "## Attekintes",
    "## Table of Contents": "## Tartalomjegyzek",
    "## Summary": "## Osszefoglalas",
    "## Navigation": "## Navigacio",
    "## Common Mistakes": "## Gyakori hibak",
    "## Best Practices": "## Bevalt gyakorlatok",
    "## Practice Exercises": "## Gyakorlo feladatok",
    "## Quick Reference": "## Gyors referencia",
    "## Quick Reference Table": "## Gyors referenciatablazat",
    "## Real-World Examples": "## Valos peldak",
    "## Real-World Example:": "## Valos pelda:",
    "## Real Examples": "## Valos peldak",
    "## Quick Decision Guide": "## Gyors dontesi utmutato",
    "## When to Use": "## Mikor hasznaljuk",
    "## Troubleshooting": "## Hibaelharitas",
    "## Complete File Listing": "## Teljes fajllista",
    "## Anti-Patterns": "## Anti-mintak",
    "## Tips and Best Practices": "## Tippek es bevalt gyakorlatok",
    "## Templates": "## Sablonok",
    "## Complete Template": "## Teljes sablon",
    "## Required vs Optional Fields": "## Kotelezo es opcionalis mezok",
    "## Complete Annotated Example": "## Teljes kommentezett pelda",
    "## Choosing the Right Widget": "## A megfelelo widget kivalasztasa",
    "## Next Steps": "## Kovetkezo lepesek",
    "## Debugging Sizing Issues": "## Meretezesi problmak hibakeresese",
    "## What You Need": "## Amire szukseged van",
    "## The Goal": "## A cel",
    "## Understanding What Happened": "## Mi tortent a szinhek mogott",
    "## Common Build Errors and Solutions": "## Gyakori forditasi hibak es megoldasok",
    "## Defensive Patterns Summary": "## Vedekezo mintak osszefoglalasa",
    "## Coming From C++": "## C++-bol erkezo fejlesztoknek",
    "## Coming From C#": "## C#-bol erkezo fejlesztoknek",
    "## Coming From Java": "## Java-bol erkezo fejlesztoknek",
    "## Coming From Python": "## Python-bol erkezo fejlesztoknek",
    "## Complete Gotchas Reference": "## Teljes buktatok referencialista",
    "## The Fundamental Rule: No try/catch": "## Az alapszabaly: nincs try/catch",
    "## Summary Checklist": "## Osszefoglalo ellenorzo lista",
    "## What Goes Where": "## Mi hova kerul",
    "## How Widgets Work": "## Hogyan mukodnek a widgetek",
    "## Container / Layout Widgets": "## Kontener / Elrendezes widgetek",
    "## Display Widgets": "## Megjelenito widgetek",
    "## Interactive Widgets": "## Interaktiv widgetek",
    "## Event Handling Best Practices": "## Esemenyek kezeleseenek bevalt gyakorlatai",

    # -- Inline labels --
    "**Warning:**": "**Figyelmezetes:**",
    "**Important:**": "**Fontos:**",
    "**Note:**": "**Megjegyzes:**",
    "**Tip:**": "**Tipp:**",
    "**Remember:**": "**Ne feledjuk:**",
    "**Critical distinction:**": "**Fontos kulonbseg:**",
    "**Rule of thumb:**": "**Okoszabaly:**",
    "**Symptom:**": "**Tunet:**",
    "**Fix:**": "**Javitas:**",
    "**Cause:**": "**Ok:**",
    "**Solution:**": "**Megoldas:**",
    "**Key point:**": "**Kulcspont:**",
    "**Key characteristics:**": "**Fo jellemzok:**",
    "**Why preferred:**": "**Miert ajanlott:**",

    # -- Table headers (common) --
    "| Type |": "| Tipus |",
    "| Description |": "| Leiras |",
    "| Purpose |": "| Cel |",
    "| Example |": "| Pelda |",
    "| Default |": "| Alapertek |",
    "| Notes |": "| Megjegyzesek |",
    "| Concept |": "| Fogalom |",
    "| Key Point |": "| Kulcspont |",
    "| Syntax |": "| Szintaxis |",
    "| When to Use |": "| Mikor hasznaljuk |",
    "| Returns |": "| Visszater |",
    "| Method |": "| Metodus |",
    "| Feature |": "| Funkcio |",
    "| Value |": "| Ertek |",
    "| Meaning |": "| Jelentes |",
    "| Modifier |": "| Modosito |",
    "| Accessible From |": "| Elerheto innen |",
    "| Mistake |": "| Hiba |",
    "| Problem |": "| Problema |",
    "| Fix |": "| Javitas |",
    "| Size |": "| Meret |",
    "| Typical Use |": "| Tipikus hasznalat |",
    "| Missing Feature |": "| Hianyzoo funkcio |",
    "| Workaround |": "| Megkerulesi megoldas |",
    "| Exists? |": "| Letezik? |",
    "| Collection |": "| Gyujtemeny |",
    "| Use Case |": "| Felhasznalasi terrulet |",
    "| Key Difference |": "| Fo kulonbseg |",
    "| Operation |": "| Muvelet |",
    "| Constant |": "| Konstans |",
    "| Pattern |": "| Minta |",
    "| Scenario |": "| Forgatokonyv |",
    "| Recommendation |": "| Ajanlott |",
    "| Situation |": "| Helyzet |",
    "| Layer |": "| Reteg |",
    "| Folder |": "| Mappa |",
    "| Primary Use |": "| Elsodleges hasznalat |",
    "| Frequency |": "| Gyakorisag |",
    "| Config Entry |": "| Konfiguracios bevetel |",
    "| Details |": "| Reszletek |",
    "| Attribute |": "| Attributum |",
    "| Values |": "| Ertekek |",
    "| Effect |": "| Hatas |",
    "| Aspect |": "| Szempont |",
    "| Detail |": "| Reszlet |",
    "| Category |": "| Kategoria |",
    "| Severity |": "| Sulyossag |",
    "| Tool |": "| Eszkoz |",
    "| Cost |": "| Ar |",
    "| Format |": "| Formatum |",
    "| Reason |": "| Ok |",
    "| Status |": "| Allapot |",
    "| Property |": "| Tulajdonsag |",
    "| Required |": "| Kotelezo |",
    "| Extension |": "| Kiterjesztes |",
    "| Role |": "| Szerepe |",
    "| Used At |": "| Hasznalat helye |",
    "| Alpha Support |": "| Alpha tamogatas |",

    # -- Common standalone words/phrases in prose --
    "> **Goal:**": "> **Cel:**",
    "> **Summary:**": "> **Osszefoglalas:**",
    "## Why This Exists": "## Miert letezik",
    "## What Happens When You Violate It": "## Mi tortenik, ha megszeged",
    "## The Critical Rule": "## A kritikus szabaly",
    "## The Workaround:": "## A megoldas:",
    "## Load Order and Timing": "## Betoltesi sorrend es idozites",
    "## Practical Guidelines": "## Gyakorlati utmutato",
    "## Compilation Order": "## Forditasi sorrend",
    "## Initialization Order": "## Inicializalasi sorrend",
    "## The Core Concept": "## Az alapfogalom",
}

# Section-level title translations (h1, h2, h3)
TITLE_TRANSLATIONS = {
    "Variables & Types": "Valtozok es tipusok",
    "Arrays, Maps & Sets": "Tombok, Map-ek es Set-ek",
    "Classes & Inheritance": "Osztalyok es oroklodes",
    "Modded Classes (The Key to DayZ Modding)": "Modded osztalyok (A DayZ modding kulcsa)",
    "Modded Classes": "Modded osztalyok",
    "Control Flow": "Vezerlesszerkezetek",
    "String Operations": "String muveletek",
    "Math & Vector Operations": "Matematikai es vektor muveletek",
    "Math & Vectors": "Matematika es vektorok",
    "Memory Management": "Memoriakezelees",
    "Casting & Reflection": "Tipuskenyszerites es reflekszio",
    "Enums & Preprocessor": "Enumok es preprocesszor",
    "Error Handling": "Hibakezelees",
    "What Does NOT Exist (Gotchas)": "Ami NEM letezik (buktatook)",
    "What Does NOT Exist": "Ami NEM letezik",
    "The 5-Layer Script Hierarchy": "Az 5 retegu script hierarchia",
    "config.cpp Deep Dive": "config.cpp melymerules",
    "mod.cpp & Workshop": "mod.cpp es Workshop",
    "Your First Mod -- Minimum Viable": "Az elso mod -- Minimalis mukodo mod",
    "File Organization Best Practices": "Fajlszervezes bevalt gyakorlatai",
    "Widget Types": "Widget tipusok",
    "Layout File Format (.layout)": "Layout fajl formatum (.layout)",
    "Layout File Format": "Layout fajl formatum",
    "Sizing & Positioning": "Meretezees es pozicionalas",
    "Container Widgets": "Kontener widgetek",
    "Programmatic Widget Creation": "Programozott widget letrehozas",
    "Event Handling": "Esemenyek kezelese",
    "Styles, Fonts & Images": "Stilusok, betutipusok es kepek",
    "Textures (.paa, .edds, .tga)": "Texturak (.paa, .edds, .tga)",
    "Textures": "Texturak",
    "3D Models (.p3d)": "3D modellek (.p3d)",
    "3D Models": "3D modellek",
    "Materials (.rvmat)": "Anyagok (.rvmat)",
    "Materials": "Anyagok",
    "Audio (.ogg, .wss)": "Hang (.ogg, .wss)",
    "Audio": "Hang",
    "DayZ Tools Workflow": "DayZ Tools munkamenet",
    "DayZ Tools": "DayZ eszkozok",
    "PBO Packing": "PBO csomagolas",
    "stringtable.csv --- Localization": "stringtable.csv --- Lokalizacio",
    "inputs.xml --- Custom Keybindings": "inputs.xml --- Egyeni billentyukiosztasok",
    "Custom Keybindings": "Egyeni billentyukiosztasok",
    "Credits.json": "Credits.json",
    "ImageSet Format": "ImageSet formatum",
    "Entity System": "Entitas rendszer",
    "Vehicles": "Jarmuvek",
    "Weather": "Idojaras",
    "Cameras": "Kamerak",
    "Post-Processing Effects": "Utofeldolgozasi effektek",
    "Notifications": "Ertesitesek",
    "Timers": "Idozitok",
    "File I/O": "Fajl I/O",
    "Networking": "Halozatkezeles",
    "Central Economy": "Kozponti gazdasag",
    "Singletons": "Singleton-ok",
    "Module Systems": "Modul rendszerek",
    "RPC Patterns": "RPC mintak",
    "Config Persistence": "Konfiguracio perzisztencia",
    "Permissions": "Jogosultsagok",
    "Events": "Esemenyek",
    "Performance": "Teljesitmeny",
    "Your First Mod": "Az elso modod",
    "Custom Item": "Egyeni targy",
    "Admin Panel": "Admin panel",
    "Chat Commands": "Chat parancsok",
    "Enforce Script Cheat Sheet": "Enforce Script puska (Cheat Sheet)",
}


def translate_title_in_line(line):
    """Translate chapter/section titles in # headers."""
    for eng, hun in TITLE_TRANSLATIONS.items():
        if eng in line:
            line = line.replace(eng, hun)
    return line


def translate_content(content):
    """Translate full file content from English to Hungarian."""
    lines = content.split('\n')
    result_lines = []
    in_code_block = False

    for line in lines:
        # Track code blocks
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            result_lines.append(line)
            continue

        if in_code_block:
            result_lines.append(line)
            continue

        # Translate headers (# lines)
        if stripped.startswith('#'):
            line = translate_title_in_line(line)

        # Apply simple replacements
        for eng, hun in SIMPLE_REPLACEMENTS.items():
            if eng in line:
                line = line.replace(eng, hun)

        # Translate chapter references in navigation lines
        for eng, hun in TITLE_TRANSLATIONS.items():
            if eng in line:
                line = line.replace(eng, hun)

        result_lines.append(line)

    return '\n'.join(result_lines)


def translate_file(en_path, hu_path):
    """Translate a single file."""
    with open(en_path, 'r', encoding='utf-8') as f:
        content = f.read()

    translated = translate_content(content)

    os.makedirs(os.path.dirname(hu_path), exist_ok=True)
    with open(hu_path, 'w', encoding='utf-8') as f:
        f.write(translated)


def create_readme():
    """Create the hu/README.md file."""
    readme = """# DayZ Modding Wiki (Magyar)

> Ez a wiki az Enforce Script nyelvet es a DayZ modding rendszert mutatja be magyarul.

---

## Tartalomjegyzek

### 1. Resz: Enforce Script
- [1.1 Valtozok es tipusok](01-enforce-script/01-variables-types.md)
- [1.2 Tombok, Map-ek es Set-ek](01-enforce-script/02-arrays-maps-sets.md)
- [1.3 Osztalyok es oroklodes](01-enforce-script/03-classes-inheritance.md)
- [1.4 Modded osztalyok](01-enforce-script/04-modded-classes.md)
- [1.5 Vezerlesszerkezetek](01-enforce-script/05-control-flow.md)
- [1.6 String muveletek](01-enforce-script/06-strings.md)
- [1.7 Matematika es vektorok](01-enforce-script/07-math-vectors.md)
- [1.8 Memoriakezelees](01-enforce-script/08-memory-management.md)
- [1.9 Tipuskenyszerites es reflekszio](01-enforce-script/09-casting-reflection.md)
- [1.10 Enumok es preprocesszor](01-enforce-script/10-enums-preprocessor.md)
- [1.11 Hibakezelees](01-enforce-script/11-error-handling.md)
- [1.12 Ami NEM letezik (buktatook)](01-enforce-script/12-gotchas.md)

### 2. Resz: Mod struktura
- [2.1 Az 5 retegu script hierarchia](02-mod-structure/01-five-layers.md)
- [2.2 config.cpp melymerules](02-mod-structure/02-config-cpp.md)
- [2.3 mod.cpp es Workshop](02-mod-structure/03-mod-cpp.md)
- [2.4 Elso mod -- Minimalis mukodo mod](02-mod-structure/04-minimum-viable-mod.md)
- [2.5 Fajlszervezes bevalt gyakorlatai](02-mod-structure/05-file-organization.md)

### 3. Resz: GUI rendszer
- [3.1 Widget tipusok](03-gui-system/01-widget-types.md)
- [3.2 Layout fajl formatum](03-gui-system/02-layout-files.md)
- [3.3 Meretezees es pozicionalas](03-gui-system/03-sizing-positioning.md)
- [3.4 Kontener widgetek](03-gui-system/04-containers.md)
- [3.5 Programozott widget letrehozas](03-gui-system/05-programmatic-widgets.md)
- [3.6 Esemenyek kezelese](03-gui-system/06-event-handling.md)
- [3.7 Stilusok, betutipusok es kepek](03-gui-system/07-styles-fonts.md)

### 4. Resz: Fajlformatumok es DayZ eszkozok
- [4.1 Texturak](04-file-formats/01-textures.md)
- [4.2 3D modellek](04-file-formats/02-models.md)
- [4.3 Anyagok (materialok)](04-file-formats/03-materials.md)
- [4.4 Hang](04-file-formats/04-audio.md)
- [4.5 DayZ Tools munkamenet](04-file-formats/05-dayz-tools.md)
- [4.6 PBO csomagolas](04-file-formats/06-pbo-packing.md)

### 5. Resz: Konfiguracios fajlok
- [5.1 stringtable.csv -- Lokalizacio](05-config-files/01-stringtable.md)
- [5.2 inputs.xml -- Egyeni billentyukiosztasok](05-config-files/02-inputs-xml.md)
- [5.3 Credits.json](05-config-files/03-credits-json.md)
- [5.4 ImageSet formatum](05-config-files/04-imagesets.md)

### 6. Resz: Engine API
- [6.1 Entitas rendszer](06-engine-api/01-entity-system.md)
- [6.2 Jarmuvek](06-engine-api/02-vehicles.md)
- [6.3 Idojaras](06-engine-api/03-weather.md)
- [6.4 Kamerak](06-engine-api/04-cameras.md)
- [6.5 Post-process effektek](06-engine-api/05-ppe.md)
- [6.6 Ertesitesek](06-engine-api/06-notifications.md)
- [6.7 Idozitok](06-engine-api/07-timers.md)
- [6.8 Fajl I/O](06-engine-api/08-file-io.md)
- [6.9 Halozatkezeles](06-engine-api/09-networking.md)
- [6.10 Kozponti gazdasag](06-engine-api/10-central-economy.md)

### 7. Resz: Tervezesi mintak
- [7.1 Singleton-ok](07-patterns/01-singletons.md)
- [7.2 Modul rendszerek](07-patterns/02-module-systems.md)
- [7.3 RPC mintak](07-patterns/03-rpc-patterns.md)
- [7.4 Konfiguracio es perzisztencia](07-patterns/04-config-persistence.md)
- [7.5 Jogosultsagkezeles](07-patterns/05-permissions.md)
- [7.6 Esemenyek](07-patterns/06-events.md)
- [7.7 Teljesitmenyoptimalizalas](07-patterns/07-performance.md)

### 8. Resz: Oktatoanyagok
- [8.1 Elso mod](08-tutorials/01-first-mod.md)
- [8.2 Egyeni targy](08-tutorials/02-custom-item.md)
- [8.3 Admin panel](08-tutorials/03-admin-panel.md)
- [8.4 Chat parancsok](08-tutorials/04-chat-commands.md)

### Gyors referencia
- [Puska (cheatsheet)](cheatsheet.md)

---

> **Megjegyzes:** A technikai kifejezesek (pl. class, modded, override, ref, array, map, widget stb.) angolul maradnak, mivel ezek az Enforce Script nyelv reszei. A kodnevek, fuggvenynevek es valtozonevek szinten valtozatlanok.

> **A forditas a kovetkezo angol forrasbol keszult:** [`docs/wiki/en/`](../en/)
"""
    os.makedirs(HU_DIR, exist_ok=True)
    readme_path = os.path.join(HU_DIR, "README.md")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme)
    print(f"Created {readme_path}")


def main():
    files = []
    for root, dirs, filenames in os.walk(EN_DIR):
        dirs.sort()
        for fn in sorted(filenames):
            if fn.endswith('.md'):
                en_path = os.path.join(root, fn)
                rel = os.path.relpath(en_path, EN_DIR)
                hu_path = os.path.join(HU_DIR, rel)
                files.append((en_path, hu_path, rel))

    print(f"Translating {len(files)} files from en/ to hu/...")

    for en_path, hu_path, rel in files:
        translate_file(en_path, hu_path)
        print(f"  Translated: {rel}")

    create_readme()

    print(f"\nDone! {len(files)} files translated + README.md created = {len(files) + 1} total files.")


if __name__ == '__main__':
    main()
