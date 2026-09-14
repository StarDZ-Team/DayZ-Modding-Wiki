# Revisão independente do delta de palavras-chave

O parecer inicial abaixo é histórico. O adendo ao final registra os reparos posteriormente autorizados pelo coordenador, seus testes e novos hashes; essa entrega de autoria aguarda revisão independente do root.

Revisão limitada em 2026-09-14, task `task_7c51051c2321`, dispatch `ctx_1dc4df64e1fa`, checkout `99c011b4d3ded81f4b45c5f30f326de7e92075b3`. O hash-base `e546ee83b11bfa2ac09e7f9239f290dcc3500c1e3d5a352bf5292a2c3d4be711` foi consultado no recibo de `review-final.md`; não foi localizada uma cópia histórica desses bytes para diff binário. A revisão reabriu a implementação atual das alterações descritas no despacho, seus consumidores e o gerador do glossário. Somente este relatório foi escrito; sem edição de produção, testes, locales, GPU, rebuild do glossário ou commit.

---

## Resultado e achados concretos

**Aprovação integral retida: há perda reproduzível de whitespace na regra inversa, apesar dos 66 testes aprovados.** A ampliação lexical e a consulta manual funcionam nos contextos simples testados, mas a preservação de toda prosa não pode ser certificada.

- **RK-01 — média, aberto, `translator.py:232`: a regra inversa modifica a origem antes de qualquer tradução.** O padrão consome `\s+`, mas a substituição usa um espaço literal. `restaurar_codigo(*proteger_codigo('keyword  out'))` retorna `'keyword out'`; `'operators\tnew'` retorna `'operators new'`; `'keywords\n\nout'` retorna `'keywords out'`, fundindo dois parágrafos. Reprodução direta em CPU, sem pipeline. O mecanismo pode anteceder o delta, mas os novos termos e descritores o tornam aplicável a estes casos novos. Recomenda-se substituir somente o span do termo e preservar o separador exatamente; restringir o contexto à mesma linha também evita inferir contexto entre parágrafos. Acrescentar contratos de round trip para espaços duplos, tab e quebra de parágrafo antes de aceitar a correção.
- **RK-02 — média, aberto como concessão de precisão, `translator.py:231–232`: há prosa comum congelada mesmo com os contextos novos.** Na frase `'Use this class for storage.'`, o mapa contém `['this', 'for']`: `this` é o demonstrativo da frase e `for` é a preposição depois de `class`, mas são retirados da entrada do modelo como se fossem nomes de palavras-chave. O round trip preserva bytes, porém uma tradução natural pode precisar de ambos traduzidos. A causa é permitir `class` como descritor genérico antes/depois de qualquer candidato, incluindo `this` e `for`. Não invalida os três controles negativos pedidos, que passam; invalida uma afirmação mais ampla de que apenas usos técnicos reais ficam protegidos. Refinar combinações candidato/descritor, em especial contexto inverso com `class/classes`, ou manter essa limitação explicitamente aceita e recomendar crases para os usos técnicos. O STUDY já reconhece falsos positivos heurísticos; este é um caso concreto adicional causado pela lista ampliada.

Nenhum reparo foi realizado por este revisor. O coordenador deve decidir RK-02; RK-01 precisa de correção e nova verificação do arquivo efetivamente entregue.

---

## Verificação executada

Python `3.14.3`, na raiz da wiki:

```powershell
scripts/Translator/.env/Scripts/python.exe -B -m unittest discover -s scripts/Translator -p 'test_*.py'
scripts/Translator/.env/Scripts/python.exe -B scripts/Translator/translator.py --term out
```

A suíte informou **66 testes em 1,251 s, OK**. O comando de consulta concluiu com **exit 0**. Uma matriz adicional via stdin, sem arquivo de teste, verificou **1.456 pares**: os 26 termos novos × 28 descritores singulares/plurais × duas ordens, sempre com um espaço. Todos protegem o candidato e restauram exatamente a origem. Essa matriz verifica o mecanismo, não a validade semântica de todas as combinações.

Controles negativos: `'Go out and return later. An event starts here.'` permanece integralmente exposto ao modelo, com mapa vazio e round trip exato. Controle positivo: `'out parameters; sealed classes; return statements; new operators; event methods; thread keywords'` protege exatamente `out`, `sealed`, `return`, `new`, `event`, `thread` e restaura a origem. Os casos extras de RK-01 e RK-02 foram executados diretamente. Também se confirmou a sensibilidade à caixa: `'out Parameters'` e `'Keywords out'` ficam sem proteção; isso é limite heurístico, não prova de reconhecimento de todos os títulos.

