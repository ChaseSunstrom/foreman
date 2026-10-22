"""T-1509: fm smoke's hostile profiles (torture content, emptied data, offline, slow 3G, colour-vision filters, a frozen
clock, sampled motion frames) and the visual-qa frame matrix (360/768/1440 × light/dark + reduced motion at 360), kept
under stable names a receipt can point at. Without a browser each is skipped with a reason, never installed."""
import functools
import http.server
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import unittest

from helpers import ForemanTestCase, PLUGIN

import fmsmoke

BIN = os.path.join(PLUGIN, "bin")
SCRIPT = os.path.join(PLUGIN, "lib", "smoke_web.cjs")
PLAYBOOK = os.path.join(PLUGIN, "skills", "playbooks", "references", "ui", "visual-qa.md")
MATRIX = [f"home-{w}-{t}.png" for w in (360, 768, 1440) for t in ("light", "dark")] + ["home-360-reduce.png"]

# Drives smoke_web.cjs's own hooks against a recording stand-in for Playwright: no browser needed to see what each
# profile does to the page.
HARNESS = r"""
const s = require(process.argv[2]);
const [mode, out] = process.argv.slice(3);
s.run.url = "http://127.0.0.1:9/"; s.run.out = out;
const calls = []; let n = 0;
const plain = x => typeof x === "function" ? "fn:" + x.toString() : x instanceof Date ? x.toISOString() : x;
const rec = (name, ret) => (...a) => {
  calls.push([name, ...a.map(plain)]);
  return Promise.resolve(typeof ret === "function" ? ret(...a) : ret);
};
const page = {
  addInitScript: rec("page.addInitScript"), evaluate: rec("page.evaluate", []), goto: rec("page.goto"),
  screenshot: rec("page.screenshot", () => Buffer.from(mode === "still" ? "same" : String(n++))),
  waitForTimeout: rec("page.waitForTimeout"), clock: { setFixedTime: rec("page.clock.setFixedTime") },
};
const ctx = {
  setOffline: rec("ctx.setOffline"), route: rec("ctx.route"), newPage: rec("ctx.newPage", page), close: rec("ctx.close"),
  newCDPSession: rec("ctx.newCDPSession", () => ({ send: rec("cdp.send", {}) })),
};
const browser = { newContext: rec("browser.newContext", ctx) };
(async () => {
  let prof = null;
  if (mode === "frames" || mode === "still") await s.frames(browser);
  else if (mode !== "keys") {
    prof = s.PROFILES[mode];
    if (prof.setup) await prof.setup(ctx, page);
    if (prof.loaded) await prof.loaded(ctx, page);
    if (prof.view) await prof.view(page, "desktop start");
    if (prof.end) prof.end();
  }
  console.log(JSON.stringify({ calls, keys: Object.keys(s.PROFILES), sizes: s.SIZES, themes: s.THEMES,
                               context: prof && prof.context, state: s.state }));
})().catch(e => { console.log(JSON.stringify({ error: e.stack })); });
"""


