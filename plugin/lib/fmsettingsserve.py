"""T-1659: fm settings serve: the settings as a page in the browser, generated from fm settings' schema, each change
posted back through fm settings' own setter (set_key: every check, the history and, inside Claude Code, the guard).

Bound to 127.0.0.1 on a random port, never another interface (there is no --host). The printed URL carries a token of
32 random bytes that works once: the first visit swaps it for a cookie (HttpOnly, SameSite=Strict, another 32 random
bytes, so a URL left in history or a screenshot can't be replayed) and a 303 to the token-free page; every request
after needs that cookie (compared in constant time). The Host header must name 127.0.0.1 or localhost with the port
(DNS rebinding) and a POST's Origin must be the page's own (Referrer-Policy same-origin, so a browser sends it). A body
over BODY_MAX bytes is refused unread. No CORS headers; the CSP allows nothing but the page's nonce'd style and its
form posts. Each connection gets its own daemon thread, so a slow client holds only its own. It stops on Ctrl-C or
SIGTERM, and after IDLE seconds without an authenticated request. The URL is printed once; nothing is logged. Stdlib
http.server only."""
import hmac
import html
import http.cookies
import http.server
import secrets
import signal
import sys
import threading
import time
import urllib.parse

import fmsettings

BODY_MAX = 16_384  # bytes of a POST: one setting's key and value (a layout list is a few hundred)
IDLE = 1800  # seconds without an authenticated request before the server stops
TIMEOUT = 10  # seconds each read or write on a connection may wait

STYLE = ("body{font:14px system-ui,sans-serif;margin:2em;max-width:60em;color:#222}"
         "h2{margin-top:1.5em}form{display:grid;grid-template-columns:14em 1fr 4em;gap:.5em;align-items:center;"
         "margin:.3em 0}input,select{font:inherit}small{grid-column:1/-1;color:#666;margin-top:-.3em}"
         ".msg{padding:.5em;border:1px solid #888;white-space:pre-wrap}.bad{border-color:#c33;color:#900}")


def cookie_name(port):
    return f"fm_settings_{port}"  # cookies aren't kept per port: two runs at once don't clobber each other's


def _value(r):
    """The value as fm settings set takes it: a word as it is, anything else as the file writes it."""
    v = r["value"]
    return v if isinstance(v, str) else fmsettings._shown(v, r["surface"])


def _field(r):
    e = html.escape
    if r["type"] == "choice" and r["choices"]:
        opts = "".join(f'<option value="{e(str(c))}"{" selected" if c == r["value"] else ""}>{e(str(c))}</option>'
                       for c in r["choices"])
        return f'<select name="value">{opts}</select>'
    return f'<input name="value" value="{e(_value(r))}">'


def page(nonce, msg, bad=False):
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
    group = None
    for r in got:
        if (r["surface"], r["group"]) != group:
            group = (r["surface"], r["group"])
            out.append(f"<h2>{e(r['surface'])}: {e(str(r['group']))}</h2>")
        out.append(f'<form method="post" action="/set"><label>{e(r["key"])}</label>{_field(r)}'
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
    lines = []
    for s, v, warn in done:
        lines.append(f"{s}: {key} = {fmsettings._shown(v, s)}")
        lines += [f"  now skipped: {w}" for w in warn]
        lines += [f"  {o}" for o in fmsettings.overrides(key)] if s == "app" else []  # a profile that wins: said
    return not refused, "\n".join(lines + refused)


class Handler(http.server.BaseHTTPRequestHandler):
    timeout = TIMEOUT

    def log_message(self, *a):  # the first request line holds the token: nothing is logged
        pass

    def _send(self, status, body="", nonce="", extra=()):
        data = body.encode("utf-8")
        self.send_response(status)
        for k, v in extra:
            self.send_header(k, v)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Content-Security-Policy", f"default-src 'none'; style-src 'nonce-{nonce}'; "
                         "form-action 'self'; base-uri 'none'; frame-ancestors 'none'" if nonce else "default-src 'none'")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "same-origin")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Connection", "close")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(data)

    def _mine(self):
        port = self.server.server_address[1]
        return f"127.0.0.1:{port}", f"localhost:{port}"

    def _cookie(self):
        try:
            jar = http.cookies.SimpleCookie(self.headers.get("Cookie") or "")
        except http.cookies.CookieError:
            return b""
        got = jar.get(cookie_name(self.server.server_address[1]))
        return got.value.encode("utf-8") if got else b""

    def _allowed(self):
        """The request's path when its Host is this server's and it carries the session cookie; None when it was
        answered here: a 403, or the one exchange of the URL's token for the cookie (a 303 to /)."""
        if (self.headers.get("Host") or "").lower() not in self._mine():
            self._send(403, "refused: not this server's host")
            return None
        url = urllib.parse.urlsplit(self.path)
        if hmac.compare_digest(self._cookie(), self.server.session.encode()):
            self.server.last = time.monotonic()
            return url.path
        given = urllib.parse.parse_qs(url.query).get("t", [""])[0].encode("utf-8")
        if self.command == "GET" and url.path == "/" and given:
            with self.server.once:  # two first visits at once: one gets the cookie
                fresh = self.server.token is not None and hmac.compare_digest(given, self.server.token.encode())
                if fresh:
                    self.server.token = None
            if fresh:
                self.server.last = time.monotonic()
                self._send(303, "", extra=(("Location", "/"), ("Set-Cookie", f"{cookie_name(self.server.server_address[1])}"
                                           f"={self.server.session}; HttpOnly; SameSite=Strict; Path=/")))
                return None
        self._send(403, "refused: open the URL fm settings serve printed (it works once, in one browser)")
        return None

    def _render(self, status, msg="", bad=False):
        nonce = secrets.token_urlsafe(16)
        self._send(status, page(nonce, msg, bad), nonce)

    def do_GET(self):
        path = self._allowed()
        if path is None:
            return
        if path not in ("/", "/set"):  # /set: the page reloaded after a change
            return self._send(404, "not found")
        self._render(200)

    def do_POST(self):
        path = self._allowed()
        if path is None:
            return
        if (self.headers.get("Origin") or "").lower() not in [f"http://{h}" for h in self._mine()]:
            return self._send(403, "refused: not posted from this page")
        if path != "/set":
            return self._send(404, "not found")
        size = self.headers.get("Content-Length") or ""
        if self.headers.get("Transfer-Encoding") or not (size.isascii() and size.isdigit()):
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


class Server(http.server.ThreadingHTTPServer):
    daemon_threads = True  # a connection still open when the server stops doesn't hold the process
    block_on_close = False


def make(p=None):
    """A server bound to 127.0.0.1 on a random port, not yet serving: (server, the URL's one-time token)."""
    server = Server(("127.0.0.1", 0), Handler)
    server.token, server.session = secrets.token_urlsafe(32), secrets.token_urlsafe(32)
    server.once, server.project, server.last = threading.Lock(), p, time.monotonic()
    return server, server.token


def serve(server, idle=IDLE, stop=None):
    """Answer requests until `idle` seconds pass without an authenticated one, or `stop` (an Event) is set; then
    close."""
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
    print(f"Foreman settings: {url}\n(open it once, in one browser; Ctrl-C stops it, so do {IDLE // 60} idle "
          "minutes)", flush=True)
    old = signal.signal(signal.SIGTERM, lambda *a: sys.exit(0))
    try:
        serve(server)
    except KeyboardInterrupt:
        pass
    finally:
        signal.signal(signal.SIGTERM, old)
    print("stopped", flush=True)
    return 0
