import argparse
from datetime import datetime, timezone
from contextlib import contextmanager
from copy import deepcopy
from functools import lru_cache
import hashlib
import gzip
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import unicodedata
import uuid
from markdown_it import MarkdownIt
from markdown_it.helpers import parseLinkDestination

# 1. Configuração de caminhos relativos
DIRETORIO_ATUAL = Path(__file__).resolve().parent
RAIZ_WIKI = DIRETORIO_ATUAL.parents[1] # Sobe dois níveis (de scripts/translator/ para a raiz)

PASTA_ORIGEM_EN = RAIZ_WIKI / "en"

# 2. Mapeamento de todas as línguas suportadas pela Wiki (excluindo o inglês)
IDIOMAS_SUPORTADOS = {
    "pt": "Português do Brasil",
    "de": "Alemão",
    "ru": "Russo",
    "es": "Espanhol",
    "fr": "Francês",
    "ja": "Japonês",
    "zh-hans": "Chinês Simplificado",
    "cs": "Tcheco",
    "pl": "Polonês",
    "hu": "Húngaro",
    "it": "Italiano"
}

MODELOS = {
    "llama": ("meta-llama/Llama-3.1-8B-Instruct", "0e9e39f249a16976918f6564b8830bc894c89659"),
    "qwen": ("Qwen/Qwen3-8B", "b968826d9c46dd6066d109eabc6255188de91218"),
}
model_id, MODEL_REVISION = MODELOS["qwen"]
pipe = None

# Preserva também termos sem crases. A correspondência distingue maiúsculas.
TERMOS_TECNICOS = {
    "DayZ", "Enforce Script", "Enfusion", "Enforce", "RPC", "PBO",
    "Addon Builder", "Workbench", "Central Economy", "Object Builder",
    "CfgPatches", "CfgMods", "CfgVehicles", "CfgWeapons", "CfgMagazines",
    "requiredAddons", "requiredVersion", "scriptModule", "worldScriptModule",
    "gameScriptModule", "missionScriptModule", "stringtable",
    "Class", "Managed", "EntityAI", "ItemBase", "ManBase", "PlayerBase",
    "ScriptedWidgetEventHandler", "MissionServer", "MissionGameplay", "GetGame",
    "int", "float", "bool", "string", "vector", "typename", "void",
    "modded", "override", "proto", "native", "autoptr", "ref", "notnull",
    "class", "enum", "typedef", "const", "static", "private", "protected",
    "public", "super", "null", "true", "false", "array", "map", "set",
    "func", "auto", "inout", "owned", "external", "volatile",
}

# Podem ser palavras comuns. Fora de código, só protege se houver sintaxe explícita.
TERMOS_AMBIGUOS = {"class", "array", "map", "set", "static", "private", "protected", "public", "auto", "Set", "Get", "Copy", "Clear", "Insert", "Remove", "Update", "Delete", "Create", "Read", "Write", "Open", "Close", "Start", "Stop", "Init", "Load", "Save"}
TERMOS_AMBIGUOS.update({"native", "true", "false", "string", "override", "Call"})
TERMOS_AMBIGUOS.update({"Type", "Size", "Default", "Value", "Text", "Reference"})
# Inclui também termos usados ao comparar linguagens; não afirma suporte nativo.
TERMOS_AMBIGUOS.update({"out", "thread", "event", "sealed", "if", "else", "for",
                       "foreach", "while", "switch", "case", "default", "break",
                       "continue", "return", "new", "delete", "this", "do", "try",
                       "catch", "throw", "interface", "abstract", "namespace", "delegate"})

# Estes nomes também descrevem prosa comum ("this type", "return type").
# Fora de sintaxe explícita, exigem um descritor de palavra-chave ou operador.
TERMOS_PROSA_COMUM = {"if", "else", "for", "foreach", "while", "switch", "case",
                      "default", "break", "continue", "return", "new", "delete",
                      "this", "do", "try", "catch", "throw", "interface",
                      "abstract", "namespace", "delegate"}


@lru_cache(maxsize=1)
def carregar_inventario():
    caminho = DIRETORIO_ATUAL / "technical_glossary.json.gz"
    if not caminho.is_file():
        raise RuntimeError("Glossário ausente. Execute build_glossary.py antes de traduzir.")
    return json.loads(gzip.decompress(caminho.read_bytes()))


def carregar_glossario():
    return carregar_inventario()["terms"]


def consultar_termo(termo):
    inventario = carregar_inventario()
    registro = inventario["terms"].get(termo)
    saida = {"term": termo, "manual_rule": termo in TERMOS_TECNICOS or termo in TERMOS_AMBIGUOS, "ambiguous": termo in TERMOS_AMBIGUOS, "found": registro is not None}
    if registro:
        saida["categories"] = registro["categories"]
        saida["evidence"] = [{**inventario["sources"][e["source"]], "line": e["line"]} for e in registro["evidence"]]
    print(json.dumps(saida, ensure_ascii=False, indent=2))
    return 0 if registro or saida["manual_rule"] else 1


def diagnosticar():
    import importlib.metadata
    import torch
    from huggingface_hub import get_token
    dados = {"python": sys.version, "executable": sys.executable, "cuda_available": torch.cuda.is_available(), "torch_cuda": torch.version.cuda, "hf_token_configured": bool(get_token()), "model": model_id, "revision": MODEL_REVISION}
    dados["packages"] = {p: importlib.metadata.version(p) for p in ("torch", "transformers", "bitsandbytes", "accelerate", "huggingface-hub", "markdown-it-py", "lingua-language-detector")}
    if torch.cuda.is_available():
        dados["gpu"] = torch.cuda.get_device_name(0)
    inventario = carregar_inventario()
    dados["glossary_terms"] = len(inventario["terms"])
    dados["glossary_sources"] = inventario["source_counts"]
    print(json.dumps(dados, ensure_ascii=False, indent=2))
    return 0 if dados["cuda_available"] else 1


