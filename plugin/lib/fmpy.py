"""fmpy (T-0368): fm and every hook start with `env python3`; when that one is below Foreman's floor (JARVIS: 3.11.2,
where argparse drops `fm task evidence ID --step N CMD RESULT`), re-run under a supported interpreter found on this
machine. The first old-Python call searches once and saves the answer in state/python ("none" when there is none);
`fm doctor` searches again. Standard library only, and syntax old interpreters still parse."""
import glob
import os
import subprocess
import sys

NAMES = ("python3.14", "python3.13", "python3.12")


def ok(v):
    """3.12.7+, but not 3.13.0 (T-0319: argparse before 3.12.7 and in 3.13.0 drops trailing positionals)."""
    return tuple(v[:3]) >= (3, 12, 7) and tuple(v[:3]) != (3, 13, 0)


def saved_path():
    home = os.environ.get("FOREMAN_HOME") or os.path.join(os.path.expanduser("~"), ".claude", "foreman")
    return os.path.join(home, "state", "python")


def _read():
    """The saved answer: a path, "none", or None when there is no trustworthy file. It picks the interpreter the
    guard runs on, so a file someone else owns or can write is ignored."""
    path = saved_path()
    try:
        st = os.lstat(path)
        if not os.path.isfile(path) or os.path.islink(path) or st.st_uid != os.getuid() or st.st_mode & 0o022:
            return None
        with open(path, encoding="utf-8") as f:
            return f.read().strip() or None
    except OSError:
        return None


def find():
    """A supported interpreter on this machine, or None: versioned names on PATH and in ~/.local/bin, then uv's."""
    dirs = os.environ.get("PATH", "").split(os.pathsep) + [os.path.join(os.path.expanduser("~"), ".local", "bin")]
    cands = [os.path.join(d, n) for n in NAMES for d in dirs if d]
    cands += sorted(glob.glob(os.path.join(os.path.expanduser("~"), ".local", "share", "uv", "python",
                                           "cpython-3.1[2-9]*", "bin", "python3.1[2-9]")), reverse=True)
    seen = set()
    for exe in cands:
        real = os.path.realpath(exe)
        if real in seen or not os.access(exe, os.X_OK):
            continue
        seen.add(real)
        try:
            out = subprocess.run([exe, "-c", "import sys; print(*sys.version_info[:3])"], capture_output=True,
                                 text=True, timeout=10).stdout.split()
            if ok(tuple(int(x) for x in out)):
                return exe
        except (OSError, ValueError, subprocess.SubprocessError):
            continue
    return None


def _save(answer):
    path = saved_path()
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = f"{path}.{os.getpid()}"
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(answer + "\n")
        os.replace(tmp, path)
    except OSError:
        pass


def refresh():
    """Search again and save the answer (fm doctor): the interpreter, or None."""
    exe = find()
    _save(exe or "none")
    return exe


def target(v):
    """The interpreter to re-run under, or None: only below the floor, and never the one already running."""
    if ok(v) or os.environ.get("FOREMAN_PY_CHILD"):  # the child it started never starts another
        return None
    exe = _read()
    if exe is None and not os.path.lexists(saved_path()):
        exe = refresh() or "none"
    if not exe or exe == "none" or not os.access(exe, os.X_OK):
        return None
    return None if os.path.realpath(exe) == os.path.realpath(sys.executable) else exe


def reexec():
    """Call first in an entry point, before stdin is read: re-runs this process under a supported Python if needed."""
    exe = target(sys.version_info)
    if exe:
        os.environ["FOREMAN_PY_CHILD"] = "1"
        os.execv(exe, [exe] + sys.argv)
