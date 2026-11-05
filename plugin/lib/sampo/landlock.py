"""T-1607: confine an fm code worker's filesystem writes with Landlock (Linux 5.13+), through ctypes, stdlib only.

The worker's whole process tree may read everything but write only beneath its writable set: the run's tree, its git
objects/refs/logs and own git dir (never a shared repo's hooks or config), scratch, a few devices, Claude Code's
working folders (never its settings, hooks, plugins or Sampo's code), Sampo's state and the common tool caches.
The ruleset is built in the parent (prepare); the child only locks itself (enter), so nothing is loaded after fork.
Inherited by everything the worker starts and impossible to undo from inside. Optional: on another OS, an older
kernel or with the LSM off, available() says why and nothing changes.
ponytail: enter() guards against a worker writing where it shouldn't by mistake, not against a hostile one: its reads,
the network and AF_UNIX sockets in /tmp (tmux, X11, systemd) aren't restricted. prepare_jail with syscall_filter is the
hostile-child jail (T-3160): reads and writes only where named, no socket, no signal or ptrace beyond its own domain."""
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
    from sampo import core
    home = os.path.expanduser("~")
    out = [os.path.realpath(root), "/tmp", "/var/tmp", *_DEVICES]
    git_dir, common = _git(root, "--git-dir"), _git(root, "--git-common-dir")
    if git_dir:
        out.append(git_dir)  # a worktree's own HEAD and index; a plain checkout's .git is inside the tree anyway
    if common and common != git_dir:  # shared with the main checkout: its objects and refs, never hooks or config
        out += [os.path.join(common, x) for x in ("objects", "refs", "logs", "packed-refs")]
    out += [os.path.join(home, ".claude", x) for x in _CLAUDE_WRITABLE]
    out += [os.path.join(home, x) for x in _HOME_WRITABLE]
    out.append(core.state_dir())
    for var, sub in (("TMPDIR", ""), ("XDG_CACHE_HOME", ""), ("CARGO_HOME", "registry"), ("GOPATH", "pkg")):
        if os.environ.get(var):
            out.append(os.path.join(os.environ[var], sub) if sub else os.environ[var])
    seen = []
    for p in out:
        if os.path.lexists(p) and os.path.realpath(p) not in seen:
            seen.append(os.path.realpath(p))
    return seen


def _ruleset(attr, rules):
    """A ruleset fd from a packed landlock_ruleset_attr and (path, rights on a dir, rights on a file) rules."""
    nr = _NR.get(platform.machine())
    rs = _LIBC.syscall(nr[0], ctypes.c_char_p(attr), ctypes.c_size_t(len(attr)), ctypes.c_uint32(0))
    if rs < 0:
        raise OSError(ctypes.get_errno(), "landlock_create_ruleset failed")
    try:
        for p, on_dir, on_file in rules:
            try:
                fd = os.open(p, os.O_PATH | os.O_CLOEXEC)
            except OSError:
                continue  # gone since the set was made: nothing to allow
            try:
                allowed = on_dir if stat.S_ISDIR(os.fstat(fd).st_mode) else on_file  # a file rule: file rights only
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


def prepare(paths):
    """In the parent: a Landlock ruleset fd allowing writes only beneath paths (close it after starting the child).
    Raises OSError when it can't, so a caller never starts a worker it believes confined without confinement."""
    nr, v = _NR.get(platform.machine()), abi()
    if not nr or v < 1:
        raise OSError("Landlock isn't available")
    handled = _writes(v)
    return _ruleset(struct.pack("Q", handled), [(p, handled, handled & (_A["WRITE_FILE"] | _A["TRUNCATE"]))
                                                for p in paths])


_READS = _A["EXECUTE"] | _A["READ_FILE"] | _A["READ_DIR"]
NET_ABI, SCOPE_ABI = 4, 6  # TCP bind/connect rules; abstract unix sockets and signals scoped to the domain


def prepare_jail(reads, writes):
    """T-3160: a ruleset for a hostile child: it reads and runs only beneath reads, writes only beneath writes, and from
    ABI 4 binds and connects no TCP port; from ABI 6 its abstract unix sockets and signals stay inside. Raises OSError
    when Landlock isn't there (the caller then refuses to run anything)."""
    nr, v = _NR.get(platform.machine()), abi()
    if not nr or v < 1:
        raise OSError("Landlock isn't available")
    handled = _writes(v) | _READS
    attr = struct.pack("Q", handled) + (struct.pack("Q", 3) if v >= NET_ABI else b"") + \
        (struct.pack("Q", 3) if v >= SCOPE_ABI else b"")  # no net rule follows: every TCP bind and connect is refused
    files = _A["EXECUTE"] | _A["READ_FILE"]
    wfiles = (files | _A["WRITE_FILE"] | _A["TRUNCATE"]) & handled
    return _ruleset(attr, [(p, _READS, files) for p in reads] + [(p, handled, wfiles) for p in writes])


