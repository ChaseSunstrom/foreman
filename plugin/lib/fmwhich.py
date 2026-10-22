"""fm which TASK (T-1699): the Foreman skills, playbooks and fm commands that fit a task in plain words, each with the
call that loads it. With a dozen skills, eighty playbooks and a hundred commands nobody knows what exists.

Lexical, stdlib only: a document per skill (its name and description, from the skills folder as it is when this runs,
so a skill added later is indexed with no list to update), per playbook (its path and header: title and the lines above
its first section) and per command (name, help and options' help, as fm help reads them). The words are fmplaybooks'
(\\w+, so 3d and ui count) with fmrecall's suffix stems and stop words; a document scores the idf of each task word it
holds, 1 + NAMED times when its name holds it, and a kind lists the ones within CUT of its best and FLOOR of the best
overall.
ponytail: lexical, so a synonym (animation for motion) misses; embeddings if that starts to matter."""
import glob
import math
import os
import re

import fmcore as c

SKILLS = os.environ.get("FOREMAN_SKILLS") or os.path.join(c.PLUGIN_ROOT, "skills")  # tests: a fixture
READ_MAX = 8000  # characters of a file read: a header is near the top
CUT = 0.4  # listed: a score at least this share of its kind's best (a skill's one sentence scores less than a playbook)
FLOOR = 0.25  # and this share of the best overall: a kind whose best is one stray word lists nothing
NAMED = 2  # extra weight of a task word in a document's name (ui/motion, fm notify, foreman:tidy)
SHOWN = {"skills": 3, "playbooks": 5, "commands": 3}
SELF = {"which", "help"}  # the commands that answer this same question
_SHORT = set("""to of in on it is be as at by or an my me we us so do if up no go am where were who why they them their
our about some very really please""".split())  # function words fmrecall's stop list leaves in
_USER_ONLY = re.compile(r"^disable-model-invocation:[ \t]*true[ \t]*$", re.M | re.I)


def _stem(w):
    """fmrecall's suffix strip, cut at 6 letters rather than 5 (archives and architecture are two words here)."""
    for suffix in ("ing", "ed", "es", "s"):
        if w.endswith(suffix) and len(w) - len(suffix) >= 4:
            return w[:-len(suffix)][:6]
    return w[:6]


def words(text):
    """A text's stems, less stop words and asking words (need, want, how…)."""
    import fmrecall
    return [_stem(w) for w in re.findall(r"\w+", (text or "").lower()) if len(w) > 1 and w not in _SHORT
            and w not in fmrecall._STOP and fmrecall._stem(w) not in fmrecall._CAN_ASK]


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
        front = re.match(r"---\n(.*?)\n---", _head(path), re.S)
        typed = bool(front and _USER_ONLY.search(front.group(1)))
        out.append({"name": name, "load": f"(you type /foreman:{name})" if typed else f"Skill foreman:{name}",
                    "summary": desc, "text": f"{name.replace('-', ' ')} {desc}"})
    return out


def playbooks():
    """[{name, load, summary, text}] for each playbook: its stage and name, title and the lines above its first
    section (the Use-when line), the way fm playbooks show names it."""
    import fmplaybooks
    out = []
    for rel in fmplaybooks._playbooks(fmplaybooks.ROOT):
        _, prose = fmplaybooks._blocks(_head(os.path.join(fmplaybooks.ROOT, rel)))
        head = prose[:next((i for i, x in enumerate(prose) if x.startswith("## ")), len(prose))]
        head = [x for x in head if x.strip() and not x.lstrip().startswith("<!--")]
        name = rel.removeprefix("references/").removesuffix(".md")
        title = next((x[2:].strip() for x in head if x.startswith("# ")), name)
        out.append({"name": name, "load": f"fm playbooks show {name}", "summary": c.plain(title),
                    "text": f"{name.replace('/', ' ').replace('-', ' ')} {' '.join(head)}"})
    return out


def commands():
    import fmcli
    import fmrecall
    return [{"name": n, "load": f"fm {n}", "summary": fmcli._no_ids(" ".join(h.split())), "text": t}
            for n, (h, t) in sorted(fmrecall.verb_docs().items()) if n not in SELF]


def rank(task, found=None):
    """{kind: [row with its score]} for the task's words, best first; every kind empty when nothing shares a word."""
    want = list(dict.fromkeys(words(task)))
    found = found or {"skills": skills(), "playbooks": playbooks(), "commands": commands()}
    docs = [(kind, x, set(words(x["text"])), set(words(x["name"].replace("/", " ").replace("-", " "))))
            for kind, rows in found.items() for x in rows]
    df = {w: sum(w in d for _, _, d, _ in docs) for w in want}
    idf = {w: math.log(1 + len(docs) / df[w]) for w in want if df[w]}
    scored = [(sum(v for w, v in idf.items() if w in d) + NAMED * sum(v for w, v in idf.items() if w in n), kind, x)
              for kind, x, d, n in docs]
    top = max((s for s, _, _ in scored), default=0)
    best = {kind: max((s for s, k, _ in scored if k == kind), default=0) for kind in found}
    out = {kind: [] for kind in found}
    for s, kind, x in sorted(scored, key=lambda r: (-r[0], r[1], r[2]["name"])):
        if s and s >= CUT * best[kind] and s >= FLOOR * top and len(out[kind]) < SHOWN.get(kind, 3):
            out[kind].append(dict(x, score=round(s, 2)))
    return out


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
        fmcli.out(args, data, f"Nothing matches {c.fit(c.plain(task), 60)!r}: no skill, playbook or fm command shares "
                  "its words.\nfm help --all lists every command; say what the work is in other words.")
        return 1
    lines = []
    for kind, title in (("skills", "Skills"), ("playbooks", "Playbooks"), ("commands", "fm commands")):
        if got[kind]:
            w = max(len(r["load"]) for r in got[kind]) + 2
            lines += [f"{title}:"] + [f"  {r['load']:<{w}}{fmrecall.gist(r['summary'], task, max(30, 98 - w))}"
                                      for r in got[kind]]
    fmcli.out(args, data, "\n".join(lines))
    return 0