@unittest.skipUnless(shutil.which("node"), "no node here: smoke_web.cjs can't be loaded")
class ProfilesInThePageScript(unittest.TestCase):
    """Each profile, as the page script applies it, against a recording stand-in for Playwright."""

    @classmethod
    def setUpClass(cls):
        cls.dir = tempfile.mkdtemp()
        cls.harness = os.path.join(cls.dir, "harness.cjs")
        with open(cls.harness, "w") as f:
            f.write(HARNESS)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.dir, ignore_errors=True)

    def drive(self, mode):
        out = tempfile.mkdtemp(dir=self.dir)
        r = subprocess.run(["node", self.harness, SCRIPT, mode, out], capture_output=True, text=True, timeout=60)
        res = json.loads(r.stdout.strip().splitlines()[-1]) if r.stdout.strip() else {"error": r.stderr}
        self.assertNotIn("error", res, res.get("error"))
        res["out"] = out
        return res

    def named(self, res, name):
        return [c[1:] for c in res["calls"] if c[0] == name]

    def test_the_page_script_and_fm_know_the_same_profiles(self):
        self.assertEqual(self.drive("keys")["keys"], list(fmsmoke.PROFILES))
        self.assertGreaterEqual(set(fmsmoke.PROFILES), {"torture", "empty", "offline", "slow3g", "deuteranopia",
                                                        "protanopia", "tritanopia", "achromatopsia", "frozen",
                                                        "motion"})

    def test_torture_writes_long_words_rtl_and_huge_numbers_into_the_page(self):
        res = self.drive("torture")
        args = json.dumps(self.named(res, "page.evaluate"), ensure_ascii=False)
        self.assertRegex(args, r"[^\s\"]{60,}", "a word of 60+ characters with no break")
        self.assertRegex(args, r"[\u0590-\u08ff]", "a right-to-left run")
        self.assertRegex(args, r"\d{15,}", "a huge number")

    def test_empty_hollows_the_apps_own_json(self):
        res = self.drive("empty")
        self.assertEqual(len(self.named(res, "ctx.route")), 1, res["calls"])
        self.assertIn("nothing was emptied", " ".join(res["state"]["notes"]), "no JSON came: it says so")

    def test_offline_cuts_the_network_after_the_first_load(self):
        self.assertIn([True], self.named(self.drive("offline"), "ctx.setOffline"))

    def test_slow3g_throttles_the_network(self):
        sent = dict((c[0], c[1] if len(c) > 1 else None) for c in self.named(self.drive("slow3g"), "cdp.send"))
        net = sent.get("Network.emulateNetworkConditions")
        self.assertIsNotNone(net, sent)
        self.assertGreaterEqual(net["latency"], 2000)
        self.assertLessEqual(net["downloadThroughput"], 60000)
        self.assertFalse(net["offline"])

    def test_each_colour_vision_profile_filters_the_page_with_its_own_matrix(self):
        seen = {}
        for name in ("deuteranopia", "protanopia", "tritanopia", "achromatopsia"):
            init = self.named(self.drive(name), "page.addInitScript")
            self.assertEqual(len(init), 1, name)
            fn, arg = init[0][0], init[0][1]
            self.assertIn("feColorMatrix", fn, name)
            self.assertIn("filter", fn, name)
            values = [float(x) for x in str(arg).split()]
            self.assertEqual(len(values), 20, name)
            seen[name] = tuple(values)
        self.assertEqual(len(set(seen.values())), 4, "each deficiency its own matrix")
        a = seen["achromatopsia"]
        self.assertEqual(a[0:3], a[5:8], "no colour: every channel is the same mix")
        self.assertEqual(a[0:3], a[10:13])

    def test_frozen_fixes_the_clock_and_stops_animations(self):
        res = self.drive("frozen")
        self.assertEqual(self.named(res, "page.clock.setFixedTime"), [["2026-01-15T10:00:00.000Z"]])
        self.assertIn("animation-play-state", json.dumps(self.named(res, "page.addInitScript")))
        self.assertTrue(any("frozen" in n for n in res["state"]["notes"]), res["state"])  # the stand-in moves

    def test_motion_samples_frames_of_each_view(self):
        res = self.drive("motion")
        shots = [c[0]["path"] for c in self.named(res, "page.screenshot")]
        self.assertGreaterEqual(len(shots), 4, shots)
        self.assertEqual(len(set(shots)), len(shots), "one file per sample")
        self.assertTrue(all(os.path.dirname(s) == res["out"] and "motion" in s for s in shots), shots)
        self.assertTrue(any("moves" in n for n in res["state"]["notes"]), res["state"])

    def test_the_frame_matrix_matches_the_visual_qa_playbook(self):
        res = self.drive("frames")
        with open(PLAYBOOK, encoding="utf-8") as f:
            sizes = re.search(r"const SIZES = (\[\[.*?\]\]);", f.read()).group(1)
        self.assertEqual(res["sizes"], json.loads(sizes))
        self.assertEqual(res["themes"], ["light", "dark"])
        opened = [(c[0]["viewport"]["width"], c[0]["viewport"]["height"], c[0]["colorScheme"], c[0]["reducedMotion"])
                  for c in self.named(res, "browser.newContext")]
        self.assertEqual(opened, [(w, h, t, "no-preference") for w, h in json.loads(sizes) for t in ("light", "dark")]
                         + [(360, 800, "light", "reduce")])
        shots = [c[0]["path"] for c in self.named(res, "page.screenshot") if c[0].get("path")]
        self.assertEqual(shots, [os.path.join(res["out"], "frames", n) for n in MATRIX])
        self.assertIn("still moving under reduced motion", json.dumps(res["state"]["defects"]))
        self.assertNotIn("still moving", json.dumps(self.drive("still")["state"]["defects"]))


