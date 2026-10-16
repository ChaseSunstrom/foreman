#!/usr/bin/env python3
"""Aggregates of Foreman's own history for the site's charts (T-1220): python3 site/stats.py [--state DIR] [--no-bench]

Reads this repo's Foreman state (the ledger, the task briefs) and git, and writes site/data/stats.json. Only counts,
categories and timings are written: never a task title, a path, a command or a session id. CI has no Foreman state, so
this runs here and its output is committed; site/build.py only reads it."""
import argparse
import collections
import datetime
import glob
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site", "data", "stats.json")
TYPES = ["FEATURE", "FIX", "CLEAN", "PERFORMANCE", "SECURITY", "RESEARCH"]


def git(*a):
    return subprocess.run(["git", "-C", ROOT, *a], capture_output=True, text=True, check=True).stdout


def state_dir():
    """This repo's project: the foreman-* project folder with the biggest ledger (sandboxes and improve worktrees have
    their own, much smaller ones)."""
    home = os.environ.get("FOREMAN_HOME") or ROOT
    found = [d for d in glob.glob(os.path.join(home, "state", "projects", "foreman-*"))
             if os.path.isfile(os.path.join(d, "ledger.jsonl"))]
    return max(found, key=lambda d: os.path.getsize(os.path.join(d, "ledger.jsonl")), default=None)


def briefs(state):
    """{task id: (type, tier)} from every brief's frontmatter, archived ones included."""
    out = {}
    for path in glob.glob(os.path.join(state, "tasks", "*.md")) + glob.glob(os.path.join(state, "archive", "**", "*.md"),
                                                                            recursive=True):
        try:
            with open(path, encoding="utf-8") as f:
                head = f.read(1500)
        except OSError:
            continue
        tid = re.search(r"(?m)^id: (T-\d+)", head)
        typ = re.search(r"(?m)^type: (\w+)", head)
        tier = re.search(r"(?m)^tier: (\w+)", head)
        if tid and typ:
            out[tid.group(1)] = (typ.group(1), tier.group(1) if tier else "S")
    return out


def day(ts):
    return ts[:10]


