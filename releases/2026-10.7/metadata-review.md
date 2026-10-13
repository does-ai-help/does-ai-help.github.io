# October 2026 metadata review

## Repository dates for four previously undated pages

Version 2026.10.7 replaces four undated entries with source-backed dates. Repository files were matched to the live page contents, and public GitHub or Forgejo file-history APIs supplied the commit identities and timestamps. The evidence database retains pinned file links, authored and committed timestamps, date type and date basis. None is inferred from the inspection date.

| Source | Citation date | Basis and inspected revision |
| --- | --- | --- |
| Gravity About | 12 September 2026 | File's initial-import/latest-affecting commit, [b1a74639](https://github.com/GravityLinux/website/blob/b1a74639fe8931640f7f8eecb99f8b77f257463a/content/about.md). Not a fork or deployment date. |
| Gravity LLM policy | 15 September 2026 | Current file revision [d0bdd178](https://github.com/GravityLinux/website/blob/d0bdd17839e9975a00d9201e842705acf2ca5a69/content/policies/llm.md), committed 15 September but authored 12 September. |
| Zig Code of Conduct | 22 November 2025 | Date declared in the source, already present in the [introducing commit](https://codeberg.org/ziglang/ziglang.org/src/commit/f768f750524efd7595252759fcee1a20925a358b/content/en-US/code-of-conduct.smd). Current [0601a435 revision](https://codeberg.org/ziglang/ziglang.org/src/commit/0601a4358fec6fe445688face107a5e914b68a16/content/en-US/code-of-conduct.smd) is dated 25 September 2026 in -07:00 (26 September UTC); AI rules were clarified on 24 May 2026. The citation year does not backdate the expanded rules. |
| Asahi LLM policy | 8 September 2026 | Publication date declared in [6eccc031 source](https://github.com/AsahiLinux/AsahiLinux.github.io/blob/6eccc0319839a9e21d89977f98140821369c3255/content/llm-policy.md): 09:00 in +10:00 on 8 September. Git committed the revision on 7 September UTC. |

Repository introduction, source-declared publication, later revision, first deployment and policy adoption are distinct events. Earlier undated snapshots are preserved; these dates establish the cited documents, not the effectiveness of the policies or their first historical adoption.

## Open-source and benchmark follow-up

Version 2026.10.6 dates QEMU's repository introduction of the AI rule to its 24 June 2025 commit, distinguishing the proposal's authored date and the current file's 22 May 2026 formatting revision. GIMP, Redox and Linux entries explicitly date document revisions, not original AI adoption. Undated live policies remain undated; the inspection date is not a publication date.

The SWE-bench repository README recommends the [ICLR 2024 paper for SWE-bench and Verified](https://openreview.net/forum?id=VTF8yNQM66), the [ICLR 2025 Multimodal paper](https://openreview.net/forum?id=riTiq3i21b), and [SWE-smith for Multilingual](https://arxiv.org/abs/2504.21798). The [authors' pinned README](https://github.com/SWE-bench/SWE-bench/blob/e2c13307b6cf7764a50958b9c8bfbfb3f72cb70a/README.md) supplies the exact entries in the separate `swebench-recommended.bib` download. These recommendations are not three additional appraised experiments; OpenReview was access-blocked. The original preprint remains dated 2023, and the cited README revision is dated 2026.

The automated checker may use GitHub's official raw-file route, preserving repository, ref and path, only when a blob page returns a temporary 502/503/504 service error. It records the original failure and alternate URL/hash, and still requires a matching document heading. Local Chrome also displayed a GitHub service-error page during this update; that observation is not recorded as identity confirmation. This fallback neither overrides conflicting identities nor treats a missing page as available.

## Registry clarification

Version 2026.10.5 clarifies that Crossref successfully returns the Hicks version DOI, its older registered title and 2025 year. The earlier DataCite 404 was a query to a different registry. It must not be interpreted as an absent DOI. Chrome separately resolves the OSF page/PDF title difference and dynamic rendering. The initial 2026.10.4 snapshot remains preserved; findings and source counts are unchanged.

## Supplied documents and matched online versions

Version 2026.10.4 records three PDFs supplied by the human coauthor, matched to their online versions in local Chrome. Three inherited candidates now have established identities. The Hamza study's original SSRN 6996078 record is not the supplied 7070979 PDF; the actual SSRN version menu links them, and the published ESEM version has a completed DOI and 5 October 2026 publication date. The Hicks OSF page retains an older title but embeds the supplied revised-title PDF; both are recorded. Chess-paper first posting and its 2026 revision are kept separate. The [document follow-up](document-followup.md) records reading scopes, hashes, reporting questions and limitations. Financial Times remains inaccessible to the coauthor and unappraised here.

## Publication-date follow-up

Version 2026.10.3 resolves 16 of the 18 undated checked references. Each correction retains its evidence in `date_basis`, visible in the evidence map and downloadable exports. Exact dates are used only where supplied: IZA provides March 2026, while DORA's v. 2025.2, JetBrains' 2025 edition and the ICSE 2025 conference entry establish years but not publication days. Ramp's landing page uses the dated launch announcement, explicitly distinguished from a paper revision. Faros, Sonar and Yahoo provide publication dates in primary structured metadata, inspected in the pages retrieved on 12 October.

SWE-bench Verified was published on 13 August 2024 and updated on 24 February 2025. Its named author list and OpenAI publisher credit were rechecked in local Chrome; the earlier receipt is preserved. SEI credits Michael Hilton in addition to its two headline authors. The Springer/Apress book identifies Sadowski and Zimmermann as editors; exports preserve that role rather than making them authors.

QEMU's live code-provenance documentation and the SWE-bench repository remain undated: neither the access date, current copyright year nor the associated research paper's year establishes when the cited live resource was published. Candidate records without established identities are not assigned speculative publication years and remain excluded from checked-citation exports.

## Local Chrome follow-up

Version 2026.10.2 adds actual local Chrome observations for 15 selected resources. These are recorded separately from the earlier indexed-primary exceptions, which are not retrospectively labeled as Chrome checks. The Elsevier PII now resolves to Chang and Huang's journal paper and DOI 10.1016/j.im.2026.104306; the CNBC URL resolves to Corynn Winston's dated article. Newly observed supporting bylines and dates are retained in `browser-source-updates.json`. Scope limits, subscription boundaries and the genuine Kent Beck newsletter redirect are documented in the public browser ledger. No scientific correctness is certified.

Checked by GPT 6.1 using primary pages and live Crossref metadata on 13 October 2026 (Warsaw time). This is AI-assisted editorial verification, not an independent human audit or scientific replication.

## Title differences

The 13 October follow-up records additional identity edge cases. QEMU's short *Code provenance* heading has the explicit full-page title alias *Code provenance — QEMU documentation*. AHM's statement appears under a lower-level heading on a generically titled statements page. The OpenAI manuscript's first-page title is split into `NA VIER` by one PDF parser; primary PDF retrieval and Poppler establish the intended heading. These observations are documented rather than handled by lowering the global title-match threshold.

New expiring confirmations cover those inspected identities and restricted primary pages for Gates, Mukherjee and OpenAI, plus an intermittently timing-out Clearinghouse page. They are explicitly AI-assisted identity checks, not independent human checks. Thomas Hales is the author of the Lean guest essay; Tao is its host. The code-ownership manuscript's 2021 running header is a template artifact, while the author's publication list identifies the 2026 journal work. DOI identity remains unestablished for that paper and is not fabricated.

- Stack Overflow's page title is *AI | 2025 Stack Overflow Developer Survey*; the earlier label reordered these words. The canonical citation now uses the page title.
- The SPACE framework has the full subtitle on ACM Queue and the shorter *The SPACE of Developer Productivity* in Crossref. Authors, DOI 10.1145/3454122.3454124 and 2021 year agree; both titles are explicitly recorded.
- Cambridge's *Generative AI in Computer Science Education* has the subtitle *Challenges and Opportunities* in publisher citation metadata but not Crossref. Authors and DOI agree; the shorter registry title is an explicit alias.
- *Speed at the Cost of Quality* has a longer title in its November 2025 arXiv version and a shorter 2026 conference title. The same authors and associated DOI link these versions. They are not independent studies.

## Date and authorship warnings

The five supporting arXiv records `ref-619316fd46`, `ref-1fb28b41e8`, `ref-cebccd633f`, `ref-e71e370e4c` and `ref-59e035c44a` have 2025 submission dates and associated DOI registry publication dates in 2026. The database year describes the cited arXiv version; the DOI leads to a later published version. These are identity-consistent version differences, not additional independent findings. Substantive appraisal of these supporting records remains pending.

FunSearch (`funsearch2023`) was published online in December 2023 and appeared in the January 2024 Nature issue; publisher issue metadata and registry online dates differ. The review uses 2023 for the chronological development. Both dates are visible in the audit.

DORA 2025 (`dora2025`) was initially attributed to its organization. The primary Google Research page supplies named report authors. Corporate versus personal authorship is not an unrelated work; the source's named authors are now retained in the canonical record.

## Restricted access

HESA's exact title and date are identifiable in indexed primary HESA material although direct automated retrieval returns 403. Two OpenAI pages are available through primary web retrieval but intermittently block the script. The JetBrains coding-tool survey page is accessible through primary web retrieval but intermittently returns an empty HTTP 202 response to the script. Documented, expiring exceptions record the evidence and AI reviewer rather than pretending that direct access succeeded. A future release must refresh this evidence. Metadata evidence confirms identity, not claim validity or current unrestricted access.

Candidates remain excluded from checked-citation exports. Generic site titles such as “OSF” do not establish the identity of an intended paper. A working link is never used by itself to promote a candidate.
