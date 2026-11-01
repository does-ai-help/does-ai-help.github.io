# Supplied-document follow-up - 13 October 2026

Witold Bołt supplied three downloaded PDFs and opened their article pages in local Chrome. GPT 6.1 inspected bibliographic identity, selected substantive sections and source-version relationships. The supplied files remain local: downloading or supplying a PDF is not permission to redistribute it. Public records contain original annotations, identifiers, filenames, checksums and scoped observations only. Nothing here is independent replication, a human full-text audit, or certification of scientific correctness.

## Agent participation and developer behavior

**Canonical publication:** Hamza, Siemon and Awan, [Does Working with AI Agents Change How Developers Code, Test, and Review?](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESEM.2026.67), published 5 October 2026 in ESEM's Emerging Results, Vision & Reflection Track. DOI: [10.4230/LIPIcs.ESEM.2026.67](https://doi.org/10.4230/LIPIcs.ESEM.2026.67).

**Version mapping:** the inherited [SSRN 6996078](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6996078) was posted 18 July 2026 and gives 25 June as Date Written. The supplied `ssrn-7070979.pdf` belongs to [SSRN 7070979](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7070979), posted 24 July, written 7 July. The actual Chrome version menu links the two records. The original record has no downloadable PDF. The supplied 12-page preprint contains unfinished proceedings-template fields; its incomplete LIPIcs DOI is not a valid publication identifier. The publisher's linked 13-page PDF establishes the completed DOI and adds more explicit discussion of proxy validity and adoption timing.

The sample consists of 669 developer-repository pairs in 103 exposed repositories and 228 control pairs in 148 repositories. Entry requires persistent contribution; only merged PRs are analyzed. The design combines within-developer comparisons, distributional difference-in-differences, fixed-effects checks and limited repository matching. Adoption means the first visible autonomous-agent PR, not first use of any AI coding tool. Controls split their histories at their own median PR date, rather than sharing a naturally occurring intervention date.

The reassuring result is selective: longer descriptions and small test-change associations, with no clear coding-volume decline. Apparent review changes do not remain significant after comparison with controls. That makes this useful against simplistic automation-complacency narratives; it is not proof of higher software quality or of zero review harm. Longer descriptions need not be clearer; test-file inclusion need not mean stronger assertions; comment counts need not measure review quality. Controls may already use other AI assistants, and workflow changes can coincide with agents.

**Reporting questions, not resolved here:** the text reports seven of ten significant before/after findings failing the comparative check, while Table 5 appears to list ten significant before/after metrics with four comparatively supported ones (which would leave six). Table 1's 349/344 median pre/post days also needs reconciliation with the stated seven-month windows. Do not repeat the headline 70% misattribution estimate as an independently established statistic. These discrepancies merit clarification or replication, not an accusation that the whole study is invalid. Test-change effects can be distributional even when median deltas are zero; that alone is not a contradiction.

**Inspected:** supplied preprint identity, methods/results and version fields; published PDF abstract, methods, Tables 1-5 and discussion. The replication package was not executed. The three publication records belong to one study family. AIDev overlap with other repository studies is marked, without assuming identical analytic samples.

## Assistance design and learning in chess

