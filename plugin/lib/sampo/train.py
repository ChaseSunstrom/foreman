"""T-3380: sampo lane train, a merge queue. Reviewed lanes merge one after another in a scratch integration worktree
(never the main checkout); the project's gates run once on the result; a red set is bisected to its culprit lanes by
prefix (each probe a gate run), which are dropped; the main checkout's branch then fast-forwards to the gated tip.
The train's check_run carries the code tree (core.code_tree: no CHANGELOG.md, no sync mirror), so `sampo check` after
each close reuses the pass while the code is unchanged. T-3544: the full-suite gate runs only the tests the batch's
changes reach (_affected_gate); the full suite then runs on the landed merges in the background (lanes.pm_run)."""
import concurrent.futures
import os
import re
import shlex
import shutil
import tempfile
import time

from sampo import core as c
from sampo.lanes import _git, _ref_ok, _verify, pm_record, pm_rerun_cmd, pm_wait

PROBE_JOBS = 3  # T-3531: pre-filter probes at once
_CLASS = re.compile(r"^(?:FAIL|ERROR): \S+ \(([\w.]+?)\.\w+\)", re.M)  # the red classes unittest names (release.py too)
_stem = lambda t: os.path.basename(t).rsplit(".", 1)[0]  # noqa: E731  a test file's module name


def _affected_gate(p, wt, base, checks):
    """T-3544: (the full-suite gate, the affected template, the tests the merged batch reaches) or None to run every
    gate as configured. The full suite is the gate equal to the affected template's runner with no names (`python3
    plugin/tests/run.py`); the tests are cli.affected's since the base on the merged tree, as the probes pick them,
    the rule tests among them. None: FOREMAN_FULL_GATE=1, no such gate, or nothing picked (the full suite decides)."""
    from sampo import cli
    meta = c.read_meta(p)
    tpl = meta.get("affected") or ""
    bare = lambda s: " ".join(s.split())  # noqa: E731
    full = next((g for g in checks if bare(g) == bare(tpl.replace("{names}", "").replace("{tests}", ""))), None)
    if os.environ.get("FOREMAN_FULL_GATE") or not tpl or not full:
        return None
    try:
        _, tests, _ = cli.affected(c.Project(p.slug, wt, p.dir, p.lane), since=base)
    except Exception:  # no affected command or no map: the full suite decides
        return None
    tests = [t for t in tests if not t.endswith(tuple(meta.get("affected_by") or ()))]  # another runner's: its own gate
    return (full, tpl, tests) if tests else None


def _why_red(r):
    """T-3544: a red gate run as a reason: the gate (on how many affected modules), the classes it names failing and
    its last 15 lines, so nobody reruns a full suite to learn them."""
    s = r["cmd"] + (f" on {len(r['affected'])} affected test module(s)" if r.get("affected") else "")
    s += f", failing {c.joinmore(r['failing'], 8)}" if r.get("failing") else ""
    return s + "".join("\n    " + ln for ln in r.get("tail") or ())


def _merge_in(wt, b, tip, log):
    """Merge `tip` into the scratch tree; a conflict is aborted and logged (id, files). The new head sha or None."""
    r = _git(wt, "-c", "user.name=sampo", "-c", "user.email=sampo@localhost", "merge", "--no-ff", "-m",
             f"Merge {b.id}: {b.title}", tip)
    if not r.returncode:
        return _git(wt, "rev-parse", "HEAD").stdout.strip()
    files = [f for f in _git(wt, "diff", "--name-only", "--diff-filter=U", "-z").stdout.split("\0") if f]
    _git(wt, "merge", "--abort")
    log.append((b.id, "conflicts with an earlier lane in the train" + (f": {c.joinmore(files, 8)}" if files else "")))
    return None


