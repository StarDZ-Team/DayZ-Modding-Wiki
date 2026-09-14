# Independent translator protection review

Reviewed 2026-09-14 in `D:/StarDZ/docs/wiki`; task `task_b655e2f6a1f5`, dispatch `ctx_655036f42cea`. This is an adversarial static and mocked-generation review, not a translation-quality or DayZ runtime certification. Only this report was edited; no production changes, commits, subworkers, GPU/model calls, or translated output files were created.

---

## Result and priorities

The existing 12 tests passed, and all 105 current English pages round-tripped through protection/restoration unchanged. Those results do **not** establish preservation under generated changes. Confirmed initial-snapshot failures below include deterministic loss of angle-bracket link destinations, exposed code and link targets, incomplete output accepted as successful, and both missing and excessive identifier protection. Concurrent repairs landed before review completion; consult the final receipts and repair-status addendum for superseded fixtures. This is not final approval of those changing production files.

| ID | Priority | Confirmed finding | Suggested acceptance check |
|---|---|---|---|
| RP-01 | P1 | Nested placeholders lose their original contents even with an echo response | Angle-bracket links and HTML attributes round-trip without leaked markers |
| RP-02 | P1 | Indented code and HTML code contents reach the model and can be rewritten without rejection | Protect complete code nodes, or reject unsupported nodes before generation |
| RP-03 | P1 | Title-bearing links, reference links and nested-parenthesis destinations remain exposed | Preserve every destination/reference identifier independently of translated labels |
| RP-04 | P1 | End marker plus heading depths accepts a summary omitting all instructions/lists | Reject structural omissions and explicitly retain semantic completeness as a review limitation |
| RP-05 | P2 | Glossary declared types/config keys are ignored unless they match a naming heuristic | Use categories plus context for known single-word types and lowercase keys |
| RP-06 | P2 | Lexical extraction misses actual simple API names and common mod config keys | Inventory declarations/config keys across relevant input kinds, with provenance |
| RP-07 | P2 | Ordinary prose words and capitalized words before parentheses are frozen | Keep ambiguous prose translatable; require technical evidence/context |
| RP-08 | P2 | Filename whitelist omits real DayZ `.imageset` assets | Cover observed asset/config formats and paths, with boundary tests |
| RP-09 | P2 | Valid list-item fenced blocks are rejected as unclosed | Support list-container fences or report the unsupported syntax accurately |

These priorities concern the translator's preservation contract. Except for RP-01, showing that content is exposed does not prove the real Llama model will corrupt every occurrence. RP-02 through RP-04 additionally have mocked-generation demonstrations of corrupted/incomplete strings accepted by `traduzir_conteudo_wiki`.

---

## Exact review receipts

Git HEAD at review: `bbfa203d036e8f02c733e50011c89b9dfbdf9ecf`. Translator files are untracked in the shared checkout; the coordinator is editing concurrently. Initial source hashes:

| File | SHA-256 |
|---|---|
| `translator.py` | `fd555b8c4ceef5f7c7f7f109dc8a6280f68f8c024c76656eb149fa46064e0145` |
| `build_glossary.py` | `726ae43ef4a88758a0e8f6d1b90024ce1b6b80ae256600a40dd706536f36ef46` |
| `technical_glossary.json` | `8f03eff18da06fb2d85110464440f6896339ca87447fad7e67bd11d0ac403d34` |
| `test_translator.py` | `7ff9165017bd846b344b56bf491e0fbcb87265079f4eb640b7f6bb430526e1f8` |

A later observed translator hash was `f8cc4df8ff80477da26b20b9875756ac1a44a3f8d2b9fc0957573e6ba3dbd274`; protection, restoration and response checks were reopened at that revision, and the cited patterns remained. Changes after these receipts require fresh review. The final append-only receipt below records a consolidated reproduction against one in-memory source snapshot.

Reviewing agent model: exact runtime model identifier was not exposed to this worker; no claim is made about model selection. The translator's configured model is `meta-llama/Llama-3.1-8B-Instruct`; it was never loaded. All Python checks used `scripts/Translator/.env/Scripts/python.exe -B`, preventing import bytecode writes.

Read repository `AGENTS.md`, `CLAUDE.md`, translator README, installed orchestration skill and version-matched CLI guide. Read the dated second-pass report/source-use report/disposition ledger introductions as context, without treating their claims as evidence for this review.

