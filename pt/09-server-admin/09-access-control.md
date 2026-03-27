# Chapter 9.9: Controle de Acesso

[Inicio](../README.md) | [<< Anterior: Ajuste de Performance](08-performance.md) | [Proximo: Gerenciamento de Mods >>](10-mod-management.md)

---

> **Resumo:** Configure quem pode conectar ao seu servidor DayZ, como bans funcionam, como ativar administracao remota e como a verificacao de assinatura de mods impede conteudo nao autorizado. Este capitulo cobre todos os mecanismos de controle de acesso disponiveis para um operador de servidor.

---

## Sumario

- [Acesso de Admin via serverDZ.cfg](#acesso-de-admin-via-serverdzcfg)
- [ban.txt](#bantxt)
- [whitelist.txt](#whitelisttxt)
- [Anti-Cheat BattlEye](#anti-cheat-battleye)
- [RCON (Console Remoto)](#rcon-console-remoto)
- [Verificacao de Assinatura](#verificacao-de-assinatura)
- [O Diretorio keys/](#o-diretorio-keys)
- [Ferramentas de Admin In-Game](#ferramentas-de-admin-in-game)
- [Erros Comuns](#erros-comuns)

---

## Acesso de Admin via serverDZ.cfg

O parametro `passwordAdmin` no **serverDZ.cfg** define a senha de admin do seu servidor:

```cpp
passwordAdmin = "YourSecretPassword";
```

Voce usa essa senha de duas formas:

1. **In-game** -- abra o chat e digite `#login YourSecretPassword` para ganhar privilegios de admin naquela sessao.
2. **RCON** -- conecte com um cliente RCON do BattlEye usando essa senha (veja a secao RCON abaixo).

Mantenha a senha de admin longa e unica. Qualquer pessoa com ela tem controle total sobre o servidor em execucao.

---

## ban.txt

O arquivo **ban.txt** fica no diretorio de perfil do servidor (o caminho que voce definiu com `-profiles=`). Ele contem um SteamID64 por linha:

```
76561198012345678
76561198087654321
```

- Cada linha e um SteamID64 de 17 digitos -- sem nomes, sem comentarios, sem senhas.
- Jogadores cujo SteamID aparece neste arquivo sao recusados na conexao ao tentar entrar.
- Voce pode editar o arquivo enquanto o servidor esta rodando; alteracoes fazem efeito na proxima tentativa de conexao.

---

## whitelist.txt

O arquivo **whitelist.txt** fica no mesmo diretorio de perfil. Quando voce ativa a whitelist, apenas SteamIDs listados neste arquivo podem conectar:

```
76561198012345678
76561198087654321
```

O formato e identico ao **ban.txt** -- um SteamID64 por linha, nada mais.

A whitelist e util para comunidades privadas, servidores de teste ou eventos onde voce precisa de uma lista de jogadores controlada.

---

## Anti-Cheat BattlEye

BattlEye e o sistema anti-cheat integrado ao DayZ. Seus arquivos ficam na pasta `BattlEye/` dentro do diretorio do servidor:

| Arquivo | Proposito |
|------|---------|
| **BEServer_x64.dll** | O binario do engine anti-cheat BattlEye |
| **beserver_x64.cfg** | Arquivo de configuracao (porta RCON, senha RCON) |
| **bans.txt** | Bans especificos do BattlEye (baseados em GUID, nao SteamID) |

O BattlEye e ativado por padrao. Voce inicia o servidor com `DayZServer_x64.exe` e o BattlEye carrega automaticamente. Para desativa-lo explicitamente (nao recomendado para producao), use o parametro de lancamento `-noBE`.

O arquivo **bans.txt** na pasta `BattlEye/` usa GUIDs do BattlEye, que sao diferentes de SteamID64s. Bans emitidos atraves de RCON ou comandos do BattlEye escrevem neste arquivo automaticamente.

---

## RCON (Console Remoto)

O RCON do BattlEye permite administrar o servidor remotamente sem estar in-game. Configure no `BattlEye/beserver_x64.cfg`:

```
RConPassword yourpassword
RConPort 2306
```

A porta RCON padrao e a porta do jogo mais 4. Se seu servidor roda na porta `2302`, o RCON usa `2306` por padrao.

### Comandos RCON Disponiveis

| Comando | Efeito |
|---------|--------|
| `kick <jogador> [motivo]` | Kickar um jogador do servidor |
| `ban <jogador> [minutos] [motivo]` | Banir um jogador (escreve no bans.txt do BattlEye) |
| `say -1 <mensagem>` | Transmitir uma mensagem para todos os jogadores |
| `#shutdown` | Desligamento gracioso do servidor |
| `#lock` | Trancar o servidor (sem novas conexoes) |
| `#unlock` | Destrancar o servidor |
| `players` | Listar jogadores conectados |

Voce conecta ao RCON usando um cliente RCON do BattlEye (existem varias ferramentas gratuitas). A conexao requer o IP, porta RCON e a senha do **beserver_x64.cfg**.

---

## Verificacao de Assinatura

O parametro `verifySignatures` no **serverDZ.cfg** controla se o servidor verifica assinaturas de mods:

```cpp
verifySignatures = 2;
```

| Valor | Comportamento |
|-------|----------|
| `0` | Desativado -- qualquer pessoa pode entrar com quaisquer mods, sem verificacao de assinatura |
| `2` | Verificacao completa -- clientes devem ter assinaturas validas para todos os mods carregados (padrao) |

Sempre use `verifySignatures = 2` em servidores de producao. Definir como `0` permite que jogadores entrem com mods modificados ou nao assinados, o que e um risco serio de seguranca.

---

## O Diretorio keys/

O diretorio `keys/` na raiz do servidor contem arquivos **.bikey**. Cada `.bikey` corresponde a um mod e diz ao servidor "as assinaturas deste mod sao confiaveis."

Quando `verifySignatures = 2`:

1. O servidor verifica cada mod que o cliente conectando tem carregado.
2. Para cada mod, o servidor procura um `.bikey` correspondente em `keys/`.
3. Se a chave correspondente estiver faltando, o jogador e kickado.

Todo mod que voce instala no servidor vem com um arquivo `.bikey` (geralmente na subpasta `Keys/` ou `Key/` do mod). Voce copia esse arquivo para o diretorio `keys/` do servidor.

```
DayZServer/
├── keys/
│   ├── dayz.bikey              ← vanilla (sempre presente)
│   ├── MyMod.bikey             ← copiado de @MyMod/Keys/
│   └── AnotherMod.bikey        ← copiado de @AnotherMod/Keys/
```

Se voce adicionar um novo mod e esquecer de copiar o `.bikey`, todo jogador rodando aquele mod sera kickado ao conectar.

---

## Ferramentas de Admin In-Game

Uma vez que voce faca login com `#login <senha>` no chat, voce ganha acesso as ferramentas de admin:

- **Lista de jogadores** -- visualize todos os jogadores conectados com seus SteamIDs.
- **Kick/ban** -- remova ou bana jogadores diretamente da lista de jogadores.
- **Teleporte** -- use o mapa de admin para teleportar para qualquer posicao.
- **Log de admin** -- log do lado do servidor de acoes de jogadores (kills, conexoes, desconexoes) escrito em arquivos `*.ADM` no diretorio de perfil.
- **Camera livre** -- desconecte do seu personagem e voe pelo mapa.

Essas ferramentas sao integradas ao jogo vanilla. Mods de terceiros (como Community Online Tools) estendem as capacidades de admin significativamente.

---

## Erros Comuns

Estes sao os problemas que operadores de servidores encontram com mais frequencia:

| Erro | Sintoma | Solucao |
|---------|---------|-----|
| `.bikey` faltando em `keys/` | Jogadores sao kickados ao entrar com erro de assinatura | Copie o arquivo `.bikey` do mod para o diretorio `keys/` do servidor |
| Colocar nomes ou senhas no **ban.txt** | Bans nao funcionam; erros aleatorios | Use apenas valores SteamID64, um por linha |
| Conflito de porta RCON | Cliente RCON nao consegue conectar | Garanta que a porta RCON nao esta sendo usada por outro servico; verifique regras de firewall |
| `verifySignatures = 0` em producao | Qualquer pessoa pode entrar com mods adulterados | Defina como `2` em qualquer servidor publico |
| Esquecendo de abrir a porta RCON no firewall | Cliente RCON da timeout | Abra a porta UDP do RCON (padrao 2306) no seu firewall |
| Editando **bans.txt** em `BattlEye/` com SteamIDs | Bans nao funcionam | O **bans.txt** do BattlEye usa GUIDs, nao SteamIDs; use **ban.txt** no diretorio de perfil para bans por SteamID |

---

[Inicio](../README.md) | [<< Anterior: Ajuste de Performance](08-performance.md) | [Proximo: Gerenciamento de Mods >>](10-mod-management.md)
