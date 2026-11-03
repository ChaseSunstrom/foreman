"""Build the Runestone logo files from one mark geometry (T-2751).

Run from anywhere:

    python3 design/sampo/logo/build.py [OUT]

OUT defaults to this folder, so a plain run rewrites the committed files in place. Python's standard library and
rsvg-convert (librsvg) on PATH are all it needs.

It writes, into OUT:
- the SVGs: mark, mark-light, mark-animated, mono, icon-16, wordmark, app-icon, desktop-icon, readme-header-light,
  readme-header-dark and share;
- the PNGs, which rsvg-convert renders from those SVGs: app-icon-512, app-icon-1024, desktop-icon-1024 and share;
- favicon.ico, which packs icon-16.svg as rsvg-convert renders it at 16, 32 and 48 px.

The SVGs are byte-for-byte reproducible, and test_sampo_design rebuilds them into a temp dir to check that. The PNG
and .ico bytes depend on the rsvg-convert version, so the test doesn't compare those.

The type (SAMPO, and the share card's line) is outlined from glyphs.json, which this folder keeps. It holds the
font-unit outlines, advance widths, cap height and kerning pairs of only the glyphs these files use, taken from TeX
Gyre Pagella (Palatino's metrics; GUST Font License, i.e. LPPL 1.3c, so outlining it for a logo is free). To re-extract
them from a folder that holds qplb and qplr (.pfb and .afm, from CTAN fonts/tex-gyre), which needs fontTools:

    uv run --with fonttools python design/sampo/logo/build.py --glyphs FONTDIR
"""
import json
import math
import os
import re
import struct
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GLYPHS = os.path.join(HERE, "glyphs.json")

IRON, BRONZE, GLOW, EMBER, CORE = "#16181C", "#B07A3B", "#FF9E3D", "#E0601F", "#FFE3A8"
FURROW, RING = "#4A5160", "#3A3F48"
LIGHT_BRONZE, PARCHMENT, LIGHT_MUTED = "#7A5020", "#F6F0E4", "#58503F"
NIGHT, SUNKEN, RAISED, DARK_BRONZE, DARK_MUTED, LINE = "#121418", "#0B0C0F", "#1B1E24", "#D9A870", "#BDB29E", "#9CCBEB"
C = 32
WORD, TAG = "SAMPO", "the mill that produces by itself"


def n(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def polar(r, deg):  # degrees clockwise from twelve o'clock
    a = math.radians(deg)
    return C + r * math.sin(a), C - r * math.cos(a)


# --- furrows: eight harps, each a curved master furrow and a shorter one beside it (sickle dress)
def rot(p, deg):
    a = math.radians(deg)
    x, y = p[0] - C, p[1] - C
    return C + x * math.cos(a) - y * math.sin(a), C + x * math.sin(a) + y * math.cos(a)


def q(p0, c, p1):
    return f"M{n(p0[0])} {n(p0[1])}Q{n(c[0])} {n(c[1])} {n(p1[0])} {n(p1[1])}"


def harp(theta, r0=8.6, r1=17.4, sweep=38, t=0.45):
    """A master furrow curving out from the eye, and the shorter furrow of its harp: the master's outer part, turned
    half a harp on, so the two run parallel as a millwright dresses them."""
    p0, p1 = polar(r0, theta), polar(r1, theta + sweep)
    pm = polar((r0 + r1) / 2, theta + sweep * 0.3)
    c = 2 * pm[0] - (p0[0] + p1[0]) / 2, 2 * pm[1] - (p0[1] + p1[1]) / 2
    lerp = lambda a, b: (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
    s0 = lerp(lerp(p0, c), lerp(c, p1))  # de Casteljau split at t
    return q(p0, c, p1) + q(rot(s0, 22.5), rot(lerp(c, p1), 22.5), rot(p1, 22.5))


FURROWS = "".join(harp(h * 45) for h in range(8))


# --- runes: a stave (x=32, y 5..11, 5 is the rim side), each with its own silhouette; radial, so none stands
# upright as a letter
RUNES = [
    (22.5, "M32 5V11M32 8.6L34.4 6.2"),                           # one branch up-right
    (67.5, "M32 5V11M32 5.2L34 7M32 10.8L30 9"),                  # opposed hooks at the two ends
    (112.5, "M32 5V11M30.5 8.9L33.5 7.1"),                        # naudiz: a short slant across
    (157.5, "M32 5V11M32 6.6L33.7 8L32 9.4"),                     # thorn: a small bump mid-stave
    (202.5, "M32 5V11M34.4 5.4L32 7.4L34.4 9.4"),                 # a chevron off the stave
    (247.5, "M32 5V11M29.6 6.2H34.4M32 10.6L34.2 8.8"),           # a cross bar and one slant
    (292.5, "M32 5V11"),                                          # a bare stave
    (337.5, "M32 5V11M29.8 7L32 5.4L34.2 7M29.8 9.6L32 8L34.2 9.6"),  # a double chevron
]


def runes_g(stroke, width="1.4"):
    paths = "".join(f'<path class="r{i + 1}" transform="rotate({n(a)} 32 32)" d="{d}"/>'
                    for i, (a, d) in enumerate(RUNES))
    return f'<g id="runes" stroke="{stroke}" stroke-width="{width}">{paths}</g>'


def eye_defs(cx=32, cy=32, r=6.5, ident="eye"):
    return (f'<radialGradient id="{ident}" cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="{CORE}"/><stop offset="0.55" stop-color="{GLOW}"/>'
            f'<stop offset="1" stop-color="{EMBER}"/></radialGradient>')


def mark(disc=IRON, rim=BRONZE, anim=False):
    stone = ' class="stone"' if anim else ""
    eye = ' class="eye"' if anim else ""
    return (f'<circle id="disc" cx="32" cy="32" r="30" fill="{disc}" stroke="{rim}" stroke-width="2"/>\n'
            f'<g{stone} fill="none" stroke-linecap="round" stroke-linejoin="round">\n'
            f'<circle cx="32" cy="32" r="19" stroke="{RING}"/>\n'
            f'<path id="furrows" stroke="{FURROW}" stroke-width="1.5" d="{FURROWS}"/>\n'
            f'{runes_g(GLOW)}\n</g>\n'
            f'<circle id="eye-core"{eye} cx="32" cy="32" r="6.5" fill="url(#eye)"/>\n'
            f'<rect{stone} x="25.5" y="31" width="13" height="2" rx="1" fill="{IRON}"/>\n')


def svg(w, h, title, body, defs="", style="", size=True):
    dims = f' width="{n(w)}" height="{n(h)}"' if size else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n(w)} {n(h)}"{dims} role="img" '
            f'aria-labelledby="t">\n<title id="t">{title}</title>\n'
            + (f"<style>\n{style}</style>\n" if style else "")
            + (f"<defs>{defs}</defs>\n" if defs else "") + body + "</svg>\n")


