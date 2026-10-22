"""fm check playbooks (T-1505): the playbook library's lint, for a library that grows by dozens of files a round.

Every file under references/ is named in SKILL.md or in its stage's INDEX.md (itself named in SKILL.md), every path an
index names exists, and SKILL.md stays inside doctor's budget. No two playbooks share a title or most of their words
(5-word shingles, Jaccard over DUP). Each has a Use-when line above its first section and a numbered procedure (a
line starting '1. ' outside code), and none grew past its size in ratchet.json (growth is said out loud with
`fm check playbooks ratchet`; a new playbook has no record yet and passes). Every `fm lib show NAME` is a card, and
every python block not marked no-run (```python no-run) exits 0 under python3 -I in an empty folder with stdin closed,
PATH its only inherited variable, and a timeout. reach() names the playbooks no session has read lately (events.jsonl's Read
events, as fm cost counts them, across every project: the playbooks are shared)."""
import json
import os
import re
import signal
import subprocess
import sys
import tempfile
import textwrap
import time

import fmcore as c

ROOT = os.path.join(c.PLUGIN_ROOT, "skills", "playbooks")
RATCHET = "ratchet.json"  # {path: tokens (chars / 4)}
DUP = 0.6  # word-shingle Jaccard over which two playbooks are one
SHINGLE = 5
TIMEOUT = 20  # seconds per python block
REACH_DAYS = 60
OUTPUT_MAX = 8 << 20  # bytes a block may write (stderr included): a runaway loop stops here, not at a full disk
_FENCE = re.compile(r"^(\s*)(`{3,}|~{3,})(.*)$")
_PATH = re.compile(r"`((?:\.\./[\w.-]+/)?references/[^`\s]+)`")
# the sentence that says when to reach for it: "Use when…", "Use PROACTIVELY when…", "Use for…", "Use before…"
_USE = re.compile(r"(?:^|[.!?:>*]\s*)Use(?:\s+[\w-]+){0,4}?\s+(?:when|whenever|before|after|for|on)\b")
_LIB = re.compile(r"\bfm lib show ([^\s`]+)")
_PY = {"python", "python3", "py"}
_MARK = "/skills/playbooks/references/"  # a Read event's target, as fm cost matches it


