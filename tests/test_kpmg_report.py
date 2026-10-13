import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class KpmgReportTests(unittest.TestCase):
    def setUp(self):
        self.records = {r['id']: r for r in json.loads((ROOT / 'data/sources.json').read_text())}

    def test_report_authors_and_month_precision(self):
        report = self.records['kpmgpulseq32026']
        self.assertEqual(report['authors'], ['Emmanuel, Priya', 'Höck, Benedikt', 'Benson, Simon'])
        self.assertEqual(report['date'], '2026-09')
        self.assertIn('page 27', report['authorship_basis'])
        self.assertEqual(report['verification']['level'], 'content-checked')
        self.assertEqual(report['document_verification']['pages'], 30)
        self.assertFalse(report['document_verification']['redistributed'])

    def test_quarters_are_related_not_conflated(self):
        earlier = self.records['ref-fee88585ea']
        report = self.records['kpmgpulseq32026']
        self.assertEqual(earlier['authors'], ['KPMG International'])
        self.assertEqual(earlier['study_family'], report['study_family'])
        self.assertIn(report['id'], earlier['related_to'])
        self.assertIn(earlier['id'], report['related_to'])
        self.assertIn('Q2', earlier['summary'])

    def test_findings_remain_qualified_in_manuscript(self):
        article = (ROOT / 'manuscript/article.md').read_text()
        self.assertIn('89% report measurable AI value', article)
        self.assertIn('value/cost questions exclude early-stage respondents', article)
        self.assertIn('not proof that those practices caused returns', article)
