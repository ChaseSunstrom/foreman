"""fm doctor: Foreman self-check (BUILD_PROMPT §12). Each check returns a Result; FAIL makes the command exit 1."""
import glob
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from dataclasses import asdict, dataclass

import fmcore as c
import fmpy
import fmserve
import fmsetup

PLUGIN = c.PLUGIN_ROOT
RULES_MAX, BLOCK_MAX, ALWAYS_ON_MAX = 80, 5, 120
DESCRIPTIONS_MAX = 6000  # chars (~1.5k tokens) of skill/agent/command descriptions, loaded in every session
SKILL_MAX = 10000  # chars of one SKILL.md body: loaded whole whenever the skill runs
RULES_CHARS_MAX = 6400  # T-1279: the reply format moved in from the output style; chars (~1.5k tokens) of always-on rules: denser lines cost as much as more lines
CTX_BUDGET, PROMPT_BUDGET = 2000, 400
READ_ONLY_TOOLS = {"Read", "Grep", "Glob", "WebFetch", "WebSearch"}
EDITING_AGENTS = {"fm-builder.md": {"Edit", "Write", "Bash"},  # T-0234: bounded exceptions, each in its own worktree
                  "fm-reproducer.md": {"Edit", "Write", "Bash"}}  # T-0608: the failing test, on its lane branch
EXPECTED_EXIT = {"PreToolUse:Bash:block": [2], "TaskCompleted": [2]}  # fixtures that are designed to block
SCRIPTS = ["install.sh", "setup-plugins.sh", "configure-repo.sh", "reset-claude.sh", "plugin/uninstall.sh"]


@dataclass
class Result:
    name: str
    status: str  # PASS | WARN | FAIL
    detail: str = ""


def _load_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def _read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return None


def _run(cmd, timeout=120, **kw):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, **kw)
    except (OSError, subprocess.SubprocessError) as e:
        return subprocess.CompletedProcess(cmd, 127, "", str(e))


# ---------------------------------------------------------------- individual checks

def check_settings_json(paths):
    bad, checked = [], 0
    for p in paths:
        if not os.path.exists(p):
            continue
        checked += 1
        try:
            with open(p, encoding="utf-8") as f:
                json.load(f)
        except ValueError as e:
            bad.append(f"{p}: {e}")
    return Result("settings json", "FAIL" if bad else "PASS", "; ".join(bad) or f"{checked} file(s) valid")


def check_hook_scripts(plugin=PLUGIN):
    hooks = (_load_json(os.path.join(plugin, "hooks", "hooks.json")) or {}).get("hooks") or {}
    problems, cmds = [], set()
    for groups in hooks.values():
        for g in groups:
            for h in g.get("hooks", []):
                cmds.add(h.get("command", "").replace("${CLAUDE_PLUGIN_ROOT}", plugin))
    for extra in ("bin/fm", "hooks/statusline", "hooks/subagent-statusline"):
        cmds.add(os.path.join(plugin, extra))
    for cmd in sorted(cmds):
        if not os.path.exists(cmd):
            problems.append(f"missing {cmd}")
        elif not os.access(cmd, os.X_OK):
            problems.append(f"not executable {cmd}")
    if not hooks:
        problems.append("hooks.json has no hooks")
    return Result("hook scripts", "FAIL" if problems else "PASS", "; ".join(problems) or f"{len(cmds)} executables OK")


PSI_CPU = "/proc/pressure/cpu"


def busy():
    """'cpu pressure P%' when tasks waited for a CPU at least 10% of the last 10 s (T-1219: the 1-minute load lags a
    sudden burst, such as the test suite starting), else 'load L on N cores' when that passes the core count, else
    None (T-0367)."""
    try:
        with open(PSI_CPU, encoding="ascii") as f:
            some = float(f.readline().split("avg10=", 1)[1].split()[0])
        if some >= 10:
            return f"cpu pressure {some:.0f}%"
    except (OSError, ValueError, IndexError):
        pass
    try:
        load, cores = os.getloadavg()[0], os.cpu_count() or 1
    except (OSError, AttributeError):
        return None
    return f"load {load:.1f} on {cores} cores" if load > cores else None


def bench_runs(busy):
    """A busy machine runs each fixture once: the exit codes still count, the timings wouldn't."""
    return 1 if busy else 5


def check_hook_latency(bench, busy=None):
    if busy:
        return Result("hook latency", "WARN", f"not measured: {busy} (run plugin/tests/bench_hooks.py when it's idle)")
    over =[f"{k} p95 {v['p95']}ms > {v['budget']}ms" for k, v in bench.items() if not v["ok"]]
    worst = max((v["p95"] for v in bench.values()), default=0)
    return Result("hook latency", "FAIL" if over else "PASS", "; ".join(over) or f"all {len(bench)} fixtures, worst p95 {worst} ms")


SLO_RUNS = 200  # T-0486: the recent PreToolUse runs the SLO judges (state/events.jsonl, hook_ms)


def _p95(xs):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(len(xs) * 0.95))]  # as bench_hooks takes it


def check_hook_slo():
    """T-0486: the guard's real latency, from the hooks' own timings, against bench_hooks' budget; over it, the Foreman
    revision where it rose (the first whose own p95 is over, after one under). In-process time: import time isn't in it."""
    try:
        if os.path.join(PLUGIN, "tests") not in sys.path:
            sys.path.insert(0, os.path.join(PLUGIN, "tests"))
        import bench_hooks
        slo = bench_hooks.BUDGET_MS["default"]
    except Exception:  # an install without the tests folder
        slo = 150
    runs = [e for e in c.tail_jsonl(os.path.join(c.state_dir(), "events.jsonl"), 20000) if e.get("kind") == "hook_ms"
            and e.get("event") == "PreToolUse" and isinstance(e.get("ms"), (int, float))][-SLO_RUNS:]
    if len(runs) < 20:
        return Result("hook SLO", "PASS", f"{len(runs)} PreToolUse run(s) recorded; it judges from 20")
    p95 = _p95([e["ms"] for e in runs])
    if p95 <= slo:
        return Result("hook SLO", "PASS", f"PreToolUse p95 {p95:.0f} ms over the last {len(runs)} runs (SLO {slo} ms)")
    by = {}
    for e in runs:  # first-seen order
        by.setdefault(str(e.get("rev") or "?"), []).append(e["ms"])
    revs = [(r, _p95(ms)) for r, ms in by.items()]
    rose = next(((cur, prev) for prev, cur in zip(revs, revs[1:]) if prev[1] <= slo < cur[1]), None)
    where = (f"it rose at {rose[0][0]} (p95 {rose[0][1]:.0f} ms; {rose[1][0]} before it: {rose[1][1]:.0f} ms)" if rose
             else f"over since {revs[0][0]} at least (the oldest revision in the window)")
    return Result("hook SLO", "WARN", f"PreToolUse p95 {p95:.0f} ms over the last {len(runs)} runs > the {slo} ms SLO "
                                      f"(bench_hooks' budget); {where}")


def check_hook_exit_codes(bench):
    bad = [f"{k}: {v['exit_codes']} (expected {EXPECTED_EXIT.get(k, [0])})" for k, v in bench.items()
           if v["exit_codes"] != EXPECTED_EXIT.get(k, [0])]
    return Result("hook exit codes", "FAIL" if bad else "PASS", "; ".join(bad) or "guard blocks the block fixture; others exit 0")


def check_injection_budgets(sizes):
    bad = []
    if sizes.get("SessionStart", 0) > CTX_BUDGET:
        bad.append(f"SessionStart {sizes['SessionStart']} > {CTX_BUDGET} chars")
    if sizes.get("UserPromptSubmit", 0) > PROMPT_BUDGET:
        bad.append(f"UserPromptSubmit {sizes['UserPromptSubmit']} > {PROMPT_BUDGET} chars")
    return Result("injection budgets", "FAIL" if bad else "PASS", "; ".join(bad) or
                  f"SessionStart {sizes.get('SessionStart', 0)} chars, UserPromptSubmit {sizes.get('UserPromptSubmit', 0)} chars")


def check_footprint(rules_path, claude_md_path, plugin=PLUGIN):
    rules = (_read(rules_path) or "").splitlines()
    md = _read(claude_md_path) or ""
    m = re.search(r"<!-- foreman:begin -->.*?<!-- foreman:end -->", md, re.S)
    block = m.group(0).splitlines() if m else []
    total = len(rules) + len(block)
    bad = []
    if len(rules) > RULES_MAX:
        bad.append(f"rules {len(rules)} lines > {RULES_MAX}")
    chars = sum(len(l) + 1 for l in rules)
    if chars > RULES_CHARS_MAX:
        bad.append(f"rules {chars} chars > {RULES_CHARS_MAX}")
    if len(block) > BLOCK_MAX:
        bad.append(f"CLAUDE.md block {len(block)} lines > {BLOCK_MAX}")
    if total > ALWAYS_ON_MAX:
        bad.append(f"always-on {total} lines > {ALWAYS_ON_MAX}")
    # skill, agent and command descriptions are in every session's context too
    desc = sum(len((_frontmatter(f) or {}).get("description", "")) for pattern in
               ("skills/*/SKILL.md", "agents/*.md", "commands/*.md") for f in glob.glob(os.path.join(plugin, pattern)))
    if desc > DESCRIPTIONS_MAX:
        bad.append(f"skill/agent/command descriptions {desc} chars > {DESCRIPTIONS_MAX}")
    bad += [f"{os.path.relpath(f, plugin)} {n} chars > {SKILL_MAX}" for f in glob.glob(os.path.join(plugin, "skills/*/SKILL.md"))
            if (n := len(_read(f) or "")) > SKILL_MAX]
    return Result("footprint", "FAIL" if bad else "PASS",
                  "; ".join(bad) or f"rules {len(rules)} + CLAUDE.md block {len(block)} = {total} always-on lines "
                                    f"(≤ {ALWAYS_ON_MAX}), rules {chars} chars (≤ {RULES_CHARS_MAX}); descriptions {desc} chars (≤ {DESCRIPTIONS_MAX})")


STATE_BUDGET = 200 * 1024 * 1024  # T-0920: bytes of state per project before doctor speaks up (the largest here: ~55 MB)


def check_state_size(projects, budget=STATE_BUDGET):
    """T-0920: a project's state past the budget, with its largest top-level part; fm tidy prunes and rolls."""
    over = []
    for p in projects:
        parts = {}
        for root, _, names in os.walk(p.dir):
            top = os.path.relpath(root, p.dir).split(os.sep)[0]
            for n in names:
                try:
                    size = os.path.getsize(os.path.join(root, n))
                except OSError:
                    continue
                if top == "backups":  # tidy's own copies: counting them would warn about the fix
                    continue
                key = n if top == "." else top
                parts[key] = parts.get(key, 0) + size
        total = sum(parts.values())
        if total > budget:
            big = max(parts, key=parts.get)
            over.append(f"{p.slug} {total // 2**20} MB (most in {big}: {parts[big] // 2**20} MB)")
    return Result("state size", "WARN" if over else "PASS",
                  f"{'; '.join(over)} > {budget // 2**20} MB: fm tidy --apply prunes and rolls it" if over
                  else f"{len(projects)} project(s) under {budget // 2**20} MB each")


def _frontmatter(path):
    if not os.path.isfile(path):  # T-1434: a FIFO would block the open forever, a device never end
        return None
    m = re.match(r"^---\n(.*?)\n---\n", _read(path) or "", re.S)
    if not m:
        return None
    meta = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        if k.strip():
            meta[k.strip()] = v.strip()
    return meta


def _description_problems(skills):
    """T-1698: the model sees only each model-invocable skill's name and description; flag Foreman jargon in place of
    task words, and two descriptions sharing over 60% of the shorter one's words."""
    words, bad = {}, []
    for name in sorted(os.listdir(skills)) if os.path.isdir(skills) else []:
        meta = _frontmatter(os.path.join(skills, name, "SKILL.md")) or {}
        desc = meta.get("description", "")
        if not desc or meta.get("disable-model-invocation") == "true":
            continue
        if jargon := sorted(set(re.findall(r"\b(?:STATE|STATUS|RESUME|briefs?)\b", desc))):
            bad.append(f"skill {name}: Foreman jargon in the description ({', '.join(jargon)}); say what the person is doing")
        words[name] = set(re.findall(r"[a-z]{3,}", desc.lower()))
    names = sorted(words)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            shared = len(words[a] & words[b]) / (min(len(words[a]), len(words[b])) or 1)
            if shared > 0.6:
                bad.append(f"skills {a}/{b}: descriptions overlap {shared:.0%} of their words")
    return bad


def check_frontmatter(plugin=PLUGIN):
    bad = []
    skills = os.path.join(plugin, "skills")
    for name in sorted(os.listdir(skills)) if os.path.isdir(skills) else []:
        if not os.path.isdir(os.path.join(skills, name)):
            continue  # a skill is a folder; skills/routing.json (T-0252) is data
        meta = _frontmatter(os.path.join(skills, name, "SKILL.md"))
        if meta is None or not meta.get("name") or not meta.get("description"):
            bad.append(f"skill {name}: missing frontmatter name/description")
            continue
        import fmplugins  # T-1396: the Agent Skills spec, as fm lib's source indexer checks it
        why = fmplugins.spec_problems(fmplugins._frontmatter(os.path.join(skills, name, "SKILL.md")), name)
        if why:
            bad.append(f"skill {name}: {'; '.join(why)}")
    bad += _description_problems(skills)
    agents = os.path.join(plugin, "agents")
    for f in sorted(os.listdir(agents)) if os.path.isdir(agents) else []:
        meta = _frontmatter(os.path.join(agents, f))
        if meta is None or not meta.get("name") or not meta.get("description"):
            bad.append(f"agent {f}: missing frontmatter")
            continue
        tools = {t.strip() for t in meta.get("tools", "").strip("[]").split(",") if t.strip()}
        if not tools:  # Claude Code: an omitted or empty tools list inherits every tool
            bad.append(f"agent {f}: not read-only (empty or missing tools list = every tool)")
        elif tools - READ_ONLY_TOOLS - EDITING_AGENTS.get(f, set()):
            bad.append(f"agent {f}: not read-only ({', '.join(sorted(tools - READ_ONLY_TOOLS - EDITING_AGENTS.get(f, set())))})")
        # T-0768: Claude Code ignores a value it doesn't know, so a typo silently undoes the saving
        for key, ok in (("effort", {"low", "medium", "high", "xhigh", "max"}.__contains__),
                        ("maxTurns", lambda v: v.isascii() and v.isdigit() and int(v) > 0),
                        ("omitClaudeMd", {"true", "false"}.__contains__),
                        ("autoCompactWindow", lambda v: v.isascii() and v.isdigit() and int(v) > 0)):  # "²".isdigit()
            if key in meta and not ok(meta[key]):
                bad.append(f"agent {f}: {key}: {meta[key]!r} isn't a value Claude Code knows")
    return Result("frontmatter", "FAIL" if bad else "PASS", "; ".join(bad) or "skills and read-only agents valid")


UNLOADED_SESSIONS = 5  # T-1703: sessions that named a skill, none loading it, before doctor says so
IDLE_NAMED = {"next"}  # the idle Next line names /foreman:next every turn, so every session names it


