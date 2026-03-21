# Capitulo 5.4: Formato ImageSet

> **Resumo:** ImageSets definem regioes de sprites nomeadas dentro de um atlas de textura. Sao o mecanismo principal do DayZ para referenciar icones, graficos de UI e sprite sheets a partir de arquivos de layout e scripts. Em vez de carregar centenas de arquivos de imagem individuais, voce empacota todos os icones em uma unica textura e descreve a posicao e tamanho de cada icone em um arquivo de definicao de imageset.

---

## Sumario

- [Visao Geral](#visao-geral)
- [Como ImageSets Funcionam](#como-imagesets-funcionam)
- [Formato ImageSet Nativo do DayZ](#formato-imageset-nativo-do-dayz)
- [Formato ImageSet XML](#formato-imageset-xml)
- [Registrando ImageSets no config.cpp](#registrando-imagesets-no-configcpp)
- [Referenciando Imagens em Layouts](#referenciando-imagens-em-layouts)
- [Referenciando Imagens em Scripts](#referenciando-imagens-em-scripts)
- [Flags de Imagem](#flags-de-imagem)
- [Texturas Multi-Resolucao](#texturas-multi-resolucao)
- [Criando Conjuntos de Icones Personalizados](#criando-conjuntos-de-icones-personalizados)
- [Padrao de Integracao Font Awesome](#padrao-de-integracao-font-awesome)
- [Exemplos Reais](#exemplos-reais)
- [Erros Comuns](#erros-comuns)

---

## Visao Geral

Um atlas de textura e uma unica imagem grande (tipicamente no formato `.edds`) contendo muitos icones menores organizados em uma grade ou layout livre. Um arquivo de imageset mapeia nomes legiveis por humanos para regioes retangulares dentro daquele atlas.

Por exemplo, uma textura 1024x1024 pode conter 64 icones de 64x64 pixels cada. O arquivo de imageset diz "o icone chamado `arrow_down` esta na posicao (128, 64) e tem 64x64 pixels." Seus arquivos de layout e scripts referenciam `arrow_down` pelo nome, e o motor extrai o sub-retangulo correto do atlas no momento da renderizacao.

Esta abordagem e eficiente: um unico carregamento de textura na GPU serve a todos os icones, reduzindo draw calls e overhead de memoria.

---

## Como ImageSets Funcionam

O fluxo de dados:

1. **Atlas de textura** (arquivo `.edds`) --- uma unica imagem contendo todos os icones
2. **Definicao de ImageSet** (arquivo `.imageset`) --- mapeia nomes para regioes no atlas
3. **Registro no config.cpp** --- diz ao motor para carregar o imageset na inicializacao
4. **Referencia em layout/script** --- usa a sintaxe `set:name image:iconName` para renderizar um icone especifico

Uma vez registrado, qualquer widget em qualquer arquivo de layout pode referenciar qualquer imagem do conjunto pelo nome.

---

## Formato ImageSet Nativo do DayZ

O formato nativo usa a sintaxe baseada em classes do motor Enfusion (similar ao config.cpp). Este e o formato usado pelo jogo vanilla e pela maioria dos mods estabelecidos.

### Estrutura

```
ImageSetClass {
 Name "my_icons"
 RefSize 1024 1024
 Textures {
  ImageSetTextureClass {
   mpix 1
   path "MyMod/GUI/imagesets/my_icons.edds"
  }
 }
 Images {
  ImageSetDefClass icon_name {
   Name "icon_name"
   Pos 0 0
   Size 64 64
   Flags 0
  }
 }
}
```

### Campos de Nivel Superior

| Campo | Descricao |
|-------|-----------|
| `Name` | O nome do conjunto. Usado na parte `set:` das referencias de imagem. Deve ser unico entre todos os mods carregados. |
| `RefSize` | Dimensoes de referencia da textura (largura altura). Usado para mapeamento de coordenadas. |
| `Textures` | Contem uma ou mais entradas `ImageSetTextureClass` para diferentes niveis de resolucao mip. |

### Campos de Entrada de Textura

| Campo | Descricao |
|-------|-----------|
| `mpix` | Nivel minimo de pixel (nivel mip). `0` = resolucao mais baixa, `1` = resolucao padrao. |
| `path` | Caminho para o arquivo de textura `.edds`, relativo a raiz do mod. Pode usar formato GUID do Enfusion (`{GUID}path`) ou caminhos relativos simples. |

### Campos de Entrada de Imagem

Cada imagem e um `ImageSetDefClass` dentro do bloco `Images`:

| Campo | Descricao |
|-------|-----------|
| Nome da classe | Deve corresponder ao campo `Name` (usado para buscas do motor) |
| `Name` | O identificador da imagem. Usado na parte `image:` das referencias. |
| `Pos` | Posicao do canto superior esquerdo no atlas (x y), em pixels |
| `Size` | Dimensoes (largura altura), em pixels |
| `Flags` | Flags de comportamento de repeticao (veja [Flags de Imagem](#flags-de-imagem)) |

### Exemplo Completo (DayZ Vanilla)

```
ImageSetClass {
 Name "dayz_gui"
 RefSize 1024 1024
 Textures {
  ImageSetTextureClass {
   mpix 0
   path "{534691EE0479871C}Gui/imagesets/dayz_gui.edds"
  }
  ImageSetTextureClass {
   mpix 1
   path "{C139E49FD0ECAF9E}Gui/imagesets/dayz_gui@2x.edds"
  }
 }
 Images {
  ImageSetDefClass Gradient {
   Name "Gradient"
   Pos 0 317
   Size 75 5
   Flags ISVerticalTile
  }
  ImageSetDefClass Expand {
   Name "Expand"
   Pos 121 257
   Size 20 20
   Flags 0
  }
 }
}
```

---

## Formato ImageSet XML

Um formato alternativo baseado em XML existe e e usado por alguns mods. E mais simples, mas oferece menos recursos (sem suporte multi-resolucao).

### Estrutura

```xml
<?xml version="1.0" encoding="utf-8"?>
<imageset name="mh_icons" file="MyMod/GUI/imagesets/mh_icons.edds">
  <image name="icon_store" pos="0 0" size="64 64" />
  <image name="icon_cart" pos="64 0" size="64 64" />
  <image name="icon_wallet" pos="128 0" size="64 64" />
</imageset>
```

### Atributos XML

**Elemento `<imageset>`:**

| Atributo | Descricao |
|----------|-----------|
| `name` | O nome do conjunto (equivalente ao `Name` nativo) |
| `file` | Caminho para o arquivo de textura (equivalente ao `path` nativo) |

**Elemento `<image>`:**

| Atributo | Descricao |
|----------|-----------|
| `name` | Identificador da imagem |
| `pos` | Posicao superior esquerda como `"x y"` |
| `size` | Dimensoes como `"largura altura"` |

### Quando Usar Qual Formato

| Recurso | Formato Nativo | Formato XML |
|---------|----------------|-------------|
| Multi-resolucao (niveis mip) | Sim | Nao |
| Flags de repeticao | Sim | Nao |
| Caminhos GUID do Enfusion | Sim | Sim |
| Simplicidade | Menor | Maior |
| Usado pelo DayZ vanilla | Sim | Nao |
| Usado pelo Expansion, MyMod, VPP | Sim | Ocasionalmente |

**Recomendacao:** Use o formato nativo para mods de producao. Use o formato XML para prototipagem rapida ou conjuntos de icones simples que nao precisam de repeticao ou suporte multi-resolucao.

---

## Registrando ImageSets no config.cpp

Arquivos de ImageSet devem ser registrados no `config.cpp` do seu mod sob o bloco `CfgMods` > `class defs` > `class imageSets`. Sem este registro, o motor nunca carrega o imageset e suas referencias de imagem falham silenciosamente.

### Sintaxe

```cpp
class CfgMods
{
    class MyMod
    {
        // ... other fields ...
        class defs
        {
            class imageSets
            {
                files[] =
                {
                    "MyMod/GUI/imagesets/my_icons.imageset",
                    "MyMod/GUI/imagesets/my_other_icons.imageset"
                };
            };
        };
    };
};
```

### Exemplo Real: MyFramework

MyFramework registra sete imagesets incluindo conjuntos de icones Font Awesome:

```cpp
class defs
{
    class imageSets
    {
        files[] =
        {
            "MyFramework/GUI/imagesets/prefabs.imageset",
            "MyFramework/GUI/imagesets/CUI.imageset",
            "MyFramework/GUI/icons/thin.imageset",
            "MyFramework/GUI/icons/light.imageset",
            "MyFramework/GUI/icons/regular.imageset",
            "MyFramework/GUI/icons/solid.imageset",
            "MyFramework/GUI/icons/brands.imageset"
        };
    };
};
```

### Exemplo Real: VPP Admin Tools

```cpp
class defs
{
    class imageSets
    {
        files[] =
        {
            "VPPAdminTools/GUI/Textures/dayz_gui_vpp.imageset"
        };
    };
};
```

### Exemplo Real: DayZ Editor

```cpp
class defs
{
    class imageSets
    {
        files[] =
        {
            "DayZEditor/gui/imagesets/dayz_editor_gui.imageset"
        };
    };
};
```

---

## Referenciando Imagens em Layouts

Em arquivos `.layout`, use a propriedade `image0` com a sintaxe `set:name image:imageName`:

```
ImageWidgetClass MyIcon {
 size 32 32
 hexactsize 1
 vexactsize 1
 image0 "set:dayz_gui image:icon_refresh"
}
```

### Detalhamento da Sintaxe

```
set:SETNAME image:IMAGENAME
```

- `SETNAME` --- o campo `Name` da definicao do imageset (ex.: `dayz_gui`, `solid`, `brands`)
- `IMAGENAME` --- o campo `Name` de uma entrada especifica `ImageSetDefClass` (ex.: `icon_refresh`, `arrow_down`)

### Multiplos Estados de Imagem

Alguns widgets suportam multiplos estados de imagem (normal, hover, pressionado):

```
ImageWidgetClass icon {
 image0 "set:solid image:circle"
}

ButtonWidgetClass btn {
 image0 "set:dayz_gui image:icon_expand"
}
```

### Exemplos de Mods Reais

```
image0 "set:regular image:arrow_down_short_wide"     -- MyMod: Font Awesome regular icon
image0 "set:dayz_gui image:icon_minus"                -- MyMod: vanilla DayZ icon
image0 "set:dayz_gui image:icon_collapse"             -- MyMod: vanilla DayZ icon
image0 "set:dayz_gui image:circle"                    -- MyMod: vanilla DayZ shape
image0 "set:dayz_editor_gui image:eye_open"           -- DayZ Editor: custom icon
```

---

## Referenciando Imagens em Scripts

No Enforce Script, use `ImageWidget.LoadImageFile()` ou defina propriedades de imagem nos widgets:

### LoadImageFile

```c
ImageWidget icon = ImageWidget.Cast(layoutRoot.FindAnyWidget("MyIcon"));
icon.LoadImageFile(0, "set:solid image:circle");
```

O parametro `0` e o indice da imagem (correspondente a `image0` nos layouts).

### Multiplos Estados via Indice

```c
ImageWidget collapseIcon;
collapseIcon.LoadImageFile(0, "set:regular image:square_plus");    // Normal state
collapseIcon.LoadImageFile(1, "set:solid image:square_minus");     // Toggled state
```

Alterne entre estados usando `SetImage(index)`:

```c
collapseIcon.SetImage(isExpanded ? 1 : 0);
```

### Usando Variaveis String

```c
// From DayZ Editor
string icon = "set:dayz_editor_gui image:search";
searchBarIcon.LoadImageFile(0, icon);

// Later, change dynamically
searchBarIcon.LoadImageFile(0, "set:dayz_gui image:icon_x");
```

---

## Flags de Imagem

O campo `Flags` em entradas de imageset no formato nativo controla o comportamento de repeticao quando a imagem e esticada alem do seu tamanho natural.

| Flag | Valor | Descricao |
|------|-------|-----------|
| `0` | 0 | Sem repeticao. A imagem estica para preencher o widget. |
| `ISHorizontalTile` | 1 | Repete horizontalmente quando o widget e mais largo que a imagem. |
| `ISVerticalTile` | 2 | Repete verticalmente quando o widget e mais alto que a imagem. |
| Ambos | 3 | Repete em ambas as direcoes (`ISHorizontalTile` + `ISVerticalTile`). |

### Uso

```
ImageSetDefClass Gradient {
 Name "Gradient"
 Pos 0 317
 Size 75 5
 Flags ISVerticalTile
}
```

Esta imagem `Gradient` tem 75x5 pixels. Quando usada em um widget mais alto que 5 pixels, ela repete verticalmente para preencher a altura, criando uma faixa de gradiente repetida.

A maioria dos icones usa `Flags 0` (sem repeticao). Flags de repeticao sao usadas principalmente para elementos de UI como bordas, divisores e padroes repetitivos.

---

## Texturas Multi-Resolucao

O formato nativo suporta multiplas texturas de resolucao para o mesmo imageset. Isso permite que o motor use arte de maior resolucao em displays de alta DPI.

```
Textures {
 ImageSetTextureClass {
  mpix 0
  path "Gui/imagesets/dayz_gui.edds"
 }
 ImageSetTextureClass {
  mpix 1
  path "Gui/imagesets/dayz_gui@2x.edds"
 }
}
```

- `mpix 0` --- baixa resolucao (usada em configuracoes de baixa qualidade ou elementos de UI distantes)
- `mpix 1` --- resolucao padrao/alta (padrao)

A convencao de nomenclatura `@2x` e emprestada do sistema Retina display da Apple, mas nao e obrigatoria --- voce pode nomear o arquivo como quiser.

### Na Pratica

A maioria dos mods inclui apenas `mpix 1` (uma unica resolucao). Suporte multi-resolucao e usado principalmente pelo jogo vanilla:

```
Textures {
 ImageSetTextureClass {
  mpix 1
  path "MyFramework/GUI/icons/solid.edds"
 }
}
```

---

## Criando Conjuntos de Icones Personalizados

### Fluxo de Trabalho Passo a Passo

**1. Crie o Atlas de Textura**

Use um editor de imagem (Photoshop, GIMP, etc.) para organizar seus icones em uma unica tela:
- Escolha um tamanho em potencia de dois (256x256, 512x512, 1024x1024, etc.)
- Organize icones em uma grade para facilitar o calculo de coordenadas
- Deixe algum padding entre icones para evitar sangramento de textura
- Salve como `.tga` ou `.png`

**2. Converta para EDDS**

O DayZ usa o formato `.edds` (Enfusion DDS) para texturas. Use o DayZ Workbench ou as ferramentas do Mikero para converter:
- Importe seu `.tga` no DayZ Workbench
- Ou use `Pal2PacE.exe` para converter `.paa` para `.edds`
- A saida deve ser um arquivo `.edds`

**3. Escreva a Definicao do ImageSet**

Mapeie cada icone para uma regiao nomeada. Se seus icones estao em uma grade de 64 pixels:

```
ImageSetClass {
 Name "mymod_icons"
 RefSize 512 512
 Textures {
  ImageSetTextureClass {
   mpix 1
   path "MyMod/GUI/imagesets/mymod_icons.edds"
  }
 }
 Images {
  ImageSetDefClass settings {
   Name "settings"
   Pos 0 0
   Size 64 64
   Flags 0
  }
  ImageSetDefClass player {
   Name "player"
   Pos 64 0
   Size 64 64
   Flags 0
  }
  ImageSetDefClass map_marker {
   Name "map_marker"
   Pos 128 0
   Size 64 64
   Flags 0
  }
 }
}
```

**4. Registre no config.cpp**

Adicione o caminho do imageset ao config.cpp do seu mod:

```cpp
class imageSets
{
    files[] =
    {
        "MyMod/GUI/imagesets/mymod_icons.imageset"
    };
};
```

**5. Use em Layouts e Scripts**

```
ImageWidgetClass SettingsIcon {
 image0 "set:mymod_icons image:settings"
 size 32 32
 hexactsize 1
 vexactsize 1
}
```

---

## Padrao de Integracao Font Awesome

O MyFramework (herdado do DabsFramework) demonstra um padrao poderoso: converter fontes de icones Font Awesome em imagesets do DayZ. Isso da aos mods acesso a milhares de icones de qualidade profissional sem criar arte personalizada.

### Como Funciona

1. Icones do Font Awesome sao renderizados em um atlas de textura em um tamanho fixo de grade (64x64 por icone)
2. Cada estilo de icone ganha seu proprio imageset: `solid`, `regular`, `light`, `thin`, `brands`
3. Nomes de icone no imageset correspondem aos nomes do Font Awesome (ex.: `circle`, `arrow_down`, `discord`)
4. Os imagesets sao registrados no config.cpp e disponiveis para qualquer layout ou script

### Conjuntos de Icones do MyFramework / DabsFramework

```
MyFramework/GUI/icons/
  solid.imageset       -- Icones preenchidos (atlas 3648x3712, 64x64 por icone)
  regular.imageset     -- Icones delineados
  light.imageset       -- Icones delineados leves
  thin.imageset        -- Icones delineados ultra-finos
  brands.imageset      -- Logos de marcas (Discord, GitHub, etc.)
```

### Uso em Layouts

```
image0 "set:solid image:circle"
image0 "set:solid image:gear"
image0 "set:regular image:arrow_down_short_wide"
image0 "set:brands image:discord"
image0 "set:brands image:500px"
```

### Uso em Scripts

```c
// DayZ Editor using the solid set
CollapseIcon.LoadImageFile(1, "set:solid image:square_minus");
CollapseIcon.LoadImageFile(0, "set:regular image:square_plus");
```

### Por Que Este Padrao Funciona Bem

- **Biblioteca massiva de icones**: Milhares de icones disponiveis sem nenhuma criacao de arte
- **Estilo consistente**: Todos os icones compartilham o mesmo peso visual e estilo
- **Multiplos pesos**: Escolha solid, regular, light ou thin para diferentes contextos visuais
- **Icones de marca**: Logos prontos para Discord, Steam, GitHub, etc.
- **Nomes padrao**: Nomes de icone seguem convencoes do Font Awesome, tornando a descoberta facil

### A Estrutura do Atlas

O imageset solid, por exemplo, tem um `RefSize` de 3648x3712 com icones organizados em intervalos de 64 pixels:

```
ImageSetClass {
 Name "solid"
 RefSize 3648 3712
 Textures {
  ImageSetTextureClass {
   mpix 1
   path "MyFramework/GUI/icons/solid.edds"
  }
 }
 Images {
  ImageSetDefClass circle {
   Name "circle"
   Pos 0 0
   Size 64 64
   Flags 0
  }
  ImageSetDefClass 360_degrees {
   Name "360_degrees"
   Pos 320 0
   Size 64 64
   Flags 0
  }
  ...
 }
}
```

---

## Exemplos Reais

### VPP Admin Tools

VPP empacota todos os icones de ferramentas admin em um unico atlas 1920x1080 com posicionamento livre (nao uma grade rigida):

```
ImageSetClass {
 Name "dayz_gui_vpp"
 RefSize 1920 1080
 Textures {
  ImageSetTextureClass {
   mpix 1
   path "{534691EE0479871E}VPPAdminTools/GUI/Textures/dayz_gui_vpp.edds"
  }
 }
 Images {
  ImageSetDefClass vpp_icon_cloud {
   Name "vpp_icon_cloud"
   Pos 1206 108
   Size 62 62
   Flags 0
  }
  ImageSetDefClass vpp_icon_players {
   Name "vpp_icon_players"
   Pos 391 112
   Size 62 62
   Flags 0
  }
 }
}
```

Referenciado em layouts como:
```
image0 "set:dayz_gui_vpp image:vpp_icon_cloud"
```

### MyWeapons Mod

Icones de armas e acessorios empacotados em atlas grandes com tamanhos variados de icone:

```
ImageSetClass {
 Name "SNAFU_Weapons_Icons"
 RefSize 2048 2048
 Textures {
  ImageSetTextureClass {
   mpix 1
   path "{7C781F3D4B1173D4}SNAFU_Guns_01/gui/Imagesets/SNAFU_Weapons_Icons.edds"
  }
 }
 Images {
  ImageSetDefClass SNAFUFGRIP {
   Name "SNAFUFGRIP"
   Pos 123 19
   Size 300 300
   Flags 0
  }
  ImageSetDefClass SNAFU_M14Optic {
   Name "SNAFU_M14Optic"
   Pos 426 20
   Size 300 300
   Flags 0
  }
 }
}
```

Isso mostra que icones nao precisam ser de tamanho uniforme --- icones de inventario para armas usam 300x300 enquanto icones de UI tipicamente usam 64x64.

### MyFramework Prefabs

Primitivas de UI (cantos arredondados, gradientes alfa) empacotadas em um atlas pequeno de 256x256:

```
ImageSetClass {
 Name "prefabs"
 RefSize 256 256
 Textures {
  ImageSetTextureClass {
   mpix 1
   path "{82F14D6B9D1AA1CE}MyFramework/GUI/imagesets/prefabs.edds"
  }
 }
 Images {
  ImageSetDefClass Round_Outline_TopLeft {
   Name "Round_Outline_TopLeft"
   Pos 24 21
   Size 8 8
   Flags 0
  }
  ImageSetDefClass "Alpha 10" {
   Name "Alpha 10"
   Pos 0 15
   Size 1 1
   Flags 0
  }
 }
}
```

Notavel: nomes de imagem podem conter espacos quando entre aspas (ex.: `"Alpha 10"`). Porem, referenciar estes em layouts requer o nome exato incluindo o espaco.

### MyMod Market Hub (Formato XML)

Um imageset XML mais simples para o modulo market hub:

```xml
<?xml version="1.0" encoding="utf-8"?>
<imageset name="mh_icons" file="DayZMarketHub/GUI/imagesets/mh_icons.edds">
  <image name="icon_store" pos="0 0" size="64 64" />
  <image name="icon_cart" pos="64 0" size="64 64" />
  <image name="icon_wallet" pos="128 0" size="64 64" />
  <image name="icon_vip" pos="192 0" size="64 64" />
  <image name="icon_weapons" pos="0 64" size="64 64" />
  <image name="icon_success" pos="0 192" size="64 64" />
  <image name="icon_error" pos="64 192" size="64 64" />
</imageset>
```

Referenciado como:
```
image0 "set:mh_icons image:icon_store"
```

---

## Erros Comuns

### Esquecendo o Registro no config.cpp

O problema mais comum. Se seu arquivo de imageset existe mas nao esta listado em `class imageSets { files[] = { ... }; };` no config.cpp, o motor nunca o carrega. Todas as referencias de imagem falharao silenciosamente (widgets aparecem em branco).

### Colisao de Nomes de Conjunto

Se dois mods registram imagesets com o mesmo `Name`, apenas um e carregado (o ultimo vence). Use um prefixo unico:

```
Name "mymod_icons"     -- Bom
Name "icons"           -- Arriscado, muito generico
```

### Caminho de Textura Errado

O `path` deve ser relativo a raiz do PBO (como o arquivo aparece dentro do PBO empacotado):

```
path "MyMod/GUI/imagesets/icons.edds"     -- Correto se MyMod e a raiz do PBO
path "GUI/imagesets/icons.edds"            -- Errado se a raiz do PBO e MyMod/
path "C:/Users/dev/icons.edds"            -- Errado: caminhos absolutos nao funcionam
```

### RefSize Incompativel

O `RefSize` deve corresponder as dimensoes reais em pixels da sua textura. Se voce especificar `RefSize 512 512` mas sua textura e 1024x1024, todas as posicoes de icone estarao deslocadas por um fator de dois.

### Coordenadas Pos com Offset de Um

`Pos` e o canto superior esquerdo da regiao do icone. Se seus icones estao em intervalos de 64 pixels mas voce acidentalmente desloca por 1 pixel, icones terao uma fatia fina do icone adjacente visivel.

### Usando .png ou .tga Diretamente

O motor requer formato `.edds` para atlas de textura referenciados por imagesets. Arquivos `.png` ou `.tga` brutos nao serao carregados. Sempre converta para `.edds` usando o DayZ Workbench ou as ferramentas do Mikero.

### Espacos em Nomes de Imagem

Embora o motor suporte espacos em nomes de imagem (ex.: `"Alpha 10"`), eles podem causar problemas em alguns contextos de parsing. Prefira underscores: `Alpha_10`.
