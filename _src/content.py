"""All site content in one place. Edit here, then run `python3 _src/build.py`.

Convention: text wrapped in [[ ]] is a placeholder or unconfirmed — Lauren must confirm or rewrite it.
Remove the brackets only once the copy is approved. The build renders [[ ]] in a muted colour.
"""
from brand_copy import BRAND_COPY

SITE_NAME = 'Lauren Gonzalez'
NAV_SUB = 'Senior Graphic Designer'
EMAIL = 'laurenelysegonzalez@gmail.com'
LINKEDIN = 'https://linkedin.com/in/laurenelysegonzalez/'

# ---------- HOME (approved copy, Home-Page-Copy.docx v2 Nov 17 2026 + Rodrigo's edits) ----------
HOME = dict(
    role='/ Graphic Designer',
    role_place='Colliers — Portland',
    hero='Senior graphic designer turning commercial real estate strategy into marketing that wins listings.',
    intro='Hello to you, I am Lauren Elyse Gonzalez. 16 years of experience crafting strategic brand campaigns, packaging, and marketing assets that drive business growth.',
    re_intro='Leasing brochures, offering memorandums, branding, and digital marketing for commercial real estate — strategy and execution, from first concept to launch.',
    re_note='Mockups use the original page artwork. Confidential deal data (pricing, income, rent rolls, fees, tenants) is excluded or blurred.',
    approach_label='[[Approach]]',
    approach='[[Placeholder: Strategy first, then craft — every piece is built to help brokers win the listing and move the deal.]]',
    approach_steps=[('01','Position the asset','[[Placeholder: Translate the broker’s story — location, building, audience — into one clear message.]]'),
                    ('02','Design the package','[[Placeholder: Flyers, brochures and investor offering packages built on a consistent, sharp system.]]'),
                    ('03','Launch everywhere','[[Placeholder: Carry the listing across email, web, signage and presentation decks.]]')],
    interactive_title='Interactive Presentations',
    interactive_intro='[[Placeholder: Click-through Ceros pitch experiences built for Colliers listing presentations — branding, positioning and marketing concepts for the building.]]',
    brand_intro='These featured projects showcase a selection of clients, where I had the opportunity to bring their brand personalities to life, helping them connect with their target audience.',
    testimonial=('Lauren stands at the top of my list for a reliable, responsive, high quality, thoughtful, efficient, and strategic designer. The quality of her work is absolutely impeccable.','Taylor W.','VP Marketing, ClimbOn'),
)
EXPERTISE = ['Brand Identity','Packaging','Brand Strategy','Digital Design','Illustration','Marketing']
CONTACT_LINE = 'If you’re interested in learning more about my services, discussing a potential project, or just want to chat about design and creativity, I’m here to listen.'

