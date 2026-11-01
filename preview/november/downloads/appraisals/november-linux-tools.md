# November Draft: Tool Use, Understanding and the Limits of Disclosure

Status: **unpublished November material**, inspected **16 October 2026**. This intake does not change the closed October article, database, exports, PDF, cutoff or tags. Some messages predate October's cutoff but were supplied and appraised after its closure; they belong to November's editorial intake, not a retroactive October expansion.

## Proposed Article Integration

Place the following passage in section 5, alongside the existing open-source policy discussion. Recheck policy implementation before publication and revise the existing Linux paragraph consistently; do not preserve contradictory descriptions of the current rules.

### Tool disclosure is not a test of understanding

Linux's October debate over the `Assisted-by` trailer sharpens the distinction between tool choice and accountable contribution. Torvalds opposes categorical tool bans while retaining the expectation that submitters understand their work. Pinchart argues that imperfect enforcement does not make explicit expectations worthless. Cook distinguishes declarations of origin from the explanation, testing and contributor responsibility needed for review. These are competing governance arguments, not measured productivity effects. [@torvaldstools2026; @pincharttools2026; @cooktools2026]

Levin's revised proposal would remove a structured trailer while retaining broader transparency and human responsibility. The proposal is not proof of an upstream merge: the pinned repository snapshot inspected on 16 October still contains the trailer requirement. Any November account must distinguish a policy proposal, reported support and the implemented text. [@levinassisted2026; @linuxassistants2026; @linuxgenerated2026]

Our interpretation is that neither disclosure nor manual prose alone certifies comprehension. A compiler analogy does not establish that probabilistic generation has the same failure profile as compilation. Equally, using AI to investigate, explain or draft a change need not eliminate human understanding. A more informative evaluation asks whether contributors can justify design choices, respond to unfamiliar objections, test failures and maintain the result. Such checks cost reviewer time and may affect newcomers differently. Their effectiveness remains a research question. Removing a trailer would also make adoption harder to infer from commit metadata; untagged contributions were never a dependable untreated comparison group.

## Sources and Positions

