"""T-1810: Foreman reasons ahead. The Stop hook's detached sweep (fm cost --sweep, at most every SWEEP_EVERY per
project) looks for problems nobody raised (CI red on the default branch, a changed model, window or CC version) and
caches them; session start reads those caches and the state it already has (blocked pile, tidy), never the network,
and names each problem with its action."""
import datetime
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


def predict(reqs):
    """(type, paths) of the request after reqs ((brief, type, paths), oldest first): the type from this user's own
    type transitions out of the last one (a tie goes to the most recent), the paths from their latest earlier request
    of that type (else the last's). The tick's predictor and fm exam's replay of it (T-2409)."""
    lt, lpaths = reqs[-1][1], reqs[-1][2]
    types = [t for _, t, _ in reqs]
    nxt = {}
    for a, b in zip(types, types[1:]):
        if a == lt:
            nxt[b] = nxt.get(b, 0) + 1
    ptype = max(nxt, key=lambda k: (nxt[k], -types[::-1].index(k))) if nxt else lt
    return ptype, next((ps for _, t, ps in reversed(reqs[:-1]) if t == ptype), lpaths)[:5]


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
    ptype, ppaths = predict(reqs)
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
    book = _book(p)
    scores = [r for r in book if r.get("kind") == "score"]
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
    kind("draft-ahead", [(str(r.get("at") or ""), r.get("adopted") is True, None) for r in book  # T-2407: no baseline
                         if r.get("kind") == "draft" and (r.get("adopted") or r.get("expired"))])
    ws = [r for r in book if r.get("kind") == "warning-score"]
    for w in ("date", "cochange", "state"):  # T-2408: precision (hits of hits and misses); acted-on rows ride along
        mine = [r for r in ws if r.get("wkind") == w]
        kind(f"foresight-{w}", [(str(r.get("at") or ""), r.get("hit") is True, None) for r in mine if not r.get("acted")],
             {"acted": sum(bool(r.get("acted")) for r in mine)})
    return kinds


def muted_kinds(p):
    return [k for k in prediction_kinds(p) if k["muted"]]


# ---------------------------------------------------------------- T-2408 (#3): breakage warnings
WARN_STATE = "foresight-warn.json"  # {day, head, sizes: {YYYY-MM-DD: bytes}}: the detectors run once a local day
# PAIR_MIN, PAIR_SHARE: 5 pairings and 80% of the file's commits; 3 and 60% flagged 30 of Foreman's last 20 commits
# (fmforesight without fmeco), 5 and 80% flags 4, each a module without its test file
DATE_DAYS, STATE_DAYS, PAIR_MIN, PAIR_SHARE, PAIR_COMMITS, WARN_MAX = 14, 30, 5, 0.8, 500, 3
CODE_EXT = (".py", ".pyi", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".go", ".rs", ".rb", ".java", ".kt", ".swift",
            ".c", ".h", ".cc", ".cpp", ".cs", ".php", ".sh", ".bash", ".toml", ".json", ".yml", ".yaml", ".ini", ".cfg",
            ".conf", ".sql")  # code, tests and config; prose (.md, .txt, changelogs) never counts
_DATE = re.compile(r"(?<![\d-])(20\d\d)-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])(?!\d)")


def _state_bytes(p):
    """This project's state in bytes, without fm tidy's backups (as fmdoctor.check_state_size counts it)."""
    total = 0
    for root, dirs, names in os.walk(p.dir):
        if root == p.dir:
            dirs[:] = [d for d in dirs if d != "backups"]
        for n in names:
            try:
                total += os.path.getsize(os.path.join(root, n))
            except OSError:
                pass
    return total


def _dates(p, today):
    """(path, line, date) for each literal date in tracked code, tests or config passing within DATE_DAYS.
    ponytail: reads every tracked code file once a day (20000 at most); an index if a repo outgrows that."""
    out, end = [], today + datetime.timedelta(days=DATE_DAYS)
    for rel in [x for x in c._git(p.root, "ls-files", "-z", timeout=60).split("\0") if x.endswith(CODE_EXT)][:20000]:
        path = os.path.join(p.root, rel)
        try:
            if os.path.islink(path) or os.path.getsize(path) > 512 * 1024:
                continue
            with open(path, encoding="utf-8", errors="replace") as f:
                for n, ln in enumerate(f, 1):
                    for m in _DATE.finditer(ln):
                        try:
                            d = datetime.date(*map(int, m.groups()))
                        except ValueError:
                            continue
                        if today < d <= end:  # today's own date has passed: fixtures written today aren't deadlines
                            out.append((rel, n, d.isoformat()))
        except OSError:
            continue
    return out


