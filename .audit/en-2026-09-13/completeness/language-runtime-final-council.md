# Language Runtime Final Council

> **Verdict:** Reject the current ten-file scoped delivery pending one documentation-example repair. The runtime wording is correctly bounded, but `en/01-enforce-script/13-functions-methods.md:1070-1082` declares `CustomPlayer` twice in one code block, so the advertised good example is not coherent as a compilable unit.

## Scope and identity

- Baseline: `0df58c20761f654cd91ece04d9469be4b1728c6b` (also the current `HEAD`; the reviewed delivery is an uncommitted working-tree diff).
- Reviewed exactly the ten paths listed below. Concurrent edits under `en/02-mod-structure/`, `en/04-file-formats/06-pbo-packing.md`, and `en/08-tutorials/07-publishing-workshop.md` were excluded.
- `git diff --check 0df58c2 -- <ten paths>` exited `0`.
- Each page has exactly one H1, an even number of fenced-code delimiters, and no missing relative file target.

| Path | Baseline Git blob | Reviewed Git blob | Reviewed SHA-256 | Disposition |
|---|---|---|---|---|
| `en/01-enforce-script/03-classes-inheritance.md` | `5b03b7738954535e94533b266fe251cc01633916` | `dedfccfbc87f5ac575ba93e4b1663ed94857882e` | `E7F62E8E9A3247AF7F40658265A3BDBA3DDE68ADB1A78F143F507AFBA6C6FCE9` | Accept |
| `en/01-enforce-script/07-math-vectors.md` | `5df20285a89a3366faa1fb2224a53c73be8bce11` | `9609cb6ac1c649179861253e5d233cb67d68db6d` | `847492C278E49631F52EB16327BA9729CA1879E98C1380B3A0FC37B55624F5AA` | Accept |
| `en/01-enforce-script/08-memory-management.md` | `3711b6e81ab3fed820b888cab2d8afccde1d5704` | `a296a8a9a2314b0a9f06e280edcc2873797151c6` | `599F6F656E8E87F297F58CF2838C551A8E3C33AF1FB4ADB2AC1191CD4CF4D076` | Accept |
| `en/01-enforce-script/09-casting-reflection.md` | `037e600e7012bb75c0953ba89d81abc4fec4a8f7` | `e61a85032acea55786a57dac85bf3148c6ed8a20` | `6DCC7D5119FA070574C312A930375C40E247992CFE26A251322F38D7767B859F` | Accept |
| `en/01-enforce-script/12-gotchas.md` | `cc417be121b9f0c87fd4cb8fd1df803b1c3ebab3` | `97000f4d4ae44c7951927371b8dbefc10494f581` | `55AA05DF8B89EEE5F6374ADB02B2CC74EF80F64B2AC710A577E9B6F7D66EE09F` | Accept |
| `en/01-enforce-script/13-functions-methods.md` | `fb7f5777685199be08d4bbd709b40f37f8cc331d` | `d32d299973b68fdb2fc8b073cd6f2ff39451ef02` | `F1359D4A73BE7970B2217D63438CFFA0A96EB4821D13597D886AC91D1D332B84` | Reject pending repair |
| `en/07-patterns/01-singletons.md` | `56faa9367a178c88fef8cbf02baee47e72642b91` | `0424756771bf222de8078a6122217974ba4ef1ba` | `5EF4AF4604B35E4F714E56E61726EAC870B484B8195EF5445BA9401C3E144F55` | Accept |
| `en/07-patterns/02-module-systems.md` | `dd0f2b8cb535b5ee0f8f7a2a0c2a86577ab1f8f0` | `9435fafab7559c8953b80fd9c3dcfb84a0f4d1c1` | `36178D0ADF5E8D72F89A8E2BCB5463C11618279D19350C7CB5F7DC79186D3BD9` | Accept |
| `en/07-patterns/06-events.md` | `ea9412613d6d5e94323184603f5f8cf991fcc51f` | `b1909fadba37a2c8f479817091bab0921ccd169d` | `1C34099B5A2F23C8190C01FD1ECC9EA74AF1D8EEF9AF907988538CCB639DC6F3` | Accept |
| `en/glossary.md` | `38de9cc78089a86b7bdc9b161d82e3a50e44684f` | `9af7e1a5f94ca88c052f3b0e492bdaa012d4ff95` | `29C821A526C00308CF1F03C8AB03DE6CCB77CDA823633D20E38D5138A1FC8A99` | Accept |

## Independent evidence review

The retained original and prior council evidence was reopened rather than rerun. The following hashes recomputed exactly:

