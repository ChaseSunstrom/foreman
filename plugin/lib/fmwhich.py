"""fm which TASK (T-1699): the Foreman skills, playbooks and fm commands that fit a task in plain words, each with the
call that loads it. With a dozen skills, eighty playbooks and a hundred commands nobody knows what exists.

Lexical, stdlib only: a document per skill (its name and description, from the skills folder as it is when this runs,
so a skill added later is indexed with no list to update), per playbook (its path and header: title and the lines above
its first section, HEADER_MAX characters at most) and per command (name, help and options' help, as fm help reads them;
not Foreman's own-repo tools, FOREMAN_ONLY). The words are fmrecall.words (\\w+, so 3d and ui count; its stems and
stop words). A document scores the idf of each task word it holds, 1 + NAMED times when its name holds it; it can be
listed when it holds at least half the task's words or its name holds one, and is when it is within CUT of its kind's
best and FLOOR of the best overall. When the listed ones together hold under half the task's words, nothing matches:
one common word ("page" in a login task) isn't a fit.
ponytail: lexical, so a synonym (animation for motion) misses; embeddings if that starts to matter."""
import glob
import math
import os
import re

import fmcore as c

SKILLS = os.environ.get("FOREMAN_SKILLS") or os.path.join(c.PLUGIN_ROOT, "skills")  # tests: a fixture
READ_MAX = 8000  # characters of a file read: a header is near the top
HEADER_MAX = 600  # characters of a playbook's header indexed: a body's common words would outrank real headers
CUT = 0.4  # listed: a score at least this share of its kind's best (a skill's one sentence scores less than a playbook)
FLOOR = 0.25  # and this share of the best overall: a kind whose best is one stray word lists nothing
NAMED = 2  # extra weight of a task word in a document's name (ui/motion, fm notify, foreman:tidy)
STEM = 6  # letters a stem keeps: at fmrecall's 5, archives and architecture are one word
SHOWN = {"skills": 3, "playbooks": 5, "commands": 3}
BIG = 2000  # T-1835: past this many playbooks, candidates come from fmplaybooks.find's index, not every header
SELF = {"which", "help"}  # the commands that answer this same question
FOREMAN_ONLY = {"release", "release-check", "bench", "burden", "evals"}  # Foreman's own repo's tools, not a user's
_USER_ONLY = re.compile(r"^disable-model-invocation:[ \t]*true[ \t]*$", re.M | re.I)


def words(text):
    import fmrecall
    return fmrecall.words(text, cut=STEM)


def _head(path):
    if not os.path.isfile(path):  # a FIFO would block the read
        return ""
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read(READ_MAX)
    except OSError:
        return ""


def skills(root=None):
    """[{name, load, summary, text}] for each skill folder's SKILL.md; a user-only one (disable-model-invocation) is
    one the user types, so that is its load line."""
    import fmplugins
    out = []
    for path in sorted(glob.glob(os.path.join(root or SKILLS, "*", "SKILL.md"))):
        fm = fmplugins._frontmatter(path)
        name = c.plain(fm.get("name") or os.path.basename(os.path.dirname(path)))
        desc = c.plain(fm.get("description") or "")
        if len(desc) > 1 and desc[0] == desc[-1] and desc[0] in "\"'":  # YAML's quoted scalar
            desc = desc[1:-1]
        front = re.match(r"---\n(.*?)\n---", _head(path), re.S)
        typed = bool(front and _USER_ONLY.search(front.group(1)))
        out.append({"name": name, "load": f"(you type /foreman:{name})" if typed else f"Skill foreman:{name}",
                    "summary": desc, "text": f"{name.replace('-', ' ')} {desc}"})
    return out


