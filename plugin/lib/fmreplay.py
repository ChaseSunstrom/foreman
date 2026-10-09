"""T-0189: the guard replayed on real commands. Every shell command Claude ran in recent Claude Code sessions (their logs
under ~/.claude/projects) goes through the current guard, with no grants, in the folder it ran in, and the verdicts are
compared with the last accepted ones: a guard change shows which real commands it now blocks (a likely false positive)
or now lets through (a possible bypass). The baseline keeps a hash and a verdict per command, never the command."""
import glob
import hashlib
import json
import os
import time

import fmcore as c

DAYS = 14  # how far back the session logs are read
MAX = 5000  # distinct commands, newest sessions first
SHOW = 10  # changed commands listed per kind


def _logs(days):
    root = os.path.join(os.path.expanduser("~"), ".claude", "projects")
    since = time.time() - days * 86400
    files = [f for f in glob.glob(os.path.join(root, "**", "*.jsonl"), recursive=True) if os.path.getmtime(f) >= since]
    return sorted(files, key=os.path.getmtime, reverse=True)


def corpus(days=DAYS, cap=MAX):
    """[(command, cwd)], distinct, from the Bash tool calls in recent session logs."""
    seen, out = set(), []
    for path in _logs(days):
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                for line in f:
                    if '"Bash"' not in line:
                        continue
                    try:
                        entry = json.loads(line)
                    except ValueError:
                        continue
                    content = (entry.get("message") or {}).get("content") if isinstance(entry, dict) else None
                    for block in content if isinstance(content, list) else []:
                        cmd = (block.get("input") or {}).get("command") if isinstance(block, dict) and \
                            block.get("type") == "tool_use" and block.get("name") == "Bash" else None
                        key = (cmd, entry.get("cwd") or "")
                        if isinstance(cmd, str) and cmd.strip() and key not in seen:
                            seen.add(key)
                            out.append(key)
                            if len(out) >= cap:
                                return out
        except OSError:
            continue
    return out


def _key(cmd, cwd):
    return hashlib.sha256(f"{cwd}\0{cmd}".encode("utf-8", "replace")).hexdigest()[:20]


def _ctx(cwd, g=None):
    """The guard's context with no grants, in the folder a command runs in."""
    if g is None:
        import fmguard as g
    home = os.path.expanduser("~")
    cwd = cwd or home
    return g.Ctx(cwd=cwd, project_root=g.project_root_for(cwd, home), home=home, foreman_home=c.foreman_home(),
                 state_dir=c.state_dir(), state_fallbacks=c.state_fallbacks(), scratch=["/tmp", "/var/tmp"])


def verdicts(cmds, g=None):
    """{key: the category the guard blocks it with, or 'allow'} with no grants, each in the folder it ran in; g: another
    guard module (a candidate, T-0712)."""
    if g is None:
        import fmguard as g
    import warnings
    warnings.simplefilter("ignore", SyntaxWarning)  # the guard parses Python inside commands; their escapes aren't ours
    home, out = os.path.expanduser("~"), {}
    for cmd, cwd in cmds:
        cwd = cwd or home
        ctx = _ctx(cwd, g)
        try:
            b = g.check("Bash", {"command": cmd}, ctx)
            out[_key(cmd, cwd)] = b.category if b else "allow"
        except Exception as e:  # the guard fails closed in the hook; here it is a finding of its own
            out[_key(cmd, cwd)] = f"error: {type(e).__name__}"
    return out


def _baseline_path():
    return os.path.join(c.state_dir(), "guard-replay.json")


