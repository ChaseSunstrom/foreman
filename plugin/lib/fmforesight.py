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
    if net:  # T-2356: the same sweep runs the model-free tick (orders, the cached CI result, approved issues)
        try:
            import fmnight
            fmnight.tick(p, fetch_ci=False)  # this sweep just fetched CI itself
        except Exception:
            pass  # a tick that fails never costs the sweep its caches
    return changed


def _ci(p, fetch=True, sent=None):
    """The repo's CI result, fetched when its cache is older than CI_EVERY (fetch) and filed once per red sha. A
    request that leaves the machine is appended to `sent` first (T-2356: a tick lists each one for the final report,
    even when something after it fails)."""
    repo = github_repo(p.root)
    if not repo:
        return
    shared = os.path.join(c.state_dir(), "ci", repo.replace("/", "__") + ".json")
    r = _load(shared)
    if fetch and time.time() - r.get("checked", 0) >= CI_EVERY * (48 if r.get("private") else 1):
        if sent is not None:
            sent.append(repo)
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
                                  "FIX", "discovered", key=f"CI-red: {r['sha']}", trigger="ci-red",
                                  trial_key=f"ci:{r['branch']}:{','.join(sorted(r['failed']))}")  # T-2351
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


# ---------------------------------------------------------------- T-2406 (#3): the prediction book
PREDICTIONS = "predictions.jsonl"  # write-once rows: a next-request prediction, then (later) its one score row
MUTE_MIN = 20  # scored rows before a kind that trails its baseline is muted


def _requests(p):
    """The user's own requests, oldest first, as (brief, type, paths): paths are its scope and the files it touched
    (this project's ledger). Foreman's captures, followups and triggers aren't the user's, so they never count."""
    briefs = sorted((b for b in c.load_briefs(p, include_archive=True) if b.meta.get("source") == "user"),
                    key=lambda b: (str(b.meta.get("created") or ""), b.id))
    touched = {}
    for e in c.ledger_events(p, ("touched",)):
        f = (e.get("data") or {}).get("file")
        if e.get("task") and isinstance(f, str):
            touched.setdefault(e["task"], set()).add(os.path.relpath(f, p.root) if os.path.isabs(f) else f)
    out = []
    for b in briefs:
        scope = b.meta.get("scope") if isinstance(b.meta.get("scope"), list) else []
        out.append((b, b.type, sorted({str(x) for x in scope} | touched.get(b.id, set()))[:20]))
    return out


def _book(p):
    try:
        with open(os.path.join(p.dir, PREDICTIONS), encoding="utf-8") as f:
            rows = []
            for ln in f:
                try:
                    r = json.loads(ln)
                except ValueError:
                    continue
                if isinstance(r, dict) and isinstance(r.get("id"), str):
                    rows.append(r)
            return rows
    except OSError:
        return []


def _jaccard(a, b):
    a, b = set(a or ()), set(b or ())
    return None if not b else round(len(a & b) / len(a | b), 3)


