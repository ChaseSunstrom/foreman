"""The hero: the mark's world scaled up. Scene units 1200 x 1000; the rune stone and anvil are the mark itself at 3.2x
(drawn in the mark's own 256 grid), set in front of a hearth of dry-laid stone under the turning sky. One fire lights it all."""
import math, random
from art import *

W, H = 1200, 1000
S = 3.2; TX, TY = 290.4, 131.2                    # mark grid -> scene
M = f'matrix({S} 0 0 {S} {TX} {TY})'
def sc(x, y): return (S * x + TX, S * y + TY)

STRIKE = (745, 387)                               # top of the billet, where the hammer lands
BY = 398                                          # the flames' roots
PLUMES = [(640, 70, 272, 0, 1), (548, 46, 188, 1.7, 1), (470, 28, 96, 3.1, 0), (852, 42, 142, 4.2, 1), (940, 26, 86, 2.4, 0),
          (1006, 18, 52, 5.3, 0), (404, 17, 46, .9, 0), (716, 26, 104, 2.9, 0), (790, 18, 58, 3.7, 0)]   # same list as page.js
STONE_L = [(46, 150), (92, 148), (86, 232), (40, 226), (34, 190)]
STONE_M = [(92, 148), (170, 146), (176, 234), (86, 232)]
STONE_R = [(170, 146), (206, 150), (220, 186), (212, 228), (176, 234)]
BAND_T = [(37, 160), (94, 157), (169, 155), (210, 159)]
BAND_B = [(36, 170), (93, 167), (170, 165), (213, 169)]
RIVETS = along([(37, 162.6), (94, 159.6), (169, 157.6), (211, 161.6)], 9, .045, .955)
FRONT_RUNES = [('algiz', 57, 172, 'blue'), ('thurs', 100, 172, 'gold'), ('wunjo', 128, 172, 'green'), ('ingwaz', 150, 172, 'violet'), ('kaun', 184, 172, 'orange')]

# ------------------------------------------------------------------------------------------------ the far range
def far():
    """Three depth bands of faceted ridges, the farthest nearly the sky's colour. Every peak is split into four facets, two
    to a side, each side split by a crease. Two lightings are drawn, one shown per theme: by night the faces toward the
    forge take the fire (`n` set), by day the faces toward the dawn at the upper right take the sun (`d` set).
    Snow on the high peaks; a haze band in front of each ridge line. The copper rim is its own layer (returned), so it can
    answer the fire."""
    rng = random.Random(41); s = []; rims = []
    bands = [('b3', 790, 470, 610, (90, 170), True, 140), ('b2', 800, 540, 670, (80, 150), True, 90), ('b1', 812, 620, 730, (70, 130), False, 50)]
    for cls, base, ymin, ymax, (st0, st1), snow, edge in bands:
        x = -140; ridge = []; peak = True
        while x < 1340:
            e = max(0, 1 - min(abs(x - 120), abs(x - 1180)) / 260)
            y = (rng.uniform(ymin, ymin + (ymax - ymin) * .45) - e * edge) if peak else rng.uniform(ymin + (ymax - ymin) * .55, ymax)
            ridge.append((x, y, peak)); x += rng.uniform(st0, st1) * (.6 if peak else .5); peak = not peak
        s.append(f'<path class="{cls}a" d="{poly_d([(-140, base)] + [(x, y) for x, y, _ in ridge] + [(1340, base)])}"/>')
        F = {k: [] for k in ('nk1', 'nk2', 'ns1', 'ns2', 'dk1', 'dk2', 'ds1', 'ds2')}; crease, snows = [], []
        for i in range(1, len(ridge) - 1):
            x, y, pk = ridge[i]
            if not pk: continue
            l, r = ridge[i - 1], ridge[i + 1]
            fl = (x + (l[0] - x) * .3 + rng.uniform(-8, 8), base); fr = (x + (r[0] - x) * .3 + rng.uniform(-8, 8), base)
            # each side: an upper facet from the peak along the shoulder, and a lower one under the crease
            ml = (lerp(x, l[0], .5) + rng.uniform(-6, 6), lerp(y, l[1], .5) + rng.uniform(8, 22)); mr = (lerp(x, r[0], .5) + rng.uniform(-6, 6), lerp(y, r[1], .5) + rng.uniform(8, 22))
            L1 = poly_d([(x, y), (l[0], l[1]), ml]); L2 = poly_d([(x, y), ml, (l[0], l[1]), (l[0], base), fl])
            R1 = poly_d([(x, y), (r[0], r[1]), mr]); R2 = poly_d([(x, y), mr, (r[0], r[1]), (r[0], base), fr])
            toward = 'R' if x < 650 else 'L'                  # the face toward the forge, by night
            for side, (p1, p2) in (('L', (L1, L2)), ('R', (R1, R2))):
                F['nk1' if side == toward else 'ns1'].append(p1); F['nk2' if side == toward else 'ns2'].append(p2)
                F['dk1' if side == 'R' else 'ds1'].append(p1); F['dk2' if side == 'R' else 'ds2'].append(p2)   # the dawn is at the upper right
            crease.append(f'M{f(x)} {f(y)}L{f(ml[0])} {f(ml[1])}M{f(x)} {f(y)}L{f(mr[0])} {f(mr[1])}M{f(x)} {f(y)}L{f(lerp(x, (fl[0] + fr[0]) / 2, .7))} {f(lerp(y, base, .7))}')
            side = r if x < 650 else l
            rims.append(f'M{f(x)} {f(y)}L{f(lerp(x, side[0], .55))} {f(lerp(y, side[1], .55))}')
            if snow and y < ymin + (ymax - ymin) * .3 - (40 if cls == 'b3' else 0):
                k = .22; a_, b_ = (lerp(x, l[0], k), lerp(y, l[1], k)), (lerp(x, r[0], k), lerp(y, r[1], k))
                snows.append(poly_d([(x, y), b_, (lerp(x, b_[0], .55), lerp(y, b_[1], .55) + 6), (x + rng.uniform(-3, 3), y + (b_[1] - y) * .95), (lerp(x, a_[0], .5), lerp(y, a_[1], .5) + 7), a_]))
        for k, ds in F.items(): s.append(f'<path class="{cls}{k} {k[0]}" d="{"".join(ds)}"/>')
        s.append(f'<path class="crease" d="{"".join(crease)}"/>')
        if snows: s.append(f'<path class="snow" d="{"".join(snows)}"/>')
        s.append(f'<rect class="haze" x="-140" y="{base - 150}" width="1480" height="190"/>')
    for x, y, h, rn, col in ((215, 772, 66, 'tiwaz', 'blue'), (330, 782, 44, 'laguz', 'violet'), (1110, 778, 58, 'sowilo', 'green')):
        w = h * .36
        P = [(x - w * .5, y), (x - w * .42, y - h * .82), (x - w * .1, y - h), (x + w * .45, y - h * .9), (x + w * .5, y)]
        s.append(f'<path class="men" d="{poly_d(P)}"/><path class="menl" d="{poly_d([P[0], P[1], P[2], (x - w * .05, y)])}"/>')
        s.append(f'<g opacity=".5">{rune_cut(rn, x - 4, y - h * .72, .38, col, groove=2.2, core=.9, glow=.6)}</g>')
    return ''.join(s), ''.join(rims)

