# November Release Readiness

Updated on **13 November 2026** for **2026.11.0-preview.7**. Evidence cutoff: **12 November**. Intended publication: **13 November 2026**, subject to editorial approval. This report does not declare a final release.

## Verification Scope

This is a source-based review, not a reproduction study. We check authentic publication locations, authorship, identifiers, versions, the support for cited statements within the inspected material, and relationships between studies, announcements and commentary. We do not rerun experiments, reconstruct datasets, execute exploits or compile third-party proofs as a publication requirement.

Limited access narrows what may be asserted; it does not turn an abstract into a full-text appraisal. Identity confirmation is not scientific validation. Multiple accounts of one event are not independent evidence.

## Completed Checks

- A complete automated identity pass covered all **381 evidence records**. Following the new-network retry and the human coauthor's explicit access decision: **335 confirmed**, **26 confirmed through local Chrome**, **1 covered by an existing time-limited manual confirmation**, **15 unresolved candidates**, and **4 retained as currently unverified under a November-only deferral**. **No strict identity blockers remain under that explicit decision; the four records have not been confirmed.** Applying the decision did not perform new network checks or refresh access timestamps. These categories describe reference identities, not independent experiments.
- The link pass checked **509 distinct URLs** and found **no HTTP 404/410 responses**. There were **48 HTTP 403 responses**, **1 HTTP 500**, **3 HTTP 502**, **1 HTTP 503**, and **6 other connection errors**. A successful HTTP response alone does not establish citation correctness. Versioned publication URLs intentionally deferred until deployment are listed separately in the machine-readable report.
- Local Chrome revisits are recorded individually with dates, inspected titles and access limits. The original October ledger is retained and November receipts are appended only in the isolated November build. All **41 explicitly selected monthly sources** have an attempted revisit recorded; the current audit-driven queue has **no missing or stale monthly observations**. An access-blocked receipt records an attempt, not a successful identity confirmation. The 13 November follow-up confirms ten previously problematic identities, including two through pinned official Gravity Linux sources, without erasing earlier failed attempts. See [the source-by-source follow-up](does-ai-help-verification-followup-2026.11.0-preview.7.md).
- The ILO paper's short DOI title, **Disruption without dividend?**, is documented as an alias of the publisher title with its subtitle. This resolves a metadata mismatch rather than changing the study's identity or evidence.
- Wiles, AutoDNA and NBER 36003 were revisited at their primary publication pages in local Chrome. The current reading boundaries remain explicit. The final Wiles abstract uses **N=487**, unlike the older author's copy (**N=573**); that copy is not substituted. NBER 36003 now has a direct primary-page check rather than only an indexed-abstract check.
- Apache's advisory, its CNA record and Red Hat's assessment were inspected. HTTP/2 configuration, affected versions, separate module versions and finder credits remain distinct. The CISA feed actually inspected was version **2026.11.10**: the selected PHP and Brotli entries were present; Apache CVE-2026-119618 was absent. Absence from that snapshot does not establish an absence of exploitation.
- The pinned Omarchy repository and m1n1 relicensing commit were inspected. This confirms document provenance, not license compliance or the truth of allegations about unnamed parties. The standalone mod_h2 archive notice explicitly says maintenance continues in Apache httpd.
- The high-impact formalization sources were revisited through primary pages: AlphaProof Code, CPython, Julia and PTX. Human-approved specifications, partial model coverage, bug-candidate triage and single-demonstration scope remain qualifications, not unresolved demands for reproduction.
- A targeted manuscript review retained the distinctions between activity and outcomes, exposure and adoption, sales and profits, assistance and autonomy, reported discovery and accepted proof, and limited telemetry versus global exploitation. Positive, adverse and null evidence are not combined by vote counting.
- **168 automated tests passed**, including expiry, identity binding, mismatch/not-found rejection, historical-record preservation and visible unverified labels. Final web/PDF/local-link/checksum integrity and October preservation are checked after packaging and synchronization.
- The publication repository had **no open issues or pull requests** when checked in this session. October inputs and published artifacts were unchanged before preparation; the final preservation check must also pass after synchronization.

## Retained but Currently Unverified