def placed(x, y, scale, body):
    return f'<g transform="translate({n(x)} {n(y)}) scale({n(scale)})">\n{body}</g>\n'


# --- type: outlines from glyphs.json, in font units (1000 to the em, y up)
def text_path(face, text, size, x, baseline, track):
    """text at size px from x on baseline, as one path's d and its advance; track is in ems between letters."""
    s, x0, out = size / 1000, x, []
    for i, ch in enumerate(text):
        w, d = face["glyphs"][ch]
        out.append(re.sub(r"(-?[\d.]+) (-?[\d.]+)",
                          lambda m: f"{n(x + s * float(m[1]))} {n(baseline - s * float(m[2]))}", d))
        x += w * s
        if i < len(text) - 1:
            x += track * size + face["kern"].get(text[i:i + 2], 0) * s
    return "".join(out), x - x0


def extract(fontdir):
    """Write glyphs.json from Pagella Bold (the word) and Regular (the line) in fontdir."""
    from fontTools.pens.recordingPen import RecordingPen
    from fontTools.t1Lib import T1Font

    ops = {"moveTo": "M", "lineTo": "L", "curveTo": "C", "closePath": "Z", "endPath": ""}
    data = {}
    for key, stem, text in (("bold", "qplb", WORD), ("roman", "qplr", TAG)):
        font = T1Font(os.path.join(fontdir, stem + ".pfb"))
        font.parse()
        gs = font.getGlyphSet()
        with open(os.path.join(fontdir, stem + ".afm"), encoding="latin-1") as f:
            afm = [ln.split() for ln in f]
        kpx = {(p[1], p[2]): float(p[3]) for p in afm if p and p[0] == "KPX"}
        name = {" ": "space"}
        chars = sorted(set(text))
        glyphs = {}
        for ch in chars:
            pen = RecordingPen()
            gs[name.get(ch, ch)].draw(pen)
            glyphs[ch] = [gs[name.get(ch, ch)].width,
                          "".join(ops[op] + " ".join(n(v) for pt in pts for v in pt) for op, pts in pen.value)]
        kern = {a + b: kpx[name.get(a, a), name.get(b, b)] for a in chars for b in chars
                if (name.get(a, a), name.get(b, b)) in kpx}
        data[key] = {"cap": next(float(p[1]) for p in afm if p and p[0] == "CapHeight"), "glyphs": glyphs,
                     "kern": kern}
    with open(GLYPHS, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, sort_keys=True)
        f.write("\n")


