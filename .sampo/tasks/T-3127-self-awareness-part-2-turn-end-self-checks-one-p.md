---
id: T-3127
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/sampo/selfcheck.py, plugin/lib/sampo/core.py, plugin/tests/test_selfcheck.py, CHANGELOG.md, docs/map/**, MASTER.md, plugin/lib/fmselfcheck.py, plugin/lib/sampo/hooks.py, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/fleet, .sampo/fleet.md, .sampo/README.md, .sampo/research, .sampo/tasks, docs/map/files-lib-3.md]
depends_on: []
source: user
created: 2026-11-05T03:20:44Z
updated: 2026-11-06T21:59:28Z
inferred_deps: [T-3123]
inferred_why: T-3123: named in its request
group: self-awareness and miss ledger
base: 81de6117ebb5eb92339e29c572d44667cd4faca5
base_tree: 4292d2cb372e7e78d517e0b86024e6a8727f7921
lane_stop: merged 2026-11-06T18:26:22Z
verified: strong
---
# Self-awareness part 2: turn-end self-checks, one per miss class, that fire with numbers before the user would ask (T-3123)
## Raw request
> Self-awareness part 2: turn-end self-checks, one per miss class, that fire with numbers before the user would ask (T-3123)
## Interpretation
Reading 1 (chosen): the Stop hook runs cheap checks (no model) and names each hit with its numbers: a user-sourced task unmoved for 60 min; a refusal or failure this turn routed around with no capture; a merge or builder slot waiting over 30 min; a store over 500 items with no page that lists it; a target its measured rate can't reach in 30 days; a capability with zero real-work uses in 7 days; a background job whose log or store hasn't changed in 30 min. Each hit is held once per turn like the clause check. Reading 2: a daily report; rejected, tonight's misses cost hours each.
## Assumptions (confidence)
## Acceptance criteria
- [x] sampo next names, with numbers, each of: finished lanes waiting 30+ min (with the train), landed work unshipped 2+ h after the last ship, a retired mirror folder tracked beside the new one, the user's asks from the last 3 days not landed (oldest first); each quiet once resolved; cached so a hook pays one git call per 5 min — verify with `python3 plugin/tests/run.py test_selfcheck`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: the Stop hook's held-once gates, the ledger and events, task sources, lane and merge state, store counts; likely outcome: each class fires on tonight's cases in tests. 2. Do less: three classes; fails if: the user still points out the rest. 3. A model reviews the turn; fails if: models advise, proof decides, and these are countable. Choice 1 (80%)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests per class with fixtures
2. [x] the checks in the Stop hook, held once
3. [x] failing tests per class, then selfcheck.py and its line in next_for
## Resume here
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_selfcheck` → ✗ exit 1 · Ran 5 tests in 1.4s (1 jobs, 16 at a time; slowest: SelfCheck 1s) / FAILED (1 classes: test_selfcheck.SelfCheck) [ran] [tree 5e498adb3416] [world 2f1906870a] (2026-11-06T16:38:06Z)
- (ac 1) `python3 plugin/tests/run.py test_selfcheck` → exit 0 · Ran 5 tests in 13.5s (1 jobs, 16 at a time; slowest: SelfCheck 1s) / OK [ran] [tree f6dd8f50c9ef] [world 2f1906870a] (2026-11-06T16:41:47Z)
- (ac 1) `python3 plugin/tests/run.py test_selfcheck` → exit 0 · Ran 6 tests in 1.4s (1 jobs, 16 at a time; slowest: SelfCheck 1s) / OK [ran] [tree dea84a75f66a] [world 2f1906870a] (2026-11-06T16:54:30Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 0d1b0112a9c9] (2026-11-06T18:32:05Z)
- (step 1) `python3 plugin/tests/run.py test_selfcheck` → exit 0 · Ran 6 tests in 3.7s (1 jobs, 16 at a time; slowest: SelfCheck 2s) / OK [ran] [tree c0181b0bf521] [world 2f1906870a] (2026-11-06T18:34:37Z)
- (step 2) `python3 plugin/tests/run.py test_selfcheck` → exit 0 · Ran 6 tests in 1.6s (1 jobs, 16 at a time; slowest: SelfCheck 1s) / OK [ran] [tree c0181b0bf521] [world 2f1906870a] (2026-11-06T18:34:39Z)
- (step 3) `python3 plugin/tests/run.py test_selfcheck` → exit 0 · Ran 6 tests in 1.4s (1 jobs, 16 at a time; slowest: SelfCheck 1s) / OK [ran] [tree c0181b0bf521] [world 2f1906870a] (2026-11-06T18:34:41Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 43716d582d4e] (2026-11-06T18:54:04Z)
- (ac 1) `python3 plugin/tests/run.py test_selfcheck` → exit 0 · Ran 7 tests in 38.6s (1 jobs, 16 at a time; slowest: SelfCheck 2s) / OK [ran] [tree 43716d582d4e] [world 2f1906870a] (2026-11-06T18:54:49Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 43716d582d4e] (2026-11-06T18:54:49Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 43716d582d4e] (2026-11-06T18:54:49Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 43716d582d4e] (2026-11-06T18:54:49Z)
## Log
- 2026-11-05T03:20:44Z created
- 2026-11-05T03:20:50Z set approved=True
- 2026-11-05T03:20:50Z blocked: approved; waits for a builder slot
- 2026-11-05T03:49:26Z add a class: CI red on main (2026-11-05: the tests workflow red for 14 h, two pushes, unnoticed until the drive offered T-2969)
- 2026-11-05T04:43:24Z stalled-ask check: before flagging a user ask as stalled, test whether it is already built (T-2082/T-1792 sat blocked 6 days on a confirm for pages T-1220 had shipped)
- 2026-11-06T03:52:28Z unblocked
- 2026-11-06T16:35:06Z steer: 2026-11-06 the user asked, unprompted by me: why so many merges wait (train built, unused), why GitHub isn't updated, why .foreman beside .sampo, why the Rune page and the README video aren't done, and 'I shouldn't even need to send any of the messages'. Part 1 here: the classes those questions were — merge wait (with the train), unshipped work, a retired-name folder tracked, user asks not landed — in sampo next and the drive line, numbers first; the rest of the brief's classes stay for part 2
- 2026-11-06T16:35:06Z criterion 1 removed: each class fires on a fixture of tonight's case (the T-3055 merge waiting 3 h behind closes; the 27B never tried on a real task; cards with no page; moons at 3.2% yield against 10,000; the card writer stopped) and stays quiet when the case is resolved; a hit is held once per turn and names its numbers — verify with `python3 plugin/tests/run.py test_self_aware`
- 2026-11-06T16:35:07Z set scope=['plugin/lib/sampo/selfcheck.py', 'plugin/lib/sampo/core.py', 'plugin/tests/test_selfcheck.py', 'CHANGELOG.md', 'docs/map/**', 'MASTER.md']
- 2026-11-06T16:35:08Z lane: ~/.claude/foreman.lanes/T-3127 on foreman/T-3127
- 2026-11-06T16:38:06Z start point recorded late (no focus had kept one): its diff starts at a278d03
- 2026-11-06T16:47:26Z set scope=['plugin/lib/sampo/selfcheck.py', 'plugin/lib/sampo/core.py', 'plugin/tests/test_selfcheck.py', 'CHANGELOG.md', 'docs/map/**', 'MASTER.md', 'plugin/lib/fmselfcheck.py']
- 2026-11-06T16:54:31Z set scope=['plugin/lib/sampo/selfcheck.py', 'plugin/lib/sampo/core.py', 'plugin/tests/test_selfcheck.py', 'CHANGELOG.md', 'docs/map/**', 'MASTER.md', 'plugin/lib/fmselfcheck.py', 'plugin/lib/sampo/hooks.py']
- 2026-11-06T18:26:22Z merged foreman/T-3127 in merge train
- 2026-11-06T18:32:04Z set scope=['plugin/lib/sampo/selfcheck.py', 'plugin/lib/sampo/core.py', 'plugin/tests/test_selfcheck.py', 'CHANGELOG.md', 'docs/map/**', 'MASTER.md', 'plugin/lib/fmselfcheck.py', 'plugin/lib/sampo/hooks.py', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/fleet', '.sampo/fleet.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'docs/map/files-lib-3.md']
- 2026-11-06T18:32:04Z scope: widened at merge to the reviewed lane's own diff (5cc5094f5), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T18:59:14Z done
- 2026-11-06T21:59:28Z lane removed: ~/.claude/foreman.lanes/T-3127; dropped: its task is closed; the lane was left behind after the merge
## Follow-ups captured
## Why not caught
the builder's own failing test before the fix, then the lane review; no earlier gate covered this path (see the brief's Regression test)
## Lessons
- A miss class written only in memory never runs: each one needs a check in the line read every turn.
## Files touched
- CHANGELOG.md
- MASTER.md
- docs/map/files-lib-3.md
- plugin/lib/fmselfcheck.py
- plugin/lib/sampo/core.py
- plugin/lib/sampo/hooks.py
- plugin/lib/sampo/selfcheck.py
- plugin/tests/test_selfcheck.py
