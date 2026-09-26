"""Foreman guard: decides whether a tool call is dangerous enough to block (PROTECTED CORE).

Pure functions, no state writes. The PreToolUse hook calls check(); a Block is denied unless the
active brief's `allow:` lists its category. `state-direct` is never authorizable. Callers treat any
exception as a block (fail closed). This is a speed bump with good coverage, not a sandbox: shell
text can always be obfuscated; deny rules and git are the other layers.
"""
import os
import re
import shlex
import subprocess
from dataclasses import dataclass, field

CATEGORIES = ["self-authorize", "state-direct", "core", "remote", "credentials", "system", "rm-outside", "git-destructive",
              "pipe-shell", "publish"]
NOT_AUTHORIZABLE = {"state-direct", "self-authorize"}
USER_ONLY = {"core", "remote"}  # granted only by the user's reply to `fm ask`, never by `fm task set --allow`
FILE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
DEFAULT_BRANCHES = {"main", "master", "trunk"}


@dataclass
class Ctx:
    cwd: str
    project_root: str
    home: str
    foreman_home: str
    scratch: list = field(default_factory=list)
    allow: set = field(default_factory=set)
    task_id: str = None
    state_dir: str = None  # when Foreman state lives outside foreman_home (read-only home fallback)
    state_fallbacks: list = field(default_factory=list)  # where a fallback could live: state even before it's used


@dataclass
class Block:
    category: str
    detail: str


def check(tool_name, tool_input, ctx):
    if tool_name in FILE_TOOLS:
        raw = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
        path = _resolve(_expand(raw, ctx), ctx.cwd)
        found = [(cat, path) for cat in classify_write(path, ctx)]
    elif tool_name == "Bash":
        found = check_bash(tool_input["command"], ctx)
    else:
        return None
    for cat in CATEGORIES:
        for got, detail in found:
            if got == cat and (got in NOT_AUTHORIZABLE or got not in ctx.allow):
                return Block(got, detail)
    return None


def _is_allow(arg):
    """`--allow`, `--allow=…` and any abbreviation argparse would have accepted (fm now rejects those too)."""
    flag = arg.partition("=")[0]
    return len(flag) > 3 and "--allow".startswith(flag)


_ASK = "fm ask {id} {cat} --why \"<what and why>\", then ask the user one yes/no question; their yes grants it"


def message(block, ctx):
    cat, detail = block.category, block.detail
    tid = ctx.task_id or "<ID>"
    if cat == "self-authorize":
        return (f"Foreman guard: blocked self-authorize: {detail}. Protected core (Foreman code, rules, evals, "
                f"BUILD_PROMPT.md, settings) and remote sessions need the user's approval, which an agent can't grant: "
                + _ASK.format(id=tid, cat="<core|remote>") + ".")
    if cat == "state-direct":
        return (f"Foreman guard: blocked state-direct: {detail} is Foreman state. Change it through fm "
                f"(fm task …, fm capture, fm checkpoint); direct writes are never authorized.")
    if ctx.task_id:
        how = f"fm task set {ctx.task_id} --allow {cat} (records it in the brief), then retry"
    else:
        how = (f"create or focus a task first (fm task new \"…\" --type T --tier S, or fm focus ID), "
               f"then fm task set <ID> --allow {cat}, then retry")
    if cat == "core":
        return f"Foreman guard: blocked core: {detail} is protected core. To authorize: " + _ASK.format(id=tid, cat=cat) + "."
    if cat == "remote":
        return f"Foreman guard: blocked remote: {detail}. To authorize: " + _ASK.format(id=tid, cat=cat) + "."
    return f"Foreman guard: blocked {cat}: {detail}. To authorize: {how}."


def project_root_for(cwd, home):
    d = os.path.realpath(cwd)
    probe = d
    while True:
        if os.path.exists(os.path.join(probe, ".git")):
            return probe
        parent = os.path.dirname(probe)
        if parent == probe:
            break
        probe = parent
    h = os.path.realpath(home)
    if d == "/" or d == h or h.startswith(d.rstrip("/") + "/"):
        return None
    return d