TESTIMONIALS = [
 ('Aaron C.','CEO + Co-Founder, Zulay Kitchen','Lauren creates beauty and professionalism with simple touches that go a long way. I’ve never accepted a completed design from Lauren that I did not like because she would never allow it! I highly recommend to have Lauren work on packaging or branding for you as they always do a great job.'),
 ('Patrick O.','Founder, Farm & Bee','We generated more early sales than we expected. She really took the time to understand the essence of our business. Lauren helped us establish a brand identity that instantly communicated the values and quality of our product.'),
 ('Tiffany G.','Founder, Abundant Earth','Lauren not only understood the design aesthetic I was after, but more importantly, the emotion and feeling I wanted our designs to evoke. She is excellent at her craft, efficient, flexible, and a wonderful communicator. Lauren gave me the gift of feeling aligned with my branding for the first time in years.'),
 ('Taylor W.','VP Marketing, ClimbOn','I have worked with dozens of designers and design agencies during my career in consumer goods marketing, and Lauren stands at the top of my list for a reliable, responsive, high quality, thoughtful, efficient, and strategic designer. The quality of her work is absolutely impeccable. She goes above and beyond with thoroughness in the project deliverables and files.'),
 ('Laurie R.','Program Manager, UCLA','We had a great experience working with Lauren. Not only is she very attuned to what the client wants, but she’s also very detailed and patient. She chose all the photos for our manual and took the time to make sure that all the visuals matched the mission of our work. We were on a deadline and she delivered before! I won’t hesitate to call her again next time we need a design specialist.'),
]
STUDENTS = [
 ('Parker Stewart','Student','Because of her program, now my business is flourishing. I have a full-fledged agency. The opportunities we have gotten are out of this world, we have a steady stream of clients, but nothing of what I’m doing or what I’ve learned could have come to life if it weren’t for Lauren.'),
 ('Samantha & Danielle Glassman','Students','Starting a business can be intimidating, but with Lauren’s guidance, we gained the confidence and support we needed to succeed. Thanks to Lauren’s mentorship, we’ve been able to land new clients, refine our niche, and create a strong social media presence that attracts leads.'),
 ('Donald Thomas','Student','I started her How To Graphic Design Course a few months back and I’ve learned so much. I’m much more confident about my work and my skillset. Lauren really over-delivers. I can’t recommend her highly enough.'),
]
ABOUT = dict(
    lead='As a Senior Graphic Designer with 16 years of experience, I have had the opportunity to craft strategic brand campaigns, packaging, and marketing assets that drive business growth primarily in the e-commerce and retail industries.',
    body='I specialize in brand identity design, brand strategy, packaging, surface pattern design, and creative direction, collaborating with teams to develop compelling visuals.',
    colliers='[[Placeholder: A line on Lauren’s current role at Colliers — confirm wording with Lauren.]]',
    educator='In the process of creating and growing my own design business, I witnessed how many new designers struggled—not just with the business side, but also with the fundamentals of graphic design and branding. This inspired me to create 4 The Creatives, a platform dedicated to teaching essential design skills, brand identity, and the tools needed to grow a successful career. Through courses, workshops, and mentorship, I have had the opportunity to help thousands of creatives build confidence in both their work and their future.',
)

# ---------- PROJECTS ----------
# cat: 're' | 'interactive' | 'brand'.  Images live in assets/img/<slug>/ :
#   hero.jpg (mockup / lead image), card.jpg (optional, falls back to hero.jpg), p01.. (document pages), g01.. (gallery), s01.. (screens)
RE_PH = dict(
    project='[[Placeholder: One or two sentences on the property, the client team and what the piece had to do.]]',
    solution=['[[Placeholder: The design approach — layout system, typography, photography and how the story is structured.]]',
              '[[Placeholder: The deliverables — print, digital, signage — and how the system carries across them.]]'],
    results='[[Placeholder: Outcome to be confirmed by Lauren / Colliers — do not invent metrics.]]',
)
def re_proj(slug, title, typ, place, year, summary, home=True, pages_title='The pages', pages_intro='Selected pages from the piece.'):
    return dict(slug=slug, title=title, cat='re', type=typ, place=place, year=year, client='Colliers <span class="muted">[[team — confirm]]</span>',
                role='[[Lauren to confirm]]', summary=summary, home=home, pages_title=pages_title, pages_intro=pages_intro, **RE_PH)

