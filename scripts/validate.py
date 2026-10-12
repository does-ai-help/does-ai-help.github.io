#!/usr/bin/env python3
"""Validate release consistency, citations, local links, exports and snapshots."""
import csv
import hashlib
import json
import re
import zipfile
import argparse
import datetime as dt
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids = [], set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag in {"a", "link"} and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag in {"img", "script"} and attrs.get("src"):
            self.links.append(attrs["src"])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", type=Path, help="Require a complete matching identity audit no older than seven days")
    args = parser.parse_args()
    errors = []
    records = json.loads((ROOT / "data/sources.json").read_text())
    release = json.loads((ROOT / "data/release.json").read_text())
    if args.audit:
        audit = json.loads(args.audit.read_text())
        if audit.get("database_sha256") != hashlib.sha256((ROOT / "data/sources.json").read_bytes()).hexdigest():
            errors.append("Identity audit does not match the current database")
        age = dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(audit["checked_at"])
        if age.total_seconds() < 0 or age.days > 7 or not audit.get("complete") or audit.get("blocking_ids"):
            errors.append("Identity audit is incomplete, stale, future-dated, or has unresolved release blockers")
    ids = [r["id"] for r in records]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate source IDs")
    urls = [r["url"] for r in records]
    if len(urls) != len(set(urls)):
        errors.append("Duplicate canonical source URLs")
    byid = {r["id"]:r for r in records}
    for r in records:
        if (r.get('year') or 0) > int(release['cutoff'][:4]):
            errors.append(f"Future or misparsed publication year: {r['id']}")
        for key in ["title", "summary", "limitations", "verification", "authors", "topics", "method", "publication_status"]:
            if key not in r:
                errors.append(f"Missing {key}: {r['id']}")
        if r['verified'] != (r['verification']['level'] in {'identity-checked','content-checked'}):
            errors.append(f"Inconsistent verification flag: {r['id']}")
        if r['editorial_priority']=='core' and r['verification']['level']!='content-checked':
            errors.append(f"Unappraised core source: {r['id']}")
        for related in r.get('related_to',[]):
            if related not in byid:
                errors.append(f"Missing related source: {related}")
    article = (ROOT / "manuscript/article.md").read_text()
    cited = set(k.strip().lstrip('@') for group in re.findall(r'\[@([^\]]+)\]', article) for k in group.split(';'))
    for key in cited:
        if key not in byid or byid[key]['verification']['level']!='content-checked':
            errors.append(f"Missing or unappraised citation: {key}")
    pages = {}
    for p in (ROOT / "site").glob("*.html"):
        parser = Links()
        parser.feed(p.read_text())
        pages[p.resolve()] = parser
    for p, parsed in pages.items():
        for link in parsed.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            target = (p.parent / unquote(url.path)).resolve() if url.path else p
            if not target.exists():
                errors.append(f"Missing local resource: {p.name}: {link}")
            if url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                errors.append(f"Missing anchor: {p.name}: {link}")
    downloads = ROOT / "site/downloads"
    if json.loads((downloads / "sources.json").read_text()) != records:
        errors.append("Published evidence JSON differs from the canonical database")
    if (downloads / "article.md").read_text() != article:
        errors.append("Published manuscript differs from the canonical manuscript")
    published_release = json.loads((downloads / "release.json").read_text())
    if any(published_release.get(key) != value for key, value in release.items()):
        errors.append("Published author/release metadata differs from the release manifest")
    csl = json.loads((downloads / "bibliography.csl.json").read_text())
    verified = {r['id'] for r in records if r['verified']}
    if {r['id'] for r in csl} != verified:
        errors.append("CSL export does not match checked records")
    if len(list(csv.DictReader((downloads/'sources.csv').open()))) != len(records):
        errors.append("CSV row count differs from database")
    if len((downloads/'sources.jsonl').read_text().splitlines()) != len(records):
        errors.append("JSONL row count differs from database")
    pdf = downloads / f"ai-intellectual-work-{release['release']}.pdf"
    if not pdf.exists() or not pdf.read_bytes().startswith(b'%PDF'):
        errors.append("PDF missing or invalid header")
    for line in (downloads / "checksums.sha256").read_text().splitlines():
        digest, name = line.split('  ',1)
        if hashlib.sha256((downloads / name).read_bytes()).hexdigest()!=digest:
            errors.append(f"Checksum mismatch: {name}")
    archive = downloads / f"release-{release['release']}.zip"
    with zipfile.ZipFile(archive) as bundle:
        if len(bundle.namelist()) != len(set(bundle.namelist())):
            errors.append("Duplicate release ZIP member names")
        if bundle.testzip():
            errors.append("Release ZIP integrity failure")
    try:
        import jsonschema
        jsonschema.validate(records,json.loads((ROOT/'data/source-schema.json').read_text()))
    except ImportError:
        print("Optional JSON Schema package unavailable; structural checks completed.")
    except Exception as error:
        errors.append(f"Schema validation: {error}")
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f"Validated {len(records)} records, {len(verified)} checked identities, {len(cited)} article citations, all local resources and release checksums.")


if __name__ == "__main__":
    main()
