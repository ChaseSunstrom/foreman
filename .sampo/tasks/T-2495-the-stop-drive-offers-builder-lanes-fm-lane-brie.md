---
id: T-2495
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-01T18:53:08Z
updated: 2026-11-01T19:25:59Z
base: f3c59a14a598c72a36269211efb9a81ece660d82
base_tree: 039c75422ac1f409007fd57112ef2030c5d33c6a
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-01T19:09:47Z
plan0_scope: []
verified: strong
---
# Under economy mode the Stop drive offers main-thread prep, never a builder lane
## Raw request
> FIX: the Stop drive offers builder lanes (fm lane brief + Agent) while economy mode (weekly usage past 80%) forbids subagents, so every stop during a background gate costs a turn declining it; under economy it should offer main-thread prep (read-only diagnosis, drafts) or say wait for the notification
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] with fmbudget.usage_high() true, a planned S/M side task's offer names drafting its red test in the scratchpad and no builder launch; with usage normal and a free lane the builder offer stays — verify with `python3 plugin/tests/run.py test_drive_side test_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_drive_side: the offer under usage_high
2. [x] the drive passes usage_high() to _start_how, which offers scratchpad prep instead of a lane
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_drive_side.EconomyOffer` → ✗ exit 1 · Ran 2 tests in 2.0s (1 classes, 16 at a time; slowest: EconomyOffer 2s) / FAILED (1 classes: test_drive_side.EconomyOffer) [ran] [tree 464e7a473783] (2026-11-01T19:10:14Z)
- (step 1) `python3 plugin/tests/run.py test_drive_side.EconomyOffer` → exit 0 · Ran 2 tests in 2.0s (1 classes, 16 at a time; slowest: EconomyOffer 2s) / OK [ran] [tree 87fd9796ba63] (2026-11-01T19:11:29Z)
- (step 2) `python3 plugin/tests/run.py test_drive_side test_hooks test_budget` → exit 0 · Ran 261 tests in 57.4s (35 classes, 16 at a time; slowest: Stop 57s, NoTaskGate 42s, PreToolUse 36s) / OK [ran] [tree 87fd9796ba63] (2026-11-01T19:12:27Z)
- `python3 plugin/tests/run.py test_drive_side.EconomyOffer` → ✗ exit 1 · Ran 2 tests in 3.2s (1 classes, 16 at a time; slowest: EconomyOffer 2s) / FAILED (1 classes: test_drive_side.EconomyOffer) (start tree + this task's tests) [ran] [tree 87fd9796ba63] (2026-11-01T19:12:33Z)
- `python3 plugin/tests/run.py test_drive_side.EconomyOffer` → exit 0 · Ran 2 tests in 2.1s (1 classes, 16 at a time; slowest: EconomyOffer 2s) / OK [ran] [tree 87fd9796ba63] (2026-11-01T19:12:33Z)
- (ac 1) `python3 plugin/tests/run.py test_drive_side test_hooks` → exit 0 · Ran 252 tests in 41.6s (34 classes, 16 at a time; slowest: Stop 41s, NoTaskGate 26s, PreToolUse 21s) / OK [ran] [tree e731dbac6bc8] (2026-11-01T19:19:05Z)
- (audit edge) `self-review: _economy() reuses fmbudget.usage_high (economy mode's own 80% weekly threshold) and never raises; the economy branch sits after the captured check, so an unplanned item is still offered planning; under 80% the lane offer is unchanged (test pins both)` → unreadable usage reads as not economy, so the lane offer stays; an L or RESEARCH side task under economy also gets scratchpad prep, never fm second plan's model call [tree e731dbac6bc8] (2026-11-01T19:19:05Z)
- (audit self) `self-review: _economy() reuses fmbudget.usage_high (economy mode's own 80% weekly threshold) and never raises; the economy branch sits after the captured check, so an unplanned item is still offered planning; under 80% the lane offer is unchanged (test pins both)` → no findings [tree e731dbac6bc8] (2026-11-01T19:19:05Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm ask: text in a file; a run of a documented command proves it (--yes-run) / · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a f [ran] [tree e731dbac6bc8] (2026-11-01T19:20:41Z)
## Log
- 2026-11-01T18:53:08Z created
- 2026-11-01T18:53:47Z planned from capture
- 2026-11-01T19:09:46Z focused
- 2026-11-01T19:09:47Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-01T19:12:49Z scope: fmhooks _economy + _start_how economy branch, test_drive_side EconomyOffer, MASTER, CHANGELOG
- 2026-11-01T19:20:05Z done
- 2026-11-01T19:20:08Z committed 8df00388 (4 files)
- 2026-11-01T19:20:42Z guard authorization added: publish
- 2026-11-01T19:25:59Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0401 [FIX M, done, 3 steps] Drive: while background work runs, name a concrete queued task to start (builder lane / plan / block), offer up to 3 in turn, then wait — J…
- research mission-20261009-091631.pack: can you spawn a bunch of brainstorm agents to super recursive brainstorm on capabilities/features for foreman itself? not just sim…
- T-1967 [FEATURE M, done, 3 steps] round 12: fm check waits for an ambient run, ambient skips during gates, loop round respects pace — lesson: A slowdown reason from fmbu…
- decision 2026-10-31: [costly] Subagent pace gate hit (weekly usage 75% with 49% of the week gone; T-0320/T-0364's rule, no fm ask category): builders already out keep ru…
## Lessons
- a drive message is a per-turn cost: when a mode forbids the action it offers, the offer must change with the mode (seen live: the economy offer replaced the builder offer at once)
## Plan gaps
- failed first: step 1 red test in test_drive_side: the offer under usage_high
## Files touched
- plugin/tests/test_drive_side.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
- MASTER.md
