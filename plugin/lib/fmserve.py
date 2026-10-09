"""fm serve / fm run: Foreman working without a terminal open.

fm serve runs Claude Code Remote Control in a repo as a systemd user unit, so requests sent from claude.ai/code or
the Claude app keep getting worked (the project is put in full autonomy with drive on). Remote Control needs no TTY;
its output (which includes the session URL) is discarded, errors go to the journal. Restart=always with a
start-limit breaker keeps it up without hammering a login or usage problem, and a restart reconnects its sessions.

fm run works the queue in fresh `claude -p` sessions, one task per session (drive is scoped to it through
FOREMAN_DRIVE_TASK), so a long queue never runs in one ever-growing context.
"""
import fcntl
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import time

import fmcore as c

MARK = "# Managed by Foreman (fm serve); `fm serve stop` removes it"
HOME_TAG = "# foreman-home: "  # which Foreman install owns the unit (another install's units are left alone)
SESSIONS_PER_TASK = 3  # fresh sessions fm run gives one task before it stops
RESTART = {"burst": 5, "window_s": 600, "delay_s": 30}  # a login/usage failure stops after 5 tries, not forever
RUN_LOG_MAX = 1_000_000  # bytes; the run log rotates to .1 past this
# Claude Code's own usage-limit wording, matched on the last line a failed session printed
USAGE_LIMIT = re.compile(r"You've hit your|You've reached your|You're out of usage|out of usage|usage limit reached", re.I)
WAIT_FIRST, WAIT_STEP_MAX = 300, 3600  # seconds; a usage-limit wait doubles per hit in a row, capped per wait
FAILS_MAX = 2  # T-0434: failed sessions (fm run) or jobs (fm night) in a row before the breaker stops; never a retry
BEAT_SLACK = 600  # seconds past a heartbeat's expected next beat before fm doctor calls it stale


def unit_dir():
    base = os.environ.get("XDG_CONFIG_HOME") or os.path.join(os.path.expanduser("~"), ".config")
    return os.path.join(base, "systemd", "user")


def unit_name(slug):
    return f"foreman-serve-{slug}.service"


def trusted(root):
    """Claude Code's workspace trust for this repo root (Remote Control exits on an untrusted folder). Checked on the
    root itself: a trusted parent folder doesn't carry over into a separate repo."""
    try:
        with open(os.path.join(os.path.expanduser("~"), ".claude.json")) as f:
            projects = json.load(f).get("projects") or {}
    except (OSError, ValueError, AttributeError):
        return False
    return any(isinstance(v, dict) and v.get("hasTrustDialogAccepted") and os.path.realpath(k) == os.path.realpath(root)
               for k, v in projects.items())


def _arg(s):
    """One systemd command-line word: plain when safe, else quoted; % and $ never expand."""
    if re.fullmatch(r"[\w@+=:,./-]+", s):
        return s
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("%", "%%").replace("$", "$$") + '"'


def unit_text(p, mode):
    if re.search(r"[\x00-\x1f]", p.root):  # a newline would end its line and start a new unit directive
        raise c.PolicyError(f"fm serve can't run in a path with control characters: {p.root!r}")
    name = re.sub(r"[^\w .()-]", "", os.path.basename(p.root)) + " (foreman)"
    # env finds claude on the unit's PATH at every start, so a reinstall elsewhere doesn't strand the unit
    rc = [shutil.which("env") or "/usr/bin/env", "claude", "remote-control", "--name", name, "--spawn", "same-dir"]
    rc += ["--permission-mode", mode] if mode else []
    path = ":".join(d for d in os.environ.get("PATH", "").split(":") if not re.search(r"[\x00-\x1f]", d))
    path_env = path.replace("\\", "\\\\").replace('"', '\\"').replace("%", "%%")
    return "\n".join([
        MARK, f"{HOME_TAG}{c.foreman_home()}", "[Unit]", f"Description=Foreman serve: Claude Code Remote Control in {p.root.replace('%', '%%')}",
        f"StartLimitIntervalSec={RESTART['window_s']}", f"StartLimitBurst={RESTART['burst']}", "",
        "[Service]", "Type=simple", f"WorkingDirectory={p.root.replace('%', '%%')}",
        f'Environment="PATH={path_env}"',  # the session's tools (git, fm, language toolchains) as in your shell
        "ExecStart=" + " ".join(map(_arg, rc)),
        "StandardOutput=null", "StandardError=journal",
        "Restart=always", f"RestartSec={RESTART['delay_s']}", "",
        "[Install]", "WantedBy=default.target", ""])


