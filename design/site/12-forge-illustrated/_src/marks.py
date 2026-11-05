"""The mark in 12's own hand: logo.svg, logo-animated.svg, icon-16.svg, banner-dark.svg, banner-light.svg (into the folder root).
Same drawing functions as the page: faceted stone, band of nine rivets, five runes, molten seam, the anvil, and the
bonfire of layered tongues (a sheet along the bed, three plumes, blue cores, copper-green and violet salts)."""
import math, os, re, random, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE); sys.path.insert(0, HERE)
import art, hero
from art import f, poly_d, rune_cut, stone, band, along, anvil, star4, circ, tongue as _t
from build import EXTRA_DEFS

ALL_DEFS = art.DEFS + art.LOGO_FLAME_DEFS + EXTRA_DEFS

def defs_for(body):
    """Only the gradients, patterns and filters the drawing uses (and what those use)."""
    want, out, seen = set(re.findall(r'url\(#([\w-]+)\)', body)), [], set()
    while want - seen:
        i = min(want - seen); seen.add(i)                      # in a fixed order, so the files diff cleanly
        m = re.search(r'<(linearGradient|radialGradient|pattern|filter) id="%s"[\s\S]*?</\1>' % re.escape(i), ALL_DEFS)
        if m: out.append(m.group(0)); want |= set(re.findall(r'url\(#([\w-]+)\)', m.group(0)))
    return '<defs>' + ''.join(out) + '</defs>'

# ---- the flame, as the page draws it (a port of page.js tongue(), frozen at one instant)
def chain(P):
    s = ''
    for i in range(len(P) - 1):
        p0, p1, p2, p3 = P[max(0, i - 1)], P[i], P[i + 1], P[min(len(P) - 1, i + 2)]
        s += f'C{p1[0] + (p2[0] - p0[0]) / 6:.1f} {p1[1] + (p2[1] - p0[1]) / 6:.1f} {p2[0] - (p3[0] - p1[0]) / 6:.1f} {p2[1] - (p3[1] - p1[1]) / 6:.1f} {p2[0]:.1f} {p2[1]:.1f}'
    return s

def tongue(cx, by, w, h, t, ph, sw):
    N = 6; L = []; R = []
    for i in range(N + 1):
        s = i / N; y = by - h * s; prof = w * math.sin(math.pi * (.2 + .8 * s)) ** .8 * (1 - .3 * s) if s < 1 else 0
        d = sw * w * s ** 1.4 * (.62 * math.sin(s * 4.6 - t * 5.4 + ph) + .38 * math.sin(s * 9.3 - t * 9.1 + ph * 1.9))
        L.append((cx + d - prof, y)); R.append((cx + d + prof, y))
    R.reverse()
    return f'M{R[N][0]:.1f} {R[N][1]:.1f}Q{cx:.1f} {by + w * .5:.1f} {L[0][0]:.1f} {L[0][1]:.1f}{chain(L)}{chain(R)}Z'

