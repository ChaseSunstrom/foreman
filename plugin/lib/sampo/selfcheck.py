"""T-3127: self-checks: what the user would otherwise have to point out, named with its numbers before they ask. On
2026-11-06 they asked, one message each: why landed work hadn't reached GitHub in 22 hours, why a retired .foreman/
was tracked beside .sampo/, and why pages they had asked for weren't done, then "I shouldn't even need to send any of
the messages". Each check reads state and at most one git call; lines() caches the set CACHE_S per project, and
next_for (sampo next and the drive's line) shows it in every state, not only when idle."""
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


CHECKS = (unshipped, old_mirror, asks_waiting)


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
