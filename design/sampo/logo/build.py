"""Build Sampo's anvil-stone logo files (design direction 12, the illustrated forge) from one drawing (T-2850).

Run from anywhere:

    python3 design/sampo/logo/build.py [OUT]

OUT defaults to this folder, so a plain run rewrites the committed files in place. Python's standard library and
rsvg-convert (librsvg) on PATH are all it needs. The drawing functions live in art.py, beside this file.

It writes, into OUT:
- the SVGs: mark (full, 96 px and up), mark-simple (32 to 96 px), icon-16 (the 16 px glyph), mark-animated,
  mark-light, mono, wordmark, app-icon, desktop-icon, readme-header-light, readme-header-dark and share;
- the PNGs, which rsvg-convert renders from those SVGs: app-icon-512, app-icon-1024, desktop-icon-1024 and share;
- favicon.ico, which packs icon-16.svg as rsvg-convert renders it at 16, 32 and 48 px.

The SVGs are byte-for-byte reproducible (seeded randomness, ids counted from zero per file, defs in a fixed order), and
test_sampo_design rebuilds them into a temp dir to check that. The PNG and .ico bytes depend on the rsvg-convert
version, so the test doesn't compare those.

The type is outlined from glyphs.json, which this folder keeps: the font-unit outlines and advances of only the glyphs
these files use, from Bodoni Moda (the word and the italic line) and Martian Mono (the kicker), both under the SIL Open
Font License, so outlining them for a logo is free. To re-extract them from a folder holding BodoniModa-normal.woff2,
BodoniModa-italic.woff2 and MartianMono-normal.woff2, which needs fontTools and brotli:

    uv run --with fonttools --with brotli python design/sampo/logo/build.py --glyphs FONTDIR
"""
import json
import math
import os
import random
import re
import struct
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GLYPHS = os.path.join(HERE, "glyphs.json")
sys.path.insert(0, HERE)
import art  # noqa: E402
from art import f, poly_d, rune_cut, stone, band, along, anvil, star4, circ, tongue, fire  # noqa: E402

WORD = "Sampo"
TAGLINE = "Your coding agent, with a smith on the job."
KICKER = "FORMERLY FOREMAN · DISCIPLINE FOR CODING AGENTS"
FACES = {"display": ("BodoniModa-normal.woff2", {"wght": 420, "opsz": 96}, WORD),
         "italic": ("BodoniModa-italic.woff2", {"wght": 400, "opsz": 28}, TAGLINE),
         "mono": ("MartianMono-normal.woff2", {"wght": 500}, KICKER)}

# the themes' roles the files use (tokens.json): the star is the accent by night and the bronze by day
DARK = {"ink": "#EEF0FA", "muted": "#9097BC", "brass": "#D4AE66", "star": "#F0D392"}
LIGHT = {"ink": "#12163A", "muted": "#555B80", "brass": "#7A5A26", "star": "#7A5A26"}

EXTRA_DEFS = (
    '<linearGradient id="seamU" x1="40" x2="216" y1="0" y2="0" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#7A1E10"/><stop offset=".18" stop-color="#E2481A"/><stop offset=".38" stop-color="#FFB03C"/><stop offset=".52" stop-color="#FFF8E6"/><stop offset=".66" stop-color="#FFB03C"/><stop offset=".86" stop-color="#E2481A"/><stop offset="1" stop-color="#7A1E10"/></linearGradient>'
    '<radialGradient id="forgeSide" cx="20" cy="240" r="230" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#FF8A2A" stop-opacity=".34"/><stop offset=".6" stop-color="#E0541A" stop-opacity=".08"/><stop offset="1" stop-color="#E0541A" stop-opacity="0"/></radialGradient>'
    '<linearGradient id="hWood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B07A4C"/><stop offset=".45" stop-color="#6E4428"/><stop offset="1" stop-color="#2E1A0E"/></linearGradient>'
    '<linearGradient id="hSteel" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9AA4B6"/><stop offset=".35" stop-color="#4E5562"/><stop offset="1" stop-color="#1B1E25"/></linearGradient>'
    '<linearGradient id="seamCast" x1="0" y1="151" x2="0" y2="176" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#FF8A3A" stop-opacity=".6"/><stop offset=".4" stop-color="#E0541A" stop-opacity=".22"/><stop offset="1" stop-color="#E0541A" stop-opacity="0"/></linearGradient>'
    '<linearGradient id="billetG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFD870"/><stop offset=".3" stop-color="#FFA43A"/><stop offset=".7" stop-color="#F06A1C"/><stop offset="1" stop-color="#B8301A"/></linearGradient>')
ALL_DEFS = art.DEFS + art.LOGO_FLAME_DEFS + EXTRA_DEFS


