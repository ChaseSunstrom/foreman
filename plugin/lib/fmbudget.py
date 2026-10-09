"""fm budget (T-0227): bounded use of model work, not avoidance. Everything Foreman spawns — tool-less children (fm ideas,
oracle, research ask, evolve's mutation), headless replays (fm bench) and Claude's Agent subagents — records what it
cost in one global ledger (state/spend.jsonl: USD from claude's JSON result, tokens for subagents), and caps
(state/budget.json) refuse a command whose estimate would pass the per-command or the day's limit. Past 80% of weekly
usage (or 90% of the 5-hour window, the statusline's snapshot) every cap halves, like economy mode. Raising a cap isn't
blocked: it is recorded as a costly decision, which the user reviews (fm decide --review). Subagents have no token cap
(T-0320): they wait only while usage runs ahead of the week's pace or the 5-hour window is nearly spent."""
import datetime
import glob
import json
import math
import os
import time

import fmcore as c

DEFAULTS = {"day": 15.0, "run": 6.0}  # USD per day, USD per command
PACE_FLOOR = 75  # weekly usage % below which subagents never wait for the pace (T-0364)
WEIGHTS = {"input_tokens": 1, "cache_creation_input_tokens": 1.25, "cache_read_input_tokens": 0.1, "output_tokens": 5}


class BudgetError(ValueError):  # a ValueError: callers already turn those into a clean refusal
    pass


def _path(name):
    return os.path.join(c.state_dir(), name)


