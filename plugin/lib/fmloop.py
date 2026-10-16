"""fm loop (T-1057): Foreman improves itself without end. With the loop on, an empty queue starts a round instead of
ending the run: fm next names it and the Stop drive continues into it. A round reviews what shipped since the last one,
brainstorms past the newest earlier ones, grounds and queues what survives, and builds it; fm loop yield N records how
many grounded ideas it queued, and two dry rounds in a row (fewer than DRY_YIELD each) end the loop with a decision on
record. Enforced by fm next and the drive, so no session has to remember to do it: a round left without a yield is
counted by Foreman (the tasks made since it started) when the next one starts."""
import glob
import os
import shlex

import fmcore as c

DRY_YIELD = 3  # a round that queues fewer grounded ideas than this is dry
DRY_STOP = 2   # dry rounds in a row that end the loop
SEEN_MAX = 6   # ponytail: the newest earlier brainstorms only (each carries 300+ titles, all of them would swamp every
# lens's prompt); an older idea that comes back is caught at grounding, where ideas.md marks it near the finished task


def state(p):
    s = c.read_meta(p).get("loop")
    return s if isinstance(s, dict) else {}


def on(p):
    return bool(state(p).get("on"))


def action(p):
    """What fm next says with the queue and inbox empty and the loop on."""
    s = state(p)
    dry = f", {s['dry']} dry so far" if s.get("dry") else ""
    nxt = " --next" if is_open(s) else ""  # T-1153: a drained open round is ended explicitly; a plain call re-reads it
    return (f"forever loop round {int(s.get('round') or 0) + 1}{dry}: fm loop round{nxt}, then follow it (review what shipped, "
            f"brainstorm past the newest earlier runs, ground, queue, build); fm loop off stops it")


def seen(p):
    files = sorted(glob.glob(os.path.join(p.dir, "research", "brainstorm-*", "ideas.md")))
    return files[-SEEN_MAX:]


def shipped(p, since):
    """Tasks closed done since `since` (an ISO time; everything when empty), newest first, and the commits since."""
    t0 = c.parse_ts(since) if since else None
    at = lambda b: c.parse_ts(b.meta.get("updated"))  # review: an unreadable time is never "since"
    done = [b for b in c.load_briefs(p) if b.status == "done" and (not t0 or (at(b) and at(b) >= t0))]
    done.sort(key=lambda b: str(b.meta.get("updated") or ""), reverse=True)
    commits = []
    if since:  # Foreman's git runner: no traceback without git, no GIT_DIR pointing elsewhere
        r = c._git(p.root, "log", "--oneline", f"--since={since}", "-n", "40", timeout=20, proc=True)
        commits = r.stdout.splitlines() if r.returncode == 0 else []
    return done, commits


def made_since(p, since):
    """How many tasks were made since `since`: a round's yield when nobody recorded one."""
    t0 = c.parse_ts(since)
    return sum(1 for b in c.load_briefs(p) if t0 and (c.parse_ts(b.meta.get("created")) or t0) >= t0 and b.meta.get("created")) if t0 else 0


def is_open(s):
    """A round has started and has no yield yet."""
    return bool(s.get("round")) and s.get("yielded") is None


def round_brief(p, advance=False):
    """Start the next round: mark it and say what to do in it. While a round is open (no yield yet) a plain call shows
    that round's brief again (T-1153: re-reading it counted the round dry and started another); with advance, the open
    round is counted first (the tasks made since it started), so the dry stop never depends on the session remembering
    fm loop yield; when that ends the loop, None."""
    s = state(p)
    if is_open(s) and not advance:
        return _brief(p, int(s["round"]), s.get("since", s.get("started") or ""))
    if is_open(s):
        s, stop = record_yield(p, made_since(p, s.get("last")))
        if stop:
            return None
    n = int(s.get("round") or 0) + 1
    since = s.get("last") or s.get("started") or ""
    s.update(round=n, last=c.now(), since=since, yielded=None)
    c.update_meta(p, loop=s)
    return _brief(p, n, since)


