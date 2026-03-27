# Chapter 9.11: Solucao de Problemas do Servidor

[Inicio](../README.md) | [<< Anterior: Gerenciamento de Mods](10-mod-management.md) | [Proximo: Topicos Avancados >>](12-advanced.md)

---

> **Resumo:** Diagnostique e corrija os problemas mais comuns de servidores DayZ -- falhas de inicializacao, problemas de conexao, crashes, loot e spawn de veiculos, persistencia e performance. Toda solucao aqui vem de padroes reais de falha em milhares de relatos da comunidade.

---

## Sumario

- [O Servidor Nao Inicia](#o-servidor-nao-inicia)
- [Jogadores Nao Conseguem Conectar](#jogadores-nao-conseguem-conectar)
- [Crashes e Null Pointers](#crashes-e-null-pointers)
- [Loot Nao Spawna](#loot-nao-spawna)
- [Veiculos Nao Spawnam](#veiculos-nao-spawnam)
- [Problemas de Persistencia](#problemas-de-persistencia)
- [Problemas de Performance](#problemas-de-performance)
- [Lendo Arquivos de Log](#lendo-arquivos-de-log)
- [Checklist Rapido de Diagnostico](#checklist-rapido-de-diagnostico)

---

## O Servidor Nao Inicia

### Arquivos DLL Faltando

Se `DayZServer_x64.exe` crasha imediatamente com erro de DLL faltando, instale o **Visual C++ Redistributable for Visual Studio 2019** (x64) mais recente do site oficial da Microsoft e reinicie.

### Porta Ja em Uso

Outra instancia do DayZ ou aplicacao esta ocupando a porta 2302. Verifique com `netstat -ano | findstr 2302` (Windows) ou `ss -tulnp | grep 2302` (Linux). Encerre o processo conflitante ou mude sua porta com `-port=2402`.

### Pasta de Missao Faltando

O servidor espera `mpmissions/<template>/` onde o nome da pasta corresponde exatamente ao valor `template` no **serverDZ.cfg**. Para Chernarus, isso e `mpmissions/dayzOffline.chernarusplus/` e deve conter pelo menos o **init.c**.

### serverDZ.cfg Invalido

Um unico ponto e virgula faltando ou tipo de aspas errado impede a inicializacao silenciosamente. Fique atento a:

- `;` faltando no final das linhas de valor
- Aspas inteligentes em vez de aspas retas
- `{};` faltando ao redor de entradas de classe

### Arquivos de Mod Faltando

Todo caminho em `-mod=@CF;@VPPAdminTools;@MyMod` deve existir relativo a raiz do servidor e conter uma pasta **addons/** com arquivos `.pbo`. Um unico caminho invalido impede a inicializacao.

---

## Jogadores Nao Conseguem Conectar

### Redirecionamento de Portas

O DayZ requer estas portas redirecionadas e abertas no seu firewall:

| Porta | Protocolo | Proposito |
|------|----------|---------|
| 2302 | UDP | Trafego do jogo |
| 2303 | UDP | Rede Steam |
| 2304 | UDP | Consulta Steam (interna) |
| 27016 | UDP | Consulta do navegador de servidores Steam |

Se voce mudou a porta base com `-port=`, todas as outras portas mudam pelo mesmo offset.

### Bloqueio de Firewall

Adicione **DayZServer_x64.exe** as excecoes do firewall do SO. No Windows: `netsh advfirewall firewall add rule name="DayZ Server" dir=in action=allow program="C:\DayZServer\DayZServer_x64.exe" enable=yes`. No Linux, abra as portas com `ufw` ou `iptables`.

### Incompatibilidade de Mods

Clientes devem ter exatamente as mesmas versoes de mods que o servidor. Se um jogador ve "Mod mismatch", um dos lados tem uma versao desatualizada. Atualize ambos quando qualquer mod receber uma atualizacao da Workshop.

### Arquivos .bikey Faltando

Todo arquivo `.bikey` de mod deve estar no diretorio `keys/` do servidor. Sem ele, o BattlEye rejeita os PBOs assinados do cliente. Procure dentro da pasta `keys/` ou `key/` de cada mod.

### Servidor Cheio

Verifique `maxPlayers` no **serverDZ.cfg** (padrao 60).

---

## Crashes e Null Pointers

### Acesso a Null Pointer

`SCRIPT (E): Null pointer access in 'MyClass.SomeMethod'` -- o erro de script mais comum. Um mod esta chamando um metodo em um objeto deletado ou nao inicializado. Isso e um bug do mod, nao uma configuracao errada do servidor. Reporte ao autor do mod com o log RPT completo.

### Encontrando Erros de Script

Procure no log RPT por `SCRIPT (E)`. O nome da classe e metodo no erro indica qual mod e responsavel. Localizacoes do RPT:

- **Servidor:** diretorio `$profiles/` (ou raiz do servidor se nenhum `-profiles=` foi definido)
- **Cliente:** `%localappdata%\DayZ\`

### Crash ao Reiniciar

Se o servidor crasha a cada reinicializacao, **storage_1/** pode estar corrompido. Pare o servidor, faca backup de `storage_1/`, delete `storage_1/data/events.bin` e reinicie. Se isso falhar, delete todo o diretorio `storage_1/` (limpa toda a persistencia).

### Crash Apos Atualizacao de Mod

Reverta para a versao anterior do mod. Verifique o changelog da Workshop por mudancas que quebram -- classes renomeadas, configs removidos e formatos de RPC alterados sao causas comuns.

---

## Loot Nao Spawna

### types.xml Nao Registrado

Itens definidos no **types.xml** nao spawnarao a menos que o arquivo esteja registrado no **cfgeconomycore.xml**:

```xml
<economycore>
    <ce folder="db">
        <file name="types.xml" type="types" />
    </ce>
</economycore>
```

Se voce usa um arquivo de types customizado (ex.: **types_custom.xml**), adicione uma entrada `<file>` separada para ele.

### Tags de Category, Usage ou Value Erradas

Toda tag `<category>`, `<usage>` e `<value>` no seu types.xml deve corresponder a um nome definido no **cfglimitsdefinition.xml**. Um erro de digitacao como `usage name="Military"` (M maiusculo) quando a definicao diz `military` (minusculo) silenciosamente impede o item de spawnar.

### Nominal Definido como Zero

Se `nominal` e `0`, o CE nunca spawnara aquele item. Isso e intencional para itens que devem existir apenas via crafting, eventos ou colocacao de admin. Se voce quer que o item spawne naturalmente, defina `nominal` como pelo menos `1`.

### Posicoes de Grupo de Mapa Faltando

Itens precisam de posicoes de spawn validas dentro de construcoes. Se um item customizado nao tem posicoes de grupo de mapa correspondentes (definidas no **mapgroupproto.xml**), o CE nao tem onde coloca-lo. Atribua o item a categorias e usos que ja tem posicoes validas no mapa.

---

## Veiculos Nao Spawnam

Veiculos usam o sistema de eventos, **nao** o types.xml.

### Configuracao do events.xml

Spawns de veiculos sao definidos no **events.xml**:

```xml
<event name="VehicleOffroadHatchback">
    <nominal>8</nominal>
    <min>5</min>
    <max>8</max>
    <lifetime>3888000</lifetime>
    <restock>0</restock>
    <saferadius>500</saferadius>
    <distanceradius>500</distanceradius>
    <cleanupradius>200</cleanupradius>
    <flags deletable="0" init_random="0" remove_damaged="1"/>
    <position>fixed</position>
    <limit>child</limit>
    <active>1</active>
    <children>
        <child lootmax="0" lootmin="0" max="1" min="1" type="OffroadHatchback"/>
    </children>
</event>
```

### Posicoes de Spawn Faltando

Eventos de veiculos com `<position>fixed</position>` requerem entradas no **cfgeventspawns.xml**. Sem coordenadas definidas, o evento nao tem onde colocar o veiculo.

### Evento Desativado

Se `<active>0</active>`, o evento esta completamente desativado. Defina como `1`.

### Veiculos Danificados Bloqueando Slots

Se `remove_damaged="0"`, veiculos destruidos permanecem no mundo para sempre e ocupam slots de spawn. Defina `remove_damaged="1"` para que o CE limpe destrocos e spawne substitutos.

---

## Problemas de Persistencia

### Bases Desaparecendo

Bandeiras de territorio devem ser refreshed antes do timer expirar. O `FlagRefreshFrequency` padrao e `432000` segundos (5 dias). Se nenhum jogador interagir com a bandeira dentro daquela janela, a bandeira e todos os objetos dentro do raio sao deletados.

Verifique o valor no **globals.xml**:

```xml
<var name="FlagRefreshFrequency" type="0" value="432000"/>
```

Aumente este valor em servidores de baixa populacao onde jogadores fazem login com menos frequencia.

### Itens Desaparecendo Apos Reinicializacao

Todo item tem um `lifetime` no **types.xml** (segundos). Quando ele expira sem interacao do jogador, o CE o remove. Referencia: `3888000` = 45 dias, `604800` = 7 dias, `14400` = 4 horas. Itens dentro de containers herdam o lifetime do container.

### storage_1/ Crescendo Demais

Se seu diretorio `storage_1/` cresce alem de varias centenas de MB, sua economia esta produzindo itens demais. Reduza valores de `nominal` no seu types.xml, especialmente para itens de alta contagem como comida, roupas e municao. Um arquivo de persistencia inchado causa tempos de reinicializacao mais longos.

### Dados de Jogadores Perdidos

Inventarios e posicoes de jogadores sao armazenados em `storage_1/players/`. Se este diretorio for deletado ou corrompido, todos os jogadores spawnam frescos. Faca backup de `storage_1/` regularmente.

---

## Problemas de Performance

### FPS do Servidor Caindo

Servidores DayZ miram 30+ FPS para gameplay suave. Causas comuns de FPS baixo no servidor:

- **Muitos zumbis** -- reduza `ZombieMaxCount` no **globals.xml** (padrao 800, tente 400-600)
- **Muitos animais** -- reduza `AnimalMaxCount` (padrao 200, tente 100)
- **Loot excessivo** -- diminua valores de `nominal` no seu types.xml
- **Muitos objetos de base** -- bases grandes com centenas de itens sobrecarregam a persistencia
- **Mods pesados em script** -- alguns mods rodam logica cara por frame

### Desync

Jogadores experimentando rubber-banding, acoes atrasadas ou zumbis invisiveis sao sintomas de desync. Isso quase sempre significa que o FPS do servidor caiu abaixo de 15. Corrija o problema de performance subjacente em vez de procurar uma configuracao especifica de desync.

### Tempos de Reinicializacao Longos

O tempo de reinicializacao e diretamente proporcional ao tamanho de `storage_1/`. Se reinicializacoes levam mais de 2-3 minutos, voce tem muitos objetos persistentes. Reduza valores nominais de loot e defina lifetimes apropriados.

---

## Lendo Arquivos de Log

### Localizacao do RPT do Servidor

O arquivo RPT esta em `$profiles/` (se lancado com `-profiles=`) ou na raiz do servidor. Padrao de nome: `DayZServer_x64_<data>_<hora>.RPT`.

### O Que Procurar

| Termo de busca | Significado |
|-------------|---------|
| `SCRIPT (E)` | Erro de script -- um mod tem um bug |
| `[ERROR]` | Erro a nivel de engine |
| `ErrorMessage` | Erro fatal que pode causar desligamento |
| `Cannot open` | Arquivo faltando (PBO, config, missao) |
| `Crash` | Crash a nivel de aplicacao |

### Logs do BattlEye

Logs do BattlEye estao no diretorio `BattlEye/` dentro da raiz do servidor. Eles mostram eventos de kick e ban. Se jogadores relatam ser kickados inesperadamente, verifique aqui primeiro.

---

## Checklist Rapido de Diagnostico

Quando algo da errado, trabalhe por esta lista em ordem:

```
1. Verifique o RPT do servidor por linhas SCRIPT (E) e [ERROR]
2. Verifique se todo caminho de -mod= existe e contem addons/*.pbo
3. Verifique se todos os arquivos .bikey estao copiados para keys/
4. Verifique o serverDZ.cfg por erros de sintaxe (pontos e virgulas faltando)
5. Verifique redirecionamento de portas: 2302 UDP + 27016 UDP
6. Verifique se a pasta de missao corresponde ao valor template no serverDZ.cfg
7. Verifique storage_1/ por corrupcao (delete events.bin se necessario)
8. Teste com zero mods primeiro, depois adicione mods um por vez
```

O passo 8 e a tecnica mais poderosa. Se o servidor funciona vanilla mas quebra com mods, voce pode isolar o mod problematico atraves de busca binaria -- adicione metade dos seus mods, teste, e va estreitando.

---

[Inicio](../README.md) | [<< Anterior: Gerenciamento de Mods](10-mod-management.md) | [Proximo: Topicos Avancados >>](12-advanced.md)
