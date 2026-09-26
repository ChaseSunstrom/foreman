"""fm watch: live Foreman dashboard (curses) and its plain-text twin (--once). Stdlib only, read-only."""
import json
import os
import statistics
import time

import fmcore as c


def _tail_jsonl(path, max_bytes=256 * 1024):
    try:
        with open(path, "rb") as f:
            f.seek(0, os.SEEK_END)
            f.seek(max(0, f.tell() - max_bytes))
            lines = f.read().decode("utf-8", "replace").splitlines()
    except OSError:
        return []
    out = []
    for line in lines:
        try:
            out.append(json.loads(line))
        except ValueError:
            continue
    return out


def _latest_session(project):
    d = os.path.join(c.state_dir(), "sessions")
    try:
        files = sorted((os.path.join(d, f) for f in os.listdir(d) if f.endswith(".json")), key=os.path.getmtime, reverse=True)
    except OSError:
        return None
    for path in files:
        try:
            with open(path) as f:
                snap = json.load(f)
        except (OSError, ValueError):
            continue
        if snap.get("project") in (project, None):
            return snap
    return None


def gather(p):
    briefs = c.load_briefs(p)
    sd = c.state_dict(p, briefs)
    act = c.active_brief(briefs)
    events = _tail_jsonl(os.path.join(c.state_dir(), "events.jsonl"))
    mine = [e for e in events if e.get("project") in (p.slug, None)]
    running = {}
    for e in events:
        if e.get("kind") == "subagent_start":
            running[e.get("agent_id")] = e
        elif e.get("kind") == "subagent_stop":
            running.pop(e.get("agent_id"), None)
    latency = {}
    for e in events[-2000:]:
        if e.get("kind") == "hook_ms" and isinstance(e.get("ms"), (int, float)):
            latency.setdefault(e.get("event"), []).append(e["ms"])
    touched, ledger = [], c.ledger_tail(p, 400)
    if act:
        for e in ledger:
            f = (e.get("data") or {}).get("file")
            if e.get("event") == "touched" and e.get("task") == act.id and f and f not in touched:
                touched.append(f)
    return {"sd": sd, "active": act, "project": p, "latency": latency, "touched": touched[-10:],
            "tools": [e for e in mine if e.get("kind") in ("tool", "tool_fail")][-12:],
            "subagents": list(running.values())[-5:], "guard": [e for e in mine if e.get("kind") == "guard_block"][-5:],
            "session": _latest_session(p.slug),
            "recent": [line for line in map(_recent, ledger) if line][-8:]}


def _recent(e):
    """One line for a ledger event worth seeing (evidence, audits, captures, decisions, approvals, done)."""
    d, t, ts = e.get("data") or {}, e.get("task") or "", (e.get("ts") or "")[11:16]
    kind = e.get("event")
    if kind == "evidence":
        what = f"step {d['step']}" if d.get("step") else f"criterion {d['ac']}" if d.get("ac") else "check"
        text = f"✓ {t} {what}: {d.get('cmd', '')} → {d.get('result', '')}"
    elif kind == "audit":
        text = f"◇ {t} audit {d.get('lens')}: {d.get('result', '')}"
    elif kind in ("capture", "intake"):
        text = f"⚑ {t} captured" if t else "⚑ intake"
    elif kind == "decision":
        text = f"◆ {d.get('decision', '')}"
    elif kind == "approval_requested":
        text = f"? {t} asked: {'+'.join(d.get('allow') or [])}"
    elif kind in ("approval_granted", "approval_declined"):
        text = f"{'✔' if kind == 'approval_granted' else '✖'} {t} {kind.split('_')[1]}"
    elif kind == "task_done":
        text = f"■ {t} done"
    else:
        return None
    return f"  {ts}  {text}"


def _pct(vals, q):
    vals = sorted(vals)
    return vals[min(len(vals) - 1, int(len(vals) * q))]


