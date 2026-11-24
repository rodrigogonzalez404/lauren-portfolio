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
FIXED = '/workspace/uploads/leftbank-desk-mockup-bleed-fixed.png'   # t104u: master with the black block bled to the sheet's left edge
ORANGE = np.array([202, 86, 37])

def shadowed(src, out, off=(4, 16), blur=30, k=0.95):
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

def bleed_fix(im):
    """t104u: the black 'Local Amenities' block on the printed map sheet stopped a few px short of the sheet's left edge,
    leaving a white sliver of paper. The sheet's left edge is fitted as a straight line (desk -> paper transition) and,
    row by row, everything from that line to the block is painted the block's black, anti-aliased by sub-pixel coverage,
    keeping the sheet's thin dark edge line, so the paper edge against the desk stays natural. Nothing else in the photo changes."""
    a = np.asarray(im, np.float32).copy(); L = a.mean(2)
    rows, ys, es, xbs = range(820, 975), [], [], {}
    for y in rows:
        seg = L[y, 400:560]; blk = np.where(seg < 40)[0]
        if not len(blk) or blk[0] > 90: continue
        xb = 400 + blk[0]; dl = np.median(L[y, xb - 30:xb - 12])
        w = L[y, xb - 10:xb]; k = int(np.argmin(w[:-1]))
        if w[k] < dl - 25: x = xb - 10 + k + 1                # the sheet's thin dark edge line: paper starts just inside it
        else:
            x = xb - 10
            while x < xb and L[y, x] < dl + 25: x += 1       # no edge line: first paper pixel
        xbs[y] = xb; ys.append(y); es.append(x)
    for y, x in zip(ys, es):                                  # the sheet's own dark edge line stays; the paper sliver inside it turns black
        if y < min(ys) + 2: continue                          # the block's top edge row: leave the paper margin above it
        a[y, x:xbs[y]] = 1
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def main():
    shadowed(os.path.join(I, 'sheets', 's01.jpg'), 'brochure_front.jpg')
    shadowed(os.path.join(I, 'sheets', 's07.jpg'), 'brochure_back.jpg')
    im = bleed_fix(Image.open(UPLOAD).convert('RGB'))            # 1448x1086 = 4:3; the upload itself stays untouched
    im.save(FIXED)
    im.crop(HERO_BOX).save(os.path.join(I, 'hero.jpg'), 'JPEG', quality=90, optimize=True, progressive=True)   # shown in a 1448:920 frame (build.py HERO_RATIO)
    im.resize((1440, 1080), Image.LANCZOS).save(os.path.join(I, 'card.jpg'), 'JPEG', quality=88, optimize=True, progressive=True)
if __name__ == '__main__': main()
