# Chapter 4.1: Textures (.paa, .edds, .tga)

[Home](../../README.md) | **Textures** | [Next: 3D Models >>](02-models.md)

---

## Introducao

Toda superficie que voce ve no DayZ -- skins de armas, roupas, terreno, icones de UI -- e definida por arquivos de textura. O motor do jogo usa um formato compactado proprietario chamado **PAA** em tempo de execucao, mas durante o desenvolvimento voce trabalha com varios formatos de origem que sao convertidos durante o processo de build. Entender esses formatos, as convencoes de nomenclatura por sufixo que dizem ao motor como interpretar cada textura, os requisitos de resolucao e as regras de canal alfa e fundamental para criar conteudo visual para mods de DayZ.

Este capitulo cobre todos os formatos de textura que voce encontrara, o sistema de nomenclatura por sufixos que informa ao motor como interpretar cada textura, requisitos de resolucao e canal alfa, e o fluxo de trabalho pratico para converter entre formatos.

---

## Sumario

- [Visao Geral dos Formatos de Textura](#visao-geral-dos-formatos-de-textura)
- [Formato PAA](#formato-paa)
- [Formato EDDS](#formato-edds)
- [Formato TGA](#formato-tga)
- [Formato PNG](#formato-png)
- [Convencoes de Nomenclatura de Textura](#convencoes-de-nomenclatura-de-textura)
- [Requisitos de Resolucao](#requisitos-de-resolucao)
- [Suporte a Canal Alfa](#suporte-a-canal-alfa)
- [Convertendo Entre Formatos](#convertendo-entre-formatos)
- [Qualidade de Textura e Compressao](#qualidade-de-textura-e-compressao)
- [Exemplos Reais](#exemplos-reais)
- [Erros Comuns](#erros-comuns)
- [Boas Praticas](#boas-praticas)

---

## Visao Geral dos Formatos de Textura

O DayZ usa quatro formatos de textura em diferentes estagios do pipeline de desenvolvimento:

| Formato | Extensao | Funcao | Suporte a Alfa | Usado Em |
|---------|----------|--------|----------------|----------|
| **PAA** | `.paa` | Formato de execucao do jogo (compactado) | Sim | Build final, distribuido em PBOs |
| **EDDS** | `.edds` | Variante DDS para editor/intermediario | Sim | Preview no Object Builder, converte automaticamente |
| **TGA** | `.tga` | Arte-fonte nao compactada | Sim | Workspace do artista, exportacao do Photoshop/GIMP |
| **PNG** | `.png` | Formato de origem portatil | Sim | Texturas de UI, ferramentas externas |

O fluxo de trabalho geral e: **Origem (TGA/PNG) --> Conversao pelo DayZ Tools --> PAA (pronto para o jogo)**.

---

## Formato PAA

**PAA** (PAcked Arma) e o formato de textura compactado nativo usado pelo motor Enfusion em tempo de execucao. Toda textura distribuida em um PBO deve estar no formato PAA (ou sera convertida para ele durante a binarizacao).

### Caracteristicas

- **Compactado:** Usa compressao DXT1, DXT5 ou ARGB8888 internamente, dependendo da presenca do canal alfa e das configuracoes de qualidade.
- **Com mipmaps:** Arquivos PAA contem uma cadeia completa de mipmaps, gerada automaticamente durante a conversao. Isso e critico para o desempenho de renderizacao -- o motor seleciona o nivel de mip apropriado com base na distancia.
- **Dimensoes em potencia de dois:** O motor exige que texturas PAA tenham dimensoes que sejam potencias de 2 (256, 512, 1024, 2048, 4096).
- **Somente leitura em tempo de execucao:** O motor carrega arquivos PAA diretamente dos PBOs. Voce nunca edita um arquivo PAA -- voce edita a origem e reconverte.

### Tipos de Compressao Interna

| Tipo | Alfa | Qualidade | Caso de Uso |
|------|------|-----------|-------------|
| **DXT1** | Nao (1-bit) | Boa, taxa 6:1 | Texturas opacas, terreno |
| **DXT5** | Total 8-bit | Boa, taxa 4:1 | Texturas com alfa suave (vidro, folhagem) |
| **ARGB4444** | Total 4-bit | Media | Texturas de UI, icones pequenos |
| **ARGB8888** | Total 8-bit | Sem perda | Debug, qualidade maxima (tamanho de arquivo grande) |
| **AI88** | Escala de cinza + alfa | Boa | Normal maps, mascaras em escala de cinza |

### Quando Voce Encontrara Arquivos PAA

- Dentro dos dados vanilla descompactados do jogo (diretorio `dta/` e PBOs de addon)
- Como saida da conversao do TexView2
- Como saida do Binarize ao processar texturas de origem
- No PBO final do seu mod apos o build

---

## Formato EDDS

**EDDS** e um formato de textura intermediario usado principalmente pelo **Object Builder** do DayZ e pelas ferramentas do editor. E essencialmente uma variante do formato padrao DirectDraw Surface (DDS) com metadados especificos do motor.

### Caracteristicas

- **Formato de preview:** O Object Builder pode exibir texturas EDDS diretamente, tornando-as uteis durante a criacao de modelos.
- **Converte automaticamente para PAA:** Quando voce executa o Binarize ou AddonBuilder (sem `-packonly`), arquivos EDDS na sua arvore de origem sao automaticamente convertidos para PAA.
- **Maior que PAA:** Arquivos EDDS nao sao otimizados para distribuicao -- existem por conveniencia do editor.
- **Formato do DayZ-Samples:** Os exemplos oficiais DayZ-Samples fornecidos pela Bohemia usam texturas EDDS extensivamente.

### Fluxo de Trabalho com EDDS

```
Artista cria TGA/PNG de origem
    --> Plugin DDS do Photoshop exporta EDDS para preview
        --> Object Builder exibe EDDS no modelo
            --> Binarize converte EDDS para PAA no PBO
```

> **Dica:** Voce pode pular completamente o EDDS se preferir. Converta suas texturas de origem diretamente para PAA usando o TexView2 e referencie os caminhos PAA nos seus materiais. EDDS e uma conveniencia, nao um requisito.

---

## Formato TGA

**TGA** (Truevision TGA / Targa) e o formato de origem nao compactado tradicional para trabalho com texturas do DayZ. Muitas texturas vanilla do DayZ foram originalmente criadas como arquivos TGA.

### Caracteristicas

- **Nao compactado:** Sem perda de qualidade, profundidade de cor total (24-bit ou 32-bit com alfa).
- **Tamanhos de arquivo grandes:** Um TGA 2048x2048 com alfa tem aproximadamente 16 MB.
- **Alfa em canal dedicado:** TGA suporta um canal alfa de 8 bits (TGA 32-bit), que mapeia diretamente para transparencia no PAA.
- **Compativel com TexView2:** O TexView2 pode abrir arquivos TGA diretamente e converte-los para PAA.

### Quando Usar TGA

- Como seu arquivo-mestre de origem para texturas que voce cria do zero.
- Ao exportar do Substance Painter ou Photoshop para DayZ.
- Quando a documentacao do DayZ-Samples ou tutoriais da comunidade especificam TGA como formato de origem.

### Configuracoes de Exportacao TGA

Ao exportar TGA para conversao no DayZ:

- **Profundidade de bits:** 32-bit (se alfa for necessario) ou 24-bit (texturas opacas)
- **Compressao:** Nenhuma (nao compactado)
- **Orientacao:** Origem no canto inferior esquerdo (orientacao padrao do TGA)
- **Resolucao:** Deve ser potencia de 2 (veja [Requisitos de Resolucao](#requisitos-de-resolucao))

---

## Formato PNG

**PNG** (Portable Network Graphics) e amplamente suportado e pode ser usado como formato de origem alternativo, particularmente para texturas de UI.

### Caracteristicas

- **Compressao sem perda:** Menor que TGA, mas mantem qualidade total.
- **Canal alfa completo:** PNG 32-bit suporta alfa de 8 bits.
- **Compativel com TexView2:** O TexView2 pode abrir e converter PNG para PAA.
- **Ideal para UI:** Muitos imagesets e icones de UI em mods usam PNG como formato de origem.

### Quando Usar PNG

- **Texturas e icones de UI:** PNG e a escolha pratica para imagesets e elementos de HUD.
- **Retexturas simples:** Quando voce precisa apenas de um mapa de cor/diffuse sem alfa complexo.
- **Fluxos de trabalho multi-ferramenta:** PNG e universalmente suportado entre editores de imagem, ferramentas web e scripts.

> **Nota:** PNG nao e um formato de origem oficial da Bohemia -- eles preferem TGA. Porem, as ferramentas de conversao lidam com PNG sem problemas e muitos modders o utilizam com sucesso.

---

## Convencoes de Nomenclatura de Textura

O DayZ usa um sistema rigoroso de sufixos para identificar a funcao de cada textura. O motor e os materiais referenciam texturas pelo nome do arquivo, e o sufixo informa tanto ao motor quanto a outros modders que tipo de dados a textura contem.

### Sufixos Obrigatorios

| Sufixo | Nome Completo | Proposito | Formato Tipico |
|--------|---------------|-----------|----------------|
| `_co` | **Color / Diffuse** | A cor base (albedo) de uma superficie | RGB, alfa opcional |
| `_nohq` | **Normal Map (High Quality)** | Normais de detalhe de superficie, define relevos e sulcos | RGB (normal em espaco tangente) |
| `_smdi` | **Specular / Metallic / Detail Index** | Controla brilho e propriedades metalicas | Canais RGB codificam dados separados |
| `_ca` | **Color with Alpha** | Textura de cor onde o canal alfa carrega dados significativos (transparencia, mascara) | RGBA |
| `_as` | **Ambient Shadow** | Oclusao ambiental / shadow bake | Escala de cinza |
| `_mc` | **Macro** | Variacao de cor em larga escala visivel a distancia | RGB |
| `_li` | **Light / Emissive** | Mapa de auto-iluminacao (partes que brilham) | RGB |
| `_no` | **Normal Map (Standard)** | Variante de normal map de qualidade inferior | RGB |
| `_mca` | **Macro with Alpha** | Textura macro com canal alfa | RGBA |
| `_de` | **Detail** | Textura de detalhe com repeticao para variacao de superficie em close | RGB |

### Convencao de Nomenclatura na Pratica

Um unico item tipicamente tem multiplas texturas, todas compartilhando um nome base:

```
data/
  my_rifle_co.paa          <-- Cor base (o que voce ve)
  my_rifle_nohq.paa        <-- Normal map (relevos da superficie)
  my_rifle_smdi.paa         <-- Specular/metallic (brilho)
  my_rifle_as.paa           <-- Ambient shadow (AO baked)
  my_rifle_ca.paa           <-- Cor com alfa (se transparencia for necessaria)
```

### Os Canais do _smdi

A textura specular/metallic/detail empacota tres fluxos de dados em uma unica imagem RGB:

| Canal | Dados | Faixa | Efeito |
|-------|-------|-------|--------|
| **R** | Metalico | 0-255 | 0 = nao-metal, 255 = totalmente metalico |
| **G** | Rugosidade (specular invertido) | 0-255 | 0 = rugoso/fosco, 255 = liso/brilhante |
| **B** | Indice de detalhe / AO | 0-255 | Repeticao de detalhe ou oclusao ambiental |

### Os Canais do _nohq

Normal maps no DayZ usam codificacao em espaco tangente:

| Canal | Dados |
|-------|-------|
| **R** | Normal do eixo X (esquerda-direita) |
| **G** | Normal do eixo Y (cima-baixo) |
| **B** | Normal do eixo Z (em direcao ao observador) |
| **A** | Potencia specular (opcional, depende do material) |

---

## Requisitos de Resolucao

O motor Enfusion exige que todas as texturas tenham **dimensoes em potencia de dois**. Tanto a largura quanto a altura devem ser independentemente uma potencia de 2, mas nao precisam ser iguais (texturas nao-quadradas sao validas).

### Dimensoes Validas

| Tamanho | Uso Tipico |
|---------|------------|
| **64x64** | Icones minusculos, elementos de UI |
| **128x128** | Icones pequenos, miniaturas de inventario |
| **256x256** | Paineis de UI, texturas de itens pequenos |
| **512x512** | Texturas de itens padrao, roupas |
| **1024x1024** | Armas, roupas detalhadas, pecas de veiculos |
| **2048x2048** | Armas de alto detalhe, modelos de personagens |
| **4096x4096** | Texturas de terreno, texturas de veiculos grandes |

### Texturas Nao-Quadradas

Texturas nao-quadradas com potencia de dois sao validas:

```
256x512    -- Valido (ambos sao potencias de 2)
512x1024   -- Valido
1024x2048  -- Valido
300x512    -- INVALIDO (300 nao e potencia de 2)
```

### Diretrizes de Resolucao

- **Armas:** 2048x2048 para o corpo principal, 1024x1024 para acessorios.
- **Roupas:** 1024x1024 ou 2048x2048 dependendo da area de cobertura da superficie.
- **Icones de UI:** 128x128 ou 256x256 para icones de inventario, 64x64 para elementos de HUD.
- **Terreno:** 4096x4096 para mapas de satelite, 512x512 ou 1024x1024 para tiles de material.
- **Normal maps:** Mesma resolucao da textura de cor correspondente.
- **Mapas SMDI:** Mesma resolucao da textura de cor correspondente.

> **Aviso:** Se uma textura tiver dimensoes que nao sejam potencia de dois, o motor ira recusar carrega-la ou exibir uma textura de erro magenta. O TexView2 mostrara um aviso durante a conversao.

---

## Suporte a Canal Alfa

O canal alfa em uma textura carrega dados adicionais alem da cor. Como ele e interpretado depende do sufixo da textura e do shader do material.

### Funcoes do Canal Alfa

| Sufixo | Interpretacao do Alfa |
|--------|-----------------------|
| `_co` | Geralmente nao usado; se presente, pode definir transparencia para materiais simples |
| `_ca` | Mascara de transparencia (0 = totalmente transparente, 255 = totalmente opaco) |
| `_nohq` | Mapa de potencia specular (maior = reflexo specular mais nitido) |
| `_smdi` | Geralmente nao usado |
| `_li` | Mascara de intensidade emissiva |

### Criando Texturas com Alfa

No seu editor de imagem (Photoshop, GIMP, Krita):

1. Crie o conteudo RGB normalmente.
2. Adicione um canal alfa.
3. Pinte branco (255) onde voce quer opacidade/efeito total, preto (0) onde nao quer nada.
4. Exporte como TGA 32-bit ou PNG.
5. Converta para PAA usando o TexView2 -- ele detectara o canal alfa automaticamente.

### Verificando Alfa no TexView2

Abra o PAA no TexView2 e use os botoes de exibicao de canal:

- **RGBA** -- Mostra o composto final
- **RGB** -- Mostra apenas a cor
- **A** -- Mostra apenas o canal alfa (branco = opaco, preto = transparente)

---

## Convertendo Entre Formatos

### TexView2 (Ferramenta Principal)

**TexView2** esta incluido no DayZ Tools e e o utilitario padrao de conversao de texturas.

**Abrindo um arquivo:**
1. Abra o TexView2 a partir do DayZ Tools ou diretamente de `DayZ Tools\Bin\TexView2\TexView2.exe`.
2. Abra seu arquivo de origem (TGA, PNG ou EDDS).
3. Verifique se a imagem parece correta e confira as dimensoes.

**Convertendo para PAA:**
1. Abra a textura de origem no TexView2.
2. Va em **File --> Save As**.
3. Selecione **PAA** como formato de saida.
4. Escolha o tipo de compressao:
   - **DXT1** para texturas opacas (sem necessidade de alfa)
   - **DXT5** para texturas com transparencia alfa
   - **ARGB4444** para texturas de UI pequenas onde o tamanho do arquivo importa
5. Clique em **Save**.

**Conversao em lote via linha de comando:**

```bash
# Convert a single TGA to PAA
"P:\DayZ Tools\Bin\TexView2\TexView2.exe" -i "source.tga" -o "output.paa"

# TexView2 will auto-select compression based on alpha channel presence
```

### Binarize (Automatizado)

Quando o Binarize processa o diretorio de origem do seu mod, ele converte automaticamente todos os formatos de textura reconhecidos (TGA, PNG, EDDS) para PAA. Isso acontece como parte do pipeline do AddonBuilder.

**Fluxo de conversao do Binarize:**
```
source/mod_name/data/texture_co.tga
    --> Binarize detects TGA
        --> Converts to PAA with automatic compression selection
            --> Output: build/mod_name/data/texture_co.paa
```

### Tabela de Conversao Manual

| De | Para | Ferramenta | Notas |
|----|------|------------|-------|
| TGA --> PAA | TexView2 | Fluxo de trabalho padrao |
| PNG --> PAA | TexView2 | Funciona identicamente ao TGA |
| EDDS --> PAA | TexView2 ou Binarize | Automatico durante o build |
| PAA --> TGA | TexView2 (Save As TGA) | Para editar texturas existentes |
| PAA --> PNG | TexView2 (Save As PNG) | Para extrair para formato portatil |
| PSD --> TGA/PNG | Photoshop/GIMP | Exporte do editor, depois converta |

---

## Qualidade de Textura e Compressao

### Selecao do Tipo de Compressao

| Cenario | Compressao Recomendada | Motivo |
|---------|------------------------|--------|
| Diffuse opaco (`_co`) | DXT1 | Melhor taxa, sem necessidade de alfa |
| Diffuse transparente (`_ca`) | DXT5 | Suporte completo a alfa |
| Normal maps (`_nohq`) | DXT5 | Canal alfa carrega potencia specular |
| Mapas specular (`_smdi`) | DXT1 | Geralmente opaco, apenas canais RGB |
| Texturas de UI | ARGB4444 ou DXT5 | Tamanho pequeno, bordas nitidas |
| Mapas emissivos (`_li`) | DXT1 ou DXT5 | DXT5 se o alfa carrega intensidade |

### Qualidade vs. Tamanho do Arquivo

```
Format        2048x2048 approx. size
-----------------------------------------
ARGB8888      16.0 MB    (uncompressed)
DXT5           5.3 MB    (4:1 compression)
DXT1           2.7 MB    (6:1 compression)
ARGB4444       8.0 MB    (2:1 compression)
```

### Configuracoes de Qualidade no Jogo

Os jogadores podem ajustar a qualidade da textura nas configuracoes de video do DayZ. O motor seleciona niveis de mip mais baixos quando a qualidade e reduzida, entao suas texturas parecerão progressivamente mais borradas em configuracoes mais baixas. Isso e automatico -- voce nao precisa criar niveis de qualidade separados.

---

## Exemplos Reais

### Conjunto de Texturas de Arma

Um mod de arma tipico contem estes arquivos de textura:

```
MyWeapons/data/weapons/m4a1/
  my_weapon_co.paa           <-- 2048x2048, DXT1, base color
  my_weapon_nohq.paa         <-- 2048x2048, DXT5, normal map
  my_weapon_smdi.paa          <-- 2048x2048, DXT1, specular/metallic
  my_weapon_as.paa            <-- 1024x1024, DXT1, ambient shadow
```

O arquivo de material (`.rvmat`) referencia essas texturas e as atribui aos estagios do shader.

### Textura de UI (Origem do Imageset)

```
MyFramework/data/gui/icons/
  my_icons_co.paa           <-- 512x512, ARGB4444, sprite atlas
```

Texturas de UI sao frequentemente empacotadas em um unico atlas (imageset) e referenciadas por nome nos arquivos de layout. Compressao ARGB4444 e comum para UI porque preserva bordas nitidas mantendo tamanhos de arquivo pequenos.

### Texturas de Terreno

```
terrain/
  grass_green_co.paa         <-- 1024x1024, DXT1, tiling color
  grass_green_nohq.paa       <-- 1024x1024, DXT5, tiling normal
  grass_green_smdi.paa        <-- 1024x1024, DXT1, tiling specular
  grass_green_mc.paa          <-- 512x512, DXT1, macro variation
  grass_green_de.paa          <-- 512x512, DXT1, detail tiling
```

Texturas de terreno se repetem pela paisagem. A textura macro `_mc` adiciona variacao de cor em larga escala para evitar repeticao.

---

## Erros Comuns

### 1. Dimensoes Nao Potencia de Dois

**Sintoma:** Textura magenta no jogo, avisos no TexView2.
**Correcao:** Redimensione sua origem para a potencia de 2 mais proxima antes de converter.

### 2. Sufixo Ausente

**Sintoma:** O material nao encontra a textura, ou ela renderiza incorretamente.
**Correcao:** Sempre inclua o sufixo adequado (`_co`, `_nohq`, etc.) no nome do arquivo.

### 3. Compressao Errada para Alfa

**Sintoma:** Transparencia parece blocada ou binaria (ligado/desligado sem gradiente).
**Correcao:** Use DXT5 em vez de DXT1 para texturas que precisam de gradientes alfa suaves.

### 4. Esquecendo Mipmaps

**Sintoma:** Textura fica bem de perto, mas cintila/brilha a distancia.
**Correcao:** Arquivos PAA gerados pelo TexView2 incluem mipmaps automaticamente. Se voce estiver usando uma ferramenta nao padrao, certifique-se de que a geracao de mipmaps esta habilitada.

### 5. Formato Incorreto do Normal Map

**Sintoma:** Iluminacao no modelo parece invertida ou achatada.
**Correcao:** Certifique-se de que seu normal map esta no formato de espaco tangente com convencao de eixo Y estilo DirectX (canal verde: para cima = mais claro). Algumas ferramentas exportam estilo OpenGL (Y invertido) -- voce precisa inverter o canal verde.

### 6. Incompatibilidade de Caminho Apos Conversao

**Sintoma:** Modelo ou material mostra magenta porque referencia um caminho `.tga`, mas o PBO contem `.paa`.
**Correcao:** Materiais devem referenciar o caminho final `.paa`. O Binarize lida com o remapeamento de caminhos automaticamente, mas se voce empacotar com `-packonly` (sem binarizacao), voce deve garantir que os caminhos combinem exatamente.

---

## Boas Praticas

1. **Mantenha os arquivos de origem no controle de versao.** Armazene os mestres TGA/PNG junto com seu mod. Os arquivos PAA sao saida gerada -- as origens sao o que importa.

2. **Combine a resolucao com a importancia.** Um rifle que o jogador olha por horas merece 2048x2048. Uma lata de feijao no fundo de uma prateleira pode usar 512x512.

3. **Sempre forneca um normal map.** Mesmo um normal map plano (128, 128, 255 em preenchimento solido) e melhor do que nenhum -- normal maps ausentes causam erros de material.

4. **Nomeie consistentemente.** Um nome base, multiplos sufixos: `myitem_co.paa`, `myitem_nohq.paa`, `myitem_smdi.paa`. Nunca misture esquemas de nomenclatura.

5. **Faca preview no TexView2 antes do build.** Abra sua saida PAA e verifique se parece correta. Confira cada canal individualmente.

6. **Use DXT1 por padrao, DXT5 somente quando alfa for necessario.** DXT1 tem metade do tamanho do arquivo do DXT5 e parece identico para texturas opacas.

7. **Teste em configuracoes de qualidade baixa.** O que fica otimo em Ultra pode ficar ilegivel em Low porque o motor descarta niveis de mip agressivamente.

---

## Navegacao

| Anterior | Acima | Proximo |
|----------|-------|---------|
| [Parte 3: Sistema GUI](../03-gui-system/07-styles-fonts.md) | [Parte 4: Formatos de Arquivo & DayZ Tools](../04-file-formats/01-textures.md) | [4.2 Modelos 3D](02-models.md) |
