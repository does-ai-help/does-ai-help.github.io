import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from verify_references import check, doi_normal, exception_valid, page_metadata, title_match


class IdentityTests(unittest.TestCase):
    def test_punctuation_and_site_suffix(self):
        self.assertTrue(title_match("Does AI Help Us?", "Does AI Help Us? | A Research Review")[0])

    def test_unrelated_or_generic_title(self):
        for title in ["Nature", "Concentraties in het bankwezen", "Page not found", "Just a moment"]:
            self.assertFalse(title_match("Generative AI at Work", title)[0])

    def test_topic_similarity_is_not_identity(self):
        self.assertFalse(title_match("Generative AI at Work", "Generative AI in Education")[0])

    def test_metadata_priority_and_doi(self):
        m = page_metadata(b'<title>Site</title><meta name="citation_title" content="Generative AI at Work"><meta name="citation_doi" content="10.1093/qje/qjae044">')
        self.assertIn("Generative AI at Work", m["titles"])
        self.assertEqual(doi_normal("https://doi.org/10.1093/QJE/QJAE044"), m["doi"])

    def test_svg_titles_do_not_concatenate_document_title(self):
        m = page_metadata(b"<title>Study title</title><svg><title>Icon</title></svg>")
        self.assertEqual(m["titles"], ["Study title", "Icon"])

    @patch("verify_references.registry_metadata")
    @patch("verify_references.retrieve")
    def test_registry_match_cannot_hide_wrong_source_url(self, fetch, registry):
        fetch.return_value = ({"status": 200, "url": "https://example.org"}, b"<title>A completely unrelated research study</title>")
        registry.return_value = [{"access": {"url": "https://api.crossref.org/works/test"}, "titles": ["Generative AI at Work"], "doi": "10.1234/right"}]
        result = check({"id": "x", "title": "Generative AI at Work", "url": "https://example.org", "doi": "10.1234/right"})
        self.assertEqual(result["identity_status"], "unresolved")

    @patch("verify_references.retrieve")
    def test_http_success_not_identity(self, fetch):
        fetch.return_value = ({"status": 200, "url": "https://example.org"}, b"<title>Unrelated work</title>")
        result = check({"id": "x", "title": "Generative AI at Work", "url": "https://example.org"})
        self.assertEqual(result["identity_status"], "unresolved")

    @patch("verify_references.retrieve")
    def test_matching_title_with_wrong_authors_needs_review(self, fetch):
        fetch.return_value = ({"status": 200, "url": "https://example.org"}, b'<title>Generative AI at Work</title><meta name="citation_author" content="Different, Person">')
        result = check({"id": "x", "title": "Generative AI at Work", "url": "https://example.org", "authors": ["Smith, Alice"]})
        self.assertEqual(result["identity_status"], "unresolved")

    @patch("verify_references.registry_metadata")
    @patch("verify_references.retrieve")
    def test_doi_conflict_blocks_even_matching_title(self, fetch, registry):
        fetch.return_value = ({"status": 200, "url": "https://example.org"}, b'<title>Generative AI at Work</title><meta name="citation_doi" content="10.1234/wrong">')
        registry.return_value = []
        result = check({"id": "x", "title": "Generative AI at Work", "url": "https://example.org", "doi": "10.1234/right"})
        self.assertEqual(result["identity_status"], "mismatch")

    def test_expired_or_mismatch_exception_rejected(self):
        result = {"identity_status": "unresolved", "expected_title": "Generative AI at Work", "url": "https://example.org"}
        ex = {"reviewer": "Editor", "reason": "Primary metadata inspected", "evidence_url": "https://example.org", "observed_title": result["expected_title"], "expected_title": result["expected_title"], "url": result["url"], "checked_on": "2026-10-13", "expires_on": "2026-11-13"}
        self.assertTrue(exception_valid(ex, result, "2026-10-13"))
        self.assertFalse(exception_valid(ex, result, "2026-12-13"))
        result["identity_status"] = "mismatch"
        self.assertFalse(exception_valid(ex, result, "2026-10-13"))


if __name__ == "__main__":
    unittest.main()