def check_unloaded_skills(events=None, plugin=PLUGIN, n=UNLOADED_SESSIONS):
    """T-1703: a model-invocable skill named in more than `n` sessions in 30 days and loaded in none is mis-described
    or not needed. Counts like fm usage (fmcost.note_skill), per session so a chatty one counts once. WARN only."""
    import collections
    import fmcost
    skills = os.path.join(plugin, "skills")
    names = sorted(s for s in os.listdir(skills) if os.path.isfile(os.path.join(skills, s, "SKILL.md"))) \
        if os.path.isdir(skills) else []
    if events is None:
        events = c.global_events(fmcost._since(30))
    named, loaded = collections.defaultdict(set), collections.defaultdict(set)
    for e in events:
        if e.get("kind") in ("skill_named", "slash"):
            fmcost.note_skill(e, names, named, loaded)
        elif e.get("kind") == "tool" and e.get("tool") == "Skill":
            loaded[e.get("session_id")].add(str(e.get("target") or "").split(":")[-1])
    ever = set().union(*loaded.values()) if loaded else set()
    missed = collections.Counter(s for ns in named.values() for s in ns)
    bad = [f"{s} ×{k}" for s, k in missed.most_common() if k > n and s not in ever and s not in IDLE_NAMED
           and (_frontmatter(os.path.join(skills, s, "SKILL.md")) or {}).get("disable-model-invocation") != "true"]
    return Result("unloaded skills", "WARN" if bad else "PASS",
                  f"named in sessions, never loaded in 30 days: {', '.join(bad)}; reword the description or retire it"
                  if bad else "no model-invocable skill is named often and never loaded")


def _strip_generated(text):
    return re.sub(r"(?m)^_Generated .*_$", "", text or "")


def check_briefs(p):
    errors = []
    briefs = c.load_briefs(p, errors=errors)
    if errors:
        return Result("briefs", "FAIL", f"{p.slug}: unparseable " + ", ".join(os.path.basename(e[0]) for e in errors))
    if (c.read_meta(p).get("schema") or 0) > c.STATE_SCHEMA:
        return Result("briefs", "FAIL", f"{p.slug}: state written by a newer Foreman (schema "
                                        f"{c.read_meta(p)['schema']} > {c.STATE_SCHEMA}); update this install")
    current = _read(os.path.join(p.dir, "STATE.md"))
    expected = c.render_state(c.state_dict(p, briefs))
    if current is not None and _strip_generated(current) != _strip_generated(expected):
        return Result("briefs", "WARN", f"{p.slug}: STATE.md differs from the briefs (fm tidy --apply regenerates it)")
    return Result("briefs", "PASS", f"{p.slug}: {len(briefs)} brief(s) parse; STATE matches")


def check_file_map(home, master_path):
    text = _read(master_path)
    if text is None:
        return Result("file map", "FAIL", f"{master_path} missing")
    m = re.search(r"(?ms)^##[^\n]*File map[^\n]*\n(.*?)(?=^## |\Z)", text)
    if not m:
        return Result("file map", "FAIL", "MASTER.md has no 'File map' section")
    listed, missing = [], []
    for row in m.group(1).splitlines():
        if not row.lstrip().startswith("|"):
            continue
        cells = row.split("|")
        for path in re.findall(r"`([^`]+)`", cells[1] if len(cells) > 1 else ""):
            listed.append(path)
            if "runtime" in row.lower() or any(ch in path for ch in "*<>"):
                continue
            full = os.path.expanduser(path) if path.startswith("~") else os.path.join(home, path)
            if not os.path.exists(full.rstrip("/")):
                missing.append(path)
    uncovered = []
    plugin_dir = os.path.join(home, "plugin")
    if os.path.isdir(plugin_dir):
        for entry in sorted(os.listdir(plugin_dir)):
            if entry == "__pycache__" or (entry.startswith(".") and entry != ".claude-plugin"):
                continue
            if not any(p.rstrip("/") == "plugin" or p.startswith(f"plugin/{entry}") for p in listed):
                uncovered.append(f"plugin/{entry}")
    bad = [f"listed but missing: {', '.join(missing)}"] if missing else []
    bad += [f"on disk but not in the map: {', '.join(uncovered)}"] if uncovered else []
    return Result("file map", "FAIL" if bad else "PASS", "; ".join(bad) or f"{len(listed)} entries match disk")


def check_backup(home):
    """T-0574: the newest backups/*.tgz is read through to its end, as a restore would (gzip checks its CRC there);
    nothing is written."""
    import tarfile
    d = os.path.join(home, "backups")
    tgz = sorted(f for f in os.listdir(d) if f.endswith(".tgz")) if os.path.isdir(d) else []
    if not tgz:
        return Result("backup", "WARN", "no backups/*.tgz yet")  # T-0844: a fresh install has none: not a failure
    files = 0
    try:  # ponytail: reads every member's bytes, never extracts; a real extract into a temp dir if this misses one
        with tarfile.open(os.path.join(d, tgz[-1]), "r:gz") as t:
            for m in t:
                if m.isfile():
                    files += 1
                    f = t.extractfile(m)
                    while f and f.read(1 << 20):
                        pass
    except (OSError, EOFError, tarfile.TarError, ValueError) as e:
        return Result("backup", "FAIL", f"the newest backup {tgz[-1]} doesn't restore: {c.fit(str(e), 120)}")
    return Result("backup", "PASS", f"latest {tgz[-1]}: restore rehearsal read {files} files")


def check_validate(home):
    bad = []
    for target in (home, os.path.join(home, "plugin")):
        r = _run(["claude", "plugin", "validate", "--strict", target])
        if r.returncode != 0:
            tail = (r.stdout + r.stderr).strip().splitlines()[-1:] or ["failed"]
            bad.append(f"{target}: {tail[0]}")
    return Result("plugin validate", "FAIL" if bad else "PASS", "; ".join(bad) or "marketplace and plugin pass --strict")


# repo-relative protected core, for comparing with git; the guard's own list (fmguard._is_core, _protected_roots) also
# covers paths outside the repo (settings, ~/.claude.json, state): change both together
CORE_PATHS = ("plugin/lib", "plugin/bin", "plugin/hooks", "plugin/evals", "plugin/rules/foreman.md", "BUILD_PROMPT.md")


def check_core_integrity(home):
    """Protected core that differs from the last commit: a half-applied edit, or a change nobody reviewed."""
    if not os.path.exists(os.path.join(home, ".git")):  # a worktree's .git is a file
        return Result("core integrity", "PASS", "not a git checkout: nothing to compare")
    out = _run(["git", "-C", home, "status", "--porcelain", "--", *CORE_PATHS]).stdout
    changed = [l[3:] for l in out.splitlines() if len(l) > 3]
    return Result("core integrity", "WARN" if changed else "PASS",
                  f"protected core differs from the last commit: {', '.join(changed[:6])}"
                  + (f" (+{len(changed) - 6} more)" if len(changed) > 6 else "")
                  + " — commit it through a task, or git checkout it back" if changed
                  else "protected core matches the last commit")


def check_git_hygiene(repo):
    tracked = _run(["git", "-C", repo, "ls-files", "-ci", "--exclude-standard"]).stdout.split()
    # T-0382: --no-renames, or a staged rename that also adds a secret (R, not A or M) is never scanned
    staged = [f for f in _run(["git", "-C", repo, "diff", "--cached", "--name-only", "--no-renames", "--diff-filter=AM",
                               "-z"]).stdout.split("\0") if f]
    secrets = [p for p in staged if (lambda t: c.redact(t) != t)(_run(["git", "-C", repo, "show", f":{p}"]).stdout)]
    bad = [f"ignored but tracked: {', '.join(tracked)}"] if tracked else []
    bad += [f"secret-like content staged in: {', '.join(secrets)}"] if secrets else []
    return Result("git hygiene", "FAIL" if bad else "PASS", "; ".join(bad) or "nothing ignored is tracked; no secrets staged")


def check_statusline(settings, manifest, wrapper):
    if manifest is None:
        return Result("statusline", "WARN", "Foreman not wired into ~/.claude (fm install-user)")
    cmd = ((settings or {}).get("statusLine") or {}).get("command")
    if cmd == wrapper and "statusLine_original" in manifest:
        orig = (manifest.get("statusLine_original") or {}).get("command")
        return Result("statusline", "PASS", f"Foreman wrapper in place; original preserved ({orig or 'none'})")
    return Result("statusline", "FAIL", f"statusLine is {cmd!r}, not the Foreman wrapper recorded at install")


def check_deny_rules(settings, manifest):
    if not manifest:
        return Result("deny rules", "WARN", "not wired")
    deny = set(((settings or {}).get("permissions") or {}).get("deny") or [])
    missing = [r for r in manifest.get("deny_added", []) if r not in deny]
    return Result("deny rules", "FAIL" if missing else "PASS",
                  f"missing: {', '.join(missing)}" if missing else f"{len(manifest.get('deny_added', []))} Foreman deny rules present")


def check_rules_symlink(plugin=PLUGIN):
    link = os.path.join(os.path.expanduser("~"), ".claude", "rules", "foreman.md")
    target = os.path.join(plugin, "rules", "foreman.md")
    if not os.path.lexists(link):
        return Result("rules symlink", "WARN", f"{link} missing (fm install-user)")
    ok = os.path.realpath(link) == os.path.realpath(target)
    return Result("rules symlink", "PASS" if ok else "FAIL", f"{link} → {os.path.realpath(link)}")


def _login_fm(shell=None):
    """T-1333: the fm a fresh login shell finds (only its profile's PATH, as a new terminal has): its path, '' when it
    finds none, None when no login shell could be asked."""
    shell = shell or os.environ.get("SHELL") or "/bin/sh"
    env = {"HOME": os.path.expanduser("~"), "PATH": "/usr/bin:/bin", "USER": os.environ.get("USER", ""), "TERM": "dumb"}
    try:
        r = subprocess.run([shell, "-lc", "command -v fm"], env=env, capture_output=True, text=True, timeout=5,
                           stdin=subprocess.DEVNULL)
    except (OSError, subprocess.SubprocessError):
        return None
    if r.returncode not in (0, 1):
        return None
    found = [ln.strip() for ln in r.stdout.splitlines() if ln.strip().startswith("/")]  # a profile may print first
    return found[-1] if r.returncode == 0 and found else ""


def _profile_fix(shell):
    name = os.path.basename(shell or "")
    if name == "fish":
        return "run fish_add_path ~/.local/bin, then open a new terminal"
    where = {"bash": "~/.bash_profile (or ~/.profile when there's none)", "zsh": "~/.zprofile"}.get(name, "~/.profile")
    return f'add export PATH="$HOME/.local/bin:$PATH" to {where}, then open a new terminal'


def check_fm_link(link=None, target=None, path=None, shell=None):
    """T-1324: fm in any shell (T-0853): ~/.local/bin/fm points at this Foreman's plugin/bin/fm, and a new login shell
    finds it (T-1333: FAIL with the profile line when it doesn't; shell False, or no shell to ask: this process's PATH).
    An install from before T-0853 never made the link, so fm worked only inside Claude Code; session start makes it now."""
    link = link or os.path.join(os.path.expanduser("~"), ".local", "bin", "fm")
    target = target or os.path.join(PLUGIN, "bin", "fm")
    path = os.environ.get("PATH", "") if path is None else path
    if not os.path.lexists(link):
        return Result("fm link", "WARN", f"{link} is missing, so fm works only inside Claude Code: the next session "
                                         "start makes it, or fm install-user")
    if os.path.realpath(link) != os.path.realpath(target):
        return Result("fm link", "WARN", f"{link} → {os.path.realpath(link)}, not this Foreman's {target}: move it "
                                         "aside and run fm install-user")
    found = None if shell is False else _login_fm(shell)
    if found is not None:
        if found and os.path.realpath(found) == os.path.realpath(target):
            return Result("fm link", "PASS", f"{link} → {target}; a new login shell finds it")
        return Result("fm link", "FAIL", (f"a new login shell finds {found} first, not {link}" if found else
                                          "a new login shell doesn't find fm")
                      + f": {_profile_fix(shell or os.environ.get('SHELL'))}")
    if os.path.dirname(link) not in path.split(os.pathsep):
        return Result("fm link", "WARN", f"{os.path.dirname(link)} isn't on PATH, so a shell doesn't find fm: add it "
                                         "in your shell's profile")
    return Result("fm link", "PASS", f"{link} → {target}")


def _version(root):
    return (_load_json(os.path.join(root, ".claude-plugin", "plugin.json")) or {}).get("version") or "?"


def check_dual_install(home=None, known=None, installed=None):
    """T-0923: Foreman installed from a marketplace that isn't this home (GitHub, another folder) beside install.sh's
    copy here: sessions run whichever they started with, and the two drift apart. Different versions warn."""
    home = home or c.foreman_home()
    entry = next(iter(((_load_json(installed or os.path.expanduser("~/.claude/plugins/installed_plugins.json")) or {})
                       .get("plugins") or {}).get("foreman@foreman") or []), None)
    if not entry or not os.path.isdir(os.path.join(home, "plugin")):
        return Result("installs", "PASS", "one Foreman install")
    src = ((_load_json(known or os.path.expanduser("~/.claude/plugins/known_marketplaces.json")) or {})
           .get("foreman") or {}).get("source") or {}
    if src.get("source") == "directory" and os.path.realpath(src.get("path") or "") == os.path.realpath(home):
        return Result("installs", "PASS", f"the foreman marketplace is this home ({home})")
    there = entry.get("version") or _version(entry.get("installPath") or "")
    here = _version(os.path.join(home, "plugin"))
    where = src.get("repo") or src.get("url") or src.get("path") or "another marketplace"
    if there == here:
        return Result("installs", "PASS", f"two Foreman installs at {here}: {where} and {home}")
    return Result("installs", "WARN", f"two Foreman installs: {there} from {where} and {here} in {home}; a session runs "
                  "whichever it started with. Keep one: claude plugin update foreman@foreman (or uninstall it and keep "
                  "this home's)")


def check_product(p):
    """T-0417: a project that ships a web UI has a product check (fm smoke), so a UI that doesn't load can't pass."""
    if not p or not c.git_root(p.root):
        return Result("product check", "PASS", "not in a project")
    import fmmission
    import fmsmoke
    why = fmsmoke.nudge(fmmission.surfaces(p.root), c.read_meta(p))
    return Result("product check", "WARN" if why else "PASS", why or "fm smoke set, or no web UI")


def check_running_code(ledger, installed, plugin=PLUGIN):
    """T-0391: the Foreman code this project's last session ran (session_start records its plugin root) against the
    one installed (or this copy, without an install record). A session keeps the folder it started with, so a fix
    copied anywhere else never reaches it (JARVIS ran 1.2.3 from its Folder marketplace while 1.2.4 sat in caches)."""
    root = None
    try:
        with open(ledger, "rb") as f:
            f.seek(max(0, os.path.getsize(ledger) - 2_000_000))
            for line in f.read().decode("utf-8", "replace").splitlines():
                if '"session_start"' in line:
                    try:
                        root = (json.loads(line).get("data") or {}).get("root") or root
                    except ValueError:
                        continue
    except OSError:
        pass
    entry = next(iter(((_load_json(installed) or {}).get("plugins") or {}).get("foreman@foreman") or []), None)
    num = lambda v: tuple(int(x) for x in re.findall(r"\d+", v)[:3])  # noqa: E731
    # the newest Foreman here: the installed copy or this one (a dev checkout runs ahead of its install record)
    want_root = max(filter(None, [(entry or {}).get("installPath"), plugin]), key=lambda r: num(_version(r)))
    want = _version(want_root)
    if not root:
        return Result("running code", "PASS", f"newest Foreman here {want} ({want_root}); no session recorded its root yet")
    ran = _version(root)
    if num(ran) < num(want):
        return Result("running code", "WARN", f"the last session ran Foreman {ran} from {root}, but {want} is at "
                                              f"{want_root}: restart that session, or put the fix in {root}")
    return Result("running code", "PASS", f"sessions run Foreman {ran} from {root}")


