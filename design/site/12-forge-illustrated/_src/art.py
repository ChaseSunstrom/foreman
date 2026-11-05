"""The illustrated forge: every drawing on the page, in the approved mark's language.
Faceted stone (three-facet gradients, pits, engraved hatch, cracks, warm and cool rim light), iron bands with rivets,
runes cut deep and lit from inside, a molten seam, steel with a bright face line, and the mark's layered flame.
Deterministic: every random detail comes from a seeded RNG."""
import math, random

_uid = [0]
def uid(p='u'):
    _uid[0] += 1
    return f'{p}{_uid[0]}'

def f(v): return f'{v:.1f}'.rstrip('0').rstrip('.') if abs(v - round(v)) > 1e-6 else str(int(round(v)))
def pts(P): return ' '.join(f'{f(x)},{f(y)}' for x, y in P)
def poly_d(P): return 'M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in P) + ' Z'

def inside(p, P):
    x, y = p; c = False; n = len(P)
    for i in range(n):
        x1, y1 = P[i]; x2, y2 = P[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-9) + x1: c = not c
    return c

def bbox(P):
    xs = [p[0] for p in P]; ys = [p[1] for p in P]
    return min(xs), min(ys), max(xs), max(ys)

def lerp(a, b, t): return a + (b - a) * t

