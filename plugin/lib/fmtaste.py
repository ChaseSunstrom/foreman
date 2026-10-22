"""T-1537: the taste ledger for looks (plugin/skills/library/cards/looks). It learns only from what the user says or
does: a look kept, reverted or met with 'not like that', twelve A-or-B calibration answers, and the local files the
user names (read-only, capped, never the network). It ranks the looks by it; the directions skill drafts from the top.
Stored in Foreman's state (state/taste/looks.json), one file for every project: taste is the user's. Stdlib only."""
import json
import os
import re
import stat
import sys

import fmcore as c

LOOKS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "skills", "library", "cards", "looks")
WEIGHTS = {"kept": 3, "reverted": -3, "not": -2, "learned": 1}  # a calibration pick is +1, the other look -1
PAIRS = 12
EVENTS_KEEP = 500  # the oldest go first; ponytail: a cap, not decay; weigh recent events more if old taste drags
WHY_CAP = 200
SOURCE_CAP = 8 * 1024 * 1024  # bytes read of a named file at most: a photo fits, a disk image doesn't
IMAGE_PIXELS = 40_000_000  # a photo past this isn't decoded
LEARN_MAX = 50  # files one fm looks learn reads
_HEX = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})(?![0-9a-fA-F])")
_IMAGE = (b"\x89PNG", b"\xff\xd8\xff", b"GIF8", b"RIFF")
_GENERIC_TAGS = {"look", "style", "palette"}


def looks(folder=LOOKS):
    """name → {title, line, palette (rgb tuples), tags} for each look card."""
    out = {}
    for n in sorted(os.listdir(folder)):
        if not (n.startswith("look-") and n.endswith(".md")):
            continue
        with open(os.path.join(folder, n), encoding="utf-8") as f:
            text = f.read()
        head, _, body = text.partition("\n---\n")
        title = re.search(r'(?m)^title:\s*"?Look:\s*([^"\n]+)', head)
        tags = re.search(r"(?m)^tags:\s*\[([^\]]*)\]", head)
        palette = body.split("\n## Palette", 1)[-1].split("\n## ", 1)[0]
        out[n[:-3]] = {"title": title.group(1).strip() if title else n[5:-3],
                       "line": next((x.strip() for x in body.splitlines() if x.strip()), ""),
                       "palette": [_rgb(h) for h in re.findall(r"\|\s*(#[0-9A-Fa-f]{6})\s*\|", palette)],
                       "tags": [t.strip() for t in (tags.group(1) if tags else "").split(",")
                                if t.strip() and t.strip() not in _GENERIC_TAGS]}
    return out


def _rgb(h):
    h = h.lstrip("#")
    h = "".join(ch * 2 for ch in h) if len(h) == 3 else h
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def name_of(word, known):
    """A look's card name from its name, short name or title ("look-lido", "lido", "Night market")."""
    w = re.sub(r"[\s_]+", "-", str(word or "").strip().lower())
    w = w if w.startswith("look-") else "look-" + w
    if w not in known:
        raise ValueError(f"no look {word!r}: one of {', '.join(sorted(known))}")
    return w


def ledger_path():
    return os.path.join(c.state_dir(), "taste", "looks.json")


