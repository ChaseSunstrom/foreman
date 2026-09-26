"""fm tidy: hygiene for Foreman state, auto memory, CLAUDE.md and rules (BUILD_PROMPT §9).

Dry-run by default. --apply performs only safe, reversible actions (archive, rotate, roll up, dedupe after
archiving a copy) and logs them; everything needing judgment (stale inbox items, dead paths, cycles,
oversize memory, contradictions) is reported for a decision. Nothing is deleted without an archive copy,
except derived caches (old statusline snapshots).
"""
import json
import os
import re
import shutil
import time

import fmcore as c

ARCHIVE_AFTER_DAYS = 14
INBOX_STALE_DAYS = 30
LEDGER_ROLL_BYTES = 1_000_000
EVENTS_ROTATE_BYTES = 5_000_000
HOOKS_LOG_ROTATE_BYTES = 1_000_000
ROTATED_KEEP = 3
SNAPSHOT_MAX_DAYS = 7
MEMORY_MAX_LINES, MEMORY_MAX_BYTES = 200, 25_000
GLOBAL_MD_MAX, PROJECT_MD_MAX = 50, 150
KNOWN_PLUGINS = {"ponytail", "claude-hud", "security-guidance", "code-review", "context7", "skill-creator",
                 "claude-md-management", "plugin-dev", "frontend-design", "clangd-lsp", "rust-analyzer-lsp",
                 "pyright-lsp", "typescript-lsp", "gopls-lsp", "playwright", "chrome-devtools-mcp", "foreman",
                 "ecc", "superpowers", "design", "figma", "document-skills", "differential-review",
                 "insecure-defaults", "static-analysis", "sharp-edges", "supply-chain-risk-auditor", "c-review"}
LSP_BINARIES = {"clangd-lsp": "clangd", "pyright-lsp": "pyright-langserver", "typescript-lsp": "typescript-language-server",
                "gopls-lsp": "gopls", "rust-analyzer-lsp": "rust-analyzer"}


def finding(project, kind, severity, detail, fix="", auto=False):
    return {"project": project, "kind": kind, "severity": severity, "detail": detail, "fix": fix, "auto": auto}


# ---------------------------------------------------------------- helpers

_PATH_TOKEN = re.compile(r"`([^`\s]+)`")


def _looks_like_path(tok):
    if any(ch in tok for ch in "<>$*{}|()=,;") or "://" in tok or tok.startswith(("-", "@", "#")):
        return False
    if re.fullmatch(r"/[\w:-]+", tok):  # a slash command such as /foreman:intake, not a path
        return False
    return "/" in tok or bool(re.fullmatch(r"[\w.-]+\.[A-Za-z0-9]{1,6}", tok))


def dead_paths(text, base):
    out = []
    for tok in _PATH_TOKEN.findall(text):
        if not _looks_like_path(tok):
            continue
        path = os.path.expanduser(tok) if tok.startswith("~") else os.path.join(base, tok)
        if not os.path.exists(path.rstrip("/")) and tok not in out:
            out.append(tok)
    return out


def stale_commands(text, root):
    out = []
    pkg = os.path.join(root, "package.json")
    scripts = None
    if os.path.exists(pkg):
        try:
            with open(pkg) as f:
                scripts = set((json.load(f).get("scripts") or {}).keys())
        except (OSError, ValueError):
            scripts = None
    if scripts is not None:  # without a package.json, npm lines are generic guidance, not this repo's commands
        for m in re.finditer(r"\b(?:npm run|pnpm run|yarn run|bun run)\s+([\w:.-]+)", text):
            if m.group(1) not in scripts:
                out.append(m.group(0))
    mk = os.path.join(root, "Makefile")
    if os.path.exists(mk):
        with open(mk, errors="replace") as f:
            targets = set(re.findall(r"^([\w.-]+)\s*:(?!=)", f.read(), re.M))
        for m in re.finditer(r"`make\s+([\w.-]+)", text):
            if m.group(1) not in targets:
                out.append(f"make {m.group(1)}")
    return list(dict.fromkeys(out))


def _norm(line):
    return re.sub(r"\s+", " ", line.strip().lstrip("-*").strip().lower())


def _read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return None


def memory_dir(root):
    return os.path.join(os.path.expanduser("~"), ".claude", "projects", re.sub(r"[^A-Za-z0-9]", "-", root), "memory")


