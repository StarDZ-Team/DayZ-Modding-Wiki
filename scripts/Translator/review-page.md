# Recibo da tradução manual completa de Variáveis e tipos

- Data: 2026-09-14.
- Despacho: `task_f9504eaec7e8` / `ctx_774e8c95feaf`.
- Revisão Git observada: `7dd37924983a71a7835c5a926b9cd7b284a84a3d` (workspace compartilhado, com alterações existentes).
- Fonte de verdade lida integralmente: `en/01-enforce-script/01-variables-types.md`.
- Página publicada lida integralmente para comparação: `pt/01-enforce-script/01-variables-types.md`.
- Entrega: `scripts/Translator/.translations/manual-preview/pt/01-enforce-script/01-variables-types.md`.

---

## Resultado

Tradução manual completa para português brasileiro das 760 linhas da fonte inglesa, incluindo as seções ausentes na página publicada de 336 linhas. Foram traduzidas as 162 linhas não vazias de títulos, prosa, listas e células de tabelas, preservando a organização da fonte. A página publicada termina dentro de um bloco de código e contém traduções indevidas de código e identificadores; a prévia foi reconstruída diretamente do EN, sem reutilizar esses exemplos corrompidos.

Todos os blocos cercados, incluindo Mermaid, comentários e exemplos deliberadamente incorretos, foram preservados literalmente conforme solicitado. Código inline, identificadores de APIs e destinos dos links permanecem iguais aos da fonte. Qualificadores e negações, inclusive as ressalvas sobre `auto`, referências fracas, conversões, condições e escopos, foram mantidos na tradução.

---

## Hashes SHA-256 dos bytes

| Arquivo | Linhas | Bytes | SHA-256 |
|---------|--------|-------|---------|
| Fonte EN | 760 | 26214 | `62ea48ed2b4d4ca84e379e596d824fd46ed4ababb7a3aa15f1bcb6cedc84e990` |
| PT publicada observada | 336 | 14020 | `3f35f7f7123527035ec21669708059fbee392138e43ca00658b6554953d9b2cf` |
| Prévia entregue | 760 | 29732 | `0c8098f70e3c611daabb84aa766656b779fe57261f0652b64e5bf966a5097d02` |

---

## Validação executada

Ambiente: `scripts/Translator/.env/Scripts/python.exe`, importando `translator` com a gravação de bytecode desativada. O Python padrão inicialmente falhou ao importar `markdown_it`; o ambiente existente do tradutor contém essa dependência e executou todas as verificações abaixo com código de saída zero. Nenhum modelo local foi carregado ou executado.

1. Conferência de cobertura: o conjunto de números das linhas traduzidas corresponde exatamente a todas as linhas não vazias fora de blocos cercados, excluindo apenas separadores horizontais e separadores de tabelas.
2. `translator.validar_estrutura(origem, destino)` executado antes da adição de âncoras: aprovado.
3. `translator.fixar_ancoras(origem, destino)` aplicado: 41 títulos com IDs baseados no EN.
4. Releitura da entrega e nova chamada de `validar_estrutura` após remover somente os IDs explícitos adicionados: aprovada.
5. Comparação ordenada dos 29 blocos cercados, incluindo cercas, conteúdo e quebras de linha, diretamente em bytes: igualdade exata.
6. Comparação ordenada dos 222 trechos de código inline fora dos blocos cercados, incluindo delimitadores e escapes: igualdade exata.
7. Comparação ordenada dos 28 destinos de links Markdown: igualdade exata.
8. Comparação de `translator.ancoras_titulos` da fonte e da entrega, incluindo posição de linha e ID: igualdade exata.
9. Leitura de revisão da tradução e conferência da seção final de resumo: conteúdo completo, sem truncamento.

---

## Limites e integração

Apenas a prévia e este recibo foram escritos por este despacho. A página PT publicada já aparece modificada no workspace; este worker não a alterou. Não houve edição do EN, tradutor, testes ou arquivos de outros workers, nem commit.

Esta entrega valida fidelidade de tradução e preservação estrutural; não constitui uma nova auditoria factual das afirmações do EN nem execução dos exemplos no jogo. Não foi executado build VitePress, pois a entrega é uma prévia aguardando revisão e aplicação pelo coordenador. A revisão independente do artefato e sua aplicação à página publicada continuam pendentes com o coordenador.

## Aceitação pelo coordenador

O coordenador reabriu toda a prosa da fonte e da entrega em pares, incluindo tabelas e ressalvas, e verificou novamente estrutura, 29 blocos, 222 inline, 28 destinos e 41 IDs. Aprovou a entrega `0c8098f70e3c611daabb84aa766656b779fe57261f0652b64e5bf966a5097d02` e a aplicou editorialmente à página PT após conferir os hashes da fonte e do destino anterior; os bytes anteriores foram preservados em backup. Essa reparação foi produzida por agente Codex e revisada pelo coordenador, não por uma geração Qwen concluída. A inspeção do navegador confirmou o título português, 41 IDs e Mermaid com 13 nós, sem erro de detecção de diagrama. O resultado do build integrado está no recibo validation.json.
