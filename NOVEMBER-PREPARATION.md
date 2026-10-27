# November 2026 Release Preparation

Status: **unpublished preparation**. Branch: `codex/november-2026-preparation`.
Starting baseline: final October version `2026.10.14`, tags `v2026.10.14` and `october-2026-final`, evidence cutoff 13 October 2026. The affiliation-only patch `2026.10.15` is incorporated without reopening October's scientific content.

The live site remains on the final October release until a reviewed November release is merged into `main`. This branch initially retains October's manifest and built artifacts as its baseline; they are not November deliverables. No November publication, cutoff or verification date has been assigned. Intended first November version: `2026.11.0`, subject to release preparation.

## Staged Material

### 16 October: Linux Tool Use and Disclosure

- [Analysis and ready-to-integrate article passage](manuscript/november-linux-tools.md): Torvalds's tool-neutral position, Pinchart's norm-setting objection, Cook's review and accountability argument, and the distinction between proposal and implemented policy.
- [Six new source records](data/november-sources.json), [two existing-policy rechecks](data/november-source-rechecks.json), and [alternative Chrome observations](november/browser-observations.json).
- Existing October article, database, citation exports, PDF, version manifest and release artifacts are unchanged. These intake files are not automatically consumed by the October curation/build pipeline.
- During November integration, merge the appraised intake into the curation inputs, apply the policy rechecks to existing IDs rather than duplicating them, set the actual November manifest/cutoff, regenerate exports and article together, and refresh selected browser receipts. Do not treat October intake observations as November release verification.

### 26 October: Ambition and Previously Uneconomic Software

- [Analysis and proposed article passage](manuscript/november-ambitious-software.md), connecting Dan Luu's essay to option value, verification costs and different quality thresholds.
- Three additional records in [November sources](data/november-sources.json): the essay and two primary PostgreSQL follow-ups. Publication date verified from the publisher's RSS; practitioner testimony is distinguished from causal evidence and production-readiness claims.
- This intake brought the staged reference count to nine. No October article, database or release artifacts are regenerated.

### 26 October: Payoff, Prices, Contracts and Assessment

- [Admission decisions and proposed article additions](manuscript/november-payoff-costs-and-assessment.md) assess all five suggestions, distinguishing macro commentary, price accounting, contractual value capture, educational assessment and a mathematical perspective.
- Seven records added: Slok/Apollo, Woolf, Strogatz, Baime/The Daily Californian, Reuters via attributed syndication, and primary Anthropic pricing and Vercel methods. Total staged new references: **16**.
- The Atlantic essay was read in full using the user-supplied Safari PDF. [Full-text appraisal](manuscript/november-strogatz-mathematical-practice.md) separates discovery, understanding, training and participation, including constructive and adverse perspectives. [Document observations](november/document-observations.json) record the printout's checksum and reading scope without redistributing it; the historical preview-only Chrome observation is unchanged. The Berkeley article was read in full through local Chrome. Both sources require appropriately dated monthly rechecks before November publication.
- October remains unchanged; no new public release or generated bibliography is produced at this intake stage.

### 27 October: Coordination, Skills and Scientific Stewardship

- [Admission decisions, critical reading and proposed article additions](manuscript/november-coordination-skills-and-scientific-stewardship.md) cover all five new suggestions.
- Seven new records: van den Berg, OpenAI, Voytko, Kärki and Stewart, plus the public Microsoft memo and GeekWire corroboration. Total staged references: **23**; the three Microsoft records concern one event, not independent employment-effect studies.
- New emphasis: coordination costs; historical software-quality baselines; collective responsibility for skills; and scientific stewardship distinct from proof validation. A primary-source crosscheck qualifies the deskilling paper's use of a self-report study as evidence of skill decay.
- Four alternative Chrome observations record actual reading scope, including Business Insider's subscription overlay. Selected resources require fresh monthly checks before publication. No October outputs are rebuilt.

### 27 October: Security Discovery and Remediation

