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
2. **Additional maintainer:** invite a trusted editor through organization/repository access settings. With only one human maintainer, requiring another person's approval would prevent that maintainer from merging their own work. Once another editor joins, require an approving review and consider enforcing protections for administrators too.
3. **Deployment approval (optional):** in **Settings > Environments > github-pages**, add required reviewers if every publication should need explicit approval. Decide whether the person initiating deployment may approve it. These choices depend on the editorial team.
4. **Organization security:** enable two-factor authentication, review recovery arrangements, and add a second owner when appropriate. These are account-level decisions, not prerequisites for the public website.
5. **Monthly review:** inspect scheduled Actions reports and community suggestions; prepare a new release after appraisal. Expiring identity exceptions must be refreshed or removed, not extended automatically.
6. **Custom domain (optional):** no purchase or DNS change is required. If a domain is chosen later, verify ownership in GitHub first. Update the release manifest, links and outputs together.

If deployment fails, read the failed step in **Actions > Publish static review**. Resolve citation mismatches or confirmed broken links rather than disabling verification gates. Restrictions need documented, time-limited evidence. Published snapshots remain immutable; corrections require a new version.

Official guidance: [GitHub Pages site types](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages), [custom domains](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages), and [deployment environments](https://docs.github.com/en/actions/deployment/targeting-different-environments/managing-environments-for-deployment).