# ------------------------------------------------------------------------------------------------ floor and hearth
def floor():
    rng = random.Random(9); s = []; fills = {}; rims = []; fp = []
    VX, VY = 700, 120
    rows = [790, 808, 832, 864, 906, 960, 1030]
    for i in range(len(rows) - 1):
        ya, yb = rows[i], rows[i + 1]
        n = 7 + i
        step = 1700 / n; off = rng.uniform(0, step)
        xs = [-250 + off + k * step + rng.uniform(-step * .18, step * .18) for k in range(n + 2)]
        def at(xb, y): return VX + (xb - VX) * (y - VY) / (1000 - VY)
        for k in range(len(xs) - 1):
            g = 3 + i * .9
            a, b = xs[k] + g, xs[k + 1] - g
            P = [(at(a, ya + g * .5), ya + g * .5), (at(b, ya + g * .5), ya + g * .5), (at(b, yb - g * .5), yb - g * .5), (at(a, yb - g * .5), yb - g * .5)]
            if rng.random() < .5: P.insert(1, (lerp(P[0][0], P[1][0], .9), ya + g * .5 + rng.uniform(2, 6)))
            fill = rng.choice(['url(#sB1)', 'url(#sB2)', 'url(#sB4)'])
            fills.setdefault(fill, []).append(poly_d(P)); rims.append(f'M{f(P[0][0])} {f(P[0][1])}L{f(P[-3][0] if len(P) > 4 else P[1][0])} {f(P[0][1])}')
            for _ in range(1 + (i > 2) + (i > 4)):
                cx = rng.uniform(min(P[0][0], P[-1][0]) + 6, max(P[1][0], P[2][0]) - 6); cy = rng.uniform(ya + 4, yb - 4)
                fp.append((cx, cy, rng.uniform(.6, 2.2) * (1 + i * .25)))
    s.append('<rect x="-100" y="780" width="1400" height="300" class="jt"/>')
    for fill, ds in fills.items(): s.append(f'<path d="{"".join(ds)}" fill="{fill}"/>')
    s.append(f'<path d="{"".join(rims)}" stroke="#FFB070" stroke-opacity=".12" stroke-width="1"/>' + pits_paths(fp))
    s.append('<rect class="wash" x="-100" y="780" width="1400" height="300"/><rect class="floorfade" x="-100" y="780" width="1400" height="60"/>')
    # by day the dawn is at the upper right: the stone and the plinth throw long shadows across the flags to the lower left
    s.append('<path class="dayshade" d="M404 878 L992 874 L760 1010 L60 1010 Z M168 800 L340 800 L250 1010 L-40 1010 Z"/>')
    return ''.join(s)

