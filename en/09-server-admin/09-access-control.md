# Chapter 9.9: Access Control

[Home](../README.md) | [<< Previous: Performance Tuning](08-performance.md) | [Next: Mod Management >>](10-mod-management.md)

---

> **Summary:** Configure who can connect to your DayZ server, how bans work, how to enable remote administration, and how mod signature verification keeps unauthorized content out. This chapter covers every access control mechanism available to a server operator.

---

## Table of Contents

- [Admin Access via serverDZ.cfg](#admin-access-via-serverdzcfg)
- [ban.txt](#bantxt)
- [whitelist.txt](#whitelisttxt)
- [BattlEye Anti-Cheat](#battleye-anti-cheat)
- [RCON (Remote Console)](#rcon-remote-console)
- [Signature Verification](#signature-verification)
- [The keys/ Directory](#the-keys-directory)
- [In-Game Admin Tools](#in-game-admin-tools)
- [Common Mistakes](#common-mistakes)

---

## Admin Access via serverDZ.cfg

The `passwordAdmin` parameter in **serverDZ.cfg** sets the admin password for your server:

```cpp
passwordAdmin = "YourSecretPassword";
```

You use this password in two ways:

1. **In-game** -- open the chat and type `#login YourSecretPassword` to gain admin privileges for that session.
2. **RCON** -- connect with a BattlEye RCON client using this password (see the RCON section below).

Keep the admin password long and unique. Anyone with it has full control over the running server.

---

## ban.txt

The file **ban.txt** lives in your server profile directory (the path you set with `-profiles=`). It contains one SteamID64 per line:

```
76561198012345678
76561198087654321
```

- Each line is a bare 17-digit SteamID64 -- no names, no comments, no passwords.
- Players whose SteamID appears in this file are refused connection at join time.
- You can edit the file while the server is running; changes take effect on the next connection attempt.

---

## whitelist.txt

The file **whitelist.txt** sits in the same profile directory. When you enable whitelisting, only SteamIDs listed in this file can connect:

```
76561198012345678
76561198087654321
```

The format is identical to **ban.txt** -- one SteamID64 per line, nothing else.

Whitelisting is useful for private communities, testing servers, or events where you need a controlled player list.

---

## BattlEye Anti-Cheat

BattlEye is the anti-cheat system integrated into DayZ. Its files live in the `BattlEye/` folder inside your server directory:

| File | Purpose |
|------|---------|
| **BEServer_x64.dll** | The BattlEye anti-cheat engine binary |
| **beserver_x64.cfg** | Configuration file (RCON port, RCON password) |
| **bans.txt** | BattlEye-specific bans (GUID-based, not SteamID) |

BattlEye is enabled by default. You launch the server with `DayZServer_x64.exe` and BattlEye loads automatically. To explicitly disable it (not recommended for production), use the `-noBE` launch parameter.

The **bans.txt** file in the `BattlEye/` folder uses BattlEye GUIDs, which are different from SteamID64s. Bans issued through RCON or BattlEye commands write to this file automatically.

---

## RCON (Remote Console)

BattlEye RCON lets you administer the server remotely without being in-game. Configure it in `BattlEye/beserver_x64.cfg`:

```
RConPassword yourpassword
RConPort 2306
```

The default RCON port is your game port plus 4. If your server runs on port `2302`, RCON defaults to `2306`.

### Available RCON Commands

| Command | Effect |
|---------|--------|
| `kick <player> [reason]` | Kick a player from the server |
| `ban <player> [minutes] [reason]` | Ban a player (writes to BattlEye bans.txt) |
| `say -1 <message>` | Broadcast a message to all players |
| `#shutdown` | Graceful server shutdown |
| `#lock` | Lock the server (no new connections) |
| `#unlock` | Unlock the server |
| `players` | List connected players |

You connect to RCON using a BattlEye RCON client (several free tools exist). The connection requires the IP, RCON port, and the password from **beserver_x64.cfg**.

---

## Signature Verification

The `verifySignatures` parameter in **serverDZ.cfg** controls whether the server checks mod signatures:

```cpp
verifySignatures = 2;
```

| Value | Behavior |
|-------|----------|
| `0` | Disabled -- anyone can join with any mods, no signature checks |
| `2` | Full verification -- clients must have valid signatures for all loaded mods (default) |

Always use `verifySignatures = 2` on production servers. Setting it to `0` allows players to join with modified or unsigned mods, which is a serious security risk.

---

## The keys/ Directory

The `keys/` directory in your server root holds **.bikey** files. Each `.bikey` corresponds to a mod and tells the server "this mod's signatures are trusted."

When `verifySignatures = 2`:

1. The server checks every mod the connecting client has loaded.
2. For each mod, the server looks for a matching `.bikey` in `keys/`.
3. If a matching key is missing, the player is kicked.

Every mod you install on the server ships with a `.bikey` file (usually in the mod's `Keys/` or `Key/` subfolder). You copy that file into your server's `keys/` directory.

```
DayZServer/
├── keys/
│   ├── dayz.bikey              ← vanilla (always present)
│   ├── MyMod.bikey             ← copied from @MyMod/Keys/
│   └── AnotherMod.bikey        ← copied from @AnotherMod/Keys/
```

If you add a new mod and forget to copy its `.bikey`, every player running that mod gets kicked on connect.

---

## In-Game Admin Tools

Once you log in with `#login <password>` in chat, you gain access to the admin tools:

- **Player list** -- view all connected players with their SteamIDs.
- **Kick/ban** -- remove or ban players directly from the player list.
- **Teleport** -- use the admin map to teleport to any position.
- **Admin log** -- server-side log of player actions (kills, connections, disconnections) written to `*.ADM` files in the profile directory.
- **Free camera** -- detach from your character and fly around the map.

These tools are built into the vanilla game. Third-party mods (such as Community Online Tools) extend admin capabilities significantly.

---

## Common Mistakes

These are the problems server operators hit most often:

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Missing `.bikey` in `keys/` | Players get kicked on join with a signature error | Copy the mod's `.bikey` file into your server's `keys/` directory |
| Putting names or passwords in **ban.txt** | Bans do not work; random errors | Use only bare SteamID64 values, one per line |
| RCON port conflict | RCON client cannot connect | Ensure the RCON port is not used by another service; check firewall rules |
| `verifySignatures = 0` in production | Anyone can join with tampered mods | Set it to `2` on any public-facing server |
| Forgetting to open RCON port in firewall | RCON client times out | Open the RCON UDP port (default 2306) in your firewall |
| Editing **bans.txt** in `BattlEye/` with SteamIDs | Bans do not work | BattlEye **bans.txt** uses GUIDs, not SteamIDs; use **ban.txt** in the profile directory for SteamID bans |

---

[Home](../README.md) | [<< Previous: Performance Tuning](08-performance.md) | [Next: Mod Management >>](10-mod-management.md)
