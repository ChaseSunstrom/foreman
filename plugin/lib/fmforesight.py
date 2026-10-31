"""T-1810: Foreman reasons ahead. The Stop hook's detached sweep (fm cost --sweep, at most every SWEEP_EVERY per
project) looks for problems nobody raised (CI red on the default branch, a changed model, window or CC version) and
caches them; session start reads those caches and the state it already has (blocked pile, tidy), never the network,
and names each problem with its action."""
import glob
import json
import os
import re
import time

import fmcore as c

CI_EVERY = 1800  # GitHub's unauthenticated API allows 60 calls an hour per address: 2 an hour per project
CHANGE_DAYS = 3  # a setup change stays in the session-start line this long
STALE_DAYS = 14  # a blocked task untouched this long is a pile, not a wait
SWEEP_EVERY = 600  # the Stop hook spawns the sweep at most this often per project; the burn scan's own 10 min


def _path():
    return os.path.join(c.state_dir(), "foresight.json")


def setup_now():
    """{model, window, cc} from the newest statusline snapshot that names a model, or None."""
    snaps = sorted(glob.glob(os.path.join(c.state_dir(), "sessions", "*.json")), key=os.path.getmtime)
    for path in reversed(snaps[-3:]):
        try:
            with open(path, encoding="utf-8") as f:
                d = json.load(f)
        except (OSError, ValueError):
            continue
        if d.get("model"):
            return {"model": d["model"], "window": d.get("context_size"), "cc": d.get("version")}
    return None


def _k(n):
    return f"{n / 1e6:g}M" if n >= 1e6 else f"{n / 1e3:g}k"


def setup_change(old, new):
    """'Opus 5 → Opus 5.5, window 200k → 1M, CC 2.1.305 → 2.1.312' for what differs ('' for nothing); a value one side
    doesn't know (an older snapshot without the CC version) isn't a change."""
    out = []
    for key, label, fmt in (("model", "", str), ("window", "window ", _k), ("cc", "CC ", str)):
        a, b = old.get(key), new.get(key)
        if a and b and a != b:
            out.append(f"{label}{fmt(a)} → {fmt(b)}")
    return ", ".join(out)


def github_repo(root):
    """'owner/name' of origin when it's on github.com, else None."""
    code, url = c.run_command(root, "git remote get-url origin", timeout=5)
    m = re.search(r"github\.com[:/]([\w.-]+/[\w.-]+?)(?:\.git)?/?$", url.strip()) if code == 0 else None
    return m.group(1) if m else None


def default_branch(root):
    """origin's default branch as this clone knows it (origin/HEAD), else main."""
    code, out = c.run_command(root, "git symbolic-ref --short refs/remotes/origin/HEAD", timeout=5)
    m = re.fullmatch(r"origin/([\w./-]{1,60})", out.strip()) if code == 0 else None
    return m.group(1) if m else "main"


BAD = ("failure", "timed_out", "startup_failure")


