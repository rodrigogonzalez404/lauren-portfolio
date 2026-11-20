"""Kress-style card thumbnail: a flyer's front page lying at an angle on warm beige paper, with a soft shadow.
Everything is made here (procedural paper texture, PIL perspective warp). Run: python3 _src/flyer_card.py
Uses the already-blurred sheet 1 (assets/img/<slug>/sheets/s01.jpg) so contact blurs carry into the thumbnail."""
import os, numpy as np
from PIL import Image, ImageFilter, ImageDraw
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 2304, 1728                                   # same size/aspect as the Kress card (kress hero.jpg)
def coeffs(dst, src):
    A, B = [], []
    for (x, y), (u, v) in zip(dst, src):
        A += [[x, y, 1, 0, 0, 0, -u*x, -u*y], [0, 0, 0, x, y, 1, -v*x, -v*y]]; B += [u, v]
    return np.linalg.solve(np.array(A, float), np.array(B, float)).tolist()
def paper(seed=3):
    rng = np.random.default_rng(seed)
    base = np.array([214, 207, 198], float)          # warm light beige, sampled to match the Kress card surface
    n = rng.standard_normal((H, W)) * 6
    fib = np.array(Image.fromarray(rng.standard_normal((H // 3, W // 3)).astype(np.float32)).resize((W, H), Image.BICUBIC)) * 3.5
    blot = np.array(Image.fromarray(rng.standard_normal((H // 240, W // 240)).astype(np.float32)).resize((W, H), Image.BICUBIC)) * 1.5
    v = n + fib + blot
    img = base[None, None, :] + v[..., None] * np.array([1, .98, .95])[None, None, :]
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
    # soft light falloff from top-left
    yy, xx = np.mgrid[0:H, 0:W]; g = 1.03 - 0.07 * ((xx / W) * .5 + (yy / H) * .8)
    return Image.fromarray(np.clip(np.array(im) * g[..., None], 0, 255).astype(np.uint8))
def card(slug):
    src = Image.open(os.path.join(ROOT, 'assets', 'img', slug, 'sheets', 's01.jpg')).convert('RGB')
    sw, sh = src.size
    k = W / 1024
    quad = [(208, 222), (772, 158), (832, 552), (252, 628)]          # TL TR BR BL, ~ Kress framing
    quad = [(520 + (x - 520) * .9, 385 + (y - 385) * .9) for x, y in quad]
    quad = [(x * k, y * k) for x, y in quad]
    bg = paper()
    # shadow
    sh_m = Image.new('L', (W, H), 0); ImageDraw.Draw(sh_m).polygon([(x + 26, y + 34) for x, y in quad], fill=150)
    sh_m = sh_m.filter(ImageFilter.GaussianBlur(34))
    bg.paste(Image.new('RGB', (W, H), (60, 50, 42)), (0, 0), sh_m)
    tight = Image.new('L', (W, H), 0); ImageDraw.Draw(tight).polygon([(x + 6, y + 8) for x, y in quad], fill=120)
    bg.paste(Image.new('RGB', (W, H), (40, 34, 28)), (0, 0), tight.filter(ImageFilter.GaussianBlur(7)))
    # paper thickness (edge on right/bottom)
    edge = [quad[1], (quad[1][0] + 6, quad[1][1] + 7), (quad[2][0] + 6, quad[2][1] + 7), (quad[3][0] + 6, quad[3][1] + 7), quad[3], quad[2]]
    ImageDraw.Draw(bg).polygon(edge, fill=(226, 222, 216))
    # sheet
    warped = src.transform((W, H), Image.PERSPECTIVE, coeffs(quad, [(0, 0), (sw, 0), (sw, sh), (0, sh)]), Image.BICUBIC)
    m = Image.new('L', (W * 2, H * 2), 0); ImageDraw.Draw(m).polygon([(x * 2, y * 2) for x, y in quad], fill=255)
    m = m.resize((W, H), Image.LANCZOS)
    # subtle sheen
    yy, xx = np.mgrid[0:H, 0:W]; sheen = (np.clip(1 - ((xx - W * .35) ** 2 + (yy - H * .25) ** 2) ** .5 / (W * .55), 0, 1) * 14).astype(np.uint8)
    w2 = Image.fromarray(np.clip(np.array(warped).astype(int) + sheen[..., None] - 4, 0, 255).astype(np.uint8))
    bg.paste(w2, (0, 0), m)
    out = os.path.join(ROOT, 'assets', 'img', slug, 'card.jpg')
    bg.save(out, 'JPEG', quality=84, optimize=True, progressive=True); print(out)
if __name__ == '__main__':
    card('pdx-west')
