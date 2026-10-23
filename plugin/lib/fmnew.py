"""fm new (T-1519): strict-by-default templates, each passing as shipped the check that keeps it strict. A web page and
a 3D scene pass fm design lint (and the web page's Content-Security-Policy refuses other hosts); an fm code panel
loads, draws inside its box in theme styles within fm code's time budget at every size, and its handlers take an event
with no fields.

  fm new [list]            the templates: what each is and the file it lands as
  fm new NAME [DIR]        copy one, never over an existing file (created O_EXCL); --force replaces it, and a symlink
                           there is replaced itself, never written through; a panel lands in fm code's tui/
  fm new check PATH... [--run]   design lint for a page; for a .py the panel rules, which RUN the file: only one fm code
                           would load (owned by you, writable by no one else), and one inside a project (a .git above
                           it) only with --run, so a repo's code never runs as you by accident

The panel check runs in a child (fmplaybooks._run: a new temporary folder, stdin closed, limits, CHECK_SECONDS, then
its process group killed); the child's verdict counts only on a line with a token made for that run, so a file that
exits early (sys.exit, os._exit), swallows exceptions or hangs never passes. The scene is the playbook's own file
(references/ui/templates/scene.html), not a copy of it."""
import json
import os
import secrets
import tempfile
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
CHECK_SECONDS = 20  # a panel check that runs longer is killed
_CHILD = """import json, sys
sys.path.insert(0, {lib!r})
import fmnew
try:
    found = fmnew._panel_problems({path!r})
except SystemExit as e:
    found = [f"called sys.exit({{e.code!r}}): it would quit fm code"]
print({token!r} + json.dumps(found), flush=True)
"""


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


def _panel(path):
    """_panel_problems in a child (see the module): its verdict, or why it gave none."""
    import fmplaybooks
    token = f"fm-new-check-{secrets.token_hex(8)}:"
    code = _CHILD.format(lib=os.path.dirname(os.path.abspath(__file__)), path=os.path.abspath(path), token=token)
    with tempfile.TemporaryFile() as out:  # its size capped by the child's file-size limit
        why = fmplaybooks._run(code, CHECK_SECONDS, fmplaybooks._limits(), what="the check", stdout=out)
        out.seek(0)
        text = out.read().decode("utf-8", "replace")
    if why:
        return [why + (": it would hang fm code" if why.startswith("timed out") else "")]
    line = next((x for x in reversed(text.splitlines()) if x.startswith(token)), "")
    try:
        found = json.loads(line[len(token):])
    except ValueError:
        found = None
    if not isinstance(found, list):
        return ["ended before the check finished (os._exit, or a thread that quit the process): fm code would too"]
    return [str(x) for x in found]


def _runnable(path, run):
    """Why fm new check won't run this .py, or None: fm code's own rule (fmcodetui.load_extensions) first, then a
    project's file (a .git above it, outside fm code's tui/ folder) only when run is asked for."""
    import fmcodetui
    try:
        st = os.stat(path)
    except OSError as e:
        return f"can't read it: {e.strerror}"
    uid = getattr(os, "getuid", lambda: None)()
    if (uid is not None and st.st_uid != uid) or st.st_mode & 0o022:
        return "skipped: another user can change it (fm code wouldn't load it either)"
    real = os.path.realpath(path)
    if run or real.startswith(os.path.realpath(fmcodetui.extensions_dir()) + os.sep):
        return None
    d = os.path.dirname(real)
    while not os.path.exists(os.path.join(d, ".git")):
        if os.path.dirname(d) == d:
            return None
        d = os.path.dirname(d)
    return (f"it sits in the project at {d}, and checking a panel runs it: a project's files never run as you "
            f"unless you say so (fm new check PATH --run)")


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

        def setting(self, *a, **k):  # T-1657: API version 2; a declaration is checked when the app loads it
            pass

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


def check(path, run=False):
    """One file's problems against its template's rules: [] when it keeps them. A .py is run (see _runnable)."""
    import fmdesign
    if not os.path.isfile(path):
        return [f"{path}: not a file"]
    ext = os.path.splitext(path)[1].lower()
    if ext == ".py":
        why = _runnable(path, run)
        return [f"{path}: {why}"] if why else [f"{path}: {x}" for x in _panel(path)]
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
            raise fmcli.UsageError("fm new check PATH... [--run]: a page or an fm code panel (a panel's check runs "
                                   "the file) to hold to its template's rules")
        found = [x for p in words[1:] for x in check(p, run=getattr(args, "run", False))]
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
    try:
        with open(source(name), encoding="utf-8") as f:
            text = f.read()
        if args.force:
            c.write_atomic(dest, text)  # a symlink at dest is replaced itself, never written through
            os.chmod(dest, 0o644)  # fm code skips an extension others can write
        else:
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            fd = os.open(dest, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)  # whatever is there, or appears, stays
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as f:
                    f.write(text)
            except BaseException:
                os.unlink(dest)  # ours: O_EXCL made it
                raise
    except FileExistsError:
        raise fmcli.UsageError(f"{dest} exists; fm new never writes over a file (--force replaces it, and a symlink "
                               "there is replaced itself, never written through)")
    except OSError as e:
        raise fmcli.UsageError(f"can't write {dest}: {e.strerror or e}")
    then = (f"; then name its panel in a [layout] column of {os.path.join(c.foreman_home(), 'tui.toml')}"
            if name == "panel" else "")
    fmcli.out(args, {"wrote": dest, "template": name}, f"Wrote {dest}.\nKeep it strict: fm new check {dest}{then}")
    return 0