def fire(by, plumes, t=.35, sheet=(84, 172, 14), cls=False):
    """plumes: (cx, w, h, phase, core). Layers back to front, as on the page."""
    x0, x1, sh = sheet; g = []
    def sheet_d(hgt, k0):
        pts = [(x0, by + 3)]
        for i in range(17):
            x = x0 + i * (x1 - x0) / 16; env = math.exp(-((x - (x0 + x1) / 2) / ((x1 - x0) * .45)) ** 2)
            pts.append((x, by - hgt * (.35 + .65 * env) * (.75 + .25 * math.sin(x * .3 - t * 3.1 + k0) + .18 * math.sin(x * .7 + t * 4.7 + k0 * 2))))
        pts.append((x1, by + 3)); return poly_d(pts)
    g.append(f'<path d="{sheet_d(sh * 1.4, 1.3)}" fill="url(#fRed)" opacity=".5"/><path d="{sheet_d(sh, 0)}" fill="url(#fOut)"/>')
    L = {k: [] for k in ('red', 'out', 'out2', 'grn', 'vio', 'mid', 'core', 'base')}
    for i, (x, w, h, p, core) in enumerate(plumes):
        c = f' class="pl p{i}"' if cls else ''
        L['red'].append(f'<path{c} fill="url(#fRed)" d="{tongue(x, by + 2, w * 1.32, h * 1.12, t * .8, p + .5, .7)}"/>')
        L['out'].append(f'<path{c} fill="url(#fOut)" d="{tongue(x, by, w, h, t, p, .9)}"/>')
        if w >= 12:
            L['out2'].append(f'<path{c} fill="url(#fOut)" d="{tongue(x - w * .32, by, w * .55, h * .68, t * 1.15, p + 2.2, 1.3)}"/>')
            L['grn'].append(f'<path{c} fill="url(#fGrn)" d="{tongue(x + w * .44, by - h * .06, w * .28, h * .5, t * 1.3, p + 1, .9)}"/>')
            L['vio'].append(f'<path{c} fill="url(#fVio)" d="{tongue(x - w * .46, by - h * .05, w * .26, h * .46, t * 1.25, p + 4, .9)}"/>')
        L['mid'].append(f'<path{c} fill="url(#fMid)" d="{tongue(x, by, w * .62, h * .74, t * 1.05, p + .3, .8)}"/>')
        if core:
            L['core'].append(f'<path{c} fill="url(#fCore)" d="{tongue(x, by, w * .32, h * .44, t * 1.2, p + .6, .5)}"/>')
            L['base'].append(f'<ellipse cx="{x}" cy="{by - 1.5}" rx="{w * .5:.1f}" ry="{w * .16:.1f}" fill="#F4F8FF" opacity=".85"/>')
    g.append(f'<g opacity=".45">{"".join(L["red"])}</g>')
    for k in ('out', 'out2', 'grn', 'vio', 'mid', 'core', 'base'): g.append(''.join(L[k]))
    return ''.join(g)

STONE = ([(46, 150), (92, 148), (86, 232), (40, 226), (34, 190)], [(92, 148), (170, 146), (176, 234), (86, 232)], [(170, 146), (206, 150), (220, 186), (212, 228), (176, 234)])
RIV = along([(37, 162.6), (94, 159.6), (169, 157.6), (211, 161.6)], 9, .045, .955)
RUNES5 = [('algiz', 57, 172, 'blue'), ('thurs', 100, 172, 'gold'), ('wunjo', 128, 172, 'green'), ('ingwaz', 150, 172, 'violet'), ('kaun', 184, 172, 'orange')]
PLUMES = [(128, 25, 82, 0, 1), (103, 15, 50, 1.7, 1), (154, 16, 56, 4.2, 0), (86, 8, 22, .9, 0), (171, 8, 26, 2.9, 0)]
BILLET = 'M112 81.4 L114 80 H148 L150 81.4 V87 H112 Z'
# the side-on hammer at mark scale: head .11 of the page's, a handle short enough to stay in the frame
# the hero's head (hammer()) at the hero's head-to-handle ratio (150 : 496), so the mark's hammer is the same tool, not a matchstick
_HK = 66 / 496
_HH = [(-24, 64), (24, 64), (27, 58), (27, -18), (21, -26), (4, -86), (-4, -86), (-21, -26), (-27, -18), (-27, 58)]
MINI_HAMMER = ('<g class="hm"><path d="M3.2 -1.6 L66 -2.1 L66 2.1 L3.2 1.6 Z" fill="url(#hWood)"/><path d="M3.2 -1.6 L66 -2.1" stroke="#FFD2A0" stroke-opacity=".5" stroke-width=".4"/>'
               f'<path d="{poly_d([(x * _HK, y * _HK) for x, y in _HH])}" fill="url(#hSteelW)"/><path d="{poly_d([(x * _HK, y * _HK) for x, y in _HH])}" fill="url(#cheekG)"/>'
               f'<path d="M{f(-27 * _HK)} {f(-18 * _HK)} H{f(27 * _HK)}" stroke="#000" stroke-opacity=".4" stroke-width=".5"/>'
               f'<path d="M{f(-24 * _HK)} {f(64 * _HK)} H{f(24 * _HK)}" stroke="#fff" stroke-width=".7"/>'
               f'<path d="M{f(-27 * _HK)} {f(58 * _HK)} V{f(-18 * _HK)} L{f(-21 * _HK)} {f(-26 * _HK)} L{f(-4 * _HK)} {f(-86 * _HK)}" fill="none" stroke="#FFB070" stroke-opacity=".7" stroke-width=".45"/></g>')