def _systemctl(*args, check=True):
    try:
        r = subprocess.run(["systemctl", "--user", *args], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError) as e:
        raise c.PolicyError(f"fm serve needs systemd --user: {e}")
    if check and r.returncode != 0:
        raise c.PolicyError(f"systemctl --user {' '.join(args)} failed: {(r.stderr or r.stdout).strip()[:300]}")
    return r


def units():
    """{slug: unit path} for the units fm serve wrote."""
    out = {}
    d = unit_dir()
    for f in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        m = re.fullmatch(r"foreman-serve-(.+)\.service", f)
        text = _read(os.path.join(d, f)) or ""
        if m and MARK in text and f"\n{HOME_TAG}{c.foreman_home()}\n" in text:
            out[m.group(1)] = os.path.join(d, f)
    return out


def _read(path):
    try:
        with open(path) as f:
            return f.read()
    except OSError:
        return None


def _run_active(p):
    try:
        with open(os.path.join(p.dir, "run.lock"), "a") as f:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return False
    except BlockingIOError:
        return True


def start(p, mode=None):
    if _run_active(p):
        raise c.PolicyError(f"fm run is working {p.slug}'s queue; a second writer would collide. Let it finish first")
    if not trusted(p.root):
        raise c.PolicyError(f"Claude Code hasn't trusted {p.root} yet and Remote Control refuses untrusted folders: "
                            f"open claude there once and accept the trust dialog, then run fm serve again")
    meta = c.read_meta(p)
    mode = mode or ("default" if meta.get("sensitive") else None)
    os.makedirs(unit_dir(), exist_ok=True)
    c.write_atomic(os.path.join(unit_dir(), unit_name(p.slug)), unit_text(p, mode))
    _systemctl("daemon-reload")
    _systemctl("enable", "--now", unit_name(p.slug))
    lingering = _linger() or (_loginctl("enable-linger") is not None and _linger())
    with c.lock(p.dir):
        meta = c.read_meta(p)
        prev = meta.get("serve") or {"prev_autonomy": meta.get("autonomy", "standard"),
                                     "prev_drive": meta.get("drive", True)}
        meta.update(autonomy="full", drive=True, serve=dict(prev, unit=unit_name(p.slug), mode=mode, started=c.now()))
        c.write_meta(p, meta)
        c.log_event(p, "serve_start", data={"unit": unit_name(p.slug), "mode": mode, "linger": lingering})
        c.regen_views(p)
    return lingering


def _loginctl(*args):
    try:
        r = subprocess.run(["loginctl", *args], capture_output=True, text=True, timeout=30)
        return r.stdout.strip() if r.returncode == 0 else None
    except (OSError, subprocess.SubprocessError):
        return None


def _linger():
    """Whether this user's systemd instance (and so the unit) outlives their last login session."""
    user = os.environ.get("USER") or str(os.getuid())
    return _loginctl("show-user", user, "-p", "Linger", "--value") == "yes"


def stop(slug):
    """Stop and remove one unit and put the project's autonomy and drive back. Returns what it did."""
    done = []
    path = units().get(slug)
    if path:
        _systemctl("disable", "--now", unit_name(slug), check=False)
        os.remove(path)
        _systemctl("daemon-reload", check=False)
        done.append(f"stopped and removed {unit_name(slug)}")
    p = c.project_by_slug(slug)
    if p:
        with c.lock(p.dir):
            meta = c.read_meta(p)
            prev = meta.pop("serve", None)
            if prev:
                meta.update(autonomy=prev.get("prev_autonomy", "standard"), drive=prev.get("prev_drive", True))
                c.write_meta(p, meta)
                c.log_event(p, "serve_stop", data={"unit": unit_name(slug)})
                c.regen_views(p)
                done.append(f"{slug}: autonomy {meta['autonomy']}, drive {'on' if meta['drive'] else 'off'} again")
    return done


