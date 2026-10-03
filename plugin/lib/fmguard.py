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

CATEGORIES = ["self-authorize", "state-direct", "core", "remote", "plugin", "credentials", "system", "rm-outside",
              "git-destructive", "pipe-shell", "publish"]
NOT_AUTHORIZABLE = {"state-direct", "self-authorize"}
USER_ONLY = {"core", "remote", "plugin"}  # granted only by the user's reply to `fm ask`, never by `fm task set --allow`
FILE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
DEFAULT_BRANCHES = {"main", "master", "trunk"}


# Plain classes, no imports from the rest of Foreman: the guard must load (and fall back to its committed copy) even
# when the rest of the library is broken, and dataclasses would cost every hook ~9 ms of import.
class Ctx:
    def __init__(self, cwd, project_root, home, foreman_home, scratch=(), allow=(), task_id=None, state_dir=None,
                 state_fallbacks=(), standing=(), trusted=False):
        self.cwd, self.project_root, self.home, self.foreman_home = cwd, project_root, home, foreman_home
        self.scratch, self.allow, self.task_id = list(scratch), set(allow), task_id
        self.state_dir = state_dir  # when Foreman state lives outside foreman_home (read-only home fallback)
        self.state_fallbacks = list(state_fallbacks)  # where a fallback could live: state even before it's used
        self.standing = set(standing)  # T-0119: the project's standing yeses (core only)
        self.trusted = bool(trusted)  # T-0120: /fm-trust on: the guard file and Claude Code settings too


class Block:
    def __init__(self, category, detail):
        self.category, self.detail = category, detail

    def __repr__(self):
        return f"Block({self.category!r}, {self.detail!r})"


def findings(tool_name, tool_input, ctx):
    """Every (category, detail) a tool call touches, allowed or not."""
    if tool_name in FILE_TOOLS:
        raw = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
        path = _resolve(_expand(raw, ctx), ctx.cwd)
        return [(cat, path) for cat in classify_write(path, ctx)]
    if tool_name == "Bash":
        return check_bash(tool_input["command"], ctx)
    return []


def check(tool_name, tool_input, ctx, found=None):
    found = findings(tool_name, tool_input, ctx) if found is None else found
    for cat in CATEGORIES:
        for got, detail in found:
            if got == cat and (got in NOT_AUTHORIZABLE or got not in ctx.allow):
                if got == "core" and ("core" in ctx.standing and _standing_covers(detail, ctx)
                                      or ctx.trusted and _trust_covers(detail, ctx)):
                    continue
                return Block(got, detail)
    if sum(1 for got, _ in found if got == "plugin") > 1:  # a plugin yes is used up by one change (fmhooks)
        return Block("plugin", "more than one plugin change in one command; one yes covers one change: run each as "
                               "its own command, after its own fm ask")
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
                + _ASK.format(id=tid, cat="<" + "|".join(sorted(USER_ONLY)) + ">") + ".")
    if cat == "state-direct":
        return (f"Foreman guard: blocked state-direct: {detail} is Foreman state. Change it through fm "
                f"(fm task …, fm capture, fm checkpoint); direct writes are never authorized.")
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


def _standing_covers(path, ctx):
    """A standing core yes (T-0119) covers Foreman's own code, rules, evals and spec; never this guard file, Claude
    Code's settings or Foreman state, which still ask each time."""
    fh = ctx.foreman_home
    if not isinstance(path, str) or not path.startswith("/") or _under(os.path.join(fh, "plugin", "lib", "fmguard.py"), path):
        return False  # not a path, the guard itself, or a whole-tree write that includes it
    return path in {os.path.join(fh, f) for f in ("plugin/rules/foreman.md", "BUILD_PROMPT.md")} or any(
        _strictly_under(path, os.path.join(fh, "plugin", d)) for d in ("lib", "bin", "hooks", "evals"))


def _trust_covers(path, ctx):
    """/fm-trust on (T-0120) covers every core file, the guard and Claude Code settings included; never Foreman state
    (only fm writes it) or a whole-tree write."""
    if not isinstance(path, str) or not path.startswith("/") or " (a tree write" in path:
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
            or "/.git/hooks/" in p)


def _protected_roots(ctx):
    """(path, category) of everything the guard protects, for writes that cover a whole tree."""
    fh, cl = ctx.foreman_home, os.path.join(ctx.home, ".claude")
    roots = [(os.path.join(fh, "plugin", d), "core") for d in ("lib", "bin", "hooks", "evals")]
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


def classify_write(path, ctx):
    cats = []
    for p in _variants(path):
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
    return list(dict.fromkeys(cats))


# ---------------------------------------------------------------- shell parsing

