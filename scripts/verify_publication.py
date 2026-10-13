#!/usr/bin/env python3
"""Check deployed pages and downloads after CDN propagation, without credentials."""
import json
import time
import urllib.request
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
meta = json.loads((ROOT / "data/release.json").read_text())
base = meta["canonical_url"]
paths = ["", "bibliography.html", "releases.html", f"downloads/does-ai-help-{meta['release']}.pdf", "downloads/bibliography.csl.json", "downloads/" + meta.get("archive_name", f"release-{meta['release']}.zip")]
for path in paths:
    error = None
    for attempt in range(5):
        try:
            with urllib.request.urlopen(urljoin(base, path), timeout=30) as response:
                body = response.read()
                if response.status != 200 or not body:
                    raise ValueError("Empty or unsuccessful publication response")
            if path.endswith(".pdf") and not body.startswith(b"%PDF"):
                raise ValueError("PDF URL does not return a PDF")
            if path.endswith(".zip") and not body.startswith(b"PK"):
                raise ValueError("Archive URL does not return a ZIP")
            if path.endswith(".json"):
                json.loads(body)
            if not path and meta["title"] not in body.decode("utf-8"):
                raise ValueError("Homepage title does not match this publication")
            error = None
            break
        except (OSError, ValueError) as failure:
            error = failure
            if attempt < 4:
                time.sleep(15)
    if error:
        raise SystemExit(f"Publication check failed: {urljoin(base, path)}: {error}")
    print(f"Verified deployed resource: {path or 'homepage'}", flush=True)
