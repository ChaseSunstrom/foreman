---
id: T-3448
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/models.py, plugin/lib/sampo/cli.py, plugin/tests/test_models.py, CHANGELOG.md, plugin/tests/helpers.py, plugin/tests/test_live.py, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/fleet, .sampo/fleet.md, .sampo/README.md, .sampo/research, .sampo/tasks]
depends_on: []
source: discovered
created: 2026-11-06T15:19:25Z
updated: 2026-11-06T21:59:31Z
base: b2637ff28fed89fb38365309077dd4982e40675f
base_tree: e2603b01514d315470af506975b10c5db03ad682
lane_stop: merged 2026-11-06T17:18:26Z
verified: strong
unproven: [meaning]
---
# Other code reads SAMPO_* env names directly after importing sampo.core, whose mirror_env…
## Raw request
> FIX: other code reads SAMPO_* env names directly after importing sampo.core, whose mirror_env renames them to FOREMAN_* (T-3442's cause): SAMPO_CARDS (callcards.py, smallcards.py), SAMPO_SECRETS (models.py:877), SAMPO_CALLCARDS, SAMPO_JEFF_HOME; read both names through one helper, and a test that greps for direct SAMPO_ reads
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a child sampo started with the parent's call-log path logs there, not under its own home — verify with `python3 plugin/tests/run.py test_models`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test, then read and set the call log under FOREMAN_CALLS (the name mirror_env leaves)
## Resume here
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_models.NoteCallWhere` → ✗ exit 1 · Ran 2 tests in 0.6s (1 jobs, 16 at a time; slowest: NoteCallWhere 0s) / FAILED (1 classes: test_models.NoteCallWhere) [ran] [tree 79b66a63178f] [world 2f1906870a] (2026-11-06T16:05:35Z)
- (step 1) `python3 plugin/tests/run.py test_models test_live` → exit 0 · Ran 185 tests in 28.4s (95 jobs, 16 at a time; slowest: Page.test_the_charts_are_drawn_from_one_kit_labelled_and_readable_in_both_schemes 24s, Page.test_the_network_view_draws_three_columns_and_pulses [ran] [tree 8159c69dcfbe] [world 2f1906870a] (2026-11-06T16:07:16Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree ef6945132ad1] (2026-11-06T17:18:28Z)
- `python3 plugin/tests/run.py test_live test_models` → ✗ exit 1 · Ran 185 tests in 23.0s (51 jobs, 16 at a time; slowest: Page.test_the_charts_are_drawn_from_one_kit_labelled_and_readable_in_both_schemes 21s, Page.test_the_network_view_draws_three_columns_and_pulses (start tree + this task's tests) [ran] [tree ef6945132ad1] [world 2f1906870a] (2026-11-06T17:19:16Z)
- `python3 plugin/tests/run.py test_live test_models` → exit 0 · Ran 185 tests in 21.9s (77 jobs, 16 at a time; slowest: Page.test_the_charts_are_drawn_from_one_kit_labelled_and_readable_in_both_schemes 22s, Page.test_the_network_view_draws_three_columns_and_pulses [ran] [tree ef6945132ad1] [world 2f1906870a] (2026-11-06T17:19:16Z)
- (ac 1) `python3 plugin/tests/run.py test_models` → exit 0 · Ran 90 tests in 16.1s (15 jobs, 16 at a time; slowest: Bench 3s, RunRoute 1s, OpenAIShape 1s) / OK [ran] [tree ef6945132ad1] [world 2f1906870a] (2026-11-06T17:19:36Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree ef6945132ad1] (2026-11-06T17:19:36Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree ef6945132ad1] (2026-11-06T17:19:36Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree ef6945132ad1] (2026-11-06T17:19:36Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree ef6945132ad1] (2026-11-06T17:19:36Z)
## Log
- 2026-11-06T15:19:25Z created
- 2026-11-06T16:05:14Z set tier=S, scope=['plugin/lib/sampo/models.py', 'plugin/lib/sampo/cli.py', 'plugin/tests/test_models.py', 'CHANGELOG.md']
- 2026-11-06T16:05:14Z planned: it has criteria and steps
- 2026-11-06T16:05:15Z steer: the others named (SAMPO_CARDS, SAMPO_SECRETS, SAMPO_CALLCARDS, SAMPO_JEFF_HOME) already read both names; SAMPO_CALLS is the one broken: the child's mirror moves the inherited path to FOREMAN_CALLS, then its cli.main sets SAMPO_CALLS to its own temp home, which note_call reads
- 2026-11-06T16:05:15Z lane: ~/.claude/foreman.lanes/T-3448 on foreman/T-3448
- 2026-11-06T16:05:35Z start point recorded late (no focus had kept one): its diff starts at 9b5639c
- 2026-11-06T16:07:17Z set scope=['plugin/lib/sampo/models.py', 'plugin/lib/sampo/cli.py', 'plugin/tests/test_models.py', 'CHANGELOG.md', 'plugin/tests/helpers.py', 'plugin/tests/test_live.py']
- 2026-11-06T16:08:40Z steer: review LOW — sandboxes that drop FOREMAN_* (demo, long, louhi, drill, bench) now don't inherit the call log; before, they inherited SAMPO_CALLS but their own cli.main overwrote it, so they logged to their temp home either way: no change for them
- 2026-11-06T17:18:26Z merged foreman/T-3448 in merge train
- 2026-11-06T17:18:28Z set scope=['plugin/lib/sampo/models.py', 'plugin/lib/sampo/cli.py', 'plugin/tests/test_models.py', 'CHANGELOG.md', 'plugin/tests/helpers.py', 'plugin/tests/test_live.py', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/fleet', '.sampo/fleet.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks']
- 2026-11-06T17:18:28Z scope: widened at merge to the reviewed lane's own diff (327287498), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T17:23:46Z done
- 2026-11-06T17:23:53Z committed fe4fb1903 (1 file)
- 2026-11-06T21:59:31Z lane removed: ~/.claude/foreman.lanes/T-3448; dropped: its task is closed; the lane was left behind after the merge
## Follow-ups captured
## Why not caught
the builder's own failing test before the fix, then the lane review; no earlier gate covered this path (see the brief's Regression test)
## Lessons
- An env name the CLI sets for its children must be the one mirror_env leaves, or the child's own default overwrites it.
## Plan gaps
- failed first: step 1 failing test, then read and set the call log under FOREMAN_CALLS (the name mirror_env leaves)
## Files touched
- CHANGELOG.md
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/models.py
- plugin/tests/helpers.py
- plugin/tests/test_live.py
- plugin/tests/test_models.py
