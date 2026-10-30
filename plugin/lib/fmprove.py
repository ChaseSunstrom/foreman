"""fm prove (T-2122): fm find's candidates become proof tickets a person can rerun, or leads. An untested candidate is
instrumented on a throwaway copy to leave a marker file when it runs. It is proven when the suite stays green, a
control function the tests name leaves its marker, and the candidate leaves none: no test runs it. Repo code runs only
on the copy, and only when HEAD is the user's own commit (their global git email) or the user passes --yes-run, a flag
the guard keeps the user's. The isolation is the environment's only: credential, Foreman, Claude, D-Bus, XDG and GPG
variables are dropped and HOME is the throwaway folder, but the code still runs as the user, with the network. fm find
itself never runs repo code, and this verb never touches the tree it reads."""
import ast
import json
import os
import shlex
import shutil
import sys
import tempfile
import time

import fmcore as c

RUN_T = 300  # seconds a suite run may take, like fm adopt's gate run
DEADLINE = 900  # seconds for one fm prove; candidates past it stay leads
STALE = 86400  # a copy older than this was left by a killed run
COLD = {"docs", "dep", "secret"}  # their finder's own check, re-run cold on a fresh copy
SKIP = {".git", "node_modules", "target", "__pycache__", ".venv", "venv"}
DROP = ("FOREMAN_", "CLAUDE_", "DBUS_", "XDG_", "GPG_", "PYTHONPATH", "NODE_OPTIONS", "RUBYOPT")
SCRIPT = {"py": "python3", "js": "node", "ts": "node", "rb": "ruby"}  # tests that run themselves: the file is the suite


def _sweep():
    base = tempfile.gettempdir()
    for n in os.listdir(base):
        p = os.path.join(base, n)
        try:
            if n.startswith("fm-prove-") and time.time() - os.lstat(p).st_mtime > STALE:
                shutil.rmtree(p, ignore_errors=True)
        except OSError:
            continue


def _copy(root):
    """(tmp, copy) of root without symlinks, sockets, FIFOs or build and VCS folders: nothing in it reaches outside."""
    tmp = tempfile.mkdtemp(prefix="fm-prove-")
    dst = os.path.join(tmp, "w")

    def skip(d, names):
        return [n for n in names if n in SKIP or os.path.islink(os.path.join(d, n))
                or not (os.path.isfile(os.path.join(d, n)) or os.path.isdir(os.path.join(d, n)))]
    try:
        shutil.copytree(root, dst, ignore=skip)
    except (OSError, shutil.Error):
        shutil.rmtree(tmp, ignore_errors=True)
        raise
    return tmp, dst


def _env(home):
    """The environment repo code runs with: no credentials, no Foreman, Claude, keyring or XDG state, HOME the
    throwaway folder."""
    import fmbench
    env = {k: v for k, v in os.environ.items() if not fmbench.CREDENTIALS.match(k) and not k.startswith(DROP)}
    env["HOME"] = home
    return env


def _code(root):
    import fmfind
    return [fmfind.Src(r, t) for r, t in fmfind._files(root)[0] if os.path.splitext(r)[1].lower() in fmfind.LANG]


def _suites(root, code):
    """Commands that may run the tree's tests: the repo's own (fm map's gate detection) first, then its test files run
    as scripts by their language's interpreter."""
    import fmmap
    files = []
    for d, dirs, names in os.walk(root):
        dirs[:] = [x for x in dirs if x not in SKIP and not os.path.islink(os.path.join(d, x))]
        files += [os.path.relpath(os.path.join(d, n), root) for n in names]
    out = [g for g in fmmap._gates(root, files, []) if "test" in g]
    scripts = [f"{SCRIPT[s.lang]} {shlex.quote(s.rel)}" for s in code if s.test and s.lang in SCRIPT]
    return out + ([" && ".join(scripts)] if scripts else [])


def _control(code, skip):
    """(file, line, name, lang) of a function the tests name that fm find didn't flag: the suite must run it, or the
    suite can't show that another function goes unrun."""
    import fmfind
    said = fmfind._words("\n".join(s.text for s in code if s.test))
    return next(((s.rel, i + 1, name, s.lang) for s in code if not s.test for i, ind, name, _ in s.defs
                 if not ind and name in said and name not in skip and not name.startswith(("_", "test"))), None)


