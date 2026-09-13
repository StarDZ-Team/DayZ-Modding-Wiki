# Vehicle & Dynamic Event Spawning


---

> **Summary:** Vehicles and dynamic events (heli crashes, convoys, police cars) do NOT use `types.xml`. They use a separate three-file system: `events.xml` defines what spawns and how many, `cfgeventspawns.xml` defines where, and `cfgeventgroups.xml` defines grouped formations. This chapter covers all three files with real vanilla values.

---

## Table of Contents

- [How Vehicle Spawning Works](#how-vehicle-spawning-works)
- [events.xml Vehicle Entries](#eventsxml-vehicle-entries)
- [Vehicle Event Field Reference](#vehicle-event-field-reference)
- [cfgeventspawns.xml -- Spawn Positions](#cfgeventspawnsxml----spawn-positions)
- [Heli Crash Events](#heli-crash-events)
- [Military Convoy](#military-convoy)
- [Police Car](#police-car)
- [cfgeventgroups.xml -- Grouped Spawns](#cfgeventgroupsxml----grouped-spawns)
- [cfgeconomycore.xml Vehicle Root Class](#cfgeconomycorexml-vehicle-root-class)
- [Common Mistakes](#common-mistakes)

---

## How Vehicle Spawning Works

Vehicles are **not** defined in `types.xml`. If you add a vehicle class to `types.xml`, it will not spawn. Vehicles use a dedicated three-file pipeline:

1. **`events.xml`** -- Defines each vehicle event: how many should exist on the map (nominal), which variants can spawn (children), and behavior flags like lifetime and safe radius.

2. **`cfgeventspawns.xml`** -- Defines the physical world positions where vehicle events can place entities. Each event name maps to a list of `<pos>` entries with x, z coordinates and angle.

3. **`cfgeventgroups.xml`** -- Defines grouped spawns where multiple objects spawn together with relative positional offsets (e.g., train wrecks).

The CE reads `events.xml`, picks an event that needs spawning, looks up matching positions in `cfgeventspawns.xml`, selects one at random that satisfies the `saferadius` and `distanceradius` constraints, then spawns a randomly selected child entity at that position.

`events.xml` lives in `mpmissions/<your_mission>/db/`, while `cfgeventspawns.xml` and `cfgeventgroups.xml` live at the mission root (`mpmissions/<your_mission>/`).

---

## events.xml Vehicle Entries

Every vanilla vehicle type has its own event entry. Here are all of them with real values:

### Civilian Sedan

```xml
<event name="VehicleCivilianSedan">
    <nominal>8</nominal>
    <min>5</min>
    <max>11</max>
    <lifetime>300</lifetime>
    <restock>0</restock>
    <saferadius>500</saferadius>
    <distanceradius>500</distanceradius>
    <cleanupradius>200</cleanupradius>
    <flags deletable="0" init_random="0" remove_damaged="1"/>
    <position>fixed</position>
    <limit>mixed</limit>
    <active>1</active>
    <children>
        <child lootmax="0" lootmin="0" max="5" min="3" type="CivilianSedan"/>
        <child lootmax="0" lootmin="0" max="5" min="3" type="CivilianSedan_Black"/>
        <child lootmax="0" lootmin="0" max="5" min="3" type="CivilianSedan_Wine"/>
    </children>
</event>
```

### All Vanilla Vehicle Events

All vehicle events use the same structure as the Sedan above. Only the values differ:

| Event Name | Nominal | Min | Max | Lifetime | Children (variants) |
|------------|---------|-----|-----|----------|---------------------|
| `VehicleCivilianSedan` | 8 | 5 | 11 | 300 | `CivilianSedan`, `_Black`, `_Wine` |
| `VehicleOffroadHatchback` | 8 | 5 | 11 | 300 | `OffroadHatchback`, `_Blue`, `_White` |
| `VehicleHatchback02` | 8 | 5 | 11 | 300 | Hatchback02 variants |
| `VehicleSedan02` | 8 | 5 | 11 | 300 | Sedan02 variants |
| `VehicleTruck01` | 8 | 5 | 11 | 300 | `Truck_01_Covered` variants |
| `VehicleOffroad02` | 3 | 2 | 3 | 300 | Gunter -- fewer spawn |
| `VehicleBoat` | 17 | 15 | 24 | 600 | Boats -- highest count, longer lifetime |

`VehicleOffroad02` has a lower nominal (3) than other land vehicles (8). `VehicleBoat` has both the highest nominal (17) and a longer lifetime (600 vs 300).

---

## Vehicle Event Field Reference

### Event-Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Event identifier. Must match an entry in `cfgeventspawns.xml` when `position="fixed"`. |
| `nominal` | int | Target number of active instances of this event on the map. |
| `min` | int | The CE will attempt to spawn more when the count drops below this. |
| `max` | int | Hard upper cap. The CE will never exceed this count. |
| `lifetime` | int | Seconds between respawn checks. For vehicles, this is NOT the vehicle's persistence lifetime -- it is the interval at which the CE re-evaluates whether to spawn or clean up. |
| `restock` | int | Minimum seconds between respawn attempts. 0 = next cycle. |
| `saferadius` | int | Minimum distance (meters) from any player for the event to spawn. Prevents vehicles appearing in front of players. |
| `distanceradius` | int | Minimum distance (meters) between two instances of the same event. Prevents two sedans spawning next to each other. |
| `cleanupradius` | int | If a player is within this distance (meters), the event entity is protected from cleanup. |

### Flags

| Flag | Values | Description |
|------|--------|-------------|
| `deletable` | 0, 1 | Whether the CE can delete this event entity. Vehicles use 0 (not deletable by CE). |
| `init_random` | 0, 1 | Randomize initial positions on first spawn. 0 = use fixed positions from `cfgeventspawns.xml`. |
| `remove_damaged` | 0, 1 | Remove the entity when it becomes ruined. **Critical for vehicles** -- see [Common Mistakes](#common-mistakes). |

### Other Fields

| Field | Values | Description |
|-------|--------|-------------|
| `position` | `fixed`, `player`, `uniform` | `fixed` = spawn at positions from `cfgeventspawns.xml`. `player` = spawn relative to player positions. `uniform` = distributed evenly (used by vanilla ambient events like `StaticChristmasTree`). |
| `limit` | `child`, `mixed`, `custom`, `parent` | `child` = min/max enforced per child type. `mixed` = min/max shared across all children. `custom` = engine-specific behavior. `parent` = enforced at the parent/group level (used by vanilla `StaticContaminatedArea`). |
| `active` | 0, 1 | Enable or disable this event. 0 = the event is skipped entirely. |

### Child Fields

| Attribute | Description |
|-----------|-------------|
| `type` | Class name of the entity to spawn. |
| `min` | Minimum instances of this variant. |
| `max` | Maximum instances of this variant. |
| `lootmin` | Minimum number of loot items spawned inside/around the entity. 0 for vehicles (parts come from `cfgspawnabletypes.xml`). |
| `lootmax` | Maximum loot items. Used by heli crashes and dynamic events, not vehicles. |

---

## cfgeventspawns.xml -- Spawn Positions

This file maps event names to world coordinates. Each `<event>` block contains a list of valid spawn positions for that event type. When the CE needs to spawn a vehicle, it picks a random position from this list that satisfies the `saferadius` and `distanceradius` constraints.

```xml
<event name="VehicleCivilianSedan">
    <pos x="4509.1" z="9321.5" a="172"/>
    <pos x="6283.7" z="2468.3" a="90"/>
    <pos x="11447.2" z="11203.8" a="45"/>
    <pos x="2961.4" z="5107.6" a="0"/>
    <!-- ... more positions ... -->
</event>
```

Each `<pos>` has three attributes:

| Attribute | Description |
|-----------|-------------|
| `x` | World X coordinate (east-west position on the map). |
| `z` | World Z coordinate (north-south position on the map). |
| `a` | Angle in degrees (0-360). The direction the vehicle faces when spawned. |

**Key rules:**

- If an event has no matching `<event>` block in `cfgeventspawns.xml`, it **will not spawn** regardless of the `events.xml` configuration.
- You need at least as many `<pos>` entries as your `nominal` value. If you set `nominal=8` but only have 3 positions, only 3 can spawn.
- Positions should be on roads or flat ground. A position inside a building or on steep terrain will cause the vehicle to spawn buried or flipped.
- The `a` (angle) value determines the vehicle's facing direction. Align it with the road direction for natural-looking spawns.

---

## Heli Crash Events

Helicopter crashes are dynamic events that spawn a wreck with military loot and surrounding infected. They use the `<secondary>` tag to define ambient zombie spawns around the crash site.

```xml
<event name="StaticHeliCrash">
    <nominal>3</nominal>
    <min>0</min>
    <max>0</max>
    <lifetime>2100</lifetime>
    <restock>0</restock>
    <saferadius>1000</saferadius>
    <distanceradius>1000</distanceradius>
    <cleanupradius>1000</cleanupradius>
    <secondary>InfectedArmy</secondary>
    <flags deletable="1" init_random="0" remove_damaged="0"/>
    <position>fixed</position>
    <limit>child</limit>
    <active>1</active>
    <children>
        <child lootmax="15" lootmin="10" max="3" min="1" type="Wreck_UH1Y"/>
    </children>
</event>
```

### Key differences from vehicle events

- **`<secondary>InfectedArmy</secondary>`** -- spawns military zombies around the crash site. This tag references an infected spawn group that the CE places in the vicinity.
- **`lootmin="10"` / `lootmax="15"`** -- the wreck spawns with 10-15 dynamic event loot items. These are items flagged with `deloot="1"` in `types.xml` (military gear, rare weapons).
- **`lifetime=2100`** -- the crash persists for 35 minutes before the CE cleans it up and spawns a new one elsewhere.
- **`saferadius=1000`** -- crashes never appear within 1 km of a player.
- **`remove_damaged=0`** -- the wreck is already "damaged" by definition, so this must be 0 or it would be immediately cleaned up.

---

## Military Convoy

Military convoys are static wrecked vehicle groups that spawn with military loot and infected guards.

```xml
<event name="StaticMilitaryConvoy">
    <nominal>6</nominal>
    <min>0</min>
    <max>0</max>
    <lifetime>1800</lifetime>
    <restock>0</restock>
    <saferadius>500</saferadius>
    <distanceradius>1000</distanceradius>
    <cleanupradius>1000</cleanupradius>
    <secondary>InfectedArmyDesert</secondary>
    <flags deletable="1" init_random="0" remove_damaged="0"/>
    <position>fixed</position>
    <limit>child</limit>
    <active>1</active>
    <children/>
</event>
```

Convoys work like heli crashes: the `<secondary>` tag spawns `InfectedArmyDesert` around the site, and loot items with `deloot="1"` appear on the wrecks. Unlike the heli crash, the convoy event has an empty `<children/>` element -- its wrecked vehicles are defined as a group in `cfgeventgroups.xml` and placed via group references in `cfgeventspawns.xml`. With `nominal=6`, up to 6 convoy sites exist on the map simultaneously. Each lasts 1800 seconds (30 minutes) before cycling to a new location.

---

## Police Car

Police car events spawn wrecked police vehicles with police-type infected nearby. They are **disabled by default**.

```xml
<event name="StaticPoliceCar">
    <nominal>10</nominal>
    <min>0</min>
    <max>0</max>
    <lifetime>2500</lifetime>
    <restock>0</restock>
    <saferadius>500</saferadius>
    <distanceradius>500</distanceradius>
    <cleanupradius>200</cleanupradius>
    <secondary>InfectedPoliceHard</secondary>
    <flags deletable="1" init_random="0" remove_damaged="0"/>
    <position>fixed</position>
    <limit>child</limit>
    <active>0</active>
    <children>
        <child lootmax="5" lootmin="3" max="5" min="5" type="Land_Wreck_sed01_aban1_police"/>
        <child lootmax="5" lootmin="3" max="5" min="5" type="Land_Wreck_sed01_aban2_police"/>
    </children>
</event>
```

**`active=0`** means this event is disabled by default -- change to `1` to enable it. The `<secondary>InfectedPoliceHard</secondary>` tag spawns hard-variant police zombies (tougher than standard infected). With `nominal=10` and `saferadius=500`, police cars are more numerous but less valuable than heli crashes.

---

## cfgeventgroups.xml -- Grouped Spawns

This file defines events where multiple objects spawn together with relative positional offsets. The most common use is abandoned trains.

```xml
<group name="Train_Abandoned_Cherno">
    <child type="StaticObj_Wreck_Train_742_Red_DE" deloot="0" lootmax="3" lootmin="1" x="0" z="0" a="78.123" y="1.9"/>
    <child type="StaticObj_Wreck_Train_Wagon_Tanker_DE" deloot="0" lootmax="3" lootmin="1" x="12.085" z="2.740" a="256.739" y="1.789"/>
    <child type="Land_Train_Wagon_Box_DE" deloot="0" lootmax="3" lootmin="2" x="34.546" z="8.424" a="255.837" y="1.32"/>
    <child type="Land_Train_Wagon_Box_DE" deloot="0" lootmax="3" lootmin="2" x="46.285" z="11.341" a="255.321" y="1.398"/>
</group>
```

Each group is declared with a `<group name="...">` element inside the file's root `<eventgroupdef>`, and its `<child>` entries are direct children of `<group>` (there is no `<children>` wrapper here). The first child is placed at the position from `cfgeventspawns.xml`. Subsequent children are offset by their `x`, `z`, `y`, `a` values relative to that origin.

Each `<child>` in a group has:

| Attribute | Description |
|-----------|-------------|
| `type` | Class name of the object to spawn. |
| `x` | X offset in meters from the group origin. |
| `z` | Z offset in meters from the group origin. |
| `y` | Y (vertical) offset in meters from the group origin. |
| `a` | Angle offset in degrees from the group origin. |
| `deloot` | Whether dynamic event loot can spawn in this child (0 or 1). |
| `lootmin` | Minimum number of loot items spawned in this child. |
| `lootmax` | Maximum number of loot items spawned in this child. |

The group event itself still needs a matching entry in `events.xml` to control nominal counts, lifetime, and active state.

---

## cfgeconomycore.xml Vehicle Root Class

For the CE to recognize vehicles as trackable entities, they must have a root class declaration in `cfgeconomycore.xml`:

```xml
<economycore>
    <classes>
        <rootclass name="CarScript" act="car"/>
        <rootclass name="BoatScript" act="car"/>
    </classes>
</economycore>
```

- **`CarScript`** is the base class for all land vehicles in DayZ.
- **`BoatScript`** is the base class for all boats.
- The `act="car"` attribute tells the CE to treat these entities with vehicle-specific behavior (persistence, event-based spawning).

Without these root class entries, the CE would not track or manage vehicle instances. If you add a modded vehicle that inherits from a different base class, you may need to add its root class here.

---

## Common Mistakes

These are the most frequent vehicle spawning issues encountered by server admins.

### Putting vehicles in types.xml

**Problem:** You add `CivilianSedan` to `types.xml` with a nominal of 10. No sedans spawn.

**Fix:** Remove the vehicle from `types.xml`. Add or edit the vehicle event in `events.xml` with the appropriate children, and ensure matching spawn positions exist in `cfgeventspawns.xml`. Vehicles use the event system, not the item spawn system.

### No matching spawn positions in cfgeventspawns.xml

**Problem:** You create a new vehicle event in `events.xml` but the vehicle never appears.

**Fix:** Add a matching `<event name="YourEventName">` block in `cfgeventspawns.xml` with enough `<pos>` entries. The event `name` in both files must match exactly. You need at least as many positions as your `nominal` value.

### Setting remove_damaged=0 for drivable vehicles

**Problem:** You set `remove_damaged="0"` on a vehicle event. Over time, the server fills with wrecked vehicles that never despawn, blocking spawn positions and tanking performance.

**Fix:** Keep `remove_damaged="1"` for all drivable vehicles (sedans, trucks, hatchbacks, boats). This ensures that when a vehicle is destroyed, the CE removes it and spawns a fresh one. Only set `remove_damaged="0"` for wreck objects (heli crashes, convoys) that are already damaged by design.

### Forgetting to set active=1

**Problem:** You configure a vehicle event but it never spawns.

**Fix:** Check the `<active>` tag. If it is set to `0`, the event is disabled. Some vanilla events like `StaticPoliceCar` ship with `active=0`. Set it to `1` to enable spawning.

### Not enough spawn positions for the nominal count

**Problem:** You set `nominal=15` for a vehicle event but only 6 positions exist in `cfgeventspawns.xml`. Only 6 vehicles ever spawn.

**Fix:** Add more `<pos>` entries. As a rule, include at least 2-3x your nominal value in positions to give the CE enough options to satisfy `saferadius` and `distanceradius` constraints.

### Vehicle spawns inside buildings or underground

**Problem:** A vehicle spawns clipped into a building or buried in terrain.

**Fix:** Review the `<pos>` coordinates in `cfgeventspawns.xml`. Test positions in-game using admin teleport before adding them to the file. Positions should be on flat roads or open ground, and the angle (`a`) should align with the road direction.
