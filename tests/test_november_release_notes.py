import hashlib
import importlib.util
import json
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('notes_builder', ROOT / 'scripts/prepare_november.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class PageLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        if tag == 'a' and attrs.get('href'):
            self.links.append(attrs['href'])


class NovemberReleaseNotesTests(unittest.TestCase):
    def test_notes_describe_current_draft_not_completed_release(self):
        notes = (ROOT / 'november/RELEASE-NOTES.md').read_text()
        _, records, meta = builder.assemble()
        self.assertIn(meta['version'], notes)
        self.assertIn(f'**229 to {len(records)} evidence records**', notes)
        self.assertIn(f'**{len(records) - 229} references**', notes)
        self.assertIn('do not announce a completed release', notes)
        self.assertIn('Outstanding Work Before Publication', notes)
        self.assertIn('not inserted into the article PDF', notes)

    def test_rendered_notes_navigation_and_evidence_targets(self):
        site = ROOT / 'preview/november'
        html = (site / 'release-notes.html').read_text()
        self.assertIn('November 2026 Release Notes', html)
        self.assertIn('noindex,follow', html)
        self.assertIn('https://does-ai-help.github.io/preview/november/release-notes.html', html)
        self.assertIn('Back to top', html)
        notes = PageLinks()
        notes.feed(html)
        evidence = {r['id'] for r in builder.assemble()[1]}
        for link in notes.links:
            if link.startswith('bibliography.html#'):
                self.assertIn(link.split('#', 1)[1], evidence)
            elif link.startswith('#'):
                self.assertIn(link[1:], notes.ids)
        for page in ['index.html', 'updates.html', 'releases.html']:
            self.assertIn('href="release-notes.html">November release notes</a>', (site / page).read_text())

    def test_notes_are_not_part_of_article(self):
        article, _, _ = builder.assemble()
        self.assertNotIn('November 2026 Release Notes', article)
        self.assertNotIn('release-notes.html', article)


class CheckedPdfReuseTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.download = self.root / 'preview/november/downloads'
        self.download.mkdir(parents=True)
        self.meta = {'version': 'test-preview', 'cutoff': '2026-11-12'}
        self.article = 'Unchanged manuscript\n'
        self.records = [{'id': 'sample'}]
        self.pdf = b'%PDF-1.7\nexisting bytes\n'
        (self.download / 'release.json').write_text(json.dumps(self.meta))
        (self.download / 'sources.json').write_text(json.dumps(self.records))
        (self.download / 'article.md').write_text(self.article)
        (self.download / 'does-ai-help-test-preview.pdf').write_bytes(self.pdf)
        (self.download / 'checksums.sha256').write_text(hashlib.sha256(self.pdf).hexdigest() + '  does-ai-help-test-preview.pdf\n')

    def reuse(self, article=None, records=None, meta=None):
        with patch.object(builder, 'ROOT', self.root):
            return builder.existing_pdf_for_web_update(
                self.article if article is None else article,
                self.records if records is None else records,
                self.meta if meta is None else meta)

    def test_checked_pdf_is_returned_byte_for_byte(self):
        self.assertEqual(self.reuse(), self.pdf)

    def test_changed_publication_inputs_require_full_build(self):
        with self.assertRaisesRegex(ValueError, 'unchanged manuscript'):
            self.reuse(article='Changed manuscript')
        with self.assertRaisesRegex(ValueError, 'unchanged evidence'):
            self.reuse(records=[])
        with self.assertRaisesRegex(ValueError, 'unchanged release metadata'):
            self.reuse(meta={**self.meta, 'cutoff': '2026-11-13'})

    def test_corrupt_pdf_cannot_be_reused(self):
        (self.download / 'does-ai-help-test-preview.pdf').write_bytes(b'%PDF-1.7\nchanged bytes')
        with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
            self.reuse()


if __name__ == '__main__':
    unittest.main()
