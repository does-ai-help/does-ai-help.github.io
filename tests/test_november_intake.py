import json
import re
import unittest
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class NovemberIntakeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = json.loads((ROOT / 'data/november-sources.json').read_text())
        cls.base = json.loads((ROOT / 'data/sources.json').read_text())
        cls.by_id = {r['id']: r for r in cls.sources}

    def test_unique_staged_identities_and_scope(self):
        self.assertEqual(len(self.sources), len(self.by_id))
        self.assertEqual(len(self.sources), len({r['url'] for r in self.sources}))
        self.assertFalse(set(self.by_id) & {r['id'] for r in self.base})
        taxonomy = json.loads((ROOT / 'data/topic-taxonomy.json').read_text())
        for source in self.sources:
            self.assertEqual(source['target_release'], '2026-11')
            self.assertEqual(source['staging_status'], 'appraised-not-yet-published')
            self.assertEqual(source['verification']['level'], 'content-checked')
            self.assertTrue(source['verification']['basis'])
            self.assertLessEqual(source['date'], source['verification']['checked_on'])
            self.assertFalse(set(source['topics']) - set(taxonomy['topics']))

    def test_draft_citations_resolve_without_expanding_october(self):
        draft = '\n'.join(path.read_text() for path in (ROOT / 'manuscript').glob('november-*.md'))
        ids = {item.strip().lstrip('@') for group in re.findall(r'\[@([^\]]+)\]', draft)
               for item in group.split(';')}
        available = set(self.by_id) | {r['id'] for r in self.base}
        self.assertFalse(ids - available)
        self.assertIn('torvaldstools2026', ids)
        self.assertIn('pincharttools2026', ids)
        self.assertIn('cooktools2026', ids)
        self.assertIn('luuambitious2026', ids)
        for source in self.sources:
            for related in source['related_to']:
                self.assertIn(related, available)

    def test_alternative_checks_are_not_november_receipts(self):
        ledger = json.loads((ROOT / 'november/browser-observations.json').read_text())
        self.assertEqual(ledger['target_release'], '2026-11')
        self.assertFalse(ledger['release_receipts_complete'])
        self.assertEqual(ledger['method'], 'local-chrome-native')
        for observation in ledger['observations']:
            self.assertIn(observation['id'], self.by_id)
            self.assertEqual(observation['source_url'], self.by_id[observation['id']]['url'])
            self.assertTrue(observation['refresh_required'])

    def test_policies_are_rechecks_not_duplicate_sources(self):
        rechecks = json.loads((ROOT / 'data/november-source-rechecks.json').read_text())
        self.assertRegex(rechecks['upstream_revision'], r'^[a-f0-9]{40}$')
        existing = {r['id'] for r in self.base}
        for record in rechecks['records']:
            self.assertIn(record['id'], existing)
            self.assertNotIn(record['id'], self.by_id)
            self.assertIn(rechecks['upstream_revision'], record['inspected_url'])

    def test_essay_date_uses_publisher_metadata(self):
        source = self.by_id['luuambitious2026']
        observation = source['metadata_observation']
        self.assertEqual(observation['guid'], source['url'])
        self.assertEqual(parsedate_to_datetime(observation['pubDate']).date().isoformat(), source['date'])
        self.assertEqual(observation['feed_type'], 'rss')
        self.assertEqual(source['method'], 'expert-commentary')
