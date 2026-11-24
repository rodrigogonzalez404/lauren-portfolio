"""Leftbank (Nov 24, Rodrigo t102u):
- 'The brochure' section: the front/back pages get a soft drop shadow where the photo sits over Lauren's orange offset block
  (shadow cast onto the orange only; the artwork itself is untouched). Written as brochure_front/back.jpg; the iPad viewer keeps the plain sheets.
- hero + card = Rodrigo's own desk mockup (tablet with the cover + printed Local Amenities map), used as provided."""
import os
import numpy as np
from PIL import Image, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
I = os.path.join(ROOT, 'assets', 'img', 'leftbank')
UPLOAD = '/workspace/uploads/leftbank-desk-mockup-new.jpg'
HERO_BOX = (0, 50, 1448, 970)   # tablet top ~y85, map sheet bottom ~y955 of 1086: nothing cut
ORANGE = np.array([202, 86, 37])

def shadowed(src, out, off=(8, 11), blur=18, k=0.38):
    a = np.asarray(Image.open(src).convert('RGB')).astype(np.float32); H, W = a.shape[:2]
    o = np.abs(a - ORANGE).sum(2) < 30
    rows, cols = o.sum(1), o.sum(0)
    y0 = np.where(rows > 1000)[0].max() + 1          # bottom of the orange top band = top edge of the photo
    x1 = np.where(cols > 500)[0].min()               # left edge of the orange right band = right edge of the photo
    m = Image.new('L', (W, H), 0); m.paste(255, (0, y0, x1, H))
    sh = m.transform((W, H), Image.AFFINE, (1, 0, -off[0], 0, 1, -off[1]), Image.BILINEAR).filter(ImageFilter.GaussianBlur(blur))
    s = np.asarray(sh, np.float32) / 255 * k
    s *= ~(np.asarray(m) > 0)                          # only outside the photo
    s *= np.asarray(Image.fromarray((o * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1)), np.float32) / 255   # only on the orange
    a = a * (1 - s[..., None])
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(os.path.join(I, out), 'JPEG', quality=90, optimize=True, progressive=True); print(out)

def main():
    shadowed(os.path.join(I, 'sheets', 's01.jpg'), 'brochure_front.jpg')
    shadowed(os.path.join(I, 'sheets', 's07.jpg'), 'brochure_back.jpg')
    im = Image.open(UPLOAD).convert('RGB')                       # 1448x1086 = 4:3
    im.crop(HERO_BOX).save(os.path.join(I, 'hero.jpg'), 'JPEG', quality=90, optimize=True, progressive=True)   # shown in a 1448:920 frame (build.py HERO_RATIO)
    im.resize((1440, 1080), Image.LANCZOS).save(os.path.join(I, 'card.jpg'), 'JPEG', quality=88, optimize=True, progressive=True)
if __name__ == '__main__': main()