def prediction_tick(p):
    """T-2406, on the tick (fmnight.tick): the pending next-request prediction is scored against the first user request
    after the one it followed, once (an appended score row, never rewritten); then, once per request, the next one is
    predicted beside the naive baseline (the last request again): its type from this user's own type transitions, its
    paths from their latest request of that type. Reads only this project's briefs and ledger; a sensitive project
    predicts nothing. ponytail: no co-change neighbours yet (fm graph's db can take seconds to build on a tick)."""
    if c.read_meta(p).get("sensitive"):
        return None
    reqs = _requests(p)
    if not reqs:
        return None
    rows, path = _book(p), os.path.join(p.dir, PREDICTIONS)
    scored = {r["id"] for r in rows if r.get("kind") == "score"}
    ids = [b.id for b, _, _ in reqs]
    for r in rows:
        if r.get("kind") != "next-request" or r["id"] in scored or r.get("after") not in ids:
            continue
        i = ids.index(r["after"])
        if i + 1 >= len(reqs):
            continue
        b, t, paths = reqs[i + 1]
        pred, base = r.get("pred") or {}, r.get("base") or {}
        c.append_line(path, json.dumps({"kind": "score", "id": r["id"], "for": b.id, "at": c.now(),
                                        "type_hit": pred.get("type") == t, "base_type_hit": base.get("type") == t,
                                        "overlap": _jaccard(pred.get("paths"), paths),
                                        "base_overlap": _jaccard(base.get("paths"), paths)}) + "\n")
        scored.add(r["id"])
    last, lt, lpaths = reqs[-1]
    if any(r.get("kind") == "next-request" and r.get("after") == last.id for r in rows):
        return None
    types = [t for _, t, _ in reqs]
    nxt = {}
    for a, b in zip(types, types[1:]):
        if a == lt:
            nxt[b] = nxt.get(b, 0) + 1
    ptype = max(nxt, key=lambda k: (nxt[k], -types[::-1].index(k))) if nxt else lt  # a tie goes to the most recent
    ppaths = next((ps for _, t, ps in reversed(reqs[:-1]) if t == ptype), lpaths)[:5]
    row = {"kind": "next-request", "id": f"P-{len(rows) + 1}-{int(time.time())}", "at": c.now(), "after": last.id,
           "pred": {"type": ptype, "paths": ppaths}, "base": {"type": lt, "paths": lpaths}}
    c.append_line(path, json.dumps(row) + "\n")
    return row


def _rate(xs):
    return round(sum(xs) / len(xs), 3) if xs else None


def prediction_kinds(p):
    """T-2406: per prediction kind, scored rows, the hit rate beside the naive baseline's, and whether it is muted (it
    trailed the baseline over MUTE_MIN+ rows scored since its last unmute). next-request: the type hit (the path
    overlap's means ride along); effort (T-2290): a predicted minutes within 2x of the actual, against the median
    minutes of the tier's earlier closes."""
    import statistics
    import fmoutcomes
    unmuted = c.read_meta(p).get("predictions_unmuted") or {}
    since = lambda k: str(unmuted.get(k) or "") if isinstance(unmuted, dict) else ""  # noqa: E731
    scores = [r for r in _book(p) if r.get("kind") == "score"]
    kinds = []

    def kind(name, rows, extra=None):  # rows: (at, hit, base hit or None)
        fresh = [(h, bh) for at, h, bh in rows if at >= since(name) and bh is not None]
        hit, base = _rate([h for h, _ in fresh]), _rate([bh for _, bh in fresh])
        kinds.append(dict({"kind": name, "n": len(rows), "hit": _rate([h for _, h, _ in rows]),
                           "base_hit": _rate([bh for _, _, bh in rows if bh is not None]),
                           "muted": len(fresh) >= MUTE_MIN and hit is not None and base is not None and hit < base},
                          **(extra or {})))
    kind("next-request", [(str(r.get("at") or ""), r.get("type_hit") is True, r.get("base_type_hit") is True)
                          for r in scores],
         {"overlap": _rate([r["overlap"] for r in scores if isinstance(r.get("overlap"), (int, float))]),
          "base_overlap": _rate([r["base_overlap"] for r in scores if isinstance(r.get("base_overlap"), (int, float))])})
    effort, seen = [], {}
    for r in fmoutcomes._closes(p):
        pm, m, tier = r.get("predict_minutes"), r.get("minutes"), r.get("tier")
        if not (isinstance(pm, int) and pm > 0 and isinstance(m, int) and m > 0 and tier):
            continue
        prior = seen.setdefault(tier, [])
        base = statistics.median(prior) if prior else None
        effort.append((str(r.get("at") or ""), 0.5 <= m / pm <= 2, (0.5 <= m / base <= 2) if base else None))
        prior.append(m)
    kind("effort", effort)
    return kinds


def muted_kinds(p):
    return [k for k in prediction_kinds(p) if k["muted"]]
