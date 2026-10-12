# Methodology and interpretation

Release: October 2026. Cutoff: 12 October 2026.

This is a critical narrative review and evidence map, not a systematic review or a statistical meta-analysis. The initial supplied reference collection was expanded through primary-source searches and bibliographic checks. The scope concentrates on 2023-2026, with selected earlier foundations.

## Two layers of evidence

The article uses content-checked records only. Their verification scope states whether checking covered a full report, an abstract, a methods section, or an official summary. The wider database also includes identity-checked supporting records and candidates with unresolved access or identity. Identity checks never establish validity of findings.

The `verified` field means that bibliographic identity or inspected content was checked. It does not mean independent replication, scientific consensus, or that every causal claim is accepted. Publication status is separate: preprint, working paper, journal article, vendor report, and commentary have different roles.

## Database conventions

- Stable IDs are retained across releases. IDs are not inferred evidence grades.
- An original short summary and limitations are supplied for core records. Supporting records have scope descriptions without unappraised outcome claims.
- Authors and publication dates are taken from primary metadata or explicit editorial checking where available. Unknown fields remain empty; year inference from an identifier is labelled in `date_basis`.
- `date` is a publication date when established. A revision may appear in `version_note`; publication, revision, retrieval, and press coverage dates must remain distinct.
- An organizational name is treated as a corporate author only when it is the responsible source. Absence of a personal author does not justify inventing one.
- Several versions or pages of one work may be listed for access and context. Such entries do not represent independent experiments. Known relationships appear in `related_to` or `dataset_family`.
- Candidate records are present in evidence JSON and CSV but excluded from BibTeX, RIS, and the main CSL-JSON export.

## Admission and appraisal

For each important claim, inspect the population, intervention or exposure, comparator, outcome definition, sample size, uncertainty, model/tool vintage, resource budget, and evaluation protocol. Separate randomized access from chosen adoption; observable activity from value; assisted performance from unaided learning; and formal validity from validity of the specification.

Prefer primary sources and revised versions. Include null findings and plausible counterexamples. Identify interests and limited independence in vendor evidence. Interpret commentary as an argument rather than empirical proof. Do not assume peer review removes confounding or turns a proxy into direct value measurement.

Searches and collection are purposive and English-language weighted. The review can miss research in other languages, inaccessible data, and non-public organizational experience. Automated metadata auditing detects identity and accessibility problems but does not discover all retractions or authenticate every scientific result.

## Reproducibility

`data/sources.json` is the release evidence database. `data/editorial.json` holds human-readable editorial overrides and original annotations. `data/audit.json` contains public metadata observations and access status. Third-party full text is not distributed. The exclusions log records an inherited link that resolved to an unrelated publication.

Article citations use stable keys in the manuscript. The build produces the same numbered reference order in HTML and LaTeX and rejects missing or unappraised citation keys. A release includes the PDF, citation exports, cutoff metadata, changelog, and SHA-256 checksums.

## Attribution

GPT 6.1 is credited as lead AI author for curation, appraisal, synthesis and drafting. Witold Bołt is co-author for topic initiation, initial links and viewpoints, conceptual framing and direction, and initiation of the review in this form. This attribution does not claim separate human auditing of every record or peer review of the article.