| Source | Evidentiary role and reading priority |
| --- | --- |
| [Torvalds, 13 October](https://lkml.org/lkml/2026/10/13/3242), `torvaldstools2026` | Primary requested source, read in local Chrome. Tool-neutral expectations, not an exemption from review or licensing. |
| [Pinchart, 13 October](https://lkml.org/lkml/2026/10/13/3226), `pincharttools2026` | Read his own reply separately from quoted participants. Norm-setting can matter even when perfect enforcement is unavailable. His Mesa comparison is not independently verified here. |
| [Cook, 14 October](https://lkml.org/lkml/2026/10/14/2388), `cooktools2026` | Primary follow-up, read in local Chrome. Useful practitioner testimony about drafting, review volume, trust and testing; not an independently measured benefit. |
| [Levin, v2, 13 October](https://lkml.iu.edu/2610.1/11683.html), `levinassisted2026` | Author-attributed patch and rationale on a public university mirror. Reports strong but non-unanimous summit support. [Version 1, 9 October](https://lkml.iu.edu/2610.1/02723.html) is the same proposal, not independent evidence. |
| [Larabel, Phoronix, 13 October](https://www.phoronix.com/news/Linux-Dropping-Assisted-By-Req), `larabelassisted2026` | Secondary reporting that describes a plan and acknowledges disagreement. Do not count it as another observation of outcomes. |
| [Posch, Hackaday, 15 October](https://hackaday.com/2026/10/15/linux-kernel-drops-ai-tag-requirement-uses-meta-ai-for-code-reviews/), `poschassisted2026` | Useful skeptical commentary, but its definite headline goes beyond the implementation status established here. Its broad statement about most open-source projects is not adopted as a prevalence finding. |

Additional primary replies from Jori Koolstra, Krzysztof Kozlowski and Jeff Layton were inspected while tracing v2 to its author. They are contextual acknowledgments, not extra independent studies. Search-discovered automated news summaries and anonymous reader comments are not promoted into evidence of effectiveness or representative community sentiment.

## What the Repository Check Establishes

The official GitHub API resolved `torvalds/linux` master to revision `2f2f7eeef8b0a1a9b9ca998231419873ccae8d4e`, committed 15 October 2026 at 22:10:26 UTC. Full files at that revision were inspected:

- [AI Coding Assistants](https://github.com/torvalds/linux/blob/2f2f7eeef8b0a1a9b9ca998231419873ccae8d4e/Documentation/process/coding-assistants.rst) still has the attribution section and trailer requirement. The queried file history's latest entry is the August documentation merge, not an October removal.
- [Kernel Guidelines for Tool-Generated Content](https://github.com/torvalds/linux/blob/2f2f7eeef8b0a1a9b9ca998231419873ccae8d4e/Documentation/process/generated-content.rst) retains transparency, testing, human understanding and maintainer discretion over acceptance or extra scrutiny.

This is evidence about that snapshot, not every subsystem or staging tree, nor a prediction of the final policy. A summit account, a posted diff and an upstream change are distinct events. Before November publication, check the exact merged revision and wording, not just a headline or an evolving documentation landing page. Reuse existing database IDs `linuxassistants2026` and `linuxgenerated2026`; do not add duplicate policy records as independent evidence. Details are in [the staged recheck record](../data/november-source-rechecks.json).

## Analytical Implications

1. **Understanding is an outcome, not a production method.** Tool-free writing may encourage reflection but cannot guarantee comprehension. Generated text may support explanation or conceal its absence. The learning and code-ownership experiments already in the review remain relevant; this thread does not overturn them.
2. **Norms and enforcement answer different questions.** Expectations can coordinate behavior without perfect policing. Whether a particular disclosure rule supplies useful information is a separate empirical question.
3. **Disclosure has several possible purposes.** Provenance, accountability, reviewer triage and research measurement should not be collapsed into one binary label. Context about how a tool was used may be more informative, but that benefit must be tested rather than assumed.
4. **Reviewer attention is part of the value pathway.** Faster submission generation is not evidence of faster accepted delivery. Assess explanation quality, review effort, rework, escaped defects and follow-through. Trust-based triage may reduce workload while making entry harder for unfamiliar contributors; that trade-off needs measurement.
5. **Policy changes can change the data.** An absent trailer does not establish non-use. A before/after count can mix changes in behavior, disclosure and recording rules. The proposal's tagged-commit count is not a census of AI adoption.

These are the review's hypotheses and interpretations unless explicitly attributed to a source. We do not infer a performance advantage from Torvalds's authority, infer inability from AI use, or interpret disagreement as a survey of the entire community.

## Integration and Verification

The six new sources are staged in [November sources](../data/november-sources.json), using the existing evidence-record fields, explicit methods, related-case links and actual inspection dates. They are **not yet merged into `data/sources.json` or October's citation exports**. During November preparation, admit them into the curation inputs and regenerate the November database and citations together with its actual manifest and cutoff. The passage above is draft article text, not a published update.

The [local Chrome observations](../november/browser-observations.json) document the alternative inspection channel for the three LKML messages. Their date is 16 October, not a fabricated November check. On promotion, add their IDs to the monthly browser watchlist and record fresh observations in the release ledger. Repeat selected inspections during the November release gate; these intake observations do not replace the monthly browser ledger. Do not infer an RFC Message-ID that was not exposed by the inspected archive view.

Before publication:

- Recheck the proposal's implementation and any later maintainer response, pinned to an exact upstream revision.
- Refresh source access and metadata, including local Chrome inspection where needed.
- Keep proposal versions and press coverage grouped as one discussion, not independent empirical corroboration.
- Verify any new claims about Sashiko, performance or other projects against their own primary sources before adding them.
- Seek comparative outcome evidence before endorsing any proposed screening practice as effective.
