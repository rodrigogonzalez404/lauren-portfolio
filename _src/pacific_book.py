"""Pacific Center 'like Nomad / Madison' (Nov 23, Rodrigo): design system (swatches), the printed brochure, flip-book.
Source: /workspace/lauren-case-studies/source/extracted/PacificCenter-Flyer.pdf, 7 PDF pages, all letter-size (612x792).
PDF 1 = front cover, PDF 2-6 = two-page spreads (printed pp. 2-11) that were exported SQUASHED to half width,
PDF 7 = back cover. The spreads are rendered from the vectors at 2x width (pdftoppm -scale-to-x 3400 -scale-to-y 2200)
into /workspace/lauren-case-studies/pages/pacific-center-brochure/, which restores the true 17x11 in proportions.
Confidentiality (Nov 23 rule: only financials): no pricing, rents or operating figures anywhere; availabilities list
suite sizes (SF) only -> every page included, nothing blurred. Back cover broker contacts are shown (not financial)."""
import os, json, glob, subprocess
from PIL import Image
from images import MOCK, save
PDF = '/workspace/lauren-case-studies/source/extracted/PacificCenter-Flyer.pdf'
SRC = '/workspace/lauren-case-studies/pages/pacific-center-brochure/'
SLUG = 'pacific-center'

def render():
    os.makedirs(SRC, exist_ok=True)
    for n in range(1, 8):
        spread = 2 <= n <= 6
        name = SRC + (f'sp-{n}' if spread else f'pg-{n}')
        if glob.glob(name + '*.png'): continue
        subprocess.run(['pdftoppm', '-f', str(n), '-l', str(n), '-png', '-scale-to-x', '3400' if spread else '1700',
                        '-scale-to-y', '2200', PDF, name], check=True)

def pg(stem): return Image.open(glob.glob(SRC + stem + '*.png')[0]).convert('RGB')

def main():
    render()
    seq = [('cover', pg('pg-1'))]
    for n in range(2, 7):
        im = pg(f'sp-{n}'); W, H = im.size
        seq += [(f'p{2*n-2}', im.crop((0, 0, W // 2, H))), (f'p{2*n-1}', im.crop((W // 2, 0, W, H)))]
    seq += [('back', pg('pg-7'))]
    names = []
    for i, (tag, im) in enumerate(seq):
        nm = f'f{i:02d}.jpg'; save(im, SLUG + '/flip', nm, 1200); names.append(tag + ':' + nm)
    # (Nov 24) the open-spread mockup was dropped; book_fan.jpg + hero/card come from pacific_mock.py
    save(pg('pg-1'), SLUG, 'book_cover.jpg', 1600)
    save(pg('pg-7'), SLUG, 'book_back.jpg', 1600)
    json.dump(names, open(os.path.join(os.path.dirname(__file__), 'pacific_flip.json'), 'w'), indent=1)
    print(len(names), 'pacific book pages')

if __name__ == '__main__': main()