---

## Reproduction harness

From the repository root, pipe this Python into `scripts/Translator/.env/Scripts/python.exe -B -`. It imports no GPU libraries and writes no files:

```python
import sys, re
from unittest.mock import patch
sys.path.insert(0, "scripts/Translator")
import translator as t

class Tokenizer:
    eos_token_id = 0
    def encode(self, text, **kwargs):
        return list(text)

class CorruptingPipeline:
    tokenizer = Tokenizer()
    def __call__(self, messages, **kwargs):
        text = messages[-1]["content"].split("\n\n", 1)[1]
        text = text.replace("installation", "instalacao")
        text = text.replace("danger", "perigo").replace("TranslateMe", "Traduzir")
        return [{"generated_text": text}]

class SummarizingPipeline:
    tokenizer = Tokenizer()
    def __call__(self, messages, **kwargs):
        end = re.search(r"WIKIEND[A-F0-9]+", messages[-1]["content"]).group()
        return [{"generated_text": "# Titulo\n\nOmitido.\n" + end}]

def show(source):
    masked, saved = t.proteger_codigo(source)
    print(repr(masked), saved)
    print(repr(t.restaurar_codigo(masked, saved)))

show('[Read](<guide.md>)\n')
show('<span title="`Widget`">Text</span>\n')

with patch.object(t, "pipe", CorruptingPipeline()):
    for source in (
        'Code:\n\n    danger = TranslateMe;\n    return danger;\n',
        '<pre><code>danger = TranslateMe;</code></pre>\n',
        '[Read](../guide.md#installation "Install guide")\n',
    ):
        print(repr(t.traduzir_conteudo_wiki(source, "Portuguese")))

with patch.object(t, "pipe", SummarizingPipeline()):
    source = ('# Heading\n\nFirst essential instruction.\n\n'
              'Second essential instruction.\n\n'
              '- Check access before deleting.\n- Save a backup.\n')
    print(repr(t.traduzir_conteudo_wiki(source, "Portuguese")))
```

The fake tokenizer simply counts characters; these examples fit in one input chunk. No claim about actual model tokenization or stochastic failure rate follows from these checks.

---

## Findings and repairs to consider

### RP-01 — Nested placeholder contents are discarded

`proteger_codigo` applies inline-code masking, HTML masking, then link-destination masking. A later mask can contain an earlier placeholder. Its final dictionary comprehension retains only markers present in the outer text (`ordem`, initially lines 157–158), so nested originals disappear. `restaurar_codigo` checks only this incomplete dictionary and returns successfully with an unresolved marker.

Exact inputs and observed output patterns:

```text
Input:  [Read](<guide.md>)\n
Output: [Read](WIKICODE<nonce>X0X)\n

Input:  [Read](<https://example.com/guide>)\n
Output: [Read](WIKICODE<nonce>X0X)\n

Input:  <span title="`Widget`">Text</span>\n
Output: <span title="WIKICODE<nonce>X0X">Text</span>\n
```

For the first input, the returned dictionary is effectively `{X1X: X0X}` rather than retaining the original `<guide.md>`. This is deterministic source corruption, independent of model quality. Prevent overlapping/nested replacement or preserve and correctly expand the full dependency graph; reject leaked markers after restoration. The round-trip assertion must compare restored bytes, not merely call restoration without checking equality.

### RP-02 — Code is protected only for recognized fences/backticks

The exact indented-code input in the harness produces an empty protected dictionary. The HTML input protects only the tags; its `danger = TranslateMe;` content remains exposed. With the corrupting mock, accepted results are:

```text
Code:\n\n    perigo = Traduzir;\n    return perigo;\n
<pre><code>perigo = Traduzir;</code></pre>\n
```

No generated backticks, heading changes or missing placeholders occur, so every current postcondition passes. Protect Markdown indented-code nodes and HTML code/pre content, or fail closed on unsupported forms. Add adversarial assertions that the text sent to the model excludes code and that a rewriting response cannot alter it.

### RP-03 — Link regex recognizes a restricted destination grammar

The destination regex requires a target directly followed by `)` and does not account for optional titles/reference definitions/deeper balanced parentheses. Exact exposed inputs:

```text
[Read](../guide.md#installation "Install guide")\n
[Read][guide]\n\n[guide]: ../guide.md#installation "Install guide"\n
[Read](../chapter_(draft_(two)).md#installation)\n
```

