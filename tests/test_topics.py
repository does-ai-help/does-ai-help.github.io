import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from topics import classify, title_topics


class TopicTests(unittest.TestCase):
    def setUp(self):
        self.taxonomy = json.loads((ROOT / 'data/topic-taxonomy.json').read_text())
        self.corrections = json.loads((ROOT / 'data/topic-corrections.json').read_text())
        self.records = json.loads((ROOT / 'data/sources.json').read_text())
        self.by_id = {r['id']: r for r in self.records}

    def test_corrections_target_real_records(self):
        self.assertFalse(set(self.corrections) - set(self.by_id))
        for correction in self.corrections.values():
            self.assertTrue(correction['basis'])

    def test_controlled_vocabulary_and_parents(self):
        for record in self.records:
            self.assertFalse(set(record['topics']) - set(self.taxonomy['topics']))
            for topic in record['topics']:
                for parent in self.taxonomy['parents'].get(topic, []):
                    self.assertIn(parent, record['topics'], record['id'])

    def test_mathematics_coverage(self):
        for key in ['mathmisalignment2026', 'taomath2026', 'leiden2026',
                    'openainavierpaper2026', 'alphaevolve2025', 'funsearch2023']:
            self.assertIn('mathematics', self.by_id[key]['topics'])
        self.assertGreaterEqual(sum('mathematics' in r['topics'] for r in self.records), 20)
        self.assertNotIn('mathematics', self.by_id['dgm2025']['topics'])

    def test_fallback_is_conservative(self):
        self.assertNotIn('security', title_topics('Learning and the risk of capacity dissolution'))
        self.assertNotIn('science', title_topics('Computer science enrollment report'))
        self.assertIn('security', title_topics('Remote code execution in AI tools'))

    def test_unknown_label_fails(self):
        with self.assertRaises(ValueError):
            classify({'id': 'test', 'topics': ['made-up']}, self.taxonomy, {})

    def test_reader_citations_do_not_reuse_audit_history(self):
        builder = (ROOT / 'scripts/build.mjs').read_text()
        refs = builder.split('const texRefs =', 1)[1].split("write('latex/body.tex'", 1)[0]
        self.assertNotIn('version_note', refs)
        notes = json.loads((ROOT / 'data/citation-notes.json').read_text())
        self.assertFalse(set(notes) - set(self.by_id))
        self.assertNotIn('Previously an unresolved candidate', ' '.join(notes.values()))
