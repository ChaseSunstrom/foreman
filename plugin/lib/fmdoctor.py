"""fm doctor: Foreman self-check (BUILD_PROMPT §12). Each check returns a Result; FAIL makes the command exit 1."""
import glob
import json
import os
import re
import shutil
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
RULES_CHARS_MAX = 6000  # chars (~1.5k tokens) of always-on rules: denser lines cost as much as more lines
CTX_BUDGET, PROMPT_BUDGET = 2000, 400
READ_ONLY_TOOLS = {"Read", "Grep", "Glob", "WebFetch", "WebSearch"}
EDITING_AGENTS = {"fm-builder.md": {"Edit", "Write", "Bash"}}  # T-0234: the one bounded exception, in its own worktree
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


def busy():
    """'load L on N cores' when the 1-minute load passes the core count, else None (T-0367)."""
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


def _frontmatter(path):
    m = re.match(r"^---\n(.*?)\n---\n", _read(path) or "", re.S)
    if not m:
        return None
    meta = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        if k.strip():
            meta[k.strip()] = v.strip()
    return meta


def check_frontmatter(plugin=PLUGIN):
    bad = []
    skills = os.path.join(plugin, "skills")
    for name in sorted(os.listdir(skills)) if os.path.isdir(skills) else []:
        if not os.path.isdir(os.path.join(skills, name)):
            continue  # a skill is a folder; skills/routing.json (T-0252) is data
        meta = _frontmatter(os.path.join(skills, name, "SKILL.md"))
        if meta is None or not meta.get("name") or not meta.get("description"):
            bad.append(f"skill {name}: missing frontmatter name/description")
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
    return Result("frontmatter", "FAIL" if bad else "PASS", "; ".join(bad) or "skills and read-only agents valid")


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
        return Result("backup", "FAIL", "no backups/*.tgz")
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


def _version(root):
    return (_load_json(os.path.join(root, ".claude-plugin", "plugin.json")) or {}).get("version") or "?"


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


def recent_hook_errors():
    """Hook errors of the last 24h, each its log lines: "<ts> <event> <traceback…>" and its continuation."""
    log = _read(os.path.join(c.state_dir(), "logs", "hooks.log")) or ""
    entries = []
    for line in log.splitlines():
        if re.match(r"\d{4}-\d\d-\d\dT\S+ ", line):
            entries.append([line])
        elif entries:
            entries[-1].append(line)
    return [e for e in entries if (c.age_days(e[0].split(" ", 1)[0]) or 99) < 1]


def paused_hooks():
    """T-0087: the events the hook breaker has paused after failing in a row."""
    import fmhooks
    return fmhooks.paused_hooks()


def check_hook_errors():
    recent, paused = recent_hook_errors(), paused_hooks()
    if paused:
        return Result("hook errors", "FAIL", f"paused: {', '.join(paused)} ({len(recent)} hook error(s) in the last "
                                             f"24h; a paused hook runs again 10 min after its last failure; "
                                             f"state/logs/hooks.log)")
    if not recent:
        return Result("hook errors", "PASS", "no hook errors in the last 24h")
    last = recent[-1]
    event = c.plain((last[0].split(" ") + ["", ""])[1])  # log text can carry anything an error message quoted
    cause = c.plain(next((l.strip() for l in reversed(last) if l.strip()), ""))
    return Result("hook errors", "WARN", f"{len(recent)} hook error(s) in the last 24h; latest: {event} "
                                         f"{c.fit(cause, 120)} (state/logs/hooks.log)")


