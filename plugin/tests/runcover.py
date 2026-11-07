"""T-3593: run.py's coverage recorder. A .pth in the venv run.py starts each class with loads it in every Python of the
class's process tree, never from plugin/tests. It appends to the file RUNPY_COVER names the files under the folders
RUNPY_COVER_ROOTS names (the repo) that the process reads: "f PATH" for a module it runs or a file it opens, "s PATH"
for one it stats (exists, isdir, access), "d PATH" for a folder it lists (not the import system's own listings), and
"*" (the whole tree; with "g", git's HEAD and tags, when that child is git on the repo) when it starts a child it can't
follow: a Python without this hook or writing elsewhere (another interpreter, -S, another RUNPY_COVER), git on the
repo, a program working in the repo or given a path in it, or one that runs a python itself (a shell, env, bwrap)."""
import os
import sys

VAR, ROOTS_VAR = "RUNPY_COVER", "RUNPY_COVER_ROOTS"
PY = ""  # this venv's python: a child started with it records too
_ST = {"ctx": None, "seen": set(), "fd": -1, "ino": None, "out0": None, "rs": None, "roots": (), "roots0": ""}


def setup(py):
    """The process's start: what it was given still counts if the code under test clears its environment."""
    global PY
    PY = py
    _ST["out0"], _ST["roots0"] = os.environ.get(VAR), os.environ.get(ROOTS_VAR, "")
    sys.addaudithook(_hook)
    os.stat, os.lstat, os.access = _watch(os.stat), _watch(os.lstat), _watch(os.access)


def _watch(fn):
    """fn recording the repo path it is asked about ("s PATH"): stat, exists, isdir, access raise no audit event.
    The watched one stands in os.supports_* where fn does, so shutil.rmtree keeps its fd-based walk."""
    def watched(path, *args, **kw):
        try:
            if kw.get("dir_fd") is None and isinstance(p := os.fspath(path), (str, bytes)) and _inside(
                    p := os.fsdecode(p)):
                _put([f"s {os.path.abspath(p)}"])
        except Exception:  # an fd, or nothing to record: fn answers as ever
            pass
        return fn(path, *args, **kw)
    watched.__name__, watched.__qualname__, watched.__doc__ = fn.__name__, fn.__qualname__, fn.__doc__
    for group in (os.supports_fd, os.supports_dir_fd, os.supports_follow_symlinks, os.supports_effective_ids):
        if fn in group:
            group.add(watched)
    return watched


def _out():
    return os.environ.get(VAR) or _ST["out0"]


def _roots():
    r = os.environ.get(ROOTS_VAR, "")
    if r != _ST["rs"]:  # a nested run.py names its own repo: the one this process started for stays too
        _ST["rs"], _ST["roots"] = r, tuple({x for x in (r + os.pathsep + _ST["roots0"]).split(os.pathsep) if x})
    return _ST["roots"]


def _inside(path, cwd=None):
    """path (relative to cwd, else this process's) is in the repo; an absolute one never asks for a gone cwd."""
    return (os.path.normpath(path if os.path.isabs(path) else os.path.join(cwd or os.getcwd(), path))
            + os.sep).startswith(_roots())


def _fd(out):
    """The open record file and whether this process (a fork) or file is new; reopened when the code under test
    closed the descriptor or reused its number (os.closerange), so a line never lands in a file of its own."""
    ctx = (os.getpid(), out)
    if _ST["ctx"] == ctx:
        try:
            st = os.fstat(_ST["fd"])
            if (st.st_dev, st.st_ino) == _ST["ino"]:
                return _ST["fd"], False
        except OSError:
            pass
    fd = os.open(out, os.O_WRONLY | os.O_APPEND | os.O_CREAT | os.O_CLOEXEC, 0o600)
    st, new = os.fstat(fd), _ST["ctx"] != ctx
    _ST["ctx"], _ST["fd"], _ST["ino"] = ctx, fd, (st.st_dev, st.st_ino)
    if new:
        _ST["seen"] = set()
    return fd, new


def _put(lines):
    out = _out()
    if not out:
        return
    fd, new = _fd(out)
    if new:  # what the process already runs counts too (a fork server's preloaded modules)
        lines = [*lines, *(f"f {f}" for m in list(sys.modules.values())
                           if isinstance(f := getattr(m, "__file__", None), str) and os.path.isabs(f) and _inside(f))]
    new = [ln for ln in dict.fromkeys(lines) if ln not in _ST["seen"]]
    if new:  # no lock: two threads racing write a line twice at worst, never miss one
        os.write(fd, "".join(ln + "\n" for ln in new).encode("utf-8", "surrogateescape"))
        _ST["seen"].update(new)


def _python_follows(prog, argv, cwd, e):
    it = iter(argv[1:])
    for a in it:  # its options, up to the script, -c or -m
        if a in ("-X", "-W"):
            next(it, None)
        elif a.startswith(("-X", "-W")):
            continue
        elif a == "-" or not a.startswith("-") or a.startswith("--"):
            break
        elif "S" in a:  # -S: no site, so no .pth and no hook
            return False
        elif "c" in a or "m" in a:
            break
    return os.path.abspath(os.path.join(cwd, prog)) == PY and e.get(VAR) == _out()


def _which(name, path):
    import shutil  # here: its import costs ~10 ms, too much for every Python's start
    return shutil.which(name, path=path)


