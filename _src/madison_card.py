"""Madison Plaza home/works card (Nov 23, Rodrigo): his device + brochure mockup (white background, also the case hero,
which stays untouched) set on the shared cream surface, the whole composition fitted inside the 4:3 card with padding.
Light pixels are multiplied onto the cream (backdrop, shadows, paper, aluminium); device screens are kept exact.
Writes assets/img/madison-plaza/card.jpg (build.card_img prefers card.jpg over hero.jpg)."""
import os, cv2, numpy as np
from PIL import Image
import flyer_mockups as F
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = '/workspace/lauren-case-studies/mockups/madison-plaza_hero-override.jpg'
W, H = F.W, F.H          # 2304 x 1728 (4:3)
FILL = 0.88              # composition width as a share of the card

def bg_weight(a):
    """Multiply weight (1 = takes the cream fully). Backdrop and soft shadows: 1. Device screens (regions enclosed by
    their dark bezels): 0, so the screens stay true. Everything else (printed pages, aluminium, pencil): by lightness, so
    white surfaces pick up the same ambient cream and no cut-out edges or halos appear."""
    b = cv2.resize(a, None, fx=.5, fy=.5, interpolation=cv2.INTER_AREA)
    g = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY).astype(np.float32)
    dark = (g < 90).astype(np.uint8)                                   # bezels / keyboard
    dark = cv2.morphologyEx(dark, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    h, w = dark.shape; f = dark.copy(); cv2.floodFill(f, np.zeros((h + 2, w + 2), np.uint8), (0, 0), 1)
    holes = ((1 - f) > 0).astype(np.uint8)                             # enclosed by dark = screens
    n, lab, st, _ = cv2.connectedComponentsWithStats(holes)
    scr = np.isin(lab, [i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] > 20000])
    wgt = np.clip((g - 150) / 90, 0, 1)
    wgt[scr] = 0
    wgt = cv2.GaussianBlur(wgt, (0, 0), 1.2)
    return cv2.resize(wgt, (a.shape[1], a.shape[0]), interpolation=cv2.INTER_LINEAR)[..., None]

def main():
    a = cv2.imread(SRC)
    wgt = bg_weight(a)
    k = W * FILL / a.shape[1]
    if a.shape[0] * k > H * FILL: k = H * FILL / a.shape[0]
    nw, nh = int(a.shape[1] * k), int(a.shape[0] * k)
    a = cv2.resize(a, (nw, nh), interpolation=cv2.INTER_AREA).astype(np.float32)
    wgt = cv2.resize(wgt[..., 0], (nw, nh), interpolation=cv2.INTER_AREA)[..., None]
    cv = np.asarray(F.surface(seed=11, light=(0.45, 0.25)), np.float32)[..., ::-1].copy()   # BGR
    x, y = (W - nw) // 2, (H - nh) // 2 + int(H * 0.01)
    reg = cv[y:y + nh, x:x + nw]
    cv[y:y + nh, x:x + nw] = wgt * (reg * a / 255.0) + (1 - wgt) * a
    out = os.path.join(ROOT, 'assets/img/madison-plaza/card.jpg')
    Image.fromarray(np.clip(cv, 0, 255).astype(np.uint8)[..., ::-1]).save(out, quality=86, optimize=True, progressive=True)
    print('madison card', out, (W, H))
if __name__ == '__main__': main()
