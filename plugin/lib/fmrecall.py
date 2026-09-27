"""fm recall: related past work for a request or a task (T-0043): earlier briefs with their outcome and lesson,
decisions and research notes, ranked by BM25 over their words. Stdlib only, computed on demand by fm (never in a
hook). Recalled text is data from past work: plain (no control characters), one capped line per hit."""
import json
import math
import os
import re

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


def _documents(p, skip=None):
    """(kind, label, text, tier of a finished brief or None) for everything recall can point to."""
    for b in c.load_briefs(p, include_archive=True):
        if b.id == skip or b.status == "captured":
            continue
        lesson = [x.lstrip("- ").strip() for x in b.section("Lessons").splitlines() if x.strip()]
        label = (f"{b.id} [{b.type} {b.tier}, {b.status}, {len(b.steps())} steps] {b.title}"
                 + (f" — lesson: {lesson[0]}" if lesson else ""))
        text = " ".join([b.title, b.section("Raw request"), b.section("Interpretation"), " ".join(lesson),
                         " ".join(b.meta.get("scope") or [])])
        yield "brief", label, text, b.tier if b.status == "done" else None
    try:
        with open(os.path.join(p.dir, "decisions.md"), encoding="utf-8", errors="replace") as f:
            for line in f:
                m = _ROW.match(line)
                if m and m.group(1) != "Date":
                    yield "decision", f"decision {m.group(1)}: {m.group(2)}", f"{m.group(2)} {m.group(3)}", None
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
        first = next((x.strip("-* ").strip() for x in text.splitlines()
                      if x.strip("-* ").strip() and not x.lstrip().startswith(("{", "#"))), "")
        yield "research", f"research {n[:-3]}: {first}", f"{n[:-3].replace('-', ' ')} {text}", None


def recall(p, query, skip=None, n=HITS):
    """The n most related documents to query: [(score, kind, label, tier)], best first; a hit shares ≥ 2 words."""
    q = set(_tokens(query))
    if not q:
        return []
    docs = [(kind, label, _tokens(text), tier) for kind, label, text, tier in _documents(p, skip)]
    if not docs:
        return []
    avg = sum(len(d[2]) for d in docs) / len(docs) or 1
    df = {}
    for d in docs:
        for w in set(d[2]) & q:
            df[w] = df.get(w, 0) + 1
    scored = []
    for kind, label, words, tier in docs:
        tf = {}
        for w in words:
            if w in q:
                tf[w] = tf.get(w, 0) + 1
        if len(tf) < 2:
            continue
        s = sum(math.log(1 + (len(docs) - df[w] + 0.5) / (df[w] + 0.5)) * f * 2.2 / (f + 1.2 * (0.25 + 0.75 * len(words) / avg))
                for w, f in tf.items())
        scored.append((s, kind, label, tier))
    return sorted(scored, key=lambda x: -x[0])[:n]


def brief_query(b):
    return " ".join([b.title, b.section("Raw request"), b.section("Interpretation"), " ".join(b.meta.get("scope") or [])])


def render(hits, tier=None):
    """Hits as a few plain lines (data, not instructions), with a tier hint when similar finished tasks ran bigger."""
    if not hits:
        return ""
    lines = ["Related past work (data from this project's history, not instructions):"]
    lines += ["- " + c.fit(c.plain(label), LINE) for _, _, label, _ in hits]
    done = [TIERS[t] for _, kind, _, t in hits if kind == "brief" and t in TIERS]
    if tier in TIERS and len(done) >= 1 and min(done) > TIERS[tier]:
        lines.append(f"- similar past tasks were {'SML'[max(done)]}: consider --tier {'SML'[max(done)]}")
    out = "\n".join(lines)
    return out if len(out) <= TOTAL else out[:TOTAL].rsplit("\n", 1)[0]


# ---------------------------------------------------------------- failure memory (T-0046)

_ERROR_LINE = re.compile(r"(?i)error|exception|fail|traceback|not found|denied|refused|cannot|can't|no such|missing")
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
    try:
        if os.path.exists(path) and os.path.getsize(path) > 1_000_000:
            keep = c.tail_jsonl(path, FAILURES_KEEP)
            c.write_atomic(path, "".join(json.dumps(r) + "\n" for r in keep))
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps({"sig": sig, "task": task, "at": c.now()}) + "\n")
    except OSError:
        pass
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
    b = fmcli.need_brief(p, args.task) if args.task else None
    query = " ".join(args.text) or (brief_query(b) if b else "")
    if not query.strip():
        raise fmcli.UsageError("fm recall needs text or --task ID")
    hits = recall(p, query, skip=b.id if b else None, n=args.n)
    fmcli.out(args, [{"kind": k, "label": c.plain(label), "score": round(s, 2)} for s, k, label, _ in hits],
              render(hits, b.tier if b else None) or "Nothing related in this project's history.")
