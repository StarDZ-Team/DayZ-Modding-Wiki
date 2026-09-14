# Tradutor local da wiki

Você traduz a prosa de `en/` para os 11 outros idiomas com proteção técnica e recuperação por backup. **A prévia é o padrão; revise-a antes de aplicar.** As verificações automáticas não comprovam fidelidade semântica. Consulte [STUDY.md](STUDY.md) para fontes, decisões e limites.

---

## Ambiente e instalação

Execute os exemplos no PowerShell, dentro de `scripts/Translator`. A pasta `.env` existente é um ambiente virtual Python, não um arquivo de credenciais. Use seu executável diretamente, sem ativação:

```powershell
Set-Location D:\StarDZ\docs\wiki\scripts\Translator
.\.env\Scripts\python.exe --version
```

O ambiente observado em 2026-09-14 usa Python **3.14.3**, PyTorch **2.14.0+cu130**, Transformers **5.17.0** e bitsandbytes **0.50.2**. Os demais pacotes estão fixados em [requirements.txt](requirements.txt). Em outra instalação, crie `.env` com essa versão do Python somente se a pasta ainda não existir. Instale o PyTorch pelo índice CUDA separado antes dos demais pacotes:

```powershell
.\.env\Scripts\python.exe -m pip install torch==2.14.0+cu130 --index-url https://download.pytorch.org/whl/cu130
.\.env\Scripts\python.exe -m pip install -r requirements.txt
.\.env\Scripts\python.exe -m pip check
```

