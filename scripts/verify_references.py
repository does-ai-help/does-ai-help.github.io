#!/usr/bin/env python3
"""Compare citation identities with live primary metadata; never verify findings."""
import argparse
import concurrent.futures
import csv
import datetime as dt
import hashlib
import io
import json
import re
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import threading
import time
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

from audit_sources import Metadata

ROOT = Path(__file__).resolve().parents[1]
BLOCKED = ("just a moment", "access denied", "page not found", "not found", "robot check", "attention required", "subscribe to read", "verify you are human", "client challenge", "checking your browser")
REGISTRY_LOCK = threading.Lock()
REGISTRY_NEXT = 0.0


def normal(text):
    text = unicodedata.normalize("NFKD", text).casefold()
    return " ".join(re.findall(r"[^\W_]+", text, re.UNICODE))


def title_match(expected, observed):
    a, b = normal(expected), normal(observed)
    if not a or not b or len(a.split()) < 3 or any(t in b for t in BLOCKED):
        return False, 0.0
    if a == b or (len(a) >= 12 and a in b and b.startswith(a + " ")):
        return True, 1.0
    score = SequenceMatcher(None, a, b).ratio()
    # Word order alone is insufficient: a shuffled unrelated title must not pass.
    overlap = len(set(a.split()) & set(b.split())) / max(1, len(set(a.split())))
    return score >= .91 and overlap >= .85, round(score, 3)


def doi_normal(value):
    return re.sub(r"^https?://(?:dx\.)?doi\.org/|^doi:\s*", "", value or "", flags=re.I).strip().lower()


def retrieve_once(url):
    result = {"url": url}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "AIIntellectualWorkReview/2026.10 citation identity audit"})
        with urllib.request.urlopen(req, timeout=25) as response:
            body = response.read(12_000_001)
            result.update(status=response.status, resolved_url=response.url,
                          content_type=response.headers.get("Content-Type", ""),
                          sha256=hashlib.sha256(body).hexdigest())
        if len(body) > 12_000_000:
            result["error"] = "Response exceeds 12 MB metadata inspection limit"
            return result, b""
        return result, body
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        result.update(status=getattr(error, "code", None), error=str(error)[:240])
        return result, b""


def retrieve(url):
    global REGISTRY_NEXT
    for attempt in range(3):
        if urllib.parse.urlsplit(url).netloc in {"api.crossref.org", "api.datacite.org"}:
            with REGISTRY_LOCK:
                time.sleep(max(0, REGISTRY_NEXT - time.monotonic()))
                REGISTRY_NEXT = time.monotonic() + 1.0
        access, body = retrieve_once(url)
        if access.get("status") not in {429, 500, 502, 503, 504}:
            return access, body
        if attempt < 2:
            time.sleep(3 * (attempt + 1))
    return access, body


def page_metadata(body):
    if not body:
        return {}
    if body.startswith(b"%PDF"):
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(body))
            text = "\n".join(page.extract_text() or "" for page in reader.pages[:2])
            return {"titles": [str(reader.metadata.title or "")] if reader.metadata else [], "pdf_identity_text": text[:18000]}
        except Exception as error:
            return {"parse_error": f"PDF: {type(error).__name__}"}
    class PageMetadata(Metadata):
        def __init__(self):
            super().__init__()
            self.title_groups, self.h1_groups = [], []

        def handle_starttag(self, tag, attrs):
            if tag == "title":
                self.title = []
            if tag == "h1":
                self.h1 = []
            super().handle_starttag(tag, attrs)

        def handle_endtag(self, tag):
            if tag == "title":
                self.title_groups.append("".join(self.title))
            if tag == "h1":
                self.h1_groups.append("".join(self.h1))
            super().handle_endtag(tag)

    parser = PageMetadata()
    parser.feed(body.decode("utf-8", errors="replace"))
    m = parser.meta
    titles = [v for key in ("citation_title", "dc.title", "og:title") for v in m.get(key, [])]
    titles += parser.h1_groups + parser.title_groups
    return {"titles": list(dict.fromkeys(t for t in titles if t)),
            "authors": m.get("citation_author", []) or m.get("dc.creator", []),
            "dates": m.get("citation_publication_date", []) or m.get("citation_date", []) or m.get("dc.date", []),
            "doi": next((v for key in ("citation_doi", "dc.identifier") for v in m.get(key, []) if v.startswith("10.") or "doi.org/" in v), "")}


def registry_metadata(doi):
    observations = []
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="")
    access, body = retrieve(url)
    if body:
        try:
            m = json.loads(body)["message"]
            observations.append({"access": access, "titles": m.get("title", []), "doi": m.get("DOI", ""),
                                 "authors": [f"{a.get('family', '')}, {a.get('given', '')}" for a in m.get("author", [])],
                                 "dates": [str(m[k]["date-parts"][0][0]) for k in ("published", "published-online", "published-print") if m.get(k, {}).get("date-parts")]})
            return observations
        except (ValueError, KeyError, TypeError):
            access["error"] = "Unrecognized registry response"
    observations.append({"access": access})
    access, body = retrieve("https://api.datacite.org/dois/" + urllib.parse.quote(doi, safe=""))
    if body:
        try:
            m = json.loads(body)["data"]["attributes"]
            observations.append({"access": access, "titles": [t["title"] for t in m.get("titles", [])], "doi": m.get("doi", ""),
                                 "authors": [a.get("name", "") for a in m.get("creators", [])], "dates": [str(m.get("publicationYear", ""))]})
            return observations
        except (ValueError, KeyError, TypeError):
            access["error"] = "Unrecognized registry response"
    observations.append({"access": access})
    return observations


