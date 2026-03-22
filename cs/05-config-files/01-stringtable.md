# Chapter 5.1: stringtable.csv --- Localization

[Domů](../../README.md) | **stringtable.csv** | [Další: inputs.xml >>](02-inputs-xml.md)

---

> **Shrnutí:** The `stringtable.csv` file provides lokálníized text for your DayZ mod. Engine reads this CSV při startu and resolves translation keys based on hráč's language setting. Every user-facing string --- UI labels, input binding names, item descriptions, notification text --- should live in řetězectable spíše než being hardcoded.

---

## Obsah

- [Overview](#overview)
- [CSV Format](#csv-format)
- [Column Reference](#column-reference)
- [Key Naming Convention](#key-naming-convention)
- [Referencing Strings](#referencing-strings)
- [Creating a New Stringtable](#creating-a-new-stringtable)
- [Empty Cell Handling and Fallback Behavior](#empty-cell-handling-and-fallback-behavior)
- [Multi-Language Workflow](#multi-language-workflow)
- [Modular Stringtable Approach (DayZ Expansion)](#modular-stringtable-approach-dayz-expansion)
- [Real Examples](#real-examples)
- [Běžné Mistakes](#common-mistakes)

---

## Přehled

DayZ uses a CSV-based lokálníization system. When engine encounters řetězec key prefixed with `#` (například, `#STR_MYMOD_HELLO`), it looks up that key in all loaded stringtable files and vrací translation matching hráč's current language. If no match is found for the active language, engine falls back through a defined chain.

The stringtable file must be named exactly `stringtable.csv` and placed inside your mod's PBO structure. Engine discovers it automatickýally --- no config.cpp registration je povinný.

---

## Formát CSV

The file is a standard comma-separated values file with quoted fields. The first row is the header, and každý subsequent row defines one translation key.

### Řádek záhlaví

Řádek záhlaví definuje sloupce. DayZ rozpoznává až 15 sloupců:

```csv
"Language","original","english","czech","german","russian","polish","hungarian","italian","spanish","french","chinese","japanese","portuguese","chinesesimp",
```

### Datové řádky

Each row starts with řetězec key (no `#` prefix in the CSV), followed by the translation for každý language:

```csv
"STR_MYMOD_HELLO","Hello World","Hello World","Ahoj světe","Hallo Welt","Привет мир","Witaj świecie","Helló világ","Ciao mondo","Hola mundo","Bonjour le monde","你好世界","ハローワールド","Olá mundo","你好世界",
```

### Koncová čárka

Mnoho souborů stringtable obsahuje koncovou čárku za posledním sloupcem. Toto je konvenční a bezpečné --- engine tolerates it.

### Pravidla uvozovek

- Fields **must** be quoted with double quotes if they contain commas, novýlines, or double quotes.
- V praxi většina mods quote každý field for consistency.
- Some mods (like MyMod Missions) omit quotes celýly; engine handles oba styles as long as the field content ne contain commas.

---

## Reference sloupců

DayZ supports 13 player-selectable languages. The CSV has 15 columns protože the first column is klíč name and the second is the `original` column (the mod author's native language or výchozí text).

| # | Column Name | Language | Notes |
|---|-------------|----------|-------|
| 1 | `Language` | --- | The string key identifier (e.g. `STR_MYMOD_HELLO`) |
| 2 | `original` | Author's native | Fallback of last resort; used if no jiný column matches |
| 3 | `english` | English | Most common primary language for international mods |
| 4 | `czech` | Czech | |
| 5 | `german` | German | |
| 6 | `russian` | Russian | |
| 7 | `polish` | Polish | |
| 8 | `hungarian` | Hungarian | |
| 9 | `italian` | Italian | |
| 10 | `spanish` | Spanish | |
| 11 | `french` | French | |
| 12 | `chinese` | Chinese (Traditional) | Traditional Chinese characters |
| 13 | `japanese` | Japanese | |
| 14 | `portuguese` | Portuguese | |
| 15 | `chinesesimp` | Chinese (Simplified) | Simplified Chinese characters |

### Na pořadí sloupců záleží

Engine identifies columns by their **header name**, not by position. Nicméně following the standard order shown výše is strongly doporučený for compatibility and readability.

### Volitelné sloupce

You ne need to include all 15 columns. Pokud váš mod pouze supports English, můžete use a minimal header:

```csv
"Language","english"
"STR_MYMOD_HELLO","Hello World"
```

Some mods add non-standard columns like `korean` (MyMod Missions does this). Engine ignores columns it ne recognize as a podporovaný language, but those columns can serve as documentation or preparation for future language support.

---

## Konvence pojmenování klíčů

Klíče řetězců sledují hierarchický vzor pojmenování:

```
STR_MODNAME_CATEGORY_ELEMENT
```

### Pravidla

1. **Vždy start with `STR_`** --- this is a universal DayZ convention
2. **Mod prefix** --- uniquely identifies your mod (e.g., `MYMOD`, `COT`, `EXPANSION`, `VPP`)
3. **Category** --- groups related strings (e.g., `INPUT`, `TAB`, `CONFIG`, `DIR`)
4. **Element** --- the specifický string (e.g., `ADMIN_PANEL`, `NORTH`, `SAVE`)
5. **Use UPPERCASE** --- the convention across all major mods
6. **Use underscores** as separators, nikdy spaces or hyphens

### Příklady z reálných modů

```
STR_MYMOD_INPUT_ADMIN_PANEL       -- MyMod: keybinding label
STR_MYMOD_CLOSE                   -- MyMod: generic "Close" button
STR_MYMOD_DIR_NORTH                  -- MyMod: compass direction
STR_MYMOD_TAB_ONLINE                 -- MyMod: admin panel tab name
STR_COT_ESP_MODULE_NAME            -- COT: module display name
STR_COT_CAMERA_MODULE_BLUR         -- COT: camera tool label
STR_EXPANSION_ATM                  -- Expansion: feature name
STR_EXPANSION_AI_COMMAND_MENU      -- Expansion: input label
```

### Anti-vzory

```
STR_hello_world          -- Bad: lowercase, no mod prefix
MY_STRING                -- Bad: missing STR_ prefix
STR_MYMOD Hello World    -- Bad: spaces in key
```

---

## Odkazování na řetězce

Existují three distinct contexts where you reference lokálníized strings, and každý uses a slightly odlišný syntax.

### V souborech layoutu (.layout)

Use the `#` prefix before klíč name. Engine resolves it at widget creation time.

```
TextWidgetClass MyLabel {
 text "#STR_MYMOD_CLOSE"
 size 100 30
}
```

The `#` prefix tells the layout parser "this is a lokálníization key, not literal text."

### V Enforce Script (soubory .c)

Use `Widget.TranslateString()` to resolve klíč za běhu. The `#` prefix je povinný in the argument.

```c
string translated = Widget.TranslateString("#STR_MYMOD_CLOSE");
// translated == "Close" (if player language is English)
// translated == "Fechar" (if player language is Portuguese)
```

You can také set widget text přímo:

```c
TextWidget label = TextWidget.Cast(layoutRoot.FindAnyWidget("MyLabel"));
label.SetText(Widget.TranslateString("#STR_MYMOD_ADMIN_PANEL"));
```

Or use string keys přímo in widget text properties, and engine resolves them:

```c
label.SetText("#STR_MYMOD_ADMIN_PANEL");  // Also works -- engine auto-resolves
```

### V inputs.xml

Use the `loc` atribut **bez** `#` předpony.

```xml
<input name="UAMyAction" loc="STR_MYMOD_INPUT_MY_ACTION" />
```

Toto je one place where you omit the `#`. The input system adds it interníly.

### Shrnutí Table

| Context | Syntax | Example |
|---------|--------|---------|
| Layout file `text` attribute | `#STR_KEY` | `text "#STR_MYMOD_CLOSE"` |
| Script `TranslateString()` | `"#STR_KEY"` | `Widget.TranslateString("#STR_MYMOD_CLOSE")` |
| Script widget text | `"#STR_KEY"` | `label.SetText("#STR_MYMOD_CLOSE")` |
| inputs.xml `loc` attribute | `STR_KEY` (no #) | `loc="STR_MYMOD_INPUT_ADMIN_PANEL"` |

---

## Vytvoření nové stringtable

### Step 1: Vytvořte the File

Vytvořte `stringtable.csv` at the root of your mod's PBO content directory. Engine scans all loaded PBOs for files named exactly `stringtable.csv`.

Typical placement:

```
@MyMod/
  Addons/
    MyMod_Scripts.pbo
      config.cpp
      stringtable.csv        <-- Here
      Scripts/
        3_Game/
        4_World/
        5_Mission/
```

### Step 2: Zapište the Header

Spusťte with the plný 15-column header:

```csv
"Language","original","english","czech","german","russian","polish","hungarian","italian","spanish","french","chinese","japanese","portuguese","chinesesimp",
```

### Step 3: Přidejte Your Strings

Přidejte one row per translatable string. Spusťte with English, fill in jiný languages as translations become dostupný:

```csv
"Language","original","english","czech","german","russian","polish","hungarian","italian","spanish","french","chinese","japanese","portuguese","chinesesimp",
"STR_MYMOD_TITLE","My Cool Mod","My Cool Mod","","","","","","","","","","","","",
"STR_MYMOD_OPEN","Open","Open","Otevřít","Öffnen","Открыть","Otwórz","Megnyitás","Apri","Abrir","Ouvrir","打开","開く","Abrir","打开",
```

### Krok 4: Zabalení a testování

Sestavte your PBO. Spusťte the game. Ověřte that `Widget.TranslateString("#STR_MYMOD_TITLE")` returns "My Cool Mod" in your script logs. Change the game language in settings to verify fallback behavior.

---

## Zpracování prázdných buněk a záložní chování

When engine looks up řetězec key for hráč's current language and finds an prázdný cell, it follows a fallback chain:

1. **Player's selected language column** --- zkontrolován jako první
2. **`english` column** --- if hráč's language cell is prázdný
3. **`original` column** --- if `english` is také prázdný
4. **Raw key name** --- if all columns are prázdný, engine displays klíč itself (e.g., `STR_MYMOD_TITLE`)

To znamená, you může bezpečně leave non-English columns prázdný during development. English-speaking hráči viz the `english` column, and jiný hráči viz the English fallback until a proper translation is added.

### Praktický důsledek

You ne need to copy the English text into každý column as a placeholder. Leave untranslated cells prázdný:

```csv
"STR_MYMOD_HELLO","Hello","Hello","","","","","","","","","","","","",
```

Players whose language is German will viz "Hello" (anglickou zálohu) dokud nebude poskytnuta German překlad.

---

## Pracovní postup pro více jazyků

### Pro samostatné vývojáře

1. Zapište all strings in English (both `original` and `english` columns).
2. Release the mod. English serves as the universal fallback.
3. As community members volunteer translations, fill in additional columns.
4. Rebuild and release updates.

### Pro týmy s překladateli

1. Maintain the CSV in a shared repository or spreadsheet.
2. Assign one translator per language.
3. Use the `original` column for the author's native language (e.g., Portuguese for Brazilian developers).
4. The `english` column is vždy filled --- it is the international baseline.
5. Use a diff přílišl to track which keys have been added since the last translation pass.

### Použití tabulkového softwaru

CSV files open naturally in Excel, Google Sheets, or LibreOffice Calc. Be aware of these pitfalls:

- **Excel may add BOM (Byte Order Mark)** to UTF-8 files. DayZ handles BOM, but it can cause issues with některé přílišls. Uložte as "CSV UTF-8" to be safe.
- **Excel auto-formatting** can mangle fields that look like dates or numbers.
- **Line endings**: DayZ accepts oba `\r\n` (Windows) and `\n` (Unix).

---

## Modulární přístup ke stringtable (DayZ Expansion)

DayZ Expansion demonstrates a osvědčený postup for large mods: splitting translations across více stringtable files organized by feature module. Their structure uses 20 oddělený stringtable files inside a `languagecore` directory:

```
DayZExpansion/
  languagecore/
    AI/stringtable.csv
    BaseBuilding/stringtable.csv
    Book/stringtable.csv
    Chat/stringtable.csv
    Core/stringtable.csv
    Garage/stringtable.csv
    Groups/stringtable.csv
    Hardline/stringtable.csv
    Licensed/stringtable.csv
    Main/stringtable.csv
    MapAssets/stringtable.csv
    Market/stringtable.csv
    Missions/stringtable.csv
    Navigation/stringtable.csv
    PersonalStorage/stringtable.csv
    PlayerList/stringtable.csv
    Quests/stringtable.csv
    SpawnSelection/stringtable.csv
    Vehicles/stringtable.csv
    Weapons/stringtable.csv
```

### Proč rozdělit?

- **Manageability**: A jeden stringtable for a large mod can grow to thousands of lines. Splitting by feature module makes každý file manageable.
- **Independent updates**: Translators can work on one module at a time without merge conflicts.
- **Conditional inclusion**: Each sub-mod's PBO pouze includes řetězectable for its own feature, keeping PBO sizes smaller.

### Jak to funguje

Engine scans každý loaded PBO for `stringtable.csv`. Protože každý Expansion sub-module is packed into its own PBO, každý one naturally includes pouze its own stringtable. No special configuration is needed --- jen name soubor `stringtable.csv` and place it inside the PBO.

Key names stále use a globální prefix (`STR_EXPANSION_`) to avoid collisions.

---

## Reálné příklady

### MyMod Core

MyMod Core uses the plný 15-column format with Portuguese as the `original` language (the development team's native language) and comprehensive translations for all 13 podporovaný languages:

```csv
"Language","original","english","czech","german","russian","polish","hungarian","italian","spanish","french","chinese","japanese","portuguese","chinesesimp",
"STR_MYMOD_INPUT_GROUP","MyMod","MyMod","MyMod","MyMod","MyMod","MyMod","MyMod","MyMod","MyMod","MyMod","MyMod","MyMod","MyMod","MyMod",
"STR_MYMOD_INPUT_ADMIN_PANEL","Painel Admin","Open Admin Panel","Otevřít Admin Panel","Admin-Panel öffnen","Открыть Админ Панель","Otwórz Panel Admina","Admin Panel megnyitása","Apri Pannello Admin","Abrir Panel Admin","Ouvrir le Panneau Admin","打开管理面板","管理パネルを開く","Abrir Painel Admin","打开管理面板",
"STR_MYMOD_CLOSE","Fechar","Close","Zavřít","Schließen","Закрыть","Zamknij","Bezárás","Chiudi","Cerrar","Fermer","关闭","閉じる","Fechar","关闭",
"STR_MYMOD_SAVE","Salvar","Save","Uložit","Speichern","Сохранить","Zapisz","Mentés","Salva","Guardar","Sauvegarder","保存","保存","Salvar","保存",
```

Notable patterns:
- `original` contains Portuguese text (the team's native language)
- `english` is vždy filled as the international baseline
- All 13 language columns are populated

### COT (Community Online Tools)

COT uses the stejný 15-column format. Its keys follow the `STR_COT_MODULE_CATEGORY_ELEMENT` pattern:

```csv
Language,original,english,czech,german,russian,polish,hungarian,italian,spanish,french,chinese,japanese,portuguese,chinesesimp,
STR_COT_CAMERA_MODULE_BLUR,Blur:,Blur:,Rozmazání:,Weichzeichner:,Размытие:,Rozmycie:,Elmosódás:,Sfocatura:,Desenfoque:,Flou:,模糊:,ぼかし:,Desfoque:,模糊:,
STR_COT_ESP_MODULE_NAME,Camera Tools,Camera Tools,Nástroje kamery,Kamera-Werkzeuge,Камера,Narzędzia Kamery,Kamera Eszközök,Strumenti Camera,Herramientas de Cámara,Outils Caméra,相機工具,カメラツール,Ferramentas da Câmera,相机工具,
```

### VPP Admin Tools

VPP uses a reduced column set (13 columns, no `hungarian` column) and ne prefix keys with `STR_`:

```csv
"Language","original","english","czech","german","russian","polish","italian","spanish","french","chinese","japanese","portuguese","chinesesimp"
"vpp_focus_on_game","[Hold/2xTap] Focus On Game","[Hold/2xTap] Focus On Game","...","...","...","...","...","...","...","...","...","...","..."
```

This demonstrates that the `STR_` prefix is a convention, not a requirement. Nicméně omitting it means můžetenot use the `#` prefix resolution in layout files. VPP references these keys pouze through script code. The `STR_` prefix is strongly doporučený for all nový mods.

### MyMod Missions

MyMod Missions uses an unquoted, headerless-style CSV (no quotes around fields) with an extra `Korean` column:

```csv
Language,English,Czech,German,Russian,Polish,Hungarian,Italian,Spanish,French,Chinese,Japanese,Portuguese,Korean
STR_MYMOD_MISSION_AVAILABLE,MISSION AVAILABLE,MISE K DISPOZICI,MISSION VERFÜGBAR,МИССИЯ ДОСТУПНА,...
```

Notable: the `original` column is absent, and `Korean` is added as an extra language. Engine ignores unrecognized column names, so `Korean` serves as documentation until official Korean support is added.

---

## Časté chyby

### Zapomenutí předpony `#` ve skriptech

```c
// WRONG -- displays the raw key, not the translation
label.SetText("STR_MYMOD_HELLO");

// CORRECT
label.SetText("#STR_MYMOD_HELLO");
```

### Použití `#` v inputs.xml

```xml
<!-- WRONG -- the input system adds # internally -->
<input name="UAMyAction" loc="#STR_MYMOD_MY_ACTION" />

<!-- CORRECT -->
<input name="UAMyAction" loc="STR_MYMOD_MY_ACTION" />
```

### Duplicitní klíče mezi mody

Pokud dva mods define `STR_CLOSE`, engine uses whichever PBO loads last. Vždy use your mod prefix:

```csv
"STR_MYMOD_CLOSE","Close","Close",...
```

### Nesouhlasící počet sloupců

Pokud row has fewer columns than the header, engine may tiše skip it or assign prázdný strings to the chybějící columns. Vždy ensure každý row has the stejný number of fields as the header.

### Problémy s BOM

Some text editors insert a UTF-8 BOM (byte order mark) at the start of soubor. This can cause the first key in the CSV to be tiše broken. Pokud váš first string key nikdy resolves, check for and remove the BOM.

### Použití čárek v neuvedených polích

```csv
STR_MYMOD_MSG,Hello, World,Hello, World,...
```

This breaks parsing protože `Hello` and ` World` are read as oddělený columns. Either quote the field or avoid commas in values:

```csv
"STR_MYMOD_MSG","Hello, World","Hello, World",...
```

---

## Osvědčené postupy

- Vždy use the `STR_MODNAME_` prefix for každý key. This prevents collisions when více mods are loaded together.
- Quote každý field in the CSV, dokonce if the content has no commas. This prevents subtle parsing errors when translations in jiný languages contain commas or special characters.
- Fill the `english` column for každý key, dokonce if your native language is odlišný. English is the universal fallback and the baseline for community translators.
- Udržujte one stringtable per PBO for small mods. For large mods with 500+ keys, split into per-feature stringtable files in oddělený PBOs (following the Expansion pattern).
- Uložte files as UTF-8 without BOM. If using Excel, explicitly choose "CSV UTF-8" format on export.

---

## Teorie vs praxe

> What the documentation says versus how things actually work za běhu.

| Concept | Theory | Reality |
|---------|--------|---------|
| Column order ne matter | Engine identifies columns by header name | True, but některé community přílišls and spreadsheet exports reorder columns. Keeping the standard order prevents confusion |
| Fallback chain: language > english > original > raw key | Documented cascade | If oba `english` and `original` are prázdný, engine displays the raw key with the `#` prefix stripped -- užitečný for spotting chybějící translations ve hře |
| `Widget.TranslateString()` | Resolves at call time | The result is cached per session. Changing the game language requires a restart for stringtable lookups to update |
| Multiple mods with stejný key | Last-loaded PBO wins | PBO pořadí načítání is not guaranteed mezi mods. Pokud dva mods define `STR_CLOSE`, the displayed text depends on which mod loads last -- vždy use a mod prefix |
| `#` prefix in `SetText()` | Engine auto-resolves lokálníization keys | Works, but pouze on the first call. Pokud call `SetText("#STR_KEY")` and later call `SetText("literal text")`, switching back to `SetText("#STR_KEY")` works fine -- no caching issue at the widget level |

---

## Kompatibilita a dopad

- **Více modů:** String key collisions are the primary risk. Two mods defining `STR_ADMIN_PANEL` will conflict tiše. Vždy prefix keys with your mod name (`STR_MYMOD_ADMIN_PANEL`).
- **Výkon:** Stringtable lookup is fast (hash-based). Having thousands of keys across více mods has no measurable performance impact. The celý stringtable is loaded into memory při startu.
- **Verze:** The CSV-based stringtable format has been unchanged since DayZ Standalone alpha. The 15-column layout and fallback behavior have remained stable across all versions.
