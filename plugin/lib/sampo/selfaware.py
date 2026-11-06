"""T-3126 (T-3123 part 1): the miss ledger. A user message that points something out ("why isn't X done", "are you also
tracking Y", "have you tried Z") is a thing Sampo should have caught itself. The UserPromptSubmit hook runs `note`:
plain patterns pick the class; a message with no pattern is never sent to a model from the hook (latency on every
turn). `sampo misses` counts the logged `miss` events by class and day; `sampo misses --sweep` asks the user's local
model about recent unmatched questions, naming only the fixed classes below (the model's answer is accepted only if it
is one of them; no Claude-written label ever trains or decides anything). A request or a thanks is not a miss."""
import contextlib
import os
import re

from sampo import core as c

CLASSES = ("stalled", "unfiled", "unmeasured", "invisible", "unreachable", "unused", "dead", "other")
# first match wins; each row is (class, pattern) seeded from the user's own pointing-out messages
PATTERNS = [
    ("stalled", r"\bwhy (is|isn'?t|are|aren'?t|hasn'?t|haven'?t|was|wasn'?t)\b.*\b(done|finished|ready|built|complete|yet)\b"),
    ("stalled", r"\b(still not|not) (done|finished|ready) yet\b"),
    ("unfiled", r"\bare you (also |still )?(keeping track|tracking|fixing|filing|capturing|logging|noting)\b"),
    ("unfiled", r"\b(bugs|problems|issues|workarounds?) you (come|came|run|ran|hit|noticed|see)\b"),
    ("unmeasured", r"\bhow (can|could|do|would) (we|i|you) (improve|speed|make|reduce|cut)\b.*"
                   r"\b(speed|fast|efficien|slow|queue|wait|latency|time)\b"),
    ("unused", r"\bhave you (tried|used|considered|looked at|thought about)\b"),
    ("invisible", r"\bhow (can|could|do|would) i (view|see|find|open|get to|look at|browse)\b"),
    ("unreachable", r"\bwhy (can'?t|couldn'?t|won'?t|doesn'?t|don'?t) (you|we|it|sampo)\b"),
    ("dead", r"\b(is|are|was) (it|that|this|the (job|run|task|build|lane|agent)s?)\b.*\b(stuck|hung|dead|frozen|still running)\b"),
    ("dead", r"\bnothing (is )?(happening|moving|running)\b"),
    ("other", r"\b(make|making) yourself\b|\bself.?aware\b|\bso i (don'?t|do not) (need|have) to (point|tell|remind|ask)\b"
             r"|\byou (missed|forgot|should have|didn'?t notice)\b"),
]
_PATTERNS = [(k, re.compile(p, re.I)) for k, p in PATTERNS]
_SWEEPABLE = re.compile(r"\?\s*$|\byou\b", re.I)  # a question or one aimed at Sampo; the rest is a request or chat
_THANKS = re.compile(r"^\W*(thanks?|thank you|thx|ty|great|nice|ok(ay)?|cool|perfect|yes|no)\W*$", re.I)
MAX_TEXT = 300


def classify(text, ask=None):
    """The miss class of a message, or None. Patterns first; `ask(text)` (a model's one-word answer) only when none
    matched and the message could be aimed at Sampo; an answer outside CLASSES counts as no miss."""
    text = (text or "").strip()
    if not text or _THANKS.match(text):
        return None
    for cls, rx in _PATTERNS:
        if rx.search(text):
            return cls
    if ask and _SWEEPABLE.search(text):
        got = str(ask(text) or "").strip().lower().strip(".")
        return got if got in CLASSES else None
    return None


def note(p, text, session=None, ask=None):
    """Log a `miss` event when the message points something out; returns the class or None. Never raises."""
    try:
        cls = classify(text, ask)
        if cls:
            c.log_event(p, "miss", data={"cls": cls, "text": c.fit(c.redact(c.plain(text)), MAX_TEXT)}, session=session)
        return cls
    except Exception:
        return None


def report(p, days=30):
    """{total, by_class, by_day} over the last `days` days of `miss` events."""
    from datetime import timedelta
    since =(c.clock() - timedelta(days=days)).strftime("%Y-%m-%dT00:00:00Z")
    by_class, by_day = {}, {}
    for e in c.ledger_events(p, ["miss"], since=since):
        d = e.get("data") if isinstance(e.get("data"), dict) else {}
        cls = d.get("cls") if d.get("cls") in CLASSES else "other"
        by_class[cls] = by_class.get(cls, 0) + 1
        day = str(e.get("ts") or "")[:10]
        by_day[day] = by_day.get(day, 0) + 1
    return {"total": sum(by_class.values()), "by_class": by_class, "by_day": dict(sorted(by_day.items())),
            "catches": len(c.ledger_events(p, ["predicted_catch"], since=since))}


def local_ask(p):
    """A one-word classifier on the user's local model, or None when none is up. The prompt names only CLASSES."""
    from sampo import models, moonscale
    prof = moonscale._local(bool(c.read_meta(p).get("sensitive")))
    if not prof:
        return None
    system = ("A user wrote this to their coding assistant. If it points out something the assistant should have "
              "noticed itself, answer with exactly one word from: " + ", ".join(CLASSES)
              + ". If it is a request, a thanks or plain chat, answer: none.")

    def ask(text):
        try:
            r = models.complete(prof, [{"role": "system", "content": system}, {"role": "user", "content": text}],
                                max_tokens=8, timeout=60, think=False)
        except (models.ModelError, OSError, ValueError):
            return None
        return (r or {}).get("text")
    return ask