The authoritative observations and current decisions are in `verification-2026-11-13/reference-verification.json` and `access-deferrals.json`. The human coauthor explicitly approved flagging the four remaining inaccessible references as unverified and continuing. They remain contextual sources with earlier dated reading history, not newly confirmed sources. HESA's temporary failure was resolved by a successful Chrome inspection at 08:58 UTC and is not part of this deferral.

| Record | Current limitation / November disposition |
| --- | --- |
| `baimehomework2026` | Daily Californian denies access. Currently unverified; retained as context, non-blocking by explicit approval. |
| `torvaldstools2026` | LKML bot check/server failures. Currently unverified; retained as context, non-blocking by explicit approval. |
| `pincharttools2026` | LKML HTTP 502. Currently unverified; retained as context, non-blocking by explicit approval. |
| `cooktools2026` | LKML navigation failure. Currently unverified; retained as context, non-blocking by explicit approval. |

The decision is bound to these exact citation identities and **November 2026**, expires **30 November**, and must be reconsidered in the next monthly release. It cannot clear mismatches, explicit not-found results, changed citations or other unresolved references. The website, article methods, citation-manager notes and downloadable decision manifest disclose the limitation. Historical `verified`/reading-scope fields describe earlier admission and inspection; the current-release audit and deferral manifest govern present access status.

The direct OpenAI Navier–Stokes PDF also timed out in Chrome, although its primary announcement was readable and its identity did not remain an automated strict blocker. This is a reading/access boundary, not proof invalidation.

## Gravity Linux: Access Versus Identity

The human coauthor reports DNS4EU's warning, “The content of this page can be harmful,” and successful access from a mobile connection using different DNS. This report does not independently diagnose the DNS response or declare the domain harmful or safe. Earlier certificate-hostname errors remain in the access history, but are not described as a proven origin-server certificate defect.

Both official source files were read in local Chrome and crosschecked through GitHub's API/file history. Their immutable source links are now included alongside the unchanged canonical website URLs. The About revision is `cfc74e6` (14 October); the policy revision is `2d7bbba` (13 October). These are file-revision dates, not fork or adoption dates. This deliberate fallback is not reported as an observed HTTP redirect. October's source records remain unchanged.

At 08:57 UTC, after the human coauthor reported changing networks/DNS, both canonical Gravity pages loaded directly in Chrome and matched the previously inspected repository content. Successful direct visits are appended after the earlier blocked-access and repository-fallback observations. This supports a connection-dependent access difference, not a controlled diagnosis of the earlier filtering or an independent website-safety finding.

## Release Decision

**Source gate cleared with four explicitly retained, currently unverified contextual records.** This is not an assertion that every reference is currently verified, and it is not final editorial approval. No global threshold was weakened and no successful source receipt was fabricated. Stop trying to repair these four access failures for this release; reconsider them in the next monthly review.

Full-text follow-up is optional where the existing bounded statement is supported by an authentic public abstract. Additional details requiring unavailable methods must not be added. Independent scientific reproduction is outside scope.

After source clearance and human editorial approval, set the final cutoff, date, version and changelog together, rebuild final artifacts, verify their checksums, and deliberately merge/tag the November release. **No merge, final tag or replacement of October is authorized by this readiness report.**

## Audit Artifacts

- `verification-2026-11-13/reference-verification.json`, `.csv`, `.md`: current complete source-identity audit and retry results, tied to the exact assembled database hash.
- `verification-2026-11-13/access-report.json`: current link access checks, including failures and deferred publication URLs.
- `verification-2026-11-13/browser-review-queue.json`: current monthly-check queue, with no missing observations; failed access does not imply identity clearance.
- `verification-2026-11-12/`: retained earlier audit snapshot, not relabeled as the current pass.
- `verification-followup-2026-11-13.md`: ten successful follow-up identities, versions, reading boundaries and the human-reported DNS restriction.
- `release-browser-checks.tsv`: curated visible observations and failed-attempt records; temporary security-challenge tokens are not retained.
- `identity-title-aliases.json`: explicit publisher/registry heading variants, scoped to November.
- `access-deferrals.json`: the human coauthor's four identity-bound, November-only access decisions; not a manual-confirmation list.

The preview builder accepts a saved audit only when its database hash matches the assembled November evidence file. It does not relabel a stale or unrelated audit as a fresh release check.