class Cmd:
    def __init__(self, argv, redirs, piped, procsub=False):
        self.argv, self.redirs, self.piped, self.procsub = argv, redirs, piped, procsub


_HEREDOC_START = r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1"


def _lines(text):
    """Newlines as command separators for the tokenizer, placed after each line so a # comment ends at its line (it ran
    to the end of the whole command, hiding every later line: T-0158)."""
    return text.replace("\n", "\n;")


def _live_heredocs(cmd):
    """The bodies of heredocs with an unquoted delimiter: a shell runs their substitutions (T-0158)."""
    lines, out, i = cmd.split("\n"), [], 0
    while i < len(lines):
        line = lines[i]
        i += 1
        for quote, delim in re.findall(_HEREDOC_START, line):
            body = []
            while i < len(lines) and lines[i].strip() != delim:
                body.append(lines[i])
                i += 1
            i += 1
            if not quote:
                out.append("\n".join(body))
    return out


def _heredocs(cmd):
    """(the command without its heredoc bodies, the bodies)"""
    lines, out, bodies, i = cmd.split("\n"), [], [], 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        i += 1
        for _, delim in re.findall(_HEREDOC_START, line):
            while i < len(lines) and lines[i].strip() != delim:
                bodies.append(lines[i])
                i += 1
            i += 1
    return "\n".join(out), "\n".join(bodies)


def _strip_heredocs(cmd):
    return _heredocs(cmd)[0]


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


_KEYWORDS = {"do", "then", "else", "elif", "if", "while", "until", "{", "!", "coproc"}  # words before a command


def _strip_wrappers(argv):
    """Drop env assignments and exec wrappers (sudo, env, timeout, xargs, npx…). Returns (argv, via_xargs)."""
    i = 0
    while i < len(argv):
        a = argv[i]
        base = os.path.basename(a)
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", a) or a in _KEYWORDS:  # T-0159: `do rm …` is rm, not a command `do`
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
_DOWNLOAD_SUBST = re.compile(r"(\$\(|`)\s*(curl|wget|fetch)\b")


_INTERP_NAMES = r"(?:python|perl|ruby|php)[0-9.]*|py|jruby|truffleruby|irb|node|nodejs|deno|bun"
_INTERP = re.compile(rf"(?:^|[\s;&|(/`])({_INTERP_NAMES})(?=\s|$|[;&|)`])")
_TEXT_TICKS = re.compile(r"(?:python[0-9.]*|py|node|nodejs|deno|bun)$")  # a backtick is only text in these
_WRITE_API = re.compile(
    r"""open\s*\([^)]*['"][rwxab+]*[wxa+][rwxab+]*['"]|\.write_(?:text|bytes)\s*\(|(?:write|append)FileSync|"""
    r"createWriteStream|\bos\.(?:replace|rename|remove|unlink)\b|\bshutil\.\w+\(|\.(?:unlink|rename|replace|touch)\(|"
    r"File\.write|file_put_contents|open\s*\(\s*(?:my\s+)?\$?\w+\s*,\s*['\"]?[>+]")
_QUOTED = re.compile(r"""(['"])((?:[~/.]|[\w.-]+/)[^'"\s]*)\1""")
_GUARDED_BY_PATH = ("core", "state-direct", "credentials", "plugin")
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
                          r"checkpoint|mutate|cmd_\w+|task_\w+|_resolve_approvals|_activate_fallback|"
                          r"restore_default_state)\s*\(|"
                          rf"\bgetattr\s*\(\s*{_FM_ENTRY}\b|"
                          rf"\b{_FM_ENTRY}\s*\.\s*\w+\s*\(|\bfrom\s+{_FM_ENTRY}\s+import\b|\bimport\s+{_FM_ENTRY}\s+as\b|"
                          rf"(?:__import__|import_module)\s*\(\s*['\"]{_FM_ENTRY}")


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
    return q is None and not esc


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


