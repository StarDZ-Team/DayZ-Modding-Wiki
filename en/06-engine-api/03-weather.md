# Weather System

> **Summary:** Read and control overcast, rain, snow, fog, wind, and lightning through the `Weather` singleton and its `WeatherPhenomenon` objects, configure declarative defaults in `cfgweather.xml`, and hook the weather state machine via `WeatherOnBeforeChange()`.

---

## Introduction

DayZ has a fully dynamic weather system controlled through the `Weather` class. The system manages overcast, rain, snowfall, fog, wind, and thunderstorms. Weather can be configured through script (the Weather API), through `cfgweather.xml` in the mission folder, or through a scripted weather state machine. This chapter covers the script API for reading and controlling weather programmatically.

---

## Accessing the Weather Object

```c
Weather weather = GetGame().GetWeather();
```

The `Weather` object is a singleton managed by the engine. It is always available after the game world initializes.

---

## Weather Phenomena

Each weather phenomenon (overcast, fog, rain, snowfall, wind magnitude, wind direction) is represented by a `WeatherPhenomenon` object. You access them through getter methods on `Weather`.

### Getting Phenomenon Objects

```c
proto native Overcast      GetOvercast();
proto native Fog           GetFog();
proto native Rain          GetRain();
proto native Snowfall      GetSnowfall();
proto native WindMagnitude GetWindMagnitude();
proto native WindDirection GetWindDirection();
```

Those six return types are not distinct classes --- `3_Game/weather.c` declares them as plain typedefs of `WeatherPhenomenon`:

```c
typedef WeatherPhenomenon Overcast;
typedef WeatherPhenomenon Fog;
typedef WeatherPhenomenon Rain;
typedef WeatherPhenomenon Snowfall;
typedef WeatherPhenomenon WindDirection;
typedef WeatherPhenomenon WindMagnitude;
```

So every phenomenon has exactly the same members, and you can hold any of them in a `WeatherPhenomenon` variable. The distinct names exist only for readability.

### WeatherPhenomenon API

Each phenomenon shares the same interface:

```c
class WeatherPhenomenon
{
    // Current state
    proto native float GetActual();          // Current interpolated value (0.0 - 1.0 for most)
    proto native float GetForecast();        // Target value being interpolated toward
    proto native float GetNextChange();      // Seconds until the next forecast is computed

    // Set the forecast (server only)
    proto native void Set(float forecast, float time = 0, float minDuration = 0);
    // forecast: target value
    // time:     seconds to interpolate to that value (0 = instant)
    // minDuration: minimum time the value holds before auto-change

    // Limits (current value is always held in [fnMin, fnMax])
    proto native void SetLimits(float fnMin, float fnMax);
    proto void        GetLimits(out float fnMin, out float fnMax);

    // Forecast time limits (seconds range in which the next forecast is computed; defaults 300-3600)
    proto native void SetForecastTimeLimits(float ftMin, float ftMax);
    proto void        GetForecastTimeLimits(out float ftMin, out float ftMax);

    // Forecast change limits (how much the forecast value can change per recompute; defaults 0-1)
    proto native void SetForecastChangeLimits(float fcMin, float fcMax);
    proto void        GetForecastChangeLimits(out float fcMin, out float fcMax);
}
```

**Example --- read current weather state:**

```c
Weather w = GetGame().GetWeather();
float overcast  = w.GetOvercast().GetActual();
float rain      = w.GetRain().GetActual();
float fog       = w.GetFog().GetActual();
float snow      = w.GetSnowfall().GetActual();
float windSpeed = w.GetWindMagnitude().GetActual();
float windDir   = w.GetWindDirection().GetActual();

Print(string.Format("Overcast: %1, Rain: %2, Fog: %3", overcast, rain, fog));
```

**Example --- force clear weather (server):**

```c
void ForceClearWeather()
{
    Weather w = GetGame().GetWeather();
    w.GetOvercast().Set(0.0, 30, 600);    // Clear sky, 30s transition, hold 10 min
    w.GetRain().Set(0.0, 10, 600);        // No rain
    w.GetFog().Set(0.0, 30, 600);         // No fog
    w.GetSnowfall().Set(0.0, 10, 600);    // No snow
}
```

**Example --- create a storm:**

```c
void ForceStorm()
{
    Weather w = GetGame().GetWeather();
    w.GetOvercast().Set(1.0, 60, 1800);   // Full overcast, 60s ramp, hold 30 min
    w.GetRain().Set(0.8, 120, 1800);      // Heavy rain
    w.GetFog().Set(0.3, 120, 1800);       // Light fog
    w.GetWindMagnitude().Set(15.0, 60, 1800);  // Strong wind (m/s)
}
```