- [Critical appraisal and proposed article passage](manuscript/november-security-discovery-and-remediation.md) add Hugh Son's CNBC report on Bank of America's patching contractors. The original article was read in full in Chrome; the linked primary transcript was located but not accessible for inspection.
- Distinguish exposed from AI-created flaws, contractor additions from net employment, mixed compliance/remediation expense from a model-only cost, and forecast savings from realized net benefits.
- One new record brings the staged total to **24**. October remains unchanged.

### 27 October: PHP2Shell, Brotli and AI-Assisted Security Research

- [Detailed review and selected reading](manuscript/november-ai-security-php-brotli.md) cover PHP2Shell, shared Brotli exposure in Node.js/.NET/PHP, Firefox maintainer-confirmed findings and N-day capability research.
- Twenty new primary, first-party and expert-analysis records bring the staged total to **44**. Family labels prevent treating downstream advisories, discovery partners or reporting aliases as independent discoveries.
- [Dated observations](november/security-observations.json) preserve the qualified PHP-prevalence denominator, Censys service units and CISA catalog additions: PHP on 26 October and Brotli on 27 October. Earlier negative sensor observations are not current global absence claims.
- Three new Chrome observations document dynamically loaded data and inaccessible article text. All selected resources need appropriately dated November checks; no October outputs are rebuilt.

### 27 October: Python Brotli Follow-Up

- Added Aikido's analysis and the reviewed Python package advisory to the [security review](manuscript/november-ai-security-php-brotli.md). Total staged references: **46**.
- [Package observations](november/security-observations.json) retain fixed versions, PYSEC/GHSA aliases, the null GitHub CVE field and differing lower affected bounds. Do not equate installation or downloads with reachable exploitation.
- Both new records share the existing Brotli family. No additional discovery, Python RCE reproduction or scanner efficacy is asserted; October remains unchanged.

## Editorial Priorities

- Review incoming GitHub source suggestions, corrections and substantive alternative interpretations; record admission decisions and overlapping evidence.
- Search for independent replications, randomized or credible quasi-experimental interventions, longer-run outcomes, null and adverse results, and broad companion reviews.
- Revisit production quality, security, reviewer effort, accepted output, adoption costs and actual use rather than activity counts alone.
- Seek learning retention and transfer measures, credible instructional interventions, subgroup effects and synthesis-method sensitivity.
- Track specialist responses to mathematical proof claims, precise artifact revisions and institutional decisions without treating announcements as settled validation.
- Examine autonomous-research novelty, task memorization, result selection, compute budgets, evaluator independence and fair human comparisons.
- Recheck labor-market study revisions, entry-level pathways and institutional differences; distinguish forecasts from observed effects.
- Invite independent human or specialist review of the October synthesis, especially causal identification and mathematical interpretation.

## Preparation Checklist

- [ ] Establish the November search window and document searches and exclusions.
- [ ] Triage community issues and proposed references.
- [ ] Inspect revised sources, publication status, corrections and retractions.
- [ ] Record outcome-level changes to conclusions, not just additions to the source count.
- [ ] Integrate the staged Linux discussion and verify whether the trailer-removal proposal has been merged.
- [ ] Set November manifest, snapshot, citation metadata and actual cutoff together when release preparation begins.
- [ ] Refresh selected local Chrome receipts for November; do not redate or reuse October observations as November verification.
- [ ] Draft a concise “What's new” section distinguishing new evidence from editorial corrections.
- [ ] Preserve all October versioned downloads, archives, tags and checksums.
- [ ] Regenerate site, citation exports and PDF; inspect desktop/mobile layouts and all PDF pages.
- [ ] Run unit tests, strict reference and access checks, browser-receipt validation and release checksums.
- [ ] Complete editorial approval, merge into `main`, verify deployment, and tag the November publication.

Follow `MAINTENANCE.md` and `BROWSER-VERIFICATION.md`. The monitoring workflow checks access; it does not approve evidence or publish a new research article. No future verification is asserted by this plan.