def check(record):
    access, body = retrieve(record["url"])
    page = {"access": access, **page_metadata(body)}
    if page.get("titles") and all(any(term in normal(t) for term in BLOCKED) for t in page["titles"]):
        page["access"]["restriction"] = "Challenge or unavailable page; HTTP success does not establish page identity"
    observations = [page]
    embedded = re.search(r"https://link\.springer\.com/(?:book|article)/(10\.[^?#]+)", record["url"])
    doi = doi_normal(record.get("doi", "") or (urllib.parse.unquote(embedded[1]) if embedded else ""))
    if doi:
        observations += registry_metadata(doi)
        # Test the persistent landing link independently from registry identity.
        resolver, _ = retrieve("https://doi.org/" + doi)
        observations.append({"access": resolver})
    titles = [record["title"], *record.get("title_aliases", [])]
    matches, conflicts, warnings = [], [], []
    nature = re.search(r"https://www\.nature\.com/articles/([^/?#]+)", record["url"])
    if doi and nature and doi.split("/", 1)[-1] != nature[1].lower():
        conflicts.append("Nature article URL identifier differs from the declared DOI")
    for obs in observations:
        observed_doi = doi_normal(obs.get("doi", ""))
        if doi and observed_doi and doi != observed_doi:
            conflicts.append("Declared DOI differs from primary/registry DOI")
        comparisons = [(title_match(a, b), b) for a in titles for b in obs.get("titles", [])]
        best = max(comparisons, key=lambda pair: pair[0][1], default=((False, 0), ""))
        obs["title_score"] = best[0][1]
        obs["matched_title"] = best[1] if best[0][0] else None
        pdf_text = normal(obs.get("pdf_identity_text", ""))
        pdf_match = any(len(normal(t)) >= 24 and normal(t) in pdf_text for t in titles)
        if best[0][0] or pdf_match:
            matches.append(obs)
            obs["identity_basis"] = "PDF opening-page title text" if pdf_match else "primary/registry title match"
        elif obs.get("titles") and not all(any(term in normal(t) for term in BLOCKED) for t in obs["titles"]):
            # Low similarity is a review flag, not proof of an unrelated work.
            warnings.append("Title mismatch requires review: " + str(obs["access"]["url"]))
            if observed_doi and doi and obs["access"]["url"].startswith(("https://api.crossref.org/", "https://api.datacite.org/")):
                conflicts.append("DOI registry title does not match the cited work or a documented title alias")
        if obs.get("dates") and record.get("year"):
            years = [int(m.group()) for d in obs["dates"] if (m := re.search(r"\b(?:19|20)\d{2}\b", d))]
            if years and record["year"] not in years:
                warnings.append("Date/version differs from recorded year: " + str(years))
        if obs.get("authors") and record.get("authors"):
            expected = {normal(a.split(",")[0]) if "," in a else normal(a).split()[-1] for a in record["authors"]}
            found = {normal(a.split(",")[0]) if "," in a else normal(a).split()[-1] for a in obs["authors"] if normal(a)}
            if expected and found and not expected & found:
                warnings.append("No author-family match; inspect authorship/version")
        # Retain metadata, not third-party document text, in the public audit.
        obs.pop("pdf_identity_text", None)
    status = "mismatch" if conflicts else "confirmed" if matches else "unresolved"
    if page.get("titles") and not page.get("identity_basis") and any("Title mismatch" in w and record["url"] in w for w in warnings):
        status = "unresolved" if not conflicts else "mismatch"
    if any("No author-family match" in w for w in warnings):
        status = "mismatch" if conflicts else "unresolved"
    arxiv_id = record.get("arxiv_id")
    if arxiv_id:
        resolved = access.get("resolved_url", "")
        identifier = re.search(r"arxiv\.org/(?:abs|html|pdf)/([^/?#]+)", resolved)
        if identifier and identifier[1].removesuffix(".pdf").split("v")[0] != arxiv_id.split("v")[0]:
            status = "mismatch"
            conflicts.append("Redirect changed the arXiv identifier")
    return {"id": record["id"], "expected_title": record["title"], "url": record["url"],
            "doi": doi or None, "arxiv_id": arxiv_id, "checked_reference": bool(record.get("verified")),
            "identity_status": status, "conflicts": conflicts, "warnings": sorted(set(warnings)), "observations": observations}