# ---------------------------------------------------------------- paths

def _expand(tok, ctx):
    t = re.sub(r"^~(?=/|$)", lambda _: ctx.home, tok)
    return t.replace("${HOME}", ctx.home).replace("$HOME", ctx.home)


def _unresolvable(tok):
    return "$" in tok or "`" in tok


def _resolve(tok, base):
    return os.path.normpath(tok if os.path.isabs(tok) else os.path.join(base, tok))


def _under(path, root):
    root = root.rstrip("/")
    return not root or path == root or path.startswith(root + "/")


def _strictly_under(path, root):
    return path != root.rstrip("/") and _under(path, root)


def _variants(path):
    out = {path}
    try:
        out.add(os.path.realpath(path))
    except OSError:
        pass
    return out


_SAFE_DEV = re.compile(r"^/dev/(null|zero|stdout|stderr|stdin|tty|random|urandom|fd/.*|shm/.*)$")
_DOC_EXT = {".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".c", ".h", ".cc", ".cpp", ".hpp", ".java", ".kt", ".rb",
            ".php", ".cs", ".swift", ".scala", ".sh", ".md", ".rst", ".adoc", ".html", ".css", ".nix", ".lua", ".zig", ".ml"}
_CRED_DIRS = [".ssh", ".aws", ".config/gcloud", ".kube", ".gnupg", ".config/gh"]
_CRED_FILES = [".netrc", ".npmrc", ".pypirc", ".git-credentials", ".claude/.credentials.json", ".docker/config.json"]


def _is_credential(path, ctx):
    for d in _CRED_DIRS:
        if _under(path, os.path.join(ctx.home, d)):
            return True
    if path in {os.path.join(ctx.home, f) for f in _CRED_FILES}:
        return True
    base = os.path.basename(path)
    if re.fullmatch(r"\.env(\..+)?", base) and not re.search(r"\.(example|sample|template|dist|defaults?)$", base):
        return True
    if re.search(r"\.(pem|key|p12|pfx|keystore|jks)$", base) or re.match(r"id_(rsa|dsa|ecdsa|ed25519)(?!.*\.pub$)", base):
        return True
    stem, ext = os.path.splitext(base)
    return bool(re.search(r"(^|[._-])(tokens?|secrets?|credentials?)([._-]|$)", stem.lower())) and ext.lower() not in _DOC_EXT


def _is_core(path, ctx):
    """Protected core: all Foreman code (it enforces the guard), the rules, the eval suite, the spec and settings."""
    fh = ctx.foreman_home
    files = {os.path.join(fh, f) for f in ("plugin/rules/foreman.md", "BUILD_PROMPT.md")}
    dirs = [os.path.join(fh, "plugin", d) for d in ("lib", "bin", "hooks", "evals")]
    return path in files or any(_under(path, d) for d in dirs) or path == os.path.join(ctx.home, ".claude.json") or \
        bool(re.search(r"/\.claude/settings(\.local)?\.json$", path))


def classify_write(path, ctx):
    cats = []
    for p in _variants(path):
        if any(d and _under(p, d) for d in [os.path.join(ctx.foreman_home, "state"), ctx.state_dir,
                                            *ctx.state_fallbacks]):
            cats.append("state-direct")
        if _is_core(p, ctx):
            cats.append("core")
        if _is_credential(p, ctx):
            cats.append("credentials")
        if (p.startswith("/dev/") and not _SAFE_DEV.match(p)) or _under(p, os.path.join(ctx.home, ".config", "systemd")):
            cats.append("system")  # device files; user units (persistence that outlives the session)
    return list(dict.fromkeys(cats))


# ---------------------------------------------------------------- shell parsing

