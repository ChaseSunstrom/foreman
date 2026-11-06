---
id: T-3448
type: FIX
tier: S
status: planned
priority: normal
scope: [plugin/lib/sampo/models.py, plugin/lib/sampo/cli.py, plugin/tests/test_models.py, CHANGELOG.md, plugin/tests/helpers.py, plugin/tests/test_live.py]
depends_on: []
source: discovered
created: 2026-11-06T15:19:25Z
updated: 2026-11-06T16:08:40Z
lane: ~/.claude/foreman.lanes/T-3448
base: 9b5639c438e9f1956fa429aabfa14132c50b6872
---
# Other code reads SAMPO_* env names directly after importing sampo.core, whose mirror_env…
## Raw request
> FIX: other code reads SAMPO_* env names directly after importing sampo.core, whose mirror_env renames them to FOREMAN_* (T-3442's cause): SAMPO_CARDS (callcards.py, smallcards.py), SAMPO_SECRETS (models.py:877), SAMPO_CALLCARDS, SAMPO_JEFF_HOME; read both names through one helper, and a test that greps for direct SAMPO_ reads
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] a child sampo started with the parent's call-log path logs there, not under its own home — verify with `python3 plugin/tests/run.py test_models`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test, then read and set the call log under FOREMAN_CALLS (the name mirror_env leaves)
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_models.NoteCallWhere` → ✗ exit 1 · Ran 2 tests in 0.6s (1 jobs, 16 at a time; slowest: NoteCallWhere 0s) / FAILED (1 classes: test_models.NoteCallWhere) [ran] [tree 79b66a63178f] [world 2f1906870a] (2026-11-06T16:05:35Z)
- (step 1) `python3 plugin/tests/run.py test_models test_live` → exit 0 · Ran 185 tests in 28.4s (95 jobs, 16 at a time; slowest: Page.test_the_charts_are_drawn_from_one_kit_labelled_and_readable_in_both_schemes 24s, Page.test_the_network_view_draws_three_columns_and_pulses [ran] [tree 8159c69dcfbe] [world 2f1906870a] (2026-11-06T16:07:16Z)
## Log
- 2026-11-06T15:19:25Z created
- 2026-11-06T16:05:14Z set tier=S, scope=['plugin/lib/sampo/models.py', 'plugin/lib/sampo/cli.py', 'plugin/tests/test_models.py', 'CHANGELOG.md']
- 2026-11-06T16:05:14Z planned: it has criteria and steps
- 2026-11-06T16:05:15Z steer: the others named (SAMPO_CARDS, SAMPO_SECRETS, SAMPO_CALLCARDS, SAMPO_JEFF_HOME) already read both names; SAMPO_CALLS is the one broken: the child's mirror moves the inherited path to FOREMAN_CALLS, then its cli.main sets SAMPO_CALLS to its own temp home, which note_call reads
- 2026-11-06T16:05:15Z lane: ~/.claude/foreman.lanes/T-3448 on foreman/T-3448
- 2026-11-06T16:05:35Z start point recorded late (no focus had kept one): its diff starts at 9b5639c
- 2026-11-06T16:07:17Z set scope=['plugin/lib/sampo/models.py', 'plugin/lib/sampo/cli.py', 'plugin/tests/test_models.py', 'CHANGELOG.md', 'plugin/tests/helpers.py', 'plugin/tests/test_live.py']
- 2026-11-06T16:08:40Z steer: review LOW — sandboxes that drop FOREMAN_* (demo, long, louhi, drill, bench) now don't inherit the call log; before, they inherited SAMPO_CALLS but their own cli.main overwrote it, so they logged to their temp home either way: no change for them
## Follow-ups captured