# ---------------------------------------------------------------- shared defs (one hidden svg; ids are global)
DEFS = '''
<linearGradient id="sL" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5A5560"/><stop offset="1" stop-color="#2B2830"/></linearGradient>
<linearGradient id="sM" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3B3A44"/><stop offset="1" stop-color="#1C1B22"/></linearGradient>
<linearGradient id="sR" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#22232C"/><stop offset=".8" stop-color="#15151B"/><stop offset="1" stop-color="#3A4258"/></linearGradient>
<linearGradient id="sT" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8A7F86"/><stop offset="1" stop-color="#4A4450"/></linearGradient>
<linearGradient id="rfl-blue" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6E9BFF" stop-opacity=".25"/><stop offset=".28" stop-color="#6E9BFF"/><stop offset=".72" stop-color="#6E9BFF"/><stop offset="1" stop-color="#6E9BFF" stop-opacity=".25"/></linearGradient>
<linearGradient id="rfl-gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFC24D" stop-opacity=".25"/><stop offset=".28" stop-color="#FFC24D"/><stop offset=".72" stop-color="#FFC24D"/><stop offset="1" stop-color="#FFC24D" stop-opacity=".25"/></linearGradient>
<linearGradient id="rfl-green" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#45E0A0" stop-opacity=".25"/><stop offset=".28" stop-color="#45E0A0"/><stop offset=".72" stop-color="#45E0A0"/><stop offset="1" stop-color="#45E0A0" stop-opacity=".25"/></linearGradient>
<linearGradient id="rfl-violet" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#BC8BFF" stop-opacity=".25"/><stop offset=".28" stop-color="#BC8BFF"/><stop offset=".72" stop-color="#BC8BFF"/><stop offset="1" stop-color="#BC8BFF" stop-opacity=".25"/></linearGradient>
<linearGradient id="rfl-orange" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FF9440" stop-opacity=".25"/><stop offset=".28" stop-color="#FF9440"/><stop offset=".72" stop-color="#FF9440"/><stop offset="1" stop-color="#FF9440" stop-opacity=".25"/></linearGradient>
<linearGradient id="rfl-white" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#DCE8FF" stop-opacity=".25"/><stop offset=".28" stop-color="#DCE8FF"/><stop offset=".72" stop-color="#DCE8FF"/><stop offset="1" stop-color="#DCE8FF" stop-opacity=".25"/></linearGradient>
<linearGradient id="rfl-red" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FF6A4A" stop-opacity=".25"/><stop offset=".28" stop-color="#FF6A4A"/><stop offset=".72" stop-color="#FF6A4A"/><stop offset="1" stop-color="#FF6A4A" stop-opacity=".25"/></linearGradient>
<linearGradient id="sB1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" style="stop-color:var(--sb1a,#4A4550)"/><stop offset="1" style="stop-color:var(--sb1b,#24222A)"/></linearGradient>
<linearGradient id="sB2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" style="stop-color:var(--sb2a,#433F4B)"/><stop offset="1" style="stop-color:var(--sb2b,#1F1E26)"/></linearGradient>
<linearGradient id="sB3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" style="stop-color:var(--sb3a,#504853)"/><stop offset="1" style="stop-color:var(--sb3b,#2A2630)"/></linearGradient>
<linearGradient id="sB4" x1="0" y1="0" x2="0" y2="1"><stop offset="0" style="stop-color:var(--sb4a,#3C3A46)"/><stop offset="1" style="stop-color:var(--sb4b,#1B1A21)"/></linearGradient>
<linearGradient id="pit" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".6"/><stop offset=".5" stop-color="#000" stop-opacity="0"/><stop offset=".6" stop-color="#E8E2F0" stop-opacity="0"/><stop offset="1" stop-color="#E8E2F0" stop-opacity=".22"/></linearGradient>
<linearGradient id="bevel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFC48A" stop-opacity=".55"/><stop offset="1" stop-color="#FF8A3A" stop-opacity=".05"/></linearGradient>
<linearGradient id="steelV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C9D2DE"/><stop offset=".08" stop-color="#6E7684"/><stop offset=".45" stop-color="#2E333C"/><stop offset="1" stop-color="#16181D"/></linearGradient>
<linearGradient id="steelH" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FF8A3A" stop-opacity=".45"/><stop offset=".45" stop-color="#FF8A3A" stop-opacity="0"/><stop offset=".85" stop-color="#7DA2FF" stop-opacity="0"/><stop offset="1" stop-color="#7DA2FF" stop-opacity=".35"/></linearGradient>
<linearGradient id="steelFlat" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4A515E"/><stop offset=".5" stop-color="#2A2E37"/><stop offset="1" stop-color="#15171C"/></linearGradient>
<linearGradient id="seam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7A1E10"/><stop offset=".18" stop-color="#E2481A"/><stop offset=".38" stop-color="#FFB03C"/><stop offset=".52" stop-color="#FFF8E6"/><stop offset=".66" stop-color="#FFB03C"/><stop offset=".86" stop-color="#E2481A"/><stop offset="1" stop-color="#7A1E10"/></linearGradient>
<linearGradient id="drip" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFD27A"/><stop offset=".5" stop-color="#E2481A"/><stop offset="1" stop-color="#5A1408" stop-opacity="0"/></linearGradient>
<linearGradient id="fOut" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FF7022" stop-opacity="0"/><stop offset=".16" stop-color="#FA621E" stop-opacity=".6"/><stop offset=".3" stop-color="#F66820" stop-opacity=".94"/><stop offset=".6" stop-color="#FF8A1F"/><stop offset="1" stop-color="#FFC24D"/></linearGradient>
<linearGradient id="fRed" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FF7828" stop-opacity="0"/><stop offset=".3" stop-color="#FF7828" stop-opacity="0"/><stop offset=".55" stop-color="#FA6E24" stop-opacity=".3"/><stop offset=".8" stop-color="#F86822" stop-opacity=".62"/><stop offset="1" stop-color="#F66E28" stop-opacity=".85"/></linearGradient>
<linearGradient id="fMid" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFB040" stop-opacity="0"/><stop offset=".35" stop-color="#FFC24D"/><stop offset="1" stop-color="#FFF1C8"/></linearGradient>
<linearGradient id="fCore" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3D6BFF" stop-opacity="0"/><stop offset=".4" stop-color="#4C78FF"/><stop offset=".85" stop-color="#9FC0FF"/><stop offset="1" stop-color="#EAF2FF"/></linearGradient>
<linearGradient id="fGrn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#45E0A0" stop-opacity="0"/><stop offset=".5" stop-color="#45E0A0" stop-opacity=".8"/><stop offset="1" stop-color="#A8F5D2" stop-opacity=".9"/></linearGradient>
<linearGradient id="fVio" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#BC8BFF" stop-opacity="0"/><stop offset=".5" stop-color="#BC8BFF" stop-opacity=".8"/><stop offset="1" stop-color="#E2CCFF" stop-opacity=".9"/></linearGradient>
<radialGradient id="halo"><stop offset="0" stop-color="#FFB050" stop-opacity=".5"/><stop offset=".45" stop-color="#FF7A2A" stop-opacity=".16"/><stop offset="1" stop-color="#FF7A2A" stop-opacity="0"/></radialGradient>
<radialGradient id="haloB"><stop offset="0" stop-color="#9FC0FF" stop-opacity=".55"/><stop offset=".5" stop-color="#4C78FF" stop-opacity=".14"/><stop offset="1" stop-color="#4C78FF" stop-opacity="0"/></radialGradient>
<radialGradient id="haloV"><stop offset="0" stop-color="#D9C2FF" stop-opacity=".7"/><stop offset=".45" stop-color="#BC8BFF" stop-opacity=".2"/><stop offset="1" stop-color="#BC8BFF" stop-opacity="0"/></radialGradient>
<radialGradient id="haloG"><stop offset="0" stop-color="#A8F5D2" stop-opacity=".6"/><stop offset=".45" stop-color="#45E0A0" stop-opacity=".18"/><stop offset="1" stop-color="#45E0A0" stop-opacity="0"/></radialGradient>
<radialGradient id="coalGlow"><stop offset="0" stop-color="#FFF1C8"/><stop offset=".25" stop-color="#FFB03C"/><stop offset=".6" stop-color="#E2481A" stop-opacity=".7"/><stop offset="1" stop-color="#7A1E10" stop-opacity="0"/></radialGradient>
<radialGradient id="rivet" cx=".38" cy=".34" r=".7"><stop offset="0" stop-color="#B9C2D2"/><stop offset=".35" stop-color="#6B7180"/><stop offset="1" stop-color="#22252D"/></radialGradient>
<radialGradient id="rivetHot" cx=".4" cy=".36" r=".7"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".35" stop-color="#CFE0FF"/><stop offset="1" stop-color="#4C78FF"/></radialGradient>
<linearGradient id="band" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4A4E58"/><stop offset=".25" stop-color="#2E3038"/><stop offset="1" stop-color="#17181D"/></linearGradient>
<linearGradient id="wood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7A4E30"/><stop offset=".5" stop-color="#4E2F1C"/><stop offset="1" stop-color="#2A1910"/></linearGradient>
<linearGradient id="leather" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7A3A24"/><stop offset="1" stop-color="#3A1A12"/></linearGradient>
<linearGradient id="barHot" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#B8301A"/><stop offset=".25" stop-color="#FF8A1F"/><stop offset=".55" stop-color="#FFE9B0"/><stop offset=".8" stop-color="#FF9A2E"/><stop offset="1" stop-color="#C8381E"/></linearGradient>
<linearGradient id="barCool" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7E8796"/><stop offset=".2" stop-color="#4A515E"/><stop offset="1" stop-color="#1D2026"/></linearGradient>
<linearGradient id="water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3A2A30"/><stop offset=".3" stop-color="#1A1622"/><stop offset="1" stop-color="#0B0A10"/></linearGradient>
<linearGradient id="brass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF1CC"/><stop offset=".4" stop-color="#E9C98A"/><stop offset="1" stop-color="#9A6F30"/></linearGradient>
<pattern id="hp76" width="7" height="46" patternUnits="userSpaceOnUse" patternTransform="rotate(-14)"><path d="M1 0 V19 M1 23 V46 M4.6 5 V31 M4.6 35 V44" stroke="#000" stroke-opacity=".2" stroke-width=".7"/><path d="M2.2 8 V16" stroke="#F4E8E0" stroke-opacity=".07" stroke-width=".6"/></pattern>
<pattern id="hp88" width="6.4" height="52" patternUnits="userSpaceOnUse" patternTransform="rotate(-2)"><path d="M1 0 V27 M1 31 V52 M4.2 9 V40 M4.2 44 V50" stroke="#000" stroke-opacity=".2" stroke-width=".7"/><path d="M2.3 30 V41" stroke="#F4E8E0" stroke-opacity=".07" stroke-width=".6"/></pattern>
<pattern id="hp100" width="7.4" height="40" patternUnits="userSpaceOnUse" patternTransform="rotate(10)"><path d="M1 0 V15 M1 19 V40 M4.8 3 V26 M4.8 30 V37" stroke="#000" stroke-opacity=".2" stroke-width=".7"/><path d="M2.4 20 V30" stroke="#F4E8E0" stroke-opacity=".06" stroke-width=".6"/></pattern>
<pattern id="gapcell" width="4.4" height="4.4" patternUnits="userSpaceOnUse"><rect width="3.4" height="3.4" fill="#1C1F26"/></pattern>
<filter id="gl2" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="2"/></filter>
<filter id="gl3" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="3.2"/></filter>
<filter id="gl6" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="gl12" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="12"/></filter>
<filter id="gl24" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="24"/></filter>
<filter id="soft" x="-30%" y="-80%" width="160%" height="260%"><feGaussianBlur stdDeviation="2.4"/></filter>
'''