def _cochange(p, head):
    """(sha, file, partner) for each commit since head that changed a file without the partner it went with in
    PAIR_MIN+ of the last PAIR_COMMITS commits and PAIR_SHARE+ of the file's own (commits of 30+ files don't count)."""
    new = c._git(p.root, "rev-list", "--max-count=20", f"{head}..HEAD", timeout=30).split() if head else []
    if not new:
        return []
    commits = {}
    for chunk in c._git(p.root, "log", f"--max-count={PAIR_COMMITS}", "--name-only", "--format=%x00%H",
                        timeout=60).split("\0")[1:]:
        lines = chunk.strip().splitlines()
        if lines:
            commits[lines[0]] = set(lines[1:])
    one, two = {}, {}
    for sha, files in commits.items():
        if sha in new or len(files) > 30:
            continue
        for x in files:
            one[x] = one.get(x, 0) + 1
            for y in files - {x}:
                two[(x, y)] = two.get((x, y), 0) + 1
    out = []
    for sha in reversed(new):
        files = commits.get(sha, set())
        out += [(sha, x, y) for (x, y), k in two.items() if x in files and y not in files and k >= PAIR_MIN
                and k / one[x] >= PAIR_SHARE and os.path.exists(os.path.join(p.root, y))]
    return out


def _state_days(sizes, budget):
    """Days until the state's trend (a least-squares line over the last STATE_DAYS of daily sizes) reaches budget,
    when that is within STATE_DAYS; None when flat, shrinking, already over or further off."""
    pts = sorted((datetime.date.fromisoformat(k), v) for k, v in sizes.items())
    pts = [(d, v) for d, v in pts if (pts[-1][0] - d).days <= STATE_DAYS]
    if len(pts) < 2 or (pts[-1][0] - pts[0][0]).days < 3 or pts[-1][1] >= budget:
        return None
    xs, ys = [(d - pts[0][0]).days for d, _ in pts], [v for _, v in pts]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    days = (budget - ys[-1]) / slope if slope > 0 else None
    return int(days) if days is not None and days <= STATE_DAYS else None


def _failed_at(events, target):
    """A failed run naming the target's file stem: a failed evidence run or a gate run's failing test names."""
    stem = re.compile(r"\b" + re.escape(os.path.splitext(os.path.basename(target))[0]) + r"\b")
    for e in events:
        d = e.get("data") or {}
        if e.get("event") == "evidence" and (c.result_exit(d.get("result")) or 0) and stem.search(
                f"{d.get('cmd')} {d.get('result')}"):
            return True
        if e.get("event") == "check_run" and any(r.get("exit") and any(stem.search(str(n)) for n in r.get("failing") or ())
                                                 for r in d.get("results") or () if isinstance(r, dict)):
            return True
    return False


def _score_warnings(p, rows, today, size, budget):
    """Each open warning scored once: a hit when the failure shows at its target (a failed run naming it, the state
    budget crossed) or a commit from a task other than the warning's own changes it (the dated literal, the partner);
    acted on when only its own task's commits did; a miss (or acted on) once its window passes."""
    scored = {r.get("id") for r in rows if r.get("kind") == "warning-score"}
    todo = [r for r in rows if r.get("kind") == "warning" and r.get("id") not in scored
            and isinstance(r.get("until"), str) and isinstance(r.get("at"), str)]
    events = c.ledger_events(p, ("evidence", "check_run"), since=min(r["at"] for r in todo)) if todo else []
    for r in todo:
        hit = acted = False
        if r.get("wkind") == "state":
            hit = size >= budget
        else:
            hit = _failed_at([e for e in events if str(e.get("ts") or "") >= r["at"]], r["target"])
            if not hit and r.get("head"):
                pick = [f"-S{r['date']}"] if r.get("date") else []
                subj = c._git(p.root, "log", "--format=%s", *pick, f"{r['head']}..HEAD", "--", r["target"],
                              timeout=30).splitlines()
                own = [s for s in subj if re.match(re.escape(str(r.get("task"))) + r"\b", s)]
                hit, acted = len(subj) > len(own), bool(own)
        if hit or today > datetime.date.fromisoformat(r["until"][:10]):
            c.append_line(os.path.join(p.dir, PREDICTIONS), json.dumps(
                {"kind": "warning-score", "id": r["id"], "wkind": r.get("wkind"), "at": c.now(), "hit": hit,
                 "acted": acted and not hit}) + "\n")


