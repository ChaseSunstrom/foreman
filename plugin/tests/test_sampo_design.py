"""T-2747: Sampo's design system and its three logo directions (SAMPO.md, Design). design/sampo/tokens.json is the one
source every surface reads (light and dark palettes, type stacks, motion rules); each of the three directions under
design/sampo/directions/ ships a full mark, a 16 px icon, a monochrome mark, a wordmark and an animated mark whose
still is what reduced motion shows; index.html previews them all in both themes. Nothing loads from another host."""
# map-links: design/sampo/tokens.json design/sampo/index.html site/style.css design/sampo/logo/build.py design/sampo/logo/art.py design/sampo/logo/glyphs.json design/sampo/logo/mark-simple.svg design/sampo/logo/pane-glyph.txt
import json
import math
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import unicodedata
import unittest
import xml.etree.ElementTree as ET

from helpers import PLUGIN, read_text

from sampo import design

ROOT = os.path.join(os.path.dirname(PLUGIN), "design", "sampo")
DIRS = os.path.join(ROOT, "directions")
VARIANTS = ("mark.svg", "icon-16.svg", "mono.svg", "wordmark.svg", "mark-animated.svg")
SVG = "{http://www.w3.org/2000/svg}"
LOGO = os.path.join(ROOT, "logo")
COMPOSED = ("mark-animated.svg", "mark-light.svg", "mono.svg", "wordmark.svg", "app-icon.svg", "desktop-icon.svg",
            "readme-header-light.svg", "readme-header-dark.svg", "share.svg")
LOGO_SVGS = ("mark.svg", "mark-simple.svg", "icon-16.svg") + COMPOSED
RASTERS = {"app-icon-512.png": (512, 512), "app-icon-1024.png": (1024, 1024), "desktop-icon-1024.png": (1024, 1024),
           "share.png": (1200, 630)}
GENERIC = {"serif", "sans-serif", "monospace", "system-ui", "ui-monospace", "ui-serif", "ui-sans-serif"}


def tokens():
    with open(os.path.join(ROOT, "tokens.json"), encoding="utf-8") as f:
        return json.load(f)


def hex_of(theme, role):
    tok = tokens()[theme]["color"][role]
    v = tok["$value"]
    return v["hex"] if isinstance(v, dict) else v


def ratio(a, b):
    return design.contrast(design.parse_colour(a), design.parse_colour(b))


def directions():
    return sorted(d for d in os.listdir(DIRS) if os.path.isdir(os.path.join(DIRS, d)))


def outside(text):
    """Each reference in text (an attribute or a stylesheet) that would reach past the file itself."""
    refs = re.findall(r"url\(\s*['\"]?([^'\")]*)", text) + re.findall(r"@import\s+['\"]?([^'\";\s]+)", text)
    return [r for r in refs if not r.startswith("#")]


def check_svg(test, path, limit=12000):
    """path is a well-formed SVG that runs nothing and loads nothing from another host."""
    text = read_text(path)
    test.assertNotRegex(text, r"<!(?:DOCTYPE|ENTITY)", f"{path}: no DTD, so no entity reaches out")
    root = ET.fromstring(text)  # raises on a malformed file
    test.assertEqual(root.tag, SVG + "svg", path)
    test.assertTrue(root.get("viewBox"), path)
    tags = {e.tag.replace(SVG, "") for e in root.iter()}
    test.assertFalse(tags & {"script", "foreignObject", "image", "use", "text", "a", "iframe"}, f"{path}: {tags}")
    test.assertNotRegex(text, r"font-family|@font-face|https?://(?!www\.w3\.org/)", path)
    for e in root.iter():
        for k, val in e.attrib.items():
            if k.endswith("href") or k == "src":
                test.assertTrue(val.startswith("#"), f"{path}: {k}={val}")
            if k.startswith("on"):
                test.fail(f"{path}: event handler {k}")
        test.assertEqual(outside(" ".join(e.attrib.values()) + (e.text or "")), [], path)
    ids = [e.get("id") for e in root.iter() if e.get("id")]
    test.assertEqual(len(ids), len(set(ids)), f"{path}: an id defined twice resolves to whichever comes first")
    test.assertFalse(set(re.findall(r"url\(#([\w.-]+)\)", text)) - set(ids), f"{path}: url() names a missing id")
    test.assertLess(len(text), limit, f"{path}: keep the geometry small")
    return root


