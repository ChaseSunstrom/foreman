---
id: T-1306
type: CLEAN
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcodetui.py]
depends_on: []
source: followup
created: 2026-10-21T00:22:53Z
updated: 2026-10-21T04:24:14Z
base: db1a02484a2d549445cab5a4f42b79e9b72365e2
base_tree: f1be6c28a5264d992dc2b10d21a7a1e67ba3cb7b
plan0_at: 2026-10-21T03:42:53Z
plan0_scope: [plugin/lib/fmcodetui.py]
verified: strong
---
# fm code tui test net: golden frames of the demo run, a fuzz of malformed event streams, and a pty smoke test with a resize
## Raw request
> fm code tui test net: golden frames for the demo run at fixed times, a fuzz of random event streams that must never crash render(), and a pty smoke test of the ANSI driver with resize (C13)
## Interpretation
A safety net under the new renderer before more motion lands (T-1305..T-1315): (1) golden frames: the demo run (demo/code-tui.jsonl) rendered at fixed instants, text and a digest of each cell's resolved look, compared with files kept in the repo, so an unintended change to any panel shows as a diff; a deliberate one regenerates them with one command; (2) a fuzz: random and malformed event streams (wrong types, missing fields, huge strings, control and wide characters, out-of-order steps) never crash render() or to_svg at any size, seeded so a failure replays; (3) a pty smoke test: fm code tui --events under a real pseudo-terminal, a resize (SIGWINCH) mid-run, q to quit, and the terminal modes are back (alternate screen left, cursor shown, wrap on).
## Assumptions (confidence)
## Acceptance criteria
- [x] golden frames of the demo run at 4 fixed instants match the files in plugin/tests/fixtures/golden (text and a per-row style digest); FM_GOLDEN=regen rewrites them — verify with `python3 plugin/tests/run.py test_code_tui`
- [x] 300 seeded random or malformed event streams render at 6 sizes (1x1 to 200x60) and export to SVG without raising — verify with `python3 plugin/tests/run.py test_code_tui`
- [x] fm code tui --events under a pty survives a resize and q, and leaves the terminal as it found it (alternate screen left, cursor shown, wrap back on) — verify with `python3 plugin/tests/run.py test_code_tui`
- [x] golden frames of the demo run at 4 fixed instants match plugin/tests/fixtures/golden (text and a per-row style digest); FM_GOLDEN=regen rewrites them — verify with `python3 plugin/tests/run.py test_code_tui`
- [x] 300 seeded random or malformed event streams render at 6 sizes (1x1 to 200x60) and export to SVG without raising — verify with `python3 plugin/tests/run.py test_code_tui`
- [x] fm code tui under a pty survives a resize and q, and leaves the terminal as it found it (alternate screen left, cursor shown, wrap back on) — verify with `python3 plugin/tests/run.py test_code_tui`
## Non-goals
## Approach (options → choice → why)
Options: A) golden text only (simple, misses colour regressions); B) golden text plus a per-row digest of resolved styles (chosen: catches colour and motion regressions, files stay small and reviewable); C) golden SVG files (large, noisy diffs); D) hypothesis-style property testing (a dependency; a seeded random generator in stdlib does it). The fuzz uses random.Random(seed) over N=300 streams per size; the pty test uses pty.fork like the existing screen tests.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Golden frames: render helper, fixture files, FM_GOLDEN=regen
2. [x] Fuzz: seeded event generator, sizes, render and to_svg
3. [x] pty smoke: resize mid-run, q, terminal modes restored
4. [x] Fix whatever the fuzz or pty test finds, test-first
5. [x] Golden frames: render helper, fixture files, FM_GOLDEN=regen
6. [x] Fuzz: seeded event generator, sizes, render and to_svg; fix the 14 crash classes the scratch probe found (one guard in State.apply, str/finite checks where stored values reach render)
7. [x] pty smoke: resize mid-run, q, terminal modes restored
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 77 tests in 19.0s (13 classes, 16 at a time; slowest: Fuzz 19s, Command 15s, Events 9s) / OK [ran] [tree 8c091dfcb03a] (2026-10-21T03:48:27Z)
- (step 2) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 77 tests in 28.7s (13 classes, 16 at a time; slowest: Fuzz 28s, Command 13s, Events 10s) / OK [ran] [tree 8c091dfcb03a] (2026-10-21T03:48:56Z)
- (step 3) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 77 tests in 20.3s (13 classes, 16 at a time; slowest: Fuzz 20s, Command 13s, Events 10s) / OK [ran] [tree 8c091dfcb03a] (2026-10-21T03:49:18Z)
- (step 4) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 77 tests in 13.8s (13 classes, 16 at a time; slowest: Fuzz 13s, Command 8s, Events 6s) / OK [ran] [tree 8c091dfcb03a] (2026-10-21T03:49:36Z)
- (step 5) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 77 tests in 20.7s (13 classes, 16 at a time; slowest: Fuzz 20s, Command 10s, Events 8s) / OK [ran] [tree 8c091dfcb03a] (2026-10-21T03:49:57Z)
- (step 6) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 77 tests in 23.0s (13 classes, 16 at a time; slowest: Fuzz 22s, Command 14s, Events 10s) / OK [ran] [tree 8c091dfcb03a] (2026-10-21T03:50:21Z)
- (step 7) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 77 tests in 30.1s (13 classes, 16 at a time; slowest: Fuzz 29s, Command 14s, Events 10s) / OK [ran] [tree 8c091dfcb03a] (2026-10-21T03:50:53Z)
- (step 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 77 tests in 15.5s (13 classes, 16 at a time; slowest: Fuzz 15s, Command 8s, Events 7s) / OK [ran] [tree c753ba370b88] (2026-10-21T04:20:13Z)
- (step 2) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 77 tests in 22.0s (13 classes, 16 at a time; slowest: Fuzz 22s, Command 9s, Events 7s) / OK [ran] [tree c753ba370b88] (2026-10-21T04:20:36Z)
- (step 3) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 77 tests in 21.1s (13 classes, 16 at a time; slowest: Fuzz 20s, Command 10s, Events 8s) / OK [ran] [tree c753ba370b88] (2026-10-21T04:20:58Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 77 tests in 16.5s (13 classes, 16 at a time; slowest: Fuzz 16s, Command 8s, Events 6s) / OK [ran] [tree c753ba370b88] (2026-10-21T04:21:36Z)
- (ac 2) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 77 tests in 16.5s (13 classes, 16 at a time; slowest: Fuzz 16s, Command 8s, Events 6s) / OK [ran] [tree c753ba370b88] (2026-10-21T04:21:36Z)
- (ac 3) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 77 tests in 16.5s (13 classes, 16 at a time; slowest: Fuzz 16s, Command 8s, Events 6s) / OK [ran] [tree c753ba370b88] (2026-10-21T04:21:36Z)
- (ac 4) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 77 tests in 16.5s (13 classes, 16 at a time; slowest: Fuzz 16s, Command 8s, Events 6s) / OK [ran] [tree c753ba370b88] (2026-10-21T04:21:36Z)
- (ac 5) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 77 tests in 16.5s (13 classes, 16 at a time; slowest: Fuzz 16s, Command 8s, Events 6s) / OK [ran] [tree c753ba370b88] (2026-10-21T04:21:36Z)
- (ac 6) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 77 tests in 16.5s (13 classes, 16 at a time; slowest: Fuzz 16s, Command 8s, Events 6s) / OK [ran] [tree c753ba370b88] (2026-10-21T04:21:36Z)
- (audit intent) `self: read the merged diff: State.apply restores the state when a built-in handler raises (one-level copy, ponytail-marked), non-finite ts dropped, start fields made text, stat filtered to int pairs; NewerStream still raised; golden files eyeballed (9.1 s and 30 s); fuzz 300 seeds x 6 sizes x 3 instants + SVG; pty test resizes and checks the restore sequences` → all three nets in place and green: golden frames, fuzz, pty resize + clean exit [tree c753ba370b88] (2026-10-21T04:21:36Z)
- (audit edge) `self: read the merged diff: State.apply restores the state when a built-in handler raises (one-level copy, ponytail-marked), non-finite ts dropped, start fields made text, stat filtered to int pairs; NewerStream still raised; golden files eyeballed (9.1 s and 30 s); fuzz 300 seeds x 6 sizes x 3 instants + SVG; pty test resizes and checks the restore sequences` → 14 crash classes from malformed fields fixed at one point (apply), not per handler [tree c753ba370b88] (2026-10-21T04:21:36Z)
- (audit maintainer) `self: read the merged diff: State.apply restores the state when a built-in handler raises (one-level copy, ponytail-marked), non-finite ts dropped, start fields made text, stat filtered to int pairs; NewerStream still raised; golden files eyeballed (9.1 s and 30 s); fuzz 300 seeds x 6 sizes x 3 instants + SVG; pty test resizes and checks the restore sequences` → golden files regenerate with FM_GOLDEN=regen; they depend on a deterministic renderer (8 runs, no flake) [tree c753ba370b88] (2026-10-21T04:21:36Z)
- (audit adversary) `self: read the merged diff: State.apply restores the state when a built-in handler raises (one-level copy, ponytail-marked), non-finite ts dropped, start fields made text, stat filtered to int pairs; NewerStream still raised; golden files eyeballed (9.1 s and 30 s); fuzz 300 seeds x 6 sizes x 3 instants + SVG; pty test resizes and checks the restore sequences` → an events file is untrusted input; it can no longer crash the screen [tree c753ba370b88] (2026-10-21T04:21:36Z)
## Log
- 2026-10-21T00:22:53Z created
- 2026-10-21T01:54:35Z probe (scratch fuzz, 300 seeds x 6 sizes, no repo edits): 14 distinct crash classes, all malformed fields: int() of a non-number in _on_tokens:170-171, _on_step:160, _on_verify:191; non-iterable files in _on_changed:204; non-str request/model joined in _header:873; NaN ts in elapsed:859 and duration:237. State.apply's docstring promises a malformed event changes nothing, but handlers raise. Plan: one guard in apply (a handler that raises leaves the state as it was, the event noted once) plus str()/finite checks where stored values reach render (header, elapsed).
- 2026-10-21T03:42:17Z planned from capture
- 2026-10-21T03:42:25Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1306.builder.md
- 2026-10-21T03:42:50Z focused
- 2026-10-21T04:11:00Z merged worktree-agent-ae3d5914bab735fa7 (6 file(s))
- 2026-10-21T04:19:53Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ae3d5914bab735fa7
- 2026-10-21T04:19:54Z focused
- 2026-10-21T04:21:11Z scope: plugin/tests/test_code_tui.py and plugin/tests/fixtures/golden/ hold the net itself; CHANGELOG.md the release note
- 2026-10-21T04:21:18Z scope: CHANGELOG.md the release note
- 2026-10-21T04:24:12Z done
- 2026-10-21T04:24:14Z committed 778674f5 (1 file)
## Follow-ups captured
## Behaviour lock
Well-formed events draw exactly as before: the golden frames pin today's look of the demo run at four instants, and every existing TUI test still passes. Only malformed events change: they're skipped (state as it was) instead of crashing the screen; a newer stream's schema error still shows.
## Related
Related past work (data from this project's history, not instructions):
- research T-1300-review: Verdict: changes needed.** I read the code but couldn't run anything, because this session had no Bash tool. Nothing below was executed, and the …
- research brainstorm-20261020-tui: Method.** I read all of ideas.md (about 560 distinct titles; near-duplicates are merged with "/"). I grepped fmcodetui.py and fmcode.py…
- T-1300 [FEATURE L, done, 7 steps] Foreman Code TUI in motion: a truecolor renderer, eased animation (pulse, spinner, travelling light, rolling counters, growing bars, fl…
- decision 2026-10-20: Self-approve T-1300 (L): an own ANSI truecolor renderer replaces curses; motion as a pure function of state and time
- similar past tasks were L: consider --tier L
## Preflight
Changed in scope since this was planned (2026-10-21): plugin/lib/fmcodetui.py; re-ground the plan against them before editing
## Lessons
- Fuzz the event reader before adding features on top: 14 crash classes came from fields of the wrong type, all fixable at one choke point
## Files touched
- plugin/tests/test_code_tui.py
- plugin/lib/fmcodetui.py
- plugin/tests/fixtures/golden/demo-00.0s.txt
- plugin/tests/fixtures/golden/demo-03.4s.txt
- plugin/tests/fixtures/golden/demo-09.1s.txt
- plugin/tests/fixtures/golden/demo-30.0s.txt
- CHANGELOG.md