def sweep(p, days=3):
    """Ask the local model about recent prompts no pattern matched and that were never noted; returns the count
    logged. Idempotent: a prompt already seen (by its text) is skipped."""
    ask = local_ask(p)
    if not ask:
        return 0
    from datetime import timedelta
    since = (c.clock() - timedelta(days=days)).strftime("%Y-%m-%dT00:00:00Z")
    seen = {(e.get("data") or {}).get("text") for e in c.ledger_events(p, ["miss", "miss_checked"], since=since)}
    n = 0
    for e in c.ledger_events(p, ["prompt"], since=since):
        text = c.fit(c.redact(c.plain((e.get("data") or {}).get("text") or "")), MAX_TEXT)
        if text in seen or classify(text) or not _SWEEPABLE.search(text) or _THANKS.match(text):
            continue
        seen.add(text)
        if note(p, text, session=e.get("session_id"), ask=ask):
            n += 1
        else:
            c.log_event(p, "miss_checked", data={"text": text}, session=e.get("session_id"))
    return n


def cmd_misses(args):
    from sampo import cli
    p = cli.resolve(args)
    swept = sweep(p) if getattr(args, "sweep", False) else 0
    r = report(p, getattr(args, "days", 30))
    lines = [f"{r['total']} misses in the last {getattr(args, 'days', 30)} days"
             + (f" ({swept} found by the local model)" if swept else "")]
    lines += [f"  {k:<11} {v}" for k, v in sorted(r["by_class"].items(), key=lambda kv: -kv[1])]
    if r["by_day"]:
        lines.append("per day:")
        lines += [f"  {d}  {n}  {'#' * min(n, 40)}" for d, n in r["by_day"].items()]
    lines.append(f"{r['catches']} catch{'es' if r['catches'] != 1 else ''} (asks Sampo predicted and filed before "
                 f"the user made them)")
    cli.out(args, r, "\n".join(lines))


# ---- T-3128 (T-3123 part 3): the boundary review. No model on the close path: it reads the predictions the tick keeps.
BOUNDARY_CAP, COVERED = 3, 0.6  # captures per boundary; share of a guess's words an open task or a user message must hold


def predicted_asks(p):
    """[(type, text)] the next-request predictor last guessed, best first: the local arm's words, then the structural
    guess's type and files. Reads the stored rows only (foresight.prediction_tick wrote them)."""
    from sampo import foresight
    rows = foresight._book(p)
    out = []
    for r in [r for r in rows if r.get("kind") == "next-request-local"][-1:]:
        pr = r.get("pred") or {}
        if pr.get("words") and pr.get("type") in c.TYPES:
            out.append((pr["type"], " ".join(pr["words"])))
    for r in [r for r in rows if r.get("kind") == "next-request"][-1:]:
        pr = r.get("pred") or {}
        if pr.get("type") in c.TYPES and pr.get("paths"):
            out.append((pr["type"], "work on " + c.joinmore(pr["paths"], 3)))
    return out


MIN_GUESS, MIN_MATCH, OPEN_CAP, REFILE_DAYS = 3, 2, 3, 7  # words a guess needs, words that must match, open predicted captures, days a title stays filed
FLAG = "predicted_open"  # p.dir marker: a boundary filed something; catch() reads no briefs while it is absent


def _held(ask_words, text):
    from sampo import foresight
    hit = len(ask_words & foresight._words(text))
    return len(ask_words) >= MIN_GUESS and hit >= MIN_MATCH and hit / len(ask_words) >= COVERED


def boundary(p):
    """At a task boundary (a close or a drop): the top BOUNDARY_CAP predicted asks no open task covers become inbox
    captures with source 'predicted' (eco.capture_once also dedupes an identical open title). Returns the briefs filed."""
    if c.read_meta(p).get("sensitive"):
        return []
    from sampo import eco, foresight
    open_text = [" ".join([b.title, b.section("Raw request")] + [a.text for a in b.acceptance()])
                 for b in c.load_briefs(p) if b.status not in c.CLOSED]
    every = c.load_briefs(p, include_archive=True)
    room = OPEN_CAP - sum(1 for b in every if b.meta.get("source") == "predicted" and b.status not in c.CLOSED)
    recent = {" ".join(b.title.lower().split()) for b in every if b.meta.get("source") == "predicted"
              and (c.age_days(b.meta.get("created")) or 0) < REFILE_DAYS}  # any status: a dropped guess stays dropped
    filed = []
    for typ, text in predicted_asks(p):
        if len(filed) >= min(BOUNDARY_CAP, room):
            break
        text = c.fit(c.redact(c.plain(text)), 160)
        if " ".join(text.lower().split()) in recent or any(_held(foresight._words(text), t) for t in open_text):
            continue
        b, new = eco.capture_once(p, text, typ, "predicted")
        if new:
            filed.append(b)
            open_text.append(b.title)
    if filed:
        c.write_atomic(os.path.join(p.dir, FLAG), "1")
    return filed


def catch(p, text):
    """A user message that matches an open predicted capture is a catch: logs `predicted_catch`, marks the capture;
    returns the ids caught (each once)."""
    from sampo import foresight
    got, flag = [], os.path.join(p.dir, FLAG)
    if not os.path.exists(flag):
        return got
    live = False
    for b in c.load_briefs(p):
        live = live or (b.meta.get("source") == "predicted" and b.status not in c.CLOSED)
        if b.meta.get("source") == "predicted" and b.status not in c.CLOSED and not b.meta.get("caught") \
                and _held(foresight._words(b.title), text):
            b.meta["caught"] = c.now()
            c.save_brief(p, b)
            c.log_event(p, "predicted_catch", task=b.id, data={"text": c.fit(c.redact(c.plain(text)), MAX_TEXT)})
            got.append(b.id)
    if not live:
        with contextlib.suppress(OSError):
            os.remove(flag)
    return got
