# Bounded PBO Size-Boundary Experiment Plan

**Status:** design complete; runtime, packing, signing, and BankRev results are pending.

**Designed:** 2026-09-14 on repository `99c011b4d3ded81f4b45c5f30f326de7e92075b3`.

**Owned future root:** `TEMP/pbo-boundary-plan/runtime/<run-id>/`.

**Scope:** current Windows DayZDiag `1.29.0.163709` and installed DayZ Experimental Tools build `23909709`. A result applies only to the exact archive/tool/game combination tested.

No large file was created and no packer, signer, BankRev, game, server, or client was launched while producing this plan.

---

## Decision the experiment can make

The reverse-engineered layout has unsigned 32-bit `OriginalSize` and `DataSize` fields for each member, but no total-archive-size field; the field historically called `Offset` is reserved/normally zero. That does not establish a 2 GiB or 4 GiB total-PBO ceiling.

The matrix below distinguishes:

- an implementation treating one member length as signed at `2^31`;
- a reader/tool failing when cumulative physical position crosses `2^31` or `2^32`;
- the unsigned per-member representability boundary at `2^32 - 1`;
- Addon Builder, BankRev, signer, and DayZ mount/read outcomes;
- stored size from original size and compressed from uncompressed content; and
- local format/tool/runtime evidence from filesystem or Workshop distribution, which this experiment does not test.

Interpret the 2 GiB comparison as follows:

- `sum-i31-at` succeeds but `member-i31-at` fails: evidence for a per-member signed-length implementation defect in the failing stage.
- both fail after `member-i31-minus` succeeds: evidence for a cumulative/archive-position boundary in the failing stage, not proof of a member-field ceiling.
- both succeed and read their sentinels: the historical 2,165,383,988-byte crash is not reproduced on this exact build/fixture.

Interpret the 4 GiB comparison as follows:

- `sum-u32-at` succeeds after `sum-u32-minus`: a total archive and readable member beyond byte `2^32` worked for this fixture/build; this is not an unlimited-support claim.
- `sum-u32-at` fails at one stage while its independently parsed PBO is valid: scope the limit to that stage.
- `member-u32-plus1` cannot be a valid single-member PBO in this layout. Its packaging result tests tool rejection only; never launch it in DayZ.

---

## Fixed fixture and deterministic payload recipe

Use one small probe PBO plus exactly one boundary PBO per engine run. Keep the probe separate so its `MissionServer.OnInit()` can compile even if the boundary PBO does not mount.

Each boundary source root contains, in intended payload order:

1. root `config.cpp`, defining a unique, dependency-free `CfgPatches` class;
2. one or more `payload/aa_filler_NN.txt` members; and
3. `payload/zz_sentinel_<case>.txt`.

The sentinel is ASCII without BOM or trailing newline:

```text
PBOBOUNDARY|schema=1|case=<case>|nonce=<run-id>|expected-path=PBOBoundary/<case>/payload/zz_sentinel_<case>.txt
```

Generate fillers as real, non-sparse source files. Build one canonical 1 MiB block from the concatenation of `SHA-256("PBOBOUNDARY/v1/block/" || uint64-le(counter))` for counters `0..32767`; repeat that block and write its leading remainder to reach the exact member size. This is deterministic and hashable, and it avoids a deliberately short repeating pattern within the 8 KiB LZSS window described by the format page; the parser still detects any compression. The generator must stream with a fixed buffer, hash while writing, then re-hash the closed file. Reject a source with `SparseFile` or `Compressed` attributes, a different logical length, a generation/re-read hash mismatch, or an allocation result inconsistent with a real file.

`-packonly` is expected to store these members uncompressed. For this matrix, every filler and sentinel must parse with packing method `0` and `OriginalSize == DataSize == source length`. If Addon Builder emits `Cprs` or unequal sizes, record the tool result but mark the case `not_comparable_compression_changed`; do not infer a size boundary. A compressed-member boundary study needs its own sourced current-tool recipe and is not part of these eight cases.

---

## Smallest discriminating matrix

Constants: `B31 = 2,147,483,648`, `B32 = 4,294,967,296`, and `M = 1,048,576` bytes. `H` is the parsed byte position immediately after the zero header terminator, and `C` is the stored `config.cpp` size. The parser, not a filename-order assumption, proves `sentinelOffset = H + C + sum(filler DataSize)` for the required order.