# ---------------------------------------------------------------- runes: straight cuts, the mark's five first
RUNES = {
    'algiz':   'M9 4 V34 M9 14 L0 4 M9 14 L18 4',
    'thurs':   'M6 0 V34 M6 7 L16 16 L6 25',
    'wunjo':   'M6 0 V34 M6 0 L18 12 L6 24',
    'ingwaz':  'M10 0 L20 17 L10 34 L0 17 Z',
    'kaun':    'M6 4 V34 M6 16 L16 6',
    'fehu':    'M4 0 V34 M4 7 L16 0 M4 17 L16 10',
    'ehwaz':   'M2 0 V34 M18 0 V34 M2 0 L10 10 L18 0',
    'othala':  'M10 0 L19 9 L4 24 L0 34 M10 0 L1 9 L16 24 L20 34',
    'raido':   'M4 0 V34 M4 0 L15 8 L4 16 L16 34',
    'tiwaz':   'M10 0 V34 M0 10 L10 0 L20 10',
    'dagaz':   'M2 0 V34 M18 0 V34 M2 0 L18 34 M18 0 L2 34',
    'mannaz':  'M2 0 V34 M18 0 V34 M2 0 L18 15 M18 0 L2 15',
    'berkano': 'M4 0 V34 M4 0 L15 8 L4 17 L15 26 L4 34',
    'laguz':   'M6 0 V34 M6 0 L16 9',
    'sowilo':  'M14 0 L4 12 L16 22 L6 34',
    'hagalaz': 'M2 0 V34 M18 0 V34 M2 12 L18 22',
}
COL = {'blue': '#6E9BFF', 'gold': '#FFC24D', 'green': '#45E0A0', 'violet': '#BC8BFF', 'orange': '#FF9440', 'white': '#DCE8FF', 'red': '#FF6A4A'}

def _hot(c, k):
    """Mix a fire colour toward white (k > 0) or toward black (k < 0)."""
    c = c.lstrip('#'); r, g, b = (int(c[i:i + 2], 16) for i in (0, 2, 4))
    return '#%02X%02X%02X' % tuple(int(v + (255 - v) * k) if k >= 0 else int(v * (1 + k)) for v in (r, g, b))

def rune_cut(name, x, y, s, col, groove=5, core=1.8, glow=.42, gid='gl3'):
    """A rune cut into the stone as a V, lit by the fire from the upper left: the cut's opening in the stone's own dark, its
    lower-right wall catching the light and a lit lip along that edge, the upper-left wall left in shadow, and the heat only
    on the narrow floor, brightest mid-stroke and fading toward the ends (`rfl-<colour>`). No outline, no pale tube, no
    halo: the warmth reaches a tenth of the groove past its edge. `gid` is kept for callers; no filter is used."""
    d = RUNES[name]; tr = f'translate({f(x)} {f(y)}) scale({s})'
    c = COL.get(col, col); g = groove / s; floor = f'url(#rfl-{col})' if col in COL else c
    return (f'<g transform="{tr}" fill="none" stroke-linecap="butt" stroke-linejoin="miter">'
            f'<path d="{d}" stroke="{c}" stroke-width="{g * 1.2:.2f}" opacity="{glow * .26:.3f}"/>'
            f'<path d="{d}" stroke="#D8CABA" stroke-opacity=".42" stroke-width="{g:.2f}" transform="translate({.11 * g:.2f} {.11 * g:.2f})"/>'
            f'<path d="{d}" stroke="#2A2226" stroke-opacity=".9" stroke-width="{g:.2f}"/>'
            f'<path d="{d}" stroke="#6A5C5C" stroke-opacity=".7" stroke-width="{g * .44:.2f}" transform="translate({.14 * g:.2f} {.14 * g:.2f})"/>'
            f'<path d="{d}" stroke="#120E12" stroke-opacity=".55" stroke-width="{g * .4:.2f}" transform="translate({-.12 * g:.2f} {-.12 * g:.2f})"/>'
            f'<path d="{d}" stroke="{floor}" stroke-width="{max(core / s * .8, g * .24):.2f}"/></g>')

def rune_glow(name, x, y, s, col, w=6, gid='gl6', crawl=True):
    """The kindling overlay: heat swelling up from the floor of the cut, no blur (its opacity animates)."""
    d = RUNES[name]; tr = f'translate({f(x)} {f(y)}) scale({s})'; c = COL.get(col, col)
    return (f'<g transform="{tr}" fill="none" stroke-linecap="square">'
            f'<path d="{d}" stroke="{c}" stroke-width="{w * 1.9 / s:.2f}" opacity=".18"/>'
            f'<path d="{d}" stroke="{c}" stroke-width="{w * 1.2 / s:.2f}" opacity=".35"/>'
            f'<path d="{d}" stroke="{_hot(c, .35)}" stroke-width="{w * .55 / s:.2f}" opacity=".9"/>'
            f'<path d="{d}" stroke="{_hot(c, .8)}" stroke-width="{w * .24 / s:.2f}"/>'
            + '</g>' + (crawl_path(name, x, y, s, w) if crawl else ''))

