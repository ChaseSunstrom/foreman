"""fmpy (T-0368): fm and every hook start with `env python3`; when that one is below Sampo's floor (JARVIS: 3.11.2,
where argparse drops `fm task evidence ID --step N CMD RESULT`), re-run under a supported interpreter found on this
machine. The first old-Python call searches once and saves the answer in state/python ("none" when there is none);
`fm doctor` searches again. Standard library only, and syntax old interpreters still parse."""
import os
import sys

NAMES = ("python3.14", "python3.13", "python3.12")


def ok(v):
    """3.12.7+, but not 3.13.0 (T-0319: argparse before 3.12.7 and in 3.13.0 drops trailing positionals)."""
    return tuple(v[:3]) >= (3, 12, 7) and tuple(v[:3]) != (3, 13, 0)


def saved_path():
    home = os.environ.get("SAMPO_HOME") or os.environ.get("FOREMAN_HOME") or os.path.join(  # before core's mirror
        os.path.expanduser("~"), ".claude", "foreman")
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


def find(names=NAMES, uv="python3.1[2-9]"):
    """A supported interpreter on this machine, or None: versioned names on PATH and in ~/.local/bin, then uv's.
    names, uv: only these (T-1805: fm check --python 3.12 passes ("python3.12",), "python3.12")."""
    import glob  # T-2023: only a search, rare, pays for these
    import subprocess
    dirs = os.environ.get("PATH", "").split(os.pathsep) + [os.path.join(os.path.expanduser("~"), ".local", "bin")]
    cands = [os.path.join(d, n) for n in names for d in dirs if d]
    cands += sorted(glob.glob(os.path.join(os.path.expanduser("~"), ".local", "share", "uv", "python",
                                           "cpython-3.1[2-9]*", "bin", uv)), reverse=True)
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


def lane_reexec(me):
    """T-2843: run from inside a lane (a git worktree of this checkout), the main install's fm hands over to the lane's own
    plugin/bin/<same name>, so PLUGIN_ROOT is the lane (fm lib check lints its cards; writes land in it). Once (SAMPO_LANE_CHILD).
    No git call: the nearest `.git` above the cwd must be a file naming a worktrees/<x> folder of the .git dir beside this bin
    whose own `gitdir` file names that .git file back, and the lane, that file and the bin must be ours and not group/world-writable."""
    try:
        if os.environ.get("SAMPO_LANE_CHILD"):
            return
        me = os.path.realpath(me)
        git = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(me))), ".git")
        if not os.path.isdir(git):  # not the main checkout (a copy, a lane itself, the plugin cache)
            return
        d = os.path.realpath(os.getcwd())
        while not os.path.exists(os.path.join(d, ".git")):
            if os.path.dirname(d) == d:
                return
            d = os.path.dirname(d)
        link = os.path.join(d, ".git")
        if not os.path.isfile(link):
            return
        with open(link, encoding="utf-8") as f:
            line = f.readline(4096)
        if not line.startswith("gitdir:"):
            return
        # The folder's own text proves nothing (a tarball can say anything): the main repo's registry, which git writes
        # when it makes the worktree, must point back at this very .git file.
        gd = os.path.realpath(os.path.join(d, line[7:].strip()))
        if os.path.dirname(gd) != os.path.join(os.path.realpath(git), "worktrees") or not os.path.isdir(gd):
            return
        with open(os.path.join(gd, "gitdir"), encoding="utf-8") as f:
            back = f.readline(4096).strip()
        cand = os.path.join(d, "plugin", "bin", os.path.basename(me))
        if not back or os.path.realpath(os.path.join(gd, back)) != os.path.realpath(link) or not os.path.isfile(cand) \
                or os.path.realpath(cand) == me:
            return
        for p in (d, link, cand):  # ours alone: nobody else can swap what we are about to run
            st = os.stat(p)
            if st.st_uid != os.getuid() or st.st_mode & 0o022:
                return
        os.environ["SAMPO_LANE_CHILD"] = "1"
        sys.stderr.write("fm: running the lane's own plugin at %s\n" % d)
        sys.stderr.flush()
        os.execv(sys.executable, [sys.executable, cand] + sys.argv[1:])
    except Exception:  # fail closed: any doubt runs the main install as before
        return


def reexec():
    """Call first in an entry point, before stdin is read: re-runs this process under a supported Python if needed."""
    exe = target(sys.version_info)
    if exe:
        os.environ["FOREMAN_PY_CHILD"] = "1"
        os.execv(exe, [exe] + sys.argv)
