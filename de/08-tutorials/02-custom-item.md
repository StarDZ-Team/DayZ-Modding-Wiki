# Kapitel 8.2: Ein eigenes Item erstellen

[Startseite](../../README.md) | [<< Zurueck: Ihre erste Mod](01-first-mod.md) | **Ein eigenes Item erstellen** | [Weiter: Ein Admin-Panel bauen >>](03-admin-panel.md)

---

## Inhaltsverzeichnis

- [Was wir bauen](#was-wir-bauen)
- [Voraussetzungen](#voraussetzungen)
- [Schritt 1: Die Item-Klasse in config.cpp definieren](#schritt-1-die-item-klasse-in-configcpp-definieren)
- [Schritt 2: Hidden Selections fuer Texturen einrichten](#schritt-2-hidden-selections-fuer-texturen-einrichten)
- [Schritt 3: Grundlegende Texturen erstellen](#schritt-3-grundlegende-texturen-erstellen)
- [Schritt 4: In types.xml fuer Server-Spawning hinzufuegen](#schritt-4-in-typesxml-fuer-server-spawning-hinzufuegen)
- [Schritt 5: Einen Anzeigenamen mit Stringtable erstellen](#schritt-5-einen-anzeigenamen-mit-stringtable-erstellen)
- [Schritt 6: Im Spiel testen](#schritt-6-im-spiel-testen)
- [Schritt 7: Feinschliff -- Modell, Texturen und Sounds](#schritt-7-feinschliff----modell-texturen-und-sounds)
- [Vollstaendige Dateireferenz](#vollstaendige-dateireferenz)
- [Fehlerbehebung](#fehlerbehebung)
- [Naechste Schritte](#naechste-schritte)

---

## Was wir bauen

Wir erstellen ein Item namens **Field Journal** -- ein kleines Notizbuch, das Spieler in der Welt finden, aufheben und in ihrem Inventar aufbewahren koennen. Es wird:

- Ein Vanilla-Modell verwenden (von einem bestehenden Item geliehen), sodass wir keine 3D-Modellierung benoetigen
- Ein eigenes retexturiertes Erscheinungsbild ueber Hidden Selections haben
- In der Spawntabelle des Servers erscheinen
- Einen korrekten Anzeigenamen und eine Beschreibung haben

Dies ist der Standard-Workflow zum Erstellen jedes Items in DayZ, sei es Nahrung, Werkzeuge, Kleidung oder Baumaterialien.

---

## Voraussetzungen

- Eine funktionierende Mod-Struktur (schliessen Sie zuerst [Kapitel 8.1](01-first-mod.md) ab)
- Ein Texteditor
- DayZ Tools installiert (fuer Texturkonvertierung, optional)

Wir bauen auf der Mod aus Kapitel 8.1 auf. Ihre aktuelle Struktur sollte so aussehen:

```
MyFirstMod/
    mod.cpp
    Scripts/
        config.cpp
        5_Mission/
            MyFirstMod/
                MissionHello.c
```

---

## Schritt 1: Die Item-Klasse in config.cpp definieren

Items in DayZ werden in der `CfgVehicles`-Config-Klasse definiert. Trotz des Namens "Vehicles" haelt diese Klasse ALLE Entitaetstypen: Items, Gebaeude, Fahrzeuge, Tiere und alles andere.

### Eine Data-config.cpp erstellen

Es ist Best Practice, Item-Definitionen in einem separaten PBO von Ihren Skripten zu halten. Erstellen Sie eine neue Ordnerstruktur:

```
MyFirstMod/
    mod.cpp
    Scripts/
        config.cpp              <-- Existiert bereits (Skripte)
    Data/
        config.cpp              <-- NEU (Item-Definitionen)
```

Erstellen Sie die Datei `MyFirstMod/Data/config.cpp` mit diesem Inhalt:

```cpp
class CfgPatches
{
    class MyFirstMod_Data
    {
        units[] = { "MFM_FieldJournal" };
        weapons[] = {};
        requiredVersion = 0.1;
        requiredAddons[] =
        {
            "DZ_Data",
            "DZ_Characters"
        };
    };
};

class CfgVehicles
{
    class Inventory_Base;

    class MFM_FieldJournal : Inventory_Base
    {
        scope = 2;
        displayName = "$STR_MFM_FieldJournal";
        descriptionShort = "$STR_MFM_FieldJournal_Desc";
        model = "\DZ\characters\accessories\data\Notebook\Notebook.p3d";
        rotationFlags = 17;
        weight = 200;
        itemSize[] = { 1, 2 };
        absorbency = 0.5;

        class DamageSystem
        {
            class GlobalHealth
            {
                class Health
                {
                    hitpoints = 100;
                    healthLevels[] =
                    {
                        { 1.0, {} },
                        { 0.7, {} },
                        { 0.5, {} },
                        { 0.3, {} },
                        { 0.0, {} }
                    };
                };
            };
        };

        hiddenSelections[] = { "camoGround" };
        hiddenSelectionsTextures[] = { "MyFirstMod\Data\Textures\field_journal_co.paa" };
    };
};
```

### Was jedes Feld bedeutet

| Feld | Wert | Erklaerung |
|-------|-------|-------------|
| `scope` | `2` | Macht das Item oeffentlich -- spawnbar und in Admin-Tools sichtbar. Verwenden Sie `0` fuer Basisklassen, die nie direkt gespawnt werden sollen. |
| `displayName` | `"$STR_MFM_FieldJournal"` | Referenziert einen Stringtable-Eintrag fuer den Itemnamen. Das `$STR_`-Praefix sagt der Engine, ihn in der `stringtable.csv` nachzuschlagen. |
| `descriptionShort` | `"$STR_MFM_FieldJournal_Desc"` | Kurzbeschreibung, die im Inventar-Tooltip angezeigt wird. |
| `model` | Pfad zur `.p3d` | Das 3D-Modell. Wir leihen das Vanilla-Notizbuch-Modell. Das `\DZ\`-Praefix referenziert Vanilla-Spieldateien. |
| `rotationFlags` | `17` | Bitmaske, die steuert, wie das Item im Inventar rotiert werden kann. `17` erlaubt Standardrotation. |
| `weight` | `200` | Gewicht in Gramm. |
| `itemSize[]` | `{ 1, 2 }` | Inventar-Rastergroesse: 1 Spalte breit, 2 Zeilen hoch. |
| `absorbency` | `0.5` | Wie stark das Item Wasser absorbiert (0 = gar nicht, 1 = vollstaendig). Beeinflusst das Item bei Regen. |
| `hiddenSelections[]` | `{ "camoGround" }` | Benannte Texturslots auf dem Modell, die ueberschrieben werden koennen. |
| `hiddenSelectionsTextures[]` | Pfad zur `.paa` | Ihre eigene Textur fuer jede Hidden Selection. |

### Ueber die Elternklasse

```cpp
class Inventory_Base;
```

Diese Zeile ist eine **Vorwaertsdeklaration**. Sie sagt dem Config-Parser, dass `Inventory_Base` existiert (sie ist im Vanilla-DayZ definiert). Ihre Item-Klasse erbt dann davon:

```cpp
class MFM_FieldJournal : Inventory_Base
```

`Inventory_Base` ist die Standard-Elternklasse fuer kleine Items, die ins Spielerinventar gehen. Andere haeufige Elternklassen:

| Elternklasse | Verwenden fuer |
|-------------|---------|
| `Inventory_Base` | Generische Inventar-Items |
| `Edible_Base` | Nahrung und Getraenke |
| `Clothing_Base` | Tragbare Kleidung/Ruestung |
| `Weapon_Base` | Feuerwaffen |
| `Magazine_Base` | Magazine und Munitionsboxen |
| `HouseNoDestruct` | Gebaeude und Strukturen |

### Ueber DamageSystem

Der `DamageSystem`-Block definiert, wie das Item Schaden nimmt und abnutzt. Das `healthLevels`-Array ordnet Gesundheitsprozente Texturzustaenden zu:

- `1.0` = makellos
- `0.7` = abgenutzt
- `0.5` = beschaedigt
- `0.3` = stark beschaedigt
- `0.0` = ruiniert

Die leeren `{}` nach jeder Stufe sind Platzhalter fuer Schadensoverlay-Texturen. Zur Vereinfachung lassen wir sie leer.

---

## Schritt 2: Hidden Selections fuer Texturen einrichten

Hidden Selections sind der Mechanismus, den DayZ verwendet, um Texturen auf einem 3D-Modell zu tauschen, ohne die Modelldatei selbst zu modifizieren. Das Vanilla-Notizbuch-Modell hat eine Hidden Selection namens `"camoGround"`, die seine Haupttextur steuert.

### Wie Hidden Selections funktionieren

1. Das 3D-Modell (`.p3d`) definiert benannte Bereiche, sogenannte **Selektionen**
2. In der config.cpp listet `hiddenSelections[]` auf, welche Selektionen Sie ueberschreiben moechten
3. `hiddenSelectionsTextures[]` stellt Ihre Ersatztexturen bereit, in passender Reihenfolge

```cpp
hiddenSelections[] = { "camoGround" };
hiddenSelectionsTextures[] = { "MyFirstMod\Data\Textures\field_journal_co.paa" };
```

Der erste Eintrag in `hiddenSelectionsTextures` ersetzt den ersten Eintrag in `hiddenSelections`. Wenn Sie mehrere Selektionen haetten:

```cpp
hiddenSelections[] = { "camoGround", "camoMale", "camoFemale" };
hiddenSelectionsTextures[] = { "pfad\tex1.paa", "pfad\tex2.paa", "pfad\tex3.paa" };
```

### Hidden-Selection-Namen finden

Um herauszufinden, welche Hidden Selections ein Vanilla-Modell unterstuetzt:

1. Oeffnen Sie **Object Builder** (aus DayZ Tools)
2. Laden Sie die `.p3d`-Modelldatei
3. Schauen Sie in die **Named Selections**-Liste
4. Selektionen, die mit `"camo"` beginnen, sind typischerweise die, die Sie ueberschreiben koennen

Alternativ schauen Sie in die Vanilla-`config.cpp` des Items, auf dem Sie Ihr Item basieren. Das `hiddenSelections[]`-Array zeigt, was verfuegbar ist.

---

## Schritt 3: Grundlegende Texturen erstellen

DayZ verwendet das `.paa`-Format fuer Texturen. Waehrend der Entwicklung koennen Sie mit einem einfachen farbigen Bild beginnen und es spaeter konvertieren.

### Den Texturordner erstellen

```
MyFirstMod/
    Data/
        config.cpp
        Textures/
            field_journal_co.paa
```

### Option A: Einen Platzhalter verwenden (am schnellsten)

Fuer erste Tests koennen Sie `hiddenSelectionsTextures` auf eine Vanilla-Textur zeigen lassen, anstatt eine eigene zu erstellen:

```cpp
hiddenSelectionsTextures[] = { "\DZ\characters\accessories\data\Notebook\notebook_co.paa" };
```

Dies verwendet die Vanilla-Notizbuch-Textur. Ihr Item sieht identisch zum Vanilla-Notizbuch aus, funktioniert aber als Ihr eigenes Item. Ersetzen Sie es durch Ihre eigene Textur, sobald Sie bestaetigt haben, dass alles funktioniert.

### Option B: Eine eigene Textur erstellen

1. **Ein Quellbild erstellen:**
   - Oeffnen Sie einen beliebigen Bildeditor (GIMP, Photoshop, Paint.NET oder sogar MS Paint)
   - Erstellen Sie ein neues Bild mit **512x512 Pixeln** (Zweierpotenzen sind erforderlich: 256, 512, 1024, 2048)
   - Fuellen Sie es mit einer Farbe oder einem Design. Fuer ein Feldtagebuch versuchen Sie ein dunkles Braun oder Gruen.
   - Speichern Sie als `.tga` (TGA-Format) oder `.png`

2. **In `.paa` konvertieren:**
   - Oeffnen Sie **TexView2** aus DayZ Tools
   - Gehen Sie zu **File > Open** und waehlen Sie Ihre `.tga` oder `.png`
   - Gehen Sie zu **File > Save As** und speichern Sie im `.paa`-Format
   - Speichern Sie nach `MyFirstMod/Data/Textures/field_journal_co.paa`

   Das `_co`-Suffix ist eine Namenskonvention fuer "Color" (die Diffuse-/Albedo-Textur). Andere Suffixe sind `_nohq` (Normal Map), `_smdi` (Specular) und `_as` (Alpha/Transparenz).

### Textur-Namenskonventionen

| Suffix | Typ | Zweck |
|--------|------|---------|
| `_co` | Farbe (Diffuse) | Die Hauptfarb-/Erscheinungstextur |
| `_nohq` | Normal Map | Oberflaechendetail und Beleuchtungsnormalen |
| `_smdi` | Specular | Glaenz- und Metalleigenschaften |
| `_as` | Alpha/Surface | Transparenz oder Oberflaechenmaskierung |
| `_de` | Detail | Zusaetzliches Detail-Overlay |

Fuer ein erstes Item benoetigen Sie nur die `_co`-Textur. Das Modell verwendet Standardwerte fuer die anderen.

---

## Schritt 4: In types.xml fuer Server-Spawning hinzufuegen

Die `types.xml`-Datei steuert, welche Items in der Welt spawnen, wie viele gleichzeitig existieren und wo sie erscheinen. Diese Datei befindet sich im **Missionsordner** des Servers (nicht in Ihrer Mod).

### types.xml finden

Fuer einen Standard-DayZ-Server befindet sich `types.xml` unter:

```
<DayZ Server>\mpmissions\dayzOffline.chernarusplus\db\types.xml
```

### Ihren Item-Eintrag hinzufuegen

Oeffnen Sie `types.xml` und fuegen Sie diesen Block innerhalb des `<types>`-Wurzelelements hinzu:

```xml
<type name="MFM_FieldJournal">
    <nominal>10</nominal>
    <lifetime>14400</lifetime>
    <restock>1800</restock>
    <min>5</min>
    <quantmin>-1</quantmin>
    <quantmax>-1</quantmax>
    <cost>100</cost>
    <flags count_in_cargo="0" count_in_hoarder="0" count_in_map="1" count_in_player="0" crafted="0" deloot="0" />
    <category name="tools" />
    <usage name="Town" />
    <usage name="Village" />
    <value name="Tier1" />
    <value name="Tier2" />
</type>
```

### Was jedes Tag bedeutet

| Tag | Wert | Erklaerung |
|-----|-------|-------------|
| `name` | `"MFM_FieldJournal"` | Muss exakt mit Ihrem config.cpp-Klassennamen uebereinstimmen |
| `nominal` | `10` | Zielanzahl dieses Items in der Welt zu jedem Zeitpunkt |
| `lifetime` | `14400` | Sekunden bevor ein fallengelassenes Item despawnt (14400 = 4 Stunden) |
| `restock` | `1800` | Sekunden zwischen Respawn-Pruefungen (1800 = 30 Minuten) |
| `min` | `5` | Minimum, das die Central Economy aufrechtzuerhalten versucht |
| `quantmin` / `quantmax` | `-1` | Mengenbereich (-1 = nicht anwendbar, verwendet fuer Items mit variabler Menge wie Wasserflaschen) |
| `cost` | `100` | Wirtschafts-Prioritaetsgewicht (hoeher = spawnt bereitwilliger) |
| `flags` | Verschiedene | Was zum Nominal-Limit zaehlt |
| `category` | `"tools"` | Item-Kategorie fuer Wirtschaftsbalancierung |
| `usage` | `"Town"`, `"Village"` | Wo das Item spawnt (Standortkategorien) |
| `value` | `"Tier1"`, `"Tier2"` | Karten-Tier-Zonen, in denen das Item erscheint |

### Haeufige usage- und value-Tags

**Usage (wo es spawnt):**
- `Town`, `Village`, `Farm`, `Industrial`, `Military`, `Hunting`, `Medical`, `Coast`, `Firefighter`, `Prison`, `Police`, `School`, `ContaminatedArea`

**Value (Karten-Tier):**
- `Tier1` -- Kueste/Startgebiete
- `Tier2` -- Inland-Staedte
- `Tier3` -- Militaer/Nordwesten
- `Tier4` -- Tiefstes Inland/Endgame

---

## Schritt 5: Einen Anzeigenamen mit Stringtable erstellen

Die Stringtable bietet lokalisierte Texte fuer Item-Namen und -Beschreibungen. DayZ liest Stringtables aus `stringtable.csv`-Dateien.

### Die Stringtable erstellen

Erstellen Sie die Datei `MyFirstMod/Data/Stringtable.csv` mit diesem Inhalt:

```csv
"Language","English","Czech","German","Russian","Polish","Hungarian","Italian","Spanish","French","Chinese","Japanese","Portuguese","ChineseSimp","Korean"
"STR_MFM_FieldJournal","Field Journal","","Feldtagebuch","","","","","","","","","","",""
"STR_MFM_FieldJournal_Desc","A weathered leather journal used to record field notes and observations.","","Ein abgenutztes Ledertagebuch zum Aufzeichnen von Feldnotizen und Beobachtungen.","","","","","","","","","","",""
```

Jede Zeile hat Spalten fuer jede unterstuetzte Sprache. Sie muessen nur die `"English"`-Spalte ausfuellen. Die anderen Spalten koennen leere Strings sein -- die Engine faellt auf Englisch zurueck, wenn eine Uebersetzung fehlt.

### Wie String-Referenzen funktionieren

In Ihrer config.cpp haben Sie geschrieben:

```cpp
displayName = "$STR_MFM_FieldJournal";
```

Das `$STR_`-Praefix sagt der Engine: "Suche einen Stringtable-Eintrag namens `STR_MFM_FieldJournal`." Die Engine durchsucht alle geladenen `Stringtable.csv`-Dateien nach einer passenden Zeile und gibt den Text fuer die Sprache des Spielers zurueck.

### CSV-Formatregeln

- Die erste Zeile muss die Kopfzeile mit Sprachnamen sein (in der exakten Reihenfolge wie oben gezeigt)
- Jede folgende Zeile ist: `"SCHLUESSEL","Englischer Text","Tschechischer Text",...`
- Alle Werte muessen in doppelten Anfuehrungszeichen stehen
- Werte durch Kommas trennen
- Kein abschliessendes Komma nach dem letzten Wert
- Als UTF-8-Kodierung speichern (wichtig fuer Nicht-ASCII-Zeichen in anderen Sprachen)

---

## Schritt 6: Im Spiel testen

### Ihre Scripts-config.cpp aktualisieren

Vor dem Testen muessen Sie Ihre `Scripts/config.cpp` aktualisieren, um auch den Data-Ordner zu packen, ODER den Data-Ordner als separates PBO packen.

**Option A: Separates PBO (empfohlen)**

Packen Sie `MyFirstMod/Data/` als zweites PBO:

```
@MyFirstMod/
    mod.cpp
    Addons/
        Scripts.pbo          <-- Enthaelt Scripts/config.cpp und 5_Mission/
        Data.pbo             <-- Enthaelt Data/config.cpp, Textures/, Stringtable.csv
```

Verwenden Sie Addon Builder mit:
- Source: `MyFirstMod/Data/`
- Prefix: `MyFirstMod/Data`

**Option B: File Patching (Entwicklung)**

Waehrend der Entwicklung mit `-filePatching` liest die Engine direkt aus Ihren Ordnern. Kein zusaetzliches PBO-Packen noetig:

```
DayZDiag_x64.exe -mod=P:\MyFirstMod -filePatching
```

### Das Item ueber die Skriptkonsole spawnen

Der schnellste Weg, Ihr Item zu testen, ohne auf natuerliches Spawnen zu warten:

1. Starten Sie DayZ mit geladener Mod
2. Treten Sie Ihrem lokalen Server bei oder starten Sie den Offline-Modus
3. Oeffnen Sie die **Skriptkonsole** (bei Verwendung von DayZDiag ist diese ueber das Debug-Menue verfuegbar)
4. Geben Sie in der Skriptkonsole ein:

```c
GetGame().GetPlayer().GetInventory().CreateInInventory("MFM_FieldJournal");
```

5. Druecken Sie **Execute** (oder den Ausfuehren-Button)

Das Item sollte im Inventar Ihres Charakters erscheinen.

### Alternative: In der Naehe des Spielers spawnen

Wenn Ihr Inventar voll ist, spawnen Sie das Item auf dem Boden neben Ihrem Charakter:

```c
vector pos = GetGame().GetPlayer().GetPosition();
GetGame().CreateObject("MFM_FieldJournal", pos, false, false, true);
```

### Was zu pruefen ist

1. **Erscheint das Item?** Wenn ja, ist die config.cpp-Klassendefinition korrekt.
2. **Hat es den richtigen Namen?** Pruefen Sie, ob "Field Journal" erscheint (nicht `$STR_MFM_FieldJournal`). Wenn Sie die rohe Stringreferenz sehen, laedt die Stringtable nicht.
3. **Hat es die richtige Textur?** Wenn Sie eine eigene Textur verwenden, ueberpruefen Sie, ob die Farben stimmen. Wenn das Item ganz weiss oder pink erscheint, ist der Texturpfad falsch.
4. **Kann man es aufheben?** Wenn das Item spawnt, aber nicht aufgehoben werden kann, pruefen Sie `itemSize` und `scope`.
5. **Sieht das Inventar-Icon korrekt aus?** Die Groesse sollte mit Ihrer `itemSize[]`-Definition uebereinstimmen.

---

## Schritt 7: Feinschliff -- Modell, Texturen und Sounds

Sobald Ihr Item mit einem geliehenen Modell funktioniert, koennen Sie es mit eigenen Assets aufwerten.

### Eigenes 3D-Modell

Das Erstellen eines eigenen `.p3d`-Modells erfordert:

1. **Blender oder 3DS Max** mit dem DayZ-Tools-Plugin (Blender ist kostenlos)
2. Das Modell als `.p3d` mit Object Builder exportieren
3. Korrekte Geometrie (visuelle Mesh), Feuergeometrie (Kollision) und View-Geometrie (LODs) definieren
4. UV-Maps fuer Ihre Texturen erstellen
5. Benannte Selektionen fuer Hidden Selections definieren

Dies ist ein erheblicher Aufwand. Fuer die meisten Items ist das Retexturieren eines Vanilla-Modells (wie wir es oben getan haben) ausreichend.

### Verbesserte Texturen

Fuer ein professionell aussehendes Item:

1. Erstellen Sie eine **2048x2048**-Textur fuer Nahdetails (oder 1024x1024 fuer kleine Items)
2. Fuegen Sie eine **Normal Map** (`_nohq.paa`) fuer Oberflaechendetails ohne zusaetzliche Polygone hinzu
3. Fuegen Sie eine **Specular Map** (`_smdi.paa`) fuer Materialeigenschaften (Glaenze, Rauheit) hinzu
4. Aktualisieren Sie Ihre Config:

```cpp
hiddenSelections[] = { "camoGround" };
hiddenSelectionsTextures[] = { "MyFirstMod\Data\Textures\field_journal_co.paa" };
hiddenSelectionsMaterials[] = { "MyFirstMod\Data\Textures\field_journal.rvmat" };
```

Eine `.rvmat`-Datei (Rvmat-Materialdatei) verbindet alle Textur-Maps:

```cpp
ambient[] = { 1.0, 1.0, 1.0, 1.0 };
diffuse[] = { 1.0, 1.0, 1.0, 1.0 };
forcedDiffuse[] = { 0.0, 0.0, 0.0, 0.0 };
emmisive[] = { 0.0, 0.0, 0.0, 0.0 };
specular[] = { 0.2, 0.2, 0.2, 1.0 };
specularPower = 40;

PixelShaderID = "NormalMap";
VertexShaderID = "NormalMap";

class Stage1
{
    texture = "MyFirstMod\Data\Textures\field_journal_nohq.paa";
    uvSource = "tex";
};

class Stage2
{
    texture = "MyFirstMod\Data\Textures\field_journal_smdi.paa";
    uvSource = "tex";
};
```

### Eigene Sounds

Um einen Sound hinzuzufuegen, wenn das Item verwendet oder aufgehoben wird:

1. Erstellen Sie eine `.ogg`-Audiodatei (OGG-Vorbis-Format, das einzige Format, das DayZ fuer eigene Sounds unterstuetzt)
2. Definieren Sie `CfgSoundShaders` und `CfgSoundSets` in Ihrer Data-config.cpp:

```cpp
class CfgSoundShaders
{
    class MFM_JournalOpen_SoundShader
    {
        samples[] = {{ "MyFirstMod\Data\Sounds\journal_open", 1 }};
        volume = 0.6;
        range = 3;
        limitation = 0;
    };
};

class CfgSoundSets
{
    class MFM_JournalOpen_SoundSet
    {
        soundShaders[] = { "MFM_JournalOpen_SoundShader" };
        volumeFactor = 1.0;
        frequencyFactor = 1.0;
        spatial = 1;
    };
};
```

Hinweis: Sounddateipfade in `samples[]` enthalten KEINE `.ogg`-Erweiterung.

### Skript-Verhalten hinzufuegen

Um Ihrem Item eigenes Verhalten zu geben (zum Beispiel eine Aktion, wenn der Spieler es verwendet), erstellen Sie eine Skriptklasse in `4_World`:

```
MyFirstMod/
    Scripts/
        config.cpp              <-- worldScriptModule-Eintrag hinzufuegen
        4_World/
            MyFirstMod/
                MFM_FieldJournal.c
        5_Mission/
            MyFirstMod/
                MissionHello.c
```

Aktualisieren Sie `Scripts/config.cpp`, um die neue Schicht einzuschliessen:

```cpp
dependencies[] = { "World", "Mission" };

class defs
{
    class worldScriptModule
    {
        value = "";
        files[] = { "MyFirstMod/Scripts/4_World" };
    };
    class missionScriptModule
    {
        value = "";
        files[] = { "MyFirstMod/Scripts/5_Mission" };
    };
};
```

Erstellen Sie `4_World/MyFirstMod/MFM_FieldJournal.c`:

```c
class MFM_FieldJournal extends Inventory_Base
{
    override bool CanPutInCargo(EntityAI parent)
    {
        if (!super.CanPutInCargo(parent))
            return false;

        return true;
    }

    override void SetActions()
    {
        super.SetActions();
        // Eigene Aktionen hier hinzufuegen
        // AddAction(ActionReadJournal);
    }

    override void OnInventoryEnter(Man player)
    {
        super.OnInventoryEnter(player);
        Print("[MyFirstMod] Spieler hat das Feldtagebuch aufgehoben!");
    }

    override void OnInventoryExit(Man player)
    {
        super.OnInventoryExit(player);
        Print("[MyFirstMod] Spieler hat das Feldtagebuch abgelegt.");
    }
};
```

---

## Vollstaendige Dateireferenz

### Endgueltige Verzeichnisstruktur

```
MyFirstMod/
    mod.cpp
    Scripts/
        config.cpp
        4_World/
            MyFirstMod/
                MFM_FieldJournal.c
        5_Mission/
            MyFirstMod/
                MissionHello.c
    Data/
        config.cpp
        Stringtable.csv
        Textures/
            field_journal_co.paa
```

Die vollstaendigen Dateiinhalte entsprechen den in den obigen Schritten gezeigten Codebeispielen.

---

## Fehlerbehebung

### Item erscheint nicht beim Spawnen ueber die Skriptkonsole

- **Klassennamen-Nichtueberereinstimmung:** Der Name im Spawn-Befehl muss exakt mit Ihrem config.cpp-Klassennamen uebereinstimmen: `"MFM_FieldJournal"` (gross-/kleinschreibungssensitiv).
- **config.cpp nicht geladen:** Pruefen Sie, ob Ihr Data-PBO gepackt und geladen ist, oder ob File Patching aktiv ist.
- **CfgPatches fehlt:** Jede config.cpp muss einen gueltigen `CfgPatches`-Block haben.

### Item-Name zeigt `$STR_MFM_FieldJournal` an (rohe Stringreferenz)

- **Stringtable nicht gefunden:** Stellen Sie sicher, dass `Stringtable.csv` im selben PBO wie die Config ist, die sie referenziert, oder im Mod-Stammverzeichnis.
- **Falscher Schluesselname:** Der Schluessel in der CSV muss exakt uebereinstimmen (ohne das `$`-Praefix): `"STR_MFM_FieldJournal"`.
- **CSV-Formatfehler:** Stellen Sie sicher, dass alle Werte in doppelten Anfuehrungszeichen stehen und die Kopfzeile korrekt ist.

### Item erscheint ganz weiss, pink oder unsichtbar

- **Texturpfad falsch:** Ueberpruefen Sie, dass `hiddenSelectionsTextures[]` auf die korrekte `.paa`-Datei zeigt. Pfade verwenden in config.cpp Backslashes.
- **Hidden-Selection-Name falsch:** Der Selektionsname muss dem entsprechen, was das Modell definiert. Pruefen Sie mit Object Builder.
- **Textur nicht im PBO:** Bei Verwendung gepackter PBOs muss die Texturdatei im PBO enthalten sein.

### Item kann nicht aufgehoben werden

- **`scope` nicht auf 2 gesetzt:** Stellen Sie sicher, dass `scope = 2;` in Ihrer Item-Klasse steht.
- **`itemSize` zu gross:** Wenn die Item-Groesse den Inventarplatz des Spielers uebersteigt, kann er es nicht aufheben.
- **Elternklasse falsch:** Stellen Sie sicher, dass Sie von `Inventory_Base` oder einer anderen gueltigen Item-Elternklasse erben.

### Item spawnt, hat aber falsche Groesse im Inventar

- **`itemSize[]`:** Die Werte sind `{ Spalten, Zeilen }`. `{ 1, 2 }` bedeutet 1 breit und 2 hoch. `{ 2, 3 }` bedeutet 2 breit und 3 hoch.

---

## Naechste Schritte

1. **[Kapitel 8.3: Ein Admin-Panel-Modul bauen](03-admin-panel.md)** -- Erstellen Sie ein UI-Panel mit Server-Client-Kommunikation.
2. **Varianten hinzufuegen** -- Erstellen Sie Farbvarianten Ihres Items mit verschiedenen Hidden-Selection-Texturen.
3. **Rezepte hinzufuegen** -- Definieren Sie Herstellungskombinationen in config.cpp mit `CfgRecipes`.
4. **Kleidung erstellen** -- Erweitern Sie `Clothing_Base` statt `Inventory_Base` fuer tragbare Items.
5. **Eine Waffe bauen** -- Erweitern Sie `Weapon_Base` fuer Feuerwaffen mit Anbauteilen und Animationen.

---

**Zurueck:** [Kapitel 8.1: Ihre erste Mod (Hello World)](01-first-mod.md)
**Weiter:** [Kapitel 8.3: Ein Admin-Panel-Modul bauen](03-admin-panel.md)
