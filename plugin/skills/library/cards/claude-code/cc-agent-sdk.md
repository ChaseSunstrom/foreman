---
name: cc-agent-sdk
title: Claude Agent SDK
area: claude-code
tags: [claude-code, agent-sdk, typescript, python, query, agents]
detect: [dep:@anthropic-ai/claude-agent-sdk, dep:claude-agent-sdk]
related: [cc-headless, cc-settings-permissions, cc-hook-payloads, cc-subagents, cc-mcp-config]
---
The Agent SDK runs Claude Code's agent loop from TypeScript (`@anthropic-ai/claude-agent-sdk`) or Python (`claude-agent-sdk`) through `query()`.

## Verify
- `npx tsc --noEmit`: options and message types check (TypeScript).
- `pyright` or `mypy .`: types for `ClaudeAgentOptions` (Python).
- `python -c "import claude_agent_sdk"`: installed in the active venv.
- `pytest -q` or `npx vitest run`: your agent tests, with the model stubbed or a capped live smoke test.

## Test first
Keep result handling a pure function of the message fields and test it; add one capped live run.
```python
from types import SimpleNamespace as NS
def outcome(msg):
    ok = msg.subtype == "success" and not msg.is_error and msg.terminal_reason == "completed"
    return msg.result if ok else None
def test_failed_final_request_is_not_success():
    msg = NS(subtype="success", is_error=True, terminal_reason="api_error", result="partial")
    assert outcome(msg) is None
```

## Do
- TypeScript: `for await (const m of query({ prompt, options })) { if (m.type === "result") ... }`. Python: `async for message in query(prompt=..., options=ClaudeAgentOptions(...))`.
- Use `ClaudeSDKClient` for multi-turn sessions and interrupts; `query()` for one-offs.
- Choose tools with `allowedTools` (or `allowed_tools`), which pre-approves them; remove tools with `disallowed_tools`.
- Set `permissionMode`, `maxTurns` and `max_budget_usd` on every unattended run.
- Pass `systemPrompt: { type: "preset", preset: "claude_code", append }` to keep Claude Code's prompt; omit it and you get a minimal one.
- Control config loading with `settingSources` (`[]` for none); skills, memory and settings otherwise load from disk.
- Gate calls with PreToolUse hook callbacks; `canUseTool` runs only when the flow would prompt.
- On results check `terminal_reason` and `subtype`, read `total_cost_usd`, and use `model_usage` for full accounting.
- Authenticate with an API key, not a claude.ai login.

## Avoid
- Treating `allowedTools` as a whitelist: it only auto-approves. Deny with rules or `disallowedTools`.
- Relying on `canUseTool` for security: auto-approved calls bypass it. Use hooks.
- Breaking out of the message loop early in Python: let it finish or use a flag.
- Assuming `subtype == "success"` means success: a failed final request reports it. Check `is_error` and `terminal_reason`.
- Unbounded loops with no `maxTurns` or budget.
- Loading the host's user settings in a service: pass `settingSources: ["project"]` or `[]`.

## Review
- [ ] Turn and budget limits are set.
- [ ] Permission mode and tool lists are explicit.
- [ ] Result errors are handled via `is_error` and `terminal_reason`.
- [ ] Setting sources are chosen on purpose.
- [ ] Auth uses an API key from the environment.
