"""fm lane (T-0134): a lane is a linked git worktree of a project's repo with its own active task, so two sessions can
work two tasks without touching each other's files. `new` makes one for a task (beside the repo, in <repo>.lanes/, on
branch foreman/<id>) and gives the task to it; `list` shows them; `rm` removes one with nothing uncommitted, keeps its
branch unless it is merged, and puts the task back in the queue."""
import os
import subprocess

import fmcore as c


def _git(root, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}  # nothing points it at another repo
    return subprocess.run(["git", "-C", root, *args], capture_output=True, text=True, timeout=120, env=env)


def cmd_lane(args):
    import fmcli
    p = fmcli.resolve(args)
    main = c.main_worktree(p.root) or p.root  # from inside a lane: its main checkout
    if args.action == "list":
        briefs = c.load_briefs(p)
        rows, lines = [], []
        for block in _git(main, "worktree", "list", "--porcelain").stdout.strip().split("\n\n")[1:]:
            fields = dict(line.partition(" ")[::2] for line in block.splitlines())
            path = os.path.realpath(fields.get("worktree", ""))
            tasks = [b for b in briefs if b.meta.get("lane") == path]
            rows.append({"path": path, "branch": fields.get("branch", "").replace("refs/heads/", ""),
                         "tasks": [{"id": b.id, "status": b.status, "title": b.title} for b in tasks]})
            gone = not os.path.isdir(path)  # deleted by hand: git lists it until pruned
            rows[-1]["missing"] = gone
            lines.append(f"{path} [{'missing' if gone else rows[-1]['branch'] or 'detached'}]: "
                         + ("; ".join(f"{b.id} {b.status} {c.fit(b.title, 50)}" for b in tasks) or "no task")
                         + (f" — fm lane rm {tasks[0].id} frees it" if gone and tasks else ""))
        listed = {r["path"] for r in rows}
        for b in briefs:  # review: a task whose lane folder is gone is still held; say how to free it
            if b.meta.get("lane") and b.meta["lane"] not in listed and b.status not in c.CLOSED:
                rows.append({"path": b.meta["lane"], "branch": None, "missing": True,
                             "tasks": [{"id": b.id, "status": b.status, "title": b.title}]})
                lines.append(f"{b.meta['lane']} [missing]: {b.id} {b.status} {c.fit(b.title, 50)} — fm lane rm {b.id} "
                             f"frees it")
        return fmcli.out(args, {"lanes": rows}, "\n".join(lines) or "No lanes: fm lane new <task id> makes one.")
    if not args.id:
        raise fmcli.UsageError(f"fm lane {args.action} needs a task id")
    b = fmcli.need_brief(p, args.id)
    branch = f"foreman/{b.id}"
    if args.action == "new":
        if b.status in c.CLOSED or b.status in ("active", "verifying") or b.meta.get("lane"):
            raise c.PolicyError(f"{b.id} is {b.meta.get('lane') and 'already in lane ' + b.meta['lane'] or b.status}: "
                                f"a lane takes a task nobody is working on")
        path = os.path.join(os.path.dirname(main), os.path.basename(main) + ".lanes", b.id)
        _git(main, "worktree", "prune")  # a lane folder deleted by hand would block re-adding it
        have =_git(main, "rev-parse", "--verify", "-q", f"refs/heads/{branch}").returncode == 0
        r = _git(main, "worktree", "add", "-q", *([path, branch] if have else ["-b", branch, path, "HEAD"]))
        if r.returncode:
            raise fmcli.UsageError(f"git worktree add failed: {r.stderr.strip()[:300]}")
        path = os.path.realpath(path)

        def give(x):
            x.meta["lane"] = path
            for k in ("base", "base_tree", "paused_tree"):  # its start point is taken in the lane, at focus
                x.meta.pop(k, None)
            x.append_log(f"lane: {path} on {branch}")
        fmcli.mutate(p, b.id, give, "lane_new", {"path": path, "branch": branch})
        return fmcli.out(args, {"id": b.id, "path": path, "branch": branch},
                         f"{b.id}: lane {path} on {branch}. Work there: cd into it and start claude; fm focus {b.id}.")
    if not b.meta.get("lane"):
        raise fmcli.UsageError(f"{b.id} isn't in a lane")
    path, kept = remove(p, b, main)
    return fmcli.out(args, {"id": b.id, "path": path, "branch_kept": kept},
                     f"{b.id}: lane {path} removed" + (f"; branch foreman/{b.id} kept (not merged)" if kept else "") + ".")