@dataclass
class Cmd:
    argv: list
    redirs: list
    piped: bool
    procsub: bool = False


def _strip_heredocs(cmd):
    lines, out, i = cmd.split("\n"), [], 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        i += 1
        for _, delim in re.findall(r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1", line):
            while i < len(lines) and lines[i].strip() != delim:
                i += 1
            i += 1
    return "\n".join(out)


def _tokens(cmd):
    try:
        lex = shlex.shlex(cmd, posix=True, punctuation_chars=";&|()<>")
        lex.whitespace_split = True
        lex.commenters = "#"
        return list(lex)
    except ValueError:
        return cmd.replace(";", " ; ").replace("|", " | ").split()


def _split(tokens):
    cmds, cur = [], Cmd([], [], False)
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t in ("<(", ">("):
            cur.procsub = True
            cmds.append(cur)
            cur = Cmd([], [], False)
            i += 1
            continue
        if re.fullmatch(r"[;&|()]+", t) and not re.fullmatch(r"&>+", t):
            if cur.argv or cur.redirs or cur.procsub:
                cmds.append(cur)
            cur = Cmd([], [], t in ("|", "|&"))
            i += 1
            continue
        if re.fullmatch(r"[<>&]+", t):
            nxt = tokens[i + 1] if i + 1 < len(tokens) else ""
            if t == "<" and nxt == "(":
                cur.procsub = True
                cmds.append(cur)
                cur = Cmd([], [], False)
                i += 2
                continue
            if t.endswith("&") and re.fullmatch(r"\d+|-", nxt):
                i += 2
                continue
            if nxt and (t.startswith(">") or t in ("&>", "&>>", "<>")):
                cur.redirs.append(nxt)
            i += 2
            continue
        cur.argv.append(t)
        i += 1
    if cur.argv or cur.redirs or cur.procsub:
        cmds.append(cur)
    return cmds


def _strip_wrappers(argv):
    """Drop env assignments and exec wrappers (sudo, env, timeout, xargs, npx…). Returns (argv, via_xargs)."""
    i = 0
    while i < len(argv):
        a = argv[i]
        base = os.path.basename(a)
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", a):
            i += 1
        elif base in ("sudo", "doas"):
            i += 1
            while i < len(argv) and argv[i].startswith("-"):
                i += 2 if argv[i] in ("-u", "-g", "-C", "-D", "-h", "-p", "-r", "-t", "-U") else 1
        elif base in ("nohup", "time", "command", "builtin", "exec", "noglob", "stdbuf", "nice", "ionice", "chronic"):
            i += 1
            while i < len(argv) and argv[i].startswith("-"):
                i += 2 if argv[i] in ("-n", "-c", "-p") else 1
        elif base == "timeout":
            i += 1
            while i < len(argv) and argv[i].startswith("-"):
                i += 2 if argv[i] in ("-s", "-k", "--signal", "--kill-after") else 1
            i += 1
        elif base == "env":
            i += 1
            while i < len(argv) and (argv[i].startswith("-") or "=" in argv[i]):
                i += 2 if argv[i] in ("-u", "-C", "--unset", "--chdir") else 1
        elif base == "xargs":
            i += 1
            while i < len(argv) and argv[i].startswith("-"):
                i += 2 if argv[i] in ("-n", "-I", "-L", "-P", "-d", "-s", "-E", "-a") else 1
        elif base in ("npx", "bunx"):
            i += 1
            while i < len(argv) and argv[i].startswith("-"):
                i += 1
        else:
            break
    return argv[i:], any(os.path.basename(a) == "xargs" for a in argv[:i])


def _positionals(args):
    return [a for a in args if not a.startswith("-")]


def _name(argv):
    stripped, _ = _strip_wrappers(argv)
    return os.path.basename(stripped[0]) if stripped else ""


# ---------------------------------------------------------------- bash checks

_SHELLS = re.compile(r"^((ba|z|da|k|fi|c|tc)?sh|python[0-9.]*|perl|ruby|node|php|pwsh)$")
_FETCHERS = {"curl", "wget", "fetch"}
_SUBST = re.compile(r"\$\(([^()]*)\)|`([^`]*)`")
_DOWNLOAD_SUBST = re.compile(r"(\$\(|`)\s*(curl|wget|fetch)\b")


_INTERP = re.compile(r"(?:^|[\s;&|(/])(?:python[0-9.]*|py|perl|ruby|node|deno|bun|php)(?:\s|$)")
_WRITE_API = re.compile(
    r"""open\s*\([^)]*['"][rwxab+]*[wxa+][rwxab+]*['"]|\.write_(?:text|bytes)\s*\(|(?:write|append)FileSync|"""
    r"createWriteStream|\bos\.(?:replace|rename|remove|unlink)\b|\bshutil\.\w+\(|\.(?:unlink|rename|replace|touch)\(|"
    r"File\.write|file_put_contents|open\s*\(\s*(?:my\s+)?\$?\w+\s*,\s*['\"]?[>+]")
_QUOTED = re.compile(r"""(['"])((?:[~/.]|[\w.-]+/)[^'"\s]*)\1""")
_GUARDED_BY_PATH = ("core", "state-direct", "credentials")


# Any Foreman module (fm*.py in plugin/lib), so new modules are covered without editing this list. Calls into the entry
# point modules count as mutating; fmcore/fmguard/fmdocs/fmdoctor are mostly read-only, so their mutators are by name.
_FM_INTERNALS = re.compile(r"\b(?:import|from)\s+fm[a-z]+\b")
_FM_ENTRY = r"(?:fmcli|fmhooks|fmsetup|fmtidy|fmideas|fmserve)"
_FM_MUTATORS = re.compile(r"\b(?:save_brief|write_meta|update_meta|write_atomic|log_event|regen_views|init_project|"
                          r"checkpoint|mutate|cmd_\w+|task_\w+|_resolve_approvals|_activate_fallback|"
                          r"restore_default_state)\s*\(|"
                          rf"\b{_FM_ENTRY}\s*\.\s*\w+\s*\(|\bfrom\s+{_FM_ENTRY}\s+import\b")


def _interpreter_writes(cmd, ctx):
    """Interpreter code (heredoc, -c, -e) that writes files: every quoted path it names counts as a write target.

    Coarse on purpose: a script that names a protected path and writes anything is treated as writing it. Code that
    imports Foreman's modules and calls their writers bypasses fm (the only state writer): that needs core, i.e. the
    user's yes, rather than never-authorizable state-direct, because the text match can't tell code from test data."""
    if not _INTERP.search(cmd):
        return []
    if _FM_INTERNALS.search(cmd) and _FM_MUTATORS.search(cmd):
        return [("core", "interpreter code driving Foreman's modules (use the fm CLI)")]
    if not _WRITE_API.search(cmd):
        return []
    found = []
    for m in _QUOTED.finditer(cmd):
        path = _resolve(_expand(m.group(2), ctx), ctx.cwd)
        found += [(cat, f"{path} (written from interpreter code)") for cat in classify_write(path, ctx)
                  if cat in _GUARDED_BY_PATH]
    return found


def fm_calls(cmd):
    """The argument lists of every direct `fm …` (or `python3 …/fm …`) call in a shell command."""
    calls = []
    for c in _split(_tokens(_strip_heredocs(cmd).replace("\n", " ; "))):
        argv, _ = _strip_wrappers(c.argv)
        name, args = (os.path.basename(argv[0]) if argv else ""), argv[1:]
        if name == "fm":
            calls.append(args)
        elif re.match(r"^python[0-9.]*$", name) and args[:1] and args[0].endswith("/fm"):
            calls.append(args[1:])
    return calls


def check_bash(cmd, ctx, depth=0):
    """Return [(category, detail)] for every dangerous thing found in a shell command."""
    if depth > 4:
        return [("rm-outside", "command nesting too deep to analyse")]
    found = _interpreter_writes(cmd, ctx) if depth == 0 else []
    cmds = _split(_tokens(_strip_heredocs(cmd).replace("\n", " ; ")))
    cwd, chain = ctx.cwd, []
    for idx, c in enumerate(cmds):
        argv, via_xargs = _strip_wrappers(c.argv)
        if not c.piped:
            chain = []
        name = os.path.basename(argv[0]) if argv else ""
        args = argv[1:]
        if name in ("cd", "pushd"):
            tgt = args[0] if args else ctx.home
            if not _unresolvable(tgt):
                cwd = _resolve(_expand(tgt, ctx), cwd)
        for tok in c.argv:
            for m in _SUBST.finditer(tok):
                found += check_bash(m.group(1) or m.group(2) or "", ctx, depth + 1)
        if _SHELLS.match(name) and "-c" in args and args.index("-c") + 1 < len(args):
            inner = args[args.index("-c") + 1]
            found += check_bash(inner, ctx, depth + 1)
            if _DOWNLOAD_SUBST.search(inner):
                found.append(("pipe-shell", f"{name} -c runs a downloaded script"))
        if name == "eval":
            joined = " ".join(args)
            found += check_bash(joined, ctx, depth + 1)
            if _DOWNLOAD_SUBST.search(joined):
                found.append(("pipe-shell", "eval of a downloaded script"))
        if _SHELLS.match(name) or name in ("source", "."):
            if c.piped and any(_name(x.argv) in _FETCHERS for x in chain):
                found.append(("pipe-shell", f"downloaded content piped into {name}"))
            nxt = cmds[idx + 1] if idx + 1 < len(cmds) else None
            if c.procsub and nxt and _name(nxt.argv) in _FETCHERS:
                found.append(("pipe-shell", f"{name} <(download)"))
        for target in c.redirs + _write_targets(name, args):
            if not _unresolvable(target):
                found += [(cat, target) for cat in classify_write(_resolve(_expand(target, ctx), cwd), ctx)]
        if name == "fm" or (re.match(r"^python[0-9.]*$", name) and any(a.endswith("/fm") for a in args[:1])):
            fm_args = args[1:] if name != "fm" else args
            if any(_is_allow(a) and (a.partition("=")[2] or b) in USER_ONLY for a, b in zip(fm_args, fm_args[1:] + [""])):
                found.append(("self-authorize", "an agent may not grant core or remote"))
            if fm_args[:1] == ["serve"] and fm_args[1:2] not in (["status"], ["stop"]):
                found.append(("remote", "fm serve starts a persistent Remote Control session reachable from the "
                                        "user's claude.ai account"))
        found += _check_rm(name, args, via_xargs, chain, cwd, ctx)
        found += _check_git(name, args, cwd, ctx)
        found += _check_system(name, args)
        found += _check_publish(name, args)
        chain.append(Cmd(c.argv, c.redirs, c.piped))
    return found


def _opt_values(args, *flags):
    """Values of options given as `-X v`, `-Xv`, `--long v` or `--long=v`."""
    out = []
    for i, a in enumerate(args):
        for f in flags:
            if a == f and i + 1 < len(args):
                out.append(args[i + 1])
            elif f.startswith("--") and a.startswith(f + "="):
                out.append(a[len(f) + 1:])
            elif not f.startswith("--") and a.startswith(f) and len(a) > len(f):
                out.append(a[len(f):])
    return out


def _tar_targets(args):
    """Where tar writes: the -C dir (else the cwd) when extracting, the archive when creating."""
    short = [a[1:] for a in args if a.startswith("-") and not a.startswith("--")]
    if args and not args[0].startswith("-"):
        short.append(args[0])  # old style: tar xzf archive
    longs = {a.split("=")[0] for a in args if a.startswith("--")}
    out = []
    if any("x" in c for c in short) or longs & {"--extract", "--get"}:
        out += _opt_values(args, "-C", "--directory") or ["."]
    if any(set(c) & set("cruA") for c in short) or longs & {"--create", "--append", "--update"}:
        out += _opt_values(args, "--file") + [args[i + 1] for i, a in enumerate(args[:-1])
                                              if (a.startswith("-") and not a.startswith("--") or i == 0)
                                              and a.endswith("f")]
    return out


def _write_targets(name, args):
    """Paths a command writes (a directory means anything under it). Archives, clones and -t target dirs included:
    the guard can't see an archive's members, so the destination itself is what's checked."""
    pos = _positionals(args)
    if name == "tee":
        return pos
    if name in ("cp", "mv", "install", "ln", "rsync"):
        tdir = _opt_values(args, "-t", "--target-directory") if name != "rsync" else []  # rsync -t: keep times
        return tdir + ([pos[-1]] if len(pos) >= 2 else [])
    if name in ("tar", "gtar", "bsdtar"):
        return _tar_targets(args)
    if name == "unzip":
        return [] if set(args) & {"-l", "-t", "-v", "-Z", "-p", "-c"} else _opt_values(args, "-d") or ["."]
    if name == "cpio":
        extract = any("i" in a[1:] for a in args if a.startswith("-") and not a.startswith("--")) or "--extract" in args
        return (_opt_values(args, "-D", "--directory") or ["."]) if extract else []
    if name in ("7z", "7za", "7zz") and pos and pos[0] in ("x", "e"):
        return _opt_values(args, "-o") or ["."]
    if name == "git":
        i = 0
        while i < len(args) and args[i].startswith("-"):  # global options before the subcommand
            i += 2 if args[i] in ("-C", "-c") else 1
        if i < len(args) and args[i] == "clone":
            rest = _positionals(args[i + 1:])
            return [rest[-1]] if len(rest) >= 2 else ["."]
    if name == "sed" and any(a == "--in-place" or a.startswith("-i") for a in args):
        return pos if any(a in ("-e", "-f") for a in args) else pos[1:]
    if name == "dd":
        return [a[3:] for a in args if a.startswith("of=")]
    if name in ("truncate", "rm"):
        return pos
    if name == "curl":
        return [args[i + 1] for i, a in enumerate(args[:-1]) if a in ("-o", "--output")]
    if name == "wget":
        return [args[i + 1] for i, a in enumerate(args[:-1]) if a in ("-O", "--output-document")] + \
            _opt_values(args, "-P", "--directory-prefix")
    return []


def _rm_target_violation(tok, cwd, ctx, root_ok=False):
    if _unresolvable(tok):
        return f"unresolvable target {tok}"
    path = _resolve(_expand(tok, ctx), cwd)
    if path == "/":
        return "/"
    for s in list(ctx.scratch) + ["/tmp", "/var/tmp", os.environ.get("TMPDIR", "/tmp")]:
        # a scratch root that contains $HOME (odd setups, test fixtures) never exempts paths in $HOME
        if s and _strictly_under(path, s) and not (_under(path, ctx.home) and not _under(s, ctx.home)):
            return None
    if ctx.project_root and (_under if root_ok else _strictly_under)(path, ctx.project_root):
        return None
    return path


def _check_rm(name, args, via_xargs, chain, cwd, ctx):
    out = []
    if name == "rm":
        opts, targets, seen_dd = [], [], False
        for a in args:
            if a == "--" and not seen_dd:
                seen_dd = True
            elif a.startswith("-") and not seen_dd:
                opts.append(a)
            else:
                targets.append(a)
        recursive = any(o in ("-r", "-R", "--recursive") or (not o.startswith("--") and re.search(r"[rR]", o)) for o in opts)
        if recursive:
            if not targets:
                upstream = next((x for x in reversed(chain) if _name(x.argv) == "find"), None)
                targets = _find_paths(_strip_wrappers(upstream.argv)[0][1:]) if (via_xargs and upstream) else []
                if not targets:
                    out.append(("rm-outside", "recursive rm with targets from stdin"))
            for t in targets:
                v = _rm_target_violation(t, cwd, ctx)
                if v:
                    out.append(("rm-outside", f"recursive delete of {v}"))
    elif name == "find":
        deleting = "-delete" in args or any(a in ("-exec", "-execdir", "-ok") and i + 1 < len(args)
                                            and os.path.basename(args[i + 1]) in ("rm", "shred") for i, a in enumerate(args))
        if deleting:
            for t in _find_paths(args):
                v = _rm_target_violation(t, cwd, ctx, root_ok=True)  # find deletes matches inside, not the root
                if v:
                    out.append(("rm-outside", f"find -delete under {v}"))
    return out


def _find_paths(args):
    paths = []
    for a in args:
        if a.startswith("-") or a in ("(", "!", ")"):
            break
        paths.append(a)
    return paths or ["."]


def _git(cwd, *args):
    try:
        r = subprocess.run(["git", "-C", cwd, *args], capture_output=True, text=True, timeout=2)
        return r.stdout.strip() if r.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        return ""


def _defaults(cwd):
    d = set(DEFAULT_BRANCHES)
    head = _git(cwd, "symbolic-ref", "--short", "refs/remotes/origin/HEAD")
    if "/" in head:
        d.add(head.split("/", 1)[1])
    return d


def _check_git(name, args, cwd, ctx):
    if name != "git":
        return []
    i, gcwd = 0, cwd
    while i < len(args) and args[i].startswith("-"):
        if args[i] == "-C" and i + 1 < len(args):
            gcwd = _resolve(_expand(args[i + 1], ctx), cwd)
            i += 2
        elif args[i] in ("-c", "--git-dir", "--work-tree", "--namespace") and i + 1 < len(args):
            i += 2
        else:
            i += 1
    if i >= len(args):
        return []
    sub, rest = args[i], args[i + 1:]
    out = []
    if sub == "push":
        force = any(o in ("-f", "--force", "--force-with-lease", "--force-if-includes") or o.startswith("--force-with-lease=")
                    for o in rest)
        delete = any(o in ("-d", "--delete") for o in rest)
        if "--tags" in rest:
            out.append(("publish", "git push --tags"))
        pos = [r for j, r in enumerate(rest)
               if not r.startswith("-") and not (j and rest[j - 1] in ("-o", "--push-option", "--repo"))]
        refspecs = pos[1:]
        defaults = _defaults(gcwd)
        current = _git(gcwd, "rev-parse", "--abbrev-ref", "HEAD")
        for r in refspecs:
            plus, r2 = r.startswith("+"), r.lstrip("+")
            src, dst = r2.split(":", 1) if ":" in r2 else (r2, r2)
            dst = current if dst == "HEAD" else dst.replace("refs/heads/", "")
            if ":" in r2 and src == "" and dst in defaults:
                out.append(("git-destructive", f"push deleting default branch {dst}"))
            elif delete and dst in defaults:
                out.append(("git-destructive", f"push --delete of default branch {dst}"))
            elif (force or plus) and dst in defaults:
                out.append(("git-destructive", f"force push to default branch {dst}"))
        if force and not refspecs and (current in defaults or any(o in ("--all", "--mirror") for o in rest)):
            out.append(("git-destructive", f"force push while on default branch {current}"))
    elif sub == "reset" and "--hard" in rest:
        current = _git(gcwd, "rev-parse", "--abbrev-ref", "HEAD")
        if current in _defaults(gcwd):
            out.append(("git-destructive", f"reset --hard on default branch {current}"))
    elif sub == "branch" and any(o in ("-D", "-d", "--delete") for o in rest):
        for n in _positionals(rest):
            if n in _defaults(gcwd):
                out.append(("git-destructive", f"deleting default branch {n}"))
    return out


_DISK = {"fdisk", "sfdisk", "cfdisk", "parted", "gdisk", "sgdisk", "wipefs", "mkswap"}
_POWER = {"shutdown", "reboot", "poweroff", "halt"}
_SYSTEMCTL_MUTATE = {"start", "stop", "restart", "reload", "try-restart", "reload-or-restart", "enable", "disable",
                     "reenable", "mask", "unmask", "kill", "isolate", "daemon-reload", "daemon-reexec", "set-default",
                     "poweroff", "reboot", "halt", "suspend", "hibernate", "edit", "set-property", "link", "revert",
                     "preset", "reset-failed"}


def _check_system(name, args):
    pos = _positionals(args)
    if name.startswith("mkfs") or name in _DISK:
        return [("system", f"{name} (disk/partition change)")]
    if name == "dd" and any(a.startswith("of=/dev/") and not _SAFE_DEV.match(a[3:]) for a in args):
        return [("system", "dd onto a device")]
    if name in ("iptables", "ip6tables", "iptables-restore", "ip6tables-restore"):
        if not any(a in ("-L", "--list", "-S", "--list-rules") for a in args):
            return [("system", f"{name} firewall change")]
    if name == "nft" and pos[:1] != ["list"]:
        return [("system", "nft firewall change")]
    if name == "ufw" and pos[:1] not in (["status"], ["show"]):
        return [("system", "ufw firewall change")]
    if name == "firewall-cmd" and not all(a.startswith(("--list", "--get", "--state", "--query", "--zone")) for a in args):
        return [("system", "firewall-cmd change")]
    if name == "systemctl" and "--user" not in args and pos and pos[0] in _SYSTEMCTL_MUTATE:
        return [("system", f"systemctl {pos[0]} (system unit)")]
    if name in _POWER or (name == "init" and pos[:1] in (["0"], ["6"])):
        return [("system", f"{name} (power state)")]
    if name == "cryptsetup" and pos[:1] and pos[0] in ("luksFormat", "erase", "luksErase", "reencrypt"):
        return [("system", f"cryptsetup {pos[0]}")]
    return []


_PUBLISH = {
    "npm": ["publish", "unpublish"], "pnpm": ["publish"], "yarn": ["publish", "npm publish"], "bun": ["publish"],
    "cargo": ["publish", "yank"], "twine": ["upload"], "gem": ["push"], "poetry": ["publish"], "uv": ["publish"],
    "docker": ["push"], "podman": ["push"], "gh": ["release create", "release upload", "release edit"],
    "terraform": ["apply", "destroy"], "tofu": ["apply", "destroy"], "pulumi": ["up", "destroy"],
    "kubectl": ["apply", "delete", "rollout", "replace", "patch", "scale", "create", "set"],
    "helm": ["install", "upgrade", "uninstall", "rollback", "delete"],
    "fly": ["deploy"], "flyctl": ["deploy"], "firebase": ["deploy"], "serverless": ["deploy"], "sls": ["deploy"],
    "wrangler": ["deploy", "publish"], "heroku": ["releases:rollback"],
}


def _check_publish(name, args):
    if "--dry-run" in args:
        return []
    if re.match(r"^python[0-9.]*$", name) and args[:1] == ["-m"] and len(args) > 1:
        name, args = args[1], args[2:]
    pos = _positionals(args)
    joined = " ".join(pos[:2])
    for verb in _PUBLISH.get(name, []):
        if joined == verb or joined.startswith(verb + " ") or pos[:1] == [verb]:
            return [("publish", f"{name} {verb}")]
    if name in ("vercel", "netlify") and "--prod" in args:
        return [("publish", f"{name} production deploy")]
    if name == "claude" and pos[:2] == ["plugin", "tag"] and "--push" in args:
        return [("publish", "claude plugin tag --push")]
    return []