def check_icon_16(test, path):
    root = ET.fromstring(read_text(path))
    test.assertEqual(root.get("viewBox").split(), ["0", "0", "16", "16"], path)
    shapes = [e for e in root.iter() if e.tag.replace(SVG, "") in ("path", "rect", "circle", "line", "polygon",
                                                                     "polyline", "ellipse")]
    test.assertLessEqual(len(shapes), 10, f"{path}: a 16 px icon keeps few shapes")


def check_mono(test, path):
    text = read_text(path)
    inks = set(re.findall(r"(?:fill|stroke)\s*[=:]\s*['\"]?\s*(#[0-9A-Fa-f]{3,8}|currentColor|[a-z]+\()", text))
    test.assertEqual(inks, {"currentColor"}, path)
    test.assertNotIn("Gradient", text, path)


def check_animation(test, path):
    """The animated mark ends inside 5 s (WCAG 2.2.2) and rests on its still under reduced motion."""
    text = read_text(path)
    test.assertRegex(text, r"@keyframes", path)
    m = re.search(r"@media\s*\(\s*prefers-reduced-motion:\s*reduce\s*\)\s*\{(.*?)\}\s*\}", text, re.S)
    test.assertTrue(m, f"{path}: no reduced-motion block")
    test.assertRegex(m.group(1), r"animation\s*:\s*none", path)
    test.assertNotRegex(text, r"\binfinite\b", f"{path}: autoplay must end (WCAG 2.2.2)")
    test.assertNotRegex(text, r"<animate|<set\b", f"{path}: SMIL ignores the reduced-motion query")
    test.assertNotRegex(text, r"animation-(?:duration|delay|iteration-count)", f"{path}: shorthand only")
    decls = re.findall(r"animation\s*:\s*([^;}]+)", text)
    test.assertTrue([x for x in decls if x.strip() != "none"], path)
    for decl in decls:
        test.assertNotRegex(decl, r"(?<!\d)\.\d+m?s\b", f"{path}: write 0.5s, not .5s, so the bound below reads it")
        bare =re.sub(r"[\w-]+\([^)]*\)", " ", decl).split()  # drop cubic-bezier(…) and steps(…)
        secs = [float(x[:-2]) / 1000 if x.endswith("ms") else float(x[:-1])
                for x in bare if re.fullmatch(r"\d+(?:\.\d+)?m?s", x)]
        count = [float(x) for x in bare if re.fullmatch(r"\d+(?:\.\d+)?", x)]
        end = (secs[1] if len(secs) > 1 else 0) + (secs[0] if secs else 0) * (count[0] if count else 1)
        test.assertLessEqual(end, 5, f"{path}: {decl.strip()} ends after 5 s (WCAG 2.2.2)")
    return text


