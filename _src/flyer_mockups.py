"""Self-made flyer mockups (no stock): thin printed sheets on a textured surface, with lifted corners and soft shadows.
Run: python3 _src/flyer_mockups.py   (needs assets/img/<slug>/sheets/sNN.jpg from flyer_sheets.py; cover contacts already blurred)
Writes for PDX West: mock_cover.jpg (cover sheet with a second sheet under it) and mock_spread.jpg (three inside sheets fanned out, for 'The printed piece')."""
import os, math, numpy as np
from PIL import Image, ImageDraw, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 2304, 1728

def surface(base=(214, 207, 198), seed=3, light=(0.3, 0.2)):
    rng = np.random.default_rng(seed)
    def up(n, f): return np.array(Image.fromarray(rng.standard_normal((max(2, H // f), max(2, W // f))).astype(np.float32)).resize((W, H), Image.BICUBIC))
    v = rng.standard_normal((H, W)) * 6 + up(0, 3) * 3.5 + up(0, 240) * 1.5
    img = np.array(base, float)[None, None, :] + v[..., None] * np.array([1, .98, .95])
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.hypot(xx / W - light[0], yy / H - light[1])
    img = img * (1.05 - 0.13 * d)[..., None]
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))

def coeffs(dst, src):
    A, B = [], []
    for (x, y), (u, v) in zip(dst, src):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]; B += [u, v]
    return np.linalg.solve(np.array(A, float), np.array(B, float)).tolist()

def rect(cx, cy, w, ang):
    h = w / 1.2945; a = math.radians(ang); c, s = math.cos(a), math.sin(a)
    pts = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]

SS = 4   # supersampling for the sheet artwork and every mask

def _poly_mask(pts, size, scale=2):
    m = Image.new('L', (size[0] * scale, size[1] * scale), 0)
    ImageDraw.Draw(m).polygon([(x * scale, y * scale) for x, y in pts], fill=255)
    return np.asarray(m.resize(size, Image.BOX), np.float32) / 255

def _multiply(cv, a, tint=(0.40, 0.37, 0.34)):
    """darken the canvas where alpha a>0 (a multiply shadow keeps the surface texture visible)"""
    c = np.asarray(cv, np.float32)
    c = c * (1 - a[..., None]) + c * np.array(tint, np.float32) * a[..., None]
    cv.paste(Image.fromarray(np.clip(c, 0, 255).astype(np.uint8)))

def place(cv, src, corners, lift_corner=None, lift=0.0, shadow=1.0):
    """Lay a flat printed sheet `src` on canvas `cv` at `corners` (TL,TR,BR,BL).
    The sheet is one exact perspective warp rendered at SS x and downsampled, with an edge-replicated source so the
    anti-aliased edge carries the artwork's own colour (no fringe, no rim). Light comes from the top-left.
    lift_corner (0..3) suggests a slightly raised corner through light and shadow only (no geometry seams)."""
    W_, H_ = cv.size
    P = np.array(corners, float)
    # --- shadows: contact, mid and ambient layers, offset away from the light
    a = np.zeros((H_, W_), np.float32)
    base = _poly_mask(P, (W_, H_))
    lifted = None
    if lift_corner is not None and lift > 0:
        yy, xx = np.mgrid[0:H_, 0:W_]
        diag = np.hypot(*(P[2] - P[0]))
        cx, cy = P[lift_corner]
        lifted = np.clip(1 - np.hypot(xx - cx, yy - cy) / (0.42 * diag), 0, 1) ** 2
    for off, blur, k in [((0, 0), 2.5, 0.20), ((1.2, 2.0), 1.6, 0.55), ((5, 9), 9, 0.22), ((16, 26), 38, 0.20)]:
        m = Image.fromarray((base * 255).astype(np.uint8)).transform((W_, H_), Image.AFFINE, (1, 0, -off[0], 0, 1, -off[1]), Image.BILINEAR)
        m = np.asarray(m.filter(ImageFilter.GaussianBlur(blur)), np.float32) / 255
        if lifted is not None and blur < 5: m = m * (1 - 0.85 * lifted)      # the raised corner does not touch the table
        a = np.maximum(a, m * k * shadow)
    if lifted is not None:
        o = lift * 0.9
        m = Image.fromarray((base * 255).astype(np.uint8)).transform((W_, H_), Image.AFFINE, (1, 0, -o * .7, 0, 1, -o), Image.BILINEAR)
        m = np.asarray(m.filter(ImageFilter.GaussianBlur(22)), np.float32) / 255 * lifted
        a = np.maximum(a, m * 0.30 * shadow)
    a = a * (1 - base)          # shadow only outside the sheet; the sheet itself is pasted on top
    _multiply(cv, a)
    # --- the sheet
    x0, y0 = np.floor(P.min(0)).astype(int) - 2; x1, y1 = np.ceil(P.max(0)).astype(int) + 2
    bw, bh = x1 - x0, y1 - y0
    pad = 8
    sp = Image.fromarray(np.pad(np.asarray(src.convert('RGB')), ((pad, pad), (pad, pad), (0, 0)), mode='edge'))
    sw, sh = src.size
    dst = [((x - x0) * SS, (y - y0) * SS) for x, y in P]
    srcq = [(pad, pad), (pad + sw, pad), (pad + sw, pad + sh), (pad, pad + sh)]
    hi = sp.transform((bw * SS, bh * SS), Image.PERSPECTIVE, coeffs(dst, srcq), Image.BICUBIC)
    tile = np.asarray(hi.resize((bw, bh), Image.LANCZOS), np.float32)
    m = Image.new('L', (bw * SS, bh * SS), 0); ImageDraw.Draw(m).polygon(dst, fill=255)
    al = np.asarray(m.resize((bw, bh), Image.BOX), np.float32) / 255
    # paper lighting: soft gradient from the top-left light, a touch of sheen on a raised corner
    yy, xx = np.mgrid[y0:y1, x0:x1]
    t = ((xx - P[:, 0].mean()) * 0.6 + (yy - P[:, 1].mean())) / np.hypot(bw, bh)
    lightm = 1.02 - 0.05 * t
    if lifted is not None:
        lightm = lightm + 0.035 * lifted[y0:y1, x0:x1]
    tile = np.clip(tile * lightm[..., None], 0, 255)
    reg = np.asarray(cv, np.float32)[y0:y1, x0:x1]
    out_ = reg * (1 - al[..., None]) + tile * al[..., None]
    cv.paste(Image.fromarray(out_.astype(np.uint8)), (int(x0), int(y0)))
    return cv

def sheets(slug): return [Image.open(os.path.join(ROOT, 'assets', 'img', slug, 'sheets', f)).convert('RGB') for f in sorted(os.listdir(os.path.join(ROOT, 'assets', 'img', slug, 'sheets')))]

def out(im, slug, name): p = os.path.join(ROOT, 'assets', 'img', slug, name); im.save(p, 'JPEG', quality=84, optimize=True, progressive=True); print(p)

def pdx():
    S = sheets('pdx-west')
    # hero.jpg + card.jpg: Rodrigo's mockup, composited onto the cream surface by pdx_rodrigo_mockup.py (Nov 23)
    # card: Kress framing, single thin cover with a lifted corner and a second sheet peeking underneath
    k = W / 1024
    cv = surface(seed=3)
    place(cv, S[1], rect(498 * k, 372 * k, 540 * k, 3.0), shadow=.6)
    place(cv, S[0], rect(532 * k, 400 * k, 565 * k, -6.5), lift_corner=2, lift=42)
    out(cv, 'pdx-west', 'mock_cover.jpg')   # printed piece; card.jpg + hero.jpg now come from pdx_rodrigo_mockup.py
    # printed piece: three inside sheets fanned out
    cv = surface(seed=21, light=(0.5, 0.2))
    place(cv, S[2], rect(700, 930, 1040, -7), shadow=.8)
    place(cv, S[7], rect(1610, 930, 1040, 7), shadow=.8)
    place(cv, S[4], rect(1155, 870, 1180, 1.5), lift_corner=2, lift=30)
    out(cv, 'pdx-west', 'mock_spread.jpg')
    import pdx_rodrigo_mockup; pdx_rodrigo_mockup.main()   # Rodrigo's mockup (Nov 23) replaces hero.jpg + card.jpg

if __name__ == '__main__': pdx()
