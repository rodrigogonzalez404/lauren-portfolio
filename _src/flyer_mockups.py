"""Self-made flyer mockups (no stock): thin printed sheets on a textured surface, with lifted corners and soft shadows.
Run: python3 _src/flyer_mockups.py   (needs assets/img/<slug>/sheets/sNN.jpg from flyer_sheets.py; cover contacts already blurred)
Writes for PDX West: hero.jpg (2304x1728, key content inside the 16:9 band the hero shows), card.jpg (Kress-style
thumbnail) and mock_spread.jpg (three inside sheets fanned out, for 'The printed piece')."""
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

def place(cv, src, corners, lift_corner=None, lift=0.0, shadow=1.0, N=14):
    """Lay sheet `src` on canvas `cv` at `corners` (TL,TR,BR,BL). lift_corner 0..3 curls that corner up by `lift` px."""
    sw, sh = src.size
    P = [np.array(p, float) for p in corners]
    cu = [(0, 0), (1, 0), (1, 1), (0, 1)]
    def flat(u, v): return (1 - u) * (1 - v) * P[0] + u * (1 - v) * P[1] + u * v * P[2] + (1 - u) * v * P[3]
    def f(u, v):
        if lift_corner is None: return 0.0
        cx, cy = cu[lift_corner]; d = math.hypot(u - cx, v - cy) / 0.55
        return max(0.0, 1 - d) ** 2
    up = np.array([0.18, -1.0])
    def pos(u, v): return flat(u, v) + up * lift * f(u, v)
    # shadow: flat footprint + extra soft shadow under the lifted area
    sm = Image.new('L', (W, H), 0); dr = ImageDraw.Draw(sm)
    outline = [tuple(pos(u, 0)) for u in np.linspace(0, 1, N)] + [tuple(pos(1, v)) for v in np.linspace(0, 1, N)] + \
              [tuple(pos(u, 1)) for u in np.linspace(1, 0, N)] + [tuple(pos(0, v)) for v in np.linspace(1, 0, N)]
    fl = [flat(*c) for c in cu]
    dr.polygon([(x + 10, y + 14) for x, y in fl], fill=int(120 * shadow))
    sm = sm.filter(ImageFilter.GaussianBlur(26))
    if lift_corner is not None and lift > 0:
        s2 = Image.new('L', (W, H), 0)
        cx, cy = cu[lift_corner]
        pts = [tuple(flat(cx + (0.5 - cx) * a, cy + (0.5 - cy) * b) + np.array([lift * .35, lift * .25])) for a, b in [(0, 0), (0.8, 0), (0.8, 0.8), (0, 0.8)]]
        ImageDraw.Draw(s2).polygon(pts, fill=int(70 * shadow)); s2 = s2.filter(ImageFilter.GaussianBlur(40))
        sm = Image.fromarray(np.maximum(np.array(sm), np.array(s2)))
    contact = Image.new('L', (W, H), 0); ImageDraw.Draw(contact).polygon([(x + 2, y + 3) for x, y in fl], fill=int(110 * shadow))
    sm = Image.fromarray(np.maximum(np.array(sm), np.array(contact.filter(ImageFilter.GaussianBlur(4)))))
    cv.paste(Image.new('RGB', (W, H), (52, 44, 38)), (0, 0), sm)
    # sheet, cell by cell, onto a layer clipped by the exact outline (2x supersampled for a clean edge)
    layer = Image.new('RGB', (W, H), (240, 238, 234))
    for i in range(N - 1):
        for j in range(N - 1):
            u0, u1 = i / (N - 1), (i + 1) / (N - 1); v0, v1 = j / (N - 1), (j + 1) / (N - 1)
            d = [pos(u0, v0), pos(u1, v0), pos(u1, v1), pos(u0, v1)]
            s = [(u0 * sw, v0 * sh), (u1 * sw, v0 * sh), (u1 * sw, v1 * sh), (u0 * sw, v1 * sh)]
            bx0, by0 = int(min(p[0] for p in d)) - 2, int(min(p[1] for p in d)) - 2
            bx1, by1 = int(max(p[0] for p in d)) + 3, int(max(p[1] for p in d)) + 3
            loc = [(p[0] - bx0, p[1] - by0) for p in d]
            tile = src.transform((bx1 - bx0, by1 - by0), Image.PERSPECTIVE, coeffs(loc, s), Image.BICUBIC)
            k = (f(u0, v0) + f(u1, v1)) / 2          # lifted areas catch a little more light
            if k > 0:
                tile = Image.fromarray(np.clip(np.array(tile).astype(float) * (1 + 0.06 * k) + 6 * k, 0, 255).astype(np.uint8))
            m = Image.new('L', tile.size, 0)
            c = np.mean(loc, axis=0); ImageDraw.Draw(m).polygon([tuple(c + (np.array(p) - c) * 1.06) for p in loc], fill=255)
            layer.paste(tile, (bx0, by0), m)
    def omask(grow):
        m = Image.new('L', (W * 2, H * 2), 0); c = np.mean(outline, axis=0)
        ImageDraw.Draw(m).polygon([tuple(2 * (c + (np.array(p) - c) * (1 + grow))) for p in outline], fill=255)
        return m.resize((W, H), Image.LANCZOS)
    cv.paste(Image.new('RGB', (W, H), (236, 234, 229)), (0, 0), omask(0.0016))   # paper-thin rim
    cv.paste(layer, (0, 0), omask(-0.0004))
    return cv

