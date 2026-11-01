"""T-2352: the self-change gate at fm lane merge. A branch that changes Foreman's own plugin/ merges only when it keeps
what the base has: the guard blocks no less (its labelled cases and allow-corpus, the union of base's and branch's so a
deleted case can't hide, plus recent real commands, judged with no grants by each tree's own guard), no hook gets
slower (the hooks of each tree on the base's bench), and the always-on footprint doesn't grow with no cut to pay for it
(T-2358's rule). The harness is always the base's (fmreplay.py, bench_hooks.py and its payloads), so a branch can't
rewrite the judge; trees are built from git's blobs, not git archive (whose .gitattributes a branch controls).
A refusal names the numbers. Only the user's yes to `fm ask ID core` given after a refusal of the same commit passes
it: never the standing yes, never a decision, never a yes for an earlier commit. A gate that can't run refuses with the
reason, and the same yes passes that too."""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

import fmcore as c

CASES = ("plugin/tests/fixtures/guard_cases.jsonl", "plugin/tests/fixtures/guard_allow.jsonl")
HARNESS = ("lib/fmreplay.py", "tests/bench_hooks.py", "tests/fixtures/hook_payloads.json")  # judged by base's copies
RISE = 0.15  # a hook's p95 rise that refuses (T-2358's latency band)
FLOOR_MS = 5.0  # under this, a rise is jitter whatever its share
RUNS = 10  # bench runs per tree; a refusal is benched again and must hold twice
WALL_RISE, WALL_FLOOR_MS = 1.0, 100.0  # T-2363: on a loaded bench, a wall-time rise this big is a hook that waits
CORPUS = 2000  # recent real commands replayed, newest first (fmreplay.corpus)
_RUNNER = ("import json, os, sys\nsys.path.insert(0, sys.argv[1])\nimport fmreplay as r\n"
           "cmds = [(x, r.resolve_cwd(y) if y else y) for x, y in json.load(sys.stdin)]\nv = r.verdicts(cmds)\n"
           "print(json.dumps([v.get(r._key(x, y or os.path.expanduser('~'))) for x, y in cmds]))\n")
# ponytail: base's replay and bench are rerun on every gated merge (2-4 min); cache them by HEAD sha if merges queue up


def _git(main, *a, text=False, input=None):
    return subprocess.run(["git", "-C", main, "-c", "core.fsmonitor=false", "-c", "core.hooksPath=/dev/null", *a],
                          capture_output=True, text=text, input=input, timeout=180)


def _tree(main, sha, dest):
    """sha's committed plugin/ written under dest from git's blobs (links and submodules skipped)."""
    ls = _git(main, "ls-tree", "-r", "-z", "--full-tree", sha, "--", "plugin")
    if ls.returncode:
        raise RuntimeError(f"git ls-tree {sha[:12]}: {ls.stderr.decode(errors='replace').strip()[:160]}")
    files = []
    for rec in filter(None, ls.stdout.split(b"\0")):
        meta, path = rec.split(b"\t", 1)
        mode, kind, blob = meta.split()
        if kind == b"blob" and mode != b"120000":
            files.append((mode, blob, os.path.normpath(path.decode("utf-8", "surrogateescape"))))
    cat = _git(main, "cat-file", "--batch", input=b"".join(blob + b"\n" for _, blob, _ in files))
    out, i, root = cat.stdout, 0, os.path.realpath(dest)
    for mode, blob, rel in files:
        nl = out.index(b"\n", i)
        size = int(out[i:nl].split()[2])
        data, i = out[nl + 1:nl + 1 + size], nl + 2 + size
        dst = os.path.join(root, rel)
        if rel.startswith("..") or os.path.isabs(rel) or not dst.startswith(root + os.sep):
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "wb") as f:
            f.write(data)
        os.chmod(dst, 0o755 if mode == b"100755" else 0o644)
    return os.path.join(root, "plugin")


def _cases(main, sha):
    """{(cmd, cwd): id} of sha's labelled guard cases and allow-corpus."""
    out = {}
    for f in CASES:
        r = _git(main, "show", f"{sha}:{f}", text=True)
        for ln in (r.stdout if r.returncode == 0 else "").splitlines():
            try:
                k = json.loads(ln)
            except ValueError:
                continue
            if isinstance(k, dict) and isinstance(k.get("cmd"), str):
                out[(k["cmd"], str(k.get("cwd") or ""))] = str(k.get("id") or "")
    return out


def _corpus():
    """Recent real commands from Claude Code's session logs (fmreplay.corpus), so coverage isn't only the fixtures."""
    import fmreplay
    return [(cmd, cwd or "") for cmd, cwd in fmreplay.corpus(cap=CORPUS)]