def stop_all():
    return [line for slug in units() for line in stop(slug)]


def states():
    """{slug: systemd state} for this install's fm serve units."""
    return {slug: _systemctl("is-active", unit_name(slug), check=False).stdout.strip() or "unknown" for slug in units()}


def status_rows():
    """T-0328: each fm serve unit as data (the desktop app's Remote Control panel): its project, state, folder, work
    and, when it isn't running, the last log lines (session URLs removed)."""
    rows = []
    for slug, path in units().items():
        state = _systemctl("is-active", unit_name(slug), check=False).stdout.strip() or "unknown"
        root = re.search(r"^WorkingDirectory=(.*)$", _read(path) or "", re.M)
        p = c.project_by_slug(slug)
        sd = c.state_dict(p) if p else None
        row = {"project": slug, "unit": unit_name(slug), "state": state,
               "root": root.group(1).replace("%%", "%") if root else None,
               "active": sd["active"]["id"] if sd and sd["active"] else None, "queue": len(sd["queue"]) if sd else 0,
               "serve_mode": bool(p and c.read_meta(p).get("serve")), "log": []}
        if state != "active":
            try:
                log = subprocess.run(["journalctl", "--user", "-u", unit_name(slug), "-n", "3", "--no-pager", "-o",
                                      "cat"], capture_output=True, text=True, timeout=30).stdout.strip()
            except (OSError, subprocess.SubprocessError):
                log = ""
            row["log"] = re.sub(r"https?://\S+", "<url>", c.redact(log)).splitlines()[-3:]  # never the session URL
        rows.append(row)
    return rows


def status_lines():
    lines = []
    for r in status_rows():
        work = "" if r["queue"] is None else (f" · active {r['active']}" if r["active"] else " · idle") + f" · queue {r['queue']}"
        lines.append(f"{r['project']}: {r['state']} · {r['root'] or '?'}{work}")
        if r["state"] != "active" and r["serve_mode"]:
            lines.append(f"  {r['project']} is still full autonomy with drive on: fm serve stop restores them")
        lines += [f"  {line}" for line in r["log"]]
    return lines or ["No fm serve units."]


def cmd_serve(args):
    import fmcli
    action, rest = "start", list(args.args)
    if rest and rest[0] in ("start", "status", "stop"):
        action = rest.pop(0)
    if action == "status":
        if getattr(args, "json", False):
            return print(json.dumps({"v": 1, "units": status_rows()}))
        return print("\n".join(status_lines()))
    if action == "stop" and args.all:
        return print("\n".join(stop_all()) or "No fm serve units.")
    if rest:
        p = c.find_project(os.path.abspath(rest[0]), create=True)
        if not p:
            raise fmcli.UsageError(f"{rest[0]} isn't a Foreman project (run fm init there)")
    else:
        p = fmcli.resolve(args)
    if action == "stop":
        return print("\n".join(stop(p.slug)) or f"fm serve isn't running for {p.slug}.")
    lingering = start(p, args.permission_mode)
    print(f"Serving {p.root}: Claude Code Remote Control runs under {unit_name(p.slug)}, autonomy full, drive on. "
          f"Open it from claude.ai/code or the Claude app and send requests there.\n"
          + ("It survives logout and reboot (linger is on).\n" if lingering else
             "Warning: linger is off and couldn't be turned on, so the unit stops when you log out; an admin can run "
             f"`loginctl enable-linger {os.environ.get('USER') or os.getuid()}`.\n")
          + "Status: fm serve status · Stop: fm serve stop")


# ---------------------------------------------------------------- fm run

def _fingerprint(b):
    return (b.status, sum(s.done for s in b.steps()), sum(a.checked for a in b.acceptance()), len(b.audits()),
            b.section("Verification evidence").count("\n- "))


