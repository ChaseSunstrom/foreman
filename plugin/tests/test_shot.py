"""The UI snapshot harness (mods/foreman-ui/tools/shot.py) never leaks FOREMAN_* into a tmux server's global
environment, where every later session would inherit it (T-0138: a leaked FOREMAN_STATE pointed the user's own
Claude Code session at the demo state).

T-1636: fm shot captures a page in a headless browser it finds (never installs): a viewport shot, frames in real
time and, for a page that moves, a poster frame (the one with the most painted pixels); with no browser it exits 0
and says why. Capture drives fm shot's own DevTools-pipe code against a stub browser; InABrowser uses a real one."""
import base64
import json
import os
import shutil
import stat
import subprocess
import sys
import unittest

from helpers import ForemanTestCase

import fmshot

SHOT =os.path.join(os.path.dirname(__file__), "..", "..", "mods", "foreman-ui", "tools", "shot.py")


@unittest.skipUnless(shutil.which("tmux"), "needs tmux")
class Harness(unittest.TestCase):
    def test_foreman_variables_stay_in_the_harness_session(self):
        env = dict(os.environ, FOREMAN_STATE="/tmp/fm-demo-state", FOREMAN_SESSION_ID="x",
                   FM_SHOT_SOCKET=f"fm-shot-test-{os.getpid()}")  # T-0744: two suites at once never share it
        p = subprocess.run([sys.executable, SHOT, "selftest"], env=env, capture_output=True, text=True, timeout=60)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_watch_refuses_outside_tmux_and_stops_on_time(self):
        # T-0143: 'add a hook to screenshot every few seconds'; run detached, it must never outlive --for
        env = {k: v for k, v in os.environ.items() if k not in ("TMUX", "TMUX_PANE")}
        p = subprocess.run([sys.executable, SHOT, "watch", os.devnull, "--every", "1", "--for", "0"], env=env,
                           capture_output=True, text=True, timeout=30)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("not inside tmux", p.stderr)


class OneOff(unittest.TestCase):
    def test_a_session_with_its_own_state_is_a_working_session(self):
        # T-1013: the demo recorder runs its session on a state of its own; marked one-off (T-0995) it was never driven
        # to close its task, and the recording timed out with nothing written
        import argparse
        import importlib.util
        spec = importlib.util.spec_from_file_location("shot_t1013", SHOT)
        shot = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(shot)
        seen = []
        shot.tmux = lambda *args, check=True: seen.append(args)
        a = argparse.Namespace(dir=".", cols=10, rows=5, model=None)
        saved = os.environ.pop("FOREMAN_STATE", None)
        try:
            shot.start(a, cmd="true")  # the user's own state: a one-off, never driven
            shared = " ".join(seen[-1])
            os.environ["FOREMAN_STATE"] = "/tmp/fm-demo-state"
            shot.start(a, cmd="true")
            own = " ".join(seen[-1])
        finally:
            os.environ.pop("FOREMAN_STATE", None)
            if saved is not None:
                os.environ["FOREMAN_STATE"] = saved
        self.assertIn("FOREMAN_ONEOFF=1", shared)
        self.assertNotIn("FOREMAN_STATE=", shared)
        self.assertIn("FOREMAN_STATE=/tmp/fm-demo-state", own)
        self.assertNotIn("FOREMAN_ONEOFF", own)

    def test_the_harness_keeps_true_color(self):
        # T-1209: Claude Code drops to 256 colours whenever TMUX is set unless CLAUDE_CODE_TMUX_TRUECOLOR is; the demo
        # was recorded with every colour on the 256 palette, so the pane's tinted chart wells became neutral gray blocks
        import argparse
        import importlib.util
        spec = importlib.util.spec_from_file_location("shot_t1209", SHOT)
        shot = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(shot)
        seen = []
        shot.tmux = lambda *args, check=True: seen.append(args)
        shot.start(argparse.Namespace(dir=".", cols=10, rows=5, model=None), cmd="true")
        args = seen[-1]
        self.assertIn("CLAUDE_CODE_TMUX_TRUECOLOR=1", args)
        self.assertEqual(args[args.index("CLAUDE_CODE_TMUX_TRUECOLOR=1") - 1], "-e")