def crawl_path(name, x, y, s, w):
    """The ember crawling along a kindled rune's stroke: its own small layer, so animating it never repaints the rest."""
    return f'<path class="crawl" d="{RUNES[name]}" transform="translate({f(x)} {f(y)}) scale({s})" fill="none" stroke="#FFFDF4" stroke-width="{w * .5 / s:.2f}" pathLength="100"/>'

# ---------------------------------------------------------------- faceted stone
def circ(x, y, r):
    q = f(r) if r >= 1 else f'{r:.2f}'.lstrip('0'); q2 = f(2 * r) if r >= .5 else f'{2 * r:.2f}'.lstrip('0')
    return f'M{f(x - r)} {f(y)}a{q} {q} 0 1 0 {q2} 0a{q} {q} 0 1 0 -{q2} 0'

def pits_paths(pts, u=1.0):
    """Carved pits as three compound paths: the hollow, its deep core, and the lit lower-right lip."""
    dark, deep, lip = [], [], []
    for x, y, r in pts:
        dark.append(circ(x, y, r))
        lip.append(circ(x + r * .38, y + r * .38, r * .5))
        if r > 2.2 * u: deep.append(circ(x - r * .15, y - r * .15, r * .45))
    out = f'<path d="{"".join(dark)}" fill="#000" fill-opacity=".34"/><path d="{"".join(lip)}" fill="#E8E2F0" fill-opacity=".16"/>'
    if deep: out += f'<path d="{"".join(deep)}" fill="#000" fill-opacity=".38"/>'
    return out

def stone(facets, seed, u=1.0, pits=60, cracks=4, hatch='pat', rims=(), avoid=(), chisel=30, extra='', sp=2.8):
    """facets: list of (polygon, fill, hatch_angle_deg). Draws fills, engraved hatch, pits, chisel marks and cracks,
    each clipped to its facet, then the rim lights: (polyline, colour, opacity, width). Details are compound paths."""
    rng = random.Random(seed); out = []
    areas = [(bbox(P)[2] - bbox(P)[0]) * (bbox(P)[3] - bbox(P)[1]) for P, _, _ in facets]; tot = sum(areas)
    for (P, fill, ang), ar in zip(facets, areas):
        x0, y0, x1, y1 = bbox(P); cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; R = math.hypot(x1 - x0, y1 - y0) / 2 + 2
        out.append(f'<path d="{poly_d(P)}" fill="{fill}"/>')
        if hatch == 'lines':
            cid = uid('c'); out.append(f'<clipPath id="{cid}"><path d="{poly_d(P)}"/></clipPath>'); g = [f'<g clip-path="url(#{cid})">']
        else: g = ['<g>']
        # broad planes: the stone was split, not sawn (fans from the facet's own corners, so they never leave it)
        pl = {'#fff': [], '#000': []}; mx = sum(p[0] for p in P) / len(P); my = sum(p[1] for p in P) / len(P)
        for _ in range(3):
            i = rng.randrange(len(P)); A_, B_ = P[i], P[(i + 1) % len(P)]; t_ = rng.uniform(.25, .8)
            Q = [A_, B_, (lerp(mx, B_[0], t_ * .5), lerp(my, B_[1], t_ * .5)), (lerp(mx, A_[0], t_), lerp(my, A_[1], t_))]
            pl['#fff' if rng.random() < .5 else '#000'].append(poly_d(Q))
        for c_, ds in pl.items():
            if ds: g.append(f'<path d="{"".join(ds)}" fill="{c_}" opacity="{.04 if c_ == "#fff" else .07}"/>')
        if hatch == 'pat':
            # the pattern is filled straight into the facet, scaled so its cuts follow the stone's size
            hp = min((76, 88, 100), key=lambda q: abs(q - ang)); z = u / 2.4
            Pz = [(cx + (x - cx) / z, cy + (y - cy) / z) for x, y in P]
            g.append(f'<path transform="translate({f(cx)} {f(cy)}) scale({z:.3f}) translate({f(-cx)} {f(-cy)})" d="{poly_d(Pz)}" fill="url(#hp{hp})"/>')
        elif hatch:
            # hand-cut hatch: lines start at random points so one dash pattern never lines up
            th = math.radians(ang); dx, dy = math.cos(th), math.sin(th); nx, ny = -dy, dx
            sp_ = sp * u; k = -R; hl = []; hl2 = []
            while k < R:
                ox, oy = cx + nx * k, cy + ny * k; e = rng.uniform(0, 40) * u
                a1, a2 = (ox - dx * (R + e), oy - dy * (R + e)), (ox + dx * R, oy + dy * R)
                hl.append(f'M{f(a1[0])} {f(a1[1])}L{f(a2[0])} {f(a2[1])}')
                if rng.random() < .3: hl2.append(f'M{f(a1[0] + nx * .5 * u)} {f(a1[1] + ny * .5 * u)}L{f(a2[0] + nx * .5 * u)} {f(a2[1] + ny * .5 * u)}')
                k += sp_ * rng.uniform(.75, 1.3)
            g.append(f'<path d="{"".join(hl)}" fill="none" stroke="#000" stroke-opacity=".17" stroke-width="{.24 * u:.2f}" stroke-dasharray="{f(17 * u)} {f(3 * u)} {f(7 * u)} {f(2 * u)} {f(25 * u)} {f(5 * u)} {f(4 * u)} {f(1.5 * u)}"/>')
            g.append(f'<path d="{"".join(hl2)}" fill="none" stroke="#F4E8E0" stroke-opacity=".07" stroke-width="{.24 * u:.2f}" stroke-dasharray="{f(6 * u)} {f(14 * u)} {f(9 * u)} {f(19 * u)}"/>')
        # pits: dark at the upper left, lit at the lower right, as the mark draws them
        n = max(1, round(pits * ar / tot)); placed = 0; tries = 0; ps = []
        while placed < n and tries < n * 30:
            tries += 1
            p = (rng.uniform(x0, x1), rng.uniform(y0, y1))
            r_ = (.45 + 4.2 * rng.random() ** 3.2) * u
            if not all(inside((p[0] + dx * r_ * 1.2, p[1] + dy * r_ * 1.2), P) for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1))) or any(ax0 <= p[0] <= ax1 and ay0 <= p[1] <= ay1 for ax0, ay0, ax1, ay1 in avoid): continue
            ps.append((p[0], p[1], r_)); placed += 1
        g.append(pits_paths(ps, u))
        # chisel marks: short paired strokes, a dark cut and its lit lip
        cd, cl = [], []
        for _ in range(round(chisel * ar / tot)):
            p = (rng.uniform(x0, x1), rng.uniform(y0, y1))
            if not inside(p, P): continue
            a = math.radians(ang + rng.uniform(-35, 35)); L = rng.uniform(1.5, 4.5) * u
            q = (p[0] + math.cos(a) * L, p[1] + math.sin(a) * L)
            if not inside(q, P): continue
            cd.append(f'M{f(p[0])} {f(p[1])}L{f(q[0])} {f(q[1])}'); cl.append(f'M{f(p[0] + .4 * u)} {f(p[1] + .5 * u)}L{f(q[0] + .4 * u)} {f(q[1] + .5 * u)}')
        if cd: g.append(f'<path d="{"".join(cd)}" fill="none" stroke="#000" stroke-opacity=".4" stroke-width="{.35 * u:.2f}" stroke-linecap="round"/><path d="{"".join(cl)}" fill="none" stroke="#FFE2C8" stroke-opacity=".13" stroke-width="{.35 * u:.2f}" stroke-linecap="round"/>')
        g.append('</g>')
        out.append(''.join(g))
    # cracks: random walks from an edge, carved (dark) with a lit lip
    cr = []
    for _ in range(cracks):
        P = rng.choice(facets)[0]; i = rng.randrange(len(P)); a_, b_ = P[i], P[(i + 1) % len(P)]
        t = rng.uniform(.2, .8); p = [lerp(a_[0], b_[0], t), lerp(a_[1], b_[1], t)]
        cxp = sum(q[0] for q in P) / len(P); cyp = sum(q[1] for q in P) / len(P)
        ang = math.atan2(cyp - p[1], cxp - p[0]); line = [tuple(p)]
        for _ in range(rng.randint(3, 7)):
            ang += rng.uniform(-.7, .7); L = rng.uniform(3, 9) * u
            p = [p[0] + math.cos(ang) * L, p[1] + math.sin(ang) * L]
            if not inside(p, P): break
            line.append(tuple(p))
        if len(line) > 1: cr.append('M' + 'L'.join(f'{f(x)} {f(y)}' for x, y in line))
    if cr:
        d = ''.join(cr)
        out.append(f'<path d="{d}" fill="none" stroke="#08080B" stroke-width="{1.1 * u:.2f}" stroke-linejoin="round" opacity=".85"/>'
                   f'<path d="{d}" fill="none" stroke="#E8DCD0" stroke-opacity=".12" stroke-width="{.45 * u:.2f}" transform="translate({.6 * u:.2f} {.7 * u:.2f})"/>')
    for line, col, op, w in rims:
        out.append(f'<path d="M{" L".join(f"{f(x)} {f(y)}" for x, y in line)}" fill="none" stroke="{col}" stroke-opacity="{op}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')
    out.append(extra)
    return ''.join(out)

