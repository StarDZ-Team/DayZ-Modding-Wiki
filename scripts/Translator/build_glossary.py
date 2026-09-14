"""Gera um inventário lexical; ocorrência de um nome não valida seu comportamento."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import gzip
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
IDENTIFIER = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\b")
NON_CODE = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\x27(?:\\.|[^\x27\\])*\x27')


def technical_shape(name):
    return bool(re.search(r"[a-z][A-Z]|[A-Z]{2,}[a-z]|[A-Za-z]_[A-Za-z]|^[A-Z][A-Z0-9_]{2,}$", name))


def build(game_root, mod_root):
    sources = []
    terms = {}

    def add(term, category, source, line):
        entry = terms.setdefault(term, {"categories": [], "evidence": []})
        if category not in entry["categories"]:
            entry["categories"].append(category)
        if len(entry["evidence"]) < 2:
            evidence = {"source": source, "line": line}
            if evidence not in entry["evidence"]:
                entry["evidence"].append(evidence)

    inputs = [(p, "wiki") for p in sorted((ROOT / "en").rglob("*.md"))]
    if not (game_root / "scripts").is_dir():
        raise FileNotFoundError(game_root / "scripts")
    inputs += [(p, "extracted_script") for p in sorted((game_root / "scripts").rglob("*.c"))]
    inputs += [(p, "extracted_config") for p in sorted(game_root.rglob("config.cpp")) if "SteamLibrary" not in p.parts]
    for folder in sorted(mod_root.glob("StarDZ_*")):
        inputs += [(p, "user_mod") for p in sorted(folder.rglob("*.c"))]
        inputs += [(p, "user_mod_config") for p in sorted(folder.rglob("config.cpp"))]
    for path, kind in inputs:
        raw = path.read_bytes()
        text = raw.decode("utf-8-sig", errors="replace")
        source_id = len(sources)
        sources.append({"path": path.as_posix(), "kind": kind, "sha256": hashlib.sha256(raw).hexdigest()})
        if kind == "wiki":
            # Só trechos explicitamente marcados como código alimentam o inventário.
            matches = list(re.finditer(r"^```[^\n]*\n[\s\S]*?^```[ \t]*$|(?<!`)`[^`\n]+`(?!`)", text, re.M))
            segments = [(match.group(), text.count("\n", 0, match.start()) + 1) for match in matches]
        else:
            segments = [(text, 1)]
        for segment, first_line in segments:
            clean = NON_CODE.sub(lambda m: "\n" * m.group().count("\n"), segment)
            for offset, line in enumerate(clean.splitlines()):
                for match in re.finditer(r"\b(?:class|enum)\s+([A-Za-z_]\w*)", line):
                    add(match[1], "declared_type", source_id, first_line + offset)
                for match in re.finditer(r"^\s*(?:(?:proto|native|external|owned|static|override|private|protected|public|volatile)\s+)*[A-Za-z_]\w*(?:<[^>]+>)?\s+([A-Za-z_]\w*)\s*\(", line):
                    add(match[1], "declared_callable", source_id, first_line + offset)
                for match in IDENTIFIER.finditer(line):
                    if technical_shape(match[0]):
                        add(match[0], "technical_identifier", source_id, first_line + offset)
                if kind in ("extracted_config", "user_mod_config") or (kind == "wiki" and segment.startswith("```cpp")):
                    for match in re.finditer(r"\b([A-Za-z_]\w*)\s*(?:\[\])?\s*=", line):
                        add(match[1], "config_key", source_id, first_line + offset)
    result = {
        "schema": 1,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "game_version": "unknown; exact local inputs identified by SHA-256",
        "source_counts": dict(Counter(s["kind"] for s in sources)),
        "sources": sources,
        "terms": dict(sorted(terms.items())),
    }
    serialized = (json.dumps(result, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
    (OUT / "technical_glossary.json.gz").write_bytes(gzip.compress(serialized, mtime=0))
    print(json.dumps({"terms": len(terms), "sources": result["source_counts"]}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--game-root", type=Path, default=Path("D:/DayZ Projects"))
    parser.add_argument("--mod-root", type=Path, default=Path("D:/StarDZ"))
    args = parser.parse_args()
    build(args.game_root, args.mod_root)