def carregar_modelo():
    import torch
    from transformers import pipeline, BitsAndBytesConfig

    if not torch.cuda.is_available():
        raise RuntimeError(
            "CUDA indisponível neste Python. Instale o PyTorch com suporte CUDA "
            "no ambiente .env (consulte README.md nesta pasta)."
        )
    dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=dtype,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True
    )
    print(f"Carregando {model_id} em 4-bit: {torch.cuda.get_device_name(0)}...")
    return pipeline(
        "text-generation",
        model=model_id,
        revision=MODEL_REVISION,
        model_kwargs={"quantization_config": quantization_config},
        dtype=dtype,
        device_map={"": 0}
    )

def proteger_codigo(texto):
    """Retira código, destinos de links e termos técnicos da entrada do modelo."""
    termos = TERMOS_TECNICOS - TERMOS_AMBIGUOS
    glossario = carregar_glossario()
    for nome in set(re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", texto)):
        if nome in glossario and nome not in TERMOS_AMBIGUOS:
            categorias = glossario[nome]["categories"]
            if len(nome) > 1 and (re.search(r"[a-z][A-Z]|[A-Z]{2,}[a-z]|[A-Za-z]_[A-Za-z]|^[A-Z][A-Z0-9_]{2,}$", nome) or (nome[0].isupper() and "declared_type" in categorias)):
                termos.add(nome)
    # APIs usadas com parênteses e identificadores explicitamente marcados.
    termos.update(re.findall(r"\b([A-Z][A-Za-z0-9_]*)(?=\()", texto))
    termos.update(re.findall(r"\b(?:[Cc]all|[Ii]nvoke|[Mm]ethod|[Ff]unction)[ \t]+([A-Z][A-Za-z0-9_]*)\b", texto))
    termos.update(re.findall(r"(?<!`)`([A-Z][A-Za-z0-9_]*)`(?!`)", texto))
    prefixo = "WIKICODE" + hashlib.sha256(texto.encode("utf-8")).hexdigest()[:10].upper()
    while prefixo in texto:
        prefixo = f"WIKICODE{uuid.uuid4().hex[:10].upper()}"
    protegidos = {}

    def guardar(conteudo):
        # Uma proteção externa pode englobar outra (links com <destino>, HTML).
        # Expande os marcadores internos antes de guardar, evitando perda de dados.
        if prefixo in conteudo:
            for anterior, original in protegidos.items():
                conteudo = conteudo.replace(anterior, original)
        marcador = f"{prefixo}X{len(protegidos)}X"
        protegidos[marcador] = conteudo
        return marcador

    # O corpo de pre/code também é código, mesmo sem cercas Markdown.
    texto = re.sub(r"<(pre|code|script|style)\b[^>]*>[\s\S]*?</\1\s*>", lambda m: guardar(m.group()), texto, flags=re.I)
    if texto.startswith("---\n") or texto.startswith("---\r\n"):
        frontmatter = re.match(r"\A---\r?\n[\s\S]*?\r?\n---(?=\r?\n|$)", texto)
        if frontmatter:
            texto = guardar(frontmatter.group()) + texto[frontmatter.end():]
    linhas = texto.splitlines(keepends=True)
    partes = []
    indice = 0
    for token in MarkdownIt().parse(texto):
        if token.type not in ("fence", "code_block", "hr"):
            continue
        inicio, fim = token.map
        if inicio < indice:
            raise ValueError("Blocos Markdown sobrepostos não são suportados.")
        if token.type == "fence":
            cerca = token.markup
            fechamento = r"^[ \t>]*" + re.escape(cerca[0]) + "{" + str(len(cerca)) + r",}[ \t]*(?:\r?\n)?$"
            if fim - inicio < 2 or not re.match(fechamento, linhas[fim - 1]):
                raise ValueError("Bloco de código sem fechamento no Markdown de origem.")
        partes.extend(linhas[indice:inicio])
        bloco = "".join(linhas[inicio:fim])
        quebra = "\r\n" if bloco.endswith("\r\n") else "\n" if bloco.endswith("\n") else ""
        partes.append(guardar(bloco[:-len(quebra)] if quebra else bloco) + quebra)
        indice = fim
    partes.extend(linhas[indice:])

    texto = "".join(partes)
    inline = re.compile(r"(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)", re.DOTALL)
    texto = inline.sub(lambda match: guardar(match.group(0)), texto)
    texto = re.sub(r"\{#[^{}\s]+\}", lambda m: guardar(m.group()), texto)
    html = re.compile(r"<!--[\s\S]*?-->|</?[A-Za-z][^>]*>")
    texto = html.sub(lambda match: guardar(match.group(0)), texto)
    diretivas = re.compile(r"(?m)^([ \t]*:::[ \t]*(?:[A-Za-z-]+)?)")
    texto = diretivas.sub(lambda match: guardar(match.group(0)), texto)
    texto = re.sub(r"(?m)^[ \t]*<<<[^\n]*", lambda m: guardar(m.group()), texto)
    # O parser reconhece destinos com escapes e parênteses balanceados.
    spans = []
    for match in re.finditer(r"\]\([ \t]*", texto):
        inicio = match.end()
        destino = parseLinkDestination(texto, inicio, len(texto))
        if destino.ok and destino.pos > inicio:
            spans.append((inicio, destino.pos))
    for inicio, fim in reversed(spans):
        texto = texto[:inicio] + guardar(texto[inicio:fim]) + texto[fim:]
    # Referências: a definição completa e o identificador usado devem coincidir.
    referencias = set(re.findall(r"(?m)^[ \t]{0,3}\[([^]\n]+)\]:", texto))
    texto = re.sub(r"(?m)^[ \t]{0,3}\[[^]\n]+\]:[^\n]*(?:\n[ \t]+[^\n]+)*", lambda m: guardar(m.group()), texto)
    texto = re.sub(r"(?<=\])\[([^]\n]+)\]", lambda m: guardar(m.group()), texto)
    for referencia in referencias:
        # Referências curtas/colapsadas usam o próprio rótulo como chave.
        padrao = r"\[" + re.escape(referencia) + r"\](?:\[\])?(?![\[(])"
        texto = re.sub(padrao, lambda m: guardar(m.group()), texto, flags=re.I)
    caminhos = re.compile(r"https?://[^\s<>]+|(?:\$profile:|\$saves:|\$CurrentDir:|[A-Za-z]:[\\/])[^\s<>\"`]*")
    texto = caminhos.sub(lambda match: guardar(match.group(0)), texto)
    arquivos = re.compile(r"\b[\w$][\w.$-]*\.(?:cpp|hpp|pbo|paa|p3d|rvmat|layout|xml|json|cfg|csv|c|md|yaml|yml|exe|bat|ps1|bikey|bisign|edds|ogg|wav|sqf)\b")
    texto = arquivos.sub(lambda match: guardar(match.group(0)), texto)
    expressoes = re.compile(r"\b[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)+(?:\(\))?|\b[A-Za-z_]\w*\(\)")
    texto = expressoes.sub(lambda match: guardar(match.group(0)), texto)
    chaves = {nome for nome in re.findall(r"\b[A-Za-z_]\w*\b", texto) if nome not in TERMOS_AMBIGUOS and nome in glossario and "config_key" in glossario[nome]["categories"]}
    if chaves:
        contexto = re.compile(r"\b(?:" + "|".join(re.escape(k) for k in sorted(chaves, key=len, reverse=True)) + r")\b(?=[ \t]*(?:\[\]|=|property\b|setting\b|field\b|parameter\b|attribute\b|array\b))")
        texto = contexto.sub(lambda match: guardar(match.group(0)), texto)
    ambiguos = "|".join(re.escape(t) for t in sorted(TERMOS_AMBIGUOS, key=len, reverse=True))
    texto = re.sub(r"\b(?:" + ambiguos + r")\b(?=[ \t]*(?:\(|\[|=))", lambda m: guardar(m.group()), texto)
    contexto_tecnico = r"(?:(?:keyword|modifier|type|method|function|setting|field|parameter|attribute|literal|statement|operator)s?|propert(?:y|ies))"
    for candidatos, contexto in (
        (TERMOS_AMBIGUOS - TERMOS_PROSA_COMUM, contexto_tecnico),
        (TERMOS_PROSA_COMUM, r"(?:keyword|statement|operator)s?"),
        ({"sealed", "abstract", "static", "private", "protected", "public"}, r"class(?:es)?"),
    ):
        nomes = "|".join(re.escape(t) for t in sorted(candidatos, key=len, reverse=True))
        texto = re.sub(r"\b(?:" + nomes + r")\b(?=[ \t]+" + contexto + r"\b)", lambda m: guardar(m.group()), texto)
        texto = re.sub(r"\b(" + contexto + r")([ \t]+)(" + nomes + r")\b", lambda m: m[1] + m[2] + guardar(m[3]), texto)
    padrao_termos = re.compile(r"(?<![\w])(?:" + "|".join(re.escape(t) for t in sorted(termos, key=len, reverse=True)) + r")(?![\w])")
    texto = padrao_termos.sub(lambda match: guardar(match.group(0)), texto)
    # Quantidades fazem parte das afirmações técnicas; não deixe o modelo mudá-las.
    numeros = re.compile(r"(?<![\w.])[+-]?(?:0[xX][0-9a-fA-F]+|(?:\d+(?:[.,]\d+)*|[.,]\d+)(?:[eE][+-]?\d+)?)(?:%|\b)")
    def guardar_numero(match):
        inicio_linha = texto.rfind("\n", 0, match.start()) + 1
        if not texto[inicio_linha:match.start()].strip() and re.match(r"[.)]\s", texto[match.end():]):
            return match.group()
        return guardar(match.group())
    texto = numeros.sub(guardar_numero, texto)
    # A ordem de criação difere da ordem no documento quando há código inline.
    ordem = re.findall(re.escape(prefixo) + r"X\d+X", texto)
    return texto, {marcador: protegidos[marcador] for marcador in ordem}


def restaurar_codigo(texto, protegidos):
    if not protegidos:
        return texto
    prefixo = next(iter(protegidos)).split("X", 1)[0]
    encontrados = re.findall(re.escape(prefixo) + r"X\d+X", texto)
    if encontrados != list(protegidos):
        raise RuntimeError(
            "O modelo removeu, duplicou ou alterou a ordem dos marcadores protegidos; "
            "a tradução não será gravada."
        )
    for marcador, original in protegidos.items():
        if re.match(r"[ \t>]*(?:(?:[-+*]|\d+[.)])[ \t]+)?(?:`{3,}|~{3,})|^(?: {4}|\t)", original):
            if not re.search(r"^[ \t]*" + re.escape(marcador) + r"[ \t]*\r?$", texto, re.M):
                raise RuntimeError("O modelo moveu um bloco de código para dentro de um parágrafo.")
        texto = texto.replace(marcador, original)
    return texto


def dividir_texto(texto, tokenizer, limite=1200):
    """Divide em linhas/parágrafos sem cortar identificadores ou marcadores."""
    partes = []
    atual = ""
    for linha in texto.splitlines(keepends=True):
        if len(tokenizer.encode(linha, add_special_tokens=False)) > limite:
            raise RuntimeError("Uma linha excede o limite de entrada; divida-a antes de traduzir.")
        if atual and len(tokenizer.encode(atual + linha, add_special_tokens=False)) > limite:
            partes.append(atual)
            atual = ""
        atual += linha
        if not linha.strip() and len(tokenizer.encode(atual, add_special_tokens=False)) >= limite // 2:
            partes.append(atual)
            atual = ""
    if atual:
        partes.append(atual)
    return partes


def validar_estrutura(origem, destino):
    def estrutura(texto):
        tokens = MarkdownIt().enable("table").parse(texto)
        blocos = [(t.type, t.tag, t.nesting, t.attrs) for t in tokens if t.type != "inline"]
        inline = [(c.type, c.tag, c.nesting) for t in tokens for c in (t.children or []) if c.type not in ("text", "softbreak")]
        listas = re.findall(r"^[ \t]*(?:[-*+] |\d+[.)] )", texto, re.M)
        return blocos, inline, listas
    if estrutura(origem) != estrutura(destino):
        raise RuntimeError("O modelo alterou a estrutura de títulos, listas ou tabelas; a tradução não será gravada.")
    sem_marcadores = lambda s: re.sub(r"WIKICODE[A-F0-9]+X\d+X", "", s)
    original = re.sub(r"\s+", "", sem_marcadores(origem))
    traduzido = re.sub(r"\s+", "", sem_marcadores(destino))
    if len(original) > 100 and len(traduzido) < len(original) * 0.2:
        raise RuntimeError("Resposta muito curta em relação à origem; possível resumo ou omissão.")


def ancoras_titulos(texto):
    tokens = MarkdownIt().parse(texto)
    usados = set()
    resultado = []
    for i, token in enumerate(tokens):
        if token.type != "heading_open":
            continue
        titulo = "".join(c.content for c in (tokens[i + 1].children or []) if c.type in ("text", "code_inline"))
        explicito = re.search(r"\s*\{#([^{}\s]+)\}\s*$", titulo)
        if explicito:
            slug = explicito[1]
        else:
            slug = unicodedata.normalize("NFKD", titulo)
            slug = re.sub(r"[\u0300-\u036f\x00-\x1f]", "", slug)
            especiais = "~`!@#$%^&*()-_+=[]{}|\\;:\"'“”‘’<>,.?/"
            slug = re.sub(r"[\s" + re.escape(especiais) + r"]+", "-", slug).strip("-").lower()
            slug = re.sub(r"^(\d)", r"_\1", slug)
        base = slug
        numero = 1
        while slug in usados:
            slug = f"{base}-{numero}"
            numero += 1
        usados.add(slug)
        resultado.append((token.map[0], slug))
    return resultado


def fixar_ancoras(origem, destino):
    originais = ancoras_titulos(origem)
    traduzidos = ancoras_titulos(destino)
    if len(originais) != len(traduzidos):
        raise RuntimeError("Número de títulos alterado.")
    linhas = destino.splitlines(keepends=True)
    for (_, slug), (linha, _) in zip(originais, traduzidos):
        if not re.match(r"#{1,6}\s", linhas[linha]):
            raise RuntimeError("Use títulos ATX (#) antes de traduzir.")
        quebra = "\n" if linhas[linha].endswith("\n") else ""
        titulo = re.sub(r"\s*\{#[^{}\s]+\}\s*$", "", linhas[linha].rstrip())
        titulo = re.sub(r"\s+#+$", "", titulo)
        linhas[linha] = titulo + " {#" + slug + "}" + quebra
    return "".join(linhas)


@lru_cache(maxsize=1)
def detector_idioma():
    from lingua import Language, LanguageDetectorBuilder
    idiomas = [Language.ENGLISH, Language.PORTUGUESE, Language.GERMAN, Language.RUSSIAN,
               Language.SPANISH, Language.FRENCH, Language.JAPANESE, Language.CHINESE,
               Language.CZECH, Language.POLISH, Language.HUNGARIAN, Language.ITALIAN]
    return LanguageDetectorBuilder.from_languages(*idiomas).build()


def validar_idioma(texto, idioma_destino):
    prosa = re.sub(r"WIKICODE[A-F0-9]+X\d+X", " ", texto)
    letras = "".join(c for c in prosa if c.isalpha())
    codigo = next((tag for tag, nome in IDIOMAS_SUPORTADOS.items() if nome == idioma_destino), None)
    if codigo is None:
        codigo = {"Português": "pt", "Portuguese": "pt"}.get(idioma_destino)
    if codigo is None:
        raise ValueError(f"Idioma desconhecido: {idioma_destino}")
    if len(letras) < (10 if codigo in ("ja", "zh-hans", "ru") else 40):
        return  # Amostra insuficiente: não é uma verificação de idioma.
    esperado = "zh" if codigo == "zh-hans" else codigo
    detectado = detector_idioma().detect_language_of(prosa)
    if detectado is None or detectado.iso_code_639_1.name.lower() != esperado:
        nome = detectado.name if detectado is not None else "indeterminado"
        raise RuntimeError(f"Idioma detectado: {nome}; esperado: {idioma_destino}. A tradução não será gravada.")


# 4. Engenharia de prompt dinâmica por idioma
class FalhaTraducao(RuntimeError):
    def __init__(self, mensagem, detalhes):
        super().__init__(mensagem)
        self.detalhes = detalhes


def traduzir_conteudo_wiki(texto_original, idioma_destino, max_new_tokens=4096, cache_dir=None, reutilizar=True):
    texto_protegido, protegidos = proteger_codigo(texto_original)
    if restaurar_codigo(texto_protegido, protegidos) != texto_original:
        raise RuntimeError("Proteção de código alterou a origem; tradução recusada antes da geração.")
    global pipe
    if pipe is None:
        pipe = carregar_modelo()
    nomes = dict(zip(IDIOMAS_SUPORTADOS.values(), ("Brazilian Portuguese", "German", "Russian", "Spanish", "French", "Japanese", "Simplified Chinese", "Czech", "Polish", "Hungarian", "Italian")))
    alvo = nomes.get(idioma_destino, idioma_destino)
    system_prompt = (
        f"Translate English DayZ modding documentation into {alvo}. Write all explanatory prose in {alvo}.\n"
        "Translate faithfully: preserve every instruction, qualification, negation and dependency. Never summarize, omit or add information.\n"
        "Preserve Markdown exactly: heading levels, paragraph breaks, list indentation, table rows/cells, emphasis, links and images. Do not rewrap lines.\n"
        "Protected spans are opaque tokens beginning with WIKICODE. Copy each token exactly once, in the same order and location. "
        "Never expand, translate, decorate or put backticks around tokens. A token alone on a line must remain alone on that line.\n"
        "Translate ordinary language naturally, including words such as inventory, class or string when used as prose. "
        "Preserve actual programming identifiers, class/method names, configuration keys and tool names. "
        "Do not invent code, headings, introductions, comments about the translation or Markdown fences.\n"
    )

    traducoes = []
    trechos = dividir_texto(texto_protegido, pipe.tokenizer)
    for numero_trecho, trecho in enumerate(trechos, 1):
        cache = cache_dir / (hashlib.sha256((trecho + alvo).encode()).hexdigest() + ".json") if cache_dir else None
        if cache and reutilizar and cache.is_file():
            try:
                salvo = json.loads(cache.read_text(encoding="utf-8"))
                if not isinstance(salvo, dict) or not isinstance(salvo.get("output"), str):
                    raise ValueError("Formato de cache inválido")
                if salvo["sha256"] == hashlib.sha256(salvo["output"].encode()).hexdigest():
                    validar_estrutura(trecho, salvo["output"])
                    locais = {m: protegidos[m] for m in re.findall(r"WIKICODE[A-F0-9]+X\d+X", trecho)}
                    restaurar_codigo(salvo["output"], locais)
                    traducoes.append(salvo["output"])
                    continue
            except (KeyError, ValueError, RuntimeError):
                pass  # Cache inválido é regenerado, nunca publicado diretamente.
        if cache_dir:
            print(f"    Trecho {numero_trecho}/{len(trechos)}...")
        fim = "WIKIEND" + hashlib.sha256((trecho + alvo).encode("utf-8")).hexdigest()[:10].upper()
        rejeicoes = []
        for tentativa in (1, 2):
            orientacao = ""
            if rejeicoes:
                orientacao = (
                    "\nThe previous response failed validation: " + rejeicoes[-1]["error"] +
                    "\nRegenerate the entire original section below. Preserve every protected token "
                    "and the Markdown structure; do not patch or reuse the rejected response."
                )
            messages = [
                {"role": "system", "content": system_prompt + orientacao + f"\nEnd your response with the literal marker {fim}. Output only the translation and this marker."},
                {"role": "user", "content": f"Translate this section into {alvo}:\n\n{trecho}\n{fim}"}
            ]
            generation = {"max_new_tokens": max_new_tokens, "do_sample": False, "pad_token_id": pipe.tokenizer.eos_token_id}
            if hasattr(pipe, "generation_config"):
                from transformers import set_seed
                set_seed(41 + tentativa)
                config = deepcopy(pipe.generation_config)
                config.max_length = None
                config.max_new_tokens = max_new_tokens
                config.do_sample = model_id.startswith("Qwen/")
                config.temperature = 0.7 if config.do_sample else 1.0
                config.top_p = 0.8 if config.do_sample else 1.0
                config.top_k = 20 if config.do_sample else 50
                config.pad_token_id = pipe.tokenizer.eos_token_id
                generation = {"generation_config": config}
            # Falhas do pipeline (incluindo OOM) não são falhas de validação e não repetem.
            outputs = pipe(
                messages,
                **generation,
                return_full_text=False,
                clean_up_tokenization_spaces=False,
                tokenizer_encode_kwargs={"enable_thinking": False}
            )
            conteudo = outputs[0]["generated_text"]
            detalhes = {"chunk": numero_trecho, "language": idioma_destino, "source_protected": trecho,
                        "attempt": tentativa, "seed": 41 + tentativa, "response": conteudo}
            try:
                if not isinstance(conteudo, str) or conteudo.count(fim) != 1 or not conteudo.rstrip().endswith(fim):
                    raise RuntimeError("Resposta incompleta ou sem marcador final; a tradução não será gravada.")
                conteudo = conteudo[:conteudo.index(fim)].strip()
                if not conteudo:
                    raise RuntimeError("O modelo não retornou uma tradução válida.")
                # Mantém separadores entre trechos; o modelo pode omiti-los.
                inicio = re.match(r"\s*", trecho).group()
                final = re.search(r"\s*$", trecho).group()
                conteudo = inicio + conteudo + final
                if "`" in conteudo or re.search(r"^[ \t]*~{3,}", conteudo, re.M):
                    raise RuntimeError("O modelo inventou cercas de código; a tradução não será gravada.")
                validar_estrutura(trecho, conteudo)
                locais = {m: protegidos[m] for m in re.findall(r"WIKICODE[A-F0-9]+X\d+X", trecho)}
                restaurar_codigo(conteudo, locais)
            except RuntimeError as erro:
                rejeicoes.append({**detalhes, "error": str(erro)})
                if tentativa == 2:
                    raise FalhaTraducao(str(erro), {**detalhes, "attempts": rejeicoes}) from erro
                continue
            break
        if cache:
            cache.parent.mkdir(parents=True, exist_ok=True)
            salvo = {"sha256": hashlib.sha256(conteudo.encode()).hexdigest(), "output": conteudo}
            salvar_traducao(cache, json.dumps(salvo, ensure_ascii=False) + "\n")
        traducoes.append(conteudo)
    conteudo = "".join(traducoes)
    if "`" in conteudo or re.search(r"^[ \t]*~{3,}", conteudo, re.M):
        raise RuntimeError("O modelo inventou cercas de código; a tradução não será gravada.")
    try:
        validar_estrutura(texto_protegido, conteudo)
        validar_idioma(conteudo, idioma_destino)
        restaurado = restaurar_codigo(conteudo, protegidos)
        validar_estrutura(texto_original, restaurado)
    except RuntimeError as erro:
        raise FalhaTraducao(str(erro), {"language": idioma_destino, "source_protected": texto_protegido, "response": conteudo}) from erro
    return fixar_ancoras(texto_original, restaurado)


def salvar_traducao(arquivo_destino, conteudo):
    # Substitui o destino apenas depois de concluir a gravação.
    temporario = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="", dir=arquivo_destino.parent,
            suffix=".tmp", delete=False
        ) as f:
            temporario = Path(f.name)
            f.write(conteudo)
        os.replace(temporario, arquivo_destino)
    finally:
        if temporario is not None:
            temporario.unlink(missing_ok=True)