def _interpreter_writes(cmd, ctx):
    """Interpreter code (heredoc, -c, -e) that writes files: every quoted path it names counts as a write target.

    Coarse on purpose: a script that names a protected path and writes anything is treated as writing it. Code that
    imports Foreman's modules and calls their writers bypasses fm (the only state writer): that needs core, i.e. the
    user's yes, rather than never-authorizable state-direct, because the text match can't tell code from test data."""
    if not _INTERP.search(_mask_fm(cmd, ctx)):
        return []
    if _FM_INTERNALS.search(cmd) and _FM_MUTATORS.search(cmd):
        return [("core", "interpreter code driving Foreman's modules (use the fm CLI)")]
    code = _interp_code(cmd)
    # T-0150/T-0155: a backtick runs code unless every interpreter here treats it as text (markdown in a Python heredoc)
    ticks = "`" in code and any(not _TEXT_TICKS.match(m.group(1)) for m in _INTERP.finditer(cmd))
    if _CLAUDE_IN_CODE.search(code) and (_EXEC_API.search(code) or ticks):
        return [("plugin", "interpreter code running claude's plugin, MCP or config commands" + plugin_mark("?"))]
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
    for c in _split(_tokens(_lines(_strip_heredocs(cmd)))):
        argv, _ = _strip_wrappers(c.argv)
        name, args = (os.path.basename(argv[0]) if argv else ""), argv[1:]
        if name == "fm":
            calls.append(args)
        elif re.match(r"^python[0-9.]*$", name) and args[:1] and args[0].endswith("/fm"):
            calls.append(args[1:])
    return calls


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
_ASSIGNISH = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)(?:\[[^\]]*\])?\+?=")  # NAME=, NAME+= and NAME[i]=
# bash sets these itself, ignores an assignment to them or makes it fail (readonly)
_SHELL_SET = re.compile(r"^(?:_|PWD|OLDPWD|DIRSTACK|BASH\w*|RANDOM|SRANDOM|SECONDS|LINENO|EPOCH\w+|HISTCMD|PPID|E?UID|"
                        r"GROUPS|FUNCNAME|PIPESTATUS|OPT\w+|REPLY|MAPFILE|COPROC\w*|SHELLOPTS|SHLVL|HOST\w+|MACHTYPE|"
                        r"OSTYPE|COMP_\w+|READLINE_\w+|COLUMNS|LINES)$")


def _straight_line(shell):
    return not _BRANCHY.search(re.sub(r"\$\{\w+\}|\d*>&\d*-?|&>>?", " ", shell))  # ${VAR}, 2>&1 and &> aren't branches


def _with_vars(tok, env):
    return re.sub(r"\$(?:\{(\w+)\}|(\w+))", lambda m: env.get(m.group(1) or m.group(2), m.group(0)), tok)


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
        elif ch in " \t\n;":
            words, cur = (words + [cur]) if cur else words, ""
            if ch != " " and ch != "\t" and words:
                cmds, words = cmds + [words], []
            i += 1
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


def _track_vars(words, env):
    """T-0161: the variables after one simple command (its words as written), or None once any could be unknown."""
    words = [w for i, w in enumerate(words) if not re.match(r"\d*(?:[<>]|&>)", w)  # redirections and their targets
             and not (i and re.fullmatch(r"\d*(?:[<>]+&?|&>>?)", words[i - 1]))]
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
            k, v = _ASSIGN.match(w).group(1), _unquote(w.partition("=")[2])
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
    if re.search(r"[$`*?\[]", word):
        return None  # T-0162: a name bash computes ($X, `…`, a glob) can turn out to be a builtin
    name = _unquote(word) or ""
    return None if name in _BUILTINS and name not in _INERT else env


