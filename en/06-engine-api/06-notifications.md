# Notification System


---

## Introduction

DayZ includes a built-in notification system for displaying toast-style popup messages to players. The `NotificationSystem` class provides static methods for sending notifications both locally (client-side) and from server to client via RPC. This chapter covers the full API for sending, customizing, and managing notifications.

---

## NotificationSystem

**File:** `3_Game/client/notifications/notificationsystem.c` (320 lines)

A static class that manages the notification queue. Notifications appear as small popup cards at the top of the screen, stacked vertically, and fade out after their display time expires.

### Constants

```c
const int   DEFAULT_TIME_DISPLAYED = 10;    // Default display time in seconds
const float NOTIFICATION_FADE_TIME = 3.0;   // Fade-out duration in seconds
protected static const int MAX_NOTIFICATIONS = 5;  // Max simultaneously visible; it is
                                            // protected, so mod script cannot read it
```

---

## Server-to-Client Notifications

These methods are called on the server. They send an RPC to the target player's client, which displays the notification locally.

### SendNotificationToPlayerExtended

```c
static void SendNotificationToPlayerExtended(
    Man player,            // Target player (Man or PlayerBase)
    float show_time,       // Display duration in seconds
    string title_text,     // Notification title
    string detail_text = "",  // Optional body text
    string icon = ""       // Optional icon path (e.g., "set:dayz_gui image:notification_friend")
);
```

**Example --- notify a specific player:**

```c
void NotifyPlayer(PlayerBase player, string message)
{
    if (!GetGame().IsServer())
        return;

    NotificationSystem.SendNotificationToPlayerExtended(
        player,
        8.0,                   // Show for 8 seconds
        "Server Notice",       // Title
        message,               // Body
        ""                     // Default icon
    );
}
```

### SendNotificationToPlayerIdentityExtended

```c
static void SendNotificationToPlayerIdentityExtended(
    PlayerIdentity player,   // Target identity (null = broadcast to ALL players)
    float show_time,
    string title_text,
    string detail_text = "",
    string icon = ""
);
```

**Example --- broadcast to all players:**

```c
void BroadcastNotification(string title, string message)
{
    if (!GetGame().IsServer())
        return;

    NotificationSystem.SendNotificationToPlayerIdentityExtended(
        null,                  // null = all connected players
        10.0,                  // Show for 10 seconds
        title,
        message,
        ""
    );
}
```

### SendNotificationToPlayer (Typed)

```c
static void SendNotificationToPlayer(
    Man player,
    NotificationType type,    // Predefined notification type
    float show_time,
    string detail_text = ""
);
```

This variant uses predefined `NotificationType` enum values that map to built-in titles and icons. The `detail_text` is appended as the body.

---

## Client-Side (Local) Notifications

These methods display notifications only on the local client. They do not involve any networking.

### AddNotificationExtended

```c
static void AddNotificationExtended(
    float show_time,
    string title_text,
    string detail_text = "",
    string icon = ""
);
```

**Example --- local notification on client:**

```c
void ShowLocalNotification(string title, string body)
{
    if (!GetGame().IsClient())
        return;

    NotificationSystem.AddNotificationExtended(
        5.0,
        title,
        body,
        "set:dayz_gui image:notification_friend"
    );
}
```

### AddNotification (Typed)

```c
static void AddNotification(
    NotificationType type,
    float show_time,
    string detail_text = ""
);
```

Uses a predefined `NotificationType` for the title and icon.

---

## NotificationType Enum

The vanilla game defines notification types with associated titles and icons. Common values:

| Type | Description |
|------|-------------|
| `NotificationType.FRIEND_CONNECTED` | A friend connected |
| `NotificationType.INVITE_FAIL_SAME_SERVER` | Invite failed (already on same server) |
| `NotificationType.JOIN_FAIL_GET_SESSION` | Failed to get session when joining |
| `NotificationType.CONNECT_FAIL_GENERIC` | Generic connection failure |
| `NotificationType.DISCONNECTED` | Disconnected from server |
| `NotificationType.GENERIC_ERROR` | Generic error |
| `NotificationType.NOTIFICATIONS_END` | Sentinel value (marks the end of the enum) |

> **Note:** The available types depend on the game version. For maximum flexibility, use the `Extended` variants which accept custom title and icon strings.

---

## Icon Paths

Icons use the DayZ image set syntax:

```
"set:dayz_gui image:icon_name"
```

The image name must actually exist in the referenced imageset. Verify it against the set file itself --- `gui/imagesets/dayz_gui.imageset` in the unpacked game data lists every `ImageSetDefClass` name it defines. A name that is not in the set resolves to nothing and the notification simply renders without an icon, with no error.

