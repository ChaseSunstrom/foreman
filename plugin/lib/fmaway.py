"""T-1155: the return-after-gap summary (fm away; one line at session start after a long gap)."""
import os
import time

import fmcore as c

GAP = 2 * 3600  # seconds of silence from the user that counts as being away
MAX = 6         # lines per kind


def since(p, now=None, tail=4000):
    """(ts, gap seconds) of the last time the user spoke before a silence of GAP or more, else None. The silence runs
    to the next prompt, or to now for the latest: so a prompt typed on return (fm away itself) still finds the gap.
    T-2025: the live ledger's tail first, then one 4x wider, parsing prompt lines only (a silence sat 4,133 lines back
    on a busy day); consecutive prompts inside a tail bound a true silence, so only a tail without one scans every
    ledger file, and the cap keeps that case near the old cost."""
    now = now or time.time()
    path = os.path.join(p.dir, "ledger.jsonl")
    for n in (tail, tail * 4):
        rows = c._tail_rows(path, n, keep=('"prompt"',))
        gap = _newest_gap([e for e in rows if isinstance(e, dict) and e.get("event") == "prompt"], now)
        if gap:
            break
    return gap or _newest_gap(c.ledger_events(p, ("prompt",)), now)


def _newest_gap(events, now):
    stamps = sorted(t.timestamp() for e in events if (t := c.parse_ts(e.get("ts"))))
    for i in range(len(stamps) - 1, -1, -1):
        end = stamps[i + 1] if i + 1 < len(stamps) else now
        if end - stamps[i] >= GAP:
            return c.iso(stamps[i]), end - stamps[i]
    return None


def summary(p, ts, titles=True):
    """[(kind, line)] of what closed, blocked, was asked (and still waits) or was reverted after ts; titles=False
    skips the brief lookup per closed task (the session-start line only counts)."""
    def title(tid):
        b = c.find_brief(p, tid) if tid and titles else None
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
        if (t := fmoutcomes._ts(at)) and c.iso(t.timestamp()) > ts:
            rows.append(("reverted", f"{', '.join(sorted(tasks)) or '-'}: {c.fit(subj, 100)}"))
    return rows


def returned(p, n=500):
    """T-2008: the away line for the prompt just logged, when the prompt before it came GAP or more earlier; else "".
    Reads the ledger's tail; only when the previous prompt is further back does it scan the whole ledger."""
    rows = c.ledger_tail(p, n)
    at = [i for i, e in enumerate(rows) if e.get("event") == "prompt" and c.parse_ts(e.get("ts"))]
    if any(e.get("event") == "session_start" and (e.get("data") or {}).get("source") in ("startup", "resume")
           for e in rows[at[-2] if len(at) > 1 else 0:at[-1] if at else 0]):
        return ""  # this session's start already carried the line
    stamps = [c.parse_ts(rows[i].get("ts")).timestamp() for i in at]
    if len(stamps) >= 2:
        gap = stamps[-1] - stamps[-2]
        return line(p, (c.iso(stamps[-2]), gap)) if gap >= GAP else ""
    s = since(p, stamps[-1]) if stamps else None
    ended = s and abs(c.parse_ts(s[0]).timestamp() + s[1] - stamps[-1]) < 2  # since() may find an older silence
    return line(p, s) if ended else ""


def line(p, s=None):
    """One session-start line, or "" after a short gap or when nothing happened. s: since()'s (ts, gap) when known."""
    s = s or since(p)
    if not s:
        return ""
    rows = summary(p, s[0], titles=False)
    n = {k: sum(1 for kk, _ in rows if kk == k) for k in ("closed", "blocked", "asked", "reverted")}
    parts = [f"{v} {k}" for k, v in n.items() if v]
    ids = list(dict.fromkeys(r.split(":")[0].split(" ")[0] for _, r in rows if r.startswith("T-")))[-6:]  # newest last
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
