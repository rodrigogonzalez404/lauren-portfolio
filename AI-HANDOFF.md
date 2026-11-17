# AI handoff — Lauren Gonzalez portfolio

Read this first if you are an AI assistant (Claude, ChatGPT, Cursor, etc.) continuing this project.

## Who / what
- **Lauren Elyse Gonzalez** — graphic designer at **Colliers, Portland** (current role; never call it "former").
  Home role line: "/ Graphic Designer"; nav subtitle: "Senior Graphic Designer". "16 years of experience".
- Goal of the site: support her promotion at Colliers. **Real Estate leads, Brand & Ecommerce second.**
- Owner of the build: Rodrigo (4TC). Lauren will keep changing mockups — the site is the backbone.

## Hard rules
1. **Confidentiality** (site is public): leave confidential material out; blur only where omitting would look bad.
   No prices, rents, cap rates, NOI, financials, comps, fee proposals, broker names/phones/emails, team photos,
   references, stacking plans with SF. Log every blur/omission in `_src/confidentiality.py` (→ `CONFIDENTIALITY.md`).
   Do a visual check of every new image before publishing.
2. **Excluded projects — do not add:** The Galt, 8210 Mauzey Court, Fruit Valley, Pomeroy, Overland AI, W+K,
   American Brush / REMS, Houghton RFQ. Apex is skipped.
3. **Ceros (Big Pink, Marketplace I & II):** curated screenshots only; no live embeds, no links to Ceros URLs
   (pending Colliers approval).
4. **Copy:** use real copy only. Anything invented or unconfirmed goes in `[[ ]]`; never invent metrics.
   Never AI-redraw Lauren's artwork — mockups composite the original page art.
5. **Nomad flip-book:** pages are unblurred on purpose (Rodrigo: "remove the blur"); confidential pages stay out.
6. `noindex, nofollow` meta on every page + `robots.txt` disallow all. Don't remove.
7. Don't deploy to Vercel. Don't push/publish without Rodrigo's OK.

## How it's built
- `_src/content.py` — all copy and the project list (`PROJECTS`, `CEROS`, `BRAND`; `ALL` drives page order and "Next project").
- `_src/brand_copy.py` — verbatim copy from Lauren's live Webflow case studies.
- `_src/confidentiality.py` — per-project blur/omission log (+ the note shown under each gallery).
- `_src/build.py` — writes all HTML (Python 3 + Pillow). Run from repo root: `python3 _src/build.py`.
- `_src/images.py` — regenerates `assets/img/` from the original PDFs/mockups on the build box (paths under `/workspace/...`,
  not in the repo). Contains the page selections and blur boxes (fractions of the page). You normally won't need it —
  just drop replacement images into `assets/img/<slug>/` with the same names.
- Case template = the "Nomad v2" case layout: Cover → Hero mockup → Meta row → dark Project/Solution/Results → Galleries → Next project.
- Responsive: one page serves desktop and mobile (breakpoints at 960 / 820 / 640px; fluid `clamp()` type).

## Open items (as of the initial commit)
- All Real Estate case copy (Project / Solution / Results / summary / role / client team) is `[[placeholder]]` — needs Lauren.
- Nomad copy is a draft written from the document — Lauren to review. Results unknown.
- Ceros: type, city, year, and whether Colliers approves showing them.
- Home "Approach" section is placeholder copy.
- Contact page has no form (GitHub Pages is static) — email + LinkedIn only.
- Portland Office Market Report: only cover + contents shown; the report may be public — confirm before adding data pages.
- Fortis Net Lease sits under Real Estate (works page only, not on Home); its location is `[[National]]`.
- Zulay Kitchen and CGK case copy contain sales metrics that are on Lauren's live site; Home no longer mentions 8-figure / Target / Walmart (Rodrigo's request) — confirm whether the case pages should keep them.