def build(out):
    os.makedirs(out, exist_ok=True)
    with open(GLYPHS, encoding="utf-8") as f:
        faces = json.load(f)
    bold, roman = faces["bold"], faces["roman"]
    track = 0.06  # caps want more air than the token's +0.02em running-text tracking

    def word(cap, x, baseline, fill):
        d, w = text_path(bold, WORD, cap / (bold["cap"] / 1000), x, baseline, track)
        return f'<path fill="{fill}" d="{d}"/>\n', w

    def write(name, text):
        with open(os.path.join(out, name), "w", encoding="utf-8") as f:
            f.write(text)
        return os.path.join(out, name)

    def render(src, w, h=None):  # rsvg-convert writes the PNG to stdout when no -o is given
        return subprocess.run(["rsvg-convert", "-w", str(w), "-h", str(h or w), src], check=True,
                              stdout=subprocess.PIPE).stdout

    eye = eye_defs()
    title = "Sampo: a rune-cut millstone, its forge-lit eye crossed by the rynd bar"
    write("mark.svg", svg(64, 64, title, mark(), eye))
    write("mark-light.svg", svg(64, 64, title, mark(rim=LIGHT_BRONZE), eye))

    anim = """.stone{transform-origin:32px 32px;animation:turn 4.2s cubic-bezier(0.25,0.1,0.25,1) both}
.eye{animation:heat 3s ease-in both}
""" + "".join(f".r{i + 1}{{animation:lite 240ms ease-out {n(1.2 + 0.24 * i)}s both}}\n" for i in range(8)) + """.k>*{opacity:0}
.k1{animation:k1 900ms ease-out 2.9s both}
.k2{animation:k2 900ms ease-out 3s both}
.k3{animation:k3 900ms ease-out 3.1s both}
@keyframes turn{from{transform:rotate(-450deg)}to{transform:rotate(0deg)}}
@keyframes heat{from{opacity:0.3}to{opacity:1}}
@keyframes lite{from{opacity:0.15}to{opacity:1}}
"""
    sparks = []  # (rim angle near the last rune at 337.5, flight along the clockwise tangent: they leave with the spin)
    for i, (ang, dx, dy) in enumerate([(322, 6.5, -5), (334, 7, -3.5), (310, 5, -6.5)]):
        x, y = polar(30, ang)
        sparks.append(f'<circle class="k{i + 1}" cx="{n(x)}" cy="{n(y)}" r="2"/>')
        anim += (f"@keyframes k{i + 1}{{0%{{opacity:0;transform:none}}15%{{opacity:1}}"
                 f"100%{{opacity:0;transform:translate({n(dx)}px,{n(dy)}px)}}}}\n")
    anim += "@media (prefers-reduced-motion: reduce){*{animation:none!important}}\n"
    write("mark-animated.svg", svg(64, 64, "Sampo: the rune millstone makes a turn and a quarter and settles, its runes "
                                   "light in order, sparks leave the rim", mark(anim=True)
                                   + f'<g class="k" fill="{EMBER}">' + "".join(sparks) + "</g>\n", eye, anim))

    mono = ('<g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">\n'
            '<circle id="disc" cx="32" cy="32" r="30" stroke-width="2.5"/>\n<circle cx="32" cy="32" r="19"/>\n'
            f'<path id="furrows" stroke-width="1.1" d="{FURROWS}"/>\n{runes_g("currentColor")}\n</g>\n'
            '<path fill="currentColor" d="M25.58 31A6.5 6.5 0 0 1 38.42 31ZM25.58 33A6.5 6.5 0 0 0 38.42 33Z"/>\n')
    write("mono.svg", svg(64, 64, "Sampo, one ink", mono))

    # the 16 px icon: its own drawing, no runes: dark disc, bronze rim, hot eye, the 1 px rynd bar. The bar sits on
    # whole pixels (row 7, columns 5..10) and stops a pixel short of the eye's edge (4..12) at each end, so forge light
    # shows past it: a full-width bar read as a circled minus. Its gradient has its own id: a page inlining the mark
    # and the icon must not swap gradients.
    icon = write("icon-16.svg", svg(16, 16, "Sampo", f'<circle cx="8" cy="8" r="7.25" fill="{IRON}" stroke="{BRONZE}" '
                                    'stroke-width="1.5"/>\n<circle cx="8" cy="8" r="4" fill="url(#eye16)"/>\n'
                                    f'<rect x="5" y="7" width="6" height="1" fill="{IRON}"/>\n',
                                    eye_defs(8, 8, 4, "eye16")))

    wpath, ww = word(26, 80, 45, BRONZE)
    write("wordmark.svg", svg(math.ceil(80 + ww + 2), 64, "Sampo", mark() + wpath, eye))

    forge = ('<radialGradient id="forge" cx="32" cy="32" r="46" gradientUnits="userSpaceOnUse">'
             f'<stop offset="0.45" stop-color="#3A2614"/><stop offset="0.75" stop-color="{RAISED}"/>'
             f'<stop offset="1" stop-color="{SUNKEN}"/></radialGradient>')
    app = write("app-icon.svg", svg(64, 64, "Sampo", '<rect width="64" height="64" fill="url(#forge)"/>\n'
                                    + placed(6.4, 6.4, 0.8, mark()), eye + forge))

    tile = ('<linearGradient id="tile" x1="0" y1="6" x2="0" y2="58" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="#2A2E36"/><stop offset="1" stop-color="{SUNKEN}"/></linearGradient>'
            + forge.replace('id="forge"', 'id="forge" fx="32" fy="32"'))
    desk = write("desktop-icon.svg", svg(64, 64, "Sampo", '<rect x="6.25" y="6.25" width="51.5" height="51.5" '
                                         'rx="11.6" fill="url(#tile)"/>\n<rect x="6.25" y="6.25" width="51.5" '
                                         'height="51.5" rx="11.6" fill="url(#forge)" opacity="0.55"/>\n<rect x="6.45" '
                                         'y="6.45" width="51.1" height="51.1" rx="11.4" fill="none" stroke="#B07A3B" '
                                         'stroke-opacity="0.45" stroke-width="0.4"/>\n'
                                         + placed(32 - 32 * 0.6, 32 - 32 * 0.6, 0.6, mark()), eye + tile))

    for name, bg, rim, ink in (("readme-header-light.svg", PARCHMENT, LIGHT_BRONZE, LIGHT_BRONZE),
                               ("readme-header-dark.svg", NIGHT, BRONZE, DARK_BRONZE)):
        w, h, m, cap = 960, 240, 160, 64
        x0 = (w - (m + 44 + word(cap, 0, 0, ink)[1])) / 2
        body = (f'<rect width="{w}" height="{h}" rx="16" fill="{bg}"/>\n'
                + placed(x0, (h - m) / 2, m / 64, mark(rim=rim)) + word(cap, x0 + m + 44, h / 2 + cap / 2, ink)[0])
        write(name, svg(w, h, "Sampo", body, eye))

    # share: 1200 x 630, the mark in forge light on the night, the word and its one line
    w, h, mx, my, ms = 1200, 630, 300, 315, 300
    glow = (f'<radialGradient id="glow" cx="{mx}" cy="{my}" r="330" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0.4" stop-color="{GLOW}" stop-opacity="0.22"/><stop offset="1" stop-color="{GLOW}" '
            'stop-opacity="0"/></radialGradient>')
    lines = (f'<g fill="none" stroke="{LINE}" stroke-opacity="0.16" stroke-width="1.2">'
             f'<circle cx="{mx}" cy="{my}" r="200" stroke-dasharray="4 8"/><circle cx="{mx}" cy="{my}" r="248"/>'
             f'<path d="M{mx - 270} {my}H{w - 60}M{mx} 30V{h - 30}"/></g>\n')
    body = (f'<rect width="{w}" height="{h}" fill="{NIGHT}"/>\n<rect width="{w}" height="{h}" fill="url(#glow)"/>\n'
            + lines + placed(mx - ms / 2, my - ms / 2, ms / 64, mark()) + word(84, 560, 316, DARK_BRONZE)[0]
            + f'<path fill="{DARK_MUTED}" d="{text_path(roman, TAG, 38, 563, 386, 0.01)[0]}"/>\n')
    share = write("share.svg", svg(w, h, "Sampo, the mill that produces by itself", body, eye + glow))

    # the rasters, all from rsvg-convert
    for src, name, pw, ph in ((app, "app-icon-512.png", 512, 512), (app, "app-icon-1024.png", 1024, 1024),
                              (desk, "desktop-icon-1024.png", 1024, 1024), (share, "share.png", 1200, 630)):
        with open(os.path.join(out, name), "wb") as f:
            f.write(render(src, pw, ph))
    # favicon.ico: a 6-byte header, a 16-byte directory entry per size, then the PNGs as they are
    pngs = [(s, render(icon, s)) for s in (16, 32, 48)]
    dirs, body, off = b"", b"", 6 + 16 * len(pngs)
    for s, data in pngs:
        dirs += struct.pack("<BBBBHHII", s % 256, s % 256, 0, 0, 1, 32, len(data), off + len(body))
        body += data
    with open(os.path.join(out, "favicon.ico"), "wb") as f:
        f.write(struct.pack("<HHH", 0, 1, len(pngs)) + dirs + body)


if __name__ == "__main__":
    if sys.argv[1:2] == ["--glyphs"]:
        extract(sys.argv[2])
    else:
        build(os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else HERE)
