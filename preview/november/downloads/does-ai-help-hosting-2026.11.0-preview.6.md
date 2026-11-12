# Publication hosting and administration

## Repository and website

- Organization: [does-ai-help](https://github.com/does-ai-help).
- Public repository: [does-ai-help.github.io](https://github.com/does-ai-help/does-ai-help.github.io).
- Organization-site address: [https://does-ai-help.github.io/](https://does-ai-help.github.io/).
- Site files: `site/`; publishing branch: `main`; Pages source: **GitHub Actions**.

One repository holds the article, bibliography, tooling, contribution forms, releases and website. No separate publishing repository or paid domain is needed. The workflow validates committed outputs and verifies source identities before deployment; it does not generate a research release automatically. CI reports are available in Actions.

## Managed configuration

The repository has issues, source/correction forms, a pull-request template, squash merging and automatic deletion of merged contribution branches. Default Actions permissions are read-only; the publication workflow explicitly requests the Pages and identity-token permissions required for deployment. Automation cannot approve pull requests. The Pages environment is restricted to `main`.

Contribution checks validate data, citations, exports and archive consistency. The monthly workflow monitors source access and identities, producing audit artifacts. Editorial review, source inclusion and publication remain maintainer responsibilities. `data/release.json` contains the actual repository and website addresses; `CITATION.cff` supplies attribution metadata.

## Human decisions and manual steps

1. **Editorial sign-off:** read the article and review abstract-only appraisals and access exceptions. Passing CI does not certify scientific validity.
2. **Branch protection and another maintainer:** `main` is currently unprotected; deployment checks do not enforce review before merging. Invite a trusted editor, then use **Settings > Branches** (or Rulesets) to protect `main`: require pull requests, at least one approving review, the `validate` contribution check, up-to-date branches, resolved conversations, and protection against force pushes/deletion. Apply protections to administrators too. Requiring independent approval while only one human maintainer exists would prevent that person from merging their own changes; choose the team arrangement explicitly. The proposed administrator-bypass/no-approval policy was not applied.
3. **Deployment approval (optional):** in **Settings > Environments > github-pages**, add required reviewers if every publication should need explicit approval. Decide whether the person initiating deployment may approve it. These choices depend on the editorial team.
4. **Organization security:** enable two-factor authentication, review recovery arrangements, and add a second owner when appropriate. These are account-level decisions, not prerequisites for the public website.
5. **Monthly review:** inspect scheduled Actions reports and community suggestions; prepare a new release after appraisal. Expiring identity exceptions must be refreshed or removed, not extended automatically.
6. **Custom domain (optional):** no purchase or DNS change is required. If a domain is chosen later, verify ownership in GitHub first. Update the release manifest, links and outputs together.

If deployment fails, read the failed step in **Actions > Publish static review**. Resolve citation mismatches or confirmed broken links rather than disabling verification gates. Restrictions need documented, time-limited evidence. Published snapshots remain immutable; corrections require a new version.

Before deployment, the access checker defers only the publication's own URLs, since a first-time site does not exist yet. All cited-source URLs remain checked. Local links are validated against `site/`, and a post-deployment check verifies the live pages and principal downloads after CDN propagation.

Official guidance: [GitHub Pages site types](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages), [custom domains](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages), and [deployment environments](https://docs.github.com/en/actions/deployment/targeting-different-environments/managing-environments-for-deployment).