def defs_for(body):
    """Only the gradients, patterns and filters the drawing uses (and what those use), in ALL_DEFS order."""
    want, seen, found = set(re.findall(r'url\(#([\w-]+)\)', body)), set(), {}
    while want - seen:
        i = min(want - seen)
        seen.add(i)
        m = re.search(r'<(linearGradient|radialGradient|pattern|filter) id="%s"[\s\S]*?</\1>' % re.escape(i), ALL_DEFS)
        if m:
            found[m.start()] = m.group(0)
            want |= set(re.findall(r'url\(#([\w-]+)\)', m.group(0)))
    return '<defs>' + ''.join(found[k] for k in sorted(found)) + '</defs>'


def doc(w, h, body, title, extra='', vb=None):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb or f"0 0 {w} {h}"}" width="{w}" height="{h}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title>{extra}{defs_for(body)}{body}</svg>\n')


def sec(v):
    """Seconds for a CSS shorthand, always with a leading digit (0.4s, not .4s)."""
    return ('%.2f' % v).rstrip('0').rstrip('.') + 's'


# ---- one geometry: the stone's three facets and the anvil (art.ANVIL_D) are the same outlines in every file
STONE = ([(46, 150), (92, 148), (86, 232), (40, 226), (34, 190)], [(92, 148), (170, 146), (176, 234), (86, 232)],
         [(170, 146), (206, 150), (220, 186), (212, 228), (176, 234)])
STONE_D = ' '.join(poly_d(F) for F in STONE)
BAND_TOP, BAND_BOT = [(37, 160), (94, 157), (169, 155), (210, 159)], [(36, 170), (93, 167), (170, 165), (213, 169)]
RIV = along([(37, 162.6), (94, 159.6), (169, 157.6), (211, 161.6)], 9, .045, .955)
RUNES5 = [('algiz', 57, 172, 'blue'), ('thurs', 100, 172, 'gold'), ('wunjo', 128, 172, 'green'),
          ('ingwaz', 150, 172, 'violet'), ('kaun', 184, 172, 'red')]
PLUMES = [(128, 25, 82, 0, 1), (103, 15, 50, 1.7, 1), (154, 16, 56, 4.2, 0), (86, 8, 22, .9, 0), (171, 8, 26, 2.9, 0)]
SIMPLE_PLUMES = ((128, 27, 96, 0, 1), (98, 17, 56, 1.7, 0), (158, 18, 62, 4.2, 0))
BILLET = 'M112 81.4 L114 80 H148 L150 81.4 V87 H112 Z'
# the side-on hammer at mark scale: a short handle so it stays in the frame
_HD = [(-24, 64), (24, 64), (27, 58), (27, -26), (9, -86), (-9, -86), (-27, -26), (-27, 58)]
MINI_HAMMER = ('<g class="hm"><path d="M2.6 -1.4 L66 -2 L66 2 L2.6 1.4 Z" fill="url(#hWood)"/><path d="M2.6 -1.4 L66 -2" stroke="#FFD2A0" stroke-opacity=".5" stroke-width=".4"/>'
               f'<path d="{poly_d([(x * .11, y * .11) for x, y in _HD])}" fill="url(#hSteel)"/><path d="M-2.6 6.4 H2.6" stroke="#fff" stroke-width=".6"/>'
               '<path d="M-2.97 6.4 V-2.9 L-1 -9.5" fill="none" stroke="#FFB070" stroke-opacity=".6" stroke-width=".4"/></g>')
TITLE = ('Sampo: a steel anvil set into a rune-cut stone bound with nine rivets and a molten seam, a fire of many colours '
         'rising behind it, blue at the root into gold with green and violet tongues, one star above.')