def _env(state):
    """What the tree's code sees: the real home and Foreman home (so core and home rules judge real paths), an empty
    state (no grants, trust or standing yes), and nothing else of this session's environment (no tokens)."""
    keep = ("PATH", "HOME", "LANG", "LC_ALL", "TMPDIR", "FOREMAN_HOME")
    return dict({k: os.environ[k] for k in keep if k in os.environ}, FOREMAN_STATE=state)


def _verdicts(plugin, cmds):
    """Each command's verdict from this tree's own guard, judged by the base's fmreplay."""
    # T-2363: a hook the bench started may still be writing its state as this returns; a leftover file is no reason
    # for the gate to fail (a gate that can't run refuses)
    with tempfile.TemporaryDirectory(prefix="fm-gate-state-", ignore_cleanup_errors=True) as state:
        r = subprocess.run([sys.executable, "-I", "-c", _RUNNER, os.path.join(plugin, "lib")], input=json.dumps(cmds),
                           capture_output=True, text=True, timeout=600, env=_env(state))
    got = json.loads(r.stdout or "null")
    if not isinstance(got, list) or len(got) != len(cmds):
        raise RuntimeError(f"guard replay: {(r.stderr or r.stdout).strip()[-160:]}")
    return got


def _bench(plugin):
    """({fixture: timings}, {event: injected chars}) from the base's bench over this tree's hooks."""
    # T-2363: a hook the bench started may still be writing its state as this returns; a leftover file is no reason
    # for the gate to fail (a gate that can't run refuses)
    with tempfile.TemporaryDirectory(prefix="fm-gate-state-", ignore_cleanup_errors=True) as state:
        r = subprocess.run([sys.executable, "-I", os.path.join(plugin, "tests", "bench_hooks.py"), "--runs", str(RUNS),
                            "--json", "--inject"], cwd=plugin, capture_output=True, text=True, timeout=600,
                           env=_env(state))
    got = json.loads(r.stdout or "null")  # exit 1 is a hook over budget; the JSON still stands
    if not isinstance(got, dict):
        raise RuntimeError(f"hook bench: {r.stderr.strip()[-160:]}")
    return got.get("bench") or {}, got.get("injected") or {}


def _ms(v, loaded):
    x = v.get("cpu_p95") if loaded else v.get("p95")
    return x if isinstance(x, (int, float)) and not isinstance(x, bool) else None


def _slower(base, branch):
    """Hooks whose p95 rose past RISE (and FLOOR_MS) or past the base's budget, on one basis (CPU time if either run
    was loaded). A new fixture takes the base's tightest budget; the branch's own budgets are never read."""
    loaded = any(v.get("load", 0) > 1 for v in list(base.values()) + list(branch.values()))
    tight = min((v["budget"] for v in base.values() if isinstance(v.get("budget"), (int, float))), default=None)
    rows = {}
    for k, v in branch.items():
        b1, b0 = _ms(v, loaded), _ms(base.get(k) or {}, loaded)
        budget = (base.get(k) or {}).get("budget", tight)
        if b1 is None:
            continue
        over = isinstance(budget, (int, float)) and b1 > budget and not (b0 is not None and b0 > budget)
        rise = b0 is not None and b0 > 0 and b1 > b0 * (1 + RISE) and b1 - b0 >= FLOOR_MS
        if over or rise:
            rows[k] = f"hook {k} p95 {b0} -> {b1} ms" + (f" (past its {budget} ms budget)" if over else
                                                          f" (+{(b1 - b0) * 100 / b0:.0f}%)")
        elif loaded:  # CPU time misses a hook that sleeps or waits on I/O: a doubling past 100 ms of wall is no load noise
            w1, w0 = _ms(v, False), _ms(base.get(k) or {}, False)
            if w0 and w1 and w1 >= w0 * (1 + WALL_RISE) and w1 - w0 >= WALL_FLOOR_MS:
                rows[k] = f"hook {k} p95 {w0} -> {w1} ms wall (+{(w1 - w0) * 100 / w0:.0f}%; its CPU time didn't rise: it waits)"
    return rows


def _footprint(plugin, sizes):
    import fmdoctor
    return dict(fmdoctor.footprint(os.path.join(plugin, "rules", "foreman.md"), plugin),
                **fmdoctor.measured(None, sizes))


def _verbs(plugin):
    """T-2363: the fm verbs a tree's fmcli registers (its add("name", …) lines), as fmgenesis._lean counts them."""
    try:
        with open(os.path.join(plugin, "lib", "fmcli.py"), encoding="utf-8", errors="replace") as f:
            return sorted(set(re.findall(r'(?<![.\w])add\("([a-z][\w-]*)"', f.read())))
    except OSError:
        return []


