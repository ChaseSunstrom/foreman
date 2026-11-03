"""The landing page's layout at phone widths (T-1683): measured in a real headless Chromium, skipped with a reason
when there is none."""
import functools
import http.server
import json
import os
import sys
import threading
import unittest

from helpers import PLUGIN

import fmshot

SITE = os.path.join(os.path.dirname(PLUGIN), "site")
RECTS = """JSON.stringify([...document.querySelectorAll('header.top .brand, header.top .nav > *')]
  .filter(e => getComputedStyle(e).display !== 'none')
  .map(e => { const r = e.getBoundingClientRect(), g = document.createRange(); g.selectNodeContents(e);
              const t = g.getBoundingClientRect();  // T-2089: the text, which can spill past a shrunk box
              return [e.textContent.trim() || e.className, Math.min(r.left, t.left), Math.max(r.right, t.right),
                      r.top, r.bottom]; })
  .concat([['page', 0, document.documentElement.scrollWidth, 0, 0]]))"""


class Header(unittest.TestCase):
    """T-1683: at 320 px the brand overlapped the Install link."""

    @classmethod
    def setUpClass(cls):
        cls.browser = fmshot.find_browser("test_site")[0]
        if not cls.browser:
            raise unittest.SkipTest("no headless Chromium (FOREMAN_CHROME, PATH or Playwright's)")
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=SITE)
        handler.log_message = lambda *a: None
        cls.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def rects(self, width, page="index.html"):
        b = fmshot.Browser(self.browser, (width, 640))
        try:
            fmshot.load(b, f"http://127.0.0.1:{self.server.server_address[1]}/{page}")
            got = b.call("Runtime.evaluate", b.sid, expression=RECTS, returnByValue=True)
            return json.loads(got["result"]["value"])
        finally:
            b.close()

    def test_nothing_in_the_header_overlaps_or_overflows_at_phone_widths(self):
        for width, name in ((w, n) for w in (320, 360, 390) for n in ("index.html", "genesis/index.html")):
            with self.subTest(width=width, page=name):  # T-2089: without Barlow the wider fallback spilled at 360
                *items, page = self.rects(width, name)
                self.assertLessEqual(page[2], width, "the page scrolls sideways")
                for (a, al, ar, at, ab), (b, bl, br, bt, bb) in zip(items, items[1:]):
                    self.assertLessEqual(ar, bl + 0.5, f"{a!r} overlaps {b!r} at {width} px")
                for name, left, right, *_ in items:
                    self.assertGreaterEqual(left, 0, f"{name!r} starts off screen at {width} px")
                    self.assertLessEqual(right, width, f"{name!r} ends off screen at {width} px")


class CodePageCoversFmCode(unittest.TestCase):
    """T-2071: every fm code verb and long flag, read from its own argparse, is on the Foreman Code page, or here with
    a reason; the page drifted 131 commits behind once."""
    SKIP = {  # flag or verb -> why the page leaves it out
        "--project": "fm's own project selector, the same on every verb",    }

    def test_every_verb_and_flag_is_on_the_page(self):
        import argparse
        import re
        import fmcli
        import test_site_build
        sub = next(a for a in fmcli.build_parser()._actions if isinstance(a, argparse._SubParsersAction))
        code = sub.choices["code"]
        flags = {o for a in code._actions for o in a.option_strings
                 if o.startswith("--") and o != "--help" and a.help != argparse.SUPPRESS}  # --tui is internal
        request = next(a for a in code._actions if a.dest == "request").help
        m = re.search(r"\(or: ([^)]*)\)", request)
        self.assertIsNotNone(m, "fm code request help lost its '(or: …)' verb list")
        verbs = set(re.split(r"[ ,]+", m.group(1)))
        self.assertGreaterEqual(len(flags), 30)
        self.assertLessEqual({"models", "runners", "config", "why", "bench", "tui"}, verbs)
        page = next(p for p in test_site_build.site("pages").PAGES if p["slug"] == "code")
        text = " ".join(x for b in page["blocks"] for x in b if isinstance(x, str)) + page["lede"]
        text = re.sub(r"<[^>]+>", "", text)
        missing = sorted(f for f in flags if f not in self.SKIP and not re.search(re.escape(f) + r"(?![\w-])", text))
        missing += sorted("sampo code " + v for v in verbs if v not in self.SKIP and not re.search(
            r"sampo code (?:\w+ )?" + re.escape(v) + r"\b", text))
        self.assertEqual(missing, [], "on fm code's --help but not on the Foreman Code page (site/pages.py): add a "
                                      "sentence, or an entry with a reason in SKIP")
        for k in self.SKIP:  # a stale entry hides nothing
            self.assertTrue(k in flags or k in verbs, k + " is no longer an fm code flag or verb")