def _probe(p, main, base, b, tip, notes):
    """T-3474: why this lane can't land, known before any full gate run, or ''. `git merge-tree` names a conflict with
    the base in milliseconds; the tests affected by the lane's change (cli.affected, as `sampo ship` runs them first)
    run on base+lane in a throwaway tree, naming a red lane in a minute instead of a bisection of full gate runs. A
    timeout (124) or a run of no tests (5) proves nothing, so the lane goes on to the gates. Before blaming, the red
    classes rerun once on base+lane (green: a flake) and then on the bare base (red there too: the base's); each goes
    on to the gates with a line in `notes`."""
    from sampo import cli
    r = _git(main, "merge-tree", "--write-tree", "--name-only", "--no-messages", base, tip)
    if r.returncode == 1:  # 1 is a conflict; any other failure (an old git) leaves it to the train's own merge
        files = r.stdout.splitlines()[1:]  # the first line is the merged tree
        return "conflicts with the base" + (f": {c.joinmore(files, 8)}" if files else "")
    wt = tempfile.mkdtemp(prefix="sampo-probe-")
    try:
        if _git(main, "worktree", "add", "-q", "--detach", wt, base).returncode or _git(
                wt, "-c", "user.name=sampo", "-c", "user.email=sampo@localhost", "merge", "--no-ff", "--no-edit",
                tip).returncode:
            return ""
        pw = c.Project(p.slug, wt, p.dir, p.lane)
        try:
            cmd, tests, changed = cli.affected(pw, since=base)
        except Exception:  # no affected command configured, or no map: the full gates still decide
            return ""
        if not cmd:
            return ""
        held = _ran_green(pw, b, tests, changed)
        if held:
            notes.append((b.id, f"probe skipped: its own green run of these {len(tests)} test(s) on tree {held[:9]} "
                                "still holds (nothing they cover differs from base+lane)"))
            return ""
        def run(cmd):  # (exit, the classes it names red)
            cwd, cmd, _ = c.normalize_verify(wt, cmd)  # T-3411's cwd fix first: the nice wrapper would hide it
            if shutil.which("nice"):  # the probe yields to whatever else the machine runs
                cmd = "nice -n 10 bash -c " + shlex.quote(cmd)
            code, out = c.run_command(cwd, cmd, c.load_scaled(900))
            return code, set(_CLASS.findall(out))

        def again(classes):  # the red classes alone where the runner names them (pm_rerun_cmd), else cmd again
            return run(pm_rerun_cmd(wt, sorted(classes)) or cmd)

        code, bad = run(cmd)
        if code in (0, 5, 124):
            return ""
        if not bad:
            return f"its affected tests fail on the base: exit {code}"
        code, red = again(bad)
        still = ((bad & red) or bad) if code else set()  # a flake is green on the rerun; a red naming none stays red
        if bad - still:
            notes.append((b.id, f"flaky (red once, green on a rerun): {c.joinmore(sorted(bad - still), 6)}"))
        _git(wt, "reset", "-q", "--hard", base)
        based = (still & again(still)[1]) if still else set()  # red without the lane too: the base's, not the lane's
        if based:
            notes.append((b.id, f"its affected tests are red on the base itself: {c.joinmore(sorted(based), 6)}; "
                                "left to the gates"))
        blame = still - based
        return "its affected tests fail on the base: " + c.joinmore(sorted(blame), 6) if blame else ""
    finally:
        _git(main, "worktree", "remove", "--force", wt)
        shutil.rmtree(wt, ignore_errors=True)
        _git(main, "worktree", "prune")


def _ran_green(p, b, tests, changed):
    """T-3531: a tree the lane's own evidence ran every one of `tests` green on (ran, exit 0, each named by path or
    bare name), when its diff to base+lane (p.root's HEAD) touches none of the tests, the sources the map links them to
    or the lane's changed files: that run still holds, so the probe needn't repeat it; '' when none does. Evidence keeps
    no base, but its tree is base+lane as it ran, which is the base's diff and the lane's later edits in one. A wrong
    skip costs a bisection, never a red landing: the full gates still run."""
    from sampo import map as smap
    links = smap.load(p).get("tests") or {}
    cover = set(tests) | set(changed) | {s for t in tests for s in links.get(t, [])}
    dirs = tuple(s for s in cover if s.endswith("/"))  # a folder link (site/) covers what's under it
    now = _git(p.root, "rev-parse", "HEAD^{tree}").stdout.strip()
    holds, named, last = {}, set(), ""
    for line in b.evidence():
        m, t = re.match(r"- (?:\((?:step|ac) \d+\) )?`(.*?)` → exit 0 ", line), c._TREE_MARK.search(line)
        if not (m and t and c._RAN_MARK in line) or c.NEVER_RAN in line:
            continue
        tree = t.group(1)
        if tree not in holds:
            d = _git(p.root, "diff", "--name-only", tree, now)
            holds[tree] = not d.returncode and not any(f in cover or f.startswith(dirs) for f in d.stdout.splitlines())
        if holds[tree]:
            named |= set(m.group(1).split())
            last = tree
    return last if last and all(t in named or os.path.basename(t).rsplit(".", 1)[0] in named for t in tests) else ""