def band(top, bot, rivets, u=1.0, hot=(), rr=1.0):
    """An iron band: top and bottom edges as polylines (left to right), rivets at given points."""
    P = list(top) + list(reversed(bot))
    s = [f'<path d="{poly_d(P)}" fill="url(#band)" stroke="#0B0B0E" stroke-width="{.8 * u:.2f}"/>',
         f'<path d="M{" L".join(f"{f(x)} {f(y)}" for x, y in top)}" fill="none" stroke="#A9B4C6" stroke-opacity=".45" stroke-width="{.9 * u:.2f}"/>',
         f'<path d="M{" L".join(f"{f(x)} {f(y + 1.6 * u)}" for x, y in bot)}" fill="none" stroke="#000" stroke-opacity=".45" stroke-width="{1.6 * u:.2f}" filter="url(#gl2)"/>']
    rng = random.Random(len(rivets) * 7 + int(top[0][0]))
    # hammer dents on the band
    x0, y0, x1, y1 = bbox(P); dents = {True: [], False: []}
    for _ in range(int((x1 - x0) / (3 * u))):
        x = rng.uniform(x0 + 2 * u, x1 - 2 * u)
        # interpolate band centre
        yc = None
        for i in range(len(top) - 1):
            if top[i][0] <= x <= top[i + 1][0]:
                t = (x - top[i][0]) / (top[i + 1][0] - top[i][0] + 1e-9); yt = lerp(top[i][1], top[i + 1][1], t); break
        else: yt = top[0][1]
        for i in range(len(bot) - 1):
            if bot[i][0] <= x <= bot[i + 1][0]:
                t = (x - bot[i][0]) / (bot[i + 1][0] - bot[i][0] + 1e-9); yb = lerp(bot[i][1], bot[i + 1][1], t); break
        else: yb = bot[0][1]
        y = rng.uniform(yt + (yb - yt) * .25, yb - (yb - yt) * .2); r = rng.uniform(.6, 1.6) * u
        dents[rng.random() < .5].append(circ(x, y, r))
    s.append(f'<path d="{"".join(dents[True])}" fill="#C8D2E2" opacity=".1"/><path d="{"".join(dents[False])}" fill="#000" opacity=".14"/>')
    # brushed iron: long faint strokes along the band
    s.append('<path d="' + ''.join(f'M{f(rng.uniform(x0, x0 + (x1 - x0) * .3))} {f(rng.uniform(y0 + 2 * u, y1 - 2 * u))}h{f(rng.uniform(20, 70) * u)}' for _ in range(int((x1 - x0) / (8 * u)))) + f'" stroke="#C8D2E2" stroke-opacity=".08" stroke-width="{.4 * u:.2f}"/>')
    for i, (x, y) in enumerate(rivets):
        r = 2.5 * u * rr
        s.append(f'<circle cx="{f(x + .4 * u)}" cy="{f(y + .7 * u)}" r="{r:.2f}" fill="#000" opacity=".5"/>'
                 f'<circle cx="{f(x)}" cy="{f(y)}" r="{r:.2f}" fill="url(#rivet)"/>'
                 f'<circle cx="{f(x - .8 * u)}" cy="{f(y - .8 * u)}" r="{.8 * u:.2f}" fill="#E6ECF6" opacity=".75"/>'
                 f'<path d="M{f(x - r * .9)} {f(y + r * .2)} A{r * .95:.2f} {r * .95:.2f} 0 0 1 {f(x - r * .1)} {f(y - r * .9)}" fill="none" stroke="#FFB070" stroke-opacity=".55" stroke-width="{.5 * u:.2f}"/>')
    return ''.join(s)

