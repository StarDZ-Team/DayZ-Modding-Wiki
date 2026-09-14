# Critical Council Implementation Report

## Scope and baseline

- Baseline commit: `9dc36064459f3184404bdba4db9d95b843b6fcaa`.
- The named `critical-implementation.md` and `.json` inputs were not present; this delivery follows the exact replacement blocks in `critical-council.md` and its current JSON record.
- No locale other than English and no `.vitepress/config.mts` file changed. No commit was created.

## Finding mapping

| Finding | Changed surfaces | Approved correction applied | Deliberately still open |
|---|---|---|---|
| OPS-C01 | `en/09-server-admin/09-access-control.md` | Separates `passwordAdmin` from BattlEye `RConPassword`; retains the disposable-server/login/log caveat. | Distinct-canary login tests and fresh server/admin/BattlEye/RCon log inspection. |
| OPS-C02 | `en/09-server-admin/09-access-control.md` | Replaces the asserted vanilla panel inventory with the retail player-list, Diag, RCon, and mod-tool boundary. | Retail dedicated-server/client capture without admin mods. |
| TUT-C01 | `README.md`, `en/README.md`, `en/index.md`, `en/glossary.md`, `en/08-tutorials/08-hud-overlay.md`, `en/08-tutorials/12-trading-system.md` | Reframes the chapter and both diagrams as server validation followed by refusal before mutation; labels provided code and EN navigation consistently. | Durable transaction state machine and the two-client injected-failure fixture. |
| TUT-C02 | `README.md`, `en/glossary.md`, `en/08-tutorials/05-mod-template.md`, `en/08-tutorials/09-professional-template.md` | Downgrades readiness claims, corrects the Addon Builder boundary, and adds the exact renamed-fixture checklist. | Materialization, compile/pack/sign/inspect, server/client/lifecycle/negative-path evidence. |
| LANG-C03 | `en/01-enforce-script/09-casting-reflection.md` | Changes only the TOC label to Config-Based Type Checking; the heading and anchor remain unchanged. | None beyond static anchor verification, which passed. |
| RPC-C02 | `en/07-patterns/03-rpc-patterns.md` | Replaces both published-ceiling claims with build- and delivery-mode-scoped measurement language. | Dedicated-server two-client payload matrix across directions, delivery modes, shapes, and sizes. |

## Exact file hashes

Git blob IDs are `baseline -> worktree`.

| File | Baseline | Final |
|---|---|---|
| `README.md` | `c8c7ff24af4a34af959e0545fc2059d3e77e9ba5` | `cd7fd1e9d9e6b895a023f08be6d9b299a8379752` |
| `en/01-enforce-script/09-casting-reflection.md` | `9dd67378efd9f22a7a95a6c46fa327dfa9645eae` | `037e600e7012bb75c0953ba89d81abc4fec4a8f7` |
| `en/07-patterns/03-rpc-patterns.md` | `6623e7a7312156201cf54a3fba31ce96e04f1041` | `20331ed0c688953ba257c468f1f4d78db1b1e526` |
| `en/08-tutorials/05-mod-template.md` | `d97c8606e7c8ccf483031c852308c5b1b308c4a6` | `732a197a79a6f323ccee23b056779f22dcea4159` |
| `en/08-tutorials/08-hud-overlay.md` | `364e9312a2669bbe8d6de1c912805ccb9c275db1` | `dd98fdd6e7c726c87fcb1fbc44f8f5c4c11ab93a` |
| `en/08-tutorials/09-professional-template.md` | `0cf898679de1a2b325625c7654acea3f4d5e2953` | `47a16d1cacf37357eeb0b1b8c2923e29e43ce6f0` |
| `en/08-tutorials/12-trading-system.md` | `882c7819861632bc260909c2f750463fc04147da` | `14a58a214db1f36d4db0830882db82fbdd693a51` |
| `en/09-server-admin/09-access-control.md` | `0c352620e1564125c869ed96e74e57f62c96b7ff` | `5666591e927541b325fd1216c6b12355863c9259` |
| `en/README.md` | `e9a865796d4e075cf3a61d2c91df25c64d4e0fe1` | `38a5a956538f225ece6452322ebe9956f6418c94` |
| `en/glossary.md` | `9e52ed00bc73448c69efcb86fb98c58c694a2bfa` | `38de9cc78089a86b7bdc9b161d82e3a50e44684f` |
| `en/index.md` | `cea0876799350b55c6b3971e6685b23ce9307988` | `81b7ddcf32f3aa1c19adba12d48c42da18d16142` |

## Validation actually run

1. `node scripts/check-links.mjs --anchors --strict` — exit 0: 1,265 Markdown files checked with zero dead file links; 105 EN files and 1,278 fragments checked with zero dead anchors. The checker renders headings with the installed VitePress `createMarkdownRenderer`, so this also rendered the changed Markdown, code fences, and Mermaid fence.
2. `git diff --check` — exit 0.

No full site build, DayZ runtime test, compiler, packer, signer, server, or client was run.
