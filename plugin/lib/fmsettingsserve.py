"""T-1659: fm settings serve: the settings as a page in the browser, generated from fm settings' schema, each change
posted back through fm settings' own setter (set_key: every check, the history and, inside Claude Code, the guard).

Bound to 127.0.0.1 on a random port, never another interface (there is no --host). A token of 32 random bytes, made
for this run, is required on every request (compared in constant time); the Host header must name 127.0.0.1 or
localhost with the port (DNS rebinding) and a POST must come from the page itself (Origin, or Sec-Fetch-Site where
the page's no-referrer policy makes a browser send Origin: null). A body over BODY_MAX bytes is refused unread. No
CORS headers; the CSP allows nothing but the page's own nonce'd style and its form posts. It stops on Ctrl-C or
SIGTERM, and after IDLE seconds without a request carrying the token. The URL (token in it) is printed once; nothing
is logged. Stdlib http.server only."""
import hmac
import html
import http.server
import secrets
import signal
import sys
import time
import urllib.parse

import fmsettings

BODY_MAX = 16_384  # bytes of a POST: one setting's key and value (a layout list is a few hundred)
IDLE = 1800  # seconds without a tokened request before the server stops
TIMEOUT = 10  # seconds a connection may take to send its request

STYLE = ("body{font:14px system-ui,sans-serif;margin:2em;max-width:60em;color:#222}"
         "h2{margin-top:1.5em}form{display:grid;grid-template-columns:14em 1fr 4em;gap:.5em;align-items:center;"
         "margin:.3em 0}input,select{font:inherit}small{grid-column:1/-1;color:#666;margin-top:-.3em}"
         ".msg{padding:.5em;border:1px solid #888;white-space:pre-wrap}.bad{border-color:#c33;color:#900}")


def _value(r):
    """The value as fm settings set takes it: a word as it is, anything else as the file writes it."""
    v = r["value"]
    return v if isinstance(v, str) else fmsettings._shown(v, r["surface"])


def _field(r):
    e = html.escape
    if r["type"] == "choice" and r["choices"]:
        opts = "".join(f'<option value="{e(str(c))}"{" selected" if c == r["value"] else ""}>{e(str(c))}</option>' for c in r["choices"])
        return f'<select name="value">{opts}</select>'
    return f'<input name="value" value="{e(_value(r))}">'


def page(token, nonce, msg, bad=False):
    """The page: every setting fm settings list shows, one form each; all schema text escaped (a plugin's help is
    outside text)."""
    e = html.escape
    problems = []
    got = fmsettings.rows(problems=problems)
    out = [f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Foreman settings</title>'
           f'<style nonce="{e(nonce)}">{STYLE}</style></head><body><h1>Foreman settings</h1>']
    if msg:
        out.append(f'<p class="msg{" bad" if bad else ""}">{e(msg)}</p>')
    out += [f'<p class="msg bad">{e(s)}: {e(x)}</p>' for s, x in problems]
    action = e(f"/set?t={urllib.parse.quote(token)}")
    group = None
    for r in got:
        if (r["surface"], r["group"]) != group:
            group = (r["surface"], r["group"])
            out.append(f"<h2>{e(r['surface'])}: {e(str(r['group']))}</h2>")
        out.append(f'<form method="post" action="{action}"><label>{e(r["key"])}</label>{_field(r)}'
                   f'<button>set</button><input type="hidden" name="key" value="{e(r["key"])}">'
                   f'<input type="hidden" name="surface" value="{e(r["surface"])}">'
                   f'<small>{e(str(r["help"]))} (default {e(fmsettings._shown(r["default"], r["surface"]))}; '
                   f'{e(str(r.get("effect") or ""))})</small></form>')
    return "".join(out + ["</body></html>"])


def apply(fields, p=None):
    """One posted change through fm settings' setter: (ok, the message fm settings set would print)."""
    key, value, surface = (fields.get(k, "") for k in ("key", "value", "surface"))
    if surface not in ("", "app", "plugin"):
        return False, f"surface {surface!r}: app or plugin"
    if not fmsettings.find(key, surface or None):
        return False, f"{key}: no such setting (fm settings list shows them)"
    try:
        done, refused = fmsettings.set_key(key, value, surface or None, p)
    except fmsettings.SettingError as x:
        return False, str(x)
    lines = [f"{s}: {key} = {fmsettings._shown(v, s)}" + "".join(f"\n  now skipped: {w}" for w in warn)
             for s, v, warn in done]
    return not refused, "\n".join(lines + refused)


