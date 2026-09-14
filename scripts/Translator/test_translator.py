import io
import re
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import translator as t


class Tokenizer:
    eos_token_id = 0

    def encode(self, text, **kwargs):
        return list(text)


class ProtectionTests(unittest.TestCase):
    def test_changed_source_is_rejected_before_model_load_or_cache_write(self):
        with tempfile.TemporaryDirectory() as folder:
            cache = Path(folder) / 'cache'
            self.enterContext(patch.object(t, 'pipe', None))
            self.enterContext(patch.object(t, 'proteger_codigo', return_value=('Changed source.', {})))
            loader = self.enterContext(patch.object(t, 'carregar_modelo'))
            writer = self.enterContext(patch.object(t, 'salvar_traducao'))
            with self.assertRaisesRegex(RuntimeError, 'alterou a origem'):
                t.traduzir_conteudo_wiki('Original source.', 'Português', cache_dir=cache)
            loader.assert_not_called()
            writer.assert_not_called()
            self.assertEqual(list(Path(folder).iterdir()), [])

    def test_check_rejects_changed_source_without_loading_or_writing(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source_dir = root / 'en'
            source_dir.mkdir()
            page = source_dir / 'page.md'
            original = b'# Original\n\nSource text.\n'
            page.write_bytes(original)
            self.enterContext(patch.object(t, 'PASTA_ORIGEM_EN', source_dir))
            self.enterContext(patch.object(t, 'DIRETORIO_ATUAL', root))
            self.enterContext(patch.object(t, 'proteger_codigo', return_value=('Changed source.', {})))
            self.enterContext(patch.object(t.sys, 'argv', ['translator.py', '--check', '--languages', 'pt']))
            errors = self.enterContext(patch.object(t.sys, 'stderr', io.StringIO()))
            self.enterContext(patch.object(t.sys, 'stdout', io.StringIO()))
            loader = self.enterContext(patch.object(t, 'carregar_modelo'))
            writer = self.enterContext(patch.object(t, 'salvar_traducao'))
            self.assertEqual(t.main(), 1)
            self.assertIn('alterou a origem', errors.getvalue())
            self.assertIn(str(page), errors.getvalue())
            loader.assert_not_called()
            writer.assert_not_called()
            self.assertEqual(page.read_bytes(), original)
            self.assertEqual(set(root.rglob('*')), {source_dir, page})

    def test_language_keywords_in_explicit_context_and_ordinary_prose(self):
        source = 'Use out parameters, a sealed class, the return statement and the thread keyword. Go out and return later. An event starts here.'
        masked, saved = t.proteger_codigo(source)
        for phrase in ('out parameters', 'sealed class', 'return statement', 'thread keyword'):
            self.assertNotIn(phrase, masked)
        self.assertIn('Go out and return later. An event starts here.', masked)
        self.assertEqual(t.restaurar_codigo(masked, saved), source)

    def test_keyword_context_preserves_horizontal_whitespace(self):
        for separator in ('  ', '\t', ' \t '):
            for left, right, term in (('keyword', 'out', 'out'),
                                      ('operators', 'new', 'new'),
                                      ('sealed', 'classes', 'sealed'),
                                      ('parameters', 'out', 'out')):
                source = left + separator + right
                with self.subTest(source=source):
                    masked, saved = t.proteger_codigo(source)
                    self.assertEqual(list(saved.values()), [term])
                    self.assertIn(separator, masked)
                    self.assertEqual(t.restaurar_codigo(masked, saved), source)

    def test_keyword_context_does_not_cross_line_boundaries(self):
        for separator in ('\n', '\r\n', '\n\n', '\r\n\r\n'):
            for left, right in (('keywords', 'out'), ('out', 'parameters'),
                                ('operators', 'new'), ('sealed', 'classes'),
                                ('class', 'sealed'), ('return', '(later)'),
                                ('method', 'Set')):
                source = left + separator + right
                with self.subTest(source=source):
                    masked, saved = t.proteger_codigo(source)
                    self.assertEqual(saved, {})
                    self.assertEqual(masked, source)
                    self.assertEqual(t.restaurar_codigo(masked, saved), source)

    def test_common_words_are_translatable_beside_generic_descriptors(self):
        for source in ('Use this class for storage.', 'Use this type.',
                       'Use a new type.', 'Use the default parameter.',
                       'Check the return type.', 'The classes for storage.',
                       'Take the class out later.',
                       'Go out and return later. An event starts here.'):
            with self.subTest(source=source):
                masked, saved = t.proteger_codigo(source)
                self.assertEqual(saved, {})
                self.assertEqual(masked, source)

    def test_common_words_require_explicit_keyword_descriptors(self):
        for term in ('if', 'else', 'for', 'foreach', 'while', 'switch', 'case',
                     'default', 'break', 'continue', 'return', 'new', 'delete',
                     'this', 'do', 'try', 'catch', 'throw', 'interface',
                     'abstract', 'namespace', 'delegate'):
            for descriptor in ('keyword', 'keywords', 'statement', 'statements',
                               'operator', 'operators'):
                for source in (f'{term} {descriptor}', f'{descriptor} {term}'):
                    with self.subTest(source=source):
                        masked, saved = t.proteger_codigo(source)
                        self.assertEqual(list(saved.values()), [term])
                        self.assertEqual(t.restaurar_codigo(masked, saved), source)

    def test_parameter_class_and_method_keyword_contexts_remain_protected(self):
        for term, descriptor in (('out', 'parameters'), ('sealed', 'class'),
                                 ('sealed', 'classes'), ('thread', 'keywords'),
                                 ('event', 'methods')):
            for source in (f'{term} {descriptor}', f'{descriptor} {term}'):
                with self.subTest(source=source):
                    masked, saved = t.proteger_codigo(source)
                    self.assertEqual(list(saved.values()), [term])
                    self.assertEqual(t.restaurar_codigo(masked, saved), source)

    def test_round_trip_code_and_technical_terms(self):
        source = '# Example\n\nPlayerBase uses `modded class` and config.cpp.\n\n```mermaid\ngraph TD\nA[Class] --> B[Managed]\n```\n'
        masked, saved = t.proteger_codigo(source)
        for literal in ('PlayerBase', 'modded', 'config.cpp', 'graph TD', 'Managed'):
            self.assertNotIn(literal, masked)
        self.assertEqual(t.restaurar_codigo(masked, saved), source)

    def test_nested_fences_crlf_and_inline_backticks(self):
        source = 'Text ``a ` b``\r\n\r\n````md\r\n```c\r\nint a;\r\n```\r\n````\r\n\n~~~xml\n<x/>\n~~~\n'
        masked, saved = t.proteger_codigo(source)
        self.assertEqual(t.restaurar_codigo(masked, saved), source)

    def test_missing_duplicate_changed_reordered_markers_rejected(self):
        masked, saved = t.proteger_codigo('`int` then `float`')
        first, second = list(saved)
        for broken in (masked.replace(first, ''), masked + first, masked.replace(first, first.lower()), masked.replace(first, 'TEMP').replace(second, first).replace('TEMP', second)):
            with self.assertRaises(RuntimeError):
                t.restaurar_codigo(broken, saved)

    def test_block_moved_into_prose_rejected(self):
        masked, saved = t.proteger_codigo('```c\nint x;\n```\n')
        with self.assertRaises(RuntimeError):
            t.restaurar_codigo('Example ' + masked, saved)

    def test_ambiguous_prose_and_identifier_boundaries(self):
        source = 'Set a map on the table. A class can contain a PlayerBase. falsehood is prose.'
        masked, saved = t.proteger_codigo(source)
        self.assertIn('map on the table', masked)
        self.assertIn('A class can', masked)
        self.assertIn('falsehood', masked)
        self.assertNotIn('PlayerBase', masked)
        self.assertEqual(t.restaurar_codigo(masked, saved), source)

    def test_links_html_paths_frontmatter_and_directives(self):
        source = '---\ntitle: API\n---\n\n[Read](../en/file.md#anchor)\n<Widget name="Inventory">text</Widget>\n::: warning\nUse P:\\mods\\config.cpp\n:::\n'
        masked, saved = t.proteger_codigo(source)
        self.assertIn('[Read]', masked)
        for literal in ('../en/file.md', 'Widget', '::: warning', 'P:\\mods'):
            self.assertNotIn(literal, masked)
        self.assertEqual(t.restaurar_codigo(masked, saved), source)

    def test_glossary_symbol_outside_backticks(self):
        for term in ('JsonFileLoader', 'EEInit', 'requiredAddons', 'ScriptRPC', 'ScriptInvoker'):
            masked, saved = t.proteger_codigo(f'Use {term} here.')
            self.assertNotIn(term, masked)
            self.assertIn(term, saved.values())

    def test_unclosed_source_block_rejected(self):
        with self.assertRaises(ValueError):
            t.proteger_codigo('```c\nint x;')

    def test_chunks_preserve_source(self):
        source = ('A paragraph.\n\n' * 15) + 'Last line.'
        chunks = t.dividir_texto(source, Tokenizer(), limite=50)
        self.assertEqual(''.join(chunks), source)
        self.assertTrue(all(len(chunk) <= 50 for chunk in chunks))
        with self.assertRaises(RuntimeError):
            t.dividir_texto('x' * 51, Tokenizer(), limite=50)

    def test_incomplete_generation_rejected(self):
        fake = SimpleNamespace(tokenizer=Tokenizer())
        class Pipeline:
            tokenizer = fake.tokenizer
            def __call__(self, *args, **kwargs):
                return [{'generated_text': 'Truncated translation'}]
        with patch.object(t, 'pipe', Pipeline()):
            with self.assertRaisesRegex(RuntimeError, 'incompleta'):
                t.traduzir_conteudo_wiki('# Heading\n\nText.', 'Português')

    def test_pipeline_round_trip_without_sending_code(self):
        class Pipeline:
            tokenizer = Tokenizer()
            def __call__(self, messages, **kwargs):
                content = messages[-1]['content'].split('\n\n', 1)[1]
                self_test.assertNotIn('graph TD', content)
                return [{'generated_text': content.replace('Hello', 'Olá')}]
        self_test = self
        source = '# Hello\n\n```mermaid\ngraph TD\nA --> B\n```\n'
        with patch.object(t, 'pipe', Pipeline()):
            self.assertEqual(t.traduzir_conteudo_wiki(source, 'Português'), source.replace('# Hello', '# Olá {#hello}'))

    def test_source_heading_anchors_survive_translation_and_duplicates(self):
        original = '# Guide\n\n## Use `PlayerBase`\n\n## Use `PlayerBase`\n'
        translated = '# Guia\n\n## Use `PlayerBase`\n\n## Use `PlayerBase`\n'
        self.assertEqual(t.fixar_ancoras(original, translated), '# Guia {#guide}\n\n## Use `PlayerBase` {#use-playerbase}\n\n## Use `PlayerBase` {#use-playerbase-1}\n')

    def test_atomic_failure_preserves_existing_file(self):
        with tempfile.TemporaryDirectory() as folder:
            destination = Path(folder) / 'page.md'
            destination.write_text('original', encoding='utf-8')
            with patch.object(t.os, 'replace', side_effect=OSError('failure')):
                with self.assertRaises(OSError):
                    t.salvar_traducao(destination, 'new')
            self.assertEqual(destination.read_text(encoding='utf-8'), 'original')
            self.assertEqual(list(Path(folder).iterdir()), [destination])


if __name__ == '__main__':
    unittest.main()
