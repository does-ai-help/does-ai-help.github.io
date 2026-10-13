import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from audit_sources import Metadata, publication_metadata
from export import to_csl


class PublicationMetadataTests(unittest.TestCase):
    def parse(self, nodes):
        parsed = Metadata()
        parsed.feed('<script type="application/ld+json">' + json.dumps(nodes) + '</script>')
        return publication_metadata(parsed, "Primary article")

    def test_publication_not_modification(self):
        self.assertEqual(self.parse({"@type": "BlogPosting", "headline": "Primary article", "datePublished": "2024-08-13", "dateModified": "2025-02-24", "author": {"name": "OpenAI"}}), ("2024-08-13", ["OpenAI"]))

    def test_ignore_other_articles_and_site_dates(self):
        self.assertEqual(self.parse({"@graph": [{"@type": "Organization", "name": "Primary article", "datePublished": "2008"}, {"@type": "Article", "headline": "Related article", "datePublished": "2026-01-01"}, {"@type": "Article", "headline": "Primary article", "datePublished": "2025-10-21"}]}), ("2025-10-21", []))

    def test_conflicting_dates_require_editor(self):
        self.assertEqual(self.parse([{"@type": "Article", "headline": "Primary article", "datePublished": date} for date in ["2024", "2025"]])[0], "")

    def test_no_inference_from_modification_only(self):
        self.assertEqual(self.parse({"@type": "Article", "headline": "Primary article", "dateModified": "2026-10-13"}), ("", []))

    def test_malformed_jsonld_is_ignored(self):
        parsed = Metadata()
        parsed.feed('<script type="application/ld+json">invalid</script>')
        self.assertEqual(publication_metadata(parsed, "Primary article"), ("", []))

    def test_edited_book_preserves_roles_and_partial_date(self):
        source = {"id": "book", "title": "Example", "url": "https://example.org", "authors": [], "editors": ["Editor, Alice"], "year": 2019, "date": "2019-05", "date_basis": "Publisher metadata", "publication_status": "book", "summary": "", "topics": [], "method": "review", "verification": {"level": "identity-checked"}, "limitations": ""}
        citation = to_csl(source)
        self.assertEqual(citation["type"], "book")
        self.assertEqual(citation["author"], [])
        self.assertEqual(citation["editor"], [{"family": "Editor", "given": "Alice"}])
        self.assertEqual(citation["issued"]["date-parts"], [[2019, 5]])
        self.assertIn("Publisher metadata", citation["note"])


if __name__ == "__main__":
    unittest.main()
