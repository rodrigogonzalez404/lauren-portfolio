"""Big Pink — leads with the OnePink identity (Grid-style), then the Ceros pitch and the concept exploration (Nov 23). Called from build.case().
Never say the client chose OnePink: it is the idea carried into the sample marketing material."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
NAVY, ROYAL, ROSE, GREY = '#282334', '#3A4687', '#C67484', '#D7D7DD'
COLORS = [('Dark Blue', NAVY, 'Trust · Stability · Authority'), ('Royal Blue', ROYAL, 'Creativity · Energy · Confidence'),
          ('Rose Pink', ROSE, 'Artistic charm'), ('Grey', GREY, 'Professionalism'), ('White', '#FFFFFF', '')]
NAMES = ['111 Fifth', 'One Portland', 'One Eleven Fifth', 'Pink Tower', 'One Eleven', 'One Rose', 'Beacon', 'One Pink', 'Big Pink',
         'Triple One', 'Roselight', 'The Panorama', 'Vantage', 'The Prism', 'Vertirosa', 'Luma Tower']
IDEAS = [('01', 'OneEleven', 'concept_oneeleven.jpg', 'An architectural monogram for 111 SW 5th Avenue, with a wide-set wordmark.'),
         ('02', 'Big Pink', 'concept_bigpink.jpg', 'Keeps the name the city already uses: folded chevrons crown a tall, slender frame over a condensed wordmark.')]   # 03 OnePink leads the case

def _symbol(name, sid):
    """OnePink wordmark (traced from the Ceros concept board) as an SVG <symbol>; ONE / PINK colours come from --one / --pink."""
    src = open(os.path.join(HERE, 'bigpink', name)).read()
    vb = re.search(r'viewBox="([^"]+)"', src).group(1)
    inner = src[src.index('>', src.index('<svg')) + 1:src.rindex('</svg>')]
    inner = inner.replace('class="w1" fill="currentColor"', 'fill="var(--one,currentColor)"').replace('class="w2" fill="currentColor"', 'fill="var(--pink,currentColor)"')
    return f'<symbol id="{sid}" viewBox="{vb}">{inner}</symbol>', vb

def defs():
    h, _ = _symbol('onepink-h.svg', 'op-h'); v, _ = _symbol('onepink-vertical.svg', 'op-v')
    return f'<svg width="0" height="0" style="position:absolute" aria-hidden="true">{h}{v}</svg>'

def op(one, pink, cls='', vertical=False):
    sid = 'op-v' if vertical else 'op-h'
    _, vb = _symbol('onepink-vertical.svg' if vertical else 'onepink-h.svg', sid)
    return f'<svg class="bp-op {cls}" viewBox="{vb}" role="img" aria-label="OnePink logo" style="--one:{one};--pink:{pink}"><use href="#{sid}"/></svg>'

def label(t, sub=''):
    sb = f'<span class="mono-s muted">{sub}</span>' if sub else ''
    return f'<div class="gr-lab"><span class="mono-s">{t}</span>{sb}</div>'

def tile(inner, style, lab, sub='', cls=''):
    return f'<div class="gr-cell"><div class="gr-panel {cls}" style="{style}">{inner}</div>{label(lab, sub)}</div>'

def blocks(r, gsec, swatches, img_rows, viewer):
    s = [f'scr/s{i:02d}.jpg' for i in range(1, 26)]
    files = (s[:8] + [('CONF', '[03] The Market · submarket figures, absorption, rents and concessions')] + s[8:9]
             + [('CONF', '[04] The Competition · competitive set')] + s[9:18] + [('CONF', '[06] Fee Proposal · fee terms')] + s[18:])
    pres = viewer('big-pink', 'Big Pink', files, r, 'Market figures, the competitive set and the fee terms are confidential and left out. Team, client and reference pages are not shown.', 'Ceros presentation', 'laptop')
    sw = ''.join(f'<div class="col gap8"><div class="sw" style="background:{h}"></div><span class="mono-s">{n}</span><span class="mono-s muted">{h}</span>{f"<span class=bp-mean>{m}</span>" if m else ""}</div>' for n, h, m in COLORS)
    color = f'<div class="gallery"><div class="swatches">{sw}</div></div>'
    mark = ('<div class="gr-two">'
            + tile(op('#FFFFFF', ROSE, 'v', True), f'background:{NAVY}', 'Vertical', 'Set like the tower, as on the building and the brochure cover')
            + tile(op(NAVY, ROSE, 'h'), 'background:#fff', 'Horizontal', 'For a line of text, the web and signage', 'bordered')
            + '</div>')
    var = ('<div class="gr-two">'
           + tile(op(NAVY, ROSE, 'h'), 'background:#fff', 'Primary', 'Dark Blue and Rose Pink on white', 'bordered')
           + tile(op('#FFFFFF', ROSE, 'h'), f'background:{NAVY}', 'Reversed', 'White and Rose Pink on Dark Blue')
           + tile(op('#FFFFFF', '#FFFFFF', 'h'), f'background:{ROSE}', 'One colour', 'White on Rose Pink')
           + tile(op(NAVY, NAVY, 'h'), f'background:{GREY}', 'One colour', 'Dark Blue on Grey')
           + '</div>')
    typ = ('<div class="gr-cell"><div class="gr-panel white bordered gr-band"><div class="gr-type bp-type"><span class="gr-aa">Aa</span><div class="gr-tw">'
           '<span class="b">CABIN BOLD</span><span class="l">Cabin Regular</span><span class="abc">ABCDEFGHIJKLMNOPQRSTUVWXYZ</span><span class="abc">abcdefghijklmnopqrstuvwxyz</span><span class="abc">0123456789 — &amp; ’ “ ”</span>'
           '</div></div></div>' + label('Supporting typeface', 'Cabin, the presentation’s typeface') + '</div>')
    place = (img_rows('big-pink', [[('concept_onepink.jpg', 'OnePink over the Portland skyline, in dimensional letters on a wall and on building signage')],
                                   [('material.jpg', 'OnePink sample marketing material — brochure, flyer, tablet and phone')]], r)
             + f'<div class="bp-tag" style="background:{NAVY}"><p><b>One</b> City</p><p><b>One</b> Workplace</p><p><b>One</b> Big Experience</p></div>'
             + label('Tagline', 'From the marketing approach'))
    names = ('<div class="bp-names"><div class="bp-scale"><span class="mono-s">Standard names</span><span class="bp-line"></span><span class="mono-s">Unique names</span></div>'
             '<ul class="gr-keys bp-chips">' + ''.join(f'<li>{n}</li>' for n in NAMES) + '</ul></div>')
    ideas = ''
    for n, name, f, line in IDEAS:
        ideas += (f'<div class="bp-idea"><div class="bp-ihead"><span class="mono-s muted">Logo idea {n}</span><h3 class="gr-ch">{name}</h3><p class="bm muted">{line}</p></div>'
                  + img_rows('big-pink', [[(f, f'{name} logo idea over the skyline, in dimensional letters and on building signage')]], r) + '</div>')
    ideas += ('<div class="bp-idea"><div class="bp-ihead"><span class="mono-s muted">First round</span><h3 class="gr-ch">Prism</h3><p class="bm muted">An angular, faceted mark from the first round of logo concepts, shown the same way.</p></div>'
              + img_rows('big-pink', [[('concept_prism.jpg', 'Prism logo concept over the skyline, in dimensional letters and on building signage')]], r) + '</div>')
    secs = [  # (anchor, title, body, intro) — Rodrigo t76u order; the presentation is last
        ('bp-mark', 'The mark', mark, 'OnePink joins the address and the nickname in one word. Wide-set, rounded capitals run vertically like the tower, with ONE set apart from PINK in rose.'),
        ('bp-versions', 'Versions', var, 'One mark, set for the palette’s light and dark grounds and in a single colour.'),
        ('bp-moodboard', 'Moodboard', img_rows('big-pink', [[('moodboard.jpg', 'Big Pink moodboard and palette')]], r), 'The tower, the city and Mt. Hood, Old Town streets, a rose mural and stone — and the palette taken from them.'),
        ('bp-color', 'Color', color, 'Four colours, each chosen for what it says about the building.'),
        ('bp-type', 'Typography', typ, 'The wordmark is lettered, not typeset; Cabin, the presentation’s typeface, carries the titles and text around it.'),
        ('bp-concepts', 'Concept exploration', f'<div class="bp-ideas">{ideas}</div>', 'The presentation showed three logo ideas, each over the skyline, in dimensional letters and on building signage. OnePink, shown first, is the one carried into the sample marketing material; OneEleven and Big Pink, and Prism from the first round of logo concepts, remain concepts.'),
        ('bp-naming', 'Naming', names, 'Sixteen sample names, on a scale from the standard to the unique.'),
        ('bp-place', 'In place', place, 'Over the skyline, in dimensional letters and on building signage — then carried through a sample brochure, flyer, tablet and phone, with a tagline built on “one”.'),
        ('bp-presentation', 'The presentation', pres, 'Thirty-eight screens in eight chapters, built in Ceros as a click-through pitch and framed by a vertical BIG PINK wordmark. The design screens are here — click through them on the laptop.'),
    ]
    toc = ('<nav class="toc" aria-label="On this page"><div class="toc-head"><span class="mono muted">[Contents]</span><span class="mono-s muted">'
           f'{len(secs):02d} sections</span></div><ol class="toc-list">'
           + ''.join(f'<li><a href="#{a}"><span class="mono muted">[{i:02d}]</span><span class="toc-t">{t}</span><span class="toc-ar" aria-hidden="true">↓</span></a></li>' for i, (a, t, _, _) in enumerate(secs, 1))
           + '</ol></nav>')
    return ('<div class="grid-case bp-case">' + defs() + gsec(toc)
            + ''.join(gsec(body, t, intro, aid=a) for a, t, body, intro in secs)
            + '</div>')