Poulidis, Hamsa Bastani and Osbert Bastani, [Self-Regulated AI Use Hinders Long-Term Learning](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5604932), DOI [10.2139/ssrn.5604932](https://doi.org/10.2139/ssrn.5604932). Chrome confirms first posting on 16 October 2025, Date Written on 1 October 2025 and revision on 1 August 2026; the supplied artifact has 63 pages.

The experiment spans 14 weeks, including 12 weeks of training. It recruits 306 active chess-club students; the main analysis contains 216 completers. Both conditions receive automatically triggered tips; only one adds a button for solution-revealing advice. It is not an AI/no-AI trial, and its engine is Stockfish 16.1 rather than an LLM.

Table 1 reports adjusted differences of -0.749 on a 0-6 test-game scale and -1.106 on a 0-10 quiz scale, with HC1 standard errors 0.207 and 0.250. The much-cited 30% versus 64% concerns relative improvements in test-game scores, not proportional growth in expertise. The authors explicitly warn that test scores and latent chess ability are not linearly interchangeable. Both arms improve; an additional comparison with other chess students is observational and cannot establish an AI treatment effect.

Random assignment makes the assistance-design contrast informative. Important limits are approximately 29% attrition, analysis conditional on completion, financial incentives, a selected motivated chess population, and a reliable solution-revealing engine. Reported absence of differential attrition is reassuring but not sufficient to rule out all selection. Productive struggle and engagement are plausible mechanisms; causal mediation adds assumptions beyond random treatment assignment. Preregistration is reported and linked, but compliance with the preregistered plan was not independently audited here.

**Inspected:** title/abstract, design, main Table 1, mechanism discussion and assumptions, boundary conditions and selected appendix details on Stockfish, attrition and external activity. No raw-data reanalysis. Related conference abstracts or faculty explainers are not additional experiments.

## AI Skill Threat, culture and identity

Hicks, Lee and Foster-Marks, [OSF version 2](https://osf.io/preprints/psyarxiv/2gej5_v2), submitted 15 March 2025. The site retains *The New Developer: AI Skill Threat, Identity Change & Developer Thriving in the Transition to AI-Assisted Software Development*, but embeds the supplied 55-page PDF titled *AI Skill Threat: How the Structure of Developers' Beliefs about Software Development Ability Impacts Their Psychological Resilience During Rapid Technology Shift*. Its first page also dates the draft 15 March 2025. Chrome shows last edited 27 August 2025; that is not substituted for submission. The preprint's version number and embedded file's internal version number are distinct.

The publisher displays DOI [10.31234/osf.io/2gej5_v2](https://doi.org/10.31234/osf.io/2gej5_v2), and DOI resolution redirects to OSF. The subsequent Crossref audit confirms its older registered title and 2025 year. Initial DataCite lookups returned 404 because that is not the registry holding this DOI; those responses do not mean that the DOI is missing or unregistered. Chrome remains useful because automated retrieval of the OSF application yields only a generic site title. This clarification supersedes the initial registry-access wording in the preserved 2026.10.4 snapshot.

The volunteer survey includes 3,267 respondents: 2,472 individual contributors and 795 managers/leaders. Recruitment used social media, professional lists and Pluralsight platforms. Measures concern perceived identity threat, beliefs, belonging, reported productivity/effectiveness and intended behavior. Competitive and innate-brilliance beliefs accompany more threat; learning culture and belonging accompany more favorable experiences. Some hypotheses and group contrasts are not supported. Demographic responses are optional, so subgroup denominators differ from the full sample.

These are important experiences, not direct evidence of engineering throughput, actual retraining or future skill loss. Cross-sectional mediation does not establish a causal cultural pathway, and respondents' skepticism about AI accuracy is not disproved by an association with threat. Group results should not be used to diagnose individuals or discount concerns about discrimination, security or employment. Developer Success Lab/Pluralsight affiliations and recruitment channels warrant disclosure; OSF declares no conflict of interest. Public raw data are unavailable because participants did not consent to release. Measures and preregistration links are provided, but were not independently validated here.

**Inspected:** first-page identity, abstract, recruitment, measures, principal results and limitations, with supplementary measurement details sampled. This is a preprint, not a confirmed peer-reviewed journal article. Preserve both titles as version aliases rather than counting them twice.

## Artifact provenance

| Artifact | Pages | SHA-256 |
| --- | ---: | --- |
| Supplied `ssrn-7070979.pdf` | 12 | `d5a518024677df9ecbf9f51dcc820a968b493f165bb1b0e87813406b6973f410` |
| Supplied `AIST_ Preprint Update.pdf` | 55 | `576ea4b6b35ac4ca1d1198e077dc77572b8f85976bba60ba977e1408cd076560` |
| Supplied `ssrn-5604932.pdf` | 63 | `42b052fff67d466c52463948560f33507dd1a1a53c133881a99b416cdbfae7ec` |
| Publisher `LIPIcs.ESEM.2026.67.pdf` | 13 | `342b776c023a75dd9a17cf1b0494e6e264c4358340fa48a6e58cdd5cb545ab0f` |

Browser identity receipts are appended to the existing public ledger; the four affected online records are now mandatory monthly Chrome revisits. If a revised PDF changes, reassess version identity and the passages supporting claims. CI checks recorded provenance but cannot reopen private Downloads files or certify that the supplied artifact remains the current online revision.

## Financial Times

The coauthor reports that the [Financial Times suggestion](https://www.ft.com/content/9183a122-10b7-4707-a728-b61ab50da378) is paywalled and unavailable to him. It remains an unappraised candidate, excluded from empirical claims and checked-citation exports. We neither bypass the paywall nor substitute another article's text or metadata. Lack of access says nothing about the truth of the intended article.
