# Chapter 9.10: Gerenciamento de Mods

[Inicio](../README.md) | [<< Anterior: Controle de Acesso](09-access-control.md) | [Proximo: Solucao de Problemas >>](11-troubleshooting.md)

---

> **Resumo:** Instale, configure e mantenha mods de terceiros em um servidor dedicado DayZ. Cobre parametros de lancamento, downloads da Workshop, chaves de assinatura, ordem de carregamento, mods somente servidor vs obrigatorios para cliente, atualizacoes e os erros mais comuns que causam crashes ou kicks de jogadores.

---

## Sumario

- [Como Mods Carregam](#como-mods-carregam)
- [Formato do Parametro de Lancamento](#formato-do-parametro-de-lancamento)
- [Instalacao de Mods da Workshop](#instalacao-de-mods-da-workshop)
- [Chaves de Mod (.bikey)](#chaves-de-mod-bikey)
- [Ordem de Carregamento e Dependencias](#ordem-de-carregamento-e-dependencias)
- [Mods Somente Servidor vs Obrigatorios para Cliente](#mods-somente-servidor-vs-obrigatorios-para-cliente)
- [Atualizando Mods](#atualizando-mods)
- [Solucionando Conflitos de Mods](#solucionando-conflitos-de-mods)
- [Erros Comuns](#erros-comuns)

---

## Como Mods Carregam

O DayZ carrega mods atraves do parametro de lancamento `-mod=`. Cada entrada e um caminho para uma pasta contendo arquivos PBO e um `config.cpp`. O engine le cada PBO em cada pasta de mod, registra suas classes e scripts, e continua para o proximo mod na lista.

Servidor e cliente devem ter os mesmos mods em `-mod=`. Se o servidor lista `@CF;@MyMod` e o cliente so tem `@CF`, a conexao falha com um erro de assinatura. Mods somente servidor colocados em `-servermod=` sao a excecao -- clientes nunca precisam deles.

---

## Formato do Parametro de Lancamento

Um comando de lancamento tipico de servidor moddado:

```batch
DayZServer_x64.exe -config=serverDZ.cfg -port=2302 -profiles=profiles -mod=@CF;@VPPAdminTools;@MyContentMod -servermod=@MyServerLogic -dologs -adminlog
```

| Parametro | Proposito |
|-----------|---------|
| `-mod=` | Mods obrigatorios tanto para servidor quanto para todos os clientes conectando |
| `-servermod=` | Mods somente servidor (clientes nao precisam deles) |

Regras:
- Caminhos sao **separados por ponto e virgula** sem espacos ao redor dos pontos e virgulas
- Cada caminho e relativo ao diretorio raiz do servidor (ex.: `@CF` significa `<raiz_do_servidor>/@CF/`)
- Voce pode usar caminhos absolutos: `-mod=D:\Mods\@CF;D:\Mods\@VPP`
- **A ordem importa** -- dependencias devem aparecer antes dos mods que precisam delas

---

## Instalacao de Mods da Workshop

### Passo 1: Baixar o Mod

Use o SteamCMD com o App ID do **cliente** DayZ (221100) e o Workshop ID do mod:

```batch
steamcmd.exe +force_install_dir "C:\DayZServer" +login your_username +workshop_download_item 221100 1559212036 +quit
```

Arquivos baixados ficam em:

```
C:\DayZServer\steamapps\workshop\content\221100\1559212036\
```

### Passo 2: Criar um Symlink ou Copiar

Pastas da Workshop usam IDs numericos, que sao inutilizaveis no `-mod=`. Crie um symlink nomeado (recomendado) ou copie a pasta:

```batch
mklink /J "C:\DayZServer\@CF" "C:\DayZServer\steamapps\workshop\content\221100\1559212036"
```

Usar uma juncao significa que atualizacoes via SteamCMD sao aplicadas automaticamente -- sem necessidade de re-copiar.

### Passo 3: Copiar o .bikey

Veja a proxima secao.

---

## Chaves de Mod (.bikey)

Todo mod assinado vem com uma pasta `keys/` contendo um ou mais arquivos `.bikey`. Esses arquivos dizem ao BattlEye quais assinaturas de PBO aceitar.

1. Abra a pasta do mod (ex.: `@CF/keys/`)
2. Copie todos os arquivos `.bikey` para o diretorio `keys/` na raiz do servidor

```
DayZServer/
  keys/
    dayz.bikey              # Vanilla -- sempre presente
    cf.bikey                # Copiado de @CF/keys/
    vpp_admintools.bikey    # Copiado de @VPPAdminTools/keys/
```

Sem a chave correta, qualquer jogador rodando aquele mod recebe: **"Player kicked: Modified data"**.

---

## Ordem de Carregamento e Dependencias

Mods carregam da esquerda para a direita no parametro `-mod=`. O `config.cpp` de um mod declara suas dependencias:

```cpp
class CfgPatches
{
    class MyMod
    {
        requiredAddons[] = { "CF" };
    };
};
```

Se `MyMod` requer `CF`, entao `@CF` deve aparecer **antes** de `@MyMod` no parametro de lancamento:

```
-mod=@CF;@MyMod          ✓ correto
-mod=@MyMod;@CF          ✗ crash ou classes faltando
```

**Padrao geral de ordem de carregamento:**

1. **Mods de framework** -- CF, Community-Online-Tools
2. **Mods de biblioteca** -- BuilderItems, qualquer pacote de assets compartilhado
3. **Mods de funcionalidade** -- adicoes de mapa, armas, veiculos
4. **Mods dependentes** -- qualquer coisa que lista os acima como `requiredAddons`

Na duvida, verifique a pagina da Workshop ou documentacao do mod. A maioria dos autores de mods publica a ordem de carregamento necessaria.

---

## Mods Somente Servidor vs Obrigatorios para Cliente

| Parametro | Quem precisa | Exemplos tipicos |
|-----------|-------------|------------------|
| `-mod=` | Servidor + todos os clientes | Armas, veiculos, mapas, mods de UI, roupas |
| `-servermod=` | Somente servidor | Gerenciadores de economia, ferramentas de logging, backends de admin, scripts de agendamento |

A regra e direta: se um mod contem **qualquer** script do lado do cliente, layouts, texturas ou modelos, ele deve ir no `-mod=`. Se ele so roda logica do lado do servidor sem assets que o cliente sequer toque, use `-servermod=`.

Colocar um mod somente servidor em `-mod=` forca todo jogador a baixa-lo. Colocar um mod obrigatorio para cliente em `-servermod=` causa texturas faltando, UI quebrada ou erros de script no cliente.

---

## Atualizando Mods

### Procedimento

1. **Pare o servidor** -- atualizar arquivos enquanto o servidor roda pode corromper PBOs
2. **Re-baixe** via SteamCMD:
   ```batch
   steamcmd.exe +force_install_dir "C:\DayZServer" +login your_username +workshop_download_item 221100 <modID> +quit
   ```
3. **Copie arquivos .bikey atualizados** -- autores de mods ocasionalmente rotacionam suas chaves de assinatura. Sempre copie o `.bikey` novo da pasta `keys/` do mod para o diretorio `keys/` do servidor
4. **Reinicie o servidor**

Se voce usou symlinks (juncoes), o passo 2 atualiza os arquivos do mod no local. Se voce copiou arquivos manualmente, voce deve copia-los novamente.

### Atualizacoes do Lado do Cliente

Jogadores inscritos no mod na Steam Workshop recebem atualizacoes automaticamente. Se voce atualizar um mod no servidor e um jogador tiver a versao antiga, eles recebem um erro de assinatura e nao podem conectar ate o cliente deles atualizar.

---

## Solucionando Conflitos de Mods

### Verificar o Log RPT

Abra o arquivo `.RPT` mais recente em `profiles/`. Procure por:

- **"Cannot register"** -- colisao de nome de classe entre dois mods
- **"Missing addons"** -- uma dependencia nao esta carregada (ordem de carregamento errada ou mod faltando)
- **"Signature verification failed"** -- incompatibilidade de `.bikey` ou chave faltando

### Verificar o Log de Script

Abra o `script_*.log` mais recente em `profiles/`. Procure por:

- **"SCRIPT (E)"** -- erros de script, frequentemente causados por ordem de carregamento ou incompatibilidade de versao
- **"Definition of variable ... already exists"** -- dois mods definem a mesma classe

### Isolar o Problema

Quando voce tem muitos mods e algo quebra, teste incrementalmente:

1. Comece apenas com mods de framework (`@CF`)
2. Adicione um mod por vez
3. Inicie e verifique logs apos cada adicao
4. O mod que causa erros e o culpado

### Dois Mods Editando a Mesma Classe

Se dois mods usam `modded class PlayerBase`, aquele carregado **por ultimo** (mais a direita em `-mod=`) vence. Sua chamada `super` encadeia para a versao do outro mod. Isso geralmente funciona, mas se um mod sobrescreve um metodo sem chamar `super`, as alteracoes do outro mod sao perdidas.

---

## Erros Comuns

**Ordem de carregamento errada.** O servidor crasha ou registra "Missing addons" porque uma dependencia nao foi carregada ainda. Solucao: mova o mod de dependencia para mais cedo na lista de `-mod=`.

**Esquecendo `-servermod=` para mods somente servidor.** Jogadores sao forcados a baixar um mod que nao precisam. Solucao: mova mods somente servidor de `-mod=` para `-servermod=`.

**Nao atualizar arquivos `.bikey` apos atualizacao de mod.** Jogadores sao kickados com "Modified data" porque a chave do servidor nao corresponde as novas assinaturas PBO do mod. Solucao: sempre re-copie arquivos `.bikey` ao atualizar mods.

**Reempacotando PBOs de mods.** Reempacotar os arquivos PBO de um mod quebra sua assinatura digital, causa kicks do BattlEye para todo jogador e viola os termos da maioria dos autores de mods. Nunca reempacote um mod que voce nao criou.

**Misturando caminhos da Workshop com caminhos locais.** Usar o caminho numerico bruto da Workshop para alguns mods e pastas nomeadas para outros causa confusao ao atualizar. Escolha uma abordagem -- symlinks sao a mais limpa.

**Espacos em caminhos de mods.** Um caminho como `-mod=@My Mod` quebra o parsing. Renomeie pastas de mods para evitar espacos, ou envolva o parametro inteiro em aspas: `-mod="@My Mod;@CF"`.

**Mod desatualizado no servidor, atualizado no cliente (ou vice-versa).** Incompatibilidade de versao impede conexao. Mantenha versoes do servidor e Workshop sincronizadas. Atualize todos os mods e o servidor ao mesmo tempo.

---

[Inicio](../README.md) | [<< Anterior: Controle de Acesso](09-access-control.md) | [Proximo: Solucao de Problemas >>](11-troubleshooting.md)
