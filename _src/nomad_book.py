"""Nomad (Nov 24, Lauren via Rodrigo t97u): flip-book with every page except printed pp. 50-55, the printed-book mockups,
and the hero from Rodrigo's own mockup.
Run: python3 _src/nomad_book.py   (needs the 200-dpi page renders: pages/nomad-om/page-NN.png, see lauren-handoff-extras/render_pages.sh)
Source: Final OM PDFs/Nomad OM-digital.pdf, 29 PDF pages: PDF 1 = front cover (printed p. 1), PDF 2-28 = two-page spreads
(PDF n = printed pp. 2n-2 / 2n-1), PDF 29 = back cover (p. 56). Printed pp. 50-55 = PDF 26-28 (pro forma, monthly
financials, underwriting notes) are DROPPED and replaced by a black 'Confidential — financial information omitted' spread
right after the 05 The Financials divider (PDF 25, pp. 48-49, kept).
Blur: only property-specific financial figures on pages that are otherwise kept (every '$' figure word, padded):
PDF 5 the subject's average-rent vs MSA line, PDF 6 the development-cost table, PDF 23-24 the rent-comparable tables and
chart labels. Market data (neighborhood/city statistics) and the contacts are shown."""
import os, re, json, subprocess, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from images import PAGES, save, blur
import flyer_mockups as FM
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = PAGES + 'nomad-om/'
PDF = '/workspace/lauren-case-studies/source/extracted/Final OM PDFs/Nomad OM-digital.pdf'
SLUG = 'nomad'
BLUR_DOLLARS = {5: 'MOAT', 6: None, 23: None, 24: None}   # None = every word with a '$' on the page; a word = only the first '$' word after it
KEEP = list(range(2, 26))     # PDF spreads 2-25 -> printed pp. 2-49 (25 = 05 The Financials divider)
DROPPED = [26, 27, 28]        # printed pp. 50-55

def boxes(n, only=None, pad=2.5):
    xml = subprocess.run(['pdftotext', '-f', str(n), '-l', str(n), '-bbox', PDF, '-'], capture_output=True, text=True).stdout
    pw, ph = map(float, re.search(r'<page width="([\d.]+)" height="([\d.]+)"', xml).groups())
    out, seen = [], only is None
    for a, b, c, d, t in re.findall(r'xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)<', xml):
        if t == only: seen = True; continue
        if '$' in t and seen:
            if only is not None: seen = False
            a, b, c, d = map(float, (a, b, c, d))
            out.append(((a - pad) / pw, (b - pad) / ph, (c + pad) / pw, (d + pad) / ph))
    return out

def pg(n):
    im = Image.open(F + f'page-{n:02d}.png').convert('RGB')
    if n in BLUR_DOLLARS: im = blur(im, boxes(n, BLUR_DOLLARS[n]))
    return im

def halves(im): w = im.width // 2; return im.crop((0, 0, w, im.height)), im.crop((w, 0, im.width, im.height))

def flip():
    d = os.path.join(ROOT, 'assets', 'img', SLUG, 'flip')
    for f in os.listdir(d) if os.path.isdir(d) else []: os.remove(os.path.join(d, f))
    seq, k = [], 0
    def add(im, tag):
        nonlocal k
        nm = f'f{k:02d}.jpg'; save(im, SLUG + '/flip', nm, 1600); seq.append(f'{tag}:{nm}'); k += 1
    add(pg(1), 'cover')
    for n in KEEP:
        L, R = halves(pg(n)); add(L, f'p{2 * n - 2}'); add(R, f'p{2 * n - 1}')
    seq += ['BLACK', 'BLACK']
    add(pg(29), 'back')
    json.dump(seq, open(os.path.join(ROOT, '_src', 'nomad_flip.json'), 'w'), indent=1)
    print('nomad flip', len(seq), 'pages')

