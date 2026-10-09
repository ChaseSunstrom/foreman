"""T-0706 (Frontier 06, first slice): a red run comes with what a debugger would gather first, before any guessing.
fm suspects: files ranked from signals already on hand (repo frames on the stack, what the task changed, the sources
linked to the failing tests, edit recency); the failure hook adds its top 3. fm whyred: the minimal set of hunks that
turns a green command red (delta debugging against the task's start tree, in a scratch copy). fm record: the locals of
each repo frame the failure unwound through (sys.monitoring, Python 3.12+)."""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

import fmcore as c

MAX_RUNS = 32  # whyred's budget of command runs


def _base(p):
    act = c.active_brief(c.load_briefs(p), p.lane)
    return (c.task_base(p.root, act) if act else None) or "HEAD", act


def board(p, text):
    """[(path, score, [reasons])], best first, for a failure's output."""
    import fminstr
    import fmmap
    base, act = _base(p)
    changed = set(fmmap.changed(p.root, base) or [])
    m = fmmap.load(p)
    scores, why = {}, {}

    def add(f, s, reason):
        scores[f] = scores.get(f, 0) + s
        why.setdefault(f, []).append(reason)
    frames = [(rel, n) for path, n, _ in fminstr._frames(text) if (rel := fminstr._locate(path, p.root))]
    innermost = True
    for rel, n in frames:  # innermost first; a file counts once, however many of its frames the stack holds
        if rel in scores:
            continue
        test = bool(fmmap._TEST.search(rel))
        add(rel, 1 if test else 2 + innermost, f"on the stack at line {n}" + (" (innermost)" if innermost and not test
                                                                              else ""))
        innermost = innermost and test
        if rel in changed:
            add(rel, 2, "changed and on the stack")
    ids = " ".join(fminstr._test_id(h.group(0)) for h in fminstr._HEADER.finditer(text)) + " " + " ".join(
        c.failing_tests(text))
    tests = {t for t in m["tests"] if os.path.basename(t).rsplit(".", 1)[0] in ids} | {r for r, _ in frames
                                                                                       if r in m["tests"]}
    for t in sorted(tests):
        for src in m["tests"][t]:
            add(src, 1.5 + (src in changed), f"linked to {os.path.basename(t)}")
    for f in changed:  # since the last green, the change is the likeliest cause
        if os.path.isfile(os.path.join(p.root, f)):
            add(f, 3, "changed in this task")
    recent = sorted(c.task_touches(p, act.id).items(), key=lambda kv: kv[1], reverse=True) if act else []
    for i, (f, _) in enumerate(recent[:2]):
        add(f, 1 / (i + 1), "edited last" if not i else "edited before that")
    return sorted(((f, s, why[f]) for f, s in scores.items()), key=lambda x: -x[1])


def line(p, text, top=3):
    """The failure hook's one line, or None when nothing points anywhere."""
    ranked = board(p, text)[:top]
    return ("Suspects: " + "; ".join(f"{f} ({', '.join(r[:2])})" for f, _, r in ranked) + " (fm suspects, fm whyred)"
            if ranked else None)


def cmd_suspects(args):
    import fmcli
    import fminstr
    p = fmcli.resolve(args)
    text = fminstr._input(args.file)
    ranked = board(p, text)[:args.top]
    fmcli.out(args, {"suspects": [{"path": f, "score": round(s, 2), "reasons": r} for f, s, r in ranked]},
              ("Suspects (stack, change since the task started, test links, edit recency):\n"
               + "\n".join(f"  {i}. {f} — {'; '.join(r)}" for i, (f, _, r) in enumerate(ranked, 1)))
              if ranked else "No suspects: no repo frame, changed file or linked test in that output.")


# ---------------------------------------------------------------- whyred

def _units(diff):
    """The diff split into hunks: [(file header, hunk)]; a new, deleted or binary file is one unit."""
    out = []
    for block in re.split(r"(?m)^(?=diff --git )", diff):
        if not block.startswith("diff --git"):
            continue
        head, sep, body = block.partition("\n@@")
        if not sep or re.search(r"(?m)^(new|deleted) file mode|^Binary files", head):
            out.append((block, ""))
            continue
        for h in re.split(r"(?m)^(?=@@)", "@@" + body):
            if h.strip():
                out.append((head + "\n", h))
    return out


def _patch(units):
    text, last = "", None
    for head, hunk in units:
        text += ("" if head == last and hunk else head) + hunk
        last = head
    return text


