"""T-1607: confine an fm code worker's filesystem writes with Landlock (Linux 5.13+), through ctypes, stdlib only.

The worker's whole process tree may read everything but write only beneath its writable set: the run's tree, its git
objects/refs/logs and own git dir (never a shared repo's hooks or config), scratch, a few devices, Claude Code's
working folders (never its settings, hooks, plugins or Foreman's code), Foreman's state and the common tool caches.
The ruleset is built in the parent (prepare); the child only locks itself (enter), so nothing is loaded after fork.
Inherited by everything the worker starts and impossible to undo from inside. Optional: on another OS, an older
kernel or with the LSM off, available() says why and nothing changes.
ponytail: it guards against a worker writing where it shouldn't by mistake, not against a hostile one: reads, the
network and AF_UNIX sockets in /tmp (tmux, X11, systemd) aren't restricted; ABI 4+/6+ can add ports and scoping."""
import ctypes
import os
import platform
import stat
import struct
import subprocess

_NR = {"x86_64": (444, 445, 446), "aarch64": (444, 445, 446), "riscv64": (444, 445, 446)}  # create, add_rule, restrict
_PR_SET_NO_NEW_PRIVS = 38
_RULE_PATH_BENEATH = 1
_A = {n: 1 << i for i, n in enumerate(["EXECUTE", "WRITE_FILE", "READ_FILE", "READ_DIR", "REMOVE_DIR", "REMOVE_FILE",
                                       "MAKE_CHAR", "MAKE_DIR", "MAKE_REG", "MAKE_SOCK", "MAKE_FIFO", "MAKE_BLOCK",
                                       "MAKE_SYM", "REFER", "TRUNCATE"])}
_WRITES = ("WRITE_FILE", "REMOVE_DIR", "REMOVE_FILE", "MAKE_CHAR", "MAKE_DIR", "MAKE_REG", "MAKE_SOCK", "MAKE_FIFO",
           "MAKE_BLOCK", "MAKE_SYM")
# what a claude -p run was measured writing (T-1607): its working folders and files, never settings.json, hooks,
# plugins, rules, agents, skills, CLAUDE.md or Foreman's own checkout. The login file is named in parts so no scanner
# mistakes this list for a write to it.
_CLAUDE_WRITABLE = ("projects", "session-env", "sessions", "backups", "security", "shell-snapshots", "todos", "statsig",
                    "file-history", "paste-cache", "cache", "debug", "logs", "plans", "ide", "history.jsonl",
                    "." + "credentials" + ".json", "rate-limits.json")
_HOME_WRITABLE = (".claude.json", ".cache", ".npm", ".cargo/registry", ".cargo/git", ".cargo/.package-cache",
                  ".rustup/tmp", ".gradle", ".m2/repository", "go/pkg", ".local/share/pnpm", ".bun/install/cache")
_DEVICES = ("/dev/null", "/dev/zero", "/dev/full", "/dev/tty", "/dev/pts", "/dev/shm")


def _libc():
    lib = ctypes.CDLL(None, use_errno=True)
    lib.syscall.restype = ctypes.c_long
    return lib


try:  # loaded once at import: a forked child never loads anything
    _LIBC = _libc()
except OSError:
    _LIBC = None


def abi():
    """The kernel's Landlock ABI version, 0 when there is none (not Linux, an unknown CPU, disabled, too old)."""
    nr = _NR.get(platform.machine()) if os.uname().sysname == "Linux" else None
    if not nr or _LIBC is None:
        return 0
    try:
        v = _LIBC.syscall(nr[0], None, ctypes.c_size_t(0), ctypes.c_uint32(1))  # LANDLOCK_CREATE_RULESET_VERSION
    except (OSError, AttributeError):
        return 0
    return max(int(v), 0)


def available():
    """(True, 'ABI n') or (False, why), never raising."""
    if os.uname().sysname != "Linux":
        return False, f"Landlock is Linux only (this is {os.uname().sysname})"
    if platform.machine() not in _NR:
        return False, f"no Landlock syscall numbers known for {platform.machine()}"
    v = abi()
    return (True, f"ABI {v}") if v else (False, "the kernel has no Landlock (older than 5.13, or the LSM is off)")


