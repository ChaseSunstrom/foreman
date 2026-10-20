"""Foreman guard: decides whether a tool call is dangerous enough to block (PROTECTED CORE).

Pure functions, no state writes. The PreToolUse hook calls check(); a Block is denied unless the
active brief's `allow:` lists its category. `state-direct` is never authorizable. Callers treat any
exception as a block (fail closed). This is a speed bump with good coverage, not a sandbox: shell
text can always be obfuscated; deny rules and git are the other layers.
"""
import collections
import os
import re
import sys
import shlex
import subprocess

CATEGORIES = ["self-authorize", "state-direct", "core", "remote", "plugin", "credentials", "system", "rm-outside",
              "git-destructive", "pipe-shell", "publish", "confirm", "confine", "brief"]
# confine (T-0234): a builder writes in its worktree only; brief (T-0308): no edits without a task — start one
NOT_AUTHORIZABLE = {"state-direct", "self-authorize", "confine", "brief"}
# fm subcommands that undo or grant what only the user decides: sub -> (the word that makes it so, why, what they type).
# One table, so the next one isn't forgotten.
USER_ONLY_FM = {
    "posture": ("lite", "fm posture lite turns Foreman's hooks off but the guard's: the user decides that",
                "fm posture lite"),  # T-0963
    "pause": ("off", "fm pause off is the user's to run: they paused everything Foreman runs unattended, so only they "
                     "lift it", "fm pause off"),  # T-0591
    "approve-reads": ("on", "fm approve-reads on lets Foreman answer Claude Code's permission dialogs for reads: the "
                            "user turns it on", "fm approve-reads on"),  # T-0974
    "rule": ("rm", "fm rule rm is the user's to run: their rule stops what they said to stop, so only they lift it",
             "fm rule rm N"),  # T-0971; `add rm` is a rare miss
    "taste": ("--block", "fm taste compile N --block makes a rule that stops a command outright, and only the user lifts it "
                         "(fm rule rm): they decide what blocks", "fm taste compile N --block"),  # T-1063
    "rollback": ("--yes", "fm rollback --yes is the user's to run: it puts back an older state, with consent they "
                          "may have revoked since", "fm rollback --yes"),  # T-1085
    "decide": ("--answer", "fm decide ANSWER --answer N records the user's answer to an ask, and answers become "
                           "precedent for proxy answers: only the user records them", "fm decide ANSWER --answer N"),  # T-1064
    "risk": ("set", "fm risk set moves the daily risk budget that slows Claude's autonomy: the brake is the user's to "
                    "move", "fm risk set --day N --because \"<why>\""),  # T-1080
}
def _user_only_hit(word, arg):
    """A word matches itself; a --flag also matches argparse's abbreviations (--y, --ye) and --flag=value."""
    a = arg.split("=")[0] if word.startswith("--") else arg
    return a == word or (word.startswith("--") and len(a) >= 3 and a.startswith("--") and word.startswith(a))


USER_ONLY = {"core", "remote", "plugin", "confirm"}  # granted only by the user's reply to `fm ask`, never by `fm task set --allow`
# (confirm, T-0289: a request a child found in an old transcript is worked only after the user says it's theirs)
FILE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
_CORE_DIRS = ("lib", "bin", "hooks", "evals", "integrations")  # plugin/…: Foreman's code (integrations: T-0340)
DEFAULT_BRANCHES = {"main", "master", "trunk"}


# Plain classes, no imports from the rest of Foreman: the guard must load (and fall back to its committed copy) even
# when the rest of the library is broken, and dataclasses would cost every hook ~9 ms of import.
class Ctx:
    def __init__(self, cwd, project_root, home, foreman_home, scratch=(), allow=(), task_id=None, state_dir=None,
                 state_fallbacks=(), standing=(), trusted=False, confine=None, unbriefed=None):
        self.cwd, self.project_root, self.home, self.foreman_home = cwd, project_root, home, foreman_home
        # T-1249: each scratch folder as given and as it really is (macOS's /tmp is a link to /private/tmp, and a
        # path is judged where it really points too)
        self.scratch = list(dict.fromkeys([*scratch, *(os.path.realpath(s) for s in scratch if s)]))
        self.allow, self.task_id = set(allow), task_id
        self.state_dir = state_dir  # when Foreman state lives outside foreman_home (read-only home fallback)
        # where a fallback could live: state even before it's used, as named and in its folder's real path (T-1284:
        # macOS's temp folder is a link). Never the leaf's link: another user can plant /tmp/foreman-state-<uid> -> /
        self.state_fallbacks = list(dict.fromkeys([*state_fallbacks, *(
            os.path.join(os.path.realpath(os.path.dirname(s)), os.path.basename(s)) for s in state_fallbacks if s)]))
        self.standing = set(standing)  # T-0119: the project's standing yeses (core only)
        self.trusted = bool(trusted)  # T-0120: /fm-trust on: the guard file and Claude Code settings too
        # T-0234: (a builder's worktree, its project's main checkout) — every write outside the worktree is refused but
        # scratch, and the main checkout is never scratch (even under /tmp)
        self.confine = confine
        self.unbriefed = unbriefed  # T-0308: the project's root while no task is active — writes inside wait for one


class Block:
    def __init__(self, category, detail):
        self.category, self.detail = category, detail
        self.rule = rule_id(category, str(detail))  # T-0672: which check fired, for fire counts

    def __repr__(self):
        return f"Block({self.category!r}, {self.detail!r})"


def rule_id(category, detail):
    """T-0672: a stable name for the check behind a refusal: its category and the first words of its wording, with
    paths, quoted text and numbers taken out (rm -rf ~ and rm -rf /x are one rule)."""
    words = re.sub(r"\S*[/~$\\]\S*|\S*\d\S*|`[^`]*`|'[^']*'|\"[^\"]*\"", " ", detail.lower())
    ext = os.path.splitext(detail.split()[0])[1].lstrip(".").lower() if "/" in detail else ""  # T-0894: kinds apart
    path = ("path-" + ext if ext.isalnum() else "path") if "/" in detail else "other"
    return f"{category}:{'-'.join(re.findall(r'[a-z]+', words)[:4]) or path}"


def findings(tool_name, tool_input, ctx):
    """Every (category, detail) a tool call touches, allowed or not."""
    if tool_name in FILE_TOOLS:
        raw = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
        path = _resolve(_expand(raw, ctx), ctx.cwd)
        return [(cat, path) for cat in classify_write(path, ctx)]
    if tool_name == "Bash":
        return check_bash(tool_input["command"], ctx)
    if tool_name == "Read":  # T-1224
        path = _resolve(_expand(str(tool_input.get("file_path") or ""), ctx), ctx.cwd)
        return [(cat, path) for cat in classify_read(path, ctx)]
    return []


def check(tool_name, tool_input, ctx, found=None):
    found = findings(tool_name, tool_input, ctx) if found is None else found
    for cat in CATEGORIES:
        for got, detail in found:
            if got == cat and (got in NOT_AUTHORIZABLE or got not in ctx.allow):
                if got == "core" and ("core" in ctx.standing and _standing_covers(detail, ctx)
                                      or ctx.trusted and _trust_covers(detail, ctx)):
                    continue
                if got == "brief" and tool_name == "Bash" and _focuses(tool_input.get("command") or ""):
                    detail += _FOCUS_LATE  # T-0404: the line's own fm focus hasn't run when the guard reads it
                return Block(got, detail)
    plug = [d for got, d in found if got == "plugin"]
    # T-0201: refreshing listings before one `claude plugin update` is that update (unpinned; it refreshes them itself)
    if plug.count(_UPDATE) == 1 and all(d in (_UPDATE, _MARKET_UPDATE) for d in plug):
        plug = [_UPDATE]
    if len(plug) > 1:  # a plugin yes is used up by one change (fmhooks)
        return Block("plugin", "more than one plugin change in one command; one yes covers one change: run each as "
                               "its own command, after its own fm ask")
    return None


def _is_allow(arg):
    """`--allow`, `--allow=…` and any abbreviation argparse would have accepted (fm now rejects those too)."""
    flag = arg.partition("=")[0]
    return len(flag) > 3 and "--allow".startswith(flag)


_ASK = "fm ask {id} {cat} --why \"<what and why>\", then ask the user one yes/no question; their yes grants it"


_FOCUS_LATE = " (this command's own fm focus hasn't run yet: the guard reads the whole command first)"


def _focuses(cmd):
    """T-0404: whether a command focuses a task itself (fm focus, fm task new … --focus)."""
    try:
        return any(a[:1] == ["focus"] or (a[:2] == ["task", "new"] and "--focus" in a) for a in fm_calls(cmd))
    except Exception:
        return False


def _hint(detail, cat=""):
    """T-0185: when the guard couldn't pin the target down, the rewrite that lets it (a false block cost a guess)."""
    research = (" If it is a download or notes for the project's research, write it to the scratchpad and file it with "
                "fm research add NAME --file PATH (it replaces an existing NAME; add --append to keep it).") if cat == "state-direct" else ""  # T-0814
    if "(not known before it runs" in detail:
        return (" If the target is elsewhere, name it literally or set its variable once before any loop, pipe or "
                "branch (D=/path; for …), and chain a cd with &&, so the guard can read where it writes." + research)
    if "unresolvable target" in detail:
        return (" If it is elsewhere, name the path literally, or set the variable once before any loop or pipe."
                + research)
    if re.fullmatch(r"downloaded content piped into python[0-9.]*", detail):  # T-0395
        return (" A python -c that only reads the download as data (json.load(sys.stdin)) passes when every command "
                "before it, or after it in its pipeline, is a plain data tool that writes no file (curl -s, jq, head, "
                "tail, sleep) or sets a new name (T=…), and no & runs anything beside it: run a program that writes "
                "files, or a redirect, as its own command or after python's pipeline (; git log).")
    if "is written earlier in this command and run here" in detail:  # T-1289
        return " Write the script in one command, run it in the next command (Edit/Write tool or cat > f <<'EOF')."
    if detail.endswith(_FOCUS_LATE):
        return " Run the fm focus (or fm task new … --focus) as its own command, then this one."
    if detail.endswith("; git merge)"):
        return (" On Foreman's own repo, land a reviewed builder branch with fm lane merge ID: it merges --no-ff and "
                "checks each file it changes as that task's write.")
    if detail.endswith("(written from interpreter code)"):
        return (" If the script only writes other files, keep it to builtin open() on literal paths with no import but "
                "re, json, textwrap or sys, so only those count, or use the Edit tool.") + research
    return research


def message(block, ctx):
    detail = block.detail if isinstance(block.detail, str) else ""
    where = ""  # T-1125: a shell left inside state/ by an earlier cd turns a relative path into a state write
    if detail.endswith("(written from interpreter code)") and _under(ctx.cwd or "", os.path.join(ctx.foreman_home, "state")):
        where = f" The shell is in {ctx.cwd}, so a relative path lands there: use an absolute path or cd out first."
    return _message(block, ctx) + where + _hint(detail, block.category)


def _message(block, ctx):
    cat, detail = block.category, block.detail
    tid = ctx.task_id or "<ID>"
    if cat == "self-authorize":
        return (f"Foreman guard: blocked self-authorize: {detail}. Protected core (Foreman code, rules, evals, "
                f"BUILD_PROMPT.md, settings) and remote sessions need the user's approval, which an agent can't grant: "
                + _ASK.format(id=tid, cat="<" + "|".join(sorted(USER_ONLY)) + ">") + ".")
    if cat == "confine":
        return (f"Foreman guard: blocked confine: {detail} is outside this builder's worktree ({ctx.confine[0]}). A builder "
                f"writes only there (and in scratch); report what needs changing elsewhere to the main thread.")
    if cat == "brief":
        return (f"Foreman: no active task in this project, so {detail} can't be edited yet. One command starts a small "
                f"task: fm task new \"<title>\" --type FIX --tier S --ac \"<done when>\" --step \"<step>\" --focus "
                f"(bigger work: /foreman:intake; fm next says what's next).")
    if cat == "state-direct":
        diff = re.search(r"/audits/(T-\d+)\.diff$", str(detail))  # T-0413
        return (f"Foreman guard: blocked state-direct: {detail} is Foreman state. Change it through fm "
                f"(fm task …, fm capture, fm checkpoint{f'; fm audit prep {diff[1]} rewrites it' if diff else ''}); "
                f"direct writes are never authorized.")
    if ctx.task_id:
        how = f"fm task set {ctx.task_id} --allow {cat} (records it in the brief), then retry"
    else:
        how = (f"create or focus a task first (fm task new \"…\" --type T --tier S, or fm focus ID), "
               f"then fm task set <ID> --allow {cat}, then retry")
    if cat in USER_ONLY:  # rules/foreman.md, README and MASTER name these categories too
        what = f"{detail} is protected core" if cat == "core" else detail
        return f"Foreman guard: blocked {cat}: {what}. To authorize: " + _ASK.format(id=tid, cat=cat) + "."
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
    if re.match(r"~[\w.-]+(/|$)", t):  # ~user (T-0175 review)
        t = os.path.expanduser(t)
    return t.replace("${HOME}", ctx.home).replace("$HOME", ctx.home)


def _unresolvable(tok):
    return "$" in tok or "`" in tok or bool(re.match(r"~[+-]", tok))  # ~+ and ~- are $PWD and $OLDPWD


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
    if any(_under(path, s) for s in getattr(ctx, "scratch", ()) or ()):
        return False  # T-0169: a scratch file's name says nothing of its contents (its real path is checked too)
    stem, ext = os.path.splitext(base)
    if ext.lower() in _DOC_EXT or ext.lower() in (".example", ".sample", ".template", ".dist", ".tmpl"):
        return False  # T-0386: secrets.yaml.example is the placeholder copy, as .env.example is
    if re.search(r"(^|[._-])(secrets?|credentials?)([._-]|$)", stem.lower()):
        return True
    # a design system's tokens (colours, spacing, durations) aren't auth tokens (JARVIS: design/tokens.json was refused)
    design = re.search(r"/(design|themes?|styles?|ui)/", path.lower()) or re.match(r"(design|theme|style)[._-]", stem.lower())
    return bool(re.search(r"(^|[._-])tokens?([._-]|$)", stem.lower())) and not (design and stem.lower() != "token")


_CRED_PUBLIC = {".ssh": {"known_hosts", "known_hosts.old", "authorized_keys", "authorized_keys2", "config"},
                ".aws": {"config"}}  # profiles and regions


def classify_read(path, ctx):
    """T-1224: a read of the home folder's credential folders and files (their public parts aside: *.pub, ~/.ssh's
    known_hosts, authorized_keys and config, ~/.aws/config), where the path is and where it really is. A project's .env
    or *.key is the project's own: its reads stay ordinary."""
    for p in _variants(re.sub(r"^/+", "/", path)):
        if p.endswith(".pub") or os.path.basename(p) in _CRED_PUBLIC.get(
                os.path.relpath(os.path.dirname(p), ctx.home), ()):
            continue
        if any(_under(p, os.path.join(ctx.home, d)) for d in _CRED_DIRS) or p in {
                os.path.join(ctx.home, f) for f in _CRED_FILES}:
            return ["credentials"]
    return []


# T-1224: commands whose file arguments are read (a tool that only uses a key, ssh or ssh-add, is not a read of it)
_READERS = {"cat", "tac", "less", "more", "most", "head", "tail", "nl", "sort", "uniq", "cut", "paste", "fold", "rev",
            "cp", "scp", "rsync", "tar", "zip", "gzip", "bzip2", "xz", "zstd", "base64", "base32", "basenc", "xxd", "od",
            "hexdump", "strings", "bat", "batcat", "view", "vi", "vim", "nvim", "nano", "emacs", "diff", "cmp", "iconv",
            "grep", "egrep", "fgrep", "zgrep", "rg", "ag", "awk", "gawk", "mawk", "sed", "jq", "yq"}
_PATTERN_FIRST = {"grep", "egrep", "fgrep", "zgrep", "rg", "ag", "awk", "gawk", "mawk", "sed", "jq", "yq"}
_SENDERS = {"curl", "wget", "nc", "ncat", "netcat", "socat", "telnet"}
_SKIPS = ("--exclude", "--include", "--exclude-from", "--include-from")
_VALUE_OPTS = {"scp": ("-i", "-F", "-o", "-c", "-J", "-l", "-P", "-S", "-D", "-X") + _SKIPS,
               "rsync": ("-e", "--rsh", "-f", "--filter", "--files-from", "--log-file", "-T", "--temp-dir") + _SKIPS,
               "tar": ("-C", "--directory", "-X", "-T", "--files-from") + _SKIPS}
# security review: these options read the file they name (a list of names or patterns)
_LIST_OPTS = {"rsync": ("--files-from", "--exclude-from", "--include-from"),
              "tar": ("-X", "-T", "--files-from", "--exclude-from", "--include-from")}


def _read_targets(name, args):
    """The files a reading command reads: its operands (a grep-like's first one is its pattern, unless -e or -f gives
    it; tar's relative ones are under its -C folder), the lists tar and rsync read names from, and dd's if=."""
    if name == "dd":
        return [a[3:] for a in args if a.startswith("if=")]
    if name not in _READERS:
        return []
    takes = _VALUE_OPTS.get(name, ())  # review: scp -i KEY uses the key; tar --exclude .ssh names what it skips
    pos, cdir = [], None
    for i, a in enumerate(args):
        if name == "tar" and (i and args[i - 1] in ("-C", "--directory") or a.startswith("--directory=")):
            cdir = a.split("=", 1)[1] if a.startswith("--directory=") else a
        elif not a.startswith("-") and not (i and args[i - 1] in takes):
            pos.append(a if cdir is None or a.startswith(("/", "~", "$")) else os.path.join(cdir, a))
    if name in _PATTERN_FIRST and not any(re.match(r"-[a-zA-Z]*[ef]|--(regexp|file|expression|from-file)", a)
                                          for a in args):
        pos = pos[1:]
    return pos + _opt_values(args, *_LIST_OPTS.get(name, ()))


def _sent_files(name, args):
    """T-1224: (files, reads stdin) a network sender attaches: curl's -d/--data*/--json @F, -F x=@F or x=<F and -T F;
    wget's --post-file/--body-file; nc, socat and telnet send their stdin."""
    if name in ("nc", "ncat", "netcat", "socat", "telnet"):
        return [], True
    if name == "wget":
        files = _opt_values(args, "--post-file", "--body-file")
    else:
        files = [v[1:] for v in _opt_values(args, "-d", "--data", "--data-binary", "--data-ascii", "--json")
                 if v.startswith("@")]
        files += [v.split("@", 1)[1] for v in _opt_values(args, "--data-urlencode") if "@" in v.split("=", 1)[0]]
        files += [m[1] for v in _opt_values(args, "-F", "--form") for m in [re.search(r"=[@<]([^;]*)", v)] if m]
        files += _opt_values(args, "-T", "--upload-file")
    stdin = [f for f in files if f in ("-", ".", "/dev/stdin")]
    return [f for f in files if f not in stdin], bool(stdin)


_ENVIRON = re.compile(r"/proc/[^/\s]+/environ$")


def _prints_environment(c):
    """env, printenv (no names), set, export -p or declare -x print the whole environment; or a read of /proc/*/environ."""
    argv, _ = _strip_wrappers(c.argv)  # env CMD is a wrapper (it runs CMD); env with no command is left as nothing
    if not argv:
        return any(os.path.basename(a) == "env" for a in c.argv)
    name, args = os.path.basename(argv[0]), argv[1:]
    if any(_ENVIRON.search(a) for a in args):
        return True
    return (name == "printenv" and not _positionals(args) or name in ("set", "export", "declare", "typeset")
            and all(a in ("-p", "-x", "-px", "-xp") for a in args) and (name != "set" or not args))


# T-1224: chmod/chown/chgrp -R, or a mode that opens write to others, on / , the home folder or a system folder:
# folders always the system's (anything under them), and folders whose top only is (/var, /opt, /home: what's inside
# may be the user's). /dev, /proc and /sys count inside only recursively: chmod 666 /dev/ttyUSB0 is a dev box's chore
_SYS_TREES = ("/etc", "/usr", "/bin", "/sbin", "/lib", "/lib32", "/lib64", "/boot", "/System", "/Library", "/private/etc")
_DEV_TREES = ("/dev", "/proc", "/sys")
_SYS_TOPS = ("/", "/var", "/opt", "/srv", "/home", "/root", "/Users", "/private", "/snap", "/run", "/mnt", "/media")
_MODE_OPT = re.compile(r"--\S+|-[RfvchHLP]+")


def _opens_mode(mode, bits):
    """A mode that gives group or other any of `bits` ("w", or "wx"): 0775, g+w, o=rwx, +w (no who: all, less the
    umask). Taking them away (go-w) or setting them for the owner only (u+w, 0700) is no hazard."""
    if re.fullmatch(r"[0-7]{1,4}", mode):
        mask = (2 if "w" in bits else 0) | (1 if "x" in bits else 0)
        return any(int(d) & mask for d in mode.zfill(3)[-2:])
    for cl in mode.split(","):
        m = re.fullmatch(r"([ugoa]*)([+=])([rwxXst]*)", cl)
        if m and set(m[3]) & set(bits + ("X" if "x" in bits else "")) and (not m[1] or set(m[1]) & set("goa")):
            return True
    return False


def _mode_targets(name, args):
    """(targets, recursive) of a chmod/chown/chgrp that changes them recursively (chmod: opening write or exec to
    others) or opens write to others; ([], False) for any other."""
    if name not in ("chmod", "chown", "chgrp"):
        return [], False
    words = [a for a in args if not _MODE_OPT.fullmatch(a) and a != "--"]
    recursive = any(a.startswith("--rec") or re.fullmatch(r"-[RfvchHLP]*R[RfvchHLP]*", a) for a in args)
    if any(a.startswith("--ref") for a in args) or not words:
        return (words, True) if recursive else ([], False)
    if name != "chmod":
        return (words[1:], True) if recursive else ([], False)
    if _opens_mode(words[0], "wx" if recursive else "w"):
        return words[1:], recursive
    return [], False


def classify_system_mode(path, ctx, recursive=True):
    for p in _variants(re.sub(r"^/+", "/", os.path.normpath(path))):  # //etc is /etc; a link is where it points
        if _SAFE_DEV.match(p):  # /dev/null is 666 already
            continue
        if p in _SYS_TOPS + _DEV_TREES + (os.path.normpath(ctx.home),) or any(
                _under(p, t) for t in _SYS_TREES + (_DEV_TREES if recursive else ())):
            return ["system"]
    return []


# T-0340: where Codex, Gemini CLI and opencode load Foreman's hooks from (user-wide or a project's): editing one can
# switch the guard off in that agent, as Claude Code's settings can in Claude
_AGENT_WIRING = re.compile(r"/\.codex/(?:hooks\.json|config\.toml)$|/\.gemini/settings\.json$|/opencode\.jsonc?$|"
                           r"/\.?opencode/plugins?(?:/|$)")


def _is_core(path, ctx):
    """Protected core: all Foreman code (it enforces the guard), the rules, the eval suite, the spec and settings."""
    fh = ctx.foreman_home
    files = {os.path.join(fh, f) for f in ("plugin/rules/foreman.md", "BUILD_PROMPT.md")}
    dirs = [os.path.join(fh, "plugin", d) for d in _CORE_DIRS]
    codex = os.environ.get("CODEX_HOME")
    return path in files or any(_under(path, d) for d in dirs) or path == os.path.join(ctx.home, ".claude.json") or \
        bool(re.search(r"/\.claude/settings(\.local)?\.json$", path) or _AGENT_WIRING.search(path)) or \
        bool(codex) and path in (os.path.join(codex, "hooks.json"), os.path.join(codex, "config.toml"))


def _plain_path(detail):
    """T-0180: the one file a finding names, for a standing or trusted yes to cover: the path itself, or written from
    interpreter code; None for anything else (a tree write, a target not known before it runs, a relative path)."""
    if not isinstance(detail, str):
        return None
    path = detail.removesuffix(" (written from interpreter code)")
    return path if path.startswith("/") and " (" not in path else None


def _standing_covers(path, ctx):
    """A standing core yes (T-0119) covers Foreman's own code, rules, evals and spec; never this guard file, Claude
    Code's settings or Foreman state, which still ask each time."""
    fh, path = ctx.foreman_home, _plain_path(path)
    if path is None or _under(os.path.join(fh, "plugin", "lib", "fmguard.py"), path):
        return False  # not a path, the guard itself, or a whole-tree write that includes it
    return path in {os.path.join(fh, f) for f in ("plugin/rules/foreman.md", "BUILD_PROMPT.md")} or any(
        _strictly_under(path, os.path.join(fh, "plugin", d)) for d in _CORE_DIRS)


def _trust_covers(path, ctx):
    """/fm-trust on (T-0120) covers every core file, the guard and Claude Code settings included; never Foreman state
    (only fm writes it) or a whole-tree write."""
    path = _plain_path(path)
    if path is None:
        return False
    states = [os.path.join(ctx.foreman_home, "state"), ctx.state_dir, *ctx.state_fallbacks]
    return not any(d and _under(path, d) for d in states)


_SHELL_RC = {".bashrc", ".bash_profile", ".bash_login", ".bash_logout", ".profile", ".zshrc", ".zprofile", ".zshenv",
             ".zlogin", ".zlogout", ".xprofile", ".xinitrc", ".xsessionrc", ".config/fish/config.fish"}
_LATER_DIRS = (".config/systemd", ".config/autostart", ".config/environment.d", ".config/fish/conf.d",
               ".config/fish/functions", ".bashrc.d", ".local/share/applications")


def _runs_later(p, ctx):
    """Code that runs later, outside the session: user units and autostart entries, shell startup files, git hooks."""
    home = ctx.home
    return (any(p == os.path.join(home, f) for f in _SHELL_RC) or any(_under(p, os.path.join(home, d))
                                                                      for d in _LATER_DIRS)
            or "/.git/hooks/" in p or _GIT_CONFIG_FILE.search(p) is not None
            or p in (os.path.join(home, ".gitconfig"), os.path.join(home, ".config", "git", "config")))


# T-1107: a git config file can set core.hooksPath, a `!` alias or a filter driver, as `git config` can (_git_config_code)
_GIT_CONFIG_FILE = re.compile(r"/\.git/(?:worktrees/[^/]+/)?config(?:\.worktree)?$", re.I)  # I: macOS folds case


def _protected_roots(ctx):
    """(path, category) of everything the guard protects, for writes that cover a whole tree."""
    fh, cl = ctx.foreman_home, os.path.join(ctx.home, ".claude")
    roots = [(os.path.join(fh, "plugin", d), "core") for d in _CORE_DIRS]
    roots += [(os.path.join(ctx.home, f), "core") for f in (".codex/hooks.json", ".codex/config.toml",  # T-0340
                                                             ".gemini/settings.json", ".config/opencode")]
    roots += [(os.path.join(fh, "plugin", "rules", "foreman.md"), "core"), (os.path.join(fh, "BUILD_PROMPT.md"), "core"),
              (os.path.join(ctx.home, ".claude.json"), "core"), (os.path.join(cl, "plugins"), "plugin")]
    # user-wide Claude Code settings (a project's own are handled in classify_tree)
    roots += [(os.path.join(ctx.home, ".claude", f), "core") for f in ("settings.json", "settings.local.json")]
    # Foreman state inside a tree write: the user may approve it (core); a direct write never is (state-direct)
    roots += [(d, "core") for d in [os.path.join(fh, "state"), ctx.state_dir, *ctx.state_fallbacks] if d]
    roots += [(os.path.join(ctx.home, d), "credentials") for d in _CRED_DIRS + _CRED_FILES]
    return roots


def classify_tree(path, ctx):
    """A checkout, extraction or recursive copy at `path` can rewrite anything under it: the protected paths it
    contains, as categories (classify_write covers what `path` itself is under)."""
    cats = []
    for p in _variants(path):
        cats += [cat for root, cat in _protected_roots(ctx) if _under(os.path.normpath(root), p)]
        # this project's .claude/settings*.json, for writes aimed into the project (cp -r x .claude/), not a checkout
        # at its root: branch work in the user's own repo is ordinary
        pr = ctx.project_root
        if pr and _strictly_under(p, pr) and any(_under(os.path.join(pr, ".claude", f), p)
                                                  for f in ("settings.json", "settings.local.json")):
            cats.append("core")
    return list(dict.fromkeys(cats))


def _new_context_file(p, ctx):
    """Creating a skill, agent or command (user-wide or this project's) adds always-on context to every session there;
    editing one that exists is ordinary work. A whole folder (copied, moved, linked or extracted) counts too: aimed at
    the skills/agents/commands folder itself, or a new entry directly in it."""
    q = os.path.normpath(p)
    for d in (os.path.normpath(os.path.join(base, ".claude", kind)) for base in (ctx.home, ctx.project_root) if base
              for kind in ("skills", "agents", "commands")):
        if q == d or (_under(q, d) and not os.path.exists(q) and (q.endswith(".md") or os.path.dirname(q) == d)):
            return True
    return False


