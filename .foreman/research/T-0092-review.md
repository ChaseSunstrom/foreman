**Verdict: approve with nits.** I found no defect that breaks the stated focus checks. I read the diff and the surrounding `statusline` and `fmcore` code. I ran no tests.

**Findings**

- MEDIUM — `plugin/hooks/statusline:310-313`. `snapshot()` runs before `print()`, and it isn't guarded (lines 118-128). If `write_atomic` fails (read-only or full state dir, permissions), the exception reaches `except Exception` at line 323. The output then collapses to the bare word `foreman`. The old path collected its lines first, so a snapshot failure still printed them. A malformed `COLUMNS` (line 1289, `int(...)`) or a missing key in `foreman_segs` does the same. This conflicts with "statusline never fails". Fix: build `out`, print it, then call `snapshot` in its own try/except. Also parse `COLUMNS` defensively. Confidence: high.

- LOW — `mods/foreman-ui/hooks/register.tsx` (`tool.call` handler). `starts.set` and `agentCalls.set` run before the `try/finally`. `await noteSubagent(...)` can reject, for example if `$.agent.list()` fails. When it does, those entries are never deleted. `!starts.size` then stays false, so the clock only stops through the 15-minute `IDLE_FRAMES` cap, and the map entries leak. It is bounded, but "no leak per tool call" isn't strictly met. Fix: move the `try` up to just after `starts.set`, or wrap `noteSubagent` in a catch. Confidence: medium.

- LOW — `register.tsx` ToolUse renderer, `if (!e.props.isRunning) return next(e)`. It checks only `isRunning`. The test props also carry `isErrored` and `isInterrupted`. If the engine ever leaves `isRunning` true on an errored or interrupted row, the animated row would stay up. I couldn't verify engine semantics from the diff. Fix: `if (!e.props.isRunning || e.props.isErrored || e.props.isInterrupted) return next(e)`. Confidence: low.

- LOW — `register.tsx` `advance`. `IDLE_FRAMES` is measured from `lastActive`, and `lastActive` is only refreshed on `wake` (turn start or tool call). A single tool call longer than 15 minutes, such as a long build, freezes its animation. The clock does stop, so this is safe, but the row looks hung. Fix: refresh `lastActive` while `starts.size > 0`, or accept it.

**Dismissed pre-audit items**
- CHANGELOG.md, MASTER.md, README.md, `statusline`, `fmcore.py` and `test_visibility.py` are all edited consistently. No further edit is needed.
- `exec(` is not present in the new code. The only match is the file-level pre-audit flag.

**Acceptance criteria**
- **Statusline layout**: met in code. The default is two lines, or a chip when `foreman-ui@foreman` is enabled. The stack applies only when `statusline_layout` is `"stack"`. With `quick_manifest` returning a manifest, the old path (`start_children(raw, manifest)` then import) is unchanged. When it returns None, the manifest is now loaded after the import, and the result is the same. `test_visibility` pins stack through `setdefault`. The tests themselves weren't run.
- **Mod tests**: the code covers band and pane cards, animated rows for Edit/Bash/Read/Agent via `toolFace`, finished rows passed through, the spinner suffix, and the clock stopping after `turn.complete` (turns and starts both empty, then `sleep()`). Raster is used only when `surface === 'terminal'` (`meter`). Not verifiable without running `claude plugin test`.
- **Mod validates**: not verifiable here.
- **Full suite green**: not verifiable here.

**Not checked**
- I did not run any tests or `claude plugin validate`.
- I did not check the real Claude Code engine semantics of `ToolUse` props or `TurnDuration.durationMs`. The summary is matched by equal `durationMs`, so it breaks if the engine rounds it differently from `turn.complete`.
- I did not check install/uninstall scripts or the e2e suites.
