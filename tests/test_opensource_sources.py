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

    def test_unknown_adoption_dates_not_observation_dates(self):
        for key in ["asahipolicy2026", "zigpolicy2026", "gravitypolicy2026", "gravityabout2026"]:
            self.assertIsNone(self.records[key]["date"])

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
