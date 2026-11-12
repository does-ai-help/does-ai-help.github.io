import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('apache_builder', ROOT / 'scripts/prepare_november.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class ApacheSecurityIntakeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = json.loads((ROOT / 'november/search-2026-11-12-apache.json').read_text())
        cls.article, records, cls.meta = builder.assemble()
        cls.sources = {r['id']: r for r in records}

    def test_metadata_scope_and_links(self):
        topics = json.loads((ROOT / 'data/topic-taxonomy.json').read_text())['topics']
        self.assertEqual(len(set(self.log['selected_ids'])), 5)
        self.assertEqual(self.log['selected_count'], 5)
        for key in self.log['selected_ids']:
            source = self.sources[key]
            self.assertEqual(source['verification']['checked_on'], '2026-11-12')
            self.assertEqual(source['verification']['level'], 'content-checked')
            self.assertTrue(source['reading_scope'])
            self.assertFalse(set(source['topics']) - set(topics))
            self.assertTrue(set(source.get('related_to', [])).issubset(self.sources))
        for key in self.log['reused_existing_ids']:
            self.assertIn(key, self.sources)
        self.assertGreaterEqual(len(self.sources), self.log['combined_record_count_after_session'])

    def test_shared_flaw_not_multiple_independent_discoveries(self):
        keys = ['apachehttp21196182026', 'cve1196182026', 'wizapache2026', 'redhatapache2026']
        self.assertEqual(len({self.sources[k]['study_family'] for k in keys}), 1)
        for key in keys:
            self.assertIn('CVE-2026-119618', self.sources[key]['advisory_identifiers'])
        self.assertIn("Google Cloud researchers", self.sources['apachehttp21196182026']['summary'])

    def test_telemetry_patch_and_exploit_limits(self):
        self.assertIn('without configuration checks', self.sources['wizapache2026']['summary'])
        self.assertIn('2.0.24', self.sources['wizapache2026']['limitations'])
        self.assertIn('not Apache', self.sources['redhatapache2026']['limitations'])
        self.assertIn('not a local Chrome observation', self.sources['cve1196182026']['verification']['basis'])
        self.assertEqual(self.sources['modh2archive2026']['date'], '2026-06-09')
        self.assertFalse(self.log['access_notes']['exploit_or_scanner_run'])

    def test_main_framing_preserves_cluster_and_trend_boundary(self):
        self.assertIn('within 22 days', self.article)
        self.assertIn('overlapping remediation demand', self.article)
        self.assertIn('possible new norm', self.article)
        self.assertIn('does not by itself establish a historically unprecedented rate', self.article)
        self.assertIn('@openssh106p22026', self.article)
        self.assertIn('@modh2archive2026', self.article)


if __name__ == '__main__':
    unittest.main()
