"""Independent preservation/publishing contracts; no GPU or live wiki writes.

Run with: .env/Scripts/python.exe -B -m unittest test_review_regressions -v
Language identification is stubbed: these fixtures test structure and publishing,
not linguistic quality. Failed contracts are intentionally not expectedFailure.
"""
from contextlib import ExitStack, redirect_stdout
import io
import json
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch

import translator as t


class CharacterTokenizer:
    eos_token_id = 0

    def encode(self, text, **kwargs):
        return list(text)


class FakePipeline:
    tokenizer = CharacterTokenizer()

    def __init__(self, transform=None, before=None):
        self.transform = transform or (lambda text: text.replace('Hello', 'Olá'))
        self.before = before
        self.inputs = []

    def __call__(self, messages, **kwargs):
        text = messages[-1]['content'].split('\n\n', 1)[1]
        self.inputs.append(text)
        if self.before:
            self.before()
        return [{'generated_text': self.transform(text)}]


class OfflineCase(unittest.TestCase):
    def setUp(self):
        self.stack = self.enterContext(ExitStack())
        self.stack.enter_context(patch.object(t, 'carregar_modelo', side_effect=AssertionError('GPU loading forbidden in regression tests')))
        self.stack.enter_context(patch.object(t, 'validar_idioma', return_value=None))
        self.pipeline = FakePipeline()
        self.stack.enter_context(patch.object(t, 'pipe', self.pipeline))

    def translate(self, source, transform=None):
        if transform is not None:
            self.pipeline.transform = transform
        return t.traduzir_conteudo_wiki(source, t.IDIOMAS_SUPORTADOS['pt'])

    def assertProtectedRoundtrip(self, source, literals):
        masked, saved = t.proteger_codigo(source)
        for literal in literals:
            self.assertNotIn(literal, masked, f'Protected content reached model: {literal!r}')
        self.assertEqual(t.restaurar_codigo(masked, saved), source)


