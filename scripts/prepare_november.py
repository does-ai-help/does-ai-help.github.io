#!/usr/bin/env python3
"""Assemble an explicitly provisional November preview without editing October."""
import argparse
import copy
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text())


def assemble():
    config = load('november/preview.json')
    records = copy.deepcopy(load('data/sources.json'))
    by_id = {r['id']: r for r in records}
    for update in load('november/source-updates.json')['records']:
        if update['id'] not in by_id:
            raise ValueError('Update does not identify an October source')
        by_id[update['id']].update(update['fields'])
    for source in load('data/november-sources.json'):
        if source['id'] in by_id:
            raise ValueError('Duplicate staged source: ' + source['id'])
        source = copy.deepcopy(source)
        source['intake_editorial_priority'] = source['editorial_priority']
        source['editorial_priority'] = 'core' if source['editorial_priority'].startswith('core') else 'supporting'
        source['staging_status'] = 'included-in-draft-preview'
        records.append(source)
        by_id[source['id']] = source
    for source in records:
        if source['publication_status'] == 'peer-reviewed-conference-paper':
            source['publication_status'] = 'peer-reviewed-conference'
    urls = [r['url'].rstrip('/') for r in records]
    dois = [r['doi'].lower().removeprefix('https://doi.org/') for r in records if r.get('doi')]
    if len(urls) != len(set(urls)) or len(dois) != len(set(dois)):
        raise ValueError('Duplicate canonical URL or DOI in assembled database')
    article = (ROOT / 'manuscript/article.md').read_text()
    old = 'The October 2026 release covers sources available by 13 October 2026;'
    if article.count(old) != 1:
        raise ValueError('October abstract anchor changed')
    cutoff = date.fromisoformat(config['cutoff'])
    cutoff_label = f'{cutoff.day} {cutoff:%B %Y}'
    article = article.replace(old, f'This November 2026 draft preview has a provisional evidence cutoff of {cutoff_label};')
    for addition in load('november/article-additions.json'):
        anchor = addition['before']
        if article.count(anchor) != 1:
            raise ValueError('Manuscript anchor changed: ' + anchor)
        text = addition['text'].replace('{{new_source_count}}', str(len(load('data/november-sources.json'))))
        text = text.replace('{{cutoff_date}}', cutoff_label)
        article = article.replace(anchor, text + '\n\n' + anchor)
    for match in re.findall(r'\[@([^\]]+)\]', article):
        for key in match.split(';'):
            source = by_id.get(key.strip().lstrip('@'))
            if not source or source['verification']['level'] != 'content-checked':
                raise ValueError('Unappraised manuscript citation: ' + key)
            if (source.get('date') or '') > config['cutoff']:
                raise ValueError('Manuscript citation exceeds preview cutoff: ' + key)
    meta = load('data/release.json')
    meta.update({k: v for k, v in config.items() if k not in ['notice', 'preview_path', 'baseline_commit']})
    meta.update(snapshot=config['version'], archive_name=f"does-ai-help-release-{config['version']}.zip",
                article_status='Public draft preview; not peer reviewed; final November checks pending')
    return article, records, meta


def run(args, work):
    env = dict(os.environ)
    env['PATH'] = '/Library/TeX/texbin:' + env.get('PATH', '')
    subprocess.run(args, cwd=work, env=env, check=True)


