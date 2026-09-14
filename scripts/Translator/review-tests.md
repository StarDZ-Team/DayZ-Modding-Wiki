# Independent translator regression tests

Task `task_08602cb796e1`, dispatch `ctx_43e74a341994`, 2026-09-14. Only `test_review_regressions.py` and this report were edited; no production edits, commits, subworkers, real translations, model downloads or GPU calls.

## Coverage

Added 36 independent unittest methods: 20 protection cases and 16 publishing cases. Final combined run: **48 tests passed, zero failures or errors**, at the stable hashes below; earlier failures were repaired by the coordinator. Fixtures encode intended safe behavior, with no expected-failure decorators or production changes to satisfy them.

- RP-01: angle-bracket destinations and nested inline markers inside HTML attributes round-trip without leaked placeholders.
- RP-02: indented and HTML pre/code contents never reach fake generation.
- RP-03: title-bearing, deeply nested-parenthesis and reference links preserve destinations/keys while translating labels.
- RP-04: fake summaries retaining every marker but deleting lists are rejected; table-row omission is rejected.
- RP-05: actual known types and explicit configuration assignments are protected while ordinary scope/weight/units prose remains translatable.
- RP-06: Print outside backticks is protected; actual inputs/dependencies keys must exist in the glossary and be protected in assignments.
- RP-07: ordinary native/false/string/override and imperative Call prose remains translatable; parenthetical Documentation is not treated as an API call.
- RP-08: observed asset/config filenames include imageset/bin/css.
- RP-09: unordered and ordered list-contained fences are supported.
- Numeric values: unsigned values, percentage decimals, negative signs and scientific notation survive attempted changes.
- Publishing: preview-only default, cached resume, explicit no-resume, model revision invalidation, exact original CRLF backup bytes, repeated apply, source/destination edits before and during apply, corrupted/missing preview, read-only check, failed generation, traversal, failed atomic live replacement.

All publishing paths are patched into a TemporaryDirectory, including source, destination, previews, manifest and backups. The real glossary is read once for domain evidence; publishing tests redirect glossary disk fingerprinting to a temporary file and use the captured dictionary in memory. FakePipeline records submitted text, uses a character-count tokenizer and never loads transformers/torch. carregar_modelo is patched to raise immediately if accidentally called. Language identification is stubbed deliberately: these tests cannot establish language quality or the correctness of the language detector.

## Commands and results

New suite command from repository root:

```powershell
scripts/Translator/.env/Scripts/python.exe -B -m unittest discover -s scripts/Translator -p test_review_regressions.py -v
```

The corrected standalone run executed 35 tests with process exit 1, nine failure records across five methods (subtests count separately), and no errors. Thirty methods passed, including all 15 publishing methods. The final suite below additionally includes the 12 pre-existing tests and records current source hashes before and after execution. The in-process report runner itself exits normally; use successful/failure_records below for the test outcome rather than its shell exit code.

One test-fixture issue was fixed before the final run: the injected os.replace failure now compares resolved paths because Windows temporary paths can have short/long-name aliases. Before correction the injection did not fire; that earlier result was not a production failure. Assertion diagnostics for missing glossary entries were also narrowed to avoid printing the entire dictionary. No behavioral assertions were weakened.

## Earlier failure meaning and final resolution

All concrete earlier failures listed here passed in the final run after coordinator production repairs. The signed/scientific fixture originally returned `+15` and `9e+3` for source `-15` and `1e-3`, demonstrating changed technical values accepted by the translation function. Mod config tests expose missing `inputs` and `dependencies` categories/protection. Prose tests expose unconditional freezing of ordinary native/false/string/override/Call words. Consult the final receipt and failure traces below for the exact current result; the coordinator may repair production concurrently.

Source changed between preview and apply is allowed either to be refused safely or to trigger fresh generation; it must never silently apply stale output. Corrupt cache is similarly allowed to be rejected or regenerated, with live content protected. The final deliberate workflow contract additionally requires apply to use an existing current preview and never generate; a dedicated test now enforces that rule. These assertions test safety outcomes rather than low-level implementation details. Crash durability, symlink race attacks, simultaneous writers after the final hash check, semantic translation fidelity and actual model/GPU behavior are not certified by these tests. List/table omission tests establish rejection of their explicit examples; marker-preserving semantic omissions with unchanged structure remain a review limitation.

The coordinator subsequently changed apply to refuse generation when no valid preview exists. Generation-race and failed-generation fixtures now run preview mode first and assert the fake pipeline was actually invoked; the destination-race test then applies the staged preview and requires refusal. This maintains coverage of the intended event instead of passing merely because apply refuses an absent preview.

## Final receipt

