# File I/O & JSON


---

## Introduction

DayZ provides file I/O operations for reading and writing text files, JSON serialization/deserialization, directory management, and file enumeration. All file operations use special path prefixes (`$profile:`, `$saves:`, `$mission:`) rather than absolute filesystem paths. This chapter covers every file operation available in Enforce Script.

---

## Path Prefixes

| Prefix | Location | Writable |
|--------|----------|----------|
| `$profile:` | Server/client profile directory (e.g., `DayZServer/profiles/`) | Yes |
| `$saves:` | Save directory | Yes |
| `$mission:` | Current mission folder (e.g., `mpmissions/dayzOffline.chernarusplus/`) | Read typically |
| `$CurrentDir:` | Current working directory | Depends |
| No prefix | Relative to game root | Read only |

> **Important:** Most file write operations are restricted to `$profile:` and `$saves:`. Attempting to write elsewhere may silently fail.

---

## File Existence Check

```c
proto bool FileExist(string name);
```

Returns `true` if the file exists at the given path.

**Example:**

```c
if (FileExist("$profile:MyMod/config.json"))
{
    Print("Config file found");
}
else
{
    Print("Config file not found, creating defaults");
}
```

---

## Opening & Closing Files

```c
proto FileHandle OpenFile(string name, FileMode mode);
proto void CloseFile(FileHandle file);
```

### FileMode Enum

```c
enum FileMode
{
    READ,     // Open for reading (file must exist)
    WRITE,    // Open for writing (creates new / overwrites existing)
    APPEND    // Open for appending (creates if not exists)
}
```

`FileHandle` is declared as `typedef int[] FileHandle` (`1_Core/proto/ensystem.c`) --- an opaque handle, not a number you should do arithmetic on. Compare it against `0` to detect failure, exactly as vanilla's own examples do.

**Example:**

```c
FileHandle fh = OpenFile("$profile:MyMod/log.txt", FileMode.WRITE);
if (fh != 0)
{
    // File opened successfully
    // ... do work ...
    CloseFile(fh);
}
```

> **Critical:** Always call `CloseFile()` when done. Failure to close files can cause data loss and resource leaks.

---

## Writing Files

### FPrintln (Write Line)

```c
proto void FPrintln(FileHandle file, void var);
```

Writes the value followed by a newline character.

### FPrint (Write Without Newline)

```c
proto void FPrint(FileHandle file, void var);
```

Writes the value without a trailing newline.

**Example --- write a log file:**

```c
void WriteLog(string message)
{
    FileHandle fh = OpenFile("$profile:MyMod/log.txt", FileMode.APPEND);
    if (fh != 0)
    {
        int year, month, day, hour, minute;
        GetGame().GetWorld().GetDate(year, month, day, hour, minute);
        string timestamp = string.Format("[%1-%2-%3 %4:%5]", year, month, day, hour, minute);

        FPrintln(fh, timestamp + " " + message);
        CloseFile(fh);
    }
}
```

---

## Reading Files

### FGets (Read Line)

```c
proto int FGets(FileHandle file, string var);
```

Reads one line from the file into `var`. Returns the number of characters read, or `-1` at end of file.

> **Use `>= 0`, not `> 0`, as the loop condition.** The vanilla doc comment states that "end of file is EMPTY line", and vanilla's own example loops on `FGets(...) > 0`. That stops at the *first blank line* in the file, not at the end of it, because a blank line also returns `0`. Looping on `>= 0` reads blank lines as blank lines and still terminates correctly, since only true EOF returns `-1`.

**Example --- read a file line by line:**

```c
void ReadConfigFile()
{
    FileHandle fh = OpenFile("$profile:MyMod/settings.txt", FileMode.READ);
    if (fh != 0)
    {
        string line;
        while (FGets(fh, line) >= 0)
        {
            Print("Line: " + line);
            ProcessLine(line);
        }
        CloseFile(fh);
    }
}
```

### ReadFile (Raw Binary Read)

```c
proto int ReadFile(FileHandle file, void param_array, int length);
```

Reads raw bytes into a buffer. Used for binary data.

---

## Directory Operations

### MakeDirectory

```c
proto native bool MakeDirectory(string name);
```

Creates a directory. Returns `true` on success. Creates only the final directory --- parent directories must already exist.

**Example --- ensure directory structure:**

```c
void EnsureDirectories()
{
    MakeDirectory("$profile:MyMod");
    MakeDirectory("$profile:MyMod/data");
    MakeDirectory("$profile:MyMod/logs");
}
```

### DeleteFile

```c
proto native bool DeleteFile(string name);
```

Deletes a file. Only works in `$profile:` and `$saves:` directories.

### CopyFile

```c
proto native bool CopyFile(string sourceName, string destName);
```