def check_version_skew(projects, changes=None):
    """T-0463: projects whose last session ran a Foreman older than released fixes, with the task ids they lack."""
    import fmeco
    changes = fmeco.changelog() if changes is None else changes
    behind = []
    for p, meta in projects:
        ran = (meta.get("foreman") or {}).get("version")
        lacks = fmeco.lacks(ran, changes)
        if lacks:
            behind.append(f"{p.slug} ran {ran}, lacks {len(lacks)} ({', '.join(lacks[:4])}{' …' if len(lacks) > 4 else ''})")
    return Result("version skew", "WARN" if behind else "PASS",
                  "; ".join(behind[:6]) + " — restart their sessions on the new Foreman" if behind else
                  "every project's last session ran the newest released Foreman (or none recorded one yet)")


def check_python(v=sys.version_info[:3], refresh=None, child=False):
    """T-0319: fm and every hook start on the python3 on PATH. Before 3.12.7 (and in 3.13.0) argparse drops
    `fm task evidence ID --ac N CMD RESULT`; install.sh installs a newer one, and T-0368 re-runs Foreman under a
    supported one it finds (`child`: this run already is one; `refresh`: search again and save the answer)."""
    have = ".".join(map(str, v))
    if fmpy.ok(v):
        return Result("python", "WARN" if child else "PASS",
                      f"python3 on PATH is below 3.12.7; Foreman runs under {sys.executable} ({have})" if child
                      else f"python3 {have}")
    exe = refresh() if refresh else None
    if exe:
        return Result("python", "WARN", f"python3 is {have}, below 3.12.7; Foreman now runs under {exe}")
    return Result("python", "FAIL", f"python3 is {have}; Foreman needs 3.12.7+ (rerun install.sh to install one)")


# T-0785: (feature, minimum Claude Code, globs under plugin/, regex showing it is used); a feature no file uses isn't checked
CC_FEATURES = [
    ("hook onFailure", (2, 1, 295), ["hooks/*.json"], r'"onFailure"'),
    ("agent omitClaudeMd", (2, 1, 271), ["agents/*.md"], r"(?m)^omitClaudeMd:"),
    # read from 2.1.296, but below Foreman's CLAUDE_CODE_AUTO_COMPACT_WINDOW (T-1796) it only lowers it from 2.1.312
    ("agent autoCompactWindow", (2, 1, 312), ["agents/*.md"], r"(?m)^autoCompactWindow:"),
    ("agent effort/maxTurns", (2, 1, 78), ["agents/*.md"], r"(?m)^(effort|maxTurns):"),
    ("hook if", (2, 1, 85), ["hooks/*.json"], r'"if"\s*:'),
    ("plugin monitors", (2, 1, 105), ["monitors/monitors.json"], r"."),
    ("PostToolUse updatedToolOutput", (2, 1, 121), ["lib/fmhooks.py"], r"updatedToolOutput"),
    ("UserPromptSubmit sessionTitle", (2, 1, 94), ["lib/fmhooks.py"], r"sessionTitle"),
    ("worktree.baseRef setting", (2, 1, 133), ["lib/fmsetup.py"], r"baseRef"),  # wired into ~/.claude (T-0803)
]


def check_cc_features(version=None, plugin=PLUGIN):
    """T-0785: WARN naming each Foreman feature in use that the installed Claude Code is too old for (it would
    silently do nothing). `version`: stubbed (tuple); default fmhooks._cc_version(); () = unknown, nothing to compare."""
    if version is None:
        import fmhooks
        version = fmhooks._cc_version()
    if not version:
        return Result("claude code features", "PASS", "Claude Code version unknown; not compared")
    old = []
    for name, need, globs, pat in CC_FEATURES:
        if version >= need:
            continue
        for g in globs:
            if any(re.search(pat, open(f, encoding="utf-8", errors="replace").read())
                   for f in glob.glob(os.path.join(plugin, g))):
                old.append(f"{name} (needs {'.'.join(map(str, need))})")
                break
    have = ".".join(map(str, version))
    return Result("claude code features", "WARN" if old else "PASS",
                  f"Claude Code {have} is too old for {', '.join(old)}; upgrade it (claude update)" if old
                  else f"Claude Code {have} supports every Claude Code feature Foreman uses")


def check_scripts(home, full=False):
    bad = []
    for s in SCRIPTS:
        path = os.path.join(home, s)
        if os.path.exists(path) and _run(["bash", "-n", path]).returncode != 0:
            bad.append(f"{s} doesn't parse")
    if os.path.exists(os.path.join(home, "setup-plugins.sh")):
        r = _run([os.path.join(home, "setup-plugins.sh"), "--dry-run"], timeout=180)
        if r.returncode != 0:
            bad.append(f"setup-plugins.sh --dry-run exited {r.returncode}")
    if full and os.path.exists(os.path.join(home, "install.sh")):
        r = _run([os.path.join(home, "install.sh"), "--no-plugins"], timeout=300, env=dict(os.environ, FOREMAN_HOME=home))
        if r.returncode != 0:
            bad.append(f"install.sh --no-plugins exited {r.returncode}: {r.stderr.strip()[-200:]}")
    ok = "scripts parse; setup-plugins --dry-run clean" + ("; install.sh --no-plugins clean" if full else "")
    return Result("scripts", "FAIL" if bad else "PASS", "; ".join(bad) or ok)


def _enabled_plugin_paths(settings):
    installed = _load_json(os.path.join(os.path.expanduser("~"), ".claude", "plugins", "installed_plugins.json")) or {}
    enabled = {k for k, v in ((settings or {}).get("enabledPlugins") or {}).items() if v}
    out = {}
    for pid, entries in (installed.get("plugins") or {}).items():
        if pid in enabled and not pid.startswith("foreman@"):
            for e in entries if isinstance(entries, list) else [entries]:
                if isinstance(e, dict) and e.get("installPath"):
                    out[pid] = e["installPath"]
    return out


def check_name_collisions(settings, plugin=PLUGIN):
    ours = set(os.listdir(os.path.join(plugin, "skills")))
    clashes = []
    for pid, path in _enabled_plugin_paths(settings).items():
        for sub in ("skills", "commands"):
            d = os.path.join(path, sub)
            if os.path.isdir(d):
                names = {n[:-3] if n.endswith(".md") else n for n in os.listdir(d)}
                clashes += [f"{n} ({pid})" for n in sorted(ours & names)]
    user = os.path.join(os.path.expanduser("~"), ".claude", "skills")
    if os.path.isdir(user):
        clashes += [f"{n} (~/.claude/skills)" for n in sorted(ours & set(os.listdir(user)))]
    return Result("name collisions", "WARN" if clashes else "PASS",
                  ("bare names shared (use /foreman:<name>): " + ", ".join(clashes)) if clashes else "no skill/command name collisions")


def check_hook_writers(settings, home):
    sources = {"user settings": (settings or {}).get("hooks") or {}}
    for pid, path in _enabled_plugin_paths(settings).items():
        sources[pid] = (_load_json(os.path.join(path, "hooks", "hooks.json")) or {}).get("hooks") or {}
    state = os.path.join(home, "state")
    bad = []
    for src, hooks in sources.items():
        for event, groups in hooks.items():
            for g in groups:
                for h in g.get("hooks", []):
                    text = " ".join([h.get("command", "")] + list(h.get("args", [])))
                    if "foreman/state" in text or state in text or "foreman/plugin/hooks/hook" in text:
                        bad.append(f"{src} {event}: {text[:80]}")
    return Result("hook state writers", "FAIL" if bad else "PASS",
                  "; ".join(bad) or "only Foreman's own hooks write Foreman state; no duplicate registrations")


def recent_hook_errors(days=1):
    """Hook errors of the last `days` (24h), each its log lines: "<ts> <event> <traceback…>" and its continuation."""
    log = _read(os.path.join(c.state_dir(), "logs", "hooks.log")) or ""
    entries = []
    for line in log.splitlines():
        if re.match(r"\d{4}-\d\d-\d\dT\S+ ", line):
            entries.append([line])
        elif entries:
            entries[-1].append(line)
    return [e for e in entries if (c.age_days(e[0].split(" ", 1)[0]) or 99) < days]


def _recent_errors(days=7):
    """T-1076: (ts, text) of the last `days`: each hook error and every project's failure signatures (not the
    hinted copy fmrecall adds to a repeat)."""
    out = [(e[0].split(" ", 1)[0], "\n".join(e)) for e in recent_hook_errors(days)]
    for p, _ in c.all_projects():
        out += [(r.get("at"), str(r.get("sig") or "")) for r in c.tail_jsonl(os.path.join(p.dir, "failures.jsonl"), 1000)
                if isinstance(r, dict) and not r.get("hinted") and (c.age_days(r.get("at")) or 99) < days]
    return out


def _cc_installed_at(path=None):
    """When the installed Claude Code arrived: the inode-change time of the file `claude` resolves to (npm pins
    mtimes to 1985; ctime is when it was unpacked); 0 when unknown."""
    # ponytail: a later chmod or restore of the binary moves it too; that only hides older errors, never adds one
    try:
        found = shutil.which("claude", path=path)
        return os.stat(os.path.realpath(found)).st_ctime if found else 0
    except OSError:
        return 0


def _after(ts, since):
    t = c.parse_ts(ts)
    return bool(t) and t.timestamp() >= since


def check_upstream(errors=None, version=None, issues=None, since=None):
    """T-1076: an error seen twice or more in 7 days that matches a known Claude Code issue (lib/upstream-issues.json),
    with the version that fixes it. Stubs: `errors` (ts, text) pairs, `version` tuple (() unknown), `issues` entries,
    `since` when the installed version arrived (epoch; 0 unknown): only later errors can say a fix didn't hold."""
    if errors is None:
        errors = _recent_errors()
    if version is None:
        import fmhooks
        version = fmhooks._cc_version()
    if since is None:
        since = _cc_installed_at()
    if issues is None:
        issues = _load_json(os.path.join(PLUGIN, "lib", "upstream-issues.json"))
        if not isinstance(issues, list):
            return Result("upstream issues", "WARN", "plugin/lib/upstream-issues.json is missing or unreadable")
    found = []
    for i in issues:
        try:  # a bad entry is a finding, never a crashed doctor run
            hits = [ts for ts, text in errors if re.search(i["pattern"], text, re.I)]
            if len(hits) < 2:
                continue
            url, fix = i["issue_url"], i["fixed_in"]
            if not fix:
                found.append(f"matches {url} (seen {len(hits)}×); no fix released yet: {i['note']}")
            elif not version:
                found.append(f"matches {url} (seen {len(hits)}×); fixed in {fix}; installed version unknown "
                             f"(claude --version)")
            elif version < tuple(map(int, fix.split("."))):
                found.append(f"matches {url} (seen {len(hits)}×); fixed in {fix}: claude update")
            elif not since:
                found.append(f"matches {url}, seen {len(hits)}× in 7 days (possibly before an update); should be "
                             f"fixed in {fix} yet recurs")
            elif sum(_after(ts, since) for ts in hits) >= 2:
                found.append(f"matches {url} (seen {sum(_after(ts, since) for ts in hits)}× since this Claude Code "
                             f"was installed); should be fixed in {fix} yet recurs")
        except (KeyError, TypeError, ValueError, AttributeError, re.error) as e:
            name = i.get("id") if isinstance(i, dict) else c.fit(str(i), 40)
            found.append(f"entry {name} in upstream-issues.json is unusable ({type(e).__name__}: {e})")
    return Result("upstream issues", "WARN" if found else "PASS", "; ".join(found) or
                  f"no error seen twice in 7 days matches the {len(issues)} known Claude Code issue(s)")


def paused_hooks():
    """T-0087: the events the hook breaker has paused after failing in a row."""
    import fmhooks
    return fmhooks.paused_hooks()


_FRAME = re.compile(r'^\s*File "([^"]+)", line (\d+), in ')


def _stale(err):
    """T-1139: the error's last frame in Foreman's code shows a line the file no longer has there (the code changed
    since: a half-written edit, a bug already fixed)."""
    frames = [(m.group(1), int(m.group(2)), i) for i, ln in enumerate(err) if (m := _FRAME.match(ln))
              and os.path.realpath(m.group(1)).startswith(os.path.realpath(PLUGIN) + os.sep)]
    if not frames:
        return False
    path, n, i = frames[-1]
    shown = err[i + 1].strip() if i + 1 < len(err) else ""
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            now = f.read().splitlines()
    except OSError:
        return True
    return bool(shown) and (n > len(now) or now[n - 1].strip() != shown)


def check_hook_errors():
    errors, paused = recent_hook_errors(), paused_hooks()
    recent = [e for e in errors if not _stale(e)]
    stale = len(errors) - len(recent)
    if paused:
        return Result("hook errors", "FAIL", f"paused: {', '.join(paused)} ({len(recent)} hook error(s) in the last "
                                             f"24h; a paused hook runs again 10 min after its last failure; "
                                             f"state/logs/hooks.log)")
    if not recent:
        return Result("hook errors", "PASS", "no hook errors in the last 24h" + (
            f" ({stale} from code changed since)" if stale else ""))
    last = recent[-1]
    event = c.plain((last[0].split(" ") + ["", ""])[1])  # log text can carry anything an error message quoted
    cause = c.plain(next((l.strip() for l in reversed(last) if l.strip()), ""))
    return Result("hook errors", "WARN", f"{len(recent)} hook error(s) in the last 24h; latest: {event} "
                                         f"{c.fit(cause, 120)} (state/logs/hooks.log)")


# ---------------------------------------------------------------- orchestration

class _NoBench(Exception):
    pass


def _bench_and_injection(runs=5):
    import tempfile
    sys.path.insert(0, os.path.join(PLUGIN, "tests"))
    import bench_hooks
    bench = bench_hooks.run_bench(runs=runs)
    sizes = {}
    with tempfile.TemporaryDirectory() as tmp:
        repo, env = bench_hooks._scratch_project(tmp)
        env["CLAUDE_ENV_FILE"] = os.path.join(tmp, "envfile")
        for event, extra in (("SessionStart", {"source": "startup"}),
                             ("UserPromptSubmit", {"prompt": "FIX: a\nFEATURE!: b\nCLEAN?: c\nCONTEXT: d"})):
            payload = json.dumps(dict({"session_id": "doctor", "cwd": repo, "hook_event_name": event}, **extra))
            out = _run([os.path.join(PLUGIN, "hooks", "hook"), event], input=payload, env=env, cwd=repo).stdout
            try:
                sizes[event] = len(json.loads(out)["hookSpecificOutput"]["additionalContext"])
            except (ValueError, KeyError, TypeError):
                sizes[event] = 0
    return bench, sizes


def _fm_commands():
    """{top-level fm command: {its subcommands}} straight from the parser, so the check can't drift from the code."""
    import argparse
    import fmcli
    out = {}
    for a in fmcli.build_parser()._actions:
        if isinstance(a, argparse._SubParsersAction):
            for name, sp in a.choices.items():
                out[name] = {n for b in sp._actions if isinstance(b, argparse._SubParsersAction) for n in b.choices}
    return out


_FM_MENTION = re.compile(r"(?:^|[\s;|&(])fm\s+([a-z][\w-]*)(?:\s+([a-z][\w-]*))?")


