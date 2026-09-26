"""fm docs: markdown that drifted from the repo — paths that don't exist, npm/make commands that aren't defined.

Report-only. Reuses tidy's detectors; paths may be relative to the file or to the repo root, gitignored
(machine-specific) paths and fenced code blocks are skipped.
"""
import os
import re
import subprocess

from fmtidy import dead_paths, stale_commands

SKIP_DIRS = {"node_modules", "vendor", "dist", "build", "target", "venv", "__pycache__"}
_FENCE = re.compile(r"```.*?```", re.S)


def _markdown(root):
    for d, dirs, files in os.walk(root):
        dirs[:] = sorted(x for x in dirs if x not in SKIP_DIRS and not x.startswith("."))
        yield from (os.path.join(d, f) for f in sorted(files) if f.endswith(".md"))


def _ignored(root, rels):
    if not rels:
        return set()
    try:
        p = subprocess.run(["git", "-C", root, "check-ignore", "--stdin"], input="\n".join(rels), capture_output=True,
                           text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return set()
    return set(p.stdout.splitlines())


def _anchored(tok, root, here):
    """Only paths that clearly point into this repo: ./ or ../, or a first component that exists at the repo root or
    next to the file. Bare names, other repos (org/repo), branches and domains are too ambiguous to call drift."""
    if tok.startswith(("./", "../")):
        return True
    first = tok.split("/", 1)[0]
    return "/" in tok and bool(first) and (os.path.exists(os.path.join(root, first)) or
                                           os.path.exists(os.path.join(here, first)))


def scan(root):
    findings = []
    for md in _markdown(root):
        try:
            with open(md, encoding="utf-8", errors="replace") as f:
                text = _FENCE.sub("", f.read())
        except OSError:
            continue
        rel, here = os.path.relpath(md, root), os.path.dirname(md)
        missing = [t for t in dead_paths(text, here) if _anchored(t, root, here)
                   and not os.path.exists(os.path.join(root, t))]
        ignored = _ignored(root, missing)
        findings += [{"file": rel, "kind": "path", "detail": t} for t in missing if t not in ignored]
        findings += [{"file": rel, "kind": "command", "detail": cmd} for cmd in stale_commands(text, root)]
    return findings


def task_docs(root, docs_impact):
    """For fm task done (M/L): (blockers, notes). Docs the task says it updated must exist and show no drift; drift in
    other docs is reported, not blocking, so an old problem elsewhere never holds up unrelated work."""
    named = {os.path.normpath(n) for n in re.findall(r"[\w./-]+\.md\b", docs_impact or "")}
    blockers = [f"docs impact names {n}, which doesn't exist" for n in sorted(named)
                if not os.path.exists(os.path.join(root, n))]
    notes = []
    for f in scan(root):
        line = f"{f['file']}: {f['kind']} {f['detail']}"
        if os.path.normpath(f["file"]) in named:
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