# 5. Execução em lote para todas as línguas
def hash_arquivo(caminho):
    return hashlib.sha256(caminho.read_bytes()).hexdigest() if caminho.is_file() else None


def caminho_seguro(raiz, relativo):
    caminho = (raiz / relativo).resolve()
    if not caminho.is_relative_to(raiz.resolve()):
        raise ValueError(f"Caminho fora da pasta permitida: {relativo}")
    return caminho


@contextmanager
def bloquear_lote():
    trabalho = DIRETORIO_ATUAL / ".translations"
    trabalho.mkdir(exist_ok=True)
    lock = trabalho / "run.lock"
    try:
        with lock.open("x", encoding="utf-8") as arquivo:
            arquivo.write(json.dumps({"pid": os.getpid(), "started_utc": datetime.now(timezone.utc).isoformat()}))
    except FileExistsError:
        raise RuntimeError(f"Outro lote possui o bloqueio {lock}. Se houve interrupção abrupta, confira o PID antes de remover o bloqueio.") from None
    try:
        yield
    finally:
        lock.unlink(missing_ok=True)


def iniciar_traducao_em_massa(idiomas=None, filtros=None, aplicar=False, verificar=False, retomar=True, max_falhas=3):
    if verificar:
        return executar_lote(idiomas, filtros, aplicar, verificar, retomar, max_falhas)
    with bloquear_lote():
        return executar_lote(idiomas, filtros, aplicar, verificar, retomar, max_falhas)


