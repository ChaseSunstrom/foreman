"""fm doctor: Foreman self-check (BUILD_PROMPT §12). Each check returns a Result; FAIL makes the command exit 1."""
import json
import os
import re
import subprocess
import sys
from dataclasses import asdict, dataclass

import fmcore as c

PLUGIN = c.PLUGIN_ROOT
RULES_MAX, BLOCK_MAX, ALWAYS_ON_MAX = 80, 5, 120
CTX_BUDGET, PROMPT_BUDGET = 2000, 400
READ_ONLY_TOOLS = {"Read", "Grep", "Glob", "WebFetch", "WebSearch"}
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


def check_hook_latency(bench):
    over = [f"{k} p95 {v['p95']}ms > {v['budget']}ms" for k, v in bench.items() if not v["ok"]]
    worst = max((v["p95"] for v in bench.values()), default=0)
    return Result("hook latency", "FAIL" if over else "PASS", "; ".join(over) or f"all {len(bench)} fixtures, worst p95 {worst} ms")


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


def check_footprint(rules_path, claude_md_path):
    rules = (_read(rules_path) or "").splitlines()
    md = _read(claude_md_path) or ""
    m = re.search(r"<!-- foreman:begin -->.*?<!-- foreman:end -->", md, re.S)
    block = m.group(0).splitlines() if m else []
    total = len(rules) + len(block)
    bad = []
    if len(rules) > RULES_MAX:
        bad.append(f"rules {len(rules)} lines > {RULES_MAX}")
    if len(block) > BLOCK_MAX:
        bad.append(f"CLAUDE.md block {len(block)} lines > {BLOCK_MAX}")
    if total > ALWAYS_ON_MAX:
        bad.append(f"always-on {total} lines > {ALWAYS_ON_MAX}")
    return Result("footprint", "FAIL" if bad else "PASS",
                  "; ".join(bad) or f"rules {len(rules)} + CLAUDE.md block {len(block)} = {total} always-on lines (≤ {ALWAYS_ON_MAX})")


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
        elif tools - READ_ONLY_TOOLS:
            bad.append(f"agent {f}: not read-only ({', '.join(sorted(tools - READ_ONLY_TOOLS))})")
    return Result("frontmatter", "FAIL" if bad else "PASS", "; ".join(bad) or "skills and read-only agents valid")


def _strip_generated(text):
    return re.sub(r"(?m)^_Generated .*_$", "", text or "")


def check_briefs(p):
    errors = []
    briefs = c.load_briefs(p, errors=errors)
    if errors:
        return Result("briefs", "FAIL", f"{p.slug}: unparseable " + ", ".join(os.path.basename(e[0]) for e in errors))
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
    d = os.path.join(home, "backups")
    tgz = sorted(f for f in os.listdir(d) if f.endswith(".tgz")) if os.path.isdir(d) else []
    return Result("backup", "PASS" if tgz else "FAIL", f"latest {tgz[-1]}" if tgz else "no backups/*.tgz")


def check_validate(home):
    bad = []
    for target in (home, os.path.join(home, "plugin")):
        r = _run(["claude", "plugin", "validate", "--strict", target])
        if r.returncode != 0:
            tail = (r.stdout + r.stderr).strip().splitlines()[-1:] or ["failed"]
            bad.append(f"{target}: {tail[0]}")
    return Result("plugin validate", "FAIL" if bad else "PASS", "; ".join(bad) or "marketplace and plugin pass --strict")


def check_git_hygiene(repo):
    tracked = _run(["git", "-C", repo, "ls-files", "-ci", "--exclude-standard"]).stdout.split()
    staged = _run(["git", "-C", repo, "diff", "--cached", "--name-only", "--diff-filter=AM"]).stdout.split()
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


def check_hook_errors():
    log = _read(os.path.join(c.state_dir(), "logs", "hooks.log")) or ""
    recent = [l for l in log.splitlines() if (c.age_days(l.split(" ", 1)[0]) or 99) < 1]
    return Result("hook errors", "WARN" if recent else "PASS",
                  f"{len(recent)} hook error(s) in the last 24h (state/logs/hooks.log)" if recent else "no hook errors in the last 24h")


# ---------------------------------------------------------------- orchestration