# ---------- printed-book mockups (self-made, top-down, on the textured stone) ----------
def _edges(im, t, sides):
    """add page-stack thickness: fine stacked page edges below and on the given outer sides"""
    W, H = im.size; out = Image.new('RGB', (W + t * ('l' in sides) + t * ('r' in sides), H + t), (0, 0, 0))
    ox = t if 'l' in sides else 0
    a = np.zeros((out.height, out.width, 3), np.float32) + 240
    yy = np.arange(out.height)[:, None]; xx = np.arange(out.width)[None, :]
    lines = 1 - 0.06 * (np.sin(yy * 2.1) > 0.3) - 0.04 * (np.sin(xx * 1.7) > 0.5)
    a *= lines[..., None]
    o = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    m = Image.new('L', out.size, 0); dr = ImageDraw.Draw(m)
    dr.rectangle((ox, t, ox + W, H + t - 1), fill=255)                         # bottom edge band
    if 'l' in sides: dr.rectangle((0, t // 2, ox, H + t - 1), fill=255)
    if 'r' in sides: dr.rectangle((ox + W, t // 2, out.width - 1, H + t - 1), fill=255)
    out.paste(o, (0, 0), m)
    out.paste(im, (ox, 0))
    alpha = Image.new('L', out.size, 0); ImageDraw.Draw(alpha).rectangle((ox, 0, ox + W - 1, H - 1), fill=255)
    alpha.paste(m, (0, 0), m)
    out = out.convert('RGBA'); out.putalpha(alpha)
    return out

def open_spread(n, w):
    """an open, bound spread seen from above: gutter shadow + curl light, page thickness on three sides"""
    im = pg(n); W, H = im.size
    x = (np.arange(W) - W / 2) / W
    d = np.abs(x)
    shade = 1 - 0.38 * np.exp(-d / 0.010) - 0.12 * np.exp(-d / 0.05) + 0.035 * np.exp(-((d - 0.09) / 0.05) ** 2) - 0.05 * (d / 0.5) ** 3
    a = np.asarray(im, np.float32) * shade[None, :, None]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    im = im.resize((int(w), int(w * H / W)), Image.LANCZOS)
    return _edges(im, max(4, int(w * 0.006)), 'lr')

def closed_book(n, w):
    im = pg(n); W, H = im.size
    im = im.resize((int(w), int(w * H / W)), Image.LANCZOS)
    x = np.linspace(0, 1, im.width)
    a = np.asarray(im, np.float32) * (1 - 0.10 * np.exp(-x / 0.012))[None, :, None]   # spine crease on the left
    return _edges(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)), max(5, int(w * 0.012)), 'r')

def lay(cv, obj, cx, cy, ang):
    o = obj.rotate(ang, Image.BICUBIC, expand=True)
    FM.put_device(cv, o, cx, cy, shadow=0.9)

def stone(w, h, seed):
    W0, H0 = FM.W, FM.H; FM.W, FM.H = w, h
    try: return FM.surface(seed=seed, light=(0.4, 0.2))
    finally: FM.W, FM.H = W0, H0

def mockups():
    out = lambda cv, nm: (cv.save(os.path.join(ROOT, 'assets', 'img', SLUG, nm), 'JPEG', quality=84, optimize=True, progressive=True), print(nm))
    # A: the 03 Market Overview divider spread beside the closed cover (like the reference, top row)
    cv = stone(2400, 1350, 31)
    lay(cv, open_spread(15, 1360), 760, 690, 1.5)
    lay(cv, closed_book(1, 640), 1880, 665, -2.5)
    out(cv, 'book_a.jpg')
    # B: the back cover (contacts) beside the Overlook Neighborhood / Statistics spread (reference, bottom row)
    cv = stone(2400, 1350, 37)
    lay(cv, closed_book(29, 640), 470, 690, 2.0)
    lay(cv, open_spread(16, 1360), 1600, 680, -1.5)
    out(cv, 'book_b.jpg')
    # C: three inside spreads fanned on the table: property overview, apartment amenities, floor plans
    cv = stone(2400, 1350, 41)
    lay(cv, open_spread(8, 1250), 760, 470, -5)
    lay(cv, open_spread(12, 1250), 1640, 520, 4)
    lay(cv, open_spread(11, 1350), 1180, 860, -1)
    out(cv, 'book_c.jpg')

def hero():
    """Rodrigo's own mockup (open Overlook spread + closed cover on white), used as is: only the empty white margin is trimmed
    to the 16:9 hero frame (objects span y 235-2723 of 3000, so nothing is cut)."""
    im = Image.open('/workspace/uploads/nomad-main-mockup-new.jpg').convert('RGB')
    W, H = im.size; h = round(W * 9 / 16); y0 = 215
    save(im.crop((0, y0, W, y0 + h)), SLUG, 'hero.jpg')

def main():
    flip(); mockups(); hero()
if __name__ == '__main__': main()