In the first two, only `guide.md` is masked by the filename fallback; `../`, the anchor and reference identifier remain exposed. The third remains entirely unmasked. The corrupting mock turns the first anchor into `#instalacao`, accepted by the translation function. Reference usage/definition labels can also diverge. Handle targets and reference identifiers using parsed source spans, preserving link labels/alt text as translatable prose. A target being masked does not itself validate the resulting route or translated heading anchor.

### RP-04 — End-marker presence does not prove complete translation

The summarizing mock in the harness returns `# Titulo\n\nOmitido.\n`. The source contains two instruction paragraphs and two list items; all are omitted. It is accepted because it is nonempty, has the end marker, and keeps one H1. There are no technical markers to force preservation of the deleted content.

This proves acceptance by `traduzir_conteudo_wiki`, not an observed real-model omission or an actual disk write. The caller can consequently pass that successful return value to its normal save path. Preserve/check paragraph/list/table structures or translate bounded identified prose units; validate each unit's presence. Counts and length ratios can catch gross omissions but remain heuristics and cannot establish semantic completeness. Document any residual need for review instead of presenting an end sentinel as a completeness guarantee.

### RP-05 — Glossary evidence categories are not used by protection

Exact input:

```text
Use Timer and Widget and Object. Call Print(). Set scope = 2 and weight = 100.
```

Only `Print` is masked (the capitalized-call regex). `Timer`, `Widget`, `Object`, `scope` and `weight` remain exposed. The first three already have `declared_type` entries; the last two have `config_key` entries. The protector discards that evidence by reapplying the CamelCase/underscore/acronym heuristic.

The source declarations were independently opened (see source receipts). Do not simply freeze every lowercase config key everywhere: `scope`, `weight`, `units` and many type names also occur in ordinary prose. Add category-aware contextual handling for explicit declarations/assignments/API mentions and tests for ambiguous prose. Current inline-code masking covers these names when authors use backticks; this failure concerns the advertised protection outside backticks.

### RP-06 — The 89,963-term inventory is not a complete API/config glossary

`Print` is absent even though `proto void Print(void var);` exists in the included official extraction at `scripts/1_core/proto/endebug.c:96`. `Call Print to log the message.` remains completely unmasked. `build_glossary.py` records simple declared types, technical-shaped tokens, and extracted-config assignment names; it does not extract all function declarations.

`inputs` and `dependencies` are also absent. They appear in the actual opened StarDZ mod config and English example, but the builder reads user mod `*.c` only, and its `config_key` extraction is restricted to `extracted_config`. Lowercase keys from wiki code therefore do not enter the dictionary, and user mod `config.cpp` is not an input. Consider user mod configs, relevant XML/layout schemas and declaration-aware extraction; retain source-kind distinctions and do not treat occurrence as proof of behavior.

The inventory reports 105 wiki files, 2,810 extracted scripts, 209 extracted configs and 730 user mod scripts. All 105 recorded wiki input hashes matched current files during this review. That verifies provenance freshness for that subset, not lexical completeness or source correctness.

### RP-07 — Ambiguity handling freezes ordinary language

Exact input:

```text
This is true for native tools, not false. Use a string to override the value.
Documentation (optional).
```

The first line freezes `true`, `native`, `false`, `string`, and `override` regardless of context. The second freezes `Documentation` merely because a capitalized word precedes a parenthesis; no glossary membership is required. The resulting target-language text must retain these English tokens even when they are ordinary prose. Expand ambiguity handling and require meaningful call syntax/known symbol evidence rather than any capitalized word plus optional whitespace and `(`. Avoid solving RP-05 with indiscriminate freezing that worsens this problem.

### RP-08 — Real asset filenames outside the whitelist are exposed

`Use prefabs.imageset and config.bin and styles.css.` remains wholly unmasked. `prefabs.imageset` is independently evidenced by the opened beta config at line 37; this is a real DayZ mod asset reference, not an invented extension. The existing `arquivos` whitelist includes `.layout` but omits `.imageset` (and other formats). Expand coverage from observed file/path evidence, with punctuation/path-boundary tests; do not describe a finite whitelist as universal filename protection.

### RP-09 — List-container fence opening is not recognized

Exact valid Markdown input:

```text
- ```c\n  danger = TranslateMe;\n  ```\n
```

