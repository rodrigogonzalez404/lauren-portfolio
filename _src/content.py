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
    re_note='Mockups use the original page artwork. Confidential deal data (pricing, income, rent rolls, fees) is excluded or blurred.',
    approach_label='[Approach]',
    approach='Strategy first, then craft — every piece is built to help brokers win the listing and move the deal.',
    approach_steps=[('01','Position the asset','I start with the broker’s story — the building, the location, the audience — and turn it into one clear message before a single page is designed.'),
                    ('02','Design the package','Brochures, flyers and offering memorandums built on one sharp, consistent system, so dense facts read at a glance and every page feels like the same building.'),
                    ('03','Launch everywhere','The identity then travels with the listing — from print to iPad, email, web, signage and pitch presentations — so the message lands the same way everywhere.')],
    interactive_title='Interactive Presentations',
    interactive_intro='Click-through Ceros pitch presentations built for Colliers — branding, positioning and marketing concepts for the building.',
    brand_intro='These featured projects showcase a selection of clients, where I had the opportunity to bring their brand personalities to life, helping them connect with their target audience.',
    testimonial=('Lauren stands at the top of my list for a reliable, responsive, high quality, thoughtful, efficient, and strategic designer. The quality of her work is absolutely impeccable.','Taylor W.','VP Marketing, ClimbOn'),
)
EXPERTISE = ['Brand Identity','Packaging','Brand Strategy','Digital Design','Illustration','Marketing']
CONTACT_LINE = 'Open to new opportunities in brand and real estate marketing design. Whether it’s a role, a collaboration or a conversation about design, I’d love to hear from you.'
RESUME_LINE = 'Résumé available on request — just send me a note.'
RESUME_MAILTO = 'mailto:laurenelysegonzalez@gmail.com?subject=R%C3%A9sum%C3%A9%20request'

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
    colliers='',
    educator='In the process of creating and growing my own design business, I witnessed how many new designers struggled—not just with the business side, but also with the fundamentals of graphic design and branding. This inspired me to create 4 The Creatives, a platform dedicated to teaching essential design skills, brand identity, and the tools needed to grow a successful career. Through courses, workshops, and mentorship, I have had the opportunity to help thousands of creatives build confidence in both their work and their future.',
)

