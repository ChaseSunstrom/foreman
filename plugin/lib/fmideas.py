"""fm ideas: tool-less brainstorm children, one per lens, run in parallel (skills/brainstorm).

A Claude Code subagent can't have zero tools (an empty `tools:` list means every tool), so each lens runs as a
fresh `claude -p` session with no built-in tools and no MCP servers, in a scratch directory outside any project.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import time

import fmcore as c

LENSES = ["user value", "reliability", "performance", "security and safety", "simplicity", "bold bets"]
PROMPT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      "skills", "brainstorm", "references", "ideas-prompt.md")
# No built-in tools, no MCP servers, and no user settings (so other plugins' hooks and prompts don't bias the lens).
NO_TOOLS = ["--setting-sources", "project,local", "--tools", "", "--strict-mcp-config",
            "--mcp-config", json.dumps({"mcpServers": {}})]


def child_cmd(lens, pack, model, system):
    return ["claude", "-p", "--model", model, "--no-session-persistence", *NO_TOOLS, "--append-system-prompt", system,
            f"Lens: {lens}\n\nContext pack:\n{pack}\n\nReturn 5-8 ideas in the required format."]


def cmd_ideas(args):
    import fmcli
    p = fmcli.resolve(args)
    pack = sys.stdin.read() if args.pack == "-" else open(args.pack, encoding="utf-8").read()
    lenses = list(dict.fromkeys(args.lens or LENSES))
    with open(PROMPT, encoding="utf-8") as f:
        system = f.read()
    out_dir = os.path.join(p.dir, "research", "brainstorm-" + time.strftime("%Y%m%d-%H%M%S"))
    os.makedirs(out_dir, exist_ok=True)
    results = []
    with tempfile.TemporaryDirectory(prefix="fm-ideas-", dir=os.environ.get("XDG_RUNTIME_DIR") or None) as cwd:
        procs = [(lens, subprocess.Popen(child_cmd(lens, pack, args.model, system), cwd=cwd, text=True,
                                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)) for lens in lenses]
        deadline = time.time() + args.timeout
        for lens, pr in procs:
            try:
                out, err = pr.communicate(timeout=max(1, deadline - time.time()))
                ok = pr.returncode == 0 and bool(out.strip())
                why = "" if ok else f"exit {pr.returncode}: {(err or out).strip()[-200:]}"
            except subprocess.TimeoutExpired:
                pr.kill()
                out, _ = pr.communicate()
                ok, why = False, f"timed out after {args.timeout}s"
            path = os.path.join(out_dir, re.sub(r"[^a-z0-9]+", "-", lens.lower()).strip("-") + ".md")
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"# Brainstorm — lens: {lens}\n\n" + (c.redact(out.strip()) if ok else f"FAILED: {why}") + "\n")
            results.append({"lens": lens, "file": path, "ok": ok, "error": why})
    with c.lock(p.dir):
        c.log_event(p, "ideas", data={"dir": out_dir, "lenses": lenses, "failed": [r["lens"] for r in results if not r["ok"]]},
                    session=fmcli.session())
    fmcli.out(args, {"dir": out_dir, "results": results},
              "\n".join([f"Brainstorm ideas in {out_dir}:"] + [f"  {'ok  ' if r['ok'] else 'FAIL'} {r['lens']}: {r['file'] if r['ok'] else r['error']}" for r in results]))
    failed = [r["lens"] for r in results if not r["ok"]]
    if failed:
        raise fmcli.UsageError(f"brainstorm lens(es) failed: {', '.join(failed)} (the others are saved)")
