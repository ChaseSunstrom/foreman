"""fm docs: markdown that drifted from the repo — paths that don't exist, npm/make commands that aren't defined.

Report-only. Reuses tidy's detectors; paths may be relative to the file or to the repo root, gitignored
(machine-specific) paths and fenced code blocks are skipped.
"""
import os
import re
import stat
import subprocess

from fmtidy import dead_paths, stale_commands

SKIP_DIRS = {"node_modules", "vendor", "dist", "build", "target", "venv", "__pycache__"}
_FENCE = re.compile(r"```.*?```", re.S)
# T-1817: paths in other trees: a stack card's are the detected project's (./gradlew), a changelog's files as they were
_FRONT = re.compile(r"---\n(.*?)\n---\n", re.S)
_HISTORY = re.compile(r"(?i)(changelog|changes|history|news)(\.\w+)?\.md")


def _markdown(root):
    """The repo's markdown: tracked, or untracked and not ignored (ignored notes, like Foreman's state/, are
    point-in-time records, not docs). Outside git, every .md not in a skipped or hidden folder."""
    try:
        r = subprocess.run(["git", "-C", root, "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--",
                            "*.md"], capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        r = None
    if r and r.returncode == 0:
        rels = sorted({f for f in r.stdout.split("\0") if f})
        yield from (os.path.join(root, f) for f in rels
                    if not any(part in SKIP_DIRS or part.startswith(".") for part in f.split("/")[:-1])
                    and _regular(os.path.join(root, f)))
        return
    for d, dirs, files in os.walk(root):
        dirs[:] = sorted(x for x in dirs if x not in SKIP_DIRS and not x.startswith("."))
        yield from (os.path.join(d, f) for f in sorted(files) if f.endswith(".md") and _regular(os.path.join(d, f)))


def _regular(path):
    """A regular file, not a link: a link may point at /dev/zero, a FIFO or a file outside the tree (fm find)."""
    try:
        return stat.S_ISREG(os.lstat(path).st_mode)
    except OSError:
        return False


def _ignored(root, rels):
    if not rels:
        return set()
    try:
        p = subprocess.run(["git", "-C", root, "check-ignore", "--stdin"], input="\n".join(rels), capture_output=True,
                           text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return set()
    return set(p.stdout.splitlines())


def _top_level(root):
    """Top-level names that hold repo content (tracked, or untracked and not ignored); every name outside git. A
    folder with only ignored files (Claude Code's .claude/scheduled_tasks.lock) doesn't make `.claude/…` a repo path."""
    try:
        r = subprocess.run(["git", "-C", root, "ls-files", "--cached", "--others", "--exclude-standard"],
                           capture_output=True, text=True, timeout=30)
        if r.returncode == 0:
            return {line.split("/", 1)[0] for line in r.stdout.splitlines() if line}
    except (OSError, subprocess.SubprocessError):
        pass
    try:
        return set(os.listdir(root))
    except OSError:
        return set()


def _anchored(tok, root, here, tops):
    """Only paths that clearly point into this repo: ./ or ../, or a first component that is repo content at the root
    or exists next to the file. Bare names, other repos (org/repo), branches and domains are too ambiguous."""
    if tok.startswith(("./", "../")):
        return True
    first = tok.split("/", 1)[0]
    return "/" in tok and bool(first) and (first in tops or (here != root and os.path.exists(os.path.join(here, first))))


def scan(root):
    findings, tops = [], _top_level(root)
    for md in _markdown(root):
        try:
            with open(md, encoding="utf-8", errors="replace") as f:
                text = _FENCE.sub("", f.read())
        except OSError:
            continue
        front = _FRONT.match(text)
        if front and re.search(r"(?m)^detect:", front.group(1)) or _HISTORY.fullmatch(os.path.basename(md)):
            continue
        rel, here = os.path.relpath(md, root), os.path.dirname(md)
        missing = [t for t in dead_paths(text, here) if _anchored(t, root, here, tops)
                   and not os.path.exists(os.path.join(root, t))]
        ignored = _ignored(root, missing)
        findings += [{"file": rel, "kind": "path", "detail": t} for t in missing if t not in ignored]
        findings += [{"file": rel, "kind": "command", "detail": cmd} for cmd in stale_commands(text, root)]
    return findings


def _added_text(root, rel):
    """What the working tree adds to *rel* against HEAD: the + lines of its diff, or the whole file when git does
    not track it yet. A doc's drift is the task's only where it sits in that text (T-0035)."""
    try:
        tracked = subprocess.run(["git", "-C", root, "ls-files", "--error-unmatch", "--", rel],
                                 capture_output=True, text=True, timeout=30).returncode == 0
        if tracked:
            diff = subprocess.run(["git", "-C", root, "diff", "-U0", "HEAD", "--", rel],
                                  capture_output=True, text=True, timeout=30).stdout
            return "\n".join(line[1:] for line in diff.splitlines() if line.startswith("+") and not line.startswith("+++"))
    except (OSError, subprocess.SubprocessError):
        return None  # can't tell: treat all of it as the task's, as before
    try:
        with open(os.path.join(root, rel), encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def task_docs(root, docs_impact):
    """For fm task done (M/L): (blockers, notes). Docs the task says it updated must exist and add no drift; drift in
    other docs, and old drift in the ones it updated, is reported, not blocking, so an old problem never holds up
    unrelated work."""
    named = {os.path.normpath(n) for n in re.findall(r"[\w./-]+\.md\b", docs_impact or "")}
    gone = [n for n in sorted(named) if not os.path.exists(os.path.join(root, n))]
    try:  # T-1995: name the one tracked doc it most likely meant ("rules/foreman.md" for plugin/rules/foreman.md)
        tracked = subprocess.run(["git", "-C", root, "ls-files", "--", "*.md"], capture_output=True, text=True,
                                 timeout=30).stdout.splitlines() if gone else []
    except (OSError, subprocess.SubprocessError):
        tracked = []
    meant = {n: [t for t in tracked if t.endswith("/" + n)] for n in gone}
    blockers = [f"docs impact names {n}, which doesn't exist" + (f" ({meant[n][0]}?)" if len(meant[n]) == 1 else
                f" (one of {', '.join(meant[n][:3])}?)" if meant[n] else "") for n in gone]  # T-2000: up to three
    notes = []
    added = {}
    for f in scan(root):
        line = f"{f['file']}: {f['kind']} {f['detail']}"
        rel = os.path.normpath(f["file"])
        if rel in named and rel not in added:
            added[rel] = _added_text(root, rel)
        # Drift that predates the task is the doc's, not the task's: a ledger with old relative paths refused every
        # task that added a row to it (T-0035). Only drift in what this task wrote blocks.
        if rel in named and (added[rel] is None or f["detail"] in added[rel]):
            blockers.append(f"doc drift in a doc this task updated: {line}")
        else:
            notes.append(line)
    return blockers, notes


def cmd_docs(args):
    import fmcli
    import fmcore as c
    start = os.path.abspath(args.path or os.getcwd())
    root = c.git_root(start) or start
    findings = scan(root)
    fmcli.out(args, {"root": root, "findings": findings},
              "\n".join([f"{f['file']}: {f['kind']} {f['detail']}" for f in findings]) or f"No doc drift in {root}.")
    if args.strict and findings:
        raise fmcli.UsageError(f"{len(findings)} doc drift finding(s)")
