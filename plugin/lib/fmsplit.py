"""T-0709 (Frontier 09, first slice): a task too big for one session splits along the code's seams into child tasks,
and only a capsule comes back up. fm task split partitions the task's files over the work graph (fm graph: code,
co-change and test edges) so the cut between parts is light, and makes each part a child brief scoped to its files.
fm task capsule is a child's return to its parent: a bounded summary, never the transcript. A parent can't close while
a child is open (fmcli's done gate). Children run through the lanes and builders like any task, and can split again."""
import fnmatch
import os
import re

import fmcore as c

CAPSULE_LINES = 15
KINDS = {"uses": 1.0, "cochange": 1.0, "tests": 2.0}  # a test goes with what it tests


def _files(p, b, given):
    import fmgraph
    if given:
        return sorted(dict.fromkeys(given))
    tracked = c._git(p.root, "ls-files", timeout=60).splitlines()
    scope = b.meta.get("scope") or []
    if scope:
        return sorted(f for f in tracked if any(fnmatch.fnmatch(f, g) or f.startswith(g.rstrip("*/") + "/")
                                                for g in scope))
    return sorted(f for f, _ in fmgraph.pack(p, b.title + " " + b.section("Interpretation"), top=12))


def _weights(p, files):
    import fmgraph
    con = fmgraph.db(p)
    marks = ",".join("?" * len(files))
    w = {}
    for s, d, k, _, x in con.execute(f"SELECT src, dst, kind, t, w FROM edges WHERE src IN ({marks}) AND dst IN "
                                     f"({marks})", (*files, *files)):
        if k in KINDS and s != d:
            key = tuple(sorted((s, d)))
            w[key] = w.get(key, 0) + KINDS[k] * (x or 1)
    return w


