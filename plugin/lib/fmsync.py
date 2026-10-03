"""fm sync: an opt-in mirror of a project's Foreman state inside the repo (.foreman/), committed with the code, so
another clone or machine can pick the work up.

Briefs (and their archive), decisions and research travel; the ledger, meta, sessions, pending asks, gates and views
stay local. Nothing from the mirror counts for this machine's gates: grants (`allow`, `approved`) are stripped both
ways, fm's `[ran]`/`[tree]` marks and audits recorded elsewhere are neutralized on import, and focus (active) is per
machine. fm writes the folder (the guard treats hand edits as state-direct); its markdown is left out of the worktree
id, so exports don't stale audits, while anything else put there still shows.

Git is the transport and the conflict detector. meta["sync_base"] keeps a hash of what fm last wrote to or took from
each mirror file: a file that differs from it changed in the repo (a pull or merge). Exports leave such a file alone;
the next fm command (or session start, or `fm sync import`) takes it in before working. If the local copy changed too,
the local one wins and theirs is kept under sync-conflicts/ for a manual merge; files with unresolved merge markers
wait until git's conflict is resolved. Callers hold the project lock.
"""
import hashlib
import os
import re
import shutil

import fmcore as c

DIR = ".foreman"
LOCAL_ONLY = ("allow", "approved", "plugin_pin")
BRIEFS = ("tasks/", "archive/")
README = """# .foreman

Foreman's task briefs, decisions and research for this repository, mirrored by `fm sync` so another clone or machine
can pick the work up (`fm sync import`, or automatically at session start). fm writes this folder; change the work
through fm, not by editing these files. Approvals, run marks, audits and focus never count on another machine.
"""
MAX_IMPORT = 1_000_000  # bytes; a mirrored note bigger than this is left in the repo
_ID = re.compile(r"^(T-\d{4,})")
_CONFLICT = re.compile(r"(?m)^(<{7}|={7}|>{7})( |$)")
_AUDIT_LINE = re.compile(r"(?m)^(-\s+\(audit\s+[a-z]+)\)")


def mirror(p):
    return os.path.join(c.main_view(p).root, DIR)  # T-0134: one mirror, the main checkout's, never a lane's copy


def _sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def _write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    c.write_atomic(path, text)


def _walk(base):
    """Regular markdown files under base, as relative paths; symlinks are never followed (a pulled one could point
    anywhere)."""
    if os.path.islink(base) or not os.path.isdir(base):
        return
    for d, dirs, files in os.walk(base):
        dirs[:] = sorted(x for x in dirs if not os.path.islink(os.path.join(d, x)))
        for f in sorted(files):
            path = os.path.join(d, f)
            if f.endswith(".md") and not os.path.islink(path) and os.path.isfile(path):  # no FIFO or device reads
                yield os.path.relpath(os.path.join(d, f), base).replace(os.sep, "/")


def _travels(rel):
    return rel.startswith(BRIEFS) or rel.startswith("research/") or rel == "decisions.md"


def _for_mirror(text):
    b = c.Brief.parse(text)
    for k in LOCAL_ONLY:
        b.meta.pop(k, None)
    return b.render()


def _from_mirror(text):
    """A mirrored brief as this machine may take it: no grants, no run or worktree marks, audits relabelled so they
    don't count here (this machine's gates need its own runs and audits)."""
    # a pulled brief is untrusted text that fm task show and other listings print: no terminal sequences
    b = c.Brief.parse(c.plain_lines(_AUDIT_LINE.sub(r"\1, imported)", c._unmarked(text))))
    for k in LOCAL_ONLY:
        b.meta.pop(k, None)
    return b


def _save_base(p, base):
    meta = c.read_meta(p)
    if meta.get("sync_base") != base:
        meta["sync_base"] = base
        c.write_meta(p, meta)