class Tokens(unittest.TestCase):
    def test_both_themes_carry_the_same_roles(self):
        t = tokens()
        light, dark = set(t["light"]["color"]), set(t["dark"]["color"])
        self.assertEqual(light, dark)
        self.assertTrue({"surface", "raised", "text", "text-muted", "border", "accent", "on-accent", "glow",
                         "ember"} <= light, light)

    def test_the_palette_names_the_six_materials(self):
        brand = tokens()["brand"]["color"]
        for name in ("forge-light", "hammered-bronze", "iron", "parchment", "blueprint", "ember"):
            self.assertIn(name, brand)
            self.assertRegex(brand[name]["$value"], r"^#[0-9A-Fa-f]{6}$")

    def test_every_text_pair_passes_wcag_aa_in_both_themes(self):
        pairs = tokens()["$extensions"]["sampo"]["pairs"]
        named = set()
        for p in pairs:
            floor = p["min"]
            if p.get("kind", "text") == "text":
                self.assertGreaterEqual(floor, 4.5, p)  # a text pair can't lower its own floor below AA
                named.add(p["fg"])
            for theme in ("light", "dark"):
                fg, bg = hex_of(theme, p["fg"]), hex_of(theme, p["bg"])
                self.assertGreaterEqual(ratio(fg, bg), floor, f"{theme}: {p['fg']} {fg} on {p['bg']} {bg}")
        text_roles = {r for r in tokens()["light"]["color"] if r.startswith(("text", "on-")) or r == "accent"}
        self.assertEqual(text_roles - named, set(), "a text role no pair proves")

    def test_the_chart_series_pass_3_to_1_on_the_panel_and_neighbours_differ_in_hue(self):
        """T-2757: six series per theme; the site's chart panel is the raised surface."""
        for theme in ("light", "dark"):
            series = tokens()[theme]["chart"]
            self.assertEqual([k for k in series if not k.startswith("$")], [f"s{i}" for i in range(1, 7)])
            cols = [series[f"s{i}"]["$value"] for i in range(1, 7)]
            for c in cols:
                self.assertGreaterEqual(ratio(c, hex_of(theme, "raised")), 3, f"{theme}: {c}")
            hues = [design.oklch_of(design.parse_colour(c))[2] for c in cols]
            for i, a in enumerate(hues):
                for j, b in enumerate(hues[:i]):
                    gap = min(abs(a - b), 360 - abs(a - b))
                    self.assertGreaterEqual(gap, 40 if j == i - 1 else 10, f"{theme}: s{j + 1} vs s{i + 1}")

    def test_the_preview_and_the_site_css_carry_the_chart_series_from_the_tokens(self):
        preview = read_text(os.path.join(ROOT, "index.html"))
        css = read_text(os.path.join(os.path.dirname(os.path.dirname(ROOT)), "site", "style.css"))
        for theme in ("light", "dark"):
            for k, v in tokens()[theme]["chart"].items():
                if not k.startswith("$"):
                    self.assertIn(f"--{k}: {v['$value']};", preview, theme)
                    self.assertIn(f"--{k}: {v['$value']};", css, theme)

    def test_status_hues_stay_clear_of_the_forge(self):
        # forge light and ember are brand fire, never a status: each status hue sits 30 degrees or more away
        def hue(h):
            return design.oklch_of(design.parse_colour(h))[2]

        for theme in ("light", "dark"):
            for status in ("error", "warning", "success"):
                for fire in ("glow", "ember"):
                    a, b = hue(hex_of(theme, status)), hue(hex_of(theme, fire))
                    gap = min(abs(a - b), 360 - abs(a - b))
                    self.assertGreaterEqual(gap, 30, f"{theme}: {status} {a:.0f} vs {fire} {b:.0f}")

    def test_type_stacks_are_system_fonts_ending_in_a_generic(self):
        fams = tokens()["font"]
        for role in ("display", "text", "mono"):
            stack = fams[role]["$value"]
            self.assertIsInstance(stack, list)
            self.assertIn(stack[-1], GENERIC, role)
            self.assertEqual(outside(json.dumps(stack)), [])
        self.assertNotRegex(json.dumps(tokens()), r"https?://|@font-face|\.woff")

    def test_motion_rules_bound_autoplay_and_name_a_reduced_still(self):
        m = tokens()["motion"]
        for name in ("tap", "small", "enter", "exit", "move", "stage"):
            self.assertRegex(m["duration"][name]["$value"], r"^\d+ms$")
        for name in ("enter", "exit", "move"):
            self.assertEqual(len(m["easing"][name]["$value"]), 4)
        self.assertLessEqual(int(m["autoplay-limit"]["$value"].rstrip("ms")), 5000)  # WCAG 2.2.2
        self.assertIn("still", m["reduced"]["$description"])


