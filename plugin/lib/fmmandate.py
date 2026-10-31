"""fm mandate (T-1400): a sweeping request kept as one standing record (its text, its clauses, an end date, a spend
bound) that fm scout and fm night read. While it stands, what scout captures says it was found under it; once it ends,
scout captures one decision (renew it or let it lapse) and nothing more under it until the user renews or clears it."""
import argparse
import time

import fmcore as c


def get(p):
    """The project's mandate with `expired` worked out, or None."""
    m = c.read_meta(p).get("mandate")
    if not isinstance(m, dict) or not m.get("text"):
        return None
    until = c.parse_ts(m.get("until"))  # a datetime, or None for a missing or damaged one (never ends)
    return dict(m, expired=bool(until and until.timestamp() <= time.time()))


def day(iso):
    """T-2135: the local day an until falls on, the day the user typed (it's stored as the end of that day in UTC, so
    its first 10 characters read a day late west of UTC); '?' for a missing or damaged one."""
    t = c.parse_ts(iso)
    return time.strftime("%Y-%m-%d", time.localtime(t.timestamp())) if t else "?"


def _archive(meta, status):
    """T-2135: a goal with items is kept in goal_history (the last 20) when anything replaces, overwrites or clears it."""
    old = meta.get("mandate")
    if isinstance(old, dict) and old.get("items"):
        meta["goal_history"] = (meta.get("goal_history") or [])[-19:] + [dict(old, status=status, replaced_at=c.now())]


def put(p, text, until, usd=None, status="overwritten"):
    """Set the mandate: text, its clauses (fm clauses), until (epoch seconds; None for a goal with no end date), an
    optional USD bound. An old goal with items is archived first (status says how it went)."""
    import fmrecall
    m = {"text": c.plain(text).strip(), "clauses": fmrecall.clauses(text)[:20], "until": c.iso(until) if until else None,
         "set_at": c.now(), **({"usd": usd} if usd is not None else {})}
    with c.lock(p.dir):
        meta = c.read_meta(p)
        _archive(meta, status)
        meta["mandate"] = m
        meta.pop("goal_verdict", None)  # T-2137: a verdict belongs to the goal it judged
        c.write_meta(p, meta)
    c.log_event(p, "mandate", data={"text": c.fit(m["text"], 200), "until": m["until"]})
    return m


def clear(p):
    with c.lock(p.dir):
        meta = c.read_meta(p)
        _archive(meta, "cleared")
        had = meta.pop("mandate", None)
        meta.pop("goal_verdict", None)
        c.write_meta(p, meta)
    return had


def lapse_finding(m):
    """The one decision an ended mandate leaves: a scout Finding keyed by when it was set, so it's captured once."""
    import fmscout
    return fmscout.Finding(f"mandate:{m.get('set_at')}", f"Mandate ended: {c.fit(m['text'], 90)}", "RESEARCH", "S",
                           f"the standing mandate set {day(m.get('set_at'))} ended {day(m.get('until'))}; "
                           "nothing more is captured under it. Decide: renew it (fm mandate set \"<text>\" --until "
                           "YYYY-MM-DD) or let it lapse (fm mandate off).")


def _until(day):
    import fmcli
    try:
        t = time.mktime(time.strptime(day, "%Y-%m-%d")) + 86400 - 1  # the end of that local day
    except (TypeError, ValueError):
        raise fmcli.UsageError(f"--until takes a date, YYYY-MM-DD, got {day!r}")
    if t <= time.time():
        raise fmcli.UsageError(f"--until {day} has already passed: give a later date")
    return t


def cmd_mandate(args):
    import fmcli
    p = fmcli.resolve(args)
    if args.action == "set":
        if not args.text or not args.until:
            raise fmcli.UsageError('fm mandate set "<the sweeping request>" --until YYYY-MM-DD [--usd N]')
        m = put(p, " ".join(args.text), _until(args.until), args.usd)
        return fmcli.out(args, m, f"Mandate set until {day(m['until'])}: {c.fit(m['text'], 120)} "
                                  f"({len(m['clauses'])} clause(s)); fm scout and fm night read it.")
    if args.action == "off":
        had = clear(p)
        return fmcli.out(args, {"cleared": bool(had)}, "Mandate cleared." if had else "No mandate was set.")
    m = get(p)
    if not m:
        return fmcli.out(args, {"mandate": None}, 'No mandate. fm mandate set "<request>" --until YYYY-MM-DD sets one.')
    if m.get("items") or not m.get("until"):  # T-2135: a goal speaks as one (read-only here: no checks run, exit 0)
        show(p, args, key="mandate", run=False)
        return 0
    state = "ended" if m["expired"] else "stands"
    return fmcli.out(args, {"mandate": m}, "\n".join(
        [f"Mandate {state} (until {day(m.get('until'))}): {m['text']}"] + [f"  - {x}" for x in m["clauses"][:10]]))


