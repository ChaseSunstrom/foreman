---
name: cc-plugin-testing
title: Testing plugins
area: claude-code
tags: [claude-code, plugin, testing, fixtures, hooks, validate]
detect: [file:.claude-plugin/plugin.json]
related: [cc-plugins, cc-hooks, cc-plugin-evals, cc-mod-testing, cc-plugin-debugging]
---
Test a plugin in layers: validate the structure, feed fixture payloads to hook scripts, then run a real session against a dev copy.

## Verify
- `claude plugin validate --strict .`: structure layer.
- `python3 -m unittest discover -s tests -t tests`: fixture layer for hook and helper scripts (or your runner of choice).
- `claude --plugin-dir ./plugin -p "ping" --output-format stream-json --verbose | grep plugin_errors`: session layer; the `system/init` event lists `plugin_errors` when a plugin failed to load.
- `claude plugin test <dir>`: for mod plugins.

## Test first
Fixture tests of hook scripts need no model.
```python
import json, subprocess, unittest
def fire(event, payload):
    r = subprocess.run(["hooks/hook", event], input=json.dumps(payload), capture_output=True, text=True, timeout=10)
    return r.returncode, r.stdout
class Guard(unittest.TestCase):
    def test_allows_read(self):
        rc, out = fire("PreToolUse", {"tool_name": "Read", "tool_input": {"file_path": "a"}})
        self.assertEqual(rc, 0)
    def test_blocks_force_push(self):
        rc, out = fire("PreToolUse", {"tool_name": "Bash", "tool_input": {"command": "git push -f origin main"}})
        self.assertTrue(rc == 2 or '"deny"' in out)
```

## Do
- Keep recorded real payloads as JSON fixtures per event, and replay them.
- Test the exit code and the JSON separately; both matter.
- Run scripts against a temporary HOME and a scratch repo so tests never touch real state.
- Test both allow and block paths, plus malformed and empty input.
- Add a latency assertion for tool-path hooks.
- Run headless smoke tests with `--allowedTools` and a low `--max-turns`; add `--bare` plus `--plugin-dir` to isolate from the host's config.
- Keep model-driven checks in evals, and deterministic ones here.

## Avoid
- Only testing with a live model: slow, costly and non-deterministic. Push logic into scripts with fixture tests.
- Tests that read or write the real `~/.claude`: they pass on your machine only and can damage state. Point HOME at a temp dir.
- Fixtures invented from memory: payload shapes drift. Capture real ones with debug logging.
- Asserting on stdout text only: a hook that exits 1 looks fine. Assert the code too.
- Skipping `--strict` validate in CI: warnings today are failures after an update.
- Testing hooks through `claude` alone when a script test would do.

## Review
- [ ] Each hook event has allow, block and malformed fixtures.
- [ ] Tests use temp HOME and scratch repos.
- [ ] Validate runs with `--strict` in CI.
- [ ] A headless smoke test proves the plugin loads.
- [ ] Hook latency is asserted.