class GoalPage(unittest.TestCase):
    def test_the_planning_page_describes_the_goal_verbs_and_the_across_days_line(self):  # T-2141
        sys.path.insert(0, SITE)
        try:
            import pages
        finally:
            sys.path.pop(0)
        page = next(x for x in pages.PAGES if x["slug"] == "planning")
        text = json.dumps(page["blocks"], default=str)
        for word in ("Goal to finish", "sampo goal set", "sampo goal item", "sampo goal link", "sampo goal show",
                     "sampo goal verdict", "sampo task new", "--goal", "across days"):
            self.assertIn(word, text)


class LacksPage(unittest.TestCase):  # T-2378: #5 on the site, its figures from the ledger (site/stats.py)
    def test_the_tools_it_lacks_page_names_every_surface_and_renders_from_state(self):
        sys.path.insert(0, SITE)
        try:
            import pages
            import build
        finally:
            sys.path.pop(0)
        page = next(x for x in pages.PAGES if x["slug"] == "lacks")
        text = json.dumps(page["blocks"], default=str)
        for word in ("sampo which", "sampo new tool", "sampo ask", "--later", "never", "sampo code", "Codex", "MCP", "band"):
            self.assertIn(word, text)
        tools = {"misses": 41, "resolved": 30, "proved": 7, "searches": 55, "queued": 3, "refused": 1}
        html = build.render_page(page, {"tools": tools}, pages.PAGES)
        for figure in ("41", "30", "55"):
            self.assertIn(figure, html)
        self.assertIn('class="tiles"', build.render_page(page, {}, pages.PAGES))  # no data yet: zeros, still a figure
        root = os.path.dirname(SITE)
        for name in ("README.md", "MASTER.md", "CHANGELOG.md"):  # each surface named where a reader looks
            with open(os.path.join(root, name), encoding="utf-8") as f:
                doc = f.read()
            for word in ("`grants`", "fm which", "PostToolUseFailure"):
                self.assertIn(word, doc, f"{name}: {word}")


class ProofPage(unittest.TestCase):  # T-2395: #6/#10 on the site, built from Foreman's own code and data
    def test_proof_page_names_every_kind_from_the_code_and_renders_counts_over_time(self):
        sys.path.insert(0, SITE)
        try:
            import pages
            import build
        finally:
            sys.path.pop(0)
        import fmcore
        page = next(x for x in pages.PAGES if x["slug"] == "verifying")
        text = json.dumps(page["blocks"], default=str)
        for kind in fmcore.PROOF_KINDS:
            self.assertIn(kind, text)
        for word in ("sampo prove --rollup", "proof", "beyond", "unproven"):
            self.assertIn(word, text)
        proof = {"n": 12, "counts": {"typed": 5, "meaning": 4}, "history": [{"day": "2026-10-30", "n": 15},
                                                                             {"day": "2026-10-31", "n": 12}]}
        html = build.render_page(page, {"proof": proof}, pages.PAGES)
        self.assertIn("12", html)
        self.assertIn("meaning", html)
        self.assertIn('class="tiles"', build.render_page(page, {}, pages.PAGES))  # no data: still a figure


class DecisionTape(unittest.TestCase):  # T-2348 (Mission 5 inbox): every fm decide row on one timeline
    def test_the_decisions_page_lists_rows_newest_first_with_kind_confidence_and_reversal(self):
        import shutil
        import tempfile
        sys.path.insert(0, SITE)
        try:
            import pages
            import build
            import stats
        finally:
            sys.path.pop(0)
        d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, d, True)
        with open(os.path.join(d, "decisions.md"), "w", encoding="utf-8") as f:
            f.write("| Date | Decision | Why | Rejected |\n|---|---|---|---|\n"
                    "| 2026-10-30 | [costly] [confidence: 70%] Keep the file cache | fast | |\n"
                    "| 2026-10-31 | Use <b>SQLite</b> for the index | simpler | |\n"
                    "| 2026-11-01 | [reverses: file cache] Drop the cache | stale reads | |\n")
        tape = stats.decisions(d)
        self.assertEqual([x["date"] for x in tape], ["2026-11-01", "2026-10-31", "2026-10-30"])
        self.assertEqual((tape[-1]["kind"], tape[-1]["confidence"], tape[-1]["later"]),
                         ("costly", 70, {"date": "2026-11-01", "how": "reversed"}))
        self.assertIsNone(tape[1]["later"])
        page = next(x for x in pages.PAGES if x["slug"] == "decisions")
        html = build.render_page(page, {"decisions": tape}, pages.PAGES)
        for figure in ("Keep the file cache", "70%", "costly", "reversed 2026-11-01"):
            self.assertIn(figure, html)
        self.assertIn("&lt;b&gt;SQLite", html)  # a row's text is escaped
        self.assertNotIn("<b>SQLite", html)
        self.assertIn('class="tiles"', build.render_page(page, {}, pages.PAGES))


