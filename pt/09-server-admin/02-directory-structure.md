# Chapter 9.2: Estrutura de Diretorios e Pasta de Missao

[Inicio](../README.md) | [<< Anterior: Configuracao do Servidor](01-server-setup.md) | **Estrutura de Diretorios** | [Proximo: Referencia do serverDZ.cfg >>](03-server-cfg.md)

---

> **Resumo:** Um guia completo de cada arquivo e pasta no diretorio do servidor DayZ e na pasta de missao. Saber o que cada arquivo faz -- e quais podem ser editados com seguranca -- e essencial antes de mexer na economia de loot ou adicionar mods.

---

## Sumario

- [Diretorio Raiz do Servidor](#diretorio-raiz-do-servidor)
- [A Pasta addons/](#a-pasta-addons)
- [A Pasta keys/](#a-pasta-keys)
- [A Pasta profiles/](#a-pasta-profiles)
- [A Pasta mpmissions/](#a-pasta-mpmissions)
- [Estrutura da Pasta de Missao](#estrutura-da-pasta-de-missao)
- [A Pasta db/ -- Nucleo da Economia](#a-pasta-db----nucleo-da-economia)
- [A Pasta env/ -- Territorios de Animais](#a-pasta-env----territorios-de-animais)
- [A Pasta storage_1/ -- Persistencia](#a-pasta-storage_1----persistencia)
- [Arquivos de Missao no Nivel Superior](#arquivos-de-missao-no-nivel-superior)
- [Quais Arquivos Editar vs Nao Mexer](#quais-arquivos-editar-vs-nao-mexer)

---

## Diretorio Raiz do Servidor

```
DayZServer/
  DayZServer_x64.exe          # Executavel do servidor
  serverDZ.cfg                 # Configuracao principal (nome, senha, mods, hora)
  dayzsetting.xml              # Configuracoes de renderizacao (irrelevante para servidores dedicados)
  ban.txt                      # Steam64 IDs banidos, um por linha
  whitelist.txt                # Steam64 IDs na whitelist, um por linha
  steam_appid.txt              # Contem "221100" -- nao edite
  dayz.gproj                   # Arquivo de projeto do Workbench -- nao edite
  addons/                      # PBOs vanilla do jogo
  battleye/                    # Arquivos anti-cheat
  config/                      # Configuracao do Steam (config.vdf)
  dta/                         # PBOs do engine (scripts, GUI, graficos)
  keys/                        # Chaves de verificacao de assinatura (arquivos .bikey)
  logs/                        # Logs a nivel de engine
  mpmissions/                  # Todas as pastas de missao
  profiles/                    # Saida em execucao (logs de script, BD de jogadores, dumps de crash)
  server_manager/              # Utilitarios de gerenciamento do servidor
```

---

## A Pasta addons/

Contem todo o conteudo vanilla do jogo empacotado como arquivos PBO. Cada PBO tem um arquivo de assinatura `.bisign` correspondente:

```
addons/
  ai.pbo                       # Scripts de comportamento de IA
  ai.pbo.dayz.bisign           # Assinatura do ai.pbo
  animals.pbo                  # Definicoes de animais
  characters_backpacks.pbo     # Modelos/configs de mochilas
  characters_belts.pbo         # Modelos de itens de cinto
  weapons_firearms.pbo         # Modelos/configs de armas
  ... (100+ arquivos PBO)
```

**Nunca edite esses arquivos.** Eles sao sobrescritos toda vez que voce atualiza o servidor via SteamCMD. Mods sobrescrevem o comportamento vanilla atraves do sistema de `modded` class, nao alterando PBOs.

---

## A Pasta keys/

Contem arquivos de chave publica `.bikey` usados para verificar assinaturas de mods:

```
keys/
  dayz.bikey                   # Chave de assinatura vanilla (sempre presente)
```

Quando voce adiciona um mod, copie o arquivo `.bikey` dele para esta pasta. O servidor usa `verifySignatures = 2` no `serverDZ.cfg` para rejeitar qualquer PBO que nao tenha um `.bikey` correspondente nesta pasta.

Se um jogador carregar um mod cuja chave nao esta na sua pasta `keys/`, ele recebe um kick de **"Signature check failed"**.

---

## A Pasta profiles/

Criada no primeiro lancamento do servidor. Contem saida em tempo de execucao:

```
profiles/
  BattlEye/                              # Logs e bans do BE
  DataCache/                             # Dados em cache
  Users/                                 # Arquivos de preferencia por jogador
  DayZServer_x64_2026-03-08_11-34-31.ADM  # Log de admin
  DayZServer_x64_2026-03-08_11-34-31.RPT  # Relatorio do engine (info de crash, avisos)
  script_2026-03-08_11-34-35.log           # Log de script (sua principal ferramenta de debug)
```

O **log de script** e o arquivo mais importante aqui. Toda chamada `Print()`, todo erro de script e toda mensagem de carregamento de mod vai para ca. Quando algo quebra, e aqui que voce olha primeiro.

Arquivos de log se acumulam com o tempo. Logs antigos nao sao deletados automaticamente.

---

## A Pasta mpmissions/

Contem uma subpasta por mapa:

```
mpmissions/
  dayzOffline.chernarusplus/    # Chernarus (gratuito)
  dayzOffline.enoch/            # Livonia (DLC)
  dayzOffline.sakhal/           # Sakhal (DLC)
```

O formato do nome da pasta e `<nomeDaMissao>.<nomeDoTerreno>`. O valor `template` no `serverDZ.cfg` deve corresponder exatamente a um desses nomes de pasta.

---

## Estrutura da Pasta de Missao

A pasta de missao de Chernarus (`mpmissions/dayzOffline.chernarusplus/`) contem:

```
dayzOffline.chernarusplus/
  init.c                         # Script de ponto de entrada da missao
  db/                            # Arquivos de economia centrais
  env/                           # Definicoes de territorio de animais
  storage_1/                     # Dados de persistencia (jogadores, estado do mundo)
  cfgeconomycore.xml             # Classes raiz da economia e configuracoes de log
  cfgenvironment.xml             # Links para arquivos de territorio de animais
  cfgeventgroups.xml             # Definicoes de grupos de eventos
  cfgeventspawns.xml             # Posicoes exatas de spawn para eventos (veiculos, etc.)
  cfgeffectarea.json             # Definicoes de zonas contaminadas
  cfggameplay.json               # Ajustes de gameplay (stamina, dano, construcao)
  cfgignorelist.xml              # Itens excluidos da economia inteiramente
  cfglimitsdefinition.xml        # Definicoes validas de tags de categoria/uso/valor
  cfglimitsdefinitionuser.xml    # Definicoes de tags customizadas pelo usuario
  cfgplayerspawnpoints.xml       # Locais de spawn de jogadores novos
  cfgrandompresets.xml           # Definicoes reutilizaveis de pools de loot
  cfgspawnabletypes.xml          # Itens pre-anexados e carga em entidades spawnadas
  cfgundergroundtriggers.json    # Triggers de areas subterraneas
  cfgweather.xml                 # Configuracao de clima
  areaflags.map                  # Dados de flags de area (binario)
  mapclusterproto.xml            # Definicoes de prototipo de cluster de mapa
  mapgroupcluster.xml            # Definicoes de cluster de grupo de construcoes
  mapgroupcluster01.xml          # Dados de cluster (parte 1)
  mapgroupcluster02.xml          # Dados de cluster (parte 2)
  mapgroupcluster03.xml          # Dados de cluster (parte 3)
  mapgroupcluster04.xml          # Dados de cluster (parte 4)
  mapgroupdirt.xml               # Posicoes de loot no chao/terra
  mapgrouppos.xml                # Posicoes de grupos no mapa
  mapgroupproto.xml              # Definicoes de prototipos de grupos no mapa
```

---

## A Pasta db/ -- Nucleo da Economia

Este e o coracao da Economia Central. Cinco arquivos controlam o que aparece, onde e em que quantidade:

```
db/
  types.xml        # O ARQUIVO principal: define regras de spawn de cada item
  globals.xml      # Parametros globais da economia (timers, limites, contagens)
  events.xml       # Eventos dinamicos (animais, veiculos, helicopteros)
  economy.xml      # Toggles dos subsistemas da economia (loot, animais, veiculos)
  messages.xml     # Mensagens agendadas do servidor para jogadores
```

### types.xml

Define regras de spawn para **todo item** no jogo. Com aproximadamente 23.000 linhas, este e de longe o maior arquivo de economia. Cada entrada especifica quantas copias de um item devem existir no mapa, onde ele pode spawnar e por quanto tempo persiste. Veja o [Capitulo 9.4](04-loot-economy.md) para um mergulho profundo.

### globals.xml

Parametros globais que afetam toda a economia: contagens de zumbis, contagens de animais, timers de limpeza, faixas de dano de loot, timing de respawn. Sao 33 parametros no total. Veja o [Capitulo 9.4](04-loot-economy.md) para a referencia completa.

### events.xml

Define eventos de spawn dinamico para animais e veiculos. Cada evento especifica uma contagem nominal, restricoes de spawn e variantes filhas. Por exemplo, o evento `VehicleCivilianSedan` spawna 8 sedans pelo mapa em 3 variantes de cor.

### economy.xml

Toggles mestres para subsistemas da economia:

```xml
<economy>
    <dynamic init="1" load="1" respawn="1" save="1"/>
    <animals init="1" load="0" respawn="1" save="0"/>
    <zombies init="1" load="0" respawn="1" save="0"/>
    <vehicles init="1" load="1" respawn="1" save="1"/>
    <randoms init="0" load="0" respawn="1" save="0"/>
    <custom init="0" load="0" respawn="0" save="0"/>
    <building init="1" load="1" respawn="0" save="1"/>
    <player init="1" load="1" respawn="1" save="1"/>
</economy>
```

| Flag | Significado |
|------|---------|
| `init` | Spawnar itens no primeiro inicio do servidor |
| `load` | Carregar estado salvo da persistencia |
| `respawn` | Permitir respawn de itens apos limpeza |
| `save` | Salvar estado nos arquivos de persistencia |

### messages.xml

Mensagens agendadas transmitidas para todos os jogadores. Suporta timers de contagem regressiva, intervalos de repeticao, mensagens ao conectar e avisos de desligamento:

```xml
<messages>
    <message>
        <deadline>600</deadline>
        <shutdown>1</shutdown>
        <text>#name will shutdown in #tmin minutes.</text>
    </message>
    <message>
        <delay>2</delay>
        <onconnect>1</onconnect>
        <text>Welcome to #name</text>
    </message>
</messages>
```

Use `#name` para o nome do servidor e `#tmin` para o tempo restante em minutos.

---

## A Pasta env/ -- Territorios de Animais

Contem arquivos XML que definem onde cada especie animal pode spawnar:

```
env/
  bear_territories.xml
  cattle_territories.xml
  domestic_animals_territories.xml
  fox_territories.xml
  hare_territories.xml
  hen_territories.xml
  pig_territories.xml
  red_deer_territories.xml
  roe_deer_territories.xml
  sheep_goat_territories.xml
  wild_boar_territories.xml
  wolf_territories.xml
  zombie_territories.xml
```

Esses arquivos contem centenas de pontos de coordenadas definindo zonas de territorio pelo mapa. Eles sao referenciados pelo `cfgenvironment.xml`. Voce raramente precisa edita-los, a menos que queira mudar onde animais ou zumbis spawnam geograficamente.

---

## A Pasta storage_1/ -- Persistencia

Guarda o estado persistente do servidor entre reinicializacoes:

```
storage_1/
  players.db         # Banco de dados SQLite de todos os personagens
  spawnpoints.bin    # Dados binarios de pontos de spawn
  backup/            # Backups automaticos de dados de persistencia
  data/              # Estado do mundo (itens colocados, construcoes de base, veiculos)
```

**Nunca edite `players.db` enquanto o servidor estiver rodando.** Ele e um banco de dados SQLite bloqueado pelo processo do servidor. Se voce precisar limpar personagens, pare o servidor primeiro e delete ou renomeie o arquivo.

Para fazer um **wipe completo de persistencia**, pare o servidor e delete toda a pasta `storage_1/`. O servidor a recriara no proximo lancamento com um mundo novo.

Para fazer um **wipe parcial** (manter personagens, resetar loot):
1. Pare o servidor
2. Delete os arquivos em `storage_1/data/` mas mantenha `players.db`
3. Reinicie

---

## Arquivos de Missao no Nivel Superior

### cfgeconomycore.xml

Registra classes raiz para a economia e configura o log do CE:

```xml
<economycore>
    <classes>
        <rootclass name="DefaultWeapon" />
        <rootclass name="DefaultMagazine" />
        <rootclass name="Inventory_Base" />
        <rootclass name="HouseNoDestruct" reportMemoryLOD="no" />
        <rootclass name="SurvivorBase" act="character" reportMemoryLOD="no" />
        <rootclass name="DZ_LightAI" act="character" reportMemoryLOD="no" />
        <rootclass name="CarScript" act="car" reportMemoryLOD="no" />
        <rootclass name="BoatScript" act="car" reportMemoryLOD="no" />
    </classes>
    <defaults>
        <default name="log_ce_loop" value="false"/>
        <default name="log_ce_dynamicevent" value="false"/>
        <default name="log_ce_vehicle" value="false"/>
        <default name="log_ce_lootspawn" value="false"/>
        <default name="log_ce_lootcleanup" value="false"/>
        <default name="log_ce_lootrespawn" value="false"/>
        <default name="log_ce_statistics" value="false"/>
        <default name="log_ce_zombie" value="false"/>
        <default name="log_storageinfo" value="false"/>
        <default name="log_hivewarning" value="true"/>
        <default name="log_missionfilewarning" value="true"/>
        <default name="save_events_startup" value="true"/>
        <default name="save_types_startup" value="true"/>
    </defaults>
</economycore>
```

Defina `log_ce_lootspawn` como `"true"` ao debugar problemas de spawn de itens. Isso produz uma saida detalhada no log RPT mostrando quais itens o CE esta tentando spawnar e por que eles falham ou tem sucesso.

### cfglimitsdefinition.xml

Define os valores validos para os elementos `<category>`, `<usage>`, `<value>` e `<tag>` usados no `types.xml`:

```xml
<lists>
    <categories>
        <category name="tools"/>
        <category name="containers"/>
        <category name="clothes"/>
        <category name="food"/>
        <category name="weapons"/>
        <category name="books"/>
        <category name="explosives"/>
        <category name="lootdispatch"/>
    </categories>
    <tags>
        <tag name="floor"/>
        <tag name="shelves"/>
        <tag name="ground"/>
    </tags>
    <usageflags>
        <usage name="Military"/>
        <usage name="Police"/>
        <usage name="Medic"/>
        <usage name="Firefighter"/>
        <usage name="Industrial"/>
        <usage name="Farm"/>
        <usage name="Coast"/>
        <usage name="Town"/>
        <usage name="Village"/>
        <usage name="Hunting"/>
        <usage name="Office"/>
        <usage name="School"/>
        <usage name="Prison"/>
        <usage name="Lunapark"/>
        <usage name="SeasonalEvent"/>
        <usage name="ContaminatedArea"/>
        <usage name="Historical"/>
    </usageflags>
    <valueflags>
        <value name="Tier1"/>
        <value name="Tier2"/>
        <value name="Tier3"/>
        <value name="Tier4"/>
        <value name="Unique"/>
    </valueflags>
</lists>
```

Se voce usar uma tag `<usage>` ou `<value>` no `types.xml` que nao esteja definida aqui, o item silenciosamente nao vai spawnar.

### cfgignorelist.xml

Itens listados aqui sao completamente excluidos da economia, mesmo que tenham entradas no `types.xml`:

```xml
<ignore>
    <type name="Bandage"></type>
    <type name="CattleProd"></type>
    <type name="Defibrillator"></type>
    <type name="HescoBox"></type>
    <type name="StunBaton"></type>
    <type name="TransitBus"></type>
    <type name="Spear"></type>
    <type name="Mag_STANAGCoupled_30Rnd"></type>
    <type name="Wreck_Mi8"></type>
</ignore>
```

Isso e usado para itens que existem no codigo do jogo mas nao devem spawnar naturalmente (itens inacabados, conteudo obsoleto, itens sazonais fora de epoca).

### cfggameplay.json

Um arquivo JSON que sobrescreve parametros de gameplay. Controla stamina, movimento, dano de base, clima, temperatura, obstrucao de arma, afogamento e mais. Este arquivo e opcional -- se ausente, o servidor usa valores padrao.

### cfgplayerspawnpoints.xml

Define onde jogadores recem-spawnados aparecem no mapa, com restricoes de distancia de infectados, outros jogadores e construcoes.

### cfgeventspawns.xml

Contem coordenadas exatas do mundo onde eventos (veiculos, helicrashes, etc.) podem spawnar. Cada nome de evento do `events.xml` tem uma lista de posicoes validas:

```xml
<eventposdef>
    <event name="VehicleCivilianSedan">
        <pos x="12071.933594" z="9129.989258" a="317.953339" />
        <pos x="12302.375001" z="9051.289062" a="60.399284" />
        <pos x="10182.458985" z="1987.5271" a="29.172445" />
        ...
    </event>
</eventposdef>
```

O atributo `a` e o angulo de rotacao em graus.

---

## Quais Arquivos Editar vs Nao Mexer

| Arquivo / Pasta | Seguro para Editar? | Observacoes |
|---------------|:---:|-------|
| `serverDZ.cfg` | Sim | Configuracao principal do servidor |
| `db/types.xml` | Sim | Regras de spawn de itens -- sua edicao mais comum |
| `db/globals.xml` | Sim | Parametros de ajuste da economia |
| `db/events.xml` | Sim | Eventos de spawn de veiculos/animais |
| `db/economy.xml` | Sim | Toggles de subsistemas da economia |
| `db/messages.xml` | Sim | Mensagens broadcast do servidor |
| `cfggameplay.json` | Sim | Ajustes de gameplay |
| `cfgspawnabletypes.xml` | Sim | Presets de anexos/carga |
| `cfgrandompresets.xml` | Sim | Definicoes de pools de loot |
| `cfglimitsdefinition.xml` | Sim | Adicionar tags customizadas de uso/valor |
| `cfgplayerspawnpoints.xml` | Sim | Locais de spawn de jogadores |
| `cfgeventspawns.xml` | Sim | Coordenadas de spawn de eventos |
| `cfgignorelist.xml` | Sim | Excluir itens da economia |
| `cfgweather.xml` | Sim | Padroes de clima |
| `cfgeffectarea.json` | Sim | Zonas contaminadas |
| `init.c` | Sim | Script de entrada da missao |
| `addons/` | **Nao** | Sobrescrito na atualizacao |
| `dta/` | **Nao** | Dados do engine |
| `keys/` | Apenas adicionar | Copie arquivos `.bikey` de mods aqui |
| `storage_1/` | Apenas deletar | Persistencia -- nao edite manualmente |
| `battleye/` | **Nao** | Anti-cheat -- nao toque |
| `mapgroup*.xml` | Cuidado | Posicoes de loot em construcoes -- edicao avancada apenas |

---

**Anterior:** [Configuracao do Servidor](01-server-setup.md) | [Inicio](../README.md) | **Proximo:** [Referencia do serverDZ.cfg >>](03-server-cfg.md)
