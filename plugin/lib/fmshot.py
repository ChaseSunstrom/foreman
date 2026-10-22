"""fm shot (T-1636): what a page looks like, from a headless Chromium this machine already has (FOREMAN_CHROME, one on
PATH, or Playwright's download; nothing is ever installed). fm shot URL|FILE... [--frames N] [--every MS] [--frozen]
[--out DIR] writes, per page, viewport.png once it has loaded, frame-00.png… N frames --every ms apart in real time
(headless virtual time barely runs requestAnimationFrame) and, when the frames differ, poster.png: the frame with the
most painted pixels (those off the frame's commonest colour). --frozen applies fm smoke's frozen profile first (the
clock fixed at 2026-01-15 10:00 UTC, CSS animations and transitions paused), so the frames should match. Shots go in
<project state>/shots/<page>/ unless --out names a folder (never a link); a rerun replaces its own files. Without a
browser it exits 0 and says why.

The browser is driven over --remote-debugging-pipe (fd 3 in, fd 4 out, NUL-separated JSON): stdlib only, the way
test_site_hero's devtools() does (T-1610)."""
import base64
import collections
import contextlib
import glob
import json
import os
import pathlib
import re
import select
import shutil
import signal
import tempfile
import time

import fmcore as c
import fmimg

SIZE = (1280, 800)
FRAMES, EVERY_MS = 5, 250  # fm smoke's motion profile: five frames 250 ms apart
MAX_FRAMES, MIN_EVERY, MAX_EVERY = 60, 10, 10000
LOAD_S, CALL_S, SETTLE_S = 30, 30, 0.5
MAX_MSG = 64 << 20  # one DevTools message: a screenshot's base64 is a few MB at most
LOCK_S = 120
FROZEN_MS = 1768471200000  # 2026-01-15T10:00:00Z, smoke_web.cjs's NOW
# smoke_web.cjs's freeze(): CSS animations and transitions held still (test_shot keeps the two in step)
FREEZE_CSS = ("*, *::before, *::after { animation-play-state: paused !important; transition: none !important; "
              "caret-color: transparent !important; scroll-behavior: auto !important }")
FREEZE = """(() => {
  const D = Date, T = %d;
  function F(...a) { return new.target ? new D(...(a.length ? a : [T])) : new D(T).toString(); }
  F.prototype = D.prototype; F.now = () => T; F.parse = D.parse; F.UTC = D.UTC;
  window.Date = F;
  const put = () => { const s = document.createElement("style"); s.textContent = %s; document.documentElement.appendChild(s); };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", put); else put();
})();""" % (FROZEN_MS, json.dumps(FREEZE_CSS))
# Headless Chromium keeps running a CSS animation under the paused rule until something recalculates style (even a
# pause() from a load listener didn't hold it); asked once the page has loaded, getAnimations() does. Each animation,
# Web Animations too, is held at its start, so a frozen shot is the same on every run.
HOLD = "document.getAnimations().forEach(a => { a.pause(); a.currentTime = 0; })"
OURS = re.compile(r"(viewport|poster|frame-\d+)\.png")
NONE = ("no browser found (looked for FOREMAN_CHROME, chrome-headless-shell, chromium, chromium-browser or "
        "google-chrome on PATH, and Playwright's download in ~/.cache/ms-playwright); fm shot installs nothing: "
        "set FOREMAN_CHROME=<a Chromium binary> or install one yourself")


def chrome():
    """A headless Chromium: FOREMAN_CHROME, one on PATH, or Playwright's newest download; None if absent."""
    builds = glob.glob(os.path.expanduser(
        "~/.cache/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-*/chrome-headless-shell"))
    build = lambda p: int((re.search(r"chromium_headless_shell-(\d+)/", p) or (0, -1))[1])  # noqa: E731
    found = [os.environ.get("FOREMAN_CHROME")] + [shutil.which(n) for n in (
        "chrome-headless-shell", "chromium", "chromium-browser", "google-chrome")] + sorted(builds, key=build, reverse=True)
    return next((p for p in found if p and os.path.isfile(p) and os.access(p, os.X_OK)), None)


def painted(img):
    """Pixels off the image's commonest colour (its background)."""
    px = memoryview(img.rgba).cast("I")
    return len(px) - collections.Counter(px).most_common(1)[0][1] if len(px) else 0