def cmd_whyred(args):
    import fmcli
    p = fmcli.resolve(args)
    base, _ = _base(p)
    diff = c.task_diff(p.root, base)
    units = _units(diff or "")
    if not units:
        raise fmcli.UsageError("nothing changed since the task started: no delta to debug")
    work = tempfile.mkdtemp(prefix="fm-whyred-")
    runs = [0]
    try:
        tar = subprocess.run(["git", "-C", p.root, "archive", base], capture_output=True)
        subprocess.run(["tar", "-x", "-C", work], input=tar.stdout, check=True)
        git = ["git", "-C", work, "-c", "user.name=fm", "-c", "user.email=fm@localhost"]
        subprocess.run([*git, "init", "-q"], check=True)
        subprocess.run([*git, "add", "-A"], check=True)
        subprocess.run([*git, "commit", "-qm", "base", "--allow-empty"], check=True)

        def red(subset):
            subprocess.run([*git, "checkout", "-q", "--", "."], capture_output=True)
            subprocess.run([*git, "clean", "-fdq"], capture_output=True)
            if subset:
                ap = subprocess.run([*git, "apply", "--whitespace=nowarn", "-"], input=_patch(subset).encode(),
                                    capture_output=True)
                if ap.returncode:
                    return False  # these hunks don't apply without the others: not a candidate
            runs[0] += 1
            return c.run_command(work, args.cmd, args.timeout)[0] != 0
        if red([]):
            return fmcli.out(args, {"red_at_base": True}, f"`{args.cmd}` fails on the task's start tree too: the "
                                                          f"failure isn't from this change (fm sentinel --bisect looks "
                                                          f"at commits).")
        if not red(units):
            return fmcli.out(args, {"red": False}, f"`{args.cmd}` passes with the whole change applied in a clean "
                                                   f"copy: the failure depends on something outside the diff "
                                                   f"(untracked state, the environment, flakiness).")
        found = _ddmin(units, red, runs)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    files = sorted({re.search(r"diff --git a/(\S+)", h).group(1) for h, _ in found})
    text = (f"Why red: `{args.cmd}` passes on the task's start tree and fails with its {len(units)} hunk(s) of change "
            f"({runs[0]} runs{', budget spent: not minimal' if runs[0] >= MAX_RUNS else ''}).\n"
            f"Minimal failing change ({len(found)} hunk(s) in {', '.join(files)}):\n"
            + "\n".join(_show(h, k) for h, k in found))
    fmcli.out(args, {"hunks": len(units), "minimal": [_show(h, k) for h, k in found], "runs": runs[0]}, text)
    return 1


def _show(head, hunk):
    name = re.search(r"diff --git a/(\S+)", head).group(1)
    lines = [ln for ln in (hunk or head).splitlines() if ln[:1] in "+-" and not ln.startswith(("+++", "---"))]
    return f"  {name} {(hunk.splitlines() or ['(whole file)'])[0][:60]}\n" + "\n".join(f"    {c.fit(ln, 150)}"
                                                                                       for ln in lines[:12])


def _ddmin(units, red, runs):
    """Zeller's ddmin: a 1-minimal subset of units that is still red, within MAX_RUNS runs."""
    n = 2
    while len(units) >= 2 and runs[0] < MAX_RUNS:
        size = -(-len(units) // n)
        chunks = [units[i:i + size] for i in range(0, len(units), size)]
        for ch in chunks:
            if runs[0] < MAX_RUNS and red(ch):
                units, n = ch, 2
                break
        else:
            for ch in chunks:
                rest = [u for u in units if u not in ch]
                if len(chunks) > 2 and runs[0] < MAX_RUNS and red(rest):
                    units, n = rest, max(n - 1, 2)
                    break
            else:
                if n >= len(units):
                    break
                n = min(len(units), 2 * n)
    return units


# ---------------------------------------------------------------- record

_RECORDER = '''import atexit, json, os, reprlib, sys, time
_root, _out, _rows = os.environ.get("FOREMAN_RECORD_ROOT", ""), os.environ.get("FOREMAN_RECORD_OUT", ""), []
if _root and _out and hasattr(sys, "monitoring"):
    try:
        _r = reprlib.Repr()
        _r.maxstring = _r.maxother = 80
        _M = sys.monitoring
        _M.use_tool_id(4, "foreman-record")

        def _unwind(code, offset, exc):
            f = code.co_filename
            if not f.startswith(_root) or "/." in f[len(_root):] or "site-packages" in f:
                return
            fr = sys._getframe(1)
            _rows.append({"file": f[len(_root):].lstrip("/"), "line": fr.f_lineno, "function": code.co_name,
                          "error": (type(exc).__name__ + ": " + str(exc))[:200], "t": time.time(),
                          "locals": {k: _r.repr(v) for k, v in list(fr.f_locals.items())[:20] if not k.startswith("__")}})
            del _rows[:-50]
        _M.register_callback(4, _M.events.PY_UNWIND, _unwind)
        _M.set_events(4, _M.events.PY_UNWIND)

        def _save():
            if _rows:
                with open(os.path.join(_out, str(os.getpid()) + ".json"), "w") as fh:
                    json.dump(_rows, fh)
        atexit.register(_save)
    except Exception:
        pass
'''


def cmd_record(args):
    """Rerun a command with the flight recorder on: the locals of the repo frames its exceptions unwound through.
    ponytail: our sitecustomize shadows a project's own one for this run; handled exceptions are recorded too, so the
    newest few are shown."""
    import fmcli
    p = fmcli.resolve(args)
    if sys.version_info < (3, 12):
        raise fmcli.UsageError("fm record needs Python 3.12+ (sys.monitoring)")
    work = tempfile.mkdtemp(prefix="fm-record-")
    try:
        with open(os.path.join(work, "sitecustomize.py"), "w") as f:
            f.write(_RECORDER)
        env = dict(os.environ, FOREMAN_RECORD_ROOT=p.root.rstrip("/") + "/", FOREMAN_RECORD_OUT=work,
                   PYTHONPATH=os.pathsep.join(filter(None, [work, os.environ.get("PYTHONPATH")])))
        code, output = c.run_command(p.root, args.cmd, args.timeout, env=env)
        rows = []
        for n in os.listdir(work):
            if n.endswith(".json"):
                with open(os.path.join(work, n)) as f:
                    rows += json.load(f)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    rows = sorted(rows, key=lambda r: r["t"])[-args.top:]
    text = (f"`{args.cmd}` → {c.run_result(code, output)}\n"
            + ("Where the exceptions unwound (newest last):\n" + "\n".join(
                f"  {r['file']}:{r['line']} in {r['function']} — {r['error']}\n    "
                + ", ".join(f"{k} = {v}" for k, v in r["locals"].items()) for r in rows)
               if rows else "No exception unwound through a repo frame (not Python, or nothing raised)."))
    fmcli.out(args, c.redact_obj({"exit": code, "unwinds": rows}), c.redact(text))  # locals can hold credentials
    return 1 if code else 0
