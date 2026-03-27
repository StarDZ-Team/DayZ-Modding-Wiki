# Chapter 9.8: Ajuste de Performance

[Inicio](../README.md) | [<< Anterior: Persistencia](07-persistence.md) | [Proximo: Controle de Acesso >>](09-access-control.md)

---

> **Resumo:** Performance de servidor no DayZ se resume a tres coisas: contagem de itens, eventos dinamicos e carga de mods/jogadores. Este capitulo cobre as configuracoes especificas que importam, como diagnosticar problemas e qual hardware realmente ajuda -- tudo baseado em dados reais da comunidade de 400+ relatos no Discord sobre quedas de FPS, lag e desync.

---

## Sumario

- [O Que Afeta a Performance do Servidor](#o-que-afeta-a-performance-do-servidor)
- [Ajuste do globals.xml](#ajuste-do-globalsxml)
- [Ajuste da Economia para Performance](#ajuste-da-economia-para-performance)
- [Logging do cfgeconomycore.xml](#logging-do-cfgeconomycorexml)
- [Configuracoes de Performance do serverDZ.cfg](#configuracoes-de-performance-do-serverdzcfg)
- [Impacto de Performance de Mods](#impacto-de-performance-de-mods)
- [Recomendacoes de Hardware](#recomendacoes-de-hardware)
- [Monitorando a Saude do Servidor](#monitorando-a-saude-do-servidor)
- [Erros Comuns de Performance](#erros-comuns-de-performance)

---

## O Que Afeta a Performance do Servidor

A partir de dados da comunidade (400+ mencoes no Discord sobre FPS/performance/lag/desync), os tres maiores fatores de performance sao:

1. **Contagem de itens** -- valores altos de `nominal` no `types.xml` significam que a Economia Central rastreia e processa mais objetos a cada ciclo. Esta e consistentemente a causa numero um de lag do lado do servidor.
2. **Spawn de eventos** -- muitos eventos dinamicos ativos (veiculos, animais, helicrashes) no `events.xml` consomem ciclos de spawn/limpeza e slots de entidade.
3. **Contagem de jogadores + contagem de mods** -- cada jogador conectado gera atualizacoes de entidade, e cada mod adiciona classes de script que o engine deve compilar e executar a cada tick.

O loop de jogo do servidor roda a uma taxa fixa de 30 FPS. Quando o servidor nao consegue manter 30 FPS, jogadores experimentam desync -- rubber-banding, coletas de itens atrasadas e falhas no registro de acertos. Abaixo de 15 FPS do servidor, o jogo se torna injogavel.

---

## Ajuste do globals.xml

Estes sao os padroes vanilla para os parametros que afetam diretamente a performance:

```xml
<var name="ZombieMaxCount" type="0" value="1000"/>
<var name="AnimalMaxCount" type="0" value="200"/>
<var name="ZoneSpawnDist" type="0" value="300"/>
<var name="SpawnInitial" type="0" value="1200"/>
<var name="CleanupLifetimeDefault" type="0" value="45"/>
```

### O Que Cada Valor Controla

| Parametro | Padrao | Efeito na Performance |
|-----------|---------|-------------------|
| `ZombieMaxCount` | 1000 | Limite para total de infectados no servidor. Cada zumbi roda pathfinding de IA. Diminuir para 500-700 melhora notavelmente o FPS do servidor em servidores populados. |
| `AnimalMaxCount` | 200 | Limite para animais. Animais tem IA mais simples que zumbis mas ainda consomem tempo de tick. Diminua para 100 se voce ver problemas de FPS. |
| `ZoneSpawnDist` | 300 | Distancia em metros na qual zonas de zumbis ativam ao redor de jogadores. Diminuir para 200 significa menos zonas ativas simultaneas. |
| `SpawnInitial` | 1200 | Numero de itens que o CE spawna no primeiro inicio. Valores mais altos significam carregamento inicial mais longo. Nao afeta performance em estado estavel. |
| `CleanupLifetimeDefault` | 45 | Tempo de limpeza padrao em segundos para itens sem lifetime especifico. Valores mais baixos significam ciclos de limpeza mais rapidos mas processamento do CE mais frequente. |

**Perfil de performance recomendado** (para servidores com dificuldade acima de 40 jogadores):

```xml
<var name="ZombieMaxCount" type="0" value="700"/>
<var name="AnimalMaxCount" type="0" value="100"/>
<var name="ZoneSpawnDist" type="0" value="200"/>
```

---

## Ajuste da Economia para Performance

A Economia Central roda um loop continuo verificando cada tipo de item contra seus alvos de `nominal`/`min`. Mais tipos de itens com nominais mais altos significa mais trabalho por ciclo.

### Reduzir Valores Nominais

Todo item no `types.xml` com `nominal > 0` e rastreado pelo CE. Se voce tem 2000 tipos de itens com um nominal medio de 20, o CE esta gerenciando 40.000 objetos. Reduza nominais de forma geral para cortar este numero:

- Itens civis comuns: diminua de 15-40 para 10-25
- Armas: mantenha baixo (vanilla ja e 2-10)
- Variantes de roupa: considere desativar variantes de cor que voce nao precisa (`nominal=0`)

### Reduzir Eventos Dinamicos

No `events.xml`, cada evento ativo spawna e monitora grupos de entidades. Diminua o `nominal` em eventos de veiculos e animais, ou defina `<active>0</active>` em eventos que voce nao precisa.

### Usar Modo Ocioso

Quando nenhum jogador esta conectado, o CE pode pausar inteiramente:

```xml
<var name="IdleModeCountdown" type="0" value="60"/>
<var name="IdleModeStartup" type="0" value="1"/>
```

`IdleModeCountdown=60` significa que o servidor entra em modo ocioso 60 segundos apos o ultimo jogador desconectar. `IdleModeStartup=1` significa que o servidor inicia em modo ocioso e so ativa o CE quando o primeiro jogador conecta. Isso previne o servidor de processar ciclos de spawn enquanto vazio.

### Ajustar Taxa de Respawn

```xml
<var name="RespawnLimit" type="0" value="20"/>
<var name="RespawnTypes" type="0" value="12"/>
<var name="RespawnAttempt" type="0" value="2"/>
```

Estes controlam quantos itens e tipos de itens o CE processa por ciclo. Valores mais baixos reduzem a carga do CE por tick mas desaceleram o respawn de loot. Os padroes vanilla acima ja sao conservadores.

---

## Logging do cfgeconomycore.xml

Ative logs de diagnostico do CE temporariamente para medir tempos de ciclo e identificar gargalos. No seu `cfgeconomycore.xml`:

```xml
<default name="log_ce_loop" value="false"/>
<default name="log_ce_dynamicevent" value="false"/>
<default name="log_ce_vehicle" value="false"/>
<default name="log_ce_lootspawn" value="false"/>
<default name="log_ce_lootcleanup" value="false"/>
<default name="log_ce_statistics" value="false"/>
```

Para diagnosticar performance, defina `log_ce_statistics` como `"true"`. Isso gera dados de tempo de ciclo do CE no log RPT do servidor. Procure linhas mostrando quanto tempo cada ciclo do CE leva -- se ciclos excedem 1000ms, a economia esta sobrecarregada.

Defina `log_ce_lootspawn` e `log_ce_lootcleanup` como `"true"` para ver quais tipos de itens estao spawnando e sendo limpos com mais frequencia. Estes sao seus candidatos para reducao de nominal.

**Desative o logging apos diagnostico.** Escritas de log consomem I/O e podem piorar a performance se deixadas ativadas permanentemente.

---

## Configuracoes de Performance do serverDZ.cfg

O arquivo de configuracao principal do servidor tem opcoes limitadas relacionadas a performance:

| Configuracao | Efeito |
|---------|--------|
| `maxPlayers` | Diminua se o servidor estiver com dificuldade. Cada jogador gera trafego de rede e atualizacoes de entidade. Ir de 60 para 40 jogadores pode recuperar 5-10 FPS do servidor. |
| `instanceId` | Determina o caminho do `storage_1/`. Nao e uma configuracao de performance, mas se seu armazenamento esta em um disco lento, afeta o I/O de persistencia. |

**O que voce nao pode mudar:** a taxa de tick do servidor e fixa em 30 FPS. Nao ha configuracao para aumentar ou diminui-la. Se o servidor nao consegue manter 30 FPS, ele simplesmente roda mais devagar.

---

## Impacto de Performance de Mods

Cada mod adiciona classes de script que o engine compila na inicializacao e executa a cada tick. O impacto varia dramaticamente pela qualidade do mod:

- **Mods somente de conteudo** (armas, roupas, construcoes) adicionam tipos de itens mas overhead minimo de script. Seu custo esta no rastreamento do CE, nao no processamento de tick.
- **Mods pesados em script** com loops `OnUpdate()` ou `OnTick()` rodam codigo a cada frame do servidor. Loops mal otimizados nesses mods sao a causa mais comum de lag relacionada a mods.
- **Mods de trader/economia** que mantem grandes inventarios adicionam objetos persistentes que o engine deve rastrear.

### Diretrizes

- Adicione mods incrementalmente. Teste o FPS do servidor apos cada adicao, nao apos adicionar 10 de uma vez.
- Monitore o FPS do servidor com ferramentas de admin ou saida do log RPT apos adicionar novos mods.
- Se um mod causar problemas, verifique seu codigo-fonte por operacoes caras executadas por frame.

Consenso da comunidade: "Itens (types) e spawn de eventos sao os mais exigentes -- mods que adicionam milhares de entradas no types.xml prejudicam mais do que mods que adicionam scripts complexos."

---

## Recomendacoes de Hardware

A logica de jogo do servidor DayZ e **single-threaded**. CPUs multi-nucleo ajudam com overhead do SO e I/O de rede, mas o loop principal do jogo roda em um nucleo.

| Componente | Recomendacao | Por que |
|-----------|---------------|-----|
| **CPU** | Maior performance single-thread possivel. AMD 5600X ou melhor. | O loop do jogo e single-threaded. Velocidade de clock e IPC importam mais que contagem de nucleos. |
| **RAM** | 8 GB minimo, 12-16 GB para servidores com muitos mods | Mods e mapas grandes consomem memoria. Acabar a memoria causa travadas. |
| **Armazenamento** | SSD obrigatorio | I/O de persistencia do `storage_1/` e constante. HDD causa engasgos durante ciclos de salvamento. |
| **Rede** | 100 Mbps+ com baixa latencia | Largura de banda importa menos que estabilidade de ping para prevencao de desync. |

Dica da comunidade: "OVH oferece bom custo-beneficio -- cerca de $60 USD por uma maquina dedicada com 5600X que roda servidores moddados de 60 slots."

Evite hospedagem compartilhada/VPS para servidores populados. O problema do vizinho barulhento em hardware compartilhado causa quedas de FPS imprevisiveis que sao impossiveis de diagnosticar do seu lado.

---

## Monitorando a Saude do Servidor

### FPS do Servidor

Verifique o log RPT por linhas contendo FPS do servidor. Um servidor saudavel mantem 30 FPS consistentemente. Limiares de aviso:

| FPS do Servidor | Status |
|------------|--------|
| 25-30 | Normal. Flutuacoes menores sao esperadas durante combate pesado ou reinicializacoes. |
| 15-25 | Degradado. Jogadores notam desync em interacoes com itens e combate. |
| Abaixo de 15 | Critico. Rubber-banding, acoes falhando, registro de acertos quebrado. |

### Avisos de Ciclo do CE

Com `log_ce_statistics` ativado, observe tempos de ciclo do CE. Normal e abaixo de 500ms. Se ciclos regularmente excedem 1000ms, sua economia esta pesada demais.

### Crescimento do Armazenamento

Monitore o tamanho de `storage_1/`. Crescimento descontrolado indica inchaco de persistencia -- muitos objetos colocados, tendas ou esconderijos acumulando. Wipes regulares do servidor ou reducao de `FlagRefreshMaxDuration` no `globals.xml` ajudam a controlar isso.

### Relatos de Jogadores

Relatos de desync de jogadores sao seu indicador em tempo real mais confiavel. Se multiplos jogadores relatam rubber-banding simultaneamente, o FPS do servidor caiu abaixo de 15.

---

## Erros Comuns de Performance

### Valores Nominais Muito Altos

Definir todo item como `nominal=50` porque "mais loot e divertido" cria dezenas de milhares de objetos rastreados. O CE gasta todo seu ciclo gerenciando itens em vez de rodar o jogo. Comece com nominais vanilla e aumente seletivamente.

### Muitos Eventos de Veiculos

Veiculos sao entidades caras com simulacao de fisica, rastreamento de anexos e persistencia. O vanilla spawna cerca de 50 veiculos no total. Servidores rodando 150+ veiculos veem perda significativa de FPS.

### Rodando 30+ Mods Sem Testar

Cada mod e aceitavel isoladamente. O efeito composto de 30+ mods -- milhares de types extras, dezenas de scripts por frame e aumento de pressao de memoria -- pode derrubar o FPS do servidor em 50% ou mais. Adicione mods em lotes de 3-5 e teste apos cada lote.

### Nunca Reinicializando o Servidor

Alguns mods tem vazamentos de memoria que se acumulam ao longo do tempo. Agende reinicializacoes automaticas a cada 4-6 horas. A maioria dos paineis de hospedagem de servidores suporta isso. Mesmo mods bem escritos se beneficiam de reinicializacoes periodicas porque a propria fragmentacao de memoria do engine aumenta ao longo de sessoes longas.

### Ignorando Inchaco do Armazenamento

Uma pasta `storage_1/` que cresce para varios gigabytes desacelera cada ciclo de persistencia. Faca wipe ou reduza periodicamente, especialmente se voce permite construcao de base sem limites de decadencia.

### Logging Deixado Ativado

Logging de diagnostico do CE, logging de debug de script e logging de ferramentas de admin escrevem no disco a cada tick. Ative-os para diagnostico e depois desative. Logging verboso persistente em um servidor movimentado pode custar 1-2 FPS por si so.

---

[Inicio](../README.md) | [<< Anterior: Persistencia](07-persistence.md) | [Proximo: Controle de Acesso >>](09-access-control.md)
