import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
spec = importlib.util.spec_from_file_location('november_verification_builder', ROOT / 'scripts/prepare_november.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class NovemberReleaseVerificationTests(unittest.TestCase):
    def test_doi_short_title_is_documented_without_changing_october(self):
        original = (ROOT / 'data/sources.json').read_bytes()
        _, records, _ = builder.assemble()
        paper = next(r for r in records if r['id'] == 'gmyrekdivide2026')
        self.assertIn('Disruption without dividend?', paper['title_aliases'])
        self.assertEqual(original, (ROOT / 'data/sources.json').read_bytes())

    def test_browser_history_is_append_only_and_keeps_access_limits(self):
        _, records, meta = builder.assemble()
        baseline = json.loads((ROOT / 'data/browser-verification.json').read_text())
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            (work / 'data').mkdir()
            builder.stage_browser_checks(work, records, meta)
            history = json.loads((work / 'data/browser-verification.json').read_text())
            self.assertEqual(history['checks'][:len(baseline['checks'])], baseline['checks'])
            checks = {r['id']: r for r in history['checks']}
            self.assertEqual(checks['barwickshared2026']['outcome'], 'identity-confirmed')
            self.assertEqual(checks['hesa2026']['outcome'], 'identity-confirmed')
            self.assertTrue(any(r['id'] == 'hesa2026' and r['outcome'] == 'access-blocked'
                                for r in history['checks']))
            self.assertEqual(checks['openainavierpaper2026']['outcome'], 'access-blocked')
            self.assertIn('not scientific replication', checks['barwickshared2026']['scope'])
            for key in ['gravityabout2026', 'gravitypolicy2026', 'ref-776550e112',
                        'ref-47ac0a3015', 'norwayschools2026', 'jabarianvoice2025',
                        'activtrakworkplace2026', 'luopitfalls2026',
                        'openaiphp2026', 'accenturetalent2026']:
                self.assertEqual(checks[key]['outcome'], 'identity-confirmed')
                self.assertTrue(checks[key]['checked_at'].startswith('2026-11-13'))
            gravity = next(r for r in history['checks'] if r['id'] == 'gravitypolicy2026'
                           and 'github.com/GravityLinux/website/blob/' in r['observed']['resolved_url'])
            self.assertIn('github.com/GravityLinux/website/blob/', gravity['observed']['resolved_url'])
            self.assertIn('not a redirect', gravity['redirect_basis'])
            self.assertIn('DNS4EU', gravity['notes'])
            self.assertEqual(checks['gravitypolicy2026']['observed']['resolved_url'],
                             'https://gravitylinux.org/policies/llm/')
            self.assertEqual(checks['hesa2026']['checked_at'], '2026-11-13T08:58:00.766Z')
            previous = [r for r in history['checks'] if r['id'] == 'gravityabout2026']
            self.assertTrue(any(r['outcome'] == 'access-blocked' for r in previous))

    def test_gravity_updates_preserve_canonical_urls_and_pin_revisions(self):
        _, records, _ = builder.assemble()
        by_id = {r['id']: r for r in records}
        base = {r['id']: r for r in json.loads((ROOT / 'data/sources.json').read_text())}
        expected = {'gravityabout2026': ('2026-10-14', 'cfc74e6b3fcdb2f794fbf725464f27b506ad8d21'),
                    'gravitypolicy2026': ('2026-10-13', '2d7bbba836646caed9441ed998021b3f18c479da')}
        for key, (date, revision) in expected.items():
            self.assertEqual(by_id[key]['url'], base[key]['url'])
            self.assertEqual(by_id[key]['date'], date)
            self.assertEqual(by_id[key]['source_revision']['commit'], revision)
            self.assertIn(revision, by_id[key]['source_revision']['file_url'])
            self.assertIn('local-chrome', by_id[key]['verification']['method'])
            self.assertEqual(base[key]['verification']['checked_on'], '2026-10-13')

    def test_saved_audit_is_rejected_for_a_different_database(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            (work / 'data').mkdir()
            (work / 'data/sources.json').write_text('[]\n')
            self.assertFalse(builder.stage_saved_audit(work))


if __name__ == '__main__':
    unittest.main()