# T-0954: zero-width, bidi and tag characters hide instructions from the person reading the file; a ZWJ between two
# non-ASCII characters is an emoji sequence, not hidden text
_INVISIBLE = re.compile(  # emoji glue (a ZWJ between non-ASCII characters) is fine; a run of it isn't. Variation
    # selectors, VS15/16 included, are hidden wherever they sit, as fmcore.plain has it (T-1687)
    "[\u00ad\u061c\u180e\u200b\u200c\u200e\u200f\u202a-\u202e\u2060-\u2064\u2066-\u2069\ufeff\ufe00-\ufe0f"
    "\U000e0000-\U000e007f\U000e0100-\U000e01ef]"
    "|(?:^|[\x00-\x7f])\u200d|\u200d{2}|\u200d(?:$|[\x00-\x7f])", re.M)


def instruction_files(plugin=PLUGIN):
    """The files Claude reads as instructions: the user's CLAUDE.md, CLAUDE.local.md and rules; Foreman's rules,
    skills (with their references and cards), agents, commands and output styles."""
    claude = os.path.join(os.path.expanduser("~"), ".claude")
    mine = [os.path.join(claude, "CLAUDE.md"), os.path.join(claude, "CLAUDE.local.md")] + glob.glob(
        os.path.join(claude, "rules", "*.md"))
    return mine + sorted(set(glob.glob(os.path.join(plugin, "skills", "**", "*.md"), recursive=True)
                             + [x for d in ("rules", "agents", "commands", "output-styles")
                                for x in glob.glob(os.path.join(plugin, d, "*.md"))]))


# T-1267: (a line that says it, the Foreman rule it contradicts, how to settle it in a line). Each pattern wants the
# whole clause ("never run the tests."), so "don't run tests in parallel" or "don't commit secrets" pass
_END = r"\s*(?:[.;,!:)]|$)"
CONFLICTS = (
    (r"\b(?:never|don'?t|do not) run (?:the |any )?(?:unit |integration )?(?:tests?|test suite|suite)" + _END,
     "a task closes only on a fresh passing run", "name the slow or paid tests to skip instead (fm gates)"),
    (r"\bskip (?:running )?(?:the )?tests" + _END,
     "a task closes only on a fresh passing run", "name the slow or paid tests to skip instead (fm gates)"),
    (r"\b(?:never|don'?t|do not) (?:write|add) (?:any )?(?:unit )?tests?" + _END,
     "a FIX starts with a failing test", "say where tests aren't wanted (scripts, prototypes)"),
    (r"\bcommit (?:after|on) (?:every|each) (?:change|edit|file|step)" + _END,
     "one commit per task, after the gates pass", "commit per task instead"),
    (r"\b(?:never|don'?t|do not) (?:git )?commit(?: anything| changes| yourself| on your own)?" + _END,
     "fm task finish --commit commits a task's own files", "close tasks with fm task done, or allow task commits"),
    (r"\b(?:skip|don'?t|do not|never) (?:the )?plan(?:ning)?" + _END,
     "no edits without a brief", "keep small work tier S: a brief of one line"),
)


def rule_files(root):
    """T-1267: the files whose lines Claude takes as the user's rules: CLAUDE.md, CLAUDE.local.md and rules, the user's
    and the project's, and Claude Code's memory for the project."""
    claude = os.path.join(os.path.expanduser("~"), ".claude")
    files = [os.path.join(claude, "CLAUDE.md"), os.path.join(claude, "CLAUDE.local.md")] + sorted(
        glob.glob(os.path.join(claude, "rules", "*.md")))
    if root:
        files += [os.path.join(root, "CLAUDE.md"), os.path.join(root, "CLAUDE.local.md"),
                  os.path.join(root, ".claude", "CLAUDE.md")] + sorted(glob.glob(os.path.join(root, ".claude", "rules",
                                                                                              "*.md")))
        files += sorted(glob.glob(os.path.join(claude, "projects", re.sub(r"[^A-Za-z0-9]", "-", root), "memory", "*.md")))
    return files


def check_rule_conflicts(paths, plugin=PLUGIN):
    """T-1267: WARN with file:line, Foreman's rule and a fix for each line that contradicts Foreman's rules; Foreman's
    own files, its block in CLAUDE.md, code fences and lines about Foreman itself are left alone."""
    hits, home, mine = [], os.path.expanduser("~"), os.path.realpath(plugin) + os.sep
    for path in dict.fromkeys(paths):
        if os.path.realpath(path).startswith(mine):
            continue
        text = re.sub(r"<!-- foreman:begin -->.*?<!-- foreman:end -->", lambda m: "\n" * m.group(0).count("\n"),
                      _read(path) or "", flags=re.S)
        fence = False
        for n, line in enumerate(text.split("\n"), 1):
            if line.lstrip().startswith("```"):
                fence = not fence
            elif not fence and not re.search(r"\b(?:fm|foreman)\b", line, re.I):
                rule = next(((r, fix) for pat, r, fix in CONFLICTS if re.search(pat, line, re.I)), None)
                if rule:
                    hits.append(f"{path.replace(home, '~', 1)}:{n} \"{c.fit(line.strip(), 70)}\" contradicts Foreman's "
                                f"rule ({rule[0]}): {rule[1]}")
    return Result("rule conflicts", "WARN" if hits else "PASS",
                  ("; ".join(hits[:6]) + (f"; and {len(hits) - 6} more" if len(hits) > 6 else "")) if hits else
                  "no line in CLAUDE.md, rules or memory contradicts Foreman's")


def check_invisible_text(paths):
    """WARN with file:line for each line of an instruction file holding invisible characters."""
    hits = []
    for path in dict.fromkeys(paths):
        text = _read(path) or ""
        for n, line in enumerate((text[1:] if text.startswith("\ufeff") else text).split("\n"), 1):
            if _INVISIBLE.search(line):
                hits.append(f"{path.replace(os.path.expanduser('~'), '~', 1)}:{n}")
    return Result("invisible text", "WARN" if hits else "PASS",
                  ("zero-width, bidi or tag characters (hidden instructions?) at " + ", ".join(hits[:8])
                   + (f" and {len(hits) - 8} more" if len(hits) > 8 else "")) if hits else "instruction files clean")


def check_self_docs(home=None, plugin=PLUGIN):
    """Foreman's own docs vs its code: fm commands named in docs exist, MASTER.md lists every command, skill and
    agent, and README's install flags match install.sh --help."""
    home = home or os.path.dirname(os.path.abspath(plugin))
    cmds, bad = _fm_commands(), []
    master = _read(os.path.join(home, "MASTER.md")) or ""
    docs = [os.path.join(home, f) for f in ("README.md", "MASTER.md")] + [os.path.join(plugin, "rules", "foreman.md")]
    for d, _, files in os.walk(os.path.join(plugin, "skills")):
        if "playbooks" not in d:  # ported third-party procedures don't talk about fm
            docs += [os.path.join(d, f) for f in files if f.endswith(".md")]
    for path in docs:
        raw = _read(path) or ""
        text = re.sub(r"```.*?```", "", raw, flags=re.S)  # fences would shift backtick pairing
        fenced = [ln for block in re.findall(r"```[^\n]*\n(.*?)```", raw, flags=re.S)  # T-0954: usage examples
                  for ln in block.splitlines() if re.match(r"\s*(?:\$\s+)?fm\s", ln)]
        for span in re.findall(r"`([^`\n]+)`", text) + fenced:
            for m in _FM_MENTION.finditer(span):
                top, sub = m.group(1), m.group(2)
                if top not in cmds:
                    bad.append(f"{os.path.relpath(path, home)}: `fm {top}` isn't an fm command")
                elif cmds[top] and sub and sub not in cmds[top]:
                    bad.append(f"{os.path.relpath(path, home)}: `fm {top} {sub}` isn't an fm command")
    listed = {w for span in re.findall(r"`(fm [^`\n]+)`", re.sub(r"```.*?```", "", master, flags=re.S))
              for w in re.split(r"[\s|\[\]]+", span)}  # only names inside `fm …` spans count
    missing = [n for n in sorted(cmds) if n not in listed]
    if missing:
        bad.append("MASTER.md lacks fm " + ", ".join(missing))
    import fmcli  # T-1011: fm help's tiers name every command once (a new verb with none passed every check but the suite)
    tiered = [w for _, names in fmcli.HELP_TIERS for w in names.split()]
    if [n for n in sorted(cmds) if n not in tiered]:
        bad.append("fm help's tiers lack " + ", ".join(n for n in sorted(cmds) if n not in tiered))
    bad += [f"fm help's tiers list {n} twice" for n in sorted({w for w in tiered if tiered.count(w) > 1})]
    bad += [f"fm help's tiers: {n} isn't an fm command" for n in sorted(set(tiered) - set(cmds))]
    for kind, folder, strip in (("skill", "skills", ""), ("agent", "agents", ".md")):
        for name in sorted(os.listdir(os.path.join(plugin, folder))) if os.path.isdir(os.path.join(plugin, folder)) else []:
            name = name[:-len(strip)] if strip and name.endswith(strip) else name
            if name not in master:
                bad.append(f"MASTER.md doesn't mention the {kind} {name}")
    bad += [f"MASTER.md doesn't name the module {m}" for m in missing_modules(home, master)]  # T-0491
    readme, install = _read(os.path.join(home, "README.md")) or "", _read(os.path.join(home, "install.sh")) or ""
    header = "\n".join(l for l in install.splitlines()[:20] if l.startswith("#"))  # the --help text
    help_flags = set(re.findall(r"(--[\w-]+)", header))
    readme_flags, in_flags = set(), False  # T-0902: a "Flags:" line, or a **Flags:** heading and the bullets under it
    for line in readme.splitlines():
        if re.match(r"\**Flags:", line.strip()):
            in_flags = True
        elif line.strip() and not line.lstrip().startswith("- "):
            in_flags = False
        if in_flags:
            readme_flags |= set(re.findall(r"`(--[\w-]+)`", line))
    bad += [f"README.md doesn't document install.sh {f}" for f in sorted(help_flags - readme_flags)]
    bad += [f"README.md lists {f}, which install.sh doesn't have" for f in sorted(readme_flags - help_flags)]
    bad = list(dict.fromkeys(bad))
    return Result("self docs", "FAIL" if bad else "PASS", "; ".join(bad[:12]) + (f" (+{len(bad) - 12} more)" if len(bad) > 12
                                                                                  else "") if bad else "docs match the code")


def missing_modules(home, master=None):
    """T-0491: plugin/lib/fm*.py modules MASTER.md never names, so its module map keeps up with the code."""
    master = master if master is not None else (_read(os.path.join(home, "MASTER.md")) or "")
    lib = os.path.join(home, "plugin", "lib")
    names = sorted(f[:-3] for f in (os.listdir(lib) if os.path.isdir(lib) else []) if re.fullmatch(r"fm\w+\.py", f))
    return [n for n in names if not re.search(rf"\b{n}\b", master)]


def check_state_dir(home, state):
    default = os.path.join(home, "state")
    if state == default:
        return Result("state dir", "PASS", state)
    if os.environ.get("FOREMAN_STATE"):
        return Result("state dir", "WARN", f"FOREMAN_STATE is set: state is in {state}, not {default}")
    tmp = " It's under the temp dir, so a reboot can clear it." if state.startswith(tempfile.gettempdir()) else ""
    return Result("state dir", "WARN", f"fallback in use: {state} ({default} wasn't writable; the marker in it keeps "
                  f"every process there).{tmp} fm doctor --restore-state moves it back once {default} is writable")


def _fs_type(path):
    """The filesystem type path is on, from /proc/mounts (longest mount point that holds it); 'unknown' elsewhere."""
    path, best = os.path.realpath(path), ("", "unknown")
    try:
        with open("/proc/mounts") as f:
            for line in f:
                parts = line.split()
                mnt = parts[1].replace("\\040", " ") if len(parts) > 2 else ""
                if (path == mnt or path.startswith(mnt.rstrip("/") + "/")) and len(mnt) >= len(best[0]):
                    best = (mnt, parts[2])
    except OSError:
        pass
    return best[1]


def check_lock_probe(state):
    """T-1405: every Foreman lock is an flock under state/; on a filesystem where flock doesn't exclude (NFS, some FUSE)
    they all silently protect nothing. A child holds an flock on a probe file; this process's LOCK_NB must be refused.
    That proves exclusion between processes on this host only, not across hosts sharing the filesystem."""
    try:
        import fcntl
        import select
    except ImportError:
        return Result("lock probe", "WARN", "no flock on this platform: not probed")
    probe = os.path.join(state, f".lock-probe-{os.getpid()}")
    held = ("import fcntl, sys\nf = open(sys.argv[1], 'a')\nfcntl.flock(f, fcntl.LOCK_EX)\nprint('held', flush=True)\n"
            "sys.stdin.read()\n")
    try:
        os.makedirs(state, exist_ok=True)
    except OSError as e:
        return Result("lock probe", "WARN", f"not probed: {e}")
    try:
        child = subprocess.Popen([sys.executable, "-c", held, probe], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=subprocess.DEVNULL, text=True)
    except OSError as e:
        return Result("lock probe", "WARN", f"couldn't start the probe child: {e}; not probed")
    try:
        if not select.select([child.stdout], [], [], 10)[0]:
            return Result("lock probe", "WARN", f"the probe child didn't take its lock in {state} within 10 s "
                          "(flock may hang there); not probed")
        if child.stdout.readline().strip() != "held":
            return Result("lock probe", "WARN", f"couldn't start the probe child (it ended before taking its lock in "
                          f"{state}); not probed")
        fs = _fs_type(state)
        with open(probe, "a") as f:
            try:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                return Result("lock probe", "PASS", f"flock excludes between processes on this host in {state} ({fs})")
            return Result("lock probe", "FAIL", f"a second process here took an flock the probe child held on {state} "
                          f"({fs} filesystem): Foreman's locks may protect nothing there; move state to a local disk "
                          "(FOREMAN_STATE)")
    finally:
        child.stdin.close()
        try:
            child.wait(timeout=10)
        except subprocess.TimeoutExpired:
            child.kill()
            child.wait()
        child.stdout.close()
        try:
            os.remove(probe)
        except OSError:
            pass


def check_hook_events(registered=None):
    """Every event fmhooks handles is registered in hooks.json (a new hook needs /reload-plugins to take effect)."""
    import fmhooks
    if registered is None:  # an event's name, or the handler an entry names in its args (T-0947: PostToolUseValidate)
        hooks = _load_json(os.path.join(PLUGIN, "hooks", "hooks.json")).get("hooks") or {}
        registered = set(hooks) | {(h.get("args") or [None])[0] for gs in hooks.values() for g in gs
                                   for h in g.get("hooks") or []} - {None}
    missing = sorted((set(fmhooks.HANDLERS) | {"PreToolUse"}) - set(registered))
    if missing:
        return Result("hook events", "FAIL", "handled but not registered in hooks.json: " + ", ".join(missing))
    return Result("hook events", "PASS", f"{len(registered)} events registered (after changes: /reload-plugins)")


def check_worktree_base(settings):
    """T-0803: Agent isolation worktrees start from worktree.baseRef; the default ('fresh', the remote's default branch)
    makes a builder lane start behind the branch being worked, and the builder stops (T-0379)."""
    ref = ((settings or {}).get("worktree") or {}).get("baseRef") or "fresh"
    if ref == "head":
        return Result("worktree base", "PASS", "builder lanes start from the current HEAD")
    return Result("worktree base", "WARN", f"worktree.baseRef is {ref!r}: builder lanes start from the remote's default "
                                           "branch, not yours (fm install-user sets head)")


