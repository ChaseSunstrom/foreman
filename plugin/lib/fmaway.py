"""T-1155: the return-after-gap summary (fm away; one line at session start after a long gap)."""
import time

import fmcore as c

GAP = 2 * 3600  # seconds of silence from the user that counts as being away
MAX = 6         # lines per kind


def since(p, now=None):
    """(ts, gap seconds) of the last time the user spoke before a silence of GAP or more, else None. The silence runs
    to the next prompt, or to now for the latest: so a prompt typed on return (fm away itself) still finds the gap."""
    now = now or time.time()
    stamps = [t.timestamp() for e in c.ledger_events(p, ("prompt",)) if (t := c.parse_ts(e.get("ts")))]
    stamps = sorted(stamps)
    for i in range(len(stamps) - 1, -1, -1):
        end = stamps[i + 1] if i + 1 < len(stamps) else now
        if end - stamps[i] >= GAP:
            return c.iso(stamps[i]), end - stamps[i]
    return None


def summary(p, ts):
    """[(kind, line)] of what closed, blocked, was asked (and still waits) or was reverted after ts."""
    def title(tid):
        b = c.find_brief(p, tid) if tid else None
        return f"{tid} {c.fit(b.title, 60)}" if b else str(tid)
    pending = {a.get("q") for a in (c.read_meta(p).get("ask_digest") or {}).get("asks") or []}
    rows = []
    for e in c.ledger_events(p, ("task_done", "task_block", "ask_queued", "rollback"), since=ts):
        if str(e.get("ts")) <= ts:
            continue
        d, k = e.get("data") or {}, e.get("event")
        if k == "task_done":
            rows.append(("closed", title(e.get("task"))))
        elif k == "task_block":
            rows.append(("blocked", f"{e.get('task')}: {c.fit(str(d.get('reason') or ''), 100)}"))
        elif k == "ask_queued" and d.get("q") in pending:
            rows.append(("asked", f"{e.get('task') or '-'}: {c.fit(str(d.get('q')), 100)} (default {d.get('default')})"))
        elif k == "rollback":
            rows.append(("reverted", f"rolled back to snapshot {d.get('snapshot')}"))
    import fmoutcomes
    for at, subj, _, tasks in fmoutcomes.reverts(p):
        if (t := c.parse_ts(at)) and c.iso(t.timestamp()) > ts:
            rows.append(("reverted", f"{', '.join(sorted(tasks)) or '-'}: {c.fit(subj, 100)}"))
    return rows


def line(p):
    """One session-start line, or "" after a short gap or when nothing happened."""
    s = since(p)
    if not s:
        return ""
    rows = summary(p, s[0])
    n = {k: sum(1 for kk, _ in rows if kk == k) for k in ("closed", "blocked", "asked", "reverted")}
    parts = [f"{v} {k}" for k, v in n.items() if v]
    ids = sorted({r.split(":")[0].split(" ")[0] for _, r in rows if r.startswith("T-")})[:6]
    return (f"Away: {s[1] / 3600:.0f} h since you last spoke: {', '.join(parts)} ({' '.join(ids)}; fm away)"
            if parts else "")


def cmd_away(args):
    import fmcli
    p = fmcli.resolve(args)
    s = since(p)
    rows = summary(p, s[0]) if s else []
    lines = [f"Since you last spoke ({s[0]}, {s[1] / 3600:.0f} h of silence): {len(rows)} item(s)"] if s else \
        ["No gap of 2 h or more in your prompts yet (nothing to summarize)."]
    for kind in ("closed", "blocked", "asked", "reverted"):
        lines += [f"{kind.capitalize()}:"] + [f"- {r}" for k, r in rows if k == kind][-MAX:] if any(k == kind for k, _ in rows) else []
    fmcli.out(args, {"since": s and s[0], "items": [{"kind": k, "line": r} for k, r in rows]}, "\n".join(lines))