def classify_unlink(path, ctx):
    """T-0412: rm of a symlink (no trailing slash) removes the link, never what it points at: judged by its own path."""
    return classify_write(path, ctx, real=not os.path.islink(path))


def classify_write(path, ctx, real=True):
    cats = []
    # a link (real=False) is judged where it is, and where its folder really is (a link inside a linked folder)
    for p in (_variants(path) if real else {path, os.path.join(os.path.realpath(os.path.dirname(path)),
                                                                os.path.basename(path))}):
        mirror = os.path.join(ctx.project_root, ".foreman") if ctx.project_root else None  # fm sync writes it
        if any(d and _under(p, d) for d in [os.path.join(ctx.foreman_home, "state"), ctx.state_dir,
                                            *ctx.state_fallbacks, mirror]):
            cats.append("state-direct")
        if _is_core(p, ctx):
            cats.append("core")
        if _is_credential(p, ctx):
            cats.append("credentials")
        if (p.startswith("/dev/") and not _SAFE_DEV.match(p)) or _runs_later(p, ctx):
            cats.append("system")  # device files; persistence that outlives the session
        if _under(p, os.path.join(ctx.home, ".claude", "plugins")) or _new_context_file(p, ctx):
            cats.append("plugin")  # installed plugins, or a new skill/agent/command: what runs in every session
        lane, main = getattr(ctx, "confine", None) or (None, None)
        if lane and not _under(p, lane) and not (p.startswith("/dev/") and _SAFE_DEV.match(p)) and (
                _under(p, main or "/nonexistent") or not any(_under(p, s) for s in ctx.scratch)):
            cats.append("confine")
        root = getattr(ctx, "unbriefed", None)  # strictly inside: a checkout-wide git write (merge, pull) is no edit
        if root and _strictly_under(p, root) and "state-direct" not in cats and not any(  # a scratch dir holding the
                _under(p, d) for d in [*ctx.scratch, os.path.join(ctx.home, ".claude", "projects")]  # project (/tmp)
                if not _under(root, d)):  # doesn't make the project scratch
            cats.append("brief")
    return list(dict.fromkeys(cats))


# ---------------------------------------------------------------- shell parsing

class Cmd:
    def __init__(self, argv, redirs, piped, procsub=False, op="", depth=0):
        self.argv, self.redirs, self.piped, self.procsub = argv, redirs, piped, procsub
        self.op = op  # T-0339: the separator before it (";", "&&", "|", …; "" first)
        self.depth = depth  # T-0414: the ( it sits inside, unclosed: a subshell, $( ) or <( ) (negative: a stray ))
        self.feeds = []  # T-0589: ("<<", delimiter) and ("<<<", word): what it reads on stdin
        self.stdin = None  # T-1129: the file a < (or <>) redirect gives it


_HEREDOC_START = r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1"


def _heredoc_starts(seen, line):
    """T-0178: the heredocs a line starts, only where a shell reads one: outside every quote, comments aside (seen: the
    command's lines before it, bodies left out). A quoted marker is text; taken for a start, it made every later line
    a body, so `echo '<<EOF'` hid the command after it from the guard."""
    before = "".join(x + "\n" for x in seen)
    return [(m.group(1), m.group(2)) for m in re.finditer(_HEREDOC_START, line)
            if _inner_quote(_strip_comments(before + line[:m.start()])) is None]


def _inner_quote(prefix):
    """T-0669: the quote open in the innermost $( … ) or `…` where shell text ends. Each opens a fresh quoting context,
    so the "x <<EOF" in "$(echo "x <<EOF")" is quoted text, though a flat scan reads the outer string as closed there.
    A case arm's ) may close a context early: then more reads as quoted, never less as code (no line hides)."""
    st, esc, i = [["", None, 0]], False, 0  # [kind, quote, paren depth]
    while i < len(prefix):
        ch, top = prefix[i], st[-1]
        if esc:
            esc = False
        elif ch == "\\" and top[1] != "'":
            esc = True
        elif top[1] == "'":
            top[1] = None if ch == "'" else "'"
        elif ch == "`":
            if top[0] == "`" and top[1] is None:
                st.pop()
            else:
                st.append(["`", None, 0])
        elif ch == "$" and prefix[i + 1:i + 2] == "(":
            st.append(["$(", None, 0])
            i += 2
            continue
        elif top[1] == '"':
            top[1] = None if ch == '"' else '"'
        elif ch in "'\"":
            top[1] = ch
        elif ch == "(" and top[0] == "$(":
            top[2] += 1
        elif ch == ")" and top[0] == "$(":
            if top[2]:
                top[2] -= 1
            else:
                st.pop()
        i += 1
    return "\\" if esc else st[-1][1]


def _lines(text):
    """Newlines as command separators for the tokenizer, placed after each line so a # comment ends at its line (it ran
    to the end of the whole command, hiding every later line: T-0158). T-0669: not a newline inside quotes — that one
    is part of the word, and a second shell (eval 'a\\⏎b') must get it back as written."""
    mask = _mask_quotes(text)
    return "".join(ch + ";" if ch == "\n" and mask[i] == "\n" else ch for i, ch in enumerate(text))


def _ends_body(text, delim, starter):
    """Whether a line ends a heredoc body as bash reads it (T-0286 review): only the exact delimiter, leading tabs
    dropped for <<-. `X ` or ` X` is still body — taken for the end, the lines after it hid from the guard."""
    return text == delim or text.lstrip("\t") == delim and bool(
        re.search(r"<<-\s*(['\"]?)" + re.escape(delim) + r"\1", starter))


# T-0576: a plain expansion of IFS (default: space, tab, newline) reads as the space it splits on. T-0585 (its
# security review): only the plain forms; an operator form (${IFS:+word}) yields any word, and a line that may change
# IFS (named with quotes and backslashes removed, a loop variable, a nameref; IFS=… read scopes to that read) and
# splits anything on it can't be read that way
_IFS_PLAIN = re.compile(r"\$IFS(?![A-Za-z0-9_])|\$\{IFS\}")
_IFS_OP = re.compile(r"\$\{[#!]?IFS(?![A-Za-z0-9_])")
_IFS_NAME = re.compile(r"(?<![A-Za-z0-9_])IFS(?![A-Za-z0-9_])")
_IFS_IN_VALUE = re.compile(r"(?<![\w$])[A-Za-z_]\w*(?:\[[^\]]*\])?\+?=[^\s;&|()<>]*(?:\$IFS(?![A-Za-z0-9_])|\$\{IFS\})")
_IFS_FOR_READ = re.compile(r"(?<![\w$])IFS=(?:\$?'[^'\n]*'|\"[^\"\n]*\"|[^\s;&|'\"])*[ \t]+read\b")  # one line
_READ_REDEFINED = re.compile(r"\b(?:alias|enable|function)\b|\bread\s*\(")
_NAME_COMPUTED = re.compile(  # a variable name built by an expansion: declare $'\x49FS=/', export "$n=/", (( $n = 1 ))
    r"(?:^|[;&|({`\n]|\$\(|\b(?:then|do|else|elif)\s)\s*(?:builtin\s+|command\s+)?(?:"  # at command position
    r"(?:declare|typeset|local|export|readonly|read|mapfile|readarray|getopts|let)\b[^;&|\n]*?\s[^\s=;&|]*[$`'\"\\]"
    r"|(?:declare|typeset|local)\b[^;&|\n]*\s-\w*n|printf\b[^;&|\n]*-v\s*\S*[$`'\"\\])"
    r"|\(\(\s*(?:[^()]*,\s*)?\$\{?\w+\}?\s*(?:[-+*/%^|&]|<<|>>)?=(?!=)|\$\{![^}]*=")  # (( $n = 1 )), not (( a == b ))
_UNQUOTED = re.compile(r"\$[\w{@*#?!$(-]|`")
_RUNS_HERE = re.compile(  # T-0590: code this shell runs that the line doesn't show: eval text, a sourced file
    r"(?:^|[;&|({`\n]|\$\(|\b(?:then|do|else|elif)\s)\s*(?:builtin\s+|command\s+)?(?:eval|source|\.)(?=\s)")


def _ifs_unreadable(cmd):
    """T-0585: why bash's word splitting on this line can't be read (IFS may not be the default), or None."""
    rest = _IFS_PLAIN.sub(" ", cmd)
    if _IFS_OP.search(rest):
        return "IFS is expanded with an operator: the guard can't read the word it yields"
    if _IFS_IN_VALUE.search(_mask_quotes(cmd)):  # T-0592: bash keeps it whole there; a space would end the value
        return "IFS in an assignment's value: the guard can't read where that value is split later"
    why = "IFS may be changed on a line that splits words on it: the guard can't read how bash splits them"
    plain, hidden = rest != cmd, _RUNS_HERE.search(rest)
    data = _ifs_data(cmd) if plain else None
    if data is not None:  # T-0698: IFS only in data, unless eval or source beside it may run it here
        return why if _RUNS_HERE.search(data) or _NAME_COMPUTED.search(_mask_quotes(_strip_heredocs(data))) else None
    if plain and hidden:  # T-0590: eval or source may set IFS out of sight
        return why
    scoped = rest if _READ_REDEFINED.search(rest) else _IFS_FOR_READ.sub(" read", rest)
    # quoted text and heredoc bodies are data: check_bash reads what eval, bash -c and bash <<EOF run on their own;
    # beside a plain use or an eval/source they aren't (T-0590: eval 'IFS=m'; "r$IFS" -rf ~)
    bare = _mask_quotes(_strip_heredocs(scoped))
    text = scoped if plain or hidden else bare
    if _IFS_NAME.search(re.sub(r"[\\'\"]", "", text)):  # I""FS and I\FS are IFS to bash
        split = plain or "$" in text or "`" in text
    elif _NAME_COMPUTED.search(bare):  # ponytail: a computed name is refused only beside an expansion that splits
        split = plain or _UNQUOTED.search(bare)
    else:
        return None
    return why if split else None


def _ifs_data(cmd):
    """T-0698: cmd with one piece of data blanked when every IFS on the line, plain or named, is in it: a '…' string
    or the body of a quoted-delimiter heredoc no shell on the line reads. Nothing in it expands, and a shell that runs
    it (eval, bash -c) reads it whole on its own. None when IFS is also beside it or in a second piece (bash -c
    'IFS=/ source /dev/stdin' <<< '…${IFS}…'), or where quotes aren't read flat (`…`, and what _mask_quotes leaves)."""
    lines, bodies, seen, i = cmd.split("\n"), [], [], 0
    offs = [0]
    for line in lines:
        offs.append(offs[-1] + len(line) + 1)
    while i < len(lines):
        line, i = lines[i], i + 1
        starts = _heredoc_starts(seen, line)
        seen.append(line)
        for quote, delim in starts:
            first = i
            while i < len(lines) and not _ends_body(lines[i], delim, line):
                i += 1
            bodies.append((offs[first], offs[i], quote))
            i += 1
    code = cmd
    for s, e, _ in bodies:
        code = code[:s] + re.sub(r"[^\n]", " ", code[s:e]) + code[e:]
    fed = any(q for *_, q in bodies) and _stdin_scripts(cmd, _split(_tokens(_lines("\n".join(seen)))))
    mask, pieces = "" if "`" in code else _mask_quotes(code), set()  # same length; quoted text as underscores
    for m in _IFS_PLAIN.finditer(cmd):
        p = m.start()
        body = next((b for b in bodies if b[0] <= p < b[1]), None)
        if body:
            if not body[2] or fed:  # <<E bodies expand; a shell's are code (T-0589)
                return None
            pieces.add(body[:2])
            continue
        o, c = max(mask.rfind("'", 0, p), mask.rfind('"', 0, p)), mask.find("'", p)
        if mask[o:o + 1] != "'" or c < 0 or set(mask[o + 1:c]) != {"_"}:  # "…" expands; code; a comment
            return None
        pieces.add((o + 1, c))
    if len(pieces) != 1:
        return None
    (s, e), = pieces
    out = cmd[:s] + re.sub(r"[^\n]", " ", cmd[s:e]) + cmd[e:]
    return None if _IFS_NAME.search(re.sub(r"[\\'\"]", "", out)) else out


def _ifs_spaces(cmd):
    """T-0576: an unquoted plain IFS expansion as the space bash splits on. T-0590: a # right after it stays a
    literal, not a comment; quoted text is left as it is for the nested check that reads it (bash -c '…')."""
    out, last = [], 0
    for m in _IFS_PLAIN.finditer(_mask_quotes(cmd)):  # same length as cmd, quoted text blanked
        out += [cmd[last:m.start()], " \\" if cmd[m.end():m.end() + 1] == "#" else " "]
        last = m.end()
    return "".join(out) + cmd[last:]


def _join_continued(cmd):
    """Lines as bash reads a command (T-0286 review): one ending in an unescaped backslash outside quotes and comments
    is joined with the next before heredoc bodies are read, so `python3 - <<'X' \\` + `1>FILE` is a redirect on the
    command line, not the first body line. Bodies are kept as they are."""
    lines, out, i = cmd.split("\n"), [], 0
    while i < len(lines):
        line = lines[i]
        i += 1
        while i < len(lines):
            code = _strip_comments("\n".join(out + [line]))
            tail = len(code) - len(code.rstrip("\\"))
            if not (code.endswith("\\") and tail % 2 and _quote_at(code[:-1]) in (None, '"')):  # T-0669: in "…" too
                break
            line = line[:-1] + lines[i]
            i += 1
        starts = _heredoc_starts(out, line)
        out.append(line)
        for _, delim in starts:
            while i < len(lines) and not _ends_body(lines[i], delim, line):
                out.append(lines[i])
                i += 1
            if i < len(lines):
                out.append(lines[i])
                i += 1
    return "\n".join(out)


def _live_heredocs(cmd):
    """The bodies of heredocs with an unquoted delimiter: a shell runs their substitutions (T-0158)."""
    lines, out, seen, i = cmd.split("\n"), [], [], 0
    while i < len(lines):
        line = lines[i]
        i += 1
        for quote, delim in _heredoc_starts(seen, line):
            body = []
            while i < len(lines) and not _ends_body(lines[i], delim, line):
                body.append(lines[i])
                i += 1
            i += 1
            if not quote:
                out.append("\n".join(body))
        seen.append(line)
    return out


def _heredoc_split(cmd):
    """(the command's lines without heredoc bodies, each body's lines in order)"""
    lines, out, bodies, i = cmd.split("\n"), [], [], 0
    while i < len(lines):
        line = lines[i]
        i += 1
        starts = _heredoc_starts(out, line)
        out.append(line)
        for _, delim in starts:
            bodies.append([])
            while i < len(lines) and not _ends_body(lines[i], delim, line):
                bodies[-1].append(lines[i])
                i += 1
            i += 1
    return out, bodies


def _heredocs(cmd):
    """(the command without its heredoc bodies, the bodies)"""
    out, bodies = _heredoc_split(cmd)
    return "\n".join(out), "\n".join(x for b in bodies for x in b)


# T-0589: what may read a heredoc or here-string as code (bash, sh -s, bash /dev/stdin, { bash; }, . /dev/stdin …)
_RUNS_STDIN = re.compile(r"(ba|z|da|k|fi|c|tc|a|mk|ya|po|lk)?sh|busybox|source|\.|eval")
_STDIN_PATHS = {"-", "/dev/stdin", "/dev/fd/0", "/proc/self/fd/0"}
_INLINE = {"sh": "c", "py": "cm", "js": "ep", "pl": "eE", "rb": "e", "php": "rBRFE"}  # flags whose next word is the code
# T-0716: options whose next word is a value, not the script (bash -o posix, python3 -W ignore, node -r ./hook.js)
_OPT_VALUE = {"sh": "oO", "py": "WXQ", "js": "rC", "pl": "IMm", "rb": "IrCEF", "php": "cdz"}
_LONG_VALUE = {"--rcfile", "--init-file", "--require", "--import", "--loader", "--experimental-loader", "--input-type",
               "--conditions", "--title", "--env-file"}
# inline code that runs what it reads on stdin (python3 -c 'exec(sys.stdin.read())', perl -e 'eval <STDIN>');
# json.load, re.compile and ast.literal_eval read data
_RUNS_IT = re.compile(r"(?<![.\w'\"])(?:eval|compile)\b|(?<!['\"])\b(?:exec|execSync|execFile\w*|execv\w*|execl\w*|"
                      r"Function|runpy|run(?:In\w*Context)|system|popen|Popen|subprocess|spawn\w*|instance_eval|"
                      r"class_eval)\b(?!['\"])")  # a quoted word ('system' in rows) names it, doesn't call it
_STDIN_WORD = re.compile(r"stdin|STDIN|<>|readFileSync\(\s*0|/dev/fd/0|php://stdin")
_CAT_SUBST = re.compile(r"\$\(\s*(?:cat\b[^)]*|<\s*/dev/stdin\s*)\)|`\s*cat\b[^`]*`")
_READ_RUNS = re.compile(r"(?:^|[;&|({]|\bdo|\bthen|\belse)\s*(?:eval\b|\"?\$|\S*sh\s+-\w*c\s+\"?\$)")  # read l; $l


def _reads_stdin_code(name, args, via_xargs=False, any_word=False):
    """T-0715: whether a shell or interpreter reads its program from stdin: no script file and no inline code (a pipe
    into it then runs whatever the pipe carries; `curl … | python3 -c '…'` reads data, `| python3` reads code).
    T-0716: an option's value isn't the script, -s reads stdin whatever follows, a word that doesn't look like a path
    isn't taken for a script, and inline code that runs its stdin (or xargs' item) counts."""
    if name in ("source", "."):
        return bool(args) and args[0] in _STDIN_PATHS
    if re.fullmatch(r"[gmn]?awk", name):  # awk '{system($0)}', print | "sh": each input line run as a command
        return any(re.search(r"\bsystem\s*\(|\|\s*\"[^\"]*sh\b", a) for a in args)
    kind = ("sh" if re.fullmatch(r"(ba|z|da|k|fi|c|tc|a|mk|ya|po|lk)?sh|busybox", name) else
            "py" if re.fullmatch(r"python[0-9.]*|pypy[0-9.]*", name) else "js" if name in ("node", "nodejs", "deno", "bun")
            else "pl" if name == "perl" else "rb" if name == "ruby" else "php" if name == "php" else None)
    if kind is None:
        return False
    i, applet = 0, name != "busybox"
    while i < len(args):
        a = args[i]
        i += 1
        if a in _STDIN_PATHS:
            return True
        if a == "--":
            continue
        if a.startswith("--"):
            if kind == "js" and a in ("--eval", "--print") or kind == "sh" and a == "--command":
                return _inline_runs_stdin(kind, args[i] if i < len(args) else None, via_xargs)
            i += a in _LONG_VALUE
            continue
        if a.startswith(("-", "+")) and len(a) > 1:
            for j, f in enumerate(a[1:]):
                if f in _INLINE[kind] and not (kind == "py" and f == "m"):
                    code = a[j + 2:] or (args[i] if i < len(args) else None)
                    loops = kind in ("pl", "rb") and re.search(r"[np]", a[1:j + 1])  # perl -ne: $_ is each stdin line
                    return _inline_runs_stdin(kind, code if kind != "sh" else (args[i] if i < len(args) else None),
                                              via_xargs, loops)
                if kind == "py" and f == "m":
                    return False  # a module reads stdin as data (python3 -m json.tool)
                if kind == "sh" and f == "s" and a[0] == "-":
                    return True  # sh -s ARGS: the arguments are $1…, the script is stdin
                if f in _OPT_VALUE[kind]:
                    i += j == len(a) - 2  # -o VALUE; -Wignore holds its own
                    break
            continue
        if not applet:
            if a not in ("sh", "ash"):
                return False  # another busybox applet
            applet = True
            continue
        return not (any_word or re.search(r"[/.]", a))  # a script file; a bare word (bash posix) isn't clearly one
    return True


def _inline_runs_stdin(kind, code, via_xargs, loops=False):
    """Whether inline code (sh -c CODE, python3 -c CODE …) runs what it reads on stdin."""
    if code is None or via_xargs and code.strip() in ("{}", '"$@"', "$@", "$*", "$1"):
        return True  # no code here: xargs supplies it from the pipe
    if kind != "sh":
        return bool(_RUNS_IT.search(code) and (loops or _STDIN_WORD.search(code)))
    if _CAT_SUBST.search(code) and re.search(r"\beval\b|\b(?:ba|z|da|k)?sh\s+-\w*c", code):
        return True  # eval "$(cat)"
    if re.search(r"\bread\b", code) and _READ_RUNS.search(code):
        return True  # while read l; do $l; done
    for x in _split(_tokens(code)):
        argv, inner = _strip_wrappers(x.argv)
        if argv and not x.piped and not x.feeds and _reads_stdin_code(os.path.basename(argv[0]), argv[1:], inner):
            return True  # exec bash, source /dev/stdin: it inherits the pipe
    return False


def _stdin_scripts(cmd, cmds):
    """T-0589: the heredoc bodies and here-string words on a line that also runs a shell, source or eval: which of
    them a shell reads as its script isn't modelled (its review: /dev/stdin, a group, -c 'source /dev/stdin'), so
    all of them, read as commands"""
    feeds = [f for x in cmds for f in x.feeds]

    def reads(x):  # T-0714 (JARVIS): `. .venv/bin/activate` or `bash ./run.sh` runs a file, not its stdin
        argv, xargs = _strip_wrappers(x.argv)
        name = os.path.basename(argv[0]) if argv else ""
        return name == "eval" or bool(_RUNS_STDIN.fullmatch(name)) and _reads_stdin_code(name, argv[1:], xargs)
    if not feeds or not any(reads(x) or x.feeds and re.search(r"[$`]", _name(x.argv))
                            for x in cmds):  # T-0669: $X <<EOF, when that $X is the one fed
        return []
    return [w for op, w in feeds if op == "<<<"] + (["\n".join(b) for b in _heredoc_split(cmd)[1]]
                                                    if any(op == "<<" for op, _ in feeds) else [])


def _strip_heredocs(cmd):
    return _heredocs(cmd)[0]


def _drop_data_heredocs(cmd, only=None):
    """T-0171: the command without the bodies of heredocs that only write text: cat or tee as the line's first word,
    a quoted delimiter (nothing in the body expands) and no pipe or substitution on the line. For the interpreter gate
    only: a script written with cat isn't run by writing it. Anything else keeps its body, and so does a data
    heredoc whose line `only` (when given) rejects."""
    lines, out, seen, i = cmd.split("\n"), [], [], 0
    while i < len(lines):
        line = lines[i]
        i += 1
        starts = _heredoc_starts(seen, line)
        out.append(line)
        seen.append(line)
        for quote, delim in starts:
            # T-1141: fm edit reads its heredoc as edit blocks it applies through the guard's own Edit check, never runs it
            data = bool(quote) and not re.search(r"[|`;&]|\$\(", line) and (
                line.split()[:2] == ["fm", "edit"]
                or line.split()[:1] in (["cat"], ["tee"]) and (only is None or only(line)))
            while i < len(lines) and not _ends_body(lines[i], delim, line):
                if not data:
                    out.append(lines[i])
                i += 1
            if i < len(lines):
                out.append(lines[i])
                i += 1
    return "\n".join(out)


def _strip_comments(text):
    """T-0161 review: a # starts a comment only at the start of a word outside quotes; shlex's own commenters also cut
    at the # in `echo a#b; rm …` and hid the rest of the line. Under $'…' quoting nothing is cut (fails closed)."""
    if "$'" in text:
        return text
    out, q, i = [], None, 0
    while i < len(text):
        ch = text[i]
        if ch == "\\" and q != "'":
            out.append(text[i:i + 2])
            i += 2
            continue
        if q:
            q = None if ch == q else q
        elif ch in "'\"":
            q = ch
        elif ch == "#" and (i == 0 or text[i - 1] in " \t\n;&|(<>"):  # after ) it may end a $(…) word (T-0163)
            i = text.find("\n", i)
            if i < 0:
                break
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def _tokens(cmd):
    try:
        lex = shlex.shlex(_strip_comments(cmd), posix=True, punctuation_chars=";&|()<>")
        lex.whitespace_split = True
        lex.commenters = ""
        return list(lex)
    except ValueError:
        return re.sub(r"([;&|()])", r" \1 ", cmd).split()  # unbalanced quotes: still split commands apart


def _split(tokens):
    cmds, cur, depth = [], Cmd([], [], False), 0
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if re.fullmatch(r"[;&|()<>]+", t):  # every punctuation run, even one read below as a word (<(( …)
            depth += t.count("(") - t.count(")")
        if t in ("<(", ">("):
            cur.procsub = True
            cmds.append(cur)
            cur = Cmd([], [], False, depth=depth)
            i += 1
            continue
        if re.fullmatch(r"[;&|()]+", t) and not re.fullmatch(r"&>+", t):
            empty = not (cur.argv or cur.redirs or cur.procsub or cur.stdin)  # T-1224: $(< file) reads file
            if t == ";" and empty and cur.op in ("|", "|&", "&&", "||"):
                i += 1  # a newline after | && || continues the command (_lines made it a ;): T-0355 review
                continue
            if not empty:
                cmds.append(cur)
            keep = empty and cur.piped and "(" in t  # T-0581: `| (bash)` and `|⏎(bash)`: the group reads the pipe
            cur = Cmd([], [], t in ("|", "|&") or keep, op=cur.op + t if keep else t, depth=depth)
            i += 1
            continue
        if re.fullmatch(r"[<>&]+\|?", t):
            t = t.rstrip("|")  # >| writes even under noclobber (T-0358)
            nxt = tokens[i + 1] if i + 1 < len(tokens) else ""
            if t == "<" and nxt == "(":
                cur.procsub = True
                cmds.append(cur)
                depth += 1
                cur = Cmd([], [], False, depth=depth)
                i += 2
                continue
            if t.endswith("&") and re.fullmatch(r"\d+|-", nxt):
                i += 2
                continue
            if t in ("<<", "<<<"):
                cur.feeds.append((t, nxt))
            elif t in ("<", "<>"):
                cur.stdin = nxt
            if nxt and (t.startswith(">") or t in ("&>", "&>>", "<>")):
                cur.redirs.append(nxt)
            i += 2
            continue
        cur.argv.append(t)
        i += 1
    if cur.argv or cur.redirs or cur.procsub or cur.stdin:
        cmds.append(cur)
    return cmds


_KEYWORDS = {"do", "then", "else", "elif", "if", "while", "until", "{", "!", "coproc"}  # words before a command


def _strip_wrappers(argv):
    """Drop env assignments and exec wrappers (sudo, env, timeout, xargs, npx…). Returns (argv, via_xargs)."""
    i = 0
    while i < len(argv):
        a = argv[i]
        base = os.path.basename(a)
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*\+?=", a) or a in _KEYWORDS:  # T-0159: `do rm …` is rm; T-0270: NAME+=v
            i += 1
        elif base in ("sudo", "doas"):
            i += 1
            while i < len(argv) and argv[i].startswith("-"):
                i += 2 if argv[i] in ("-u", "-g", "-C", "-D", "-h", "-p", "-r", "-t", "-U") else 1
        elif base in ("nohup", "time", "command", "builtin", "exec", "noglob", "stdbuf", "nice", "ionice", "chronic",
                      "setsid", "busybox"):  # setsid, busybox: T-0160 (the differential test)
            i += 1
            while i < len(argv) and argv[i].startswith("-"):
                i += 2 if argv[i] in ("-n", "-c", "-p") else 1
        elif base == "flock":  # flock [opts] FILE CMD…: the command after the lock file (T-0160)
            i += 1
            while i < len(argv) and argv[i].startswith("-"):
                i += 2 if argv[i] in ("-w", "--timeout", "-E", "--conflict-exit-code") else 1
            i += 1
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
            i += 1 + _xargs_opts(argv[i + 1:])[0]
        elif base in ("npx", "bunx"):
            i += 1
            while i < len(argv) and argv[i].startswith("-"):
                i += 1
        else:
            break
    return argv[i:], any(os.path.basename(a) == "xargs" for a in argv[:i])


def _xargs_opts(words):
    """T-1123: (words xargs's options take, whether one changes how stdin splits or is replaced), read as getopt does:
    a cluster's value options (n s P L E I a d, and the old e i l) swallow the rest of the cluster or the next word."""
    i, odd = 0, False
    while i < len(words) and words[i].startswith("-") and words[i] != "-":
        w = words[i]
        i += 1
        if w == "--":
            break
        if w.startswith("--"):
            odd = odd or bool(re.match(r"--(?:arg-file|delimiter|replace|null|max-lines|eof)", w))
            i += 1 if w in ("--max-args", "--max-procs", "--max-chars", "--arg-file", "--delimiter", "--eof") else 0
            continue
        odd = odd or any(ch in "adEeIiLl0" for ch in w[1:])  # any such letter, even inside a value: doubt is unknown
        for k, ch in enumerate(w[1:], 1):
            if ch in "nsPLEIad":
                i += 1 if k == len(w) - 1 else 0
                break
    return i, odd


