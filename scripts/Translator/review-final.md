# Revisão independente final do tradutor

Revisão em 2026-09-14, no checkout `7dd37924983a71a7835c5a926b9cd7b284a84a3d`, com mudanças locais concorrentes do coordenador. Foram editados somente este relatório e `test_final_regressions.py`; nenhum arquivo de produção, locale ou documento da wiki foi alterado por este worker. Nenhuma GPU, tradução real, build da wiki ou commit foi executado.

---

## Fontes reabertas e método

Leitura direta de `translator.py`, `test_translator.py`, `test_review_regressions.py`, `README.md` desta pasta e `CLAUDE.md` da raiz. O glossário real foi carregado pelos testes de proteção; isto não constitui auditoria da origem de todos os seus identificadores. A revisão é do programa local e não formula novas afirmações sobre APIs do jogo.

O comando literal solicitado, `.env/Scripts/python.exe -m unittest discover -s scripts/Translator -p test_*.py`, falhou na raiz porque ali não existe esse executável. Executado o equivalente com caminho real, `scripts/Translator/.env/Scripts/python.exe -m unittest discover -s scripts/Translator -p test_*.py`, na raiz da wiki, com Python 3.14.3: baseline 49 testes, sucesso; após os 11 novos testes, 60 testes, **exit 1, uma falha e quatro erros de subtestes**. Após reparos do coordenador, a execução final teve **60 testes, 1,018 s, OK, exit 0**. Os testes são contratos normais, não `expectedFailure` nem testes ignorados.

As fixtures de geração são determinísticas e usam arquivos temporários. A validação de idioma é simulada nessas fixtures; somente `RealLanguageContracts` executa o detector Lingua real, em CPU. O carregamento de modelo é explicitamente proibido nos testes de geração.

---

## Achados reproduzíveis

- **RF-01 — cache JSON com tipo inválido não se recupera.** `CacheContracts.test_corrupt_chunk_is_regenerated` grava um trecho válido e substitui seu JSON por `null`, `[]`, `{"sha256":"x","output":null}` ou `{"sha256":"x","output":123}`. Na leitura do cache em `traduzir_conteudo_wiki`, o acesso a `salvo["sha256"]` produz `TypeError`, ou `salvo["output"].encode()` produz `AttributeError`; o tratamento atual captura somente `KeyError`, `ValueError` e `RuntimeError`. O lote falha em vez de regenerar o trecho; não foi observada publicação do conteúdo corrompido. Recomenda-se validar explicitamente o objeto e os campos antes de reutilizar, e regenerar qualquer entrada com esquema inválido. JSON sintaticamente inválido, objeto vazio e bytes UTF-8 inválidos já se recuperaram no mesmo teste.
- **RF-02 — alinhamento de tabela pode mudar sem rejeição.** `StructureContracts.test_table_alignment_change_is_rejected` substitui a linha `| :--- | ---: |` por `| ---: | :--- |` na resposta simulada. A tradução é aceita, embora inverta o alinhamento das duas colunas. `validar_estrutura` compara tipo/tag/nesting e ignora os atributos de alinhamento dos tokens `th_open`/`td_open`. Recomenda-se incluir os atributos estruturais relevantes na assinatura; o teste espera rejeição da alteração.

Os dois achados foram enviados ao coordenador para correção em produção, cuja edição está fora da autorização deste worker. O coordenador corrigiu ambos: reabri o código final e confirmei a verificação explícita de `dict`/`output` como `str` antes de reutilizar cache, e a inclusão de `t.attrs` na assinatura dos blocos Markdown. Os respectivos testes passaram sem alteração de suas expectativas; **RF-01 e RF-02 estão resolvidos na revisão final identificada abaixo**. Não foram repetidos os achados sobre HR ou Titlecase que o coordenador já estava corrigindo.

---

## Evidência positiva e limites

- Cache ausente é regenerado; cache válido é reutilizado sem nova chamada ao pipeline simulado; hash válido com marcador protegido ausente é recusado e regenerado.
- Restauração recupera exatamente os bytes UTF-8 com BOM, acentos e CRLF, e a segunda restauração é idempotente. Destino editado e backup corrompido são recusados sem modificar o destino nesses cenários.
- Um segundo escritor que utiliza o lock é recusado; uma exceção libera o lock do primeiro escritor. O teste usa aquisição aninhada no mesmo processo, não processos concorrentes nem falha abrupta do sistema operacional. Editores externos não são coordenados por esse lock; verificações de hash e substituição atômica não demonstram ausência de todas as corridas externas.
- O bloco Mermaid com CRLF permanece exato na tradução simulada e seu corpo não alcança o pipeline; `PlayerBase` e `GetGame()` são preservados. Remoção de blockquote ou ênfase é recusada.
- O detector real recusa o parágrafo longo em inglês destinado a português e aceita a amostra portuguesa. `Hello` é curto demais e passa sem detecção, como documenta o teste: sucesso da função nessa amostra **não é verificação de idioma**.
- Preservação de marcadores, forma Markdown e detecção de idioma não demonstram fidelidade semântica universal: negações, qualificações, dependências e correspondência entre instruções ainda exigem revisão humana de prévias. Nenhum teste aqui valida traduções reais nos onze idiomas, comportamento de modelo/GPU, compilação de exemplos ou funcionamento no jogo.
- O caminho de cache ainda carrega o modelo/tokenizer quando `pipe` é `None`, antes de examinar todos os trechos; reutilização testada significa ausência de nova geração, não garantia de reconstrução sem carregar o modelo.

