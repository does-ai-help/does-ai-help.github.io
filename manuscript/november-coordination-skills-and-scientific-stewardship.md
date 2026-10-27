# November Intake: Coordination, Skills and Scientific Stewardship

Inspected **27 October 2026**. Unpublished preparation for November; no October content or generated release artifacts are changed.

## Admission Decisions

| Source | Use in the synthesis | Evidence boundary |
| --- | --- | --- |
| [Jan van den Berg, 27 October](https://j11g.com/the-mythical-man-month-in-the-age-of-ai) | Agent coordination, sequential dependencies and integration effort. | Practitioner analogy, not a scaling experiment. |
| [OpenAI, 26 October](https://openai.com/index/building-scientific-understanding-with-academic-communities/) | Research disclosure, expert stewardship and the distinction between output and understanding. | Developer claims, not independent confirmation of discoveries. |
| [Jake Voytko, 27 October](https://www.bitlog.com/2026/10/27/software-may-be-getting-worse-but-it-used-to-be-horrible/) | Historical baseline and skepticism toward nostalgia about software quality. | Selected memories, not a historical quality series or AI comparison. |
| [Kaisa Kärki, 23 September](https://doi.org/10.1515/humaff-2026-0080) | Collective responsibility for maintaining expertise. | Normative argument, not a new estimate of skill loss. |
| [Ashley Stewart, Business Insider, 26 October](https://www.businessinsider.com/microsoft-is-offering-buyouts-read-the-memo-2026-10) | Workforce context, with accessible primary and reported crosschecks. | Subscription overlay limits certified reading scope; eligibility is not actual departures or AI displacement. |

## Proposed Article Additions and Reading Notes

### Engineering: More Parallel Work Is Not Necessarily More Delivery

Van den Berg argues that agents leave sequential dependencies intact and shift work toward specification, review and integration. Treat this as a hypothesis about coordination, not a quantitative extension of Brooks's law. In particular, instant onboarding and inevitable edit conflicts are not universal facts about agent systems. [@vandenbergagents2026]

Our proposed evaluation separates generation time, useful concurrency, integration failures, reviewer effort and accepted delivery. Measure the task graph and compare different orchestration designs rather than assume either perfect scaling or universal congestion. This also qualifies the opportunity described in Dan Luu's essay: making previously uneconomic work feasible need not remove dependencies or maintenance costs. [@luuambitious2026]

Voytko challenges idealized memories of old software through accounts of instability, data loss and other failures, while remaining concerned about current quality and lost understanding. He explicitly flags uncertainty in one remembered example. His account is a useful warning about baselines, not evidence that present-day AI improves or worsens quality. [@voytkoquality2026]

Our inference is methodological: use comparable systems, workloads and exposure periods, distinguish fault counts from failure severity, and track user harm and recovery. Generating more code at a fixed error rate does not by itself establish the rate of defects escaping review or their operational consequences. Historical comparisons also mix changes in hardware, distribution, functionality and security expectations.

### Science: Stewardship Is an Outcome to Study

OpenAI proposes different disclosure arrangements for three claimed results: direct release for mathematics, public artifacts plus an explanatory group for complexity theory, and deferred artifacts for physics. It acknowledges that initial collaborator selection creates information asymmetry. These arrangements make verification access, credit and the work of interpretation relevant research questions; they do not independently establish the claims. [@openaiunderstanding2026]

The [pinned ETH scope note](https://github.com/openai/math/blob/7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a/lean/docs/378.md) was read; the linked manuscript's existence was checked, not its proof. Formalization requires scrutiny of statements, assumptions and correspondence with the claimed theorem, not just a repository link. Distinguish Yang-Mills existence from the full existence-and-mass-gap problem. Named experts' participation is not their endorsement. The connection to Strogatz is a shift from obtaining artifacts to building shared understanding, not independent corroboration of his reported breakthroughs. [@strogatzfuture2026]

### Expertise: Do Not Leave Skill Preservation to Individual Vigilance Alone

Kärki argues for professional-community responsibility, beginning with identifying core skills and preserving opportunities to exercise and acquire them. This supplies a governance argument relevant to both retained competence and novice development. It does not show that a specific preservation program works. [@karkideskilling2026]

One empirical characterization requires qualification. Section 2 describes critical-thinking decay with reference to Lee et al.; the [primary abstract](https://www.microsoft.com/en-us/research/publication/the-impact-of-generative-ai-on-critical-thinking-self-reported-reductions-in-cognitive-effort-and-confidence-effects-from-a-survey-of-knowledge-workers/) reports a survey of 319 workers and perceived effort, not longitudinal measurement of skill decline. This does not refute the normative argument, but it limits one supporting inference. Do not pool self-reported effort, short-run errors, failure to learn and durable skill decay as a single endpoint. [@ref-712e3405f2; @shen2026]

Our proposed research question is which combinations of deliberate practice, feedback, unaided assessment and workplace incentives maintain capabilities while permitting beneficial AI use. Profession-led standards themselves require evaluation: they can protect essential competence but should not become untested requirements to preserve every legacy task.

### Employment: An Offer Is Not a Realized Job-Loss Count

Amy Coleman's public memo confirms a voluntary-exit program for selected teams in four countries. It is explicitly edited for external use and does not state the 60,000 figure. GeekWire separately attributes that eligibility count to Microsoft and reports no numerical acceptance projection. These sources establish the event more securely than reliance on a restricted headline alone. [@colemanexit2026; @bishopbuyouts2026; @stewartbuyouts2026]

Record three distinct quantities: eligible employees, accepted offers and net employment changes. The first is not the second or third. AI investment alongside a workforce program is not identification of AI-driven replacement. Equally, absence of an identified causal link is not evidence that AI has no employment consequences. Follow realized outcomes and role composition rather than classify this announcement as a productivity success or an observed mass replacement.

The memo and both reports concern the same event; their separate records improve traceability, not the number of independent studies. The public memo does not authenticate every word of the internal version reproduced by a reporter.

## Verification and Release Handling

Seven records were added to [November sources](../data/november-sources.json): the five suggestions plus the public Microsoft memo and GeekWire crosscheck. Staged total: **23**. Existing Lee and Shen references are reused, not duplicated or silently upgraded in October's database.

[Chrome observations](../november/browser-observations.json) document the alternative channel for the two blogs, the journal article and Business Insider. Full blog articles and the open-access journal body were read; the Business Insider page remains access-limited despite extensive DOM text. Publisher identity and links being checked is not proof validation. No trial or subscription was started, and no restricted article is redistributed.

Before November publication, recheck selected publisher pages and corrections, pin any revised research artifacts, seek independent specialist assessments, and update the workforce case only when outcomes are actually observed. October intake observations are not November release receipts. The live October article and bibliography are unchanged.
