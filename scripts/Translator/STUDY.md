# Estudo do tradutor e das proteções

Este estudo registra a leitura do código e das fontes em **2026-09-14**. O objetivo é preservar conteúdo técnico enquanto você traduz prosa. O inventário lexical, a detecção de idioma e as verificações estruturais têm funções distintas; nenhuma delas comprova fidelidade integral da tradução.

---

## Corpus lexical e proveniência

O arquivo `technical_glossary.json.gz` lido contém **93.118 candidatos lexicais em 3.875 fontes**, gerados em `2026-09-14T05:14:53.857757+00:00`:

| Categoria | Arquivos | Origem e interpretação |
|---|---:|---|
| `wiki` | 105 | Código marcado nas páginas EN; exemplos documentais, não comportamento comprovado |
| `extracted_script` | 2.810 | Scripts `.c` em `D:/DayZ Projects/scripts` |
| `extracted_config` | 209 | `config.cpp` na extração local, excluindo caminhos com componente `SteamLibrary` |
| `user_mod` | 730 | Scripts dos diretórios `D:/StarDZ/StarDZ_*` |
| `user_mod_config` | 21 | Configurações desses mods beta; implementações que também podem conter erros |

O gerador [build_glossary.py](build_glossary.py) remove comentários e strings dos segmentos analisados e usa expressões regulares para tipos declarados, chamadas declaradas, identificadores com grafia técnica e chaves de configuração. Na wiki, seleciona código cercado por três crases e código inline reconhecidos pelo padrão do gerador; isso não é uma varredura de toda sintaxe Markdown possível. Chaves também são extraídas dos blocos `cpp` reconhecidos. O inventário não é um parser completo de Enforce Script nem uma lista de APIs todas verificadas.

Cada fonte registra caminho, categoria e SHA-256; cada termo registra categorias e até **duas** evidências com índice da fonte e linha. As duas evidências não representam todas as ocorrências e não precisam ser fontes independentes. O campo `game_version` declara versão desconhecida; hashes identificam os arquivos locais, sem estabelecer versão oficial do jogo. O número de candidatos não mede cobertura completa, correção ou validade de API.

Você pode consultar a proveniência com `translator.py --term Print`. Para reconstruir o inventário a partir das fontes locais disponíveis:

```powershell
.\.env\Scripts\python.exe build_glossary.py --game-root 'D:/DayZ Projects' --mod-root 'D:/StarDZ'
```

A reconstrução altera o glossário e invalida a identidade das prévias/cache anteriores. A data de geração também faz parte do conteúdo serializado. Nenhuma reconstrução foi executada nesta revisão documental.

---

## Fontes locais efetivamente abertas

Foram lidos [translator.py](translator.py), [build_glossary.py](build_glossary.py), [review-protection.md](review-protection.md) e [WORKLOG.md](WORKLOG.md), além dos metadados do inventário. O checkpoint do WORKLOG lido nessa etapa ainda apresentava Llama como padrão e 93.115 candidatos; o registro foi atualizado depois na integração. O código e o inventário aqui examinados já usam Qwen e 93.118 candidatos. Os achados RP-01 a RP-09 descrevem revisões anteriores; não representam automaticamente defeitos atuais nem aprovação do código posterior.

Duas fontes DayZ foram reabertas diretamente para distinguir ocorrência de afirmação comportamental:

| Arquivo local | Trecho aberto | Evidência limitada |
|---|---|---|
| `D:/DayZ Projects/scripts/1_core/proto/endebug.c` | Linhas 83–105; `Print` na 96 | Declaração `proto void Print(void var);` |
| `D:/StarDZ/StarDZ_Core/StarDZ_Core/Scripts/config.cpp` | Linhas 1–43; `inputs` na 22, `dependencies` na 26, `prefabs.imageset` na 37 | Uso real em configuração beta, sem validação de comportamento nativo |

Hashes SHA-256 dos arquivos examinados:

```text
translator.py
60602eef190101474b9f01be4961a0054f62c25cadc473394cc61eec777b617f
build_glossary.py
469be5d49637df0986f1094364341881515edcf83fafd3f5ef12db1163ff00fe
technical_glossary.json.gz
fc2c1a39414cbe322e1944344e008215f03ed0d6b64e7c6e28a93ddfe4f67b96
D:/DayZ Projects/scripts/1_core/proto/endebug.c
ca3151514781ced9355bf1e2f095f98d984764091d5fa51d621bd099f51ea746
D:/StarDZ/StarDZ_Core/StarDZ_Core/Scripts/config.cpp
faf4136778bd63623a61a1d26df1b192052cd4001ff95d8858b3faaae96dffc9
```

Esses recibos identificam a leitura, não aprovam futuras alterações. A presente revisão não leu manualmente as 3.875 fontes nem testou seus exemplos no jogo.

---

## Proteção e suas concessões

