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
- Case template (Rodrigo, Nov 19): ABOVE the gallery = the redesign intro (cover label + big title + summary → 16:9 hero, or the auto-playing playlist on interactive pages → ruled meta row, equal 72 top/bottom → dark [01] Project / [02] Solution / [03] Results). FROM the gallery down = Figma page "01 Rebuild (current site)" frame 7:2: white gallery (cols 2–7, 128 top/bottom) → grey Next Project (80) → footer. No captions/labels on any picture.
- Spacing: 8-col grid (147/24 gutters/48 margins at 1440; 16 margins mobile). Tokens in `assets/css/site.css`: `--cs` 128 (info + gallery padding, equal top and bottom), `--cn` 80 (Next Project), hero clamp(360px,43.75vw,630px). Galleries are equal-height rows (full width / pairs / portrait triples, sized by aspect ratio) so nothing is cropped. Home/Works/About keep the `--sec`/`--s96…` rhythm. CSS/JS are cache-busted with `?v=<md5>` by build.py. Hero override: `python3 _src/set_hero.py SLUG file.jpg` stores a supplied mockup as `<MOCK>/SLUG_hero-override.jpg` (images.py prefers it); Madison Plaza shows an override uncropped on white (`.case-hero.fit`).
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

## Madison Plaza (Nov 19) — "like Nomad"
- Hero, intro, meta row and dark [01]/[02]/[03] are unchanged (hero = Rodrigo's mockup via `_src/set_hero.py`).
- Below that: Design system (colour swatches only, sampled from the PDF: #B0144A, #A41D41, #37272C, #ACA5A8, #FFFFFF; brochure crops, type note and captions removed per Rodrigo) → The printed book → Inside the book (same PageFlip component as Nomad).
- Assets come from `_src/madison_book.py` (also run by images.py); page order is saved in `_src/madison_flip.json`.
- Flip-book order: cover, printed pages 2–23 (PDF pages 2–12; PDF 12 is the "03 The Financials" divider and is kept), then a black HTML spread reading "Confidential — financial information omitted", then printed pages 34–45 (PDF pages 18–23), then the back cover (PDF 24).
- PDF pages 13–17 (printed pages 24–33) are financials and are never published.
- Blur boxes are defined in `madison_book.py` and logged in CONFIDENTIALITY.md.

## Leftbank (Nov 20) — flyer as a sheet stack
- Same intro as every case page. Below it: Design system (swatches #CB5625 Burnt Orange, #000000 Black, #50B848 Leaf Green, #ECEBF0 Map Grey, #FFFFFF White) → The printed piece (flyer mockup + flat front sheet and back sheet) → Inside the flyer (sheet stack).
- Sheet stack is a reusable component:
  - Build: `sheet_stack(slug, title, n, r)` in build.py.
  - Styles: `.ss-*` in site.css, sitting on the shared `.fb-stage` desk.
  - Behaviour: the "sheet stack" block in site.js. Arrows, click, drag/swipe and ← → keys all work; it respects prefers-reduced-motion.
  - Images: `assets/img/<slug>/sheets/sNN.jpg`, rendered fresh from the PDF at 200 dpi by `_src/flyer_sheets.py`. Add new flyers to its FLYERS dict, with optional blur boxes.
- Leftbank PDF page 7 (broker contacts) is never shown. Sheets 1–6 need no blurs.
