# Balance self-review and October source-admission log

Review date and evidence cutoff: **13 October 2026**. Publication: **Does AI Help?**, version **2026.10.1**.

## Purpose and scope

This is an AI-assisted editorial self-review, not an independent external audit. It examines the complete current manuscript, the existing database's annotations and evidentiary roles, and the new sources listed below. It does not claim to have reread every full publication in the database. The inspected scope remains recorded for each source; a checked abstract is not relabeled as a full-paper assessment.

The question is whether benefits, failures, costs and refusal receive comparable scrutiny and prominence. Objectivity requires consistent admission and interpretation rules, not equal space for every viewpoint or an artificial 50:50 split.

## Findings and corrections

| Dimension | Finding before this follow-up | Correction |
| --- | --- | --- |
| Opening and conclusion | Important counterevidence was present, but an affirmative closing compressed heterogeneous results into an optimistic overall answer. | The conclusion now explicitly distinguishes helpful, harmful and unresolved settings and declines to estimate which predominates overall. |
| Negative experimental findings | METR and learning experiments were cited, but some adverse outcomes appeared principally as qualifications to gains. | The measured slowdown and comprehension losses are stated as outcomes in their own right. |
| Null downstream effects | Engineering bottlenecks were central, but popular headlines risked implying precisely zero benefit. | Preserve uncertainty and distinguish bounds on pass-through from exact zero effects. |
| Mixed interventions | Extra output could overshadow costs within the same study. | Pair output gains with review load, comprehension and downstream uncertainty; do not add unlike measures into a net score. |
| Community boundaries | Little coverage of actual restrictions or principled refusal. | Include official project policies and mathematical-community statements, separating blanket bans, conditional acceptance and organizational opposition. |
| Mathematical claims | Formal verification was discussed generally, without the current high-profile claim and challenge. | Separate announcement, theorem statement, certificate, translation fidelity, independent checking and institutional recognition. |
| Secondary reporting | Some new links cover research already present. | Retain useful analysis but label duplicate coverage and avoid counting it as independent corroboration. |
| Selection and interests | Limits were disclosed but neutrality could still be presumed from authorship. | Explicitly acknowledge AI authorship, business affiliation, developer/vendor incentives and this review's non-exhaustive selection. |

### What the evidence can support

- **Bounded tasks and selected operational workflows:** credible positive intervention evidence exists. It is stronger than a claim that adoption alone implies value.
- **Expert maintenance and comprehension:** credible adverse results exist in particular settings. Newer tools do not retroactively invalidate those findings; neither do those findings determine every future deployment.
- **Team delivery and organizational value:** activity gains often exceed downstream gains. Observational designs and imperfect outcome proxies prevent a universal causal estimate.
- **Learning:** assisted performance and retained learning are different outcomes; instructional design, populations and synthesis methods matter. A confidence interval containing zero is not proof of equivalence.
- **Science:** specialized contributions and selected validated workflows are credible. Autonomous novelty, explanation, semantic fidelity and collective scientific value remain distinct questions.
- **Employment and distribution:** aggregate and subgroup effects differ across periods and institutions. Neither displacement announcements nor favorable adopter comparisons settle an economy-wide counterfactual.
- **Refusal and governance:** documented objections and participation restrictions matter even when technically capable tools exist. They are evidence of policy and values, not automatically evidence of poor model performance.

There is no defensible tally of "AI-positive" versus "AI-negative" papers here. A single study can support several outcomes with different directions; papers overlap, outcome validity varies, and our search is selective. We therefore do not assert that the literature has a positive or negative majority. Where the evidence is stronger for one specified outcome, the article says so rather than manufacturing equipoise.

## Source-admission decisions

### User-suggested engineering and public-discussion sources

