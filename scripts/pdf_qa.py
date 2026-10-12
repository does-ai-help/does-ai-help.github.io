#!/usr/bin/env python3
"""Inspect PDF content and create a contact sheet from rendered page images."""
import json
from pathlib import Path
from PIL import Image, ImageDraw
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]


def main():
    reader=PdfReader(ROOT / "site/downloads/ai-intellectual-work-2026-10.pdf")
    counts=[]
    for i,page in enumerate(reader.pages):
        text=page.extract_text() or ""
        counts.append(len(text.strip()))
        if not text.strip():
            raise SystemExit(f"Blank page: {i+1}")
    images=sorted((ROOT / "build").glob("pdf-page-*.png"))
    if len(images)!=len(reader.pages):
        raise SystemExit("Render every PDF page before running visual QA")
    width,height=235,350
    sheet=Image.new("RGB",(width*4,height*((len(images)+3)//4)),"#e4e8e5")
    draw=ImageDraw.Draw(sheet)
    for i,p in enumerate(images):
        page=Image.open(p).convert("RGB");page.thumbnail((width-14,height-28))
        x=(i%4)*width+7;y=(i//4)*height+20
        sheet.paste(page,(x,y));draw.text((x,y-16),f"Page {i+1}",fill="#232527")
    output=ROOT / "build/qa";output.mkdir(parents=True,exist_ok=True)
    sheet.save(output / "pdf-contact-sheet.png")
    (output / "pdf-report.json").write_text(json.dumps({"pages":len(reader.pages),"text_characters_per_page":counts,"pdf_metadata":dict(reader.metadata)},ensure_ascii=False,indent=2))
    print(f"PDF: {len(reader.pages)} nonblank pages, text extracted and contact sheet prepared.")


if __name__ == "__main__":
    main()
