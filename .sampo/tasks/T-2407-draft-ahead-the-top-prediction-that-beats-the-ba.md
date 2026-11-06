---
id: T-2407
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmdraft.py, plugin/lib/fmtriggers.py, plugin/lib/fmcli.py]
depends_on: [T-2355, T-2406]
source: user
created: 2026-10-31T14:33:36Z
updated: 2026-11-01T05:44:30Z
builder_model: sonnet
inferred_deps: [T-2409]
inferred_why: T-2409: draft lane uses the forecast beating the baseline
group: Mission 8 forecasting and watching
base: a3b7b352cfb848b6412563479849f9334dec148b
base_tree: 6937c180ac6eeaae919687542b6e3dd5c8474a19
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-01T05:32:27Z
plan0_scope: [plugin/lib/fmdraft.py, plugin/lib/fmtriggers.py, plugin/lib/fmcli.py]
verified: strong
---
# Draft ahead: the top prediction that beats the baseline is planned in a draft lane on the tick and adopted when the real request overlaps it (Mission 8, #3)
## Raw request
> Draft ahead: the top prediction that beats the baseline is planned in a draft lane on the tick and adopted when the real request overlaps it (Mission 8, #3)
## Interpretation
Reading 1: a predicted request is planned (plan only, no code) in a throwaway draft lane while its kind beats the baseline, and the plan is adopted when a real request overlaps it. Reading 2: draft code too. Rejected for now: tokens and review load on guesses, and plan-only keeps a miss cheap.
## Assumptions (confidence)
## Acceptance criteria
- [x] While the next-request kind beats its baseline, the tick drafts a plan only (no code) for the top prediction in a throwaway draft worktree labelled speculative; nothing is pushed or merged; a draft older than 3 days is removed; a muted kind drafts nothing — verify with `python3 plugin/tests/run.py test_foresight test_triggers`
- [x] Where a task is created (fm task new and the UserPromptSubmit hook's request queueing, T-1242), the adoption check costs one file stat when no draft exists; a user request overlapping a draft by 60%+ of its paths and words gets the drafted plan attached as 'drafted ahead'; one under 20% leaves the draft alone; each adoption and each expiry is scored in fm outcomes --predictions — verify with `python3 plugin/tests/run.py test_foresight`
## Non-goals
## Approach (options → choice → why)
1) A prediction trigger row in the trigger table (T-2355) whose route reaches lane only while the next-request kind beats its baseline (the book from T-2406): fm draft writes a plan only (Interpretation, Approach, acceptance criteria, steps) for the top prediction in its throwaway worktree, labelled speculative, removed after 3 days; when a user request's paths and words overlap a draft by 60%+, the new task gets the plan attached as drafted ahead; under 20% the draft is left alone. Fails if: a bad plan anchors the session, which the label and the 60% bar limit. 2) Use what exists: fm draft (T-1062), which drafts the top queued S task in a throwaway worktree on branch draft/T-x, never merged. Likely outcome: reuse the worktree, expiry and never-merge rules. 3) Do less: show the prediction as a hint only. Fails if: it is advice, not action. 4) Draft code too. Breaks cost on guesses: tokens and review load. Choice 1 (80%): plan-only, gated by a baseline-beating kind.
## Risks and rollback
Blast radius (fm graph blast): co-changes CHANGELOG.md, MASTER.md, plugin/tests/test_cli.py, plugin/lib/fmcore.py, plugin/lib/fmhooks.py; past FIXes T-0875, T-0880, T-0908, T-0926, T-0928.
## Execution prompt
## Steps
1. [x] blocked on T-2355 (the prediction trigger's route comes from its table) and on brief 18's book; start once both are done
2. [x] red tests: plan-only draft while the kind beats its baseline; none when muted; expiry; adoption at 60%, none under 20%
3. [x] draft-ahead in fmdraft, the prediction row, adoption at task creation
4. [x] docs: MASTER, CHANGELOG
## Resume here
## Docs impact
MASTER.md (Draft ahead T-2407 note, section count 22), CHANGELOG.md Unreleased
## Verification evidence
- (step 1) `fm task show T-2355 --json | grep -o '"status": "[a-z]*"' | head -1; fm task show T-2406 --json | grep -o '"status": "[a-z]*"' | head -1` → exit 0 · "status": "done" / "status": "done" [ran] [tree 6937c180ac6e] (2026-11-01T05:32:29Z)
- (step 2) `python3 plugin/tests/run.py test_foresight -k DraftAhead` → ✗ exit 1 · Ran 3 tests in 1.6s (1 classes, 16 at a time; slowest: DraftAhead 1s) / FAILED (1 classes: test_foresight.DraftAhead) [ran] [tree 032e4e734ea9] (2026-11-01T05:32:44Z)
- (step 3) `python3 plugin/tests/run.py test_foresight test_triggers test_draft test_serve` → exit 0 · Ran 87 tests in 16.8s (22 classes, 16 at a time; slowest: Run 16s, RunRoute 10s, PredictionBook 7s) / OK [ran] [tree 91faa94b72be] (2026-11-01T05:33:24Z)
- (ac 1) `python3 plugin/tests/run.py test_foresight test_triggers` → exit 0 · Ran 41 tests in 4.8s (10 classes, 16 at a time; slowest: PredictionBook 4s, DraftAhead 2s, Triggers 1s) / OK [ran] [tree 91faa94b72be] (2026-11-01T05:33:34Z)
- (ac 2) `python3 plugin/tests/run.py test_foresight` → exit 0 · Ran 21 tests in 4.7s (5 classes, 16 at a time; slowest: PredictionBook 4s, DraftAhead 2s, Foresight 0s) / OK [ran] [tree 91faa94b72be] (2026-11-01T05:33:39Z)
- (step 4) `grep -c 'T-2407' MASTER.md CHANGELOG.md; grep -c 'Draft ahead' CHANGELOG.md` → exit 0 · CHANGELOG.md:0 / 1 [ran] [tree b980581cf8ad] (2026-11-01T05:33:49Z)
- `python3 plugin/tests/run.py test_foresight -k DraftAhead` → ✗ exit 1 · Ran 3 tests in 2.6s (1 classes, 16 at a time; slowest: DraftAhead 1s) / FAILED (1 classes: test_foresight.DraftAhead) (start tree + this task's tests) [ran] [tree b980581cf8ad] (2026-11-01T05:33:58Z)
- `python3 plugin/tests/run.py test_foresight -k DraftAhead` → exit 0 · Ran 3 tests in 1.9s (1 classes, 16 at a time; slowest: DraftAhead 2s) / OK [ran] [tree b980581cf8ad] (2026-11-01T05:33:58Z)
- (step 3) `python3 plugin/tests/run.py test_foresight test_triggers test_draft test_serve` → ✗ exit 1 · Ran 87 tests in 18.5s (22 classes, 16 at a time; slowest: Run 18s, RunRoute 8s, PredictionBook 5s) / FAILED (1 classes: test_foresight.DraftAhead) [ran] [tree 173baef057f0] (2026-11-01T05:35:07Z)
- (step 3) `python3 plugin/tests/run.py test_foresight test_triggers test_draft test_serve test_docs` → exit 0 · Ran 190 tests in 15.5s (46 classes, 16 at a time; slowest: Run 15s, RunRoute 9s, Fences 8s) / OK [ran] [tree a2d0ee62b17b] (2026-11-01T05:36:12Z)
- (ac 1) `python3 plugin/tests/run.py test_foresight test_triggers` → exit 0 · Ran 41 tests in 4.7s (10 classes, 16 at a time; slowest: PredictionBook 4s, DraftAhead 2s, Triggers 1s) / OK [ran] [tree a2d0ee62b17b] (2026-11-01T05:36:17Z)
- (ac 2) `python3 plugin/tests/run.py test_foresight` → exit 0 · Ran 21 tests in 4.7s (5 classes, 16 at a time; slowest: PredictionBook 4s, DraftAhead 2s, Foresight 0s) / OK [ran] [tree a2d0ee62b17b] (2026-11-01T05:36:22Z)
- `python3 plugin/tests/run.py test_foresight -k DraftAhead` → ✗ exit 1 · Ran 3 tests in 2.6s (1 classes, 16 at a time; slowest: DraftAhead 1s) / FAILED (1 classes: test_foresight.DraftAhead) (start tree + this task's tests) [ran] [tree a2d0ee62b17b] (2026-11-01T05:38:03Z)
- `python3 plugin/tests/run.py test_foresight -k DraftAhead` → exit 0 · Ran 3 tests in 1.9s (1 classes, 16 at a time; slowest: DraftAhead 2s) / OK [ran] [tree a2d0ee62b17b] (2026-11-01T05:38:03Z)
- (ac 1) `python3 plugin/tests/run.py test_foresight test_triggers` → exit 0 · Ran 41 tests in 4.7s (10 classes, 16 at a time; slowest: PredictionBook 4s, DraftAhead 2s, Triggers 1s) / OK [ran] [tree a2d0ee62b17b] (2026-11-01T05:43:42Z)
- (ac 2) `python3 plugin/tests/run.py test_foresight` → exit 0 · Ran 21 tests in 4.6s (5 classes, 16 at a time; slowest: PredictionBook 4s, DraftAhead 2s, Foresight 0s) / OK [ran] [tree a2d0ee62b17b] (2026-11-01T05:43:42Z)
- (audit intent) `fm check exit 0 (5506 tests); 3 red→green tests (plan-only draft, muted kind and muted route, expiry, adoption at 60%, none under, none for Foreman's own capture); fm task prove proved` → a plan, never code, drafted only while next-request beats its baseline; the user's next matching request gets it as 'Drafted ahead'; adoptions and expiries are scored (draft-ahead in fm outcomes --predictions) [tree a2d0ee62b17b] (2026-11-01T05:43:42Z)
- (audit adversary) `fm check exit 0 (5506 tests); 3 red→green tests (plan-only draft, muted kind and muted route, expiry, adoption at 60%, none under, none for Foreman's own capture); fm task prove proved` → git runs with list args (no shell); the worktree name comes from Foreman's own prediction id, sanitized to [\w.-]; the plan is the user's own past brief text, redacted, its headings stripped so it can't split the brief's sections [tree a2d0ee62b17b] (2026-11-01T05:43:42Z)
- (audit edge) `fm check exit 0 (5506 tests); 3 red→green tests (plan-only draft, muted kind and muted route, expiry, adoption at 60%, none under, none for Foreman's own capture); fm task prove proved` → no HEAD or no git → no draft; a corrupt ahead.json reads as none; a Foreman capture reusing the request's words never adopts (source is the request's, not a reused capture's); fm task new --from a capture keeps the section [tree a2d0ee62b17b] (2026-11-01T05:43:42Z)
## Log
- 2026-10-31T14:33:36Z created
- 2026-10-31T16:08:15Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2407.builder.md
- 2026-10-31T16:08:15Z builder slot freed
- 2026-10-31T16:11:40Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2407.builder.md
- 2026-10-31T16:11:40Z builder slot freed
- 2026-11-01T05:32:26Z focused
- 2026-11-01T05:32:27Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-01T05:34:02Z scope: plugin/tests/test_foresight.py (the tests), plugin/lib/fmforesight.py (the draft-ahead kind in prediction_kinds), plugin/lib/fmnight.py (the tick calls fmdraft.ahead), MASTER.md and CHANGELOG.md (docs)
- 2026-11-01T05:38:03Z scope: plugin/tests/test_foresight.py (the tests), plugin/lib/fmforesight.py (the draft-ahead kind in prediction_kinds), plugin/lib/fmnight.py (the tick calls fmdraft.ahead), MASTER.md and CHANGELOG.md (docs, the section's note count)
- 2026-11-01T05:44:28Z done
- 2026-11-01T05:44:30Z committed 7cb3bb1c (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2406 [FEATURE M, done, 4 steps] Prediction book: Foreman predicts the user's next request from their own request stream and scores each against a naive baseline (Missi…
- T-1062 [FEATURE M, done, 3 steps] Speculative next task: while Claude waits on the user or a long job, the top queued S task — lesson: A headless session needs an explic…
- T-2353 [FEATURE M, done, 3 steps] The router picks the cheapest model that holds: probing down a tier, and fm run uses it too (Mission 8, #9) — lesson: A confirmation st…
- decision 2026-10-31: [cites: user steer 2026-10-31: run the remaining independent missions in parallel lanes] Parallel Missions 5-8 (user steer 2026-10-31): fm lane refu…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_draft.py, plugin/tests/test_triggers.py
## Preflight
Changed in scope since this was planned (2026-10-31): plugin/lib/fmcli.py, plugin/lib/fmtriggers.py; re-ground the plan against them before editing
## Lessons
- Who asked is the request's source, not the brief's: fm task new can reuse a Foreman capture, so a check on b.meta source misreads the user's own request
## Plan gaps
- failed first: step 2 red tests: plan-only draft while the kind beats its baseline; none when muted; expiry; adoption at …
## Files touched
- plugin/tests/test_foresight.py
- plugin/lib/fmdraft.py
- plugin/lib/fmforesight.py
- plugin/lib/fmnight.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