def exception_valid(exception, result, today):
    try:
        lifespan = dt.date.fromisoformat(exception["expires_on"]) - dt.date.fromisoformat(exception["checked_on"])
        if not 0 < lifespan.days <= 31:
            return False
    except (KeyError, ValueError, TypeError):
        return False
    return bool(result["identity_status"] == "unresolved" and exception.get("reviewer") and exception.get("reason")
                and exception.get("evidence_url") and exception.get("observed_title")
                and exception.get("expected_title") == result["expected_title"]
                and exception.get("url") == result["url"]
                and exception.get("checked_on", "9999") <= today <= exception.get("expires_on", "")
                and title_match(result["expected_title"], exception["observed_title"])[0])


def apply_browser_receipt(result, receipt, source, release):
    from browser_review import receipt_errors
    if receipt and not receipt_errors(receipt, source, release):
        result["alternative_review"] = receipt
        if receipt["outcome"] in {"mismatch", "not-found"}:
            result.update(identity_status="mismatch")
            result["conflicts"].append("Local Chrome inspection found an identity failure")
        elif receipt["outcome"] == "identity-confirmed" and result["identity_status"] == "unresolved":
            result.update(identity_status="browser-confirmation")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="Exit nonzero for unresolved checked identities or any mismatch")
    parser.add_argument("--workers", type=int, default=5)
    parser.add_argument("--output", type=Path, default=ROOT / "build/reference-verification.json")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--retry-unresolved", action="store_true", help="Retry unresolved identities using a complete same-database audit from the last 24 hours")
    args = parser.parse_args()
    database_bytes = (ROOT / "data/sources.json").read_bytes()
    records = json.loads(database_bytes)
    all_records = records
    previous = None
    if args.retry_unresolved:
        previous = json.loads(args.output.read_text())
        age = dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(previous["checked_at"])
        if not previous.get("complete") or previous.get("database_sha256") != hashlib.sha256(database_bytes).hexdigest() or not 0 <= age.total_seconds() <= 86400:
            raise SystemExit("Retry requires a complete matching audit no older than 24 hours; run a fresh full audit")
        retry_ids = {r["id"] for r in previous["records"] if r["identity_status"] in {"unresolved", "mismatch"}}
        records = [r for r in records if r["id"] in retry_ids]
    if args.limit:
        records = records[:args.limit]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(check, records))
    if previous:
        new = {r["id"]: r for r in results}
        results = [new.get(r["id"], r) for r in previous["records"]]
    today = dt.datetime.now(dt.timezone.utc).date().isoformat()
    from browser_review import latest_receipts
    release = json.loads((ROOT / "data/release.json").read_text())
    browser_checks = latest_receipts(json.loads((ROOT / "data/browser-verification.json").read_text()))
    byid = {r["id"]: r for r in all_records}
    exceptions = {e["id"]: e for e in json.loads((ROOT / "data/identity-exceptions.json").read_text())}
    for result in results:
        receipt = browser_checks.get(result["id"])
        apply_browser_receipt(result, receipt, byid[result["id"]], release)
        ex = exceptions.get(result["id"], {})
        if exception_valid(ex, result, today):
            result.update(identity_status="manual-confirmation", manual_review=ex)
    # DOI duplicates may be related versions, but unrelated identities need inspection.
    duplicates = []
    groups = {}
    for r in all_records:
        if r.get("doi"):
            groups.setdefault(doi_normal(r["doi"]), []).append(r)
    for doi, group in groups.items():
        if len(group) > 1:
            duplicates.append({"doi": doi, "ids": [r["id"] for r in group]})
    failures = [r["id"] for r in results if r["identity_status"] == "mismatch" or (r["checked_reference"] and r["identity_status"] == "unresolved")]
    fingerprint = hashlib.sha256(database_bytes).hexdigest()
    report = {"checked_at": previous["checked_at"] if previous else dt.datetime.now(dt.timezone.utc).isoformat(), "retry_completed_at": dt.datetime.now(dt.timezone.utc).isoformat() if previous else None, "scope": "Live access and bibliographic identity, not scientific validity or claim support. Similarity checks can miss errors; substantive and version warnings require editorial review.",
              "database_sha256": fingerprint, "complete": len(results) == len(all_records), "counts": dict(Counter(r["identity_status"] for r in results)),
              "blocking_ids": failures, "duplicate_dois": duplicates, "records": results}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    with args.output.with_suffix(".csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["id", "identity_status", "title", "url", "doi", "warnings"])
        writer.writerows([r["id"], r["identity_status"], r["expected_title"], r["url"], r["doi"], "; ".join(r["conflicts"] + r["warnings"])] for r in results)
    args.output.with_suffix(".md").write_text("# Reference identity audit\n\nChecked: " + report["checked_at"] + "\n\n" + report["scope"] + "\n\nCounts: " + str(report["counts"]) + "\n\nBlocking IDs: " + (", ".join(failures) or "none") + "\n\nSee the accompanying JSON/CSV for observed metadata, redirects, access failures and warnings.\n")
    print(json.dumps({k: report[k] for k in ("counts", "complete", "blocking_ids")}, indent=2))
    if args.strict and (failures or not report["complete"]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
