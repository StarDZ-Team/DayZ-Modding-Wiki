# PBO limits and multi-PBO architecture research

**Audit date:** 2026-09-13  
**Scope:** English wiki research only; no wiki page was edited and no claim below is council-approved.  
**Repository checkpoint:** branch `wiki-reorg`, HEAD `789abaf29df2642912c4b7c7e05b18ff514d1665`; reviewed wiki files are additionally identified by hashes because the worktree contains unrelated changes.  
**Machine context:** Windows; retail `DayZ_x64.exe` file version `1.29.0.163709`; DayZ Experimental Tools Steam build `23909709`; installed Addon Builder file version `1.0.240.639`.  
**Evidence index:** [`pbo-evidence.json`](pbo-evidence.json) records the exact source snapshots, hashes, repository commits, line/symbol scopes, observations, and limitations used here.

---

## Executive conclusion

The current wiki is right not to publish a numeric total-PBO engine ceiling. The available format description uses 32-bit fields for each member's original and stored sizes, but its nominal offset field is unused/reserved and the archive has no single total-length field. That supports a per-field representability statement, not a universal 2 GiB or 4 GiB DayZ archive limit. Tool implementations, engine readers, signing tools, local filesystems, memory, and Steam distribution are separate boundaries and require separate evidence.

The wiki's multi-PBO guidance needs a sharper model. A mod folder is selected with `-mod` or `-serverMod`; a PBO is a physical archive; its prefix mounts member names into a virtual tree; a `CfgPatches` class is an addon identity that can be named in `requiredAddons[]`; and `CfgMods` registers script/input modules by virtual paths. Confusing any of these produces bad dependency, load-order, and client/server advice.

There are also concrete repair candidates: the PBO structure description calls a reserved field an offset, the supplied multi-PBO build examples do not reliably name or sign every output, server-only exclusion is described at PBO instead of mod-folder granularity, the key-rotation advice contradicts the publishing chapter, `inputs` is described as relative to the PBO root, and the publishing chapter treats command-line order as a substitute for addon dependencies.

---

## What was actually inspected

### Current English pages

The following current files were opened rather than inferred from earlier audit reports:

- `en/04-file-formats/06-pbo-packing.md` in full (SHA-256 `D60F2BE9D40C4B8DEF8373C24B780A2F8A62C31ED32895663F0A2BC314A4A586`).
- `en/02-mod-structure/01-five-layers.md` through `06-server-client-split.md`, with detailed review of `02-config-cpp.md` (SHA-256 `8AF40F97A560E63F45AB69DD67694BBA22B56BEEC1C07019E37FBCAC135E0AB1`), `05-file-organization.md`, and `06-server-client-split.md` (SHA-256 `EFBBD4214B68F07B3AC30888823FA7E4A717CFA125AA829391104BD56B6DA05A`). `01-five-layers.md` was reopened during the author revision and hashes to `1C8571C015339DD7508D92C519A0F6A563B3790D5120ED776832EFBA345C8413`.
- The relevant build, layout, publishing, and testing sections in `en/08-tutorials/01-first-mod.md`, `05-mod-template.md`, `06-debugging-testing.md`, `07-publishing-workshop.md` (SHA-256 `B7F98787CE9554A91A8B3A6B2C2FEE41C32E11491D48CCD2BAC7D8E2CA6C7A55`), and `09-professional-template.md`.

### Official and primary material

