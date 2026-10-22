"""fm scout (T-0950): Foreman finds its own work, so nobody has to ask. Zero-token probes look for a newer Claude Code to
adopt, dependencies in the user's projects that no stack card covers, doctor failures, skill sources gone stale, and an
empty queue that wants a brainstorm round. Each finding is captured once, under a key of its own, into the inbox; the
drive then plans and works it under full autonomy. Bounded: MAX_CAPTURES a run, MAX_OPEN open at once, one quick run
per GAP_S. The idle Stop runs the quick probes (cached data only) and starts the slow ones (network, doctor, project
scans) detached; fm night runs them all first."""
import collections
import hashlib
import json
import os
import re
import subprocess
import sys
import time

import fmcore as c

CC_TESTED = "2.1.304"  # the Claude Code version Foreman was last adapted to (README says the same)
MAX_CAPTURES = 3
MAX_OPEN = 5
GAP_S = 1800
CACHE_S = 12 * 3600
SOURCES_STALE_S = 7 * 86400
_VERSION = re.compile(r"^\d+\.\d+\.\d+$")
SLOW_GAP_S = 6 * 3600  # the drain asks for the slow probes at most this often

Finding = collections.namedtuple("Finding", "key title type tier why")


def _ver(v):
    return tuple(int(x) for x in v.split(".")) if isinstance(v, str) and _VERSION.match(v) else None


def _cache_path():
    return os.path.join(c.state_dir(), "scout.json")


