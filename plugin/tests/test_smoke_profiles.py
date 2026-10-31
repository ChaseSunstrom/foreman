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
import struct
import threading
import time
import unittest

from helpers import ForemanTestCase, PLUGIN

import fmsmoke

BIN = os.path.join(PLUGIN, "bin")
SCRIPT = os.path.join(PLUGIN, "lib", "smoke_web.cjs")
PLAYBOOK = os.path.join(PLUGIN, "skills", "playbooks", "references", "ui", "visual-qa.md")
MATRIX = [f"home-{w}-{t}.png" for w in (360, 768, 1440) for t in ("light", "dark")] + ["home-360-reduce.png"]
CAP = 8000  # a frame's height cap (smoke_web.cjs's FRAME_MAX_H)

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
const page = {  // "tall": a page 50000 px tall, 400 px wide at 360, showing "null"
  addInitScript: rec("page.addInitScript"), evaluate: rec("page.evaluate", mode === "tall" ? [400, 50000, "null"] : []),
  screenshot: rec("page.screenshot", () => Buffer.from(mode === "still" ? "same" : String(n++))),
  waitForTimeout: rec("page.waitForTimeout"), clock: { setFixedTime: rec("page.clock.setFixedTime") },
  goto: rec("page.goto"),
};
const ctx = {
  setOffline: rec("ctx.setOffline"), route: rec("ctx.route"), newPage: rec("ctx.newPage", page), close: rec("ctx.close"),
  newCDPSession: rec("ctx.newCDPSession", () => ({ send: rec("cdp.send", {}) })),
};
const browser = { newContext: rec("browser.newContext", ctx) };
(async () => {
  let prof = null;
  if (["frames", "still", "tall"].includes(mode)) await s.frames(browser);
  else if (mode === "timeout") {
    s.outOfTime(s.PROFILES.slow3g, "desktop start");
    s.outOfTime(s.PROFILES.offline, "phone start");
    s.outOfTime({}, "desktop tab Telemetry");
  } else if (mode !== "keys") {
    prof = s.PROFILES[mode];
    if (prof.setup) await prof.setup(ctx, page);
    if (prof.loaded) await prof.loaded(ctx, page);
    if (prof.view) await prof.view(page, "desktop start");
    if (prof.end) prof.end();
  }
  const slugs = ["desktop tab 设置", "desktop tab 设备", "phone tab Ünïcødé", "desktop tab إعدادات", "desktop tab " + "长".repeat(80)];
  console.log(JSON.stringify({ calls, keys: Object.keys(s.PROFILES), sizes: s.SIZES, themes: s.THEMES, cap: s.FRAME_MAX_H,
                               slugs: slugs.map(s.slug), state: s.state }));
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
        # review: a finding, not a defect: a live page (polling, video, canvas) mustn't break an existing gate
        self.assertIn("still moving under reduced motion", json.dumps(res["state"]["frame_findings"]))
        self.assertEqual(res["state"]["defects"], [])
        self.assertNotIn("still moving", json.dumps(self.drive("still")["state"]["frame_findings"]))
        self.assertEqual(self.named(res, "page.clock.setFixedTime"), [], "the user's app runs at its own time")

    def test_a_frame_is_capped_in_height_and_its_findings_kept_apart(self):
        res = self.drive("tall")
        full = [c[0] for c in self.named(res, "page.screenshot") if c[0].get("fullPage")]
        self.assertEqual(len(full), 7)
        self.assertEqual(res["cap"], CAP)
        self.assertTrue(all(o["clip"]["height"] == CAP for o in full), full)
        self.assertEqual([o["clip"]["width"] for o in full], [400, 400, 768, 768, 1440, 1440, 400], "overflow shows")
        found = json.dumps(res["state"]["frame_findings"])
        self.assertIn("page wider than the screen (400 px > 360 px)", found)
        self.assertEqual(res["state"]["defects"], [])
        self.assertIn('"null"', " ".join(res["state"]["notes"]))

    def test_a_patient_profile_running_out_of_time_is_a_note(self):
        state = self.drive("timeout")["state"]
        notes = " ".join(state["notes"])
        self.assertIn("desktop start: ran out of time on slow3g", notes)
        self.assertIn("phone start: ran out of time on offline", notes)
        self.assertEqual([(d["where"], d["what"][:30]) for d in state["defects"]],
                         [("desktop tab Telemetry", "the page stopped responding (n")])

    def test_view_names_keep_their_letters(self):
        slugs = self.drive("keys")["slugs"]
        self.assertEqual(slugs[:4], ["desktop-tab-设置", "desktop-tab-设备", "phone-tab-Ünïcødé", "desktop-tab-إعدادات"])
        self.assertEqual(len(slugs[4]), 60, "capped in characters, never half a character")


class ProfilesFromFm(ForemanTestCase):
    def runner(self, defects=None, skipped=None, frame_findings=None, skip_after=None):
        """A stand-in for the browser: records its argv and whether its commit folder was locked, writes a frame and
        a view shot, prints the result (skipped from call skip_after + 1 on, when given)."""
        path = os.path.join(self.tmp, "runner.py")
        self.argv_log, self.lock_log = os.path.join(self.tmp, "argv.jsonl"), os.path.join(self.tmp, "lock.log")
        res = {"skipped": skipped} if skipped else {"views": ["desktop start"], "defects": defects or [],
                                                    "frame_findings": frame_findings or []}
        with open(path, "w") as f:
            f.write("import fcntl, json, os, sys\n"
                    f"open({self.argv_log!r}, 'a').write(json.dumps(sys.argv[1:]) + '\\n')\n"
                    "out = sys.argv[2]\n"
                    "fd = os.open(os.path.join(os.path.dirname(out), '.lock'), os.O_RDWR | os.O_CREAT)\n"
                    "try:\n"
                    "    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB); held = 'free'\n"
                    "except BlockingIOError:\n"
                    "    held = 'busy'\n"
                    f"open({self.lock_log!r}, 'a').write(held + '\\n')\n"
                    "os.makedirs(os.path.join(out, 'frames'), exist_ok=True)\n"
                    "open(os.path.join(out, 'frames', 'home-360-light.png'), 'w').write('png')\n"
                    "open(os.path.join(out, os.environ.get('SHOT', 'desktop-start') + '.png'), 'w').write('png')\n"
                    f"res = {res!r}\n"
                    f"if {skip_after!r} is not None and len(open({self.argv_log!r}).readlines()) > {skip_after!r}:\n"
                    "    res = {'skipped': 'no browser for this Playwright: gone'}\n"
                    "print(json.dumps(res))\n")
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
        self.assertEqual(r.returncode, 0, "a hostile profile's findings fail nothing unless strict\n" + r.stdout)
        self.assertEqual([a[-1] for a in self.argvs()], list(fmsmoke.PROFILES))
        self.assertIn("Profiles: " + " · ".join(f"{n} ✗ 1" for n in fmsmoke.PROFILES), r.stdout)
        self.assertEqual(self.fm("smoke", "--profile", "empty", "--strict", env=env, check=False).returncode, 1)
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

    def test_a_later_profile_skipped_still_shows_the_earlier_findings(self):
        env = self.runner([{"where": "phone start", "what": "text runs out of its box: li"}], skip_after=1)
        r = self.fm("smoke", "--profile", "torture", "--profile", "offline", env=env, check=False)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertLess(r.stdout.index("✗ phone start: text runs out of its box: li"),
                        r.stdout.index("skipped http://127.0.0.1:8199/: no browser for this Playwright: gone"))
        d = self.fm_json("smoke", "--profile", "torture", "--profile", "offline", env=env, check=False)
        self.assertEqual(d["skipped"][:30], "no browser for this Playwright")
        self.assertEqual(d["profiles"], [], "this run: the first call was skipped too")

    def test_a_failing_product_check_fails_even_without_a_browser(self):
        # review: the skip used to return before the cmd check's verdict counted
        self.fm("smoke", "set", "cmd", "false")
        r = self.fm("smoke", env={"PATH": BIN + os.pathsep + os.environ["PATH"], "FOREMAN_PLAYWRIGHT": ""},
                    check=False)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("✗ failed  cmd false", r.stdout)
        self.assertIn("skipped http://127.0.0.1:8199/: no Playwright", r.stdout)

    def test_frame_findings_are_notes_unless_strict(self):
        env = self.runner(frame_findings=[{"where": "frame 360 reduce", "what": "still moving under reduced motion"}])
        r = self.fm("smoke", env=env, check=False)
        self.assertEqual(r.returncode, 0, "a live page (polling, video, canvas) keeps its gate\n" + r.stdout)
        self.assertIn("· frame 360 reduce: still moving under reduced motion", r.stdout)
        self.assertIn("fm smoke set strict on", r.stdout)
        self.assertEqual(self.fm("smoke", "--strict", env=env, check=False).returncode, 1)
        self.fm("smoke", "set", "strict", "on")
        r = self.fm("smoke", env=env, check=False)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("✗ frame 360 reduce: still moving under reduced motion", r.stdout)
        self.assertEqual(self.fm("check", "list").stdout.count("fm smoke"), 1, "strict is no second gate")
        self.fm("smoke", "set", "strict", "off")
        self.assertEqual(self.fm("smoke", env=env, check=False).returncode, 0)
        ledger = os.path.join(self.fm_json("smoke", env=env)["shots"].split(os.sep + "smoke" + os.sep)[0],
                              "ledger.jsonl")
        with open(ledger) as f:
            counted = [json.loads(x)["data"].get("defects") for x in f if json.loads(x)["event"] == "smoke"]
        self.assertEqual(counted[-1], 0, "fm outcomes doesn't count a note against a closed task")
        self.assertEqual(self.fm("smoke", "set", "strict", "maybe", check=False).returncode, 1)

    def test_a_crawl_past_its_time_is_stopped_with_its_whole_group(self):
        stub, pids, term = (os.path.join(self.tmp, x) for x in ("slow.py", "pids", "term"))
        with open(stub, "w") as f:  # a crawl that never answers, with a child of its own (a browser's stand-in)
            f.write("import signal, subprocess, sys, time\n"
                    f"signal.signal(signal.SIGTERM, lambda *a: (open({term!r}, 'w').write('term'), sys.exit(0)))\n"
                    "child = subprocess.Popen(['sleep', '60'])\n"
                    f"open({pids!r}, 'w').write(str(child.pid))\n"
                    "time.sleep(60)\n")
        os.environ["FOREMAN_SMOKE_RUNNER"] = f"{sys.executable} {stub}"
        try:
            t0 = time.time()
            res = fmsmoke.crawl(None, "http://127.0.0.1:9/", os.path.join(self.tmp, "out"), timeout=2)
        finally:
            os.environ.pop("FOREMAN_SMOKE_RUNNER")
        self.assertLess(time.time() - t0, 15)  # wall clock: the crawl timeout=2 deadline
        self.assertIn("the crawl did not finish", res["defects"][0]["what"])
        self.assertTrue(os.path.exists(term), "SIGTERM first: node's exit then kills the browser's own group")
        with open(pids) as f:
            pid = int(f.read())

        def gone():
            try:
                with open(f"/proc/{pid}/stat") as f:
                    return f.read().rsplit(")", 1)[1].split()[0] == "Z"
            except OSError:
                return True
        for _ in range(50):
            if gone():
                break
            time.sleep(0.1)
        self.assertTrue(gone(), "no child outlives the crawl")

    def test_a_run_holds_its_commit_folder(self):
        self.fm("smoke", env=self.runner())
        self.fm("smoke", "--profile", "torture", env=self.runner())
        with open(self.lock_log) as f:
            self.assertEqual(f.read().split(), ["busy", "busy"], "a second fm smoke on the commit waits its turn")

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
        rev = lambda: os.path.basename(os.path.dirname(self.fm_json("smoke", env=self.runner())["shots"]))  # noqa: E731
        with open(os.path.join(self.repo, "README.md"), "a") as f:
            f.write("changed\n")
        dirty = rev()
        self.assertRegex(dirty, rf"^{self.head()}-dirty-[0-9a-f]{{8}}$", "a dirty run is named by its diff")
        self.assertEqual(rev(), dirty, "the same changes, the same folder")
        with open(os.path.join(self.repo, "README.md"), "a") as f:
            f.write("changed again\n")
        self.assertNotEqual(rev(), dirty, "other changes don't overwrite the frames a receipt names")
        self.assertTrue(os.path.isdir(os.path.join(os.path.dirname(runs), os.pardir, dirty)))

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
        with open(os.path.join(cls.dir, "tall.html"), "w") as f:
            f.write('<!doctype html><body style="margin:0"><div style="height:30000px;background:#357"></div></body>')
        cls.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=cls.dir))
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.base = f"http://127.0.0.1:{cls.server.server_address[1]}/"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        shutil.rmtree(cls.dir, ignore_errors=True)

    def crawl(self, profile="", page=""):
        out = os.path.join(self.dir, "shots", profile or "default" + page)
        res = fmsmoke.crawl(_browser_pw(), self.base + page, out, timeout=120, profile=profile)
        if res.get("skipped"):
            self.skipTest(res["skipped"])
        res["out"] = out
        return res

    def found(self, res):
        return "\n".join(f"{d['where']}: {d['what']}" for d in res["defects"] + res.get("frame_findings", [])) + "\n" + \
            "\n".join(res["notes"])

    def test_the_default_run_shoots_the_frame_matrix(self):
        res = self.crawl()
        self.assertEqual(sorted(os.listdir(os.path.join(res["out"], "frames"))), sorted(MATRIX))
        self.assertIn("still moving under reduced motion", self.found(res), "the spinner ignores reduced motion")
        self.assertNotIn("still moving", json.dumps(res["defects"]), "a finding, not a gate failure")
        self.assertIn("desktop-start.png", os.listdir(res["out"]))

    def test_a_tall_page_frame_is_capped(self):
        frames = os.path.join(self.crawl(page="tall.html")["out"], "frames")
        for name in ("tall-html-360-light.png", "tall-html-1440-dark.png", "tall-html-360-reduce.png"):
            with open(os.path.join(frames, name), "rb") as f:
                width, height = struct.unpack(">II", f.read(24)[16:24])
            self.assertEqual(height, CAP, name)
            self.assertIn(width, (360, 1440), name)

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
