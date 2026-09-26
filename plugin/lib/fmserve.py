"""fm serve / fm run: Foreman working without a terminal open.

fm serve runs Claude Code Remote Control in a repo as a systemd user unit, so requests sent from claude.ai/code or
the Claude app keep getting worked (the project is put in full autonomy with drive on). Remote Control needs no TTY;
its output (which includes the session URL) is discarded, errors go to the journal. Restart=always with a
start-limit breaker keeps it up without hammering a login or usage problem, and a restart reconnects its sessions.

fm run works the queue in fresh `claude -p` sessions, one task per session (drive is scoped to it through
FOREMAN_DRIVE_TASK), so a long queue never runs in one ever-growing context.
"""
import fcntl
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


def status_lines():
    lines = []
    for slug, path in units().items():
        state = _systemctl("is-active", unit_name(slug), check=False).stdout.strip() or "unknown"
        root = re.search(r"^WorkingDirectory=(.*)$", _read(path) or "", re.M)
        p = c.project_by_slug(slug)
        work = ""
        if p:
            sd = c.state_dict(p)
            work = (f" · active {sd['active']['id']}" if sd["active"] else " · idle") + f" · queue {len(sd['queue'])}"
        lines.append(f"{slug}: {state} · {root.group(1).replace('%%', '%') if root else '?'}{work}")
        if state != "active" and p and c.read_meta(p).get("serve"):
            lines.append(f"  {slug} is still full autonomy with drive on: fm serve stop restores them")
        if state != "active":
            try:
                log = subprocess.run(["journalctl", "--user", "-u", unit_name(slug), "-n", "3", "--no-pager", "-o",
                                      "cat"], capture_output=True, text=True, timeout=30).stdout.strip()
            except (OSError, subprocess.SubprocessError):
                log = ""
            log = re.sub(r"https?://\S+", "<url>", c.redact(log))  # never show the session URL
            lines += [f"  {l}" for l in log.splitlines()[-3:]]
    return lines or ["No fm serve units."]


def cmd_serve(args):
    import fmcli
    action, rest = "start", list(args.args)
    if rest and rest[0] in ("start", "status", "stop"):
        action = rest.pop(0)
    if action == "status":
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
    briefs = c.load_briefs(p)
    meta = c.read_meta(p)
    pending, autonomy = c.pending_tasks(meta), meta.get("autonomy", "standard")
    act = c.active_brief(briefs)
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


def _prompt(p, b):
    nxt = c.next_action(b, "full", c.last_change(p, b.id))
    title = re.sub(r"[\x00-\x1f\"]", " ", b.title)[:200]  # task text is data: one quoted line
    return (f"Foreman worker (fm run): work task {b.id} (titled \"{title}\") until it is done, following the Foreman rules. "
            f"Autonomy is full: never ask; decide with your default and record it (fm decide). If it can't be "
            f"finished, record why with fm task block {b.id} \"<why>\". Next: {nxt}")


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
        sys.exit(1)

    if not 0 <= args.wait < float("inf"):
        raise fmcli.UsageError(f"--wait takes hours from 0 up, got {args.wait}")
    finished, skip, told, sessions = 0, set(), set(), {}
    budget, step = args.wait * 3600, WAIT_FIRST  # usage-limit waiting left for this run, and the next wait
    while finished < args.max:
        b = _next_runnable(p, skip, told)
        if not b:
            break
        before = _fingerprint(b)
        cmd = ["claude", "-p", _prompt(p, b)] + (["--permission-mode", args.permission_mode]
                                               if args.permission_mode else [])
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
            time.sleep(pause)
            continue
        if code != 0:
            fail(f"{b.id}: claude exited {code} (login or crash); stopping")
        step = WAIT_FIRST
        after = c.find_brief(p, b.id)
        if after.status == "done":
            finished += 1
            print(f"{b.id} done")
        elif after.status in ("blocked", "dropped", "deferred"):
            skip.add(b.id)
            print(f"{b.id} {after.status}")
        elif _fingerprint(after) == before:
            fail(f"{b.id}: no progress in a fresh session; stopping")
        else:
            sessions[b.id] = sessions.get(b.id, 0) + 1
            if sessions[b.id] >= SESSIONS_PER_TASK:
                fail(f"{b.id} still not done after {SESSIONS_PER_TASK} sessions; stopping")
    print(f"fm run: {finished} task{'s' if finished != 1 else ''} done"
          + ("; the queue has nothing else runnable" if finished < args.max else f"; stopped at --max {args.max}"))