def _positionals(args):
    return [a for a in args if not a.startswith("-")]


def _name(argv):
    stripped, _ = _strip_wrappers(argv)
    return os.path.basename(stripped[0]) if stripped else ""


# ---------------------------------------------------------------- bash checks

_SHELLS = re.compile(r"^((ba|z|da|k|fi|c|tc)?sh|python[0-9.]*|perl|ruby|node|php|pwsh)$")
_FETCHERS = {"curl", "wget", "fetch"}
_FETCH_WORD = re.compile(r"(?<![\w./-])(?:\S*/)?(?:curl|wget|(?<!git )fetch)(?![\w.-])")  # T-0421: a fetcher anywhere; T-0937: not `git fetch`
_PRINTED_SUBST = re.compile(r"(\$\(|`)\s*((?:(?:command\s+|builtin\s+)?(?:\S*/)?(?:echo|printf))\s[^`)]*?)\s*(?:\)|`)")
_DOWNLOAD_SUBST = re.compile(r"(\$\(|`)\s*(curl|wget|fetch)\b")


_INTERP_NAMES = r"(?:python|perl|ruby|php)[0-9.]*|py|jruby|truffleruby|irb|node|nodejs|deno|bun"
_INTERP = re.compile(rf"(?:^|[\s;&|(/`])({_INTERP_NAMES})(?=\s|$|[;&|)`])")
_TEXT_TICKS = re.compile(r"(?:python[0-9.]*|py|node|nodejs|deno|bun)$")  # a backtick is only text in these
_WRITE_API = re.compile(
    r"""open\s*\([^)]*['"][rwxab+]*[wxa+][rwxab+]*['"]|\.write_(?:text|bytes)\s*\(|(?:write|append)FileSync|"""
    r"createWriteStream|\bos\.(?:replace|rename|remove|unlink)\b|\bshutil\.\w+\(|\.(?:unlink|rename|replace|touch)\(|"
    r"File\.write|file_put_contents|open\s*\(\s*(?:my\s+)?\$?\w+\s*,\s*['\"]?[>+]")
# T-0344: .replace( stays a write here even with two string arguments: os.replace('a', 'b'), an aliased os or (os) look
# the same as str.replace to a text match, and only a proved script (_open_targets) can tell them apart
_QUOTED = re.compile(r"""(['"])((?:[~/.]|[\w.-]+/)[^'"\s]*)\1""")
_GUARDED_BY_PATH = ("core", "state-direct", "credentials", "plugin", "brief")
# A slash command that changes plugins, MCP servers or config, sent to claude as a prompt (argv, stdin or a heredoc).
_SLASH_BODY = (r"/(?:plugins?\s+(?:install|i|enable|disable|uninstall|remove|update|"
               r"marketplace\s+(?:add|remove|rm|update))|"
               r"mcp\s+(?:add|remove|enable|disable)|config\s+(?:set|add|remove))\b")
_SLASH_CHANGE = re.compile(r"(?:^|[\s'\"])" + _SLASH_BODY)
# Interpreter code that runs claude's plugin/mcp/config subcommands (argv list, split argv array or command string) or
# sends such a slash command. Both an exec API and the command shape must appear, so code that merely mentions them
# isn't blocked.
_CLAUDE_IN_CODE = re.compile(r"""['"]claude['"][^;\n]{0,40}?['"](?:plugins?|mcp|config)['"]|"""
                             r"""['"`]claude\s+(?:plugins?|mcp|config)\b|['"]\s*""" + _SLASH_BODY)
_EXEC_API = re.compile(r"\bsubprocess\b|\bos\.(?:system|popen|exec\w*|spawn\w*)\b|\bPopen\b|child_process|"
                       r"\b(?:exec|execSync|spawn|spawnSync|system)\s*\(")


# Any Foreman module (fm*.py in plugin/lib), so new modules are covered without editing this list. Calls into the entry
# point modules count as mutating; fmcore/fmguard/fmdocs/fmdoctor are mostly read-only, so their mutators are by name.
_FM_INTERNALS = re.compile(r"\b(?:import|from)\s+fm[a-z]+\b|(?:__import__|import_module)\s*\(\s*['\"]fm[a-z]+")
_FM_ENTRY = r"(?:fmcli|fmhooks|fmsetup|fmtidy|fmideas|fmserve|fmplugins)"
_FM_MUTATORS = re.compile(r"\b(?:save_brief|write_meta|update_meta|write_atomic|log_event|regen_views|init_project|"
                          r"add_rule|drop_rule|add_veto|drop_veto|"  # T-0971 review: the user's rules and vetoes
                          r"checkpoint|mutate|cmd_\w+|task_\w+|_resolve_approvals|_activate_fallback|"
                          r"restore_default_state)\s*\(|"
                          rf"\bgetattr\s*\(\s*{_FM_ENTRY}\b|"
                          rf"\b{_FM_ENTRY}\s*\.\s*\w+\s*\(|\bfrom\s+{_FM_ENTRY}\s+import\b|\bimport\s+{_FM_ENTRY}\s+as\b|"
                          rf"(?:__import__|import_module)\s*\(\s*['\"]{_FM_ENTRY}|"
                          # T-0170: a writer imported by name, then called under an alias (from fmcore import x as w)
                          r"\bfrom\s+fm[a-z]+\s+import\s+[^\n;]*\b(?:save_brief|write_meta|update_meta|write_atomic|"
                          r"log_event|regen_views|init_project|checkpoint|mutate|restore_default_state)\b")


_FM_RUN_ARG = re.compile(r"""--run(?:=|\s+)(?:"(?:\\.|[^"\\])*"|'[^']*')""")


def _unescape_ticks(body):
    """A backtick body as the shell runs it: \\`, \\$ and \\\\ lose their backslash (nested backticks: T-0158)."""
    return re.sub(r"\\([`$\\])", r"\1", body)


def _subst_bodies(text, tails=True):
    """Every command-substitution body a shell would run in text (T-0158): `…` and $( … ), nested ones too, bare or
    inside double quotes, never inside single quotes or after a backslash; $(( … )) is arithmetic. Each $( opens a fresh
    quoting context, as in bash. With $'…' quoting (where \\' is a quote) the scan can't follow: every span between
    backticks and every greedy $( … ) is returned instead (fails closed). An unterminated body runs to the end."""
    if "$'" in text:
        return [_unescape_ticks(b) for b in text.split("`")[1::2]] + [text[m.end():] for m in re.finditer(r"\$\(", text)]
    ends = []  # every substitution is also read to the end: a case pattern's ) or a comment can close it early
    bodies, ctx, tick, esc, i = [], [[None, 0, 0]], None, False, 0  # ctx: [quote, body start, paren depth]
    while i < len(text):
        ch, top = text[i], ctx[-1]
        if esc:
            esc = False
        elif ch == "\\" and top[0] != "'":
            esc = True
        elif top[0] == "'":
            top[0] = None if ch == "'" else "'"
        elif tick is not None:
            if ch == "`":
                bodies.append(_unescape_ticks(text[tick:i]))
                tick = None
        elif ch == "`":
            tick = i + 1
        elif ch == "$" and text[i + 1:i + 2] == "(":
            ends.append(text[i + 2:])  # $(( … )) too: bash falls back to a subshell when )) doesn't close it
            last = text.rfind(")")  # T-0669: and, when it ends inside a quote, up to the last ): an outer `)"`
            if last > i + 2 and _quote_at(text[i + 2:]) is not None:  # left it open (whole code stays whole)
                ends.append(text[i + 2:last])
            if text[i + 2:i + 3] != "(":
                ctx.append([None, i + 2, 0])
            i += 2
            continue
        elif ch == '"':
            top[0] = None if top[0] == '"' else '"'
        elif top[0] is None and ch == "'":
            top[0] = "'"
        elif top[0] is None and ch == "(" and len(ctx) > 1:
            top[2] += 1
        elif top[0] is None and ch == ")" and len(ctx) > 1:
            if top[2]:
                top[2] -= 1
            else:
                bodies.append(text[top[1]:i])
                ctx.pop()
        i += 1
    return bodies + ([_unescape_ticks(text[tick:])] if tick is not None else []) + (ends if tails else [])


def _real_fm(argv, ctx):
    """argv runs Foreman's own fm: bare `fm` (the caller has ruled out PATH, alias and function changes), or its real
    path, directly or as python's script. Anything else named fm is just a program (automated review of T-0153)."""
    fm_bin = os.path.realpath(os.path.join(ctx.foreman_home, "plugin", "bin", "fm"))
    same = lambda path: os.path.realpath(os.path.join(ctx.cwd, os.path.expanduser(path))) == fm_bin
    if not argv:
        return False
    if argv[0] == "fm":
        return True
    if re.match(r"^python[0-9.]*$", os.path.basename(argv[0])):
        return len(argv) > 1 and not argv[1].startswith("-") and same(argv[1])
    return same(argv[0])


def _mask_fm(cmd, ctx):
    """The command with each top-level fm command blanked to `fm`: its arguments are data to fm (its --run values are
    checked on their own, substitutions inside are read recursively), so an interpreter named in an fm task's text isn't
    interpreter code (T-0153). Heredoc bodies are kept; where the quote scan can't follow, nothing is blanked."""
    shell, bodies = _heredocs(cmd)
    if ("$'" in shell or len(re.findall(r"(?<!<)<<(?!<)", shell)) != len(re.findall(_HEREDOC_START, shell))
            or "#" in shell or re.search(r"\bPATH\b|\balias\b|\bhash\b|\bfunction\s+fm\b|\bfm\s*\(\s*\)", shell)):
        return cmd  # the quote scan can't follow, or which program `fm` names could change: blank nothing
    out, seg, q, esc = [], [], None, False

    def flush():
        text = "".join(seg)
        argv, _ = _strip_wrappers(_tokens(text))
        fm = _real_fm(argv, ctx)
        # a substitution in fm's arguments runs: keep that segment whole (the $( ) reader misses nested parentheses)
        out.append(" fm " if fm and "$(" not in text and "`" not in text else text)
        seg.clear()
    for ch in shell:
        if esc:
            esc = False
        elif ch == "\\" and q != "'":
            esc = True
        elif q:
            q = None if ch == q else q
        elif ch in "'\"":
            q = ch
        elif ch in ";&|\n()`":
            flush()
            out.append(ch)
            continue
        seg.append(ch)
    flush()
    return cmd if q else "".join(out) + "\n" + bodies  # an unclosed quote: the scan lost track, blank nothing


def _top_level(prefix):
    """True when shell text ending here is outside every quote and escape (a quote scan: wrong only towards False)."""
    return _quote_at(prefix) is None


def _quote_at(prefix):
    """The quote open where shell text ends (None, ' or "); "\\" when it ends inside an escape."""
    q, esc = None, False
    for ch in prefix:
        if esc:
            esc = False
        elif ch == "\\" and q != "'":
            esc = True
        elif q:
            q = None if ch == q else q
        elif ch in "'\"":
            q = ch
    return "\\" if esc else q


_DYNAMIC = {"exec", "eval", "compile", "getattr", "__import__", "import_module", "importlib", "globals", "vars",
            "__builtins__", "builtins", "setattr",
            # code in a string can also run in another process (T-0170, own adversary pass)
            "system", "popen", "Popen", "run", "call", "check_call", "check_output", "getoutput", "getstatusoutput",
            "startfile", "posix_spawn", "posix_spawnp", "fork", "forkpty", "spawnl", "spawnle", "spawnlp", "spawnlpe",
            "spawnv", "spawnve", "spawnvp", "spawnvpe", "execl", "execle", "execlp", "execlpe", "execv", "execve",
            "execvp", "execvpe"}
# a parsed script that imports only these can't load or run the code its strings hold (anything else: read as text)
_PLAIN_IMPORTS = {"re", "json", "os", "sys", "pathlib", "textwrap", "difflib", "collections", "itertools", "functools",
                  "string", "datetime", "time", "shutil", "glob", "fnmatch", "math"}


def _python_units(cmd):
    """(the bodies of quoted heredocs fed straight to python, the rest of the command, the lines that feed them): a
    unit only when it's the line's one heredoc, on a `python - <<` line with no pipe, `;`, `&`, backtick or `$(` —
    after a chain of plain `cd DIR &&` (T-0282: a working directory doesn't change what the code does)."""
    lines, rest, units, starters, seen, i = cmd.split("\n"), [], [], [], [], 0
    while i < len(lines):
        line = lines[i]
        i += 1
        starts = _heredoc_starts(seen, line)
        seen.append(line)
        # T-0315: plain name=value; first (lowercase: a shell variable, never PATH, HOME or LD_* that pick which python
        # runs or what it loads) and the script's own arguments (sys.argv: they pick what it reads, never what it may
        # write, which _open_targets proves from literals) don't change what the code does
        run = re.match(r"\s*(?:[a-z_][a-z0-9_]*=[\w./~@+:=,-]*\s*;\s*)*(?:cd\s+[\w./~@+:=,-]+\s*&&\s*)*"
                       r"(python[0-9.]*\s+-(?:\s+(?:'[^'\n]*'|\"[^\"`\n]*\"|[\w./~@+:=,$-]+))*\s*<<.*)$", line)
        # review (T-0286): bash must read the body the guard parses — no continued line (`\`), no second `<<` form
        # the heredoc scan doesn't know (`<<\E`: the last redirect wins)
        fed = len(starts) == 1 and starts[0][0] and run and not re.search(r"[|`;&\\]|\$\(", run.group(1)) and \
            len(re.findall(r"(?<!<)<<(?!<)", line)) == 1
        (starters if fed else rest).append(line)
        for quote, delim in starts:
            body = []
            while i < len(lines) and not _ends_body(lines[i], delim, line):
                body.append(lines[i])
                i += 1
            if i < len(lines):
                rest.append(lines[i])
                i += 1
            (units if fed else rest).append("\n".join(body))
    return units, rest, starters


# module → (functions it may call, values it may name: flags, exception classes, argv); nothing that holds a module
_PY_PURE = {"re": (set("sub subn search match fullmatch findall finditer split compile escape".split()),
                   set("error I IGNORECASE M MULTILINE S DOTALL X VERBOSE A ASCII".split())),
            "json": ({"loads", "dumps", "load", "dump"}, {"JSONDecodeError"}),
            "textwrap": ({"dedent", "indent", "fill", "wrap", "shorten"}, set()),
            "sys": ({"exit"}, {"argv", "stdin"})}  # T-0344: reading stdin writes nothing
_FRAME_ATTR = re.compile(r"(?:gi|cr|ag|f|tb)_")
_PY_PATH_VARS = ("PYTHONPATH", "PYTHONHOME", "PYTHONUSERBASE", "PYTHONPLATLIBDIR", "PYTHONSTARTUP")  # what imports load
# review: the only builtins a proved script may name (not type: type(f.buffer.raw) is FileIO, which opens files; not
# locals: locals()['__builtins__'].open, or a name rebound behind the binding count)
_PY_BUILTINS = set("""print len str int float bool bytes bytearray list dict set frozenset tuple range enumerate zip
    sorted reversed min max sum any all abs round repr isinstance map filter chr ord hex oct bin format hash iter next
    divmod pow slice input exit Exception ValueError KeyError IndexError TypeError OSError FileNotFoundError
    RuntimeError AssertionError NotImplementedError StopIteration SystemExit UnicodeDecodeError""".split())


def _open_targets(code):
    """T-0176: the paths a python script can write, or None when that can't be proved. Proved when nothing in it can
    reach a module that writes: no import but the pure functions of _PY_PURE (used as module.function only), nothing
    dynamic (_DYNAMIC, breakpoint, help), no dunder or frame attribute, the builtin open never rebound or passed on.
    Builtin open is then its only writer, and every open with a write mode (or one it can't read) must name a literal,
    or a name bound once at the top level to one (+ joins them)."""
    import ast
    import collections
    try:
        tree = ast.parse(code)
    except (SyntaxError, ValueError, MemoryError, RecursionError):
        return None
    nodes = list(ast.walk(tree))
    parent = {c: n for n in nodes for c in ast.iter_child_nodes(n)}
    names = {n.id for n in nodes if isinstance(n, ast.Name)}
    if names & _DYNAMIC or any(x.startswith("__") for x in names) or any(
            isinstance(n, ast.Attribute) and (n.attr in _DYNAMIC or n.attr.startswith("__") or n.attr == "open"
                                              or _FRAME_ATTR.match(n.attr)) for n in nodes) or any(
            isinstance(n, ast.Constant) and isinstance(n.value, str) and n.value.startswith("__") for n in nodes) or \
            any(isinstance(n, (ast.ImportFrom, ast.Match, ast.Global, ast.Nonlocal)) for n in nodes):
        return None
    mods = {a.name for n in nodes if isinstance(n, ast.Import) for a in n.names}
    if any(a.name not in _PY_PURE or a.asname for n in nodes if isinstance(n, ast.Import) for a in n.names):
        return None
    bound = collections.Counter()
    for n in nodes:
        if isinstance(n, ast.Name) and not isinstance(n.ctx, ast.Load):
            bound[n.id] += 1
        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            bound[n.name] += 1
        elif isinstance(n, ast.arg):
            bound[n.arg] += 1
        elif isinstance(n, ast.alias):
            bound[n.name] += 1
        elif isinstance(n, ast.ExceptHandler) and n.name:
            bound[n.name] += 1
    if bound["open"] or any(bound[m] != 1 for m in mods):
        return None
    if {n.id for n in nodes if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)} - set(bound) - _PY_BUILTINS \
            - {"open"}:
        return None  # a builtin outside the plain list
    for n in nodes:
        p = parent.get(n)
        if isinstance(n, ast.Name) and n.id in mods:
            calls, values = _PY_PURE[n.id]
            called = isinstance(parent.get(p), ast.Call) and parent[p].func is p
            if not (isinstance(p, ast.Attribute) and p.value is n and (
                    p.attr in values or (p.attr in calls and called))):
                return None  # the module passed on, a part outside the list (re.enum.bltns…), a function not called
        if isinstance(n, ast.Name) and n.id == "open" and not (isinstance(p, ast.Call) and p.func is n):
            return None
    top = {s.targets[0].id: s.value for s in tree.body if isinstance(s, ast.Assign) and len(s.targets) == 1
           and isinstance(s.targets[0], ast.Name) and bound[s.targets[0].id] == 1}

    def text(e, depth=0):
        if isinstance(e, ast.Constant) and isinstance(e.value, str):
            return e.value
        if isinstance(e, ast.Name) and e.id in top and depth < 20:
            return text(top[e.id], depth + 1)
        if isinstance(e, ast.BinOp) and isinstance(e.op, ast.Add) and depth < 20:
            a, b = text(e.left, depth + 1), text(e.right, depth + 1)
            return None if a is None or b is None else a + b
        return None

    targets = []
    for n in nodes:
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "open":
            if any(k.arg is None for k in n.keywords) or any(isinstance(a, ast.Starred) for a in n.args):
                return None
            kw = {k.arg: k.value for k in n.keywords}
            mode = n.args[1] if len(n.args) > 1 else kw.get("mode")
            m = "r" if mode is None else text(mode)
            if m is None or set(m) & set("wax+"):
                path = text(n.args[0] if n.args else kw.get("file"))
                if path is None:
                    return None
                targets.append(path)
    return targets


def _chain_dir(starters, shell, ctx):
    """T-0774: the one folder every python unit runs in, when each starter changes folder only by `cd DIR &&` links
    (python runs only after each succeeded) to absolute, ~ or ./ ../ targets (no CDPATH lookup, no `cd -`) and nothing
    else in the command changes folder; None when that isn't certain (every named folder counts then). Review: a
    regex for folder changes misses "cd", \\cd, source and eval, so the rest of the command may hold nothing but the
    heredocs' own end lines."""
    ends = {m.group(1) for s in starters for m in [re.search(r"<<-?\s*'(\w+)'", s)] if m}
    if any(line.strip() and line.strip() not in ends for line in shell.splitlines()):
        return None
    dirs = set()
    for s in starters:
        d = ctx.cwd
        for t in re.findall(r"\bcd\s+([\w./~@+:=,-]+)\s*&&", s):
            t = _expand(t, ctx)
            if _unresolvable(t) or not re.match(r"(/|\./|\.\./|\.\.?$)", t):
                return None
            d = _resolve(t, d)
        dirs.add(d)
    return dirs.pop() if len(dirs) == 1 else None


def _proved_writes(cmd, ctx):
    """T-0176: the files a command's python can write, as paths, when every interpreter in it is a quoted heredoc fed
    straight to python whose writes _open_targets proves; None otherwise (the coarse rule decides). A relative path
    after a cd counts in every folder the command names too."""
    units, rest, starters = _python_units(cmd)
    shell = "\n".join(rest)
    around = "\n".join(rest + starters)  # review (T-0286): a cd on the python line itself picks the folder too
    if not units or _INTERP.search(_mask_fm(_drop_data_heredocs(shell), ctx)):
        return None
    # review: python's own settings (PYTHONPATH on a continued line, or inherited) choose what an import runs
    if "PYTHON" in shell or re.search(r"\\\s*$", shell, re.M) or any(os.environ.get(k) for k in _PY_PATH_VARS):
        return None
    targets = []
    for code in units:
        found = _open_targets(code)
        if found is None:
            return None
        targets += found
    bases = [ctx.cwd]
    if re.search(r"(?:^|[\s;&|(])(?:cd|pushd|popd)\b", around):
        only = _chain_dir(starters, shell, ctx)
        bases = [only] if only else bases + [
            d for d in (_resolve(_expand(w, ctx), ctx.cwd) for w in _WORD.findall(around) if not _unresolvable(w))
            if os.path.isdir(d)]
    import ast
    mods = {a.name for code in units for n in ast.walk(ast.parse(code)) if isinstance(n, ast.Import) for a in n.names}
    if any(os.path.exists(os.path.join(b, m + x)) for b in bases for m in mods for x in (".py", "")):
        return None  # python - searches the current folder first: a json.py there would be what runs
    return list(dict.fromkeys(_resolve(_expand(t, ctx), b) for t in targets for b in bases))


_SOURCE_WRITE = re.compile(r"(?:cat\s+>>?\s*|tee\s+(?:-a\s+)?)([\w./~@+-]+)\s*(?:>\s*/dev/null\s*)?<<-?\s*"
                           r"(?:'\w+'|\"\w+\")\s*$")  # a quoted marker: the body is data, never expanded
# T-0981: Foreman's code and tests, in the checkout or in a builder worktree's copy of it
_SOURCE_DIRS = re.compile(r"(?:\.claude/worktrees/[\w.-]+/)?plugin/(?:" + "|".join(_CORE_DIRS) + r"|tests)/")


def _writes_unrun_source(line, cmd, ctx):
    """T-0761: a data heredoc writing one file of Foreman's own code (T-0981: or its tests, or a worktree's copy) that
    the command never names again is a source edit (a core path write the user's yes gates), not interpreter code run
    here. Run or imported by name, it is."""
    m = _SOURCE_WRITE.fullmatch(line.strip())
    if not m:
        return False
    path = _resolve(_expand(m.group(1), ctx), ctx.cwd)
    stem = re.escape(os.path.splitext(os.path.basename(path))[0])
    real = os.path.realpath(path)  # a symlink in plugin/lib to a scratch script isn't Foreman's code
    home = os.path.realpath(ctx.foreman_home)
    rel = os.path.relpath(real, home) if _strictly_under(real, home) else ""
    return bool(_SOURCE_DIRS.match(rel)) and len(re.findall(rf"\b{stem}\b", _drop_data_heredocs(cmd))) == 1


def _run_dir(starter, cwd):
    """The folder `python -` runs in (its sys.path[0]) after the starter's `cd` chain, or None when it can't be known."""
    d = cwd
    for target in re.findall(r"\bcd\s+([\w./~@+:=,-]+)\s*&&", starter):
        target = os.path.expanduser(target)
        d = target if os.path.isabs(target) else os.path.join(d, target) if d else None
    return d


# the cd chain is bounded (unbounded, each separator rescans the chain: quadratic); a longer chain is matched from a
# later link, and the cd before it makes the run folder unknown in _drives_fm
_PY_C = re.compile(r"(?:^|(?<=[\n;&|(]))[ \t]*((?:cd\s+[\w./~@+:=,-]+\s*&&\s*){0,8}(?:/[\w./-]*/)?python[0-9.]*\s+"
                   r"(?:-(?:[bBdEIOPqsSuvV]+|[WX]\s*[\w.:=-]+)\s+)*-[bBdEIOPqsSuvV]*c\s+)"  # not -i: stdin runs after
                   r"""('[^']*'|"(?:[^"\\$`]|\\[\s\S])*")(?=\s|$|[;&|)])""")
_CD = re.compile(r"(?:^|[\s;&|(])(?:cd|pushd|popd)\b")


def _python_c_units(shell):
    """T-1194: (the code of each `python -c CODE` that starts a command at shell top level, CODE one literal word with
    no expansion, after a chain of plain `cd DIR &&`; the shell with those words emptied; their starters). Nothing
    when the quote scan could part from bash's: a heredoc, $'…', a comment, an unclosed quote, a shell function or
    alias that could stand for python, ${…} (a ; in it is a word's text), python's own settings (what its imports load)."""
    if "<<" in shell or "$'" in shell or "${" in shell or "PYTHON" in shell or any(
            os.environ.get(k) for k in _PY_PATH_VARS) or re.search(
            r"\balias\b|\bfunction\b|python[0-9.]*\s*\(\s*\)", shell):
        return [], shell, []
    top, q, esc = [], None, False  # top[i]: shell[i] is outside every quote and escape (_quote_at, in one pass)
    for ch in shell:
        top.append(q is None and not esc)
        if esc:
            esc = False
        elif ch == "\\" and q != "'":
            esc = True
        elif q:
            q = None if ch == q else q
        elif ch in "'\"":
            q = ch
    if q or esc or any(ch == "#" and top[i] and (i == 0 or shell[i - 1] in " \t\n;&|(") for i, ch in enumerate(shell)):
        return [], shell, []
    units, starters, out, last = [], [], [], 0
    for m in _PY_C.finditer(shell):
        if not (top[m.start()] and (m.start() == 0 or top[m.start() - 1])):  # x\;python3 is one word, not a command
            continue
        word = m.group(2)[1:-1]
        units.append(word if m.group(2)[0] == "'" else
                     re.sub(r'\\(\n|[$`"\\])', lambda e: "" if e.group(1) == "\n" else e.group(1), word))
        starters.append(m.group(1))
        out.append(shell[last:m.start(2)] + "''")
        last = m.end()
    return units, "".join(out) + shell[last:], starters


def _drives_fm(cmd, cwd=None):
    """T-0170: interpreter code that imports Foreman's modules and calls their writers. Quoted heredocs fed straight to
    python, and (T-1194) literal `python -c` code, are parsed: text that merely mentions `import fm…` (an edit script's
    strings) isn't an import. The text match of before decides for everything else: fm import text outside those
    (data heredocs, the shell, -c code it can't read), code that doesn't parse, and dynamic code (exec, eval, getattr,
    importlib…). It only relaxes what it can prove."""
    if not (_FM_INTERNALS.search(cmd) and _FM_MUTATORS.search(cmd)):
        return False
    units, rest, starters = _python_units(cmd)
    c_units, shell, c_starters = _python_c_units("\n".join(rest))
    if _FM_INTERNALS.search("\n".join([shell] + starters)):
        return True
    # T-1204: python's own settings (PYTHONPATH loads sitecustomize, PYTHONSTARTUP…), set in the command or inherited,
    # change what any of its code runs, as _python_c_units already refuses for -c
    if (units or c_units) and ("PYTHON" in "\n".join([shell] + starters) or any(os.environ.get(k) for k in _PY_PATH_VARS)):
        return True
    # python - and -c import from the folder they run in: a cd anywhere but in their own `cd DIR &&` chain (an earlier
    # line, a `;`) makes that folder unknown (T-1204: heredocs too)
    moved = len(_CD.findall("\n".join([shell] + starters))) > sum(len(_CD.findall(s)) for s in starters + c_starters)
    runs = [None if moved else _run_dir(s, cwd) for s in starters + c_starters]
    import ast
    for code, run in zip(units + c_units, runs):
        if not _FM_INTERNALS.search(code):
            continue
        try:
            tree = ast.parse(code)
        except (SyntaxError, ValueError):
            return True
        names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)} | \
                {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
        modules = [a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names] + \
                  [n.module or "" for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)]
        if names & _DYNAMIC or any(x.startswith("__") for x in names) or \
                any(m.split(".")[0] not in _PLAIN_IMPORTS and not m.startswith("fm") for m in modules):
            return True  # its strings could still run: a process, a module it wrote, pickle, dunder walking…
        # review (T-0286): python - (and -c) imports from its folder first — a json.py there runs
        if modules and (run is None or any(os.path.exists(os.path.join(run, m.split(".")[0] + x))
                                           for m in modules for x in (".py", ""))):
            return True
        fm_from = [n for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and (n.module or "").startswith("fm")]
        fm_import = [a for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names if a.name.startswith("fm")]
        if fm_from or (fm_import and _FM_MUTATORS.search(code)):
            return True
    return False