def remove(p, b, main):
    """fm lane rm (and fm tidy --apply, T-0186): the lane's folder, its registration and its branch if merged; never
    uncommitted or ignored files (PolicyError). (path, whether the branch was kept)."""
    import fmcli
    path, branch = b.meta["lane"], f"foreman/{b.id}"
    if os.path.isdir(path):
        st = _git(path, "status", "--porcelain", "--ignored")  # ignored files (.env, builds) go with the folder too
        if st.returncode or st.stdout.strip():
            ignored = [ln[3:] for ln in st.stdout.splitlines() if ln.startswith("!! ")]
            raise c.PolicyError(f"lane {path} has " + (f"ignored files ({', '.join(ignored[:5])}) that removing it would "
                                                       f"delete: move or delete them" if ignored and len(ignored) ==
                                                       len(st.stdout.splitlines()) else
                                                       "uncommitted work: commit it (fm task finish --commit) or remove it")
                                + " there first; fm lane rm never discards anything")
        r = _git(main, "worktree", "remove", path)
        if r.returncode:
            raise fmcli.UsageError(f"git worktree remove failed: {r.stderr.strip()[:300]}")
    _git(main, "worktree", "prune")  # a folder deleted by hand leaves a registration that holds the branch (review)
    kept = _git(main, "branch", "-d", branch).returncode != 0  # -d refuses an unmerged branch: its commits stay

    def take_back(x):
        x.meta.pop("lane", None)
        if x.status in ("active", "verifying"):
            x.meta["status"] = "planned"  # not the main checkout's active task by accident
        x.append_log(f"lane removed: {path}" + (f" (branch {branch} kept: not merged)" if kept else ""))
    fmcli.mutate(p, b.id, take_back, "lane_rm", {"path": path, "branch_kept": kept})
    return path, kept


def stale(p, briefs, apply, actions, finding):
    """fm tidy (T-0186): lanes whose task closed, and merged foreman/T-* branches no worktree holds."""
    import fmcli
    main = c.main_worktree(p.root) or p.root
    if not c.git_root(main):
        return []
    out = []
    for b in briefs:
        if b.meta.get("lane") and b.status in c.CLOSED:
            out.append(finding(p.slug, "stale_lane", "action", f"{b.id} is {b.status}; its lane {b.meta['lane']} remains",
                               f"fm lane rm {b.id}", auto=True))
            if apply:
                try:
                    remove(p, b, main)
                    actions.append(("lane_rm", b.id))
                except (c.PolicyError, fmcli.UsageError) as e:
                    out[-1].update(severity="warn", auto=False, fix=str(e))
    held = {ln.partition(" ")[2] for ln in _git(main, "worktree", "list", "--porcelain").stdout.splitlines()
            if ln.startswith("branch ")}
    for ref in _git(main, "branch", "--merged", "HEAD", "--format=%(refname)", "--list", "foreman/T-*").stdout.split():
        if ref in held:
            continue
        name = ref.removeprefix("refs/heads/")
        out.append(finding(p.slug, "merged_lane_branch", "action", f"{name} is merged and no lane uses it",
                           f"git branch -d {name}", auto=True))
        if apply and _git(main, "branch", "-d", name).returncode == 0:  # -d: never an unmerged one
            actions.append(("branch_rm", name))
    return out
