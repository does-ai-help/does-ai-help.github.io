#!/usr/bin/env python3
"""Report public-source availability without treating access errors as invalidity."""
import argparse
import concurrent.futures
import datetime
import json
import urllib.error
import urllib.request
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urldefrag, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class ExternalLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = set()

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in {"href", "src"} and value and value.startswith(("https://", "http://")):
                self.urls.add(urldefrag(value)[0])


def check(record):
    try:
        request = urllib.request.Request(record["url"], method="GET", headers={"User-Agent": "AIIntellectualWorkReview link monitor", "Range": "bytes=0-8191"})
        with urllib.request.urlopen(request, timeout=20) as response:
            response.read(8192)
            return {"id": record["id"], "url": record["url"], "status": response.status, "resolved_url": response.url}
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        return {"id": record["id"], "url": record["url"], "status": getattr(error, "code", None), "error": str(error)[:180]}


def is_publication_link(record, meta):
    if record['id'] not in {'publication-document-link', 'website-external-link'}:
        return False
    origin = urlsplit(meta.get('canonical_url', ''))
    if origin.netloc and urlsplit(record['url']).netloc == origin.netloc:
        return True
    github = meta.get('github_url', '').rstrip('/')
    return bool(github) and record['url'] == f"{github}/releases/tag/v{meta['version']}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("build/access-report.json"))
    parser.add_argument("--strict", action="store_true", help="Fail on confirmed 404/410 responses; other access restrictions need editorial inspection")
    parser.add_argument("--pre-deployment", action="store_true", help="Defer this publication's Pages URLs and exact current GitHub release until publication; never skip reference URLs")
    args = parser.parse_args()
    records = json.loads((ROOT / "data/sources.json").read_text())
    known = {r["url"] for r in records}
    link_manifest = ROOT / "site/downloads/external-links.json"
    if link_manifest.exists():
        for url in json.loads(link_manifest.read_text()):
            if url not in known:
                records.append({"id": "publication-document-link", "url": url})
                known.add(url)
    for page in (ROOT / "site").glob("*.html"):
        parser = ExternalLinks()
        parser.feed(page.read_text())
        for url in sorted(parser.urls - known):
            records.append({"id": "website-external-link", "url": url})
            known.add(url)
    for record in list(records):
        if record.get("doi"):
            url = "https://doi.org/" + record["doi"]
            if url not in known:
                records.append({"id": record["id"] + "-doi", "url": url})
                known.add(url)
    deferred = []
    if args.pre_deployment:
        meta = json.loads((ROOT / "data/release.json").read_text())
        deferred = [r for r in records if is_publication_link(r, meta)]
        records = [r for r in records if r not in deferred]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(check, records))
    report = {"checked_at": datetime.datetime.now(datetime.timezone.utc).isoformat(), "interpretation": "Access checks only. Failure may reflect a paywall, bot restriction, redirect, timeout or unavailable resource; it is not a scientific-validity verdict.", "deferred_publication_urls": [r["url"] for r in deferred], "records": results}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(f"Access report written: {args.output}")
    broken = [r["url"] for r in results if r.get("status") in {404, 410}]
    print(f"Checked {len(results)} unique public URLs; {len(broken)} HTTP 404/410 responses. Other failures are recorded, not classified as dead links.")
    if args.strict and broken:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