The only icon vanilla itself uses for notifications is the one its own presets reference in `scripts/data/notifications.json`:

| Icon | Set Path | Used by |
|------|----------|---------|
| Friend | `"set:dayz_gui image:notification_friend"` | `FRIEND_CONNECTED`, `INVITE_FAIL_SAME_SERVER` |

The remaining vanilla notification presets (`JOIN_FAIL_GET_SESSION`, `CONNECT_FAIL_GENERIC`, `DISCONNECTED`, `GENERIC_ERROR`) ship with `"m_Icon": ""` --- no icon at all. `dayz_gui` does contain other usable glyphs (`iconSkull`, `icon_engine_alert`, `icon_hammer`, `icon_close`, ...), but those are HUD/inventory art rather than a documented notification icon set, so check how each one looks at notification size before shipping it.

You can also pass a direct path to an `.edds` image file:

```c
"MyMod/GUI/notification_icon.edds"
```

Or pass an empty string `""` for no icon.

---

## Events

The `NotificationSystem` exposes script invokers for reacting to notification lifecycle:

```c
ref ScriptInvoker m_OnNotificationAdded;
ref ScriptInvoker m_OnNotificationRemoved;
```

Both invokers are called with one argument --- the `NotificationRuntimeData` for the notification that was added or removed --- so your listeners must declare that parameter. Vanilla's own listeners (`NotificationUI.AddNotification` / `RemoveNotification` in `3_Game/client/notifications/notificationui.c`) have exactly this shape.

**Example --- react to notifications:**

```c
void Init()
{
    NotificationSystem notifSys = NotificationSystem.GetInstance();
    if (notifSys)
    {
        notifSys.m_OnNotificationAdded.Insert(OnNotifAdded);
        notifSys.m_OnNotificationRemoved.Insert(OnNotifRemoved);
    }
}

void OnNotifAdded(NotificationRuntimeData data)
{
    Print("A notification was added: " + data.GetTitleText());
}

void OnNotifRemoved(NotificationRuntimeData data)
{
    Print("A notification was removed: " + data.GetTitleText());
}
```

---

## Update Loop

The notification system must be ticked each frame to handle fade-in/fade-out animations and removal of expired notifications:

```c
static void Update(float timeslice);
```

