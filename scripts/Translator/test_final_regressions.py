"""Independent final contracts; temporary files and fake generation, never GPU."""
import hashlib
import json
from pathlib import Path
import re
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

import translator as t
import test_review_regressions as support


class RetryPipeline:
    tokenizer = support.CharacterTokenizer()

    def __init__(self, transforms):
        self.transforms = transforms
        self.messages = []
        self.generation_config = SimpleNamespace(max_length=20)

    def __call__(self, messages, **kwargs):
        self.messages.append(messages)
        content = messages[-1]['content'].split('\n\n', 1)[1]
        return [{'generated_text': self.transforms[len(self.messages) - 1](content)}]


class RetryContracts(support.OfflineCase):
    def test_second_attempt_recovers_each_validation_failure_and_uses_seed43(self):
        invalid = [lambda s: re.sub(r'WIKIEND[A-F0-9]+', '', s),
                   lambda s: s.replace('# Hello', 'Hello'),
                   lambda s: re.sub(r'WIKICODE[A-F0-9]+X\d+X', '', s, count=1)]
        source = '# Hello\n\nInspect `PlayerBase`.\n'
        for corrupt in invalid:
            with self.subTest(corrupt=corrupt), tempfile.TemporaryDirectory() as folder:
                pipeline = RetryPipeline([corrupt, lambda s: s.replace('Hello', 'Olá')])
                seed = Mock()
                with patch.object(t, 'pipe', pipeline), patch.dict(sys.modules, {'transformers': SimpleNamespace(set_seed=seed)}):
                    output = t.traduzir_conteudo_wiki(source, 'Português', cache_dir=Path(folder))
                self.assertEqual(output, source.replace('# Hello', '# Olá {#hello}'))
                self.assertEqual([call.args[0] for call in seed.call_args_list], [42, 43])
                self.assertEqual(len(pipeline.messages), 2)
                self.assertEqual(pipeline.messages[0][-1], pipeline.messages[1][-1])
                self.assertIn('failed validation', pipeline.messages[1][0]['content'])
                self.assertIn('Regenerate the entire original section', pipeline.messages[1][0]['content'])
                cached = json.loads(next(Path(folder).glob('*.json')).read_text(encoding='utf-8'))
                self.assertIn('Olá', cached['output'])
                self.assertIn('WIKICODE', cached['output'])

    def test_two_rejections_keep_both_raw_responses_and_leave_no_cache(self):
        pipeline = RetryPipeline([lambda s: 'Missing end', lambda s: re.sub(r'WIKICODE[A-F0-9]+X\d+X', '', s, count=1)])
        with tempfile.TemporaryDirectory() as folder, patch.object(t, 'pipe', pipeline), patch.dict(sys.modules, {'transformers': SimpleNamespace(set_seed=Mock())}):
            with self.assertRaises(t.FalhaTraducao) as raised:
                t.traduzir_conteudo_wiki('Hello `PlayerBase`.\n', 'Português', cache_dir=Path(folder))
            self.assertEqual(list(Path(folder).iterdir()), [])
        details = raised.exception.detalhes
        self.assertEqual(details['attempt'], 2)
        self.assertEqual([r['attempt'] for r in details['attempts']], [1, 2])
        self.assertEqual([r['seed'] for r in details['attempts']], [42, 43])
        self.assertEqual(details['attempts'][0]['response'], 'Missing end')
        self.assertIn('marcador final', details['attempts'][0]['error'])
        self.assertIn('marcadores protegidos', details['attempts'][1]['error'])
        self.assertEqual(len(pipeline.messages), 2)

    def test_pipeline_runtime_error_is_not_retried(self):
        pipeline = Mock(tokenizer=support.CharacterTokenizer(), side_effect=RuntimeError('CUDA out of memory'))
        with patch.object(t, 'pipe', pipeline), patch.dict(sys.modules, {'transformers': SimpleNamespace(set_seed=Mock())}):
            with self.assertRaisesRegex(RuntimeError, 'CUDA out of memory'):
                self.translate('Hello `PlayerBase`.\n')
        self.assertEqual(pipeline.call_count, 1)

    def test_loading_failure_is_not_retried(self):
        with patch.object(t, 'pipe', None), patch.object(t, 'carregar_modelo', side_effect=RuntimeError('load failed')) as loader:
            with self.assertRaisesRegex(RuntimeError, 'load failed'):
                self.translate('Hello `PlayerBase`.\n')
        loader.assert_called_once()


