#!/usr/bin/env python3
"""Build the XeLaTeX article and place a single downloadable PDF in the site."""
import shutil
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    compiler = shutil.which("latexmk") or "/Library/TeX/texbin/latexmk"
    if not Path(compiler).exists():
        raise SystemExit("latexmk is unavailable. Install a TeX Live or MacTeX environment with XeLaTeX.")
    output = ROOT / "build/latex"
    output.mkdir(parents=True, exist_ok=True)
    result = subprocess.run([compiler, "-xelatex", "-interaction=nonstopmode", "-halt-on-error", f"-outdir={output}", "article.tex"], cwd=ROOT / "latex", capture_output=True, text=True)
    (ROOT / "build/compile-output.txt").write_text(result.stdout + result.stderr)
    if result.returncode:
        print((result.stdout + result.stderr)[-8000:])
        raise SystemExit(result.returncode)
    source = output / "article.pdf"
    if not source.exists():
        raise SystemExit("The compiler returned without producing the expected PDF.")
    release = json.loads((ROOT / "data/release.json").read_text())["release"]
    target = ROOT / "site/downloads" / f"does-ai-help-{release}.pdf"
    shutil.copyfile(source, target)
    print(f"PDF compiled: {target} ({target.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
