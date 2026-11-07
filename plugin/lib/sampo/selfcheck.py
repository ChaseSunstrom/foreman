"""T-3127: self-checks: what the user would otherwise have to point out, named with its numbers before they ask. On
2026-11-06 they asked, one message each: why landed work hadn't reached GitHub in 22 hours, why a retired .foreman/
was tracked beside .sampo/, and why pages they had asked for weren't done, then "I shouldn't even need to send any of
the messages". Each check reads state and at most one git call; lines() caches the set CACHE_S per project, and
next_for (sampo next and the drive's line) shows it in every state, not only when idle."""
import collections
import json
import os
import time

from sampo import core as c

CACHE_S = 300
SHIP_H = 2  # landed work unshipped this long (its oldest commit since the last ship)
ASK_DAYS, ASK_H = 3, 2  # the user's asks from the last ASK_DAYS days, open ASK_H hours or more
OPEN = ("captured", "planned", "active", "verifying")  # deferred: the user said later; blocked: its own line says why


def _age(secs):
    h = secs / 3600
    return f"{h:.0f} h" if h >= 1 else f"{secs / 60:.0f} min"


def unshipped(p, briefs, now):
    """Commits since the last sampo ship (its ref) whose oldest is SHIP_H hours old: ship_waiting says how many only
    when no task is open, so a busy session never saw 22 hours of work wait."""
    last = "refs/foreman/shipped"  # release.SHIPPED; re-picked or rebased past it, the range isn't what main lacks
    if c._git(p.root, "merge-base", "--is-ancestor", last, "HEAD", proc=True, timeout=10).returncode:
        return None
    times = c._git(p.root, "log", "--first-parent", "--format=%ct", f"{last}..HEAD", timeout=10).split()
    if not times:
        return None
    oldest = now - int(times[-1])
    if oldest < SHIP_H * 3600:
        return None
    return f"{len(times)} landed commit(s) unshipped, the oldest {_age(oldest)} → sampo ship"


def old_mirror(p, briefs, now):
    """The retired mirror folder tracked beside the current one: a process on pre-rename code (or a pull) brings it
    back, and a close commits it (T-3390's did, 6,233 files)."""
    old, new = c.MIRRORS[1], c.MIRROR
    if not os.path.isdir(os.path.join(p.root, old)) or not os.path.isdir(os.path.join(p.root, new)):
        return None
    if not c._git(p.root, "ls-files", "--", old, timeout=10).strip():
        return None
    return f"the retired {old}/ is tracked beside {new}/ → sampo sync export folds it in and commits it gone"


def asks_waiting(p, briefs, now):
    """The user's own asks from the last ASK_DAYS days that are open ASK_H hours or more, oldest first, each with
    where it sits: they ask "why isn't X done" next."""
    from sampo import foresight
    tower, rows = foresight._tower_ids(p), []  # review: the tower's own briefs and agent-noted ones aren't the user's
    for b in briefs:
        if b.meta.get("source") != "user" or b.status not in OPEN or b.id in tower \
                or c._NOTE_RAW.search(b.section("Raw request")):
            continue
        made = c.age_days(b.meta.get("created"))
        if made is None or made > ASK_DAYS or made * 24 < ASK_H:
            continue
        rows.append((made, b))
    if not rows:
        return None
    rows.sort(key=lambda r: -r[0])
    shown = []
    for made, b in rows[:3]:
        where = b.status + (": its lane waits on a merge" if b.meta.get("builder_returned") else "")
        shown.append(f"{b.id} ({_age(made * 86400)}, {where})")
    return (f"{len(rows)} of the user's asks from the last {ASK_DAYS} days aren't landed; oldest: " + "; ".join(shown)
            + " → land or unblock the oldest first")


WAIT_MIN, RATE_H = 5, 2  # T-3478: lanes waiting before the rate is worth a line; the window it is measured over


def landing_rate(p, briefs, now):
    """T-3478: finished lanes waiting on a merge, the landings of the last RATE_H hours (minutes each) and the hours
    the pile takes to clear at that rate: 'why is this taking so long just to push?' was asked with ~50 waiting at
    ~15 min each, a number nobody had said."""
    from sampo import lanes as slanes
    waiting = slanes.awaiting_merge(p, briefs)
    if len(waiting) < WAIT_MIN:
        return None
    since = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now - RATE_H * 3600))
    landed = {e.get("task") for e in c.ledger_events(p, ("lane_merge",), since=since)
              if str(e.get("ts", "")) >= since and not (e.get("data") or {}).get("undone")}
    if not landed:
        return f"{len(waiting)} finished lanes wait and none landed in the last {RATE_H} h → {c.merge_hint(waiting)}"
    each = RATE_H * 60 / len(landed)
    return (f"{len(waiting)} finished lanes wait; {len(landed)} landed in the last {RATE_H} h (~{each:.0f} min each), "
            f"so the pile clears in ~{len(waiting) * each / 60:.0f} h at this rate → measure the slowest step and cut it")


CHECKS = (unshipped, old_mirror, asks_waiting, landing_rate)


UNTRACKED_H, UNTRACKED_STATS = 1, 500  # untracked this long is left behind, not work in progress; files stat'ed


def _older(path, now):
    try:
        return now - os.path.getmtime(path) >= UNTRACKED_H * 3600
    except OSError:
        return False


def untracked(p, briefs, now):
    """T-3548: untracked, non-ignored files in the main checkout are part of its code tree (core.worktree_tree), so no
    close there matches the train's pass on the merged commit and each reruns its linked tests: an untracked scripts/
    did that all day (78-309 s a close). The mirror's .md files are left out, as worktree_tree leaves them. From a lane
    (p.root is its worktree, the cache is the project's) it reads the main checkout all the same. Only files untouched
    UNTRACKED_H hours count: one made a minute ago is work in progress."""
    main = c.main_worktree(p.root) or p.root
    out = c._git(main, "ls-files", "-z", "--others", "--exclude-standard", "--", ".",
                 *(f":(exclude,glob){m}/**/*.md" for m in c.MIRRORS), timeout=10)
    # ponytail: only the first UNTRACKED_STATS listed are stat'ed; a bigger pile is named by its first part
    files = [f for f in out.split("\0")[:UNTRACKED_STATS] if f and _older(os.path.join(main, f), now)]
    if not files:
        return None
    tops = collections.Counter(f.split("/")[0] + ("/" if "/" in f else "") for f in files)  # ls-files order on ties
    shown = [t + (f" ({n})" if t.endswith("/") else "") for t, n in tops.most_common()]
    return (f"{len(files)} untracked file(s) in the main checkout ({c.joinmore(shown, 4)}) keep every close off the "
            "train's pass, so each reruns its tests → commit, .gitignore or remove them")


CHECKS += (untracked,)


def lines(p, briefs=None, now=None):
    """The checks' hits, cached CACHE_S (a hook calls this on every Stop). A check that can't read its source is
    skipped, never a crash."""
    now = time.time() if now is None else now
    path = os.path.join(p.dir, "selfcheck.json")
    try:
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        if 0 <= now - float(d.get("at", 0)) < CACHE_S:
            return list(d.get("lines") or [])
    except (OSError, ValueError, TypeError, AttributeError):
        pass
    briefs = c.load_briefs(p) if briefs is None else briefs
    out = []
    for check in CHECKS:
        try:
            hit = check(p, briefs, now)
        except Exception:  # noqa: BLE001 — a check never costs the next action
            hit = None
        if hit:
            out.append(hit)
    try:
        c.write_atomic(path, json.dumps({"at": now, "lines": out}))
    except OSError:
        pass
    return out