def _held(p, b, main, tip):
    """The reason `sampo lane merge` would refuse this lane's files (guard, self-change gate), or ''."""
    import fmguard
    from sampo import selfgate
    meta = c.read_meta(p)
    ctx = fmguard.Ctx(cwd=main, project_root=main, home=os.path.expanduser("~"), foreman_home=c.foreman_home(),
                      state_dir=c.state_dir(), state_fallbacks=c.state_fallbacks(), scratch=[],
                      allow=set(b.meta.get("allow") or []), task_id=b.id, standing=set(meta.get("standing") or {}),
                      trusted=bool(c.trusted()))
    files = [f for f in _git(main, "diff", "--name-only", "--no-renames", "-z", f"HEAD...{tip}").stdout.split("\0") if f]
    for f in files:
        blk = fmguard.check("Write", {"file_path": os.path.join(main, f), "content": ""}, ctx)
        if blk:
            return f"the guard refuses {f} ({blk.category})"
    held = selfgate.gate(p, b, main, tip, files)
    return "the self-change gate holds it: " + c.joinmore(held, 4, "; ") if held else ""


def train(p, main, ids=None):
    """Land the named `ids` (a bare train would land lanes nobody picked) through one gate run, one train at a time.
    Returns a dict: merged, left_out [(id, why)], gate_runs, tip, branch. Raises PolicyError when nothing can land, the
    base is red or the branch moved."""
    from sampo import cli
    ids = list(dict.fromkeys(ids or []))
    if not ids:
        raise cli.UsageError("name the lanes to land: sampo lane train T-0001,T-0002 (it never lands a lane nobody picked)")
    with c.lock(os.path.join(p.dir, "train"), timeout=1):  # a second train, not a lane merge, waits on this one
        return _run(p, main, ids)


