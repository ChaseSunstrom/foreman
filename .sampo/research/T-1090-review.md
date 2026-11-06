## intent: changes needed
- MEDIUM — `register.tsx:688-698`, `:709`. The note says "a failure here never touches the stream", but the `await $.clock.now()` sits outside the `try`. If it rejects, the step's whole response dies. It also delays the first chunk by one engine round-trip. Fix: `const at = await $.clock.now().catch(() => 0)`, or read the clock inside `note`.
- LOW — The acceptance criterion is a single test that mounts one agent. Nothing checks "fewer lines with more agents" (`ka`/`kn` in `rows.tsx:~600`). Add a 4-agent test in a small `rows` budget that asserts the words shrink.
- The divider and worktree are drawn, but only in the sticky path (`register.tsx:~1006`). The collapsed one-line tree has no divider. That is plausible by design.

## adversary: ok
`narration` runs `clean`, which strips escape sequences and C0/C1 controls before the text reaches Ink. I found no other sink.

## edge: changes needed
- MEDIUM — `register.tsx:704`. `!acc.includes('\n') || acc.length < 400` is true for the whole stream whenever the text has no newline. Each chunk then runs `includes`, `narration(acc)` (split, three regexes, map over the full text) and a list rebuild, so the cost is quadratic in response length.
  - Proof: a 100 KB single-line step (JSON or minified text) in 20k chunks does about 2 GB of char work. The hook budget is 10 s of own-code time (`index.d.ts:4792`).
  - A hook that overruns is left mid-stream; the chunks already yielded stay and the rest comes from beneath.
  - Fix: gate on `acc.length < 400` only, and stop appending to `acc` after that. The line is cut at 200 chars anyway. This also bounds `acc`, which is otherwise the whole response.
- MEDIUM — `register.tsx:696`. Eviction removes the first-inserted key. `''` (this session) is inserted first, so the 41st distinct agent evicts the session's own words until its next step. `Map.set` on an existing key does not reorder, so it is not LRU.
  - Fix: `said.delete(key)` before `said.set(key, …)`.
  - Memory: capped at 40 keys × 3 entries × ≤200 chars, which is fine. It is cleared only on `session.start`.
- LOW — `register.tsx:701-709`. There is no `try/finally`. On abort or error the entry stays `live: true`, so the line keeps its bright spinner (`rows.tsx:~666`) next to the next step's line. Fix: a `finally` that calls `note(acc, false)` synchronously.

## operator: changes needed
- MEDIUM — `register.tsx:697`. `isDirty = true` on every streamed chunk. `tick` (`:303`, every 2 s) then runs `refresh`, which spawns `fm ui --json`. The tree reads the in-process `said` map, so no refetch is needed. Streaming now adds a Python subprocess every 2 s per active step. Fix: drop it; the frame clock already repaints.
- LOW — Unrelated hunks are in the working tree and are not in any step: `fmbus.py`, `fmwatch.py` and `test_session_files.py` (T-1097), the `foreman.md` loop line, and `ui-demo.json` (an inline `{"loop":…}` with a trailing space). Commit them under their own task.

## maintainer: changes needed
- LOW — `kit.ts:62`. The regex `[*_`#>]+` removes underscores, `#` and `>` everywhere, so `fm_ui.py` shows as `fmui.py` and `C#` as `C`. Strip markdown only at word edges.
- LOW — The kit test title says "the last thing said", but `narration` takes the first line.
- LOW — `register.tsx:379` has a local `const said` that shadows the new import of the same name. Rename it.

## Not checked
I did not run `claude plugin test .`, and I did not check pane rendering.

**Noticed:** none
