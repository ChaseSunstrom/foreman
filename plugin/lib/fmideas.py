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
DEFAULT_LENSES = ["user value", "reliability", "simplicity", "bold bets"]  # T-0061: the rest on request
PROMPT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      "skills", "brainstorm", "references", "ideas-prompt.md")
# No built-in tools, no MCP servers, and no user settings (so other plugins' hooks and prompts don't bias the lens).
NO_TOOLS = ["--setting-sources", "project,local", "--tools", "", "--strict-mcp-config",
            "--mcp-config", json.dumps({"mcpServers": {}})]


def child_cmd(model, system):
    """The prompt (lens + pack) goes in on stdin: packs can exceed the per-argument size limit."""
    return ["claude", "-p", "--model", model, "--no-session-persistence", *NO_TOOLS, "--append-system-prompt", system]


def child_prompt(lens, pack):
    return f"Lens: {lens}\n\nContext pack:\n{pack}\n\nReturn 5-8 ideas in the required format."


_TITLE = re.compile(r"(?m)^\s*[-*]\s*\*\*(.+?)\*\*")
_WORD = re.compile(r"[a-z0-9]{3,}")


def _words(title):
    return {w[:5] for w in _WORD.findall(title.lower())}


def _is_new(title, seen):
    """Not a near-repeat of an idea already on the list (most of its words shared)."""
    w = _words(title)
    return bool(w) and all(len(w & s) / len(w | s) < 0.6 for s in seen)


def later_round_pack(pack, titles, n):
    return (pack + "\n\n## Ideas so far (don't repeat these; go past them)\n" + "\n".join(f"- {t}" for t in titles)
            + f"\n\nRound {n}: propose only NEW ideas: gaps nobody covered, second-order improvements on the ideas "
              f"above, combinations worth more together, and what a genuinely fully featured version would still lack.")


def _run_round(lenses, pack, system, args, out_dir, prefix, fmcli):
    results = []
    with tempfile.TemporaryDirectory(prefix="fm-ideas-", dir=os.environ.get("XDG_RUNTIME_DIR") or None) as cwd:
        procs = []
        try:
            for lens in lenses:
                pr = subprocess.Popen(child_cmd(args.model, system), cwd=cwd, text=True, stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                procs.append((lens, pr))
                pr.stdin.write(child_prompt(lens, pack))
                pr.stdin.close()
        except OSError as e:
            for _, pr in procs:
                pr.kill()
                pr.communicate()
            raise fmcli.UsageError(f"can't start the brainstorm children: {e} (is `claude` on PATH and logged in?)")
        deadline = time.time() + args.timeout
        for i, (lens, pr) in enumerate(procs, 1):
            try:
                out, err = pr.communicate(timeout=max(1, deadline - time.time()))
                ok = pr.returncode == 0 and bool(out.strip())
                why = "" if ok else f"exit {pr.returncode}: {(err or out).strip()[-200:]}"
            except subprocess.TimeoutExpired:
                pr.kill()
                out, _ = pr.communicate()
                ok, why = False, f"timed out after {args.timeout}s"
            slug = re.sub(r"[^a-z0-9]+", "-", lens.lower()).strip("-") or "lens"
            path = os.path.join(out_dir, f"{prefix}{i:02d}-{slug}.md")
            text = c.redact(out.strip()) if ok else ""
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"# Brainstorm — lens: {lens}\n\n" + (text if ok else f"FAILED: {why}") + "\n")
            results.append({"lens": lens, "file": path, "ok": ok, "error": why,
                            "titles": [c.plain(t).strip() for t in _TITLE.findall(text)]})
    return results


def cmd_ideas(args):
    """One round of lenses, or a super brainstorm (--rounds N): each later round sees every idea so far and is asked
    only for new ones; it stops when a round adds fewer than --dry new ideas (T-0071)."""
    import fmcli
    p = fmcli.resolve(args)
    pack = sys.stdin.read() if args.pack == "-" else open(args.pack, encoding="utf-8").read()
    lenses = list(dict.fromkeys(args.lens or DEFAULT_LENSES))
    with open(PROMPT, encoding="utf-8") as f:
        system = f.read()
    out_dir = os.path.join(p.dir, "research", "brainstorm-" + time.strftime("%Y%m%d-%H%M%S"))
    os.makedirs(out_dir, exist_ok=True)
    results, titles, seen, by_round, rounds = [], [], [], [], 0
    for n in range(1, max(1, args.rounds) + 1):
        rounds = n
        prefix = f"r{n}-" if args.rounds > 1 else ""
        got = _run_round(lenses, pack if n == 1 else later_round_pack(pack, titles, n), system, args, out_dir,
                         prefix, fmcli)
        results += [dict(r, round=n) for r in got]
        new = []
        for t in (t for r in got for t in r["titles"]):
            if _is_new(t, seen):
                seen.append(_words(t))
                new.append(t)
        titles += new
        by_round.append(new)
        if n > 1 and len(new) < args.dry:
            break
    with open(os.path.join(out_dir, "ideas.md"), "w", encoding="utf-8") as f:
        f.write("# Ideas by round (deduplicated titles; details in the lens files)\n"
                + "".join(f"\n## Round {i}\n" + "".join(f"- {t}\n" for t in ts) for i, ts in enumerate(by_round, 1)))
    failed = [f"{r['lens']} (round {r['round']})" for r in results if not r["ok"]]
    with c.lock(p.dir):
        c.log_event(p, "ideas", data={"dir": out_dir, "lenses": lenses, "rounds": rounds, "ideas": len(titles),
                                      "failed": failed}, session=fmcli.session())
    fmcli.out(args, {"dir": out_dir, "rounds": rounds, "ideas": len(titles), "results": results},
              f"Brainstorm ideas in {out_dir} ({len(titles)} distinct over {rounds} round(s); index: ideas.md):\n"
              + "\n".join(f"  {'ok  ' if r['ok'] else 'FAIL'} {'r' + str(r['round']) + ' ' if args.rounds > 1 else ''}"
                          f"{r['lens']}: {r['file'] if r['ok'] else r['error']}" for r in results)
              + (f"\n  dry after round {rounds}: it added {len(by_round[-1])} new" if rounds < args.rounds else ""))
    if failed:
        raise fmcli.UsageError(f"brainstorm lens(es) failed: {', '.join(failed)} (the others are saved)")
