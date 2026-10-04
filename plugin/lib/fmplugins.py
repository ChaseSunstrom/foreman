"""fm plugins: find a capability in the known marketplaces, check enabled plugins for conflicts with Foreman and with
each other, and install one after the user's yes (guard category `plugin`, granted only through `fm ask`).

Everything is read from disk (~/.claude/plugins): marketplace indexes, their local plugin copies and the install
cache. Always-on cost is estimated from skill/agent/command descriptions (~4 characters a token).
"""
import glob
import hashlib
import json
import os
import re
import subprocess

import fmcore as c

# What Foreman already owns, and the skill/command names that duplicate it (process, not domain, knowledge).
FOREMAN_OWNS = {
    "brainstorming": ("brainstorm", "ideation"),
    "planning and intake": ("writing-plans", "executing-plans", "plan-mode", "planner", "feature-dev", "prd"),
    "verification gates": ("verification-before-completion", "verify-before", "quality-gate"),
    "task tracking and drive": ("todo", "task-tracker", "ralph"),
}
# Measured conflicts, by plugin name; setup-plugins.sh warns about the same ones (test_docs keeps the lists equal).
KNOWN_CONFLICTS = {
    "ecc": "~41k always-on tokens and 24 hook handlers, with its own memory, learning and planning; Foreman ports "
           "its useful procedures as /foreman:playbooks",
    "superpowers": "a second orchestrator (brainstorm → plan → execute); Foreman ports its debugging, TDD and "
                   "verification procedures",
    "feature-dev": "duplicates Foreman's intake and planning",
    "ralph-loop": "keeps Claude running via a Stop hook; collides with Foreman's completion gate",
    "example-skills": "12 mostly unrelated skills; duplicates skill-creator and frontend-design",
}
_STOP = {"a", "an", "the", "for", "and", "or", "of", "to", "with", "in", "on", "my", "i", "need", "plugin"}


def claude_dir():
    return os.environ.get("CLAUDE_CONFIG_DIR") or os.path.join(os.path.expanduser("~"), ".claude")


