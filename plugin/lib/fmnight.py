"""fm night (T-0236): budgeted background work while the user is away — the daily second read of the last session,
the landscape scan when due, one research-debt question, the court of the user's steers, a bench tournament for one
kept fm evolve candidate — each an existing fm command, kept while the night's estimate fits --max-usd and today's
remaining budget. Refused when usage is high, when usage is unknown the limit halves, a sensitive project runs
nothing, and the night stops as soon as real spend passes the limit or usage climbs (T-0298 review). Never merges;
the morning's fm digest says what ran. Scheduling (cron, a systemd timer) is the user's to set up."""
import glob
import os
import subprocess
import sys
import time

import fmbudget
import fmcore as c
import fmserve

STALE_H = 12  # a statusline snapshot older than this says nothing about tonight's usage
JOB_TIMEOUT = 3 * 3600  # seconds one night job may take
NAMES = ("second session", "landscape", "research debt", "court", "evolve candidate")


def jobs(p):
    """[(name, fm argv, USD estimate)] of what tonight could do, cheapest and most useful first."""
    import fmbench
    import fmoutside
    meta, out = c.read_meta(p), []
    if meta.get("second_session") != c.now()[:10]:
        out.append(("second session", ["second", "session", "--if-due"], fmbudget.estimate("second-session", 1, 0.05)))
    age = c.age_days(meta.get("landscape_at"))
    if age is None or age >= fmoutside.LANDSCAPE_DAYS:
        out.append(("landscape", ["landscape", "--if-due"], fmbudget.estimate("research", 4, 0.2)))
    events = c.ledger_tail(p, 5000)
    asked = {e.get("task") for e in events if e.get("event") == "research"}
    debt = next((b for b in c.rank_inbox(c.load_briefs(p)) if b.type == "RESEARCH" and b.id not in asked), None)
    if debt:  # the oldest research question nobody has asked yet: one a night
        out.append(("research debt", ["research", "ask", c.fit(debt.title, 300), "--task", debt.id],
                    fmbudget.estimate("research", 4, 0.2)))
    if fmbench.court_cases(p, 3)[0]:
        est = fmbudget.estimate("bench", 3, 0.5)
        out.append(("court", ["bench", "court", "--max", "3", "--budget", f"{max(0.1, est / 3):.2f}"], est))
    benched = {str((e.get("data") or {}).get("old", "")) for e in events if e.get("event") == "bench_versions"}
    cand = next((d.get("branch") for e in reversed(events) if e.get("event") == "evolve"
                 for d in [e.get("data") or {}] if d.get("kept") and d.get("branch")
                 and not any(str(d["branch"]) in b for b in benched)), None)
    if cand:  # a kept candidate nobody has raced yet against this Foreman
        est = fmbudget.estimate("bench", 4, 0.5)
        out.append((f"evolve candidate {cand}", ["bench", "versions", cand, "--max", "2", "--budget",
                                                 f"{max(0.1, est / 4):.2f}"], est))
    return out


def _usage():
    """(why usage is high, or None; whether it is known): a snapshot older than STALE_H hours is not knowledge."""
    snaps = glob.glob(os.path.join(c.state_dir(), "sessions", "*.json"))
    fresh = any(time.time() - os.path.getmtime(s) < STALE_H * 3600 for s in snaps)
    return fmbudget.usage_high(), fresh


