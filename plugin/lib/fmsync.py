"""fm sync: an opt-in mirror of a project's Foreman state inside the repo (.foreman/), committed with the code, so
another clone or machine can pick the work up.

Briefs (and their archive), decisions and research travel; the ledger, meta, sessions, pending asks, gates and views
stay local. Authorization never travels: `allow` and `approved` are stripped on export and ignored on import, so a
pulled branch can't grant anything. The mirror is written only by fm (the guard treats hand edits as state-direct)
and is left out of the worktree id, so exports don't stale audits.
"""
import os
import re
import shutil

import fmcore as c

DIR = ".foreman"
LOCAL_ONLY = ("allow", "approved")
BRIEFS = ("tasks/", "archive/")
README = """# .foreman

Foreman's task briefs, decisions and research for this repository, mirrored by `fm sync` so another clone or machine
can pick the work up (`fm sync import`, or automatically at session start). fm writes this folder; change the work
through fm, not by editing these files. Approvals never travel: they stay on the machine where they were granted.
"""
_ID = re.compile(r"^(T-\d{4,})")


def mirror(p):
    return os.path.join(p.root, DIR)


def _read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def _write_if_changed(path, text):
    try:
        if _read(path) == text:
            return False
    except OSError:
        pass
    os.makedirs(os.path.dirname(path), exist_ok=True)
    c.write_atomic(path, text)
    return True


def _without_grants(text):
    b = c.Brief.parse(text)
    for k in LOCAL_ONLY:
        b.meta.pop(k, None)
    return b


def _walk(base):
    for d, _, files in os.walk(base):
        for f in sorted(files):
            if f.endswith(".md"):
                yield os.path.relpath(os.path.join(d, f), base).replace(os.sep, "/")


def export(p):
    """Bring the mirror up to date with local state. Returns the number of files written."""
    root, written, here = mirror(p), 0, {}
    written += _write_if_changed(os.path.join(root, "README.md"), README)
    for rel in _walk(p.dir):
        if rel.startswith(BRIEFS) or rel.startswith("research/") or rel == "decisions.md":
            text = _read(os.path.join(p.dir, rel))
            if rel.startswith(BRIEFS):
                text = _without_grants(text).render()
                here[_ID.match(os.path.basename(rel)).group(1)] = rel
            written += _write_if_changed(os.path.join(root, rel), text)
    for rel in list(_walk(root)):  # a brief archived here moved: drop its old place (briefs only known elsewhere stay)
        m = _ID.match(os.path.basename(rel))
        if rel.startswith(BRIEFS) and m and here.get(m.group(1), rel) != rel:
            os.remove(os.path.join(root, rel))
    return written


def import_(p):
    """Take in what the mirror has that is new or newer here. Local grants stay; the mirror's are ignored.
    Returns {"added", "updated", "conflicts"}. The caller holds the project lock and regenerates views."""
    root, res = mirror(p), {"added": 0, "updated": 0, "conflicts": []}
    if not os.path.isdir(root):
        return res
    mine = {b.id: b for b in c.load_briefs(p, include_archive=True)}
    for rel in _walk(root):
        src, dest = os.path.join(root, rel), os.path.join(p.dir, rel)
        if rel.startswith(BRIEFS):
            try:
                theirs = _without_grants(_read(src))
            except (OSError, ValueError):
                res["conflicts"].append(f"{rel}: unreadable")
                continue
            local = mine.get(theirs.id)
            if local is None:
                _write_if_changed(dest, theirs.render())
                res["added"] += 1
            elif (theirs.meta.get("updated") or "") > (local.meta.get("updated") or ""):
                if theirs.meta.get("created") != local.meta.get("created"):  # the same id for different work
                    res["conflicts"].append(f"{theirs.id}: a different task here has this id; kept the local one")
                    continue
                for k in LOCAL_ONLY:
                    if k in local.meta:
                        theirs.meta[k] = local.meta[k]
                if os.path.abspath(local.path) != os.path.abspath(dest):
                    os.remove(local.path)  # archived (or restored) on the other side
                _write_if_changed(dest, theirs.render())
                res["updated"] += 1
        elif rel == "decisions.md":  # append-only: take the lines this copy lacks
            have = _read(dest) if os.path.exists(dest) else ""
            extra = [l for l in _read(src).splitlines() if l.strip() and l not in have.splitlines()]
            if extra:
                _write_if_changed(dest, have.rstrip("\n") + ("\n" if have else "") + "\n".join(extra) + "\n")
                res["updated"] += 1
        elif rel.startswith("research/") and not os.path.exists(dest):
            _write_if_changed(dest, _read(src))
            res["added"] += 1
    return res


