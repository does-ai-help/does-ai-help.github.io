#!/usr/bin/env python3
"""Archive a complete release without overwriting an existing different snapshot."""
import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def checksum(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--replace-draft", action="store_true", help="Replace this unreleased draft snapshot during its initial preparation.")
    args = parser.parse_args()
    meta = json.loads((ROOT / "data/release.json").read_text())
    release = meta.get("snapshot", meta["release"])
    destination = ROOT / "releases" / release
    download = ROOT / "site/downloads"
    files = sorted(p for p in download.iterdir() if p.is_file() and p.suffix != ".zip" and p.name != "checksums.sha256")
    expected = "".join(f"{checksum(p)}  {p.name}\n" for p in files)
    if destination.exists() and (destination / "checksums.sha256").exists() and (destination / "checksums.sha256").read_text() != expected and not args.replace_draft:
        raise SystemExit("This release snapshot already differs. Increment the release version or use --replace-draft only before initial publication.")
    destination.mkdir(parents=True, exist_ok=True)
    for p in files:
        shutil.copyfile(p, destination / p.name)
    for folder in [destination, download]:
        (folder / "checksums.sha256").write_text(expected)
    archive = download / meta.get("archive_name", f"release-{meta['release']}.zip")
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for p in sorted(destination.iterdir()):
            if p.is_file():
                bundle.write(p, f"{release}/{p.name}")
        for p in sorted((ROOT / "latex").glob("*.tex")):
            bundle.write(p, f"{release}/latex/{p.name}")
        bundle.write(ROOT / "site/assets/evidence-pathway.png", f"{release}/site/assets/evidence-pathway.png")
        if not (destination / "LICENSE-CONTENT.md").exists():
            bundle.write(ROOT / "LICENSE-CONTENT.md", f"{release}/LICENSE-CONTENT.md")
    print(f"Release {release}: {len(files)} files archived, ZIP {archive.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
