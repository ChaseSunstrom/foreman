"""fm page looks (T-1649): one self-contained gallery page with a living specimen per look card."""
import glob
import json
import os
import re
import shutil

from helpers import ForemanTestCase, read_text

import fmdesign
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


class Roll(ForemanTestCase):
    """fm design roll (T-1648): a seeded pick of one look card, written into DESIGN.md as one patch --undo reverses."""

    def setUp(self):
        super().setUp()
        self.fm("init")
        self.md = os.path.join(self.repo, "DESIGN.md")

    def roll(self, *extra, check=True):
        r = self.fm("design", "roll", *extra, "--json", check=check)
        return json.loads(r.stdout) if r.returncode == 0 else r

    def test_the_same_seed_gives_the_same_coherent_look_and_never_a_generic_face(self):
        a, b = self.roll("--seed", "7"), self.roll("--seed", "7")
        self.assertEqual(a, b)
        cards = {x["name"]: x for x in fmpage.look_cards()}
        picked = set()
        for n in range(8):
            got = self.roll("--seed", str(n))
            picked.add(got["look"])
            card = cards[got["look"]]
            self.assertEqual(got["roles"], card["roles"], "palette, type and motion all come from one card")
            self.assertEqual([t["class"] for t in got["type"]], card["faces"])
            self.assertEqual(got["motion"], card["motion"])
            for t in got["type"]:
                self.assertNotIn(t["lead"].strip('"').lower(), fmdesign.GENERIC_FONTS, t)
                self.assertNotRegex(t["stack"], r"(?i)(?<![\w-])inter(?![\w-])", t)
        self.assertGreater(len(picked), 3, "seeds spread over the cards")
        self.assertFalse(os.path.exists(self.md), "a roll without --apply writes nothing")
        r = self.fm("design", "roll", check=False)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertRegex(r.stdout, r"seed \d+", "an unseeded roll prints the seed that repeats it")

    def test_apply_then_undo_restores_design_md_byte_for_byte_across_rerolls(self):
        before = b"# DESIGN.md: shop\r\n\r\n## Direction\r\nWarm and plain.\r\n\r\n## Knobs\r\n- density: calm\r\n"
        with open(self.md, "wb") as f:
            f.write(before)
        got = self.roll("--seed", "3", "--apply")
        with open(self.md, "rb") as f:
            text = f.read().decode()
        self.assertIn("## Look", text)
        self.assertIn(got["roles"]["--accent"], text)
        self.assertIn(f"seed {got['seed']}", text)
        self.assertIn("## Direction\r\nWarm and plain.", text, "the rest is kept, CRLF and all")
        self.assertNotIn("\n", text.replace("\r\n", ""), "every line end stays CRLF")
        self.roll("--seed", "4", "--apply")  # a reroll replaces its own section; undo still goes back to the start
        self.assertEqual(read_text(self.md).count("## Look"), 1)
        self.fm("design", "roll", "--undo")
        with open(self.md, "rb") as f:
            self.assertEqual(f.read(), before)
        r = self.fm("design", "roll", "--undo", check=False)
        self.assertEqual(r.returncode, 2)
        self.assertIn("nothing to undo", r.stderr)

    def test_golden_seeds_name_their_card_in_the_written_section(self):
        # a seed's meaning changes when the cards do: update these with the card set, and the ## Look names its card
        golden = {0: "look-lido", 1: "look-card-catalogue", 2: "look-archive-ledger", 3: "look-cartographer"}
        self.assertEqual({s: self.roll("--seed", str(s))["look"] for s in golden}, golden)
        self.roll("--seed", "3", "--apply")
        self.assertIn("`look-cartographer` (Cartographer), seed 3", read_text(self.md))

    def undo_files(self, ext=".json"):
        return glob.glob(os.path.join(self.home, "state", "projects", "*", "design-roll", "*" + ext))

    def test_a_failed_or_half_done_reroll_keeps_the_bytes_before_the_first_roll(self):
        if os.geteuid() == 0:
            self.skipTest("root writes into a read-only folder")
        before = b"# DESIGN.md: mine\n\nkept\n"
        with open(self.md, "wb") as f:
            f.write(before)
        self.roll("--seed", "1", "--apply")
        os.chmod(self.repo, 0o555)  # the next write of DESIGN.md fails
        try:
            r = self.roll("--seed", "2", "--apply", check=False)
        finally:
            os.chmod(self.repo, 0o755)
        self.assertEqual(r.returncode, 2, r)
        self.roll("--seed", "3", "--apply")
        (rec_path,) = self.undo_files()
        with open(rec_path, encoding="utf-8") as f:
            rec = json.load(f)
        rec["after"] = None  # a roll that died after its write, before it recorded what it wrote
        with open(rec_path, "w", encoding="utf-8") as f:
            json.dump(rec, f)
        self.roll("--seed", "4", "--apply")
        self.fm("design", "roll", "--undo")
        with open(self.md, "rb") as f:
            self.assertEqual(f.read(), before)
        self.assertEqual(self.undo_files() + self.undo_files(".orig"), [])

    def test_a_half_done_roll_on_no_file_undoes_quietly_and_an_edited_file_keeps_a_plain_copy(self):
        self.roll("--seed", "1", "--apply")
        os.remove(self.md)  # as if the roll died before its write: no file, a record with nothing after it
        (rec_path,) = self.undo_files()
        with open(rec_path, encoding="utf-8") as f:
            rec = json.load(f)
        rec["after"] = None
        with open(rec_path, "w", encoding="utf-8") as f:
            json.dump(rec, f)
        self.fm("design", "roll", "--undo")
        self.assertFalse(os.path.exists(self.md))
        with open(self.md, "wb") as f:
            f.write(b"original\n")
        self.roll("--seed", "1", "--apply")
        (orig,) = self.undo_files(".orig")
        with open(orig, "rb") as f:
            self.assertEqual(f.read(), b"original\n", "a plain copy anyone can restore by hand")
        with open(self.md, "a", encoding="utf-8") as f:
            f.write("\nedited\n")
        r = self.fm("design", "roll", "--undo", check=False)
        self.assertIn(orig, r.stderr)

    def test_undo_removes_a_design_md_the_roll_created_and_refuses_one_edited_since(self):
        self.roll("--seed", "1", "--apply")
        self.fm("design", "roll", "--undo")
        self.assertFalse(os.path.exists(self.md))
        self.roll("--seed", "1", "--apply")
        with open(self.md, "a", encoding="utf-8") as f:
            f.write("\nmy own note\n")
        r = self.fm("design", "roll", "--undo", check=False)
        self.assertEqual(r.returncode, 2)
        self.assertIn("changed since", r.stderr)
        self.assertIn("my own note", read_text(self.md), "an edit after the roll is never thrown away")

    def test_a_symlinked_design_md_is_refused_and_its_target_untouched(self):
        target = os.path.join(self.tmp, "elsewhere.md")
        with open(target, "w", encoding="utf-8") as f:
            f.write("mine\n")
        os.symlink(target, self.md)
        r = self.roll("--seed", "2", "--apply", check=False)
        self.assertEqual(r.returncode, 2)
        self.assertIn("symlink", r.stderr)
        self.assertEqual(read_text(target), "mine\n")
        r = self.fm("design", "roll", "--seed", "x", check=False)
        self.assertNotEqual(r.returncode, 0)
        r = self.fm("design", "lint", check=False)
        self.assertEqual(r.returncode, 2, "lint still needs its paths")
