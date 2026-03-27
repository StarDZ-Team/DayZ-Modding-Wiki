# Chapter 9.7: Estado do Mundo e Persistencia

[Inicio](../README.md) | [<< Anterior: Spawn de Jogadores](06-player-spawning.md) | [Proximo: Ajuste de Performance >>](08-performance.md)

A persistencia do DayZ mantem o mundo vivo entre reinicializacoes. Entender como ela funciona permite que voce gerencie bases, planeje wipes e evite corrupcao de dados.

## Sumario

- [Como a Persistencia Funciona](#como-a-persistencia-funciona)
- [O Diretorio storage_1/](#o-diretorio-storage_1)
- [Parametros de Persistencia do globals.xml](#parametros-de-persistencia-do-globalsxml)
- [Sistema de Bandeira de Territorio](#sistema-de-bandeira-de-territorio)
- [Itens de Hoarder](#itens-de-hoarder)
- [Configuracoes de Persistencia do cfggameplay.json](#configuracoes-de-persistencia-do-cfggameplayjson)
- [Procedimentos de Wipe do Servidor](#procedimentos-de-wipe-do-servidor)
- [Estrategia de Backup](#estrategia-de-backup)
- [Erros Comuns](#erros-comuns)

---

## Como a Persistencia Funciona

O DayZ armazena o estado do mundo no diretorio `storage_1/` dentro da pasta de perfil do servidor. O ciclo e direto:

1. O servidor salva o estado do mundo periodicamente (padrao a cada ~30 minutos) e no desligamento gracioso.
2. Na reinicializacao, o servidor le `storage_1/` e restaura todos os objetos persistidos -- veiculos, bases, tendas, barris, inventarios de jogadores.
3. Itens sem persistencia (a maioria do loot no chao) sao regenerados pela Economia Central a cada reinicializacao.

Se `storage_1/` nao existir na inicializacao, o servidor cria um mundo novo sem dados de jogadores e sem estruturas construidas.

---

## O Diretorio storage_1/

Seu perfil do servidor contem `storage_1/` com estes subdiretorios e arquivos:

| Caminho | Conteudo |
|------|----------|
| `data/` | Arquivos binarios contendo objetos do mundo -- partes de base, itens colocados, posicoes de veiculos |
| `players/` | Arquivos **.save** por jogador indexados por SteamID64. Cada arquivo armazena posicao, inventario, saude, efeitos de status |
| `snapshot/` | Snapshots do estado do mundo usados durante operacoes de salvamento |
| `events.bin` / `events.xy` | Estado de eventos dinamicos -- rastreia locais de helicrash, posicoes de comboio e outros eventos spawnados |

A pasta `data/` e o grosso da persistencia. Ela contem dados serializados de objetos que o servidor le na inicializacao para reconstruir o mundo.

---

## Parametros de Persistencia do globals.xml

O arquivo **globals.xml** (na sua pasta de missao) controla timers de limpeza e comportamento de bandeiras. Estes sao os valores relevantes para persistencia:

```xml
<!-- Refresh de bandeira de territorio -->
<var name="FlagRefreshFrequency" type="0" value="432000"/>      <!-- 5 dias (segundos) -->
<var name="FlagRefreshMaxDuration" type="0" value="3456000"/>    <!-- 40 dias (segundos) -->

<!-- Timers de limpeza -->
<var name="CleanupLifetimeDefault" type="0" value="45"/>         <!-- Limpeza padrao (segundos) -->
<var name="CleanupLifetimeDeadPlayer" type="0" value="3600"/>    <!-- Corpo de jogador morto: 1 hora -->
<var name="CleanupLifetimeDeadAnimal" type="0" value="1200"/>    <!-- Animal morto: 20 minutos -->
<var name="CleanupLifetimeDeadInfected" type="0" value="330"/>   <!-- Zumbi morto: 5,5 minutos -->
<var name="CleanupLifetimeRuined" type="0" value="330"/>         <!-- Item arruinado: 5,5 minutos -->

<!-- Comportamento de limpeza -->
<var name="CleanupLifetimeLimit" type="0" value="50"/>           <!-- Max itens limpos por ciclo -->
<var name="CleanupAvoidance" type="0" value="100"/>              <!-- Pular limpeza dentro de 100m de um jogador -->
```

O valor `CleanupAvoidance` previne o servidor de despawnar objetos perto de jogadores ativos. Se um corpo morto esta dentro de 100 metros de qualquer jogador, ele permanece ate o jogador se afastar ou o timer resetar.

---

## Sistema de Bandeira de Territorio

Bandeiras de territorio sao o nucleo da persistencia de bases no DayZ. Veja como os dois valores-chave interagem:

- **FlagRefreshFrequency** (`432000` segundos = 5 dias) -- Com que frequencia voce deve interagir com sua bandeira para mante-la ativa. Va ate a bandeira e use a acao "Refresh".
- **FlagRefreshMaxDuration** (`3456000` segundos = 40 dias) -- O tempo de protecao maximo acumulado. Cada refresh adiciona ate FlagRefreshFrequency de tempo, mas o total nao pode exceder este limite.

Quando o timer de uma bandeira acaba:

1. A propria bandeira se torna elegivel para limpeza.
2. Todas as partes de construcao de base vinculadas aquela bandeira perdem sua protecao de persistencia.
3. No proximo ciclo de limpeza, partes desprotegidas comecam a despawnar.

Se voce diminuir FlagRefreshFrequency, jogadores devem visitar suas bases com mais frequencia. Se voce aumentar FlagRefreshMaxDuration, bases sobrevivem mais tempo entre visitas. Ajuste ambos os valores juntos para combinar com o estilo de jogo do seu servidor.

---

## Itens de Hoarder

No **cfgspawnabletypes.xml**, certos containers sao marcados com `<hoarder/>`. Isso os marca como itens capazes de esconderijo que contam para limites de armazenamento por jogador na Economia Central.

Os itens de hoarder vanilla sao:

| Item | Tipo |
|------|------|
| Barrel_Blue, Barrel_Green, Barrel_Red, Barrel_Yellow | Barris de armazenamento |
| CarTent, LargeTent, MediumTent, PartyTent | Tendas |
| SeaChest | Armazenamento subaquatico |
| SmallProtectorCase | Case pequeno trancavel |
| UndergroundStash | Esconderijo enterrado |
| WoodenCrate | Caixa craftavel |

Exemplo do **cfgspawnabletypes.xml**:

```xml
<type name="SeaChest">
    <hoarder/>
</type>
```

O servidor rastreia quantos itens de hoarder cada jogador colocou. Quando o limite e atingido, novas colocacoes falham ou o item mais antigo despawna (dependendo da configuracao do servidor).

---

## Configuracoes de Persistencia do cfggameplay.json

O arquivo **cfggameplay.json** na sua pasta de missao contem configuracoes que afetam a durabilidade de bases e containers:

```json
{
  "GeneralData": {
    "disableBaseDamage": false,
    "disableContainerDamage": false
  }
}
```

| Configuracao | Padrao | Efeito |
|---------|---------|--------|
| `disableBaseDamage` | `false` | Quando `true`, partes de construcao de base (paredes, portoes, torres de vigia) nao podem ser danificadas. Isso efetivamente desativa raid. |
| `disableContainerDamage` | `false` | Quando `true`, containers de armazenamento (tendas, barris, caixas) nao podem receber dano. Itens dentro permanecem seguros. |

Definir ambos como `true` cria um servidor amigavel a PvE onde bases e armazenamento sao indestrutivos. A maioria dos servidores PvP deixa ambos em `false`.

---

## Procedimentos de Wipe do Servidor

Voce tem quatro tipos de wipe, cada um mirando uma parte diferente do `storage_1/`. **Sempre pare o servidor antes de realizar qualquer wipe.**

### Wipe Completo

Delete toda a pasta `storage_1/`. O servidor cria um mundo novo na proxima inicializacao. Todas as bases, veiculos, tendas, dados de jogadores e estado de eventos sao eliminados.

### Wipe de Economia (Manter Jogadores)

Delete `storage_1/data/` mas deixe `storage_1/players/` intacto. Jogadores mantem seus personagens e inventarios, mas todos os objetos colocados (bases, tendas, barris, veiculos) sao removidos.

### Wipe de Jogadores (Manter Mundo)

Delete `storage_1/players/`. Todos os personagens de jogadores resetam para spawns frescos. Bases e objetos colocados permanecem no mundo.

### Reset de Clima / Evento

Delete `events.bin` ou `events.xy` do `storage_1/`. Isso reseta posicoes de eventos dinamicos (helicrashes, comboios). O servidor gera novos locais de evento na proxima inicializacao.

---

## Estrategia de Backup

Dados de persistencia sao irreplacaveis uma vez perdidos. Siga estas praticas:

- **Faca backup com o servidor parado.** Copie toda a pasta `storage_1/` enquanto o servidor nao estiver rodando. Copiar durante a execucao arrisca capturar um estado parcial ou corrompido.
- **Agende backups antes de reinicializacoes.** Se voce roda reinicializacoes automaticas (a cada 4-6 horas), adicione um passo de backup ao seu script de reinicializacao que copia `storage_1/` antes do processo do servidor iniciar.
- **Mantenha multiplas geracoes.** Rotacione backups para ter pelo menos 3 copias recentes. Se seu backup mais recente estiver corrompido, voce pode reverter para um anterior.
- **Armazene fora da maquina.** Copie backups para um drive separado ou armazenamento em nuvem. Uma falha de disco na maquina do servidor leva seus backups junto se estiverem no mesmo drive.

Um script de backup minimo (roda antes do inicio do servidor):

```bash
BACKUP_DIR="/path/to/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r /path/to/serverprofile/storage_1 "$BACKUP_DIR/"
```

---

## Erros Comuns

Estes aparecem repetidamente em comunidades de administradores de servidores:

| Erro | O Que Acontece | Prevencao |
|---------|-------------|------------|
| Deletar `storage_1/` com o servidor rodando | Corrupcao de dados. O servidor escreve em arquivos que nao existem mais, causando crashes ou estado parcial na proxima inicializacao. | Sempre pare o servidor primeiro. |
| Nao fazer backup antes de um wipe | Se voce acidentalmente deletar a pasta errada ou o wipe der errado, nao ha recuperacao. | Faca backup de `storage_1/` antes de cada wipe. |
| Confundir reset de clima com wipe completo | Deletar `events.xy` apenas reseta posicoes de eventos dinamicos. Nao reseta loot, bases ou jogadores. | Saiba quais arquivos controlam o que (veja a tabela de diretorios acima). |
| Bandeira nao refreshed a tempo | Apos 40 dias (FlagRefreshMaxDuration), a bandeira expira e todas as partes de base vinculadas se tornam elegiveis para limpeza. Jogadores perdem toda a sua base. | Lembre os jogadores do intervalo de refresh. Diminua FlagRefreshMaxDuration em servidores de baixa populacao. |
| Editar globals.xml com o servidor rodando | Alteracoes nao sao aplicadas ate a reinicializacao. Pior, o servidor pode sobrescrever suas edicoes no desligamento. | Edite arquivos de configuracao apenas com o servidor parado. |

---

[Inicio](../README.md) | [<< Anterior: Spawn de Jogadores](06-player-spawning.md) | [Proximo: Ajuste de Performance >>](08-performance.md)
