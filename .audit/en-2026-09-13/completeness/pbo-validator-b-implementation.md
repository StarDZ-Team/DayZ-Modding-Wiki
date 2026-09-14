# PBO Validator B Implementation Record

**Status:** independently authored Python validator B and its pure tests are complete for council/integration review. This record does not compare validator B with validator A and does not report a packer, signer, game, server, or boundary-limit result.

## Delivered files

- `examples/en/pbo-boundary/scripts/validate_pbo.py` — SHA-256 `662B98FF32CB562A95032F21AC0A60E44B64A6B06016DA4BC2D6C8FA7700F1D3`
- `examples/en/pbo-boundary/scripts/test_validate_pbo.py` — SHA-256 `02561D5852973D9146CB2549C842416AC8F4826DD453B5E4C4423C01A178C178`
- `TEMP/pbo-validator-b/native-441-inventory.json` — SHA-256 `FD693188BDAC9CB30478D8F01ECCF3812BEE4E32CBC52937AA1DEDBA74ED2CF2`
- `TEMP/pbo-validator-b/native-441-report.json` — SHA-256 `2BF60E69CB5866383563DE9F5ED22C9BE47B4FD3A2EE05559BE829437387AD2F`
- `TEMP/pbo-validator-b/sources/` — small exact copies of the pinned third-party source files listed below.

The implementation uses only the Python standard library. It parses bounded strict-UTF-8 NUL strings and `<5I` little-endian fields, verifies the exact inventory and profile rules, computes checked UInt64 ranges, streams archive/source/member hashes with a fixed 1 MiB maximum read, verifies the exact `00 || SHA-1(pre-footer)` footer and EOF, emits deterministic JSON, and atomically replaces a safe report destination. Normal mode verifies every physical source's declared length/SHA-256 before comparing it to its member; only the contract's size-bounded raw-small mode omits source equality.

## Independent authorship boundary

I did not open or read validator A, its tests, or its implementation reports before or during this work. I used the neutral contract, approved repaired plan/closeout, the coordinator-authorized source-ledger slice, the retained 441-byte control, and the pinned raw third-party sources only. The coordinator resolved two ambiguities through the neutral contract process (exact `prefix` behavior and raw-control config/totals behavior); I implemented the resulting final contract bytes without borrowing validator A behavior.

Runtime: Codex worker; the worker preamble did not expose a more specific model identifier. Repository HEAD observed during final verification: `d795fca51eca92781a4dbdfc89d753790569fb4d`.

## Contract and approved-plan provenance

| File | SHA-256 |
|---|---|
| `examples/en/pbo-boundary/validator-contract.json` (final) | `B49448E24F19378EBCF5E8F54B9908E156139D161D7923A8A21676FEB1928C6B` |
| `.audit/en-2026-09-13/completeness/pbo-boundary-plan-repaired.md` | `6BB0DE45770489FDF0A7801068C59C27BB29ABE78B2A25FB441E9F3A34343D79` |
| `.audit/en-2026-09-13/completeness/pbo-boundary-plan-repaired.json` | `A83E1054EB054221CA0BFD47D45FB00791F53BBF79EA8BA1964141E90A38EA20` |
| `.audit/en-2026-09-13/completeness/pbo-boundary-plan-closeout.json` | `84A1E41FF643D4F62E5274D60597B6448FD002252325EFBD20AFA8EACF07CB5C` |

The coordinator explicitly authorized reading only lines 463–504 of the original plan's source ledger to recover the raw pinned source locations and hashes; no other original-plan content was used for implementation semantics.

## Pinned source examination

All third-party sources were accessed on 2026-09-14. Their code describes Arma-family community implementations and is not native DayZ proof.