def mirrored_ids(p):
    root = mirror(p)
    return {m.group(1) for rel in _walk(root) if rel.startswith(BRIEFS)
            for m in [_ID.match(os.path.basename(rel))] if m} if os.path.isdir(root) else set()


def status(p):
    root, meta = mirror(p), c.read_meta(p)
    local = {b.id: b for b in c.load_briefs(p, include_archive=True)}
    theirs = {}
    for rel in (_walk(root) if os.path.isdir(root) else []):
        if rel.startswith(BRIEFS):
            try:
                b = c.Brief.parse(_read(os.path.join(root, rel)))
                theirs[b.id] = b
            except (OSError, ValueError):
                continue
    newer = lambda a, b: (a.meta.get("updated") or "") > (b.meta.get("updated") or "")
    return {"on": bool(meta.get("sync")), "dir": root, "briefs": len(theirs), "local": len(local),
            "repo_only": sorted(set(theirs) - set(local)), "local_only": sorted(set(local) - set(theirs)),
            "newer_in_repo": sorted(i for i in set(theirs) & set(local) if newer(theirs[i], local[i])),
            "newer_here": sorted(i for i in set(theirs) & set(local) if newer(local[i], theirs[i]))}


def cmd_sync(args):
    import fmcli
    p = fmcli.resolve(args)
    if args.action == "on":
        c.update_meta(p, sync=True)
        with c.lock(p.dir):
            n = export(p)
            c.log_event(p, "sync", data={"on": True, "written": n}, session=fmcli.session())
        note = (" This repo is marked sensitive: review .foreman/ before pushing (evidence is redacted, but briefs "
                "describe the work)." if c.read_meta(p).get("sensitive") else "")
        return print(f"Mirroring Foreman state to {mirror(p)} ({n} file(s) written); commit it with your work. "
                     f"Approvals stay on this machine.{note}")
    if args.action == "off":
        c.update_meta(p, sync=False)
        if args.remove and os.path.isdir(mirror(p)):
            shutil.rmtree(mirror(p))
        with c.lock(p.dir):
            c.log_event(p, "sync", data={"on": False, "removed": bool(args.remove)}, session=fmcli.session())
        return print(f"Sync off; {mirror(p)} " + ("removed." if args.remove else "left as it is (fm sync off --remove "
                                                                                    "deletes it)."))
    if args.action in ("import", "export"):
        with c.lock(p.dir):
            if args.action == "export":
                res = {"written": export(p)}
                text = f"{res['written']} file(s) written to {mirror(p)}."
            else:
                res = import_(p)
                text = (f"{res['added']} added, {res['updated']} updated from {mirror(p)}."
                        + "".join(f"\n  conflict: {x}" for x in res["conflicts"]))
            c.log_event(p, "sync_" + args.action, data=dict(res), session=fmcli.session())
            c.regen_views(p)
        return fmcli.out(args, res, text)
    st = status(p)
    fmcli.out(args, st, f"Sync {'on' if st['on'] else 'off'} · {st['dir']} · {st['briefs']} brief(s) mirrored, "
                        f"{st['local']} here" + "".join(f"\n  {k.replace('_', ' ')}: {', '.join(st[k])}" for k in
                                                         ("repo_only", "local_only", "newer_in_repo", "newer_here")
                                                         if st[k]))
