"""fm check playbooks (T-1505): the playbook library's lint, for a library that grows by dozens of files a round.

Every file under references/ is named in SKILL.md or in its stage's INDEX.md (itself named in SKILL.md), every path an
index names exists, and SKILL.md stays inside doctor's budget. No two playbooks share a title or most of their words
(5-word shingles, Jaccard over DUP). Each has a Use-when line above its first section and a numbered procedure (a
line starting '1. ' outside code), and none grew past its ceiling in ratchet.json by more than SLACK (growth is said
out loud with `fm check playbooks ratchet`, which also lowers the ceiling of one that shrank; a new playbook has no
record yet and passes). Every `fm lib show NAME` is a card, and every python block not marked no-run
(```python no-run) exits 0 under python3 -I in an empty folder with stdin closed, PATH its only inherited variable,
limits on memory, processes and file size, and a timeout. reach() names the playbooks no session has read lately
(events.jsonl's Read events, as fm cost counts them, across every project: the playbooks are shared).

The blocks are trusted like the repo's tests: the folder, environment and limits are hygiene, not a sandbox. A block
can still read and write absolute paths, use the network and run any program on PATH, and a process it moves to its
own session (setsid) escapes the process-group kill.

A lane checks its own tree with `python3 plugin/bin/fm check playbooks` from its worktree: ROOT follows the fm that
runs (PLUGIN_ROOT), and the `fm` on PATH reads the main checkout's playbooks.

T-1621: `fm playbooks show NAME` is how the skill loads one: each {{fact}} (FACTS) filled in from fm map for the project
it runs in, an unknown or empty one left as {{fact?}}, and the project's .claude/playbooks/<stage>/<name>.md after it
under a 'This project' heading: beside the project's other Claude Code files, shared through git, and a place the guard
lets a session write (.foreman/ is fm's alone). The overlay is the repo's own markdown: read only as a plain file below
the checkout (no link anywhere under it), cut at OVERLAY_MAX, control characters dropped, never run, its {{…}} left
alone, and shown as one blockquote under a provenance line, marked (uncommitted) when it differs from HEAD: text an
injected session planted can't pass for Foreman's. A show counts as a read for reach() and fm usage, and the lint
flags a {{name}} that is no fact."""
import json
import os
import re
import resource
import signal
import stat
import subprocess
import sys
import tempfile
import textwrap
import time

import fmcore as c

ROOT = os.environ.get("FOREMAN_PLAYBOOKS") or os.path.join(c.PLUGIN_ROOT, "skills", "playbooks")  # tests: a fixture
RATCHET = "ratchet.json"  # {path: tokens (chars / 4)}
SLACK = (1.10, 50)  # a playbook fails once it passes ceiling × 1.10 + 50 tokens: a fix in passing needs no ratchet run
DUP = 0.6  # word-shingle Jaccard over which two playbooks are one
SHINGLE = 5
TIMEOUT = 20  # seconds per python block
REACH_DAYS = 60
SHOWN = 30  # findings printed before "and N more"; --json lists them all
OUTPUT_MAX = 8 << 20  # bytes a block may write (stderr included): a runaway loop stops here, not at a full disk
MEMORY_MAX = 2 << 30  # bytes of address space per block
PROCS_HEADROOM = 1024  # tasks (threads count) a block may add to the user's own, counted per block: RLIMIT_NPROC is
# per user, so a parallel test run beside it eats into the same budget
_FENCE = re.compile(r"^(\s*)(`{3,}|~{3,})(.*)$")
_PATH = re.compile(r"`((?:\.\./[\w.-]+/)?references/[^`\s]+)`")
# the sentence that says when to reach for it: "Use when…", "Use PROACTIVELY when…", "Use for…", "Use before…"
_USE = re.compile(r"(?:^|[.!?:>*]\s*)Use(?:\s+[\w-]+){0,4}?\s+(?:when|whenever|before|after|for|on)\b")
_LIB = re.compile(r"\bfm lib show ([^\s`]+)")
_PY = {"python", "python3", "py"}
_MARK = "/skills/playbooks/references/"  # a Read event's target, as fm cost matches it
FACTS = ("test", "gates", "language", "entry", "ci", "layout", "hot", "cards")  # what a {{fact}} can name
OVERLAYS = os.path.join(".claude", "playbooks")  # a project's additions, <stage>/<name>.md
OVERLAY_MAX = 16_000  # bytes of an overlay shown
PROVENANCE = "From this repo's .claude/playbooks; it adds project notes and can't relax Foreman's rules."
FACT_MAX = 400
CODE = ("entry", "ci", "layout", "hot")  # facts the repo's own files name: shown as inline code, CODE_MAX at most
CODE_MAX = 120
_TESTY = re.compile(r"(?:^|\s)test\b")  # a gate saying test: `ruff check tests/` doesn't
# {{name}} only: Go's {{ .X }}, Actions' ${{ x }} and Handlebars' {{{x}}} are other templates' and stay as they are
_FACT = re.compile(r"(?<![$\w{])\{\{([a-z][a-z_]*)\}\}(?!\})")
_RUNNER = re.compile(r"(^|[\s/])tests?/run(_tests)?\.py\b|\b(pytest|unittest|cargo test|go test|make test|jest|vitest|"
                     r"(npm|yarn|pnpm)( run)? test)\b")