def _interp_code(cmd):
    """What the interpreter claude-check reads: the whole command but the `--run "<cmd>"` arguments of real fm calls,
    which check_bash reads on their own (interpreter checks included). A span is left out only when it starts at shell
    top level, outside heredoc bodies, in a simple command whose word is fm; heredoc bodies are read whole. T-0144: the
    T-0135 version stripped every match, so a fake `--run "` inside heredoc or -c code swallowed the call after it, and
    --run handed to the interpreter itself hid its argument. Anything uncertain is kept, so mistakes fail closed."""
    shell, bodies = _heredocs(cmd)
    if "$'" in shell or len(re.findall(r"(?<!<)<<(?!<)", shell)) != len(re.findall(_HEREDOC_START, shell)):
        return cmd  # $'…' quoting, or a heredoc form _heredocs doesn't know (<<\EOF): the scan can't follow, read all
    out, last = [], 0
    for m in _FM_RUN_ARG.finditer(shell):
        before = shell[:m.start()]
        if not _top_level(before):
            continue
        argv, _ = _strip_wrappers(_tokens(re.split(r"[;&|()\n`]", before)[-1]))
        name = os.path.basename(argv[0]) if argv else ""
        if name == "fm" or (re.match(r"^python[0-9.]*$", name) and argv[1:2] and argv[1].endswith("/fm")):
            out.append(shell[last:m.start()] + " ")
            last = m.end()
    return "".join(out) + shell[last:] + "\n" + bodies


# T-0345: python calls that start a program, by module: where its command is (an argument index, or "k:" for the
# positional arguments from k on as the argv)
_SPAWN = {"subprocess": dict.fromkeys(("run", "call", "check_call", "check_output", "Popen", "getoutput",
                                       "getstatusoutput"), 0),
          "os": {"system": 0, "popen": 0, **dict.fromkeys(("execv", "execve", "execvp", "execvpe", "posix_spawn",
                                                           "posix_spawnp"), 1),
                 **dict.fromkeys(("execl", "execle", "execlp", "execlpe"), "1:"),
                 **dict.fromkeys(("spawnv", "spawnve", "spawnvp", "spawnvpe"), 2),
                 **dict.fromkeys(("spawnl", "spawnle", "spawnlp", "spawnlpe"), "2:")},
          "pty": {"spawn": 0}}


def _python_sources(cmd):
    """T-0345: the python code a command may run: every heredoc body (one that parses as python is read as python) and
    the code of each `python -c` (option clusters such as -uc included)."""
    out, lines, seen, i = [], cmd.split("\n"), [], 0
    while i < len(lines):
        line = lines[i]
        i += 1
        starts = _heredoc_starts(seen, line)
        seen.append(line)
        for _, delim in starts:
            body = []
            while i < len(lines) and not _ends_body(lines[i], delim, line):
                body.append(lines[i])
                i += 1
            i += 1
            out.append("\n".join(body))
    for c in _split(_tokens(_lines(_strip_heredocs(cmd)))):
        argv, _ = _strip_wrappers(c.argv)
        if argv and re.match(r"^python[0-9.]*$", os.path.basename(argv[0])):
            out += _shell_c(argv[1:])
    return out


def _spawned_commands(code):
    """T-0345: the shell commands python code starts (subprocess, os.system/popen/exec*/spawn*, pty.spawn, under any
    import alias), as text check_bash reads: a literal string as it stands, a literal list with its words quoted, any
    other part as an unknown "$_" (so a delete of a variable is a delete of an unknown target), cwd= as a cd first."""
    import ast
    try:
        tree = ast.parse(code)
    except (SyntaxError, ValueError, MemoryError, RecursionError):
        return []
    alias = {}  # local name → (module, None) for the module, (module, function) for a from-import
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            alias.update({a.asname or a.name: (a.name, None) for a in n.names if a.name in _SPAWN})
        elif isinstance(n, ast.ImportFrom) and n.module in _SPAWN:
            alias.update({a.asname or a.name: (n.module, a.name) for a in n.names if a.name in _SPAWN[n.module]})
    word = lambda e: shlex.quote(e.value) if isinstance(e, ast.Constant) and isinstance(e.value, str) else '"$_"'  # noqa: E731
    out = []
    for n in ast.walk(tree):
        f = getattr(n, "func", None) if isinstance(n, ast.Call) else None
        if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name) and alias.get(f.value.id, (0, 0))[1] is None:
            mod, fn = alias[f.value.id][0], f.attr
        elif isinstance(f, ast.Name) and alias.get(f.id, (0, None))[1]:
            mod, fn = alias[f.id]
        else:
            continue
        where = _SPAWN[mod].get(fn)
        if where is None:
            continue
        if isinstance(where, str):
            text = " ".join(word(e) for e in n.args[int(where[:-1]):])
        else:
            arg = n.args[where] if len(n.args) > where else next(
                (k.value for k in n.keywords if k.arg in ("args", "argv", "cmd", "command")), None)
            if arg is None:
                continue
            text = arg.value if isinstance(arg, ast.Constant) and isinstance(arg.value, str) else \
                " ".join(word(e) for e in arg.elts) if isinstance(arg, (ast.List, ast.Tuple)) else '"$_"'
        cwd = next((k.value for k in n.keywords if k.arg == "cwd"), None)
        out.append((f"cd {word(cwd)} && " if cwd is not None else "") + text)
    return out


def _interpreter_writes(cmd, ctx):
    """Interpreter code (heredoc, -c, -e) that writes files: every quoted path it names counts as a write target.

    Coarse on purpose: a script that names a protected path and writes anything is treated as writing it. Code that
    imports Foreman's modules and calls their writers bypasses fm (the only state writer): that needs core, i.e. the
    user's yes, rather than never-authorizable state-direct, because the text match can't tell code from test data."""
    if not _INTERP.search(_mask_fm(_drop_data_heredocs(cmd), ctx)):
        return []
    if _drives_fm(_drop_data_heredocs(cmd, only=lambda line: _writes_unrun_source(line, cmd, ctx)), ctx.cwd):
        # T-0740: 9 repeats in a day; T-0934: `cd DIR; python3 - <<EOF` is refused only because of the `;`. T-1171: 12
        # of 31 refusals in four days wrote a test with cat <<EOF and ran the tests in the same command
        return [("core", "interpreter code driving Foreman's modules (use the fm CLI; to edit a Foreman source file "
                         "whose text names its modules, use the Edit or Write tool"
                         + ("; chain the cd with && instead of ;, or pass the path" if re.search(r"\bcd\s+[^\n;&|]+;", cmd)
                            else "")
                         + ("; write the file in one command and run it in the next: the write alone is data"
                            if re.search(r"\b(?:cat\s*>>?|tee\b)[^\n]*<<", cmd) else "") + ")")]
    code = _interp_code(cmd)
    # T-0150/T-0155: a backtick runs code unless every interpreter here treats it as text (markdown in a Python heredoc)
    ticks = "`" in code and any(not _TEXT_TICKS.match(m.group(1)) for m in _INTERP.finditer(cmd))
    if _CLAUDE_IN_CODE.search(code) and (_EXEC_API.search(code) or ticks):
        return [("plugin", "interpreter code running claude's plugin, MCP or config commands" + plugin_mark("?"))]
    proved = _proved_writes(cmd, ctx)  # T-0176: a script that provably writes only its open() files
    if proved is None and not _WRITE_API.search(cmd):
        return []
    found = []
    for path in proved if proved is not None else [_resolve(_expand(m.group(2), ctx), ctx.cwd)
                                                   for m in _QUOTED.finditer(cmd)]:
        found += [(cat, f"{path} (written from interpreter code)") for cat in classify_write(path, ctx)
                  if cat in _GUARDED_BY_PATH]
    return found


def fm_calls(cmd):
    """The argument lists of every direct `fm …` (or `python3 …/fm …`) call in a shell command."""
    calls = []
    for c in _split(_tokens(_lines(_strip_heredocs(cmd)))):
        argv, _ = _strip_wrappers(c.argv)
        name, args = (os.path.basename(argv[0]) if argv else ""), argv[1:]
        if name == "fm":
            calls.append(args)
        elif re.match(r"^python[0-9.]*$", name) and args[:1] and args[0].endswith("/fm"):
            calls.append(args[1:])
    return calls


# T-0974: programs that only read, each with the flags that would make it write, run something or never end. A command
# passes read_only() only when every part is one of these without those flags.
_READS = {
    "ls": (), "cat": (), "head": (), "tail": ("-f", "-F", "--follow"), "wc": (), "pwd": (), "which": (), "file": ("-C", "--compile"),
    "stat": (), "du": (), "df": (), "tree": ("-o", "-R"), "grep": (), "egrep": (), "fgrep": (),
    "rg": ("--pre", "--pre-glob", "--hostname-bin", "-z", "--search-zip"),
    "sort": ("-o", "--output", "--compress-program"), "uniq": (), "cut": (), "nl": (), "diff": (), "cmp": (), "realpath": (),
    "file": ("-C", "--compile"), "basename": (), "dirname": (), "echo": (), "printf": (), "true": (), "date": ("-s", "--set"), "tr": (),
    "column": (), "find": ("-exec", "-execdir", "-ok", "-okdir", "-delete", "-fprint", "-fprint0",
                                     "-fprintf", "-fls"),
}
_GIT_READS = {"status", "log", "diff", "show", "blame", "rev-parse", "ls-files", "describe", "shortlog", "grep"}
_GIT_BAD = ("-o", "--output", "--ext-diff", "--textconv", "--open-files-in-pager", "-O")


def _bad_flag(args, bad):
    """True when an argument is one of the bad flags: a long option counts when it abbreviates one (GNU and git accept
    --comp=), a single-dash cluster when it holds a bad short letter anywhere (-uo, -oFILE, -nOcat); a bad flag with a
    longer single-dash name (find -exec) matches exactly."""
    for a in args:  # past a '--' too: it ends getopt's options, not find's expression (find -- . -delete)
        if a == "--":
            continue
        if a.startswith("--"):
            if any(b.startswith("--") and b.startswith(a.partition("=")[0]) for b in bad):
                return True
        elif a.startswith("-") and any(a == b or len(b) == 2 and b[1] in a[1:] for b in bad if b[:1] == "-" and b[1:2] != "-"):
            return True
    return False


def read_only(cmd):
    """T-0974: True when the whole command only reads: every part a _READS program (or a reading git subcommand)
    without its writing flags, nothing redirected but to /dev/null, nothing substituted, expanded, backgrounded or
    assigned.
    Conservative on purpose: anything it doesn't know gets Claude Code's own dialog."""
    if not cmd.strip() or any(x in cmd.strip() for x in ("`", "$", "<(", ">(", "\n")):  # review: $VAR can print a secret
        return False
    parts = _split(_tokens(cmd))
    for x in parts:
        if x.procsub or x.feeds or x.depth or any(r != "/dev/null" for r in x.redirs) or x.op not in ("", ";", "&&", "||", "|"):
            return False
        argv = x.argv
        if not argv or "=" in argv[0] or "/" in argv[0]:
            return False
        if argv[0] == "git":
            sub = argv[1] if len(argv) > 1 else ""
            if sub not in _GIT_READS or _bad_flag(argv[2:], _GIT_BAD if sub == "grep" else _GIT_BAD[:4]):
                return False
            continue
        bad = _READS.get(argv[0])
        if bad is None or _bad_flag(argv[1:], bad):
            return False
        if argv[0] == "uniq" and len([a for a in argv[1:] if not a.startswith("-")]) > 1:  # uniq IN OUT writes OUT
            return False
    return bool(parts)


def lone_fm_ask(cmd):
    """The arguments of `fm ask …` when it is the whole command (nothing chained, piped, redirected or substituted):
    a permission prompt then approves exactly that request."""
    if "`" in cmd or "$(" in cmd or "\n" in cmd.strip():
        return None
    cmds = _split(_tokens(_strip_heredocs(cmd)))
    if len(cmds) != 1 or cmds[0].redirs or cmds[0].procsub:
        return None
    calls = fm_calls(cmd)
    return calls[0] if len(calls) == 1 and calls[0][:1] == ["ask"] else None


# T-0151: variables are resolved only in a straight-line command (simple commands joined by ; or newlines): a pipe, &&,
# ||, &, a subshell, a group or a control keyword can make an assignment conditional or local, so then none are
_BRANCHY = re.compile(r"[|&(){}]|\b(?:if|then|else|elif|fi|for|while|until|do|done|case|esac|select|function|coproc)\b")
# T-0161: only a builtin can change a variable of this shell (an alias or a function needs one first), so resolving stops
# at any builtin outside the inert ones (cd and pushd set only names that are never resolved; [[ -eq assigns)
_BUILTINS = set(". : [ [[ alias bg bind break builtin caller cd command compgen complete compopt continue declare dirs "
                "disown echo enable eval exec exit export false fc fg getopts hash help history jobs kill let local logout "
                "mapfile popd printf pushd pwd read readarray readonly return set shift shopt source suspend test times "
                "trap true type typeset ulimit umask unalias unset wait".split())
_INERT = set(": [ cd dirs echo exit false hash help jobs kill popd pushd pwd shift test times true type ulimit umask".split())
_ASSIGN = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)=(.*)$", re.S)


def _setter(name, args):
    """A builtin that can set this shell's names. T-0370: printf only as printf -v NAME (the option comes first, before
    any --), so a plain printf no longer makes every name unknown."""
    if name == "printf":  # its security review: a first word bash computes ($X, `…`, {a,b}, a glob) may become -v
        first = args[0] if args else ""
        word, m = _unquote(first), re.search(r"[*?\[{]", first)  # a glob or brace makes -v… only from a -v prefix
        return bool(args) and (word is None or "$" in first or "`" in first or word.startswith("-v")
                               or bool(m) and "-v".startswith(first[:m.start()]))
    return name in _BUILTINS and name not in _INERT
_ASSIGNISH = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)(?:\[[^\]]*\])?\+?=")  # NAME=, NAME+= and NAME[i]=
# bash sets these itself, ignores an assignment to them or makes it fail (readonly)
_SHELL_SET = re.compile(r"^(?:_|PWD|OLDPWD|DIRSTACK|BASH\w*|RANDOM|SRANDOM|SECONDS|LINENO|EPOCH\w+|HISTCMD|PPID|E?UID|"
                        r"GROUPS|FUNCNAME|PIPESTATUS|OPT\w+|REPLY|MAPFILE|COPROC\w*|SHELLOPTS|SHLVL|HOST\w+|MACHTYPE|"
                        r"OSTYPE|COMP_\w+|READLINE_\w+|COLUMNS|LINES)$")


def _straight_line(shell):
    s = re.sub(r"\$\{\w+\}|\d*>&\d*-?|&>>?", " ", shell)  # ${VAR}, 2>&1 and &> aren't branches
    if "&&" in s:  # T-0175: in a chain joined only by &&, a command runs only after every earlier one ran; mixed with
        s = s.replace("&&", " ")  # ; or a newline, one can be skipped and the next still run (false && D=x; rm $D)
        if re.search(r"[;\n]", s.strip()):
            return False
    return not _BRANCHY.search(s)


def _with_vars(tok, env):
    return re.sub(r"\$(?:\{(\w+)\}|(\w+))", lambda m: env.get(m.group(1) or m.group(2), m.group(0)), tok)


_WORD = re.compile(r"[^\s'\"`;|&<>()=]+")
_PART = re.compile(r"\$(?:\{(\w+)\}|(\w+))|\$\{[^}]*\}?|\$\([^)]*\)?|`[^`]*`?|\$")  # what a shell fills in at run time


def _top(shell):
    """(straight, and_chain, mixed) at the command's top level, command substitutions blanked: straight when every command
    there runs in this shell, in order (no branch, subshell, pipe, background or !: `! cd BAD && x` runs x); and_chain
    when only && joins them, so a failed cd stops the rest."""
    s, prev = re.sub(r"`[^`]*`", "S", shell), None
    while s != prev:
        s, prev = re.sub(r"\$\([^()]*\)", "S", s), s
    s = _mask_quotes(s)  # T-0384: a quoted ( | or ; is text
    straight = "!" not in s and _straight_line(s)
    # T-0339: a ; list with && in it: each &&-segment is a chain of its own, the segments run in order; T-0355: its
    # elements may be pipelines (a pipe runs in subshells, so only a cd outside one moves the shell)
    mixed = not straight and "!" not in s and _straight_line(re.sub(r"&&|(?<!\|)\|&?(?!\|)", ";", s))
    return straight, straight and "&&" in s, mixed


_DATA_TOOLS = {"curl", "wget", "head", "tail", "echo", "printf", "jq", "cat", "wc", "grep", "cut", "tr", "sleep", "true",
               "nvidia-smi"}  # T-0397: a GPU query (its -f/--filename, which logs to a file, voids it)
# flags that write no file; T-0397: -k -i -I -v (stdout or stderr only) and a timeout fused to them (-sSm5)
_CURL_SAFE = re.compile(r"-[sSLfkiIv]*m\d+(?:\.\d+)?|-[sSLfkiIv]+|--(?:silent|show-error|location|fail|compressed|insecure|"
                        r"include|head|verbose|(?:max-time|connect-timeout)=\d+(?:\.\d+)?)")
_CURL_TIMES = re.compile(r"-[sSLfkiIv]*m|--max-time|--connect-timeout")  # T-0397: take a number next
_WGET_SAFE = {"-q", "--quiet", "-nv"}
_RUNS = re.compile(r"\$\(|`|\$\{[^}]*=")  # T-0414: a word that runs a command or sets a name as it expands
_REACHES_PYTHON = re.compile(r"PYTHON\w*|LD_\w*|PATH|HOME|ENV|BASH_ENV|IFS")  # read by python, its loader or the shell


_BRACES = re.compile(r"\{[^{}]*(?:,|\.\.)[^{}]*\}")  # a brace expansion bash would turn into several words


def _writes_nothing(x):
    """T-0344 review: a command beside the python that can't create a file python would then import: no output
    redirect, and curl or wget only with flags that keep their download on stdout (any other flag, -o/-O, a config
    or a cookie jar, voids it); every other data tool writes nowhere but stdout. T-0414: no word with a substitution
    left in it (a quoted "$( )" or `…` runs a command _split doesn't see; an unquoted $( ) is a command of its own,
    checked here too) and no printf -v; a command of NAME=value words only sets names, each absent from the
    environment (so not exported to python) and none that python, its loader or the shell reads (_REACHES_PYTHON)."""
    if x.redirs or any(_RUNS.search(w) or _BRACES.search(w) for w in x.argv):  # T-0422: {-o,json.py} is -o json.py
        return False
    sets = [_ASSIGN.match(w) for w in x.argv]
    if x.argv and all(sets):
        return not any(m.group(1) in os.environ or _REACHES_PYTHON.fullmatch(m.group(1)) for m in sets)
    a, _ = _strip_wrappers(x.argv)
    if x.argv != a or not a or os.path.basename(a[0]) not in _DATA_TOOLS:
        return False
    name, args = os.path.basename(a[0]), a[1:]
    if name == "printf" and _setter(name, args):
        return False
    if name == "curl":  # value flags: a header or agent, a -w format (not %output{file}), -o only to /dev/null
        i = 0
        while i < len(args):
            w, v = args[i], args[i + 1] if i + 1 < len(args) else ""
            if w in ("-H", "--header", "-A", "--user-agent", "-X", "--request") or \
                    w in ("-w", "--write-out") and "%output{" not in v or w in ("-o", "--output") and v == "/dev/null" \
                    or _CURL_TIMES.fullmatch(w) and re.fullmatch(r"\d+(?:\.\d+)?", v):
                i += 2
            elif w.startswith("-") and not _CURL_SAFE.fullmatch(w):
                return False
            else:
                i += 1
        return True
    if name == "nvidia-smi":  # T-0397: -f/--filename logs to a file; every other option prints
        return not any(w == "-f" or (w.startswith("-f") and not w.startswith("--")) or w.startswith("--filename")
                       for w in args)
    if name == "wget":  # every -O must name stdout (the last one wins: -qO- URL -O json.py writes json.py)
        outs, i = [], 0
        while i < len(args):
            w = args[i]
            if w in ("-O", "-qO", "--output-document"):
                outs.append(args[i + 1] if i + 1 < len(args) else "")
                i += 2
                continue
            if w in ("-O-", "-qO-") or w.startswith("--output-document="):
                outs.append("-" if w in ("-O-", "-qO-") else w.partition("=")[2])
            elif w.startswith("-") and w != "-" and w not in _WGET_SAFE:
                return False
            i += 1
        return bool(outs) and all(o == "-" for o in outs)
    return True


def _shadowed(cwds, mods):
    """T-0344 review: a module python -c would import from the folder it runs in instead of the standard library — a
    name the code imports, or any stdlib name (json imports re, which imports enum) — as X.py, X.pyc, an extension
    module or a package (X/__init__.py); a plain folder shadows nothing."""
    names = set(sys.stdlib_module_names) | set(mods)
    for b in cwds:
        try:
            entries = os.listdir(b)
        except OSError:
            return True  # a folder the guard can't read could hold anything
        for n in entries:
            stem, _, ext = n.partition(".")
            if stem in names and (ext.split(".")[-1] in ("py", "pyc", "so", "pyd") and ext or
                                  os.path.isfile(os.path.join(b, n, "__init__.py"))):
                return True
    return False


def _reads_pipe_as_data(c, argv, cmds, cwds, cmd):
    """T-0344: `curl … | python3 -c CODE` reads the download as data when CODE is proved (_open_targets: pure modules,
    nothing dynamic, nothing written) and nothing makes python read stdin as code. -c comes first (every word after
    CODE is sys.argv, so no -i before it); python runs bare and every other command is a plain data tool that writes no
    file or a plain assignment of a name python can't see (_writes_nothing), so no env, export or eval can set
    PYTHONINSPECT (its review: PYTH""ONINSPECT=1) and no module can appear before python starts; none is inherited; and
    nothing in the folder it runs in shadows a module it may import (_shadowed: python -c searches that folder first).
    T-0414: "every other" is every command up to the end of python's pipeline when python sits outside every ( ) (a
    group's redirect or pipe is written after python but opens before it or runs beside it); what runs after python
    exits can't change it. A bare & refuses outright (it runs a command beside python, and `&</dev/null x` hides x
    from _split), as does a substitution in a live heredoc body. A name set here may be read only where its every value
    is a plain word: no space, glob, quote, $ or leading -, so it can't split into flags or close a string in CODE."""
    name, args = (os.path.basename(argv[0]) if argv else ""), argv[1:]
    if not (re.match(r"^python[0-9.]*$", name) and c.argv == argv and set(c.redirs) <= {"/dev/null"} and len(args) >= 2
            and args[0] == "-c"):
        return False
    shell = _mask_quotes(_strip_heredocs(cmd))
    if re.search(r"(?<![&<>|])&(?![&>])", shell) or any(_RUNS.search(b) for b in _live_heredocs(cmd)):
        return False
    i = end = cmds.index(c)
    while end + 1 < len(cmds) and "|" in cmds[end + 1].op.replace("||", ""):
        end += 1
    # review: _split counts a quoted ")" as a real one (shlex makes it a bare token), so python can look outside a
    # group it is in; bare paren tokens that outnumber the unquoted parens mean the depths can't be trusted
    bare = [t for t in _tokens(_lines(_strip_heredocs(cmd))) if re.fullmatch(r"[$<>]?\(+|\)+", t)]
    top = (c.depth == 0 and all(x.depth >= 0 for x in cmds) and shell.count("(") == shell.count(")")
           and sum(t.count("(") for t in bare) == shell.count("(") and sum(t.count(")") for t in bare) == shell.count(")"))
    others = [x for x in (cmds[:end + 1] if top else cmds) if x is not c]
    if not all(_writes_nothing(x) for x in others):
        return False
    pairs = [w.split("=", 1) for x in others if all(_ASSIGN.match(w) for w in x.argv) for w in x.argv]
    loose = {k for k, v in pairs if v.startswith("-") or not re.fullmatch(r"[\w.:/@%+,=-]*", v)}
    words = [w for x in others + [c] if not all(_ASSIGN.match(v) for v in x.argv) for w in x.argv]
    read = {r for w in words for r in re.findall(r"\$\{?[#!]?([A-Za-z_]\w*)", w)}
    if loose & read or loose and any("${!" in w for w in words):  # ${!R} reads the name R holds
        return False
    if any(os.environ.get(k) for k in ("PYTHONINSPECT", *_PY_PATH_VARS)) or _open_targets(args[1]) != []:
        return False
    import ast
    mods = {al.name.split(".")[0] for n in ast.walk(ast.parse(args[1])) if isinstance(n, ast.Import) for al in n.names}
    return not _shadowed(cwds, mods)


def _a_path(word, fixed):
    """T-0331: a command word that runs a file, never a builtin or function: a literal / in it, and its only
    expansions $NAME or ${NAME} of plain literals this command set before it (fixed: no space or glob, so they can't
    split into `eval …`; its review). `$S/app` with S=/tmp/x is a path; `$S/etc` with S unknown may be `eval X=/etc`."""
    rest = re.sub(r"\$(?:\{\w+\}|\w+)", "", word)
    return "/" in rest and not re.search(r"[$`*?\[\\'\"\s]", rest) and all(
        (a or b) in fixed for a, b in re.findall(r"\$(?:\{(\w+)\}|(\w+))", word))


def _outside(shell, cmds, ctx, fixed=None):
    """T-0175 review: ({NAME: value} for the names this command can't set itself, as it inherits them; the names it may
    set). It may set every name it writes bare (an assignment, read NAME, for NAME, ${NAME:=…}), and any name at all
    (None) with a builtin that sets names indirectly (eval, read, declare, source…) or a computed command name. Values
    are Claude Code's environment, HOME the user's; one a shell would split or expand stays unknown."""
    for c in cmds:
        argv, _ = _strip_wrappers(c.argv)
        if argv and (_setter(os.path.basename(argv[0]), argv[1:]) or re.search(r"[$`*?\[]", argv[0]) and not _a_path(
                argv[0], fixed or {})):
            return {}, None
    bare = set(re.findall(r"[A-Za-z_]\w*", re.sub(r"\$\w+|\$\{\w+\}", " ", shell)))
    return {k: v for k, v in {**os.environ, "HOME": ctx.home}.items() if k not in bare and not _SHELL_SET.match(k)
            and v and not re.search(r"[\s*?\[]", v) and not v.startswith("~")}, bare


def _moved(cwds, lost, tgt, sure, cdpath, ctx):
    """T-0175 review: the places the shell may be after a cd: cwds, the ones the guard can name, and lost, the paths
    below a folder it can't name (a cd to a target it can't resolve, or a relative one CDPATH may send elsewhere). When
    the cd surely happened (sure: an && chain stops at a failed one; a straight command's cd into an existing folder
    can't fail) the new places replace the old; otherwise it may fail or run in a subshell, so they add to them."""
    if _unresolvable(tgt):
        new, tails = [], [""]
    else:
        t = _expand(tgt, ctx)
        if os.path.isabs(t):
            new, tails = [os.path.normpath(t)], []
        else:
            new = [_resolve(t, b) for b in cwds]
            tails = [os.path.join(x, t) for x in lost] + ([t] if cdpath else [])
    return list(dict.fromkeys(new if sure else cwds + new)), list(dict.fromkeys(tails if sure else lost + tails))


_BRACE = re.compile(r"\{([^{}]*)\}")
_SEQ = re.compile(r"(-?\d+|[A-Za-z])\.\.(-?\d+|[A-Za-z])(?:\.\.-?\d+)?")
EXPANSIONS_MAX = 1024  # ponytail: a brace product past this is checked only this far


