"""Nomad mockup photos on the shared surface (palette.CREAM, now stone #ECEAE6). Rebuilt from the original scene
photos kept in /workspace/redesign/img/nomad-pre-cream-nov23/ (tan studio backdrops), written to
/workspace/redesign/img/nomad/ (images.py copies them into assets/img/nomad/). Same recipe as /workspace/mk/mock.py:
backdrop (soft mask by colour distance, border-connected) -> colour grade toward CREAM; texture is kept (no blur)."""
import os, sys, cv2, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from palette import CREAM
SRC = '/workspace/redesign/img/nomad-pre-cream-nov23/'; DST = '/workspace/redesign/img/nomad/'
FILES = ['n01_hero_spread-investment-summary.jpg', 'n02_cover-on-desk.jpg', 'n03_printed-stack.jpg', 'n06_tablet-neighborhood-map.jpg']

def convert(f):
    im = cv2.imread(SRC + f).astype(np.float32)
    lab = cv2.cvtColor(np.clip(im, 0, 255).astype(np.uint8), cv2.COLOR_BGR2LAB).astype(np.float32)
    edge = np.concatenate([lab[:8].reshape(-1, 3), lab[-8:].reshape(-1, 3), lab[:, :8].reshape(-1, 3), lab[:, -8:].reshape(-1, 3)])
    ref = np.median(edge, 0)
    # backdrop weight: chroma close to the backdrop's, lightness within the backdrop's shading range (shadows included)
    dc = np.hypot(lab[..., 1] - ref[1], lab[..., 2] - ref[2])
    dl = np.clip(ref[0] - lab[..., 0], 0, None) * 0.12 + np.clip(lab[..., 0] - ref[0], 0, None) * 0.8
    w = np.clip(1 - (dc - 12) / 8, 0, 1) * np.clip(1 - (dl - 16) / 14, 0, 1)
    # backdrop = only the regions connected to the image border (artwork greys inside the pieces are never touched),
    # with the backdrop's own texture speckles (small holes) filled
    m = (w > 0.5).astype(np.uint8)
    g = cv2.GaussianBlur(cv2.cvtColor(np.clip(im, 0, 255).astype(np.uint8), cv2.COLOR_BGR2GRAY), (0, 0), 1.5)
    edges = cv2.dilate(cv2.Canny(g, 18, 45), np.ones((5, 5), np.uint8))   # the outlines of the pieces wall the backdrop off
    m[edges > 0] = 0
    n, lab_, st, _ = cv2.connectedComponentsWithStats(m, 8)
    border = set(np.unique(np.concatenate([lab_[0], lab_[-1], lab_[:, 0], lab_[:, -1]]))) - {0}
    bgm = np.isin(lab_, list(border)).astype(np.uint8)
    wm = (w > 0.5).astype(np.uint8)
    for _ in range(4): bgm = cv2.dilate(bgm, np.ones((5, 5), np.uint8)) & wm   # grow back over the edge walls (geodesic, ~8 px)
    inv = 1 - bgm; n2, l2, s2, _ = cv2.connectedComponentsWithStats(inv, 8)
    small = [i for i in range(1, n2) if s2[i, cv2.CC_STAT_AREA] < 1500]
    bgm[np.isin(l2, small)] = 1
    dist = cv2.distanceTransform(bgm, cv2.DIST_L2, 5)
    # final weight: inside the backdrop region (grown 15 px so contact shadows and edge zones are included), each
    # pixel converts by how backdrop-like its colour is — soft, so no speckles and the pieces' own colours stay
    R = cv2.GaussianBlur(cv2.dilate(bgm, np.ones((31, 31), np.uint8)).astype(np.float32), (0, 0), 3)
    w = np.maximum(np.clip(dist / 3.0, 0, 1), cv2.GaussianBlur(w, (0, 0), 0.8) * R)
    # colour grade only (Rodrigo t78u): no blur / denoise — warm cast out (chroma x0.55), hue to stone, luminance kept
    # and lifted ~8% (capped at stone), so the photo's own texture, grain and light stay
    lum = im.mean(2, keepdims=True); bg = lum + (im - lum) * 0.55
    med = np.median(bg[bgm > 0], 0); st = np.array(CREAM[::-1], np.float32)
    Lt = min(st.mean(), med.mean() * 1.08); bg = bg * ((st * Lt / st.mean()) / med)
    out = im * (1 - w[..., None]) + bg * w[..., None]
    cv2.imwrite(DST + f, np.clip(out, 0, 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 90]); print(f)

def main():
    for f in FILES: convert(f)
if __name__ == '__main__': main()
