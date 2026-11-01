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
