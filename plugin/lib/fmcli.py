"""fm — the only writer of Foreman state.

Exit codes: 0 ok · 1 usage error / not found · 2 refused by policy · 3 lock timeout · 4 state corrupt.
"""
import argparse
import json
import os
import re
import sys

import fmcore as c

EDITABLE = {"type", "tier", "priority", "scope", "depends_on", "source", "status", "branch", "explore", "approved", "title"}
LIST_FIELDS = {"scope", "depends_on"}
SETTABLE_STATUS = {"captured", "planned", "active", "verifying", "blocked", "deferred"}


class UsageError(Exception):
    """Bad input or unknown object. Exit code 1."""


def session():
    return c.session_id()


def out(args, data, text):
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2, ensure_ascii=False))
    elif text is not None:
        print(text)


# ---------------------------------------------------------------- project resolution

def resolve(args, create=True):
    if getattr(args, "project", None):
        p = c.project_by_slug(args.project)
        if not p:
            raise UsageError(f"unknown project {args.project!r} (see state/registry.md)")
        return p
    p = c.find_project(os.getcwd(), create=create)
    if not p and os.environ.get("FOREMAN_PROJECT"):
        p = c.project_by_slug(os.environ["FOREMAN_PROJECT"])
    if not p:
        raise UsageError("not in a Foreman project; run `fm init` here or pass -p SLUG")
    return p


def need_brief(p, tid):
    b = c.find_brief(p, tid)
    if not b:
        raise UsageError(f"no task {tid} in {p.slug}")
    return b


def mutate(p, tid, fn, event, data=None):
    """Load a brief under the project lock, apply fn(brief), save, log, regenerate views."""
    with c.lock(p.dir):
        b = need_brief(p, tid)
        result = fn(b)
        c.save_brief(p, b)
        c.log_event(p, event, task=b.id, data=data or {}, session=session())
        c.regen_views(p)
    return b, result


# ---------------------------------------------------------------- commands

def cmd_init(args):
    path = os.path.abspath(args.path or os.getcwd())
    root = c.git_root(path) or path
    p = c.init_project(root)
    if args.sensitive:
        cmd_sensitive(argparse.Namespace(state="on", path=root, json=False, project=None))
    with c.lock(p.dir):
        c.log_event(p, "init", data={"root": root}, session=session())
        c.regen_views(p)
    out(args, {"project": p.slug, "root": root}, p.slug)


def cmd_state(args):
    p = resolve(args)
    sd = c.state_dict(p)
    if args.line:
        print(c.state_line(sd))
    elif args.json:
        print(json.dumps(sd, indent=2, ensure_ascii=False))
    else:
        text = c.render_state(sd)
        if args.brief:
            text = "\n".join(text.splitlines()[:15])
        print(text.rstrip("\n"))


def _raw_with_block(item, r):
    lines = [item.raw.strip() or f"{item.type}: {item.text}"]
    lines += [f"CONTEXT: {v}" for v in r.context]
    lines += [v if v.startswith(("MUST:", "NEVER:")) else f"CONSTRAINT: {v}" for v in r.constraints]
    lines += [f"DONE-WHEN: {v}" for v in r.done_when]
    lines += [f"SKIP: {v}" for v in r.skip]
    return "\n".join(lines)


def _create(p, title, type, tier, status, raw=None, scope=(), depends=(), source="user", priority="normal", explore=False):
    tid = c.next_id(p)
    b = c.Brief.new(tid, title, type, tier, raw=raw, scope=scope, depends=depends, source=source,
                    priority=priority, status=status, explore=explore)
    c.save_brief(p, b, touch=False)
    return b


def _title(text):
    first = text.strip().splitlines()[0] if text.strip() else "untitled"
    first = c._SCOPE_RE.sub("", c._REF_RE.sub("", first)).strip()
    return (first[:1].upper() + first[1:])[:90] or "untitled"