class Handler(http.server.BaseHTTPRequestHandler):
    timeout = TIMEOUT  # a client that never finishes its request can't hold the (single-threaded) server

    def log_message(self, *a):  # the request line holds the token: nothing is logged
        pass

    def _send(self, status, body, nonce=""):
        data = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Content-Security-Policy", f"default-src 'none'; style-src 'nonce-{nonce}'; "
                         "form-action 'self'; base-uri 'none'; frame-ancestors 'none'" if nonce else "default-src 'none'")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Connection", "close")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(data)

    def _allowed(self):
        """The request's path when its Host and token are this server's; else None, a 403 sent."""
        port = self.server.server_address[1]
        hosts = (f"127.0.0.1:{port}", f"localhost:{port}")
        if (self.headers.get("Host") or "").lower() not in hosts:
            self._send(403, "refused: not this server's host")
            return None
        url = urllib.parse.urlsplit(self.path)
        given = urllib.parse.parse_qs(url.query).get("t", [""])[0].encode("utf-8")
        if not hmac.compare_digest(given, self.server.token.encode()):
            self._send(403, "refused: no token, or not this run's")
            return None
        self.server.last = time.monotonic()
        return url.path

    def _render(self, status, msg="", bad=False):
        nonce = secrets.token_urlsafe(16)
        self._send(status, page(self.server.token, nonce, msg, bad), nonce)

    def do_GET(self):
        path = self._allowed()
        if path is None:
            return
        if path not in ("/", "/set"):  # /set: the page reloaded after a change
            return self._send(404, "not found")
        self._render(200)

    def _same_origin(self):
        port = self.server.server_address[1]
        mine = (f"http://127.0.0.1:{port}", f"http://localhost:{port}")
        origin = self.headers.get("Origin")
        if origin and origin != "null":
            return origin.lower() in mine
        ref = urllib.parse.urlsplit(self.headers.get("Referer") or "")
        return f"{ref.scheme}://{ref.netloc}".lower() in mine or self.headers.get("Sec-Fetch-Site") == "same-origin"

    def do_POST(self):
        path = self._allowed()
        if path is None:
            return
        if not self._same_origin():
            return self._send(403, "refused: not posted from this page")
        if path != "/set":
            return self._send(404, "not found")
        size = self.headers.get("Content-Length") or ""
        if self.headers.get("Transfer-Encoding") or not size.isdigit():
            return self._send(411, "a Content-Length is required")
        if int(size) > BODY_MAX:
            return self._send(413, f"over {BODY_MAX} bytes")
        try:
            body = self.rfile.read(int(size)).decode("utf-8")
            pairs = urllib.parse.parse_qsl(body, keep_blank_values=True, strict_parsing=bool(body), max_num_fields=8)
        except ValueError:  # bad UTF-8, a malformed form or too many fields
            return self._send(400, "not a form this page posts")
        fields = dict(pairs)
        if len(fields) != len(pairs):
            return self._send(400, "a field given twice")
        try:
            ok, msg = apply(fields, self.server.project)
        except Exception as x:  # whatever the setter raised: said, nothing more (it writes nothing on a failure)
            return self._render(500, f"{type(x).__name__}: {x}", True)
        self._render(200 if ok else 422, msg, not ok)

    def _no(self):
        self._send(405, "method not allowed")

    do_PUT = do_DELETE = do_PATCH = do_OPTIONS = do_HEAD = do_TRACE = do_CONNECT = _no


def make(p=None):
    """A server bound to 127.0.0.1 on a random port, not yet serving: (server, token)."""
    server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
    server.token, server.project, server.last = secrets.token_urlsafe(32), p, time.monotonic()
    return server, server.token


def serve(server, idle=IDLE, stop=None):
    """Answer requests until `idle` seconds pass without a tokened one, or `stop` (an Event) is set; then close."""
    server.timeout = 0.5
    server.last = time.monotonic()
    try:
        while not (stop and stop.is_set()) and time.monotonic() - server.last < idle:
            server.handle_request()
    finally:
        server.server_close()


def cmd_serve(args):
    """fm settings serve: print the URL once, serve until Ctrl-C, SIGTERM or IDLE seconds idle."""
    import fmcli
    if args.key or args.value or args.surface:
        raise fmcli.UsageError("fm settings serve: takes no key, value or --surface (the page has every setting)")
    server, token = make(fmsettings._project(args))
    url = f"http://127.0.0.1:{server.server_address[1]}/?t={token}"
    print(f"Foreman settings: {url}\n(this terminal only; Ctrl-C stops it, so do {IDLE // 60} idle minutes)",
          flush=True)
    old = signal.signal(signal.SIGTERM, lambda *a: sys.exit(0))
    try:
        serve(server)
    except KeyboardInterrupt:
        pass
    finally:
        signal.signal(signal.SIGTERM, old)
    print("stopped", flush=True)
    return 0
