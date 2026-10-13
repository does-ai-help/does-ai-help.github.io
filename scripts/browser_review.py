#!/usr/bin/env python3
"""Prepare local Chrome review tasks and validate explicit editorial receipts.

This script never controls a browser, authenticates, or invents observations.
The local reviewer uses connected Chrome UI tools and records what was seen.
"""
import argparse
import datetime as dt
import hashlib
import html
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
METHOD = "local-chrome-native"


def fingerprint(record):
    fields = {key: record.get(key) for key in ("id", "title", "url", "doi", "authors")}
    return hashlib.sha256(json.dumps(fields, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def receipt_errors(receipt, source, release, now=None):
    now = now or dt.datetime.now(dt.timezone.utc)
    errors = []
    for key in ("reviewer", "scope", "notes", "source_fingerprint", "checked_at", "source_url"):
        if not receipt.get(key):
            errors.append(f"Missing {key}")
    if receipt.get("method") != METHOD:
        errors.append("Not a local Chrome observation")
    if receipt.get("release_month") != release["release"]:
        errors.append("Browser inspection must be repeated for this release month")
    if receipt.get("source_url") != source["url"] or receipt.get("source_fingerprint") != fingerprint(source):
        errors.append("Receipt does not match the current citation identity")
    try:
        checked = dt.datetime.fromisoformat(receipt["checked_at"])
        if checked.tzinfo is None or not 0 <= (now - checked).total_seconds() <= 31 * 86400:
            errors.append("Browser inspection is future-dated, unzoned or older than 31 days")
        if checked.strftime("%Y-%m") != release["release"]:
            errors.append("Inspection date is outside the release month")
    except (KeyError, TypeError, ValueError):
        errors.append("Invalid browser inspection timestamp")
    if receipt.get("outcome") not in {"identity-confirmed", "access-blocked", "not-found", "mismatch"}:
        errors.append("Invalid inspection outcome")
    observed = receipt.get("observed", {})
    if receipt.get("outcome") == "identity-confirmed":
        from verify_references import doi_normal, normal, title_match
        titles = [source["title"], *source.get("title_aliases", [])]
        title = observed.get("title", "")
        if not title or not any(normal(t) == normal(title) or title_match(t, title)[0] for t in titles):
            errors.append("Observed title does not match the citation or an explicit alias")
        resolved = urlsplit(observed.get("resolved_url", ""))
        if resolved.scheme != "https" or not resolved.netloc:
            errors.append("Missing observed HTTPS source address")
        expected = urlsplit(source["url"])
        same_page = (resolved.netloc.removeprefix("www.") == expected.netloc.removeprefix("www.")
                     and resolved.path.rstrip("/") == expected.path.rstrip("/"))
        if not same_page and not receipt.get("redirect_basis"):
            errors.append("Changed source address needs an explicitly observed redirect explanation")
        expected_doi, found_doi = doi_normal(source.get("doi")), doi_normal(observed.get("doi"))
        if expected_doi and found_doi and expected_doi != found_doi:
            errors.append("Browser observation conflicts with the declared DOI")
        if source.get("authors") and observed.get("authors"):
            families = lambda authors: {normal(a.split(",")[0]) if "," in a else normal(a).split()[-1] for a in authors if normal(a)}
            if not families(source["authors"]) & families(observed["authors"]):
                errors.append("Browser-observed authors conflict with the citation")
    return errors


def latest_receipts(document):
    output = {}
    for receipt in document["checks"]:
        if receipt["id"] not in output or receipt["checked_at"] > output[receipt["id"]]["checked_at"]:
            output[receipt["id"]] = receipt
    return output


def load_context():
    data = ROOT / "data"
    return (
        json.loads((data / "release.json").read_text()),
        json.loads((data / "sources.json").read_text()),
        json.loads((data / "browser-review-policy.json").read_text()),
        json.loads((data / "browser-verification.json").read_text()),
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", type=Path, help="Add checked citations unresolved by a matching automated audit")
    parser.add_argument("--strict", action="store_true", help="Block releases with missing/stale selected inspections or explicit browser mismatches")
    parser.add_argument("--output", type=Path, default=ROOT / "build/browser-review-queue.json")
    args = parser.parse_args()
    release, sources, policy, history = load_context()
    byid = {r["id"]: r for r in sources}
    selected = set(policy["selected_ids"])
    if args.audit:
        audit = json.loads(args.audit.read_text())
        digest = hashlib.sha256((ROOT / "data/sources.json").read_bytes()).hexdigest()
        if audit.get("database_sha256") != digest or not audit.get("complete"):
            raise SystemExit("Browser queue requires a complete matching automated audit")
        selected.update(r["id"] for r in audit["records"] if r["checked_reference"] and r["identity_status"] in {"unresolved", "mismatch", "manual-confirmation"})
    receipts = latest_receipts(history)
    tasks, blockers = [], []
    for key in sorted(selected):
        if key not in byid:
            raise SystemExit(f"Unknown selected browser source: {key}")
        source = byid[key]
        receipt = receipts.get(key)
        errors = receipt_errors(receipt, source, release) if receipt else ["No browser inspection recorded"]
        if receipt and receipt.get("outcome") in {"mismatch", "not-found"}:
            errors.append("Explicit browser identity failure requires correction or removal")
        if errors:
            blockers.append(key)
        tasks.append({"id": key, "url": source["url"], "expected_title": source["title"], "doi": source.get("doi"),
                      "source_fingerprint": fingerprint(source), "release_month": release["release"],
                      "last_outcome": receipt.get("outcome") if receipt else None, "needs_review": bool(errors), "reasons": errors})
    report = {"release_month": release["release"], "scope": "Local Chrome identity inspection; not scientific replication.",
              "selected": len(tasks), "pending": len(blockers), "blocking_ids": blockers, "tasks": tasks}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    rows = "".join(f'<tr><td>{html.escape(t["id"])}</td><td><a target="_blank" rel="noopener" href="{html.escape(t["url"], quote=True)}">{html.escape(t["expected_title"])}</a></td><td>{html.escape("; ".join(t["reasons"]) or "Current inspection recorded")}</td></tr>' for t in tasks)
    args.output.with_suffix(".html").write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>Local Chrome reference review</title><style>body{font:16px system-ui;max-width:1100px;margin:40px auto;padding:20px}td,th{text-align:left;padding:12px;border-bottom:1px solid #ddd}a{color:#166f59}</style><h1>Local Chrome reference review</h1><p>Open these primary sources in local Chrome. Record observed metadata, access limits and inspected scope; do not bypass access controls or certify scientific validity.</p><table><tr><th>ID</th><th>Source</th><th>Review status</th></tr>' + rows + '</table></html>')
    print(f"Chrome review: {len(tasks)} selected, {len(blockers)} pending for {release['release']}")
    if args.strict and blockers:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
