# PBO Boundary Controller and Validator A Implementation

**Status:** implementation delivered for independent static review. Python validator B remains an external independently authored dependency; no DayZ tool, PBO packer, signer, Workbench, game, server, client, or multi-GiB boundary run was launched.

**Implementation base:** Git `d795fca51eca92781a4dbdfc89d753790569fb4d` on 2026-09-14, PowerShell `7.6.0`, .NET `10.0.5`, Windows `10.0.26200.0`. This worker was assigned Sol/high and did not create sub-workers.

## Delivered behavior

The new `examples/en/pbo-boundary/` fixture contains the exact eight-case matrix, a neutral A/B validator contract, deterministic bounded generator, PowerShell/.NET validator A, fixed standalone Mission probe, external runtime evaluator, contained controller, static adversarial tests, and real command documentation.

The controller's default action is preparation only. Its state counts one fixed probe build separately from eight boundary packaging attempts and seven eligible runtime launches. It refuses a missing explicit Python validator, repeats, a large case before the complete small-control gate, a changed scoped tool/config/DayZ hash, unsafe physical paths, insufficient resources, non-exact inventories, non-agreeing validators, non-exact BankRev/signature results, or a halted wave awaiting failure/crash classification.

External processes are created suspended, attached to a kill-on-close Windows Job, and then resumed. The helper records exact executable/argv, root and descendant PID/parent/creation identity, resource samples, console hashes/times, and pre-termination/post-cleanup identity checks. It scans owned allocated bytes through `GetCompressedFileSizeW`, rejects reparse/sparse/compressed/multi-link fixture sources, applies the 64/48/40 GiB disk, 12/8 GiB memory, 16 GiB tree-private, and 40 GiB owned-allocation gates, and projects three possible Builder copies in addition to currently owned bytes.

Validator A accepts the final `pbo-boundary-validator-v1` contract. It parses a single first `Vers` extension header, strict UTF-8 bounded strings/properties, exact all-zero header terminator, exact ordinal member inventory/order, zero reserved fields, stored method 0, control-derived `OriginalSize`, checked `UInt64` contiguous ranges, fixed-buffer source/member SHA-256, exact EOF, and `00 || SHA-1(all pre-footer bytes)`. Boundary inventories require exactly one final sentinel; probe/raw-control inventories require zero and report `T=0`, `sentinelEnd=null`. Invalid archives cannot pass from process exit alone.

The fixed Enforce Script source opens all seven literal slash paths with `OpenFile(..., FileMode.READ)`, performs one bounded `ReadFile(..., 4096)` for every open, closes each handle, and prints raw opened/read/count markers without a self-hash or success claim. The evaluator requires two exact copies of one execution block, exactly one selected open, exact raw bytes/count/nonce, fresh log creation/write times, and unchanged external seed/PBO/parser receipt identities.

## Final static verification

Command:

```powershell
pwsh -NoProfile -File .\examples\en\pbo-boundary\scripts\test-static.ps1
```

Result: exit `0`, 26/26 passed. Durable receipt: `TEMP/pbo-boundary-implementation/test-73aa086a/static-tests.json`, SHA-256 `5BA1DB06662F392369FF2A6737350A283E323950429423FB2939635AF4E43D00`.

The tests covered valid/tiny parsing; malformed, unterminated, invalid-UTF-8 and duplicate-property headers; bad footer; wrong order; multiple/zero sentinel semantics; raw-control zero/multiple config semantics; an absent required exact prefix; wrapped `UInt32` range; wrong uncompressed convention; deterministic 1 MiB-plus-remainder generation; the retained 441-byte PBO (`H=151`, `A=441`, expected prefix/hash); hard-link/reparse/report-alias rejection; a normal contained process; a captured two-process timeout tree with identity checks and complete cleanup; exact runtime evaluation; wrong open count; an error marker; wrong context; and a stale validator receipt. A fresh parser pass also reported zero syntax errors in all six `.ps1`/`.psm1` files.

Earlier small development runs exposed and were repaired: a C# interop type mismatch, exception-type/nullable handling, the tiny PBO writer's byte-array overload, report-alias exit semantics, atomic replacement compatibility, and a transient console-log hash race. No failed iteration ran DayZ tooling or created a large file.

## Reopened evidence

