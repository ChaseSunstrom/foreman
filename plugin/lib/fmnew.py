"""fm new (T-1519): strict-by-default templates, each passing as shipped the check that keeps it strict. A web page and
a 3D scene pass fm design lint (and the web page's Content-Security-Policy refuses other hosts); an fm code panel
loads, draws inside its box in theme styles within fm code's time budget at every size, and its handlers take an event
with no fields.

  fm new [list]            the templates: what each is and the file it lands as
  fm new NAME [DIR]        copy one (never over an existing file without --force); a panel lands in fm code's tui/
  fm new check PATH...     design lint for a page, the panel rules for a .py (it runs the file, as fm code would)

The scene is the playbook's own file (references/ui/templates/scene.html), not a copy of it."""
import os
import signal
import time
import types

import fmcore as c

TEMPLATES = {  # name: (source under the plugin, the file it lands as, what it is)
    "web": ("templates/web/index.html", "index.html",
            "a one-page site: tokens for colour, type, space, radius, lift and motion; light and dark at AA contrast; "
            "a serif display and a humanist body from local faces; a CSP that refuses other hosts; reduced motion"),
    "scene": ("skills/playbooks/references/ui/templates/scene.html", "scene.html",
              "a one-file WebGL2 scene: poster first, a text twin, each survival clause of the ui/scene-3d.md playbook"),
    "panel": ("templates/tui/panel.py", "panel.py",
              "an fm code panel: an event tally that fits its box, in theme styles, inside fm code's time budget"),
}
SIZES = ((1, 1), (12, 2), (40, 6), (120, 30))  # (columns, lines) a panel is drawn at
SAMPLE_EVENTS = ("task", "plan", "step", "tokens", "say")  # what a "*" handler is fed, each with no fields
CHECK_SECONDS = 10  # a panel check that runs longer stops


def source(name):
    return os.path.join(c.PLUGIN_ROOT, TEMPLATES[name][0])


def _draw(tui, fn, state, w, h):
    """Why one panel fails at w×h, or None. Timed over PANEL_STRIKES frames, as fm code switches one off."""
    took = []
    for _ in range(tui.PANEL_STRIKES):
        t0 = time.monotonic()
        try:
            lines = fn(state, w, h, None)
        except Exception as e:
            return f"raised {type(e).__name__}: {e}"
        took.append(time.monotonic() - t0)
    if min(took) > tui.PANEL_BUDGET:
        return f"took {min(took) * 1000:.0f} ms a frame (fm code's budget is {tui.PANEL_BUDGET * 1000:.0f} ms)"
    if not isinstance(lines, list) or not all(isinstance(ln, list) and all(isinstance(s, tuple) and len(s) == 2
                                                                           for s in ln) for ln in lines):
        return "didn't return a list of lines, each a list of (text, style)"
    if len(lines) > h:
        return f"{len(lines)} lines for a {h}-line box"
    for ln in lines:
        cols = sum(tui.width(t) for t, _ in ln)
        if cols > w:
            return f"a line {cols} columns wide for a {w}-column box"
        bad = [s for _, s in ln if not isinstance(s, str) or s not in tui.THEME]
        if bad:
            return f"style {bad[0]!r} isn't a theme style (text, strong, dim, accent, ok, bad, warn, chart, chip_ok…)"
    return None


class _Overtime(BaseException):  # not an Exception: the file's own `except Exception` can't swallow it
    pass


def _panel(path):
    """_panel_problems under an alarm of CHECK_SECONDS (fm's main thread; elsewhere unbounded): an extension that
    loops forever would hang fm code too."""
    def stop(*_):
        raise _Overtime
    try:
        old = signal.signal(signal.SIGALRM, stop)
    except (AttributeError, ValueError):  # no SIGALRM, or not the main thread
        return _panel_problems(path)
    signal.alarm(CHECK_SECONDS)
    try:
        return _panel_problems(path)
    except _Overtime:
        return [f"still running after {CHECK_SECONDS} s: it would hang fm code"]
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)


