"""T-1648: fm design roll. A seeded, coherent pick: one look card (plugin/skills/library/cards/looks) gives the palette
roles, type pair, motion and texture together, never a mix of cards; the seed picks the card, then which named face of
each type class leads its stack (the generic ones, Inter, Roboto, Arial, never lead and are dropped). --apply writes it
as DESIGN.md's ## Look section, one patch: the file's exact bytes before the first roll go to an undo file in the
project's state, and --undo puts them back (or removes a DESIGN.md the roll created) only while the file is still
what the last roll wrote. A symlinked DESIGN.md is refused. Stdlib only."""
import base64
import hashlib
import json
import os
import random
import secrets
import sys

import fmcore
import fmdesign
import fmpage


def roll(seed, folder=None):
    """{seed, look, title, line, roles, type [{class, lead, stack}], motion, texture} for this seed."""
    rng = random.Random(seed)
    card = rng.choice(fmpage.look_cards(folder))
    type_ = []
    for cls in card["faces"]:
        stack = [f.strip() for f in fmpage.FACES[cls].split(",")]
        low = {f: f.strip('"').lower() for f in stack}
        named = [f for f in stack if low[f] not in fmdesign.GENERIC_FONTS | fmdesign.GENERIC_KEYWORDS]
        lead = rng.choice(named)
        rest = [f for f in stack if f != lead and (low[f] in fmdesign.GENERIC_KEYWORDS
                                                   or low[f] not in fmdesign.GENERIC_FONTS)]
        type_.append({"class": cls, "lead": lead, "stack": ", ".join([lead] + rest)})
    flat = lambda text: " ".join(text.split())  # noqa: E731 one line each in DESIGN.md
    return {"seed": seed, "look": card["name"], "title": card["title"], "line": flat(card["line"]),
            "roles": card["roles"], "type": type_, "motion": flat(card["motion"]), "texture": flat(card["texture"])}


def section(look):
    """DESIGN.md's ## Look section (markdown lines)."""
    s = look["seed"]
    return (["## Look", f"Rolled from the look card `{look['look']}` ({look['title']}), seed {s}: "
             f"`fm design roll --seed {s}` repeats it, `fm design roll --undo` takes it back.", "", look["line"], "",
             "| Role | Hex |", "|---|---|"] + [f"| `{k}` | {v} |" for k, v in look["roles"].items()] + [""]
            + [f"- Type, {t['class']}: `font-family: {t['stack']}`" for t in look["type"]]
            + [f"- Motion: {look['motion']}", f"- Texture: {look['texture']}"])


def _bytes(path):
    """The file's exact bytes (None when there's none); a symlink, a non-file, a big or non-UTF-8 file is refused."""
    if os.path.islink(path):
        raise ValueError(f"{path} is a symlink: roll writes only a plain file (--out the file it points to)")
    if not os.path.lexists(path):
        return None
    text, why = fmdesign._read(path, strict=True)
    if text is None:
        raise ValueError(f"{path}: {why}")
    return text.encode("utf-8")  # strict UTF-8 decodes and encodes back to the same bytes


def _sha(data):
    return None if data is None else hashlib.sha256(data).hexdigest()


def _undo_file(project_dir, out):
    return os.path.join(project_dir, "design-roll", hashlib.sha256(out.encode()).hexdigest()[:16] + ".json")


def _load(path):
    if not os.path.exists(path):
        return None
    try:
        with open(path, encoding="utf-8") as f:
            rec = json.load(f)
        if not isinstance(rec, dict) or not {"before", "after"} <= set(rec):
            raise ValueError("not an undo record")
        return rec
    except (OSError, ValueError) as e:
        raise ValueError(f"the undo file {path} is unreadable ({e}); nothing changed")


def apply(out, look, undo):
    """Write the look as out's ## Look section; the undo file keeps the bytes before the first of a run of rolls."""
    before = _bytes(out)
    prior = _load(undo)
    rec = prior if prior and prior["after"] == _sha(before) else {"path": out, "before": None if before is None else
                                                                  base64.b64encode(before).decode()}
    rec["after"] = None  # until the write lands: --undo refuses a half-done roll rather than guess
    fmcore.write_atomic(undo, json.dumps(rec))
    fmdesign.write_section(out, section(look), os.path.basename(os.path.dirname(out)), heading="## Look")
    rec["after"] = _sha(_bytes(out))
    fmcore.write_atomic(undo, json.dumps(rec))


def undo_roll(out, undo):
    rec = _load(undo)
    if rec is None:
        raise ValueError(f"nothing to undo for {out}: no roll was applied to it")
    if rec["after"] is None or _sha(_bytes(out)) != rec["after"]:
        raise ValueError(f"{out} changed since the roll; nothing restored (its bytes before the roll: {undo})")
    if rec["before"] is None:
        os.remove(out)
    else:
        fmcore.write_atomic(out, base64.b64decode(rec["before"]))
    os.remove(undo)


def cmd_roll(args, fmcli):
    try:
        if args.apply and args.undo:
            raise ValueError("--apply or --undo, not both")
        out = args.out or fmdesign._default_out()
        if out == "-" and (args.apply or args.undo):
            raise ValueError("--apply and --undo need a file, not -")
        out = os.path.join(os.path.realpath(os.path.dirname(os.path.abspath(out))), os.path.basename(out))
        if args.apply or args.undo:
            undo = _undo_file(fmcli.resolve(args).dir, out)
            with fmcore.lock(os.path.join(fmcore.state_dir(), "locks", "design-roll")):
                if args.undo:
                    undo_roll(out, undo)
                    fmcli.out(args, {"out": out, "undone": True}, f"design roll: {out} is back as it was")
                    return 0
                look = roll(secrets.randbelow(10 ** 6) if args.seed is None else args.seed)
                apply(out, look, undo)
        else:
            look = roll(secrets.randbelow(10 ** 6) if args.seed is None else args.seed)
        tail = (f"→ {out} (## Look; fm design roll --undo takes it back)" if args.apply else
                "(--apply writes it into DESIGN.md)")
        fmcli.out(args, dict(look, out=out, applied=args.apply),
                  "\n".join(section(look)) + f"\n\ndesign roll: seed {look['seed']}, {look['title']} {tail}")
        return 0
    except (ValueError, OSError, fmcli.c.LockTimeout) as e:
        print(f"fm: design roll: {e}", file=sys.stderr)
        return 2