Esses pins registram o ambiente local; a instalação limpa não foi reproduzida nesta revisão documental. Você precisa de GPU NVIDIA com driver compatível. O script exige CUDA e usa a GPU 0, quantização NF4 em 4 bits, dupla quantização e cálculo BF16 quando disponível, FP16 caso contrário. Consulte o [guia PyTorch](https://pytorch.org/get-started/locally/) e o [índice CUDA 13.0](https://download.pytorch.org/whl/cu130/torch/).

O padrão é `Qwen/Qwen3-8B`, revisão `b968826d9c46dd6066d109eabc6255188de91218`. O download inicial usa o cache Hugging Face. A opção `--model llama` seleciona `meta-llama/Llama-3.1-8B-Instruct`, revisão `0e9e39f249a16976918f6564b8830bc894c89659`, e requer acesso autorizado ao modelo. O cliente usa a autenticação existente; não copie tokens para comandos ou relatórios. O checkpoint registra uma amostra Llama pedida em japonês que saiu em português; isso não valida JA.

---

## Diagnóstico, consulta e filtros

```powershell
.\.env\Scripts\python.exe translator.py --doctor
.\.env\Scripts\python.exe translator.py --term Print
.\.env\Scripts\python.exe translator.py --check --languages pt --files '01-enforce-script/01-variables-types.md'
```

`--doctor` informa Python, pacotes, CUDA, GPU, modelo e inventário sem baixar/carregar o modelo. Só informa se há token configurado, nunca seu valor; retorna 1 quando CUDA está indisponível. `--term` consulta a grafia exata, categorias e evidências; retorna 1 se não houver entrada nem regra manual. Ocorrência lexical não comprova uma API.

`--check` verifica proteção/restauração das origens selecionadas sem carregar modelo ou gravar arquivos. Não testa tradução, links renderizados ou comportamento DayZ.

Use `--languages pt de` para selecionar idiomas entre `pt de ru es fr ja zh-hans cs pl hu it`; sem filtro, seleciona todos. `--files` aceita caminhos e globs relativos a `en/`, unindo resultados. Coloque padrões entre aspas:

```powershell
.\.env\Scripts\python.exe translator.py --check --languages pt de --files '01-enforce-script/*.md' 'glossary.md'
```

Filtros sem páginas Markdown ou fora de `en/` são recusados. Sem `--files`, todas as páginas EN entram no escopo.

---

## Gerar, revisar e aplicar

1. Gere uma prévia pequena primeiro. Este comando usa GPU e pode baixar o modelo:

```powershell
.\.env\Scripts\python.exe translator.py --languages pt --files '01-enforce-script/01-variables-types.md' --max-failures 1
```

2. Compare `.translations/preview/pt/01-enforce-script/01-variables-types.md` com `../../en/01-enforce-script/01-variables-types.md`. Revise instruções, condições, negações, números, omissões, termos, tabelas e navegação. Leia `.translations/last-run.json`. A revisão humana é uma etapa de trabalho; o programa não registra sua aprovação.

3. Aplique somente depois da revisão:

```powershell
.\.env\Scripts\python.exe translator.py --apply --languages pt --files '01-enforce-script/01-variables-types.md'
```

`--apply` não gera tradução: exige prévia com hashes atuais da origem, script, glossário, identidade/revisão do modelo e saída. Recusa sobrescrever um destino alterado desde a geração, salvo se já contiver a saída. Use o mesmo `--model` nas duas etapas. Editar a prévia manualmente invalida seu hash; não altere o manifesto para contornar essa verificação. Ajuste o processo e regenere, ou faça uma edição editorial separada na wiki fora desse fluxo.

Antes de substituir um destino existente diferente da saída, o script preserva seu conteúdo em `.translations/backups/`. Gravações de texto usam arquivo temporário e `os.replace`. O lote não é uma transação única: páginas concluídas permanecem quando outra falha. Depois de aplicar, confira diff, rota, âncoras e diagramas no VitePress; o tradutor não executa essa validação.

Blocos de código inteiros, inclusive Mermaid, **mantêm os comentários e rótulos em inglês**. Destinos de links são preservados, sem migração automática de `/en/` para outro locale. Âncoras explícitas baseadas nos títulos EN ajudam a preservar referências, mas não comprovam que todas as rotas existem.

---

## Restaurar backup

```powershell
.\.env\Scripts\python.exe translator.py --restore --languages pt --files '01-enforce-script/01-variables-types.md'
```

Informe idiomas e caminhos exatos; `--restore` não expande globs. O manifesto identifica o backup pelo hash do destino anterior. A restauração verifica esse hash, preserva CRLF/BOM e recusa substituir uma página editada após aplicação. Se já corresponde ao original, informa que está restaurada. Se o destino não existia antes, não há backup. Preserve manifesto e backups: regenerar prévias pode atualizar a referência ao destino anterior; este comando não é um navegador de versões históricas.

---

## Retomada, bloqueio e falhas

| Artefato em `.translations/` | Uso |
|---|---|
| `preview/<idioma>/<página>` | Saída completa para revisão |
| `manifest.json` | Hashes de origem, saída, destino anterior e configuração |
| `chunks/<fingerprint>/<idioma>/` | Cache de trechos que passaram pelas verificações locais |
| `backups/<idioma>/<página>.<hash>.bak` | Conteúdo anterior à aplicação |
| `last-run.json` | Resultados do último lote, inclusive sucessos parciais |
| `failures/<idioma>/<página>.json` | Origem protegida e resposta nas exceções `FalhaTraducao` |
| `run.lock` | PID e horário do processo que bloqueia o lote |

A retomada reutiliza prévias atuais e, ao regenerar uma página, trechos compatíveis em cache. Script, glossário e modelo compõem a versão do cache; versões dos pacotes não entram nessa chave. Cada trecho em cache passa por hash, estrutura e marcadores; a página montada passa pela validação final. Isso não substitui revisão humana.

Para ignorar prévias e trechos em cache:

```powershell
.\.env\Scripts\python.exe translator.py --languages pt --files '01-enforce-script/01-variables-types.md' --no-resume
```

`--no-resume` não apaga todo o cache e não pode ser combinado com `--apply`. A geração usa trechos de até 1.200 tokens de entrada protegida e até 4.096 tokens novos por trecho. Uma linha acima do limite de entrada é recusada; contexto semântico entre trechos não é garantido.

Prévia, aplicação e restauração usam bloqueio exclusivo. Após interrupção abrupta, leia `run.lock`, confira o PID e confirme que o processo terminou antes de remover somente o lock obsoleto. Não remova lock ativo. O smoke test não usa o bloqueio de lote; evite executá-lo junto com geração.

Uma rejeição de validação do trecho permite até duas tentativas totais, com sementes 42/43 e feedback do erro, sem relaxar a proteção. Falhas do pipeline (inclusive falta de memória GPU) e rejeições na validação final da página não acionam essa repetição. Se as duas tentativas forem rejeitadas, os detalhes incluem ambas as respostas.

O lote para após três falhas por padrão; ajuste com `--max-failures N`, inteiro positivo. Falhas retornam 1; erro de argumentos retorna 2. Erros anteriores ao processamento podem aparecer somente no console, sem novo relatório. Nem toda exceção cria `failures/`, e arquivos antigos de falha podem permanecer: confira relatório e horários. Investigue marcadores faltantes, idioma inesperado ou mudança estrutural; não relaxe verificações para publicar a saída.

`--smoke-test --languages pt ja` gera amostras curtas na GPU e registra `.translations/smoke-qwen.json`; sem seleção usa húngaro. Não altera páginas da wiki e não substitui revisão de página completa. Os resultados reais da página PT e a validação final são registrados separadamente pelo coordenador; este documento não declara testes ou build aprovados.