def executar_lote(idiomas, filtros, aplicar, verificar, retomar, max_falhas):
    if not PASTA_ORIGEM_EN.is_dir():
        raise RuntimeError(f"Pasta de origem não encontrada em: {PASTA_ORIGEM_EN}")
    arquivos = sorted(PASTA_ORIGEM_EN.rglob("*.md"))
    if filtros:
        selecionados = set()
        for filtro in filtros:
            caminho_seguro(PASTA_ORIGEM_EN, filtro)
            correspondentes = list(PASTA_ORIGEM_EN.glob(filtro))
            correspondentes = [p for p in correspondentes if p.is_file() and p.suffix == ".md"]
            if not correspondentes:
                raise ValueError(f"Filtro sem páginas Markdown: {filtro}")
            selecionados.update(correspondentes)
        arquivos = [p for p in arquivos if p in selecionados]
    if not arquivos:
        raise RuntimeError(f"Nenhum Markdown encontrado em: {PASTA_ORIGEM_EN}")
    idiomas = idiomas or list(IDIOMAS_SUPORTADOS)
    if any(idioma not in IDIOMAS_SUPORTADOS for idioma in idiomas):
        raise ValueError("Idioma de destino inválido.")
    print(f"Páginas: {len(arquivos)}; idiomas: {', '.join(idiomas)}; modo: {'aplicar' if aplicar else 'prévia'}.")
    # Pré-validação de todo o escopo antes de carregar o modelo ou gravar saídas.
    for arquivo in arquivos:
        origem = arquivo.read_text(encoding="utf-8")
        protegido, trechos = proteger_codigo(origem)
        if restaurar_codigo(protegido, trechos) != origem:
            raise RuntimeError(f"Proteção de código alterou a origem: {arquivo}; lote recusado antes da geração.")
    if verificar:
        print("Pré-validação concluída. Nenhum modelo carregado e nenhum arquivo alterado.")
        return 0

    trabalho = DIRETORIO_ATUAL / ".translations"
    trabalho.mkdir(exist_ok=True)
    manifesto_path = trabalho / "manifest.json"
    manifesto = json.loads(manifesto_path.read_text(encoding="utf-8")) if manifesto_path.exists() else {}
    versao = hashlib.sha256((str(hash_arquivo(Path(__file__))) + str(hash_arquivo(DIRETORIO_ATUAL / "technical_glossary.json.gz")) + model_id + MODEL_REVISION).encode()).hexdigest()
    sucessos = 0
    falhas = 0
    reutilizados = 0
    relatorio = {"started_utc": datetime.now(timezone.utc).isoformat(), "model": model_id, "model_revision": MODEL_REVISION, "fingerprint": versao, "mode": "apply" if aplicar else "preview", "results": []}
    for arquivo_md in arquivos:
        caminho_relativo = arquivo_md.relative_to(PASTA_ORIGEM_EN)
        source_hash = hash_arquivo(arquivo_md)
        conteudo_original = arquivo_md.read_text(encoding="utf-8")
        for tag_idioma in idiomas:
            chave = f"{tag_idioma}/{caminho_relativo.as_posix()}"
            arquivo_destino = caminho_seguro(RAIZ_WIKI / tag_idioma, caminho_relativo)
            previa = caminho_seguro(trabalho / "preview", chave)
            destino_hash = hash_arquivo(arquivo_destino)
            resultado = {"page": chave}
            print(f" -> {chave}")
            try:
                registro = manifesto.get(chave, {})
                if retomar and registro.get("source_hash") == source_hash and registro.get("fingerprint") == versao and registro.get("output_hash") and registro.get("output_hash") == hash_arquivo(previa):
                    conteudo_traduzido = previa.read_text(encoding="utf-8")
                    reutilizados += 1
                else:
                    if aplicar:
                        raise RuntimeError("Prévia ausente, alterada ou desatualizada. Gere e revise a prévia antes de usar --apply.")
                    conteudo_traduzido = traduzir_conteudo_wiki(conteudo_original, IDIOMAS_SUPORTADOS[tag_idioma], cache_dir=trabalho / "chunks" / versao / tag_idioma, reutilizar=retomar)
                    if hash_arquivo(arquivo_md) != source_hash:
                        raise RuntimeError("A origem mudou durante a tradução; execute novamente.")
                    previa.parent.mkdir(parents=True, exist_ok=True)
                    salvar_traducao(previa, conteudo_traduzido)
                    registro = {"source_hash": source_hash, "fingerprint": versao, "output_hash": hash_arquivo(previa), "destination_hash": destino_hash}
                    manifesto[chave] = registro
                    salvar_traducao(manifesto_path, json.dumps(manifesto, ensure_ascii=False, indent=2) + "\n")
                if aplicar:
                    if hash_arquivo(arquivo_md) != source_hash:
                        raise RuntimeError("A origem mudou; a prévia não será aplicada.")
                    if hash_arquivo(arquivo_destino) != registro["destination_hash"] and hash_arquivo(arquivo_destino) != registro["output_hash"]:
                        raise RuntimeError("O destino mudou desde a geração da prévia; não foi sobrescrito.")
                    arquivo_destino.parent.mkdir(parents=True, exist_ok=True)
                    if arquivo_destino.is_file() and hash_arquivo(arquivo_destino) != registro["output_hash"]:
                        backup = caminho_seguro(trabalho / "backups", f"{chave}.{hash_arquivo(arquivo_destino)}.bak")
                        backup.parent.mkdir(parents=True, exist_ok=True)
                        if not backup.exists():
                            backup.write_bytes(arquivo_destino.read_bytes())
                    salvar_traducao(arquivo_destino, conteudo_traduzido)
                sucessos += 1
                resultado["status"] = "applied" if aplicar else "preview"
            except Exception as e:
                falhas += 1
                resultado.update(status="failed", error=str(e))
                if isinstance(e, FalhaTraducao):
                    falha = caminho_seguro(trabalho / "failures", chave + ".json")
                    falha.parent.mkdir(parents=True, exist_ok=True)
                    salvar_traducao(falha, json.dumps(e.detalhes, ensure_ascii=False, indent=2) + "\n")
                    resultado["details"] = str(falha)
                print(f"    [ERRO] {e}")
            relatorio["results"].append(resultado)
            salvar_traducao(trabalho / "last-run.json", json.dumps(relatorio, ensure_ascii=False, indent=2) + "\n")
            if falhas >= max_falhas:
                print(f"Interrompido após {falhas} falhas. Consulte .translations/last-run.json.")
                return 1
    print(f"\nConcluídas: {sucessos}; reutilizadas: {reutilizados}; falhas: {falhas}.")
    return 1 if falhas else 0