| Order | Case | Exact filler sizes (bytes) | What it isolates | Required sentinel position | Engine |
|---:|---|---:|---|---|---|
| 0 | `small-control` | `1,048,576` | Complete pack/parse/sign/mount/read control | Any valid data-block position | Yes |
| 1 | `member-i31-minus` | `2,146,435,072` (`B31-M`) | One member below signed boundary; total/sentinel below boundary | `< B31`; require `H+C < M` | Yes |
| 2 | `sum-i31-at` | `1,073,741,824` + `1,073,741,824` | Cumulative position crosses `B31` while each member is below it | `> B31` | Yes |
| 3 | `member-i31-at` | `2,147,483,648` (`B31`) | Same filler sum as case 2, but one member sets the sign bit | `> B31` | Yes |
| 4 | `sum-u32-minus` | four × `1,073,479,680` (`(B32-M)/4`) | Valid members and sentinel just below unsigned cumulative boundary | `< B32`; require `H+C < M` | Yes |
| 5 | `sum-u32-at` | four × `1,073,741,824` (`B32/4`) | Valid per-member fields with sentinel physically beyond `B32` | `> B32` | Yes |
| 6 | `member-u32-max` | `4,294,967,295` (`B32-1`) | Largest representable single stored/original size; archive itself exceeds `B32` | `> B32` | Yes, only if all validity gates pass |
| 7 | `member-u32-plus1` | `4,294,967,296` (`B32`) | Addon Builder handling of an unrepresentable single member | No valid header value exists | **No: tool-only** |

Do not add exact-byte searches, extra member counts, compression variants, client cases, or alternate packers to this wave. The one-versus-two cases have the same filler sum at `B31`; the four-member pair changes only cumulative sum by `M` while keeping every member far below `B31`.

Every case has its own tiny readable sentinel and both parsers prove its exact physical offset. The two below-boundary bracket controls intentionally prove the sentinel remains below the boundary; every case used as above-boundary evidence must independently prove the sentinel starts beyond that boundary before launch.

---

## Packaging, inspection, and signing gates

Adapt the already council-approved isolated workflow in `examples/en/multi-pbo/build.ps1` (SHA-256 `38F24D830DBCB7985ABF1ED9636493C5BDFEA1E160169379FE10E8F50BADB956`). For each case, use empty, case-specific source, Addon Builder temp, and output directories:

```powershell
& $addonBuilder $sourceRoot $buildDir `
  '-packonly' '-clear' "-temp=$componentTemp" `
  "-prefix=PBOBoundary\$case" "-toolsDirectory=$toolRoot"
```

Record the exact argv, UTC times, process exit, stdout/stderr, peak working/private bytes, free physical memory, free disk before/after, and SHA-256 of tools and inputs. Reject `FATAL`/`ERROR` text even with exit `0`. Require exactly one newly created non-empty PBO; discover its actual output name, then move it once to the final case name before hashing.

Run these independent checks before any engine launch:

1. BankRev `-properties` must show exactly the expected prefix; `-logFull` must list the exact normalized member set. Do not extract the multi-gigabyte fillers.
2. A strict PowerShell/.NET parser must read the five fields as `UInt32`, accumulate `UInt64` positions with checked addition, validate the `Vers` block, zero header terminator, every member range, exact EOF/footer position, and the Addon Builder footer established by the small control. It must stream-hash each member and directly seek/read/hash the sentinel.
3. An independently implemented Python parser must repeat the header walk and `sentinelOffset` calculation using `struct.unpack('<5I')` and Python integers, then seek to and hash the sentinel. It must not call `read(size)` for a filler.
4. Both parsers must agree on `H`, member order, `OriginalSize`, `DataSize`, physical start/end offsets, sentinel bytes/hash, data end, footer start, and archive length. Require `config.cpp` before every filler and the sentinel after every filler; otherwise the case is invalid, not a boundary result.
5. Stream-hash each archived filler range and match it to the closed source file before deleting the source. This proves Addon Builder stored the generated payload, rather than only writing the claimed header length.

Record every tool independently:

| Stage | Outcome categories |
|---|---|
| Addon Builder | `accepted_exact`, `rejected_nonzero`, `rejected_error_text`, `no_output`, `wrong_output_count`, `size_wrap_or_truncation`, `resource_abort` |
| Binary parsing | `valid_exact`, `invalid_header`, `invalid_member_range`, `unexpected_compression`, `footer_or_eof_mismatch`, `sentinel_offset_wrong`, `payload_hash_mismatch` |
| BankRev | `listed_exact`, `rejected_or_crashed`, `wrong_members_or_prefix`, `timeout` |
| DSSignFile | `signed_pbo_unchanged`, `rejected_or_crashed`, `timeout`; always compare PBO hash before/after |
| DSCheckSignatures | `one_exact_ok`, `non_ok_stdout`, `timeout`; exit `0` alone is not success |

