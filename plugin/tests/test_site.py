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
        missing += sorted("fm code " + v for v in verbs if v not in self.SKIP and not re.search(
            r"fm code (?:\w+ )?" + re.escape(v) + r"\b", text))
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
        for word in ("Goal to finish", "fm goal set", "fm goal item", "fm goal link", "fm goal show", "fm goal verdict",
                     "fm task new", "--goal", "across days"):
            self.assertIn(word, text)


if __name__ == "__main__":
    unittest.main()
