# Config Persistence

> **Summary:** How to save and load mod configuration data — JSON serialization with `JsonFileLoader`, raw file I/O with `FileHandle` and `FPrintln`, versioned auto-migration, directory management, and auto-save timers.

---

## Introduction

Almost every DayZ mod needs to save and load configuration data: server settings, spawn tables, ban lists, player data, teleport locations. The engine provides `JsonFileLoader` for simple JSON serialization and raw file I/O (`FileHandle`, `FPrintln`) for everything else. Professional mods layer config versioning and auto-migration on top.

This chapter covers the standard patterns for config persistence, from basic JSON load/save through versioned migration systems, directory management, and auto-save timers.

This chapter covers reflected JSON configuration and explicit file I/O. It does not cover the ordered `ParamsWriteContext` / `ParamsReadContext` stream used by entity `OnStoreSave()` and `OnStoreLoad()` callbacks; see [Entity System](../06-engine-api/01-entity-system.md#entity-persistence-callbacks).

---

## Table of Contents

- [JsonFileLoader Pattern](#jsonfileloader-pattern)
- [Manual JSON Writing (FPrintln)](#manual-json-writing-fprintln)
- [The $profile Path](#the-profile-path)
- [Directory Creation](#directory-creation)
- [Config Data Classes](#config-data-classes)
- [Config Versioning and Migration](#config-versioning-and-migration)
- [Auto-Save Timers](#auto-save-timers)
- [Common Mistakes](#common-mistakes)
- [Best Practices](#best-practices)

---

## JsonFileLoader Pattern

`JsonFileLoader` is the engine's built-in serializer. It converts between Enforce Script objects and JSON files using reflection --- it reads the public fields of your class and maps them to JSON keys automatically.

### Two APIs: Prefer LoadFile/SaveFile, Not the Legacy JsonLoadFile/JsonSaveFile

`JsonFileLoader<T>` actually exposes two generations of the same operation, and the vanilla source itself marks the older pair as superseded (`jsonfileloader.c`, comments directly above each: *"use JsonFileLoader::LoadFile instead"* / *"use JsonFileLoader::SaveFile instead"*):

| Method | Returns | Notes |
|--------|---------|-------|
| `static bool LoadFile(string filename, out T data, out string errorMessage)` | `bool` | **Modern, preferred.** Tells you whether the load succeeded and gives you an error string when it did not. |
| `static bool SaveFile(string filename, T data, out string errorMessage)` | `bool` | **Modern, preferred.** Same success/error reporting for saves. |
| `static void JsonLoadFile(string filename, out T data)` | `void` | Legacy. No success/failure signal at all -- see the gotcha below. |
| `static void JsonSaveFile(string filename, T data)` | `void` | Legacy. Same limitation for saves. |

Prefer `LoadFile`/`SaveFile` in new code -- they give you a real `bool` result plus an error message, which sidesteps the entire gotcha this section used to have to work around. The legacy `JsonLoadFile`/`JsonSaveFile` still work and appear throughout older mods and this chapter's examples, so the gotcha below still matters when you touch that code.

### Critical Gotcha (Legacy API Only)

**`JsonFileLoader<T>.JsonLoadFile()` and `JsonFileLoader<T>.JsonSaveFile()` return `void`.** You cannot check their return value. You cannot assign them to a `bool`. You cannot use them in an `if` condition. This is one of the most common mistakes in DayZ modding -- and the reason the modern `LoadFile`/`SaveFile` pair above exists.

```c
// WRONG — will not compile
bool success = JsonFileLoader<MyConfig>.JsonLoadFile(path, config);

// WRONG — will not compile
if (JsonFileLoader<MyConfig>.JsonLoadFile(path, config))
{
    // ...
}

// WORKAROUND with the legacy API — call and then check the object state
JsonFileLoader<MyConfig>.JsonLoadFile(path, config);
// Check if the data was actually populated
if (config.m_ServerName != "")
{
    // Data loaded successfully
}

// BETTER — switch to the modern API and get a real result
string error;
if (!JsonFileLoader<MyConfig>.LoadFile(path, config, error))
{
    Print("Config load failed: " + error);
}
```

### Basic Load/Save

```c
// Data class — public fields are serialized to/from JSON
class ServerSettings
{
    string ServerName = "My DayZ Server";
    int MaxPlayers = 60;
    float RestartInterval = 14400.0;
    bool PvPEnabled = true;
};

class SettingsManager
{
    private static const string SETTINGS_PATH = "$profile:MyMod/ServerSettings.json";
    protected ref ServerSettings m_Settings;

    void Load()
    {
        m_Settings = new ServerSettings();

        if (FileExist(SETTINGS_PATH))
        {
            JsonFileLoader<ServerSettings>.JsonLoadFile(SETTINGS_PATH, m_Settings);
        }
        else
        {
            // First run: save defaults
            Save();
        }
    }

    void Save()
    {
        JsonFileLoader<ServerSettings>.JsonSaveFile(SETTINGS_PATH, m_Settings);
    }
};
```

### What Gets Serialized

`JsonFileLoader` serializes **all public fields** of the object. It does not serialize:
- Private or protected fields
- Methods
- Static fields
- Transient/runtime-only fields (there is no `[NonSerialized]` attribute --- use access modifiers)

The resulting JSON looks like:

```json
{
    "ServerName": "My DayZ Server",
    "MaxPlayers": 60,
    "RestartInterval": 14400.0,
    "PvPEnabled": true
}
```

### Supported Field Types

| Type | JSON Representation |
|------|-------------------|
| `int` | Number |
| `float` | Number |
| `bool` | `true` / `false` |
| `string` | String |
| `vector` | Array of 3 numbers |
| `array<T>` | JSON array |
| `map<K, T>` | JSON object (`K` may be `string`, `int`, or an `enum`; JSON renders all keys as strings) |
| Nested class | Nested JSON object |

### Nested Objects

```c
class SpawnPoint
{
    string Name;
    vector Position;
    float Radius;
};

class SpawnConfig
{
    ref array<ref SpawnPoint> SpawnPoints = new array<ref SpawnPoint>();
};
```

Produces:

```json
{
    "SpawnPoints": [
        {
            "Name": "Coast",
            "Position": [13000, 0, 3500],
            "Radius": 100.0
        },
        {
            "Name": "Airfield",
            "Position": [4500, 0, 9500],
            "Radius": 50.0
        }
    ]
}
```

---

## Manual JSON Writing (FPrintln)

Sometimes `JsonFileLoader` is not flexible enough: it cannot handle arrays of mixed types, custom formatting, or non-class data structures. In those cases, use raw file I/O.

### Basic Pattern

```c
void WriteCustomData(string path, array<string> lines)
{
    FileHandle file = OpenFile(path, FileMode.WRITE);
    if (!file) return;

    FPrintln(file, "{");
    FPrintln(file, "    \"entries\": [");

    for (int i = 0; i < lines.Count(); i++)
    {
        string comma = "";
        if (i < lines.Count() - 1) comma = ",";
        FPrintln(file, "        \"" + lines[i] + "\"" + comma);
    }

    FPrintln(file, "    ]");
    FPrintln(file, "}");

    CloseFile(file);
}
```

### Reading Raw Files

```c
void ReadCustomData(string path)
{
    FileHandle file = OpenFile(path, FileMode.READ);
    if (!file) return;

    string line;
    while (FGets(file, line) >= 0)
    {
        line = line.Trim();
        if (line == "") continue;
        // Process line...
    }

    CloseFile(file);
}
```

### When to Use Manual I/O

- Writing log files (append mode)
- Writing CSV or plain-text exports
- Custom JSON formatting that `JsonFileLoader` cannot produce
- Parsing non-JSON file formats (e.g., DayZ's `.map` or `.xml` files)

For standard config files, prefer `JsonFileLoader`. It is faster to implement, less error-prone, and automatically handles nested objects.

---

## The $profile Path

DayZ provides the `$profile:` path prefix, which resolves to the server's profile directory (typically the folder containing `DayZServer_x64.exe`, or the profile path specified with `-profiles=`).

```c
// These resolve to the profile directory:
"$profile:MyMod/config.json"       // → C:/DayZServer/MyMod/config.json
"$profile:MyMod/Players/data.json" // → C:/DayZServer/MyMod/Players/data.json
```

### Always Use $profile

Never use absolute paths. Never use relative paths. Always use `$profile:` for any file your mod creates or reads at runtime:

```c
// BAD: Absolute path — breaks on any other machine
const string CONFIG_PATH = "C:/DayZServer/MyMod/config.json";

// BAD: Relative path — depends on working directory, which varies
const string CONFIG_PATH = "MyMod/config.json";

// GOOD: $profile resolves correctly everywhere
const string CONFIG_PATH = "$profile:MyMod/config.json";
```

### Conventional Directory Structure

Most mods follow this convention:

```
$profile:
  └── YourModName/
      ├── Config.json          (main server config)
      ├── Permissions.json     (admin permissions)
      ├── Logs/
      │   └── 2025-01-15.log   (daily log files)
      └── Players/
          ├── 76561198xxxxx.json
          └── 76561198yyyyy.json
```

---

## Directory Creation

Before writing a file, you must ensure its parent directory exists. DayZ does not auto-create directories.

### MakeDirectory

```c
void EnsureDirectories()
{
    string baseDir = "$profile:MyMod";
    if (!FileExist(baseDir))
    {
        MakeDirectory(baseDir);
    }

    string playersDir = baseDir + "/Players";
    if (!FileExist(playersDir))
    {
        MakeDirectory(playersDir);
    }

    string logsDir = baseDir + "/Logs";
    if (!FileExist(logsDir))
    {
        MakeDirectory(logsDir);
    }
}
```

### Important: MakeDirectory Is Not Recursive

`MakeDirectory` creates only the final directory in the path. If the parent does not exist, the create does not happen -- the signature is `proto native bool MakeDirectory(string name)` (`1_core/proto/ensystem.c:525`), returning a `bool` you should check rather than assume; vanilla documents only `//!Makes a directory` (`:524`) and does not state what value comes back for a missing parent, so treat the return value as the contract to test, not a known outcome. Create each level in turn:

```c
// WRONG: Parent "MyMod" doesn't exist yet
MakeDirectory("$profile:MyMod/Data/Players");  // Nothing is created; the return value is your only signal

// RIGHT: Create each level
MakeDirectory("$profile:MyMod");
MakeDirectory("$profile:MyMod/Data");
MakeDirectory("$profile:MyMod/Data/Players");
```

### Constants for Paths Pattern

A framework mod defines all paths as constants in a dedicated class:

```c
class LNT_Const
{
    static const string PROFILE_DIR    = "$profile:Lantern";
    static const string CONFIG_DIR     = "$profile:Lantern/Configs";
    static const string LOG_DIR        = "$profile:Lantern/Logs";
    static const string PLAYERS_DIR    = "$profile:Lantern/Players";
    static const string PERMISSIONS_FILE = "$profile:Lantern/Permissions.json";
};
```

This avoids path string duplication across the codebase and makes it easy to find every file your mod touches.

---

## Config Data Classes

A well-designed config data class provides default values, version tracking, and clear documentation of each field.

### Basic Pattern

```c
class MyModConfig
{
    // Version tracking for migrations
    int ConfigVersion = 3;

    // Gameplay settings with sensible defaults
    bool EnableFeatureX = true;
    int MaxEntities = 50;
    float SpawnRadius = 500.0;
    string WelcomeMessage = "Welcome to the server!";

    // Complex settings
    ref array<string> AllowedWeapons = new array<string>();
    ref map<string, float> ZoneRadii = new map<string, float>();

    void MyModConfig()
    {
        // Initialize collections with defaults
        AllowedWeapons.Insert("AK74");
        AllowedWeapons.Insert("M4A1");

        ZoneRadii.Set("safe_zone", 100.0);
        ZoneRadii.Set("pvp_zone", 500.0);
    }
};
```

### Reflective ConfigBase Pattern

The Lantern examples in this wiki use a reflective config base — `LNT_ConfigBase` — where each config subclass declares its fields as descriptors. This lets an admin panel auto-generate UI for any config without hardcoded field names. This chapter is where that base is canonically defined:

```c
// Field descriptor: one entry per configurable field.
// GetFields() returns an array of these so the admin panel can
// render UI without hardcoding field names.
class LNT_ConfigField
{
    string m_Name;      // field identifier, e.g. "MaxDistance"
    string m_Type;      // "int", "float", "bool", "string"
    string m_Category;  // grouping label for the admin panel
}

// Reflective config base (the wiki's Lantern teaching example):
class LNT_ConfigBase
{
    // Each config declares its version
    int ConfigVersion;
    string ModId;

    // Subclasses override to declare their fields
    void Init(string modId)
    {
        ModId = modId;
    }

    // Reflection: get all configurable fields
    array<ref LNT_ConfigField> GetFields();

    // Dynamic get/set by field name (for admin panel sync)
    string GetFieldValue(string fieldName);
    void SetFieldValue(string fieldName, string value);

    // Hooks for custom logic on load/save
    void OnAfterLoad() {}
    void OnBeforeSave() {}
};
```

### Self-Loading Config Module

A config manager does not need a separate load call from the mission. A module can JSON-load its own config in `OnInit`, writing defaults on first run. This keeps each feature's config self-contained — the module owns its file and its lifecycle. (For the module lifecycle itself, see [Module Systems](02-module-systems.md).)

```c
// Data class — public fields are serialized
class LNT_ESPConfig
{
    bool EnableESP = true;
    float MaxDistance = 1000.0;
    int RefreshRate = 5;
};

// Module loads its own config on init, saving defaults if the file is absent
class LNT_AutoConfigModule
{
    protected ref LNT_ESPConfig m_Config;
    protected const string CONFIG_PATH = "$profile:Lantern/ESP.json";

    void OnInit()
    {
        m_Config = new LNT_ESPConfig();

        if (FileExist(CONFIG_PATH))
        {
            JsonFileLoader<LNT_ESPConfig>.JsonLoadFile(CONFIG_PATH, m_Config);
        }
        else
        {
            // First run: persist defaults so the admin has a file to edit
            JsonFileLoader<LNT_ESPConfig>.JsonSaveFile(CONFIG_PATH, m_Config);
        }
    }

    LNT_ESPConfig GetConfig()
    {
        return m_Config;
    }
};
```

---

## Config Versioning and Migration

As your mod evolves, config structures change. You add fields, remove fields, rename fields, change defaults. Without versioning, users with old config files will silently get wrong values or crash.

### The Version Field

Every config class should have an integer version field:

```c
class MyModConfig
{
    int ConfigVersion = 5;  // Increment when the structure changes
    // ...
};
```

### Migration on Load

When loading a config, compare the on-disk version with the current code version. If they differ, run migrations:

```c
void LoadConfig()
{
    MyModConfig config = new MyModConfig();  // Has current defaults

    if (FileExist(CONFIG_PATH))
    {
        JsonFileLoader<MyModConfig>.JsonLoadFile(CONFIG_PATH, config);

        if (config.ConfigVersion < CURRENT_VERSION)
        {
            MigrateConfig(config);
            config.ConfigVersion = CURRENT_VERSION;
            SaveConfig(config);  // Re-save with updated version
        }
    }
    else
    {
        SaveConfig(config);  // First run: write defaults
    }

    m_Config = config;
}
```

### Migration Functions

```c
static const int CURRENT_VERSION = 5;

void MigrateConfig(MyModConfig config)
{
    // Run each migration step sequentially
    if (config.ConfigVersion < 2)
    {
        // v1 → v2: "SpawnDelay" was renamed to "RespawnInterval"
        // Old field is lost on load; set new default
        config.RespawnInterval = 300.0;
    }

    if (config.ConfigVersion < 3)
    {
        // v2 → v3: Added "EnableNotifications" field
        config.EnableNotifications = true;
    }

    if (config.ConfigVersion < 4)
    {
        // v3 → v4: "MaxZombies" default changed from 100 to 200
        if (config.MaxZombies == 100)
        {
            config.MaxZombies = 200;  // Only update if user hadn't changed it
        }
    }

    if (config.ConfigVersion < 5)
    {
        // v4 → v5: "DifficultyMode" changed from int to string
        // config.DifficultyMode = "Normal"; // Set new default
    }

    LNT_Log.Info("Config", "Migrated config from v" + config.ConfigVersion.ToString() + " to v" + CURRENT_VERSION.ToString());
}
```

### A Versioned-Migration Checklist

Large, long-lived mods treat config migration as a first-class feature. DayZ Expansion is the clearest public example: each of its settings classes carries a `static const int VERSION` and converts older files forward on load, so server owners never hand-edit a config after an update. In the repository's `experimental` branch at commit `6dacd00`, 48 settings classes declare such a constant and the highest has reached **32** (`DayZExpansion/AI/Scripts/3_Game/DayZExpansion_AI/Settings/Patrols/ExpansionAIPatrolSettings.c:61`), with 23 and 20 elsewhere. `ExpansionAISettings` shows the mechanism directly: a ladder of `if (m_Version < N)` steps from 1 up to 20, then `m_Version = VERSION` (`.../Settings/ExpansionAISettings.c:24,266-373`). Read those numbers as a snapshot of that one commit -- they record how many times each settings schema has been revised, not a release history of the mod. However you structure it, a robust migration flow follows the same checklist:

1. Give each config an integer `ConfigVersion` field from day one.
2. Write a dedicated migration step for every version bump.
3. Run migrations in order (1 to 2, then 2 to 3, then 3 to 4, etc.) — never skip intermediate steps, because each one assumes the previous ran.
4. Make each step change only what that version step requires; leave everything else untouched.
5. Preserve user-modified values: only overwrite a field when it still holds the old default.
6. Write the final version number to disk after all steps complete, then re-save the file.
7. Log the migration (`from v3 to v5`) so a broken upgrade is visible in the server log.

---

## Auto-Save Timers

For configs that change at runtime (admin edits, player data accumulation), implement an auto-save timer to prevent data loss on crashes.

### Timer-Based Auto-Save

```c
class MyDataManager
{
    protected const float AUTOSAVE_INTERVAL = 300.0;  // 5 minutes
    protected float m_AutosaveTimer;
    protected bool m_Dirty;  // Has data changed since last save?

    void MarkDirty()
    {
        m_Dirty = true;
    }

    void OnUpdate(float dt)
    {
        m_AutosaveTimer += dt;
        if (m_AutosaveTimer >= AUTOSAVE_INTERVAL)
        {
            m_AutosaveTimer = 0;

            if (m_Dirty)
            {
                Save();
                m_Dirty = false;
            }
        }
    }

    void OnMissionFinish()
    {
        // Always save on shutdown, even if timer hasn't fired
        if (m_Dirty)
        {
            Save();
            m_Dirty = false;
        }
    }
};
```

### Dirty Flag Optimization

Only write to disk when data has actually changed. File I/O is expensive. If nothing changed, skip the save:

```c
void UpdateSetting(string key, string value)
{
    if (m_Settings.Get(key) == value) return;  // No change, no save

    m_Settings.Set(key, value);
    MarkDirty();
}
```

### Save on Critical Events

In addition to timed saves, save immediately after critical operations:

```c
void BanPlayer(string uid, string reason)
{
    m_BanList.Insert(uid);
    Save();  // Immediate save — bans must survive crashes
}
```

---

## Common Mistakes

### 1. Treating JsonLoadFile as if It Returns a Value

```c
// WRONG — does not compile
if (JsonFileLoader<MyConfig>.JsonLoadFile(path, config)) { ... }
```

`JsonLoadFile` returns `void`. Either call it and then check the object's state, or -- better -- switch to `JsonFileLoader<T>.LoadFile(path, config, error)`, which returns a real `bool` and an error message (see [JsonFileLoader Pattern](#jsonfileloader-pattern)).

### 2. Not Checking FileExist Before Loading

```c
// WRONG — silently does nothing when the file is absent, and says so to no one
JsonFileLoader<MyConfig>.JsonLoadFile("$profile:MyMod/Config.json", config);

// RIGHT — check first, create defaults if missing
if (!FileExist("$profile:MyMod/Config.json"))
{
    SaveDefaults();
    return;
}
JsonFileLoader<MyConfig>.JsonLoadFile("$profile:MyMod/Config.json", config);
```

`JsonLoadFile` opens with `if (FileExist(filename))` and simply returns when that check fails (`3_game/tools/jsonfileloader.c:105-108`), so a missing file leaves your object exactly as you passed it in -- no crash, no error, no signal. That is why you check first and write defaults yourself, or use `LoadFile`, which reports `File "%1" does not exist` through its `out` error string.

### 3. Forgetting to Create Directories

`JsonSaveFile` gives up silently if the file cannot be opened for writing -- it returns as soon as `OpenFile` yields a null handle, with no error (`3_game/tools/jsonfileloader.c:143-147`). A missing parent directory is the usual cause. Always ensure directories before saving, or use `SaveFile`, which returns `false` and fills in an error message.

### 4. Public Fields You Did Not Intend to Serialize

Every `public` field on a config class ends up in the JSON. If you have runtime-only fields, make them `protected` or `private`:

```c
class MyConfig
{
    // These go to JSON:
    int MaxPlayers = 60;
    string ServerName = "My Server";

    // This does NOT go to JSON (protected):
    protected bool m_Loaded;
    protected float m_LastSaveTime;
};
```

### 5. Absolute, Backslashed Paths in Config Values

The `\\` and `\"` escape sequences work fine in Enforce Script string literals -- vanilla writes `"DZ\\plants"` in `3_game/objectspawner.c:4` and `"Cannot open file \"%1\" for reading"` in `3_game/tools/jsonfileloader.c:14`, and the manual-JSON example earlier in this chapter uses `\"` for the same reason. The mistake is not the escaping; it is storing a machine-specific absolute path at all.

```c
// BAD — absolute, machine-specific, and outside the profile sandbox
string LogPath = "C:\\DayZ\\Logs\\server.log";

// GOOD — profile-relative and portable across every host
string LogPath = "$profile:MyMod/Logs/server.log";
```

Use forward slashes in stored paths as a convention: the filesystem prefixes (`$profile:`, `$saves:`, `$mission:`) are written that way throughout vanilla, and one engine subsystem's fix-up for the wrong delimiter is a **diagnostic-build-only** convenience, not something to rely on -- particle registration rewrites `\` to `/` and logs a warning, but only inside `#ifdef DIAG_DEVELOPER` (`3_game/particles/particlelist.c:390-395`, guarding the `Replace` at `:391` and the `ErrorEx` at `:393`, under a comment that reads "Silently fail on retail" at `:389`). On a **retail** build, a backslash path is not normalised at all (`:397`) -- which is precisely why the forward-slash convention matters. One real escaping caveat remains, and it belongs to JSON rather than to Enforce Script: a backslash inside a JSON *string value* must be escaped in the file itself, so a Windows path written into JSON appears as `"C:\\DayZ"` on disk. Another reason to stay with `$profile:` and forward slashes.

---

## Best Practices

1. **Use `$profile:` for all file paths.** Never hardcode absolute paths.

2. **Create directories before writing files.** Check with `FileExist()`, create with `MakeDirectory()`, one level at a time.

3. **Always provide default values in your config class constructor or field initializers.** This ensures first-run configs are sensible.

4. **Version your configs from day one.** Adding a `ConfigVersion` field costs nothing and saves hours of debugging later.

5. **Separate config data classes from manager classes.** The data class is a dumb container; the manager handles load/save/sync logic.

6. **Use auto-save with a dirty flag.** Do not write to disk every time a value changes --- batch writes on a timer.

7. **Save on mission finish.** The auto-save timer is a safety net, not the primary save. Always save during `OnMissionFinish()`.

8. **Define path constants in one place.** A `LNT_Const` class with all paths prevents string duplication and makes path changes trivial.

9. **Log load/save operations.** When debugging config issues, a log line saying "Loaded config v3 from $profile:MyMod/Config.json" is invaluable.

10. **Test with a deleted config file.** Your mod should handle first-run gracefully: create directories, write defaults, log what it did.

---

## Compatibility & Impact

- **Multi-Mod:** Each mod writes to its own `$profile:ModName/` directory. Conflicts only happen if two mods use the same directory name. Use a unique, recognizable prefix for your mod's folder.
- **Load Order:** Config loading happens in `OnInit` or `OnMissionStart`, both controlled by the mod's own lifecycle. No cross-mod load-order issues unless two mods try to read/write the same file (which they should never do).
- **Listen Server:** Config files are server-side only (`$profile:` resolves on the server). On listen servers, client-side code can technically access `$profile:`, but configs should only be loaded by server modules to avoid ambiguity.
- **Performance:** `JsonFileLoader` is synchronous and blocks the main thread. For large configs (100+ KB), load during `OnInit` (before gameplay starts). Auto-save timers prevent repeated writes; the dirty-flag pattern ensures disk I/O only happens when data has actually changed.
- **Migration:** Adding new fields to a config class is safe --- `JsonFileLoader` ignores missing JSON keys and leaves the class default value. Removing or renaming fields requires a versioned migration step to avoid silent data loss.

---

## Theory vs Practice

| Textbook Says | DayZ Reality |
|---------------|-------------|
| Use async file I/O to avoid blocking | Enforce Script has no async file I/O; all reads/writes are synchronous. Load at startup, save on timers. |
| Validate JSON with a schema | No JSON schema validation exists; validate fields in `OnAfterLoad()` or with guard clauses after loading. |
| Use a database for structured data | No database access from Enforce Script; JSON files in `$profile:` are the only persistence mechanism. |
