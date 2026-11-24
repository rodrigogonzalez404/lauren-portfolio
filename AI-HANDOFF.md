# AI handoff — Lauren Gonzalez portfolio

**Assistants: read `CLAUDE-HANDOFF.md` first. It supersedes older notes here and in AI-HANDOFF.md.**

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
2. **Excluded projects — do not add:** The Galt, Fruit Valley, Pomeroy, Overland AI, W+K,
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
- Case template (Rodrigo, Nov 19): ABOVE the gallery = the redesign intro (cover label + big title + summary → 16:9 hero (interactive pages too since Nov 23 — the playlist is gone) → ruled meta row, equal 72 top/bottom → dark [01] Project / [02] Solution / [03] Results; an empty `results` string hides [03]). FROM the gallery down = Figma page "01 Rebuild (current site)" frame 7:2: white gallery (cols 2–7, 128 top/bottom) → grey Next Project (80) → footer. No captions/labels on any picture.
- Spacing: 8-col grid (147/24 gutters/48 margins at 1440; 16 margins mobile). Tokens in `assets/css/site.css`: `--cs` 128 (info + gallery padding, equal top and bottom), `--cn` 80 (Next Project), hero clamp(360px,43.75vw,630px). Galleries are equal-height rows (full width / pairs / portrait triples, sized by aspect ratio) so nothing is cropped. Home/Works/About keep the `--sec`/`--s96…` rhythm. CSS/JS are cache-busted with `?v=<md5>` by build.py. Hero override: `python3 _src/set_hero.py SLUG file.jpg` stores a supplied mockup as `<MOCK>/SLUG_hero-override.jpg` (images.py prefers it); Madison Plaza shows an override uncropped on white (`.case-hero.fit`).
- Responsive: one page serves desktop and mobile (breakpoints at 960 / 820 / 640px; fluid `clamp()` type).

## Open items (as of the initial commit)
- All Real Estate case copy (Project / Solution / Results / summary / role / client team) is `[[placeholder]]` — needs Lauren.
- Nomad copy is a draft written from the document — Lauren to review. Results unknown.
- Ceros: Big Pink settled Nov 23 (see below). Marketplace I & II removed from the site Nov 23 PM (sources kept).
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

## PDX West (Nov 20) — same sheet stack as Leftbank
- Swatches: #76A48E Sage, #505F69 Slate, #374B4E Deep Slate, #ECF3F0 Mist, #FFFFFF White.
- There is no signage for PDX West; it is a leasing flyer only. Don't mention signs or billboards in its copy or alt text.
- Mockups are all self-made by `_src/flyer_mockups.py` from the already-blurred sheets, with no stock and no props. The pen was removed on Nov 20 because it looked fake. Each sheet is one exact perspective warp rendered at 4× and downsampled with LANCZOS. The source is edge-padded, so the anti-aliased edge keeps the artwork's own colour: no rim, fringe or seams. Shadows are multiply layers (ambient, contact and two soft offsets, with the light from the top-left). A raised corner is suggested only through light and shadow. The beige surface is procedural.
  - `hero.jpg` + `card.jpg` (Nov 23): Rodrigo's own mockup (standing cover, tablet with Property Highlights, flat back sheet), source `/workspace/lauren-case-studies/mockups/pdx-west_rodrigo-mockup.png`. `_src/pdx_rodrigo_mockup.py` puts it on the cream surface. Nothing is blurred: contacts are readable per the Nov 23 rule; the traced contact quads are kept as `CONTACTS_TRACED`. Background and shadow pixels are multiplied onto the cream, so the studio shadows carry over and the edges have no white halo. Object pixels are kept as they are. The object mask is saturated or dark pixels with the holes filled, plus traced polygons for the standing pad's page stack and easel and for the flat sheet. In the hero, the objects sit inside the wide central band the case-hero crop shows (about 58% of the height). In the card (4:3, shown whole), they fill about 86% of the width. If Rodrigo sends a new version of this mockup, re-trace `STAND`/`FLAT` in that script.
  - `mock_spread.jpg` (The printed piece): three inside sheets (site plan, submarket, building) fanned out.
  - `mock_cover.jpg` (The printed piece; this was the card until Nov 23): one thin cover sheet with a lifted corner and a second sheet peeking out underneath.