def export(p):
    """Bring the mirror up to date with local state, leaving files that changed in the repo for the import.
    Returns the number of files written."""
    root = mirror(p)
    if os.path.islink(root):
        raise OSError(f"{root} is a symlink; fm sync writes only a real folder")
    base, written, here = dict(c.read_meta(p).get("sync_base") or {}), 0, {}
    if not os.path.exists(os.path.join(root, "README.md")):
        _write(os.path.join(root, "README.md"), README)
    for rel in _walk(p.dir):
        if not _travels(rel):
            continue
        text = _read(os.path.join(p.dir, rel))
        if rel.startswith(BRIEFS):
            m = _ID.match(os.path.basename(rel))
            if not m:
                continue  # not a brief (fm names them T-NNNN-…)
            try:
                text = _for_mirror(text)
            except ValueError:
                continue
            here[m.group(1)] = rel
        text = c.redact(text)  # the mirror is committed: no secret from any older note may reach it
        dest = os.path.join(root, rel)
        cur = _read(dest) if os.path.isfile(dest) and not os.path.islink(dest) else None
        if cur is not None and cur != text and _sha(cur) != base.get(rel):
            continue  # changed in the repo (pull, merge): the import takes it first
        if cur != text:
            _write(dest, text)
            written += 1
        base[rel] = _sha(text)
    for rel in list(_walk(root)):  # a brief archived here moved: drop its old copy if it is still ours
        m = _ID.match(os.path.basename(rel))
        if rel.startswith(BRIEFS) and m and here.get(m.group(1), rel) != rel \
                and _sha(_read(os.path.join(root, rel))) == base.get(rel):
            os.remove(os.path.join(root, rel))
            base.pop(rel, None)
    _save_base(p, base)
    return written


def _set_aside(p, rel, text):
    dest = os.path.join(p.dir, "sync-conflicts", rel.replace("/", "__"))
    _write(dest, text)
    return os.path.relpath(dest, p.dir)


def import_(p):
    """Take in what changed in the mirror since fm last wrote or read it. Returns {added, updated, conflicts}."""
    root, res = mirror(p), {"added": 0, "updated": 0, "conflicts": []}
    base = dict(c.read_meta(p).get("sync_base") or {})
    mine = {b.id: b for b in c.load_briefs(p, include_archive=True)}
    active = {b.id for b in mine.values() if b.status in ("active", "verifying")}
    for rel in _walk(root):
        if not _travels(rel):
            continue
        if os.path.getsize(os.path.join(root, rel)) > MAX_IMPORT:
            res["conflicts"].append(f"{rel}: too large to import (over {MAX_IMPORT // 1000} kB); left in the repo")
            continue
        cur = _read(os.path.join(root, rel))
        h = _sha(cur)
        if base.get(rel) == h:
            continue  # nothing new from the repo
        if _CONFLICT.search(cur):
            res["conflicts"].append(f"{rel}: unresolved merge conflict (resolve it in git, then fm sync import)")
            continue
        dest = os.path.join(p.dir, rel)
        if rel.startswith(BRIEFS):
            try:
                theirs = _from_mirror(cur)
            except ValueError:
                res["conflicts"].append(f"{rel}: not a brief")
                continue
            local = mine.get(theirs.id)
            if theirs.status in ("active", "verifying") and theirs.id not in active:
                theirs.meta["status"] = "planned"  # focus is per machine
            if local is None:
                _write(dest, theirs.render())
                res["added"] += 1
            else:
                mine_text = _for_mirror(_read(local.path))
                if base.get(rel) is None and (theirs.meta.get("updated") or "") <= (local.meta.get("updated") or ""):
                    base[rel] = h  # never synced, and this copy is as new: keep it (the next export writes it)
                    continue
                if base.get(rel) is not None and _sha(mine_text) != base[rel]:
                    res["conflicts"].append(f"{theirs.id}: changed here and in the repo; kept this one, theirs is in "
                                            f"{_set_aside(p, rel, cur)}")
                    base[rel] = h
                    continue
                if local.meta.get("created") and theirs.meta.get("created") != local.meta.get("created"):
                    res["conflicts"].append(f"{theirs.id}: the repo has a different task with this id; kept this one, "
                                            f"theirs is in {_set_aside(p, rel, cur)}")
                    base[rel] = h
                    continue
                for k in LOCAL_ONLY:
                    if k in local.meta:
                        theirs.meta[k] = local.meta[k]
                if os.path.abspath(local.path) != os.path.abspath(dest):
                    os.remove(local.path)  # archived (or restored) on the other side
                _write(dest, theirs.render())
                res["updated"] += 1
        elif rel == "decisions.md":  # append-only: take the lines this copy lacks
            have = _read(dest) if os.path.exists(dest) else ""
            extra = [l for l in c.plain_lines(cur).splitlines() if l.strip() and l not in have.splitlines()]
            if extra:
                _write(dest, have.rstrip("\n") + ("\n" if have else "") + "\n".join(extra) + "\n")
                res["updated"] += 1
        elif not os.path.exists(dest):
            _write(dest, c.plain_lines(cur))  # pulled text: no terminal sequences
            res["added"] += 1
        elif _read(dest) != cur:
            res["conflicts"].append(f"{rel}: differs here; kept this one, theirs is in {_set_aside(p, rel, cur)}")
        base[rel] = h
    _save_base(p, base)
    return res