---

## Rain Thresholds

Rain is tied to overcast levels. The engine only renders rain when overcast exceeds a threshold. You can configure this declaratively via `cfgweather.xml`:

```xml
<rain>
    <thresholds min="0.5" max="1.0" end="120" />
</rain>
```

- `min` / `max`: overcast range where rain is allowed
- `end`: seconds for rain to stop if overcast falls below threshold

The same thresholds are also available directly on `Weather`, for setting them from script instead of (or in addition to) `cfgweather.xml`:

```c
// tMin, tMax: overcast range where rain/snowfall is allowed; tTime: seconds to stop once outside that range
proto native void SetRainThresholds(float tMin, float tMax, float tTime);       // defaults: 0.6, 1, 30
proto native void SetSnowfallThresholds(float tMin, float tMax, float tTime);   // defaults: 0.6, 1, 30
```

In script, rain will not visually appear if overcast is too low, even if `GetRain().GetActual()` returns a non-zero value.

---

## Wind

Wind uses two phenomena: magnitude (speed in m/s) and direction (angle in radians).

### Wind Vector

```c
proto native vector GetWind();           // Wind vector: direction, with speed (m/s) encoded as its length
proto native float  GetWindSpeed();      // Wind speed in m/s (equivalent to GetWindMagnitude().GetActual())
```

**Example --- get wind info:**

```c
Weather w = GetGame().GetWeather();
vector windVec = w.GetWind();
float windSpd = w.GetWindSpeed();
Print(string.Format("Wind: %1 m/s, direction: %2", windSpd, windVec));
```

---

## Thunderstorms (Lightning)

```c
proto native void SetStorm(float density, float threshold, float timeout);
```

| Parameter | Description |
|-----------|-------------|
| `density` | Lightning density (0.0 - 1.0) |
| `threshold` | Minimum overcast level for lightning to appear (0.0 - 1.0) |
| `timeout` | Seconds between lightning strikes |

**Example --- enable frequent lightning:**

```c
GetGame().GetWeather().SetStorm(1.0, 0.6, 10);
// Full density, triggers at 60% overcast, strikes every 10 seconds
```

---

## MissionWeather Control

```c
void MissionWeather(bool use);       // Weather, 3_Game/weather.c
bool GetMissionWeather();
void SetWeatherUpdateFreeze(bool state);
bool GetWeatherUpdateFrozen();
```

`MissionWeather(true)` is widely described as "disabling the automatic weather state machine". **That needs disambiguating.** It does switch off the scripted, per-map `WorldData` weather state machine, but it does not stop the engine's own forecast machinery --- which is what readers usually assume "disabling the weather state machine" buys them. Read `WeatherPhenomenon.OnBeforeChange()`, which the engine calls before applying each computed forecast change:

```c
bool OnBeforeChange( float change, float time )
{
    // check if mission forces use of custom weather
    Weather weather = g_Game.GetWeather();

    if ( weather.GetMissionWeather() )
        return false;

    if (weather.GetWeatherUpdateFrozen())
        return true;

    // check for active worlddata with custom onbeforechange behaviour
    Mission currentMission = g_Game.GetMission();
    if ( currentMission )
    {
        WorldData worldData = currentMission.GetWorldData();
        if ( worldData )
            return worldData.WeatherOnBeforeChange( GetType(), GetActual(), change, time );
    }

    return false;
}
```

The return contract is stated in the vanilla doc comment directly above it: *"True when script modifies state of this phenomenon false otherwise."* So:

| Situation | `OnBeforeChange` returns | Effect |
|---|---|---|
| `MissionWeather(true)` | `false` --- "script did not modify it" | The engine's computed change is **still applied**. The `WorldData` callback and the freeze guard below it are simply skipped |
| `SetWeatherUpdateFreeze(true)` (and mission weather off) | `true` --- "script modified it" | The engine's computed change is **not** applied. This is the actual freeze |
| A `WorldData` override that sets the phenomenon and returns `true` | `true` | The engine's computed change is not applied; your value stands |
| Everything else | `false` | Normal automatic weather |

What `MissionWeather(true)` therefore buys you is a **bypass of the two script hooks** --- the per-map `WorldData.WeatherOnBeforeChange()` logic and the freeze flag --- not a halt of the forecast machinery. If you want the weather to genuinely stop changing on its own, use `SetWeatherUpdateFreeze(true)`, or override `WorldData.WeatherOnBeforeChange()` and return `true`. If you want a scripted cycle, keep re-issuing `Set()` with a long `minDuration` and treat the automatic forecast as something you are competing with, not something you have switched off.