# T-2135: fm goal, the mandate grown into a ledger: items (text, source, a done-when check, the tasks that build it).
# One standing goal; --replace archives the old one under goal_history. Links are made, never inferred.
def standing(p):
    """The standing goal, or a UsageError saying why there's none to add to (an ended one is the user's to renew)."""
    import fmcli
    m = get(p)
    if not m:
        raise fmcli.UsageError('no goal stands: fm goal set "<the request>" [--until YYYY-MM-DD] [--usd N] sets one')
    if m["expired"]:
        raise fmcli.UsageError(f"the goal ended {day(m.get('until'))}; renewing or replacing it is the user's "
                               "call (T-2186): they run fm mandate set \"<text>\" --until YYYY-MM-DD, or fm mandate off")
    return m


def item(p, n):
    """Item n (1-based) of the standing goal, or a UsageError."""
    import fmcli
    items = standing(p).get("items") or []
    if not str(n).isdecimal() or not str(n).isascii() or not 1 <= int(n) <= len(items):
        raise fmcli.UsageError(f"the goal has no item {n} (it has {len(items)}): fm goal item TEXT --done-when CMD")
    return items[int(n) - 1]


def set_goal(p, text, until=None, usd=None, replace=False):
    import fmcli
    old = get(p)
    if old and old["expired"]:
        standing(p)  # raises: the user renews an ended goal
    if old and not replace:
        raise fmcli.UsageError(f"a goal stands ({c.fit(old['text'], 80)}): --replace archives it with its items")
    m = put(p, text, until, usd, status="replaced")
    c.log_event(p, "goal_set", data={"text": c.fit(m["text"], 200), "until": m["until"], "replaced": bool(old)})
    return m


def _locked_items(meta):
    import fmcli
    m = meta.get("mandate")
    if not isinstance(m, dict) or not m.get("text"):  # cleared since standing() looked
        raise fmcli.UsageError("no goal stands any more")
    return m.setdefault("items", [])


def add_item(p, text, done_when, source=None):
    import fmcli
    standing(p)
    done_when = c.plain(done_when or "").strip()
    if not done_when:
        raise fmcli.UsageError("--done-when needs a check command (an empty one would always pass)")
    fmcli._refuse_unrunnable(p, [done_when])
    fmcli.guard_stored(p, None, done_when)  # T-0901: refused now, not at the first fm goal show
    with c.lock(p.dir):
        meta = c.read_meta(p)
        items = _locked_items(meta)
        it = {"n": len(items) + 1, "text": c.plain(text).strip(), "source": c.plain(source or "").strip() or None,
              "done_when": done_when, "tasks": []}
        items.append(it)
        c.write_meta(p, meta)
    c.log_event(p, "goal_item", data={"n": it["n"], "text": c.fit(it["text"], 200)})
    return it


def link(p, n, tid):
    """Task tid builds item n: listed on the item, stamped goal: n on its brief."""
    import fmcli
    item(p, n)
    b = c.find_brief(p, tid)
    if not b:
        raise fmcli.UsageError(f"no task {tid}")
    with c.lock(p.dir):
        meta = c.read_meta(p)
        items = _locked_items(meta)
        for other in items:  # a task builds one item: a new link moves it
            other["tasks"] = [t for t in other["tasks"] if t != b.id]
        items[int(n) - 1]["tasks"].append(b.id)
        c.write_meta(p, meta)
    b.meta["goal"] = str(int(n))
    c.save_brief(p, b, touch=False)
    c.log_event(p, "goal_link", task=b.id, data={"item": int(n)})


CHECK_S, CHECKS_S = 300, 900  # one done-when check, and all of one show's together


