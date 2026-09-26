"""Foreman core: paths, projects, locking, atomic writes, redaction, ledger, briefs, intake, queue.

Stdlib only. Everything that writes state goes through this module (via fm).
"""
import contextlib
import datetime
import fcntl
import hashlib
import heapq
import json
import os
import re
import string
import time
from collections import defaultdict
from dataclasses import dataclass, field

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TYPES = ["RESEARCH", "CLEAN", "PERFORMANCE", "SECURITY", "FIX", "FEATURE"]
RANK = {t: i for i, t in enumerate(TYPES)}
RUNNABLE = {"planned", "active", "verifying"}
OPEN = RUNNABLE | {"captured", "blocked", "deferred"}
CLOSED = {"done", "dropped"}
STATUSES = OPEN | CLOSED
SENSITIVE_MODES = {"default", "manual", "acceptEdits", "plan", "dontAsk"}


class PolicyError(Exception):
    """A state change Foreman refuses on principle (e.g. done without evidence). Exit code 2."""


class LockTimeout(Exception):
    """Another process holds the project lock. Exit code 3."""


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_ts(ts):
    try:
        return datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
    except (TypeError, ValueError):
        return None


def age_days(ts):
    t = parse_ts(ts)
    if not t:
        return None
    return (datetime.datetime.now(datetime.timezone.utc) - t).total_seconds() / 86400


# ---------------------------------------------------------------- paths and projects

def foreman_home():
    h = os.environ.get("FOREMAN_HOME")
    if h:
        return os.path.abspath(os.path.expanduser(h))
    return os.path.join(os.path.expanduser("~"), ".claude", "foreman")


def state_dir():
    return os.path.join(foreman_home(), "state")


def projects_dir():
    return os.path.join(state_dir(), "projects")


def slug_for(root):
    name = re.sub(r"[^a-z0-9]+", "-", os.path.basename(root.rstrip("/")).lower()).strip("-") or "root"
    return f"{name}-{hashlib.sha1(root.encode()).hexdigest()[:6]}"


