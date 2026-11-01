# November Draft: Ambition and the Feasible Project Set

Status: **unpublished November intake**, inspected **26 October 2026**. October's article and artifacts remain unchanged.

## Proposed Article Passage

Place in section 9 beside the discussion of option value, with a connection to section 5's distinction between prototype and delivered software.

Dan Luu argues that AI makes previously uneconomic software worth attempting. His examples distinguish personal utility from production readiness, while a quoted objection from Yossi Kreinin emphasizes maintenance and weak validation. Luu acknowledges limited benchmarking. This is practitioner testimony supporting a hypothesis about the feasible project set, not a general productivity estimate. [@luuambitious2026]

Selected PostgreSQL replies corroborate specific bug-report follow-up: one contributor reports reproduction; another agrees with an analysis and proposes a fix with a regression test. We did not run the code or establish that either patch was merged. These records do not isolate AI's contribution or validate pgrust as a production database. [@pgrustspgist2026; @pgrustformat2026]

The implication for our framework is to compare more than completion time. A project that was never commissioned has no earlier delivery time to beat. Relevant measures include the cost of a credible experiment, useful discoveries even if the project is abandoned, and the ongoing burden of operating what is built. Evaluation should distinguish valuable personal tooling, a promising prototype and a maintained product, rather than treat one quality threshold as appropriate for every use. This is our analytical interpretation, not a measured effect of the cited cases.

## Appraisal and Citation Notes

- [Essay](https://danluu.com/ambitious/): Dan Luu, **24 October 2026**, established by the matching entry's `pubDate` in the [publisher feed](https://danluu.com/atom.xml). The feed is RSS despite its filename. Full essay, appendices and caveats were read.
- Preserve the verification concern: greater implementation scope can create harder checking problems. Kreinin's objection is quoted within Luu's essay, not independently published evidence inspected here.
- Keep the author's unusually explicit caveats visible. Do not import unreplicated model rankings, speedups, cost figures or database benchmark claims as measured results of this review.
- The [SP-GiST follow-up](https://www.postgresql.org/message-id/CAJTYsWXFmxSc60e1Kj29QFtaRn5P28prg40sVVGhHyg8dF0VgQ@mail.gmail.com) and [format-cache follow-up](https://www.postgresql.org/message-id/CAB8bMit-UFnAz0C%2Bi-0DCo3O7Dzq-%2B0C75z78W-MpJMyW%2BcztA@mail.gmail.com) are primary technical discussions, not independent productivity studies. Their original reports were also inspected. Reproducers and attachments were not executed or independently reviewed.

## November Integration

Three records are staged in [November sources](../data/november-sources.json), with actual inspection dates, related-source links and explicit limitations. Integrate them into the November curation inputs and citation exports when preparing its manifest. They are not added to the closed October database. Recheck revisions and any upstream patch status before making stronger claims in November.
