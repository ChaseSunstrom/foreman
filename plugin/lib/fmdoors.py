"""T-2342: Foreman stops only at an irreversible, ambiguous step. Each plan step and verify command is sorted by door
when the task is focused: a command the guard puts in a category (or can't read) is the guard's, with its run-time
stop and grant path untouched; a step naming a path git doesn't track is a local one-way step; the rest are two-way.
A local one-way step gets a verified snapshot and an Undo line, or runs only when the request asked for it and the
brief has one reading, or parks the task for the final report. Never changes fmguard: it only reads its categories."""
import hashlib
import os
import re
import shlex
import subprocess
import tempfile

import fmcore as c

CAP = 20 * 1024 * 1024  # bytes a snapshot may hold (FM_DOOR_CAP overrides); state grows by at most this per step
FILES = 2000  # entries a snapshot may hold: the copy and the hash stay bounded in time too
CONFIDENCE = 90  # the percent a verified snapshot's step is not reversed: the Undo line restores what it names
_TICK = re.compile(r"`([^`\n]+)`")
_UNDO = re.compile(r"\bUndo:")
# ponytail: a verb gates which untracked paths a step "names" (reading /etc/hosts isn't a door); a step that changes a
# file with another word is read as two-way here and still met by the guard when its command runs
_DESTROY = re.compile(r"(?i)\b(delet\w*|remov\w*|rm|eras\w*|wip\w*|purg\w*|drop\w*|truncat\w*|overwr\w*|rewrit\w*|replac\w*|"
                      r"renam\w*|mv|mov(?:e|es|ed|ing)|clean\w*|reset|prun\w*|migrat\w*|convert\w*|regenerat\w*|clobber\w*|"
                      r"discard\w*)\b")


def _cap():
    try:
        return int(os.environ.get("FM_DOOR_CAP", CAP))
    except ValueError:
        return CAP


def _ctx(p, b):
    import fmguard
    home = os.path.expanduser("~")
    return fmguard.Ctx(cwd=p.root, project_root=fmguard.project_root_for(p.root, home), home=home,
                       foreman_home=c.foreman_home(), state_dir=c.state_dir(), state_fallbacks=c.state_fallbacks(),
                       scratch=[x for x in ("/tmp", "/var/tmp", os.environ.get("TMPDIR")) if x],
                       task_id=b.id if b else None)


def _cats(cmds, ctx):
    """The guard's own category for each command, whichever it puts one on; a command it can't read counts too
    (fail closed: a stop the guard would make at run time is never Foreman's to decide)."""
    import fmguard
    out = []
    for cmd in cmds:
        try:
            out += [cat for cat, _ in fmguard.check_bash(cmd, ctx)]
        except Exception:  # noqa: BLE001 — any failure to classify is the guard's call
            out.append("unclassified")
    return sorted(set(out))


def _tokens(text):
    """Path-like words of a step: one with a '/' or a '.', no flag or URL."""
    for w in re.split(r"[\s`]+", text):
        w = w.strip("\"'()[]{},;:").rstrip(".")
        if w and "://" not in w and not w.startswith("-") and ("/" in w or "." in w) and w not in (".", ".."):
            yield w


def _full(root, tok):
    return os.path.join(root, os.path.expanduser(tok) if tok.startswith("~/") else tok)


def _inside(path, root):
    return os.path.commonpath([path, root]) == root


