# Approved server documentation integration

This change integrates the independently accepted twelve English server-administration pages on `wiki-reorg`, preserving the prior config, engine and tutorial commits. It corrects server reference and economy guidance whose earlier wording presented conventions or unsupported engine behavior as established facts.

---

## Source-backed changes

- Server configuration now distinguishes documented defaults from sample values, includes the vendor parameter inventory and jobsystem context, and qualifies identifier formats, FPS conventions and native parser behavior. `disableBanlist` uses the documented boolean form without asserting integer coercion.
- Economy and persistence guidance corrects territory flag refresh, globals defaults, storage location and state-loss caveats. Mission-file overrides now explain complete flags subfields for types/events, group replacement, append-only messages and retained event children. Speculative per-item probability models are removed.
- Spawn and territory sections retain the approved vanilla XML counts and field descriptions. The 22-row economy file inventory corrects mapgroupdirt purpose and directs territory readers to chapter 12.

Source basis is inherited from the accepted council, not a new factual audit: vanilla `totem.c`, `entityai.c`, `actionraiseflag.c`, constants and connection-error enums; the English stringtable; and Bohemia's DayZ-Central-Economy mission XML pinned at `9a21bb9f5fb9c62a7ce2761402196091588133e6`. The final bounded repairs were independently checked against the actual cached raw [mission-file merge rules](https://community.bistudio.com/wiki/DayZ:Central_Economy_mission_files_modding?action=raw), [custom-terrain economy setup](https://community.bistudio.com/wiki/DayZ:Central_Economy_setup_for_custom_terrains?action=raw), and [server configuration](https://community.bistudio.com/wiki/DayZ:Server_Configuration?action=raw). Exact cache and page hashes are in council-server-ACCEPTANCE.json.

---

## Approval and exact-byte integration

CS13-1 through CS13-4 are approved, with eight resolved third-revision findings and all 21 historical dispositions preserved. All twelve source raw/LF hashes passed before copying; main server pages matched predecessor `9c3f2b0d6406dcdccf5f6f7487a2c18391c08fe6` and the council baseline. Existing destination pages and selected report files were backed up externally before copying; the receipt records the backup directory. Five selected third/fourth-revision evidence files were copied locally and remain unstaged historical evidence.

The only deviations from approved page bytes are 12 newly introduced link fragments in six pages, each with one unambiguous heading ID read from the installed VitePress renderer. `server-integration-anchor-corrections.json` records exact replacements and before/after raw/LF hashes. Reversing those replacements restores every approved raw hash; factual prose is unchanged. In particular, the newly added territory pointer uses `#cfgenvironment-xml-and-animal-territories`, the renderer's actual target; the acceptance report's earlier heading-existence check did not validate that slug.

---

## Checks and limits

The server scope has zero missing file links. Existing sidebar validation passes all 1,236 targets. Strict anchor validation remains nonzero: 42 failures before integration, 51 after copying, and 39 after fixing the 12 introduced references. The 39 remaining failures are inherited, including a previously broken performance TOC link whose filename spelling changed; no new broken reference remains. No general anchor repair was performed.

The current delivery inventory accounts for 105 integrated English pages: 93 prior paths rehashed against the latest domain integration records (including the separately committed config-anchor correction), plus 12 server pages. This is delivery coverage, not project completion. Global graph refresh, final integrated-site build, and global navigation/LLM finalization remain pending. No full build, runtime/game test, translation, dependency, workflow, child-workspace, push or unrelated edits are included.

The staged scope is explicit: twelve server pages, this report, the two existing server acceptance records, the mechanical-anchor evidence, and current-delivery-inventory.json. The untracked user workflow `.claude/workflows/wiki-sync-translations.js` is preserved. Post-commit server-integration-commit.json and server-integration-commit-REPORT.md record the actual SHA, normalization checks, backups and final scoped status; these local receipts are written after the commit and are not in its tree.
