"""Madison Plaza cards (Rodrigo t79u, Nov 23): his device + brochure mockup (white background; also the case hero, which
stays untouched) on the textured pale-stone surface. ONLY the background takes the stone: the devices, screens and
brochure pages are copied exactly (pure white stays white — no multiply on the object). The object is separated from
the white backdrop by an edge-closed, border-connected mask; the backdrop (and its soft grey shadows) is multiplied
onto the stone, so the original shadows land on it. A short ramp just inside the mask edge lets shadow-grey (never
page-white, >= 242) blend into the stone so no seam shows.
Writes assets/img/madison-plaza/card-wide.jpg (16:9, home big slot) and card.jpg (4:3, works index)."""
import os, cv2, numpy as np
from PIL import Image
import flyer_mockups as F
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = '/workspace/lauren-case-studies/mockups/madison-plaza_hero-override.jpg'

def object_weight(a):
    """1 = keep exact pixel (object), 0 = backdrop (multiply onto stone)."""
    s = cv2.resize(a, None, fx=.5, fy=.5, interpolation=cv2.INTER_AREA)
    g = cv2.cvtColor(s, cv2.COLOR_BGR2GRAY).astype(np.float32)
    gb = cv2.GaussianBlur(g, (0, 0), 0.8)
    mag = np.hypot(cv2.Sobel(gb, cv2.CV_32F, 1, 0), cv2.Sobel(gb, cv2.CV_32F, 0, 1))
    e = ((mag > 16) | (g < 120)).astype(np.uint8)
    e = cv2.morphologyEx(e, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats((1 - e).astype(np.uint8), connectivity=4)
    border = set(lab[0, :]) | set(lab[-1, :]) | set(lab[:, 0]) | set(lab[:, -1]); border.discard(0)
    obj = (~np.isin(lab, list(border))).astype(np.uint8)
    n2, l2, s2, _ = cv2.connectedComponentsWithStats(obj)
    obj = np.isin(l2, [i for i in range(1, n2) if s2[i, 4] > 4000]).astype(np.uint8)
    obj = cv2.resize(obj, (a.shape[1], a.shape[0]), interpolation=cv2.INTER_NEAREST)
    G = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY).astype(np.float32)
    dist = cv2.distanceTransform(obj, cv2.DIST_L2, 5)
    ramp = np.clip(dist / 40.0, 0, 1)                       # 0 at the mask edge -> 1 at 40 px inside
    shadowish = np.clip((242 - G) / 12, 0, 1) * np.clip((G - 120) / 40, 0, 1)
    sat = a.max(2).astype(np.float32) - a.min(2)
    shadowish *= np.clip((14 - sat) / 8, 0, 1)
    # trim the closing fringe: backdrop white caught inside the mask edge (halo) is regrown into the backdrop, through
    # white pixels only, within 24 px of the edge; page edges have a grey outline, so pages are not eaten
    bgm = (obj == 0).astype(np.uint8); band = (dist < 40) & (obj > 0); white = G >= 236
    for _ in range(40):
        grow = cv2.dilate(bgm, np.ones((3, 3), np.uint8)).astype(bool) & band & white
        if not (grow & (bgm == 0)).any(): break
        bgm = (bgm.astype(bool) | grow).astype(np.uint8)
    obj = (bgm == 0).astype(np.uint8)
    dist = cv2.distanceTransform(obj, cv2.DIST_L2, 5); ramp = np.clip(dist / 40.0, 0, 1)
    w = obj * (1 - (1 - ramp) * shadowish)
    w = cv2.GaussianBlur(w.astype(np.float32), (0, 0), 1.0)
    w[(obj > 0) & (G >= 242)] = 1                           # page/screen white is never tinted
    return w, obj

def compose(a, w, obj, W, H, fill, seed, light):
    ys, xs = np.where(obj > 0)
    pad = int(0.025 * a.shape[1])
    x0, x1 = max(0, xs.min() - pad), min(a.shape[1], xs.max() + pad)
    y0, y1 = max(0, ys.min() - pad), min(a.shape[0], ys.max() + pad)
    a, w = a[y0:y1, x0:x1], w[y0:y1, x0:x1]
    k = min(W * fill / a.shape[1], H * fill / a.shape[0])
    nw, nh = int(a.shape[1] * k), int(a.shape[0] * k)
    a = cv2.resize(a, (nw, nh), interpolation=cv2.INTER_AREA).astype(np.float32)
    w = cv2.resize(w, (nw, nh), interpolation=cv2.INTER_AREA)[..., None]
    F.W, F.H = W, H
    cv = np.asarray(F.surface(seed=seed, light=light), np.float32)[..., ::-1].copy()   # BGR
    F.W, F.H = 2304, 1728
    x, y = (W - nw) // 2, (H - nh) // 2
    reg = cv[y:y + nh, x:x + nw]
    cv[y:y + nh, x:x + nw] = (1 - w) * (reg * a / 255.0) + w * a
    return Image.fromarray(np.clip(cv, 0, 255).astype(np.uint8)[..., ::-1])

# Financials (CONFIDENTIALITY: Madison p08 operating text is blurred in the flip-book) — the phone screen shows the same
# opex paragraph ("T12 operating expenses of $9,875 per unit ...") and is now large enough to read, so it is blurred
# here too; only neutral (text-on-white) pixels inside the rectangles, so the brochure's sky/photo is untouched.
# Rodrigo t80u (Nov 23, 2:52 PM PT): "please ensure nothing is blur on this image" — he approved showing the phone
# paragraph on the card, so no rectangles are blurred any more (kept for reference: (2766,1452,3214,1618), (3050,1612,3214,1700)).
BLUR = []
def blur_financials(a):
    for x0, y0, x1, y1 in BLUR:
        r = a[y0:y1, x0:x1].astype(np.float32)
        b = cv2.GaussianBlur(r, (0, 0), 7)
        sat = r.max(2) - r.min(2)
        m = cv2.GaussianBlur(((sat < 22) & (r.mean(2) > 40)).astype(np.float32), (0, 0), 2)[..., None]
        a[y0:y1, x0:x1] = np.clip(m * b + (1 - m) * r, 0, 255).astype(np.uint8)
    return a

def main():
    a = cv2.imread(SRC)   # no blur (Rodrigo t80u)
    w, obj = object_weight(a)
    d = os.path.join(ROOT, 'assets/img/madison-plaza')
    compose(a, w, obj, 2400, 1350, 0.94, 11, (0.45, 0.25)).save(os.path.join(d, 'card-wide.jpg'), quality=88, optimize=True, progressive=True)
    compose(a, w, obj, 2304, 1728, 0.94, 12, (0.45, 0.25)).save(os.path.join(d, 'card.jpg'), quality=88, optimize=True, progressive=True)
    print('madison cards', d)
if __name__ == '__main__': main()
