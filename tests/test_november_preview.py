import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('november_builder', ROOT / 'scripts/prepare_november.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class NovemberPreviewTests(unittest.TestCase):
    def test_assembly_is_additive_and_updates_existing_identity(self):
        article, sources, meta = builder.assemble()
        base = json.loads((ROOT / 'data/sources.json').read_text())
        new = json.loads((ROOT / 'data/november-sources.json').read_text())
        self.assertEqual(len(sources), len(base) + len(new))
        self.assertEqual(len(sources), len({r['id'] for r in sources}))
        paper = next(r for r in sources if r['id'] == 'ref-712e3405f2')
        self.assertEqual(paper['doi'], '10.1145/3706598.3713778')
        self.assertEqual(paper['publication_status'], 'peer-reviewed-conference')
        self.assertEqual(meta['release_status'], 'draft-preview')
        self.assertIn('provisional evidence cutoff', article)
        self.assertIn('not the final November release', article)

    def test_preview_cannot_change_october_inputs(self):
        original = (ROOT / 'data/release.json').read_bytes()
        manuscript = (ROOT / 'manuscript/article.md').read_bytes()
        builder.assemble()
        self.assertEqual((ROOT / 'data/release.json').read_bytes(), original)
        self.assertEqual((ROOT / 'manuscript/article.md').read_bytes(), manuscript)
        self.assertEqual(json.loads(original)['version'], '2026.10.15')

    def test_preview_workflow_overlays_preview_on_main_only(self):
        workflow = (ROOT / '.github/workflows/november-preview.yml').read_text()
        self.assertIn('ref: main', workflow)
        self.assertIn('diff -qr published/site deployment --exclude=preview', workflow)
        self.assertIn("github.ref == 'refs/heads/codex/november-2026-preparation'", workflow)
        self.assertIn("github.ref == 'refs/heads/main'", (ROOT / '.github/workflows/publish.yml').read_text())

    def test_csl_conference_type_is_preserved(self):
        self.assertEqual(next(r for r in builder.assemble()[1] if r['id'] == 'ref-712e3405f2')['publication_status'], 'peer-reviewed-conference')

    def test_summary_link_opens_rendered_page(self):
        article = builder.assemble()[0]
        self.assertIn('[November update summary](updates.html)', article)
        self.assertNotIn('[November update summary](downloads/november-update-summary.md)', article)

    def test_rendered_summary_retains_download_and_shared_navigation(self):
        page = (ROOT / 'preview/november/updates.html').read_text()
        self.assertIn('<h1 id="november-2026-preview-evidence-update">', page)
        self.assertIn('href="updates.html">What\'s new</a>', page)
        self.assertIn('href="downloads/november-update-summary.md" download', page)
        self.assertIn('href="downloads/search-2026-11-01.json"', page)
        self.assertIn('href="downloads/appraisals/november-citation-followup-2026-11-01.md"', page)
        self.assertIn('https://does-ai-help.github.io/preview/november/updates.html', page)
        self.assertIn('Back to top', page)

    def test_reference_previews_include_evidence_context(self):
        page = (ROOT / 'preview/november/index.html').read_text()
        self.assertIn('id="reference-preview-templates"', page)
        self.assertIn('class="reference-preview-summary"', page)
        self.assertIn('<strong>Limitations</strong>', page)
        self.assertIn('<strong>Source inspection</strong>', page)
        self.assertIn('assets/reference-preview.js', page)
        self.assertIn('assets/reference-preview.css', page)

    def test_reference_preview_preserves_touch_and_keyboard_access(self):
        script = (ROOT / 'scripts/web/reference-preview.js').read_text()
        self.assertIn('(hover: hover) and (pointer: fine) and (min-width: 721px)', script)
        self.assertIn("tooltip.setAttribute('role', 'tooltip')", script)
        self.assertIn("event.key === 'Escape'", script)
        self.assertIn("event.pointerType !== 'touch'", script)
        self.assertNotIn('preventDefault', script)
