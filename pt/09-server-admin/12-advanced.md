# Chapter 9.12: Topicos Avancados de Servidor

[Inicio](../README.md) | [<< Anterior: Solucao de Problemas](11-troubleshooting.md) | [Inicio da Parte 9](01-server-setup.md)

---

> **Resumo:** Arquivos de configuracao profunda, setups multi-mapa, divisao de economia, territorios de animais, eventos dinamicos, controle de clima, reinicializacoes automatizadas e o sistema de mensagens.

---

## Sumario

- [Mergulho Profundo no cfggameplay.json](#mergulho-profundo-no-cfggameplayjson)
- [Servidores Multi-Mapa](#servidores-multi-mapa)
- [Ajuste Customizado da Economia](#ajuste-customizado-da-economia)
- [cfgenvironment.xml e Territorios de Animais](#cfgenvironmentxml-e-territorios-de-animais)
- [Eventos Dinamicos Customizados](#eventos-dinamicos-customizados)
- [Automacao de Reinicializacao do Servidor](#automacao-de-reinicializacao-do-servidor)
- [cfgweather.xml](#cfgweatherxml)
- [Sistema de Mensagens](#sistema-de-mensagens)

---

## Mergulho Profundo no cfggameplay.json

O arquivo **cfggameplay.json** fica na sua pasta de missao e sobrescreve padroes de gameplay hardcoded. Ative-o no **serverDZ.cfg** primeiro:

```cpp
enableCfgGameplayFile = 1;
```

Estrutura vanilla:

```json
{
  "version": 123,
  "GeneralData": {
    "disableBaseDamage": false,
    "disableContainerDamage": false,
    "disableRespawnDialog": false,
    "disableRespawnInUnconsciousness": false
  },
  "PlayerData": {
    "disablePersonalLight": false,
    "StaminaData": {
      "sprintStaminaModifierErc": 1.0, "sprintStaminaModifierCro": 1.0,
      "staminaWeightLimitThreshold": 6000.0, "staminaMax": 100.0,
      "staminaKg": 0.3, "staminaMin": 0.0,
      "staminaDepletionSpeed": 1.0, "staminaRecoverySpeed": 1.0
    },
    "ShockHandlingData": {
      "shockRefillSpeedConscious": 5.0, "shockRefillSpeedUnconscious": 1.0,
      "allowRefillSpeedModifier": true
    },
    "MovementData": {
      "timeToSprint": 0.45, "timeToJog": 0.0,
      "rotationSpeedJog": 0.3, "rotationSpeedSprint": 0.15
    },
    "DrowningData": {
      "staminaDepletionSpeed": 10.0, "healthDepletionSpeed": 3.0,
      "shockDepletionSpeed": 10.0
    },
    "WeaponObstructionData": { "staticMode": 1, "dynamicMode": 1 }
  },
  "WorldsData": {
    "lightingConfig": 0, "objectSpawnersArr": [],
    "environmentMinTemps": [-3, -2, 0, 4, 9, 14, 18, 17, 13, 11, 9, 0],
    "environmentMaxTemps": [3, 5, 7, 14, 19, 24, 26, 25, 18, 14, 10, 5]
  },
  "BaseBuildingData": { "canBuildAnywhere": false, "canCraftAnywhere": false },
  "UIData": {
    "use3DMap": false,
    "HitIndicationData": {
      "hitDirectionOverrideEnabled": false, "hitDirectionBehaviour": 1,
      "hitDirectionStyle": 0, "hitDirectionIndicatorColorStr": "0xffbb0a1e",
      "hitDirectionMaxDuration": 2.0, "hitDirectionBreakPointRelative": 0.2,
      "hitDirectionScatter": 10.0, "hitIndicationPostProcessEnabled": true
    }
  }
}
```

- `version` -- deve corresponder ao que o binario do servidor espera. Nao altere.
- `lightingConfig` -- `0` (padrao) ou `1` (noites mais claras).
- `environmentMinTemps` / `environmentMaxTemps` -- 12 valores, um por mes (Jan-Dez).
- `disablePersonalLight` -- remove a luz ambiente tenue perto de novos jogadores a noite.
- `staminaMax` e modificadores de sprint controlam ate onde jogadores podem correr antes da exaustao.
- `use3DMap` -- troca o mapa in-game para a variante 3D renderizada no terreno.

---

## Servidores Multi-Mapa

O DayZ suporta multiplos mapas atraves de diferentes pastas de missao dentro de `mpmissions/`:

| Mapa | Pasta de Missao |
|-----|---------------|
| Chernarus | `mpmissions/dayzOffline.chernarusplus/` |
| Livonia | `mpmissions/dayzOffline.enoch/` |
| Sakhal | `mpmissions/dayzOffline.sakhal/` |

Cada mapa tem seus proprios arquivos de CE (`types.xml`, `events.xml`, etc.). Troque de mapa via `template` no **serverDZ.cfg**:

```cpp
class Missions {
    class DayZ {
        template = "dayzOffline.chernarusplus";
    };
};
```

Ou com um parametro de lancamento: `-mission=mpmissions/dayzOffline.enoch`

Para rodar multiplos mapas simultaneamente, use instancias de servidor separadas com sua propria config, diretorio de perfil e faixa de portas.

---

## Ajuste Customizado da Economia

### Dividindo o types.xml

Divida itens em multiplos arquivos e registre-os no **cfgeconomycore.xml**:

```xml
<economycore>
    <ce folder="db">
        <file name="types.xml" type="types" />
        <file name="types_weapons.xml" type="types" />
        <file name="types_vehicles.xml" type="types" />
    </ce>
</economycore>
```

O servidor carrega e mescla todos os arquivos com `type="types"`.

### Categorias e Tags Customizadas

**cfglimitsdefinition.xml** define categorias/tags para o `types.xml` mas e sobrescrito em atualizacoes. Use **cfglimitsdefinitionuser.xml** em vez disso:

```xml
<lists>
    <categories>
        <category name="custom_rare" />
    </categories>
    <tags>
        <tag name="custom_event" />
    </tags>
</lists>
```

---

## cfgenvironment.xml e Territorios de Animais

O arquivo **cfgenvironment.xml** na sua pasta de missao linka para arquivos de territorio no subdiretorio `env/`:

```xml
<env>
    <territories>
        <file path="env/zombie_territories.xml" />
        <file path="env/bear_territories.xml" />
        <file path="env/wolf_territories.xml" />
    </territories>
</env>
```

A pasta `env/` contem estes arquivos de territorio de animais:

| Arquivo | Animais |
|------|---------|
| **bear_territories.xml** | Ursos pardos |
| **wolf_territories.xml** | Alcateias de lobos |
| **fox_territories.xml** | Raposas |
| **hare_territories.xml** | Coelhos/lebres |
| **hen_territories.xml** | Galinhas |
| **pig_territories.xml** | Porcos |
| **red_deer_territories.xml** | Cervos vermelhos |
| **roe_deer_territories.xml** | Cervos-roe |
| **sheep_goat_territories.xml** | Ovelhas/cabras |
| **wild_boar_territories.xml** | Javalis |
| **cattle_territories.xml** | Vacas |

Uma entrada de territorio define zonas circulares com posicao e contagem de animais:

```xml
<territory color="4291543295" name="BearTerritory 001">
    <zone name="Bear zone" smin="-1" smax="-1" dmin="1" dmax="4" x="7628" z="5048" r="500" />
</territory>
```

- `x`, `z` -- coordenadas do centro; `r` -- raio em metros
- `dmin`, `dmax` -- contagem minima/maxima de animais na zona
- `smin`, `smax` -- reservado (defina como `-1`)

---

## Eventos Dinamicos Customizados

Eventos dinamicos (helicrashes, comboios) sao definidos no **events.xml**. Para criar um evento customizado:

**1. Defina o evento** no **events.xml**:

```xml
<event name="StaticMyCustomCrash">
    <nominal>3</nominal> <min>1</min> <max>5</max>
    <lifetime>1800</lifetime> <restock>600</restock>
    <saferadius>500</saferadius> <distanceradius>200</distanceradius> <cleanupradius>100</cleanupradius>
    <flags deletable="0" init_random="0" remove_damaged="1" />
    <position>fixed</position> <limit>child</limit> <active>1</active>
    <children>
        <child lootmax="10" lootmin="5" max="3" min="1" type="Wreck_Mi8_Crashed" />
    </children>
</event>
```

**2. Adicione posicoes de spawn** no **cfgeventspawns.xml**:

```xml
<event name="StaticMyCustomCrash">
    <pos x="4523.2" z="9234.5" a="180" />
    <pos x="7812.1" z="3401.8" a="90" />
</event>
```

**3. Adicione guardas infectados** (opcional) -- adicione elementos `<secondary type="ZmbM_PatrolNormal_Autumn" />` na definicao do seu evento.

**4. Spawns agrupados** (opcional) -- defina clusters no **cfgeventgroups.xml** e referencie o nome do grupo no seu evento.

---

## Automacao de Reinicializacao do Servidor

O DayZ nao tem agendador de reinicializacao integrado. Use automacao a nivel de SO.

### Windows

Crie **restart_server.bat** e execute via Tarefa Agendada do Windows a cada 4-6 horas:

```batch
@echo off
taskkill /f /im DayZServer_x64.exe
timeout /t 10
xcopy /e /y "C:\DayZServer\profiles\storage_1" "C:\DayZBackups\%date:~-4%-%date:~-7,2%-%date:~-10,2%\"
C:\SteamCMD\steamcmd.exe +force_install_dir C:\DayZServer +login anonymous +app_update 223350 validate +quit
start "" "C:\DayZServer\DayZServer_x64.exe" -config=serverDZ.cfg -profiles=profiles -port=2302
```

### Linux

Crie um shell script e adicione ao cron (`0 */4 * * *`):

```bash
#!/bin/bash
kill $(pidof DayZServer) && sleep 15
cp -r /home/dayz/server/profiles/storage_1 /home/dayz/backups/$(date +%F_%H%M)_storage_1
/home/dayz/steamcmd/steamcmd.sh +force_install_dir /home/dayz/server +login anonymous +app_update 223350 validate +quit
cd /home/dayz/server && ./DayZServer -config=serverDZ.cfg -profiles=profiles -port=2302 &
```

Sempre faca backup de `storage_1/` antes de cada reinicializacao. Persistencia corrompida durante o desligamento pode apagar bases e veiculos de jogadores.

---

## cfgweather.xml

O arquivo **cfgweather.xml** na sua pasta de missao controla padroes de clima. Cada mapa vem com seus proprios padroes:

Cada fenomeno tem `min`, `max`, `duration_min` e `duration_max` (segundos):

| Fenomeno | Min Padrao | Max Padrao | Observacoes |
|------------|-------------|-------------|-------|
| `overcast` | 0.0 | 1.0 | Controla a densidade de nuvens e probabilidade de chuva |
| `rain` | 0.0 | 1.0 | So ativa acima de um limite de overcast. Defina max como `0.0` para sem chuva |
| `fog` | 0.0 | 0.3 | Valores acima de `0.5` produzem visibilidade quase zero |
| `wind_magnitude` | 0.0 | 18.0 | Afeta balistica e movimento do jogador |

---

## Sistema de Mensagens

O arquivo **db/messages.xml** na sua pasta de missao controla mensagens agendadas do servidor e avisos de desligamento:

```xml
<messages>
    <message deadline="0" shutdown="0"><text>Welcome to our server!</text></message>
    <message deadline="240" shutdown="1"><text>Server restart in 4 minutes!</text></message>
    <message deadline="60" shutdown="1"><text>Server restart in 1 minute!</text></message>
    <message deadline="0" shutdown="1"><text>Server is restarting now.</text></message>
</messages>
```

- `deadline` -- minutos antes da mensagem disparar (para mensagens de desligamento, minutos antes do servidor parar)
- `shutdown` -- `1` para mensagens de sequencia de desligamento, `0` para broadcasts regulares

O sistema de mensagens nao reinicializa o servidor. Ele apenas exibe avisos quando um agendamento de reinicializacao e configurado externamente.

---

[Inicio](../README.md) | [<< Anterior: Solucao de Problemas](11-troubleshooting.md) | [Inicio da Parte 9](01-server-setup.md)