class ProfilesFromFm(ForemanTestCase):
    def runner(self, defects=None, skipped=None):
        """A stand-in for the browser: records its argv, writes a frame and a view shot, prints the result."""
        path = os.path.join(self.tmp, "runner.py")
        self.argv_log = os.path.join(self.tmp, "argv.jsonl")
        res = {"skipped": skipped} if skipped else {"views": ["desktop start"], "defects": defects or []}
        with open(path, "w") as f:
            f.write("import json, os, sys\n"
                    f"open({self.argv_log!r}, 'a').write(json.dumps(sys.argv[1:]) + '\\n')\n"
                    "out = sys.argv[2]\n"
                    "os.makedirs(os.path.join(out, 'frames'), exist_ok=True)\n"
                    "open(os.path.join(out, 'frames', 'home-360-light.png'), 'w').write('png')\n"
                    "open(os.path.join(out, os.environ.get('SHOT', 'desktop-start') + '.png'), 'w').write('png')\n"
                    f"print(json.dumps({res!r}))\n")
        return {"FOREMAN_SMOKE_RUNNER": f"{sys.executable} {path}", "PATH": BIN + os.pathsep + os.environ["PATH"]}

    def argvs(self):
        with open(self.argv_log) as f:
            return [json.loads(x) for x in f]

    def head(self):
        return subprocess.run(["git", "-C", self.repo, "rev-parse", "--short", "HEAD"], capture_output=True,
                              text=True).stdout.strip()

    def setUp(self):
        super().setUp()
        self.fm("init")
        self.fm("smoke", "set", "web", "http://127.0.0.1:8199/")

    def test_each_profile_flag_reaches_the_page_script(self):
        env = self.runner()
        for name in fmsmoke.PROFILES:
            r = self.fm("smoke", "run", "--profile", name, env=env, check=False)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn(f"--profile {name}", r.stdout)
        self.assertEqual([a[-1] for a in self.argvs()], list(fmsmoke.PROFILES))

    def test_all_runs_every_profile_and_sums_them_up(self):
        env = self.runner([{"where": "phone start", "what": "page wider than the screen (900 px > 390 px)"}])
        r = self.fm("smoke", "--profile", "all", env=env, check=False)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertEqual([a[-1] for a in self.argvs()], list(fmsmoke.PROFILES))
        self.assertIn("Profiles: " + " · ".join(f"{n} ✗ 1" for n in fmsmoke.PROFILES), r.stdout)
        ledger = os.path.join(self.fm_json("smoke", "--profile", "offline", env=env, check=False)["profiles"][0]
                              ["shots"].split(os.sep + "smoke" + os.sep)[0], "ledger.jsonl")
        with open(ledger) as f:
            events = [json.loads(x)["event"] for x in f]
        self.assertNotIn("smoke", events, "a hostile profile's findings aren't a regression in fm outcomes")
        self.assertIn("smoke_profile", events)

    def test_an_unknown_profile_is_refused_naming_the_known_ones(self):
        r = self.fm("smoke", "--profile", "nope", env=self.runner(), check=False)
        self.assertEqual(r.returncode, 2)
        self.assertIn("torture", r.stderr)

    def test_a_profile_without_a_browser_is_skipped_with_a_reason(self):
        no_pw = {"PATH": BIN + os.pathsep + os.environ["PATH"], "FOREMAN_PLAYWRIGHT": ""}
        r = self.fm("smoke", "--profile", "torture", env=no_pw, check=False)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("skipped", r.stdout)
        self.assertIn("no Playwright", r.stdout)
        r = self.fm("smoke", "--profile", "offline", "--profile", "motion", check=False,
                    env=self.runner(skipped="no usable browser: Executable doesn't exist at /x/chrome"))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("skipped http://127.0.0.1:8199/: no usable browser: Executable doesn't exist", r.stdout)
        self.assertEqual(len(self.argvs()), 1, "no browser for one profile is no browser for the next")

    def test_screenshots_keep_stable_names_per_commit(self):
        runs = None
        for shot in ("first-only", "desktop-start"):
            env = dict(self.runner(), SHOT=shot)
            d = self.fm_json("smoke", env=env)
            self.assertEqual(os.path.basename(d["shots"]), "default")
            self.assertEqual(os.path.basename(os.path.dirname(d["shots"])), self.head())
            self.assertEqual(d["frames"], os.path.join(d["shots"], "frames"))
            self.assertTrue(os.path.isfile(os.path.join(d["frames"], "home-360-light.png")))
            runs = runs or d["shots"]
            self.assertEqual(d["shots"], runs, "the same commit, the same folder")
        self.assertEqual(sorted(os.listdir(runs)), ["desktop-start.png", "frames"], "a re-run leaves no stale shot")
        self.assertIn(f"{self.head()}{os.sep}default", self.fm("smoke", env=self.runner()).stdout)
        p = self.fm_json("smoke", "--profile", "torture", env=self.runner())["profiles"][0]
        self.assertEqual(p["shots"], os.path.join(os.path.dirname(runs), "torture"))
        with open(os.path.join(self.repo, "README.md"), "a") as f:
            f.write("changed\n")
        self.assertEqual(os.path.basename(os.path.dirname(self.fm_json("smoke", env=self.runner())["shots"])),
                         self.head() + "-dirty")

    def test_old_commits_runs_are_pruned(self):
        smoke = os.path.dirname(os.path.dirname(self.fm_json("smoke", env=self.runner())["shots"]))
        for i in range(fmsmoke.KEEP + 2):
            os.makedirs(os.path.join(smoke, f"old{i}"))
            os.utime(os.path.join(smoke, f"old{i}"), (time.time() - 1000 + i, time.time() - 1000 + i))
        self.fm("smoke", env=self.runner())
        kept = sorted(os.listdir(smoke))
        self.assertEqual(len(kept), fmsmoke.KEEP, kept)
        self.assertIn(self.head(), kept)
        self.assertNotIn("old0", kept)


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def _browser_pw():
    return fmsmoke.playwright(os.environ.get("FOREMAN_SMOKE_ROOT") or os.getcwd())