def _bench_and_injection():
    import tempfile
    sys.path.insert(0, os.path.join(PLUGIN, "tests"))
    import bench_hooks
    bench = bench_hooks.run_bench(runs=5)
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
    missing = [n for n in sorted(cmds) if not re.search(rf"\b{re.escape(n)}\b", master)]
    if missing:
        bad.append("MASTER.md lacks fm " + ", ".join(missing))
    for kind, folder, strip in (("skill", "skills", ""), ("agent", "agents", ".md")):
        for name in sorted(os.listdir(os.path.join(plugin, folder))) if os.path.isdir(os.path.join(plugin, folder)) else []:
            name = name[:-len(strip)] if strip and name.endswith(strip) else name
            if name not in master:
                bad.append(f"MASTER.md doesn't mention the {kind} {name}")
    readme, install = _read(os.path.join(home, "README.md")) or "", _read(os.path.join(home, "install.sh")) or ""
    header = "\n".join(l for l in install.splitlines()[:20] if l.startswith("#"))  # the --help text
    help_flags = set(re.findall(r"(--[\w-]+)", header))
    readme_flags = {f for line in readme.splitlines() if line.startswith("Flags:") for f in re.findall(r"`(--[\w-]+)`", line)}
    bad += [f"README.md doesn't document install.sh {f}" for f in sorted(help_flags - readme_flags)]
    bad += [f"README.md lists {f}, which install.sh doesn't have" for f in sorted(readme_flags - help_flags)]
    bad = list(dict.fromkeys(bad))
    return Result("self docs", "FAIL" if bad else "PASS", "; ".join(bad[:12]) + (f" (+{len(bad) - 12} more)" if len(bad) > 12
                                                                                  else "") if bad else "docs match the code")


def check_state_dir(home, state):
    default = os.path.join(home, "state")
    if state == default:
        return Result("state dir", "PASS", state)
    return Result("state dir", "WARN", f"fallback in use: {state} ({default} isn't writable, or FOREMAN_STATE is set)")


def run_all(full=False):
    home = c.foreman_home()
    claude = os.path.join(os.path.expanduser("~"), ".claude")
    settings_path = os.path.join(claude, "settings.json")
    settings = _load_json(settings_path) or {}
    manifest = _load_json(os.path.join(c.state_dir(), "install-manifest.json"))
    results = [check_settings_json([settings_path, os.path.join(claude, "settings.local.json"),
                                    os.path.join(home, ".claude-plugin", "marketplace.json"),
                                    os.path.join(PLUGIN, ".claude-plugin", "plugin.json"),
                                    os.path.join(PLUGIN, "settings.json"), os.path.join(PLUGIN, "hooks", "hooks.json")]),
               check_hook_scripts(), check_state_dir(home, c.state_dir())]
    try:
        bench, sizes = _bench_and_injection()
        results += [check_hook_latency(bench), check_hook_exit_codes(bench), check_injection_budgets(sizes)]
    except Exception as e:  # the bench itself failing is a finding, not a crash
        results += [Result(n, "FAIL", f"bench failed: {e}") for n in ("hook latency", "hook exit codes", "injection budgets")]
    results += [check_hook_errors(), check_hook_writers(settings, home), check_name_collisions(settings),
                check_footprint(os.path.join(PLUGIN, "rules", "foreman.md"), os.path.join(claude, "CLAUDE.md")),
                check_frontmatter()]
    projects = [p for p, _ in c.all_projects()]
    brief_results = [check_briefs(p) for p in projects]
    worst = next((s for s in ("FAIL", "WARN") if any(r.status == s for r in brief_results)), "PASS")
    results.append(Result("briefs", worst, "; ".join(r.detail for r in brief_results if r.status != "PASS")
                          or f"{len(projects)} project(s) OK"))
    results += [check_self_docs(home), check_file_map(home, os.path.join(home, "MASTER.md")), check_backup(home), check_validate(home),
                check_git_hygiene(home), check_statusline(settings, manifest, os.path.join(PLUGIN, "hooks", "statusline")),
                check_deny_rules(settings, manifest), check_rules_symlink(), check_scripts(home, full)]
    return results


def cmd_doctor(args):
    results = run_all(full=args.full)
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
