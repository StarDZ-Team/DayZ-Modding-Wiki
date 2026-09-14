# Language Runtime Implementation Record

> **Scope:** Apply the accepted, build-specific English corrections from `runtime-council.md` without promoting unresolved runtime cases to facts.

---

## Evidence reopened

- `runtime-council.md` and `runtime-council.json`, recorded 2026-09-13. The reviewed build is DayZDiag `1.29.0.163709`; the council records the executable SHA-256 `34F6377BE4FD065D104E67263E0C96AC2CB2E348119A4838EBA08D2E61B7A69A`.
- `D:\DayZ Projects\scripts\1_core\proto\enconvert.c`: `Normalize()` is declared at line 153 and argumentless `typename.Spawn()` at line 530. Those declarations were not used to infer zero-vector behavior or untested constructor signatures.
- `D:\DayZ Projects\scripts\3_game\entities\object.c`: `Object.IsAlive()` returns `!IsDamageDestroyed()` at lines 523-525.
- `D:\StarDZ\docs\DayZ\Enforce Script Syntax.md`: the local official-page snapshot describes `autoptr` variable-lifetime behavior, but not universal block, plain-local, or alias behavior.

---

## Applied mapping

| Council finding | Pages updated | Bounded outcome |
|---|---|---|
| Zero `Normalize()` | `07-math-vectors.md` | `vector.Zero.Normalize()` returned `0` and remained zero in the named build; the direction guard remains advice for later logic. |
| `typename.Spawn()` | `09-casting-reflection.md` | No explicit argument list; the tested one-required-`int` constructor received `0`. Other signatures, inheritance, and native constructors remain unverified. |
| Omitted `override` | `03-classes-inheritance.md`, `13-functions-methods.md` | Same-signature omission is documented as the named compiler error; invalid declarations are commented so the paired examples remain structurally valid. |
| `Object.IsDeleted()` | `08-memory-management.md` | Limited to the Mission-module compiler result; the page no longer says every raw alias becomes null or that null is the sole deletion signal. |
| `autoptr` | `08-memory-management.md`, `12-gotchas.md`, `glossary.md` | Documents variable-lifetime wording and the one function-return observation without claiming lexical-block equivalence, plain-local equivalence, or stale-alias safety. |
| Static lifecycle | `08-memory-management.md`, `01-singletons.md`, `02-module-systems.md`, `06-events.md` | Two calls in one callback are recorded; reconnect, `#restart`, and real mission reload persistence remain unverified. |

The valid global function declaration in `13-functions-methods.md` was preserved. The separate top-level `Print` statement compiler finding does not refute a declaration whose `Print` call is inside its function body.

---

## File identity

Base commit: `0df58c20761f654cd91ece04d9469be4b1728c6b`. Hashes are Git blob object IDs before and after this implementation.

| File | Baseline | Final |
|---|---|---|
| `en/01-enforce-script/03-classes-inheritance.md` | `5b03b7738954535e94533b266fe251cc01633916` | `dedfccfbc87f5ac575ba93e4b1663ed94857882e` |
| `en/01-enforce-script/07-math-vectors.md` | `5df20285a89a3366faa1fb2224a53c73be8bce11` | `9609cb6ac1c649179861253e5d233cb67d68db6d` |
| `en/01-enforce-script/08-memory-management.md` | `3711b6e81ab3fed820b888cab2d8afccde1d5704` | `a296a8a9a2314b0a9f06e280edcc2873797151c6` |
| `en/01-enforce-script/09-casting-reflection.md` | `037e600e7012bb75c0953ba89d81abc4fec4a8f7` | `e61a85032acea55786a57dac85bf3148c6ed8a20` |
| `en/01-enforce-script/12-gotchas.md` | `cc417be121b9f0c87fd4cb8fd1df803b1c3ebab3` | `97000f4d4ae44c7951927371b8dbefc10494f581` |
| `en/01-enforce-script/13-functions-methods.md` | `fb7f5777685199be08d4bbd709b40f37f8cc331d` | `d32d299973b68fdb2fc8b073cd6f2ff39451ef02` |
| `en/07-patterns/01-singletons.md` | `56faa9367a178c88fef8cbf02baee47e72642b91` | `0424756771bf222de8078a6122217974ba4ef1ba` |
| `en/07-patterns/02-module-systems.md` | `dd0f2b8cb535b5ee0f8f7a2a0c2a86577ab1f8f0` | `9435fafab7559c8953b80fd9c3dcfb84a0f4d1c1` |
| `en/07-patterns/06-events.md` | `ea9412613d6d5e94323184603f5f8cf991fcc51f` | `b1909fadba37a2c8f479817091bab0921ccd169d` |
| `en/glossary.md` | `38de9cc78089a86b7bdc9b161d82e3a50e44684f` | `9af7e1a5f94ca88c052f3b0e492bdaa012d4ff95` |

---

## Validation

- `git diff --check`: exit `0`.
- Changed-page structural check: all ten pages have one H1, balanced fenced blocks, and existing relative-link targets.
- Canonical validation: `node scripts/check-links.mjs --anchors --strict` checked 1,265 files and found zero dead file links. It checked 1,280 English anchors and reported one dead anchor in unrelated `en/04-file-formats/06-pbo-packing.md:30`; none is in this runtime scope.
- No VitePress build or DayZ launch was run. This validates documentation structure only, not Enforce Script compilation or runtime behavior.

---

## Remaining runtime gates for independent council

1. Probe `typename.Spawn()` separately for `string`, object, vector, multiple scalar, and inheritance constructor shapes.
2. Probe `autoptr` aliases after function return with guarded access; do not combine unsafe dereference with positive checks.
3. Reproduce static state and initializer behavior across controlled mission teardown/recreation and a real `#restart`.
4. Establish a stable diagnostic Mission/listener recipe before claiming Mission or listener lifecycle behavior.