class CacheContracts(support.OfflineCase):
    def test_absent_chunk_regenerates_and_valid_chunk_reuses(self):
        with tempfile.TemporaryDirectory() as folder:
            cache = Path(folder)
            source = 'Hello `PlayerBase`.\n'
            expected = t.traduzir_conteudo_wiki(source, 'Português', cache_dir=cache)
            self.assertEqual(len(self.pipeline.inputs), 1)
            self.assertEqual(t.traduzir_conteudo_wiki(source, 'Português', cache_dir=cache), expected)
            self.assertEqual(len(self.pipeline.inputs), 1)
            next(cache.glob('*.json')).unlink()
            self.assertEqual(t.traduzir_conteudo_wiki(source, 'Português', cache_dir=cache), expected)
            self.assertEqual(len(self.pipeline.inputs), 2)

    def test_corrupt_chunk_is_regenerated(self):
        corruptions = [b'{', b'{}', b'null', b'[]', b'{"sha256":"x","output":null}',
                       b'{"sha256":"x","output":123}', b'\xff\xfe']
        for corruption in corruptions:
            with self.subTest(corruption=corruption), tempfile.TemporaryDirectory() as folder:
                cache = Path(folder)
                source = 'Hello `PlayerBase`.\n'
                expected = t.traduzir_conteudo_wiki(source, 'Português', cache_dir=cache)
                next(cache.glob('*.json')).write_bytes(corruption)
                before = len(self.pipeline.inputs)
                self.assertEqual(t.traduzir_conteudo_wiki(source, 'Português', cache_dir=cache), expected)
                self.assertEqual(len(self.pipeline.inputs), before + 1)

    def test_hash_valid_chunk_with_missing_marker_is_regenerated(self):
        with tempfile.TemporaryDirectory() as folder:
            cache = Path(folder)
            source = 'Hello `PlayerBase`.\n'
            expected = t.traduzir_conteudo_wiki(source, 'Português', cache_dir=cache)
            output = 'Olá.\n'
            next(cache.glob('*.json')).write_text(json.dumps({'output': output, 'sha256': hashlib.sha256(output.encode()).hexdigest()}), encoding='utf-8')
            self.assertEqual(t.traduzir_conteudo_wiki(source, 'Português', cache_dir=cache), expected)
            self.assertEqual(len(self.pipeline.inputs), 2)