def cmd_intake(args):
    text = args.text if args.text is not None else (open(args.file).read() if args.file else sys.stdin.read())
    r = c.parse_intake(text)
    p = resolve(args)
    created = []
    with c.lock(p.dir):
        for item in r.items:
            b = _create(p, _title(item.text), item.type, c.guess_tier(item.type, item.text), "captured",
                        raw=_raw_with_block(item, r), scope=item.scopes, depends=item.refs,
                        priority="urgent" if item.urgent else "normal", explore=item.explore)
            if r.skip:
                b.set_section("Non-goals", "".join(f"- {s}\n" for s in r.skip))
                c.save_brief(p, b, touch=False)
            created.append(b)
        c.log_event(p, "intake", data={"created": [b.id for b in created], "overrides": r.overrides,
                                       "untagged": bool(r.untagged)}, session=session())
        c.regen_views(p)
    order = sorted(created, key=lambda b: (0 if b.priority == "urgent" else 1, c.RANK.get(b.type, 99), c.id_num(b.id)))
    data = {"created": [c.brief_summary(b) for b in created], "order": [c.brief_summary(b) for b in order],
            "context": r.context, "constraints": r.constraints, "done_when": r.done_when, "skip": r.skip,
            "untagged": r.untagged, "overrides": r.overrides}
    lines = [f"Captured {len(created)} item(s). Canonical order:"] + \
            [f"  {b.id} [{b.type}{'!' if b.priority == 'urgent' else ''}{'?' if b.meta.get('explore') else ''} {b.tier}] {b.title}"
             for b in order]
    if r.untagged:
        lines.append(f"Untagged text (classify it yourself): {r.untagged[:200]}")
    out(args, data, "\n".join(lines))


def cmd_capture(args):
    if args.self_:
        home = c.foreman_home()
        p = c.find_project(home, create=True) or c.init_project(home)
    else:
        p = resolve(args)
    type_ = (args.type or "FEATURE").upper()
    type_ = c.WORK_TAGS.get(type_, type_)
    if type_ not in c.TYPES:
        raise UsageError(f"unknown type {args.type!r}; one of {', '.join(c.TYPES)}")
    with c.lock(p.dir):
        b = _create(p, _title(args.text), type_, args.tier or c.guess_tier(type_, args.text), "captured",
                    raw=args.text, scope=args.scope or (), source=args.source,
                    priority="urgent" if args.urgent else "normal")
        c.log_event(p, "capture", task=b.id, data={"source": args.source, "type": type_}, session=session())
        c.regen_views(p)
    out(args, c.brief_summary(b), f"Captured as {b.id} [{b.type}, {b.tier}] (source: {args.source}).")


def cmd_task(args):
    p = resolve(args)
    sub = args.task_cmd
    if sub == "new":
        return task_new(p, args)
    if sub == "show":
        b = need_brief(p, args.id)
        if args.json:
            return print(json.dumps(dict(c.brief_summary(b), meta=b.meta, blockers=b.done_blockers()), indent=2))
        return print(b.render(), end="")
    if sub == "set":
        return task_set(p, args)
    if sub == "step":
        return task_step(p, args)
    if sub == "ac":
        return task_ac(p, args)
    if sub == "log":
        b, _ = mutate(p, args.id, lambda b: b.append_log(args.text), "note", {"text": args.text[:300]})
        return out(args, c.brief_summary(b), f"{b.id}: logged.")
    if sub == "evidence":
        b, _ = mutate(p, args.id, lambda b: b.add_evidence(args.cmd, args.result, step=args.step, ac=args.ac),
                      "evidence", {"step": args.step, "ac": args.ac, "cmd": args.cmd, "result": args.result[:300]})
        return out(args, c.brief_summary(b), f"{b.id}: evidence recorded.")
    if sub == "audit":
        if args.lens not in c.AUDIT_LENSES:
            raise UsageError(f"unknown lens {args.lens!r}; one of {', '.join(c.AUDIT_LENSES)}")
        tree = c.worktree_id(p.root)
        b, _ = mutate(p, args.id, lambda b: b.add_audit(args.lens, args.how, args.result, tree=tree),
                      "audit", {"lens": args.lens, "how": args.how[:200], "result": args.result[:300]})
        return out(args, c.brief_summary(b), f"{b.id}: audit ({args.lens}) recorded.")
    if sub == "done":
        import fmdocs
        since, tree = c.last_change(p, args.id), c.worktree_id(p.root)
        pre = need_brief(p, args.id)
        drift, notes = fmdocs.task_docs(p.root, pre.section("Docs impact")) if pre.tier in ("M", "L") else ([], [])

        def done(b):
            reasons = b.done_blockers(since, tree) + drift
            if reasons:
                raise c.PolicyError(f"{b.id} can't be marked done:\n  - " + "\n  - ".join(reasons))
            b.meta["status"] = "done"
            b.append_log("done")
        b, _ = mutate(p, args.id, done, "task_done")
        return out(args, dict(c.brief_summary(b), doc_drift=notes), f"{b.id} done." + (
            "\nDoc drift elsewhere (fm docs; not from this task):\n  - " + "\n  - ".join(notes[:10]) if notes else ""))
    if sub in ("block", "drop", "defer"):
        status = {"block": "blocked", "drop": "dropped", "defer": "deferred"}[sub]
        reason = getattr(args, "reason", None) or ""

        def change(b):
            b.meta["status"] = status
            b.append_log(f"{status}: {reason}" if reason else status)
        b, _ = mutate(p, args.id, change, f"task_{sub}", {"reason": reason})
        return out(args, c.brief_summary(b), f"{b.id} {status}." + (f" Reason: {reason}" if reason else ""))
    raise UsageError(f"unknown task subcommand {sub}")