def mark(animated=False, lite=False):
    """The mark's body in its 256 grid."""
    s = ['<ellipse cx="128" cy="238" rx="100" ry="6" fill="#000" opacity=".5" filter="url(#soft)"/>',
         '<circle cx="128" cy="58" r="84" fill="url(#halo)"/>']
    s.append(f'<g class="{"fire" if animated else ""}">{fire(88, PLUMES, cls=animated)}</g>')
    S_L, S_M, S_R = STONE
    s.append(stone([(S_L, 'url(#sL)', 76), (S_M, 'url(#sM)', 88), (S_R, 'url(#sR)', 100)], 77, u=.42, pits=36 if lite else 80, cracks=5, chisel=12 if lite else 50, hatch=None if lite else 'lines', sp=6,
                   avoid=[(50, 168, 82, 210), (96, 168, 120, 210), (124, 168, 150, 210), (146, 168, 174, 210), (180, 172, 204, 210)],
                   rims=[([(46, 150), (34, 190), (40, 226)], '#FFB070', .5, 1.2), ([(206, 150), (220, 186), (212, 228)], '#8FA6D6', .45, 1.1),
                         ([(92, 148), (86, 232)], '#000', .45, .9), ([(170, 146), (176, 234)], '#000', .45, .9), ([(46, 150), (92, 148), (170, 146), (206, 150)], '#FFC48A', .55, .8)]))
    s.append('<path d="M46,150 L92,148 L86,232 L40,226 L34,190 Z M92,148 L170,146 L176,234 L86,232 Z M170,146 L206,150 L220,186 L212,228 L176,234 Z" fill="url(#forgeSide)" style="mix-blend-mode:screen"/>')
    s.append('<path d="M46 150 L92 148 L170 146 L206 150 L203 153.5 L170 150 L92 152 L48 154 Z" fill="url(#bevel)"/>')
    s.append(band([(37, 160), (94, 157), (169, 155), (210, 159)], [(36, 170), (93, 167), (170, 165), (213, 169)], RIV, u=.95))
    if animated:
        s.append(''.join(f'<circle class="rv" style="--i:{i}" cx="{f(x)}" cy="{f(y)}" r="2.4"/>' for i, (x, y) in enumerate(RIV)))
    for name, x, y, col in RUNES5: s.append(rune_cut(name, x, y, 1, col))
    if animated:
        for i, (name, x, y, col) in enumerate(RUNES5):
            s.append(f'<g class="rg" style="--i:{i}">{art.rune_glow(name, x, y, 1, col, w=2.4, gid="gl3")}</g>')
    s.append(f'<g opacity=".8">{rune_cut("fehu", 41, 200, .55, "white", groove=3, core=1.1)}{rune_cut("sowilo", 204.5, 207, .42, "green", groove=2.6, core=1)}</g>')
    s.append(f'<g class="seamg">{hero.seam_pool()}</g>')
    s.append(anvil(seed=3, detail=not lite))
    s.append('<path d="M108 77 H154 V90 H108 Z" fill="#FF9A2A" filter="url(#gl2)" opacity=".6"/>')
    s.append(f'<path d="{BILLET}" fill="url(#billetG)"/><path d="M114 80 H148 L150 81.4 H112 Z" fill="#FFF0B0" opacity=".9"/>')
    if animated:
        s.append(f'<path class="barhot" d="{BILLET}" fill="#FFF4D8"/>')
        s.append(MINI_HAMMER)
        rng = random.Random(5); sp = []
        for i in range(16):
            a = math.radians(rng.uniform(-170, -10)); v = rng.uniform(26, 60)
            c = rng.choice(['#EAF2FF', '#FFE9B0', '#FFC24D', '#FF9440']) if rng.random() > .2 else rng.choice(['#45E0A0', '#BC8BFF', '#6E9BFF'])
            sp.append(f'<path d="M-5 0 H0" transform="translate(142 80) rotate({math.degrees(a):.0f})" stroke="{c}" stroke-width="1.3" stroke-linecap="round" style="--dx:{math.cos(a) * v:.1f}px;--dy:{math.sin(a) * v + 14:.1f}px"/>')
        s.append(f'<g class="sparks">{"".join(sp)}</g>')
        s.append(f'<g class="flash"><circle cx="142" cy="80" r="22" fill="url(#haloB)"/>{star4(142, 80, 9, "#F4F8FF")}<path d="M112 80 H172" stroke="#DCE8FF" stroke-width=".8"/></g>')
        s.append(''.join(f'<circle class="em" style="--i:{i};--x:{x}px" cx="{cx}" cy="70" r="1.1" fill="{c}"/>' for i, (cx, x, c) in enumerate([(110, -8, '#FFC24D'), (128, 6, '#FF9440'), (146, -4, '#FFE9B0'), (120, 10, '#45E0A0'), (138, -10, '#FF6A4A'), (132, 4, '#BC8BFF')])))
    s.append(f'<g class="star">{star4(208, 26, 13, "#F0D392")}</g>')
    return ''.join(s)

