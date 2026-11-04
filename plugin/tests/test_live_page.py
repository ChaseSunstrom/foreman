"""T-2999: the live page (plugin/web/live) under the server's strict CSP. Static checks on the page's three files, then
recorded snapshots (fixtures/live) played through a stand-in for `sampo live`: every panel filled, sparks that travel
from caller to model, reduced motion shown by highlights, a dropped stream shown as reconnecting, no console errors,
at 1920x1080 and 390 wide."""
import glob
import json
import os
import re
import secrets
import sys
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from helpers import PLUGIN, headless_chrome

WEB = os.path.join(PLUGIN, "web", "live")
FIXTURES = sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "live", "snap-*.json")))
PANELS = ("scene", "focus", "gpu", "jobs", "queue", "closes", "counters", "bench", "ticker")
KINDS = {"write", "judge", "embed", "train", "plan", "act", "review"}
TYPES = {".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8",
         ".woff2": "font/woff2", ".json": "application/json"}
FLAT = r"^[A-Za-z0-9_-][A-Za-z0-9._-]*$"  # the names `sampo live` serves under /static (T-2998's _static)


def text(name):
    with open(os.path.join(WEB, name), encoding="utf-8") as f:
        return f.read()


def snaps():
    out = []
    for path in FIXTURES:
        with open(path, encoding="utf-8") as f:
            out.append(json.load(f))
    return out


class Files(unittest.TestCase):
    """What the CSP and the offline promise need, read from the files themselves."""

    def test_fixtures_follow_the_schema_and_carry_flows(self):
        got = snaps()
        self.assertGreaterEqual(len(got), 3)
        keys = {"at", "project", "focus", "queue", "closed_today", "lanes", "jobs", "models", "gpu", "flows", "events",
                "stats"}
        self.assertTrue([s for s in got if s["flows"]], "some snapshot carries flows")
        last = got[-1]  # the server today: bench rows and job progress don't exist yet, so the last snapshot has none
        self.assertEqual(last["stats"]["bench"], [])
        self.assertEqual({j["progress"] for j in last["jobs"]}, {None})
        for s in got:
            self.assertEqual(set(s), keys)
            self.assertLessEqual({f["kind"] for f in s["flows"]}, KINDS)
            self.assertLessEqual({m["family"] for m in s["models"]}, {"claude", "ollama", "jeff", "jarvis", "embed"})
            self.assertLessEqual({j["kind"] for j in s["jobs"]}, {"funnel", "grow", "exam", "train", "bench", "check",
                                                                   "other"})
            self.assertLessEqual(len(s["queue"]), 12)
            self.assertLessEqual(len(s["events"]), 60)

    def test_every_tag_that_loads_code_or_style_carries_the_nonce(self):
        page = text("index.html")
        tags = re.findall(r"<(?:script|style)\b[^>]*>|<link\b[^>]*\bstylesheet\b[^>]*>", page, re.I)
        self.assertTrue(tags)
        for tag in tags:
            self.assertIn('nonce="__NONCE__"', tag, tag)
        for tag in re.findall(r"<script\b[^>]*>", page, re.I):
            self.assertRegex(tag, r'\bsrc="/static/[\w.-]+\.js"', "scripts load from /static, never inline")

    def test_no_inline_handlers_style_attributes_or_script_urls(self):
        page = text("index.html")
        self.assertNotRegex(page, r"(?i)\son[a-z]+\s*=", "an inline handler breaks under the CSP")
        self.assertNotRegex(page, r"(?i)\sstyle\s*=", "a style attribute breaks under the CSP")
        self.assertNotIn("javascript:", page.lower())

    def test_no_external_urls_anywhere(self):
        for name in ("index.html", "live.css", "live.js"):
            body = text(name)
            for pat in (r"(?i)\bhttps?://", r"(?i)url\(\s*['\"]?//", r"(?i)(?:src|href)\s*=\s*['\"]//", r"(?i)@import"):
                self.assertNotRegex(body, pat, f"{name}: everything works offline")

    def test_the_script_stays_inside_the_csp(self):
        js = text("live.js")
        for pat in (r"\beval\s*\(", r"\bnew\s+Function\b", r"\.innerHTML\b", r"\.outerHTML\b", r"insertAdjacentHTML",
                    r"document\.write", r"setAttribute\(\s*['\"]style", r"set(?:Timeout|Interval)\(\s*['\"`]"):
            self.assertNotRegex(js, pat)

    def test_every_panel_has_its_element(self):
        page = text("index.html")
        for panel in PANELS + ("link", "motion"):
            self.assertRegex(page, rf'\bid="{panel}"', panel)

    def test_scrolling_lists_take_the_keyboard(self):  # T-2999 review: keyboard users could not scroll long lists
        html = text("index.html")
        for i in ("jobs-list", "queue-list", "closes-list", "sessions-list", "projects-list"):
            self.assertRegex(html, rf'id="{i}" tabindex="0" aria-label="[^"]+"')

    def test_phone_controls_are_big_enough(self):  # T-3026 review: iOS zooms into a field under 16px
        css = text("live.css")
        phone = css[css.index("max-width:700px"):]
        self.assertRegex(phone, r"\.note-in\{[^}]*font-size:16px")
        self.assertRegex(phone, r"\.act\{[^}]*min-height:28px")

    def test_reduced_motion_is_honoured_by_the_style_and_the_script(self):
        self.assertIn("prefers-reduced-motion", text("live.css"))
        self.assertIn("prefers-reduced-motion", text("live.js"))

    def test_fonts_are_bundled_files(self):
        urls = re.findall(r"url\(\s*['\"]?([^'\")]+)", text("live.css"))
        self.assertTrue(urls, "the display face comes with the page")
        for u in urls:
            self.assertRegex(u, FLAT, f"{u}: /static serves flat names only")
            self.assertTrue(os.path.isfile(os.path.join(WEB, u)), u)