PROJECTS = [
 dict(re_proj('pdx-west','PDX West Logistics Center','Digital Leasing Brochure','Portland, OR','2026','A digital leasing brochure for a 938,000 SF Class A distribution building on Portland’s Airport Way.'),
      project='PDX West Logistics Center is a planned 938,000 SF Class A, cross-loaded distribution building at NE Marine Drive and NE 33rd Drive — Airport Way’s largest available Class A industrial space, half a mile from Portland International Airport, breaking ground in spring 2027. Colliers and developer Capstone Partners needed a digital leasing brochure that could sell a building still on the drawing board to logistics and distribution tenants and the brokers who represent them: make the scale and specifications legible at a glance, prove the location, and look as considered as the Class A product it describes.',
      solution=['A landscape digital brochure built on architectural renderings and aerial photography, cut through with oversized, translucent sage-green triangles and anchored by a heavy, wide all-caps display face for the PDX West wordmark and section titles. A restrained palette of sage, slate and white keeps ten information-dense pages calm and recognisably one family.',
                'The story moves from the building outward: property highlights set out as a two-column specification sheet under a single headline claim, then the site plan, corporate neighbors, the Airport Way submarket, a location map, the regional logistics hubs, workforce statistics and a West Coast drive-time map. Each page pairs one strong image or map with one tight block of facts, so a broker can find clear height, dock doors, trailer stalls or drive distances in seconds.']),
 dict(re_proj('kress-building','Kress Building','Digital Leasing Brochure','Portland, OR','2026','A digital leasing brochure for a fully modernized historic landmark in the heart of downtown Portland.'),
      project='The Kress Building at 630 SW 5th Avenue is a fully modernized historic landmark in the heart of downtown Portland’s retail and business core, with Nike and Sephora anchoring its ground floor. Colliers needed a digital leasing brochure to bring 20,300 SF of office space across the second and third floors — including a 10,000 SF spec suite under construction — to tenants and the brokers who represent them, and to make the case that a landmark can work like new: upgraded building systems, an excellent window line, a well-capitalized local owner and one of the city’s best-connected addresses.',
      solution=['A landscape brochure in deep Kress green and warm parchment, with a single rust-orange accent kept for the message brokers must not miss. Cinzel’s inscriptional capitals give the headlines the presence of a landmark, Proxima Nova keeps every fact clean and modern, and a line-drawn rosette medallion — repeated large and tonal behind the cover — carries the identity from the first page to the last.',
                'The pages read the way a tenant tours: the cover leads with three reasons to call — one block from the future James Beard Market, a well-capitalized local ownership group, a 10,000 SF spec suite under construction — then “A Landmark Redefined” sets out the renovation and the availability, a full-bleed street view declares “Where Business Moves”, two numbered maps prove the neighborhood and the parking, and floor plans for both floors plus a designed spec-suite layout close the case.']),
 dict(slug='nomad', title='Nomad', cat='re', type='Investor Offering Package', place='Overlook, North Portland, OR', year='2026', home=True,
      client='Colliers <span class="muted">[[team — confirm]]</span>', role='[[Lauren to confirm]]',
      summary='[[An investor offering package that sells a North Portland apartment community through bold colour, editorial photography and clear market storytelling.]]',
      project='Nomad is an apartment community in North Portland’s Overlook neighborhood, brought to market by Colliers as an investment sale. The offering package had to give institutional and private investors a fast, credible read on the property, the neighborhood and the Portland market — and make the opportunity stand out in a crowded deal pipeline.',
      solution=['A landscape document organized into five numbered chapters — Investment Summary, Property Description, Market Overview, The Comparables and The Financials. Each chapter opens on a full-bleed photograph washed in a red-to-yellow colour gradient, with a charcoal chapter tab and an oversized italic numeral.',
                'A tight system carries every page: heavy italic display type and orange headlines in outlined title boxes, a four-colour palette of signal red, orange, sun yellow and charcoal, diagonal hatch accents, a consistent icon set, a custom site plan, neighborhood and access maps, and charts drawn in the same palette so market data reads at a glance.'],
      results='[[Placeholder: outcome — launch, investor interest, tours or sale — to be confirmed by Lauren / Colliers. The document itself states no results.]]',
      draft_note='[[Draft copy written from the document — Lauren to review]]'),
 dict(re_proj('the-grid','The Grid (Kirkland 405)','Naming & Brand Identity','Kirkland, WA','2025','A name and identity for a Kirkland office building, repositioned for the region’s innovation economy.'),
      project='Kirkland 405 is an office building in Kirkland, Washington, being repositioned to attract dynamic, innovation-focused tenants from the region’s growing ecosystem of AI, healthcare and creative technology companies. The Colliers team needed a name and an identity to lead that story — one that would feel modern, connected and tech-driven, and tie the building to the broader Kirkland and Seattle innovation story.',
      solution=['A naming study that developed three names — The Grid, Stage One and The Pulse — all the way to a logo, each with its own mark, five key messages, the reasoning behind the name, and the mark shown in place on an exterior blade sign and a lobby feature wall. Every route shares one restrained presentation system, a single cool grey on warm stone with light Open Sans, so the client compares ideas, not styling.',
                'The Grid is a nod to both the tech infrastructure that powers innovation and the urban connectivity of Seattle. Its mark pairs two offset, open square frames — a plan of connected space — with a light geometric wordmark whose open letters echo the gaps in the frames. Drawn as simple line work, it translates directly into dimensional letters, reverses cleanly onto dark panels, and reduces to the two frames alone.'],
      results='The client chose The Grid as the building’s name and logo. In their feedback it stood out immediately as modern, connected and tech-driven — the right direction for repositioning the property for innovation-focused tenants — and they called the full set of concepts a strong creative foundation for telling the building’s story.'),
 re_proj('pacific-center','Pacific Center','Leasing Brochure','Portland, OR','2026','[[Placeholder: A leasing brochure for a downtown Portland office tower.]]'),
 dict(re_proj('leftbank','The Leftbank Project','Digital Leasing Brochure','Portland, OR','2026','A digital leasing brochure for a historic creative-office block in the heart of Albina.'),
      project='The Leftbank Building at 240 N Broadway is a 1923 A.E. Doyle design and one of only three remaining original buildings from Portland’s Albina neighborhood — a former warehouse whose nearly 100-year history runs through hospitality, manufacturing and music, including the Dude Ranch jazz club. Colliers needed a digital leasing brochure to market office and creative spaces from 500 to 6,500+ SF to tenants and their brokers: lead with the character of a seismically retrofitted landmark, and show a neighborhood on the rise.',
      solution=['A landscape brochure that lets the building’s own materials carry it: brick, timber, vaulted ceilings and oversized windows in full-bleed photography, framed by black panels and a burnt-orange accent drawn from the brick. Corsario’s warm serif headlines give it a sense of history, Open Sans keeps the details plain, and a row of simple line icons turns the six key amenities — seismic retrofit, the warehouse-to-office conversion, an on-site café, Energy Star certification, the ceilings and windows, and transit, bike and parking access — into a scannable strip.',
                'The pages move from the building outward: the cover and its amenity strip, the history spread, the spaces, a local-amenities map with bike and transit scores of 95 and 81, then an aerial of Lower Albina that maps the revitalization around the block — Albina Vision Trust, the I-5 Rose Quarter project, the Moda Center renovation and Lloyd Center redevelopment — before closing on the street view and the leasing team.']),
 re_proj('madison-plaza','Madison Plaza','Investor Offering Package','Kent, WA','2026','An investor offering package for a 157-unit apartment community next to Kent Station.'),
 re_proj('redmond-gateway','Redmond Gateway','Investor Offering Package','Redmond, WA','2026','[[Placeholder: An offering memorandum for a two-parcel development site in downtown Redmond.]]'),
 dict(re_proj('springwood','Springwood of Beaverton','Digital Offering Memorandum','Beaverton, OR','2026','A digital offering memorandum for a 55+ manufactured-home community in Beaverton.'),
      project='Springwood of Beaverton is an age-restricted (55+) manufactured-home community on 14.57 acres in Washington County: 74 multi-section homes and one apartment attached to the clubhouse, 100% occupied and made up entirely of tenant-owned homes. Colliers was taking it to market through a call for offers, and needed an offering memorandum that would give investors the full picture — the asset, its value-add story and its location near some of Oregon’s largest employers — in a document as orderly as the community itself.',
      solution=['A landscape memorandum in charcoal, deep teal and white, with aerial photography of the community and a vintage-style Springwood badge that carries from the cover to the back page. Arboria’s rounded geometric headlines and light numerals keep a data-heavy document open and approachable, and fine diagonal hatching adds texture to the cover.',
                'The document is organized into five numbered sections — Executive Summary, Property Overview, Financial Overview, Market Comparables and Location Overview — each opening on a full-bleed teal divider over the aerial. Property highlights become a grid of icons, the details read as a clean spec table, and a site plan, photo spreads of the homes and clubhouse, an annotated aerial and the MSA, employment and Oregon rent-control pages build the investment case.']),
 re_proj('pointe-at-bridgeport','The Pointe at Bridgeport','Leasing Flyer','Tualatin, OR','2026','[[Placeholder: A leasing flyer for office space above retail at Bridgeport Village.]]'),
 re_proj('portland-office-market-report','Portland Office Market Report Q1 2026','Market Report','Portland, OR','2026','[[Placeholder: Design of Colliers’ quarterly Portland office market report.]]',
         pages_intro='Cover and contents. The data pages are left out of this portfolio [[— confirm whether the published report can be shown in full]].'),
]
fc=BRAND_COPY['fortis-net-lease']
PROJECTS.append(dict(slug='fortis-net-lease', title='Fortis Net Lease', cat='re', type='Marketing Design', place='[[National]]', year=fc['year'], home=False,
     client=fc['client'], industry=fc['industry'], service=fc['service'], role=None,
     summary=fc['project'], project=fc['project'], solution=fc['solution'], results=' '.join(fc['results']), gallery_title='Selected work'))

