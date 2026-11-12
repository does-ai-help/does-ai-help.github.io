import importlib.util
import json
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('latest_november_builder', ROOT / 'scripts/prepare_november.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class LatestNovemberSourcesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = json.loads((ROOT / 'november/search-2026-11-11.json').read_text())
        records = json.loads((ROOT / 'data/sources.json').read_text()) + json.loads((ROOT / 'data/november-sources.json').read_text())
        cls.sources = {r['id']: r for r in records}

    def test_selected_sources_are_appraised_and_linked(self):
        self.assertEqual(self.log['selected_count'], 12)
        self.assertEqual(len(set(self.log['selected_ids'])), 12)
        taxonomy = json.loads((ROOT / 'data/topic-taxonomy.json').read_text())['topics']
        for key in self.log['selected_ids']:
            source = self.sources[key]
            self.assertEqual(source['verification']['checked_on'], '2026-11-11')
            self.assertEqual(source['verification']['level'], 'content-checked')
            self.assertTrue(source['date_basis'])
            self.assertTrue(source['reading_scope'])
            self.assertTrue(source['limitations'])
            self.assertFalse(set(source['topics']) - set(taxonomy))
            self.assertTrue(set(source.get('related_to', [])).issubset(self.sources))
        for edge in self.log['confirmed_citation_edges']:
            self.assertIn(edge['citing'], self.sources)
            self.assertIn(edge['cited'], self.sources)
            self.assertTrue(edge['basis'])

    def test_reports_and_commentary_are_not_replications(self):
        pairs = [('chaudhurialphaproofcode2026', 'kohlicode2026'), ('metrrdassessment2026', 'cotrard2026')]
        for primary, commentary in pairs:
            self.assertEqual(self.sources[primary]['study_family'], self.sources[commentary]['study_family'])
        self.assertEqual(self.sources['djadphp2026']['study_family'], self.sources['phpoom2026']['study_family'])
        self.assertEqual(len(self.sources['chaudhurialphaproofcode2026']['authors']), 9)
        self.assertIn('Not verification of the complete Signal apps', self.sources['chaudhurialphaproofcode2026']['limitations'])
        self.assertIn('redacted', self.sources['metrrdassessment2026']['limitations'])
        self.assertIn('not directly observed', self.sources['cotrard2026']['limitations'])

    def test_telemetry_is_not_causal_or_a_single_sample(self):
        release = self.sources['activtraklonger2026']
        annual = self.sources['activtrakworkplace2026']
        self.assertIn('9,140', release['summary'])
        self.assertIn('467', release['summary'])
        self.assertIn('not continuous active labor', release['limitations'])
        self.assertIn('2023-2025', annual['date_basis'])
        self.assertEqual(annual['date'], '2026')
        self.assertIn('no established untreated counterfactual', annual['limitations'])

    def test_alternative_reading_does_not_invent_chrome_receipts(self):
        self.assertFalse(self.log['access_notes']['local_chrome_used'])
        for key in self.log['access_notes']['alternative_http_reading']:
            self.assertIn('alternative-public-http', self.sources[key]['verification']['method'])
        self.assertIn('bdc478f', self.sources['djadphp2026']['date_basis'])
        self.assertEqual(self.sources['djadphp2026']['date'], '2026-11-08')

    def test_cutoff_and_manifest_stay_consistent(self):
        article, records, meta = builder.assemble()
        config = json.loads((ROOT / 'november/preview.json').read_text())
        self.assertEqual(meta['cutoff'], config['cutoff'])
        self.assertEqual(meta['version'], config['version'])
        self.assertGreaterEqual(len(records), self.log['combined_record_count_after_session'])
        cutoff = date.fromisoformat(config['cutoff'])
        label = f'{cutoff.day} {cutoff:%B %Y}'
        self.assertIn('provisional evidence cutoff of ' + label, article)
        self.assertIn('provisional evidence cutoff is ' + label, article)
        self.assertNotIn('{{cutoff_date}}', article)
        self.assertNotIn('provisional evidence cutoff is 1 November 2026', article)

    def test_cited_post_cutoff_source_is_rejected(self):
        original = builder.load

        def changed(path):
            value = original(path)
            if path == 'november/preview.json':
                value['cutoff'] = '2026-11-01'
            return value

        with patch.object(builder, 'load', side_effect=changed):
            with self.assertRaisesRegex(ValueError, 'exceeds preview cutoff'):
                builder.assemble()

    def test_later_batches_resolve_without_relabeling_the_evidence(self):
        for filename in ['search-2026-11-11-followup.json', 'search-2026-11-11-prerelease.json']:
            log = json.loads((ROOT / 'november' / filename).read_text())
            self.assertEqual(log['selected_count'], len(set(log['selected_ids'])))
            for key in log['selected_ids']:
                source = self.sources[key]
                self.assertEqual(source['verification']['checked_on'], log['searched_on'])
                self.assertLessEqual(source['date'], log['searched_on'])
                self.assertTrue(set(source.get('related_to', [])).issubset(self.sources))
        self.assertEqual(self.sources['andrewscpython2026']['authors'], ['Andrews, David', 'Zhang, Chao'])
        self.assertNotIn('doi', self.sources['koskaptx2026'])
        self.assertIn('partial correctness', self.sources['koskaptx2026']['limitations'])
        self.assertEqual(len({self.sources[k]['study_family'] for k in ['vaughanalpine2026', 'alpineauth2026', 'openssh106p22026', 'kultekinssh2026']}), 1)

    def test_version_and_outcome_boundaries_are_retained(self):
        final = self.sources['wilestemporary2026']
        self.assertIn('487', final['summary'])
        self.assertIn('573', final['limitations'])
        self.assertIn('not be silently substituted', final['limitations'])
        self.assertIn('agent versus chatbot', self.sources['balepurunderstanding2026']['limitations'])
        self.assertIn('2024 intervention', self.sources['wangfeedback2026']['limitations'])
        self.assertEqual(self.sources['jabarianvoice2025']['date'], '2025-08-18')
        self.assertIn('one percentage point', self.sources['jabarianvoice2025']['summary'])
        self.assertIn('403', self.sources['barwickshared2026']['limitations'])
        self.assertIn('10 November', self.sources['gallupproductivity2026']['date_basis'])

    def test_historical_counts_remain_valid_after_later_batches(self):
        log = json.loads((ROOT / 'november/search-2026-11-11-prerelease.json').read_text())
        article, records, _ = builder.assemble()
        self.assertGreaterEqual(len(records), log['combined_record_count_after_session'])
        self.assertGreaterEqual(len(json.loads((ROOT / 'data/november-sources.json').read_text())), log['staged_total_after_session'])
        self.assertEqual(log['planned_publication_target'], '2026-11-13')
        self.assertIn('November 2026 draft preview', article)


if __name__ == '__main__':
    unittest.main()
