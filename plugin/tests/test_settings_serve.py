"""T-1659: fm settings serve: a loopback-only page from the settings schema, a one-time token on every request, the
Host header and a POST's Origin checked, writes only through fm settings' own setter (set_key)."""
import html
import http.client
import json
import os
import threading
import time
import unittest.mock as mock
import urllib.parse

from helpers import ForemanTestCase, read_text

import fmsettings
import fmsettingsserve


class Serve(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.uhome = os.path.join(self.tmp, "uhome")
        os.makedirs(os.path.join(self.uhome, ".claude"))
        self.toml = os.path.join(self.home, "tui.toml")
        self.patches = [mock.patch.dict(os.environ, {"HOME": self.uhome}),
                        mock.patch.object(fmsettings, "in_claude_code", return_value=False)]
        for x in self.patches:
            x.start()
        os.environ.pop("CLAUDE_CONFIG_DIR", None)
        self.server, self.token = fmsettingsserve.make()
        self.port = self.server.server_address[1]
        self.stop = threading.Event()
        self.thread = threading.Thread(target=fmsettingsserve.serve, args=(self.server, 30, self.stop), daemon=True)
        self.thread.start()

    def tearDown(self):
        self.stop.set()
        self.thread.join(5)
        for x in reversed(self.patches):
            x.stop()
        super().tearDown()

    def req(self, method="GET", path=None, body=None, headers=None, token=True):
        c = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        path = path or ("/?t=" + self.token if token else "/")
        h = {"Host": f"127.0.0.1:{self.port}", **(headers or {})}
        c.request(method, path, body=body, headers=h)
        r = c.getresponse()
        out = r.status, r.read().decode(), dict(r.getheaders())
        c.close()
        return out

    def post(self, fields, origin=None, **kw):
        body = urllib.parse.urlencode(fields)
        h = {"Content-Type": "application/x-www-form-urlencoded",
             "Origin": origin or f"http://127.0.0.1:{self.port}", **kw.pop("headers", {})}
        return self.req("POST", "/set?t=" + self.token, body, h, **kw)

    def test_binds_loopback_only_with_a_long_random_token(self):
        self.assertEqual(self.server.server_address[0], "127.0.0.1")
        self.assertGreaterEqual(len(self.token), 43, "32 bytes from secrets, url-safe")
        self.assertNotEqual(fmsettingsserve.make()[1], self.token)

    def test_the_page_lists_the_schema_escaped_with_strict_headers(self):
        status, body, h = self.req()
        self.assertEqual(status, 200)
        for e in fmsettings.schema():
            self.assertIn(html.escape(e["key"]), body)
        self.assertIn("default-src 'none'", h["Content-Security-Policy"])
        self.assertEqual(h["X-Frame-Options"], "DENY")
        self.assertEqual(h["Referrer-Policy"], "no-referrer")
        self.assertFalse([k for k in h if k.lower().startswith("access-control")], h)
        self.assertNotIn("<script", body)

    def test_schema_text_is_escaped(self):
        evil = [dict(fmsettings.schema()[0], help='<script>alert(1)</script>"', key="x<b>")]
        with mock.patch.object(fmsettings, "rows", return_value=[dict(evil[0], value="<i>", where="w")]):
            page = fmsettingsserve.page("tok", "nonce", "")
        self.assertNotIn("<script>", page)
        self.assertNotIn("x<b>", page)
        self.assertIn("&lt;script&gt;", page)

    def test_a_missing_or_wrong_token_is_refused(self):
        self.assertEqual(self.req(token=False)[0], 403)
        self.assertEqual(self.req(path="/?t=" + "x" * len(self.token))[0], 403)
        self.assertEqual(self.req(path="/?t=%C3%A9%FF")[0], 403)
        self.assertEqual(self.req(path=f"/?t={self.token}x")[0], 403)
        status, body, _ = self.req("POST", "/set", "key=border&value=double",
                                   {"Origin": f"http://127.0.0.1:{self.port}", "Content-Type":
                                    "application/x-www-form-urlencoded"})
        self.assertEqual(status, 403)
        self.assertFalse(os.path.exists(self.toml))

    def test_a_foreign_host_is_refused(self):  # DNS rebinding: evil.example resolving to 127.0.0.1
        self.assertEqual(self.req(headers={"Host": f"evil.example:{self.port}"})[0], 403)
        self.assertEqual(self.req(headers={"Host": "127.0.0.1"})[0], 403)
        self.assertEqual(self.req(headers={"Host": f"localhost:{self.port}"})[0], 200)

    def test_a_post_from_another_origin_is_refused(self):
        self.assertEqual(self.post({"key": "border", "value": "double"}, origin="http://evil.example")[0], 403)
        # no-referrer makes a browser send Origin: null; only Sec-Fetch-Site (which a page can't set) lets that in
        self.assertEqual(self.post({"key": "border", "value": "double"}, origin="null")[0], 403)
        self.assertEqual(self.post({"key": "border", "value": "double"}, origin="null",
                                   headers={"Sec-Fetch-Site": "cross-site"})[0], 403)
        self.assertFalse(os.path.exists(self.toml))
        self.assertEqual(self.post({"key": "border", "value": "double"}, origin="null",
                                   headers={"Sec-Fetch-Site": "same-origin"})[0], 200)

    def test_other_methods_and_an_oversize_body_are_refused(self):
        for m in ("PUT", "DELETE", "OPTIONS", "PATCH"):
            self.assertIn(self.req(m)[0], (405, 501), m)
        big = "key=border&value=" + "d" * (fmsettingsserve.BODY_MAX + 1)
        status, _, _ = self.req("POST", "/set?t=" + self.token, big,
                                {"Origin": f"http://127.0.0.1:{self.port}"})
        self.assertEqual(status, 413)
        self.assertFalse(os.path.exists(self.toml))

    def test_a_valid_change_lands_through_the_setter(self):
        real = fmsettings.set_key
        with mock.patch.object(fmsettings, "set_key", side_effect=real) as setter:
            status, body, _ = self.post({"key": "border", "value": "double", "surface": "app"})
        self.assertEqual(status, 200, body)
        setter.assert_called_once()
        self.assertEqual(setter.call_args[0][:3], ("border", "double", "app"))
        self.assertIn('border = "double"', read_text(self.toml))
        self.assertIn("border", body)

    def test_an_invalid_value_is_refused_with_the_setters_message(self):
        status, body, _ = self.post({"key": "border", "value": "nope", "surface": "app"})
        self.assertEqual(status, 422)
        _, refused = fmsettings.set_key("border", "nope", "app")
        self.assertTrue(refused)
        self.assertIn(html.escape(refused[0]), body)
        self.assertFalse(os.path.exists(self.toml) and "nope" in read_text(self.toml))
        status, body, _ = self.post({"key": "no.such", "value": "1"})
        self.assertEqual(status, 422)
        self.assertIn("no such setting", body)

    def test_it_stops_when_idle(self):
        server, _ = fmsettingsserve.make()
        t = threading.Thread(target=fmsettingsserve.serve, args=(server, 0.3), daemon=True)
        start = time.monotonic()
        t.start()
        t.join(5)
        self.assertFalse(t.is_alive())
        self.assertLess(time.monotonic() - start, 5)
        self.assertEqual(server.socket.fileno(), -1, "the socket closed")

    def test_the_command_prints_the_url_once_and_stops_on_sigterm(self):
        import signal
        import subprocess
        import sys
        from helpers import FM
        env = dict(os.environ, FOREMAN_HOME=self.home, CLAUDECODE="", CLAUDE_CODE_ENTRYPOINT="")
        proc = subprocess.Popen([sys.executable, FM, "settings", "serve"], cwd=self.repo, env=env, text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            first = proc.stdout.readline()
            url = urllib.parse.urlsplit(first[first.index("http://"):].split()[0])
            self.assertEqual(url.hostname, "127.0.0.1")
            token = urllib.parse.parse_qs(url.query)["t"][0]
            c = http.client.HTTPConnection("127.0.0.1", url.port, timeout=5)
            c.request("GET", f"/?t={token}", headers={"Host": url.netloc})
            self.assertEqual(c.getresponse().status, 200)
            c.close()
            proc.send_signal(signal.SIGTERM)
            out, err = proc.communicate(timeout=10)
        finally:
            proc.kill()
        self.assertEqual(proc.returncode, 0, err)
        self.assertNotIn(token, out + err, "the token printed once, never logged")

    def test_there_is_no_host_flag(self):
        p = self.fm("settings", "serve", "--host", "0.0.0.0", check=False)
        self.assertNotEqual(p.returncode, 0)