def restaurar_backups(idiomas, filtros):
    if not idiomas or not filtros:
        raise ValueError("--restore exige --languages e --files explícitos.")
    trabalho = DIRETORIO_ATUAL / ".translations"
    manifesto = json.loads((trabalho / "manifest.json").read_text(encoding="utf-8"))
    with bloquear_lote():
        for idioma in idiomas:
            for relativo in filtros:
                destino = caminho_seguro(RAIZ_WIKI / idioma, relativo)
                registro = manifesto.get(f"{idioma}/{Path(relativo).as_posix()}")
                if not registro or not registro.get("destination_hash"):
                    raise RuntimeError(f"Não há backup registrado para {idioma}/{relativo}.")
                if hash_arquivo(destino) == registro["destination_hash"]:
                    print(f"Já restaurado: {destino}")
                    continue
                if hash_arquivo(destino) != registro["output_hash"]:
                    raise RuntimeError(f"O destino foi editado após a aplicação: {destino}")
                backup = caminho_seguro(trabalho / "backups", f"{idioma}/{Path(relativo).as_posix()}.{registro['destination_hash']}.bak")
                if hash_arquivo(backup) != registro["destination_hash"]:
                    raise RuntimeError(f"Backup ausente ou alterado: {backup}")
                # Preserva também CRLF/BOM do arquivo anterior.
                with backup.open("r", encoding="utf-8", newline="") as arquivo:
                    salvar_traducao(destino, arquivo.read())
                print(f"Restaurado: {destino}")
    return 0


