---
id: T-3424
type: FIX
tier: M
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/fleet, .sampo/fleet.md, .sampo/README.md, .sampo/research, .sampo/tasks, plugin/lib/sampo/rune.py, plugin/tests/test_genesis.py]
depends_on: []
source: discovered
created: 2026-11-06T10:23:40Z
updated: 2026-11-07T00:42:48Z
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-06T10:25:05Z
plan0_scope: []
builder_returned: 2026-11-06T10:43:28Z
base: 8b61cb1082cf8cdc9efee5ee9ef7869d024fc263
base_tree: f997eb98c8d4be4238b3699f7edc2ec5717a28e2
lane_stop: merged 2026-11-06T21:46:50Z
verified: strong
unproven: [meaning]
---
# rune._refresh_cards' publish guard compares only card counts, so a degraded export…
## Raw request
> FIX: rune._refresh_cards' publish guard compares only card counts, so a degraded export (all-default kit heights, empty demos, missing images) with an equal count is committed to the public site; add a content check (heights present and varied, every demo non-empty) that fails the refresh
## Interpretation
Reading 1: add a pure content check on the built export, fail the refresh before commit. Reading 2: fix the export itself so it never degrades (T-3228's job, ruled out: the guard must hold for any cause).
## Assumptions (confidence)
## Acceptance criteria
- [x] degraded export is refused, good one passes — verify with `python3 plugin/tests/run.py test_genesis.CardsDegraded`
## Non-goals
## Approach (options → choice → why)
1) one pure helper reading index.json and kit.json; likely outcome: fast, catches the named cases. 2) also parse every shard's per-card demos; fails if too slow (5000 cards). 3) use what exists: compare with the previous export's heights; fails on a legit re-measure. 4) do less: keep the count guard only; fails on the equal-count degraded export (the bug). Choice 1 (80%): fast, pure, covers the named failures.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test then implement _cards_degraded
## Resume here
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_genesis.CardsDegraded 2>&1 | tail -5` → ✗ exit 1 · Ran 1 tests in 55.8s (1 jobs, 16 at a time; slowest: CardsDegraded 0s) / FAILED (1 classes: test_genesis.CardsDegraded) [ran] [tree 90bc1b218589] [world 2f1906870a] (2026-11-06T10:26:21Z)
- (step 1) `python3 plugin/tests/run.py test_genesis.CardsDegraded test_genesis.GenesisLive` → ✗ exit 1 · Ran 9 tests in 74.2s (2 jobs, 16 at a time; slowest: GenesisLive 6s, CardsDegraded 0s) / FAILED (1 classes: test_genesis.CardsDegraded) [ran] [tree ae37161f3448] [world 2f1906870a] (2026-11-06T10:27:44Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis.CardsDegraded 2>&1 | grep -B3 -A12 "^FAIL"` → ✗ exit 1 · Ran 1 tests in 29.4s (1 jobs, 16 at a time; slowest: CardsDegraded 0s) / FAILED (1 classes: test_genesis.CardsDegraded) [ran] [tree ae37161f3448] [world 2f1906870a] (2026-11-06T10:28:15Z)
- (step 1) `python3 plugin/tests/run.py test_genesis.CardsDegraded test_genesis.GenesisLive` → exit 0 · Ran 9 tests in 19.8s (2 jobs, 16 at a time; slowest: GenesisLive 9s, CardsDegraded 0s) / OK [ran] [tree 04a4ae6774c9] [world 2f1906870a] (2026-11-06T10:28:41Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_genesis test_left_out test_models test_moons_scale test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [21.91s] [ran] [tree 04a4ae6774c9] [world 2f1906870a] (2026-11-06T10:30:37Z)
- (step 1) `python3 plugin/tests/run.py test_genesis.CardsDegraded test_genesis.GenesisLive` → exit 0 · Ran 11 tests in 4.5s (2 jobs, 16 at a time; slowest: GenesisLive 4s, CardsDegraded 0s) / OK [ran] [tree c7c44f783c59] [world 2f1906870a] (2026-11-06T10:43:21Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 80570ff48cd2] (2026-11-06T22:25:21Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis.CardsDegraded` → exit 0 · Ran 3 tests in 0.5s (1 jobs, 16 at a time; slowest: CardsDegraded 0s) / OK [ran] [tree 80570ff48cd2] [world 2f1906870a] (2026-11-06T22:25:26Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 80570ff48cd2] (2026-11-06T22:25:26Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 80570ff48cd2] (2026-11-06T22:25:26Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 80570ff48cd2] (2026-11-06T22:25:26Z)
## Log
- 2026-11-06T10:23:40Z created
- 2026-11-06T10:24:52Z planned: it has criteria and steps
- 2026-11-06T10:25:04Z focused
- 2026-11-06T10:25:05Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-06T17:37:52Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aa84c72e440b55592 (branch worktree-agent-aa84c72e440b55592 kept: not merged)
- 2026-11-06T17:37:53Z lane: ~/.claude/foreman.lanes/T-3424 on foreman/T-3424
- 2026-11-06T17:38:50Z focused
- 2026-11-06T21:46:50Z merged foreman/T-3424 in merge train
- 2026-11-06T22:25:20Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/fleet', '.sampo/fleet.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'plugin/lib/sampo/rune.py', 'plugin/tests/test_genesis.py']
- 2026-11-06T22:25:20Z scope: widened at merge to the reviewed lane's own diff (2690da5fa), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T22:26:06Z done
- 2026-11-06T22:26:09Z committed 5353fdd05 (1 file)
- 2026-11-07T00:42:48Z lane removed: ~/.claude/foreman.lanes/T-3424; dropped: merged and closed; the train merge path never removed it
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research readme-site-audit: Seven read-only auditors, one per slice; each claim checked against code and live data. Findings below are verified
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-3266 [FEATURE M, active, 3 steps] Remake the Rune page (site/genesis) in the Sampo look with Kalevala: every tower, the meta-generations and Väinämöinen's acts
- decision 2026-10-23: T-1615: the desk card is a file, never a listener
- similar past tasks were L: consider --tier L
- the similar finished task took 9 steps
## Why not caught
the builder's own failing test before the fix, then the lane review; no earlier gate covered this path (see the brief's Regression test)
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Plan gaps
- failed first: step 1 test then implement _cards_degraded
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/sampo/rune.py
- CHANGELOG.md
