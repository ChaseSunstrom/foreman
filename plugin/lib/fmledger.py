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
    r = {"head": None, "chained": 0, "lines": 0, "start": None, "gaps": [], "broken": None, "damaged": []}
    prev, prev_at, found, pending, damage = c.ledger_hash(b""), "the start of the ledger", False, {}, None
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
                if r["start"] and raw.endswith(b"\0"):  # T-1456: an unclean shutdown zero-filled the unflushed tail
                    kept = raw[len(_CHAINED):len(_CHAINED) + 16]  # its own prev, when the zeroing left it
                    if raw.startswith(_CHAINED) and len(kept) == 16 and not kept.strip(b"0123456789abcdef") \
                            and kept.decode() != prev:
                        r["broken"] = f"{at} doesn't follow {prev_at}: one of them was edited, or lines between " \
                                      f"them were removed"
                        return r
                    # keyed by the line before it too: the same number of zero bytes always hashes the same
                    key = f"{prev}:{c.ledger_hash(raw)}"
                    damage = pending[key] = {"at": at, "bytes": len(raw) - len(raw.rstrip(b"\0")), "key": key,
                                             "before": prev}
                    r["damaged"].append(damage)
                    prev, prev_at = c.ledger_hash(raw), at
                    continue
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
                        e = json.loads(raw)
                    except ValueError:
                        r["broken"] = f"{at} is not a whole JSON line: cut short or corrupted"
                        return r
                    # the first write after a crash names the line before the damage: lines removed there show
                    if damage and isinstance(e, dict) and e.get("after_damage") not in (None, damage["before"]):
                        r["broken"] = f"{at} names a different line before the damage at {damage['at']}: lines " \
                                      f"before it were edited or removed"
                        return r
                    damage = None
                    if isinstance(e, dict) and e.get("event") == DAMAGE_ACK:  # it covers only damage before it
                        data = e.get("data") if isinstance(e.get("data"), dict) else {}
                        for k in data.get("keys") or []:
                            if isinstance(k, str) and k in pending:
                                pending.pop(k)["accepted"] = True
                prev, prev_at = c.ledger_hash(raw), at
                found = found or prev == anchor
    if anchor:
        r["anchor"] = {"head": anchor, "found": found}
    if pending:
        d = next(iter(pending.values()))
        r["broken"] = f"{d['at']} ends in {d['bytes']} zero bytes: an unclean shutdown lost the events written just " \
                      f"before it (fm verify-ledger --accept-damage records it once you've checked)"
        r["damage_only"] = True
        return r
    r["head"] = prev
    return r


DAMAGE_ACK = "ledger_damage_ack"


def accept_damage(p, anchor=None):
    """T-1456: one chained line naming each zeroed line not yet accepted; anything but crash damage is never accepted,
    nor is damage while a receipt's head (anchor) is missing."""
    r = chain(p, anchor)
    if not r.get("damage_only") or (anchor and not r["anchor"]["found"]):
        return []
    new = [d for d in r["damaged"] if not d.get("accepted")]
    c.log_event(p, DAMAGE_ACK, data={"keys": [d["key"] for d in new], "lines": [f"{d['at']} ({d['bytes']} zero bytes)"
                                                                              for d in new]})
    return new


def receipt(p):
    """The finish receipt's line (T-1065)."""
    r = chain(p)
    if r["broken"]:
        return f"Ledger: chain broken at {r['broken']} (fm verify-ledger)"
    n = sum(1 for d in r["damaged"] if d.get("accepted"))
    return f"Ledger: head {r['head']} ({r['chained']} chained line{'' if r['chained'] == 1 else 's'}" + \
        (f"; {n} crash-damaged line{'' if n == 1 else 's'} accepted" if n else "") + ")"


def cmd_verify_ledger(args):
    import fmcli
    p = fmcli.resolve(args)
    accepted = accept_damage(p, getattr(args, "head", None)) if getattr(args, "accept_damage", False) else []
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
    if accepted:
        text = "Crash damage accepted: " + ", ".join(f"{d['at']} ({d['bytes']} zero bytes)" for d in accepted) + \
               "\n" + text
    elif getattr(args, "accept_damage", False) and r["broken"]:
        text += "\nNothing accepted: --accept-damage covers only lines an unclean shutdown zeroed."
    if r["damaged"] and not r["broken"]:
        text += "\nCrash damage (accepted; the events written just before each were lost): " + \
                ", ".join(f"{d['at']} ({d['bytes']} zero bytes)" for d in r["damaged"][:10])
    if r["gaps"] and not r["broken"]:
        text += f"\n{len(r['gaps'])} unchained line(s) after the start (an older Foreman wrote them; the line before " \
                f"each is unproven): " + ", ".join(r["gaps"][:10])
    fmcli.out(args, r, text)
    return 1 if r["broken"] or lost else 0


def cmd_outbound(args):
    """T-1086: fm outbound [ID]: the requests a task's sessions made to the outside (hosts, queries, MCP tools), counted."""
    import collections
    import fmcli
    p = fmcli.resolve(args)
    act = c.active_brief(c.load_briefs(p), p.lane)
    tid = args.id or (act.id if act else None)
    if not tid:
        raise fmcli.UsageError("fm outbound needs a task id (no task is focused)")
    n = collections.Counter((e["data"].get("tool"), e["data"].get("target")) for e in c.ledger_events(p, ["outbound"])
                            if e.get("task") == tid)
    rows = [{"tool": t, "target": g, "count": k} for (t, g), k in n.most_common()]
    text = f"{tid}: " + (f"{sum(n.values())} outbound request(s)\n" + "\n".join(
        f"  {r['count']:>3}  {r['tool']}  {r['target']}" for r in rows) if rows else "no outbound requests logged")
    return fmcli.out(args, {"id": tid, "outbound": rows}, text)
