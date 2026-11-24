"""Madison Plaza (Nov 24, Rodrigo t105u): hero + cards = Rodrigo's own mockup (MacBook + iPhone with the Madison site,
open printed brochure), used as provided. This overrides the earlier 'Madison hero never changes' rule at his request.
hero.jpg = the image as is (1448x1086, own 4:3 frame via build.py HERO_RATIO); card.jpg = 1440x1080 resize;
card-wide.jpg (home 16:9 slot) = the image centred with the plain studio backdrop extended left/right (objects untouched)."""
import os
import numpy as np
from PIL import Image, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, 'assets', 'img', 'madison-plaza')
UPLOAD = '/workspace/uploads/madison-mockup-new.png'

def widen(im, W):
    a = np.asarray(im, np.float32); H, w = a.shape[:2]; pad = (W - w) // 2
    L = a[:, 2:14].mean(1); R = a[:, -14:-2].mean(1)                  # backdrop tone per row at each edge
    L = np.asarray(Image.fromarray(L[:, None].repeat(4, 1).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6)), np.float32)[:, :1]
    R = np.asarray(Image.fromarray(R[:, None].repeat(4, 1).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6)), np.float32)[:, :1]
    rng = np.random.default_rng(5)
    out = np.empty((H, W, 3), np.float32)
    out[:, :pad] = L[:, None, :] if L.ndim == 2 else L
    out[:, pad + w:] = R[:, None, :] if R.ndim == 2 else R
    out[:, pad:pad + w] = a
    grain = rng.normal(0, 1.2, (H, W, 1)); grain[:, pad:pad + w] = 0
    return Image.fromarray(np.clip(out + grain, 0, 255).astype(np.uint8))

def main():
    im = Image.open(UPLOAD).convert('RGB')
    im.save(os.path.join(D, 'hero.jpg'), quality=90, optimize=True, progressive=True)
    im.resize((1440, 1080), Image.LANCZOS).save(os.path.join(D, 'card.jpg'), quality=88, optimize=True, progressive=True)
    w = widen(im, round(im.height * 16 / 9))
    w.resize((2400, 1350), Image.LANCZOS).save(os.path.join(D, 'card-wide.jpg'), quality=88, optimize=True, progressive=True)
    print('madison hero/card/card-wide')
if __name__ == '__main__': main()