def coals(rng, n, x0, x1, ybase, heap, rmin, rmax, salts=.1, hotx=650, crack_cls=''):
    """Lumps that glow from within: a dark crust lit on its top edges, and fissures through each one as tapered wedges,
    hottest at their middle, with heat bleeding onto the crust round them. Only the coals under the plumes are white-hot."""
    body, lit, core, bleed, edge = [], [], {}, {}, {}
    for _ in range(n):
        cx = rng.uniform(x0, x1); heat = math.exp(-((cx - hotx) / 270) ** 2)
        cy = ybase - heat * heap + rng.uniform(-6, 5); r = rng.uniform(rmin, rmax) * (1 - .25 * heat)
        m = rng.randint(5, 7); P = [(cx + math.cos(a) * r * rng.uniform(.7, 1.05), cy + math.sin(a) * r * rng.uniform(.5, .78)) for a in [k * 6.283 / m + rng.uniform(-.25, .25) for k in range(m)]]
        body.append(poly_d(P))
        top = sorted(range(m), key=lambda i: P[i][1])[:3]
        lit.append(poly_d([P[i] for i in sorted(top)] + [(cx, cy)]))
        hot = '#FFF4D8' if heat > .8 else '#FFC24D' if heat > .45 else '#FF8A2A'
        if rng.random() < salts: hot = rng.choice(['#8FB4FF', '#6BEBB4', '#C9A2FF'])
        i0 = rng.randrange(m); i1 = (i0 + m // 2 + rng.choice((0, 1))) % m
        a_ = (lerp(P[i0][0], cx, .25), lerp(P[i0][1], cy, .25)); b_ = (lerp(P[i1][0], cx, .25), lerp(P[i1][1], cy, .25))
        mid = (cx + rng.uniform(-r * .15, r * .15), cy + rng.uniform(-r * .1, r * .1))
        dx, dy = b_[0] - a_[0], b_[1] - a_[1]; L = math.hypot(dx, dy) or 1; nx, ny = -dy / L, dx / L
        wd = r * (.09 + .07 * heat)
        wedge = lambda k: poly_d([a_, (mid[0] + nx * wd * k, mid[1] + ny * wd * k), b_, (mid[0] - nx * wd * k, mid[1] - ny * wd * k)])
        core.setdefault(hot, []).append(wedge(1)); bleed.setdefault(hot, []).append(wedge(2.6))
        tp = sorted((P[i] for i in top), key=lambda q: q[0])
        edge.setdefault('#FFB070' if heat > .3 else '#C8603A', []).append('M' + 'L'.join(f'{f(x)} {f(y)}' for x, y in tp))
    s = [f'<path d="{"".join(body)}" fill="#1A0F0E"/>', f'<path d="{"".join(lit)}" fill="#5A3020" opacity=".5"/>']
    s.append(f'<g class="{crack_cls}">' if crack_cls else '<g>')
    for col, ds in bleed.items(): s.append(f'<path d="{"".join(ds)}" fill="{col}" opacity=".22"/>')
    for col, ds in core.items(): s.append(f'<path d="{"".join(ds)}" fill="{col}"/>')
    s.append('</g>')
    for col, ds in edge.items(): s.append(f'<path d="{"".join(ds)}" fill="none" stroke="{col}" stroke-width="1" stroke-linejoin="round" stroke-opacity=".6"/>')
    return ''.join(s)

def hearth_back():
    rng = random.Random(17); s = ['<g id="hz-hearth">']
    x0, x1, top, base = 340, 1062, 412, 802
    bed = [(346, 404), (360, 380), (430, 372), (520, 360), (600, 350), (680, 348), (760, 356), (860, 364), (960, 372), (1040, 382), (1056, 404)]
    s.append(f'<path d="{poly_d(bed)}" fill="url(#bedG)"/>')
    s.append('<ellipse cx="650" cy="372" rx="300" ry="34" fill="url(#coalGlow)" filter="url(#gl12)"/>')
    s.append(coals(rng, 64, 360, 1040, 392, 30, 11, 22, .08))
    courses = [(top, 470), (470, 540), (540, 612), (612, 690), (690, base)]
    fills = ['url(#sB1)', 'url(#sB2)', 'url(#sB3)', 'url(#sB4)']
    s.append(f'<rect x="{x0}" y="{top}" width="{x1 - x0}" height="{base - top}" class="jt"/>')
    blocks = []
    for ci, (ya, yb) in enumerate(courses):
        x = x0 + (ci % 2) * rng.uniform(30, 70) - 40
        while x < x1:
            w = rng.uniform(90, 170); a, b = max(x, x0), min(x + w, x1)
            if b - a > 20:
                g = 2.5; c1, c2 = rng.uniform(3, 9), rng.uniform(3, 9)
                P = [(a + g + c1, ya + g), (b - g - c2, ya + g), (b - g, ya + g + c2), (b - g, yb - g - rng.uniform(0, 5)), (b - g - rng.uniform(0, 6), yb - g), (a + g, yb - g), (a + g, ya + g + c1)]
                blocks.append((P, rng.choice(fills)))
            x += w
    for P, fill in blocks:
        s.append(stone([(P, fill, rng.choice([80, 95, 70]))], rng.randrange(1 << 30), u=2.6, pits=8, cracks=1, chisel=4,
                       rims=[([P[0], P[1]], '#FFB070', .32, 1.2), ([P[1], P[2], P[3]], '#8FA6D6', .1, 1)]))
    # the fire lights the face from above: brightest under the flames, falling off to the ends and down
    s.append(f'<rect x="{x0}" y="{top}" width="{x1 - x0}" height="{base - top}" fill="url(#hearthRad)"/>')
    # the anvil's contact shadow on the face behind it
    s.append(f'<g transform="{M} translate(0 5)" opacity=".5" filter="url(#gl12)"><path d="{ANVIL_D}" fill="#000"/></g>')
    s.append(rune_cut('dagaz', 366, 490, 1.4, 'gold', groove=8, core=2.4, glow=.5))
    s.append(rune_cut('othala', 1012, 488, 1.3, 'violet', groove=7, core=2.2, glow=.5))
    s.append('</g>')
    s.append(plinth())
    return ''.join(s)

def hearth_front():
    rng = random.Random(23); s = ['<g id="hz-front">']
    x0, x1 = 334, 1068
    s.append(coals(rng, 40, 350, 1050, 404, 8, 12, 21, .14))
    x = x0; caps = []
    while x < x1:
        w = rng.uniform(120, 200); b = min(x + w, x1)
        P = [(x + 3, 404), (b - 3, 404 + rng.uniform(-2, 2)), (b - 1, 410), (b - 2, 432), (x + 2, 432), (x + 1, 410)]
        caps.append(P); x = b
    for P in caps:
        heat = math.exp(-(((P[0][0] + P[1][0]) / 2 - 650) / 330) ** 2)
        s.append(stone([(P, 'url(#sB3)', 0)], int(P[0][0]), u=2.4, pits=10, cracks=0, chisel=4,
                       rims=[([P[5], P[0], P[1], P[2]], '#FFC48A', .35 + .5 * heat, 1.6)]))
        s.append(f'<path d="{poly_d([P[5], P[0], P[1], P[2]])}" fill="url(#bevel)" opacity="{.3 + .5 * heat:.2f}"/>')
    s.append('</g>')
    return ''.join(s)

# ------------------------------------------------------------------------------------------------ the stone and anvil
def seam_pool():
    """The molten seam: a pool with a meniscus climbing the anvil's foot, rounded ends, spilling a little past the near
    corner; a white-hot core, dark skin islands, drips, and its light cast down the stone."""
    rng = random.Random(4)
    bot = [(x, 151.2 + rng.uniform(-.4, .5) + (1.6 * math.exp(-((x - 182) / 7) ** 2))) for x in range(184, 70, -6)]
    pool = ('M66.4 148.8 Q66.2 146.6 69.6 146.3 L82.6 145.9 Q84 144.6 85.2 145.6 H170.8 Q172 144.6 173.4 145.9 L186.6 146.4 Q192.6 146.9 192.8 149.2 '
            'Q192.6 153.6 186 153.4 ' + ' '.join(f'L{f(x)} {f(y)}' for x, y in bot) + ' L70 151.2 Q66.6 150.8 66.4 148.8 Z')
    core = 'M74 147.6 Q74 146.8 76 146.8 H180 Q183 146.8 183 148 Q183 149.4 180 149.4 H76 Q74 149.4 74 147.6 Z'
    skins = ''.join(poly_d([(x + rng.uniform(-1, 1) * w * .5 + dx * w, 148 + dy * 1.3) for dx, dy in ((-.5, -.4), (.2, -.6), (.6, .1), (.1, .6), (-.4, .4))])
                    for x, w in ((80, 4), (101, 3), (127, 3.4), (149, 2.6), (177, 4)))
    s = ('<path d="M70 151 L186 151 L194 176 L62 176 Z" fill="url(#seamCast)" style="mix-blend-mode:screen"/>'
         '<path d="M68 148 H190" stroke="#FF6A1E" stroke-width="7" stroke-opacity=".35"/>'
         f'<path d="{pool}" fill="url(#seamU)"/><path d="{core}" fill="#FFFBEE" opacity=".85"/>'
         f'<path d="{skins}" fill="#4A1A0C" opacity=".7"/><path d="M85.2 145.6 H170.8" stroke="#FFF4D8" stroke-width=".7" opacity=".8"/>')
    for x, L in ((80, 6), (97, 3.5), (141, 8), (162, 4.5), (181, 6.5)):
        s += f'<path d="M{x - .9} 151 Q{x - .8} {151 + L * .7} {x} {151 + L} Q{x + .8} {151 + L * .7} {x + .9} 151 Z" fill="url(#drip)"/>'
    return s

def tongs():
    """Real tongs in the mark's grid: two jaws biting the billet's end, a riveted boss, reins running off to the smith."""
    return ('<g class="tongs">'
            '<path d="M168 82.2 L330 121.3 L330 125.9 L167 85 Z" fill="url(#ironRein)"/><path d="M168 85.6 L330 130.3 L330 135.1 L166.4 88.6 Z" fill="url(#ironRein)"/>'
            '<path d="M168 82.2 L330 121.3" stroke="#C9B6A6" stroke-opacity=".55" stroke-width=".5"/><path d="M168 85.6 L330 130.3" stroke="#C9B6A6" stroke-opacity=".4" stroke-width=".45"/>'
            '<path d="M146.5 78.6 L158 77.8 L168 81.2 L167 84.6 L157 81.2 L146.5 81.4 Z" fill="#2A2C33"/><path d="M146.5 78.6 L158 77.8 L168 81.2" stroke="#FFC48A" stroke-opacity=".55" stroke-width=".5" fill="none"/>'
            '<path d="M150.6 80.6 L152.8 80.6 L156 85.4 L166 86 L166.4 89 L154 88.4 L150.6 86.6 Z" fill="#202228"/>'
            '<path d="M162.6 81 l2.6 -1 l2.6 1.2 l.2 2.8 l-2.6 1.2 l-2.6 -1 Z" fill="#3E424C"/><path d="M163.4 81.2 l1.8 -.6" stroke="#E6D2C0" stroke-width=".5"/></g>')

def anvil_stone():
    s = [f'<g id="hz-anvil"><g transform="{M}">']
    s.append('<ellipse cx="128" cy="236" rx="102" ry="6" fill="#000" opacity=".55" filter="url(#soft)"/>')
    avoid = [(50, 168, 82, 210), (96, 168, 120, 210), (124, 168, 150, 210), (146, 168, 174, 210), (180, 172, 204, 210)]
    s.append(stone([(STONE_L, 'url(#sL)', 76), (STONE_M, 'url(#sM)', 88), (STONE_R, 'url(#sR)', 100)], 77, u=.42, pits=170, cracks=6, chisel=110, hatch='lines', sp=4.2,
                   avoid=avoid, rims=[([(46, 150), (34, 190), (40, 226)], '#FFB070', .5, 1.2), ([(206, 150), (220, 186), (212, 228)], '#8FA6D6', .3, 1.1),
                                      ([(92, 148), (86, 232)], '#000', .45, .9), ([(170, 146), (176, 234)], '#000', .45, .9),
                                      ([(46, 150), (92, 148), (170, 146), (206, 150)], '#FFC48A', .6, .9)]))
    s.append('<path d="M46,150 L92,148 L86,232 L40,226 L34,190 Z M92,148 L170,146 L176,234 L86,232 Z M170,146 L206,150 L220,186 L212,228 L176,234 Z" fill="url(#forgeSide)" style="mix-blend-mode:screen"/>')
    s.append('<path d="M46 150 L92 148 L170 146 L206 150 L203 153.5 L170 150 L92 152 L48 154 Z" fill="url(#bevel)"/>')
    s.append(band(BAND_T, BAND_B, RIVETS, u=.95))
    for name, x, y, col in FRONT_RUNES: s.append(rune_cut(name, x, y, 1, col))
    s.append(f'<g opacity=".8">{rune_cut("fehu", 41, 200, .55, "white", groove=3, core=1.1)}{rune_cut("sowilo", 204.5, 207, .42, "green", groove=2.6, core=1)}</g>')
    s.append(seam_pool())
    s.append(anvil())
    s.append('</g></g>')
    return ''.join(s)

def billet():
    """The workpiece, its own layer so each blow can flatten it. Hot steel, not a painted bar. Under everything, the floor of
    its heat: orange-hot along its length, dull red in the jaws (`billetW`), so between blows it cools through colour and
    never to the brown of cold steel. Over that, the fresh heat (`.barhot`): white-yellow where the hammer lands, fading
    each blow; its light on the anvil's face and in the air round it (`.barglow`) fades with it but never goes out. The
    edge darkening and the scale (on the free end, the coolest) sit on top, so the bar keeps its form at any heat."""
    rng = random.Random(8); X0, Y0 = sc(112, 80); X1, Y1 = sc(150, 87); w, h = X1 - X0, Y1 - Y0
    hx, my = X0 + w * .78, (Y0 + Y1) / 2 + 2                  # where the hammer lands (STRIKE), the hottest
    sp = ''.join(circ(rng.uniform(X0 + 4, X0 + 26), rng.uniform(Y0 + 6, Y1 - 2), rng.uniform(.5, 1.1)) for _ in range(6))
    body = f'M{f(X0)} {f(Y0 + 4)} L{f(X0 + 3)} {f(Y0)} L{f(X1 - 3)} {f(Y0)} L{f(X1)} {f(Y0 + 4)} L{f(X1)} {f(Y1)} L{f(X0)} {f(Y1)} Z'
    topf = f'M{f(X0 + 3)} {f(Y0)} L{f(X1 - 3)} {f(Y0)} L{f(X1)} {f(Y0 + 4)} L{f(X0)} {f(Y0 + 4)} Z'
    inner = (f'<g class="barglow"><ellipse cx="{f(hx - w * .1)}" cy="{f(Y1 + 2)}" rx="{f(w * .85)}" ry="12" fill="url(#faceGlow)"/>'      # its light on the anvil's face
             f'<path d="M{f(X0 - 14)} {f(Y0 - 12)} H{f(X1 + 4)} V{f(Y1 + 8)} H{f(X0 - 14)} Z" fill="url(#barGlow)"/></g>'                # and in the air round it
             f'<g class="bil"><path d="{body}" fill="url(#billetW)"/><path d="{topf}" fill="url(#billetWTop)"/></g>'
             f'<g class="barhot"><path d="{body}" fill="url(#billetH)"/><path d="{topf}" fill="url(#billetHTop)"/>'
             f'<ellipse cx="{f(hx)}" cy="{f(my)}" rx="{f(w * .24)}" ry="{f(h * .32)}" fill="url(#hotSpot)"/></g>'
             f'<path d="{body}" fill="url(#edgeDark)"/><path d="{sp}" fill="#3A1408" opacity=".3"/>'
             f'<path d="M{f(X0 + 1)} {f(Y1 - 1)} H{f(X1)}" stroke="#5A1408" stroke-width="2" opacity=".7"/>'
             f'<path class="bflare" d="{body}" fill="#FFFDF4" opacity="0"/>')
    box = (X0 - 20, Y0 - 20, w + 40, h + 40)
    return ov(W, H, box, inner, 'billet', f'transform-origin:50% {(Y1 - box[1]) / box[3] * 100:.1f}%', 'id="billet"')

def tongs_ov():
    """The tongs on their own sheet over the whole scene (placed by its class, `.scene .tongs`), so that every fifth blow
    they can carry the billet back into the fire. The reins run on past the scene's edge to the smith."""
    return f'<svg class="tongs" viewBox="0 0 1200 1000" aria-hidden="true"><g id="hz-tongs" transform="{M}">{tongs()}</g></svg>'

# ------------------------------------------------------------------------------------------------ the light rig
def lightrig_floor():
    """Under the anvil, over the floor: the fire's pool on the near flags, and the stone's shadow thrown toward us."""
    pool = ov(W, H, (100, 760, 1100, 260), '<ellipse cx="650" cy="880" rx="560" ry="120" fill="url(#halo)"/><ellipse cx="700" cy="900" rx="300" ry="60" fill="url(#halo)"/>', 'lite pool')
    shad = ov(W, H, (300, 860, 800, 160), '<path d="M402 878 L990 878 L1080 1010 L320 1010 Z" fill="url(#shadG)"/><path d="M420 878 L972 878 L1010 920 L380 920 Z" fill="url(#shadG)" opacity=".7"/>', 'shad', 'transform-origin:58% 10%')
    return pool, shad

def lightrig_fore():
    """On the anvil, screen-blended and capped: the fire's light falling off along the face from the fire's end, the flames'
    reflection breathing in it, and the horn's specular catching the flicker. No filters: its opacity moves every frame."""
    refl = ''.join(f'M{x - w * 1.3} 86.4 Q{x} {86.4 - L * 1.5} {x + w * 1.3} 86.4 Q{x} {86.4 - L * .5} {x - w * 1.3} 86.4 Z' for x, w, L in FACE_REFL)
    face = (f'<g transform="{M}" opacity=".42"><path d="{ANVIL_TOP}" fill="url(#faceFall)"/><path d="{refl}" fill="#FFC060" opacity=".8"/>'
            '<path d="M72 86.6 H164 C176 86.6 196 90.6 220 96.4" fill="none" stroke="url(#faceFall)" stroke-width="1.4"/>'
            '<path d="M168 89.8 C184 90.4 198 93 214 96.6" fill="none" stroke="#EAF2FF" stroke-width=".9" stroke-linecap="round"/></g>')
    X0, Y0 = sc(50, 80); X1, Y1 = sc(226, 104)
    return ov(W, H, (X0, Y0, X1 - X0, Y1 - Y0), face, 'lite anv')

# ------------------------------------------------------------------------------------------------ stills
def static_fx():
    """A still keeps a few embers aloft, not a frozen burst."""
    rng = random.Random(77); s = []
    for _ in range(14):
        x = rng.uniform(470, 980); y = rng.uniform(80, 330); c = rng.choice(['#FFC24D', '#FF9440', '#FFE9B0', '#45E0A0', '#BC8BFF'])
        s.append(f'<path d="M{f(x)} {f(y)} l.9 2.4 l-.9 1.6 l-.9 -1.6 Z" fill="{c}" opacity="{rng.uniform(.5, .9):.2f}"/>')
    return ''.join(s)

def static_flames():
    """The stills' fire is the live fire's geometry at one instant, placed where the loop places it."""
    return fire(BY, PLUMES, t=.35, sheet=(372, 1040, 52), cls=True, red=.42)

# ------------------------------------------------------------------------------------------------ the hammer
def hammer(hand=True):
    """Side-on cross-peen held by the smith. Local frame: the head's centre at 0,0, the handle along +x, the striking face at +y,
    the peen's wedge at -y with a hard shoulder. The fire side (-x, +y) takes a warm cheek and rim; a gloved fist grips the
    handle near its end, thumb wrapped over, and the bare forearm runs out of a leather cuff and out of frame."""
    rng = random.Random(3); s = ['<g class="hh">']               # the handle: what the heat haze bends (the head and fist stay crisp)
    end = 346 if hand else 496
    s.append(f'<path d="M24 -12 L{end - 70} -13 L{end - 18} -15 L{end - 6} -16 L{end} -9 L{end + 1} 0 L{end} 9 L{end - 6} 16 L{end - 18} 15 L{end - 70} 13 L24 12 Z" fill="url(#hWood)"/>')
    s.append(f'<path d="{"".join(f"M{f(x)} {f(y)} C{f(x + 60)} {f(y + rng.uniform(-2, 2))} {f(x + 130)} {f(y + rng.uniform(-2, 2))} {f(x + 200)} {f(y * 1.1)}" for x, y in ((rng.uniform(40, 100 if hand else 140), rng.uniform(-8, 8)) for _ in range(7)))}" fill="none" stroke="#1A0E08" stroke-opacity=".38" stroke-width="1"/>')
    s.append(f'<path d="M24 -12 L{end - 18} -15" stroke="#FFD2A0" stroke-opacity=".5" stroke-width="1.6"/><path d="M24 12 L{end - 18} 15" stroke="#000" stroke-opacity=".35" stroke-width="1.4"/></g>')
    head = [(-24, 64), (24, 64), (27, 58), (27, -18), (21, -26), (4, -86), (-4, -86), (-21, -26), (-27, -18), (-27, 58)]
    s.append(f'<path d="{poly_d(head)}" fill="url(#hSteelW)"/>')
    s.append(f'<path d="{poly_d(head)}" fill="url(#cheekG)"/>')     # the fire-side cheek: warm on the lower-left face, cold up and right
    s.append('<path d="M-21 -26 L-4 -86 L4 -86 L21 -26 Z" fill="#000" opacity=".12"/><path d="M-21 -26 L-4 -86 L-1 -86 L-14 -26 Z" fill="#FFC48A" opacity=".3"/>')  # the peen's wedge, its lit facet
    s.append('<path d="M-27 -18 H27 L21 -26 H-21 Z" fill="#000" opacity=".4"/><path d="M-27 -18 H27" stroke="#E8D2C0" stroke-opacity=".35" stroke-width="1.2"/>')   # the hard shoulder
    s.append('<path d="M-4 -86 H4" stroke="#FFE6CC" stroke-width="2.4"/>')
    s.append('<path d="M-24 64 L24 64 L27 58 L-27 58 Z" fill="#E8DCCF"/><path d="M-24 65.4 H24" stroke="#FFFFFF" stroke-width="2.2"/>'
             '<path d="M-18 61 h6 M-6 60.6 h4 M6 61.2 h7" stroke="#FFB050" stroke-width="1.6" opacity=".75"/>')      # the face, the flames caught in it
    s.append('<path d="M-27 58 V-18 L-21 -26 L-4 -86" fill="none" stroke="#FF9A5A" stroke-opacity=".8" stroke-width="2"/><path d="M27 58 V-18 L21 -26 L4 -86" fill="none" stroke="#8FA6D6" stroke-opacity=".4" stroke-width="1.4"/>')
    s.append('<path d="M27 -14 L36 -16 L36 16 L27 14 Z" fill="#3E424C"/><path d="M27 -14 L36 -16" stroke="#FFD2A0" stroke-opacity=".5"/>')
    s.append(f'<path d="{"".join(circ(rng.uniform(-24, 24), rng.uniform(-20, 54), rng.uniform(.3, .9)) for _ in range(36))}" fill="#000" opacity=".3"/>')
    if not hand: return ''.join(s)
    s.append(fist())
    return ''.join(s)

FIST_D = (.7071, -.7071)        # the forearm's run from the wrist, in the hammer's frame: up the peen side and back
def fist():
    """The smith's right hand, gloved, seen from its back: one mass, the knuckles a ridge along the handle, the fingers'
    gaps only shadow lines, the wrap a curved ridge where the fingers turn under, the thumb laid across the index finger;
    a flared gauntlet cuff; the bare forearm a tapering limb with a terminator and a warm rim on the fire side, ending in
    a rolled linen sleeve. The fire side (toward -x and +y) is lit warm; the far side takes the cold sky."""
    dx, dy = FIST_D; nx, ny = -dy, dx                        # n: across the arm, toward the fire side
    def at(s_, w_, c=(318, -58)): return (c[0] + dx * s_ + nx * w_, c[1] + dy * s_ + ny * w_)
    def pts(P): return ' '.join(f'{f(x)} {f(y)}' for x, y in P)
    o = []
    # the sleeve, linen, out of frame; then its roll
    o.append(f'<path d="M{pts([at(232, -38)])} L{pts([at(380, -42)])} L{pts([at(380, 40)])} L{pts([at(232, 36)])} Z" fill="url(#sleeveG)"/>')
    o.append(f'<path d="M{pts([at(260, -36)])} Q{pts([at(268, -6)])} {pts([at(262, 36)])} M{pts([at(300, -40)])} Q{pts([at(306, 0)])} {pts([at(298, 38)])}" fill="none" stroke="#2A221A" stroke-opacity=".45" stroke-width="1.6"/>')
    # the forearm: a tapering limb, the far half in shadow, a soft terminator, the near edge lit by the fire
    # far edge: the wrist, then the muscle's belly swelling toward the elbow; near edge: flatter, the ulna's line
    far_ = 'M' + pts([at(22, -17)]) + ' C' + pts([at(60, -18), at(95, -27), at(140, -33)]) + ' C' + pts([at(180, -37), at(214, -34), at(238, -31)])
    near_ = ' L' + pts([at(238, 29)]) + ' C' + pts([at(200, 28), at(150, 25), at(110, 23)]) + ' C' + pts([at(70, 21), at(40, 17), at(22, 15)]) + ' Z'
    o.append(f'<path d="{far_ + near_}" fill="url(#skinG)"/>')
    o.append(f'<path d="M{pts([at(34, -5)])} C{pts([at(90, -11), at(160, -14), at(236, -11)])}" fill="none" stroke="#3A1E14" stroke-opacity=".28" stroke-width="9"/>')     # the terminator, soft
    o.append(f'<path d="{far_}" fill="none" stroke="#8FA6D6" stroke-opacity=".22" stroke-width="1.4"/>')                                                             # the sky on the far side
    o.append(f'<path d="M{pts([at(22, 15)])} C{pts([at(40, 17), at(70, 21), at(110, 23)])} C{pts([at(150, 25), at(200, 28), at(238, 29)])}" fill="none" stroke="#FFA060" stroke-opacity=".8" stroke-width="2.6"/>')    # the warm rim
    o.append(f'<path d="M{pts([at(70, -14)])} C{pts([at(100, -20), at(130, -22), at(150, -20)])}" fill="none" stroke="#2A140C" stroke-opacity=".3" stroke-width="1.2"/>')    # the muscle's edge
    o.append(f'<path d="M{pts([at(236, -40)])} C{pts([at(226, -20), at(226, 18), at(236, 38)])} L{pts([at(214, 36)])} C{pts([at(202, 16), at(203, -20), at(214, -38)])} Z" fill="url(#rollG)"/>'
             f'<path d="M{pts([at(214, -38)])} C{pts([at(203, -20), at(202, 16), at(214, 36)])}" fill="none" stroke="#FFC890" stroke-opacity=".45" stroke-width="1.4"/>'
             f'<path d="M{pts([at(222, -36)])} C{pts([at(216, -14), at(218, 6), at(224, 20)])} M{pts([at(230, -18)])} C{pts([at(226, -6), at(227, 10), at(232, 26)])}" fill="none" stroke="#2A221A" stroke-opacity=".45" stroke-width="1.2"/>')     # the rolled sleeve, its folds
    # the gauntlet cuff, flared, curved, stitched; its hem lit on the fire side
    o.append(f'<path d="M{pts([at(-6, -28)])} Q{pts([at(-10, 0)])} {pts([at(-6, 27)])} C{pts([at(10, 30), at(28, 34), at(42, 34)])} Q{pts([at(48, 0)])} {pts([at(42, -38)])} C{pts([at(28, -38), at(10, -32), at(-6, -28)])} Z" fill="url(#cuffG)"/>')
    o.append(f'<path d="M{pts([at(36, -35)])} Q{pts([at(42, 0)])} {pts([at(36, 31)])}" fill="none" stroke="#E8C090" stroke-opacity=".45" stroke-width="1" stroke-dasharray="3 3"/>'
             f'<path d="M{pts([at(42, -38)])} Q{pts([at(48, 0)])} {pts([at(42, 34)])}" fill="none" stroke="#1A0E08" stroke-width="2.2"/>'
             f'<path d="M{pts([at(-6, 27)])} C{pts([at(10, 30), at(28, 34), at(42, 34)])}" fill="none" stroke="#FFB070" stroke-opacity=".8" stroke-width="2"/>')
    # the fist: one mass from the knuckle ridge to the wrist, the fingers curled under the handle
    mass = ('M300 -77 C288 -66 268 -50 255 -40 C249 -36 245 -30 245 -22 C244 -8 245 6 249 15 C252 21 258 23 266 22 '
            'C274 24 282 24 290 23 C298 24 306 23 314 21 C322 20 330 16 333 8 C337 -6 337 -22 336 -40 Z')
    o.append(f'<path d="{mass}" fill="url(#gloveG)"/>')
    knuckles = [(260.5, -41.6, 7.2, 4.4, -8, .9), (278.6, -43.4, 9.4, 5.6, -3, 1), (296.2, -42.2, 8.1, 4.9, 4, .85), (314.8, -38.6, 6.3, 4.1, 12, .7)]   # each its own size, lean and light
    o.append(''.join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" transform="rotate({r} {x} {y})" fill="url(#knuckleG)" opacity="{a}"/>' for x, y, rx, ry, r, a in knuckles))   # the knuckles, raised under the leather
    o.append('<path d="M269.6 -44 C272 -28 270 -6 268 21 M287.6 -45 C289 -26 288 -4 286 22 M305.4 -42.6 C306 -26 305 -4 303 21" fill="none" stroke="#0C0705" stroke-opacity=".6" stroke-width="1.5"/>')  # the gaps between the fingers
    o.append('<path d="M250 6 C268 12 300 13 333 5" fill="none" stroke="#7A5A40" stroke-opacity=".35" stroke-width="2.2"/>'
             '<path d="M252 13 C270 20 302 20 331 13 C326 20 318 23 300 23 C286 25 268 24 256 21 Z" fill="#0A0604" opacity=".45"/>')                 # the wrap: the ridge where the fingers turn under, the curl in shadow
    o.append('<path d="M300 -77 C296 -64 300 -50 312 -42 M318 -70 C318 -58 322 -50 330 -44" fill="none" stroke="#0C0705" stroke-opacity=".4" stroke-width="1.2"/>')   # the glove's points
    o.append('<path d="M245 -22 C244 -8 245 6 249 15 C252 21 258 23 266 22" fill="none" stroke="#FFB070" stroke-opacity=".75" stroke-width="2"/>')                    # the fire side
    # the thumb, laid across the index finger, its tip resting on the middle finger
    thumb = 'M246 -30 C240 -20 242 -8 252 -2 C260 2 272 4 282 1 C287 -1 287 -7 282 -9 C274 -11 264 -13 259 -18 C255 -22 253 -28 250 -33 Z'
    o.append(f'<path d="{thumb}" fill="url(#thumbG)"/><path d="M246 -30 C240 -20 242 -8 252 -2 C260 2 272 4 282 1" fill="none" stroke="#0A0604" stroke-opacity=".5" stroke-width="1.4"/>'
             '<path d="M250 -33 C253 -28 255 -22 259 -18 C264 -13 274 -11 282 -9" fill="none" stroke="#8A6A50" stroke-opacity=".4" stroke-width="1.6"/>')
    o.append('<path d="M226 -12 L240 -12 L240 12 L226 12 Z" fill="#000" opacity=".25"/>')                                                    # the hand's shadow on the handle
    return ''.join(o)

HAMMER_BOX = (-40, -335, 640, 415)   # local box of the hammer svg (the forearm runs up to -320)
POSE_RAISED = (870, 84, 46)          # the pose every still freezes on

# ------------------------------------------------------------------------------------------------ the bellows
# Great bellows, pear-shaped (about 1.6:1), seen from above at an angle: the bottom board resting in a cradle on a stone
# plinth built against the hearth, the top board hinged at the neck, the pleated leather belly swelling between them,
# an iron nozzle running into the hearth wall. Rig frame: u runs from the back (-142) to the neck (0); v across the board.
BW = (318, 446, 3)                   # the neck (hinge) in scene units, and the rig's tilt
BW_HALF = [(0, 10), (-15, 13), (-35, 22), (-60, 34), (-85, 42), (-105, 44), (-122, 40), (-134, 30), (-140, 15), (-142, 0)]
BW_K, BW_T, BW_G, BW_N = .38, 7, 6, 5     # foreshortening across the board, board thickness, gap at the hinge, pleats
def bw_theta(b): return 6 + 10 * b        # the top board's opening, degrees, for openness b (0 shut .. 1 open)

def bellows_paths(b):
    """(light folds, dark folds, fold lines, top-board transform) in the rig frame. Mirrors page.js bellows()."""
    tn = math.tan(math.radians(bw_theta(b))); bul = .08 + .22 * b
    def ring(k):
        e = bul * math.sin(math.pi * k)
        return [(u * (1 + e * .25), w * (1 + e) * BW_K - k * (BW_G - u * tn)) for u, w in BW_HALF]
    R = [ring(i / BW_N) for i in range(BW_N + 1)]
    light = ''.join(poly_d(R[i] + R[i + 1][::-1]) for i in range(0, BW_N, 2))
    dark = ''.join(poly_d(R[i] + R[i + 1][::-1]) for i in range(1, BW_N, 2))
    folds = ''.join('M' + 'L'.join(f'{f(x)} {f(y)}' for x, y in R[i]) for i in range(1, BW_N))
    return light, dark, folds, f'matrix(1 {tn:.4f} 0 1 0 {-BW_G})'

def _pear(dy=0):
    near = [(u, w * BW_K + dy) for u, w in BW_HALF]; far_ = [(u, -w * BW_K + dy) for u, w in reversed(BW_HALF)]
    return near, far_

def plinth():
    """The bellows' plinth: dry-laid courses against the hearth's left end, a capstone, a wooden cradle on it."""
    rng = random.Random(29); blocks = []
    for ya, yb in ((478, 548), (548, 624), (624, 706), (706, 802)):
        x = 170 + rng.uniform(-14, 6)
        while x < 340:
            w_ = rng.uniform(48, 90); a_, b_ = max(x, 168), min(x + w_, 340)
            if b_ - a_ > 16: blocks.append([(a_ + 2.5, ya + 2), (b_ - 2.5, ya + 2), (b_ - 2.5, yb - 2), (a_ + 2.5, yb - 2)])
            x += w_
    out = ''.join(stone([(P, rng.choice(['url(#sB1)', 'url(#sB2)', 'url(#sB4)']), 80)], rng.randrange(1 << 30), u=2.4, pits=6, cracks=1, chisel=3,
                        rims=[([P[0], P[1]], '#FFB070', .22, 1), ([P[1], P[2]], '#FF9A5A', .3, 1.2)]) for P in blocks)
    cap = [(162, 466), (342, 462), (344, 480), (164, 482)]
    return (f'<path d="M166 470 H340 V802 H166 Z" class="jt"/>{out}'
            + stone([(cap, 'url(#sB3)', 0)], 41, u=2.4, pits=10, cracks=0, chisel=4, rims=[([cap[0], cap[1]], '#FFC48A', .4, 1.4), ([cap[1], cap[2]], '#FF9A5A', .5, 1.4)])
            + '<path d="M196 468 L204 450 L214 450 L222 468 Z M284 468 L292 452 L302 452 L310 468 Z" fill="url(#wood)"/>'
              '<path d="M204 450 H214 M292 452 H302" stroke="#FFC48A" stroke-opacity=".4"/>')

def bellows_static():
    hx, hy, ang = BW
    light, dark, folds, top_tf = bellows_paths(.55)
    T = BW_T; near, far_ = _pear(); nearT, farT = _pear(-T)
    surf = poly_d(near + far_)
    edge = poly_d(near + [(u, y + T) for u, y in reversed(near)])          # the near edge of a board, its thickness
    surfT = poly_d(nearT + farT); edgeT = poly_d(nearT + [(u, y + T) for u, y in reversed(nearT)])
    grip = lambda dy: poly_d([(-138, -3 + dy), (-176, -2.4 + dy), (-184, .5 + dy), (-176, 3 + dy), (-138, 4 + dy)])
    studs = ''.join(circ(u, w * BW_K - T * .5, 1.3) for u, w in BW_HALF[1:8])
    grain = ''.join(f'M{-14 - i * 18} {f(-3 + (i % 3) * 3 - T)} l-14 {f(.6 - (i % 2) * 1.2)}' for i in range(7))
    return (f'<g transform="translate({hx} {hy}) rotate({ang})">'
            # the nozzle: a short iron cone from the neck into the hearth wall, a ring where it is bound to the boards
            '<path d="M-6 -12 L38 -6.5 L38 1.5 L-6 9 Z" fill="url(#hSteel)"/><path d="M-6 -12 L38 -6.5" stroke="#FFD2A0" stroke-opacity=".6"/><path d="M-6 9 L38 1.5" stroke="#000" stroke-opacity=".5"/>'
            '<path d="M-9 -14 L0 -14 L0 11 L-9 11 Z" fill="#2A2C33"/><path d="M-9 -14 H0" stroke="#FFC48A" stroke-opacity=".55"/>'
            '<path d="M34 -10 L44 -10 L46 -2.5 L44 5 L34 5 Z" fill="#14151A"/>'
            '<g id="bwMouth" style="opacity:.5"><path d="M38 -9 L48 -11 L52 -2.5 L48 6 L38 4 Z" fill="url(#halo)" transform="translate(-8 -14) scale(1.3)"/>'
            '<path d="M38 -5.5 L42 -6 L43 -2.5 L42 1 L38 .6 Z" fill="#FFD27A"/><path d="M39.5 -4 L41.5 -4.2 L42 -2.5 L41.5 -.8 L39.5 -1 Z" fill="#FFF6E0"/></g>'
            # the bottom board, its handle; the leather belly; the top board on its hinge
            f'<path d="{surf}" fill="url(#wood)"/><path d="{edge}" fill="#3A2216"/><path d="{grip(T * .5)}" fill="url(#wood)"/>'
            f'<path d="M{" L".join(f"{f(u)} {f(y + T)}" for u, y in near)}" fill="none" stroke="#000" stroke-opacity=".5"/>'
            f'<path id="bwLight" d="{light}" fill="url(#leatherB)"/><path id="bwDark" d="{dark}" fill="#2E140C"/>'
            f'<path id="bwFold" d="{folds}" fill="none" stroke="#120604" stroke-opacity=".7" stroke-width=".9"/>'
            f'<g id="bwTop" transform="{top_tf}"><path d="{edgeT}" fill="#4A2C1A"/><path d="{surfT}" fill="url(#woodTop)"/>'
            f'<path d="M{" L".join(f"{f(u)} {f(y)}" for u, y in farT)}" fill="none" stroke="#FFC48A" stroke-opacity=".55" stroke-width="1.2"/>'
            f'<path d="{grain}" stroke="#2A160C" stroke-opacity=".45"/><path d="{grip(-T * .5)}" fill="url(#wood)"/>'
            f'<path d="{studs}" fill="url(#brass)"/><path d="M-30 {-T - 2} L-118 {-T - 2}" stroke="#FFE2B8" stroke-opacity=".18" stroke-width="3"/></g></g>')

# ------------------------------------------------------------------------------------------------ near
def trough():
    """A stone quench trough seen a little from above: the water a dark mirror holding the forge's reflection, broken by
    ripples into sliding bands, two arcs of ripple, and its two runes wet-lit from below."""
    s = []
    F = [(1012, 816), (1158, 812), (1162, 898), (1018, 902)]
    T = [(1022, 784), (1150, 780), (1158, 812), (1012, 816)]
    s.append('<ellipse cx="1088" cy="906" rx="96" ry="8" fill="#000" opacity=".6" filter="url(#soft)"/>')
    s.append(stone([(F, 'url(#sB2)', 90), (T, 'url(#sT)', 0)], 31, u=2.2, pits=22, cracks=2, chisel=10,
                   rims=[([F[0], F[3]], '#FFB070', .5, 1.4), ([T[0], T[1]], '#FFC48A', .5, 1.2), ([F[0], F[1]], '#FFC48A', .35, 1.2)]))
    WATER = [(1032, 789), (1142, 786), (1148, 806), (1024, 809)]
    s.append(f'<path d="{poly_d(WATER)}" fill="url(#waterM)"/><path d="M1032 789 L1142 786 L1143 790 L1031 793 Z" class="wsheen"/>')
    # the forge mirrored in it, broken by ripples: the flames squashed and cut into bands that slide apart
    s.append('<path d="M1050 790 L1126 788 L1112 800 L1066 801 Z" fill="#FF8A2A" opacity=".18" filter="url(#gl6)"/>')
    s.append(broken_reflection(1086, 790.4, 807.5, 70, ('#FFF1C8', '#FFC24D', '#FF9440', '#E2481A', '#8A2410'), 31, lean=-3))
    s.append('<path d="M1088 801 A16 3.2 0 0 0 1120 801 M1078 803.6 A26 4.6 0 0 0 1130 803.6" fill="none" stroke="#FFD2A0" stroke-opacity=".22" stroke-width=".8" stroke-dasharray="7 3"/>'
             '<path d="M1032 789 L1142 786" stroke="#FFC48A" stroke-opacity=".4"/>')
    s.append(rune_cut('laguz', 1052, 842, 1.1, 'blue', groove=6, core=2))
    s.append(rune_cut('ingwaz', 1106, 840, 1.05, 'green', groove=6, core=2))
    s.append('<path d="M1040 896 H1140" stroke="#6E9BFF" stroke-opacity=".25" stroke-width="3"/>')
    return ''.join(s)

def steam_ov():
    """Two wisps off the trough's water, each its own layer animated whole (transform and opacity only, so the compositor moves them)."""
    return ''.join(ov(W, H, (x - 60, 620, 120, 190), wisp(x, 792, 54, 150, 90 + i, 'vapor', .3), 'stw', f'--i:{i}') for i, x in enumerate((1074, 1112)))

def near():
    rng = random.Random(51); s = []
    for P, rim in (([(-60, 1010), (-40, 930), (40, 900), (150, 918), (240, 960), (280, 1010)], [(-40, 930), (40, 900), (150, 918)]),
                   ([(1100, 1010), (1140, 958), (1200, 944), (1260, 960), (1260, 1010)], [(1140, 958), (1200, 944)])):
        s.append(f'<path d="{poly_d(P)}" class="nrock"/><path d="M{" L".join(f"{f(x)} {f(y)}" for x, y in rim)}" fill="none" stroke="#FF9A5A" stroke-opacity=".45" stroke-width="2.2" stroke-linecap="round"/>')
    for _ in range(24):
        x = rng.uniform(380, 1000); y = rng.uniform(890, 945)
        c = rng.choice(['#FF9440', '#FFC24D', '#E2481A', '#FF6A4A'])
        s.append(f'<path d="M{f(x - 2)} {f(y)} l2 -1 l2.4 .8 l-1.6 1.2 Z" fill="{c}" opacity="{rng.uniform(.35, .8):.2f}"/>')
    return ''.join(s)

# ------------------------------------------------------------------------------------------------ overlays
def overlays():
    """Composited layers over the scene: kindling runes, rivets set hot, the seam's breath."""
    o = []
    for i, (name, x, y, col) in enumerate(FRONT_RUNES):
        X, Y = sc(x - 6, y - 6); w = 34 * S; h = 46 * S
        o.append(ov(W, H, (X, Y, w, h), f'<g transform="{M}">{rune_glow(name, x, y, 1, col, w=2.4, gid="gl3", crawl=False)}</g>', 'rg', f'--i:{i}'))
        o.append(ov(W, H, (X, Y, w, h), f'<g transform="{M}">{crawl_path(name, x, y, 1, 2.4)}</g>', 'rgc'))
    for i, (x, y) in enumerate(RIVETS):
        X, Y = sc(x, y); r = 7 * S
        o.append(ov(W, H, (X - r, Y - r, 2 * r, 2 * r),
                    f'<circle cx="{f(X)}" cy="{f(Y)}" r="{f(5.5 * S)}" fill="url(#haloB)"/><circle cx="{f(X)}" cy="{f(Y)}" r="{f(2.5 * S)}" fill="url(#rivetHot)"/>', 'rv b', f'--i:{i}'))
        o.append(ov(W, H, (X - r, Y - r, 2 * r, 2 * r),
                    f'<circle cx="{f(X)}" cy="{f(Y)}" r="{f(5 * S)}" fill="url(#halo)"/><circle cx="{f(X)}" cy="{f(Y)}" r="{f(2.5 * S)}" fill="#FFB050"/>', 'rv g', f'--i:{i}'))
    rng = random.Random(12); X, Y = STRIKE
    spk = ''.join(f'<path d="M{f(X + math.cos(t) * a_)} {f(Y + math.sin(t) * a_)} L{f(X + math.cos(t) * (a_ + 16))} {f(Y + math.sin(t) * (a_ + 16))}" stroke="{c}"/>'
                  for t, a_, c in ((math.radians(rng.uniform(-175, -5)), rng.uniform(30, 120), rng.choice(['#FFE9B0', '#FFC24D', '#FF9440', '#EAF2FF', '#45E0A0'])) for _ in range(22)))
    o.append(ov(W, H, (X - 160, Y - 160, 320, 200), f'<ellipse cx="{X}" cy="{Y}" rx="150" ry="90" fill="url(#haloB)"/>{star4(X, Y, 46, "#F4F8FF")}'
                f'<g stroke-width="2" stroke-linecap="round">{spk}</g>', 'strikestill'))
    sx, sy = sc(56, 136)
    o.append(ov(W, H, (sx, sy, 144 * S, 30 * S), f'<g transform="{M}"><path d="M62 147.5 H194" stroke="#FFB03C" stroke-width="12" stroke-opacity=".18"/><path d="M64 147.5 H192" stroke="#FFB03C" stroke-width="6" stroke-opacity=".35"/><path d="M72 146.8 H184" stroke="#FFF8E6" stroke-width="1.4"/><path d="M70 151 L186 151 L194 168 L62 168 Z" fill="url(#seamCast)"/></g>', 'seamglow'))
    return ''.join(o)

def sky_static():
    """No-JS and still skies: the turning field frozen, small sharp stars; Otava in its true proportions near the pole."""
    rng = random.Random(11); s = []; bk = {}
    for _ in range(320):
        x = rng.uniform(0, 1440); y = rng.uniform(0, 900) ** 1.25 / 900 ** .25 * .92
        m = rng.random() ** 2.6; c = rng.random()
        col = '#FFD6A0' if c < .12 else '#AAC4FF' if c < .3 else '#EBF0FF'
        r = .4 + m * .7
        bk.setdefault((col, 0 if m < .2 else 1 if m < .5 else 2), []).append(f'M{f(x - r)} {f(y - r)}h{r * 2:.1f}v{r * 2:.1f}h{-r * 2:.1f}z')
    for (col, lv), ds in bk.items(): s.append(f'<path d="{"".join(ds)}" fill="{col}" opacity="{(.35, .6, .95)[lv]}"/>')
    px, py = 1066, 90; P = otava(px - 260, py + 30, 15)
    s.append('<path d="' + ' '.join(f'M{f(P[a][0])} {f(P[a][1])} L{f(P[b][0])} {f(P[b][1])}' for a, b in OTAVA_LINES) + '" stroke="#D4AE66" stroke-opacity=".3" stroke-width=".8" fill="none"/>')
    for x, y in P: s.append(f'<path d="M{f(x - 1.2)} {f(y - 1.2)}h2.4v2.4h-2.4z" fill="#FFF4DC"/>')
    s.append(star4(px, py, 12, '#F0D392'))
    return ''.join(s)

# Otava (the Big Dipper) from right ascension and declination, projected flat about its centre: RA grows to the left.
OTAVA = [(11.062, 61.75), (11.031, 56.38), (11.897, 53.69), (12.257, 57.03), (12.900, 55.96), (13.399, 54.93), (13.792, 49.31)]
OTAVA_LINES = [(0, 1), (1, 2), (2, 3), (3, 0), (3, 4), (4, 5), (5, 6)]
def otava(cx, cy, k):
    ra0, de0 = 12.4, 56
    return [(cx - (ra - ra0) * 15 * math.cos(math.radians(de)) * k, cy - (de - de0) * k) for ra, de in OTAVA]
