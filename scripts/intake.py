#!/usr/bin/env python3
"""Import URLs from an existing reference list; retain only neutral English labels."""
import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


def canonical(url):
    parts = urlsplit(url.rstrip(".,)>"))
    if parts.hostname == "arxiv.org":
        match = re.search(r"/(?:abs|pdf|html)/(\d{4}\.\d{4,5})", parts.path)
        if match:
            return f"https://arxiv.org/abs/{match[1]}"
    identity_query = urlencode([(k, v) for k, v in parse_qsl(parts.query) if k.lower() in {"abstract_id", "id"}])
    return urlunsplit((parts.scheme, parts.netloc, parts.path.rstrip("/"), identity_query, ""))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    text = args.input.read_text()
    bibliography = text.split("## Bibliografia linkowana", 1)[-1]
    urls = sorted({canonical(u) for u in re.findall(r"https?://[^\s<>\)]+", bibliography)})
    records = []
    for url in urls:
        key = "ref-" + hashlib.sha256(url.encode()).hexdigest()[:10]
        records.append({"id": key, "url": url, "title": "Reference awaiting identity verification", "topics": [], "method": "not-classified", "publication_status": "not-established", "summary": "Candidate reference; no substantive conclusion is attributed before source review.", "limitations": "Result-level appraisal pending.", "verification": {"level": "candidate", "checked_on": None}})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n")
    print(f"Imported {len(records)} unique candidate URLs")


if __name__ == "__main__":
    main()