> This correction is scoped to what `3_Game/weather.c` shows statically. The engine side of `OnBeforeChange` is native and unpublished, so the table above describes the script contract and its documented return meaning --- not measured in-game behaviour.

**Example --- setting a starting state in init.c:**

```c
void main()
{
    Weather w = GetGame().GetWeather();

    // Skip the per-map WorldData weather logic and the freeze guard.
    // This does NOT stop the engine's own forecast changes.
    w.MissionWeather(true);

    // Set the starting state. minDuration is 0 here, so these values are
    // only a starting point -- the forecast will move away from them.
    w.GetOvercast().Set(0.3, 0, 0);
    w.GetRain().Set(0.0, 0, 0);
    w.GetFog().Set(0.1, 0, 0);
}
```

If the intent is weather that genuinely does not drift, add the freeze instead of relying on `MissionWeather` alone:

```c
void main()
{
    Weather w = GetGame().GetWeather();

    w.GetOvercast().Set(0.3, 0, 0);
    w.GetRain().Set(0.0, 0, 0);
    w.GetFog().Set(0.1, 0, 0);

    // Both flags are single globals on the Weather singleton, so another
    // module may have left mission weather on. Clear it explicitly: it is
    // checked BEFORE the freeze and would short-circuit past it.
    w.MissionWeather(false);

    // OnBeforeChange returns true while this is set, so computed
    // forecast changes are not applied.
    w.SetWeatherUpdateFreeze(true);
}
```

---

## Date & Time

The game date and time affect lighting, sun position, and the day/night cycle. These are controlled through the `World` object, not `Weather`, but they are closely related.

### Getting Current Date/Time

```c
int year, month, day, hour, minute;
GetGame().GetWorld().GetDate(year, month, day, hour, minute);
```

### Setting Date/Time (Server Only)

```c
proto native void SetDate(int year, int month, int day, int hour, int minute);
```

**Example --- set time to noon:**

```c
int year, month, day, hour, minute;
GetGame().GetWorld().GetDate(year, month, day, hour, minute);
GetGame().GetWorld().SetDate(year, month, day, 12, 0);
```

### Time Acceleration

Time acceleration is configured in `serverDZ.cfg` via:

```
serverTimeAcceleration = 12;      // 12x real time
serverNightTimeAcceleration = 4;  // 4x acceleration during night
```

In script, you can change the time acceleration at runtime (mostly for debug) with `GetGame().GetWorld().SetTimeMultiplier(float timeMultiplier)`, where `timeMultiplier` is a 0-64 acceleration value (or `-1` to reset back to the config value). There is no script getter for the current multiplier.

---

## WorldData Weather State Machine

Vanilla DayZ uses a scripted weather state machine in `WorldData` classes (e.g., `ChernarusPlusData`, `EnochData`, `SakhalData`). The key override point is:

Declared on `WorldData` in `3_Game/worlddata.c`, overridden by `ChernarusPlusData`, `EnochData`, `SakhalData` and `MainMenuWorldData` in `4_World/classes/worlds/`:

```c
class WorldData
{
    bool WeatherOnBeforeChange(EWeatherPhenomenon type, float actual, float change,
                                float time);
}
```

`type` is an `EWeatherPhenomenon` value: `OVERCAST`, `FOG`, `RAIN`, `SNOWFALL`, `WIND_DIRECTION`, `WIND_MAGNITUDE`, `VOLFOG_HEIGHT_DENSITY`, `VOLFOG_DISTANCE_DENSITY`, `VOLFOG_HEIGHT_BIAS`.

> **On the return value.** `WeatherPhenomenon.OnBeforeChange()` documents it as *"True when script modifies state of this phenomenon false otherwise."* Return `true` from your override when you have called `Set()` on the phenomenon yourself and the engine should leave its own computed change alone; return `false` to let the automatic change through. The base `WorldData` implementation returns `false` (its comment, *"default behaviour is same like setting MissionWeather (in Weather) to true"*, refers to the fact that both paths end up returning `false` from `OnBeforeChange`, not to freezing anything). The vanilla per-map subclasses set the phenomenon explicitly and return a value per branch --- mirror that shape.