# ---------------------------------------------------------------- per-project checks

def check_project(p, apply, actions):
    out, slug = [], p.slug
    briefs = c.load_briefs(p)
    import fmdocs  # fmdocs reuses this module's detectors
    for f in fmdocs.scan(p.root):
        out.append(finding(slug, "docs_drift", "warn", f"{f['file']}: {f['kind']} `{f['detail']}` doesn't exist",
                           "update the doc (fm docs lists every drift)"))
    for b in briefs:
        age = c.age_days(b.meta.get("updated")) or 0
        if b.status in c.CLOSED and age > ARCHIVE_AFTER_DAYS:
            out.append(finding(slug, "archive_task", "action", f"{b.id} {b.status} {int(age)}d ago: {b.title}",
                               "move to archive/YYYY-MM/", auto=True))
            if apply:
                dest = os.path.join(p.dir, "archive", (b.meta.get("updated") or c.now())[:7])
                os.makedirs(dest, exist_ok=True)
                shutil.move(b.path, os.path.join(dest, os.path.basename(b.path)))
                actions.append(("archive_task", b.id))
        elif b.status == "captured" and age > INBOX_STALE_DAYS:
            out.append(finding(slug, "inbox_stale", "warn", f"{b.id} captured {int(age)}d ago: {b.title}",
                               f"keep (fm task new … --from {b.id}) or drop (fm task drop {b.id} \"<why>\")"))
    _, cycles, dangling = c.order_queue(briefs)
    for cyc in cycles:
        out.append(finding(slug, "cycle", "warn", "dependency cycle: " + " ↔ ".join(cyc), "fm task set ID depends_on=…"))
    for a, d in dangling:
        out.append(finding(slug, "dangling_dep", "warn", f"{a} depends on unknown {d}", f"fm task set {a} depends_on=…"))
    status = {b.id: b.status for b in briefs}
    for b in briefs:
        deps = b.meta.get("depends_on") or []
        if b.status == "blocked" and deps and all(status.get(d) in c.CLOSED for d in deps):
            out.append(finding(slug, "unblockable", "warn", f"{b.id} is blocked but its dependencies are closed",
                               f"fm task set {b.id} status=planned"))
    out += _roll_ledger(p, apply, actions)
    out += _check_memory(p, apply, actions)
    out += _check_instructions(slug, p.root, [os.path.join(p.root, "CLAUDE.md"), os.path.join(p.root, ".claude", "CLAUDE.md"),
                                              os.path.join(p.root, "CLAUDE.local.md")],
                               os.path.join(p.root, ".claude", "rules"), PROJECT_MD_MAX)
    if apply:
        with c.lock(p.dir):
            c.regen_views(p)
        c.update_meta(p, last_tidy=c.now())
        c.log_event(p, "tidy", data={"actions": [f"{k}:{v}" for k, v in actions if k != "global"][:50],
                                     "findings": len(out)})
    return out


def _roll_ledger(p, apply, actions):
    path = os.path.join(p.dir, "ledger.jsonl")
    try:
        size = os.path.getsize(path)
    except OSError:
        return []
    if size <= LEDGER_ROLL_BYTES:
        return []
    out = [finding(p.slug, "roll_ledger", "action", f"ledger.jsonl is {size // 1024} KB",
                   "move past months to archive/ledger-YYYY-MM.jsonl", auto=True)]
    if apply:
        month = c.now()[:7]
        with c.lock(p.dir):
            keep, rolled = [], {}
            with open(path, encoding="utf-8") as f:
                for line in f:
                    try:
                        m = json.loads(line).get("ts", month)[:7]
                    except ValueError:
                        m = month
                    (rolled.setdefault(m, []) if m < month else keep).append(line)
            os.makedirs(os.path.join(p.dir, "archive"), exist_ok=True)
            for m, lines in rolled.items():
                with open(os.path.join(p.dir, "archive", f"ledger-{m}.jsonl"), "a", encoding="utf-8") as f:
                    f.writelines(lines)
            c.write_atomic(path, "".join(keep))
        c.log_event(p, "ledger_rolled", data={m: len(v) for m, v in rolled.items()})
        actions.append(("roll_ledger", ",".join(sorted(rolled))))
    return out


