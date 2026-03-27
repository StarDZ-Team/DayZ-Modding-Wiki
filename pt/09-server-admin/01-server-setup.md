# Chapter 9.1: Configuracao do Servidor e Primeiro Lancamento

[Inicio](../README.md) | **Configuracao do Servidor** | [Proximo: Estrutura de Diretorios >>](02-directory-structure.md)

---

> **Resumo:** Instale um servidor dedicado DayZ Standalone do zero usando SteamCMD, inicie-o com uma configuracao minima, verifique se ele aparece no navegador de servidores e conecte-se como jogador. Este capitulo cobre tudo, desde requisitos de hardware ate a correcao dos problemas mais comuns no primeiro lancamento.

---

## Sumario

- [Pre-requisitos](#pre-requisitos)
- [Instalando o SteamCMD](#instalando-o-steamcmd)
- [Instalando o Servidor DayZ](#instalando-o-servidor-dayz)
- [Diretorio Apos Instalacao](#diretorio-apos-instalacao)
- [Primeiro Lancamento com Configuracao Minima](#primeiro-lancamento-com-configuracao-minima)
- [Verificando se o Servidor Esta Rodando](#verificando-se-o-servidor-esta-rodando)
- [Conectando como Jogador](#conectando-como-jogador)
- [Problemas Comuns no Primeiro Lancamento](#problemas-comuns-no-primeiro-lancamento)

---

## Pre-requisitos

### Hardware

| Componente | Minimo | Recomendado |
|-----------|---------|-------------|
| CPU | 4 nucleos, 2.4 GHz | 6+ nucleos, 3.5 GHz |
| RAM | 8 GB | 16 GB |
| Disco | 20 GB SSD | 40 GB NVMe SSD |
| Rede | 10 Mbps de upload | 50+ Mbps de upload |
| SO | Windows Server 2016 / Ubuntu 20.04 | Windows Server 2022 / Ubuntu 22.04 |

O servidor DayZ usa uma unica thread para a logica de gameplay. A frequencia do clock importa mais do que a quantidade de nucleos.

### Software

- **SteamCMD** -- o cliente Steam via linha de comando para instalar servidores dedicados
- **Visual C++ Redistributable 2019** (Windows) -- necessario pelo `DayZServer_x64.exe`
- **DirectX Runtime** (Windows) -- geralmente ja esta presente
- Portas **2302-2305 UDP** redirecionadas no seu roteador/firewall

---

## Instalando o SteamCMD

### Windows

1. Baixe o SteamCMD em https://developer.valvesoftware.com/wiki/SteamCMD
2. Extraia `steamcmd.exe` para uma pasta permanente, ex. `C:\SteamCMD\`
3. Execute `steamcmd.exe` uma vez -- ele se atualiza automaticamente

### Linux

```bash
sudo add-apt-repository multiverse
sudo dpkg --add-architecture i386
sudo apt update
sudo apt install steamcmd
```

---

## Instalando o Servidor DayZ

O App ID do DayZ Server no Steam e **223350**. Voce pode instala-lo sem fazer login em uma conta Steam que possua o DayZ.

### Instalacao em Uma Linha (Windows)

```batch
C:\SteamCMD\steamcmd.exe +force_install_dir "C:\DayZServer" +login anonymous +app_update 223350 validate +quit
```

### Instalacao em Uma Linha (Linux)

```bash
steamcmd +force_install_dir /home/dayz/server +login anonymous +app_update 223350 validate +quit
```

### Script de Atualizacao

Crie um script que voce pode re-executar sempre que sair um patch:

```batch
@echo off
C:\SteamCMD\steamcmd.exe ^
  +force_install_dir "C:\DayZServer" ^
  +login anonymous ^
  +app_update 223350 validate ^
  +quit
echo Atualizacao completa.
pause
```

A flag `validate` verifica todos os arquivos em busca de corrupcao. Em uma instalacao nova, espere um download de 2-3 GB.

---

## Diretorio Apos Instalacao

Apos a instalacao, a raiz do servidor fica assim:

```
DayZServer/
  DayZServer_x64.exe        # O executavel do servidor
  serverDZ.cfg               # Configuracao principal do servidor
  dayzsetting.xml            # Configuracoes de renderizacao/video (nao relevante para dedicado)
  addons/                    # Arquivos PBO vanilla (ai.pbo, animals.pbo, etc.)
  battleye/                  # Anti-cheat BattlEye (BEServer_x64.dll)
  dta/                       # Dados do engine (bin.pbo, scripts.pbo, gui.pbo)
  keys/                      # Chaves de assinatura (dayz.bikey para vanilla)
  logs/                      # Logs do engine (conexao, conteudo, audio)
  mpmissions/                # Pastas de missao
    dayzOffline.chernarusplus/   # Missao de Chernarus
    dayzOffline.enoch/           # Missao de Livonia (DLC)
    dayzOffline.sakhal/          # Missao de Sakhal (DLC)
  profiles/                  # Saida em tempo de execucao: logs RPT, logs de script, BD de jogadores
  ban.txt                    # Lista de jogadores banidos (Steam64 IDs)
  whitelist.txt              # Jogadores na whitelist (Steam64 IDs)
  steam_appid.txt            # Contem "221100"
```

Pontos importantes:
- **Voce edita** `serverDZ.cfg` e arquivos dentro de `mpmissions/`.
- **Voce nunca edita** arquivos em `addons/` ou `dta/` -- eles sao sobrescritos a cada atualizacao.
- **PBOs de mods** vao na raiz do servidor ou em uma subpasta (coberto em um capitulo posterior).
- **`profiles/`** e criado no primeiro lancamento e contem seus logs de script e dumps de crash.

---

## Primeiro Lancamento com Configuracao Minima

### Passo 1: Editar serverDZ.cfg

Abra `serverDZ.cfg` em um editor de texto. Para um primeiro teste, use a configuracao mais simples possivel:

```cpp
hostname = "My Test Server";
password = "";
passwordAdmin = "changeme123";
maxPlayers = 10;
verifySignatures = 2;
forceSameBuild = 1;
disableVoN = 0;
vonCodecQuality = 20;
disable3rdPerson = 0;
disableCrosshair = 0;
disablePersonalLight = 1;
lightingConfig = 0;
serverTime = "SystemTime";
serverTimeAcceleration = 12;
serverNightTimeAcceleration = 4;
serverTimePersistent = 0;
guaranteedUpdates = 1;
loginQueueConcurrentPlayers = 5;
loginQueueMaxPlayers = 500;
instanceId = 1;
storageAutoFix = 1;

class Missions
{
    class DayZ
    {
        template = "dayzOffline.chernarusplus";
    };
};
```

### Passo 2: Iniciar o Servidor

Abra um Prompt de Comando no diretorio do servidor e execute:

```batch
DayZServer_x64.exe -config=serverDZ.cfg -port=2302 -profiles=profiles -dologs -adminlog -netlog -freezecheck
```

| Flag | Proposito |
|------|---------|
| `-config=serverDZ.cfg` | Caminho para o arquivo de configuracao |
| `-port=2302` | Porta principal do jogo (tambem usa 2303-2305) |
| `-profiles=profiles` | Pasta de saida para logs e dados de jogadores |
| `-dologs` | Ativar logs do servidor |
| `-adminlog` | Registrar acoes de admin |
| `-netlog` | Registrar eventos de rede |
| `-freezecheck` | Auto-reiniciar ao detectar travamento |

### Passo 3: Aguardar a Inicializacao

O servidor leva de 30 a 90 segundos para iniciar completamente. Observe a saida do console. Quando voce vir uma linha como:

```
BattlEye Server: Initialized (v1.xxx)
```

...o servidor esta pronto para conexoes.

---

## Verificando se o Servidor Esta Rodando

### Metodo 1: Log de Script

Verifique `profiles/` por um arquivo com nome como `script_YYYY-MM-DD_HH-MM-SS.log`. Abra-o e procure por:

```
SCRIPT       : ...creatingass. world
SCRIPT       : ...creating mission
```

Essas linhas confirmam que a economia foi inicializada e a missao foi carregada.

### Metodo 2: Arquivo RPT

O arquivo `.RPT` em `profiles/` mostra a saida a nivel de engine. Procure por:

```
Dedicated host created.
BattlEye Server: Initialized
```

### Metodo 3: Navegador de Servidores do Steam

Abra o Steam, va em **Visualizar > Servidores de Jogos > Favoritos**, clique em **Adicionar um Servidor**, digite `127.0.0.1:2302` (ou seu IP publico) e clique em **Encontrar jogos neste endereco**. Se o servidor aparecer, ele esta rodando e acessivel.

### Metodo 4: Porta de Consulta

Use uma ferramenta externa como https://www.battlemetrics.com/ ou o pacote npm `gamedig` para consultar a porta 27016 (porta de consulta Steam = porta do jogo + 24714).

---

## Conectando como Jogador

### Da Mesma Maquina

1. Inicie o DayZ (nao o DayZ Server -- o cliente normal do jogo)
2. Abra o **Navegador de Servidores**
3. Va para a aba **LAN** ou **Favoritos**
4. Adicione `127.0.0.1:2302` aos favoritos
5. Clique em **Conectar**

Se estiver rodando cliente e servidor na mesma maquina, use `DayZDiag_x64.exe` (o cliente de diagnostico) em vez do cliente retail. Inicie com:

```batch
"C:\Program Files (x86)\Steam\steamapps\common\DayZ\DayZDiag_x64.exe" -connect=127.0.0.1 -port=2302
```

### De Outra Maquina

Use o **IP publico** ou **IP da LAN** do seu servidor, dependendo se o cliente esta na mesma rede. As portas 2302-2305 UDP devem estar redirecionadas.

---

## Problemas Comuns no Primeiro Lancamento

### O Servidor Inicia Mas Fecha Imediatamente

**Causa:** Visual C++ Redistributable ausente ou erro de sintaxe no `serverDZ.cfg`.

**Solucao:** Instale o VC++ Redist 2019 (x64). Verifique o `serverDZ.cfg` por ponto e virgula faltando -- toda linha de parametro deve terminar com `;`.

### "BattlEye initialization failed"

**Causa:** A pasta `battleye/` esta ausente ou o antivirus esta bloqueando `BEServer_x64.dll`.

**Solucao:** Re-valide os arquivos do servidor via SteamCMD. Adicione uma excecao no antivirus para toda a pasta do servidor.

### O Servidor Roda Mas Nao Aparece no Navegador

**Causa:** Portas nao redirecionadas, ou Firewall do Windows bloqueando o executavel.

**Solucao:**
1. Adicione uma regra de entrada no Firewall do Windows para `DayZServer_x64.exe` (permitir todo UDP)
2. Redirecione as portas **2302-2305 UDP** no seu roteador
3. Verifique com um testador de portas externo se a porta 2302 UDP esta aberta no seu IP publico

### "Version Mismatch" ao Conectar

**Causa:** Servidor e cliente estao em versoes diferentes.

**Solucao:** Atualize ambos. Execute o comando de atualizacao do SteamCMD para o servidor. O cliente atualiza automaticamente pelo Steam.

### Loot Nao Aparece

**Causa:** O arquivo `init.c` esta ausente ou o Hive falhou ao inicializar.

**Solucao:** Verifique se `mpmissions/dayzOffline.chernarusplus/init.c` existe e contem `CreateHive()`. Verifique o log de script por erros.

### O Servidor Usa 100% de Um Nucleo da CPU

Isso e normal. O servidor DayZ usa uma unica thread. Nao execute multiplas instancias de servidor no mesmo nucleo -- use afinidade de processador ou maquinas separadas.

### Jogadores Aparecem como Corvos / Travados no Carregamento

**Causa:** O template da missao no `serverDZ.cfg` nao corresponde a uma pasta existente em `mpmissions/`.

**Solucao:** Verifique o valor do template. Ele deve corresponder exatamente ao nome de uma pasta:

```cpp
template = "dayzOffline.chernarusplus";  // Deve corresponder ao nome da pasta em mpmissions/
```

---

**[Inicio](../README.md)** | **Proximo:** [Estrutura de Diretorios >>](02-directory-structure.md)
