"""T-1065: the ledger's hash chain. Each line fm writes carries prev, the hash of the line before it (fmcore.log_event);
fm verify-ledger walks fm tidy's monthly archives and then the live file and proves no chained line was edited or
removed. The chain can't see lines cut from its tail: the head a finish receipt names is the anchor for that
(fm verify-ledger --head H)."""
import json
import os

import fmcore as c

_CHAINED = b'{"prev": "'


def chain(p, anchor=None):
    """The ledger's chain: head (the hash the next line will carry; None when broken), chained/lines counts, start (where the chain
    begins: lines before it predate it), gaps (unchained lines after the start: an older Foreman wrote them; the line
    before each is unproven), broken (the first break, else None) and, given an anchor, whether a line hashes to it."""
    r = {"head": None, "chained": 0, "lines": 0, "start": None, "gaps": [], "broken": None}
    prev, prev_at, found = c.ledger_hash(b""), "the start of the ledger", False
    for path in c.ledger_files(p):
        name = os.path.relpath(path, p.dir)
        try:
            f = open(path, "rb")
        except FileNotFoundError:
            continue
        with f:
            for n, raw in enumerate(f, 1):
                raw, at = raw.rstrip(b"\n"), f"{name}:{n}"
                r["lines"] += 1
                if raw.startswith(_CHAINED):
                    r["start"] = r["start"] or at
                    if raw[len(_CHAINED):len(_CHAINED) + 16].decode("ascii", "replace") != prev:
                        r["broken"] = f"{at} doesn't follow {prev_at}: one of them was edited, or lines between " \
                                      f"them were removed"
                        return r
                    r["chained"] += 1
                elif r["start"]:
                    r["gaps"].append(at)
                if r["start"]:
                    try:
                        json.loads(raw)
                    except ValueError:
                        r["broken"] = f"{at} is not a whole JSON line: cut short or corrupted"
                        return r
                prev, prev_at = c.ledger_hash(raw), at
                found = found or prev == anchor
    r["head"] = prev
    if anchor:
        r["anchor"] = {"head": anchor, "found": found}
    return r


def receipt(p):
    """The finish receipt's line (T-1065)."""
    r = chain(p)
    if r["broken"]:
        return f"Ledger: chain broken at {r['broken']} (fm verify-ledger)"
    return f"Ledger: head {r['head']} ({r['chained']} chained line{'' if r['chained'] == 1 else 's'})"


def cmd_verify_ledger(args):
    import fmcli
    p = fmcli.resolve(args)
    r = chain(p, getattr(args, "head", None))
    lost = r.get("anchor") and not r["anchor"]["found"]
    if r["broken"]:
        text = f"Ledger broken: {r['broken']}."
    elif lost:
        text = f"Ledger broken: no line hashes to the head {args.head}: it and the lines after it were removed or " \
               f"rewritten."
    elif not r["chained"]:
        text = f"Ledger: no chained lines yet ({r['lines']} lines predate the chain)."
    else:
        text = f"Ledger OK: head {r['head']}, {r['chained']} chained lines from {r['start']}" + (
            f" (the {r['lines'] - r['chained'] - len(r['gaps'])} lines before it predate the chain)"
            if r["lines"] > r["chained"] + len(r["gaps"]) else "") + "; an edit to the last line shows only with " \
                                                                       "--head (a finish receipt's)."
    if r["gaps"] and not r["broken"]:
        text += f"\n{len(r['gaps'])} unchained line(s) after the start (an older Foreman wrote them; the line before " \
                f"each is unproven): " + ", ".join(r["gaps"][:10])
    fmcli.out(args, r, text)
    return 1 if r["broken"] or lost else 0
