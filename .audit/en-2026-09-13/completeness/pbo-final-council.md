# Final Council: Revised PBO Research and Fixture

**Review date:** 2026-09-13  
**Repository state:** `wiki-reorg` at `9dc36064459f3184404bdba4db9d95b843b6fcaa`  
**Role and scope:** independent final council; no English page, fixture, or author artifact was edited and no game was launched.  
**Decision:** **reject the exact revised research/evidence-and-fixture set for a scoped commit pending the repairs below.** The research conclusions are substantively supported, and the fixture builds successfully, but the exact evidence ledger and build script are not yet final-council clean. This is not a full-wiki disposition.

---

## Exact artifact dispositions

| Artifact | SHA-256 | Disposition |
|---|---|---|
| `pbo-research.md` | `03FE483067A9259D6C0601A2F6FF9C9C7B6601201FAB6982343A8A15582D7949` | Content accepted; do not commit as the final bundle until its evidence ledger is repaired. |
| `pbo-evidence.json` | `081584169BBC4D8FC2893C9C116B2570DC88A23829DC5AB60ACCE259385F2BF2` | Rejected: the corrected `01-five-layers.md` read is still absent as a source object. |
| `examples/en/multi-pbo/build.ps1` | `123E454ED89A87167262228D110DA5E81A71406CCBC445ABC8DED34769FCFBE8` | Rejected: DSCheck acceptance is not exhaustive, and global collision validation happens after signing. |
| `examples/en/multi-pbo/manifest.json` | `63D5E5E9468AF98B37B30AB71C3CCEA69D45694E266377025F68E6953F088582` | Accepted as fixture data, subject to the repaired runner. |
| `examples/en/multi-pbo/README.md` | `84200850C3323C51218DD1163B293109AB99313E5EEDE7C24A3BC34731AFC7D0` | Needs the final rerun receipt and any runner-behavior wording synchronized after repair. |
| `pbo-revision.md` / `pbo-revision.json` | `A443203C0321F5FD313ED9FF67AB40D7BD7CC51DE14802AC60933A65E7405DD7` / `9301E870FFE255D71447C2812A309664145C1024CA4CA7EDA3AC5934288ACB78` | Historical author receipt verified; supersede after repair rather than treating it as final approval. |

All twelve fixture source/config/manifest/readme/script hashes recorded in `pbo-revision.json` matched the current files. The retained author run receipt hash `AF2366C97CC04686FB77866592318989FF0E2249F563E239108A53743B368C4C` and all four recorded PBO and `.bisign` hashes also matched the retained bytes.

---

## Required repairs

1. Add a `current_wiki` source object for `en/02-mod-structure/01-five-layers.md` to `pbo-evidence.json`, with SHA-256 `1C8571C015339DD7508D92C519A0F6A563B3790D5120ED776832EFBA345C8413` and the actual reviewed scope. The corrected research names the file, but the evidence index it points to does not record it.
2. Make DSCheck validation exhaustive per package. Reject `Key not found`, `No signature found`, non-OK/invalid signature lines, and any unexpected output; parse the full set of `Signature <expected-bisign> is OK` lines and require a one-to-one match with every manifest PBO/signature. The current `if ($checkText -notmatch 'Signature .* is OK')` succeeds when only one of several signatures is OK.
3. Complete building, final naming, BankRev inspection, and normalized collision collection for every component before hashing or signing any PBO. Only after the global collision scan passes should a second phase hash and sign each final PBO. The current duplicate-path test created four signatures before rejecting the release, contrary to the council workflow and the order stated in the revision narrative.
4. Parse `BankRev -logFull` as complete trimmed lines rather than matching `[^\r\n\t ]+`-style whitespace-delimited tokens. Preserve member names containing spaces, validate an exact normalized prefix boundary, and then apply case-insensitive path normalization.
5. As a repository-hygiene guard, reject a `WorkRoot` located inside `examples/en/multi-pbo` (or another versioned fixture path). No key, PBO, signature, receipt, or log is currently present in the fixture tree, but the runner presently permits this unsafe destination.
6. Rerun success, partial/missing/wrong signature, duplicate-path, bad-tool-path, and stale-parent-output cases; regenerate `pbo-revision.md/json` and every changed source/code hash; then return the exact repaired files for final-diff review.

