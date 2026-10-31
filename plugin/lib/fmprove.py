"""fm prove (T-2122): fm find's candidates become proof tickets a person can rerun, or leads. An untested candidate is
instrumented on a throwaway copy to leave a marker file when it runs. It is proven when the suite stays green, a
control function the tests name leaves its marker, and the candidate leaves none: no test runs it. Repo code runs only
on the copy, and only in a tree the user said yes to with --yes-run (a flag the guard keeps the user's; the yes is kept
per tree path, not per version of its code, in Foreman state, which only fm writes). Anything inside a tree, a commit's
author email included, is only a claim, so elsewhere untested candidates stay leads (T-2202). The yes governs Foreman's
own initiative; it isn't a sandbox against a session set on running the code, which could run the tests directly.
The isolation is the environment's only: credential, Foreman, Claude, D-Bus, XDG and GPG
variables are dropped and HOME is the throwaway folder, but the code still runs as the user, with the network. fm find
itself never runs repo code, and this verb never touches the tree it reads."""
import ast
import hashlib
import json
import os
import re
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
RECEIPT = "prove-receipt.md"  # T-2123: research/, written when --capture finds nothing proven
RAN = "a test runs"  # an untested candidate's lead when its marker appeared: what fixing it looks like


def proof_id(key):
    """T-2123: a finding's id in its task's criterion (fm prove --only ID): hex, so no repo text reaches a shell."""
    return hashlib.sha1(key.encode()).hexdigest()[:12]


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


TRUST = "prove-trusted.json"  # T-2202: trees the user ran fm prove --yes-run in (state: never written but by fm)
NO_RUN = "running this tree's tests needs the user's yes, once per tree: fm prove PATH --yes-run"


def _trusted():
    try:
        with open(os.path.join(c.state_dir(), TRUST)) as f:
            return {x for x in json.load(f) if isinstance(x, str)}
    except (OSError, ValueError, TypeError):
        return set()


def trusted(root):
    """A tree the user said yes to. Nothing in a tree can say it's the user's (an author email is anyone's to write),
    and no environment variable either: FOREMAN_HOME is a session's to set (T-2202)."""
    return os.path.realpath(root) in _trusted()