TITLE = 'Sampo: a steel anvil set into a rune-cut stone bound with nine rivets and a molten seam, a fire of many colours rising behind it, blue at the root into gold with green and violet tongues, one star above.'
ANIM_CSS = '''<style>
.fire .pl{transform-box:fill-box;transform-origin:50% 100%;animation:burn 1.7s ease-in-out infinite}
.fire .p1{animation-duration:1.3s;animation-delay:-.4s} .fire .p2{animation-duration:1.5s;animation-delay:-.9s} .fire .p3,.fire .p4{animation-duration:1.1s;animation-delay:-.2s}
@keyframes burn{0%,100%{transform:scale(1,1) skewX(0)}30%{transform:scale(.95,1.1) skewX(-3deg)}55%{transform:scale(1.04,.94) skewX(2deg)}80%{transform:scale(.98,1.05) skewX(-1deg)}}
.seamg{animation:breathe 3.6s ease-in-out infinite} @keyframes breathe{0%,100%{opacity:.55}40%{opacity:1}}
.rg{opacity:0;animation:rune 4.5s ease-in-out infinite;animation-delay:calc(var(--i)*.6s)} @keyframes rune{0%,100%{opacity:0}12%{opacity:.9}40%{opacity:.25}}
.rv{fill:#6B7180;animation:rivet 4.5s ease-out infinite;animation-delay:calc(var(--i)*.5s)} @keyframes rivet{0%{fill:#FFFFFF}6%{fill:#6E9BFF}22%{fill:#FFB050}45%,100%{fill:#6B7180}}
.barhot{opacity:0;animation:hot 2.6s ease-out infinite} @keyframes hot{0%{opacity:.95}50%,100%{opacity:0}}
.hm{transform-box:view-box;transform-origin:0 0;transform:translate(194px,56px) rotate(48deg);animation:swing 2.6s infinite}
@keyframes swing{0%{transform:translate(140.4px,72.3px) rotate(-12deg);animation-timing-function:cubic-bezier(.2,.8,.3,1)}6%{transform:translate(140.7px,68.6px) rotate(-15deg);animation-timing-function:ease-in-out}34%{transform:translate(168px,56px) rotate(16deg);animation-timing-function:ease-in-out}56%{transform:translate(194px,56px) rotate(48deg);animation-timing-function:ease-in-out}86%{transform:translate(198px,53px) rotate(53deg);animation-timing-function:cubic-bezier(.6,0,1,.6)}100%{transform:translate(140.4px,72.3px) rotate(-12deg)}}
.flash{opacity:0;animation:flash 2.6s ease-out infinite} @keyframes flash{0%{opacity:1}14%,100%{opacity:0}}
.sparks path{opacity:0;animation:fly 2.6s cubic-bezier(.15,.7,.4,1) infinite} @keyframes fly{0%{opacity:1;translate:0 0}45%{opacity:0;translate:var(--dx) var(--dy)}100%{opacity:0;translate:var(--dx) var(--dy)}}
.em{opacity:0;animation:rise 4.2s ease-in infinite;animation-delay:calc(var(--i)*-.7s)} @keyframes rise{0%{opacity:0;transform:none}15%{opacity:.95}100%{opacity:0;transform:translate(var(--x),-74px)}}
.star{transform-box:fill-box;transform-origin:center;animation:twinkle 2.6s ease-in-out infinite} @keyframes twinkle{0%,100%{transform:scale(1) rotate(0)}8%{transform:scale(1.25) rotate(10deg)}20%{transform:scale(.92)}}
@media (prefers-reduced-motion: reduce){*{animation:none!important}.sparks,.flash,.em,.rg,.barhot{display:none}}
</style>'''