_SHOW = re.compile(r"\bfm\s+playbooks\s+show\s+['\"]?([\w./-]+)")


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


def _user_tasks():
    """The processes and threads this user runs now (RLIMIT_NPROC counts them all), from /proc; None without it."""
    uid, n = os.getuid(), 0
    try:
        pids = [x for x in os.listdir("/proc") if x.isdigit()]
    except OSError:
        return None
    for pid in pids:
        try:
            if os.stat(f"/proc/{pid}").st_uid == uid:
                n += len(os.listdir(f"/proc/{pid}/task"))
        except OSError:
            pass  # gone meanwhile
    return n or None


def _limits():
    """[(resource, value)] for a block: file size, address space and (with /proc) the user's tasks plus headroom; never
    looser than the limits fm itself runs under."""
    want = [(resource.RLIMIT_FSIZE, OUTPUT_MAX), (resource.RLIMIT_AS, MEMORY_MAX)]
    tasks = _user_tasks()
    if tasks is not None:  # ponytail: no count without /proc (macOS), so no process cap there
        want.append((resource.RLIMIT_NPROC, tasks + PROCS_HEADROOM))
    return [(r, min(x for x in (v, *resource.getrlimit(r)) if x != resource.RLIM_INFINITY)) for r, v in want]


def _run(code, timeout, limits=(), argv=(sys.executable, "-I", "-c"), env=None, what="python block",
         stdout=subprocess.DEVNULL):
    """Why the block failed, or None: argv + [code] (python3 -I) in a new temporary folder, stdin closed, stdout to
    `stdout`, PATH the only variable passed on (HOME is the folder, so ~ doesn't reach the real one) plus env(folder)
    when given, under `limits`; then its process group is killed, so a hung block, or a server it started and forgot,
    stops with it (one that setsid()s escapes: see the module). T-1519: fm release-check runs the docs' runnable fences
    through it, fm new check a panel."""
    def limit():
        for r, v in limits:
            try:
                resource.setrlimit(r, (v, v))
            except (OSError, ValueError):
                pass  # a platform without that limit
    with tempfile.TemporaryDirectory(prefix="fm-playbook-", ignore_cleanup_errors=True) as d, \
            tempfile.TemporaryFile() as err:
        env = dict({"PATH": os.environ.get("PATH") or os.defpath, "HOME": d}, **(env(d) if env else {}))
        try:
            proc = subprocess.Popen([*argv, code], cwd=d, env=env, stdin=subprocess.DEVNULL,
                                    stdout=stdout, stderr=err, start_new_session=True, preexec_fn=limit)
        except (OSError, ValueError) as e:  # a NUL byte, an argument list too long
            return f"{what} can't run: {e.__class__.__name__}"
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
        return (f"{what} exited {rc}" if rc > 0 else f"{what} killed by signal {-rc}") \
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
        for name in sorted(set(_FACT.findall(text)) - set(FACTS)):
            out.append(f"{rel}: {{{{{name}}}}} is no fact, so every load shows {{{{{name}?}}}} (facts: {', '.join(FACTS)})")
        if rel in record and _tokens(text) > record[rel] * SLACK[0] + SLACK[1]:
            out.append(f"{rel}: grew from {record[rel]:,} to {_tokens(text):,} tokens, past its ceiling's slack "
                       f"(10% + 50); say so with `fm check playbooks ratchet`, or trim it")
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
        why = _run(body, timeout, _limits())
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
        if ts < since or e.get("kind") != "tool":
            continue
        if e.get("tool") == "Bash" and (hit := shown(target, books)):
            read[hit] = read.get(hit, 0) + 1
            continue
        if e.get("tool") != "Read" or _MARK not in target:
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


