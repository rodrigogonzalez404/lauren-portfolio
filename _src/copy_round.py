# Nov 24 (t109u): Rodrigo — for every Colliers real-estate case (not branding, not Fortis Net Lease): no Results,
# Project and Solution in the same size/weight, and both short and to the point. Facts only from the earlier copy.
COLLIERS_SHORT = {
 'pdx-west': ('A planned 938,000 SF Class A distribution building on Airport Way, half a mile from Portland International Airport. Colliers and Capstone Partners needed a digital leasing brochure to sell a building not yet built to logistics tenants and their brokers.',
   ['Architectural renderings and aerials, cut with translucent sage-green triangles and a heavy, wide display face, in a calm palette of sage, slate and white. Each page pairs one strong image or map with one tight block of facts, moving from the building out to the submarket, logistics hubs and drive times.']),
 'kress-building': ('A fully modernized historic landmark in downtown Portland, with Nike and Sephora on the ground floor. Colliers needed a digital leasing brochure to market 20,300 SF of office space on the second and third floors, including a 10,000 SF spec suite.',
   ['Deep Kress green and warm parchment with a single rust-orange accent, Cinzel capitals for the landmark and Proxima Nova for the facts, tied together by a line-drawn rosette medallion. The pages read like a tour: the renovation, the street, two neighborhood maps and the floor plans.']),
 'nomad': ('An apartment community in North Portland’s Overlook neighborhood, brought to market by Colliers as an investment sale. The offering package had to give investors a fast, credible read and stand out in a crowded pipeline.',
   ['Five numbered chapters, each opening on a full-bleed photo washed in a red-to-yellow gradient. Heavy italic type, a four-colour palette, a consistent icon set and charts in the same colours keep every page reading at a glance.']),
 'the-grid': ('Kirkland 405, an office building in Kirkland, Washington, was being repositioned for AI, healthcare and creative-technology tenants. The Colliers team needed a name and an identity that felt modern, connected and tech-driven.',
   ['A naming study taking three names — The Grid, Stage One and The Pulse — all the way to a logo, each shown on a blade sign and a lobby wall in one restrained presentation system. The Grid pairs two offset, open square frames with a light geometric wordmark, built to work as dimensional letters and on dark panels.']),
 'pacific-center': ('A Class A office tower in downtown Portland, half a block from Pioneer Courthouse Square and directly on the MAX light rail. Colliers needed a leasing brochure to market its suites to tenants and their brokers.',
   ['A tall-format brochure in deep navy and warm taupe, with light Gotham capitals, Adobe Caslon text and photography leading every spread. It moves from the building and its amenities to the neighborhood, the availabilities, a sample floor plan and the leasing team.']),
 'leftbank': ('A 1923 A.E. Doyle building, one of the last originals from Portland’s Albina neighborhood, now seismically retrofitted. Colliers needed a digital leasing brochure for its office and creative spaces that led with the building’s character and a neighborhood on the rise.',
   ['Full-bleed photography of brick, timber and big windows, framed by black panels and a burnt-orange accent, with Corsario headlines and a strip of six amenity icons. The pages move from the building’s history and spaces out to a local-amenities map and the revitalization of Lower Albina.']),
 'madison-plaza': ('A 157-unit apartment community built in 2022 in downtown Kent, Washington, next to the Kent Sounder Station. Colliers’ Capital Markets Group needed an offering memorandum to present it as a core-plus investment.',
   ['A landscape memorandum in raspberry and plum charcoal, set in Montserrat and led by bright photography, in four numbered sections. Clean tables, maps and oversized figures keep a data-heavy document readable.']),
 'springwood': ('A 55+ manufactured-home community in Beaverton, Oregon, fully occupied with tenant-owned homes. Colliers was taking it to market through a call for offers and needed an offering memorandum that showed investors the full picture.',
   ['Charcoal, deep teal and white with aerial photography and a vintage-style Springwood badge from cover to back page. Five numbered sections open on teal dividers, with an icon grid, a spec table, a site plan and photo spreads building the case.']),
 'mauzey-court': ('A 20,000 SF flex/industrial building in Hillsboro, Oregon, fully leased to flavor and terpene manufacturer True Terpenes. Colliers needed an offering memorandum showing investors a turnkey, mission-critical asset in a strong tech submarket.',
   ['Deep teal and seafoam with Rift’s condensed capitals, full-bleed aerials and interiors, and dot grids and thin rules for a precise, technical feel. It reads the way an investor works a deal: the asset, the tenant, a photo tour, the market and three access maps.']),
 'big-pink': ('Big Pink, the U.S. Bancorp Tower in downtown Portland, had a new owner. Colliers pitched to lead its leasing and marketing with an interactive presentation showing the landmark “seen from a new angle”.',
   ['The proposed identity, OnePink, joins the address and the nickname in one word, set in wide, rounded vertical capitals on deep navy and carried through sample marketing material. It sits inside an eight-chapter interactive Ceros presentation, where the marketing approach builds up to three logo ideas — OneEleven, Big Pink and OnePink.']),
}
def apply(projects):
    for p in projects:
        if p['slug'] in COLLIERS_SHORT:
            pr, so = COLLIERS_SHORT[p['slug']]
            p.update(project=pr, solution=so, results='', summary_eq=True)
