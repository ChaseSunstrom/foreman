"""T-0705 (Frontier 05, first slice): ambient verification. After an edit, the affected tests (fm check --affected's
selection) run in a detached process, out of the model's turns. Only a flip reaches the model — passing tests that now
fail, or failing ones that pass again — as one note on its next tool call; a passing run is the current step's
evidence. Opt-in per project (fm check ambient on); skipped on a strained host; nothing leaves the machine."""
import json
import os
import re
import subprocess

import fmcore as c

RERUNS = 3  # edits that land during a run trigger at most this many reruns, then the next edit starts a new one
RED_STEP = re.compile(r"(?i)\b(fail|red\b|reproduc|repro\b)")  # a step that wants a red run, which a pass won't verify


def _dir(p):
    d = os.path.join(p.dir, "ambient")
    os.makedirs(d, exist_ok=True)
    return d


def after_edit(p, path):
    """The PostToolUse hook's call after an edit: start a run, or mark the running one dirty so it runs again."""
    if not c.read_meta(p).get("ambient") or not path.startswith(p.root.rstrip("/") + "/") or c.host_strain():
        return
    if os.environ.get("FOREMAN_AMBIENT_SYNC"):  # tests: inline, so the result is there when the hook returns
        return run(p)
    if os.environ.get("FOREMAN_NO_BACKGROUND"):
        return
    if _running(p):
        open(os.path.join(_dir(p), "dirty"), "w").close()
        return
    subprocess.Popen([os.path.join(c.PLUGIN_ROOT, "bin", "fm"), "check", "ambient", "run"], cwd=p.root,
                     stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                     start_new_session=True)


def _running(p):
    try:
        with open(os.path.join(_dir(p), "run.pid")) as f:
            os.kill(int(f.read().strip()), 0)
        return True
    except (OSError, ValueError):
        return False


def run(p):
    """Run the affected tests until no edit landed meanwhile (at most RERUNS more times); record flips and evidence."""
    import fmcli
    d = _dir(p)
    pid = os.path.join(d, "run.pid")
    try:
        fd = os.open(pid, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        if _running(p):
            return
        os.unlink(pid)  # a run that died left it
        fd = os.open(pid, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    try:
        os.write(fd, str(os.getpid()).encode())
        os.close(fd)
        for _ in range(1 + RERUNS):
            try:
                os.unlink(os.path.join(d, "dirty"))
            except OSError:
                pass
            cmd, tests, _ = fmcli.affected(p)
            if not cmd:  # an edit that undid the change selects nothing; a failing last run still needs its answer
                cmd, tests = _last_failing(p)
            if cmd:
                code, output = c.run_command(p.root, cmd, 600)
                _record(p, cmd, tests, code, output)
            if not os.path.exists(os.path.join(d, "dirty")):
                break
    except Exception as e:  # never a crash in a detached run: one line in the folder says why
        c.write_atomic(os.path.join(d, "error.txt"), f"{type(e).__name__}: {e}\n")
    finally:
        try:
            os.unlink(pid)
        except OSError:
            pass


def _last_failing(p):
    try:
        with open(os.path.join(_dir(p), "last.json")) as f:
            last = json.load(f)
    except (OSError, ValueError):
        return None, []
    return (last.get("cmd"), last.get("tests") or []) if last.get("exit") else (None, [])


def _record(p, cmd, tests, code, output):
    d = _dir(p)
    last = os.path.join(d, "last.json")
    try:
        with open(last) as f:
            prev = json.load(f).get("exit")
    except (OSError, ValueError):
        prev = None
    result = c.run_result(code, c.redact(output))
    c.write_atomic(last, json.dumps({"cmd": cmd, "tests": tests, "exit": code, "ts": c.now()}))
    names = ", ".join(os.path.basename(t) for t in tests[:6]) + (" …" if len(tests) > 6 else "")
    if code and (prev is None or not prev):
        text = (f"Ambient tests: ✗ the affected tests now fail after your last edit ({names}): {c.fit(cmd, 160)} → "
                f"{c.fit(result, 300)}")
    elif not code and prev:
        text = f"Ambient tests: ✓ the affected tests pass again ({names})."
    else:
        text = None
    if text:
        c.write_atomic(os.path.join(d, "note.json"), json.dumps({"text": text, "ts": c.now()}))
    act = c.active_brief(c.load_briefs(p), p.lane)
    cur = act.current_step() if act and not code else None
    if cur and not act.has_evidence(step=cur.n) and not RED_STEP.search(cur.text):
        with c.lock(p.dir):
            b = c.find_brief(p, act.id)
            b.add_evidence(cmd, result, step=cur.n, tree=c.worktree_id(p.root), ran=True)
            c.save_brief(p, b)
            c.log_event(p, "evidence", task=b.id, data={"step": cur.n, "cmd": cmd[:200], "auto": "ambient"})
    c.log_event(p, "ambient_run", task=act.id if act else None, data={"tests": len(tests), "exit": code,
                                                                       "flip": bool(text)})


def note(p):
    """The flip waiting for the model, once: the PreToolUse hook's note, then it's gone."""
    path = os.path.join(p.dir, "ambient", "note.json")
    try:
        with open(path) as f:
            text = json.load(f).get("text")
        os.unlink(path)
    except (OSError, ValueError):
        return None
    return text
