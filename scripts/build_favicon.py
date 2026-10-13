#!/usr/bin/env python3
"""Export the font-independent favicon SVG using librsvg and Pillow."""
import shutil
import subprocess
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def main():
    renderer = shutil.which('rsvg-convert')
    if not renderer:
        raise SystemExit('Install librsvg to regenerate favicon assets (rsvg-convert).')
    site = ROOT / 'site'
    for size, destination in [(32, site / 'assets/favicon-32.png'), (180, site / 'apple-touch-icon.png')]:
        subprocess.run([renderer, '-w', str(size), '-h', str(size), '-o', str(destination), str(site / 'favicon.svg')], check=True)
    with Image.open(site / 'assets/favicon-32.png') as icon:
        icon.save(site / 'favicon.ico', sizes=[(16, 16), (32, 32)])
    print('Built SVG-backed 16/32 px ICO, 32 px PNG and 180 px touch icon.')


if __name__ == '__main__':
    main()
