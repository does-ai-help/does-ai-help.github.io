#!/usr/bin/env python3
"""Render an original conceptual figure, not a quantitative research plot."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]


def font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default(size=size)


def main():
    image = Image.new("RGB", (1800, 680), "white")
    draw = ImageDraw.Draw(image)
    ink, green, red, grey = "#232527", "#166f59", "#b43539", "#5b6364"
    draw.text((42, 35), "WHERE DOES THE BENEFIT SURVIVE?", font=font(28, True), fill=green)
    stages = [
        ("Generation", ["Candidates, artifacts,", "calculations, hypotheses"]),
        ("Verification", ["Tests, proofs, expert", "review, experiments"]),
        ("Integration", ["Accepted changes and", "a functioning workflow"]),
        ("Use", ["Adoption, interpretation,", "decisions, deployment"]),
        ("Value", ["Outcomes relative", "to total effort and cost"]),
    ]
    for i, (title, lines) in enumerate(stages):
        x = 42 + i * 350
        draw.line((x, 148, x+305, 148), fill=green if i in [0,4] else grey, width=5)
        draw.text((x, 179), f"0{i+1}", fill=red, font=font(24, True))
        draw.text((x, 220), title, fill=ink, font=font(39, True))
        for j, line in enumerate(lines):
            size=29
            while draw.textlength(line,font=font(size))>305:
                size-=1
            draw.text((x, 281+j*39), line, fill=grey, font=font(size))
        if i < 4:
            y=230
            draw.line((x+307,y,x+334,y),fill=grey,width=3)
            draw.polygon([(x+334,y),(x+325,y-7),(x+325,y+7)],fill=grey)
    draw.line((42, 418, 1750, 418), fill="#dce2df", width=2)
    draw.text((42, 455), "Learning and judgment support every stage", fill=ink, font=font(30, True))
    draw.text((42, 508), "Real-world outcomes inform the next question, specification, or experiment.", fill=grey, font=font(25))
    draw.text((42, 597), "Conceptual synthesis by the authors. Equal widths do not represent durations or effect sizes.", fill=grey, font=font(20))
    output=ROOT / "site/assets/evidence-pathway.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, optimize=True)
    print(output)


if __name__ == "__main__":
    main()
