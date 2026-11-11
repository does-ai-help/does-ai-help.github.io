# Formalization, Judgment and Cross-Component Security

Second reader-suggested appraisal batch, **11 November 2026**. Nine records are added: four suggested articles and five linked primary materials. Counts and decisions are recorded in the [follow-up log](../november/search-2026-11-11-followup.json).

## Formalization Is Not a Single Guarantee

[Andrews and Zhang's CPython project](https://broyojo.com/python-formalization/) is relevant evidence of an expanding assurance workflow. Follow the authors' supplied title and attribution, but distinguish their model from the implementation it represents. The repository and tests improve inspectability without eliminating this gap. Candidate bug records are not all confirmed, novel vulnerabilities. [@andrewscpython2026]

The linked [Julia account](https://discourse.julialang.org/t/formalizing-julia-in-lean-and-finding-400-bugs-in-base/140243) supplies a particularly useful caution: a checker can accept a theorem that assumes away the intended difficulty. Its upstream issue links make findings inspectable, but are not independent validation of every reported count. [@cranmerjulia2026]

The linked [PTX preprint](https://arxiv.org/abs/2611.04447) adds another assurance level. Its trust assumptions differ from both executable-level AlphaProof Code and source-mirroring projects. The important comparison is what is modeled and excluded, not how many proof lines each system produces. [@koskaptx2026; @chaudhurialphaproofcode2026]

These projects support the possibility of previously uneconomic verification becoming feasible. They do not establish universal security, cheap verification of every result, or a net productivity effect after specification and maintenance costs.

## Human Judgment: A Hypothesis, Not a Permanent Boundary

[Shahar Glazner's essay](https://shahar.blog/2026/11/08/on-being-an-engineer-in-2026/) is useful for its emphasis on framing and long-term responsibility. Its argument about persistent human leverage depends on unmeasured premises; we should not turn tacit experience into proof that machines cannot improve in these areas. [@glaznerengineer2026]

[Ethan Mollick's demonstrations](https://www.oneusefulthing.org/p/fable-52-and-jagged-agi) make the complementary point that generation and self-evaluation can diverge. The linked research demo explicitly disclaims complete human verification. We include the demonstration as process evidence, not its generated economic findings as established research. “Jagged AGI” remains the author's framing, not the review's capability classification. [@mollickjagged2026]

## Alpine/OpenSSH: Separate the Security Fact From the AI Attribution

The [ZDNET report](https://www.zdnet.com/tech/alpine-linux-openssh-patch-flaw/) is retained as a discovery route. Its [Alpine advisory](https://alpinelinux.org/posts/2026-11-05-openssh-password-authentication-bypass/) and [version-specific OpenSSH notes](https://www.openssh.org/txt/release-10.6p2) are stronger sources for conditions and remediation. The [discoverer's account](https://sshhole.com/) supplies the explicit agent-use attribution, not an experimentally estimated discovery advantage. [@vaughanalpine2026; @alpineauth2026; @openssh106p22026; @kultekinssh2026]

The methodological lesson is cross-component coverage: assumptions that appear safe locally can fail in combination. The governance lesson is that finding defects creates release and deployment work. Project acknowledgement and released fixes strengthen the security claim; neither establishes population compromise or the causal size of AI's contribution.

## Reading and Verification Boundaries

Original public HTTP reading resolved search-reader failures for three suggested pages; no Chrome receipt is claimed. The Python repository revision is recorded, but neither its proof build nor any exploit was run. The arXiv PTX identifier is stable; a DOI marked pending registration was not promoted. The NVD page did not yield readable content, so a CVE number from secondary snippets was not treated as verified. These are selected inspections, not the final monthly audit.