def svg(w, h, body, title, extra='', vb=None):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb or f"0 0 {w} {h}"}" width="{w}" height="{h}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title>{extra}{defs_for(body)}{body}</svg>\n')

def icon16():
    """Drawn on the 16 grid, edges on whole and half pixels, the mark's silhouette: a wide stone with its band, the seam, the anvil, a low fire."""
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16" role="img" aria-labelledby="t"><title id="t">Sampo</title>'
            '<defs><linearGradient id="f" x1="0" y1="1" x2="0" y2="7" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#E2481A"/><stop offset=".55" stop-color="#FF9A2E"/><stop offset="1" stop-color="#FFE08A"/></linearGradient></defs>'
            '<path fill="url(#f)" d="M8 1 C9.6 2.6 10.6 4 10.4 5.4 L10.3 6.5 H5.7 L5.6 5.4 C5.4 4 6.4 2.6 8 1 Z"/>'
            '<path fill="url(#f)" d="M4.6 3.4 C5.5 4.3 5.9 5.3 5.8 6.5 H3.4 C3.3 5.3 3.7 4.3 4.6 3.4 Z M11.4 3 C12.4 4 12.8 5.1 12.6 6.5 H10.2 C10.1 5.1 10.5 4 11.4 3 Z"/>'
            '<path fill="#5B8CFF" d="M8 3.4 C8.8 4.3 9.1 5 9 5.7 L8.9 6.5 H7.1 L7 5.7 C6.9 5 7.2 4.3 8 3.4 Z"/>'
            '<path fill="#B9AFA8" d="M2 6.5 H11.5 C13 6.5 14.3 6.8 15.6 7.4 C14.4 8 13 8.3 11.6 8.4 L10.3 8.5 V9.5 H5.7 V8.5 L3.5 8.4 L3.1 7.5 H2 Z"/>'
            '<path fill="#FFE6C8" d="M3 6.5 H11.5 V7 H3 Z"/><path fill="#4E5260" d="M3.2 8 H11.6 L10.3 8.5 V9.5 H5.7 V8.5 L3.5 8.4 Z"/>'
            '<path fill="#FF9A2E" d="M4 9.5 H12 V10.3 H4 Z"/><path fill="#FFF1C8" d="M6.5 9.5 H9.5 V10 H6.5 Z"/>'
            '<path fill="#5A5664" d="M2 10.3 H5.6 L5.4 15.5 H1 Z"/><path fill="#3A3944" d="M5.6 10.3 H10.6 L10.8 15.5 H5.4 Z"/><path fill="#22232C" d="M10.6 10.3 H14 L15 15.5 H10.8 Z"/>'
            '<path fill="#2A2C33" d="M1.8 11.5 H14.3 V12.6 H1.6 Z"/><path fill="#A9B4C6" d="M1.8 11.5 H14.3 V11.9 H1.8 Z"/>'
            '<path fill="#FFC48A" d="M2 10.3 H14 V10.7 H2 Z" opacity=".7"/>'
            '</svg>\n')

