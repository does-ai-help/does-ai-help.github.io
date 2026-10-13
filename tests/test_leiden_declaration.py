import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class LeidenDeclarationTests(unittest.TestCase):
    def setUp(self):
        self.record = next(r for r in json.loads((ROOT / 'data/sources.json').read_text()) if r['id'] == 'leiden2026')

    def test_registered_authors_not_endorsers(self):
        self.assertEqual(len(self.record['authors']), 16)
        self.assertEqual(self.record['authors'][0], 'Alper, Jarod')
        self.assertIn('Naskręcki, Bartosz', self.record['authors'])
        self.assertNotIn('Tao, Terence', self.record['authors'])
        self.assertNotIn('International Mathematical Union', self.record['authors'])

    def test_original_date_and_persistent_identifier(self):
        self.assertEqual(self.record['date'], '2026-06-02')
        self.assertEqual(self.record['doi'], '10.5281/zenodo.20302944')
        self.assertIn('2609.35334v2', self.record['version_note'])

    def test_normative_status_and_source_rights(self):
        self.assertEqual(self.record['method'], 'community-declaration')
        self.assertEqual(self.record['publication_status'], 'public-statement')
        self.assertIn('CC BY-NC 4.0', self.record['version_note'])
        self.assertIn('not an experiment', self.record['limitations'])
