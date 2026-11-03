"""T-2747: Sampo's design system and its three logo directions (SAMPO.md, Design). design/sampo/tokens.json is the one
source every surface reads (light and dark palettes, type stacks, motion rules); each of the three directions under
design/sampo/directions/ ships a full mark, a 16 px icon, a monochrome mark, a wordmark and an animated mark whose
still is what reduced motion shows; index.html previews them all in both themes. Nothing loads from another host."""
import json
import os
import re
import unittest
import xml.etree.ElementTree as ET

from helpers import PLUGIN, read_text

import fmdesign

ROOT = os.path.join(os.path.dirname(PLUGIN), "design", "sampo")
DIRS = os.path.join(ROOT, "directions")
VARIANTS = ("mark.svg", "icon-16.svg", "mono.svg", "wordmark.svg", "mark-animated.svg")
SVG = "{http://www.w3.org/2000/svg}"
GENERIC = {"serif", "sans-serif", "monospace", "system-ui", "ui-monospace", "ui-serif", "ui-sans-serif"}


def tokens():
    with open(os.path.join(ROOT, "tokens.json"), encoding="utf-8") as f:
        return json.load(f)


def hex_of(theme, role):
    tok = tokens()[theme]["color"][role]
    v = tok["$value"]
    return v["hex"] if isinstance(v, dict) else v


def ratio(a, b):
    return fmdesign.contrast(fmdesign.parse_colour(a), fmdesign.parse_colour(b))


def directions():
    return sorted(d for d in os.listdir(DIRS) if os.path.isdir(os.path.join(DIRS, d)))


def outside(text):
    """Each reference in text (an attribute or a stylesheet) that would reach past the file itself."""
    refs = re.findall(r"url\(\s*['\"]?([^'\")]*)", text) + re.findall(r"@import\s+['\"]?([^'\";\s]+)", text)
    return [r for r in refs if not r.startswith("#")]


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

    def test_status_hues_stay_clear_of_the_forge(self):
        # forge light and ember are brand fire, never a status: each status hue sits 30 degrees or more away
        def hue(h):
            return fmdesign.oklch_of(fmdesign.parse_colour(h))[2]

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
                path = os.path.join(DIRS, d, v)
                text = read_text(path)
                self.assertNotRegex(text, r"<!(?:DOCTYPE|ENTITY)", f"{path}: no DTD, so no entity reaches out")
                root = ET.fromstring(text)  # raises on a malformed file
                self.assertEqual(root.tag, SVG + "svg", path)
                self.assertTrue(root.get("viewBox"), path)
                tags = {e.tag.replace(SVG, "") for e in root.iter()}
                self.assertFalse(tags & {"script", "foreignObject", "image", "use", "text", "a", "iframe"},
                                 f"{path}: {tags}")
                self.assertNotRegex(text, r"font-family|@font-face|https?://(?!www\.w3\.org/)", path)
                for e in root.iter():
                    for k, val in e.attrib.items():
                        if k.endswith("href") or k == "src":
                            self.assertTrue(val.startswith("#"), f"{path}: {k}={val}")
                        if k.startswith("on"):
                            self.fail(f"{path}: event handler {k}")
                    self.assertEqual(outside(" ".join(e.attrib.values()) + (e.text or "")), [], path)
                self.assertLess(len(text), 12000, f"{path}: keep the geometry small")

    def test_the_16_px_icon_is_drawn_on_a_16_grid(self):
        for d in directions():
            root = ET.fromstring(read_text(os.path.join(DIRS, d, "icon-16.svg")))
            self.assertEqual(root.get("viewBox").split(), ["0", "0", "16", "16"], d)
            shapes = [e for e in root.iter() if e.tag.replace(SVG, "") in ("path", "rect", "circle", "line",
                                                                             "polygon", "polyline", "ellipse")]
            self.assertLessEqual(len(shapes), 10, f"{d}: a 16 px icon keeps few shapes")

    def test_mono_uses_one_ink(self):
        for d in directions():
            text = read_text(os.path.join(DIRS, d, "mono.svg"))
            inks = set(re.findall(r"(?:fill|stroke)\s*[=:]\s*['\"]?\s*(#[0-9A-Fa-f]{3,8}|currentColor|[a-z]+\()",
                                  text))
            self.assertEqual(inks, {"currentColor"}, d)
            self.assertNotIn("Gradient", text, d)

    def test_the_animated_mark_rests_on_its_still_under_reduced_motion(self):
        for d in directions():
            text = read_text(os.path.join(DIRS, d, "mark-animated.svg"))
            self.assertRegex(text, r"@keyframes", d)
            m = re.search(r"@media\s*\(\s*prefers-reduced-motion:\s*reduce\s*\)\s*\{(.*?)\}\s*\}", text, re.S)
            self.assertTrue(m, f"{d}: no reduced-motion block")
            self.assertRegex(m.group(1), r"animation\s*:\s*none", d)
            self.assertNotRegex(text, r"\binfinite\b", f"{d}: autoplay must end (WCAG 2.2.2)")
            self.assertNotRegex(text, r"<animate|<set\b", f"{d}: SMIL ignores the reduced-motion query")
            self.assertNotRegex(text, r"animation-(?:duration|delay|iteration-count)", f"{d}: shorthand only")
            decls = re.findall(r"animation\s*:\s*([^;}]+)", text)
            self.assertTrue([x for x in decls if x.strip() != "none"], d)
            for decl in decls:
                bare = re.sub(r"[\w-]+\([^)]*\)", " ", decl).split()  # drop cubic-bezier(…) and steps(…)
                secs = [float(x[:-2]) / 1000 if x.endswith("ms") else float(x[:-1])
                        for x in bare if re.fullmatch(r"\d+(?:\.\d+)?m?s", x)]
                count = [float(x) for x in bare if re.fullmatch(r"\d+(?:\.\d+)?", x)]
                end = (secs[1] if len(secs) > 1 else 0) + (secs[0] if secs else 0) * (count[0] if count else 1)
                self.assertLessEqual(end, 5, f"{d}: {decl.strip()} ends after 5 s (WCAG 2.2.2)")


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