---

## Independent verification

The corrected `01-five-layers.md` path exists and its claimed hash matches. The corrected BIKI server snapshot exists, hashes to `B2D11B4CD7D973FF65FD9804406E02D4C091176F9926EE1AF1F04142FE4142F7`, and lines 180-181 support folder-level `-mod` / `-serverMod` wording. Forty-seven recorded checks matched: 26 direct file hashes, seven pinned repository HEAD/origin checks, and fourteen pinned child-file hashes. Live BIKI reopening again returned HTTP 403; the identified local snapshots were reopened, while the reverse-engineered PBO-format URL remains explicitly qualified and lacks a durable local snapshot in the ledger.

An independent run succeeded under `TEMP/pbo-final-council/success-work/pboexample-20260913-205127-ba47a884`; receipt SHA-256 is `EB8ED1F5E08236B2B744D64A1DDB10A74BF6D61737B32951CDE3CA908EC0C65B`. It produced exactly three PBOs in `@PBOExample` and one in `@PBOExampleServer`, with the manifest names and prefixes. BankRev extraction reproduced all seven source members byte-for-byte, including the four `config.cpp` files and both script files. `CfgConvert` returned zero for all four configs but created no output, so this remains only a bounded parser invocation, not compilation proof.

| Component | Prefix | Members | Independent PBO SHA-256 |
|---|---|---:|---|
| `PBOExample_Core.pbo` | `PBOExample/Core` | 1 | `496744B371AE7CF1EE3895BB0B53D54F0B9E563D53B286A12B3E2BBF5D2A471E` |
| `PBOExample_Scripts.pbo` | `PBOExample/Scripts` | 2 | `C356135E8CD5A188F1246ED38A04E09086A2E2A867370908C8BFAA3B2DF0E3D1` |
| `PBOExample_Data.pbo` | `PBOExample/Data` | 2 | `E16D865C90C37154C0299FCB0666398FD4B468107356EAACAA396E5BCF3EBA0F` |
| `PBOExample_Server.pbo` | `PBOExample/Server` | 2 | `1FF053D7344906BA8BD5AE2F75458D6418B5648E1DB4D9830F156C22068F86C6` |

Meaningful negative results were reproduced:

- Addon Builder returned `0`, emitted `[ERROR]`, and created no PBO for a nonexistent tools directory; the fixture's log matcher recognizes this output.
- DSCheck returned `0` plus `Key not found` for an empty keys directory; the fixture's positive-OK guard rejects that all-missing-key case.
- With three PBOs but only two signatures, DSCheck returned `0`, printed two `is OK` lines and `No signature found` for the third PBO; the fixture's current condition incorrectly passes.
- A duplicate Core/Data virtual path was rejected and no receipt was written, but all four PBOs had already been signed.
- A stale unrelated PBO placed in the parent `WorkRoot` was ignored and preserved while a fresh isolated run succeeded.
- DSCheck reported `is OK` for an old `.bisign` beside different rebuilt PBO bytes (`D439...20D0E` versus `4967...A471E`). This independently confirms that this installed DSCheck invocation is a narrow signature/key check, not PBO-byte binding or server-enforcement proof.

No test keys or generated PBOs, signatures, logs, or receipts were found under `examples/en/multi-pbo`.

---

## Outstanding runtime and service gates

DayZ boot and Enforce compilation, clean-client join and folder-level `-serverMod` distribution, mounted `CfgMods` path execution, missing/renamed `requiredAddons` behavior, `verifySignatures=2` valid/modified/missing/wrong/rotated-key enforcement, serverMod-only signature enforcement, controlled PBO boundary tests, and Workshop upload/download remain untested here. The existing game logs make later runtime work feasible, but that work belongs to the separate runtime owner.