def git_root(path):
    d = os.path.realpath(path)
    while True:
        if os.path.exists(os.path.join(d, ".git")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


@dataclass
class Project:
    slug: str
    root: str
    dir: str


def _project(slug, root):
    return Project(slug, root, os.path.join(projects_dir(), slug))


def detect_sensitive(root):
    for name in ("settings.local.json", "settings.json"):
        try:
            with open(os.path.join(root, ".claude", name)) as f:
                mode = (json.load(f).get("permissions") or {}).get("defaultMode")
        except (OSError, ValueError, AttributeError):
            continue
        if mode in SENSITIVE_MODES:
            return True
    return False


def read_meta(p):
    with open(os.path.join(p.dir, "meta.json")) as f:
        return json.load(f)


def write_meta(p, meta):
    write_atomic(os.path.join(p.dir, "meta.json"), json.dumps(meta, indent=2, sort_keys=True) + "\n")


def update_meta(p, **changes):
    with lock(p.dir):
        meta = read_meta(p)
        meta.update(changes)
        write_meta(p, meta)
    return meta


def init_project(root, sensitive=None):
    root = os.path.realpath(root)
    p = _project(slug_for(root), root)
    for sub in ("tasks", "research", "archive"):
        os.makedirs(os.path.join(p.dir, sub), exist_ok=True)
    with lock(p.dir):
        path = os.path.join(p.dir, "meta.json")
        if os.path.exists(path):
            meta = read_meta(p)
        else:
            meta = {"slug": p.slug, "created": now(), "last_active": now(), "last_tidy": None,
                    "session": {}, "next_id": 1, "drive": True}
        meta["path"] = root
        meta["sensitive"] = detect_sensitive(root) if sensitive is None else bool(sensitive)
        write_meta(p, meta)
        dec = os.path.join(p.dir, "decisions.md")
        if not os.path.exists(dec):
            write_atomic(dec, "# Decisions\n\n| Date | Decision | Why | Alternatives rejected |\n|---|---|---|---|\n")
    regen_registry()
    return p


def all_projects():
    out = []
    try:
        names = sorted(os.listdir(projects_dir()))
    except FileNotFoundError:
        return out
    for slug in names:
        try:
            with open(os.path.join(projects_dir(), slug, "meta.json")) as f:
                meta = json.load(f)
            out.append((_project(slug, meta["path"]), meta))
        except (OSError, ValueError, KeyError):
            continue
    return out


def project_by_slug(slug):
    for p, _ in all_projects():
        if p.slug == slug:
            return p
    return None


def find_project(cwd, create=False):
    gr = git_root(cwd)
    if gr:
        p = _project(slug_for(gr), gr)
        if os.path.exists(os.path.join(p.dir, "meta.json")):
            return p
        return init_project(gr) if create else None
    cwd = os.path.realpath(cwd)
    best = None
    for p, _ in all_projects():
        if cwd == p.root or cwd.startswith(p.root.rstrip("/") + "/"):
            if best is None or len(p.root) > len(best.root):
                best = p
    return best


def regen_registry():
    rows = sorted(all_projects(), key=lambda pm: pm[1].get("last_active") or "", reverse=True)
    lines = ["# Foreman project registry", "", "_Generated by fm from state/projects/*/meta.json; do not edit._", "",
             "| Slug | Path | Last active | Sensitive |", "|---|---|---|---|"]
    lines += [f"| {p.slug} | {p.root} | {m.get('last_active') or ''} | {'yes' if m.get('sensitive') else 'no'} |"
              for p, m in rows]
    write_atomic(os.path.join(state_dir(), "registry.md"), "\n".join(lines) + "\n")


# ---------------------------------------------------------------- writes and locks

def write_atomic(path, text):
    d = os.path.dirname(path)
    os.makedirs(d, exist_ok=True)
    tmp = os.path.join(d, f".{os.path.basename(path)}.{os.getpid()}.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


@contextlib.contextmanager
def lock(directory, timeout=5.0):
    os.makedirs(directory, exist_ok=True)
    fd = os.open(os.path.join(directory, ".lock"), os.O_CREAT | os.O_RDWR, 0o600)
    deadline = time.monotonic() + timeout
    try:
        while True:
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    raise LockTimeout(f"lock busy: {directory}")
                time.sleep(0.02)
        yield
    finally:
        os.close(fd)  # closing the descriptor releases the flock


# ---------------------------------------------------------------- redaction

_V = r"""[^\s"',;\\]"""
_SECRET_RES = [
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----"), "[REDACTED PRIVATE KEY]"),
    (re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"), "[REDACTED JWT]"),
    (re.compile(r"\b(?:sk-ant-[A-Za-z0-9_-]{8,}|sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}"
                r"|AKIA[0-9A-Z]{16}|xox[abprs]-[A-Za-z0-9-]{10,}|glpat-[A-Za-z0-9_-]{20,}|AIza[0-9A-Za-z_-]{30,})"), "[REDACTED]"),
    (re.compile(r"(?i)(authorization\s*[:=]\s*)(?:(?:bearer|basic|token)\s+)?" + r"""[^\s"'\\]+"""), r"\1[REDACTED]"),
    (re.compile(r"(?i)((?:api[_-]?key|access[_-]?key|secret[_-]?key|client[_-]?secret|auth[_-]?token|token|secret|password|passwd|pwd)"
                r"\s*[=:]\s*)(\\?[\"']?)" + _V + "{4,}"), r"\1\2[REDACTED]"),
    (re.compile(r"(://[^/\s:@]+:)[^@\s/]+@"), r"\1[REDACTED]@"),
]


def redact(text):
    if not isinstance(text, str):
        return text
    for rx, repl in _SECRET_RES:
        text = rx.sub(repl, text)
    return text


def redact_obj(obj):
    if isinstance(obj, str):
        return redact(obj)
    if isinstance(obj, list):
        return [redact_obj(x) for x in obj]
    if isinstance(obj, dict):
        return {k: redact_obj(v) for k, v in obj.items()}
    return obj


# ---------------------------------------------------------------- ledger

def log_event(p, event, task=None, data=None, session=None):
    rec = {"ts": now(), "session_id": session or os.environ.get("FOREMAN_SESSION_ID"), "project": p.slug,
           "task": task, "event": event, "data": redact_obj(data or {})}
    os.makedirs(p.dir, exist_ok=True)
    # One short O_APPEND write per event: atomic for concurrent writers on a local filesystem.
    with open(os.path.join(p.dir, "ledger.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def ledger_tail(p, n=200):
    try:
        with open(os.path.join(p.dir, "ledger.jsonl"), "rb") as f:
            f.seek(0, os.SEEK_END)
            size = f.tell()
            f.seek(max(0, size - 64 * 1024))
            lines = f.read().decode("utf-8", "replace").splitlines()
    except FileNotFoundError:
        return []
    out = []
    for line in lines[-n:]:
        try:
            out.append(json.loads(line))
        except ValueError:
            continue
    return out


# ---------------------------------------------------------------- briefs

def _fmt_value(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (list, tuple)):
        return "[" + ", ".join(str(x) for x in v) + "]"
    return "" if v is None else str(v)


def _parse_value(raw):
    v = re.sub(r"\s+#.*$", "", raw).strip()
    if v.startswith("[") and v.endswith("]"):
        return [x.strip().strip("'\"") for x in v[1:-1].split(",") if x.strip()]
    if v in ("true", "false"):
        return v == "true"
    return v


_STEP_RE = re.compile(r"^(\d+)\.\s+\[([ xX])\]\s+(.*?)(\s+<- CURRENT)?\s*$")
_AC_RE = re.compile(r"^-\s+\[([ xX])\]\s+(.*?)\s*$")
_EV_RE = re.compile(r"^-\s+\((step|ac)\s+(\d+)\)")


@dataclass
class Step:
    n: int
    done: bool
    text: str
    current: bool


@dataclass
class Criterion:
    n: int
    checked: bool
    text: str


class Brief:
    """A task brief: YAML-ish frontmatter + markdown sections. Round-trips unchanged content byte-for-byte."""

    def __init__(self, meta, fm_lines, preamble, sections, path=None):
        self.meta = meta
        self._fm_lines = fm_lines                    # [(key, raw_line)]
        self._orig = {k: v for k, v in meta.items()}
        self.preamble = preamble                     # text between frontmatter and first "## " (title)
        self.sections = sections                     # [[heading, body_text]]
        self.path = path

    # --- parse / render
    @classmethod
    def parse(cls, text, path=None):
        if not text.startswith("---\n"):
            raise ValueError("brief has no frontmatter")
        end = text.find("\n---\n", 4)
        if end < 0:
            raise ValueError("unterminated frontmatter")
        meta, fm_lines = {}, []
        for line in text[4:end].split("\n"):
            m = re.match(r"^([A-Za-z_][\w-]*):(.*)$", line)
            if m:
                meta[m.group(1)] = _parse_value(m.group(2))
                fm_lines.append((m.group(1), line))
            else:
                fm_lines.append((None, line))
        body = text[end + 5:]
        parts = re.split(r"(?m)^## (.*)\n", body)
        preamble, sections = parts[0], [[parts[i], parts[i + 1]] for i in range(1, len(parts), 2)]
        return cls(meta, fm_lines, preamble, sections, path)

    def render(self):
        out, seen = [], set()
        for key, raw in self._fm_lines:
            if key is None:
                out.append(raw)
            elif key in self.meta:
                seen.add(key)
                same = key in self._orig and self.meta[key] == self._orig[key]
                out.append(raw if same else f"{key}: {_fmt_value(self.meta[key])}")
        out += [f"{k}: {_fmt_value(v)}" for k, v in self.meta.items() if k not in seen]
        body = self.preamble + "".join(f"## {h}\n{b}" for h, b in self.sections)
        return "---\n" + "\n".join(out) + "\n---\n" + body

    @classmethod
    def new(cls, id, title, type, tier, raw=None, scope=(), depends=(), source="user", priority="normal",
            status="planned", now=None, explore=False):
        ts = now or globals()["now"]()
        raw_text = "\n".join("> " + line for line in (raw or title).splitlines()) or "> " + title
        with open(os.path.join(PLUGIN_ROOT, "templates", "brief.md"), encoding="utf-8") as f:
            tpl = string.Template(f.read())
        text = tpl.substitute(id=id, title=title, type=type, tier=tier, status=status, priority=priority,
                              scope=_fmt_value(list(scope)), depends_on=_fmt_value(list(depends)), source=source,
                              created=ts, raw=raw_text)
        b = cls.parse(text)
        if explore:
            b.meta["explore"] = True
        return b

    # --- fields
    id = property(lambda self: self.meta.get("id", ""))
    type = property(lambda self: str(self.meta.get("type", "")).upper())
    tier = property(lambda self: self.meta.get("tier", ""))
    status = property(lambda self: self.meta.get("status", ""))
    priority = property(lambda self: self.meta.get("priority", "normal"))

    @property
    def title(self):
        for line in self.preamble.splitlines():
            if line.startswith("# "):
                return line[2:].strip()
        return ""

    # --- sections
    def section(self, name):
        for h, b in self.sections:
            if h.strip() == name:
                return b
        return ""

    def set_section(self, name, body):
        body = body if body.endswith("\n") or not body else body + "\n"
        for s in self.sections:
            if s[0].strip() == name:
                s[1] = body
                return
        self.sections.append([name, body])

    def _append_line(self, name, line):
        cur = self.section(name)
        self.set_section(name, cur + line + "\n")

    def append_log(self, text, ts=None):
        self._append_line("Log", f"- {ts or now()} {redact(text)}")

    # --- steps
    def steps(self):
        out = []
        for line in self.section("Steps").splitlines():
            m = _STEP_RE.match(line)
            if m:
                out.append(Step(int(m.group(1)), m.group(2) in "xX", m.group(3), bool(m.group(4))))
        return out

    def current_step(self):
        return next((s for s in self.steps() if s.current), None)

    def _write_steps(self, steps):
        by_n = {s.n: s for s in steps}
        lines, done_ns = [], set()
        for line in self.section("Steps").splitlines():
            m = _STEP_RE.match(line)
            if m and int(m.group(1)) in by_n:
                s = by_n[int(m.group(1))]
                done_ns.add(s.n)
                lines.append(f"{s.n}. [{'x' if s.done else ' '}] {s.text}" + ("  <- CURRENT" if s.current else ""))
            else:
                lines.append(line)
        for s in steps:
            if s.n not in done_ns:
                lines.append(f"{s.n}. [{'x' if s.done else ' '}] {s.text}" + ("  <- CURRENT" if s.current else ""))
        self.set_section("Steps", "\n".join(lines) + ("\n" if lines else ""))

    def add_step(self, text):
        steps = self.steps()
        has_current = any(s.current and not s.done for s in steps)
        steps.append(Step(len(steps) + 1, False, text.strip(), not has_current))
        self._write_steps(steps)
        return steps[-1].n

    def set_current(self, n):
        steps = self.steps()
        if not any(s.n == n for s in steps):
            raise KeyError(f"no step {n}")
        for s in steps:
            s.current = s.n == n
        self._write_steps(steps)

    def mark_step(self, n):
        steps = self.steps()
        s = next((s for s in steps if s.n == n), None)
        if s is None:
            raise KeyError(f"no step {n}")
        if not self.has_evidence(step=n):
            raise PolicyError(f"{self.id} step {n} has no verification evidence; record it with "
                              f"`fm task evidence {self.id} --step {n} \"<cmd>\" \"<result>\"`")
        was_current, s.done, s.current = s.current, True, False
        if was_current:
            nxt = next((x for x in steps if x.n > n and not x.done), None) or next((x for x in steps if not x.done), None)
            if nxt:
                nxt.current = True
        self._write_steps(steps)

    # --- evidence
    def evidence(self):
        return [l for l in self.section("Verification evidence").splitlines() if l.startswith("- ")]

    def has_evidence(self, step=None, ac=None):
        lines = self.evidence()
        if step is None and ac is None:
            return bool(lines)
        want = ("step", step) if step is not None else ("ac", ac)
        for line in lines:
            m = _EV_RE.match(line)
            if m and (m.group(1), int(m.group(2))) == want:
                return True
        return False

    def add_evidence(self, cmd, result, step=None, ac=None, ts=None):
        tag = f"(step {step}) " if step is not None else f"(ac {ac}) " if ac is not None else ""
        cmd = redact(str(cmd)).replace("`", "'").strip()
        result = redact(str(result)).replace("\n", " ").strip()
        self._append_line("Verification evidence", f"- {tag}`{cmd}` → {result} ({ts or now()})")

    # --- acceptance criteria
    def acceptance(self):
        out = []
        for line in self.section("Acceptance criteria").splitlines():
            m = _AC_RE.match(line)
            if m:
                out.append(Criterion(len(out) + 1, m.group(1) in "xX", m.group(2)))
        return out

    def add_ac(self, text, verify=None):
        line = f"- [ ] {text.strip()}" + (f" — verify with `{verify}`" if verify else "")
        self._append_line("Acceptance criteria", line)

    def check_ac(self, n):
        if not self.has_evidence(ac=n):
            raise PolicyError(f"{self.id} acceptance criterion {n} has no evidence; record it with "
                              f"`fm task evidence {self.id} --ac {n} \"<cmd>\" \"<result>\"`")
        lines, k = [], 0
        for line in self.section("Acceptance criteria").splitlines():
            m = _AC_RE.match(line)
            if m:
                k += 1
                if k == n:
                    line = f"- [x] {m.group(2)}"
            lines.append(line)
        if k < n:
            raise KeyError(f"no acceptance criterion {n}")
        self.set_section("Acceptance criteria", "\n".join(lines) + "\n")

    def done_blockers(self):
        reasons = []
        for s in self.steps():
            if not s.done:
                reasons.append(f"step {s.n} not done: {s.text}")
            elif not self.has_evidence(step=s.n):
                reasons.append(f"step {s.n} has no evidence")
        for a in self.acceptance():
            if not a.checked:
                reasons.append(f"acceptance criterion {a.n} not checked: {a.text}")
        if not self.has_evidence():
            reasons.append("no verification evidence recorded")
        return reasons

    # --- resume
    def set_resume_auto(self, text):
        cur = self.section("Resume here")
        human = cur.split("<!-- auto -->")[0].rstrip("\n")
        body = (human + "\n" if human else "") + "<!-- auto -->\n" + text.rstrip("\n") + "\n"
        self.set_section("Resume here", body)

    def set_resume_note(self, text):
        cur = self.section("Resume here")
        auto = cur[cur.index("<!-- auto -->"):] if "<!-- auto -->" in cur else ""
        self.set_section("Resume here", redact(text).rstrip("\n") + "\n" + auto)


def kebab(s, limit=48):
    k = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return k[:limit].rstrip("-") or "task"


def id_num(tid):
    m = re.match(r"^T-(\d+)$", str(tid))
    return int(m.group(1)) if m else 10 ** 9


_BRIEF_FILE = re.compile(r"^(T-\d+)(?:-.*)?\.md$")


def brief_paths(p, include_archive=False):
    paths = []
    tdir = os.path.join(p.dir, "tasks")
    if os.path.isdir(tdir):
        paths += [os.path.join(tdir, f) for f in sorted(os.listdir(tdir)) if _BRIEF_FILE.match(f)]
    if include_archive:
        for dirpath, _, files in os.walk(os.path.join(p.dir, "archive")):
            paths += [os.path.join(dirpath, f) for f in sorted(files) if _BRIEF_FILE.match(f)]
    return paths


def load_briefs(p, include_archive=False, errors=None):
    out = []
    for path in brief_paths(p, include_archive):
        try:
            with open(path, encoding="utf-8") as f:
                out.append(Brief.parse(f.read(), path))
        except (OSError, ValueError) as e:
            if errors is not None:
                errors.append((path, str(e)))
    return out


def find_brief(p, tid):
    tid = tid.upper()
    for path in brief_paths(p):
        m = _BRIEF_FILE.match(os.path.basename(path))
        if m and m.group(1) == tid:
            with open(path, encoding="utf-8") as f:
                return Brief.parse(f.read(), path)
    return None


def save_brief(p, b, touch=True):
    if touch:
        b.meta["updated"] = now()
    if not b.path:
        b.path = os.path.join(p.dir, "tasks", f"{b.id}-{kebab(b.title)}.md")
    write_atomic(b.path, b.render())
    return b.path


def next_id(p):
    """Allocate the next T-id. Caller must hold the project lock."""
    meta = read_meta(p)
    highest = max([id_num(_BRIEF_FILE.match(os.path.basename(x)).group(1)) for x in brief_paths(p, True)] or [0])
    n = max(int(meta.get("next_id", 1)), highest + 1)
    meta["next_id"] = n + 1
    write_meta(p, meta)
    return f"T-{n:04d}"


# ---------------------------------------------------------------- queue

def _key(b):
    return (0 if b.status in ("active", "verifying") else 1, 0 if b.priority == "urgent" else 1,
            RANK.get(b.type, 99), id_num(b.id))


def order_queue(briefs):
    """Runnable briefs in canonical order with dependencies respected. Returns (queue, cycles, dangling)."""
    by_id = {b.id: b for b in briefs}
    runnable = [b for b in briefs if b.status in RUNNABLE]
    rid = {b.id for b in runnable}
    deps, dangling = {}, []
    for b in runnable:
        ds = []
        for d in b.meta.get("depends_on") or []:
            if d in rid:
                ds.append(d)
            elif d not in by_id:
                dangling.append((b.id, d))
        deps[b.id] = ds
    indeg = {i: len(ds) for i, ds in deps.items()}
    rev = defaultdict(list)
    for i, ds in deps.items():
        for d in ds:
            rev[d].append(i)
    heap = [(_key(by_id[i]), i) for i, n in indeg.items() if n == 0]
    heapq.heapify(heap)
    out = []
    while heap:
        _, i = heapq.heappop(heap)
        out.append(by_id[i])
        for j in rev[i]:
            indeg[j] -= 1
            if indeg[j] == 0:
                heapq.heappush(heap, (_key(by_id[j]), j))
    placed = {b.id for b in out}
    remaining = [i for i in deps if i not in placed]
    cycles = _cycles({i: [d for d in deps[i] if d in remaining] for i in remaining})
    out += sorted((by_id[i] for i in remaining), key=_key)
    return out, cycles, dangling


def _cycles(graph):
    """Strongly connected components of size > 1 (or self-loops), Tarjan."""
    index, low, stack, on, res, counter = {}, {}, [], set(), [], [0]

    def visit(v):
        index[v] = low[v] = counter[0]
        counter[0] += 1
        stack.append(v)
        on.add(v)
        for w in graph.get(v, []):
            if w not in index:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in on:
                low[v] = min(low[v], index[w])
        if low[v] == index[v]:
            comp = []
            while True:
                w = stack.pop()
                on.discard(w)
                comp.append(w)
                if w == v:
                    break
            if len(comp) > 1 or v in graph.get(v, []):
                res.append(sorted(comp, key=id_num))

    for v in sorted(graph, key=id_num):
        if v not in index:
            visit(v)
    return sorted(res)


# ---------------------------------------------------------------- intake language

WORK_TAGS = {"CLEAN": "CLEAN", "REFACTOR": "CLEAN", "TIDY": "CLEAN", "PERFORMANCE": "PERFORMANCE", "PERF": "PERFORMANCE",
             "SECURITY": "SECURITY", "SEC": "SECURITY", "FIX": "FIX", "BUG": "FIX", "FEATURE": "FEATURE",
             "FEAT": "FEATURE", "CAPABILITY": "FEATURE", "CAP": "FEATURE", "ADD": "FEATURE",
             "RESEARCH": "RESEARCH", "SPIKE": "RESEARCH", "INVESTIGATE": "RESEARCH"}
BLOCK_TAGS = {"CONTEXT": "context", "NOTE": "context", "CONSTRAINT": "constraints", "MUST": "constraints",
              "NEVER": "constraints", "DONE-WHEN": "done_when", "ACCEPT": "done_when", "SKIP": "skip", "OUT": "skip"}
_TAG_LINE = re.compile(r"^(?P<tag>[A-Za-z][A-Za-z-]*)(?P<mod>[!?])?:(?:\s+|$)(?P<text>.*)$")
_SCOPE_RE = re.compile(r"(?<![\w@])@([\w./*-]+)")
_REF_RE = re.compile(r"#(T-\d{4,})\b")
_PAUSE = {"pause", "stop", "hold on", "hold", "wait"}


@dataclass
class IntakeItem:
    type: str
    text: str
    urgent: bool = False
    explore: bool = False
    now: bool = False
    scopes: list = field(default_factory=list)
    refs: list = field(default_factory=list)
    raw: str = ""


@dataclass
class IntakeResult:
    items: list = field(default_factory=list)
    context: list = field(default_factory=list)
    constraints: list = field(default_factory=list)
    done_when: list = field(default_factory=list)
    skip: list = field(default_factory=list)
    untagged: str = ""
    overrides: list = field(default_factory=list)


def parse_intake(text):
    r = IntakeResult()
    whole = re.sub(r"[.!]+$", "", text.strip().lower())
    if whole in _PAUSE:
        r.overrides.append("PAUSE")
    elif whole == "resume":
        r.overrides.append("RESUME")
    elif whole == "status":
        r.overrides.append("STATUS")
    elif re.match(r"^that(?:'s| is) for the current task\b", whole):
        r.overrides.append("STEER")
    untagged, current = [], None
    for line in text.splitlines():
        if not line.strip():
            current = None
            continue
        if line[0] in " \t" and current is not None:
            if isinstance(current, IntakeItem):
                current.text += "\n" + line.strip()
                current.raw += "\n" + line
                current.scopes = _SCOPE_RE.findall(current.text)
                current.refs = _REF_RE.findall(current.text)
            else:
                getattr(r, current)[-1] += " " + line.strip()
            continue
        body, is_now = line.strip(), False
        m_now = re.match(r"^NOW:\s*(.*)$", body, re.I)
        if m_now:
            is_now, body = True, m_now.group(1)
            if "NOW" not in r.overrides:
                r.overrides.append("NOW")
        m = _TAG_LINE.match(body)
        tag = m.group("tag").upper() if m else None
        if tag in WORK_TAGS:
            txt = m.group("text").strip()
            item = IntakeItem(WORK_TAGS[tag], txt, urgent=m.group("mod") == "!" or is_now, explore=m.group("mod") == "?",
                              now=is_now, scopes=_SCOPE_RE.findall(txt), refs=_REF_RE.findall(txt), raw=line)
            r.items.append(item)
            current = item
        elif tag in BLOCK_TAGS:
            key = BLOCK_TAGS[tag]
            val = m.group("text").strip()
            getattr(r, key).append(f"{tag}: {val}" if tag in ("MUST", "NEVER") else val)
            current = key
        else:
            untagged.append(body)
            current = None
    r.untagged = "\n".join(untagged)
    return r


_L_WORDS = re.compile(r"\b(migrat\w*|schema|auth\w*|oauth\w*|security|architecture|rewrite|redesign|api|database|"
                      r"cross-cutting|breaking|concurren\w*|payment\w*)\b", re.I)


def guess_tier(type, text):
    if _L_WORDS.search(text):
        return "L"
    if type in ("FIX", "CLEAN") and len(text) <= 60:
        return "S"
    return "M"


# ---------------------------------------------------------------- state views (STATE.md, INBOX.md, --json, --line)

TIDY_EVERY_DAYS = 7


def brief_summary(b):
    steps = b.steps()
    cur = next((s for s in steps if s.current), None)
    return {"id": b.id, "type": b.type, "tier": b.tier, "status": b.status, "title": b.title, "priority": b.priority,
            "explore": bool(b.meta.get("explore")), "source": b.meta.get("source"), "scope": b.meta.get("scope") or [],
            "allow": b.meta.get("allow") or [], "updated": b.meta.get("updated"), "created": b.meta.get("created"),
            "steps_done": sum(s.done for s in steps), "steps_total": len(steps),
            "step": {"n": cur.n, "of": len(steps), "text": cur.text} if cur else None, "path": b.path}


def active_brief(briefs):
    return next((b for b in briefs if b.status in ("active", "verifying")), None)


def _last_log(b):
    lines = [l for l in b.section("Log").splitlines() if l.startswith("- ")]
    return re.sub(r"^- \S+\s*", "", lines[-1]) if lines else ""


def state_dict(p, briefs=None):
    briefs = load_briefs(p) if briefs is None else briefs
    meta = read_meta(p)
    queue, cycles, dangling = order_queue(briefs)
    act = active_brief(briefs)
    since = meta.get("last_tidy") or meta.get("created")
    days = age_days(since)
    return {
        "project": p.slug, "root": p.root,
        "active": brief_summary(act) if act else None,
        "queue": [brief_summary(b) for b in queue if b is not act],
        "inbox": [brief_summary(b) for b in briefs if b.status == "captured"],
        "blocked": [dict(brief_summary(b), reason=_last_log(b)) for b in briefs if b.status == "blocked"],
        "deferred": [b.id for b in briefs if b.status == "deferred"],
        "cycles": cycles, "dangling": [list(d) for d in dangling],
        "sensitive": bool(meta.get("sensitive")), "drive": meta.get("drive", True), "paused": bool(meta.get("paused")),
        "last_tidy": meta.get("last_tidy"),
        "tidy_overdue_days": int(days) if days is not None and days > TIDY_EVERY_DAYS else None,
        "session": meta.get("session") or {},
    }


def _more(n, shown):
    return [f"(+{n - shown} more)"] if n > shown else []


def render_state(sd, ts=None):
    a = sd["active"]
    out = [f"# STATE — {sd['project']}", f"_Generated {ts or now()} by fm from the briefs; do not edit._", "", "## Focus"]
    if a:
        out.append(f"{a['id']} [{a['type']} {a['tier']}] {a['title']}")
        if a["step"]:
            out.append(f"Step {a['step']['n']}/{a['step']['of']}: {a['step']['text']}")
        else:
            out.append(f"Steps: {a['steps_done']}/{a['steps_total']} done")
    else:
        out.append("No active task.")
    out += ["", f"## Queue ({len(sd['queue'])})"]
    out += [f"{i}. {q['id']} {q['type']} {q['tier']}{' !' if q['priority'] == 'urgent' else ''} — {q['title'][:70]}"
            for i, q in enumerate(sd["queue"][:10], 1)] + _more(len(sd["queue"]), 10)
    out += ["", f"## Inbox ({len(sd['inbox'])})"]
    out += [f"- {q['id']} [{q['type']}{'?' if q['explore'] else ''} {q['tier']}] {q['title'][:70]}"
            for q in sd["inbox"][:5]] + _more(len(sd["inbox"]), 5)
    out += ["", f"## Blocked ({len(sd['blocked'])})"]
    out += [f"- {q['id']} — {q['reason'][:80]}" for q in sd["blocked"][:5]] + _more(len(sd["blocked"]), 5)
    out += ["", "## Hygiene", f"Last tidy: {sd['last_tidy'] or 'never'}"
            + (f" (overdue: {sd['tidy_overdue_days']}d)" if sd["tidy_overdue_days"] else "")]
    if sd["cycles"]:
        out.append("Dependency cycles: " + "; ".join(" ↔ ".join(c) for c in sd["cycles"])[:200])
    if sd["dangling"]:
        out.append("Dangling deps: " + ", ".join(f"{a}→{b}" for a, b in sd["dangling"])[:200])
    out += ["", "## Notes", f"Sensitive: {'yes' if sd['sensitive'] else 'no'} · Drive: {'on' if sd['drive'] else 'off'}"
            + (" · PAUSED" if sd["paused"] else "")]
    return "\n".join(out[:60]) + "\n"


def render_inbox(sd, ts=None):
    out = [f"# INBOX — {sd['project']}", f"_Generated {ts or now()} by fm: captured, not yet planned. Do not edit; use fm._", ""]
    for q in sd["inbox"]:
        age = age_days(q["created"])
        out.append(f"- {q['id']} [{q['type']}{'?' if q['explore'] else ''} {q['tier']}] {q['title']}"
                   f" (source: {q['source']}, {int(age) if age is not None else '?'}d old)")
    if not sd["inbox"]:
        out.append("Empty.")
    return "\n".join(out) + "\n"


def state_line(sd):
    a = sd["active"]
    if a:
        head = f"{a['id']} {a['type']}"
        head += f" {a['step']['n']}/{a['step']['of']}" if a["step"] else f" {a['steps_done']}/{a['steps_total']}"
    else:
        head = "idle"
    parts = [head, f"q{len(sd['queue'])}", f"in{len(sd['inbox'])}"]
    if sd["blocked"]:
        parts.append(f"blk{len(sd['blocked'])}")
    if sd["paused"]:
        parts.append("PAUSED")
    return " · ".join(parts)


def regen_views(p, briefs=None):
    sd = state_dict(p, briefs)
    ts = now()
    write_atomic(os.path.join(p.dir, "STATE.md"), render_state(sd, ts))
    write_atomic(os.path.join(p.dir, "INBOX.md"), render_inbox(sd, ts))
    write_atomic(os.path.join(p.dir, "state.line"), state_line(sd) + "\n")
    write_atomic(os.path.join(p.dir, "badge.txt"), badge_text(sd) + "\n")
    return sd


def badge_text(sd):
    """Short focus label for the per-reply badge and terminal title; empty when idle."""
    a = sd["active"]
    if not a:
        return ""
    return f"{a['id']} {a['type']} · " + (f"{a['step']['n']}/{a['step']['of']}" if a["step"] else f"{a['steps_done']}/{a['steps_total']}")


def glob_match(rel, pattern):
    """Scope glob: `**` spans directories, `*` and `?` stay within one; a bare path matches itself and its subtree."""
    pat = pattern.strip().rstrip("/")
    if pat.startswith("./"):
        pat = pat[2:]
    if not any(ch in pat for ch in "*?["):
        return rel == pat or rel.startswith(pat + "/")
    rx, i = "", 0
    while i < len(pat):
        if pat.startswith("**/", i):
            rx, i = rx + "(?:.*/)?", i + 3
        elif pat.startswith("**", i):
            rx, i = rx + ".*", i + 2
        elif pat[i] == "*":
            rx, i = rx + "[^/]*", i + 1
        elif pat[i] == "?":
            rx, i = rx + "[^/]", i + 1
        else:
            rx, i = rx + re.escape(pat[i]), i + 1
    return re.fullmatch(rx, rel) is not None


# ---------------------------------------------------------------- checkpoint / resume

def _git(root, *args, timeout=2):
    import subprocess
    try:
        r = subprocess.run(["git", "-C", root, *args], capture_output=True, text=True, timeout=timeout)
        return r.stdout if r.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        return ""


def git_summary(root):
    branch = _git(root, "rev-parse", "--abbrev-ref", "HEAD").strip()
    changed = [l[3:] for l in _git(root, "status", "--porcelain").splitlines() if len(l) > 3]
    return branch, changed


def touched_since_checkpoint(p, tid):
    files = []
    for e in reversed(ledger_tail(p, 400)):
        if e.get("event") == "checkpoint" and e.get("task") == tid:
            break
        if e.get("event") == "touched" and e.get("task") == tid:
            f = (e.get("data") or {}).get("file")
            if f and f not in files:
                files.append(f)
    return list(reversed(files))


def checkpoint(p, note=None, auto=False, session=None):
    """Flush the exact resume point into the active brief and STATE. Caller holds the lock."""
    briefs = load_briefs(p)
    b = active_brief(briefs)
    data = {"auto": auto}
    if b:
        steps = b.steps()
        cur = b.current_step()
        branch, changed = git_summary(p.root)
        lines = [f"- {now()} " + (f"step {cur.n}/{len(steps)}: {cur.text}" if cur else f"steps {sum(s.done for s in steps)}/{len(steps)} done")]
        if branch:
            lines.append(f"- git: {branch}; {len(changed)} uncommitted" + (": " + ", ".join(changed[:10]) if changed else ""))
        touched = touched_since_checkpoint(p, b.id)
        if touched:
            lines.append("- touched since last checkpoint: " + ", ".join(os.path.relpath(f, p.root) if f.startswith(p.root) else f
                                                                         for f in touched[:15]))
        b.set_resume_auto("\n".join(lines))
        if note:
            b.set_resume_note(note)
        save_brief(p, b)
        data.update(step=cur.n if cur else None, note=note)
    log_event(p, "checkpoint", task=b.id if b else None, data=data, session=session)
    regen_views(p)
    return b


def resume_info(p):
    b = active_brief(load_briefs(p))
    if not b:
        return {"id": None}
    s = brief_summary(b)
    return {"id": b.id, "type": b.type, "tier": b.tier, "title": b.title, "status": b.status, "step": s["step"],
            "steps_done": s["steps_done"], "steps_total": s["steps_total"], "resume": b.section("Resume here").strip(),
            "execution_prompt": b.section("Execution prompt").strip(), "path": b.path}