class Trust(unittest.TestCase):
    """T-1032: the harness stalled at Claude Code's folder-trust prompt on every new folder (each demo recording); it
    answers it itself, but only for a folder Foreman made (a temp or scratch folder, its own repo): trusting a cloned
    repo would let that repo's hooks run."""

    def load(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("shot_t1032", SHOT)
        shot = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(shot)
        return shot

    def test_it_answers_for_a_folder_foreman_made_and_never_for_others(self):
        import tempfile
        import types
        shot = self.load()
        sent, screens = [], []

        def tmux(*args, check=True):
            if args[0] == "capture-pane":
                return types.SimpleNamespace(stdout=screens.pop(0) if screens else "❯ ", returncode=0)
            sent.append(args)
            return types.SimpleNamespace(stdout="", returncode=0)
        shot.tmux = tmux
        from unittest import mock
        nap = mock.patch.object(shot.time, "sleep", lambda s: None)  # review: never the whole test process's sleep
        nap.start()
        self.addCleanup(nap.stop)
        dialog = "Quick safety check: Is this a project you created or one you trust?\n❯ No, exit\n  Yes, I trust this folder"
        with tempfile.TemporaryDirectory() as d:
            screens[:] = [dialog, "❯ "]
            self.assertTrue(shot.answer_trust(d, wait=2))
            self.assertTrue(any("Enter" in a for a in sent), sent)
        sent.clear()
        screens[:] = [dialog]
        self.assertFalse(shot.answer_trust("/srv/someone-elses-clone", wait=2))
        self.assertEqual(sent, [])
        screens[:] = ["❯ "]  # no dialog: nothing pressed
        with tempfile.TemporaryDirectory() as d:
            self.assertFalse(shot.answer_trust(d, wait=1))
        self.assertEqual(sent, [])
        with tempfile.TemporaryDirectory() as d:  # a repo cloned into /tmp with its own Claude Code config
            os.makedirs(os.path.join(d, ".claude"))
            screens[:] = [dialog]
            self.assertFalse(shot.answer_trust(d, wait=2))
        self.assertEqual(sent, [])

    def test_the_live_recorder_trusts_only_through_the_shared_check(self):
        # T-1034: demo/record_live.py pressed Down/Enter on the trust prompt for any folder, a cloned --repo included
        with open(os.path.join(os.path.dirname(SHOT), "..", "..", "..", "demo", "record_live.py"), encoding="utf-8") as f:
            src = f.read()
        self.assertIn("shot.answer_trust(", src)
        self.assertNotIn('"Down")', src)


LIB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lib")
# A stand-in for Chromium's --remote-debugging-pipe: NUL-separated JSON on fds 3 (in) and 4 (out). Each screenshot is
# an 8x8 white PNG with the next count from STUB_PAINT painted black (the first is the viewport shot); every call is
# logged to STUB_LOG.
STUB = f"""#!{sys.executable}
import base64, json, os, sys
sys.path.insert(0, {LIB!r})
import fmimg
log = open(os.environ["STUB_LOG"], "a")
log.write(json.dumps({{"argv": sys.argv[1:]}}) + "\\n")
paint = [int(x) for x in os.environ.get("STUB_PAINT", "0").split(",")]
shots, buf = 0, b""
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
            n = paint[min(shots, len(paint) - 1)]
            shots += 1
            px = bytearray(b"\\xff" * 256)
            for i in range(n):
                px[i * 4:i * 4 + 3] = b"\\0\\0\\0"
            res = {{"data": base64.b64encode(fmimg.encode(8, 8, bytes(px))).decode()}}
        send({{"id": msg["id"], "result": res}})
        if msg["method"] == "Page.navigate":
            send({{"method": "Page.loadEventFired", "sessionId": "s1", "params": {{}}}})
"""


class Capture(ForemanTestCase):
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

    def test_with_no_browser_it_exits_0_naming_why(self):
        empty = os.path.join(self.tmp, "empty")
        os.makedirs(empty)
        r = self.fm("shot", self.page, env={"FOREMAN_CHROME": "", "PATH": empty, "HOME": empty})
        self.assertEqual(r.returncode, 0)
        self.assertIn("no browser", r.stdout)
        self.assertIn("FOREMAN_CHROME", r.stdout)  # how to point it at one
        self.assertIn("installs nothing", r.stdout)
        self.assertFalse(os.path.exists(self.log))

    def test_a_stub_browser_lists_the_viewport_frames_and_poster(self):
        data = json.loads(self.shot(self.page, "--frames", "4", "--every", "20", "--json", paint="0,1,4,9,2").stdout)
        [page] = data["pages"]
        names = [os.path.basename(x) for x in page["shots"]]
        self.assertEqual(names, ["viewport.png", "frame-00.png", "frame-01.png", "frame-02.png", "frame-03.png",
                                 "poster.png"])
        self.assertTrue(all(x.startswith(self.home) for x in page["shots"]), "under the project's state dir")
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

    def test_targets_it_refuses(self):
        for bad in ("javascript:alert(1)", os.path.join(self.tmp, "missing.html"), "ftp://example.com/"):
            r = self.shot(bad, check=False)
            self.assertNotEqual(r.returncode, 0, bad)
        for bad in (["--frames", "999"], ["--every", "5"]):
            self.assertNotEqual(self.shot(self.page, *bad, check=False).returncode, 0, bad)

    def test_painted_counts_pixels_off_the_background(self):
        self.assertEqual(fmshot.painted(fmshot.fmimg.decode(base64.b64decode(_png(3)))), 3)
        self.assertEqual(fmshot.painted(fmshot.fmimg.decode(base64.b64decode(_png(0)))), 0)


def _png(n):
    import fmimg
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