class Browser:
    """One headless Chromium over the DevTools pipe; close() kills its whole process group."""

    def __init__(self, path, size):
        import fcntl
        self.profile = tempfile.TemporaryDirectory(prefix="fm-shot-")
        child_in, self.feed = os.pipe()
        self.out, child_out = os.pipe()
        high = [fcntl.fcntl(fd, fcntl.F_DUPFD_CLOEXEC, 10) for fd in (child_in, child_out)]
        try:
            self.pid = os.posix_spawn(path, [
                path, "--headless", "--remote-debugging-pipe", "--user-data-dir=" + self.profile.name,
                "--no-first-run", "--hide-scrollbars", "--mute-audio", "--use-angle=swiftshader",
                "--enable-unsafe-swiftshader", f"--window-size={size[0]},{size[1]}", "about:blank"], os.environ,
                setsid=True, file_actions=[(os.POSIX_SPAWN_DUP2, high[0], 3), (os.POSIX_SPAWN_DUP2, high[1], 4),
                                           (os.POSIX_SPAWN_OPEN, 0, os.devnull, os.O_RDONLY, 0),
                                           (os.POSIX_SPAWN_OPEN, 1, os.devnull, os.O_WRONLY, 0),
                                           (os.POSIX_SPAWN_OPEN, 2, os.devnull, os.O_WRONLY, 0)])
        except OSError:
            self._fds()
            raise
        finally:
            for fd in (child_in, child_out, *high):
                os.close(fd)
        self.buf, self.n, self.events = b"", 0, []
        try:
            tid = self.call("Target.createTarget", url="about:blank")["targetId"]
            self.sid = self.call("Target.attachToTarget", targetId=tid, flatten=True)["sessionId"]
            self.call("Page.enable", self.sid)
            self.call("Emulation.setDeviceMetricsOverride", self.sid, width=size[0], height=size[1],
                      deviceScaleFactor=1, mobile=False)
        except BaseException:  # never leave a browser running behind a failed start
            self.close()
            raise

    def _fds(self):
        for fd in (self.feed, self.out):
            try:
                os.close(fd)
            except OSError:
                pass
        self.profile.cleanup()

    def _next(self, deadline, what):
        while b"\0" not in self.buf:
            if len(self.buf) > MAX_MSG:
                raise RuntimeError(f"an answer over {MAX_MSG >> 20} MB during {what}")
            if not select.select([self.out], [], [], max(0.0, deadline - time.monotonic()))[0]:
                raise TimeoutError(f"no answer to {what} in {CALL_S} s")
            chunk = os.read(self.out, 1 << 16)
            if not chunk:
                raise EOFError(f"the browser closed during {what}")
            self.buf += chunk
        line, self.buf = self.buf.split(b"\0", 1)
        return json.loads(line)

    def call(self, method, session=None, **params):
        self.n += 1
        os.write(self.feed, json.dumps({"id": self.n, "method": method, "params": params,
                                        **({"sessionId": session} if session else {})}).encode() + b"\0")
        deadline = time.monotonic() + CALL_S
        while True:
            got = self._next(deadline, method)
            if got.get("id") == self.n:
                if "error" in got:
                    raise RuntimeError(f"{method}: {got['error'].get('message', got['error'])}")
                return got.get("result") or {}
            if got.get("method"):
                self.events.append(got["method"])

    def wait(self, event, seconds):
        """True once `event` has come (since the last wait), False after `seconds`."""
        deadline = time.monotonic() + seconds
        try:
            while event not in self.events:
                got = self._next(deadline, event)
                if got.get("method"):
                    self.events.append(got["method"])
            return True
        except TimeoutError:
            return False
        finally:
            self.events.clear()

    def png(self):
        return base64.b64decode(self.call("Page.captureScreenshot", self.sid, format="png")["data"])

    def close(self):
        try:
            os.killpg(self.pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass
        os.waitpid(self.pid, 0)
        self._fds()


def _url(target):
    import fmcli
    if re.match(r"(?i)(https?|file)://", target):
        return target
    if not os.path.isfile(target):  # javascript:, data:, chrome: and the rest are refused here too
        raise fmcli.UsageError(f"fm shot takes an http(s) or file URL or an existing file: {target!r}")
    return pathlib.Path(os.path.abspath(target)).as_uri()


def _slug(url, taken):
    m = re.match(r"(?i)[a-z]+://([^/?#]*)([^?#]*)", url)
    raw = os.path.basename(m[2]) if url.lower().startswith("file:") else (m[1] + m[2]) if m else url
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", raw).strip("-.")[:60] or "page"
    name, i = slug, 1
    while name in taken:
        i += 1
        name = f"{slug}-{i}"
    taken.add(name)
    return name


def _folder(base, name):
    import fmcli
    folder = os.path.join(base, name)
    os.makedirs(folder, exist_ok=True)
    if os.path.islink(folder):
        raise fmcli.UsageError(f"{folder} is a link: fm shot never writes through one")
    for f in os.listdir(folder):  # a rerun leaves none of the last run's frames behind
        if OURS.fullmatch(f):
            os.unlink(os.path.join(folder, f))
    return folder


def _write(folder, name, data):
    path = os.path.join(folder, name)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644)  # cleared just before
    with os.fdopen(fd, "wb") as f:
        f.write(data)
    return path


