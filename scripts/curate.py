#!/usr/bin/env python3
"""Merge checked metadata and editorial annotations into the release database."""
import hashlib
import json
import re
from pathlib import Path
from topics import classify, title_topics

ROOT = Path(__file__).resolve().parents[1]


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def load(name):
    return json.loads((ROOT / "data" / name).read_text(), object_pairs_hook=unique_object)


def topics_from_title(title):
    return title_topics(title)


def main():
    release = load("release.json")
    related = load("related-reviews.json") + load("october-followup.json") + load("browser-source-updates.json") + load("document-source-updates.json") + load("opensource-source-updates.json")
    allowed = {r["url"] for r in load("intake.json") + related}
    audit = load("audit.json") + load("audit-additions.json") + load("audit-related.json")
    records = {r["url"]: r for r in audit if r["url"] in allowed}
    rejected = []
    for url, r in list(records.items()):
        title = r.get("observed_title", "")
        if "econbiz.de" in url:
            rejected.append({"url": url, "reason": "Resolved primary metadata identifies an unrelated Dutch banking publication; inherited intended citation not verified.", "observed_title": title})
            del records[url]
            continue
        if title.lower().strip() in {"gitlab", "osf", "3 ai", "3. ai"}:
            r["verification"]["level"] = "candidate"
            r["title"] = "Reference awaiting identity verification"
    for annotation in load("editorial.json") + related:
        url = annotation["url"]
        r = records.setdefault(url, {"id": "ref-" + hashlib.sha256(url.encode()).hexdigest()[:10], "url": url})
        r.update(annotation)
        scope = annotation.get("verification_scope", "")
        level = annotation.get("verification_level", "content-checked")
        if not annotation.get("checked_on"):
            raise ValueError(f"Editorial checking date is required for {annotation['id']}")
        r["verification"] = {"level": level, "checked_on": annotation["checked_on"], "basis": scope, "source_url": url}
        r["editorial_priority"] = "core" if level == "content-checked" else "supporting" if level == "identity-checked" else "pending"
    output = []
    from browser_review import latest_receipts, receipt_errors
    browser_checks = latest_receipts(load("browser-verification.json"))
    corrections = load("bibliographic-corrections.json")
    taxonomy = load('topic-taxonomy.json')
    topic_corrections = load('topic-corrections.json')
    missing = set(topic_corrections) - {r['id'] for r in records.values()}
    if missing:
        raise ValueError(f'Unknown topic-correction IDs: {sorted(missing)}')
    for r in records.values():
        r.update(corrections.get(r["id"], {}))
        r.setdefault("authors", [])
        journals = {
            "nature.com/articles/s41586-": "Nature",
            "academic.oup.com/qje/": "The Quarterly Journal of Economics",
            "doi.org/10.1126/science.": "Science",
            "doi.org/10.1073/pnas.": "Proceedings of the National Academy of Sciences",
            "queue.acm.org/": "ACM Queue",
        }
        for pattern, journal in journals.items():
            if pattern in r["url"]:
                r.setdefault("container_title", journal)
        arxiv_identifier = re.search(r"arxiv.org/abs/(\d{4}\.\d{4,5})", r["url"])
        if arxiv_identifier:
            r["arxiv_id"] = arxiv_identifier[1]
        r.setdefault("topics", topics_from_title(r.get("title", "")))
        if not r["topics"]:
            r["topics"] = topics_from_title(r.get("title", ""))
        classify(r, taxonomy, topic_corrections)
        r.setdefault("method", "not-classified")
        r.setdefault("publication_status", "not-established")
        if r["publication_status"] == "not-established" and "arxiv.org/" in r["url"]:
            r["publication_status"] = "preprint"
        r.setdefault("date", r.get("observed_date", "").replace("/", "-")[:10] or None)
        if not r.get("year"):
            match = re.search(r"(?:19|20)\d{2}", r.get("date") or r.get("observed_date", ""))
            arxiv = re.search(r"arxiv.org/abs/(\d{2})(\d{2})\.", r["url"])
            pathyear = re.search(r"/(20\d{2})(?:/|$)", r["url"])
            r["year"] = int(match.group()) if match else int("20" + arxiv[1]) if arxiv else int(pathyear[1]) if pathyear else None
            r.setdefault("date_basis", "primary metadata" if match else "identifier or URL year; exact date not established" if r["year"] else "not established")
        r["verified"] = r.get("verification", {}).get("level") in {"identity-checked", "content-checked"}
        browser_check = browser_checks.get(r["id"])
        if browser_check and not receipt_errors(browser_check, r, release):
            r["browser_verification"] = browser_check
        r.setdefault("editorial_priority", "supporting" if r["verified"] else "pending")
        if r["editorial_priority"] != "core":
            title = r.get("title", "")
            if r["verified"]:
                r["summary"] = f"Supporting reference on {', '.join(r['topics'])}. Scope indicated by the primary-source title: {title}. Result-level appraisal is pending."
                r["limitations"] = "Bibliographic identity checked; substantive findings have not been independently appraised for this release."
            else:
                r.setdefault("summary", "Candidate reference retained for follow-up; no result is attributed in the synthesis.")
                r.setdefault("limitations", "Access or identity verification incomplete.")
        r["added_in"] = "2026-10"
        output.append(r)
    output.sort(key=lambda r: (-(r.get("year") or 0), r["title"].lower()))
    groups = [
        ["https://arxiv.org/abs/2507.09089", "https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study"],
        ["https://www.microsoft.com/en-us/research/publication/the-effects-of-generative-ai-on-high-skilled-work-evidence-from-three-field-experiments-with-software-developers", "https://pubsonline.informs.org/doi/10.1287/mnsc.2025.00535"],
        ["https://research.google/pubs/dora-2025-state-of-ai-assisted-software-development-report", "https://blog.google/innovation-and-ai/technology/developers-tools/dora-report-2025"],
        ["https://ramp.com/data/ai-jobs-impact", "https://ramp.com/data/ai-jobs-impact/paper"],
        ["https://arxiv.org/abs/2410.12944", "https://conf.researchr.org/details/icse-2025/icse-2025-software-engineering-in-practice/26/How-much-does-AI-impact-development-speed-An-enterprise-based-randomized-controlled-"],
    ]
    for group in groups:
        members = [r for r in output if r["url"] in group]
        for r in members:
            r["related_to"] = list(dict.fromkeys([*r.get("related_to", []), *[other["id"] for other in members if other["id"] != r["id"]]]))
    for r in output:
        if r["id"] == "coverage2026":
            r["dataset_family"] = "AIDev"
    (ROOT / "data" / "sources.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    (ROOT / "data" / "exclusions.json").write_text(json.dumps(rejected, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"total": len(output), "verified_identity_or_content": sum(r['verified'] for r in output), "content_checked": sum(r['verification']['level']=='content-checked' for r in output), "excluded": len(rejected)}))


if __name__ == "__main__":
    main()
