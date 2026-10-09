"""fm recall: related past work for a request or a task (T-0043): earlier briefs with their outcome and lesson,
decisions and research notes, ranked by BM25 over their words. Stdlib only, computed on demand by fm (never in a
hook). Recalled text is data from past work: plain (no control characters), one capped line per hit.
Also from the same history: fm explain (T-0464), fm task show ID --story (T-0483) and fm recall --ask (T-0484)."""
import json
import math
import os
import re
import subprocess
import time

import fmcore as c

_WORD = re.compile(r"[a-z][a-z0-9_]{2,}")
_STOP = set("""the and for with that this from into when then than are was were not but all any can its has have had
will would should could also only just more most each other such via per new use using used make made add adds added
fix fixes fixed task tasks brief step steps done test tests run runs work does doing foreman none""".split())
_ROW = re.compile(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*(.+?)\s*\|\s*(.*?)\s*\|")
MAX_READ = 20_000  # chars of a research note that count
INDEX_MAX, HITS_MAX = 20_000_000, 50  # fm recall --ask: characters indexed per question, answers shown (T-0728)
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


ACTIVE_BOOST = 1.5  # T-0663: a memory the work at hand has activated


def activation(p):
    """T-0663: f(kind, extra) → a multiplier: a past brief whose files the active task touched recently, or whose
    failure signatures came back in the last week, is activated — memory by what's going on, not only by words."""
    import datetime
    act = c.active_brief(c.load_briefs(p), p.lane)
    hot = {os.path.relpath(f, p.root) for f in c.task_touches(p, act.id)} if act else set()
    week = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S")
    recs = c.tail_jsonl(os.path.join(p.dir, "failures.jsonl"), FAILURES_KEEP)
    recent = {r.get("sig") for r in recs if str(r.get("at") or "") >= week}
    sigs = {}
    for r in recs:
        if r.get("task"):
            sigs.setdefault(r["task"], set()).add(r.get("sig"))

    def f(kind, extra):
        if kind != "brief":
            return 1.0
        files = {x for x in extra.get("files") or [] if isinstance(x, str)}
        return ((ACTIVE_BOOST if hot and files & hot else 1.0)
                * (ACTIVE_BOOST if sigs.get(extra.get("id"), set()) & recent else 1.0))
    return f


def recall(p, query, skip=None, n=HITS, cover=0.0):
    """The n most related documents to query: [(score, kind, label, tier, extra)], best first; a hit shares ≥ 2
    words, and at least `cover` of the query's words (T-0206: research asks for 2/3). Older history counts less (half
    at HALF_LIFE days)."""
    q = set(_tokens(query))
    if not q:
        return []
    act = activation(p)
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
        scored.append((s / (1 + extra.get("age", 0) / HALF_LIFE) * act(kind, extra), kind, label, tier, extra))
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


def nearest_dropped(p, text, skip=None):
    """T-0438: (id, title, why) of the dropped brief that shares at least half the request's words (2 or more), so a
    re-ask is noticed at capture; None when there is none."""
    q, best = set(_tokens(text)), None
    for b in c.load_briefs(p, include_archive=True):
        if b.status != "dropped" or b.id == skip:
            continue
        d = set(_tokens(" ".join([b.title, b.section("Raw request")])))
        n = len(q & d)  # T-0726: and a real share of the dropped one's words, not a few of a batch's hundreds
        if n >= max(2, (len(q) + 1) // 2) and n >= 0.2 * len(d) and (not best or n > best[0]):
            why = re.findall(r"(?m)dropped: (.+)$", b.section("Log"))
            best = (n, b.id, b.title, why[-1] if why else "")
    return best[1:] if best else None


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
    if getattr(args, "magnets", False):  # T-0613: where fixes keep landing
        fixes = {b.id for b in c.load_briefs(p, include_archive=True) if b.type == "FIX"}
        by_file = {}
        for e in c.ledger_tail(p, 50000):
            f = (e.get("data") or {}).get("file")
            if e.get("event") == "touched" and e.get("task") in fixes and f:
                by_file.setdefault(os.path.relpath(f, p.root), set()).add(e["task"])
        rows = sorted(by_file.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:args.n * 4]
        return fmcli.out(args, {"magnets": {f: sorted(t) for f, t in rows}}, "Fix magnets (files the most FIX tasks "
                         "touched):\n" + "\n".join(f"  {f} — {len(t)} fix{'es' if len(t) != 1 else ''} "
                                                    f"({', '.join(sorted(t)[-4:])})" for f, t in rows)
                         if rows else "No FIX task has touched a file yet.")
    if args.ask:  # T-0484
        hits = ask(p, args.ask, n=args.n)
        cited = list(dict.fromkeys(t for h in hits for t in h["cites"]))[:12]
        return fmcli.out(args, {"question": args.ask, "hits": hits, "cited": cited},
                         render_answer(args.ask, hits, cited))
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


# ---------------------------------------------------------------- one ledger event as a line (explain, story)

_KEYS = ("step", "ac", "type", "tier", "lens", "category", "allow", "on", "level", "section", "changes", "evidence", "cmd",
         "result", "how", "text", "decision", "why", "reason", "lesson", "detail", "note", "offer", "running", "sha")


def _detail(data):
    parts = []
    for k in _KEYS:
        v = data.get(k)
        if v is None or v == "" or v == [] or v == {}:
            continue
        v = (("on" if v else "off") if isinstance(v, bool) else ", ".join(f"{a}={b}" for a, b in v.items())
             if isinstance(v, dict) else ", ".join(map(str, v)) if isinstance(v, list) else v)
        parts.append(f"{k} {v}" if k in ("step", "ac") else str(v))
    return c.fit(c.defang(c.plain(" · ".join(parts))), 160)


def _brief_event(e):
    return {"ts": str(e.get("ts") or ""), "event": str(e.get("event") or e.get("kind") or ""), "task": e.get("task"),
            "detail": _detail(e.get("data") or {})}


def _line(e, when):
    return " ".join(filter(None, [when, e["event"], e["task"] or "", e["detail"]]))


# ---------------------------------------------------------------- fm explain (T-0464)

DRIVE_RULES = {  # the branch of the Stop hook behind each decision it logs (fmhooks._drive, _evidence_gate)
    "drive": "work remains and nothing waits on the user, so the Stop hook kept the turn going",
    "drive_wait": "background work was running: its notification wakes the session, so the drive waited for it",
    "drive_offer": "background work was running: the drive offered another queued task to start meanwhile",
    "drive_drained": "the queue was empty in full autonomy: check the product as its user would (once per drain)",
    "drive_reload": "the Foreman UI changed: the turn ended so Claude Code reloads it, then the work resumes",
    "stop_gate": "the turn said a step was done with no evidence recorded for it, so the Stop hook asked for it",
}
GRANTS = ("approval_requested", "approval_granted", "approval_declined", "approval_used", "standing_granted",
          "standing_off")
SETTINGS = ("drive", "autonomy")  # what the drive reads, as the ledger last recorded it
BEHIND = 6  # ledger events shown before a decision


def _hook_events():
    return c.tail_jsonl(os.path.join(c.state_dir(), "events.jsonl"), 20000)


def _apart(a, b):
    ta, tb = c.parse_ts(a), c.parse_ts(b)
    return abs((ta - tb).total_seconds()) if ta and tb else 1e9


def explain(p, what=None):
    """The newest guard block or drive/Stop decision on record (what: block|drive) with the rule that fired, its
    inputs, the ledger events behind it and the hook breaker; None when there is none."""
    ledger, events = c.ledger_tail(p, c.TASK_WINDOW), _hook_events()
    ids = {b.id for b in c.load_briefs(p, include_archive=True)}
    found = [("block", e, "guard_block") for e in ledger if e.get("event") == "guard_block"]
    found += [("drive", e, "stop_gate") for e in ledger if e.get("event") == "stop_gate"]
    # ponytail: drive records from before T-0464 carry no project, so their task id stands in (ids repeat across projects)
    found += [("drive", e, e["kind"]) for e in events if e.get("kind") in DRIVE_RULES
              and (e["project"] == p.slug if e.get("project") else e.get("task") in ids)]
    found = [x for x in found if what in (None, x[0])]
    if not found:
        return None
    kind, e, decision = max(found, key=lambda x: str(x[1].get("ts") or ""))
    ts, task, sid, data = str(e.get("ts") or ""), e.get("task"), e.get("session_id"), e.get("data") or {}
    before = [x for x in ledger if str(x.get("ts") or "") <= ts and x is not e]
    rec = {"kind": kind, "decision": decision, "at": ts, "task": task, "session": sid}
    if kind == "block":
        import fmguard
        cat, detail = str(data.get("category") or ""), str(data.get("detail") or "")
        raw = next((x for x in reversed(events) if x.get("kind") == "guard_block" and x.get("session_id") == sid
                    and x.get("category") == cat and x.get("project") in (p.slug, None)
                    and _apart(x.get("ts"), ts) <= 5), {})  # the hook's own record has the tool and the command
        b = c.find_brief(p, task) if task else None
        try:
            said = fmguard.message(fmguard.Block(cat, detail), fmguard.Ctx(
                p.root, p.root, os.path.expanduser("~"), c.foreman_home(), task_id=task, confine=(p.root, p.root)))
        except Exception:  # an old record the current guard can't word: the rule id still says which check
            said = ""
        rec.update(rule=data.get("rule") or raw.get("rule") or fmguard.rule_id(cat, detail), category=cat,
                   said=c.plain(said), inputs={"tool": raw.get("tool"), "command": c.plain(str(raw.get("cmd") or "")),
                                               "target": c.plain(detail), "task": task,
                                               "task allows": list((b.meta.get("allow") if b else None) or [])})
        grants = [x for x in before if x.get("event") in GRANTS and cat in ((x.get("data") or {}).get("allow") or [])]
    else:
        rec.update(rule=DRIVE_RULES[decision], inputs=dict(
            {k: v for k, v in e.items() if k not in ("ts", "kind", "event", "session_id", "project", "data")}, **data))
        grants = list(filter(None, (next((x for x in reversed(before) if x.get("event") == s), None) for s in SETTINGS)))
    near = [x for x in before if (x.get("task") == task if task else x.get("session_id") == sid)][-BEHIND:]
    rec["grants" if kind == "block" else "settings"] = [_brief_event(x) for x in grants]
    rec["ledger"] = [_brief_event(x) for x in near]
    import fmhooks
    rec["breaker"] = [f"{ev} paused until {time.strftime('%H:%M', time.localtime(v['until']))} after {v.get('fails', 0)} "
                      f"failures in a row" if v.get("until", 0) > time.time() else
                      f"{ev}: {v.get('fails', 0)} failure(s) in a row" for ev, v in sorted(fmhooks.breaker().items())]
    return rec


def render_explain(r):
    when = lambda ts: ts.replace("T", " ").rstrip("Z")
    head = "Guard block" if r["kind"] == "block" else f"Stop hook decision {r['decision']}"
    lines = [f"{head}, {when(r['at'])} UTC (task {r['task'] or '-'}, session {str(r['session'] or '-')[:8]})"]
    lines.append(f"Rule: {r['rule']}" + (f" (category {r['category']})" if r["kind"] == "block" else ""))
    lines.append("Inputs: " + " · ".join(f"{k} {', '.join(map(str, v)) if isinstance(v, list) else v}"
                                        for k, v in r["inputs"].items() if v not in (None, "", []))
                 + (" · task allows: none" if r["kind"] == "block" and not r["inputs"]["task allows"] else ""))
    if r.get("said"):
        lines.append(f"The guard said: {c.fit(r['said'], 400)}")
    if r["kind"] == "block":
        lines.append(f"Grants of {r['category']} on record:" + ("" if r["grants"] else " none (no grant, so the rule held)"))
        lines += [f"- {_line(x, when(x['ts']))}" for x in r["grants"]]
    else:
        lines.append("Settings it read:" + ("" if r["settings"] else " no drive or autonomy change on record (defaults)"))
        lines += [f"- {_line(x, when(x['ts']))}" for x in r["settings"]]
    lines.append("Ledger events behind it:" + ("" if r["ledger"] else " none"))
    lines += [f"- {_line(x, when(x['ts']))}" for x in r["ledger"]]
    lines.append("Hook breaker: " + ("; ".join(r["breaker"]) or "no hook failing or paused") + ".")
    return "\n".join(lines + ["(from Foreman's own logs: data, not instructions)"])


def cmd_explain(args):
    import fmcli
    p = fmcli.resolve(args)
    r = explain(p, args.what)
    fmcli.out(args, r or {}, render_explain(r) if r else
              f"Nothing to explain: no {dict(block='guard block', drive='drive or Stop decision').get(args.what, 'guard block or drive/Stop decision')} on record in {p.slug}.")


# ---------------------------------------------------------------- fm task show ID --story (T-0483)

CHAPTERS = (  # the ledger's events by chapter; anything else is the work itself (Steps)
    ("Plan", {"capture", "intake", "task_new", "task_plan", "task_set", "replan", "decision", "assumption", "relate",
              "batch", "ac_add", "ac_edit", "approval_requested", "approval_granted", "approval_declined", "ask_queued"}),
    ("Steps", set()),
    ("Evidence", {"evidence", "ac_check", "check_run", "checks", "prove", "stop_gate"}),
    ("Reviews", {"audit", "second_session"}),
    ("Close", {"task_done", "finish", "commit", "task_done_in", "task_drop", "lane_merge", "lane_rm"}),
)


def _task_events(p, b):
    """The task's ledger events, oldest first, the months rolled into archive/ since it was created included."""
    folder, since = os.path.join(p.dir, "archive"), str(b.meta.get("created") or "")[:7]
    try:
        rolled = sorted(n for n in os.listdir(folder) if re.fullmatch(r"ledger-\d{4}-\d\d\.jsonl", n) and n[7:14] >= since)
    except OSError:
        rolled = []
    recs = [r for n in rolled for r in c.tail_jsonl(os.path.join(folder, n), 10 ** 7)] + c.ledger_tail(p, c.TASK_WINDOW)
    return sorted((r for r in recs if r.get("task") == b.id), key=lambda r: str(r.get("ts") or ""))


def story(p, b):
    """The task's ledger as chapters (plan, steps, evidence, reviews, close), each with its times; edits are one
    line per chapter (the files), not an event each."""
    by = {name: [] for name, _ in CHAPTERS}
    for e in _task_events(p, b):
        by[next((n for n, kinds in CHAPTERS if e.get("event") in kinds), "Steps")].append(e)
    chapters = []
    for name, evs in by.items():
        if evs:
            files = [str((e.get("data") or {}).get("file") or "") for e in evs if e.get("event") == "touched"]
            chapters.append({"name": name, "from": str(evs[0].get("ts") or ""), "to": str(evs[-1].get("ts") or ""),
                             "events": [_brief_event(e) for e in evs if e.get("event") != "touched"],
                             "edited": sorted({os.path.relpath(f, p.root) if f.startswith(p.root.rstrip("/") + "/")
                                               else f for f in files if f})})
    return {"id": b.id, "title": c.plain(b.title), "type": b.type, "tier": b.tier, "status": b.status,
            "chapters": chapters}


def render_story(s):
    when = lambda ts: ts[5:16].replace("T", " ")
    every = [ch[k] for ch in s["chapters"] for k in ("from", "to")]
    lines = [f"{s['id']} [{s['type']} {s['tier']}, {s['status']}] {s['title']}"
             + (f" — {when(min(every))} → {when(max(every))} UTC" if every else "")]
    for ch in s["chapters"]:
        n = len(ch["events"]) + len(ch["edited"])
        lines.append(f"{ch['name']}  {when(ch['from'])} → {when(ch['to'])} · {n} event{'s' if n != 1 else ''}")
        lines += [f"  {_line(dict(e, task=None), when(e['ts']))}" for e in ch["events"]]
        if ch["edited"]:
            lines.append(f"  edited {len(ch['edited'])} file(s): {c.fit(', '.join(ch['edited']), 140)}")
    if not s["chapters"]:
        lines.append("No ledger events for it on record.")
    return "\n".join(lines)


# ---------------------------------------------------------------- fm recall --ask (T-0484)

_ASKING = set("why how what who whom when where which did does was were is are there their about".split())
_TID = re.compile(r"\bT-\d{4,}\b")
# ledger events whose text is noise, or already in a brief, decisions.md or a research note
_ECHOED = {"touched", "scope_note", "session_start", "focus", "evidence", "audit", "note", "step_add", "step_current",
           "step_done", "ac_add", "ac_check", "task_set", "task_plan", "task_new", "decision", "subagent", "checks",
           "check_run", "capture", "intake", "research", "task_done", "finish"}


def _passages(p):
    """(label, [task ids it cites], text) for every passage the project's memory answers from: a brief's title and
    sections (its Log one entry each), ledger events, decisions.md rows and research paragraphs."""
    for b in c.load_briefs(p, include_archive=True):
        yield f"{b.id} title", [b.id], b.title
        for head, body in b.sections:
            if head == "Related":  # it quotes other tasks: their words, cited as this one
                continue
            for part in (body.splitlines() if head == "Log" else [body]):
                if part.strip():
                    yield f"{b.id} {head}", [b.id], part
    decided = {}
    for e in c.ledger_tail(p, c.TASK_WINDOW):
        d = e.get("data") or {}
        if e.get("event") == "decision" and e.get("task"):
            decided[str(d.get("decision") or "")] = e["task"]
        elif e.get("event") not in _ECHOED:
            text = " ".join(v for v in d.values() if isinstance(v, str) and len(v) >= 12)
            if text:
                yield (f"ledger {e.get('event')} {str(e.get('ts') or '')[:10]}", [e["task"]] if e.get("task") else [],
                       text)
    try:
        with open(os.path.join(p.dir, "decisions.md"), encoding="utf-8", errors="replace") as f:
            for line in f:
                m = _ROW.match(line)
                if m and m.group(1) != "Date":
                    yield (f"decision {m.group(1)}", [decided[m.group(2)]] if m.group(2) in decided else [],
                           f"{m.group(2)} {m.group(3)}")
    except OSError:
        pass
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
        for para in re.split(r"\n\s*\n", text):
            if para.strip():
                yield f"research {n[:-3]}", [], para


def ask(p, question, n=HITS):
    """The n passages that best answer question, best first: [{label, cites, text, score}], ranked by SQLite FTS5's
    BM25 over briefs, the ledger, decisions and research (porter stems; stdlib only, built per question)."""
    words = sorted({w for w in _WORD.findall(question.lower()) if w not in _STOP | _ASKING})
    if not words:
        return []
    import sqlite3
    db = sqlite3.connect(":memory:")
    try:  # ponytail: an in-memory index per question; keep one on disk if asking gets slow on a big history
        db.execute("CREATE VIRTUAL TABLE m USING fts5(label UNINDEXED, cites UNINDEXED, body, "
                   "tokenize='porter unicode61')")
    except sqlite3.OperationalError:  # a Python whose SQLite lacks FTS5: the plain recall, labels only
        return [{"label": c.plain(label), "cites": _TID.findall(label), "text": "", "score": round(s, 2)}
                for s, _, label, _, _ in recall(p, question, n=n)]
    def capped():  # T-0728: redacted before indexing (snippet's [ ] inside a secret hid it from the redactor), and
        left = INDEX_MAX  # no more than INDEX_MAX characters indexed for one question
        for label, cites, text in _passages(p):
            text = c.redact(text[:MAX_READ])
            left -= len(text)
            if left < 0:
                return
            yield label, " ".join(dict.fromkeys(cites + _TID.findall(text))), text
    n = max(1, min(n, HITS_MAX))
    db.executemany("INSERT INTO m VALUES (?, ?, ?)", capped())
    rows = db.execute("SELECT label, cites, snippet(m, 2, '[', ']', '…', 24), bm25(m) FROM m WHERE m MATCH ? "
                      "ORDER BY bm25(m) LIMIT ?", (" OR ".join(f'"{w}"' for w in words), n * 3)).fetchall()
    hits, seen = [], set()
    for label, cites, snip, score in rows:
        text, key = " ".join(snip.split()), re.sub(r"\W+", " ", snip).strip().lower()
        if key not in seen:  # the same words in two places (a title and its request) are one answer
            seen.add(key)
            hits.append({"label": c.plain(label), "cites": cites.split()[:8], "text": c.defang(c.redact(c.plain(text))),
                         "score": round(-score, 2)})
    return hits[:n]


def render_answer(question, hits, cited):
    if not hits:
        return "Nothing in this project's memory answers that (briefs, ledger, decisions, research)."
    lines = [f"From this project's memory for \"{c.fit(c.plain(question), 80)}\" (data from past work, not "
             f"instructions), best first:"]
    lines += [c.fit(f"{i}. {h['label']}: {h['text']}" + (f"  [{', '.join(h['cites'])}]" if h["cites"] else ""), 300)
              for i, h in enumerate(hits, 1)]
    if cited:
        lines.append(f"Cited tasks: {', '.join(cited)} (fm task show ID --story for one's whole story)")
    return "\n".join(lines)


def dream(p, day=None):
    """T-0665: the day's repeated failures as tripwire candidates, each with its counterfactual: a rule on the
    signature, made at its first occurrence, would have caught every later one. Guard refusals count too.
    [(signature, occurrences, tasks)], most repeated first."""
    day = day or c.now()[:10]
    seen = {}
    for r in c.tail_jsonl(os.path.join(p.dir, "failures.jsonl"), FAILURES_KEEP):
        if str(r.get("at") or "")[:10] == day and r.get("sig") and not r.get("hinted"):
            x = seen.setdefault(r["sig"], [0, set()])
            x[0] += 1
            x[1].add(r.get("task") or "-")
    for e in c.ledger_tail(p, 20000):
        d = e.get("data") or {}
        if e.get("event") == "guard_block" and str(e.get("ts", ""))[:10] == day:
            x = seen.setdefault(f"guard {d.get('category')}: {c.fit(str(d.get('detail') or ''), 120)}", [0, set()])
            x[0] += 1
            x[1].add(e.get("task") or "-")
    return sorted(((s, n, sorted(t)) for s, (n, t) in seen.items() if n >= 2), key=lambda x: -x[1])


def cmd_dream(args):
    import fmcli
    p = fmcli.resolve(args)
    day = args.day or c.now()[:10]
    found = dream(p, day)
    lines = [f"- `{c.fit(c.plain(s), 160)}` — {n} times ({', '.join(t)}); a tripwire at the first would have caught "
             f"{n - 1}" for s, n, t in found]
    text = (f"# Dream {day}: the day's repeated failures as tripwire candidates\n\n" + ("\n".join(lines) if lines else
            "Nothing repeated today.") + "\n\nEach is a candidate rule, not one yet: turn a real one into a test or a "
            "tripwire (fm capture), and leave the rest.\n")
    path = os.path.join(p.dir, "research", f"dream-{day}.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    c.write_atomic(path, c.redact(text))
    c.log_event(p, "dream", data={"day": day, "candidates": len(found)})
    return fmcli.out(args, {"day": day, "path": path, "candidates": [{"sig": s, "count": n, "tasks": t}
                                                                     for s, n, t in found]}, text.strip())
