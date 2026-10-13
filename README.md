# Does AI Help?

**Evidence on productivity, learning, engineering, and scientific discovery**

Final October 2026 release · Version 2026.10.15 · Evidence cutoff: 13 October 2026

October's final editorial checkpoint is preserved at tags `v2026.10.14` and `october-2026-final`. Version `2026.10.15` is an affiliation-only presentation patch; findings and cutoff are unchanged. November preparation uses `codex/november-2026-preparation`; drafts on that branch are not published to the live site. See the [final editorial self-review](manuscript/october-final-review.md) for scope, corrections and remaining limits.

Lead AI author: **GPT 6.1**. Co-author: **Witold Bołt, PhD**, Vice-President of [Jit Team](https://jit.team), a software consulting company. For discussion of the review and its implications: [Witold.Bolt@jit.team](mailto:Witold.Bolt@jit.team) or [LinkedIn](https://www.linkedin.com/in/witoldbolt/). Affiliation is disclosed, not offered as evidence or product endorsement.

Original content is free to reuse under **CC BY 4.0**, including commercially, with appropriate attribution, a license link and an indication of changes. See [LICENSE-CONTENT.md](LICENSE-CONTENT.md). Source publications retain their rights; tooling uses MIT.

Read the publication at [does-ai-help.github.io](https://does-ai-help.github.io/). Evidence suggestions and corrections are welcome through [GitHub issues](https://github.com/does-ai-help/does-ai-help.github.io/issues/new/choose) and [pull requests](https://github.com/does-ai-help/does-ai-help.github.io/pulls). See [CONTRIBUTING.md](CONTRIBUTING.md), the issue forms and PR template in `.github/`, and [HOSTING.md](HOSTING.md). Monthly releases include editorial triage, not automatic acceptance.

## Pre-release reference audit

Selected problematic sources have an additional [local Chrome verification channel](BROWSER-VERIFICATION.md), a [monthly watchlist](data/browser-review-policy.json) and an [append-only observation ledger](data/browser-verification.json). Checks identify the AI-assisted reviewer and inspected scope. A new monthly release requires new Chrome observations; CI validates these receipts instead of pretending to operate the local browser. Two formerly unresolved suggestions were identified through this channel.

The [companion-review search log](manuscript/related-reviews.md) positions this publication alongside broad OECD/ILO syntheses, Stanford AI Index, systematic software reviews, education meta-analyses and scientific-agent surveys. Annotations and inspected scopes are maintained in `data/related-reviews.json`; do not describe abstract-only checks as full-paper appraisal.

Run `python3 -m unittest discover -s tests`, `python3 scripts/verify_references.py --strict`, and `python3 scripts/check_links.py --strict`, then `python3 scripts/validate.py --audit build/reference-verification.json`. Install the requirements first for PDF extraction. The identity audit compares declared titles/aliases and DOI metadata against live primary pages and Crossref/DataCite, inspects PDF opening pages, records redirects, metadata hashes, access failures, author/year warnings and duplicate DOIs, and checks arXiv redirects. It does not establish scientific validity or claim support.

Unresolved checked identities and mismatched identifiers/titles block deployment. HTTP 404/410 blocks the access gate, including candidate links that need removal or repair. Paywalls, bot restrictions, timeouts and other failures are reported separately. A documented, dated, expiring editorial exception can confirm an unresolved identity, but cannot override a detected mismatch. See `data/identity-exceptions.json`. Short/changed titles require documented aliases in `data/bibliographic-corrections.json`, not a relaxed global match threshold. A matching registry entry cannot conceal an unrelated source page. Never treat an AI-generated or inherited bibliography as primary verification.

Audit JSON, CSV and a summary are downloadable with the release. Fresh deployment audits must match the database hash and be no more than seven days old. The publication workflow retains live audit artifacts even on failure; manually appraise warnings and cited claims before approving a release.

A living critical narrative review and evidence map of AI's effects on intellectual work. The English article follows the development of evidence from task-level assistance to organizational outcomes, learning, scientific discovery, and employment. Its companion database records verification scope, method, publication status, original annotations, limitations, and stable identifiers.

## Read the publication

- [Web article](https://does-ai-help.github.io/)
- [Searchable evidence map](site/bibliography.html)
- [Article PDF](site/downloads/does-ai-help-2026.10.15.pdf)
- [Balance self-review and October source-admission log](manuscript/balance-review.md)
- [Complete October release](site/downloads/does-ai-help-release-2026.10.15.zip)
- [SWE-bench authors' recommended citations](site/downloads/does-ai-help-swebench-recommended-2026.10.15.bib)
- [Annotated database](data/sources.json)
- [CSL-JSON](site/downloads/does-ai-work-2026.10.15.csl.json), [BibTeX](site/downloads/does-ai-work-2026.10.15.bib), [RIS](site/downloads/does-ai-work-2026.10.15.ris), [CSV](site/downloads/does-ai-help-evidence-2026.10.15.csv), and [JSON Lines](site/downloads/does-ai-help-evidence-2026.10.15.jsonl)

Public downloads include the full release version, including patch numbers. `data/download-names.json` defines their project-specific names; the build generates a downloadable filename manifest. Generic file paths remain compatibility aliases for existing links and tools. Archives include current files and aliases, never other releases' versioned downloads.
- [Review method](manuscript/methodology.md) and [changelog](CHANGELOG.md)

Citation-manager exports contain checked identities only. The evidence database also retains candidates awaiting verification. A content check is qualified by the inspected scope; it is not independent replication. The article is not peer reviewed.

## Directory layout

| Directory | Purpose |
|---|---|
| `data/` | Evidence records, editorial annotations, metadata observations, exclusions and schema |
| `manuscript/` | English manuscript with stable citation keys and methodology |
| `latex/` | Professional XeLaTeX source; body and references generated from the manuscript |
| `scripts/` | Curation, export, build, validation, release packaging and maintenance checks |
| `site/` | Complete static publication for GitHub Pages |
| `releases/2026-10/` | Archived initial release and machine-readable checksums |
| `releases/2026-10.1/` | October patch release with balance review, source additions and corrected publication metadata |
| `releases/2026-10.2/` | Local Chrome verification ledger, corrected references and mandatory monthly browser-review process |
| `releases/2026-10.3/` | Publication-date corrections, explicit date provenance, authors and editor roles |
| `releases/2026-10.4/` | Supplied-document appraisal, three resolved candidates, agent-study version links and PDF provenance |
| `releases/2026-10.5/` | Clarifies Crossref registration of the Hicks version DOI; previous document-follow-up snapshot preserved |
| `releases/2026-10.6/` | Open-source policy contrasts, related research, QEMU history and SWE-bench citation recommendations |
| `releases/2026-10.7/` | Repository-backed dates for Gravity, Zig and Asahi, with pinned revision provenance |
| `releases/2026-10.8/` | Verified author/publisher credits, registered declaration creators and METR follow-up relationships |
| `releases/2026-10.9/` | Readable 12-character Git commit IDs in BibTeX; full provenance retained in evidence records |
| `releases/2026-10.10/` | Primary KPMG Q3 report, named authors and qualified value-versus-cost findings |
| `releases/2026-10.11/` | Leiden Declaration, registered authors, original date and mathematical governance context |
| `releases/2026-10.12/` | Project-specific versioned downloads, filename manifest and compatibility aliases |
| `releases/2026-10.13/` | Reviewed topic coverage, clean article references and GitHub star navigation |
| `releases/2026-10.14/` | Final October publication and editorial self-review |
| `releases/2026-10.15/` | Affiliation-only presentation patch to the closed October edition |
| `.github/workflows/` | Pages deployment and monthly source-access monitoring, for a standalone repository |

The directory is self-contained and intended to become the root of a dedicated GitHub repository. The existing parent checkout is not required for building or serving the release. No account credentials are included.

## Local build

Requires Python 3.10+, Node.js 20+, Pillow, and XeLaTeX with TeX Gyre fonts, `latexmk`, and standard LaTeX packages.

The favicon's editable source is `site/favicon.svg`. To regenerate its PNG, ICO and Apple touch variants, run `python3 scripts/build_favicon.py` with Pillow and librsvg's `rsvg-convert` installed. Hosting uses the committed assets and does not require librsvg.

```bash
npm install
python3 -m pip install -r requirements.txt
python3 scripts/curate.py
python3 scripts/export.py
python3 scripts/figures.py
npm run build
python3 scripts/build_pdf.py
python3 scripts/package_release.py
python3 scripts/validate.py
```

The current built publication is included, so a reader does not need LaTeX or Node.js. The article and searchable database also work when their HTML files are opened directly. For a conventional local preview, serve the static directory:

```bash
python3 -m http.server 8765 --directory site
```

Open `http://localhost:8765`.

## GitHub Pages

Use this directory as the repository root. Configure **Settings → Pages → Source → GitHub Actions**. The supplied `publish.yml` workflow validates and deploys the included static publication from `site/`. Run it manually for the first deployment, or push a release to `main`. It does not regenerate a research article automatically.

The repository is `does-ai-help/does-ai-help.github.io`, with organization-site address `https://does-ai-help.github.io/`. These addresses are configured in `data/release.json`. Review author contributions and conclusions before approving a release; no publication DOI is claimed. See [HOSTING.md](HOSTING.md) for configuration and remaining administrative steps.

For reproducible regeneration, the included build is separate from hosting. The deployment action uses committed static outputs, allowing readers to download the exact PDF and data that accompany the article.

## Monthly releases

See [MAINTENANCE.md](MAINTENANCE.md). Monthly access checks produce a report; editorial work determines source admission and changes in conclusions. Preserve an existing release archive when moving the current site to a new version. Update the release manifest, manuscript, bibliography, changelog and citation metadata together.

## Licensing

Original article text, original annotations, original figure and the compiled PDF: [CC BY 4.0](LICENSE-CONTENT.md). Publication tooling: [MIT](LICENSE-CODE). Third-party publications retain their rights; full texts are not redistributed. Citation metadata may carry source-specific terms where applicable.

Use [CITATION.cff](CITATION.cff) for attribution. No DOI or formal journal acceptance is claimed.