- Extracted declarations: `enconvert.c` SHA-256 `ABF20B92773A0872EB890F5A36EA3E4A228E4D4724BB9CD3ED86FC534A718CD4`; it declares `proto float Normalize()` at line 153 and argumentless `proto volatile Class Spawn()` at line 530. Neither declaration proves the observed zero-vector result or untested constructor shapes.
- Extracted `object.c` SHA-256 `EBAC48FF196148AB4722A9D9A81C277796D4EA07896A5CF09742213D32424B4C`; lines 523-525 define `Object.IsAlive()` as `!IsDamageDestroyed()`.
- Local Bohemia-page snapshot `Enforce Script Syntax.md` SHA-256 `668281B26FD8212CA0995A524140BAB1B9706153E3095ECB19444E1B9290DFD9`; lines 354 and 473-505 support variable-lifetime/function-return wording for `autoptr`, not universal lexical-block, plain-local, or alias behavior.
- Council positive source/PBO/script log/RPT hashes are `6637C29E...D3840`, `C747659E...827B`, `70B888CD...52A6`, and `B75B8725...8C67`. Reopened markers show zero normalization returned `0` and stayed zero; no-argument and one-required-`int` `Spawn()` succeeded with the `int` equal to `0`; marked base dispatch selected the child; the nested-brace `autoptr` alias remained non-null before destruction at function return; and a static counter produced `1`, then `2`, in one callback.
- Council omitted-override source/PBO/script log/RPT hashes are `5AADAAE1...EDFD`, `BFEDF700...57CC`, `8D316F11...E1D`, and `410BE681...3CCE`. The council log contains the specific omitted-`override` diagnostic; the retained original log, SHA-256 `4E432020...B4D4`, also contains `Can't compile "Mission" script module!`.
- The retained `Object.IsDeleted()` source SHA-256 is `936889E0...D6A9`; its script log SHA-256 `FC402798...90B` contains `Undefined function 'Object.IsDeleted'` and the Mission-module compilation failure.
- The retained bare-global-`Print` source SHA-256 is `9A449B67...5982`; its log SHA-256 `9BB9FA29...4572` proves only that the call statement on source line 1 is a syntax error. The valid global function declarations at `en/01-enforce-script/13-functions-methods.md:57-73`, including `Print()` inside a function body, remain intact.

## Wording decisions

- **Zero `Normalize()`: accepted.** Both changed passages name DayZDiag `1.29.0.163709`, report only the observed return/value, and frame the nonzero guard as advice when a meaningful direction is required.
- **`typename.Spawn()`: accepted.** The prose separates the argumentless API from the observed no-argument and one-`int` constructor results, enumerates unverified shapes, and directs initialization-sensitive and world-entity creation to explicit mechanisms.
- **Omitted `override`: accepted wording.** All changed claims are build/module-specific and match the retained compiler evidence. The changed `Parent`/`Child` and `Animal`/`Dog` pairs are coherent because the bad member is commented and the good member remains active.
- **`Object.IsDeleted()`: accepted.** The claim is limited to the tested Mission-module instance call. Post-deletion alias/null behavior and facilities elsewhere remain explicitly unverified.
- **`autoptr`: accepted.** The changed passages distinguish documentation from the one observed destruction sequence and avoid universal plain-local, brace-scope, and stale-alias claims.
- **Static lifecycle: accepted.** The pages record only two calls in one callback and present teardown reset as defensive design; reconnect, `#restart`, and real mission reload remain unverified.
- **No unsupported universal runtime claim was found in the changed prose.** This approval does not extend to unchanged surrounding claims or to runtime cases still gated below.

## Required repair

In `en/01-enforce-script/13-functions-methods.md:1070-1082`, replace the two same-name class declarations with one coherent class:

```c
class CustomPlayer extends PlayerBase
{
    // BAD: uncommenting this produces the omitted-override compiler error.
    // void OnConnect() { Print("Custom!"); }

    // GOOD: properly overrides.
    override void OnConnect() { Print("Custom!"); }
}
```

After that edit, recompute this file's Git blob and SHA-256, recheck the exact ten-file diff, and rerun the structural and canonical validations before approval. No other runtime content repair is required by this council.

## Canonical validation and remaining gates

`node scripts/check-links.mjs --anchors --strict` checked 1,265 files, reported zero dead file links, checked 1,282 English anchors, and exited `1` for one dead anchor outside runtime ownership: current `en/04-file-formats/06-pbo-packing.md:613` links to `../../.audit/en-2026-09-13/completeness/pbo-research.md#pbo-011--replace-vague-real-mods-claims-with-pinned-examples`, whose rendered target anchor does not exist. This is a concurrent PBO-worker defect and was not edited here.

Runtime gates remain unchanged: separately probe other `typename.Spawn()` constructor shapes; post-return `autoptr` alias behavior; static state across controlled mission teardown and real `#restart`; and a stable diagnostic Mission/listener recipe. No DayZ process was launched and no runtime content file was edited in this review.