def _mark(lang, path):
    """A statement that creates the marker file at path, in lang; None where it can't be said without a header."""
    q = json.dumps(path)
    return {"py": f"__import__('pathlib').Path({q}).touch()",
            "js": f"globalThis.process?.getBuiltinModule?.('node:fs')?.writeFileSync({q}, '');",
            "ts": f"globalThis.process?.getBuiltinModule?.('node:fs')?.writeFileSync({q}, '');",
            "rb": f"File.write({q}, '')", "rs": f"let _ = std::fs::write({q}, \"\");"}.get(lang)


def _instrument(path, line, lang, marker):
    """Make the function defined at `line` create `marker` as its first statement. False when that can't be done
    safely: a one-line or expression-bodied definition, no body found, a file that doesn't parse after it."""
    stmt = _mark(lang, marker)
    with open(path, encoding="utf-8", errors="replace") as f:
        lines = f.read().split("\n")
    if not stmt or not 0 < line <= len(lines):
        return False
    if lang == "py":
        try:
            fn = next((n for n in ast.walk(ast.parse("\n".join(lines)))
                       if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.lineno == line), None)
        except SyntaxError:
            return False
        if not fn or fn.body[0].lineno == fn.lineno:
            return False
        lines.insert(fn.body[0].lineno - 1, " " * fn.body[0].col_offset + stmt)
        try:
            ast.parse("\n".join(lines))
        except SyntaxError:
            return False
    elif lang == "rb":
        head = lines[line - 1]
        if "=" in head.split("def", 1)[-1].split(")")[-1]:  # def x = expr: an endless method has no body to open
            return False
        lines.insert(line, head[:len(head) - len(head.lstrip())] + "  " + stmt)
    else:  # brace languages: the body's '{', before any ';' that would end an expression-bodied definition
        for i in range(line - 1, min(line + 4, len(lines))):
            s = lines[i]
            brace, semi, arrow = s.find("{"), s.find(";"), s.find("=>")
            if semi >= 0 and (brace < 0 or semi < brace):
                return False
            if brace >= 0:
                if 0 <= arrow and brace < arrow:  # ({a}) => a: a destructured parameter, not the body
                    return False
                lines[i] = s[:brace + 1] + " " + stmt + s[brace + 1:]
                break
        else:
            return False
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return True


def _last(out):
    return json.dumps(c.fit(c.plain(next((x.strip() for x in reversed(out.splitlines()) if x.strip()), "")), 120))


def own_tree(root):
    """'' when HEAD is the user's own commit (their global git user.email: a repo's own config can't set it), else why
    not. git runs with the repo's code-running config neutralised."""
    git = lambda *a: c._git(root, "-c", "core.fsmonitor=false", "-c", "core.hooksPath=/dev/null", "-c",
                            "log.showSignature=false", *a, timeout=30)
    me, head = git("config", "--global", "user.email").strip().lower(), \
        git("log", "-1", "--no-show-signature", "--format=%ae").strip().lower()
    if not head:
        return "no git history here"
    return "" if me and head == me else \
        f"HEAD's author is {c.plain(head)}, not you ({c.plain(me) or 'no global git user.email'})"


def _pick(root, code, flagged):
    """(suite, control, '') for the first command that is green untouched and runs the control, else (None, None, why
    each failed)."""
    control, tried = _control(code, flagged), []
    for cmd in _suites(root, code):
        tmp, dst = _copy(root)
        try:
            ran, out = c.run_command(dst, cmd, timeout=RUN_T, env=_env(tmp))
            if ran:
                tried.append(f"`{cmd}` isn't green untouched (exit {ran}: {_last(out)})")
                continue
            mark = os.path.join(tmp, "ran-control")
            if not control or not _instrument(os.path.join(dst, control[0]), control[1], control[3], mark):
                tried.append(f"`{cmd}` is green, but no function the tests name could be instrumented to show it runs "
                             "code")
                continue
            ran, out = c.run_command(dst, cmd, timeout=RUN_T, env=_env(tmp))
            if ran or not os.path.exists(mark):
                tried.append(f"`{cmd}` never ran {control[2]} (which the tests name), so it can't show a function goes "
                             "unrun")
                continue
            return cmd, control, ""
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    return None, None, "; ".join(tried) or "no test command found here (fm check add '<cmd>' names one)"