| Suggested source | Decision and role |
| --- | --- |
| [Chen and Stratton, author PDF](https://fion.ac/jellyfish.pdf) | Already included as `chenstratton2026`; retain the August version and strengthen the interpretation of output bounds. |
| [Vella and Blincoe, arXiv](https://arxiv.org/abs/2605.23135) and [v1 HTML](https://arxiv.org/html/2605.23135v1) | Already included as `vella2026`. These are one study, not two replications. |
| [Ars Technica](https://arstechnica.com/ai/2026/10/ai-coding-agents-generate-more-code-but-not-more-software/) | Add as `orland2026`, secondary reporting related to the existing firm study. |
| [Elsevier PII S0378720626000066](https://www.sciencedirect.com/science/article/abs/pii/S0378720626000066) | Retain as candidate. Access failed; title, authors and DOI were not reliably established. No findings enter the article. |
| [The Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/the-impact-of-ai-on-software-engineers-2026) | Add as `pragmatic2026`, with public-preview and self-selection limits. No claim of reading the paid report. |
| [TechTarget](https://www.techtarget.com/ai/tip/The-risks-of-AI-overreliance-in-software-engineering) | Add as `kompella2026`; follow selected links to primary research rather than inherit its categorical framing. |
| [ACM sustainability study](https://dl.acm.org/doi/10.1145/3786148.3788622) | Add as `iqbal2026`; a peer-reviewed workshop contribution, not a quantified lifecycle balance. |
| [Advisor Perspectives / Bloomberg commentary](https://www.advisorperspectives.com/articles/2026/10/08/ai-eating-software-investors-noticed?topic=small-cap) | Add as `mukherjee2026`, explicitly market commentary rather than measured productivity. |
| [Gates Notes](https://www.gatesnotes.com/work/make-ai-work-for-everyone/reader/a-turbulent-ai-era-and-critical-choices-to-make) | Add as `gates2026`, dated August 2026; a policy perspective, not future-outcome verification. |
| [CNBC jobs URL](https://www.cnbc.com/2026/10/11/ai-software-developer-jobs.html) | Retain as candidate after access restrictions and unsuccessful identification. The URL slug is not a verified title or result. |

Selected linked primary studies added: [the enterprise mandate study, v1](https://arxiv.org/abs/2607.01904v1) and [the author-hosted code-ownership experiment](https://personal.us.es/amarlop/wp-content/uploads/2026/03/More-Code-Less-Understanding-On-the-Impact-of-AI-Assistants-on-Developers-Productivity-and-Code-Ownership.pdf). Other linked studies already represented in the database were not duplicated.

### Official contribution policies

Added [QEMU's provenance policy](https://www.qemu.org/docs/master/devel/code-provenance.html), [Ghostty's pinned AI policy](https://github.com/ghostty-org/ghostty/blob/00c33eaf72af6c9b93d9fd8d54b6f7086612a95b/AI_POLICY.md) and [pinned contribution guide](https://github.com/ghostty-org/ghostty/blob/22f9233a0f7b85747483ce713411c67be4643d8f/CONTRIBUTING.md). These illustrate different policy choices; no prevalence estimate is inferred. GitHub revisions were obtained from official repository history within the cutoff. QEMU's live documentation should be rechecked at each release.

### Tao, mathematical practice and current proof claims

The retained primary discussion includes:

- [Math 2.0 slides](https://teorth.github.io/tao-web/slides/math-2-0-caltech-2026.pdf), delivered 9 October; [author announcement](https://terrytao.wordpress.com/2026/10/10/math-2-0/) dated 10 October.
- [Tao's living summary](https://teorth.github.io/tao-web/ai-views.html), inspected at its 11 October update, including its AI-assistance disclosure.
- [Mathematics in the age of AI, v1](https://arxiv.org/abs/2608.16753v1) and [Klowden and Tao, v1](https://arxiv.org/abs/2603.26524v1).
- [A Severe Misalignment of AI in Mathematics](https://mathandai.org/), with its publisher-displayed Zenodo identifier, and [AHM's statement](https://www.ahmath.org/statements). These represent distinct positions, not empirical replications.
- [Hales's guest essay](https://terrytao.wordpress.com/2026/10/09/what-mathematicians-should-know-about-the-lean-theorem-proverquestions-of-reliability-and-ai/) and [de Moura's maintainer postmortem](https://leodemoura.github.io/blog/2026-8-24-postmortem-for-the-kernel-soundness-bug-hunt/).
- [OpenAI's announcement](https://openai.com/index/navier-stokes-solution/), [written manuscript](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf), [pinned Lean artifacts](https://github.com/openai/NavierStokesAndEuler/tree/f9e8bc5b38b6e212696e8a30e3e91517af887bbd), [Clay's statement](https://www.claymath.org/news/navier-stokes-announcement/) and [the October translation critique, v1](https://arxiv.org/abs/2610.08144v1).

The review does not claim to have rerun the Lean artifacts, independently checked the long mathematical proof, or resolved the dispute. The two strongest claims to avoid are "OpenAI's announcement proves scientific acceptance" and "a translation mismatch proves every formal result false." Later revisions, technical responses and institutional decisions remain update priorities. Future events mentioned in slides are not counted as completed evidence.

## Search boundaries and reproducibility

Searches on 13 October used the supplied URLs; exact arXiv, DOI and PII identifiers; official project documents and revision histories; Tao's own linked writings; official OpenAI and Clay pages; and selected primary studies linked by the engineering analyses. Exact-identifier searches for inaccessible publisher and news pages were inconclusive. We did not circumvent paywalls or access controls. We followed relevant links selectively rather than recursively importing every citation, advertisement or comment.

New annotations live in `data/october-followup.json` and are merged reproducibly by `scripts/curate.py`. Bibliographic verification remains a separate release gate. Candidates are visible in the evidence map but excluded from checked citation exports. A failing or unresolved identity check must not be concealed merely to publish a more comprehensive bibliography.

## Remaining risks and next-release priorities

1. Obtain an independent human methodological review, including whether the narrative foregrounds some harms or benefits disproportionately.
2. Seek replications and longer-run production, learning and employment outcomes, including unsuccessful or abandoned deployments.
3. Audit the mathematical claim and critique through specialist responses, exact revisions and primary checking records.
4. Resolve the two inaccessible suggestions before attributing any findings; correct or remove them if identity proves wrong.
5. Improve prospective search reporting and outcome-level extraction. Do not turn overlapping reviews, press coverage or declarations into extra effect estimates.
6. Record retractions and corrections with the same prominence as favorable advances, and reconsider conclusions when evidence warrants it.