# ---------- PROJECTS ----------
# cat: 're' | 'interactive' | 'brand'.  Images live in assets/img/<slug>/ :
#   hero.jpg (mockup / lead image), card.jpg (optional, falls back to hero.jpg), p01.. (document pages), g01.. (gallery), s01.. (screens)
RE_PH = dict(project='', solution=[], results='')   # Nov 23 (t82u): no placeholders; every published RE case sets its own Project/Solution; Results only where sourced (The Grid)
def re_proj(slug, title, typ, place, year, summary, home=True, pages_title='The pages', pages_intro='Selected pages from the piece.'):
    return dict(slug=slug, title=title, cat='re', type=typ, place=place, year=year, client='Colliers',
                role='Graphic Designer', summary=summary, home=home, pages_title=pages_title, pages_intro=pages_intro, **RE_PH)

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
      client='Colliers', role='Graphic Designer',
      summary='An investor offering package that sells a North Portland apartment community through bold colour, editorial photography and clear market storytelling.',
      project='Nomad is an apartment community in North Portland’s Overlook neighborhood, brought to market by Colliers as an investment sale. The offering package had to give institutional and private investors a fast, credible read on the property, the neighborhood and the Portland market — and make the opportunity stand out in a crowded deal pipeline.',
      solution=['A landscape document organized into five numbered chapters — Investment Summary, Property Description, Market Overview, The Comparables and The Financials. Each chapter opens on a full-bleed photograph washed in a red-to-yellow colour gradient, with a charcoal chapter tab and an oversized italic numeral.',
                'A tight system carries every page: heavy italic display type and orange headlines in outlined title boxes, a four-colour palette of signal red, orange, sun yellow and charcoal, diagonal hatch accents, a consistent icon set, a custom site plan, neighborhood and access maps, and charts drawn in the same palette so market data reads at a glance.'],),
 dict(re_proj('the-grid','The Grid (Kirkland 405)','Naming & Brand Identity','Kirkland, WA','2025','A name and identity for a Kirkland office building, repositioned for the region’s innovation economy.'),
      project='Kirkland 405 is an office building in Kirkland, Washington, being repositioned to attract dynamic, innovation-focused tenants from the region’s growing ecosystem of AI, healthcare and creative technology companies. The Colliers team needed a name and an identity to lead that story — one that would feel modern, connected and tech-driven, and tie the building to the broader Kirkland and Seattle innovation story.',
      solution=['A naming study that developed three names — The Grid, Stage One and The Pulse — all the way to a logo, each with its own mark, five key messages, the reasoning behind the name, and the mark shown in place on an exterior blade sign and a lobby feature wall. Every route shares one restrained presentation system, a single cool grey on warm stone with light Open Sans, so the client compares ideas, not styling.',
                'The Grid is a nod to both the tech infrastructure that powers innovation and the urban connectivity of Seattle. Its mark pairs two offset, open square frames — a plan of connected space — with a light geometric wordmark whose open letters echo the gaps in the frames. Drawn as simple line work, it translates directly into dimensional letters, reverses cleanly onto dark panels, and reduces to the two frames alone.'],
      results='The client chose The Grid as the building’s name and logo. In their feedback it stood out immediately as modern, connected and tech-driven — the right direction for repositioning the property for innovation-focused tenants — and they called the full set of concepts a strong creative foundation for telling the building’s story.'),
 dict(re_proj('pacific-center','Pacific Center','Leasing Brochure','Portland, OR','2026','A leasing brochure for a Class A office tower half a block from Pioneer Courthouse Square.'),
      project='Pacific Center at 851 SW Sixth Avenue is a Class A office tower in the heart of downtown Portland’s Central Business District — half a block from Pioneer Courthouse Square, directly on the MAX light rail and bus mall, and owned and managed by Schnitzer Properties. Colliers needed a leasing brochure to market suites from about 1,300 SF to nearly 16,000 SF to tenants and their brokers, and to show a building with the amenities of a modern workplace at one of the city’s most connected addresses.',
      solution=['A tall-format brochure in deep navy with warm taupe panels: light, widely spaced Gotham capitals for the headlines, Adobe Caslon for the text, and a slim vertical folio running down each page edge. Photography leads every spread — the tower, the atrium lobby, the new employee lounge, the fitness center — framed by navy margins so the building always reads first.',
                'The spreads move from the building to the street: the cover and the downtown story, the amenities, the highlights in a grid of line icons, then the neighborhood — walk, transit and bike scores of 99, 97 and 94 over a map of restaurants, shops and culture — before the availabilities, a sample floor plan with a spec furniture layout, and the leasing team on the back cover.']),
 dict(re_proj('leftbank','The Leftbank Project','Digital Leasing Brochure','Portland, OR','2026','A digital leasing brochure for a historic creative-office block in the heart of Albina.'),
      project='The Leftbank Building at 240 N Broadway is a 1923 A.E. Doyle design and one of only three remaining original buildings from Portland’s Albina neighborhood — a former warehouse whose nearly 100-year history runs through hospitality, manufacturing and music, including the Dude Ranch jazz club. Colliers needed a digital leasing brochure to market office and creative spaces from 500 to 6,500+ SF to tenants and their brokers: lead with the character of a seismically retrofitted landmark, and show a neighborhood on the rise.',
      solution=['A landscape brochure that lets the building’s own materials carry it: brick, timber, vaulted ceilings and oversized windows in full-bleed photography, framed by black panels and a burnt-orange accent drawn from the brick. Corsario’s warm serif headlines give it a sense of history, Open Sans keeps the details plain, and a row of simple line icons turns the six key amenities — seismic retrofit, the warehouse-to-office conversion, an on-site café, Energy Star certification, the ceilings and windows, and transit, bike and parking access — into a scannable strip.',
                'The pages move from the building outward: the cover and its amenity strip, the history spread, the spaces, a local-amenities map with bike and transit scores of 95 and 81, then an aerial of Lower Albina that maps the revitalization around the block — Albina Vision Trust, the I-5 Rose Quarter project, the Moda Center renovation and Lloyd Center redevelopment — before closing on the street view and the leasing team.']),
 dict(re_proj('madison-plaza','Madison Plaza','Investor Offering Package','Kent, WA','2026','An investor offering package for a 157-unit apartment community next to Kent Station.'),
      project='Madison Plaza is a 157-unit apartment community built in 2022 at 102 Madison Avenue in downtown Kent, Washington, with ground-floor retail and the Kent Sounder Station next door. Colliers’ Capital Markets Group was bringing it to market as a core-plus investment and needed an offering memorandum that would make the case for its embedded revenue upside — transit access, a growing South King County economy and a renter base drawn to downtown Kent.',
      solution=['A landscape memorandum in raspberry and plum charcoal on white, set entirely in Montserrat — thin, wide capitals for the headlines with the key words picked out in bold raspberry — and led by bright photography of the new building and its interiors. A numbered contents spread sets up four sections: Executive Summary, The Property, The Financials and The Market.',
                'A consistent system keeps a data-heavy document readable: a clean offering-summary table, maps that place the property between Seattle, the airport and the Kent Valley industrial core, transit and connectivity tables, oversized figures for the region’s growth and its renters, and “The Kent Advantage”, which sets each fact beside what it means and why it matters.']),
 re_proj('redmond-gateway','Redmond Gateway','Investor Offering Package','Redmond, WA','2026','[[Placeholder: An offering memorandum for a two-parcel development site in downtown Redmond.]]'),
 dict(re_proj('springwood','Springwood of Beaverton','Digital Offering Memorandum','Beaverton, OR','2026','A digital offering memorandum for a 55+ manufactured-home community in Beaverton.'),
      project='Springwood of Beaverton is an age-restricted (55+) manufactured-home community on 14.57 acres in Washington County: 74 multi-section homes and one apartment attached to the clubhouse, 100% occupied and made up entirely of tenant-owned homes. Colliers was taking it to market through a call for offers, and needed an offering memorandum that would give investors the full picture — the asset, its value-add story and its location near some of Oregon’s largest employers — in a document as orderly as the community itself.',
      solution=['A landscape memorandum in charcoal, deep teal and white, with aerial photography of the community and a vintage-style Springwood badge that carries from the cover to the back page. Arboria’s rounded geometric headlines and light numerals keep a data-heavy document open and approachable, and fine diagonal hatching adds texture to the cover.',
                'The document is organized into five numbered sections — Executive Summary, Property Overview, Financial Overview, Market Comparables and Location Overview — each opening on a full-bleed teal divider over the aerial. Property highlights become a grid of icons, the details read as a clean spec table, and a site plan, photo spreads of the homes and clubhouse, an annotated aerial and the MSA, employment and Oregon rent-control pages build the investment case.']),
 re_proj('pointe-at-bridgeport','The Pointe at Bridgeport','Leasing Flyer','Tualatin, OR','2026','[[Placeholder: A leasing flyer for office space above retail at Bridgeport Village.]]'),
 re_proj('portland-office-market-report','Portland Office Market Report Q1 2026','Market Report','Portland, OR','2026','[[Placeholder: Design of Colliers’ quarterly Portland office market report.]]',
         pages_intro='Cover and contents. The data pages are left out of this portfolio [[— confirm whether the published report can be shown in full]].'),
]
PROJECTS.append(dict(re_proj('mauzey-court','8210 Mauzey Court','Digital Offering Memorandum','Hillsboro, OR','2026','A digital offering memorandum for a fully leased flex/industrial building in Hillsboro’s tech corridor.'),
      project='8210 Mauzey Court is a 20,000 SF flex/industrial building in Hillsboro, Oregon, 100% leased to True Terpenes — a flavor and terpene manufacturer whose 2021 buildout added high-end offices, production areas, clean rooms and a fully climate-controlled warehouse. Colliers was bringing it to market as an investment sale and needed an offering memorandum that would show investors a turnkey, mission-critical asset in one of the region’s strongest tech submarkets, home to Intel, Tokyo Electron and ASML.',
      solution=['A landscape memorandum in deep teal and seafoam, with Rift’s tall, condensed capitals for the headlines and Proxima Nova for the text. Full-bleed aerials and interior photography sit beside solid colour panels, while small dot grids, thin rules and outlined circles give the pages a precise, technical rhythm that suits a clean-room manufacturer.',
                'The document reads the way an investor works through a deal: the executive summary and property overview, six investment highlights with line icons, the tenant and the lease, a photo tour of the offices, production floor and warehouse, then the market — Portland and Washington County industrial data charted in the same palette — demographics, and three maps that prove regional, national and local access, before closing on the building and the brokers.']))