def task_new(p, args):
    type_ = c.WORK_TAGS.get(args.type.upper(), args.type.upper())
    if type_ not in c.TYPES:
        raise UsageError(f"unknown type {args.type!r}")
    if args.tier not in ("S", "M", "L"):
        raise UsageError("tier must be S, M or L")
    with c.lock(p.dir):
        if args.from_id:
            b = need_brief(p, args.from_id)
            if b.status != "captured":
                raise UsageError(f"{b.id} is {b.status}, not captured")
            b.meta.update(type=type_, tier=args.tier, status="planned")
            if args.scope:
                b.meta["scope"] = args.scope
            if args.depends:
                b.meta["depends_on"] = args.depends
            b.preamble = f"# {args.title}\n"
            b.append_log("planned from capture")
            c.save_brief(p, b)
        else:
            b = _create(p, args.title, type_, args.tier, "planned", raw=args.raw, scope=args.scope or (),
                        depends=args.depends or (), source=args.source)
        c.log_event(p, "task_new", task=b.id, data={"type": type_, "tier": args.tier, "from": args.from_id},
                    session=session())
        c.regen_views(p)
    if args.ac or args.step:
        def plan(b):
            for text in args.ac or []:
                b.add_ac(text)
            for text in args.step or []:
                b.add_step(text)
        b, _ = mutate(p, b.id, plan, "task_plan", {"ac": len(args.ac or []), "step": len(args.step or [])})
    out(args, c.brief_summary(b), f"{b.id} [{b.type} {b.tier}] {b.title} — planned ({b.path})")
    if args.focus:
        cmd_focus(argparse.Namespace(id=b.id, project=getattr(args, "project", None), json=False))


def task_set(p, args):
    import fmguard
    for cat in args.allow or []:
        if cat in fmguard.USER_ONLY:
            raise c.PolicyError(f"{cat} can't be granted from the command line (whoever runs it); request it with "
                                f"`fm ask ID {cat} --why \"…\"` and the user's yes grants it")
        if cat not in fmguard.CATEGORIES or cat in fmguard.NOT_AUTHORIZABLE:
            raise UsageError(f"can't allow {cat!r}; authorizable: " + ", ".join(
                x for x in fmguard.CATEGORIES if x not in fmguard.NOT_AUTHORIZABLE | fmguard.USER_ONLY))
    changes = {}
    for kv in args.assignments:
        if "=" not in kv:
            raise UsageError(f"expected key=value, got {kv!r}")
        k, v = kv.split("=", 1)
        if k not in EDITABLE:
            raise UsageError(f"can't set {k!r}; editable: {', '.join(sorted(EDITABLE))} (authorizations via --allow)")
        if k == "status" and v not in SETTABLE_STATUS:
            raise UsageError(f"status {v!r} not settable here (use fm task done/drop, or one of {sorted(SETTABLE_STATUS)})")
        if k == "type":
            v = c.WORK_TAGS.get(v.upper(), v.upper())
            if v not in c.TYPES:
                raise UsageError(f"unknown type {v!r}")
        if k == "tier" and v not in ("S", "M", "L"):
            raise UsageError("tier must be S, M or L")
        if k == "priority" and v not in ("normal", "urgent"):
            raise UsageError("priority must be normal or urgent")
        changes[k] = [x.strip() for x in v.split(",") if x.strip()] if k in LIST_FIELDS else (v == "true" if k in ("explore", "approved") else v)
    section_text = None
    if args.section:
        section_text = args.text if args.text is not None else (open(args.file).read() if args.file else None)
        if section_text is None:
            raise UsageError("--section needs --text or --file")

    def apply(b):
        tiers = "SML"
        if "tier" in changes and changes["tier"] in tiers and b.tier in tiers and \
                tiers.index(changes["tier"]) < tiers.index(b.tier) and b.evidence():
            raise c.PolicyError(f"{b.id}: tier can't be lowered ({b.tier} → {changes['tier']}) once work has "
                                f"evidence; it sets which audits are required")
        for k, v in changes.items():
            if k == "title":
                b.preamble = f"# {v}\n"
            else:
                b.meta[k] = v
        for cat in args.allow or []:
            allow = list(b.meta.get("allow") or [])
            if cat not in allow:
                allow.append(cat)
            b.meta["allow"] = allow
            b.append_log(f"guard authorization added: {cat}")
        if args.section:
            b.set_section(args.section, c.redact(section_text))
        if changes:
            b.append_log("set " + ", ".join(f"{k}={v}" for k, v in changes.items()))
    b, _ = mutate(p, args.id, apply, "task_set", {"changes": changes, "allow": args.allow or [], "section": args.section})
    out(args, c.brief_summary(b), f"{b.id} updated.")