def _expansions(path):
    """T-0177: the paths bash may make of a target: comma and sequence braces (innermost first; {x} with neither stays
    as written) and, for any with * ? or [, the existing paths it matches."""
    out, todo = [], [path]
    while todo and len(out) + len(todo) <= EXPANSIONS_MAX:
        p = todo.pop()
        m = next((m for m in _BRACE.finditer(p) if "," in m.group(1) or _SEQ.fullmatch(m.group(1))), None)
        if not m:
            out.append(p)
            continue
        seq, inner = _SEQ.fullmatch(m.group(1)), m.group(1)
        if seq:
            a, b = seq.group(1), seq.group(2)
            num = a.lstrip("-").isdigit() and b.lstrip("-").isdigit()
            lo, hi = (int(a), int(b)) if num else (ord(a), ord(b))
            step = 1 if hi >= lo else -1
            alts = [str(i) if num else chr(i) for i in range(lo, hi + step, step)][:EXPANSIONS_MAX]
        else:
            alts = inner.split(",")
        todo += [p[:m.start()] + x + p[m.end():] for x in alts]
    out += todo
    import glob
    import itertools
    return list(dict.fromkeys(out + [g for p in out if re.search(r"[*?\[]", p)
                                     for g in itertools.islice(glob.iglob(p), EXPANSIONS_MAX)]))


def _makeable(d):
    """mkdir -p d can succeed: its nearest existing folder is a folder this user may write and enter."""
    while not os.path.exists(d):
        d = os.path.dirname(d)
    return os.path.isdir(d) and os.access(d, os.W_OK | os.X_OK)


def _possible(path):
    """False when a folder in the path is an existing file: nothing can be written there."""
    d = os.path.dirname(path)
    while d not in ("", "/"):
        if os.path.exists(d):
            return os.path.isdir(d)
        d = os.path.dirname(d)
    return True


GUESS_WORDS = 48  # ponytail: words tried per unknown part (two parts: their pairs); a longer command is guessed this far


_PLAIN = r"[^()`'\"\\#\n]*"  # no quote, escape, comment, newline or paren: bash's closing ) is the first one


def _mask_substs(shell):
    """T-0370: each plain $(…) and `…` (innermost first, so nesting unwinds) as $___…, an unknown value of the same
    length; a tail's leading plain `…)` (the rest of a substitution it opens in) too. Only plain bodies: a quote, \\),
    a # comment, a heredoc or a case pattern can move the real closing paren past the first, and an S= inside it would
    then look like this shell's (its review: X=$(echo \\); S=/tmp/ok; true); rm -rf $S/ is rm -rf /)."""
    def mask(m):
        body = m.group(0)
        return body if re.search(r"\bcase\b|<<", body) else "$" + "_" * (len(body) - 1)
    shell = re.sub(r"^" + _PLAIN + r"\)", lambda m: m.group(0) if mask(m) == m.group(0) else " " * len(m.group(0)),
                   shell)  # a tail's head ran in the subshell: no command of this shell
    while True:
        t = re.sub(r"\$\(" + _PLAIN + r"\)|`[^()`'\"\\#\n]*`", mask, shell)
        if t == shell:
            return shell
        shell = t


def _mask_quotes(text):
    """T-0384: the text inside '…' and "…" as underscores, same length, the quotes kept: a quoted ( | ; & or keyword
    is a literal, never a branch (a jq filter or sed script made the whole line read as branchy). A # comment is
    blanked to its line's end too (its review: a quote in a comment paired with one in a later comment hid a ||).
    Escapes and comments as _strip_comments reads them; unchanged (fails closed) under $'…', an unclosed quote or a
    substitution inside double quotes, whose own quotes don't pair with the outer ones."""
    if "$'" in text:
        return text
    out, q, i = [], None, 0
    while i < len(text):
        ch = text[i]
        if ch == "\\" and q != "'":
            out.append(text[i:i + 2] if q is None else "_" * len(text[i:i + 2]))
            i += 2
            continue
        if q == '"' and (ch == "`" or text.startswith("$(", i) or (text.startswith("${", i)
                                                                    and not re.match(r"\$\{\w+\}", text[i:]))):
            return text
        if q is None and ch == "#" and (i == 0 or text[i - 1] in " \t\n;&|(<>"):
            j = text.find("\n", i)
            j = len(text) if j < 0 else j
            out.append("_" * (j - i))
            i = j
            continue
        if q and ch != q:
            out.append("_")
        else:
            q = None if q else (ch if ch in "'\"" else None)
            out.append(ch)
        i += 1
    return text if q else "".join(out)


# `done` ends the loop only where a command starts (`echo done` is an argument)
_LOOP = re.compile(r"(?<![\w$-])for\s+([A-Za-z_]\w*)\s+in\s+([^;\n]*?)\s*[;\n]\s*do\b(.*?[;\n&])\s*done(?![^\s;&|()<>])",
                   re.S)
_LITERAL_WORD = re.compile(r"[\w./@:+,=%-]+")
_LOOP_SETTERS = re.compile(r"(?<![\w-])(?:read|readarray|mapfile|declare|typeset|local|export|printf|eval|unset|let|"
                           r"source|for|while|until|select|case|function|do|done|break|continue)(?![\w-])|"
                           r"(?:^|[\s;&|(])\.\s|<<|\$\{!")  # break/continue: V may keep an earlier word


def _single_quoted(text, i):
    """Whether position i of text is inside '…' as bash reads it (escapes as _mask_quotes reads them)."""
    q, j = None, 0
    while j < i:
        ch = text[j]
        if ch == "\\" and q != "'":
            j += 2
            continue
        if q:
            q = None if ch == q else q
        elif ch in "'\"":
            q = ch
        j += 1
    return q == "'"


def _expand_literal_loops(cmd):
    """T-0411: a top-level `for V in w1 w2; do BODY; done` whose words are plain literals runs BODY once per word, so
    it is read as `BODY[w1]; BODY[w2]; V=w2`. Only when the body has no nested loop, case, heredoc or way to set V
    (an assignment, read, eval, source …), and no $V bash leaves unexpanded ('…'); break and continue only make bash
    do less than what is checked. Anything else is left as written (V stays unknown, as before)."""
    # IFS: bash splits the word it substitutes; a backslash: an escaped ; or & separates nothing
    if "for" not in cmd or "$'" in cmd or "<<" in cmd or "IFS" in cmd or "\\" in cmd:
        return cmd
    masked = _mask_quotes(cmd)
    if masked == cmd and re.search(r"['\"]", cmd):  # quoting the guard can't read: leave it
        return cmd
    out, last = [], 0
    for m in _LOOP.finditer(masked):
        var, words = m.group(1), cmd[m.start(2):m.end(2)].split()
        body, mbody = cmd[m.start(3):m.end(3)], m.group(3)
        before = masked[:m.start()].rstrip()
        uses = list(re.finditer(rf"\$(?:\{{{var}\}}|{var}(?!\w))", body))
        if (before and before[-1] not in ";&|\n(" or not words or not all(_LITERAL_WORD.fullmatch(w) for w in words)
                or _LOOP_SETTERS.search(mbody) or re.search(rf"(?<![\w$-]){var}(?!\w)", re.sub(
                    rf"\$(?:\{{{var}\}}|{var}(?!\w))", "", body)) or any(_single_quoted(body, u.start()) for u in uses)):
            continue
        after = masked[m.end():].lstrip(" \t")
        runs = "; ".join(re.sub(rf"\$(?:\{{{var}\}}|{var}(?!\w))", lambda _, w=w: w, body).strip().rstrip(";").strip()
                         for w in words)
        # V keeps the last word only when the loop surely ran in this shell: not behind && / || (maybe skipped) or in
        # a pipeline (a subshell)
        ran = not before or before[-1] in ";\n(" or before[-1] == "&" and before[-2:] not in ("&&", "|&")
        keeps = ran and (not after or after[0] in ";\n" or after[:2] in ("&&", "||"))
        out.append(cmd[last:m.start()] + runs + (f"; {var}={words[-1]}" if keeps else ""))
        last = m.end()
    return "".join(out) + cmd[last:] if out else cmd


_MOVERS = re.compile(r"(?<![\w./-])(?:cd|pushd|popd|eval|source|trap|mapfile|readarray)(?![\w./-])|(?:^|[\s;&|(])\.\s")
_CD_TO = re.compile(r"(?<![\w./-])(?:cd|pushd)\s+(?:-[LPe@]+\s+)*([^\s;&|<>()'\"`$]+)")
# a command word bash computes: a $ expansion or a quote right where a command starts
_COMPUTED = re.compile(r"(?:^|[;&|(\n]|\b(?:then|do|else|elif|time|!))\s*[\"']?\$")


def _cd_targets(code):
    """T-0384: the literal folders shell text's cd and pushd lines name, quotes and backslashes removed as bash does."""
    code = _strip_comments(code)
    return list(dict.fromkeys(_CD_TO.findall(code) + _CD_TO.findall(re.sub(r"[\\'\"]", "", code))))


def _moves_text(code):
    """T-0384: whether shell text may cd this shell: a mover word, also once quotes and backslashes are removed (c\\d
    and c""d are cd), a command word it computes, or a brace, glob or substitution that may make one."""
    code = _strip_comments(code)
    return bool(_MOVERS.search(code) or _MOVERS.search(re.sub(r"[\\'\"]", "", code)) or _COMPUTED.search(code)
                or re.search(r"[`{*?\[]|\$\(", code))


def _moves_shell(name, args, cwds, ctx, shell=""):
    """T-0384: (whether eval, source, ., trap or mapfile -C may run a cd in this shell or one more of themselves, the
    literal folders its cd and pushd lines name). Computed text, a script found on PATH, one that isn't a plain file
    (its review: /dev/stdin, a FIFO), one the command also names elsewhere (it may write it first), one given
    arguments, or one it can't read may move it; a literal or a readable script with none of those doesn't."""
    if name in ("mapfile", "readarray"):
        cbs = [args[j + 1] for j, a in enumerate(args[:-1]) if a == "-C"] + [a[2:] for a in args if a.startswith("-C")
                                                                              and len(a) > 2]
        return (bool(cbs) and any(_moves_text(cb) or not cb for cb in cbs)), [d for cb in cbs for d in _cd_targets(cb)]
    if name in ("eval", "trap"):
        rest = args[1:] if args[:1] == ["--"] else args
        if name == "trap" and rest[:1] and rest[0].startswith("-"):
            return rest[0] not in ("-p", "-l", "-P"), []  # -p and -l only print
        text = " ".join(rest) if name == "eval" else (rest[0] if rest else "")
        return bool(re.search(r"[$`\\]", text) or _moves_text(text)), _cd_targets(text)
    if len(args) != 1 or "/" not in args[0] or _unresolvable(args[0]):
        return True, []  # source NAME searches PATH first; arguments become its $1 …
    if shell.count(os.path.basename(args[0])) > 1:
        return True, []
    moves, places = False, []
    for base in cwds:
        path = _resolve(_expand(args[0], ctx), base)
        if not os.path.isfile(path) or re.match(r"/(?:dev|proc|sys)/", os.path.realpath(path)):
            return True, places
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                code = f.read(1_000_000)
        except OSError:
            return True, places
        if _moves_text(code):
            moves, places = True, places + _cd_targets(code)
    return moves, places


def _prefix_vars(shell, cmds, home=None):
    """T-0183: NAME=literal values a branchy command sets in its straight top-level prefix (the commands before its
    first branch, pipe, subshell, group or keyword run first, in this shell), for names written bare nowhere else in
    it; {} when nothing qualifies. Only where no builtin can set names indirectly (the caller checks)."""
    # T-0370: a substitution is no branch (a subshell sets nothing here): read the prefix with each one as an unknown
    # value of the same length, so `f=$(ls …); S=/tmp/x; … > $S/a` knows S; f stays unknown, and a name also set
    # inside a substitution is written twice (counts, below, reads the real text)
    full, shell = shell, _mask_substs(shell)
    s = _mask_quotes(re.sub(r"\$\{\w+\}|\d*>&\d*-?|&>>?", lambda m: " " * len(m.group(0)), shell))
    # T-0384: a pipeline is no cut either: its parts run in subshells and set nothing here (dropped below)
    cut = next((m.start() for m in re.finditer(r"&&|\|\||(?<!\|)\|&|&|[(){}`]|\$\(|\b(?:if|then|else|elif|fi|for|while|until|do|"
                                                r"done|case|esac|select|function|coproc)\b", s) if m.group(0) != "&&"), len(s))
    # what an && may skip is set for sure only if everything after it runs only when the chain got that far:
    # `false && HOME=/x; rm $HOME` runs the rm anyway (T-0338 review), `S=/x && rm $S/a && ls | head` doesn't
    amp = s.find("&&", 0, cut)
    skippable = amp >= 0 and re.search(r";|\n|\|\||(?<![&|])&(?!&)", s[amp + 2:].replace("&&", "  "))
    seps = list(re.finditer(r";|\n|&&", s[:cut]))
    if skippable:  # keep the elements that surely ran: after a ; or newline, or after && links that can't fail
        keep, start, sure = [], 0, True
        for m in seps:
            elem = shell[start:m.start()]
            if sure:
                keep.append(elem)
            sure = (sure and bool(re.fullmatch(r"\s*(?:\w+=[^\s;&|$`()<>'\"\\]*\s+)*\w+=[^\s;&|$`()<>'\"\\]*\s*",
                                                elem))) if m.group(0) == "&&" else True  # a plain assignment can't fail
            start = m.end()
        prefix = "; ".join(e.strip() for e in keep if e.strip())
    else:  # T-0330: a ; list mixed with && (D=~/x; mkdir -p $D && cd $D && tar xf -) isn't straight either
        prefix = shell[:seps[-1].start()] if seps and (cut < len(s) or not _straight_line(full) or full != shell) else ""
    # T-0384: drop the pipelines (no lastpipe without a shopt, a setter that voids all of this) and read the rest
    # with quoted text masked, as _raw_cmds reads quotes
    mp = _mask_quotes(prefix)
    if "$'" not in prefix and (mp != prefix or not re.search(r"['\"]", prefix)):  # unchanged with quotes: unread
        cuts = [0] + [x for m in re.finditer(r";|\n|&&", mp) if not (m.group(0) == "\n" and re.search(  # its review: a
            r"\|&?\s*$", mp[:m.start()])) for x in (m.start(), m.end())] + [len(prefix)]  # | ends no pipeline
        prefix = "; ".join(prefix[a:b].strip() for a, b in zip(cuts[::2], cuts[1::2])
                           if prefix[a:b].strip() and not re.search(r"(?<!\|)\|(?!\|)", mp[a:b]))
        mp = _mask_quotes(prefix)
    raw = _raw_cmds(prefix) if prefix and _straight_line(mp) else None
    env = {}
    for words in raw or []:
        env = _track_vars(words, env, home)
        if env is None:
            return {}
    # T-0331: a word after - / or . (a flag like -S, a path segment like /tmp/S/) can't name a variable
    counts = collections.Counter(re.findall(r"(?<![\w/.-])[A-Za-z_]\w*", re.sub(r"\$\w+|\$\{\w+\}", " ", full)))

    def set_first(k):  # T-0370 review: `echo > $S/x; S=/tmp/x` writes /x (S is unset there): no value before it is set
        a, r = re.search(rf"(?<![\w$]){k}=", full), re.search(rf"\$\{{?{k}\b", full)
        return a is not None and (r is None or a.start() < r.start())
    return {k: v for k, v in env.items() if counts[k] == 1 and set_first(k)}


def _target_cats(target, known, bare, cwds, lost, shell, ctx, classify, note="", guess=True):
    """(category, detail) for one write target, through the variables known here (T-0175: a target with a $ in it was
    skipped), in every place the shell may be. A resolved one is named by its path, so a standing or trusted yes covers
    it as usual. One the command itself makes unknown (a name it sets in a way the guard can't follow, a command
    substitution) could be any path the command names, in the unknown part's place; a relative one after a cd the guard
    couldn't follow, any folder the command names. Each counts, the way interpreter code is judged."""
    here = cwds or [ctx.cwd]
    t = re.sub(r"^~-(?=/|$)", "$OLDPWD", re.sub(r"^~\+(?=/|$)", "$PWD", target))  # review: ~+ and ~-
    t = _with_vars(t, {**known, "PWD": cwds[0]} if len(cwds) == 1 and not lost else known)
    found = []
    if not _unresolvable(t):
        e = _expand(t, ctx)
        for path in dict.fromkeys(_resolve(e, b) for b in ([ctx.cwd] if os.path.isabs(e) else cwds)):
            found += [(cat, f"{path}{note}") for cat in classify(path, ctx)]  # T-0180: its real path, as Edit's
            found += [(cat, f"{p}{note}") for p in _expansions(path) if p != path for cat in classify(p, ctx)]
        if os.path.isabs(e) or not lost or not guess:
            return found
    elif not guess:  # T-1224: reads and modes judge resolved paths only
        return found
    elif not any(not (m.group(1) or m.group(2)) or bare is None or (m.group(1) or m.group(2)) in bare
                 or _SHELL_SET.match(m.group(1) or m.group(2)) for m in _PART.finditer(t)):
        # only names it neither sets nor inherits: bash expands them to nothing (T-0374: echo x > $NOPE/<guard file>
        # wrote the guard file), so the target is the rest of the word
        e = _expand(_PART.sub("", t), ctx)
        for path in dict.fromkeys(_resolve(e, b) for b in ([ctx.cwd] if os.path.isabs(e) else cwds)):
            found += [(cat, f"{target}{note} (an unset name is empty: {path})") for cat in classify(path, ctx)
                      if cat in _GUARDED_BY_PATH]
        return found
    text = re.sub(r"(?<![\w$])[A-Za-z_]\w*\+?=", " ", shell)  # T-0190: a variable's name is no guess, its value is
    raw = [w for w in dict.fromkeys(_with_vars(w, known) for w in _WORD.findall(text)) if not _unresolvable(w)]
    if _unresolvable(t):
        # T-0183: words as written, one per unknown part, the first two paired (a word in every part guessed
        # <abs>/<abs>), the rest a neutral name; the whole guess is resolved after. T-0374: and every part empty,
        # as an unset name (or a substitution that prints nothing) expands
        raw, pair = raw[:GUESS_WORDS], len(list(_PART.finditer(t))) > 1
        guesses = [_resolve(_expand(_PART.sub("", t), ctx), base) for base in here]
        for a in raw:
            for b in raw if pair else [None]:
                vals = iter((a, b))
                guess = _PART.sub(lambda _: next(vals, None) or "x", t)
                guesses += [_resolve(_expand(guess, ctx), base) for base in here]
    else:  # relative, somewhere a cd went that the guard couldn't follow: only a folder that exists takes a cd
        words = [p for w in raw for p in dict.fromkeys(_resolve(_expand(w, ctx), b) for b in here)]
        guesses = [os.path.join(w, x, _expand(t, ctx)) for w in words for x in lost if os.path.isdir(os.path.join(w, x))]
    for path in dict.fromkeys(guesses):
        if _possible(path):
            found += [(cat, f"{target}{note} (not known before it runs: it could be {path})")
                      for cat in classify(path, ctx) if cat in _GUARDED_BY_PATH]
    return found


def _raw_cmds(shell):
    """T-0161 review: a straight-line command's simple commands as written, quotes kept (shlex drops them, and
    `"D=x"`, `\\D=x` and `D"="x` are commands in bash, not assignments). None when the quoting can't be read."""
    if "$'" in shell:
        return None
    cmds, words, cur, q, i, text = [], [], "", None, 0, _strip_comments(shell)
    while i < len(text):
        ch = text[i]
        if ch == "\\" and q != "'":
            cur += text[i:i + 2]
            i += 2
            continue
        if q:
            q = None if ch == q else q
        elif ch in "'\"":
            q = ch
        elif ch in " \t\n;" or text[i:i + 2] == "&&":
            words, cur = (words + [cur]) if cur else words, ""
            if ch != " " and ch != "\t" and words:
                cmds, words = cmds + [words], []
            i += 2 if ch == "&" else 1
            continue
        cur += ch
        i += 1
    if q:
        return None
    words += [cur] if cur else []
    return cmds + ([words] if words else [])


def _unquote(word):
    try:
        return "".join(shlex.split(word))
    except ValueError:
        return None


def _shell_c(args):
    """The command strings `sh -c` runs: the word after a bare -c, and (T-0324) the first operand once any option
    cluster holds c (bash -lc, zsh -o x -ic, bash --rcfile f -ec -- CMD)."""
    out = [args[args.index("-c") + 1]] if "-c" in args and args.index("-c") + 1 < len(args) else []
    has_c, i = False, 0
    while i < len(args):
        a = args[i]
        if a == "--":
            i += 1
            break
        if a in ("-o", "+o", "-O", "+O", "--rcfile", "--init-file"):
            i += 2
        elif re.fullmatch(r"[-+][a-zA-Z]+", a):
            has_c = has_c or (a[0] == "-" and "c" in a)
            i += 1
        elif a.startswith("--"):
            i += 1
        else:
            break
    if has_c and i < len(args) and args[i] not in out:
        out.append(args[i])
    return out


# T-0892: NAME=$(mktemp -d) (no -p/--tmpdir/template) is a fresh folder in TMPDIR or /tmp: read as that literal path,
# so `rm -r $T` later is a known target, and `$T/../..` still resolves to what it would remove
_MKTEMP_D = re.compile(r"""(?<![\w$])(\w+=)(["']?)(?:\$\(\s*mktemp\s+-d\s*\)|`\s*mktemp\s+-d\s*`)\2""")
# T-0906: a command that names TMPDIR or PATH at all (TMPDIR=, TMPDIR[0]=, ${TMPDIR:=…}), gives a shell an rc file
# (BASH_ENV, ENV, --rcfile, --init-file), defines its own mktemp or repoints it (hash -p, enable, an alias) makes the
# folder somewhere else (after eval or source the guard already treats T as unknown: see the KnownVars cases)
_MKTEMP_MOVED = re.compile(r"\b(?:TMPDIR|PATH|BASH_ENV|ENV)\b|--(?:rcfile|init-file)\b|\bmktemp\s*\(\s*\)|"
                           r"\bfunction\s+mktemp\b|\balias\b[^;&|\n]*\bmktemp\b|\b(?:hash|enable)\s")


def _mktemp_literal(cmd):
    if _MKTEMP_MOVED.search(cmd):
        return cmd
    return _MKTEMP_D.sub(lambda m: m.group(1) + os.path.join(os.environ.get("TMPDIR") or "/tmp", "tmp.mktemp"), cmd)


def _track_vars(words, env, home=None):
    """T-0161: the variables after one simple command (its words as written), or None once any could be unknown."""
    words = [w for i, w in enumerate(words) if not re.match(r"\d*(?:[<>]|&>)", w)  # redirections and their targets
             and not (i and re.fullmatch(r"\d*(?:[<>]+&?|&>>?)\|?", words[i - 1]))]
    runner = False
    while words and words[0] in ("!", "time", "command", "builtin"):  # unquoted: these keep the command in this shell
        runner = runner or words[0] in ("command", "builtin")  # whose `command D=x` runs a program named D=x
        words = words[1:]
        while words and words[0].startswith("-"):
            words = words[1:]
    if words[:1] == ["export"] and all(_ASSIGN.match(w) or re.fullmatch(r"\w+", w) for w in words[1:]):
        words, runner = [w for w in words[1:] if "=" in w], False  # a bare name keeps its value
    if not runner and all(_ASSIGN.match(w) for w in words):
        for w in words:
            k, rv = _ASSIGN.match(w).group(1), w.partition("=")[2]
            # T-0330: an unquoted leading ~ or ~/ in an assignment is the home folder (bash expands it there)
            v = _unquote(home + rv[1:] if home and re.match(r"~(?:/|$)", rv) else rv)
            if k == "IFS":
                return None  # word splitting changes: no expansion can be read
            if _SHELL_SET.match(k) or v is None or _unresolvable(v) or re.search(r"[*?\[~\s]", v):
                env.pop(k, None)  # a glob, a tilde form or a space is expanded or split later: leave it unknown
            else:
                env[k] = v
        return env
    for m in filter(None, map(_ASSIGNISH.match, words)):  # a prefix assignment (it can outlive a special builtin),
        if m.group(1) == "IFS":                            # NAME+= or NAME[i]=, or one a command is handed
            return None
        env.pop(m.group(1), None)
    word = next((w for w in words if not _ASSIGNISH.match(w)), "")
    m = re.fullmatch(r"\$(?:\{(\w+)\}|(\w+))(/[^$`*?\[\s'\"\\{]*)", word)
    if m and (m.group(1) or m.group(2)) in env:  # T-0384: $S/tool with S a known literal (no space, glob or $) is a
        word = env[m.group(1) or m.group(2)] + m.group(3)  # path, and a path is never a builtin
    if re.search(r"[$`*?\[]", word):
        return None  # T-0162: a name bash computes ($X, `…`, a glob) can turn out to be a builtin
    name = _unquote(word) or ""
    return None if _setter(name, words[words.index(word) + 1:] if word in words else []) else env


