---
name: cc-mcp-config
title: MCP server configuration
area: claude-code
tags: [claude-code, mcp, mcp-json, stdio, http, tools]
detect: [file:.mcp.json]
related: [cc-plugins, cc-plugin-manifest, cc-hook-security, cc-context-budget, cc-headless]
---
`.mcp.json` declares MCP servers by name under `mcpServers`; plugins ship the same file at the plugin root.

## Verify
- `claude mcp list`: servers and their connection status.
- `claude mcp get <name>`: the resolved entry and its scope.
- `python3 -m json.tool .mcp.json`: parses.
- `claude plugin validate .`: checks plugin MCP entries (needs Claude Code 2.1.281 or later), including unknown `${user_config.KEY}` and bad URLs.

## Test first
Prove the server answers before wiring Claude to it.
```bash
printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | ./server.js | head -1 | python3 -m json.tool
```
Then assert a headless run sees it: `claude -p "ping" --output-format stream-json --verbose` and check `mcp_servers` in the `system/init` event for status `connected`.

## Do
- To expose a CLI as tools, start from `fm mcp new NAME --wrap 'CMD' [--sub a,b]`: a stdlib server (argv only, validated arguments, a timeout, an output cap) and a test that drives it over stdio; `fm mcp register claude DIR` prints the add line.
- Shape: `{"mcpServers": {"name": {"type": "stdio", "command": "node", "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"], "env": {...}}}}`.
- Remote servers: `"type": "http", "url": "...", "headers": {...}`; use `http` over `sse`, which is deprecated.
- Put secrets in the environment and reference `${VAR}` or `${VAR:-default}` (expanded in `command`, `args`, `env`, `url`, `headers`); in plugins use `userConfig` with `sensitive: true`.
- Scopes: local (default), `project` (`.mcp.json`, shared), `user`; add with `claude mcp add --transport http <name> <url>`.
- Match tools by their full name: `mcp__<server>__<tool>`, and for plugin servers `mcp__plugin_<plugin>_<server>__<tool>`.
- Set `timeout` per server (milliseconds) for slow tools; `MCP_TIMEOUT` controls startup.
- Keep tool results small; output over 10,000 tokens warns and 25,000 is the default cap.

## Avoid
- A `url` entry without `type`: read as stdio and skipped. Always set `type`.
- `http://` URLs to non-loopback hosts, or literal tokens in headers: flagged by validate. Use https and variables.
- Credential-named variables (such as `ANTHROPIC_API_KEY`) in a remote `url` or `headers`: they expand to empty. Use another variable name.
- Matching a plugin server by its bare key in hooks or permissions: it never matches. Use the `mcp__plugin_...` name.
- Writing to stdout from a stdio server for logs: it breaks the protocol. Log to stderr.
- Trusting project `.mcp.json` in `-p` runs: it loads without a prompt. Use `--bare` or `--strict-mcp-config` in CI.

## Review
- [ ] Every entry has `type`.
- [ ] No literal secrets; variables or `userConfig` only.
- [ ] Tool outputs are bounded.
- [ ] Permission rules name the full tool.
- [ ] CI uses explicit `--mcp-config`.