| Repository and commit | File, hash, and actual symbols/lines examined | Relevant observation |
|---|---|---|
| `KoffeinFlummi/armake2` `3cc3362101900ff41504db3e780dd1625634cf94` | `src/pbo.rs`, SHA-256 `BEC43AC4560626FE4B154922938D0A2BDEDB0561D68118AE822AB9C030387549`; `PBOHeader`, `PBOHeader::read/write`, `PBO::read/write`, lines 18–25, 52–70, 97–142, 221–268 | Five UInt32 fields follow a C string; member data is sequential; its reader allocates `data_size`, and its writer casts length to UInt32, so those allocation/cast choices were not copied. |
| `BrettMayson/HEMTT` `bf2168ce03d5bb8bd3849090e9b2996402624b1c` | `libs/pbo/src/model/header.rs`, SHA-256 `D3D828D2B2881AB6CBBA5F8628B586E2212119CB237E808145FE7C9020176B66`, `Header`, `ReadPbo::read_pbo`, `WritePbo::write_pbo`, lines 9–118 | Confirms C-string plus five little-endian UInt32 fields. |
| same | `libs/pbo/src/file.rs`, SHA-256 `77E5D829442A45F59B3E5A657902A09B1AABD16CF178114FAB30F76337FF1E2F`, `File::new` and `Read for File`, lines 9–57 | Shows field-sized allocation for compressed data, which this stored-only validator rejects before payload reading. |
| same | `libs/pbo/src/read.rs`, SHA-256 `9A8C1FA3382D45ADC4E220B0097B740A5A4C01437E3AB68FF0657A340221DF53`, `ReadablePbo::from/file/file_raw/file_offset`, lines 18–162 | Uses UInt64 cumulative blob offsets, sequential sizes, one marker byte/checksum, and exact trailing-data rejection. |
| same | `libs/pbo/src/write.rs`, SHA-256 `CBCB0355715DCC3330D7AA343F30478247447FF14D683F2AF7A4D20557B945F2`, `WritablePbo::add_file/write`, lines 33–46 and 132–200 | Rejects individual files above UInt32, then writes headers, sequential payloads, zero marker, and SHA-1; its whole-member buffer was not copied. |
| `KoffeinFlummi/armake` `e4940fae0d28c4dd07d9d2c591f8e056545fee3f` | `src/build.c`, SHA-256 `C68E3D02B59F62DBC18430BABF40C0122120A7763A3C551342410712ABB39012`, `write_header_to_pbo` and `write_data_to_pbo`, lines 85–180 | Assigns `ftell` into UInt32 header fields and a signed `int` data loop, demonstrating implementation-specific risk only. |
| same | `src/unpack.c`, SHA-256 `71D41F2693F1FF564768D816966D10FA3F7997EFF22C887F4F12DDC0F05EE505`, `cmd_inspect` and `cmd_unpack`, lines 59–160 and 213–303 | Parses property strings and five-field member records using bounded fixed arrays and signed/`long` seek positions; not adopted as a safety model. |

## Verification results

Python was `3.14.4`.

1. `python examples\en\pbo-boundary\scripts\test_validate_pbo.py` — exit `0`; 19 tests passed in 1.087 seconds. Tests cover a generated normal-mode boundary fixture; the retained native 441-byte raw-control; exact/missing/extra/duplicate/wrong-order members and properties; profile and prefix rules; strict UTF-8 and ordinal matching; Vers/member reserved fields; compression and OriginalSize conventions; truncation, UInt32 maximum declarations, checked UInt64 overflow and canonical decimal parsing; member/source hash mismatches; sentinel offset/final-order and no-sentinel probe/raw totals; footer marker/SHA-1/trailing data; JSON/schema/source errors; CLI exit/report behavior; archive/source report aliases; raw-small size guarding; deterministic atomic replacement; and bounded read sizes. Generated archives are explicitly synthetic parser fixtures, not native tool output.
2. `python -m py_compile examples\en\pbo-boundary\scripts\validate_pbo.py examples\en\pbo-boundary\scripts\test_validate_pbo.py` — exit `0`.
3. `git diff --check -- examples/en/pbo-boundary/scripts/validate_pbo.py examples/en/pbo-boundary/scripts/test_validate_pbo.py` — exit `0`.
4. `python D:\StarDZ\docs\wiki\examples\en\pbo-boundary\scripts\validate_pbo.py --archive-path D:\StarDZ\docs\wiki\TEMP\multi-pbo-confirmation\build\pboexample-20260914-002734-8140c691\release\@PBOExample\Addons\PBOExample_Data.pbo --expected-inventory-path D:\StarDZ\docs\wiki\TEMP\pbo-validator-b\native-441-inventory.json --raw-small-fixture --report-path D:\StarDZ\docs\wiki\TEMP\pbo-validator-b\native-441-report.json` — exit `0`, `valid_exact`. Observed archive SHA-256 `1CE4ADB9D28C778E083CA506E0042217CE6A68FF2EC7FC085E2E19596D619071`, length `441`, `H=151`, member DataSizes `188,81`, `S=339`, `dataEnd=420`, null sentinel end, and matching footer SHA-1 `B451A3F09D692D6CD01FD70619D69F8D942B7115`.

The native-artifact check validates parser behavior against the retained exact bytes described by the approved closeout. It is not a new packing run, game test, provenance audit, or size-limit result. A VitePress build was not run because this delivery changes isolated Python/audit artifacts rather than wiki navigation or rendered content.

## Remaining integration limits

- Validator A/B agreement has not been evaluated; the coordinator's separate council must reopen both final implementations and compare their projections and failure behavior.
- No controller/harness integration, official packer, BankRev, signer, signature verification, DayZ runtime, server/client, or large boundary case was run.
- Parser tests establish only validator behavior. They do not establish a universal/native PBO, member, cumulative offset, tool, Workshop, distribution, allocation, or runtime limit.
- The retained native control ran only through the explicitly bounded raw-small path, where source equality is intentionally null. Boundary acceptance still requires normal-mode source equality and every separate gate in the approved plan.
