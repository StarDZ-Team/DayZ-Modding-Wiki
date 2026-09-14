# Critical Corrections — Final Independent Council

> **Verdict:** Rejected for scoped commit. The reviewed prose corrections are mostly accurate, but the eleven-file delivery still contains two uncorrected readiness claims and one invalid Mermaid diagram. The required shared sidebar rename is also absent outside the eleven-file content scope.

## Scope

- Baseline and current `HEAD`: `9dc36064459f3184404bdba4db9d95b843b6fcaa`.
- Reviewed exactly the eleven author-listed content files below against that baseline.
- Reopened the cited official extraction, saved Bohemia pages, pinned CF/COT/VPP checkouts, cookbook, and currency contract. Their recorded SHA-256 hashes and pinned commits matched `critical-council.md/json`.
- Did not edit English content, launch DayZ, or treat static rendering as script/runtime validation.

## Decisions

| Finding | Prose implementation | Functional finding | Reason |
|---|---|---|---|
| `OPS-C01` | Accepted | Unresolved | The page now separates `passwordAdmin` from BattlEye `RConPassword` and retains the distinct-canary/log test requirement. |
| `OPS-C02` | Accepted | Unresolved | The unsupported vanilla panel inventory is replaced by an evidence-bounded retail/Diag/RCon/mod distinction; retail capture remains outstanding. |
| `TUT-C01` | Rejected | Unresolved | The safe-refusal prose matches the handlers, but the changed Mermaid diagram does not parse and `.vitepress/config.mts:137` still says `Trading System`. The durable transaction fixture remains outstanding. |
| `TUT-C02` | Rejected | Unresolved | The main chapter downgrade is accurate, but `README.md:77` still says `Production-ready starter` and `en/08-tutorials/05-mod-template.md:57` still says `full production template`. The materialized end-to-end fixture remains outstanding. |
| `LANG-C03` | Accepted | Accepted after static check | The TOC now says `Config-Based Type Checking`, and the unchanged anchor resolves. |
| `RPC-C02` | Accepted | Unresolved | Both unmeasured ceiling claims are qualified correctly. The two-client measurement matrix remains outstanding. |

Accepted content files: `en/01-enforce-script/09-casting-reflection.md`, `en/07-patterns/03-rpc-patterns.md`, `en/08-tutorials/08-hud-overlay.md`, `en/08-tutorials/09-professional-template.md`, `en/09-server-admin/09-access-control.md`, `en/README.md`, `en/glossary.md`, and `en/index.md`.

Rejected content files: `README.md`, `en/08-tutorials/05-mod-template.md`, and `en/08-tutorials/12-trading-system.md`. Acceptance of `en/08-tutorials/09-professional-template.md` is file-scoped; `TUT-C02` remains rejected until its two cross-page claims are repaired.

## Exact repairs

1. In `README.md:77`, replace the whole line with:

   ```markdown
   - [Professional Mod Template](en/08-tutorials/09-professional-template.md) — Feature-rich illustrative starter (not runtime-validated)
   ```

2. In `en/08-tutorials/05-mod-template.md:57`, replace the final sentence with:

   ```markdown
   Chapter 8.9 is the feature-rich illustrative template (not runtime-validated).
   ```

3. In `en/08-tutorials/12-trading-system.md:44`, replace the Mermaid message with:

   ```text
   S->>S: Bind sender, validate quantity and catalog
   ```

   The current semicolon is parsed as a Mermaid statement terminator and produces a sequence-diagram parse error.

4. Outside this worker's eleven-file review/edit scope, change `.vitepress/config.mts:137` from `Trading System` to `Shop UI & Safe Refusal` without changing the route.

After those repairs, rerun Mermaid grammar parsing, strict links/anchors, `git diff --check`, and a fresh exact-hash review. Do not close `OPS-C01`, `OPS-C02`, `TUT-C01`, `TUT-C02`, or `RPC-C02` as functionally complete.

## Validation

- `node scripts/check-links.mjs --anchors --strict`: exit 0; 1,265 Markdown files, zero dead file links; 105 EN files and 1,278 fragments, zero dead anchors.
- Installed `mermaid.parse()` on the changed diagram: failed at `Bind sender; validate quantity and catalog` with `Expecting ... got 'NEWLINE'`.
- `git diff --check 9dc3606... -- <eleven files>`: exit 0.
- Fence/H1 inspection found no changed fence-balance or H1-count defect; the Mermaid failure is grammar-specific.
- No full VitePress build, Enforce compilation, pack/sign operation, server/client run, or gameplay test was performed.