def breakage_tick(p, today=None, budget=None):
    """T-2408 (#3), on the tick, once a local day: open warnings are scored, then each detector files what it sees
    through the trigger table (fmeco.capture_once, trigger foresight-KIND), WARN_MAX a kind a day, one open warning
    per target: a literal date in tracked code, tests or config passing within DATE_DAYS; a commit since the last
    look that changed a file without its usual co-change partner (a 14-day window); state whose 30-day trend reaches
    its budget (fmdoctor.STATE_BUDGET) within STATE_DAYS. Each warning is a book row with its window. The new rows."""
    import fmdoctor
    import fmeco
    import fmmodels  # $FOREMAN_TODAY pins the clock (fm exam's breakage replay, T-2409)
    today, budget = today or fmmodels._today(None), budget or fmdoctor.STATE_BUDGET
    path = os.path.join(p.dir, WARN_STATE)
    try:
        with open(path, encoding="utf-8") as f:
            st = json.load(f)
    except (OSError, ValueError):
        st = {}
    st = st if isinstance(st, dict) else {}
    if st.get("day") == today.isoformat():
        return []
    sizes = {k: v for k, v in (st.get("sizes") or {}).items() if isinstance(k, str) and isinstance(v, int)
             and re.fullmatch(r"\d{4}-\d\d-\d\d", k) and (today - datetime.date.fromisoformat(k)).days <= 2 * STATE_DAYS}
    sizes[today.isoformat()] = _state_bytes(p)
    head = c._git(p.root, "rev-parse", "HEAD", timeout=10).strip()
    rows = _book(p)
    _score_warnings(p, rows, today, sizes[today.isoformat()], budget)
    scored = {r.get("id") for r in _book(p) if r.get("kind") == "warning-score"}
    live = {(r.get("wkind"), r.get("target"), r.get("line")) for r in rows if r.get("kind") == "warning"
            and r.get("id") not in scored}
    soon = (today + datetime.timedelta(days=DATE_DAYS)).isoformat()
    found = [("date", rel, n, d, f"Breakage ahead: {rel}:{n} holds the date {d}, which passes in "
              f"{(datetime.date.fromisoformat(d) - today).days} days", {"date": d}) for rel, n, d in _dates(p, today)]
    found += [("cochange", y, None, soon, f"Breakage ahead: {sha[:7]} changed {x} without {y}, which changed with it "
               f"in most past commits", {"file": x, "sha": sha}) for sha, x, y in _cochange(p, st.get("head"))]
    days = _state_days(sizes, budget)
    if days is not None:
        found.append(("state", "state", None, (today + datetime.timedelta(days=days)).isoformat(),
                      f"Breakage ahead: this project's state ({sizes[today.isoformat()] // 2**20} MB) reaches its "
                      f"{budget // 2**20} MB budget in about {days} days at its 30-day trend (fm tidy --apply)", {}))
    new, per = [], {}
    for wkind, target, line, until, text, extra in found:
        if (wkind, target, line) in live or per.get(wkind, 0) >= WARN_MAX:
            continue
        key = f"foresight-{wkind} {target}" + (f":{line}" if line else "")
        b, made = fmeco.capture_once(p, f"{c.plain(text)}\n{key}", "FIX", "foresight", key=key,
                                     trigger=f"foresight-{wkind}")
        if not (b and made):
            continue
        live.add((wkind, target, line))
        per[wkind] = per.get(wkind, 0) + 1
        row = dict({"kind": "warning", "id": f"W-{len(rows) + len(new) + 1}-{int(time.time())}", "wkind": wkind,
                    "at": c.now(), "until": until, "target": target, "line": line, "head": head, "task": b.id}, **extra)
        c.append_line(os.path.join(p.dir, PREDICTIONS), json.dumps(row) + "\n")
        new.append(row)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"day": today.isoformat(), "head": head, "sizes": sizes}, f)
    return new
