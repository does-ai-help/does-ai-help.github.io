import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate import document_receipt_errors
from export import to_csl


class DocumentProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.records = json.loads((ROOT / "data/document-source-updates.json").read_text())
        self.receipt = next(r["document_verification"] for r in self.records if r["id"] == "ref-47ac0a3015")

    def test_valid_receipt(self):
        self.assertEqual(document_receipt_errors(self.receipt), [])

    def test_private_path_is_rejected(self):
        self.assertTrue(document_receipt_errors(dict(self.receipt, filename="/Users/example/private/paper.pdf")))

    def test_invalid_hash_and_page_count_are_rejected(self):
        self.assertTrue(document_receipt_errors(dict(self.receipt, sha256="not-a-checksum")))
        self.assertTrue(document_receipt_errors(dict(self.receipt, pages=0)))

    def test_redistribution_is_not_implicitly_permitted(self):
        self.assertTrue(document_receipt_errors(dict(self.receipt, redistributed=True)))

    def test_future_reading_date_is_rejected(self):
        self.assertTrue(document_receipt_errors(dict(self.receipt, checked_on="2099-01-01")))

    def test_versions_are_linked_not_independent_studies(self):
        versions = [r for r in self.records if r.get("study_family") == "hamza-agent-behavior"]
        self.assertEqual(len(versions), 3)
        self.assertEqual(sum(r["verification_level"] == "content-checked" for r in versions), 1)
        ids = {r["id"] for r in versions}
        for r in versions:
            self.assertEqual(set(r["related_to"]), ids - {r["id"]})

    def test_original_record_does_not_claim_supplied_pdf(self):
        original = next(r for r in self.records if r["id"] == "ref-776550e112")
        self.assertNotIn("document_verification", original)

    def test_citation_export_preserves_document_scope(self):
        record = next(r for r in self.records if r["id"] == "ref-283d4e8368")
        citation = to_csl(dict(record, verification={"level": "content-checked"}))
        self.assertIn(record["document_verification"]["sha256"], citation["note"])
        self.assertIn("not redistributed", citation["note"])


if __name__ == "__main__":
    unittest.main()