## Reopened evidence

- Saved Bohemia server configuration `D:/StarDZ/docs/DayZ/Server Configuration.md`, SHA-256 `D7126F849E9A460887A3B640068CA8C88304324EDFD3AFA1526AE69E4BECAA8E`, lines 19 and 150-175: separate `passwordAdmin` and `RConPassword` paths.
- Saved Bohemia Diag Menu `D:/StarDZ/docs/DayZ/Diag Menu.md`, SHA-256 `58CAD3A5194F0237A99D30C08BE68F60B5B2A531C605817022E50397D14FE616`, lines 690-694 and 801-854: Diag free camera and teleport controls.
- Official extraction under `D:/DayZ Projects/scripts`: `gameplay.c`, `object.c`, inventory creation, deletion, player-list, and developer-plugin files all matched the hashes recorded in `critical-council.json`.
- Pinned CF `0763e7e7548c9a0bed6626afff835de80693ebf3`, COT `41f2c2b99565d0e3970163e162efbf1283fdca62`, and VPP `dc22e420df3b54e821055f9764da1e48f4a31e71` checkouts matched their cited commits and file hashes. They were used only as third-party implementation evidence.
- `D:/StarDZ/docs/COOKBOOK_RECEITAS_COMPLETAS.md`, SHA-256 `0D05D8B011933D7E9ADC246CA3180C14A6EC2681F39CC91C655458509DEB9B9A`, lines 241-254: packing is not Enforce compilation.
- `D:/StarDZ/docs/STARDZ_CURRENCY_BRIDGE_CONTRACT.md`, SHA-256 `2CCF77EDC3DC6F0E3CD3FD8AC7B3CBDB8A85EBCCB845C88223958AA15DA2EEE9`, lines 1-124: useful idempotency/recovery design, explicitly unfinished Enforce validation rather than proof of a working tutorial.

## Exact final file identities

These identities describe the rejected review state and must be recomputed after repair.

| File | Final Git blob | Final SHA-256 |
|---|---|---|
| `README.md` | `cd7fd1e9d9e6b895a023f08be6d9b299a8379752` | `E0EF643ED1ACF985A086116AC12FE79E6AFAF5BC2D404FDA823A2334D289519E` |
| `en/01-enforce-script/09-casting-reflection.md` | `037e600e7012bb75c0953ba89d81abc4fec4a8f7` | `24DB725C3D0B6B2C098B0446C2970F3CD0463E1AB871ACE688393563FD4FCE2C` |
| `en/07-patterns/03-rpc-patterns.md` | `20331ed0c688953ba257c468f1f4d78db1b1e526` | `7185F4FE065041BFE705A78641C6967771FEE1D0C5443C83AA21768DE50EDFEA` |
| `en/08-tutorials/05-mod-template.md` | `732a197a79a6f323ccee23b056779f22dcea4159` | `2B8E601D3DFD4783C1212CDA1B6730083BE489295DF7B00CBD081709AA55756B` |
| `en/08-tutorials/08-hud-overlay.md` | `dd98fdd6e7c726c87fcb1fbc44f8f5c4c11ab93a` | `5FF49B0CB3808A4D02797A53126CA1C0C82A5568400ED06C76D4051A3856597C` |
| `en/08-tutorials/09-professional-template.md` | `47a16d1cacf37357eeb0b1b8c2923e29e43ce6f0` | `F324AB2DB983293666500FA34F7965D2FD25CE4A5C06E4F343865DD13521053E` |
| `en/08-tutorials/12-trading-system.md` | `14a58a214db1f36d4db0830882db82fbdd693a51` | `63FEA7F7098FB06BF51D450E8ABA7D5CF62EEFED2D2A34F4E8702D850D83B77B` |
| `en/09-server-admin/09-access-control.md` | `5666591e927541b325fd1216c6b12355863c9259` | `04908C8185ABD19391FC1406C5AA0A4A39F82D71CFB41F861330AF7922B76A77` |
| `en/README.md` | `38a5a956538f225ece6452322ebe9956f6418c94` | `5472366533CE34642FEE78A3F72E255602E6264874FADE8CAE3224615B73B19A` |
| `en/glossary.md` | `38de9cc78089a86b7bdc9b161d82e3a50e44684f` | `F7DF274111CB8DC3066AA872771814296EA37308606584D7FC37D5EA2BAB365B` |
| `en/index.md` | `81b7ddcf32f3aa1c19adba12d48c42da18d16142` | `BCDA199EFB23A664353237DD10B273EB3F10F14AC5D844266A6680D030912718` |
