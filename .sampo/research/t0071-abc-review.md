## intent: changes needed

- **MEDIUM** — `plugin/lib/fmcli.py:551-568` (`cmd_focus`/`_moved_since_planned`). `target.set_section("Related", related)` is only called inside the `if not target.section("Related").strip():` block (line 564-565), which runs *before* `moved = _moved_since_planned(p, target)` (line 566) is computed. `moved` is appended to the local `related` string and shown once in this command's own stdout, but is never written back with `set_section`, so `c.save_brief` persists the brief without it. The stated purpose ("re-ground the plan against them before editing", meant to survive for a fresh session) is lost the moment this command's output scrolls away. Fix: call `target.set_section("Related", related)` again after computing `moved`, or move the `set_section` call after both blocks. Confidence: high (read both branches, indentation confirmed).

## adversary: changes needed

- **MEDIUM/HIGH** — `plugin/lib/fmcli.py:224-227`. The out-of-scope-edit gate is silenced forever after the *first* time the word "scope:" appears anywhere in the Log section (`"scope:" not in b.section("Log").lower()`), not tied to the specific files currently outside scope or to when they were logged. One `fm task log ID "scope: because X"` early in a task permanently disables this check for any later, unrelated out-of-scope edits for the rest of the task's life. Fix: only suppress the warning for files/paths actually covered by a scope-log line (or require the log line to postdate the newest out-of-scope touch). Confidence: high.
- **LOW/MEDIUM** — `plugin/lib/fmcli.py:213-214` (`_SIDE_EFFECTS`, `cmd_sentinel`). The denylist used before blindly re-running a past task's recorded verify command is missing common file-mutating commands (`sed -i`, `--fix`/`--write` formatters, `chmod`, `dd`, arbitrary `python -c`). A blocklist for auto-executed historical commands is inherently leaky; an allowlist or a "read-only" heuristic would be safer. Confidence: medium (heuristic gap, not proven exploited).
- Note (acknowledged in code, `fmcore.py:512`): `task_files`/`scope_drift` only see Edit/Write/MultiEdit/NotebookEdit; a Bash-based edit fully evades scope-drift detection. Already flagged with a `ponytail:` comment; just surfacing it.

## edge: changes needed

- **MEDIUM** — `plugin/lib/fmcore.py:512-525` (`task_files`, `first_touch`). Both scan only `ledger_tail(p, 5000)` — a fixed window over the *whole project's shared* ledger, not per-task. For a long-running task in a busy project (many `touched`/`check_run`/`correction` events from other work), the task's early edits can roll out of that window. `first_touch` then silently returns `""`, which makes the CLEAN "behaviour lock" requirement (`fmcli.py:228-232`) skip entirely rather than fire, and `task_files`/`scope_drift` under-report edited files. Confidence: high (verified `ledger_tail` truncation semantics).

## maintainer: nits

- `plugin/lib/fmcli.py:248-252` — `fmrecall.write_tripwires(p)` after `mutate()` only catches `OSError`; any other exception while parsing archived briefs would raise past a task that's already been marked done, producing a confusing failed-looking `fm task done`.
- `plugin/lib/fmcli.py:228` (`_SIDE_EFFECTS.search`) already matches `\bfm\b`; the following `or cmd.startswith("fm check")` is dead/redundant.

## Not checked
Shell scripts/hooks registration, `fmguard.py`, `fmdocs.py`, `fmserve.py`, the plugin test suite under `plugin/tests`, `skills/*` prompt/reference content, and non-diff surrounding code beyond what was needed to verify the above.
