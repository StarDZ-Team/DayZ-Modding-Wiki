# Refinamento do tradutor — integração

Em 2026-09-14, foram corrigidos carregamento quantizado, proteção técnica, validação, recuperação e fluxo de prévia. O guia atual está em README.md; fontes e limites estão em STUDY.md. Os relatórios review-*.md registram achados, reparos e hashes de cada entrega.

## Resultado integrado

- Venv existente: Python 3.14.3, PyTorch 2.14.0+cu130, RTX 4060 Laptop. Credenciais existentes reutilizadas sem exposição.
- Qwen3-8B com revisão fixada é o padrão. Llama continua opcional; uma amostra solicitada em JA saiu em PT.
- Inventário: 93.118 candidatos lexicais, 3.875 fontes com caminhos, linhas e hashes. Não é certificação de APIs ou cobertura universal.
- Código/Mermaid, inline, destinos, HTML, diretivas, números e identificadores são protegidos. Termos ambíguos usam contexto; não se congela o inventário inteiro.
- Até duas tentativas por rejeição local, cache validado, checagem de idioma/estrutura/marcadores, IDs EN, prévia padrão, aplicação separada, backup, restore e lock.
- Página PT reparada por tradução editorial de agente Codex, revisada pelo coordenador contra a prosa EN pareada. Voltou de 336 para 760 linhas; preservou 29 blocos cercados, 222 inline, 28 destinos e 41 IDs. Backup anterior em .translations/backups/reported-page. Foi uma integração editorial separada, sem alterar manifesto para forçar aplicação.
- scripts/Translator foi excluído da coleta de páginas do VitePress; utilitário, relatórios e ambiente local não são páginas da wiki.

## Evidência e limites

O teste real Qwen passou nas verificações automáticas dos 11 idiomas, no snapshot e546ee83b11bfa2ac09e7f9239f290dcc3500c1e3d5a352bf5292a2c3d4be711. A extensão contextual posterior não integra esse snapshot. A saída espanhola conservou extends e outras amostras têm construções pouco naturais: isso não é aprovação semântica nativa. Recibo em smoke-results.json.

Duas tentativas anteriores de página PT completa foram recusadas: separador omitido e identificador omitido no terceiro trecho. Nenhuma publicou saída rejeitada. O retry limitado foi adicionado depois, com testes offline; não há recibo de sucesso automático da página completa. Logs e respostas estão preservados em .translations/.

Comentários e rótulos dentro de blocos permanecem na língua original. Detector e regras não comprovam fidelidade de sentido, variante regional ou ausência de toda palavra estrangeira. Prévias exigem revisão editorial. Uma rejeição segura não deve ser contornada removendo validações.

Resultados finais, hashes, versões e build são registrados em validation.json. O grafo existente cobre en/ e serviu de orientação; nenhuma página EN foi alterada neste escopo, portanto esse corpus não foi regenerado para incorporar uma tradução PT ou código Python. Build documental não valida exemplos no jogo.

## Coordenação e Git

Orca 1.4.199, run run_78eb761ccb70; somente agentes Codex. O identificador exato dos modelos herdados não foi exposto nos recibos. Workers concluídos são reutilizados ou liberados após aceitação. O coordenador reabriu fontes, código e entregas; relatórios históricos não aprovam alterações posteriores.

Mudanças alheias e arquivos previamente no índice foram preservados. O escopo de integração é scripts/Translator (sem venv/cache/temporários), a página PT e a exclusão da pasta do tradutor na configuração VitePress. Nenhum push foi solicitado ou realizado.
