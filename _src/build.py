"""Static site generator for the Lauren Gonzalez portfolio.
Usage (from repo root):  python3 _src/build.py
Writes index.html, works.html, about.html, contact.html and work/<slug>.html.
Needs only Python 3 + Pillow (Pillow is used to read image sizes). Images must already be in assets/img/ (see _src/images.py).
The generated HTML is committed, so GitHub Pages serves it with no build step.
"""
import os, re, html, json, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import *
from confidentiality import LOG

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
<link rel="stylesheet" href="{r}assets/css/site.css">
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
<script src="{r}assets/js/site.js"></script>
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
def card(p, r, ratio='', small=False):
    sub = f'{T(short_type(p))} · {T(p["place"])}' if p['cat'] != 'brand' else T(short_type(p))
    return f'''<a class="card" href="{r}work/{p["slug"]}.html" data-name="Project Card / {E(p["title"])}"><div class="ph {ratio}">{img(card_img(p["slug"]), p["title"]+" — project image", r)}</div>
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
<div class="sec-head clean"><div class="col gap16"><span class="mono muted">[01] ({len(re_home):02d})</span><h2 class="xl">Real Estate</h2></div>
<p class="bm muted intro">{T(H["re_intro"])}</p></div>
<div class="grid2">{card(R["pdx-west"], r)}{card(R["kress-building"], r)}</div>
<div class="mt64">{card(R["nomad"], r, "r169")}</div>
<div class="grid2 mt64">{card(R["the-grid"], r)}{card(R["pacific-center"], r)}</div>
<div class="grid3 mt64">{card(R["leftbank"], r, small=True)}{card(R["madison-plaza"], r, small=True)}{card(R["redmond-gateway"], r, small=True)}</div>
<div class="grid3 mt64">{card(R["springwood"], r, small=True)}{card(R["pointe-at-bridgeport"], r, small=True)}{card(R["portland-office-market-report"], r, small=True)}</div>
<div class="row mt64" style="justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px"><p class="mono-s muted">{T(H["re_note"])}</p>{btn("All Real Estate work", "works.html#real-estate", "sec")}</div>
</section>

<section class="wrap" style="padding-bottom:var(--sec)" id="interactive" data-name="Interactive Presentations">
<div class="sec-head clean"><div class="col gap16"><span class="mono muted">[Interactive] ({len(CEROS):02d})</span><h2 class="l">{E(H["interactive_title"])}</h2></div>
<p class="bm muted intro">{T(H["interactive_intro"])}</p></div>
<div class="grid2">{"".join(playlist(p, r) for p in CEROS)}</div>
<p class="mono-s muted mt40">Pages auto-advance like a playlist; click to open the case study. Only design pages are shown — market data, fees, team and client lists are left out.</p>
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
<div class="grid2">{"".join(playlist(p, r) for p in CEROS)}</div></div>
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
def fig(rel, alt, n, cap, r, cls=''):
    return f'<figure class="fig {cls}">{img(rel, alt, r)}<figcaption class="cap mono-s"><span>[{n:02d}]</span><span>{T(cap)}</span></figcaption></figure>'
def shead(label, title, intro=''):
    return f'<div class="sec-head"><div class="col"><span class="mono muted">[{label}]</span><h2 class="m">{title}</h2></div>{f"<p class={chr(34)}bm muted intro{chr(34)}>{T(intro)}</p>" if intro else ""}</div>'
def auto_gallery(slug, files, r, start, title, portrait_three=True):
    """Nomad rhythm: wide images run full width; the rest sit in rows of two (three for portrait page sets).
    Row items are sized by aspect ratio so every row has one common height — no crops, no holes."""
    n = start
    sizes = [size(f'assets/img/{slug}/{f}') for f in files]
    portrait = portrait_three and sum(1 for w, h in sizes if h > w) > len(sizes) / 2
    per = 3 if portrait else 2
    rows, cur = [], []
    for i, (w, h) in enumerate(sizes):
        wide = (not portrait) and (w / h > 1.9 or (i == 0 and w / h > 1.2))
        if wide:
            if cur: rows.append(cur); cur = []
            rows.append([i])
        else:
            cur.append(i)
            if len(cur) == per: rows.append(cur); cur = []
    if cur:
        # a leftover single image joins the previous partial-free row structure: pair it with the previous row if that was a pair
        if len(cur) == 1 and rows and len(rows[-1]) == per and per == 2 and sizes[cur[0]][0] / sizes[cur[0]][1] < 1.2:
            rows[-1].append(cur[0])
        else:
            rows.append(cur)
    out = []
    for row in rows:
        items = ''
        for i in row:
            w, h = sizes[i]
            fg = fig(f'assets/img/{slug}/{files[i]}', f'{title} — image {i+1}', start + i, f'{title} — {i+1:02d}', r)
            items += fg.replace('<figure class="fig ', f'<figure style="flex:{w/h:.4f} 1 0" class="fig ', 1)
        out.append(f'<div class="g-row{" solo" if len(row) == 1 else ""}">{items}</div>')
    return f'<div class="gallery">{"".join(out)}</div>', start + len(files)

def case_head(p, r):
    lab = CAT_LABEL[p['cat']]
    L = len(p['title'])
    tcls = 'case-title' + ('' if L <= 6 else ' t2' if L <= 9 else ' t3' if L <= 24 else ' t4')
    summ = T(p["summary"]) if p["cat"] != "brand" and p["slug"] != "fortis-net-lease" else T(first_sentence(p["summary"]))
    return f'''<section class="wrap case-cover" data-name="Case Cover"><div class="row" style="justify-content:space-between;gap:16px"><span class="mono muted">[Case Study] {lab}</span><a class="mono muted" href="{r}works.html">← All Works</a></div>