This is called automatically from `DayZGame.OnUpdate` (the game's update loop), not the mission's `OnUpdate`. If you are writing a completely custom game class, make sure to call it.

---

## Complete Server-to-Client Example

A typical mod pattern for sending notifications from server code:

```c
// Server-side: in a mission event handler or module
class MyServerModule
{
    void OnMissionStarted(string missionName, vector location)
    {
        if (!GetGame().IsServer())
            return;

        // Broadcast to all players
        string title = "Mission Started!";
        string body = string.Format("Go to %1!", missionName);

        NotificationSystem.SendNotificationToPlayerIdentityExtended(
            null,
            12.0,
            title,
            body,
            "set:dayz_gui image:notification_friend"
        );
    }

    void OnPlayerEnteredZone(PlayerBase player, string zoneName)
    {
        if (!GetGame().IsServer())
            return;

        // Notify just this player
        NotificationSystem.SendNotificationToPlayerExtended(
            player,
            5.0,
            "Zone Entered",
            string.Format("You have entered %1", zoneName),
            ""
        );
    }
}
```

---

## Building a Custom Notification Layer

Notification features and rendering paths are framework-specific. At pinned CommunityFramework commit `0763e7e7548c9a0bed6626afff835de80693ebf3`, CF mods the vanilla `NotificationSystem` and feeds its inherited notification path rather than establishing an independent channel; inspect other frameworks and versions separately. You do not need a framework for the conveniences shown here --- a thin static wrapper over the vanilla `NotificationSystem` gives you named severity helpers, consistent icons, and a single choke point for logging while sharing the vanilla 5-notification stack.

The example below wraps the `Extended` server-to-client call. Every helper routes through `SendNotificationToPlayerExtended`, so a Lantern notification behaves exactly like a vanilla one on the client:

```c
// Lantern_Core/Scripts/3_Game/LNT_Notify.c
// Static convenience wrapper over the vanilla NotificationSystem.
// Named severity helpers pick a preset icon and a sensible display time.
class LNT_Notify
{
    // Icons live in the mod's imageset (lnt_icons.imageset).
    // Use colored glyphs to convey severity, since vanilla toasts
    // do not carry a per-message color of their own.
    static const string ICON_INFO    = "set:lnt_icons image:info";
    static const string ICON_WARNING = "set:lnt_icons image:warning";
    static const string ICON_SUCCESS = "set:lnt_icons image:success";

    static void Info(PlayerBase player, string title, string body = "")
    {
        Send(player, title, body, ICON_INFO, 8.0);
    }

    static void Warning(PlayerBase player, string title, string body = "")
    {
        Send(player, title, body, ICON_WARNING, 10.0);
    }

    static void Success(PlayerBase player, string title, string body = "")
    {
        Send(player, title, body, ICON_SUCCESS, 6.0);
    }

    // Single choke point: guard, validate, then hand off to vanilla.
    static void Send(PlayerBase player, string title, string body, string icon, float show_time)
    {
        if (!GetGame().IsServer())
            return;

        if (!player)
            return;

        NotificationSystem.SendNotificationToPlayerExtended(player, show_time, title, body, icon);
    }
}
```

Calling it from server code stays readable:

```c
// Server-side
LNT_Notify.Warning(player, "Restart Soon", "Server restarts in 5 minutes.");
LNT_Notify.Success(player, "Objective Complete", "You secured the airfield.");
```

### Registering a Custom Preset in notifications.json

The typed variants (`SendNotificationToPlayer`, `AddNotification`) do not carry a title or icon in the call --- they look those up by `NotificationType` in `scripts/data/notifications.json`. At startup `NotificationSystem.LoadNotificationData()` reads that file into a map keyed by the enum value:

```json
{
    "0": {
        "m_Icon": "set:dayz_gui image:notification_friend",
        "m_TitleText": "#ps4_invite_friend_connected",
        "m_DescriptionText": ""
    }
}
```

Each key is the integer value of a `NotificationType`; `m_Icon` uses the same `"set:... image:..."` syntax as the `Extended` methods, and the two text fields accept stringtable keys (`#STR_...`) for localization. If a type in the enum has no matching JSON entry, `LoadNotificationData()` writes a placeholder row for it and re-saves the file.

For most mods, prefer the `Extended` wrapper above: it needs no shared data file and cannot collide with another mod's preset keys. Reserve the typed/JSON route for notifications whose icon and localized title you want defined as data rather than passed at every call site.

---

## Summary

| Concept | Key Point |
|---------|-----------|
| Server to player | `SendNotificationToPlayerExtended(player, time, title, text, icon)` |
| Server to all | `SendNotificationToPlayerIdentityExtended(null, time, title, text, icon)` |
| Client local | `AddNotificationExtended(time, title, text, icon)` |
| Typed | `SendNotificationToPlayer(player, NotificationType, time, text)` |
| Max visible | 5 notifications stacked |
| Default time | 10 seconds display, 3 seconds fade |
| Icons | `"set:dayz_gui image:icon_name"` or direct `.edds` path |
| Events | `m_OnNotificationAdded`, `m_OnNotificationRemoved` |

---

## Best Practices

- **Use the `Extended` variants for custom notifications.** `SendNotificationToPlayerExtended` gives you full control over title, body, and icon. The typed `NotificationType` variants are limited to vanilla presets.
- **Respect the 5-notification stack limit.** At most five notifications are visible. Additional notifications are appended to the deferred array and promoted as visible notifications expire. This script implementation promotes the last deferred entry first, so its overflow backlog is LIFO. Batch related messages or use longer display times.
- **Always guard server notifications with `GetGame().IsServer()`.** Calling `SendNotificationToPlayerExtended` on the client has no effect and wastes a method call.
- **Pass `null` as the identity for true broadcasts.** `SendNotificationToPlayerIdentityExtended(null, ...)` delivers to all connected players. Do not loop through players manually to send the same message.
- **Keep notification text concise.** The toast popup has limited display width. Long titles or bodies will be clipped. Aim for titles under 30 characters and body text under 80 characters.

---

## Compatibility & Impact

- **Multi-Mod:** The vanilla `NotificationSystem` is shared by all mods, so simultaneous notifications can contend for its visible stack. Do not assume a framework is independent: CommunityFramework mods the vanilla `NotificationSystem`; inspect the specific framework/version before reasoning about queue or layer isolation.
- **Performance:** Notifications are lightweight (a single RPC per notification). However, broadcasting to all players every few seconds generates measurable network traffic on servers with 60+ players.
- **Server/Client:** `SendNotificationToPlayer*` methods are server-to-client RPCs. `AddNotificationExtended` is client-only (local). The `Update()` tick runs on the client mission loop.