def simple():
    """32 to 96 px: the same silhouette with the detail taken out. Wide stone in three facets, one band with three
    rivets, the seam, the anvil with its lit face, a hot billet, three plumes with a blue core. No runes, no pits."""
    S_L, S_M, S_R = STONE
    s = ['<circle cx="128" cy="70" r="80" fill="url(#halo)"/>']
    for (x, w, h, p, core) in ((128, 27, 96, 0, 1), (98, 17, 56, 1.7, 0), (158, 18, 62, 4.2, 0)):
        s.append(f'<path fill="url(#fOut)" d="{tongue(x, 88, w, h, .35, p, .7)}"/><path fill="url(#fMid)" d="{tongue(x, 88, w * .6, h * .7, .4, p + .3, .6)}"/>')
        if core: s.append(f'<path fill="url(#fCore)" d="{tongue(x, 88, w * .34, h * .46, .45, p + .6, .4)}"/>')
    s.append(f'<path d="{poly_d(S_L)}" fill="#5A5560"/><path d="{poly_d(S_M)}" fill="#34333C"/><path d="{poly_d(S_R)}" fill="#1E1E26"/>')
    s.append('<path d="M46 150 L92 148 L170 146 L206 150" fill="none" stroke="#FFC48A" stroke-width="3" stroke-linejoin="round"/>'
             '<path d="M46 150 L34 190 L40 226" fill="none" stroke="#FFB070" stroke-opacity=".6" stroke-width="3"/>')
    s.append('<path d="M37 160 L94 157 L169 155 L210 159 L213 175 L170 171 L93 173 L36 176 Z" fill="#2A2C33"/><path d="M37 160 L94 157 L169 155 L210 159" fill="none" stroke="#A9B4C6" stroke-opacity=".6" stroke-width="2"/>')
    for x, y in ((66, 166), (128, 163), (190, 165)): s.append(f'<circle cx="{x}" cy="{y}" r="5" fill="url(#rivet)"/>')
    s.append('<path d="M66 147.5 H190" stroke="#FF6A1E" stroke-width="9" opacity=".6" filter="url(#gl3)"/><path d="M70 144.5 H186 V150.5 H70 Z" fill="url(#seamU)"/>')
    s.append(f'<path d="{art.ANVIL_D}" fill="url(#aSteel)"/><path d="M72 87 H164 C176 87 196 91 220 96.6" fill="none" stroke="url(#faceLit)" stroke-width="3"/>')
    s.append(f'<path d="{BILLET}" fill="url(#billetG)"/><path d="M114 80 H148 L150 82 H112 Z" fill="#FFF0B0"/>')
    return ''.join(s)

