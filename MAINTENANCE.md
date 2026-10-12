# Monthly release procedure

The publication is maintained through explicit, versioned editorial releases. Automated access checks do not approve claims or write the next article.

1. Create the next monthly release manifest and set the evidence cutoff. Retain the existing release directory and ZIP without modification.
2. Re-check revised core papers, publication status, corrections and retractions. Compare actual versions rather than their latest media coverage.
3. Search primary sources for new experiments, replications, longer-run outcomes, independent datasets, null findings and meaningful methodological analyses.
4. Add candidate records with stable IDs. Check identity, then record the precise content inspected before admitting conclusions.
5. Evaluate whether a new source changes a conclusion, supplies a new mechanism, improves identification, or merely adds another example. Record dataset overlap and related versions.
6. Update original annotations, limitations and citation fields in `data/editorial.json`. Keep unknown facts unknown. New citations require content checking; metadata-only records remain supporting sources.
7. Edit the manuscript and changelog, identifying strengthened, weakened, corrected and unresolved claims. Keep publication dates separate from revision and retrieval dates.
8. Regenerate the database, citation exports, HTML, LaTeX, PDF and conceptual figure if changed. Inspect the PDF page images and responsive browser layouts.
9. Run validation, verify downloads and citation-manager imports, then package the release with checksums. Add the new release to the website history.
10. Commit the release and publish through GitHub Pages. Retain the cutoff, original source version notes and previous release archive.

## Search priorities

- Intellectual-work experiments with real quality and outcome measures.
- Delivery and maintenance rather than only commits, tokens, PR counts or user enthusiasm.
- Learning that persists without AI and transfers to new tasks.
- Scientific validation, novelty, importance and independent replication.
- AI research automation with contamination checks, fair compute/time comparisons and selection-aware evaluation.
- Organizational value and workforce effects with credible treatment definitions and appropriate institutional comparators.

## Automated monitoring

The supplied GitHub workflow runs on the first day of each month and is manually runnable. It checks public source access and saves a report as a workflow artifact. Access failures can be temporary, access-controlled or redirects; they are not proof that a study is invalid. No automatic research publication or external messaging is performed.

`scripts/audit_sources.py` can update identity observations using public metadata. Its `--cutoff` must reflect the actual checking date. Curation must retain any content-check date accurately rather than silently carrying it forward to a new month.
# Community triage and verification

At each monthly release, review GitHub source-suggestion and correction issues. Record inclusion decisions, reasons for deferral/exclusion, related versions and overlapping samples. Credit substantive contributions with consent; never publish private contact details submitted in an issue without permission.

Before release run the strict reference-identity audit and all-link access check described in README.md. Inspect author/date warnings and DOI duplicates, check the exact passages behind article claims, and record any title aliases or time-limited identity exceptions with primary evidence. A metadata match is not replication or a guarantee against misinterpretation. The monthly workflow only produces monitoring reports; it cannot replace editorial appraisal. Keep the original review and annotations under CC BY 4.0 and preserve third-party rights.
