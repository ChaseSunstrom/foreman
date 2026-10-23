"""The landing page's layout at phone widths (T-1683): measured in a real headless Chromium, skipped with a reason
when there is none."""
import functools
import http.server
import json
import os
import threading
import unittest

from helpers import PLUGIN

import fmshot

SITE = os.path.join(os.path.dirname(PLUGIN), "site")
RECTS = """JSON.stringify([...document.querySelectorAll('header.top .brand, header.top .nav > *')]
  .filter(e => getComputedStyle(e).display !== 'none')
  .map(e => { const r = e.getBoundingClientRect(); return [e.textContent.trim() || e.className, r.left, r.right,
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

    def rects(self, width):
        b = fmshot.Browser(self.browser, (width, 640))
        try:
            fmshot.load(b, f"http://127.0.0.1:{self.server.server_address[1]}/index.html")
            got = b.call("Runtime.evaluate", b.sid, expression=RECTS, returnByValue=True)
            return json.loads(got["result"]["value"])
        finally:
            b.close()

    def test_nothing_in_the_header_overlaps_or_overflows_at_phone_widths(self):
        for width in (320, 360, 390):
            with self.subTest(width=width):
                *items, page = self.rects(width)
                self.assertLessEqual(page[2], width, "the page scrolls sideways")
                for (a, al, ar, at, ab), (b, bl, br, bt, bb) in zip(items, items[1:]):
                    self.assertLessEqual(ar, bl + 0.5, f"{a!r} overlaps {b!r} at {width} px")
                for name, left, right, *_ in items:
                    self.assertGreaterEqual(left, 0, f"{name!r} starts off screen at {width} px")
                    self.assertLessEqual(right, width, f"{name!r} ends off screen at {width} px")


if __name__ == "__main__":
    unittest.main()
