#!/usr/bin/env python3
"""Offline integrity checks for the provisional site, not a fresh source audit."""
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from prepare_november import ROOT, assemble, load


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ['href', 'src']:
            if attrs.get(key):
                self.links.append(attrs[key])


def main():
    article, records, meta = assemble()
    site = ROOT / 'preview/november'
    assert (ROOT / 'manuscript/article-november.md').read_text() == article, 'Stale manuscript'
    exported = json.loads((site / 'downloads/sources.json').read_text())
    assert exported == records, 'Stale preview database'
    manifest = json.loads((site / 'downloads/release.json').read_text())
    assert manifest['version'] == meta['version']
    assert manifest['counts']['total'] == len(records)
    prefix = load('november/preview.json')['preview_path']
    for file in site.glob('*.html'):
        html = file.read_text()
        assert 'November draft preview' in html
        assert 'noindex,follow' in html
        assert 'Permanent versioned release' not in html
        parser = Links()
        parser.feed(html)
        for link in parser.links:
            url = urlsplit(link)
            if url.scheme or url.netloc or not url.path or url.path == '/':
                continue
            path = unquote(url.path)
            if path.startswith(prefix):
                target = site / path[len(prefix):]
            elif path.startswith('/'):
                raise AssertionError('Unexpected root-relative preview URL: ' + link)
            else:
                target = file.parent / path
            if target.is_dir():
                target = target / 'index.html'
            assert target.is_file(), f'Broken local link in {file.name}: {link}'
    for line in (site / 'downloads/checksums.sha256').read_text().splitlines():
        digest, name = line.split('  ', 1)
        assert hashlib.sha256((site / 'downloads' / name).read_bytes()).hexdigest() == digest, name
    pdfs = list((site / 'downloads').glob(f'does-ai-help-{meta["version"]}.pdf'))
    assert len(pdfs) == 1 and pdfs[0].read_bytes().startswith(b'%PDF-')
    print(f'Preview integrity passed: {len(records)} records, manuscript, downloads, local links and checksums.')


if __name__ == '__main__':
    main()