`change` and `time` are documented on `WeatherPhenomenon.OnBeforeChange( float change, float time )` itself (the two-parameter method shown in [MissionWeather Control](#missionweather-control)): `change` = the **computed change** of the forecast value, `time` = seconds until the next forecast is computed. `actual` is not a parameter of that method at all --- it belongs only to the four-parameter `WorldData.WeatherOnBeforeChange()` shown directly above, which `WeatherPhenomenon.OnBeforeChange()` calls as `worldData.WeatherOnBeforeChange(GetType(), GetActual(), change, time)`. `GetActual()` is documented separately as "actual value of phenomenon in range <0, 1>" (wind is the exception --- it always returns the magnitude value instead). Note that `change` is a delta, not the resulting target -- so you cannot read it as "the forecast is about to become X".

**If you want a hard ceiling on a phenomenon, do not try to compute it in this hook.** Use `SetLimits(min, max)`, which the API documents as holding the value inside the range, and which is exactly how vanilla pins snowfall off on Chernarus (`m_Weather.GetSnowfall().SetLimits(0, 0)` in `ChernarusPlusData.WeatherOnBeforeChange`):

```c
modded class ChernarusPlusData
{
    override bool WeatherOnBeforeChange(EWeatherPhenomenon type, float actual,
                                         float change, float time)
    {
        // Hard ceiling on rain: the phenomenon value is held inside the range,
        // so nothing the forecast computes can push it past 0.5.
        // This is the same mechanism vanilla uses here to keep snowfall at 0.
        m_Weather.GetRain().SetLimits(0.0, 0.5);

        // Everything else keeps the map's own behaviour.
        return super.WeatherOnBeforeChange(type, actual, change, time);
    }
}
```

Use the return value only for a phenomenon your override genuinely takes over -- set it yourself, then claim it:

```c
modded class ChernarusPlusData
{
    override bool WeatherOnBeforeChange(EWeatherPhenomenon type, float actual,
                                         float change, float time)
    {
        if (type == EWeatherPhenomenon.RAIN)
        {
            // This override owns rain outright: drive it explicitly and return
            // true so the engine does not also apply its computed change.
            m_Weather.GetRain().Set(0.0, time, 300);
            return true;
        }

        // Fall through to the map's own logic for everything else
        return super.WeatherOnBeforeChange(type, actual, change, time);
    }
}
```

---

## cfgweather.xml

The `cfgweather.xml` file in the mission folder provides a declarative way to configure weather without scripting. When present, it overrides the default weather state machine parameters.

Key structure:

```xml
<weather reset="0" enable="1">
    <overcast>
        <current actual="0.45" time="120" duration="240" />
        <limits min="0.0" max="1.0" />
        <timelimits min="900" max="1800" />
        <changelimits min="0.0" max="1.0" />
    </overcast>
    <fog>...</fog>
    <rain>
        ...
        <thresholds min="0.5" max="1.0" end="120" />
    </rain>
    <snowfall>...</snowfall>
    <windMagnitude>...</windMagnitude>
    <windDirection>...</windDirection>
    <storm density="1.0" threshold="0.7" timeout="25"/>
</weather>
```

| Field | Description |
|-------|-------------|
| `reset` | Whether to load the weather in from storage (`false` by default) |
| `enable` | Whether this file is active (`true` by default) |
| `actual` | Initial target value |
| `time` | Seconds to change to that value |
| `duration` | Seconds the value then holds |
| `limits min/max` | Range the phenomenon value is held within. Units differ per phenomenon: `0..1` for overcast, fog, rain and snowfall; m/s for `windMagnitude`; radians for `windDirection` |
| `timelimits min/max` | Seconds it takes to change from one value to another |
| `changelimits min/max` | How much the value should change per recomputation |
| `thresholds min/max/end` | On `rain` and `snowfall` only: the overcast range that allows the phenomenon, plus the seconds it takes to stop once overcast leaves that range |
| `storm density/threshold/timeout` | Lightning density `0..1`, the overcast threshold for lightning to appear, and seconds between strikes |

### Attribute form and element form are interchangeable

Everything except `reset` and `enable` is a float, and each value can be written **either as an attribute or as a child element** --- including a mix of both in one file. These two fragments are equivalent:

```xml
<weather reset="false" enable="true">
    <rain>
        <limits>
            <min>0</min>
            <max>1</max>
        </limits>
    </rain>
    <wind>
        <maxspeed>0</maxspeed>
    </wind>
</weather>
```

```xml
<weather reset="0" enable="1">
    <rain>
        <limits min="0" max="1"/>
    </rain>
    <wind maxspeed="0"/>
</weather>
```

`reset` and `enable` are booleans and accept `0`/`1`, `true`/`false` or `yes`/`no`.

This chapter uses the attribute form throughout because it is more compact, but you will encounter the element form in published missions and it is equally valid. (Source: Bohemia's [Weather Configuration](https://community.bistudio.com/wiki/DayZ:Weather_Configuration) page, which also documents the `<wind maxspeed>` entry shown above --- the declarative counterpart of the `SetWindMaximumSpeed()` call vanilla's `ChernarusPlusData` makes from script.)

> **Which mechanism to use.** The same vendor page notes that all vanilla server-side missions use the scripted weather state machine, and recommends `cfgweather.xml` for adjusting weather behaviour. That is a recommendation about authoring, not a statement about engine internals --- for what the script flags actually do, see [MissionWeather Control](#missionweather-control) above, which is derived from `3_Game/weather.c` rather than from the vendor page.

---

## Summary

| Concept | Key Point |
|---------|-----------|
| Access | `GetGame().GetWeather()` returns the `Weather` singleton |
| Phenomena | `GetOvercast()`, `GetRain()`, `GetFog()`, `GetSnowfall()`, `GetWindMagnitude()`, `GetWindDirection()` |
| Read | `phenomenon.GetActual()` for current value (0.0 - 1.0) |
| Write | `phenomenon.Set(forecast, transitionTime, holdDuration)` (server only) |
| Storms | `SetStorm(density, threshold, timeout)` |
| Manual mode | `MissionWeather(true)` bypasses the `WorldData` hook and the freeze flag; `SetWeatherUpdateFreeze(true)` is what actually suppresses automatic changes |
| Date/Time | `GetGame().GetWorld().GetDate()` / `SetDate()` |
| Config file | `cfgweather.xml` in mission folder for declarative setup |

---

## Best Practices

- **Do not rely on `MissionWeather(true)` to hold a value.** It bypasses the `WorldData` weather hook and the freeze flag, but per `WeatherPhenomenon.OnBeforeChange()` it returns `false` --- the engine's automatic forecast changes still apply. For a value that must hold, use `SetWeatherUpdateFreeze(true)`, or a `WorldData.WeatherOnBeforeChange()` override returning `true`, or re-issue `Set()` with a long `minDuration`.
- **Always provide a `minDuration` parameter in `Set()`.** Setting `minDuration` to 0 means the weather system can immediately transition away from your value. Use at least 300-600 seconds to hold your desired state.
- **Set overcast before rain.** Rain is visually tied to overcast thresholds. If overcast is below the threshold configured in `cfgweather.xml`, rain will not render even if `GetRain().GetActual()` returns a non-zero value.
- **Use `WeatherOnBeforeChange()` for server-wide weather policy.** Override this in a `modded class ChernarusPlusData` (or the appropriate WorldData subclass) to clamp or redirect weather transitions without fighting the state machine.
- **Read weather on both sides, write only on server.** `GetActual()` and `GetForecast()` work on client and server, but `Set()` only has effect on the server.

---

## Compatibility & Impact

> **Mod Compatibility:** Weather mods commonly override `WeatherOnBeforeChange()` in WorldData subclasses. Only one mod's override chain runs per map's WorldData class.

- **Load Order:** Multiple mods overriding `WeatherOnBeforeChange` on the same WorldData subclass (e.g., `ChernarusPlusData`) must all call `super`, or earlier mods lose their weather logic.
- **Modded Class Conflicts:** `MissionWeather` and `SetWeatherUpdateFreeze` are single global flags on the `Weather` singleton, so the last writer wins and there is no ownership tracking. A mod that sets either one silently changes which hooks run for every other weather mod on the server. Document which flags your mod touches.
- **Performance Impact:** Weather API calls are lightweight. The phenomena interpolation runs in the engine, not in script. Frequent `Set()` calls (every frame) are wasteful but not harmful.
- **Server/Client:** All `Set()` calls are server-only. Clients receive weather state via engine synchronization automatically. Client-side `Set()` calls are silently ignored.

---

## Common Patterns in the Wild

- **Scripted weather cycles.** Server frameworks call `MissionWeather(true)` in mission init and then drive a repeating weather cycle with `GetGame().GetCallQueue(CALL_CATEGORY_SYSTEM).CallLater()`, stepping through preset overcast/rain/fog states. Note this is a convention, not a guarantee: the flag does not stop the engine's own forecast, so these cycles work by re-asserting `Set()` often enough with a long `minDuration`.
- **Area-based weather policy.** Overriding `WeatherOnBeforeChange()` in a modded WorldData class lets a mod veto or clamp specific transitions server-wide — for example suppressing rain during an event window.
- **Admin force-weather commands.** Admin tools expose clear/storm buttons that call `Set()` with a long `minDuration` so the state machine cannot immediately revert the forced state. See [Admin & Server Tools](22-admin-server.md) for building an admin command pipeline.
- **Winter-map tuning.** Winter maps ship a custom `cfgweather.xml` in the mission folder with thresholds tuned so precipitation renders as snowfall rather than rain.
