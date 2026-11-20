"""Self-made dark charcoal desk texture (procedural wood grain) for the flip-book stage. Run: python3 _src/desk_texture.py"""
import numpy as np, os
from PIL import Image, ImageFilter
rng = np.random.default_rng(7)
W, H = 2400, 1400
y = np.arange(H)[:, None].astype(float); x = np.arange(W)[None, :].astype(float)
def smooth_noise(w, h, sx, sy):
    n = rng.standard_normal((h // sy + 2, w // sx + 2))
    return np.array(Image.fromarray(n.astype(np.float32)).resize((w, h), Image.BICUBIC))
warp = smooth_noise(W, H, 300, 120) * 22 + smooth_noise(W, H, 900, 300) * 40
rings = np.sin((y + warp) / 5.5 + smooth_noise(W, H, 600, 40) * 1.6)
streak = smooth_noise(W, H, 1200, 3) * 0.6           # long fine fibres along the grain
fine = rng.standard_normal((H, W)) * 0.35
v = 0.55 * rings + streak + fine
v = (v - v.min()) / (v.max() - v.min())
base = np.array([27, 25, 24], float)                  # warm charcoal, sits between --ink #0F0F0F and --body #29292B
img = base[None, None, :] + (v[..., None] - 0.5) * np.array([11, 10, 9])[None, None, :]
im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'img', 'ui', 'desk-charcoal.jpg')
os.makedirs(os.path.dirname(out), exist_ok=True)
im.save(out, 'JPEG', quality=78, optimize=True, progressive=True); print(out, os.path.getsize(out))
