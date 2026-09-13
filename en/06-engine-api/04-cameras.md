# Camera System


---

## Introduction

DayZ uses a multi-layered camera system. The player camera is managed by the engine through `DayZPlayerCamera` subclasses. For modding and debugging, the `FreeDebugCamera` allows free-flight. The engine also provides global accessors for the current camera state. This chapter covers camera types, how to access camera data, and how to use the scripted camera tools.

---

## Current Camera State (Global Accessors)

These methods are available anywhere and return the active camera's state regardless of camera type:

Declared on `CGame` (`3_Game/global/game.c`), called through `GetGame()`:

```c
// Current camera world position
proto native vector GetCurrentCameraPosition();

// Current camera forward direction (unit vector)
proto native vector GetCurrentCameraDirection();

// Convert world position to screen coordinates
proto native vector GetScreenPos(vector world_pos);
// Returns: x = screen X (pixels), y = screen Y (pixels), z = depth (distance from camera)
```

**Example --- check if a position is on screen:**

```c
bool IsPositionOnScreen(vector worldPos)
{
    vector screenPos = GetGame().GetScreenPos(worldPos);

    // z < 0 means behind the camera
    if (screenPos[2] < 0)
        return false;

    int screenW, screenH;
    GetScreenSize(screenW, screenH);

    return (screenPos[0] >= 0 && screenPos[0] <= screenW &&
            screenPos[1] >= 0 && screenPos[1] <= screenH);
}
```

**Example --- get distance from camera to a point:**

```c
float DistanceFromCamera(vector worldPos)
{
    return vector.Distance(GetGame().GetCurrentCameraPosition(), worldPos);
}
```

---

## DayZPlayerCamera System

DayZ player cameras are native classes managed by the engine's player controller. They are not directly instantiated from script --- instead, the engine selects the appropriate camera based on the player's state (standing, prone, swimming, vehicle, unconscious, etc.).

### Camera Types (DayZPlayerCameras Constants)

The camera type IDs are defined as constants:

| Constant | Description |
|----------|-------------|
| `DayZPlayerCameras.DAYZCAMERA_1ST` | First-person camera |
| `DayZPlayerCameras.DAYZCAMERA_3RD_ERC` | Third-person erect (standing) |
| `DayZPlayerCameras.DAYZCAMERA_3RD_CRO` | Third-person crouched |
| `DayZPlayerCameras.DAYZCAMERA_3RD_PRO` | Third-person prone |
| `DayZPlayerCameras.DAYZCAMERA_3RD_ERC_SPR` | Third-person sprint |
| `DayZPlayerCameras.DAYZCAMERA_3RD_ERC_RAISED` | Third-person raised weapon |
| `DayZPlayerCameras.DAYZCAMERA_3RD_CRO_RAISED` | Third-person crouched raised |
| `DayZPlayerCameras.DAYZCAMERA_IRONSIGHTS` | Ironsight aiming |
| `DayZPlayerCameras.DAYZCAMERA_OPTICS` | Optic/scope aiming |
| `DayZPlayerCameras.DAYZCAMERA_3RD_VEHICLE` | Third-person vehicle |
| `DayZPlayerCameras.DAYZCAMERA_1ST_VEHICLE` | First-person vehicle |
| `DayZPlayerCameras.DAYZCAMERA_1ST_UNCONSCIOUS` | First-person unconscious |
| `DayZPlayerCameras.DAYZCAMERA_3RD_CLIMB` | Third-person climbing |
| `DayZPlayerCameras.DAYZCAMERA_3RD_JUMP` | Third-person jumping |

### Getting the Current Camera Type

```c
DayZPlayer player = GetGame().GetPlayer();
if (player)
{
    DayZPlayerCamera cam = player.GetCurrentCamera();
    if (cam && cam.GetCameraName() == "DayZPlayerCamera1stPerson")
    {
        Print("Player is in first person");
    }
}
```

---

## FreeDebugCamera

**File:** `3_Game/entities/camera.c`

The free-flight camera used for debugging and cinematic work. Available in diagnostic builds or when enabled by mods.

### Accessing the Instance

```c
static proto native FreeDebugCamera GetInstance();
```

This static method returns the singleton free camera instance (or null if it does not exist). Call it as `FreeDebugCamera.GetInstance()`.

### Key Methods

```c
// Enable/disable the free camera (inherited from Camera)
proto native void SetActive(bool active);
proto native bool IsActive();

// Position and orientation
vector GetPosition();
void   SetPosition(vector pos);
vector GetOrientation();
void   SetOrientation(vector ori);   // yaw, pitch, roll

// Camera direction
vector GetDirection();
```

**Example --- activate free camera and teleport it:**

```c
void ActivateDebugCamera(vector pos)
{
    FreeDebugCamera cam = FreeDebugCamera.GetInstance();
    if (cam)
    {
        cam.SetActive(true);
        cam.SetPosition(pos);
        cam.SetOrientation(Vector(0, -30, 0));  // Look slightly down
    }
}
```

---

## Field of View (FOV)

The engine controls FOV natively. You can read and modify it through the player camera system:

### Reading FOV

```c
// Get current camera FOV (in radians)
float fov = Camera.GetCurrentFOV();
```

### DayZPlayerCamera FOV Override

In custom camera classes that extend `DayZPlayerCamera`, you can override the FOV:

```c
class MyCustomCamera extends DayZPlayerCamera1stPerson
{
    override void OnUpdate(float pDt, out DayZPlayerCameraResult pOutResult)
    {
        super.OnUpdate(pDt, pOutResult);
        pOutResult.m_fFovAbsolute = 0.7854;  // ~45 degrees (radians)
    }
}
```

---

## Depth of Field (DOF)

Depth of field is controlled through the Post-Process Effects system (see [Chapter 6.5](05-ppe.md)). However, the camera system works with DOF through these mechanisms:

### Setting DOF via CGame

```c
// OverrideDOF(enable, focusDistance, focusLength, focusLengthNear, blur, focusDepthOffset)
GetGame().OverrideDOF(true, 5.0, 100.0, 0.5, 0.3, 0.0);
```

### Disabling DOF

```c
GetGame().OverrideDOF(false, 0, 0, 0, 0, 1);  // First argument false disables DOF
```

---

## ScriptCamera (GameLib)

**File:** `2_GameLib/entities/scriptcamera.c`

A lower-level scripted camera entity from the GameLib layer. This is the base for custom camera implementations.

### Creating a Camera

```c
ScriptCamera camera = ScriptCamera.Cast(
    GetGame().CreateObject("ScriptCamera", pos, true)  // local only
);
```

### Key Methods

> **Note:** `ScriptCamera` is compiled only under `#ifdef GAME_TEMPLATE` and is not present in the DayZ game build. It configures itself through `GenericEntity` camera methods (`SetCameraVerticalFOV`, `SetCameraNearPlane`, `SetCameraFarPlane`, `SetCameraType`). The methods below belong to the engine `Camera` class (`3_Game/entities/camera.c`), which `FreeDebugCamera` extends:

```c
proto native void SetFOV(float fov);                 // FOV in radians
proto native void SetNearPlane(float nearPlane);     // clamped internally to 0.01m
proto native float GetNearPlane();
proto native void SetFocus(float distance, float blur);  // depth of field
```

### Activating a Camera

```c
// Make this camera the active rendering camera
GetGame().SelectPlayer(null, null);   // Detach from player
GetGame().ObjectRelease(camera);      // Release to engine
```

> **Note:** Switching away from the player camera requires careful handling of input and HUD. Most mods use the free debug camera or PPE overlay effects instead of creating custom cameras.

---

## Raycasting from Camera

A common pattern is to raycast from the camera position in the camera direction to find what the player is looking at:

```c
Object GetObjectInCrosshair(float maxDistance)
{
    vector from = GetGame().GetCurrentCameraPosition();
    vector to = from + (GetGame().GetCurrentCameraDirection() * maxDistance);

    vector contactPos;
    vector contactDir;
    int contactComponent;
    set<Object> hitObjects = new set<Object>;

    if (DayZPhysics.RaycastRV(from, to, contactPos, contactDir,
                               contactComponent, hitObjects, null, null,
                               false, false, ObjIntersectView, 0.0))
    {
        if (hitObjects.Count() > 0)
            return hitObjects[0];
    }

    return null;
}
```

---

## Summary

| Concept | Key Point |
|---------|-----------|
| Global accessors | `GetCurrentCameraPosition()`, `GetCurrentCameraDirection()`, `GetScreenPos()` |
| Camera types | `DayZPlayerCameras` constants (1ST, 3RD_ERC, IRONSIGHTS, OPTICS, VEHICLE, etc.) |
| Current type | `player.GetCurrentCamera().GetCameraName()` |
| Free camera | `FreeDebugCamera.GetInstance()`, then `cam.SetActive(true)` |
| FOV | `Camera.GetCurrentFOV()` to read, set `pOutResult.m_fFovAbsolute` in `OnUpdate` |
| DOF | `GetGame().OverrideDOF(enable, focusDist, focusLen, focusLenNear, blur, offset)` |
| Screen conversion | `GetScreenPos(worldPos)` returns pixel XY + depth Z |

---

## Best Practices

- **Cache camera position when querying multiple times per frame.** `GetGame().GetCurrentCameraPosition()` and `GetCurrentCameraDirection()` are engine calls -- store the result in a local variable if you need it in multiple calculations within the same frame.
- **Use `GetScreenPos()` depth check before UI placement.** Always verify `screenPos[2] > 0` (in front of camera) before drawing HUD markers at world positions, or markers will appear mirrored behind the player.
- **Avoid creating custom ScriptCamera instances for simple effects.** The FreeDebugCamera and PPE system cover most cinematic and visual needs. Custom cameras require careful input/HUD management that is easy to break.
- **Respect the engine's camera type transitions.** Do not force camera type changes from script unless you fully handle the player controller state. Unexpected camera switches can lock the player's movement or cause desync.
- **Guard free camera usage behind admin/debug checks.** FreeDebugCamera provides god-like world inspection. Only enable it for authenticated admins or diagnostic builds to prevent abuse.

---

## Compatibility & Impact

- **Multi-Mod:** Camera accessors are read-only globals, so multiple mods can safely read camera state simultaneously. Conflicts arise only if two mods both try to activate FreeDebugCamera or custom ScriptCamera instances.
- **Performance:** `GetScreenPos()` and `GetCurrentCameraPosition()` are lightweight engine calls. Raycasting from the camera (`DayZPhysics.RaycastRV`) is more expensive -- limit to once per frame, not per entity.
- **Server/Client:** Camera state exists only on the client. All camera methods return meaningless data on a dedicated server. Never use camera queries in server-side logic.

---

[<< Previous: Weather](03-weather.md) | **Cameras** | [Next: Post-Process Effects >>](05-ppe.md)
