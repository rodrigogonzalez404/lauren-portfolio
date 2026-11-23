"""Extract the three Kirkland 405 logo concepts as clean vector SVGs from the naming deck (pdftocairo -svg).
Keeps only the logo-grey (#777C80) paths; drops photos, background panels and clip/filters. Output: logo-<name>.svg
(viewBox cropped tight to the artwork, fill=currentColor so the site can recolour them)."""
import re, subprocess, io, xml.etree.ElementTree as ET
import numpy as np, cairosvg
from PIL import Image
PDF = '/workspace/lauren-case-studies/source/extracted/Kirkland Brand Design/Kirkland405_Logo-NameIdeas_draft1.pdf'
NS = {'svg': 'http://www.w3.org/2000/svg'}; ET.register_namespace('', NS['svg']); ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
GREY = '46.665955%'
def extract(page, name):
    svg = subprocess.run(['pdftocairo', '-svg', '-f', str(page), '-l', str(page), PDF, '-'], capture_output=True, check=True).stdout
    root = ET.fromstring(svg)
    def clean(el):
        for ch in list(el):
            tag = ch.tag.split('}')[1]
            if tag in ('defs', 'image', 'use', 'filter', 'clipPath', 'mask'): el.remove(ch); continue
            if tag == 'path':
                st = (ch.get('fill') or '') + (ch.get('stroke') or '')
                if GREY not in st: el.remove(ch); continue
                for a in ('fill', 'stroke'):
                    if ch.get(a) and GREY in ch.get(a): ch.set(a, 'currentColor')
                continue
            for a in ('clip-path', 'mask', 'filter'): ch.attrib.pop(a, None)
            clean(ch)
    clean(root)
    s = ET.tostring(root, encoding='unicode')
    # bbox by rasterising at 8x
    png = cairosvg.svg2png(bytestring=s.replace('currentColor', '#000').encode(), output_width=1008 * 8, output_height=612 * 8)
    a = np.array(Image.open(io.BytesIO(png)).convert('RGBA'))[..., 3]
    ys, xs = np.nonzero(a > 8); x0, x1, y0, y1 = xs.min() / 8, (xs.max() + 1) / 8, ys.min() / 8, (ys.max() + 1) / 8
    root.set('viewBox', f'{x0:.2f} {y0:.2f} {x1 - x0:.2f} {y1 - y0:.2f}'); root.set('width', f'{x1 - x0:.2f}'); root.set('height', f'{y1 - y0:.2f}')
    out = ET.tostring(root, encoding='unicode')
    out = re.sub(r'\s+', ' ', out)
    open(f'logo-{name}.svg', 'w').write(out); print(name, round(x1 - x0, 1), round(y1 - y0, 1), len(out))
for p, n in [(3, 'the-grid'), (5, 'stage-one'), (7, 'the-pulse')]: extract(p, n)