- The printed piece: mock_spread + mock_cover, then the flat front sheet (s01) and back sheet (s07 = PDF p9).
- Sheet stack (Nov 23): 7 sheets = PDF pages 1, 2, 3, 5, 6, 8, 9 (Rodrigo removed stack sheets 4 corporate neighbors and 7 regional logistics hubs). Page 1 unblurred. Page 10 (back cover with broker contacts) is omitted. `flyer_mockups.pdx()` indexes S[2]/S[3]/S[5] = PDF p3/p5/p8.
- `flyer_sheets.py` re-runs `flyer_mockups.pdx()` after rendering the sheets.
- Project and Solution copy is written from the flyer (no rents, prices or deal figures). Results stays `[[ ]]`.
- `sheet_stack(..., note)` prints the confidentiality line under the stack. Leftbank and PDX pass `LOG[slug]['note']` (the STD text).

## Confidentiality rule change (Rodrigo, Nov 23)
- Rodrigo: "Anything in the front pages is not confidential. Confidential means financials."
- Covers, thumbnails, cards and hero mockups are shown unblurred: contacts, headlines, addresses, broker strips and the Kress commission callout. Done in `/workspace/mk/run.py` (Kress, Pointe mockups), `_src/images.py` (Kress/Pointe p01), `_src/flyer_sheets.py` (PDX s01) and `_src/pdx_rodrigo_mockup.py`.
- Still blurred or omitted, because it's financial: Kress p02 asking rate; the Springwood cover average-rent figure (cover and hero); Madison section 03 and its financial blurs; omitted rent, comp and financial pages everywhere.
- Interior blurs that cover only contacts or names are unchanged and waiting for Rodrigo to confirm: Madison p02 and back cover broker contacts, and Redmond p03/p04 owner names and lease dates (Redmond is no longer published as of Nov 23).
- The STD stack disclaimer ("...contact details are blurred.") is Rodrigo's verbatim wording and is still printed under the PDX and Leftbank stacks. It is not accurate any more, so wait for his call before changing it.

## Batch Nov 23 (Rodrigo t70u)
- **One cream — now pale stone #ECEAE6** (Rodrigo t77u, Nov 23 PM; see the section at the end). Before that: `CREAM = (210, 206, 200)` #D2CEC8 was the only mockup surface colour; it replaced PDX's #D6CFC6 and the tan scene photos (#C1BAB0 Kress/Springwood, #B7AFA5 Pacific, etc.). `flyer_mockups.surface()` normalises its median to CREAM (PDX hero/card/mock_*, Madison book + card). `/workspace/mk/mock.py compose()` cools/desaturates each scene backdrop (chroma ×0.7, then per-channel gain so the backdrop median = CREAM; artwork untouched; `NO_CREAM={'billboard'}`). Regenerate: `cd /workspace/mk && python3 run.py kress pacific leftbank pointe grid madison springwood && python3 nomad.py`, then copy the four Nomad mockups at 1800 px wide into `/workspace/redesign/img/nomad/` (pre-change copies in `nomad-pre-cream-nov23/`), then `python3 _src/images.py && python3 _src/build.py`. The dark charcoal flip-book/stack desk is not part of this.
- **Madison card.** `_src/madison_card.py` (called by images.py) puts Rodrigo's white mockup on the cream, whole, about 88% of the 4:3 card width: light pixels are multiplied onto the cream and the device screens are kept exact. Output is `madison-plaza/card.jpg`; the case hero (`hero.jpg`, white, `.case-hero.fit`) is unchanged.
- **Nomad.** The design-system crops (ds_*) and the [Type] line were removed; only the swatches remain.
- **Wild Naturals.** The gallery follows Figma frame 12:2 (`FIG_ROWS` in build.py): full · pair · full · pair (inset, `.g-inset`) · full · full · full, at 1002 / 489+489 px at 1440.
- **Removed:** Redmond Gateway and Portland Office Market Report (`content.UNPUBLISHED`). Their entries are kept in content.py/images.py/confidentiality.py as source, with no page, card, Next link or images.

