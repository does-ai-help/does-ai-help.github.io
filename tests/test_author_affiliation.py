import json
import unittest
from pathlib import Path
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]


class AffiliationTests(unittest.TestCase):
    def test_web_byline_and_pdf_title_page(self):
        meta = json.loads((ROOT / 'data/release.json').read_text())
        author = next(a for a in meta['authors'] if a['name'] == 'Witold Bołt')
        self.assertEqual(author['institution'], 'Jit Team')
        html = (ROOT / 'site/index.html').read_text()
        byline = html.split('<p class="byline">', 1)[1].split('</p>', 1)[0]
        self.assertIn('Witold Bołt, PhD', byline)
        self.assertIn('author-affiliation">· Jit Team', byline)
        page = PdfReader(ROOT / 'site/downloads' / f"does-ai-help-{meta['version']}.pdf").pages[0]
        text = page.extract_text()
        self.assertIn('Jit Team', text)
        self.assertLess(text.index('Jit Team'), text.index('Abstract'))
