# Source Verification Follow-up: 13 November 2026

The human coauthor opened eight previously problematic references in local Chrome. Their visible source pages, or the PDF cover in Accenture's case, were inspected directly on 13 November. Two Gravity Linux records were checked through the official website repository supplied by the human coauthor. No DNS configuration, certificate validation, browser protection or account settings were changed.

These are source-identity and bounded reading checks, not independent scientific validation. The November evidence cutoff remains **12 November**; inspecting an already available source on 13 November does not make it a newly published study.

## Ten Confirmed Records

| Record | Inspected scope and important distinction |
| --- | --- |
| [Hamza et al., original SSRN record](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6996078) | Title, three authors, posted 18 July 2026, written 25 June, abstract, two-version indicator and no-download notice. It remains linked to the later preprint and conference paper, not counted as another experiment. |
| [Hicks et al., OSF version 2](https://osf.io/preprints/psyarxiv/2gej5_v2) | Page uses *The New Developer* title; its embedded 55-page *AIST_ Preprint Update.pdf* uses *AI Skill Threat*. Both match the existing provenance record. Page version 2 and embedded file Version: 1 are different labels. Submitted 15 March 2025; edited 27 August 2025. |
| [Norwegian government recommendations](https://www.regjeringen.no/no/aktuelt/kunstig-intelligens-skal-i-all-hovedsak-ikke-brukes-i-barneskolen/id3166807/) | Dated 19 June 2026. Grade-specific guidance and exceptions for pupils who need AI-based support are explicit. This is a policy statement, not a learning-outcome experiment. |
| [Jabarian and Henkel, Voice AI in Firms](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5395709) | Original posting 18 August 2025; revision 11 September 2026; 127 pages. DOI 10.2139/ssrn.5395709 confirmed. The abstract's 12% is a relative offer-rate effect; people make final hiring decisions. Existing author-PDF appraisal supplies the detailed design reading. |
| [ActivTrak, 2026 State of the Workplace](https://www.activtrak.com/resources/state-of-the-workplace/) | Full HTML report now renders. Main sample covers 1,111 companies, 163,638 employees and over 443 million activity hours in 2023–2025; subsidiary datasets differ. Activity-based productivity and utilization proxies do not establish delivered outcomes, clinical burnout or AI causality. |
| [Luo et al., autonomous AI scientists](https://pubmed.ncbi.nlm.nih.gov/42832657/) | Three authors, PMID 42832657, DOI 10.1073/pnas.2610214123, online date 5 October and issue date 13 October 2026 confirmed. Abstract and conflict disclosure inspected, not complete final methods. |
| [Accenture, Our Talent Strategy](https://investor.accenture.com/~/media/Files/A/accenture-v4/investors/documents/accenture-investor-day-fy27-transcript-our-talent-strategy.pdf) | Official five-page PDF renders in Chrome. Cover shows 14 October 2026, Julie Sweet and Kate Clifford. Cover identity confirmed visually; earlier selected-passage reading retained. |
| [OpenAI, Patch the Planet](https://openai.com/index/coordinated-disclosure-of-critical-vulnerabilities/) | Title, author OpenAI, 21 October 2026 date and coordination account inspected. Maintainer-led fixes, Calif discovery, independent Wiz reporting and expectations about future discoveries remain separate propositions. |
| [Gravity Linux About, pinned official source](https://github.com/GravityLinux/website/blob/cfc74e6b3fcdb2f794fbf725464f27b506ad8d21/content/about.md) | FAQ explicitly attributes the initial fork to policy differences concerning LLM use. Latest file commit `cfc74e6`, 14 October 2026, changes the Discord invite, not the fork rationale. Self-description is not independent historical evidence. |
| [Gravity Linux LLM policy, pinned official source](https://github.com/GravityLinux/website/blob/2d7bbba836646caed9441ed998021b3f18c479da/content/policies/llm.md) | Latest file commit `2d7bbba`, 13 October 2026 at 22:02:14 UTC, clarifies commit-message requirements. LLM assistance is conditional on responsibility, clean-room provenance and disclosure; assisted code must carry `Assisted-By: LLM`, and a human must sign off. This is a policy description, not a legal opinion or evidence of effectiveness. |

## Gravity Linux Access Classification

Witold Bołt reports that DNS4EU blocks the live domain with the warning **“The content of this page can be harmful.”** He reports successful access from a mobile connection using different DNS. This explains why a locally unavailable page can still be a genuine source; it does not independently establish that the domain is either harmful or safe.

Earlier automated access and Chrome attempts recorded certificate-hostname errors. Those observations are preserved. They should not be restated as a proven defect in Gravity's origin-server certificate: the local filtering path was not independently diagnosed.

The official repository was inspected in Chrome and crosschecked through GitHub's file-history/content APIs. The fallback was deliberate, not an HTTP redirect. Both canonical live URLs remain in the bibliography; the evidence records additionally expose immutable source-file links and accurate revision dates. October's records remain unchanged.

## Verification Record

Append-only dated observations appear in `release-browser-checks.tsv` and the assembled browser-verification ledger. Failed 12 November attempts remain alongside successful 13 November checks. An inspection of a landing page or cover is not relabeled as a full-text reading. No third-party PDFs are redistributed.

The four other previously flagged records are the Daily Californian article and the three LKML messages. They were not among the user-opened reference tabs in this follow-up; their earlier access limits remain unless a subsequent check clears them. Consult the latest identity audit for the current strict-gate result, including any new transient failures.

## New-network Recheck, 08:57–08:58 UTC

After the human coauthor reported switching networks and DNS, local Chrome inspection produced the following results. This records an access change, not an independently controlled test of DNS providers or website safety.

| Source | Observed outcome |
| --- | --- |
| Gravity Linux About | Live canonical page loads normally and its FAQ matches the earlier pinned official source. |
| Gravity Linux LLM policy | Live canonical policy loads normally and matches the repository content. Existing immutable links remain useful provenance. |
| HESA | Initially displayed an intermediate security-check page, then loaded successfully. Title, 27 January 2026 date, HESA/Jisc attribution and institutional text confirmed at 08:58:00 UTC. |
| Daily Californian | Still shows Cloudflare's access-denied page. Article body not inspected. |
| LKML: Torvalds | Anubis bot-check page rather than message content; a further normal navigation failed. No challenge bypassed. |
| LKML: Pinchart | Still returns HTTP 502. |
| LKML: Cook | Navigation fails with an HTTP response-code error. |

HESA distinguishes an overall UK enrollment decline in 2024/25 from growth in computing subjects (7%) and artificial intelligence (21%). These are subject/year/geography-specific official statistics, not an AI-caused enrollment effect. The source is now identity-confirmed; the initial empty page is retained as an intermediate observation rather than the final status.

The **four remaining strict identity blockers** are the Daily Californian article and three LKML messages. Earlier failed attempts, the official-repository fallback and successful direct visits remain dated separately in the append-only ledger. No network setting, certificate validation, bot protection or account setting was weakened.

## Subsequent Editorial Decision

The human coauthor explicitly instructed: flag the four remaining inaccessible entries as unverified and continue. They are therefore **retained as currently unverified contextual records, non-blocking for November**, not promoted to confirmed identities. Earlier references to four blockers above describe the state before this decision.

The identity-bound policy in `access-deferrals.json` expires on 30 November 2026 and is reconsidered next month. It does not clear mismatches, missing pages, changed identities or unrelated failures. Applying the decision does not issue new requests, refresh failed-access dates or create successful browser observations. Readers see the unverified status in the evidence list, article reference previews, article methods and citation-manager notes.