Copies a file from source to destination.

**Example:**

```c
// Backup before overwriting
if (FileExist("$profile:MyMod/config.json"))
{
    CopyFile("$profile:MyMod/config.json", "$profile:MyMod/config.json.bak");
}
```

---

## File Enumeration (FindFile / FindNextFile)

Enumerate files matching a pattern in a directory.

```c
proto FindFileHandle FindFile(string pattern, out string fileName,
                               out FileAttr fileAttributes, FindFileFlags flags);
proto bool FindNextFile(FindFileHandle handle, out string fileName,
                         out FileAttr fileAttributes);
proto native void CloseFindFile(FindFileHandle handle);
```

### FileAttr Enum

```c
enum FileAttr
{
    DIRECTORY,   // Entry is a directory
    HIDDEN,      // Entry is hidden
    READONLY,    // Entry is read-only
    INVALID      // Invalid entry
}
```

> **Caveat on testing `FileAttr`:** community frameworks commonly test file/directory type with the bit-test idiom `fileAttr & FileAttr.DIRECTORY` (Community Framework's `CF_File._SetAttributes()` and Community Online Tools' `FileAttributeToString()` both test all four members this way). This does not work as written: the script-side declaration above gives the enum no explicit values, so `DIRECTORY` is the zero-valued first member, and `fileAttr & FileAttr.DIRECTORY` evaluates to `0` for every possible `fileAttr` --- a bitmask test against `DIRECTORY` can never match, so code copied from `CF_File._SetAttributes()` reports every entry as not-a-directory. The engine side is native and Bohemia has not published the attribute encoding, and no vanilla script tests these bits --- all four vanilla `FindFile()` call sites (`2_GameLib/entities/worldsmenu.c:72`, `5_Mission/gui/newui/videoplayer.c:81`, `4_World/Plugins/PluginBase/PluginFileHandler/PluginConfigHandler/pluginconfigscene.c:112`, `4_World/Plugins/PluginBase/PluginFileHandler/PluginLocalProfile/pluginlocalprofilescene.c:72`) ignore `fileAttr` entirely; the two plugin sites additionally pass an uninitialised `flags` local (which resolves to `0`, i.e. `FindFileFlags.DIRECTORIES`) rather than a deliberate value. The examples below therefore do not filter by `FileAttr` at all --- if separating files from directories matters to your mod, confirm the behaviour on your target build rather than assuming either an ordinal or bitmask reading.

### FindFileFlags Enum

`FindFileFlags` selects which storage location to search, not which entry types (files vs. directories) to return --- a script would have to read that distinction from `FileAttr.DIRECTORY` on each result instead, subject to the caveat above:

```c
enum FindFileFlags
{
    DIRECTORIES,  // Search the loose filesystem only (not packed .pak archives)
    ARCHIVES,     // Search inside packed archives (.pak) only
    ALL           // Search both loose filesystem and archives
}
```

**Example --- enumerate all JSON files in a directory:**

```c
void ListJsonFiles()
{
    string fileName;
    FileAttr fileAttr;
    FindFileHandle handle = FindFile(
        "$profile:MyMod/missions/*.json", fileName, fileAttr, FindFileFlags.ALL
    );

    if (handle)
    {
        // Process first result
        Print("Found: " + fileName);

        // Process remaining results
        while (FindNextFile(handle, fileName, fileAttr))
        {
            Print("Found: " + fileName);
        }

        CloseFindFile(handle);
    }
}
```

> **Important:** `FindFile` returns just the file name, not the full path. You must prepend the directory path yourself when processing the files.

**Example --- count files in a directory:**

`$profile:`/`$saves:` locations are loose filesystem, not packed `.pak` archives, so use `FindFileFlags.ALL` (or `DIRECTORIES`, meaning "loose filesystem") rather than `ARCHIVES` here. This example counts every entry `FindFile` returns; see the caveat above if you need to exclude directories:

```c
int CountFiles(string pattern)
{
    int count = 0;
    string fileName;
    FileAttr fileAttr;
    FindFileHandle handle = FindFile(pattern, fileName, fileAttr, FindFileFlags.ALL);

    if (handle)
    {
        count++;
        while (FindNextFile(handle, fileName, fileAttr))
        {
            count++;
        }
        CloseFindFile(handle);
    }

    return count;
}
```

---

## JsonFileLoader (Generic JSON)

**File:** `3_Game/tools/jsonfileloader.c` (173 lines)

The recommended way to load and save JSON data. Works with any class that has public fields.

### Modern API (Preferred)

```c
class JsonFileLoader<Class T>
{
    // Load JSON file into object
    static bool LoadFile(string filename, out T data, out string errorMessage);

    // Save object to JSON file
    static bool SaveFile(string filename, T data, out string errorMessage);

    // Parse JSON string into object
    static bool LoadData(string string_data, out T data, out string errorMessage);

    // Serialize object to JSON string
    static bool MakeData(T inputData, out string outputData,
                          out string errorMessage, bool prettyPrint = true);
}
```