def cmd_night(args):
    import fmcli
    p = fmcli.resolve(args)
    if c.panicked():
        raise c.PolicyError(c.PAUSED)
    if not getattr(args, "dry_run", False):
        try:  # T-0452: standing orders capture their tasks (no session runs, so no spend)
            import fmorders
            fmorders.run(p)
        except Exception as e:  # an order file never costs the night
            print(f"fm: warning: standing orders: {e}", file=sys.stderr)
    bad = [n for n in args.only or [] if n not in NAMES]
    if bad:
        raise fmcli.UsageError(f"no such night job: {', '.join(bad)} (jobs: {', '.join(NAMES)})")
    high, known = _usage()
    if high:
        raise fmcli.UsageError(f"usage is high ({high}): nothing runs tonight — the user's own work comes first")
    if not args.max_usd >= 0:  # NaN too
        raise fmcli.UsageError("--max-usd must be a number ≥ 0")
    cur, _ = fmbudget.effective()
    start, _ = fmbudget.spent()
    limit = max(0.0, min(args.max_usd, cur["day"] - start)) / (1 if known else 2)
    limit = round(limit, 4)
    note = "" if known else f"usage unknown (no statusline snapshot from the last {STALE_H} h): the limit is halved"
    if c.read_meta(p).get("sensitive"):  # review: nothing of a sensitive project leaves for children or replays
        return fmcli.out(args, {"jobs": [], "skipped": [], "ran": [], "limit": limit,
                                "note": "sensitive project: nothing runs at night"},
                         "night: sensitive project: nothing runs at night")
    plan, skipped, total = [], [], 0.0
    for name, argv, est in jobs(p):
        if args.only and not any(name == n or name.startswith(n + " ") for n in args.only):
            continue
        (plan if total + est <= limit else skipped).append({"name": name, "argv": argv, "usd": est})
        total += est if total + est <= limit else 0
    head = f"night: {len(plan)} job(s), about ${total:.2f} of ${limit:.2f}" + (f" ({note})" if note else "")
    rows = [f"  {j['name']}: fm {' '.join(j['argv'])} (≈ ${j['usd']:.2f})" for j in plan] + \
           [f"  skipped {j['name']} (≈ ${j['usd']:.2f}: over the limit)" for j in skipped]
    if args.dry_run:
        return fmcli.out(args, {"jobs": plan, "skipped": skipped, "limit": limit, "note": note}, "\n".join([head] + rows))
    ran, stopped = [], ""
    for j in plan:  # one at a time; before each, the real spend so far and the usage now (review)
        night_usd = fmbudget.spent()[0] - start
        if night_usd >= limit and ran:
            stopped = f"spend ${night_usd:.2f} reached the limit ${limit:.2f}"
            break
        if fmbudget.usage_high():
            stopped = f"usage climbed ({fmbudget.usage_high()})"
            break
        if c.panicked():
            stopped = c.PAUSED
            break
        if len(ran) >= fmserve.FAILS_MAX and all(x["exit"] for x in ran[-fmserve.FAILS_MAX:]):  # T-0434: the breaker
            stopped = f"{fmserve.FAILS_MAX} jobs failed in a row"
            break
        fmserve.beat(p, "night", JOB_TIMEOUT, j["name"])
        try:
            r = subprocess.run([sys.executable, os.path.join(c.PLUGIN_ROOT, "bin", "fm"), *j["argv"]], cwd=p.root,
                               env=dict(os.environ, FOREMAN_NO_BACKGROUND="1"), capture_output=True, text=True,
                               timeout=JOB_TIMEOUT)
            code, tail = r.returncode, (r.stdout + r.stderr).strip().splitlines()[-1:]
        except (OSError, subprocess.TimeoutExpired) as e:
            code, tail = 124, [str(e)]
        ran.append({"name": j["name"], "exit": code, "tail": c.fit(c.plain(" ".join(tail)), 160)})
    if not stopped and ran and fmbudget.spent()[0] - start > limit:
        stopped = f"spend ${fmbudget.spent()[0] - start:.2f} passed the limit ${limit:.2f} in the last job"
    with c.lock(p.dir):
        c.log_event(p, "night", data={"ran": ran, "skipped": [s["name"] for s in skipped], "limit": limit,
                                      "stopped": stopped}, session=fmcli.session())
    fmcli.out(args, {"ran": ran, "skipped": skipped, "limit": limit, "stopped": stopped, "note": note},
              "\n".join([head] + [f"  {'✓' if x['exit'] == 0 else '✗'} {x['name']}: {x['tail']}" for x in ran]
                        + [f"  skipped {s['name']}" for s in skipped] + ([f"  stopped: {stopped}"] if stopped else [])))