def along(line, n, t0=.04, t1=.96):
    """n points evenly along a polyline."""
    L = [0]
    for i in range(1, len(line)): L.append(L[-1] + math.dist(line[i - 1], line[i]))
    out = []
    for k in range(n):
        d = lerp(t0, t1, k / (n - 1)) * L[-1]
        for i in range(1, len(line)):
            if L[i] >= d:
                t = (d - L[i - 1]) / (L[i] - L[i - 1] + 1e-9)
                out.append((lerp(line[i - 1][0], line[i][0], t), lerp(line[i - 1][1], line[i][1], t))); break
    return out

# ---------------------------------------------------------------- the mark's anvil, in its own 256 grid
ANVIL_D = 'M56 90 H70 L72 86 H164 C176 86 196 90 222 96 C204 104 186 110 168 112 L160 114 C148 116 146 120 146 126 L150 136 H170 L172 146 H84 L86 136 H106 L110 126 C110 120 106 116 96 114 L74 112 L70 104 H56 Z'

ANVIL_TOP = 'M72 86.6 L74 84.2 H163 C176 84.2 197 88.4 221 95.2 L220 96.4 C196 90.6 176 86.6 164 86.6 Z'   # the face, seen just from above
# the flames, mirrored and squashed on the polished face: (x, half-width, length) in the mark grid
FACE_REFL = [(84, 3.2, 1.9), (95, 2.4, 1.5), (104, 2.8, 2.1), (156, 2.6, 1.7), (166, 2, 1.3), (176, 1.6, 1.1)]

def anvil(seed=3, mark=True, detail=True):
    """One steel everywhere: a mid-tone body lit warm by the fire behind and cool from the sky, the face seen just from above
    (warm at the fire's end, cool at the horn, the flames reflected in it), mill scale, a blue specular along the horn,
    a 1 px dark edge, and a foot in shadow but lit from the seam below."""
    rng = random.Random(seed)
    s = [f'<path d="{ANVIL_D}" fill="url(#aSteel)"/>', f'<path d="{ANVIL_D}" fill="url(#steelH)" style="mix-blend-mode:screen"/>']
    if detail:
        cid = uid('c'); s.append(f'<clipPath id="{cid}"><path d="{ANVIL_D}"/></clipPath><g clip-path="url(#{cid})">')
        st = {True: [], False: []}
        for _ in range(30):
            y = rng.uniform(90, 140); x = rng.uniform(60, 200); L = rng.uniform(8, 40)
            st[rng.random() < .55].append(f'M{f(x)} {f(y)}H{f(x + L)}')
        s.append(f'<path d="{"".join(st[True])}" stroke="#E2D6CC" stroke-opacity=".1" stroke-width=".35"/><path d="{"".join(st[False])}" stroke="#000" stroke-opacity=".14" stroke-width=".35"/>')
        sp = {True: [], False: []}
        for _ in range(240):
            sp[rng.random() < .4].append(circ(rng.uniform(58, 215), rng.uniform(90, 145), rng.uniform(.12, .42)))
        s.append(f'<path d="{"".join(sp[True])}" fill="#E8DED6" opacity=".2"/><path d="{"".join(sp[False])}" fill="#0C0E12" opacity=".3"/>')
        s.append(f'<path d="{ANVIL_D}" fill="url(#edgeDark)"/>')
        s.append('<path d="M84 128 H172 V146 H84 Z" fill="#000" opacity=".1"/><path d="M84 138 H172 V146 H84 Z" fill="url(#footCast)"/>')
        s.append('<path d="M86 136 H106 L110 126 M150 136 L146 126" fill="none" stroke="#000" stroke-opacity=".3" stroke-width=".8"/>')
        s.append('<path d="M84 141 H172" stroke="#E0B898" stroke-opacity=".25" stroke-width=".7"/><path d="M110 127 C110 121 106 117 96 115" fill="none" stroke="#FFB070" stroke-opacity=".4" stroke-width=".8"/>')
        s.append('<path d="M150 136 H170 L172 146" fill="none" stroke="#8FA6D6" stroke-opacity=".4" stroke-width=".6"/><path d="M86 136 H106" fill="none" stroke="#FFB070" stroke-opacity=".45" stroke-width=".6"/>')
        # the horn: a blue-white specular along its top, a cool bounce under it
        s.append('<path d="M166 89.6 C182 90.2 198 92.8 216 96.6" fill="none" stroke="#DCE8FF" stroke-opacity=".5" stroke-width="1" stroke-linecap="round"/>')
        s.append('<path d="M170 104.6 C184 102 198 100 214 97.8" fill="none" stroke="#7DA2FF" stroke-opacity=".35" stroke-width=".8"/>')
        s.append('<path d="M58 92 V103" stroke="#FFB070" stroke-opacity=".35" stroke-width=".8"/>')
        s.append('</g>')
    # the face: its strip seen from just above, warm at the fire's end, cool toward the horn, the flames in it
    s.append(f'<path d="{ANVIL_TOP}" fill="url(#faceTop)"/>')
    if detail:
        s.append('<path d="' + ''.join(f'M{x - w} 86.4 Q{x} {86.4 - L * 1.2} {x + w} 86.4 Q{x} {86.4 - L * .4} {x - w} 86.4 Z' for x, w, L in FACE_REFL) + '" fill="#FFB050" opacity=".55"/>')
    s.append('<path d="M72 86.6 H164 C176 86.6 196 90.6 220 96.4" fill="none" stroke="url(#faceLit)" stroke-width=".8"/>'
             '<path d="M118 86.4 Q120.5 89 123 86.4" fill="#1A1C22"/><path d="M56 90.6 H70" stroke="#C9D2DE" stroke-width="1" opacity=".55"/>')
    s.append(f'<path d="{ANVIL_D}" fill="none" stroke="#0B0D12" stroke-opacity=".7" stroke-width=".32" stroke-linejoin="round"/>')
    if detail:
        for x in (79, 97, 139, 156):
            s.append(f'<path d="M{x} 86.4 l1.2 1.4 l1.4 -1.4 Z" fill="#14161B" opacity=".8"/>')
    if mark:
        s.append('<g transform="translate(122.5 119.5)"><path d="M0 0 H11 V6 L5.5 10.5 L0 6 Z" fill="#0F1116" stroke="#BC8BFF" stroke-opacity=".35" stroke-width=".5"/>'
                 '<path d="M4 1.8 V8 M4 1.8 L7.6 4.6" fill="none" stroke="#BC8BFF" stroke-width=".8" opacity=".75"/></g>')
    return ''.join(s)

