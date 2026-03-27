# Chapter 9.5: Spawn de Veiculos e Eventos Dinamicos

[Inicio](../README.md) | [<< Anterior: Economia de Loot](04-loot-economy.md) | [Proximo: Spawn de Jogadores >>](06-player-spawning.md)

---

> **Resumo:** Veiculos e eventos dinamicos (helicrashes, comboios, carros de policia) NAO usam o `types.xml`. Eles usam um sistema separado de tres arquivos: `events.xml` define o que spawna e quantos, `cfgeventspawns.xml` define onde, e `cfgeventgroups.xml` define formacoes agrupadas. Este capitulo cobre todos os tres arquivos com valores reais do vanilla.

---

## Sumario

- [Como o Spawn de Veiculos Funciona](#como-o-spawn-de-veiculos-funciona)
- [Entradas de Veiculos no events.xml](#entradas-de-veiculos-no-eventsxml)
- [Referencia de Campos de Eventos de Veiculos](#referencia-de-campos-de-eventos-de-veiculos)
- [cfgeventspawns.xml -- Posicoes de Spawn](#cfgeventspawnsxml----posicoes-de-spawn)
- [Eventos de Helicrash](#eventos-de-helicrash)
- [Comboio Militar](#comboio-militar)
- [Carro de Policia](#carro-de-policia)
- [cfgeventgroups.xml -- Spawns Agrupados](#cfgeventgroupsxml----spawns-agrupados)
- [Classe Raiz de Veiculo no cfgeconomycore.xml](#classe-raiz-de-veiculo-no-cfgeconomycorexml)
- [Erros Comuns](#erros-comuns)

---

## Como o Spawn de Veiculos Funciona

Veiculos **nao** sao definidos no `types.xml`. Se voce adicionar uma classe de veiculo ao `types.xml`, ele nao spawnara. Veiculos usam um pipeline dedicado de tres arquivos:

1. **`events.xml`** -- Define cada evento de veiculo: quantos devem existir no mapa (nominal), quais variantes podem spawnar (filhos), e flags de comportamento como lifetime e raio seguro.

2. **`cfgeventspawns.xml`** -- Define as posicoes fisicas no mundo onde eventos de veiculos podem colocar entidades. Cada nome de evento mapeia para uma lista de entradas `<pos>` com coordenadas x, z e angulo.

3. **`cfgeventgroups.xml`** -- Define spawns agrupados onde multiplos objetos spawnam juntos com offsets posicionais relativos (ex.: trens abandonados).

O CE le o `events.xml`, escolhe um evento que precisa spawnar, busca posicoes correspondentes no `cfgeventspawns.xml`, seleciona uma aleatoriamente que satisfaca as restricoes de `saferadius` e `distanceradius`, e entao spawna uma entidade filha selecionada aleatoriamente naquela posicao.

Todos os tres arquivos ficam em `mpmissions/<sua_missao>/db/`.

---

## Entradas de Veiculos no events.xml

Todo tipo de veiculo vanilla tem sua propria entrada de evento. Aqui estao todos com valores reais:

### Sedan Civil

```xml
<event name="VehicleCivilianSedan">
    <nominal>8</nominal>
    <min>5</min>
    <max>11</max>
    <lifetime>300</lifetime>
    <restock>0</restock>
    <saferadius>500</saferadius>
    <distanceradius>500</distanceradius>
    <cleanupradius>200</cleanupradius>
    <flags deletable="0" init_random="0" remove_damaged="1"/>
    <position>fixed</position>
    <limit>mixed</limit>
    <active>1</active>
    <children>
        <child lootmax="0" lootmin="0" max="5" min="3" type="CivilianSedan"/>
        <child lootmax="0" lootmin="0" max="5" min="3" type="CivilianSedan_Black"/>
        <child lootmax="0" lootmin="0" max="5" min="3" type="CivilianSedan_Wine"/>
    </children>
</event>
```

### Todos os Eventos de Veiculos Vanilla

Todos os eventos de veiculos usam a mesma estrutura do Sedan acima. Apenas os valores diferem:

| Nome do Evento | Nominal | Min | Max | Lifetime | Filhos (variantes) |
|------------|---------|-----|-----|----------|---------------------|
| `VehicleCivilianSedan` | 8 | 5 | 11 | 300 | `CivilianSedan`, `_Black`, `_Wine` |
| `VehicleOffroadHatchback` | 8 | 5 | 11 | 300 | `OffroadHatchback`, `_Blue`, `_White` |
| `VehicleHatchback02` | 8 | 5 | 11 | 300 | Variantes do Hatchback02 |
| `VehicleSedan02` | 8 | 5 | 11 | 300 | Variantes do Sedan02 |
| `VehicleTruck01` | 8 | 5 | 11 | 300 | Variantes do caminhao V3S |
| `VehicleOffroad02` | 3 | 2 | 3 | 300 | Gunter -- menos spawnam |
| `VehicleBoat` | 22 | 18 | 24 | 600 | Barcos -- maior contagem, lifetime mais longo |

`VehicleOffroad02` tem um nominal mais baixo (3) que outros veiculos terrestres (8). `VehicleBoat` tem tanto o maior nominal (22) quanto um lifetime mais longo (600 vs 300).

---

## Referencia de Campos de Eventos de Veiculos

### Campos no Nivel do Evento

| Campo | Tipo | Descricao |
|-------|------|-------------|
| `name` | string | Identificador do evento. Deve corresponder a uma entrada no `cfgeventspawns.xml` quando `position="fixed"`. |
| `nominal` | int | Numero-alvo de instancias ativas deste evento no mapa. |
| `min` | int | O CE tentara spawnar mais quando a contagem cair abaixo deste valor. |
| `max` | int | Limite maximo. O CE nunca excedera esta contagem. |
| `lifetime` | int | Segundos entre verificacoes de respawn. Para veiculos, este NAO e o lifetime de persistencia do veiculo -- e o intervalo no qual o CE reavalia se deve spawnar ou limpar. |
| `restock` | int | Segundos minimos entre tentativas de respawn. 0 = proximo ciclo. |
| `saferadius` | int | Distancia minima (metros) de qualquer jogador para o evento spawnar. Previne veiculos aparecendo na frente de jogadores. |
| `distanceradius` | int | Distancia minima (metros) entre duas instancias do mesmo evento. Previne dois sedans spawnando um ao lado do outro. |
| `cleanupradius` | int | Se um jogador esta dentro desta distancia (metros), a entidade do evento e protegida da limpeza. |

### Flags

| Flag | Valores | Descricao |
|------|--------|-------------|
| `deletable` | 0, 1 | Se o CE pode deletar esta entidade de evento. Veiculos usam 0 (nao deletavel pelo CE). |
| `init_random` | 0, 1 | Aleatorizar posicoes iniciais no primeiro spawn. 0 = usar posicoes fixas do `cfgeventspawns.xml`. |
| `remove_damaged` | 0, 1 | Remover a entidade quando ela ficar arruinada. **Critico para veiculos** -- veja [Erros Comuns](#erros-comuns). |

### Outros Campos

| Campo | Valores | Descricao |
|-------|--------|-------------|
| `position` | `fixed`, `player` | `fixed` = spawnar em posicoes do `cfgeventspawns.xml`. `player` = spawnar relativo a posicoes de jogadores. |
| `limit` | `child`, `mixed`, `custom` | `child` = min/max aplicado por tipo filho. `mixed` = min/max compartilhado entre todos os filhos. `custom` = comportamento especifico do engine. |
| `active` | 0, 1 | Ativar ou desativar este evento. 0 = o evento e completamente ignorado. |

### Campos de Filhos

| Atributo | Descricao |
|-----------|-------------|
| `type` | Nome de classe da entidade a spawnar. |
| `min` | Instancias minimas desta variante. |
| `max` | Instancias maximas desta variante. |
| `lootmin` | Numero minimo de itens de loot spawnados dentro/ao redor da entidade. 0 para veiculos (pecas vem do `cfgspawnabletypes.xml`). |
| `lootmax` | Numero maximo de itens de loot. Usado por helicrashes e eventos dinamicos, nao veiculos. |

---

## cfgeventspawns.xml -- Posicoes de Spawn

Este arquivo mapeia nomes de eventos para coordenadas do mundo. Cada bloco `<event>` contem uma lista de posicoes de spawn validas para aquele tipo de evento. Quando o CE precisa spawnar um veiculo, ele escolhe uma posicao aleatoria desta lista que satisfaca as restricoes de `saferadius` e `distanceradius`.

```xml
<event name="VehicleCivilianSedan">
    <pos x="4509.1" z="9321.5" a="172"/>
    <pos x="6283.7" z="2468.3" a="90"/>
    <pos x="11447.2" z="11203.8" a="45"/>
    <pos x="2961.4" z="5107.6" a="0"/>
    <!-- ... mais posicoes ... -->
</event>
```

Cada `<pos>` tem tres atributos:

| Atributo | Descricao |
|-----------|-------------|
| `x` | Coordenada X do mundo (posicao leste-oeste no mapa). |
| `z` | Coordenada Z do mundo (posicao norte-sul no mapa). |
| `a` | Angulo em graus (0-360). A direcao que o veiculo encara ao spawnar. |

**Regras importantes:**

- Se um evento nao tem um bloco `<event>` correspondente no `cfgeventspawns.xml`, ele **nao spawnara** independentemente da configuracao do `events.xml`.
- Voce precisa de pelo menos tantas entradas `<pos>` quanto o seu valor de `nominal`. Se voce definir `nominal=8` mas tiver apenas 3 posicoes, apenas 3 podem spawnar.
- Posicoes devem estar em estradas ou terreno plano. Uma posicao dentro de uma construcao ou em terreno ingreme fara o veiculo spawnar enterrado ou capotado.
- O valor `a` (angulo) determina a direcao frontal do veiculo. Alinhe com a direcao da estrada para spawns de aparencia natural.

---

## Eventos de Helicrash

Helicrashes sao eventos dinamicos que spawnam destrocos com loot militar e infectados ao redor. Eles usam a tag `<secondary>` para definir spawns de zumbis ao redor do local do crash.

```xml
<event name="StaticHeliCrash">
    <nominal>3</nominal>
    <min>1</min>
    <max>3</max>
    <lifetime>2100</lifetime>
    <restock>0</restock>
    <saferadius>1000</saferadius>
    <distanceradius>500</distanceradius>
    <cleanupradius>200</cleanupradius>
    <secondary>InfectedArmy</secondary>
    <flags deletable="1" init_random="0" remove_damaged="0"/>
    <position>fixed</position>
    <limit>mixed</limit>
    <active>1</active>
    <children>
        <child lootmax="15" lootmin="10" max="3" min="1" type="Wreck_UH1Y"/>
    </children>
</event>
```

### Diferencas principais dos eventos de veiculos

- **`<secondary>InfectedArmy</secondary>`** -- spawna zumbis militares ao redor do local do crash. Esta tag referencia um grupo de spawn de infectados que o CE coloca nas proximidades.
- **`lootmin="10"` / `lootmax="15"`** -- os destrocos spawnam com 10-15 itens de loot de evento dinamico. Esses sao itens com flag `deloot="1"` no `types.xml` (equipamento militar, armas raras).
- **`lifetime=2100`** -- o crash persiste por 35 minutos antes do CE limpa-lo e spawnar um novo em outro lugar.
- **`saferadius=1000`** -- crashes nunca aparecem a menos de 1 km de um jogador.
- **`remove_damaged=0`** -- os destrocos ja estao "danificados" por definicao, entao este valor deve ser 0 ou eles seriam limpos imediatamente.

---

## Comboio Militar

Comboios militares sao grupos de veiculos destruidos estaticos que spawnam com loot militar e guardas infectados.

```xml
<event name="StaticMilitaryConvoy">
    <nominal>5</nominal>
    <min>3</min>
    <max>5</max>
    <lifetime>1800</lifetime>
    <restock>0</restock>
    <saferadius>1000</saferadius>
    <distanceradius>500</distanceradius>
    <cleanupradius>200</cleanupradius>
    <secondary>InfectedArmy</secondary>
    <flags deletable="1" init_random="0" remove_damaged="0"/>
    <position>fixed</position>
    <limit>mixed</limit>
    <active>1</active>
    <children>
        <child lootmax="10" lootmin="5" max="5" min="3" type="Wreck_V3S"/>
    </children>
</event>
```

Comboios funcionam de forma identica a helicrashes: a tag `<secondary>` spawna `InfectedArmy` ao redor do local, e itens de loot com `deloot="1"` aparecem nos destrocos. Com `nominal=5`, ate 5 locais de comboio existem no mapa simultaneamente. Cada um dura 1800 segundos (30 minutos) antes de mudar para um novo local.

---

## Carro de Policia

Eventos de carros de policia spawnam veiculos policiais destruidos com infectados do tipo policia nas proximidades. Eles sao **desativados por padrao**.

```xml
<event name="StaticPoliceCar">
    <nominal>10</nominal>
    <min>5</min>
    <max>10</max>
    <lifetime>2500</lifetime>
    <restock>0</restock>
    <saferadius>500</saferadius>
    <distanceradius>200</distanceradius>
    <cleanupradius>100</cleanupradius>
    <secondary>InfectedPoliceHard</secondary>
    <flags deletable="1" init_random="0" remove_damaged="0"/>
    <position>fixed</position>
    <limit>mixed</limit>
    <active>0</active>
    <children>
        <child lootmax="5" lootmin="3" max="10" min="5" type="Wreck_PoliceCar"/>
    </children>
</event>
```

**`active=0`** significa que este evento esta desativado por padrao -- altere para `1` para ativa-lo. A tag `<secondary>InfectedPoliceHard</secondary>` spawna zumbis policiais variante hard (mais resistentes que infectados padrao). Com `nominal=10` e `saferadius=500`, carros de policia sao mais numerosos mas menos valiosos que helicrashes.

---

## cfgeventgroups.xml -- Spawns Agrupados

Este arquivo define eventos onde multiplos objetos spawnam juntos com offsets posicionais relativos. O uso mais comum sao trens abandonados.

```xml
<event name="Train_Abandoned_Cherno">
    <children>
        <child type="Land_Train_Wagon_Tanker_Blue" x="0" z="0" a="0"/>
        <child type="Land_Train_Wagon_Box_Brown" x="0" z="15" a="0"/>
        <child type="Land_Train_Wagon_Flatbed_Green" x="0" z="30" a="0"/>
        <child type="Land_Train_Engine_Blue" x="0" z="45" a="0"/>
    </children>
</event>
```

O primeiro filho e colocado na posicao do `cfgeventspawns.xml`. Filhos subsequentes sao deslocados pelos seus valores `x`, `z`, `a` relativos a essa origem. Neste exemplo, os vagoes estao espacados 15 metros ao longo do eixo z.

Cada `<child>` em um grupo tem:

| Atributo | Descricao |
|-----------|-------------|
| `type` | Nome de classe do objeto a spawnar. |
| `x` | Deslocamento X em metros da origem do grupo. |
| `z` | Deslocamento Z em metros da origem do grupo. |
| `a` | Deslocamento de angulo em graus da origem do grupo. |

O evento de grupo ainda precisa de uma entrada correspondente no `events.xml` para controlar contagens nominais, lifetime e estado ativo.

---

## Classe Raiz de Veiculo no cfgeconomycore.xml

Para o CE reconhecer veiculos como entidades rastreaveis, eles devem ter uma declaracao de classe raiz no `cfgeconomycore.xml`:

```xml
<economycore>
    <classes>
        <rootclass name="CarScript" act="car"/>
        <rootclass name="BoatScript" act="car"/>
    </classes>
</economycore>
```

- **`CarScript`** e a classe base para todos os veiculos terrestres no DayZ.
- **`BoatScript`** e a classe base para todos os barcos.
- O atributo `act="car"` diz ao CE para tratar essas entidades com comportamento especifico de veiculos (persistencia, spawn baseado em eventos).

Sem essas entradas de classe raiz, o CE nao rastrearia ou gerenciaria instancias de veiculos. Se voce adicionar um veiculo moddado que herda de uma classe base diferente, voce pode precisar adicionar sua classe raiz aqui.

---

## Erros Comuns

Estes sao os problemas de spawn de veiculos mais frequentes encontrados por admins de servidores.

### Colocando veiculos no types.xml

**Problema:** Voce adiciona `CivilianSedan` ao `types.xml` com nominal de 10. Nenhum sedan spawna.

**Solucao:** Remova o veiculo do `types.xml`. Adicione ou edite o evento de veiculo no `events.xml` com os filhos apropriados, e garanta que posicoes de spawn correspondentes existam no `cfgeventspawns.xml`. Veiculos usam o sistema de eventos, nao o sistema de spawn de itens.

### Sem posicoes de spawn correspondentes no cfgeventspawns.xml

**Problema:** Voce cria um novo evento de veiculo no `events.xml` mas o veiculo nunca aparece.

**Solucao:** Adicione um bloco `<event name="NomeDoSeuEvento">` correspondente no `cfgeventspawns.xml` com entradas `<pos>` suficientes. O `name` do evento em ambos os arquivos deve corresponder exatamente. Voce precisa de pelo menos tantas posicoes quanto o seu valor de `nominal`.

### Definindo remove_damaged=0 para veiculos dirigiveis

**Problema:** Voce define `remove_damaged="0"` em um evento de veiculo. Com o tempo, o servidor enche de veiculos destruidos que nunca desaparecem, bloqueando posicoes de spawn e prejudicando a performance.

**Solucao:** Mantenha `remove_damaged="1"` para todos os veiculos dirigiveis (sedans, caminhoes, hatchbacks, barcos). Isso garante que quando um veiculo e destruido, o CE o remove e spawna um novo. So defina `remove_damaged="0"` para objetos de destrocos (helicrashes, comboios) que ja sao danificados por design.

### Esquecendo de definir active=1

**Problema:** Voce configura um evento de veiculo mas ele nunca spawna.

**Solucao:** Verifique a tag `<active>`. Se estiver definida como `0`, o evento esta desativado. Alguns eventos vanilla como `StaticPoliceCar` vem com `active=0`. Defina como `1` para ativar o spawn.

### Posicoes de spawn insuficientes para a contagem nominal

**Problema:** Voce define `nominal=15` para um evento de veiculo mas apenas 6 posicoes existem no `cfgeventspawns.xml`. Apenas 6 veiculos spawnam.

**Solucao:** Adicione mais entradas `<pos>`. Como regra, inclua pelo menos 2-3x o seu valor nominal em posicoes para dar ao CE opcoes suficientes para satisfazer restricoes de `saferadius` e `distanceradius`.

### Veiculo spawna dentro de construcoes ou subterraneo

**Problema:** Um veiculo spawna clipado dentro de uma construcao ou enterrado no terreno.

**Solucao:** Revise as coordenadas `<pos>` no `cfgeventspawns.xml`. Teste posicoes in-game usando teleporte de admin antes de adiciona-las ao arquivo. Posicoes devem estar em estradas planas ou terreno aberto, e o angulo (`a`) deve se alinhar com a direcao da estrada.

---

[Inicio](../README.md) | [<< Anterior: Economia de Loot](04-loot-economy.md) | [Proximo: Spawn de Jogadores >>](06-player-spawning.md)