PAGE = """<!doctype html><html><head><style>
.card { width: 220px; white-space: nowrap; border: 1px solid #888 }
@keyframes spin { to { transform: rotate(360deg) } }
.spin { width: 40px; height: 40px; background: red; animation: spin 1s linear infinite }
</style></head><body>
<div class="card" id="name">Ada Lovelace</div><div class="card">Balance: 42</div>
<p id="now"></p><div class="spin"></div><ul id="list"></ul>
<script>
document.getElementById("now").textContent = new Date().toISOString();
fetch("/items.json").then(r => r.json()).then(d => {
  document.getElementById("list").innerHTML = d.items.map(x => `<li>${x}</li>`).join("");
  if (!d.items.length) throw new Error("no items");
});
setInterval(() => fetch("/items.json").catch(e => { throw new Error("offline: " + e.message); }), 400);
</script></body></html>"""


@unittest.skipUnless(_browser_pw(), "no Playwright here (FOREMAN_PLAYWRIGHT or a node_modules/playwright)")
class ProfilesInABrowser(unittest.TestCase):
    """Each profile against a real page; a Playwright without its browser skips with the crawl's own reason."""

    @classmethod
    def setUpClass(cls):
        cls.dir = tempfile.mkdtemp()
        with open(os.path.join(cls.dir, "index.html"), "w") as f:
            f.write(PAGE)
        with open(os.path.join(cls.dir, "items.json"), "w") as f:
            json.dump({"items": ["one", "two"]}, f)
        cls.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=cls.dir))
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.base = f"http://127.0.0.1:{cls.server.server_address[1]}/"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        shutil.rmtree(cls.dir, ignore_errors=True)

    def crawl(self, profile=""):
        out = os.path.join(self.dir, "shots", profile or "default")
        res = fmsmoke.crawl(_browser_pw(), self.base, out, timeout=120, profile=profile)
        if res.get("skipped"):
            self.skipTest(res["skipped"])
        res["out"] = out
        return res

    def found(self, res):
        return "\n".join(f"{d['where']}: {d['what']}" for d in res["defects"]) + "\n" + "\n".join(res["notes"])

    def test_the_default_run_shoots_the_frame_matrix(self):
        res = self.crawl()
        self.assertEqual(sorted(os.listdir(os.path.join(res["out"], "frames"))), sorted(MATRIX))
        self.assertIn("still moving under reduced motion", self.found(res), "the spinner ignores reduced motion")
        self.assertIn("desktop-start.png", os.listdir(res["out"]))

    def test_each_profile_in_a_real_browser(self):
        want = {"torture": "text runs out of its box", "empty": "no items", "offline": "offline: ", "motion": "moves"}
        for name in fmsmoke.PROFILES:
            with self.subTest(profile=name):
                res = self.crawl(name)
                self.assertIn("desktop start", res["views"], self.found(res))
                self.assertIn("desktop-start.png", os.listdir(res["out"]), self.found(res))
                if name in want:
                    self.assertIn(want[name], self.found(res))
                if name == "frozen":  # the spinner stops
                    self.assertNotIn("still changes", self.found(res))
                if name == "motion":
                    self.assertIn("desktop-start-motion-4.png", os.listdir(res["out"]))


if __name__ == "__main__":
    unittest.main()
