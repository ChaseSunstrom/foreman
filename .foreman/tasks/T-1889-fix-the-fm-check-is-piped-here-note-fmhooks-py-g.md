---
id: T-1889
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-29T00:55:39Z
updated: 2026-10-29T01:58:26Z
base: 91cf61d54f98d84d6de3916abf4f1c16bb4eb80f
base_tree: 163f25f1cf373f0822fd991639773d72fcf8fe33
plan0_at: 2026-10-29T01:41:07Z
plan0_scope: []
verified: strong
---
# The fm check is piped note is given in full once per session
## Raw request
> FIX: the 'fm check is piped here' note (fmhooks.py:_gate_pipe_note) repeats in full every time (8x); after the first in a session give a one-line form, as the stack-card note does
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a second piped gate in a session, after a compaction too, gets a one-line note; another session the full one — verify with `python3 plugin/tests/run.py test_hooks.GatePipe test_hooks.GatePipeOnce`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: GatePipeOnce
2. [x] keep.* session files outlive compaction; _gate_pipe_note short form after the first
3. [x] CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hooks.GatePipeOnce` → red as expected (exit 1) · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: GatePipeOnce 0s) / FAILED (1 classes) [ran] [tree b8ef1a3dbb32] (2026-10-29T01:41:10Z)
- (step 2) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 205 tests in 85.9s (27 classes, 16 at a time; slowest: Stop 85s, NoTaskGate 59s, PreToolUse 55s) / OK [ran] [tree 8b7b96ac4254] (2026-10-29T01:42:40Z)
- (step 3) `grep -c T-1889 CHANGELOG.md` → exit 0 · 1 [ran] [tree 8b7b96ac4254] (2026-10-29T01:42:45Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmhooks.py — commit it through a task, or git checkout it back / fm doctor: OK (48 pass, 6 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                41.1    47.3     150  [0] / SessionEnd                  35.9    43.2     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman- [ran] [tree 8b7b96ac4254] (2026-10-29T01:48:16Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks.GatePipe test_hooks.GatePipeOnce` → exit 0 · Ran 2 tests in 0.4s (2 classes, 16 at a time; slowest: GatePipeOnce 0s, GatePipe 0s) / OK [ran] [tree 8b7b96ac4254] (2026-10-29T01:48:25Z)
- (audit intent) `self-review of the diff plus the lenses below; gates exit 0` → the piped fm check note is said in full once per session, then a one-line reminder; the once-mark survives compaction (keep.* files) [tree 8b7b96ac4254] (2026-10-29T01:48:25Z)
- (audit adversary) `self-review of the diff plus the lenses below; gates exit 0` → no session id gives the full note every time (never silent); another session's mark doesn't shorten this one's [tree 8b7b96ac4254] (2026-10-29T01:48:25Z)
- (audit edge) `self-review of the diff plus the lenses below; gates exit 0` → session_start's cleanup keeps sid.keep.* like sid.taint.*, so a compact doesn't bring the full note back [tree 8b7b96ac4254] (2026-10-29T01:48:25Z)
- (audit self) `self-review of the diff plus the lenses below; gates exit 0` → no findings [tree 8b7b96ac4254] (2026-10-29T01:48:25Z)
- `python3 plugin/tests/run.py test_hooks.GatePipeOnce` → ✗ exit 1 · Ran 1 tests in 1.2s (1 classes, 16 at a time; slowest: GatePipeOnce 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 8b7b96ac4254] (2026-10-29T01:49:18Z)
- `python3 plugin/tests/run.py test_hooks.GatePipeOnce` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: GatePipeOnce 0s) / OK [ran] [tree 8b7b96ac4254] (2026-10-29T01:49:18Z)
- (audit intent) `self-review of the diff plus the lenses below; gates exit 0` → the piped fm check note is said in full once per session, then a one-line reminder; the once-mark survives compaction (keep.* files) [tree 8b7b96ac4254] (2026-10-29T01:49:23Z)
- (audit adversary) `self-review of the diff plus the lenses below; gates exit 0` → no session id gives the full note every time (never silent); another session's mark doesn't shorten this one's [tree 8b7b96ac4254] (2026-10-29T01:49:23Z)
- (audit edge) `self-review of the diff plus the lenses below; gates exit 0` → session_start's cleanup keeps sid.keep.* like sid.taint.*, so a compact doesn't bring the full note back [tree 8b7b96ac4254] (2026-10-29T01:49:23Z)
- (audit self) `self-review of the diff plus the lenses below; gates exit 0` → no findings [tree 8b7b96ac4254] (2026-10-29T01:49:23Z)
## Log
- 2026-10-29T00:55:39Z created
- 2026-10-29T01:09:38Z planned from capture
- 2026-10-29T01:41:07Z focused
- 2026-10-29T01:50:09Z done
- 2026-10-29T01:50:11Z committed ce17e08b (3 files)
- 2026-10-29T01:58:26Z lesson correction: the refusal came from --expect-fail evidence not counting as red (T-1893), not from differing commands
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1814 [FEATURE M, dropped, 0 steps] CLEAN: _gate_pipe_note (fmhooks.py:2089) fires on every piped fm check (13x seen); emit on
- T-1258 [PERFORMANCE M, done, 2 steps] A context-tax ratchet: a replayed hook session's injected bytes per event stay under a bud — lesson: Measure a tax by kind before c…
- T-1762 [FEATURE M, done, 3 steps] fm code app action cards: a failure or a stall shows a card with what happened and one-key next steps, the app sweeps r… — lesson: A pr…
- decision 2026-10-20: Slate, round 1: T-1254 cost per fully-correct session on the Benchmarks page; T-1255 the Claude Code version in every bench result; T-1256 piped tes…
- similar past tasks were M: consider --tier M
## Lessons
- Record red and green with the same test command (or use fm task prove), or finish refuses for want of red-to-green proof
## Files touched
- plugin/tests/test_hooks.py
- CHANGELOG.md
- plugin/lib/fmhooks.py
