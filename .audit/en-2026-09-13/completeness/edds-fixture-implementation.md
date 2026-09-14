# EDDS fixture implementation receipt

**Prepared:** 2026-09-14 America/Sao_Paulo  
**Result:** a concrete standalone `EDDSProbe` source tree, deterministic source PNG, private project proposal, and future-only pack verifier are present. No generated EDDS, metadata, PBO, GUID, conversion, packaging, or runtime receipt exists.

## Files and SHA-256

| Path | SHA-256 |
|---|---|
| `examples/en/edds-probe/scripts/generate_probe_png.py` | `117D1A2D40F7F460E8960E5986ED6DF47BB2209676449ED925E85F98C7831BF3` |
| `examples/en/edds-probe/scripts/verify_preparation.py` | `200A5633E1FA3EF58986DA21597AF71019E51F5484D52164DE4F9AEC83E8F21C` |
| `examples/en/edds-probe/source/EDDSProbe/GUI/imagesets/probe_ui.png` | `EDB68FB0779781BF8F672D2595897EB870792675EB576BDDDF08E4E231B7522C` |
| `examples/en/edds-probe/source/EDDSProbe/config.cpp` | `A399BA5FF8E4C10C113F4021400FA292BDE065A85C2802FF7A512860872E8CA9` |
| `examples/en/edds-probe/source/EDDSProbe/GUI/imagesets/probe_ui.imageset` | `B4D648347F441E58466923F427D2BD97DDC6D47FCBE419B3922A9EF5B5140A98` |
| `examples/en/edds-probe/source/EDDSProbe/GUI/layouts/probe_ui.layout` | `C4B5048565D985AD827C533651C85145BC04D59E84AF7609574E5E3A86F6B579` |
| `examples/en/edds-probe/source/EDDSProbe/Scripts/5_Mission/EDDSProbeMission.c` | `B1B7E775F777EC432E0918D133D0BAD184D2AB8EEF2F42CF70189C2F49D4C275` |
| `TEMP/edds-fixture-preparation/EDDSProbe.gproj` | `A5632B06E21C4E87CA56BB51DFA4BEF7997C4881FF87B36D55D8E8AB90C03598` |

## Prepared behavior and checks

- The generator produces only the original 64x32 RGBA8 fixture, with PNG filter-0 bytes and no stock image dependency.
- The independent verifier checks each decompressed pixel and PNG chunk CRC, source-tree structure, the intentionally absent pre-conversion EDDS/meta pair, and later accepts the two observed effective EDDS header/table offsets.
- `config.cpp` has the standalone `CfgPatches`/`CfgMods` registrations and the required vanilla dependency (`DZ_Scripts`) only. The mission hook has distinct `EDDSProbe/Create`, `EDDSProbe/Load`, and `EDDSProbe/SetImage` event tokens and null guards.
- The future pack recipe places all outputs below an explicit caller-owned work root and checks the PBO table with BankRev before any later client run. It aborts without Workbench-generated EDDS and metadata.

## Mount receipt

The installed `dayz.gproj` and Workbench executable hashes are recorded in `edds-workflow-repaired.md`. The installed project was not mutated; it contains prior StarDZ entries. `P:` was not present, while the private source root and PNG existed on disk; the private project maps that physical root in source-backed `FileSystemPathClass` syntax, but no GUI observation proves how Workbench will expose it.

## Remaining prerequisites

1. Independently review this exact source and private project, then observe source-root visibility in Workbench.
2. Perform one default import and record any generated EDDS/meta/identity without editing their generated contents.
3. Run the supplied structural output check, pack once with the future recipe, and retain the BankRev receipt.
4. Run the one baseline client observation; at most one correction is allowed for an objective path, prefix, package-table, or reference defect.