fc=BRAND_COPY['fortis-net-lease']
PROJECTS.append(dict(slug='fortis-net-lease', title='Fortis Net Lease', cat='re', type='Marketing Design', place='', year=fc['year'], home=False,
     client=fc['client'], industry=fc['industry'], service=fc['service'], role=None,
     summary=fc['project'], project=fc['project'], solution=fc['solution'], results=' '.join(fc['results']), gallery_title='Selected work'))

# Nov 23 (Rodrigo): removed from the site. Entries kept above as source; not published (no page, card, nav or Next link).
UNPUBLISHED = {'redmond-gateway', 'portland-office-market-report', 'marketplace', 'pointe-at-bridgeport'}   # pointe: replaced by Mauzey Court Nov 23 (Rodrigo t82u)
#   # marketplace: removed Nov 23 PM (Rodrigo t78u)
PROJECTS = [p for p in PROJECTS if p['slug'] not in UNPUBLISHED]

CEROS = [
 dict(slug='big-pink', title='Big Pink', cat='interactive', type='Pitch Presentation & Brand Concepts', place='Portland, OR', year='2025', tool='Ceros',
      summary='A Ceros pitch for Big Pink, the U.S. Bancorp Tower, and the identity it proposed — OnePink, from the logo to sample marketing material.'),
 dict(slug='marketplace', title='Marketplace I & II', cat='interactive', type='[[Interactive Pitch]]', place='Portland, OR', year='2026', tool='Ceros',
      summary='[[Placeholder: A click-through Ceros pitch presentation for Marketplace I & II — introductions, market overview, competition, case studies and approach.]]'),
]
for c in CEROS:
    c.update(client='Colliers <span class="muted">[[team — confirm]]</span>', role='[[Lauren to confirm]]',
             project='[[Placeholder: What the pitch had to do and who it was for.]]',
             solution=['[[Placeholder: How the interactive deck is structured and designed.]]'],
             results='[[Placeholder: Outcome to be confirmed by Lauren / Colliers.]]',
             note='Selected design screens only. Market data, fee details, team and client information are left out.')

