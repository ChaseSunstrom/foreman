"""T-1553: the guard's oracle. A line runs in a throwaway bwrap sandbox (read-only root, no network, its own /tmp and
/run, the home folder an empty tmpfs, memory and file size capped) whose PATH holds nothing, so bash's
command_not_found_handle records each program the shell would start, with the argv it really built, instead of running
it. Each line runs twice, the recorded programs failing and then succeeding, so both sides of `a || b` and an if/else
are seen. Judged alone, every recorded command must pass the guard wherever the whole line passed; one that doesn't is
a line the guard misread. A sandbox that didn't start, or a guard that raised, is "unable", never agreement (T-1517).
Optional: with no bwrap there is no oracle (nothing is installed).
ponytail: a program the line reaches without a PATH lookup isn't recorded (it runs for real, inside the sandbox only):
an absolute or ./ path, a PATH it sets itself, command -p, hash -p, exec, or a nested bash -c; a fork bomb is cut only
by the timeout. Recorded commands are judged alone in the folder the line's cd's reached (pushd/popd aren't followed):
a redirection or an env prefix isn't carried."""
import os
import re
import shlex
import shutil
import subprocess
import tempfile
import warnings

TIMEOUT = 10
# each program the shell would start: its argv, NUL-separated, in a file of its own named by the time it ran (bash
# line-buffers what it writes, so records that share one file come apart in a pipeline whose stages run at once); the
# handler and its settings are read-only so the line can't switch the recorder off
_SCRIPT = ('command_not_found_handle() { printf "%s\\0" "$ORACLE_PWD" "$@" > "$ORACLE_LOG/$EPOCHREALTIME.$BASHPID"; '
           # path helpers whose output steers what follows (d=$(mktemp -d) && cd "$d") run for real, in the sandbox
           'case $1 in mktemp|basename|dirname|realpath|readlink|date) PATH=/usr/bin:/bin "$@"; return;; esac; '
           'return "$ORACLE_STATUS"; }; '
           # the folder the line moved to, kept by path even where the sandbox lacks it (its home is empty)
           'cd() { local t; [ $# = 0 ] && t=$HOME; for t; do :; done; [ -z "$t" ] && return 0; '
           '[ "$t" = - ] && t=${OLDPWD:-$ORACLE_PWD}; '
           'case $t in /*) ;; *) t=$ORACLE_PWD/$t;; esac; ORACLE_PWD=$t; builtin cd "$t" 2>/dev/null; return 0; }; '
           'readonly -f command_not_found_handle cd; readonly ORACLE_LOG ORACLE_STATUS; '
           'ulimit -v 2097152; ulimit -f 102400; : > "$ORACLE_STARTED"; eval "$1"')
_RECORD = re.compile(r"\d+\.\d+\.\d+")


def sandbox():
    """The bwrap binary, or None: the oracle never runs a command outside a sandbox."""
    return shutil.which("bwrap")


def _records(folder):
    names = [n for n in os.listdir(folder) if _RECORD.fullmatch(n) and os.path.isfile(os.path.join(folder, n))]
    out = []
    for n in sorted(names, key=lambda n: (float(n.rsplit(".", 1)[0]), n)):
        with open(os.path.join(folder, n), "rb") as f:
            parts = [a.decode("utf-8", "replace") for a in f.read().split(b"\0")[:-1]]
        if len(parts) > 1:
            out.append((os.path.normpath(parts[0]), parts[1:]))
    return out


def _inside(path, base):
    return path.startswith(base.rstrip("/") + "/")