def _brief(p, n, since):
    done, commits = shipped(p, since)
    seen_args = " ".join(f"--seen {shlex.quote(f)}" for f in seen(p))
    lines = [f"Forever loop, round {n}" + (f" (shipped since {since[:16]})" if since else "") + ".", "",
             "Shipped since the last round:"]
    lines += [f"- {b.id} {b.title}" for b in done[:25]] or ["- nothing closed since the last round"]
    if len(done) > 25:
        lines.append(f"- … {len(done) - 25} more")
    if commits:
        lines += ["", f"Commits ({len(commits)}):"] + [f"- {x}" for x in commits[:15]]
    lines += ["", "Do, in order:",
              "1. Review what shipped above as its user would: what is weak, missing, slow or confusing now.",
              f"2. fm mission --request \"forever loop round {n}: improve past everything shipped\", add the review to "
              "the pack, then:",
              f"   fm ideas --pack <pack> --rounds 2 --deepen 2 {seen_args}".rstrip(),
              "3. Cluster and ground every idea against the code (fm-recon for a big set); keep what is real and new.",
              "4. Queue every grounded idea with one fm intake block, then work the queue.",
              f"5. fm loop yield <how many you queued> — fewer than {DRY_YIELD} is a dry round; {DRY_STOP} dry rounds "
              "in a row end the loop."]
    return "\n".join(lines)


def record_yield(p, n):
    """Record a round's grounded yield; the second dry round in a row turns the loop off, with a decision on record."""
    s = state(p)
    s["dry"] = int(s.get("dry") or 0) + 1 if n < DRY_YIELD else 0
    s["yielded"] = n
    hist = (s.get("history") or [])[-19:]
    s["history"] = hist + [{"round": s.get("round"), "yield": n, "at": c.now()}]
    stop = s["dry"] >= DRY_STOP
    if stop:
        s.update(on=False, reason=f"{DRY_STOP} dry rounds in a row")
    c.update_meta(p, loop=s)
    if stop:
        import fmcli
        fmcli._write_decision(p, f"forever loop off after round {s.get('round')}: {DRY_STOP} dry rounds in a row",
                              why=f"the last rounds queued fewer than {DRY_YIELD} grounded ideas each")
    return s, stop


def view(p):
    """The loop for fm ui: on, round, dry streak."""
    s = state(p)
    return {"on": bool(s.get("on")), "round": int(s.get("round") or 0), "dry": int(s.get("dry") or 0)} if s else None


def cmd_loop(args):
    import fmcli
    p = fmcli.resolve(args)
    act = args.action or "status"
    if act == "on":
        s = state(p)
        s.update(on=True, started=s.get("started") if s.get("on") else c.now(), dry=0, reason=None)
        c.update_meta(p, loop=s)
        return fmcli.out(args, view(p), "Forever loop: on. When the queue and inbox are empty, fm next starts the next "
                         "round; two dry rounds in a row, the budget or fm loop off end it.")
    if act == "off":
        s = state(p)
        s.update(on=False, reason="turned off")
        c.update_meta(p, loop=s)
        return fmcli.out(args, view(p), "Forever loop: off.")
    if act == "round":
        if not on(p):
            raise fmcli.UsageError("the forever loop is off: fm loop on first")
        brief = round_brief(p, advance=args.next)
        if brief is None:
            s = state(p)
            return fmcli.out(args, view(p), f"Forever loop: off ({s.get('reason')}); round {s.get('round')} queued "
                             f"{s.get('yielded')}.")
        return fmcli.out(args, {"brief": brief, **(view(p) or {})}, brief)
    if act == "yield":
        if args.n is None or args.n < 0:
            raise fmcli.UsageError("fm loop yield N: how many grounded ideas this round queued")
        s = state(p)
        if not s.get("round"):
            raise fmcli.UsageError("no round has started: fm loop round first")
        if s.get("yielded") is not None:
            raise fmcli.UsageError(f"round {s['round']} already has its yield ({s['yielded']}); fm loop round starts "
                                   "the next")
        s, stop = record_yield(p, args.n)
        return fmcli.out(args, view(p), f"Round {s.get('round')}: {args.n} queued"
                         + (f"; {s['dry']} dry in a row" if s.get("dry") else "")
                         + (f". Forever loop: off ({s['reason']})." if stop else ". Forever loop: on."))
    s = state(p)
    text = ("Forever loop: on" if s.get("on") else "Forever loop: off") + (
        f" · round {s.get('round') or 0}" + (f" · {s['dry']} dry" if s.get("dry") else "")
        + (f" · {s['reason']}" if not s.get("on") and s.get("reason") else "") if s else "")
    return fmcli.out(args, view(p) or {"on": False}, text)