def check_bash(cmd, ctx, depth=0, tails=True):
    """Return [(category, detail)] for every dangerous thing found in a shell command."""
    if depth > 4:
        return [("rm-outside", "command nesting too deep to analyse")]
    # the whole command only: a nested shell's text alone would miss what its caller set (BASH_ENV=… bash -c '…')
    cmd = _mktemp_literal(_join_continued(cmd)) if depth == 0 else _join_continued(cmd)
    unreadable = _ifs_unreadable(cmd)  # added last, never instead: a granted system mustn't let the rest through
    cmd = _ifs_spaces(cmd)  # T-0576: rm${IFS}-rf ~ is "rm -rf ~" to bash (IFS splits the expansion into words)
    cmd = _expand_literal_loops(cmd)  # T-0411: a loop over literal words, as the commands it runs
    found = _interpreter_writes(cmd, ctx)  # every depth: an fm --run command is read on its own (T-0128 review)
    # T-0345: what python code starts; a script only written with cat isn't run by writing it, unless the same
    # command also runs an interpreter (cat > t.py <<EOF … EOF; python3 t.py)
    dry = _drop_data_heredocs(cmd)
    for spawned in (x for src in _python_sources(cmd if _INTERP.search(dry) else dry) for x in _spawned_commands(src)):
        found += check_bash(spawned, ctx, depth + 1)
    shell = _strip_heredocs(cmd)
    # T-0158: every `…` and $( … ) a shell runs (unquoted heredoc bodies included), read as a command of its own
    # a tail (the text after a substitution opens) is read once as it stands: its own tails are suffixes of it already
    live = [x for t in _live_heredocs(cmd) for x in ([t, _unescape_ticks(t)] if "\\`" in t else [t])]  # T-0669: in
    for body in _subst_bodies(shell, tails) + [b for t in live for b in _subst_bodies(t, tails)]:  # `…` a \` is a `
        found += check_bash(body, ctx, depth + 1, tails=False)
    cmds = _split(_tokens(_lines(shell)))
    lits = _line_literals(shell)  # T-0587: literal values a computed name, eval or sh -c text may use
    for script in _stdin_scripts(cmd, cmds):  # T-0589: bash <<'EOF' … EOF and sh <<< '…' run that text
        found += check_bash(script, ctx, depth + 1)
    cwd, chain = ctx.cwd, []
    raw = _raw_cmds(shell) if _straight_line(shell) else None  # the same commands, quotes kept (T-0161)
    # T-0330 review: ~ is $HOME, so once the command may set HOME a ~ in a value isn't the user's home any more
    tilde = None if re.search(r"(?<![\w${])HOME\b", shell) else ctx.home
    pre = _prefix_vars(shell, cmds, tilde)  # T-0183; also what a path-named command may expand (T-0331)
    outside, bare = _outside(shell, cmds, ctx, pre)  # T-0175: what it inherits and can't change
    # VAR → literal (T-0151); rm trusts no inherited value but HOME, a write target any (its review)
    env = {k: v for k, v in outside.items() if k == "HOME"} if raw is not None and len(raw) == len(cmds) else None
    (straight, and_chain, mixed), cwds, lost, made = _top(shell), [ctx.cwd], [], set()  # where it may be (T-0175)
    base = None  # T-0339: (cwds, lost, made) where the current &&-segment of a mixed list began, and its folders
    cdpath = bare is None or "CDPATH" in shell or bool(os.environ.get("CDPATH"))
    fixed = pre if env is None and bare is not None else {}  # T-0183: set once before the
    outside = {**outside, **fixed}                                                  # branches, known in them
    scan = _mask_fm(shell, ctx)  # T-0183: guess from the command's own words, not fm's text arguments
    wrote, fed = [], []  # T-0275: files earlier commands here write (all; and those a heredoc fills)
    for idx, c in enumerate(cmds):
        nxt_op = cmds[idx + 1].op if idx + 1 < len(cmds) else ""
        piped = c.op in ("|", "|&") or nxt_op in ("|", "|&")  # T-0355: in a pipeline, a cd moves its subshell only
        in_chain = mixed and not piped and (c.op == "&&" or nxt_op == "&&")
        if mixed and c.op not in ("&&", "|", "|&"):  # a new segment: the last one's chain may have stopped anywhere
            if base:
                cwds, lost = list(dict.fromkeys(base[0] + cwds)), list(dict.fromkeys(base[1] + lost))
                made = base[2]
            ops = [x.op for x in cmds[idx + 1:]]
            seg = ops[:next((i for i, o in enumerate(ops) if o not in ("&&", "|", "|&")), len(ops))]
            base = (cwds, lost, set(made)) if "&&" in seg else None
        if env is not None:
            env = _track_vars(raw[idx], env, tilde)
        known = outside if env is None else {**outside, **env}
        argv, via_xargs = _strip_wrappers(c.argv)
        xodd = via_xargs and any(_xargs_opts(c.argv[j + 1:])[1] for j, x in enumerate(c.argv[:len(c.argv) - len(argv)])
                                 if os.path.basename(x) == "xargs")  # T-1123
        if not c.piped:
            chain = []
        name = os.path.basename(argv[0]) if argv else ""
        args = argv[1:]
        if name == "mkdir" and "-p" in args:  # a folder this command makes takes a cd as surely as one that exists,
            made.update(d for d in (os.path.normpath(_expand(_with_vars(a, known), ctx)) for a in args)  # when its
                        if os.path.isabs(d) and "$" not in d and _makeable(d))  # nearest existing folder lets it be made
        if name in ("cd", "pushd", "popd"):
            dirs = [a for a in args if a not in ("-P", "-L", "-e", "-@", "--")]
            if name == "cd" or "-n" not in dirs:  # pushd/popd -n change only the stack
                unknown = name == "popd" or dirs[:1] == ["-"] or (
                    name == "pushd" and (not dirs or re.fullmatch(r"[+-]\d+", dirs[0])))  # rotations, a swap, cd -
                tgt = "$OLDPWD" if unknown else _with_vars(dirs[0], known) if dirs else ctx.home
                if not _unresolvable(tgt):
                    cwd = _resolve(_expand(tgt, ctx), cwd)
                d = "" if _unresolvable(tgt) else _expand(tgt, ctx)
                can_fail = len(dirs) > 1 or not (os.path.isabs(d) and (os.path.normpath(d) in made or (  # review: cd a b
                    os.path.isdir(d) and os.access(d, os.X_OK))))  # fails with too many arguments
                certain = not piped and (and_chain or in_chain or ((straight or mixed) and not can_fail))
                cwds, lost = _moved(cwds, lost, tgt, certain, cdpath, ctx)
                if base and c.op not in ("&&", "|", "|&") and not piped and not can_fail:
                    base = (list(cwds), list(lost), base[2])  # T-0384: a head cd that can't fail: the chain stops after
                elif base:  # the chain may stop after any cd in it: every folder it reaches stays possible (its review)
                    base = (base[0] + cwds, base[1] + lost, base[2])
        moves, places = (_moves_shell(name, args, cwds, ctx, shell) if name in ("eval", "source", ".", "trap",
                                                                               "mapfile", "readarray") else (0, []))
        if moves:  # T-0384: it may cd here: anywhere, or any folder it names after a cd
            for d in ["$OLDPWD"] + places:
                cwds, lost = _moved(cwds, lost, d, False, cdpath, ctx)
            if base:
                base = (base[0] + cwds, base[1] + lost, base[2])
        for inner in (x for t in _shell_c(args) for x in _readings(t, {**lits, **known})) if _SHELLS.match(name) else ():
            found += check_bash(inner, ctx, depth + 1)
            if _DOWNLOAD_SUBST.search(inner):
                found.append(("pipe-shell", f"{name} -c runs a downloaded script"))
        # T-0160 (differential test against bash): commands these run as text or as their own arguments
        if name == "trap" and args and not args[0].startswith("-"):
            found += check_bash(args[0], ctx, depth + 1)
        if name == "script":
            for j, a in enumerate(args[:-1]):
                if a in ("-c", "--command") or re.fullmatch(r"-[a-zA-Z]*c", a):
                    found += check_bash(args[j + 1], ctx, depth + 1)
        if name == "find":
            for j, a in enumerate(args):
                if a in ("-exec", "-execdir", "-ok", "-okdir"):
                    end = next((k for k in range(j + 1, len(args)) if args[k] in (";", "+")), len(args))
                    found += check_bash(" ".join(shlex.quote(x) for x in args[j + 1:end]), ctx, depth + 1)
        if name == "eval":
            joined = " ".join(args)
            for text in _readings(joined, {**lits, **known}):  # T-0587: q='rm -rf'; eval "$q ~"
                found += check_bash(text, ctx, depth + 1)
            for m in _PRINTED_SUBST.finditer(joined):  # T-1123: eval "$(printf 'rm -rf ~')" runs the printed text
                try:
                    w = shlex.split(m.group(2))
                except ValueError:
                    w = []
                cmdname, w = (w[0], w[1:]) if w else ("", [])
                if cmdname == "echo":
                    w = [a for a in w if a != "-n"]
                if w and (cmdname == "echo" and not any(a.startswith("-") for a in w[:1] if a != "--") or
                          cmdname == "printf" and not re.search(r"[%\\]", w[0])):
                    found += check_bash(" ".join(w), ctx, depth + 1)
                else:  # flags, escapes, a format, a wrapped or pathed echo: the text isn't what is written
                    found.append(("rm-outside", "eval of computed text"))
            if _DOWNLOAD_SUBST.search(joined):
                found.append(("pipe-shell", "eval of a downloaded script"))
        computed = bool(re.search(r"[$`]", name))  # `| $GREP pat` is common: any word after it counts as its script
        # ponytail: a bare `$` name inside a substitution reading is the read-to-the-end tail of "$(a) | $(b)" in
        # quotes, not a pipe; a real `| $(echo bash)` nested inside another $( ) slips by (top level is refused)
        # T-0982: inside a substitution reading (depth > 0: a "$( )" tail read to the end, odd quotes and all), a
        # "name" holding a quote or a redirect is debris of the quote-blind fallback split, e.g. awk's program
        # $1<1200'. The top-level command is still read whole, so a real | python3 there is still refused
        debris = bool(depth and re.search(r"['\"<>]", name))
        if c.piped and not debris and not (name == "$" and depth) and _reads_stdin_code("bash" if computed else name, args, via_xargs, any_word=computed) and not (
                # T-0715: echo 'rm -rf ~' | bash; T-0716: | (sh), | $SH (a computed name may be a shell); a
                any(_name(x.argv) in _FETCHERS for x in chain) or _FETCH_WORD.search(_mask_quotes(cmd))):  # download
            # piped in is pipe-shell's (below), which the user can grant for an installer
            found.append(("system", f"{name} reads its program from a pipe, which the guard can't read: put it in a "
                                    f"heredoc ({name} <<'EOF' … EOF), which it reads, or in a file"))
        if _SHELLS.match(name) or name in ("source", "."):
            # T-0421: a download anywhere on the line counts (a $( ), a group or a <( ) splits it from the shell's own
            # chain; a file downloaded first and then piped in is a download too), and so does a pipe into a group
            fetched = any(_name(x.argv) in _FETCHERS for x in chain) or _FETCH_WORD.search(_mask_quotes(cmd))
            if (c.piped or "|" in c.op) and fetched and not _reads_pipe_as_data(c, argv, cmds, cwds, cmd):
                found.append(("pipe-shell", f"downloaded content piped into {name}"))
            nxt = cmds[idx + 1] if idx + 1 < len(cmds) else None
            if c.procsub and nxt and _name(nxt.argv) in _FETCHERS:
                found.append(("pipe-shell", f"{name} <(download)"))
        git_env = [a.split("=", 1)[1] for a in c.argv if name == "git" and a.startswith(("GIT_DIR=", "GIT_WORK_TREE="))]
        if name == "git" and any(re.match(r"(?i)GIT_CONFIG_(KEY_\d+|PARAMETERS)=.*core\.hookspath", a) for a in c.argv):
            found.append(("system", "git with core.hooksPath set through the environment"))
        # T-0269/T-0270: a command git (or a program) will run on its own is checked as if typed; config it would load
        # from elsewhere is refused; a file a variable makes it write is a write target
        for why, code in _env_channels(c.argv, name) + (_git_code(args) if name == "git" else []) + _exec_options(
                name, args):
            found += [("system", why)] if code is None else check_bash(code, ctx, depth + 1)
        # T-0275: the file a shell, source, python or an executable with a #! line is told to run
        kind, script = _script_target(name, argv[0] if argv else "", args)
        if script:
            norm = lambda w: os.path.normpath(os.path.join(cwd, os.path.expanduser(w)))  # noqa: E731
            path = norm(script)
            if path in {norm(w) for w in fed} and kind != "py":  # cat > f <<'EOF' … EOF; bash f: the body is the script
                for body in _heredoc_split(cmd)[1]:  # (which heredoc wrote it isn't modelled: all are read, as for bash <<EOF)
                    found += check_bash("\n".join(body), ctx, depth + 1)
            # a python script written by a heredoc in this command is read by the heredoc scan (T-0345); a path-named
            # command is refused only when it looks like a script: curl -o x; ./x is a download, not a script
            elif path in {norm(w) for w in wrote} and not (kind == "py" and "<<" in cmd) and (
                    kind != "exec" or script.endswith((".sh", ".bash", ".zsh", ".py", ".ksh"))):
                found.append(("system", f"{script} is written earlier in this command and run here, which the guard "
                                        "can't read: write it in one command, run it in the next"))
            else:
                found += _script_verdict(script, cwd, kind, ctx, depth)
        fed += c.redirs if any(op == "<<" for op, _ in c.feeds) else []
        # an in-place edit (sed -i FILE && python3 FILE) is the everyday edit-then-run: only a file made here counts
        wrote += c.redirs + ([] if name in ("sed", "gsed", "perl", "ed", "ex") else _write_targets(name, args))
        unlinks = set(_write_targets(name, args)) if name == "rm" else set()  # T-0412: rm of a link unlinks it
        # T-0859: a bare git init where the cwd the guard resolves already holds .git rewrites nothing
        init = name == "git" and args[:1] == ["init"]  # no global options: -C and --git-dir move the target
        # security review: git takes unique prefixes of long options (--templ= is --template) and GIT_* env can plant
        # a template dir, so only `git init` / `git init -q` qualify, and only when nothing in the command sets GIT_*
        bare_init = init and not lost and not git_env and all(a in ("-q", "--quiet") for a in args[1:]) and all(
            os.path.exists(os.path.join(d, ".git")) for d in cwds or [ctx.cwd]) and not re.search(
            r"(?:^|[\s;&|(`])(?:export\s+|env\s+)?GIT_\w*=", cmd)
        # T-1195: an environment that changes how git reads pathspecs makes a named-file checkout a tree write
        # (anywhere in the command text: export, env, an earlier assignment)
        targs = args + ["--pathspec-from-file"] if name == "git" and re.search(
            r"(?:^|[\s;&|(`])(?:export\s+|env\s+)?GIT_(?:GLOB|ICASE)_PATHSPECS=", cmd) else args
        for target in c.redirs + ([] if bare_init else _write_targets(name, targs)) + git_env + _env_files(c.argv):
            how = classify_unlink if target in unlinks and not target.endswith("/") else classify_write
            found += _target_cats(target, known, bare, cwds, lost, scan, ctx, how)
        for target in [] if bare_init else _tree_targets(name, targs) + git_env:
            found += _target_cats(target, known, bare, cwds, lost, scan, ctx, classify_tree,  # T-0394: a merge's
                                  " (a tree write over it" + ("; git merge" if name == "git" and "merge" in args
                                                             else "") + ")" +  # refusal names fm lane merge
                                  ("; git init writes its folder: chain the cd with && or pass the path, "
                                   'git init "$S/toy"' if init else ""))
        # T-1224: the files it reads (operands, a < redirect), what it sends out, a recursive or world-writable mode;
        # an unknown name is guessed from the words the command names, as a write's is (security review: for f in
        # ~/.ssh/*; do cat $f; done read every key)
        for target in _read_targets(name, args) + ([c.stdin] if c.stdin else []):
            found += _target_cats(target, known, bare, cwds, lost, scan, ctx, classify_read, " (read)")
        if name in _SENDERS:
            files, stdin = _sent_files(name, args)
            for target in files:
                found += _target_cats(target, known, bare, cwds, lost, scan, ctx, classify_read, f" (sent by {name})")
            if stdin and c.piped and any(_prints_environment(x) for x in chain):
                found.append(("credentials", f"the environment piped into {name}, which sends it off the machine"))
        targets, recursive = _mode_targets(name, args)
        for target in targets:
            found += _target_cats(target, known, bare, cwds, lost, scan, ctx,
                                  lambda p, x: classify_system_mode(p, x, recursive),
                                  f" ({name} {'recursive' if recursive else 'opening write to others'} on a system "
                                  "folder)", guess=False)
        if name == "fm" or (re.match(r"^python[0-9.]*$", name) and any(a.endswith("/fm") for a in args[:1])):
            fm_args = args[1:] if name != "fm" else args
            if any(_is_allow(a) and (a.partition("=")[2] or b) in USER_ONLY for a, b in zip(fm_args, fm_args[1:] + [""])):
                found.append(("self-authorize", "an agent may not grant core or remote"))
            sub, rest = _fm_subcommand(fm_args)
            # commands fm runs on Claude's behalf (evidence --run, stored gates) get the checks a typed one would
            for a, b in zip(fm_args, fm_args[1:] + [""]):
                flag, eq, val = a.partition("=")
                if flag.startswith("--r") and "--run".startswith(flag):
                    found += check_bash(val if eq else b, ctx, depth + 1)
            for stored in _fm_stored(sub, rest, fm_args):  # T-0901: a command fm keeps and runs later
                found += check_bash(stored, ctx, depth + 1)
            if sub in ("quiet", "at"):  # T-0898: their trailing command runs (fm quiet -- rm -rf ~ used to pass)
                words = _fm_trailing(rest, 1 if sub == "at" else 0)
                if words:
                    found += check_bash(words[0] if len(words) == 1 else " ".join(map(shlex.quote, words)), ctx,
                                        depth + 1)
            if sub == "plugins" and rest[:1] and rest[0] in ("install", "enable", "disable", "add-marketplace"):
                target = plugin_mark(_one_plugin([a for a in rest[1:] if not a.startswith('-')])) \
                    if rest[0] in ("install", "enable") else ""
                found.append(("plugin", f"fm plugins {rest[0]} changes Claude Code's plugins{target}"))
            if sub in USER_ONLY_FM and any(_user_only_hit(USER_ONLY_FM[sub][0], a) for a in rest):  # flag order is free
                word, why, typed = USER_ONLY_FM[sub]
                found.append(("self-authorize", f"{why} (they can type ! {typed})"))
            if sub == "agents" and "uninstall" in rest[:2]:  # T-0340: it takes the guard out of another agent
                found.append(("core", "fm agents uninstall removes Foreman's guard from another coding agent"))
            if sub == "serve" and _fm_subcommand(rest, takes_value=("--permission-mode",))[0] not in ("status", "stop"):
                found.append(("remote", "fm serve starts a persistent Remote Control session reachable from the "
                                        "user's claude.ai account"))
        rm_vars = env or fixed  # T-0190: a literal set once before a branch holds for rm as for a write
        names = [name]
        if re.search(r"[$`]", name):  # T-0587: a name bash computes, read every way it may run
            m = re.fullmatch(r"\$(?:\{(\w+)\}|(\w+))", argv[0])
            val = ({**lits, **known}.get(m.group(1) or m.group(2)) if m else None)
            rest_args = [shlex.quote(a) for a in args]
            if val is not None:  # its value on this line, split as bash splits it unquoted
                found += check_bash(" ".join([val] + rest_args), ctx, depth + 1)
            found += check_bash(" ".join(rest_args), ctx, depth + 1) if args else []  # it may expand to nothing
            for t in _shell_c(args) + ([" ".join(args)] if args else []):  # T-0668 (review): or be bash -c, or eval
                for x in _readings(t, {**lits, **known}):
                    found += check_bash(x, ctx, depth + 1)
            names += _COMPUTED_AS  # or be any dangerous command
        for nm in names:
            if nm == "rm" != name and not _rm_opts_only(args):  # GNU rm stops at an option it doesn't know
                continue                                      # (-fwrapv, -Wno-unused…): nothing is deleted
            found += _check_rm(nm, [_with_vars(a, rm_vars) for a in args] if rm_vars else args, via_xargs, chain, cwd, ctx,
                               xodd)
            found += _check_git(nm, args, cwd, ctx)
            found += _check_system(nm, args)
            found += _check_claude_config(nm, args, cmd if c.piped or "<<" in cmd else "")
            found += _check_publish(nm, args)
        chain.append(Cmd(c.argv, c.redirs, c.piped))
    return found + [("system", unreadable)] if unreadable else found


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


_GIT_WORKTREE_WRITES = {"pull", "checkout", "switch", "reset", "merge", "rebase", "restore", "stash", "apply",
                        "am", "cherry-pick", "revert", "clean", "rm", "mv"}


_GIT_EXEC_KEYS = re.compile(r"(?i)^(core\.(pager|editor|fsmonitor|sshcommand|askpass|gitproxy|alternaterefscommand)|"
                            r"pager\..+|sequence\.editor|diff\.external|diff\..+\.(command|textconv)|merge\..+\.driver|"
                            r"filter\..+\.(clean|smudge|process)|credential\..*helper|gpg\.program|gpg\..+\.program|"
                            r"interactive\.difffilter|uploadpack\.packobjectshook|remote\..+\.(uploadpack|receivepack)|"
                            r"(mergetool|difftool|browser|man)\..+\.(cmd|path)|trailer\..+\.command|"
                            r"submodule\..+\.update|sendemail\.(sendmailcmd|smtpserver))$")
_GIT_VALUED = ("-C", "-c", "--git-dir", "--work-tree", "--namespace", "--config-env")  # global options taking a value
_GIT_EXEC_ENV = {"GIT_PAGER", "PAGER", "GIT_EXTERNAL_DIFF", "GIT_SSH_COMMAND", "GIT_SSH", "GIT_EDITOR", "EDITOR", "VISUAL",
                 "GIT_SEQUENCE_EDITOR", "GIT_ASKPASS", "SSH_ASKPASS", "GIT_PROXY_COMMAND"}


_GIT_CONFIG_SOURCES = {"GIT_CONFIG_GLOBAL", "GIT_CONFIG_SYSTEM", "GIT_CONFIG", "GIT_TEMPLATE_DIR", "GIT_EXEC_PATH"}
_GIT_FILE_ENV = re.compile(r"^(GIT_TRACE\w*|GIT_INDEX_FILE)$")  # a path value: git writes that file
# T-0270: options whose value is a command git runs (a short flag's value may also be attached: -O'cmd')
_GIT_EXEC_FLAGS = {"rebase": ("-x", "--exec"), "difftool": ("-x", "--extcmd"), "grep": ("-O", "--open-files-in-pager"),
                   "fetch": ("--upload-pack",), "pull": ("--upload-pack",), "clone": ("--upload-pack", "-u"),
                   "ls-remote": ("--upload-pack",), "fetch-pack": ("--upload-pack", "--exec"), "archive": ("--exec",),
                   "push": ("--receive-pack", "--exec"), "send-pack": ("--receive-pack", "--exec"),
                   "filter-branch": ("--tree-filter", "--index-filter", "--msg-filter", "--env-filter", "--commit-filter",
                                     "--parent-filter", "--tag-name-filter")}
_GIT_CONFIG_READS = {"--get", "--get-all", "--get-regexp", "--get-urlmatch", "--list", "-l", "--unset", "--unset-all",
                     "--remove-section", "--rename-section", "--show-origin", "--show-scope", "--edit", "-e"}


def _git_writes(sub, rest):
    """T-0270: the files and folders a git subcommand writes, relative to where it runs."""
    if sub == "format-patch":
        return _opt_values(rest, "-o", "--output-directory")
    if sub == "archive":
        return _opt_values(rest, "-o")
    if sub == "config":
        return _opt_values(rest, "-f", "--file")
    if sub == "checkout-index":
        return _opt_values(rest, "--prefix")
    if sub == "bundle" and rest[:1] == ["create"]:
        return _git_pos(rest[1:], ())[:1]
    if sub == "worktree" and rest[:1] == ["add"]:
        return _git_pos(rest[1:], ("-b", "-B", "--reason"))[:1]
    if sub == "init":
        return _git_pos(rest, ("--template", "-b", "--initial-branch", "--object-format", "--ref-format",
                               "--separate-git-dir"))[:1] or ["."]
    if sub in ("fast-export", "fast-import"):
        return _opt_values(rest, "--export-marks")
    if sub in ("index-pack", "bugreport", "diagnose"):
        return _opt_values(rest, "-o", "--output-directory")
    if sub == "pack-objects" and "--stdout" not in rest:
        return _git_pos(rest, ())[:1]
    if sub == "submodule" and rest[:1] == ["add"]:
        pos = _git_pos(rest[1:], ("-b", "--branch", "--name", "--reference", "--depth"))
        if pos:  # <repo> [<path>]; without a path, the repo's name
            return pos[1:2] or [re.sub(r"\.git$", "", pos[0].rstrip("/").rsplit("/", 1)[-1])]
    return []


def _git_pos(args, valued):
    """Positionals of a git subcommand's arguments, without the values of the options in `valued`."""
    out, skip = [], False
    for a in args:
        if skip:
            skip = False
        elif a in valued:
            skip = True
        elif not a.startswith("-"):
            out.append(a)
    return out


_ASSIGN_ANY = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\+?=(.*)$", re.S)  # NAME=v and NAME+=v


def _assignments(argv):
    """(NAME, value) for what a simple command sets: every assignment before its real command — wherever the
    wrappers and keywords _strip_wrappers skips put it (timeout 5 env X=…, do X=…, env -u H X=…) — and
    export/declare's arguments."""
    words = list(argv)
    stripped, _ = _strip_wrappers(words)
    cand = words[:len(words) - len(stripped)]
    if stripped and os.path.basename(stripped[0]) in ("export", "declare", "typeset", "readonly", "local"):
        cand += stripped[1:]
    return [m.groups() for m in map(_ASSIGN_ANY.match, cand) if m]


def _clip(s, n=60):
    return s if len(s) <= n else s[:n] + "…"


def _opts_match(rx):
    """A code-loading variable's check: its value is refused unread (None) when rx finds a loading option, else it is
    harmless (False)."""
    return lambda val: None if re.search(rx, val) else False


# T-0275: variables that make the next program run code. A value that is a command or a script is read (the string
# returned is checked as a command); one that names a binary or a module can't be read here: None refuses it.
_CODE_VARS = {
    "BASH_ENV": lambda v: f"source {shlex.quote(v)}", "ENV": lambda v: f"source {shlex.quote(v)}",  # ENV: sh only
    "PROMPT_COMMAND": lambda v: v, "LESSOPEN": lambda v: v.lstrip("|-") or False,
    "LESSCLOSE": lambda v: v.lstrip("|-") or False, "RSYNC_RSH": lambda v: v,
    "TAR_OPTIONS": lambda v: next((c for _, c in _exec_options("tar", _words(v)) if c is not None), False),
    "LD_PRELOAD": lambda v: None, "LD_AUDIT": lambda v: None,
    "NODE_OPTIONS": _opts_match(r"(?:^|\s)(?:-r\b|--require\b|--import\b|--loader\b|--experimental-loader\b)"),
    "PERL5OPT": _opts_match(r"(?:^|\s)-[Mm]"), "RUBYOPT": _opts_match(r"(?:^|\s)-r"),
    **{k: _opts_match(r"-(?:javaagent|agentpath|agentlib|Xbootclasspath|XX:OnOutOfMemoryError|XX:OnError)")
       for k in ("JAVA_TOOL_OPTIONS", "_JAVA_OPTIONS", "JDK_JAVA_OPTIONS")},
    **{k: _opts_match(r"\$\(|`") for k in ("PS4", "SHELLOPTS")},  # expanded by the shell on every traced line
}


def _words(s):
    try:
        return shlex.split(s)
    except ValueError:
        return s.split()


def _parse_opts(args, short="", long=()):
    """([(option, value)], positionals) of an argv: a letter in `short` takes the rest of its cluster, else the next
    word (-avze CMD, -Co OPT, -I'cmd'); a `long` option takes =value or the next word. Everything after -- is positional."""
    vals, pos, i = [], [], 0
    while i < len(args):
        a, i = args[i], i + 1
        if a == "--":
            pos += args[i:]
            break
        if a.startswith("--"):
            key, eq, v = a.partition("=")
            if key in long:
                if not eq and i < len(args):
                    v, i = args[i], i + 1
                vals.append((key, v))
        elif a.startswith("-") and len(a) > 1:
            for j, ch in enumerate(a[1:], 1):
                if ch in short:
                    v = a[j + 1:]
                    if not v and i < len(args):
                        v, i = args[i], i + 1
                    vals.append(("-" + ch, v))
                    break
        else:
            pos.append(a)
    return vals, pos


def _quoted(*words):
    return " ".join(shlex.quote(w) for w in words)


def _ssh_options(name, args):
    out = []
    vals, _ = _parse_opts(args, "BbcDEeFIiJLlmOopQRSWw" if name == "ssh" else "BbcDFiJloPRSsX")
    for opt, o in vals:
        if opt == "-o":
            m = re.match(r"\s*(\w+)\s*[=\s]\s*(.*)", o, re.S)  # Key=value and "Key value"
            key, val = (m.group(1).lower(), m.group(2).strip().strip("'\"")) if m else ("", "")
            if key in ("proxycommand", "localcommand", "knownhostscommand") and val:
                out.append((f"ssh -o {m.group(1)}", val))
            elif key in ("pkcs11provider", "securitykeyprovider") and val not in ("", "none"):
                out.append((f"ssh -o {m.group(1)}={_clip(val)} loads a library", None))
        elif opt == "-F" and o != "/dev/null":  # a config file may hold a ProxyCommand or LocalCommand
            out.append(("ssh -F config file (it may set a ProxyCommand or LocalCommand)", None))
        elif opt == "-I" and name == "ssh" and o:
            out.append((f"ssh -I {_clip(o)} loads a PKCS#11 library", None))
        elif opt == "-S" and name != "ssh" and o:  # scp/sftp -S PROGRAM replaces ssh
            out.append((f"{name} -S", o))
    return out


def _sed_code(args):
    """What sed's `e` command and `s///e` flag run: the `e COMMAND` text, or None when it is computed from the input."""
    if "--sandbox" in args:
        return []
    args = [next((f + a[len(a.partition("=")[0]):] for f in ("--expression", "--file")
                  if len(a.partition("=")[0]) >= 4 and f.startswith(a.partition("=")[0])), a)
            if a.startswith("--") else a for a in args]
    vals, pos = _parse_opts(args, "efl", ("--expression", "--file"))
    out = [("sed -f/--file runs a script file the guard can't read here", None)
           for o, _ in vals if o in ("-f", "--file")][:1]
    scripts = [v for o, v in vals if o in ("-e", "--expression")] or pos[:1]
    addr = re.compile(r"\s*(?:\d+|\$|[,~+!]|/(?:\\.|[^/\\])*/[IM]*|\\(.)(?:\\.|(?!\1).)*?\1[IM]*)")
    for text in scripts:
        unsplit = False
        for seg in re.split(r";|\n", text):
            while True:  # addresses, and the { of a block, before the command letter
                n = 0
                while (am := addr.match(seg, n)) and am.end() > n:
                    n = am.end()
                seg = seg[n:].lstrip()
                if not seg.startswith("{"):
                    break
                seg = seg[1:]
            seg = seg.rstrip().rstrip("}").rstrip()
            if seg[:1] and not seg[0].isalpha() and seg[0] not in "#=:}":
                unsplit = True  # an address form the guard doesn't parse
            m = re.match(r"e(?:\s+(.*))?$", seg)
            if m:
                out.append(("sed e command", m.group(1) or None))
            elif seg.startswith("s") and len(seg) > 1:
                d = re.escape(seg[1])
                if re.match(rf"s{d}(?:\\.|[^{d}\\])*{d}(?:\\.|[^{d}\\])*{d}\w*e", seg):
                    out.append(("sed s///e runs its result as a command", None))
                elif not re.fullmatch(rf"s{d}(?:\\.|[^{d}\\])*{d}(?:\\.|[^{d}\\])*{d}[\w\s}}]*", seg):
                    unsplit = True  # a ; (or newline) inside the s command cut it: the split is a guess
        if unsplit and re.search(r"[/|#,:@!]e\b|(?:^|[;\n{}\s])e(?:\s|$)", text):
            out.append(("sed script with an e command or flag the guard can't split reliably", None))
    return out