def caps():
    try:
        with open(_path("budget.json"), encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        data = {}
    out = dict(DEFAULTS)
    for k, v in DEFAULTS.items():  # a corrupt or hand-edited file falls back per cap, never crashes or disables
        try:
            x = type(v)(data.get(k, v)) if isinstance(data, dict) else v
            out[k] = x if math.isfinite(x) and x >= 0 else v
        except (TypeError, ValueError, OverflowError):
            pass
    return out


def set_caps(**new):
    cur = caps()
    cur.update({k: v for k, v in new.items() if v is not None and k in DEFAULTS})
    os.makedirs(c.state_dir(), exist_ok=True)
    c.write_atomic(_path("budget.json"), json.dumps(cur))
    return cur


def _today():
    return datetime.date.today().isoformat()  # the user's local day


def ledger(days=1):
    since = (datetime.date.today() - datetime.timedelta(days=days - 1)).isoformat()
    return [e for e in c.tail_jsonl(_path("spend.jsonl"), 20000) if str(e.get("day", "")) >= since]


def record(feature, usd=None, runs=1, tokens=None, project=None, detail=""):
    e = {"ts": c.now(), "day": _today(), "feature": feature, "usd": round(usd, 4) if usd is not None else None,
         "runs": runs, "tokens": tokens, "project": project, "detail": c.fit(str(detail), 120)}
    os.makedirs(c.state_dir(), exist_ok=True)
    with open(_path("spend.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(e) + "\n")
    return e


def spent(day_rows=None):
    rows = ledger() if day_rows is None else day_rows
    return (round(sum(e.get("usd") or 0 for e in rows), 4),
            sum(e.get("tokens") or 0 for e in rows if str(e.get("feature", "")).startswith("subagent")))


def estimate(feature, runs, fallback):
    """USD for `runs` more runs of a feature: its recent mean cost per run, else the fallback per run."""
    recent = [e for e in c.tail_jsonl(_path("spend.jsonl"), 5000) if e.get("feature") == feature and e.get("usd")
              and e.get("runs")][-20:]
    per = sum(e["usd"] for e in recent) / sum(e["runs"] for e in recent) if recent else fallback
    return round(per * runs, 4)


def rate_limits():
    """{"five_hour": %, "seven_day": %, "week_gone": share of the week gone by} from the newest statusline snapshot
    that has any; a window whose reset time has passed reads as 0 (it emptied since the snapshot)."""
    snaps = sorted(glob.glob(os.path.join(c.state_dir(), "sessions", "*.json")), key=os.path.getmtime)
    now = time.time()
    for path in reversed(snaps[-3:]):
        try:
            with open(path, encoding="utf-8") as f:
                rl = json.load(f).get("rate_limits") or {}
            out = {}
            for k in ("five_hour", "seven_day"):
                w = rl.get(k) or {}
                used, resets = w.get("used_percentage"), w.get("resets_at")
                if not isinstance(used, (int, float)) or isinstance(used, bool):
                    continue
                known = isinstance(resets, (int, float))
                out[k] = 0 if known and resets <= now else used
                if k == "seven_day" and known and 0 < resets - now <= 7 * 86400:  # else (ms epoch, skew) pace unknown
                    out["week_gone"] = 1 - (resets - now) / (7 * 86400)
        except (OSError, ValueError, AttributeError):
            continue
        if out:
            return out
    return {}


def usage_high():
    """'weekly usage 85%' when the newest statusline snapshot is past 80% weekly or 90% of the 5-hour window, else
    None: the same thresholds as foreman-ui's economy mode (T-0198)."""
    u = rate_limits()
    if u.get("seven_day", 0) >= 80:
        return f"weekly usage {u['seven_day']:g}%"
    if u.get("five_hour", 0) >= 90:
        return f"5-hour usage {u['five_hour']:g}%"
    return None


def subagent_pause():
    """Why subagents should wait, or None (T-0320): the 5-hour window at 90%+, or weekly usage ahead of the week's
    pace — more than 10 points past the share of the week gone by, never before 75% (the user, T-0364: "the budget
    stuff shouldn't matter until 75% usage") and never past 90%. Unknown usage never pauses."""
    u = rate_limits()
    if u.get("five_hour", 0) >= 90:
        return f"5-hour usage {u['five_hour']:g}%"
    week, gone = u.get("seven_day"), u.get("week_gone")
    if week is not None and week >= max(PACE_FLOOR, min(90, 100 * gone + 10 if gone is not None else 80)):
        return f"weekly usage {week:g}%" + (f" with {100 * gone:.0f}% of the week gone" if gone is not None else "")
    return None


def degrade():
    """T-0449: why optional work (the drive's side tasks, the friction pass, brainstorm deepening) is dropped, or None:
    the pace subagents wait on. Never a cap: check() still refuses what's over one, and required gates still run."""
    return subagent_pause()


def effective():
    """(caps after economy, why they were halved or None)."""
    cur, high = caps(), usage_high()
    if high:
        cur = {k: v / 2 for k, v in cur.items()}
    return cur, high


def check(feature, est, smaller=""):
    """Raise BudgetError when a command estimated at `est` USD would pass the per-command cap or today's."""
    cur, high = effective()
    usd, _ = spent()
    why = f" (halved: {high})" if high else ""
    hint = f"; {smaller}" if smaller else ""
    if est > cur["run"]:
        raise BudgetError(f"budget: {feature} would spend about ${est:.2f}, over the ${cur['run']:.2f} per command "
                          f"cap{why}{hint}; or raise it: fm budget set --run N --because \"<why>\"")
    if usd + est > cur["day"]:
        raise BudgetError(f"budget: {feature} would spend about ${est:.2f}; today ${usd:.2f} of ${cur['day']:.2f} is "
                          f"spent{why}{hint}; or raise it: fm budget set --day N --because \"<why>\"")


def check_subagent():
    why = subagent_pause()
    if why:
        raise BudgetError(f"budget: subagents wait while usage is ahead of pace ({why}); do it in the main thread")


def result(stdout):
    """(text, usd) from `claude -p --output-format json`; plain text (an older claude, a stub) gives (text, None)."""
    for line in reversed((stdout or "").strip().splitlines()):
        try:
            data = json.loads(line)
        except ValueError:
            continue
        if isinstance(data, dict) and "result" in data:
            return str(data.get("result") or ""), data.get("total_cost_usd")
    return stdout or "", None


def transcript_tokens(path):
    """Input-equivalent tokens in a subagent transcript, each message counted once."""
    seen = {}
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                try:
                    e = json.loads(line)
                except ValueError:
                    continue
                m = e.get("message") if isinstance(e, dict) else None
                if isinstance(m, dict) and isinstance(m.get("usage"), dict):
                    seen[m.get("id") or len(seen)] = m["usage"]
    except OSError:
        return 0
    return int(sum((u.get(k) or 0) * w for u in seen.values() for k, w in WEIGHTS.items()))


def cmd_budget(args):
    import fmcli
    p = fmcli.resolve(args)
    if args.action == "set":
        cur = caps()
        new = {"day": args.day, "run": args.run}
        bad = [k for k, v in new.items() if v is not None and not (math.isfinite(v) and v >= 0)]
        if bad:
            raise fmcli.UsageError(f"caps are finite numbers ≥ 0: {', '.join(bad)}")
        up = [k for k, v in new.items() if v is not None and v > cur[k]]
        if up and not args.because:
            raise fmcli.UsageError("raising a cap needs --because \"<why>\" (it is recorded as a costly decision)")
        res = set_caps(**new)
        if up:  # not blocked: recorded for the user's review of costly decisions
            import argparse
            fmcli.cmd_decide(argparse.Namespace(
                project=getattr(args, "project", None), json=False, list=False, review=False, n=30, task=None,
                decision=f"budget raised: {', '.join(f'{k} {cur[k]:g} → {res[k]:g}' for k in up)}", why=args.because,
                rejected="", kind="costly", reverses=None))
        return fmcli.out(args, res, "caps: " + ", ".join(f"{k} {v:g}" for k, v in res.items()))
    rows = ledger(args.days)
    today = [e for e in rows if e.get("day") == _today()]
    usd, tokens = spent(today)
    cur, high = effective()
    by = {}
    for e in rows:
        f = by.setdefault(e.get("feature"), {"usd": 0.0, "runs": 0, "tokens": 0})
        f["usd"] += e.get("usd") or 0
        f["runs"] += e.get("runs") or 0
        f["tokens"] += e.get("tokens") or 0
    pause = subagent_pause()
    lines = [f"today: ${usd:.2f} of ${cur['day']:.2f} · per command ≤ ${cur['run']:.2f}" + (f" (halved: {high})" if high else ""),
             f"subagents: {tokens:,} tokens today · " + (f"waiting: {pause}" if pause else "running (usage on pace)")]
    lines += [f"  {k}: ${v['usd']:.2f} over {v['runs']} run(s)" + (f", {v['tokens']:,} tokens" if v["tokens"] else "")
              for k, v in sorted(by.items(), key=lambda kv: -kv[1]["usd"] - kv[1]["tokens"] / 1e6)]
    fmcli.out(args, {"today_usd": usd, "today_subagent_tokens": tokens, "caps": cur, "halved": high,
                     "subagents_paused": pause, "by_feature": by},
              "\n".join(lines))
