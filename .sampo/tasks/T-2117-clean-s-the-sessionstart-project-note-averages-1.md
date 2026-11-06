---
id: T-2117
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T07:46:48Z
updated: 2026-10-30T11:36:59Z
base: b74a315e0d2338c9ea329b7350f9fb6b3498685b
base_tree: d2de22394a2e13033980efe42e87bb38ec769249
plan0_at: 2026-10-30T11:26:11Z
plan0_scope: []
verified: strong
---
# CLEAN S: the SessionStart project note averages 1,932 chars per session (fm friction's…
## Raw request
> CLEAN S: the SessionStart project note averages 1,932 chars per session (fm friction's new T-2109 line): trim it under 1,500 (fold the Usage burn / Blocked / Guard collisions lines into one pointer)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the burn, blocked and guard-collision notes are one Watch: pointer line — verify with `python3 plugin/tests/run.py test_risk test_foresight test_usage_burn`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fold the three into one Watch: line, each to its verb
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_risk test_foresight test_usage_burn` → red as expected (exit 1) · Ran 28 tests in 3.0s (5 classes, 16 at a time; slowest: Risk 3s, Foresight 0s, UsageBurn 0s) / FAILED (1 classes) [ran] [tree b0cd582683d5] (2026-10-30T11:26:15Z)
- (step 1) `python3 plugin/tests/run.py test_risk test_foresight test_usage_burn test_hooks` → ✗ exit 1 · Ran 237 tests in 31.4s (33 classes, 16 at a time; slowest: Stop 31s, NoTaskGate 23s, PreToolUse 18s) / FAILED (1 classes) [ran] [tree 4f97c2bd099c] (2026-10-30T11:26:54Z)
- (step 1) `python3 plugin/tests/run.py test_risk test_foresight test_usage_burn test_hooks` → exit 0 · Ran 237 tests in 31.4s (33 classes, 16 at a time; slowest: Stop 31s, NoTaskGate 23s, PreToolUse 18s) / OK [ran] [tree 368fd0c463ab] (2026-10-30T11:28:09Z)
- (step 1) `python3 plugin/tests/run.py test_risk test_foresight test_usage_burn test_hooks` → exit 0 · Ran 237 tests in 31.5s (33 classes, 16 at a time; slowest: Stop 31s, NoTaskGate 23s, PreToolUse 18s) / OK [ran] [tree 5d58acf778d7] (2026-10-30T11:29:22Z)
- (ac 1) `python3 plugin/tests/run.py test_risk test_foresight test_usage_burn` → exit 0 · Ran 28 tests in 3.0s (5 classes, 16 at a time; slowest: Risk 3s, Foresight 0s, UsageBurn 0s) / OK [ran] [tree 5d58acf778d7] (2026-10-30T11:29:33Z)
- (audit edge) `self: read the diff; each part still fails alone (a bad cache costs only its own item, test_foresight); items are short and name their verb; collision rule text stays c.plain'd from collisions(); fm risk keeps the rewrite (test_risk); measured the live note: 1,888 → 1,646 chars, 1,454 without the transient Setup changed line` → no items → no Watch line; only the tidy item → 'Watch: tidy overdue 12 days → fm tidy.' (test) [tree 5d58acf778d7] (2026-10-30T11:29:33Z)
- (audit self) `self: read the diff; each part still fails alone (a bad cache costs only its own item, test_foresight); items are short and name their verb; collision rule text stays c.plain'd from collisions(); fm risk keeps the rewrite (test_risk); measured the live note: 1,888 → 1,646 chars, 1,454 without the transient Setup changed line` → no findings [tree 5d58acf778d7] (2026-10-30T11:29:33Z)
## Log
- 2026-10-30T07:46:48Z created
- 2026-10-30T07:46:52Z set type=CLEAN, tier=S
- 2026-10-30T11:26:11Z planned: it has criteria and steps
- 2026-10-30T11:26:11Z focused
- 2026-10-30T11:30:10Z done
- 2026-10-30T11:30:11Z committed ff138891 (8 files)
- 2026-10-30T11:34:07Z guard authorization added: publish
- 2026-10-30T11:36:59Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2109 [CLEAN S, done, 1 steps] CLEAN S: friction repeat detector skips SessionStart/UserPromptSubmit…
- T-1797 [FEATURE M, done, 3 steps] CC 2.1.305-2.1.312 adoption: give fm-reviewer/fm-recon an autoCompactWindow; fm doctor poi — lesson: Subagent transcripts carry their p…
- T-1800 [PERFORMANCE M, done, 3 steps] Foreman reasons ahead: names why usage burns, unasked (session start, fm doctor, fm digest) — lesson: Account-wide scans hung on a …
- decision 2026-10-16: T-1242 L plan approval under standard autonomy: the user's explicit request ('showcase that it is able to go for a long time with new ideas, after c…
- similar finished tasks took 1–3 steps
## Files touched
- plugin/tests/test_risk.py
- plugin/lib/fmcost.py
- plugin/lib/fmforesight.py
- plugin/lib/fmhooks.py
- plugin/lib/fmrisk.py
- plugin/tests/test_foresight.py
- CHANGELOG.md
- MASTER.md
