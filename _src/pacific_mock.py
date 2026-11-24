"""Pacific Center (Nov 24, Rodrigo t99u): main image = open inside spread behind + closed cover in front on WHITE,
in the manner of Rodrigo's Nomad mockup; printed-brochure image = three inside spreads fanned on textured stone.
Built from Lauren's own pages (pages/pacific-center-brochure, no financial content in this brochure)."""
import os, glob
import numpy as np
from PIL import Image
import nomad_book as N, flyer_mockups as FM
from images import PAGES
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = PAGES + 'pacific-center-brochure/'
SLUG = 'pacific-center'
def page(stem): return Image.open(glob.glob(SRC + stem + '*.png')[0]).convert('RGB')
STEMS = {1: 'pg-1-', 2: 'sp-2-', 3: 'sp-3-', 4: 'sp-4-', 5: 'sp-5-', 6: 'sp-6-', 7: 'pg-7-'}
N.pg = lambda n: page(STEMS[n])          # reuse Nomad's spread / closed-book renderers on Pacific pages

def persp(o, k):
    """mild camera tilt: the far (top) edge a little narrower than the near edge"""
    W, H = o.size; d = W * k / 2
    return o.transform((W, H), Image.PERSPECTIVE, FM.coeffs([(d, 0), (W - d, 0), (W, H), (0, H)], [(0, 0), (W, 0), (W, H), (0, H)]), Image.BICUBIC)

def white(w, h):
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.hypot((xx - w * 0.45) / w, (yy - h * 0.42) / h)
    v = 252 - 22 * np.clip(r - 0.25, 0, None) ** 1.5 * 2
    return Image.fromarray(np.repeat(np.clip(v, 0, 255)[..., None], 3, 2).astype(np.uint8))

def lay(cv, obj, cx, cy, ang, k=0.0, shadow=0.8):
    if k: obj = persp(obj, k)
    FM.put_device(cv, obj.rotate(ang, Image.BICUBIC, expand=True), cx, cy, shadow=shadow)

def save(im, name): im.save(os.path.join(ROOT, 'assets', 'img', SLUG, name), 'JPEG', quality=86, optimize=True, progressive=True); print(name)

UPLOAD = '/workspace/uploads/pacific-desk-mockup-new.png'   # Rodrigo's own mockup (t101u): cover + Highlights spread on a concrete desk
HERO_BOX = (0, 70, 1448, 980)    # the book spans y 104-956 of 1086, so the hero frame is 1448:910 (build.py HERO_RATIO), nothing cut

def main():
    """Nov 24 (t101u): Rodrigo's desk mockup is the Pacific hero and card, used as provided.
    The earlier generated white hero, desk card and fanned book_fan.jpg (desk(), desk_card(), white()) are no longer used."""
    im = Image.open(UPLOAD).convert('RGB')
    save(im.crop(HERO_BOX), 'hero.jpg')
    save(im.resize((1440, 1080), Image.LANCZOS), 'card.jpg')     # source is 1448x1086 = 4:3 already
if __name__ == '__main__': main()
