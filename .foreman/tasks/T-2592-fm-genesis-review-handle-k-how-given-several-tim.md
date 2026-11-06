---
id: T-2592
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-02T08:25:50Z
updated: 2026-11-02T09:16:23Z
base: f6e153015a2343136c3c9c9396659dde7583ddaf
base_tree: 3b050b21883f477cec18675eca67c4ebd7eb6314
predict_minutes: 9
predict_attempts: 1
plan0_at: 2026-11-02T08:46:53Z
plan0_scope: []
verified: strong
---
# fm genesis review --handle is repeatable: every K=HOW in one call is applied, none silently dropped
## Raw request
> FIX: fm genesis review --handle K=HOW given several times keeps only the last (argparse store): 12 of 13 handlings in one call were silently lost; make --handle repeatable (action=append) and apply each
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm genesis review N --handle 1=gap --handle '2=dismissed: why' marks both findings and drops both filed tasks; one bad value refuses before any is applied — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_genesis
2. [x] action=append in fmcli and a loop in fmgenesis's review branch
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis` → ✗ exit 1 · Ran 210 tests in 18.4s (24 classes, 16 at a time; slowest: GenesisRead 18s, GenerationReview 16s, GenesisCheck 15s) / FAILED (1 classes: test_genesis.GenerationReview) [ran] [tree 5c5b907793c7] [world 2f1906870a] (2026-11-02T08:47:20Z)
- (step 2) `python3 plugin/tests/run.py test_genesis test_cli` → exit 0 · Ran 354 tests in 24.1s (67 classes, 16 at a time; slowest: TaskLifecycle 24s, GenerationReview 17s, GenesisRead 16s) / OK [ran] [tree 00a821fac331] [world 2f1906870a] (2026-11-02T08:48:28Z)
- `python3 plugin/tests/run.py test_genesis.GenerationReview` → ✗ exit 1 · Ran 7 tests in 10.1s (1 classes, 16 at a time; slowest: GenerationReview 9s) / FAILED (1 classes: test_genesis.GenerationReview) (start tree + this task's tests) [ran] [tree 6465a9696240] [world 2f1906870a] (2026-11-02T08:54:19Z)
- `python3 plugin/tests/run.py test_genesis.GenerationReview` → exit 0 · Ran 7 tests in 9.0s (1 classes, 16 at a time; slowest: GenerationReview 9s) / OK [ran] [tree 6465a9696240] [world 2f1906870a] (2026-11-02T08:54:19Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 210 tests in 15.5s (24 classes, 16 at a time; slowest: GenerationReview 14s, ProofBeforePresentation 12s, GenesisRead 12s) / OK [ran] [tree 6465a9696240] [world 2f1906870a] (2026-11-02T08:54:36Z)
- (step 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 210 tests in 15.5s (24 classes, 16 at a time; slowest: GenerationReview 14s, ProofBeforePresentation 12s, GenesisRead 12s) / OK [ran] [tree 6465a9696240] [world 2f1906870a] (2026-11-02T08:54:36Z)
- (audit intent) `self-review: review_handle takes a str or a list, validates every spec (format and finding number) before any write, applies all, saves once; the CLI's --handle is action=append; the single-str path returns the dict as before` → two --handle values in one call mark both and drop both tasks (CLI test); a bad second value applies neither (test) [tree 6465a9696240] (2026-11-02T08:54:36Z)
- (audit edge) `self-review: review_handle takes a str or a list, validates every spec (format and finding number) before any write, applies all, saves once; the CLI's --handle is action=append; the single-str path returns the dict as before` → the mutate lambda binds how per finding (how=how), so each dropped task logs its own reason; a single --handle still prints one line [tree 6465a9696240] (2026-11-02T08:54:36Z)
- (audit self) `self-review: review_handle takes a str or a list, validates every spec (format and finding number) before any write, applies all, saves once; the CLI's --handle is action=append; the single-str path returns the dict as before` → no findings [tree 6465a9696240] (2026-11-02T08:54:36Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree 773b6e126ee1] [world 2f1906870a] (2026-11-02T09:16:23Z)
## Log
- 2026-11-02T08:25:50Z created
- 2026-11-02T08:26:15Z planned from capture
- 2026-11-02T08:46:52Z set approved=True
- 2026-11-02T08:46:52Z focused
- 2026-11-02T08:46:53Z predicted from its closes: 9 min, 1 attempt(s)
- 2026-11-02T08:48:29Z scope: plugin/lib/fmcli.py — the --handle argument becomes repeatable
- 2026-11-02T08:55:14Z done
- 2026-11-02T08:55:17Z committed cbaef56f (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1124 [FIX S, done, 1 steps] Fm task set ID --section A --text x --section B --text y applies only the last pair silent — lesson: A repeated flag without action=append …
- T-1664 [FEATURE M, done, 4 steps] Backlog extras: good-first list, deferred swipe, learned priorities, spike rule, ticket planner — lesson: a flag a sub-action doesn't r…
- T-1866 [FEATURE M, done, 7 steps] Backlog swipe everywhere: app view, terminal loop, pick explores, prefer --reset — lesson: A loop that applies one verdict at a time mu…
- decision 2026-10-23: T-1623: the five UI contract rules are written down from what the UI playbooks already require: motion (reduced motion as its own path), contrast (p…
## Lessons
- An option a session will repeat must be action=append, or argparse keeps the last value and drops the rest silently
## Plan gaps
- failed first: step 1 red test in test_genesis
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmcli.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