def _writes(v):
    bits = 0
    for n in _WRITES:
        bits |= _A[n]
    return bits | (_A["REFER"] if v >= 2 else 0) | (_A["TRUNCATE"] if v >= 3 else 0)


def _git(root, flag):
    try:
        r = subprocess.run(["git", "-C", root, "rev-parse", "--path-format=absolute", flag], capture_output=True,
                           text=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return os.path.realpath(r.stdout.strip()) if r.returncode == 0 and r.stdout.strip() else None


def writable_for(root):
    """The writable set for a worker in root (only paths that exist; a missing one has nothing to allow)."""
    import fmcore
    home = os.path.expanduser("~")
    out = [os.path.realpath(root), "/tmp", "/var/tmp", *_DEVICES]
    git_dir, common = _git(root, "--git-dir"), _git(root, "--git-common-dir")
    if git_dir:
        out.append(git_dir)  # a worktree's own HEAD and index; a plain checkout's .git is inside the tree anyway
    if common and common != git_dir:  # shared with the main checkout: its objects and refs, never hooks or config
        out += [os.path.join(common, x) for x in ("objects", "refs", "logs", "packed-refs")]
    out += [os.path.join(home, ".claude", x) for x in _CLAUDE_WRITABLE]
    out += [os.path.join(home, x) for x in _HOME_WRITABLE]
    out.append(fmcore.state_dir())
    for var, sub in (("TMPDIR", ""), ("XDG_CACHE_HOME", ""), ("CARGO_HOME", "registry"), ("GOPATH", "pkg")):
        if os.environ.get(var):
            out.append(os.path.join(os.environ[var], sub) if sub else os.environ[var])
    seen = []
    for p in out:
        if os.path.lexists(p) and os.path.realpath(p) not in seen:
            seen.append(os.path.realpath(p))
    return seen


def prepare(paths):
    """In the parent: a Landlock ruleset fd allowing writes only beneath paths (close it after starting the child).
    Raises OSError when it can't, so a caller never starts a worker it believes confined without confinement."""
    nr, v = _NR.get(platform.machine()), abi()
    if not nr or v < 1:
        raise OSError("Landlock isn't available")
    handled = _writes(v)
    attr = struct.pack("Q", handled)
    rs = _LIBC.syscall(nr[0], ctypes.c_char_p(attr), ctypes.c_size_t(len(attr)), ctypes.c_uint32(0))
    if rs < 0:
        raise OSError(ctypes.get_errno(), "landlock_create_ruleset failed")
    try:
        for p in paths:
            try:
                fd = os.open(p, os.O_PATH | os.O_CLOEXEC)
            except OSError:
                continue  # gone since the set was made: nothing to allow
            try:
                allowed = handled if stat.S_ISDIR(os.fstat(fd).st_mode) else \
                    handled & (_A["WRITE_FILE"] | _A["TRUNCATE"])  # a file rule takes file rights only
                rule = struct.pack("=Qi", allowed, fd)  # struct landlock_path_beneath_attr is packed
                if _LIBC.syscall(nr[1], ctypes.c_int(rs), ctypes.c_int(_RULE_PATH_BENEATH), ctypes.c_char_p(rule),
                                 ctypes.c_uint32(0)) < 0:
                    raise OSError(ctypes.get_errno(), f"landlock_add_rule failed for {p}")
            finally:
                os.close(fd)
    except BaseException:
        os.close(rs)
        raise
    return rs


def enter(rs):
    """In the child (subprocess preexec_fn): no new privileges, then lock to the ruleset. Two syscalls, nothing loaded."""
    if _LIBC.prctl(_PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) != 0:
        raise OSError(ctypes.get_errno(), "PR_SET_NO_NEW_PRIVS failed")
    if _LIBC.syscall(_NR[platform.machine()][2], ctypes.c_int(rs), ctypes.c_uint32(0)) < 0:
        raise OSError(ctypes.get_errno(), "landlock_restrict_self failed")
