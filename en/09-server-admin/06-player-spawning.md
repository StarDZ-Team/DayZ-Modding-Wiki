# Player Spawning


---

> **Summary:** Player spawn locations are controlled by **cfgplayerspawnpoints.xml** (position bubbles) and **init.c** (starting gear). This chapter covers both files with real vanilla values from Chernarus. For the JSON-based starting-gear preset system, see [Spawning Gear Configuration](../05-config-files/06-spawning-gear.md).

---

## Table of Contents

- [cfgplayerspawnpoints.xml Overview](#cfgplayerspawnpointsxml-overview)
- [File Structure](#file-structure)
- [Spawn Parameters](#spawn-parameters)
- [Generator Parameters](#generator-parameters)
- [Group Parameters](#group-parameters)
- [Fresh Spawn Bubbles](#fresh-spawn-bubbles)
- [Hop Spawns](#hop-spawns)
- [Map-Specific Configs](#map-specific-configs)
- [init.c -- Starting Equipment](#initc----starting-equipment)
- [Adding Custom Spawn Points](#adding-custom-spawn-points)
- [Common Mistakes](#common-mistakes)

---

## cfgplayerspawnpoints.xml Overview

This file lives in your mission folder (e.g., `dayzOffline.chernarusplus/cfgplayerspawnpoints.xml`). It has three sections, each with its own parameters and position bubbles:

- **`<fresh>`** -- brand new characters (first life or after death)
- **`<hop>`** -- server hoppers (player had a character on another server)
- **`<travel>`** -- in-game map travel/teleport spawns

`<fresh>` is required. `<hop>` and `<travel>` are only used on official-style server hives, but should still be defined -- see [Common Mistakes](#common-mistakes).

---

## File Structure

Each of the three sections contains the same three sub-elements: `<spawn_params>` (runtime scoring), `<generator_params>` (candidate grid generation), and `<generator_posbubbles>` (the actual positions):

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<playerspawnpoints>
    <fresh>
        <spawn_params>...</spawn_params>
        <generator_params>...</generator_params>
        <generator_posbubbles>...</generator_posbubbles>
    </fresh>
    <hop>
        <spawn_params>...</spawn_params>
        <generator_params>...</generator_params>
        <generator_posbubbles>...</generator_posbubbles>
    </hop>
    <travel>
        <spawn_params>...</spawn_params>
        <generator_params>...</generator_params>
        <generator_posbubbles>...</generator_posbubbles>
    </travel>
</playerspawnpoints>
```

---

## Spawn Parameters

Vanilla fresh spawn values:

```xml
<spawn_params>
    <min_dist_infected>30</min_dist_infected>
    <max_dist_infected>70</max_dist_infected>
    <min_dist_player>65</min_dist_player>
    <max_dist_player>150</max_dist_player>
    <min_dist_static>0</min_dist_static>
    <max_dist_static>2</max_dist_static>
</spawn_params>
```

| Parameter | Value | Meaning |
|-----------|-------|---------|
| `min_dist_infected` | 30 | Player must spawn at least 30m from the nearest infected |
| `max_dist_infected` | 70 | If no position exists 30m+ away, accept up to 70m as fallback range |
| `min_dist_player` | 65 | Player must spawn at least 65m from any other player |
| `max_dist_player` | 150 | Fallback range -- accept positions up to 150m from other players |
| `min_dist_static` | 0 | Minimum distance from static objects (buildings, walls) |
| `max_dist_static` | 2 | Maximum distance from static objects -- keeps players close to structures |

**Scoring logic:** the engine scores each candidate point rather than applying hard cutoffs, and the higher the score the more likely the point is chosen. Bohemia draws the curve in the mission file's own comments, with five anchor values:

```
distance:    0           min    mid    max          MAX
             |============|======|======|============|
score:      -1           0.1    1.1    0.1           0
```

Read left to right: a point right on top of whatever is being measured scores `-1`, and the score climbs to `0.1` at `min_dist`, peaks at `1.1` midway between `min_dist` and `max_dist`, falls back to `0.1` at `max_dist`, and tails off to `0` at the engine's maximum considered distance. Both ends are ramps, not cliffs -- a point closer than `min_dist` is *very unlikely* rather than forbidden, and a point past `max_dist` still scores above zero for a while. The engine therefore strongly prefers the middle of the `min_dist`--`max_dist` band and falls back outward when nothing better exists.

**Per-parameter weights.** Bohemia annotates a weight on every `spawn_params` child, so the four distance measures do not count equally toward the total:

| Measure | Weight |
|---------|--------|
| `min_dist_infected` / `max_dist_infected` | 2x |
| `min_dist_player` / `max_dist_player` | 3x |
| `min_dist_static` / `max_dist_static` | 1x |
| `min_dist_trigger` / `max_dist_trigger` | 6x |

Distance from other players counts three times as heavily as distance from buildings, and the trigger pair -- where present -- dominates at 6x. The total is also influenced by the static score the generator computed for that point.

> **Sakhal:** the `min_dist_trigger` / `max_dist_trigger` pair (the 6x row above) appears in the Sakhal mission, which sets them to 50 and 100. The weights and the curve above are quoted from the comments in `dayzOffline.sakhal/cfgplayerspawnpoints.xml`.

---

## Generator Parameters

The generator creates a grid of candidate positions around each bubble:

```xml
<generator_params>
    <grid_density>4</grid_density>
    <grid_width>200</grid_width>
    <grid_height>200</grid_height>
    <min_dist_static>0</min_dist_static>
    <max_dist_static>2</max_dist_static>
    <min_steepness>-45</min_steepness>
    <max_steepness>45</max_steepness>
</generator_params>
```

| Parameter | Value | Meaning |
|-----------|-------|---------|
| `grid_density` | 4 | Sampling frequency (number of subdivisions) of the grid -- higher = more candidates, higher CPU cost. Spacing between points = `grid_width` / `grid_density` |
| `grid_width` | 200 | Total width of the candidate grid in meters (centered on the bubble) -- extends ~100m to each side on the X axis |
| `grid_height` | 200 | Total height of the candidate grid in meters (centered on the bubble) -- extends ~100m to each side on the Z axis |
| `min_dist_static` | 0 | Minimum distance from static objects. Bohemia's note: points **below** this are *discarded* during binarisation. Chernarus sets 0, so nothing is discarded on this basis; Sakhal sets 3. |
| `max_dist_static` | 2 | Maximum distance from static objects. Bohemia's note: points **above** this are not discarded, just *less likely* than those inside the range. Sakhal sets 10. |
| `min_steepness` / `max_steepness` | -45 / 45 | Terrain slope range in degrees -- points outside the range are discarded during binarisation, which rejects cliff faces and steep hills. Sakhal narrows this to -30 / 30. |

Each bubble gets a 200x200 m grid subdivided `grid_density` times per axis, so each cell is `grid_width` / `grid_density` = 200/4 = 50 m across and the candidates sit on the cell corners. Bohemia's diagrams in the mission file make the count explicit: density 4 draws a 5x5 lattice (**25** candidates) and density 8 a 9x9 one (81). The engine filters by steepness and static distance and discards points that overlap objects or fall in water, then applies `spawn_params` at spawn time.

`grid_density` must be at least `1` and cannot exceed the smaller of `grid_width` and `grid_height`. When set to `0`, only the bubble's center point is used as a candidate.

#### `allow_in_water` Parameter (1.28+)

DayZ 1.28 added a boolean `allow_in_water` child to `generator_params`, defaulting to `false`. Bohemia's stable changelog lists it verbatim under **SERVER**. The source is the *Stable Update 1.28* thread in the official, read-only **PC Stable Updates** forum, posted 2025-06-02 by a DayZ Community Support account, under the post's own heading *"PC Stable 1.28 Update 1 - Version 1.28.159992 (Release on 03.06.2025)"*:

> Added: "allow_in_water" bool to "generator_params" in "cfgplayerspawnpoints.xml" defaulting to "false"

The `false` behaviour is separately documented by Bohemia inside the Sakhal mission's own `cfgplayerspawnpoints.xml`, which comments the generator as *"Generated spawn points which overlap with objects or water are discarded."* Setting the flag to `true` is described by its name and by that default as lifting the water half of that filter; Bohemia has published no further description of the `true` case, so treat the exact behaviour as inferred rather than documented.

```xml
<generator_params>
    <grid_density>4</grid_density>
    <grid_width>200</grid_width>
    <grid_height>200</grid_height>
    <min_dist_static>0</min_dist_static>
    <max_dist_static>2</max_dist_static>
    <min_steepness>-45</min_steepness>
    <max_steepness>45</max_steepness>
    <allow_in_water>false</allow_in_water>
</generator_params>
```

By default the generator discards candidate positions that fall in water. Setting `allow_in_water` to `true` is what lifts that filter.

Two practical notes:

- **You have to add the element yourself.** `allow_in_water` appears in none of Bohemia's shipped mission files -- a full-text search of the official [DayZ-Central-Economy](https://github.com/BohemiaInteractive/DayZ-Central-Economy) repository at commit `9a21bb9` (2026-08-13) finds zero occurrences repository-wide -- the repository holds 17 mission folders, of which only three (`dayzOffline.chernarusplus`, `dayzOffline.enoch`, `dayzOffline.sakhal`) contain a `cfgplayerspawnpoints.xml` at all, and `allow_in_water` appears in none of them, nor anywhere else in the repository -- and the official [Player Spawning Configuration](https://community.bistudio.com/wiki/DayZ:Player_Spawning_Configuration) wiki page does not list it either (that page was last edited 2024-02-06, before 1.28). That is expected for an optional parameter whose default is `false`; it is not evidence against the parameter, but it does mean there is no vanilla example to copy.
- **Leave it at `false` unless you specifically want water spawns.** The scenario usually cited for `true` is a custom map with island or coastal spawns. This audit found no Bohemia-authored guidance on when to enable it.

---

## Group Parameters

```xml
<group_params>
    <enablegroups>true</enablegroups>
    <groups_as_regular>true</groups_as_regular>
    <lifetime>120</lifetime>
    <counter>2</counter>
</group_params>
```

| Parameter | Value | Meaning |
|-----------|-------|---------|
| `enablegroups` | true | Position bubbles are organized into named groups and rotate over time |
| `groups_as_regular` | true | Only relevant when `enablegroups` is `false`: treat grouped positions as regular spawn points instead of ignoring them |
| `lifetime` | 120 | Seconds a spawn group stays active before the system swaps to another group. -1 = disabled |
| `counter` | 2 | Number of logins a group stays active before being swapped (per-group). -1 = disabled |

`lifetime` controls how long a spawn group remains the active group before the system swaps to another group; it is not a per-position lockout. Spacing between simultaneous spawns is enforced by `min_dist_player`.

Individual groups can override the global `lifetime` and `counter` values via attributes:

```xml
<group name="Tents" lifetime="300" counter="25">
    <pos x="4212.421875" z="11038.256836" />
</group>
```

**Without groups**, positions are listed directly under `<generator_posbubbles>` and the engine treats them as one flat pool:

```xml
<generator_posbubbles>
    <pos x="4212.421875" z="11038.256836" />
    <pos x="4712.299805" z="10595" />
    <pos x="5334.310059" z="9850.320313" />
</generator_posbubbles>
```

---

## Fresh Spawn Bubbles

Vanilla Chernarus defines 11 groups along the coast for fresh spawns. Each group clusters 3-8 positions around a town:

| Group | Positions | Area |
|-------|-----------|------|
| WestCherno | 4 | West side of Chernogorsk |
| EastCherno | 4 | East side of Chernogorsk |
| WestElektro | 5 | West Elektrozavodsk |
| EastElektro | 4 | East Elektrozavodsk |
| Kamyshovo | 5 | Kamyshovo coastline |
| Solnechny | 5 | Solnechniy factory area |
| Orlovets | 4 | Between Solnechniy and Nizhnoye |
| Nizhnee | 4 | Nizhnoye coast |
| SouthBerezino | 3 | Southern Berezino |
| NorthBerezino | 8 | Northern Berezino + extended coast |
| Svetlojarsk | 3 | Svetlojarsk harbor |

### Real Group Examples

```xml
<generator_posbubbles>
    <group name="WestCherno">
        <pos x="6063.018555" z="1931.907227" />
        <pos x="5933.964844" z="2171.072998" />
        <pos x="6199.782715" z="2241.805176" />
        <pos x="13552.5654" z="5955.893066" />
    </group>
    <group name="WestElektro">
        <pos x="8747.670898" z="2357.187012" />
        <pos x="9363.6533" z="2017.953613" />
        <pos x="9488.868164" z="1898.900269" />
        <pos x="9675.2216" z="1817.324585" />
        <pos x="9821.274414" z="2194.003662" />
    </group>
    <group name="Kamyshovo">
        <pos x="11830.744141" z="3400.428955" />
        <pos x="11930.805664" z="3484.882324" />
        <pos x="11961.211914" z="3419.867676" />
        <pos x="12222.977539" z="3454.867188" />
        <pos x="12336.774414" z="3503.847168" />
    </group>
</generator_posbubbles>
```

Coordinates use `x` (east-west) and `z` (north-south). The Y axis (altitude) is calculated automatically from the terrain heightmap.

---

## Hop Spawns

Hop spawns are more lenient on player distance and use smaller grids:

```xml
<!-- Hop spawn_params differences from fresh -->
<min_dist_player>25.0</min_dist_player>   <!-- fresh: 65 -->
<max_dist_player>70.0</max_dist_player>   <!-- fresh: 150 -->
<min_dist_static>0.5</min_dist_static>    <!-- fresh: 0 -->

<!-- Hop generator_params differences -->
<grid_width>150</grid_width>              <!-- fresh: 200 -->
<grid_height>150</grid_height>            <!-- fresh: 200 -->

<!-- Hop group_params differences -->
<enablegroups>false</enablegroups>        <!-- fresh: true -->
<lifetime>360</lifetime>                  <!-- fresh: 120 -->
```

Hop groups are spread **inland**: Balota (6), Cherno (5), Pusta (5), Kamyshovo (4), Solnechny (5), Nizhnee (6), Berezino (5), Olsha (4), Svetlojarsk (5), Dobroye (5). With `enablegroups=false`, the engine treats all 50 positions as a flat pool.

---

## Map-Specific Configs

Each map ships its own `cfgplayerspawnpoints.xml` in its mission folder:

| Map | Mission Folder | Notes |
|-----|----------------|-------|
| Chernarus | `dayzOffline.chernarusplus/` | Coastal spawns: Cherno, Elektro, Kamyshovo, Berezino, Svetlojarsk |
| Livonia | `dayzOffline.enoch/` | Spread across the map with different group names |
| Sakhal | `dayzOffline.sakhal/` | Adds `min_dist_trigger`/`max_dist_trigger` params, more detailed comments |

When creating a custom map or modifying spawn locations, always work from the vanilla file for your map as a starting point and adjust positions to match the geography.

---

## init.c -- Starting Equipment

The **init.c** file in your mission folder controls character creation and starting gear. Two overrides matter:

- **`CreateCharacter`** -- calls `GetGame().CreatePlayer()`. The engine picks the position from **cfgplayerspawnpoints.xml** before this runs; you do not set spawn position here.
- **`StartingEquipSetup`** -- runs after character creation. The player already has default clothing (shirt, jeans, sneakers). This method adds starting items.

> **Note:** If JSON spawn gear presets are registered through `cfggameplay.json`, they take priority and `StartingEquipSetup()` is never called. See [Spawning Gear Configuration](../05-config-files/06-spawning-gear.md).

### Vanilla StartingEquipSetup (Chernarus)

```c
override void StartingEquipSetup(PlayerBase player, bool clothesChosen)
{
    EntityAI itemClothing;
    EntityAI itemEnt;
    float rand;

    itemClothing = player.FindAttachmentBySlotName( "Body" );
    if ( itemClothing )
    {
        SetRandomHealth( itemClothing );  // 0.45 - 0.65 health

        itemEnt = itemClothing.GetInventory().CreateInInventory( "BandageDressing" );
        player.SetQuickBarEntityShortcut(itemEnt, 2);

        string chemlightArray[] = { "Chemlight_White", "Chemlight_Yellow", "Chemlight_Green", "Chemlight_Red" };
        int rndIndex = Math.RandomInt( 0, 4 );
        itemEnt = itemClothing.GetInventory().CreateInInventory( chemlightArray[rndIndex] );
        SetRandomHealth( itemEnt );
        player.SetQuickBarEntityShortcut(itemEnt, 1);

        rand = Math.RandomFloatInclusive( 0.0, 1.0 );
        if ( rand < 0.35 )
            itemEnt = player.GetInventory().CreateInInventory( "Apple" );
        else if ( rand > 0.65 )
            itemEnt = player.GetInventory().CreateInInventory( "Pear" );
        else
            itemEnt = player.GetInventory().CreateInInventory( "Plum" );
        player.SetQuickBarEntityShortcut(itemEnt, 3);
        SetRandomHealth( itemEnt );
    }

    itemClothing = player.FindAttachmentBySlotName( "Legs" );
    if ( itemClothing )
        SetRandomHealth( itemClothing );
}
```

What this gives each player: **BandageDressing** (quickbar 2), random **Chemlight** (quickbar 1), random fruit -- 35% Apple, 30% Plum, 35% Pear (quickbar 3). `SetRandomHealth` sets 45-65% condition on all items.

### Adding custom starting gear

```c
// Add after the fruit block, inside the Body slot check
itemEnt = player.GetInventory().CreateInInventory( "KitchenKnife" );
SetRandomHealth( itemEnt );
```

---

## Adding Custom Spawn Points

To add a custom spawn group, edit the `<fresh>` section of **cfgplayerspawnpoints.xml**:

```xml
<group name="MyCustomSpawn">
    <pos x="7500.0" z="7500.0" />
    <pos x="7550.0" z="7520.0" />
    <pos x="7480.0" z="7540.0" />
    <pos x="7520.0" z="7480.0" />
</group>
```

Steps:

1. Open your map in-game or use iZurvive to find coordinates
2. Pick 3-5 positions spread across 100-200m in a safe area (no cliffs, no water)
3. Add the `<group>` block inside `<generator_posbubbles>`
4. Use `x` for east-west and `z` for north-south -- the engine calculates Y (altitude) from the terrain
5. Restart the server -- no persistence wipe required

For balanced spawning, keep at least 4 positions per group so a single group has enough spread to keep `min_dist_player` satisfied when multiple players die at once.

> **Position format:** The `x` and `z` attributes use DayZ world coordinates. `x` is east-west, `z` is north-south. The `y` (height) coordinate is not specified --- the engine places the point on the terrain surface. You can find coordinates using the in-game debug monitor or the DayZ Editor mod (a free community tool).

---

## Common Mistakes

### Players spawning in the ocean

You swapped `z` (north-south) with Y (altitude), or used coordinates outside the 0-15360 range. Coast positions have low `z` values (south edge). Double-check with iZurvive.

### Not enough spawn points

With only 2-3 positions, the active group cannot spread players out and clustering results. Vanilla uses 49 fresh positions across 11 groups. Aim for at least 20 positions in 4+ groups.

### Forgetting the hop section

An empty `<hop>` section means server hoppers spawn at `0,0,0` -- the ocean on Chernarus. Always define hop points, even if you copy them from `<fresh>`.

### Spawn points on steep terrain

The generator rejects slopes beyond 45 degrees. If all custom positions are on hillsides, no valid candidates exist. Use flat ground near roads.

### Players always spawning at the same spot

Groups with 1-2 positions have too few candidates for the engine to vary the chosen position. Add more positions per group.