Use one disposable authority under the owned run root. Keep the private key out of retained/public outputs. Signing and BankRev failure identify their tool boundary but do not turn a parser-valid archive into an invalid format claim. An engine launch is allowed only after both parsers prove the exact sentinel bytes and required physical position; never reinterpret invalid-entry rejection as a size limit.

If Addon Builder cannot produce a parser-valid case, stop and research its documented/current behavior before any retry. Manual PBO construction is a last-resort separate proposal: it first has to reproduce the small Addon Builder control byte structure (valid `Vers` properties, file headers, zero terminator, contiguous payloads, `0x00` plus matching 20-byte SHA-1 footer) and pass both parsers plus BankRev. A manually constructed result must be labelled non-official-tool output and cannot replace the Addon Builder result.

---

## Runtime proof

Copy, do not mutate, the known recipe `TEMP/multi-pbo-confirmation/run-case.ps1` (SHA-256 `FBAC12CD27A18E254D72CB4F6C9AC5FCF34775BF24D8A3BBD567D980040C4E55`) and its reviewed 43-file mission manifest (`1260F07AC011D4CFDA66BF0915D8475ECDD072776CCD3B2BE8A43EF4B3B7EA3E`). Preserve its controls: exactly one numeric `instanceId`, private mission containment, `steamQueryPort = game port + 1`, three free ports before launch, captured-process-only cleanup, `WaitForExit()`, and empty ports afterward.

Use 45 seconds per case, sequentially:

| Case | `instanceId` | Ports |
|---|---:|---|
| `small-control` | 790 | 26300–26302 |
| `member-i31-minus` | 791 | 26310–26312 |
| `sum-i31-at` | 792 | 26320–26322 |
| `member-i31-at` | 793 | 26330–26332 |
| `sum-u32-minus` | 794 | 26340–26342 |
| `sum-u32-at` | 795 | 26350–26352 |
| `member-u32-max` | 796 | 26360–26362 |

Build one fixed small probe PBO that checks all seven case paths but requires exactly one to open. For the mounted case it must call `ReadFile`, not only `FileExist`, and print this exact block to both RPT and script log:

```text
PBOBOUNDARY:RUNTIME:BEGIN
PBOBOUNDARY:RUNTIME:CASE=<case>
PBOBOUNDARY:RUNTIME:PATH=<full virtual path>
PBOBOUNDARY:RUNTIME:OPEN=true
PBOBOUNDARY:RUNTIME:READ_BYTES=<exact sentinel byte count>
PBOBOUNDARY:RUNTIME:SENTINEL=<exact sentinel text>
PBOBOUNDARY:RUNTIME:END
```

Success requires the complete block in both logs, exact bytes/text, and the prelaunch parser receipt proving that sentinel's physical archive start is on the required side of the boundary. Startup, PBO presence, a mount line, `FileExist`, or one partial marker is insufficient.

Runtime categories are `read_exact`, `mounted_but_read_failed`, `addon_missing_or_skipped`, `compile_failed`, `process_crash` (retain RPT/minidump), `timeout_no_marker`, and `resource_abort`. Record exact executable hash/version, launch argv, PID, instance ID, ports, RPT/script-log/console hashes, and owned cleanup. Use `verifySignatures=0`; signature enforcement and client/distribution behavior are separate experiments.

---

## Resource budget and sequential retention

Design-time observation at `2026-09-14T05:39:42.7420737Z`:

- `D:` is healthy NTFS, size `1,000,186,310,656` bytes, free `608,304,656,384` bytes (about `566.53 GiB`).
- Physical memory is `68,137,205,760` bytes (about `63.46 GiB`), with `29,921,193,984` bytes (about `27.87 GiB`) free.

The experiment owns at most `40 GiB` under its run root and requires at least `64 GiB` free on `D:` before starting. Stop before a new case if the volume would fall below `48 GiB` free, system free physical memory is below `12 GiB`, the owned root exceeds `40 GiB`, or a captured tool exceeds `16 GiB` private bytes. During a tool run, terminate only its captured process tree if free physical memory falls below `8 GiB` or free disk below `40 GiB`; record `resource_abort`.

Run one case at a time. Retain every parser-valid final PBO and compact logs/receipts (approximately `18 GiB` total for the seven expected valid archives). After source-to-archive streaming hashes match and the case receipt is atomically written and re-read, remove only that case's verified source fillers and Addon Builder temp directory; retain the deterministic generator, exact size recipe, source hashes, small config/sentinel, final PBO, `.bisign`, logs, and receipt. For the expected-unrepresentable case, retain any produced PBO as evidence; otherwise retain its tool log/receipt and delete its verified source filler. Never use a broad glob or recursive target derived from case text: resolve every deletion target, require it to be a child of the recorded run root, list it in `cleanup.json`, and check the target no longer exists.