SEALED = ("bwrap", "docker", "podman", "firejail", "unshare", "chroot", "ssh", "sudo")  # another view of the files


def _shebang(prog, path):
    """The python a script's #! line runs (resolved on PATH for /usr/bin/env), else None."""
    try:
        with open(prog, "rb") as f:
            line = f.read(256).split(b"\n", 1)[0].decode()
    except (OSError, UnicodeDecodeError):
        return None
    words = line[2:].split() if line.startswith("#!") else []
    if words[:1] and os.path.basename(words[0]) == "env":
        words = [w for w in words[1:] if w != "-S"]
        words[:1] = [_which(words[0], path) or words[0]] if words else []
    return words[0] if words and os.path.basename(words[0]).startswith("python") else None


def _blind(prog, argv, cwd, env, wrapper=False):
    """Truthy when a child would read what no hook records ("g": git on the repo; a wrapper's own part: not judged by
    its working folder)."""
    e = os.environ if env is None else env
    path = e.get("PATH", os.defpath)
    if "/" not in prog:  # found on the child's PATH, as subprocess and exec find it
        prog = _which(prog, path) or prog
    if (py := _shebang(os.path.join(cwd, prog), path)):  # a python script run as a program: fm, the hook
        prog, argv = py, [py, os.path.join(cwd, prog), *argv[1:]]
    name = os.path.basename(prog)
    if name.startswith("python"):
        return not _python_follows(prog, argv, cwd, e)
    if name in SEALED:
        return True
    at = next((i for i, a in enumerate(argv[1:], 1) if os.path.abspath(os.path.join(cwd, a)) == PY), None)
    if at is not None:  # a wrapper (env, timeout, a claude stand-in) running this venv's python: that one records
        return _blind(prog, argv[:at], cwd, env, True) or not _python_follows(PY, argv[at:], cwd, e)
    if name == "git":
        where, it, sub = cwd, iter(argv[1:]), None
        for a in it:
            if a in ("-C", "--git-dir", "--work-tree"):
                where = os.path.join(where, next(it, ""))
            elif a.startswith(("--git-dir=", "--work-tree=")):
                where = os.path.join(where, a.split("=", 1)[1])
            elif a in ("-c", "--namespace", "--exec-path"):
                next(it, None)
            elif not a.startswith("-"):
                sub = a
                break
        cwd = where  # git reads its paths from there
        if sub not in ("init", "clone") and _inside(where) or any(_inside(v) for k in ("GIT_DIR", "GIT_WORK_TREE")
                                                                   if (v := e.get(k))):
            return "g"  # it reads the files and git's own state (HEAD, tags)
    elif _inside(cwd) and not wrapper:  # it may read the repo through its working folder (ls, make, grep -r)
        return True
    toks = [t.strip("'\"();|&<>=") for a in [prog, *argv] for t in a.split()]
    if name in ("sh", "bash", "dash", "zsh"):  # a command line: a python it runs must be this one, a program not ours
        for t in toks[1:]:
            w = _which(t, path) if t and "/" not in t else t
            if w and os.path.basename(w).startswith("python") and (os.path.abspath(os.path.join(cwd, w)) != PY
                                                                   or e.get(VAR) != _out()):
                return True
            if w and "/" not in t and _inside(w):
                return True
    elif any(os.path.basename(t).startswith("python") for t in toks[1:]):  # a python it runs another way
        return True
    return any(t and _inside(t, cwd) and os.path.exists(os.path.join(cwd, t)) for t in toks)


def _hook(ev, args):
    try:
        if ev == "exec":
            f = getattr(args[0], "co_filename", "")
            if f[:1] != "<" and _inside(f):
                _put([f"f {os.path.abspath(f)}"])
        elif ev in ("open", "sqlite3.connect", "cpython.run_file"):
            p = args[0]
            if isinstance(p, (str, bytes)) and _inside(p := os.fsdecode(p)) and p != _out() and (
                    os.path.isabs(p) or os.path.exists(p)):  # a missing relative name: likely a dir_fd's (rmtree)
                _put([f"f {os.path.abspath(p)}"])
        elif ev in ("os.listdir", "os.scandir"):
            p = "." if args[0] is None else args[0]
            if isinstance(p, (str, bytes)) and _inside(p := os.fsdecode(p)) and \
                    not sys._getframe(1).f_code.co_filename.startswith("<frozen importlib"):  # its path cache
                _put([f"d {os.path.abspath(p)}"])
        elif ev in ("subprocess.Popen", "os.exec", "os.posix_spawn"):
            if ev == "os.posix_spawn" and sys._getframe(1).f_code.co_filename.endswith("subprocess.py"):
                return  # its Popen event was judged
            exe, argv, cwd, env = args if ev == "subprocess.Popen" else (*args[:2], None, args[2])
            argv = [os.fsdecode(a) for a in argv] if isinstance(argv, (list, tuple)) else [os.fsdecode(argv)]
            cwd = os.fsdecode(cwd) if cwd else os.getcwd()
            if why := _blind(os.fsdecode(exe) if exe else argv[0], argv, cwd, env):
                _put(["*", "g"] if why == "g" else ["*"])
        elif ev == "os.system":
            _put(["*"])
    except Exception:  # never fail the code under test (a line a full disk refused is lost)
        pass
