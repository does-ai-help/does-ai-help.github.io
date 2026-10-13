import copy
import datetime as dt
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from browser_review import fingerprint, latest_receipts, receipt_errors
from verify_references import apply_browser_receipt
from unittest.mock import patch


class BrowserReviewTests(unittest.TestCase):
    def setUp(self):
        self.source = {"id": "example", "title": "Generative AI at Work", "url": "https://example.org/paper", "authors": ["Smith, Alice"], "doi": "10.1234/example"}
        self.release = {"release": "2026-10"}
        self.now = dt.datetime(2026, 10, 14, tzinfo=dt.timezone.utc)
        self.receipt = {"id": "example", "method": "local-chrome-native", "release_month": "2026-10", "reviewer": "AI-assisted editor", "scope": "Title and byline only", "notes": "Full text not read", "source_url": self.source["url"], "source_fingerprint": fingerprint(self.source), "checked_at": "2026-10-13T09:00:00+00:00", "outcome": "identity-confirmed", "observed": {"title": self.source["title"], "authors": self.source["authors"], "doi": self.source["doi"], "resolved_url": self.source["url"]}}

    def test_current_receipt(self):
        self.assertEqual(receipt_errors(self.receipt, self.source, self.release, self.now), [])

    def test_next_month_requires_fresh_inspection(self):
        self.assertTrue(receipt_errors(self.receipt, self.source, {"release": "2026-11"}, self.now))

    def test_citation_change_invalidates_receipt(self):
        source = dict(self.source, title="Another research paper")
        self.assertTrue(receipt_errors(self.receipt, source, self.release, self.now))

    def test_old_future_and_unzoned_receipts(self):
        for timestamp in ["2026-08-13T09:00:00+00:00", "2026-10-15T09:00:00+00:00", "2026-10-13T09:00:00"]:
            self.assertTrue(receipt_errors(dict(self.receipt, checked_at=timestamp), self.source, self.release, self.now))

    def test_wrong_method_not_a_chrome_inspection(self):
        self.assertTrue(receipt_errors(dict(self.receipt, method="headless-playwright"), self.source, self.release, self.now))

    def test_conflicting_doi_or_authors_rejected(self):
        for key, value in [("doi", "10.1234/wrong"), ("authors", ["Jones, Bob"]), ("title", "An unrelated work")]:
            receipt = copy.deepcopy(self.receipt)
            receipt["observed"][key] = value
            self.assertTrue(receipt_errors(receipt, self.source, self.release, self.now))

    def test_redirect_requires_explanation(self):
        receipt = copy.deepcopy(self.receipt)
        receipt["observed"]["resolved_url"] = "https://other.example/article"
        self.assertTrue(receipt_errors(receipt, self.source, self.release, self.now))
        receipt["redirect_basis"] = "Observed publisher redirect in Chrome"
        self.assertEqual(receipt_errors(receipt, self.source, self.release, self.now), [])

    def test_access_blocked_is_attempt_not_identity_confirmation(self):
        receipt = dict(self.receipt, outcome="access-blocked", observed={})
        self.assertEqual(receipt_errors(receipt, self.source, self.release, self.now), [])
        self.assertNotEqual(receipt["outcome"], "identity-confirmed")

    def test_history_selects_latest_without_destroying_older_receipt(self):
        old = dict(self.receipt, checked_at="2026-10-12T09:00:00+00:00")
        history = {"checks": [self.receipt, old]}
        self.assertEqual(latest_receipts(history)["example"], self.receipt)
        self.assertEqual(len(history["checks"]), 2)

    @patch("browser_review.receipt_errors", return_value=[])
    def test_browser_confirmation_never_overrides_automated_mismatch(self, validate):
        result = {"identity_status": "mismatch", "conflicts": ["DOI conflict"]}
        self.assertEqual(apply_browser_receipt(result, self.receipt, self.source, self.release)["identity_status"], "mismatch")

    @patch("browser_review.receipt_errors", return_value=[])
    def test_access_blocked_never_clears_unresolved_identity(self, validate):
        result = {"identity_status": "unresolved", "conflicts": []}
        receipt = dict(self.receipt, outcome="access-blocked")
        self.assertEqual(apply_browser_receipt(result, receipt, self.source, self.release)["identity_status"], "unresolved")

    @patch("browser_review.receipt_errors", return_value=[])
    def test_current_confirmed_receipt_clears_unresolved_only(self, validate):
        result = {"identity_status": "unresolved", "conflicts": []}
        self.assertEqual(apply_browser_receipt(result, self.receipt, self.source, self.release)["identity_status"], "browser-confirmation")

    @patch("browser_review.receipt_errors", return_value=[])
    def test_browser_missing_source_blocks_prior_automatic_confirmation(self, validate):
        result = {"identity_status": "confirmed", "conflicts": []}
        self.assertEqual(apply_browser_receipt(result, dict(self.receipt, outcome="not-found"), self.source, self.release)["identity_status"], "mismatch")


if __name__ == "__main__":
    unittest.main()
