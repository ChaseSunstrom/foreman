"""fm plugins: find a capability in the known marketplaces, check enabled plugins for conflicts with Foreman and with
each other, and install one after the user's yes (guard category `plugin`, granted only through `fm ask`).

Everything is read from disk (~/.claude/plugins): marketplace indexes, their local plugin copies and the install
cache. Always-on cost is estimated from skill/agent/command descriptions (~4 characters a token).
"""
import glob
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
    "task tracking and drive": ("todo", "task-tracker", "ralph", "loop"),
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
    return dict(re.findall(r"^(name|description):\s*(.+)$", m.group(1), re.M)) if m else {}


def profile(path):
    """What a plugin directory brings: skills, commands, agents (name, description), hook events, MCP servers and an
    always-on token estimate."""
    out = {"skills": [], "commands": [], "agents": [], "hooks": set(), "mcp": {}, "tokens": 0}
    if not path or not os.path.isdir(path):
        return out
    for kind, pattern in (("skills", "skills/*/SKILL.md"), ("commands", "commands/*.md"), ("agents", "agents/*.md")):
        for f in sorted(glob.glob(os.path.join(path, pattern))):
            fm = _frontmatter(f)
            name = fm.get("name") or os.path.basename(os.path.dirname(f) if kind == "skills" else f)[:-3 if kind != "skills" else None]
            out[kind].append((name, fm.get("description", "")))
            out["tokens"] += (len(name) + len(fm.get("description", ""))) // 4 + 5
    hooks = (_json(os.path.join(path, "hooks", "hooks.json"), {}) or {}).get("hooks") or {}
    out["hooks"] = set(hooks)
    out["mcp"] = (_json(os.path.join(path, ".mcp.json"), {}) or {}).get("mcpServers") or {}
    return out


def index():
    """Every plugin in the known marketplaces: id, description, category, and its local copy when there is one."""
    out = []
    for f in sorted(glob.glob(os.path.join(claude_dir(), "plugins", "marketplaces", "*", ".claude-plugin",
                                           "marketplace.json"))):
        root, data = os.path.dirname(os.path.dirname(f)), _json(f, {}) or {}
        mk = data.get("name") or os.path.basename(root)
        for p in data.get("plugins") or []:
            src = p.get("source")
            local = os.path.normpath(os.path.join(root, src)) if isinstance(src, str) else None
            out.append({"id": f"{p.get('name')}@{mk}", "name": p.get("name", ""), "marketplace": mk,
                        "description": p.get("description", ""), "category": p.get("category", ""),
                        "local": local if local and os.path.isdir(local) else None})
    return out


def installed():
    """{id: {"path", "enabled"}} for installed plugins (enabled per the user's settings)."""
    data = (_json(os.path.join(claude_dir(), "plugins", "installed_plugins.json"), {}) or {}).get("plugins") or {}
    enabled = (_json(os.path.join(claude_dir(), "settings.json"), {}) or {}).get("enabledPlugins") or {}
    out = {}
    for pid, entries in data.items():
        entry = entries[0] if isinstance(entries, list) and entries else entries if isinstance(entries, dict) else {}
        out[pid] = {"path": entry.get("installPath"), "enabled": bool(enabled.get(pid, False))}
    return out


def find(need, n=10):
    words = [w for w in re.findall(r"[a-z0-9+#.-]+", need.lower()) if w not in _STOP]
    if not words:
        return []
    have, hits = installed(), []
    for p in index():
        name, text = p["name"].lower(), f"{p['description']} {p['category']}".lower()
        score = sum(3 * (w in name) + (w in text) for w in words)
        if score:
            hits.append(dict(p, score=score, installed=p["id"] in have,
                             enabled=have.get(p["id"], {}).get("enabled", False),
                             tokens=profile(p["local"] or have.get(p["id"], {}).get("path"))["tokens"]))
    return sorted(hits, key=lambda h: (-h["score"], h["id"]))[:n]


def check(only=None):
    """Conflicts among enabled plugins and with Foreman: [{plugin, kind, detail, action}]."""
    found, mcp = [], {}
    for pid, info in sorted(installed().items()):
        if not info["enabled"] or pid.startswith("foreman@") or (only and pid != only):
            continue
        prof = profile(info["path"])
        if "Stop" in prof["hooks"]:
            found.append({"plugin": pid, "kind": "stop-hook", "detail": "a Stop hook: it competes with Foreman's "
                          "evidence gate and drive for when a turn may end",
                          "action": f"claude plugin disable {pid} (after fm ask ID plugin)"})
        for name, _ in prof["skills"] + prof["commands"]:
            owner = next((b for b, keys in FOREMAN_OWNS.items() if any(k in name.lower() for k in keys)), None)
            if owner:
                found.append({"plugin": pid, "kind": "overlaps-foreman", "detail": f"{name} duplicates Foreman's {owner}",
                              "action": "use Foreman's; disable the plugin if both keep triggering"})
        for server, spec in prof["mcp"].items():
            key = (server, json.dumps(spec, sort_keys=True))
            if server in {k[0] for k in mcp} or key in mcp:
                first = next(v for k, v in mcp.items() if k[0] == server or k == key)
                found.append({"plugin": pid, "kind": "duplicate-mcp", "detail": f"MCP server {server!r} is also "
                              f"provided by {first}", "action": f"keep one: claude plugin disable {pid} or {first}"})
            mcp.setdefault(key, pid)
    return found


def cmd_plugins(args):
    import fmcli
    if args.action == "find":
        hits = find(" ".join(args.words))
        fmcli.out(args, hits, "\n".join(
            f"{h['id']:<40} {'enabled' if h['enabled'] else 'installed' if h['installed'] else 'available':<9} "
            f"~{h['tokens']} tok  {h['description'][:70]}" for h in hits) or "No matching plugin in the known marketplaces.")
    elif args.action == "check":
        found = check(args.words[0] if args.words else None)
        fmcli.out(args, found, "\n".join(f"{f['plugin']}: {f['detail']} → {f['action']}" for f in found)
                  or "No conflicts among enabled plugins.")
