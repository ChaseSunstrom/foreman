---
name: mcp-servers
title: MCP servers
area: ml
tags: [mcp, tools, protocol, llm, server, stdio]
detect: [dep:mcp, dep:@modelcontextprotocol/sdk, dep:fastmcp]
related: [tool-use, claude-agent-sdk, agent-loops, llm-guardrails]
---
Model Context Protocol servers expose tools, resources and prompts to LLM clients; keep them typed, narrow and safe on stdio or HTTP.

## Verify
- `npx @modelcontextprotocol/inspector <server command>`: lists tools and lets you call them interactively.
- `pytest -q tests/test_server.py`: tools are exercised in process through the SDK client.
- `python server.py < /dev/null`: the server starts and exits cleanly on closed stdin.

## Test first
Call the tool through a client session, not the bare function.
```python
import pytest
from app.server import mcp

@pytest.mark.anyio
async def test_tool_rejects_path_escape():
    res = await mcp.call_tool("read_note", {"path": "../../etc/passwd"})
    assert "outside" in str(res).lower()
```

## Do
- Give each tool a precise name, a description that says when to use it, and typed parameters so the generated JSON Schema is tight.
- Keep tools few and task-shaped; return compact, structured results with only what the model needs.
- On stdio, write protocol messages to stdout only and logs to stderr.
- Validate and normalise all inputs (paths, ids, URLs) server-side; enforce an allowlist root.
- Report failures as tool errors with an actionable message, not stack traces.
- Authenticate remote (HTTP) servers and scope tokens per tool; never expose a server unauthenticated.
- Mark read-only tools and require confirmation on the client for mutating ones.

## Avoid
- `print()` debugging on a stdio server: it corrupts the JSON-RPC stream. Log to stderr.
- One mega-tool taking free-form commands: model misuse and injection. Split into narrow typed tools.
- Returning whole files or tables: blows context. Paginate and cap output.
- Trusting tool arguments: the model is steerable by untrusted content. Validate like web input.
- Secrets in tool descriptions or results: they reach the model and logs.
- Hard-coding absolute paths or credentials in the server: read from env or config.

## Review
- [ ] Every tool has a clear description and strict schema.
- [ ] Inputs validated; filesystem and network access constrained.
- [ ] stdout carries protocol only.
- [ ] Output size is bounded and paginated.
- [ ] Remote transport authenticated; mutating tools gated.