The opening regex accepts whitespace and `>` prefixes, but not the list marker. It later treats the closing fence as an opening and raises `ValueError: Bloco de código sem fechamento no Markdown de origem.` This is a fail-closed availability bug rather than accepted code corruption. Parse container structure, and include nested ordered/unordered lists in regression fixtures.

---

## Independently opened DayZ evidence

The extraction's game/build version was not independently established; evidence here establishes spelling/declarations at the exact local hashes only. The StarDZ config is a beta implementation, not authoritative native behavior. No web sources or community discussions were accessed for this bounded lexical review.

| Actual file | Lines opened / evidence | SHA-256 |
|---|---|---|
| `D:/DayZ Projects/scripts/3_game/tools/tools.c` | 570–594; `class Timer extends TimerBase` at 576 | `60050a0079a434568b2310662608b5a32959ade19cfcc7cc2593f55974cd2a84` |
| `D:/DayZ Projects/scripts/1_core/proto/enwidgets.c` | 100–118; `class Widget: Managed` at 107 | `6bb20bad5efa498e584c7ae8976a1bf5310bcd9019215f31cb2990af21ce0c9e` |
| `D:/DayZ Projects/scripts/3_game/entities/object.c` | 60–76; `class Object extends IEntity` at 64 | `ebac48ff196148ab4722a9d9a81c277796d4ea07896a5cf09742213d32424b4c` |
| `D:/DayZ Projects/bin/config.cpp` | 365–383; `scope=0` at 372, `attachments[]={}` at 379 | `42b4cf95cf945b7f4164c69748ebab226c00e1e6e4de5f111a0d9f7754d37b6e` |
| `D:/DayZ Projects/DZ/AI/config.cpp` | 1–20; `units[]={}` at 5 | `da53bdb980d01362f442799ea4086e1f7406d5d9270c2af1066ab1c11b0baf86` |
| `D:/DayZ Projects/scripts/1_core/proto/endebug.c` | 83–104; `proto void Print(void var)` at 96 | `ca3151514781ced9355bf1e2f095f98d984764091d5fa51d621bd099f51ea746` |
| `D:/StarDZ/StarDZ_Core/StarDZ_Core/Scripts/config.cpp` | 1–43; `inputs` at 22, `dependencies[]` at 26, `prefabs.imageset` at 37 | `faf4136778bd63623a61a1d26df1b192052cd4001ff95d8858b3faaae96dffc9` |
| `en/02-mod-structure/02-config-cpp.md` | 162–190; `inputs` at 176, `dependencies[]` at 182 | `bdd728c3d49ea79a87af331a7079ab8dddc683fdc254f19a57603226f1bddc06` |

---

## Existing tests and limitations

Executed `scripts/Translator/.env/Scripts/python.exe -B -m unittest discover -s scripts/Translator -p test_translator.py -v`: **12 passed, exit 0**. Existing tests exercise missing end markers, marker order/multiplicity, recognized fenced blocks, simple inline code, one simple destination, a few selected glossary terms, and atomic replace failure. They do not test the adversarial cases above.

The 105-page protection/restoration sweep reported zero exceptions and zero mismatches. It does not prove all generated outputs preserve those pages; the mocked mutation tests demonstrate the difference. No VitePress build was needed for this report-only task, and none was run. No actual GPU translation, script compilation, game behavior, save-path execution or language quality was tested. CLI/chunking/recovery design belongs to the coordinator's concurrent work and is not approved by this report.


---

## Final in-memory snapshot reproduction receipt

The following results were obtained by compiling one captured `translator.py` byte sequence in memory, avoiding ambiguity from concurrent edits during that run. Marker nonces are intentionally nondeterministic.