<div class="g12"><h1 class="{tcls} c1-8">{E(p["title"])}</h1><p class="bl c8-13">{summ}</p></div></section>'''
def first_sentence(s):
    m = re.match(r'(.+?[.!?])(\s|$)', s); return m.group(1) if m else s
def meta_row(p):
    if p['cat'] == 'brand' or p['slug'] == 'fortis-net-lease':
        items = [('Client', p['client']), ('Industry', p['industry']), ('Service', p['service']), ('Year', p['year'])]
    elif p['cat'] == 'interactive':
        items = [('Client', p['client']), ('Type', p['type']), ('Format', p['tool'] + ' interactive presentation'), ('Location', p['place']), ('Year', p['year']), ('Role', p['role'])]
    else:
        items = [('Client', p['client']), ('Type', p['type']), ('Location', p['place']), ('Year', p['year']), ('Role', p['role'])]
    return '<section class="wrap case-meta" data-name="Meta"><div class="meta-row">' + ''.join(
        f'<div><span class="mono-s muted">[{k}]</span><span class="bm">{T(v)}</span></div>' for k, v in items if v) + '</div></section>'
def psr(p):
    sol = ''.join(f'<p class="bl">{T(s)}</p>' for s in p['solution'])
    note = f'<p class="mono-s muted draft">{T(p["draft_note"])}</p>' if p.get('draft_note') else ''
    return f'''<section class="dark psr" data-name="Project / Solution / Results">{note}
<div class="blk"><div class="lab"><span class="mono muted">[01]</span><span class="s">Project</span></div><div class="txt"><p class="s">{T(p["project"])}</p></div></div>
<div class="blk"><div class="lab"><span class="mono muted">[02]</span><span class="s">Solution</span></div><div class="txt">{sol}</div></div>
<div class="blk"><div class="lab"><span class="mono muted">[03]</span><span class="s">Results</span></div><div class="txt"><p class="{'m' if len(strip_ph(p['results'])) < 220 else 's'}">{T(p["results"])}</p></div></div></section>'''
def next_block(p, r, bg="white"):
    i = ALL.index(p); nx = ALL[(i + 1) % len(ALL)]
    return f'''<section class="wrap {bg} next" data-name="Next Project"><div class="next-top"><span class="mono muted">[Next Project]</span>{btn("All Works", r+"works.html", "sec")}</div>
