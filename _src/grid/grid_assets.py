"""The Grid (Kirkland 405) case-study assets (Nov 23). Run by images.py (after OUT is wiped) or on its own.
Writes assets/img/the-grid/:
  hero.jpg   chosen logo on the deck's warm stone, over a faint square grid (code-built, vector logo)
  card.jpg   the existing lobby-sign mockup (unchanged thumbnail Rodrigo referred to)
  sign_blade.jpg / sign_lobby.jpg            The Grid in place, cropped from Lauren's naming deck (page 3)
  stage_blade / stage_lobby / pulse_blade / pulse_lobby .jpg   the two concepts in place (deck pages 5 and 7)
  cards.jpg  business cards (front + back), code-built, laid on the shared cream surface
Logos: _src/grid/logo-*.svg (extracted vector paths from the deck PDF, fill=currentColor; see extract_logos.py)."""
import os, io, sys, math, subprocess, tempfile
import numpy as np, cairosvg
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.dirname(HERE); ROOT = os.path.dirname(SRC)
sys.path.insert(0, SRC)
import flyer_mockups as FM
from palette import CREAM
OUT = os.path.join(ROOT, 'assets', 'img', 'the-grid')
DECK = '/workspace/lauren-case-studies/source/extracted/Kirkland Brand Design/Kirkland405_Logo-NameIdeas_draft1.pdf'
MOCK = '/workspace/lauren-case-studies/mockups/the-grid_lobby-sign.jpg'
FONT = '/usr/share/fonts/truetype/sand-box/google/Open Sans/OpenSans-VariableFont_wdth,wght.ttf'
GREY, STONE, GRAPHITE = '#777C80', '#EAE7E3', '#1D1D1F'
SYMBOL_VB = '149.25 241.25 136.2 146.5'   # the two frames only (wordmark starts at x~308)

def svg(name, color, vb=None):
    s = open(os.path.join(HERE, f'logo-{name}.svg')).read().replace('currentColor', color)
    if vb:
        import re
        w, h = vb.split()[2:]
        s = re.sub(r'width="[^"]+" height="[^"]+" viewBox="[^"]+"', f'width="{w}" height="{h}" viewBox="{vb}"', s, count=1)
    return s

def logo(name, color, width, vb=None):
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg(name, color, vb).encode(), output_width=int(width)))).convert('RGBA')

def save(im, name, q=86):
    os.makedirs(OUT, exist_ok=True)
    im.convert('RGB').save(os.path.join(OUT, name), 'JPEG', quality=q, optimize=True, progressive=True)

def hero():
    W, H = 3200, 1800
    rng = np.random.default_rng(5)
    base = np.array([234, 231, 227], np.float32)
    yy, xx = np.mgrid[0:H, 0:W]
    img = base[None, None] + rng.standard_normal((H, W, 1)).astype(np.float32) * 1.6
    d = np.hypot((xx - W * .5) / W, (yy - H * .45) / H)
    img *= (1.015 - 0.07 * d)[..., None]
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    # faint square grid, aligned to the centre
    g = Image.new('L', (W, H), 0); dr = ImageDraw.Draw(g); step = 150
    for x in range(W // 2 % step, W, step): dr.line([(x, 0), (x, H)], fill=255, width=2)
    for y in range(H // 2 % step, H, step): dr.line([(0, y), (W, y)], fill=255, width=2)
    a = np.asarray(g, np.float32)[..., None] / 255 * 0.14
    arr = np.asarray(im, np.float32); arr = arr * (1 - a) + (arr * 0.80) * a
    im = Image.fromarray(arr.astype(np.uint8))
    L = logo('the-grid', GREY, 1500)
    im.paste(L, ((W - L.width) // 2, (H - L.height) // 2), L)
    save(im, 'hero.jpg', 88)

def deck_crops():
    with tempfile.TemporaryDirectory() as t:
        for n, names in ((3, ('sign_blade', 'sign_lobby')), (5, ('stage_blade', 'stage_lobby')), (7, ('pulse_blade', 'pulse_lobby'))):
            subprocess.run(['pdftoppm', '-f', str(n), '-l', str(n), '-r', '300', '-png', '-singlefile', DECK, f'{t}/p'], check=True)
            im = Image.open(f'{t}/p.png').convert('RGB'); W, H = im.size
            x0 = int(math.ceil(585.5 / 1008 * W))
            top = im.crop((x0, 0, W, int(296.5 / 612 * H)))
            bot = im.crop((x0, int(math.ceil(316 / 612 * H)), W, H))
            save(top, names[0] + '.jpg', 84); save(bot, names[1] + '.jpg', 84)

def card_art(front=True, w=1750):
    h = int(w * 2 / 3.5)
    if front:
        c = Image.new('RGB', (w, h), STONE)
        L = logo('the-grid', GREY, w * 0.50); c.paste(L, ((w - L.width) // 2, (h - L.height) // 2), L)
        return c
    c = Image.new('RGB', (w, h), GRAPHITE)
    big = logo('the-grid', '#2A2A2D', h * 1.55 * 136.2 / 146.5, SYMBOL_VB)   # tonal frames running off the edge
    c.paste(big, (int(w * 0.50), int(h * 0.12)), big)
    L = logo('the-grid', '#FFFFFF', w * 0.25); c.paste(L, (int(w * 0.085), int(h - w * 0.085 - L.height)), L)
    return c

def crect(cx, cy, w, ang, ratio=3.5 / 2):
    h = w / ratio; a = math.radians(ang); c, s = math.cos(a), math.sin(a)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]]

def cards():
    cv = FM.surface(seed=21, light=(0.35, 0.2))
    W, H = cv.size
    FM.place(cv, card_art(False), crect(W * .60, H * .60, W * .44, 5.5), shadow=0.9)
    FM.place(cv, card_art(True), crect(W * .39, H * .40, W * .44, -7), shadow=0.9)
    save(cv, 'cards.jpg', 86)

def entrance():
    """Card + hero (Rodrigo t78u: "should be on a wall, looking like the logo of an entrance of a building"): the
    entrance mockup from Lauren's naming deck p.3 — the mounted panel on the stone-clad facade beside the glass doors,
    sidewalk below. Photographic, sharp, native resolution (the deck image is 1774 px wide). The old self-made
    lobby-sign (MOCK) and the vector-logo hero() are retired."""
    im = Image.open(os.path.join(OUT, 'sign_blade.jpg')).convert('RGB'); W, H = im.size
    # gentle white balance toward pale stone (the cladding reads cool blue-grey): 50% of the way, by lightness only on
    # light pixels, so the black panel, the glass and the texture are untouched
    a = np.asarray(im, np.float32); L = a.mean(2)
    lightm = L > 150; med = np.median(a[lightm], 0); st = np.array(CREAM, np.float32)
    gain = 1 + 0.5 * ((st / st.mean()) / (med / med.mean()) - 1)
    wgt = np.clip((L - 120) / 80, 0, 1)[..., None]
    im = Image.fromarray(np.clip(a * (1 - wgt) + a * gain * wgt, 0, 255).astype(np.uint8))
    cw = round(H * 4 / 3); save(im.crop((W - cw, 0, W, H)), 'card.jpg', 90)            # 4:3, keeps the panel and the doors
    ch = round(W * 9 / 16); y0 = round((H - ch) * 0.08)   # 16:9, keeps the panel's top edge
    save(im.crop((0, y0, W, y0 + ch)), 'hero.jpg', 90)

def main():
    os.makedirs(OUT, exist_ok=True)
    deck_crops(); cards(); entrance()
    print('the-grid assets ->', OUT)
if __name__ == '__main__': main()
