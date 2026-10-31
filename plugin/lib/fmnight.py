"""fm night (T-0236): budgeted background work while the user is away — the daily second read of the last session,
the landscape scan when due, the sentinel (T-0888), one research-debt question, the court of the user's steers, a bench tournament for one
kept fm evolve candidate — each an existing fm command, kept while the night's estimate fits --max-usd and today's
remaining budget. Refused when usage is high, when usage is unknown the limit halves, a sensitive project runs
nothing, and the night stops as soon as real spend passes the limit or usage climbs (T-0298 review). Never merges;
the morning's fm digest says what ran. --tick (T-2356) is the model-free pass: orders, the cached CI result, and CI or issues only where
the user said yes. It runs from the Stop hook's sweep, and from the timers T-2357 stages: --stage writes the nightly and
hourly units into state and queues one plugin request; --install (the user's yes, through the guard) installs them."""
import fcntl
import glob
import json
import os
import re
import shlex
import subprocess
import sys
import time

import fmbudget
import fmcore as c
import fmdraft
import fmserve

STALE_H = 12  # a statusline snapshot older than this says nothing about tonight's usage
JOB_TIMEOUT = 3 * 3600  # seconds one night job may take
_LEASE = None  # T-0921: the open lock file of a running night
NAMES = ("scout", "dream", "cold files", "guard cases", "steer checks", "compost", "consolidate", "sentinel", "smoke", "pre-plan", "model lesion", "second session", "landscape", "research debt", "court", "evolve candidate", "queue", "draft")


def current_model(p):
    """The model of the newest finished task here (task_done events carry it), or None."""
    return next(((e.get("data") or {}).get("model") for e in reversed(c.ledger_tail(p, 5000))
                 if e.get("event") == "task_done" and (e.get("data") or {}).get("model")), None)


def next_lesion(p):
    """T-0734: the first rule or skill file not yet ablated (fm evolve --drop) on the current model, when this project
    has bench cases to gate it; None otherwise."""
    import fmbench
    model = current_model(p)
    if not model or not fmbench._load_cases(p):
        return None
    done = {(e.get("data") or {}).get("target") for e in c.ledger_tail(p, 20000) if e.get("event") == "evolve"
            and (e.get("data") or {}).get("model") == model}
    root = os.path.dirname(c.PLUGIN_ROOT)
    files = [os.path.relpath(os.path.join(c.PLUGIN_ROOT, "rules", "foreman.md"), root)] + sorted(
        os.path.relpath(x, root) for x in glob.glob(os.path.join(c.PLUGIN_ROOT, "skills", "*", "SKILL.md")))
    return next((f for f in files if f not in done), None)


