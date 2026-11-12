# Asahi, Omarchy M and the Distribution of AI's Benefits

Case appraisal, 12 November 2026. Public statements, selected repository evidence and online coverage were inspected. This is a governance case, not a controlled productivity study, a complete provenance audit or legal advice.

## What happened, and why Omarchy is central

It would be misleading to present the connection to Omarchy as merely incidental. Omarchy's own [11 September announcement](https://omarchy.org/news/2026/09/introducing-omarchy-m/) explicitly positions its Apple Silicon effort as completing Asahi's work and celebrates agent-assisted development. Its [4 November release announcement](https://omarchy.org/news/2026/11/omarchy-4-5/) repeats that framing. DHH subsequently answers questions about Asahi directly. Several accounts connect the events, including [Omarchy Central](https://omarchycentral.com/news/asahi-linux-is-moving-to-gpl-version-2-or-later-and-dhh-says-it-changes-nothing-for-omarchy/), [Sesame Disk](https://sesamedisk.com/asahi-omarchy-license-fight/) and the [It's FOSS interview](https://itsfoss.com/interview/dhh-asahi-omarchy-take/). These establish a prominent public interpretation, not a measured community consensus or independent forensic corroboration.

On [7 November, James Calligeros announced](https://asahilinux.org/2026/11/progress-report-7-3/) a transition toward GPLv2-or-later and alleged unattributed reuse and LLM-assisted concealment of origins. Asahi did not name Omarchy or identify offending commits. The inference that Omarchy is an important context is therefore stronger than the evidence that it committed each alleged act. We retain that distinction explicitly.

The [10 November interview with DHH](https://itsfoss.com/interview/dhh-asahi-omarchy-take/) provides his direct response: he defends reuse, asserts compliance and says the no-AI contribution rule prevents upstreaming. These are his claims; the interview does not audit compliance or show a particular submitted patch being rejected. A policy-based explanation is not a demonstrated history of every attempted contribution.

## Funding changes the fairness question

[The Register's 17 September account](https://www.theregister.com/software/2026/09/17/omarchy-gains-185m-in-backing-fresh-converts-and-fierce-critics/5296780) reports approximately $18.5 million in announced backing. This includes multiyear commitments and AI tokens, not simply cash already received. Current [patron](https://omarchy.org/patrons/) and [foundation](https://omarchy.org/foundation/) pages corroborate substantial financial and in-kind support but are not audited accounts. We do not construct an exact current total from changing pages, or assume it all funds Apple Silicon work.

**Our interpretation:** a well-funded, visible downstream project built on painstaking upstream work can change who captures attention, donations and bargaining power. That concern remains intelligible even if reuse complies with a license. Conversely, packaging, integration, accessibility and reaching new users can be genuine contributions rather than merely appropriation. Funding alone proves neither wrongdoing nor superior engineering, and AI may amplify an older upstream/downstream tension rather than create it.

The fairness issue is therefore not exhausted by asking whether a fork is permitted. Relevant questions include whether foundational contributors remain visible, whether downstream funding supports shared maintenance, and whether maintainers can decline work they cannot responsibly certify. This review has not established that Omarchy caused a loss of Asahi donations or that sponsors deliberately displaced the upstream project.

## What repository inspection actually establishes

| Observation | Evidence and boundary |
|---|---|
| The AI policy predates this November dispute | The existing Asahi policy citation dates its revised text to 8 September. It is inaccurate to describe it as newly invented after Omarchy 4.5. |
| A component changed license earlier | m1n1 commit [`ce2b8a4`](https://github.com/AsahiLinux/m1n1/commit/ce2b8a43cea4220b602af1005dc9dbfc59c9624e), dated 2 October, replaces MIT; the README specifies GPL version 2 or later. This is not an audit of every Asahi repository. |
| Omarchy documents its dependency | The inspected [Mac repository snapshot `667500c`](https://github.com/omacom/omarchy-mac/tree/667500c5eefab78424af66350f5ea7bf40fdede6) acknowledges Asahi Alarm. A statement that Omarchy never credits Asahi would be false. That acknowledgment does not settle commit-level attribution disputes. |
| Native installer and legacy script are distinct | The [installer snapshot `c07e54c`](https://github.com/omacom/omarchy-mac-installer/tree/c07e54c2134a8ec1415e7e2b917589ae1d3d7dc9) documents dependency licensing separately from its own MIT code. Its source lock pins Asahi installer v0.9.2 and m1n1 [`06a4601`](https://github.com/AsahiLinux/m1n1/blob/06a4601a351ebfd1abb6abba9a44c34e40d94776/LICENSE), whose license was checked as MIT. This is source-document evidence, not verification of every shipped binary. |
| The transition is not fully reflected in policy pages | Asahi's [copyright policy](https://asahilinux.org/copyright/) still contains permissive-licensing guidance. Its source front matter dates publication to 5 January 2021; the inspected revision includes July 2026 changes. It should not override the newer announcement or be used to imply that the entire relicensing is completed or invalid. |

No installer, driver, untrusted project script or model was executed. No exhaustive comparison of personal forks, accepted contributions, missing notices or generated rewrites was performed.

## Five distinctions the review must preserve

1. **License permission versus social reciprocity.** The [MIT text](https://opensource.org/license/mit) permits broad reuse, including sale, but requires retention of copyright and permission notices in copies or substantial portions. It is not permission to remove required notices. Public praise and Git authorship are related but distinct forms of credit.
2. **Contribution rules versus downstream rights.** A project's refusal of AI-assisted submissions does not, by itself, prohibit all licensed downstream reuse. A downstream license does not oblige upstream maintainers to accept a contribution. Asahi's [AI policy](https://asahilinux.org/llm-policy/) concerns ethical and provenance risks, not merely whether generated code runs.
3. **Copyleft versus a noncommercial or anti-AI restriction.** The inspected GPLv2 text permits commercial distribution, distinguishes aggregation and derivative works, and specifies source obligations. Copyleft is not a prohibition on forks or a general AI ban. Nor does merely putting source somewhere prove compliance. Application depends on the actual artifact and distribution arrangement.
4. **Rewriting versus demonstrable independent provenance.** Changed identifiers or an LLM rewrite do not establish independent creation. An allegation of concealment is also not self-proving. A defensible investigation needs the original and resulting artifacts, dates, notices, licenses and a traceable development process. A publicly available development branch is not the same thing as private leaked Apple material.
5. **Tool disclosure versus credit to prior human work.** Saying that an agent helped does not credit the people whose code, experiments or hardware knowledge enabled the result. Conversely, an AI-assisted contribution can contain valuable original work. Copyright ownership, scholarly/community credit and responsibility for maintenance are different questions; none is resolved by an AI-generated label alone.

These are scoped readings and analytical distinctions, not conclusions about infringement, statutory fair use, model-training rights or ownership of particular outputs. Claims that a rewrite automatically erases obligations, or that the legal merits are already settled, are not adopted.

## Why this belongs in Does AI Help?

Our interpretation is that benefit must be evaluated at ecosystem level as well as project level. Faster integration may benefit users while opaque provenance, duplicated maintenance, loss of credit or weakened cooperation impose costs elsewhere. The case makes those possible mechanisms visible without measuring their size or establishing that they occurred in every instance.

There are also choices between unrestricted agent use and complete refusal. Gravity's existing [LLM policy](https://gravitylinux.org/policies/llm/) permits disclosed assistance while retaining human responsibility and prohibiting provenance laundering. This is a governance alternative, not evidence that its safeguards are effective. Gravity, Omarchy and other Apple Silicon efforts must not be treated as one interchangeable project or automatically assigned responsibility for one another's actions.

Useful future evidence would include specific disputed diffs, preserved author trails, accepted upstream fixes, source/binary correspondence, maintenance costs and funding flows. Without those, the case informs the review's analysis of incentives and accountability, not an estimate of AI's net productivity effect.

## Source selection and access

Nine new records are admitted; policies already in the database are reused rather than duplicated. Secondary coverage helped locate primary material but is not treated as multiple independent confirmations of allegations. X returned an access error, so social posts are not represented as directly verified. GNU endpoints timed out; the GPLv2 text was read in m1n1's repository instead. No Chrome receipt or release-wide audit is claimed.

A related preprint, [The AI Attribution Paradox](https://arxiv.org/abs/2512.00867), was screened but not admitted as empirical support in this batch: its arXiv submission date, internal date and stated data window need reconciliation, and its keyword-selected sample cannot establish general AI-use prevalence. No claim of fabrication is made. The [search log](../november/search-2026-11-12-omarchy.json) records selection and limitations.