def shoot(b, url, folder, frames, every, frozen):
    """One page: {url, folder, shots, animated, poster_of, notes}."""
    notes = []
    nav = b.call("Page.navigate", b.sid, url=url)
    if nav.get("errorText"):
        raise RuntimeError(f"did not load: {nav['errorText']}")
    if not b.wait("Page.loadEventFired", LOAD_S):
        notes.append(f"still loading after {LOAD_S} s; shot as it stood")
    time.sleep(SETTLE_S)
    if frozen:
        b.call("Runtime.evaluate", b.sid, expression=HOLD)
    shots = [_write(folder, "viewport.png", b.png())]
    pngs, start = [], time.monotonic()
    for i in range(frames):
        time.sleep(max(0.0, start + i * every / 1000 - time.monotonic()))
        pngs.append(b.png())
        shots.append(_write(folder, f"frame-{i:02d}.png", pngs[-1]))
    animated, poster_of = len(set(pngs)) > 1, None
    if animated:  # ponytail: pure-Python decode, about a second a megapixel per frame; fine at a viewport's size
        counts = [painted(fmimg.decode(x)) for x in pngs]
        best = counts.index(max(counts))
        poster_of = f"frame-{best:02d}.png"
        shots.append(_write(folder, "poster.png", pngs[best]))
        if frozen:
            notes.append("still moves with the clock frozen and CSS animations paused (a canvas, video, timer or "
                         "requestAnimationFrame loop)")
    return {"url": url, "folder": folder, "shots": shots, "animated": animated, "poster_of": poster_of,
            "notes": notes}


def cmd_shot(args):
    import fmcli
    if not 0 <= args.frames <= MAX_FRAMES:
        raise fmcli.UsageError(f"--frames is 0 to {MAX_FRAMES}")
    if not MIN_EVERY <= args.every <= MAX_EVERY:
        raise fmcli.UsageError(f"--every is {MIN_EVERY} to {MAX_EVERY} ms")
    urls = [_url(t) for t in args.targets]
    if args.out:
        base = os.path.abspath(args.out)
        if os.path.islink(base):
            raise fmcli.UsageError(f"--out {base} is a link: name a real folder")
        if os.path.exists(base) and not os.path.isdir(base):
            raise fmcli.UsageError(f"--out {base} isn't a folder")
    else:
        base = os.path.join(fmcli.resolve(args).dir, "shots")
    path = chrome()
    if not path:
        return fmcli.out(args, {"skipped": NONE}, f"fm shot: skipped: {NONE}.")
    os.makedirs(base, exist_ok=True)
    pages, failed, taken = [], [], set()
    # a second run into Foreman's folder waits for the first; --out is the user's folder: no .lock left in it
    with contextlib.nullcontext() if args.out else c.lock(base, timeout=LOCK_S):
        try:
            b = Browser(path, SIZE)
        except (OSError, RuntimeError, EOFError, ValueError) as e:  # TimeoutError is an OSError
            failed.append({"url": ", ".join(urls), "error": f"the browser ({path}) did not start: {e}"})
            b = None
        try:
            if b and args.frozen:
                b.call("Page.addScriptToEvaluateOnNewDocument", b.sid, source=FREEZE)
            for url in urls if b else []:
                try:
                    pages.append(shoot(b, url, _folder(base, _slug(url, taken)), args.frames, args.every, args.frozen))
                except (OSError, RuntimeError, EOFError, ValueError) as e:
                    failed.append({"url": url, "error": str(e)})
                    if isinstance(e, (EOFError, TimeoutError)):  # the browser is gone or hung: the rest would wait too
                        break
        except (OSError, RuntimeError, EOFError, ValueError) as e:
            failed.append({"url": ", ".join(urls), "error": f"the browser ({path}) failed: {e}"})
        finally:
            if b:
                b.close()
    lines = []
    for pg in pages:
        names = [os.path.basename(s) for s in pg["shots"]]
        frames = [n for n in names if n.startswith("frame-")]
        lines.append(f"fm shot: {pg['url']} → {pg['folder']}")
        lines.append("  viewport.png")
        if frames:
            lines.append(f"  {frames[0]}" + (f" … {frames[-1]}" if len(frames) > 1 else "")
                         + f" ({len(frames)} frames {args.every} ms apart, real time"
                         + (", frozen clock" if args.frozen else "") + ")")
        if pg["poster_of"]:
            lines.append(f"  poster.png ({pg['poster_of']}: the most painted of {len(frames)})")
        elif len(frames) > 1:
            lines.append("  no poster: the page held still")
        lines += [f"  note: {n}" for n in pg["notes"]]
    lines += [f"✗ {f['url']}: {f['error']}" for f in failed]
    fmcli.out(args, {"browser": path, "pages": pages, "failed": failed}, "\n".join(lines))
    if failed:
        raise SystemExit(1)
    return None
