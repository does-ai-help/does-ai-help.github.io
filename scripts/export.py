#!/usr/bin/env python3
"""Export annotated citations without fabricating missing bibliographic fields."""
import csv
import io
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def csl_author(name):
    if ", " in name:
        family, given = name.split(", ", 1)
        return {"family": family, "given": given}
    return {"literal": name}


def to_csl(r):
    status = r["publication_status"]
    kind = "paper-conference" if status == "peer-reviewed-conference" else "article-journal" if status.startswith("peer-reviewed") else "manuscript" if status == "preprint" else "report" if "paper" in status or "report" in status else "webpage"
    item = {"id": r["id"], "type": kind, "title": r["title"], "URL": r["url"], "author": [csl_author(a) for a in r["authors"]], "abstract": r["summary"], "keyword": "; ".join(r["topics"]), "note": f"Method: {r['method']}. Status: {status}. Verification: {r['verification']['level']} ({r['verification'].get('basis','')}). Limitations: {r['limitations']}"}
    if r.get("editors"):
        item["editor"] = [csl_author(a) for a in r["editors"]]
        item["type"] = "book"
    if r.get("publisher"):
        item["publisher"] = r["publisher"]
    if r.get("date_basis"):
        item["note"] += " Date basis: " + r["date_basis"]
    if r.get("authorship_basis"):
        item["note"] += " Authorship: " + r["authorship_basis"]
    if r.get("author_note"):
        item["note"] += " Attribution: " + r["author_note"]
    if r.get("year"):
        parts = [r["year"]]
        if r.get("date") and re.fullmatch(r"\d{4}-\d{2}(?:-\d{2})?", r["date"]):
            parts = [int(x) for x in r["date"].split("-")]
        item["issued"] = {"date-parts": [parts]}
    checked = r["verification"].get("checked_on")
    if checked:
        item["accessed"] = {"date-parts": [[int(x) for x in checked.split("-")]]}
    if r.get("doi"):
        item["DOI"] = r["doi"]
    if r.get("container_title"):
        item["container-title"] = r["container_title"]
    if r.get("version_note"):
        item["note"] += " Version: " + r["version_note"]
    if r.get("arxiv_id"):
        item["note"] += " Persistent identifier: arXiv:" + r["arxiv_id"]
    if r.get("browser_verification"):
        b = r["browser_verification"]
        item["note"] += f" Alternative verification: local Chrome, {b['checked_at']}; {b['outcome']}. Scope: {b['scope']}"
    if r.get("document_verification"):
        d = r["document_verification"]
        item["note"] += f" Document inspection: {d['method']}, {d['checked_on']}; {d['pages']} pages; SHA-256 {d['sha256']}. Scope: {d['scope']}. Artifact not redistributed."
    return item


def bib_escape(value):
    replacements = {"\\": r"\textbackslash{}", "{": r"\{", "}": r"\}", "%": r"\%", "&": r"\&", "#": r"\#", "_": r"\_"}
    return "".join(replacements.get(c, c) for c in str(value))