def remember(root):
    c.write_atomic(os.path.join(c.state_dir(), TRUST), json.dumps(sorted(_trusted() | {os.path.realpath(root)})))


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
            return "lead", f"{RAN} {sym}: its marker appeared under `{suite}`"
        return "proven", (f"instrumented {sym} ({f['file']}:{f['line']}) and the control {control[2]}; `{suite}` stayed "
                          f"green, ran {control[2]} and never ran {sym}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def prove(root, found, limit=10, deadline=DEADLINE, run=True):
    """One ticket per live candidate, best first, up to limit: {verdict: proven|lead, evidence, kind, file, line,
    symbol, says, finder}. untested: instrumented (above), only when run (the tree's code runs). docs, dep, secret:
    re-found on a fresh copy, no code run. Other kinds need a failing test that shows them (T-2199): leads here."""
    import fmfind
    _sweep()
    can = COLD | {"untested"}  # what a check here can prove; the rest are leads whatever happens (T-2123 review)
    t0, live = time.time(), sorted((f for f in found if not f.get("held")),  # stable: best first within each group
                                   key=lambda f: (f["kind"] not in can, not run and f["kind"] == "untested"))[:limit]
    flagged = {f["symbol"] for f in found if f["kind"] == "untested"}
    suite = control = why = None
    tickets = []
    for f in live:
        t = {k: f.get(k) for k in ("kind", "file", "line", "symbol", "says", "finder", "key")}
        if time.time() - t0 > deadline:
            t.update(verdict="lead", evidence=f"not tried: fm prove's {deadline // 60}-minute budget ran out")
        elif f["kind"] in COLD:
            tmp, dst = _copy(root)
            try:
                again = any((g["kind"], g["file"], g["line"], g["symbol"]) == (f["kind"], f["file"], f["line"], f["symbol"])
                            for g in fmfind.find(dst))
            finally:
                shutil.rmtree(tmp, ignore_errors=True)
            t.update(verdict="proven" if again else "lead", fixed=not again,
                     evidence="re-found on a fresh copy by the same deterministic check: the tree itself holds it, not "
                              "its surroundings" if again else
                              "not re-found on a fresh copy: it depends on something outside the tree")
        elif f["kind"] == "untested" and not run:
            t.update(verdict="lead", evidence=NO_RUN)
        elif f["kind"] == "untested":
            if suite is None and why is None:
                suite, control, why = _pick(root, _code(root), flagged)
            v, e = ("lead", why) if not suite else _untested(root, f, suite, control)
            t.update(verdict=v, evidence=e, fixed=e.startswith(RAN))
        else:
            t.update(verdict="lead", evidence=f"a {f['kind']} needs a failing test that shows it before it counts")
        tickets.append(t)
    return {"root": root, "suite": suite, "control": control and control[2], "tickets": tickets}


def _lane_trusted(p, root):
    """T-2123: in a builder lane, the user's yes for the same tree in the main checkout (a task's criterion re-proves
    the lane's copy of it)."""
    main = c.main_worktree(p.lane) if p and getattr(p, "lane", None) else None
    return bool(main) and trusted(os.path.join(main, os.path.relpath(os.path.realpath(root), os.path.realpath(p.root))))


def cmd_prove(args):
    import fmcli
    import fmfind
    root = os.path.abspath(args.path)
    if not os.path.isdir(root):
        print(f"fm prove: not a directory: {args.path}", file=sys.stderr)
        return 2
    p, cap = c.find_project(os.getcwd()), args.capture
    bad = ("--capture N: N is how many tasks to file, at least 1" if cap is not None and cap < 1
           else "--capture files tasks: run it inside a Foreman project" if cap and not p
           else "--capture: the tree's path holds a control character, which would split its tasks' criteria"
           if cap and re.search(r"[\x00-\x1f\x7f]", root) else None)
    if bad:
        print(f"fm prove: {bad}", file=sys.stderr)
        return 2
    if args.yes_run:  # the user's yes (the guard keeps the flag theirs), kept for this tree once the call is valid (T-2235)
        try:
            remember(root)
        except OSError as e:
            print(f"fm prove: ran on your yes, but couldn't keep it for {root}: {c.plain(str(e))[:300]}", file=sys.stderr)
    try:
        found = fmfind.scan(root, fmfind.precision(p) if p else {})[1]
        for key, f in fmfind.keyed(found, os.path.realpath(root), os.path.realpath(p.root if p else root)):
            f["key"] = key  # fm find --capture's key, so a task filed from either is never filed twice
        if args.only:  # T-2123: one finding, as a task's criterion names it; gone from fm find means fixed
            found = [dict(f, held=None) for f in found if proof_id(f["key"]) == args.only]
        # ponytail: each --only re-check scans and runs the suite up to three times; cache per tree id if it drags
        res = prove(root, found, args.limit, run=args.yes_run or trusted(root) or _lane_trusted(p, root))
    except (OSError, shutil.Error) as e:
        print(f"fm prove: couldn't copy {root}: {c.plain(str(e))[:300]}", file=sys.stderr)
        return 2
    proven = [t for t in res["tickets"] if t["verdict"] == "proven"]
    if args.only:  # T-2123: a task's criterion: 0 only once the finding is gone or shown fixed; unshown stays red
        t = (res["tickets"] or [None])[0]
        fixed = t is None or bool(t.get("fixed"))
        fmcli.out(args, res | {"only": args.only, "fixed": fixed}, c.plain_lines(f"{args.only}: " + (
            "fixed: fm find no longer reports it (or the id is from another tree)" if t is None else
            f"{'fixed' if fixed else 'still open'}: {t['evidence']}")))
        return 0 if fixed else 1
    made = receipt = None
    if cap and proven:  # T-2123: planned tasks fm run works on lanes; each criterion is red until its fix
        rel = os.path.relpath(os.path.realpath(root), os.path.realpath(p.root))  # criteria run at the checkout's root:
        out = rel == os.pardir or rel.startswith(os.pardir + os.sep)  # ..cache is a folder here, not outside
        where = shlex.quote(os.path.realpath(root) if out else rel)  # a lane re-proves its own copy
        made = fmfind.capture(p, proven, cap, root, proof=lambda k: f"fm prove {where} --only {proof_id(k)}")
    elif cap:
        receipt = os.path.join(p.dir, "research", RECEIPT)
        os.makedirs(os.path.dirname(receipt), exist_ok=True)
        c.write_atomic(receipt, c.defang(c.redact(  # repo text: quoted, one line each
            f"# fm prove receipt\n\n{c.now()}: nothing proven under {json.dumps(c.plain(root))}: fm find reported "
            f"{len(found)} finding(s), {sum(1 for f in found if f.get('held'))} held back, {len(res['tickets'])} tried "
            f"(--limit {args.limit}; held back: a muted finder or a score under the bar).\n\n"
            + "".join(f"- lead {json.dumps(c.plain(t['file']))}:{t['line']} {t['kind']} {json.dumps(t['symbol'] or '-')}: "
                      f"{c.plain(t['evidence'])}\n" for t in res["tickets"]))))
    fmcli.out(args, res | ({"captured": made or [], "receipt": receipt} if cap else {}), c.plain_lines(
        f"{len(proven)} proven, {len(res['tickets']) - len(proven)} lead(s) of {len(res['tickets'])} candidate(s) "
        f"under {root}" + (f" (suite: {res['suite']}; control: {res['control']})" if res["suite"] else "") + "\n"
        + "\n".join(f"{'✓ proven' if t['verdict'] == 'proven' else '· lead  '} {t['file']}:{t['line']}  {t['kind']}  "
                    f"{json.dumps(t['symbol'] or '-')}: {t['evidence']}" for t in res["tickets"])
        + (fmfind.filed_line(p, made) if made is not None else "")
        + (f"\nNothing proven: receipt at {receipt}." if receipt else "")))
    return 1 if proven else 0