---

## Trial ceiling and stopping conditions

- Maximum planned attempts: eight packaging attempts and seven engine launches.
- Maximum retries: two total, each an exact-byte rerun only after source research records a falsifiable cause and a distinguishing result. Absolute caps are ten packaging attempts and nine engine launches.
- If `small-control` fails any stage, stop the wave.
- If a case fails source length/hash, parser validity, sentinel placement, or resource guards, do not launch it.
- If a process crashes, preserve its PBO/logs/dump/process receipt, clean up only the captured PID, and stop later cases until the failure is classified.
- If the paired comparison already discriminates member versus cumulative behavior, do not add variants. If it does not, report unresolved; do not start a binary search in this wave.
- If repeated trials stop producing distinguishing evidence, consolidate, return to official/current-tool and public-source research, and seek independent council before any new variation.

The final receipt must preserve commands, source recipe and hashes, tool/game versions and hashes, filesystem/resource snapshots, member fields, physical offsets, full PBO hashes, stage outcomes, runtime markers, crash artifacts, cleanup, and explicit limitations. Independent council must reopen the retained PBOs and sources before any EN wording change.

---

## Source ledger and limits

Exact machine-readable entries are in `pbo-boundary-plan.json`. Key evidence:

- Prior accepted audit: `pbo-research.md` (`03FE...7949`), repaired `pbo-evidence.json` (`38E2...E1BBA`), `pbo-council.md` (`D19E...4A31`), `pbo-final-council.md` (`D971...5E02`), and `pbo-repair-council.md` (`8488...4922`). These explicitly leave the numeric matrix unresolved.
- Completed runtime recipe/council: `multi-pbo-confirmation-runtime.md` (`3DA1...B745`), its JSON (`5B3D...73C`), and `multi-pbo-confirmation-council.json` (`3B30...3BD4`). They prove the `instanceId` harness and exact `ReadFile` marker path on DayZDiag `1.29.0.163709`, not size behavior.
- Fallible local claims: `D:/StarDZ/docs/REFERENCIA_LIMITES_E_MUROS.md` (`7260...EA0`) and `GUIA_FERRAMENTAS_E_BUILD.md` (`2ECA...67D9`) report 2/4 GiB behavior, but the failing bytes/logs/version receipt were not found. `D:/StarDZ/dev.py` (`E686...C64F`) repeats signed/unsigned conclusions and implements conservative splitting; it is a lead, not engine proof.
- Extracted metadata: `D:/DayZ Projects/scripts.txt` (`E45D...F55F`) says `prefix=scripts\\`, `product=dayz`, `version=124588`; `pboapi.c` (`9C4B...A61`) exposes `GetPBOVersion` only. Neither declares a size limit, and extraction version is not equated with runtime build.
- Reverse-engineered documentation: BIKI `PBO File Format` identifies five per-member 32-bit fields, sequential data, optional footer, and its own unofficial status. Direct page fetches returned HTTP 403 during this run; indexed content was available and no current authoritative DayZ numeric ceiling was found.
- Official tool documentation: BIKI `Addon Builder` oldid `341605` documents `-packonly`, `-clear`, `-temp`, `-prefix`, `-sign`, `-include`, and tool-path options, but no numeric PBO limit. Direct fetch was HTTP 403; indexed content was accessed 2026-09-14.
- Third-party armake2 `3cc3362101900ff41504db3e780dd1625634cf94`, `src/pbo.rs` (`BEC4...9549`), uses `u32` member fields, sequential payloads, whole-member allocations, and unchecked `usize as u32` on write. It is not native proof.
- Third-party HEMTT `bf2168ce03d5bb8bd3849090e9b2996402624b1c`, `libs/pbo/src/{model/header.rs,file.rs,read.rs,write.rs}`, uses `u32` member sizes, `u64` cumulative offsets, rejects source size above `u32::MAX`, and currently buffers a member during write. It is an implementation example, not DayZ proof.
- Third-party armake `e4940fae0d28c4dd07d9d2c591f8e056545fee3f`, `src/build.c`, assigns `ftell()` to both `uint32_t` header sizes and a signed `int datasize`; `src/unpack.c` uses `long` positions plus `fseek`. It demonstrates why implementation integer types must be tested separately from the format, not how DayZ itself behaves.

Filesystem success, signer success, or a finite successful archive does not establish Workshop support, deployment compatibility, client/server distribution, all compressed layouts, another DayZ/tool build, or an unlimited maximum.
