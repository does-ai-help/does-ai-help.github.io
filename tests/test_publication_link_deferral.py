import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from check_links import is_publication_link


class PublicationDeferralTests(unittest.TestCase):
    meta = {'canonical_url': 'https://does-ai-help.github.io/',
            'github_url': 'https://github.com/does-ai-help/does-ai-help.github.io',
            'version': '2026.10.14'}

    def test_only_exact_current_release_is_deferred(self):
        url = self.meta['github_url'] + '/releases/tag/v2026.10.14'
        self.assertTrue(is_publication_link({'id': 'website-external-link', 'url': url}, self.meta))
        self.assertFalse(is_publication_link({'id': 'website-external-link', 'url': url.replace('.14', '.13')}, self.meta))

    def test_reference_records_are_never_deferred(self):
        for url in [self.meta['canonical_url'], self.meta['github_url'] + '/releases/tag/v2026.10.14']:
            self.assertFalse(is_publication_link({'id': 'research-source', 'url': url}, self.meta))

    def test_external_releases_are_never_deferred(self):
        self.assertFalse(is_publication_link({'id': 'website-external-link',
                                              'url': 'https://github.com/other/repo/releases/tag/v2026.10.14'}, self.meta))
