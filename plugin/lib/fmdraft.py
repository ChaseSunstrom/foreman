"""fm draft (T-1062): while nobody is waiting on the queue, a headless claude drafts the top queued S task in a throwaway
worktree on branch draft/T-x, ready to review. The draft is fingerprinted (task id + brief hash) in draft.json and swept
when the queue's top or its brief changes. Never merged; fm tidy's lanes pass and the branch name are the user's to act on."""
import hashlib
import json
import os
import re
import shutil
import subprocess

import fmcore as c

TIMEOUT = 1800


def _top(p):
    """The first queued S task whose dependencies are closed, or None."""
    briefs = c.load_briefs(p)
    state = {b.id: b.status for b in briefs}
    return next((b for b in c.order_queue(briefs)[0]
                 if b.tier == "S" and all(state.get(d) in c.CLOSED for d in c._deps(b))), None)


def _fp(b):
    with open(b.path, "rb") as f:
        return {"task": b.id, "hash": hashlib.sha256(f.read()).hexdigest()[:16]}


def _wt(p, tid):
    return os.path.join(os.path.dirname(p.root), os.path.basename(p.root) + ".draft", tid)


def _drop(p, tid):
    c._git(p.root, "worktree", "remove", "--force", _wt(p, tid), timeout=60)
    shutil.rmtree(_wt(p, tid), ignore_errors=True)
    c._git(p.root, "worktree", "prune", timeout=30)
    c._git(p.root, "branch", "-D", f"draft/{tid}", timeout=30)


def sweep(p):
    """Remove the draft when the queue's top (or its brief) no longer matches; the swept task ids."""
    path = os.path.join(p.dir, "draft.json")
    try:
        with open(path, encoding="utf-8") as f:
            old = json.load(f)
    except (OSError, ValueError):
        return []
    top = _top(p)
    if top and _fp(top) == old:
        return []
    _drop(p, old["task"])
    os.remove(path)
    return [old["task"]]


def cmd_draft(args):
    import fmcli
    p = fmcli.resolve(args)
    swept = sweep(p)
    if args.status:
        path = os.path.join(p.dir, "draft.json")
        cur = json.load(open(path, encoding="utf-8"))["task"] if os.path.exists(path) else None
        return fmcli.out(args, {"swept": swept, "draft": cur},
                         "\n".join([f"swept the stale draft of {t}" for t in swept] + [f"draft: {cur or 'none'}"]))
    top = _top(p)
    if not top:
        return fmcli.out(args, {"drafted": None, "swept": swept}, "nothing to draft: no unblocked queued S task")
    if os.path.exists(os.path.join(p.dir, "draft.json")):
        return fmcli.out(args, {"drafted": None, "swept": swept}, "a draft is already waiting for review")
    if c.read_meta(p).get("sensitive"):
        raise fmcli.UsageError("sensitive project: nothing is drafted")
    wt = _wt(p, top.id)
    os.makedirs(os.path.dirname(wt), exist_ok=True)
    r = c._git(p.root, "worktree", "add", "-q", "-b", f"draft/{top.id}", wt, "HEAD", timeout=120, proc=True)
    if r.returncode:
        raise fmcli.UsageError(f"git worktree add: {r.stderr.strip()[:200]}")
    title = re.sub(r"[\x00-\x1f\"]", " ", top.title)[:200]
    prompt = (f"Draft task {top.id} (titled \"{title}\") in this throwaway worktree: edit files so the change is ready "
              f"to review, with its test. Do not commit, push or merge; do not run fm. Brief:\n{top.section('Acceptance criteria')[:1500]}")
    try:
        subprocess.run(["claude", "-p", prompt, "--output-format", "json"], cwd=wt, capture_output=True, text=True,
                       timeout=TIMEOUT)
        c._git(wt, "add", "-A", timeout=60)
        c._git(wt, "-c", "user.name=Foreman draft", "-c", "user.email=foreman@localhost", "-c", "commit.gpgsign=false",
               "commit", "-q", "--no-verify", "-m", f"draft: {top.id} (not reviewed)", timeout=60)
    except (OSError, subprocess.SubprocessError) as e:
        _drop(p, top.id)
        raise fmcli.UsageError(f"the draft of {top.id} failed: {e}")
    with c.lock(p.dir):
        with open(os.path.join(p.dir, "draft.json"), "w", encoding="utf-8") as f:
            json.dump(_fp(top), f)
        c.log_event(p, "draft", task=top.id, data={"branch": f"draft/{top.id}"}, session=fmcli.session())
    fmcli.out(args, {"drafted": top.id, "branch": f"draft/{top.id}", "worktree": wt, "swept": swept},
              f"drafted {top.id} on draft/{top.id} ({wt}): review it, then merge or `fm draft --status` to sweep")