def jobs(p):
    """[(name, fm argv, USD estimate)] of what tonight could do, cheapest and most useful first."""
    import fmbench
    import fmoutside
    meta, out = c.read_meta(p), [("scout", ["scout", "--slow"], 0.0)]  # T-0950: free to look: work nobody asked for
    out.append(("dream", ["dream"], 0.0))  # T-0665: free: the day's failures as tripwire candidates
    out.append(("cold files", ["map", "--cold", "--capture"], 0.0))  # T-0660: free: hot files nobody has read
    import fmreplay
    if os.path.realpath(p.root) == os.path.realpath(fmreplay.repo_root()) and fmreplay.load_cases()[0]:
        out.append(("guard cases", ["replay", "--cases", "--capture"], 0.0))  # T-1162: free: only Foreman's own repo; a drift is one FIX
    if c.steer_rules(p):  # T-2350: free: the user's rules' checks; a failing one is a FIX and a name in the report
        out.append(("steer checks", ["genesis", "steer"], 0.0))
    out.append(("compost", ["tidy", "--apply", "--lanes-only"], 0.0))  # T-1071: free: worktrees and branches of closed tasks
    out.append(("consolidate", ["recall", "--lessons", "--consolidate", "--capture", "--from-night"], 0.0))  # T-1071: free: a merge proposal, retires nothing
    if any(e.get("event") == "task_done" for e in c.ledger_tail(p, 5000)):  # T-0888: free: closed tasks' checks on HEAD
        out.append(("sentinel", ["sentinel", "--bisect"], 0.0))
    smoke = meta.get("smoke") or {}
    if any(k != "off" for k in smoke) and "off" not in smoke:  # T-0743: a target is set; the crawl runs locally
        out.append(("smoke", ["smoke"], 0.0))
    if meta.get("second_session") != c.now()[:10]:
        out.append(("second session", ["second", "session", "--if-due"], fmbudget.estimate("second-session", 1, 0.05)))
    age = c.age_days(meta.get("landscape_at"))
    if age is None or age >= fmoutside.LANDSCAPE_DAYS:
        out.append(("landscape", ["landscape", "--if-due"], fmbudget.estimate("research", 4, 0.2)))
    lesion = None if fmbudget.degrade(p) else next_lesion(p)
    if lesion:  # T-0734: a model nobody has ablated Foreman's rules and skills on yet
        out.append((f"model lesion {lesion}", ["evolve", "--target", lesion, "--drop"], fmbudget.estimate("bench", 3, 0.5)))
    big = None if fmbudget.degrade(p) else next(  # T-0730: optional, so it waits while usage runs ahead of pace
        (b for b in c.order_queue(c.load_briefs(p))[0] if b.tier == "L" and not b.section("Plan review").strip()), None)
    if big:  # a queued L task's plan read by another model while nobody is waiting on it
        out.append((f"pre-plan {big.id}", ["second", "plan", big.id], fmbudget.estimate("second-plan", 1, 0.05)))
    events = c.ledger_tail(p, 5000)
    asked = {e.get("task") for e in events if e.get("event") == "research"}
    debt = next((b for b in c.rank_inbox(c.load_briefs(p)) if b.type == "RESEARCH" and b.id not in asked
                 and b.meta.get("source") != "cold"), None)  # local files are read here, never sent to web research
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
    briefs = c.load_briefs(p)
    state = {b.id: b.status for b in briefs}
    if any(b.tier in ("S", "M") and all(state.get(d) in c.CLOSED for d in c._deps(b))
           for b in c.order_queue(briefs)[0]):  # T-1046: an unblocked small task is waiting: fm run works it
        out.append(("queue", ["run", "--fit", "--max", "2", "--wait", "0"], fmbudget.estimate("run", 2, 0.5)))
    top = fmdraft._top(p)
    if top and not os.path.exists(os.path.join(p.dir, "draft.json")):  # T-1062: a small task drafted for review, never merged
        out.append((f"draft {top.id}", ["draft"], fmbudget.estimate("run", 1, 0.3)))
    return out


def _usage():
    """(why usage is high, or None; whether it is known): a snapshot older than STALE_H hours is not knowledge."""
    snaps = glob.glob(os.path.join(c.state_dir(), "sessions", "*.json"))
    fresh = any(time.time() - os.path.getmtime(s) < STALE_H * 3600 for s in snaps)
    return fmbudget.usage_high(), fresh


def units(p, max_usd=2.0):
    """T-0955, T-2357: {file: text}: the nightly fm night and hourly fm night --tick systemd user units (Persistent=, so
    a machine asleep at the hour runs it on waking), and crontab.txt, the same two lines for a machine without systemd."""
    fm = f"{shlex.quote(sys.executable)} {shlex.quote(os.path.join(c.PLUGIN_ROOT, 'bin', 'fm'))}"
    # systemd and cron start with a bare environment: this state dir, and the tools on your PATH (claude, git)
    path = ":".join(d for d in os.environ.get("PATH", "").split(":") if d and not re.search(r"[\x00-\x1f\"%\s]", d))
    home, out, cron = c.foreman_home(), {}, []
    if re.search(r"[\x00-\x1f\x7f]", p.root + home + fm):  # a newline would add a line to the unit
        raise c.PolicyError("the project or Foreman home path holds a control character: no timer unit is written for it")
    sd = lambda s: s.replace("%", "%%")  # noqa: E731 - systemd expands %-specifiers in these fields
    for kind, every, when, args, minute in (("night", "nightly", "*-*-* 02:30", f"night --max-usd {max_usd:g}", "30 2"),
                                            ("tick", "hourly", "hourly", "night --tick", "0 *")):
        name = f"foreman-{kind}-{p.slug}"
        out[name + ".service"] = "\n".join([
            "[Unit]", f"Description=Foreman {kind} ({p.slug})", "", "[Service]", "Type=oneshot",
            f"WorkingDirectory={sd(p.root)}", f'Environment="FOREMAN_HOME={sd(home)}"', f'Environment="PATH={path}"',
            f"ExecStart={sd(fm)} {args}", ""])
        out[name + ".timer"] = "\n".join([
            "[Unit]", f"Description=Foreman {kind} ({p.slug}), {every}", "", "[Timer]", f"OnCalendar={when}",
            "Persistent=true", "", "[Install]", "WantedBy=timers.target", ""])
        cron.append(f"{minute} * * * cd {shlex.quote(p.root)} && FOREMAN_HOME={shlex.quote(home)} "
                    f"PATH={shlex.quote(path)} {fm} {args}")
    out["crontab.txt"] = "\n".join(cron) + "\n"
    return out


