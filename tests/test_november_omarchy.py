import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('omarchy_builder', ROOT / 'scripts/prepare_november.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class OmarchyCaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = json.loads((ROOT / 'november/search-2026-11-12-omarchy.json').read_text())
        cls.article, records, cls.meta = builder.assemble()
        cls.sources = {r['id']: r for r in records}

    def test_selected_records_have_traceable_scopes(self):
        topics = json.loads((ROOT / 'data/topic-taxonomy.json').read_text())['topics']
        self.assertEqual(len(set(self.log['selected_ids'])), 9)
        for key in self.log['selected_ids']:
            record = self.sources[key]
            self.assertEqual(record['verification']['checked_on'], '2026-11-12')
            self.assertEqual(record['verification']['level'], 'content-checked')
            self.assertTrue(record['reading_scope'])
            self.assertTrue(record['date_basis'])
            self.assertFalse(set(record['topics']) - set(topics))
            self.assertTrue(set(record.get('related_to', [])).issubset(self.sources))
            if record.get('source_revision'):
                self.assertTrue(record['date_kind'])
                for field in ['file_url', 'history_url', 'authored_at', 'committed_at']:
                    self.assertTrue(record['source_revision'][field])
        for key in self.log['reused_existing_ids']:
            self.assertIn(key, self.sources)

    def test_allegations_are_not_adjudicated_or_tallied_as_trials(self):
        self.assertIn('Does not name Omarchy', self.sources['calligerosasahi2026']['summary'])
        self.assertIn('not audited findings', self.sources['prakashomarchy2026']['limitations'])
        self.assertEqual(self.sources['calligerosasahi2026']['study_family'], self.sources['prakashomarchy2026']['study_family'])
        self.assertIn('specific misconduct is not established', self.article)
        self.assertIn('not its measured net effect', self.article)

    def test_dates_and_license_scope_are_not_conflated(self):
        self.assertEqual(self.sources['m1n1license2026']['date'], '2026-10-02')
        self.assertEqual(self.sources['asahicopyright2021']['date'], '2021-01-05')
        self.assertIn('19 July 2026', self.sources['asahicopyright2021']['date_basis'])
        self.assertIsNone(self.sources['mitlicense']['date'])
        self.assertIn('older MIT-licensed', self.article)
        self.assertIn('multiyear commitments and AI tokens', self.sources['provenomarchyfunding2026']['summary'])

    def test_checks_do_not_overstate_access_or_audit(self):
        self.assertFalse(self.log['access_notes']['x_posts_directly_verified'])
        self.assertFalse(self.log['access_notes']['local_chrome_used'])
        self.assertFalse(self.log['access_notes']['forensic_source_or_binary_audit'])
        self.assertNotIn('2512.00867', [s.get('arxiv') for s in self.sources.values()])
        self.assertGreaterEqual(len(self.sources), self.log['combined_record_count_after_session'])
        for edge in self.log['confirmed_citation_edges']:
            self.assertIn(edge['citing'], self.sources)
            self.assertIn(edge['cited'], self.sources)


if __name__ == '__main__':
    unittest.main()