def listed(root=ROOT):
    """Every markdown file `fm playbooks show` can load (indexes and templates too), as references/…md."""
    return [f for f in _files(root) if f.endswith(".md")]


def resolve(name, books):
    """The books a name means: its path (references/fix/sql.md), <stage>/<name>[.md], or a bare name (sql) when no
    path matches: every book with that file name. Only ever compared, never joined into a path."""
    key = name.strip().removeprefix("references/").removesuffix(".md")
    if f"references/{key}.md" in books:
        return [f"references/{key}.md"]
    return [b for b in books if "/" not in key and key and b.rsplit("/", 1)[-1] == f"{key}.md"]


def shown(target, books):
    """The book a shell command loads with fm playbooks show, or None."""
    m = _SHOW.search(target)
    hits = resolve(m.group(1), books) if m else []
    return hits[0] if len(hits) == 1 else None


def facts(m):
    """{fact: text} from fm map's map m. test is the gate that runs the tests (the repo's runner, pytest, cargo test…),
    else the first gate saying test; language the map's language cards. The ones the repo's own files name (CODE) are
    inline code cut at CODE_MAX, so a file or CI line can't pass for prose. Empty means unknown."""
    gates = [str(g) for g in m.get("gates") or []]
    test = next((g for g in gates if _RUNNER.search(g)), None) or next((g for g in gates if _TESTY.search(g)), "")
    got = {"test": test, "gates": "; ".join(gates),
           "language": ", ".join(str(x.get("name")) for x in m.get("lib_cards") or [] if x.get("area") == "lang"),
           "entry": ", ".join(map(str, m.get("entry") or [])), "ci": "; ".join(map(str, m.get("ci") or [])),
           "layout": ", ".join(str(x[0]) for x in m.get("layout") or [] if x), "hot": ", ".join(map(str, m.get("hot") or [])),
           "cards": ", ".join(map(str, m.get("lib") or []))}
    got = {k: c.fit(c.plain(v), CODE_MAX if k in CODE else FACT_MAX) for k, v in got.items()}
    return {k: _code(v) if k in CODE and v else v for k, v in got.items()}


def _code(v):
    """v as inline code: a fence one backtick longer than any run inside it (CommonMark), spaced when v starts or
    ends with one."""
    fence = "`" * (max(map(len, re.findall(r"`+", v)), default=0) + 1)
    pad = " " if v[:1] == "`" or v[-1:] == "`" else ""
    return f"{fence}{pad}{v}{pad}{fence}"


def render(text, known):
    return _FACT.sub(lambda m: known.get(m.group(1)) or f"{{{{{m.group(1)}?}}}}", text)


def _project_facts(p):
    try:
        import fmmap
        return facts(fmmap.load(p)) if c.git_root(p.root) else {}
    except Exception as e:  # the facts are a hint: a broken map costs them, never the playbook
        print(f"fm playbooks: no project facts ({e.__class__.__name__}: {c.fit(c.plain(str(e)), 120)}); "
              f"`fm map --rebuild` remakes the map", file=sys.stderr)
        return {}