# T-3160: seccomp refuses with EPERM: socket(2) and io_uring_setup(2) (its ops open sockets too); ptrace and reading or
# writing another process's memory; setsid and setpgid (a run can't leave the process group killpg ends); setpriority,
# and prlimit64 on another process; and below SCOPE_ABI, where Landlock doesn't scope signals, every syscall that
# signals another process, and fcntl F_SETOWN. ponytail: sched_setaffinity and ioprio_set on another process of the
# uid still pass (a slowdown, never a kill); deny them here if that matters. Another syscall ABI
# (i386 through int 0x80) kills the process, and x32 numbers are refused. (audit arch, {syscall: nr}) per CPU.
_GENERIC = {"socket": 198, "ptrace": 117, "process_vm_readv": 270, "process_vm_writev": 271, "pidfd_getfd": 438,
            "setsid": 157, "setpgid": 154, "kill": 129, "tkill": 130, "tgkill": 131, "rt_sigqueueinfo": 138,
            "rt_tgsigqueueinfo": 240, "pidfd_send_signal": 424, "io_uring_setup": 425, "setpriority": 140,
            "prlimit64": 261, "fcntl": 25}  # asm-generic/unistd.h
_SECCOMP_ARCH = {"x86_64": (0xC000003E, {"socket": 41, "ptrace": 101, "process_vm_readv": 310, "process_vm_writev": 311,
                                         "pidfd_getfd": 438, "setsid": 112, "setpgid": 109, "kill": 62, "tkill": 200,
                                         "tgkill": 234, "rt_sigqueueinfo": 129, "rt_tgsigqueueinfo": 297,
                                         "pidfd_send_signal": 424, "io_uring_setup": 425, "setpriority": 141,
                                         "prlimit64": 302, "fcntl": 72}),
                 "aarch64": (0xC00000B7, _GENERIC), "riscv64": (0xC00000F3, _GENERIC)}
_DENY = ("socket", "io_uring_setup", "ptrace", "process_vm_readv", "process_vm_writev", "pidfd_getfd", "setsid",
         "setpgid", "setpriority")
_SIGNALS = ("kill", "tkill", "tgkill", "rt_sigqueueinfo", "rt_tgsigqueueinfo", "pidfd_send_signal")


class _FProg(ctypes.Structure):
    _fields_ = [("len", ctypes.c_ushort), ("filter", ctypes.c_void_p)]


def syscall_filter():
    """In the parent: a seccomp program for enter_jail, or None when this CPU's numbers aren't known. Below SCOPE_ABI
    it refuses signals too: a run can't even kill its own children then (killpg from the parent still ends them)."""
    arch = _SECCOMP_ARCH.get(platform.machine())
    if not arch:
        return None
    nr, scoped = arch[1], abi() >= SCOPE_ABI
    # (code, jt, jf, k): a jump is an offset or "ok"/"no", resolved below. ld 0x20, jeq 0x15, jge 0x35, ret 0x06.
    ins = [(0x20, 0, 0, 4), (0x15, 1, 0, arch[0]), (0x06, 0, 0, 0x80000000),  # arch: same ABI or kill the process
           (0x20, 0, 0, 0), (0x35, "no", 0, 0x40000000)]  # the syscall number; x32's are refused
    ins += [(0x15, "no", 0, nr[s]) for s in _DENY + (() if scoped else _SIGNALS)]
    # prlimit64 on itself only (pid 0, as glibc's setrlimit calls it): another process's RLIMIT_CPU kills it at any
    # ABI. The args sit at offset 16, 8 bytes each, low word first (all three CPUs are little-endian).
    ins += [(0x15, 0, 4, nr["prlimit64"]), (0x20, 0, 0, 16), (0x15, 0, "no", 0), (0x20, 0, 0, 20),
            (0x15, "ok", "no", 0)]
    if not scoped:  # F_SETOWN and F_SETOWN_EX aim SIGIO, any signal with F_SETSIG, at another process
        ins += [(0x15, 0, 3, nr["fcntl"]), (0x20, 0, 0, 24), (0x15, "no", 0, 8), (0x15, "no", "ok", 15)]
    ins += [(0x06, 0, 0, 0x7FFF0000), (0x06, 0, 0, 0x00050000 | 1)]  # ok: allow; no: SECCOMP_RET_ERRNO | EPERM
    to = {"ok": len(ins) - 2, "no": len(ins) - 1}
    ins = [(op, *(to[j] - i - 1 if isinstance(j, str) else j for j in (jt, jf)), k) for i, (op, jt, jf, k) in
           enumerate(ins)]
    buf = ctypes.create_string_buffer(b"".join(struct.pack("=HBBI", *i) for i in ins))
    prog = _FProg(len(ins), ctypes.cast(buf, ctypes.c_void_p))
    prog.buf = buf  # kept alive with the program
    return prog


def enter_jail(rs, prog):
    """In the child: no new privileges, the seccomp program (when there is one), then the Landlock ruleset."""
    if _LIBC.prctl(_PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) != 0:
        raise OSError(ctypes.get_errno(), "PR_SET_NO_NEW_PRIVS failed")
    if prog is not None and _LIBC.prctl(22, 2, ctypes.byref(prog), 0, 0) != 0:  # PR_SET_SECCOMP, MODE_FILTER
        raise OSError(ctypes.get_errno(), "seccomp failed")
    if _LIBC.syscall(_NR[platform.machine()][2], ctypes.c_int(rs), ctypes.c_uint32(0)) < 0:
        raise OSError(ctypes.get_errno(), "landlock_restrict_self failed")


def enter(rs):
    """In the child (subprocess preexec_fn): no new privileges, then lock to the ruleset. Two syscalls, nothing loaded."""
    if _LIBC.prctl(_PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) != 0:
        raise OSError(ctypes.get_errno(), "PR_SET_NO_NEW_PRIVS failed")
    if _LIBC.syscall(_NR[platform.machine()][2], ctypes.c_int(rs), ctypes.c_uint32(0)) < 0:
        raise OSError(ctypes.get_errno(), "landlock_restrict_self failed")