def ledger(state, kinds):
    tasks = briefs(state)
    done_by_day = collections.defaultdict(collections.Counter)
    tiers, types = collections.Counter(), collections.Counter()
    guard, lenses, severities, agents = collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter()
    lanes_by_day, evidence_by_day, gate_secs = collections.Counter(), collections.Counter(), []
    totals = collections.Counter()
    seen_done = set()
    with open(os.path.join(state, "ledger.jsonl"), encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                e = json.loads(line)
            except ValueError:
                continue
            ev, ts, data = e.get("event"), e.get("ts") or "", e.get("data") or {}
            if not ts:
                continue
            totals[ev] += 1
            if ev == "task_done" and e.get("task") not in seen_done:
                seen_done.add(e.get("task"))
                typ, tier = tasks.get(e.get("task"), ("FEATURE", "S"))
                typ = typ if typ in TYPES else "FEATURE"
                done_by_day[day(ts)][typ] += 1
                tiers[tier] += 1
                types[typ] += 1
            elif ev == "guard_block":
                guard[str(data.get("category") or "other")] += 1
            elif ev == "finding":
                lenses[str(data.get("lens") or "other")] += 1
                if data.get("severity"):
                    severities[str(data["severity"]).upper()] += 1
            elif ev == "subagent":
                agents[str(data.get("agent_type") or "other").replace("foreman:", "")] += 1
            elif ev == "lane_merge":
                lanes_by_day[day(ts)] += 1
            elif ev == "evidence":
                evidence_by_day[day(ts)] += 1
            elif ev == "check_run":
                s = sum(r.get("s") or 0 for r in data.get("results") or [] if isinstance(r, dict))
                if s:
                    gate_secs.append(round(s, 1))
    days = sorted(set(done_by_day) | set(lanes_by_day) | set(evidence_by_day))
    return {
        "totals": {"tasks_done": len(seen_done), "evidence": totals["evidence"], "proofs": totals["prove"],
                   "commits": totals["commit"], "gate_runs": totals["check_run"], "subagents": totals["subagent"],
                   "lanes_merged": totals["lane_merge"], "findings": totals["finding"],
                   "guard_blocks": totals["guard_block"], "captures": totals["capture"],
                   "lessons_shown": totals["lesson_shown"]},
        "daily": [{"day": d, **{t: done_by_day[d][t] for t in TYPES}, "lanes": lanes_by_day[d],
                   "evidence": evidence_by_day[d]} for d in days],
        "tiers": {k: tiers[k] for k in ("S", "M", "L")},
        "types": {t: types[t] for t in TYPES},
        "guard": dict(guard.most_common(8)),
        "findings": {"lenses": dict(lenses.most_common(6)), "severity": dict(severities.most_common(4))},
        "subagents": dict(agents.most_common(6)),
        "gate_seconds": {"runs": len(gate_secs), "median": sorted(gate_secs)[len(gate_secs) // 2] if gate_secs else 0},
    }


def releases():
    out = []
    for line in git("log", "--format=%h %ad %s", "--date=short", "-E", "--grep=^Foreman [0-9]+\\.[0-9]+\\.[0-9]+$").splitlines()[:16]:
        sha, day, _, version = line.split(" ", 3)
        tests = 0
        for row in git("grep", "-c", "def test_", sha, "--", "plugin/tests").splitlines():
            tests += int(row.rsplit(":", 1)[1])
        out.append({"version": version, "day": day, "tests": tests})
    return list(reversed(out))


def cards():
    base = os.path.join(ROOT, "plugin", "skills", "library", "cards")
    return dict(sorted(((a, len(glob.glob(os.path.join(base, a, "*.md")))) for a in os.listdir(base)
                        if os.path.isdir(os.path.join(base, a))), key=lambda kv: -kv[1]))


def bench():
    p = subprocess.run([sys.executable, os.path.join(ROOT, "plugin", "tests", "bench_hooks.py"), "--runs", "20", "--json"],
                       capture_output=True, text=True, timeout=600)
    data = json.loads(p.stdout or "{}")
    return {k: {"p50": v["p50"], "p95": v["p95"], "budget": v["budget"]} for k, v in data.items() if "p95" in v}


def duel(state, model=None):
    """The newest fm bench duel --vs none (with that model, if given): each case's pass, cost, turns and time for both
    arms (T-1222)."""
    res = os.path.join(state, "bench", "results")
    for path in sorted(glob.glob(os.path.join(res, "duel-none-foreman-*.json")), reverse=True):
        bare_path = os.path.join(res, "duel-none-bare-" + path.rsplit("duel-none-foreman-", 1)[1])
        with open(path, encoding="utf-8") as f:
            fm_ = json.load(f)
        if os.path.isfile(bare_path) and (not model or fm_.get("model") == model):
            break
    else:
        return None
    with open(bare_path, encoding="utf-8") as f:
        bare = json.load(f)
    pick = lambda x: {"pass": bool(x.get("pass")), "cost": round(x.get("cost_usd") or 0, 3), "score": x.get("score"),
                      "runs": x.get("runs") or 1, "passed": round((x.get("pass_rate") or 0) * (x.get("runs") or 1)),
                      "seconds": x.get("seconds") or 0, "turns": x.get("turns") or 0, "error": bool(x.get("error"))}
    b = {x["id"]: x for x in bare.get("cases", [])}
    try:  # T-1231: a commit case's id is its sha; its title names the module the task adds
        with open(os.path.join(state, "bench", "cases.json"), encoding="utf-8") as f:
            titles = {x["id"]: x.get("title") or "" for x in json.load(f)}
    except (OSError, ValueError, TypeError, KeyError):
        titles = {}
    def name(cid):  # kit.lru → "lru"; otherwise the title's first words
        t = titles.get(cid, "")
        mod = re.findall(r"\bkit\.(\w+)", t)
        return mod[0] if mod else (" ".join(re.sub(r"[:(].*", "", t).split()[:5]).rstrip(",;.") or cid)
    cases = [{"case": name(x["id"]), "foreman": pick(x), "bare": pick(b[x["id"]])} for x in fm_.get("cases", [])
             if x["id"] in b]
    return {"model": fm_.get("model"), "at": (fm_.get("at") or "")[:10], "cases": cases}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--state")
    ap.add_argument("--duel", action="append", metavar="NAME=DIR",
                    help="a Foreman project state folder whose newest duel to show, named (repeatable); default: this "
                         "repo's, as the quality duel")
    ap.add_argument("--no-bench", action="store_true", help="keep the hook timings already in stats.json")
    a = ap.parse_args()
    state = a.state or state_dir()
    if not state:
        sys.exit("no Foreman state for this repo (FOREMAN_HOME/state/projects/foreman-*)")
    old = {}
    if os.path.isfile(OUT):
        with open(OUT, encoding="utf-8") as f:
            old = json.load(f)
    stats = {"generated": datetime.date.today().isoformat(), **ledger(state, None), "releases": releases(),
             "cards": cards(), "bench": old.get("bench", {}) if a.no_bench else bench(),
             "duels": [dict(d, name=n) for n, d in ((x.partition("=")[0], duel(*x.partition("=")[2].split("@", 1)))
                                                     for x in (a.duel or [f"quality={state}"])) if d]
             or old.get("duels") or []}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=1)
        f.write("\n")
    print(f"wrote {OUT}: {stats['totals']['tasks_done']} tasks, {len(stats['daily'])} days, "
          f"{len(stats['releases'])} releases, {len(stats['bench'])} hook timings")


if __name__ == "__main__":
    main()