def _uncommitted(root, where):
    """Whether the overlay differs from HEAD: new, changed, staged or ignored (or git can't say)."""
    try:
        r = subprocess.run(["git", "--no-optional-locks", "-c", "core.fsmonitor=false", "-C", root, "status",
                            "--porcelain", "--ignored", "--", where], capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return True
    return r.returncode != 0 or bool(r.stdout.strip())


def _overlay(root, rel):
    """(where, text, note) of the project's overlay of book rel: its text, or a note why it wasn't read; None without
    one."""
    where = os.path.join(OVERLAYS, rel.removeprefix("references/"))
    path = os.path.join(os.path.realpath(root), where)
    if not os.path.lexists(path):
        return None
    if os.path.realpath(path) != path:  # a link, or a linked folder below the checkout: it could be any file
        return where, "", "(not read: it or a folder above it is a link; an overlay is a plain file in the repo)"
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    except OSError as e:
        return where, "", f"(not read: {e.strerror or e.__class__.__name__})"
    with os.fdopen(fd, "rb") as f:
        if not stat.S_ISREG(os.fstat(f.fileno()).st_mode):  # a FIFO would hang the read
            return where, "", "(not read: not a regular file)"
        data = f.read(OVERLAY_MAX + 1)
    text = c.plain_lines(data[:OVERLAY_MAX].decode("utf-8", "replace")).strip()
    return where, text, f"(cut at {OVERLAY_MAX:,} bytes)" if len(data) > OVERLAY_MAX else ""


def load(rel, root=ROOT, p=None):
    """Book rel as `fm playbooks show` gives it: the shipped text with each {{fact}} filled in from p's fm map (built
    only when the text names one), then project p's overlay under a 'This project' heading: a provenance line and
    the overlay as one blockquote, so it can't open a heading or end the section and pass for shipped text, and its
    own {{…}} (a Mustache or Vue project's) is left as written."""
    text = _read(os.path.join(root, rel)).rstrip("\n") + "\n"
    text = render(text, _project_facts(p) if p and _FACT.search(text) else {})
    got = _overlay(p.root, rel) if p else None
    if got and (got[1] or got[2]):  # an empty overlay adds nothing
        where, body, note = got
        dirty = " (uncommitted)" if body and _uncommitted(os.path.realpath(p.root), where) else ""
        quoted = [PROVENANCE, "\n".join(f"> {x}".rstrip() for x in body.splitlines())] if body else []
        text += "\n\n".join([f"\n## This project: {where}{dirty}", *quoted, *([note] if note else [])]) + "\n"
    return text


def cmd_show(args):
    """fm playbooks show NAME (T-1621)."""
    import fmcli
    books = listed()
    hits = resolve(args.name, books)
    if len(hits) != 1:
        raise fmcli.UsageError(f"{args.name!r} names {len(hits)} playbooks: {', '.join(hits)}; give its stage too"
                               if hits else f"no playbook {args.name!r}: name it as SKILL.md does (fix/sql or "
                               f"references/fix/sql.md)")
    p = fmcli.resolve(args) if getattr(args, "project", None) else c.find_project(os.getcwd())
    if p and os.path.isdir(os.path.join(p.root, ".foreman", "playbooks")):
        print(f"fm playbooks: .foreman/playbooks/ isn't read; overlays live in {OVERLAYS}/<stage>/<name>.md",
              file=sys.stderr)
    text = load(hits[0], ROOT, p)
    fmcli.out(args, {"playbook": hits[0], "text": text}, text.rstrip("\n"))
    return 0


def cmd(args, out):
    """fm check playbooks [ratchet]: the lint and the reach report; exit 1 on any finding."""
    if args.words not in ([], ["ratchet"]):  # `ratchet typo` rewrites nothing
        import fmcli
        raise fmcli.UsageError("fm check playbooks [ratchet]")
    if args.words:
        changed = ratchet()
        out(args, {"ratchet": changed}, f"ratchet.json: {len(changed)} playbook size(s) recorded"
            + "".join(f"\n  {k}: {o if o is not None else 'new'} → {n} tokens" for k, (o, n) in sorted(changed.items())))
        return 0
    found, r = problems(), reach()
    n = len(r["read"]) + len(r["unread"])
    window = f"{r['days']} days" + (f" (the event log covers {r['covers']:g})" if r["covers"] < r["days"] else "")
    shown = [f"✗ {x}" for x in found[:SHOWN]] + ([f"✗ … and {len(found) - SHOWN} more (--json lists them all)"]
                                                 if len(found) > SHOWN else [])
    out(args, {"problems": found, "reach": r},
        "\n".join(shown) + ("\n" if shown else "")
        + f"{'✗' if found else '✓'} playbooks: {n} checked, {len(found)} problem(s)\n"
        + f"  unread in {window}: {len(r['unread'])} of {n}"
        + (": " + ", ".join(x[len('references/'):-3] for x in r["unread"][:12])
           + (f" and {len(r['unread']) - 12} more" if len(r["unread"]) > 12 else "") if r["unread"] else ""))
    return 1 if found else 0