def task_step(p, args):
    if args.action == "add":
        b, n = mutate(p, args.id, lambda b: b.add_step(args.arg), "step_add", {"text": args.arg})
        return out(args, c.brief_summary(b), f"{b.id}: added step {n}.")
    try:
        n = int(args.arg)
    except ValueError:
        raise UsageError(f"step number expected, got {args.arg!r}")
    if args.action == "current":
        b, _ = mutate(p, args.id, lambda b: b.set_current(n), "step_current", {"step": n})
        return out(args, c.brief_summary(b), f"{b.id}: current step {n}.")
    ev = args.evidence

    def done(b):
        if ev:
            b.add_evidence(ev[0], ev[1], step=n)
        b.mark_step(n)
    b, _ = mutate(p, args.id, done, "step_done", {"step": n, "evidence": ev})
    s = c.brief_summary(b)
    nxt = f" Next: step {s['step']['n']}/{s['step']['of']} {s['step']['text']}" if s["step"] else " All steps done."
    out(args, s, f"{b.id}: step {n} done.{nxt}")


def task_ac(p, args):
    if args.action == "add":
        b, _ = mutate(p, args.id, lambda b: b.add_ac(args.arg, args.verify), "ac_add", {"text": args.arg})
        return out(args, c.brief_summary(b), f"{b.id}: criterion added.")
    try:
        n = int(args.arg)
    except ValueError:
        raise UsageError(f"criterion number expected, got {args.arg!r}")
    ev = args.evidence

    def check(b):
        if ev:
            b.add_evidence(ev[0], ev[1], ac=n)
        b.check_ac(n)
    b, _ = mutate(p, args.id, check, "ac_check", {"ac": n})
    out(args, c.brief_summary(b), f"{b.id}: criterion {n} checked.")


def cmd_focus(args):
    p = resolve(args)
    warn = None
    with c.lock(p.dir):
        target = need_brief(p, args.id)
        if target.status in c.CLOSED:
            raise UsageError(f"{target.id} is {target.status}")
        gaps = [] if target.status in ("active", "verifying") else \
            c.plan_gaps(target, c.read_meta(p).get("autonomy", "standard"))
        if gaps:
            raise c.PolicyError(f"{target.id} isn't planned enough to start: missing {', '.join(gaps)} "
                                f"(fm task set/ac/step, or /foreman:intake; fm next says what's next)")
        for b in c.load_briefs(p):
            if b.status in ("active", "verifying") and b.id != target.id:
                b.meta["status"] = "planned"
                b.append_log(f"paused: focus moved to {target.id}")
                c.save_brief(p, b)
        target.meta["status"] = "active"
        target.append_log("focused")
        c.save_brief(p, target)
        other = c.read_meta(p).get("session") or {}
        age = c.age_days(other.get("seen"))
        if other.get("id") and session() and other["id"] != session() and age is not None and age < 10 / 1440:
            warn = f"note: another Claude Code session ({other['id'][:8]}) was active in this project within 10 minutes"
        c.log_event(p, "focus", task=target.id, session=session())
        c.regen_views(p)
    if warn:
        print(warn, file=sys.stderr)
    out(args, c.brief_summary(target), f"Focus: {target.id} [{target.type} {target.tier}] {target.title}")


def cmd_checkpoint(args):
    p = resolve(args)
    with c.lock(p.dir):
        b = c.checkpoint(p, note=args.note, auto=args.auto, session=session())
    out(args, {"task": b.id if b else None}, f"Checkpoint saved{' for ' + b.id if b else ' (no active task)'}.")


def cmd_resume(args):
    p = resolve(args)
    r = c.resume_info(p)
    if not r["id"]:
        nxt = ", ".join(q["id"] for q in c.state_dict(p)["queue"][:3]) or "none"
        return out(args, r, f"No active task. Next in queue: {nxt}")
    step = f"step {r['step']['n']}/{r['step']['of']}: {r['step']['text']}" if r["step"] else f"{r['steps_done']}/{r['steps_total']} steps done"
    out(args, r, f"Resume {r['id']} [{r['type']} {r['tier']}] {r['title']} — {step}\n{r['resume']}\nBrief: {r['path']}")


