"""fm serve / fm run: Foreman working without a terminal open.

fm serve runs Claude Code Remote Control in a repo under a systemd user unit, so requests sent from claude.ai/code or
the Claude app keep getting worked (the project is put in full autonomy with drive on). The unit starts tmux on a
private socket: Remote Control needs a TTY, and `fm serve attach` gives a way in. Restart=always with a start-limit
breaker keeps it up without hammering a login or usage problem.

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

import fmcore as c

MARK = "# Managed by Foreman (fm serve); `fm serve stop` removes it"
SESSIONS_PER_TASK = 3  # fresh sessions fm run gives one task before it stops


def unit_dir():
    base = os.environ.get("XDG_CONFIG_HOME") or os.path.join(os.path.expanduser("~"), ".config")
    return os.path.join(base, "systemd", "user")


def unit_name(slug):
    return f"foreman-serve-{slug}.service"


def tmux_socket(slug):
    return f"foreman-{slug}"


def trusted(path):
    """Claude Code's workspace trust (Remote Control exits on an untrusted folder); a trusted parent covers it."""
    try:
        with open(os.path.join(os.path.expanduser("~"), ".claude.json")) as f:
            projects = json.load(f).get("projects") or {}
    except (OSError, ValueError, AttributeError):
        return False
    ok = {os.path.realpath(k) for k, v in projects.items() if isinstance(v, dict) and v.get("hasTrustDialogAccepted")}
    d = os.path.realpath(path)
    while d not in ok:
        if os.path.dirname(d) == d:
            return False
        d = os.path.dirname(d)
    return True


def _arg(s):
    """One systemd command-line word: plain when safe, else quoted; % and $ never expand."""
    if re.fullmatch(r"[\w@+=:,./-]+", s):
        return s
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("%", "%%").replace("$", "$$") + '"'


def unit_text(p, mode):
    tmux = shutil.which("tmux") or "tmux"
    name = re.sub(r"[^\w .()-]", "", os.path.basename(p.root)) + " (foreman)"
    rc = [shutil.which("claude") or "claude", "remote-control", "--name", name, "--spawn", "same-dir"]
    start = [tmux, "-L", tmux_socket(p.slug), "new-session", "-d", "-s", "foreman", "-x", "200", "-y", "50",
             "-c", p.root] + rc + (["--permission-mode", mode] if mode else [])
    path_env = os.environ.get("PATH", "").replace("\\", "\\\\").replace('"', '\\"').replace("%", "%%")
    return "\n".join([
        MARK, "[Unit]", f"Description=Foreman serve: Claude Code Remote Control in {p.root.replace('%', '%%')}",
        "StartLimitIntervalSec=600", "StartLimitBurst=5", "",
        "[Service]", "Type=forking", f"WorkingDirectory={p.root.replace('%', '%%')}",
        f'Environment="PATH={path_env}"',  # the session's tools (git, fm, language toolchains) as in your shell
        "ExecStart=" + " ".join(map(_arg, start)),
        "ExecStop=" + " ".join(map(_arg, [tmux, "-L", tmux_socket(p.slug), "kill-server"])),
        "Restart=always", "RestartSec=30", "",
        "[Install]", "WantedBy=default.target", ""])


def _systemctl(*args, check=True):
    try:
        r = subprocess.run(["systemctl", "--user", *args], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError) as e:
        raise c.PolicyError(f"fm serve needs systemd --user: {e}")
    if check and r.returncode != 0:
        raise c.PolicyError(f"systemctl --user {' '.join(args)} failed: {(r.stderr or r.stdout).strip()[:300]}")
    return r


def _ours():
    """{slug: unit path} for the units fm serve wrote."""
    out = {}
    d = unit_dir()
    for f in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        m = re.fullmatch(r"foreman-serve-(.+)\.service", f)
        if m and MARK in (_read(os.path.join(d, f)) or ""):
            out[m.group(1)] = os.path.join(d, f)
    return out


def _read(path):
    try:
        with open(path) as f:
            return f.read()
    except OSError:
        return None


