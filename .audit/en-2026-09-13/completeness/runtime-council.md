# Runtime startup and probe council review

> **Council result:** Accept the build-specific zero-vector, one-`int` `typename.Spawn()`, explicit-`override`, omitted-`override`, and `Object.IsDeleted()` compiler findings. Reject the affected EN universal claims. Keep static state across a mission restart, post-destruction alias behavior, other constructor signatures, and a stable diagnostic Mission/listener unresolved.

## Reviewed material and identity

The review reopened the exact probe sources, configs, PBOs, script logs, RPTs, English pages, and local documentation rather than relying on the author summaries.

- Runtime: `D:\SteamLibrary\steamapps\common\DayZ\DayZDiag_x64.exe`, 20,245,560 bytes, product version `1.29.0.163709`, SHA-256 `34F6377BE4FD065D104E67263E0C96AC2CB2E348119A4838EBA08D2E61B7A69A`. The retained and council RPT headers all report `Version 1.29.163709` and executable timestamp `2026/08/13 04:52:12`.
- Packer: `D:\SteamLibrary\steamapps\common\DayZ Experimental Tools\Bin\PboUtils\FileBank.exe`, SHA-256 `F89AAEB22421B9158FBBF173F75D52B6F3DE69986CB462E58956C78DA82C4CAF`. Council packing of three independent PBOs returned exit code `0`; runtime logs, not this exit code, decide script compilation.
- `runtime-probes.md` and `.json` still hash to the values recorded by the startup author: `0FAD140C...B5FDA` and `23D47A37...173E0`. They are a historical no-log report. Its baseline source/PBO paths were subsequently rebuilt, so those paths no longer have the old `55B81C...` / `FFFC1F...` hashes; use its recorded hashes for that historical attempt and `runtime-startup` for the superseding artifacts.
- Current `runtime-startup.md` hashes `4F37104E11846A9A0B505200B673649EA2E47E478C0535350A3F1E3B60A60A42`; its JSON hashes `BE842B97CDC82EE61570EECC22F25C0DE2ACFC5348126DCFFB1331AAD2D888CD`.
- All 23 executable, packer, current source, PBO, script-log, RPT, initial-error-log, and launcher-incident hashes explicitly recorded in `runtime-startup.json` were recomputed and matched. The spawn RPT also matched its recorded `8CE4E472...F9F08` hash. The three negative RPTs exist with the stated isolated command lines and build header, although the JSON does not assign all three a path/hash.
- `BankRev` extraction independently showed that the current original baseline, omitted-override, and `Object.IsDeleted` PBO payload scripts are byte-identical to the reported sources. The same check passed for the council PBOs. Thus the log's mod define, PBO hash, and unpacked source form a closed source-to-runtime chain.
- Retained file creation/modification times, RPT current times, isolated profile paths, command lines, module defines, and marker/error content are mutually consistent with the reported runs. They support freshness; timestamps alone would not prove it. The council reruns below provide independent fresh confirmation.

The extracted declaration source was also reopened: `D:\DayZ Projects\scripts\1_core\proto\enconvert.c`, SHA-256 `ABF20B92773A0872EB890F5A36EA3E4A228E4D4724BB9CD3ED86FC534A718CD4`, declares `proto float Normalize()` at line 153 and argumentless `proto volatile Class Spawn()` at line 530. Its adjacent comments do not specify zero-vector behavior or permitted constructor signatures. `D:\DayZ Projects\scripts.txt` says `version=124588`; that field was not treated as a game build number.

## Independent reruns

All runs used a dedicated `TEMP/runtime-council` source/mod/profile tree, `UseShellExecute = false`, hidden launch, and one complete option per `ProcessStartInfo.ArgumentList` element. No option contained literal profile-path quotes in the accepted runs. Each exact owned PID was stopped and awaited; the final process check found no `DayZDiag_x64`, `DayZServer_x64`, or `FileBank` process.

| Run | Source/PBO/log evidence | Result |
|---|---|---|
| Positive, PID `3808` | source `6637C29E...D3840`; PBO 2,342 bytes, `C747659E...827B`; script log `70B888CD...52A6`; RPT `B75B8725...8C67` | Fresh RPT command line used seven separate quote-free options and reports build `1.29.163709`. Markers show zero `Normalize()` returned `0` and remained zero; no-arg `Spawn()` succeeded; one-required-`int` `Spawn()` invoked the constructor with `0` and returned non-null; base-typed dispatch selected the child method marked `override`; the alias was non-null after the inner brace block; the destructor printed as the function returned; and the static counter printed `1`, then `2` in the same callback. |
| Omitted `override`, PID `32900` | source `5AADAAE1...EDFD`; PBO 976 bytes, `BFEDF700...57CC`; script log `8D316F11...E1D`; RPT `410BE681...3CCE` | Fresh compiler error: `Overriding function 'Label' but not marked as 'override'`. The process was stopped immediately after the specific diagnostic, before this log appended the generic `Can't compile` line. The retained original log independently contains both lines. |
| `Object.IsDeleted` control, PID `2140` | source `9C5EC366...D9D`; PBO 828 bytes, `D42D5708...30B7`; partial script log `A5A2FC4E...B354`; RPT `91757502...ED9E` | Inconclusive council rerun: a polling-expression error led to an owned stop before Mission compilation. It neither confirms nor contradicts the retained original compile error. The original source/PBO/log chain was independently reopened and hash-verified, so no further broad rerun was justified. |