<a class="g12" href="{r}work/{nx["slug"]}.html"><div class="c1-7 col"><h2 class="xl">{E(nx["title"])}</h2><span class="mono mt16">{T(short_type(nx))} · {T(nx["year"])} →</span></div><div class="c7-13 ph">{img(card_img(nx["slug"]), nx["title"], r)}</div></a></section>'''

def case(p):
    r = '../'; s = p['slug']
    body = case_head(p, r)
    if p['cat'] == 'interactive':
        body += f'<div class="case-stage" data-name="Hero Playlist">{playlist(p, r, link=False)}</div><div class="wrap cap mono-s"><span>[01]</span><span>Selected screens, auto-playing</span></div>'
    else:
        body += f'<div class="case-hero" data-name="Hero Mockup">{img(f"assets/img/{s}/hero.jpg", p["title"]+" — hero mockup", r, eager=True)}</div><div class="wrap cap mono-s"><span>[01]</span><span>{"Mockup using the original artwork" if p["cat"] == "re" and s != "fortis-net-lease" else E(p["title"])}</span></div>'
    body += meta_row(p) + psr(p)
    if s == 'nomad':
        body += nomad_galleries(r)
    elif p['cat'] == 're' and s != 'fortis-net-lease':
        g, _ = auto_gallery(s, imgs(s, 'p'), r, 2, p['title'])
        body += f'<section class="wrap white sec" data-name="Gallery / Pages">{shead("Gallery 01", E(p["pages_title"]), p["pages_intro"])}{g}<p class="mono-s note">{T(LOG[s]["note"])}</p></section>'
    elif p['cat'] == 'interactive':
        g, _ = auto_gallery(s, imgs(s, 's'), r, 1, p['title'])
        body += f'<section class="wrap white sec" data-name="Gallery / Screens">{shead("Gallery 01", "Selected screens")}{g}<p class="mono-s note">{T(p["note"])}</p></section>'
    else:
        g, _ = auto_gallery(s, imgs(s, 'g'), r, 2, p['title'], portrait_three=False)
        extra = f'<p class="mono-s note">{T(LOG[s]["note"])}</p>' if s in LOG and LOG[s].get('note') else ''
        body += f'<section class="wrap white sec" data-name="Gallery">{shead("Gallery 01", p.get("gallery_title","Selected work"))}{g}{extra}</section>'
    body += next_block(p, r, 'white' if s == 'nomad' else 'paper')
    extra_js = '<script src="../assets/js/page-flip.browser.js"></script>\n' if s == 'nomad' else ''
    page = head(f'{strip_ph(p["title"])} — Case Study — Lauren Gonzalez', r, strip_ph(first_sentence(p['summary']))) + nav(r, 'brand' if p['cat'] == 'brand' else 're') + body + footer(r)
    page = page.replace(f'<script src="{r}assets/js/site.js">', extra_js + f'<script src="{r}assets/js/site.js">')
    write(f'work/{s}.html', page)

NOMAD_PAL = [('Signal Red', '#FF343B'), ('Orange', '#FF7B21'), ('Sun Yellow', '#FFC55E'), ('Charcoal', '#3C3839'), ('White', '#FFFFFF')]
FLIP_ALTS = ['Cover', '01 Investment Summary', '01 Investment Summary', '02 Property Description', '02 Property Description', 'Site plan', 'Community amenities', 'Apartment amenities', 'Apartment amenities', 'Floor plans', 'Floor plans', '03 Market Overview', '03 Market Overview', 'Access map', 'Market supply chart', '04 The Comparables', '04 The Comparables']
def nomad_galleries(r):
    I = 'assets/img/nomad/'
    F = lambda f, cap, n, alt=None: fig(I + f, alt or cap, n, cap, r)
    sw = ''.join(f'<div class="col gap8"><div class="sw" style="background:{h}"></div><span class="mono-s">{n}</span><span class="mono-s muted">{h}</span></div>' for n, h in NOMAD_PAL)
    pages = ''.join(f'<div class="fb-page"{" data-density=\"hard\"" if i == 0 else ""}><img alt="Nomad offering package — {a}" src="{r}{I}flip/f{i:02d}.jpg" draggable="false"></div>' for i, a in enumerate(FLIP_ALTS))
    pages += '<div class="fb-page fb-end" data-density="hard"><div class="fb-endin"><span class="mono">[End]</span><div><div class="fb-endt">Nomad</div><div class="mono" style="margin-top:14px">Investor Offering Package · 2026</div></div><span class="mono fb-endm">Colliers · Overlook, North Portland — selected pages; confidential pages omitted</span></div></div>'
    hint = '<span class="hd">Drag a page corner, click a page, or use the ← → keys</span><span class="hm">Swipe the page, drag a corner past the edge, or tap the arrows</span>'
    return f'''