# ---- the wordmark: Bodoni Moda outlined, so the banners need no font
def outline(font_file, text, size, x, y, axes, track=0):
    from fontTools.ttLib import TTFont
    from fontTools.varLib.instancer import instantiateVariableFont
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    ft = instantiateVariableFont(TTFont(os.path.join(HERE, 'fonts', font_file)), axes)
    gs = ft.getGlyphSet(); cmap = ft.getBestCmap(); sc = size / ft['head'].unitsPerEm; d = []; cx = x
    for ch in text:
        g = cmap[ord(ch)]; pen = SVGPathPen(gs, ntos=lambda v: f'{v:.1f}'.rstrip('0').rstrip('.'))
        gs[g].draw(TransformPen(pen, (sc, 0, 0, -sc, cx, y))); d.append(pen.getCommands()); cx += gs[g].width * sc + track
    return ''.join(d), cx - x

def banner(theme):
    W, H = 1280, 320; dark = theme == 'dark'; rng = random.Random(11); s = []
    if dark:
        s.append('<linearGradient id="bgN" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0B1030"/><stop offset="1" stop-color="#060819"/></linearGradient>'
                 '<radialGradient id="bgG" cx="230" cy="300" r="380" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#FF8A2A" stop-opacity=".28"/><stop offset="1" stop-color="#FF8A2A" stop-opacity="0"/></radialGradient>'
                 '<linearGradient id="eng" x1="0" y1="92" x2="0" y2="212" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#FFF6DD"/><stop offset=".3" stop-color="#F0D392"/><stop offset=".55" stop-color="#B9873F"/><stop offset=".76" stop-color="#E9C98A"/><stop offset="1" stop-color="#E9C98A"/></linearGradient>')
    else:
        s.append('<linearGradient id="bgN" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E2E6F1"/><stop offset="1" stop-color="#EEF0F6"/></linearGradient>'
                 '<radialGradient id="bgG" cx="230" cy="300" r="380" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#FFAA5A" stop-opacity=".28"/><stop offset="1" stop-color="#FFAA5A" stop-opacity="0"/></radialGradient>'
                 '<linearGradient id="eng" x1="0" y1="92" x2="0" y2="212" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#2A2140"/><stop offset=".45" stop-color="#12163A"/><stop offset=".76" stop-color="#3C3426"/><stop offset="1" stop-color="#3C3426"/></linearGradient>')
    defs_local = '<defs>' + s.pop() + '</defs>'
    b = [f'<rect width="{W}" height="{H}" rx="14" fill="url(#bgN)"/><rect width="{W}" height="{H}" rx="14" fill="url(#bgG)"/>']
    if dark:
        st = {}
        for _ in range(260):
            x = rng.uniform(8, W - 8); y = rng.uniform(8, H - 8); m = rng.random() ** 2.6; c = rng.random()
            col = '#FFD6A0' if c < .12 else '#AAC4FF' if c < .3 else '#EBF0FF'
            st.setdefault((col, 0 if m < .25 else 1), []).append(circ(x, y, .45 + m * 1.1))
        for (col, lv), ds in st.items(): b.append(f'<path d="{"".join(ds)}" fill="{col}" opacity="{(.35, .85)[lv]}"/>')
        OT = [(11.06, 61.75), (11.03, 56.38), (11.9, 53.69), (12.26, 57.03), (12.9, 55.96), (13.4, 54.93), (13.79, 49.31)]
        P = [(1010 + (ra - 11) * 95, 40 + (62 - de) * 6.5) for ra, de in OT]
        b.append('<path d="' + ''.join(f'M{f(P[a][0])} {f(P[a][1])}L{f(P[c][0])} {f(P[c][1])}' for a, c in [(0, 1), (1, 2), (2, 3), (3, 0), (3, 4), (4, 5), (5, 6)]) + '" stroke="#D4AE66" stroke-opacity=".35" stroke-width=".9" fill="none"/>')
        b.append(''.join(f'<circle cx="{f(x)}" cy="{f(y)}" r="1.8" fill="#FFF4DC"/>' for x, y in P))
    # the mark's scene at banner scale, embers climbing out of it
    b.append(f'<g transform="translate(70 18) scale(1.17)">{mark()}</g>')
    for _ in range(26):
        x = rng.uniform(150, 330); y = rng.uniform(16, 90); c = rng.choice(['#FFC24D', '#FF9440', '#FFE9B0', '#FF6A4A', '#45E0A0', '#BC8BFF'])
        b.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{rng.uniform(.8, 1.8):.1f}" fill="{c}" opacity="{rng.uniform(.4, .95):.2f}"/>')
    ink = '#EEF0FA' if dark else '#12163A'; muted = '#9097BC' if dark else '#555B80'; brass = '#D4AE66' if dark else '#7A5A26'
    wd, ww = outline('BodoniModa-normal.woff2', 'Sampo', 118, 420, 182, {'wght': 420, 'opsz': 96}, track=-1)
    b.append(f'<path d="{wd}" fill="url(#eng)"/>')
    td, tw = outline('BodoniModa-italic.woff2', 'Your coding agent, with a smith on the job.', 30, 424, 252, {'wght': 400, 'opsz': 28})
    b.append(f'<path d="{td}" fill="{ink}"/>')
    md, mw = outline('MartianMono-normal.woff2', 'FORMERLY FOREMAN · DISCIPLINE FOR CODING AGENTS', 11.5, 424, 64, {'wght': 500}, track=2.2)
    b.append(f'<path d="{md}" fill="{muted}"/><path d="M424 52 l4 -4 l4 4 l-4 4 Z" fill="#FFC24D" transform="translate(-14 8)"/>')
    # an engraved brass rule with ticks, straight, like the edge of an instrument
    x1 = 424 + max(ww, tw); b.append(f'<path d="M424 280 H{f(x1)}" stroke="{brass}" stroke-opacity=".7"/><path d="' + ''.join(f'M{f(x)} 280 v{5 if (i % 5) else 9}' for i, x in enumerate(range(424, int(x1) + 1, 12))) + f'" stroke="{brass}" stroke-opacity=".5"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t"><title id="t">Sampo, formerly Foreman: discipline for coding agents. {TITLE}</title>'
            + defs_local + defs_for(''.join(b)) + ''.join(b) + '</svg>\n')

