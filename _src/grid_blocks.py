"""The Grid (Kirkland 405) case-study body (Nov 23). Called from build.case(). Logos are inlined as SVG from _src/grid/."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
GRID_VB = (149.25, 241.25, 268.25, 146.5)
SYMBOL_VB = '149.25 241.25 136.2 146.5'
WORD_VB = '305.5 255 114 95'
GRID_PAL = [('Grid Grey', '#777C80'), ('Stone', '#EAE7E3'), ('Silver', '#BABABA'), ('Graphite', '#1D1D1F'), ('White', '#FFFFFF')]

def _inner(name):
    s = open(os.path.join(HERE, 'grid', f'logo-{name}.svg')).read()
    return re.sub(r'(?s)^.*?<svg[^>]*>|</svg>\s*$', '', s).strip()

def logo(name='the-grid', label='The Grid logo', cls='', vb=None):
    s = open(os.path.join(HERE, 'grid', f'logo-{name}.svg')).read()
    v = vb or re.search(r'viewBox="([^"]+)"', s).group(1)
    if vb: cls += ' crop'
    return f'<svg class="gr-logo {cls}" viewBox="{v}" role="img" aria-label="{label}" xmlns="http://www.w3.org/2000/svg">{_inner(name)}</svg>'

def clear_space():
    x0, y0, w, h = GRID_VB; u = h / 4; p = u * 0.9
    X0, Y0, W, H = x0 - u - p, y0 - u - p, w + 2 * (u + p), h + 2 * (u + p)
    def dim(xa, ya, xb, yb, tx, ty):
        t = 2.2; v = xa == xb
        ticks = (f'<line x1="{xa-t}" y1="{ya}" x2="{xa+t}" y2="{ya}" class="d"/><line x1="{xb-t}" y1="{yb}" x2="{xb+t}" y2="{yb}" class="d"/>' if v else
                 f'<line x1="{xa}" y1="{ya-t}" x2="{xa}" y2="{ya+t}" class="d"/><line x1="{xb}" y1="{yb-t}" x2="{xb}" y2="{yb+t}" class="d"/>')
        return (f'<line x1="{xa}" y1="{ya}" x2="{xb}" y2="{yb}" class="d"/>{ticks}'
                f'<text x="{tx}" y="{ty}" class="t">x</text>')
    return f'''<svg class="gr-clear" viewBox="{X0:.2f} {Y0:.2f} {W:.2f} {H:.2f}" role="img" aria-label="The Grid logo with its clear-space zone, one quarter of the logo height on every side" xmlns="http://www.w3.org/2000/svg">
<rect x="{x0-u}" y="{y0-u}" width="{w+2*u}" height="{h+2*u}" class="z"/><rect x="{x0}" y="{y0}" width="{w}" height="{h}" class="in"/>
<rect x="{x0-u}" y="{y0-u}" width="{w+2*u}" height="{h+2*u}" class="out"/>
{dim(x0+w*0.58, y0-u, x0+w*0.58, y0, x0+w*0.58+4, y0-u/2+2.6)}{dim(x0-u, y0+h*0.5, x0, y0+h*0.5, x0-u/2-2.4, y0+h*0.5-4)}
{dim(x0+w, y0+h*0.5, x0+w+u, y0+h*0.5, x0+w+u/2-2.4, y0+h*0.5-4)}{dim(x0+w*0.58, y0+h, x0+w*0.58, y0+h+u, x0+w*0.58+4, y0+h+u/2+2.6)}
<g class="lg">{_inner('the-grid')}</g></svg>'''

def label(t, sub=''):
    sb = f'<span class="mono-s muted">{sub}</span>' if sub else ''
    return f'<div class="gr-lab"><span class="mono-s">{t}</span>{sb}</div>'

def tile(inner, cls, lab, sub=''):
    return f'<div class="gr-cell"><div class="gr-panel {cls}">{inner}</div>{label(lab, sub)}</div>'

CONCEPTS = [
    ('the-grid', 'The Grid', 'Concept 01 · Chosen', ['Connected', 'Tech Infrastructure', 'Urban Energy', 'Startup Ecosystem', 'Seattle Roots'],
     'The Grid is a nod to both the tech infrastructure that powers innovation and the urban connectivity of Seattle. It positions the building as a place where startups stay plugged into the city’s energy, resources, and talent. Whether you’re launching a new idea or scaling up, The Grid is where you stay connected.', None),
    ('stage-one', 'Stage One', 'Concept 02', ['Foundation', 'Growth Platform', 'Startup Journey', 'Performance Space', 'Scalable'],
     'Stage One represents both a starting point and a platform for growth. It’s a place where businesses, whether at their first pitch or their hundredth hire, can thrive. The name also evokes a performance stage, giving tenants a space to shine, present, and lead. It’s aspirational, flexible, and empowering.', 'stage'),
    ('the-pulse', 'The Pulse', 'Concept 03', ['Vitality', 'Innovation Hub', 'Momentum', 'Creative Energy', 'Startup Culture'],
     'The Pulse symbolizes the heartbeat of innovation. It’s where energy flows, ideas spark, and businesses come to life. With its modern finishes and user-focused upgrades, the building becomes more than just a workspace, it’s a living hub for creativity and momentum.', 'pulse'),
]

def grid_blocks(r, gsec, swatches, img_rows):
    I = 'assets/img/the-grid/'
    mark = (tile(clear_space(), 'white bordered gr-wide', 'Clear space', 'x = ¼ of the logo height on every side')
            + '<div class="gr-two">'
            + tile(logo(label='The Grid symbol', cls='w34', vb=SYMBOL_VB), 'grey on-dark', 'Symbol', 'The two frames, used alone')
            + tile(logo(label='The Grid wordmark', cls='w58', vb=WORD_VB), 'stone', 'Wordmark', 'Custom lettering — light, geometric, open')
            + '</div>')
    var = ('<div class="gr-two">'
           + tile(logo(cls='w62'), 'stone', 'Primary', 'Grid Grey on Stone')
           + tile(logo(cls='w62'), 'graphite on-dark', 'Reversed', 'White on Graphite')
           + tile(logo(cls='w62'), 'white bordered ink', 'One colour', 'Black on white')
           + tile(logo(cls='w62'), 'grey on-dark', 'On colour', 'White on Grid Grey')
           + '</div>'
           + tile('<div class="gr-avs">' + ''.join(f'<span class="gr-av" style="width:{s}px;height:{s}px">{logo(label="The Grid avatar", vb=SYMBOL_VB)}</span>' for s in (168, 112, 72, 44, 28)) + '</div>',
                  'white bordered gr-avpanel', 'Avatar &amp; favicon', 'The symbol in a circle, from profile image to browser tab'))
    typ = tile('<div class="gr-type"><span class="gr-aa">Aa</span><div class="gr-tw"><span class="l">Open Sans Light</span><span class="s">Open Sans Semibold</span>'
               '<span class="abc">ABCDEFGHIJKLMNOPQRSTUVWXYZ</span><span class="abc">abcdefghijklmnopqrstuvwxyz</span><span class="abc">0123456789 — &amp; @ ’ “ ”</span></div></div>',
               'white bordered gr-band', 'Supporting typeface', 'Open Sans Light and Semibold')
    # the entrance sign (sign_blade) is the hero and card since t78u, so In place shows the lobby wall and the cards
    app = img_rows('the-grid', [[('sign_lobby.jpg', 'The Grid in dimensional letters on a lobby feature wall'), ('cards.jpg', 'The Grid business cards, front and back')]], r)
    con = ''
    for name, title, tag, keys, why, pre in CONCEPTS:
        chosen = pre is None
        con += (f'<div class="gr-concept{" chosen" if chosen else ""}"><div class="gr-panel stone">{logo(name, title + " logo concept", "w60" if name != "stage-one" else "w46")}</div>'
                f'<div class="gr-ctext"><span class="mono-s{"" if chosen else " muted"}">{tag}</span><h3 class="gr-ch">{title}</h3>'
                f'<ul class="gr-keys">{"".join(f"<li>{k}</li>" for k in keys)}</ul><p class="bm muted">{why}</p></div></div>')
        if pre:
            con += img_rows('the-grid', [[(f'{pre}_blade.jpg', f'{title} concept on an exterior blade sign'), (f'{pre}_lobby.jpg', f'{title} concept on a lobby feature wall')]], r)
    return ('<div class="grid-case">'
            + gsec(mark, 'The mark', 'Two offset, open frames — a plan of connected space — beside a light geometric wordmark whose open letters echo the gaps in the frames.')
            + gsec(var, 'Versions', 'One mark, set for every background it meets: stone and white, dark panels and the building’s own grey.')
            + gsec(swatches(GRID_PAL), 'Color')
            + gsec(typ, 'Typography', 'The wordmark is drawn, not typeset; Open Sans, the naming deck’s typeface, carries everything around it.')
            + gsec(app, 'In place', 'The identity inside the building — dimensional letters on the lobby wall — and on a business card; the entrance sign opens the page.')
            + gsec(f'<div class="gr-concepts">{con}</div>', 'Concept exploration', 'Three names were developed all the way to a logo, each with its own key messages and the reasoning behind it, alongside a wider list that included Node113, 405Xchange and Kirkland Hub. The Grid was chosen; Stage One and The Pulse remain concepts.')
            + '</div>')