def mark(animated=False, lite=False, star=DARK["star"]):
    """The full mark's body in its 256 grid: fire, faceted stone, band of nine rivets, five runes, molten seam, anvil,
    billet, one star. animated adds the hammer, sparks, flash, embers and the kindling layers the CSS drives."""
    s = ['<ellipse cx="128" cy="238" rx="100" ry="6" fill="#000" opacity=".5" filter="url(#soft)"/>',
         '<circle cx="128" cy="58" r="84" fill="url(#halo)"/>',
         f'{"<g class=\"fire\">" if animated else "<g>"}{fire(88, PLUMES, cls=animated)}</g>']
    S_L, S_M, S_R = STONE
    s.append(stone([(S_L, 'url(#sL)', 76), (S_M, 'url(#sM)', 88), (S_R, 'url(#sR)', 100)], 77, u=.42,
                   pits=36 if lite else 80, cracks=5, chisel=12 if lite else 50, hatch=None if lite else 'lines', sp=6,
                   avoid=[(50, 168, 82, 210), (96, 168, 120, 210), (124, 168, 150, 210), (146, 168, 174, 210), (180, 172, 204, 210)],
                   rims=[([(46, 150), (34, 190), (40, 226)], '#FFB070', .5, 1.2), ([(206, 150), (220, 186), (212, 228)], '#8FA6D6', .45, 1.1),
                         ([(92, 148), (86, 232)], '#000', .45, .9), ([(170, 146), (176, 234)], '#000', .45, .9),
                         ([(46, 150), (92, 148), (170, 146), (206, 150)], '#FFC48A', .55, .8)]))
    s.append(f'<path id="stone" d="{STONE_D}" fill="url(#forgeSide)" style="mix-blend-mode:screen"/>')
    s.append('<path d="M46 150 L92 148 L170 146 L206 150 L203 153.5 L170 150 L92 152 L48 154 Z" fill="url(#bevel)"/>')
    s.append(band(BAND_TOP, BAND_BOT, RIV, u=.95))
    if animated:
        s.append(''.join(f'<circle class="rv rv{i}" cx="{f(x)}" cy="{f(y)}" r="2.4"/>' for i, (x, y) in enumerate(RIV)))
    s.append('<g id="runes">' + ''.join(rune_cut(name, x, y, 1, col) for name, x, y, col in RUNES5) + '</g>')
    if animated:
        for i, (name, x, y, col) in enumerate(RUNES5):
            s.append(f'<g class="rg rg{i}">{art.rune_glow(name, x, y, 1, col, w=2.4, gid="gl3")}</g>')
    s.append(f'<g opacity=".8">{rune_cut("fehu", 41, 200, .55, "white", groove=3, core=1.1)}'
             f'{rune_cut("sowilo", 204.5, 207, .42, "green", groove=2.6, core=1)}</g>')
    s.append(f'<g class="seamg">{art.seam_pool()}</g>')
    s.append(anvil(seed=3, detail=not lite))
    s.append('<path d="M108 77 H154 V90 H108 Z" fill="#FF9A2A" filter="url(#gl2)" opacity=".6"/>')
    s.append(f'<path d="{BILLET}" fill="url(#billetG)"/><path d="M114 80 H148 L150 81.4 H112 Z" fill="#FFF0B0" opacity=".9"/>')
    if animated:
        s.append(f'<path class="barhot" d="{BILLET}" fill="#FFF4D8"/>')
        s.append(MINI_HAMMER)
        rng, sp = random.Random(5), []
        for _ in range(16):
            a = math.radians(rng.uniform(-170, -10))
            v = rng.uniform(26, 60)
            c = rng.choice(['#EAF2FF', '#FFE9B0', '#FFC24D', '#FF9440']) if rng.random() > .2 else rng.choice(['#45E0A0', '#BC8BFF', '#6E9BFF'])
            sp.append(f'<path d="M-8 0 H0" transform="translate(142 80) rotate({math.degrees(a):.0f})" stroke="{c}" stroke-width="2.4" '
                      f'stroke-linecap="round" style="--dx:{math.cos(a) * v:.1f}px;--dy:{math.sin(a) * v + 14:.1f}px"/>')
        s.append(f'<g class="sparks">{"".join(sp)}</g>')
        s.append(f'<g class="flash"><circle cx="142" cy="80" r="22" fill="url(#haloB)"/>{star4(142, 80, 9, "#F4F8FF")}'
                 '<path d="M112 80 H172" stroke="#DCE8FF" stroke-width=".8"/></g>')
        s.append(''.join(f'<circle class="em em{i}" style="--x:{x}px" cx="{cx}" cy="70" r="1.1" fill="{c}"/>'
                         for i, (cx, x, c) in enumerate([(110, -8, '#FFC24D'), (128, 6, '#FF9440'), (146, -4, '#FFE9B0'),
                                                         (120, 10, '#45E0A0'), (138, -10, '#FF6A4A'), (132, 4, '#BC8BFF')])))
    s.append(f'<g class="star" id="star" fill="{star}">{star4(208, 26, 13, star)}</g>')
    return ''.join(s)


