---
id: T-2984
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T14:25:49Z
updated: 2026-11-04T14:27:25Z
base: 36c83154e00faa8b6c277b21341985ad71962511
base_tree: 09ba3246ae3ff96b577beabe8dfd8a3df7d0e943
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-04T14:25:50Z
plan0_scope: []
verified: strong
---
# Every card a small model writes is rejected at admission: gemma4:12b answers traps as one string of sentences (and may answer a step as a plain string), and smallcards._clean requires lists, so 400 calls kept 0 cards; parse leniently, check strictly: a traps string splits into its sentences, a string step becomes {do, cmd} with a backticked span as its cmd
## Raw request
> Every card a small model writes is rejected at admission: gemma4:12b answers traps as one string of sentences (and may answer a step as a plain string), and smallcards._clean requires lists, so 400 calls kept 0 cards; parse leniently, check strictly: a traps string splits into its sentences, a string step becomes {do, cmd} with a backticked span as its cmd
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a card with traps as a sentence string and a step as a string is admitted when its content passes, and the strict checks (vague steps, chained shell, unknown commands, too few commands) still reject as before; a one-call grow on the local 12B keeps at least one card — verify with `python3 plugin/tests/run.py test_small_cards`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test with gemma's real reply shape; then _clean's lenient parse
## Resume here
## Docs impact
CHANGELOG line (T-2984)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_small_cards` → exit 0 · Ran 13 tests in 1.1s (3 classes, 16 at a time; slowest: Admit 1s, Grow 1s, Store 0s) / OK [ran] [tree 57dd947ac037] [world 2f1906870a] (2026-11-04T14:26:56Z)
- `python3 plugin/tests/run.py test_small_cards` → ✗ exit 1 · Ran 13 tests in 2.6s (3 classes, 16 at a time; slowest: Admit 1s, Grow 1s, Store 0s) / FAILED (1 classes: test_small_cards.Admit) (start tree + this task's tests) [ran] [tree 57dd947ac037] [world 2f1906870a] (2026-11-04T14:27:01Z)
- `python3 plugin/tests/run.py test_small_cards` → exit 0 · Ran 13 tests in 1.3s (3 classes, 16 at a time; slowest: Admit 1s, Grow 1s, Store 0s) / OK [ran] [tree 57dd947ac037] [world 2f1906870a] (2026-11-04T14:27:01Z)
- (ac 1) `python3 plugin/tests/run.py test_small_cards` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T14:27:01Z [ran] [tree 57dd947ac037] [world 2f1906870a] (2026-11-04T14:27:02Z)
- (audit edge) `self: the shape came from a logging proxy between the grower and Ollama (gemma's real reply); the lenient parse runs before admit's unchanged strict checks` → a traps string splits on sentence ends; a string step's first backticked span is its cmd and the rest its do; the strict checks then refuse a short trap, a vague step, a chained or unknown command, as the test shows [tree 57dd947ac037] (2026-11-04T14:27:02Z)
- (audit adversary) `self: the shape came from a logging proxy between the grower and Ollama (gemma's real reply); the lenient parse runs before admit's unchanged strict checks` → a backticked command still goes through _bad_command (chains, redirects, deletes and unknown first words refused) [tree 57dd947ac037] (2026-11-04T14:27:02Z)
- (audit self) `self: the shape came from a logging proxy between the grower and Ollama (gemma's real reply); the lenient parse runs before admit's unchanged strict checks` → no findings [tree 57dd947ac037] (2026-11-04T14:27:02Z)
## Log
- 2026-11-04T14:25:49Z created
- 2026-11-04T14:25:49Z focused
- 2026-11-04T14:25:50Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-04T14:27:01Z live: a three-call grow on gpu-gemma12-32k kept 2 of 12 (10 refused for commands: sqlfluff and redirects); before the change 1 call kept 0 of 4, all refused for shape (traps as a string)
- 2026-11-04T14:27:23Z done
- 2026-11-04T14:27:25Z committed de9ce0b0 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2909 [FEATURE M, done, 5 steps] Small-model cards part 1: a store of cards written for small models (research/cards/cards.jsonl), a grid (kind of work x stack x stage …
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- playbook Shell script errors (bash -n, ShellCheck, bats) (fm playbooks show build/shell-build)
- decision 2026-11-03: [outward] [cites: user steer: read SAMPO.md (plugin foreman@foreman becomes sampo@sampo; nothing a user already has may break)] [check: pending T-27…
- similar past tasks were M: consider --tier M
- similar finished tasks took 5–5 steps
## Why not caught
the card tests used Claude-shaped fixtures (lists everywhere); the first live grow was the first small-model reply admit ever saw
## Lessons
- Measure a small model's reply shape before blaming its content: one probe through a logging proxy showed every refusal was the shape, not the card
## Files touched
- plugin/tests/test_small_cards.py
- plugin/lib/sampo/smallcards.py
- models.json
- CHANGELOG.md
