import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from prepare_november import assemble, flag_deferred_access, stage_access_deferrals
from verify_references import access_deferral_valid
from export import to_csl


class AccessDeferralTests(unittest.TestCase):
    def setUp(self):
        _, records, self.release = assemble()
        self.sources = {r['id']: r for r in records}
        policy = json.loads((ROOT / 'november/access-deferrals.json').read_text())
        common = {k: v for k, v in policy.items() if k != 'records'}
        self.decisions = [{**common, **r} for r in policy['records']]
        self.source = self.sources['baimehomework2026']
        self.decision = next(d for d in self.decisions if d['id'] == self.source['id'])
        self.result = {'id': self.source['id'], 'identity_status': 'unresolved', 'conflicts': [],
                       'observations': [{'access': {'status': 403}}]}

    def valid(self, decision=None, result=None, source=None, release=None, today='2026-11-13'):
        return access_deferral_valid(decision or self.decision, result or self.result,
                                     source or self.source, release or self.release, today)

    def test_explicit_decision_does_not_assert_identity_confirmation(self):
        self.assertTrue(self.valid())
        self.assertEqual(self.result['identity_status'], 'unresolved')
        self.assertEqual(len(self.decisions), 4)
        self.assertNotIn('observed_title', self.decision)

    def test_decision_cannot_hide_mismatch_not_found_or_conflict(self):
        for status in ['mismatch', 'confirmed', 'browser-confirmation']:
            self.assertFalse(self.valid(result={**self.result, 'identity_status': status}))
        for code in [404, 410]:
            self.assertFalse(self.valid(result={**self.result, 'observations': [{'access': {'status': code}}]}))
        self.assertFalse(self.valid(result={**self.result, 'conflicts': ['Wrong DOI']}))

    def test_expired_changed_and_unapproved_records_are_not_deferred(self):
        self.assertFalse(self.valid(today='2026-12-01'))
        self.assertFalse(self.valid(today='2026-11-12'))
        self.assertFalse(self.valid(release={**self.release, 'release': '2026-12'}))
        for key in ['approved_by', 'approval_basis', 'reason', 'source_fingerprint']:
            self.assertFalse(self.valid(decision={**self.decision, key: ''}))
        self.assertFalse(self.valid(source={**self.source, 'url': 'https://example.org/other'}))
        self.assertFalse(self.valid(source={**self.source, 'authors': ['Other, Author']}))

    def test_stage_only_changes_isolated_exceptions(self):
        original = (ROOT / 'data/identity-exceptions.json').read_bytes()
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            (work / 'data').mkdir()
            decisions = stage_access_deferrals(work, list(self.sources.values()), self.release)
            staged = json.loads((work / 'data/identity-exceptions.json').read_text())
            self.assertEqual(len(staged), len(json.loads(original)) + 4)
            self.assertEqual(decisions, self.decisions)
        self.assertEqual(original, (ROOT / 'data/identity-exceptions.json').read_bytes())

    def test_public_label_and_export_note_distinguish_history_from_current_access(self):
        key = self.source['id']
        html = (f'<article class="source-row" id="{key}" data-id="{key}">'
                '<span class="status checked">content checked</span>'
                '<div class="source-body"><details>Earlier appraisal</details></div></article>'
                f'<li id="ref-{key}">Citation</li>'
                f'<template data-reference-id="{key}">Preview</template>')
        flagged = flag_deferred_access(html, self.decisions, self.release['version'])
        self.assertEqual(flagged.count('Currently unverified for November.'), 3)
        self.assertNotIn('>content checked<', flagged)
        self.assertIn('does-ai-help-access-deferrals-', flagged)
        self.assertLess(flagged.index('Currently unverified for November.'), flagged.index('<details>'))
        self.assertIn('Currently unverified', to_csl(self.source, 'Currently unverified')['note'])
        self.assertNotIn('Currently unverified', to_csl(self.source)['note'])


if __name__ == '__main__':
    unittest.main()
