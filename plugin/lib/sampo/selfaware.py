"""T-3126 (T-3123 part 1): the miss ledger. A user message that points something out ("why isn't X done", "are you also
tracking Y", "have you tried Z") is a thing Sampo should have caught itself. The UserPromptSubmit hook runs `note`:
plain patterns pick the class; a message with no pattern is never sent to a model from the hook (latency on every
turn). `sampo misses` counts the logged `miss` events by class and day; `sampo misses --sweep` asks the user's local
model about recent unmatched questions, naming only the fixed classes below (the model's answer is accepted only if it
is one of them; no Claude-written label ever trains or decides anything). A request or a thanks is not a miss."""
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
    return {"total": sum(by_class.values()), "by_class": by_class, "by_day": dict(sorted(by_day.items()))}


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
    cli.out(args, r, "\n".join(lines))
