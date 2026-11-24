"""Nov 24 final round (Rodrigo t106u):
- Madison HOME wide card: his mockup scaled to ~75% inside the 16:9 frame, centred, on the plain studio backdrop
  (breathing room on all sides). Works card + hero (madison_mock.py) unchanged.
- Nomad hero + card = Rodrigo's desk mockup uploads/nomad-desk-mockup-new.png (open Overlook spread + cover on a desk),
  used as provided: hero in its own 4:3 frame (build.py HERO_RATIO), card = 1440x1080 resize. Replaces nomad_book.hero()/card."""
import os
import numpy as np
from PIL import Image, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, 'assets', 'img')
MADISON = '/workspace/uploads/madison-mockup-new.png'
NOMAD = '/workspace/uploads/nomad-desk-mockup-new.png'
SPRINGWOOD = '/workspace/uploads/springwood-mockup-v2.png'   # t108u: cover + Site Plan + Table of Contents on stone (Rodrigo's mockup; replaces springwood-mockup-new.png)

def madison_wide(scale=0.75, W=2400, H=1350):
    im = Image.open(MADISON).convert('RGB')
    h = int(H * scale * 1.02); w = round(im.width * h / im.height)        # mockup content height ~76% of the frame
    sm = im.resize((w, h), Image.LANCZOS)
    a = np.asarray(im, np.float32)
    top = np.median(a[:30].reshape(-1, 3), 0); bot = np.median(a[-12:].reshape(-1, 3), 0)
    t = np.linspace(0, 1, H)[:, None, None]
    yy, xx = np.mgrid[0:H, 0:W]
    vig = 1 - 0.025 * (np.hypot((xx - W / 2) / W, (yy - H / 2) / H) * 2) ** 2   # the backdrop's own soft fall-off
    bg = (top * (1 - t) + bot * t) * vig[..., None] + np.random.default_rng(3).normal(0, 1.0, (H, W, 1))
    cv = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8))
    m = Image.new('L', (w, h), 0); f = 36
    m.paste(255, (f, f, w - f, h - f)); m = m.filter(ImageFilter.GaussianBlur(f / 2))   # feathered edge into the backdrop
    x0 = (W - w) // 2; y0 = (H - h) // 2 + int(H * 0.01)
    cv.paste(sm, (x0, y0), m)
    cv.save(os.path.join(IMG, 'madison-plaza', 'card-wide.jpg'), quality=88, optimize=True, progressive=True)

def nomad():
    im = Image.open(NOMAD).convert('RGB')
    im.save(os.path.join(IMG, 'nomad', 'hero.jpg'), quality=90, optimize=True, progressive=True)
    im.resize((1440, 1080), Image.LANCZOS).save(os.path.join(IMG, 'nomad', 'card.jpg'), quality=88, optimize=True, progressive=True)

def springwood():
    im = Image.open(SPRINGWOOD).convert('RGB')                     # 1448x1086 = 4:3, used as provided
    im.save(os.path.join(IMG, 'springwood', 'hero.jpg'), quality=90, optimize=True, progressive=True)
    im.resize((1440, 1080), Image.LANCZOS).save(os.path.join(IMG, 'springwood', 'card.jpg'), quality=88, optimize=True, progressive=True)

def main():
    madison_wide(); nomad(); springwood(); print('final round: madison card-wide, nomad hero/card')
if __name__ == '__main__': main()
