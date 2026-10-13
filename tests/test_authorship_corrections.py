import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from export import to_csl
from curate import unique_object


class AuthorshipCorrectionTests(unittest.TestCase):
    def test_duplicate_corrections_cannot_silently_erase_authors(self):
        with self.assertRaisesRegex(ValueError, "Duplicate JSON key"):
            json.loads('{"source":{"authors":["Author"]},"source":{"date":"2026"}}', object_pairs_hook=unique_object)

    def setUp(self):
        self.records = {r["id"]: r for r in json.loads((ROOT / "data/sources.json").read_text())}

    def test_highlighted_sources_have_authors_and_provenance(self):
        corrections = json.loads((ROOT / "data/bibliographic-corrections.json").read_text(), object_pairs_hook=unique_object)
        for key, correction in corrections.items():
            if correction.get("authorship_basis"):
                self.assertTrue(self.records[key]["authors"], key)
                self.assertTrue(self.records[key]["publisher"], key)
                self.assertIn("13 October 2026", self.records[key]["authorship_basis"])

    def test_registered_creators_not_later_endorsers(self):
        record = self.records["mathmisalignment2026"]
        self.assertEqual(len(record["authors"]), 25)
        self.assertEqual(record["authors"][0], "Avila, Artur")
        self.assertIn("Tao, Terence", record["authors"])
        self.assertEqual(record["author_display"], "Terence Tao et al.")
        self.assertEqual(len(to_csl(record)["author"]), 25)
        self.assertIn("alphabetical creator order", to_csl(record)["note"])
        self.assertNotIn("et al..", (ROOT / "latex/body.tex").read_text())

    def test_kpmg_quoted_speakers_are_not_authors(self):
        record = self.records["ref-fee88585ea"]
        self.assertEqual(record["authors"], ["KPMG International"])
        self.assertIn("Chase, Steve", record["quoted_speakers"])

    def test_anthropic_recommended_named_authors(self):
        record = self.records["ref-b05d2a6ff4"]
        self.assertEqual(len(record["authors"]), 7)
        self.assertEqual(record["authors"][0], "Huang, Saffron")
        self.assertEqual(record["publisher"], "Anthropic")

    def test_metr_followup_does_not_replace_original(self):
        update = self.records["metr2026update"]
        self.assertIn("metr2025", update["follow_up_to"])
        self.assertIn("metr2026update", self.records["ref-596ebdd94b"]["related_to"])
        self.assertEqual(self.records["ref-596ebdd94b"]["authors"][2], "Barnes, Beth")
        self.assertEqual(self.records["metr2025"]["authors"][2], "Barnes, Elizabeth")
