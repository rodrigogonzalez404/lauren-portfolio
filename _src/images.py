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
 'kress-building':('kress-building','kress-building_brochure.jpg',[(1,[]),(2,[(0.066,0.866,0.175,0.899)]),(3,[]),(4,[]),(5,[]),(6,[]),(7,[(0.066,0.462,0.168,0.499)]),(8,[(0.066,0.462,0.168,0.499)]),(9,[]),(10,[])]),  # Nov 23 iPad viewer: all 10 pages; only the '$28/SF FSG' asking rate is blurred (p2, p7, p8)
 'pdx-west':('pdx-west-flyer',None,[]),  # sheets: _src/flyer_sheets.py; hero, card, mock_spread: _src/flyer_mockups.py
 'the-grid':('kirkland-405-brand',None,[]),  # Nov 23 identity case: all assets from _src/grid/grid_assets.py (hero = vector logo; card = lobby-sign mockup)
 'pacific-center':('pacific-center-flyer','pacific-center_poster.jpg',[]),  # hero = poster mockup; brochure + flip-book: see _src/pacific_book.py (Nov 23)
 'leftbank':('leftbank-flyer','leftbank_flyer.jpg',[]),  # sheets for the stack: see _src/flyer_sheets.py
 'madison-plaza':('madison-plaza-om','madison-plaza_om-cover.jpg',[]),  # page gallery replaced by the Nomad-style book: see _src/madison_book.py
 'redmond-gateway':('redmond-assemblage-om','redmond-gateway_om-stack.jpg',[(1,[]),(2,[]),(6,[(0.035,0.24,0.315,0.43)]),(7,[(0.035,0.24,0.315,0.43)]),(14,[]),(15,[])]),  # parcel text names owners + lease dates -> blurred),
 'springwood':('springwood-om','springwood_om-cover.jpg',[(1,[(0.7854,0.8905,0.9356,0.9265)]),(2,[]),(3,[]),(4,[(0.2172,0.4183,0.3093,0.4461)]),(5,[(0.7576,0.6471,0.9508,0.7565)]),(6,[]),(7,[(0.2462,0.6846,0.3043,0.7141)]),(8,[]),(9,[]),(10,[]),(11,[]),(12,[]),(13,[]),(16,[]),(18,[]),(19,[]),(20,[]),(21,[]),(22,[])]),  # Nov 23 iPad viewer: p01..p19 = PDF 1-13,16,18-22; blurred only: p1 '$1,035 Avg. Rent', p4 lot-rent range, p5 rent-upside paragraph, p7 property tax; PDF 14-15 (financials) + 17 (rent comps) omitted
 'pointe-at-bridgeport':('the-pointe-bridgeport','the-pointe_flyer-stack.jpg',[(1,[]),(2,[]),(3,[]),(4,[]),(7,[]),(8,[])]),
 'portland-office-market-report':('portland-office-report-q1-2026','portland-office-report_laptop.jpg',[(1,[]),(2,[])]),
}
NOMAD_FLIP=['p00_cover.jpg','page-03_L.jpg','page-03_R.jpg','page-07_L.jpg','page-07_R.jpg','page-10_L.jpg','page-10_R.jpg','page-11_L.jpg','page-11_R.jpg','page-12_L.jpg','page-12_R.jpg','page-15_L.jpg','page-15_R.jpg','page-17_L.jpg','page-19_R.jpg','page-22_L.jpg','page-22_R.jpg']
NOMAD_IMG=['n01_hero_spread-investment-summary.jpg','n02_cover-on-desk.jpg','n03_printed-stack.jpg','n06_tablet-neighborhood-map.jpg','n08_detail-supply-chart.jpg']  # Nov 23: design-system crops (ds_*) removed from the page (Rodrigo)
CEROS={'big-pink':['bigpink-%02d'%i for i in (1,2,3,6,7,16,18,19,20,23)],
       'marketplace':['marketplace-%02d'%i for i in (1,2,3,5,9,11,13,15,16)]}
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
    for f in NOMAD_IMG: save(Image.open(RD+'nomad/'+f),'nomad',('hero.jpg' if f.startswith('n01') else f.split('_')[0]+'.jpg') if f.startswith('n') else f)
    for i,f in enumerate(NOMAD_FLIP): save(Image.open(RD+'nomad/flip/'+f),'nomad/flip',f'f{i:02d}.jpg',1600)
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
    import flyer_sheets; flyer_sheets.main()
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'grid')); import grid_assets; grid_assets.main()   # The Grid identity case
    import madison_card; madison_card.main()   # Madison home/works card on the shared cream (hero stays Rodrigo's white original)
    os.makedirs(os.path.join(OUT, 'ui'), exist_ok=True); import flyer_mockups as FM; FM.surface(seed=7, light=(0.5, 0.15)).resize((1600, 1200), Image.LANCZOS).save(os.path.join(OUT, 'ui', 'cream-surface.jpg'), quality=82, optimize=True, progressive=True)   # iPad viewer stage (shared CREAM)
    import runpy; runpy.run_path(os.path.join(os.path.dirname(__file__),'desk_texture.py'))   # ui/desk-charcoal.jpg (OUT is wiped above)
    json.dump(man,open(os.path.join(os.path.dirname(__file__),'image_manifest.json'),'w'),indent=1)
    print('done')
if __name__=='__main__': main()