class Stand(BaseHTTPRequestHandler):
    """`sampo live` as the page meets it: / with a fresh nonce and a strict CSP, /static, /api/state (the first
    snapshot) and /api/stream (the rest, then a dropped connection; the second connection answers late)."""
    server_version, sys_version = "live-test", ""

    def log_message(self, *a):
        pass

    def send(self, code, body, kind, extra=()):
        self.send_response(code)
        self.send_header("Content-Type", kind)
        self.send_header("Cache-Control", "no-store")
        for k, v in extra:
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):  # T-3026: /api/act as the page meets it: record headers and body; "forbid" in a note is a 403
        srv = self.server
        raw = self.rfile.read(int(self.headers.get("Content-Length") or 0))
        try:
            body = json.loads(raw)
        except ValueError:
            body = None
        srv.posts.append({"path": self.path, "type": self.headers.get("Content-Type"), "nonce": self.headers.get("X-Sampo-Nonce"),
                          "body": body})
        if self.path != "/api/act" or not isinstance(body, dict):
            return self.send(404, b"", "text/plain")
        if body.get("action") == "resume":
            time.sleep(0.6)  # in flight long enough for a second press to be seen refused
        if body.get("text") == "forbid":
            return self.send(403, json.dumps({"ok": False, "error": "bad nonce"}).encode(), TYPES[".json"])
        self.send(200, json.dumps({"ok": True, "exit": 0, "action": body.get("action")}).encode(), TYPES[".json"])

    def do_GET(self):
        srv, path = self.server, self.path.split("?")[0]
        if path == "/":
            nonce = secrets.token_urlsafe(16)
            csp = (f"default-src 'none'; script-src 'self' 'nonce-{nonce}'; style-src 'self' 'nonce-{nonce}'; "
                   "img-src 'self' data:; font-src 'self'; connect-src 'self'; base-uri 'none'; form-action 'none'; "
                   "frame-ancestors 'none'")
            page = text("index.html").replace("__NONCE__", nonce).replace(
                "</head>", f'<meta name="sampo-act" content="{srv.token}">\n</head>').encode()
            return self.send(200, page, TYPES[".html"], [("Content-Security-Policy", csp)])
        if path.startswith("/static/"):
            name = path[len("/static/"):]
            full = os.path.join(WEB, name)
            if not re.match(FLAT, name) or os.path.splitext(name)[1] not in TYPES or not os.path.isfile(full):
                return self.send(404, b"", "text/plain")
            with open(full, "rb") as f:
                return self.send(200, f.read(), TYPES.get(os.path.splitext(full)[1], "application/octet-stream"))
        srv.log.append(self.path)
        slug = (parse_qs(urlparse(self.path).query).get("project") or [""])[0]
        if path == "/api/machine":
            return self.send(200, json.dumps(srv.machine).encode(), TYPES[".json"])
        if slug and slug != srv.snaps[0]["project"]["slug"] and (path in ("/api/state", "/api/stream")):
            if slug != srv.other["project"]["slug"]:
                return self.send(404, b"", "text/plain")
            if path == "/api/state":
                return self.send(200, json.dumps(srv.other).encode(), TYPES[".json"])
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.end_headers()
            try:
                for _ in range(30):
                    self.wfile.write(b"event: state\ndata: " + json.dumps(srv.other).encode() + b"\n\n")
                    self.wfile.flush()
                    if srv.stop.wait(0.7):
                        return
            except OSError:
                pass
            return
        if path == "/api/state":
            return self.send(200, json.dumps(srv.snaps[0]).encode(), TYPES[".json"])
        if path == "/api/stream":
            with srv.lock:
                srv.streams += 1
                nth = srv.streams
            if nth > 1:
                time.sleep(1.2)  # the page shows "reconnecting" meanwhile
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            try:
                self.wfile.write(b"retry: 300\n\n")
                rest = srv.snaps[1:] if nth == 1 else srv.snaps[-1:] * 30
                for s in rest:
                    if srv.stop.wait(0.7):
                        return
                    self.wfile.write(b"event: state\ndata: " + json.dumps(s).encode() + b"\n\n")
                    self.wfile.flush()
            except OSError:
                pass
            return  # HTTP/1.0: returning closes the stream
        self.send(404, b"", "text/plain")


