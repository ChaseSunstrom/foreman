---
id: T-1643
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcritique.py, plugin/tests/test_critique.py, CHANGELOG.md]
depends_on: [T-1642]
source: user
created: 2026-10-22T20:58:07Z
updated: 2026-10-23T03:31:19Z
base: 67a3b2a3e2f2902a527a7de85b006e1fbbbf974c
base_tree: 75dc9b1b7a058c7bf6418d00cb2615835215f50c
plan0_at: 2026-10-23T03:13:51Z
plan0_scope: [plugin/lib/fmcritique.py, plugin/tests/test_critique.py, CHANGELOG.md]
verified: strong
---
# Pseudo-localisation and content-stress strings with surface profiles (TV, e-ink, car, wrist)
## Raw request
> Pseudo-localisation and content-stress strings with surface profiles (TV, e-ink, car, wrist)
## Interpretation
fm critique --stress expands strings for pseudo-localisation (accents, 30–40% longer, brackets to spot truncation, placeholders kept intact) and offers surface profiles (TV at 10 feet, e-ink, car, wrist) as viewport and contrast presets for fm shot and the smoke harness.
## Assumptions (confidence)
## Acceptance criteria
- [x] pseudo-localised strings are longer and keep placeholders — verify with `python3 plugin/tests/run.py test_critique.Pseudo`
## Non-goals
## Approach (options → choice → why)
Options: a translation service (outbound, costly); deterministic pseudo-localisation; skip. Choice: deterministic expansion: the standard technique, testable, no network.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] expander and profile table
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_critique.Pseudo` → ✗ exit 1 · Ran 3 tests in 3.4s (1 classes, 16 at a time; slowest: Pseudo 0s) / FAILED (1 classes) [ran] [tree 0a13e378f8d0] (2026-10-23T03:14:16Z)
- (step 2) `python3 plugin/tests/run.py test_critique.Pseudo` → exit 0 · Ran 3 tests in 1.5s (1 classes, 16 at a time; slowest: Pseudo 1s) / OK [ran] [tree bbbb9fabb14a] (2026-10-23T03:14:48Z)
- (ac 1) `python3 plugin/tests/run.py test_critique.Pseudo 2>&1 | grep -E "^(FAIL|OK)|AssertionError" | head -3` → exit 0 · OK [ran] [tree b81f80f6003c] (2026-10-23T03:29:15Z)
- (step 1) `python3 plugin/tests/run.py test_critique.Pseudo` → red as expected (exit 1) · Ran 3 tests in 0.8s (1 classes, 16 at a time; slowest: Pseudo 0s) / FAILED (1 classes) [ran] [tree 3fa98595c237] (2026-10-23T03:29:24Z)
- (ac 1) `python3 plugin/tests/run.py test_critique test_cli` → exit 0 · Ran 132 tests in 32.7s (39 classes, 16 at a time; slowest: TaskLifecycle 32s, StateViews 11s, AuditPrep 11s) / OK [ran] [tree 5dbea7f6161f] (2026-10-23T03:30:07Z)
- (step 1) `python3 plugin/tests/run.py test_critique.Pseudo` → exit 0 · Ran 3 tests in 0.9s (1 classes, 16 at a time; slowest: Pseudo 0s) / OK [ran] [tree 11069d6e80d1] (2026-10-23T03:30:22Z)
- (ac 1) `python3 plugin/tests/run.py test_critique.Pseudo` → exit 0 · Ran 3 tests in 0.4s (1 classes, 16 at a time; slowest: Pseudo 0s) / OK [ran] [tree 11069d6e80d1] (2026-10-23T03:30:33Z)
- (audit intent) `self: read the diff; the placeholder pattern keeps {n}, {{, %d, %(n)s, ${x}, tags, and now HTML entities (found in review: &amp; became &àmp;, fixed test-first); the flags stand alone; input capped at 2000 characters` → a stress string shows truncation and fixed widths before translators do [tree 11069d6e80d1] (2026-10-23T03:30:33Z)
- (audit edge) `self: read the diff; the placeholder pattern keeps {n}, {{, %d, %(n)s, ${x}, tags, and now HTML entities (found in review: &amp; became &àmp;, fixed test-first); the flags stand alone; input capped at 2000 characters` → empty input prints nothing; a million characters is capped; nested braces {a{b}} are a known ceiling [tree 11069d6e80d1] (2026-10-23T03:30:33Z)
- (audit self) `self: read the diff; the placeholder pattern keeps {n}, {{, %d, %(n)s, ${x}, tags, and now HTML entities (found in review: &amp; became &àmp;, fixed test-first); the flags stand alone; input capped at 2000 characters` → no findings [tree 11069d6e80d1] (2026-10-23T03:30:33Z)
## Log
- 2026-10-22T20:58:07Z created
- 2026-10-22T20:58:08Z set scope=['plugin/lib/fmcritique.py', 'plugin/tests/test_critique.py', 'CHANGELOG.md']
- 2026-10-22T20:58:09Z split from T-1533 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T21:29:57Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_critique.Pseudo`
- 2026-10-22T21:30:20Z criterion 1 text: pseudo-localised strings are longer and keep placeholders — verify with python3 plugin/tests/run.py test_critique.Pseudo → pseudo-localised strings are longer and keep placeholders
- 2026-10-22T23:41:22Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1643.builder.md
- 2026-10-22T23:41:54Z builder slot freed
- 2026-10-23T02:08:52Z set depends_on=['T-1642']
- 2026-10-23T02:08:52Z depends on T-1642: --stress is an fm critique option
- 2026-10-23T03:13:03Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1643.builder.md
- 2026-10-23T03:13:49Z focused
- 2026-10-23T03:29:03Z merged worktree-agent-a07afe577233bd518 (3 file(s))
- 2026-10-23T03:29:03Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a07afe577233bd518
- 2026-10-23T03:29:04Z focused
- 2026-10-23T03:30:32Z scope: plugin/lib/fmcli.py (critique flags), CHANGELOG.md
- 2026-10-23T03:31:16Z done
- 2026-10-23T03:31:19Z committed cd628439 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1533 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Design critique tools: a computed-style census critique, 'why does this
- T-1636 [FEATURE M, done, 3 steps] fm shot: viewport and frame captures and a poster frame per animated page, or a stated reason without a browser — lesson: Headless Chro…
- research T-1509-review: Verdict: changes needed.** The default gate failure (finding 1) and the untested exit-code fix (finding 2) block approval. The rest are nits. [st…
- decision 2026-09-26: Full autonomy never asks mid-run but still can't grant itself core or run destructive/irreversible guard categories: those are recorded with fm ask …
- similar past tasks were M: consider --tier M
- likely tests for the scope: plugin/tests/test_critique.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmcritique.py, plugin/tests/test_critique.py; re-ground the plan against them before editing
## Lessons
- A pseudo-localiser must keep HTML entities as well as format placeholders
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/tests/test_critique.py
- plugin/lib/fmcritique.py
- plugin/lib/fmcli.py
- CHANGELOG.md