def cmd_queue(args):
    p = resolve(args)
    briefs = c.load_briefs(p)
    order, cycles, dangling = c.order_queue(briefs)
    if args.replan:
        with c.lock(p.dir):
            c.log_event(p, "replan", data={"order": [b.id for b in order]}, session=session())
            c.regen_views(p, briefs)
    data = {"order": [c.brief_summary(b) for b in order], "cycles": cycles, "dangling": [list(d) for d in dangling]}
    lines = [f"{i}. {b.id} {b.type} {b.tier} [{b.status}]{' !' if b.priority == 'urgent' else ''} — {b.title}"
             for i, b in enumerate(order, 1)] or ["Queue empty."]
    if cycles:
        lines.append("Cycles: " + "; ".join(" ↔ ".join(x) for x in cycles))
    if dangling:
        lines.append("Dangling: " + ", ".join(f"{a}→{b}" for a, b in dangling))
    out(args, data, "\n".join(lines))


def cmd_log(args):
    p = resolve(args)
    try:
        data = json.loads(args.data) if args.data else {}
    except ValueError as e:
        raise UsageError(f"data must be JSON: {e}")
    if not isinstance(data, dict):
        data = {"value": data}
    rec = c.log_event(p, args.event, task=args.task, data=data, session=session())
    out(args, rec, None)


def cmd_sensitive(args):
    if args.path:
        root = c.git_root(args.path) or os.path.abspath(args.path)
        p = c.find_project(root) or c.init_project(root)
    else:
        p = resolve(args)
    path = os.path.join(p.root, ".claude", "settings.local.json")
    data = {}
    if os.path.exists(path):
        with open(path) as f:
            data = json.load(f)
    perms = data.setdefault("permissions", {})
    if args.state == "on":
        perms["defaultMode"] = "default"
    else:
        perms.pop("defaultMode", None)
        if not perms:
            data.pop("permissions")
    c.write_atomic(path, json.dumps(data, indent=2) + "\n")
    _git_exclude(p.root, ".claude/settings.local.json")
    c.update_meta(p, sensitive=args.state == "on")
    with c.lock(p.dir):
        c.log_event(p, "sensitive", data={"on": args.state == "on"}, session=session())
        c.regen_views(p)
    what = "new sessions here start in manual permission mode" if args.state == "on" else "user default mode applies again"
    out(args, {"sensitive": args.state == "on"}, f"{p.slug}: sensitive {args.state} ({what}).")


def _git_exclude(root, rel):
    """Keep a machine-local settings file out of commits without touching the repo's .gitignore."""
    excl = os.path.join(root, ".git", "info", "exclude")
    if not os.path.isdir(os.path.dirname(excl)):
        return
    try:
        cur = open(excl).read() if os.path.exists(excl) else ""
        if rel not in cur.split("\n"):
            with open(excl, "a") as f:
                f.write(("" if cur.endswith("\n") or not cur else "\n") + rel + "\n")
    except OSError:
        pass


def _take_seen_ask(p, tid, cats):
    """The record the PreToolUse hook made for this exact `fm ask` (consumed): session, and whether a dialog was
    raised for it. None when the hook didn't see it."""
    import time
    path = os.path.join(p.dir, "asks.json")
    try:
        with open(path) as f:
            seen = json.load(f)
    except (OSError, ValueError):
        return None
    match = next((a for a in reversed(seen) if isinstance(a, dict) and a.get("task") == tid
                  and sorted(set(a.get("allow") or [])) == sorted(set(cats))
                  and time.time() - a.get("at", 0) < c.ASK_TTL), None)
    if match:
        seen.remove(match)
        c.write_atomic(path, json.dumps(seen))
    return match


def _prompted(p, tid, cats):
    """A permission dialog was shown for this exact request (this command only runs once it was approved)."""
    try:
        with open(os.path.join(p.dir, "prompts.json")) as f:
            seen = json.load(f)
    except (OSError, ValueError):
        return False
    import time
    return any(isinstance(a, dict) and a.get("task") == tid and a.get("allow") == sorted(set(cats))
               and time.time() - a.get("at", 0) < c.APPROVAL_TTL for a in seen)