def flame_logo(tr, op=1, cls=''):
    """The mark's flame, exactly as drawn there (outer, two salt tongues, mid, blue core, white base)."""
    return (f'<g transform="{tr}" opacity="{op}" class="{cls}">'
            '<path fill="url(#fOutL)" d="M128 6 C140 26 160 40 158 62 C157 76 148 86 128 90 C108 86 98 76 98 62 C97 46 112 38 116 22 C120 34 126 38 128 6 Z"/>'
            '<path fill="#45E0A0" opacity=".75" d="M150 46 C158 54 160 64 154 74 C150 66 148 58 150 46 Z"/>'
            '<path fill="#BC8BFF" opacity=".75" d="M104 52 C98 60 98 70 104 78 C107 70 107 62 104 52 Z"/>'
            '<path fill="url(#fMidL)" d="M128 24 C138 40 148 52 146 66 C145 78 138 86 128 89 C118 86 111 78 110 66 C109 54 120 44 128 24 Z"/>'
            '<path fill="url(#fCoreL)" d="M128 44 C134 56 138 64 137 72 C136 82 132 87 128 89 C124 87 120 82 119 72 C118 64 122 56 128 44 Z"/>'
            '<ellipse cx="128" cy="86" rx="9" ry="3.2" fill="#F4F8FF" opacity=".9"/></g>')

LOGO_FLAME_DEFS = '''
<linearGradient id="fOutL" x1="0" y1="8" x2="0" y2="90" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#C8281A" stop-opacity="0"/><stop offset=".25" stop-color="#E2481A"/><stop offset=".6" stop-color="#FF8A1F"/><stop offset="1" stop-color="#FFC24D"/></linearGradient>
<linearGradient id="fMidL" x1="0" y1="24" x2="0" y2="90" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#FFB040" stop-opacity="0"/><stop offset=".35" stop-color="#FFC24D"/><stop offset="1" stop-color="#FFF1C8"/></linearGradient>
<linearGradient id="fCoreL" x1="0" y1="44" x2="0" y2="90" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#3D6BFF" stop-opacity="0"/><stop offset=".4" stop-color="#4C78FF"/><stop offset=".85" stop-color="#9FC0FF"/><stop offset="1" stop-color="#EAF2FF"/></linearGradient>
<linearGradient id="aSteel" x1="0" y1="86" x2="0" y2="146" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#B8A496"/><stop offset=".06" stop-color="#7A7476"/><stop offset=".22" stop-color="#5A5F6C"/><stop offset=".55" stop-color="#3C414D"/><stop offset="1" stop-color="#1C2029"/></linearGradient>
<linearGradient id="faceTop" x1="70" x2="222" y1="0" y2="0" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#C89A78"/><stop offset=".25" stop-color="#E8B890"/><stop offset=".55" stop-color="#B8B0B0"/><stop offset=".82" stop-color="#9AA8C4"/><stop offset="1" stop-color="#C8D8F0"/></linearGradient>
<linearGradient id="footCast" x1="0" y1="146" x2="0" y2="138" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#FF8A3A" stop-opacity=".45"/><stop offset="1" stop-color="#FF8A3A" stop-opacity="0"/></linearGradient>
<linearGradient id="faceLit" x1="56" x2="222" y1="0" y2="0" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#FFC48A"/><stop offset=".45" stop-color="#FFE6C8"/><stop offset=".75" stop-color="#FFD2A8"/><stop offset="1" stop-color="#C9D8F0"/></linearGradient>
<linearGradient id="edgeDark" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset=".85" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".3"/></linearGradient>
'''

def star4(x, y, r, fill='#F0D392', cls=''):
    k = r / 14
    d = f'M{f(x)} {f(y - 14 * k)} L{f(x + 2 * k)} {f(y - 2 * k)} L{f(x + 14 * k)} {f(y)} L{f(x + 2 * k)} {f(y + 2 * k)} L{f(x)} {f(y + 14 * k)} L{f(x - 2 * k)} {f(y + 2 * k)} L{f(x - 14 * k)} {f(y)} L{f(x - 2 * k)} {f(y - 2 * k)} Z'
    return f'<path class="{cls}" d="{d}" fill="{fill}"/>'

# ---------------------------------------------------------------- an overlay: a small composited svg over a figure
def ov(vb_w, vb_h, box, inner, cls='', style='', extra_attr=''):
    x, y, w, h = box
    st = f'left:{x / vb_w * 100:.3f}%;top:{y / vb_h * 100:.3f}%;width:{w / vb_w * 100:.3f}%;height:{h / vb_h * 100:.3f}%;{style}'
    return f'<svg class="ov {cls}" viewBox="{f(x)} {f(y)} {f(w)} {f(h)}" style="{st}" aria-hidden="true" {extra_attr}>{inner}</svg>'

def pct(vb_w, vb_h, x, y):
    return f'left:{x / vb_w * 100:.2f}%;top:{y / vb_h * 100:.2f}%'

