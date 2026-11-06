**Verdict: changes needed.** Two MEDIUM issues, one unguarded callback and one control-character leak, plus smaller ones. I could not run the tests because Bash was unavailable to me. Every finding comes from reading the code. Line numbers are working-tree lines.

## lens: adversary / edge
- MEDIUM — plugin/lib/fmcore.py:464 (also :453, :459) — `pump` calls `sink`, `on_line` and `on_idle` with no guard. If one raises, the reader thread dies and nobody drains the pipe. The CLI then blocks on a full 64 KB pipe until `worker_timeout` (1200 s) in `run_bounded`, or `limit` in `_cli`. Trigger: a `Read` tool_use whose `file_path` is `"\ud800"`. `json.loads` keeps the lone surrogate, and `Run.emit` hits `print(text)` at fmcode.py:261 (no `--json`), which raises `UnicodeEncodeError`. A closed stdout, as in `fm code … | head`, has the same effect. Before this change the reader thread only drained and never emitted. Fix: wrap each callback in `try/except Exception` and keep reading, or move the emit off the draining path. — confidence high
- MEDIUM — plugin/lib/fmmodels.py:376 (`stream_tools`), with fmcode.py:261 and :563 — the target is cut with `" ".join(target.split())`, which does not remove ESC (`'\x1b'.isspace()` is False), BEL or C1 `\x9b`. The action name for an unknown tool (`str(name).lower()[:40]`) has the same gap. The TUI is safe (fmcodetui.py:332 and :796 filter with `isprintable`), and `--json` escapes the text. Plain `fm code` output goes straight to `print(text)`. Example: a file claude reads makes it run Bash with `"\u001b]52;c;…\u0007"`, and the terminal acts on it. `answer` already strips these at fmcode.py:1252. Fix: filter with `"".join(c for c in s if c.isprintable())` in `stream_tools` for both target and action. — confidence high
- LOW — plugin/lib/fmcode.py:563 — the live `tool` event target is not passed through `self.redact`. It is redacted only in `self.kept`, the journal copy. The existing `action` event (fmcode.py:659) also goes out unredacted, so this follows precedent. Fix: wrap the target in `self.redact`. — confidence medium
- LOW — plugin/lib/fmmodels.py:435 — `reader.join(5)` can time out when a setsid'd grandchild holds the pipe, and `_cli` has no `reap`. The reader then keeps calling `emit` from a second thread while the main thread emits and writes `self.kept`. `run_bounded` on Linux avoids this because `reap=True`. Fix: close the stream or kill orphans before returning, and ignore late lines. — confidence medium

## lens: intent
- MEDIUM — plugin/lib/fmmodels.py:447 (reached from :444) — a stream whose result line has no string `result` field falls through to `return {"text": stdout.strip()}`, which is the whole raw stream. This happens with `subtype: error_max_turns`, which carries `is_error` but no `result`. The `is_error` check at :450 comes after it. Before this change it was one JSON object, now it can be up to 8 MB handed to the planner's repair loop. Fix: when `stream` is set, raise `ModelError` if `found[-1]` has no string `result`. — confidence medium
- MEDIUM — plugin/lib/fmcode.py:~815 (`all_runners`: `out.setdefault(name,{}).update(mine)`), with fmmodels.py:441 — a `code.toml` override of claude's `plan` or `work` keeps `"stream": "claude"`. Planner turns whose own argv doesn't emit stream-json then fail with "no result line", where they worked before. Fix: drop `stream` when `work` or `plan` is overridden, or set it only if the argv contains `stream-json`. — confidence high
- LOW — the request names "codex (--json)", but only claude is wired. Codex gets heartbeats only. The acceptance criteria name claude only, so this is a scope note, not a criterion failure.

## Questions you asked
1. Deadlock: `run_bounded` merges stderr into stdout, and `_cli` sends stderr to a temp file, so both are drained. A group kill follows a timeout or signal, and the only remaining hang is the callback-exception case above.
2. Single thread: events come from one reader thread per turn. The sole overlap is the post-`join` leak above.
3. Fails loudly: a stream with no result line errors, and codex plain text still becomes the plan. The two exceptions are the missing-`result` stream above and the stale `stream` flag.
4. Injection: the plain output path leaks control characters. The TUI does not.

## Acceptance criteria
- Tool lines from the recorded stream: met in the code and tests, but not run.
- Planner reply and tokens from the result line, malformed lines skipped, no-result error: met, apart from the `error_max_turns` and override edges.
- 10 s heartbeat from the reader thread, shown as one ticking TUI line: met. The `select` timeout fires once overdue unless data is always pending.

## Implicit decisions
- Only claude is wired for streaming, via a `stream: "claude"` key.
- `FM_HEARTBEAT` has a 0.1 s floor.
- A line's trailing partial buffer is capped at 1 MiB.
- A CLI's stdout is kept for its reply up to 8 MiB.

## Not checked
Test execution, the fixture's contents, the TUI layout, and the CHANGELOG and README wording.

Noticed: none