def serve():
    srv = ThreadingHTTPServer(("127.0.0.1", 0), Stand)
    srv.daemon_threads = True
    srv.snaps, srv.streams, srv.lock, srv.stop = snaps(), 0, threading.Lock(), threading.Event()
    srv.log, srv.posts, srv.token = [], [], secrets.token_hex(16)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "live", "machine.json"), encoding="utf-8") as f:
        srv.machine = json.load(f)
    srv.other = json.loads(json.dumps(srv.snaps[-1]))  # another project: its own slug and task at the anvil
    srv.other["project"] = {"slug": "other-1b2c3d", "drive": False, "autonomy": "standard"}
    srv.other["focus"] = {"id": "T-9001", "title": "The other project's task", "step": "1/2", "stage": "building"}
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


# Before the page: watch data-link change over time (live -> reconnecting -> live) without trusting the page's word.
WATCH = """(() => { window.__links = [];
  new MutationObserver(() => { const v = document.documentElement && document.documentElement.getAttribute("data-link");
    if (v && window.__links[window.__links.length - 1] !== v) window.__links.push(v); })
  .observe(document, {attributes: true, subtree: true, attributeFilter: ["data-link"]}); })()"""

PROBE = """(() => { const $ = id => document.getElementById(id), n = (id, sel) => $(id) ? $(id).querySelectorAll(sel).length : -1;
  const c = $("scene"), r = c ? c.getBoundingClientRect() : {width: 0, height: 0};
  return {links: window.__links, motion: document.documentElement.getAttribute("data-motion"),
    filled: Object.fromEntries(%s.map(id => [id, $(id) ? $(id).textContent.trim().length : -1])),
    focus: $("focus") ? $("focus").textContent : "", gpu: $("gpu") ? $("gpu").textContent : "",
    counters: $("counters") ? $("counters").textContent : "",
    gpuModels: n("gpu", "[data-model]"), jobs: n("jobs", "li"), queue: n("queue", "li"), closes: n("closes", "li"),
    bench: n("bench", "tbody tr"), ticker: n("ticker", "li"),
    nodes: +(c && c.dataset.nodes || 0), sparks: +(c && c.dataset.sparks || 0), flown: +(c && c.dataset.flown || 0),
    lit: +(c && c.dataset.lit || 0), scene: [Math.round(r.width), Math.round(r.height)], canvas: c ? [c.width, c.height] : [0, 0],
    hash: location.hash, sessions: n("sessions-list", "li"), projects: n("projects-list", "li"),
    picks: n("rail", "button[data-project]"), rail: $("rail") ? $("rail").textContent : "",
    railhtml: $("rail") ? $("rail").innerHTML : "", project: $("project") ? $("project").textContent : "",
    wide: document.documentElement.scrollWidth}; })()""" % json.dumps(list(PANELS))