def check_bash(cmd, ctx, depth=0, tails=True):
    """Return [(category, detail)] for every dangerous thing found in a shell command."""
    if depth > 4:
        return [("rm-outside", "command nesting too deep to analyse")]
    found = _interpreter_writes(cmd, ctx)  # every depth: an fm --run command is read on its own (T-0128 review)
    shell = _strip_heredocs(cmd)
    # T-0158: every `…` and $( … ) a shell runs (unquoted heredoc bodies included), read as a command of its own
    # a tail (the text after a substitution opens) is read once as it stands: its own tails are suffixes of it already
    for body in _subst_bodies(shell, tails) + [b for t in _live_heredocs(cmd) for b in _subst_bodies(t, tails)]:
        found += check_bash(body, ctx, depth + 1, tails=False)
    cmds = _split(_tokens(_lines(shell)))
    cwd, chain = ctx.cwd, []
    raw = _raw_cmds(shell) if _straight_line(shell) else None  # the same commands, quotes kept (T-0161)
    env = {} if raw is not None and len(raw) == len(cmds) else None  # VAR → literal, for rm targets (T-0151)
    for idx, c in enumerate(cmds):
        if env is not None:
            env = _track_vars(raw[idx], env)
        argv, via_xargs = _strip_wrappers(c.argv)
        if not c.piped:
            chain = []
        name = os.path.basename(argv[0]) if argv else ""
        args = argv[1:]
        if name in ("cd", "pushd"):
            tgt = args[0] if args else ctx.home
            if not _unresolvable(tgt):
                cwd = _resolve(_expand(tgt, ctx), cwd)
        if _SHELLS.match(name) and "-c" in args and args.index("-c") + 1 < len(args):
            inner = args[args.index("-c") + 1]
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
            found += check_bash(joined, ctx, depth + 1)
            if _DOWNLOAD_SUBST.search(joined):
                found.append(("pipe-shell", "eval of a downloaded script"))
        if _SHELLS.match(name) or name in ("source", "."):
            if c.piped and any(_name(x.argv) in _FETCHERS for x in chain):
                found.append(("pipe-shell", f"downloaded content piped into {name}"))
            nxt = cmds[idx + 1] if idx + 1 < len(cmds) else None
            if c.procsub and nxt and _name(nxt.argv) in _FETCHERS:
                found.append(("pipe-shell", f"{name} <(download)"))
        git_env = [a.split("=", 1)[1] for a in c.argv if name == "git" and a.startswith(("GIT_DIR=", "GIT_WORK_TREE="))]
        if name == "git" and any(re.match(r"(?i)GIT_CONFIG_(KEY_\d+|PARAMETERS)=.*core\.hookspath", a) for a in c.argv):
            found.append(("system", "git with core.hooksPath set through the environment"))
        for target in c.redirs + _write_targets(name, args) + git_env:
            if not _unresolvable(target):
                found += [(cat, target) for cat in classify_write(_resolve(_expand(target, ctx), cwd), ctx)]
        for target in _tree_targets(name, args) + git_env:
            if not _unresolvable(target):
                found += [(cat, f"{target} (a tree write over it)")
                          for cat in classify_tree(_resolve(_expand(target, ctx), cwd), ctx)]
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
            if sub == "check" and rest[:1] == ["add"]:
                found += check_bash(" ".join(rest[1:]), ctx, depth + 1)
            if sub == "plugins" and rest[:1] and rest[0] in ("install", "enable", "disable", "add-marketplace"):
                target = plugin_mark(_one_plugin([a for a in rest[1:] if not a.startswith('-')])) \
                    if rest[0] in ("install", "enable") else ""
                found.append(("plugin", f"fm plugins {rest[0]} changes Claude Code's plugins{target}"))
            if sub == "serve" and _fm_subcommand(rest, takes_value=("--permission-mode",))[0] not in ("status", "stop"):
                found.append(("remote", "fm serve starts a persistent Remote Control session reachable from the "
                                        "user's claude.ai account"))
        found += _check_rm(name, [_with_vars(a, env) for a in args] if env else args, via_xargs, chain, cwd, ctx)
        found += _check_git(name, args, cwd, ctx)
        found += _check_system(name, args)
        found += _check_claude_config(name, args, cmd if c.piped or "<<" in cmd else "")
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


_GIT_WORKTREE_WRITES = {"pull", "checkout", "switch", "reset", "merge", "rebase", "restore", "stash", "apply",
                        "am", "cherry-pick", "revert", "clean", "rm", "mv"}


def _tree_targets(name, args):
    """Directories a command rewrites as a whole (checkouts, extractions, recursive copies, rsync): whatever they
    contain can change, so classify_tree checks what lies under them."""
    recursive = any(a in ("-r", "-R", "-a", "--recursive", "--archive") or re.fullmatch(r"-[a-zA-Z]*[rRa][a-zA-Z]*", a)
                    for a in args)
    if name in ("git", "tar", "gtar", "bsdtar", "unzip", "cpio", "7z", "7za", "7zz", "rsync") or \
            (name in ("cp", "install") and recursive):
        return _write_targets(name, args)
    return []


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
            i += 2 if args[i] in ("-C", "-c", "--git-dir", "--work-tree") else 1
        if i < len(args) and args[i] == "clone":
            rest = _positionals(args[i + 1:])
            return [rest[-1]] if len(rest) >= 2 else ["."]
        if i < len(args) and (args[i] in _GIT_WORKTREE_WRITES or (  # rewrites its checkout (and repository)
                args[i] == "fetch" and ({"-u", "--update-head-ok"} & set(args[i + 1:])))):  # fetch can move HEAD then
            base = os.path.join(*where) if where else "."
            return [os.path.join(base, t) for t in trees] or [base]
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


def _fm_subcommand(args, takes_value=("-p", "--project")):
    """(first word that isn't an option, what follows it); `takes_value` options consume the next word."""
    i = 0
    while i < len(args) and args[i].startswith("-"):
        i += 2 if args[i] in takes_value else 1
    return (args[i], args[i + 1:]) if i < len(args) else (None, [])


_CLAUDE_CHANGES = {"plugin": {"install", "i", "enable", "disable", "uninstall", "remove", "update"},
                   "mcp": {"add", "add-json", "add-from-claude-desktop", "remove"}, "config": {"set", "add", "remove"}}


_SESSION_CONFIG = ("--settings", "--mcp-config", "--plugin-dir")


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
