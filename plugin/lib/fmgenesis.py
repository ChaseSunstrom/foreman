"""fm genesis (T-2078): the Genesis tower's home, research/genesis in the project's state. gen-0 is kept byte for byte and
read-only; the other tower docs (gap map, lineage, exam results, each generation's seed, missions and critiques) are
filed only in the tower's shape; the status lists every generation."""
import os
import re

import fmcore as c

SHAPE = re.compile(r"(gap-map|lineage|catalogue|report)\.md|exam\.jsonl"
                   r"|gen-[1-9][0-9]*/(seed|(mission|critique)-[a-z0-9][a-z0-9-]*)\.md")
GEN = re.compile(r"gen-([1-9][0-9]*)")


def home(p):
    return os.path.join(p.dir, "research", "genesis")


def init(p, data):
    """Save gen-0 as given (bytes) and make it read-only; refuses a second one."""
    path = os.path.join(home(p), "gen-0.md")
    kinds = c.secret_kinds(data.decode("utf-8", "replace"))
    if kinds:  # gen-0 is never redacted, so a secret would sit in it for good
        raise ValueError(f"gen-0 holds what looks like {', '.join(kinds)}; reword that line first (gen-0 is kept verbatim)")
    with c.lock(p.dir):  # the check sits inside the lock: two inits can't both pass it
        if os.path.exists(path):
            raise ValueError(f"gen-0 is already saved ({path}) and is never edited")
        c.write_atomic(path, data)
        os.chmod(path, 0o444)
    return path


def put(p, name, text):
    if not SHAPE.fullmatch(name):
        raise ValueError(f"{name!r} isn't a tower doc: gap-map.md, lineage.md, catalogue.md, report.md, exam.jsonl, or "
                         "gen-N/seed.md, gen-N/mission-NAME.md, gen-N/critique-NAME.md (N from 1)")
    path = os.path.join(home(p), name)
    with c.lock(p.dir):
        c.write_atomic(path, c.redact(text))
    return path


def status(p):
    d = home(p)
    gens = []
    for name in os.listdir(d) if os.path.isdir(d) else ():
        m, sub = GEN.fullmatch(name), os.path.join(d, name)
        if not (m and os.path.isdir(sub)):
            continue
        files = sorted(os.listdir(sub))
        gens.append({"n": int(m.group(1)), "seed": "seed.md" in files,
                     "missions": [f[8:-3] for f in files if f.startswith("mission-") and f.endswith(".md")],
                     "critiques": [f[9:-3] for f in files if f.startswith("critique-") and f.endswith(".md")]})
    try:
        with open(os.path.join(d, "exam.jsonl"), encoding="utf-8", errors="replace") as f:
            exam = sum(1 for line in f if line.strip())
    except OSError:
        exam = 0
    have = {x: os.path.isfile(os.path.join(d, x)) for x in ("gen-0.md", "gap-map.md", "lineage.md")}
    return {"dir": d, "gen0": have["gen-0.md"], "gap_map": have["gap-map.md"], "lineage": have["lineage.md"],
            "exam_lines": exam, "generations": sorted(gens, key=lambda g: g["n"])}


def _text(s):
    def n(k, xs):
        return f"{len(xs)} {k}{'s' * (len(xs) != 1)}" + (f" ({', '.join(xs)})" if xs else "")
    lines = [f"Genesis — {s['dir']}",
             "gen-0: saved, read-only" if s["gen0"] else "gen-0: none yet (fm genesis init --file F)",
             f"gap map: {'yes' if s['gap_map'] else 'none yet'} · lineage: {'yes' if s['lineage'] else 'none yet'}"]
    lines += [f"gen-{g['n']}: {'seed' if g['seed'] else 'no seed'}, {n('mission', g['missions'])}, "
              f"{n('critique', g['critiques'])}" for g in s["generations"]]
    return "\n".join(lines + [f"exam: {s['exam_lines']} results"])


def cmd_genesis(args):
    import fmcli
    p = fmcli.resolve(args)
    action = args.action or "status"
    if action != "status" and not args.file:
        raise fmcli.UsageError(f"fm genesis {action} needs --file F")
    try:
        if action == "init":
            with open(args.file, "rb") as f:
                path = init(p, f.read())
            c.log_event(p, "genesis_init", data={"path": path}, session=fmcli.session())
            return fmcli.out(args, {"dir": home(p), "path": path}, f"gen-0 saved, read-only: {path}")
        if action == "put":
            if not args.path:
                raise fmcli.UsageError("fm genesis put NAME --file F")
            with open(args.file, encoding="utf-8", errors="replace") as f:
                text = f.read()
            path, kinds = put(p, args.path, text), c.secret_kinds(text)
            c.log_event(p, "genesis_put", data={"name": args.path}, session=fmcli.session())
            return fmcli.out(args, {"dir": home(p), "path": path, "redacted": kinds},
                             f"Filed: {path}" + (f" (redacted: {', '.join(kinds)})" if kinds else ""))
    except (OSError, ValueError) as e:
        raise fmcli.UsageError(str(e))
    s = status(p)
    return fmcli.out(args, s, _text(s))