if __name__ == '__main__':
    body = mark(); open(os.path.join(OUT, 'logo.svg'), 'w').write(svg(256, 256, body, TITLE))
    body = mark(True); open(os.path.join(OUT, 'logo-animated.svg'), 'w').write(svg(256, 256, body, TITLE + ' The fire burns, a blow throws sparks, runes kindle and rivets heat in turn.', ANIM_CSS))
    open(os.path.join(OUT, 'icon-16.svg'), 'w').write(icon16())
    body = simple(); open(os.path.join(OUT, 'logo-simple.svg'), 'w').write(svg(256, 256, body, 'Sampo: an anvil on a stone bound with an iron band, a fire behind it.', vb='8 0 240 240'))
    for th in ('dark', 'light'): open(os.path.join(OUT, f'banner-{th}.svg'), 'w').write(banner(th))
    for n in ('logo.svg', 'logo-simple.svg', 'logo-animated.svg', 'icon-16.svg', 'banner-dark.svg', 'banner-light.svg'): print(n, os.path.getsize(os.path.join(OUT, n)) // 1024, 'KB')

def scoped_css():
    """The animated mark's CSS, scoped to .mk so it can live inline in a page."""
    css = ANIM_CSS.replace('<style>', '').replace('</style>', '')
    css = re.sub(r'(^|[}\n])\s*(\.[\w-][^{@]*)\{', lambda m_: m_.group(1) + ','.join('.mk ' + x.strip() for x in m_.group(2).split(',')) + '{', css)
    css = re.sub(r'@keyframes (\w+)', r'@keyframes mk-\1', css)
    css = re.sub(r'animation:(\w+) ', r'animation:mk-\1 ', css)
    return css.replace('*{animation:none!important}', '.mk *{animation:none!important}')