def check_plugins():
    import fmplugins
    found = fmplugins.check()
    if found:
        names = sorted({f["plugin"] for f in found})
        return Result("plugins", "WARN", f"{len(found)} conflict(s) in {', '.join(names[:4])}"
                      + (" …" if len(names) > 4 else "") + " (fm plugins check)")
    return Result("plugins", "PASS", "no conflicts among enabled plugins")


LOW_DISK_BYTES = 10e9  # T-1450: below this, or below LOW_DISK_SHARE of the disk, doctor warns
LOW_DISK_SHARE = 0.05


def check_disk(path=None, usage=None, projects=None):
    """T-1450: the disk filled on 2026-10-22 and every hook that wrote state failed (ENOSPC) with no warning first.
    Builder worktrees pile up unseen, so their counts are named (a listdir each; sizing them would be slow)."""
    try:
        u = (usage or shutil.disk_usage)(path or c.state_dir())
    except OSError:
        return Result("disk", "PASS", "not measured")
    free = f"{u.free / 1e9:.0f} GB free ({100 * u.free / u.total:.0f}%)"
    if u.free >= LOW_DISK_BYTES and u.free >= LOW_DISK_SHARE * u.total:
        return Result("disk", "PASS", free)
    lanes = []
    for p, _ in (c.all_projects() if projects is None else projects):
        try:
            n = len(os.listdir(os.path.join(p.root, ".claude", "worktrees")))
        except OSError:
            continue
        if n:
            lanes.append((n, os.path.basename(p.root.rstrip(os.sep))))
    where = ", ".join(f"{name} {n}" for n, name in sorted(lanes, reverse=True)[:5])
    return Result("disk", "WARN", f"{free} on the disk holding Foreman's state: hooks fail when it fills"
                  + (f"; builder worktrees: {where} (git worktree list; fm lane rm the merged ones)" if where else ""))


def check_mod_release(home=None, listing=None):
    """T-0191: every other session draws the installed foreman-ui, which lags this repo until it is released (0.4.0
    stayed installed while the repo reached 0.5.0). Its hooks are compared, so code changed without a version bump
    counts too."""
    import fmplugins
    repo = os.path.join(home or c.foreman_home(), "mods", "foreman-ui")
    entry = ((_load_json(listing or os.path.expanduser("~/.claude/plugins/installed_plugins.json")) or {})
             .get("plugins") or {}).get("foreman-ui@foreman") or [{}]
    inst = entry[0].get("installPath") if isinstance(entry[0], dict) else None
    if not os.path.isdir(os.path.join(repo, "hooks")) or not inst or not os.path.isdir(inst):
        return Result("foreman-ui release", "PASS", "not installed from this repo")
    # T-1451: Claude Code reads a directory marketplace in place, so the cache copy above is a record no session draws
    known = os.path.join(os.path.dirname(listing or os.path.expanduser("~/.claude/plugins/x")), "known_marketplaces.json")
    src = (((_load_json(known) or {}).get("foreman") or {}).get("source") or {})
    if isinstance(src, dict) and src.get("source") == "directory" and isinstance(src.get("path"), str) and \
            os.path.realpath(src["path"]) == os.path.realpath(home or c.foreman_home()):
        return Result("foreman-ui release", "PASS", "read in place from this checkout (a directory marketplace)")
    have = entry[0].get("version") or "?"
    want = (_load_json(os.path.join(repo, ".claude-plugin", "plugin.json")) or {}).get("version") or "?"
    if fmplugins._tree_hash(os.path.join(repo, "hooks")) == fmplugins._tree_hash(os.path.join(inst, "hooks")):
        return Result("foreman-ui release", "PASS", f"the installed foreman-ui ({have}) matches this repo")
    return Result("foreman-ui release", "WARN", f"the installed foreman-ui is {have}, this repo's is {want}"
                  + (" with newer code" if have == want else "") + ": other sessions draw the old UI until it is "
                  "released (bump its version, then a plugin yes to update it)")


def check_serve(states):
    """fm serve units that aren't running (a dead one leaves its project in full autonomy with drive on)."""
    down = [f"{slug} {state}" for slug, state in states.items() if state != "active"]
    if down:
        return Result("fm serve", "WARN", "not running: " + ", ".join(down) + " (fm serve status shows why)")
    return Result("fm serve", "PASS", f"{len(states)} unit(s) active" if states else "no fm serve units")


def check_heartbeats(projects, now=None):
    """T-0434: an overdue fm run/night heartbeat (wedged, or killed mid-work) warns, and the project's notify command
    (fm notify) hears of it once per stale episode: the next beat starts a new one."""
    stale = []
    for p in projects:
        for name, hb in fmserve.stale_beats(p, now):
            what = f"{p.slug} fm {name} ({c.plain(str(hb.get('doing')))[:80]}, last beat {hb.get('at')})"
            stale.append(what)
            told = c.read_meta(p).get("heartbeat_told") or {}
            if told.get(name) != hb["due"]:
                fmserve._notify(p, f"fm {name} looks stuck or dead: {what}")
                c.update_meta(p, heartbeat_told=dict(told, **{name: hb["due"]}))
    if stale:
        return Result("heartbeats", "WARN", "overdue: " + "; ".join(stale) + " (the run log says what it last did)")
    return Result("heartbeats", "PASS", "no overdue fm run/night heartbeat")


def check_env(settings, manifest):
    """The env values fm install-user sets (drive continuation cap, earlier compaction), unless Foreman isn't wired."""
    if manifest is None:
        return Result("env", "PASS", "not wired (fm install-user hasn't run)")
    env = settings.get("env") or {}
    missing = [f"{k} ({fmsetup.WHY[k]})" for k in fmsetup.ENV if k not in env]
    if missing:
        return Result("env", "WARN", "settings.json lacks " + "; ".join(missing) + ": fm install-user adds it")
    return Result("env", "PASS", ", ".join(f"{k}={env[k]}" for k in fmsetup.ENV))


def _git_dir(root):
    """The repository folder holding root's objects (worktrees share the main one), or None outside git."""
    r = _run(["git", "-C", root, "rev-parse", "--git-common-dir"], timeout=20)
    d = r.stdout.strip()
    return os.path.normpath(os.path.join(root, d)) if r.returncode == 0 and d else None


def _empty_objects(root):
    """Zero-byte loose objects: what a crash mid-write leaves; git then fails on any command that reads one. None
    outside git. Only object names count (git's in-flight tmp_obj_* files are zero-byte for a moment), and only files
    older than a few seconds (one being written now isn't damage)."""
    gd = _git_dir(root)
    objects = os.path.join(gd, "objects") if gd else None
    if not objects or not os.path.isdir(objects):
        return None
    out, now = [], time.time()
    try:
        subs = [x for x in os.scandir(objects) if x.is_dir(follow_symlinks=False) and re.fullmatch(r"[0-9a-f]{2}", x.name)]
    except OSError:
        return []
    for sub in subs:
        try:  # git gc or prune can remove a file or folder between the listing and the stat
            for e in os.scandir(sub.path):
                if re.fullmatch(r"[0-9a-f]{38}|[0-9a-f]{62}", e.name) and e.is_file(follow_symlinks=False):
                    st = e.stat()
                    if st.st_size == 0 and now - st.st_mtime > 5:
                        out.append(e.path)
        except OSError:
            continue
    return out


def integrity_roots(projects=None):
    """Foreman's own repo and every project's root."""
    projects = [p for p, _ in c.all_projects()] if projects is None else projects
    return list(dict.fromkeys([c.foreman_home()] + [p.root for p in projects]))


def check_integrity(roots, projects, current=None):
    """T-0268: crash damage — empty git objects, zero-byte briefs, state JSON that no longer parses. T-0293: damage in
    Foreman's own repo or the current project fails; another project's only warns (its own doctor run fails it), so
    one broken repo doesn't fail every project's gate."""
    bad, scanned = [], 0
    # current: the project doctor runs in (a lane counts as its main checkout); None: every finding fails (direct
    # callers); False: run from no project, so only Foreman's own repo fails (review)
    mine = {c.foreman_home()} | ({current.root, c.main_worktree(current.root) or current.root} if current else set())
    for root in roots:
        empty = _empty_objects(root)
        scanned += empty is not None
        n = len(empty or [])
        if n:
            bad.append((current is None or root in mine, f"{n} empty git object{'s' * (n != 1)} in {root} (a crash mid-write; fm doctor "
                                      f"--repair moves them aside, and git rewrites any the working files still hold)"))
    for p in projects:
        here = current is None or bool(current) and p.slug == current.slug
        for path in sorted(glob.glob(os.path.join(p.dir, "tasks", "*.md"))):
            try:
                empty = os.path.getsize(path) == 0
            except OSError:  # removed since the listing
                continue
            if empty:
                bad.append((here, f"{p.slug}: empty brief {os.path.basename(path)} (fm doctor --restore-state or a backup)"))
        for path in sorted(glob.glob(os.path.join(p.dir, "*.json"))):
            try:
                with open(path, encoding="utf-8") as f:
                    json.load(f)
            except (OSError, ValueError):
                bad.append((here, f"{p.slug}: {os.path.basename(path)} doesn't parse (truncated?)"))
    status = "FAIL" if any(m for m, _ in bad) else "WARN" if bad else "PASS"
    return Result("integrity", status, "; ".join(d for _, d in bad) or f"{scanned} repo(s) and state intact")


def check_routing(path=None):
    """T-0293: skills/routing.json as routing_problem judges it — c.routing() quietly returns {} for a broken file, so
    hints and --split review groups would vanish with no word."""
    path = path or os.path.join(PLUGIN, "skills", "routing.json")
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError) as e:
        return Result("routing", "FAIL", f"{path}: {e}")
    why = c.routing_problem(data)
    return Result("routing", "FAIL" if why else "PASS", f"{path}: {why}" if why else "routing tables sound")


def repair(roots):
    """Move every zero-byte loose object into Foreman's quarantine (never deleted): [(from, to or the error)]."""
    stamp, moved = time.strftime("%Y%m%d-%H%M%S"), []
    for root in roots:
        for path in _empty_objects(root) or []:
            dest = os.path.join(c.state_dir(), "quarantine", f"git-objects-{stamp}",
                                re.sub(r"\W+", "-", root).strip("-"), os.path.basename(os.path.dirname(path))
                                + os.path.basename(path))
            try:  # shutil.move: the quarantine may be on another filesystem than the repo
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.move(path, dest)
                moved.append((path, dest))
            except OSError as e:
                moved.append((path, f"not moved: {e.strerror or e}"))
    return moved


_SUPPLY_SKIP = {".git", "node_modules", "__pycache__", ".venv", ".pytest_cache"}


_IN_USE = re.compile(rb'\{"pid":(\d{1,10}),"procStart":"\d{1,24}"\}\n?')


def _in_use_marker(root, d, f, full):
    """T-1455: the .in_use/<pid> file Claude Code writes into every installed plugin for each running session (one
    JSON line). Only that exact shape, in the install root's .in_use, named for its own pid, is left out of the hash."""
    if d != os.path.join(root, ".in_use") or not f.isdigit() or os.path.islink(full):
        return False
    try:
        if not os.path.isfile(full) or os.path.getsize(full) > 64:
            return False
        with open(full, "rb") as fh:
            m = _IN_USE.fullmatch(fh.read(65))
    except FileNotFoundError:
        return True  # its session ended mid-walk
    return bool(m) and m.group(1) == f.encode()


_SKIP_CAP, _SKIP_DIRS, _SKIP_TOTAL = 20_000, 20_000, 100_000  # per skipped folder: entries, then folders; per plugin
_NAMED_CAP, _NAMED_BYTES = 500, 64 << 20  # named scripts in skipped folders read per plugin, and their bytes


def _budget():
    """T-1459 review: what one plugin's skipped folders and named scripts may still cost, shared by all of them."""
    return {"entries": _SKIP_TOTAL, "bytes": _NAMED_BYTES, "read": set(), "pyc": _PYC_CAP}


_PYC_CAP, _PYC_SRC_BYTES = 200, 1 << 20  # pycs compiled per plugin; the biggest source compiled


def _pyc_of_source(p, st, budget):
    """T-1466: True only when pyc p is byte-for-byte what py_compile writes under THIS Python for the NAME.py beside its
    __pycache__: magic, flags 0, source mtime and size, and a body equal to marshal.dumps(compile(source, path)). A
    pyc Python wrote at runtime adds nothing; any other (tampered body, orphan, another Python's, hash-based, over a
    cap) keeps its stand-in. compile() never runs the source. Any doubt is False, the safe side."""
    import importlib.util
    import io
    import marshal
    import struct
    if not p.endswith(".pyc") or not stat.S_ISREG(st.st_mode) or st.st_size > 8 * _PYC_SRC_BYTES:
        return False
    d = os.path.dirname(p)
    name = os.path.basename(p).split(".", 1)[0]
    src = os.path.join(os.path.dirname(d), name + ".py")
    try:
        if (os.path.basename(d) != "__pycache__" or not name or budget["pyc"] <= 0
                or p != importlib.util.cache_from_source(src) or os.path.islink(src)):
            return False
        budget["pyc"] -= 1
        with open(src, "rb") as fh:
            ss = os.fstat(fh.fileno())
            if not stat.S_ISREG(ss.st_mode) or ss.st_size > _PYC_SRC_BYTES:
                return False
            source = fh.read(_PYC_SRC_BYTES + 1)
        with open(p, "rb") as fh:
            got = fh.read(8 * _PYC_SRC_BYTES + 1)
        # co_filename is the source path as py_compile and the importer are given it: absolute, as listed here
        code = compile(source, os.path.abspath(src), "exec", dont_inherit=True)
        head = importlib.util.MAGIC_NUMBER + struct.pack("<III", 0, int(ss.st_mtime) & 0xFFFFFFFF, ss.st_size & 0xFFFFFFFF)
        if got[:16] != head or len(got) > 8 * _PYC_SRC_BYTES:
            return False
        # marshal's ref flags follow refcounts, which differ between processes, so both bodies go through loads then
        # dumps in this process: equal means the same object graph (filename, names, consts, code), nothing trailing
        # (marshal.load builds objects only, never runs code; a hostile pyc raises, is capped at 8 MB, and stays flagged)
        # T-1799: both sides are dumped as temporaries: a held reference sets other ref flags on 3.12
        body = io.BytesIO(got[16:])
        mine = marshal.dumps(marshal.load(body))
        return body.tell() == len(got) - 16 and mine == marshal.dumps(marshal.loads(marshal.dumps(code)))
    except (OSError, ValueError, EOFError, TypeError, SyntaxError, MemoryError, RecursionError):
        return False


def _unlisted_stand(root, e, stand):
    """T-1444: a folder a walk can't list: its mode and times stand in for its files."""
    try:
        st = os.stat(e.filename)
        stand(os.fsencode(os.path.relpath(e.filename or root, root))
              + f"\0!unlisted {st.st_mode} {st.st_mtime_ns} {st.st_ctime_ns}\0".encode())
    except (OSError, TypeError):
        pass