def _staged(p):
    return os.path.join(p.dir, "night", "staged")


def write_staged(p, issues=(), ci=False, max_usd=2.0):
    """T-2357: the units and plan.json in state only (nothing outside it); returns (plan, the lines the ask names)."""
    import hashlib
    import shutil
    files = units(p, max_usd)
    plan = {"units": sorted(n for n in files if n.endswith((".service", ".timer"))), "max_usd": max_usd,
            "watch": {"ci": bool(ci), "issues": sorted(set(issues))}}
    plan["hash"] = hashlib.sha256(json.dumps([files, plan], sort_keys=True).encode()).hexdigest()[:8]
    d = _staged(p)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    for name, text in dict(files, **{"plan.json": json.dumps(plan, indent=1) + "\n"}).items():
        c.write_atomic(os.path.join(d, name), text)
    lines = [f"nightly fm night at 02:30 (at most ${max_usd:.2f})", "hourly fm night --tick (no tokens)"] \
        + [f"issue watch {r}" for r in plan["watch"]["issues"]] \
        + (["CI check with no session open"] if ci else []) + ["undo: fm night --uninstall"]
    return plan, lines


def _plan(p):
    try:
        with open(os.path.join(_staged(p), "plan.json"), encoding="utf-8") as f:
            plan = json.load(f)
        return plan if isinstance(plan, dict) and isinstance(plan.get("units"), list) else None
    except (OSError, ValueError):
        return None


def install(p):
    """T-2357: the staged units (staged now when none are) go to the systemd user folder and their timers start; the
    watch lines that were staged, and only those, are turned on. The guard lets an agent run this only after the user's
    yes to the queued plugin request; a user typing it has said yes."""
    import shutil
    plan = _plan(p) or write_staged(p)[0]
    if not shutil.which("systemctl"):
        raise c.PolicyError(f"no systemd --user here: the staged crontab lines are in "
                            f"{os.path.join(_staged(p), 'crontab.txt')} (crontab -e)")
    udir = fmserve.unit_dir()
    os.makedirs(udir, exist_ok=True)
    names = [n for n in plan["units"] if re.fullmatch(rf"foreman-(night|tick)-{re.escape(p.slug)}\.(service|timer)", n)]
    for n in names:
        shutil.copyfile(os.path.join(_staged(p), n), os.path.join(udir, n))
    fmserve._systemctl("daemon-reload")
    for n in names:
        if n.endswith(".timer"):
            fmserve._systemctl("enable", "--now", n)
    w = plan.get("watch") if isinstance(plan.get("watch"), dict) else {}
    watch = {"ci": w.get("ci") is True, "issues": [r for r in w.get("issues") or [] if isinstance(r, str) and _REPO.fullmatch(r)]}
    with c.lock(p.dir):
        meta = c.read_meta(p)
        meta["watch"] = watch
        meta["night_units"] = {"units": names, "home": c.foreman_home(), "at": c.now()}
        c.write_meta(p, meta)
    c.log_event(p, "night_installed", data={"units": names, "watch": watch})
    shutil.rmtree(_staged(p), ignore_errors=True)
    return names, watch