def existing_pdf_for_web_update(article, records, meta):
    """Reuse a PDF only when its manuscript, evidence and release inputs match."""
    download = ROOT / 'preview/november/downloads'
    previous_meta = json.loads((download / 'release.json').read_text())
    if any(previous_meta.get(key) != value for key, value in meta.items()):
        raise ValueError('PDF reuse requires unchanged release metadata')
    if json.loads((download / 'sources.json').read_text()) != records:
        raise ValueError('PDF reuse requires unchanged evidence records')
    canonical_text = lambda text: '\n'.join(line.rstrip() for line in text.splitlines()).rstrip()
    if canonical_text((download / 'article.md').read_text()) != canonical_text(article):
        raise ValueError('PDF reuse requires an unchanged manuscript')
    pdf = (download / f"does-ai-help-{meta['version']}.pdf").read_bytes()
    if not pdf.startswith(b'%PDF-'):
        raise ValueError('Existing preview PDF is invalid')
    checksums = dict(line.split('  ', 1)[::-1] for line in (download / 'checksums.sha256').read_text().splitlines())
    if hashlib.sha256(pdf).hexdigest() != checksums.get(f"does-ai-help-{meta['version']}.pdf"):
        raise ValueError('Existing preview PDF checksum mismatch')
    return pdf


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--assemble-only', action='store_true')
    pdf_mode = parser.add_mutually_exclusive_group()
    pdf_mode.add_argument('--skip-pdf', action='store_true', help='For quick development only; not for publishing.')
    pdf_mode.add_argument('--reuse-pdf', action='store_true', help='Web-only update: preserve a checked PDF with unchanged publication inputs.')
    args = parser.parse_args()
    config = load('november/preview.json')
    article, records, meta = assemble()
    existing_pdf = existing_pdf_for_web_update(article, records, meta) if args.reuse_pdf else None
    (ROOT / 'manuscript/article-november.md').write_text(article)
    if args.assemble_only:
        print(f'Assembled November manuscript and {len(records)} evidence records')
        return
    work = ROOT / 'build/november-work'
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    for name in ['data', 'scripts', 'manuscript', 'latex']:
        shutil.copytree(ROOT / name, work / name, ignore=shutil.ignore_patterns('__pycache__'))
    for file in ROOT.glob('*.md'):
        shutil.copyfile(file, work / file.name)
    shutil.copyfile(ROOT / 'CITATION.cff', work / 'CITATION.cff')
    (work / 'node_modules').symlink_to(ROOT / 'node_modules', target_is_directory=True)
    (work / 'site/downloads').mkdir(parents=True)
    shutil.copytree(ROOT / 'site/assets', work / 'site/assets')
    for name in ['favicon.svg', 'favicon.ico', 'apple-touch-icon.png']:
        shutil.copyfile(ROOT / 'site' / name, work / 'site' / name)
    (work / 'data/sources.json').write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n')
    (work / 'data/release.json').write_text(json.dumps(meta, ensure_ascii=False, indent=2) + '\n')
    (work / 'manuscript/article.md').write_text(article)
    summary = ROOT / 'november/UPDATE-SUMMARY.md'
    summary_html_source = summary.read_text().replace('../manuscript/', 'downloads/appraisals/')
    summary_html_source = re.sub(r'\]\((search-[^()]+\.json)\)', r'](downloads/\1)', summary_html_source)
    (work / 'manuscript/update-summary.md').write_text(summary_html_source)
    notes = ROOT / 'november/RELEASE-NOTES.md'
    (work / 'manuscript/release-notes.md').write_text(notes.read_text())
    (work / 'CHANGELOG.md').write_text('# November Draft Preview\n\nVersion ' + meta['version'] +
                                      '. Provisional cutoff: ' + meta['cutoff'] +
                                      '. Final editorial and release verification checks pending.\n\n' +
                                      (ROOT / 'november/UPDATE-SUMMARY.md').read_text() +
                                      '\n\n## Earlier Published History\n\n' + (ROOT / 'CHANGELOG.md').read_text())
    citation = (work / 'CITATION.cff').read_text()
    citation = citation.replace(load('data/release.json')['version'], meta['version'])
    citation = citation.replace('2026-10-13', meta['release_date'])
    citation = citation.replace('October 2026', 'November 2026 draft preview').replace('month: 10', 'month: 11')
    citation = citation.replace('https://does-ai-help.github.io/', meta['canonical_url'])
    (work / 'CITATION.cff').write_text(citation)
    run([sys.executable, 'scripts/export.py'], work)
    run(['node', 'scripts/build.mjs'], work)
    if not args.skip_pdf and existing_pdf is None:
        run([sys.executable, 'scripts/build_pdf.py'], work)
    from download_names import download_names
    names = download_names(meta)
    if existing_pdf is not None:
        for filename in [f"does-ai-help-{meta['release']}.pdf", names[f"does-ai-help-{meta['release']}.pdf"]]:
            (work / 'site/downloads' / filename).write_bytes(existing_pdf)
    # Replace release-only claims in the isolated preview, not in October's builder.
    banner = ('<aside class="draft-notice" aria-label="Draft status"><strong>November draft preview</strong><br>'
              + escape(config['notice']) + ' <a href="/">Read the published October edition</a>.</aside>')
    for page in (work / 'site').glob('*.html'):
        text = page.read_text().replace('href="/"', f'href="{config["preview_path"]}"')
        text = text.replace('<head>', '<head><meta name="robots" content="noindex,follow">')
        text = text.replace('</header>', '</header>' + banner, 1)
        text = re.sub(r'<p><a href="[^"]+/releases/tag/[^"]+">Permanent versioned release</a></p>',
                      '<p>Draft preview, not a tagged release. <a href="https://github.com/does-ai-help/does-ai-help.github.io/tree/codex/november-2026-preparation">View the preparation branch</a>.</p>', text)
        text = text.replace('Initial October 2026 publication: a critical synthesis and searchable evidence map covering productivity, learning, engineering, scientific discovery and community perspectives. Technical version history is preserved in the release changelog; monthly literature updates begin with the next release.',
                            'Public November working draft. The main site and final October artifacts remain unchanged. Final November editorial and verification checks are pending.')
        text = text.replace('Latest identity audit', 'Preview verification status')
        page.write_text(text)
    with (work / 'site/assets/style.css').open('a') as stream:
        stream.write('\n.draft-notice{max-width:1200px;margin:16px auto;padding:14px 20px;border-left:3px solid #b43539;background:#f7f8f9;font-size:14px;line-height:1.6}.draft-notice a{text-decoration:underline}\n')
        stream.write('header nav{flex-wrap:wrap}.update-summary{padding-top:38px}.update-summary h1{font-size:36px;line-height:1.2}.update-summary h2{margin:36px 0 16px}.update-summary table{font-size:14px;line-height:1.55}.update-summary .summary-download{font-family:Arial,Helvetica,sans-serif;font-size:14px;margin-top:32px}.update-summary .community-note{font-family:Arial,Helvetica,sans-serif}\n')
        stream.write('.release-notes-link{font-family:Arial,Helvetica,sans-serif;font-size:15px}.release-notes-contents{border-bottom:1px solid #d9dfdd;padding-bottom:20px;margin-bottom:30px;font-family:Arial,Helvetica,sans-serif;font-size:15px}.release-notes-contents h2{font-size:18px;margin:0 0 12px}.release-notes-contents ul{columns:2;column-gap:30px;padding-left:20px}.release-notes-contents li{break-inside:avoid;margin-bottom:8px}@media(max-width:720px){.release-notes-contents ul{columns:1}}\n')
    (work / 'site/downloads/november-update-summary.md').write_text(summary.read_text().replace('../manuscript/', 'appraisals/'))
    (work / 'site/downloads' / f"does-ai-help-release-notes-{meta['version']}.md").write_text(notes.read_text())
    shutil.copyfile(ROOT / 'november/RELEASE-CHECKLIST.md', work / 'site/downloads' / f"does-ai-help-release-checklist-{meta['version']}.md")
    for log in (ROOT / 'november').glob('search-*.json'):
        shutil.copyfile(log, work / 'site/downloads' / log.name)
    shutil.copyfile(ROOT / 'november/browser-observations.json', work / 'site/downloads/november-browser-observations.json')
    appraisal_dir = work / 'site/downloads/appraisals'
    appraisal_dir.mkdir()
    for file in (ROOT / 'manuscript').glob('november-*.md'):
        shutil.copyfile(file, appraisal_dir / file.name)
    status = {'status': 'draft-not-release-audit', 'preview_version': meta['version'],
              'assembled_records': len(records), 'staged_new_records': len(load('data/november-sources.json')),
              'release_receipts_complete': False,
              'note': 'Existing source inspections retain their dates. No new release-wide live audit or monthly Chrome refresh is claimed.'}
    download = work / 'site/downloads'
    (download / names['reference-verification.json']).write_text(json.dumps(status, indent=2) + '\n')
    (download / names['reference-verification.md']).write_text('# Preview Verification Status\n\n' + status['note'] + '\n\nFinal November editorial, live reference and browser checks remain pending.\n')
    # Canonical text endings keep generated CSV/RIS and copied Markdown diffable.
    text_types = {'.md', '.ris', '.bib', '.csv', '.json', '.jsonl', '.cff', '.html', '.js', '.css', '.svg'}
    for file in (work / 'site').rglob('*'):
        if file.is_file() and file.suffix in text_types:
            file.write_text('\n'.join(line.rstrip() for line in file.read_text().splitlines()).rstrip() + '\n')
    # The archive packages this preview only, with no implied immutable release/tag.
    archive = download / meta['archive_name']
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as bundle:
        for file in sorted(download.rglob('*')):
            if file.is_file() and file != archive:
                bundle.write(file, file.relative_to(download))
    sums = ''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(download)}\n'
                   for p in sorted(download.rglob('*')) if p.is_file() and p.name not in ['checksums.sha256', names['checksums.sha256']])
    for name in ['checksums.sha256', names['checksums.sha256']]:
        (download / name).write_text(sums)
    target = ROOT / 'preview/november'
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(work / 'site', target)
    print(f'Built {config["version"]}: {len(records)} records at {target}')


if __name__ == '__main__':
    main()
