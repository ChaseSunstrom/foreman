---
name: cc-plugin-debugging
title: Debugging plugins
area: claude-code
tags: [claude-code, debugging, plugin, hooks, logs, validate]
detect: []
related: [cc-plugins, cc-hooks, cc-hook-payloads, cc-plugin-testing, cc-mcp-config]
---
Debug a plugin from the outside in: does it load, did the component register, did the event fire, what did the script receive and return.

## Verify
- `claude plugin validate --strict .`: load-time problems with their fixes.
- `claude plugin list`: installed plugins and warnings, such as a default folder ignored by a manifest key.
- `claude --plugin-dir ./plugin --debug`: loading, hook runs, exit codes and parsed output in the debug log.
- `/plugin` (Errors tab), `/hooks`, `/mcp`, `/permissions` in a session: what loaded and from where.
- `claude mcp list`: MCP server status.

## Test first
Reproduce with a saved payload before changing code.
```bash
echo "$PAYLOAD" > /tmp/payload.json
hooks/hook PreToolUse < /tmp/payload.json; echo "exit=$?"
```
Make that the failing case, fix the script, rerun, then confirm in a live session.

## Do
- Start with `claude plugin validate`; most failures (paths, wrapper keys, strict objects) are reported there with a message.
- Capture real payloads: write `cat > /tmp/last-payload.json` in a temporary debug hook, then replay with the script directly.
- Log to a file or stderr inside the script, never stdout on exit-0 hooks.
- After editing a plugin loaded from disk, run `/reload-plugins` or restart; hooks in `settings.json` snapshot at session start.
- Use `claude -p ... --output-format stream-json --verbose` and read the `system/init` event: `plugins`, `plugin_errors`, `mcp_servers`, `mcp_server_errors`.
- Check matcher syntax: exact names or `A|B` for plain words, regex otherwise; MCP tools need the full `mcp__server__tool` name.
- Confirm environment: `${CLAUDE_PLUGIN_ROOT}` exists in hook, MCP and LSP processes but not in Bash tool commands.
- Bisect by disabling hooks or components one at a time.

## Avoid
- Editing code with no reproducer: you cannot tell a fix from luck. Save the payload first.
- Assuming the hook ran: a wrong matcher, a missing `hooks` wrapper or an `if` rule that does not fit silently skips it. Check `/hooks` and the debug log.
- Reading exit 1 as a block: it is non-blocking. Only exit 2 blocks.
- Debug prints on stdout: they corrupt the JSON answer. Use stderr.
- Testing with a stale session: changes do not apply until reload. Reload, then retest.
- Ignoring warnings: unknown top-level fields are stripped and the feature quietly disappears.

## Review
- [ ] Validate output is clean.
- [ ] A saved payload reproduces the issue outside Claude Code.
- [ ] A regression test now covers it.
- [ ] Debug output is removed or on stderr.
- [ ] A fresh session shows the fix.
