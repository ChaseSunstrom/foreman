---
name: cc-hook-payloads
title: Hook payloads and answers
area: claude-code
tags: [claude-code, hooks, json, stdin, hookspecificoutput, exit-codes]
detect: [file:hooks/hooks.json]
related: [cc-hooks, cc-hook-security, cc-hook-performance, cc-plugin-debugging]
---
Hooks read one JSON object on stdin and answer with an exit code plus, optionally, one JSON object on stdout whose shape depends on the event.

## Verify
- `echo '{}' | hooks/hook PreToolUse; echo $?`: an empty or odd payload does not crash the hook.
- `hooks/hook PreToolUse < fixture.json | python3 -m json.tool`: stdout is exactly one valid JSON object.
- `claude --plugin-dir ./plugin --debug`: shows the hook command, exit code and parsed output.

## Test first
Pin the answer shape per event.
```python
import json, subprocess
def answer(event, payload):
    r = subprocess.run(["hooks/hook", event], input=json.dumps(payload), capture_output=True, text=True)
    return r.returncode, (json.loads(r.stdout) if r.stdout.strip() else None)
def test_pre_tool_use_uses_hook_specific_output():
    rc, out = answer("PreToolUse", {"tool_name": "Bash", "tool_input": {"command": "rm -rf /"}})
    assert out["hookSpecificOutput"]["hookEventName"] == "PreToolUse"
```

## Do
- Common input fields: `session_id`, `transcript_path`, `cwd`, `permission_mode`, `hook_event_name`; tool events add `tool_name`, `tool_input`, `tool_use_id`.
- PreToolUse answer: `{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "allow|deny|ask|defer", "permissionDecisionReason": "..."}}`; `updatedInput` there rewrites arguments.
- PostToolUse, Stop, SubagentStop and UserPromptSubmit block with top-level `{"decision": "block", "reason": "..."}`.
- Add context with `hookSpecificOutput.additionalContext` (capped at 10,000 characters); plain stdout reaches Claude only for `UserPromptSubmit`, `SessionStart` and a few others.
- Universal fields: `continue`, `stopReason`, `systemMessage`.
- Read defensively: `(payload.get("tool_input") or {}).get("command", "")`.
- Exit 0 means the JSON is read; exit 2 means stderr is the reason; any other code is a non-blocking error.

## Avoid
- Top-level `{"permissionDecision": ...}` for PreToolUse: wrong shape, ignored. Nest it under `hookSpecificOutput` with `hookEventName`.
- `decision: "block"` for PreToolUse: use `permissionDecision: "deny"`.
- Printing two JSON objects or text plus JSON: parse fails. Emit one object and nothing else.
- Indexing `payload["tool_input"]["command"]` directly: a Write or Read call has no `command`. Use `.get` chains.
- Expecting UserPromptSubmit to rewrite the prompt: it can only block or add context.
- Exit 2 combined with a JSON decision: exit 2 wins and stdout is ignored.

## Review
- [ ] Each event's answer shape matches the list above.
- [ ] Missing or null fields never raise.
- [ ] Only one JSON object reaches stdout; logs go to stderr.
- [ ] Context additions stay well under the cap.