def _check_memory(p, apply, actions):
    d = memory_dir(p.root)
    index = os.path.join(d, "MEMORY.md")
    text = _read(index)
    out = []
    if text is None:
        return out
    lines = text.splitlines()
    if len(lines) > MEMORY_MAX_LINES or len(text.encode()) > MEMORY_MAX_BYTES:
        out.append(finding(p.slug, "memory_oversize", "warn", f"MEMORY.md is {len(lines)} lines / {len(text.encode())} B "
                           f"(startup window {MEMORY_MAX_LINES} lines / {MEMORY_MAX_BYTES} B)", "move detail into topic files"))
    seen, dupes, deduped = set(), [], []
    for line in lines:
        key = _norm(line)
        if key and not line.lstrip().startswith("#") and key in seen:
            dupes.append(line.strip())
            continue
        seen.add(key)
        deduped.append(line)
    if dupes:
        out.append(finding(p.slug, "memory_duplicate", "action", f"{len(dupes)} duplicate MEMORY.md line(s): {dupes[0][:80]}",
                           "keep the first occurrence (a copy is archived first)", auto=True))
        if apply:
            os.makedirs(os.path.join(p.dir, "archive"), exist_ok=True)
            shutil.copy2(index, os.path.join(p.dir, "archive", f"memory-{time.strftime('%Y%m%d-%H%M%S')}.md"))
            c.write_atomic(index, "\n".join(deduped) + ("\n" if text.endswith("\n") else ""))
            actions.append(("memory_duplicate", len(dupes)))
    for tok in dead_paths(text, p.root):
        out.append(finding(p.slug, "memory_dead_path", "warn", f"MEMORY.md mentions missing path `{tok}`",
                           "update or remove the entry"))
    for f in sorted(os.listdir(d)):
        full = os.path.join(d, f)
        if f != "MEMORY.md" and re.search(r"progress|status|todo|tasks", f, re.I) and os.path.getsize(full) > 20_000:
            out.append(finding(p.slug, "memory_progress_log", "info", f"memory/{f} is {os.path.getsize(full) // 1024} KB of "
                               "progress notes", "task status belongs in Foreman briefs/STATE; keep memory for durable learnings"))
    return out


def _check_instructions(slug, base, md_files, rules_dir, max_lines):
    out, texts = [], {}
    for path in md_files:
        text = _read(path)
        if text is None:
            continue
        texts[path] = text
        n = len(text.splitlines())
        if n > max_lines:
            out.append(finding(slug, "claude_md_size", "warn", f"{path} is {n} lines (budget {max_lines})",
                               "move detail to rules with paths: or to docs read on demand"))
        for tok in dead_paths(text, base):
            out.append(finding(slug, "dead_path", "warn", f"{os.path.basename(path)} mentions missing path `{tok}`",
                               "fix or remove the line"))
        for cmd in stale_commands(text, base):
            out.append(finding(slug, "stale_command", "warn", f"{os.path.basename(path)} mentions `{cmd}`, not defined in "
                               "package.json/Makefile", "update the command"))
    rules = {}
    if os.path.isdir(rules_dir):
        for f in sorted(os.listdir(rules_dir)):
            if f.endswith(".md"):
                rules[f] = _read(os.path.join(rules_dir, f)) or ""
                for tok in dead_paths(rules[f], base):
                    out.append(finding(slug, "dead_path", "warn", f"rules/{f} mentions missing path `{tok}`", "fix the rule"))
    md_lines = {_norm(l) for t in texts.values() for l in t.splitlines() if len(_norm(l)) > 25}
    for f, t in rules.items():
        for line in t.splitlines():
            if len(_norm(line)) > 25 and _norm(line) in md_lines:
                out.append(finding(slug, "rule_duplicate", "warn", f"rules/{f} repeats a CLAUDE.md line: {line.strip()[:80]}",
                                   "keep it in one place"))
    return out


# ---------------------------------------------------------------- global checks