All methods return `bool` --- `true` on success, `false` on failure with the error in `errorMessage`.

### Legacy API (Deprecated)

```c
class JsonFileLoader<Class T>
{
    static void JsonLoadFile(string filename, out T data);    // Returns void!
    static void JsonSaveFile(string filename, T data);
    static void JsonLoadData(string string_data, out T data);
    static string JsonMakeData(T data);
}
```

> **Critical Gotcha:** `JsonLoadFile()` returns `void`, so there is no result for the caller to branch on:
> ```c
> // WRONG - JsonLoadFile returns void; there is nothing to test
> if (JsonFileLoader<MyConfig>.JsonLoadFile(path, cfg)) { }
>
> // CORRECT - use the modern LoadFile() which returns bool
> if (JsonFileLoader<MyConfig>.LoadFile(path, cfg, error)) { }
> ```
>
> Be precise about *what* the legacy call does and does not tell you --- the three failure paths in `JsonFileLoader.JsonLoadFile()` behave differently:
>
> | Failure | What the legacy `JsonLoadFile()` does |
> |---|---|
> | File does not exist | The whole body is inside `if (FileExist(filename))`, so it returns having done nothing. No diagnostic at all |
> | `OpenFile()` fails (handle `0`) | Early `return`. No diagnostic at all |
> | JSON fails to parse | Calls `ErrorEx(...)` with the filename and the serializer's error --- this **is** reported, in the log |
>
> So the accurate statement is that the legacy API gives the *caller* no way to detect or handle any of these, and is genuinely silent for the two file-access failures; it is not true that it can never report anything. `LoadFile()` returns `false` and fills `errorMessage` for all three, which is why it is the one to use.

### Data Class Requirements

The target class must have **public fields** with default values. The JSON serializer maps field names directly to JSON keys.

```c
class MyConfig
{
    int MaxPlayers = 60;
    float SpawnRadius = 150.0;
    string ServerName = "My Server";
    bool EnablePVP = true;
    ref array<string> AllowedItems = new array<string>;
    ref map<string, int> ItemPrices = new map<string, int>;

    void MyConfig()
    {
        AllowedItems.Insert("BandageDressing");
        AllowedItems.Insert("Canteen");
    }
}
```

This produces JSON:

```json
{
    "MaxPlayers": 60,
    "SpawnRadius": 150.0,
    "ServerName": "My Server",
    "EnablePVP": true,
    "AllowedItems": ["BandageDressing", "Canteen"],
    "ItemPrices": {}
}
```

### Complete Load/Save Example

```c
class MyModConfig
{
    int Version = 1;
    float RespawnTime = 300.0;
    ref array<string> SpawnItems = new array<string>;
}

class MyModConfigManager
{
    protected static const string CONFIG_PATH = "$profile:MyMod/config.json";
    protected ref MyModConfig m_Config;

    void Init()
    {
        MakeDirectory("$profile:MyMod");
        m_Config = new MyModConfig();
        Load();
    }

    void Load()
    {
        if (!FileExist(CONFIG_PATH))
        {
            Save();  // Create default config
            return;
        }

        string error;
        if (!JsonFileLoader<MyModConfig>.LoadFile(CONFIG_PATH, m_Config, error))
        {
            Print("[MyMod] Config load error: " + error);
            m_Config = new MyModConfig();  // Reset to defaults
            Save();
        }
    }

    void Save()
    {
        string error;
        if (!JsonFileLoader<MyModConfig>.SaveFile(CONFIG_PATH, m_Config, error))
        {
            Print("[MyMod] Config save error: " + error);
        }
    }

    MyModConfig GetConfig()
    {
        return m_Config;
    }
}
```

---

## JsonSerializer (Direct Use)

**File:** `3_Game/gameplay.c`

For cases where you need to serialize/deserialize JSON strings directly without file operations:

```c
class JsonSerializer : Serializer
{
    proto bool WriteToString(void variable_out, bool nice, out string result);
    proto bool ReadFromString(void variable_in, string jsonString, out string error);
}
```

**Example:**

```c
MyConfig cfg = new MyConfig();
cfg.MaxPlayers = 100;

JsonSerializer js = new JsonSerializer();

// Serialize to string
string jsonOutput;
js.WriteToString(cfg, true, jsonOutput);  // true = pretty print
Print(jsonOutput);

// Deserialize from string
MyConfig parsed = new MyConfig();
string parseError;
js.ReadFromString(parsed, jsonOutput, parseError);
Print("MaxPlayers: " + parsed.MaxPlayers);
```

