# Capitulo 4.3: Materiais (.rvmat)

[<< Anterior: Modelos 3D](02-models.md) | **Materiais** | [Proximo: Audio >>](04-audio.md)

---

## Introducao

Um material no DayZ e a ponte entre um modelo 3D e sua aparencia visual. Enquanto texturas fornecem dados brutos de imagem, o arquivo **RVMAT** (Real Virtuality Material) define como essas texturas sao combinadas, qual shader as interpreta e quais propriedades de superficie o motor deve simular -- brilho, transparencia, auto-iluminacao e mais. Toda face em todo modelo P3D no jogo referencia um arquivo RVMAT, e entender como cria-los e configura-los e essencial para qualquer mod visual.

Este capitulo cobre o formato de arquivo RVMAT, tipos de shader, configuracao de estagios de textura, propriedades de material, o sistema de troca de material por nivel de dano, e exemplos praticos extraidos dos DayZ-Samples.

---

## Sumario

- [Visao Geral do Formato RVMAT](#visao-geral-do-formato-rvmat)
- [Estrutura do Arquivo](#estrutura-do-arquivo)
- [Tipos de Shader](#tipos-de-shader)
- [Estagios de Textura](#estagios-de-textura)
- [Propriedades do Material](#propriedades-do-material)
- [Niveis de Saude (Troca de Material por Dano)](#niveis-de-saude-troca-de-material-por-dano)
- [Como Materiais Referenciam Texturas](#como-materiais-referenciam-texturas)
- [Criando um RVMAT do Zero](#criando-um-rvmat-do-zero)
- [Exemplos Reais](#exemplos-reais)
- [Erros Comuns](#erros-comuns)
- [Boas Praticas](#boas-praticas)

---

## Visao Geral do Formato RVMAT

Um arquivo **RVMAT** e um arquivo de configuracao baseado em texto (nao binario) que define um material. Apesar da extensao customizada, o formato e texto puro usando a sintaxe de configuracao estilo Bohemia com classes e pares chave-valor.

### Caracteristicas Principais

- **Formato texto:** Editavel em qualquer editor de texto (Notepad++, VS Code).
- **Vinculacao de shader:** Cada RVMAT especifica qual shader de renderizacao usar.
- **Mapeamento de textura:** Define quais arquivos de textura sao atribuidos a quais entradas do shader (diffuse, normal, specular, etc.).
- **Propriedades de superficie:** Controla intensidade specular, brilho emissivo, transparencia e mais.
- **Referenciado por modelos P3D:** Faces no LOD Resolution do Object Builder recebem um RVMAT. O motor carrega o RVMAT e todas as texturas que ele referencia.
- **Referenciado pelo config.cpp:** `hiddenSelectionsMaterials[]` pode sobrescrever materiais em tempo de execucao.

### Convencao de Caminho

Arquivos RVMAT ficam junto com suas texturas, tipicamente em um diretorio `data/`:

```
MyMod/
  data/
    my_item.rvmat              <-- Material definition
    my_item_co.paa             <-- Diffuse texture (referenced by the RVMAT)
    my_item_nohq.paa           <-- Normal map (referenced by the RVMAT)
    my_item_smdi.paa           <-- Specular map (referenced by the RVMAT)
```

---

## Estrutura do Arquivo

Um arquivo RVMAT tem uma estrutura consistente. Aqui esta um exemplo completo e anotado:

```cpp
ambient[] = {1.0, 1.0, 1.0, 1.0};        // Ambient color multiplier (RGBA)
diffuse[] = {1.0, 1.0, 1.0, 1.0};        // Diffuse color multiplier (RGBA)
forcedDiffuse[] = {0.0, 0.0, 0.0, 0.0};  // Additive diffuse override
emmisive[] = {0.0, 0.0, 0.0, 0.0};       // Emissive (self-illumination) color
specular[] = {0.7, 0.7, 0.7, 1.0};       // Specular highlight color
specularPower = 80;                        // Specular sharpness (higher = tighter highlight)
PixelShaderID = "Super";                   // Shader program to use
VertexShaderID = "Super";                  // Vertex shader program

class Stage1                               // Texture stage: Normal map
{
    texture = "MyMod\data\my_item_nohq.paa";
    uvSource = "tex";
    class uvTransform
    {
        aside[] = {1.0, 0.0, 0.0};
        up[] = {0.0, 1.0, 0.0};
        dir[] = {0.0, 0.0, 0.0};
        pos[] = {0.0, 0.0, 0.0};
    };
};

class Stage2                               // Texture stage: Diffuse/Color map
{
    texture = "MyMod\data\my_item_co.paa";
    uvSource = "tex";
    class uvTransform
    {
        aside[] = {1.0, 0.0, 0.0};
        up[] = {0.0, 1.0, 0.0};
        dir[] = {0.0, 0.0, 0.0};
        pos[] = {0.0, 0.0, 0.0};
    };
};

class Stage3                               // Texture stage: Specular/Metallic map
{
    texture = "MyMod\data\my_item_smdi.paa";
    uvSource = "tex";
    class uvTransform
    {
        aside[] = {1.0, 0.0, 0.0};
        up[] = {0.0, 1.0, 0.0};
        dir[] = {0.0, 0.0, 0.0};
        pos[] = {0.0, 0.0, 0.0};
    };
};
```

### Propriedades de Nivel Superior

Estas sao declaradas antes das classes Stage e controlam o comportamento geral do material:

| Propriedade | Tipo | Descricao |
|-------------|------|-----------|
| `ambient[]` | float[4] | Multiplicador de cor de luz ambiente. `{1,1,1,1}` = total, `{0,0,0,0}` = sem ambiente. |
| `diffuse[]` | float[4] | Multiplicador de cor de luz difusa. Geralmente `{1,1,1,1}`. |
| `forcedDiffuse[]` | float[4] | Override aditivo de difuso. Geralmente `{0,0,0,0}`. |
| `emmisive[]` | float[4] | Cor de auto-iluminacao. Valores nao-zero fazem a superficie brilhar. Nota: Bohemia usa a grafia errada `emmisive`, nao `emissive`. |
| `specular[]` | float[4] | Cor e intensidade do reflexo specular. |
| `specularPower` | float | Nitidez dos reflexos speculares. Faixa 1-200. Maior = mais apertado, reflexao mais focada. |
| `PixelShaderID` | string | Nome do programa de pixel shader. |
| `VertexShaderID` | string | Nome do programa de vertex shader. |

---

## Tipos de Shader

Os valores `PixelShaderID` e `VertexShaderID` determinam qual pipeline de renderizacao processa o material. Ambos geralmente devem ser configurados com o mesmo valor.

### Shaders Disponiveis

| Shader | Caso de Uso | Estagios de Textura Necessarios |
|--------|-------------|--------------------------------|
| **Super** | Superficies opacas padrao (armas, roupas, itens) | Normal, Diffuse, Specular/Metallic |
| **Multi** | Terreno multicamada e superficies complexas | Multiplos pares diffuse/normal |
| **Glass** | Superficies transparentes e semi-transparentes | Diffuse com alfa |
| **Water** | Superficies de agua com reflexao e refracao | Texturas especiais de agua |
| **Terrain** | Superficies de solo do terreno | Satelite, mascara, camadas de material |
| **NormalMap** | Superficie simplificada com normal map | Normal, Diffuse |
| **NormalMapSpecular** | Normal map com specular | Normal, Diffuse, Specular |
| **Hair** | Renderizacao de cabelo de personagem | Diffuse com alfa, translucencia especial |
| **Skin** | Pele de personagem com espalhamento subsuperficial | Diffuse, Normal, Specular |
| **AlphaTest** | Transparencia de borda rigida (folhagem, cercas) | Diffuse com alfa |
| **AlphaBlend** | Transparencia suave (vidro, fumaca) | Diffuse com alfa |

### Shader Super (Mais Comum)

O shader **Super** e o shader padrao de renderizacao baseada em fisica usado para a grande maioria dos itens no DayZ. Ele espera tres estagios de textura:

```
Stage1 = Normal map (_nohq)
Stage2 = Diffuse/Color map (_co)
Stage3 = Specular/Metallic map (_smdi)
```

Se voce esta criando um item de mod (arma, roupa, ferramenta, container), voce quase sempre usara o shader Super.

### Shader Glass

O shader **Glass** lida com superficies transparentes. Ele le o alfa da textura diffuse para determinar a transparencia:

```cpp
PixelShaderID = "Glass";
VertexShaderID = "Glass";

class Stage1
{
    texture = "MyMod\data\glass_nohq.paa";
    uvSource = "tex";
    class uvTransform { /* ... */ };
};

class Stage2
{
    texture = "MyMod\data\glass_ca.paa";    // Note: _ca suffix for color+alpha
    uvSource = "tex";
    class uvTransform { /* ... */ };
};
```

---

## Estagios de Textura

Cada classe `Stage` no RVMAT atribui uma textura a uma entrada especifica do shader. O numero do estagio determina qual funcao a textura desempenha.

### Atribuicoes de Estagio para o Shader Super

| Estagio | Funcao da Textura | Sufixo Tipico | Descricao |
|---------|-------------------|---------------|-----------|
| **Stage1** | Normal map | `_nohq` | Detalhe de superficie, relevos, sulcos |
| **Stage2** | Mapa diffuse / cor | `_co` ou `_ca` | Cor base da superficie |
| **Stage3** | Mapa specular / metalico | `_smdi` | Brilho, propriedades metalicas, detalhe |
| **Stage4** | Ambient Shadow | `_as` | Oclusao ambiental pre-assada (opcional) |
| **Stage5** | Mapa macro | `_mc` | Variacao de cor em larga escala (opcional) |
| **Stage6** | Mapa de detalhe | `_de` | Micro-detalhe com repeticao (opcional) |
| **Stage7** | Mapa emissivo / de luz | `_li` | Auto-iluminacao (opcional) |

### Propriedades do Estagio

Cada estagio contem:

```cpp
class Stage1
{
    texture = "path\to\texture.paa";    // Path relative to P: drive
    uvSource = "tex";                    // UV source: "tex" (model UVs) or "tex1" (2nd UV set)
    class uvTransform                    // UV transformation matrix
    {
        aside[] = {1.0, 0.0, 0.0};     // U-axis scale and direction
        up[] = {0.0, 1.0, 0.0};        // V-axis scale and direction
        dir[] = {0.0, 0.0, 0.0};       // Not typically used
        pos[] = {0.0, 0.0, 0.0};       // UV offset (translation)
    };
};
```

### UV Transform para Repeticao

Para repetir uma textura (repeti-la em uma superficie), modifique os valores `aside` e `up`:

```cpp
class uvTransform
{
    aside[] = {4.0, 0.0, 0.0};     // Tile 4x horizontally
    up[] = {0.0, 4.0, 0.0};        // Tile 4x vertically
    dir[] = {0.0, 0.0, 0.0};
    pos[] = {0.0, 0.0, 0.0};
};
```

Isso e comumente usado para materiais de terreno e superficies de edificios onde a mesma textura de detalhe se repete.

---

## Propriedades do Material

### Controle Specular

Os valores `specular[]` e `specularPower` trabalham juntos para definir quao brilhante uma superficie aparece:

| Tipo de Material | specular[] | specularPower | Aparencia |
|------------------|-----------|---------------|-----------|
| **Plastico fosco** | `{0.1, 0.1, 0.1, 1.0}` | 10 | Opaco, reflexo amplo |
| **Metal desgastado** | `{0.3, 0.3, 0.3, 1.0}` | 40 | Brilho moderado |
| **Metal polido** | `{0.8, 0.8, 0.8, 1.0}` | 120 | Reflexo brilhante e apertado |
| **Cromado** | `{1.0, 1.0, 1.0, 1.0}` | 200 | Reflexao tipo espelho |
| **Borracha** | `{0.02, 0.02, 0.02, 1.0}` | 5 | Quase sem reflexo |
| **Superficie molhada** | `{0.6, 0.6, 0.6, 1.0}` | 80 | Liso, reflexo medio-nitido |

### Emissivo (Auto-Iluminacao)

Para fazer uma superficie brilhar (LEDs, telas, elementos luminosos):

```cpp
emmisive[] = {0.2, 0.8, 0.2, 1.0};   // Green glow
```

A cor emissiva e adicionada a cor final do pixel independentemente da iluminacao. Um mapa emissivo `_li` em um estagio posterior de textura pode mascara quais partes da superficie brilham.

### Renderizacao em Dois Lados

Para superficies finas que devem ser visiveis de ambos os lados (bandeiras, folhagem, tecido):

```cpp
renderFlags[] = {"noZWrite", "noAlpha", "twoSided"};
```

Esta nao e uma propriedade de nivel superior do RVMAT, mas e configurada no config.cpp ou atraves das configuracoes de shader do material dependendo do caso de uso.

---

## Niveis de Saude (Troca de Material por Dano)

Itens do DayZ degradam ao longo do tempo. O motor suporta troca automatica de material em diferentes limiares de dano, definidos no `config.cpp` usando o array `healthLevels[]`. Isso cria a progressao visual de pristino ate arruinado.

### Estrutura do healthLevels[]

```cpp
class MyItem: Inventory_Base
{
    // ... other config ...

    healthLevels[] =
    {
        // {health_threshold, {"material_set"}},

        {1.0, {"MyMod\data\my_item.rvmat"}},           // Pristine (100% health)
        {0.7, {"MyMod\data\my_item_worn.rvmat"}},       // Worn (70% health)
        {0.5, {"MyMod\data\my_item_damaged.rvmat"}},     // Damaged (50% health)
        {0.3, {"MyMod\data\my_item_badly_damaged.rvmat"}},// Badly Damaged (30% health)
        {0.0, {"MyMod\data\my_item_ruined.rvmat"}}       // Ruined (0% health)
    };
};
```

### Como Funciona

1. O motor monitora o valor de saude do item (0.0 a 1.0).
2. Quando a saude cai abaixo de um limiar, o motor troca o material para o RVMAT correspondente.
3. Cada RVMAT pode referenciar texturas diferentes -- tipicamente variantes progressivamente mais danificadas.
4. A troca e automatica. Nenhum codigo de script e necessario.

### Progressao de Textura de Dano

Uma progressao tipica de dano:

| Nivel | Saude | Mudanca Visual |
|-------|-------|----------------|
| **Pristino** | 1.0 | Aparencia limpa, novo de fabrica |
| **Desgastado** | 0.7 | Arranhoes leves, desgaste menor |
| **Danificado** | 0.5 | Arranhoes visiveis, descoloracao, sujeira |
| **Muito Danificado** | 0.3 | Desgaste pesado, ferrugem, rachaduras, tinta descascando |
| **Arruinado** | 0.0 | Severamente degradado, aparencia quebrada |

### Criando Materiais de Dano

Para cada nivel de dano, crie um RVMAT separado que referencia texturas progressivamente mais danificadas:

```
data/
  my_item.rvmat                    --> my_item_co.paa (clean)
  my_item_worn.rvmat               --> my_item_worn_co.paa (light damage)
  my_item_damaged.rvmat            --> my_item_damaged_co.paa (moderate damage)
  my_item_badly_damaged.rvmat      --> my_item_badly_damaged_co.paa (heavy damage)
  my_item_ruined.rvmat             --> my_item_ruined_co.paa (destroyed)
```

> **Dica:** Voce nem sempre precisa de texturas unicas para cada nivel de dano. Uma otimizacao comum e compartilhar os normal maps e specular maps entre todos os niveis e mudar apenas a textura diffuse:
>
> ```
> my_item.rvmat           --> my_item_co.paa
> my_item_worn.rvmat      --> my_item_co.paa  (same diffuse, lower specular)
> my_item_damaged.rvmat   --> my_item_damaged_co.paa
> my_item_ruined.rvmat    --> my_item_ruined_co.paa
> ```

### Usando Materiais de Dano Vanilla

O DayZ fornece um conjunto de materiais genericos de overlay de dano que podem ser usados se voce nao quiser criar texturas de dano personalizadas:

```cpp
healthLevels[] =
{
    {1.0, {"MyMod\data\my_item.rvmat"}},
    {0.7, {"DZ\data\data\default_worn.rvmat"}},
    {0.5, {"DZ\data\data\default_damaged.rvmat"}},
    {0.3, {"DZ\data\data\default_badly_damaged.rvmat"}},
    {0.0, {"DZ\data\data\default_ruined.rvmat"}}
};
```

---

## Como Materiais Referenciam Texturas

A conexao entre modelos, materiais e texturas forma uma cadeia:

```
P3D Model (Object Builder)
  |
  |--> Face assigned to RVMAT
         |
         |--> Stage1.texture = "path\to\normal_nohq.paa"
         |--> Stage2.texture = "path\to\color_co.paa"
         |--> Stage3.texture = "path\to\specular_smdi.paa"
```

### Resolucao de Caminho

Todos os caminhos de textura em arquivos RVMAT sao relativos a raiz da **unidade P:**:

```cpp
// Correct: relative to P: drive
texture = "MyMod\data\textures\my_item_co.paa";

// This means: P:\MyMod\data\textures\my_item_co.paa
```

Quando empacotado em um PBO, o prefixo do caminho deve corresponder ao prefixo do PBO:

```
PBO prefix: MyMod
Internal path: data\textures\my_item_co.paa
Full reference: MyMod\data\textures\my_item_co.paa
```

### Override de hiddenSelectionsMaterials

O config.cpp pode sobrescrever qual material e aplicado a uma selecao nomeada em tempo de execucao:

```cpp
class MyItem_Green: MyItem
{
    hiddenSelections[] = {"camo"};
    hiddenSelectionsTextures[] = {"MyMod\data\my_item_green_co.paa"};
    hiddenSelectionsMaterials[] = {"MyMod\data\my_item_green.rvmat"};
};
```

Isso permite criar variantes de item (esquemas de cor, padroes de camuflagem) que compartilham o mesmo modelo P3D mas usam materiais diferentes.

---

## Criando um RVMAT do Zero

### Passo a Passo: Item Opaco Padrao

1. **Crie seus arquivos de textura:**
   - `my_item_co.paa` (cor diffuse)
   - `my_item_nohq.paa` (normal map)
   - `my_item_smdi.paa` (specular/metallic)

2. **Crie o arquivo RVMAT** (texto puro):

```cpp
ambient[] = {1.0, 1.0, 1.0, 1.0};
diffuse[] = {1.0, 1.0, 1.0, 1.0};
forcedDiffuse[] = {0.0, 0.0, 0.0, 0.0};
emmisive[] = {0.0, 0.0, 0.0, 0.0};
specular[] = {0.5, 0.5, 0.5, 1.0};
specularPower = 60;
PixelShaderID = "Super";
VertexShaderID = "Super";

class Stage1
{
    texture = "MyMod\data\my_item_nohq.paa";
    uvSource = "tex";
    class uvTransform
    {
        aside[] = {1.0, 0.0, 0.0};
        up[] = {0.0, 1.0, 0.0};
        dir[] = {0.0, 0.0, 0.0};
        pos[] = {0.0, 0.0, 0.0};
    };
};

class Stage2
{
    texture = "MyMod\data\my_item_co.paa";
    uvSource = "tex";
    class uvTransform
    {
        aside[] = {1.0, 0.0, 0.0};
        up[] = {0.0, 1.0, 0.0};
        dir[] = {0.0, 0.0, 0.0};
        pos[] = {0.0, 0.0, 0.0};
    };
};

class Stage3
{
    texture = "MyMod\data\my_item_smdi.paa";
    uvSource = "tex";
    class uvTransform
    {
        aside[] = {1.0, 0.0, 0.0};
        up[] = {0.0, 1.0, 0.0};
        dir[] = {0.0, 0.0, 0.0};
        pos[] = {0.0, 0.0, 0.0};
    };
};
```

3. **Atribua no Object Builder:**
   - Abra seu modelo P3D.
   - Selecione faces no LOD Resolution.
   - Clique direito --> **Face Properties**.
   - Navegue ate seu arquivo RVMAT.

4. **Teste no jogo** via file patching ou build de PBO.

---

## Exemplos Reais

### DayZ-Samples Test_ClothingRetexture

Os DayZ-Samples oficiais incluem um exemplo `Test_ClothingRetexture` que demonstra o fluxo de trabalho padrao de material:

```cpp
// From DayZ-Samples retexture example
ambient[] = {1.0, 1.0, 1.0, 1.0};
diffuse[] = {1.0, 1.0, 1.0, 1.0};
forcedDiffuse[] = {0.0, 0.0, 0.0, 0.0};
emmisive[] = {0.0, 0.0, 0.0, 0.0};
specular[] = {0.3, 0.3, 0.3, 1.0};
specularPower = 50;
PixelShaderID = "Super";
VertexShaderID = "Super";

class Stage1
{
    texture = "DZ_Samples\Test_ClothingRetexture\data\tshirt_nohq.paa";
    uvSource = "tex";
    class uvTransform
    {
        aside[] = {1.0, 0.0, 0.0};
        up[] = {0.0, 1.0, 0.0};
        dir[] = {0.0, 0.0, 0.0};
        pos[] = {0.0, 0.0, 0.0};
    };
};

class Stage2
{
    texture = "DZ_Samples\Test_ClothingRetexture\data\tshirt_co.paa";
    uvSource = "tex";
    class uvTransform
    {
        aside[] = {1.0, 0.0, 0.0};
        up[] = {0.0, 1.0, 0.0};
        dir[] = {0.0, 0.0, 0.0};
        pos[] = {0.0, 0.0, 0.0};
    };
};

class Stage3
{
    texture = "DZ_Samples\Test_ClothingRetexture\data\tshirt_smdi.paa";
    uvSource = "tex";
    class uvTransform
    {
        aside[] = {1.0, 0.0, 0.0};
        up[] = {0.0, 1.0, 0.0};
        dir[] = {0.0, 0.0, 0.0};
        pos[] = {0.0, 0.0, 0.0};
    };
};
```

### Material de Arma Metalica

Um cano de arma polido com alta resposta metalica:

```cpp
ambient[] = {1.0, 1.0, 1.0, 1.0};
diffuse[] = {1.0, 1.0, 1.0, 1.0};
forcedDiffuse[] = {0.0, 0.0, 0.0, 0.0};
emmisive[] = {0.0, 0.0, 0.0, 0.0};
specular[] = {0.9, 0.9, 0.9, 1.0};        // High specular for metal
specularPower = 150;                        // Tight, focused highlight
PixelShaderID = "Super";
VertexShaderID = "Super";

// ... Stage definitions with weapon textures ...
```

### Material Emissivo (Tela Brilhante)

Um material para a tela de um dispositivo que emite luz:

```cpp
ambient[] = {1.0, 1.0, 1.0, 1.0};
diffuse[] = {1.0, 1.0, 1.0, 1.0};
forcedDiffuse[] = {0.0, 0.0, 0.0, 0.0};
emmisive[] = {0.05, 0.3, 0.05, 1.0};      // Soft green glow
specular[] = {0.5, 0.5, 0.5, 1.0};
specularPower = 80;
PixelShaderID = "Super";
VertexShaderID = "Super";

// ... Stage definitions including _li emissive map in Stage7 ...
```

---

## Erros Comuns

### 1. Ordem de Stage Errada

**Sintoma:** Textura aparece embaralhada, normal map mostra como cor, cor mostra como relevos.
**Correcao:** Garanta que Stage1 = normal, Stage2 = diffuse, Stage3 = specular (para o shader Super).

### 2. Grafia Errada de `emmisive`

**Sintoma:** Emissivo nao funciona.
**Correcao:** Bohemia usa `emmisive` (m duplo, s unico). Usar a grafia correta em ingles `emissive` nao funciona. Essa e uma peculiaridade historica conhecida.

### 3. Incompatibilidade de Caminho de Textura

**Sintoma:** Modelo aparece com material cinza padrao ou magenta.
**Correcao:** Verifique se os caminhos de textura no RVMAT correspondem exatamente aos locais dos arquivos relativos a unidade P:. Caminhos usam barras invertidas. Confira capitalizacao -- alguns sistemas sao case-sensitive.

### 4. Atribuicao de RVMAT Ausente no P3D

**Sintoma:** Modelo renderiza sem material (cinza flat ou shader padrao).
**Correcao:** Abra o modelo no Object Builder, selecione faces e atribua o RVMAT via **Face Properties**.

### 5. Usando Shader Errado para Itens Transparentes

**Sintoma:** Textura transparente aparece opaca, ou toda a superficie desaparece.
**Correcao:** Use o shader `Glass`, `AlphaTest` ou `AlphaBlend` em vez de `Super` para superficies transparentes. Use texturas com sufixo `_ca` com canais alfa adequados.

---

## Boas Praticas

1. **Comece a partir de um exemplo funcional.** Copie um RVMAT dos DayZ-Samples ou de um item vanilla e modifique. Comecar do zero convida erros de digitacao.

2. **Mantenha materiais e texturas juntos.** Armazene o RVMAT no mesmo diretorio `data/` que suas texturas. Isso torna a relacao obvia e simplifica o gerenciamento de caminhos.

3. **Use o shader Super a menos que tenha um motivo para nao usar.** Ele lida com 95% dos casos de uso corretamente.

4. **Crie materiais de dano mesmo para itens simples.** Jogadores percebem quando itens nao degradam visualmente. No minimo, use os materiais de dano padrao vanilla para os niveis de saude mais baixos.

5. **Teste o specular no jogo, nao apenas no Object Builder.** A iluminacao do editor e a iluminacao no jogo produzem resultados muito diferentes. O que parece perfeito no Object Builder pode ser muito brilhante ou muito opaco sob a iluminacao dinamica do DayZ.

6. **Documente suas configuracoes de material.** Quando encontrar valores de specular/power que funcionam bem para um tipo de superficie, registre-os. Voce reutilizara essas configuracoes em muitos itens.

---

## Navegacao

| Anterior | Acima | Proximo |
|----------|-------|---------|
| [4.2 Modelos 3D](02-models.md) | [Parte 4: Formatos de Arquivo & DayZ Tools](01-textures.md) | [4.4 Audio](04-audio.md) |