def _next_runnable(p, skip, told):
    briefs = c.lane_view(c.load_briefs(p), p.lane)  # T-0134: never another lane's task
    meta = c.read_meta(p)
    pending, autonomy = c.pending_tasks(meta), meta.get("autonomy", "standard")
    act = c.active_brief(briefs, p.lane)
    for b in ([act] if act else []) + c.order_queue(briefs)[0]:
        if b.id in skip:
            continue
        why = c.waits_on_user(b, pending, autonomy)
        if why:
            if b.id not in told:
                told.add(b.id)
                print(f"{b.id} waits on the user ({why}); skipped")
            continue
        return b
    return None


PARALLEL_MAX = 3  # T-0167: lanes at once at most (each is a full session: usage adds up)
FM_BIN = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bin", "fm")


def _fm(cwd, *args, timeout=600):
    return subprocess.run([sys.executable, FM_BIN, *args], cwd=cwd, capture_output=True, text=True, timeout=timeout)


def _literal(glob):
    """A scope's literal part, normalised: ./a, a//b and a/ name what a, a/b and a name (T-0167 review)."""
    lit = re.split(r"[*?\[{]", glob)[0]
    norm = os.path.normpath(lit) if lit else ""
    return "" if norm == "." else norm


def _overlap(a, b):
    """Two scope globs might name the same file (conservative: one's literal part starts the other's)."""
    x, y = _literal(a), _literal(b)
    return x.startswith(y) or y.startswith(x)


def _pairs(p):
    """T-0445: fm map's co-change pairs ({file: [files that nearly always change with it]}); {} without a map."""
    try:
        import fmmap
        return fmmap.load(p).get("pairs") or {}
    except Exception:  # no map is no widening: scopes alone, as before
        return {}


def _footprint(scopes, pairs):
    """T-0445: what a task will touch: its scopes plus each literal file's co-change companions."""
    return list(scopes) + [f for s in scopes for f in pairs.get(_literal(s), [])]


def _batch(p, head, skip, n):
    """T-0167: head plus queued tasks that can't collide with it or each other: S or M, planned, explicit scopes that
    are pairwise disjoint, nothing unfinished they depend on, nothing waiting on the user. One task: run as before."""
    briefs = c.lane_view(c.load_briefs(p), p.lane)
    by_id, meta = {b.id: b for b in c.load_briefs(p)}, c.read_meta(p)
    pending, autonomy = c.pending_tasks(meta), meta.get("autonomy", "standard")

    def free(b):
        return (b.tier in ("S", "M") and b.status == "planned" and b.meta.get("scope") and b.id not in skip
                and not c.waits_on_user(b, pending, autonomy)
                and all(d in by_id and by_id[d].status in c.CLOSED for d in c._deps(b)))  # T-0383: inferred too
    if n < 2 or not free(head):
        return [head]
    batch, pairs = [head], _pairs(p)
    group = lambda b: b.meta.get("group")  # T-0445: fm relate's groups are related work: one at a time
    for b in c.order_queue(briefs)[0]:
        if len(batch) < n and b.id != head.id and free(b) and not any(
                group(b) and group(b) == group(x) for x in batch) and not any(
                _overlap(g, h) for x in batch for g in _footprint(x.meta["scope"], pairs)
                for h in _footprint(b.meta["scope"], pairs)):
            batch.append(b)
    return batch


def _claude_cmd(p, b, args, models):
    model = models.get(b.tier)
    return ["claude", "-p", _prompt(p, b)] + (["--permission-mode", args.permission_mode] if args.permission_mode
                                              else []) + (["--model", model] if model else [])


