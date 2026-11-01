# Contributing evidence and corrections

This living review welcomes source suggestions, citation corrections, methodological criticism, and alternative interpretations. Use [GitHub issues](https://github.com/does-ai-help/does-ai-help.github.io/issues/new/choose) for proposals and discussion and [pull requests](https://github.com/does-ai-help/does-ai-help.github.io/pulls) for specific changes. For discussion outside GitHub, contact Witold.Bolt@jit.team.

## Source suggestions

Supply the title, authors or organization, publication date and version, a primary URL, and a DOI, arXiv identifier, report number or other persistent identifier where available. Explain relevance, study design, the measured outcome, key result, limitations, and any overlap with studies already included. Distinguish an original study from a news story, commentary, abstract, preprint revision, or journal version. Declare relevant affiliations or interests. Do not upload copyrighted full texts without permission.

## Corrections

Identify the release, source ID or article passage, the precise problem, and evidence for the correction. A broken link does not establish a false finding; a functioning URL does not establish a correct citation. Report both access failures and pages that describe a different work. Urgent material errors may justify a patch release rather than waiting for the monthly cycle.

## Pull requests

Edit `data/editorial.json` for appraised source annotations, `data/intake.json` for candidates, and `manuscript/article.md` for the synthesis. Do not silently promote candidates or renew verification dates. Preserve stable source IDs, title/version history, and independence or overlap between datasets. Never invent missing authors, DOIs, findings, or dates. Include supporting primary metadata and the exact source passage, table, or abstract scope inspected. Mark AI-assisted contributions and describe the human checks performed.

Run the documented build, validation and reference verification checks. Generated exports must remain consistent with the canonical database. Do not edit archived published releases; add a version and changelog instead. Contributions to original review text and annotations are accepted under CC BY 4.0, and contributions to tooling under MIT. Contributors retain their rights and must have permission to submit their material.

## Monthly editorial review

Maintain a queue using the provided issue forms. During each monthly release, triage suggestions as accepted, awaiting evidence, duplicate/related version, out of scope, or declined with a reason. Evaluate source identity, design, validity, relevance, novelty, and conflicts of interest separately. Record accepted changes and material exclusions in the changelog and database. Submission does not guarantee inclusion or agreement. Link monitoring runs automatically; appraisal and publication are editorial decisions, not automated endorsements.

## Release gate

Run `python3 scripts/verify_references.py --strict` before release. Any identity mismatch or unresolved identity among checked references blocks publication. Access failures remain visible even when a DOI registry confirms identity. Manual exceptions require a named reviewer, dated evidence and reason, and must expire; they cannot override a detected mismatch. Inspect the public audit report and substantively check that each cited passage is actually supported: scripts cannot determine the truth of scientific claims.
