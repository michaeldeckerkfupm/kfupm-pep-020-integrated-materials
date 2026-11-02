"""Render original packet pages and passage-only images, as on ENGL010.

Usage: python render_source_images.py "/path/to/ENGL021021 Integrated Materials V8.pdf"
The PDF is the matching original export supplied beside the Word packet.
Requires PyMuPDF and Pillow. Source documents and teacher keys are not published.
"""
from pathlib import Path
import argparse
from io import BytesIO
import json
import re
import fitz
from PIL import Image

SCALE = 2.4
REFERENCE_WIDTH = 804


def render(page, target, clip=None):
    pix = page.get_pixmap(matrix=fitz.Matrix(SCALE, SCALE), clip=clip, alpha=False)
    target.parent.mkdir(parents=True, exist_ok=True)
    image = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    output = BytesIO()
    image.save(output, 'WEBP', quality=90, method=6)
    payload = output.getvalue()
    if not payload:
        image.save(output, 'WEBP', lossless=True)
        payload = output.getvalue()
    assert payload, f'Empty render: {target}'
    Image.open(BytesIO(payload)).load()
    temporary = target.with_suffix('.tmp')
    temporary.write_bytes(payload)
    temporary.replace(target)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('packet_pdf', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    html_path = root / 'index.html'
    html = html_path.read_text()
    match = re.search(r'(<script[^>]*id="packet-data"[^>]*>)(.*?)(</script>)', html, re.S)
    data = json.loads(match[2])
    pdf = fitz.open(args.packet_pdf)
    assert len(pdf) == 264, 'Expected the 264-page V8 packet'
    for number, path in data['images'].items():
        page = pdf[int(number) - 1]
        render(page, root / path)
    count = 0
    for activity in data['activities']:
        if activity['skill'] != 'Reading':
            continue
        for index, frame in enumerate(activity['readingFrames'], 1):
            page = pdf[frame['page'] - 1]
            # Existing audited crops use the original 804px page coordinate system.
            scale = page.rect.width / REFERENCE_WIDTH
            clip = fitz.Rect(*(value * scale for value in frame['crop'])) & page.rect
            assert clip.width > 0 and clip.height > 0
            path = f"assets/readings/{activity['id']}-{index}.webp"
            render(page, root / path, clip)
            frame['src'] = path
            count += 1
    html = html[:match.start(2)] + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + html[match.end(2):]
    html_path.write_text(html)
    print(f"Rendered {len(data['images'])} original pages and {count} passage crops at {SCALE}x PDF resolution")


if __name__ == '__main__':
    main()