class Directions(unittest.TestCase):
    def test_three_directions_each_with_five_variants_and_a_card(self):
        names = directions()
        self.assertEqual(len(names), 3, names)
        for d in names:
            for v in VARIANTS + ("README.md",):
                self.assertTrue(os.path.isfile(os.path.join(DIRS, d, v)), f"{d}/{v}")
            card = read_text(os.path.join(DIRS, d, "README.md"))
            for head in ("Concept", "Palette", "Strong", "Weak"):
                self.assertRegex(card, rf"(?m)^## {head}", f"{d}: README lacks {head}")

    def test_every_svg_is_well_formed_and_loads_nothing_from_another_host(self):
        for d in directions():
            for v in VARIANTS:
                check_svg(self, os.path.join(DIRS, d, v))

    def test_the_16_px_icon_is_drawn_on_a_16_grid(self):
        for d in directions():
            check_icon_16(self, os.path.join(DIRS, d, "icon-16.svg"))

    def test_mono_uses_one_ink(self):
        for d in directions():
            check_mono(self, os.path.join(DIRS, d, "mono.svg"))

    def test_the_animated_mark_rests_on_its_still_under_reduced_motion(self):
        for d in directions():
            check_animation(self, os.path.join(DIRS, d, "mark-animated.svg"))


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
        return None
    return struct.unpack(">II", head[16:24])


def ico_sizes(path):
    """The (width, height) of each PNG entry in an .ico; None when an entry isn't a PNG inside the file."""
    with open(path, "rb") as f:
        data = f.read()
    reserved, kind, count = struct.unpack("<HHH", data[:6])
    if reserved != 0 or kind != 1:
        return None
    sizes = []
    for i in range(count):
        w, h, _, _, _, _, size, offset = struct.unpack("<BBBBHHII", data[6 + 16 * i:22 + 16 * i])
        if offset + size > len(data) or data[offset:offset + 8] != b"\x89PNG\r\n\x1a\n":
            return None
        sizes.append((w or 256, h or 256))
    return sorted(sizes)


FIRE = {"#6E9BFF": "blue", "#FFC24D": "gold", "#FF6A4A": "red", "#45E0A0": "green", "#BC8BFF": "violet"}


def by_id(path, ident):
    return next((e for e in ET.fromstring(read_text(path)).iter() if e.get("id") == ident), None)


def shorthand(text, selector):
    """The times and count of selector's animation shorthand: (duration, delay, count)."""
    m = re.search(re.escape(selector) + r"\{[^}]*?animation:\w+ ([\d.]+)s [\w-]+(?:\([^)]*\))? ([\d.]+)s(?: (\d+))?", text)
    return m and (float(m.group(1)), float(m.group(2)), int(m.group(3) or 1))


def frames(text, name):
    """A @keyframes block as {percent: declarations}."""
    body = re.search(r"@keyframes %s\{(.*?\})\}" % name, text, re.S).group(1)
    out = {}
    for sel, decl in re.findall(r"([\d.%,]+)\{([^}]*)\}", body):
        for pc in sel.split(","):
            out[float(pc.rstrip("%"))] = decl
    return out


