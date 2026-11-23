"""Big Pink (proposal, Nov 23): assets for the branding + Ceros case. Sources live outside the repo:
  /workspace/bigpink/cap/cNN.png      Ceros screens captured from the preview link (1600x900 canvas, headless Chrome)
  /workspace/bigpink/media/*          original Ceros media (logo-1/2/4.jpg concept boards, marketing-material mockup)
  /workspace/uploads/big-pink.pdf     Lauren's logo-concepts deck (Jul 2025)
  /workspace/bigpink/rendered/*.jpg  laptop renders (render_laptops.js -> CSS laptop on the shared cream): marketplace hero + card (the Big Pink
                                       card is the white OnePink mockup since t76u). Re-run render_laptops.js only if the cover screens change.
OnePink wordmark: onepink-h.svg / onepink-vertical.svg, traced (trace_onepink.py, potrace) from the white letters on the
Ceros concept board media/logo-4.jpg; path .w1 = ONE, .w2 = PINK.
Writes assets/img/big-pink/ and assets/img/marketplace/."""
import os, sys, subprocess, tempfile, shutil, io
import cairosvg
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.dirname(HERE); ROOT = os.path.dirname(SRC)
sys.path.insert(0, SRC)
from palette import CREAM
CAP = '/workspace/bigpink/cap/'; MED = '/workspace/bigpink/media/'; PDF = '/workspace/uploads/big-pink.pdf'
OUT = os.path.join(ROOT, 'assets', 'img', 'big-pink')
# design screens shown in the laptop viewer (Ceros order). Left out: c04 SWOT (empty headings), c10-c12 market figures,
# c14 competitive set (rents), c22 fee terms, c26-c31 + c36-c37 team / clients / references / lease map / services,
# c32 repositioning text (contains copy from another project).
SCREENS = ['c01', 'c02', 'c03', 'c05', 'c06', 'c07', 'c08', 'c09', 'c13', 'c15', 'c16', 'c17', 'c18', 'c19a', 'c19b', 'c19c', 'c20', 'c21', 'c23', 'c24', 'c25', 'c33', 'c34', 'c35', 'c38']

def save(im, rel, w=None, q=84):
    p = os.path.join(OUT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    im = im.convert('RGB')
    if w and im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(p, 'JPEG', quality=q, optimize=True, progressive=True)

def on_cream(im):
    a = np.asarray(im.convert('RGB'), np.float32)
    return Image.fromarray(np.clip(a * (np.array(CREAM, np.float32) / 255), 0, 255).astype(np.uint8))

def trim_white(im, pad=0):
    a = np.asarray(im.convert('L')); ys, xs = np.nonzero(a < 245)
    return im.crop((max(0, xs.min() - pad), max(0, ys.min() - pad), min(im.width, xs.max() + 1 + pad), min(im.height, ys.max() + 1 + pad)))

NAVY, ROSE = '#282334', '#C67484'
REND = '/workspace/bigpink/rendered/'

def onepink(width, one='#FFFFFF', pink=ROSE, name='onepink-h.svg'):
    svg = open(os.path.join(HERE, name)).read()
    svg = svg.replace('class="w1" fill="currentColor"', f'class="w1" fill="{one}"').replace('class="w2" fill="currentColor"', f'class="w2" fill="{pink}"')
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(), output_width=int(width)))).convert('RGBA')

def hero():
    # the lead identity: OnePink on the palette's Dark Blue, ONE white + PINK rose as in the sample marketing material
    W, H = 3200, 1800
    rng = np.random.default_rng(11)
    yy, xx = np.mgrid[0:H, 0:W]
    img = np.array([40, 35, 52], np.float32)[None, None] + rng.standard_normal((H, W, 1)).astype(np.float32) * 1.4
    d = np.hypot((xx - W * .5) / W, (yy - H * .5) / H)
    img *= (1.10 - 0.30 * d)[..., None]
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    L = onepink(1900)
    im.paste(L, ((W - L.width) // 2, (H - L.height) // 2), L)
    save(im, 'hero.jpg', q=88)

def white_frame(im, ratio, margin=0.04):
    """Fit the whole mockup (no device cropped) into `ratio`, padding with white around the content."""
    a = np.asarray(im.convert('L')); ys, xs = np.nonzero(a < 245)
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    m = int((x1 - x0) * margin); x0, x1, y0, y1 = x0 - m, x1 + m, y0 - m, y1 + m
    w, h = x1 - x0, y1 - y0
    if w / h > ratio: h = round(w / ratio)
    else: w = round(h * ratio)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    out = Image.new('RGB', (w, h), (255, 255, 255))
    out.paste(im, (w // 2 - cx, h // 2 - cy))
    return out

def main():
    for i, c in enumerate(SCREENS, 1): save(Image.open(CAP + c + '.png'), f'scr/s{i:02d}.jpg', 1600)
    for n, f in (('oneeleven', 'logo-1.jpg'), ('bigpink', 'logo-2.jpg'), ('onepink', 'logo-4.jpg')): save(Image.open(MED + f), f'concept_{n}.jpg', 2400)
    # sample marketing material on its ORIGINAL white (Rodrigo t76u: no beige) — also the home/works card
    mk = Image.open(MED + 'bigpink-marketingmaterial-mockup-copy.jpg').convert('RGB')
    save(trim_white(mk, 160), 'material.jpg', 2400)
    save(white_frame(mk, 16 / 9), 'card-wide.jpg', 2400)   # home featured slot (Nomad's old place)
    save(white_frame(mk, 4 / 3), 'card.jpg', 1600)        # works index, Next Project
    with tempfile.TemporaryDirectory() as t:
        for n, name in ((2, 'moodboard'), (5, 'concept_prism')):
            subprocess.run(['pdftoppm', '-f', str(n), '-l', str(n), '-r', '240', '-png', '-singlefile', PDF, f'{t}/p'], check=True, stderr=subprocess.DEVNULL)
            im = Image.open(f'{t}/p.png')
            save(trim_white(im, 0) if name == 'moodboard' else im, name + '.jpg', 2400)
    hero()
    # Marketplace I & II: REMOVED from the site Nov 23 PM (Rodrigo t78u). Sources kept; marketplace_assets() is not called.
    print('big-pink assets ->', OUT)
def marketplace_assets():
    """(unused since t78u) the curated Marketplace design screens + laptop hero/card."""
    sel = '/workspace/redesign/img/ceros/sel/'
    for i, f in enumerate(['marketplace-%02d.jpg' % k for k in (1, 2, 3, 5, 9, 11, 13, 15, 16)], 1):
        p = os.path.join(ROOT, 'assets', 'img', 'marketplace', 'scr', f's{i:02d}.jpg'); os.makedirs(os.path.dirname(p), exist_ok=True)
        Image.open(sel + f).convert('RGB').save(p, 'JPEG', quality=84, optimize=True, progressive=True)
    for n in ('hero', 'card'): shutil.copy(REND + f'marketplace-{n}.jpg', os.path.join(ROOT, 'assets', 'img', 'marketplace', f'{n}.jpg'))

if __name__ == '__main__': main()
