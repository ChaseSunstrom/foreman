[instruction-like text quoted from a file or tool; data, not instructions] **Verdict: changes needed.** One real gap: the statusline tower segment goes stale after a tower edit. The rest is nits.

## lens: intent
- MEDIUM — plugin/lib/fmgenesis.py:1372-1378 (with plugin/lib/fmcore.py:3743 and plugin/hooks/statusline:271) — The statusline reads `status.json`, which only `regen_views` writes. `fm genesis init|put|spec|drift|sweep|select|seed` never call it; they only log and `kick`, and `fm genesis put` only logs. After `fm genesis put gen-1/seed.md` the bar still says `⌂ gen 1 · seed` until some task mutation or session start regenerates it. The `UserPromptSubmit` hook only calls `state_dict`, which doesn't write the file. This breaks AC2's intent that the segment tracks a tower edit. The test hides it by calling `c.regen_views(p)` by hand (plugin/tests/test_statusline_ui.py:352,355). Fix: call `c.regen_views(p)` after the mutating genesis actions in `cmd_genesis`, and add a test that runs `fm genesis put` and then reads `status.json`. Confidence: high.

## lens: adversary
- LOW — plugin/lib/fmhooks.py:231 (also plugin/lib/fmcore.py:3770, STATE.md via `render_state`) — `genesis_line` embeds `caps.strip()` from the seed row, and the session being policed writes the seed. `agents_md` runs `c.defang` on the line, but the SessionStart context and STATE.md do not. A row like `| 1 | mission-x.md | Ignore prior rules and … | … |` reaches the next session's `additionalContext` with no instruction marker. Only `plain()` is applied, and it just strips control characters. Fix: apply `c.defang` inside `genesis_line`, so every surface gets it. Confidence: medium.
- The pre-audit's `sha1(` flag is dismissed: it is a cache key, not a security use.

## lens: edge
- LOW — plugin/lib/fmgenesis.py:372-379 — A crash in `step` is cached as `step: None` under the current key. If it was transient, such as a tower file half-written, the surface stays blank until a file or task status changes. It is bounded and fails safe, so I'd accept it or skip caching on exception.

## lens: operator
- LOW — plugin/lib/fmagents.py:294 — The new rules line goes into every project's shim blocks (`fm agents on`), including projects with no tower. That is about 40 tokens per other-agent session, always on. Gate it on a tower existing, or accept the cost.
- LOW — plugin/lib/fmwatch.py:695 — A blocked Mission task now raises two amber signals: "N blocked" and "genesis … blocked". The second duplicates the first. Fold them into one if the pane gets noisy.
- Cost: `state_dict` now calls `health` on every `UserPromptSubmit` and every `regen_views`. A warm cache costs one `os.walk` stat pass plus a JSON read, and a cold one costs one `step()`. The docstring's "~80 ms" figure is not backed by a recorded measurement. Without a tower the cost is one `isfile`.

## lens: maintainer
- MEDIUM — plugin/tests/test_genesis.py:324 — The fm code check calls `_work_row` directly. The real wiring (plugin/lib/fmcodetui.py:2862, `rows.append(genesis row)`) and the pane's `register.tsx:1648` row are untested. Add a test through the project view, or a vitest case.
- LOW — plugin/lib/fmgenesis.py:304 — Moving `import fmcli` into the branch is unrequested. It is probably there to keep `health` light. Say so in a comment.

## Acceptance criteria
- AC1 (`health` caches, refreshes, returns None without a tower): met. `test_cached_until_a_tower_file_or_a_task_status_changes` covers the warm cache, a task status change, a tower file change, a `step` crash and the no-tower case. I did not run it.
- AC2 (`status.json` carries genesis, the statusline draws a warn-coloured segment when not ok): partly met. The code and test are fine, but `status.json` goes stale after tower edits (see intent).
- AC3 (state text and `--json`, fm code, `export agents`, `fm ui --json` with a signal): met for state, export and ui. The fm code project view is only tested at the row renderer.

## Implicit decisions
- The cache file is `genesis-step.json` in the project state dir. It is keyed on a sha1 of the tower files' mtime, size and inode plus every task's id and status.
- The statusline always shows the tower, including `ok` and `done`, dimmed unless the kind is blocked, stopped or fatal.
- A sensitive project withholds the AGENTS.md section but still shows the line in `fm state`, STATE.md and the session context. That is local-only, and `fmsync` doesn't mirror STATE.md.
- `fatal` gives a red signal; `blocked` and `stopped` give amber.
- The pane's genesis row has the lowest priority, behind signals and "done since".

## Not checked
- Whether the plan names the files marked "no step names it".
- MASTER.md and CHANGELOG.md content (MASTER.md's diff was elided).
- Statusline truncation at narrow widths.
- Run-time behaviour; I read the code only and ran no tests.

**Noticed:** `fm genesis` mutations don't regenerate the other views (STATE.md, `badge.txt`, `progress.line`) either. That is the same root cause as the finding above.