class RestoreAndLockContracts(support.OfflineCase):
    # Reuse setup/helpers, without inheriting and rerunning the old test methods.
    run_batch = support.PublishingRegressionTests.run_batch

    def setUp(self):
        super().setUp()
        glossary = t.carregar_glossario()
        self.root = Path(self.enterContext(tempfile.TemporaryDirectory()))
        self.tool = self.root / 'scripts' / 'Translator'
        self.tool.mkdir(parents=True)
        (self.tool / 'technical_glossary.json.gz').write_bytes(b'fixture fingerprint')
        self.source = self.root / 'en' / 'chapter' / 'page.md'
        self.live = self.root / 'pt' / 'chapter' / 'page.md'
        self.source.parent.mkdir(parents=True)
        self.live.parent.mkdir(parents=True)
        self.source.write_text('# Hello\n\nInspect the item.\n', encoding='utf-8')
        self.original = b'# Previous translation\r\n\r\nUser content.\r\n'
        self.live.write_bytes(self.original)
        for name, value in (('DIRETORIO_ATUAL', self.tool), ('RAIZ_WIKI', self.root), ('PASTA_ORIGEM_EN', self.root / 'en')):
            self.stack.enter_context(patch.object(t, name, value))
        self.stack.enter_context(patch.object(t, 'carregar_glossario', return_value=glossary))
        self.preview = self.tool / '.translations' / 'preview' / 'pt' / 'chapter' / 'page.md'

    def test_restore_preserves_utf8_bom_and_crlf_exactly(self):
        original = b'\xef\xbb\xbf# Tradu\xc3\xa7\xc3\xa3o\r\n\r\nTexto.\r\n'
        self.live.write_bytes(original)
        self.assertEqual(self.run_batch(), 0)
        self.assertEqual(self.run_batch(aplicar=True), 0)
        self.assertEqual(t.restaurar_backups(['pt'], ['chapter/page.md']), 0)
        self.assertEqual(self.live.read_bytes(), original)
        self.assertEqual(t.restaurar_backups(['pt'], ['chapter/page.md']), 0)

    def test_two_invalid_attempts_do_not_publish_or_cache(self):
        self.pipeline.transform = lambda s: 'Missing end'
        self.assertEqual(self.run_batch(), 1)
        self.assertEqual(len(self.pipeline.inputs), 2)
        self.assertEqual(self.live.read_bytes(), self.original)
        self.assertFalse(self.preview.exists())
        self.assertEqual(list((self.tool / '.translations' / 'chunks').rglob('*.json')), [])
        receipt = json.loads((self.tool / '.translations' / 'failures' / 'pt' / 'chapter' / 'page.md.json').read_text(encoding='utf-8'))
        self.assertEqual([r['attempt'] for r in receipt['attempts']], [1, 2])

    def test_restore_refuses_modified_destination_and_corrupt_backup(self):
        self.assertEqual(self.run_batch(), 0)
        self.assertEqual(self.run_batch(aplicar=True), 0)
        applied = self.live.read_bytes()
        self.live.write_bytes(b'User edit\r\n')
        with self.assertRaisesRegex(RuntimeError, 'editado'):
            t.restaurar_backups(['pt'], ['chapter/page.md'])
        self.assertEqual(self.live.read_bytes(), b'User edit\r\n')
        self.live.write_bytes(applied)
        next((self.tool / '.translations' / 'backups').rglob('*.bak')).write_bytes(b'corrupt')
        with self.assertRaisesRegex(RuntimeError, 'Backup ausente ou alterado'):
            t.restaurar_backups(['pt'], ['chapter/page.md'])
        self.assertEqual(self.live.read_bytes(), applied)

    def test_lock_excludes_second_writer_and_cleans_up_on_exception(self):
        lock = self.tool / '.translations' / 'run.lock'
        with self.assertRaisesRegex(ValueError, 'injected'):
            with t.bloquear_lote():
                receipt = lock.read_bytes()
                with self.assertRaisesRegex(RuntimeError, 'bloqueio'):
                    self.run_batch()
                self.assertEqual(lock.read_bytes(), receipt)
                self.assertFalse(self.pipeline.inputs)
                raise ValueError('injected')
        self.assertFalse(lock.exists())
        self.assertEqual(self.live.read_bytes(), self.original)


class StructureContracts(support.OfflineCase):
    def test_mermaid_crlf_and_api_survive_full_translation(self):
        source = 'Hello PlayerBase uses GetGame().\r\n\r\n```mermaid\r\ngraph TD\r\nA[PlayerBase] --> B[EntityAI]\r\n```\r\n'
        result = self.translate(source)
        self.assertIn('```mermaid\r\ngraph TD\r\nA[PlayerBase] --> B[EntityAI]\r\n```', result)
        self.assertIn('PlayerBase uses GetGame()', result)
        self.assertNotIn('graph TD', self.pipeline.inputs[0])

    def test_table_alignment_change_is_rejected(self):
        source = '| Hello | Value |\n| :--- | ---: |\n| item | text |\n'
        with self.assertRaises(RuntimeError):
            self.translate(source, lambda s: s.replace(':--- | ---:', '---: | :---'))

    def test_blockquote_and_emphasis_removal_are_rejected(self):
        for source, transform in [('> Hello\n', lambda s: s.replace('> ', '')),
                                  ('Hello **important**.\n', lambda s: s.replace('**', ''))]:
            with self.subTest(source=source), self.assertRaises(RuntimeError):
                self.translate(source, transform)


class RealLanguageContracts(unittest.TestCase):
    def test_long_english_rejected_and_portuguese_accepted(self):
        with self.assertRaisesRegex(RuntimeError, 'Idioma detectado'):
            t.validar_idioma('You must start the server before connecting. Open the inventory to inspect the item and preserve all existing settings.', t.IDIOMAS_SUPORTADOS['pt'])
        t.validar_idioma('Você precisa iniciar o servidor antes de se conectar. Abra o inventário para inspecionar o objeto e preserve todas as configurações existentes.', t.IDIOMAS_SUPORTADOS['pt'])

    def test_short_text_is_explicitly_unverified(self):
        with patch.object(t, 'detector_idioma', side_effect=AssertionError('Short text must skip detector')):
            self.assertIsNone(t.validar_idioma('Hello', t.IDIOMAS_SUPORTADOS['pt']))


if __name__ == '__main__':
    unittest.main()