def _panel_problems(path):
    """An fm code extension's problems: setup(api) runs against a recorder (a check never changes a running TUI)."""
    import fmcodetui as tui
    panels, handlers = [], []

    class Recorder:
        version = tui.API.version

        def panel(self, name, title, fn):
            panels.append((name, fn))

        def command(self, name, fn, key=None, label=None):
            pass

        def on(self, event, fn):
            handlers.append((event, fn))

    try:  # compiled from the source each time: no __pycache__ written beside it, none read back stale
        with open(path, encoding="utf-8") as f:
            code = compile(f.read(), path, "exec")
        mod = types.ModuleType("fm_new_check")
        mod.__file__ = path
        exec(code, mod.__dict__)
        mod.setup(Recorder())
    except Exception as e:  # its own bug, said in one line
        return [f"doesn't load: {type(e).__name__}: {e}"]
    if not panels:
        return ["adds no panel: setup(api) calls api.panel(name, title, draw)"]
    out, fed = [], tui.State()
    for event, fn in handlers:
        for kind in SAMPLE_EVENTS if event == "*" else (event,):
            t0 = time.monotonic()
            try:
                fn(fed, {"event": kind})
            except Exception as e:
                out.append(f"its {event} handler raised {type(e).__name__}: {e} on a {kind} event with no fields")
                break
            if time.monotonic() - t0 > tui.HANDLER_BUDGET:
                out.append(f"its {event} handler took over {tui.HANDLER_BUDGET * 1000:.0f} ms")
                break
    for state in (tui.State(), fed):  # before any event, then after some
        for name, fn in panels:
            why = next((f"at {w}×{h}: {x}" for w, h in SIZES for x in [_draw(tui, fn, state, w, h)] if x), None)
            if why and f"panel {name} {why}" not in out:
                out.append(f"panel {name} {why}")
    return out


def check(path):
    """One file's problems against its template's rules: [] when it keeps them."""
    import fmdesign
    if not os.path.isfile(path):
        return [f"{path}: not a file"]
    ext = os.path.splitext(path)[1].lower()
    if ext == ".py":
        return [f"{path}: {x}" for x in _panel(path)]
    if ext not in fmdesign.EXTS:
        return [f"{path}: fm new check reads a page ({' '.join(sorted(fmdesign.EXTS))}) or an fm code panel (.py)"]
    skipped = []
    return fmdesign.render(fmdesign.lint([path], skipped)) + [f"{x['file']}: not read: {x['why']}" for x in skipped]


def cmd_new(args):
    import fmcli
    words = list(args.words or [])
    if words[:1] == ["templates"]:  # fm new templates [list] is fm new list
        words = words[1:]
    if words in ([], ["list"]):
        rows = [{"name": n, "file": f, "what": what, "source": source(n)} for n, (_, f, what) in TEMPLATES.items()]
        fmcli.out(args, {"templates": rows}, "Templates, strict by default (fm new NAME [DIR]; fm new check PATH):\n"
                  + "\n".join(f"  {r['name']:<6} {r['file']:<11} {r['what']}" for r in rows)
                  + "\n  (a panel lands in fm code's tui/ folder in Foreman's home unless DIR is given)")
        return 0
    if words[0] == "check":
        if len(words) < 2:
            raise fmcli.UsageError("fm new check PATH...: a page or an fm code panel to hold to its template's rules")
        found = [x for p in words[1:] for x in check(p)]
        fmcli.out(args, {"problems": found}, "\n".join(found) if found else
                  f"✓ {len(words) - 1} file(s) keep their template's rules")
        return 1 if found else 0
    name = words[0]
    if name not in TEMPLATES or len(words) > 2:
        raise fmcli.UsageError(f"fm new {'|'.join(TEMPLATES)} [DIR] [--force] · fm new list · fm new check PATH...")
    if len(words) > 1:
        d = words[1]
    elif name == "panel":
        import fmcodetui
        d = fmcodetui.extensions_dir()  # where fm code loads extensions from
    else:
        d = "."
    dest = os.path.abspath(os.path.join(d, TEMPLATES[name][1]))
    if os.path.lexists(dest) and not args.force:
        raise fmcli.UsageError(f"{dest} exists; fm new never writes over a file (--force replaces it)")
    try:
        with open(source(name), encoding="utf-8") as f:
            text = f.read()
        c.write_atomic(dest, text)  # a planted link at dest is replaced, never written through
        os.chmod(dest, 0o644)  # fm code skips an extension others can write
    except OSError as e:
        raise fmcli.UsageError(f"can't write {dest}: {e.strerror or e}")
    then = (f"; then name its panel in a [layout] column of {os.path.join(c.foreman_home(), 'tui.toml')}"
            if name == "panel" else "")
    fmcli.out(args, {"wrote": dest, "template": name}, f"Wrote {dest}.\nKeep it strict: fm new check {dest}{then}")
    return 0