```json
{
  "utc": "2026-09-14T05:05:03.023971+00:00",
  "python": "3.14.3 (tags/v3.14.3:323c59a, Feb  3 2026, 16:04:56) [MSC v.1944 64 bit (AMD64)]",
  "tests_run": 48,
  "failure_records": 0,
  "errors": 0,
  "successful": true,
  "hashes_before": {
    "translator.py": "f1a8ab22bb12b02de2ef60f4dd2e3af19672d2f73d8f8a5098b857ea12604152",
    "build_glossary.py": "4b6700c1ba8fd27b553f7be752b9c3e274d1073903656ab926fa8598f823e737",
    "technical_glossary.json": "9b1e1026f4cb14b764df31da785e54acd44051f9103d9b79deae336d49b9109b",
    "test_translator.py": "7ff9165017bd846b344b56bf491e0fbcb87265079f4eb640b7f6bb430526e1f8",
    "test_review_regressions.py": "15f7f3018a1532fb2e1359c9c62803f067da57ef6eadb2abe718295b1c8cf9bd"
  },
  "hashes_after": {
    "translator.py": "f1a8ab22bb12b02de2ef60f4dd2e3af19672d2f73d8f8a5098b857ea12604152",
    "build_glossary.py": "4b6700c1ba8fd27b553f7be752b9c3e274d1073903656ab926fa8598f823e737",
    "technical_glossary.json": "9b1e1026f4cb14b764df31da785e54acd44051f9103d9b79deae336d49b9109b",
    "test_translator.py": "7ff9165017bd846b344b56bf491e0fbcb87265079f4eb640b7f6bb430526e1f8",
    "test_review_regressions.py": "15f7f3018a1532fb2e1359c9c62803f067da57ef6eadb2abe718295b1c8cf9bd"
  },
  "stable_during_run": true
}
```

## Failure details

None in final run.

## Full test output

