"""T-0710 (Frontier 10, first slice): a milestone built in one pass lands as a stack of commits, one per step group (per
member for a batch host), each checked alone. Files go to the step they were last edited in, read from the ledger's
order of touched and step-evidence events; each commit is checked in a scratch worktree with --stack-check or the
group's own verify commands; one whose check fails alone is folded into the next. Called by fm task finish --stack."""
import os
import re
import shutil
import subprocess
import tempfile

import fmcore as c


def assign(p, b, files):
    """{file: step number}: the step current when the file was last edited (after step N's evidence, step N+1)."""
    n = max(len(b.steps()), 1)
    step, where = 1, {}
    for e in c.ledger_tail(p, c.TASK_WINDOW):
        if e.get("task") != b.id:
            continue
        d = e.get("data") or {}
        if e.get("event") == "evidence" and isinstance(d.get("step"), int):
            step = max(step, min(d["step"] + 1, n))
        elif e.get("event") == "touched" and d.get("file"):
            rel = os.path.relpath(d["file"], p.root)
            if rel in files:
                where[rel] = step
    return {f: where.get(f, n) for f in files}


def groups(b, steps_of):
    """[(label, [files], [verify commands])] in step order: a batch host's steps group by member."""
    out, keyed, of_step = [], {}, {}
    for s in b.steps():
        m = re.match(r"(T-\d{4,}):", s.text)
        key = m.group(1) if m else f"step {s.n}"
        if key not in keyed:
            verify = [v for a in b.acceptance() if m and a.text.startswith(f"{key}:") and (v := c.verify_of(a.text))]
            keyed[key] = (key if m else f"step {s.n}: {c.fit(s.text, 60)}", [], verify)
            out.append(keyed[key])
        of_step[s.n] = keyed[key]
    if not out:
        return [("all", sorted(steps_of), [])]
    for f, n in sorted(steps_of.items()):
        (of_step.get(n) or out[-1])[1].append(f)
    return out


def _git(root, *a, env=None, input=None):
    return subprocess.run(["git", "-C", root, *a], capture_output=True, text=True, env=env, input=input, timeout=300)


def commit(p, b, files, message, check=None):
    """Build the stack on the current branch; returns the report lines. Raises ValueError when it can't."""
    root = c.git_root(p.root)
    branch = _git(root, "symbolic-ref", "-q", "HEAD").stdout.strip()
    head = _git(root, "rev-parse", "HEAD").stdout.strip()
    if not branch or not head:
        raise ValueError("a stack needs a branch with a commit (not a detached or empty HEAD)")
    flat = []
    for f in files:  # a synced .foreman/ mirror is a folder: its files
        full = os.path.join(p.root, f)
        flat += [os.path.relpath(os.path.join(d, n), p.root) for d, _, ns in os.walk(full) for n in ns] \
            if os.path.isdir(full) else [f]
    files = flat
    rels = [os.path.relpath(os.path.join(p.root, f), root) for f in files]
    plan = [g for g in groups(b, assign(p, b, files)) if g[1]] or [("all", list(files), [])]
    subject, _, body = message.partition("\n")
    parent, pending, made, report = head, [], [], []
    with tempfile.TemporaryDirectory() as tmp:
        env = dict(os.environ, GIT_INDEX_FILE=os.path.join(tmp, "index"))
        for i, (label, gfiles, verify) in enumerate(plan):
            pending += gfiles
            last = i == len(plan) - 1
            _git(root, "read-tree", parent, env=env)
            paths = [os.path.relpath(os.path.join(p.root, f), root) for f in pending]
            _git(root, "update-index", "--add", "--remove", "--", *paths, env=env)
            tree = _git(root, "write-tree", env=env).stdout.strip()
            msg = f"{subject} ({len(made) + 1}/{len(plan)}): {label}" + (f"\n{body}" if body.strip() else "")
            new = _git(root, "commit-tree", tree, "-p", parent, "-m", msg, "-m", f"Foreman-Task: {b.id}").stdout.strip()
            if not new:
                raise ValueError(f"git commit-tree failed for {label}")
            cmds = [check] if check else verify
            if cmds and not last:
                red = _red(root, new, cmds)
                if red:
                    report.append(f"  {label}: folded into the next commit (alone it fails: {red})")
                    continue
            parent, pending = new, []
            made.append(new)
            report.append(f"  {new[:8]} {label}: {', '.join(gfiles) or '(nothing of its own)'}"
                          + (", checked alone" if cmds and not last else ""))
    if _git(root, "update-ref", branch, parent, head).returncode:
        raise ValueError(f"the branch moved while the stack was built; nothing changed ({branch} is still {head[:8]})")
    _git(root, "reset", "-q", "--", *rels)  # only the task's paths: other staged work stays staged
    return [f"{b.id}: committed a stack of {len(made)} on {branch.rsplit('/', 1)[-1]}:"] + report


def _red(root, commit, cmds):
    """Why the commit fails alone, or None: each command run in a scratch worktree of it."""
    wt = tempfile.mkdtemp(prefix="fm-stack-")
    try:
        if _git(root, "worktree", "add", "-q", "--detach", wt, commit).returncode:
            return "its scratch worktree couldn't be made"
        for cmd in cmds:
            code, output = c.run_command(wt, cmd, 600)
            if code:
                return f"{cmd} → {c.run_result(code, output)}"
        return None
    finally:
        _git(root, "worktree", "remove", "--force", wt)
        shutil.rmtree(wt, ignore_errors=True)
