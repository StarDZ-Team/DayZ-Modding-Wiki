# Critical Corrections — Independent Repair Council

> **Verdict:** Approved for the scoped commit. The four requested repairs are present, the eight previously accepted files retain their recorded identities, and every bounded validation gate passed. This does not approve the still-open functional findings or replace the required full integrated content build.

## Scope and comparison

- Content comparison baseline: `9dc36064459f3184404bdba4db9d95b843b6fcaa`.
- Current `HEAD` at final review: `381f6d18f3d2e31800ca352fadaabb04bea6b084`; the intervening approved PBO/runtime-evidence commits do not alter any of the twelve scoped file identities.
- Prior decision records: `completeness/critical-final-council.md` and `completeness/critical-final-council.json` under `.audit/en-2026-09-13/`.
- Reviewed the prior council's eleven content files plus `.vitepress/config.mts`.
- Reused the still-matching accepted evidence and file identities; did not repeat the full technical research.
- Made no content/config edits, launched no game or tool runtime, and did not run the full VitePress build.

## Repair decisions

| Repair | Decision | Evidence |
|---|---|---|
| `README.md:77` readiness description | Accepted | The link now calls Chapter 8.9 a feature-rich illustrative starter and explicitly says it is not runtime-validated. Reversing only this text reproduces the prior council's Git-normalized blob. |
| `en/08-tutorials/05-mod-template.md:57` readiness sentence | Accepted | The cross-page claim now describes the illustrative, unvalidated template. Reversing only this sentence reproduces the prior council's Git-normalized blob. |
| `en/08-tutorials/12-trading-system.md:43` Mermaid message | Accepted | The semicolon is replaced by a comma. Mermaid `11.13.0` parses the changed fence successfully. Reversing only this message reproduces the prior council's Git-normalized blob. |
| `.vitepress/config.mts:137` sidebar label | Accepted | The route is unchanged; `lang === 'en'` selects `Shop UI & Safe Refusal`, while every other locale retains `Trading System`. Live dev rendering confirmed the EN and PT outcomes. |

The eight previously accepted files are byte-identical to their recorded prior-council SHA-256 values and retain the same Git blob identities. The three repaired content files reproduce their prior-council Git blobs when only the requested replacement is reversed, confirming the commit-visible delta is exactly the requested prose/diagram repair. The config diff is one conditional label change; it does not change the route or non-English label.

## Validation

- `node scripts/check-links.mjs --anchors --strict`: exit 0; 1,265 Markdown files, zero dead file links; 105 EN files and 1,278 fragments, zero dead anchors.
- Installed `mermaid.parse()` (`mermaid` 11.13.0) on the changed fence: exit 0.
- `git diff --check 9dc36064459f3184404bdba4db9d95b843b6fcaa -- <twelve scoped files>`: exit 0.
- `npm run dev -- --host 127.0.0.1 --port 5177`, inspected through headless Chrome 152: the EN route returned the title/heading `Shop UI, Catalog RPC, and Safe Refusal` and sidebar label `Shop UI & Safe Refusal`; the PT counterpart retained its translated title/heading and sidebar label `Trading System`.
- Review runtime: Node `v24.14.0`, npm `11.17.0`.
- Full integrated `npm run build`: not run; it remains a separate required final-content gate.

## Finding status boundary

This repair review does not close the prior council's functional work. `OPS-C01`, `OPS-C02`, `TUT-C01`, `TUT-C02`, and `RPC-C02` remain unresolved at runtime/fixture level; `LANG-C03` remains accepted after static checking. Approval is limited to committing the twelve exact file states below as the critical-correction content/config scope.

## Exact approved file identities

| File | Git blob | SHA-256 of working bytes |
|---|---|---|
| `README.md` | `5b96bc9f1eb3d97d2fd16350f437b59bdded0f7e` | `4E19D18AC2D96CF6FB2E01C1D30094E110281C8A045F48C73E543A47165AFFCB` |
| `en/01-enforce-script/09-casting-reflection.md` | `037e600e7012bb75c0953ba89d81abc4fec4a8f7` | `24DB725C3D0B6B2C098B0446C2970F3CD0463E1AB871ACE688393563FD4FCE2C` |
| `en/07-patterns/03-rpc-patterns.md` | `20331ed0c688953ba257c468f1f4d78db1b1e526` | `7185F4FE065041BFE705A78641C6967771FEE1D0C5443C83AA21768DE50EDFEA` |
| `en/08-tutorials/05-mod-template.md` | `947460e7cf3bb46d77014f70929fbdc8fa9924f2` | `E16C07E5362649AB67B3EE4CF1127EAF572963DCA164E7D5663A58642B4324D1` |
| `en/08-tutorials/08-hud-overlay.md` | `dd98fdd6e7c726c87fcb1fbc44f8f5c4c11ab93a` | `5FF49B0CB3808A4D02797A53126CA1C0C82A5568400ED06C76D4051A3856597C` |
| `en/08-tutorials/09-professional-template.md` | `47a16d1cacf37357eeb0b1b8c2923e29e43ce6f0` | `F324AB2DB983293666500FA34F7965D2FD25CE4A5C06E4F343865DD13521053E` |
| `en/08-tutorials/12-trading-system.md` | `e87b795d92d2c9831751272e1a673125d7087968` | `5C96B201F1ABE116682D2D43090E4EF47B8E4E621331AB101D51398076A08756` |
| `en/09-server-admin/09-access-control.md` | `5666591e927541b325fd1216c6b12355863c9259` | `04908C8185ABD19391FC1406C5AA0A4A39F82D71CFB41F861330AF7922B76A77` |
| `en/README.md` | `38a5a956538f225ece6452322ebe9956f6418c94` | `5472366533CE34642FEE78A3F72E255602E6264874FADE8CAE3224615B73B19A` |
| `en/glossary.md` | `38de9cc78089a86b7bdc9b161d82e3a50e44684f` | `F7DF274111CB8DC3066AA872771814296EA37308606584D7FC37D5EA2BAB365B` |
| `en/index.md` | `81b7ddcf32f3aa1c19adba12d48c42da18d16142` | `BCDA199EFB23A664353237DD10B273EB3F10F14AC5D844266A6680D030912718` |
| `.vitepress/config.mts` | `e0f8327928c8ea4cff65714b0f96febf74859a0b` | `269BAC4F8B88B0E8A96049444B3BB20E88BCA70D2246298D646DDB9B0A2FD371` |