<section class="wrap white sec" data-name="Design System">{shead("Design system", "Design system", "Palette sampled from the printed pages; typefaces as embedded in the PDF.")}
<div class="swatches">{sw}</div>
<div class="gallery-2 mt96">{F("ds_wordmark.jpg", "Display: heavy italic wordmark", 2)}{F("ds_title-box.jpg", "Headline: orange caps in an outlined title box", 3)}</div>
<div class="col gap8 mt40" style="padding-top:16px;border-top:1px solid var(--ink)"><span class="mono-s muted">[Type]</span><span class="bm">Acumin family (Variable Concept + Pro: Thin → Bold) for display and text, with Expressway, Freight Sans and Apparat in supporting roles.</span></div>
<div class="split-57 mt96">{F("ds_divider-label.jpg", "Chapter tab: oversized red numeral on charcoal", 4)}<div class="split-13">{F("ds_hatch.jpg", "Diagonal hatch accent", 5)}{F("ds_icons.jpg", "Amenity icon set", 6)}</div></div></section>
<section class="wrap sec" data-name="Gallery / The printed book">{shead("Gallery 01", "The printed book")}
<div class="gallery-2">{F("n02.jpg", "Cover: property photography, NOMAD wordmark, hatch border", 7)}{F("n03.jpg", "Printed offering packages, ready for investor tours", 8)}</div></section>
<section class="wrap white sec" data-name="Gallery / Inside the book">{shead("Gallery 02", "Inside the book", "The reading sequence as an investor meets it — chapter openers, amenities, floor plans, maps and market data. Turn the pages.")}
<div class="fb-stage" data-name="Flip-book"><div class="fb-wrap"><div id="fb-book" class="fb-book">{pages}</div></div>
<div class="fb-controls"><button class="fb-btn" id="fb-prev" aria-label="Previous page">←</button><span class="mono fb-counter" id="fb-counter" aria-live="polite">Cover</span><button class="fb-btn" id="fb-next" aria-label="Next page">→</button></div>
<div class="fb-foot"><span class="mono-s muted">[09]</span><span class="mono-s">Interactive flip-book: 16 selected pages of the offering package</span><span class="mono-s muted fb-hint">{hint}</span></div></div>
<p class="mono-s note">{T(LOG["nomad"]["note"])}</p></section>
<section class="wrap sec" data-name="Gallery / Maps &amp; data">{shead("Gallery 03", "Maps &amp; data", "Beyond the page: the neighborhood map on screen, and a close look at a chart drawn in the document palette.")}
<div class="split-57">{F("n06.jpg", "Neighborhood amenities map, shown on screen", 10)}{F("n08.jpg", "Detail: market supply chart in the document palette", 11)}</div></section>'''

if __name__ == '__main__':
    home(); works(); about(); contact()
    for p in ALL: case(p)
    md = ['# Confidentiality log (generated by _src/build.py from _src/confidentiality.py)\n',
          'Rule: leave anything confidential out; if leaving it out would look bad, blur it. The site is PUBLIC (GitHub Pages), marked noindex.\n']
    for slug, d in LOG.items():
        md.append(f"## {BY[slug]['title'] if slug in BY else slug}\n")
        md.append('- **Blurred:** ' + ('; '.join(d.get('blurred') or []) or 'nothing') )
        md.append('- **Omitted:** ' + ('; '.join(d.get('omitted') or []) or 'nothing') + '\n')
    md.append('## Brand & Ecommerce (Aafayaa, Abundant Earth, Wild Naturals, TokSuite, Farm & Bee, Zulay Kitchen, CGK Unlimited)\n')
    md.append('- Images and copy as already published on Lauren’s live Webflow site; visually checked — no prices, phones, emails or contacts.\n')
    md.append('## Projects not on the site (confidential / excluded)\n')
    md.append('- The Galt (BOV), 8210 Mauzey Court, Fruit Valley, Pomeroy, Overland AI, W+K timeline, American Brush / REMS, Houghton RFQ; Apex skipped.\n')
    open(os.path.join(ROOT, 'CONFIDENTIALITY.md'), 'w').write('\n'.join(md))
    json.dump(PAGES, open(os.path.join(ROOT, '_src', 'pages.json'), 'w'), indent=1)
    print(len(PAGES), 'pages written')
