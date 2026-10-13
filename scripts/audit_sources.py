#!/usr/bin/env python3
"""Public-source identity checks. Reachability never implies result verification."""
import argparse
import concurrent.futures
import datetime as dt
import hashlib
import json
import re
import time
import urllib.error
import urllib.request
from html import unescape
from html.parser import HTMLParser
from pathlib import Path


class Metadata(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta = {}
        self.in_title = False
        self.title = []
        self.in_h1 = False
        self.h1 = []
        self.in_jsonld = False
        self.jsonld_text = []
        self.jsonld = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "script" and attrs.get("type", "").lower() == "application/ld+json":
            self.in_jsonld = True
            self.jsonld_text = []
        if tag == "meta":
            key = attrs.get("name", attrs.get("property", "")).lower()
            if attrs.get("content"):
                self.meta.setdefault(key, []).append(attrs["content"])
        if tag == "title":
            self.in_title = True
        if tag == "h1":
            self.in_h1 = True

    def handle_endtag(self, tag):
        if tag == "script" and self.in_jsonld:
            self.in_jsonld = False
            try:
                self.jsonld.append(json.loads("".join(self.jsonld_text)))
            except ValueError:
                pass
        if tag == "title":
            self.in_title = False
        if tag == "h1":
            self.in_h1 = False

    def handle_data(self, data):
        if self.in_jsonld:
            self.jsonld_text.append(data)
        if self.in_title:
            self.title.append(data)
        if self.in_h1:
            self.h1.append(data)


def publication_metadata(parsed, title):
    """Read only matching primary article nodes, never related links or modification dates."""
    normalize = lambda value: re.sub(r"\W+", "", unescape(value).lower())
    nodes = []
    for document in parsed.jsonld:
        entries = document if isinstance(document, list) else [document]
        for entry in entries:
            if isinstance(entry, dict):
                nodes.extend(entry.get("@graph", [entry]))
    dates, authors = set(), []
    for node in nodes:
        if not isinstance(node, dict):
            continue
        types = node.get("@type", [])
        types = [types] if isinstance(types, str) else types
        if not set(types) & {"Article", "NewsArticle", "BlogPosting", "ScholarlyArticle", "Report", "Book"}:
            continue
        heading = node.get("headline") or node.get("name") or ""
        if not isinstance(heading, str) or normalize(heading) != normalize(title):
            continue
        date = node.get("datePublished")
        if isinstance(date, str) and re.fullmatch(r"\d{4}(?:-\d{2}(?:-\d{2})?)?(?:T.*)?", date):
            dates.add(date)
        byline = node.get("author", [])
        byline = byline if isinstance(byline, list) else [byline]
        for author in byline:
            name = author.get("name") if isinstance(author, dict) else author if isinstance(author, str) else None
            if name and name not in authors:
                authors.append(name)
    return (next(iter(dates)) if len(dates) == 1 else ""), authors


def fetch(record, cache, cutoff):
    result = json.loads(json.dumps(record))
    result.setdefault("verification", {"level": "candidate", "checked_on": cutoff, "basis": "Primary metadata retrieval pending."})
    url = record["url"]
    request = urllib.request.Request(url, headers={"User-Agent": "AIIntellectualWorkReview/2026.10 (public bibliographic metadata audit)"})
    try:
        with urllib.request.urlopen(request, timeout=22) as response:
            body = response.read(6_000_000)
            result["access"] = {"status": response.status, "resolved_url": response.url, "checked_on": cutoff, "content_type": response.headers.get("Content-Type", "")}
        digest = hashlib.sha256(body).hexdigest()
        cache.mkdir(parents=True, exist_ok=True)
        suffix = ".pdf" if body.startswith(b"%PDF") else ".html"
        (cache / (record["id"] + suffix)).write_bytes(body)
        if suffix == ".pdf":
            try:
                from pypdf import PdfReader
                reader = PdfReader(cache / (record["id"] + suffix))
                result["observed_title"] = (reader.metadata.title if reader.metadata else None) or ""
                result["pdf_pages"] = len(reader.pages)
            except Exception as error:
                result["access"]["parse_note"] = type(error).__name__
        else:
            parsed = Metadata()
            parsed.feed(body.decode("utf-8", errors="replace"))
            meta = parsed.meta
            title = next((meta[k][0] for k in ["citation_title", "dc.title", "og:title"] if meta.get(k)), "".join(parsed.h1) or "".join(parsed.title))
            result["observed_title"] = re.sub(r"\s+", " ", unescape(title)).strip()
            structured_date, structured_authors = publication_metadata(parsed, result["observed_title"])
            authors = meta.get("citation_author", []) or meta.get("dc.creator", []) or structured_authors
            if authors:
                result["authors"] = authors
            date = next((meta[k][0] for k in ["citation_publication_date", "citation_date", "dc.date", "article:published_time"] if meta.get(k)), structured_date)
            if date:
                result["observed_date"] = date
            doi = next((meta[k][0] for k in ["citation_doi", "dc.identifier"] if meta.get(k)), "")
            if doi and (doi.startswith("10.") or "doi.org/" in doi):
                result["doi"] = doi.replace("https://doi.org/", "")
        title = result.get("observed_title", "")
        blocked = any(term in title.lower() for term in ["just a moment", "access denied", "subscribe to read", "robot check", "attention required", "page not found"])
        if title and not blocked:
            result["title"] = title
            result["verification"] = {"level": "identity-checked", "checked_on": cutoff, "basis": "Bibliographic identity inspected in primary-source page metadata; findings not yet appraised.", "source_url": url, "retrieved_sha256": digest}
        else:
            result["verification"] = {"level": "candidate", "checked_on": cutoff, "basis": "Source retrieved, but bibliographic identity requires editorial checking."}
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        result["access"] = {"status": getattr(error, "code", None), "error": str(error)[:180], "checked_on": cutoff}
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/intake.json"))
    parser.add_argument("--output", type=Path, default=Path("data/audit.json"))
    parser.add_argument("--cache", type=Path, default=Path("/tmp/ai-intellectual-work-source-cache"))
    parser.add_argument("--cutoff", default=dt.datetime.now(dt.timezone.utc).date().isoformat(), help="Actual metadata checking date in UTC, not the publication evidence cutoff")
    parser.add_argument("--workers", type=int, default=5)
    args = parser.parse_args()
    records = json.loads(args.input.read_text())
    output = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = [executor.submit(fetch, r, args.cache, args.cutoff) for r in records]
        for future in concurrent.futures.as_completed(futures):
            output.append(future.result())
            if len(output) % 20 == 0:
                print(f"Audited {len(output)}/{len(records)} URLs", flush=True)
    output.sort(key=lambda r: r["url"])
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    checked = sum(r["verification"]["level"] == "identity-checked" for r in output)
    print(f"Identity metadata checked: {checked}; candidates requiring attention: {len(output)-checked}")


if __name__ == "__main__":
    main()