def _json(path, default=None):
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def _frontmatter(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            text = f.read(4000)
    except OSError:
        return {}
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    if not m:
        return {}
    out = {}
    # `key: value`, or a block scalar (`key: >` / `key: |`) whose value is the indented lines that follow
    for key, value, block in re.findall(r"^(name|description):[ \t]*(.*)\n?((?:[ \t]+.*\n?)*)", m.group(1), re.M):
        value = value.strip()
        out[key] = " ".join(l.strip() for l in block.splitlines()) if value[:1] in (">", "|") else value
    return out


def profile(path):
    """What a plugin directory brings: skills, commands, agents (name, description), hook events, MCP servers and an
    always-on token estimate."""
    out = {"skills": [], "commands": [], "agents": [], "hooks": set(), "mcp": {}, "tokens": 0, "sync_stop": False}
    if not path or not os.path.isdir(path):
        return out
    for kind, pattern in (("skills", "skills/*/SKILL.md"), ("commands", "commands/*.md"), ("agents", "agents/*.md")):
        for f in sorted(glob.glob(os.path.join(path, pattern))):
            fm = _frontmatter(f)
            # unnamed: a skill is its folder's name, a command or agent its file's name without .md
            name = fm.get("name") or (os.path.basename(os.path.dirname(f)) if kind == "skills" else
                                      os.path.basename(f)[:-3])
            out[kind].append((name, fm.get("description", "")))
            out["tokens"] += (len(name) + len(fm.get("description", ""))) // 4 + 5
    manifest = _json(os.path.join(path, ".claude-plugin", "plugin.json"), {}) or {}
    for key, default in (("hooks", "hooks/hooks.json"), ("mcpServers", ".mcp.json")):
        spec = manifest.get(key, default)  # plugin.json can inline them or name another file
        data = spec if isinstance(spec, dict) else _json(os.path.join(path, spec), {}) if isinstance(spec, str) else {}
        data = data.get(key, data) if isinstance(data, dict) else {}
        if key == "hooks":
            out["hooks"] |= set(data or {})
            stops = [h for e in (data or {}).get("Stop") or [] if isinstance(e, dict)
                     for h in e.get("hooks") or [] if isinstance(h, dict)]
            # async/asyncRewake Stop hooks run after the turn ends and can't hold it open
            out["sync_stop"] |= any(not (h.get("async") or h.get("asyncRewake")) for h in stops)
        else:
            out["mcp"].update(data or {})
    return out


def _marketplace_files():
    """Each known marketplace's marketplace.json: the cached ones, and directory sources registered where they live
    (known_marketplaces.json installLocation, e.g. Foreman's own repo)."""
    files = glob.glob(os.path.join(claude_dir(), "plugins", "marketplaces", "*", ".claude-plugin", "marketplace.json"))
    known = _json(os.path.join(claude_dir(), "plugins", "known_marketplaces.json"), {}) or {}
    for entry in known.values() if isinstance(known, dict) else ():
        loc = entry.get("installLocation") if isinstance(entry, dict) else None
        if isinstance(loc, str):
            files.append(os.path.join(loc, ".claude-plugin", "marketplace.json"))
    seen, out = set(), []
    for f in files:
        real = os.path.realpath(f)
        if real not in seen and os.path.isfile(real):
            seen.add(real)
            out.append(f)
    return sorted(out)


def index():
    """Every plugin in the known marketplaces: id, description, category, and its local copy when there is one."""
    out = []
    for f in _marketplace_files():
        root, data = os.path.dirname(os.path.dirname(f)), _json(f, {}) or {}
        mk = data.get("name") or os.path.basename(root)
        for p in data.get("plugins") or []:
            src = p.get("source")
            local = os.path.normpath(os.path.join(root, src)) if isinstance(src, str) else None
            out.append({"id": f"{p.get('name')}@{mk}", "name": p.get("name", ""), "marketplace": mk,
                        "description": p.get("description", ""), "category": p.get("category", ""),
                        "local": local if local and os.path.isdir(local) else None,
                        "entry_hash": _digest(json.dumps(p, sort_keys=True).encode())})
    return out


def _digest(data):
    return hashlib.sha256(data).hexdigest()[:16]


def _tree_hash(root):
    """Every file under root (paths and contents; symlinks as their targets, never followed; .git skipped)."""
    h = hashlib.sha256()
    for d, dirs, files in os.walk(root):
        links = sorted(x for x in dirs if os.path.islink(os.path.join(d, x)))
        dirs[:] = sorted(x for x in dirs if x != ".git" and x not in links)
        for f in sorted(files) + links:
            path = os.path.join(d, f)
            h.update(os.path.relpath(path, root).encode() + b"\0")
            if os.path.islink(path):
                h.update(b"link:" + os.readlink(path).encode())
            elif os.path.isfile(path):
                try:
                    with open(path, "rb") as fh:
                        h.update(hashlib.sha256(fh.read()).digest())
                except OSError:
                    h.update(b"unreadable")  # can't vouch for it: differs from any readable content
    return h.hexdigest()[:16]


def _pin_source(pid):
    """(the code a pin on pid hashes: its installed copy, else the marketplace's local copy, or None; its marketplace
    row, None for an installed copy or an unknown plugin)."""
    have = installed().get(pid) or {}
    if have.get("path") and os.path.isdir(have["path"]):
        return have["path"], None
    known = next((p for p in index() if p["id"] == pid), None)
    return (known or {}).get("local"), known


def content_hash(pid):
    """What a yes to install or enable pid approves (T-0036): its installed copy when there is one (enable), else its
    marketplace entry plus the marketplace's local copy of it, or the entry alone for a remote source (which pins the
    code only as far as the entry names a ref or sha). None for an unknown plugin."""
    code, known = _pin_source(pid)
    if not known:
        return _tree_hash(code) if code else None
    return _digest((known["entry_hash"] + (_tree_hash(code) if code else "")).encode())


def pin_covers_code(pid):
    """Whether a pin on pid hashes code, not only a remote source's marketplace entry."""
    return bool(_pin_source(pid)[0])


def installed():
    """{id: {"path", "enabled"}} for installed plugins, enabled as Claude Code resolves it here: user settings, then
    this project's .claude/settings.json and settings.local.json."""
    data = (_json(os.path.join(claude_dir(), "plugins", "installed_plugins.json"), {}) or {}).get("plugins") or {}
    root = c.git_root(os.getcwd()) or os.getcwd()
    enabled = {}
    for f in (os.path.join(claude_dir(), "settings.json"), os.path.join(root, ".claude", "settings.json"),
              os.path.join(root, ".claude", "settings.local.json")):
        enabled.update((_json(f, {}) or {}).get("enabledPlugins") or {})
    out = {}
    for pid, entries in data.items():
        entries = [e for e in (entries if isinstance(entries, list) else [entries]) if isinstance(e, dict)]
        # a stale entry (another scope, a removed checkout) must not hide the copy that is really there
        entry = next((e for e in entries if e.get("installPath") and os.path.isdir(e["installPath"])),
                     entries[0] if entries else {})
        out[pid] = {"path": entry.get("installPath"), "enabled": bool(enabled.get(pid, False))}
    return out


def find(need, n=10):
    words = [w for w in re.findall(r"[a-z0-9+#.-]+", need.lower()) if w not in _STOP]
    if not words:
        return []
    have, hits = installed(), []
    for p in index():
        name, text = p["name"].lower(), f"{p['description']} {p['category']}".lower()
        # a short word must be a whole word ("go" is not google or mongo); longer ones may prefix ("test" → testing)
        pats = [re.compile(r"\b" + re.escape(w) + (r"\b" if len(w) <= 3 else "")) for w in words]
        score = sum(3 * bool(r.search(name)) + bool(r.search(text)) for r in pats)
        if score:
            hits.append(dict(p, score=score, installed=p["id"] in have,
                             enabled=have.get(p["id"], {}).get("enabled", False),
                             tokens=profile(p["local"] or have.get(p["id"], {}).get("path"))["tokens"]))
    return sorted(hits, key=lambda h: (-h["score"], h["id"]))[:n]


def _own_findings(pid, prof):
    """Conflicts a plugin brings on its own: a Stop hook, process skills that duplicate Foreman."""
    found = []
    if prof["sync_stop"]:
        found.append({"plugin": pid, "kind": "stop-hook", "detail": "a Stop hook that can hold the turn open: it competes with Foreman's "
                      "evidence gate and drive for when a turn may end",
                      "action": f"fm plugins disable {pid} (after fm ask ID plugin)"})
    for name, _ in prof["skills"] + prof["commands"]:
        owner = next((b for b, keys in FOREMAN_OWNS.items() if any(k in name.lower() for k in keys)), None)
        if owner:
            found.append({"plugin": pid, "kind": "overlaps-foreman", "detail": f"{name} duplicates Foreman's {owner}",
                          "action": "use Foreman's; disable the plugin if both keep triggering"})
    return found


def check(only=None):
    """Conflicts among enabled plugins and with Foreman: [{plugin, kind, detail, action}]."""
    found, mcp = [], {}
    for pid, info in sorted(installed().items()):
        if not info["enabled"] or pid.startswith("foreman@") or (only and pid != only):
            continue
        prof = profile(info["path"])
        if pid.split("@")[0] in KNOWN_CONFLICTS:
            found.append({"plugin": pid, "kind": "known-conflict", "detail": KNOWN_CONFLICTS[pid.split("@")[0]],
                          "action": f"fm plugins disable {pid} (after fm ask ID plugin)"})
        found += _own_findings(pid, prof)
        for server, spec in prof["mcp"].items():
            key = (server, json.dumps(spec, sort_keys=True))
            if server in {k[0] for k in mcp} or key in mcp:
                first = next(v for k, v in mcp.items() if k[0] == server or k == key)
                found.append({"plugin": pid, "kind": "duplicate-mcp", "detail": f"MCP server {server!r} is also "
                              f"provided by {first}", "action": f"keep one: claude plugin disable {pid} or {first}"})
            mcp.setdefault(key, pid)
    return found


# T-0205: words in a skill's name or description that say it fits a stage, for fm next's hint. Claude Code's own
# skills for a stage come after the installed ones.
STAGE_WORDS = {
    "CLEAN": ("simplif", "over-engineer", "bloat", "dead code", "refactor", "clean up", "cleanup"),
    "SECURITY": ("security", "vulnerab", "threat model", "secret scan"),
    "PERFORMANCE": ("performance", "profil", "latency"),
    "FIX": ("debug", "root cause"),
    "RESEARCH": ("research", "investigat", "library documentation"),
    "FEATURE": ("test-driven", "tdd"),
}
UI_WORDS = ("frontend", "front-end", "web interface", "user interface", "ui design")
UI_FILES = re.compile(r"\.(tsx|jsx|vue|svelte|css|scss|html)\b")
BUILTIN = {"SECURITY": ("security-review",), "CLEAN": ("simplify",)}
INDEX_VERSION = 2  # bump when what the index keeps changes


def _gist(name, desc):
    """What a skill is for: its name and its description's first sentence (later sentences list side uses: a skill
    creator "benchmarks skill performance" without being a performance tool)."""
    return f"{name} {re.split(r'(?<=[.!?])\s', desc.strip(), maxsplit=1)[0]}".lower()


def _skill_index(p):
    """[{name, text}] for the skills and commands Claude can invoke here (enabled plugins', the user's, the project's)
    and how often each was invoked in this project, cached in the project's state until the plugin registry, the
    settings or a skills folder changes, or the day does."""
    root = p.root
    watch = [os.path.join(claude_dir(), "plugins", "installed_plugins.json"), os.path.join(claude_dir(), "settings.json"),
             os.path.join(root, ".claude", "settings.json"), os.path.join(root, ".claude", "settings.local.json"),
             os.path.join(claude_dir(), "skills"), os.path.join(root, ".claude", "skills")]
    key = [INDEX_VERSION, c.now()[:10]] + [os.path.getmtime(f) if os.path.exists(f) else 0 for f in watch]
    path = os.path.join(p.dir, "skill-index.json")
    cached = _json(path, {}) or {}
    if cached.get("key") == key:
        return cached
    skills = []
    for pid, info in sorted(installed().items()):
        if info["enabled"] and not pid.startswith("foreman@"):
            prof = profile(info["path"])
            skills += [{"name": f"/{pid.split('@')[0]}:{n}", "text": _gist(n, d)} for n, d in prof["skills"] + prof["commands"]]
    for base in watch[4:]:
        for f in sorted(glob.glob(os.path.join(base, "*", "SKILL.md"))):
            fm = _frontmatter(f)
            name = fm.get("name") or os.path.basename(os.path.dirname(f))
            skills.append({"name": f"/{name}", "text": _gist(name, fm.get("description", ""))})
    uses = {}
    for e in c.tail_jsonl(os.path.join(c.state_dir(), "events.jsonl"), 5000):
        if e.get("tool") == "Skill" and e.get("kind") == "tool" and e.get("project") == p.slug:
            uses[str(e.get("target"))] = uses.get(str(e.get("target")), 0) + 1
    data = {"key": key, "skills": skills, "uses": uses}
    try:
        c.write_atomic(path, json.dumps(data))
    except OSError:
        pass
    return data


def stage_skills(p, b, n=3):
    """The installed skills that fit a task's stage, ones used before first, then Claude Code's own (T-0205)."""
    idx = _skill_index(p)
    words = STAGE_WORDS.get(b.type, ())
    ui = UI_WORDS if any(UI_FILES.search(str(s)) for s in b.meta.get("scope") or []) else ()
    owned = [k for keys in FOREMAN_OWNS.values() for k in keys]  # Foreman's own process stays Foreman's
    hits = []
    for e in idx.get("skills") or []:
        score = sum(w in e["text"] for w in words + ui)
        meta = re.search(r"skill|plugin", e["name"].lower())  # tools for authoring Claude extensions, not the work
        if score and not meta and not any(k in e["name"].lower() for k in owned):
            hits.append((-idx["uses"].get(e["name"][1:], 0), -score, e["name"]))
    names = [h[2] for h in sorted(hits)][:n]
    return names + [f"/{x}" for x in BUILTIN.get(b.type, ()) if f"/{x}" not in names][:max(0, n - len(names))]


def _manifest(key, add=None, drop=None):
    """uninstall-user's record of what fm plugins added (`plugins_installed`, `marketplaces_added`). True if changed."""
    path = os.path.join(c.state_dir(), "install-manifest.json")
    m = _json(path, {}) or {}
    old = list(m.get(key) or [])
    new = list(dict.fromkeys(x for x in old + ([add] if add else []) if x != drop))
    if new == old:
        return False
    m[key] = new
    c.write_atomic(path, json.dumps(m, indent=2) + "\n")
    return True


def _claude(*args, timeout=300):
    try:
        r = subprocess.run(["claude", *args], capture_output=True, text=True, timeout=timeout)
    except FileNotFoundError:
        raise c.PolicyError("the claude CLI isn't on PATH")
    if r.returncode != 0:
        raise c.PolicyError(f"claude {' '.join(args)} failed: {(r.stderr or r.stdout).strip()[:300]}")
    return r


def _marketplaces():
    return {(_json(f, {}) or {}).get("name") or os.path.basename(os.path.dirname(os.path.dirname(f)))
            for f in _marketplace_files()}


def add_marketplace(source):
    """Add a marketplace (GitHub owner/repo, git URL or local path); a new one is recorded for uninstall-user.
    Returns the names it added."""
    before = _marketplaces()
    _claude("plugin", "marketplace", "add", source)
    new = sorted(_marketplaces() - before)
    for name in new:
        _manifest("marketplaces_added", add=name)
    return new


def install(pid):
    """Install (or, when installed but disabled, enable) a plugin; a fresh install is recorded for uninstall-user.
    Returns (what was done, conflicts it brings)."""
    known, have = {p["id"]: p for p in index()}, installed()
    if pid not in known and pid not in have:
        return None, []
    conflicts = _own_findings(pid, profile((known.get(pid) or {}).get("local") or have.get(pid, {}).get("path")))
    fresh = pid not in have
    _claude("plugin", "install", pid, "--scope", "user") if fresh else _claude("plugin", "enable", pid)
    if fresh:
        if pid not in installed():  # exit 0 without an install (e.g. a prompt it couldn't show) owns nothing
            raise c.PolicyError(f"claude plugin install exited 0 but {pid} isn't installed")
        _manifest("plugins_installed", add=pid)
    return ("installed" if fresh else "enabled"), conflicts


def cmd_plugins(args):
    import fmcli
    if args.action in ("add-marketplace", "forget") and not args.words:
        raise fmcli.UsageError(f"fm plugins {args.action} needs " + (
            "a source (owner/repo, git URL or path)" if args.action == "add-marketplace" else "an id"))
    if args.action == "add-marketplace":
        new = add_marketplace(args.words[0])
        return print((f"Added marketplace {', '.join(new)}" if new else f"{args.words[0]} was already known")
                     + "; fm plugins find <what you need> searches it.")
    if args.action == "forget":  # uninstall-user leaves it in place
        dropped = [k for k in ("plugins_installed", "marketplaces_added") if _manifest(k, drop=args.words[0])]
        return print(f"uninstall-user will keep {args.words[0]}." if dropped else
                     f"{args.words[0]} wasn't added by fm plugins; nothing to forget.")
    if args.action in ("install", "enable", "disable"):
        pid = args.words[0] if args.words else ""
        if args.action == "disable":
            _claude("plugin", "disable", pid, timeout=120)
            return print(f"{pid} disabled (/reload-plugins to apply)")
        done, conflicts = install(pid)
        if not done:
            raise fmcli.UsageError(f"{pid!r} isn't in the known marketplaces; fm plugins find <what you need> lists them")
        return print(f"{pid} {done} (/reload-plugins to load it)." + "".join(
            f"\n  note: {f['detail']} → {f['action']}" for f in conflicts))
    if args.action == "find":
        hits = find(" ".join(args.words))
        fmcli.out(args, hits, "\n".join(
            f"{h['id']:<40} {'enabled' if h['enabled'] else 'installed' if h['installed'] else 'available':<9} "
            f"~{h['tokens']} tok  {h['description'][:70]}" for h in hits) or "No matching plugin in the known marketplaces.")
    elif args.action == "check":
        found = check(args.words[0] if args.words else None)
        fmcli.out(args, found, "\n".join(f"{f['plugin']}: {f['detail']} → {f['action']}" for f in found)
                  or "No conflicts among enabled plugins.")
