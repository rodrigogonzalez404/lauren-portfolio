"""Madison Plaza 'like Nomad' assets: flip-book pages, design-system crops, printed-book images.
Run: python3 _src/madison_book.py   (needs the source page renders on the build box)
Source: Madison Plaza_OM V25-compressed.pdf rendered to pages/madison-plaza-om/page-NN.png
(PDF page 1 = front cover, PDF 2-23 = two-page spreads = printed pages 2-45, PDF 24 = back cover).
Section 03 Financials: PDF 12 is the divider spread (printed pp. 22-23, KEPT); PDF 13-17 (printed pp. 24-33:
unit mix & market rents, tax bill, income & expenses, pro forma, 10-year cash flow, rent comps) are DROPPED and
replaced by a black 'Confidential — financial information omitted' spread (HTML, see build.py).
Blur boxes are fractions of the full PDF page (spread)."""
import os, json
from PIL import Image
from images import PAGES, MOCK, save, blur
F = PAGES + 'madison-plaza-om/'
SLUG = 'madison-plaza'
BLUR = {
    2:  [(0.0, 0.28, 0.24, 0.76)],                                  # broker names, emails, phones
    4:  [(0.695, 0.30, 0.995, 0.92)],                               # offering bullets: price guidance, NOI, lender
    5:  [(0.0, 0.24, 0.355, 0.89)],                                 # operating text: opex, rents, NOI upside
    6:  [(0.0, 0.29, 0.29, 0.84), (0.72, 0.26, 0.995, 0.84)],       # ground-lease rent / MFTE savings
    21: [(0.025, 0.66, 0.092, 0.71)],                                 # 'Clears 3x in-place rent ($1,864/mo …)'
    24: [(0.02, 0.67, 0.62, 0.80)],                                 # back cover broker names, emails, phones
}
BEFORE = list(range(2, 13))     # PDF spreads 2-12  -> printed pp. 2-23 (12 = 03 The Financials divider)
DROPPED = list(range(13, 18))   # PDF 13-17 -> printed pp. 24-33
AFTER = list(range(18, 24))     # PDF spreads 18-23 -> printed pp. 34-45 (18 = 04 The Market divider)

def pg(n):
    im = Image.open(F + f'page-{n:02d}.png').convert('RGB')
    return blur(im, BLUR[n]) if n in BLUR else im

def halves(n):
    im = pg(n); W, H = im.size
    return [im.crop((0, 0, W // 2, H)), im.crop((W // 2, 0, W, H))]

def main():
    out = 'flip'
    seq = [('cover', pg(1))]
    for n in BEFORE:
        a, b = halves(n); seq += [(f'p{2*n-2}', a), (f'p{2*n-1}', b)]
    seq += [('BLACK', None), ('BLACK', None)]
    for n in AFTER:
        a, b = halves(n); seq += [(f'p{2*n-2}', a), (f'p{2*n-1}', b)]
    seq += [('back', pg(24))]
    names = []
    i = 0
    for tag, im in seq:
        if im is None: names.append('BLACK'); continue
        nm = f'f{i:02d}.jpg'; save(im, SLUG + '/flip', nm, 1600); names.append(tag + ':' + nm); i += 1
    # printed book
    save(Image.open(MOCK + 'madison-plaza_om-cover.jpg'), SLUG, 'book_mockup.jpg')
    save(pg(1), SLUG, 'book_cover.jpg', 1600)
    save(pg(24), SLUG, 'book_back.jpg', 1600)
    json.dump(names, open(os.path.join(os.path.dirname(__file__), 'madison_flip.json'), 'w'), indent=1)
    print(len(names), 'book pages', names)

if __name__ == '__main__': main()