- Complete repaired plan Markdown/JSON and closeout, plus original independent council C01-C17.
- Retained official-tool control `TEMP/multi-pbo-confirmation/.../PBOExample_Data.pbo`, SHA-256 `1CE4ADB9D28C778E083CA506E0042217CE6A68FF2EC7FC085E2E19596D619071`; validator A independently reproduced `H=151`, `A=441`, and the exact footer/hash result.
- `D:/DayZ Projects/scripts/1_core/proto/ensystem.c`, SHA-256 `8BE625999A04DF22813052E93FE658C24C82C97B257EBEF86B106279A95DB188`, for `FileMode`, `OpenFile`, `ReadFile`, and `CloseFile` declarations.
- Existing `examples/en/multi-pbo/build.ps1` and retained `TEMP/multi-pbo-confirmation/run-case.ps1` plus the retained working Mission probe config/source, used only as fallible prior recipes.
- Installed Experimental Tools manifest `appmanifest_2909700.acf`, SHA-256 `CC36D68C6020C38E60BC928DAE3B006FD6F3E8700EB9ED846D0C58539AC80160`, which states build `23909709`.
- Installed Addon Builder executable/config, `logger.xml`, `PboUtils/exclude.lst`, FileBank/BankRev/sign/check binaries, and both `1.0.240.639` per-user configs were reopened and hash-bound. Embedded help again showed `-include` as direct-copy patterns and `-filebank` as an explicit executable path; `-include` is not used as a whitelist. The executable config selects `logger.xml` and a default FileBank; the shared logger and differing user settings remain explicit provenance rather than proof of which user config is effective.

## File hashes

| File | SHA-256 |
|---|---|
| `README.md` | `6F7F5F994C755B8EFB7A7EBB645A54FE32C9DE6D5E6CFC72D0BF2DBCB269E2EB` |
| `cases.json` | `76DB65C51ADA5A608A53739BFB4A8E60EB2A518404AD75E7652172622FBE7253` |
| `validator-contract.json` | `B49448E24F19378EBCF5E8F54B9908E156139D161D7923A8A21676FEB1928C6B` |
| `probe-source/config.cpp` | `759FC3E56EECC0A656493B0CC08DE391EE0347398CE013D6070316A698EC7350` |
| `probe-source/mod.cpp` | `521E0EA921896A225F11F2FF794F65E663147412280C20521CA7966A96303F26` |
| `probe-source/scripts/5_Mission/PBOBoundaryProbe.c` | `75E7BDD80FA7617D6CF33EB5BA0EE0C3B953E0E643C7CEE839C42B2F3BD0243D` |
| `scripts/PboBoundary.Common.psm1` | `D020F09F77EFE202E027FC7D15C5129A9850B33CAE11F2EC5769D6158B295A4F` |
| `scripts/controller.ps1` | `C4D247483473369B1160E65DCC499DFC1DF4F17E944F63C46D8EDF68B646F2AE` |
| `scripts/evaluate-runtime.ps1` | `46728FCF73EC2B89BF09024D6435D96C8D75DDA61F382FECAF75A7EAED8A35BC` |
| `scripts/generate-fixture.ps1` | `558A1F35F2F737256C4AB3B1DBDC01FC184CD2CC66644B649C3CF7C247820014` |
| `scripts/test-static.ps1` | `11F04F118187EBA20A992AFBA2D98142B36EBCF816682EC160658C4CE28BF943` |
| `scripts/validate-pbo.ps1` | `2DA69FE24F3731B3D3EBFDC863B8CDE8388C5A64BEBC8EAD11659CE5DDBAA0CA` |

These hashes preceded final audit-report creation and must be regenerated after any reviewer repair.

## Pending and unresolved

Python validator B was not inspected or integrated by this worker. The complete harness cannot be approved, committed, or launched until B's independent delivery is integrated, contract-tested, exact-agreement behavior is reviewed, and the final combined diff is independently accepted.

No pack, BankRev, signing, signature-check, DayZ runtime, client, server, Workbench, or large-file validation occurred. Therefore all eight actual boundary outcomes remain unknown. Compressed `OriginalSize`/`DataSize`, decompression allocation, mixed compression, native member/total/archive-position/footer limits, client enforcement, Workshop/distribution, other filesystems/builds, and effective per-user Addon Builder config selection remain unresolved.
