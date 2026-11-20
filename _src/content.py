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
 dict(re_proj('pdx-west','PDX West Logistics Center','Leasing Flyer','Portland, OR','2026','A leasing flyer and site signage for a 938,000 SF Class A distribution building on Portland’s Airport Way.'),
      project='PDX West Logistics Center is a planned 938,000 SF Class A, cross-loaded distribution building at NE Marine Drive and NE 33rd Drive — Airport Way’s largest available Class A industrial space, half a mile from Portland International Airport, breaking ground in spring 2027. Colliers and developer Capstone Partners needed a leasing flyer that could sell a building still on the drawing board to logistics and distribution tenants and the brokers who represent them: make the scale and specifications legible at a glance, prove the location, and look as considered as the Class A product it describes.',
      solution=['A landscape flyer built on architectural renderings and aerial photography, cut through with oversized, translucent sage-green triangles and anchored by a heavy, wide all-caps display face for the PDX West wordmark and section titles. A restrained palette of sage, slate and white keeps ten information-dense pages calm and recognisably one family, and the cover art carries straight onto the site signage, so the building, the flyer and the sign read as one brand.',
                'The story moves from the building outward: property highlights set out as a two-column specification sheet under a single headline claim, then the site plan, corporate neighbors, the Airport Way submarket, a location map, the regional logistics hubs, workforce statistics and a West Coast drive-time map. Each page pairs one strong image or map with one tight block of facts, so a broker can find clear height, dock doors, trailer stalls or drive distances in seconds.']),
 re_proj('kress-building','Kress Building','Leasing Brochure','Portland, OR','2026','[[Placeholder: A leasing brochure for a renovated landmark office building in downtown Portland.]]'),
 dict(slug='nomad', title='Nomad', cat='re', type='Investor Offering Package', place='Overlook, North Portland, OR', year='2026', home=True,
      client='Colliers <span class="muted">[[team — confirm]]</span>', role='[[Lauren to confirm]]',
      summary='[[An investor offering package that sells a North Portland apartment community through bold colour, editorial photography and clear market storytelling.]]',
      project='Nomad is an apartment community in North Portland’s Overlook neighborhood, brought to market by Colliers as an investment sale. The offering package had to give institutional and private investors a fast, credible read on the property, the neighborhood and the Portland market — and make the opportunity stand out in a crowded deal pipeline.',
      solution=['A landscape document organized into five numbered chapters — Investment Summary, Property Description, Market Overview, The Comparables and The Financials. Each chapter opens on a full-bleed photograph washed in a red-to-yellow colour gradient, with a charcoal chapter tab and an oversized italic numeral.',
                'A tight system carries every page: heavy italic display type and orange headlines in outlined title boxes, a four-colour palette of signal red, orange, sun yellow and charcoal, diagonal hatch accents, a consistent icon set, a custom site plan, neighborhood and access maps, and charts drawn in the same palette so market data reads at a glance.'],
      results='[[Placeholder: outcome — launch, investor interest, tours or sale — to be confirmed by Lauren / Colliers. The document itself states no results.]]',
      draft_note='[[Draft copy written from the document — Lauren to review]]'),
 re_proj('the-grid','The Grid (Kirkland 405)','Naming & Identity','Kirkland, WA','2025','[[Placeholder: Name and logo concepts for a Kirkland office building — The Grid, Stage One and The Pulse.]]', pages_title='Name & logo concepts', pages_intro='Three naming routes, each with a mark and key messages, shown in the building.'),
 re_proj('pacific-center','Pacific Center','Leasing Brochure','Portland, OR','2026','[[Placeholder: A leasing brochure for a downtown Portland office tower.]]'),
 re_proj('leftbank','The Leftbank Project','Leasing Flyer','Portland, OR','2026','[[Placeholder: A leasing flyer for a historic creative-office block in Lower Albina.]]'),
 re_proj('madison-plaza','Madison Plaza','Investor Offering Package','Kent, WA','2026','An investor offering package for a 157-unit apartment community next to Kent Station.'),
 re_proj('redmond-gateway','Redmond Gateway','Investor Offering Package','Redmond, WA','2026','[[Placeholder: An offering memorandum for a two-parcel development site in downtown Redmond.]]'),
 re_proj('springwood','Springwood of Beaverton','Investor Offering Package','Beaverton, OR','2026','[[Placeholder: An offering memorandum for a manufactured-home community in Beaverton.]]'),
 re_proj('pointe-at-bridgeport','The Pointe at Bridgeport','Leasing Flyer','Tualatin, OR','2026','[[Placeholder: A leasing flyer for office space above retail at Bridgeport Village.]]'),
 re_proj('portland-office-market-report','Portland Office Market Report Q1 2026','Market Report','Portland, OR','2026','[[Placeholder: Design of Colliers’ quarterly Portland office market report.]]',
         pages_intro='Cover and contents. The data pages are left out of this portfolio [[— confirm whether the published report can be shown in full]].'),
]
fc=BRAND_COPY['fortis-net-lease']
PROJECTS.append(dict(slug='fortis-net-lease', title='Fortis Net Lease', cat='re', type='Marketing Design', place='[[National]]', year=fc['year'], home=False,
     client=fc['client'], industry=fc['industry'], service=fc['service'], role=None,
     summary=fc['project'], project=fc['project'], solution=fc['solution'], results=' '.join(fc['results']), gallery_title='Selected work'))

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
