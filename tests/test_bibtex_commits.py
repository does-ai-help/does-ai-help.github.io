import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from export import bib_short_commits, to_csl


class BibtexCommitTests(unittest.TestCase):
    def test_notes_and_pinned_urls_use_twelve_characters(self):
        commit = "2f127af408e1b4675662f9b8a0c3606f6565a1a7"
        text = f"Revision {commit}: https://gitlab.com/qemu-project/qemu/-/blob/{commit}/docs/file.rst"
        self.assertEqual(bib_short_commits(text), text.replace(commit, commit[:12]))

    def test_checksums_and_existing_short_ids_are_unchanged(self):
        text = "SHA-256 " + "a" * 64 + "; commit abc123def456; DOI 10.1234/example"
        self.assertEqual(bib_short_commits(text), text)

    def test_full_provenance_stays_in_canonical_data_and_csl(self):
        records = json.loads((ROOT / "data/sources.json").read_text())
        record = next(r for r in records if r["id"] == "qemupolicy2026")
        self.assertRegex(to_csl(record)["note"], r"commit [a-f0-9]{40}")
        bib = (ROOT / "site/downloads/bibliography.bib").read_text()
        self.assertIsNone(re.search(r"(?<![a-f0-9])[a-f0-9]{40}(?![a-f0-9])", bib))
        for r in records:
            if r.get("document_verification") and r["verified"]:
                self.assertIn(r["document_verification"]["sha256"], bib)
