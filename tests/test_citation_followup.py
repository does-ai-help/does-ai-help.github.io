import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CitationFollowupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = json.loads((ROOT / 'november/search-2026-11-01.json').read_text())
        cls.new = json.loads((ROOT / 'data/november-sources.json').read_text())
        cls.base = json.loads((ROOT / 'data/sources.json').read_text())
        cls.by_id = {r['id']: r for r in cls.base + cls.new}

    def test_search_selection_and_inspection_dates_resolve(self):
        log = self.log
        self.assertEqual(log['selected_count'], len(log['selected_ids']))
        self.assertEqual(len(log['selected_ids']), len(set(log['selected_ids'])))
        self.assertEqual(log['staged_total_after_session'], 98)
        self.assertEqual(log['combined_record_count_after_session'], 327)
        for key in log['selected_ids']:
            source = self.by_id[key]
            self.assertEqual(source['verification']['checked_on'], log['searched_on'])
            self.assertLessEqual(source['date'], log['searched_on'])
            self.assertTrue(source['reading_scope'])
            self.assertTrue(source['limitations'])
            self.assertTrue(source.get('doi') or source.get('arxiv_id') or source.get('report_number') or source['date_basis'])

    def test_citation_edges_are_observed_not_counts(self):
        edges = self.log['confirmed_citation_edges']
        self.assertEqual(len(edges), 17)
        self.assertEqual(len(edges), len({(e['citing'], e['cited']) for e in edges}))
        for edge in edges:
            self.assertIn(edge['citing'], self.by_id)
            self.assertIn(edge['cited'], self.by_id)
            self.assertTrue(edge['basis'])
        self.assertTrue(set(self.log['seed_ids']).issubset(self.by_id))

    def test_shared_benchmark_is_not_a_new_replication(self):
        a = self.by_id['kimunknown2026']
        b = self.by_id['alfaqeehprovenance2026']
        self.assertEqual(a['study_family'], b['study_family'])
        self.assertEqual(len(a['authors']), 28)
        self.assertIn('does not establish scientific correctness', b['limitations'])
        self.assertIn('failure to certify is not falsehood', b['limitations'])
        self.assertEqual(b['publication_status'], 'preprint')

    def test_early_career_experiment_preserves_measurement_boundaries(self):
        source = self.by_id['broschtasks2026']
        self.assertEqual(source['date'], '2026-10')
        self.assertIn('immediate', source['summary'])
        self.assertIn('internet access', source['limitations'])
        self.assertIn('LLM grading', source['limitations'])
        self.assertIn('model-version', source['limitations'])

    def test_new_reviews_and_access_limits_are_not_interventions(self):
        self.assertEqual(self.by_id['fanmetacognition2026']['method'], 'theory-building-perspective')
        self.assertEqual(self.by_id['rivacapital2026']['publication_status'], 'preprint')
        self.assertIn('403', self.by_id['iniecritical2026']['limitations'])
        self.assertIn('not a downloaded full text', self.by_id['iniecritical2026']['limitations'])
        self.assertEqual(len(self.by_id['fengprimer2026']['authors']), 19)
        self.assertIn('not recorded as a read PDF', self.by_id['fengprimer2026']['limitations'])
        self.assertEqual(self.by_id['ranadepublic2026']['authors'], ['Ranade, Gireeja'])
        self.assertIn('model scenarios', self.by_id['laneadoption2026']['limitations'])
