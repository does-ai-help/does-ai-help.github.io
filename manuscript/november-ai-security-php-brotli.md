# AI-Assisted Security Research: PHP2Shell, Brotli and the Race to Remediate

Evidence inspected **27 October 2026**. Targeted narrative review for the unpublished November release. October remains unchanged. This is research synthesis, not an operational security advisory or an exhaustive systematic review.

## Main Assessment

These cases provide concrete evidence that AI-assisted teams can expose consequential weaknesses in mature software. They also show why discoveries alone are not the right measure of public benefit. Reliable validation, maintainers' capacity, coordinated disclosure and deployment of fixes determine whether capabilities become protection. The same capabilities can assist attackers. Current evidence supports a valuable defensive capability, not a measured net reduction in internet-wide harm.

Three distinctions are essential:

- **Prevalence is not exploitability or compromise.** PHP's popularity does not mean that 70% of websites were breached, or that a universal exploit works against them.
- **Discovery, demonstration and operations are different outcomes.** A crash, laboratory code execution, a honeypot attack and a broad real-world campaign are not interchangeable.
- **One dependency flaw can generate many product advisories.** Node.js, .NET and PHP Windows notices for the same Brotli CVE are propagation of one root vulnerability, not three independent AI discoveries.

## 1. PHP2Shell: Capability Meets a Longstanding Engineering Problem

The maintainer advisories identify two critical PHP runtime issues: out-of-memory corruption, **CVE-2026-109618**, and stale global state, **CVE-2026-109619**. They concern memory management and request lifecycle behavior rather than a defect in a particular site's PHP application code. Consequences include memory disclosure or unauthenticated code execution under affected conditions. [@phpoom2026; @phpstale2026]

The history qualifies the simple story of an AI discovering an entirely unknown flaw. The PHP Foundation traces signs of the OOM problem to 2024 and reports that difficult compatibility choices, limited resources and its decision process delayed a fix. Later demonstrations made exploitability concrete. This is evidence about the discovery-to-remediation process, not merely detection accuracy. [@phpfoundation2026]

Calif's researcher describes historically informed, human-directed use of generally available models. Wiz describes AI assistance in discovery and adapting chains across selected applications. These are substantive technical case studies, but neither establishes an autonomous find-everything agent or a controlled speedup over an equally resourced human team. Their accounts refer to overlapping flaws and should not be counted as independent outcome studies. [@califphp2026; @wizphp2026]

### What Does “70% of Websites” Mean?

The primary W3Techs page inspected in Chrome reports **69.2% of websites whose server-side programming language it knows**, not an unqualified census of all websites. This is a daily prevalence statistic, not a count of vulnerable deployments or attacks. The headline's rounded figure loses both the denominator and the distinction between usage and exposure. [@w3php2026]

Censys supplies a different unit: **services**, defined as an IP address or hostname plus port. Its 27 October, 21:15 UTC snapshot classifies approximately **32.6 million services** as still on affected reported versions. Approximately **58%** of detected PHP services hide their version. Backports can retain version labels, and scans lag deployment. Consequently, the classified count is not a confirmed exploitability or compromise count. Do not convert services into unique websites, machines or organizations. [@censysphp2026]

The [dated observation ledger](../november/security-observations.json) preserves the exact figures and definitions. Changing detections, population coverage and upgrade visibility mean that dashboard movements are not automatically a causal estimate of patch effectiveness.

## 2. Exploitation Evidence Changes Over Time

| Date or observation scope | Finding | What it does not establish |
| --- | --- | --- |
| 17 October, reported by AWS on 21 October | MadPot recorded an exploitation attempt before public disclosure. | Successful compromise, attacker identity, AI use or the source of exploit knowledge. |
| 21 October | PHP published fixes for the two original CVEs. | That every deployment was already protected. |
| 23 October, CrowdStrike | No successful wild exploitation observed in its scope; lab RCE and adaptation barriers discussed. | Global absence of exploitation, then or later. |
| 26 October, CISA | Both PHP CVEs added to the Known Exploited Vulnerabilities catalog. | Internet-wide prevalence, mass compromise or attacker use of AI. |
| 27 October, Wiz | No completed chains in its own telemetry, while acknowledging external honeypot RCE evidence. | A contradiction of CISA or proof that attempts cannot succeed elsewhere. |

