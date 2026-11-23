"""PDX West hero + card from Rodrigo's mockup (Nov 23): standing flyer cover, tablet with Property Highlights, flat back sheet.
Source (white studio background): /workspace/lauren-case-studies/mockups/pdx-west_rodrigo-mockup.png (1448x1086).
- Nothing is blurred: per Rodrigo (Nov 23) only financials are confidential; broker contacts stay readable.
- The white background becomes the cream surface used by flyer_mockups (same tone/texture as before): background and
  shadow pixels are MULTIPLIED onto the cream (so the soft studio shadows carry over and anti-aliased edges composite
  cleanly, no white halo); object pixels are kept as they are. Objects = saturated/dark pixels (holes filled) + hand-traced
  polygons for the neutral parts (standing flyer page stack/easel, flat sheet with its white margin and page edge).
Run: python3 _src/pdx_rodrigo_mockup.py   (also run at the end of flyer_mockups.pdx())"""
import os, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter
import flyer_mockups as F
ROOT = F.ROOT
SRC = '/workspace/lauren-case-studies/mockups/pdx-west_rodrigo-mockup.png'
CONTACTS_TRACED = [[(128, 634), (566, 598), (568, 662), (130, 706)],      # standing cover: 3 broker blocks
            [(450, 956), (968, 924), (970, 992), (452, 1014)]]     # flat back sheet: 3 broker blocks
CONTACTS = []   # Nov 23, Rodrigo: front-page contacts are not confidential -> nothing blurred (traced quads kept above in case)
STAND = [(47, 123), (30, 129), (31, 300), (27, 560), (27, 704), (66, 702), (73, 722), (85, 731), (100, 733), (140, 731), (140, 127)]
FLAT = [(415, 709), (1194, 652), (1405, 989), (1404, 997), (425, 1053), (423, 1050)]
BG = 253.0   # studio white level of the source

def poly_mask(pts, size, ss=4):
    m = Image.new('L', (size[0] * ss, size[1] * ss), 0)
    ImageDraw.Draw(m).polygon([(x * ss, y * ss) for x, y in pts], fill=255)
    return np.asarray(m.resize(size, Image.BOX), np.float32) / 255

def blur_quads(im):
    for q in CONTACTS:
        xs, ys = [p[0] for p in q], [p[1] for p in q]
        b = (min(xs) - 4, min(ys) - 4, max(xs) + 4, max(ys) + 4)
        reg = im.crop(b); m = poly_mask([(x - b[0], y - b[1]) for x, y in q], reg.size)
        panel = np.median(np.asarray(reg).reshape(-1, 3)[m.reshape(-1) > .5], 0)       # panel colour fills outside the quad
        r = np.asarray(reg, np.float32) * m[..., None] + panel * (1 - m[..., None])
        reg2 = Image.fromarray(r.astype(np.uint8))
        small = reg2.resize((max(1, reg2.width // 24), max(1, reg2.height // 24)), Image.BILINEAR)
        reg2 = small.resize(reg2.size, Image.BILINEAR).filter(ImageFilter.GaussianBlur(max(6, reg2.height // 6)))
        mf = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)), np.float32)[..., None] / 255
        out = np.asarray(reg2, np.float32) * mf + np.asarray(reg, np.float32) * (1 - mf)
        im.paste(Image.fromarray(out.astype(np.uint8)), b[:2])
    return im

def object_alpha(a):
    mn, mx = a.min(2).astype(int), a.max(2).astype(int)
    m = (((mx - mn) > 14) | (mn < 90)).astype(np.uint8) * 255
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    ff = m.copy(); h, w = m.shape; cv2.floodFill(ff, np.zeros((h + 2, w + 2), np.uint8), (0, 0), 255); m = m | (~ff)
    size = (w, h)
    m = np.maximum(m.astype(np.float32) / 255, np.maximum(poly_mask(STAND, size), poly_mask(FLAT, size)))
    m = cv2.erode((m > .5).astype(np.uint8), np.ones((3, 3), np.uint8)).astype(np.float32)
    return cv2.GaussianBlur(m, (0, 0), 0.7)

def compose(src, alpha, scale, center, seed=11, light=(0.35, 0.25)):
    cv = np.asarray(F.surface(seed=seed, light=light), np.float32)
    w, h = round(src.width * scale), round(src.height * scale)
    s = np.asarray(src.resize((w, h), Image.LANCZOS), np.float32)
    al = np.asarray(Image.fromarray((alpha * 255).astype(np.uint8)).resize((w, h), Image.LANCZOS), np.float32)[..., None] / 255
    x0, y0 = round(center[0] - w / 2), round(center[1] - h / 2)
    reg = cv[y0:y0 + h, x0:x0 + w]
    mult = reg * np.clip(s / BG, 0, 1)
    cv[y0:y0 + h, x0:x0 + w] = s * al + mult * (1 - al)
    return Image.fromarray(np.clip(cv, 0, 255).astype(np.uint8))

def main():
    src = blur_quads(Image.open(SRC).convert('RGB'))
    alpha = object_alpha(np.asarray(src))
    # hero: the case hero shows a wide central band (~58% of the height at desktop), so keep all three objects inside it
    F.out(compose(src, alpha, 0.93, (1152, 880)), 'pdx-west', 'hero.jpg')
    # card (4:3, shown whole on Home / Works / Next Project): Kress-like breathing room
    F.out(compose(src, alpha, 1.36, (1152, 864), seed=3, light=(0.3, 0.2)), 'pdx-west', 'card.jpg')
    return src, alpha

if __name__ == '__main__': main()
