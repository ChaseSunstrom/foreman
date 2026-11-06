---
id: T-2236
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T23:56:11Z
updated: 2026-10-31T00:26:39Z
base: 0fb1d31baf6955ca1da2c71ed87917dae6a3acd1
base_tree: 52e600a5373e9501cb32f6b53ebcc29380d39053
plan0_at: 2026-10-31T00:14:19Z
plan0_scope: []
verified: strong
---
# fm genesis put: a cold reader's quote with literal \n (it writes newlines as…
## Raw request
> fm genesis put: a cold reader's quote with literal \n (it writes newlines as backslash-n) or one spanning a heading and its next line reads as stray; normalize \n to a space and match a multi-line quote piece by piece against consecutive logical lines
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a cold reader's quote with literal \n, or one spanning a heading and the next line, names the lines it spans; a quote matching nothing still fails closed — verify with `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_quote_spanning_lines_with_a_literal_newline_names_them`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in GenesisRead, then _named splits a quote on newlines (literal or real) and matches each piece against consecutive logical lines
## Resume here
## Docs impact
MASTER.md fmgenesis entry, CHANGELOG Unreleased
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_quote_spanning_lines_with_a_literal_newline_names_them` → ✗ exit 1 · Ran 1 test in 0.258s / FAILED (failures=1) [ran] [tree 023a2efecccc] (2026-10-31T00:14:32Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_genesis` → ✗ exit 1 · Ran 105 tests in 33.222s / FAILED (failures=1) [ran] [tree b0a07b9bb8f5] (2026-10-31T00:15:08Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_genesis && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 105 tests in 7.1s (13 classes, 16 at a time; slowest: GenesisCheck 6s, GenesisRead 5s, GenesisSweep 5s) / FAILED (1 classes) [ran] [tree b0a07b9bb8f5] (2026-10-31T00:15:16Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_genesis` → exit 0 · Ran 105 tests in 32.897s / OK [ran] [tree 77c73590e0d2] (2026-10-31T00:16:42Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_genesis && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.75s] [ran] [tree 77c73590e0d2] (2026-10-31T00:17:01Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_genesis` → exit 0 · Ran 106 tests in 33.468s / OK [ran] [tree 0093f9d38e0c] (2026-10-31T00:21:54Z)
- `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_quote_spanning_lines_with_a_literal_newline_names_them test_genesis.GenesisDrift.test_a_two_line_drift_quote_counts_only_its_last_line` → ✗ exit 1 · Ran 2 tests in 0.404s / FAILED (failures=2) (start tree + this task's tests) [ran] [tree 0093f9d38e0c] (2026-10-31T00:22:50Z)
- `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_quote_spanning_lines_with_a_literal_newline_names_them test_genesis.GenesisDrift.test_a_two_line_drift_quote_counts_only_its_last_line` → exit 0 · Ran 2 tests in 0.396s / OK [ran] [tree 0093f9d38e0c] (2026-10-31T00:22:50Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_quote_spanning_lines_with_a_literal_newline_names_them` → exit 0 · Ran 1 test in 0.267s / OK [ran] [tree 0093f9d38e0c] (2026-10-31T00:23:01Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_quote_spanning_lines_with_a_literal_newline_names_them test_genesis.GenesisDrift.test_a_two_line_drift_quote_counts_only_its_last_line` → exit 0 · Ran 2 tests in 0.408s / OK [ran] [tree 0093f9d38e0c] (2026-10-31T00:23:01Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_quote_spanning_lines_with_a_literal_newline_names_them` → exit 0 · Ran 1 test in 0.267s / OK [ran] [tree 1f80a981fc1c] (2026-10-31T00:23:12Z)
- (audit adversary) `fm-reviewer adversary+edge on the builder's branch: 1 MEDIUM (short pieces dropped, a fail-closed regression) and 2 LOW (DRIFT counted the heading; stray display) fixed test-first by the builder in 90515eb5; test_genesis 106 green` → every non-empty piece must name a line, so a short unmatched fragment can't let a quote pin to an accepted heading and be carried [tree 1f80a981fc1c] (2026-10-31T00:23:12Z)
- (audit edge) `fm-reviewer adversary+edge on the builder's branch: 1 MEDIUM (short pieces dropped, a fail-closed regression) and 2 LOW (DRIFT counted the heading; stray display) fixed test-first by the builder in 90515eb5; test_genesis 106 green` → a quote that is only \n, or has no 8+ character piece, stays stray; DRIFT counts only the last piece's lines [tree 1f80a981fc1c] (2026-10-31T00:23:12Z)
- (audit self) `fm-reviewer adversary+edge on the builder's branch: 1 MEDIUM (short pieces dropped, a fail-closed regression) and 2 LOW (DRIFT counted the heading; stray display) fixed test-first by the builder in 90515eb5; test_genesis 106 green` → no findings [tree 1f80a981fc1c] (2026-10-31T00:23:12Z)
## Log
- 2026-10-30T23:56:11Z created
- 2026-10-31T00:13:08Z set tier=S, type=FIX
- 2026-10-31T00:13:09Z planned: it has criteria and steps
- 2026-10-31T00:14:02Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2236.builder.md
- 2026-10-31T00:14:18Z focused
- 2026-10-31T00:22:42Z merged worktree-agent-ae2c877c93cec5498 (2 file(s))
- 2026-10-31T00:22:47Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ae2c877c93cec5498
- 2026-10-31T00:22:48Z focused
- 2026-10-31T00:23:35Z done
- 2026-10-31T00:23:37Z committed 0bab91a7 (2 files)
- 2026-10-31T00:23:50Z guard authorization added: publish
- 2026-10-31T00:26:39Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2231 [FIX S, done, 1 steps] fm genesis put: a wrapped paragraph is one logical line, so a cold reader's quote across its line break names it (critique puts read such q…
- T-2114 [FIX S, done, 2 steps] FIX S: genesis drift's cold read flags the seed's user-steer section (gen-0 doesn't name… — lesson: A seed that paraphrases gen-0 drifts: q…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- decision 2026-10-30: Genesis drift counts a cold-read DRIFT line only when a seed line holds the quote, and writes the seed's line, never the reader's words
- similar finished tasks took 1–5 steps
## Lessons
- Splitting an untrusted quote into pieces must keep fail-closed per piece: dropping the short ones reopens the hole the stray rule closed
## Plan gaps
- failed first: step 1 red test in GenesisRead, then _named splits a quote on newlines (literal or real) and matches each …
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
