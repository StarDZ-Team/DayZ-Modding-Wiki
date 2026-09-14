# Corrected Willy reference assessment

Date: 2026-09-13 (council trial completed 2026-09-14 UTC). This report supersedes the original Markdown/JSON assessment for conclusions. It records only the independent council's pinned offline evidence; no MCP dependency install, MCP/game launch, PBO packing, EN edit, or commit occurred.

## Decision

Approve only a limited, revision-pinned offline evaluation of `dayz-script-validator`; do not treat its findings as DayZ runtime verdicts. Do not install, register, or adopt MCP in the normal environment from this assessment. A later MCP smoke may be separately coordinator-dispatched under the user's standing isolated-test authorization, using the council's disposable no-registration plan; that is not approval for environment adoption or host registration.

The repositories are third-party evidence at exact revisions: `dayz-mcp` `ffa47e7ca8c82f4785279e919cb9d40053bddf8c` (tree `4d12f2d59eb1ab382aa1feb08123b84e3e2de34b`) and `DayZ-Modding-Knowledge-Pack` `9727ae83e65ac26a1cd386c64821b00159f8f933` (tree `e46b7fa0683f4567794cd49466d14de1183e617a`). The local extraction is a set of hashable snapshots, not wholesale `1.29.0.163709` evidence: `doublecheck/REPORT.md:25` scopes `1.29.163709` / Scripts Rev. `125372` to pinned Script Diff commit `86974a0…0a1`, while `1.29.0.163709` is the current executable context; adjacent `scripts.txt` records raw `version=124588` (WC-002). Static declaration agreement for selected calls remains static only (WC-003).

## Required corrections and evidence

- **WC-004:** Manifests declare `mcp==1.27.2`, `Pillow==12.2.0`, and `psutil==7.2.2`; they are not “installed dependencies.” Evidence: `dayz-mcp/tools/pyproject.toml`, `requirements-mcp.txt`, and `dependency-lock.json` hashes `337F2D85…17F`, `F434BF27…B98`, `F1C682DA…6BA`; no install or resolution receipt exists.
- **WC-006:** The two layout FAILs are detector false positives for this guarded optional probe: `$profile:mcp_hot.layout` is a runtime filesystem candidate, and `EnsureHost()` checks `FileExist` before optional `CreateWidgets`, with a packed fallback. The rules lack filesystem-namespace, use-site, and guard/control-flow analysis. Evidence: `MCPDialogController.c` hash `FB527DB8…7941`; detector hashes `D5A53E20…EDE7FA` and `D479D04F…BBD83A0`.
- **WC-007:** Five exact-`GetType()` warnings are semantic-review candidates. Exact caller-supplied type contracts may be intentional; do not prescribe `IsKindOf` without per-site API review.
- **WC-011:** `dayz_knowledge_find`, `show`, and `status` are read-only. `dayz_knowledge_prepare` writes/publishes an index; it is not read-only (`knowledge.py` hash `087146B0…3EA3`).
- **WC-008/WC-009:** Vanilla-control independently **FAIL** means tree drift, not compile/runtime failure: baseline digest `bdbc7d5a…6706`, run `94fb3e56…c336`, warning 254→263; receipt `TEMP/willy-reference-council/vanilla-control.json` hash `B11ECB04…43663`. The multi-PBO candidate scan independently **PASS** for eight files only; it has no dependency/graph, packing, signing, load-order, or runtime proof; receipt hash `473734B6…F0F4`. The 157 validator unit tests are offline fixture/unit coverage, receipt hash `E78B871E…B5960`.
- **WC-012:** Retain no-adoption. Any future isolated MCP smoke must use disposable paths, no registration/installer/skill sync, and before/after external-state evidence, as a separate coordinator dispatch; no new permission gate is implied.

## Scope and provenance

The retained original files remain byte-for-byte historical records (original Markdown SHA-256 `E3FE5DA8…FE7`; JSON `4E5BF88A…523`). Council report and machine-readable dispositions are `willy-reference-council.md/json`; retained Pack self-check hash is `8574E2BE…0E14`. No PBO was packed and no DayZ, DayZDiag, or MCP process ran. Exact source paths, hashes, council IDs, and trial receipts are machine-readable in the corrected JSON and council JSON.