def approved(p, b, sha):
    """The user's yes to `fm ask ID core` on this task, given after its last self-change refusal of this commit."""
    last, yes = None, False
    for e in c.ledger_events(p, ("self_change_refused", "approval_granted"), since=str(b.meta.get("created") or "")):
        if e.get("task") != b.id:
            continue
        if e.get("event") == "self_change_refused":
            last, yes = (e.get("data") or {}).get("sha"), False
        elif last is not None and "core" in ((e.get("data") or {}).get("allow") or []):
            yes = True
    return yes and last == sha


def _judged(f):
    return f.startswith(("plugin/lib/", "plugin/hooks/", "plugin/bin/")) or f in (
        "plugin/settings.json", "plugin/.claude-plugin/plugin.json")


def _benched(f):  # what a hook can run or read: any plugin file but tests and prose, and the changelog SessionStart shows
    return (f.startswith("plugin/") and not f.startswith("plugin/tests/") and not f.endswith(".md")) or f == "CHANGELOG.md"


def gate(p, b, main, ref, files):
    """[refusal lines] for a commit that changes Foreman's own plugin/, [] when it holds, isn't one, or the user said yes
    after its last refusal of this same commit. Each refusal is a self_change_refused ledger event with the sha."""
    if not os.path.isfile(os.path.join(main, "plugin", "lib", "fmguard.py")) or not any(
            f.startswith("plugin/") for f in files):
        return []
    sha = _git(main, "rev-parse", "--verify", f"{ref}^{{commit}}", text=True).stdout.strip()
    if sha and approved(p, b, sha):
        return []
    out, tmp = [], tempfile.mkdtemp(prefix="fm-selfgate-")
    try:
        if not sha:
            raise RuntimeError(f"no commit {ref}")
        head = _git(main, "rev-parse", "HEAD", text=True).stdout.strip()
        base, new = _tree(main, head, os.path.join(tmp, "base")), _tree(main, sha, os.path.join(tmp, "branch"))
        for rel in HARNESS:  # the judge is the base's: a branch can't rewrite how it is measured
            src, dst = os.path.join(base, rel), os.path.join(new, rel)
            if os.path.isfile(src):
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copyfile(src, dst)
        was, now = _cases(main, head), _cases(main, sha)
        out += [f"guard case {i or '?'} removed or changed by the branch: {c.fit(c.redact(cmd), 100)}"
                for (cmd, cwd), i in was.items() if (cmd, cwd) not in now]
        if any(_judged(f) for f in files) or was != now:
            cmds = list(dict.fromkeys(list(was) + list(now) + _corpus()))
            v0, v1 = _verdicts(base, [list(x) for x in cmds]), _verdicts(new, [list(x) for x in cmds])
            for (cmd, _), a, z in zip(cmds, v0, v1):
                broke = not isinstance(z, str) or (z.startswith("error:") and not str(a).startswith("error:"))
                if (a != "allow" and z == "allow") or broke:
                    out.append(f"guard: {c.fit(c.redact(' '.join(cmd.split())), 100)}: base {a}, branch {z}")
        import fmdoctor
        f0, f1 = _footprint(base, {}), _footprint(new, {})
        if any(_benched(f) for f in files) or fmdoctor.grown(f0, f1):  # timings, and the injected chars a cut needs
            (t0, s0), (t1, s1) = _bench(base), _bench(new)
            slow = _slower(t0, t1)
            if slow:  # a rise must hold on a second bench of both trees, or it was noise
                (t0, _), (t1, _) = _bench(base), _bench(new)
                again = _slower(t0, t1)
                slow = {k: again[k] for k in slow if k in again}
            out += list(slow.values())
            f0, f1 = _footprint(base, s0), _footprint(new, s1)
        out += [f"footprint {k} {w} -> {cur} (+{int((cur - w) * 100 // w)}%) with no always-on cut to pay for it"
                for k, w, cur in fmdoctor.grown(f0, f1) if not k.endswith(" ms")]
        v0, v1 = _verbs(base), _verbs(new)  # T-2363: a verb added with none removed is growth too (gen-0 §6)
        added = [v for v in v1 if v not in v0]
        if added and not [v for v in v0 if v not in v1]:
            out.append(f"verbs {len(v0)} -> {len(v1)} (+{len(added)}: {', '.join(added[:5])}) with none removed")
    except (OSError, RuntimeError, ValueError, KeyError, TypeError, IndexError, ZeroDivisionError,
            subprocess.SubprocessError) as e:
        out.append(f"the self-change gate couldn't run ({type(e).__name__}: {c.fit(str(e), 160)})")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    if out:
        c.log_event(p, "self_change_refused", task=b.id, data={"sha": sha, "rows": out[:20]})
    return out