def _stand_skipped(root, top, stand, budget):
    """T-1459: a folder _tree_hash skips (node_modules, .venv, …) by stat stand-ins: each entry's path, mode, size,
    mtime and ctime, a link's target, a folder it can't list. Never opened (a FIFO can't block), links never followed.
    Past _SKIP_CAP entries only folders, by their times (a file or package added or removed there still shows), up to
    _SKIP_DIRS of them; the plugin's budget bounds all its skipped folders together.
    ponytail: an edit in place past the cap is unseen; raise the cap if real trees hit it."""
    n = folders = 0
    rel = lambda p: os.fsencode(os.path.relpath(p, root))
    def folder(d):
        try:
            st = os.lstat(d)
            stand(rel(d) + f"\0dir {st.st_mtime_ns} {st.st_ctime_ns}\0".encode())
        except OSError:
            pass
    for d, dirs, files in os.walk(top, onerror=lambda e: _unlisted_stand(root, e, stand)):
        dirs.sort()
        if budget["entries"] <= 0:
            stand(rel(top) + b"\0!too-many\0")
            return
        if n >= _SKIP_CAP:
            folders += 1
            budget["entries"] -= 1
            if folders > _SKIP_DIRS:
                stand(rel(top) + b"\0!too-many-dirs\0")
                return
            folder(d)
            continue
        for x in sorted(dirs + files):
            if n >= _SKIP_CAP or budget["entries"] <= 0:
                stand(rel(top) + b"\0!too-many\0")
                folder(d)
                break
            n += 1
            budget["entries"] -= 1
            p = os.path.join(d, x)
            try:
                st = os.lstat(p)
                if stat.S_ISLNK(st.st_mode):
                    stand(rel(p) + b"\0->" + os.fsencode(os.readlink(p)) + b"\0")
                elif not stat.S_ISDIR(st.st_mode) and not _pyc_of_source(p, st, budget):
                    stand(rel(p) + f"\0{st.st_mode} {st.st_size} {st.st_mtime_ns} {st.st_ctime_ns}\0".encode())
            except OSError:  # removed mid-walk
                continue


def _stand_named(root, rels, stand, budget):
    """T-1459: the scripts a plugin's hooks, MCP or LSP servers name inside a skipped folder, by content. Only a file
    inside the plugin (a link out is its target path in the stat stand-ins; a file outside is never read), regular, up
    to 4 MB (past it, its size and times), opened non-blocking; each real file once, at most _NAMED_CAP files and
    _NAMED_BYTES bytes per plugin, then named as too many."""
    import hashlib
    base = os.path.realpath(root)
    for rel in rels:
        real = os.path.realpath(os.path.join(root, rel))
        if os.path.commonpath([real, base]) != base or real in budget["read"] or not os.path.isfile(real):
            continue
        if len(budget["read"]) >= _NAMED_CAP:
            stand(b"\0!too-many-named\0")
            return
        budget["read"].add(real)
        try:
            fd = os.open(real, os.O_RDONLY | os.O_NONBLOCK)
            with os.fdopen(fd, "rb") as fh:
                st = os.fstat(fd)
                if stat.S_ISREG(st.st_mode) and st.st_size <= 4_000_000:
                    if st.st_size > budget["bytes"]:
                        stand(b"\0!too-many-named\0")
                        return
                    body = fh.read(4_000_001)
                    budget["bytes"] -= len(body)
                    data = hashlib.sha256(body).hexdigest()
                else:
                    data = f"!not-read {st.st_mode} {st.st_size} {st.st_mtime_ns} {st.st_ctime_ns}"
        except OSError:
            data = "!unreadable"
        stand(os.fsencode(rel) + b"\0=" + data.encode() + b"\0")


LARGE_BYTES = 256 << 20  # T-1446: bytes of large files one plugin's check reads (streamed); past it, their stat


def _large_stand(full, rel, large, budget):
    """T-1446: a file sha only names (over 4 MB, or past its file cap) into the large hash: its bytes, streamed, while
    the plugin's LARGE_BYTES last; then its size, mtime and ctime (ctime can't be set back, so an edit shows)."""
    st = os.stat(full)
    if budget.setdefault("large", LARGE_BYTES) >= st.st_size:
        budget["large"] -= st.st_size
        digest = hashlib.sha256()
        with open(full, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                digest.update(chunk)
        large.update(rel + b"\0=" + digest.digest())
    else:
        large.update(rel + f"\0{st.st_size} {st.st_mtime_ns} {st.st_ctime_ns}\0".encode())


def _tree_hash(root, h, cap=4000, skipped=None, deps=None, budget=None, large=None):
    """Every file under an install dir (its hooks, scripts and code, not just its manifest), path and bytes, in order.
    T-1434: what h only names goes into skipped by a cheap stand-in: a symlink's target path (a linked folder's too,
    which the walk never enters) and a large file's size and mtime. A separate hash, so a baseline recorded before it
    still compares its sha as before. T-1459: the folders h skips (but .git) go into deps by stat stand-ins, a third
    hash for the same reason."""
    n, stand = 0, (skipped.update if skipped is not None else lambda b: None)
    budget = _budget() if budget is None else budget
    def unlisted(e):  # T-1444: a folder the walk can't list is named, and its mode and times stand in for its files
        h.update(os.fsencode(os.path.relpath(e.filename or root, root)) + b"\0!unlisted\0")
        _unlisted_stand(root, e, stand)
    for d, dirs, files in os.walk(root, onerror=unlisted):
        for x in sorted(dirs):
            link = os.path.join(d, x)
            if os.path.islink(link):
                stand(os.fsencode(os.path.relpath(link, root)) + b"\0->" + os.fsencode(os.readlink(link)) + b"\0")
            elif deps is not None and x in _SUPPLY_SKIP and x != ".git":
                _stand_skipped(root, link, deps.update, budget)
        dirs[:] = sorted(x for x in dirs if x not in _SUPPLY_SKIP)
        for f in sorted(files):
            full = os.path.join(d, f)
            if _in_use_marker(root, d, f, full):
                continue
            n += 1
            rel = os.fsencode(os.path.relpath(full, root))  # T-1459: a name that isn't UTF-8 is named, never raises
            try:
                # not a regular file (a FIFO would block the open forever): named, never read
                if n > cap or os.path.islink(full) or not os.path.isfile(full) or os.path.getsize(full) > 4_000_000:
                    h.update(rel + b"\0skipped\0")
                    if n <= cap and os.path.islink(full):
                        stand(rel + b"\0->" + os.fsencode(os.readlink(full)) + b"\0")
                    elif n <= cap and os.path.isfile(full):
                        st = os.stat(full)
                        stand(rel + f"\0{st.st_size} {st.st_mtime_ns}\0".encode())
                    if large is not None and not os.path.islink(full) and os.path.isfile(full):
                        _large_stand(full, rel, large, budget)
                    continue
                with open(full, "rb") as fh:
                    h.update(rel + b"\0" + fh.read())
            except OSError:  # T-1444: named, never read; raising would keep the old baseline and hide later changes
                h.update(rel + b"\0!unreadable\0")  # the stand-in below is what tells two such files apart
                try:
                    st = os.stat(full)
                    stand(rel + f"\0!unreadable {st.st_size} {st.st_mtime_ns} {st.st_ctime_ns}\0".encode())
                except OSError:
                    pass


def _supply(claude):
    """{id: {"sha": sha256, "caps": fmplugins.capabilities}} of every installed plugin's install tree (T-1392: the
    capability set beside the hash) and {"mcp:…": sha256} of each MCP server's spec (user-wide and per project), and
    {id: "why"} for each plugin it couldn't read (T-1392 review: one bad plugin costs only its own row)."""
    import hashlib
    import fmplugins
    out, errors = {}, {}
    plugins = (_load_json(os.path.join(claude, "plugins", "installed_plugins.json")) or {})
    plugins = plugins.get("plugins") if isinstance(plugins, dict) else None
    for pid, installs in sorted((plugins if isinstance(plugins, dict) else {}).items()):
        h, skipped, deps, caps, budget = hashlib.sha256(), hashlib.sha256(), hashlib.sha256(), {}, _budget()
        large = hashlib.sha256()  # T-1446
        try:
            for inst in installs if isinstance(installs, list) else [installs]:
                root = inst.get("installPath") if isinstance(inst, dict) else None
                if isinstance(root, str) and root and os.path.isdir(root):  # review: never "" (the cwd)
                    _tree_hash(root, h, skipped=skipped, deps=deps, budget=budget, large=large)
                    got = fmplugins.capabilities(root)
                    # T-1459: what runs from a skipped folder, by content
                    _stand_named(root, [s for s in got.get("scripts", []) if set(s.split(os.sep)) & _SUPPLY_SKIP],
                                 deps.update, budget)
                    for k, v in got.items():
                        caps[k] = sorted(set(caps.get(k, [])) | set(v))
        except Exception as e:
            errors[pid] = f"{type(e).__name__}: {e}"
            continue
        # T-1434: skipped, the stand-ins for what sha only names, beside it (an older entry lacks it, see _check_supply)
        # T-1459: deps, the stand-ins for the folders sha skips (node_modules, .venv, …), likewise
        # T-1446: large, the bytes of the files sha only names for their size (or past its cap: their stat), likewise
        out[pid] = {"sha": h.hexdigest(), "skipped": skipped.hexdigest(), "deps": deps.hexdigest(), "caps": caps,
                    "large": large.hexdigest()}
    conf = _load_json(os.path.join(os.path.dirname(claude), ".claude.json"))
    conf = conf if isinstance(conf, dict) else {}
    scopes = [("", conf.get("mcpServers"))] + [(f"{k}:", v.get("mcpServers")) for k, v in
                                              sorted((conf.get("projects") or {}).items()) if isinstance(v, dict)]
    for scope, servers in scopes:
        for name, spec in sorted((servers if isinstance(servers, dict) else {}).items()):
            out[f"mcp:{scope}{name}"] = hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest()
    return out, errors


def check_supply(claude, accept=False):
    """T-0672 (T-0479): plugins and MCP servers are code every session runs; a change between doctor runs (an update
    or a tampered cache) is shown once, then accepted with fm doctor --accept-supply. The first run is the baseline;
    an unreadable baseline warns (review: it never re-baselines on its own, which would hide a change)."""
    try:
        return _check_supply(claude, accept)
    except Exception as e:  # one odd file costs this check, never the whole doctor run
        return Result("supply chain", "WARN", f"not checked: {type(e).__name__}: {e}")


def _check_supply(claude, accept):
    path = os.path.join(c.state_dir(), "supply.json")
    (now, errors), seen = _supply(claude), _load_json(path)
    if os.path.exists(path) and not isinstance(seen, dict) and not accept:
        return Result("supply chain", "WARN", f"{path} is unreadable: fm doctor --accept-supply records a new baseline")
    for k in errors:  # a plugin it couldn't read keeps its old baseline: neither changed, gone nor accepted
        if isinstance(seen, dict) and k in seen:
            now[k] = seen[k]
    unchecked = "not checked: " + _ids(errors, lambda k: f" ({c.plain(errors[k])[:80]})") if errors else ""
    if seen is None or accept:
        c.write_atomic(path, json.dumps(now, sort_keys=True, indent=1))
        return Result("supply chain", "WARN" if errors else "PASS", f"{'accepted' if accept and seen is not None else 'baseline of'} "
                      f"{len(now)} plugin(s) and MCP server(s)" + (f"; {unchecked}" if errors else ""))
    sha = lambda v: v.get("sha") if isinstance(v, dict) else v  # a baseline before T-1392 holds bare hashes
    caps = lambda v: v.get("caps") if isinstance(v, dict) else None
    skip = lambda v: v.get("skipped") if isinstance(v, dict) else None  # T-1434: None in an entry recorded before it
    dep = lambda v: v.get("deps") if isinstance(v, dict) else None  # T-1459: likewise
    big = lambda v: v.get("large") if isinstance(v, dict) else None  # T-1446: likewise
    changed, added, held, upgraded = [], [], [], False
    for k in sorted(set(now) - set(errors)):
        was, cur = seen.get(k), now[k]
        if k in seen and sha(was) == sha(cur) and skip(was) in (None, skip(cur)) and dep(was) in (None, dep(cur)) \
                and big(was) in (None, big(cur)):
            if was == cur:
                continue
            old, new = caps(was), caps(cur)
            # an unchanged tree's entry gains what this version records (review), the fields its version had equal
            if isinstance(new, dict) and (not isinstance(old, dict) or all(new.get(x) == v for x, v in old.items())):
                seen[k], upgraded = cur, True
                continue
        # review: the delta is read even when the hashes match (they skip the 4,001st file on, FIFOs, devices)
        (changed if k in seen else added).append(k)
        held += [f"{c.plain(k)[:60]} {d}" for d in _capability_delta(was, cur, k)]
    if upgraded:
        c.write_atomic(path, json.dumps(seen, sort_keys=True, indent=1))
    # a spec file Foreman won't read hides what it runs, so it stays held: accepting can't see past it
    held += [f"{c.plain(k)[:60]} can't read {c.plain(u)[:80]} (outside the plugin, not a file or over 8 MB)"
             for k in sorted(now) for u in (caps(now[k]) or {}).get("unread") or []]
    gone = sorted(set(seen) - set(now))
    note = "; ".join(x for x in (f"changed: {_ids(changed)}" if changed else "", f"new: {_ids(added)}" if added else "",
                                 f"gone: {_ids(gone)}" if gone else "", unchecked) if x)
    if held:  # T-1392: new code that runs on its own is held, named, until accepted
        return Result("supply chain", "FAIL", "; ".join(held[:12]) + (f"; and {len(held) - 12} more" if len(held) > 12
                      else "") + (f" ({note})" if note else "") + " — review what it runs, then fm doctor --accept-supply")
    if not (changed or added or gone):
        return Result("supply chain", "WARN" if errors else "PASS",
                      f"{len(now)} plugin(s) and MCP server(s) unchanged" + (f"; {unchecked}" if errors else ""))
    return Result("supply chain", "WARN", note + " — expected (an update you ran)? fm doctor --accept-supply")


def _ids(ids, extra=lambda k: ""):
    """Plugin ids for a doctor line: plain (an id is outside text) and capped at ten."""
    ids = sorted(ids)
    return ", ".join(c.plain(k)[:60] + extra(k) for k in ids[:10]) + (f" and {len(ids) - 10} more" if len(ids) > 10 else "")


def _capability_delta(was, now, key=""):
    """T-1392: what an update or a new entry adds that runs on its own: hook events, hook handlers on an existing
    event, MCP servers (new, or one whose spec changed) and scripts, as phrases. A plugin with no recorded set (new,
    or a baseline before T-1392) is diffed against nothing (review). T-1434: also frontmatter hooks, LSP servers and
    hooks modules; a field the recorded set's version didn't have reads "has", like a hash-only baseline."""
    if key.startswith("mcp:"):  # a user or project MCP server: its spec's hash
        return [f"{'changes' if was is not None else 'adds'} MCP server {c.plain(key[4:])[:60]}"]
    legacy = isinstance(was, str)  # a baseline from before T-1392 holds only the hash: what runs was never recorded
    was, now = (v.get("caps") if isinstance(v, dict) else None for v in (was, now))
    recorded = isinstance(was, dict)  # a new plugin has no set: what it brings is news
    was, now = (v if isinstance(v, dict) else {} for v in (was, now))
    verb = lambda k: "has" if legacy or (recorded and k not in was) else "adds"
    def new(k):
        had = set(was.get(k) or [])
        return [x for x in now.get(k) or [] if x not in had]
    def split(specs):  # {name: {digest, …}}: two components may share a name (review), so digests compare as sets
        out = {}
        for s in specs or []:
            if isinstance(s, str) and " " in s:
                out.setdefault(s.rsplit(" ", 1)[0], set()).add(s.rsplit(" ", 1)[1])
        return out
    changes = lambda k: [m for m, d in sorted(split(now.get(k)).items()) if m in split(was.get(k))
                         and d - split(was.get(k))[m]]
    events = new("hooks")
    return ([f"{verb('hooks')} hook {c.plain(e)[:40]}" for e in events]
            + [f"{verb('handlers')} a {c.plain(h.split(' ', 1)[0])[:40]} hook handler "
               f"({c.plain(h.split(': ', 1)[-1])[:60]})" for h in new("handlers") if h.split(" ", 1)[0] not in events]
            + [f"{verb('fm_hooks')} hook {c.plain(e)[:80]}" for e in new("fm_hooks")]
            + [f"changes the hooks of {c.plain(w)[:60]}" for w in changes("fm_hook_specs")]
            + [f"runs hooks module {c.plain(m)[:80]}" for m in new("modules")]
            + [f"{verb('mcp')} MCP server {c.plain(m)[:40]}" for m in new("mcp")]
            + [f"changes MCP server {c.plain(m)[:40]}" for m in changes("mcp_specs")]
            + [f"{verb('lsp')} LSP server {c.plain(m)[:40]}" for m in new("lsp")]
            + [f"changes LSP server {c.plain(m)[:40]}" for m in changes("lsp_specs")]
            + [f"{verb('scripts')} script {c.plain(s)[:80]}" for s in new("scripts")])


ENFORCE_KINDS = ("validator_block", "merge_refused", "lane_unverified", "card_injected")


def check_enforce(p, days=7):
    """T-0949: how often the enforced steps fired in this project over the last days: write validators that blocked
    (T-0947; their first events carry no kind), lane merges refused red or waived (T-0948), cards injected at edit
    time. Information, never a failure."""
    if not p:
        return Result("enforcement", "PASS", "none: not in a Foreman project")
    counts = dict.fromkeys(ENFORCE_KINDS, 0)
    since = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(time.time() - days * 86400))
    try:
        with open(os.path.join(p.dir, "ledger.jsonl"), "rb") as f:
            lines = [l for l in f if b'"enforce"' in l or b'"lane_unverified"' in l or b'"lib' in l]
    except OSError:
        lines = []
    read = named = 0  # T-0977: stack cards read (fm lib show) and named at prompt time
    for line in lines:
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if not isinstance(e, dict) or str(e.get("ts", ""))[:19] < since or not isinstance(e.get("data") or {}, dict):
            continue  # a hand-edited line with odd data is skipped, never a crash
        if e.get("event") in ("lib", "lib_named"):
            n = len((e.get("data") or {}).get("cards") or [])
            read, named = (read + n, named) if e["event"] == "lib" else (read, named + n)
            continue
        kind = "lane_unverified" if e.get("event") == "lane_unverified" else \
            (e.get("data") or {}).get("kind", "validator_block") if e.get("event") == "enforce" else None
        if kind in counts:
            counts[kind] += 1
    return Result("enforcement", "PASS", f"last {days} days: " + ", ".join(f"{k} {n}" for k, n in counts.items())
                  + f", cards named {named}, cards read {read}")


