# Verification, Acceleration and the Shape of Work

First appraisal batch, inspected **11 November 2026** for the November draft. Twelve new records brought the collection to **339 references** at that stage, including **110 November additions**. Later batches are recorded separately. This is targeted appraisal and link following, not an exhaustive search or twelve independent studies. [Selection log](../november/search-2026-11-11.json).

## Decisions on the Suggested Sources

### AlphaProof Code: Include, With the Technical Report as the Main Citation

The [DeepMind announcement](https://deepmind.google/blog/introducing-alphaproof-code/) leads to the [technical paper](https://deepmind.google/documents/36/Formal_Verification_of_Signal_4.pdf) and [artifact overview](https://google-deepmind.github.io/code-verification/). The substantive contribution is a change in feasible assurance, not a code-output metric. Crucially, verifying a chosen specification is different from showing that the specification captures every relevant security goal. [@kohlicode2026; @chaudhurialphaproofcode2026]

Use the paper's stated boundaries in preference to the announcement's broad security language. The public artifacts are valuable for scrutiny, but this review has not rebuilt them. Announcement and report share one study family.

### Fragile Codebases and Productive Agents: Include Both as Situated Accounts

[Evan X. Merz](https://evanxmerz.com/post/ai-usage-generates-a-fragile-codebase/) offers specific failure mechanisms worth testing. Do not adopt his causal conclusions, or speculate about the reason for his layoff. The useful question is whether independent tests, maintainability and recovery capability deteriorate under output pressure. [@merzfragile2026]

[Ben Stolovitz](https://ben.stolovitz.com/posts/how-use-ai-oct-2026/) supplies a favorable but mixed counterpart. His change of job context matters when comparing years. Selected linked code artifacts establish that examples exist, not how much labor they saved or how well they will age. [@stolovitzusage2026]

Neither account is representative. Their value is in identifying mechanisms and outcomes that controlled studies and organizational measurements should examine, not in balancing two anecdotes as equal empirical votes.

### Accelerating AI Research: Include the Assessment and Label the Extrapolation

[Ajeya Cotra's essay](https://www.planned-obsolescence.org/p/ai-is-dramatically-accelerating-ai) leads to [METR's primary assessment](https://metr.org/blog/2026-11-05-anthropic-ai-rd-acceleration-assessment/) and its earlier [assessment proposal](https://metr.org/blog/2026-10-14-ai-rd-acceleration-assessment-proposal/). Treat trend estimation, causal attribution and predictions as separate inferential steps. A fit interval does not encompass every uncertainty about causation or generalization. [@cotrard2026; @metrrdassessment2026; @metrassessmentproposal2026]

The redaction boundary is unusually consequential: readers cannot independently evaluate much of the evidence behind the assessors' conclusions. That weakens public auditability without by itself disproving the assessment. Cotra's essay is not an independent replication; its conditional compounding argument should not become an observed outcome.

The comparison with InnovationEval belongs in the article: expert-guided institutional assistance and autonomous benchmark completion are different interventions. Opposite-looking results need not contradict each other. [@innovationeval2026]

### Valuation Optimism: Retain as Context, Check the Accounting

[Matteo Raso's argument](https://matteoraso.github.io/im-not-convinced-the-ai-bubble-exists.html) is a relevant counterpoint, not a financial consensus. The linked [SEC filing](https://www.sec.gov/Archives/edgar/data/2130357/000162828026067168/anthropicpbc-sx1.htm) is preferable for company figures. We do not reproduce the post's unverified industry totals, current market multiples or profitability ratio. [@rasobubble2026; @anthropics12026]

Our analytical distinction is broader: useful technology can coexist with poor investment returns, and provider revenue can grow without proving customer productivity. Neither a favorable nor an unfavorable valuation argument answers the review's central question alone.

### PHP2Shell: Add Exploitability Context, Not Another Discovery

[Ariane Djad's walkthrough](https://djad04.github.io/php2shell-deep-dive/) helps qualify general claims about exposure. The linked challenge materials are inspectable, but were not executed. This belongs to the existing PHP2Shell family, not a new observation of AI productivity. Its date comes from page-file Git history; the date the author started writing is not a publication date. [@djadphp2026]

## Additional ActivTrak Request

The [October research release](https://www.activtrak.com/news/productivity-lab-ai-users-longer-workdays/) adds behavioral observations to the discussion of work intensification. The headline's upper difference is not an estimated treatment effect. Heavy-versus-light focus comparisons and AI-versus-nonuser workday comparisons are different contrasts. Embedded versus browser tools may also proxy different jobs. [@activtraklonger2026]

The linked [annual report](https://www.activtrak.com/resources/state-of-the-workplace/) is admitted separately to preserve those distinctions. Its primary sample is 163,638 employees at 1,111 organizations during 2023-2025; the adoption before/after cohort is 10,584 employees at 376 organizations. Neither is the October release's sample. Its glossary defines workday as first-to-last computer activity. [@activtrakworkplace2026]

The review should not translate more application activity into more valuable output, or a longer recorded span into ninety extra minutes of continuous labor. Nor should an inferred workload category become a clinical burnout diagnosis. Monitoring-based evidence also warrants questions about consent, coverage and privacy; these are methodological and governance concerns, not findings that this dataset measures.

## Access, Dating and Follow-up

- All seven suggested pages are included, but only some support direct empirical claims. Four linked primary/methodological sources and the annual report receive separate records.
- Original public HTML retrieval resolved search-reader failures for Merz, Raso and Djad. This was an alternative HTTP reading method, **not local Chrome verification**. No browser receipt was invented.
- The primary AlphaProof PDF is identified by hash and page count; no third-party full text is redistributed. METR's unredacted report and ActivTrak raw telemetry were not available.
- Linked repositories are contextual artifacts, not extra independent studies. No exploit, code build or proof campaign was run.
- Before final November publication: check revisions, refresh required browser receipts, reassess access and complete the release-wide audit. Today's selected inspections do not refresh unrelated references.