[@awsphp2026; @phpoom2026; @phpstale2026; @crowdphp2026; @cisakev2026; @wizphptel2026]

The apparent conflict is largely about **dates, populations and endpoints**. Neither early warnings of imminent catastrophe nor early negative sensor observations settle the eventual harm. Known exploitation now warrants attention, but the reviewed evidence does not quantify global compromises or show that attacks used AI. Likewise, pre-disclosure attempts do not show that a particular later disclosure mistake caused them.

Wiz's follow-up also cautions against treating every exposure decline as a patch: upgrades, retirement, network restrictions and observation changes can all contribute. Security-vendor telemetry is useful precisely when its population and limits remain visible. [@wizphptel2026]

## 3. Brotli: One Flaw Across Multiple Ecosystems

**CVE-2026-111497** affects the Brotli decoder embedded in other products. Node.js's advisory credits OpenAI Codex Security researchers **Khai Tran and Sylvie Mayer**. Its documented risk requires an application to decompress attacker-controlled Brotli input. This supports an AI-associated reporting contribution, not the assertion that every item in the Node.js release was AI-discovered or that discovery required no humans. [@nodeoct2026]

Microsoft's .NET advisory makes configuration especially clear: merely installing an affected package is insufficient to establish exposure. Relevant decompression paths must be enabled or explicitly used. Default behavior and whether a decoder is bundled into a self-contained application matter. Severity labels and CVSS versions also differ between advisory contexts; they are not universal exploit probabilities. [@dotnetbrotli2026]

PHP's 26 October Windows rebuilds update Brotli without changing the PHP source-runtime version. This is a practical supply-chain distinction: a version string can conceal a relevant dependency rebuild. The same archive separately records a 23 October session-related issue, **CVE-2026-115560**, under unusual conditions. It must not be silently merged into the original two PHP2Shell CVEs or treated as proof that their fixes failed across the board. [@phpupdates2026]

Names such as Brotli2Shell, Node2Shell, HTTP2Shell and Broccoli2Shell circulate for the shared Brotli problem. Prefer the CVE for joining evidence. CISA's observed catalog adds this CVE on **27 October**; older claims that it is not listed, including Tenable's 26 October FAQ, are no longer current. Catalog inclusion does not quantify how broadly or reliably it has been exploited. [@narangbrotli2026; @cisakev2026]

### Python: Optional Dependencies and Reachable Decoding

Aikido's Python discussion adds a useful dependency-path example: applications can reach a native decoder through HTTP libraries without a direct Brotli import. Check the resolved package graph and actual processing of untrusted input. Installation is a reason to investigate, not by itself proof of a reachable attack path. The article's cited Python tests concern decoder behavior, not a complete Python RCE chain. [@aikidopython2026]

