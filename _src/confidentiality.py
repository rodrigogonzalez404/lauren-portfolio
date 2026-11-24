"""Per-project confidentiality log: what was blurred or left out of the PUBLIC site.
`note` is shown under each gallery. `blurred` / `omitted` are for the record (README / AI-HANDOFF).
Rule (Rodrigo): leave anything confidential out; if leaving it out would look bad, blur it.
"""
STD = 'Confidential pages — pricing, financials, rent comps and broker contacts — are left out; contact details are blurred.'
NOTE_NONE = 'Confidential information — pricing, financials and rent comps — is not shown.'   # Nov 23: accurate wording for pieces with no financial content (PDX West, Leftbank)
NOTE_KRESS = 'All ten pages are shown as published — the leasing details in this brochure are public record.'   # Nov 24 (Rodrigo t94u)
LOG = {
 'pdx-west': dict(note=NOTE_NONE,
    blurred=['none — Nov 23: cover broker strip unblurred (sheet stack, printed piece); Rodrigo\'s hero/card mockup shown with contacts readable (front pages are not confidential)'],
    omitted=['pages 4 (corporate neighbors) and 7 (regional logistics hubs): removed from the sheet stack Nov 23 at Rodrigo\'s request (editorial, not confidentiality)', 'page 3 (site plan) removed from the iPad viewer Nov 24 at Lauren\'s request (editorial; still in the fanned mockup). Page 10 back cover (broker names, phones, emails + disclaimer) added to the viewer Nov 24, unblurred: no pricing, financials or rent comps anywhere in the flyer'], mockup='hero + card = Rodrigo\'s mockup on the cream surface (unblurred); printed piece = self-made mockups from the sheets'),
 'kress-building': dict(note=NOTE_KRESS,
    blurred=['nothing — Nov 24: the per-SF asking rate on p02, p07 and p08 is unblurred (iPad viewer, hero and card)'],
    exception='Nov 24, Rodrigo (Lauren\'s feedback): everything in the Kress brochure is public record and not confidential, so no page is blurred — including the leasing terms that the financials rule would normally blur.',
    omitted=['nothing — all 10 pages are in the iPad viewer']),
 'nomad': dict(note='The financial pages are left out; rents, rent comparables and development costs are blurred.',
    blurred=['Nov 24 (all pages restored): p09 the subject property\'s average-rent figure; pp. 10–11 the development-cost table (cost per unit, per SF, totals); pp. 44–47 every rent figure in the rent-comparable tables and charts. Neighborhood and city market statistics and the broker contacts are shown'],
    omitted=['printed pp. 50–55 (PDF 26–28: pro forma, monthly financials, underwriting notes) — replaced by a black "Confidential — financial information omitted" spread after the kept 05 The Financials divider (Rodrigo t97u, Nov 24)']),
 'the-grid': dict(note='Name and logo concepts shown as presented; the client feedback is paraphrased without names.', blurred=[], omitted=['the client feedback email itself (paraphrased in Results; no names of individuals shown)', 'full deck pages — the logos are shown from the deck’s own vector artwork and the signage mockups are cropped from it']),
 'pacific-center': dict(note='', blurred=['none — Nov 23 flip-book: all 12 printed pages checked; no pricing, rents or operating figures (availabilities = suite numbers + SF only)'], omitted=['nothing — cover, spreads pp. 2–11 and back cover (broker contacts readable: not financial) all shown']),
 'leftbank': dict(note=NOTE_NONE, blurred=['none — pages 1–7 checked: no rents, prices or deal figures; only the 500–6,500+ SF space range. Page 7 (back cover, leasing team contacts) is shown — front-page content, not financial (Rodrigo, Nov 23)'], omitted=[]),
 'madison-plaza': dict(note='Section 03 Financials (pages 24–33) is left out; contacts and deal figures elsewhere are blurred.',
    blurred=['p02 broker names, emails and phones','p07 offering bullets (price guidance, NOI, lender)','p08 operating text (opex, in-place vs market rents, NOI upside)','p10–11 ground-rent and MFTE savings text','p40 in-place rent / income-qualification line'],
    exception='Home/works card and case hero: the phone screen in the device mockup shows the p08 operating-expense paragraph unblurred — Rodrigo approved showing it on the card (Nov 23, 2:52 PM PT: "please ensure nothing is blur on this image").',
    omitted=['PDF pages 13–17 = printed pp. 24–33 (unit mix & market rents, tax bill, income & expenses, pro forma notes, 10-year cash flow, rent comparables); replaced in the flip-book by a black "Confidential — financial information omitted" spread right after the 03 The Financials divider (pp. 22–23, kept)']),
 'redmond-gateway': dict(note=STD,
    blurred=['p03/p04 parcel pages: paragraph naming the owners and tenant lease dates'],
    omitted=['executive summary','investment highlights table','page 05 parcel SF table','pages 08–10 rent/sale comps','pages 11–13 statistics','page 16 broker contacts']),
 'springwood': dict(note='The financial overview and rent comparables are left out.',
    blurred=['none — Nov 24 (t108u): Rodrigo approved unblurring everything (p01 cover, p04, p05, p07 were blurred before): "It doesn\'t need to be blur. What is confidential is already removed."'],
    omitted=['PDF 14–15 Financial Overview (financial summary, rent roll) — replaced by a black "Confidential — financial information omitted" screen after the kept 03 divider', 'PDF 17 Rent Comparables — black screen after the kept 04 divider']),
 'mauzey-court': dict(note='The lease abstract is confidential and left out.',
    blurred=['none — Nov 24 (t109u): Rodrigo approved unblurring everything on Mauzey (p03 executive-summary headline line and p04 Price row were blurred before)'],
    omitted=['p07 Lease Abstract (base-rent schedule, NOI, tenant investment, escalations) — replaced by a black "Confidential — financial information omitted" screen in the iPad viewer'],
    shown=['cover and back cover with broker names, phones and emails (front pages are not confidential)', 'p05 tenant-funded-improvements highlight and p12 demographics (income) — not deal pricing, rents or operating figures', 'p10 Portland market overview incl. the market-wide average asking lease rate (published Colliers market data, not this property\'s rent)']),
 'pointe-at-bridgeport': dict(note=STD,
    blurred=['none — Nov 23: p01 cover broker strip + hero mockup unblurred (front page)'],
    omitted=['pages 5–6 demographics','page 9 broker contacts']),
 'portland-office-market-report': dict(note='Data pages (statistics, sale prices, tenants) are left out of this portfolio.',
    blurred=[], omitted=['pages 03–16 market data and sales']),
 'fortis-net-lease': dict(note='Listing flyers that show prices, cap rates and broker contact details are left out.',
    blurred=[], omitted=['RealEstate_Examples.jpg (readable sale prices, cap rates, listing prices)','8-FNL.jpg email flyers (listing prices, cap rates, broker names, phones, emails)']),
 'big-pink': dict(note='Laptop viewer of 25 design screens + 3 black confidential screens; OnePink identity, moodboard, naming and logo concepts are front-of-house, not financial.', blurred=[], omitted=['[03] The Market — submarket figures, absorption, rents and concessions (black screen in viewer)', '[04] The Competition — competitive set with rents (black screen in viewer)', '[06] Fee Proposal — fee terms (black screen in viewer)', 'team, client-list, reference, lease-map and services screens', 'the empty SWOT screen and the repositioning screen (carries copy from another project)', 'no live embed of, or link to, the Ceros presentation']),
 'marketplace': dict(note='Laptop viewer of 9 curated design screens.', blurred=[], omitted=['all Ceros pages outside the curated 9 (market data, fees, team, client lists)', 'no live embed of, or link to, the Ceros presentation']),
}
