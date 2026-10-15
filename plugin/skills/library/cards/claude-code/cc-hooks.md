---
name: cc-hooks
title: Claude Code hooks
area: claude-code
tags: [claude-code, hooks, pretooluse, posttooluse, stop, automation]
detect: [file:hooks/hooks.json]
related: [cc-hook-payloads, cc-hook-security, cc-hook-performance, cc-plugins, cc-settings-permissions]
---
Hooks run your command on Claude Code events; exit code and one JSON object on stdout decide what happens next.

## Verify
- `python3 -m json.tool hooks/hooks.json`: the file parses (the event map sits under a top-level `"hooks"` key).
- `claude plugin validate .`: warns on an unquoted `${CLAUDE_PLUGIN_ROOT}` in a shell-form command.
- `echo '<payload json>' | hooks/hook PreToolUse; echo $?`: a fixture payload gives the expected JSON and exit code.
- `/hooks` in a session: lists what loaded.

## Test first
Feed a payload on stdin; assert exit code and stdout.
```python
import json, subprocess
def run(payload):
    p = subprocess.run(["hooks/hook", "PreToolUse"], input=json.dumps(payload), capture_output=True, text=True)
    return p.returncode, p.stdout
def test_force_push_denied():
    rc, out = run({"hook_event_name": "PreToolUse", "tool_name": "Bash",
                   "tool_input": {"command": "git push --force origin main"}})
    assert json.loads(out)["hookSpecificOutput"]["permissionDecision"] == "deny"
```

## Do
- Shape: `{"hooks": {"Event": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "...", "timeout": 5}]}]}}`.
- Prefer exec form: `"command": "${CLAUDE_PLUGIN_ROOT}/hooks/hook", "args": ["PreToolUse"]` so paths need no quoting.
- Handler types: `command`, `http`, `mcp_tool`, `prompt`, `agent`. Use `command` for anything deterministic.
- Narrow with `matcher` (exact names or `A|B`; any other character makes it a regex) and with `if` (one permission rule such as `Bash(git *)`).
- `timeout` is in seconds; set it low for tool-path hooks.
- Block with exit 2 plus stderr, or exit 0 plus JSON; do not mix them, exit 2 overrides JSON.
- MCP tools are `mcp__server__tool`; match a server with `mcp__server__.*`.

## Avoid
- Exit 1 to block: non-blocking, the action proceeds. Use exit 2, or `onFailure: "block"` (2.1.295 and later) for a fail-closed guard.
- Printing logs to stdout from an exit-0 hook: stdout is parsed as JSON. Log to stderr.
- A hooks file without the `"hooks"` wrapper: it fails to load.
- Matchers on `UserPromptSubmit` or `Stop`: ignored. Filter inside the script.
- Assuming sequential order: matching hooks run in parallel, so they cannot depend on each other.
- A `Stop` hook that always blocks: it loops. Check `stop_hook_active` in the payload.

## Review
- [ ] Every event has a fixture test for allow and block.
- [ ] Blocking paths use exit 2 or a documented JSON decision.
- [ ] Matchers are as narrow as the need.
- [ ] Timeouts are explicit.
- [ ] A broken script cannot block the user unless it is meant to.