def _untested(root, f, suite, control):
    """One untested candidate, instrumented beside the control on a fresh copy: (verdict, evidence)."""
    import fmfind
    tmp, dst = _copy(root)
    try:
        mine, theirs = os.path.join(tmp, "ran-candidate"), os.path.join(tmp, "ran-control")
        lang = fmfind.LANG.get(os.path.splitext(f["file"])[1].lower())
        jobs = sorted([(f["file"], f["line"], lang, mine), (control[0], control[1], control[3], theirs)],
                      key=lambda j: (j[0], -j[1]))  # the later line first: an insertion shifts what follows it
        done = {m: _instrument(os.path.join(dst, p), n, lg, m) for p, n, lg, m in jobs}
        sym = json.dumps(f["symbol"])
        if not done[mine]:
            return "lead", f"couldn't instrument {sym} safely here (a one-line or expression-bodied definition)"
        ran, out = c.run_command(dst, suite, timeout=RUN_T, env=_env(tmp))
        if ran:
            return "lead", f"`{suite}` failed with the markers in place (exit {ran}: {_last(out)})"
        if not os.path.exists(theirs):
            return "lead", f"the control {control[2]} left no marker this run, so it proves nothing"
        if os.path.exists(mine):
            return "lead", f"a test runs {sym}: its marker appeared under `{suite}`"
        return "proven", (f"instrumented {sym} ({f['file']}:{f['line']}) and the control {control[2]}; `{suite}` stayed "
                          f"green, ran {control[2]} and never ran {sym}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def prove(root, found, limit=10, deadline=DEADLINE):
    """One ticket per live candidate, best first, up to limit: {verdict: proven|lead, evidence, kind, file, line,
    symbol, says, finder}. untested: instrumented (above). docs, dep, secret: re-found on a fresh copy. Other kinds need
    a failing test that shows them (T-2199): leads here."""
    import fmfind
    _sweep()
    t0, live = time.time(), [f for f in found if not f.get("held")][:limit]
    flagged = {f["symbol"] for f in found if f["kind"] == "untested"}
    suite = control = why = None
    tickets = []
    for f in live:
        t = {k: f.get(k) for k in ("kind", "file", "line", "symbol", "says", "finder")}
        if time.time() - t0 > deadline:
            t.update(verdict="lead", evidence=f"not tried: fm prove's {deadline // 60}-minute budget ran out")
        elif f["kind"] in COLD:
            tmp, dst = _copy(root)
            try:
                again = any((g["kind"], g["file"], g["line"], g["symbol"]) == (f["kind"], f["file"], f["line"], f["symbol"])
                            for g in fmfind.find(dst))
            finally:
                shutil.rmtree(tmp, ignore_errors=True)
            t.update(verdict="proven" if again else "lead",
                     evidence="re-found on a fresh copy by the same deterministic check: the tree itself holds it, not "
                              "its surroundings" if again else
                              "not re-found on a fresh copy: it depends on something outside the tree")
        elif f["kind"] == "untested":
            if suite is None and why is None:
                suite, control, why = _pick(root, _code(root), flagged)
            v, e = ("lead", why) if not suite else _untested(root, f, suite, control)
            t.update(verdict=v, evidence=e)
        else:
            t.update(verdict="lead", evidence=f"a {f['kind']} needs a failing test that shows it before it counts")
        tickets.append(t)
    return {"root": root, "suite": suite, "control": control and control[2], "tickets": tickets}


def cmd_prove(args):
    import fmcli
    import fmfind
    root = os.path.abspath(args.path)
    if not os.path.isdir(root):
        print(f"fm prove: not a directory: {args.path}", file=sys.stderr)
        return 2
    why = "" if args.yes_run else own_tree(root)
    if why:  # proving runs the tree's tests: only the user decides to run a tree that isn't theirs
        print(f"fm prove: not run: {why}. Proving runs this tree's tests on a throwaway copy, so it runs only where "
              "HEAD is your own commit; the user can run it anyway with fm prove PATH --yes-run", file=sys.stderr)
        return 2
    p = c.find_project(os.getcwd())
    try:
        res = prove(root, fmfind.scan(root, fmfind.precision(p) if p else {})[1], args.limit)
    except (OSError, shutil.Error) as e:
        print(f"fm prove: couldn't copy {root}: {c.plain(str(e))[:300]}", file=sys.stderr)
        return 2
    proven = [t for t in res["tickets"] if t["verdict"] == "proven"]
    fmcli.out(args, res, c.plain_lines(
        f"{len(proven)} proven, {len(res['tickets']) - len(proven)} lead(s) of {len(res['tickets'])} candidate(s) "
        f"under {root}" + (f" (suite: {res['suite']}; control: {res['control']})" if res["suite"] else "") + "\n"
        + "\n".join(f"{'✓ proven' if t['verdict'] == 'proven' else '· lead  '} {t['file']}:{t['line']}  {t['kind']}  "
                    f"{json.dumps(t['symbol'] or '-')}: {t['evidence']}" for t in res["tickets"])))
    return 1 if proven else 0