def _cache():
    try:
        with open(_cache_path(), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def _save_cache(**kw):
    data = dict(_cache(), **kw)
    c.write_atomic(_cache_path(), json.dumps(data, indent=1))


# ---------------------------------------------------------------- probes: (p, ctx) -> [Finding]

def probe_claude_code(p, ctx):
    latest, installed = _ver(ctx.get("latest")), _ver(ctx.get("installed"))
    if not latest:
        return []
    have = max(x for x in (installed, _ver(CC_TESTED)) if x)
    if latest <= have:
        return []
    v = ctx["latest"]
    return [Finding(f"cc:{v}", f"Adopt Claude Code {v}: install it and take its new features and fixes into Foreman",
                    "FEATURE", "M", f"published {v}; installed {ctx.get('installed') or 'unknown'}; Foreman tested on "
                    f"{CC_TESTED}. Read its changelog since {CC_TESTED}, adopt what helps, re-verify the hooks and the "
                    f"pane, then raise CC_TESTED and the README")]


def probe_lib_gaps(p, ctx):
    """Dependencies used in the user's projects that no card's dep: signal covers and no earlier finding named, most
    used first. Cards live in Foreman's own repo, so without named roots it runs there only."""
    import fmlib
    if not ctx.get("roots") and os.path.realpath(p.root or "") != os.path.realpath(os.path.dirname(c.PLUGIN_ROOT)):
        return []
    roots = ctx.get("roots") or [x.root for x, _ in c.all_projects() if x.root and os.path.isdir(x.root)]
    asked = {d for k in c.read_meta(p).get("scout_keys") or {} if k.startswith("libgap:") for d in k[7:].split(",")}
    seen = fmlib.uncovered_deps(roots, asked)
    top = [d for d, _ in sorted(seen.items(), key=lambda kv: (-kv[1], kv[0]))[:8]]
    if not top:
        return []
    return [Finding("libgap:" + ",".join(sorted(top)), f"Write stack cards for {', '.join(top[:5])}", "FEATURE", "S",
                    f"dependencies in your projects with no stack card: {', '.join(top)}. Write one card each to the "
                    f"spec in plugin/skills/library/SKILL.md (a writer subagent per batch), then fm lib check")]


def probe_brainstorm(p, ctx):
    """An empty queue and inbox with no brainstorm in 7 days: a round of fm ideas, grounded and queued."""
    if any(b.status not in c.CLOSED for b in c.load_briefs(p)):
        return []
    folder = os.path.join(p.dir, "research")
    stamps = [m.group(1) for n in (os.listdir(folder) if os.path.isdir(folder) else [])
              for m in [re.match(r"brainstorm-(\d{8})", n)] if m]
    recent = time.strftime("%Y%m%d", time.gmtime(time.time() - 7 * 86400))
    if any(s >= recent for s in stamps):
        return []
    week = time.strftime("%G-W%V", time.gmtime())
    return [Finding(f"brainstorm:{week}", "Brainstorm round: what Foreman should build or fix next", "RESEARCH", "M",
                    "the queue and inbox are empty and no brainstorm ran this week: /foreman:brainstorm, a cheap "
                    "probe first (two lenses), ground every idea, queue the ones worth building")]


def probe_friction(p, ctx):
    """No self-improvement pass scheduled (fm friction --every), none in 7 days, and at least 3 tasks closed since:
    one pass this week, so Foreman fixes its own friction without being asked."""
    meta = c.read_meta(p)
    if int(meta.get("rsi_every") or 0) > 0 or (meta.get("rsi_at") and (c.age_days(meta["rsi_at"]) or 0) < 7):
        return []
    start = meta.get("rsi_at") or ""
    done = sum(1 for e in c.tail_jsonl(os.path.join(p.dir, "ledger.jsonl"), 6000)
               if e.get("event") == "task_done" and (e.get("ts") or "") >= start)
    if done < 3:
        return []
    import fmfriction
    return [Finding("friction:" + time.strftime("%G-W%V", time.gmtime()), "Self-improvement pass: Foreman's own "
                    "friction since the last one", "RESEARCH", "S", f"{done} tasks closed and no pass in a week: "
                    + fmfriction.ACTION)]


def probe_doctor(p, ctx):
    try:
        r = subprocess.run([sys.executable, os.path.join(c.PLUGIN_ROOT, "bin", "fm"), "doctor", "--json"], cwd=p.root,
                           capture_output=True, text=True, timeout=120, env=dict(os.environ, FOREMAN_NO_BACKGROUND="1"))
    except subprocess.TimeoutExpired:
        raise OSError("fm doctor --json took over 120 s")
    rows = json.loads(r.stdout)["results"]  # a broken answer is a probe error (logged), never "nothing found"
    out = []
    for row in rows if isinstance(rows, list) else []:
        if isinstance(row, dict) and row.get("status") == "FAIL":
            detail = c.plain(str(row.get("detail", "")))
            key = "doctor:" + str(row.get("name")) + ":" + hashlib.sha1(detail.encode()).hexdigest()[:8]
            out.append(Finding(key, f"Fix the doctor's {row.get('name')} check", "FIX", "S", c.fit(detail, 300)))
    return out


def probe_sources(p, ctx):
    """Skill sources older than a week are refreshed (a read-only data index: no item, no code run)."""
    import calendar
    import fmlib
    if ctx.get("dry"):
        return []
    out = []
    for meta, _ in fmlib.sources():
        added = meta.get("added") or ""
        try:
            age = time.time() - calendar.timegm(time.strptime(added, "%Y-%m-%dT%H:%M:%SZ"))
        except ValueError:
            age = SOURCES_STALE_S
        if age >= SOURCES_STALE_S:
            try:
                new = fmlib.source_add(meta["url"], meta["name"], replace=True)
            except Exception:  # offline, or the repo moved: next time
                continue
            moved = fmlib.class_change(meta, new[0]) if isinstance(new, tuple) else ""
            if moved:  # T-1389: a licence class that moved is one finding, never silent
                out.append(Finding(f"licence:{new[0].get('name')}:{new[0].get('class')}:"
                                   f"{str(new[0].get('commit', ''))[:8]}", f"Source {moved}",
                                   "RESEARCH", "S", f"fm lib source refreshed {c.plain(str(meta['name']))}; its licence "
                                   "class moved. Read the new licence and decide whether the source stays a default."))
    return out


QUICK = [("claude-code", probe_claude_code), ("friction", probe_friction), ("brainstorm", probe_brainstorm)]
SLOW = [("claude-code", probe_claude_code), ("library gaps", probe_lib_gaps), ("doctor", probe_doctor),
        ("sources", probe_sources), ("friction", probe_friction), ("brainstorm", probe_brainstorm)]


# ---------------------------------------------------------------- running and capturing

def _installed():
    try:
        r = subprocess.run(["claude", "--version"], capture_output=True, text=True, timeout=20)
        m = re.search(r"\d+\.\d+\.\d+", r.stdout or "")
        return m.group(0) if m else None
    except (OSError, subprocess.SubprocessError):
        return None


def _latest():
    import urllib.request
    try:
        with urllib.request.urlopen("https://downloads.claude.ai/claude-code-releases/latest", timeout=5) as r:
            v = r.read(64).decode("ascii", "replace").strip()
    except Exception:  # offline, a timeout, a block: unknown, never "no update"
        return None
    return v if _VERSION.match(v) else None


def context(slow=False, dry=False):
    """What the probes read: the published and installed Claude Code versions, from the environment (tests), else a
    fresh fetch (slow runs, successes cached unless dry) or the cache (quick runs: no network in a hook)."""
    cache = _cache()
    latest, installed = os.environ.get("FOREMAN_SCOUT_LATEST"), os.environ.get("FOREMAN_SCOUT_INSTALLED")
    if slow and not latest and time.time() - (cache.get("cc_latest_at") or 0) >= CACHE_S:
        got = _latest()
        if got and dry:
            cache = dict(cache, cc_latest=got)
        elif got:
            _save_cache(cc_latest=got, cc_latest_at=time.time())
            cache = _cache()
    if slow and not installed:
        got = _installed()
        if got and dry:
            cache = dict(cache, cc_installed=got)
        elif got:
            _save_cache(cc_installed=got)
            cache = _cache()
    return {"latest": latest or cache.get("cc_latest"), "installed": installed or cache.get("cc_installed"), "dry": dry}


def run_probes(p, probes, ctx):
    found, errors = [], []
    for name, fn in probes:
        try:
            found += fn(p, ctx) or []
        except Exception as e:  # one failing probe never stops the others
            errors.append(f"{name}: {type(e).__name__}: {c.fit(str(e), 120)}")
    return found, errors


def capture(p, findings, dry=False):
    """New inbox items for the findings not captured before under their key; at most MAX_CAPTURES now and MAX_OPEN
    open scout items in all. Returns the new ids (none when dry)."""
    import fmcli
    made = []
    with c.lock(p.dir):
        meta = c.read_meta(p)
        keys = dict(meta.get("scout_keys") or {})
        open_n = sum(b.meta.get("source") == "scout" and b.status not in c.CLOSED for b in c.load_briefs(p))
        for f in findings:
            if f.key in keys or len(made) >= MAX_CAPTURES or open_n + len(made) >= MAX_OPEN:
                continue
            if dry:
                made.append(f.key)
                continue
            b = fmcli._create(p, c.fit(f.title, 120), f.type, f.tier, "captured", raw=f"Found by fm scout: {f.why}",
                              source="scout")
            c.log_event(p, "capture", task=b.id, data={"source": "scout", "key": f.key})
            keys[f.key] = b.id
            made.append(b.id)
        if made and not dry:
            meta = c.read_meta(p)
            meta["scout_keys"] = keys
            c.write_meta(p, meta)
            c.regen_views(p)
    return [] if dry else made


def due(p):
    return time.time() - float(c.read_meta(p).get("scout_at") or 0) >= GAP_S


def run(p, slow=False, dry=False):
    """One scout run; a real one is ledgered with what it captured and each probe that failed.
    ponytail: probes run in-process with no deadline of their own; fm night's job timeout bounds a hung slow run."""
    found, errors = run_probes(p, SLOW if slow else QUICK, context(slow, dry))
    made = capture(p, found, dry=dry)
    if not dry:
        c.update_meta(p, scout_at=time.time(), **({"scout_slow_at": time.time()} if slow else {}))
        c.log_event(p, "scout", data={"slow": slow, "captured": made, "errors": errors})
    return made, found, errors


def idle(p):
    """The drained queue's Stop: the quick probes now (cached data, no network). (new ids, whether to ask Claude to
    run the slow probes): asked when the quick ones found nothing and none ran in SLOW_GAP_S, so what they capture
    reaches this session's drive instead of waiting in the inbox for the next one."""
    made, _, _ = run(p)
    slow_due = time.time() - float(c.read_meta(p).get("scout_slow_at") or 0) >= SLOW_GAP_S
    return made, not made and slow_due and not os.environ.get("FOREMAN_SCOUT_QUICK_ONLY")


def cmd_scout(args):
    import fmcli
    p = fmcli.resolve(args)
    made, found, errors = run(p, slow=args.slow or args.dry, dry=args.dry)
    lines = [f"  {f.key:<34} {c.fit(f.title, 90)}" for f in found]
    head = ("fm scout (dry run): what it would capture" if args.dry else
            f"fm scout: captured {', '.join(made)}" if made else "fm scout: nothing new to capture")
    fmcli.out(args, {"captured": made, "found": [f._asdict() for f in found], "errors": errors},
              "\n".join([head] + lines + [f"  probe failed: {e}" for e in errors]))