Discarded harness attempts are recorded rather than silently promoted: PID `13892` received all options accidentally concatenated into one `ArgumentList` element and produced no profile output; PID `34740` used seven correct elements and loaded Mission but was stopped at the 50-second deadline before the main-menu marker; both were stopped and are not evidence for a language claim.

### Launcher finding

The quote-free `ArgumentList` recipe is accepted: PID `3808`'s WMI command line and fresh RPT show each complete `-mod=...` and `-profiles=...` option, the intended isolated profile received the logs, and the probe ran.

The startup author's narrower causal observation is credible but not fully reproducible from durable files: the reported PID memory string containing quote characters and thread context existed only live. Council PID `1276` deliberately supplied a literal-quote-bearing `ArgumentList` element. WMI showed the differently serialized raw command line `"-profiles=\"...\""`; after seven seconds it had a window and about five CPU seconds but no file in the configured profile, then was stopped. That is not the same raw command line or symptom as the earlier low-CPU/no-window PID, so it must not be represented as an independent reproduction.

Disposition: keep wording limited to the observed launcher. Recommend this replacement for `TEMP/wiki-runtime-probes/README.md:12-13` (not edited here):

> In the tested PowerShell launch, passing literal quote characters inside the `-profiles` option produced a quoted path in DayZ process memory and blocked that run. With `ProcessStartInfo.ArgumentList`, add the complete option as one element, for example `-profiles=D:\path`, without literal quote characters. This does not describe how batch files, `cmd.exe`, `Start-Process`, or other launchers quote arguments.

The official DayZ batch examples quote the whole command-line token. They do not contradict the `ArgumentList` recipe and do not establish a general shell-quoting rule.

## Findings and exact EN replacement wording

### Accepted repairs

1. **Zero vector normalization — accepted.** `en/01-enforce-script/07-math-vectors.md:664` and `:700` are contradicted. Replace both NaN claims with:

   > On DayZDiag `1.29.0.163709`, normalizing `vector.Zero` returned `0` and left the vector `<0,0,0>`; it did not produce NaN. Still guard with `LengthSq() > 0` when your later logic requires a meaningful direction.

2. **`typename.Spawn()` constructor restriction — accepted repair, bounded result.** `en/01-enforce-script/09-casting-reflection.md:313` and `:582` incorrectly require a parameterless constructor. Replace the note with:

   > `typename.Spawn()` accepts no explicit argument list. On DayZDiag `1.29.0.163709`, it created both a class with a no-argument constructor and a class whose constructor declared one required `int`; that `int` arrived as `0`, the type's default scalar value. This does not establish behavior for other parameter types, multiple parameters, inheritance cases, or every native constructor. Use explicit `new` or an `Init(...)` method when initialization data matters. Create DayZ world entities through the engine factories such as `CreateObject()` / `CreateObjectEx()`.

   Table wording at `:582`: `Takes no explicit arguments; a tested one-int constructor received 0 on 1.29.0.163709. Other signatures remain unverified.` The extracted `Spawn()` declaration being argumentless is not evidence that only parameterless constructors are accepted, nor that every constructor can be called with native defaults.

3. **Omitted `override` — accepted.** `en/01-enforce-script/03-classes-inheritance.md:901` and `en/01-enforce-script/13-functions-methods.md:718`, `:746-760`, `:1059`, and `:1068-1081` must not describe a warning, hidden new method, or parent-type dispatch. Use:

   > On DayZDiag `1.29.0.163709`, a child method with the same signature as a parent method must be marked `override`. Omitting the keyword emits `Overriding function '<name>' but not marked as 'override'` and prevents the Mission module from compiling.

   Keep the bad declaration commented in examples; the present `Dog` example declares both same-signature methods in one class and is not a valid good/bad pair. The positive base-typed dispatch only proves the explicitly marked override selected the child implementation.