# Every animation is finite and ends by 4.8 s (WCAG 2.2.2: autoplay ends inside 5 s); each ends on the still: the hammer
# raised, the glows and sparks gone, the fire and the seam at rest. Times are shorthand only, with a leading digit.
ANIM_CSS = ('<style>'
            '.fire .pl{transform-box:fill-box;transform-origin:50% 100%;animation:burn 1.7s ease-in-out 0s 2}'
            '.fire .p1{animation:burn 1.3s ease-in-out 0s 3}.fire .p2{animation:burn 1.5s ease-in-out 0s 3}'
            '.fire .p3,.fire .p4{animation:burn 1.1s ease-in-out 0s 4}'
            '@keyframes burn{0%,100%{transform:scale(1,1) skewX(0deg)}30%{transform:scale(.95,1.1) skewX(-3deg)}'
            '55%{transform:scale(1.04,.94) skewX(2deg)}80%{transform:scale(.98,1.05) skewX(-1deg)}}'
            '.seamg{animation:breathe 3.6s ease-in-out 0s 1}@keyframes breathe{0%,100%{opacity:1}40%{opacity:.55}}'
            '.rg{opacity:0}' + ''.join(f'.rg{i}{{animation:rune 1.8s ease-in-out {sec(.6 + .3 * i)} 1}}' for i in range(5))
            + '@keyframes rune{0%,100%{opacity:0}30%{opacity:.9}}'
            '.rv{opacity:0;fill:#FFB050}' + ''.join(f'.rv{i}{{animation:rivet 1.6s ease-out {sec(1 + .25 * i)} 1}}' for i in range(9))
            + '@keyframes rivet{0%{opacity:1;fill:#FFFFFF}6%{fill:#6E9BFF}22%{opacity:.9;fill:#FFB050}45%,100%{opacity:0}}'
            '.hm{transform-box:view-box;transform-origin:0 0;transform:translate(194px,56px) rotate(48deg);animation:swing 2.2s linear 0.4s 2}'
            '@keyframes swing{0%{transform:translate(194px,56px) rotate(48deg);animation-timing-function:ease-in-out}'
            '22%{transform:translate(198px,53px) rotate(53deg);animation-timing-function:cubic-bezier(.6,0,1,.6)}'
            '36%{transform:translate(140.7px,73.7px) rotate(-12deg);animation-timing-function:cubic-bezier(.2,.8,.3,1)}'
            '42%{transform:translate(141px,70px) rotate(-15deg);animation-timing-function:ease-in-out}'
            '70%{transform:translate(168px,56px) rotate(16deg);animation-timing-function:ease-in-out}'
            '100%{transform:translate(194px,56px) rotate(48deg)}}'
            '.sparks path{opacity:0;animation:fly 2.2s cubic-bezier(.15,.7,.4,1) 0.4s 2}'
            '@keyframes fly{0%,35%{opacity:0;translate:0 0}36%{opacity:1;translate:0 0}70%,100%{opacity:0;translate:var(--dx) var(--dy)}}'
            '.flash{opacity:0;animation:hot 2.2s ease-out 0.4s 2}.barhot{opacity:0;animation:hot 2.2s ease-out 0.4s 2}'
            '@keyframes hot{0%,35%{opacity:0}36%{opacity:.95}60%,100%{opacity:0}}'
            '.star{transform-box:fill-box;transform-origin:center;animation:twinkle 2.2s ease-in-out 0.4s 2}'
            '@keyframes twinkle{0%,30%,100%{transform:scale(1) rotate(0deg)}38%{transform:scale(1.25) rotate(10deg)}50%{transform:scale(.92)}}'
            '.em{opacity:0}' + ''.join(f'.em{i}{{animation:rise 2.4s ease-in {sec(.2 + .4 * i)} 1}}' for i in range(6))
            + '@keyframes rise{0%{opacity:0;transform:none}15%{opacity:.95}100%{opacity:0;transform:translate(var(--x),-74px)}}'
            '@media (prefers-reduced-motion: reduce){*{animation:none!important}.sparks,.flash,.em,.rg,.barhot,.rv{display:none}}'
            '</style>')


def simple():
    """32 to 96 px: the same silhouette with the detail taken out. The stone in three flat facets, one band with three
    rivets, the seam, the anvil with its lit face, a hot billet, three plumes with a blue core. No runes, no pits."""
    S_L, S_M, S_R = STONE
    s = ['<circle cx="128" cy="70" r="80" fill="url(#halo)"/>']
    for (x, w, h, p, core) in SIMPLE_PLUMES:
        s.append(f'<path fill="url(#fOut)" d="{tongue(x, 88, w, h, .35, p, .7)}"/><path fill="url(#fMid)" d="{tongue(x, 88, w * .6, h * .7, .4, p + .3, .6)}"/>')
        if core:
            s.append(f'<path fill="url(#fCore)" d="{tongue(x, 88, w * .34, h * .46, .45, p + .6, .4)}"/>')
    s.append(f'<path d="{poly_d(S_L)}" fill="#5A5560"/><path d="{poly_d(S_M)}" fill="#34333C"/><path d="{poly_d(S_R)}" fill="#1E1E26"/>')
    s.append(f'<path id="stone" d="{STONE_D}" fill="url(#forgeSide)" style="mix-blend-mode:screen"/>')
    s.append('<path d="M46 150 L92 148 L170 146 L206 150" fill="none" stroke="#FFC48A" stroke-width="3" stroke-linejoin="round"/>'
             '<path d="M46 150 L34 190 L40 226" fill="none" stroke="#FFB070" stroke-opacity=".6" stroke-width="3"/>')
    s.append('<path d="M37 160 L94 157 L169 155 L210 159 L213 175 L170 171 L93 173 L36 176 Z" fill="#2A2C33"/>'
             '<path d="M37 160 L94 157 L169 155 L210 159" fill="none" stroke="#A9B4C6" stroke-opacity=".6" stroke-width="2"/>')
    for x, y in ((66, 166), (128, 163), (190, 165)):
        s.append(f'<circle cx="{x}" cy="{y}" r="5" fill="url(#rivet)"/>')
    s.append('<path d="M66 147.5 H190" stroke="#FF6A1E" stroke-width="9" opacity=".6" filter="url(#gl3)"/><path d="M70 144.5 H186 V150.5 H70 Z" fill="url(#seamU)"/>')
    s.append(f'<path id="anvil" d="{art.ANVIL_D}" fill="url(#aSteel)"/><path d="M72 87 H164 C176 87 196 91 220 96.6" fill="none" stroke="url(#faceLit)" stroke-width="3"/>')
    s.append(f'<path d="{BILLET}" fill="url(#billetG)"/><path d="M114 80 H148 L150 82 H112 Z" fill="#FFF0B0"/>')
    s.append(f'<g id="star" fill="{DARK["star"]}">{star4(208, 26, 13, DARK["star"])}</g>')
    return ''.join(s)