def _vim_code(args):
    """-S/-s/-u/-l/--cmd load a script the guard can't read; in a -c or + command a `!` (after a space, an address, r
    or read; not wq!) runs the rest in the shell, and :py/:lua/system() run code."""
    out = []
    i = 0
    while i < len(args):
        a, i = args[i], i + 1
        nxt = args[i] if i < len(args) else ""
        if a.startswith("-S") or a in ("-s", "-l", "--cmd") or a == "-u" and nxt not in ("NONE", "NORC", "DEFAULTS"):
            out.append((f"vim {a} loads a script the guard can't read", None))
            continue
        cmd = nxt if a == "-c" else a[2:] if a.startswith("-c") and len(a) > 2 else a[1:] if a.startswith("+") else None
        if not cmd:
            continue
        bangs = [x.rstrip("\"' ") for x in re.findall(r"(?:^|[\s:|%,;\"'$\d]|\br|\bread)!\s*(\S.*)$", cmd)]
        out += [("vim !command", x) for x in bangs if x]
        if not bangs and re.search(r"(?:^|[\s:|])(?:system\(|py3?\b|python3?\b|pyx\b|lua\b|perl\b|ruby\b|terminal\b)", cmd):
            out.append(("vim command that runs code", None))
    return out


def _exec_options(name, args):
    """T-0275: [(why, shell code or None)] for the command string an option makes a program run (tar --to-command,
    ssh -o ProxyCommand, rsync -e, zip -TT, less +!cmd, vim -c !cmd, sed e). None: refused, it can't be read here.
    Long options match by prefix as GNU getopt does (--to-com= is --to-command); a prefix of two exec options
    expands to the first."""
    out = []
    longs = {"tar": ("--to-command", "--use-compress-program", "--info-script", "--new-volume-script",
                     "--checkpoint-action", "--rsh-command", "--rmt-command"), "rsync": ("--rsh",),
             "zip": ("--unzip-command",)}.get({"gtar": "tar", "bsdtar": "tar"}.get(name, name), ())
    if longs:
        args = [next((f + a[len(a.partition("=")[0]):] for f in longs if f.startswith(a.partition("=")[0])
                      and len(a.partition("=")[0]) >= 5 and a.partition("=")[0] != "--checkpoint"), a)
                if a.startswith("--") else a for a in args]
    if name in ("tar", "gtar", "bsdtar"):
        vals, _ = _parse_opts(args, "bCfFgHIKLNTVX", longs)
        for opt, v in vals:
            if opt == "--checkpoint-action":
                out += [("tar --checkpoint-action exec", v[5:])] if v.startswith("exec=") and v[5:].strip() else []
            elif opt in ("-I", "-F") or opt in longs:
                out += [(f"tar {opt}", v)] if v.strip() else []
    elif name in ("ssh", "scp", "sftp"):
        out += _ssh_options(name, args)
    elif name == "rsync":
        vals, _ = _parse_opts(args, "eBTfM@", ("--rsh",))
        out += [("rsync -e", v) for o, v in vals if o in ("-e", "--rsh") and v.strip()]
    elif name == "zip":
        out += [("zip -TT", v) for v in _opt_values(args, "-TT", "--unzip-command") if v.strip()]
    elif name == "less":
        out += [("less +!", a[2:]) for a in args if a.startswith("+!")]
    elif name in ("vim", "vi", "nvim", "view", "ex", "gvim"):
        out += _vim_code(args)
    elif name in ("sed", "gsed"):
        out += _sed_code(args)
    return out


_SCRIPT_LIMIT = 1 << 18
_SH_NAME = re.compile(r"^(ba|z|da|k|fi|c|tc)?sh$")


def _script_text(path, cwd, shebang=False, data=None):
    """(text, problem, kind) of a script file a shell, source or python is told to run (shebang: of an executable run
    by its path, read only when it starts #! with a shell or python; a binary or other script is no concern).
    text None: not read (computed, missing, not a plain file). problem: refused (over the size limit).
    data: the file's bytes (at most limit + 1) the caller already read and hashed: the text is those bytes, never a
    second open that a swap could answer differently.
    ponytail: a script a variable names is not read; one over 256 KB is refused, run by path it is skipped."""
    if re.search(r"[$`*?\[]", path):
        return None, None, None
    p = os.path.join(cwd, os.path.expanduser(path))
    try:
        if not os.path.isfile(p):
            return None, None, None
        kind = None
        if shebang:
            if not os.access(p, os.X_OK):
                return None, None, None
            if data is not None:
                head = data[:256].split(b"\n")[0].decode("utf-8", "replace")
            else:
                with open(p, "rb") as f:
                    head = f.readline(256).decode("utf-8", "replace")
            words = head[2:].split() if head.startswith("#!") else []
            interp = os.path.basename(words[1] if words[:1] and os.path.basename(words[0]) == "env" and len(words) > 1
                                      else words[0]) if words else ""
            kind = "py" if interp.startswith("python") else "sh" if _SH_NAME.match(interp) else None
            if kind is None:
                return None, None, None
        size = len(data) if data is not None and len(data) <= _SCRIPT_LIMIT else os.path.getsize(p)
        if size > _SCRIPT_LIMIT:
            if shebang:
                return None, None, None
            return None, f"{path} is {size // 1024} KB, over the {_SCRIPT_LIMIT >> 10} KB the guard reads: run its " \
                         f"commands directly or split it", kind
        if data is not None:
            return data.decode("utf-8", "replace"), None, kind
        with open(p, encoding="utf-8", errors="replace") as f:
            return f.read(), None, kind
    except OSError:
        return None, None, None


def _script_chunks(text, limit=2000):
    """A script's text cut at blank lines into pieces check_bash reads on their own: reading it whole is quadratic
    (a 21 KB deploy script took 12 s). A piece stays open while a quote or a heredoc is open in it; a cut never
    drops text."""
    out, cur = [], []
    for line in text.split("\n"):
        cur.append(line)
        chunk = "\n".join(cur)
        if len(chunk) < limit // 4:
            continue
        open_here = any(not re.search(rf"^\s*{re.escape(m.group(1))}\s*$", chunk[m.end():], re.M)
                        for m in re.finditer(r"<<-?\s*['\"]?(\w+)['\"]?", chunk))
        if not open_here and chunk.count("'") % 2 == 0 and chunk.count('"') % 2 == 0 and chunk.count("`") % 2 == 0 \
                and chunk.count("$(") <= chunk.count(")") and not chunk.rstrip().endswith("\\"):
            out.append(chunk)
            cur = []
    return out + (["\n".join(cur)] if cur else [])


def _check_script(text, ctx, depth, acc):
    """check_bash over a script file's pieces, keeping what is certain: a target a variable holds ("not known before
    it runs", `$HOME/x`) is every script's `rm -rf "$DIR"`, and one that reads .env is a deploy script: counting them
    refused 4 of 10 real scripts. ponytail: a literal danger (rm -rf ~, a pipe into a shell) is what is caught.
    What it finds goes into `acc` as it goes, so a read cut off by the time budget keeps what it had."""
    # only what no script of the user's does innocently: a deploy script reboots, installs plugins, reads .env, and
    # splits words on IFS (replay of 3 real scripts: reboot, plugin, system and credentials refusals were all benign)
    state = []  # what earlier pieces did that a later one depends on: cd, literal assignments, files written
    for chunk in _script_chunks(text):
        # core: a script of Foreman's own (evals) writes its checkout; only its state folder counts
        for f in check_bash("\n".join(state[-40:] + [chunk]), ctx, depth + 1):
            if f == ("system", "script nests too deep to read"):
                pass  # from a script further down the chain: it keeps its way up
            elif "too deep" in f[1]:
                # a chain of scripts this deep hides its last one: refuse, never read as clean. Only from the third
                # script in a chain: a script of its own deep $( … ) nesting is no chain (5 of 330 real scripts)
                if len(_IN_SCRIPT) < 3:
                    continue
                f = ("system", "script nests too deep to read")
            elif not ((f[0] in ("rm-outside", "self-authorize", "state-direct") or f[0] == "core" and "/state" in f[1]
                       or f[0] == "system" and ("is written earlier in this command" in f[1] or "too deep" in f[1]))
                      and "$" not in f[1] and not re.search(r"not known|unresolvable|from stdin", f[1])):
                continue
            if f not in acc:  # the carried lines are read again with each piece
                acc.append(f)
        state += _state_lines(chunk)
    return acc


_STATE_LINE = re.compile(r"^\s*(?:(?:cd|pushd|popd)\b.*|(?:(?:export|declare|local|readonly)\s+)?[A-Za-z_]\w*=[^\s`$(]*"
                         r"|.*(?:[^<>&\d]|^)>>?\s*(?!/dev/null)[^\s&>|]\S*.*|.*\b(?:tee|cp|mv|install|ln)\b.*)$")
_HEREDOC_OP = re.compile(r"<<-?\s*['\"]?\w+['\"]?")


def _state_lines(chunk):
    """The lines of a piece a later piece may depend on: a cd, a plain assignment, a write (heredoc operators cut, so a
    carried line never opens a heredoc). Pieces are read with these in front, so `cd /` in one and `rm -rf etc` in the
    next are read as one script, and so is a file written in one and run in the next. ponytail: the last 40 lines."""
    out = []
    for line in chunk.split("\n"):
        line = _HEREDOC_OP.sub("", line)
        if line.strip() and not line.lstrip().startswith("#") and len(line) < 400 and "<<" not in line \
                and not line.rstrip().endswith("\\") and _STATE_LINE.match(line):
            out.append(line)
    return out


class _OverBudget(BaseException):  # not an Exception: check_bash's own handlers must not swallow it
    pass


_UNREAD = []  # (path, why) of scripts this call left unread (the hook logs and notes them)
_IN_SCRIPT = []  # non-empty while a script is being read: the outermost read owns the clock


def take_unread():
    out, _UNREAD[:] = list(_UNREAD), []
    return out


def _script_budget():
    try:
        return float(os.environ.get("FM_GUARD_SCRIPT_BUDGET") or _BUDGET)
    except ValueError:
        return _BUDGET


_BUDGET = 0.2  # CPU seconds. 0.5 gave a cold hook p95 of 331 ms over 330 real scripts (goal 300); 0.2 trims the tail


def _script_cache_path(ctx):
    """In Foreman's state folder, where the guard refuses a direct write: a session can't forge an entry."""
    return os.path.join(ctx.state_dir or os.path.join(ctx.foreman_home, "state"), "guard-scripts.json")


_GUARD_HASH = []


def _guard_hash():
    """sha256 of this file's bytes: an edited guard reads every script again."""
    if not _GUARD_HASH:
        import hashlib
        with open(__file__, "rb") as f:
            _GUARD_HASH.append(hashlib.sha256(f.read()).hexdigest()[:16])
    return _GUARD_HASH[0]


_CACHE_MAX = 200


def _pairs(v, n):
    return isinstance(v, list) and all(isinstance(x, list) and len(x) == n and all(isinstance(y, str) for y in x)
                                       for x in v)


def _cache_load(path):
    """The cache's good entries: one that is malformed (a hand edit, a crash, an older shape) is dropped on its own,
    never an error that blocks every script run. Limit, documented not fixed: the cache is trusted as the guard's own
    file because the guard refuses a Bash write to Foreman's state; a write made outside the guard (another program
    running as the user) can forge an entry."""
    import json
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        return {}
    if not isinstance(data, dict):
        return {}
    return {k: v for k, v in data.items() if isinstance(k, str) and isinstance(v, dict) and isinstance(v.get("p"), str)
            and _pairs(v.get("f"), 2) and _pairs(v.get("n", []), 2) and isinstance(v.get("u"), (str, type(None)))
            and isinstance(v.get("at"), (int, float)) and not isinstance(v.get("at"), bool)}


def _cache_store(path, key, entry):
    """Atomic write of one more entry: files that are gone dropped first, then the oldest past 200."""
    import json
    cache = {k: v for k, v in _cache_load(path).items() if isinstance(v, dict) and os.path.exists(v.get("p", ""))}
    cache[key] = entry
    for k in sorted(cache, key=lambda k: cache[k].get("at", 0))[:max(0, len(cache) - _CACHE_MAX)]:
        del cache[k]
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = f"{path}.{os.getpid()}.tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(cache, f)
        os.replace(tmp, path)
    except OSError:
        pass  # no cache dir: the next run reads the file again


_SCAN = [(re.compile(rx, re.M | re.I if ci else re.M), why) for rx, why, ci in (
    # every quantifier is bounded: a line of NODE_OPTIONS= repeated would otherwise cost its length per occurrence
    (r"\b(?:LD_PRELOAD|LD_AUDIT|BASH_ENV|PROMPT_COMMAND|RSYNC_RSH|PERL5OPT)=[^\s\n]", "a code-loading variable", False),
    (r"\b(?:NODE_OPTIONS|RUBYOPT)=[^\n]{0,200}?(?:--require|--import|--loader|(?:^|[ \t'\"=])-r)",
     "code loaded by an option", False),
    (r"(?:^|[\s;&|(])(?:(?:ba|z|da|k)?sh\b|source\b|\.(?=[ \t])|eval\b)[^\n]{0,60}?(?:<\(|\$\(|`)\s*(?:curl|wget)\b",
     "downloaded code run", False),
    (r"-javaagent|OnOutOfMemoryError|-XX:OnError|--to-command|--use-compress-program|--checkpoint-action=exec|"
     r"--rsh-command|--rmt-command|--unzip-command", "a command an option runs", False),
    (r"\b(?:Proxy|Local)Command[ =]|\bvim?[ \t][^\n]{0,200}?-c[ \t]*['\"]?!", "a command an option runs", True),
)]
_LINE_CAP = 4096  # a longer line is scanned in overlapping pieces of this size, never as one backtracking field
_RM_TARGET = re.compile(r"/?\*?$")
_PIPE_SH = re.compile(r"(?:curl|wget)\b[^|\n]*(?:\|[^|\n]*)*?\|\s*(?:(?:sudo|exec|env|command|nohup)(?:\s+-\S+)*\s+|"
                      r"[A-Za-z_]+=\S*\s+)*(?:/\S+/)?(?:ba|z|da|k)?sh\b")


def _scan_units(text):
    """(text, original line number per line): continuation lines joined (rm \\ -rf \\ ~), lines over _LINE_CAP cut
    into overlapping pieces so no regex runs over more than that at once."""
    out, nums, lines, i = [], [], text.split("\n"), 0
    while i < len(lines):
        start, cur = i + 1, lines[i]
        # (a comment ends at its newline whatever it ends with: bash runs the next line)
        while cur.endswith("\\") and not cur.lstrip().startswith("#") and i + 1 < len(lines) and len(cur) < 4 * _LINE_CAP:
            i += 1
            cur = cur[:-1] + " " + lines[i]
        step = _LINE_CAP * 7 // 8
        for k in range(0, max(len(cur), 1), step):
            out.append(cur[k:k + _LINE_CAP])
            nums.append(start)
            if k + _LINE_CAP >= len(cur):
                break
        i += 1
    return "\n".join(out), nums


def _commented(text, pos):
    """Whether the line holding pos is a comment (`#   curl … | sh` in a usage note isn't run)."""
    return text[text.rfind("\n", 0, pos) + 1:pos].lstrip().startswith("#")


def _rm_hit(text):
    """The first `rm` with a recursive flag and a target of ~, / or $HOME (also /*, "$HOME"/*), operands and flags in
    any order, as (position, line)."""
    for m in re.finditer(r"\brm\b([^\n;&|]*)", text):
        if _commented(text, m.start()):
            continue
        ops = m.group(1)[:_LINE_CAP].split()
        flags = [o for o in ops if o.startswith("-") and not o.startswith("--") and o[1:].isalpha()]
        if any("r" in f or "R" in f for f in flags) or "--recursive" in ops:
            for o in ops:
                t = re.sub(r"/{2,}", "/", o.replace('"', "").replace("'", ""))  # ~//* and // are ~/* and /
                if not t.startswith("-") and _RM_TARGET.sub("", t) in ("", "~", "$HOME", "${HOME}"):
                    return m.start(), m.group(0)
    return None


def _fm_hit(text):
    """The first `fm …` the guard itself refuses an agent (USER_ONLY_FM verbs, --allow core|remote), as (position, line):
    read from the guard's own tables, so a new entry there is caught here."""
    for m in re.finditer(r"\bfm\b([^\n;&|]*)", text):
        if _commented(text, m.start()):
            continue
        args = [a.replace('"', "").replace("'", "") for a in m.group(1)[:_LINE_CAP].split()]
        sub, rest = _fm_subcommand(args)
        if sub in USER_ONLY_FM and any(_user_only_hit(USER_ONLY_FM[sub][0], a) for a in rest):
            return m.start(), m.group(0)
        if any(_is_allow(a) and (a.partition("=")[2] or b) in USER_ONLY for a, b in zip(args, args[1:] + [""])):
            return m.start(), m.group(0)
    return None


def _pipe_sh_hit(text):
    """The first download piped (maybe through tee, env, a path, a newline) into a shell.
    ponytail: the first 200 curl/wget words and a 1500-character window each; a pipe further on is missed."""
    pos = 0
    for _ in range(200):
        m = re.compile(r"\b(?:curl|wget)\b").search(text, pos)
        if not m:
            return None
        h = _PIPE_SH.match(text, m.start(), m.start() + 1500)
        if h and not _commented(text, m.start()):
            return m.start(), h.group(0)
        pos = m.end()
    return None


def _literal_scan(text, ctx=None):
    """[(line number, line, why)] for the dangerous literals in a script's raw text: a plain regex pass with no shell
    parsing (about 10 ms for 256 KB). What the guard falls back to when a script can't be parsed in time."""
    out = []
    text, nums = _scan_units(text)
    at = lambda pos: nums[min(text.count("\n", 0, pos), len(nums) - 1)]  # noqa: E731  original line of a position
    for hit, why in ((_rm_hit(text), "rm -r of ~, / or $HOME"), (_pipe_sh_hit(text), "a download piped into a shell"),
                     (_fm_hit(text), "an fm command only the user may run")):
        if hit:
            out.append((at(hit[0]), hit[1].strip()[:120], why))
    # a write into Foreman's state: find the path as a plain substring (a regex over the whole text was 30 ms), then
    # look for a writing word on that line
    marks = [".claude/foreman/state", "FOREMAN_HOME}/state", "FOREMAN_HOME/state"]
    if ctx is not None:  # the state folder this guard runs with, when it isn't under ~/.claude/foreman
        marks.append(ctx.state_dir or os.path.join(ctx.foreman_home, "state"))
    # a path, quote, backslash or backtick before the verb (/bin/rm, \rm, "rm", `rm`); not rm-rf-helper or install-manifest
    verbs = re.compile(r"(?:^|[\s;&|(`\"'\\])(?:[\w./-]{0,200}/)?(?:tee|cp|mv|rm|install|ln)[\"']?(?=\s)|\bsed[ \t]+-i")
    redirect = re.compile(r">>?[ \t]*[\"']?([^\s;&|\"']+)")  # the target of a redirect, not `>/dev/null` on the line
    for mark in marks:
        i = text.find(mark)
        while i != -1:
            a, b = text.rfind("\n", 0, i) + 1, text.find("\n", i)
            line = text[a:len(text) if b == -1 else b]
            if not line.lstrip().startswith("#") and (verbs.search(line) or any(
                    mark in r.group(1) for r in redirect.finditer(line))):
                out.append((at(i), line.strip(), "a write into Foreman's state"))
                break
            i = text.find(mark, len(text) if b == -1 else b)
    for rx, why in _SCAN:
        for m in rx.finditer(text):
            a, b = text.rfind("\n", 0, m.start()) + 1, text.find("\n", m.start())
            line = text[a:len(text) if b == -1 else b].strip()
            if line.startswith("#"):  # a usage comment ("#   curl … | sh") isn't run
                continue
            out.append((at(m.start()), line, why))
            break  # the first of each kind is enough to refuse
    return sorted(out)


_TEXTS = []  # (path, text) of the scripts read since the outermost read began: what a budget cut-off scans
_DEPS = []  # (path, sha256) of every nested script that read used: a cached verdict is valid while they are unchanged


def _file_digest(p):
    """sha256 of a script's bytes as the verdict read them (at most limit + 1), "" if it can't be read (absent too:
    a dependency on an absent script holds only while it stays absent). A link is followed."""
    import hashlib
    try:
        if not os.path.isfile(p):
            return ""
        with open(p, "rb") as f:
            return hashlib.sha256(f.read(_SCRIPT_LIMIT + 1)).hexdigest()
    except OSError:
        return ""


_RUN_CMD = re.compile(r"(?:^|[;&|(\s`])(?:/[^\s;&|]*/)?(?:env[ \t]+)?(?:(?:ba|z|da|k)?sh|python3?|source|\.)(?=[ \t])"
                      r"([^\n;&|)<>]{0,300})", re.M)
_RUN_DIRECT = re.compile(r"(?:^|[;&|(\s`])((?:\./|/)[^\s;&|)<>\"'$`]*(?:\.(?:sh|bash|zsh|ksh|py)\b|(?<=\./)[^\s;&|)<>\"'$`]+))",
                         re.M)


def _run_targets(text):
    """Script files a script's text runs by name: bash/sh/zsh/python/source/. X (also /bin/bash, env bash, options such
    as -e and -o pipefail before X) and a ./x or /abs/x.sh run directly. Literal words only (a $ or ` is skipped)."""
    out, text = [], text[:_SCRIPT_LIMIT]
    for m in _RUN_CMD.finditer(text):
        words, i = m.group(1).split(), 0
        while i < len(words):
            w = words[i]
            i += 1
            if w in ("-o", "+o", "-O", "+O", "-W", "-X"):
                i += 1
            elif not w.startswith(("-", "+")):
                w = w.strip("\"'")
                if w and not re.search(r"[$`]", w):
                    out.append(w)
                break
        if len(out) >= 40:
            break
    out += [m.group(1) for m in _RUN_DIRECT.finditer(text)][:40]
    return out


def _script_verdict(script, cwd, kind, ctx, depth):
    """Findings for the script file a command runs, cached by the sha256 of its bytes (and of this guard file) in
    Foreman's state folder, where the guard refuses direct writes: a script run again costs a hash, not a parse (the
    hook runs before every Bash call: a 20 KB script took seconds to parse cold). One cold read has a time budget
    (FM_GUARD_SCRIPT_BUDGET, CPU seconds, default _BUDGET). Past it the whole file gets the literal scan instead
    (_literal_scan): a hit is refused, none is allowed unread and noted in _UNREAD; either is cached. The file's own
    size over the limit is refused (_script_text)."""
    if re.search(r"[$`*?\[]", script):
        return []
    p = os.path.realpath(os.path.join(cwd, os.path.expanduser(script)))
    import hashlib
    import signal
    import time
    lex = os.path.normpath(os.path.join(cwd, os.path.expanduser(script)))  # as named: a link is followed at each check
    nested = bool(_IN_SCRIPT)
    data = None
    if os.path.isfile(p):  # a FIFO or a device would block the open below, and the hook with it
        try:
            with open(p, "rb") as f:
                data = f.read(_SCRIPT_LIMIT + 1)
        except OSError:
            pass
    if nested:  # the outer verdict is only as good as this file's bytes, or as its absence
        _DEPS.append((lex, hashlib.sha256(data).hexdigest() if data is not None else ""))
    if data is None:
        return []
    digest = hashlib.sha256(data).hexdigest()
    key = None
    if len(data) <= _SCRIPT_LIMIT:  # over it: refused below, nothing to cache
        key = "|".join((p, digest, hashlib.sha256(repr(
            (ctx.home, ctx.foreman_home, ctx.project_root, ctx.cwd, cwd, depth, tuple(ctx.scratch), ctx.state_dir, tuple(ctx.state_fallbacks), ctx.confine,
             ctx.unbriefed, kind, _guard_hash())).encode()).hexdigest()[:16]))
    path = _script_cache_path(ctx)
    hit = None if nested or key is None else _cache_load(path).get(key)
    if hit and all(_file_digest(dp) == dd for dp, dd in hit.get("n", [])):  # the scripts it read, unchanged
        if hit.get("u"):
            _UNREAD.append((p, hit["u"]))
        return [tuple(f) for f in hit["f"]]
    found, unread = [], None
    if not nested:
        _TEXTS.clear()
        _DEPS.clear()
    _IN_SCRIPT.append(1)
    old = None
    try:
        text, why, got = _script_text(script, cwd, shebang=kind == "exec", data=data)
        if text is not None:
            _TEXTS.append((p, text))
        if not nested:
            def over(*_):
                raise _OverBudget()
            try:
                old = signal.signal(signal.SIGPROF, over)  # CPU time, not wall: a busy machine mustn't trip it
                signal.setitimer(signal.ITIMER_PROF, _script_budget())
            except ValueError:  # not the main thread: no clock (ponytail: only the main thread is time-boxed)
                old = None
        if why:
            found.append(("system", why))
        elif text is not None and (got or kind) == "py":
            for spawned in _spawned_commands(text):  # only a command written out: computed ones ("$_")
                if '"$_"' not in spawned:  # flag every demo script that builds a path (replay: 27 false denials)
                    found += check_bash(spawned, ctx, depth + 1)
        elif text is not None:
            _check_script(text, ctx, depth, found)
    except _OverBudget:
        if nested:
            raise  # the outermost read owns the clock and decides
        unread = f"read past its {_script_budget():g} s budget; only scanned for literals"
        # never an empty verdict for a script not fully read: the whole text by plain regexes, and the scripts it runs
        # (bash X, source X, ./X: up to 8 files, one level of those too)
        todo, seen = list(_TEXTS), set()
        while todo and len(seen) < 8:
            sp, st = todo.pop(0)
            if sp in seen:
                continue
            seen.add(sp)
            found += [("system", f"{sp} line {n}: {line[:80]} ({why}; the script was too long to parse in time)")
                      for n, line, why in _literal_scan(st, ctx)]
            for target in _run_targets(st)[:8]:  # ponytail: 8 files; a script past that, or named by a variable, is unread
                lex = os.path.normpath(os.path.join(cwd, os.path.expanduser(target)))
                tp, raw = os.path.realpath(lex), None
                if tp not in seen and os.path.isfile(tp):
                    try:
                        with open(tp, "rb") as f:
                            raw = f.read(_SCRIPT_LIMIT + 1)
                    except OSError:
                        pass
                _DEPS.append((lex, hashlib.sha256(raw).hexdigest() if raw is not None else ""))  # absent: stays absent
                if raw is not None and len(raw) <= _SCRIPT_LIMIT:
                    todo.append((tp, raw.decode("utf-8", "replace")))
    finally:
        _IN_SCRIPT.pop()
        if old is not None:
            signal.setitimer(signal.ITIMER_PROF, 0)
            signal.signal(signal.SIGPROF, old)
    if nested:
        return found  # the owner's read decides what is cached
    if unread:
        _UNREAD.append((p, unread))
    if key:
        _cache_store(path, key, {"p": p, "f": found, "u": unread, "at": time.time(),
                                 "n": [[dp, dd] for dp, dd in dict.fromkeys(_DEPS)]})
    return found


def _script_target(name, argv0, args):
    """(kind, path): the script file a command runs: `sh` for source, `.` and a shell's script word, `py` for python,
    `exec` for a path-named command. None where the code comes from -c, a module, stdin or -n (syntax check only), or
    the command isn't one that runs a script file. Options are read as the program reads them: -n counts only
    before the script word, and a value-taking option (-o, -W, -X) takes its value."""
    if name in ("source", "."):
        return ("sh", next((a for a in args if a != "--"), None))
    py = name.startswith("python")
    if not (py or _SH_NAME.match(name)):
        return ("exec", argv0) if "/" in argv0 else (None, None)
    i = 0
    while i < len(args):
        a, i = args[i], i + 1
        if a == "--":
            return (("py" if py else "sh"), args[i] if i < len(args) else None)
        if a == "-" or not a.startswith(("-", "+")):
            return (None, None) if a == "-" else (("py" if py else "sh"), a)
        if a.startswith("--"):
            if a in ("--rcfile", "--init-file", "--check-hash-based-pycs"):
                i += 1
            continue
        for j, ch in enumerate(a[1:], 1):
            if py and ch in "cm" or not py and ch in "cs":
                return (None, None)  # code from -c, a module, or stdin
            if not py and ch == "n" and a[0] == "-":
                return (None, None)  # -n: reads the script for syntax only
            if py and ch in "WXQ" or not py and ch in "oO" and j == len(a) - 1:
                if not (py and j < len(a) - 1):  # -Wonce: the value is attached; -W once: the next word
                    i += 1
                if not py and args[i - 1:i] == ["noexec"]:
                    return (None, None)
                break
    return (None, None)