def check_usage_burn(found=None):
    """T-1800: why usage burns, named with its fix (fmcost.burn_findings), so nobody has to notice it first."""
    if found is None:
        import fmcost
        found = fmcost.burn_findings()
        fmcost.write_burn(found)
    return Result("usage burn", "WARN" if found else "PASS",
                  "; ".join(f"{a} → {b}" for a, b in found) + "; /usage names Claude Code's own causes, f applies them"
                  if found else "no sign of usage burn in the last 2 days")


def check_idle_stops(p, days=7):
    """T-0957: stops with open work that nothing kept going (the drive was off, paused or done nudging). Information:
    many of them mean the drive gave up early or the user keeps stopping it."""
    if not p:
        return Result("idle stops", "PASS", "none: not in a Foreman project")
    since = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(time.time() - days * 86400))
    try:  # bytes first, as check_enforce does: prompt events make the ledger large
        with open(os.path.join(p.dir, "ledger.jsonl"), "rb") as f:
            lines = [ln for ln in f if b'"idle_stop"' in ln]
    except OSError:
        lines = []
    n = 0
    for ln in lines:
        try:
            e = json.loads(ln)
        except ValueError:
            continue
        n += isinstance(e, dict) and e.get("event") == "idle_stop" and str(e.get("ts", ""))[:19] >= since
    return Result("idle stops", "PASS", f"last {days} days: {n} idle stop{'s' if n != 1 else ''} with open work")


# ---------------------------------------------------------------- fm fsck (T-1667)

FSCK_SKIP = {"lib-sources", "lib-drafts", "quarantine", "snapshots", "outputs", "cache", "research-cache"}  # other
# repos' files and copies, not Foreman's live state: never scanned, so --fix can't reach them
FSCK_TAIL = 65536  # bytes of a journal read: its last line is judged, never the whole file
FSCK_LOCK_AGE = 3600  # s: a pid file is judged only once this old. A holder in another PID namespace (Claude Code's
# sandbox) looks dead to os.kill, and fmcli._sentinel already counts an hour-old sentinel.pid as no run (review)
FSCK_KINDS = ("broken lane", "stale lock", "torn journal", "corrupt state", "unreadable")
FSCK_JSON_MAX = 1 << 20  # bytes: a state *.json bigger than this isn't parsed (T-1669)
PID_NS = "/proc/self/ns/pid"
INIT_PID_NS = "pid:[4026531836]"  # the kernel's fixed inode of the initial PID namespace (PROC_PID_INIT_INO); a user
# can't read /proc/1/ns/pid to compare with


def _tail(path, n):
    """(the last n bytes, the stat) of a regular file; (None, None) for a symlink, a FIFO or a device (T-1434: a plain
    open of a FIFO blocks forever) or a file gone or unreadable for another reason. PermissionError is raised: the
    caller names the file as unreadable rather than pass it over."""
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    except PermissionError:
        raise
    except OSError:
        return None, None
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode):
            return None, None
        os.lseek(fd, max(0, st.st_size - n), os.SEEK_SET)
        return os.read(fd, n), st
    except OSError:
        return None, None
    finally:
        os.close(fd)


def _stale_pid(path, now=None):
    """Why a *.pid lock's holder is gone ("" while it may live): the file is FSCK_LOCK_AGE s old or more and its pid
    names no process, or it holds no pid. A pid that exists (another user's too: EPERM) keeps it, and so does a file
    too big to be a pid file of ours."""
    data, st = _tail(path, 33)
    if data is None or st.st_size > 32 or (now or time.time()) - st.st_mtime < FSCK_LOCK_AGE:
        return ""
    text = data.strip()
    if not (text.isdigit() and len(text) <= 9 and int(text) > 0):  # never os.kill(0): that signals our own group
        return "it holds no pid" if text else "it is empty"
    try:
        os.kill(int(text), 0)
    except ProcessLookupError:
        return f"process {int(text)} is gone"
    except OSError:
        pass
    return ""


def _torn(path):
    """Why a journal's last line is torn ("" when it is whole): no newline after it (a write cut short) or not JSON. A
    last line longer than FSCK_TAIL isn't judged. A torn tail is read once more a moment later: events.jsonl is
    appended all the time, and a line landing now is whole by then."""
    why = _torn_once(path)
    if why:
        time.sleep(0.05)
        why = _torn_once(path)
    return why


def _torn_once(path):
    data, st = _tail(path, FSCK_TAIL)
    if not data:
        return ""
    if not data.endswith(b"\n"):
        return "its last line has no newline (a write cut short)"
    body = data[:-1]
    if b"\n" not in body and len(data) < st.st_size:
        return ""
    last = body.rsplit(b"\n", 1)[-1].strip()
    try:
        if last:
            json.loads(last)
    except (ValueError, RecursionError):  # UnicodeDecodeError too; a line of 60k "[" is nested past the stack
        return "its last line isn't JSON"
    return ""


def _not_a_worktree(lane):
    """Why a lane folder is no git worktree any more ("" when it is one, or can't be told): gone, no .git, or a .git
    file whose gitdir record git worktree prune removed."""
    if not os.path.isdir(lane):
        return "its folder is gone"
    git = os.path.join(lane, ".git")
    if os.path.isdir(git) or os.path.islink(git):
        return ""
    try:
        data, _ = _tail(git, 4096)
    except PermissionError:
        return ""
    m = re.fullmatch(rb"gitdir:\s*(.+?)\s*", data or b"")
    if not m:
        return "its folder isn't a git worktree any more"
    record = os.path.join(lane, os.fsdecode(m.group(1)))  # a relative gitdir is relative to the lane
    return "" if os.path.isdir(record) else f"its git record is gone ({record}: git worktree prune removed it)"


def _broken_lanes(projects, here=None):
    """Open tasks whose lane folder is gone or no git worktree, or whose branch is gone. Only looks: a lane's files and
    another project's worktrees are never touched (git only reads refs, from the project's root). The fm lane rm hint
    is given only for here, the current project's slug: task ids repeat across projects."""
    out = []
    for p in projects:
        for b in c.load_briefs(p):
            lane, branch = b.meta.get("lane"), b.meta.get("lane_branch")
            if not isinstance(lane, str) or not lane or b.status in c.CLOSED:  # a closed task's lane is fm tidy's
                continue
            why = _not_a_worktree(lane)
            if not why and isinstance(branch, str) and branch and c._git(
                    p.root, "rev-parse", "--verify", "-q", f"refs/heads/{branch}", timeout=10, proc=True).returncode == 1:
                why = f"its branch {branch} is gone"  # only git's own "no such ref": a timeout or no repo says nothing
            if why:
                out.append({"kind": "broken lane", "path": lane, "task": b.id, "project": p.slug,
                            "detail": f"{b.id}: {why}" + (f" (fm lane rm {b.id} frees the task)" if p.slug == here
                                                          else "")})
    return out


def fsck(projects=None, state=None, here=None):
    """T-1667: what a crash or a hand edit left broken in Foreman's own state, as {kind, path, detail, project[, task]}:
    open tasks' lanes whose folder or branch is gone, *.pid locks whose process is dead, journals (*.jsonl) whose last
    line is torn, state *.json that doesn't parse (T-1669), and files it can't read. project is None for state no
    project owns. Reads only."""
    state = state or c.state_dir()
    found = _broken_lanes([p for p, _ in c.all_projects()] if projects is None else projects, here)
    pdir, now = os.path.join(state, "projects"), time.time()
    for root, dirs, names in os.walk(state):  # symlinked folders aren't followed
        dirs[:] = sorted(x for x in dirs if root != state or x not in FSCK_SKIP)
        for n in sorted(names):
            path, lock = os.path.join(root, n), n.endswith(".pid")
            state_json = n.endswith(".json") and (root == state or os.path.dirname(root) == pdir)  # T-1669: meta,
            # gate, status: the files fm reads whole; a session's or an audit's own files aren't judged
            try:
                if state_json:
                    why, kind = _corrupt_json(path), "corrupt state"
                else:
                    why = _stale_pid(path, now) if lock else _torn(path) if n.endswith(".jsonl") else ""
                    kind = "stale lock" if lock else "torn journal"
            except PermissionError:
                what = "lock" if lock else "state file" if state_json else "journal"
                why, kind = f"permission denied: fsck can't check this {what}", "unreadable"
            if why:
                rel = os.path.relpath(path, pdir)
                found.append({"kind": kind, "path": path, "detail": why,
                              "project": None if rel.startswith("..") else rel.split(os.sep)[0]})
    return found


def _corrupt_json(path):
    """T-1669: why a state *.json doesn't parse ("" when it does, or is too big to judge)."""
    if os.path.getsize(path) > FSCK_JSON_MAX:
        return ""
    with open(path, encoding="utf-8", errors="replace") as f:
        try:
            json.load(f)
        except ValueError as e:
            return f"isn't valid JSON ({e}); Foreman can't read it: fix it by hand or restore it"
    return ""


def _pid_ns_doubt():
    """Why os.kill can't be trusted to see every lock's holder here ("" when it can): this process runs in a PID
    namespace of its own (a sandbox or a container), or that can't be told."""
    if not sys.platform.startswith("linux"):
        return ""  # no PID namespaces
    try:
        ns = os.readlink(PID_NS)
    except OSError as e:
        return f"this process's PID namespace can't be read ({e.strerror})"
    return "" if ns == INIT_PID_NS else (f"this process runs in a PID namespace of its own ({ns}: a sandbox or a "
                                         f"container), where a live lock's holder can look dead")


def fsck_fix(found):
    """Remove the stale locks among found, each re-checked just before; (removed paths, the findings left for a person).
    A broken lane or a torn journal is never repaired here: the ledger is hash-chained, and a lane holds work. Refused
    (PolicyError) where os.kill can't see every process."""
    doubt = _pid_ns_doubt()
    if doubt:
        raise c.PolicyError(f"{doubt}: fm fsck --fix removes no lock here; run it from a shell outside the sandbox")
    fixed, left = [], []
    for f in found:
        if f["kind"] != "stale lock":
            left.append(f)
            continue
        try:
            stale = _stale_pid(f["path"])  # a new holder may have written its pid since the scan: then it isn't stale
        except PermissionError:
            left.append(dict(f, kind="unreadable", detail="permission denied: fsck can't check this lock"))
            continue
        if stale:
            try:  # ponytail: the re-check narrows the race with a holder starting now to microseconds; it doesn't close it
                os.unlink(f["path"])
                fixed.append(f["path"])
            except FileNotFoundError:
                pass
            except OSError as e:
                left.append(dict(f, detail=f"{f['detail']}; couldn't remove it: {e.strerror}"))
    return fixed, left


def _fsck_counts(found):
    return ", ".join(f"{n} {k}{'s' if n > 1 else ''}" for k in FSCK_KINDS if (n := sum(f["kind"] == k for f in found)))


def check_fsck(projects=None):
    """T-1667: fm fsck's one line in fm doctor, so /foreman:doctor covers it."""
    try:
        found = fsck(projects)
    except Exception as e:  # the scan failing is a finding, not a crash of doctor
        return Result("fsck", "WARN", f"not run: {e}")
    return Result("fsck", "WARN", f"{_fsck_counts(found)}: fm fsck lists them (--fix removes only the stale locks)") \
        if found else Result("fsck", "PASS", "no broken lanes, stale locks, torn journals or corrupt state")


def check_landlock():
    """T-1607: whether fm code workers can be confined (Landlock); unavailable is a note, never a failure."""
    import fmlandlock
    ok, why = fmlandlock.available()
    if os.environ.get("FOREMAN_CONFINE") == "0":
        return Result("worker confinement", "PASS", "off (FOREMAN_CONFINE=0)")
    return Result("worker confinement", "PASS", f"Landlock {why}: fm code workers write only in their tree" if ok
                  else f"not available ({why}): fm code workers run unconfined, as before")


def check_headless():
    """T-1638: whether fm shot can render headlessly (a Chromium and its version); a note, never a failure."""
    import fmshot
    name = "headless rendering"
    path = fmshot.chrome()
    if not path:
        env = os.environ.get("FOREMAN_CHROME")
        return Result(name, "PASS", f"not available (FOREMAN_CHROME={env!r} is not an executable file)" if env
                      else "not available (no Chromium on PATH or in Playwright's download); optional, nothing is installed")
    try:  # a version probe only, never a page load
        p = subprocess.run([path, "--version"], capture_output=True, text=True, timeout=5, stdin=subprocess.DEVNULL)
    except (OSError, subprocess.TimeoutExpired) as e:
        return Result(name, "PASS", f"not available ({path} did not start: {type(e).__name__})")
    if p.returncode:
        last = next((x for x in reversed((p.stderr or p.stdout).splitlines()) if x.strip()), f"exit {p.returncode}")
        return Result(name, "PASS", f"not available ({path} failed to start: {fmshot.safe(last.strip())[:200]})")
    ver = fmshot.safe((p.stdout.strip().splitlines() or ["version unknown"])[0])[:80]
    return Result(name, "PASS", f"available ({path}, {ver})")