4. **`Object.IsDeleted()` — accept only the tested compile claim.** At `en/01-enforce-script/08-memory-management.md:499-520`, replace the universal heading/opening with:

   > In the DayZ `1.29.0.163709` Mission module, `Object.IsDeleted()` is not an available instance call: the exact call compiled as `Undefined function 'Object.IsDeleted'`. This does not prove that no deletion-state facility exists anywhere in native code or on another type.

   The extracted `scripts/3_game/entities/object.c:523-525` does support the narrower statement that its script-defined `Object.IsAlive()` returns `!IsDamageDestroyed()`. The probe does **not** establish `:510`'s claims that every raw reference becomes null or that null is the only possible signal; qualify those statements until an entity deletion/alias runtime test exists.

5. **Bare top-level `Print` — no EN repair to global function declarations.** The retained compiler log proves only that a bare call statement at file top level is a syntax error. It does not contradict `en/01-enforce-script/13-functions-methods.md:57-65`, where a global *function declaration* contains `Print` in its body.

### Rejected or unsupported EN wording

- `en/01-enforce-script/08-memory-management.md:215`, `:223-245`, `:699`, `:729`, and `:753` overstate `autoptr` as universally identical to a plain local and as adding nothing. Replace the core explanation with:

  > Bohemia documents `autoptr` as destroying its target when the variable lifetime ends, giving function return or destruction of the containing class as examples. In the retained and council 1.29 probes, an `autoptr` declared inside nested braces remained alive through the statement after those braces and was destroyed as the function returned. That establishes this function's destruction order only; it does not establish universal equivalence with plain locals or safe use of a stale alias.

  The official-page snapshot `D:\StarDZ\docs\DayZ\Enforce Script Syntax.md` (SHA-256 `668281B2...DFD9`) supports end-of-variable-lifetime wording at lines 354 and 473-505. It does not prove every alias or every lexical block behavior. Apply the same qualification to `en/glossary.md:75`, `:643`, and `en/01-enforce-script/12-gotchas.md:333`; `scope` should not be glossed as every brace pair.

- `en/01-enforce-script/08-memory-management.md:469-495` is unresolved. The marker sequence proves only that a static field retained state between two immediate calls from one `MissionMainMenu.OnInit` callback in one process. Replace the section's factual lead with:

  > Static state persisted across two calls in one callback in the 1.29 probe. Persistence and initializer behavior across reconnect, `#restart`, or a real mission reload have not yet been reproduced here. Reset mutable static state during mission teardown as defensive lifecycle design, but do not present cross-restart persistence as a tested fact.

  The same evidence caveat applies to the factual persistence wording in `en/07-patterns/01-singletons.md:463`, `en/07-patterns/02-module-systems.md:712`, and `en/07-patterns/06-events.md:533`; the cleanup recommendations may remain as prudent design guidance.

## Source scope

- Primary official links consulted on `2026-09-13`: [Enforce Script Syntax](https://community.bistudio.com/wiki/DayZ%3AEnforce_Script_Syntax), [Modding Basics](https://community.bistudio.com/wiki/DayZ%3AModding_Basics), [Workbench Script Debugging](https://community.bistudio.com/wiki/DayZ%3AWorkbench_Script_Debugging), and [Server Configuration](https://community.bistudio.com/wiki/DayZ%3AServer_Configuration). Direct retrieval returned HTTP 403 for all four, so this review does not claim to have opened their current page bodies.
- Local fallible snapshots were actually read: `Enforce Script Syntax.md` (`668281B2...DFD9`, relevant lines 354, 473-505, 942-947), `Modding Basics.md` (`1A0B2C1...5839`, lines 154-173), and `Workbench Script Debugging.md` (`2E46B120...F16`, lines 49-52). They preserve official-page text but are not version-specific runtime proof.
- The official batch examples wrap a complete token such as `"-mod=P:\Mods\@FirstMod"`; the local diagnostic page says `DayZDiag_x64.exe` can act as client or server with `-server`. These sources support the reported launch form and server-mode lead only. The stable Mission/listener attempt still did not load Mission or prove a listening endpoint.

## Unresolved next tests

1. Run an isolated static probe across a controlled mission teardown/recreation and a real `#restart`, recording callback order and the same process ID. A stable Mission context is a prerequisite.
2. Test `autoptr` aliases in separate cases: alias nulling after function return, guarded alias access, and an attempted dereference. Do not combine a potentially unsafe dereference with positive probes.
3. Test `typename.Spawn()` constructor shapes separately: `string`, object, vector, multiple scalars, and inheritance. Report each default/value or compiler result; do not infer a universal native rule.
4. Repair the stable diagnostic mission recipe until `MissionServer.OnInit` and an owned loopback listener are both observed. The retained `SERVER`/`NO_GUI` World-module defines and orderly termination are accepted, but Mission/listen semantics remain unresolved.

No English file or original runtime artifact was edited, no commit was created, and no VitePress build was run.