class Page(unittest.TestCase):
    """The page in a real Chromium; skipped where there is none."""

    def setUp(self):
        self.browser = headless_chrome()
        if not self.browser:
            self.skipTest("no headless Chromium (FOREMAN_CHROME, chrome-headless-shell or Playwright's download)")
        sys.path.insert(0, os.path.join(PLUGIN, "lib"))
        self.last = snaps()[-1]

    def watch(self, size, reduced, done, within=45, step=None, hash=""):
        """Load the page at size, poll PROBE until done(got) or `within` s; (got, errors). step(b, got), if given, runs
        on every poll (it clicks, reloads); got["reqs"] lists the requests the server saw.
        A green run returns in about 8 s; the long ceiling is for a loaded machine (the gates run 16 at a time)."""
        from sampo import shot
        srv, errs = serve(), []
        b = shot.Browser(self.browser, size, reduced=reduced)
        try:
            b.on["Runtime.exceptionThrown"] = lambda p: errs.append("exception: " + json.dumps(p.get("exceptionDetails"))[:400])
            b.on["Runtime.consoleAPICalled"] = lambda p: p.get("type") in ("error", "assert", "warning") and errs.append(
                "console: " + json.dumps(p.get("args"))[:400])
            b.on["Log.entryAdded"] = lambda p: p["entry"].get("level") in ("error", "warning") and errs.append(
                "log: " + p["entry"].get("text", "") + " " + p["entry"].get("url", ""))
            b.call("Runtime.enable", b.sid)
            b.call("Log.enable", b.sid)
            b.call("Page.addScriptToEvaluateOnNewDocument", b.sid, source=WATCH)
            shot.load(b, f"http://127.0.0.1:{srv.server_address[1]}/" + hash)
            deadline = time.monotonic() + within
            while True:
                got = b.call("Runtime.evaluate", b.sid, expression=PROBE, returnByValue=True)["result"].get("value") or {}
                got["reqs"] = list(srv.log)
                got["posts"], got["token"] = list(srv.posts), srv.token
                if step and not done(got):
                    step(b, got)
                if done(got) or time.monotonic() > deadline:
                    return got, errs
                b.wait("live-test.never", 0.3)  # events (console, log) are read meanwhile
        finally:
            b.close()
            srv.stop.set()
            srv.shutdown()
            srv.server_close()

    def filled(self, got, size):
        last, where = self.last, f"at {size[0]}x{size[1]}"
        for panel in PANELS:
            self.assertGreater(got["filled"].get(panel, -1), 0 if panel != "scene" else -1, f"{panel} {where}")
        self.assertIn(last["focus"]["id"], got["focus"])
        self.assertIn(last["gpu"]["name"], got["gpu"])
        self.assertEqual(got["gpuModels"], sum(1 for m in last["models"] if m["loaded"] and (m["vram_mb"] or 0) > 0
                                                and m["where"] == "gpu"), where)
        self.assertEqual(got["jobs"], len(last["jobs"]), where)
        self.assertEqual(got["queue"], len(last["queue"]), where)
        self.assertEqual(got["closes"], len(last["closed_today"]), where)
        self.assertEqual(got["bench"], len(last["stats"]["bench"]), where)
        self.assertEqual(got["ticker"], len(last["events"]), where)
        self.assertIn(f"{last['stats']['cards']['general']:,}", got["counters"])
        self.assertIn(f"{last['stats']['moons']['candidates']:,}", got["counters"])
        self.assertGreater(got["nodes"], 0, where)
        self.assertGreaterEqual(got["scene"][1], 300, f"the scene is the hero {where}")
        self.assertLessEqual(got["wide"], size[0], f"no sideways scroll {where}")

    @staticmethod
    def back(got):
        """The stream dropped and came back: by then the page holds the last snapshot (earlier ones share its queue)."""
        links = got.get("links") or [""]
        return "reconnecting" in links and links[-1] == "live"

    def test_sparks_travel_from_caller_to_model_at_desktop_and_phone(self):
        for size in ((1920, 1080), (390, 844)):
            got, errs = self.watch(size, False, lambda g: self.back(g) and g.get("flown", 0) > 0)
            self.assertEqual(errs, [], f"console at {size}")
            self.filled(got, size)
            self.assertEqual(got["motion"], "full")
            self.assertGreater(got["sparks"], 0, size)
            self.assertGreater(got["flown"], 0, f"a spark reached its model at {size}")
            links = got["links"]
            self.assertEqual(links[-1], "live", links)
            self.assertIn("reconnecting", links, "a dropped stream is shown")

    def test_the_rail_and_strip_show_the_machine_and_a_pick_switches_the_scene(self):
        pick = "document.querySelector('#projects-list button[data-project=\"other-1b2c3d\"]').click()"
        for size in ((1920, 1080), (390, 844)):
            ctx = {"stage": 0}

            def step(b, got):
                ev = lambda js: b.call("Runtime.evaluate", b.sid, expression=js, returnByValue=True)
                if ctx["stage"] == 0 and got.get("picks", 0) >= 3:  # the machine arrived: pick the other project
                    ev(pick)
                    ctx["stage"] = 1
                elif ctx["stage"] == 1 and "T-9001" in got.get("focus", "") and got.get("hash") == "#project=other-1b2c3d":
                    ctx["seen"] = dict(got)
                    b.call("Page.reload", b.sid)  # the pick survives a reload through the hash
                    ctx["stage"] = 2
                elif ctx["stage"] == 2 and "T-9001" in got.get("focus", "") and got.get("picks", 0) >= 3:
                    ctx["stage"] = 3
                    ev("history.back()")  # back goes to the default project: the hash is the one source of truth
            got, errs = self.watch(size, False, lambda g: ctx["stage"] == 3 and "T-2995" in g.get("focus", "")
                                   and g.get("hash", "x") == "", step=step, within=60)
            self.assertEqual(errs, [], f"console at {size}")
            self.assertEqual(ctx["stage"], 3, f"the pick, the reload and back all happened at {size}")
            seen = ctx["seen"]
            self.assertEqual((seen["sessions"], seen["projects"]), (3, 4), size)
            for word in (".config", "vault", "T-9001", "claude-opus-4-6", "41%", "verifying", "7"):
                self.assertIn(word, seen["rail"], word)
            for word in ("T-7777", "hush-model-9"):  # T-3024 review: a sensitive project's session shows its name only
                self.assertNotIn(word, seen["rail"], word)
                self.assertNotIn(word, seen["railhtml"], word)
            self.assertLessEqual(seen["wide"], size[0], f"no sideways scroll at {size}")
            self.assertLessEqual(got["wide"], size[0], f"no sideways scroll at {size}")
            reqs = got["reqs"]
            self.assertTrue([r for r in reqs if r.startswith("/api/state?project=other-1b2c3d")], reqs)
            self.assertTrue([r for r in reqs if r.startswith("/api/stream?project=other-1b2c3d")], reqs)
            self.assertTrue([r for r in reqs if r.startswith("/api/machine")], reqs)

    def test_an_unknown_project_in_the_hash_shows_unknown_not_old_data_and_stops_asking(self):  # T-3024 review
        ctx = {}

        def step(b, got):
            if "no project" in got.get("project", "") and "t" not in ctx:
                ctx["t"] = time.monotonic()
        got, errs = self.watch((1920, 1080), False, lambda g: "t" in ctx and time.monotonic() - ctx["t"] > 4,
                               step=step, hash="#project=nope-123456")
        self.assertEqual([e for e in errs if "404" not in e], [])
        self.assertIn("nope-123456", got["project"])
        self.assertIn("no project", got["project"])
        self.assertNotIn("T-2995", got["focus"])
        self.assertEqual((got["queue"], got["closes"], got["ticker"]), (0, 0, 0))
        streams = [r for r in got["reqs"] if r.startswith("/api/stream")]
        self.assertLessEqual(len(streams), 1, streams)  # the stream is closed after the 404, not retried

    def test_an_empty_hash_pins_the_project_and_a_reconnect_names_it(self):  # T-3024 review
        got, errs = self.watch((1920, 1080), False, self.back)
        self.assertEqual(errs, [])
        self.assertEqual(got["hash"], "")
        streams = [r for r in got["reqs"] if r.startswith("/api/stream")]
        self.assertEqual(streams[0], "/api/stream")
        self.assertTrue(all("project=" in r for r in streams[1:]) and len(streams) > 1, streams)

    def test_reduced_motion_lights_changes_and_sends_no_sparks(self):
        got, errs = self.watch((1920, 1080), True, lambda g: self.back(g) and g.get("lit", 0) > 0)
        self.assertEqual(errs, [])
        self.filled(got, (1920, 1080))
        self.assertEqual(got["motion"], "still")
        self.assertEqual(got["sparks"], 0)
        self.assertGreater(got["lit"], 0, "changes show as highlights")

    def test_the_controls_steer_through_api_act_by_mouse_and_keyboard(self):  # T-3026 part 2
        ctx = {"s": 0, "t": 0}
        FOREMAN, SESS = "foreman-4a056f", "e5f6a7b8"
        drive = f'#projects-list button[data-act^="drive_"][data-target="{FOREMAN}"]'
        cp = f'#projects-list button[data-act="checkpoint"][data-target="{FOREMAN}"]'
        note = f'#sessions-list button[data-act="note"][data-target="{SESS}"]'
        resume = f'#projects-list button[data-act="resume"][data-target="{FOREMAN}"]'

        def step(b, got):
            ev = lambda js: b.call("Runtime.evaluate", b.sid, expression=js, returnByValue=True)["result"].get("value")
            focus = lambda sel: ev(f"(document.querySelector({json.dumps(sel)}) || {{focus(){{}}}}).focus()")

            def key(k, code, vk, txt=""):
                for t in ("keyDown", "keyUp"):
                    b.call("Input.dispatchKeyEvent", b.sid, type=t, key=k, code=code, windowsVirtualKeyCode=vk,
                           **({"text": txt} if t == "keyDown" and txt else {}))
            enter = lambda: key("Enter", "Enter", 13, "\r")
            space = lambda: key(" ", "Space", 32, " ")
            status = lambda: ev("document.getElementById('act-status') ? document.getElementById('act-status').textContent : ''")
            posts, s = got["posts"], ctx["s"]
            if s == 0 and ev(f"!!document.querySelector({json.dumps(drive)}) && !!document.querySelector({json.dumps(note)})"):
                focus(f'#projects-list button.pick[data-project="{FOREMAN}"]')  # Tab from the plate's pick lands on a control
                key("Tab", "Tab", 9)
                ctx["tab"] = ev("(document.activeElement.dataset||{}).act || ''")
                ctx["nodrive"] = ev("document.querySelectorAll('#projects-list [data-target=\"broken-000000\"][data-act^=\"drive_\"]').length")
                ctx["fallback_acts"] = ev("document.querySelectorAll('#projects-list [data-target=\"broken-000000\"]').length")
                ctx["private"] = ev("document.querySelectorAll('.plate.private [data-act]').length")
                ctx["role"] = ev("document.getElementById('act-status').getAttribute('role')")
                ctx["live"] = ev("document.getElementById('act-status').getAttribute('aria-live')")
                ctx["pressed"] = ev(f"document.querySelector({json.dumps(drive)}).getAttribute('aria-pressed')")
                focus(drive); enter(); ctx["s"] = 1
            elif s == 1 and len(posts) >= 1:
                ctx["status1"] = status(); focus(cp); space(); ctx["s"] = 2
            elif s == 2 and len(posts) >= 2:  # a double press on resume starts one run: the button is disabled in flight
                ctx["dbl"] = ev(f"(() => {{ const r = document.querySelector({json.dumps(resume)}); r.click(); r.click(); "
                                "return r.disabled; })()")
                ctx["s"] = 21
            elif s == 21 and len(posts) >= 3 and ev(f"!document.querySelector({json.dumps(resume)}).disabled"):
                ctx["n_resume"] = len(posts)
                focus("#act-pause"); enter()  # the first press only arms it
                ctx["armed"] = ev("document.getElementById('act-pause').textContent")
                ctx["n_armed"] = len(posts); ctx["t"] = time.monotonic(); ctx["s"] = 3
            elif s == 3 and time.monotonic() - ctx["t"] > 4.8:
                ctx["disarmed"] = ev("document.getElementById('act-pause').textContent")
                ctx["n_disarmed"] = len(posts)
                focus("#act-pause"); enter(); enter()  # a double press (key repeat) arms but cannot confirm
                ctx["fast"] = ev("document.getElementById('act-pause').textContent")
                ctx["t"] = time.monotonic(); ctx["s"] = 31
            elif s == 31 and time.monotonic() - ctx["t"] > 0.9:
                ctx["n_fast"] = len(posts)
                focus("#act-pause"); enter(); ctx["s"] = 4  # after the gap the second press confirms
            elif s == 4 and len(posts) >= 4:
                ctx["status4"] = status(); focus("#act-pause-off"); space(); ctx["s"] = 5
            elif s == 5 and len(posts) >= 5:
                focus(note); enter()  # opens the field; Escape cancels it
                ctx["field"] = ev("!!document.querySelector('#sessions-list input')")
                key("Escape", "Escape", 27)
                ctx["gone"] = ev("!document.querySelector('#sessions-list input')")
                ctx["back"] = ev(f"document.activeElement === document.querySelector({json.dumps(note)})")
                focus(note); enter(); ctx["s"] = 6
            elif s == 6 and ev("!!document.querySelector('#sessions-list input')"):
                focus("#sessions-list input"); b.call("Input.insertText", b.sid, text="hello there"); enter(); ctx["s"] = 7
            elif s == 7 and len(posts) >= 6:
                focus(note); enter(); ctx["s"] = 8
            elif s == 8 and ev("!!document.querySelector('#sessions-list input')"):
                focus("#sessions-list input"); b.call("Input.insertText", b.sid, text="forbid"); enter(); ctx["s"] = 9
            elif s == 9 and "reload" in status().lower():
                ctx["status9"] = status()  # a refused note keeps its field and text
                ctx["kept"] = ev("(document.querySelector('#sessions-list input') || {}).value")
                ctx["s"] = 10

        got, errs = self.watch((1920, 1080), False, lambda g: ctx["s"] == 10, step=step, within=70)
        self.assertEqual([e for e in errs if "403" not in e], [])  # the forced 403 is the browser's own log line
        self.assertEqual(ctx["s"], 10, ctx)
        self.assertEqual(ctx["tab"], "drive_off", "Tab from a plate's pick reaches its first control")  # foreman drive is on
        self.assertEqual((ctx["role"], ctx["live"], ctx["pressed"]), ("status", "polite", "true"))
        self.assertEqual(ctx["private"], 0, "a sensitive project's plate has no controls")
        posts = got["posts"]
        self.assertEqual(len(posts), 7, posts)
        self.assertEqual((ctx["nodrive"], ctx["fallback_acts"]), (0, 2), "a row without a drive state has no drive toggle")
        self.assertTrue(ctx["dbl"], "the pressed button is disabled in flight")
        self.assertEqual(ctx["n_resume"], 3, "two presses on resume ran one")
        self.assertIn("press again", ctx["fast"])
        self.assertEqual(ctx["n_fast"], 3, "a double press cannot confirm pause now")
        self.assertEqual(ctx["kept"], "forbid", "a refused note keeps its text")
        self.assertEqual(ctx["status9"].lower().count("reload"), 1, ctx["status9"])
        for p in posts:
            self.assertEqual((p["path"], p["type"], p["nonce"]), ("/api/act", "application/json", got["token"]))
        self.assertEqual([p["body"] for p in posts], [
            {"action": "drive_off", "project": FOREMAN}, {"action": "checkpoint", "project": FOREMAN},
            {"action": "resume", "project": FOREMAN}, {"action": "pause_now", "confirmed": True}, {"action": "pause_off"},
            {"action": "note", "session": SESS, "text": "hello there"}, {"action": "note", "session": SESS, "text": "forbid"}])
        self.assertIn("drive", ctx["status1"].lower())
        self.assertEqual(ctx["n_armed"], 3, "one press of pause now sends nothing")
        self.assertIn("press again", ctx["armed"])
        self.assertEqual((ctx["disarmed"], ctx["n_disarmed"]), ("pause now", 3), "it disarms by itself")
        self.assertIn("pause", ctx["status4"].lower())
        self.assertEqual((ctx["field"], ctx["gone"], ctx["back"]), (True, True, True), "Esc cancels the note field")
        self.assertIn("reload", ctx["status9"].lower())
        self.assertIn("bad nonce", ctx["status9"])
        self.assertEqual(got["hash"], "", "a control press never switches the project")

    def test_the_controls_fit_a_phone(self):
        got, errs = self.watch((390, 844), False, lambda g: g.get("picks", 0) >= 3)
        self.assertEqual(errs, [])
        self.assertLessEqual(got["wide"], 390)


if __name__ == "__main__":
    unittest.main()