# Nov 23 (Rodrigo): removed from the site. Entries kept above as source; not published (no page, card, nav or Next link).
UNPUBLISHED = {'redmond-gateway', 'portland-office-market-report'}
PROJECTS = [p for p in PROJECTS if p['slug'] not in UNPUBLISHED]

CEROS = [
 dict(slug='big-pink', title='Big Pink', cat='interactive', type='[[Interactive Pitch]]', place='Portland, OR', year='[[Year]]', tool='Ceros',
      summary='[[Placeholder: A click-through Ceros pitch for the U.S. Bancorp Tower (“Big Pink”) — the building, amenity additions, activation concepts, a sample re-naming and a marketing approach.]]'),
 dict(slug='marketplace', title='Marketplace I & II', cat='interactive', type='[[Interactive Pitch]]', place='[[City]]', year='[[Year]]', tool='Ceros',
      summary='[[Placeholder: A click-through Ceros pitch presentation for Marketplace I & II — introductions, market overview, competition, case studies and approach.]]'),
]
for c in CEROS:
    c.update(client='Colliers <span class="muted">[[team — confirm]]</span>', role='[[Lauren to confirm]]',
             project='[[Placeholder: What the pitch had to do and who it was for.]]',
             solution=['[[Placeholder: How the interactive deck is structured and designed.]]'],
             results='[[Placeholder: Outcome to be confirmed by Lauren / Colliers.]]',
             note='Selected design screens only. Market data, fee details, team and client information are left out. [[The live presentation is not linked — confirm with Colliers before sharing it.]]')

BRAND_ORDER = [('aafayaa','Aafayaa'),('abundant-earth','Abundant Earth'),('wild-naturals','Wild Naturals'),('toksuite','TokSuite'),('farm-bee','Farm & Bee'),('zulay','Zulay Kitchen'),('cgk','CGK Unlimited')]
BRAND = []
for slug,title in BRAND_ORDER:
    c=BRAND_COPY[slug]
    BRAND.append(dict(slug=slug,title=title,cat='brand',type=c['service'],place=c['industry'],year=c['year'],client=c['client'],industry=c['industry'],
                      service=c['service'],role=None,summary=c['project'],project=c['project'],solution=c['solution'],results=' '.join(c['results']),
                      home=slug in ('aafayaa','abundant-earth','wild-naturals'),gallery_title='Selected work'))

ALL = PROJECTS + CEROS + BRAND   # case-page order (also drives "Next project")
