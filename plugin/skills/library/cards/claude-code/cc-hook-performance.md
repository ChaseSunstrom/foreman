---
name: cc-hook-performance
title: Hook performance
area: claude-code
tags: [claude-code, hooks, latency, async, timeout, startup]
detect: [file:hooks/hooks.json]
related: [cc-hooks, cc-hook-payloads, cc-hook-security, cc-context-budget]
---
A PreToolUse or PostToolUse hook runs on every matching tool call, so its latency is paid hundreds of times a session.

## Verify
- `time (echo '{"hook_event_name":"PreToolUse","tool_name":"Read","tool_input":{}}' | hooks/hook PreToolUse)`: wall time of one cold call.
- `python3 -X importtime hooks/hook PreToolUse < fixture.json 2>&1 | sort -t'|' -k2 -n | tail`: which imports dominate startup.
- `python3 -m json.tool hooks/hooks.json`: every `timeout` is set and small.

## Test first
Assert a latency budget in a test so slowness is a failure.
```python
import json, subprocess, time
def test_pre_tool_use_under_budget():
    payload = json.dumps({"tool_name": "Read", "tool_input": {"file_path": "x"}})
    t = time.perf_counter()
    for _ in range(10):
        subprocess.run(["hooks/hook", "PreToolUse"], input=payload, text=True, capture_output=True)
    assert (time.perf_counter() - t) / 10 < 0.15
```

## Do
- Match narrowly: `matcher` for tools and `if` (for example `Bash(git *)`) so most calls never start your process.
- Keep startup tiny: lazy-import heavy modules after reading the payload, and return early for events you ignore.
- Set `timeout` (seconds, default 600) to a few seconds on tool-path hooks.
- Run slow, non-deciding work in the background with `async: true`, or hand it to a detached process; async hooks cannot block.
- Cache expensive facts (git root, config) in a file keyed by session or mtime.
- Measure with a benchmark script in the repo and keep a p95 budget.
- Use `statusMessage` for any hook that must take noticeable time.

## Avoid
- Running tests, linters or network calls synchronously in PostToolUse: every edit waits. Use `async` or a Stop-time check.
- One interpreter-heavy script per event with many imports: pay the import cost once by lazy-loading, or compile a small launcher.
- A default 600 second timeout on a guard: a hang freezes the session. Set 5 or so.
- Broad matchers (`*`) for hooks that care about one tool: narrow them.
- Assuming async output can steer Claude: asynchronous hooks cannot return a block decision; use `asyncRewake` only to wake on exit 2.
- Injecting large `additionalContext` each prompt: it is paid in tokens every turn. Keep it to a few hundred characters.

## Review
- [ ] p95 hook latency is measured and within budget.
- [ ] Every handler has an explicit `timeout`.
- [ ] Matchers and `if` rules cut needless invocations.
- [ ] Nothing slow runs synchronously on the tool path.
- [ ] Injected context is small.
