import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from verify_references import check, github_raw_url


class GithubFallbackTests(unittest.TestCase):
    def test_preserves_repo_ref_and_path(self):
        self.assertEqual(github_raw_url("https://github.com/org/repo/blob/abc/docs/POLICY.md"), "https://raw.githubusercontent.com/org/repo/abc/docs/POLICY.md")

    def test_rejects_unrelated_or_ambiguous_addresses(self):
        for url in ["https://evil.test/org/repo/blob/main/POLICY.md", "https://github.com/org/repo/blob/main/../POLICY.md", "https://github.com/org/repo/blob/main/%2e%2e/POLICY.md", "https://github.com/org/repo/blob/main/POLICY.md?token=secret"]:
            self.assertIsNone(github_raw_url(url))

    def test_service_error_can_use_matching_official_heading(self):
        source = {"id": "policy", "url": "https://github.com/org/repo/blob/main/POLICY.md", "title": "AI Usage Policy", "verified": True}
        with patch("verify_references.retrieve", side_effect=[({"url": source["url"], "status": 503}, b""), ({"url": github_raw_url(source["url"]), "status": 200}, b"# AI Usage Policy\n")]):
            result = check(source)
        self.assertEqual(result["identity_status"], "confirmed")
        self.assertEqual(result["observations"][1]["retrieval_method"], "official-github-raw-file")

    def test_does_not_override_missing_page_or_wrong_title(self):
        source = {"id": "policy", "url": "https://github.com/org/repo/blob/main/POLICY.md", "title": "AI Usage Policy", "verified": True}
        with patch("verify_references.retrieve", return_value=({"url": source["url"], "status": 404}, b"")) as request:
            self.assertEqual(check(source)["identity_status"], "unresolved")
            self.assertEqual(request.call_count, 1)
        with patch("verify_references.retrieve", side_effect=[({"url": source["url"], "status": 503}, b""), ({"url": github_raw_url(source["url"]), "status": 200}, b"# Unrelated Project Rules\n")]):
            self.assertEqual(check(source)["identity_status"], "unresolved")