def _read(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def _files(root):
    """Every file under references/, as a path relative to the skill (references/ui/motion.md)."""
    ref = os.path.join(root, "references")
    return sorted(os.path.relpath(os.path.join(d, n), root) for d, _, fs in os.walk(ref) for n in fs)


def _playbooks(root):
    """The procedures: not the stage indexes, nor a template's own markdown (references/ui/templates/…)."""
    return [f for f in _files(root) if f.endswith(".md") and os.path.basename(f) != "INDEX.md"
            and "/templates/" not in f]


def _blocks(text):
    """([(line, info words, body)] per fenced block, the lines with fenced ones blanked): CommonMark's rule that a
    fence closes on a run of its own character at least as long, and an unclosed one runs to the end."""
    lines = text.splitlines()
    prose, blocks, i = list(lines), [], 0
    while i < len(lines):
        m = _FENCE.match(lines[i])
        if not m or (m.group(2)[0] == "`" and "`" in m.group(3)):
            i += 1
            continue
        close = re.compile(rf"^\s*{re.escape(m.group(2)[0])}{{{len(m.group(2))},}}\s*$")
        j = next((k for k in range(i + 1, len(lines)) if close.match(lines[k])), len(lines))
        blocks.append((i + 1, m.group(3).split(), textwrap.dedent("\n".join(lines[i + 1:j])) + "\n"))
        prose[i:j + 1] = [""] * len(prose[i:j + 1])
        i = j + 1
    return blocks, prose


def _shingles(text):
    w = re.findall(r"\w+", text.lower())
    return {tuple(w[i:i + SHINGLE]) for i in range(len(w) - SHINGLE + 1)}


def _record(root):
    """ratchet.json as {path: tokens}, and a problem when it can't be read."""
    try:
        got = json.loads(_read(os.path.join(root, RATCHET)))
    except FileNotFoundError:
        return {}, None
    except (OSError, ValueError) as e:
        return {}, f"{RATCHET}: unreadable ({e.__class__.__name__}); `fm check playbooks ratchet` rewrites it"
    if not isinstance(got, dict):
        return {}, f"{RATCHET}: not a {{path: tokens}} object; `fm check playbooks ratchet` rewrites it"
    return {k: v for k, v in got.items() if isinstance(v, int)}, None


def _tokens(text):
    return len(text) // 4


def ratchet(root=ROOT):
    """Record every playbook's size as its new ceiling; {path: [old, new]} for the ones that changed."""
    old, _ = _record(root)
    new = {rel: _tokens(_read(os.path.join(root, rel))) for rel in _playbooks(root)}
    c.write_atomic(os.path.join(root, RATCHET), json.dumps(new, indent=1, sort_keys=True) + "\n")
    return {k: [old.get(k), v] for k, v in new.items() if old.get(k) != v}


def _cards():
    import fmlib
    return {n for x in fmlib.cards() for n in (x["name"], f"{x['dir']}/{x['name']}")}  # fm lib show takes both


def _run(code, timeout):
    """Why the block failed, or None: python3 -I in an empty temporary folder, stdin closed, PATH the only variable
    passed on (HOME is the folder, so ~ doesn't reach the real one); then its whole process group is killed, so neither
    a hung block nor a server it started and forgot outlives the check."""
    def limit():
        import resource
        resource.setrlimit(resource.RLIMIT_FSIZE, (OUTPUT_MAX, OUTPUT_MAX))
    with tempfile.TemporaryDirectory(prefix="fm-playbook-", ignore_cleanup_errors=True) as d, \
            tempfile.TemporaryFile() as err:
        env = {"PATH": os.environ.get("PATH") or os.defpath, "HOME": d}
        try:
            proc = subprocess.Popen([sys.executable, "-I", "-c", code], cwd=d, env=env, stdin=subprocess.DEVNULL,
                                    stdout=subprocess.DEVNULL, stderr=err, start_new_session=True, preexec_fn=limit)
        except (OSError, ValueError) as e:  # a NUL byte, an argument list too long
            return f"python block can't run: {e.__class__.__name__}"
        try:
            rc = proc.wait(timeout)
        except subprocess.TimeoutExpired:
            rc = None
        try:  # a timed-out leader isn't reaped yet, and live members hold the group id: it can't have been reused
            os.killpg(proc.pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass
        if rc is None:
            proc.wait()
            return f"timed out after {timeout:g} s"
        if not rc:
            return None
        err.seek(max(0, err.seek(0, 2) - 4096))
        last = next((x for x in reversed(err.read().decode("utf-8", "replace").splitlines()) if x.strip()), "")
        return (f"python block exited {rc}" if rc > 0 else f"python block killed by signal {-rc}") \
            + (f": {c.fit(last.strip(), 160)}" if last.strip() else "")


def problems(root=ROOT, card_names=None, timeout=TIMEOUT, run=True):
    """Every lint finding, as 'path[:line]: what'; [] when the library is clean."""
    import fmdoctor
    out, files = [], _files(root)
    try:
        skill = _read(os.path.join(root, "SKILL.md"))
    except OSError:
        skill = ""
        out.append("SKILL.md: missing, so nothing is indexed")
    if len(skill) > fmdoctor.SKILL_MAX:
        out.append(f"SKILL.md: {len(skill):,} characters, over its {fmdoctor.SKILL_MAX:,}-character budget: move a "
                   f"stage's lines into references/<stage>/INDEX.md")
    indexes = {"SKILL.md": skill}
    for f in files:
        if os.path.basename(f) == "INDEX.md" and f.count("/") == 2 and f in set(_PATH.findall(skill)):
            indexes[f] = _read(os.path.join(root, f))
    named = {}
    for name, text in indexes.items():
        for n, line in enumerate(text.splitlines(), 1):
            for path in _PATH.findall(line):
                named.setdefault(path, set()).add(name)
                if not os.path.exists(os.path.join(root, path)):
                    out.append(f"{name}:{n}: {path} doesn't exist")
    for f in files:
        stage = "/".join(f.split("/")[:2]) + "/INDEX.md"
        if not named.get(f, set()) & {"SKILL.md", stage}:
            out.append(f"{f}: in no index (SKILL.md, or {stage} named in SKILL.md)")
    record, bad = _record(root)
    if bad:
        out.append(bad)
    cards = card_names if card_names is not None else _cards()
    titles, shingles, snippets = {}, {}, []
    for rel in _playbooks(root):
        text = _read(os.path.join(root, rel))
        blocks, prose = _blocks(text)
        title = next((x[2:].strip() for x in prose if x.startswith("# ")), rel).lower()  # untitled: its path, unique
        if title in titles:
            out.append(f"{rel}: same title as {titles[title]} ({title!r})")
        titles.setdefault(title, rel)
        shingles[rel] = _shingles(text)
        head = prose[:next((i for i, x in enumerate(prose) if x.startswith("## ")), len(prose))]
        if not any(_USE.search(x) for x in head):
            out.append(f"{rel}: no Use-when line above its first section ('Use when …')")
        if not any(x.startswith("1. ") for x in prose):
            out.append(f"{rel}: no numbered procedure (a line starting '1. ' outside code)")
        if rel in record and _tokens(text) > record[rel]:
            out.append(f"{rel}: grew from {record[rel]:,} to {_tokens(text):,} tokens; say so with "
                       f"`fm check playbooks ratchet`, or trim it")
        for n, line in enumerate(text.splitlines(), 1):
            for name in _LIB.findall(line):
                name = name.rstrip(".,;:)!?'\"")
                if name and not name.startswith("-") and not re.search(r"[A-Z<>{}\[\]]", name) \
                        and name not in cards:  # NAME, <name>: placeholders; --section: an option
                    out.append(f"{rel}:{n}: fm lib show {name}: no such card")
        snippets += [(rel, n, body) for n, info, body in blocks
                     if info and info[0].lower() in _PY and "no-run" not in info[1:]]
    books = sorted(shingles)
    for i, a in enumerate(books):
        for b in books[i + 1:]:
            union = len(shingles[a] | shingles[b])
            share = len(shingles[a] & shingles[b]) / union if union else 0
            if share > DUP:
                out.append(f"{b}: shares {share:.0%} of its wording with {a}: merge them or cut one")
    for rel, n, body in snippets if run else ():
        why = _run(body, timeout)
        if why:
            out.append(f"{rel}:{n}: {why} (mark it ```python no-run if it isn't a self-check)")
    return out


def reach(root=ROOT, days=REACH_DAYS):
    """{days, covers, read: {path: reads}, unread: [path]}: Read events of each playbook in the window, from every
    project; covers is the days the event log actually spans, when that is fewer."""
    books, read, oldest = _playbooks(root), {}, None
    since = c.iso(time.time() - days * 86400)
    for e in c.tail_jsonl(os.path.join(c.state_dir(), "events.jsonl"), 100000):
        ts = str(e.get("ts") or "")
        oldest = ts if ts and (oldest is None or ts < oldest) else oldest
        target = str(e.get("target") or "")
        if ts < since or e.get("kind") != "tool" or e.get("tool") != "Read" or _MARK not in target:
            continue
        key = "references/" + target.split(_MARK, 1)[1]
        # fmhooks keeps 120 characters of a target: a cut path still names one playbook by its prefix
        hit = [b for b in books if b == key] or ([] if key.endswith(".md") else [b for b in books if b.startswith(key)])
        if len(hit) == 1:
            read[hit[0]] = read.get(hit[0], 0) + 1
    ts = c.parse_ts(oldest) if oldest and oldest > since else None
    covers = 0 if oldest is None else round((time.time() - ts.timestamp()) / 86400, 1) if ts else days
    return {"days": days, "covers": covers,
            "read": read, "unread": [b for b in books if b not in read]}


def cmd(args, out):
    """fm check playbooks [ratchet]: the lint and the reach report; exit 1 on any finding."""
    if args.words[:1] == ["ratchet"]:
        changed = ratchet()
        out(args, {"ratchet": changed}, f"ratchet.json: {len(changed)} playbook size(s) recorded"
            + "".join(f"\n  {k}: {o if o is not None else 'new'} → {n} tokens" for k, (o, n) in sorted(changed.items())))
        return 0
    if args.words:
        import fmcli
        raise fmcli.UsageError("fm check playbooks [ratchet]")
    found, r = problems(), reach()
    n = len(r["read"]) + len(r["unread"])
    window = f"{r['days']} days" + (f" (the event log covers {r['covers']:g})" if r["covers"] < r["days"] else "")
    out(args, {"problems": found, "reach": r},
        "\n".join(f"✗ {x}" for x in found) + ("\n" if found else "")
        + f"{'✗' if found else '✓'} playbooks: {n} checked, {len(found)} problem(s)\n"
        + f"  unread in {window}: {len(r['unread'])} of {n}"
        + (": " + ", ".join(x[len('references/'):-3] for x in r["unread"][:12])
           + (f" and {len(r['unread']) - 12} more" if len(r["unread"]) > 12 else "") if r["unread"] else ""))
    return 1 if found else 0