def _env_channels(argv, name):
    """[(why, code or None)] for variables a command sets that make git (or any program) run a command, or that point
    git at config, templates or programs from elsewhere (None: refused, it can't be read here)."""
    out = []
    for var, val in _assignments(argv):
        if var == "ENV" and not (name == "sh" or name == "bash" and "--posix" in argv):
            continue  # ENV=production make: only an sh (or bash --posix) reads a startup file from it
        if var in _CODE_VARS and val.strip():  # T-0275
            hit = _CODE_VARS[var](val)
            if hit is not False:
                out.append((f"{var}={_clip(val)} loads code into the next program", hit))
        elif var in _GIT_EXEC_ENV and val.strip():
            out.append((f"{var} set to a command", val))
        elif var in _GIT_CONFIG_SOURCES and val not in ("", "/dev/null"):
            out.append((f"{var} points git at config, templates or programs from elsewhere", None))
        elif var in ("HOME", "XDG_CONFIG_HOME") and name == "git":
            out.append((f"git with {var} moved (its config is read from there)", None))
        elif re.fullmatch(r"(?i)GIT_CONFIG_(KEY_\d+|VALUE_\d+|PARAMETERS|COUNT)", var) and any(
                _GIT_EXEC_KEYS.match(k) or k.lower().startswith(("alias.", "include")) or k.lower() == "protocol.ext.allow"
                for k in (x.strip("'\" ").partition("=")[0] for x in re.split(r"'\s+'|\s+", val))):  # review: key=value
            out.append(("git config that runs a command, set through the environment", None))
    return out


def _env_files(argv):
    """Files git writes because of a variable (GIT_TRACE=/path, GIT_INDEX_FILE=/path); 1, 2, true… mean stderr."""
    return [val for var, val in _assignments(argv) if _GIT_FILE_ENV.match(var)
            and not re.fullmatch(r"\d*|true|false|yes|no|on|off", val.lower())]


def _git_config_code(var, value):
    """(why, code or None) for a config key whose value git will run, load or alias; None when it is harmless."""
    key = var.lower()
    if key.startswith("alias."):  # an alias to a git subcommand can't be followed into the commands that use it later
        return (f"git alias {var[6:]}", value[1:]) if value.startswith("!") else (f"a git alias ({var})", None)
    if key.startswith("include") or key in ("core.hookspath", "protocol.ext.allow", "init.templatedir"):
        return (f"git config {var} (config, hooks or transports from elsewhere)", None)
    if _GIT_EXEC_KEYS.match(var) and value.strip():
        return (f"git config {var}", value.lstrip("!"))
    return None


def _git_code(args):
    """[(why, shell code or None)] for the commands a git invocation will run on its own (T-0269/T-0270): `-c` keys
    whose value is a command, a `-c alias.NAME=…` it then calls, `git config` setting such a key, subcommand options
    that take a command (rebase -x, bisect run, submodule foreach, …). None: refused outright, it can't be read here
    (--exec-path, --config-env, --template, config included from a file)."""
    out = []
    i, aliases = 0, {}
    while i < len(args) and args[i].startswith("-"):
        opt, eq, val = args[i].partition("=")
        if opt == "-c" and i + 1 < len(args):
            key, _, value = args[i + 1].partition("=")
            if key.lower().startswith("alias."):
                aliases[key[6:].lower()] = value
            else:
                hit = _git_config_code(key, value)
                out += [hit] if hit else []
        elif opt == "--exec-path" and eq:
            out.append(("git --exec-path=DIR (its subcommands run from there)", None))
        elif opt == "--config-env":
            key = (val if eq else (args[i + 1] if i + 1 < len(args) else "")).partition("=")[0]
            if _GIT_EXEC_KEYS.match(key) or key.lower().startswith(("alias.", "include")):
                out.append((f"git --config-env {key}", None))
        i += 2 if args[i] in _GIT_VALUED else 1
    sub, tail = (args[i].lower() if i < len(args) else ""), args[i + 1:]
    rest = " ".join(shlex.quote(x) for x in tail)
    if sub in aliases:  # the expansion keeps the global options (-C DIR …) the alias ran under
        value, opts = aliases[sub], " ".join(shlex.quote(x) for x in args[:i])
        out.append((f"git alias {sub}", value[1:] + " " + rest if value.startswith("!") else f"git {opts} {value} {rest}"))
    longs = [f for f in _GIT_EXEC_FLAGS.get(sub, ()) if f.startswith("--")]  # git takes --exe for --exec: expand
    tail = [next((f + a[len(a.partition("=")[0]):] for f in longs if len(a.partition("=")[0]) >= 5
                  and f.startswith(a.partition("=")[0])), a) if a.startswith("--") else a for a in tail]
    if sub == "clone":  # clone -c/--config writes the key into the new repo, and git uses it during the clone
        for kv in _opt_values(tail, "-c", "--config"):
            hit = _git_config_code(*kv.partition("=")[::2])
            out += [hit] if hit else []
    for flag in _GIT_EXEC_FLAGS.get(sub, ()):
        if flag in ("-O", "--open-files-in-pager"):  # an optional value: attached only (-Ocmd, --open-files-in-pager=cmd)
            vals = [a[len(flag) + (flag.startswith("--")):] for a in tail
                    if a.startswith(flag + "=" if flag.startswith("--") else flag) and len(a) > len(flag)]
        else:
            vals = _opt_values(tail, flag)
        out += [(f"git {sub} {flag}", v) for v in vals if v.strip()]
    if sub == "bisect" and tail[:1] == ["run"] and tail[1:]:
        out.append(("git bisect run", " ".join(shlex.quote(x) for x in tail[1:])))
    if sub == "submodule" and "foreach" in tail:
        words = [x for x in tail[tail.index("foreach") + 1:] if x not in ("--recursive", "--quiet", "-q")]
        out += [("git submodule foreach", " ".join(words))] if words else []
    if sub in ("init", "clone") and (_opt_values(tail, "--template") or any(a.startswith("--template=") for a in tail)):
        out.append((f"git {sub} --template (hooks from a template folder)", None))
    if sub == "config" and not (_GIT_CONFIG_READS & {a.partition("=")[0] for a in tail}):
        pos, skip = [], False
        for a in tail:  # positionals, without the values of options that take one
            if skip:
                skip = False
            elif a in ("-f", "--file", "--blob", "--type", "--default", "--comment", "--value"):
                skip = True
            elif not a.startswith("-"):
                pos.append(a)
        if pos[:1] == ["set"]:
            pos = pos[1:]
        elif pos[:1] and pos[0] in ("get", "list", "unset", "rename-section", "remove-section", "edit"):
            pos = []
        if len(pos) >= 2:
            hit = _git_config_code(pos[0], pos[1])
            out += [hit] if hit else []
        elif pos[:1] and pos[0].lower().startswith("include"):
            out.append((f"git config {pos[0]}", None))
    return out


def _tree_targets(name, args):
    """Directories a command rewrites as a whole (checkouts, extractions, recursive copies, rsync): whatever they
    contain can change, so classify_tree checks what lies under them."""
    recursive = any(a in ("-r", "-R", "-a", "--recursive", "--archive") or re.fullmatch(r"-[a-zA-Z]*[rRa][a-zA-Z]*", a)
                    for a in args)
    if name in ("git", "tar", "gtar", "bsdtar", "unzip", "cpio", "7z", "7za", "7zz", "rsync") or \
            (name in ("cp", "install") and recursive):
        return _write_targets(name, args)
    return []


def write_targets(cmd):
    """T-0971 review: the paths a Bash command writes, as the guard reads them (redirects and the writers it knows),
    unresolved; [] when it can't be parsed."""
    out = []
    try:
        for x in _split(_tokens(cmd)):
            if x.argv:
                stripped, _ = _strip_wrappers(x.argv)
                out += list(x.redirs) + (_write_targets(os.path.basename(stripped[0]), stripped[1:]) if stripped else [])
    except Exception:
        return []
    return [t for t in out if isinstance(t, str) and t and t != "/dev/null"]


def _checkout_files(base, rest):
    """The files `git checkout` restores when it names only files (after `--`, or every word an existing path and
    no commit), else [] (a branch, -b/-B/--orphan, `.`, a pathspec magic word or a word that is also a commit: the
    whole tree). T-1195."""
    if "--" in rest:
        if any(a.startswith("--p") for a in rest[:rest.index("--")]):  # --pathspec-from-file, or a prefix of it
            return []
        files = rest[rest.index("--") + 1:]
    else:
        if any(a.startswith("-") and a != "-" for a in rest):  # -b, -B, --orphan, --pathspec-from-file, -p ...
            return []
        files = rest
        if not files or any(not os.path.exists(os.path.join(base, a))
                            or _git(base, "rev-parse", "--verify", "-q", f"{a}^{{commit}}") for a in files):
            return []
    # git expands globs in a pathspec (and GIT_GLOB_PATHSPECS / GIT_ICASE_PATHSPECS change how), so a word with a
    # glob character names files the guard can't list
    if any(f.startswith(":") or f.startswith("-") or os.path.normpath(f) == "." or re.search(r"[*?\[\\]", f)
           for f in files):
        return []
    return files


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
        i, where, trees = 0, [], []
        while i < len(args) and args[i].startswith("-"):  # global options before the subcommand
            opt, eq, val = args[i].partition("=")
            if opt in ("-C", "--git-dir", "--work-tree") and not eq:
                val = args[i + 1] if i + 1 < len(args) else ""
            if opt == "-C":
                where.append(val)
            elif opt in ("--git-dir", "--work-tree"):
                trees.append(val)
            i += 2 if args[i] in _GIT_VALUED else 1
        if i < len(args) and args[i] == "clone":
            rest = _positionals(args[i + 1:])
            return ([rest[-1]] if len(rest) >= 2 else ["."]) + _opt_values(args[i + 1:], "--separate-git-dir")
        base, sub, rest = os.path.join(*where) if where else ".", args[i] if i < len(args) else "", args[i + 1:]
        # T-0269 review: --output=FILE writes a file from any diff-family subcommand (diff, log, show, stash show);
        # T-0270: the files and folders other subcommands write
        outs = [a.split("=", 1)[1] for a in rest if a.startswith("--output=")] + \
            [b for a, b in zip(rest, rest[1:]) if a == "--output"] + _opt_values(rest, "--separate-git-dir")
        outs += _git_writes(sub, rest)
        outs = [os.path.join(base, o) for o in outs]
        read_only = sub == "stash" and rest[:1] in (["list"], ["show"])  # T-0265: listing a stash writes nothing
        # T-0935: reset moves HEAD and the index; only --hard/--merge/--keep (or a unique prefix of one, git takes
        # those; or --recurse-submodules) rewrite files
        if sub == "reset" and not any(a.startswith("--") and len(a) > 2 and a != "--" and (
                any(w.startswith(a) for w in ("--hard", "--merge", "--keep", "--recurse-submodules")))
                for a in rest):
            read_only = True
        if not read_only and (sub in _GIT_WORKTREE_WRITES or (  # rewrites its checkout (and repository)
                sub == "fetch" and ({"-u", "--update-head-ok"} & set(rest)))):  # fetch can move HEAD then
            if sub == "checkout" and not trees and not any(  # --icase/--glob-pathspecs change what a word matches
                    a.endswith("pathspecs") and a not in ("--literal-pathspecs", "--noglob-pathspecs")
                    for a in args[:i]) and (files := _checkout_files(base, rest)):
                return [os.path.join(base, f) for f in files] + outs  # T-1195: named files, not the whole tree
            return ([os.path.join(base, t) for t in trees] or [base]) + outs
        return outs
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


def _check_rm(name, args, via_xargs, chain, cwd, ctx, xodd=False):
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
        recursive = any(o in ("-r", "-R") or (not o.startswith("--") and re.search(r"[rR]", o))  # T-0668: getopt takes
                        or (o.startswith("--") and len(o) > 2 and "recursive".startswith(o[2:].split("=")[0]))  # --rec
                        for o in opts)
        out_t = list(targets)
        unknown = False
        if via_xargs:  # T-1123: xargs appends what stdin holds, split on whitespace, to rm's own operands
            up = chain[-1] if chain else None  # only the command feeding xargs directly says what it gets
            uname = _name(up.argv) if up else ""
            rest = _strip_wrappers(up.argv)[0][1:] if up else []
            if xodd or not up:
                unknown = True
            elif uname == "find":
                out_t += _find_paths(rest)
            elif (_strip_wrappers(up.argv)[0][0] == "echo" and all(re.fullmatch(r"[^\s\\*?\[\]{}\"'`$%<>&;|()-][^\s\\*?\[\]{}\"'`$%<>&;|()]*", x) for x in rest)):
                out_t += rest  # plain `echo word…`: no flags, nothing xargs or echo rewrites
            else:
                unknown = True
        elif recursive and not targets:
            unknown = True
        if unknown and (recursive or via_xargs):
            out.append(("rm-outside", f"{'recursive ' if recursive else ''}rm with targets from stdin"))
        if recursive or via_xargs:
            kind = "recursive delete" if recursive else "delete"
            for t in out_t:
                v = _rm_target_violation(t, cwd, ctx, root_ok=not recursive)
                if v:
                    out.append(("rm-outside", f"{kind} of {v}"))
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
        elif args[i] in _GIT_VALUED and i + 1 < len(args):
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


def discards_work(cmd, cwd, depth=0):
    """T-0884: [(folder, what)] for each git command in cmd that throws away uncommitted work, what being "tree" (the
    working files) or "stash drop <ref>" / "stash clear": what the PreToolUse hook saves first. Never a refusal. A cd
    before it, a -C (~ and $VARS expanded), a shell's -c text and `git worktree remove --force <dir>` are followed;
    heredoc bodies are data. ponytail: --git-dir/--work-tree and commands python spawns aren't followed."""
    out = []
    for cm in _split(_tokens(_lines(_strip_heredocs(_join_continued(cmd))))):
        argv, _ = _strip_wrappers(cm.argv)
        name = os.path.basename(argv[0]) if argv else ""
        here = lambda d, base: os.path.normpath(os.path.join(base, os.path.expanduser(os.path.expandvars(d))))
        if name == "cd" and argv[1:2] and argv[1] != "-":
            cwd = here(argv[1], cwd)
        elif re.fullmatch(r"(ba|z|da|k)?sh", name) and depth < 3:
            for text in _shell_c(argv[1:]):
                out += discards_work(text, cwd, depth + 1)
        if name != "git":
            continue
        i, where = 1, cwd
        while i < len(argv) and argv[i].startswith("-"):
            if argv[i] == "-C" and i + 1 < len(argv):
                where = here(argv[i + 1], where)
            i += 2 if argv[i] in _GIT_VALUED or argv[i] == "-C" else 1
        if i >= len(argv):
            continue
        sub, rest = argv[i], argv[i + 1:]
        flags = set(rest)
        short = "".join(a[1:] for a in rest if re.fullmatch(r"-[a-zA-Z]+", a))
        pos = [a for a in rest if not a.startswith("-")]
        if sub == "stash" and pos[:1] in (["drop"], ["clear"]):
            out.append((where, " ".join(["stash"] + pos[:2])))
            continue
        if sub == "worktree" and pos[:1] == ["remove"] and pos[1:] and (flags & {"-f", "--force"} or "f" in short):
            out.append((here(pos[1], where), "tree"))
            continue
        # a word that names a file and no commit is a path (git checkout main beside a main/ folder is the branch)
        paths = [a for a in pos if os.path.exists(os.path.join(where, a))
                 and not _git(where, "rev-parse", "--verify", "-q", f"{a}^{{commit}}")] if sub == "checkout" else []
        staged = "--staged" in flags or "S" in short
        if (sub == "reset" and flags & {"--hard", "--merge"}
                or sub == "checkout" and (flags & {"--force", "--", "."} or "f" in short or paths)
                or sub == "restore" and (not staged or "--worktree" in flags or "W" in short)
                or sub == "clean" and ("--force" in flags or "f" in short)
                and not ("--dry-run" in flags or "n" in short)
                or sub == "switch" and (flags & {"--force", "--discard-changes"} or "f" in short)
                or sub == "rm" and ("--force" in flags or "f" in short)
                or sub in ("merge", "rebase", "cherry-pick", "revert", "am") and "--abort" in flags):
            out.append((where, "tree"))
    return out


_DISK = {"fdisk", "sfdisk", "cfdisk", "parted", "gdisk", "sgdisk", "wipefs", "mkswap"}
_POWER = {"shutdown", "reboot", "poweroff", "halt"}
_SYSTEMCTL_MUTATE = {"start", "stop", "restart", "reload", "try-restart", "reload-or-restart", "enable", "disable",
                     "reenable", "mask", "unmask", "kill", "isolate", "daemon-reload", "daemon-reexec", "set-default",
                     "poweroff", "reboot", "halt", "suspend", "hibernate", "edit", "set-property", "link", "revert",
                     "preset", "reset-failed"}


_FM_VALUED = {"--timeout", "--repeat", "--evidence", "--step", "--ac", "--expect", "--status", "--json-key", "-p",
              "--project", "--tail", "--top", "--text", "--section", "--file", "--run", "--verify", "--check", "--same",
              "--stack-check", "--good", "--why", "--audit", "--lens", "--docs", "--lesson", "--commit", "--type",
              "--tier", "--title", "--source", "--until", "--model", "--max"}
NOTIFY_PROBE = "rm -rf ~"  # what $1 is read as: a notify command that runs its message as code is refused


def _fm_words(rest):
    """T-0901 review: an fm call's positional words, its options (and their values) left out, as argparse reads them."""
    out, i = [], 0
    while i < len(rest):
        a = rest[i]
        if a == "--":
            return out + rest[i + 1:]
        if a.startswith("-") and len(a) > 1:
            i += 2 if a in _FM_VALUED else 1
            continue
        out.append(a)
        i += 1
    return out


def _fm_stored(sub, rest, fm_args):
    r"""T-0901: the commands an fm call stores, or runs from a word the hook would otherwise never read: a verify
    (`--ac "x :: CMD"`, `--verify`, `fm task ac … "x :: CMD"`, an Acceptance criteria text's `verify with \`CMD\``,
    an intake `DONE-WHEN: x :: CMD`), `fm task assume --check`, `--same`, `--stack-check`, `fm check add`/`affected`
    ({tests} and {names} read as one word), `fm smoke set cmd`, `fm notify` ($1 read as NOTIFY_PROBE), and the CMD of
    `fm record` / `fm whyred`. A capture's text runs nothing, so it isn't one."""
    out, words = [], _fm_words(rest)
    section = ""
    for a, b in zip(fm_args, fm_args[1:] + [""]):  # fm refuses abbreviated options, so these are the spellings
        flag, eq, v = a.partition("=") if a.startswith("--") else (a, "", "")
        v = v if eq else b
        if flag in ("--verify", "--same", "--stack-check") or (flag == "--check" and words[:1] == ["assume"]):
            out.append(v)
        elif flag == "--ac" and " :: " in v:
            out.append(v.rpartition(" :: ")[2])
        elif flag == "--section":
            section = v
        elif flag == "--text" and words[:1] == ["set"] and section.lower().startswith("acceptance"):
            out += re.findall(r"verify with `([^`]+)`", v)
    if sub == "task" and words[:1] == ["ac"]:
        out += [w.rpartition(" :: ")[2] for w in words if " :: " in w]
    if sub == "intake":
        out += [ln.rpartition(" :: ")[2] for w in words for ln in w.splitlines()
                if " :: " in ln and re.match(r"\s*(DONE-WHEN|ACCEPT)\s*:", ln, re.I)]
    if sub == "check" and words[:1] in (["add"], ["affected"]) and words[1:]:
        out.append(re.sub(r"\{(tests|names)\}", "tests", " ".join(words[1:])))
    if sub == "smoke" and words[:2] == ["set", "cmd"] and words[2:]:
        out.append(" ".join(words[2:]))
    if sub == "notify" and words:
        out.append(re.sub(r"\$\{?1\}?", NOTIFY_PROBE, " ".join(words)))
    if sub in ("record", "whyred") and words:
        out.append(words[0])
    return [x for x in dict.fromkeys(out) if x.strip()]


def _fm_trailing(rest, positionals):
    """T-0898: the command words after `fm quiet` / `fm at TARGET` options (argparse's REMAINDER, or after --)."""
    i, seen = 0, 0
    while i < len(rest):
        a = rest[i]
        if a == "--":
            return rest[i + 1:]
        if a in ("--tail", "--timeout", "-p", "--project"):
            i += 2
        elif a.startswith("-"):
            i += 1
        elif seen < positionals:
            seen, i = seen + 1, i + 1
        else:
            return rest[i:]
    return []


def _fm_subcommand(args, takes_value=("-p", "--project")):
    """(first word that isn't an option, what follows it); `takes_value` options consume the next word."""
    i = 0
    while i < len(args) and args[i].startswith("-"):
        i += 2 if args[i] in takes_value else 1
    return (args[i], args[i + 1:]) if i < len(args) else (None, [])


_CLAUDE_CHANGES = {"plugin": {"install", "i", "enable", "disable", "uninstall", "remove", "update"},
                   "mcp": {"add", "add-json", "add-from-claude-desktop", "remove"}, "config": {"set", "add", "remove"}}


_SESSION_CONFIG = ("--settings", "--mcp-config", "--plugin-dir")
_UPDATE = "claude plugin update changes Claude Code's plugins, MCP servers or config"  # the details check() pairs
_MARKET_UPDATE = "claude plugin marketplace update"


def _check_claude_config(name, args, stdin=""):
    """Installing or toggling plugins, marketplaces and MCP servers, or changing Claude Code's config: new code and
    always-on context in every session, so only the user's yes to `fm ask ID plugin` allows it. A session started
    with its own settings, MCP servers or plugins counts too (its settings can switch Foreman's hooks off)."""
    if not re.fullmatch(r"claude(?:-code)?(?:@[\w.-]+)?", name):  # also npx @anthropic-ai/claude-code[@version]
        return []
    # a prompt's slash command isn't a tool call the guard sees; `stdin` is the raw command text when claude reads a
    # pipe or heredoc (echo … | claude -p, claude -p <<EOF)
    if _SLASH_CHANGE.search(stdin) or any(_SLASH_CHANGE.search(a) for a in args):
        return [("plugin", "a /plugin, /mcp or /config change sent to claude as a prompt" + plugin_mark("?"))]
    flags = [a.split("=", 1)[0] for a in args if a.split("=", 1)[0] in _SESSION_CONFIG]
    if flags:
        return [("plugin", f"claude {flags[0]} starts a session with its own settings, MCP servers or plugins")]
    # every adjacent pair, not just the first two words: global options and their values can come first
    pos = ["plugin" if a == "plugins" else a for a in args if not a.startswith("-")]
    for a, b, c3 in zip(pos, pos[1:], pos[2:] + [""]):
        if (a, b) == ("plugin", "marketplace") and c3 in ("add", "remove", "rm", "update"):
            return [("plugin", f"claude plugin marketplace {c3}")]
        if b in _CLAUDE_CHANGES.get(a, ()):
            target = plugin_mark(_claude_plugin_target(args)) if a == "plugin" and b in _PLUGIN_ADDS else ""
            return [("plugin", f"claude {a} {b} changes Claude Code's plugins, MCP servers or config{target}")]
    return []


_PLUGIN_ADDS = ("install", "i", "enable")  # the plugin changes that bring code in: a yes for them is pinned (T-0036)
PLUGIN_ID = re.compile(r"[\w.-]+(?:@[\w.-]+)?")  # name or name@marketplace; fm ask --pin takes the same


def plugin_mark(target):
    """The end of a plugin finding's detail naming the plugin it installs or enables ("?" when it can't tell); the
    hook reads it back with plugin_target, the only other place that knows this format."""
    return f" [plugin {target}]"


def plugin_target(detail):
    m = re.search(r" \[plugin (\S+)\]$", str(detail))
    return m.group(1) if m else None


def _one_plugin(words):
    """The plugin id when words name exactly one, else "?": no yes is spent on a change it can't check (T-0036)."""
    return words[0] if len(words) == 1 and PLUGIN_ID.fullmatch(words[0]) else "?"


def _claude_plugin_target(args):
    """The plugin a `claude plugin install|i|enable …` names (the value of -s/--scope isn't one), or "?"."""
    for i, (x, y) in enumerate(zip(args, args[1:])):
        if x in ("plugin", "plugins") and y in _PLUGIN_ADDS:
            words, skip = [], False
            for a in args[i + 2:]:
                if skip or a in ("-s", "--scope"):
                    skip = not skip
                    continue
                if not a.startswith("-"):
                    words.append(a)
            return _one_plugin(words)
    return "?"


_USER_UNIT_PERSIST = {"link", "enable", "reenable", "edit", "preset", "revert", "set-property", "add-wants",
                      "add-requires"}


def _check_system(name, args):
    pos = _positionals(args)
    # scheduled or hook code that runs later, outside the session (like a user systemd unit)
    if name == "crontab" and not set(args) & {"-l", "--list"}:
        return [("system", "crontab change (code that runs on a schedule)")]
    if name in ("at", "batch"):
        return [("system", f"{name} schedules a command to run later")]
    if name == "direnv" and pos[:1] in (["allow"], ["permit"], ["grant"]):
        return [("system", "direnv allow (.envrc runs on every cd into the folder)")]
    if name == "git":
        # hooks from another folder, set for one command (-c, --config-env) or persistently (git config)
        if any(re.match(r"(?i)(--config-env=|-c)?core\.hookspath=", a) for a in args):
            return [("system", "git with core.hooksPath (hooks from another folder)")]
        sub, rest = _fm_subcommand(args, takes_value=("-C", "-c"))
        values = [a for a in rest if not a.startswith("-")]
        if sub == "config" and [v.lower() for v in values[:1]] == ["core.hookspath"] and len(values) > 1 \
                and not set(rest) & {"--get", "--get-all", "--list", "-l", "--unset", "--unset-all"}:
            return [("system", "git core.hooksPath (hooks that run on every git command)")]
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
    if name == "systemctl" and "--user" in args and pos and pos[0] in _USER_UNIT_PERSIST:
        return [("system", f"systemctl --user {pos[0]} (a user unit outlives the session)")]
    if name == "systemd-run":
        return [("system", "systemd-run (a transient unit outside the session)")]
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
_LIT_ASSIGN = re.compile(r"(?<![\w$])([A-Za-z_]\w*)=(?:'([^']*)'|\"([^\"$`\\]*)\"|([^\s;&|()<>'\"$`\\]*))(?=[\s;&|)]|$)")


def _line_literals(shell):
    """T-0587: NAME → value for a name set once on the line to a literal (spaces kept: q='rm -rf') and named nowhere
    else but in $q / ${q}, so no loop, read, declare or second assignment can have changed it."""
    out = {}
    for m in _LIT_ASSIGN.finditer(_mask_quotes(shell)):  # an assignment, not quoted text that looks like one
        k = next(k for k in (2, 3, 4) if m.group(k) is not None)
        name, val = m.group(1), shell[m.start(k):m.end(k)]
        rest = shell[:m.start()] + shell[m.end():]
        if not re.search(rf"(?<![\w$]){name}(?!\w)|\$\{{[#!]?{name}[^}}]", re.sub(rf"\$(?:\{{{name}\}}|{name}(?!\w))", "", rest)):
            out[name] = val
    return out


# T-0587: what a command name bash computes from an unknown value ($X, `which x`) is checked as: those whose check
# reads the arguments (ponytail: crontab, at, nft, ufw, disk and power tools refuse nearly any arguments, so they'd
# refuse every computed name; a bare `$X` that is shutdown stays unread)
_COMPUTED_AS = ["rm", "git", "claude", "dd", "systemctl", "cryptsetup", "direnv", "init"] + sorted(_PUBLISH)
_RM_LONG = ("force", "interactive", "one-file-system", "no-preserve-root", "preserve-root", "recursive", "dir", "verbose",
            "help", "version")


def _readings(text, vals):
    """T-0587 (its review): text eval or sh -c runs, as written (an unknown $q: empty, conditional, a subshell's) and,
    when it differs, with the literal values this line set: both are read, so a value adds findings, never hides one"""
    out = [text]
    for t in (_with_vars(text, vals), re.sub(r"\\([$`])", r"\1", text)):  # T-0669: and with \$ and \` unescaped, as
        if t not in out:                                                 # double quotes unescape them
            out.append(t)
    return out


def _rm_opts_only(args):
    """T-0587: no option rm would refuse (one makes it exit before deleting). T-0668 (its review): getopt takes any
    prefix of a long option (--rec), and under POSIXLY_CORRECT options end at the first operand, so only the options
    before it count; any doubt reads as rm."""
    for a in args:
        if a == "--" or not a.startswith("-") or a == "-":
            return True
        if a.startswith("--"):
            if not any(o.startswith(a[2:].split("=")[0]) for o in _RM_LONG):
                return False
        elif not re.fullmatch(r"-[fiIrRdv]+", a):
            return False
    return True


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