---

## Summary

| Operation | Function | Notes |
|-----------|----------|-------|
| Check exists | `FileExist(path)` | Returns bool |
| Open | `OpenFile(path, FileMode)` | Returns handle (0 = fail) |
| Close | `CloseFile(handle)` | Always call when done |
| Write line | `FPrintln(handle, data)` | With newline |
| Write | `FPrint(handle, data)` | Without newline |
| Read line | `FGets(handle, out line)` | Returns -1 at EOF |
| Make dir | `MakeDirectory(path)` | Single level only |
| Delete | `DeleteFile(path)` | Only `$profile:` / `$saves:` |
| Copy | `CopyFile(src, dst)` | -- |
| Find files | `FindFile(pattern, ...)` | Returns handle, iterate with `FindNextFile` |
| JSON load | `JsonFileLoader<T>.LoadFile(path, data, error)` | Modern API, returns bool |
| JSON save | `JsonFileLoader<T>.SaveFile(path, data, error)` | Modern API, returns bool |
| JSON string | `JsonSerializer.WriteToString()` / `ReadFromString()` | Direct string operations |

| Concept | Key Point |
|---------|-----------|
| Path prefixes | `$profile:` (writable), `$mission:` (read), `$saves:` (writable) |
| JsonLoadFile | **Returns void** --- the caller cannot detect failure; file-access failures are silent, parse failures only reach the log via `ErrorEx`. Use `LoadFile()` (bool) instead |
| Data classes | Public fields with defaults, `ref` for arrays/maps |
| Always close | Every `OpenFile` must have a matching `CloseFile` |
| FindFile | Returns only filenames, not full paths |

---

## Best Practices

- **Always wrap file operations in existence checks and close handles in all code paths.** An unclosed `FileHandle` leaks resources and can prevent the file from being written to disk. Use guard patterns: check `fh != 0`, do work, then `CloseFile(fh)` before every `return`.
- **Use the modern `JsonFileLoader<T>.LoadFile()` (returns bool) instead of the legacy `JsonLoadFile()` (returns void).** The legacy call gives the caller no way to detect failure: a missing file and a failed `OpenFile()` return with no diagnostic at all, and while a parse error does reach the log through `ErrorEx()`, your code still cannot branch on it. `LoadFile()` returns `false` and fills `errorMessage` in every one of those cases.
- **Create directories with `MakeDirectory()` in order from parent to child.** `MakeDirectory` only creates the final directory segment. `MakeDirectory("$profile:A/B/C")` fails if `A/B` does not exist. Create each level sequentially.
- **Use `CopyFile()` to create backups before overwriting config files.** JSON parse errors from corrupted saves are unrecoverable. A `.bak` copy lets server owners restore the last good state.
- **Remember that `FindFile()` returns only filenames, not full paths.** You must concatenate the directory prefix yourself when loading files found via `FindFile`/`FindNextFile`.

---

## Compatibility & Impact

> **Mod Compatibility:** File I/O is inherently isolated per mod when each mod uses its own `$profile:` subdirectory. Conflicts occur only when two mods read/write the same file path.

- **Load Order:** File I/O has no load-order dependency. Mods read and write independently.
- **Modded Class Conflicts:** No class conflicts. The risk is two mods using the same `$profile:` subdirectory name or filename, causing data corruption.
- **Performance Impact:** JSON serialization via `JsonFileLoader` is synchronous and blocks the main thread. Loading large JSON files (>100KB) during gameplay causes frame hitches. Load configs in `OnInit()` or `OnMissionStart()`, never in `OnUpdate()`.
- **Server/Client:** File writes are restricted to `$profile:` and `$saves:`. On clients, `$profile:` points to the client profile directory. On dedicated servers, it points to the server profile. `$mission:` is typically read-only on both sides.

---

## Common File I/O Patterns

These combinations recur across server-side mods. Each builds on the primitives above.

| Pattern | How it is built | Where it is covered |
|---------|-----------------|---------------------|
| Settings manager | `MakeDirectory` chain + `FileExist` check + `LoadFile` with fallback to freshly-constructed defaults, then `SaveFile` to persist the defaults on first run | [Config Persistence](../07-patterns/04-config-persistence.md) |
| Backup before save | `CopyFile` the current config to a `.bak` sibling before overwriting, so a corrupt write can be recovered | `CopyFile` example above |
| Per-player enumeration | `FindFile`/`FindNextFile` over `$profile:<mod>/Players/*.json` to load every stored player record on startup | [Config Persistence](../07-patterns/04-config-persistence.md) |
| RPC payload serialization | `JsonSerializer.WriteToString()` to turn a config object into a string, sent over the network with no file involved | [RPC Patterns](../07-patterns/03-rpc-patterns.md) |