```json
{
  "python": "3.14.3 (tags/v3.14.3:323c59a, Feb  3 2026, 16:04:56) [MSC v.1944 64 bit (AMD64)]",
  "translator_sha256": "fdc1b37a3c37c78f58c77547bcedc5186b1f139ba213650bc151d8014d49be81",
  "model_configured": "meta-llama/Llama-3.1-8B-Instruct",
  "model_revision_configured": "0e9e39f249a16976918f6564b8830bc894c89659",
  "hashes": {
    "build_glossary.py": "8c8f02043f814371f86920d7458b3c296f75698a3950a7c304c290d0428aa36f",
    "technical_glossary.json": "a13dbabeee701ee59e6743a46f612afac92e330eeef66afc2ed027e7a1a230f6",
    "test_translator.py": "7ff9165017bd846b344b56bf491e0fbcb87265079f4eb640b7f6bb430526e1f8"
  },
  "results": {
    "RP-01": {
      "masked": "[Read](WIKICODEA0D217DDX1X)\n",
      "saved": [
        "<guide.md>"
      ],
      "roundtrip": true
    },
    "RP-02-indent": {
      "masked": "Code:\n\nWIKICODEA8191077X0X\n",
      "saved": [
        "    danger = TranslateMe;\n    return danger;"
      ],
      "roundtrip": true
    },
    "RP-02-html": {
      "masked": "WIKICODEE37D9049X0X\n",
      "saved": [
        "<pre><code>danger = TranslateMe;</code></pre>"
      ],
      "roundtrip": true
    },
    "RP-03": {
      "masked": "[Read](WIKICODE84ACAB3CX0X \"Install guide\")\n",
      "saved": [
        "../guide.md#installation"
      ],
      "roundtrip": true
    },
    "RP-05": {
      "masked": "Use WIKICODEC85C74DBX1X and WIKICODEC85C74DBX2X and WIKICODEC85C74DBX3X. Set WIKICODEC85C74DBX0X = 2.",
      "saved": [
        "Timer",
        "Widget",
        "Object",
        "scope"
      ],
      "roundtrip": true
    },
    "RP-06": {
      "masked": "WIKICODE2A70DF63X0X WIKICODE2A70DF63X1X to log the message.",
      "saved": [
        "Call",
        "Print"
      ],
      "roundtrip": true
    },
    "RP-07": {
      "masked": "WIKICODE7ECB53BFX0X (optional).",
      "saved": [
        "Documentation"
      ],
      "roundtrip": true
    },
    "RP-08": {
      "masked": "Use WIKICODE5F10AA1DX0X and WIKICODE5F10AA1DX1X and WIKICODE5F10AA1DX2X.",
      "saved": [
        "prefabs.imageset",
        "config.bin",
        "styles.css"
      ],
      "roundtrip": true
    },
    "RP-09": {
      "error": "ValueError: Bloco de código sem fechamento no Markdown de origem."
    },
    "RP-04": {
      "error": "O modelo removeu, duplicou ou alterou a ordem dos marcadores protegidos; a tradução não será gravada."
    }
  }
}
```

## Concurrent repair status — limited follow-up, not final approval

The coordinator requested finalization against the reviewed snapshot and will request a separate final review after repairs. The snapshot receipt above already confirms the demonstrated angle-bracket link, indented/pre-code, title-bearing target, known type/assignment and filename examples now protect correctly. It does not certify all variations: reference links, deeply nested targets and list fences still require their explicit tests. RP-07 remains and the broadened callable inventory now also freezes the ordinary imperative `Call` in `Call Print to log the message.`; type/callable membership alone is not sufficient disambiguation. The reopened builder still excludes user mod config.cpp and only extracts config keys for extracted_config, so the inputs/dependencies intake gap remains.

The original summarizing mock now fails because previously unprotected prose words were added to the glossary; this is not structural validation. A modified mock copies every WIKICODE marker in input order into one summary paragraph. By the time this follow-up ran, a newer concurrent revision had added list/table structural checks and correctly rejected the omitted list; the exact rejection is recorded below. This supersedes the original RP-04 demonstration for that specific list-omission fixture, without proving semantic completeness. Its replacement response expression is `"# Titulo\n\nOmitido. " + " ".join(re.findall(r"WIKICODE[A-F0-9]+X\d+X", messages[-1]["content"])) + "\n" + end`. Exact result:

```json
{
  "translator_sha256": "d824e2fc113d0e0717f57697242605b6abb1f31cad25d66745892bee87db99ac",
  "marker_preserving_summary_result": "RuntimeError: O modelo alterou a estrutura de t\u00edtulos, listas ou tabelas; a tradu\u00e7\u00e3o n\u00e3o ser\u00e1 gravada."
}
```

Proposed measurable checks for RP-04: preserve ordered/unordered item count and nesting, table row/cell counts, paragraph/unit IDs, link/image counts and destinations, and block ordering; reject responses missing any required unit. These catch specific structural omissions, while paraphrase fidelity and semantic completeness remain an explicit review limitation.