def icon16():
    """Drawn on the 16 grid, every edge on a whole or half pixel: a low fire with a blue core, the anvil, the seam, the
    stone in three facets and its band. Ten shapes, no runes."""
    shapes = [('url(#f)', 'M8 1 L10 3.5 L10.5 6.5 H5.5 L6 3.5 Z M4.5 3.5 L5.5 5 V6.5 H3.5 V5 Z M11.5 3 L12.5 4.5 V6.5 H10.5 V4.5 Z'),
              ('#5B8CFF', 'M8 3.5 L9 5 V6.5 H7 V5 Z'),
              ('#B9AFA8', 'M2 6.5 H11.5 L13.5 7 L15.5 7.5 L13.5 8 L10.5 8.5 V9.5 H5.5 V8.5 L3.5 8.5 L3 7.5 H2 Z'),
              ('#FFE6C8', 'M3 6.5 H11.5 V7 H3 Z'),
              ('#4E5260', 'M3.5 8 H11.5 L10.5 8.5 V9.5 H5.5 V8.5 H3.5 Z'),
              ('#FF9A2E', 'M4 9.5 H12 V10.5 H4 Z'),
              ('#5A5664', 'M2 10.5 H5.5 V15.5 H1 Z'),
              ('#3A3944', 'M5.5 10.5 H10.5 L11 15.5 H5.5 Z'),
              ('#22232C', 'M10.5 10.5 H14 L15 15.5 H11 Z'),
              ('#2A2C33', 'M1.5 11.5 H14.5 V12.5 H1.5 Z')]
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16" role="img" aria-labelledby="t"><title id="t">Sampo</title>'
            '<defs><linearGradient id="f" x1="0" y1="1" x2="0" y2="7" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#E2481A"/>'
            '<stop offset=".55" stop-color="#FF9A2E"/><stop offset="1" stop-color="#FFE08A"/></linearGradient></defs>'
            + ''.join(f'<path fill="{c}" d="{d}"/>' for c, d in shapes) + '</svg>\n')


def mono():
    """One ink, currentColor: the fire's tongues, the stone's facets, the band, the five runes, the anvil, the star."""
    flame = ''.join(tongue(x, 84, w, h, .35, p, .7) for x, w, h, p, _ in SIMPLE_PLUMES)
    runes = ''.join(f'<path d="{art.RUNES[n]}" transform="translate({x} {y})"/>' for n, x, y, _ in RUNES5)
    return (f'<path d="{flame}" fill="currentColor"/>'
            f'<path id="stone" d="{STONE_D}" fill="none" stroke="currentColor" stroke-width="4" stroke-linejoin="round"/>'
            '<path d="M37 160 L94 157 L169 155 L210 159 M36 170 L93 167 L170 165 L213 169" fill="none" stroke="currentColor" stroke-width="3"/>'
            '<path d="M70 147.5 H186" fill="none" stroke="currentColor" stroke-width="4"/>'
            f'<g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="square">{runes}</g>'
            f'<path id="anvil" d="{art.ANVIL_D}" fill="currentColor"/>'
            + star4(208, 26, 13, 'currentColor'))


