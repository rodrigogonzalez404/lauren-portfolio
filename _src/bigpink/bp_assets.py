"""Big Pink (proposal, Nov 23): assets for the branding + Ceros case. Sources live outside the repo:
  /workspace/bigpink/cap/cNN.png      Ceros screens captured from the preview link (1600x900 canvas, headless Chrome)
  /workspace/bigpink/media/*          original Ceros media (logo-1/2/4.jpg concept boards, marketing-material mockup)
  /workspace/uploads/big-pink.pdf     Lauren's logo-concepts deck (Jul 2025)
  /workspace/bigpink/rendered/*.jpg  laptop renders (render_laptops.js -> CSS laptop on the shared cream): big-pink card,
                                       marketplace hero + card. Re-run render_laptops.js only if the cover screens change.
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

def main():
    for i, c in enumerate(SCREENS, 1): save(Image.open(CAP + c + '.png'), f'scr/s{i:02d}.jpg', 1600)
    for n, f in (('oneeleven', 'logo-1.jpg'), ('bigpink', 'logo-2.jpg'), ('onepink', 'logo-4.jpg')): save(Image.open(MED + f), f'concept_{n}.jpg', 2400)
    save(on_cream(trim_white(Image.open(MED + 'bigpink-marketingmaterial-mockup-copy.jpg'), 120)), 'material.jpg', 2400)
    with tempfile.TemporaryDirectory() as t:
        for n, name in ((2, 'moodboard'), (5, 'concept_prism')):
            subprocess.run(['pdftoppm', '-f', str(n), '-l', str(n), '-r', '240', '-png', '-singlefile', PDF, f'{t}/p'], check=True, stderr=subprocess.DEVNULL)
            im = Image.open(f'{t}/p.png')
            save(trim_white(im, 0) if name == 'moodboard' else im, name + '.jpg', 2400)
    # Marketplace: the curated design screens already used on the site (16:9 captures)
    sel = '/workspace/redesign/img/ceros/sel/'
    for i, f in enumerate(['marketplace-%02d.jpg' % k for k in (1, 2, 3, 5, 9, 11, 13, 15, 16)], 1):
        p = os.path.join(ROOT, 'assets', 'img', 'marketplace', 'scr', f's{i:02d}.jpg'); os.makedirs(os.path.dirname(p), exist_ok=True)
        Image.open(sel + f).convert('RGB').save(p, 'JPEG', quality=84, optimize=True, progressive=True)
    hero()
    shutil.copy(REND + 'big-pink-card.jpg', os.path.join(OUT, 'card.jpg'))
    for n in ('hero', 'card'): shutil.copy(REND + f'marketplace-{n}.jpg', os.path.join(ROOT, 'assets', 'img', 'marketplace', f'{n}.jpg'))
    print('big-pink assets ->', OUT)
if __name__ == '__main__': main()