BRAND_ORDER = [('aafayaa','Aafayaa'),('abundant-earth','Abundant Earth'),('wild-naturals','Wild Naturals'),('toksuite','TokSuite'),('farm-bee','Farm & Bee'),('zulay','Zulay Kitchen'),('cgk','CGK Unlimited')]
BRAND = []
for slug,title in BRAND_ORDER:
    c=BRAND_COPY[slug]
    BRAND.append(dict(slug=slug,title=title,cat='brand',type=c['service'],place=c['industry'],year=c['year'],client=c['client'],industry=c['industry'],
                      service=c['service'],role=None,summary=c['project'],project=c['project'],solution=c['solution'],results=' '.join(c['results']),
                      home=slug in ('aafayaa','abundant-earth','wild-naturals'),gallery_title='Selected work'))

CEROS = [c for c in CEROS if c['slug'] not in UNPUBLISHED]
ALL = PROJECTS + CEROS + BRAND   # case-page order (also drives "Next project")

# Big Pink copy (Nov 23; leads with OnePink — never say the client chose it; Colliers did not win, so no Results) — written from the Ceros presentation and Lauren's logo-concepts deck
for _p in PROJECTS: _p.setdefault('results', '')   # Results only where sourced (t82u)
for c in CEROS:
    if c['slug'] == 'big-pink':
        c.update(project='Big Pink — the U.S. Bancorp Tower at 111 SW 5th Avenue, “the icon of downtown Portland” — had a new owner, who called owning it “deeply meaningful” and “also a responsibility.” Colliers pitched to lead the building’s leasing and marketing with an interactive presentation that had to show the tower “seen from a new angle”: its story, the market and the competition, and a marketing approach bold enough to reposition a landmark — down to a possible new name.',
                 solution=['The proposed identity, OnePink, joins the address and the nickname in one word. Wide-set, rounded capitals run vertically like the tower — ONE in white, PINK in rose on deep navy — with a four-colour palette chosen for what each colour says about the building and a tagline, “One City. One Workplace. One Big Experience.” It is carried through sample marketing material: a brochure, a flyer, a tablet and a phone.',
                           'It sits inside an interactive Ceros presentation in eight numbered chapters — Introductions, The Building, The Market, The Competition, Marketing Approach, Fee Proposal, Why Us? and Appendix. Each chapter opens on a deep navy panel with a rose-pink outlined numeral beside full-bleed photography of the tower and the city; a vertical BIG PINK wordmark frames the cover and the close. The marketing approach builds up to the identity through a moodboard, sixteen sample names from standard to unique, and three logo ideas — OneEleven, Big Pink and OnePink — each shown over the skyline, in dimensional letters and on building signage.'],
                 results='',   # Rodrigo, Nov 23: leave Results empty (block hidden) — no outcome claimed
                 role='Designer — the full Ceros presentation, naming and logo concepts', client='Colliers', note='')   # Rodrigo t76u: "Colliers was the team"

import copy_round; copy_round.apply(ALL)   # Nov 24 (t109u): short Project/Solution, no Results, Colliers real estate only