def check_global(apply, actions, plugins=False):
    home_claude = os.path.join(os.path.expanduser("~"), ".claude")
    out = _check_instructions(None, os.path.expanduser("~"), [os.path.join(home_claude, "CLAUDE.md")],
                              os.path.join(home_claude, "rules"), GLOBAL_MD_MAX)
    logs = os.path.join(c.state_dir(), "logs")
    for name, limit, kind in (("events.jsonl", EVENTS_ROTATE_BYTES, "rotate_events"),
                              (os.path.join("logs", "hooks.log"), HOOKS_LOG_ROTATE_BYTES, "rotate_hooks_log")):
        path = os.path.join(c.state_dir(), name)
        try:
            size = os.path.getsize(path)
        except OSError:
            continue
        if size <= limit:
            continue
        out.append(finding(None, kind, "action", f"{name} is {size // 1024} KB", "rotate into state/logs/", auto=True))
        if apply:
            os.makedirs(logs, exist_ok=True)
            stem, ext = os.path.basename(name).rsplit(".", 1)
            os.replace(path, os.path.join(logs, f"{stem}-{time.strftime('%Y%m%d-%H%M%S')}.{ext}"))
            open(path, "a").close()
            rotated = sorted(f for f in os.listdir(logs) if f.startswith(stem + "-"))
            for old in rotated[:-ROTATED_KEEP]:
                os.remove(os.path.join(logs, old))
            actions.append(("global", kind))
    sessions = os.path.join(c.state_dir(), "sessions")
    if os.path.isdir(sessions):
        old = [f for f in os.listdir(sessions)
               if time.time() - os.path.getmtime(os.path.join(sessions, f)) > SNAPSHOT_MAX_DAYS * 86400]
        if old:
            out.append(finding(None, "old_snapshots", "action", f"{len(old)} statusline snapshot(s) older than "
                               f"{SNAPSHOT_MAX_DAYS}d", "delete (derived cache)", auto=True))
            if apply:
                for f in old:
                    os.remove(os.path.join(sessions, f))
                actions.append(("global", "old_snapshots"))
    if plugins:
        out += _check_plugins()
    return out


def _check_plugins():
    import subprocess
    out = []
    try:
        listing = json.loads(subprocess.run(["claude", "plugin", "list", "--json"], capture_output=True, text=True,
                                            timeout=60).stdout or "[]")
    except (OSError, ValueError, subprocess.SubprocessError):
        return [finding(None, "plugins", "info", "could not run `claude plugin list --json`")]
    for pl in listing:
        pid = pl.get("id", "")
        name = pid.split("@")[0]
        if not pl.get("enabled", True):
            continue
        if name not in KNOWN_PLUGINS:
            out.append(finding(None, "plugin_unclassified", "warn", f"{pid} isn't classified in BUILD_PROMPT §4.6",
                               "map it to a lifecycle stage, scope it to projects, or disable it"))
        if name in LSP_BINARIES and not shutil.which(LSP_BINARIES[name]):
            out.append(finding(None, "plugin_lsp_missing", "warn", f"{pid} is enabled but `{LSP_BINARIES[name]}` isn't on PATH",
                               f"install the server or: claude plugin disable {pid}"))
        try:
            details = subprocess.run(["claude", "plugin", "details", pid], capture_output=True, text=True, timeout=60).stdout
        except (OSError, subprocess.SubprocessError):
            continue
        m = re.search(r"Always-on:\s+~?([\d,.]+k?) tok", details)
        if m:
            out.append(finding(None, "plugin_footprint", "info", f"{pid}: ~{m.group(1)} always-on tokens"))
    return out


# ---------------------------------------------------------------- command

def cmd_tidy(args):
    import fmcli
    projects = [p for p, _ in c.all_projects()] if args.all else [fmcli.resolve(args)]
    actions, findings = [], []
    for p in projects:
        findings += check_project(p, args.apply, actions)
    findings += check_global(args.apply, actions, plugins=getattr(args, "plugins", False))
    report = {"applied": bool(args.apply), "projects": [p.slug for p in projects], "findings": findings,
              "actions": [f"{k}:{v}" for k, v in actions]}
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return
    if not findings:
        print("Tidy: nothing to do.")
        return
    order = {"action": 0, "warn": 1, "info": 2}
    for f in sorted(findings, key=lambda f: (order[f["severity"]], f["project"] or "", f["kind"])):
        mark = {"action": "DONE" if args.apply else "APPLY", "warn": "DECIDE", "info": "info"}[f["severity"]]
        print(f"{mark:6} [{f['project'] or 'global'}] {f['kind']}: {f['detail']}" + (f"  → {f['fix']}" if f["fix"] else ""))
    if not args.apply and any(f["auto"] for f in findings):
        print("Dry run. `fm tidy --apply` performs the APPLY items (archives first, never deletes user requests).")
