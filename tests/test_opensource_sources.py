import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class OpenSourceSourceTests(unittest.TestCase):
    def setUp(self):
        self.records = {r["id"]: r for r in json.loads((ROOT / "data/sources.json").read_text())}

    def test_policies_are_checked_not_experiments(self):
        for key in ["gimppolicy2026", "netbsdpolicy2024", "zigpolicy2026", "redoxpolicy2026", "asahipolicy2026", "linuxgenerated2026", "linuxassistants2026", "gravitypolicy2026"]:
            with self.subTest(key=key):
                self.assertEqual(self.records[key]["method"], "project-policy")
                self.assertEqual(self.records[key]["verification"]["level"], "content-checked")

    def test_related_studies_not_independent_replications(self):
        self.assertEqual(self.records["horapolicies2026"]["study_family"], self.records["horapoliciesearly2026"]["study_family"])
        self.assertIn("horapoliciesearly2026", self.records["horapolicies2026"]["related_to"])

    def test_repository_dates_have_pinned_provenance(self):
        dates = {"asahipolicy2026": "2026-09-08", "zigpolicy2026": "2025-11-22", "gravitypolicy2026": "2026-09-15", "gravityabout2026": "2026-09-12"}
        for key, date in dates.items():
            record = self.records[key]
            self.assertEqual(record["date"], date)
            self.assertIn(record["source_revision"]["commit"], record["source_revision"]["file_url"])
            self.assertEqual(record["source_revision"]["checked_on"], "2026-10-13")

    def test_authored_and_committed_dates_stay_distinct(self):
        source = self.records["gravitypolicy2026"]
        self.assertEqual(source["source_revision"]["authored_at"][:10], "2026-09-12")
        self.assertEqual(source["source_revision"]["committed_at"][:10], source["date"])
        self.assertEqual(source["date_kind"], "git-file-revision")

    def test_pdf_repository_urls_are_breakable(self):
        tex = (ROOT / "latex/body.tex").read_text()
        self.assertIn(r"\url{" + self.records['redoxpolicy2026']['url'] + '}', tex)
        # Detailed source-revision provenance belongs to the evidence record.
        self.assertIn('03d6b8bc05bab7cf03490671cd3d23571214a720',
                      self.records['redoxpolicy2026']['version_note'])

    def test_qemu_introduction_date(self):
        self.assertEqual(self.records["qemupolicy2026"]["date"], "2025-06-24")
        self.assertIn("committed", self.records["qemupolicy2026"]["date_basis"])

    def test_swebench_conference_preprint_and_repository_distinct(self):
        recommended = (ROOT / "data/swebench-recommended.bib").read_text()
        self.assertIn("@inproceedings{jimenez2024swebench", recommended)
        self.assertIn("year={2024}", recommended)
        self.assertIn("booktitle={The Twelfth International Conference", recommended)
        self.assertEqual(self.records["ref-3e4a5dea3a"]["year"], 2023)
        self.assertEqual(self.records["ref-8ecd8d70a1"]["date"], "2026-09-01")


if __name__ == "__main__":
    unittest.main()
