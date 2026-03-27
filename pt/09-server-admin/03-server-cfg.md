# Chapter 9.3: Referencia Completa do serverDZ.cfg

[Inicio](../README.md) | [<< Anterior: Estrutura de Diretorios](02-directory-structure.md) | **Referencia do serverDZ.cfg** | [Proximo: Economia de Loot em Profundidade >>](04-loot-economy.md)

---

> **Resumo:** Cada parametro do `serverDZ.cfg` documentado com seu proposito, valores validos e comportamento padrao. Este arquivo controla a identidade do servidor, configuracoes de rede, regras de gameplay, aceleracao de tempo e selecao de missao.

---

## Sumario

- [Formato do Arquivo](#formato-do-arquivo)
- [Identidade do Servidor](#identidade-do-servidor)
- [Rede e Seguranca](#rede-e-seguranca)
- [Regras de Gameplay](#regras-de-gameplay)
- [Tempo e Clima](#tempo-e-clima)
- [Performance e Fila de Login](#performance-e-fila-de-login)
- [Persistencia e Instancia](#persistencia-e-instancia)
- [Selecao de Missao](#selecao-de-missao)
- [Arquivo de Exemplo Completo](#arquivo-de-exemplo-completo)
- [Parametros de Lancamento que Sobrescrevem a Config](#parametros-de-lancamento-que-sobrescrevem-a-config)

---

## Formato do Arquivo

`serverDZ.cfg` usa o formato de configuracao da Bohemia (similar ao C). Regras:

- Toda atribuicao de parametro termina com **ponto e virgula** `;`
- Strings sao envolvidas em **aspas duplas** `""`
- Comentarios usam `//` para linha unica
- O bloco `class Missions` usa chaves `{}` e termina com `};`
- O arquivo deve ter codificacao UTF-8 ou ANSI -- sem BOM

Um ponto e virgula faltando fara o servidor falhar silenciosamente ou ignorar parametros subsequentes.

---

## Identidade do Servidor

```cpp
hostname = "My DayZ Server";         // Nome do servidor mostrado no navegador
password = "";                       // Senha para conectar (vazio = publico)
passwordAdmin = "";                  // Senha para login de admin via console in-game
description = "";                    // Descricao mostrada nos detalhes do navegador de servidores
```

| Parametro | Tipo | Padrao | Observacoes |
|-----------|------|---------|-------|
| `hostname` | string | `""` | Exibido no navegador de servidores. Max ~100 caracteres. |
| `password` | string | `""` | Deixe vazio para servidor publico. Jogadores devem digitar para entrar. |
| `passwordAdmin` | string | `""` | Usado com o comando `#login` in-game. **Defina isso em todo servidor.** |
| `description` | string | `""` | Descricoes multi-linha nao sao suportadas. Mantenha curto. |

---

## Rede e Seguranca

```cpp
maxPlayers = 60;                     // Maximo de slots de jogadores
verifySignatures = 2;                // Verificacao de assinatura PBO (apenas 2 e suportado)
forceSameBuild = 1;                  // Exigir versao correspondente cliente/servidor
enableWhitelist = 0;                 // Ativar/desativar whitelist
disableVoN = 0;                      // Desativar voz pela rede
vonCodecQuality = 20;               // Qualidade de audio VoN (0-30)
guaranteedUpdates = 1;               // Protocolo de rede (sempre use 1)
```

| Parametro | Tipo | Valores Validos | Padrao | Observacoes |
|-----------|------|-------------|---------|-------|
| `maxPlayers` | int | 1-60 | 60 | Afeta o uso de RAM. Cada jogador adiciona ~50-100 MB. |
| `verifySignatures` | int | 2 | 2 | Apenas o valor 2 e suportado. Verifica arquivos PBO contra chaves `.bisign`. |
| `forceSameBuild` | int | 0, 1 | 1 | Quando 1, clientes devem corresponder a versao exata do executavel do servidor. Sempre mantenha em 1. |
| `enableWhitelist` | int | 0, 1 | 0 | Quando 1, apenas Steam64 IDs listados em `whitelist.txt` podem conectar. |
| `disableVoN` | int | 0, 1 | 0 | Defina como 1 para desativar completamente o chat de voz in-game. |
| `vonCodecQuality` | int | 0-30 | 20 | Valores mais altos significam melhor qualidade de voz mas mais largura de banda. 20 e um bom equilibrio. |
| `guaranteedUpdates` | int | 1 | 1 | Configuracao de protocolo de rede. Sempre use 1. |

### Shard ID

```cpp
shardId = "123abc";                  // Seis caracteres alfanumericos para shards privados
```

| Parametro | Tipo | Padrao | Observacoes |
|-----------|------|---------|-------|
| `shardId` | string | `""` | Usado para servidores de hive privado. Jogadores em servidores com o mesmo `shardId` compartilham dados de personagem. Deixe vazio para hive publico. |

---

## Regras de Gameplay

```cpp
disable3rdPerson = 0;               // Desativar camera em terceira pessoa
disableCrosshair = 0;               // Desativar a mira
disablePersonalLight = 1;           // Desativar a luz ambiente do jogador
lightingConfig = 0;                 // Brilho noturno (0 = mais claro, 1 = mais escuro)
```

| Parametro | Tipo | Valores Validos | Padrao | Observacoes |
|-----------|------|-------------|---------|-------|
| `disable3rdPerson` | int | 0, 1 | 0 | Defina como 1 para servidores somente primeira pessoa. Esta e a configuracao "hardcore" mais comum. |
| `disableCrosshair` | int | 0, 1 | 0 | Defina como 1 para remover a mira. Frequentemente combinado com `disable3rdPerson=1`. |
| `disablePersonalLight` | int | 0, 1 | 1 | A "luz pessoal" e um brilho sutil ao redor do jogador a noite. A maioria dos servidores desativa (valor 1) por realismo. |
| `lightingConfig` | int | 0, 1 | 0 | 0 = noites mais claras (luar visivel). 1 = noites completamente escuras (necessita lanterna/NVG). |

---

## Tempo e Clima

```cpp
serverTime = "SystemTime";                 // Hora inicial
serverTimeAcceleration = 12;               // Multiplicador de velocidade do tempo (0-24)
serverNightTimeAcceleration = 1;           // Multiplicador de velocidade noturna (0.1-64)
serverTimePersistent = 0;                  // Salvar hora entre reinicializacoes
```

| Parametro | Tipo | Valores Validos | Padrao | Observacoes |
|-----------|------|-------------|---------|-------|
| `serverTime` | string | `"SystemTime"` ou `"YYYY/MM/DD/HH/MM"` | `"SystemTime"` | `"SystemTime"` usa o relogio local da maquina. Defina um horario fixo como `"2024/9/15/12/0"` para um servidor permanentemente diurno. |
| `serverTimeAcceleration` | int | 0-24 | 12 | Multiplicador para o tempo in-game. Em 12, um ciclo completo de 24 horas leva 2 horas reais. Em 1, o tempo e real. Em 24, um dia completo passa em 1 hora. |
| `serverNightTimeAcceleration` | float | 0.1-64 | 1 | Multiplicado por `serverTimeAcceleration`. Com valor 4 e aceleracao 12, a noite passa a 48x de velocidade (noites muito curtas). |
| `serverTimePersistent` | int | 0, 1 | 0 | Quando 1, o servidor salva o relogio in-game em disco e retoma dele apos reiniciar. Quando 0, o tempo reseta para `serverTime` a cada reinicializacao. |

### Configuracoes de Tempo Comuns

**Sempre de dia:**
```cpp
serverTime = "2024/6/15/12/0";
serverTimeAcceleration = 0;
serverTimePersistent = 0;
```

**Ciclo dia/noite rapido (dias de 2 horas, noites curtas):**
```cpp
serverTime = "SystemTime";
serverTimeAcceleration = 12;
serverNightTimeAcceleration = 4;
serverTimePersistent = 1;
```

**Dia/noite em tempo real:**
```cpp
serverTime = "SystemTime";
serverTimeAcceleration = 1;
serverNightTimeAcceleration = 1;
serverTimePersistent = 1;
```

---

## Performance e Fila de Login

```cpp
loginQueueConcurrentPlayers = 5;     // Jogadores processados simultaneamente durante login
loginQueueMaxPlayers = 500;          // Tamanho maximo da fila de login
```

| Parametro | Tipo | Padrao | Observacoes |
|-----------|------|---------|-------|
| `loginQueueConcurrentPlayers` | int | 5 | Quantos jogadores podem carregar simultaneamente. Valores mais baixos reduzem picos de carga do servidor apos reinicializacao. Aumente para 10-15 se seu hardware for forte e jogadores reclamarem de tempo de fila. |
| `loginQueueMaxPlayers` | int | 500 | Se esta quantidade de jogadores ja estiver na fila, novas conexoes sao rejeitadas. 500 e suficiente para a maioria dos servidores. |

---

## Persistencia e Instancia

```cpp
instanceId = 1;                      // Identificador da instancia do servidor
storageAutoFix = 1;                  // Auto-reparar arquivos de persistencia corrompidos
```

| Parametro | Tipo | Padrao | Observacoes |
|-----------|------|---------|-------|
| `instanceId` | int | 1 | Identifica a instancia do servidor. Dados de persistencia sao armazenados em `storage_<instanceId>/`. Se voce roda multiplos servidores na mesma maquina, de a cada um um `instanceId` diferente. |
| `storageAutoFix` | int | 1 | Quando 1, o servidor verifica arquivos de persistencia na inicializacao e substitui corrompidos por arquivos vazios. Sempre deixe em 1. |

---

## Selecao de Missao

```cpp
class Missions
{
    class DayZ
    {
        template = "dayzOffline.chernarusplus";
    };
};
```

O valor `template` deve corresponder exatamente ao nome de uma pasta dentro de `mpmissions/`. Missoes vanilla disponiveis:

| Template | Mapa | DLC Necessaria |
|----------|-----|:---:|
| `dayzOffline.chernarusplus` | Chernarus | Nao |
| `dayzOffline.enoch` | Livonia | Sim |
| `dayzOffline.sakhal` | Sakhal | Sim |

Missoes customizadas (ex.: de mods ou mapas da comunidade) usam seu proprio nome de template. A pasta deve existir em `mpmissions/`.

---

## Arquivo de Exemplo Completo

Este e o `serverDZ.cfg` padrao completo com todos os parametros:

```cpp
hostname = "EXAMPLE NAME";              // Nome do servidor
password = "";                          // Senha para conectar ao servidor
passwordAdmin = "";                     // Senha para se tornar admin do servidor

description = "";                       // Descricao no navegador de servidores

enableWhitelist = 0;                    // Ativar/desativar whitelist (valor 0-1)

maxPlayers = 60;                        // Quantidade maxima de jogadores

verifySignatures = 2;                   // Verifica .pbos contra arquivos .bisign (apenas 2 e suportado)
forceSameBuild = 1;                     // Exigir versao correspondente cliente/servidor (valor 0-1)

disableVoN = 0;                         // Ativar/desativar voz pela rede (valor 0-1)
vonCodecQuality = 20;                   // Qualidade do codec de voz (valores 0-30)

shardId = "123abc";                     // Seis caracteres alfanumericos para shard privado

disable3rdPerson = 0;                   // Alterna a visao em terceira pessoa (valor 0-1)
disableCrosshair = 0;                   // Alterna a mira (valor 0-1)

disablePersonalLight = 1;              // Desativa luz pessoal para todos os clientes
lightingConfig = 0;                     // 0 para mais claro, 1 para mais escuro a noite

serverTime = "SystemTime";             // Hora in-game inicial ("SystemTime" ou "YYYY/MM/DD/HH/MM")
serverTimeAcceleration = 12;           // Multiplicador de velocidade do tempo (0-24)
serverNightTimeAcceleration = 1;       // Multiplicador de velocidade noturna (0.1-64), tambem multiplicado por serverTimeAcceleration
serverTimePersistent = 0;              // Salvar hora entre reinicializacoes (valor 0-1)

guaranteedUpdates = 1;                 // Protocolo de rede (sempre use 1)

loginQueueConcurrentPlayers = 5;       // Jogadores processados simultaneamente durante login
loginQueueMaxPlayers = 500;            // Tamanho maximo da fila de login

instanceId = 1;                        // ID da instancia do servidor (afeta nome da pasta storage)

storageAutoFix = 1;                    // Auto-reparar persistencia corrompida (valor 0-1)

class Missions
{
    class DayZ
    {
        template = "dayzOffline.chernarusplus";
    };
};
```

---

## Parametros de Lancamento que Sobrescrevem a Config

Algumas configuracoes podem ser sobrescritas via parametros de linha de comando ao iniciar o `DayZServer_x64.exe`:

| Parametro | Sobrescreve | Exemplo |
|-----------|-----------|---------|
| `-config=` | Caminho do arquivo de configuracao | `-config=serverDZ.cfg` |
| `-port=` | Porta do jogo | `-port=2302` |
| `-profiles=` | Diretorio de saida de perfis | `-profiles=profiles` |
| `-mod=` | Mods do lado do cliente (separados por ponto e virgula) | `-mod=@CF;@VPPAdminTools` |
| `-servermod=` | Mods apenas do servidor | `-servermod=@MyServerMod` |
| `-BEpath=` | Caminho do BattlEye | `-BEpath=battleye` |
| `-dologs` | Ativar logs | -- |
| `-adminlog` | Ativar log de admin | -- |
| `-netlog` | Ativar log de rede | -- |
| `-freezecheck` | Auto-reiniciar ao travar | -- |
| `-cpuCount=` | Nucleos de CPU a usar | `-cpuCount=4` |
| `-noFilePatching` | Desativar file patching | -- |

### Exemplo de Lancamento Completo

```batch
start DayZServer_x64.exe ^
  -config=serverDZ.cfg ^
  -port=2302 ^
  -profiles=profiles ^
  -mod=@CF;@VPPAdminTools;@MyMod ^
  -servermod=@MyServerOnlyMod ^
  -dologs -adminlog -netlog -freezecheck
```

Mods sao carregados na ordem especificada em `-mod=`. A ordem de dependencia importa: se o Mod B requer o Mod A, liste o Mod A primeiro.

---

**Anterior:** [Estrutura de Diretorios](02-directory-structure.md) | [Inicio](../README.md) | **Proximo:** [Economia de Loot em Profundidade >>](04-loot-economy.md)