def playbooks(task=None):
    """[{name, load, summary, text}] for each playbook: its stage and name, then its title and the lines above its
    first section (the Use-when line), HEADER_MAX characters at most; named the way fm playbooks show takes it. Past
    BIG books only the ones fmplaybooks.find returns for the task are read."""
    import fmplaybooks
    out, rels = [], fmplaybooks._playbooks(fmplaybooks.ROOT)
    if task and len(rels) > BIG:
        rels = [x["path"] for x in fmplaybooks.find(task, 4 * SHOWN["playbooks"], fmplaybooks.ROOT)[1]]
    for rel in rels:
        _, prose = fmplaybooks._blocks(_head(os.path.join(fmplaybooks.ROOT, rel)))
        head = prose[:next((i for i, x in enumerate(prose) if x.startswith("## ")), len(prose))]
        head = [x.strip() for x in head if x.strip() and not x.lstrip().startswith("<!--")]
        name = rel.removeprefix("references/").removesuffix(".md")
        title = next((x[2:].strip() for x in head if x.startswith("# ")), name)
        out.append({"name": name, "load": f"fm playbooks show {name}", "summary": c.plain(title),
                    "text": f"{name.replace('/', ' ').replace('-', ' ')} {' '.join(head)[:HEADER_MAX]}"})
    return out


def commands():
    import fmcli
    import fmrecall
    return [{"name": n, "load": f"fm {n}", "summary": fmcli._no_ids(" ".join(h.split())), "text": t}
            for n, (h, t) in sorted(fmrecall.verb_docs().items()) if n.split()[0] not in SELF | FOREMAN_ONLY]


def rank(task, found=None):
    """{kind: [row with its score]} for the task's words, best first; every kind empty when no fit holds half of
    them."""
    want = list(dict.fromkeys(words(task)))
    found = found or {"skills": skills(), "playbooks": playbooks(task), "commands": commands()}
    # T-2248: a name's last segment only; a folder (release/) is shared by every book in it, so as a name word it ties
    # them all and the alphabet picks; it still counts once in the text
    docs = [(kind, x, set(words(x["text"])), set(words(x["name"].rsplit("/", 1)[-1].replace("-", " "))))
            for kind, rows in found.items() for x in rows]
    df = {w: sum(w in d for _, _, d, _ in docs) for w in want}
    idf = {w: math.log(1 + len(docs) / df[w]) for w in want if df[w]}
    scored = [(sum(v for w, v in idf.items() if w in d) + NAMED * sum(v for w, v in idf.items() if w in n), kind, x,
               d & set(want)) for kind, x, d, n in docs if 2 * len(d & set(want)) >= len(want) or n & set(want)]
    top = max((r[0] for r in scored), default=0)
    best = {kind: max((r[0] for r in scored if r[1] == kind), default=0) for kind in found}
    out, covered = {kind: [] for kind in found}, set()
    for s, kind, x, shared in sorted(scored, key=lambda r: (-r[0], r[1], r[2]["name"])):
        if s and s >= CUT * best[kind] and s >= FLOOR * top and len(out[kind]) < SHOWN.get(kind, 3):
            out[kind].append(dict(x, score=round(s, 2)))
            covered |= shared
    return out if 2 * len(covered) >= len(want) else {kind: [] for kind in found}


def cmd(args):
    import fmcli
    import fmrecall
    task = " ".join(args.task)
    if not words(task):
        raise fmcli.UsageError(f"nothing to look up in {task!r}, only words like the, with and need: name the work, "
                               "e.g. fm which add a 3D hero with motion")
    got = rank(task)
    data = {"task": task, **{k: [{x: r[x] for x in ("name", "load", "summary", "score")} for r in v]
                             for k, v in got.items()}}
    if not any(got.values()):
        fmcli.out(args, data, f"Nothing matches {c.fit(c.plain(task), 60)!r}: no skill, playbook or fm command holds "
                  "enough of its words.\nfm help --all lists every command; say what the work is in other words.")
        return 1
    lines = []
    kinds = (("skills", "Skills"), ("playbooks", "Playbooks"), ("commands", "fm commands"))
    for kind, title in sorted(kinds, key=lambda k: -max((r["score"] for r in got[k[0]]), default=0)):  # T-1908
        if got[kind]:
            w = max(len(r["load"]) for r in got[kind]) + 2
            lines += [f"{title}:"] + [f"  {r['load']:<{w}}{fmrecall.gist(r['summary'], task, max(30, 98 - w))}"
                                      for r in got[kind]]
    fmcli.out(args, data, "\n".join(lines))
    return 0