def _local(tok, root):
    """True when the word names something that exists and git doesn't track (or the repo doesn't hold it at all)."""
    full = _full(root, tok)
    if not os.path.lexists(full):
        return False
    rroot = os.path.realpath(root)
    real = os.path.join(os.path.realpath(os.path.dirname(full)), os.path.basename(full))  # the leaf is never followed
    if os.path.commonpath([real, rroot]) == real:  # the repo itself or a folder above it
        return False
    if not _inside(real, rroot):
        return True
    try:
        r = subprocess.run(["git", "-C", root, "ls-files", "--others", "--exclude-standard", "-z", "--", full],
                           capture_output=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return True  # can't ask git: untracked until it says otherwise
    return r.returncode != 0 or bool(r.stdout)


def _one(where, text, shell, ctx_of, root):
    head = text.split("Undo:", 1)[0]
    cmds = [text] if shell else _TICK.findall(head)
    cats = _cats(cmds, ctx_of()) if cmds else []
    paths = [] if cats or shell or not _DESTROY.search(head) else [t for t in _tokens(head) if _local(t, root)][:8]
    return {"where": where, "door": "guard" if cats else "local" if paths else "two-way", "cats": cats, "paths": paths}


def classify(p, b):
    """[{where: 'step N' | 'verify N', door: guard | local | two-way, cats, paths}] for every step and verify command."""
    box = []

    def ctx_of():
        if not box:
            box.append(_ctx(p, b))
        return box[0]
    rows = [_one(f"step {s.n}", s.text, False, ctx_of, p.root) for s in b.steps()]
    for a in b.acceptance():
        cmd = c.verify_of(a.text)
        if cmd:
            rows.append(_one(f"verify {a.n}", cmd, True, ctx_of, p.root))
    return rows


def reply_door(text, p):
    """'one-way' when a reply's question is about a command the guard stops (a backticked one it categorizes, or a word
    of its categories: fmcli's list), else 'two-way'."""
    text = text or ""
    if _cats(_TICK.findall(text), _ctx(p, None)) if _TICK.search(text) else False:
        return "one-way"
    import fmcli
    return "one-way" if fmcli._guard_named(text) else "two-way"


# ---------------------------------------------------------------- snapshot

def _digest(path):
    h = hashlib.sha256()
    if os.path.isdir(path) and not os.path.islink(path):
        walk = []
        for dp, dn, fn in os.walk(path):
            dn.sort()
            walk.append((dp, [*fn, *(d for d in dn if os.path.islink(os.path.join(dp, d)))]))
    else:
        walk = [(os.path.dirname(path), [os.path.basename(path)])]
    for dp, names in walk:
        for name in sorted(names):
            q = os.path.join(dp, name)
            h.update(os.path.relpath(q, path).encode("utf-8", "surrogateescape") + b"\0")
            if os.path.islink(q):
                h.update(os.readlink(q).encode("utf-8", "surrogateescape"))
                continue
            with open(q, "rb") as f:
                for chunk in iter(lambda: f.read(1 << 20), b""):
                    h.update(chunk)
    return h.hexdigest()


def _same(root, snap, rels):
    """The restore command run into a temp folder gives back what the repo holds now, byte for byte (by hash)."""
    with tempfile.TemporaryDirectory() as tmp:
        r = subprocess.run(["cp", "-a", "--", snap + "/.", tmp + "/"], capture_output=True, timeout=120)
        return r.returncode == 0 and all(os.path.lexists(os.path.join(tmp, rel)) and os.path.lexists(os.path.join(root, rel))
                                         and _digest(os.path.join(tmp, rel)) == _digest(os.path.join(root, rel))
                                         for rel in rels)


def _size(path, cap):
    if not os.path.isdir(path) or os.path.islink(path):
        return os.lstat(path).st_size, 1
    total = n = 0
    for dp, dn, fn in os.walk(path):
        for name in [*fn, *dn]:
            n += 1
            total += os.lstat(os.path.join(dp, name)).st_size
            if total > cap or n > FILES:
                return total, n
    return total + os.lstat(path).st_size, n


def _snapshot(p, tid, n, toks):
    """(Undo command, note) after a copy of the named paths that restores byte for byte, else (None, why not)."""
    import shutil
    rroot, cap, rels = os.path.realpath(p.root), _cap(), []
    try:
        for t in toks:
            full = _full(p.root, t)
            real = os.path.join(os.path.realpath(os.path.dirname(full)), os.path.basename(full))
            if not _inside(real, rroot):
                return None, f"{t} is outside the repo"
            rels.append(os.path.relpath(real, rroot))
        total = count = 0
        for rel in rels:
            s, k = _size(os.path.join(rroot, rel), cap)
            total, count = total + s, count + k
        if total > cap or count > FILES:
            return None, f"over the snapshot cap ({total // 1024} KB+, {count}+ entries; FM_DOOR_CAP bytes)"
        snap = os.path.join(p.dir, "door-snapshots", f"{tid}-step{n}")
        shutil.rmtree(snap, ignore_errors=True)
        for rel in rels:
            os.makedirs(os.path.dirname(os.path.join(snap, rel)), exist_ok=True)
            r = subprocess.run(["cp", "-a", "--", os.path.join(rroot, rel), os.path.join(snap, rel)],
                               capture_output=True, timeout=120)
            if r.returncode:
                raise OSError("cp failed")
        if not _same(rroot, snap, rels):
            shutil.rmtree(snap, ignore_errors=True)
            return None, "the snapshot did not verify (restored hashes differ)"
        return f"cp -a {shlex.quote(snap + '/.')} {shlex.quote(rroot + '/')}", \
            f"{', '.join(toks)}: {total} bytes in {count} entries copied to {snap} and restored into a temp folder with matching hashes"
    except (OSError, subprocess.SubprocessError) as e:
        return None, f"no snapshot ({type(e).__name__})"


# ---------------------------------------------------------------- the gate

def _h(text):
    """What door_seen stores for a step text it has decided (a hash: frontmatter lists split on commas and strip quotes)."""
    return hashlib.sha1(text.encode("utf-8", "surrogateescape")).hexdigest()[:12]


def _named(raw, tok):
    low = raw.lower()
    return tok.lower() in low or os.path.basename(tok.rstrip("/")).lower() in low


def _ambiguous(b):
    """M/L: the Interpretation holds two or more distinct readings (one ruled out with a reason doesn't count)."""
    return b.tier in ("M", "L") and c._distinct(c._split_options(b.section("Interpretation"), bullets=False)) >= 2


def _decide(p, tid, text, why, rejected, kind, confidence=None):
    import fmcli
    fmcli._write_decision(p, text, why, rejected, kind=kind, task=tid, confidence=confidence)
    if confidence is None:
        return
    try:  # a stated confidence is a bet in the calibration ledger, as fm decide --confidence makes it
        import fmoutcomes
        tb = c.find_brief(p, tid)
        fmoutcomes.bet(p, "decision", confidence, task=tid, key=text.lower(),
                       base=fmoutcomes.base_rate(fmoutcomes.outcomes(p), fmoutcomes._first_finish(p), tb.type, tb.tier))
    except Exception:  # noqa: BLE001 — the ledger never loses the decision just written
        pass


def gate(p, tid):
    """Run when fm focus starts a task: each local one-way step gets a verified snapshot and its Undo line (a decision
    with a confidence), runs unsnapshotted only when the request names it and the brief has one reading (a costly
    decision), or parks the task (a marked step with no Undo line; c.waits_on_user reads it). Returns the park reason or None."""
    import fmcli
    b = c.find_brief(p, tid)
    if not b or b.status in c.CLOSED:
        return None
    todo, raw = {s.n: s for s in b.steps() if not s.done}, b.section("Raw request")
    seen, edits, notes, doors, park = [str(x) for x in b.meta.get("door_seen") or []], {}, [], [], None
    for d in classify(p, b):
        n = int(d["where"].split()[1]) if d["door"] == "local" else 0
        s = todo.get(n)
        if not s:
            continue
        if _UNDO.search(s.text):  # its undo is there already: ours from an earlier focus, or the user's own
            doors.append(n)
            continue
        undo, why = ((None, "the step already has evidence, so its text is fixed") if b.has_evidence(step=n)
                     else _snapshot(p, tid, n, d["paths"]))
        if undo:
            edits[n] = (s.text, f"{s.text.rstrip().rstrip('.')}. Undo: {undo}")
            doors.append(n)
            notes.append(("snap", s.text, why, d["paths"]))
        elif all(_named(raw, t) for t in d["paths"]) and not _ambiguous(b):
            if _h(s.text) not in seen:
                notes.append(("ran", s.text, why, d["paths"]))
        else:
            doors.append(n)
            park = park or n
            if _h(s.text) not in seen:
                notes.append(("park", s.text, why, d["paths"]))
        if not undo and _h(s.text) not in seen:
            seen.append(_h(s.text))
    doors = sorted(set(doors))
    if (doors, seen) != (c.door_marked(b), [str(x) for x in b.meta.get("door_seen") or []]) or edits:
        def apply(x):
            for n, (old, new) in edits.items():  # a step edited since it was read keeps its text; door_gaps says so
                cur = next((s for s in x.steps() if s.n == n), None)
                if cur is not None and cur.text == old:
                    x.edit_step(n, new)
            for key, val in (("doors", doors), ("door_seen", seen)):
                if val:
                    x.meta[key] = val
                else:
                    x.meta.pop(key, None)
        fmcli.mutate(p, tid, apply, "door_gate", {"doors": doors, "park": park})
    for kind, text, why, paths in notes:  # after the brief is saved, and outside every lock (each writer takes its own)
        if kind == "snap":
            _decide(p, tid, f"Snapshot before a one-way step: {text}", f"{why}; the step's Undo line restores it",
                    "ran the step with no copy", "reversible", CONFIDENCE)
        elif kind == "ran":
            _decide(p, tid, f"Ran one-way step the request asked for, without a snapshot: {text}",
                    f"{why}; the request names {', '.join(paths)} and the brief has one reading", "parked it for the final report", "costly")
        else:
            _decide(p, tid, f"Parked {tid} at a one-way, ambiguous step: {text}",
                    f"{why}; the request doesn't name {', '.join(paths)} or the brief has two readings: "
                    f"{c.fit(' '.join(b.section('Interpretation').split()) or 'one reading, not named by the request', 300)}",
                    "ran the step without a copy", "costly")
            c.log_event(p, "door_park", task=tid, data={"door": "one-way", "step": text[:120]}, session=fmcli.session())
    return c.door_park(c.find_brief(p, tid)) if park else None