`--term out` retornou `manual_rule: true`, `ambiguous: true`, `found: true`, categoria `config_key` e duas evidências em `D:/DayZ Projects/bin/config.cpp`, linhas 1104 e 1137. Ambas foram reabertas e contêm atribuições `out=...`; o hash real coincide com o inventário. **Essas ocorrências são chaves de configuração e não fundamentam o modificador de parâmetro.** A regra manual é identificada corretamente mesmo quando a evidência lexical pertence a outro uso. O comentário novo na lista esclarece que palavras de comparação entre linguagens não afirmam suporte nativo.

---

## Fontes reabertas e proveniência

- `D:/DayZ Projects/scripts/1_core/proto/enscript.c`, linhas 1–125: `Class.CastTo`, linha 110, declara `out Class to`; evidência lexical direta do modificador, sem ensaio de comportamento do parâmetro.
- `D:/DayZ Projects/scripts/1_core/physics/contact.c`, linhas 1–45: `sealed class Contact` na linha 9; evidência lexical direta. O caminho inicialmente tentado sob `proto/physics/` não existe e foi corrigido para este caminho efetivamente aberto.
- `en/01-enforce-script/13-functions-methods.md`: introdução, referências a `out`, seções `The event Keyword` e `Thread Methods (Coroutines)` reabertas; estabelecem o uso editorial dos nomes. Não foi reconfirmado aqui o modelo de agendamento nem todo o comportamento descrito pela página.
- `en/01-enforce-script/12-gotchas.md`: linhas iniciais, seções e tabelas de comparação localizadas e lidas por busca contextual, incluindo `try/catch/throw`, `do` e `sealed`; justificam preservar nomes ao comparar linguagens, sem converter essas comparações em alegação de suporte DayZ.
- `scripts/Translator/build_glossary.py`: leitura integral. Registra o hash dos bytes lidos antes da decodificação, caminho e tipo da fonte; preserva quebras de linha ao remover comentários/strings; mantém índice da fonte e linha na evidência; não escreve versão de jogo inventada. O limite de duas evidências e a coleta regex já documentados em STUDY continuam limitações. Categorias são acumuladas no termo, enquanto as duas evidências não são discriminadas por categoria; portanto não presumir que cada categoria tem declaração comprovada nas duas linhas exibidas. Não foi identificado novo defeito evidente de proveniência além dessas concessões conhecidas nesta inspeção limitada. Não foram auditadas individualmente as 3.875 fontes nem reconstruído o inventário.
- Reabertos `review-final.md`, `STUDY.md`, testes da proteção e orientação `CLAUDE.md`. O nome inicial tentado `03-functions-methods.md` não existe; a leitura usou `13-functions-methods.md`. Não foi necessária consulta web para este parecer lexical do código local; não se declara leitura nova de fontes web citadas por outros relatórios.

---

## Recibo SHA-256

Hashes dos arquivos efetivamente examinados/testados; aprovação não se transfere a alterações posteriores.

| Arquivo | SHA-256 |
| --- | --- |
| `scripts/Translator/translator.py` | `329536a08b60787291d55d47793e78de139c3c9622860149b5cf9d1bd054abb1` |
| `scripts/Translator/build_glossary.py` | `469be5d49637df0986f1094364341881515edcf83fafd3f5ef12db1163ff00fe` |
| `scripts/Translator/test_translator.py` | `f17e7b21b381b75a2d9541509c1c0ce365267c423e4f1b44828c5e5deb5b5dce` |
| `scripts/Translator/test_review_regressions.py` | `f7f2fbf100c864d838e05e935e4544f391f34b62fd892c51bdcea0c54641f85c` |
| `scripts/Translator/test_final_regressions.py` | `a82b0d2d78410cf201d15574c160ac45376645fd96eecaf491d014ab77e87644` |
| `scripts/Translator/technical_glossary.json.gz` | `fc2c1a39414cbe322e1944344e008215f03ed0d6b64e7c6e28a93ddfe4f67b96` |
| `D:/DayZ Projects/scripts/1_core/proto/enscript.c` | `1ca3897df3f842e6eaacb5e771a4a04ece1d77e2a7c987f0a8174351770b43d4` |
| `D:/DayZ Projects/scripts/1_core/physics/contact.c` | `320bd77b6446a3c986ca763c3a7efc0463ac8e8b89fb9b5aebfd3f8aeb915c4b` |
| `D:/DayZ Projects/bin/config.cpp` | `42b4cf95cf945b7f4164c69748ebab226c00e1e6e4de5f111a0d9f7754d37b6e` |
| `en/01-enforce-script/13-functions-methods.md` | `84a76f4c2982cf4e0f396c2ac9ee934cd3017820600fa5301404862dec3e704b` |
| `en/01-enforce-script/12-gotchas.md` | `55aa05df8b89eee5f6374adb02b2cc74ef80f64b2ac710a577e9b6f7d66ee09f` |