O tradutor retira spans protegidos da entrada do modelo e exige a mesma sequência de marcadores antes de restaurá-los. Usa tokens e mapas de linhas Markdown para reconhecer blocos, além de regras para código inline, frontmatter, HTML, diretivas, destinos de links, referências, caminhos, identificadores e quantidades. As verificações comparam estruturas de blocos, elementos inline e listas, e rejeitam respostas muito curtas em situações específicas. A documentação do [markdown-it-py, Using markdown_it](https://markdown-it-py.readthedocs.io/en/latest/using.html), efetivamente lida nas seções de parser e fluxo de tokens, descreve `type`, `nesting`, `children` e `map`. Esse parser não reproduz por si só todas as extensões e rotas do VitePress.

Blocos inteiros cercados ou indentados permanecem como na origem, **inclusive comentários e rótulos em inglês**. O mesmo vale para blocos Mermaid protegidos. Essa é uma concessão do tradutor atual frente à regra editorial de traduzir comentários: tradução desses conteúdos exige trabalho específico e revisão. A documentação oficial [Mermaid Flowcharts — Basic Syntax](https://mermaid.js.org/syntax/flowchart.html), seções de nós, texto e direção, distingue identificadores, rótulos e comandos como `flowchart`/`graph` e `TD`. Preservar o bloco reduz exposição da sintaxe ao modelo, mas também preserva defeitos existentes; não é uma execução do renderizador.

Termos como `class`, `string`, `native`, `true`, `Set` e `Value` podem ser prosa ou código. A lista de ambíguos e os padrões de contexto tentam preservar usos técnicos explícitos, por exemplo junto de parênteses, atribuição ou palavras como `keyword`. Isso é uma heurística, sensível a grafia e contexto: pode deixar nomes expostos ou congelar palavras comuns. Use crases para identificar código de forma editorialmente explícita; não congele todo o dicionário na prosa.

Destinos de links são preservados, sem converter links absolutos EN para outro locale. O código adiciona âncoras explícitas derivadas dos títulos EN à saída. Referências abreviadas podem exigir preservação do próprio rótulo porque ele também funciona como chave. Revise navegação, rótulos e destinos renderizados separadamente.

---

## Modelo, geração e detector

O código seleciona por padrão `Qwen/Qwen3-8B`, revisão `b968826d9c46dd6066d109eabc6255188de91218`, com quantização NF4 em 4 bits na GPU CUDA 0. Na pipeline real, configura `enable_thinking=False`, amostragem com temperatura `0.7`, `top_p=0.8`, `top_k=20` e sementes 42/43 para até duas tentativas totais por trecho. A segunda tentativa recebe feedback do erro e regenera o trecho original; somente rejeições de validação do trecho acionam a repetição. Erros da pipeline, como falta de memória, e falhas da validação final da página não repetem por esse mecanismo. A semente não garante resultados idênticos entre versões de bibliotecas e hardware.

O [model card oficial Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B), seções Non-Thinking Mode e Best Practices, recomenda esses três valores para modo sem thinking e também menciona `min_p=0`. O tradutor configura explicitamente os três primeiros. A tentativa de abrir o README na revisão fixada foi recusada pela ferramenta web; foi lido o card público corrente. Portanto a fonte web fundamenta a recomendação, mas não é apresentada como leitura do card naquele commit específico.

Llama permanece alternativa com `--model llama`, revisão `0e9e39f249a16976918f6564b8830bc894c89659`. O WORKLOG relata que uma amostra pedida em japonês saiu em português. Trata-se de resultado anterior reportado, não reproduzido neste estudo; a escolha de Qwen não implica certificação de todos os idiomas.

O tradutor verifica o idioma da prosa protegida ao final, restringindo o Lingua ao inglês e aos 11 idiomas de destino. No código examinado, amostras com menos de 10 letras para JA, ZH e RU, ou 40 para os demais, não são verificadas. A documentação primária [Lingua Python](https://github.com/pemistahl/lingua-py), seções Minimum Relative Distance e Confidence Values, explica seleção de idioma e dependência da extensão da amostra. A documentação consultada é corrente, sem commit fixado; o pacote local é `2.2.0`.

O detector não compara sentido com o EN, não mede fidelidade, não comprova ausência de frases em outro idioma e não distingue necessariamente todas as variantes desejadas, como português brasileiro ou chinês simplificado. Passar por ele não prova preservação de negações, condições, dependências ou instruções. Marcadores, proporção de comprimento e estruturas também não detectam toda omissão ou alteração semântica. Prévias exigem revisão humana.

---

## Ambiente, acesso e validação

Python `3.14.3` foi confirmado pelo executável do venv. `pip list --format=json` forneceu as versões instaladas, sem leitura ou exposição de tokens. [requirements.txt](requirements.txt) fixa o snapshot dos pacotes, inclusive dependências transitivas, exceto PyTorch e ferramentas de instalação; o comando CUDA separado está no [README](README.md). O [guia oficial PyTorch](https://pytorch.org/get-started/locally/) e o [índice de wheels cu130](https://download.pytorch.org/whl/cu130/torch/) foram abertos. Isso não constitui instalação limpa reproduzida nem teste de GPU nesta revisão.

Todas as fontes web vinculadas acima foram acessadas em 2026-09-14. O WORKLOG registra HTTP 403 em tentativas anteriores nas páginas Bohemia DayZ Enforce Syntax e Modding Structure; não houve nova leitura dessas páginas neste estudo e nenhum conteúdo inacessível é citado como evidência. A extração local fornece evidência lexical com versão do jogo desconhecida.

Este trabalho documental não executou geração GPU, testes de regressão, compilação DayZ ou build VitePress. Resultados históricos de review-protection e WORKLOG se aplicam aos respectivos snapshots. A tradução real da página PT, revisão final e verificações integradas ficam sob responsabilidade do coordenador e devem ter recibos próprios. Nem a leitura do corpus nem um build documental autorizam promessa de 100% de correção.

Leitura complementar após a alteração concorrente: foram reabertos o cache e o laço de geração de `translator.py`, confirmando checagem do formato do cache e duas tentativas de validação por trecho. SHA-256 nessa leitura: `e546ee83b11bfa2ac09e7f9239f290dcc3500c1e3d5a352bf5292a2c3d4be711`. O primeiro hash acima identifica a leitura inicial, anterior a esse refinamento.
