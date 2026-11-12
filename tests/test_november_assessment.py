import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('assessment_builder', ROOT / 'scripts/prepare_november.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class AssessmentIntakeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = json.loads((ROOT / 'november/search-2026-11-12-assessment.json').read_text())
        cls.article, records, cls.meta = builder.assemble()
        cls.sources = {r['id']: r for r in records}

    def test_intake_is_appraised_with_valid_metadata(self):
        self.assertEqual(len(set(self.log['selected_ids'])), 9)
        self.assertEqual(self.log['selected_count'], 9)
        topics = json.loads((ROOT / 'data/topic-taxonomy.json').read_text())['topics']
        for key in self.log['selected_ids']:
            source = self.sources[key]
            self.assertEqual(source['verification']['checked_on'], '2026-11-12')
            self.assertEqual(source['verification']['level'], 'content-checked')
            self.assertTrue(source['reading_scope'])
            self.assertTrue(source['limitations'])
            self.assertFalse(set(source['topics']) - set(topics))
            self.assertTrue(set(source.get('related_to', [])).issubset(self.sources))
        self.assertGreaterEqual(len(self.sources), self.log['combined_record_count_after_session'])
        self.assertGreaterEqual(self.meta['cutoff'], self.log['searched_on'])

    def test_correction_is_linked_not_counted_as_replication(self):
        original = self.sources['vlasselaerdetectors2026']
        correction = self.sources['vlasselaercorrection2026']
        self.assertEqual(original['study_family'], correction['study_family'])
        self.assertEqual(correction['date'], '2026-10-06')
        self.assertEqual(correction['doi'], '10.1007/s40979-026-00236-8')
        self.assertIn('o3-based', correction['summary'])
        self.assertIn('not replication', correction['limitations'])
        self.assertIn('@vlasselaercorrection2026', self.article)

    def test_policy_product_and_learning_outcomes_are_distinguished(self):
        self.assertIn('Completion is not correctness', self.sources['csmsearch2026']['limitations'])
        self.assertIn('not a student learning experiment', self.sources['csmenteens2026']['limitations'])
        self.assertIn('not measured educational benefit', self.sources['nycschools2026']['limitations'])
        self.assertIn('not evidence of a universal statutory prohibition', self.sources['norwayschools2026']['limitations'])
        self.assertEqual(self.sources['ofsassessment2026']['study_family'], self.sources['yildirimassessment2026']['study_family'])
        self.assertIn('unlabeled theses', self.article)

    def test_access_and_discovery_do_not_invent_verification(self):
        self.assertFalse(self.log['access_notes']['local_chrome_used'])
        self.assertFalse(self.log['access_notes']['release_wide_audit'])
        for edge in self.log['confirmed_citation_edges']:
            self.assertIn(edge['citing'], self.sources)
            self.assertIn(edge['cited'], self.sources)
        for relation in self.log['other_followed_relationships']:
            self.assertIn(relation['from'], self.sources)
            self.assertIn(relation['to'], self.sources)
        self.assertLess(len(self.sources['yildirimassessment2026']['summary'].split()), 10)


if __name__ == '__main__':
    unittest.main()
