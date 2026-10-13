import json
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from download_names import download_names


class DownloadLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            href = dict(attrs).get('href', '')
            if href.startswith('downloads/'):
                self.links.append(urlsplit(href).path.split('/')[-1])


class DownloadNameTests(unittest.TestCase):
    def setUp(self):
        self.meta = json.loads((ROOT / 'data/release.json').read_text())
        self.names = download_names(self.meta)

    def test_bibliography_names_and_compound_extensions(self):
        version = self.meta['version']
        self.assertEqual(self.names['bibliography.bib'], f'does-ai-work-{version}.bib')
        self.assertEqual(self.names['bibliography.csl.json'], f'does-ai-work-{version}.csl.json')
        self.assertEqual(len(self.names.values()), len(set(self.names.values())))

    def test_full_patch_version_changes_every_public_filename(self):
        next_meta = {**self.meta, 'version': self.meta['version'] + '.next'}
        for source, name in download_names(next_meta).items():
            self.assertNotEqual(name, self.names[source])

    def test_javascript_and_python_share_the_filename_manifest(self):
        manifest = json.loads((ROOT / 'site/downloads/download-files.json').read_text())
        self.assertEqual(manifest['files'], self.names)
        self.assertEqual(manifest['version'], self.meta['version'])
        self.assertEqual(manifest['filtered_csl'], f"does-ai-work-filtered-{self.meta['version']}.csl.json")

    def test_all_advertised_downloads_are_project_specific_and_versioned(self):
        for page in (ROOT / 'site').glob('*.html'):
            parser = DownloadLinks()
            parser.feed(page.read_text())
            self.assertTrue(parser.links, page.name)
            for name in parser.links:
                self.assertTrue(name.startswith(('does-ai-work-', 'does-ai-help-')), name)
                self.assertIn(self.meta['version'], name)
                self.assertTrue((ROOT / 'site/downloads' / name).exists(), name)

    def test_alias_contents_and_archive_version_boundaries(self):
        import zipfile
        downloads = ROOT / 'site/downloads'
        for original, versioned in self.names.items():
            self.assertEqual((downloads / original).read_bytes(), (downloads / versioned).read_bytes(), versioned)
        with zipfile.ZipFile(downloads / self.meta['archive_name']) as archive:
            allowed = set(self.names) | set(self.names.values())
            for member in archive.namelist():
                relative = Path(member).relative_to(self.meta['snapshot'])
                if len(relative.parts) == 1:
                    self.assertIn(relative.name, allowed)
