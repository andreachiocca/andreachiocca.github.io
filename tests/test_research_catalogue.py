"""Offline regression checks for catalogue discovery and safe refreshes."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("catalogue", Path(__file__).parents[1] / "scripts/sync_research_outputs.py")
catalogue = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalogue)


def deposit(record_id, concept="10", date="2026-01-01", orcid=catalogue.ORCID, owner="275783", name="Chiocca, Andrea"):
    return {"id": record_id, "conceptrecid": concept, "owners": [{"id": owner}],
            "metadata": {"title": "Test dataset", "publication_date": date, "doi": "10.5281/zenodo." + str(record_id),
                         "creators": [{"name": name, "orcid": orcid}], "access_right": "open", "resource_type": {"type": "dataset", "title": "Dataset"}}}


class DiscoveryTests(unittest.TestCase):
    def test_github_pagination_does_not_stop_after_first_full_page(self):
        with patch.object(catalogue, "fetch", side_effect=[[{"id": 1}] * 100, [{"id": 2}]]) as fetch:
            records = catalogue.github_repositories("achiocca1")
        self.assertEqual(len(records), 101)
        self.assertIn("page=2", fetch.call_args.args[0])

    def test_zenodo_follows_next_link(self):
        first = {"hits": {"hits": [deposit(11)], "total": 2}, "links": {"next": "https://zenodo.org/api/records?page=2"}}
        second = {"hits": {"hits": [deposit(12)], "total": 2}, "links": {}}
        with patch.object(catalogue, "fetch", side_effect=[first, second]) as fetch:
            self.assertEqual(len(catalogue.zenodo_search("test")), 2)
        self.assertEqual(fetch.call_count, 2)

    def test_incomplete_search_fails_instead_of_publishing_partial_results(self):
        with patch.object(catalogue, "fetch", return_value={"hits": {"hits": [deposit(11)], "total": 2}, "links": {}}):
            with self.assertRaises(ValueError):
                catalogue.zenodo_search("test")

    def test_identity_rejects_same_surname_or_conflicting_orcid(self):
        self.assertTrue(catalogue.verified_deposit(deposit(11)))
        self.assertTrue(catalogue.verified_deposit(deposit(11, orcid=None)))
        self.assertFalse(catalogue.verified_deposit(deposit(11, orcid=None, name="Chiocca, Other")))
        self.assertFalse(catalogue.verified_deposit(deposit(11, orcid="0000-0000-0000-0001")))
        self.assertFalse(catalogue.verified_deposit(deposit(11, orcid=None, owner="other")))

    def test_versions_group_by_concept_and_keep_all_version_links(self):
        records = [deposit(11), deposit(12, date="2026-02-01"), deposit(21, concept="20")]
        groups = catalogue.group_versions(records)
        self.assertEqual(len(groups), 2)
        self.assertEqual(groups["10"][0]["id"], 12)
        self.assertEqual(len(groups["10"]), 2)

    def test_restricted_access_and_curated_science_survive_refresh(self):
        original = {"id": "stable-anchor", "title": "Old title", "kind": "data", "description": "Reviewed scientific scope.", "scope_note": "Important limitation.", "related_publications": ["ExistingKey"]}
        record = deposit(11)
        record["metadata"]["access_right"] = "restricted"
        result = catalogue.zenodo_entry([record], original)
        self.assertEqual(result["id"], "stable-anchor")
        self.assertEqual(result["description"], original["description"])
        self.assertEqual(result["scope_note"], original["scope_note"])
        self.assertEqual(result["access_right"], "restricted")
        self.assertEqual(result["related_publications"], ["ExistingKey"])

    def test_network_failure_preserves_checked_in_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "catalogue.json"
            target.write_text('[{"id":"existing"}]', encoding="utf8")
            before = target.read_bytes()
            with patch.object(catalogue, "build_catalogue", side_effect=OSError("service unavailable")):
                with self.assertRaises(OSError):
                    catalogue.refresh(target, Path(directory) / "status.json")
            self.assertEqual(target.read_bytes(), before)

    def test_manually_verified_github_archive_pair_remains_one_card(self):
        repo = {"full_name": "andreachiocca/test", "name": "test", "html_url": "https://github.com/andreachiocca/test", "size": 0, "fork": False, "archived": False}
        existing = {"id": "stable-software", "title": "Test software", "kind": "software", "description": "Reviewed scope.", "url": "https://zenodo.org/records/11", "github_full_name": repo["full_name"], "zenodo_concept_id": "10"}
        with patch.object(catalogue, "github_repositories", side_effect=[[repo], []]), patch.object(catalogue, "zenodo_search", return_value=[deposit(11)]), patch.object(catalogue, "REQUIRED_RECORDS", {11}):
            entries, status = catalogue.build_catalogue([existing])
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["github_url"], repo["html_url"])
        self.assertEqual(entries[0]["zenodo_record_id"], "11")
        self.assertEqual(entries[0]["description"], "Reviewed scope.")

    def test_catalogue_covers_every_repository_and_deposit_version(self):
        root = Path(__file__).parents[1]
        entries = json.loads((root / "_data/research_outputs.json").read_text(encoding="utf8"))
        status = json.loads((root / "_data/catalogue_status.json").read_text(encoding="utf8"))
        catalogue.validate_catalogue(entries, status["github_full_names"], status["zenodo_record_ids"])
        self.assertEqual(len(entries), len({item["id"] for item in entries}))


if __name__ == "__main__":
    unittest.main()