def incoming(p):
    """Has the repo changed any mirrored file since fm last wrote or read it?"""
    base, root = c.read_meta(p).get("sync_base") or {}, mirror(p)
    return any(_travels(rel) and os.path.getsize(os.path.join(root, rel)) <= MAX_IMPORT
               and base.get(rel) != _sha(_read(os.path.join(root, rel))) for rel in _walk(root))


def mirrored_ids(p):
    return {m.group(1) for rel in _walk(mirror(p)) if rel.startswith(BRIEFS)
            for m in [_ID.match(os.path.basename(rel))] if m}


def status(p):
    root, meta = mirror(p), c.read_meta(p)
    base = meta.get("sync_base") or {}
    local = {b.id for b in c.load_briefs(p, include_archive=True)}
    theirs, incoming = set(), []
    for rel in _walk(root):
        if rel.startswith(BRIEFS) and (m := _ID.match(os.path.basename(rel))):
            theirs.add(m.group(1))
            if base.get(rel) != _sha(_read(os.path.join(root, rel))):
                incoming.append(m.group(1))
    return {"on": bool(meta.get("sync")), "dir": root, "briefs": len(theirs), "local": len(local),
            "repo_only": sorted(theirs - local), "local_only": sorted(local - theirs), "incoming": sorted(incoming)}


def cmd_sync(args):
    import fmcli
    p = fmcli.resolve(args)
    if args.action == "on":
        with c.lock(p.dir):
            try:
                res = import_(p)  # a clone that already has a mirror takes it before writing its own
                meta = c.read_meta(p)
                meta["sync"] = True
                c.write_meta(p, meta)
                n = export(p)
            except (OSError, ValueError) as e:
                meta = c.read_meta(p)
                meta["sync"] = False
                c.write_meta(p, meta)
                raise fmcli.UsageError(f"can't write {mirror(p)}: {e}; sync stays off")
            c.log_event(p, "sync", data={"on": True, "written": n, "imported": res["added"] + res["updated"]},
                        session=fmcli.session())
            c.regen_views(p)
        notes = [" .foreman/ is ignored by git here: add `!.foreman/` to .gitignore, or it never reaches another "
                 "clone." if c.mirror_ignored(c.main_view(p).root) else "",
                 " This repo is marked sensitive: review .foreman/ before pushing (evidence is redacted, but briefs "
                 "describe the work)." if c.read_meta(p).get("sensitive") else ""]
        return print(f"Mirroring Foreman state to {mirror(p)} ({n} file(s) written); commit it with your work. "
                     f"Approvals stay on this machine." + "".join(notes)
                     + "".join(f"\n  conflict: {x}" for x in res["conflicts"]))
    if args.action == "off":
        with c.lock(p.dir):  # with the lock, no export can recreate the folder mid-removal
            meta = c.read_meta(p)
            meta["sync"] = False
            c.write_meta(p, meta)
            if args.remove and os.path.isdir(mirror(p)) and not os.path.islink(mirror(p)):
                shutil.rmtree(mirror(p))
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
                                                         ("incoming", "repo_only", "local_only") if st[k]))
