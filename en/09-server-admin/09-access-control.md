# Access Control


---

> **Summary:** Configure who can connect to your DayZ server, how bans work, how to enable remote administration, and how mod signature verification keeps unauthorized content out. This chapter covers every access control mechanism available to a server operator.

---

## Table of Contents

- [Admin Access via serverDZ.cfg](#admin-access-via-serverdzcfg)
- [ban.txt](#bantxt)
- [whitelist.txt](#whitelisttxt)
- [Which identifier goes in these files](#which-identifier-goes-in-these-files)
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

The file **ban.txt** lives in your server root directory. It holds one identifier per line — what form that identifier takes is not documented by Bohemia:

```
kBmDmSc4S3uVuKAJsBZTrh-jLWNJ3eX0_VsT2eXyV1Y=
DCV63zXcS_oWzPfED-PWAJVnJ3wOQ4_jE4WnZdfBkW8=
```

- Each line is one player identifier. **Which identifier form the engine matches on is not documented by Bohemia** -- see [Which identifier goes in these files](#which-identifier-goes-in-these-files) below before you populate the file.
- The 44-character DayZ player UID shown above is the identifier printed in the `*.ADM` and `*.RPT` logs, and is the form most community guides use here.
- You can add a comment after an ID using the `//` prefix on the same line, or on its own commented-out line.
- Players whose listed identifier the engine matches are refused connection at join time. Which form it matches on is the open question below, so verify before relying on a ban.
- The use of **ban.txt** can be toggled with `disableBanlist` in **serverDZ.cfg** (default `false`).
- You can edit the file while the server is running; changes take effect on the next connection attempt.

---

## whitelist.txt

The file **whitelist.txt** sits in the same server root directory. When you enable whitelisting (`enableWhitelist = 1` in **serverDZ.cfg**), only players listed in this file can connect — again, in an identifier form Bohemia does not document:

```
kBmDmSc4S3uVuKAJsBZTrh-jLWNJ3eX0_VsT2eXyV1Y=
DCV63zXcS_oWzPfED-PWAJVnJ3wOQ4_jE4WnZdfBkW8=
```

The format is the same as **ban.txt** -- one identifier per line, with optional `//` comments -- and the same open question about which identifier form applies.

---

## Which identifier goes in these files

Be careful here: this wiki cannot tell you authoritatively, and neither can most guides that sound certain.

**What is documented.** Bohemia publishes no description of the `ban.txt` or `whitelist.txt` entry format -- there is no page for either file on the community wiki, and the [Server Configuration](https://community.bistudio.com/wiki/DayZ:Server_Configuration) reference mentions them only as things `disableBanlist` and `enableWhitelist` switch on and off. The one list file Bohemia *does* show a format for is the sibling `priority.txt`, and that example uses **17-digit SteamID64-shaped numbers separated by semicolons**, not the 44-character UID and not one per line:

```
SteamId;SteamId;01234567890123456;01234567890123456
```

**What is inferable, and what is not.** A connected player has two identifiers in the engine. `scripts/3_game/gameplay.c` documents `PlayerIdentity.GetId()` as the *"unique id of player (hashed steamID, database Xbox id...) can be used in database or logs"* -- this is the 44-character value you see in `.ADM` logs -- and `GetPlainId()` as the *"plaintext unique id of player (cannot be used in database or logs)"*. Both exist. Nothing in the script tree says which one the engine's ban/whitelist reader compares an incoming connection against, because that reader is engine-side. Do not read the log-safety comment on `GetPlainId()` as a rule about these files; it is about logging, not matching.

**What community sources say.** They disagree. Hosting-vendor knowledge bases and forum guides can be found asserting each form, and some baseline server packages label the entries as SteamID64 while other guides insist on the 44-character UID.

**What to do.** Test it rather than trusting any guide, including this one:

1. Get a throwaway account's identifier in both forms -- the 44-character UID from your `.ADM` log after it connects once, and its SteamID64 from its Steam profile.
2. Put one form in `ban.txt`, restart or reconnect, and try to join.
3. If it connects, swap in the other form and repeat.

Confirm the behaviour on **your** server build before you rely on a ban list for moderation. A ban list you believe in but that silently does nothing is worse than no ban list.

Whitelisting is useful for private communities, testing servers, or events where you need a controlled player list.

---

## BattlEye Anti-Cheat

BattlEye is the anti-cheat system integrated into DayZ. Its files live in the `BattlEye/` folder inside your server directory:

| File | Purpose |
|------|---------|
| **BEServer_x64.dll** | The BattlEye anti-cheat engine binary |
| **beserver_x64.cfg** | Configuration file (RCON port, RCON password) |
| **bans.txt** | BattlEye-specific bans (GUID-based, not SteamID) |

BattlEye is enabled by default. You launch the server with `DayZServer_x64.exe` and BattlEye loads automatically. To explicitly disable it (not recommended for production), set `BattlEye = 0;` in **serverDZ.cfg**.

The **bans.txt** file in the `BattlEye/` folder uses BattlEye GUIDs, which are different from SteamID64s. Bans issued through RCON or BattlEye commands write to this file automatically.

---

## RCON (Remote Console)

BattlEye RCON lets you administer the server remotely without being in-game. Configure it in `BattlEye/beserver_x64.cfg`:

```
RConPassword yourpassword
RConPort 2306
```

BattlEye does not use a fixed default RCON port -- if you omit `RConPort`, it listens on a random port. Set it explicitly, and pick a value outside the block your server already uses for game traffic and the Steam query port. A stock setup on `-port=2302` with the conventional `steamQueryPort = 2305` occupies `2302`-`2305` UDP, so `2306` is a safe RCON port. Note that Bohemia documents no *default* for `steamQueryPort` -- 2305 is the value in its sample config and the value most installations end up on, not a guaranteed engine default -- so check what your own config actually sets before choosing an RCON port.

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
| `0` | Legacy/unsupported -- historically disabled signature checks, but current server documentation states only `2` is a supported value. Do not rely on `0` behaving predictably on current game builds. |
| `2` | Full verification -- clients must have valid signatures for all loaded mods (the only officially supported value; also the default) |

Always use `verifySignatures = 2` on production (and any other) servers -- it is the only value Bohemia documents as supported. See [serverDZ.cfg Reference](03-server-cfg.md#network-security) for the authoritative parameter entry.

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

These tools are built into the vanilla game. Third-party admin mods (such as Community Online Tools or VPP Admin Tools) extend admin capabilities significantly.

---

## Common Mistakes

These are the problems server operators hit most often:

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Missing `.bikey` in `keys/` | Players get kicked on join with a signature error | Copy the mod's `.bikey` file into your server's `keys/` directory |
| Assuming an identifier form in **ban.txt** without testing it | Bans silently do not work | Bohemia documents no format for this file. Verify with a throwaway account -- see [Which identifier goes in these files](#which-identifier-goes-in-these-files) |
| RCON port conflict | RCON client cannot connect | Ensure the RCON port is not used by another service; check firewall rules |
| `verifySignatures = 0` in production | Anyone can join with tampered mods | Set it to `2` on any public-facing server |
| Forgetting to open RCON port in firewall | RCON client times out | Open the RCON UDP port (the one you set with `RConPort`, e.g. `2306`) in your firewall |
| Confusing BattlEye's **bans.txt** with the server-root **ban.txt** | Bans do not work | They are two different files with two different readers. BattlEye's `BattlEye/bans.txt` takes BattlEye GUIDs; the server-root `ban.txt` is the one `disableBanlist` switches, and Bohemia documents no entry format for it — see [Which identifier goes in these files](#which-identifier-goes-in-these-files) |