def _once(bw, cmd, cwd, home, status):
    """The records of one run with the recorded programs exiting with status, or None if the sandbox didn't start."""
    with tempfile.TemporaryDirectory(prefix="fm-oracle-") as t:
        log, empty, started = os.path.join(t, "log"), os.path.join(t, "empty"), os.path.join(t, "started")
        os.mkdir(empty)
        os.mkdir(log)
        argv = [bw, "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp", "--tmpfs", "/run",
                "--tmpfs", home, "--unshare-all", "--die-with-parent", "--new-session"]
        if os.path.isdir(cwd) and any(_inside(cwd, b) for b in (home, "/tmp", "/run")):
            argv += ["--ro-bind", cwd, cwd]  # the line's own folder, read-only, back over a tmpfs; never an ancestor
        argv += ["--bind", t, t, "--chdir", cwd if os.path.isdir(cwd) else "/",
                 "/usr/bin/env", "-i", f"PATH={empty}", f"HOME={home}", f"ORACLE_LOG={log}",
                 f"ORACLE_STATUS={status}", f"ORACLE_STARTED={started}", f"ORACLE_PWD={cwd}",
                 "/bin/bash", "--noprofile", "--norc", "-c", _SCRIPT, "oracle", cmd]
        try:
            subprocess.run(argv, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           timeout=TIMEOUT)
        except (subprocess.TimeoutExpired, OSError):
            pass  # what it recorded before the deadline still counts; one that never started is caught below
        return _records(log) if os.path.exists(started) else None


def ran(cmd, cwd=""):
    """The argv of each program the shell would start for cmd: ran_in without the folders."""
    got = ran_in(cmd, cwd)
    return None if got is None else [argv for _, argv in got]


def ran_in(cmd, cwd=""):
    """[(folder, argv)] for each program the shell would start for cmd, in order (a failing run's, then any new ones a
    succeeding run adds), the folder being where the line's cd's had taken it; run in the sandbox from cwd, with HOME
    the real home's path over an empty tmpfs. None without a sandbox or when it didn't start."""
    bw = sandbox()
    if not bw:
        return None
    home = os.path.expanduser("~")
    cwd = os.path.realpath(cwd or home)
    out = []
    for status in (1, 0):
        got = _once(bw, cmd, cwd, home, status)
        if got is None:
            return None
        out += [a for a in got if a not in out]
    return out


def _join(argv):
    """argv as a line, each argument quoted the plainest way the shell reads back the same (python -c "…'x'…" stays in
    double quotes, as people write it, not shlex's '"'"' splices): the oracle reports what runs, not a quoting style."""
    plain = re.compile(r'[$`"!]|\\[$`"\\\n]|\\\Z')  # what double quotes would still expand or escape
    return " ".join(f'"{a}"' if "'" in a and not plain.search(a) else shlex.quote(a) for a in argv)


def _guard():
    import fmguard
    return fmguard


def disagreements(cases, guard=None):
    """[{cmd, cwd, ran, verdict}] for each (cmd, cwd) the guard (default: Foreman's) lets through whole while a
    command the shell runs for it, judged alone by Foreman's guard, is refused; verdict "unable: …" where the sandbox
    didn't start or the guard raised. Judged as a hook judges: Python's path variables cleared (T-1599)."""
    import fmreplay
    real = _guard()
    guard = guard or real
    out = []
    py = {k: os.environ.pop(k) for k in getattr(real, "_PY_PATH_VARS", ()) if k in os.environ}
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)  # the guard parses Python inside commands
            for cmd, cwd in cases:
                where = fmreplay.resolve_cwd(cwd) if cwd else os.path.expanduser("~")
                ctx = fmreplay._ctx(where)
                try:
                    if guard.check("Bash", {"command": cmd}, ctx) is not None:
                        continue  # refused whole: nothing runs, nothing to compare
                    seen = ran_in(cmd, where)
                    if seen is None:
                        out.append({"cmd": cmd, "cwd": cwd, "ran": None, "verdict": "unable: the sandbox didn't start"})
                        continue
                    for at, argv in seen:
                        b = real.check("Bash", {"command": _join(argv)}, ctx if at == where else fmreplay._ctx(at))
                        if b is not None:
                            out.append({"cmd": cmd, "cwd": cwd, "ran": argv,
                                        "verdict": f"{b.category}: {b.detail}"[:200]})
                except Exception as e:  # noqa: BLE001 — the guard fails closed in the hook; here it is a finding
                    out.append({"cmd": cmd, "cwd": cwd, "ran": None,
                                "verdict": f"unable: the guard raised {type(e).__name__}"})
    finally:
        os.environ.update(py)
    return out
