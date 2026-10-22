"""fm page looks (T-1649): one self-contained gallery page with a living specimen per look card."""
import os
import re
import shutil

from helpers import ForemanTestCase, read_text

import fmpage
import fmtaste

# a load from another host: a src/href, a CSS url() or an @import that names one (an SVG xmlns is no load)
OUTSIDE = re.compile(r"""(?:\b(?:src|href|action|poster)\s*=\s*["']?|url\(\s*["']?|@import\s*["']?)(?:[a-z][\w+.-]*:)?//""",
                     re.I)


def names(folder=fmtaste.LOOKS):
    return sorted(n[:-3] for n in os.listdir(folder) if n.startswith("look-") and n.endswith(".md"))


def hidden_rules(html):
    """Selectors outside @keyframes that set opacity 0 (an empty ::before/::after glow is decoration, not content)."""
    css = "".join(re.findall(r"<style>(.*?)</style>", html, re.S))
    css = re.sub(r"@keyframes[^{]*\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}", "", css)
    return [sel.strip() for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css)
            if re.search(r"(?<![\w-])opacity\s*:\s*0(?![.\d])", body)
            and not all(re.search(r"::?(?:before|after)$", s.strip()) for s in sel.split(","))]


class Gallery(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.out = os.path.join(self.tmp, "looks.html")

    def test_one_specimen_per_look_card_in_one_file_with_no_outside_host(self):
        r = self.fm("page", "looks", "--out", self.out)
        self.assertIn(self.out, r.stdout)
        html = read_text(self.out)
        got = re.findall(r'<section class="specimen" id="(look-[\w-]+)"', html)
        self.assertEqual(sorted(got), names())
        self.assertGreaterEqual(len(got), 12)
        self.assertNotIn('class="plate" data-plate="fallback"', html, "every look card today has its own specimen")
        self.assertIsNone(OUTSIDE.search(html), OUTSIDE.search(html) and html[OUTSIDE.search(html).start() - 80:][:200])
        self.assertNotIn("<link", html)
        self.assertIsNone(re.search(r"<script\b[^>]*\bsrc\s*=", html))
        self.assertNotRegex(html, r"__[A-Z]+__", "every placeholder filled")
        self.assertNotRegex(html, r"<!--/?look\b", "no specimen block markers left")
        # motion plays once and honours reduced motion; nothing waits hidden for a script or an animation
        self.assertIn("prefers-reduced-motion: reduce", html)
        self.assertNotIn("infinite", html)
        self.assertEqual(hidden_rules(html), [], "a rule outside @keyframes hides content with opacity 0")
        reduce = "".join(re.findall(r"@media \(prefers-reduced-motion: reduce\) \{(.*?)\}\s*\}", html, re.S))
        self.assertRegex(reduce, r"\.bc \.window \{[^}]*overflow-x: auto", "a still ticker scrolls by hand")
        self.assertRegex(reduce, r"\.bc \.track span\[aria-hidden[^{]*\{[^}]*display: none", "no duplicate lap")
        # each specimen wears its own card's palette
        for card in fmpage.look_cards():
            block = re.search(r'#%s \{([^}]*)\}' % card["name"], html)
            self.assertIsNotNone(block, card["name"])
            for role in ("--surface", "--text", "--accent"):
                self.assertIn(f"{role}: {card['roles'][role]}", block.group(1), (card["name"], role))

    def test_the_loader_reads_palette_roles_and_the_type_pair(self):
        cards = {x["name"]: x for x in fmpage.look_cards()}
        self.assertEqual(sorted(cards), names())
        self.assertEqual(cards["look-archive-ledger"]["faces"], ["transitional serif", "mono"])
        self.assertEqual(cards["look-transit-signage"]["faces"], ["neo-grotesk"])
        self.assertEqual(cards["look-night-market"]["faces"], ["slab", "humanist sans"])
        self.assertEqual(cards["look-broadcast-graphics"]["roles"]["--strap"], "#16191C")
        for x in cards.values():
            self.assertTrue({"--surface", "--text", "--text-muted", "--accent"} <= set(x["roles"]), x["name"])
            self.assertTrue(x["faces"] and x["title"] and x["line"] and x["motion"] and x["texture"], x["name"])

    def test_a_card_without_its_own_specimen_gets_the_plain_one_and_its_text_is_escaped(self):
        folder = os.path.join(self.tmp, "looks")
        os.makedirs(folder)
        shutil.copy(os.path.join(fmtaste.LOOKS, "look-lido.md"), folder)
        with open(os.path.join(fmtaste.LOOKS, "look-lido.md"), encoding="utf-8") as f:
            text = (f.read().replace('title: "Look: Lido"', 'title: "Look: Pier </style><script>x()</script>"')
                    .replace("An open-air public pool:", "A pier <img src=x onerror=y()> & </section>:")
                    .replace("Clear and calm:", "Clear `</code><b>bold` and calm <script>z()</script>:"))
        with open(os.path.join(folder, "look-pier.md"), "w", encoding="utf-8") as f:
            f.write(text.replace("name: look-lido", "name: look-pier"))
        html = fmpage.looks_html(fmpage.look_cards(folder))
        self.assertEqual(re.findall(r'<section class="specimen" id="(look-[\w-]+)"', html), ["look-lido", "look-pier"])
        self.assertEqual(html.count('class="plate" data-plate="fallback"'), 1)
        for raw in ("<script>x()", "<img src=x", "<script>z()", "<b>bold", "& </section>"):
            self.assertNotIn(raw, html)
        for shown in ("Pier &lt;/style&gt;", "A pier &lt;img src=x onerror=y()&gt; &amp; &lt;/section&gt;:",
                      "<code>&lt;/code&gt;&lt;b&gt;bold</code> and calm &lt;script&gt;z()&lt;/script&gt;"):
            self.assertIn(shown, html)

    def test_out_refuses_a_file_foreman_did_not_write_and_replaces_its_own(self):
        mine = os.path.join(self.tmp, "notes.html")
        with open(mine, "w", encoding="utf-8") as f:
            f.write("<p>my own notes</p>\n")
        for verb in (("page", "looks"), ("page",)):
            r = self.fm(*verb, "--out", mine, check=False)
            self.assertNotEqual(r.returncode, 0, verb)
            self.assertIn("isn't one fm page wrote", r.stderr)
            self.assertEqual(read_text(mine), "<p>my own notes</p>\n", "the user's file is untouched")
        for verb, out in ((("page", "looks"), self.out), (("page",), os.path.join(self.tmp, "board.html"))):
            self.fm(*verb, "--out", out)
            self.fm(*verb, "--out", out)  # a second run replaces the page it wrote

    def test_out_must_be_a_plain_html_file_and_looks_takes_no_catalogue(self):
        r = self.fm("page", "looks", "--out", os.path.join(self.tmp, "looks.txt"), check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn(".html", r.stderr)
        r = self.fm("page", "looks", "--catalogue", "cat", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("looks", r.stderr)