class ProtectionRegressionTests(OfflineCase):
    def test_rp01_angle_destinations_roundtrip_without_placeholder_leak(self):
        for target in ('<guide.md>', '<https://example.com/guide>'):
            with self.subTest(target=target):
                source = f'[Read]({target})\n'
                self.assertEqual(self.translate(source), source)
                self.assertNotIn('WIKICODE', self.translate(source))

    def test_rp01_html_attribute_with_nested_inline_marker(self):
        source = '<span title="`Widget`">Hello</span>\n'
        self.assertEqual(self.translate(source), source.replace('Hello', 'Olá'))

    def test_rp02_indented_code_is_never_sent_for_translation(self):
        source = 'Hello\n\n    danger = TranslateMe;\n    return danger;\n'
        self.assertProtectedRoundtrip(source, ('danger', 'TranslateMe'))
        self.assertEqual(self.translate(source, lambda s: s.replace('danger', 'perigo')), source)

    def test_rp02_html_code_body_is_never_sent_for_translation(self):
        source = '<pre><code>danger = TranslateMe;</code></pre>\n'
        self.assertProtectedRoundtrip(source, ('danger', 'TranslateMe'))
        self.assertEqual(self.translate(source, lambda s: s.replace('danger', 'perigo')), source)

    def test_rp03_title_link_preserves_destination_translates_label(self):
        source = '[Hello](../guide.md#installation "Installation guide")\n'
        self.assertEqual(self.translate(source, lambda s: s.replace('Hello', 'Olá').replace('installation', 'instalacao')), source.replace('Hello', 'Olá'))

    def test_rp03_deep_parentheses_link_preserves_entire_destination(self):
        source = '[Hello](../chapter_(draft_(two)).md#installation)\n'
        result = self.translate(source, lambda s: s.replace('Hello', 'Olá').replace('draft', 'rascunho').replace('installation', 'instalacao'))
        self.assertEqual(result, source.replace('Hello', 'Olá'))

    def test_rp03_reference_keys_and_destination_stay_consistent(self):
        source = '[Hello][install-ref]\n\n[install-ref]: ../guide.md#installation "Guide"\n'
        result = self.translate(source, lambda s: s.replace('Hello', 'Olá').replace('install-ref', 'referencia').replace('installation', 'instalacao'))
        self.assertEqual(result, source.replace('Hello', 'Olá'))

    def test_rp04_omission_copying_all_markers_is_rejected(self):
        source = '# Hello\n\n- Inspect `PlayerBase` before deleting.\n- Preserve `EntityAI` until saved.\n'

        def omit(text):
            end = re.search(r'WIKIEND[A-F0-9]+', text).group()
            markers = re.findall(r'WIKICODE[A-F0-9]+X\d+X', text)
            return '# Olá\n\n' + ' '.join(markers) + '\n' + end

        with self.assertRaises(RuntimeError):
            self.translate(source, omit)

    def test_rp04_table_row_omission_is_rejected(self):
        source = '# Hello\n\n| Option | Meaning |\n| --- | --- |\n| first | useful |\n| second | essential |\n'
        with self.assertRaises(RuntimeError):
            self.translate(source, lambda s: '\n'.join(line for line in s.split('\n') if 'essential' not in line))

    def test_rp05_known_types_and_explicit_config_assignment_are_protected(self):
        self.assertProtectedRoundtrip('Use Timer, Widget and Object. Set scope = 2.\n', ('Timer', 'Widget', 'Object', 'scope'))

    def test_rp05_ordinary_config_key_words_remain_translatable(self):
        source = 'The scope of this guide includes weight and units of measurement.\n'
        masked, _ = t.proteger_codigo(source)
        for word in ('scope', 'weight', 'units'):
            self.assertIn(word, masked)

    def test_rp06_simple_official_callable_is_protected_in_api_context(self):
        self.assertProtectedRoundtrip('Call Print to log the message.\n', ('Print',))

    def test_rp06_mod_config_keys_are_in_inventory(self):
        glossary = t.carregar_glossario()
        for key in ('inputs', 'dependencies'):
            with self.subTest(key=key):
                self.assertTrue(key in glossary, f'Missing config key in inventory: {key}')
                self.assertIn('config_key', glossary[key]['categories'])

    def test_rp06_mod_config_assignment_keys_are_protected(self):
        self.assertProtectedRoundtrip('Set inputs = "Inputs.xml" and dependencies[] = { "Mission" }.\n', ('inputs', 'dependencies'))

    def test_rp07_ordinary_keyword_homonyms_are_translatable(self):
        for sentence, word in (('This is true for native tools.', 'native'), ('This claim is false.', 'false'), ('Tie a string around the parcel.', 'string'), ('You may override the suggested choice.', 'override')):
            with self.subTest(word=word):
                masked, _ = t.proteger_codigo(sentence)
                self.assertIn(word, masked)

    def test_rp07_parenthetical_prose_and_imperatives_are_translatable(self):
        for sentence, word in (('Documentation (optional).', 'Documentation'), ('Call your administrator.', 'Call')):
            with self.subTest(word=word):
                masked, _ = t.proteger_codigo(sentence)
                self.assertIn(word, masked)

    def test_rp08_actual_asset_and_config_filenames_are_protected(self):
        self.assertProtectedRoundtrip('Use prefabs.imageset and config.bin and styles.css.\n', ('prefabs.imageset', 'config.bin', 'styles.css'))

    def test_rp09_valid_list_fences_are_supported(self):
        for source in ('- ```c\n  danger = TranslateMe;\n  ```\n', '1. ```c\n   danger = TranslateMe;\n   ```\n'):
            with self.subTest(source=source):
                self.assertProtectedRoundtrip(source, ('danger', 'TranslateMe'))

    def test_original_unsigned_numeric_values_cannot_be_rewritten(self):
        source = 'Hello: allow 4096 bytes and 12.5% overhead.\n'
        self.assertEqual(self.translate(source, lambda s: s.replace('4096', '2048').replace('12.5', '99')), source)

    def test_original_numeric_sign_and_exponent_cannot_be_rewritten(self):
        source = 'Hello: the offset is -15 and the tolerance is 1e-3.\n'
        self.assertEqual(self.translate(source, lambda s: s.replace('-', '+').replace('1e', '9e')), source)


