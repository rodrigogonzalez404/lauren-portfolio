# Lauren Gonzalez — Portfolio (static site)

Portfolio of Lauren Elyse Gonzalez, graphic designer at Colliers (Portland). Real Estate work leads; Brand & Ecommerce follows.

**Plain HTML/CSS/JS. No build step is needed to view or host it.** Open `index.html` locally, or serve the folder with GitHub Pages.
All links are relative, so it works at `https://<user>.github.io/<repo>/`.

> The site is public but asks search engines not to index it (`noindex, nofollow` meta on every page + `robots.txt` disallow all).

## Structure

```
index.html            Home (hero, Real Estate grid, Interactive playlist, Approach, Brand & Ecommerce, testimonial)
works.html            All projects (Real Estate, Interactive, Brand & Ecommerce)
about.html            About
contact.html          Contact
work/<slug>.html      One case-study page per project (21 pages)
assets/css/site.css   The one shared, responsive stylesheet
assets/js/site.js     Mobile menu, auto-playing screen playlists, flip-book init
assets/js/page-flip.browser.js   StPageFlip 2.0.7 (MIT) — Nomad flip-book only
assets/fonts/         Geist + PT Mono
assets/img/<slug>/    Web-optimized images (≤2400px, JPEG q80)
assets/wordmark.svg   Hero wordmark
_src/                 Generator + content (optional; only needed to regenerate pages)
CONFIDENTIALITY.md    What was blurred or left out, per project
AI-HANDOFF.md         Notes for Claude / ChatGPT / any assistant continuing the work
```

## Editing

Two ways — both are fine:

1. **Edit the HTML directly.** Every page is readable hand-editable HTML. Good for quick text fixes.
2. **Edit `_src/content.py`, then run `python3 _src/build.py`** (needs Python 3 + Pillow: `pip install pillow`). This regenerates all pages consistently. Note: it overwrites hand edits to generated pages.

### Swap a mockup / image
Images use stable file names, so you can replace a file without touching HTML:

- `assets/img/<slug>/hero.jpg` — the main mockup on the case page (and the card image if there is no `card.jpg`)
- `assets/img/<slug>/card.jpg` — optional thumbnail used on Home / Works
- `assets/img/<slug>/p01.jpg, p02.jpg…` — document pages (Real Estate)
- `assets/img/<slug>/g01.jpg…` — gallery images (Brand)
- `assets/img/<slug>/s01.jpg…` — screens (Interactive / Ceros)
- `assets/img/nomad/flip/f00.jpg…f16.jpg` — Nomad flip-book pages (cover = f00)

Keep the same name, export at max 2400px on the long side, JPEG quality ~80. If the new image has a different
shape, run `python3 _src/build.py` so the width/height attributes update (or edit them in the HTML).
Adding/removing gallery files: add `p07.jpg` etc. and rebuild — galleries pick up every file with that prefix.

### Add a project
1. Create `assets/img/<new-slug>/` with at least `hero.jpg` (+ `p01.jpg…` or `g01.jpg…`).
2. Add an entry to `PROJECTS` (Real Estate) or `BRAND_ORDER` / `brand_copy.py` (Brand) in `_src/content.py`.
3. For Real Estate, add a line to `LOG` in `_src/confidentiality.py` (what was blurred / omitted).
4. To show it on Home, set `home=True` and place its card in `home()` in `_src/build.py`.
5. Run `python3 _src/build.py`.

## The `[[ ]]` convention
Text inside `[[ ]]` is a **placeholder or unconfirmed** (e.g. `[[Lauren to confirm]]`, `[[Year]]`). It shows on the
page with muted brackets so it is easy to spot. Replace the text and delete the brackets once Lauren approves it.
Copy without brackets is approved (home page copy) or already published on Lauren's live site (brand case studies, Fortis).
Search for open items: `grep -rn "\[\[" _src/content.py`.

## Confidentiality rule
This is a public site. **Leave anything confidential out; if leaving it out would look bad, blur it.**
Never publish: pricing / price guidance, financials, NOI, rent rolls, rent comps, cap rates, fee proposals, broker names/phones/emails,
team photos, references, stacking plans with SF. See `CONFIDENTIALITY.md` for the per-project log. Blurs are baked into
the images (pixelate + heavy blur), produced by `_src/images.py` from the original PDFs (originals are not in this repo).
Ceros presentations are shown only as curated screenshots — no live embeds and no links to the Ceros URLs.

## Hosting on GitHub Pages
Push this folder to a repo → Settings → Pages → *Deploy from a branch* → `main` / root. `.nojekyll` is included so files are served as-is.