def candidate(ref):
    """A candidate guard as a module: a file path, or a git ref of Foreman's own repo (its plugin/lib/fmguard.py)."""
    import importlib.util
    import subprocess
    import tempfile
    if os.path.isfile(ref):
        path = ref
    else:
        repo = os.path.dirname(c.PLUGIN_ROOT)
        src = subprocess.run(["git", "-C", repo, "show", f"{ref}:plugin/lib/fmguard.py"], capture_output=True, text=True)
        if src.returncode:
            raise ValueError(f"no plugin/lib/fmguard.py at {ref}: {src.stderr.strip()[:200]}")
        path = os.path.join(tempfile.mkdtemp(prefix="fm-cand-"), "fmguard_candidate.py")
        with open(path, "w") as f:
            f.write(src.stdout)
    spec = importlib.util.spec_from_file_location("fmguard_candidate", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def score(args, fmcli):
    """T-0712: a candidate guard against the working one on the corpus: what it would loosen (allow where the working
    guard blocks: each one a possible bypass to review) and tighten (new refusals: friction). Exit 1 when it loosens."""
    t0 = time.monotonic()
    try:
        cand = candidate(args.candidate)
    except (ValueError, OSError, SyntaxError) as e:
        raise fmcli.UsageError(f"candidate {args.candidate}: {e}")
    cmds = corpus(args.days)
    now, new = verdicts(cmds), verdicts(cmds, cand)
    by_key = {_key(cmd, cwd or os.path.expanduser("~")): cmd for cmd, cwd in cmds}
    loosened = [k for k in now if now[k] != "allow" and new.get(k) == "allow"]
    tightened = [k for k in now if now[k] == "allow" and new.get(k) not in (None, "allow")]
    changed = [k for k in now if k not in loosened and k not in tightened and new.get(k) != now[k]]
    show = lambda k: c.fit(c.redact(" ".join(by_key[k].split())), 140)
    lines = [f"Candidate {args.candidate} on {len(cmds)} real commands ({time.monotonic() - t0:.1f} s): "
             f"{len(loosened)} loosened, {len(tightened)} tightened, {len(changed)} recategorised"]
    for title, keys in (("loosened (allowed now: review each as a possible bypass)", loosened),
                        ("tightened (new refusals: friction)", tightened)):
        if keys:
            lines.append(f"  {title}:")
            lines += [f"    {now[k]} → {new[k]} · {show(k)}" for k in keys[:SHOW]]
    fmcli.out(args, {"commands": len(cmds), "loosened": len(loosened), "tightened": len(tightened),
                     "recategorised": len(changed)}, "\n".join(lines))
    if loosened:
        raise SystemExit(1)


def cmd_replay(args):
    import fmcli
    if getattr(args, "candidate", None):
        return score(args, fmcli)
    if args.cwd and not args.cmd:  # T-0293: accepted and ignored was worse than refused
        raise fmcli.UsageError("--cwd goes with --cmd: the folder that one command would run in")
    if args.cmd:  # T-0287: one command's verdict, asked and never run (no grants: what the guard says by default)
        import fmguard as g
        b = g.check("Bash", {"command": args.cmd}, _ctx(os.path.abspath(args.cwd or os.getcwd())))
        return fmcli.out(args, {"verdict": b.category if b else "allow", "detail": b.detail if b else None},
                         f"blocked {b.category}: {c.plain(b.detail)}" if b else "allow")
    t0 = time.monotonic()
    cmds = corpus(args.days)
    now = verdicts(cmds)
    path = _baseline_path()
    try:
        with open(path, encoding="utf-8") as f:
            base = json.load(f)
    except (OSError, ValueError):
        base = {}
    old = base.get("verdicts") or {}
    by_key = {_key(cmd, cwd or os.path.expanduser("~")): (cmd, cwd) for cmd, cwd in cmds}
    blocked = [k for k, v in now.items() if k in old and v != "allow" and old[k] != v]
    allowed = [k for k, v in now.items() if k in old and v == "allow" and old[k] != "allow"]
    fresh = sum(1 for k in now if k not in old)
    if args.accept:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        c.write_atomic(path, json.dumps({"at": c.now(), "verdicts": {**old, **now}}, sort_keys=True))
    res = {"commands": len(cmds), "since_days": args.days, "baseline": base.get("at"), "newly_blocked": len(blocked),
           "newly_allowed": len(allowed), "new": fresh, "seconds": round(time.monotonic() - t0, 1),
           "accepted": bool(args.accept)}
    show = lambda k: c.fit(c.redact(" ".join(by_key[k][0].split())), 140)
    lines = [f"Guard replay: {len(cmds)} real commands from the last {args.days} days of sessions "
             f"({res['seconds']} s) · baseline {base.get('at') or 'none yet'}"]
    for title, keys in (("newly blocked (likely false positives)", blocked), ("newly allowed (possible bypasses)", allowed)):
        lines.append(f"  {len(keys)} {title}")
        lines += [f"    {old.get(k)} → {now[k]} · {show(k)}" for k in keys[:SHOW]]
        if len(keys) > SHOW:
            lines.append(f"    … {len(keys) - SHOW} more")
    lines.append(f"  {fresh} new to the corpus" + (" · accepted as the baseline" if args.accept else
                 " · fm replay --accept takes these verdicts as the baseline" if blocked or allowed or not old else ""))
    fmcli.out(args, res, "\n".join(lines))
    if (blocked or allowed) and not args.accept:
        raise SystemExit(1)