# ---------------------------------------------------------------- orchestration

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
        text = re.sub(r"```.*?```", "", _read(path) or "", flags=re.S)  # fences would shift backtick pairing
        for span in re.findall(r"`([^`\n]+)`", text):
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
    for kind, folder, strip in (("skill", "skills", ""), ("agent", "agents", ".md")):
        for name in sorted(os.listdir(os.path.join(plugin, folder))) if os.path.isdir(os.path.join(plugin, folder)) else []:
            name = name[:-len(strip)] if strip and name.endswith(strip) else name
            if name not in master:
                bad.append(f"MASTER.md doesn't mention the {kind} {name}")
    bad += [f"MASTER.md doesn't name the module {m}" for m in missing_modules(home, master)]  # T-0491
    readme, install = _read(os.path.join(home, "README.md")) or "", _read(os.path.join(home, "install.sh")) or ""
    header = "\n".join(l for l in install.splitlines()[:20] if l.startswith("#"))  # the --help text
    help_flags = set(re.findall(r"(--[\w-]+)", header))
    readme_flags = {f for line in readme.splitlines() if line.startswith("Flags:") for f in re.findall(r"`(--[\w-]+)`", line)}
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


def check_hook_events(registered=None):
    """Every event fmhooks handles is registered in hooks.json (a new hook needs /reload-plugins to take effect)."""
    import fmhooks
    if registered is None:
        registered = set(_load_json(os.path.join(PLUGIN, "hooks", "hooks.json")).get("hooks") or {})
    missing = sorted((set(fmhooks.HANDLERS) | {"PreToolUse"}) - set(registered))
    if missing:
        return Result("hook events", "FAIL", "handled but not registered in hooks.json: " + ", ".join(missing))
    return Result("hook events", "PASS", f"{len(registered)} events registered (after changes: /reload-plugins)")


def check_plugins():
    import fmplugins
    found = fmplugins.check()
    if found:
        names = sorted({f["plugin"] for f in found})
        return Result("plugins", "WARN", f"{len(found)} conflict(s) in {', '.join(names[:4])}"
                      + (" …" if len(names) > 4 else "") + " (fm plugins check)")
    return Result("plugins", "PASS", "no conflicts among enabled plugins")


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


def _tree_hash(root, h, cap=4000):
    """Every file under an install dir (its hooks, scripts and code, not just its manifest), path and bytes, in order."""
    n = 0
    for d, dirs, files in os.walk(root):
        dirs[:] = sorted(x for x in dirs if x not in _SUPPLY_SKIP)
        for f in sorted(files):
            full = os.path.join(d, f)
            n += 1
            if n > cap or os.path.islink(full) or os.path.getsize(full) > 4_000_000:
                h.update(os.path.relpath(full, root).encode() + b"\0skipped\0")
                continue
            with open(full, "rb") as fh:
                h.update(os.path.relpath(full, root).encode() + b"\0" + fh.read())