## Pacific Center (Nov 23) — like Nomad / Madison, as a brochure
- Hero (poster mockup) and intro block unchanged. Below: Design system (swatches only: Navy #212B3B, Slate Blue #435774, Taupe #D7CBC4, Umber #583117, White, sampled from the pages) → The printed brochure (open-spread mockup on the shared cream + flat front/back cover) → Inside the brochure (flip-book on the charcoal desk).
- Source PDF `source/extracted/PacificCenter-Flyer.pdf`: 7 letter pages; PDF 2–6 are two-page spreads exported squashed to half width. `_src/pacific_book.py` renders them from the vectors at 2× width (`pdftoppm -scale-to-x 3400 -scale-to-y 2200`, into `pages/pacific-center-brochure/`), which restores the true proportions, then splits them into printed pp. 2–11. Flip sequence = cover, pp. 2–11, back cover (12 pages). The old squashed p01–p05 gallery is gone.
- Flip-book page size is now per book: `#fb-book data-w/data-h` (Pacific 850×1100 portrait; default 1100×850). `data-total` + `data-pg` on pages make the counter show printed page numbers ("Pages 02–03 / 12"). Nomad/Madison are unchanged. `.fb-wrap.tall` caps the portrait book at 1000px.
- Open-spread mockup: `/workspace/mk/run.py pacific-book` (scenes/spread.jpg, quad `SPREAD`) → `mockups/pacific-center_brochure-spread.jpg` → `book_mockup.jpg`.
- Confidentiality: no pricing, rents or operating figures anywhere (Availabilities = suite numbers + SF). All 12 pages shown, nothing blurred; back-cover broker contacts are readable (not financial). No disclaimer added.

## Digital brochures on an iPad (Nov 23, Rodrigo t72u/t73u) — Kress, PDX West, Leftbank, Springwood
- "These are meant to be digital brochures… an iPad and the person changes the pages." The sheet stacks / page galleries for these four are replaced by one reusable viewer: `ipad_viewer(slug, title, files, r, note, label)` in `_src/build.py`; CSS block "iPad viewer" in `site.css` (`.tab-*`); JS `.tab-stage` handler in `site.js` (drag/swipe with axis lock + rubber band, click left/right half of the screen, arrow buttons, ← → keys when in view, dots, "Page 01 / NN" counter, lazy `data-src`, reduced motion = cross-fade; `window.tabViewer`).
- CSS-drawn landscape iPad (aluminium rim, black glass, camera dot), 4:3 screen, pages `object-fit:contain` on black. Stage = shared stone #ECEAE6, flat in CSS since Nov 23 PM (the old `ui/cream-surface.jpg` texture, generated by images.py) — same on all four.
- A file entry `('CONF', 'section text')` renders a black "Confidential — financial information omitted" screen (Madison pattern). Used for Springwood (after the kept 03 and 04 dividers).
- Each case: Design system swatches (where defined) → "The brochure"/"The offering memorandum" (front + back cover) → "Inside the brochure/memorandum" viewer. PDX keeps its paper mockups in "The brochure" (Rodrigo asked for them earlier).
- Kress: all 10 pages; only the per-SF asking rate is blurred (p02, p07, p08). Springwood: PDF 1–13, 16, 18–22 shown; 14–15 (financial overview) and 17 (rent comps) omitted; cover average-rent figure, p4 lot-rent range, p5 rent-upside paragraph and p7 property tax blurred. Leftbank: all 7 pages (back cover now included). PDX: sheets 1,2,3,5,6,8,9.
- Copy changed "printed/flyer" → "digital"; types are "Digital Leasing Brochure" / "Digital Offering Memorandum". Project/Solution written from the documents; Results stay `[[ ]]`.

## The Grid (Kirkland 405) — identity case (Nov 23)
- Body built by `_src/grid_blocks.py` (called from `build.case`): The mark (clear-space diagram, symbol, wordmark) → Versions (primary, reversed, one colour, on grey, avatar sizes) → Color → Typography (Open Sans, self-hosted subset `assets/fonts/OpenSans-Var.woff2`) → In place → Concept exploration (The Grid chosen; Stage One and The Pulse labelled as concepts, with their deck signage mockups).
- Logos are real vectors extracted from Lauren's deck PDF (`_src/grid/extract_logos.py` → `logo-*.svg`, `fill=currentColor`) and inlined as SVG, so they recolour per panel. Symbol/wordmark = same SVG with a cropped viewBox (`.gr-logo.crop`).
- Raster assets from `_src/grid/grid_assets.py` (run by images.py): hero.jpg (logo on stone over a faint grid), card.jpg (the existing lobby-sign mockup — the thumbnail Rodrigo referred to), deck signage crops (page 3/5/7 right column at 300 dpi), cards.jpg (code-built business cards on the shared cream).
- Results states the client chose The Grid (source: Colliers email "They have confirmed the Grid for the name/logo"); the client's feedback is paraphrased, no names. No building banner was made (no honest way to make it flawless); the deck's exterior blade sign + lobby wall + lobby panel + business cards cover the applications.

## Big Pink + Marketplace — Ceros in a laptop, OnePink identity (Nov 23, Rodrigo t74u/t75u)
- The Ceros previews can't be iframed (CSP frame-ancestors) and must NOT be linked anywhere. Both cases show screen captures
  in a CSS laptop that reuses the iPad viewer (`ipad_viewer(..., device='laptop')` → `.tab-wrap.lap` + `.lap-base`). Home/Works
  cards are laptop renders; the auto-playing playlist is gone from cards and heroes.
- Big Pink leads with **OnePink**, Grid-style: The mark (vertical + horizontal) → Versions → Color → Typography (Cabin) →
  In place (concept board, sample marketing material, tagline) → The presentation (laptop viewer, 25 screens + 3 black
  confidential screens) → Moodboard → Naming → Concept exploration (OneEleven, Big Pink, Prism "First round").
  Rules from Rodrigo: the client did NOT pick a name or logo — never say OnePink was chosen (it is "the one carried into the
  sample marketing material"); Colliers did NOT win — Results is empty (block hidden), copy says "pitched"; Lauren designed
  the whole presentation (role line).
- Code: `_src/bigpink_blocks.py` (sections), `_src/bigpink/bp_assets.py` (called at the end of images.py; writes
  `assets/img/big-pink/` + `assets/img/marketplace/`). OnePink wordmark = `_src/bigpink/onepink-h.svg` / `onepink-vertical.svg`,
  traced with potrace (`trace_onepink.py`) from the white letters on the Ceros concept board; paths `.w1` ONE / `.w2` PINK,
  inlined once as `<symbol>`s and coloured with `--one` / `--pink`. Hero = OnePink on Dark Blue (code-built).
- Laptop renders (Big Pink card, Marketplace hero + card) are stored in `/workspace/bigpink/rendered/` and copied in by
  bp_assets; re-render with `_src/bigpink/render_laptops.js` (needs the :8765 server) only if a cover screen changes.
- Sources off-repo: `/workspace/bigpink/cap/` (Ceros captures), `/workspace/bigpink/media/` (Ceros media),
  `/workspace/uploads/big-pink.pdf` (logo-concepts deck). Screen selection + exclusions are commented in bp_assets.py.
- Viewer hints: arrows wrapped in `.kb` (Geist) — PT Mono has no ← → glyphs and showed dots.
- **Rodrigo t76u (Nov 23):** Big Pink took Nomad's place as the featured full-width card on Home (Real Estate, after
  PDX/Kress); Nomad moved down to the second full-width slot (after The Grid/Pacific). Big Pink's card is the OnePink
  marketing mockup on its ORIGINAL white (`card-wide.jpg` 16:9 for Home, `card.jpg` 4:3 for Works / Next Project — both
  padded with white, nothing cropped; built in bp_assets `white_frame`). Home Interactive section now shows Marketplace
  full width (its 16:9 laptop hero) plus a one-line pointer to Big Pink; Works keeps both Ceros cards.
  Inside: a `[Contents]` TOC (`.toc`, mono [NN] labels, charcoal rules, anchors + the site's smooth scroll) opens the
  gallery. Order: The mark, Versions, Moodboard, Color, Typography, Concept exploration, Naming, In place, The presentation
  (last) — set by the `secs` list in bigpink_blocks.py (the TOC is generated from it). In place mockup = `material.jpg`
  on white (no cream multiply). Client line = "Colliers".

## Pale stone #ECEAE6 replaces the cream (Rodrigo t77u, Nov 23 PM)
- Rodrigo found #D2CEC8 "tanned"; he picked option C from `/workspace/lauren-site-previews/bg-options/`. The cream is now
  **#ECEAE6** everywhere: `_src/palette.py` `CREAM = (236, 234, 230)` (the name CREAM is kept; it is the one source).
- **No paper texture.** `flyer_mockups.surface()` is flat stone + a faint neutral grain + a colourless light falloff;
  `ui/cream-surface.jpg` is retired. The iPad/laptop stage (`.tab-stage`, `_src/bigpink/laptop-render.html`) is flat
  #ECEAE6 with a white highlight and a neutral grey vignette. Device and sheet shadows are neutral grey
  (CSS rgba(16–22,16–22,18–22,…); `_multiply` tint 0.40/0.40/0.41). Hint/note text #5E5F62.
- **Rebuilt from source** (not re-tinted): PDX hero/card/mock_spread (pdx_rodrigo_mockup + flyer_mockups), Madison card
  (madison_card), The Grid business cards (grid_assets), Marketplace laptop hero/card (render_laptops.js →
  `/workspace/bigpink/rendered/`), and every scene mockup from `/workspace/mk/run.py kress pacific leftbank madison
  springwood pointe grid nomad pacific-book` — `mk/mock.py` now neutralises the backdrop chroma (0.25) and smooths its
  texture (masked blur) before the gain to CREAM. Nomad's four scene photos (n01/n02/n03/n06) are re-surfaced by
  `_src/nomad_surface.py` (run by images.py) from the original photos in `/workspace/redesign/img/nomad-pre-cream-nov23/`.
- Unchanged on purpose: the charcoal flip-book desk, the Madison hero (Rodrigo's white original), the Big Pink card and
  In place mockup (white), Big Pink hero (navy), brand cards, Zulay, CGK, Contact.
- Backups of the cream versions: `/workspace/lauren-case-studies/mockups-pre-stone-nov23/`,
  `/workspace/redesign/img/nomad-pre-stone-nov23/`, `/workspace/bigpink/rendered-pre-stone/`, `/workspace/mk/mock.py.pre-stone`.

## Texture back, no blur; The Grid on an entrance wall; Marketplace removed (Rodrigo t78u, Nov 23 PM)
- Rodrigo: the smoothed stone "looks blurred"; he wants "pale stone but with texture and context". **Supersedes the
  "No paper texture" / "smooths its texture" lines above.** Rule now: colour-grade only — never denoise, blur or flatten.
- `mk/mock.py` restored from `mock.py.pre-stone` (smoothed one kept as `mock.py.smoothed-073932d`); grade = backdrop
  chroma ×0.55, gain toward CREAM hue at luminance `min(stone, median×1.08)` (keeps the scene's own light and grain).
  Re-run: `run.py kress pacific leftbank madison springwood pointe nomad pacific-book`.
- `_src/nomad_surface.py`: same grade, mask only (edge walls + border-connected regions), no blur.
- `flyer_mockups.surface()` has a real neutral grain/mottle again (blur 0.8, colourless); images.py writes
  `ui/stone-surface.jpg` (seed 7) and `.tab-stage` uses it under the neutral vignette.
- **The Grid card + hero** = Lauren's deck entrance mockup (`sign_blade.jpg`: black panel on the stone-clad facade beside
  the glass doors), `grid_assets.entrance()`: card 4:3 right crop, hero 16:9 (y0 8%, keeps the panel top), a 50% white
  balance of the light cladding toward stone. Native size is only 1760 px wide (deck image), so that is the hero width.
  The old lobby-sign card and vector `hero()` are retired; In place = lobby wall letters + business cards.
- **Marketplace I & II removed** from the site (content.py `UNPUBLISHED`; home Interactive section and the Big Pink
  pointer line deleted; works index Interactive now lists only Big Pink). Sources kept: `bp_assets.marketplace_assets()`
  (not called), `/workspace/bigpink/rendered/marketplace-*.jpg`, the confidentiality LOG entry.
- Note: the page background (`--paper` #F2F2F2) was never changed; only mockup/viewer surfaces are #ECEAE6.

## Madison takes the big slot, Nomad the square (Rodrigo t79u, Nov 23 PM)
- Home Real Estate order: PDX + Kress → Big Pink (wide) → The Grid + Pacific → **Madison (wide, `card-wide.jpg`)** →
  Leftbank + **Nomad** → Springwood + Pointe.
- `_src/madison_card.py` rewritten (old multiply version: `/workspace/mk/madison_card.py.multiply-nov23`): only the
  backdrop takes the textured stone; devices, screens and brochure pages are copied exactly (whites stay 255). Object mask =
  edge-closed, border-connected region of the white-background hero source, halo trimmed by regrowing the backdrop
  through white pixels; backdrop + its soft shadows are multiplied onto `flyer_mockups.surface()`. Writes card-wide.jpg
  (2400×1350, group 94% wide) and card.jpg (4:3, works index). The phone's opex paragraph is blurred (financial, = p08).
- Nomad card = Rodrigo's cover-on-stone image `_src/nomad_card_src.png`, white screenshot border trimmed, resized to
  1440×1080 → `assets/img/nomad/card.jpg` (images.py; home + works). Source is only ~1120 px wide. Nomad hero unchanged.
- **Nov 23, 2:52 PM PT (Rodrigo t80u): "please ensure nothing is blur on this image"** — the phone paragraph blur on the
  Madison card is removed (`madison_card.BLUR = []`); recorded as an approved exception in confidentiality.py/CONFIDENTIALITY.md.

## Big Pink card = OnePink on Dark Blue (Rodrigo t81u, published a92f4e4)
- `bp_assets.navy_wordmark(W, H, logo_frac)` draws the hero treatment; `cards()` writes card-wide.jpg (2400×1350) and card.jpg
  (1600×1200, wordmark 62% wide). The white marketing mockup stays inside the case page (material.jpg).

## Mauzey Court replaces The Pointe; copy pass; Contact for career opportunities (Rodrigo t82u, Nov 23)
- **8210 Mauzey Court** (`mauzey-court`, Digital Offering Memorandum, Hillsboro, OR, 2026) — source
  `/workspace/uploads/MauzeyCourt-Hillsboro-OM.pdf` (identical to lauren-case-studies/source/extracted/). PDX treatment:
  `flyer_sheets.py` renders sheets s01–s15 = PDF 1–6, 8–16 (p3 price/NOI line and p4 Price row blurred); `flyer_mockups.mauzey()`
  makes hero/card (cover over back cover on textured stone), mock_cover, mock_spread; `build.mauzey_blocks` = design system
  (MAUZEY_PAL + Rift/Proxima Nova line) → the memorandum (mockups + front/back) → iPad viewer with a black CONF screen for p7.
- The Pointe at Bridgeport: in `content.UNPUBLISHED` (source entry, RE images config and pages kept; no page/card/link).
- **No [[ ]] anywhere** in the built site. `RE_PH` is now empty; every RE case has its own Project/Solution (Pacific Center and
  Madison written from their source PDFs this pass). Results only where sourced: The Grid, plus the approved Webflow brand
  copy and Fortis. Empty Results hide the [03] block. Client = "Colliers", Role = "Graphic Designer" on every RE case.
- Home Approach: label "[Approach]", heading + three steps written (content.HOME). About: the Colliers placeholder line removed.
- **Contact rule changed (t82u overrides "Contact stays as is")**: page title "Get in Touch", CONTACT_LINE = career/opportunity
  wording, RESUME_LINE "Résumé available on request — just send me a note.", buttons "Get in Touch" (mailto) + "Request My
  Résumé" (mailto with subject). Footer everywhere: resume line + "Request My Résumé"; nav button "Get in Touch".
