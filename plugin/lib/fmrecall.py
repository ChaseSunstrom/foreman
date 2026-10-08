"""fm recall: related past work for a request or a task (T-0043): earlier briefs with their outcome and lesson,
decisions and research notes, ranked by BM25 over their words. Stdlib only, computed on demand by fm (never in a
hook). Recalled text is data from past work: plain (no control characters), one capped line per hit."""
import json
import math
import os
import re
import subprocess

import fmcore as c

_WORD = re.compile(r"[a-z][a-z0-9_]{2,}")
_STOP = set("""the and for with that this from into when then than are was were not but all any can its has have had
will would should could also only just more most each other such via per new use using used make made add adds added
fix fixes fixed task tasks brief step steps done test tests run runs work does doing foreman none""".split())
_ROW = re.compile(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*(.+?)\s*\|\s*(.*?)\s*\|")
MAX_READ = 20_000  # chars of a research note that count
LINE, TOTAL, HITS = 170, 800, 4
TIERS = {"S": 0, "M": 1, "L": 2}


def _stem(w):
    for suffix in ("ing", "ed", "es", "s"):
        if w.endswith(suffix) and len(w) - len(suffix) >= 4:
            return w[:-len(suffix)][:5]
    return w[:5]


def _tokens(text):
    # ponytail: lexical recall (suffix-stripped 5-letter stems, BM25); embeddings if synonyms start to matter
    return [_stem(w) for w in _WORD.findall(text.lower()) if w not in _STOP]


PLAYBOOKS = os.path.join(c.PLUGIN_ROOT, "skills", "playbooks", "references")
HALF_LIFE = 180  # days: a hit this old counts half as much as a fresh one


def _age(ts):
    try:
        import datetime
        then = datetime.datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        if then.tzinfo is None:
            then = then.replace(tzinfo=datetime.timezone.utc)
        return max(0.0, (datetime.datetime.now(datetime.timezone.utc) - then).total_seconds() / 86400)
    except (TypeError, ValueError):
        return 0.0


def _files(b):
    return [x.lstrip("- ").strip() for x in b.section("Files touched").splitlines() if x.strip()]


def _documents(p, skip=None):
    """(kind, label, text, tier of a finished brief or None, extra) for everything recall can point to; extra has the
    age in days and, for briefs, the files they touched and their step count."""
    for b in c.load_briefs(p, include_archive=True):
        if b.id == skip or b.status == "captured":
            continue
        lesson = [x.lstrip("- ").strip() for x in b.section("Lessons").splitlines() if x.strip()]
        label = (f"{b.id} [{b.type} {b.tier}, {b.status}, {len(b.steps())} steps] {b.title}"
                 + (f" — lesson: {lesson[0]}" if lesson else ""))
        text = " ".join([b.title, b.section("Raw request"), b.section("Interpretation"), " ".join(lesson),
                         " ".join(b.meta.get("scope") or [])])
        yield "brief", label, text, b.tier if b.status == "done" else None, {
            "age": _age(b.meta.get("updated") or b.meta.get("created")), "files": _files(b), "steps": len(b.steps()),
            "id": b.id}
    try:
        with open(os.path.join(p.dir, "decisions.md"), encoding="utf-8", errors="replace") as f:
            for line in f:
                m = _ROW.match(line)
                if m and m.group(1) != "Date":
                    yield ("decision", f"decision {m.group(1)}: {m.group(2)}", f"{m.group(2)} {m.group(3)}", None,
                           {"age": _age(m.group(1))})
    except OSError:
        pass
    for r in c.tail_jsonl(os.path.join(p.dir, "surprises.jsonl"), 500):  # T-0253: where the model was wrong
        text = c.plain(str(r.get("text") or ""))
        yield "surprise", f"surprise {str(r.get('at') or '')[:10]} ({r.get('task') or '-'}): {c.fit(text, 200)}", text, \
            None, {"age": _age(r.get("at"))}
    folder = os.path.join(p.dir, "research")
    try:
        names = sorted(n for n in os.listdir(folder) if n.endswith(".md"))
    except OSError:
        names = []
    for n in names:
        path = os.path.join(folder, n)
        if os.path.islink(path) or not os.path.isfile(path):
            continue
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                text = f.read(MAX_READ)
        except OSError:
            continue
        first = next((x.strip("-* ").strip() for x in text.splitlines()
                      if x.strip("-* ").strip() and not x.lstrip().startswith(("{", "#"))), "")
        yield "research", f"research {n[:-3]}: {first}", f"{n[:-3].replace('-', ' ')} {text}", None, {
            "age": max(0.0, (__import__("time").time() - os.path.getmtime(path)) / 86400),
            "at": os.path.getmtime(path), "cites": _cites(p.root, text)}
    for group, _, names in sorted(os.walk(PLAYBOOKS)):  # the ported procedures: a request about profiling should
        for n in sorted(x for x in names if x.endswith(".md")):  # surface the profiling playbook (no age)
            rel = os.path.relpath(os.path.join(group, n), PLAYBOOKS)
            try:
                with open(os.path.join(group, n), encoding="utf-8", errors="replace") as f:
                    text = f.read(MAX_READ)
            except OSError:
                continue
            title = next((x[2:].strip() for x in text.splitlines() if x.startswith("# ")), n[:-3])
            yield "playbook", f"playbook {title} (skills/playbooks/references/{rel})", \
                f"{rel[:-3].replace('-', ' ').replace('/', ' ')} {text}", None, {"age": 0.0}


_PATH = re.compile(r"(?<![\w/.-])((?:[\w.-]+/)+[\w.-]+\.\w{1,6})(?::\d+)?")


def _cites(root, text):
    """Repo files a note names (path or path:line), up to 12 that exist."""
    out = []
    for m in _PATH.finditer(text):
        rel = m.group(1)
        if rel not in out and not os.path.isabs(rel) and os.path.isfile(os.path.join(root, rel)):
            out.append(rel)
            if len(out) == 12:
                break
    return out


def _stale(root, at, cites):
    """The cited files that git shows changing after the note was written (T-0210)."""
    if not cites:
        return []
    try:
        r = subprocess.run(["git", "-C", root, "log", f"--since=@{int(at)}", "--name-only", "--format=", "--", *cites],
                           capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired):
        return []
    return sorted({x for x in r.stdout.split() if x in cites})


def recall(p, query, skip=None, n=HITS, cover=0.0):
    """The n most related documents to query: [(score, kind, label, tier, extra)], best first; a hit shares ≥ 2
    words, and at least `cover` of the query's words (T-0206: research asks for 2/3). Older history counts less (half
    at HALF_LIFE days)."""
    q = set(_tokens(query))
    if not q:
        return []
    docs = [(kind, label, _tokens(text), tier, extra) for kind, label, text, tier, extra in
            [*_documents(p, skip), *_shared_docs(p)]]
    if not docs:
        return []
    avg = sum(len(d[2]) for d in docs) / len(docs) or 1
    df = {}
    for d in docs:
        for w in set(d[2]) & q:
            df[w] = df.get(w, 0) + 1
    scored = []
    for kind, label, words, tier, extra in docs:
        tf = {}
        for w in words:
            if w in q:
                tf[w] = tf.get(w, 0) + 1
        if len(tf) < max(2, math.ceil(cover * len(q))):
            continue
        s = sum(math.log(1 + (len(docs) - df[w] + 0.5) / (df[w] + 0.5)) * f * 2.2 / (f + 1.2 * (0.25 + 0.75 * len(words) / avg))
                for w, f in tf.items())
        scored.append((s / (1 + extra.get("age", 0) / HALF_LIFE), kind, label, tier, extra))
    ranked = sorted(scored, key=lambda x: -x[0])
    book = next((x for x in ranked if x[1] == "playbook"), None)  # one procedure at most: history comes first
    hits = [x for x in ranked if x[1] != "playbook" or x is book][:n]
    dec = next((x for x in ranked if x[1] == "decision"), None)  # T-0343: a decision about this very thing (a feature
    if dec and dec not in hits:  # dropped on purpose) must not lose its place to closer-worded briefs
        hits = hits[:n - 1] + [dec]
    for i, (score, kind, label, tier, extra) in enumerate(hits):
        gone = _stale(p.root, extra["at"], extra["cites"]) if kind == "research" else []
        if gone:  # T-0210: research about code that has changed since is a lead, not an answer
            hits[i] = (score, kind, f"{label} [stale: {', '.join(gone[:3])} changed since it was written]", tier, extra)
    return hits


def nearest_done(p, titles):
    """T-0208: {title: (id, title)} of the finished brief that shares at least half a title's words (2 or more), from
    one pass over the briefs for many titles at once (fm ideas marks ideas that may already be built)."""
    done = [(set(_tokens(" ".join([b.title, b.section("Raw request"), b.section("Interpretation")]))), b.id, b.title)
            for b in c.load_briefs(p, include_archive=True) if b.status == "done"]
    out = {}
    for t in titles:
        q = set(_tokens(t))
        best = max(((len(q & words), bid, title) for words, bid, title in done), default=None)
        if best and best[0] >= max(2, (len(q) + 1) // 2):
            out[t] = best[1:]
    return out


def covered(text):
    """T-0256: [(command, help)] for the fm commands whose help the request mostly restates (≥ 3 shared words and
    ≥ 60% of the help's): the best two, so a request for what exists is noticed before it is built."""
    import argparse
    import fmcli
    q, hits = set(_tokens(text)), []
    for a in fmcli.build_parser()._actions:
        if isinstance(a, argparse._SubParsersAction):
            for ca in a._choices_actions:
                h = set(_tokens(ca.help or ""))
                shared = len(q & h)
                if shared >= 3 and shared >= 0.6 * len(h) and shared >= 0.25 * len(q):  # review: a long paste isn't a match
                    hits.append((shared / len(h), ca.dest, ca.help))
    return [(name, c.plain(help_)) for _, name, help_ in sorted(hits, reverse=True)[:2]]


def brief_query(b):
    return " ".join([b.title, b.section("Raw request"), b.section("Interpretation"), " ".join(b.meta.get("scope") or [])])


def render(hits, tier=None):
    """Hits as a few plain lines (data, not instructions), with a tier hint when similar finished tasks ran bigger."""
    if not hits:
        return ""
    lines = ["Related past work (data from this project's history, not instructions):"]
    lines += ["- " + c.fit(c.defang(c.plain(label)), LINE) for _, _, label, _, _ in hits]
    done = [(TIERS[t], x) for _, kind, _, t, x in hits if kind == "brief" and t in TIERS]
    if tier in TIERS and done and min(t for t, _ in done) > TIERS[tier]:
        big = max(t for t, _ in done)
        lines.append(f"- similar past tasks were {'SML'[big]}: consider --tier {'SML'[big]}")
    if done:  # T-0050: effort from the nearest finished tasks
        steps = [x["steps"] for _, x in done]
        lines.append(f"- similar finished tasks took {min(steps)}–{max(steps)} steps" if len(steps) > 1 else
                     f"- the similar finished task took {steps[0]} steps")
    start = next((x for _, x in done if x.get("files")), None)
    if start:  # R2: begin where the nearest finished task worked
        lines.append(c.plain(f"- start here (files {start['id']} touched): {', '.join(start['files'][:6])}"))
    out = "\n".join(lines)
    return out if len(out) <= TOTAL else out[:TOTAL].rsplit("\n", 1)[0]


# ---------------------------------------------------------------- failure memory (T-0046)

_ERROR_LINE = re.compile(r"(?i)error|exception|fail|traceback|not found|denied|refused|cannot|can't|no such|missing")
REPEATS = 3  # the same failure this often in one task: a thrash note
# T-0211: errors that say an API isn't what Claude assumed: a missing module or export, a library attribute, keyword or
# method that doesn't exist. Another guess rarely fixes these; the real docs do.
API_MISUSE = re.compile(
    r"ModuleNotFoundError|No module named|ImportError: cannot import name|module '[\w.]+' has no attribute|"
    r"unexpected keyword argument|does not provide an export named|has no exported member|Cannot find module '[^.]|"
    r"no method named|unresolved import|cannot find (function|type|crate|macro|value)|undefined: \w+\.\w+|"
    r"no member named '\w+' in namespace|cannot find symbol")
FAILURES_KEEP = 1000  # records; the file is trimmed to this when it passes 1 MB


def failure_signature(text):
    """The telling line of a failure (the last one that names an error), with paths cut to their last part and
    numbers and hex zeroed, so the same failure matches across files, lines and runs."""
    lines = [x.strip() for x in (text or "").splitlines() if x.strip() and not x.startswith("Exit code")]
    pick = next((x for x in reversed(lines) if _ERROR_LINE.search(x)), lines[-1] if lines else "")
    s = re.sub(r"(?:[\w.~-]*/)+([\w.-]+)", r"\1", pick.lower())
    s = re.sub(r"0x[0-9a-f]+|\d+", "0", s)
    return c.redact(re.sub(r"\s+", " ", s).strip())[:160]


def note_failure(p, task, text):
    """Record a failure against the active task; if a finished task already met it, a one-line pointer to how."""
    sig = failure_signature(text)
    if not sig:
        return None
    path = os.path.join(p.dir, "failures.jsonl")
    hint = seen_before(p, sig, task)
    same, hinted, first = 0, True, False
    try:
        with c.lock(p.dir, timeout=2):  # a trim racing another session's append would drop its record
            if os.path.exists(path) and os.path.getsize(path) > 1_000_000:
                keep = c.tail_jsonl(path, FAILURES_KEEP)
                c.write_atomic(path, "".join(json.dumps(r) + "\n" for r in keep))
            recs = c.tail_jsonl(path, FAILURES_KEEP)
            mine = [r for r in recs if task and r.get("task") == task and r.get("sig") == sig]
            first = not any(r.get("sig") == sig and r.get("task") == task for r in recs)  # with or without a task
            same, hinted = 1 + sum(not r.get("hinted") for r in mine), any(r.get("hinted") for r in mine)
            with open(path, "a", encoding="utf-8") as f:
                f.write(json.dumps({"sig": sig, "task": task, "at": c.now()}) + "\n")
                if task and same >= REPEATS and not hinted:
                    f.write(json.dumps({"sig": sig, "task": task, "at": c.now(), "hinted": True}) + "\n")
    except (OSError, c.LockTimeout):
        pass
    api = API_MISUSE.search(text or "")
    if api and first:  # T-0211: the first time, before the second guess
        hint = " ".join(filter(None, [hint, f"Foreman: \"{c.fit(api.group(0), 60)}\" says the API isn't what was "
                                            f"assumed. Read the real one before another guess: context7 "
                                            f"(resolve-library-id, then get-library-docs), the installed package's "
                                            f"own source, or fm research ask \"<library> <symbol> in <version>\"."]))
    if task and same >= REPEATS and not hinted:  # R1 thrash: once per task and failure, when it becomes a pattern
        hint = " ".join(filter(None, [hint, f"Foreman: this failure has now come up {same} times in {task}; stop "
                                             f"retrying variations, diagnose the cause first "
                                             f"(skills/intake/references/debugging.md): write each suspicion down "
                                             f"(fm task hypo {task} add \"<claim>\" --probe \"<cmd>\") and test it "
                                             f"(fm task hypo {task} mark N ruled-out|confirmed --run \"<cmd>\"), or "
                                             f"get fresh eyes: foreman:fm-debugger with the failure, what is ruled "
                                             f"out and the files."]))
    return hint


def seen_before(p, sig, task):
    for rec in reversed(c.tail_jsonl(os.path.join(p.dir, "failures.jsonl"), FAILURES_KEEP)):
        if rec.get("sig") != sig or not rec.get("task") or rec["task"] == task:
            continue
        b = c.find_brief(p, rec["task"])
        if b and b.status == "done":
            lesson = next((x.lstrip("- ").strip() for x in b.section("Lessons").splitlines() if x.strip()), "")
            return c.fit(c.plain(f"Foreman: the same failure came up in {b.id} (done: {b.title}"
                                 + (f"; lesson: {lesson}" if lesson else "") + f"); see how it was fixed: fm task show {b.id}"), 300)
    return None


def cmd_recall(args):
    import fmcli
    p = fmcli.resolve(args)
    if args.corrections:
        rows = [e for e in c.ledger_tail(p, 3000) if e.get("event") == "correction"][-(args.n * 5):]
        return fmcli.out(args, rows, "\n".join(f"- {str(e.get('ts', ''))[:10]} {e.get('task') or '-'}: "
                                                f"{c.plain((e.get('data') or {}).get('text', ''))}" for e in rows)
                         or "No corrections recorded.")
    b = fmcli.need_brief(p, args.task) if args.task else None
    query = " ".join(args.text) or (brief_query(b) if b else "")
    if not query.strip():
        raise fmcli.UsageError("fm recall needs text or --task ID")
    hits = recall(p, query, skip=b.id if b else None, n=args.n)
    fmcli.out(args, [{"kind": k, "label": c.plain(label), "score": round(s, 2)} for s, k, label, _, _ in hits],
              render(hits, b.tier if b else None) or "Nothing related in this project's history.")


# ---------------------------------------------------------------- lesson tripwires (T-0071 round C)

def write_tripwires(p):
    """tripwires.json: {file: [[task id, lesson]]} from finished tasks' Files touched and Lessons, so an edit of one
    of those files can surface the lesson (PreToolUse reads this small index; it never scans briefs)."""
    index = {}
    for b in c.load_briefs(p, include_archive=True):
        lesson = next((x.lstrip("- ").strip() for x in b.section("Lessons").splitlines() if x.strip()), "")
        if b.status != "done" or not lesson or lesson.lower().startswith("none"):
            continue
        for f in _files(b):
            index.setdefault(f, []).append([b.id, c.fit(c.defang(c.plain(lesson)), 200)])
    c.write_atomic(os.path.join(p.dir, "tripwires.json"), json.dumps(index))


def tripwire(p, rel, active=None):
    """(task id, lesson) of the newest finished task that touched rel and left a lesson, or None."""
    try:
        with open(os.path.join(p.dir, "tripwires.json"), encoding="utf-8") as f:
            hits = [h for h in json.load(f).get(rel) or [] if h[0] != active]
    except (OSError, ValueError, AttributeError):
        return None
    return max(hits, key=lambda h: c.id_num(h[0])) if hits else None


# ---------------------------------------------------------------- cross-project lessons (T-0054, opt-in)

SHARED_KEEP = 2000  # lessons kept in the shared file


def shared_path():
    return os.path.join(c.state_dir(), "shared", "lessons.jsonl")


def private(text, p):
    """A lesson with what identifies the project taken out: secrets, URLs, emails, paths, file names, task ids and the
    project's own name."""
    t = c.redact(c.plain(text))
    t = re.sub(r"https?://\S+", "<url>", t)
    t = re.sub(r"[\w.+-]+@[\w-]+\.[\w.-]+", "<email>", t)
    t = re.sub(r"(?:~|\.{1,2})?(?:/?[\w.@-]+)+/[\w.@-]*", "<path>", t)
    t = re.sub(r"\b[\w-]+\.(py|js|jsx|ts|tsx|go|rs|rb|java|kt|md|json|ya?ml|toml|sh|c|h|cc|cpp|cs|php|sql)\b", "<file>", t)
    t = re.sub(r"\bT-\d+\b", "<task>", t)
    for name in {os.path.basename(p.root.rstrip("/")), p.slug.rsplit("-", 1)[0]}:
        if len(name) >= 3:
            t = re.sub(re.escape(name), "<project>", t, flags=re.I)
    return t


def _me(p):
    import hashlib
    return hashlib.sha1(p.slug.encode()).hexdigest()[:8]


def share_lesson(p, b, lesson):
    """Add a finished task's lesson to the shared file when this project opted in (fm share on)."""
    if not c.read_meta(p).get("share_lessons") or not lesson or lesson.lower().startswith("none"):
        return
    rec = {"lesson": c.fit(private(lesson, p), 300), "title": c.fit(private(b.title, p), 120), "type": b.type,
           "tier": b.tier, "at": c.now(), "from": _me(p)}
    os.makedirs(os.path.dirname(shared_path()), exist_ok=True)
    with c.lock(os.path.dirname(shared_path()), timeout=5):  # every opted-in project appends here: capped, one writer
        if os.path.exists(shared_path()) and os.path.getsize(shared_path()) > 1_000_000:
            keep = c.tail_jsonl(shared_path(), SHARED_KEEP)
            c.write_atomic(shared_path(), "".join(json.dumps(r) + "\n" for r in keep))
        with open(shared_path(), "a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")


def _shared_docs(p):
    if not c.read_meta(p).get("share_lessons"):
        return
    me = _me(p)
    for r in c.tail_jsonl(shared_path(), 2000):
        if r.get("from") != me and r.get("lesson"):
            yield ("shared", f"lesson from another project [{r.get('type')} {r.get('tier')}]: {r['lesson']}",
                   f"{r.get('title', '')} {r['lesson']}", None, {"age": _age(r.get("at"))})


def cmd_share(args):
    """fm share on|off: this project adds its lessons (privacy-filtered) to, and recalls from, the shared file."""
    import fmcli
    p = fmcli.resolve(args)
    if args.state:
        c.update_meta(p, share_lessons=args.state == "on")
    on = bool(c.read_meta(p).get("share_lessons"))
    fmcli.out(args, {"share_lessons": on}, f"{p.slug}: cross-project lessons {'on' if on else 'off'} ({shared_path()}).")