---

## SHA-256 dos arquivos revisados

Recebidos após o comando final de 60 testes aprovados. A reprodução inicial usou `translator.py` SHA-256 `60602eef190101474b9f01be4961a0054f62c25cadc473394cc61eec777b617f`; a tabela identifica a versão corrigida reaberta e testada. Mudanças posteriores nesses arquivos exigem novo teste e recibo; aprovação não se transfere automaticamente a revisões futuras.

| Arquivo nesta pasta | SHA-256 |
| --- | --- |
| `translator.py` | `e396ce2760eadd225a67db1a8372d6e44fecd305dda32b92b82cb63ba760df80` |
| `test_translator.py` | `fba9e1dde426aa2cbe878a1839bb8fc1b85e8dd5d1dd32dbed60878aba29fa01` |
| `test_review_regressions.py` | `f7f2fbf100c864d838e05e935e4544f391f34b62fd892c51bdcea0c54641f85c` |
| `test_final_regressions.py` | `57f2292a449407a8c26ba8be159c696624cac691fb48a88aa863a0e038977d7f` |
| `technical_glossary.json.gz` | `fc2c1a39414cbe322e1944344e008215f03ed0d6b64e7c6e28a93ddfe4f67b96` |

Disposition: RF-01 e RF-02 reproduzidos, corrigidos pelo coordenador e aceitos após reabertura do código e novo teste; demais resultados positivos limitados às fixtures descritas. Nenhum achado reproduzido permanece aberto neste escopo restrito; os limites de idioma, semântica, carregamento do modelo e concorrência continuam explícitos.

---

## Adendo de implementação: duas tentativas por trecho

Nova tarefa `task_59dcd6c1d070`, dispatch `ctx_8802db393146`, em 2026-09-14. Este adendo é uma entrega de autoria para revisão independente do coordenador, não aprovação independente do próprio código. A autorização passou a incluir `translator.py`; somente ele, `test_final_regressions.py` e este adendo foram modificados nesta tarefa, sem GPU, commit ou escrita em locales.

Reabri a falha real `.translations/failures/pt/01-enforce-script/01-variables-types.md.json`: o trecho 3 contém `WIKICODE62EA48ED2BX74X` na origem protegida, ausente na resposta registrada. Esse recibo motivou a repetição limitada; não executei novamente essa geração nem declarei sua tradução corrigida.

`traduzir_conteudo_wiki` agora permite até duas gerações por trecho. A configuração real de geração usa seed 42 na primeira e 43 na segunda; o segundo prompt informa o erro de validação e solicita regeneração integral da mesma origem, sem reutilizar a resposta rejeitada. Marcador final, resposta vazia, cercas inventadas, estrutura e preservação dos tokens continuam verificados; nenhum token é reparado automaticamente e nenhuma regra é relaxada. A verificação de cercas inventadas também ocorre antes da gravação do cache do trecho.

Somente erros da validação da resposta entram nesse laço. Carregamento do modelo, geração/pipeline (incluindo OOM), acesso a arquivos e validações finais da página não são repetidos indiscriminadamente. A segunda rejeição gera `FalhaTraducao.detalhes` com `attempt: 2`, `seed: 43`, a resposta final bruta e `attempts` contendo as duas respostas brutas, erros, números de tentativa, seeds, idioma, trecho e origem protegida. Cache e lista de traduções só recebem a resposta depois de aprovada nas validações do trecho; a publicação da página continua dependente das validações finais existentes.

Foram acrescentados cinco testes offline: recuperação após ausência do marcador final, mudança estrutural ou perda de token (subcasos com seeds 42/43 e origem idêntica); duas rejeições com recibos completos e nenhum cache; OOM do pipeline sem repetição; falha de carregamento sem repetição; e lote com duas respostas inválidas sem prévia, cache ou alteração do destino. A primeira execução encontrou um erro de posicionamento de duas asserções no próprio teste de restauração; ele foi corrigido preservando as asserções originais.

Verificação final na raiz, Python 3.14.3: `scripts/Translator/.env/Scripts/python.exe -m unittest discover -s scripts/Translator -p test_*.py` — **65 testes em 1,005 s, OK, exit 0**. O módulo `transformers` e `set_seed` são simulados nos testes de retry; isso verifica o despacho das seeds e não comportamento estocástico real do modelo. Continuam válidos os limites semânticos e de idioma descritos acima; uma segunda tentativa não garante uma tradução correta.

| Entrega para revisão independente | SHA-256 |
| --- | --- |
| `translator.py` | `e546ee83b11bfa2ac09e7f9239f290dcc3500c1e3d5a352bf5292a2c3d4be711` |
| `test_final_regressions.py` | `a82b0d2d78410cf201d15574c160ac45376645fd96eecaf491d014ab77e87644` |