def cmd_ask(args):
    """Record a request only. The grant happens in the UserPromptSubmit hook, on the user's own reply."""
    import fmguard
    p = resolve(args)
    cats = list(dict.fromkeys(args.categories))
    bad = [x for x in cats if x not in fmguard.CATEGORIES or x in fmguard.NOT_AUTHORIZABLE]
    if bad:
        ok = [x for x in fmguard.CATEGORIES if x not in fmguard.NOT_AUTHORIZABLE]
        raise UsageError(f"can't ask for {', '.join(bad)}; askable: {', '.join(ok)}")
    why = c.redact(args.why)
    with c.lock(p.dir):
        b = need_brief(p, args.id)
        if _prompted(p, b.id, cats):
            return out(args, {"task": b.id, "allow": cats, "via": "prompt"},
                       f"Approved in Claude Code's permission prompt: the hook records the grant of {', '.join(cats)} "
                       f"for {b.id}.")
        seen = _take_seen_ask(p, b.id, cats)
        sid = seen and seen.get("session")
        if not sid:
            raise UsageError("fm ask must run as its own Bash command in the Claude Code session that asks: the hook "
                             "ties the request to that session (it saw no matching call, so nothing was recorded). "
                             "If it was its own command, state was busy: run the same fm ask again")
        meta = c.read_meta(p)
        pend = [a for a in meta.get("pending_approvals") or [] if a.get("task") != b.id]
        pend.append({"task": b.id, "allow": cats, "why": why, "session": sid, "at": c.now()})
        meta["pending_approvals"] = pend
        c.write_meta(p, meta)
        c.log_event(p, "approval_requested", task=b.id, data={"allow": cats, "why": why}, session=sid)
        c.regen_views(p)  # the statusline shows what a yes would grant
    reload = (" The user approved Claude Code's permission dialog, but this session hasn't loaded Foreman's "
              "PermissionRequest hook, so the dialog can't grant it: they should run /reload-plugins.") \
        if seen.get("dialog") else ""
    out(args, {"task": b.id, "allow": cats, "why": why},
        f"Pending: {b.id} {', '.join(cats)} ({why}).{reload} Ask the user one yes/no question for it now; their next "
        f"message decides: a reply starting with yes grants it, anything else cancels it.")


def cmd_decide(args):
    p = resolve(args)

    def cell(v):
        return c.redact((v or "").replace("|", "\\|").replace("\n", " ").strip())
    row = f"| {c.now()[:10]} | {cell(args.decision)} | {cell(args.why)} | {cell(args.rejected)} |\n"
    path = os.path.join(p.dir, "decisions.md")
    with c.lock(p.dir):
        cur = open(path, encoding="utf-8").read() if os.path.exists(path) else \
            "# Decisions\n\n| Date | Decision | Why | Alternatives rejected |\n|---|---|---|---|\n"
        c.write_atomic(path, cur + row)
        c.log_event(p, "decision", task=args.task, data={"decision": args.decision, "why": args.why,
                                                          "rejected": args.rejected}, session=session())
    out(args, {"decision": args.decision}, f"Decision recorded in {path}.")


def cmd_research(args):
    p = resolve(args)
    name = args.name[:-3] if args.name.endswith(".md") else args.name
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,80}", name):
        raise UsageError(f"research name must be a plain file name, got {args.name!r}")
    text = open(args.file, encoding="utf-8").read() if args.file else sys.stdin.read()
    path = os.path.join(p.dir, "research", name + ".md")
    with c.lock(p.dir):
        c.write_atomic(path, c.redact(text))
        c.log_event(p, "research", task=args.task, data={"name": name, "chars": len(text)}, session=session())
    out(args, {"path": path}, f"Saved {path}")


def cmd_drive(args):
    p = resolve(args)
    c.update_meta(p, drive=args.state == "on")
    with c.lock(p.dir):
        c.log_event(p, "drive", data={"on": args.state == "on"}, session=session())
        c.regen_views(p)
    out(args, {"drive": args.state == "on"}, f"{p.slug}: drive {args.state}.")


def cmd_next(args):
    b, st, action = c.next_for(resolve(args))
    out(args, {"task": b.id if b else None, "stage": st, "action": action}, f"Next: {action}")


def cmd_autonomy(args):
    p = resolve(args)
    if not args.level:
        level = c.read_meta(p).get("autonomy", "standard")
        return out(args, {"autonomy": level}, f"{p.slug}: autonomy {level}.")
    c.update_meta(p, autonomy=args.level)
    with c.lock(p.dir):
        c.log_event(p, "autonomy", data={"level": args.level}, session=session())
        c.regen_views(p)
    out(args, {"autonomy": args.level}, f"{p.slug}: autonomy {args.level}.")


def lazy(module, func):
    def run(args):
        return getattr(__import__(module), func)(args)
    return run


# ---------------------------------------------------------------- parser

class _Parser(argparse.ArgumentParser):
    """No abbreviated long options (subparsers inherit the class): `--allo core` must not slip past the guard."""

    def __init__(self, *args, **kw):
        kw["allow_abbrev"] = False
        super().__init__(*args, **kw)


