"""Static site generator for the Lauren Gonzalez portfolio.
Usage (from repo root):  python3 _src/build.py
Writes index.html, works.html, about.html, contact.html and work/<slug>.html.
Needs only Python 3 + Pillow (Pillow is used to read image sizes). Images must already be in assets/img/ (see _src/images.py).
The generated HTML is committed, so GitHub Pages serves it with no build step.
"""
import os, re, html, json, sys, hashlib
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import *
from confidentiality import LOG

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def _v(rel): return hashlib.md5(open(os.path.join(ROOT, rel), 'rb').read()).hexdigest()[:8]
IMG = os.path.join(ROOT, 'assets', 'img')
E = lambda s: html.escape(s, quote=False)

def ph(s):
    """Render [[ ]] placeholder brackets muted (text stays visible)."""
    return s.replace('[[', '<span class="ph-t">[[</span>').replace(']]', '<span class="ph-t">]]</span>')
def T(s):
    """Plain copy -> safe HTML with placeholder styling. Strings that already contain tags are trusted as-is."""
    return ph(s if '<' in s else E(s))
def strip_ph(s): return re.sub(r'<[^>]+>', '', s).replace('[[', '').replace(']]', '')

def imgs(slug, prefix):
    d = os.path.join(IMG, slug)
    return sorted(f for f in os.listdir(d) if f.startswith(prefix) and f.endswith('.jpg')) if os.path.isdir(d) else []
def size(rel):
    with Image.open(os.path.join(ROOT, rel)) as im: return im.size
def img(rel, alt, r, cls='', eager=False):
    w, h = size(rel)
    return f'<img src="{r}{rel}" alt="{html.escape(alt)}" width="{w}" height="{h}" decoding="async"{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}>'
def card_img(slug):
    return f'assets/img/{slug}/card.jpg' if os.path.exists(os.path.join(IMG, slug, 'card.jpg')) else f'assets/img/{slug}/hero.jpg'

