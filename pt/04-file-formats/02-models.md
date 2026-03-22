# Chapter 4.2: 3D Models (.p3d)

[Home](../../README.md) | [<< Previous: Textures](01-textures.md) | **3D Models** | [Next: Materials >>](03-materials.md)

---

## Introducao

Todo objeto fisico no DayZ -- armas, roupas, edificios, veiculos, arvores, pedras -- e um modelo 3D armazenado no formato proprietario **P3D** da Bohemia. O formato P3D e muito mais do que um container de malha: ele codifica multiplos niveis de detalhe, geometria de colisao, selecoes de animacao, pontos de memoria para acessorios e efeitos, e posicoes de proxy para itens montaveis. Entender como os arquivos P3D funcionam e como cria-los com o **Object Builder** e essencial para qualquer mod que adicione itens fisicos ao mundo do jogo.

Este capitulo cobre a estrutura do formato P3D, o sistema de LODs, selecoes nomeadas, pontos de memoria, o sistema de proxy, configuracao de animacao via `model.cfg`, e o fluxo de importacao a partir de formatos 3D padrao.

---

## Sumario

- [Visao Geral do Formato P3D](#visao-geral-do-formato-p3d)
- [Object Builder](#object-builder)
- [O Sistema de LODs](#o-sistema-de-lods)
- [Selecoes Nomeadas](#selecoes-nomeadas)
- [Pontos de Memoria](#pontos-de-memoria)
- [O Sistema de Proxy](#o-sistema-de-proxy)
- [Model.cfg para Animacoes](#modelcfg-para-animacoes)
- [Importando de FBX/OBJ](#importando-de-fbxobj)
- [Tipos Comuns de Modelo](#tipos-comuns-de-modelo)
- [Erros Comuns](#erros-comuns)
- [Boas Praticas](#boas-praticas)

---

## Visao Geral do Formato P3D

**P3D** (Point 3D) e o formato binario de modelo 3D da Bohemia Interactive, herdado do motor Real Virtuality e mantido no Enfusion. E um formato compilado e pronto para o motor -- voce nao escreve arquivos P3D manualmente.

### Caracteristicas Principais

- **Formato binario:** Nao e legivel por humanos. Criado e editado exclusivamente com o Object Builder.
- **Container multi-LOD:** Um unico arquivo P3D contem multiplas malhas LOD (Level of Detail), cada uma com um proposito diferente.
- **Nativo do motor:** O motor do DayZ carrega P3D diretamente. Nenhuma conversao em tempo de execucao ocorre.
- **Binarizado vs. nao-binarizado:** Arquivos P3D de origem do Object Builder sao "MLOD" (editaveis). O Binarize os converte para "ODOL" (otimizado, somente leitura). O jogo pode carregar ambos, mas ODOL carrega mais rapido e e menor.

### Tipos de Arquivo que Voce Encontrara

| Extensao | Descricao |
|----------|-----------|
| `.p3d` | Modelo 3D (tanto MLOD de origem quanto ODOL binarizado) |
| `.rtm` | Runtime Motion -- dados de keyframe de animacao |
| `.bisurf` | Arquivo de propriedades de superficie (usado junto com P3D) |

### MLOD vs. ODOL

| Propriedade | MLOD (Origem) | ODOL (Binarizado) |
|-------------|---------------|-------------------|
| Criado por | Object Builder | Binarize |
| Editavel | Sim | Nao |
| Tamanho do arquivo | Maior | Menor |
| Velocidade de carregamento | Mais lento | Mais rapido |
| Usado durante | Desenvolvimento | Distribuicao |
| Contem | Dados completos de edicao, selecoes nomeadas | Dados de malha otimizados |

> **Importante:** Quando voce empacota um PBO com binarizacao habilitada, seus arquivos P3D MLOD sao automaticamente convertidos para ODOL. Se voce empacotar com `-packonly`, os arquivos MLOD sao incluidos como estao. Ambos funcionam no jogo, mas ODOL e preferido para builds de distribuicao.

---

## Object Builder

**Object Builder** e a ferramenta fornecida pela Bohemia para criar e editar modelos P3D. Esta incluido no pacote DayZ Tools no Steam.

### Capacidades Principais

- Criar e editar malhas 3D com vertices, arestas e faces.
- Definir multiplos LODs dentro de um unico arquivo P3D.
- Atribuir **selecoes nomeadas** (grupos de vertices/faces) para animacao e controle de textura.
- Posicionar **pontos de memoria** para posicoes de acessorios, origens de particulas e fontes de som.
- Adicionar **objetos proxy** para itens acoplaveis (carregadores, miras, etc.).
- Atribuir materiais (`.rvmat`) e texturas (`.paa`) a faces.
- Importar malhas dos formatos FBX, OBJ e 3DS.
- Exportar arquivos P3D validados para o Binarize.

### Configuracao do Workspace

O Object Builder requer a **unidade P:** (workdrive) configurada. Esta unidade virtual fornece um prefixo de caminho unificado que o motor usa para localizar assets.

```
P:\
  DZ\                        <-- Vanilla DayZ data (extracted)
  DayZ Tools\                <-- Tools installation
  MyMod\                     <-- Your mod's source directory
    data\
      models\
        my_item.p3d
      textures\
        my_item_co.paa
```

Todos os caminhos em arquivos P3D e materiais sao relativos a raiz da unidade P:. Por exemplo, uma referencia de material dentro do modelo seria `MyMod\data\textures\my_item_co.paa`.

### Fluxo de Trabalho Basico no Object Builder

1. **Crie ou importe** sua geometria de malha.
2. **Defina LODs** -- no minimo, crie LODs de Resolution, Geometry e Fire Geometry.
3. **Atribua materiais** a faces no LOD Resolution.
4. **Nomeie selecoes** para quaisquer partes que animam, trocam texturas ou precisam de interacao via codigo.
5. **Posicione pontos de memoria** para acessorios, posicoes de flash de boca, portas de ejecao, etc.
6. **Adicione proxies** para itens que podem ser acoplados (miras, carregadores, supressores).
7. **Valide** usando a validacao integrada do Object Builder (Structure --> Validate).
8. **Salve** como P3D.
9. **Faca o build** via Binarize ou AddonBuilder.

---

## O Sistema de LODs

Um arquivo P3D contem multiplos **LODs** (Levels of Detail), cada um servindo a um proposito especifico. O motor seleciona qual LOD usar com base na situacao -- distancia da camera, calculos de fisica, renderizacao de sombras, etc.

### Tipos de LOD

| LOD | Valor de Resolucao | Proposito |
|-----|---------------------|-----------|
| **Resolution 0** | 1.000 | Malha visual de maior detalhe. Renderizado quando o objeto esta proximo da camera. |
| **Resolution 1** | 1.100 | Detalhe medio. Renderizado a distancia moderada. |
| **Resolution 2** | 1.200 | Detalhe baixo. Renderizado a distancia longa. |
| **Resolution 3+** | 1.300+ | LODs de distancia adicionais. |
| **View Geometry** | Especial | Determina o que bloqueia a visao do jogador (primeira pessoa). Malha simplificada. |
| **Fire Geometry** | Especial | Colisao para balas e projeteis. Deve ser convexo ou composto por partes convexas. |
| **Geometry** | Especial | Colisao de fisica. Usado para colisao de movimento, gravidade, posicionamento. Deve ser convexo ou composto por decomposicao convexa. |
| **Shadow 0** | Especial | Malha de projecao de sombra (curta distancia). |
| **Shadow 1000** | Especial | Malha de projecao de sombra (longa distancia). Mais simples que Shadow 0. |
| **Memory** | Especial | Contem apenas pontos nomeados (sem geometria visivel). Usado para posicoes de acessorios, origens de som, etc. |
| **Roadway** | Especial | Define superficies caminhaveis em objetos (veiculos, edificios com interiores acessiveis). |
| **Paths** | Especial | Dicas de pathfinding de IA para edificios. |

### Valores de Resolucao de LOD (LODs Visuais)

O motor usa uma formula baseada em distancia e tamanho do objeto para determinar qual LOD visual renderizar:

```
LOD selected = (distance_to_object * LOD_factor) / object_bounding_sphere_radius
```

Valores mais baixos = camera mais proxima. O motor encontra o LOD cujo valor de resolucao e a correspondencia mais proxima ao valor calculado.

### Criando LODs no Object Builder

1. **File --> New LOD** ou clique com o botao direito na lista de LODs.
2. Selecione o tipo de LOD no dropdown.
3. Para LODs visuais (Resolution), insira o valor de resolucao.
4. Modele a geometria para aquele LOD.

### Requisitos de LOD por Tipo de Item

| Tipo de Item | LODs Obrigatorios | LODs Adicionais Recomendados |
|--------------|-------------------|------------------------------|
| **Item de mao** | Resolution 0, Geometry, Fire Geometry, Memory | Shadow 0, Resolution 1 |
| **Roupa** | Resolution 0, Geometry, Fire Geometry, Memory | Shadow 0, Resolution 1, Resolution 2 |
| **Arma** | Resolution 0, Geometry, Fire Geometry, View Geometry, Memory | Shadow 0, Resolution 1, Resolution 2 |
| **Edificio** | Resolution 0, Geometry, Fire Geometry, View Geometry, Memory | Shadow 0, Shadow 1000, Roadway, Paths |
| **Veiculo** | Resolution 0, Geometry, Fire Geometry, View Geometry, Memory | Shadow 0, Roadway, Resolution 1+ |

### Regras do LOD Geometry

Os LODs Geometry e Fire Geometry possuem requisitos rigorosos:

- **Devem ser convexos** ou compostos por multiplos componentes convexos. O sistema de fisica do motor requer formas de colisao convexas.
- **Selecoes nomeadas devem combinar** com as do LOD Resolution (para partes animadas).
- **Massa deve ser definida.** Selecione todos os vertices no LOD Geometry e atribua massa via **Structure --> Mass**. Isso determina o peso fisico do objeto.
- **Mantenha simples.** Menos triangulos = melhor desempenho de fisica. O LOD geometry de uma arma pode ter 20-50 triangulos vs. milhares no LOD visual.

---

## Selecoes Nomeadas

Selecoes nomeadas sao grupos de vertices, arestas ou faces dentro de um LOD que sao marcados com um nome. Elas servem como handles que o motor e scripts usam para manipular partes de um modelo.

### O Que Selecoes Nomeadas Fazem

| Proposito | Exemplo de Nome de Selecao | Usado Por |
|-----------|----------------------------|-----------|
| **Animacao** | `bolt`, `trigger`, `magazine` | Fontes de animacao do `model.cfg` |
| **Troca de texturas** | `camo`, `camo1`, `body` | `hiddenSelections[]` no config.cpp |
| **Texturas de dano** | `zbytek` | Sistema de dano do motor, trocas de material |
| **Pontos de acoplamento** | `magazine`, `optics`, `suppressor` | Sistema de proxy e acessorios |

### hiddenSelections (Troca de Texturas)

O uso mais comum de selecoes nomeadas para modders e **hiddenSelections** -- a capacidade de trocar texturas em tempo de execucao via config.cpp.

**No modelo P3D (LOD Resolution):**
1. Selecione as faces que devem ser retexturaveis.
2. Nomeie a selecao (ex.: `camo`).

**No config.cpp:**
```cpp
class MyRifle: Rifle_Base
{
    hiddenSelections[] = {"camo"};
    hiddenSelectionsTextures[] = {"MyMod\data\my_rifle_co.paa"};
    hiddenSelectionsMaterials[] = {"MyMod\data\my_rifle.rvmat"};
};
```

Isso permite variantes diferentes do mesmo modelo com texturas diferentes sem duplicar o arquivo P3D.

### Criando Selecoes Nomeadas

No Object Builder:

1. Selecione os vertices ou faces que deseja agrupar.
2. Va em **Structure --> Named Selections** (ou pressione Ctrl+N).
3. Clique em **New**, insira o nome da selecao.
4. Clique em **Assign** para marcar a geometria selecionada com aquele nome.

> **Dica:** Nomes de selecao sao case-sensitive. `Camo` e `camo` sao selecoes diferentes. A convencao e usar minusculas.

### Selecoes Entre LODs

Selecoes nomeadas devem ser consistentes entre LODs para que as animacoes funcionem:

- Se a selecao `bolt` existe no Resolution 0, ela tambem deve existir nos LODs Geometry e Fire Geometry (cobrindo a geometria de colisao correspondente).
- LODs de Shadow tambem devem ter a selecao se a parte animada deve projetar sombras corretas.

---

## Pontos de Memoria

Pontos de memoria sao posicoes nomeadas definidas no **LOD Memory**. Eles nao possuem representacao visual no jogo -- definem coordenadas espaciais que o motor e scripts referenciam para posicionar efeitos, acessorios, sons e mais.

### Pontos de Memoria Comuns

| Nome do Ponto | Proposito |
|----------------|-----------|
| `usti hlavne` | Posicao do cano (onde as balas originam, flash de boca aparece) |
| `konec hlavne` | Fim do cano (usado com `usti hlavne` para definir direcao do cano) |
| `nabojnicestart` | Inicio da porta de ejecao (onde estojos emergem) |
| `nabojniceend` | Fim da porta de ejecao (direcao de ejecao) |
| `handguard` | Ponto de acoplamento do handguard |
| `magazine` | Posicao do alojamento do carregador |
| `optics` | Posicao do trilho de mira |
| `suppressor` | Posicao de montagem do supressor |
| `trigger` | Posicao do gatilho (para IK da mao) |
| `pistolgrip` | Posicao do punho (para IK da mao) |
| `lefthand` | Posicao de empunhadura da mao esquerda |
| `righthand` | Posicao de empunhadura da mao direita |
| `eye` | Posicao do olho (para alinhamento de visao em primeira pessoa) |
| `pilot` | Posicao do assento do motorista/piloto (veiculos) |
| `light_l` / `light_r` | Posicoes do farol esquerdo/direito (veiculos) |

### Pontos de Memoria Direcionais

Muitos efeitos precisam tanto de uma posicao quanto de uma direcao. Isso e alcancado com pares de pontos de memoria:

```
usti hlavne  ------>  konec hlavne
(muzzle start)        (muzzle end)

The direction vector is: konec hlavne - usti hlavne
```

### Criando Pontos de Memoria no Object Builder

1. Mude para o **LOD Memory** na lista de LODs.
2. Crie um vertice na posicao desejada.
3. Nomeie-o via **Structure --> Named Selections**: crie uma selecao com o nome do ponto e atribua o vertice unico a ela.

> **Nota:** O LOD Memory deve conter APENAS pontos nomeados (vertices individuais). Nao crie faces ou arestas no LOD Memory.

---

## O Sistema de Proxy

Proxies definem posicoes onde outros modelos P3D podem ser acoplados. Quando voce ve um carregador inserido em uma arma, uma mira montada em um trilho, ou um supressor parafusado em um cano -- esses sao modelos acoplados por proxy.

### Como Proxies Funcionam

Um proxy e uma referencia especial colocada no LOD Resolution que aponta para outro arquivo P3D. O motor renderiza o modelo referenciado pelo proxy na posicao e orientacao do proxy.

### Convencao de Nomenclatura de Proxy

Nomes de proxy seguem o padrao: `proxy:\path\to\model.p3d`

Para proxies de acessorios em armas, os nomes padrao sao:

| Caminho do Proxy | Tipo de Acessorio |
|------------------|-------------------|
| `proxy:\dz\weapons\attachments\magazine\mag_placeholder.p3d` | Slot de carregador |
| `proxy:\dz\weapons\attachments\optics\optic_placeholder.p3d` | Trilho de mira |
| `proxy:\dz\weapons\attachments\suppressor\sup_placeholder.p3d` | Montagem de supressor |
| `proxy:\dz\weapons\attachments\handguard\handguard_placeholder.p3d` | Slot de handguard |
| `proxy:\dz\weapons\attachments\stock\stock_placeholder.p3d` | Slot de coronha |

### Adicionando Proxies no Object Builder

1. No LOD Resolution, posicione o cursor 3D onde o acessorio deve aparecer.
2. Va em **Structure --> Proxy --> Create**.
3. Insira o caminho do proxy (ex.: `dz\weapons\attachments\magazine\mag_placeholder.p3d`).
4. O proxy aparece como uma pequena seta indicando posicao e orientacao.
5. Rotacione e posicione o proxy para alinhar corretamente com a geometria do acessorio.

### Indice do Proxy

Cada proxy tem um numero de indice (comecando em 1). Quando um modelo tem multiplos proxies do mesmo tipo, o indice os diferencia. O indice e referenciado no config.cpp:

```cpp
class MyWeapon: Rifle_Base
{
    class Attachments
    {
        class magazine
        {
            type = "magazine";
            proxy = "proxy:\dz\weapons\attachments\magazine\mag_placeholder.p3d";
            proxyIndex = 1;
        };
    };
};
```

---

## Model.cfg para Animacoes

O arquivo `model.cfg` define animacoes para modelos P3D. Ele mapeia fontes de animacao (controladas pela logica do jogo) para transformacoes em selecoes nomeadas.

### Estrutura Basica

```cpp
class CfgModels
{
    class Default
    {
        sectionsInherit = "";
        sections[] = {};
        skeletonName = "";
    };

    class MyRifle: Default
    {
        skeletonName = "MyRifle_skeleton";
        sections[] = {"camo"};

        class Animations
        {
            class bolt_move
            {
                type = "translation";
                source = "reload";        // Engine animation source
                selection = "bolt";       // Named selection in P3D
                axis = "bolt_axis";       // Axis memory point pair
                memory = 1;               // Axis defined in Memory LOD
                minValue = 0;
                maxValue = 1;
                offset0 = 0;
                offset1 = 0.05;           // 5cm translation
            };

            class trigger_move
            {
                type = "rotation";
                source = "trigger";
                selection = "trigger";
                axis = "trigger_axis";
                memory = 1;
                minValue = 0;
                maxValue = 1;
                angle0 = 0;
                angle1 = -0.4;            // Radians
            };
        };
    };
};

class CfgSkeletons
{
    class Default
    {
        isDiscrete = 0;
        skeletonInherit = "";
        skeletonBones[] = {};
    };

    class MyRifle_skeleton: Default
    {
        skeletonBones[] =
        {
            "bolt", "",          // "bone_name", "parent_bone" ("" = root)
            "trigger", "",
            "magazine", ""
        };
    };
};
```

### Tipos de Animacao

| Tipo | Palavra-chave | Movimento | Controlado Por |
|------|---------------|-----------|----------------|
| **Translacao** | `translation` | Movimento linear ao longo de um eixo | `offset0` / `offset1` (metros) |
| **Rotacao** | `rotation` | Rotacao em torno de um eixo | `angle0` / `angle1` (radianos) |
| **RotationX/Y/Z** | `rotationX` | Rotacao em torno de um eixo fixo do mundo | `angle0` / `angle1` |
| **Ocultar** | `hide` | Mostrar/ocultar uma selecao | Limiar `hideValue` |

### Fontes de Animacao

Fontes de animacao sao valores fornecidos pelo motor que controlam as animacoes:

| Fonte | Faixa | Descricao |
|-------|-------|-----------|
| `reload` | 0-1 | Fase de recarga da arma |
| `trigger` | 0-1 | Puxar do gatilho |
| `zeroing` | 0-N | Configuracao de zeragem da arma |
| `isFlipped` | 0-1 | Estado de virada da mira de ferro |
| `door` | 0-1 | Porta aberta/fechada |
| `rpm` | 0-N | RPM do motor do veiculo |
| `speed` | 0-N | Velocidade do veiculo |
| `fuel` | 0-1 | Nivel de combustivel do veiculo |
| `damper` | 0-1 | Suspensao do veiculo |

---

## Importando de FBX/OBJ

A maioria dos modders cria modelos 3D em ferramentas externas (Blender, 3ds Max, Maya) e os importa para o Object Builder.

### Formatos de Importacao Suportados

| Formato | Extensao | Notas |
|---------|----------|-------|
| **FBX** | `.fbx` | Melhor compatibilidade. Exporte como FBX 2013 ou posterior (binario). |
| **OBJ** | `.obj` | Wavefront OBJ. Apenas dados de malha simples (sem animacoes). |
| **3DS** | `.3ds` | Formato legado do 3ds Max. Limitado a 65K vertices por malha. |

### Fluxo de Importacao

**Passo 1: Prepare no seu software 3D**
- O modelo deve estar centralizado na origem.
- Aplique todas as transformacoes (localizacao, rotacao, escala).
- Escala: 1 unidade = 1 metro. O DayZ usa metros.
- Triangule a malha (o Object Builder trabalha com triangulos).
- Faca o UV unwrap do modelo.
- Exporte como FBX (binario, sem animacao, Y-up ou Z-up -- o Object Builder lida com ambos).

**Passo 2: Importe para o Object Builder**
1. Abra o Object Builder.
2. **File --> Import --> FBX** (ou OBJ/3DS).
3. Revise as configuracoes de importacao:
   - Fator de escala (deve ser 1.0 se sua origem esta em metros).
   - Conversao de eixo (Z-up para Y-up se necessario).
4. A malha aparece em um novo LOD Resolution.

**Passo 3: Configuracao pos-importacao**
1. Atribua materiais a faces (selecione faces, clique direito --> **Face Properties**).
2. Crie LODs adicionais (Geometry, Fire Geometry, Memory, Shadow).
3. Simplifique a geometria para LODs de colisao (remova pequenos detalhes, garanta convexidade).
4. Adicione selecoes nomeadas, pontos de memoria e proxies.
5. Valide e salve.

### Dicas Especificas para Blender

- Use o addon comunitario **Blender DayZ Toolbox** se disponivel -- ele agiliza as configuracoes de exportacao.
- Exporte com: **Apply Modifiers**, **Triangulate Faces**, **Apply Scale**.
- Defina **Forward: -Z Forward**, **Up: Y Up** no dialogo de exportacao FBX.
- Nomeie os objetos de malha no Blender para corresponder as selecoes nomeadas pretendidas -- alguns importadores preservam nomes de objeto.

---

## Tipos Comuns de Modelo

### Armas

Armas sao os modelos P3D mais complexos, exigindo:
- LOD Resolution de alta poligonagem (5.000-20.000 triangulos)
- Multiplas selecoes nomeadas (bolt, trigger, magazine, camo, etc.)
- Conjunto completo de pontos de memoria (cano, ejecao, posicoes de empunhadura)
- Multiplos proxies (carregador, mira, supressor, handguard, coronha)
- Skeleton e animacoes no model.cfg
- View Geometry para obstrucao em primeira pessoa

### Roupas

Modelos de roupa sao rigged ao skeleton do personagem:
- LOD Resolution segue a estrutura de ossos do personagem
- Selecoes nomeadas para variantes de textura (`camo`, `camo1`)
- Geometria de colisao mais simples
- Sem proxies (geralmente)
- hiddenSelections para variantes de cor/camuflagem

### Edificios

Edificios possuem requisitos unicos:
- LODs Resolution grandes e detalhados
- LOD Roadway para superficies caminhaveis (pisos, escadas)
- LOD Paths para navegacao de IA
- View Geometry para evitar ver atraves das paredes
- Multiplos LODs de Shadow para desempenho em diferentes distancias
- Selecoes nomeadas para portas e janelas que abrem

### Veiculos

Veiculos combinam muitos sistemas:
- LOD Resolution detalhado com partes animadas (rodas, portas, capo)
- Skeleton complexo com muitos ossos
- LOD Roadway para passageiros em pe em cacambas de caminhoes
- Pontos de memoria para luzes, escapamento, posicao do motorista, assentos de passageiros
- Multiplos proxies para acessorios (rodas, portas)

---

## Erros Comuns

### 1. LOD Geometry Ausente

**Sintoma:** Objeto nao tem colisao. Jogadores e balas passam atraves dele.
**Correcao:** Crie um LOD Geometry com uma malha convexa simplificada. Atribua massa aos vertices.

### 2. Formas de Colisao Nao-Convexas

**Sintoma:** Glitches de fisica, objetos quicando erraticamente, itens caindo atraves de superficies.
**Correcao:** Divida formas complexas em multiplos componentes convexos no LOD Geometry. Cada componente deve ser um solido convexo fechado.

### 3. Selecoes Nomeadas Inconsistentes

**Sintoma:** Animacoes so funcionam visualmente mas nao para colisao, ou sombra nao anima.
**Correcao:** Garanta que toda selecao nomeada que existe no LOD Resolution tambem exista nos LODs Geometry, Fire Geometry e Shadow.

### 4. Escala Errada

**Sintoma:** Objeto e gigantesco ou microscopico no jogo.
**Correcao:** Verifique se seu software 3D usa metros como unidade. Um personagem do DayZ tem aproximadamente 1,8 metros de altura.

### 5. Pontos de Memoria Ausentes

**Sintoma:** Flash de boca aparece na posicao errada, acessorios flutuam no espaco.
**Correcao:** Crie o LOD Memory e adicione todos os pontos nomeados necessarios nas posicoes corretas.

### 6. Massa Nao Definida

**Sintoma:** Objeto nao pode ser pego, ou interacoes de fisica se comportam estranhamente.
**Correcao:** Selecione todos os vertices no LOD Geometry e atribua massa via **Structure --> Mass**.

---

## Boas Praticas

1. **Comece pelo LOD Geometry.** Esboce sua forma de colisao primeiro, depois construa o detalhe visual em cima. Isso previne o erro comum de criar um modelo bonito que nao consegue colidir adequadamente.

2. **Use modelos de referencia.** Extraia arquivos P3D vanilla dos dados do jogo e estude-os no Object Builder. Eles mostram exatamente o que o motor espera para cada tipo de item.

3. **Valide frequentemente.** Use **Structure --> Validate** do Object Builder apos cada mudanca significativa. Corrija avisos antes que se tornem bugs misteriosos no jogo.

4. **Mantenha contagens de triangulos dos LODs proporcionais.** Resolution 0 pode ter 10.000 triangulos; Resolution 1 deve ter ~5.000; Geometry deve ter ~100-500. Reducao dramatica em cada nivel.

5. **Nomeie selecoes descritivamente.** Use `bolt_carrier` em vez de `sel01`. Seu eu do futuro (e outros modders) agradecerão.

6. **Teste com file patching primeiro.** Carregue seu P3D nao-binarizado via modo file patching antes de se comprometer com um build completo de PBO. Isso detecta a maioria dos problemas mais rapido.

7. **Documente pontos de memoria.** Mantenha uma imagem de referencia ou arquivo de texto listando todos os pontos de memoria e suas posicoes pretendidas. Armas complexas podem ter 20+ pontos.

---

## Navegacao

| Anterior | Acima | Proximo |
|----------|-------|---------|
| [4.1 Texturas](01-textures.md) | [Parte 4: Formatos de Arquivo & DayZ Tools](01-textures.md) | [4.3 Materiais](03-materials.md) |