Validação limitada a código Python e fixtures CPU; nenhum resultado aqui comprova tradução real, compilação Enforce, comportamento em jogo ou build VitePress.

---

## Adendo de autoria: reparos RK-01 e RK-02

Task `task_bacb7b87b60c`, dispatch `ctx_f0f5ab25afb6`, 2026-09-14, mesmo checkout. O coordenador aceitou ambos os achados para reparo e autorizou alterações somente em `translator.py`, `test_translator.py` e neste relatório. Os três arquivos foram alterados; sem GPU, alterações de locales, reconstrução de glossário ou commit. Este adendo não é aprovação independente do próprio reparo.

**RK-01 implementado:** os padrões de contexto usam somente espaço/tab (`[ \t]`) como separador. A regra inversa captura e reinsere o separador exato, preservando tabs e espaços múltiplos. Os padrões de configuração e de nomes após `Call`/`Invoke`/`method`/`function` também foram limitados à mesma linha para que outro caminho de reconhecimento não reintroduza contexto entre linhas. Não foram modificados os marcadores, sua validação ou o parser Markdown.

**RK-02 implementado:** palavras de controle/comparação comuns, incluindo `this`, `for`, `new`, `default` e `return`, exigem os descritores textuais `keyword`, `statement` ou `operator` (singular/plural), além da sintaxe explícita já reconhecida de parênteses, colchetes e atribuição. Os demais ambíguos mantêm os descritores técnicos anteriores, mas `class/classes` fica em uma regra específica limitada a modificadores `sealed`, `abstract`, `static`, `private`, `protected`, `public`, nas duas ordens. Assim `class for` e `class out` não protegem preposições. Candidatos ambíguos deixam de passar pela regra genérica de chaves de configuração, evitando que a categoria `config_key` de `default`, por exemplo, contorne a restrição textual; a sintaxe explícita de atribuição continua disponível na regra de ambíguos.

Cinco testes novos cobrem separadores horizontais exatos, ausência de contexto através de LF/CRLF/quebras duplas nas duas ordens, frases comuns integralmente expostas, palavras comuns com os três descritores inequívocos e manutenção de `out parameters`, `sealed class/classes`, `thread keywords`, `event methods`. As expectativas de palavras comuns são uma lista literal independente da constante de produção. Os testes existentes de marcadores e estrutura continuam inalterados.

Verificação final na raiz, Python 3.14.3:

```powershell
scripts/Translator/.env/Scripts/python.exe -B -m unittest discover -s scripts/Translator -p 'test_*.py'
```

**71 testes, 1,081 s, OK** na execução final; a primeira execução após o reparo também aprovou 71 testes. Nenhum teste foi ignorado ou marcado como falha esperada.

Executado também, via stdin no mesmo Python com `-B`, round trip de **105/105 arquivos `en/**/*.md`**, lendo bytes, decodificando UTF-8 sem normalização de quebras de linha e exigindo `restaurar_codigo(*proteger_codigo(source)).encode('utf-8') == raw`. Todos passaram; não houve gravação de páginas. O corpus foi identificado por um manifesto em memória: `sorted(Path('en').rglob('*.md'))`, lista de objetos com chaves `path` (POSIX) e `sha256` dos bytes, serializada com `json.dumps(manifest, ensure_ascii=False, separators=(',', ':')).encode('utf-8')`; SHA-256 desse manifesto: `0e5f930681faa87878cd2719bd962912d6172253bb556f394582ff71a0feb94f`. Não foi criado arquivo auxiliar fora do escopo autorizado.

| Arquivo entregue/testado | SHA-256 final |
| --- | --- |
| `scripts/Translator/translator.py` | `45786f30fc59ecc31a453973250658da31b5e2b9626968d6bf59ef82da2e6192` |
| `scripts/Translator/test_translator.py` | `f9b7c88c46dc404e5d7d7494922fba71f7e06b13a04e31f4aba22e769075aba8` |
| `scripts/Translator/test_review_regressions.py` | `f7f2fbf100c864d838e05e935e4544f391f34b62fd892c51bdcea0c54641f85c` |
| `scripts/Translator/test_final_regressions.py` | `a82b0d2d78410cf201d15574c160ac45376645fd96eecaf491d014ab77e87644` |
| `scripts/Translator/technical_glossary.json.gz` | `fc2c1a39414cbe322e1944344e008215f03ed0d6b64e7c6e28a93ddfe4f67b96` |

Disposition de autoria: RK-01 e RK-02 reparados nos casos reproduzidos e entregues para revisão independente do root. Os testes de round trip comprovam reversibilidade, não que todo token selecionado tem sentido técnico nem fidelidade de tradução. Permanecem os limites heurísticos documentados, incluindo sensibilidade à caixa, nomes fora dos contextos reconhecidos e ambiguidades semânticas não cobertas pelas fixtures.

