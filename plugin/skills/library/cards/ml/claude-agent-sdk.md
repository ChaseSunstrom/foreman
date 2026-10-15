---
name: claude-agent-sdk
title: Claude Agent SDK
area: ml
tags: [claude, agents, sdk, tools, permissions, hooks]
detect: [dep:claude-agent-sdk, dep:@anthropic-ai/claude-agent-sdk]
related: [agent-loops, mcp-servers, tool-use, llm-guardrails, anthropic-sdk]
---
Build agents on the Claude Agent SDK: a managed loop with built-in tools, custom tools, permissions, hooks and subagents.

## Verify
- `pytest -q tests/test_agent.py`: custom tools and hooks work, with the model stubbed or recorded.
- `python -c "import claude_agent_sdk"`: the package imports in the target environment.
- `pytest -q -k permissions`: denied tools are refused and allowed ones run.

## Test first
Unit-test custom tool and hook logic directly; they are plain functions.
```python
import pytest
from app.hooks import block_dangerous_bash

@pytest.mark.anyio
async def test_rm_rf_is_denied():
    out = await block_dangerous_bash({"tool_name": "Bash", "tool_input": {"command": "rm -rf /"}}, None, None)
    assert out["hookSpecificOutput"]["permissionDecision"] == "deny"
```

## Do
- Pass an explicit allowed-tools list and a permission mode; start from least privilege.
- Set a system prompt, working directory and a max-turns limit on every run.
- Define custom tools as in-process MCP servers with typed schemas; return errors as tool errors.
- Use hooks (pre-tool-use, post-tool-use) for policy: block commands, log calls, redact output.
- Use subagents with narrow tool sets for isolated subtasks to keep the main context small.
- Handle the message stream: assistant text, tool use, tool results, and the final result message with cost and turns.
- Pass secrets via environment, never in prompts; run in a sandbox or container for untrusted work.

## Avoid
- A permission mode that bypasses prompts in production: any injected instruction then acts freely. Use an allowlist plus hooks.
- No turn or budget cap: loops run unbounded. Set max turns and monitor result cost.
- Granting Bash and write tools to a read-only task: restrict to Read and search tools.
- Ignoring the final result message's error subtype: failures look like empty success. Check it.
- Reading untrusted files as instructions: treat as data; tools can exfiltrate.
- Pinning to remembered option names: confirm the current ones in the installed package.

## Review
- [ ] Tools allowlisted and permission mode is least privilege.
- [ ] Turn and cost limits set.
- [ ] Hooks enforce policy for dangerous tools.
- [ ] Result subtype and cost checked and logged.
- [ ] Untrusted execution sandboxed.