def _run_lanes(p, batch, args, models, log):
    """A fresh session per task, each in its own lane (fm lane new), all at once; waits for every one (output to
    files, so no pipe fills while another is read). {id: (lane path, exit code or None on timeout, output)}; a task
    whose lane couldn't be made is {id: (None, None, why)}."""
    import signal
    import tempfile
    runs, lanes, results = {}, {}, {}
    try:
        for b in batch:
            made = _fm(p.root, "lane", "new", b.id, "--json")
            if made.returncode:
                results[b.id] = (None, None, made.stderr.strip()[:200])
                continue
            path = lanes[b.id] = json.loads(made.stdout)["path"]
            out = tempfile.TemporaryFile("w+", errors="replace")
            proc = subprocess.Popen(_claude_cmd(p, b, args, models), cwd=path, stdout=out, stderr=subprocess.STDOUT,
                                    env=dict(os.environ, FOREMAN_DRIVE_TASK=b.id), text=True, start_new_session=True)
            runs[b.id] = (path, proc, out, time.monotonic())
        deadline = time.monotonic() + args.timeout * 60
        for tid, (path, proc, out, t0) in runs.items():
            try:
                code = proc.wait(timeout=max(1, deadline - time.monotonic()))
            except subprocess.TimeoutExpired:
                _stop(proc, signal)  # the whole process group: tools the session started go too
                code = None
            out.seek(0)
            text = out.read()
            with open(log, "a", encoding="utf-8") as f:
                f.write(f"== {c.now()} {tid} (lane {path}) exit {code}\n{c.redact(text)}\n")
            c.log_event(p, "run_session", task=tid, data={"lane": path, "minutes": round((time.monotonic() - t0) / 60, 1),
                                                           "parallel": len(runs)})
            results[tid] = (path, code, text)
    except BaseException:  # claude missing, interrupted, or a write failed (session audit): no session is left
        for _, proc, _, _ in runs.values():  # running unwatched (its own process group: Ctrl-C never reaches it),
            _stop(proc, signal)              # and a lane nobody worked in frees its task; one with work is kept
        for tid, path in lanes.items():
            if tid not in results and not _lane_has_work(p, path):
                _fm(p.root, "lane", "rm", tid)
        raise
    finally:
        for _, _, out, _ in runs.values():
            out.close()
    return results


def _stop(proc, signal):
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except OSError:
        proc.kill()
    proc.wait()


def _lane_has_work(p, path):
    """Anything uncommitted in the lane, or commits on it the main checkout's HEAD doesn't have (then it is kept)."""
    git = lambda root, *a: subprocess.run(["git", "-C", root, *a], capture_output=True, text=True, timeout=60)
    try:
        head = git(p.root, "rev-parse", "HEAD").stdout.strip()
        return bool(git(path, "status", "--porcelain").stdout.strip()
                    or git(path, "log", "--oneline", f"{head}..HEAD").stdout.strip())
    except (OSError, subprocess.SubprocessError):
        return True


def _integrate(p, tid, path):
    """One finished lane into the main checkout, serially: rebase it on the main branch, run the gates there, then a
    fast-forward and fm lane rm. Any doubt keeps the lane and its branch, and says why."""
    try:
        return _integrate_lane(p, tid, path)
    except (OSError, subprocess.SubprocessError) as e:  # a slow gate or git: keep it, finish the others
        try:  # never left half-rebased
            subprocess.run(["git", "-C", path, "rebase", "--abort"], capture_output=True, timeout=60)
        except (OSError, subprocess.SubprocessError):
            pass
        return f"kept in {path}: {type(e).__name__} while integrating ({str(e)[:120]})"