- Bohemia Interactive Community Wiki pages: [Addon Builder](https://community.bistudio.com/wiki/Addon_Builder?oldid=341605), [DayZ Modding Basics](https://community.bistudio.com/wiki/DayZ:Modding_Basics), [DayZ Modding Structure](https://community.bistudio.com/wiki/DayZ:Modding_Structure), [PBO File Format](https://community.bistudio.com/wiki/PBO_File_Format), [CfgPatches](https://community.bistudio.com/wiki/CfgPatches), and [DayZ Server Configuration](https://community.bistudio.com/wiki/DayZ:Server_Configuration). The PBO format page itself says that the format is unofficial/undocumented; it must not be represented as a supported DayZ specification. Direct requests later returned HTTP 403, so locally captured rendered snapshots and the successfully opened revision were retained as the access record.
- The installed official tools were invoked for their own help output. Addon Builder `1.0.240.639` exposes `-packonly`, `-prefix` (automatic if absent), `-sign`, and conversion/tool-path options, but no compression switch. The installed FileBank help exposes `-property`, `-exclude`, and `-dst`, also with no compression switch. `DSSignFile` documents v3 as its default and `-v2` as an option; `DSCheckSignatures` documents directory and keys-directory arguments.
- The official [DayZ Samples](https://github.com/BohemiaInteractive/DayZ-Samples/tree/da5e5437c9502620d9853fb6eed14701135ab2ea) checkout at commit `da5e5437c9502620d9853fb6eed14701135ab2ea`, especially `Test_Inputs/config.cpp` and the multiple `Test_Terrain` config roots.
- The official-tool extraction under `D:\DayZ Projects`, especially `scripts/config.cpp` and `DZ/data_sakhal/config.cpp`. Extraction time was 2026-09-11, but no immutable game-build receipt was found beside it; conclusions from this tree therefore have extraction provenance but not a proven exact runtime version.
- The installed retail archive `D:\SteamLibrary\steamapps\common\DayZ\dta\core.pbo`, including its raw header/property records, and the retail `Addons` inventory. These are observations of build `1.29.0.163709`, not boundary tests.
- Valve's official [Steam Workshop implementation documentation](https://partner.steamgames.com/doc/features/workshop/implementation). It describes item content upload/update APIs and SteamCMD workflow but did not provide a fixed DayZ Workshop content-size ceiling in the reviewed page. Absence from one page is not proof that no platform limit exists.

### Public implementations and local project material

- Community Framework commit [`0763e7e`](https://github.com/Arkensor/DayZ-CommunityFramework/tree/0763e7e7548c9a0bed6626afff835de80693ebf3), COT commit [`41f2c2b`](https://github.com/Jacob-Mango/DayZ-CommunityOnlineTools/tree/41f2c2b99565d0e3970163e162efbf1283fdca62), VPP Admin Tools commit [`dc22e42`](https://github.com/VanillaPlusPlus/VPP-Admin-Tools/tree/dc22e420df3b54e821055f9764da1e48f4a31e71), DayZ Expansion Scripts commit [`6dacd00`](https://github.com/salutesh/DayZ-Expansion-Scripts/tree/6dacd00f6d943ebbd99e0cf1baad93f470d96419), and DayZ Editor commit [`992e6b2`](https://github.com/InclementDab/DayZ-Editor/tree/992e6b29b42b5d8e609632b59771335a23d205eb). These show implementation choices, not engine contracts.
- `D:\StarDZ\dev.py`, StarDZ Core client/server configs, current beta PBOs, `D:\StarDZ\docs\GUIA_FERRAMENTAS_E_BUILD.md`, `GUIA_DEBUG_E_PERFORMANCE.md`, and the locally saved `DayZ/Modding Structure.md`. Project docs and beta mods were treated as fallible leads.
- Third-party open-source parser/writer [armake2](https://github.com/KoffeinFlummi/armake2/blob/3cc3362101900ff41504db3e780dd1625634cf94/src/pbo.rs) at commit `3cc3362101900ff41504db3e780dd1625634cf94`, used only to corroborate the byte layout and sequential payload interpretation. It is not Bohemia or DayZ runtime evidence.

---

## Findings and exact proposed repairs

### PBO-001 — Correct the archive-header description

**Affected page:** `en/04-file-formats/06-pbo-packing.md`, current internal-structure bullet around line 39.  
**Current problem:** “paths, sizes, and offsets” implies that the archive relies on a usable per-entry offset. The unofficial format description names an `Offset` field but says it is not used and is normally zero. The inspected retail `core.pbo` has zero in that position for sampled entries, and armake2 reads payloads sequentially from the data block.

**Proposed replacement:**

> **Header entries and contiguous payloads:** each member header stores a path, packing method, uncompressed size, a reserved field, a timestamp, and stored size. The field historically labelled `Offset` is normally zero; readers locate member payloads by walking the contiguous data block. This layout is reverse-engineered rather than a Bohemia-supported DayZ file-format contract.

**Evidence:** `PBO File Format` field table and disclaimer; retail `core.pbo` SHA-256 `36ECFCE1062C31EAAEDC59F23D64CEA84DD79A52482145402582EB35BC1AB043`; armake2 `src/pbo.rs` lines 18-25, 52-70, 97-142.  
**Validation after editing:** compare the final prose against a hex/header dump of at least one retail PBO and one newly built test PBO; do not call the reserved field a runtime seek offset unless an engine/tool test proves that behavior.

### PBO-002 — Add a limits section that separates six different boundaries

**Affected page:** `en/04-file-formats/06-pbo-packing.md`, after internal structure or before “Multi-PBO Architecture.”  
**Gap:** The page avoids a numeric ceiling but does not explain why familiar 2 GiB/4 GiB claims are unproven.

**Proposed addition:**

> ## PBO Size Limits: What Is and Is Not Established
>
> Treat these as separate boundaries:
>
> | Boundary | What the evidence establishes |
> |---|---|
> | Member fields | The reverse-engineered header stores `OriginalSize` and `DataSize` as unsigned 32-bit values for one member. A value above 4,294,967,295 cannot be represented in either field. This is a field-width fact, not a tested usable-member maximum. |
> | Total archive format | The reviewed layout has no single 32-bit total-archive-size field, and its historical `Offset` field is unused/reserved. “The header uses 32-bit integers” therefore does not by itself prove a 4 GiB total-PBO ceiling. |
> | Packer and signer | Addon Builder, FileBank, and DS tools can have their own implementation limits. Record the exact tool build and retain its output when testing a boundary. |
> | DayZ runtime | A loader can fail below or above a format-field boundary for unrelated reasons. No authoritative, versioned DayZ total-PBO ceiling was found for this audit. |
> | Filesystem and deployment | Filesystem, copy, host, and server-management tools are independent limits. |
> | Workshop distribution | Steam Workshop item transfer/storage is a separate service concern. Do not infer its limit from PBO fields, and do not present a number without a current Valve/DayZ source or a reproducible upload result. |
>
> As a shipping-build observation, retail DayZ `1.29.0.163709` had 117 files in `Addons`, totaling 21,638,391,975 bytes; the largest inspected PBO was 1,216,702,399 bytes. Those values show that Bohemia ships multiple archives and are not lower or upper limits.
>
> Prefer multiple cohesive PBOs well before a single archive becomes slow or difficult to build, sign, upload, diagnose, and replace. If you investigate a boundary, vary one condition at a time and record the exact PBO bytes and SHA-256, tool build, game/server build, launch arguments, RPT/minidump, and client/server result. A single project crash is a warning, not a universal engine limit.

**Evidence and contradiction:** The local Portuguese build guide infers a 4 GiB total ceiling from `ulong` fields and reports a 2,165,383,988-byte PBO crash versus a 1,471,395,178-byte success. No failing archive, RPT, or minidump was retained in the reviewed tree, so that test could not be replayed. Preserve it as a project-specific lead, not a DayZ rule. Current StarDZ code intentionally splits large rifle assets, which is operationally sensible without promoting the historic result to a hard limit.  
**Validation after editing:** council should independently reproduce controlled boundary cases on the named DayZ and tool builds before adding any numeric engine threshold.

### PBO-003 — State compression evidence narrowly

**Affected page:** `en/04-file-formats/06-pbo-packing.md`, “PBO Internal Structure” and Addon Builder options.  
**Gap:** The current page correctly warns that old FileBank `-compress` advice is unsupported, but it lacks versioned tool evidence and can leave “PBOs are flat” sounding like the format cannot contain compressed members.

**Proposed addition:**

> The reverse-engineered format recognizes a `Cprs` member marker and stores both original and stored size, so member compression exists in the format family. However, the installed DayZ Experimental Tools Addon Builder `1.0.240.639` and FileBank help expose no compression switch. Do not document obsolete `-compress` commands or promise ZIP-style whole-archive compression. Asset conversion and format-specific compression performed before or during binarization are separate from PBO member packing.

**Evidence:** official installed Addon Builder/FileBank help and hashes in the evidence index; unofficial PBO format `Cprs` description.  
**Validation after editing:** build representative content, inspect packing markers and stored/original sizes, and report the actual tool version. Do not infer compression solely from a smaller final file.

### PBO-004 — Replace the mental model for multi-PBO dependencies

**Affected pages:** primary addition to `en/04-file-formats/06-pbo-packing.md`; align `en/02-mod-structure/02-config-cpp.md` and `05-file-organization.md`.  
**Current problem:** The page says `requiredAddons[]` establishes inter-PBO order but does not explain which name is referenced; its example lists several physical PBOs while showing only one addon identity.

**Proposed addition:**

> ### Four names you must keep separate
>
> | Layer | Example | Purpose |
> |---|---|---|
> | Launch package | `@MyMod` in `-mod=@MyMod` | Makes a mod folder and its PBOs available to that process. |
> | Physical archive | `MyMod_Scripts.pbo` | Build, signing, and distribution unit. Its filename is not a dependency identifier. |
> | Virtual root | `MyMod/Scripts` prefix | Mounts each member as a virtual path such as `MyMod/Scripts/3_Game/Foo.c`. |
> | Addon identity | `MyMod_Scripts` in `CfgPatches` | Name used by another addon's `requiredAddons[]`. |
>
> `requiredAddons[]` contains `CfgPatches` class names, not PBO filenames, prefixes, mod-folder names, or Workshop IDs. It establishes addon initialization dependencies only after the packages that contain those addons have been installed and placed on the relevant launch list; it does not download or discover a missing package.
>
> Give every independently load-ordered configuration addon a unique `CfgPatches` class. Do not assert one `CfgPatches` identity per physical PBO: a PBO can expose additional configuration roots, and shipping resource PBOs can be observed without a root config. Treat those observations as engine-content layout evidence, not as a documented public-mod contract. Put `CfgMods` only where you need to register scripts, inputs, or GUI resources. Its `files[]` and `inputs` values are mounted virtual paths; its `dependencies[]` labels are not a substitute for `requiredAddons[]` or a physical-PBO dependency declaration.

**Proposed example:**

```cpp
// MyMod_Core/config.cpp -> MyMod_Core.pbo
class CfgPatches
{
    class MyMod_Core
    {
        requiredAddons[] = { "DZ_Data" };
    };
};

// MyMod_Scripts/config.cpp -> MyMod_Scripts.pbo
class CfgPatches
{
    class MyMod_Scripts
    {
        requiredAddons[] = { "MyMod_Core", "DZ_Scripts" };
    };
};

class CfgMods
{
    class MyMod
    {
        type = "mod";
        class defs
        {
            class worldScriptModule
            {
                value = "";
                files[] = { "MyMod/Scripts/4_World" };
            };
        };
    };
};
```

**Evidence:** official DayZ Modding Basics/Structure; DayZ Samples `Test_Inputs` and `Test_Terrain`; extracted `DZ/data_sakhal/config.cpp`; CF, COT, and Expansion pinned configs. `CfgPatches` is also documented in BI's cross-game reference; DayZ-specific examples were used to avoid treating Arma-only details as DayZ proof.  
**Validation after editing:** pack to distinct PBOs, remove loose source, launch without `-filePatching`, and confirm from RPT that all dependencies resolve and the registered module executes. Then omit one required package to capture the real error path. Static reading alone does not validate loader behavior.

### PBO-005 — Make prefix collision rules testable

**Affected page:** `en/04-file-formats/06-pbo-packing.md`, current same-prefix advice around lines 558-565.  
**Current status:** The warning to avoid overlaps should be retained and strengthened. Sharing a prefix is a virtual-tree merge, not a dependency relationship.

**Proposed replacement:**

> Sharing a prefix is not itself a dependency mechanism or proof of an error. As a conservative release policy, normalize virtual paths case-insensitively across all PBOs and fail on duplicate paths by default. Permit a duplicate only through a documented allowlist backed by a controlled runtime test for the supported DayZ build; never rely on textual launch order to choose a winner. This policy is not a demonstrated universal engine requirement.

**Local contradiction worth preserving:** current StarDZ beta `StarDZ_Weapons_Rifles.pbo` and `StarDZ_Weapons_Rifles2.pbo` both mount `StarDZ_Weapons\Data\Weapons\Rifles\`. Their parsed file tables overlap at `config.cpp` and `texHeaders.bin`, with different `texHeaders.bin` sizes. This implementation is therefore a collision warning, not a best-practice example, even though both PBOs are currently loadable artifacts.  
**Validation after editing:** compute normalized, case-insensitive virtual paths (`prefix + member`) across all release PBOs and fail on duplicates. Preserve the inventory with the build receipt.

### PBO-006 — Repair build automation and signing order

**Affected page:** `en/04-file-formats/06-pbo-packing.md`, batch/Python examples around lines 372-467; cross-reference from `en/08-tutorials/09-professional-template.md`.  
**Current problems:** The batch example packs `Scripts` with `-packonly` but signs only `Data`. The Python table uses desired names such as `MyMod_Scripts`, but the command builds from leaf folders named `Scripts` and `Data`; the script never proves which output file Addon Builder created. It signs only the non-`packonly` branch. Both examples check too little and can leave stale/orphan outputs.

**Proposed replacement text and workflow:**

> Build each component from a separate source root with separate temporary and output directories. Invoke Addon Builder with a validated `-toolsDirectory` (or explicit dependency-tool paths), capture its log, reject `FATAL`/`ERROR`, and require exactly one newly created non-empty PBO. Discover that output, rename it to the manifest's final filename, inspect the final PBO's prefix and member table with BankRev, scan normalized virtual paths across the whole release, hash the final PBO, and only then sign those final bytes. Check the tool exit code **and** the exact expected files; a zero exit code alone does not prove that the desired artifact was created.
>
> For every component:
>
> 1. Clear or create a component-specific staging/output directory.
> 2. Run Addon Builder with an explicit prefix and the appropriate pack-only/binarization mode.
> 3. Require exactly one newly created PBO and move it to the manifest's final name.
> 4. Inspect the final PBO's prefix and normalized virtual member paths; reject collisions.
> 5. Sign the final PBO with the selected private key.
> 6. Require the matching `.bisign`, run `DSCheckSignatures` against a clean release-and-keys directory, interpret its stdout rather than its exit code alone, and record hashes.
> 7. Copy only manifest-listed PBOs, signatures, and public keys into the release package.

**Evidence:** installed official tool help; StarDZ `dev.py` lines 847-920, 1235-1258, and 1759-1781 shows a project solution for output detection, final naming, stale-output cleanup, isolated source leaves, and concurrency hazards; CF `Deploy.bat` lines 181-238 finds component config roots, builds components, and signs each result. The latter two are implementation examples, not guarantees about Addon Builder internals.  
**Validation after editing:** run the example from a dirty output directory containing an old unrelated PBO and verify that it still selects only the new expected artifact. The council experiment showed an old signature beside rebuilt bytes can still print `OK`, so DSCheck is not an end-to-end PBO-byte pairing proof; a real `verifySignatures=2` client/server join remains the final integration test.

### PBO-007 — Put the client/server boundary at the mod-folder level

**Affected pages:** `en/04-file-formats/06-pbo-packing.md` line 523 area and `en/02-mod-structure/06-server-client-split.md` line 197 area.  
**Current problem:** “Server-only PBOs can be excluded from client downloads” can be read as selective routing of PBOs inside a single `@Mod`. Official launch documentation describes `-mod` and `-serverMod` in terms of mod folders; it does not document per-PBO exclusion inside one package. The server/client page also says clients “download” a `-mod` package, which can imply that the server streams PBO data.

**Proposed PBO-page replacement:**

> **Distribution boundary:** `-mod=` and `-serverMod=` select mod folders/packages, not individual PBOs inside one `@Mod`. Put shared/client PBOs in `@MyMod` and load that package with `-mod`. Put code and assets that must remain server-only in a separate `@MyModServer` package and load it only with `-serverMod`. Do not place a server-only PBO inside the client Workshop package and assume DayZ will omit that file.

**Proposed server/client clarification:**

> Clients must already have a `-mod` package installed, normally through the launcher/Workshop workflow. A `-serverMod` package is loaded only by the server process and is not broadcast to clients. This describes launch routing; `CfgMods.type` is metadata and does not replace the launch flag.

**Evidence:** cached official DayZ Server Configuration snapshot lines 180-181; local official DayZ Modding Structure snapshot lines 6-14; existing page already correctly notes that BI documents only `type = "mod"`.  
**Validation after editing:** make two mod folders, put a uniquely named sentinel file/PBO only in `@MyModServer`, launch a dedicated server with `-serverMod`, connect a clean client, and verify the client installation/download contains no sentinel. Record the launcher/Workshop setup; do not infer distribution merely from successful server startup.

### PBO-008 — Correct `CfgMods` path wording

**Affected page:** `en/02-mod-structure/02-config-cpp.md`, `inputs` row around line 213 and the nearby `files[]` explanation.  
**Current problem:** `inputs` is described as relative to the PBO root. The official DayZ sample uses `samples\test_inputs\my_new_inputs.xml`, matching its mounted virtual namespace, and script module arrays likewise use complete virtual paths.

**Proposed replacement:**

> `inputs` and script-module `files[]` entries are virtual paths resolved after loaded PBO prefixes are mounted. For example, the official sample uses `samples\test_inputs\my_new_inputs.xml`. Do not rewrite these as paths relative to the physical PBO root. A path may be authored in one configuration and supplied from another archive only if the final mounted namespace resolves it; validate that cross-PBO arrangement in the packaged runtime instead of presenting it as proven by syntax alone.

**Evidence:** DayZ Samples `Test_Inputs/config.cpp` lines 9-33 and extracted Sakhal config lines 14-30.  
**Validation after editing:** inspect the packed prefix and member path, then launch PBO-only and prove that the input/module is discovered.

### PBO-009 — Do not substitute launch-string order for `requiredAddons[]`

**Affected page:** `en/08-tutorials/07-publishing-workshop.md`, server load-order guidance around lines 543-549.  
**Contradiction:** The publishing page advises intentional textual `-mod` order, while `en/02-mod-structure/02-config-cpp.md` correctly says launch-list order is not a substitute for `requiredAddons[]`.

**Proposed replacement:**

> The launch list makes each package available to the process. Declare addon initialization dependencies in `CfgPatches.requiredAddons[]`; each value is the prerequisite's `CfgPatches` class. Do not rely on textual `-mod=` ordering as a substitute. A dependency declaration also does not install or automatically add a missing package to the launch list.

**Evidence:** official DayZ Modding Basics and pinned COT/Expansion config dependency chains.  
**Validation after editing:** run both launch-list orders with correct `requiredAddons[]`; then remove the declaration in a controlled copy and compare RPT/config initialization results.

### PBO-010 — Fix signing scope and key rotation

**Affected pages:** `en/04-file-formats/06-pbo-packing.md` lines 47, 265-312, 641, 664-666, and 678-685; align `en/08-tutorials/07-publishing-workshop.md` lines 172-258 and 382-414.  
**Current problems:** “ensures the mod has not been tampered with” lacks the verifying-server context. “Generate a new key pair for breaking changes” and “key versioning per major release” contradict the publishing chapter and BI guidance that key replacement forces server operators to install the new public key.

**Proposed replacement:**

> Sign every distributed final PBO after its last byte-changing operation. Keep the private key out of the release and distribute the public `.bikey` to servers. Reuse an uncompromised, available key across ordinary updates; rotate after compromise, private-key loss or unavailability, or an intentional trust reset. Rotation requires servers to install the new public key.
>
> The installed `DSSignFile` reports signature v3 as its default and offers `-v2` explicitly; this is unrelated to `verifySignatures = 2`. In the council experiment, `DSCheckSignatures` accepted an old `.bisign` beside newly rebuilt PBO bytes and returned zero when the public key was missing. Treat it only as a stdout-interpreted signature/key check, not proof that adjacent PBO bytes match. Successful multiplayer connection to a clean `verifySignatures = 2` server is the integration test.

**Evidence:** official DayZ Modding Structure and Server Configuration for client/server verification context; installed DayZ DS tool help for signature versions and static checking; BI's cross-game [Creating an Addon](https://community.bistudio.com/wiki/Arma_3:_Creating_an_Addon) page for the explicit advice not to create a new key for every version because server operators would have to update it. The Arma page corroborates shared BI key mechanics but is not DayZ-specific runtime proof.  
**Unresolved scope:** The reviewed official DayZ page says `-serverMod` content is not broadcast to clients, but no authoritative DayZ source or retained test established whether signing a server-only, non-distributed PBO is required or useful. Avoid stating that every server-only PBO must have a `.bisign`; state the verification boundary and test the target server configuration.  
**Validation after editing:** connect with correct PBO/signature/key, then separately alter the PBO, remove the signature, and replace the server public key. Record disconnect messages and server/client RPTs for each case.

### PBO-011 — Replace vague “real mods” claims with pinned examples

**Affected page:** `en/04-file-formats/06-pbo-packing.md`, “Observed in real mods” around lines 678-685.  
**Current problem:** Named projects are cited without commits, paths, or a statement that they demonstrate third-party choices rather than DayZ guarantees.

**Proposed replacement:**

> Pinned implementation examples, not engine contracts. Every record was reviewed on 2026-09-13 and records URL, commit, local checkout, file/range, and SHA-256:
>
> - Community Framework [`0763e7e`](https://github.com/Arkensor/DayZ-CommunityFramework/tree/0763e7e7548c9a0bed6626afff835de80693ebf3), checkout `C:/Users/Leonardo Mello/AppData/Local/Temp/wiki-audit-20260911/DayZ-CommunityFramework`: `JM/CF/GUI/config.cpp` lines 1-13 (`3AA877B37DE71F381C7DD04D9A7DBB23761621A7BA9D85798528F1B1AA36F3D0`), `JM/CF/Scripts/config.cpp` lines 1-103 (`8DA49AD88AB7387B4F5E6D5D2FDBC07005F908B537E7F723152BD41B6BDD1D41`), and `Deploy.bat` lines 135-163,181-238 (`3D034012639290F267B5303D2C6164597230E05E6E49F7B9FCDE5EEFB45D8ABE`).
> - Community Online Tools [`41f2c2b`](https://github.com/Jacob-Mango/DayZ-CommunityOnlineTools/tree/41f2c2b99565d0e3970163e162efbf1283fdca62), checkout `C:/Users/Leonardo Mello/AppData/Local/Temp/wiki-audit-20260911/DayZ-CommunityOnlineTools`: `JM/COT/Scripts/config.cpp` lines 1-13 and `CfgMods` (`BD536BE5FB6E4053F8879D82779C8FE952FD95081F24B088D2C11BCC46EE2382`).
> - DayZ Expansion Scripts [`6dacd00`](https://github.com/salutesh/DayZ-Expansion-Scripts/tree/6dacd00f6d943ebbd99e0cf1baad93f470d96419), checkout `C:/Users/Leonardo Mello/AppData/Local/Temp/wiki-audit-20260911/DayZ-Expansion-Scripts`: `DayZExpansion/Core/Scripts/config.cpp` lines 1-110 (`8973F7648357EF6B1FFA70F0E8168915052674F412EB15B7090E6E38B41826EA`).
> - DayZ Editor [`992e6b2`](https://github.com/InclementDab/DayZ-Editor/tree/992e6b29b42b5d8e609632b59771335a23d205eb), checkout `C:/Users/Leonardo Mello/AppData/Local/Temp/wiki-audit-20260911/DayZ-Editor-extra`: `DayZEditor/Scripts/config.cpp` (`CfgPatches`/`CfgMods`, `1B0D5EC71A26F8B73BFBC2156CE303F65028C0CF6AFB09416AFA84F49A1BA39A`) and `DayZEditor/GUI/config.cpp` (`CfgPatches`, `39952D741DC3075102A923D93D24B74A63EBA0DD04DA7D1FECB8B1C225DC7447`).
> - VPP Admin Tools [`dc22e42`](https://github.com/VanillaPlusPlus/VPP-Admin-Tools/tree/dc22e420df3b54e821055f9764da1e48f4a31e71), checkout `C:/Users/Leonardo Mello/AppData/Local/Temp/wiki-audit-20260911/VPP-Admin-Tools`: `config.cpp` lines 1-10 (`39BD991B0E0CF043BAD82EF5D8F4C8FFCF9538D6E4E41C7B3CB81EC5A89E9061`), a monolithic/root-config choice rather than multi-PBO proof.
> - Official DayZ Samples [`da5e543`](https://github.com/BohemiaInteractive/DayZ-Samples/tree/da5e5437c9502620d9853fb6eed14701135ab2ea), checkout `C:/Users/Leonardo Mello/AppData/Local/Temp/wiki-audit-20260911/DayZ-Samples`: `Test_Inputs/config.cpp` lines 1-33 (`71B869D713C15D38037B0B8B6CC682CCAEA03599DDFF370DA786D42CD813121C`).

**Validation after editing:** council reopens each linked blob at the pinned commit and verifies the quoted class/path. Do not cite repository names alone.

### PBO-012 — Separate Workshop service limits from PBO limits

**Affected page:** `en/08-tutorials/07-publishing-workshop.md`, add a short limitations note near troubleshooting; cross-link the PBO limits section.  
**Proposed addition:**

> PBO format fields, DayZ loading, Publisher/SteamCMD behavior, and Steam Workshop item storage are separate limits. The official Steamworks upload page reviewed for this chapter did not state a fixed DayZ item-content ceiling. Record a current authoritative limit or a reproducible upload error before publishing a number. Splitting a mod into several PBOs does not by itself split it into several Workshop items or make a server-only PBO private; that requires an intentional package/Workshop layout.

**Validation after editing:** upload a controlled test item through the supported DayZ Publisher/SteamCMD path, retain tool logs and item manifest, and verify a clean subscriber receives the expected file set. No upload was performed in this audit.

---

## Recommended canonical multi-PBO layout

This example makes distribution and dependency boundaries explicit. It is a proposed documentation model, not a claim that these exact names were compiled or run during this audit.

```text
@MyMod/
├── Addons/
│   ├── MyMod_Core.pbo
│   ├── MyMod_Core.pbo.MyStudio.bisign
│   ├── MyMod_Scripts.pbo
│   ├── MyMod_Scripts.pbo.MyStudio.bisign
│   ├── MyMod_Data.pbo
│   └── MyMod_Data.pbo.MyStudio.bisign
├── Keys/
│   └── MyStudio.bikey
├── mod.cpp
└── meta.cpp

@MyModServer/
├── Addons/
│   └── MyMod_Server.pbo
└── mod.cpp
```

Launch the shared/client package on both server and clients with `-mod=@MyMod`. Launch the separate server package only on the server with `-serverMod=@MyModServer`. Inside the archives, use stable prefixes, unique `CfgPatches` identities, and one-way `requiredAddons[]` edges: for example `MyMod_Server -> MyMod_Scripts -> MyMod_Core -> DZ_Data`, never a cycle. If the server addon depends on a shared addon, both packages must be installed and listed on the server.

Do not infer the PBO filename from the addon class or vice versa. Keep a build manifest that maps source root, desired output filename, prefix, `CfgPatches` class, binarization mode, signing key, and distribution package for every component.

---

## Validation matrix for the eventual implementation

| Claim being validated | Minimum check | What it does not prove |
|---|---|---|
| Prefix and virtual members | Inspect every final PBO's properties/file table; compute normalized virtual paths and reject duplicates | Engine startup or script execution |
| Addon dependency | PBO-only launch with all dependencies, then a controlled missing-dependency run; retain RPT | Client/server distribution |
| `CfgMods` module/input path | Execute a sentinel from the packed module/input and record its expected log/action | All game versions or all module types |
| Build automation | Start with stale unrelated PBOs; require exact manifest outputs, signatures, and hashes | Runtime correctness |
| Signature | `DSCheckSignatures` on a clean release, followed by success/failure cases on `verifySignatures = 2` server | Secrecy or correctness of mod code |
| Server-only package | Clean client joins server; compare downloaded/installed files and confirm sentinel is absent client-side | Protection against server compromise |
| Size boundary | Controlled generated archives, exact hashes/sizes/tool and game builds, RPT/minidump, repeated runs | A universal ceiling on other builds/tools |
| Workshop packaging | Controlled private upload and clean subscription/download; retain upload log/manifest | PBO runtime compatibility |

The VitePress build only validates documentation rendering and links. It cannot validate a PBO, Enforce Script compilation, signature enforcement, Workshop delivery, or DayZ runtime behavior.

---

## Contradictions and unresolved questions for council

1. **2 GiB project observation versus universal rule:** StarDZ documentation records one failure above 2 GiB and one success below it, but the failed bytes/logs are absent. The finding is not reproducible from retained evidence and may involve memory, signing, file I/O, corruption, or another variable. Keep it as a test lead.
2. **4 GiB field inference versus total archive:** unsigned 32-bit member-size fields do not establish a single 4 GiB total-PBO field. A runtime/tool could still impose such a limit, but that requires separate evidence.
3. **Format compression versus current tool UI/CLI:** the reverse-engineered format describes compressed members, while current installed official tool help has no compression switch. The wiki should describe both facts without promising a workflow.
4. **Addon Builder output naming:** local build code handles output discovery/renaming and public build scripts organize component roots, but the opened official help does not document the output-naming rule. Documentation automation should discover/validate the produced artifact instead of assuming a name.
5. **Resource-only PBO config:** BI DayZ guidance describes `config.cpp`/`CfgPatches` as required for a PBO, yet shipped/archive layouts include resources whose precise initialization role was not fully mapped in this task. Recommend an addon identity whenever another PBO must depend on the resource; do not claim that every possible resource archive is invalid without one.
6. **`CfgMods.dependencies[]`:** official examples show script-layer names, and some samples omit the array. No source reviewed here proves every module must list all lower layers. Keep this separate from `requiredAddons[]` and avoid new absolutes.
7. **Same-prefix resolution order:** the beta artifacts have overlapping virtual paths, but no controlled runtime test established which PBO wins. That uncertainty is exactly why the build should reject collisions.
8. **Server-only signatures:** no reviewed primary source established a client-style signature requirement for PBOs loaded only through `-serverMod`. Test the target deployment before stating a rule.
9. **Workshop size:** no authoritative numeric DayZ Workshop content ceiling was found in the reviewed official pages. This audit did not perform an upload boundary test.
10. **Extracted source version:** the `D:\DayZ Projects` extraction has file timestamps/metadata but no immutable receipt tying it to a precise game build. Use its contents as official-tool extraction evidence with that limitation.

---

## Suggested integration order

1. Repair PBO-001, PBO-007, PBO-008, PBO-009, and PBO-010 because they correct misleading or contradictory wording.
2. Add PBO-002 and PBO-003 to establish the evidence boundary before anyone adds a numeric size claim.
3. Rework the multi-PBO and build sections with PBO-004 through PBO-006 and the canonical manifest/layout model.
4. Replace the unpinned observations with PBO-011 and add the Workshop separation in PBO-012.
5. Have an independent reviewer reopen primary/local sources and the exact proposed page diff, then perform the validation matrix. Only after that should changes be accepted, built, graphed, and committed.

No VitePress build, PBO build, signature verification, Workshop upload, client join, dedicated-server run, or engine boundary test was performed for this research delivery. The evidence consists of source review, tool-help execution, binary/header inventory, and static inspection of pinned implementations.