# ---- type: outlines from glyphs.json, in font units (y up)
def text_path(face, text, size, x, baseline, track=0.0):
    """text at size px from x on baseline, as one path's d and its advance; track is in px between letters."""
    s, x0, out = size / face["upm"], x, []
    for ch in text:
        adv, d = face["glyphs"][ch]
        out.append(re.sub(r"(-?[\d.]+) (-?[\d.]+)", lambda m: f"{f(x + s * float(m[1]))} {f(baseline - s * float(m[2]))}", d))
        x += adv * s + track
    return "".join(out), x - x0 - track


def fit(face, text, size, maxw, track=0.0):
    """The size (and tracking) at which text fits maxw, never larger than size."""
    k = min(1.0, maxw / text_path(face, text, size, 0, 0, track)[1])
    return size * k, track * k


def extract(fontdir):
    """Write glyphs.json: each face instanced at its axes, then only the glyphs its text uses."""
    from fontTools.pens.basePen import BasePen
    from fontTools.ttLib import TTFont
    from fontTools.varLib.instancer import instantiateVariableFont

    def pt(p):
        return "%d %d" % (round(p[0]), round(p[1]))

    class Pen(BasePen):
        def __init__(self, gs):
            super().__init__(gs)
            self.d = []

        def _moveTo(self, p):
            self.d.append("M" + pt(p))

        def _lineTo(self, p):
            self.d.append("L" + pt(p))

        def _curveToOne(self, a, b, c):
            self.d.append("C" + " ".join(map(pt, (a, b, c))))

        def _qCurveToOne(self, a, b):
            self.d.append("Q" + pt(a) + " " + pt(b))

        def _closePath(self):
            self.d.append("Z")

    data = {}
    for key, (name, axes, text) in FACES.items():
        ft = TTFont(os.path.join(fontdir, name))
        ft = instantiateVariableFont(ft, {a.axisTag: axes.get(a.axisTag, a.defaultValue) for a in ft["fvar"].axes})
        gs, cmap, glyphs = ft.getGlyphSet(), ft.getBestCmap(), {}
        for ch in sorted(set(text)):
            g = gs[cmap[ord(ch)]]
            pen = Pen(gs)
            g.draw(pen)
            glyphs[ch] = [g.width, "".join(pen.d)]
        data[key] = {"upm": ft["head"].unitsPerEm, "glyphs": glyphs}
    with open(GLYPHS, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1, sort_keys=True)
        fh.write("\n")


# ---- the compositions
def night_sky(rng, W, H, n):
    """n stars in three colours and two brightnesses, as one path per colour and level."""
    st = {}
    for _ in range(n):
        x, y, m, c = rng.uniform(8, W - 8), rng.uniform(8, H - 8), rng.random() ** 2.6, rng.random()
        col = '#FFD6A0' if c < .12 else '#AAC4FF' if c < .3 else '#EBF0FF'
        st.setdefault((col, 0 if m < .25 else 1), []).append(circ(x, y, .45 + m * 1.1))
    return ''.join(f'<path d="{"".join(ds)}" fill="{col}" opacity="{(.35, .85)[lv]}"/>' for (col, lv), ds in st.items())


def ground(theme, W, H, gx, gy, gr, ey0, ey1):
    """The night (or the day's pale sky), the forge's glow at (gx, gy), and the engraved-brass gradient for the word."""
    if theme == 'dark':
        return ('<defs><linearGradient id="bgN" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0B1030"/><stop offset="1" stop-color="#060819"/></linearGradient>'
                f'<radialGradient id="bgG" cx="{gx}" cy="{gy}" r="{gr}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#FF8A2A" stop-opacity=".28"/><stop offset="1" stop-color="#FF8A2A" stop-opacity="0"/></radialGradient>'
                f'<linearGradient id="eng" x1="0" y1="{ey0}" x2="0" y2="{ey1}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#FFF6DD"/><stop offset=".3" stop-color="#F0D392"/><stop offset=".55" stop-color="#B9873F"/><stop offset=".76" stop-color="#E9C98A"/><stop offset="1" stop-color="#E9C98A"/></linearGradient></defs>')
    return ('<defs><linearGradient id="bgN" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E2E6F1"/><stop offset="1" stop-color="#EEF0F6"/></linearGradient>'
            f'<radialGradient id="bgG" cx="{gx}" cy="{gy}" r="{gr}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#FFAA5A" stop-opacity=".28"/><stop offset="1" stop-color="#FFAA5A" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="eng" x1="0" y1="{ey0}" x2="0" y2="{ey1}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#2A2140"/><stop offset=".45" stop-color="#12163A"/><stop offset=".76" stop-color="#3C3426"/><stop offset="1" stop-color="#3C3426"/></linearGradient></defs>')


