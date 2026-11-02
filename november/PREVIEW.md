# Public November Preview

The [preview](https://does-ai-help.github.io/preview/november/) is public, mutable and explicitly provisional. It does not replace the October edition at the root URL. No final November tag or immutable release is created.

The preview's `reference_previews` setting enables desktop citation context from existing evidence records. It uses local, escaped templates with no remote lookup; touch links keep their normal reference navigation. Asset sources are in `scripts/web/`, and the October artifacts are not rebuilt.

## Editing and Building

1. Edit source intakes and appraisals using their established files. Existing-source corrections belong in `november/source-updates.json`, not duplicate entries.
2. Edit `november/article-additions.json` for integrated additions; it specifies stable section anchors in October's manuscript. The builder produces the complete `manuscript/article-november.md`.
   Edit `november/UPDATE-SUMMARY.md` for the reader-facing changes summary. The builder renders it at `updates.html` with shared navigation and retains the Markdown download; do not edit generated HTML directly.
3. Update `november/preview.json` and this edition's summary when advancing the preview. The cutoff is provisional, not a future verification claim.
4. Install dependencies, then run `python3 scripts/prepare_november.py`. A temporary build assembles baseline records and the current staged additions, applies existing-paper corrections, and generates `preview/november/`, exports and PDF. October inputs and outputs are not rewritten.
5. Run unit tests, `python3 scripts/check_november_preview.py`, and `node scripts/november_browser_qa.mjs`. Inspect browser screenshots and all PDF pages. Commit the source changes and generated preview together.

For a local test, serve the repository root and open `/preview/november/`. The static pages also work offline, apart from absolute navigation and external services. The live preview is marked `noindex` to reduce confusion with the published edition; it is not access-restricted.

## Deployment Safety

`.github/workflows/november-preview.yml` runs only on the preparation branch. It checks the committed preview, checks out `main` separately, verifies its October version, copies its `site/` unchanged, and adds the preview subdirectory. A byte comparison rejects accidental changes outside that subdirectory. Both deployment workflows share the `pages` concurrency group.

The GitHub Pages environment allows `main` and this preparation branch. Other branches remain excluded. The production workflow additionally rejects non-main manual runs. Preview deployment is public and does not require merging into `main`.

GitHub Pages has one deployment tree per organization site. A later main deployment removes the preview until the preparation workflow runs again. After closing November, retire or revise the preview workflow and branch permission deliberately; do not remove historical release archives.

## Limits

Offline integrity checks are not live citation verification. This preview retains dated inspections, partial reading scopes and outstanding follow-ups. Before formal November release, refresh the selected browser receipts, rerun reference/access audits, inspect revisions, complete editorial review and set the final manifest together. Draft citation formats identify the preview version, not an invented release tag.