def drift(p, m, run=True):
    """(outside, uncovered, unmet, unchecked): open tasks under way (not inbox captures) made since the goal was set
    that build no item; items with no task that still exists; items whose tasks all closed while their done-when fails,
    as (item, exit code or 'refused'); items whose check wasn't run (run=False, or past CHECKS_S). A check gets the
    guard's checks first (T-0901), as every stored command fm runs does."""
    import fmcli
    items = m.get("items") or []
    briefs = {b.id: b for b in c.load_briefs(p, include_archive=True)}
    linked = {t for it in items for t in it["tasks"]}
    outside = [b for b in briefs.values() if b.status not in c.CLOSED and b.status != "captured" and b.id not in linked
               and str(b.meta.get("created") or "") >= str(m.get("set_at") or "")]
    unmet, unchecked, deadline = [], [], time.monotonic() + CHECKS_S
    for it in items:
        mine = [t for t in it["tasks"] if t in briefs]
        if not mine or not all(briefs[t].status in c.CLOSED for t in mine):
            continue
        if not run or time.monotonic() >= deadline:
            unchecked.append(it)
            continue
        try:
            fmcli.guard_stored(p, None, it["done_when"])
        except c.PolicyError:
            unmet.append((it, "refused by the guard"))
            continue
        code, _ = c.run_command(p.root, it["done_when"], min(CHECK_S, max(1, deadline - time.monotonic())))
        if code != 0:
            unmet.append((it, f"exit {code}"))
    uncovered = [it for it in items if not any(t in briefs for t in it["tasks"])]
    return sorted(outside, key=lambda b: b.id), uncovered, unmet, unchecked


def show(p, args, key="goal", run=True):
    import fmcli
    m = get(p)
    if not m:
        return fmcli.out(args, {key: None}, 'No goal. fm goal set "<the request>" [--until YYYY-MM-DD] sets one.')
    if not m.get("items") and m.get("until"):  # a plain mandate prints as it always did
        return cmd_mandate(argparse.Namespace(**dict(vars(args), action="show")))
    outside, uncovered, unmet, unchecked = drift(p, m, run) if m.get("items") else ([], [], [], [])
    briefs = {b.id: b for b in c.load_briefs(p, include_archive=True)}
    state = "ended" if m["expired"] else "stands"
    when = f"until {day(m['until'])}" if m.get("until") else "no end date"
    money = f"budget ${m['usd']:g}" if m.get("usd") is not None else "no budget"
    lines = [f"Goal {state} ({when}, {money}): {m['text']}"] + [f"  - {x}" for x in m["clauses"][:10]]
    if m.get("items"):
        lines += ["Items:"] + [
            f"  {it['n']}. {it['text']}: " + (", ".join(f"{t} ({briefs[t].status if t in briefs else 'gone'})"
                                                         for t in it["tasks"]) or "no task")
            + f" · done when: {c.plain(it['done_when'])}" for it in m["items"]]
        lines += ["Drift: none." if not (outside or uncovered or unmet) else "Drift:"]
        if uncovered:
            lines += [f"  items with no task ({len(uncovered)}): " + "; ".join(f"{i['n']}. {i['text']}" for i in uncovered)]
        if outside:
            lines += [f"  outside the goal ({len(outside)}): " + "; ".join(f"{b.id} {c.fit(b.title, 60)}" for b in outside)]
        if unmet:
            lines += [f"  claimed, not met ({len(unmet)}): " + "; ".join(
                f"{i['n']}. {i['text']}: its tasks closed and its done-when fails ({how})" for i, how in unmet)]
        if unchecked:
            lines += [f"  closed, check not run ({len(unchecked)}; fm goal show runs them): "
                      + "; ".join(f"{i['n']}. {i['text']}" for i in unchecked)]
    fmcli.out(args, {key: m, "drift": {"outside": [b.id for b in outside], "uncovered": [i["n"] for i in uncovered],
                                       "unmet": [i["n"] for i, _ in unmet],
                                       "unchecked": [i["n"] for i in unchecked]}}, "\n".join(lines))
    return 1 if outside or uncovered or unmet else 0


