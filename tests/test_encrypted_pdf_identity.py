import io
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from verify_references import page_metadata

try:
    from pypdf import PdfWriter
except ImportError:
    PdfWriter = None


@unittest.skipUnless(PdfWriter, 'Install the verification requirements to test PDF parsing')
class EncryptedPdfIdentityTests(unittest.TestCase):
    def test_public_aes_pdf_metadata_can_be_inspected(self):
        writer = PdfWriter()
        writer.add_blank_page(width=300, height=200)
        writer.add_metadata({'/Title': 'Public AES report'})
        writer.encrypt(user_password='', owner_password='test-owner', algorithm='AES-256')
        buffer = io.BytesIO()
        writer.write(buffer)
        observed = page_metadata(buffer.getvalue())
        self.assertNotIn('parse_error', observed)
        self.assertEqual(observed['titles'], ['Public AES report'])
