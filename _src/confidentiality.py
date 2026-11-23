"""Per-project confidentiality log: what was blurred or left out of the PUBLIC site.
`note` is shown under each gallery. `blurred` / `omitted` are for the record (README / AI-HANDOFF).
Rule (Rodrigo): leave anything confidential out; if leaving it out would look bad, blur it.
"""
STD = 'Confidential pages — pricing, financials, rent comps and broker contacts — are left out; contact details are blurred.'
LOG = {
 'pdx-west': dict(note=STD,
    blurred=['none — Nov 23: cover broker strip unblurred (sheet stack, printed piece); Rodrigo\'s hero/card mockup shown with contacts readable (front pages are not confidential)'],
    omitted=['page 10 back cover: broker names, phones and emails + disclaimer (no pricing, financials or rent comps anywhere in the flyer)'], mockup='hero + card = Rodrigo\'s mockup on the cream surface (unblurred); printed piece = self-made mockups from the sheets'),
 'kress-building': dict(note=STD,
    blurred=['p02: "$28/SF FSG" rent figure (Nov 23: p01 cover + hero mockup unblurred — commission callout and broker contacts are front-page content)'],
    omitted=['page 05','pages 07–08 floor plans carrying the $28/SF FSG rate','page 10 broker contacts']),
 'nomad': dict(note='Confidential chapters — pricing, financials, rent comps and broker contacts — are left out.',
    blurred=['none (Rodrigo: "remove the blur" on the flip-book pages)'],
    omitted=['offering/price pages, financials, rent comps, contacts, page-04 offering table (nomad_om-spread.jpg not published)']),
 'the-grid': dict(note='Name and logo concepts shown as presented.', blurred=[], omitted=[]),
 'pacific-center': dict(note=STD, blurred=[], omitted=['page 6 availabilities (suites, SF, rates)','page 7 broker contacts']),
 'leftbank': dict(note=STD, blurred=['none — sheets 1–6 checked (Nov 20): no rents, prices, contacts or deal figures; only the 500–6,500+ SF space range'], omitted=['page 7 broker contacts (names, phones) — not in the sheet stack']),
 'madison-plaza': dict(note='Section 03 Financials (pages 24–33) is left out; contacts and deal figures elsewhere are blurred.',
    blurred=['p02 broker names, emails and phones','p07 offering bullets (price guidance, NOI, lender)','p08 operating text (opex, in-place vs market rents, NOI upside)','p10–11 ground-rent and MFTE savings text','p40 "Clears 3x in-place rent ($1,864/mo …)" line','back cover broker names, emails and phones'],
    omitted=['PDF pages 13–17 = printed pp. 24–33 (unit mix & market rents, tax bill, income & expenses, pro forma notes, 10-year cash flow, rent comparables); replaced in the flip-book by a black "Confidential — financial information omitted" spread right after the 03 The Financials divider (pp. 22–23, kept)']),
 'redmond-gateway': dict(note=STD,
    blurred=['p03/p04 parcel pages: paragraph naming the owners and tenant lease dates'],
    omitted=['executive summary','investment highlights table','page 05 parcel SF table','pages 08–10 rent/sale comps','pages 11–13 statistics','page 16 broker contacts']),
 'springwood': dict(note=STD,
    blurred=['p01 cover: "75 Sites | 100% Occupied | $1,035 Avg. Rent" line (also blurred on the hero mockup)'],
    omitted=['pages 04, 05, 07 (summary/offering text)','pages 13–15 financials','page 17 comps','pages 19–20 statistics','page 21 rent-control text','page 22 contacts']),
 'pointe-at-bridgeport': dict(note=STD,
    blurred=['none — Nov 23: p01 cover broker strip + hero mockup unblurred (front page)'],
    omitted=['pages 5–6 demographics','page 9 broker contacts']),
 'portland-office-market-report': dict(note='Data pages (statistics, sale prices, tenants) are left out of this portfolio.',
    blurred=[], omitted=['pages 03–16 market data and sales']),
 'fortis-net-lease': dict(note='Listing flyers that show prices, cap rates and broker contact details are left out.',
    blurred=[], omitted=['RealEstate_Examples.jpg (readable sale prices, cap rates, listing prices)','8-FNL.jpg email flyers (listing prices, cap rates, broker names, phones, emails)']),
 'big-pink': dict(note='', blurred=[], omitted=['all Ceros pages outside the curated 10 (market data, fees, team, client lists); no live embed or link']),
 'marketplace': dict(note='', blurred=[], omitted=['all Ceros pages outside the curated 9; no live embed or link']),
}
