import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


class FaviconTests(unittest.TestCase):
    def test_compatibility_sizes_and_visible_pixels(self):
        for name, size in [('assets/favicon-32.png', 32), ('apple-touch-icon.png', 180)]:
            with Image.open(ROOT / 'site' / name) as image:
                self.assertEqual(image.size, (size, size))
        with Image.open(ROOT / 'site/favicon.ico') as icon:
            self.assertEqual(icon.ico.sizes(), {(16, 16), (32, 32)})
            image = icon.ico.getimage((16, 16)).convert('RGBA')
            pixels = [image.getpixel((x, y)) for y in range(16) for x in range(16)]
            self.assertTrue(any(min(pixel[:3]) > 200 and pixel[3] > 200 for pixel in pixels))
            self.assertTrue(any(pixel[1] > pixel[0] * 2 and pixel[3] > 200 for pixel in pixels))

    def test_vector_icon_is_font_independent(self):
        root = ET.parse(ROOT / 'site/favicon.svg').getroot()
        self.assertEqual(root.attrib['viewBox'], '0 0 32 32')
        namespace = {'svg': 'http://www.w3.org/2000/svg'}
        self.assertEqual(len(root.findall('.//svg:path', namespace)), 3)
        self.assertEqual(len(root.findall('.//svg:text', namespace)), 0)

    def test_every_page_includes_browser_and_touch_icons(self):
        for page in (ROOT / 'site').glob('*.html'):
            html = page.read_text()
            self.assertIn('href="favicon.svg"', html, page.name)
            self.assertIn('href="favicon.ico"', html, page.name)
            self.assertIn('href="apple-touch-icon.png"', html, page.name)