# ---------------------------------------------------------------- the flame: page.js tongue(), frozen at one instant
def _chain(P):
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
    return f'M{R[N][0]:.1f} {R[N][1]:.1f}Q{cx:.1f} {by + w * .5:.1f} {L[0][0]:.1f} {L[0][1]:.1f}{_chain(L)}{_chain(R)}Z'

def fire(by, plumes, t=.35, sheet=None, cls=False, red=.45):
    """plumes: (cx, w, h, phase, core). Layers back to front exactly as page.js draws them. Each plume can be its own group (cls)."""
    g = []
    if sheet:
        x0, x1, sh = sheet
        def sheet_d(hgt, k0):
            pts = [(x0, by + 3)]
            for i in range(27):            # as page.js sheetPath
                x = x0 + i * (x1 - x0) / 26; env = math.exp(-((x - (x0 + x1) / 2) / ((x1 - x0) * .45)) ** 2)
                pts.append((x, by - hgt * (.35 + .65 * env) * (.75 + .25 * math.sin(x * .045 - t * 3.1 + k0) + .18 * math.sin(x * .11 + t * 4.7 + k0 * 2))))
            pts.append((x1, by + 3)); return poly_d(pts)
        g.append(f'<path d="{sheet_d(sh * 1.4, 1.3)}" fill="url(#fRed)" opacity="{red + .05:.2f}"/><path d="{sheet_d(sh, 0)}" fill="url(#fOut)"/>')
    for i, (x, w, h, p, core) in enumerate(plumes):
        L = [f'<path fill="url(#fRed)" opacity="{red}" d="{tongue(x, by + 2, w * 1.32, h * 1.12, t * .8, p + .5, .7)}"/>',
             f'<path fill="url(#fOut)" d="{tongue(x, by, w, h, t, p, .9)}"/>']
        if w >= 12:
            L += [f'<path fill="url(#fOut)" d="{tongue(x - w * .32, by, w * .55, h * .68, t * 1.15, p + 2.2, 1.3)}"/>',
                  f'<path fill="url(#fGrn)" d="{tongue(x + w * .44, by - h * .06, w * .28, h * .5, t * 1.3, p + 1, .9)}"/>',
                  f'<path fill="url(#fVio)" d="{tongue(x - w * .46, by - h * .05, w * .26, h * .46, t * 1.25, p + 4, .9)}"/>']
        L.append(f'<path fill="url(#fMid)" d="{tongue(x, by, w * .62, h * .74, t * 1.05, p + .3, .8)}"/>')
        if core:
            L.append(f'<path fill="url(#fCore)" d="{tongue(x, by, w * .32, h * .44, t * 1.2, p + .6, .5)}"/>')
            L.append(f'<path d="M{x - w * .5:.1f} {by - 1.5:.1f} L{x:.1f} {by - w * .16 - 1.5:.1f} L{x + w * .5:.1f} {by - 1.5:.1f} L{x:.1f} {by + w * .16 - 1.5:.1f} Z" fill="#F4F8FF" opacity=".8"/>')
        # positioned by the outer group, breathing on the inner one (so a CSS transform never moves it)
        g.append(f'<g><g class="{"pl p" + str(i % 5) if cls else ""}" style="transform-origin:{x:.0f}px {by:.0f}px">{"".join(L)}</g></g>')
    return ''.join(g)

def wisp(x, y, w, h, seed, grad='vapor', peak=.2):
    """Steam or smoke: four soft-edged shapes stacked up from (x, y), each wider and fainter than the one below and leaning
    a little, so the wisp widens and thins as it lifts. The soft edge is baked into the radial gradient (no filter)."""
    rng = random.Random(seed); out = []
    for i, (fy, fw, fo) in enumerate(((.1, .42, 1), (.36, .66, .85), (.6, .92, .62), (.84, 1.2, .42))):
        out.append(f'<ellipse cx="{f(x + rng.uniform(-.1, .1) * w + i * w * .07)}" cy="{f(y - fy * h)}" rx="{f(w * fw * .5)}" ry="{f(h * (.17 + i * .03))}" fill="url(#{grad})" opacity="{fo}"/>')
    return f'<g opacity="{peak}">{"".join(out)}</g>'

def broken_reflection(cx, y0, y1, width, cols, seed, lean=0):
    """A fire mirrored in dark water and broken by ripples: the flame's silhouette, upside down and drawn out toward the
    viewer, cut into rows of lens-shaped slivers (thick in the middle, tapering to points, each with a small wave), the rows
    sliding left and right on a swell. `cols` runs from the brightest (the core) to the dimmest (the rim)."""
    rng = random.Random(seed); out = {c: [] for c in cols}; y = y0; i = 0; n = max(1, int((y1 - y0) / 2.5))
    while y < y1 - 1:
        u = i / n; half = width * .5 * max(.08, (1 - u) ** .9); c0 = cx + lean * u + 3.2 * math.sin(i * 1.3 + .5) + rng.uniform(-1, 1)
        x = c0 - half
        while x < c0 + half - 2:
            L = min(c0 + half - x, rng.uniform(5, 14) * (1 - u * .4)); t = rng.uniform(1, 1.9) * (1 - u * .35); wv = rng.uniform(-.5, .5)
            k = min(len(cols) - 1, int(abs((x + L / 2) - c0) / max(half, 1) * len(cols) + u * 1.5))
            out[cols[k]].append(f'M{f(x)} {f(y)} L{f(x + L * .3)} {f(y - t / 2 + wv)} L{f(x + L * .72)} {f(y - t / 2 - wv)} L{f(x + L)} {f(y + wv * .5)} L{f(x + L * .7)} {f(y + t / 2)} L{f(x + L * .28)} {f(y + t / 2 + wv)} Z')
            x += L + rng.uniform(1.2, 4) * (1 + u)
        y += 2.2 + u * 1.4 + rng.uniform(-.2, .3); i += 1
    return ''.join(f'<path d="{"".join(ds)}" fill="{c}" opacity="{.95 - j * .2:.2f}"/>' for j, (c, ds) in enumerate(out.items()) if ds)
