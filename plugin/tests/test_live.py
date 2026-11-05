"""T-2998: sampo watch --web: a read-only, loopback-only server (settingsserve's token, cookie, Host check and CSP) with one
snapshot at /api/state and the same as a Server-Sent Events stream at /api/stream. A collector that fails leaves its field
empty; the snapshot names jobs, loaded models with VRAM, the GPU and the last minute's flows from calls already logged."""
import http.client
import json
import os
import threading
import time
import unittest.mock as mock

from helpers import ForemanTestCase

from sampo import core as c
from sampo import live

FIELDS = {"at", "project", "focus", "queue", "closed_today", "lanes", "jobs", "models", "gpu", "flows", "events", "stats"}


class Snapshot(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("task", "new", "Show the live page", "--type", "FEATURE", "--tier", "S", "--ac", "it shows :: true",
                "--step", "build it", "--focus")
        self.p = c.find_project(self.repo)
        live._CACHE.clear()

    def test_every_field_of_the_contract_is_there_and_json(self):
        s = live.snapshot(self.p)
        self.assertEqual(set(s), FIELDS)
        json.dumps(s)
        self.assertEqual(s["project"]["slug"], self.p.slug)
        self.assertEqual(s["focus"]["step"], "0/1")
        self.assertEqual(s["focus"]["title"], "Show the live page")
        self.assertEqual([q["title"] for q in s["queue"]], ["Show the live page"])

    def test_a_failing_collector_leaves_its_field_empty_the_rest_stand(self):
        def boom(p):
            raise RuntimeError("down")
        with mock.patch.dict(live.COLLECTORS, {"gpu": boom, "models": boom, "jobs": boom, "flows": boom}):
            s = live.snapshot(self.p)
        self.assertEqual((s["gpu"], s["models"], s["jobs"], s["flows"]), (None, [], [], []))
        self.assertEqual(s["project"]["slug"], self.p.slug)

    def test_jobs_models_gpu_and_flows_from_fakes(self):
        procs = [(4242, "python3 plugin/bin/sampo moons funnel --stage kill"), (1, "bash")]
        ps = {"models": [{"name": "qwen3:14b", "size_vram": 9728 * 1048576, "size": 10000 * 1048576}]}
        smi = "NVIDIA RTX 4090, 11000, 24564, 37\n"
        with mock.patch.object(live, "_procs", return_value=procs), mock.patch.object(live, "_get_json", side_effect=[ps, None]), \
                mock.patch.object(live, "_smi", return_value=smi):
            c.log_event(self.p, "cards_grow", data={"calls": 3, "models": {"qwen3:14b": 3}})
            s = live.snapshot(self.p)
        self.assertEqual([(j["name"], j["kind"], j["pid"]) for j in s["jobs"]], [("moons funnel --stage kill", "funnel", 4242)])
        m = {x["name"]: x for x in s["models"]}["qwen3:14b"]
        self.assertEqual((m["family"], m["where"], m["loaded"], m["vram_mb"]), ("ollama", "gpu", True, 9728))
        self.assertEqual(s["gpu"], {"name": "NVIDIA RTX 4090", "used_mb": 11000, "total_mb": 24564, "util_pct": 37})
        self.assertEqual([(f["from"], f["to"], f["kind"]) for f in s["flows"]], [("card grow", "qwen3:14b", "write")])
        self.assertIn("cards_grow", [e["kind"] for e in s["events"]])

    def test_flows_older_than_a_minute_are_out_and_event_text_is_redacted(self):
        old = c.log_event(self.p, "cards_grow", data={"models": {"haiku": 1}})
        with mock.patch.object(c, "now", return_value="2026-01-01T00:00:00Z"):
            c.log_event(self.p, "cards_grow", data={"models": {"old-one": 1}, "note": "sk-ant-api03-" + "a" * 40})
        s = live.snapshot(self.p)
        self.assertEqual([f["to"] for f in s["flows"]], ["haiku"])
        self.assertNotIn("a" * 40, json.dumps(s))
        self.assertTrue(old)

    def test_logged_model_calls_become_lanterns_and_flows(self):  # T-3014 live: Jarvis and Smith never showed
        from sampo import models
        with mock.patch.object(models.sys, "argv", ["sampo", "exam", "run", "s5-019", "--model", "jarvis"]):
            models.note_call({"name": "jarvis", "model": "qwen3.8-27b", "base_url": "https://jarvis.example/llm/v1"})
        with mock.patch.object(models.sys, "argv", ["sampo", "playbooks", "small", "grow"]):
            models.note_call({"name": "gpu-qwen4", "model": "qwen3.5:4b", "base_url": "http://127.0.0.1:11434/v1"})
        with mock.patch.object(live, "_get_json", return_value=None):
            s = live.snapshot(self.p)
        self.assertEqual(sorted((f["from"], f["to"], f["kind"]) for f in s["flows"]),
                         [("exam run", "jarvis", "act"), ("playbooks small grow", "qwen3.5:4b", "write")])
        m = {x["name"]: x for x in s["models"]}
        self.assertEqual((m["jarvis"]["where"], m["jarvis"]["calls_5m"]), ("remote", 1))

    def test_a_called_but_unloaded_local_model_hangs_on_the_gantry(self):  # T-3017
        from sampo import models
        models.note_call({"name": "gpu-gemma", "model": "gemma4-12b-32k", "base_url": "http://127.0.0.1:11434/v1"})
        models.note_call({"name": "jarvis", "model": "qwen3.8-27b", "base_url": "https://jarvis.example/v1"})
        with open(os.path.join(c.state_dir(), models.CALLS), "a") as f:  # an old row, no where
            f.write(json.dumps({"ts": c.now(), "to": "old-model", "from": "sampo"}) + "\n")
        with mock.patch.object(live, "_get_json", return_value=None):
            m = {x["name"]: x["where"] for x in live.snapshot(self.p)["models"]}
        self.assertEqual((m["gemma4-12b-32k"], m["jarvis"], m["old-model"]), ("gpu", "remote", "remote"))

    def test_a_ledger_row_seen_first_does_not_hide_a_local_calls_row(self):  # T-3017
        from sampo import models
        models.note_call({"name": "gpu-gemma", "model": "gemma4-12b-32k", "base_url": "http://127.0.0.1:11434/v1"})
        with mock.patch.object(c, "now", return_value=c.iso(time.time() + 60)):  # newer, so it sorts first
            c.log_event(self.p, "cards_grow", data={"models": {"gemma4-12b-32k": 1}})
        with mock.patch.object(live, "_get_json", return_value=None):
            m = {x["name"]: x["where"] for x in live.snapshot(self.p)["models"]}
        self.assertEqual(m["gemma4-12b-32k"], "gpu")

    def test_a_child_under_a_temp_home_logs_to_the_inherited_file(self):  # T-3014: exam Smith runs
        from sampo import models
        path = os.path.join(self.tmp, "real-calls.jsonl")
        with mock.patch.dict(os.environ, {"SAMPO_CALLS": path}):
            models.note_call({"name": "jarvis", "model": "qwen3.8-27b", "base_url": "https://jarvis.example/v1"})
        with open(path) as f:
            self.assertEqual(json.loads(f.read())["to"], "jarvis")
        self.assertFalse(os.path.exists(os.path.join(c.state_dir(), models.CALLS)))

    def test_complete_and_embed_log_their_calls_even_when_the_call_fails(self):  # T-3014 review
        from sampo import models
        prof = {"name": "gpu-x", "kind": "openai", "base_url": "http://127.0.0.1:11434/v1", "model": "m:1", "key_env": None}
        with mock.patch.object(models, "_post", side_effect=models.ModelError("down")):
            for call in (lambda: models.complete(prof, [{"role": "user", "content": "hi"}]),
                         lambda: models.embed(prof, ["a"])):
                with self.assertRaises(models.ModelError):
                    call()
        with open(os.path.join(c.state_dir(), models.CALLS)) as f:
            rows = [json.loads(x) for x in f]
        self.assertEqual([(r["to"], r.get("kind")) for r in rows], [("m:1", None), ("m:1", "embed")])
        with mock.patch.object(live, "_get_json", return_value=None):
            self.assertIn("embed", [f["kind"] for f in live.snapshot(self.p)["flows"]])

    def test_the_cli_hands_its_call_log_to_children(self):  # T-3014 review: an exam's Smith under a temp home
        from sampo import cli
        with mock.patch.dict(os.environ), mock.patch.object(cli.sys, "argv", ["sampo", "--version"]):
            os.environ.pop("SAMPO_CALLS", None)
            with self.assertRaises(SystemExit):
                cli.main()
            self.assertEqual(os.environ.get("SAMPO_CALLS"), os.path.join(c.state_dir(), "calls.jsonl"))

    def test_the_call_log_rotates_past_its_cap(self):
        from sampo import models
        with mock.patch.object(models, "CALLS_CAP", 200):
            for _ in range(10):
                models.note_call({"name": "gpu-qwen4", "model": "qwen3.5:4b", "base_url": "http://127.0.0.1:11434/v1"})
        path = os.path.join(c.state_dir(), models.CALLS)
        self.assertLessEqual(os.path.getsize(path), 200 + 200)
        self.assertTrue(os.path.exists(path + ".1"))

    def test_events_read_in_words(self):  # T-3014 live: the ticker printed {"file": "/home/…", "tool": "Edit"}
        c.log_event(self.p, "touched", task="T-0001", data={"file": "/home/x/proj/plugin/tests/test_traces.py", "tool": "Edit"})
        c.log_event(self.p, "evidence", task="T-0001", data={"step": 3, "ac": None, "cmd": "python3 plugin/bin/sampo shot x"})
        text = {e["kind"]: e["text"] for e in live.snapshot(self.p)["events"]}
        self.assertEqual(text["touched"], "T-0001 Edit test_traces.py")
        self.assertEqual(text["evidence"], "T-0001 step 3 · python3 plugin/bin/sampo shot x")
        self.assertNotIn("{", text["touched"] + text["evidence"])

    def test_the_snapshot_is_cached_a_moment(self):
        with mock.patch.object(live, "_procs", return_value=[]) as g:
            live.snapshot(self.p)
            live.snapshot(self.p)
        self.assertEqual(g.call_count, 1)


class Serve(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("task", "new", "Serve it", "--type", "FEATURE", "--tier", "S", "--ac", "x :: true", "--step", "s", "--focus")
        live._CACHE.clear()
        self.p = c.find_project(self.repo)
        self.peer = mock.patch.object(live, "peer_uid", return_value=None)  # the real /proc says: this test's own uid
        self.peer_mock = self.peer.start()
        self.addCleanup(self.peer.stop)
        self.server, self.token = live.make(self.p)
        self.port = self.server.server_address[1]
        self.stop = threading.Event()
        self.server.stop = self.stop
        self.thread = threading.Thread(target=live.serve, args=(self.server, self.stop), daemon=True)
        self.thread.start()
        self.cookie = None

    def tearDown(self):
        self.stop.set()
        self.thread.join(5)
        super().tearDown()

    def req(self, path="/", cookie=True, headers=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        h = {"Host": f"127.0.0.1:{self.port}", **(headers or {})}
        if cookie and self.cookie:
            h["Cookie"] = self.cookie
        conn.request("GET", path, headers=h)
        r = conn.getresponse()
        out = r.status, r.read().decode(), dict(r.getheaders())
        conn.close()
        return out

    def login(self):
        st, _, h = self.req(f"/?t={self.token}", cookie=False)
        self.assertEqual(st, 303)
        self.cookie = h["Set-Cookie"].split(";")[0]

    def test_bound_to_loopback_only(self):
        self.assertEqual(self.server.server_address[0], "127.0.0.1")

    def test_no_cookie_bad_host_and_the_token_works_once(self):
        for path in ("/", "/api/state", "/api/stream"):
            self.assertEqual(self.req(path, cookie=False)[0], 403)
        self.assertEqual(self.req("/", cookie=False, headers={"Host": "evil.example"})[0], 403)
        self.login()
        self.assertEqual(self.req(f"/?t={self.token}", cookie=False)[0], 403)  # spent
        self.assertEqual(self.req("/", headers={"Host": "evil.example"})[0], 403)  # a good cookie, a rebound host

    def test_state_is_json_with_the_contract_fields_and_a_csp(self):
        self.login()
        st, body, h = self.req("/api/state")
        self.assertEqual(st, 200)
        self.assertIn("application/json", h["Content-Type"])
        self.assertEqual(set(json.loads(body)), FIELDS)
        self.assertEqual(self.req("/api/nope")[0], 404)
        st, page, h = self.req("/")
        self.assertEqual(st, 200)
        self.assertIn("default-src 'none'", h["Content-Security-Policy"])
        self.assertNotIn("unsafe", h["Content-Security-Policy"])

    def test_the_live_theme_setting_sets_the_look_the_page_is_sent_with(self):  # T-3055
        from sampo import smithtui
        self.login()
        for want, cfg in (("modern", {}), ("forge", {"live_theme": "forge"}), ("modern", {"live_theme": "modern"})):
            with mock.patch.object(smithtui, "load_config", return_value=(cfg, [])):
                page = self.req("/")[1]
            self.assertIn(f'data-theme="{want}"', page if isinstance(page, str) else page.decode())
        with mock.patch.object(smithtui, "load_config", side_effect=OSError("no")):
            self.assertIn('data-theme="modern"', (lambda p: p if isinstance(p, str) else p.decode())(self.req("/")[1]))

    def test_a_collector_that_raises_is_not_a_500(self):
        self.login()

        def boom(p):
            raise OSError("no")
        with mock.patch.dict(live.COLLECTORS, {"jobs": boom, "stats": boom}):
            st, body, _ = self.req("/api/state")
        self.assertEqual(st, 200)
        self.assertEqual(json.loads(body)["jobs"], [])

    def test_static_files_come_from_the_folder_and_nothing_outside_it(self):
        self.login()
        d = os.path.join(self.tmp, "web")
        os.makedirs(d)
        with open(os.path.join(d, "live.css"), "w") as f:
            f.write("body{}")
        with mock.patch.object(live, "WEB", d):
            st, body, h = self.req("/static/live.css")
            self.assertEqual((st, body, h["Content-Type"].split(";")[0]), (200, "body{}", "text/css"))
            self.assertEqual(self.req("/static/..%2Flive.css")[0], 404)
            self.assertEqual(self.req("/static/../../x")[0], 404)
            self.assertEqual(self.req("/static/missing.js")[0], 404)

    def test_fonts_are_served_as_bytes(self):  # T-3014 live: every font fell back, _static 404'd anything not text
        self.login()
        d = os.path.join(self.tmp, "web")
        os.makedirs(d)
        raw = b"wOF2\x00\x01\xff\xfe" * 8
        with open(os.path.join(d, "A-normal.woff2"), "wb") as f:
            f.write(raw)
        with mock.patch.object(live, "WEB", d):
            conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
            conn.request("GET", "/static/A-normal.woff2", headers={"Host": f"127.0.0.1:{self.port}", "Cookie": self.cookie})
            r = conn.getresponse()
            self.assertEqual((r.status, r.getheader("Content-Type"), r.read()), (200, "font/woff2", raw))
            conn.close()
            self.assertEqual(self.req("/static/..%2FA-normal.woff2")[0], 404)

    def test_a_restart_keeps_an_open_tabs_cookie(self):  # T-3021 live: each restart 403'd the user's tab
        self.login()
        again, _ = live.make(self.p)
        try:
            self.assertEqual(again.session, self.server.session)
        finally:
            again.server_close()
        self.assertEqual(os.stat(os.path.join(self.p.dir, "live.session")).st_mode & 0o777, 0o600)
        st, body, _ = self.req("/api/state", cookie=False)
        self.assertEqual(st, 403)
        self.assertIn("sampo watch --web --url", body)

    def test_the_stream_sends_state_events(self):
        self.login()
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        conn.request("GET", "/api/stream", headers={"Host": f"127.0.0.1:{self.port}", "Cookie": self.cookie})
        r = conn.getresponse()
        self.assertEqual((r.status, r.getheader("Content-Type")), (200, "text/event-stream"))
        self.assertEqual(r.readline().decode().strip(), "event: state")
        data = r.readline().decode()
        self.assertTrue(data.startswith("data: "))
        self.assertEqual(set(json.loads(data[6:])), FIELDS)
        conn.close()

    def test_the_servers_own_uid_gets_in_with_no_link_another_uid_does_not(self):  # T-3023
        self.peer_mock.return_value = os.getuid()
        self.assertEqual(self.req("/api/state", cookie=False)[0], 200)
        self.assertEqual(self.req("/api/state", cookie=False, headers={"Host": "evil.example"})[0], 403)  # Host still applies
        self.peer_mock.return_value = os.getuid() + 1
        self.assertEqual(self.req("/api/state", cookie=False)[0], 403)
        self.peer_mock.return_value = None  # not found: the cookie path
        self.assertEqual(self.req("/api/state", cookie=False)[0], 403)
        self.login()
        self.assertEqual(self.req("/api/state")[0], 200)

    def test_machine_lists_projects_and_sessions_a_sensitive_one_by_name_only(self):  # T-3023
        self.login()
        other = os.path.join(self.tmp, "secretrepo")
        os.makedirs(other)
        sp = c.init_project(other, sensitive=True)
        sess = [{"session_id": "abcdef1234567890", "project": sp.slug, "cwd": other, "model": "Opus", "context_pct": 41,
                 "ts": c.now()},
                {"session_id": "99887766aaaa", "project": self.p.slug, "cwd": self.repo, "model": "Sonnet", "context_pct": 7,
                 "ts": c.now()}]
        with mock.patch("sampo.bus.live", return_value=sess):
            st, body, _ = self.req("/api/machine")
        self.assertEqual(st, 200)
        m = json.loads(body)
        mine = {x["slug"]: x for x in m["projects"]}
        self.assertEqual(mine[sp.slug], {"slug": sp.slug, "name": "secretrepo", "sensitive": True})
        self.assertEqual((mine[self.p.slug]["queue"], mine[self.p.slug]["task"], mine[self.p.slug]["drive"]),
                         (1, "T-0001", True))
        self.assertTrue(mine[self.p.slug]["stage"])
        ses = {x["id"]: x for x in m["sessions"]}
        self.assertEqual(ses["abcdef12"], {"id": "abcdef12", "project": sp.slug, "task": None, "model": None,
                                           "context_pct": 41, "seen": sess[0]["ts"]})
        self.assertEqual((ses["99887766"]["model"], ses["99887766"]["task"]), ("Sonnet", "T-0001"))

    def test_the_project_param_picks_a_snapshot_unknown_is_404_none_is_the_busiest_session(self):  # T-3023
        self.login()
        other = os.path.join(self.tmp, "otherrepo")
        os.makedirs(other)
        op = c.init_project(other, sensitive=False)
        self.assertEqual(json.loads(self.req(f"/api/state?project={op.slug}")[1])["project"]["slug"], op.slug)
        self.assertEqual(json.loads(self.req(f"/api/state?project={self.p.slug}")[1])["project"]["slug"], self.p.slug)
        self.assertEqual(self.req("/api/state?project=nope")[0], 404)
        self.assertEqual(self.req("/api/stream?project=nope")[0], 404)
        with mock.patch("sampo.bus.live", return_value=[{"session_id": "s1", "project": op.slug}]):
            self.assertEqual(json.loads(self.req("/api/state")[1])["project"]["slug"], op.slug)
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        conn.request("GET", f"/api/stream?project={op.slug}", headers={"Host": f"127.0.0.1:{self.port}", "Cookie": self.cookie})
        r = conn.getresponse()
        r.readline()
        self.assertEqual(json.loads(r.readline().decode()[6:])["project"]["slug"], op.slug)
        conn.close()

    def test_a_sensitive_project_is_not_served_by_slug(self):  # T-3023
        self.login()
        other = os.path.join(self.tmp, "hush")
        os.makedirs(other)
        sp = c.init_project(other, sensitive=True)
        self.assertEqual(self.req(f"/api/state?project={sp.slug}")[0], 404)

    def test_no_slug_with_a_sensitive_newest_session_falls_back_to_the_servers_own(self):  # T-3024 review
        self.login()
        other = os.path.join(self.tmp, "hush2")
        os.makedirs(other)
        sp = c.init_project(other, sensitive=True)
        with mock.patch("sampo.bus.live", return_value=[{"session_id": "s1", "project": sp.slug}]):
            st, body, _ = self.req("/api/state")
        self.assertEqual(st, 200)
        self.assertEqual(json.loads(body)["project"]["slug"], self.p.slug)

    def test_a_spent_token_is_replaced_and_the_url_file_follows(self):
        self.login()
        deadline = time.monotonic() + 5
        while self.server.token is None and time.monotonic() < deadline:
            time.sleep(0.05)
        self.assertIsNotNone(self.server.token)  # a fresh one, so `sampo watch --web --url` always prints a URL that works
        self.assertNotEqual(self.server.token, self.token)


class PeerUid(ForemanTestCase):  # T-3023: /proc/net/tcp as a fake root
    HEAD = "  sl  local_address rem_address   st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode\n"

    def root(self, tcp="", tcp6=None):
        d = os.path.join(self.tmp, "proc")
        os.makedirs(os.path.join(d, "net"), exist_ok=True)
        for name, rows in (("tcp", tcp), ("tcp6", tcp6)):
            if rows is not None:
                with open(os.path.join(d, "net", name), "w") as f:
                    f.write(self.HEAD + rows)
        return d

    def row(self, la, lp, ra, rp, uid):
        return f"   0: {la}:{lp:04X} {ra}:{rp:04X} 01 00000000:00000000 00:00000000 00000000  {uid}        0 12345 1 0 20 4 30 10 -1\n"

    def test_ipv4_ipv6_and_mapped_rows_the_client_side_socket_gives_the_uid(self):
        v4 = self.row("0100007F", 40000, "0100007F", 8000, 1000) + self.row("0100007F", 8000, "0100007F", 40000, 0)
        self.assertEqual(live.peer_uid("127.0.0.1", 40000, 8000, self.root(v4)), 1000)  # not the server-side row (uid 0)
        self.assertEqual(live.peer_uid("127.0.0.1", 40001, 8000, self.root(v4, "")), None)
        m = self.row("0000000000000000FFFF00000100007F", 41000, "0000000000000000FFFF00000100007F", 8000, 1234)
        self.assertEqual(live.peer_uid("127.0.0.1", 41000, 8000, self.root("", m)), 1234)
        six = self.row("00000000000000000000000001000000", 42000, "00000000000000000000000001000000", 8000, 77)
        self.assertEqual(live.peer_uid("::1", 42000, 8000, self.root("", six), saddr="::1"), 77)

    def test_another_uid_is_reported_and_unparseable_or_missing_rows_are_none(self):
        other = self.row("0100007F", 40000, "0100007F", 8000, 4242)
        self.assertEqual(live.peer_uid("127.0.0.1", 40000, 8000, self.root(other)), 4242)
        junk = "garbage\n   0: zz:yy 1:2 01\n   1: 0100007F:9C40 0100007F:1F40 01 a b c d notauid 0 1\n"
        self.assertIsNone(live.peer_uid("127.0.0.1", 40000, 8000, self.root(junk)))
        self.assertIsNone(live.peer_uid("127.0.0.1", 40000, 8000, os.path.join(self.tmp, "nowhere")))
        foreign = self.row("0A00000A", 40000, "0A00000A", 8000, 5)  # not a loopback address
        self.assertIsNone(live.peer_uid("127.0.0.1", 40000, 8000, self.root(foreign)))

    def test_another_address_with_the_users_port_number_never_inherits_the_users_uid(self):  # T-3027 review: HIGH
        user = self.row("0100007F", 40000, "0100007F", 8000, 1000)
        attacker = self.row("0200007F", 40000, "0100007F", 8000, 4242)  # 127.0.0.2:40000 -> the server
        self.assertEqual(live.peer_uid("127.0.0.2", 40000, 8000, self.root(user + attacker)), None)
        self.assertEqual(live.peer_uid("127.0.0.1", 40000, 8000, self.root(user + attacker)), 1000)
        self.assertIsNone(live.peer_uid("127.0.0.1", 40000, 8000, self.root(user + user)), "two rows: ambiguous")
        to_other = self.row("0100007F", 40000, "0100007F", 9000, 1000)  # the user's socket to another server
        self.assertIsNone(live.peer_uid("127.0.0.1", 40000, 8000, self.root(to_other)))


class Url(ForemanTestCase):
    def test_url_reprints_what_the_server_wrote(self):
        self.fm("task", "new", "x", "--type", "FEATURE", "--tier", "S", "--ac", "x :: true", "--step", "s", "--focus")
        p = c.find_project(self.repo)
        self.assertNotEqual(self.fm("watch", "--web", "--url", check=False).returncode, 0)  # none running
        live.write_url(p, "http://127.0.0.1:1/?t=abc")
        out = self.fm("watch", "--web", "--url")
        self.assertEqual(out.stdout.strip(), "http://127.0.0.1:1/?t=abc")
        self.assertEqual(os.stat(os.path.join(p.dir, "live.url")).st_mode & 0o777, 0o600)


class Act(ForemanTestCase):  # T-3026: POST /api/act, with the same-uid peer the browser is: only the refusals stand between it and a verb
    def setUp(self):
        super().setUp()
        self.fm("task", "new", "Steer it", "--type", "FEATURE", "--tier", "S", "--ac", "x :: true", "--step", "s", "--focus")
        live._CACHE.clear()
        self.p = c.find_project(self.repo)
        peer = mock.patch.object(live, "peer_uid", return_value=os.getuid())
        peer.start()
        self.addCleanup(peer.stop)
        self.server, _ = live.make(self.p)
        self.port = self.server.server_address[1]
        self.stop = threading.Event()
        self.thread = threading.Thread(target=live.serve, args=(self.server, self.stop), daemon=True)
        self.thread.start()
        self.addCleanup(self.thread.join, 5)
        self.addCleanup(self.stop.set)
        self.nonce = self.page_nonce()
        self.origin = f"http://127.0.0.1:{self.port}"

    def call(self, method, path, body=None, headers=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        conn.request(method, path, body=body, headers={"Host": f"127.0.0.1:{self.port}", **(headers or {})})
        r = conn.getresponse()
        out = r.status, r.read().decode()
        conn.close()
        return out

    def page_nonce(self):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        conn.request("GET", "/", headers={"Host": f"127.0.0.1:{self.port}"})
        html = conn.getresponse().read().decode()
        conn.close()
        return html.split('<meta name="sampo-act" content="')[1].split('"')[0]  # the act token, in the page's HTML

    def act(self, body, **over):
        h = {"Content-Type": "application/json", "Origin": self.origin, "X-Sampo-Nonce": self.nonce, **over}
        h = {k: v for k, v in h.items() if v is not None}
        return self.call("POST", "/api/act", body if isinstance(body, str) else json.dumps(body), h)

    def rows(self):
        return c.ledger_events(self.p, ["live_act"])

    def test_each_action_runs_its_verb_and_is_logged(self):
        slug = self.p.slug
        cases = [({"action": "drive_on", "project": slug}, ["drive", "on", "-p", slug]),
                 ({"action": "drive_off", "project": slug}, ["drive", "off", "-p", slug]),
                 ({"action": "checkpoint", "project": slug}, ["checkpoint", "-p", slug]),
                 ({"action": "resume", "project": slug}, ["resume", "-p", slug]),
                 ({"action": "pause_now", "confirmed": True}, ["pause", "on", "--now"]),
                 ({"action": "pause_off"}, ["pause", "off"])]
        for body, argv in cases:
            with mock.patch.object(live, "_run", return_value=0) as run:
                st, out = self.act(body)
            self.assertEqual((st, json.loads(out)["exit"]), (200, 0), body)
            run.assert_called_once_with(argv, self.p)
        self.assertEqual([r["data"]["action"] for r in self.rows()], [b["action"] for b, _ in cases])
        self.assertEqual(self.rows()[0]["data"], {"action": "drive_on", "project": slug, "exit": 0})

    def test_a_real_drive_off_changes_the_project(self):
        with mock.patch.dict(os.environ, {"FOREMAN_HOME": self.home}):
            st, out = self.act({"action": "drive_off", "project": self.p.slug})
        self.assertEqual((st, json.loads(out)["exit"]), (200, 0), out)
        self.assertIs(c.read_meta(self.p).get("drive"), False)

    def test_a_failing_verb_is_reported_and_logged(self):
        with mock.patch.object(live, "_run", return_value=3):
            st, out = self.act({"action": "resume", "project": self.p.slug})
        self.assertEqual((st, json.loads(out)["exit"]), (200, 3))
        self.assertEqual(self.rows()[0]["data"]["exit"], 3)

    def test_pause_now_needs_confirmed_true(self):
        with mock.patch.object(live, "_run") as run:
            for body in ({"action": "pause_now"}, {"action": "pause_now", "confirmed": "yes"}, {"action": "pause_now", "confirmed": False}):
                self.assertEqual(self.act(body)[0], 400)
        run.assert_not_called()

    def test_a_note_goes_through_the_bus_and_the_ledger_keeps_only_its_length(self):
        live_ = [{"session_id": "abcdef0123456789", "project": self.p.slug}]
        with mock.patch("sampo.bus.live", return_value=live_), mock.patch("sampo.bus.send") as send:
            st, _ = self.act({"action": "note", "session": "abcdef01", "text": "hello there"})
        self.assertEqual(st, 200)
        send.assert_called_once_with("abcdef0123456789", "hello there", kind="note", sender="live")
        d = self.rows()[0]["data"]
        self.assertEqual((d["action"], d["len"], d["session"]), ("note", 11, "abcdef01"))
        self.assertNotIn("hello", json.dumps(self.rows()))

    def test_a_note_to_a_session_with_no_project_is_refused(self):
        with mock.patch("sampo.bus.live", return_value=[{"session_id": "abcdef0123456789"}]), mock.patch("sampo.bus.send") as send:
            self.assertEqual(self.act({"action": "note", "session": "abcdef01", "text": "x"})[0], 400)
        send.assert_not_called()

    def test_unknown_things_are_a_400_and_run_nothing(self):
        os.makedirs(os.path.join(self.tmp, "hush"))
        sp = c.init_project(os.path.join(self.tmp, "hush"), sensitive=True)
        bad = [{"action": "rm_rf"}, {"action": 5}, {}, [1], {"action": "drive_on"}, {"action": "drive_on", "project": "nope"},
               {"action": "drive_on", "project": sp.slug}, {"action": "note", "session": "zzz", "text": "x"},
               {"action": "note", "session": "abcdef01", "text": "x"},  # a sensitive project's session
               {"action": "note", "session": "abcdef01", "text": ""}, {"action": "note", "session": "abcdef01", "text": "x" * 2500}]
        with mock.patch.object(live, "_run") as run, mock.patch("sampo.bus.send") as send, \
                mock.patch("sampo.bus.live", return_value=[{"session_id": "abcdef0123456789", "project": sp.slug}]):
            for b in bad:
                self.assertIn(self.act(b)[0], (400, 404), b)
            self.assertEqual(self.act("{not json")[0], 400)
        run.assert_not_called()
        send.assert_not_called()
        self.assertEqual(self.rows(), [])

    def test_every_refusal_runs_nothing_even_from_the_servers_own_uid(self):
        ok = {"action": "drive_off", "project": self.p.slug}
        form = {"Content-Type": "application/x-www-form-urlencoded"}
        with mock.patch.object(live, "_run") as run:
            self.assertEqual(self.call("GET", "/api/act")[0], 405)
            self.assertEqual(self.call("PUT", "/api/act", json.dumps(ok), {"Content-Type": "application/json"})[0], 405)
            for over in (form, {"Content-Type": "text/plain"}, {"Content-Type": None},
                         {"Origin": None}, {"Origin": "http://evil.example"}, {"Origin": "null"},
                         {"Origin": f"http://127.0.0.1:{self.port + 1}"}, {"Origin": f"https://127.0.0.1:{self.port}"},
                         {"X-Sampo-Nonce": None}, {"X-Sampo-Nonce": "guess"}):
                self.assertEqual(self.act(ok, **over)[0], 403, over)
            self.assertEqual(self.act("action=drive_off&project=" + self.p.slug, **form)[0], 403)
        run.assert_not_called()
        self.assertEqual(self.rows(), [])
        with mock.patch.object(live, "_run", return_value=0):  # the same request, whole: accepted (the refusals are the only gate)
            self.assertEqual(self.act(ok, Origin=f"http://localhost:{self.port}")[0], 200)
            self.assertEqual(self.act(ok, **{"Content-Type": "application/json; charset=utf-8"})[0], 200)

    def test_page_loads_cannot_evict_the_token(self):  # a cross-site page can GET / as often as it likes
        with mock.patch.object(live, "_run", return_value=0):
            for _ in range(100):
                self.assertEqual(self.page_nonce(), self.nonce)
            self.assertEqual(self.act({"action": "pause_off"})[0], 200)

    def test_a_cross_site_fetch_is_refused_by_sec_fetch_site(self):
        with mock.patch.object(live, "_run", return_value=0) as run:
            for v in ("cross-site", "same-site", "none", ""):
                self.assertEqual(self.act({"action": "pause_off"}, **{"Sec-Fetch-Site": v})[0], 403, v)
            run.assert_not_called()
            self.assertEqual(self.act({"action": "pause_off"}, **{"Sec-Fetch-Site": "same-origin"})[0], 200)

    def test_deeply_nested_json_is_a_400(self):
        with mock.patch.object(live, "_run") as run:
            self.assertEqual(self.act("[" * 2000 + "]" * 2000)[0], 400)
        run.assert_not_called()

    def test_a_timeout_kills_the_whole_process_group(self):
        child = mock.Mock(pid=4242)
        child.wait.side_effect = [live.subprocess.TimeoutExpired("x", 1), 0]
        with mock.patch.object(live.subprocess, "Popen", return_value=child) as popen, mock.patch.object(live.os, "killpg") as kill:
            self.assertEqual(live._run(["resume", "-p", "x"], self.p), 124)
        self.assertTrue(popen.call_args.kwargs["start_new_session"])
        kill.assert_called_once_with(4242, live.signal.SIGKILL)
        self.assertEqual(child.wait.call_args_list[0].kwargs["timeout"], live.SLOW_ACT_TIMEOUT)

    def test_a_body_over_the_cap_is_refused(self):
        with mock.patch.object(live, "_run") as run:
            self.assertEqual(self.act(json.dumps({"action": "note", "text": "x" * 20000}))[0], 413)
        run.assert_not_called()