def start(p, mode=None):
    if not trusted(p.root):
        raise c.PolicyError(f"Claude Code hasn't trusted {p.root} yet and Remote Control refuses untrusted folders: "
                            f"open claude there once and accept the trust dialog, then run fm serve again")
    meta = c.read_meta(p)
    mode = mode or ("default" if meta.get("sensitive") else None)
    os.makedirs(unit_dir(), exist_ok=True)
    c.write_atomic(os.path.join(unit_dir(), unit_name(p.slug)), unit_text(p, mode))
    _systemctl("daemon-reload")
    _systemctl("enable", "--now", unit_name(p.slug))
    with c.lock(p.dir):
        meta = c.read_meta(p)
        prev = meta.get("serve") or {"prev_autonomy": meta.get("autonomy", "standard"),
                                     "prev_drive": meta.get("drive", True)}
        meta.update(autonomy="full", drive=True, serve=dict(prev, unit=unit_name(p.slug), mode=mode, started=c.now()))
        c.write_meta(p, meta)
        c.log_event(p, "serve_start", data={"unit": unit_name(p.slug), "mode": mode})
        c.regen_views(p)


def stop(slug):
    """Stop and remove one unit and put the project's autonomy and drive back. Returns what it did."""
    done = []
    path = _ours().get(slug)
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
    return [line for slug in _ours() for line in stop(slug)]


def status_lines():
    lines = []
    for slug, path in _ours().items():
        state = _systemctl("is-active", unit_name(slug), check=False).stdout.strip() or "unknown"
        root = re.search(r"^WorkingDirectory=(.*)$", _read(path) or "", re.M)
        p = c.project_by_slug(slug)
        work = ""
        if p:
            sd = c.state_dict(p)
            work = (f" · active {sd['active']['id']}" if sd["active"] else " · idle") + f" · queue {len(sd['queue'])}"
        lines.append(f"{slug}: {state} · {root.group(1).replace('%%', '%') if root else '?'}{work} · "
                     f"attach: tmux -L {tmux_socket(slug)} attach -t foreman")
    return lines or ["No fm serve units."]


def cmd_serve(args):
    import fmcli
    action, rest = "start", list(args.args)
    if rest and rest[0] in ("start", "status", "stop", "attach"):
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
    if action == "attach":
        return print(f"tmux -L {tmux_socket(p.slug)} attach -t foreman   (detach: Ctrl-b d; Ctrl-C there stops "
                     f"Remote Control and systemd restarts it)")
    if action == "stop":
        return print("\n".join(stop(p.slug)) or f"fm serve isn't running for {p.slug}.")
    start(p, args.permission_mode)
    print(f"Serving {p.root}: Claude Code Remote Control runs under {unit_name(p.slug)} (survives logout and reboot), "
          f"autonomy full, drive on. Open it from claude.ai/code or the Claude app and send requests there.\n"
          f"Status: fm serve status · Stop: fm serve stop · Attach: fm serve attach")


# ---------------------------------------------------------------- fm run

def _fingerprint(b):
    return (b.status, sum(s.done for s in b.steps()), sum(a.checked for a in b.acceptance()), len(b.audits()),
            b.section("Verification evidence").count("\n- "))


def _next_runnable(p, skip, told):
    briefs = c.load_briefs(p)
    meta = c.read_meta(p)
    pending = {a.get("task") for a in meta.get("pending_approvals") or [] if isinstance(a, dict)}
    autonomy = meta.get("autonomy", "standard")
    act = c.active_brief(briefs)
    for b in ([act] if act else []) + c.order_queue(briefs)[0]:
        if b.id in skip:
            continue
        if b.id in pending or c.needs_approval(b, autonomy):
            if b.id not in told:
                told.add(b.id)
                print(f"{b.id} waits on the user ({'pending approval' if b.id in pending else 'plan approval'}); "
                      f"skipped")
            continue
        return b
    return None


def _prompt(p, b):
    nxt = c.next_action(b, "full", c.last_change(p, b.id))
    return (f"Foreman worker (fm run): work task {b.id} ({b.title}) until it is done, following the Foreman rules. "
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
    if os.path.exists(log) and os.path.getsize(log) > 1_000_000:
        os.replace(log, log + ".1")

    def fail(msg):
        print(f"fm run: {msg} (log: {log})", file=sys.stderr)
        sys.exit(1)

    finished, skip, told, sessions = 0, set(), set(), {}
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
            output, code = r.stdout + r.stderr, r.returncode
        except FileNotFoundError:
            raise fmcli.UsageError("claude isn't on PATH")
        except subprocess.TimeoutExpired as e:
            out = e.stdout or ""  # bytes on some Pythons even with text=True
            output, code = out.decode("utf-8", "replace") if isinstance(out, bytes) else out, None
        with open(log, "a", encoding="utf-8") as f:
            f.write(f"== {c.now()} {b.id} exit {code}\n{c.redact(output)}\n")
        if code is None:
            fail(f"{b.id}: the session hit the {args.timeout}-minute limit; stopping")
        if code != 0:
            fail(f"{b.id}: claude exited {code} (usage limit, login or crash); stopping")
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