---

## Adendo de autoria: guarda de igualdade antes da geração

Task `task_f8b5237b005b`, dispatch `ctx_8a1897e63594`, 2026-09-14. Alterados somente `translator.py`, `test_translator.py` e este relatório; sem GPU ou commit. A configuração VitePress foi apenas lida.

`traduzir_conteudo_wiki` agora compara explicitamente `restaurar_codigo(texto_protegido, protegidos)` com `texto_original` imediatamente após proteger a origem e antes de acessar/carregar a pipeline. Uma diferença dispara `RuntimeError` com mensagem `Proteção de código alterou a origem; tradução recusada antes da geração.` A pré-validação de `executar_lote`, compartilhada com `--check`, faz a mesma comparação com a string de origem que leu e inclui o caminho da página no erro. Essa validação ocorre antes da criação do diretório de trabalho, cache e saídas do lote. Continua sendo igualdade exata de strings; `read_text` na leitura do lote mantém a normalização de quebras de linha preexistente, sem mudança de política de leitura neste reparo.

Dois testes novos simulam `proteger_codigo` retornando texto alterado com mapa vazio (a restauração real aceita esse mapa, mas a nova igualdade deve recusar a alteração). O teste da função verifica exceção explícita, loader e escritor nunca chamados e nenhum diretório de cache criado. O teste CLI chama `main()` com `--check --languages pt` numa árvore temporária, exige retorno 1 e mensagem com caminho, verifica loader/escritor nunca chamados, bytes da página intactos e ausência de novos arquivos. Nenhum comportamento de GPU foi simulado como execução real.

Verificação final, Python 3.14.3, na raiz:

```powershell
scripts/Translator/.env/Scripts/python.exe -B -m unittest discover -s scripts/Translator -p 'test_*.py'
scripts/Translator/.env/Scripts/python.exe -B scripts/Translator/translator.py --check --languages pt
```

Resultado: **73 testes em 1,434 s, OK, exit 0**; pré-validação real das **105 páginas EN concluída**, sem carregar modelo ou alterar arquivos. A nova guarda passou sobre o corpus atual; isso não comprova fidelidade de traduções nem substitui revisão independente da implementação.

### Leitura da exclusão VitePress

O acréscimo do root em `.vitepress/config.mts:188`, `srcExclude: [..., 'scripts/Translator/**']`, é **adequado ao objetivo de remover esse utilitário e seus descendentes da descoberta de páginas Markdown**. A configuração não define `srcDir` alternativo. Reabri a implementação instalada do VitePress **1.6.4**, `node_modules/vitepress/dist/node/chunk-D3CUZ4fa.js:17135–17146`: `resolvePages` usa glob de Markdown com `cwd: srcDir` e inclui `...userConfig.srcExclude` na lista `ignore`. A declaração `srcExclude?: string[]` também foi reaberta em `dist/node/index.d.ts:2222`. A exclusão cobre a árvore do tradutor para essa finalidade; não é uma regra genérica de segurança ou remoção de assets explicitamente importados. Não executei build VitePress nem validei o site renderizado nesta tarefa; essa verificação integrada permanece com o root.

| Arquivo entregue ou reaberto | SHA-256 |
| --- | --- |
| `scripts/Translator/translator.py` | `a45f792bc74166ac73d62693f3562788d4940581d41f2daeb2062077d4ea1c79` |
| `scripts/Translator/test_translator.py` | `f58bbd68b44917ca19dd8ca8ae09ffd057fd4d42f7759f7d690e4555d52d89c1` |
| `.vitepress/config.mts` (somente leitura) | `21fd4557992a4b9319da9db6ef6ea6dce62ecde0d552239c6d176099acc812dd` |
| `node_modules/vitepress/dist/node/chunk-D3CUZ4fa.js` (somente leitura) | `07d45c356e7c850c2454904949f4b0b95c1d4a2d92119cbdaf4d419ae20dde98` |

Entrega de autoria concluída; guarda e testes aguardam revisão independente do root nos hashes acima.

## Aceitação independente pelo coordenador

O root reabriu as regras contextuais, a preservação do separador, os dois pontos de guarda e os testes das entregas. Executou novamente 73 testes (OK), --check das 105 páginas e roundtrip em bytes das 105 fontes; aceitou RK-01, RK-02 e a guarda no script `a45f792bc74166ac73d62693f3562788d4940581d41f2daeb2062077d4ea1c79`. Revalidou também os 11 resultados gravados do smoke test com os validadores finais; isso não transforma o snapshot de geração anterior em nova execução GPU nem certifica sua semântica. Todos os workers desse trabalho foram liberados após as entregas aceitas. Resultados integrados são registrados em validation.json.
