"""fm codemod (T-1554): mechanical rewrites across a repository's tracked text files, previewed as a diff before any
file is written.

    fm codemod rename OLD NEW [PATH…] [--apply]     OLD as a whole word (identifier boundaries) becomes NEW
    fm codemod sub PATTERN REPL [PATH…] [--apply]   a Python regular expression, REPL with \\1 groups

Only files git tracks under the paths (default: the whole repo) are read, text files of at most MAX_BYTES; without
--apply nothing is written, and with it each changed file is replaced whole (fmcore.write_atomic). The deprecation
playbook (clean/deprecation.md) says when a rename is safe to run this way. Stdlib only."""
import difflib
import os
import re

import fmcore as c

MAX_BYTES = 1 << 20  # a source file, not a data dump
SHOWN = 40  # diff lines of each file in the preview


def files(root, paths=()):
    """The tracked text files under paths (relative to root), at most MAX_BYTES each, in git's order."""
    out = []
    for rel in c._git(root, "ls-files", "-z", "--", *(paths or ["."]), timeout=30).split("\0"):
        path = os.path.join(root, rel)
        if not rel or os.path.islink(path) or not os.path.isfile(path) or os.path.getsize(path) > MAX_BYTES:
            continue
        with open(path, "rb") as f:
            head = f.read(8192)
        if b"\0" not in head:
            out.append(rel)
    return out


def rewrite(root, pattern, repl, paths=()):
    """[(rel, old text, new text, replacements)] for each file the rewrite changes."""
    rx = re.compile(pattern)
    out = []
    for rel in files(root, paths):
        try:
            with open(os.path.join(root, rel), encoding="utf-8") as f:
                text = f.read()
        except UnicodeDecodeError:  # not UTF-8 text: left alone, never rewritten with a guessed encoding
            continue
        new, n = rx.subn(repl, text)
        if n and new != text:
            out.append((rel, text, new, n))
    return out


def preview(changes):
    """A unified diff of each change, cut at SHOWN lines a file."""
    lines = []
    for rel, old, new, _ in changes:
        diff = list(difflib.unified_diff(old.splitlines(), new.splitlines(), f"a/{rel}", f"b/{rel}", lineterm="", n=1))
        lines += diff[:SHOWN] + ([f"… {len(diff) - SHOWN} more diff lines in {rel}"] if len(diff) > SHOWN else [])
    return "\n".join(lines)


def cmd_codemod(args):
    import fmcli
    words = list(args.words or [])
    if len(words) < 3 or words[0] not in ("rename", "sub"):
        raise fmcli.UsageError("fm codemod rename OLD NEW [PATH…] [--apply] · fm codemod sub PATTERN REPL [PATH…] "
                               "[--apply]: a preview first; --apply writes it")
    kind, a, b, paths = words[0], words[1], words[2], words[3:]
    root = c.git_root(os.getcwd())
    if not root:
        raise fmcli.UsageError("fm codemod rewrites a git repository's tracked files: run it inside one")
    if kind == "rename":
        if not re.fullmatch(r"[A-Za-z_]\w*", a) or not re.fullmatch(r"[A-Za-z_]\w*", b):
            raise fmcli.UsageError("rename takes two identifiers (letters, digits, _); fm codemod sub for anything else")
        pattern, repl = rf"(?<![\w]){a}(?![\w])", b
    else:
        pattern, repl = a, b
    try:
        changes = rewrite(root, pattern, repl, [os.path.relpath(os.path.abspath(x), root) for x in paths])
    except re.error as e:
        raise fmcli.UsageError(f"fm codemod sub: {pattern!r} isn't a regular expression: {e}")
    total = sum(n for *_, n in changes)
    if getattr(args, "apply", False):
        for rel, _, new, _ in changes:
            c.write_atomic(os.path.join(root, rel), new)
    summary = (f"{total} replacement(s) in {len(changes)} file(s)" + (": written" if getattr(args, "apply", False)
                                                                       else ": nothing written; --apply writes them"))
    fmcli.out(args, {"files": [{"path": r, "replacements": n} for r, _, _, n in changes], "replacements": total,
                     "applied": bool(getattr(args, "apply", False))},
              (preview(changes) + "\n" if changes and not getattr(args, "apply", False) else "") + summary)
    return 0
