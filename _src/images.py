"""Prepare web-optimized images for the site.
Run:  python3 _src/images.py      (from the repo root; needs Pillow and the original source folders)
Source folders live OUTSIDE this repo (on the build box). Outputs go to assets/img/<slug>/.
Blur boxes are fractions (x0,y0,x1,y1) of the full source page.
"""
import os, sys, json, shutil
from PIL import Image, ImageFilter
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(ROOT,'assets','img')
PAGES='/workspace/lauren-case-studies/pages/'
MOCK='/workspace/lauren-case-studies/mockups/'
RD='/workspace/redesign/img/'
WF='/workspace/webflow-export/lauren-gonzalez-portfolio/'
MAX=2400; Q=80

def blur(im, boxes):
    im=im.convert('RGB'); W,H=im.size
    for x0,y0,x1,y1 in boxes:
        b=(int(x0*W),int(y0*H),int(x1*W),int(y1*H))
        reg=im.crop(b)
        # pixelate + heavy gaussian so text is unrecoverable
        small=reg.resize((max(1,reg.width//24),max(1,reg.height//24)),Image.BILINEAR)
        reg=small.resize(reg.size,Image.BILINEAR).filter(ImageFilter.GaussianBlur(max(6,reg.height//6)))
        im.paste(reg,b)
    return im

def save(im, slug, name, maxw=MAX):
    os.makedirs(os.path.join(OUT,slug),exist_ok=True)
    im=im.convert('RGB')
    if max(im.size)>maxw:
        r=maxw/max(im.size); im=im.resize((round(im.width*r),round(im.height*r)),Image.LANCZOS)
    p=os.path.join(OUT,slug,name)
    im.save(p,'JPEG',quality=Q,optimize=True,progressive=True)
    return p

def page(folder, n):
    for f in (f'page-{n:02d}.png', f'page-{n}.png'):
        p=PAGES+folder+'/'+f
        if os.path.exists(p): return Image.open(p)
    raise FileNotFoundError(folder+str(n))

# slug: (pdf folder, hero mockup, [(page, blur boxes)])
# Rule (Rodrigo, Nov 23): front-page/cover content (contacts, headlines, addresses, broker strips) is NOT confidential;
# only financial data (pricing, rents, rent comps, operating figures, taxes, deal financials) is blurred or omitted.
RE={
 'kress-building':('kress-building',None,[(i,[]) for i in range(1,11)]),  # Nov 24 (Rodrigo t94u): public record -> nothing blurred (approved exception); hero + card = flyer_mockups.kress(). Before:  # Nov 23 iPad viewer: all 10 pages; only the per-SF asking rate is blurred (p2, p7, p8)
 'pdx-west':('pdx-west-flyer',None,[]),  # sheets: _src/flyer_sheets.py; hero, card, mock_spread: _src/flyer_mockups.py
 'the-grid':('kirkland-405-brand',None,[]),  # Nov 23 identity case: all assets from _src/grid/grid_assets.py (hero = vector logo; card = lobby-sign mockup)
 'pacific-center':('pacific-center-flyer','pacific-center_poster.jpg',[]),  # hero = poster mockup; brochure + flip-book: see _src/pacific_book.py (Nov 23)
 'leftbank':('leftbank-flyer','leftbank_flyer.jpg',[]),  # sheets for the stack: see _src/flyer_sheets.py
 'madison-plaza':('madison-plaza-om','madison-plaza_om-cover.jpg',[]),  # page gallery replaced by the Nomad-style book: see _src/madison_book.py
 'redmond-gateway':('redmond-assemblage-om','redmond-gateway_om-stack.jpg',[(1,[]),(2,[]),(6,[(0.035,0.24,0.315,0.43)]),(7,[(0.035,0.24,0.315,0.43)]),(14,[]),(15,[])]),  # parcel text names owners + lease dates -> blurred),
 'springwood':('springwood-om','springwood_om-cover.jpg',[(1,[]),(2,[]),(3,[]),(4,[]),(5,[]),(6,[]),(7,[]),(8,[]),(9,[]),(10,[]),(11,[]),(12,[]),(13,[]),(16,[]),(18,[]),(19,[]),(20,[]),(21,[]),(22,[])]),  # Nov 24 (t108u): Rodrigo — all blurs removed ('what is confidential is already removed'); p01..p19 = PDF 1-13,16,18-22; PDF 14-15 (financials) + 17 (rent comps) still omitted
 'pointe-at-bridgeport':('the-pointe-bridgeport','the-pointe_flyer-stack.jpg',[(1,[]),(2,[]),(3,[]),(4,[]),(7,[]),(8,[])]),
 'portland-office-market-report':('portland-office-report-q1-2026','portland-office-report_laptop.jpg',[(1,[]),(2,[])]),
}
NOMAD_FLIP=['p00_cover.jpg','page-03_L.jpg','page-03_R.jpg','page-07_L.jpg','page-07_R.jpg','page-10_L.jpg','page-10_R.jpg','page-11_L.jpg','page-11_R.jpg','page-12_L.jpg','page-12_R.jpg','page-15_L.jpg','page-15_R.jpg','page-17_L.jpg','page-19_R.jpg','page-22_L.jpg','page-22_R.jpg']
NOMAD_IMG=['n01_hero_spread-investment-summary.jpg','n02_cover-on-desk.jpg','n03_printed-stack.jpg','n06_tablet-neighborhood-map.jpg','n08_detail-supply-chart.jpg']  # Nov 23: design-system crops (ds_*) removed from the page (Rodrigo)
CEROS={}   # big-pink + marketplace: all assets from _src/bigpink/bp_assets.py (Nov 23 laptop/identity treatment)
# brand galleries: ordered as on the live Webflow case pages (already public there)
DROP={'RealEstate_Examples','8-FNL'}   # Fortis: readable listing prices, cap rates, broker names/phones/emails -> omitted

def main():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    man={}
    from content import UNPUBLISHED   # Redmond Gateway + Portland report: removed Nov 23, images not published
    for slug,(folder,mock,pages) in RE.items():
        if slug in UNPUBLISHED: continue
        ov=MOCK+slug+'_hero-override.jpg'   # mockup supplied by Rodrigo replaces the generated one
        if mock or os.path.exists(ov): save(Image.open(ov if os.path.exists(ov) else MOCK+mock),slug,'hero.jpg')
        names=[]
        for k,spec in enumerate(pages,1):
            n,boxes=spec[0],spec[1]
            im=page(folder,n)
            if boxes: im=blur(im,boxes)
            if len(spec)>2:
                W,H=im.size; c=spec[2]; im=im.crop((int(c[0]*W),int(c[1]*H),int(c[2]*W),int(c[3]*H)))
            nm=f'p{k:02d}.jpg'; save(im,slug,nm); names.append(nm)
        man[slug]=names
    import nomad_surface; nomad_surface.main()   # Nomad scene photos re-surfaced on palette.CREAM from the pre-cream originals
    import nomad_book; nomad_book.main()   # Nov 24 (t97u): hero, printed-book mockups, full flip-book
    for f in []: save(Image.open(RD+'nomad/'+f),'nomad',('hero.jpg' if f.startswith('n01') else f.split('_')[0]+'.jpg') if f.startswith('n') else f)
    for i,f in enumerate([]): save(Image.open(RD+'nomad/flip/'+f),'nomad/flip',f'f{i:02d}.jpg',1600)
    for slug,fs in CEROS.items():
        for i,f in enumerate(fs,1): save(Image.open(RD+'ceros/sel/'+f+'.jpg'),slug,f's{i:02d}.jpg')
        save(Image.open(RD+'ceros/sel/'+fs[0]+'.jpg'),slug,'card.jpg',1600)
        man[slug]=[f's{i:02d}.jpg' for i in range(1,len(fs)+1)]
    seq=json.load(open(os.path.join(os.path.dirname(__file__),'brand_sources.json')))
    for slug,files in seq.items():
        files=[f for f in files if not any(d in f for d in DROP)]
        names=[]
        for i,f in enumerate(files):
            nm='hero.jpg' if i==0 else f'g{i:02d}.jpg'
            save(Image.open(WF+f),slug,nm); names.append(nm)
        man[slug]=names
    CARDS={'aafayaa':'card_aafayaa.jpg','abundant-earth':'card_abundant.jpg','fortis-net-lease':'card_fortis.jpg','toksuite':'card_toksuite.jpg','farm-bee':'card_farmbee.jpg','wild-naturals':'card_wild.jpg','zulay':'card_zulay.jpg','cgk':'card_cgk.jpg'}
    for slug,f in CARDS.items(): save(Image.open(RD+f),slug,'card.jpg',1600)
    # about / misc
    for f in ('about_portrait.jpg','about_educator.jpg'): save(Image.open(RD+f),'about',f.replace('about_',''))
    import madison_book; madison_book.main()
    import pacific_book; pacific_book.main()
    import pacific_mock; pacific_mock.main()   # Nov 24 (t101u): hero + card = Rodrigo's desk mockup (overrides the poster hero)
    import flyer_sheets; flyer_sheets.main()
    import leftbank_round; leftbank_round.main()   # Nov 24 (t102u): shadowed brochure pages + Rodrigo's desk mockup as hero/card (needs the sheets)
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'grid')); import grid_assets; grid_assets.main()   # The Grid identity case
    import madison_card; madison_card.main()
    import madison_mock; madison_mock.main()   # Nov 24 (t105u): Rodrigo's mockup = hero + card + card-wide (overrides madison_card)
    import final_round; final_round.main()     # Nov 24 (t106u): Madison home card with breathing room; Nomad hero/card = Rodrigo's desk mockup (runs after nomad_book)
    # Nomad home/works card (Rodrigo t79u): his cover-on-stone image, used as is — the white screenshot border trimmed,
    # the stone frame (~4:3) kept whole, resized to the card size
    _n = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nomad_card_src.png')).convert('RGB')
    _n = _n.crop((53, 44, 1172, 879)).resize((1440, 1080), Image.LANCZOS)
    _n.save(os.path.join(OUT, 'nomad', 'card.jpg'), quality=90, optimize=True, progressive=True)   # Madison home/works card on the shared cream (hero stays Rodrigo's white original)
    os.makedirs(os.path.join(OUT, 'ui'), exist_ok=True); import flyer_mockups as FM; FM.surface(seed=7, light=(0.5, 0.15)).resize((1600, 1200), Image.LANCZOS).save(os.path.join(OUT, 'ui', 'stone-surface.jpg'), quality=84, optimize=True, progressive=True)   # iPad viewer stage: textured pale stone (t78u)
    import runpy; runpy.run_path(os.path.join(os.path.dirname(__file__),'desk_texture.py'))   # ui/desk-charcoal.jpg (OUT is wiped above)
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'bigpink')); import bp_assets; bp_assets.main()   # Big Pink (OnePink identity + Ceros laptop) and Marketplace
    json.dump(man,open(os.path.join(os.path.dirname(__file__),'image_manifest.json'),'w'),indent=1)
    print('done')
if __name__=='__main__': main()
