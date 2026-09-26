"""fm install-user / uninstall-user: wire Foreman into ~/.claude and undo it exactly.

Every change is recorded with its original value in state/install-manifest.json; uninstall reverses only what
Foreman added and still owns (a value the user changed afterwards is left alone). Writes are atomic, and
~/.claude/settings.json is backed up to FOREMAN_HOME/backups before each change.
"""
import copy
import json
import os
import re
import shutil
import time

import fmcore as c

DENY_RULES = [
    "Bash(rm -rf /)", "Bash(rm -rf /*)", "Bash(rm -rf ~)", "Bash(rm -rf ~/)", "Bash(rm -rf ~/*)",
    "Bash(rm -rf $HOME)", "Bash(rm -rf $HOME/*)", "Bash(rm -fr /)", "Bash(rm -fr ~)",
    "Bash(mkfs *)", "Bash(mkfs.* *)", "Bash(dd * of=/dev/*)",
    "Bash(git push --force * main)", "Bash(git push -f * main)", "Bash(git push --force * master)", "Bash(git push -f * master)",
    "Edit(~/.ssh/**)", "Edit(~/.gnupg/**)", "Edit(~/.aws/credentials)", "Edit(~/.claude/.credentials.json)",
]
STOP_CAP = "60"  # drive mode: allow long queues past Claude Code's default 8 consecutive Stop-hook continuations
COMPACT_PCT = "70"  # compact earlier than the default: PreCompact checkpoints and SessionStart re-injects the task
ENV = {"CLAUDE_CODE_STOP_HOOK_BLOCK_CAP": STOP_CAP, "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": COMPACT_PCT}
WHY = {"CLAUDE_CODE_STOP_HOOK_BLOCK_CAP": "drive mode: long queues aren't cut at 8 continuations",
       "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "compact before long contexts degrade; Foreman state survives compaction"}
BEGIN, END = "<!-- foreman:begin -->", "<!-- foreman:end -->"
BLOCK = (f"{BEGIN}\n# Foreman\nForeman is installed. Operating rules: ~/.claude/rules/foreman.md. "
         f"System map: ~/.claude/foreman/MASTER.md.\n{END}\n")
STATUSLINE_KEEP = ("padding", "refreshInterval", "hideVimModeIndicator")


class SetupError(Exception):
    pass


def paths():
    claude = os.path.join(os.path.expanduser("~"), ".claude")
    fh = c.foreman_home()
    return {"settings": os.path.join(claude, "settings.json"), "claude_md": os.path.join(claude, "CLAUDE.md"),
            "rules_link": os.path.join(claude, "rules", "foreman.md"),
            "rules_target": os.path.join(fh, "plugin", "rules", "foreman.md"),
            "wrapper": os.path.join(fh, "plugin", "hooks", "statusline"),
            "manifest": os.path.join(c.state_dir(), "install-manifest.json"), "backups": os.path.join(fh, "backups")}


def _load(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default


def _read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None


def _backup(P):
    if os.path.exists(P["settings"]):
        os.makedirs(P["backups"], exist_ok=True)
        shutil.copy2(P["settings"], os.path.join(P["backups"], f"settings.json.{time.strftime('%Y%m%d-%H%M%S')}"))


def _link_state(P):
    link = P["rules_link"]
    if os.path.islink(link):
        return "ours" if os.path.realpath(link) == os.path.realpath(P["rules_target"]) else "foreign"
    return "foreign" if os.path.exists(link) else "absent"


# ---------------------------------------------------------------- install

def plan_install(P):
    s = _load(P["settings"], None)
    m = _load(P["manifest"], {})
    settings_created = s is None
    s = {} if s is None else s
    new_s, new_m, actions = copy.deepcopy(s), copy.deepcopy(m), []
    new_m.setdefault("settings_created", settings_created)

    sl = new_s.get("statusLine") or {}
    if sl.get("command") != P["wrapper"]:
        new_m.setdefault("statusLine_original", sl or None)
        new_s["statusLine"] = dict({k: sl[k] for k in STATUSLINE_KEEP if k in sl}, type="command", command=P["wrapper"])
        actions.append(f"statusLine → {P['wrapper']} (original saved; it still renders above the Foreman line)")
    new_m.setdefault("statusline_hud", True)

    perms_existed = "permissions" in new_s
    perms = new_s.setdefault("permissions", {})
    new_m.setdefault("permissions_created", not perms_existed)
    new_m.setdefault("defaultMode_original", perms.get("defaultMode"))
    deny_existed = "deny" in perms
    deny = perms.setdefault("deny", [])
    new_m.setdefault("deny_created", not deny_existed)
    added = [r for r in DENY_RULES if r not in deny]
    if added:
        deny.extend(added)
        new_m["deny_added"] = list(dict.fromkeys(new_m.get("deny_added", []) + added))
        actions.append(f"permissions.deny += {len(added)} catastrophic-command rules")
    elif not deny_existed:
        perms.pop("deny")

    env_existed = "env" in new_s
    env = new_s.setdefault("env", {})
    new_m.setdefault("env_created", not env_existed)
    for k, v in ENV.items():
        if k not in env:
            env[k] = v
            new_m.setdefault("env_added", {})[k] = v
            actions.append(f"env.{k}={v} ({WHY[k]})")
    if not env and not env_existed:
        new_s.pop("env")

    md = _read(P["claude_md"])
    new_md = md
    if md is None or BEGIN not in md:
        sep = "" if not md or md.endswith("\n") else "\n"
        new_md = (md or "") + sep + BLOCK
        new_m["claude_md_block"] = True
        new_m["claude_md_sep"] = sep
        new_m.setdefault("claude_md_created", md is None)
        actions.append("~/.claude/CLAUDE.md += Foreman block (between foreman:begin/end markers)")

    link = _link_state(P)
    if link == "foreign":
        raise SetupError(f"{P['rules_link']} exists and isn't Foreman's symlink; move it aside and re-run")
    if link == "absent":
        new_m["rules_symlink"] = P["rules_link"]
        actions.append(f"{P['rules_link']} → {P['rules_target']} (symlink)")
    return s, new_s, m, new_m, md, new_md, link, actions


def cmd_install(args):
    P = paths()
    if getattr(args, "record_disabled", None):
        m = _load(P["manifest"], {})
        m["plugins_disabled"] = list(dict.fromkeys(m.get("plugins_disabled", []) + args.record_disabled))
        c.write_atomic(P["manifest"], json.dumps(m, indent=2, sort_keys=True) + "\n")
        print("Recorded disabled plugins: " + ", ".join(m["plugins_disabled"]))
        return
    try:
        s, new_s, m, new_m, md, new_md, link, actions = plan_install(P)
    except SetupError as e:
        raise _usage(str(e))
    if not actions:
        print("Foreman is already wired into ~/.claude; nothing to do.")
        return
    if args.dry_run:
        print("Would change:\n  - " + "\n  - ".join(actions))
        return
    _backup(P)
    os.makedirs(os.path.dirname(P["settings"]), exist_ok=True)
    if new_s != s or new_m.get("settings_created"):
        c.write_atomic(P["settings"], json.dumps(new_s, indent=2) + "\n")
    if new_md != md:
        c.write_atomic(P["claude_md"], new_md)
    if link == "absent":
        os.makedirs(os.path.dirname(P["rules_link"]), exist_ok=True)
        os.symlink(P["rules_target"], P["rules_link"])
    new_m.setdefault("installed", c.now())
    c.write_atomic(P["manifest"], json.dumps(new_m, indent=2, sort_keys=True) + "\n")
    print("Wired Foreman into ~/.claude:\n  - " + "\n  - ".join(actions) +
          f"\nBackup of settings.json in {P['backups']}. Undo with: fm uninstall-user")


# ---------------------------------------------------------------- uninstall

def cmd_uninstall(args):
    P = paths()
    m = _load(P["manifest"], None)
    if m is None:
        print("No Foreman install manifest; nothing to undo.")
        return
    s = _load(P["settings"], {})
    new_s, actions = copy.deepcopy(s), []
    if (new_s.get("statusLine") or {}).get("command") == P["wrapper"]:
        if m.get("statusLine_original"):
            new_s["statusLine"] = m["statusLine_original"]
        else:
            new_s.pop("statusLine")
        actions.append("statusLine restored")
    perms = new_s.get("permissions")
    if isinstance(perms, dict):
        if "deny" in perms:
            ours = set(m.get("deny_added", []))
            perms["deny"] = [r for r in perms["deny"] if r not in ours]
            if not perms["deny"] and m.get("deny_created"):
                perms.pop("deny")
            actions.append("deny rules removed")
        if "defaultMode_original" in m:
            if m["defaultMode_original"] is None:
                perms.pop("defaultMode", None)
            else:
                perms["defaultMode"] = m["defaultMode_original"]
            actions.append(f"permissions.defaultMode = {m['defaultMode_original']}")
        if not perms and m.get("permissions_created"):
            new_s.pop("permissions")
    env = new_s.get("env")
    if isinstance(env, dict):
        for k, v in (m.get("env_added") or {}).items():
            if env.get(k) == v:
                env.pop(k)
        if not env and m.get("env_created"):
            new_s.pop("env")
    md = _read(P["claude_md"])
    new_md = md
    if md is not None and BEGIN in md:
        new_md = re.sub(re.escape(m.get("claude_md_sep", "")) + re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n?", "", md,
                        count=1, flags=re.S)
        actions.append("CLAUDE.md block removed")
    if args.dry_run:
        print("Would change:\n  - " + "\n  - ".join(actions + ["rules symlink removed", "manifest removed"]))
        return
    _backup(P)
    if m.get("settings_created") and not new_s:
        os.remove(P["settings"])
    elif new_s != s:
        c.write_atomic(P["settings"], json.dumps(new_s, indent=2) + "\n")
    if new_md != md:
        if not new_md and m.get("claude_md_created"):
            os.remove(P["claude_md"])
        else:
            c.write_atomic(P["claude_md"], new_md)
    if _link_state(P) == "ours":
        os.unlink(P["rules_link"])
        actions.append("rules symlink removed")
    os.remove(P["manifest"])
    print("Removed Foreman's wiring from ~/.claude:\n  - " + "\n  - ".join(actions))


def _usage(msg):
    import fmcli
    return fmcli.UsageError(msg)