def verdict(p, m):
    """T-2137: the causes a goal isn't finished (empty: finished). Reuses drift's guarded checks; deterministic."""
    import fmrecall
    items = m.get("items") or []
    briefs = {b.id: b for b in c.load_briefs(p, include_archive=True)}
    _, uncovered, unmet, unchecked = drift(p, m)
    causes = [] if items else ["the goal has no items"]
    causes += [f"item {i['n']} has no task" for i in uncovered]
    # an item is done when a linked task is done and none is open; dropped tasks don't count (T-2137)
    st = {i["n"]: [briefs[t].status for t in i["tasks"] if t in briefs] for i in items}
    causes += [f"item {i['n']} has open tasks" for i in items if any(s not in c.CLOSED for s in st[i["n"]])]
    causes += [f"item {i['n']} has no done task" for i in items
               if st[i["n"]] and all(s in c.CLOSED for s in st[i["n"]]) and "done" not in st[i["n"]]]
    causes += [f"item {i['n']} check fails ({how})" for i, how in unmet]
    causes += [f"item {i['n']} check not run" for i in unchecked]
    # a clause is accounted when an item (text, done-when, task titles) shares 2 of its words (1 if it has one)
    bags = [set(fmrecall.words(" ".join([i["text"], i["done_when"]] + [briefs[t].title for t in i["tasks"] if t in briefs])))
            for i in items]
    for x in m.get("clauses") or []:
        cw = set(fmrecall.words(x))
        if not any(len(cw & b) >= min(2, len(cw)) for b in bags):
            causes.append(f"clause unaccounted: {c.fit(x, 80)}")
    runs = c.ledger_events(p, kinds=["check_run"])
    last = runs[-1].get("data") or {} if runs else None
    if last is None:
        causes.append("gates never run (fm check)")
    elif last.get("tree") != c.worktree_id(p.root):
        causes.append("gates not run on this tree (fm check)")
    elif any((r or {}).get("exit") for r in last.get("results") or []):
        causes.append("gates red (fm check)")
    return causes


def cmd_verdict(p, args):
    import fmcli
    m = get(p)
    if not m or m["expired"]:
        c.update_meta(p, goal_verdict=None)
        fmcli.out(args, {"verdict": None}, "no goal")
        return 2  # finished is 0, stopped 1
    causes = verdict(p, m)
    word = "finished" if not causes else "stopped"
    # the tree is the worktree id; root lets Stop (which runs no git) tell another checkout's verdict from this one's
    c.update_meta(p, goal_verdict={"verdict": word, "causes": causes[:10], "at": c.now(),
                                   "tree": c.worktree_id(p.root) or "", "root": p.root,
                                   "set_at": m.get("set_at")})
    fmcli.out(args, {"verdict": word, "causes": causes}, word + (": " + "; ".join(causes) if causes else ""))
    return 1 if causes else 0


def cmd_goal(args):
    import fmcli
    p = fmcli.resolve(args)
    words = args.text or []
    if args.action == "verdict":
        return cmd_verdict(p, args)
    if args.action == "set":
        if not words or not (args.until or args.no_end):  # an endless goal is said so, never a default
            raise fmcli.UsageError('fm goal set "<the request>" --until YYYY-MM-DD | --no-end [--usd N] [--replace]')
        m = set_goal(p, " ".join(words), _until(args.until) if args.until else None, args.usd, args.replace)
        return fmcli.out(args, m, f"Goal set ({'until ' + day(m['until']) if m['until'] else 'no end date'}): "
                                  f"{c.fit(m['text'], 120)}; add its contents with fm goal item TEXT --done-when CMD.")
    if args.action == "item":
        if not words or not args.done_when:
            raise fmcli.UsageError('fm goal item "<what it covers>" --done-when "<check command>" [--source S]')
        it = add_item(p, " ".join(words), args.done_when, args.source)
        return fmcli.out(args, it, f"Item {it['n']}: {it['text']}; link its tasks with fm goal link {it['n']} ID "
                                   f"or fm task new … --goal {it['n']}.")
    if args.action == "link":
        if len(words) != 2:
            raise fmcli.UsageError("fm goal link ITEM TASK")
        link(p, words[0], words[1])
        return fmcli.out(args, {"item": int(words[0]), "task": words[1].upper()},
                         f"{words[1].upper()} builds item {words[0]}.")
    return show(p, args)