class Logo(unittest.TestCase):
    """T-2850: the anvil-stone mark from direction 12 (the illustrated forge) at three levels, full, simplified and the
    16 px glyph, and every variant SAMPO.md's Logo paragraph names, in design/sampo/logo/."""

    def test_every_variant_is_there(self):
        for name in LOGO_SVGS + tuple(RASTERS) + ("favicon.ico", "pane-glyph.txt", "README.md", "REVIEW.md"):
            self.assertTrue(os.path.isfile(os.path.join(LOGO, name)), name)

    def test_every_svg_is_well_formed_and_loads_nothing_from_another_host(self):
        for name in LOGO_SVGS:
            check_svg(self, os.path.join(LOGO, name), limit=160000)

    def test_the_rasters_have_their_sizes(self):
        for name, size in RASTERS.items():
            self.assertEqual(png_size(os.path.join(LOGO, name)), size, name)

    def test_the_favicon_ico_packs_16_32_and_48(self):
        self.assertEqual(ico_sizes(os.path.join(LOGO, "favicon.ico")), [(16, 16), (32, 32), (48, 48)])

    def test_the_small_icon_is_its_own_16_grid_drawing(self):
        check_icon_16(self, os.path.join(LOGO, "icon-16.svg"))
        self.assertNotIn('id="runes"', read_text(os.path.join(LOGO, "icon-16.svg")), "no runes at 16 px")

    def test_mono_uses_one_ink(self):
        check_mono(self, os.path.join(LOGO, "mono.svg"))

    def test_every_level_and_composed_mark_shares_one_anvil_and_one_stone(self):
        """The stone (three facets) and the anvil over it are one drawing: the full mark, the simplified one, mono and
        every composition carry the same outlines, so no variant drifts from the mark."""
        names = ("mark.svg", "mark-simple.svg") + COMPOSED
        for part in ("stone", "anvil"):
            ds = {}
            for name in names:
                e = by_id(os.path.join(LOGO, name), part)
                self.assertIsNotNone(e, f"{name}: no {part}")
                ds[name] = e.get("d")
            self.assertEqual(len(set(ds.values())), 1, f"{part} differs: {ds}")
        self.assertEqual(by_id(os.path.join(LOGO, "mark.svg"), "stone").get("d").count("M"), 3, "three facets")

    def test_the_runes_glow_in_five_fire_colours(self):
        for name in ("mark.svg", "mark-animated.svg"):
            runes = list(by_id(os.path.join(LOGO, name), "runes"))
            self.assertEqual(len(runes), 5, name)
            colours = [next(p.get("stroke") for p in r.iter() if p.get("stroke")).upper() for r in runes]
            self.assertEqual(sorted(FIRE[c] for c in colours if c in FIRE), sorted(FIRE.values()), f"{name}: {colours}")
            drawings = {next(p.get("d") for p in r.iter() if p.get("d")) for r in runes}
            self.assertEqual(len(drawings), 5, f"{name}: two runes share a drawing")

    def test_the_hammer_strikes_and_settles_inside_five_seconds(self):
        text = check_animation(self, os.path.join(LOGO, "mark-animated.svg"))
        self.assertIn('class="hm"', text)
        rest = re.search(r"\.hm\{[^}]*?transform:([^;}]+)", text).group(1)
        swing = frames(text, "swing")
        pose = lambda decl: re.search(r"transform:([^;}]+)", decl).group(1)
        self.assertEqual(pose(swing[0]), rest, "it starts from the raised pose")
        self.assertEqual(pose(swing[100]), rest, "it settles on the raised pose, the still")
        strikes = [pc for pc, d in swing.items() if re.search(r"rotate\(-\d", d)]
        self.assertTrue(strikes, "the hammer comes down on the billet")
        dur, delay, count = shorthand(text, ".hm")
        self.assertLessEqual(delay + dur * count, 5)
        self.assertGreaterEqual(count, 1)

    def test_the_sparks_are_big_enough_to_see_and_fly_as_the_hammer_lands(self):
        text = read_text(os.path.join(LOGO, "mark-animated.svg"))
        sparks = [p for g in ET.fromstring(text).iter() if g.get("class") == "sparks" for p in g.iter(SVG + "path")]
        self.assertGreaterEqual(len(sparks), 12)
        for p in sparks:
            self.assertGreaterEqual(float(p.get("stroke-width")), 2, "a spark under 2 units vanishes below 128 px")
            length = float(re.fullmatch(r"M(-[\d.]+) 0 H0", p.get("d")).group(1))
            self.assertGreaterEqual(-length, 6, "a spark is a streak, not a dot")
        self.assertEqual(shorthand(text, ".sparks path"), shorthand(text, ".hm"), "sparks keep the hammer's beat")
        swing, fly = frames(text, "swing"), frames(text, "fly")
        strike = min(pc for pc, d in swing.items() if re.search(r"rotate\(-\d", d))
        lit = min(pc for pc, d in fly.items() if "opacity:1" in d)
        self.assertEqual(lit, strike, "the sparks leave the billet as the hammer meets it")

    def test_the_small_icon_sits_on_whole_and_half_pixels(self):
        root = ET.fromstring(read_text(os.path.join(LOGO, "icon-16.svg")))
        nums = [float(n) for p in root.iter(SVG + "path") for n in re.findall(r"-?\d+(?:\.\d+)?", p.get("d"))]
        self.assertTrue(nums)
        off = sorted({n for n in nums if (n * 2) != int(n * 2)})
        self.assertEqual(off, [], "an edge off the half-pixel grid blurs at 16 px")

    @unittest.skipUnless(shutil.which("rsvg-convert"), "build.py renders its PNGs with rsvg-convert")
    def test_the_generator_rebuilds_every_committed_svg_byte_for_byte(self):
        with tempfile.TemporaryDirectory() as out:
            run = subprocess.run([sys.executable, os.path.join(LOGO, "build.py"), out], capture_output=True, text=True,
                                 timeout=120)
            self.assertEqual(run.returncode, 0, run.stderr[-2000:])
            built = sorted(f for f in os.listdir(out) if f.endswith(".svg"))
            self.assertEqual(built, sorted(f for f in os.listdir(LOGO) if f.endswith(".svg")))
            for name in built:  # the PNGs and the .ico are skipped: their bytes follow the rsvg-convert version
                with open(os.path.join(out, name), "rb") as a, open(os.path.join(LOGO, name), "rb") as b:
                    self.assertEqual(a.read(), b.read(), f"{name}: the committed file is not what build.py makes")

    def test_the_light_variant_takes_the_light_themes_roles(self):
        """The forge keeps its own light by day; only the star above it, drawn on the page itself, takes the theme."""
        for theme, name in (("light", "mark-light.svg"), ("dark", "mark.svg")):
            star = by_id(os.path.join(LOGO, name), "star")
            fill = star.get("fill") or next(p.get("fill") for p in star.iter() if p.get("fill"))
            self.assertEqual(fill.upper(), hex_of(theme, "bronze" if theme == "light" else "accent").upper(), name)
            self.assertGreaterEqual(ratio(fill, hex_of(theme, "surface")), 3, f"{name}: the star holds on the page")

    def test_the_pane_glyph_fits_one_terminal_cell(self):
        lines = dict(ln.split(":", 1) for ln in read_text(os.path.join(LOGO, "pane-glyph.txt")).splitlines()
                     if re.match(r"^(rest|turn):", ln))
        self.assertEqual(sorted(lines), ["rest", "turn"])
        glyphs = lines["rest"].split() + lines["turn"].split()
        for g in glyphs:
            self.assertEqual(len(g), 1, g)
            self.assertIn(unicodedata.east_asian_width(g), ("N", "Na", "H"), f"{g}: may take two cells")
            self.assertTrue(unicodedata.category(g).startswith("S"), g)

    def test_the_review_record_names_its_verdict(self):
        self.assertRegex(read_text(os.path.join(LOGO, "REVIEW.md")), r"(?m)^Verdict: (pending|pass|fail)\b")


class Preview(unittest.TestCase):
    def test_index_previews_every_direction_in_both_themes_from_this_folder(self):
        text = read_text(os.path.join(ROOT, "index.html"))
        for d in directions():
            for v in VARIANTS:
                self.assertIn(f"directions/{d}/{v}", text)
        self.assertIn('data-theme="light"', text)
        self.assertIn('data-theme="dark"', text)
        self.assertIn("prefers-reduced-motion", text)
        self.assertNotRegex(text, r"(?:src|href)\s*=\s*['\"](?:https?:)?//|@import|<script[^>]+src", "no other host")
        self.assertEqual([r for r in outside(text) if not r.startswith("directions/")], [])


if __name__ == "__main__":
    unittest.main()
