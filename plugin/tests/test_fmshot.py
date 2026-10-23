"""T-1636: fm shot captures a page in a headless browser it finds (never installs): a viewport shot, frames in real
time and, for a page that moves, a poster frame (the one with the most painted pixels); with no browser it exits 0
and says why. Capture drives fm shot's own DevTools-pipe code against a stub browser, Unruly against stubs that
flood, hang, die or never start; InABrowser uses a real one."""
import argparse
import base64
import contextlib
import io
import json
import os
import stat
import sys
import time
import unittest
from unittest import mock

from helpers import ForemanTestCase

import fmimg
import fmshot

LIB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lib")
# A stand-in for Chromium's --remote-debugging-pipe: NUL-separated JSON on fds 3 (in) and 4 (out). Each screenshot is
# an 8x8 white PNG with the next count from STUB_PAINT painted black (the first is the viewport shot); every call is
# logged to STUB_LOG. STUB_MODE: flood (endless events once navigated), hang (screenshots never answered), die (exits
# at the first screenshot), nostart (says why on stderr and exits).
STUB = f"""#!{sys.executable}
import base64, json, os, sys, time
sys.path.insert(0, {LIB!r})
import fmimg
mode = os.environ.get("STUB_MODE", "")
if mode == "nostart":
    sys.stderr.write("chrome: error while loading shared libraries: libnss3.so: cannot open shared object file\\n")
    sys.exit(127)
log = open(os.environ["STUB_LOG"], "a")
log.write(json.dumps({{"argv": sys.argv[1:]}}) + "\\n")
paint = [int(x) for x in os.environ.get("STUB_PAINT", "0").split(",")]
shots, buf, k = 0, b"", 0
def send(msg):
    os.write(4, json.dumps(msg).encode() + b"\\0")
while True:
    chunk = os.read(3, 65536)
    if not chunk:
        break
    buf += chunk
    while b"\\0" in buf:
        line, buf = buf.split(b"\\0", 1)
        msg = json.loads(line)
        log.write(json.dumps({{"method": msg["method"], "params": msg.get("params", {{}})}}) + "\\n")
        log.flush()
        res = {{}}
        if msg["method"] == "Target.createTarget":
            res = {{"targetId": "t1"}}
        elif msg["method"] == "Target.attachToTarget":
            res = {{"sessionId": "s1"}}
        elif msg["method"] == "Page.captureScreenshot":
            if mode == "hang":
                time.sleep(3600)
            if mode == "die":
                os._exit(0)
            n = paint[min(shots, len(paint) - 1)]
            shots += 1
            px = bytearray(b"\\xff" * 256)
            for i in range(n):
                px[i * 4:i * 4 + 3] = b"\\0\\0\\0"
            res = {{"data": base64.b64encode(fmimg.encode(8, 8, bytes(px))).decode()}}
        send({{"id": msg["id"], "result": res}})
        if msg["method"] == "Page.navigate":
            while mode == "flood":
                k += 1
                send({{"method": f"Flood.e{{k}}", "sessionId": "s1", "params": {{"pad": "x" * 100}}}})
            send({{"method": "Page.loadEventFired", "sessionId": "s1", "params": {{}}}})
"""