The reviewed GitHub advisory lists fixes in `brotli` **1.2.1** and `brotlicffi` **1.2.1.0**. Both [PyPA/OSV records](https://osv.dev/vulnerability/PYSEC-2026-4322) link to the shared CVE, but lower affected bounds differ from GitHub's ranges; the [brotlicffi record](https://osv.dev/vulnerability/PYSEC-2026-4323) also needs package-specific interpretation. Preserve this metadata discrepancy rather than invent agreement or treat a missing API CVE field as absence of a known problem. [@pythonbrotliadvisory2026]

This is another downstream manifestation of the same vulnerability, not a new AI discovery. Download volume is not an exposed-installation count, and advisory publication does not guarantee that every scanner or deployment has consumed it. The practical research question is how quickly evidence moves from a shared-library flaw to package metadata and then to verified remediation. Aikido's product and image promotions are not independent efficacy evidence.

## 4. A Positive Comparator: Maintainer-Validated Firefox Findings

Mozilla's March account confirms **22 CVEs, including 14 high-severity bugs**, following collaboration with Anthropic. The maintainer emphasizes reproducible reports and joint work to validate and fix them. Its April account reports **271 vulnerability fixes** from an initial Mythos Preview evaluation. These are separate batches, not interchangeable totals. [@mozhardening2026; @mozzero2026]

This is stronger evidence of useful defensive contribution than a model vendor's unconfirmed discovery claim. It is not a randomized assessment of total engineering savings or attacks prevented. Mozilla's further optimism that cheaper discovery can favor defenders is an important perspective, not a demonstrated forecast that all vulnerabilities will be eliminated. Its warning about preserving human-comprehensible code also belongs in the discussion. [@mozzero2026]

The positive lesson is about actionable reports and maintainer integration, not indiscriminate report volume. A project can benefit from AI-assisted research while objecting to low-quality automated submissions. Those positions need not be inconsistent.

## 5. Capability Research: The Patch Gap

Anthropic's June evaluation examines **18 Firefox-engine patches** and **21 Windows-kernel patches**. It reports eight Mythos exploit successes in each set, with distinct code-execution and local privilege-escalation endpoints. This is an N-day study: participants receive evidence about already fixed vulnerabilities, not a blank search for unknown bugs. [@anthropicndays2026]

Interpret the result within the supplied artifacts, selected tasks, retries and token budgets. Firefox uses a standalone engine, not a full remote browser-compromise campaign; Windows begins with local access. Reported fastest-trial times and API charges exclude important operational work. The experiments were not independently replicated for this review. They support concern about faster exploit preparation, not an observed attacker success rate or a universal cost to compromise systems. [@anthropicndays2026]

## 6. What This Adds to “Does AI Help?”

Our synthesis is that security is an example of AI's potential to make previously uneconomic analytical work practical, but with unusually strong externalities. A defender's gain can coexist with added work for maintainers and better tools for attackers. The relevant outcome is not bugs reported per token; it is the change in harm after validation, repairs and adoption.

The PHP team's report describes 106 closed submissions that were invalid, duplicates or non-reproducing alongside 15 CVEs since July. **That is not an AI false-positive rate**: it mixes origins and closure reasons. It does demonstrate why triage must be evaluated separately from discovery. [@phptriage2026]

OpenAI proposes a maintainer-led response framework linking validation, preparation and rollout. Treat this as a process proposal to evaluate, not independent proof of public benefit. Disclosure timing and equitable access to fixes matter alongside technical capability. The funding, labor and governance needed to complete the work are part of the intervention. [@openaiphp2026]

The connection to the Bank of America case is conceptual: discovery can reveal a backlog that requires considerable remediation. Extra work can represent valuable risk reduction, a response to increased threat, or both; spending alone identifies neither success nor failure. [@sonpatching2026]

For future studies, measure:

- Accepted, reproducible, distinct vulnerabilities, not raw reports or crash counts.
- Human triage, verification and repair time, including invalid and duplicate submissions.
- Exposure conditions and severity, not product installation or popularity alone.
- Time to fix, distribution and actual deployment, including rebuilt dependencies and running processes.
- Successful exploitation and resulting harm, with sensor coverage and observation windows explicit.
- Maintainer burden, funding and access to defensive tools, not just discoverer productivity.
- Counterfactual outcomes: what comparable teams would have found, patched or suffered without the intervention.

## Selected Reading and Admission Decisions

| Priority | Sources to read | Why retained |
| --- | --- | --- |
| Essential | [PHP OOM advisory](https://github.com/php/php-src/security/advisories/GHSA-w8hw-w9fx-j79w), [stale-state advisory](https://github.com/php/php-src/security/advisories/GHSA-6wmf-4rv5-p3rp), [dated PHP notices](https://www.php.net/archive/2026.php) | Stable IDs, affected conditions and distinct update paths. |
| Essential | [PHP Foundation retrospective](https://thephp.foundation/blog/2026/10/21/todays-php-security-release-and-how-were-strengthening-php-security/), [triage account](https://thephp.foundation/blog/2026/10/14/how-the-php-security-team-handles-your-reports/) | History, institutional bottlenecks and reporting burden. |
| Essential | [Node.js](https://nodejs.org/en/blog/vulnerability/october-2026-security-releases), [.NET](https://github.com/dotnet/runtime/security/advisories/GHSA-p3jp-9v83-76w9) | Maintainer attribution and dependency/configuration scope. |
| Essential | [CISA official JSON](https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json), [W3Techs](https://w3techs.com/technologies/details/pl-php), [Censys](https://php2shell.censys.com/) | Status, denominators and exposure units; dated snapshots required. |
| Technical context | [Calif](https://calif.io/php2shell/), [Wiz discovery](https://www.wiz.io/blog/php2shell-php-rce) | Human-model workflows and demonstrated paths; not independent effectiveness estimates. |
| Dependency map | [Tenable's Brotli FAQ](https://www.tenable.com/blog/brotli2shell-frequently-asked-questions-for-google-brotli-decoder-cve-2026-111497) | Cross-product and alias map; update its dated exploitation status against CISA. |
| Python follow-up | [Aikido analysis](https://www.aikido.dev/blog/python-packages-vulnerable-node2shell-brotli-cve-2026-111497), [reviewed package advisory](https://github.com/advisories/GHSA-9v8h-qqgm-4m35) | Optional dependencies and package metadata; distinguish installation, reachability and demonstrated impact. |
| Essential balance | [AWS](https://aws.amazon.com/blogs/security/amazon-threat-intelligence-identifies-php2shell-exploitation-prior-to-public-disclosure-in-madpot/), [CrowdStrike](https://www.crowdstrike.com/en-us/blog/obstacles-to-weaponizing-php2shell-likely-constrain-exploitation/), [Wiz follow-up](https://www.wiz.io/blog/php2shell-exploitation-so-far) | Distinguish attempts, success, dates and sensor populations. |
| Positive comparator | [Mozilla March](https://blog.mozilla.org/en/firefox/hardening-firefox-anthropic-red-team/), [Mozilla April](https://blog.mozilla.org/en/firefox/ai-security-zero-day-vulnerabilities/) | Maintainer-confirmed benefits; forecasts kept separate. |
| Research and governance | [Anthropic N-days](https://www.anthropic.com/research/n-days), [OpenAI coordination proposal](https://openai.com/index/coordinated-disclosure-of-critical-vulnerabilities/) | Controlled capability evidence and a process proposal, with different evidentiary roles. |

## Scope, Exclusions and Release Preparation

This security review and its Python follow-up add **22 source records**, bringing November's staged total to **46**. Multiple reports in the PHP family and downstream Brotli advisories are linked, not counted as independent discoveries or studies. No DOI is invented for advisories or blogs; CVE/GHSA IDs supply stable identity where applicable.

Media coverage was used to locate primary sources, not to multiply evidence. Unrelated compromises, certificate incidents and supply-chain attacks are not labeled AI-discovered without established provenance. Claims about a universal working exploit, total sites compromised, offensive AI use and causal net public benefit are not established by the reviewed material. No attack code was executed, no vulnerable target probed and no patches applied to the user's machine.

The [observation ledger](../november/security-observations.json) preserves search scope and dated measurements. The [browser ledger](../november/browser-observations.json) records Chrome checks where ordinary retrieval was incomplete. These are October intake observations, not November release receipts. Recheck advisories, corrections, catalog entries and dashboards before November publication and monthly thereafter. Link to current maintainer advice rather than turn this review's historical version milestones into permanent operational instructions.
