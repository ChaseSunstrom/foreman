---
name: cc-statusline
title: Status line
area: claude-code
tags: [claude-code, statusline, settings, jq, display]
detect: []
related: [cc-settings-permissions, cc-hook-performance, cc-context-budget, cc-mods-ui]
---
The status line is a command from settings that receives session JSON on stdin and prints the bar's text; it is display only.

## Verify
- `echo '{"model":{"display_name":"X"},"context_window":{"used_percentage":12}}' | ./statusline`: prints a line and exits 0.
- `python3 -m json.tool ~/.claude/settings.json`: the `statusLine` entry is valid JSON.
- `time (echo '{}' | ./statusline)`: a cold run is fast, well under 100 ms.
- `echo '{}' | ./statusline | wc -l`: the line count you intend (multiple lines are allowed).

## Test first
Test the formatter with sparse payloads; missing fields are normal.
```python
import json, subprocess
def line(payload):
    return subprocess.run(["./statusline"], input=json.dumps(payload), capture_output=True, text=True).stdout
def test_survives_empty_payload():
    assert line({}).strip() != ""          # never blank, never a traceback
def test_shows_context_percent():
    assert "12%" in line({"context_window": {"used_percentage": 12}})
```

## Do
- Configure in settings: `"statusLine": {"type": "command", "command": "/path/to/statusline"}`, with optional `padding` and `refreshInterval` (seconds, minimum 1) for clocks or idle sessions.
- Read fields defensively: `context_window.used_percentage`, `context_window.context_window_size`, `model.display_name`, `rate_limits.five_hour.used_percentage`; any may be absent.
- Print quickly and exit: updates are debounced 300 ms and an in-flight run is cancelled by the next update.
- Print ANSI colors and several lines when useful; keep each short for narrow terminals.
- Cache slow facts (git branch, queue counts) in a file and refresh them out of band.
- For a plugin-wide default, use the manifest `settings` key; only `agent` and `subagentStatusLine` take effect there.

## Avoid
- Network calls or heavy git commands on every update: the bar lags and gets cancelled. Cache them.
- Crashing on a missing field: the bar goes blank. Default every lookup, and catch top-level errors to print something.
- Setting `refreshInterval` low by habit: it re-runs the command constantly. Use it only for time-based data.
- Writing state or editing files from the status command: it runs far more often than you expect.
- Assuming a plugin can set `statusLine`: only users or managed settings do; a plugin manifest cannot.
- Replacing the user's existing line silently: record the original so it can be restored.

## Review
- [ ] Empty payload prints a sensible line.
- [ ] Cold run is fast; slow data is cached.
- [ ] No side effects.
- [ ] Output width tested at 80 columns.
- [ ] `refreshInterval` unset unless needed.