def type_block(faces, roles, x, kick_y, word_size, word_y, line_size, line_y, rule_y, maxw):
    """The kicker with its diamond, the word in engraved brass, the italic line, and a brass rule with ticks under them."""
    kd, _ = text_path(faces["mono"], KICKER, *fit(faces["mono"], KICKER, 11.5 * word_size / 118, maxw, 2.2 * word_size / 118)[:1], x, kick_y,
                      fit(faces["mono"], KICKER, 11.5 * word_size / 118, maxw, 2.2 * word_size / 118)[1])
    wd, ww = text_path(faces["display"], WORD, word_size, x - 4 * word_size / 118, word_y, -word_size / 118)
    ls = fit(faces["italic"], TAGLINE, line_size, maxw)[0]
    td, tw = text_path(faces["italic"], TAGLINE, ls, x, line_y)
    d = word_size / 118 * 4
    x1 = x + max(ww, tw)
    return (f'<path d="{kd}" fill="{roles["muted"]}"/><path d="M{f(x - 14)} {f(kick_y - 4 - d)} l{f(d)} {f(-d)} l{f(d)} {f(d)} l{f(-d)} {f(d)} Z" fill="#FFC24D"/>'
            f'<path d="{wd}" fill="url(#eng)"/><path d="{td}" fill="{roles["ink"]}"/>'
            f'<path d="M{f(x)} {rule_y} H{f(x1)}" stroke="{roles["brass"]}" stroke-opacity=".7"/><path d="'
            + ''.join(f'M{x + 12 * i} {rule_y} v{5 if i % 5 else 9}' for i in range(int((x1 - x) // 12) + 1))
            + f'" stroke="{roles["brass"]}" stroke-opacity=".5"/>')


def banner(theme, faces):
    """The README header, 1280 x 320: the mark's scene with embers climbing out of it, and the type beside it."""
    W, H, dark = 1280, 320, theme == 'dark'
    roles, rng = (DARK if dark else LIGHT), random.Random(11)
    b = [f'<rect width="{W}" height="{H}" rx="14" fill="url(#bgN)"/><rect width="{W}" height="{H}" rx="14" fill="url(#bgG)"/>']
    if dark:
        b.append(night_sky(rng, W, H, 260))
        OT = [(11.06, 61.75), (11.03, 56.38), (11.9, 53.69), (12.26, 57.03), (12.9, 55.96), (13.4, 54.93), (13.79, 49.31)]
        P = [(950 + (ra - 11) * 95, 40 + (62 - de) * 6.5) for ra, de in OT]  # Otava, the Great Bear
        b.append('<path d="' + ''.join(f'M{f(P[a][0])} {f(P[a][1])}L{f(P[c][0])} {f(P[c][1])}' for a, c in [(0, 1), (1, 2), (2, 3), (3, 0), (3, 4), (4, 5), (5, 6)])
                 + '" stroke="#D4AE66" stroke-opacity=".35" stroke-width=".9" fill="none"/>')
        b.append(''.join(f'<circle cx="{f(x)}" cy="{f(y)}" r="1.8" fill="#FFF4DC"/>' for x, y in P))
    b.append(f'<g transform="translate(70 18) scale(1.17)">{mark(star=roles["star"])}</g>')
    for _ in range(26):
        x, y = rng.uniform(150, 330), rng.uniform(16, 90)
        c = rng.choice(['#FFC24D', '#FF9440', '#FFE9B0', '#FF6A4A', '#45E0A0', '#BC8BFF'])
        b.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{rng.uniform(.8, 1.8):.1f}" fill="{c}" opacity="{rng.uniform(.4, .95):.2f}"/>')
    b.append(type_block(faces, roles, 424, 64, 118, 182, 30, 252, 280, 800))
    return doc(W, H, ''.join(b), f'Sampo, formerly Foreman: discipline for coding agents. {TITLE}', ground(theme, W, H, 230, 300, 380, 92, 212))


def share(faces):
    """The 1200 x 630 social card: the mark large on the night, the type beside it."""
    W, H, rng = 1200, 630, random.Random(12)
    b = [f'<rect width="{W}" height="{H}" fill="url(#bgN)"/><rect width="{W}" height="{H}" fill="url(#bgG)"/>', night_sky(rng, W, H, 240)]
    b.append(f'<g transform="translate(40 70) scale(1.9)">{mark()}</g>')
    b.append(type_block(faces, DARK, 560, 214, 150, 362, 34, 432, 466, 600))
    return doc(W, H, ''.join(b), f'Sampo, formerly Foreman: your coding agent, with a smith on the job. {TITLE}', ground('dark', W, H, 290, 470, 460, 250, 380))


def app_icon():
    """Full-bleed square; the platform masks it."""
    extra = ('<defs><linearGradient id="appN" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0B1030"/><stop offset="1" stop-color="#060819"/></linearGradient>'
             '<radialGradient id="appG" cx="128" cy="170" r="150" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#FF8A2A" stop-opacity=".3"/><stop offset="1" stop-color="#FF8A2A" stop-opacity="0"/></radialGradient></defs>')
    body = ('<rect width="256" height="256" fill="url(#appN)"/><rect width="256" height="256" fill="url(#appG)"/>'
            f'<g transform="translate(25.6 25.6) scale(.8)">{mark()}</g>')
    return doc(256, 256, body, TITLE, extra)


def desktop_icon():
    """The rounded tile on the macOS icon grid (824 of 1024, radius 185), with its margin."""
    extra = ('<defs><linearGradient id="tileN" x1="0" y1="25" x2="0" y2="231" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#121A44"/><stop offset="1" stop-color="#060819"/></linearGradient>'
             '<radialGradient id="tileG" cx="128" cy="180" r="140" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#FF8A2A" stop-opacity=".32"/><stop offset="1" stop-color="#FF8A2A" stop-opacity="0"/></radialGradient>'
             '<clipPath id="tileClip"><rect x="25" y="25" width="206" height="206" rx="46"/></clipPath></defs>')
    body = ('<rect x="25" y="25" width="206" height="206" rx="46" fill="url(#tileN)"/><rect x="25" y="25" width="206" height="206" rx="46" fill="url(#tileG)"/>'
            f'<g clip-path="url(#tileClip)"><g transform="translate(35.8 33) scale(.72)">{mark()}</g></g>'
            '<rect x="25.5" y="25.5" width="205" height="205" rx="45.5" fill="none" stroke="#D4AE66" stroke-opacity=".35"/>')
    return doc(256, 256, body, TITLE, extra)


def wordmark(faces):
    wd, ww = text_path(faces["display"], WORD, 120, 262, 168, -1)
    return doc(math.ceil(262 + ww + 16), 256, mark() + f'<path d="{wd}" fill="#B8924F"/>', 'Sampo')


def build(out):
    os.makedirs(out, exist_ok=True)
    with open(GLYPHS, encoding="utf-8") as fh:
        faces = json.load(fh)
    files = [
        ("mark.svg", lambda: doc(256, 256, mark(), TITLE)),
        ("mark-light.svg", lambda: doc(256, 256, mark(star=LIGHT["star"]), TITLE)),
        ("mark-animated.svg", lambda: doc(256, 256, mark(True), TITLE + ' The fire burns, the hammer strikes twice and throws sparks, '
                                          'the runes kindle and the rivets heat in turn, then it all rests.', ANIM_CSS)),
        ("mark-simple.svg", lambda: doc(240, 240, simple(), 'Sampo: an anvil on a stone bound with an iron band, a fire behind it.', vb='8 0 240 240')),
        ("icon-16.svg", icon16),
        ("mono.svg", lambda: doc(256, 256, mono(), 'Sampo, one ink')),
        ("wordmark.svg", lambda: wordmark(faces)),
        ("app-icon.svg", app_icon),
        ("desktop-icon.svg", desktop_icon),
        ("readme-header-dark.svg", lambda: banner('dark', faces)),
        ("readme-header-light.svg", lambda: banner('light', faces)),
        ("share.svg", lambda: share(faces)),
    ]
    for name, make in files:
        art._uid[0] = 0  # ids count from zero in each file, so a rebuild is byte for byte
        with open(os.path.join(out, name), "w", encoding="utf-8") as fh:
            fh.write(make())

    def render(src, w, h=None):  # rsvg-convert writes the PNG to stdout when no -o is given
        return subprocess.run(["rsvg-convert", "-w", str(w), "-h", str(h or w), os.path.join(out, src)], check=True,
                              stdout=subprocess.PIPE).stdout

    for src, name, pw, ph in (("app-icon.svg", "app-icon-512.png", 512, 512), ("app-icon.svg", "app-icon-1024.png", 1024, 1024),
                              ("desktop-icon.svg", "desktop-icon-1024.png", 1024, 1024), ("share.svg", "share.png", 1200, 630)):
        with open(os.path.join(out, name), "wb") as fh:
            fh.write(render(src, pw, ph))
    # favicon.ico: a 6-byte header, a 16-byte directory entry per size, then the PNGs as they are
    pngs = [(s, render("icon-16.svg", s)) for s in (16, 32, 48)]
    dirs, body, off = b"", b"", 6 + 16 * len(pngs)
    for s, data in pngs:
        dirs += struct.pack("<BBBBHHII", s % 256, s % 256, 0, 0, 1, 32, len(data), off + len(body))
        body += data
    with open(os.path.join(out, "favicon.ico"), "wb") as fh:
        fh.write(struct.pack("<HHH", 0, 1, len(pngs)) + dirs + body)


if __name__ == "__main__":
    if sys.argv[1:2] == ["--glyphs"]:
        extract(sys.argv[2])
    else:
        build(os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else HERE)