def _supply(claude):
    """{id: sha256} of every enabled plugin's install tree and each MCP server's spec (user-wide and per project)."""
    import hashlib
    out = {}
    plugins = (_load_json(os.path.join(claude, "plugins", "installed_plugins.json")) or {})
    plugins = plugins.get("plugins") if isinstance(plugins, dict) else None
    for pid, installs in sorted((plugins if isinstance(plugins, dict) else {}).items()):
        h = hashlib.sha256()
        for inst in installs if isinstance(installs, list) else [installs]:
            root = inst.get("installPath") if isinstance(inst, dict) else None
            if isinstance(root, str) and root and os.path.isdir(root):  # review: never "" (the cwd)
                _tree_hash(root, h)
        out[pid] = h.hexdigest()
    conf = _load_json(os.path.join(os.path.dirname(claude), ".claude.json"))
    conf = conf if isinstance(conf, dict) else {}
    scopes = [("", conf.get("mcpServers"))] + [(f"{k}:", v.get("mcpServers")) for k, v in
                                              sorted((conf.get("projects") or {}).items()) if isinstance(v, dict)]
    for scope, servers in scopes:
        for name, spec in sorted((servers if isinstance(servers, dict) else {}).items()):
            out[f"mcp:{scope}{name}"] = hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest()
    return out


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
    now, seen = _supply(claude), _load_json(path)
    if os.path.exists(path) and not isinstance(seen, dict) and not accept:
        return Result("supply chain", "WARN", f"{path} is unreadable: fm doctor --accept-supply records a new baseline")
    if seen is None or accept:
        c.write_atomic(path, json.dumps(now, sort_keys=True, indent=1))
        return Result("supply chain", "PASS", f"{'accepted' if accept and seen is not None else 'baseline of'} "
                                              f"{len(now)} plugin(s) and MCP server(s)")
    changed = sorted(k for k in now if seen.get(k) not in (None, now[k]))
    added, gone = sorted(set(now) - set(seen)), sorted(set(seen) - set(now))
    if not (changed or added or gone):
        return Result("supply chain", "PASS", f"{len(now)} plugin(s) and MCP server(s) unchanged")
    return Result("supply chain", "WARN", "; ".join(x for x in (
        f"changed: {', '.join(changed)}" if changed else "", f"new: {', '.join(added)}" if added else "",
        f"gone: {', '.join(gone)}" if gone else "") if x) + " — expected (an update you ran)? fm doctor --accept-supply")


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
               check_hook_scripts(), check_state_dir(home, c.state_dir()), check_env(settings, manifest),
               check_serve(fmserve.states()), check_hook_events(), check_plugins(), check_mod_release(home),
               check_supply(claude, accept_supply)]
    try:
        load = busy()
        bench, sizes = _bench_and_injection(bench_runs(load))
        results += [check_hook_latency(bench, load), check_hook_exit_codes(bench), check_injection_budgets(sizes)]
    except Exception as e:  # the bench itself failing is a finding, not a crash
        results += [Result(n, "FAIL", f"bench failed: {e}") for n in ("hook latency", "hook exit codes", "injection budgets")]
    results += [check_hook_errors(), check_hook_slo(), check_hook_writers(settings, home), check_name_collisions(settings),
                check_footprint(os.path.join(PLUGIN, "rules", "foreman.md"), os.path.join(claude, "CLAUDE.md")),
                check_frontmatter()]
    projects = [p for p, _ in c.all_projects()]
    results.append(check_heartbeats(projects))
    brief_results = [check_briefs(p) for p in projects]
    worst = next((s for s in ("FAIL", "WARN") if any(r.status == s for r in brief_results)), "PASS")
    results.append(Result("briefs", worst, "; ".join(r.detail for r in brief_results if r.status != "PASS")
                          or f"{len(projects)} project(s) OK"))
    here = c.find_project(os.getcwd())
    results.append(check_running_code(os.path.join(here.dir, "ledger.jsonl") if here else "",
                                      os.path.join(claude, "plugins", "installed_plugins.json")))
    results.append(check_product(here))
    results.append(check_version_skew(c.all_projects()))
    results += [check_self_docs(home), check_file_map(home, os.path.join(home, "MASTER.md")), check_backup(home), check_validate(home),
                check_git_hygiene(home), check_core_integrity(home), check_statusline(settings, manifest, os.path.join(PLUGIN, "hooks", "statusline")),
                check_deny_rules(settings, manifest), check_rules_symlink(), check_scripts(home, full),
                check_integrity(integrity_roots(projects), projects, current=c.find_project(os.getcwd()) or False),
                check_routing()]
    return results


def cmd_doctor(args):
    if args.restore_state:
        try:
            return print(f"Foreman state is in {c.restore_default_state()}")
        except OSError as e:
            print(f"fm doctor: {e}", file=sys.stderr)
            sys.exit(1)
    if args.repair:
        moved = repair(integrity_roots())
        print("\n".join(f"{a} → {b}" for a, b in moved) or "Nothing to repair: no empty git objects.")
        return None
    results = run_all(full=args.full, accept_supply=getattr(args, "accept_supply", False))
    ok = not any(r.status == "FAIL" for r in results)
    if args.json:
        print(json.dumps({"ok": ok, "results": [asdict(r) for r in results]}, indent=2, ensure_ascii=False))
    else:
        for r in results:
            print(f"{r.status:4}  {r.name:<20} {r.detail}")
        print(f"\nfm doctor: {'OK' if ok else 'FAILED'} ({sum(r.status == 'PASS' for r in results)} pass, "
              f"{sum(r.status == 'WARN' for r in results)} warn, {sum(r.status == 'FAIL' for r in results)} fail)")
    if not ok:
        sys.exit(1)
