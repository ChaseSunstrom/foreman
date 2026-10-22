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
        # motion plays once and honours reduced motion
        self.assertIn("prefers-reduced-motion: reduce", html)
        self.assertNotIn("infinite", html)
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
            text = f.read().replace('title: "Look: Lido"', 'title: "Look: Pier </style><script>x()</script>"')
        with open(os.path.join(folder, "look-pier.md"), "w", encoding="utf-8") as f:
            f.write(text.replace("name: look-lido", "name: look-pier"))
        html = fmpage.looks_html(fmpage.look_cards(folder))
        self.assertEqual(re.findall(r'<section class="specimen" id="(look-[\w-]+)"', html), ["look-lido", "look-pier"])
        self.assertEqual(html.count('class="plate" data-plate="fallback"'), 1)
        self.assertNotIn("<script>x()", html)
        self.assertIn("Pier &lt;/style&gt;", html)

    def test_out_must_be_a_plain_html_file_and_looks_takes_no_catalogue(self):
        r = self.fm("page", "looks", "--out", os.path.join(self.tmp, "looks.txt"), check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn(".html", r.stderr)
        r = self.fm("page", "looks", "--catalogue", "cat", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("looks", r.stderr)