def load():
    try:
        with open(ledger_path(), encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and isinstance(data.get("events"), list):
            return data
    except (OSError, ValueError):
        pass  # missing, or broken: start over rather than fail every call (the events are taste, not records)
    return {"events": []}


def _append(*events):
    with c.lock(os.path.dirname(ledger_path())):
        data = load()
        data["events"] = (data["events"] + list(events))[-EVENTS_KEEP:]
        c.write_atomic(ledger_path(), json.dumps(data, indent=1) + "\n")
    return data


def _why(text):
    return c.redact(" ".join(str(text or "").split()))[:WHY_CAP]


def record(signal, look, why="", source=""):
    """One signal about one look: kept, reverted, not ('not like that') or learned (from a file the user named)."""
    if signal not in WEIGHTS:
        raise ValueError(f"no signal {signal!r}: one of {', '.join(WEIGHTS)}")
    e = {"ts": c.now(), "signal": signal, "look": name_of(look, looks())}
    if why:
        e["why"] = _why(why)
    if source:
        e["source"] = _why(source)[:80]
    _append(e)
    return e


def scores(events=None):
    """look → {score, kept, reverted, not, picked, passed, learned}."""
    out = {}

    def bump(look, key, n):
        r = out.setdefault(look, {"score": 0})
        r["score"] += n
        r[key] = r.get(key, 0) + 1
    for e in load()["events"] if events is None else events:
        if not isinstance(e, dict):
            continue
        if e.get("signal") in WEIGHTS and isinstance(e.get("look"), str):  # a hand-edited file: skip what's odd
            bump(e["look"], e["signal"], WEIGHTS[e["signal"]])
        elif e.get("signal") == "calibration" and isinstance(e.get("pairs"), list):
            for pair, ans in zip(e["pairs"], str(e.get("answers") or "")):
                if isinstance(pair, (list, tuple)) and len(pair) == 2 and all(isinstance(x, str) for x in pair):
                    for i, look in enumerate(pair):
                        won = ans == "ab"[i]
                        bump(look, "picked" if won else "passed", 1 if won else -1)
    return out


def rank(events=None):
    """Every look, best first: score, then kept, then name; one the ledger never saw is at 0."""
    s, known = scores(events), looks()
    rows = [dict({"look": n, "title": known[n]["title"], "score": 0}, **s.get(n, {})) for n in known]
    return sorted(rows, key=lambda r: (-r["score"], -r.get("kept", 0), r["look"]))


def rounds_done(events=None):
    return sum(1 for e in (load()["events"] if events is None else events)
               if isinstance(e, dict) and e.get("signal") == "calibration")


def pairs(known, rnd=None):
    """PAIRS A-or-B pairs over the looks; round r pairs each look with the one r+1 places on (sorted), so with twelve
    looks each shows twice, never against itself, and the next round meets new rivals."""
    names = sorted(known)
    if len(names) < 2:
        raise ValueError("calibration needs two looks at least")
    k = 1 + (rounds_done() if rnd is None else rnd) % max(1, (len(names) - 1) // 2)
    return [(names[i % len(names)], names[(i + k) % len(names)]) for i in range(PAIRS)]


def calibrate(answers, rnd=None):
    """Record one calibration: PAIRS answers, each a (the first look), b (the second) or n (neither)."""
    if isinstance(answers, str):  # "a,b,n,…" or "abn…"
        answers = answers.split(",") if "," in answers else list(answers.strip())
    got = [str(a).strip().lower() for a in answers]
    if len(got) != PAIRS or any(a not in ("a", "b", "n") for a in got):
        raise ValueError(f"a calibration is {PAIRS} answers, each a, b or n (neither): got {len(got)}")
    rnd = rounds_done() if rnd is None else rnd
    if rnd < 0:
        raise ValueError("--round is the round fm looks calibrate printed: 0 or more")
    e = {"ts": c.now(), "signal": "calibration", "round": rnd, "pairs": pairs(looks(), rnd), "answers": "".join(got)}
    _append(e)
    return e


def pick(prs, read_key, write, known=None):
    """The keyboard picker: one key per pair (1 or a, 2 or b, n neither); q, Ctrl-D or end of input stops with
    nothing kept (None). Any other key is asked again: an arrow's escape sequence (Esc [ A) answers nothing."""
    known = known or looks()
    answers = []
    for i, (a, b) in enumerate(prs):
        write(f"\n{i + 1}/{len(prs)}  which is more like you?\n"
              f"  1  {known[a]['title']}: {known[a]['line']}\n  2  {known[b]['title']}: {known[b]['line']}\n"
              f"  n  neither   q  stop\n> ")
        while True:
            k = read_key()
            if k in ("", "q", "\x04"):
                write("\nstopped: nothing recorded\n")
                return None
            ans = {"1": "a", "a": "a", "2": "b", "b": "b", "n": "n"}.get(k)
            if ans:
                write(ans + "\n")
                answers.append(ans)
                break
    return answers


def _tty_key():
    import termios
    import tty
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


# ---------------------------------------------------------------- learning from files the user names

def read_named(path):
    """The first SOURCE_CAP bytes of a local regular file the user named; never a URL, a folder or a pipe. Opened
    read-only and non-blocking, then checked, so a swapped-in pipe can't hang it."""
    if re.match(r"(?i)^[a-z][a-z0-9+.-]*://", path):
        raise ValueError("a URL: fm looks learns only from local files you name, never the network")
    fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK | getattr(os, "O_CLOEXEC", 0))
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise ValueError("not a regular file")
        chunks, n = [], 0
        while n < SOURCE_CAP:
            b = os.read(fd, min(1 << 20, SOURCE_CAP - n))
            if not b:
                break
            chunks.append(b)
            n += len(b)
        return b"".join(chunks)
    finally:
        os.close(fd)


def _image_colours(data):
    """A photo's main colours when Pillow is installed (detected, never installed); None without it."""
    try:
        from PIL import Image
    except ImportError:
        return None
    import io
    with Image.open(io.BytesIO(data)) as im:
        if im.size[0] * im.size[1] > IMAGE_PIXELS:  # a small file can unpack huge (a decompression bomb)
            raise ValueError(f"over {IMAGE_PIXELS // 1_000_000} megapixels")
        im.draft("RGB", (64, 64))  # JPEG decodes small; other formats decode whole, bounded by IMAGE_PIXELS
        im = im.convert("RGB")
        im.thumbnail((48, 48))
        return [rgb for _, rgb in sorted(im.getcolors(48 * 48) or [], reverse=True)[:24]]


def _votes(colours, text, known):
    """look → votes: each colour with some hue nearest a look's palette colour (RGB distance 48 or less), and each of
    the look's tags the text names. ponytail: plain RGB distance; a perceptual one (OKLab) if matches look wrong."""
    votes = {}
    for col in colours:
        if max(col) - min(col) < 24:
            continue  # greys and near-whites sit in every palette: no signal
        d, look = min((sum((x - y) ** 2 for x, y in zip(col, p)), n) for n, k in known.items() for p in k["palette"])
        if d <= 48 ** 2:
            votes[look] = votes.get(look, 0) + 1
    words = set(re.findall(r"[a-z][a-z-]+", text.lower()))
    for n, k in known.items():
        hits = sum(1 for t in k["tags"] if t in words)
        if hits:
            votes[n] = votes.get(n, 0) + hits
    return votes


def learn(paths):
    """Learn from the files the user named, each read once (capped, read-only); the best-matching look of each is
    recorded as learned, with the file's name only. → {learned: [{file, look, votes}], skipped: [{file, why}]}."""
    known, learned, skipped = looks(), [], []
    for i, path in enumerate(paths):
        name = os.path.basename(str(path).rstrip("/")) or str(path)
        if i >= LEARN_MAX:  # a shell glob can name thousands: each is read and decoded, so a run stops at LEARN_MAX
            skipped.append({"file": name, "why": f"over {LEARN_MAX} files in one run"})
            continue
        try:
            data = read_named(str(path))
        except (OSError, ValueError) as e:
            skipped.append({"file": name, "why": getattr(e, "strerror", None) or str(e)})
            continue
        if data.startswith(_IMAGE):
            try:
                colours = _image_colours(data)
            except Exception as e:  # a broken or truncated image: say so, learn nothing from it
                skipped.append({"file": name, "why": f"couldn't read the image: {type(e).__name__}"})
                continue
            if colours is None:
                skipped.append({"file": name, "why": "a photo needs Pillow to read (not found; Foreman never "
                                                     "installs it: pip install pillow, then run this again)"})
                continue
            text = ""
        elif b"\0" in data[:4096]:  # another binary (a HEIC photo, a PDF's streams): its bytes would read as noise
            skipped.append({"file": name, "why": "not text, and not a photo Foreman reads (PNG, JPEG, GIF, WebP)"})
            continue
        else:
            text = data.decode("utf-8", "replace")
            colours = [_rgb(h) for h in _HEX.findall(text)[:5000]]
        votes = _votes(colours, text, known)
        if not votes:
            skipped.append({"file": name, "why": "nothing in it matched a look"})
            continue
        best = max(sorted(votes), key=votes.get)
        record("learned", best, source=name)
        learned.append({"file": name, "look": best, "votes": votes[best]})
    return {"learned": learned, "skipped": skipped}


# ---------------------------------------------------------------- fm looks

def _rank_text(rows):
    lines = ["Looks by what you kept (score: kept +3, reverted -3, 'not like that' -2, a calibration pick +1 and its "
             "rival -1, a file you named +1):"]
    for i, r in enumerate(rows, 1):
        counts = ", ".join(f"{k} {r[k]}" for k in ("kept", "reverted", "not", "picked", "passed", "learned") if r.get(k))
        lines.append(f"  {i:2}. {r['look']:<24} {r['score']:+d}" + (f"  ({counts})" if counts else ""))
    return "\n".join(lines)


def cmd_looks(args):
    import fmcli
    action, words = args.action or "rank", list(args.words or [])
    try:
        if action == "rank":
            rows = rank()
            return fmcli.out(args, {"looks": rows, "ledger": ledger_path()}, _rank_text(rows))
        if action in ("keep", "revert", "not"):
            if not words:
                raise ValueError(f"fm looks {action} LOOK: name the look (fm looks lists them)")
            e = record({"keep": "kept", "revert": "reverted"}.get(action, action), " ".join(words), why=args.why or "")
            return fmcli.out(args, e, f"Taste ledger: {e['look']} {e['signal']}.")
        if action == "learn":
            if not words:
                raise ValueError("fm looks learn PATH…: name the pages, photos or files to learn from")
            got = learn(words)
            return fmcli.out(args, got, "\n".join(
                [f"Learned: {x['file']} → {x['look']} ({x['votes']} matches)" for x in got["learned"]]
                + [f"Skipped: {x['file']}: {x['why']}" for x in got["skipped"]]))
        # calibrate
        rnd = rounds_done() if args.round is None else args.round
        if args.answers:
            e = calibrate(args.answers, rnd)
            return fmcli.out(args, {"answered": len(e["answers"]), "round": rnd, "answers": e["answers"]},
                             f"Taste ledger: {len(e['answers'])} answers recorded (round {rnd}).")
        known, prs = looks(), pairs(looks(), rnd)
        if not args.json and sys.stdin.isatty() and sys.stdout.isatty():
            try:
                got = pick(prs, _tty_key, lambda s: (sys.stdout.write(s), sys.stdout.flush()), known)
            except KeyboardInterrupt:  # Ctrl-C: the terminal is restored (_tty_key's finally), nothing recorded
                got = None
            if got is None:
                return 1
            calibrate(got, rnd)
            print(f"Taste ledger: {PAIRS} answers recorded. fm looks shows the ranking.")
            return 0
        rows = [[dict(look=n, title=known[n]["title"], line=known[n]["line"]) for n in pr] for pr in prs]
        return fmcli.out(args, {"round": rnd, "pairs": rows}, "\n".join(
            [f"Calibration round {rnd}: {PAIRS} pairs; answer each a, b or n (neither):"]
            + [f"  {i:2}. a {a['title']}  |  b {b['title']}" for i, (a, b) in enumerate(rows, 1)]
            + [f"Then: fm looks calibrate --round {rnd} --answers a,b,n,… ({PAIRS} answers)"]))
    except ValueError as e:
        raise fmcli.UsageError(str(e))