class StubCase(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.page = os.path.join(self.repo, "page.html")
        with open(self.page, "w") as f:
            f.write("<p>hi</p>")
        self.log = os.path.join(self.tmp, "stub.jsonl")
        self.stub = os.path.join(self.tmp, "chrome")
        with open(self.stub, "w") as f:
            f.write(STUB)
        os.chmod(self.stub, stat.S_IRWXU)

    def shot(self, *args, paint="0", check=True):
        env = {"FOREMAN_CHROME": self.stub, "STUB_LOG": self.log, "STUB_PAINT": paint}
        return self.fm("shot", *args, env=env, check=check)

    def calls(self):
        with open(self.log) as f:
            return [json.loads(x) for x in f]


class Capture(StubCase):
    def test_with_no_browser_it_exits_0_naming_why(self):
        empty = os.path.join(self.tmp, "empty")
        os.makedirs(empty)
        env = {"FOREMAN_CHROME": "", "PATH": empty, "HOME": empty, "PLAYWRIGHT_BROWSERS_PATH": empty}
        r = self.fm("shot", self.page, env=env)
        self.assertEqual(r.returncode, 0)
        self.assertIn("no browser", r.stdout)
        self.assertIn("FOREMAN_CHROME", r.stdout)  # how to point it at one
        self.assertIn("installs nothing", r.stdout)
        self.assertFalse(os.path.exists(self.log))
        r = self.fm("shot", self.page, env=dict(env, FOREMAN_CHROME=self.page))  # set, but no program
        self.assertEqual(r.returncode, 0)
        self.assertIn("isn't an executable file", r.stdout)

    def test_playwright_browsers_path_is_honoured(self):
        build = os.path.join(self.tmp, "pw", "chromium_headless_shell-1300", "chrome-headless-shell-linux64")
        os.makedirs(build)
        os.symlink(self.stub, os.path.join(build, "chrome-headless-shell"))
        empty = os.path.join(self.tmp, "empty")
        os.makedirs(empty)
        with mock.patch.dict(os.environ, {"FOREMAN_CHROME": "", "PATH": empty, "HOME": empty,
                                          "PLAYWRIGHT_BROWSERS_PATH": os.path.join(self.tmp, "pw")}):
            self.assertEqual(fmshot.chrome(), os.path.join(build, "chrome-headless-shell"))

    def test_a_stub_browser_lists_the_viewport_frames_and_poster(self):
        data = json.loads(self.shot(self.page, "--frames", "4", "--every", "20", "--json", paint="0,1,4,9,2").stdout)
        [page] = data["pages"]
        names = [os.path.basename(x) for x in page["shots"]]
        self.assertEqual(names, ["viewport.png", "frame-00.png", "frame-01.png", "frame-02.png", "frame-03.png",
                                 "poster.png"])
        self.assertTrue(all(x.startswith(self.home) for x in page["shots"]), "under the project's state dir")
        self.assertEqual(os.path.basename(page["folder"]), "page")  # the file's name, no extension
        self.assertTrue(page["animated"])
        with open(page["shots"][-1], "rb") as a, open(page["shots"][3], "rb") as b:
            self.assertEqual(a.read(), b.read(), "the poster is frame-02, the most painted")
        self.assertEqual(page["poster_of"], "frame-02.png")
        text = self.shot(self.page, "--frames", "4", "--every", "20", paint="0,1,4,9,2").stdout
        self.assertIn("poster.png", text)
        self.assertIn("frame-03.png", text)
        methods = [c.get("method") for c in self.calls()]
        self.assertIn("Emulation.setDeviceMetricsOverride", methods)
        self.assertNotIn("Page.addScriptToEvaluateOnNewDocument", methods)  # real time unless --frozen
        nav = [c["params"]["url"] for c in self.calls() if c.get("method") == "Page.navigate"]
        self.assertTrue(nav[0].startswith("file:///") and nav[0].endswith("/page.html"), nav)

    def test_a_still_page_has_no_poster_and_a_rerun_drops_stale_frames(self):
        page = json.loads(self.shot(self.page, "--frames", "5", "--every", "10", "--json", paint="0,1,4").stdout)["pages"][0]
        folder = os.path.dirname(page["shots"][0])
        self.assertTrue(os.path.exists(os.path.join(folder, "poster.png")))
        r = self.shot(self.page, "--frames", "2", "--every", "10", paint="3")
        self.assertIn("still", r.stdout)
        self.assertEqual(sorted(os.listdir(folder)), ["frame-00.png", "frame-01.png", "viewport.png"])

    def test_frozen_injects_the_smoke_harness_freeze_before_any_page_script(self):
        self.shot(self.page, "--frames", "2", "--every", "10", "--frozen")
        [src] = [c["params"]["source"] for c in self.calls()
                 if c.get("method") == "Page.addScriptToEvaluateOnNewDocument"]
        self.assertIn(fmshot.FREEZE_CSS, src)
        self.assertIn(str(fmshot.FROZEN_MS), src)
        self.assertIn(fmshot.HOLD, [c["params"].get("expression") for c in self.calls()
                                    if c.get("method") == "Runtime.evaluate"])  # held after load, before the shots
        with open(os.path.join(LIB, "smoke_web.cjs")) as f:
            cjs = f.read()
        self.assertIn(fmshot.FREEZE_CSS.split(";")[0], cjs, "the same freeze as fm smoke's frozen profile")
        self.assertIn('new Date("2026-01-15T10:00:00Z")', cjs)

    def test_out_takes_a_folder_and_refuses_a_link(self):
        out = os.path.join(self.tmp, "shots")
        page = json.loads(self.shot(self.page, "--frames", "1", "--out", out, "--json").stdout)["pages"][0]
        self.assertTrue(page["shots"][0].startswith(out + os.sep))
        link = os.path.join(self.tmp, "link")
        os.symlink(out, link)
        r = self.shot(self.page, "--out", link, check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("link", r.stderr + r.stdout)
        # a planted link where a shot goes is never written through
        target = os.path.join(self.tmp, "victim")
        with open(target, "w") as f:
            f.write("keep")
        folder = os.path.dirname(page["shots"][0])
        os.unlink(os.path.join(folder, "viewport.png"))
        os.symlink(target, os.path.join(folder, "viewport.png"))
        self.shot(self.page, "--frames", "1", "--out", out, check=False)
        with open(target) as f:
            self.assertEqual(f.read(), "keep")

    def test_a_linked_page_folder_fails_that_page_and_the_rest_are_shot(self):
        out = os.path.join(self.tmp, "o")
        other = os.path.join(self.repo, "other.html")
        with open(other, "w") as f:
            f.write("<p>2</p>")
        os.makedirs(out)
        os.symlink(self.tmp, os.path.join(out, "page"))
        r = self.shot(self.page, other, "--frames", "1", "--out", out, "--json", check=False)
        self.assertEqual(r.returncode, 1)
        data = json.loads(r.stdout)
        self.assertEqual([os.path.basename(p["folder"]) for p in data["pages"]], ["other"])
        self.assertIn("is a link", data["failed"][0]["error"])

    def test_a_page_beside_its_out_folder_doesnt_collide(self):
        page = json.loads(self.shot(self.page, "--frames", "0", "--out", self.repo, "--json").stdout)["pages"][0]
        self.assertEqual(page["folder"], os.path.join(self.repo, "page"))

    def test_control_characters_never_reach_the_terminal(self):
        odd = os.path.join(self.repo, "a\x1b[2Jb.html")
        with open(odd, "w") as f:
            f.write("<p>x</p>")
        r = self.shot(odd, "--frames", "0")
        self.assertNotIn("\x1b", r.stdout)

    def test_targets_it_refuses(self):
        for bad in ("javascript:alert(1)", os.path.join(self.tmp, "missing.html"), "ftp://example.com/"):
            r = self.shot(bad, check=False)
            self.assertNotEqual(r.returncode, 0, bad)
        for bad in (["--frames", "999"], ["--every", "5"]):
            self.assertNotEqual(self.shot(self.page, *bad, check=False).returncode, 0, bad)

    def test_painted_counts_pixels_off_the_background(self):
        self.assertEqual(fmshot.painted(fmimg.decode(base64.b64decode(_png(3)))), 3)
        self.assertEqual(fmshot.painted(fmimg.decode(base64.b64decode(_png(0)))), 0)


class Unruly(StubCase):
    """A browser that floods, hangs, dies or never starts: each run ends in time and says what happened."""

    def run_shot(self, mode, frames=2):
        args = argparse.Namespace(targets=[self.page], frames=frames, every=10, frozen=False, json=True,
                                  out=os.path.join(self.tmp, "o"), project=None)
        env = {"FOREMAN_CHROME": self.stub, "STUB_LOG": self.log, "STUB_MODE": mode}
        out, code, start = io.StringIO(), 0, time.monotonic()
        with mock.patch.dict(os.environ, env), mock.patch.object(fmshot, "CALL_S", 1), \
                mock.patch.object(fmshot, "LOAD_S", 1), contextlib.redirect_stdout(out):
            try:
                fmshot.cmd_shot(args)
            except SystemExit as e:
                code = e.code
        return code, json.loads(out.getvalue()), time.monotonic() - start

    def test_a_flood_of_events_still_times_out(self):
        code, data, took = self.run_shot("flood")
        self.assertEqual(code, 1)
        self.assertLess(took, 10)
        self.assertIn("no answer to Page.captureScreenshot", data["failed"][0]["error"])

    def test_a_hung_browser_times_out(self):
        code, data, took = self.run_shot("hang")
        self.assertEqual(code, 1)
        self.assertLess(took, 10)
        self.assertIn("no answer to Page.captureScreenshot", data["failed"][0]["error"])

    def test_a_browser_that_dies_is_named(self):
        code, data, took = self.run_shot("die")
        self.assertEqual(code, 1)
        self.assertLess(took, 10)
        self.assertIn("the browser closed", data["failed"][0]["error"])

    def test_a_browser_that_never_starts_says_why(self):
        code, data, took = self.run_shot("nostart")
        self.assertEqual(code, 1)
        self.assertIn("did not start", data["failed"][0]["error"])
        self.assertIn("libnss3.so", data["failed"][0]["error"])  # its own last words


def _png(n):
    px = bytearray(b"\xff" * 64 * 4)
    for i in range(n):
        px[i * 4:i * 4 + 3] = b"\0\0\0"
    return base64.b64encode(fmimg.encode(8, 8, bytes(px)))


@unittest.skipUnless(fmshot.chrome(), "no headless Chromium here")
class InABrowser(ForemanTestCase):
    def test_an_animated_page_gets_a_poster_and_frozen_holds_it_still(self):
        self.fm("init")
        page = os.path.join(self.repo, "spin.html")
        with open(page, "w") as f:
            f.write("<style>@keyframes grow{from{width:10px}to{width:900px}}"
                    "div{height:300px;background:#c00;animation:grow 1.2s linear infinite}</style><div></div>")
        moving = json.loads(self.fm("shot", page, "--frames", "4", "--every", "250", "--json").stdout)["pages"][0]
        self.assertTrue(moving["animated"], moving)
        self.assertTrue(moving["shots"][-1].endswith("poster.png"))
        still = json.loads(self.fm("shot", page, "--frames", "3", "--every", "250", "--frozen", "--json").stdout)
        self.assertFalse(still["pages"][0]["animated"], still)

    def test_frozen_shows_a_fade_in_hero_at_its_end_not_blank(self):
        self.fm("init")
        page = os.path.join(self.repo, "hero.html")
        with open(page, "w") as f:
            f.write("<style>@keyframes fadein{from{opacity:0}to{opacity:1}}"
                    "div{height:300px;background:#c00;animation:fadein .6s forwards}</style><div></div>")
        shot = json.loads(self.fm("shot", page, "--frames", "0", "--frozen", "--json").stdout)["pages"][0]
        self.assertGreater(fmshot.painted(fmimg.load(shot["shots"][0])), 100_000, "the hero, faded in")


if __name__ == "__main__":
    unittest.main()
