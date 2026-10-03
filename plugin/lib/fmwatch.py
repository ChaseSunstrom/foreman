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
    act = c.active_brief(briefs, p.lane)
    events = _tail_jsonl(os.path.join(c.state_dir(), "events.jsonl"))
    mine = [e for e in events if e.get("project") in (p.slug, None)]
    running = {}
    for e in events:
        if e.get("kind") == "subagent_start":
            running[e.get("agent_id")] = e
        elif e.get("kind") == "subagent_stop":
            running.pop(e.get("agent_id"), None)
    latency, series = {}, []
    for e in events[-2000:]:
        if e.get("kind") == "hook_ms" and isinstance(e.get("ms"), (int, float)):
            latency.setdefault(e.get("event"), []).append(e["ms"])
            series.append(e["ms"])
    touched, ledger = [], c.ledger_tail(p, 400)
    if act:
        for e in ledger:
            f = (e.get("data") or {}).get("file")
            if e.get("event") == "touched" and e.get("task") == act.id and f and f not in touched:
                touched.append(f)
    checks = next((e for e in reversed(ledger) if e.get("event") == "check_run"), None)
    return {"sd": sd, "active": act, "project": p, "latency": latency, "series": series[-40:], "touched": touched[-10:],
            "checks": checks,
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
        result, cmd = " ".join(str(d.get("result", "")).split()), " ".join(str(d.get("cmd", "")).split())
        mark = "✗" if result.startswith("✗") else "✓"  # T-0195: a red run isn't a tick
        text = f"{mark} {t} {what}: {c.fit(cmd, 60)} → {result}"
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


def typical(events):
    """Median minutes from first focus to done per "TYPE/TIER" with 3+ closed tasks, from the ledger: what a size word
    usually means in this project (T-0116)."""
    import statistics
    kind, start, took = {}, {}, {}
    for e in events:
        t, ev = e.get("task"), e.get("event")
        if ev == "task_new" and t:
            d = e.get("data") or {}
            kind[t] = f"{d.get('type')}/{d.get('tier')}"
        elif ev == "focus" and t:
            start.setdefault(t, e.get("ts"))
        elif ev == "task_done" and t in start and t not in took:
            a, b = c.parse_ts(start[t]), c.parse_ts(e.get("ts"))
            if a and b:
                took[t] = (b - a).total_seconds() / 60
    groups = {}
    for t, m in took.items():
        if t in kind:
            groups.setdefault(kind[t], []).append(m)
    return {k: round(statistics.median(v)) for k, v in groups.items() if len(v) >= 3}


def brainstorm(p):
    """The newest brainstorm (T-0124): while fm ideas runs, how many lens answers are in and the ideas so far; after,
    how many ideas and the first ones. None when the project has none. A run that never wrote ideas.md and started
    over an hour ago counts as stopped."""
    import re
    root = os.path.join(p.dir, "research")
    try:
        name = max(d for d in os.listdir(root) if d.startswith("brainstorm-") and os.path.isdir(os.path.join(root, d)))
    except (OSError, ValueError):
        return None
    d = os.path.join(root, name)
    try:
        with open(os.path.join(d, "status.json"), encoding="utf-8") as f:
            st = json.load(f)
    except (OSError, ValueError):
        st = {}
    answers = sorted(f for f in os.listdir(d) if f.endswith(".md") and f != "ideas.md")
    age_h = round((time.time() - os.path.getmtime(d)) / 3600, 1)  # T-0146: an old one folds to a line in the pane
    if os.path.exists(os.path.join(d, "ideas.md")):
        with open(os.path.join(d, "ideas.md"), encoding="utf-8") as f:
            body = f.read().split("## New ideas per lens")[0]
        ideas = [ln[2:].strip() for ln in body.splitlines() if ln.startswith("- ")]
        return {"name": name, "running": False, "answers": len(answers), "count": len(ideas), "ideas": ideas[:8],
                "age_h": age_h}
    ideas = []
    for a in answers:
        with open(os.path.join(d, a), encoding="utf-8") as f:
            ideas += [c.plain(t).strip() for t in re.findall(r"(?m)^\s*[-*]\s*\*\*(.+?)\*\*", f.read())]
    ideas = list(dict.fromkeys(ideas))
    running = (c.age_days(st.get("started")) or 1) * 24 < 1
    return {"name": name, "running": running, "answers": len(answers),
            "expected": len(st.get("lenses") or []) * int(st.get("rounds") or 1), "count": len(ideas), "ideas": ideas[:8],
            "age_h": age_h}


def view(p):
    """The `fm ui --json` view model (v1; its TS twin is mods/foreman-ui/types/index.d.ts): one snapshot for a
    surface to render, built from gather() so it shows what fm watch shows."""
    import fmdoctor
    d = gather(p)
    sd, act = d["sd"], d["active"]
    meta = c.read_meta(p)
    autonomy = sd["autonomy"]
    pending = c.pending_tasks(meta)
    briefs = c.load_briefs(p)
    by_id = {b.id: b for b in briefs}
    active = None
    if act:
        changed = c.last_change(p, act.id)
        prog = c.audit_progress(act, changed)
        active = dict(c.brief_detail(act), stage=c.stage(act, autonomy, changed), stages=list(c.STAGES),
                      audits={"done": prog["done"], "need": prog["required"]},
                      blockers=act.done_blockers(changed)[:6])
    events = c.ledger_tail(p, 5000)
    if active:
        focused = next((e.get("ts") for e in events if e.get("event") == "focus" and e.get("task") == act.id), None)
        active["on_task_s"] = round((c.age_days(focused) or 0) * 86400) if focused else None

    def item(s):
        b = by_id.get(s["id"])
        waits = c.waits_on_user(b, pending, autonomy) if b else None
        out = {"id": s["id"], "type": s["type"], "tier": s["tier"], "title": s["title"], "status": s["status"],
               "waits": waits, "steps_done": s["steps_done"], "steps_total": s["steps_total"],
               "age_days": round(c.age_days(s.get("created")) or 0, 1)}
        if waits == "plan approval":  # a yes is given where what it approves is shown
            d = c.brief_detail(b)
            out["plan"] = {"interpretation": c.plain(b.section("Interpretation").strip())[:600],
                           "approach": c.plain(b.section("Approach (options → choice → why)").strip())[:600],
                           "steps": d["steps"], "criteria": d["criteria"]}
        return out

    closed = sorted((b for b in briefs if b.status in c.CLOSED), key=lambda b: b.meta.get("updated") or "",
                    reverse=True)[:5]
    today = time.strftime("%Y-%m-%d", time.gmtime())  # closed today by the ledger, not "saved today" (any later edit)
    done_ids = {b.id for b in briefs if b.status == "done"}
    today_done = len({e.get("task") for e in events
                      if e.get("event") == "task_done" and str(e.get("ts") or "").startswith(today)} & done_ids)
    lat = [ms for vals in d["latency"].values() for ms in vals]
    bs = brainstorm(p)
    resume = meta.get("resume_after_reload") or None
    resume_age = c.age_days(resume.get("at")) if isinstance(resume, dict) else None
    return {
        "v": 1, "project": p.slug, "root": p.root,
        "mode": {"autonomy": autonomy, "drive": bool(sd["drive"]), "sensitive": bool(sd["sensitive"]),
                 "trust": bool(c.trusted()), "standing": sorted(meta.get("standing") or {})},
        "active": active,
        "next": c.plain(c.next_for(p, briefs)[2]),
        "queue": [item(s) for s in sd["queue"]][:20],
        "inbox": [item(s) for s in sd["inbox"]][:10], "inbox_total": len(sd["inbox"]),
        "approvals": [{"task": a.get("task"), "allow": list(a.get("allow") or []), "why": c.plain(a.get("why") or "")}
                      for a in meta.get("pending_approvals") or [] if isinstance(a, dict) and a.get("task")],
        "closed": [{"id": b.id, "status": b.status} for b in closed],
        "today_done": today_done,
        "trust_file": c.trust_path(),  # where /fm-trust on writes (the mod, never a tool call)
        # T-0145: a driven turn ended so a session's mod could reload; that mod starts the next turn (fresh ones only)
        "resume_after_reload": resume if resume_age is not None and resume_age * 1440 < 10 else None,
        "typical": typical(events),
        "brainstorm": bs,
        "recent": d["recent"],
        "health": {"hook_p95_ms": round(_pct(lat, 0.95)) if lat else None, "guard_blocks": len(d["guard"]),
                   "hook_errors": len(fmdoctor.recent_hook_errors()), "paused_hooks": fmdoctor.paused_hooks()},
        "watch": [p.dir, os.path.join(p.dir, "tasks"), os.path.join(p.dir, "ledger.jsonl")]
        + ([os.path.join(p.dir, "research", bs["name"])] if bs and bs["running"] else []),  # each lens answer moves it
        "latency": [round(ms) for ms in d["series"]],
        "checks": d["checks"] and {"at": d["checks"].get("ts"), "results": [
            {"cmd": c.plain(str(r.get("cmd")))[:200], "exit": r.get("exit"), "s": r.get("s"), "note": r.get("note")}
            for r in (d["checks"].get("data") or {}).get("results") or []]},
    }


def cmd_ui(args):
    """fm ui --json: the view model for the foreman-ui mod and any other surface; {"v": 1, "project": null} outside a
    project (never creates one)."""
    import fmcli
    try:
        p = fmcli.resolve(args, create=False)
    except fmcli.UsageError:
        p = None
    v = view(p) if p else {"v": 1, "project": None}
    if getattr(args, "json", False):
        print(json.dumps(v))
    else:
        a = v.get("active")
        print(f"{v['project'] or 'not a Foreman project'}" + (f" · {a['id']} {a['stage']}" if a else "")
              + (f"\nNext: {v['next']}" if v.get("next") else ""))