def cmd_fsck(args):
    here = getattr(args, "project", None) or getattr(c.find_project(os.getcwd()), "slug", None)
    found = fsck(here=here)
    fixed, left = fsck_fix(found) if args.fix else ([], found)
    if args.json:
        print(json.dumps({"ok": not left, "findings": left, "fixed": fixed}, indent=2, ensure_ascii=False))
        return 1 if left else 0
    for path in fixed:
        print(f"{'removed':<13} {c.plain(path)}: a stale lock")
    for f in left:  # a hand-edited brief's lane path could hold escape sequences
        print(f"{f['kind']:<13} [{c.plain(f['project'] or 'state')}] {c.plain(f['path'])}: {c.plain(f['detail'])}")
    hints = (["fm fsck --fix removes the stale locks"] if any(f["kind"] == "stale lock" for f in left) else []) + (
        ["the rest is left for a person (fm lane list in its project; a torn ledger: fm verify-ledger)"]
        if any(f["kind"] != "stale lock" for f in left) else [])
    ok = "OK: no broken lanes, stale locks, torn journals or corrupt state"
    print(("\n" if fixed or left else "") + "fm fsck: " + (f"{_fsck_counts(left)}; " + "; ".join(hints) if left else ok))
    return 1 if left else 0


def run_all(full=False, accept_supply=False):
    home = c.foreman_home()
    claude = os.path.join(os.path.expanduser("~"), ".claude")
    settings_path = os.path.join(claude, "settings.json")
    settings = _load_json(settings_path) or {}
    manifest = _load_json(os.path.join(c.state_dir(), "install-manifest.json"))
    results = [check_python(refresh=fmpy.refresh, child=bool(os.environ.get("FOREMAN_PY_CHILD"))), check_settings_json([settings_path, os.path.join(claude, "settings.local.json"),
                                    os.path.join(home, ".claude-plugin", "marketplace.json"),
                                    os.path.join(PLUGIN, ".claude-plugin", "plugin.json"),
                                    os.path.join(PLUGIN, "settings.json"), os.path.join(PLUGIN, "hooks", "hooks.json")]),
               check_hook_scripts(), check_state_dir(home, c.state_dir()), check_lock_probe(c.state_dir()), check_disk(), check_env(settings, manifest),
               check_serve(fmserve.states()), check_hook_events(), check_plugins(), check_mod_release(home),
               check_supply(claude, accept_supply), check_worktree_base(settings), check_fm_link(),
               check_invisible_text(instruction_files()), check_rule_conflicts(rule_files(c.git_root(os.getcwd())))]
    try:
        if os.environ.get("FOREMAN_DOCTOR_BENCH") == "0":  # T-1379: the tests' fm doctor runs, which read no timings
            raise _NoBench
        load = busy()
        bench, sizes = _bench_and_injection(bench_runs(load))
        load = load or busy()  # T-1219: a burst that began during the bench made its timings, not the hooks, slow
        results += [check_hook_latency(bench, load), check_hook_exit_codes(bench), check_injection_budgets(sizes)]
    except _NoBench:
        results += [Result(n, "WARN", "not measured (FOREMAN_DOCTOR_BENCH=0)")
                    for n in ("hook latency", "hook exit codes", "injection budgets")]
    except Exception as e:  # the bench itself failing is a finding, not a crash
        results += [Result(n, "FAIL", f"bench failed: {e}") for n in ("hook latency", "hook exit codes", "injection budgets")]
    results += [check_hook_errors(), check_hook_slo(), check_hook_writers(settings, home), check_name_collisions(settings),
                check_footprint(os.path.join(PLUGIN, "rules", "foreman.md"), os.path.join(claude, "CLAUDE.md")),
                check_frontmatter(), check_unloaded_skills()]
    projects = [p for p, _ in c.all_projects()]
    results.append(check_heartbeats(projects))
    results.append(check_state_size(projects))
    results.append(check_fsck(projects))
    results.append(check_landlock())
    results.append(check_headless())
    brief_results = [check_briefs(p) for p in projects]
    worst = next((s for s in ("FAIL", "WARN") if any(r.status == s for r in brief_results)), "PASS")
    results.append(Result("briefs", worst, "; ".join(r.detail for r in brief_results if r.status != "PASS")
                          or f"{len(projects)} project(s) OK"))
    stale = [p.slug for p in projects if not views_match(p)]  # T-0494
    results.append(Result("views", "WARN" if stale else "PASS",
                          f"views don't match the briefs in {', '.join(stale[:5])}: fm doctor --fix regenerates them"
                          if stale else "status views match the briefs"))
    here = c.find_project(os.getcwd())
    results.append(check_dual_install())
    results.append(check_running_code(os.path.join(here.dir, "ledger.jsonl") if here else "",
                                      os.path.join(claude, "plugins", "installed_plugins.json")))
    results.append(check_product(here))
    results.append(check_enforce(here))
    results.append(check_idle_stops(here))
    results.append(check_usage_burn())
    results.append(check_version_skew(c.all_projects()))
    results += [check_self_docs(home), check_file_map(home, os.path.join(home, "MASTER.md")), check_backup(home), check_validate(home),
                check_git_hygiene(home), check_core_integrity(home), check_statusline(settings, manifest, os.path.join(PLUGIN, "hooks", "statusline")),
                check_deny_rules(settings, manifest), check_rules_symlink(), check_scripts(home, full),
                check_integrity(integrity_roots(projects), projects, current=c.find_project(os.getcwd()) or False),
                check_routing(), check_cc_features(), check_upstream()]
    return results


def _fix_views():
    n = 0
    for p, _ in c.all_projects():
        if not views_match(p):
            with c.lock(p.dir):
                c.regen_views(p, mirror=False)
            n += 1
    return f"regenerated {n} project view(s)"


def _fix_integrity():
    return f"moved {len(repair(integrity_roots()))} empty git object(s) to the quarantine"


def _recheck_integrity():
    projects = [p for p, _ in c.all_projects()]
    return check_integrity(integrity_roots(projects), projects).status == "PASS"


def _fix_state_dir():
    return f"state moved back to {c.restore_default_state()}"


def _fix_fsck():
    try:
        return f"removed {len(fsck_fix(fsck())[0])} stale lock(s)"
    except c.PolicyError as e:
        return f"no lock removed: {e}"


# result name -> (the repair a flag already performs, whether the check now passes); nothing here is new behaviour
FIXERS = {
    "views": (_fix_views, lambda: all(views_match(p) for p, _ in c.all_projects())),
    "integrity": (_fix_integrity, _recheck_integrity),
    "state dir": (_fix_state_dir, lambda: c.state_dir() == os.path.join(c.foreman_home(), "state")),
    "fsck": (_fix_fsck, lambda: check_fsck().status == "PASS"),  # T-1667: only its stale locks
}


def fix(results):
    """T-1184: apply the safe repair for each non-PASS result that has one; (fixed, left) as "name: what" lines. A
    finding is left when it has no repair, the repair errs, or the check still fails after it."""
    fixed, left = [], []
    for r in results:
        if r.status == "PASS":
            continue
        fixer = FIXERS.get(r.name)
        if not fixer:
            left.append(f"{r.name}: {r.detail}")
            continue
        try:
            did = fixer[0]()
            ok = fixer[1]()
        except OSError as e:
            did, ok = f"repair failed: {e}", False
        (fixed if ok else left).append(f"{r.name}: {did}" if ok else f"{r.name}: {did}; still failing: {r.detail}")
    return fixed, left


def report_wrong(args):
    """T-1606: fm doctor --wrong "CMD": a false alarm (or, --should block, a miss) filed as a labelled guard case plus
    one FIX task for a person to review, once per case. The guard itself is never changed here."""
    import fmcli
    import fmreplay
    should, why = args.should or "allow", (args.why or "").strip()
    k = fmreplay.add_case(args.wrong, should, os.path.abspath(args.cwd) if args.cwd else "",
                          f"fm doctor --wrong: {why}" if why else "fm doctor --wrong")
    got = (fmreplay.drift([k]) or [{}])[0].get("got")  # None: the guard agrees with the label today
    wrong_now = got is not None
    # the case lives in Foreman's own corpus, so its review task goes to that checkout's project, not the cwd's
    p, made = c.find_project(fmreplay._corpus_root()) or c.find_project(os.getcwd()), None
    if wrong_now and p:
        shown = c.fit(" ".join(k["cmd"].split()), 100)
        with c.lock(p.dir):
            have = "".join(b.section("Raw request") for b in c.load_briefs(p, include_archive=True))
            if f"[guard-case {k['id']}]" not in have:
                title = (f"Guard false alarm: should allow: {shown}" if should == "allow"
                         else f"Guard miss: should block: {shown}")
                b = fmcli._create(p, title, "FIX", "S", "captured", source="discovered", raw=(
                    f"[guard-case {k['id']}] fm doctor --wrong (T-1606): the guard "
                    f"{'refuses' if should == 'allow' else 'allows'} `{shown}` in {k.get('cwd') or '~'}; "
                    f"{why or 'no reason given'}. Review it: correct fmguard.py if the label is right ("
                    + ("never loosen the guard without the user's yes" if should == "allow" else "tighten it")
                    + "), or correct the label."))
                c.log_event(p, "capture", task=b.id, data={"source": "discovered", "type": "FIX"})
                made = b.id
        if made:
            c.regen_views(p)
    verdict = ("the guard couldn't judge it (it raised)" if got == "unable" else
               "the guard " + ("refuses" if should == "allow" else "allows") + " it today") if wrong_now else \
        f"the guard already {'allows' if should == 'allow' else 'refuses'} it today: nothing to review"
    fmcli.out(args, {"case": k, "wrong_now": wrong_now, "got": got, "captured": made,
                     "project": p.slug if p else None, "corpus": fmreplay.cases_path()},
              f"Stored guard case {k['id']} (should {should}) in {fmreplay.cases_path()}; {verdict}"
              + (f"; captured {made} in {p.slug} for review" if made else "") + ". The guard itself is unchanged.")


def cmd_doctor(args):
    if getattr(args, "wrong", None):
        return report_wrong(args)
    if args.restore_state:
        try:
            return print(f"Foreman state is in {c.restore_default_state()}")
        except OSError as e:
            print(f"fm doctor: {e}", file=sys.stderr)
            sys.exit(1)
    if args.repair:
        moved = repair(integrity_roots())
        print("\n".join(f"{a} → {b}" for a, b in moved) or "Nothing to repair: no empty git objects.")
        fixed = []
        for p, _ in c.all_projects():  # T-0494: views that don't match their briefs are regenerated
            if not views_match(p):
                with c.lock(p.dir):
                    c.regen_views(p, mirror=False)
                fixed.append(p.slug)
        print(f"Views regenerated in {', '.join(fixed)}." if fixed else "Views match the briefs everywhere.")
        return None
    results = run_all(full=args.full, accept_supply=getattr(args, "accept_supply", False))
    if getattr(args, "fix", False):
        fixed, left = fix(results)
        print("\n".join(["Fixed:"] + [f"  {x}" for x in fixed]) if fixed else "Fixed: nothing")
        print("\n".join(["Left for a person:"] + [f"  {x}" for x in left]) if left else "Left for a person: nothing")
        if left:
            sys.exit(1)
        return None
    ok = not any(r.status == "FAIL" for r in results)
    if args.json:
        print(json.dumps({"ok": ok, "results": [asdict(r) for r in results]}, indent=2, ensure_ascii=False))
    else:
        for r in results:  # T-0844: only what needs a look, unless -v
            if r.status != "PASS" or getattr(args, "verbose", False):
                print(f"{r.status:4}  {r.name:<20} {r.detail}")
        print(f"\nfm doctor: {'OK' if ok else 'FAILED'} ({sum(r.status == 'PASS' for r in results)} pass, "
              f"{sum(r.status == 'WARN' for r in results)} warn, {sum(r.status == 'FAIL' for r in results)} fail)")
    if not ok:
        sys.exit(1)


def views_match(p):
    """T-0494: whether the project's one-line views (state.line, status.json) say what its briefs do now; a torn
    or hand-edited view, or one a crash left behind, doesn't. Unreadable briefs count as matching (check_briefs
    reports those)."""
    try:
        sd = c.state_dict(c.main_view(p))
        want = {"state.line": c.state_line(sd) + "\n", "status.json": json.dumps(c.status_dict(sd)) + "\n"}
    except Exception:
        return True
    for name, text in want.items():
        try:
            with open(os.path.join(p.dir, name), encoding="utf-8") as f:
                if f.read() != text:
                    return False
        except OSError:
            return False
    return True


def cmd_wiring(args):
    """T-0469: one screen of what is wired: Foreman's version and where it runs from, its hooks, this project's flags,
    the standing yeses, trust, the pause, the budget and the enabled plugins. Read-only."""
    import fmbudget
    import fmcli
    p = fmcli.resolve(args)
    meta = c.read_meta(p)
    try:
        with open(os.path.join(PLUGIN, ".claude-plugin", "plugin.json"), encoding="utf-8") as f:
            version = json.load(f).get("version")
        with open(os.path.join(PLUGIN, "hooks", "hooks.json"), encoding="utf-8") as f:
            hooks = json.load(f).get("hooks", {})
    except (OSError, ValueError):
        version, hooks = None, {}
    try:
        with open(os.path.join(os.path.expanduser("~"), ".claude", "settings.json"), encoding="utf-8") as f:
            plugins = sorted(k for k, v in (json.load(f).get("enabledPlugins") or {}).items() if v)
    except (OSError, ValueError, AttributeError):
        plugins = []
    caps, high = fmbudget.effective()
    data = {"version": version, "plugin": PLUGIN, "hooks": {e: [g.get("matcher", "") for g in gs] for e, gs in hooks.items()},
            "autonomy": meta.get("autonomy", "standard"), "drive": bool(meta.get("drive")),
            "sensitive": bool(meta.get("sensitive")), "sync": bool(meta.get("sync")),
            "standing": sorted(meta.get("standing") or {}), "trust": bool(c.trusted()), "paused": c.panicked(),
            "budget": caps, "budget_halved": high, "plugins": plugins}
    lines = [f"Foreman version {version} from {PLUGIN}",
             "hooks: " + " · ".join(e + (f" ({', '.join(m for m in ms if m)})" if any(ms) else "")
                                    for e, ms in data["hooks"].items()),
             f"{p.slug}: autonomy {data['autonomy']} · drive {'on' if data['drive'] else 'off'} · sensitive "
             f"{'on' if data['sensitive'] else 'off'} · sync {'on' if data['sync'] else 'off'}",
             f"standing yes: {', '.join(data['standing']) or 'none'} · trust {'on' if data['trust'] else 'off'} · "
             f"pause {'ON' if data['paused'] else 'off'}",
             "budget: " + ", ".join(f"{k} ${v:g}" for k, v in caps.items()) + (f" (halved: {high})" if high else ""),
             f"plugins enabled ({len(plugins)}): " + (", ".join(plugins[:12]) + (" …" if len(plugins) > 12 else "")
                                                       if plugins else "none")]
    return fmcli.out(args, data, "\n".join(lines))