```text
test_original_numeric_sign_and_exponent_cannot_be_rewritten (test_review_regressions.ProtectionRegressionTests.test_original_numeric_sign_and_exponent_cannot_be_rewritten) ... ok
test_original_unsigned_numeric_values_cannot_be_rewritten (test_review_regressions.ProtectionRegressionTests.test_original_unsigned_numeric_values_cannot_be_rewritten) ... ok
test_rp01_angle_destinations_roundtrip_without_placeholder_leak (test_review_regressions.ProtectionRegressionTests.test_rp01_angle_destinations_roundtrip_without_placeholder_leak) ... ok
test_rp01_html_attribute_with_nested_inline_marker (test_review_regressions.ProtectionRegressionTests.test_rp01_html_attribute_with_nested_inline_marker) ... ok
test_rp02_html_code_body_is_never_sent_for_translation (test_review_regressions.ProtectionRegressionTests.test_rp02_html_code_body_is_never_sent_for_translation) ... ok
test_rp02_indented_code_is_never_sent_for_translation (test_review_regressions.ProtectionRegressionTests.test_rp02_indented_code_is_never_sent_for_translation) ... ok
test_rp03_deep_parentheses_link_preserves_entire_destination (test_review_regressions.ProtectionRegressionTests.test_rp03_deep_parentheses_link_preserves_entire_destination) ... ok
test_rp03_reference_keys_and_destination_stay_consistent (test_review_regressions.ProtectionRegressionTests.test_rp03_reference_keys_and_destination_stay_consistent) ... ok
test_rp03_title_link_preserves_destination_translates_label (test_review_regressions.ProtectionRegressionTests.test_rp03_title_link_preserves_destination_translates_label) ... ok
test_rp04_omission_copying_all_markers_is_rejected (test_review_regressions.ProtectionRegressionTests.test_rp04_omission_copying_all_markers_is_rejected) ... ok
test_rp04_table_row_omission_is_rejected (test_review_regressions.ProtectionRegressionTests.test_rp04_table_row_omission_is_rejected) ... ok
test_rp05_known_types_and_explicit_config_assignment_are_protected (test_review_regressions.ProtectionRegressionTests.test_rp05_known_types_and_explicit_config_assignment_are_protected) ... ok
test_rp05_ordinary_config_key_words_remain_translatable (test_review_regressions.ProtectionRegressionTests.test_rp05_ordinary_config_key_words_remain_translatable) ... ok
test_rp06_mod_config_assignment_keys_are_protected (test_review_regressions.ProtectionRegressionTests.test_rp06_mod_config_assignment_keys_are_protected) ... ok
test_rp06_mod_config_keys_are_in_inventory (test_review_regressions.ProtectionRegressionTests.test_rp06_mod_config_keys_are_in_inventory) ... ok
test_rp06_simple_official_callable_is_protected_in_api_context (test_review_regressions.ProtectionRegressionTests.test_rp06_simple_official_callable_is_protected_in_api_context) ... ok
test_rp07_ordinary_keyword_homonyms_are_translatable (test_review_regressions.ProtectionRegressionTests.test_rp07_ordinary_keyword_homonyms_are_translatable) ... ok
test_rp07_parenthetical_prose_and_imperatives_are_translatable (test_review_regressions.ProtectionRegressionTests.test_rp07_parenthetical_prose_and_imperatives_are_translatable) ... ok
test_rp08_actual_asset_and_config_filenames_are_protected (test_review_regressions.ProtectionRegressionTests.test_rp08_actual_asset_and_config_filenames_are_protected) ... ok
test_rp09_valid_list_fences_are_supported (test_review_regressions.ProtectionRegressionTests.test_rp09_valid_list_fences_are_supported) ... ok
test_apply_uses_staged_content_and_backs_up_exact_original_bytes (test_review_regressions.PublishingRegressionTests.test_apply_uses_staged_content_and_backs_up_exact_original_bytes) ... ok
test_apply_without_reviewable_preview_refuses_to_generate (test_review_regressions.PublishingRegressionTests.test_apply_without_reviewable_preview_refuses_to_generate) ... ok
test_check_is_read_only_and_never_generates (test_review_regressions.PublishingRegressionTests.test_check_is_read_only_and_never_generates) ... ok
test_corrupt_preview_is_not_applied_as_valid_cache (test_review_regressions.PublishingRegressionTests.test_corrupt_preview_is_not_applied_as_valid_cache) ... ok
test_default_stages_preview_and_preserves_live_bytes (test_review_regressions.PublishingRegressionTests.test_default_stages_preview_and_preserves_live_bytes) ... ok
test_destination_changed_after_preview_is_not_overwritten (test_review_regressions.PublishingRegressionTests.test_destination_changed_after_preview_is_not_overwritten) ... ok
test_destination_changed_during_generation_leaves_user_edit_intact (test_review_regressions.PublishingRegressionTests.test_destination_changed_during_generation_leaves_user_edit_intact) ... ok
test_explicit_no_resume_regenerates_preview (test_review_regressions.PublishingRegressionTests.test_explicit_no_resume_regenerates_preview) ... ok
test_failed_final_replace_preserves_live_and_keeps_backup (test_review_regressions.PublishingRegressionTests.test_failed_final_replace_preserves_live_and_keeps_backup) ... ok
test_failed_translation_leaves_live_page_intact_and_not_successful (test_review_regressions.PublishingRegressionTests.test_failed_translation_leaves_live_page_intact_and_not_successful) ... ok
test_missing_preview_is_not_trusted_from_manifest_alone (test_review_regressions.PublishingRegressionTests.test_missing_preview_is_not_trusted_from_manifest_alone) ... ok
test_model_revision_change_invalidates_cache (test_review_regressions.PublishingRegressionTests.test_model_revision_change_invalidates_cache) ... ok
test_parent_and_absolute_path_traversal_rejected_before_generation (test_review_regressions.PublishingRegressionTests.test_parent_and_absolute_path_traversal_rejected_before_generation) ... ok
test_resume_reuses_unchanged_verified_preview_without_generation (test_review_regressions.PublishingRegressionTests.test_resume_reuses_unchanged_verified_preview_without_generation) ... ok
test_source_changed_after_preview_never_applies_old_cached_translation (test_review_regressions.PublishingRegressionTests.test_source_changed_after_preview_never_applies_old_cached_translation) ... ok
test_source_changed_during_generation_leaves_live_page_intact (test_review_regressions.PublishingRegressionTests.test_source_changed_during_generation_leaves_live_page_intact) ... ok
test_ambiguous_prose_and_identifier_boundaries (test_translator.ProtectionTests.test_ambiguous_prose_and_identifier_boundaries) ... ok
test_atomic_failure_preserves_existing_file (test_translator.ProtectionTests.test_atomic_failure_preserves_existing_file) ... ok
test_block_moved_into_prose_rejected (test_translator.ProtectionTests.test_block_moved_into_prose_rejected) ... ok
test_chunks_preserve_source (test_translator.ProtectionTests.test_chunks_preserve_source) ... ok
test_glossary_symbol_outside_backticks (test_translator.ProtectionTests.test_glossary_symbol_outside_backticks) ... ok
test_incomplete_generation_rejected (test_translator.ProtectionTests.test_incomplete_generation_rejected) ... ok
test_links_html_paths_frontmatter_and_directives (test_translator.ProtectionTests.test_links_html_paths_frontmatter_and_directives) ... ok
test_missing_duplicate_changed_reordered_markers_rejected (test_translator.ProtectionTests.test_missing_duplicate_changed_reordered_markers_rejected) ... ok
test_nested_fences_crlf_and_inline_backticks (test_translator.ProtectionTests.test_nested_fences_crlf_and_inline_backticks) ... ok
test_pipeline_round_trip_without_sending_code (test_translator.ProtectionTests.test_pipeline_round_trip_without_sending_code) ... ok
test_round_trip_code_and_technical_terms (test_translator.ProtectionTests.test_round_trip_code_and_technical_terms) ... ok
test_unclosed_source_block_rejected (test_translator.ProtectionTests.test_unclosed_source_block_rejected) ... ok

----------------------------------------------------------------------
Ran 48 tests in 0.762s

OK
```