def ci_main(repo, branch="main", timeout=5):
    """(sha, [failed workflows]) from the branch's newest finished run of each workflow, via GitHub's public API: the
    newest failing run's sha when any failed. 'private' on a 404 (a private repo: retried daily), None on any other
    failure. Workflow runs, not check runs: a job marked continue-on-error doesn't fail its run."""
    import http.client
    import urllib.error
    import urllib.parse
    import urllib.request
    req = urllib.request.Request(f"https://api.github.com/repos/{repo}/actions/runs?per_page=20&branch="
                                 + urllib.parse.quote(branch, safe=""),
                                 headers={"Accept": "application/vnd.github+json", "User-Agent": "foreman"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            runs = json.load(r).get("workflow_runs") or []
    except urllib.error.HTTPError as e:
        return "private" if e.code == 404 else None
    except (OSError, ValueError, AttributeError, http.client.HTTPException):
        return None
    newest = {}
    for x in runs:  # newest first: each workflow's latest finished run; a cancelled one (a job timeout, a newer push)
        if isinstance(x, dict) and x.get("status") == "completed":  # says nothing, and an older red run no longer speaks
            newest.setdefault(x.get("name"), x)
    red = [x for x in newest.values() if x.get("conclusion") in BAD]
    sha = str(((red or list(newest.values())) or [{}])[0].get("head_sha") or "")
    if not re.fullmatch(r"[0-9a-f]{40}", sha):  # the API's text goes into a task and a model prompt: checked first
        return None
    return sha, sorted(c.fit(c.plain(str(x.get("name"))), 40) for x in red)[:5]


def _load(path):
    try:
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, dict) else {}
    except (OSError, ValueError):
        return {}


def _save(path, d):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        c.write_atomic(path, json.dumps(d))
    except OSError:
        pass  # a cache: never worth failing for


def _mine(p):
    return os.path.join(p.dir, "foresight.json")


def refresh(p, net=True):
    """The detached sweep (fm cost --sweep). True when the setup changed (the caller reruns the burn scan at once).
    Setup lives in one global file and CI in one file per repo, each written whole: two projects never drop each
    other's entries, and clones and worktrees of one repo share its one call per CI_EVERY."""
    d, changed, now = _load(_path()), False, setup_now()
    if now and d.get("setup") != now:
        what = setup_change(d.get("setup") or {}, now)
        if what:
            d["changed"], changed = {"ts": time.time(), "what": what}, True
        d["setup"] = now
        _save(_path(), d)
    if net and not os.environ.get("FOREMAN_NO_NET") and not c.read_meta(p).get("sensitive"):
        _ci(p)
    return changed


def _ci(p):
    repo = github_repo(p.root)
    if not repo:
        return
    shared = os.path.join(c.state_dir(), "ci", repo.replace("/", "__") + ".json")
    r = _load(shared)
    if time.time() - r.get("checked", 0) >= CI_EVERY * (48 if r.get("private") else 1):
        branch = default_branch(p.root)
        got = ci_main(repo, branch)
        if got == "private":
            r = {"checked": time.time(), "private": True}
        elif got:
            r = {"checked": time.time(), "branch": branch, "sha": got[0], "failed": got[1]}
        else:  # offline or rate limited: what was known stands until the next try
            r["checked"] = time.time()
        _save(shared, r)  # stored before the capture: a capture that fails retries without another call
    mine = _load(_mine(p))
    if r.get("failed") and r.get("sha") != mine.get("sha"):
        import fmeco
        b, _ = fmeco.capture_once(p, f"FIX: CI on {r['branch']} is red at {r['sha'][:7]} ({', '.join(r['failed'])})"
                                     f"\nCONTEXT: found by the session-start sweep (T-1810): "
                                     f"https://github.com/{repo}/commit/{r['sha']}\nCI-red: {r['sha']}",
                                  "FIX", "discovered", key=f"CI-red: {r['sha']}", trigger="ci-red")
        _save(_mine(p), {k: r[k] for k in ("branch", "sha", "failed")} | {"task": b.id})
    elif r.get("sha") and not r.get("failed") and mine:
        _save(_mine(p), {})  # green again


def pile_lines(sd):
    """The blocked pile and an overdue tidy, each with its action."""
    out, blocked = [], sd.get("blocked") or []
    if blocked:
        dated = sorted((x["updated"], x["id"]) for x in blocked if c.age_days(x.get("updated")) is not None)
        days = c.age_days(dated[0][0]) if dated else 0
        out.append(f"{len(blocked)} blocked" + (f", oldest untouched {days:.0f} days ({dated[0][1]})"
                                                if days > STALE_DAYS else "") + " → fm tidy")  # T-2117: short items
    if sd.get("tidy_overdue_days"):
        out.append(f"tidy overdue {sd['tidy_overdue_days']} days → fm tidy")
    return out


def lines(p):
    """What the caches say for session start: a recent setup change, this project's CI red."""
    d, out = _load(_path()), []
    ch = d.get("changed") or {}
    if ch.get("what") and time.time() - ch.get("ts", 0) < CHANGE_DAYS * 86400:
        out.append(f"Setup changed ({ch['what']}): every default's cost moves with it → fm cost --by-model and fm budget "
                   "for the new per-call cost; fm doctor for CC features to adopt and settings to redo.")
    ci = _load(_mine(p))
    if ci.get("failed") and ci.get("sha"):
        b = c.find_brief(p, str(ci.get("task") or ""))
        status = b.status if b else "closed"  # an archived task is closed too
        act = (f"{ci.get('task')} is {status}: push its fix if it isn't on {ci.get('branch') or 'main'}, else the "
               "newest run is still going" if status in c.CLOSED | {"closed"} else f"fix it first: {ci.get('task')}")
        out.append(f"CI on {ci.get('branch') or 'main'} is red at {str(ci['sha'])[:7]} ({', '.join(map(str, ci['failed']))})"
                   f" → {act}.")
    return out
