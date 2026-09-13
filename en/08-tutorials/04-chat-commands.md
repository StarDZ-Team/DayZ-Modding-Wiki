# Adding Chat Commands


---

> **Summary:** This tutorial walks you through creating a chat command system for DayZ. You will intercept chat input before it is broadcast, parse command prefixes and arguments, check admin permissions, execute a server-side action, and send feedback to the player. By the end, you will have a working `/heal` command that fully heals a character, along with a reusable framework for adding more commands.

---

## Table of Contents

- [What We Are Building](#what-we-are-building)
- [Prerequisites](#prerequisites)
- [Architecture Overview](#architecture-overview)
- [Step 1: Hook Into Chat Input](#step-1-hook-into-chat-input)
- [Step 2: Parse the Command](#step-2-parse-the-command)
- [Step 3: Check Admin Permissions](#step-3-check-admin-permissions)
- [Step 4: Execute the Server-Side Action](#step-4-execute-the-server-side-action)
- [Step 5: Send Feedback to the Admin](#step-5-send-feedback-to-the-admin)
- [Step 6: Register Commands and Handle the RPC](#step-6-register-commands-and-handle-the-rpc)
- [Step 7: List Commands in an Admin Panel](#step-7-list-commands-in-an-admin-panel)
- [Mod Registration (config.cpp)](#mod-registration-config-cpp)
- [Adding More Commands](#adding-more-commands)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)
- [Theory vs Practice](#theory-vs-practice)
- [What You Learned](#what-you-learned)

---

## What We Are Building

A chat command system with:

- **`/heal`** -- Fully heals the caller's character (health, blood, shock, hunger, thirst)
- **`/heal PlayerName`** -- Heals a specific player by name
- A reusable framework for adding `/kill`, `/teleport`, `/time`, `/weather`, and any other command
- Admin permission checking so regular players cannot use admin commands
- Server-side execution with chat feedback messages
- Clean interception so the command text is **not** broadcast to everyone as chat

---

## Prerequisites

- A working mod structure (complete [Chapter 8.1](01-first-mod.md) first)
- Understanding of the [client-server RPC pattern](03-admin-panel.md) from Chapter 8.3

### Mod Structure for This Tutorial

```
ChatCommands/
    mod.cpp
    Scripts/
        config.cpp
        3_Game/
            ChatCommands/
                CCmdRPC.c
                CCmdBase.c
                CCmdRegistry.c
        4_World/
            ChatCommands/
                CCmdServerHandler.c        (modded PlayerBase -- server RPC handler)
                commands/
                    CCmdHeal.c
        5_Mission/
            ChatCommands/
                CCmdChatHook.c             (modded ChatInputMenu -- intercept & send)
                CCmdClientRPC.c            (modded DayZGame -- receive feedback)
                CCmdRegister.c             (modded MissionServer -- register commands)
```

---

## Architecture Overview

Chat commands follow this flow:

```
CLIENT                                  SERVER
------                                  ------

1. Admin types "/heal" and presses Enter
2. ChatInputMenu.OnChange intercepts it
   BEFORE the text is broadcast as chat
3. Client sends command via RPC  ---->  4. PlayerBase.OnRPC receives it
                                            Checks admin permissions
                                            Looks up command handler
                                            Executes the command
                                        5. Server sends feedback  ---->  CLIENT
                                            (target-less RPC to caller)
                                                                     6. DayZGame.OnRPC
                                                                        shows feedback
                                                                        in chat
```

**Why process commands on the server?** Because the server has authority over game state. Only the server can reliably heal players, change weather, teleport characters, and modify world state. The client's role is limited to detecting the command and forwarding it.

**Why intercept at `ChatInputMenu`?** Vanilla `ChatInputMenu.OnChange` calls `g_Game.ChatPlayer(text)` the moment you press Enter, which broadcasts your text as a normal chat message. If you wait for the later `ChatMessageEventTypeID` event, the message has already been sent -- so everyone sees `/heal` in chat. Intercepting inside `OnChange` and skipping the vanilla broadcast is the reliable way to suppress command text.

---

## Step 1: Hook Into Chat Input

We intercept chat input at the exact point where vanilla decides to broadcast it. The `ChatInputMenu` class owns the text box you type into. Its `OnChange()` handler runs when you press Enter; if the text is non-empty it calls `g_Game.ChatPlayer(text)`, which sends the message to everyone.

By modding `OnChange()`, we can inspect the text first. If it starts with `/`, we forward it to the server as a command and return early -- **without** calling `super.OnChange()`, so the vanilla broadcast never happens.

One point worth getting right, because it is easy to assume the opposite: a `modded class` **can** access `private` members of the class it mods. Bohemia's Enforce Script syntax reference states it directly -- *"Even though modded class behaves similar to an inherited one, it can still access private members of the vanilla class"* -- so `m_edit_box`, which vanilla declares `private`, is readable from your modded `ChatInputMenu`. The code below still reads the text from the `Widget w` argument instead. That is a robustness choice, not a language limitation: `w` is the widget that actually raised the event, and a private field name carries no compatibility promise across patches.

### Create `Scripts/5_Mission/ChatCommands/CCmdChatHook.c`

```c
modded class ChatInputMenu
{
    // -------------------------------------------------------
    // OnChange fires while typing (finished == false) and once
    // more when Enter is pressed (finished == true). We only act
    // on the final submit.
    // -------------------------------------------------------
    override bool OnChange(Widget w, int x, int y, bool finished)
    {
        if (finished)
        {
            // Read the text from the widget that fired the change (w)
            // rather than from the vanilla m_edit_box field. A modded class
            // *can* read a vanilla private member -- that is documented
            // Enforce behaviour -- but m_edit_box is an internal name with no
            // compatibility promise, while w is the widget that actually
            // fired the event. Using w keeps the hook working if the field
            // is ever renamed.
            EditBoxWidget eb = EditBoxWidget.Cast(w);
            if (!eb)
                return super.OnChange(w, x, y, finished);

            string text = eb.GetText();

            if (text.Length() > 0 && text.Substring(0, 1) == "/")
            {
                // It is a command. Send it and close the input box.
                // Returning true WITHOUT calling super means the vanilla
                // handler never broadcasts the text as chat.
                SendChatCommand(text);
                Close();
                return true;
            }
        }

        // Not a command -- let vanilla chat handle it normally.
        return super.OnChange(w, x, y, finished);
    }

    // -------------------------------------------------------
    // Send the command string to the server via RPC
    // -------------------------------------------------------
    protected void SendChatCommand(string fullCommand)
    {
        Man player = GetGame().GetPlayer();
        if (!player)
            return;

        Print("[ChatCommands] Sending command to server: " + fullCommand);

        Param1<string> data = new Param1<string>(fullCommand);
        GetGame().RPCSingleParam(player, CCmdRPC.COMMAND_REQUEST, data, true);
    }
};
```

### How Chat Interception Works

`ChatInputMenu.OnChange` runs on the client. We read the current text from the box, and if it starts with `/` we treat it as a command:

1. `SendChatCommand()` sends the raw string to the server, associated with the local player object, so it arrives at that player's server-side `OnRPC`.
2. We call `Close()` to dismiss the chat input box.
3. We `return true` and skip `super`, so `g_Game.ChatPlayer()` is never called and the text is not broadcast.

Normal chat still works: any message that does not start with `/` falls through to `super.OnChange()` unchanged.

> The feedback the server sends back is received in Step 5 by a `modded class DayZGame`, not here. `ChatInputMenu` is only responsible for capturing input.

---

## Step 2: Parse the Command

On the server side, we break a command string like `/heal PlayerName` into its parts: the command name (`heal`) and the arguments (`["PlayerName"]`). We also define the RPC IDs and a base class every command extends.

### Create `Scripts/3_Game/ChatCommands/CCmdRPC.c`

```c
class CCmdRPC
{
    // Pick unique numbers that do not collide with other mods.
    static const int COMMAND_REQUEST  = 79001;
    static const int COMMAND_FEEDBACK = 79002;
};
```

### Create `Scripts/3_Game/ChatCommands/CCmdBase.c`

The base class defines the command interface and two shared helpers that every command reuses: sending feedback, and finding players. Because these helpers do not touch world entities, they live in `3_Game`.

```c
// -------------------------------------------------------
// Base class for all chat commands
// -------------------------------------------------------
class CCmdBase
{
    // The command name without the / prefix (e.g., "heal")
    string GetName()
    {
        return "";
    }

    // Short description shown in help or command list
    string GetDescription()
    {
        return "";
    }

    // Usage syntax shown when the command is used incorrectly
    string GetUsage()
    {
        return "/" + GetName();
    }

    // Whether this command requires admin privileges
    bool RequiresAdmin()
    {
        return true;
    }

    // Execute the command on the server.
    // Returns true if successful, false if failed.
    bool Execute(PlayerIdentity caller, array<string> args)
    {
        return false;
    }

    // -------------------------------------------------------
    // Shared helper: send a feedback message to one player.
    // Target is null and the recipient is the caller's identity,
    // so the client's DayZGame.OnRPC receives it (see Step 5).
    // -------------------------------------------------------
    protected void SendFeedback(PlayerIdentity caller, string prefix, string message)
    {
        if (!caller)
            return;

        Param2<string, string> data = new Param2<string, string>(prefix, message);
        GetGame().RPCSingleParam(null, CCmdRPC.COMMAND_FEEDBACK, data, true, caller);
    }

    // -------------------------------------------------------
    // Shared helper: find a player by exact identity.
    // -------------------------------------------------------
    protected Man FindPlayerByIdentity(PlayerIdentity identity)
    {
        if (!identity)
            return null;

        ref array<Man> players = new array<Man>;
        GetGame().GetPlayers(players);

        for (int i = 0; i < players.Count(); i++)
        {
            Man man = players.Get(i);
            if (man && man.GetIdentity() && man.GetIdentity().GetId() == identity.GetId())
                return man;
        }

        return null;
    }

    // -------------------------------------------------------
    // Shared helper: find a player by partial (case-insensitive) name.
    // -------------------------------------------------------
    protected Man FindPlayerByName(string partialName)
    {
        ref array<Man> players = new array<Man>;
        GetGame().GetPlayers(players);

        string searchLower = partialName;
        searchLower.ToLower();

        for (int i = 0; i < players.Count(); i++)
        {
            Man man = players.Get(i);
            if (man && man.GetIdentity())
            {
                string playerNameLower = man.GetIdentity().GetName();
                playerNameLower.ToLower();

                if (playerNameLower.Contains(searchLower))
                    return man;
            }
        }

        return null;
    }
};
```

> The same `FindPlayerByName` / `FindPlayerByIdentity` pair is the reusable "find a player" snippet referenced from the [admin panel tutorial](03-admin-panel.md). Keep it in one place and call it from every command rather than re-writing the loop each time.

### Create `Scripts/3_Game/ChatCommands/CCmdRegistry.c`

```c
// -------------------------------------------------------
// Registry that holds all available commands
// -------------------------------------------------------
class CCmdRegistry
{
    protected static ref map<string, ref CCmdBase> s_Commands;

    // -------------------------------------------------------
    // Initialize the registry (call once at startup)
    // -------------------------------------------------------
    static void Init()
    {
        if (!s_Commands)
            s_Commands = new map<string, ref CCmdBase>;
    }

    // -------------------------------------------------------
    // Register a command instance
    // -------------------------------------------------------
    static void Register(CCmdBase command)
    {
        if (!s_Commands)
            Init();

        if (!command)
            return;

        string name = command.GetName();
        name.ToLower();

        if (s_Commands.Contains(name))
        {
            Print("[ChatCommands] WARNING: Command '" + name + "' already registered, overwriting.");
        }

        s_Commands.Set(name, command);
        Print("[ChatCommands] Registered command: /" + name);
    }

    // -------------------------------------------------------
    // Look up a command by name
    // -------------------------------------------------------
    static CCmdBase GetCommand(string name)
    {
        if (!s_Commands)
            return null;

        string nameLower = name;
        nameLower.ToLower();

        CCmdBase cmd;
        if (s_Commands.Find(nameLower, cmd))
            return cmd;

        return null;
    }

    // -------------------------------------------------------
    // Get all registered command names
    // -------------------------------------------------------
    static array<string> GetCommandNames()
    {
        ref array<string> names = new array<string>;

        if (s_Commands)
        {
            for (int i = 0; i < s_Commands.Count(); i++)
            {
                names.Insert(s_Commands.GetKey(i));
            }
        }

        return names;
    }

    // -------------------------------------------------------
    // Parse a raw command string into name + args
    // Example: "/heal PlayerName" --> name="heal", args=["PlayerName"]
    // -------------------------------------------------------
    static void ParseCommand(string fullCommand, out string commandName, out array<string> args)
    {
        args = new array<string>;
        commandName = "";

        if (fullCommand.Length() == 0)
            return;

        // Remove the leading /
        string raw = fullCommand;
        if (raw.Substring(0, 1) == "/")
            raw = raw.Substring(1, raw.Length() - 1);

        // Split by spaces
        raw.Split(" ", args);

        if (args.Count() > 0)
        {
            commandName = args.Get(0);
            commandName.ToLower();
            args.RemoveOrdered(0);
        }
    }
};
```

### The Parse Logic Explained

Given the input `/heal SomePlayer`, `ParseCommand` does:

1. Removes the leading `/` to get `"heal SomePlayer"`
2. Splits by spaces to get `["heal", "SomePlayer"]`
3. Takes the first element as the command name: `"heal"`
4. Removes it from the array, leaving args: `["SomePlayer"]`

The command name is converted to lowercase so `/Heal`, `/HEAL`, and `/heal` all work.

---

## Step 3: Check Admin Permissions

Admin permission checking prevents regular players from executing admin commands. DayZ does not have a built-in admin permission system in scripts, so we check the player's Steam64 ID against a list of known admins.

The check itself is implemented **once**, as a method of the server handler you build in [Step 6](#step-6-register-commands-and-handle-the-rpc). The idea:

```c
// Conceptual sketch -- the real method (IsCommandAdmin) lives in the
// server handler in Step 6. Do not duplicate it.
string playerId = identity.GetPlainId();   // plaintext Steam64 ID
bool allowed = (adminIds.Find(playerId) != -1);
```

### Where to Find Steam64 IDs

- Open your Steam profile in a browser
- The URL contains your Steam64 ID: `https://steamcommunity.com/profiles/76561198XXXXXXXXX`
- Or use a lookup site such as https://steamid.io

### Production-Grade Permissions

In a real mod, you would:

1. Store admin IDs in a JSON file (`$profile:ChatCommands/admins.json`)
2. Load the file on server startup
3. Support permission levels (moderator, admin, superadmin)
4. Use a framework's hierarchical permission system -- the wiki's Lantern example exposes `LNT_Permissions` for exactly this (see [Chapter 7.5](../07-patterns/05-permissions.md))

---

## Step 4: Execute the Server-Side Action

Now we create the actual `/heal` command. It references `PlayerBase` and player stat methods, so it must live in `4_World` or higher.

### Create `Scripts/4_World/ChatCommands/commands/CCmdHeal.c`

```c
class CCmdHeal extends CCmdBase
{
    override string GetName()
    {
        return "heal";
    }

    override string GetDescription()
    {
        return "Fully heals a player (health, blood, shock, hunger, thirst)";
    }

    override string GetUsage()
    {
        return "/heal [PlayerName]";
    }

    override bool RequiresAdmin()
    {
        return true;
    }

    // -------------------------------------------------------
    // Execute the heal command
    // /heal         --> heals the caller
    // /heal Name    --> heals the named player
    // -------------------------------------------------------
    override bool Execute(PlayerIdentity caller, array<string> args)
    {
        if (!caller)
            return false;

        Man targetMan = null;
        string targetName = "";

        if (args.Count() > 0)
        {
            // Heal a specific player by name
            string searchName = args.Get(0);
            targetMan = FindPlayerByName(searchName);

            if (!targetMan)
            {
                SendFeedback(caller, "[Heal]", "Player '" + searchName + "' not found.");
                return false;
            }

            targetName = targetMan.GetIdentity().GetName();
        }
        else
        {
            // Heal the caller themselves (shared helper from CCmdBase)
            targetMan = FindPlayerByIdentity(caller);

            if (!targetMan)
            {
                SendFeedback(caller, "[Heal]", "Could not find your player object.");
                return false;
            }

            targetName = "yourself";
        }

        PlayerBase targetPlayer;
        if (!Class.CastTo(targetPlayer, targetMan))
        {
            SendFeedback(caller, "[Heal]", "Target is not a valid player.");
            return false;
        }

        HealPlayer(targetPlayer);

        Print("[ChatCommands] " + caller.GetName() + " healed " + targetName);
        SendFeedback(caller, "[Heal]", "Successfully healed " + targetName + ".");

        return true;
    }

    // -------------------------------------------------------
    // Apply a full heal to a player
    // -------------------------------------------------------
    protected void HealPlayer(PlayerBase player)
    {
        if (!player)
            return;

        // Restore the three health values to their maximums
        player.SetHealth("GlobalHealth", "Health", player.GetMaxHealth("GlobalHealth", "Health"));
        player.SetHealth("GlobalHealth", "Blood", player.GetMaxHealth("GlobalHealth", "Blood"));
        player.SetHealth("GlobalHealth", "Shock", player.GetMaxHealth("GlobalHealth", "Shock"));

        // Refill hunger (energy) and thirst (water) stats
        if (player.GetStatEnergy())
            player.GetStatEnergy().Set(player.GetStatEnergy().GetMax());

        if (player.GetStatWater())
            player.GetStatWater().Set(player.GetStatWater().GetMax());

        // Clear any active bleeding sources
        if (player.GetBleedingManagerServer())
            player.GetBleedingManagerServer().RemoveAllSources();
    }
};
```

### Why 4_World?

The heal command references `PlayerBase`, which is defined in the `4_World` layer, and calls stat methods (`GetStatEnergy`, `GetStatWater`, `GetBleedingManagerServer`) that only exist on world entities. The base class `CCmdBase` lives in `3_Game` because it references only `Man` and `PlayerIdentity`. Concrete commands that touch world entities live in `4_World`.

---

## Step 5: Send Feedback to the Admin

Feedback travels back to the caller as a target-less RPC, and the client receives it in `DayZGame.OnRPC` -- the same client-side receiver used by the [admin panel tutorial](03-admin-panel.md). `MissionGameplay` has no `OnRPC` method, so the receiver must mod `DayZGame`.

### Server Sends Feedback

`CCmdBase.SendFeedback()` (Step 2) sends the RPC with `target = null` and `recipient = caller`:

```c
Param2<string, string> data = new Param2<string, string>(prefix, message);
GetGame().RPCSingleParam(null, CCmdRPC.COMMAND_FEEDBACK, data, true, caller);
```

The `null` target means the client routes this RPC to `DayZGame.OnRPC` (not to a specific entity), and the `recipient` restricts delivery to the one client who issued the command.

### Client Receives and Displays Feedback

### Create `Scripts/5_Mission/ChatCommands/CCmdClientRPC.c`

```c
modded class DayZGame
{
    // -------------------------------------------------------
    // DayZGame.OnRPC is the engine's catch-all client handler.
    // Its switch only runs for target-less RPCs (target == null).
    // -------------------------------------------------------
    override void OnRPC(PlayerIdentity sender, Object target, int rpc_type, ParamsReadContext ctx)
    {
        super.OnRPC(sender, target, rpc_type, ctx);

        if (rpc_type == CCmdRPC.COMMAND_FEEDBACK)
        {
            Param2<string, string> data = new Param2<string, string>("", "");
            if (ctx.Read(data))
            {
                string prefix = data.param1;
                string message = data.param2;

                // Display feedback as a system chat message
                GetGame().Chat(prefix + " " + message, "colorStatusChannel");

                Print("[ChatCommands] Feedback: " + prefix + " " + message);
            }
        }
    }
};
```

`GetGame().Chat(text, colorClass)` displays a local message in the player's chat window. The color class selects the text color:

| Color class | Color | Typical use |
|-------------|-------|-------------|
| `"colorStatusChannel"` | Blue | System messages |
| `"colorAction"` | Yellow | Action feedback |
| `"colorFriendly"` | Green | Positive feedback |
| `"colorImportant"` | Red | Warnings / errors |

These four classes are the only ones vanilla maps to a color; any other string falls back to white.

---

## Step 6: Register Commands and Handle the RPC

Two pieces run on the server: registering commands when the mission starts, and handling incoming command RPCs on the player object.

### Register commands -- `Scripts/5_Mission/ChatCommands/CCmdRegister.c`

`MissionServer` is defined in the `5_Mission` layer, so a `modded class MissionServer` must live in `5_Mission` (not `4_World`).

```c
modded class MissionServer
{
    override void OnInit()
    {
        super.OnInit();

        CCmdRegistry.Init();

        // Register all commands here
        CCmdRegistry.Register(new CCmdHeal());

        // Add more commands:
        // CCmdRegistry.Register(new CCmdKill());
        // CCmdRegistry.Register(new CCmdTeleport());
        // CCmdRegistry.Register(new CCmdTime());

        Print("[ChatCommands] Server initialized. Commands registered.");
    }
};
```

### Handle the RPC -- `Scripts/4_World/ChatCommands/CCmdServerHandler.c`

The command request arrives on the player object (Step 1 sent it with the player as target), so the handler mods `PlayerBase`, which lives in `4_World`.

```c
modded class PlayerBase
{
    override void OnRPC(PlayerIdentity sender, int rpc_type, ParamsReadContext ctx)
    {
        super.OnRPC(sender, rpc_type, ctx);

        if (!GetGame().IsServer())
            return;

        if (rpc_type == CCmdRPC.COMMAND_REQUEST)
        {
            HandleCommandRPC(sender, ctx);
        }
    }

    protected void HandleCommandRPC(PlayerIdentity sender, ParamsReadContext ctx)
    {
        if (!sender)
            return;

        // Read the command string
        Param1<string> data = new Param1<string>("");
        if (!ctx.Read(data))
        {
            Print("[ChatCommands] ERROR: Failed to read command RPC data.");
            return;
        }

        string fullCommand = data.param1;
        Print("[ChatCommands] Received command from " + sender.GetName() + ": " + fullCommand);

        // Parse the command
        string commandName;
        ref array<string> args;
        CCmdRegistry.ParseCommand(fullCommand, commandName, args);

        if (commandName == "")
            return;

        // Look up the command
        CCmdBase command = CCmdRegistry.GetCommand(commandName);
        if (!command)
        {
            SendCommandFeedback(sender, "[Error]", "Unknown command: /" + commandName);
            return;
        }

        // Check admin permissions
        if (command.RequiresAdmin() && !IsCommandAdmin(sender))
        {
            Print("[ChatCommands] Non-admin " + sender.GetName() + " tried to use /" + commandName);
            SendCommandFeedback(sender, "[Error]", "You do not have permission to use this command.");
            return;
        }

        // Execute the command
        bool success = command.Execute(sender, args);

        if (success)
            Print("[ChatCommands] Command /" + commandName + " executed by " + sender.GetName());
        else
            Print("[ChatCommands] Command /" + commandName + " failed for " + sender.GetName());
    }

    // -------------------------------------------------------
    // The single admin check for the whole system.
    // -------------------------------------------------------
    protected bool IsCommandAdmin(PlayerIdentity identity)
    {
        if (!identity)
            return false;

        string playerId = identity.GetPlainId();

        // ----------------------------------------------------------
        // Replace these with your real admin Steam64 IDs. In
        // production, load them from a JSON config file instead.
        // ----------------------------------------------------------
        ref array<string> adminIds = new array<string>;
        adminIds.Insert("76561198000000001");
        adminIds.Insert("76561198000000002");

        return (adminIds.Find(playerId) != -1);
    }

    // -------------------------------------------------------
    // Feedback for handler-level messages (unknown command,
    // permission denied). Same target-less form as CCmdBase.
    // -------------------------------------------------------
    protected void SendCommandFeedback(PlayerIdentity target, string prefix, string message)
    {
        if (!target)
            return;

        Param2<string, string> data = new Param2<string, string>(prefix, message);
        GetGame().RPCSingleParam(null, CCmdRPC.COMMAND_FEEDBACK, data, true, target);
    }
};
```

### The Registration Pattern

Each `Register()` call creates an instance of a command class and stores it in a map keyed by the command name. When a command RPC arrives, the handler looks up the name in the registry and calls `Execute()` on the matching command object. Adding a command is trivial: create a class extending `CCmdBase`, implement `Execute()`, and add one `Register()` line.

---

## Step 7: List Commands in an Admin Panel

If you have an admin panel (from [Chapter 8.3](03-admin-panel.md)), you can display the list of available commands in the UI.

### Add RPC IDs in `CCmdRPC.c`

```c
class CCmdRPC
{
    static const int COMMAND_REQUEST   = 79001;
    static const int COMMAND_FEEDBACK  = 79002;
    static const int COMMAND_LIST_REQ  = 79003;
    static const int COMMAND_LIST_RESP = 79004;
};
```

### Server-Side: Send the Command List

Add a branch to the server `OnRPC` for `COMMAND_LIST_REQ`, and build the list from the registry:

```c
protected void HandleCommandListRequest(PlayerIdentity requestor)
{
    if (!requestor)
        return;

    array<string> names = CCmdRegistry.GetCommandNames();
    string commandList = "Available Commands:\n";

    for (int i = 0; i < names.Count(); i++)
    {
        CCmdBase cmd = CCmdRegistry.GetCommand(names.Get(i));
        if (cmd)
        {
            commandList = commandList + cmd.GetUsage() + " - " + cmd.GetDescription() + "\n";
        }
    }

    // Target-less RPC to the requesting client only
    Param1<string> data = new Param1<string>(commandList);
    GetGame().RPCSingleParam(null, CCmdRPC.COMMAND_LIST_RESP, data, true, requestor);
}
```

### Client-Side: Display in a Panel

In the `DayZGame.OnRPC` handler from Step 5, add a branch for `COMMAND_LIST_RESP`:

```c
if (rpc_type == CCmdRPC.COMMAND_LIST_RESP)
{
    Param1<string> data = new Param1<string>("");
    if (ctx.Read(data))
    {
        string commandList = data.param1;
        // Push commandList into your admin panel text widget, e.g.:
        // m_CommandListText.SetText(commandList);
        Print("[ChatCommands] Command list received:\n" + commandList);
    }
}
```

---

## Mod Registration (config.cpp)

Register all three script layers so the engine loads them in order. `3_Game` compiles first (RPC IDs, base classes), then `4_World` (server handler, commands), then `5_Mission` (chat hook, client receiver, registration).

### `ChatCommands/Scripts/config.cpp`

```cpp
class CfgPatches
{
    class ChatCommands_Scripts
    {
        units[] = {};
        weapons[] = {};
        requiredVersion = 0.1;
        requiredAddons[] =
        {
            "DZ_Data",
            "DZ_Scripts"
        };
    };
};

class CfgMods
{
    class ChatCommands
    {
        dir = "ChatCommands";
        name = "Chat Commands";
        author = "YourName";
        type = "mod";

        dependencies[] = { "Game", "World", "Mission" };

        class defs
        {
            class gameScriptModule
            {
                value = "";
                files[] = { "ChatCommands/Scripts/3_Game" };
            };
            class worldScriptModule
            {
                value = "";
                files[] = { "ChatCommands/Scripts/4_World" };
            };
            class missionScriptModule
            {
                value = "";
                files[] = { "ChatCommands/Scripts/5_Mission" };
            };
        };
    };
};
```

Every code file shown in this tutorial has already been listed in full under its own step; there is no separate combined listing to copy. Create each file at the path given in [Mod Structure](#mod-structure-for-this-tutorial), then build and load.

---

## Adding More Commands

The registry pattern makes adding new commands straightforward. Each new command is a class extending `CCmdBase`, placed in `4_World` (or higher if it touches world types).

### /kill Command

```c
class CCmdKill extends CCmdBase
{
    override string GetName()        { return "kill"; }
    override string GetDescription() { return "Kills a player"; }
    override string GetUsage()       { return "/kill [PlayerName]"; }

    override bool Execute(PlayerIdentity caller, array<string> args)
    {
        Man targetMan = null;

        if (args.Count() > 0)
            targetMan = FindPlayerByName(args.Get(0));
        else
            targetMan = FindPlayerByIdentity(caller);

        if (!targetMan)
        {
            SendFeedback(caller, "[Kill]", "Player not found.");
            return false;
        }

        PlayerBase targetPlayer;
        if (Class.CastTo(targetPlayer, targetMan))
        {
            targetPlayer.SetHealth("GlobalHealth", "Health", 0);
            SendFeedback(caller, "[Kill]", "Killed " + targetMan.GetIdentity().GetName() + ".");
            return true;
        }

        return false;
    }
};
```

### /time Command

```c
class CCmdTime extends CCmdBase
{
    override string GetName()        { return "time"; }
    override string GetDescription() { return "Sets the server time (0-23)"; }
    override string GetUsage()       { return "/time <hour>"; }

    override bool Execute(PlayerIdentity caller, array<string> args)
    {
        if (args.Count() < 1)
        {
            SendFeedback(caller, "[Time]", "Usage: " + GetUsage());
            return false;
        }

        int hour = args.Get(0).ToInt();
        if (hour < 0 || hour > 23)
        {
            SendFeedback(caller, "[Time]", "Hour must be between 0 and 23.");
            return false;
        }

        GetGame().GetWorld().SetDate(2024, 6, 15, hour, 0);
        SendFeedback(caller, "[Time]", "Server time set to " + hour.ToString() + ":00.");
        return true;
    }
};
```

### Registering New Commands

Add one line per command in `MissionServer.OnInit()` (Step 6):

```c
CCmdRegistry.Register(new CCmdHeal());
CCmdRegistry.Register(new CCmdKill());
CCmdRegistry.Register(new CCmdTime());
```

---

## Troubleshooting

### Command Is Not Recognized ("Unknown command")

- **Registration missing:** Make sure `CCmdRegistry.Register(new CCmdYourCommand())` is called in `MissionServer.OnInit()`.
- **GetName() typo:** The string returned by `GetName()` must match what the player types (without the `/`).
- **Case mismatch:** The registry converts names to lowercase. `/Heal`, `/HEAL`, and `/heal` should all work.

### Permission Denied for Admins

- **Wrong Steam64 ID:** Double-check the admin IDs in `IsCommandAdmin()`. They must be exact Steam64 IDs (17-digit numbers starting with `7656`).
- **`GetPlainId()` vs `GetId()`:** `GetPlainId()` returns the plaintext Steam64 ID. `GetId()` returns a stable hashed unique ID (safe for databases and logs), not a session ID -- the per-session ID that is reused after a player disconnects is `GetPlayerId()` (an int). Use `GetPlainId()` for admin checks.

### Feedback Message Does Not Appear in Chat

- **RPC not target-less:** The feedback must be sent with `target = null` and `recipient = caller`. If you pass the player object as target, it routes to `PlayerBase.OnRPC` on the client instead of `DayZGame.OnRPC`.
- **Client `DayZGame.OnRPC` not catching it:** Verify the RPC ID matches (`CCmdRPC.COMMAND_FEEDBACK`) and that you call `super.OnRPC()`.
- **`GetGame().Chat()` not active:** This requires the game to be in a state where chat is available. It may be silently dropped on the loading screen.

### /heal Does Not Actually Heal

- **Server-only execution:** `SetHealth()` and stat changes must run on the server. The handler already guards with `GetGame().IsServer()`; make sure your command's `Execute()` is reached from that path.
- **PlayerBase cast fails:** If `Class.CastTo(targetPlayer, targetMan)` returns false, the target is not a valid `PlayerBase` (for example an AI entity).
- **Stat getters return null:** `GetStatEnergy()`, `GetStatWater()`, and `GetBleedingManagerServer()` can return null if the player is dead or not fully initialized. The `HealPlayer()` method above null-checks each one before use.

### Command Still Appears in Chat

- **Wrong interception point:** Suppression only works if you mod `ChatInputMenu.OnChange` and skip `super` for `/` messages, as in Step 1. If you instead read the later `ChatMessageEventTypeID` event, vanilla has already called `g_Game.ChatPlayer()` and the text has been broadcast -- too late to suppress.
- **You called super anyway:** In the command branch you must `return true` *without* calling `super.OnChange()`. Falling through to `super` re-broadcasts the text.

---

## Best Practices

- **Always check permissions before executing admin commands.** A missing permission check means any player can `/heal` or `/kill` anyone. Validate the caller's Steam64 ID (via `GetPlainId()`) on the server before processing.
- **Send feedback to the admin even for failed commands.** Silent failures make debugging impossible. Always send a chat message explaining what went wrong ("Player not found", "Permission denied").
- **Use `GetPlainId()` for admin checks, not `GetId()`.** `GetId()` returns a stable hashed unique ID intended for databases and logs (the per-session ID reused after a player disconnects is `GetPlayerId()`). `GetPlainId()` returns the plaintext Steam64 ID.
- **Store admin IDs in a JSON config file, not in code.** Hardcoded IDs require a PBO rebuild to change. A `$profile:` JSON file can be edited by server admins without modding knowledge.
- **Convert command names to lowercase before matching.** Players may type `/Heal`, `/HEAL`, or `/heal`. Normalizing to lowercase prevents frustrating "unknown command" errors.

---

## Theory vs Practice

| Concept | Theory | Reality |
|---------|--------|---------|
| Chat hook via `ChatInputMenu.OnChange` | Intercept the message before it is broadcast | Works reliably because it runs *before* `g_Game.ChatPlayer()`. `m_edit_box` is `private` in vanilla, but a `modded class` is still allowed to read it -- Bohemia documents that explicitly. Prefer `EditBoxWidget.Cast(w)` anyway: `w` is the widget that fired the event, and a private field name is an internal detail that can change between patches. |
| `GetGame().Chat()` | Displays a message in the player's chat window | Only works when the chat UI is active. On the loading screen or in certain menu states, the message is silently dropped. |
| Command registry pattern | Clean architecture with one class per command | Each command class must go in the correct script layer. `CCmdBase` in `3_Game`, commands referencing `PlayerBase` in `4_World`, `modded MissionServer` in `5_Mission`. Wrong layer placement causes "Undefined type" at load time. |
| Player lookup by name | `FindPlayerByName` matches partial names | Partial matching can target the wrong player on a server with similar names. In production, prefer Steam64 ID targeting or add a confirmation step. |

---

## What You Learned

In this tutorial you learned:

- How to intercept chat input at `ChatInputMenu.OnChange` and suppress command text from being broadcast
- How to parse command prefixes and arguments from chat text
- How to check admin permissions on the server using Steam64 IDs, implemented in one place
- How to send command feedback back to the player via a target-less RPC received in `DayZGame.OnRPC`
- How to build a reusable command registry with one shared "find a player" helper across commands