def pen(cv, x, y, ang, L=620):
    a = math.radians(ang); dx, dy = math.cos(a), math.sin(a); nx, ny = -dy, dx
    sm = Image.new('L', (W, H), 0)
    ImageDraw.Draw(sm).line([(x + 18, y + 24), (x + dx * L + 18, y + dy * L + 24)], fill=150, width=26)
    cv.paste(Image.new('RGB', (W, H), (40, 34, 30)), (0, 0), sm.filter(ImageFilter.GaussianBlur(14)))
    body = Image.new('L', (W, H), 0); d = ImageDraw.Draw(body)
    d.line([(x, y), (x + dx * L, y + dy * L)], fill=255, width=22)
    cv.paste(Image.new('RGB', (W, H), (24, 24, 26)), (0, 0), body)
    d2 = ImageDraw.Draw(cv)
    d2.line([(x + nx * 5, y + ny * 5), (x + dx * L * .97 + nx * 5, y + dy * L * .97 + ny * 5)], fill=(70, 70, 74), width=3)   # highlight
    d2.line([(x + dx * L * .7, y + dy * L * .7), (x + dx * L * .74, y + dy * L * .74)], fill=(150, 150, 155), width=22)        # clip band
    tip = (x - dx * 34, y - dy * 34); d2.polygon([(x + nx * 11, y + ny * 11), (x - nx * 11, y - ny * 11), tip], fill=(30, 30, 32))

def sheets(slug): return [Image.open(os.path.join(ROOT, 'assets', 'img', slug, 'sheets', f)).convert('RGB') for f in sorted(os.listdir(os.path.join(ROOT, 'assets', 'img', slug, 'sheets')))]

def out(im, slug, name): p = os.path.join(ROOT, 'assets', 'img', slug, name); im.save(p, 'JPEG', quality=84, optimize=True, progressive=True); print(p)

def pdx():
    S = sheets('pdx-west')
    # hero: cover on top of the property-highlights sheet, pen at the side; content kept inside the central 16:9 band
    cv = surface(seed=11, light=(0.35, 0.25))
    place(cv, S[1], rect(1300, 820, 1120, -7), shadow=.8)
    place(cv, S[0], rect(1050, 880, 1180, 3.5), lift_corner=2, lift=34)
    pen(cv, 1790, 1160, -58)
    out(cv, 'pdx-west', 'hero.jpg')
    # card: Kress framing, single thin cover with a lifted corner and a second sheet peeking underneath
    k = W / 1024
    cv = surface(seed=3)
    place(cv, S[1], rect(498 * k, 372 * k, 540 * k, 3.0), shadow=.6)
    place(cv, S[0], rect(532 * k, 400 * k, 565 * k, -6.5), lift_corner=2, lift=42)
    out(cv, 'pdx-west', 'card.jpg')
    # printed piece: three inside sheets fanned out
    cv = surface(seed=21, light=(0.5, 0.2))
    place(cv, S[2], rect(700, 930, 1040, -7), shadow=.8)
    place(cv, S[7], rect(1610, 930, 1040, 7), shadow=.8)
    place(cv, S[4], rect(1155, 870, 1180, 1.5), lift_corner=2, lift=30)
    out(cv, 'pdx-west', 'mock_spread.jpg')

if __name__ == '__main__': pdx()