class SelfRunningPage(unittest.TestCase):  # T-2364: Mission 8 on the site, its figures from the ledger and books
    def test_self_running_page_names_each_surface_and_renders_from_state(self):
        sys.path.insert(0, SITE)
        try:
            import pages
            import build
        finally:
            sys.path.pop(0)
        page = next(x for x in pages.PAGES if x["slug"] == "self-running")
        text = json.dumps(page["blocks"], default=str)
        for word in ("sampo triggers", "precision", "route", "sampo night --tick", "install", "sampo lane recover",
                     "trial", "sampo outcomes --predictions", "baseline", "lean", "generation"):
            self.assertIn(word, text)
        sr = {"triggers": [{"trigger": "ci-red", "fired": 9, "precision": 0.78, "route": "inbox"}], "installs": 2,
              "recoveries": 3, "trials": {"held": 4, "didn't hold": 1}, "predictions": [{"kind": "next-request",
              "hit": 0.62, "base_hit": 0.48, "n": 40}], "lean": [{"gen": 1, "rules chars": 5200}]}
        html = build.render_page(page, {"self_running": sr}, pages.PAGES)
        for figure in ("ci-red", "0.78", "62%", "48%"):
            self.assertIn(figure, html)
        self.assertIn('class="tiles"', build.render_page(page, {}, pages.PAGES))
        root = os.path.dirname(SITE)
        for name in ("README.md", "MASTER.md", "CHANGELOG.md"):
            with open(os.path.join(root, name), encoding="utf-8") as f:
                self.assertIn("Self-running", f.read(), name)


class JudgmentPage(unittest.TestCase):  # T-2344: #2 and #8 on the site, its figures from fm outcomes --judgment --json
    def test_judgment_page_describes_the_plan_shape_races_doors_and_scores_from_calibration_data(self):
        sys.path.insert(0, SITE)
        try:
            import pages
            import build
        finally:
            sys.path.pop(0)
        page = next(x for x in pages.PAGES if x["slug"] == "judgment")
        text = json.dumps(page["blocks"], default=str)
        for word in ("Reading", "fails if", "Choice N (NN%)", "sampo lane race", "one-way", "sampo outcomes --judgment",
                     "Brier", "base rate", "MCP", "sampo code"):
            self.assertIn(word, text)
        cal = {"scored": 30, "pending": 4, "brier": {"stated": 0.18, "base": 0.24}, "bars": {"research": 70, "race": 55},
               "races": {"run": 5, "judged": 4, "first_lost": 1}, "doors_parked": ["T-1"],
               "kinds": {"choice": [{"lo": 60, "hi": 79, "n": 3, "held": 2, "pct": 67, "stated": 72, "gap": 5}]},
               "interim": {"task": [{"lo": 80, "hi": 94, "n": 9, "held": 9, "pct": 100}]}}  # T-2498
        html = build.render_page(page, {"calibration": cal}, pages.PAGES)
        for figure in ("0.18", "0.24", "1 of 4", "30", "Held, by stated confidence", "choice 60–79% · n 3", "so far"):
            self.assertIn(figure, html)
        empty = build.render_page(page, {}, pages.PAGES)
        self.assertIn("not scored yet", empty)  # no data: said, never a crash
        self.assertIn("no reliability chart", empty)


if __name__ == "__main__":
    unittest.main()


class ModelLayerPage(unittest.TestCase):  # T-2489: the gen-2 model layer on the site, its figures from the exam's replay
    def test_model_layer_page_states_the_rules_and_renders_the_newest_replay(self):
        import shutil
        import tempfile
        sys.path.insert(0, SITE)
        try:
            import pages
            import build
            import stats
        finally:
            sys.path.pop(0)
        page = next(x for x in pages.PAGES if x["slug"] == "model-layer")
        text = json.dumps(page["blocks"], default=str)
        for word in ("rule", "local", "cloud", "sensitive", "shadow", "exam", "model-live", "proof", "MCP", "Brier",
                     "install"):
            self.assertIn(word, text)
        mr = {"intake-type": {"n": 40, "path_hits": 31, "model_n": 12, "model_hits": 10, "brier": 0.14, "ms": 820}}
        html = build.render_page(page, {"models": {"run": "s2-1", "replay": mr}}, pages.PAGES)
        for figure in ("intake-type", "31 of 40", "10 of 12", "0.14", "820"):
            self.assertIn(figure, html)
        self.assertIn('class="tiles"', build.render_page(page, {}, pages.PAGES))
        d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, d, True)
        os.makedirs(os.path.join(d, "research", "genesis"))
        with open(os.path.join(d, "research", "genesis", "exam.jsonl"), "w", encoding="utf-8") as f:
            for row in ({"run": "s1-1", "model_replay": {"dedupe": {"n": 1}}}, {"run": "s2-1", "model_replay": mr},
                        {"run": "s2-2"}, "not json"):
                f.write((row if isinstance(row, str) else json.dumps(row)) + "\n")
        self.assertEqual(stats.models(d), {"run": "s2-1", "replay": mr})
        self.assertEqual(stats.models(tempfile.gettempdir() + "/no-such-state-T2489"), {})
        root = os.path.dirname(SITE)
        for name in ("README.md", "MASTER.md", "CHANGELOG.md"):
            with open(os.path.join(root, name), encoding="utf-8") as f:
                self.assertIn("Model layer", f.read(), name)