def uninstall(p):
    """T-2357: the timers stopped and their units removed, the watch lines off."""
    meta = c.read_meta(p)
    names = (meta.get("night_units") or {}).get("units") or list(units(p))[:4]
    names = [n for n in names if re.fullmatch(rf"foreman-(night|tick)-{re.escape(p.slug)}\.(service|timer)", str(n))]
    for n in names:
        if n.endswith(".timer"):
            try:
                fmserve._systemctl("disable", "--now", n, check=False)
            except c.PolicyError:  # no systemd here: the files still go
                pass
        try:
            os.remove(os.path.join(fmserve.unit_dir(), n))
        except FileNotFoundError:
            pass
    try:
        fmserve._systemctl("daemon-reload", check=False)
    except c.PolicyError:
        pass
    with c.lock(p.dir):
        meta = c.read_meta(p)
        meta.pop("night_units", None)
        meta.pop("watch", None)
        c.write_meta(p, meta)
    c.log_event(p, "night_uninstalled", data={"units": names})
    return names


ISSUES_EVERY = 1800  # a repo's issues are polled at most this often (the Stop sweep ticks every 10 min)
ISSUES_LIMIT = 10  # new issues captured per poll (a first poll of a busy tracker is not 30 tasks)
_REPO = re.compile(r"[\w.-]+/[\w.-]+")


def _watch(meta):
    """(CI fetch approved, [repos whose issue watch is approved]): meta 'watch' {"ci": true, "issues": ["o/r"]}, which
    only T-2357's one-yes install writes after the user's yes. Anything else reads as no."""
    w = meta.get("watch") if isinstance(meta.get("watch"), dict) else {}
    issues = w.get("issues")
    return w.get("ci") is True, [r for r in issues if isinstance(r, str) and _REPO.fullmatch(r)] if isinstance(issues, list) else []


CAP = 20  # issues the tick captures per repo per day: a flood of issues is not a flood of tasks


def fetches(p, days=7):
    """[(date, kind, repo, requests)] the tick sent off the machine in the last days, from its night_tick ledger
    events: routine approved polls are listed here (fm decide --review prints them), not as pending [outward] rows."""
    cut = (c.datetime.date.today() - c.datetime.timedelta(days=days)).isoformat()
    n = {}
    for e in c.ledger_tail(p, 5000):
        if e.get("event") == "night_tick" and str(e.get("ts"))[:10] >= cut:
            for f in (e.get("data") or {}).get("fetched") or []:
                k = (str(e["ts"])[:10], str(f.get("kind")), str(f.get("repo")))
                n[k] = n.get(k, 0) + 1
    return [k + (v,) for k, v in sorted(n.items())]


def _row(p, text, why):
    """One [outward] decision (fm todo holds it for the user's look), for something new: the first request for a repo,
    a failure, the cap. Once a day for the same words."""
    import fmcli
    if not any(d == c.now()[:10] and t == text for d, _, t in c._decision_rows(p)):
        fmcli._write_decision(p, text, why, "", "outward")


def _num(v):
    try:
        return float(v or 0)
    except (TypeError, ValueError):
        return 0.0


