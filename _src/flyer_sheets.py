"""Sheet-stack assets for flyers (Leftbank, PDX West). Run: python3 _src/flyer_sheets.py
Renders the flyer PDF fresh at 200 dpi (landscape letter -> 2200x1700) and saves sheets/s01..s06.jpg (2000px wide).
Leftbank page 7 = broker contacts -> omitted. Sheets 1-6 checked: no rents, prices, contacts or deal figures -> no blurs.
PDX West: pages 1-9 shown (p1 broker strip blurred), page 10 = back cover with broker contacts -> omitted. No pricing anywhere."""
import os, subprocess, tempfile, glob
from PIL import Image
from images import save, blur
FLYERS = {'leftbank': ('/workspace/lauren-case-studies/source/extracted/Leftbank_Flyer.pdf', range(1, 7), {}),
          'pdx-west': ('/workspace/lauren-case-studies/source/extracted/PDXWestFlyer_For Lease.pdf', range(1, 10), {1: [(0.039, 0.843, 0.586, 0.932)]})}  # PDX p10 = broker contacts -> omitted; p1 contacts blurred  # slug: (pdf, pages, {page: blur boxes})
def main():
    for slug, (pdf, pages, boxes) in FLYERS.items():
        with tempfile.TemporaryDirectory() as d:
            subprocess.run(['pdftoppm', '-r', '200', '-png', '-f', str(min(pages)), '-l', str(max(pages)), pdf, d + '/s'], check=True)
            for k, n in enumerate(pages, 1):
                f = [x for x in glob.glob(d + '/s-*.png') if int(x.rsplit('-', 1)[1][:-4]) == n][0]
                im = Image.open(f).convert('RGB')
                if n in boxes: im = blur(im, boxes[n])
                save(im, slug + '/sheets', f's{k:02d}.jpg', 2000)
        print(slug, 'sheets', len(pages))
    import flyer_mockups; flyer_mockups.pdx()   # hero, card + fanned-sheets mockup, all self-made
if __name__ == '__main__': main()