def partition(files, weights, k):
    """Agglomerative: merge the two most-linked groups (smallest first on ties) until k remain, no group past an even
    share plus one. ponytail: O(n³) over a task's files, fine to ~60; a real min-cut if tasks get bigger."""
    groups = [[f] for f in files]
    cap = -(-len(files) // max(k, 1)) + 1

    def link(g, h):
        return sum(weights.get(tuple(sorted((a, b))), 0) for a in g for b in h)
    while len(groups) > k:
        cands = [(link(g, h), -(len(g) + len(h)), i, j) for i, g in enumerate(groups) for j, h in enumerate(groups)
                 if i < j and len(g) + len(h) <= cap]
        if not cands:
            cap += 1
            continue
        _, _, i, j = max(cands)
        groups[i] += groups.pop(j)
    return [sorted(g) for g in groups], link


def task_split(p, args):
    import fmcli
    b = fmcli.need_brief(p, args.id)
    if b.status in c.CLOSED:
        raise fmcli.UsageError(f"{b.id} is {b.status}")
    files = _files(p, b, args.files)
    if len(files) < 2:
        raise fmcli.UsageError(f"{b.id} has {len(files)} file(s) to split: give its scope (fm task set {b.id} "
                               f"scope=…) or --files")
    k = args.parts or min(4, max(2, -(-len(files) // 4)))
    weights = _weights(p, files)
    groups, link = partition(files, weights, k)
    seams = [(i, j, link(g, h)) for i, g in enumerate(groups) for j, h in enumerate(groups) if i < j and link(g, h)]
    children = []
    if not args.dry_run:
        with c.lock(p.dir):
            for i, g in enumerate(groups, 1):
                touching = [f"part {j + 1 if a == i - 1 else a + 1}" for a, j, _ in seams if i - 1 in (a, j)]
                raw = (f"Part {i} of {len(groups)} of {b.id} ({b.title}): change only {', '.join(g)}. "
                       + (f"It meets {', '.join(sorted(set(touching)))} at shared names: keep those interfaces as they "
                          f"are, or record the change in this task's Log so the parent sees it in the capsule. "
                          if touching else "")
                       + f"The parent's request: {c.fit(b.section('Raw request').replace('>', '').strip(), 600)}")
                kid = fmcli._create(p, f"{b.title} — part {i}: {c.fit(', '.join(os.path.basename(f) for f in g), 60)}",
                                    b.type, "S" if len(g) <= 3 else "M", "planned", raw=raw, scope=g)
                kid.meta["parent"] = b.id
                kid.add_step(f"change {c.fit(', '.join(g), 120)} and keep the parent's checks green")
                for n, v in b.verify_cmds():
                    if v:
                        kid.add_ac(f"the parent's check {n} still passes", v)
                c.save_brief(p, kid)
                children.append({"id": kid.id, "files": g})
            b = c.find_brief(p, b.id)
            b.append_log(f"split into {', '.join(x['id'] for x in children)} along the code's seams")
            c.save_brief(p, b)
            c.log_event(p, "task_split", task=b.id, data={"children": [x["id"] for x in children]},
                        session=fmcli.session())
            c.regen_views(p)
    else:
        children = [{"id": None, "files": g} for g in groups]
    text = (f"{b.id} split into {len(groups)} part(s) over {len(files)} files"
            + (" (dry run)" if args.dry_run else "") + ":\n"
            + "\n".join(f"  {x['id'] or f'part {i}'}: {', '.join(x['files'])}" for i, x in enumerate(children, 1))
            + ("\nSeams (links crossing parts): " + ", ".join(f"{i + 1}–{j + 1} {w:.1f}" for i, j, w in seams)
               if seams else "\nNo links cross the parts.")
            + ("" if args.dry_run else f"\nRun each in a lane (fm lane brief ID), read each one's fm task capsule; "
                                       f"{b.id} closes after its children."))
    return fmcli.out(args, {"children": children, "seams": [{"a": i + 1, "b": j + 1, "weight": w} for i, j, w in seams]},
                     text)


def open_children(p, b, briefs=None):
    return [k for k in briefs or c.load_briefs(p) if k.meta.get("parent") == b.id and k.status not in c.CLOSED]


def task_capsule(p, args):
    """The child's return to its parent, at most CAPSULE_LINES lines: status, files and lines changed, verification,
    decisions, follow-ups and risks."""
    import fmcli
    b = fmcli.need_brief(p, args.id)
    commits = c._git(p.root, "log", "--format=%h", "--grep", f"Foreman-Task: {b.id}", timeout=30).split()
    stat = (c._git(p.root, "show", "--numstat", "--format=", *commits, timeout=30) if commits else
            (c.task_diff(p.root, base, "--numstat") or "") if (base := c.task_base(p.root, b)) else "")
    changed = {}
    for row in stat.splitlines():
        a, d, f = (row.split("\t") + ["", "", ""])[:3]
        if f:
            x = changed.setdefault(f, [0, 0])
            x[0] += int(a) if a.isdigit() else 0
            x[1] += int(d) if d.isdigit() else 0
    grade, why = b.grade()
    log = b.section("Log").splitlines()
    pick = lambda pat: [re.sub(r"^- \S+ ", "", x) for x in log if re.search(pat, x, re.I)][-2:]
    lines = [f"{b.id} {b.status}: {b.title}" + (f" (part of {b.meta['parent']})" if b.meta.get("parent") else ""),
             "changed: " + (", ".join(f"{f} +{a}/-{d}" for f, (a, d) in sorted(changed.items())[:8]) or "nothing yet")
             + (f" in {', '.join(commits[:3])}" if commits else ""),
             f"verification: {grade} ({why})"]
    lines += [f"decision: {c.fit(x, 140)}" for x in pick(r"decid|interface|seam|steer")]
    lines += [f"lesson: {c.fit(x.lstrip('- '), 140)}" for x in b.section("Lessons").splitlines()[-1:] if x.strip()]
    lines += [f"follow-up: {c.fit(x.lstrip('- '), 140)}" for x in b.section("Follow-ups captured").splitlines()[-3:]
              if x.strip()]
    lines += [f"risk: {c.fit(x, 140)}" for x in pick(r"risk|block|fail|regress")]
    text = c.redact("\n".join(c.fit(x, 200) for x in lines[:CAPSULE_LINES]))
    return fmcli.out(args, {"id": b.id, "status": b.status, "files": changed, "commits": commits, "text": text}, text)