def head(title, r, desc='Portfolio of Lauren Elyse Gonzalez, graphic designer at Colliers, Portland.'):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{E(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="preload" href="{r}assets/fonts/Geist-Medium.woff2" as="font" type="font/woff2" crossorigin>
<link rel="icon" href="{r}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{r}assets/css/site.css?v={_v('assets/css/site.css')}">
</head><body>
<a class="skip" href="#main">Skip to content</a>
'''
def nav(r, cur=''):
    def l(href, name, key):
        return f'<a class="nav-t" href="{r}{href}"{" aria-current=\"page\"" if key == cur else ""}>{name}</a>'
    return f'''<header class="nav" data-name="Nav"><a class="brand" href="{r}index.html"><b>{SITE_NAME}</b><span class="mono-s muted">{NAV_SUB}</span></a>
<button class="menu-btn mono-s" aria-expanded="false" aria-controls="site-links"><span>Menu</span></button>
<nav class="links" id="site-links">{l("works.html#real-estate","Real Estate","re")}{l("works.html#brand","Brand &amp; Ecommerce","brand")}{l("about.html","About","about")}{l("contact.html","Contact","contact")}<a class="btn sm pri" href="{r}contact.html">Let’s Get to Work <span aria-hidden="true">→</span></a></nav></header>
<main id="main">'''
def btn(t, href, k='pri', arrow='→', extra=''):
    return f'<a class="btn {k}{extra}" href="{href}">{t} <span aria-hidden="true">{arrow}</span></a>'
def footer(r, line=None):
    line = line or CONTACT_LINE
    return f'''</main>
<footer class="foot dark" data-name="Footer CTA">
<div class="g12"><span class="mono muted c1-4">[Contact]</span>
<p class="m c4-13">{T(line)}</p>
<div class="c4-13 btns mt40">{btn("Let’s Get to Work", r+"contact.html", "ond")}{btn(EMAIL, "mailto:"+EMAIL, "sec", "↗", " long")}</div></div>
<a class="big" href="{r}contact.html" aria-label="Contact"><span>Contact</span><span aria-hidden="true">↗</span></a>
<div class="bottom"><a class="mono" href="mailto:{EMAIL}">[Contact] {EMAIL}</a><a class="mono" href="{LINKEDIN}" target="_blank" rel="noopener">[Social] LinkedIn ↗</a><span class="mono muted">©2026 All rights reserved.</span></div></footer>
<script src="{r}assets/js/site.js?v={_v('assets/js/site.js')}"></script>
</body></html>
'''
def write(rel, body):
    p = os.path.join(ROOT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w').write(body); PAGES.append(rel)
PAGES = []
BY = {p['slug']: p for p in ALL}
CAT_LABEL = {'re': 'Real Estate', 'interactive': 'Real Estate · Interactive', 'brand': 'Brand &amp; Ecommerce'}

def short_type(p):
    if p['cat'] == 'brand': return ', '.join(p['service'].split(', ')[:2])
    return p['type']
def card(p, r, ratio='', small=False, src=None):
    sub = f'{T(short_type(p))} · {T(p["place"])}' if p['cat'] != 'brand' else T(short_type(p))
    return f'''<a class="card" href="{r}work/{p["slug"]}.html" data-name="Project Card / {E(p["title"])}"><div class="ph {ratio}">{img(src or card_img(p["slug"]), p["title"]+" — project image", r)}</div>
<div class="meta"><div class="col"><span class="s{' sm' if small else ''}">{E(p["title"])}</span><span class="mono{'-s' if small else ''} muted">{sub}</span></div><span class="mono{'-s' if small else ''}">{T(p["year"])}</span></div></a>'''
def playlist(p, r, link=True):
    ss = imgs(p['slug'], 's')
    ims = ''.join(f'<img src="{r}assets/img/{p["slug"]}/{f}" alt="{E(p["title"])} — screen {i+1}"{" class=\"on\"" if i == 0 else ""} decoding="async">' for i, f in enumerate(ss))
    inner = f'''<div class="scr" data-interval="3200"><div class="scr-in">{ims}</div>
<div class="scr-bar"><span class="mono-s scr-tag">● Auto-playing</span><span class="mono-s scr-n">01 / {len(ss):02d}</span></div><div class="scr-prog"><i></i></div></div>'''
    if not link: return inner
    return f'''<a class="card" href="{r}work/{p["slug"]}.html" data-name="Interactive / {E(p["title"])}">{inner}
<div class="meta mt16"><div class="col"><span class="s">{E(p["title"])}</span><span class="mono muted">{T(p["type"])} · {p["tool"]} · {T(p["place"])}</span></div><span class="mono">{T(p["year"])}</span></div></a>'''

def wordmark():
    s = open(os.path.join(IMG, '..', 'wordmark.svg')).read()
    s = re.sub(r'<\?xml[^>]*\?>', '', s)
    return f'<div class="wordmark" data-name="Wordmark" role="img" aria-label="Lauren Gonzalez">{s.replace("<svg ", "<svg aria-hidden=\"true\" ", 1)}</div>'

# ---------------- HOME ----------------
def home():
    r = ''; H = HOME
    re_home = [p for p in PROJECTS if p.get('home')]
    R = {p['slug']: p for p in re_home}
    brand_home = [p for p in BRAND if p.get('home')]
    b = head('Lauren Gonzalez — Graphic Designer', r) + nav(r) + f'''
<section class="wrap hero" data-name="Hero">
{wordmark()}
<div class="g12 mt64"><div class="c1-4 col"><span class="mono">{E(H["role"])}</span><span class="mono muted" style="margin-top:8px">{E(H["role_place"])}</span></div>
<div class="c4-13 col"><h1 class="l">{T(H["hero"])}</h1>
<p class="bl muted mt32" style="max-width:760px">{T(H["intro"])}</p>
<div class="btns mt40">{btn("Real Estate Work", "#real-estate", "pri", "↓")}{btn("Brand &amp; Ecommerce", "#brand", "sec")}</div></div></div></section>

<section class="wrap" style="padding-bottom:var(--sec)" id="real-estate" data-name="01 Real Estate">
<div class="sec-head clean"><div class="col gap16"><span class="mono muted">[01] ({len(re_home) + 1:02d})</span><h2 class="xl">Real Estate</h2></div>
<p class="bm muted intro">{T(H["re_intro"])}</p></div>
<div class="grid2">{card(R["pdx-west"], r)}{card(R["kress-building"], r)}</div>
<div class="mt64">{card(BY["big-pink"], r, "r169", src="assets/img/big-pink/card-wide.jpg")}</div>
<div class="grid2 mt64">{card(R["the-grid"], r)}{card(R["pacific-center"], r)}</div>
<div class="mt64">{card(R["nomad"], r, "r169")}</div>
<div class="grid2 mt64">{card(R["leftbank"], r)}{card(R["madison-plaza"], r)}</div>
<div class="grid2 mt64">{card(R["springwood"], r)}{card(R["pointe-at-bridgeport"], r)}</div>
<div class="row mt64" style="justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px"><p class="mono-s muted">{T(H["re_note"])}</p>{btn("All Real Estate work", "works.html#real-estate", "sec")}</div>
</section>


<section class="dark wrap sec" data-name="Approach">
<div class="g12"><span class="mono muted c1-4">{T(H["approach_label"])}</span><h2 class="l c4-13">{T(H["approach"])}</h2></div>
<div class="g12 mt64"><div class="c4-13 steps">{"".join(f'<div><span class="mono muted">[{n}]</span><span class="s">{E(t)}</span><span class="bm muted">{T(d)}</span></div>' for n, t, d in H["approach_steps"])}</div></div>
<div class="g12 mt64"><span class="mono muted c1-4">[Expertise]</span><p class="s c4-13">{" · ".join(EXPERTISE)}</p></div></section>

<section class="wrap sec" id="brand" data-name="02 Brand &amp; Ecommerce">
<div class="sec-head clean"><div class="col gap16"><span class="mono muted">[02] ({len(BRAND):02d})</span><h2 class="l">Brand &amp; Ecommerce</h2></div>
<div class="col right" style="gap:20px;align-items:flex-end"><p class="bm muted intro" style="text-align:right">{T(H["brand_intro"])}</p>{btn("See all", "works.html#brand", "sec")}</div></div>
<div class="grid3">{"".join(card(p, r, "r11", small=True) for p in brand_home)}</div></section>

<section class="wrap white sec" data-name="Testimonial"><div class="g12"><span class="mono muted c1-4">[From Clients]</span>
<div class="c4-13 col"><blockquote class="m">“{T(H["testimonial"][0])}”</blockquote>
<div class="col mt40" style="gap:4px"><span class="nav-t">{E(H["testimonial"][1])}</span><span class="mono-s muted">{E(H["testimonial"][2])}</span></div></div></div></section>
''' + footer(r)
    write('index.html', b)

# ---------------- WORKS ----------------
def works():
    r = ''
    b = head('Works — Lauren Gonzalez', r) + nav(r) + f'''
<section class="wrap case-cover" data-name="Works Hero"><span class="mono muted">[Works]</span><h1 class="xxl mt24">Works</h1></section>
<section class="wrap" id="real-estate" style="padding-top:var(--s48)" data-name="Real Estate">
<div class="sec-head clean"><div class="col gap16"><span class="mono muted">[01] ({len(PROJECTS):02d})</span><h2 class="xl">Real Estate</h2></div><p class="bm muted intro">{T(HOME["re_intro"])}</p></div>
<div class="grid2">{"".join(card(p, r) for p in PROJECTS)}</div>
<div class="works-sub" id="interactive"><div class="sec-head clean"><div class="col gap16"><span class="mono muted">[Interactive] ({len(CEROS):02d})</span><h2 class="l">{E(HOME["interactive_title"])}</h2></div><p class="bm muted intro">{T(HOME["interactive_intro"])}</p></div>
<div class="grid2">{"".join(card(p, r) for p in CEROS)}</div></div>
<p class="mono-s muted mt64">{T(HOME["re_note"])}</p></section>
<section class="wrap sec" id="brand" data-name="Brand &amp; Ecommerce">
<div class="sec-head clean"><div class="col gap16"><span class="mono muted">[02] ({len(BRAND):02d})</span><h2 class="xl">Brand &amp; Ecommerce</h2></div><p class="bm muted intro">{T(HOME["brand_intro"])}</p></div>
<div class="grid3">{"".join(card(p, r, "r11", small=True) for p in BRAND)}</div></section>
''' + footer(r)
    write('works.html', b)

# ---------------- ABOUT ----------------
def quote(n, role, q, cls=''):
    return f'<figure class="quote {cls}"><blockquote class="bm">“{T(q)}”</blockquote><figcaption class="col" style="gap:4px"><span class="nav-t">{E(n)}</span><span class="mono-s muted">{E(role)}</span></figcaption></figure>'
def about():
    r = ''; A = ABOUT
    b = head('About — Lauren Gonzalez', r) + nav(r, 'about') + f'''
<section class="wrap case-cover" style="padding-bottom:var(--sec)" data-name="About Hero"><span class="mono muted">[about me]</span>
<h1 class="xxl mt24">About</h1>
<div class="g12 mt96"><div class="c1-6">{img("assets/img/about/portrait.jpg", "Lauren Elyse Gonzalez", r, eager=True)}</div>
<div class="c7-13 col"><p class="s">{T(A["lead"])}</p>
<p class="bl muted mt24">{T(A["body"])}</p>
<p class="bl muted mt24">{T(A["colliers"])}</p>
<div class="mt40">{btn("Let’s Get to Work", "contact.html")}</div></div></div></section>
<section class="dark wrap sec" data-name="Expertise"><div class="g12"><span class="mono muted c1-4">[Expertise]</span><p class="l c4-13">{" · ".join(EXPERTISE)}</p></div></section>
<section class="wrap sec" data-name="From Clients"><div class="sec-head"><h2 class="xl">From Clients</h2><span class="mono muted">({len(TESTIMONIALS):02d})</span></div>
<div class="quotes">{"".join(quote(*t) for t in TESTIMONIALS[:3])}</div>
<div class="quotes two">{"".join(quote(*t) for t in TESTIMONIALS[3:])}</div></section>
<section class="wrap white sec" data-name="Educator"><div class="g12" style="align-items:start">
<div class="c1-7">{img("assets/img/about/educator.jpg", "Lauren teaching", r)}</div>
<div class="c8-13 col"><span class="mono muted">[2019-2025]</span><h2 class="l mt16">Educator</h2><p class="bm mt32">{T(A["educator"])}</p></div></div>
<div class="sec-head mt96"><h3 class="m">From Students</h3><span class="mono muted">(03 of 08)</span></div>
<div class="quotes">{"".join(quote(*t, cls="paper") for t in STUDENTS)}</div></section>
''' + footer(r)
    write('about.html', b)

# ---------------- CONTACT ----------------
def contact():
    r = ''
    b = head('Contact — Lauren Gonzalez', r) + nav(r, 'contact') + f'''
<section class="wrap case-cover" style="padding-bottom:var(--sec)" data-name="Contact Hero"><span class="mono muted">[Contact]</span>
<h1 class="xxl mt24">Let’s Get<br>to Work</h1>
<div class="g12 mt96"><p class="l c1-8">{T(CONTACT_LINE)}</p>
<div class="c9-13 col contact-list">
<div><span class="mono-s muted">[Contact]</span><a class="s" href="mailto:{EMAIL}" style="word-break:break-all">{EMAIL}</a></div>
<div><span class="mono-s muted">[Social]</span><a class="s" href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn ↗</a></div>
<div><span class="mono-s muted">[Expertise]</span><span class="bm">{" · ".join(EXPERTISE)}</span></div></div></div>
<p class="mono-s muted mt64">{ph("[[Placeholder: a contact form can be added later (GitHub Pages is static — it needs a form service such as Formspree). Until then, email is the contact method.]]")}</p></section>
''' + footer(r, EMAIL)
    write('contact.html', b)

# ---------------- CASE PAGES ----------------
# ---------------- CASE PAGES ----------------
# Template = Figma page "01 Rebuild (current site)", frame 7:2 "Case Study – Aafayaa" (Lauren's live Webflow case page):
#   full-bleed hero (630 desktop / 360 mobile) → grey info section (text cols 2–4, meta cols 6–8, 128px top+bottom)
#   → white gallery section (cols 2–7, 128px top+bottom, 24px gaps, no captions) → grey Next Project (80px) → footer.
def pic(rel, alt, r, flex=None):
    st = f' style="flex:{flex:.4f} 1 0"' if flex else ''
    return f'<figure class="pic"{st}>{img(rel, alt, r)}</figure>'
# Fixed row layouts taken from the original Figma case frames (index lists into the gallery files; optional row class)
FIG_ROWS = {
    # Figma 12:2 "Case Study – Wild Naturals · Desktop 1440": 1002-wide column — full 1002x899 · pair 489x489 · full 1002x665 ·
    # pair 489x355 (set 40px into 455-tall frames) · full 1002x452 · full 1002x256 · full 1002x709
    'wild-naturals': [([0], ''), ([1, 2], ''), ([3], ''), ([4, 5], 'g-inset'), ([6], ''), ([7], ''), ([8], '')],
}
def gallery(slug, files, r, title, portrait_three=True, wide_at=1.9):
    """Rows: wide images full width; others in pairs (triples for portrait/square sets). Items in a row share one height."""
    sizes = [size(f'assets/img/{slug}/{f}') for f in files]
    if slug in FIG_ROWS and sum(len(x) for x, _ in FIG_ROWS[slug]) == len(files):
        out = ''.join(f'<div class="g-row{" " + c if c else ""}">' + ''.join(pic(f'assets/img/{slug}/{files[i]}', f'{title} — image {i+1}', r, sizes[i][0] / sizes[i][1]) for i in row) + '</div>' for row, c in FIG_ROWS[slug])
        return f'<div class="gallery">{out}</div>'

    portrait = portrait_three and sum(1 for w, h in sizes if h > w * 1.05) > len(sizes) / 2
    per = 3 if portrait else 2
    rows, cur = [], []
    for i, (w, h) in enumerate(sizes):
        wide = (not portrait) and (w / h > wide_at or (i == 0 and w / h > 1.2))
        if wide:
            if cur: rows.append(cur); cur = []
            rows.append([i])
        else:
            cur.append(i)
            if len(cur) == per: rows.append(cur); cur = []
    if cur:
        if len(cur) == 1 and rows and len(rows[-1]) == 2 and per == 2 and sizes[cur[0]][0] / sizes[cur[0]][1] < 1.2:
            rows[-1].append(cur[0])
        else:
            rows.append(cur)
    out = ''
    for row in rows:
        out += '<div class="g-row">' + ''.join(pic(f'assets/img/{slug}/{files[i]}', f'{title} — image {i+1}', r, sizes[i][0] / sizes[i][1]) for i in row) + '</div>'
    return f'<div class="gallery">{out}</div>'
def first_sentence(s):
    m = re.match(r'(.+?[.!?])(\s|$)', s); return m.group(1) if m else s
def meta_items(p):
    if p['cat'] == 'brand' or p['slug'] == 'fortis-net-lease':
        return [('Client', p['client']), ('Industry', p['industry']), ('Service', p['service']), ('Year', p['year'])]
    if p['cat'] == 'interactive':
        return [('Client', p['client']), ('Type', p['type']), ('Format', p['tool'] + ' interactive presentation'), ('Location', p['place']), ('Year', p['year']), ('Role', p['role'])]
    return [('Client', p['client']), ('Type', p['type']), ('Location', p['place']), ('Year', p['year']), ('Role', p['role'])]
HERO_FIT = {"madison-plaza"}   # mockups on white: show whole image, no crop
def case_head(p, r):
    lab = CAT_LABEL[p['cat']]
    L = len(p['title'])
    tcls = 'case-title' + ('' if L <= 6 else ' t2' if L <= 9 else ' t3' if L <= 24 else ' t4')
    summ = T(p["summary"]) if p["cat"] != "brand" and p["slug"] != "fortis-net-lease" else T(first_sentence(p["summary"]))
    return f'''<section class="wrap case-cover" data-name="Case Cover"><div class="row" style="justify-content:space-between;gap:16px"><span class="mono muted">[Case Study] {lab}</span><a class="mono muted" href="{r}works.html">← All Works</a></div>
<div class="g12"><h1 class="{tcls} c1-8">{E(p["title"])}</h1><p class="bl c8-13">{summ}</p></div></section>'''
def meta_row(p):
    return '<section class="wrap case-meta" data-name="Meta"><div class="meta-row">' + ''.join(
        f'<div><span class="mono-s muted">[{k}]</span><span class="bm">{T(v)}</span></div>' for k, v in meta_items(p) if v) + '</div></section>'
def psr(p):
    sol = ''.join(f'<p class="bl">{T(s)}</p>' for s in p['solution'])
    note = f'<p class="mono-s muted draft">{T(p["draft_note"])}</p>' if p.get('draft_note') else ''
    # an empty results string hides the [03] block entirely (Big Pink: a pitch, no outcome to report)
    res = f'''<div class="blk"><div class="lab"><span class="mono muted">[03]</span><span class="s">Results</span></div><div class="txt"><p class="{'m' if len(strip_ph(p['results'])) < 220 else 's'}">{T(p["results"])}</p></div></div>''' if p['results'].strip() else ''
    return f'''<section class="dark psr" data-name="Project / Solution / Results">{note}
<div class="blk"><div class="lab"><span class="mono muted">[01]</span><span class="s">Project</span></div><div class="txt"><p class="s">{T(p["project"])}</p></div></div>
<div class="blk"><div class="lab"><span class="mono muted">[02]</span><span class="s">Solution</span></div><div class="txt">{sol}</div></div>
{res}</section>'''
def gsec(inner, head='', intro='', note='', aid=''):
    h = f'<div class="g-head"><h2 class="ci-h">{head}</h2>{f"<p class={chr(34)}bm muted{chr(34)}>{T(intro)}</p>" if intro else ""}</div>' if head else ''
    n = f'<p class="mono-s muted g-note">{T(note)}</p>' if note else ''
    return f'<div class="g-block"{f" id={chr(34)}{aid}{chr(34)}" if aid else ""}>{h}{inner}{n}</div>'
def next_block(p, r):
    i = ALL.index(p); nx = ALL[(i + 1) % len(ALL)]
    return f'''<section class="case-next" data-name="Next Project"><div class="wrap cg8">
<div class="cn-head"><h2 class="cn-title">Next Project</h2>{btn("All Works", r+"works.html", "sec sm")}</div>
<a class="cn-card" href="{r}work/{nx["slug"]}.html"><div class="ph">{img(card_img(nx["slug"]), nx["title"], r)}</div>
<div class="cn-meta"><span class="mono-s">{E(nx["title"])}</span><span class="mono-s">{T(nx["year"])}</span></div></a>
</div></section>'''

NOMAD_PAL = [('Signal Red', '#FF343B'), ('Orange', '#FF7B21'), ('Sun Yellow', '#FFC55E'), ('Charcoal', '#3C3839'), ('White', '#FFFFFF')]
FLIP_ALTS = ['Cover', '01 Investment Summary', '01 Investment Summary', '02 Property Description', '02 Property Description', 'Site plan', 'Community amenities', 'Apartment amenities', 'Apartment amenities', 'Floor plans', 'Floor plans', '03 Market Overview', '03 Market Overview', 'Access map', 'Market supply chart', '04 The Comparables', '04 The Comparables']
def nomad_blocks(r):
    I = 'assets/img/nomad/'
    def row(*fs): 
        return '<div class="g-row">' + ''.join(pic(I + f, a, r, size(I + f)[0] / size(I + f)[1]) for f, a in fs) + '</div>'
    sw = ''.join(f'<div class="col gap8"><div class="sw" style="background:{h}"></div><span class="mono-s">{n}</span><span class="mono-s muted">{h}</span></div>' for n, h in NOMAD_PAL)
    pages = ''.join(f'<div class="fb-page"{" data-density=\"hard\"" if i == 0 else ""}><img alt="Nomad offering package — {a}" src="{r}{I}flip/f{i:02d}.jpg" draggable="false"></div>' for i, a in enumerate(FLIP_ALTS))
    pages += '<div class="fb-page fb-end" data-density="hard"><div class="fb-endin"><span class="mono">[End]</span><div><div class="fb-endt">Nomad</div><div class="mono" style="margin-top:14px">Investor Offering Package · 2026</div></div><span class="mono fb-endm">Colliers · Overlook, North Portland — selected pages; confidential pages omitted</span></div></div>'
    hint = '<span class="hd">Drag a page corner, click a page, or use the <span class="kb">←</span> <span class="kb">→</span> keys</span><span class="hm">Swipe the page, drag a corner past the edge, or tap the arrows</span>'
    ds = f'''<div class="gallery"><div class="swatches">{sw}</div>
</div>'''
    book = f'''<div class="fb-stage" data-name="Flip-book"><div class="fb-wrap"><div id="fb-book" class="fb-book">{pages}</div></div>
<div class="fb-controls"><button class="fb-btn" id="fb-prev" aria-label="Previous page">←</button><span class="mono fb-counter" id="fb-counter" aria-live="polite">Cover</span><button class="fb-btn" id="fb-next" aria-label="Next page">→</button></div>
<div class="fb-foot"><span class="mono-s muted fb-hint">{hint}</span></div></div>'''
    return (gsec(ds, 'Design system', 'Palette sampled from the printed pages.')
            + gsec(f'<div class="gallery">{row(("n02.jpg", "Cover: property photography, NOMAD wordmark, hatch border"), ("n03.jpg", "Printed offering packages, ready for investor tours"))}</div>', 'The printed book')
            + gsec(book, 'Inside the book', 'The reading sequence as an investor meets it — chapter openers, amenities, floor plans, maps and market data. Turn the pages.', LOG["nomad"]["note"])
            + gsec(f'<div class="gallery">{row(("n06.jpg", "Neighborhood amenities map, shown on screen"), ("n08.jpg", "Detail: market supply chart in the document palette"))}</div>', 'Maps &amp; data', 'Beyond the page: the neighborhood map on screen, and a close look at a chart drawn in the document palette.'))

MADISON_PAL = [('Raspberry', '#B0144A'), ('Crimson', '#A41D41'), ('Plum Charcoal', '#37272C'), ('Warm Grey', '#ACA5A8'), ('White', '#FFFFFF')]
def madison_blocks(r):
    I = 'assets/img/madison-plaza/'
    def row(*fs):
        return '<div class="g-row">' + ''.join(pic(I + f, a, r, size(I + f)[0] / size(I + f)[1]) for f, a in fs) + '</div>'
    seq = json.load(open(os.path.join(ROOT, '_src', 'madison_flip.json')))
    pages = ''
    k = 0
    for i, e in enumerate(seq):
        hard = ' data-density="hard"' if i in (0, len(seq) - 1) else ''
        if e == 'BLACK':
            side = 'l' if k == 0 else 'r'; k += 1
            if side == 'l':
                txt = '<span class="fb-conft">Confidential —<span class="po"> financial information omitted</span></span>'
            else:
                txt = '<span class="fb-conft la">financial information omitted</span><span class="mono-s fb-confm po">[03] The Financials · pages 24–33</span>'
            pages += f'<div class="fb-page fb-conf fb-conf-{side}"><div class="fb-confin">{txt}</div></div>'
        else:
            tag, f = e.split(':')
            alt = {'cover': 'Front cover', 'back': 'Back cover'}.get(tag, 'Page ' + tag[1:])
            pages += f'<div class="fb-page"{hard}><img alt="Madison Plaza offering memorandum — {alt}" src="{r}{I}flip/{f}" draggable="false"></div>'
    hint = '<span class="hd">Drag a page corner, click a page, or use the <span class="kb">←</span> <span class="kb">→</span> keys</span><span class="hm">Swipe the page, drag a corner past the edge, or tap the arrows</span>'
    sw = ''.join(f'<div class="col gap8"><div class="sw" style="background:{h}"></div><span class="mono-s">{n}</span><span class="mono-s muted">{h}</span></div>' for n, h in MADISON_PAL)
    ds = f'<div class="gallery"><div class="swatches">{sw}</div></div>'
    book = f"""<div class="fb-stage" data-name="Flip-book"><div class="fb-wrap"><div id="fb-book" class="fb-book">{pages}</div></div>
<div class="fb-controls"><button class="fb-btn" id="fb-prev" aria-label="Previous page">←</button><span class="mono fb-counter" id="fb-counter" aria-live="polite">Cover</span><button class="fb-btn" id="fb-next" aria-label="Next page">→</button></div>
<div class="fb-foot"><span class="mono-s muted fb-hint">{hint}</span></div></div>"""
    return (gsec(ds, 'Design system')
            + gsec(f'<div class="gallery">{row(("book_mockup.jpg", "The printed offering memorandum"))}{row(("book_cover.jpg", "Front cover"), ("book_back.jpg", "Back cover"))}</div>', 'The printed book')
            + gsec(book, 'Inside the book', 'The reading sequence as an investor meets it — executive summary, the property, amenities and floor plans, then the market. Turn the pages.'))

PACIFIC_PAL = [('Navy', '#212B3B'), ('Slate Blue', '#435774'), ('Taupe', '#D7CBC4'), ('Umber', '#583117'), ('White', '#FFFFFF')]
def pacific_blocks(r):
    """Pacific Center (Nov 23): like Nomad/Madison — swatches, the printed brochure, flip-book on the charcoal desk.
    Portrait letter pages: the book is sized from data-w/data-h (850x1100) instead of the landscape default."""
    I = 'assets/img/pacific-center/'
    def row(*fs):
        return '<div class="g-row">' + ''.join(pic(I + f, a, r, size(I + f)[0] / size(I + f)[1]) for f, a in fs) + '</div>'
    seq = json.load(open(os.path.join(ROOT, '_src', 'pacific_flip.json')))
    pages = ''
    for i, e in enumerate(seq):
        tag, f = e.split(':')
        hard = ' data-density="hard"' if i in (0, len(seq) - 1) else ''
        alt = {'cover': 'Front cover', 'back': 'Back cover'}.get(tag, 'Page ' + tag[1:])
        num = {'cover': '01', 'back': '12'}[tag] if tag in ('cover', 'back') else f'{int(tag[1:]):02d}'
        pages += f'<div class="fb-page" data-pg="{num}"{hard}><img alt="Pacific Center leasing brochure — {alt}" src="{r}{I}flip/{f}" draggable="false"></div>'
    hint = '<span class="hd">Drag a page corner, click a page, or use the <span class="kb">←</span> <span class="kb">→</span> keys</span><span class="hm">Swipe the page, drag a corner past the edge, or tap the arrows</span>'
    sw = ''.join(f'<div class="col gap8"><div class="sw" style="background:{h}"></div><span class="mono-s">{n}</span><span class="mono-s muted">{h}</span></div>' for n, h in PACIFIC_PAL)
    ds = f'<div class="gallery"><div class="swatches">{sw}</div></div>'
    book = f"""<div class="fb-stage" data-name="Flip-book"><div class="fb-wrap tall"><div id="fb-book" class="fb-book" data-w="850" data-h="1100" data-total="12">{pages}</div></div>
<div class="fb-controls"><button class="fb-btn" id="fb-prev" aria-label="Previous page">←</button><span class="mono fb-counter" id="fb-counter" aria-live="polite">Cover</span><button class="fb-btn" id="fb-next" aria-label="Next page">→</button></div>
<div class="fb-foot"><span class="mono-s muted fb-hint">{hint}</span></div></div>"""
    return (gsec(ds, 'Design system')
            + gsec(f'<div class="gallery">{row(("book_mockup.jpg", "The printed leasing brochure, open on a table"))}{row(("book_cover.jpg", "Front cover"), ("book_back.jpg", "Back cover"))}</div>', 'The printed brochure')
            + gsec(book, 'Inside the brochure', 'The reading sequence as a prospective tenant meets it — the building and its downtown setting, amenities, highlights, the neighborhood, then availabilities. Turn the pages.'))

# Sheet stack (flyers): loose sheets on the desk; reusable — sheet_stack(slug, title, n, r)
SHEET_JITTER = [(-1.6, -10, 6), (1.2, 12, -8), (-0.6, -4, -12), (2.0, 8, 10), (-2.2, -14, 2), (0.8, 4, 12), (-1.0, 10, -4), (1.6, -8, 8)]
def sheet_stack(slug, title, n, r, note=''):
    I = f'assets/img/{slug}/sheets/'
    sh = ''.join(f'<figure class="ss-sheet" style="--r:{SHEET_JITTER[i % 8][0]}deg;--x:{SHEET_JITTER[i % 8][1]}px;--y:{SHEET_JITTER[i % 8][2]}px;z-index:{n - i}"><img src="{r}{I}s{i+1:02d}.jpg" alt="{E(title)} flyer — sheet {i+1}" width="2000" height="1545" draggable="false"></figure>' for i in range(n))
    hint = '<span class="hd">Click or drag the top sheet, or use the <span class="kb">←</span> <span class="kb">→</span> keys</span><span class="hm">Swipe the sheet or tap the arrows</span>'
    return f"""<div class="fb-stage ss-stage" data-name="Sheet stack"><div class="ss-wrap"><div class="ss" tabindex="0" role="group" aria-roledescription="sheet stack" aria-label="{E(title)} flyer sheets">{sh}</div></div>
<div class="fb-controls"><button class="fb-btn ss-prev" aria-label="Previous sheet">←</button><span class="mono fb-counter ss-counter" aria-live="polite">Sheet 01 / {n:02d}</span><button class="fb-btn ss-next" aria-label="Next sheet">→</button></div>
<div class="fb-foot"><span class="mono-s muted fb-hint">{hint}</span></div>{f'<p class="mono-s ss-note">{T(note)}</p>' if note else ''}</div>"""
# iPad viewer (digital brochures, Nov 23): a CSS-drawn iPad Pro (landscape) on the shared cream; pages slide like a tablet.
# Reusable: ipad_viewer(slug, title, files, r, note). JS in site.js (".tab-stage"); CSS "iPad viewer" block in site.css.
def ipad_viewer(slug, title, files, r, note='', label='digital brochure', device='ipad'):
    """files: image names under assets/img/<slug>/, or ('CONF', section) for a black 'Confidential — financial
    information omitted' screen (Madison pattern)."""
    n = len(files)
    def page(i, f):
        hid = '' if i == 0 else ' aria-hidden="true"'
        if isinstance(f, tuple):
            return (f'<figure class="tab-page tab-conf" role="group" aria-roledescription="page" aria-label="Page {i+1} of {n}: confidential, financial information omitted"{hid}>'
                    f'<div class="tab-confin"><span class="tab-conft">Confidential —<br>financial information omitted</span><span class="mono-s tab-confm">{E(f[1])}</span></div></figure>')
        att = 'src' if i < 2 else 'data-src'
        return (f'<figure class="tab-page{" cur" if i == 0 else ""}" role="group" aria-roledescription="page" aria-label="Page {i+1} of {n}"{hid}>'
                f'<img {att}="{r}assets/img/{slug}/{f}" alt="{E(title)} {label} — page {i+1}" draggable="false"></figure>')
    pages = ''.join(page(i, f) for i, f in enumerate(files))
    dots = ''.join('<i class="on"></i>' if i == 0 else '<i></i>' for i in range(n))
    hint = '<span class="hd">Swipe or drag the page, click its edge, or use the <span class="kb">←</span> <span class="kb">→</span> keys</span><span class="hm">Swipe the screen or tap the arrows</span>'
    lap = device == 'laptop'
    if lap: hint = '<span class="hd">Click through it like the live presentation — drag, click the screen’s edge, or use the <span class="kb">←</span> <span class="kb">→</span> keys</span><span class="hm">Swipe the screen or tap the arrows</span>'
    base = '<div class="lap-base" aria-hidden="true"><i></i></div>' if lap else ''
    return f"""<div class="tab-stage{' lap-stage' if lap else ''}" data-name="{'Laptop' if lap else 'iPad'} viewer"><div class="tab-wrap{' lap' if lap else ''}"><div class="tab"><div class="tab-glass"><span class="tab-cam" aria-hidden="true"></span>
<div class="tab-screen" tabindex="0" role="region" aria-roledescription="carousel" aria-label="{E(title)} {label}, {n} pages"><div class="tab-track">{pages}</div></div></div></div>{base}</div>
<div class="tab-controls"><button class="tab-btn tab-prev" aria-label="Previous page" disabled>←</button><span class="mono tab-counter" aria-live="polite">Page 01 / {n:02d}</span><button class="tab-btn tab-next" aria-label="Next page">→</button></div>
<div class="tab-dots" aria-hidden="true">{dots}</div>
<div class="tab-foot"><span class="mono-s tab-hint">{hint}</span></div>{f'<p class="mono-s tab-note">{T(note)}</p>' if note else ''}</div>"""

def swatches(pal):
    sw = ''.join(f'<div class="col gap8"><div class="sw" style="background:{h}"></div><span class="mono-s">{n}</span><span class="mono-s muted">{h}</span></div>' for n, h in pal)
    return f'<div class="gallery"><div class="swatches">{sw}</div></div>'
def img_rows(slug, rows, r):
    I = f'assets/img/{slug}/'
    return '<div class="gallery">' + ''.join('<div class="g-row">' + ''.join(pic(I + f, a, r, size(I + f)[0] / size(I + f)[1]) for f, a in row) + '</div>' for row in rows) + '</div>'

KRESS_PAL = [('Kress Green', '#002B29'), ('Rust', '#B45832'), ('Sand', '#C6AC8A'), ('Parchment', '#FBF5EC'), ('White', '#FFFFFF')]
SPRINGWOOD_PAL = [('Charcoal', '#2C3132'), ('Deep Teal', '#285D64'), ('Teal', '#347179'), ('Mist', '#F8F5F8'), ('White', '#FFFFFF')]
def kress_blocks(r):
    files = [f'p{i:02d}.jpg' for i in range(1, 11)]
    return (gsec(swatches(KRESS_PAL), 'Design system')
            + gsec(img_rows('kress-building', [[('p01.jpg', 'Front cover'), ('p10.jpg', 'Back cover')]], r), 'The brochure')
            + gsec(ipad_viewer('kress-building', 'Kress Building', files, r, LOG['kress-building']['note']), 'Inside the brochure',
                   'Ten pages, in the order a tenant tours the building — the landmark and its renovation, the street, the neighborhood and the parking, the office design, then the floor plans. Swipe through them on the iPad.'))
def springwood_blocks(r):
    # p01..p19 = PDF pages 1-13, 16, 18-22 (see images.py); PDF 14-15 financials and 17 rent comps are replaced by black screens
    f = [f'p{i:02d}.jpg' for i in range(1, 20)]
    files = f[:13] + [('CONF', '[03] Financial Overview · pages 14–15')] + f[13:14] + [('CONF', '[04] Market Comparables · page 17')] + f[14:]
    return (gsec(swatches(SPRINGWOOD_PAL), 'Design system')
            + gsec(img_rows('springwood', [[('p01.jpg', 'Front cover'), ('p19.jpg', 'Back cover')]], r), 'The offering memorandum')
            + gsec(ipad_viewer('springwood', 'Springwood of Beaverton', files, r, LOG['springwood']['note'], 'offering memorandum'), 'Inside the memorandum',
                   'The memorandum as an investor reads it — executive summary, property overview, then the location. The financial overview and the rent comparables stay confidential. Swipe through it on the iPad.'))

LEFTBANK_PAL = [('Burnt Orange', '#CB5625'), ('Black', '#000000'), ('Leaf Green', '#50B848'), ('Map Grey', '#ECEBF0'), ('White', '#FFFFFF')]
def leftbank_blocks(r):
    I = 'assets/img/leftbank/'
    def row(*fs):
        return '<div class="g-row">' + ''.join(pic(I + f, a, r, size(I + f)[0] / size(I + f)[1]) for f, a in fs) + '</div>'
    sw = ''.join(f'<div class="col gap8"><div class="sw" style="background:{h}"></div><span class="mono-s">{n}</span><span class="mono-s muted">{h}</span></div>' for n, h in LEFTBANK_PAL)
    return (gsec(f'<div class="gallery"><div class="swatches">{sw}</div></div>', 'Design system')
            + gsec(f'<div class="gallery">{row(("sheets/s01.jpg", "Front page"), ("sheets/s07.jpg", "Back page"))}</div>', 'The brochure')
            + gsec(ipad_viewer('leftbank', 'The Leftbank Project', [f'sheets/s{i:02d}.jpg' for i in range(1, 8)], r, LOG['leftbank']['note']), 'Inside the brochure', 'Seven pages, in the order a prospective tenant reads them — the building, its history, the spaces, the neighborhood and what is changing around it. Swipe through them on the iPad.'))

PDX_PAL = [('Sage', '#76A48E'), ('Slate', '#505F69'), ('Deep Slate', '#374B4E'), ('Mist', '#ECF3F0'), ('White', '#FFFFFF')]
def pdx_blocks(r):
    I = 'assets/img/pdx-west/'
    def row(*fs):
        return '<div class="g-row">' + ''.join(pic(I + f, a, r, size(I + f)[0] / size(I + f)[1]) for f, a in fs) + '</div>'
    sw = ''.join(f'<div class="col gap8"><div class="sw" style="background:{h}"></div><span class="mono-s">{n}</span><span class="mono-s muted">{h}</span></div>' for n, h in PDX_PAL)
    return (gsec(f'<div class="gallery"><div class="swatches">{sw}</div></div>', 'Design system')
            + gsec(f'<div class="gallery">{row(("mock_spread.jpg", "Three inside pages of the brochure fanned out on a table"), ("mock_cover.jpg", "The brochure cover, with a second page underneath"))}{row(("sheets/s01.jpg", "Front page"), ("sheets/s07.jpg", "Back page"))}</div>', 'The brochure')
            + gsec(ipad_viewer('pdx-west', 'PDX West Logistics Center', [f'sheets/s{i:02d}.jpg' for i in range(1, 8)], r, LOG['pdx-west']['note']), 'Inside the brochure', 'Seven pages, in the order a tenant or broker reads them — the building, its specifications and site plan, the submarket, then access, workforce and reach. Swipe through them on the iPad.'))

def case(p):
    r = '../'; s = p['slug']
    body = case_head(p, r)
    if False:
        pass
    else:
        body += f'<div class="case-hero{" fit" if s in HERO_FIT and os.path.exists(f"/workspace/lauren-case-studies/mockups/{s}_hero-override.jpg") else ""}" data-name="Hero Mockup">{img(f"assets/img/{s}/hero.jpg", p["title"]+" — hero mockup", r, eager=True)}</div>'
    body += meta_row(p) + psr(p)
    if s == 'nomad':
        g = nomad_blocks(r)
    elif s == 'madison-plaza':
        g = madison_blocks(r)
    elif s == 'kress-building':
        g = kress_blocks(r)
    elif s == 'springwood':
        g = springwood_blocks(r)
    elif s == 'pacific-center':
        g = pacific_blocks(r)
    elif s == 'leftbank':
        g = leftbank_blocks(r)
    elif s == 'pdx-west':
        g = pdx_blocks(r)
    elif s == 'big-pink':
        import bigpink_blocks; g = bigpink_blocks.blocks(r, gsec, swatches, img_rows, ipad_viewer)
    elif s == 'marketplace':
        g = gsec(ipad_viewer('marketplace', 'Marketplace I & II', [f'scr/s{i:02d}.jpg' for i in range(1, 10)], r, p['note'], 'Ceros presentation', 'laptop'), 'The presentation',
                 'Selected design screens from the Ceros pitch — introductions, market overview, competition, case studies and approach. Click through them on the laptop.')
    elif s == 'the-grid':
        import grid_blocks; g = grid_blocks.grid_blocks(r, gsec, swatches, img_rows)
    elif p['cat'] == 're' and s != 'fortis-net-lease':
        g = gsec(gallery(s, imgs(s, 'p'), r, p['title']), E(p['pages_title']), p['pages_intro'], LOG[s]['note'])
    elif p['cat'] == 'interactive':
        g = gsec(gallery(s, imgs(s, 's'), r, p['title']), 'Selected screens', '', p['note'])
    else:
        g = gsec(gallery(s, imgs(s, 'g'), r, p['title'], wide_at=1.2), '', '', LOG.get(s, {}).get('note', ''))
    body += f'<section class="case-gallery white" data-name="Gallery"><div class="wrap cg8"><div class="cg-col">{g}</div></div></section>'
    body += next_block(p, r)
    extra_js = '<script src="../assets/js/page-flip.browser.js"></script>\n' if s in ('nomad', 'madison-plaza', 'pacific-center') else ''
    page = head(f'{strip_ph(p["title"])} — Case Study — Lauren Gonzalez', r, strip_ph(first_sentence(p['summary']))) + nav(r, 'brand' if p['cat'] == 'brand' else 're') + body + footer(r)
    page = page.replace(f'<script src="{r}assets/js/site.js', extra_js + f'<script src="{r}assets/js/site.js')
    write(f'work/{s}.html', page)

if __name__ == '__main__':
    home(); works(); about(); contact()
    for p in ALL: case(p)
    md = ['# Confidentiality log (generated by _src/build.py from _src/confidentiality.py)\n',
          'Rule: leave anything confidential out; if leaving it out would look bad, blur it. The site is PUBLIC (GitHub Pages), marked noindex.\n\n**Updated rule (Rodrigo, Nov 23):** "Anything in the front pages is not confidential. Confidential means financials." Covers, thumbnails and hero mockups are shown unblurred (contacts, headlines, addresses, broker strips). Only financial data (pricing, rents, rent comps, operating figures, taxes, deal financials such as Madison section 03) stays blurred or omitted. Interior pages blurred only for contacts are listed below and wait for confirmation.\n']
    from content import UNPUBLISHED
    for slug, d in LOG.items():
        if slug in UNPUBLISHED: continue
        md.append(f"## {BY[slug]['title'] if slug in BY else slug}\n")
        md.append('- **Blurred:** ' + ('; '.join(d.get('blurred') or []) or 'nothing') )
        md.append('- **Omitted:** ' + ('; '.join(d.get('omitted') or []) or 'nothing') + '\n')
    md.append('## Brand & Ecommerce (Aafayaa, Abundant Earth, Wild Naturals, TokSuite, Farm & Bee, Zulay Kitchen, CGK Unlimited)\n')
    md.append('- Images and copy as already published on Lauren’s live Webflow site; visually checked — no prices, phones, emails or contacts.\n')
    md.append('## Removed from the site (Nov 23, Rodrigo)\n')
    md.append('- Redmond Gateway, Portland Office Market Report and Marketplace I & II (removed Nov 23 PM): no page, card or link; source entries kept in _src (content.UNPUBLISHED), images not generated.\n')
    md.append('## Projects not on the site (confidential / excluded)\n')
    md.append('- The Galt (BOV), 8210 Mauzey Court, Fruit Valley, Pomeroy, Overland AI, W+K timeline, American Brush / REMS, Houghton RFQ; Apex skipped.\n')
    open(os.path.join(ROOT, 'CONFIDENTIALITY.md'), 'w').write('\n'.join(md))
    json.dump(PAGES, open(os.path.join(ROOT, '_src', 'pages.json'), 'w'), indent=1)
    print(len(PAGES), 'pages written')