class PublishingRegressionTests(OfflineCase):
    def setUp(self):
        super().setUp()
        # Read the real dictionary before redirecting all mutable paths to temp.
        glossary = t.carregar_glossario()
        folder = self.enterContext(tempfile.TemporaryDirectory())
        self.root = Path(folder)
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

    def run_batch(self, **kwargs):
        with redirect_stdout(io.StringIO()):
            return t.iniciar_traducao_em_massa(idiomas=['pt'], **kwargs)

    def test_default_stages_preview_and_preserves_live_bytes(self):
        self.assertEqual(self.run_batch(), 0)
        self.assertEqual(self.live.read_bytes(), self.original)
        self.assertEqual(self.preview.read_text(encoding='utf-8'), '# Olá {#hello}\n\nInspect the item.\n')

    def test_apply_without_reviewable_preview_refuses_to_generate(self):
        self.assertNotEqual(self.run_batch(aplicar=True), 0)
        self.assertFalse(self.pipeline.inputs)
        self.assertFalse(self.preview.exists())
        self.assertEqual(self.live.read_bytes(), self.original)

    def test_resume_reuses_unchanged_verified_preview_without_generation(self):
        self.assertEqual(self.run_batch(), 0)
        self.pipeline.transform = lambda s: self.fail('Valid cached preview should not generate again')
        self.assertEqual(self.run_batch(), 0)
        self.assertEqual(self.live.read_bytes(), self.original)

    def test_apply_uses_staged_content_and_backs_up_exact_original_bytes(self):
        self.assertEqual(self.run_batch(), 0)
        staged = self.preview.read_bytes()
        self.assertEqual(self.run_batch(aplicar=True), 0)
        self.assertEqual(self.live.read_bytes(), staged)
        backups = list((self.tool / '.translations' / 'backups').rglob('*.bak'))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_bytes(), self.original)
        self.assertEqual(self.run_batch(aplicar=True), 0)
        backups_after = list((self.tool / '.translations' / 'backups').rglob('*.bak'))
        self.assertEqual([p.read_bytes() for p in backups_after], [self.original])

    def test_destination_changed_after_preview_is_not_overwritten(self):
        self.assertEqual(self.run_batch(), 0)
        edited = b'New manual translation\r\n'
        self.live.write_bytes(edited)
        self.assertNotEqual(self.run_batch(aplicar=True), 0)
        self.assertEqual(self.live.read_bytes(), edited)

    def test_source_changed_after_preview_never_applies_old_cached_translation(self):
        self.assertEqual(self.run_batch(), 0)
        self.source.write_text('# Hello\n\nDifferent source text.\n', encoding='utf-8')
        self.pipeline.inputs.clear()
        result = self.run_batch(aplicar=True)
        if result == 0:
            self.assertTrue(self.pipeline.inputs, 'Changed source must invalidate cached output')
            self.assertIn('Different source text.', self.live.read_text(encoding='utf-8'))
        else:
            self.assertEqual(self.live.read_bytes(), self.original)

    def test_source_changed_during_generation_leaves_live_page_intact(self):
        self.pipeline.before = lambda: self.source.write_text('# Concurrent edit\n', encoding='utf-8')
        self.assertNotEqual(self.run_batch(), 0)
        self.assertTrue(self.pipeline.inputs)
        self.assertEqual(self.live.read_bytes(), self.original)
        self.assertFalse(self.preview.exists())

    def test_destination_changed_during_generation_leaves_user_edit_intact(self):
        edited = b'Concurrent destination edit\n'
        self.pipeline.before = lambda: self.live.write_bytes(edited)
        self.assertEqual(self.run_batch(), 0)
        self.assertTrue(self.pipeline.inputs)
        self.assertNotEqual(self.run_batch(aplicar=True), 0)
        self.assertEqual(self.live.read_bytes(), edited)

    def test_corrupt_preview_is_not_applied_as_valid_cache(self):
        self.assertEqual(self.run_batch(), 0)
        self.preview.write_text('CORRUPTED CACHE', encoding='utf-8')
        self.pipeline.inputs.clear()
        result = self.run_batch(aplicar=True)
        self.assertNotIn(b'CORRUPTED CACHE', self.live.read_bytes())
        if result == 0:
            self.assertTrue(self.pipeline.inputs)
            self.assertIn('Olá', self.live.read_text(encoding='utf-8'))
        else:
            self.assertEqual(self.live.read_bytes(), self.original)

    def test_missing_preview_is_not_trusted_from_manifest_alone(self):
        self.assertEqual(self.run_batch(), 0)
        expected = self.preview.read_bytes()
        self.preview.unlink()
        self.pipeline.inputs.clear()
        self.assertNotEqual(self.run_batch(aplicar=True), 0)
        self.assertEqual(self.live.read_bytes(), self.original)
        self.assertEqual(self.run_batch(), 0)
        self.assertEqual(self.preview.read_bytes(), expected)

    def test_model_revision_change_invalidates_cache(self):
        self.assertEqual(self.run_batch(), 0)
        self.pipeline.inputs.clear()
        with patch.object(t, 'MODEL_REVISION', 'different-test-revision'):
            self.assertEqual(self.run_batch(), 0)
        self.assertTrue(self.pipeline.inputs)

    def test_explicit_no_resume_regenerates_preview(self):
        self.assertEqual(self.run_batch(), 0)
        self.pipeline.inputs.clear()
        self.assertEqual(self.run_batch(retomar=False), 0)
        self.assertTrue(self.pipeline.inputs)

    def test_check_is_read_only_and_never_generates(self):
        self.assertEqual(self.run_batch(verificar=True), 0)
        self.assertFalse(self.pipeline.inputs)
        self.assertFalse((self.tool / '.translations').exists())
        self.assertEqual(self.live.read_bytes(), self.original)

    def test_failed_translation_leaves_live_page_intact_and_not_successful(self):
        self.pipeline.transform = lambda s: 'Incomplete generation without final sentinel'
        self.assertNotEqual(self.run_batch(), 0)
        self.assertTrue(self.pipeline.inputs)
        self.assertEqual(self.live.read_bytes(), self.original)
        self.assertFalse(self.preview.exists())
        report = json.loads((self.tool / '.translations' / 'last-run.json').read_text(encoding='utf-8'))
        self.assertEqual(report['results'][0]['status'], 'failed')

    def test_parent_and_absolute_path_traversal_rejected_before_generation(self):
        for path in ('../pt/chapter/page.md', str(self.live.resolve())):
            with self.subTest(path=path):
                with self.assertRaises(ValueError):
                    self.run_batch(filtros=[path])
        self.assertFalse(self.pipeline.inputs)
        self.assertEqual(self.live.read_bytes(), self.original)

    def test_failed_final_replace_preserves_live_and_keeps_backup(self):
        self.assertEqual(self.run_batch(), 0)
        real_replace = t.os.replace

        def fail_live(source, destination):
            if Path(destination).resolve() == self.live.resolve():
                raise OSError('Injected live destination replace failure')
            return real_replace(source, destination)

        with patch.object(t.os, 'replace', side_effect=fail_live):
            self.assertNotEqual(self.run_batch(aplicar=True), 0)
        self.assertEqual(self.live.read_bytes(), self.original)
        self.assertEqual(list(self.live.parent.glob('*.tmp')), [])
        backups = list((self.tool / '.translations' / 'backups').rglob('*.bak'))
        self.assertTrue(any(p.read_bytes() == self.original for p in backups))


if __name__ == '__main__':
    unittest.main()