def _run(p, main, ids):
    from sampo import cli
    checks = list(c.read_meta(p).get("checks") or [])
    if not checks:
        raise cli.UsageError("no checks configured: sampo check add '<cmd>'")
    branch = _git(main, "symbolic-ref", "--short", "-q", "HEAD").stdout.strip()
    base = _git(main, "rev-parse", "HEAD").stdout.strip()
    if not branch or not base:
        raise c.PolicyError(f"{main} is on no branch: check one out for the train to fast-forward")
    pm_wait(p, main)
    pre_tree = c.worktree_tree(main)
    left, notes = [], []  # notes: (id, what a probe saw that still let the lane on)
    cands, rows = [], []  # (brief, tip) in order; (brief, tip, why so far) in order
    for tid in ids:
        b = cli.need_brief(p, tid)
        br = b.meta.get("lane_branch") or f"foreman/{b.id}"
        if b.meta.get("lane_spike"):
            rows.append((b, None, "a spike is never merged"))
        elif not _ref_ok(main, br):
            rows.append((b, None, f"no branch {br}"))
        else:
            tip = _git(main, "rev-parse", "--verify", f"{br}^{{commit}}").stdout.strip()
            rows.append((b, tip, _held(p, b, main, tip)))

    def check(row):  # (why it can't land or '', its own notes): lanes run at once, so each keeps its own notes
        b, tip, why = row
        seen = []
        if not why:  # as `lane merge` does: the lane's own acceptance commands re-run in its worktree
            try:
                _verify(b)
            except (c.PolicyError, cli.UsageError) as e:
                why = str(e).splitlines()[0]
        return why or _probe(p, main, base, b, tip, seen), seen  # T-3474: conflicts and red affected tests, before any gate run

    # T-3531: PROBE_JOBS lanes at once, each in its own scratch tree (one on a host over 2x its CPUs); map keeps the
    # candidate order, so the left-out list and notes read as a serial run's
    with concurrent.futures.ThreadPoolExecutor(1 if c.host_strain(2.0) else PROBE_JOBS) as ex:
        for (b, tip, _), (why, seen) in zip(rows, list(ex.map(check, rows))):
            notes += seen
            left.append((b.id, why)) if why else cands.append((b, tip))
    if not cands:
        raise c.PolicyError("nothing to merge: " + "; ".join(f"{i}: {w}" for i, w in left))
    wt = tempfile.mkdtemp(prefix="sampo-train-")  # outside the main checkout; git worktree add takes the empty dir
    r = _git(main, "worktree", "add", "-q", "--detach", wt, base)
    if r.returncode:
        raise c.PolicyError(f"git worktree add failed: {r.stderr.strip()[:300]}")
    runs, results, sub = [0], [], None

    def build(start, lanes):
        """Reset the scratch tree to `start`, merge `lanes`; [(brief, sha after)] of those that merged."""
        _git(wt, "reset", "-q", "--hard", start)
        out = []
        for b, tip in lanes:
            sha = _merge_in(wt, b, tip, left)
            if sha:
                out.append((b, sha))
        return out

    def moved():
        return _git(main, "rev-parse", "HEAD").stdout.strip() != base or \
            _git(main, "symbolic-ref", "--short", "-q", "HEAD").stdout.strip() != branch

    def gate():
        """True when every gate passes in the scratch tree as it stands. The full suite runs only the batch's affected
        tests found there (T-3544: a prefix or the base lacks a later lane's new test file); a red row keeps the
        classes it names failing and its last 15 lines."""
        c.wait_for_load("sampo lane train")
        runs[0] += 1
        results.clear()
        for cmd in checks:
            ts = [t for t in sub[2] if os.path.exists(os.path.join(wt, t))] if sub and cmd == sub[0] else []
            run = sub[1].replace("{tests}", shlex.join(ts)).replace("{names}", shlex.join(map(_stem, ts))) if ts else cmd
            t0 = time.monotonic()
            code, out = c.run_command(wt, run, c.load_scaled(1800))
            results.append({"cmd": cmd, "exit": code, "s": round(time.monotonic() - t0, 1)})
            if ts:  # the flag the pass's reusers read (cli._cached_pass): only these modules ran
                results[-1]["affected"] = [_stem(t) for t in ts]
            if code:
                results[-1].update(failing=sorted(set(_CLASS.findall(out))), tail=out.rstrip().splitlines()[-15:])
                return False
        return True

    try:
        merged = build(base, cands)
        sub = _affected_gate(p, wt, base, checks)
        tips = {b.id: t for b, t in cands}
        green, red = [], {}  # the rows of the newest green run; the failing row of the newest red one
        if moved():  # a lane merged meanwhile: don't spend a gate run on a base that is gone
            raise c.PolicyError(f"{branch} moved since the train started (was {base[:9]}): nothing landed; run it again")
        while merged and not gate():
            red = results[-1]
            # prefix bisection: prefix lo is green (0 = base), prefix hi is red; the lane at hi is the culprit
            lo, hi = 0, len(merged)
            while hi - lo > 1:
                mid = (lo + hi) // 2
                _git(wt, "reset", "-q", "--hard", merged[mid - 1][1])
                if gate():
                    lo, green = mid, list(results)
                else:
                    hi, red = mid, results[-1]
            if hi == 1:  # the first lane is blamed on the strength of a base nobody gated: gate it before blaming
                _git(wt, "reset", "-q", "--hard", base)
                if not gate():
                    raise c.PolicyError(f"the base {base[:9]} of {branch} is red; fix it before a train can blame a "
                                        f"lane: {_why_red(results[-1])}")
            why = "its merge turns the gates red: " + _why_red(red)
            left.append((merged[hi - 1][0].id, why))
            cli.mutate(p, merged[hi - 1][0].id, lambda x, w=why: x.append_log("left out of a merge train: " + w),
                       "lane_train_red", {"cmd": red["cmd"], "failing": red.get("failing") or []})
            keep = merged[:hi - 1]
            start = keep[-1][1] if keep else base
            rest = [(b, tips[b.id]) for b, _ in merged[hi:]]
            merged = keep + build(start, rest)  # no rest: the head is prefix lo, which passed above (or is the base)
            if not rest:
                break
        else:
            green = list(results)  # ponytail: a cut prefix with a rest behind it is gated again whole, one more run
        if not merged:
            raise c.PolicyError("nothing landed: " + "; ".join(f"{i}: {w}" for i, w in left))
        tip = _git(wt, "rev-parse", "HEAD").stdout.strip()
        if moved():
            raise c.PolicyError(f"{branch} moved while the train ran (was {base[:9]}): nothing landed; run it again")
        ids_in = [b.id for b, _ in merged]
        for b, _ in merged:  # marked before the fast-forward, so a crash can't leave landed lanes unmarked
            def done(x, b=b):
                for k in ("base", "base_tree", "paused_tree"):
                    x.meta.pop(k, None)
                x.meta.update({"base": base}, **({"base_tree": pre_tree} if pre_tree else {}))
                x.append_log(f"merged {b.meta.get('lane_branch') or 'foreman/' + b.id} in merge train")
                x.meta.update(lane_stop=f"merged {c.now()}")
            cli.mutate(p, b.id, done, "lane_merge", {"train": ids_in})
        ff = _git(main, "merge", "-q", "--ff-only", tip)
        if ff.returncode:
            for b, _ in merged:
                cli.mutate(p, b.id, lambda x: x.meta.update(lane_stop=f"refused {c.now()}: the train's fast-forward failed"),
                           "lane_merge", {"train": ids_in, "undone": True})
            raise c.PolicyError(f"fast-forward of {branch} to {tip[:9]} refused: {(ff.stderr or ff.stdout).strip()[:300]}")
        part = next((r["affected"] for r in green if r.get("affected")), None)
        if part:  # T-3544: the full suite the gate skipped verifies each landed merge in the background, newest first
            for i, (b, sha) in enumerate(merged):
                pm_record(p, sha, b.id, main, spawn=i == len(merged) - 1)
        tree = _git(main, "rev-parse", f"{tip}^{{tree}}").stdout.strip()
        ct = c.code_tree(main, tree)
        c.log_event(p, "check_run", data={"tree": tree[:12], "code_tree": ct, "env": c.env_id(), "train": ids_in,
                                          "results": green})
        return {"merged": ids_in, "left_out": left, "notes": notes, "gate_runs": runs[0], "tip": tip, "branch": branch,
                "affected": part}
    finally:
        _git(main, "worktree", "remove", "--force", wt)
        shutil.rmtree(wt, ignore_errors=True)
        _git(main, "worktree", "prune")


def cmd(p, args, main):
    from sampo import cli
    ids = [x for x in (args.id or "").replace(",", " ").split() if x]  # one positional: T-1,T-2
    got = train(p, main, ids)
    lines = [f"Train: {len(got['merged'])} lane(s) landed on {got['branch']} ({got['tip'][:9]}) in "
             f"{got['gate_runs']} gate run(s): {', '.join(got['merged'])}"]
    lines += [f"  left out {i}: {w}" for i, w in got["left_out"]] + [f"  note {i}: {w}" for i, w in got["notes"]]
    if got["affected"]:
        lines.append(f"The test gate ran {len(got['affected'])} affected test module(s), not the full suite "
                     "(FOREMAN_FULL_GATE=1 runs it); the full suite verifies the landed merges in the background.")
    lines.append("sampo check now reuses this pass while only CHANGELOG.md and the sync mirror change.")
    return cli.out(args, got, "\n".join(lines))

