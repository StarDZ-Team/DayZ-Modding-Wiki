# Isolated Four-Component Multi-PBO Fixture

This is a documentation fixture, not a production-ready or fully tested DayZ mod. It demonstrates a separate shared package (`@PBOExample`) and server package (`@PBOExampleServer`), four physical archives, distinct prefixes, and four `CfgPatches` identities.

Run it from this directory with the installed DayZ Experimental Tools root passed explicitly:

```powershell
.\build.ps1 -ToolRoot 'D:\SteamLibrary\steamapps\common\DayZ Experimental Tools' -WorkRoot 'D:\StarDZ\docs\wiki\TEMP\pbo-author-revision-run'
```

The script creates a fresh timestamped run directory beneath `WorkRoot`; it rejects a `WorkRoot` inside this versioned fixture tree. Each component has its own temporary and build-output directory, Addon Builder receives the explicit `-toolsDirectory` argument, and the script rejects non-zero exits, logged `FATAL`/`ERROR`, missing or multiple PBO outputs, missing final names, missing prefixes/member tables, and normalized case-insensitive path collisions.

The four source components are `Core`, `Scripts`, `Data`, and `Server`. `Core`, `Scripts`, and `Data` are distributed at folder level in `@PBOExample`; `Server` is placed in a separate `@PBOExampleServer` folder intended for `-serverMod`, rather than implying per-PBO server-only routing inside the shared folder.

The collision rule is a conservative fixture release policy, not an engine law: duplicate normalized virtual paths fail by default. All components are built, finally named, and `BankRev`-inspected before the global collision scan; only then does the second phase hash and sign the final PBOs. `BankRev -logFull` is read as complete trimmed member lines, preserving spaces and requiring the exact normalized manifest-prefix boundary.

`DSCheckSignatures` is interpreted from stdout, not exit code alone: every nonblank line must be an exact `Signature <expected .bisign> is OK` result, with a one-to-one match for the package's manifest signatures. Missing keys, missing signatures, wrong/invalid lines, duplicates, and any other output fail the run; this static check still is not evidence that a neighboring PBO matches its `.bisign` after tampering or rebuilding.

Verified build level: the official tools successfully packed, BankRev-inspected, collision-scanned before signing, final-byte-signed, and exhaustively stdout-checked all four fixture PBOs on 2026-09-13. The checked-in fixture then ran in one bounded headless DayZDiag `1.29.0.163709` server case: its script class and server component resolved, and it read the Data sentinel (`81` bytes). The harness stopped that server for cleanup; this is not a natural clean shutdown, and the runtime case does not run automatically when you use this fixture.

Still unverified: client join, folder-level `-serverMod` distribution, dependency-control variations beyond this fixed fixture, `verifySignatures=2` and serverMod-only signature enforcement, numeric size limits, Workshop service behavior, and behavior on other game or tool versions.
