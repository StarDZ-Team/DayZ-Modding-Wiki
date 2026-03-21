# Capitulo 5.2: inputs.xml --- Keybindings Personalizados

> **Resumo:** O arquivo `inputs.xml` permite que seu mod registre keybindings personalizados que aparecem no menu de Controles das configuracoes do jogador. Jogadores podem visualizar, reconfigurar e alternar esses inputs como acoes vanilla. Este e o mecanismo padrao para adicionar teclas de atalho a mods de DayZ.

---

## Sumario

- [Visao Geral](#visao-geral)
- [Localizacao do Arquivo](#localizacao-do-arquivo)
- [Estrutura XML Completa](#estrutura-xml-completa)
- [Bloco Actions](#bloco-actions)
- [Bloco Sorting](#bloco-sorting)
- [Bloco Preset (Keybindings Padrao)](#bloco-preset-keybindings-padrao)
- [Combos com Modificadores](#combos-com-modificadores)
- [Inputs Ocultos](#inputs-ocultos)
- [Multiplas Teclas Padrao](#multiplas-teclas-padrao)
- [Acessando Inputs no Script](#acessando-inputs-no-script)
- [Referencia de Metodos de Input](#referencia-de-metodos-de-input)
- [Suprimindo e Desabilitando Inputs](#suprimindo-e-desabilitando-inputs)
- [Referencia de Nomes de Teclas](#referencia-de-nomes-de-teclas)
- [Exemplos Reais](#exemplos-reais)
- [Erros Comuns](#erros-comuns)

---

## Visao Geral

Quando seu mod precisa que o jogador pressione uma tecla --- abrindo um menu, alternando uma funcionalidade, comandando uma unidade de IA --- voce registra uma acao de input personalizada no `inputs.xml`. O motor le este arquivo na inicializacao e integra suas acoes ao sistema universal de input. Jogadores veem seus keybindings no menu Settings > Controls do jogo, agrupados sob um cabecalho que voce define.

Inputs personalizados sao identificados por um nome de acao unico (convencionalmente prefixado com `UA` para "User Action") e podem ter keybindings padrao que os jogadores podem reconfigurar a vontade.

---

## Localizacao do Arquivo

Coloque `inputs.xml` dentro de uma subpasta `data` do seu diretorio Scripts:

```
@MyMod/
  Addons/
    MyMod_Scripts.pbo
      Scripts/
        data/
          inputs.xml        <-- Aqui
        3_Game/
        4_World/
        5_Mission/
```

Alguns mods o colocam diretamente na pasta `Scripts/`. Ambas as localizacoes funcionam. O motor descobre o arquivo automaticamente --- nenhum registro no config.cpp e necessario.

---

## Estrutura XML Completa

Um arquivo `inputs.xml` tem tres secoes, todas encapsuladas em um elemento raiz `<modded_inputs>`:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<modded_inputs>
    <inputs>
        <actions>
            <!-- Action definitions go here -->
        </actions>

        <sorting name="mymod" loc="STR_MYMOD_INPUT_GROUP">
            <!-- Sort order for the settings menu -->
        </sorting>
    </inputs>
    <preset>
        <!-- Default keybinding assignments go here -->
    </preset>
</modded_inputs>
```

Todas as tres secoes --- `<actions>`, `<sorting>` e `<preset>` --- trabalham juntas, mas servem a propositos diferentes.

---

## Bloco Actions

O bloco `<actions>` declara toda acao de input que seu mod fornece. Cada acao e um unico elemento `<input>`.

### Sintaxe

```xml
<actions>
    <input name="UAMyModOpenMenu" loc="STR_MYMOD_INPUT_OPEN_MENU" />
    <input name="UAMyModToggleHUD" loc="STR_MYMOD_INPUT_TOGGLE_HUD" />
</actions>
```

### Atributos

| Atributo | Obrigatorio | Descricao |
|----------|-------------|-----------|
| `name` | Sim | Identificador unico da acao. Convencao: prefixar com `UA` (User Action). Usado em scripts para consultar este input. |
| `loc` | Nao | Chave de stringtable para o nome de exibicao no menu de Controles. **Sem prefixo `#`** --- o sistema o adiciona. |
| `visible` | Nao | Defina como `"false"` para ocultar do menu de Controles. Padrao e `true`. |

### Convencao de Nomenclatura

Nomes de acao devem ser globalmente unicos entre todos os mods carregados. Use o prefixo do seu mod:

```xml
<input name="UAMyModAdminPanel" loc="STR_MYMOD_INPUT_ADMIN_PANEL" />
<input name="UAExpansionBookToggle" loc="STR_EXPANSION_BOOK_TOGGLE" />
<input name="eAICommandMenu" loc="STR_EXPANSION_AI_COMMAND_MENU" />
```

O prefixo `UA` e convencional mas nao obrigatorio. O Expansion AI usa `eAI` como prefixo, o que tambem funciona.

---

## Bloco Sorting

O bloco `<sorting>` controla como seus inputs aparecem nas configuracoes de Controles do jogador. Ele define um grupo nomeado (que se torna um cabecalho de secao) e lista os inputs na ordem de exibicao.

### Sintaxe

```xml
<sorting name="mymod" loc="STR_MYMOD_INPUT_GROUP">
    <input name="UAMyModOpenMenu" />
    <input name="UAMyModToggleHUD" />
    <input name="UAMyModSpecialAction" />
</sorting>
```

### Atributos

| Atributo | Obrigatorio | Descricao |
|----------|-------------|-----------|
| `name` | Sim | Identificador interno para este grupo de ordenacao |
| `loc` | Sim | Chave de stringtable para o cabecalho do grupo exibido em Settings > Controls |

### Como Aparece

Nas configuracoes de Controles, o jogador ve:

```
[MyMod]                          <-- do loc do sorting
  Open Menu .............. [Y]   <-- do loc do input + preset
  Toggle HUD ............. [H]   <-- do loc do input + preset
```

Apenas inputs listados no bloco `<sorting>` aparecem no menu de configuracoes. Inputs definidos em `<actions>` mas nao listados em `<sorting>` sao silenciosamente registrados mas invisiveis para o jogador (mesmo se `visible` nao estiver explicitamente definido como `false`).

---

## Bloco Preset (Keybindings Padrao)

O bloco `<preset>` atribui teclas padrao as suas acoes. Estas sao as teclas com as quais o jogador comeca antes de qualquer personalizacao.

### Binding Simples de Tecla

```xml
<preset>
    <input name="UAMyModOpenMenu">
        <btn name="kY"/>
    </input>
</preset>
```

Isso vincula a tecla `Y` como padrao para `UAMyModOpenMenu`.

### Sem Tecla Padrao

Se voce omitir uma acao do bloco `<preset>`, ela nao tem binding padrao. O jogador deve atribuir manualmente uma tecla em Settings > Controls. Isso e apropriado para bindings opcionais ou avancados.

---

## Combos com Modificadores

Para exigir uma tecla modificadora (Ctrl, Shift, Alt), aninhe elementos `<btn>`:

### Ctrl + Botao Esquerdo do Mouse

```xml
<input name="eAISetWaypoint">
    <btn name="kLControl">
        <btn name="mBLeft"/>
    </btn>
</input>
```

O `<btn>` externo e o modificador; o `<btn>` interno e a tecla principal. O jogador deve segurar o modificador e entao pressionar a tecla principal.

### Shift + Tecla

```xml
<input name="UAMyModQuickAction">
    <btn name="kLShift">
        <btn name="kQ"/>
    </btn>
</input>
```

### Regras de Aninhamento

- O `<btn>` **externo** e sempre o modificador (mantido pressionado)
- O `<btn>` **interno** e o gatilho (pressionado enquanto o modificador e mantido)
- Apenas um nivel de aninhamento e tipico; aninhamento mais profundo nao e testado e nao e recomendado

---

## Inputs Ocultos

Use `visible="false"` para registrar um input que o jogador nao pode ver ou reconfigurar no menu de Controles. Isso e util para inputs internos usados pelo codigo do seu mod que nao devem ser configuraveis pelo jogador.

```xml
<actions>
    <input name="eAITestInput" visible="false" />
    <input name="UAExpansionConfirm" loc="" visible="false" />
</actions>
```

Inputs ocultos ainda podem ter atribuicoes de tecla padrao no bloco `<preset>`:

```xml
<preset>
    <input name="eAITestInput">
        <btn name="kY"/>
    </input>
</preset>
```

---

## Multiplas Teclas Padrao

Uma acao pode ter multiplas teclas padrao. Liste multiplos elementos `<btn>` como irmaos:

```xml
<input name="UAExpansionConfirm">
    <btn name="kReturn" />
    <btn name="kNumpadEnter" />
</input>
```

Tanto `Enter` quanto `Numpad Enter` acionarao `UAExpansionConfirm`. Isso e util para acoes onde multiplas teclas fisicas devem mapear para a mesma acao logica.

---

## Acessando Inputs no Script

### Obtendo a API de Input

Todo acesso a input passa por `GetUApi()`, que retorna a API global de User Action:

```c
UAInput input = GetUApi().GetInputByName("UAMyModOpenMenu");
```

### Consultando no OnUpdate

Inputs personalizados sao tipicamente consultados em `MissionGameplay.OnUpdate()` ou callbacks similares por frame:

```c
modded class MissionGameplay
{
    override void OnUpdate(float timeslice)
    {
        super.OnUpdate(timeslice);

        UAInput input = GetUApi().GetInputByName("UAMyModOpenMenu");

        if (input.LocalPress())
        {
            // Key was just pressed this frame
            OpenMyModMenu();
        }
    }
}
```

### Alternativa: Usando o Nome do Input Diretamente

Muitos mods verificam inputs inline usando os metodos `UAInputAPI` com nomes string:

```c
override void OnUpdate(float timeslice)
{
    super.OnUpdate(timeslice);

    Input input = GetGame().GetInput();

    if (input.LocalPress("UAMyModOpenMenu", false))
    {
        OpenMyModMenu();
    }
}
```

O parametro `false` em `LocalPress("name", false)` indica que a verificacao nao deve consumir o evento de input.

---

## Referencia de Metodos de Input

Uma vez que voce tem uma referencia `UAInput` (de `GetUApi().GetInputByName()`), ou esta usando a classe `Input` diretamente, estes metodos detectam diferentes estados de input:

| Metodo | Retorna | Quando e Verdadeiro |
|--------|---------|---------------------|
| `LocalPress()` | `bool` | A tecla foi pressionada **neste frame** (gatilho unico no key-down) |
| `LocalRelease()` | `bool` | A tecla foi solta **neste frame** (gatilho unico no key-up) |
| `LocalClick()` | `bool` | A tecla foi pressionada e solta rapidamente (toque) |
| `LocalHold()` | `bool` | A tecla foi mantida pressionada por um tempo limite |
| `LocalDoubleClick()` | `bool` | A tecla foi tocada duas vezes rapidamente |
| `LocalValue()` | `float` | Valor analogico atual (0.0 ou 1.0 para teclas digitais; variavel para eixos analogicos) |

### Padroes de Uso

**Alternar ao pressionar:**
```c
if (input.LocalPress("UAMyModToggle", false))
{
    m_IsEnabled = !m_IsEnabled;
}
```

**Segurar para ativar, soltar para desativar:**
```c
if (input.LocalPress("eAICommandMenu", false))
{
    ShowCommandWheel();
}

if (input.LocalRelease("eAICommandMenu", false) || input.LocalValue("eAICommandMenu", false) == 0)
{
    HideCommandWheel();
}
```

**Acao de duplo toque:**
```c
if (input.LocalDoubleClick("UAMyModSpecial", false))
{
    PerformSpecialAction();
}
```

**Segurar para acao estendida:**
```c
if (input.LocalHold("UAExpansionGPSToggle"))
{
    ToggleGPSMode();
}
```

---

## Suprimindo e Desabilitando Inputs

### ForceDisable

Desabilita temporariamente um input especifico. Comumente usado ao abrir menus para prevenir que acoes do jogo disparem enquanto uma UI esta ativa:

```c
// Disable the input while menu is open
GetUApi().GetInputByName("UAMyModToggle").ForceDisable(true);

// Re-enable when menu closes
GetUApi().GetInputByName("UAMyModToggle").ForceDisable(false);
```

### SupressNextFrame

Suprime todo processamento de input para o proximo frame. Usado durante transicoes de contexto de input (ex.: fechando menus) para prevenir sangramento de input de um frame:

```c
GetUApi().SupressNextFrame(true);
```

### UpdateControls

Apos modificar estados de input, chame `UpdateControls()` para aplicar mudancas imediatamente:

```c
GetUApi().GetInputByName("UAExpansionBookToggle").ForceDisable(false);
GetUApi().UpdateControls();
```

### Exclusoes de Input

O sistema de missao vanilla fornece grupos de exclusao. Quando um menu esta ativo, voce pode excluir categorias de inputs:

```c
// Suppress gameplay inputs while inventory is open
AddActiveInputExcludes({"inventory"});

// Restore when closing
RemoveActiveInputExcludes({"inventory"});
```

---

## Referencia de Nomes de Teclas

Nomes de tecla usados no atributo `<btn name="">` seguem uma convencao de nomenclatura especifica. Aqui esta a referencia completa.

### Teclas do Teclado

| Categoria | Nomes de Tecla |
|-----------|----------------|
| Letras | `kA`, `kB`, `kC`, `kD`, `kE`, `kF`, `kG`, `kH`, `kI`, `kJ`, `kK`, `kL`, `kM`, `kN`, `kO`, `kP`, `kQ`, `kR`, `kS`, `kT`, `kU`, `kV`, `kW`, `kX`, `kY`, `kZ` |
| Numeros (linha superior) | `k0`, `k1`, `k2`, `k3`, `k4`, `k5`, `k6`, `k7`, `k8`, `k9` |
| Teclas de funcao | `kF1`, `kF2`, `kF3`, `kF4`, `kF5`, `kF6`, `kF7`, `kF8`, `kF9`, `kF10`, `kF11`, `kF12` |
| Modificadores | `kLControl`, `kRControl`, `kLShift`, `kRShift`, `kLAlt`, `kRAlt` |
| Navegacao | `kUp`, `kDown`, `kLeft`, `kRight`, `kHome`, `kEnd`, `kPageUp`, `kPageDown` |
| Edicao | `kReturn`, `kBackspace`, `kDelete`, `kInsert`, `kSpace`, `kTab`, `kEscape` |
| Numpad | `kNumpad0` ... `kNumpad9`, `kNumpadEnter`, `kNumpadPlus`, `kNumpadMinus`, `kNumpadMultiply`, `kNumpadDivide`, `kNumpadDecimal` |
| Pontuacao | `kMinus`, `kEquals`, `kLBracket`, `kRBracket`, `kBackslash`, `kSemicolon`, `kApostrophe`, `kComma`, `kPeriod`, `kSlash`, `kGrave` |
| Bloqueios | `kCapsLock`, `kNumLock`, `kScrollLock` |

### Botoes do Mouse

| Nome | Botao |
|------|-------|
| `mBLeft` | Botao esquerdo do mouse |
| `mBRight` | Botao direito do mouse |
| `mBMiddle` | Botao do meio do mouse (clique na roda de scroll) |
| `mBExtra1` | Botao 4 do mouse (botao lateral traseiro) |
| `mBExtra2` | Botao 5 do mouse (botao lateral dianteiro) |

### Eixos do Mouse

| Nome | Eixo |
|------|------|
| `mAxisX` | Movimento horizontal do mouse |
| `mAxisY` | Movimento vertical do mouse |
| `mWheelUp` | Roda de scroll para cima |
| `mWheelDown` | Roda de scroll para baixo |

### Padrao de Nomenclatura

- **Teclado**: prefixo `k` + nome da tecla (ex.: `kT`, `kF5`, `kLControl`)
- **Botoes do mouse**: prefixo `mB` + nome do botao (ex.: `mBLeft`, `mBRight`)
- **Eixos do mouse**: prefixo `m` + nome do eixo (ex.: `mAxisX`, `mWheelUp`)

---

## Exemplos Reais

### DayZ Expansion AI

Um inputs.xml bem estruturado com keybindings visiveis, inputs de debug ocultos e combos com modificadores:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<modded_inputs>
    <inputs>
        <actions>
            <input name="eAICommandMenu" loc="STR_EXPANSION_AI_COMMAND_MENU"/>
            <input name="eAISetWaypoint" loc="STR_EXPANSION_AI_SET_WAYPOINT"/>
            <input name="eAITestInput" visible="false" />
            <input name="eAITestLRIncrease" visible="false" />
            <input name="eAITestLRDecrease" visible="false" />
            <input name="eAITestUDIncrease" visible="false" />
            <input name="eAITestUDDecrease" visible="false" />
        </actions>

        <sorting name="expansion" loc="STR_EXPANSION_LABEL">
            <input name="eAICommandMenu" />
            <input name="eAISetWaypoint" />
            <input name="eAITestInput" />
            <input name="eAITestLRIncrease" />
            <input name="eAITestLRDecrease" />
            <input name="eAITestUDIncrease" />
            <input name="eAITestUDDecrease" />
        </sorting>
    </inputs>
    <preset>
        <input name="eAICommandMenu">
            <btn name="kT"/>
        </input>
        <input name="eAISetWaypoint">
            <btn name="kLControl">
                <btn name="mBLeft"/>
            </btn>
        </input>
        <input name="eAITestInput">
            <btn name="kY"/>
        </input>
        <input name="eAITestLRIncrease">
            <btn name="kRight"/>
        </input>
        <input name="eAITestLRDecrease">
            <btn name="kLeft"/>
        </input>
        <input name="eAITestUDIncrease">
            <btn name="kUp"/>
        </input>
        <input name="eAITestUDDecrease">
            <btn name="kDown"/>
        </input>
    </preset>
</modded_inputs>
```

Observacoes principais:
- `eAICommandMenu` vinculado a `T` --- visivel nas configuracoes, jogador pode reconfigurar
- `eAISetWaypoint` usa um combo modificador **Ctrl + Clique Esquerdo**
- Inputs de teste sao `visible="false"` --- ocultos dos jogadores mas acessiveis no codigo

### DayZ Expansion Market

Um inputs.xml minimo para um input utilitario oculto com multiplas teclas padrao:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<modded_inputs>
    <inputs>
        <actions>
            <input name="UAExpansionConfirm" loc="" visible="false" />
        </actions>
    </inputs>
    <preset>
        <input name="UAExpansionConfirm">
            <btn name="kReturn" />
            <btn name="kNumpadEnter" />
        </input>
    </preset>
</modded_inputs>
```

Observacoes principais:
- Input oculto (`visible="false"`) com `loc` vazio --- nunca mostrado nas configuracoes
- Duas teclas padrao: tanto Enter quanto Numpad Enter acionam a mesma acao
- Sem bloco `<sorting>` --- nao necessario ja que o input e oculto

### Template Inicial Completo

Um template minimo mas completo para um novo mod:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<modded_inputs>
    <inputs>
        <actions>
            <input name="UAMyModOpenMenu" loc="STR_MYMOD_INPUT_OPEN_MENU" />
            <input name="UAMyModQuickAction" loc="STR_MYMOD_INPUT_QUICK_ACTION" />
        </actions>

        <sorting name="mymod" loc="STR_MYMOD_INPUT_GROUP">
            <input name="UAMyModOpenMenu" />
            <input name="UAMyModQuickAction" />
        </sorting>
    </inputs>
    <preset>
        <input name="UAMyModOpenMenu">
            <btn name="kF6"/>
        </input>
        <!-- UAMyModQuickAction has no default key; player must bind it -->
    </preset>
</modded_inputs>
```

Com uma stringtable.csv correspondente:

```csv
"Language","original","english"
"STR_MYMOD_INPUT_GROUP","My Mod","My Mod"
"STR_MYMOD_INPUT_OPEN_MENU","Open Menu","Open Menu"
"STR_MYMOD_INPUT_QUICK_ACTION","Quick Action","Quick Action"
```

---

## Erros Comuns

### Usando `#` no Atributo loc

```xml
<!-- WRONG -->
<input name="UAMyAction" loc="#STR_MYMOD_ACTION" />

<!-- CORRECT -->
<input name="UAMyAction" loc="STR_MYMOD_ACTION" />
```

O sistema de input prepende `#` internamente. Adicioná-lo voce mesmo causa um duplo prefixo e a busca falha.

### Colisao de Nomes de Acao

Se dois mods definem `UAOpenMenu`, apenas um funcionara. Sempre use o prefixo do seu mod:

```xml
<input name="UAMyModOpenMenu" />     <!-- Bom -->
<input name="UAOpenMenu" />          <!-- Arriscado -->
```

### Entrada de Sorting Ausente

Se voce define uma acao em `<actions>` mas esquece de lista-la em `<sorting>`, a acao funciona no codigo mas fica invisivel no menu de Controles. O jogador nao tem como reconfigura-la.

### Esquecendo de Definir em Actions

Se voce lista um input em `<sorting>` ou `<preset>` mas nunca o define em `<actions>`, o motor silenciosamente o ignora.

### Vinculando Teclas Conflitantes

Escolher teclas que conflitam com bindings vanilla (como `W`, `A`, `S`, `D`, `Tab`, `I`) faz tanto sua acao quanto a acao vanilla dispararem simultaneamente. Use teclas menos comuns (F5-F12, teclas do numpad) ou combos com modificadores por seguranca.