def render(d, width=100):
    sd, act, p = d["sd"], d["active"], d["project"]
    out = [f"Foreman · {p.slug} · {time.strftime('%H:%M:%S')}", ""]
    if act:
        a = sd["active"]
        out.append(f"Active: {a['id']} [{a['type']} {a['tier']}] {a['title']}")
        st = a.get("stage")
        out.append("  " + " → ".join(f"[{x}]" if x == st else x for x in c.STAGES)
                   + f" · audits {a['audits']['done']}/{a['audits']['required']}")
        out += [f"  [{'x' if s.done else ' '}] {s.n}. {s.text}{'  <-' if s.current else ''}" for s in act.steps()]
        out.append(f"  evidence: {len(act.evidence())} line(s)")
    else:
        out.append("Active: none")
    out.append(f"Queue ({len(sd['queue'])}): " + ("; ".join(f"{q['id']} {q['type']} {q['tier']}" for q in sd["queue"][:8]) or "empty"))
    out.append(f"Inbox ({len(sd['inbox'])}): " + ("; ".join(f"{q['id']} {q['title'][:30]}" for q in sd["inbox"][:5]) or "empty"))
    if sd.get("asks"):
        out.append("Waiting on you: reply yes = " + "; ".join(f"{'+'.join(x['allow'])} for {x['task']}"
                                                                for x in sd["asks"]))
    out += ["", "Recent:"] + (d["recent"] or ["  (nothing yet)"])
    out += ["", "Tool timeline:"]
    for e in d["tools"]:
        ms = f"{e['ms']}ms" if e.get("ms") is not None else "-"
        out.append(f"  {e.get('ts', '')[11:19]}  {e.get('tool', ''):<10} {'ok ' if e.get('ok') else 'ERR'} {ms:>8}  {e.get('target', '')}")
    if not d["tools"]:
        out.append("  (no tool calls yet)")
    out.append("Subagents: " + (", ".join(f"{e.get('agent_type')} ({e.get('agent_id')}) since {e.get('ts', '')[11:19]}"
                                            for e in d["subagents"]) or "none running"))
    out.append("Files touched: " + (", ".join(os.path.relpath(f, p.root) if f.startswith(p.root) else f
                                              for f in d["touched"]) or "none"))
    out.append("Guard blocks: " + ("; ".join(f"{e.get('ts', '')[11:19]} {e.get('category')} ({e.get('target', '')[:40]})"
                                             for e in d["guard"]) or "none"))
    out += ["", "Hook latency (ms):"]
    for ev, vals in sorted(d["latency"].items()):
        out.append(f"  {ev:<18} p50 {statistics.median(vals):>6.1f}  p95 {_pct(vals, 0.95):>6.1f}  n={len(vals)}")
    if not d["latency"]:
        out.append("  (no samples)")
    s = d["session"]
    if s:
        rl = ((s.get("rate_limits") or {}).get("five_hour") or {}).get("used_percentage")
        hit = s.get("cache_hit_ratio")
        out.append(f"Session: {s.get('model') or '?'} · ctx {s.get('context_pct')}% · ${s.get('cost_usd')}"
                   + (f" · 5h {rl}%" if rl is not None else "") + (f" · cache {int(hit * 100)}%" if hit is not None else ""))
    else:
        out.append("Session: no statusline snapshot yet")
    return [c.plain(line)[:width] for line in out]  # titles and events are user text: no terminal sequences


def cmd_watch(args):
    import fmcli
    p = fmcli.resolve(args)
    if args.once:
        print("\n".join(render(gather(p))))
        return
    import curses

    def loop(scr):
        curses.curs_set(0)
        scr.nodelay(True)
        while True:
            h, w = scr.getmaxyx()
            scr.erase()
            for i, line in enumerate(render(gather(p), w - 1)[:h - 1]):
                scr.addnstr(i, 0, line, w - 1)
            scr.addnstr(h - 1, 0, "q quits · refresh %.1fs" % args.interval, w - 1)
            scr.refresh()
            deadline = time.monotonic() + args.interval
            while time.monotonic() < deadline:
                if scr.getch() in (ord("q"), 27):
                    return
                time.sleep(0.05)
    try:
        curses.wrapper(loop)
    except KeyboardInterrupt:
        pass