def main():
    global model_id, MODEL_REVISION, pipe
    # O console padrão do Windows pode não representar húngaro, japonês etc.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Traduz os arquivos en/ para os 11 idiomas da wiki.")
    parser.add_argument(
        "--smoke-test", action="store_true",
        help="Traduz uma frase curta para húngaro sem gravar arquivos da wiki."
    )
    parser.add_argument("--languages", nargs="+", choices=IDIOMAS_SUPORTADOS, help="Idiomas selecionados; padrão: todos.")
    parser.add_argument("--model", choices=MODELOS, default="qwen", help="Modelo local com revisão fixada; padrão: qwen.")
    parser.add_argument("--files", nargs="+", help="Caminhos ou padrões relativos a en/, por exemplo 01-enforce-script/01-variables-types.md.")
    parser.add_argument("--check", action="store_true", help="Valida a origem sem carregar o modelo ou gravar arquivos.")
    parser.add_argument("--apply", action="store_true", help="Aplica traduções validadas à wiki, preservando backup do destino.")
    parser.add_argument("--restore", action="store_true", help="Restaura backups das páginas e idiomas explicitamente selecionados.")
    parser.add_argument("--doctor", action="store_true", help="Mostra ambiente, GPU e glossário sem baixar/carregar o modelo.")
    parser.add_argument("--term", help="Consulta um identificador e suas fontes no glossário, sem carregar o modelo.")
    parser.add_argument("--no-resume", action="store_true", help="Regenera prévias, ignorando o cache de traduções concluídas.")
    parser.add_argument("--max-failures", type=int, default=3, help="Encerra o lote após este total de falhas; padrão: 3.")
    args = parser.parse_args()
    if sum((args.apply, args.restore, args.check, args.smoke_test, args.doctor, bool(args.term))) > 1:
        parser.error("Escolha apenas um modo: --apply, --restore, --check ou --smoke-test.")
    if args.apply and args.no_resume:
        parser.error("--apply utiliza somente prévias existentes; não combine com --no-resume.")
    model_id, MODEL_REVISION = MODELOS[args.model]
    try:
        if args.doctor:
            return diagnosticar()
        if args.term:
            return consultar_termo(args.term)
        if args.restore:
            return restaurar_backups(args.languages, args.files)
        if args.smoke_test:
            exemplo = "# Hello\n\nOpen the inventory to inspect the item. You must start the server before connecting.\n\nPlayerBase extends ManBase. Call GetGame().\n\n```mermaid\ngraph TD\n    A[PlayerBase] --> B[EntityAI]\n```\n"
            trabalho = DIRETORIO_ATUAL / ".translations"
            trabalho.mkdir(exist_ok=True)
            recibo = {"model": model_id, "model_revision": MODEL_REVISION, "translator_sha256": hash_arquivo(Path(__file__)), "glossary_sha256": hash_arquivo(DIRETORIO_ATUAL / "technical_glossary.json.gz"), "source": exemplo, "started_utc": datetime.now(timezone.utc).isoformat(), "results": []}
            pipe = carregar_modelo()
            for idioma in args.languages or ["hu"]:
                try:
                    resultado = traduzir_conteudo_wiki(exemplo, IDIOMAS_SUPORTADOS[idioma], max_new_tokens=512)
                    assert "```mermaid\ngraph TD\n    A[PlayerBase] --> B[EntityAI]\n```" in resultado
                    assert all(termo in resultado for termo in ("PlayerBase", "ManBase", "GetGame", "EntityAI"))
                    recibo["results"].append({"language": idioma, "status": "passed", "output": resultado})
                    print(f"[{idioma}] {resultado}")
                except Exception as erro:
                    recibo["results"].append({"language": idioma, "status": "failed", "error": str(erro)})
                    print(f"[{idioma}] ERRO: {erro}")
                salvar_traducao(trabalho / f"smoke-{args.model}.json", json.dumps(recibo, ensure_ascii=False, indent=2) + "\n")
            return 1 if any(r["status"] == "failed" for r in recibo["results"]) else 0
        if args.max_failures < 1:
            parser.error("--max-failures deve ser positivo")
        return iniciar_traducao_em_massa(args.languages, args.files, args.apply, args.check, not args.no_resume, args.max_failures)
    except Exception as e:
        print(f"[ERRO] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