def tick(p, fetch_ci=None):
    """T-2356: the model-free pass, from the Stop hook's sweep and the timer: standing orders (file and schedule
    triggers), the CI result fmforesight cached, and new issues of a repo the user approved. Spends no tokens and runs
    no child. Remote reads only with the user's yes (meta watch), never when sensitive or FOREMAN_NO_NET; CI is fetched
    here only when approved and no session is open (fetch_ci=None decides; the sweep passes False: it fetched its own).
    {orders, captured, fetched: [{kind, repo}], notes}."""
    import fmcli
    import fmeco
    import fmforesight
    import fmorders
    if c.panicked():
        raise c.PolicyError(c.PAUSED)
    res = {"orders": [], "captured": [], "fetched": [], "notes": []}
    lease = open(os.path.join(p.dir, "tick.lock"), "w")  # held until this returns (a second tick finds it taken)
    try:
        fcntl.flock(lease, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        lease.close()
        return dict(res, notes=["another tick is running"])
    before, path, loud = None, os.path.join(p.dir, "tick.json"), []
    try:
        with lease:
            meta = c.read_meta(p)
            net = not os.environ.get("FOREMAN_NO_NET") and not meta.get("sensitive")
            ci_ok, repos = _watch(meta)
            before = {b.id for b in c.load_briefs(p, include_archive=True)}
            try:
                if fmorders.load(p):
                    res["orders"] = [o["n"] for o in fmorders.run(p)]
            except Exception as e:  # an order file never costs the tick
                res["notes"].append(f"standing orders: {c.fit(c.plain(str(e)), 120)}")
            try:
                with open(path, encoding="utf-8") as f:
                    seen = json.load(f)
            except (OSError, ValueError):
                seen = {}
            seen = seen if isinstance(seen, dict) else {}
            stamps = seen["issues"] if isinstance(seen.get("issues"), dict) else {}
            told = [x for x in seen["told"] if isinstance(x, str)] if isinstance(seen.get("told"), list) else []
            day = seen["day"] if isinstance(seen.get("day"), dict) else {}
            today = c.now()[:10]
            made = day["n"] if day.get("date") == today and isinstance(day.get("n"), dict) else {}

            def save():
                c.write_atomic(path, json.dumps({"issues": stamps, "told": told, "day": {"date": today, "n": made}}))

            def first(kind, repo, what):  # the first request of a kind for a repo is one outward row; later ones aren't
                if f"{kind} {repo}" not in told:
                    told.append(f"{kind} {repo}")
                    loud.append((f"night tick {what} {repo} for the first time", "your yes to the watch line; later "
                                 "requests are night_tick ledger events (fm decide --review lists them)"))

            repo = None if meta.get("sensitive") else fmforesight.github_repo(p.root)
            if repo:
                sent = []
                try:  # the cached result always; a fetch only with the yes, and with nobody at a keyboard to ask
                    import fmbus
                    ask = net and ci_ok and (not fmbus.live() if fetch_ci is None else fetch_ci)
                    fmforesight._ci(p, fetch=bool(ask), sent=sent)
                except Exception as e:
                    res["notes"].append(f"CI: {c.fit(c.plain(str(e)), 120)}")
                if sent:  # listed even when the capture after it failed
                    res["fetched"].append({"kind": "ci", "repo": repo})
                    first("ci", repo, "fetched the CI result of")
                    save()
            if net and repo and repo in repos and time.time() - _num(stamps.get(repo)) >= ISSUES_EVERY:
                try:
                    left = CAP - int(_num(made.get(repo)))
                except (OverflowError, ValueError):
                    left = 0
                if left <= 0:
                    res["notes"].append(f"issues of {repo}: daily cap of {CAP} captured, polling resumes tomorrow")
                else:
                    stamps[repo] = time.time()
                    first("issues", repo, "polled GitHub issues of")
                    save()  # stamped first: a failing gh waits its interval too
                    res["fetched"].append({"kind": "issues", "repo": repo})
                    try:  # fm inbox gh's path: plain, defanged, quoted behind "| "; an issue's asks are never run
                        got = fmeco.inbox_gh(p, repo, min(ISSUES_LIMIT, left))
                        made[repo] = int(_num(made.get(repo))) + len(got["captured"])
                        save()
                        if made[repo] >= CAP:
                            res["notes"].append(f"issues of {repo}: daily cap of {CAP} captured, polling resumes tomorrow")
                            loud.append((f"night tick stopped capturing issues of {repo} today: {CAP} captured (the cap)",
                                         "a flood of issues is not a flood of tasks; polling resumes tomorrow"))
                    except Exception as e:  # not logged in, no gh, offline: said, never fatal
                        why = c.fit(c.redact(c.plain(str(e))), 160)
                        res["notes"].append(f"issues of {repo}: {why}")
                        loud.append((f"night tick's poll of GitHub issues of {repo} failed", why))
    finally:  # what left the machine is listed even when something after it failed
        if before is not None:
            res["captured"] = sorted({b.id for b in c.load_briefs(p, include_archive=True)} - before)
        for text, why in loud:
            _row(p, text, why)
        if res["fetched"] or res["orders"] or res["captured"]:
            c.log_event(p, "night_tick", data={k: res[k] for k in ("orders", "captured", "fetched")}, session=fmcli.session())
    return res


def cmd_night(args):
    import fmcli
    p = fmcli.resolve(args)
    if getattr(args, "stage", False):  # T-2357: staged in state, asked once (the install queue); nothing installed
        import fmgrants
        issues = getattr(args, "watch_issues", None) or []
        bad = [r for r in issues if not _REPO.fullmatch(r)]
        if bad:
            raise fmcli.UsageError(f"--watch-issues takes OWNER/REPO, not {bad[0]!r}")
        b = c.find_brief(p, args.task) if getattr(args, "task", None) else c.active_brief_fast(p)
        if not b or b.status in c.CLOSED:
            raise fmcli.UsageError("fm night --stage queues its request on an open task: focus one or pass --task ID")
        plan, lines = write_staged(p, issues, getattr(args, "watch_ci", False), args.max_usd)
        state, _ = fmgrants.queue(p, b.id, ["plugin"], "; ".join(lines), what=f"night timers {plan['hash']}",
                                  fallback="fm night --tick runs from the Stop hook's sweep while a session is open",
                                  session=fmcli.session())
        said = {"queued": f"queued on {b.id} for the user's yes (fm todo)", "dedupe": f"already queued on {b.id}",
                "refused": "the user said no to this before: not asked again", "missing": "no such task"}[state]
        return fmcli.out(args, {"staged": _staged(p), "plan": plan, "lines": lines, "task": b.id, "state": state},
                         "\n".join([f"night timers staged in {_staged(p)}; {said}:"] + [f"- {x}" for x in lines]
                                   + ["After the yes: fm night --install."]))
    if getattr(args, "install", False):
        names, watch = install(p)
        return fmcli.out(args, {"units": names, "watch": watch},
                         f"installed and started: {', '.join(n for n in names if n.endswith('.timer'))}; CI check "
                         f"{'on' if watch['ci'] else 'off'}; issue watch: {', '.join(watch['issues']) or 'none'}. "
                         "Undo: fm night --uninstall")
    if getattr(args, "uninstall", False):
        names = uninstall(p)
        return fmcli.out(args, {"removed": names}, f"removed: {', '.join(names) or 'nothing installed'}; watch lines off")
    if getattr(args, "tick", False):
        res = tick(p)
        return fmcli.out(args, res, "tick: " + ", ".join(
            [f"{len(res['orders'])} order(s) fired", f"{len(res['captured'])} captured"]
            + [f"fetched {f['kind']} of {f['repo']}" for f in res["fetched"]] + res["notes"]))
    if c.panicked():
        raise c.PolicyError(c.PAUSED)
    if not getattr(args, "dry_run", False):  # T-0921: one night at a time (a cron firing while a manual one runs)
        global _LEASE
        _LEASE = open(os.path.join(p.dir, "night.lock"), "w")  # held until the process ends
        try:
            fcntl.flock(_LEASE, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise fmcli.UsageError(f"another fm night is already running for {p.slug}")
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
    ran, stopped, t0 = [], "", c.now()
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
            left = ["--max-usd", f"{max(0.0, limit - (fmbudget.spent()[0] - start)):.4f}"] if j["name"] == "queue" else []
            r = subprocess.run([sys.executable, os.path.join(c.PLUGIN_ROOT, "bin", "fm"), *j["argv"], *left], cwd=p.root,
                               env=dict(os.environ, FOREMAN_NO_BACKGROUND="1"), capture_output=True, text=True,
                               timeout=JOB_TIMEOUT)
            code, tail = r.returncode, (r.stdout + r.stderr).strip().splitlines()[-1:]
        except (OSError, subprocess.TimeoutExpired) as e:
            code, tail = 124, [str(e)]
        ran.append({"name": j["name"], "exit": code, "tail": c.fit(c.plain(" ".join(tail)), 160)})
    if not stopped and ran and fmbudget.spent()[0] - start > limit:
        stopped = f"spend ${fmbudget.spent()[0] - start:.2f} passed the limit ${limit:.2f} in the last job"
    closed = [e["task"] for e in c.ledger_tail(p, 5000) if e.get("event") == "task_done" and e.get("task")
              and str(e.get("ts", ""))[:19] >= t0[:19]] if any(x["name"] == "queue" for x in ran) else []
    with c.lock(p.dir):
        c.log_event(p, "night", data={"ran": ran, "skipped": [s["name"] for s in skipped], "limit": limit,
                                      "stopped": stopped, "closed": closed}, session=fmcli.session())
    fmcli.out(args, {"ran": ran, "skipped": skipped, "limit": limit, "stopped": stopped, "note": note},
              "\n".join([head] + [f"  {'✓' if x['exit'] == 0 else '✗'} {x['name']}: {x['tail']}" for x in ran]
                        + [f"  skipped {s['name']}" for s in skipped] + ([f"  stopped: {stopped}"] if stopped else [])))