def main():
    records = json.loads((ROOT / "data/sources.json").read_text())
    verified = [r for r in records if r["verified"]]
    output = ROOT / "site/downloads"
    output.mkdir(parents=True, exist_ok=True)
    for filename, data in [("sources.json", records), ("bibliography.csl.json", [to_csl(r) for r in verified]), ("bibliography-core.csl.json", [to_csl(r) for r in verified if r['editorial_priority']=='core'])]:
        (output / filename).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    (output / "sources.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records))
    fields = ["id", "title", "authors", "author_display", "authorship_basis", "author_note", "editors", "publisher", "year", "date", "date_basis", "url", "doi", "arxiv_id", "study_family", "topics", "method", "publication_status", "summary", "limitations", "verified", "verification_level", "verification_scope", "checked_on", "version_note", "browser_method", "browser_checked_at", "browser_scope", "document_method", "document_checked_on", "document_sha256", "document_scope"]
    with (output / "sources.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for r in records:
            row = {k: r.get(k, "") for k in fields}
            row.update(authors="; ".join(r["authors"]), topics="; ".join(r["topics"]), verification_level=r["verification"]["level"], verification_scope=r["verification"].get("basis", ""), checked_on=r["verification"].get("checked_on", ""))
            row["editors"] = "; ".join(r.get("editors", []))
            browser = r.get("browser_verification", {})
            row.update(browser_method=browser.get("method", ""), browser_checked_at=browser.get("checked_at", ""), browser_scope=browser.get("scope", ""))
            document = r.get("document_verification", {})
            row.update(document_method=document.get("method", ""), document_checked_on=document.get("checked_on", ""), document_sha256=document.get("sha256", ""), document_scope=document.get("scope", ""))
            writer.writerow(row)
    bib, ris = [], []
    for r in verified:
        values = {"title": "{" + bib_escape(r["title"]) + "}", "url": r["url"], "note": bib_escape(r["limitations"] + " Verification: " + r["verification"]["level"])}
        if r.get("version_note"):
            values["note"] += " Version: " + bib_escape(r["version_note"])
        if r.get("browser_verification"):
            b = r["browser_verification"]
            values["note"] += bib_escape(f" Alternative verification: local Chrome, {b['checked_at']}; {b['outcome']}. Scope: {b['scope']}")
        if r["authors"]:
            values["author"] = " and ".join(bib_escape(a) if ", " in a else "{" + bib_escape(a) + "}" for a in r["authors"])
        if r.get("editors"):
            values["editor"] = " and ".join("{" + bib_escape(a) + "}" for a in r["editors"])
        if r.get("publisher"):
            values["publisher"] = bib_escape(r["publisher"])
        if r.get("date_basis"):
            values["note"] += " Date basis: " + bib_escape(r["date_basis"])
        if r.get("authorship_basis"):
            values["note"] += " Authorship: " + bib_escape(r["authorship_basis"])
        if r.get("author_note"):
            values["note"] += " Attribution: " + bib_escape(r["author_note"])
        if r.get("document_verification"):
            d = r["document_verification"]
            values["note"] += bib_escape(f" Document inspection: {d['method']}, {d['checked_on']}; SHA-256 {d['sha256']}. Scope: {d['scope']}. Artifact not redistributed.")
        if r.get("year"):
            values["year"] = str(r["year"])
        if r.get("doi"):
            values["doi"] = r["doi"]
        if r.get("container_title"):
            values["booktitle" if r["publication_status"] == "peer-reviewed-conference" else "journal"] = bib_escape(r["container_title"])
        if r.get("arxiv_id"):
            values["eprint"] = r["arxiv_id"]
            values["archivePrefix"] = "arXiv"
        kind = "inproceedings" if r["publication_status"] == "peer-reviewed-conference" else "article" if r["publication_status"].startswith("peer-reviewed") else "misc"
        if r.get("editors"):
            kind = "book"
        bib.append("@" + kind + "{" + r["id"] + ",\n" + ",\n".join("  " + key + " = {" + val + "}" for key, val in values.items()) + "\n}\n")
        rows = ["TY  - " + ("BOOK" if kind == "book" else "CPAPER" if kind == "inproceedings" else "JOUR" if kind == "article" else "ELEC"), "ID  - " + r["id"], "TI  - " + r["title"], *["AU  - " + a for a in r["authors"]], *["A2  - " + a for a in r.get("editors", [])]]
        if r.get("publisher"):
            rows.append("PB  - " + r["publisher"])
        if r.get("date"):
            rows.append("DA  - " + r["date"])
        if r.get("date_basis"):
            rows.append("N1  - Date basis: " + r["date_basis"])
        if r.get("authorship_basis"):
            rows.append("N1  - Authorship: " + r["authorship_basis"])
        if r.get("author_note"):
            rows.append("N1  - Attribution: " + r["author_note"])
        if r.get("document_verification"):
            d = r["document_verification"]
            rows.append(f"N1  - Document inspection: {d['method']}, {d['checked_on']}; SHA-256 {d['sha256']}. Scope: {d['scope']}. Artifact not redistributed.")
        if r.get("year"):
            rows.append("PY  - " + str(r["year"]))
        rows += ["UR  - " + r["url"], "AB  - " + r["summary"], "N1  - " + r["limitations"], *["KW  - " + topic for topic in r["topics"]]]
        if r.get("doi"):
            rows.append("DO  - " + r["doi"])
        if r.get("container_title"):
            rows.append(("T2  - " if kind == "inproceedings" else "JO  - ") + r["container_title"])
        if r.get("arxiv_id"):
            rows.append("AN  - arXiv:" + r["arxiv_id"])
        if r.get("version_note"):
            rows.append("N1  - Version: " + r["version_note"])
        if r.get("browser_verification"):
            b = r["browser_verification"]
            rows.append(f"N1  - Alternative verification: local Chrome, {b['checked_at']}; {b['outcome']}. Scope: {b['scope']}")
        rows.append("ER  - ")
        ris.append("\n".join(rows))
    (output / "bibliography.bib").write_text("\n".join(bib))
    (output / "bibliography.ris").write_text("\n\n".join(ris) + "\n")
    print(f"Exported {len(verified)} checked citations and {len(records)} evidence-map records")


if __name__ == "__main__":
    main()