def build_parser():
    ap = _Parser(prog="fm", description="Foreman state CLI (the only writer of Foreman state).")
    ap.add_argument("-p", "--project", help="project slug (default: from cwd, then $FOREMAN_PROJECT)")
    sp = ap.add_subparsers(dest="cmd", required=True)

    def add(name, fn, **kw):
        s = sp.add_parser(name, **kw)
        s.set_defaults(fn=fn)
        s.add_argument("--json", action="store_true", help="machine-readable output")
        s.add_argument("-p", "--project", default=argparse.SUPPRESS)
        return s

    s = add("init", cmd_init, help="register a project")
    s.add_argument("path", nargs="?")
    s.add_argument("--sensitive", action="store_true")

    s = add("state", cmd_state, help="print STATE")
    s.add_argument("--brief", action="store_true")
    s.add_argument("--line", action="store_true")

    s = add("intake", cmd_intake, help="parse an intake block into captured briefs")
    s.add_argument("text", nargs="?")
    s.add_argument("--file")

    s = add("capture", cmd_capture, help="capture a request to the inbox")
    s.add_argument("text")
    s.add_argument("--source", default="user", choices=["user", "discovered", "followup", "self"])
    s.add_argument("--type")
    s.add_argument("--tier", choices=["S", "M", "L"])
    s.add_argument("--scope", action="append")
    s.add_argument("--urgent", action="store_true")
    s.add_argument("--self", dest="self_", action="store_true", help="capture into Foreman's own project (self-improvement)")

    s = add("ask", cmd_ask, help="ask the user to authorize guard categories for a task; their next message decides")
    s.add_argument("id")
    s.add_argument("categories", nargs="+")
    s.add_argument("--why", default="")

    s = add("decide", cmd_decide, help="record a decision in decisions.md")
    s.add_argument("decision")
    s.add_argument("--why", default="")
    s.add_argument("--rejected", default="")
    s.add_argument("--task")

    s = add("research", cmd_research, help="save a research/recon summary into the project's research/")
    rsp = s.add_subparsers(dest="research_cmd", required=True)
    r = rsp.add_parser("add")
    r.add_argument("name")
    r.add_argument("--file")
    r.add_argument("--task")
    r.add_argument("--json", action="store_true")

    s = add("task", cmd_task, help="task operations")
    tsp = s.add_subparsers(dest="task_cmd", required=True)

    def tadd(name):
        t = tsp.add_parser(name)
        t.add_argument("--json", action="store_true")
        return t

    t = tadd("new")
    t.add_argument("title")
    t.add_argument("--type", required=True)
    t.add_argument("--tier", required=True)
    t.add_argument("--scope", action="append")
    t.add_argument("--depends", action="append")
    t.add_argument("--raw")
    t.add_argument("--source", default="user", choices=["user", "discovered", "followup", "self"])
    t.add_argument("--from", dest="from_id")
    t.add_argument("--ac", action="append", help="acceptance criterion (repeatable)")
    t.add_argument("--step", action="append", help="step (repeatable)")
    t.add_argument("--focus", action="store_true", help="focus it right away (the plan gate still applies)")
    t = tadd("show")
    t.add_argument("id")
    t = tadd("set")
    t.add_argument("id")
    t.add_argument("assignments", nargs="*")
    t.add_argument("--allow", action="append")
    t.add_argument("--section")
    t.add_argument("--text")
    t.add_argument("--file")
    t = tadd("step")
    t.add_argument("id")
    t.add_argument("action", choices=["add", "current", "done"])
    t.add_argument("arg")
    t.add_argument("--evidence", nargs=2, metavar=("CMD", "RESULT"))
    t = tadd("ac")
    t.add_argument("id")
    t.add_argument("action", choices=["add", "check"])
    t.add_argument("arg")
    t.add_argument("--verify")
    t.add_argument("--evidence", nargs=2, metavar=("CMD", "RESULT"))
    t = tadd("evidence")
    t.add_argument("id")
    t.add_argument("cmd")
    t.add_argument("result")
    g = t.add_mutually_exclusive_group()
    g.add_argument("--step", type=int)
    g.add_argument("--ac", type=int)
    t = tadd("audit")
    t.add_argument("id")
    t.add_argument("lens", help=", ".join(c.AUDIT_LENSES))
    t.add_argument("how")
    t.add_argument("result")
    t = tadd("log")
    t.add_argument("id")
    t.add_argument("text", help="a steer, scope change, decision or note; appended to the brief's Log")
    t = tadd("done")
    t.add_argument("id")
    for name in ("block", "drop"):
        t = tadd(name)
        t.add_argument("id")
        t.add_argument("reason")
    t = tadd("defer")
    t.add_argument("id")
    t.add_argument("reason", nargs="?")

    s = add("focus", cmd_focus, help="make a task the single active task")
    s.add_argument("id")

    s = add("checkpoint", cmd_checkpoint, help="flush the resume point into the brief and STATE")
    s.add_argument("--note")
    s.add_argument("--auto", action="store_true")

    add("resume", cmd_resume, help="print the resume point")

    s = add("queue", cmd_queue, help="ordered queue")
    s.add_argument("--replan", action="store_true")

    s = add("log", cmd_log, help="append a ledger event")
    s.add_argument("event")
    s.add_argument("data", nargs="?")
    s.add_argument("--task")

    s = add("sensitive", cmd_sensitive, help="mark a repo sensitive (manual permission mode there)")
    s.add_argument("state", choices=["on", "off"])
    s.add_argument("path", nargs="?")

    s = add("drive", cmd_drive, help="keep Claude working while the queue has unblocked work")
    s.add_argument("state", choices=["on", "off"])

    add("next", cmd_next, help="the one next required action (derived from the briefs)")

    s = add("autonomy", cmd_autonomy, help="standard (asks for L plans, ? items, approvals) or full (never asks mid-run)")
    s.add_argument("level", nargs="?", choices=["standard", "full"])

    s = add("tidy", lazy("fmtidy", "cmd_tidy"), help="hygiene (dry-run by default)")
    s.add_argument("--apply", action="store_true")
    s.add_argument("--all", action="store_true")
    s.add_argument("--plugins", action="store_true", help="also report plugin footprint (slow: runs claude plugin details)")

    s = add("doctor", lazy("fmdoctor", "cmd_doctor"), help="self-check")
    s.add_argument("--full", action="store_true")
    s.add_argument("--restore-state", action="store_true", help="move fallback state back to the default dir")

    s = add("ideas", lazy("fmideas", "cmd_ideas"), help="tool-less brainstorm children, one per lens, in parallel")
    s.add_argument("--pack", required=True, help="context pack file (- for stdin)")
    s.add_argument("--lens", action="append", help="repeatable; default: all six lenses")
    s.add_argument("--model", default="sonnet")
    s.add_argument("--timeout", type=int, default=300)

    s = add("serve", lazy("fmserve", "cmd_serve"),
            help="run Claude Code Remote Control here in the background (systemd user unit): [start|status|stop] [PATH]")
    s.add_argument("args", nargs="*", metavar="[ACTION] [PATH]")
    s.add_argument("--permission-mode", choices=c.PERMISSION_MODES)
    s.add_argument("--all", action="store_true", help="with stop: every fm serve unit")

    s = add("run", lazy("fmserve", "cmd_run"), help="work the queue in fresh claude -p sessions, one task each")
    s.add_argument("--max", type=int, default=10, help="tasks to finish before stopping")
    s.add_argument("--timeout", type=float, default=60, help="minutes per session")
    s.add_argument("--permission-mode", choices=c.PERMISSION_MODES)

    s = add("plugins", lazy("fmplugins", "cmd_plugins"),
            help="find plugins in the known marketplaces, check enabled ones for conflicts, install after approval")
    s.add_argument("action", choices=["find", "check", "install", "enable", "disable", "add-marketplace", "forget"])
    s.add_argument("words", nargs="*", help="find: what you need; check: one plugin id (default: all enabled); "
                                            "install/enable: one id (either installs it if missing, else enables "
                                            "it); add-marketplace: owner/repo, git URL or path; forget: an id to keep")

    s = add("docs", lazy("fmdocs", "cmd_docs"), help="report markdown that drifted from the repo")
    s.add_argument("path", nargs="?")
    s.add_argument("--strict", action="store_true", help="exit 1 when anything drifted")

    s = add("watch", lazy("fmwatch", "cmd_watch"), help="live dashboard")
    s.add_argument("--once", action="store_true")
    s.add_argument("--interval", type=float, default=1.0)

    s = add("install-user", lazy("fmsetup", "cmd_install"), help="wire Foreman into ~/.claude (used by install.sh)")
    s.add_argument("--dry-run", action="store_true")
    s.add_argument("--record-disabled", action="append", metavar="PLUGIN_ID",
                   help="record a plugin Foreman disabled (listed by uninstall.sh for re-enabling)")
    s = add("uninstall-user", lazy("fmsetup", "cmd_uninstall"), help="undo install-user from the manifest")
    s.add_argument("--dry-run", action="store_true")
    return ap


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        args.fn(args)
        return 0
    except c.PolicyError as e:
        print(f"fm: refused: {e}", file=sys.stderr)
        return 2
    except c.LockTimeout as e:
        print(f"fm: {e} (another fm or hook is writing; retry)", file=sys.stderr)
        return 3
    except (UsageError, KeyError) as e:
        print(f"fm: {e.args[0] if e.args else e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"fm: state looks corrupt: {e} (run fm doctor)", file=sys.stderr)
        return 4
