---
name: cc-context-budget
title: Context budget for extensions
area: claude-code
tags: [claude-code, context, tokens, budget, descriptions, injection]
detect: []
related: [cc-skill-descriptions, cc-claude-md-rules, cc-hook-performance, cc-mcp-config, cc-output-styles]
---
Everything a plugin adds to every session or turn (descriptions, injected context, rules, tool lists) is paid repeatedly, so budget it like latency.

## Verify
- `/context` in a session: where the context goes (system, tools, memory, skills, messages).
- `wc -c skills/*/SKILL.md agents/*.md output-styles/*.md`: sizes of what may load.
- `awk '/^description:/{print length($0), FILENAME}' skills/*/SKILL.md agents/*.md | sort -n`: listing cost per component.
- `echo '<SessionStart payload>' | hooks/hook SessionStart | wc -c`: bytes your hook injects at start.

## Test first
Put the budget in a test.
```python
import json, subprocess
def test_session_start_context_budget():
    out = subprocess.run(["hooks/hook", "SessionStart"], input="{}", capture_output=True, text=True).stdout
    ctx = (json.loads(out).get("hookSpecificOutput") or {}).get("additionalContext", "") if out.strip() else ""
    assert len(ctx) <= 2000
```

## Do
- Descriptions are always loaded; the combined `description` and `when_to_use` are truncated at 1,536 characters. Aim for a few hundred, trigger first.
- Skill bodies load on invoke and then stay; keep `SKILL.md` under about 500 lines and split reference files.
- Use `disable-model-invocation: true` for rarely used, side-effecting skills.
- `additionalContext` and plain hook stdout are capped at 10,000 characters; keep per-prompt injection to a few hundred.
- CLAUDE.md under about 200 lines; path-scope the rest in `.claude/rules/` with `paths`; imports do not reduce cost.
- Keep MCP tool results bounded (warning above 10,000 tokens, 25,000 default cap).
- Run noisy work in a subagent or a forked skill so only its summary returns.
- Compact between tasks; every turn re-reads the whole context.

## Avoid
- Many always-on skills with overlapping descriptions: each is listing cost. Merge them or add `paths`.
- Injecting the same status text on every prompt: pay once at session start, then only deltas.
- Large `additionalContext` from PostToolUse hooks: it accumulates per call. Send short notes.
- MCP servers with dozens of tools and verbose schemas: tool definitions cost every turn. Enable only what is needed.
- Big instructions in output styles: they ride on each request.
- Measuring by feel: use `/context` and byte counts.

## Review
- [ ] Every description has its trigger in the first line and is short.
- [ ] Session-start and per-prompt injections have a tested character cap.
- [ ] Rare skills are not auto-invocable.
- [ ] Instruction files are trimmed and path-scoped.
- [ ] Noisy output is delegated to subagents.
