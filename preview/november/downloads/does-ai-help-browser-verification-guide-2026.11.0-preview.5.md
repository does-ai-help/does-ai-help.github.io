# Local Chrome verification channel

## Why there are two channels

GitHub's headless HTTP checks can encounter bot restrictions, inaccessible metadata, dynamic rendering or PDF extraction artifacts. The alternative channel uses **Chrome on Witold Bołt's machine**, controlled through the available browser/native UI connection. It observes the publisher page a reader sees, not a second disguised headless downloader.

The browser reviewer is identified explicitly. An AI-controlled Chrome check is not labeled as a human verification. Opening a page does not prove its scientific claims, and Chrome access does not imply access to subscription full text.

## Monthly release procedure

1. Prepare the new release manifest and run the automated citation and access audits.
2. Run `python3 scripts/browser_review.py --audit build/reference-verification.json`. Open the generated `build/browser-review-queue.html` in local Chrome. The JSON task list contains stable IDs and expected citation fingerprints.
3. Revisit **every selected source for the new release month**, even if an older receipt has not yet reached 31 days. Add newly problematic sources to `data/browser-review-policy.json`; the queue also identifies checked citations unresolved by the automated audit.
4. Navigate with the local Chrome connector or native UI tools. Read the title, author attribution, date/version and DOI where visible. Inspect the relevant content only to the extent actually accessible. Observe final addresses and explain genuine publisher redirects.
5. Append a receipt to `data/browser-verification.json`. Record the exact inspected scope, access limits, reviewer, UTC timestamp, release month and citation fingerprint. Retain earlier receipts; do not renew timestamps without revisiting the source.
6. Correct bibliographic metadata or editorial annotations in the maintained input files when warranted. `data/browser-source-updates.json` holds the first two browser-resolved records. Keep stable IDs even when a candidate becomes verified. Recompute the fingerprint after a citation correction and record the corrected observed identity.
7. Run curation, exports, build, the strict browser review, strict citation verification and release validation. Archive the browser ledger with the release.

The monthly GitHub job generates a browser-review queue as an artifact. **GitHub cannot operate the local Chrome profile.** Local browser inspection is a release-time editorial step, not an unattended CI task. The release validator blocks missing, stale or wrong-month receipts for selected sources. Patch releases can reuse an unchanged current-month receipt for at most 31 days.

## Receipt contract

Each receipt contains `id`, `method` (`local-chrome-native`), `release_month`, `checked_at` (timezone-aware), `source_url`, `source_fingerprint`, `reviewer`, `outcome`, `observed`, `scope` and `notes`. A changed final address also needs `redirect_basis`.

Outcomes distinguish:

- `identity-confirmed`: the observed citation matches; an otherwise unresolved automated identity can be cleared by this current receipt.
- `access-blocked`: an inspection was attempted but did not establish identity. It satisfies the requirement to revisit, **not** the identity requirement. A separate valid identity channel remains necessary.
- `mismatch`: the citation must be corrected or removed; a browser receipt cannot override a conflicting DOI or other automated mismatch.
- `not-found`: the selected source requires repair or removal before release.

The fingerprint binds a receipt to the citation's ID, title, URL, DOI and authors. It detects accidental metadata drift; it is **not a cryptographic attestation that a person or AI genuinely visited Chrome**. The ledger is an accountable editorial record and remains open to independent review.

## Reading scope and privacy

When the coauthor supplies a PDF, match it to the actual online version before appraisal. `data/document-source-updates.json` records these follow-ups; `document_verification` preserves the basename, SHA-256, page count, inspection method and exact reading scope. A supplied file is neither proof of peer review nor permission to redistribute it. Do not put private local paths or third-party PDFs into the public repository. The four OSF/SSRN records matched during the October document follow-up are included in the mandatory monthly watchlist. If a source revision changes, refresh the artifact/version comparison and substantive appraisal, not just its timestamp. CI can validate the provenance record but cannot read the coauthor's private Downloads directory.

Record title-only, abstract, public-preview, selected-section or full-text inspection honestly. Keep identity verification separate from methodological appraisal and independent replication. Do not infer sample sizes, estimates or correctness from a headline. A certificate, DOI and working URL answer different questions.

Do not bypass paywalls, CAPTCHAs, browser security warnings or access controls. Stop for user action where required. Do not publish cookies, credentials, private browser history, institutional account details or whole accessibility snapshots. The public ledger contains only selected bibliographic facts and original review notes, not copied full texts. Screenshots, if needed for local inspection, must not expose unrelated tabs or personal information.

Legacy entries in `data/identity-exceptions.json` identify earlier indexed-primary or parser-based observations; they are **not retroactively relabeled as Chrome checks**. New Chrome receipts take precedence when valid, while existing detected conflicts still block publication.