def _main_moved(git, root, branch):
    """Why the main checkout can't take a fast-forward of branch now, or ''."""
    now = git(root, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    if not now or now == "HEAD":
        return "the main checkout isn't on a branch"
    if branch and now != branch:
        return f"the main checkout moved from {branch} to {now}"
    if git(root, "status", "--porcelain", "--untracked-files=no").stdout.strip():
        return "the main checkout has uncommitted changes"
    return ""


def _integrate_lane(p, tid, path):
    git = lambda root, *a: subprocess.run(["git", "-C", root, *a], capture_output=True, text=True, timeout=600)
    why = _main_moved(git, p.root, "")
    if why:
        return f"kept in {path}: {why}"
    branch = git(p.root, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    if not git(path, "log", "--oneline", f"{branch}..HEAD").stdout.strip():
        _fm(p.root, "lane", "rm", tid)
        return "nothing to merge"
    rebase = git(path, "rebase", "-q", branch)
    if rebase.returncode:
        git(path, "rebase", "--abort")
        why = (rebase.stderr.strip().splitlines() or ["conflicts"])[-1][:160]
        return f"kept in {path}: rebasing on {branch} failed ({why})"
    if c.read_meta(p).get("checks") and _fm(path, "check", timeout=3600).returncode:
        return f"kept in {path}: the gates failed after rebasing on {branch}"
    why = _main_moved(git, p.root, branch)  # session audit: the gates can take an hour; look again right before
    if why:
        return f"kept in {path}: {why} while the gates ran"
    if git(p.root, "merge", "-q", "--ff-only", f"foreman/{tid}").returncode:
        return f"kept in {path}: {branch} moved on; rebase the lane again"
    rm = _fm(p.root, "lane", "rm", tid)
    return f"merged into {branch}" + ("" if rm.returncode == 0 else f" (lane left: {rm.stderr.strip()[:120]})")


def _prompt(p, b):
    nxt = c.next_action(b, "full", c.last_change(p, b.id))
    title = re.sub(r"[\x00-\x1f\"]", " ", b.title)[:200]  # task text is data: one quoted line
    return (f"Foreman worker (fm run): work task {b.id} (titled \"{title}\") until it is done, following the Foreman rules. "
            f"Autonomy is full: never ask; decide with your default and record it (fm decide). If it can't be "
            f"finished, record why with fm task block {b.id} \"<why>\". Next: {nxt}")


def _models(p, args):
    """{tier: model} for fm run (T-0053): --models S=sonnet,L=opus (kept with --save), else the kept choice."""
    if not args.models:
        return c.read_meta(p).get("run_models") or {}
    try:
        models = {k.strip().upper(): v.strip() for k, v in (x.split("=", 1) for x in args.models.split(",") if x.strip())}
    except ValueError:
        models = {"?": ""}
    if not models or set(models) - {"S", "M", "L"} or not all(re.fullmatch(r"[\w.:-]+", v) for v in models.values()):
        raise c.PolicyError(f"--models takes TIER=MODEL pairs (tiers S, M, L), e.g. S=sonnet,L=opus; got {args.models!r}")
    if args.save:
        c.update_meta(p, run_models=models)
    return models


def _session_tokens(p, since):
    """Input-equivalent tokens the transcripts show for this project since a time (the session fm run just ran)."""
    try:
        import fmcost
        msgs, _ = fmcost.scan(fmcost.transcripts_dir(p.root), since[:19])
        return round(sum((u.get(k) or 0) * w for _, _, u in msgs for k, w in fmcost.WEIGHTS.items()))
    except (OSError, ValueError):
        return 0


def _notify(p, message):
    """The user's notify command (fm notify), with the message as $1: never part of the shell text."""
    cmd = c.read_meta(p).get("notify")
    if cmd:
        try:
            subprocess.run(["bash", "-c", cmd, "fm-notify", c.plain(message)[:300]], cwd=p.root, timeout=30,
                           stdin=subprocess.DEVNULL, capture_output=True)
        except (OSError, subprocess.SubprocessError):
            pass


def beat(p, name, secs, doing):
    """T-0434: fm run/night's heartbeat, in the project's state dir: what it does now and when the next beat is due
    (secs from now). Removed at a clean exit, so one left overdue means the run wedged or was killed."""
    path = os.path.join(p.dir, f"heartbeat-{name}.json")
    if path not in _BEATING:  # any exit Python sees (done, fail, an error) removes it; a kill can't
        import atexit
        _BEATING.add(path)
        atexit.register(_unbeat, path)
    c.write_atomic(path, json.dumps({"pid": os.getpid(), "at": c.now(), "doing": doing, "due": time.time() + secs}))


_BEATING = set()


def _unbeat(path):
    try:
        os.remove(path)
    except OSError:
        pass


def stale_beats(p, now=None):
    """[(name, heartbeat)] whose next beat is more than BEAT_SLACK overdue."""
    out = []
    for path in sorted(glob.glob(os.path.join(p.dir, "heartbeat-*.json"))):
        try:
            with open(path, encoding="utf-8") as f:
                hb = json.load(f)
            overdue = (now or time.time()) > float(hb["due"]) + BEAT_SLACK
        except (OSError, ValueError, KeyError, TypeError):
            continue
        if overdue:
            out.append((os.path.basename(path)[10:-5], hb))
    return out


def cmd_notify(args):
    """fm notify <cmd> (it gets the message as $1, e.g. notify-send Foreman "$1"), --off, or --test."""
    import fmcli
    p = fmcli.resolve(args)
    if args.off:
        c.update_meta(p, notify=None)
        return fmcli.out(args, {"notify": None}, "fm run notifications off.")
    if args.command:
        c.update_meta(p, notify=" ".join(args.command))
    cmd = c.read_meta(p).get("notify")
    if args.test and cmd:
        _notify(p, "Foreman test notification")
    fmcli.out(args, {"notify": cmd}, f"fm run notifies with: {cmd}" if cmd else "No notify command: fm notify '<cmd>'")


def cmd_run(args):
    import fmcli
    p = fmcli.resolve(args)
    if c.read_meta(p).get("serve"):
        raise c.PolicyError(f"fm serve is running Remote Control for {p.slug}; a second writer would collide. Send "
                            f"work to that session, or fm serve stop first")
    lockf = open(os.path.join(p.dir, "run.lock"), "w")
    try:
        fcntl.flock(lockf, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        raise fmcli.UsageError(f"another fm run is already working on {p.slug}")
    log = os.path.join(c.state_dir(), "logs", f"run-{p.slug}.log")
    os.makedirs(os.path.dirname(log), exist_ok=True)
    if os.path.exists(log) and os.path.getsize(log) > RUN_LOG_MAX:
        os.replace(log, log + ".1")

    def fail(msg):
        print(f"fm run: {msg} (log: {log})", file=sys.stderr)
        _notify(p, f"fm run stopped: {msg}")
        sys.exit(1)

    if not 0 <= args.wait < float("inf"):
        raise fmcli.UsageError(f"--wait takes hours from 0 up, got {args.wait}")
    models = _models(p, args)
    finished, skip, told, sessions, fails = 0, set(), set(), {}, 0  # fails: unfinished sessions in a row (T-0434)
    budget, step = args.wait * 3600, WAIT_FIRST  # usage-limit waiting left for this run, and the next wait
    while finished < args.max:
        b = _next_runnable(p, skip, told)
        if not b:
            break
        batch = _batch(p, b, skip, min(args.parallel, PARALLEL_MAX, args.max - finished))
        beat(p, "run", args.timeout * 60, " ".join(x.id for x in batch))
        if len(batch) > 1:  # T-0167: independent tasks at once, each in its lane, merged back one by one
            print(f"running {len(batch)} at once: {', '.join(x.id for x in batch)}", flush=True)
            limited = False
            try:
                ran = _run_lanes(p, batch, args, models, log)
            except FileNotFoundError:
                raise fmcli.UsageError("claude isn't on PATH")
            for tid, (path, code, text) in ran.items():
                if path is None:  # review: never retry a lane that can't be made, or the run loops forever
                    skip.add(tid)
                    print(f"{tid}: no lane ({text}); skipped this run", flush=True)
                    continue
                last = text.strip().splitlines()[-1:]
                hit = bool(code and last and USAGE_LIMIT.search(last[0]))
                limited = limited or hit
                after = c.find_brief(p, tid)
                if after.status == "done":
                    finished, fails = finished + 1, 0
                    beat(p, "run", 2 * 3600, f"{tid}: merging its lane")  # gates may take an hour
                    how = _integrate(p, tid, path)
                    print(f"{tid} done; {how}", flush=True)
                    _notify(p, f"{tid} done ({how}): {after.title[:80]}")
                else:
                    fails += not hit  # a usage limit is waited out, never a failure
                    skip.add(tid)  # not this run again; an empty lane frees the task for the next
                    freed = not _lane_has_work(p, path) and _fm(p.root, "lane", "rm", tid).returncode == 0
                    print(f"{tid} not finished in its lane ({after.status}, exit {code}); "
                          + ("lane removed, back in the queue" if freed else f"lane kept with its work: {path}"), flush=True)
            if fails >= FAILS_MAX:
                fail(f"{fails} sessions in a row ended unfinished; stopping")
            if limited:
                args.parallel = 1  # one at a time from here, which waits a usage limit out
                print("usage limit hit: no more lanes this run; one task at a time from here", flush=True)
            continue
        before = _fingerprint(b)
        model = models.get(b.tier)
        cmd = _claude_cmd(p, b, args, models)
        started, t0 = c.now(), time.monotonic()
        try:
            r = subprocess.run(cmd, cwd=p.root, env=dict(os.environ, FOREMAN_DRIVE_TASK=b.id), capture_output=True,
                               text=True, timeout=args.timeout * 60)
            streams, code = (r.stdout, r.stderr), r.returncode
            output = r.stdout + r.stderr
        except FileNotFoundError:
            raise fmcli.UsageError("claude isn't on PATH")
        except subprocess.TimeoutExpired as e:  # its output may be bytes even with text=True
            output = "".join(x.decode("utf-8", "replace") if isinstance(x, bytes) else x
                             for x in (e.stdout or "", e.stderr or ""))
            code = None
        with open(log, "a", encoding="utf-8") as f:
            f.write(f"== {c.now()} {b.id} exit {code}\n{c.redact(output)}\n")
        if code is None:
            fail(f"{b.id}: the session hit the {args.timeout}-minute limit; stopping")
        last = (streams[1].strip() or streams[0].strip()).splitlines()[-1:]  # a crash's own error wins over model text
        if code and last and USAGE_LIMIT.search(last[0]):
            if budget <= 0:
                fail(f"{b.id}: usage limit still in effect after waiting {args.wait:g} h (--wait); stopping")
            pause, step = min(step, budget), min(step * 2, WAIT_STEP_MAX)
            budget -= pause
            msg = f"{b.id}: usage limit; retrying at {time.strftime('%H:%M', time.localtime(time.time() + pause))}"
            print(msg, flush=True)
            with open(log, "a", encoding="utf-8") as f:
                f.write(f"== {c.now()} {msg}\n")
            beat(p, "run", pause, f"{b.id}: usage-limit wait")
            time.sleep(pause)
            continue
        if code != 0:
            fail(f"{b.id}: claude exited {code} (login or crash); stopping")
        step = WAIT_FIRST
        spent = _session_tokens(p, started)
        c.log_event(p, "run_session", task=b.id, data={"model": model or "default", "tokens": spent,
                                                        "minutes": round((time.monotonic() - t0) / 60, 1)})
        how = f" ({model or 'default model'}, {spent:,} input-equivalent tokens)" if spent else ""
        after = c.find_brief(p, b.id)
        if after.status == "done":
            finished, fails = finished + 1, 0
            print(f"{b.id} done{how}")
            _notify(p, f"{b.id} done: {b.title[:80]}")
        elif after.status in ("blocked", "dropped", "deferred"):
            skip.add(b.id)  # a block says why and the run moves on: it isn't a failure (a crash or no progress is)
            print(f"{b.id} {after.status}{how}")
            _notify(p, f"{b.id} {after.status}: {b.title[:80]}")
        elif _fingerprint(after) == before:
            fail(f"{b.id}: no progress in a fresh session; stopping")
        else:
            sessions[b.id] = sessions.get(b.id, 0) + 1
            if sessions[b.id] >= SESSIONS_PER_TASK:
                fail(f"{b.id} still not done after {SESSIONS_PER_TASK} sessions; stopping")
    _notify(p, f"fm run finished: {finished} task(s) done")
    print(f"fm run: {finished} task{'s' if finished != 1 else ''} done"
          + ("; the queue has nothing else runnable" if finished < args.max else f"; stopped at --max {args.max}"))
