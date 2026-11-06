---
id: T-0897
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T16:45:27Z
updated: 2026-10-15T17:02:11Z
base: 8367c00ccf7f564ad77f662379062635fed19c04
base_tree: 22a2b2eaacbc9cf6b1767158992a396047e5f977
verified: strong
---
# Fm spec starts from the input/output examples the user already wrote in the request before
## Raw request
> FEATURE: fm spec starts from the input/output examples the user already wrote in the request before inventing its own
> CONTEXT: round 6 #8. fmchange.py fm spec turns a one-line wish into assertions
## Interpretation
fm spec reads the examples the user already wrote in the wish (name(args) -> value, =>, ==, returns, should be/return, gives) and writes them first, as safe assertions against the module, telling the child to keep them and add others; when the child gives nothing usable, the user's examples alone still make the spec
## Assumptions (confidence)
## Acceptance criteria
- [x] a wish with examples yields those assertions verbatim, first, even if the child fails — verify with `python3 plugin/tests/run.py test_intent`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_intent, then example extraction in fmchange.cmd_spec
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_intent` → exit 0 · Ran 4 tests in 0.6s (2 classes, 16 at a time; slowest: Spec 0s, Rewrite 0s) / OK [ran] [tree 5dfeac6e2ecb] (2026-10-15T17:00:16Z)
- `python3 plugin/tests/run.py test_intent` → ✗ exit 1 · Ran 4 tests in 0.8s (2 classes, 16 at a time; slowest: Rewrite 0s, Spec 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 5dfeac6e2ecb] (2026-10-15T17:00:17Z)
- `python3 plugin/tests/run.py test_intent` → exit 0 · Ran 4 tests in 0.6s (2 classes, 16 at a time; slowest: Spec 0s, Rewrite 0s) / OK [ran] [tree 5dfeac6e2ecb] (2026-10-15T17:00:17Z)
- (ac 1) `python3 plugin/tests/run.py test_intent` → exit 0 · Ran 4 tests in 0.6s (2 classes, 16 at a time; slowest: Spec 0s, Rewrite 0s) / OK [ran] [tree 5dfeac6e2ecb] (2026-10-15T17:02:10Z)
- (audit adversary) `self review: examples parsed deterministically (call -> / => / == / returns / should be|return|equal|give / gives value), prefixed with the module when bare, and passed through the same AST allowlist as the child's lines; written first, deduped against the child's; a failed child no longer loses them` → the user's text goes through safe() exactly like model output (calls only into the module and literals), so an example like __import__('os').system(...) -> 0 is dropped; nothing from the wish is executed except through the written spec, as before [tree 5dfeac6e2ecb] (2026-10-15T17:02:10Z)
- (audit self) `self review: examples parsed deterministically (call -> / => / == / returns / should be|return|equal|give / gives value), prefixed with the module when bare, and passed through the same AST allowlist as the child's lines; written first, deduped against the child's; a failed child no longer loses them` → no findings [tree 5dfeac6e2ecb] (2026-10-15T17:02:10Z)
## Log
- 2026-10-15T16:45:27Z created
- 2026-10-15T16:45:31Z set tier=S
- 2026-10-15T16:59:34Z focused
- 2026-10-15T17:02:10Z done
- 2026-10-15T17:02:11Z committed 45c5d5f (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0713 [FEATURE M, done, 4 steps] Frontier 13 — Intent, planning and change skills — lesson: Generated code is safe to run only through an allowlist of AST shapes; a ren…
- research brainstorm-round6-20261015: Probe: `fm ideas` with user value + bold bets, 2 rounds, past every earlier ideas.md (brainstorm-20261015-113737): 49 new titles, ea…
- T-0702 [FEATURE M, dropped, 3 steps] Frontier 02 — Context firewall and cheap reader
- decision 2026-10-15: Round 6 slate: 6 builds from 49 grounded ideas (salvage on drop, research closes with a decision, fm spec from the user's examples, fm at, promise c…
- similar past tasks were M: consider --tier M
- the similar finished task took 4 steps
## Files touched
- plugin/tests/test_intent.py
- plugin/lib/fmchange.py
