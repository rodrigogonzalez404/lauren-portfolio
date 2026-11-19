# usage: python3 _src/set_hero.py SLUG /path/to/mockup.jpg  -> stores it as the hero override and writes the web-optimised hero.jpg
import sys, shutil, os
sys.path.insert(0, os.path.dirname(__file__))
from images import MOCK, save
from PIL import Image
slug, src = sys.argv[1], sys.argv[2]
shutil.copy(src, MOCK + slug + '_hero-override.jpg')
save(Image.open(src), slug, 'hero.jpg')
print('hero set for', slug)
